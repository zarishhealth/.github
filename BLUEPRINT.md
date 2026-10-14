# ZARISHHEALTH — Organization Blueprint

**Version 2.0.0 · 2026-10-14 · Status: proposal for adoption**
**Organization:** <https://github.com/zarishhealth>
**Supersedes:** `DRAFT_BLUEPRINT_ZARISHHEALTH.md`, `DRAFT_ZARISHHEALTH.md` (both drafts are merged and reconciled here)

> This document defines how every repository, directory, file, URL, API path, MCP server and well-known document of the ZarishHealth GitHub organization is named, laid out and published, so that **every path can be used as a URI/URL/API/MCP endpoint without renaming**.
> Standards were checked against current sources on 2026-10-14. Where a standard is still a draft or unsettled, this document says so (see §3 and §19).

---

## 0. How to read this

| You want to… | Go to |
| --- | --- |
| Know what changed from the drafts and why | §1 |
| Understand the "no custom domain" consequences | §2 |
| See the standards this blueprint is built on | §3 |
| Name a repo, branch, file, crate, image, endpoint | §4 |
| See the repository catalog and every repo's layout | §5, §6 |
| Design a URL, API path, FHIR path or MCP tool | §7–§10 |
| Know which `/.well-known/` file lives where | §11 |
| Fix the current repositories | §17 |

---

## 1. Decisions and corrections to the drafts

### 1.1 Decisions (the reconciled architecture)

| # | Decision | Reason |
| --- | --- | --- |
| D1 | **Rust backend**: Axum 0.8 + Tokio + SQLx; Tauri v2 for desktop/mobile shells; embedded SQLite at sites; PostgreSQL only at the optional central tier | Your stated requirement; matches both drafts |
| D2 | **Local-first**: every site works with its uplink cut. The central tier is optional and is never a dependency | Matches the org profile's rule ("a site must remain fully operational with its uplink cut") |
| D3 | **Few repositories first** (≈14), Cargo **workspace monorepo** for Rust code; split a crate into its own repo only when it needs an independent release cadence or owner | The 105-repo plan is not maintainable by a small team; every extra repo multiplies CI, security and naming work |
| D4 | **One path layout on every origin** (laptop, LAN, cloud). The hostname is configuration, never code | You own no domain (see §2) |
| D5 | **Clinical data is only under `/fhir`**; the native API (`/api/v1`) never duplicates clinical resources | Prevents two competing data models |
| D6 | **Native API errors use RFC 9457** `application/problem+json`; the FHIR endpoint uses `OperationOutcome` | Each is the standard for its surface |
| D7 | **Resource IDs are opaque UUIDv7 (RFC 9562)**, generated on the device | Safe offline generation, time-sortable for sync, and no personal data in URLs (replaces UUIDv4 and the DOB/NID-embedded IDs, see §14) |
| D8 | **Naming is lowercase kebab-case everywhere except where an external standard mandates otherwise** (Rust `snake_case` source, FHIR `PascalCase` resource types, conventional root files like `README.md`) | One rule, few exceptions, all listed in §4.9 |

### 1.2 Problems found in the drafts (not carried forward)

| Draft claim or practice | Problem | Replacement |
| --- | --- | --- |
| `api.zarishhealth.com`, `health.zarishhealth.com`, `zarishhealth.org`, `admin@zarishhealth.com`, `health-coc@zarishsphere.com` | You own none of these domains | §2 origin model; GitHub private vulnerability reporting |
| Four GitHub organizations "to yield 8,000 free build minutes" | Splitting orgs to multiply free quotas is likely to conflict with GitHub's terms and fragments governance. Also unnecessary: standard runners on **public** repositories are free | One organization |
| Repo names such as `zs-fhir-rust-server`, `zs-esm-patient-chart` | The Rust API Guidelines say crate names should not carry `-rs`/`-rust`; an org-wide `zs-` prefix duplicates the org namespace | §4.1, §4.6 |
| Keycloak for every tier | Java server; contradicts the 18–30 MB, 512 MB-RAM field target and offline operation | Embedded OAuth/OIDC issuer in the Rust server for sites; Keycloak (or any OIDC provider) optional at HQ (§12) |
| Personal Google Drive `appDataFolder` and Supabase/Render **free tiers** as PHI stores | No data-processing agreement, free-tier pausing, wrong jurisdiction control | Synthetic data only until a hosting decision is made (§14) |
| `local_sync_key` plaintext and bcrypt hashes in a `config.json` committed to Git | Secrets in version control | Secrets never in Git; per-site secrets provisioned at install (§14) |
| Version claims (`Rust v1.98`, `SQLite v3.53`, `Protobuf v29+`, "80% smaller", "18 MB RAM", "50 ms start") | Not verified; some are marketing numbers | Pin versions in `rust-toolchain.toml`/`Cargo.lock`; benchmarks go in `core/benches/` and are published only once measured |
| `ReferralRequest` as an FHIR R5 resource | Removed in R4; use `ServiceRequest` | §9 |
| Service code `MH-` used for both Maternal Health and Mental Health; `DR-REFERRAL` used twice | Colliding identifiers | §7.5 |
| Invented administrative codes `BD.2.1.4.3` | Not the OCHA COD-AB P-codes the data source actually uses | Use the P-codes from the dataset you cite |

---

## 2. The "no custom domain" model

You own exactly one namespace: **`github.com/zarishhealth`**. GitHub gives you, for free, several more URL spaces under it. Everything in this blueprint is built on those.

### 2.1 Origins

| Purpose | Origin / URL pattern | Notes |
| --- | --- | --- |
| Code, issues, releases | `https://github.com/zarishhealth/<repo>` | Canonical source of truth |
| **Org website + site-wide static files** | `https://zarishhealth.github.io/` | Served from the repo named exactly `zarishhealth.github.io`. **This is the only origin where `/.well-known/` works on Pages** |
| **Project sites** | `https://zarishhealth.github.io/<repo>/` | One Pages site per repo. The repo name becomes the first path segment, so **repo names are URL names** |
| Container images | `ghcr.io/zarishhealth/<image>` | Lowercase only |
| npm packages (if any) | `@zarishhealth/<package>` | Scope = org name |
| Rust crates | `zarish-<name>` on crates.io | crates.io has no org namespaces, so a prefix is the only protection |
| MCP Registry names | `io.github.zarishhealth/<server>` | Reverse-DNS namespace verified through GitHub login (this is the form the official registry documents for GitHub-based auth) |
| Central API (optional) | `https://{API_ORIGIN}` | Hostname assigned by whatever host you choose; **configuration, not code** |
| Site/field API | `http://localhost:8080` or `http://zarish.local:8080` (mDNS) | Same path layout as the central API |

Rules that follow:

