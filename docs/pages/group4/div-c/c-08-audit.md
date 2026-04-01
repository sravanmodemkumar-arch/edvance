# C-08 — Audit Trail & 12A/80G Compliance

> **URL:** `/college/fees/audit/`
> **File:** `c-08-audit.md`
> **Priority:** P1
> **Roles:** Finance Manager (S4) · Statutory Auditor (external) · Principal/Director (S6)

---

## 1. Audit Requirements

```
AUDIT FRAMEWORK — GCEH

STATUTORY AUDIT:
  Auditor: Chartered Accountant (registered firm)
  Audit type: Financial statement audit (Income & Expenditure, Balance Sheet)
  Filing: Form 10B (for institutions with income >₹1Cr claiming 12A exemption)
  Deadline: 30 September of following year (e.g., 2025–26 → by 30 Sep 2026)
  Status: ✅ Filed 28 Sep 2026

COMPLIANCE AUDITS:
  AICTE Inspection (random): As scheduled by AICTE/state
  NAAC Assessment: Every 5 years (next: 2029)
  JNTU Affiliation renewal: Every 3 years (inspection of facilities and records)
  Income Tax Survey (possible): Any time for Form 10B filers
  GST (ancillary services): Annual return if any taxable supply

12A/80G COMPLIANCE:
  Trust registration: ✅ (original 2010)
  12A exemption certificate: ✅ Valid
  80G certificate: ✅ Valid (donors can claim 50% deduction on donations)
  Annual declaration: No surplus distributed to promoters/founders ✅
  FCRA (if foreign funds): Not applicable (no foreign funding received)
```

---

## 2. Fee Transaction Audit Trail

```
AUDIT TRAIL — Fee Module

All fee transactions are logged with:
  Timestamp, student ID, amount, mode, gateway transaction ID, processed by

IMMUTABLE LOG: Transactions once entered cannot be deleted (only corrections
  via journal entries with reason codes)

AUDIT REPORT (Accounts Officer view):
  Date range: 1 April 2026 – 31 March 2027
  Total transactions: 1,842
  Total amount: ₹8,24,00,000
  Corrections made (journal entries): 12 (all with reasons)
  Refunds processed: 18

[Export audit trail for CA]  [Generate Form 10B working sheet]
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/fees/audit/trail/` | Full audit trail (date-range) |
| 2 | `GET` | `/api/v1/college/{id}/fees/audit/12a-compliance/` | 12A/80G compliance status |
| 3 | `GET` | `/api/v1/college/{id}/fees/audit/form10b-worksheet/` | Form 10B data worksheet |

---

## 4. Business Rules

- Fee accounting must follow double-entry; all credit entries (fees received) must have corresponding debit entries (student ledger); an unbalanced trial balance is a red flag for the auditor and signals either data entry errors or attempted manipulation
- 12A exemption requires annual renewal (Form 10A/10AB under new Tax regime); colleges that miss renewal face loss of exemption and retrospective tax liability; EduForge sends a renewal reminder 90 days before the exemption certificate expiry date
- Statutory audit findings (qualified opinion, adverse observations) must be placed before the Governing Body within 30 days; the Governing Body's response is recorded; NAAC asks about audit findings and management responses during accreditation

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division C*
