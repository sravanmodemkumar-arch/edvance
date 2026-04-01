# B-02 — Lesson Plan Review

> **URL:** `/school/academic/dept/<dept>/lesson-plans/`
> **File:** `b-02-lesson-plan-review.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HOD (S4) — review/approve own dept · VP Academic (S5) — read all · Class Teacher (S3) — submit · Subject Teacher (S3) — submit · Principal (S6) — full

---

## 1. Purpose

Manages the weekly/fortnightly lesson plan submission and review workflow. In CBSE and most state board schools, teachers are required to submit written lesson plans — the HOD reviews them for curriculum alignment, pedagogical quality, and pace. A lesson plan is not just a formality; it is the primary evidence that the teacher has prepared for the class, that the topic sequence matches the board-prescribed syllabus, and that assessment integration is planned. This page is where the HOD exercises academic quality control for their department.

**Indian context:** CBSE's Teacher Development Programme (TDP) emphasises lesson planning as a core competency. Inspection teams from CBSE check lesson plan registers during affiliation inspections. This digital system replaces the physical lesson plan register.

---

## 2. Page Layout

### 2.1 Header
```
Lesson Plan Review — Science Department         [+ Submit Plan]  [Export Register]
Term: [Term 2 ▼]  Week: [Current ▼]  Subject: [All ▼]  Status: [All ▼]
Pending Review: 4  ·  Approved This Week: 12  ·  Returned: 1
```

---

## 3. Tabs

### Tab 1 — Pending Review (default)

Lists all lesson plans awaiting HOD action, oldest first:

| # | Teacher | Subject | Class | Week/Date | Topic(s) | Submitted | Days Waiting | Action |
|---|---|---|---|---|---|---|---|---|
| 1 | Ms. Anjali Singh | Biology | XI-A | Week 12 (24–28 Mar) | Cell Division: Mitosis, Meiosis | 22 Mar | 4 days | [Review] [Return] |
| 2 | Mr. Ravi Kumar | Chemistry | XII-B | Week 12 | Electrochemistry: Nernst Equation | 21 Mar | 5 days | [Review] [Return] |
| 3 | Ms. Lakshmi Devi | Physics | XII-A | Week 12 | Wave Optics | 20 Mar | 6 days 🔴 | [Review] [Return] |
| 4 | Ms. Anjali Singh | Biology | X-A | Week 11 | Heredity and Evolution | 19 Mar | 7 days 🔴 | [Review] [Return] |

- Days waiting > 5 = amber; > 7 = red (overdue)
- [Review] opens the `lesson-plan-review` drawer

---

### Tab 2 — All Plans (History)

Full lesson plan register for the department, paginated:

| Teacher | Subject | Class | Week | Topics | Status | Reviewed By | Review Date |
|---|---|---|---|---|---|---|---|
| Ms. Lakshmi Devi | Physics | XII-A | Week 11 | Electromagnetic Induction | ✅ Approved | HOD Priya | 18 Mar |
| Mr. Ravi Kumar | Chemistry | XI-B | Week 11 | Chemical Kinetics | ✅ Approved | HOD Priya | 17 Mar |
| Ms. Anjali Singh | Biology | XI-A | Week 10 | Cell Biology: Organelles | 🔄 Returned | HOD Priya | 12 Mar |
| Dr. Suresh P | Physics | XI-A | Week 10 | Rotational Motion | ✅ Approved | HOD Priya | 11 Mar |

Status badges: ✅ Approved · 🔄 Returned (with note) · ⚠️ Pending · ❌ Rejected (rare — LP completely inadequate)

---

### Tab 3 — Template Library

Pre-built lesson plan templates that teachers can use as a starting point:

| Template Name | Board | Subject Level | Format | Last Updated |
|---|---|---|---|---|
| CBSE Standard Lesson Plan | CBSE | All | 5-E Model (Engage, Explore, Explain, Elaborate, Evaluate) | Jan 2026 |
| Science Lab Practical Plan | CBSE | Science VI–XII | Lab-specific (Aim, Materials, Procedure, Observation, Result) | Jan 2026 |
| Activity-Based Learning Plan | NEP 2020 | All primary | Activity-centred, no rote | Feb 2026 |
| Revision Lesson Plan | All boards | All | Focused revision with MCQ sets | Dec 2025 |

HOD can add/edit department-specific templates. Teachers download and fill the template, then submit.

---

## 4. Lesson Plan Review Drawer (680px)

Triggered by clicking [Review] on any plan:

### Drawer Header
```
Lesson Plan Review
Ms. Anjali Singh · Biology · Class XI-A · Week 12 (24–28 Mar 2026)
Submitted: 22 Mar 2026, 7:14 PM
```

### Section A — Plan Details

| Field | Value |
|---|---|
| Topic | Cell Division: Mitosis and Meiosis |
| Duration | 3 periods × 45 min (Mon P2, Wed P3, Fri P1) |
| Learning Objectives | 1. Students will distinguish between mitosis and meiosis; 2. Draw and label phases; 3. Relate cell division to growth and reproduction |
| Prerequisite Topics | Cell structure (Week 8), DNA structure (Week 9) |
| Teaching Method | Lecture + Diagram drawing + Microscope observation activity |
| Resources Required | NCERT Biology textbook Ch.10, microscope slides (prepared), chart paper |
| Board Alignment | CBSE Class XI Biology Chapter 10 — Cell Cycle and Cell Division |

### Section B — Period-wise Plan

| Period | Date | Topic Segment | Teaching Activity | Assessment |
|---|---|---|---|---|
| P1 (Mon P2) | 24 Mar | Cell cycle — overview + G1/S/G2 phases | Lecture + diagram | Q&A verbal |
| P2 (Wed P3) | 26 Mar | Mitosis — stages with diagram | Board drawing + student drawing | Exit ticket (5 MCQs) |
| P3 (Fri P1) | 28 Mar | Meiosis — stages, comparison with mitosis | Microscope practical | Lab diagram worksheet |

### Section C — Attachment
- Lesson Plan PDF (if uploaded) — [Preview] [Download]
- Diagram sketches (optional attachment)

### Section D — HOD Review Form

```
Curriculum Alignment: [1 ●○○○○] [2 ○●○○○] [3 ○○●○○] [4 ○○○●○] [5 ○○○○●]
Pedagogical Quality:  [1 ●○○○○] [2 ○●○○○] [3 ○○●○○] [4 ○○○●○] [5 ○○○○●]
Assessment Integration: [1] [2] [3] [4] [5]
Pace vs Syllabus:       [1] [2] [3] [4] [5]