1. **GitHub Pages is static.** The Rust server cannot run there. Pages hosts documentation, the FHIR Implementation Guide, published API contracts and brand assets only.
2. **Anything that must be served by a running server** (`/fhir`, `/api/v1`, `/mcp`, OAuth metadata) lives on the Rust server's own origin, and the server serves its own `/.well-known/*` documents. OAuth metadata in particular must be served from the origin it describes, so it cannot be hosted on `github.io` for a different origin.
3. **Pages cannot set custom response headers.** Anything that needs a specific `Content-Type` that Pages would not infer (extensionless files, `application/linkset+json`) must come from the Rust server instead.
4. **`raw.githubusercontent.com` is for Git, not for web assets.** It serves SVG as plain text, so SVGs referenced from other sites can fail to render (verify in browser devtools: the current `index.html` references raw SVG logos). Publish brand assets from Pages (§17).
5. **Local HTTPS caveat.** MCP and OAuth expect HTTPS except for loopback. LAN sites at `http://zarish.local` are fine for FHIR/native API but must not be exposed as OAuth/MCP resources to external clients; use loopback or a TLS-terminating proxy.
6. If you later buy a domain, only `{API_ORIGIN}` and the canonical-URL base change (§7.1); no repo, path or API renames are required. That is the purpose of rule D4.

---

## 3. Standards baseline (verified 2026-10-14)

| Area | Standard | Status / note |
| --- | --- | --- |
| URI syntax | **RFC 3986** | Stable. Lowercase scheme and host; percent-encode per spec; **no personal data in URIs** (they end up in logs and caches) |
| HTTP semantics | **RFC 9110** | Stable. Methods, status codes, caching, `Retry-After` |
| Well-known URIs | **RFC 8615** (supersedes RFC 5785) | Path prefix is `/.well-known/` (leading dot). Only names in the **IANA Well-Known URI registry** should be used; do not invent names |
| Registered, used here | `security.txt` (RFC 9116); `oauth-protected-resource` (RFC 9728); `oauth-authorization-server` (RFC 8414); `openid-configuration` (OIDC Discovery); `smart-configuration` (SMART App Launch); `api-catalog` (RFC 9727, June 2025) | All listed in the IANA registry or defined by the cited spec |
| Error format | **RFC 9457** Problem Details (obsoletes RFC 7807) | `type` is a URI that identifies the problem; it may be non-resolvable but ours will resolve (§7.4) |
| Deprecation signalling | `Deprecation` header (**RFC 9745**) + `Sunset` (RFC 8594) | RFC 9745 published by the IETF HTTPAPI group |
| API discovery | **RFC 9727** `api-catalog` | Publisher must answer `GET` and `HEAD` with a `Link` header; Linkset format |
| IDs | **RFC 9562** UUIDs (v7) | v7 is time-ordered; good for offline generation |
| Timestamps | RFC 3339 (UTC, `Z`) | |
| API description | **OpenAPI 3.1** baseline; 3.2 exists and is adopted by some tooling | Pin 3.1 until your Rust generator supports 3.2 |
| Healthcare | **HL7 FHIR R5 (5.0.0)** now; **R6** in normative ballot since January 2026, final publication expected late 2026–2027 | R4 remains the most widely deployed; **SMART App Launch 2.1** is published against R4 but works with any FHIR version from DSTU2 onward. Design so R5→R6 is a configuration and profile change (§9) |
| FHIR discovery | `/metadata` (CapabilityStatement) + `/.well-known/smart-configuration` | Per SMART App Launch, the well-known path is appended to the FHIR base URL even when the base has a path component |
| MCP | **Model Context Protocol 2026-07-28** (current; replaced 2025-11-25) | **Stateless**: no initialize handshake, no `Mcp-Session-Id`; `server/discover` is mandatory; `Mcp-Method`/`Mcp-Name` headers required on Streamable HTTP; list results carry `ttlMs`/`cacheScope`; HTTP+SSE transport deprecated; roots, sampling, logging and Dynamic Client Registration deprecated (removal not before 2027-07-28); tool names 1–128 chars from `A–Z a–z 0–9 _ - .` |
| MCP auth | OAuth 2.0 **Protected Resource Metadata (RFC 9728)** required for discovery; authorization servers provide RFC 8414 and/or OIDC discovery | Clients must reject metadata whose `issuer` does not match the URL it was fetched from |
| MCP server cards | **Not settled.** Proposals SEP-1649 → SEP-2127 use `/.well-known/mcp/server-card.json`, `/.well-known/mcp/server-cards.json` and `/.well-known/mcp.json` in different drafts; none is in the IANA registry | Isolate behind one config value (§10.4); do not depend on it |
| MCP registry | `server.json` under `io.github.<user>/<name>` | Namespace verified through GitHub, DNS or HTTP challenge |
| Rust naming | RFC 430 casing; crate names should **not** use `-rs`/`-rust`; modules/functions `snake_case`; acronyms as words (`HttpClient`) | Rust API Guidelines |
| Versioning | SemVer 2.0.0; Conventional Commits 1.0.0 | |
| Licensing metadata | SPDX identifiers; REUSE layout | §15 |

---

## 4. Naming rules (normative)

Keywords MUST/SHOULD/MAY are used as in RFC 2119.

### 4.1 Repositories

- MUST be lowercase ASCII `a–z`, `0–9`, hyphen. No uppercase, underscores, spaces or dots.
- Exceptions (GitHub-mandated): `.github`, `.github-private`, `zarishhealth.github.io`.
- SHOULD be one to three words, ≤ 30 characters, a **noun** describing what it is (`core`, `app`, `docs`).
- MUST NOT repeat the org name (`zarishhealth-docs` → `docs`), the language (`-rust`) or the word `repo`.
- Because Pages publishes at `/<repo>/`, a repo name is also a URL segment: treat it as permanent. GitHub redirects renamed repos on `github.com`, but **Pages URLs and canonical URLs do not redirect**.
- Site-distribution repos: `distro-<iso-country>-<place>[-<nn>]`, e.g. `distro-bd-coxs-bazar-01` (private; contains no PHI or secrets).
- Topics: lowercase kebab-case, ≤ 50 characters. Mandatory topics: `zarishhealth` plus one of `rust`, `fhir`, `mcp`, `docs`, `infrastructure`, `content`.
- Classification uses **GitHub custom properties** (`layer`, `data-class`, `release-cadence`), not name prefixes.

### 4.2 Branches, tags, releases, commits

| Item | Rule | Example |
| --- | --- | --- |
| Default branch | `main` (never renamed: raw/Pages URLs depend on it) | |
| Work branches | `feat/<issue>-<slug>`, `fix/…`, `docs/…`, `chore/…`, `refactor/…`, `test/…` | `feat/142-sync-conflict-queue` |
| Release branches | `release/<major>.<minor>` (only when a patch line is maintained) | `release/1.2` |
| Tags | `v<semver>`; in a workspace, per-crate tags `<crate>-v<semver>` | `v1.4.0`, `zarish-sync-v0.3.1` |
| Pre-release | SemVer pre-release | `v1.0.0-rc.1` |
| Commit subjects | Conventional Commits | `feat(sync): queue conflicting edits for review` |
| Issue/PR labels | `type:*`, `area:*`, `priority:p0…p3`, `status:*` plus GitHub defaults `good first issue`, `help wanted` | `area:sync` |

### 4.3 Directories

- MUST be lowercase kebab-case: `clinical-forms/`, `api-contracts/`.
- Mandated exceptions: Rust (`src/`, `tests/`, `benches/`, `examples/`, `migrations/`, `src-tauri/`), `.github/`, `.well-known/`, `node_modules/`, FHIR IG Publisher (`input/`, `input/resources/`, `input/pagecontent/`), `LICENSES/` (REUSE).
- Depth SHOULD not exceed 5 levels below a repo root.
- URL-visible directories (anything published to Pages) MUST contain only `[a-z0-9-]` and MUST NOT be renamed after publication.

