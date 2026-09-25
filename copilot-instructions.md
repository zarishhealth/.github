# ZarishHealth GitHub Organization: Primary Copilot Instructions

> **Path**: `.github/copilot-instructions.md`  
> **Scope**: Repository-Wide & Organization-Wide Guidance for GitHub Copilot Chat, Copilot Edits, Copilot CLI, Copilot Code Review, and Cloud Agents.  
> **Organization**: ZarishHealth (AI-Native Healthcare Automation Hub)

---

## 1. Organization Mission & Core Principles

ZarishHealth is an **AI-native healthcare technology organization** operating an automated software engineering platform within GitHub's **always-free infrastructure tier**. All AI assistants, custom agents, and automated workflows operating in this codebase must strictly observe the following core principles:

1. **Patient Data Privacy & HIPAA Compliance First**: Medical data protection, strict anonymization, and regulatory compliance override velocity or convenience.
2. **Zero-Trust Security**: No hardcoded credentials, token leaks, or unvalidated input processing.
3. **Always-Free Infrastructure Alignment**: Workflows must operate efficiently within GitHub's free-tier primitives (public repository unmetered compute, strict API rate-limit hedging, BYOK offloading, and automated artifact garbage collection).
4. **Deterministic & Testable Implementations**: AI-generated code must be fully typed, clean, self-documenting, and accompanied by comprehensive unit/integration tests.

---

## 2. Healthcare & Regulatory Standards (HIPAA / PHI Guardrails)

When generating, modifying, or reviewing code across ZarishHealth repositories, Copilot must enforce strict Protected Health Information (PHI) and Health Insurance Portability and Accountability Act (HIPAA) compliance:

### A. PHI Data Handling & Masking
* **Zero Plain-Text PHI**: Never include real or plausible-looking patient identifiers (Medical Record Numbers [MRN], Social Security Numbers [SSN], Patient Names, Dates of Birth, Biometric Identifiers, or Contact Information) in code, unit tests, mock fixtures, documentation, or commit messages.
* **Synthetic Mock Data Only**: All test fixtures and seeds must use explicitly synthetic data generators clearly tagged with `SYNTHETIC_TEST_DATA_ONLY`.
* **Data Sanitization at Ingress**: All API endpoints accepting patient payloads must implement strict runtime schema validation (e.g., Zod, Pydantic) and strip or redact unauthorized fields before persistence or logging.
* **Log Scrubbing**: Ensure logging utilities automatically filter out potential PHI fields before outputting to stdout or external observability drains (e.g., Dynatrace).

### B. Security & Credential Protection
* **No Hardcoded Secrets**: Never embed API keys, OAuth tokens, private keys, or connection strings in source files. Use fine-grained GitHub Secrets (`COPILOT_SPONSOR_PAT`, etc.) or environment variables.
* **Push Protection Compatibility**: Rely on GitHub Secret Protection and push protection. If a secret pattern is flagged, immediately redact it; do not attempt to bypass or suppress security warnings.
* **Encryption Standards**: Enforce TLS 1.3 for data in transit and AES-256 for data at rest across all storage layers.

---

## 3. Technology Stack & Coding Conventions

### A. TypeScript & React (Frontend & Web Services)
* **Strict Type Safety**: `noImplicitAny: true`, `strictNullChecks: true`. Avoid using `any`; define explicit interfaces, type aliases, or Zod schemas.
* **Functional Components & Hooks**: Use functional React components with hooks. Avoid legacy class components.
* **Property Shorthand**: Maintain consistent object property shorthand (e.g., `const user = { name, age }`).
* **Error Boundaries & Defend-in-Depth**: Wrap asynchronous operations and API calls in structured `try/catch` blocks with typed error handling.

### B. Python (Backend Services & Agent Runtime)
* **Type Annotations**: Enforce Python 3.12+ type hints on all function signatures (`def process_patient(record: PatientRecord) -> Result:`).
* **Pydantic Validation**: Use Pydantic v2 models for data parsing, settings management, and API request/response serialization.
* **Async IO**: Prefer `async/await` for database access, HTTP requests, and external tool calls to ensure non-blocking execution.

