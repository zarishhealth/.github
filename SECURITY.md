# Security Policy for ZarishHealth

ZarishHealth builds sovereign, paperless, offline-first Health Information Management Systems (HIMS) for non-profit healthcare networks, humanitarian operations, and clinical facilities. Because our software manages sensitive Personal Health Information (PHI) across distributed, offline-first field sites, maintaining robust security, privacy, and data integrity is paramount.

---

## 1. Supported Versions & Tiers

We actively maintain security updates for the following components and release tracks across our three organizational tiers:

| Component / Track | Supported Status | Notes |
| :--- | :--- | :--- |
| **ZarishHealth Core Engine** | :white_check_mark: Supported | Main clinical data model & offline sync reconciliation engine |
| **ZarishHealth App (Desktop/Mobile/Web)** | :white_check_mark: Supported | Multi-platform field clinician interface |
| **ZarishHealth Deploy Scripts & Images** | :white_check_mark: Supported | Containerized field deployment & local site scripts |
| **Org Profile & Config (`zarishhealth/.github`)** | :white_check_mark: Supported | Shared community health & organization security policies |
| **Legacy / Unofficial Custom Forks** | :x: Unsupported | Please rebase or migrate to the official ZarishHealth releases |

---

## 2. Reporting a Vulnerability Privately

We strongly encourage responsible, coordinated disclosure. If you discover a potential security flaw—especially those affecting patient confidentiality, offline peer-sync integrity, or field deployment encryption—please report it privately.

### Preferred Reporting Method: GitHub Private Vulnerability Reporting
1. Navigate to the specific **ZarishHealth repository** (e.g., `https://github.com/zarishhealth/.github` or related core repos).
2. Click on the **Security** tab near the top of the repository homepage.
3. In the left sidebar, select **Report a vulnerability**.
4. Complete the private submission form with your findings and click **Submit report**.

### Alternative Confidential Reporting Method
If you are unable to use GitHub Private Vulnerability Reporting, you may email our security maintainers directly:
* **Security Contact Email:** `health-coc@zarishsphere.com` (cc: `zarishhealth@gmail.com`)
* **Subject Line:** `[SECURITY] Potential Vulnerability Report - ZarishHealth`

> ⚠️ **DO NOT open public GitHub Issues, Pull Requests, or Discussions for security vulnerabilities.**

---

## 3. Information to Include in Your Report

To help our team quickly triage and address the issue, please include:
* **Component & Version:** The specific repository, file, or deployment image version affected.
* **Vulnerability Class:** (e.g., Local LAN Sync Poisoning, Unauthorized PHI Access, Weak Cryptography, Insecure Direct Object Reference, Privilege Escalation).
* **Proof of Concept (PoC):** Step-by-step reproduction instructions or sanitized test code.
* **Health & Operational Impact:** Assessment of risk to offline field nodes, local store data, or patient record privacy.

---

## 4. Response & Remediation SLA

Our maintainers commit to the following workflow for security reports:

* **Initial Acknowledgment:** Within **48 hours** of report receipt.
* **Triage & Validation:** Within **5 business days**, confirming validity and severity impact.
* **Fix & Patch Development:** High-severity issues impacting PHI or offline sync security will be prioritized for rapid patching.
* **Coordinated Disclosure:** We will publish a Security Advisory once a patch is tested and made available to field sites.

---

## 5. Security & Privacy Architectural Guidelines

When reviewing or testing ZarishHealth, note our core security principles:
* **Local-First Isolation:** Local clinic stores are the source of truth; data that never leaves the building cannot be breached from the outside.
* **Offline-First Security:** Security policies, authentication checks, and encryption must work deterministically offline without requiring cloud verification.
* **No Synthetic / Live PHI in Reports:** Never include real patient health data or live clinic environment tokens in your report or PoC.

---

## 6. Safe Harbor Policy

We welcome security research conducted in good faith. ZarishHealth will not initiate legal action against researchers who:
* Respect user privacy and refrain from accessing, modifying, or destroying real PHI or live clinic data.
* Allow reasonable time for remediation before public disclosure.
* Comply with applicable local and international data protection laws.
