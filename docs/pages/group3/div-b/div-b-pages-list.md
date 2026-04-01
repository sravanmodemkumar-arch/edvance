# Group 3 — Division B: Academic Management — Pages Reference

> **Division:** B — Academic Management
> **Roles:** 4 roles (see Role Summary below)
> **Base URL prefix:** `/school/academic/`
> **Theme:** Light (`portal_base.html`)
> **Group:** Group 3 — School Portal
> **Status key:** ✅ Spec done · ⬜ Not started

---

## Scale Context

Same as div-a: 1,000 schools · 1,000 avg students per school · 40–80 teaching staff per school · 14 class levels (LKG–XII) · 52 sections avg per school · CBSE/ICSE/28 state boards.

---

## Critical Indian Academic Management Context

The academic management layer in an Indian school is where curriculum meets delivery. The HOD is responsible for their department's academic quality — teacher performance, lesson plan quality, syllabus completion pace, question paper quality, and result analysis. The Exam Cell Head is the operational hub for all things assessment — from scheduling a Unit Test to coordinating CBSE board exam registration (LOC submission). The Academic Coordinator is the institution-wide academic planner who bridges all departments, manages the yearly academic plan, and ensures board compliance.

**Key Indian academic systems:**
- **CBSE's Academic Calendar:** Minimum 3 Periodic Tests + Half-Yearly + Annual per year; internal marks (20% for IX–X, 30% for XI–XII) + board marks (80%/70%) for Classes IX–XII
- **CBSE Internal Assessment (IA):** Periodic Tests (10m) + Notebook/Portfolio (5m) + Subject Enrichment Activity (5m) = 20m for IX–X; 30m structure for XI–XII; computed and submitted to CBSE
- **LOC (List of Candidates):** CBSE LOC submission for Class X and XII — annual mandatory activity with Aadhaar data verification, photo/signature upload, fee payment to CBSE
- **CCE (Continuous and Comprehensive Evaluation):** CBSE's formative + summative blend for junior classes (I–VIII)
- **NEP 2020 Assessment Reform:** Competency-based assessment; remedial teaching mandated for below-threshold students; schools in transition
- **State Board Systems:** AP/TS quarterly exams; Maharashtra annual; TN 3-term system; each board has its own IA and compartment exam structure
- **UFM (Unfair Means):** CBSE has a formal UFM policy; incidents during exams must be documented, investigated, and logged
- **Practical Exams (Board-level):** CBSE Class X/XII practical exams involve CBSE-appointed external examiners; separate workflow from theory exams
- **Compartment Exams:** CBSE conducts compartment (supplementary) exams in July for students who fail in 1–2 subjects
- **Competitive Exam Coaching-Integrated Schools:** Daily DPPs (Daily Practice Problems), weekly tests, monthly AITS (All India Test Series) — require a dedicated test engine workflow

---

## Division B — Role Summary

| # | Role | Level | Description | Post-Login URL |
|---|---|---|---|---|
| 1 | Head of Department (HOD) | S4 | Department-level academic leadership; teacher supervision, lesson plan review, subject allocation, question paper approval, result analysis | Redirected to Principal Dashboard with department filter |
| 2 | Exam Cell Head / Examination Controller | S4 | School-wide exam scheduling, seating, hall tickets, invigilation, result coordination, CBSE LOC submission, UFM management | `/school/academic/exams/` |
| 3 | Academic Coordinator | S4 | Institution-wide academic planning; academic year schedule, PT schedule, syllabus monitoring across departments, remedial teaching coordination, NEP compliance, PTM planning. For coaching-integrated schools: also manages DPP schedule and test series | `/school/academic/coordinator/` |
| 4 | Timetable Coordinator | S3 | Builds and maintains the school's master timetable; manages period schedule and bell timings; room/lab allotment; substitution when teachers are absent | `/school/academic/timetable/` |

**Note:** HOD does not have a separate standalone dashboard; HODs access the Principal Dashboard with department scope filters, plus specific management pages (syllabus, lesson plans, department report) in their department view. Academic Coordinator exists in all schools; coaching-integration pages (B-26/B-27) are feature-flagged separately.

