# N-03 — Data Privacy (DPDPA 2023)

> **URL:** `/coaching/compliance/data-privacy/`
> **File:** `n-03-data-privacy.md`
> **Priority:** P1
> **Roles:** Director (K7) · IT Coordinator (K3) · Branch Manager (K6)

---

## 1. DPDPA Compliance Overview

```
DATA PRIVACY COMPLIANCE — DPDPA 2023
Toppers Coaching Centre | Data Fiduciary: TCC Edu Pvt Ltd

  COMPLIANCE STATUS: ✅ COMPLIANT (as of 31 March 2026)

  WHAT DPDPA 2023 REQUIRES:
    1. Consent before collecting personal data ✅
    2. Purpose limitation (use data only for stated purpose) ✅
    3. Data minimisation (collect only what's needed) ✅
    4. Accuracy (keep data up to date) ✅
    5. Storage limitation (retain only as long as necessary) ✅
    6. Security safeguards (M-04 IT systems) ✅
    7. Accountability (Director is the Data Fiduciary) ✅
    8. Data Principal rights (access, correction, erasure, grievance) ✅
    9. Breach notification (within 72 hours to DPDPB + affected individuals) ✅
    10. Cross-border data localisation (India hosting confirmed) ✅

  TCC DATA CATEGORIES:
    Category                 │ Examples                    │ Sensitivity │ Consent Basis
    ─────────────────────────┼─────────────────────────────┼─────────────┼──────────────────
    Identity data            │ Name, photo, DOB, address   │ Medium      │ Enrollment form
    Contact data             │ Phone, email, WhatsApp      │ Medium      │ Enrollment form
    Academic data            │ Scores, attendance, doubts  │ Medium      │ Enrollment form
    Financial data           │ Fee, EMI, bank details      │ High        │ Enrollment form
    Health/welfare data      │ Aid applications, counsellg │ High        │ Explicit consent
    Marketing data           │ Testimonial, photo/video    │ High        │ Separate consent
    Biometric data           │ Fingerprint (attendance)    │ V.High      │ Explicit consent*
    ─────────────────────────┴─────────────────────────────┴─────────────┴──────────────────
    * Biometric data requires explicit, specific consent under DPDPA
```

---

## 2. Consent Management

```
CONSENT REGISTER — TCC Data Processing Activities

  CONSENT TYPE              │ Collected via         │ Students Consented │ Opt-outs
  ──────────────────────────┼───────────────────────┼────────────────────┼──────────
  General data processing   │ Enrollment form (F-04)│  1,840 (100%) ✅   │   0
  Biometric attendance       │ Biometric consent form│  1,612 (87.6%) ✅  │  228 *
  Marketing communications   │ Enrollment opt-in     │  1,540 (83.7%) ✅  │  300
  Testimonial / success story│ Separate consent form │     94 (consented) │   26 withdrawn
  Alumni result tracking     │ Alumni opt-in         │  2,640 (54.5%)    │  2,200 no report
  Survey participation       │ Survey platform login │  1,176 (per survey)│  Opt-out = skip
  ──────────────────────────┴───────────────────────┴────────────────────┴──────────
  * 228 students use manual attendance (alternative provided — DPDPA compliant)

  DPDPA DATA PRINCIPAL RIGHTS REQUESTS (AY 2025–26):
    Right to access own data:    4 requests | fulfilled within 7 days ✅
    Right to correction:         8 requests | fulfilled within 5 days ✅
    Right to erasure:            2 requests | processed (marketing data erased) ✅
    Right to grievance:          1 request  | resolved in 15 days ✅
    TOTAL: 15 requests — 0 escalated to Data Protection Board
```

---

## 3. Privacy Notices & Policies

