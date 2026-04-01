# B-11 — Exam Configuration

> **URL:** `/school/academic/exams/<exam_id>/config/`
> **File:** `b-11-exam-configuration.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Exam Cell Head (S4) — full · HOD (S4) — submit question paper · Principal (S6) — approve

---

## 1. Purpose

Detailed configuration for a single exam — marks structure, subject-class-marks mapping, internal assessment linkage, grace marks settings, paper type, and which students are eligible. While B-10 creates the exam and sets its dates, B-11 is where the Exam Cell Head configures every parameter needed before the exam can begin: how many marks per section, which teachers enter marks, whether OMR or written, internal assessment integration, and the passing criteria. This is also where HODs submit approved question papers for the exam.

---

## 2. Page Layout

### 2.1 Header
```
Exam Configuration — Annual Exam 2025–26         [Save Changes]  [Submit for Approval]
Exam ID: EX-2026-ANN  ·  Status: ⚠️ Draft — Pending Principal Approval
Classes: VI–XI (52 sections, 2,182 students)  ·  Date: 1–20 Mar 2026
```

---

## 3. Tabs

### Tab 1 — Marks Structure

Defines the marks breakdown per subject group:

| Subject Group | Total Marks | Theory | Internal Assessment | Practical | Passing Marks | Pass Criteria |
|---|---|---|---|---|---|---|
| Sciences (IX–X) | 100 | 80 | 20 | — | 33 | Theory ≥ 27 + IA ≥ 6 |
| Sciences (XI–XII) | 100 | 70 | 30 | — | 33 | Theory ≥ 23 + IA ≥ 10 |
| Mathematics (VI–VIII) | 100 | 100 | — | — | 33 | Theory ≥ 33 |
| Mathematics (IX–X) | 100 | 80 | 20 | — | 33 | Theory ≥ 27 + IA ≥ 6 |
| Languages (all) | 100 | 80 | 20 | — | 33 | Theory ≥ 27 + IA ≥ 6 |
| Computer Science (XI–XII) | 100 | 70 | 30 | — | 33 | Theory ≥ 23 + IA ≥ 10 |
| Physical Education (XI–XII) | 100 | 30 | 40 | 30 | 33 | As per CBSE PE norms |

**Passing criteria templates:** CBSE standard auto-loaded; state board variants available; fully customisable.

---

### Tab 2 — Subject-Class-Date Schedule

| Date | Class | Subject | Time | Duration | Max Marks | Paper Type | Marks Entry By |
|---|---|---|---|---|---|---|---|
| 1 Mar | VI, VII, VIII, IX, X, XI | English | 10:00–12:20 | 140 min | 80 | Written | Subject Teacher |
| 3 Mar | VI–IX, XI MPC, XI BiPC | Mathematics | 10:00–12:20 | 140 min | 80 | Written | Subject Teacher |
| 4 Mar | VI, VII, VIII | General Science | 10:00–12:20 | 140 min | 80 | Written | Subject Teacher |
| 4 Mar | IX | Physics | 10:00–12:20 | 140 min | 80 | Written | Subject Teacher |
| 4 Mar | XI MPC | Physics | 10:00–12:20 | 140 min | 80 | Written | Subject Teacher |

Paper types: Written · MCQ (OMR sheet) · Mixed (Written + MCQ) · Oral (languages) · Practical

[+ Add Row] → add a date-class-subject combination.

---

### Tab 3 — Internal Assessment Linkage

For subjects with IA component, specify which IA components count:

| Subject | IA Component | Source | Marks Contribution |
|---|---|---|---|
| All subjects (IX–X) | Periodic Tests (best of 3) | B-31 — PT1 + PT2 + PT3 | 10 marks |
| All subjects (IX–X) | Notebook/Portfolio | B-31 — Direct entry | 5 marks |
| All subjects (IX–X) | Subject Enrichment Activity | B-31 — Direct entry | 5 marks |
| All subjects (XI–XII) | Periodic Tests (best of 2) | B-31 | 10 marks |
| All subjects (XI–XII) | Practical/Project | B-31 — Practical module | 20 marks |

IA marks are pulled automatically from B-31 (Internal Assessment Manager) when result computation (B-18) runs.

---

### Tab 4 — Student Eligibility

Defines who is eligible to appear in this exam:

| Rule | Setting |
|---|---|
| Minimum attendance required | 75% (CBSE requirement) |
| Allow below-75% with principal condonation | Yes (Principal can grant exam condonation) |
| Fee clearance required | No (exams not blocked for fee dues — state policy) |
| Transfer Certificate students | Excluded from annual exam (they've left) |
| Detained students (from previous year) | Excluded from current class exam |

**Condonation list:** Shows students below 75% attendance who need Principal condonation:

| Student | Class | Attendance % | Shortage | Status |
|---|---|---|---|---|
| Rahul M | IX-A | 68.4% | 6.6% | ⏳ Awaiting Principal decision |
| Priya S | XI-B | 71.2% | 3.8% | ✅ Condonation granted |

---

### Tab 5 — Question Paper (QP) Status

Status of question paper submissions from HODs (feeds B-32 Question Paper Workflow):

| Subject | Class | Assigned Teacher | Submitted | HOD Reviewed | Exam Cell | Status |
|---|---|---|---|---|---|---|
| English | VI–VIII | Ms. Suma | ✅ 20 Feb | ✅ HOD Kavitha 22 Feb | ✅ Exam Cell 23 Feb | ✅ Ready |
| Mathematics | VI–VIII | Mr. Arjun | ✅ 19 Feb | ✅ HOD 21 Feb | ✅ 22 Feb | ✅ Ready |
| Physics | IX, XI | Ms. Lakshmi | ✅ 21 Feb | ⚠️ Pending HOD | — | 🔄 With HOD |
| Biology | IX, XI | Ms. Anjali | ⬜ Not submitted | — | — | 🔴 Overdue |
| Chemistry | IX, XI | Mr. Ravi | ⬜ Not submitted | — | — | 🔴 Overdue |

[Send Reminder] → WhatsApp + in-app reminder to teacher for overdue QP submissions.

---

### Tab 6 — Exam Settings

| Setting | Value |
|---|---|
| Grace Marks Policy | CBSE standard (Best of 5, compensatory marks) |
| OMR Answer Sheet | No (written answer sheets) |
| Hall Ticket Required | Yes |
| Seating Arrangement | Roll number order within section |
| Evaluation Mode | School teachers only (no external evaluators) |
| Result Publication Mode | Batch (all classes together after all marking done) |
| Report Card Format | CBSE standard with school letterhead |
| Special Needs Accommodation | Yes — extra time for certified students |

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/config/` | Full exam config |
| 2 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/config/` | Update config |
| 3 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/config/marks-structure/` | Marks structure |
| 4 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/config/marks-structure/` | Update marks structure |
| 5 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/config/subject-schedule/` | Subject-date-class schedule |
| 6 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/config/subject-schedule/` | Update schedule |
| 7 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/config/eligibility/` | Student eligibility list |
| 8 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/config/eligibility/condone/` | Grant condonation (Principal) |
| 9 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/config/qp-status/` | QP submission status |
| 10 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/config/qp-reminder/` | Send QP submission reminder |

---

## 5. Business Rules

- Exam configuration must be approved by Principal before hall tickets can be generated (B-12)
- Attendance eligibility check (75%) is computed from A-17 data; condonation request is routed through A-23 (Approval Workflow Hub)
- If fee clearance is enabled, the system checks against the fee module (div-d) — this is off by default as per RTE guidelines (no exam blockage for fee non-payment)
- Marks structure changes after marks entry has begun are not allowed; Exam Cell Head must contact Platform Admin for corrections
- Special needs accommodations (extra time, scribe, large-print paper) require a documented medical/disability certificate in the student's profile

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