### 4.4 Files

| Kind | Rule | Example |
| --- | --- | --- |
| Rust source | `snake_case.rs` | `conflict_queue.rs` |
| Docs, config, data, scripts | `kebab-case.<ext>` | `patient-registration-standards.md` |
| Root/community files | Conventional upper-case names | `README.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`, `AGENTS.md`, `CODEOWNERS` |
| Translations | `<name>.<bcp47>.md` | `CODE_OF_CONDUCT.bn.md` (replaces `CODE_OF_CONDUCT_bn.md`) |
| ADRs | `adr/NNNN-<kebab-title>.md` (4-digit, never reused) | `adr/0007-use-uuidv7.md` |
| RFC documents | `text/NNNN-<kebab-title>.md` | |
| Workflows | `<verb-or-purpose>.yml` | `ci.yml`, `release.yml`, `security.yml`, `pages.yml`, `reusable-rust-ci.yml` |
| SQL migrations | `<UTC-timestamp>_<snake_description>.sql` (SQLx convention) | `20261014093000_create_sync_log.sql` |
| Protobuf | `snake_case.proto` under `proto/<package-path>/<version>/` | `proto/zarishhealth/sync/v1/sync.proto` |
| JSON/YAML keys | JSON: `camelCase` (aligns with FHIR). YAML config: `snake_case` | |
| Brand assets | Keep the existing pattern `zarishhealth-<type>-<target>[-<variant>][-<WxH>].<ext>` — **frozen**, because hot-links depend on it | |
| No spaces, no uppercase (except above), no version numbers in filenames of published URLs (use paths like `/v1/`) | | |

### 4.5 URL path segments (all HTTP surfaces)

1. Lowercase kebab-case, plural nouns for collections, no verbs, no file extensions, **no trailing slash** on API paths (static Pages directories keep it).
2. Hierarchy only for true containment, max two levels: `/api/v1/sites/{siteId}/devices`.
3. Path parameters are `camelCase` in templates (`{patientId}`), values are opaque IDs (§7.2).
4. Query parameters are `snake_case` (`page_size`, `page_token`, `updated_since`), **except** FHIR, which keeps its own names (`_count`, `birthdate`).
5. No personal data (names, DOB, national ID, phone) in any path or query string. Search by identifier uses `POST` with a body or FHIR `POST [base]/Patient/_search`.
6. Axum 0.8 route syntax is `/{param}` (not `/:param`).

### 4.6 Rust

| Item | Rule | Example |
| --- | --- | --- |
| Package (crate) name | `zarish-<domain>[-<role>]`, kebab-case, **no** `-rust`/`-rs` | `zarish-fhir-model`, `zarish-sync` |
| Library path | snake_case of the package | `zarish_fhir_model` |
| Binaries | Short: `zarish` (CLI), `zarish-server` | |
| Types/traits | `UpperCamelCase`, acronyms as words | `FhirPatient`, `HttpClient` |
| Functions/modules/vars | `snake_case`; getters without `get_` | |
| Features | No placeholder words; name the thing | `sqlite`, `postgres`, `wasm` |
| Edition / toolchain | 2024 edition; exact toolchain pinned in `rust-toolchain.toml`; MSRV declared in `Cargo.toml` (`rust-version`) | |

### 4.7 Packages and images

| Artifact | Name |
| --- | --- |
| Container image | `ghcr.io/zarishhealth/<component>:<semver>` and `:<semver>-<gitsha7>`; never rely on `latest` |
| Release assets | `zarish-<component>-<semver>-<os>-<arch>.<ext>` e.g. `zarish-app-1.4.0-windows-x86_64.msi` |
| Checksums/signatures | `SHA256SUMS`, `SHA256SUMS.sig` (or sigstore bundle) |
| SBOM | `zarish-<component>-<semver>.cdx.json` (CycloneDX) |

### 4.8 Identifiers inside data

| Thing | Rule |
| --- | --- |
| Resource ID | UUIDv7, lowercase, hyphenated (RFC 9562 text form) |
| Business codes (service codes etc.) | Upper-case, hyphenated, unique per code system (§7.5). Lowercased only when used as a URL segment |
| Site ID | `site-<iso3166-2-country>-<kebab-place>-<nn>`, e.g. `site-bd-coxs-bazar-01` (matches the distro repo suffix) |
| Device ID | UUIDv7 generated at first launch |
| Language tags | BCP 47: `en`, `bn`, `my` |
| Time zone | IANA `Asia/Dhaka`, stored timestamps in UTC |

### 4.9 Allowed exceptions (complete list)

Rust source `snake_case` · Rust directories above · FHIR resource names (`Patient`) and IG Publisher file names (`StructureDefinition-zarish-patient.json`) · conventional root files · GitHub-mandated names · SQLx/Protobuf layouts. Nothing else.

---

## 5. Organization map and repository catalog

### 5.1 Phase 1 (create or normalise now)

| Repository | URL | Pages URL | Contents | Visibility |
| --- | --- | --- | --- | --- |
| `.github` | `github.com/zarishhealth/.github` | — | Org profile, community-health defaults, reusable workflows, brand kit | Public |
| `zarishhealth.github.io` | `…/zarishhealth.github.io` | `https://zarishhealth.github.io/` | Org website; static `/.well-known/security.txt`; mirrored brand assets | Public |
| `docs` | `…/docs` | `/docs/` | Handbook, architecture, ADRs, problem-type pages, deployment guides | Public |
| `core` | `…/core` | `/core/` (rustdoc) | Rust Cargo workspace: models, storage, sync, auth, server, CLI | Public |
| `app` | `…/app` | — | Tauri v2 shells + web UI (WASM) for desktop, mobile, browser | Public |
| `api` | `…/api` | `/api/` | **Contracts only**: OpenAPI, Protobuf, JSON Schemas, MCP tool schemas | Public |
| `fhir` | `…/fhir` | `/fhir/` | FHIR Implementation Guide: profiles, value sets, code systems, NamingSystems (canonical base) | Public |
| `mcp` | `…/mcp` | `/mcp/` | MCP servers (Rust), `server.json` manifests | Public |
| `content` | `…/content` | — | Clinical forms, terminology subsets, translations | Public (synthetic only) |
| `deploy` | `…/deploy` | — | Containers, IaC, field images, backup scripts | Public (no secrets) |
| `distro-template` | `…/distro-template` | — | GitHub **template** repo for site distributions | Public |
| `rfcs` | `…/rfcs` | `/rfcs/` | Proposals and governance | Public |
| `builder` | `…/builder` | — | Existing workspace repo, renamed from `ZarishHealth-builder` (§17); architecture, tests, release evidence | Public |
| `.github-private` | | | Member-only profile and internal notes | Private (optional) |

> `/fhir/`, `/api/`, `/docs/` and `/mcp/` as Pages paths are **static documentation and contracts**. They are different things from the live `/fhir`, `/api/v1` and `/mcp` endpoints on `{API_ORIGIN}`. The static site is where the contract is read; the server is where it is called.

### 5.2 Phase 2 (only when justified, with the trigger)

