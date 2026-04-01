# B-35 — Practical Exam Coordinator

> **URL:** `/school/academic/exams/practicals/`
> **File:** `b-35-practical-exam-coordinator.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Cell Head (S4) — full · HOD (S4) — read/coordinate own dept · Subject Teacher (S3) — examiner duties · Principal (S6) — full

---

## 1. Purpose

Coordinates all practical examinations — both internal (conducted throughout the year by school teachers as part of IA) and board-level (CBSE class X/XII practicals with CBSE-appointed external examiners). Board practical exams are high-stakes: the date is assigned by CBSE, an external examiner comes from outside the school, students are examined in batches, marks are submitted directly to CBSE. The school must arrange lab setup, examiner hospitality, student batching, and CBSE portal marks submission in a compressed 1–2 day window. This page manages the operational coordination of all these events.

---

## 2. Page Layout

### 2.1 Header
```
Practical Exam Coordinator                        [+ Schedule Internal Practical]  [Log External Examiner]
Academic Year: 2025–26
Board Practicals: 4 remaining  ·  Internal Practicals: 12 scheduled  ·  Completed: 8
Upcoming: Physics XII — 10 Apr 2026 (15 days away)
```

---

## 3. Practical Schedule Overview

| Practical | Subject | Class | Type | Date | Students | Internal Teacher | External Examiner | Status |
|---|---|---|---|---|---|---|---|---|
| Physics Practical | XII | MPC | Board (CBSE) | 10 Apr 2026 | 38 | Ms. Lakshmi Devi | CBSE-appointed (TBD) | ⏳ Upcoming |
| Chemistry Practical | XII | MPC | Board (CBSE) | 11 Apr 2026 | 38 | Mr. Ravi Kumar | CBSE-appointed (TBD) | ⏳ Upcoming |
| Biology Practical | XII | BiPC | Board (CBSE) | 12 Apr 2026 | 22 | Ms. Anjali Singh | CBSE-appointed (TBD) | ⏳ Upcoming |
| CS Practical | XII | MPC | Board (CBSE) | 14 Apr 2026 | 20 | Mr. Dinesh | CBSE-appointed (TBD) | ⏳ Upcoming |
| Physics Lab IA | XI | A, B | Internal | 5 Mar 2026 | 80 | Ms. Lakshmi | — (internal) | ✅ Complete |
| Chemistry Lab IA | XI | A, B | Internal | 7 Mar 2026 | 80 | Mr. Ravi | — | ✅ Complete |
| Bio Lab IA | IX | A, B | Internal | 15 Mar 2026 | 84 | Ms. Anjali | — | ✅ Complete |

---

## 4. Board Practical — Detail View

Click any Board practical row:

### Physics Practical — Class XII MPC — 10 Apr 2026

#### 4.1 CBSE-Assigned Details (from CBSE notification)
```
External Examiner:   Dr. Kishore Reddy (assigned by CBSE Delhi)
Examiner Contact:    9876543210 (CBSE-provided)
School centre code:  AP-1234
Date:                10 Apr 2026
Reporting time:      9:00 AM (examiner)
Exam start:          10:00 AM
```

[Log External Examiner Details] → enter examiner name/contact from CBSE notification letter.

#### 4.2 Student Batching

38 students, lab capacity 15 → 3 batches:

| Batch | Students | Timing |
|---|---|---|
| Batch 1 | 13 students (Roll 001–013) | 10:00 AM – 12:00 PM |
| Batch 2 | 13 students (Roll 014–026) | 12:00 PM – 02:00 PM |
| Batch 3 | 12 students (Roll 027–038) | 02:00 PM – 04:00 PM |

[Auto-Batch] → system assigns batches by roll number with even distribution.

#### 4.3 Lab Preparation Checklist

| Item | Responsibility | Status |
|---|---|---|
| Physics Lab cleaned and prepared | Lab Attendant | ✅ Done (9 Apr) |
| Apparatus per experiment laid out (15 stations) | Ms. Lakshmi | ⬜ Pending (10 Apr AM) |
| Experiment list received from CBSE (standard 15) | Exam Cell | ✅ Printed |
| Viva questions prepared (internal teacher) | Ms. Lakshmi | ✅ Done |
| Record/file books arranged (all students) | Class Teacher | ✅ Done |
| Practical mark sheets (CBSE format) printed | Exam Cell | ⬜ Print 10 Apr |
| Refreshments for examiner | Admin Officer | ⬜ Arrange |
| Examiner TA/DA claim form | Exam Cell | ⬜ Keep ready |

#### 4.4 Marks Entry (Practical Day)

On the day, as batches complete:

```
Marks Entry: Physics Practical — Batch 1 (13 students)
External Examiner: Dr. Kishore Reddy