---

## Section 1 — HOD Management Pages

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| B-01 | Department Dashboard | `/school/academic/dept/<dept>/` | `b-01-department-dashboard.md` | P0 | ✅ |
| B-02 | Lesson Plan Review | `/school/academic/dept/<dept>/lesson-plans/` | `b-02-lesson-plan-review.md` | P1 | ✅ |
| B-03 | Syllabus Tracker | `/school/academic/dept/<dept>/syllabus/` | `b-03-syllabus-tracker.md` | P0 | ✅ |
| B-04 | Question Paper Bank (Dept) | `/school/academic/dept/<dept>/question-bank/` | `b-04-question-paper-bank.md` | P1 | ✅ |
| B-05 | Department Performance Analytics | `/school/academic/dept/<dept>/analytics/` | `b-05-dept-analytics.md` | P1 | ✅ |
| B-30 | Subject Allocation Manager | `/school/academic/dept/<dept>/allocation/` | `b-30-subject-allocation.md` | P1 | ✅ |

---

## Section 2 — Timetable Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| B-28 | Period & Bell Schedule Configuration | `/school/academic/timetable/periods/` | `b-28-period-configuration.md` | P0 | ✅ |
| B-29 | Room & Lab Allotment | `/school/academic/timetable/rooms/` | `b-29-room-lab-allotment.md` | P1 | ✅ |
| B-06 | Master Timetable | `/school/academic/timetable/` | `b-06-master-timetable.md` | P0 | ✅ |
| B-07 | Timetable Builder | `/school/academic/timetable/build/` | `b-07-timetable-builder.md` | P1 | ✅ |
| B-08 | Substitution Manager | `/school/academic/timetable/substitutions/` | `b-08-substitution-manager.md` | P0 | ✅ |
| B-09 | Timetable Conflict Detector | `/school/academic/timetable/conflicts/` | `b-09-conflict-detector.md` | P1 | ✅ |

> **Note:** B-28 (Period Config) and B-30 (Subject Allocation) are prerequisites for B-07 (Timetable Builder). They must be configured before the timetable can be built.

---

## Section 3 — Examination Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| B-10 | Exam Schedule Manager | `/school/academic/exams/schedule/` | `b-10-exam-schedule-manager.md` | P0 | ✅ |
| B-11 | Exam Configuration | `/school/academic/exams/<exam_id>/config/` | `b-11-exam-configuration.md` | P0 | ✅ |
| B-32 | Question Paper Workflow | `/school/academic/exams/<exam_id>/question-papers/` | `b-32-question-paper-workflow.md` | P1 | ✅ |
| B-12 | Hall Ticket Generator | `/school/academic/exams/<exam_id>/hall-tickets/` | `b-12-hall-ticket-generator.md` | P0 | ✅ |
| B-13 | Seating Arrangement | `/school/academic/exams/<exam_id>/seating/` | `b-13-seating-arrangement.md` | P1 | ✅ |
| B-14 | Invigilation Duty Chart | `/school/academic/exams/<exam_id>/invigilators/` | `b-14-invigilation-duty-chart.md` | P1 | ✅ |
| B-15 | Answer Script Management | `/school/academic/exams/<exam_id>/scripts/` | `b-15-answer-script-management.md` | P1 | ✅ |
| B-35 | Practical Exam Coordinator | `/school/academic/exams/practicals/` | `b-35-practical-exam-coordinator.md` | P1 | ✅ |
| B-36 | UFM (Unfair Means) Register | `/school/academic/exams/ufm/` | `b-36-ufm-register.md` | P1 | ✅ |
| B-33 | Board Exam Registration (LOC) | `/school/academic/exams/board-registration/` | `b-33-board-exam-registration.md` | P0 | ✅ |
| B-39 | Supplementary / Compartment Exam | `/school/academic/exams/supplementary/` | `b-39-supplementary-exam.md` | P2 | ✅ |

---