| Candidate repo | Split out of | Trigger |
| --- | --- | --- |
| `terminology` | `fhir` / `content` | Needs licensed (SNOMED CT/LOINC) data handling or its own release cadence |
| `sdk` | `api` | A second language SDK is needed |
| `design-system` | `app` | A second UI consumes it |
| `distro-<country>-<place>-<nn>` | `distro-template` | One per real site (private) |
| `security` | `.github` | Advisories/pen-test reports need restricted access |
| Any crate in `core` | `core` | Separate owner or independent versioning |

### 5.3 Teams (GitHub)

`maintainers`, `core-rust`, `app`, `fhir-clinical`, `docs-content`, `security`, `release`. Team slugs are kebab-case; `CODEOWNERS` references `@zarishhealth/<team>`.

---

## 6. Per-repository layouts

### 6.1 `.github`

```text
.github/                              ← the repository
├── .github/
│   ├── workflows/
│   │   ├── reusable-rust-ci.yml      ← called as zarishhealth/.github/.github/workflows/reusable-rust-ci.yml@v1
│   │   ├── reusable-docs-pages.yml
│   │   ├── sync-brand-to-pages.yml   ← copies profile/assets/ → zarishhealth.github.io (§17)
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
│   ├── README.md                     ← renders at github.com/zarishhealth
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

Notes: the org profile renders only from `profile/README.md` in a **public** repo named exactly `.github`. Reusable workflows in a public `.github` repo can be called by every org repo. Pin third-party Actions to full commit SHAs.

### 6.2 `zarishhealth.github.io`

```text
zarishhealth.github.io/
├── .nojekyll                         ← REQUIRED so .well-known is published
├── .well-known/
│   └── security.txt                  ← RFC 9116 (see §11.2)
├── index.html
├── style.css
├── assets/
│   └── brand/                        ← mirrored from .github/profile/assets (logo, favicon, social)
├── robots.txt
├── sitemap.xml
├── 404.html
├── README.md
└── LICENSE
```

Published at `https://zarishhealth.github.io/`. Favicon, OG and logo URLs use `/assets/brand/…`, not `raw.githubusercontent.com`.

### 6.3 `core` (Cargo workspace)

```text
core/
├── Cargo.toml                        ← [workspace]
├── Cargo.lock
├── rust-toolchain.toml
├── deny.toml                         ← cargo-deny: licenses, advisories, bans
├── crates/
│   ├── zarish-fhir-model/            ← FHIR R5 types (serde)
│   ├── zarish-fhir-search/
│   ├── zarish-fhir-validate/
│   ├── zarish-hl7/                   ← HL7 v2 → FHIR mapping
│   ├── zarish-terminology/
│   ├── zarish-store/                 ← storage ports: SQLite + PostgreSQL (SQLx)
│   ├── zarish-sync/                  ← change log, LAN peer sync, conflict queue
│   ├── zarish-proto/                 ← generated prost code from api/proto
│   ├── zarish-crypto/                ← at-rest encryption, key handling
│   ├── zarish-auth/                  ← embedded OAuth/OIDC issuer, token validation
│   ├── zarish-audit/
│   ├── zarish-problem/               ← RFC 9457 types and mapping
│   ├── zarish-server/                ← [bin] Axum app (fhir, api, mcp host, well-known)
│   └── zarish-cli/                   ← [bin] `zarish`
├── migrations/
│   ├── sqlite/
│   └── postgres/
├── benches/
├── tests/
├── docs/                             ← crate-level notes; user docs live in the `docs` repo
├── .github/workflows/{ci,security,release}.yml
├── CHANGELOG.md  CODEOWNERS  README.md  LICENSE
```

`zarish-server` module layout (`src/`): `main.rs`, `config.rs`, `routes/{mod,fhir,api_v1,well_known,health,mcp}.rs`, `middleware/{auth,problem,request_id,cors}.rs`, `state.rs`. Routes are registered by the path tables in §8–§11, so the code layout mirrors the URL layout.

### 6.4 `api` (contracts only, source of truth)

```text
api/
├── openapi/
│   └── v1/
│       ├── zarish-api.yaml           ← OpenAPI 3.1 for /api/v1
│       └── components/               ← shared schemas, problem types, parameters
├── proto/
│   └── zarishhealth/
│       └── sync/v1/sync.proto        ← package zarishhealth.sync.v1
├── json-schema/
│   ├── clinical-form.schema.json
│   └── site-config.schema.json
├── mcp/
│   └── tools/                        ← JSON Schema for each tool input/output
├── problems/                         ← one .md per problem type (§7.4)
├── buf.yaml  buf.gen.yaml            ← Protobuf lint + breaking-change checks
├── .github/workflows/{lint,pages}.yml
└── README.md  CHANGELOG.md  LICENSE
```

Published at `https://zarishhealth.github.io/api/` (e.g. `/api/openapi/v1/zarish-api.yaml`). CI fails on breaking changes to anything under `v1/` (Buf breaking check; an OpenAPI diff tool).

### 6.5 `fhir` (Implementation Guide)

```text
fhir/
├── sushi-config.yaml                 ← canonical: https://zarishhealth.github.io/fhir
├── input/
│   ├── fsh/                          ← FHIR Shorthand sources (*.fsh)
│   ├── pagecontent/
│   ├── resources/                    ← IG Publisher naming: StructureDefinition-zarish-patient.json
│   └── images/
├── ig.ini
├── .github/workflows/ig-publish.yml  ← builds IG → GitHub Pages
└── README.md  LICENSE
```

Canonical URL base: `https://zarishhealth.github.io/fhir` (§7.1). Package id: `zarishhealth.fhir`.

### 6.6 `mcp`

```text
mcp/
├── Cargo.toml                        ← workspace
├── crates/
│   ├── zarish-mcp-core/              ← shared Streamable HTTP + stdio plumbing (2026-07-28)
│   ├── zarish-mcp-fhir/              ← read-only FHIR access
│   ├── zarish-mcp-terminology/       ← code lookup (no patient data)
│   └── zarish-mcp-docs/              ← documentation search (no patient data)
├── servers/
│   ├── fhir.server.json              ← name: io.github.zarishhealth/fhir
│   ├── terminology.server.json
│   └── docs.server.json
└── README.md  LICENSE
```

### 6.7 `app`

```text
app/
├── src-tauri/                        ← Tauri v2 (Rust)
│   ├── Cargo.toml  tauri.conf.json  capabilities/
│   └── src/
├── ui/                               ← web UI (also built to WASM/PWA)
│   ├── src/  public/  package.json
├── i18n/{en,bn,my}.json              ← BCP 47 file names
└── .github/workflows/{ci,release}.yml
```

### 6.8 `content`, `deploy`, `distro-template`, `docs`, `rfcs`

```text
content/                              deploy/                           distro-template/
├── forms/                            ├── containers/                   ├── site.example.toml     ← NO secrets
│   └── <service-code>/<form>.json    │   └── <component>/Dockerfile    ├── clinical-forms/
├── value-sets/                       ├── images/field-pi/              ├── .github/workflows/
├── translations/{en,bn,my}/          ├── infra/                        │   ├── build.yml
└── README.md                         │   └── opentofu/                 │   └── release.yml
                                      ├── backup/                       └── README.md
                                      └── README.md

docs/                                 rfcs/
├── index.md                          ├── text/NNNN-<title>.md
├── architecture/                     ├── 0000-template.md
├── adr/NNNN-<title>.md               └── README.md
├── guides/
├── problems/<slug>.md                ← resolvable problem-type pages (§7.4)
└── reference/
```

