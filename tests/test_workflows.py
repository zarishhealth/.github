# SPDX-FileCopyrightText: 2026 ZarishHealth
# SPDX-License-Identifier: Apache-2.0
"""Regression tests for the workflow compatibility changes in PR #2.

Requires Python 3.9+, PyYAML, and Bash. From the repository root:
    python3 -m unittest discover -s tests -p 'test_workflows.py' -v

Tests read the actual workflow YAML and execute only isolated step scripts.
Docker and pip are replaced by shell functions; no network, container, GitHub
credentials, asset copying, commits, or pushes are needed.
"""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml


WORKFLOW_DIRECTORY = Path(__file__).resolve().parents[1] / ".github" / "workflows"
CHECKOUT_ACTION = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
GITLEAKS_IMAGE = "ghcr.io/gitleaks/gitleaks:v8.30.1"
TOKEN_GUARD = "steps.token.outputs.available == 'true'"
WORKFLOW_JOBS = {
    "reuse.yml": "reuse",
    "security.yml": "secret-patterns",
    "sync-brand-to-pages.yml": "mirror",
}


class WorkflowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.jobs = {}
        for filename, job_id in WORKFLOW_JOBS.items():
            workflow = yaml.safe_load(
                (WORKFLOW_DIRECTORY / filename).read_text(encoding="utf-8")
            )
            cls.jobs[filename] = workflow["jobs"][job_id]

    def setUp(self):
        temporary_directory = tempfile.TemporaryDirectory(prefix="workflow-tests-")
        self.addCleanup(temporary_directory.cleanup)
        self.workspace = Path(temporary_directory.name) / "workspace with spaces"
        self.workspace.mkdir()

    def step(self, filename, name):
        matches = [
            step for step in self.jobs[filename]["steps"] if step.get("name") == name
        ]
        self.assertEqual(len(matches), 1, f"Expected one step named {name!r}")
        return matches[0]

    def run_shell(self, script, extra_environment=None):
        # Do not inherit real runner tokens, BASH_ENV, or shell startup settings.
        environment = {"PATH": os.defpath, "HOME": str(self.workspace), "LANG": "C"}
        environment.update(extra_environment or {})
        return subprocess.run(
            ["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script],
            cwd=self.workspace,
            env=environment,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )


class CheckoutCompatibilityTests(WorkflowTestCase):
    def test_changed_jobs_use_the_pinned_ubuntu_runner(self):
        for filename, job in self.jobs.items():
            with self.subTest(workflow=filename):
                self.assertEqual(job["runs-on"], "ubuntu-24.04")

    def test_all_checkouts_use_the_node_24_compatible_commit(self):
        for filename, expected_count in (
            ("reuse.yml", 1),
            ("security.yml", 1),
            ("sync-brand-to-pages.yml", 2),
        ):
            with self.subTest(workflow=filename):
                checkouts = [
                    step
                    for step in self.jobs[filename]["steps"]
                    if step.get("uses", "").startswith("actions/checkout@")
                ]
                self.assertEqual(len(checkouts), expected_count)
                for checkout in checkouts:
                    self.assertEqual(checkout["uses"], CHECKOUT_ACTION)

    def test_read_only_source_checkouts_do_not_persist_credentials(self):
        for filename, name in (
            ("reuse.yml", "Check out repository"),
            ("security.yml", "Check out repository"),
            ("sync-brand-to-pages.yml", "Check out organization brand source"),
        ):
            with self.subTest(workflow=filename):
                self.assertIs(
                    self.step(filename, name)["with"]["persist-credentials"], False
                )

    def test_pages_checkout_retains_only_the_explicit_mirror_credentials(self):
        checkout = self.step("sync-brand-to-pages.yml", "Check out Pages repository")
        self.assertEqual(
            checkout["with"]["repository"], "zarishhealth/zarishhealth.github.io"
        )
        self.assertEqual(checkout["with"]["token"], "${{ secrets.PAGES_REPO_TOKEN }}")
        self.assertIs(checkout["with"]["persist-credentials"], True)


class ReuseInstallationTests(WorkflowTestCase):
    def test_installs_the_pinned_reuse_version_in_the_user_environment(self):
        script = self.step("reuse.yml", "Install REUSE")["run"]
        result = self.run_shell('python3() { printf "%s\\0" "$@"; };\n' + script)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.split("\0")[:-1],
            ["-m", "pip", "install", "--user", "reuse==6.2.0"],
        )

    def test_failed_reuse_installation_fails_the_step(self):
        script = self.step("reuse.yml", "Install REUSE")["run"]
        result = self.run_shell("python3() { return 23; };\n" + script)
        self.assertEqual(result.returncode, 23)


