# ZarishHealth Organization `.github` repository

This repository contains the ZarishHealth GitHub organization profile, community-health files, Issue/PR templates, governance workflows, reusable workflows, workflow template, and shared brand kit.

- Organization profile: [`profile/README.md`](profile/README.md)
- Brand guidelines: [`profile/assets/BRANDING.md`](profile/assets/BRANDING.md)
- Security policy: [`SECURITY.md`](SECURITY.md)
- Public security metadata: [`/.well-known/security.txt`](.well-known/security.txt)

Purpose:
- Reusable workflows for CI, docs and pages publishing
- Organization-wide ISSUE_TEMPLATEs and PULL_REQUEST_TEMPLATE
- Global Dependabot configuration
- Workflow templates for repo creation

Do not commit secrets here. Keep this repository public so reusable workflows can be referenced by org repositories.

---

## `.github` Repository Tree

```text
.github/                              ← the repository
├── .github/
│   ├── workflows/
│   │   ├── reusable-rust-ci.yml     
│   │   ├── reusable-docs-pages.yml
│   │   ├── sync-brand-to-pages.yml   
│   │   └── lint.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── ISSUE_TEMPLATE/
│   ├── bug-report.yml
│   ├── field-report.yml
│   ├── feature-request.yml
│   └── config.yml
├── workflow-templates/
│   ├── rust-ci.yml
│   └── rust-ci.properties.json
├── profile/
│   ├── README.md                    
│   └── assets/                       ← brand kit (unchanged names)
├── AGENTS.md
├── CODE_OF_CONDUCT.md
├── CODE_OF_CONDUCT.bn.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── SECURITY.md
├── SUPPORT.md
├── LICENSE                           ← Apache-2.0 (code) — see §15
├── LICENSES/                         ← REUSE: Apache-2.0.txt, CC-BY-4.0.txt, MIT.txt
└── REUSE.toml
```
---
