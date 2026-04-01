# B-23 — Lesson Plan Submission

> **URL:** `/school/academic/lesson-plans/`
> **File:** `b-23-lesson-plan-submission.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Subject Teacher (S3) — submit/view own · Class Teacher (S3) — submit/view own · HOD (S4) — review own dept · Academic Coordinator (S4) — review all · Principal (S6) — full

---

## 1. Purpose

The teacher-facing lesson plan workflow. While B-02 is the HOD's review interface, B-23 is what teachers see — their submission dashboard where they create new lesson plans, track their submission history, view HOD feedback, and resubmit returned plans. This is the point of entry for all lesson plans into the system. Unlike B-02 (read by HODs), B-23 is written by teachers. A teacher submitting well-structured lesson plans regularly, receiving good HOD scores, is evidence of professional practice — visible to VP Academic in performance reviews.

---

## 2. Page Layout

### 2.1 Header
```
Lesson Plan Submission                            [+ New Lesson Plan]  [My Statistics]
Teacher: Ms. Anjali Singh  ·  Department: Science  ·  Academic Year: 2025–26
This Week: [Week 12 — 24–28 Mar]  ·  Next due: Friday 28 Mar by 6:00 PM
Submitted this term: 18  ·  Approved: 15  ·  Returned: 2  ·  Pending review: 1
```

---

## 3. My Lesson Plan Dashboard

### Status Summary Strip

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Approved    │ Pending     │ Returned    │ Avg HOD     │
│ This Term   │ Review      │ (resubmit)  │ Score       │
│   15        │    1        │    2        │  4.1 / 5.0  │
│ ✅          │ 🟡 pending  │ 🔄 action   │  Good       │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

---

## 4. My Plans List

| Subject | Class | Week | Topics Covered | Submitted | Status | HOD Score | Action |
|---|---|---|---|---|---|---|---|
| Biology | XI-A | Week 12 (24–28 Mar) | Cell Division: Mitosis, Meiosis | 22 Mar | ⚠️ Pending Review | — | [View] |
| Biology | X-A | Week 11 (17–21 Mar) | Heredity and Evolution | 15 Mar | 🔄 Returned | — | [Revise & Resubmit] |
| Biology | XI-A | Week 10 (10–14 Mar) | Cell Biology: Organelles | 8 Mar | ✅ Approved | 4.2/5 | [View] |
| Biology | XI-B | Week 10 | Photosynthesis | 8 Mar | ✅ Approved | 4.4/5 | [View] |
| Biology | X-A | Week 9 | Genetics: Mendel's Laws | 2 Mar | ✅ Approved | 3.8/5 | [View] |

**Returned plan feedback:**

For the Week 11 X-A Biology plan marked "Returned":
```
HOD Feedback (Dr. Priya Venkataraman, 20 Mar):
  "Good topic coverage. However, the assessment section only has a single end-of-
  period quiz. Please add more formative assessment activities — at least one per
  period (exit ticket, think-pair-share, whiteboard check). Also include NCERT
  chapter reference. Please resubmit by 25 Mar."

  Score given: Not rated (returned plans are not scored until approved)
```

[Revise & Resubmit] → opens the plan in edit mode with HOD's comments shown as a side panel.

---

## 5. New Lesson Plan Form (600px drawer)

[+ New Lesson Plan] → opens the submission form:

### Step 1 — Basics
| Field | Value |
|---|---|
| Subject | Dropdown (own assigned subjects) |
| Class | Dropdown (own assigned classes) |
| Teaching Week | Week picker (Mon–Fri date range) |
| Plan Type | Weekly / Fortnightly / Single Period |

### Step 2 — Topic Details
| Field | Value |
|---|---|
| Topic(s) | Search from Topic Master (B-22) — autocomplete by typing topic name |
| NCERT Chapter Reference | Auto-filled when topic selected; editable |
| Prerequisite Topics | Which topics should students have covered before this (cross-reference) |
| Learning Objectives | 2–4 bullet points: "Students will be able to..." |
| Prior Knowledge | What students already know that this lesson builds on |

### Step 3 — Period-wise Plan

Repeating section — one row per period:

| Period | Date | Segment | Teaching Method | Assessment |
|---|---|---|---|---|
| P1 | 24 Mar (Mon P3) | Mitosis — Cell cycle overview | Lecture + diagram on board | Verbal Q&A |
| P2 | 26 Mar (Wed P1) | Mitosis phases — prophase, metaphase | PPT + YouTube video (3 min) | Exit ticket (5 MCQ) |
| P3 | 28 Mar (Fri P2) | Meiosis — comparison with mitosis | Microscope activity | Lab worksheet |

Teaching methods: Lecture · Group discussion · Demonstration · Lab activity · Video · Activity/Game · Think-pair-share · Project work

Assessments: Verbal Q&A · Exit ticket · MCQ quiz · Worksheet · Lab report · Peer assessment · None

### Step 4 — Resources & Attachments
| Field | Value |
|---|---|
| Resources | Textbook references, YouTube links, printable material list |
| Lab/Equipment needed | List any special equipment for practical components |
| Attachment | Upload PDF/DOC (optional, max 5MB) |

### Step 5 — Review & Submit
Preview of the complete plan. [Save Draft] or [Submit to HOD].

---

## 6. Submission Reminder System

If a teacher hasn't submitted a plan for the current week by Thursday 12 PM:
- **Thursday 12 PM:** In-app reminder notification
- **Friday 6 PM:** WhatsApp reminder + HOD is notified that the teacher hasn't submitted

If still not submitted by Saturday:
- HOD gets an "Overdue submission" alert in B-01 (Dept Dashboard)
- Appears in teacher's performance tracking as a missed submission

---

## 7. My Statistics

[My Statistics] → shows personal performance metrics:

| Term | Plans Submitted | Approved | Returned | Avg Score | Submission Rate |
|---|---|---|---|---|---|
| Term 1 2025–26 | 24 | 22 | 2 | 4.0/5 | 92.3% (24/26 weeks) |
| Term 2 2025–26 | 18 | 15 | 2 | 4.1/5 | 90.0% (18/20 weeks) |
| Full Year 2024–25 | 42 | 40 | 2 | 3.8/5 | 88.5% |

Score trends over time (line chart): shows whether teacher's plan quality is improving.

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/lesson-plans/mine/?year={year}&term={term}` | Teacher's own plans |
| 2 | `POST` | `/api/v1/school/{id}/lesson-plans/` | Submit new plan |
| 3 | `GET` | `/api/v1/school/{id}/lesson-plans/{plan_id}/` | Plan detail |
| 4 | `PATCH` | `/api/v1/school/{id}/lesson-plans/{plan_id}/` | Edit draft plan |
| 5 | `POST` | `/api/v1/school/{id}/lesson-plans/{plan_id}/submit/` | Submit to HOD |
| 6 | `POST` | `/api/v1/school/{id}/lesson-plans/{plan_id}/resubmit/` | Resubmit returned plan |
| 7 | `GET` | `/api/v1/school/{id}/lesson-plans/mine/stats/` | Teacher statistics |

---

## 9. Business Rules

- A teacher can only submit plans for their own assigned subjects and classes (from B-30)
- Draft plans are auto-saved every 2 minutes when the form is open
- Once submitted, a plan cannot be edited by the teacher until the HOD returns it
- Resubmitted plans go back to the same HOD for re-review; the original submission and first review are preserved in plan history
- Plans are week-dated — a teacher cannot submit the same week/subject/class combination twice (must edit and resubmit the existing one)
- This page (B-23) and B-02 are the same underlying data seen from different role perspectives; access control determines what each user sees and can do

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
