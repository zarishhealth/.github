# zarishhealth/.github

This is the organization-wide configuration repository for [zarishhealth](https://health.zarishsphere.com).

It contains default files that apply to every repository in the
[zarishhealth](https://github.com/zarishhealth) GitHub organization.

---

## What This Repository Contains

| Path | Purpose | Scope |
|---|---|---|
| `profile/README.md` | Organization homepage at github.com/zarishhealth | Public org profile |
| `profile/assets/` | Shared images and brand assets (logo, banner, favicon) | All repos via raw URL |
| `ISSUE_TEMPLATE/*.yml` | Default issue forms for all repos | All repos |
| `PULL_REQUEST_TEMPLATE.md` | Default PR checklist for all repos | All repos |
| `CONTRIBUTING.md` | Default contribution guide for all repos | All repos |
| `CODE_OF_CONDUCT.md` | Default code of conduct for all repos | All repos |
| `SECURITY.md` | Default security policy for all repos | All repos |
| `SUPPORT.md` | Default support guide for all repos | All repos |
| `FUNDING.yml` | Sponsor button configuration for all repos | All repos |
| `workflows/*.yml` | Reusable GitHub Actions workflows | Called by other repos |
| `labeler.yml` | Auto-label configuration for PRs | Used by pr-labeler workflow |
| `stale.yml` | Stale issue/PR management configuration | Used by stale workflow |


```
.github/          ← This repository

│
├── profile/
│   ├── assets/                             ← ALL image and media files live here
│   │    ├── logo-zarishhealth.png          ← Square logo, 200×200px minimum, transparent background
│   │    ├── logo-zarishhealth-dark.png     ← Dark mode variant (white/light logo for dark backgrounds)
│   │    ├── banner-zarishhealth.png        ← Wide banner, 1280×640px, used in any README header
│   │    ├── favicon-zarishhealth.png       ← 32×32px or 64×64px, used in docs site
│   │    ├── favicon-zarishhealth.ico       ← 16×16 + 32×32 multi-size ICO file, used in HTML sites
│   │    ├── zarishhealth-banner-dark.svg   ← 
│   │    └── zarishhealth-banner-light.svg  ← 
│   └── README.md                           ← The GitHub org homepage (shown at github.com/zarishhealth)
│
├── ISSUE_TEMPLATE/
│   ├── bug_report.yml
│   ├── feature_request.yml
│   ├── country_deployment.yml
│   ├── clinical_content_request.yml
│   └── rfc_proposal.yml
│
├── workflows/
│   ├── ci-go-test.yml
│   ├── ci-go-security.yml
│   ├── ci-node-test.yml
│   ├── ci-fhir-validate.yml
│   ├── release-semantic.yml
│   ├── welcome-first-contributor.yml
│   ├── pr-labeler-auto.yml
│   └── donor-report-monthly.yml
│
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── FUNDING.yml
├── PULL_REQUEST_TEMPLATE.md
├── SECURITY.md
├── SUPPORT.md
├── labeler.yml
├── stale.yml
└── README.md                      ← Explains what this .github repo is (for developers visiting it)
```
---

## How to Override in a Specific Repository

Any repository can override these org defaults by creating its own version of the file.
For example, if `zs-core` needs a different `CONTRIBUTING.md`, create one at
`zarishhealth/zs-core/CONTRIBUTING.md` and GitHub will use that instead of this default.

---

## Asset URLs

Brand assets stored in `profile/assets/` are available at:

https://raw.githubusercontent.com/zarishhealth/.github/main/profile/assets/[filename]

Reference these URLs in any README, documentation page, or web application across the organization.

---

## Maintainers

This repository is owned by `@zarishhealth/team-community` and `@zarishhealth/owners`.
Changes require review from at least one owner.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to propose changes.
---
