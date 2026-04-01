# C-17 — UDISE+ Data Manager

> **URL:** `/school/compliance/udise/`
> **File:** `c-17-udise-data-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Data Entry Operator (S2) — data entry · Administrative Officer (S3) — full · Academic Coordinator (S4) — full · Principal (S6) — sign + submit

---

## 1. Purpose

Manages the annual UDISE+ (Unified District Information System for Education Plus) data submission — the Government of India's comprehensive school census. Every school in India (public and private) must submit UDISE+ data by September each year for the previous academic year. The data covers:
- Student enrolment counts (by class, gender, category, RTE status)
- Teacher counts and qualifications
- Infrastructure (rooms, toilets, labs, library, computers, drinking water, electricity)
- Academic results (pass rates, dropout rates)
- Special programs (MDM, scholarship counts, CWSN students)

**Why UDISE matters:**
- **Government-aided schools:** Grant amount directly computed from UDISE student count; under-reporting = less grant; over-reporting = fraud investigation
- **All schools:** CBSE affiliation renewal checks UDISE registration; schools without UDISE code face de-affiliation proceedings
- **State DISE reports:** Used by Planning Commission, World Bank, NEP implementation tracking
- **Ranking / grading:** CBSE school quality index includes UDISE compliance as a parameter

UDISE code (11-digit) is the school's permanent government identity — required on every official document including board exam registration (B-33).

---

## 2. Page Layout

### 2.1 Header
```
UDISE+ Data Manager                           [Start 2025–26 Data Entry]  [Validate]  [Export XML]
UDISE Code: 28030600101  ·  School: [School Name]
Submission Year: 2025–26  ·  Due: 30 September 2026
Status: ⚠️ In Progress (68% complete)  ·  Last Saved: 26 Mar 2026
```

### 2.2 Section Completion Progress
```
Sections:
  ✅ School Profile & Location         (Section 1)   100%
  ✅ Academic & Administrative Info    (Section 2)   100%
  🔄 Student Enrolment                (Section 3)    85%  ← Auto from EduForge records
  ✅ Teacher & Staff                  (Section 4)   100%
  ⬜ Infrastructure                   (Section 5)     0%  ← Manual entry required
  ⬜ School Development Index          (Section 6)     0%
  ⬜ Special Categories               (Section 7)     0%  ← Partially auto from C-07, C-19
  ⬜ Annual Exam Results               (Section 8)     0%  ← Auto from B-18 once approved
  ─────────────────────────────────────────────────────────
  Overall: 68%
```

---

## 3. Section 1 — School Profile

| Field | Value | Source |
|---|---|---|
| UDISE Code | 28030600101 | From school settings (A-06) |
| School Name | [School Name] | From A-06 |
| District | Hyderabad | |
| Block | Balanagar | |
| Village/Ward | Kukatpally | |
| Pincode | 500072 | |
| School Type | Private Unaided | |
| Management | Private Unaided Management | |
| School Category | Primary with Upper Primary, Secondary & Sr Secondary | |
| Affiliation Board | CBSE | |
| Affiliation No. | AP2000123 | |
| Medium of Instruction | English | |
| Year of Establishment | 2005 | |
| School Has Transport | Yes | |
| School Has Hostel | No | |

---

## 4. Section 3 — Student Enrolment (Auto-populated)

Auto-computed from EduForge enrollment records (C-05, C-08):

```
Student Enrolment — 2025–26 (as of 31 March 2026)

Class  Boys  Girls  Total  SC  ST  OBC  General  EWS/RTE
Nur     22    18     40    4   1    12     23      10
LKG     20    18     38    3   0    11     24       9
UKG     21    19     40    4   1    12     23       9
I       22    19     41    4   0    12     25      10
...
X       18    18     36    2   0    10     24       0
XI      38    38     76    6   1    22     47       0
XII     18    16     34    3   0    10     21       0
─────────────────────────────────────────────────────
TOTAL  186   194    380   32   4   110    234      38

