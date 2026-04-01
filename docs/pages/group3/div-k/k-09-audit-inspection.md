# K-09 — Audit & Inspection Management

> **URL:** `/school/compliance/audit/`
> **File:** `k-09-audit-inspection.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full access · Compliance Officer (S4) — prepare and track · Administrative Officer (S3) — coordinate documentation · Accounts Officer (S3) — financial audit records

---

## 1. Purpose

Manages all types of inspections and audits that a school may face — CBSE affiliation inspection, state education department inspection, RTE audit by DEO, financial audit (internal and external), tax audit, and POCSO/NCPCR inspections. Being "inspection ready" at all times (not just the week before) is the standard EduForge enforces.

Types of inspections:
- **CBSE affiliation inspection:** Scheduled by CBSE every 5 years (or on complaint); determines grade (A/B/C) and conditions
- **State DEO inspection:** Annual or as warranted by complaints; covers RTE compliance, teacher qualifications, fee structure
- **Financial/statutory audit:** Annual by chartered accountant (mandatory for trusts and NGOs); internal audit quarterly
- **Income Tax audit (12A/80G):** For charitable trusts running the school; ensures income tax exemption conditions are met
- **NCPCR/NHRC inspection:** On complaint of child rights violations; rare but serious
- **FSSAI inspection:** For canteen/mess; may be unannounced

---

## 2. Inspection Log

```
Inspection Log                                       [+ Log Inspection]
Academic Year: [2026–27 ▼]

Past Inspections:
  Date         Type                      Authority      Grade/Outcome   Follow-up Due
  Feb 2024     CBSE Affiliation          CBSE           Grade A         2 conditions
  Apr 2024     State DEO Annual          TG DEO         Satisfactory    —
  Sep 2025     RTE Compliance audit      DEO RTE cell   Satisfactory    1 minor note
  Nov 2025     Financial audit (annual)  CA Firm         Unqualified ✅  —
  Jan 2026     FSSAI — canteen          FSSAI           Satisfactory    2 suggestions
  Mar 2026     Internal audit (Q3)       Internal CA    Satisfactory    3 recs

Upcoming:
  Apr 2026     FSSAI — hostel mess      FSSAI           (unannounced)   —
  Jun 2026     Internal audit (Q1 FY27)  Internal CA    (scheduled)     —
  2028–29      CBSE Affiliation (next)  CBSE            (5-year cycle)  —
```

---

## 3. CBSE Inspection Preparation

```
CBSE Inspection Readiness — Current Status

Next full inspection: 2028–29 (planning now — 2 years ahead)

Inspection readiness score: 87/100

Key areas:
  Infrastructure: 22/25 — Library area shortfall (K-01 condition)
  Staff qualifications: 18/20 — 5 teachers pending TET (K-02)
  Student records: 20/20 ✅ — All registers complete
  Fee compliance: 20/20 ✅ — No capitation fee; fee structure filed
  Safety: 15/15 ✅ — Fire NOC, building cert, transport register
  Welfare: 12/15 — CWSN support partially documented; PTM register 1 gap

Action plan:
  By June 2026: Library renovation start (to reach 200 sq.m by 2027)
  By Dec 2026: 5 TET teachers complete TET (or replace)
  Immediate: Close PTM register gap (F-07 — Term 2 minutes entry)

[Generate CBSE inspection simulation report]  [Assign action items to staff]
```

---

## 4. DEO Inspection (State Education Department)

```
DEO Inspection — TG State DEO — April 2024

Inspection scope (annual state inspection):
  ● Teacher attendance register
  ● Student enrollment (match with state DISE/UDISE data)
  ● RTE 25% seats
  ● Fee structure (no excess charging)
  ● Infrastructure basic check
  ● Midday Meal (N/A for private schools)

Findings from April 2024:
  ✅ Teacher attendance: Satisfactory
  ✅ UDISE enrollment data: Matched (minor discrepancy of 2 students in UDISE — corrected)
  ✅ RTE 25% seats: Compliant
  ✅ Fee: No overcharging observed
  ⚠️ Infrastructure: One classroom exceeded 40 students per class (overcrowded — temporary)
     Action: Additional section created for Class VII (May 2024) ✅ resolved

Next DEO inspection: April 2026 (expected)
Preparation checklist:
  ☑ UDISE data updated (annual submission: 30 Sep 2025) ✅
  ☑ Staff attendance register ready
  ☑ RTE admission records (lottery, DCPU, enrollment) ready
  ☑ Fee receipts and fee structure document ready
  ☑ PTM records ready
