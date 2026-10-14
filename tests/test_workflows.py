# SPDX-FileCopyrightText: 2026 ZarishHealth
# SPDX-License-Identifier: Apache-2.0
"""Regression tests for the workflow compatibility changes in PR #2.

Requires Python 3.9+, Bash, and PyYAML (``python3 -m pip install PyYAML==6.0.3``).
Run from the repository root with:
    python3 -B -m unittest discover -s tests -p 'test_workflows.py' -v

Shell tests execute the scripts read from the workflows in temporary directories.
Docker is replaced by a recording stub; no containers, credentials, GitHub API
calls, repository copies, commits, or pushes are needed. Configuration assertions
cover GitHub Actions wiring; they do not simulate the Actions expression engine.
"""

import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

import yaml


WORKFLOWS = Path(__file__).resolve().parents[1] / ".github" / "workflows"
CHANGED_JOBS = {
    "reuse.yml": "reuse",
    "security.yml": "secret-patterns",
    "sync-brand-to-pages.yml": "mirror",
}
CHECKOUT = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
TOKEN_SECRET = "${{ secrets.PAGES_REPO_TOKEN }}"


def load_workflow(filename):
    return yaml.safe_load((WORKFLOWS / filename).read_text(encoding="utf-8"))


def named_step(job, name):
    matches = [step for step in job["steps"] if step.get("name") == name]
    if len(matches) != 1:
        raise AssertionError(f"Expected one step named {name!r}, found {len(matches)}")
    return matches[0]