Dropout Count (2025–26): 3 (from C-12 withdrawal register)
CWSN Students: 5 (from C-19)
RTE Students (enrolled under 25% quota): 38
```

[Re-sync from EduForge Records] → recomputes from current enrollment data.

---

## 5. Section 4 — Teacher & Staff (Partial Auto)

| Category | Count | Source |
|---|---|---|
| Total Teachers (Regular) | 28 | From staff module (div-l) |
| Total Teachers (Contract) | 4 | |
| Female Teachers | 22 | |
| Male Teachers | 10 | |
| Teachers with B.Ed. | 28 | |
| Teachers with M.Ed. | 4 | |
| TGT (Trained Graduate Teacher) | 18 | |
| PGT (Post-Graduate Teacher) | 12 | |
| PRT (Primary Teacher) | 8 | |
| Non-Teaching Staff | 12 | |
| Total Staff | 44 | |

---

## 6. Section 5 — Infrastructure (Manual Entry)

Must be entered manually (not derivable from other EduForge modules):

| Parameter | Value | Unit |
|---|---|---|
| Total Class Rooms | 22 | Rooms |
| Class Rooms in Good Condition | 22 | |
| Other Rooms | 8 | |
| Boys Toilets | 6 | |
| Girls Toilets | 6 | |
| Staff Toilets | 4 | |
| Has Ramp for Disabled | Yes | |
| Has Library | Yes | |
| Library Books | 2,842 | |
| Computers (Students) | 42 | |
| Internet Connection | Yes — Broadband | |
| Science Lab | Yes | |
| Math Lab | Yes | |
| Computer Lab | Yes | |
| Playground | Yes | |
| Has CCTV | Yes | |
| Drinking Water | Tap water + Purifier | |
| Electricity | Yes — Regular + Backup | |
| Kitchen (MDM) | No (private school) | |

---

## 7. Section 8 — Annual Exam Results (Auto-populated)

From B-18 Result Computation:

```
Annual Exam Results — 2024–25

Class  Enrolled  Appeared  Passed  Pass %  Dropout
VIII       42       42       40      95%      0
IX         38       38       34      89%      0
X (Board)  36       36       36     100%      0
XI         76       76       70      92%      0
XII (Board)34       34       32      94%      0
```

---

## 8. Validation

[Validate] → runs UDISE portal's own validation rules:

```
Validation Results:

✅ UDISE Code: valid and matches district records
✅ Enrolment totals: sum checks pass
⚠️ Class X boys enrolment 2025–26 (18) vs 2024–25 (22) — decrease > 10%: add remarks
⚠️ Infrastructure: Computer count (42) vs Computer Lab (Yes) — confirm
✅ Teacher qualification: all teachers have minimum qualification
```

Issues must be resolved (or remarks added) before export.

---

## 9. XML Export

[Export XML] → generates UDISE+ XML in the exact format required by the government portal:

```xml
<UDISE_SCHOOL_DATA>
  <SCHOOL_CODE>28030600101</SCHOOL_CODE>
  <ACADEMIC_YEAR>2025-26</ACADEMIC_YEAR>
  <SECTION_1>
    <SCHOOL_NAME>[School Name]</SCHOOL_NAME>
    ...
  </SECTION_1>
  <SECTION_3>
    <ENROLMENT_NURSERY_BOYS>22</ENROLMENT_NURSERY_BOYS>
    ...
  </SECTION_3>
</UDISE_SCHOOL_DATA>
```

This XML is uploaded to the UDISE+ portal (udiseplus.gov.in) by the school's UDISE data entry operator.

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/udise/?year={year}` | UDISE data + completion status |
| 2 | `PATCH` | `/api/v1/school/{id}/udise/{year}/section/{section_no}/` | Update a UDISE section |
| 3 | `POST` | `/api/v1/school/{id}/udise/{year}/sync/` | Re-sync auto-populated sections from EduForge records |
| 4 | `GET` | `/api/v1/school/{id}/udise/{year}/validate/` | Run validation checks |
| 5 | `GET` | `/api/v1/school/{id}/udise/{year}/export/xml/` | Export UDISE+ XML |
| 6 | `GET` | `/api/v1/school/{id}/udise/{year}/export/pdf/` | Export human-readable PDF for Principal review |

---

## 11. Business Rules

- UDISE data is per academic year; previous years' submitted data is locked (read-only after submission is confirmed)
- Principal must review and confirm before export — the [Export XML] button requires Principal role
- Auto-populated sections (enrolment, teacher counts, results) pull live data from EduForge; manual sections (infrastructure) are entered once and carry forward to the next year (with a prompt to update if anything changed)
- Schools are responsible for submitting the exported XML to the government portal (udiseplus.gov.in) — EduForge generates the XML but does not submit directly (as UDISE portal requires school-specific login and OTP)
- UDISE submission records (export timestamp, exporting officer, file hash) are stored in EduForge for audit

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