---

## 7. URI and identifier design

### 7.1 Canonical bases

| Thing | Canonical base | Stability |
| --- | --- | --- |
| FHIR IG / profiles | `https://zarishhealth.github.io/fhir` | Permanent |
| Problem types | `https://zarishhealth.github.io/docs/problems/<slug>` | Permanent |
| API contracts | `https://zarishhealth.github.io/api/openapi/v1/zarish-api.yaml` | Permanent per major |
| JSON Schemas (`$id`) | `https://zarishhealth.github.io/api/json-schema/<name>.schema.json` | Permanent |
| MCP registry names | `io.github.zarishhealth/<name>` | Permanent |
| Protobuf packages | `zarishhealth.<domain>.<vN>` | Permanent per major |
| Runtime API | `{API_ORIGIN}` | Replaceable |

**Rule: identifiers that get embedded in data (canonical URLs, NamingSystem URIs, JSON Schema `$id`) MUST use the permanent bases above, never `{API_ORIGIN}`.** If you later own a domain, add it as an alias but keep these identifiers valid forever.

### 7.2 Resource identifiers

- Format: UUIDv7 text (`0192f4a8-7b3c-7d1e-9a2b-3c4d5e6f7a8b`), lowercase.
- Generated on the client at creation (offline-safe).
- **Never** derived from DOB, national ID, name, phone or camp/shelter data.
- Human-friendly IDs (printed cards, QR) are separate **business identifiers** (`Patient.identifier`) that carry a check character, are not used as URL path IDs, and are looked up by `POST`.

### 7.3 Identifier systems (FHIR NamingSystems)

| Identifier | `system` URI |
| --- | --- |
| Individual patient ID | `https://zarishhealth.github.io/fhir/NamingSystem/individual-id` |
| Service enrollment ID | `https://zarishhealth.github.io/fhir/NamingSystem/service-enrollment-id` |
| Visit ID | `https://zarishhealth.github.io/fhir/NamingSystem/visit-id` |
| Site ID | `https://zarishhealth.github.io/fhir/NamingSystem/site-id` |
| External IDs (UNHCR ProGress ID, Bangladesh NID, birth registration) | **Use the issuing authority's published system URI/OID**; leave TBD until confirmed with the authority |

### 7.4 Problem types (RFC 9457)

`type` = `https://zarishhealth.github.io/docs/problems/<slug>`; each slug is a page in `docs/problems/` (kebab-case, permanent).

| Slug | HTTP status | Meaning |
| --- | --- | --- |
| `validation-failed` | 422 | Body failed schema or business validation |
| `malformed-request` | 400 | Syntax error |
| `unauthenticated` | 401 | Missing/invalid token |
| `forbidden` | 403 | Token lacks scope/role |
| `not-found` | 404 | Resource absent (also used for resources the caller may not know exist) |
| `version-conflict` | 409 / 412 | `ETag` / `If-Match` mismatch |
| `sync-conflict` | 409 | Concurrent edits queued for review |
| `rate-limited` | 429 | Includes `Retry-After` |
| `unsupported-protocol-version` | 400 | e.g. unsupported MCP or API version |
| `internal-error` | 500 | Never includes internals; includes `instance` correlation ID |

Response example (`Content-Type: application/problem+json`):

```json
{
  "type": "https://zarishhealth.github.io/docs/problems/validation-failed",
  "title": "Validation failed",
  "status": 422,
  "detail": "One or more fields are invalid.",
  "instance": "urn:uuid:0192f4a8-7b3c-7d1e-9a2b-3c4d5e6f7a8b",
  "errors": [{ "pointer": "/birthDate", "code": "invalid-date" }]
}
```

`detail` and `errors` MUST NOT echo personal data.

### 7.5 Service codes (fixing collisions)

Keep the existing service classification, but make each code unique and put them in one CodeSystem: `https://zarishhealth.github.io/fhir/CodeSystem/service`. Changes needed:

| Currently | Problem | Use |
| --- | --- | --- |
| `MH-MATERNAL` and `MH-BASIC` | `MH` means maternal health and mental health | `MCH-MATERNAL`; `MHPSS-BASIC` (matches the existing MHPSS service code in the ID scheme) |
| `DR-REFERRAL` in B-02 and in E | Same code, two groups | One code `DR-UNIT`; group membership is data, not part of the code |
| Codes in URLs | Case | `…/services/mchmaternal` is wrong; use `…/services/mch-maternal` (lowercased code) |

---

## 8. Native HTTP API (`/api/v1`)

### 8.1 Conventions

| Topic | Rule |
| --- | --- |
| Base path | `/api/v1`. Major version in the path. Header-based version selection is **not** used |
| Media types | `application/json` (and `application/problem+json` for errors). Protobuf sync bodies: `application/x-protobuf` with `Content-Type` parameter `proto=zarishhealth.sync.v1.Envelope` |
| Methods | `GET` read · `POST` create / non-idempotent action resource · `PUT` replace · `PATCH` JSON Merge Patch (`application/merge-patch+json`) · `DELETE` · `HEAD`/`OPTIONS` |
| Status codes | 200, 201 (+`Location`), 202 (async), 204, 304, 400, 401, 403, 404, 409, 412, 415, 422, 429, 5xx |
| Concurrency | `ETag` on single resources; `If-Match` required on `PUT`/`PATCH`/`DELETE` |
| Idempotency | `POST` accepts `Idempotency-Key` (IETF HTTPAPI draft; treat as a convention until it is an RFC). Mandatory for sync uploads |
| Pagination | Cursor: `page_size` (default 50, max 200), `page_token`; response `nextPageToken`; `Link: <…>; rel="next"` (RFC 8288) |
| Filtering/sorting | `field_name=value`, `updated_since=<RFC3339>`, `order_by=updated_at` / `-updated_at` |
| Field naming | JSON `camelCase`; booleans `isX`/`hasX`; timestamps `…At`, RFC 3339 UTC |
| Request correlation | Accept/emit `X-Request-Id`; propagate W3C `traceparent` |
| Caching | `ETag` + `Cache-Control`; list endpoints for reference data use `max-age` |
| CORS | Allow-list of origins from config; never `*` on authenticated endpoints |
| Deprecation | `Deprecation` (RFC 9745) + `Sunset` (RFC 8594) + `Link: <…>; rel="deprecation"`; support the previous major for ≥ 12 months |
| Security headers | `Strict-Transport-Security` when HTTPS, `X-Content-Type-Options: nosniff`, `Cache-Control: no-store` on anything with personal data |

### 8.2 Endpoint catalog

Clinical resources are **not** here; they are under `/fhir` (§9).