class GitleaksCliTests(WorkflowTestCase):
    def scanner_script(self):
        script = self.step("security.yml", "Run Gitleaks CLI")["run"]
        # Emulate the single GitHub expression needed by this step, using a
        # synthetic workspace. Never execute commands against the real checkout.
        self.assertIn("${{ github.workspace }}", script)
        return script.replace("${{ github.workspace }}", str(self.workspace))

    def test_cli_scans_git_history_with_redaction_and_a_read_only_mount(self):
        result = self.run_shell(
            'docker() { printf "%s\\0" "$@"; };\n' + self.scanner_script()
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.split("\0")[:-1],
            [
                "run",
                "--rm",
                "--user",
                f"{os.getuid()}:{os.getgid()}",
                "--volume",
                f"{self.workspace}:/repo:ro",
                "--workdir",
                "/repo",
                GITLEAKS_IMAGE,
                "git",
                "--redact",
                "--verbose",
                "/repo",
            ],
        )

    def test_leaks_and_container_errors_fail_the_scan_step(self):
        for exit_code in (1, 125):
            with self.subTest(exit_code=exit_code):
                result = self.run_shell(
                    f"docker() {{ return {exit_code}; }};\n" + self.scanner_script()
                )
                self.assertEqual(result.returncode, exit_code)

    def test_history_is_available_before_the_git_scan(self):
        checkout = self.step("security.yml", "Check out repository")
        self.assertEqual(checkout["with"]["fetch-depth"], 0)
        steps = self.jobs["security.yml"]["steps"]
        scanner = self.step("security.yml", "Run Gitleaks CLI")
        self.assertLess(steps.index(checkout), steps.index(scanner))

    def test_scanner_does_not_depend_on_the_organization_licensed_action_or_tokens(self):
        job = self.jobs["security.yml"]
        for step in job["steps"]:
            self.assertFalse(
                step.get("uses", "").startswith("gitleaks/gitleaks-action@")
            )
        scanner = self.step("security.yml", "Run Gitleaks CLI")
        self.assertNotIn("secrets.", scanner["run"])
        for environment in (job.get("env", {}), scanner.get("env", {})):
            self.assertNotIn("GITHUB_TOKEN", environment)
            self.assertNotIn("GITLEAKS_LICENSE", environment)


class PagesTokenPreflightTests(WorkflowTestCase):
    def preflight(self):
        return self.step("sync-brand-to-pages.yml", "Check Pages repository token")

    def run_preflight(self, token=None, initial_output=None):
        output = self.workspace / "github output.txt"
        if initial_output is None:
            output.unlink(missing_ok=True)
        else:
            output.write_text(initial_output, encoding="utf-8")
        environment = {"GITHUB_OUTPUT": str(output)}
        if token is not None:
            environment["PAGES_REPO_TOKEN"] = token
        result = self.run_shell(self.preflight()["run"], environment)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result, output.read_text(encoding="utf-8")

    def test_preflight_receives_the_secret_without_a_conditional(self):
        preflight = self.preflight()
        self.assertEqual(preflight["id"], "token")
        self.assertEqual(preflight["shell"], "bash")
        self.assertEqual(
            preflight["env"]["PAGES_REPO_TOKEN"], "${{ secrets.PAGES_REPO_TOKEN }}"
        )
        self.assertNotIn("if", preflight)

    def test_missing_and_empty_tokens_disable_mirroring_with_a_clear_message(self):
        for token in (None, ""):
            with self.subTest(token=token):
                result, output = self.run_preflight(token)
                self.assertEqual(output, "available=false\n")
                self.assertIn("mirror steps will be skipped", result.stdout)
                self.assertEqual(result.stderr, "")

    def test_nonempty_tokens_enable_mirroring_without_being_logged(self):
        for token in ("synthetic-test-token", "x", " ", "synthetic\nmultiline"):
            with self.subTest(token=repr(token)):
                result, output = self.run_preflight(token)
                self.assertEqual(output, "available=true\n")
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")

    def test_token_shell_metacharacters_are_never_executed(self):
        token = '$(touch injected); `touch injected`; "quoted"; $HOME; *'
        result, output = self.run_preflight(token)
        self.assertEqual(output, "available=true\n")
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")
        self.assertFalse((self.workspace / "injected").exists())

    def test_preflight_appends_to_the_existing_output_file(self):
        for token, expected in ((None, "false"), ("synthetic-test-token", "true")):
            with self.subTest(available=expected):
                _, output = self.run_preflight(
                    token, initial_output="previous=preserved\n"
                )
                self.assertEqual(output, f"previous=preserved\navailable={expected}\n")

    def test_output_write_failure_fails_the_preflight(self):
        for token in ("", "synthetic-test-token"):
            with self.subTest(token=token):
                result = self.run_shell(
                    self.preflight()["run"],
                    {
                        "PAGES_REPO_TOKEN": token,
                        # A directory cannot accept GitHub step output records.
                        "GITHUB_OUTPUT": str(self.workspace),
                    },
                )
                self.assertNotEqual(result.returncode, 0)

    def test_every_mirror_step_is_gated_after_the_preflight(self):
        steps = self.jobs["sync-brand-to-pages.yml"]["steps"]
        self.assertEqual(steps[0], self.preflight())
        downstream_steps = steps[1:]
        # Check both checkout actions and both side-effecting scripts so an
        # absent token cannot reach the asset copy or push steps either.
        self.assertEqual(len(downstream_steps), 4)
        for step in downstream_steps:
            with self.subTest(step=step["name"]):
                self.assertEqual(step.get("if"), TOKEN_GUARD)


if __name__ == "__main__":
    unittest.main()
