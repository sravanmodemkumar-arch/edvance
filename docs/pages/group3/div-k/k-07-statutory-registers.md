# K-07 — Statutory Registers Tracker

> **URL:** `/school/compliance/registers/`
> **File:** `k-07-statutory-registers.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Compliance Officer (S4) — track completeness · Administrative Officer (S3) — maintain registers · Principal (S6) — sign off registers as required

---

## 1. Purpose

Tracks the completeness and currency of all statutory registers that schools are required to maintain. CBSE and state education departments prescribe specific registers; inspectors check these during visits. An incomplete or missing register at inspection time creates adverse reports.

This is a meta-tracker — it doesn't replace the actual registers (which are in their respective modules), but tracks whether each required register exists, is current, and is Principal-signed.

---

## 2. Register Tracker Dashboard

```
Statutory Registers — Completeness Status             [Mark All Reviewed]
Academic Year: [2026–27 ▼]  Last review: 27 March 2026

Status summary:
  Complete and current: 28/32 ✅
  Needs update: 3 ⚠️
  Not started: 1 ⛔
  Not applicable to this school: 0

⚠️ Issues:
  Anti-Ragging affidavit register: 4 parent affidavits pending (K-07 view → J-03)
  Lab safety register: Not updated since January (K-04 → update)
  PTM register: Term 2 PTM minutes not yet entered (F-07)
⛔ Visiting teacher register: No register maintained (new CBSE requirement 2024)
   [Set up register — assign to Administrative Officer]
```

---

## 3. Register List

```
CBSE-Required Registers:

Register Name                    Location (Module)   Last Updated    Status      Principal Sign
Admission Register               C-01                Current ✅      ✅ Done     Termly
Attendance Register (students)   E-13 CBSE format    Current ✅      ✅ Done     Monthly
Attendance Register (staff)      L-02                Current ✅      ✅ Done     Monthly
Transfer Certificate Register    C-12                Current ✅      ✅ Done     As issued
Migration Certificate Register   C-12                Current ✅      ✅ Done     As issued
Fee Register                     D-04                Current ✅      ✅ Done     Termly
Progress Report Register         B-11                Current ✅      ✅ Done     Termly
Scholarship Register             J-09                Current ✅      ✅ Done     Annual
Stock/Property Register          Admin               Current ✅      ✅ Done     Annual
Library Accession Register       G-01                Current ✅      ✅ Done     Annual
Medical/Health Register          J-06                Current ✅      ✅ Done     Termly
Transport Safety Register        I-12                Current ✅      ✅ Done     Termly
Visitors Book                    Admin/Physical       Current ✅      ✅ Done     Daily (receptionist)
Anti-Ragging Register            J-03                Current ✅      ✅ Done     As required
Anti-Ragging Affidavits          J-03                ⚠️ 4 pending    ⚠️          —
POCSO Register                   J-02                Current ✅      ✅ Done     Restricted
Complaint/Grievance Register     J-05 + F-14         Current ✅      ✅ Done     Monthly
Staff Service Books              K-05/L module       Current ✅      ✅ Done     Annual
Lab Safety Register              K-04                ⚠️ Jan 2026     ⚠️ Update   —
PTM Register                     F-07                ⚠️ Term 2 missing ⚠️        —
Visiting Teacher Register        K-07                ⛔ Not created   ⛔          —
CBSE LOC (List of Candidates)    B-19                Current ✅      ✅ Done     Annual
Fire Drill Register              K-03                Current ✅      ✅ Done     Per drill

State-Required Registers (Telangana):
General Register (admission format) C-01             Current ✅      ✅ Done     Annual
TS School Recognition Register   K-06                Current ✅      ✅ Done     Annual
Service Books (all staff)         L module            Current ✅      ✅ Done     Annual
```

---

## 4. Register Maintenance Standards

```
Register Maintenance Standards — CBSE Inspection Ready

What inspectors look for:
  1. No blank entries — every field must be filled or marked N/A
  2. Corrections: Use single-line strikethrough; no correction fluid (Whitener)
  3. Sequential entries — no gaps in serial numbers
  4. Authorized signatures — registers must be signed by designated authority
  5. No back-dating — entries must be made contemporaneously