```

---

## 5. Financial Audit

```
Annual Financial Audit — 2024–25

Audit firm: M/s Sharma & Associates (Chartered Accountants)
Audit type: Statutory audit under Trust Act + IT Act 12A exemption
Audit period: April 2024 to March 2025

Audit outcome: Unqualified audit report ✅
  (No material misstatement; accounts present a true and fair view)

Key figures audited:
  Total fee income: ₹2,85,50,000
  Total expenditure: ₹2,42,30,000
  Surplus: ₹43,20,000 (reinvested in infrastructure per Trust resolution)
  No capitation fee income: ✅ (certified)
  Charitable purpose compliance (12A): ✅

Management letter findings (non-material):
  1. Petty cash vouchers: 3 vouchers missing (minor) — corrective process issued
  2. Fixed asset register: 2 items not tagged — tagged by December 2025 ✅
  3. Bank reconciliation: One month delayed — process tightened ✅

Audit report filed with:
  ☑ Income Tax (Form 10B): Filed 30 Sep 2025 ✅
  ☑ Society Registrar: Annual return filed ✅
  ☑ CBSE (fee compliance certificate): Filed Oct 2025 ✅

Next audit: April–June 2026 (for FY 2025–26)
[Upload audit report]  [Track management letter actions]
```

---

## 6. Unannounced Inspection Protocol

```
Protocol: What to do when an inspector arrives unannounced

Common unannounced inspectors:
  - FSSAI food safety officer (canteen/kitchen)
  - State DEO field officer (any time — common in government schools)
  - Labour Inspector (if school has contractual workers)
  - Tax officer (rare for schools, but happens)

Protocol:
  1. Receptionist notifies Principal within 5 minutes of inspector's arrival
  2. Principal (or VP if absent) greets inspector, verifies identification
  3. Administrative Officer alerted — begins pulling requested documents
  4. Inspector escorted at all times (no unaccompanied access to student areas)
  5. Comply fully — do not obstruct; do not decline reasonable requests

FSSAI unannounced inspection:
  ☑ Canteen and kitchen are always clean and compliant (not just for inspections)
  ☑ FSSAI licence displayed on kitchen wall ✅
  ☑ Food handler medical fitness certificates available ✅
  ☑ Temperature logs (if refrigeration) — up to date
  ☑ No expired items in kitchen

[Log unannounced inspection]  [Upload any show-cause or notice received]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/compliance/audit/` | Inspection log |
| 2 | `POST` | `/api/v1/school/{id}/compliance/audit/` | Log inspection event |
| 3 | `GET` | `/api/v1/school/{id}/compliance/audit/{inspection_id}/` | Inspection detail and findings |
| 4 | `PATCH` | `/api/v1/school/{id}/compliance/audit/{inspection_id}/actions/` | Update follow-up actions |
| 5 | `GET` | `/api/v1/school/{id}/compliance/audit/cbse-readiness/` | CBSE inspection readiness score |
| 6 | `GET` | `/api/v1/school/{id}/compliance/audit/financial/` | Financial audit records |

---

## 8. Business Rules

- All inspection findings (even positive ones) are logged; an inspection with "satisfactory" outcome and zero findings is as important to record as one with adverse findings — the log shows a pattern of compliance
- Show-cause notices from any authority (CBSE, DEO, FSSAI, RTO) are logged as high-priority items with a response deadline; the school's response is drafted, reviewed by Principal, and attached to the log entry; the response submission date is recorded
- Financial audit must be completed and filed with the Income Tax department (Form 10B for charitable trusts) by 30 September each year; missing this deadline risks the 12A tax exemption being suspended; EduForge creates a calendar reminder on 1 April each year
- CBSE inspection preparation does not start 2 weeks before the inspection — it is a continuous 5-year process; EduForge's compliance dashboard provides a year-round inspection readiness score; any score below 80% triggers a Principal review
- An inspector should never be denied access to a facility or document unless the document is legally privileged (e.g., lawyer-client correspondence); obstruction of an official inspection is itself a serious offence
- Inspection findings that are unresolved for >90 days generate an automatic alert to the Principal that the compliance issue is escalating; the Compliance Officer is expected to provide a weekly update on open inspection findings

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division K*