Roll  Student         File/Record(5) Experiment(10) Viva(5) Total(30)*
001   Arjun Sharma    4              8              4       28
002   Priya V         5              9              5       30
003   Rahul G         3              7              3       24
...
```

*CBSE format: Theory marks (70) + Practical marks (30) = 100 total for Class XII Physics.

Internal teacher and External examiner both enter marks independently. System shows discrepancy if > 5 marks difference on any component (requires discussion and re-award).

#### 4.5 CBSE Marks Submission

After completion:
1. Export marks in CBSE-prescribed format (Excel/XML for CBSE portal)
2. Exam Cell Head logs into CBSE Saras and uploads
3. Log submission in EduForge:

```
Practical Marks Submission Log:
  Subject: Physics  ·  Class: XII-MPC
  Submitted by: Mr. Rajan Kumar (Exam Cell Head)
  Date: 10 Apr 2026, 5:44 PM
  CBSE Portal Reference: CBSE/PRAC/2026/AP1234/002
  Students submitted: 38
  Status: ✅ Accepted
```

---

## 5. Internal Practical (IA Lab) — Detail View

For internal lab practicals (throughout the year, marked by school teacher as IA component):

### Chemistry Lab IA — Class XI-A and XI-B — 7 Mar 2026

- **No external examiner** — school teacher (Mr. Ravi Kumar) examines
- **Format:** Student performs one experiment from CBSE list; teacher marks on file/record (5m), performance (10m), viva (5m) = 20m
- Marks feed directly into B-31 (Internal Assessment)

Marks entry identical to board practical but without external examiner column.

---

## 6. External Examiner Hospitality Log

CBSE regulations require examiners to be treated respectfully. Practical exam school's responsibility:
- TA/DA reimbursement to examiner (CBSE rate)
- Lunch/refreshments
- Welcome letter from Principal

| Examiner | Practical | Date | TA Amount | Paid By | Receipt No | Notes |
|---|---|---|---|---|---|---|
| Dr. Kishore Reddy | Physics XII | 10 Apr | ₹1,500 | School | RCP-042 | From petty cash |
| Dr. Meena Rao | Chemistry XII | 11 Apr | ₹1,500 | School | RCP-043 | From petty cash |

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/practicals/?year={year}` | Practical schedule list |
| 2 | `POST` | `/api/v1/school/{id}/practicals/` | Schedule new practical |
| 3 | `GET` | `/api/v1/school/{id}/practicals/{practical_id}/` | Practical detail |
| 4 | `PATCH` | `/api/v1/school/{id}/practicals/{practical_id}/` | Update practical details |
| 5 | `POST` | `/api/v1/school/{id}/practicals/{practical_id}/batches/` | Generate/update batching |
| 6 | `PATCH` | `/api/v1/school/{id}/practicals/{practical_id}/marks/` | Enter practical marks |
| 7 | `POST` | `/api/v1/school/{id}/practicals/{practical_id}/submit-cbse/` | Log CBSE submission |
| 8 | `GET` | `/api/v1/school/{id}/practicals/{practical_id}/export-cbse/` | Export CBSE marks format |

---

## 8. Business Rules

- Board practical marks (once submitted to CBSE) cannot be edited in EduForge — they are controlled by CBSE from that point
- Internal practical marks (IA) remain editable until IA lock (B-31) is triggered
- Discrepancy > 5 marks between internal and external examiner on any component must be resolved before marks are submitted to CBSE — the system flags it and prompts discussion
- CBSE external examiner's marks take precedence in case of unresolved discrepancy (CBSE norm)
- Examiner hospitality expenses are logged and reconcile with petty cash (A-25 Procurement/Finance)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