```
PRIVACY NOTICES — Published by TCC

  DOCUMENT                         │ Published │ Location              │ Last Updated
  ─────────────────────────────────┼───────────┼───────────────────────┼──────────────
  Privacy Policy                   │ ✅        │ Website + portal      │ Oct 2023
  Cookie Policy                    │ ✅        │ Website               │ Oct 2023
  Enrollment Data Notice           │ ✅        │ Enrollment form (F-04)│ Aug 2025
  Marketing Consent Disclosure     │ ✅        │ Enrollment form       │ Aug 2025
  Biometric Consent Notice         │ ✅        │ Biometric form        │ Aug 2025
  CCTV Notice (physical signage)   │ ✅        │ All CCTV locations    │ Jan 2026
  Alumni/Testimonial Consent Form  │ ✅        │ Counsellor-issued     │ Mar 2026
  WhatsApp Opt-in Notice           │ ✅        │ WhatsApp business msg │ Jan 2026
  ─────────────────────────────────┴───────────┴───────────────────────┴──────────────

  DATA RETENTION SCHEDULE:
    Student enrollment data:       Duration of course + 3 years (for certificate issuance)
    Financial records:             7 years (Income Tax Act requirement)
    CCTV footage:                  30 days rolling
    Marketing consent (withdrawn): Suppression list retained permanently (DPDPA requirement)
    Alumni data (with consent):    Until withdrawal or 10 years inactivity
    HR/payroll records:            7 years (tax filing requirement)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/compliance/privacy/status/` | DPDPA compliance overview |
| 2 | `GET` | `/api/v1/coaching/{id}/compliance/privacy/consents/` | Consent register |
| 3 | `POST` | `/api/v1/coaching/{id}/compliance/privacy/rights-request/` | Submit data rights request |
| 4 | `GET` | `/api/v1/coaching/{id}/compliance/privacy/rights-requests/` | All rights requests and status |
| 5 | `GET` | `/api/v1/coaching/{id}/compliance/privacy/breach-log/` | Data breach log (restricted) |
| 6 | `POST` | `/api/v1/coaching/{id}/compliance/privacy/breach-report/` | Report a data breach |

---

## 5. Business Rules

- Consent under DPDPA 2023 must be free, specific, informed, and unambiguous; a blanket consent ("by enrolling you agree to all data processing") is not valid for purposes beyond the core service (education); marketing communications, biometric collection, and testimonial use each require separate, specific consent; bundling all consents into one checkbox at enrollment is not DPDPA-compliant; TCC's enrollment form uses separate checkboxes for each distinct processing purpose; pre-ticking these boxes is also non-compliant — each must be actively selected by the student (or parent for minors)
- The right to erasure (the "right to be forgotten") under DPDPA requires TCC to delete a student's personal data when they request it, subject to legal retention requirements; TCC cannot erase financial records required for 7-year tax retention; TCC cannot erase data subject to a legal dispute; but TCC must erase marketing data, testimonials, and non-mandatory data when a withdrawal request is received; the 2 erasure requests this year (marketing data) were fulfilled by removing the student's contact from all marketing lists, deleting their testimonial from active channels, and confirming deletion in writing to the student
- A data breach (unauthorised access, accidental exposure, or loss of student personal data) must be reported to the Data Protection Board of India (DPDPB) within 72 hours of TCC becoming aware; simultaneously, affected individuals must be notified without undue delay; the breach notification must describe: what data was affected, how many individuals, what happened, what TCC is doing to contain it, and what affected individuals should do; a breach where a laptop containing unencrypted student data is stolen requires immediate notification; a breach where only test scores (not financial or identity data) were briefly visible to the wrong user may require notification depending on sensitivity
- Biometric data (fingerprints collected via attendance devices) is classified as sensitive personal data under DPDPA 2023 and requires explicit consent; 228 students who did not consent to biometric collection use manual attendance (proximity card or name register); the manual alternative must be genuinely equivalent — a student who refuses biometric consent must not be penalised in attendance calculation or treated differently from biometric-consenting students; biometric data stored in the attendance device is never shared with third parties; the device manufacturer's data handling agreement must confirm Indian data storage
- TCC's Privacy Policy must be reviewed and updated annually or whenever there is a material change in data processing activities; launching the online test series (Initiative 1, L-07) for external students is a new processing activity that requires Privacy Policy update before launch; using a new analytics tool (that receives student data) is a new processing activity requiring privacy impact assessment; the Director is personally responsible as the Data Fiduciary for all DPDPA compliance; delegating to the IT coordinator or accounts team does not reduce the Director's liability — only the operational tasks are delegated, not the accountability

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division N*