## Section 4 — Results & Report Cards

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| B-31 | Internal Assessment Manager | `/school/academic/ia/` | `b-31-internal-assessment.md` | P0 | ✅ |
| B-16 | Marks Entry | `/school/academic/marks/<exam_id>/` | `b-16-marks-entry.md` | P0 | ✅ |
| B-17 | Marks Review & Approval | `/school/academic/marks/<exam_id>/review/` | `b-17-marks-review.md` | P0 | ✅ |
| B-37 | Grace Marks & Moderation Register | `/school/academic/results/grace-marks/` | `b-37-grace-marks.md` | P1 | ✅ |
| B-18 | Result Computation | `/school/academic/results/<exam_id>/compute/` | `b-18-result-computation.md` | P0 | ✅ |
| B-19 | Report Card Generator | `/school/academic/results/<exam_id>/report-cards/` | `b-19-report-card-generator.md` | P0 | ✅ |
| B-20 | Result Analytics | `/school/academic/results/<exam_id>/analytics/` | `b-20-result-analytics.md` | P1 | ✅ |

> **Note:** B-31 (Internal Assessment) must be computed before B-18 (Result Computation) can produce final marks for CBSE schools. B-37 (Grace Marks) applies after initial result computation, before finalisation.

---

## Section 5 — Syllabus & Curriculum

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| B-21 | Curriculum Manager | `/school/academic/curriculum/` | `b-21-curriculum-manager.md` | P1 | ✅ |
| B-22 | Topic Master (Subject-Class) | `/school/academic/curriculum/topics/` | `b-22-topic-master.md` | P1 | ✅ |
| B-23 | Lesson Plan Submission | `/school/academic/lesson-plans/` | `b-23-lesson-plan-submission.md` | P1 | ✅ |

---

## Section 6 — Academic Planning & Remedial

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| B-38 | Academic Year Planner | `/school/academic/planner/` | `b-38-academic-year-planner.md` | P1 | ✅ |
| B-34 | Remedial Teaching Register | `/school/academic/remedial/` | `b-34-remedial-teaching.md` | P1 | ✅ |
| B-24 | Academic Competition Tracker | `/school/academic/competitions/` | `b-24-competition-tracker.md` | P2 | ✅ |
| B-25 | Co-Curricular Activity Register | `/school/academic/cca/` | `b-25-cca-register.md` | P2 | ✅ |

---

## Section 7 — Coaching Integration (Integrated Schools)

> These pages are only visible to schools with the "Coaching Integration" feature flag enabled.

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| B-26 | DPP Schedule Manager | `/school/academic/coaching/dpp/` | `b-26-dpp-schedule.md` | P1 | ✅ |
| B-27 | Coaching Test Planner | `/school/academic/coaching/tests/` | `b-27-coaching-test-planner.md` | P1 | ✅ |

---

## Role → Page Access Matrix