| Method & path | Purpose | Scope |
| --- | --- | --- |
| `GET /api/v1/sites` · `GET /api/v1/sites/{siteId}` | Site registry | `site.read` |
| `GET /api/v1/sites/{siteId}/devices` · `POST …/devices` | Enrolled devices | `device.read` / `device.write` |
| `GET /api/v1/devices/{deviceId}` · `DELETE …` | Device record / revoke | `device.*` |
| `POST /api/v1/sync-sessions` | Open a sync session (returns `syncSessionId`) | `sync.write` |
| `POST /api/v1/sync-sessions/{syncSessionId}/changes` | Upload a change batch (Protobuf, idempotent) | `sync.write` |
| `GET /api/v1/sync-sessions/{syncSessionId}/changes?page_token=` | Download changes since cursor | `sync.read` |
| `POST /api/v1/sync-sessions/{syncSessionId}/completion` | Close the session | `sync.write` |
| `GET /api/v1/sync-conflicts` · `GET …/{conflictId}` · `PATCH …/{conflictId}` | Review queue; `PATCH` resolves | `sync.review` |
| `GET /api/v1/users` · `…/{userId}` | Local users and roles | `user.*` |
| `GET /api/v1/audit-events` | Read-only audit log query | `audit.read` |
| `GET /api/v1/reports` · `POST /api/v1/report-runs` · `GET /api/v1/report-runs/{runId}` | Reports (202 + polling) | `report.*` |
| `GET /api/v1/configuration` | Effective non-secret configuration | `config.read` |
| `GET /api/v1/openapi.json` | Served contract (same content as published YAML) | public |

Action-like operations are modelled as creatable resources (`sync-sessions`, `report-runs`, `…/completion`), not verb paths.

### 8.3 Operational endpoints (no version prefix)

| Path | Purpose | Auth |
| --- | --- | --- |
| `GET /livez` | Process is up | none (loopback/LAN only) |
| `GET /readyz` | Dependencies ready (DB, migrations) | none (loopback/LAN only) |
| `GET /metrics` | Prometheus text format | restricted |
| `GET /.well-known/api-catalog` | RFC 9727 catalog (§11) | public |

---

## 9. FHIR endpoint (`/fhir`)

| Topic | Rule |
| --- | --- |
| Base URL | `{API_ORIGIN}/fhir` |
| Version | R5 (`5.0.0`) at launch. Select with MIME parameter `Accept: application/fhir+json; fhirVersion=5.0`. A future R6 deployment is announced through `GET /fhir/metadata` (`fhirVersion`) and, if run in parallel, a separate base (`/fhir-r6`) — decided by RFC at that time |
| Formats | `application/fhir+json` (primary); `application/fhir+xml` optional |
| Paths | Standard FHIR REST: `GET /fhir/Patient/{id}`, `POST /fhir/Patient`, `GET /fhir/Observation?patient=…&_count=…`, `POST /fhir/` (transaction/batch Bundle), `POST /fhir/Patient/_search`. Resource types are `PascalCase` by FHIR rule — the allowed exception |
| Discovery | `GET /fhir/metadata` (CapabilityStatement); `GET /fhir/.well-known/smart-configuration` (path appended to the FHIR base, as SMART requires) |
| Errors | `OperationOutcome` with matching HTTP status |
| Subscriptions | R5 topic-based Subscriptions only when required; sync does **not** depend on them |
| HL7 v2 ingest | `POST /fhir/$hl7v2-ingest` is **not** used. Legacy ingest is a separate native resource: `POST /api/v1/hl7-messages` (202), keeping FHIR paths standard |
| Referral | Use `ServiceRequest` (there is no `ReferralRequest` in R4/R5) |
| Profiles | Declared in `fhir` IG; canonical `https://zarishhealth.github.io/fhir/StructureDefinition/zarish-<name>` |
| Terminology systems | Standard URIs (`http://snomed.info/sct`, `http://loinc.org`, `http://hl7.org/fhir/sid/icd-11`) — confirm each system's current registered URI in the HL7 terminology registry before use; SNOMED CT/LOINC/ICD-11 licensing must be checked per country |

R6 readiness: keep profiles in FSH, avoid R5-only elements without a mapping note, and test against the R6 ballot build in CI as a non-blocking job.

---

## 10. MCP (Model Context Protocol 2026-07-28)

### 10.1 Naming

| Item | Rule | Example |
| --- | --- | --- |
| Registry name | `io.github.zarishhealth/<kebab>` | `io.github.zarishhealth/fhir` |
| Crate | `zarish-mcp-<domain>` | `zarish-mcp-terminology` |
| Endpoint path | One path per server, `POST /mcp` for the main server; additional servers `POST /mcp/<domain>` | `/mcp/terminology` |
| Tool names | `^[a-z][a-z0-9_]{0,63}$` in practice (spec allows 1–128 of `A-Za-z0-9_-.`); `snake_case`, domain-first: `<domain>_<verb>_<noun>` | `fhir_search_resources`, `terminology_lookup_code` |
| Resource URIs | `zarish://<domain>/<path>` for non-HTTP resources; real `https://` URLs where a resource has one | `zarish://terminology/icd11/1A00` |
| Prompts | `snake_case` | `summarize_encounter_template` |
| Tool inputs | `camelCase`, JSON Schema in `api/mcp/tools/<tool-name>.schema.json` | |

### 10.2 Transport and protocol requirements

- Streamable HTTP, single endpoint, `POST` only. **No** HTTP+SSE, **no** `Mcp-Session-Id`, **no** initialize handshake.
- Required request headers: `MCP-Protocol-Version: 2026-07-28`, `Mcp-Method`, and `Mcp-Name` for `tools/call`, `resources/read`, `prompts/get`. Header value and body value must agree; mismatches are rejected.
- Implement `server/discover` (mandatory).
- All list/read results include `ttlMs` and `cacheScope`. Use `cacheScope: private` for anything user-specific.
- Tool parameters mirrored to headers use `x-mcp-header` → `Mcp-Param-{Name}`; use sparingly (for routing, e.g. `siteId`).
- Input validation failures are tool-execution errors (so the model can retry), not protocol errors.
- Do not build on deprecated features (roots, sampling, logging, DCR). Use `stderr`/OpenTelemetry for logging, and client-ID metadata documents instead of DCR.
- Local desktop use: **stdio** transport; remote/shared: Streamable HTTP.

### 10.3 Authorization

- The MCP server is an OAuth **resource server** and publishes RFC 9728 metadata (§11.1).
- Authorization servers publish RFC 8414 and/or OIDC discovery; clients try the path-insertion and path-appending forms.
- Tokens are audience-bound to the MCP resource URL (resource indicators).
- Tool scopes mirror API scopes (§12). Write tools are off by default.

### 10.4 Server card (unsettled)

Serve the card from **one** configurable path, default `/.well-known/mcp/server-card.json`, and treat the location as provisional (the proposals disagree: `server-card.json`, `server-cards.json`, `mcp.json`). Never reference it from other documents. Registry publication (`server.json`) is the stable discovery route.

### 10.5 Safety rules (health data)

1. Default MCP servers are **read-only** and expose **terminology, documentation and de-identified aggregates** first.
2. `zarish-mcp-fhir` returns patient data only to authenticated callers with the same scopes as the REST API, never to anonymous sessions, and writes an audit event per call.
3. Tool descriptions and annotations are untrusted metadata for clients; never rely on them for security. Enforce authorization on the server.
4. Never place personal data in tool names, resource URIs, or `Mcp-Name`/`Mcp-Param-*` headers (headers are logged by gateways).

---

## 11. Well-known documents: what is served where

### 11.1 Rust server (`{API_ORIGIN}`)