Overall Score: [auto-computed average]

HOD Notes / Feedback:
[                                                    ]
[                                                    ]

Action:  [✅ Approve]  [🔄 Return with Feedback]  [❌ Reject]
```

**Approve** → status = Approved; teacher gets notification
**Return** → HOD feedback notes required; teacher must re-submit revised plan
**Reject** → very rare; requires mandatory reason; VP Academic notified automatically

---

## 5. Teacher Submission View (for Class/Subject Teacher)

When a teacher accesses this page, they see only their own plans:

### My Lesson Plans

| Subject | Class | Week | Topics | Status | HOD Feedback |
|---|---|---|---|---|---|
| Biology | XI-A | Week 12 | Cell Division | ⚠️ Pending Review | — |
| Biology | XI-A | Week 11 | Cell Cycle | ✅ Approved (score: 4.4/5) | Well-paced, good assessment |
| Biology | X-A | Week 10 | Heredity | 🔄 Returned | Add more formative assessment activities |

**[+ Submit New Plan]** button triggers the submission form drawer (600px):

| Field | Type | Notes |
|---|---|---|
| Subject | Dropdown | Teacher's assigned subjects only |
| Class | Dropdown | Teacher's assigned classes |
| Week | Date picker | Week start (Monday) |
| Topic(s) | Text | Free text; should match syllabus chapter/section |
| Period-wise breakdown | Repeating section | One row per period with topic/activity/assessment |
| Teaching Method | Multi-select | Lecture, Group work, Lab practical, Discussion, Demonstration, Activity |
| Resources | Text | Materials, textbook references |
| NCERT/Board Chapter Reference | Text | e.g., "CBSE Class XI Biology Ch.10 Section 10.2" |
| Attachment | File | PDF upload (optional; max 5MB) |

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/lesson-plans/?dept={dept_id}&term={term}&status={status}` | List lesson plans |
| 2 | `POST` | `/api/v1/school/{id}/lesson-plans/` | Submit new lesson plan |
| 3 | `GET` | `/api/v1/school/{id}/lesson-plans/{plan_id}/` | Plan detail |
| 4 | `PATCH` | `/api/v1/school/{id}/lesson-plans/{plan_id}/review/` | HOD review (approve/return/reject) |
| 5 | `GET` | `/api/v1/school/{id}/lesson-plans/templates/` | Template library |
| 6 | `POST` | `/api/v1/school/{id}/lesson-plans/templates/` | Add HOD template |
| 7 | `GET` | `/api/v1/school/{id}/lesson-plans/stats/?dept={dept_id}&term={term}` | Department stats |
| 8 | `GET` | `/api/v1/school/{id}/lesson-plans/teacher/{teacher_id}/` | Teacher's plan history |
| 9 | `POST` | `/api/v1/school/{id}/lesson-plans/{plan_id}/reminder/` | Send submission reminder to teacher |

---

## 7. Business Rules

- Teachers should submit lesson plans for the coming week by Friday 6 PM (configurable school-wide)
- If a teacher hasn't submitted for the current week by Sunday midnight, HOD gets an auto-alert
- HOD must review and act within 5 working days of submission; overdue review is visible on HOD dashboard
- Returned plans must be resubmitted within 2 days
- A lesson plan is considered "submitted" only when it covers ≥ 1 period with a defined topic — empty plans are rejected at the API level
- Lesson plan scores feed into teacher performance reports visible to VP Academic and Principal
- Plans cannot be deleted; only marked as superseded (if teacher resubmits after return)
- Export Register generates a PDF that mimics the physical lesson plan register format (used for CBSE inspections)
- NCERT chapter references are validated against a master chapter database; invalid references show a warning (not a block)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