| Page | HOD S4 | Exam Cell Head S4 | Acad Coordinator S4 | Timetable Coord S3 | Class Teacher S3 | Subject Teacher S3 | Principal S6 |
|---|---|---|---|---|---|---|---|
| B-01 Dept Dashboard | ✅ Own dept | Read all depts | Read all | — | — | — | ✅ Full |
| B-02 Lesson Plan Review | ✅ Own dept | — | Read all | — | Submit | Submit | ✅ Full |
| B-03 Syllabus Tracker | ✅ Own dept | Read | Read all | — | Update own | Update own | ✅ Full |
| B-04 Question Paper Bank | ✅ Own dept | ✅ Full | Read | — | Submit | Submit | ✅ Full |
| B-05 Dept Analytics | ✅ Own dept | Read all | ✅ Full | — | — | — | ✅ Full |
| B-06 Master Timetable | Read | Read | Read | ✅ Full | Read (own) | Read (own) | ✅ Full |
| B-07 Timetable Builder | Read | Read | — | ✅ Full | — | — | ✅ Approve |
| B-08 Substitution Mgr | — | — | — | ✅ Full | — | — | ✅ Full |
| B-09 Conflict Detector | — | — | — | ✅ Full | — | — | ✅ View |
| B-10 Exam Schedule | Read | ✅ Full | ✅ Full | — | Read | Read | ✅ Approve |
| B-11 Exam Config | HOD submits QP | ✅ Full | Read | — | — | — | ✅ Approve |
| B-12 Hall Tickets | — | ✅ Full | — | — | — | — | ✅ View |
| B-13 Seating | — | ✅ Full | — | — | — | — | ✅ View |
| B-14 Invigilators | — | ✅ Full | — | ✅ View | ✅ View (own duty) | ✅ View (own duty) | ✅ Approve |
| B-15 Answer Scripts | — | ✅ Full | — | — | — | — | ✅ View |
| B-16 Marks Entry | — | — | — | — | ✅ Own class | ✅ Own subject | ✅ Full |
| B-17 Marks Review | ✅ Own dept approve | ✅ Full | — | — | — | — | ✅ Full |
| B-18 Result Computation | — | ✅ Full | — | — | — | — | ✅ Full |
| B-19 Report Cards | — | ✅ Generate | — | — | ✅ View/sign own class | — | ✅ Approve |
| B-20 Result Analytics | ✅ Own dept | ✅ Full | ✅ Full | — | Read (own class) | — | ✅ Full |
| B-21 Curriculum Mgr | ✅ Own dept | — | ✅ Full | — | — | — | ✅ Full |
| B-22 Topic Master | ✅ Own dept | — | ✅ Full | — | Update own | — | ✅ Full |
| B-23 Lesson Plans | ✅ Review | — | ✅ Review all | — | ✅ Submit | ✅ Submit | ✅ Full |
| B-24 Competition Tracker | ✅ Own dept | — | ✅ Full | — | Submit | Submit | ✅ Full |
| B-25 CCA Register | — | — | ✅ Full | — | Submit | Submit | ✅ Full |
| B-26 DPP Schedule | — | — | ✅ Full | — | Read | Read | ✅ Full |
| B-27 Coaching Test Planner | — | ✅ + Coaching | ✅ Full | — | Read | Read | ✅ Full |
| B-28 Period Config | — | — | — | ✅ Full | — | — | ✅ Approve |
| B-29 Room & Lab Allotment | Read | Read | Read | ✅ Full | Read | Read | ✅ Full |
| B-30 Subject Allocation | ✅ Own dept | Read | Read all | Read | — | — | ✅ Full |
| B-31 Internal Assessment | ✅ Own dept input | ✅ Full compute | Read | — | ✅ Enter own | ✅ Enter own | ✅ Full |
| B-32 QP Workflow | ✅ Own dept approve | ✅ Full | — | — | Submit draft | Submit draft | ✅ Full |
| B-33 Board Registration LOC | — | ✅ Full | Read | — | — | — | ✅ Approve |
| B-34 Remedial Teaching | ✅ Own dept | Read | ✅ Full | — | ✅ Conduct | ✅ Conduct | ✅ Full |
| B-35 Practical Exam | — | ✅ Full | Read | — | ✅ Examiner duties | ✅ Examiner duties | ✅ Full |
| B-36 UFM Register | — | ✅ Full | Read | — | ✅ File report | ✅ File report | ✅ Full |
| B-37 Grace Marks | ✅ Own dept view | ✅ Full | Read | — | — | — | ✅ Full |
| B-38 Academic Year Planner | Read | Read | ✅ Full | Read | Read | Read | ✅ Approve |
| B-39 Supplementary Exam | — | ✅ Full | Read | — | — | — | ✅ Full |

---

## Shared Drawers (all div-b pages)

