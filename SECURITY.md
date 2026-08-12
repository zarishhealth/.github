# Security Policy

ZarishHealth handles clinical patient data at national scale. Security is not a feature — it is a foundation.

---

## Supported Versions

I actively maintain and patch security vulnerabilities in the following versions:

| Version | Supported |
|---|---|
| Latest stable release | Yes — patches within 48 hours for Critical |
| Previous minor version | Yes — patches within 7 days |
| Older versions | No — please upgrade |

---

## Reporting a Vulnerability

**Do not open a public GitHub Issue for security vulnerabilities.**

Public disclosure before a patch is available puts live health systems at risk.

### How to Report

**Email:** platform@zarishsphere.com
**Subject line:** `[SECURITY] Brief description`
**Response time:** I will acknowledge within 48 hours

Alternatively, use GitHub's built-in **Private Vulnerability Reporting** feature on any repository:
Settings → Security → Report a vulnerability

### What to Include in Your Report

- Description of the vulnerability
- Steps to reproduce it
- Affected component and version
- Potential impact (what data or systems are at risk)
- Your suggested fix, if you have one

---

## What Happens After You Report

1. I acknowledge your report within 48 hours
2. I confirm the vulnerability and assess its severity within 7 days
3. I develop and test a patch
4. I coordinate a disclosure date with you
5. I publish a security advisory and release the patch
6. I credit you in the advisory (unless you prefer anonymity)

---

## Severity Levels

| Level | CVSS Score | Example | Response SLA |
|---|---|---|---|
| Critical | 9.0–10.0 | Unauthenticated patient data access | 48 hours |
| High | 7.0–8.9 | Privilege escalation, auth bypass | 7 days |
| Medium | 4.0–6.9 | Limited data exposure, CSRF | 30 days |
| Low | 0.1–3.9 | Information disclosure, minor issues | 90 days |

---

## Scope

In scope for vulnerability reports:

- All `zs-core-*` repositories (API, auth, audit, crypto)
- All `zs-esm-*` repositories (frontend modules)
- All `zs-infra-*` repositories (infrastructure and CI/CD)
- All deployed services at zarishsphere.com and its subdomains

Out of scope:

- Theoretical vulnerabilities without a proof of concept
- Social engineering of ZarishSphere team members
- Physical security
- Denial-of-service attacks against the demo environment

---

## Security Principles

ZarishSphere implements:

- AES-256 encryption for patient data at rest
- TLS 1.3 for all data in transit
- OAuth 2.1 and SMART on FHIR for all API authorization
- Immutable audit logs for every clinical data access
- Dependabot for automated dependency vulnerability scanning
- CodeQL static analysis on all source code
- Signed commits required on all security-critical repositories

---

## Bug Bounty

ZarishHealth does not currently offer a paid bug bounty program. I acknowledge all responsible disclosures publicly (with your permission) and prioritize your report at the top of the patch queue.

---

## Contact

**Email:** platform@zarishsphere.com
**PGP Key:** Available on request