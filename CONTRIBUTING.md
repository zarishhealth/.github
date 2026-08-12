# Contributing to ZarishHealth

Thank you for your interest in contributing. ZarishHealth is a platform-of-platforms for national digital health. Every contribution — code, documentation, translation, clinical expertise, or governance feedback — makes it better.

---

## Who Can Contribute

Anyone. Code is not required. The most impactful contributions are often documentation, clinical form design, and governance feedback from people who understand health systems — not just software.

---

## Ways to Contribute

### Without Writing Code

- **Open an Issue** — report a bug, describe a clinical workflow, or suggest a feature
- **Review an RFC** — read open RFCs at [zs-rfc](https://github.com/zarishhealth/zs-rfc) and comment
- **Write or improve documentation** — every repository has a `docs/` folder
- **Design a clinical form** — use [forms.zarishsphere.com](https://forms.zarishsphere.com) — no coding needed
- **Translate the interface** — join the translation project at [zs-contrib-translations](https://github.com/zarishhealth/zs-contrib-translations)
- **Share a case study** — document how a health facility or country could use ZarishSphere

### With Code

- **Fix a bug** — look for issues labeled `good first issue` or `help wanted`
- **Build a new ESM module** — fork [zs-esm-template-app](https://github.com/zarishhealth/zs-esm-template-app)
- **Improve a content package** — add clinical concepts or forms to any `zs-content-*` repository
- **Write a new IaC module** — add deployment support in [zs-infra-opentofu](https://github.com/zarishhealth/zs-infra-opentofu)

---

## The Contribution Process

1. **Find or open an Issue** describing the problem or change
2. **Discuss** the approach in the Issue comments before writing code
3. **Fork** the repository and create a branch: `git checkout -b feat/my-change`
4. **Write the documentation first** — update `docs/` or `README.md` before writing implementation
5. **Write or update tests** — all code changes require tests
6. **Open a Pull Request** — reference the Issue number in the PR description
7. **Respond to review comments** — at least one maintainer must approve before merge
8. **Celebrate** — your name appears in the CHANGELOG forever

---

## Commit Message Format

I use [Conventional Commits](https://www.conventionalcommits.org). Every commit must follow this format:

```
type(scope): short description

Optional longer body explaining why, not what.
```

Valid types: `feat`, `fix`, `docs`, `chore`, `security`, `content`, `infra`, `i18n`, `perf`

Examples:
- `feat(patient): add FHIR R5 Patient registration endpoint`
- `fix(auth): correct SMART on FHIR token scope validation`
- `docs(deployment): add Raspberry Pi offline setup guide`
- `content(maternal): add WHO ANC 2024 form schema`

---

## Code Standards

| Language | Formatter | Linter |
|---|---|---|
| Go | `gofmt` | `golangci-lint` |
| TypeScript | Biome v2 | ESLint |
| Dart (Flutter) | `dart format` | `flutter analyze` |
| YAML | Prettier | yamllint |
| Markdown | Prettier | markdownlint |

All formatters run automatically in CI. A PR that fails formatting will not be merged.

---

## Branch Naming

| Branch Type | Pattern | Example |
|---|---|---|
| Feature | `feat/short-description` | `feat/fhir-r5-patient-search` |
| Bug fix | `fix/short-description` | `fix/keycloak-token-expiry` |
| Documentation | `docs/short-description` | `docs/refugee-deployment-guide` |
| Content | `content/short-description` | `content/who-anc-2024-forms` |
| Infrastructure | `infra/short-description` | `infra/raspberry-pi-opentofu-module` |

---

## RFC Process — For Major Changes

Any change that affects more than one repository, or changes an architectural principle, requires an RFC.

1. Copy the RFC template from `zs-rfc/template.md`
2. Create a new file: `rfcs/YYYY-NNN-short-title.md`
3. Open a Pull Request — this begins the community review period (minimum 14 days)
4. After consensus, the RFC is merged as Accepted
5. Implementation follows the accepted RFC — not before

---

## Clinical Content Standards

All clinical content (forms, concepts, order sets) must:

- Reference a published standard (WHO, ICD-11, LOINC, SNOMED CT, CIEL)
- Include the standard's version and reference URL
- Be reviewed by at least one clinical professional before merge
- Use `CC0 1.0` license (public domain) — clinical content is never proprietary

---

## Code of Conduct

This project follows the [Contributor Covenant 2.1](CODE_OF_CONDUCT.md). All contributors agree to uphold its standards. Violations are reported to [platform@zarishsphere.com](mailto:platform@zarishsphere.com).

---

## First-Time Contributors

Look for issues labeled **`good first issue`**. These are specifically chosen because they:
- Have a clearly defined scope
- Require no prior knowledge of the full codebase
- Have a maintainer available to answer questions

When you open your first PR, our welcome bot will greet you and connect you to resources.

---

## Questions

- **GitHub Discussions:** https://github.com/orgs/zarishhealth/discussions
- **Email:** platform@zarishsphere.com
- **Documentation:** https://docs.zarishsphere.com