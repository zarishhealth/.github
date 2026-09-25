# ZarishHealth Main Repository Context & Architectural Blueprint

> **File Path**: `AGENTS.md` (Repository Root)  
> **Target Audience**: GitHub Copilot Chat, Copilot Edits, Copilot CLI, Copilot Cloud Agents, and Copilot Code Review.  
> **Organization**: ZarishHealth (AI-Native Healthcare Automation Platform)

---

## 1. Repository Purpose & Domain Context

This repository houses the core services and automation hub for **ZarishHealth**, an AI-native healthcare platform. The system processes patient records, manages clinical workflows, orchestrates automated CI/CD pipelines, and executes compliance audits.

Copilot agents and reviewers must treat this codebase as a **regulated healthcare system**. Architectural simplicity, strict type safety, zero plain-text Protected Health Information (PHI), and adherence to HIPAA guardrails are mandatory across all modules [85, 90].

---

## 2. System Architecture & Intentional Design Patterns

```
                               ┌────────────────────────────────────────┐
                               │       API Gateway / Public Ingress     │
                               └───────────────────┬────────────────────┘
                                                   │ (Schema Validation)
                                                   ▼
 ┌──────────────────────────────────┐    ┌──────────────────────────────────┐
 │    Core Healthcare Services      │    │    PHI / Patient Data Subsystem  │
 │  - /services/telehealth/         │    │  - /services/patient/            │
 │  - /services/billing/            │    │  - /api/health/                  │
 │  - /services/compliance/         │    │  (Strict Anonymization Boundary)  │
 └─────────────────┬────────────────┘    └─────────────────┬────────────────┘
                   │                                       │
                   └───────────────────┬───────────────────┘
                                       │ (TLS 1.3 / AES-256)
                                       ▼
                       ┌────────────────────────────────┐
                       │   Database & Storage Layer     │
                       └────────────────────────────────┘
```

### A. Clean / Hexagonal Architecture
* Core business logic (domain entities, clinical rules) is isolated from external frameworks, HTTP routers, and database adapters.
* Secondary adapters (database drivers, third-party EHR APIs) must implement typed interfaces defined in the domain layer.

### B. PHI Isolation Boundary
* Code residing in `/services/patient/` and `/api/health/` handles sensitive patient data structures.
* All data crossing this boundary must pass through explicit sanitization and redaction middleware before persistence or logging [85].

### C. Asynchronous & Serverless Workflows
* Background jobs, nightly compliance checks, and automated maintenance tasks execute via **GitHub Agentic Workflows (`gh-aw`)** and serverless workers (Cloudflare Workers/Probot) [45, 60].

---

## 3. High-Scrutiny Subsystems & Strict Guidelines

When operating on or reviewing code within these directories, apply elevated scrutiny:

| Subsystem Path | Primary Focus | Mandatory Requirements |
| :--- | :--- | :--- |
| **`/services/patient/`** | Patient Data Processing | Strict PHI redaction; zero hardcoded identifiers; full Pydantic/Zod schema validation. |
| **`/api/health/`** | Ingress API Endpoints | Rate-limiting; TLS 1.3 enforcement; RBAC scope verification. |
| **`.github/workflows/`** | Automation & CI/CD | Unmetered public runner routing; exponential backoff for `GITHUB_TOKEN` (max 1,000 requests/hr/repo); pin Actions by SHA. |
| **`/.github/`** | Copilot Governance | Ensure custom instructions and agents remain aligned with `.github/copilot-instructions.md`. |

---

## 4. Testing & Mock Data Policies

1. **Synthetic Data Rule**: Never use real or realistic PHI in unit tests, integration tests, or mock fixtures. All mock data must be explicitly generated and annotated with `SYNTHETIC_TEST_DATA_ONLY`.
2. **Deterministic Tests**: Unit tests must run asynchronously without external network dependencies. External EHR or billing APIs must be mocked using MSW (Mock Service Worker) or Python `unittest.mock`.
3. **Automated Coverage Gates**: Any pull request modifying domain models or security middleware must include unit tests covering both happy path and edge-case error scenarios.

---

## 5. Tooling & MCP Integration Guidance

Copilot agents reviewing or modifying this codebase should leverage configured **Model Context Protocol (MCP)** servers [10, 47]:

* **`github-mcp-server`**: Query repository commit histories, analyze Actions workflow run logs, and inspect linked issues [47, 48].
* **`dynatrace-security`**: Perform automated runtime vulnerability analysis and security posture verification [11, 12].

---

> *ZarishHealth Engineering Governance Board — Repository Context Specification*
