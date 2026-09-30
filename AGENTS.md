# ZarishHealth Organization Context

## Canonical identity

- Organization name: **ZarishHealth** (one word; capital Z and H).
- GitHub organization: <https://github.com/zarishhealth>
- Shared community-health, profile, and brand repository: <https://github.com/zarishhealth/.github>
- Organization profile: `profile/README.md` in this repository.
- Brand guidance: `profile/assets/BRANDING.md`; machine-readable visual identity skill: `profile/assets/SKILL.md`; design tokens: `profile/assets/brand-tokens.json` and `profile/assets/brand.css`.
- Product context, as stated in the organization profile: ZarishHealth is an offline-first, self-hosted, vendor-independent Health Information System for low-resource settings and clinical facilities. Do not invent implementation details, repository names, capabilities, certifications, or regulatory status; inspect the relevant source and authoritative docs first.

## Scope and repository discovery

This repository contains organization-wide GitHub profile/community materials and the brand kit. Do not assume it contains the product application's source code. Before changing another repository, confirm its actual owner, name, default branch, structure, and current instructions. Prefer links under `https://github.com/zarishhealth/` when referring to organization repositories.

Treat security, privacy, and patient-data handling as high priority in any healthcare-related code. Use synthetic test fixtures only; do not expose secrets or patient data in logs, examples, issues, or commits. Do not describe the product or a deployment as HIPAA-, GDPR-, or otherwise compliant/certified without verified evidence for that specific claim.

## Local paths and device references

- Refer to the current user's home directory as `~` or `$HOME`; use repository-relative paths when possible.
- Do not hard-code `/ubuntu`, `/home/ubuntu`, or another username-specific home path in reusable instructions, scripts, examples, or generated content. Do not describe a local device as `/ubuntu`; that is not a portable device name.
- When a concrete path is required, derive it from the active environment's home directory (for example, `$HOME/<project>`), rather than assuming a username or machine layout.

## Brand and naming

Follow `profile/assets/SKILL.md` and `profile/assets/BRANDING.md` for branded material. Keep the product name **ZarishHealth** in prose; lowercase `zarishhealth` is appropriate in handles, URLs, package names, and asset filenames. Do not redraw or alter supplied marks, and do not make unverified medical, regulatory, or security claims.

## Engineering and review

For implementation work, follow the target repository's current instructions, architecture, dependency constraints, and tests. Do not assume paths, frameworks, workflows, services, limits, or MCP integrations from another repository. Make the smallest scoped change, add or update tests where appropriate, and report validation accurately. Prefer pinned, reviewed dependencies and least-privilege credentials for automation; never invent credentials or provider capabilities.
