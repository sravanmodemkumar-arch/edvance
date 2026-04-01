# E-13 — CBSE Attendance Register

> **URL:** `/school/attendance/cbse-register/`
> **File:** `e-13-cbse-attendance-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Class Teacher (S3) — own class · Administrative Officer (S3) — all classes · Academic Coordinator (S4) — full · Principal (S6) — full

---

## 1. Purpose

Generates the official CBSE-format printed attendance register — the physical record that must be maintained by every CBSE-affiliated school and produced during board inspections. This is distinct from the digital attendance module: the CBSE register is the legal document; digital records feed into it.

Required because:
- **CBSE Affiliation Bye-Laws Rule 8.6:** Every school must maintain a register showing monthly attendance for each student in the prescribed format; registers are inspected during affiliation renewal
- **Board Exam verification:** During Class X/XII LOC verification, CBSE may ask for physical attendance registers for spot-checking
- **Audit trail:** The register, once printed and signed, becomes the school's legal record; digital corrections after signing are tracked separately
- **Annual inspection by CBSE Regional Office:** Inspectors check whether the register is maintained class-wise, month-wise, with signatures

---

## 2. Page Layout

### 2.1 Header
```
CBSE Attendance Register Generator                [Generate Register]  [Export All Classes]
Academic Year: [2026–27 ▼]   Class: [XI-A ▼]   Month: [March 2026 ▼]
```

### 2.2 Register Preview Panel

```
┌────────────────────────────────────────────────────────────────────────┐
│  ATTENDANCE REGISTER — Preview                                          │
│                                                                         │
│  Class: XI-A          Month: March 2026         Academic Year: 2026–27  │
│  Class Teacher: Ms. Anita Reddy     Subject: —                         │
│                                                                         │
│  [Showing 3 of 45 students — full preview available on PDF generation]  │
│                                                                         │
│  Roll  Name                  03  04  05  06  07  10  11  ... Total  %  │
│   01   Anjali Das             P   P   P   P   A   P   P       26/28  93%│
│   02   Arjun Sharma           P   A   P   P   P   P   P       24/28  86%│
│   03   Chandana Rao           A   A   P   A   P   P   A       19/28  68%│
│                                                                         │
│  Working Days This Month: 28       Sundays/Holidays: 3                  │
│  Teacher Signature: _______________  Date: _______________             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Register Formats

### 3.1 Class-wise Monthly Register (Standard CBSE Format)

Each class gets one register page per month:

```
ATTENDANCE REGISTER
[School Name]                                    Affiliation No.: AP2000123
Class: XI Section: A              Academic Year: 2026–27
Month: March 2026                 Class Teacher: Ms. Anita Reddy

Working days in month: 28 (excluding 3 Sundays and 0 holidays)

─────────────────────────────────────────────────────────────────────────────
Roll  Student Name            │ 3  4  5  6  7 10 11 12 13 14 17 18 19 20 21 │ Tot  %
                              │ Mo Tu We Th Fr Mo Tu We Th Fr Mo Tu We Th Fr │
─────────────────────────────────────────────────────────────────────────────
 01   Anjali Das              │ P  P  P  P  A  P  P  P  P  P  P  P  P  P  P │ 26  92.9
 02   Arjun Sharma            │ P  A  P  P  P  P  P  A  P  P  P  P  P  P  P │ 24  85.7
 03   Chandana Rao            │ A  A  P  A  P  P  A  A  P  P  A  P  P  A  P │ 19  67.9
 ...  (all 45 students)      │ ...                                           │
─────────────────────────────────────────────────────────────────────────────
TOTAL PRESENT (daily count): │28 26 27 23 25 27 28 26 28 28 26 27 28 24 25 │
─────────────────────────────────────────────────────────────────────────────

Remarks:
  15 Mar 2026 — National Holiday (not counted as working day)
  22 Mar 2026 — Saturday (optional session, counted if held)

Class Teacher Signature: ___________________   Date: _____________
Principal Signature: _______________________   Stamp: [SEAL]
```

### 3.2 Annual Cumulative Register

Year-end single-page summary per student (for CBSE LOC):

```
Annual Attendance Summary — Class XI-A — Academic Year 2026–27

Roll  Name              Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec  Jan  Feb  Mar  Total  %
 01   Anjali Das        25   20   22   24   21   20   23   22   20   24   19   26   246/260  94.6%
 02   Arjun Sharma      24   19   21   23   20   19   20   21   18   22   17   24   228/260  87.7%
 ...
```

---

## 4. Generate Register Workflow

```
[Generate Register] → options drawer:

Register Type:
  ● Monthly (single class, single month)     ← most common
  ○ Annual Cumulative (class, full year)
  ○ All Classes — Monthly (all classes, one month)  ← bulk print for inspection
  ○ Annual — All Classes (full school year-end)

Class: [Select class ▼] (or "All Classes")
Month/Year: [March 2026]

Options:
  ☑ Include daily totals row
  ☑ Include teacher signature line
  ☑ Include Principal countersignature line
  ☑ Include school seal placeholder
  ☑ Highlight absent cells (shaded)
  ☐ Print remarks column (extra space for notes)

Paper Size: ● A4 Landscape  ○ A3 (wider, fits full month without wrapping)
Font Size: [9pt ▼]

[Preview]  [Generate PDF]  [Generate XLSX (for manual filling)]
```

