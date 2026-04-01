# F-07 — PTM Outcome Register

> **URL:** `/school/ptm/outcomes/`
> **File:** `f-07-ptm-outcome-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Academic Coordinator (S4) — compile and review · Principal (S6) — sign off register · Class Teacher (S3) — view own class outcomes · Administrative Officer (S3) — export

---

## 1. Purpose

Post-PTM register consolidating all meeting outcomes, follow-up actions, and attendance statistics. This is the "after-action report" of the PTM event. Used for:
- **CBSE inspection evidence:** Demonstrates that the school held PTMs and maintained records
- **Follow-up tracking:** Ensures actions committed during PTM are actually completed
- **Academic Coordinator planning:** Identifies patterns (classes with high parent non-attendance, recurring concerns)
- **Annual report input:** School annual report cites PTM statistics (parent engagement rate)

---

## 2. Page Layout

### 2.1 Header
```
PTM Outcome Register                                [Generate PTM Report]  [Export]
PTM: [Annual PTM — 9 Mar 2026 ▼]

PTM Summary:
  Classes covered: 14 (Nursery to Class XII)
  Total slots: 380  ·  Parents who attended: 312 (82.1%)  ·  Absent: 68 (17.9%)
  Average meeting duration: 12.3 minutes (vs 15 min allotted)
  Follow-up actions generated: 34
  Welfare flags raised: 2  ·  POCSO flags: 0
```

### 2.2 Class-wise Summary
```
Class       Teacher         Attended  Absent  Avg Duration  Concerns Raised
Nursery-A   Ms. Kavya          22/24   2/24    9.2 min      0
Class I-A   Ms. Radha          20/22   2/22    10.1 min     1 (welfare)
Class VI-A  Mr. Kishore        28/32   4/32    11.5 min     2 (academic)
Class IX-A  Mr. Ravi           28/34   6/34    13.2 min     3 (attendance)
Class XI-A  Ms. Anita          40/45   5/45    12.8 min     2 (attendance/academic)
Class XII-A Ms. Lakshmi        32/35   3/35    14.6 min     4 (exam prep)

[View class details]
```

### 2.3 Follow-Up Action Tracker
```
Open Follow-Up Actions — Annual PTM (9 Mar 2026)

# | Student        | Class  | Action                              | Assigned To      | Due         | Status
1 | Chandana Rao   | XI-A   | Submit medical certificates         | Parent           | 15 Mar 26   | ⬜ Pending
2 | Chandana Rao   | XI-A   | File CBSE condonation application   | Acad. Coord      | 20 Mar 26   | ⬜ Pending
3 | Vijay S.       | X-B    | Parent to meet Principal            | Parent           | 16 Mar 26   | ⬜ Pending
4 | Transport Route 4 issue | — | Transport HOD to investigate    | HOD (Transport)  | 15 Mar 26   | ✅ Done
5 | Canteen audit  | —      | Hygiene audit to be conducted       | Admin Officer    | 20 Mar 26   | ⬜ Pending
...

[Mark Complete]  [Send Reminder]  [View All]
```

---

## 3. Parent Non-Attendance Analysis

```
Parents who did not attend — Annual PTM (9 Mar 2026)

68 parents absent. Of these:
  Pre-notified absent (booked then cancelled): 12  (18%)
  No-show (booked, didn't come): 24  (35%)
  Never booked: 32  (47%)

Concern level of non-attending students:
  🔴 High concern (attendance <75% OR academic risk): 8 students
  🟡 Medium concern (attendance 75-85%): 18 students
  ✅ Low concern (no significant issues): 42 students

Action for high-concern non-attenders:
  [Send individual follow-up WhatsApp with key teacher notes]
  [Schedule phone call with class teacher]
  [Note in F-13 communication log as "PTM not attended"]

Follow-up WhatsApp sent: ✅ 8 high-concern parents (27 Mar 2026, auto-drafted by F-06)
```

---

## 4. PTM Register (CBSE Format)

```
[Generate PTM Report] → PDF:

PARENT-TEACHER MEETING REGISTER
[School Name]  ·  Affiliation: AP2000123
Academic Year: 2026–27

PTM Held On: 9 March 2026 (Sunday)
Conducted For: Classes Nursery to XII
Venue: School Premises

┌─────────────────────────────────────────────────────────────────────────┐
│ Class  Teacher              Students  Parents  %   Report Cards Distrib.│
│ XI-A   Ms. Anita Reddy        45       40     89%  ✅ 40/45 distributed │
│ XI-B   Mr. Ravi Kumar         42       38     90%  ✅ 38/42 distributed │
│ ...                                                                      │
│ TOTAL                        380      312     82%                        │
└─────────────────────────────────────────────────────────────────────────┘

General Session:
  Conducted by: Dr. N. Subramanian (Principal)
  Topics: Exam schedule, vacation dates, fee structure, school achievements
  Parent participation in Q&A: ✅ 45 parents participated

Signature: [Principal] [Academic Coordinator]  Date: 27 Mar 2026  Seal: [SCHOOL SEAL]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/ptm/{ptm_id}/outcomes/` | PTM outcome summary |
| 2 | `GET` | `/api/v1/school/{id}/ptm/{ptm_id}/outcomes/class/{class_id}/` | Class-wise outcomes |
| 3 | `GET` | `/api/v1/school/{id}/ptm/{ptm_id}/outcomes/follow-ups/` | Follow-up action list |
| 4 | `PATCH` | `/api/v1/school/{id}/ptm/{ptm_id}/outcomes/follow-ups/{action_id}/` | Update follow-up status |
| 5 | `GET` | `/api/v1/school/{id}/ptm/{ptm_id}/outcomes/non-attendees/` | Non-attending parent list |
| 6 | `GET` | `/api/v1/school/{id}/ptm/{ptm_id}/outcomes/report-pdf/` | CBSE-format PTM register PDF |

---

## 6. Business Rules

- The PTM register PDF is signed digitally (or printed and signed) by the Principal within 7 days of the PTM; this is the formal record
- Follow-up actions assigned to parents are tracked; if no update within the due date, the system alerts the Class Teacher to follow up
- PTM attendance percentage is included in school's annual self-evaluation report (CBSE self-study report for affiliation renewal)
- The outcomes register is read-only once the Principal signs it; amendments require Principal approval and are logged as addenda
- Welfare concern flags from F-06 appear in the outcomes register and must be resolved (or escalated to J-01 counsellor) before the register is signed

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