def run_bash(script, directory, environment):
    # Use a minimal environment so local credentials and Bash startup hooks cannot
    # enter a workflow script. Each subprocess is bounded and non-interactive.
    return subprocess.run(
        ["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script],
        cwd=directory,
        env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", **environment},
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )


class WorkflowCompatibilityTests(unittest.TestCase):
    def test_changed_jobs_use_ubuntu_24_04(self):
        for filename, job_id in CHANGED_JOBS.items():
            with self.subTest(workflow=filename):
                job = load_workflow(filename)["jobs"][job_id]
                self.assertEqual(job["runs-on"], "ubuntu-24.04")

    def test_every_checkout_uses_the_node_24_compatible_commit(self):
        for filename, job_id in CHANGED_JOBS.items():
            job = load_workflow(filename)["jobs"][job_id]
            checkouts = [
                step for step in job["steps"]
                if step.get("uses", "").startswith("actions/checkout@")
            ]
            with self.subTest(workflow=filename):
                self.assertTrue(checkouts, "The job must still check out its input")
            for step in checkouts:
                with self.subTest(workflow=filename, step=step["name"]):
                    self.assertEqual(step["uses"], CHECKOUT)

    def test_validation_checkouts_do_not_persist_credentials(self):
        for filename, job_id in (
            ("reuse.yml", "reuse"), ("security.yml", "secret-patterns")
        ):
            with self.subTest(workflow=filename):
                job = load_workflow(filename)["jobs"][job_id]
                checkout = named_step(job, "Check out repository")
                self.assertIs(checkout["with"]["persist-credentials"], False)

    def test_reuse_installs_the_pinned_version_before_linting(self):
        job = load_workflow("reuse.yml")["jobs"]["reuse"]
        install = named_step(job, "Install REUSE")
        lint = named_step(job, "Check licensing metadata")
        self.assertEqual(
            shlex.split(install["run"]),
            ["python3", "-m", "pip", "install", "--user", "reuse==6.2.0"],
        )
        self.assertEqual(shlex.split(lint["run"]), ["~/.local/bin/reuse", "lint"])
        self.assertLess(job["steps"].index(install), job["steps"].index(lint))


class GitleaksWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.workflow = load_workflow("security.yml")
        self.job = self.workflow["jobs"]["secret-patterns"]
        self.scan = named_step(self.job, "Run Gitleaks CLI")

    def test_history_scan_checks_out_full_history_before_scanning(self):
        checkout = named_step(self.job, "Check out repository")
        self.assertEqual(checkout["with"]["fetch-depth"], 0)
        self.assertLess(self.job["steps"].index(checkout), self.job["steps"].index(self.scan))

    def test_scanner_needs_no_action_license_or_github_token(self):
        for step in self.job["steps"]:
            self.assertFalse(step.get("uses", "").startswith("gitleaks/gitleaks-action@"))
        self.assertNotIn("uses", self.scan)
        for configuration in (self.workflow, self.job, self.scan):
            for key, value in configuration.get("env", {}).items():
                with self.subTest(environment_variable=key):
                    self.assertNotIn("TOKEN", key.upper())
                    self.assertNotIn("${{ secrets.", str(value))
        self.assertFalse(self.scan.get("continue-on-error", False))

    def run_scanner(self, exit_code):
        with tempfile.TemporaryDirectory(prefix="gitleaks workflow ") as temporary:
            root = Path(temporary)
            executable = root / "docker"
            executable.write_text(
                '#!/bin/sh\nprintf \'%s\\0\' "$@" > "$DOCKER_ARGS_FILE"\n'
                'exit "$DOCKER_TEST_EXIT_CODE"\n',
                encoding="utf-8",
            )
            executable.chmod(0o700)
            arguments_file = root / "docker arguments"
            # A space in the workspace catches accidental removal of shell quotes.
            workspace = root / "source checkout"
            workspace.mkdir()
            script = self.scan["run"].replace("${{ github.workspace }}", str(workspace))
            result = run_bash(script, root, {
                "PATH": f"{root}:/usr/bin:/bin",
                "DOCKER_ARGS_FILE": str(arguments_file),
                "DOCKER_TEST_EXIT_CODE": str(exit_code),
            })
            self.assertTrue(arguments_file.is_file(), "The scanner must invoke Docker")
            arguments = arguments_file.read_bytes().split(b"\0")
            self.assertEqual(arguments.pop(), b"")
            return result, [os.fsdecode(argument) for argument in arguments], workspace

    def test_cli_scans_history_with_a_read_only_mount_and_redacted_output(self):
        result, arguments, workspace = self.run_scanner(0)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(arguments, [
            "run", "--rm",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--volume", f"{workspace}:/repo:ro",
            "--workdir", "/repo",
            "ghcr.io/gitleaks/gitleaks:v8.30.1",
            "git", "--redact", "--verbose", "/repo",
        ])

    def test_leaks_scanner_errors_and_container_failures_fail_the_step(self):
        for exit_code in (1, 2, 125):
            with self.subTest(exit_code=exit_code):
                result, _, _ = self.run_scanner(exit_code)
                self.assertEqual(result.returncode, exit_code, result.stderr)


class MirrorTokenPreflightTests(unittest.TestCase):
    def setUp(self):
        self.job = load_workflow("sync-brand-to-pages.yml")["jobs"]["mirror"]
        self.preflight = named_step(self.job, "Check Pages repository token")

    def run_preflight(self, token, initial_output=""):
        with tempfile.TemporaryDirectory(prefix="mirror preflight ") as temporary:
            root = Path(temporary)
            output = root / "github output"
            if initial_output:
                output.write_text(initial_output, encoding="utf-8")
            environment = {"GITHUB_OUTPUT": str(output)}
            if token is not None:
                environment["PAGES_REPO_TOKEN"] = token
            result = run_bash(self.preflight["run"], root, environment)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.is_file(), "The preflight must set its step output")
            # Only the output file should be created, including for shell-like input.
            self.assertEqual({path.name for path in root.iterdir()}, {output.name})
            if token:
                self.assertNotIn(token, result.stdout + result.stderr)
            return result, output.read_text(encoding="utf-8")

    def test_unset_or_empty_token_reports_unavailable_without_failing(self):
        for token in (None, ""):
            with self.subTest(token=token):
                result, output = self.run_preflight(token)
                self.assertEqual(output, "available=false\n")
                self.assertIn("skipped", result.stdout)

    def test_nonempty_token_reports_available_even_for_false_like_strings(self):
        for token in ("synthetic-pages-token", "false", "0"):
            with self.subTest(token=token):
                result, output = self.run_preflight(token)
                self.assertEqual(output, "available=true\n")
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")

    def test_token_is_literal_data_and_cannot_inject_commands_or_outputs(self):
        token = 'synthetic "token"; $(touch injected); `touch injected`\navailable=false'
        _, output = self.run_preflight(token)
        self.assertEqual(output, "available=true\n")

    def test_preflight_appends_instead_of_overwriting_existing_outputs(self):
        for token, available in ((None, "false"), ("synthetic-pages-token", "true")):
            with self.subTest(available=available):
                _, output = self.run_preflight(token, initial_output="existing=retained\n")
                self.assertEqual(output, f"existing=retained\navailable={available}\n")

    def test_preflight_output_is_wired_to_every_mirror_step(self):
        self.assertIs(self.job["steps"][0], self.preflight)
        self.assertEqual(self.preflight["id"], "token")
        self.assertEqual(self.preflight["shell"], "bash")
        self.assertEqual(self.preflight["env"]["PAGES_REPO_TOKEN"], TOKEN_SECRET)
        self.assertNotIn("if", self.preflight)
        dependent_steps = self.job["steps"][1:]
        self.assertGreaterEqual(len(dependent_steps), 4)
        for step in dependent_steps:
            with self.subTest(step=step["name"]):
                self.assertEqual(step["if"], "steps.token.outputs.available == 'true'")

    def test_only_pages_checkout_retains_credentials_needed_for_push(self):
        source = named_step(self.job, "Check out organization brand source")
        pages = named_step(self.job, "Check out Pages repository")
        push = named_step(self.job, "Commit and push mirror")
        self.assertIs(source["with"]["persist-credentials"], False)
        self.assertNotIn("token", source["with"])
        self.assertEqual(source["with"]["path"], "source")
        self.assertIs(pages["with"]["persist-credentials"], True)
        self.assertEqual(pages["with"]["token"], TOKEN_SECRET)
        self.assertEqual(pages["with"]["repository"], "zarishhealth/zarishhealth.github.io")
        self.assertEqual(pages["with"]["path"], push["working-directory"])


if __name__ == "__main__":
    unittest.main()