---

## 5. CBSE Register Reconciliation Check

Before generating, the system runs a consistency check:

```
Consistency Check — XI-A — March 2026

✅ E-01 daily attendance submitted: 28/28 working days
✅ No pending correction requests (E-03)
✅ Matches E-07 class report totals
⚠️  3 leave applications (E-04) pending approval — these are shown as Absent in register
    → [View Pending Leaves]  [Proceed Anyway]  [Resolve First]
✅ All on-duty absences (E-04) correctly excluded from denominator
```

**If inconsistencies exist:**
- Warning shown; user can proceed or fix first
- Register PDF carries a watermark "PRELIMINARY — Pending [N] records" if generated with inconsistencies
- Finalised register (no warnings) carries no watermark

---

## 6. Signing & Finalisation Workflow

```
Register Finalisation — XI-A — March 2026

Step 1: Class Teacher Review
  Ms. Anita Reddy — review and sign digitally
  [Review Register] → [Confirm Correct]
  Status: ✅ Reviewed on 27 Mar 2026 at 4:45 PM

Step 2: Principal Countersignature
  Principal: [Name]
  [Countersign] → Principal approval
  Status: ⬜ Pending

Once both signatures are recorded:
  → Register is locked (no further corrections without Academic Coordinator approval)
  → PDF carries "FINALISED" status
  → Physical printout generated for filing in school records
```

---

## 7. Correction After Finalisation

If a correction is needed after the register is finalised:

```
Post-Finalisation Correction Request — XI-A — March 2026

Student: Arjun Sharma (Roll 02)
Date: 12 March 2026
Current: Absent
Proposed: Present (Medical leave — approved on 14 Mar)

Reason: Leave approved after register was signed

Requires:
  → Academic Coordinator approval (E-03 correction)
  → New register reprint with corrigendum note
  → Corrigendum: "Correction to attendance: Arjun Sharma (Roll 02), 12 Mar 2026,
    changed from Absent to Present (Medical Leave, ML/2026/142). Approved by:
    [Coord Name], [Principal Name]"

[Submit Correction Request]
```

---

## 8. Subject-wise Register (for Period Attendance — CBSE Class XI–XII)

For Classes XI and XII, CBSE also requires subject-wise attendance registers maintained by subject teachers:

```
Subject Attendance Register — Physics (Class XI-A)
Teacher: Mr. Arun Kumar   Periods per week: 6

         Period #  →  1   2   3   4   5   ...  Total  % (of subject periods)
Roll  Name
 01   Anjali Das          P   P   P   P   P  ...   72/86   83.7%
 02   Arjun Sharma        P   A   P   P   P  ...   70/84   83.3%
...

Working periods this month: 24  (6 per week × 4 weeks; 2 cancelled for exam duty)
```

Subject-wise register is separate from the class-wise monthly register, fed from E-02 period attendance.

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/cbse-register/?class={class_id}&month={m}&year={y}` | Monthly register data |
| 2 | `GET` | `/api/v1/school/{id}/attendance/cbse-register/annual/?class={class_id}&year={y}` | Annual cumulative register |
| 3 | `GET` | `/api/v1/school/{id}/attendance/cbse-register/all-classes/?month={m}&year={y}` | All classes bulk register |
| 4 | `GET` | `/api/v1/school/{id}/attendance/cbse-register/subject/?subject_id={id}&month={m}` | Subject-wise register |
| 5 | `GET` | `/api/v1/school/{id}/attendance/cbse-register/consistency-check/?class={id}&month={m}&year={y}` | Pre-generation check |
| 6 | `POST` | `/api/v1/school/{id}/attendance/cbse-register/finalise/` | Mark register as finalised (CT + Principal) |
| 7 | `GET` | `/api/v1/school/{id}/attendance/cbse-register/pdf/?class={id}&month={m}&year={y}&format={landscape|a3}` | PDF generation |

---

## 10. Business Rules

- The CBSE register PDF format matches CBSE's prescribed format (Attendance Register format per CBSE Affiliation Bye-Laws Appendix 8); any change to CBSE format by notification must be updated in this module
- Finalsied registers are immutable; corrections require Academic Coordinator approval and generate a corrigendum attached to the original register PDF
- Schools must retain printed/digital registers for 5 years after the academic year (Class X/XII records: indefinitely for board exam verification)
- The register PDF carries the school's affiliation number on every page — this is checked during CBSE inspection
- Subject-wise registers (E-02 feed) are mandatory for Classes IX–XII; not required for primary classes
- Register data must match E-07 class report exactly — any discrepancy is flagged as an audit risk

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