### C. Infrastructure as Code & Actions
* **GitHub Actions Workflows**: Use pin-by-SHA for third-party Actions dependencies. Restrict permissions using minimum required scopes (`permissions: contents: read`).
* **Dev Containers**: Maintain `.devcontainer/devcontainer.json` for reproducible GitHub Codespaces setup.

---

## 4. Architecture & Instruction Hierarchy

To ensure Copilot operates with full context while respecting repository boundaries, observe the organization's multi-layered context model:

```
ZarishHealth Repository Root/
├── AGENTS.md                                   # Repository architecture & health context
├── .github/
│   ├── copilot-instructions.md                 # Primary org-wide instructions (THIS FILE)
│   └── instructions/                           # Path-specific instruction overrides
│       ├── api.instructions.md                 # Applied to API & backend code
│       └── privacy.instructions.md             # Applied to PHI/HIPAA handling modules
```

1. **Global Instructions (`.github/copilot-instructions.md`)**: Contains overarching standards (this file), applied across all Copilot Chat, Edits, and Code Review interactions.
2. **Repository Architecture (`AGENTS.md`)**: Located at the repository root to describe domain models, intentional architectural choices, system boundaries, and test setups.
3. **Path-Specific Instructions (`.github/instructions/*.instructions.md`)**: Triggered automatically by glob patterns for localized enforcement (e.g., strict HIPAA sanitization for `/services/patient/`).
4. **Agent Distribution Model**: Platform agents managed in `agent-platform` are automatically synced and flattened into `.github-private/agents/*.agent.md` to surface in developers' IDE agent pickers across the entire organization.

---

## 5. AI-Native SDLC Workflows

### A. Spec-Driven Development (`spec-kit`)
* When implementing new features, follow the **Spec-Driven Development** flow (`.github/spec-kit`):
  1. Write structured feature specifications (`.spec.md`).
  2. Generate actionable implementation plans with sub-tasks.
  3. Drive agentic code generation based on approved specifications.

### B. Agentic Workflows & Cloud Automations (`gh-aw`)
* Define GitHub Agentic Workflows in Markdown with YAML frontmatter. Ensure agent jobs are read-only and sandboxed by default, applying file modifications through dedicated, safe-output jobs.
* Cloud agent automations should handle routine tasks (nightly builds, issue labeling, test generation) autonomously.

### C. Model Context Protocol (MCP) Integration
* Utilize the **GitHub MCP Server** to query repository commits, inspect issues, and analyze Actions workflow runs via natural language.
* Integrate the **Dynatrace MCP Server** for automated vulnerability analytics and runtime security scanning.

### D. Copilot Code Review Standards
* Copilot Code Review automatically evaluates pull requests against this file, `AGENTS.md`, and any path-specific `.instructions.md` rules.
* Code reviews must prioritize:
  1. HIPAA compliance & security regressions.
  2. Type safety and zero implicit `any`.
  3. Performance & unmetered free-tier compute efficiency.
  4. Code readability and test coverage.

---

## 6. Always-Free Infrastructure & Budget Guardrails

To ensure ZarishHealth maintains zero operational software costs, Copilot and automated workflows must operate within GitHub's free-tier boundaries:

1. **Public Compute Routing**: Direct continuous integration compute and high-volume background tasks to public repositories to leverage **unmetered GitHub Actions execution minutes**.
2. **BYOK Offloading**: For heavy background programmatic tasks, leverage the Copilot SDK or BYOK harnesses (e.g., OpenHands, Cline) to execute agent loops using external model endpoints, preserving monthly Copilot requests.
3. **API Rate-Limit Hedging**: Enforce job queuing and exponential backoff in automation scripts to ensure total API calls remain strictly under the **1,000 requests/hour/repo** threshold for `GITHUB_TOKEN`.
4. **Automated Resource Pruning**: Nightly cron workflows must automatically purge old workflow run logs, temporary build artifacts, and stale container tags to keep private storage within free account quotas (500 MB Packages storage, 15 GB Codespaces storage).

---

> *ZarishHealth Engineering Governance Board — Always-Free AI-Native Architecture Specification*
```