Common inspection findings at Indian schools:
  ✗ "Attendance register filled in advance in bulk for the week" (impermissible)
  ✗ "TC register: 3 serial numbers skipped without explanation"
  ✗ "Admission register: column for parent occupation left blank for 15 students"
  ✗ "Fee register: corrections made with whitener" (suspicious)
  ✗ "POCSO register: not constituted" (serious violation)

EduForge enforcement:
  ● Prevents back-dating in all digital registers (server timestamp)
  ● Prevents deletion of entries (only superseding/correcting with original visible)
  ● Audit trails for every entry
  ● Principal sign-off reminders for monthly/termly registers
```

---

## 5. Principal Sign-Off Tracking

```
Principal Monthly Register Sign-Off — March 2026

Registers requiring monthly Principal sign-off:
  ● Attendance Register (Students): ☑ Signed — 31 Mar 2026
  ● Attendance Register (Staff): ⬜ Pending — due 31 Mar 2026
  ● Sick Room Register: ⬜ Pending
  ● Complaint Register: ⬜ Pending

Registers requiring termly sign-off (Term 2 ended Feb 2026):
  ● Fee Register Term 2: ✅ Signed 28 Feb 2026
  ● Progress Reports Term 2: ✅ Signed 10 Mar 2026
  ● Transport Safety Register Term 2: ✅ Signed 28 Feb 2026

Pending sign-offs:
  3 registers need Principal signature by 31 March 2026
  [Send reminder to Principal]

Note: Digital sign-off = Principal's OTP-verified approval in EduForge system
  + physical signature on printed register (for registers maintained physically)
```

---

## 6. Visiting Teacher Register (New — CBSE 2024)

```
Visiting Teacher Register — Setup Required

CBSE Circular 2024 requires schools to maintain a register of visiting/guest teachers,
part-time teachers, and resource persons who interact with students.

Fields required:
  - Name
  - Qualification
  - Subject taught / activity conducted
  - Date(s) of visit
  - School's principal certification of BGV status before first visit
  - Parent of students informed: Yes/No (for recurring visiting teachers)

Setup this register: [Create Register]

Note: Even a one-time visiting expert (e.g., a professional for Career Day) must be
  logged here. POCSO concerns: any adult interacting with students must be on record.
  The school is responsible for ensuring visiting persons are known and accountable.
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/compliance/registers/` | Register tracker list |
| 2 | `PATCH` | `/api/v1/school/{id}/compliance/registers/{reg_id}/status/` | Update register status |
| 3 | `POST` | `/api/v1/school/{id}/compliance/registers/{reg_id}/signoff/` | Log Principal sign-off |
| 4 | `GET` | `/api/v1/school/{id}/compliance/registers/pending-signoffs/` | Pending sign-offs |
| 5 | `GET` | `/api/v1/school/{id}/compliance/registers/inspection-readiness/` | Overall readiness report |

---

## 8. Business Rules

- Every register required by CBSE Affiliation Bye-Laws must exist; registers that are "not applicable" must be explicitly marked as such with a reason (e.g., "Hostel register — school has no hostel")
- Physical registers that are prescribed in a specific CBSE/state format cannot be replaced by digital-only records without express CBSE approval; EduForge maintains both digital (for working records) and generates physical register export for print
- Principal sign-off on registers is a CBSE requirement; EduForge sends auto-reminders on the first of every month for monthly-sign registers and on the last day of each term for termly registers
- Correction fluid (Whitener/Tipp-Ex) is prohibited in all school registers; the correction must be visible (strikethrough with initialling); this is a standard for legal records — concealment of a correction implies intent to deceive
- Missing registers at inspection: the inspector notes the gap; if it is a mandatory register, the inspection report is adverse; repeated adverse findings can lead to probationary affiliation
- Visiting teacher register: any person who regularly teaches students (more than 3 times) must be formally appointed, not just logged as a visitor; appointment triggers BGV requirement; the register distinguishes one-time resource persons from regular visiting teachers

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division K*
