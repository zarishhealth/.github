# ZarishHealth Path-Specific Instructions: Patient Privacy & PHI (HIPAA)

> **File Pattern**: `services/patient/**`, `**/phi/**`, `**/patient/**`, `**/medical/**`, `api/health/**`  
> **Scope**: Path-specific Copilot Chat, Copilot Edits, and Copilot Code Review instructions for healthcare compliance.

---

## 1. Primary Rule: Zero Plain-Text PHI

When generating, refactoring, or reviewing code matching this file pattern, strictly enforce HIPAA Protected Health Information (PHI) constraints:

* **No Real Identifiers**: Never generate real or realistic-looking Medical Record Numbers (MRN), Social Security Numbers (SSN), Patient Names, DOBs, or Addresses in code, mock data, unit tests, or comments.
* **Synthetic Test Fixtures**: All mock data in test files must be explicitly initialized using synthetic data generators and marked with the constant tag `SYNTHETIC_TEST_DATA_ONLY`.
* **Sanitization at Ingress**: Every API endpoint handling patient input must apply strict runtime schema validation (Zod for TypeScript, Pydantic for Python) and sanitize fields prior to persistence or downstream routing.

---

## 2. Mandatory Code & Review Checklist

When writing or analyzing functions in these paths:

1. **Logging Hygiene**: Verify that all logging calls pass data through an automatic PHI scrubber function (`scrub_phi(payload)` or `mask_patient_data(data)`). Never log raw request bodies.
2. **Database Storage**: Confirm that patient data attributes (SSN, medical notes, diagnoses) are encrypted at rest using AES-256 before writing to storage.
3. **Transmission**: Enforce TLS 1.3 encryption on all external network requests.
4. **Access Control**: Ensure every handler verifies JWT/OAuth patient scope claims and tenant boundaries (`tenant_id == resource.tenant_id`).

---

## 3. Example Schema Compliance Pattern

```typescript
// Required Zod schema pattern for patient payload ingress
import { z } from "zod";

export const PatientIngressSchema = z.object({
  patientId: z.string().uuid(),
  encryptedMedicalNotes: z.string().min(1),
  consentVerified: z.boolean().refine((val) => val === true, {
    message: "HIPAA consent must be explicitly verified.",
  }),
});

export type PatientIngressInput = z.infer<typeof PatientIngressSchema>;
```