| Path | Standard | Content type | Notes |
| --- | --- | --- | --- |
| `/.well-known/oauth-protected-resource` and path-suffixed forms, e.g. `/.well-known/oauth-protected-resource/mcp`, `/…/fhir`, `/…/api/v1` | RFC 9728 | `application/json` | `resource` MUST equal the resource identifier exactly; list `authorization_servers`, `scopes_supported`, `bearer_methods_supported: ["header"]`. Omit parameters that are unset |
| `/.well-known/oauth-authorization-server` | RFC 8414 | `application/json` | When the embedded issuer is used. `issuer` MUST equal the origin it is fetched from |
| `/.well-known/openid-configuration` | OIDC Discovery | `application/json` | Same issuer |
| `/fhir/.well-known/smart-configuration` | SMART App Launch | `application/json` (always JSON, regardless of `Accept`) | Capabilities, endpoints |
| `/.well-known/api-catalog` | RFC 9727 | `application/linkset+json` | Must answer `GET` and `HEAD` (with `Link` header). Lists `/api/v1` (OpenAPI), `/fhir`, `/mcp` and links to the static docs |
| `/.well-known/security.txt` | RFC 9116 | `text/plain` | Same content as the Pages copy |
| `/.well-known/mcp/server-card.json` | Provisional (§10.4) | `application/json` | Optional |

### 11.2 `https://zarishhealth.github.io` (static)

| Path | Content |
| --- | --- |
| `/.well-known/security.txt` | RFC 9116. `Contact:` must be a `mailto:` or `https:` URI; `Expires:` is required and must be refreshed at least yearly (a scheduled workflow opens an issue 60 days before expiry) |
| `/.well-known/…` other | **Nothing else.** Pages cannot set content types for extensionless files or custom headers, and OAuth/MCP metadata must be served from the resource's own origin |

`security.txt` template:

```text
Contact: https://github.com/zarishhealth/.github/security/advisories/new
Expires: 2027-10-14T00:00:00.000Z
Preferred-Languages: en, bn
Canonical: https://zarishhealth.github.io/.well-known/security.txt
Policy: https://github.com/zarishhealth/.github/blob/main/SECURITY.md
```

If a mailbox you control exists, add `Contact: mailto:…` as well. Do not use a mailbox on a domain you do not own.

### 11.3 Do not publish

`/.well-known/` names that are not in the IANA registry or defined by the specification you rely on (for example guessed `ai-plugin.json`, `agent.json`) unless you accept that they are unregistered.

---

## 12. Authentication and authorization

| Topic | Rule |
| --- | --- |
| Protocols | OAuth 2.0 with PKCE (RFC 7636) for user flows; client credentials for service-to-service; OIDC for identity. MCP profiles OAuth 2.1 (an IETF draft — verify its status when you implement) |
| Issuer | Sites: embedded issuer in `zarish-auth` (works offline; keys per site). HQ: any OIDC provider (Keycloak acceptable). Both expose the discovery documents in §11.1 |
| Token format | Short-lived JWT access tokens (≤ 15 min), `aud` = resource URL, `iss` = issuer origin, `scope` space-delimited |
| Offline | Site-local refresh tokens bound to the device key; device revocation list synced when possible |
| Scopes | `<resource>.<action>`: `site.read`, `device.write`, `sync.write`, `sync.review`, `audit.read`, `report.read`; FHIR uses SMART v2 scopes (`patient/Observation.rs`, `user/Patient.cruds`) |
| Roles → scopes | `admin`, `clinician`, `nurse`, `pharmacist`, `lab-technician`, `data-clerk`, `chw`, `auditor` (kebab-case role IDs); mapping lives in `content`, enforced in `zarish-auth` |
| Secrets | Never in Git; installed per site; rotated; test fixtures use obviously fake values |

---

## 13. Data and sync (carried over, tightened)

