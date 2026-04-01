# C-04 — Question Bank Management

> **URL:** `/coaching/faculty/question-bank/`
> **File:** `c-04-question-bank.md`
> **Priority:** P1
> **Roles:** Faculty (K2) · Question Reviewer (K4) · Test Series Coordinator (K4)

---

## 1. Question Bank Overview

```
QUESTION BANK — Mr. Suresh Kumar (Quantitative Aptitude)
As of 30 March 2026

MY CONTRIBUTIONS:
  ┌────────────────────────────────────────────────────────────────────────────┐
  │  1,240 Total    984 Approved    206 Pending    50 Rejected    4.2/5.0     │
  │  Questions      Questions       Review         Questions      Avg Quality  │
  │  (my uploads)                                  (revised: 34)  Score       │
  └────────────────────────────────────────────────────────────────────────────┘

BANK BREAKDOWN BY TOPIC (my questions):
  Topic                    │ My Qs │ Approved │ Easy │ Med  │ Hard │ Used in Tests
  ─────────────────────────┼───────┼──────────┼──────┼──────┼──────┼──────────────
  Percentage               │  120  │  118     │  40  │  58  │  22  │  84 times
  Profit & Loss            │  110  │  108     │  36  │  54  │  20  │  76 times
  Time & Work              │  140  │  136     │  48  │  66  │  26  │  92 times
  Mensuration              │  180  │  174     │  54  │  82  │  44  │  108 times
  Data Interpretation      │  220  │  210     │  38  │  110 │  72  │  140 times
  Algebra                  │  160  │  152     │  42  │  88  │  30  │  96 times
  Number Series            │   90  │  86      │  30  │  44  │  16  │  48 times
  Other                    │  220  │  —       │  —   │  —   │  —   │
```

---

## 2. Add New Question

```
ADD QUESTION — QUANTITATIVE APTITUDE

  Question Type:    (●) MCQ (single correct)   ( ) MCQ (multiple)   ( ) Integer type

  Question Text:
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ A cistern can be filled by pipe A in 12 hours and by pipe B in 16 hours.   │
  │ If both pipes are opened together, how long will it take to fill the        │
  │ cistern if a leak at the bottom empties it in 48 hours?                    │
  └─────────────────────────────────────────────────────────────────────────────┘
  [Add image/formula]  [LaTeX preview]

  Options:
    (A) [8 hours           ]    (B) [9 hours 36 min    ]
    (C) [10 hours 24 min   ]    (D) [12 hours           ]

  Correct Answer:  ( A )  (●) B   ( C )   ( D )

  Solution:
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ Combined fill rate = 1/12 + 1/16 - 1/48 = (4+3-1)/48 = 6/48 = 1/8        │
  │ Time = 8 hours... Wait: re-check. A in 12, B in 16, leak 48.              │
  │ Net = 1/12 + 1/16 - 1/48 = 4/48 + 3/48 - 1/48 = 6/48 = 1/8  → 8 hrs     │
  │ Correct answer should be (A). Revising.                                    │
  └─────────────────────────────────────────────────────────────────────────────┘

  Metadata:
    Topic:       [Pipes & Cisterns ▼]
    Sub-topic:   [Combined work with leak ▼]
    Difficulty:  ( ) Easy  (●) Medium  ( ) Hard
    Exam target: [✓] SSC CGL  [✓] SSC CHSL  [ ] RRB  [✓] Banking
    Time (sec):  [90]  (avg time a student should take to solve)
    Source:      (●) Original   ( ) Adapted from: [_________________]

  [Save as Draft]   [Submit for Review]
```

---

## 3. Review Queue (Reviewer View)

```
QUESTION REVIEW QUEUE — Ms. Ananya Roy (Reviewer)
As of 30 March 2026

  Pending review: 42 questions (from 6 faculty)

  ┌────┬─────────────────────────────┬───────────┬────────────┬──────────────────┐
  │ #  │ Question (preview)          │ By        │ Topic      │ Action           │
  ├────┼─────────────────────────────┼───────────┼────────────┼──────────────────┤
  │ 1  │ A can do work in 6 days...  │ Mr. Suresh│ Time+Work  │ [Review] [Skip]  │
  │ 2  │ Find the value of x+y if...│ Ms. Divya │ Algebra    │ [Review] [Skip]  │
  │ 3  │ The income of A is 20%...   │ Mr. Arun  │ Percentage │ [Review] [Skip]  │
  └────┴─────────────────────────────┴───────────┴────────────┴──────────────────┘

REVIEW ACTIONS (per question):
  [✅ Approve]   [✏️ Request Revision: ________________]   [❌ Reject: ________]

  Rejection reasons (common):
  • Duplicate of existing question in bank
  • Incorrect answer key
  • Ambiguous wording
  • Difficulty mislabelled (marked Easy, actually Hard)
  • Not relevant to target exam pattern
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/qbank/?faculty={fid}&topic={t}` | Faculty's questions with filters |
| 2 | `POST` | `/api/v1/coaching/{id}/qbank/` | Submit new question |
| 3 | `PATCH` | `/api/v1/coaching/{id}/qbank/{qid}/` | Edit draft question |
| 4 | `GET` | `/api/v1/coaching/{id}/qbank/review-queue/` | Pending review (reviewer role) |
| 5 | `POST` | `/api/v1/coaching/{id}/qbank/{qid}/review/` | Approve / reject / request revision |
| 6 | `GET` | `/api/v1/coaching/{id}/qbank/stats/?faculty={fid}` | Faculty contribution stats |

---

## 5. Business Rules

- Every question must go through a two-stage process: faculty submission → reviewer approval; a faculty member cannot add questions directly to the live test bank; this quality gate prevents incorrect answer keys, ambiguous wording, and duplicate questions from appearing in student-facing tests; a test paper with an incorrect answer key causes student complaints, re-evaluation demands, and brand damage
- Question difficulty calibration must be data-driven post-launch; a question marked "Medium" by the faculty that only 28% of students answer correctly is actually a "Hard" question; EduForge recalibrates difficulty labels after a question has been used in at least 3 tests with 50+ attempts; the calibrated difficulty (based on actual student performance) replaces the faculty-assigned difficulty and is used for future test composition
- Intellectual property: all questions created by faculty using TCC's time, resources, and question bank are owned by TCC, not the individual faculty member; this must be documented in faculty employment contracts; a faculty member who leaves and attempts to use TCC's questions at a competitor institute is violating TCC's IP; EduForge's question bank maintains a creation timestamp and creator ID for every question, serving as evidence in IP disputes
- Question reuse tracking (the "Used in Tests" column) helps identify overused questions; a question used in more than 8 tests risks being memorised and shared in student groups (WhatsApp, Telegram); questions used more than 8 times should be retired to an archive and replaced with fresh variants; faculty are incentivised to contribute new questions with a monthly contribution leaderboard and quality bonus for high-rated questions
- LaTeX support in the question editor is mandatory for mathematical expressions (fractions, square roots, integration, geometry diagrams); questions where the formula is rendered as plain text (e.g., "sqrt(x^2+y^2)") are harder to read and more prone to misinterpretation; all quantitative and scientific questions must use LaTeX rendering; the question editor enforces LaTeX preview before submission

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division C*