| Drawer | Trigger | Width | Description |
|---|---|---|---|
| `lesson-plan-review` | B-02 → lesson plan row | 680px | Full lesson plan view + approve/return/notes |
| `topic-coverage-update` | B-03 → topic row | 420px | Mark topic as done/in-progress/skipped + date + teacher note |
| `question-create` | B-04 → + Add Question | 680px | Question editor with type/difficulty/marks/solution |
| `exam-config-detail` | B-10/B-11 → exam row | 680px | Exam parameters, subjects, marking scheme, class-section assignment |
| `hall-ticket-preview` | B-12 → student | 480px | Hall ticket PDF preview for one student |
| `seating-plan-view` | B-13 → room | 560px | Room seating layout grid |
| `marks-entry-class` | B-16 → class row | 760px | Full class marks entry grid (student × subject) |
| `result-review` | B-17 → class | 640px | Marks overview + anomaly flags + approve |
| `report-card-preview` | B-19 → student | 640px | Full report card PDF preview |
| `substitute-assign` | B-08 → period | 480px | Select substitute from free staff list |
| `period-slot-edit` | B-28 → period row | 400px | Edit period start/end time, type, label |
| `room-booking-view` | B-29 → room row | 520px | Room weekly booking grid + conflict overlay |
| `ia-marks-entry` | B-31 → student row | 560px | IA marks entry (PT1, PT2, PT3, Notebook, Enrichment) |
| `qp-review-approval` | B-32 → QP row | 680px | QP preview + HOD/Exam Cell approval form |
| `ufm-case-detail` | B-36 → case row | 600px | UFM incident detail + committee decision form |
| `grace-apply` | B-37 → student row | 480px | Apply grace/compensatory marks with reason |

---

## Implementation Priority

```
P0 — Before school goes live
  B-28   Period & Bell Schedule Configuration  ← prerequisite for timetable
  B-01   Dept Dashboard
  B-03   Syllabus Tracker
  B-06   Master Timetable
  B-10   Exam Schedule
  B-16   Marks Entry
  B-17   Marks Review
  B-18   Result Computation
  B-19   Report Card Generator
  B-31   Internal Assessment Manager           ← CBSE IA mandatory
  B-33   Board Exam Registration (LOC)         ← CBSE Class X/XII mandatory

P1 — Sprint 2
  B-02, B-04, B-05, B-07, B-08, B-11, B-12, B-13, B-14, B-15, B-20, B-21, B-22, B-23, B-26, B-27
  B-29   Room & Lab Allotment
  B-30   Subject Allocation Manager
  B-32   Question Paper Workflow
  B-34   Remedial Teaching Register
  B-35   Practical Exam Coordinator
  B-36   UFM Register
  B-37   Grace Marks & Moderation Register
  B-38   Academic Year Planner

P2 — Sprint 3
  B-09, B-24, B-25
  B-39   Supplementary / Compartment Exam
```

---

## Why These Pages Were Added

| Page | Reason |
|---|---|
| B-28 Period Config | Prerequisite: Timetable builder (B-07) needs period slots defined before it can function |
| B-29 Room & Lab Allotment | Prevents lab double-booking; science schools have 1 chemistry/physics/biology lab each |
| B-30 Subject Allocation | Prerequisite: Timetable builder needs teacher-class-subject assignments as input data |
| B-31 Internal Assessment | CBSE mandatory: 20m IA for IX–X, 30m for XI–XII; without this, report cards are incomplete |
| B-32 QP Workflow | Custody chain: teacher draft → HOD approval → printing → sealed covers → dispatch record |
| B-33 Board Registration (LOC) | CBSE LOC submission (annual, Class X/XII): Aadhaar verification, photo/signature upload, fee payment |
| B-34 Remedial Teaching | NEP 2020 mandated; at-risk students require documented supplementary instruction plan |
| B-35 Practical Exam Coordinator | CBSE board practicals involve CBSE-appointed external examiners; distinct from theory exam workflow |
| B-36 UFM Register | CBSE policy requires formal UFM documentation; committee proceeding + outcome record |
| B-37 Grace Marks Register | Board-mandated audit trail for any grace/moderation applied before result finalisation |
| B-38 Academic Year Planner | Academic Coordinator plans full year: PT schedule, term dates, project dates, instructional days count |
| B-39 Supplementary Exam | CBSE compartment exam (July): eligibility list, hall tickets, marks submission — annual cycle |

---

*Last updated: 2026-03-26 · Total pages: 39 · Roles: 4 · Group: 3 — School Portal · Status: ✅ All 39 page specs complete*