- **Local store**: embedded SQLite per device, encrypted at rest (SQLCipher or equivalent) with a device-bound key.
- **Central store** (optional): PostgreSQL. Not a free-tier shared service for real patient data (§14).
- **Change log**: append-only, per resource version (`meta.versionId`), UUIDv7 change IDs, HLC/vector clock per device. Clinical history is never overwritten; edits append versions.
- **Transport**: Protobuf envelopes (`zarishhealth.sync.v1`), compressed, over TLS; LAN peer sync discovers peers via mDNS and requires mutual authentication with per-device keys. A shared passphrase is not authentication.
- **Conflict rule** (resolves the drafts' disagreement): non-overlapping field edits merge automatically; overlapping edits to clinical fields are **never** decided by "newest timestamp wins" — they enter the review queue (`/api/v1/sync-conflicts`). Non-clinical fields may use last-writer-wins with an audit record.
- **Backups**: encrypted client-side before leaving the device; the cloud target is a deployment choice, decided after §14.

---

## 14. Security, privacy and compliance carry-overs

1. **No PHI in URIs** (RFC 3986 and common log practice): the patient-registration spec's Individual/Service/Visit IDs embed ProGress ID/NID/DOB. Do not use them as identifiers or URL parts. Keep them, if the programme requires them, only as `Patient.identifier` values with strict access control.
2. **QR codes**: encode only an opaque reference (and a check value), not "all patient fields". A printed code with name, address and service is a data leak.
3. **Synthetic data only** in public repos (`content`, `docs`, tests, `distro-template`). Example patient names in the drafts must not appear in published files.
4. **Secrets**: scan with gitleaks in CI; enable GitHub secret scanning with push protection; remove `local_sync_key` and hashes from templates.
5. **Free-tier clouds** (Supabase, Render) and personal Google Drive: acceptable for development with synthetic data; not for patient data until a DPA, region and retention policy exist.
6. **Compliance language**: follow `AGENTS.md`: never state the software or a deployment is HIPAA/GDPR-compliant or certified without evidence. The `hipaa-ready`, `fhir-r4`, `certified` badges are visual only; **`fhir-r4` is also wrong for an R5 product** — replace with `fhir-r5` or remove.
7. **Supply chain**: `cargo-deny`, `cargo-audit`, Dependabot, pinned Action SHAs, signed releases (sigstore/cosign), SBOM per release, GitHub artifact attestations.
8. **Vulnerability reporting**: GitHub Private Vulnerability Reporting (enable on every repo); `SECURITY.md` points to it; the `zarishsphere.com` email address is removed unless you control it.

---

## 15. Licensing layout

The repositories currently contain three different files that claim to be the licence (`LICENSE` ×2 and `LICENSE_CODE`), plus text referring to another project (`cpintl-brand`). Normalise to the REUSE layout:

| Content | SPDX | File |
| --- | --- | --- |
| Code, automation, workflows | `Apache-2.0` | `LICENSE`, `LICENSES/Apache-2.0.txt` |
| Documentation, prompts, templates | `CC-BY-4.0` | `LICENSES/CC-BY-4.0.txt` |
| Brand kit artwork and tokens | `MIT` (as stated in `profile/assets/LICENSE.md`) | `LICENSES/MIT.txt`; trademark note kept |
| Third-party fonts | `OFL-1.1` | Not redistributed |

Add `REUSE.toml` mapping directories to SPDX IDs, and run `reuse lint` in CI. One `LICENSE` file per repo root; no file may share the name with another.

---

## 16. CI/CD, versioning and releases

| Topic | Rule |
| --- | --- |
| Runners | GitHub-hosted standard runners (free for public repos). Do not create extra orgs to extend quota |
| Reusable workflows | In `.github`, versioned with tag `v1`; repos call `zarishhealth/.github/.github/workflows/<file>@v1` |
| Required checks | `cargo fmt --check`, `cargo clippy -D warnings`, `cargo test`, `cargo deny check`, `cargo audit`, OpenAPI lint (Spectral), Buf lint/breaking, link check, `reuse lint`, gitleaks |
| Rulesets | `main` protected: PR required, 1 review (2 for `core`/`fhir`), required checks, linear history, signed commits recommended, no force-push, no deletion |
| Releases | Conventional Commits → release-plz (or release-please) → tag → GitHub Release with assets named per §4.7, checksums, SBOM, attestation |
| Versioning | SemVer. API: `/api/v1` changes are additive only; breaking → `/api/v2` + deprecation headers. Protobuf: package `…v1` frozen; breaking → `…v2` |
| Pages | `actions/deploy-pages` workflow per repo with Pages |
| Docs links | Link-check on every PR so renamed paths are caught before publishing |
| Dependency updates | Dependabot weekly for `cargo`, `github-actions`, `npm`, `docker` |

---

## 17. Migration checklist from the current state

Current repositories: `.github`, `zarishhealth.github.io`, `docs`, `ZarishHealth-builder`.

| # | Action | Detail |
| --- | --- | --- |
| 1 | Rename `ZarishHealth-builder` → `builder` | Uppercase violates §4.1. GitHub redirects the repo; update links in `index.html`, README, footer |
| 2 | Move both `DRAFT_*.md` files out of repo roots | Archive as `docs/architecture/legacy/…` or delete after this blueprint is adopted; keep this file as `docs/architecture/blueprint.md` and a copy at `.github/BLUEPRINT.md` |
| 3 | Site `README.md` says `styles.css`, the file is `style.css` | Fix text; `index.html` already links `style.css?v=2` |
| 4 | Brand assets served via `raw.githubusercontent.com` | Add workflow `sync-brand-to-pages.yml`: copy `.github/profile/assets/{logo,favicon,icon,social,app-icon}` → `zarishhealth.github.io/assets/brand/`; update `index.html` icon/OG/logo URLs to `/assets/brand/…` |
| 5 | `head-snippet.html` uses `zarishhealth.example` | Replace with `https://zarishhealth.github.io/…` |
| 6 | `BRANDING.md`: says assets live at `.github/profile/assets/` but repo path is `profile/assets/`; repo URL typo `https:github.com…`; "234 files" vs `ASSETS-INDEX.md` "239 files" | Correct; regenerate the index from the file list |
| 7 | `profile/README.md`: anchors `#-why-zarishhealth` do not exist | Point to `#-what-it-does` |
| 8 | Licences (§15) | One clear set |
| 9 | `SECURITY.md` | Replace mailbox on a domain you do not own; keep GitHub private reporting |
| 10 | `CODE_OF_CONDUCT_bn.md` | Rename to `CODE_OF_CONDUCT.bn.md` |
| 11 | Duplicate `LICENSE` in the site repo (two different texts named `LICENSE`) | Keep one |
| 12 | Create repos in §5.1 | Start from templates in §6; enable Pages where listed; add `.nojekyll` where Pages hosts dot-folders |
| 13 | Add `/.well-known/security.txt` | §11.2 |
| 14 | Replace `fhir-r4` badge | §14.6 |
| 15 | Org settings | Enable: Private Vulnerability Reporting, secret scanning + push protection, Dependabot, 2FA required, default branch `main`, restricted Actions (allow-list + SHA pinning), custom properties from §4.1 |

---

## 18. Roadmap (from 2026-10-14)

| Weeks | Deliverable | Exit test |
| --- | --- | --- |
| 1–2 | §17 fixes; `.github` reusable workflows; Pages brand mirror; `security.txt` | `curl -I https://zarishhealth.github.io/.well-known/security.txt` → 200 `text/plain`; logo/OG load from Pages |
| 3–4 | `core` workspace skeleton; `api` OpenAPI v1 draft; problem-type pages; `fhir` IG skeleton publishing to `/fhir/` | CI green; `/fhir/` and `/docs/problems/validation-failed` resolve |
| 5–8 | `zarish-server`: `/livez`, `/readyz`, `/fhir/metadata`, `/api/v1/sites`, RFC 9457 errors, well-known documents; SQLite store | Contract tests pass against `api/openapi`; discovery documents validate |
| 9–12 | Sync: change log, LAN peers, review queue; Tauri app shell | Two devices converge offline; conflicts land in `/api/v1/sync-conflicts` |
| 13–16 | `mcp`: terminology + docs servers (no patient data), registry publication under `io.github.zarishhealth/*` | A 2026-07-28 client lists and calls tools through `Mcp-Method`/`Mcp-Name` |
| 17+ | Pilot with synthetic data; security review; hosting decision for central tier; R6 evaluation | Written ADRs for each |

---

## 19. Open questions and unverified items

1. **MCP server-card path** is not settled (§10.4).
2. **OAuth 2.1** status: MCP references it; confirm whether it is an RFC when you implement.
3. **FHIR terminology URIs and licences** (SNOMED CT, LOINC, ICD-11) must be confirmed per deployment country.
4. **Host for `{API_ORIGIN}`** is undecided. Options: self-hosted at a project office with a dynamic-DNS or tunnel service, or a paid cloud with a DPA. This decision affects TLS and OAuth, not paths.
5. **GitHub raw SVG behaviour**: verify in browser devtools before relying on §2 rule 4 (conclusion is widely reported; check once).
6. **Idempotency-Key** and **RateLimit** headers are IETF drafts; treat as conventions.
7. **UNHCR / Bangladesh identifier system URIs** need confirmation from the issuing authorities.
8. **Exact stable versions** of Rust, Axum, Tauri, SQLx and SQLite were not re-verified for this document; pin the versions from `rustup`/`cargo` on the day you create `core`. Axum 0.8.x and Tauri 2.x are the lines in use.

---

## 20. Sources

- RFC 3986 (URI), RFC 9110 (HTTP semantics), RFC 8615 (Well-Known URIs), RFC 9116 (`security.txt`), RFC 8414, RFC 9728, RFC 9727, RFC 9457, RFC 9745, RFC 9562, RFC 8288, RFC 3339 — rfc-editor.org
- IANA Well-Known URIs registry — <https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml>
- MCP specification 2026-07-28 (transports, authorization, authorization-server discovery) — <https://modelcontextprotocol.io/specification/2026-07-28/>; release notes <https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/>
- MCP Registry (namespaces, `server.json`) — <https://modelcontextprotocol.io/registry/about>
- MCP server-card proposals (SEP-1649/SEP-2127) and related IETF drafts — <https://datatracker.ietf.org/doc/draft-morrison-mcp-dns-discovery/>, <https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/>
- SMART App Launch 2.1 — <https://www.hl7.org/fhir/smart-app-launch/>
- FHIR R5/R6 status — <https://mitre.github.io/fhir-for-research/modules/fhir-versions>
- Rust API Guidelines (naming) — <https://rust-lang.github.io/api-guidelines/naming.html>
- GitHub Pages site types and URLs — GitHub Docs "What is GitHub Pages"; `.nojekyll` and dot-folders — GitHub community threads on Pages and `.well-known`
- GitHub organization profile (`.github/profile/README.md`) — GitHub Docs
