# A-05 — My Exams

> **URL:** `/exam/my-exams/`
> **File:** `a-05-my-exams.md`
> **Priority:** P1
> **Data:** `user_exam_profile` · `exam` · `mock_attempt` · `syllabus_coverage` · `notification`

---

## 1. My Exams Dashboard

```
MY EXAMS — Ravi Kumar
Graduate · Age 24 · OBC · Domicile: Andhra Pradesh · Language: Telugu

  ┌──────────────────────────────────────────────────────────────────────┐
  │  ACTIVE EXAMS (3)       SAVED / WATCHLIST (4)      COMPLETED (2)    │
  └──────────────────────────────────────────────────────────────────────┘

  ── ACTIVE (preparing for) ────────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │  APPSC GROUP 2 — 2025                          STATE | AP | TE   │
  │  Exam date: Aug 2026 (tentative) — 152 days away                 │
  │                                                                   │
  │  PREPARATION SNAPSHOT:                                            │
  │  Syllabus:  ████████████░░░░░░░░  68%  (31/46 topics done)       │
  │  Mock avg:  124/200  |  Best: 138  |  Rank: 4,820 / 4,28,000     │
  │  Weak areas:  AP Economy  ·  Medieval AP History  ·  Physics      │
  │  Last activity:  Mock #14 — 29 Mar 2026 (2 days ago)             │
  │                                                                   │
  │  UPCOMING:  Mock #15 available  |  AP Economy topic notes ready   │
  │  APPLICATION: Submitted ✅ — Regd No: APPSC-2025-G2-482840       │
  │                                                                   │
  │  [Continue Prep]  [Take Mock]  [View Syllabus]  [Remove]         │
  ├───────────────────────────────────────────────────────────────────┤
  │  SSC CGL — 2026                              CENTRAL | EN / HI   │
  │  Exam date: Jul–Aug 2026 — 120 days away                         │
  │                                                                   │
  │  Syllabus:  █████████░░░░░░░░░░░  45%  (18/40 topics done)       │
  │  Mock avg:  138/200  |  Best: 152  |  Rank: 2,14,000 / 36,40,000 │
  │  Weak areas:  Caselet DI  ·  Error Detection  ·  Static GK       │
  │  APPLICATION: Open — Apply by 30 Jun 2026 ⏰                     │
  │  [Apply Now] ← Action required!                                   │
  │                                                                   │
  │  [Continue Prep]  [Take Mock]  [Apply Now]  [Remove]             │
  ├───────────────────────────────────────────────────────────────────┤
  │  TS POLICE CONSTABLE — 2025                    STATE | TS | TE   │
  │  Physical test: Apr 20, 2026 — 20 days away ⚠️                   │
  │                                                                   │
  │  Written result: ✅ Cleared (Score: 68/100, Rank: 12,840)        │
  │  Physical prep:  Physical measurement (height/weight/chest) done  │
  │  Running: Target 100m in 15s — Current best: 15.8s 🟡           │
  │  APPLICATION: Submitted ✅                                         │
  │                                                                   │
  │  [Physical Prep Guide]  [View Admit Card]  [Remove]              │
  └───────────────────────────────────────────────────────────────────┘

  ── SAVED / WATCHLIST (not yet preparing) ─────────────────────────────

  VRO/VRA AP 2025 · TSPSC Group 3 2026 · IBPS Clerk 2026 · AP DSC 2026
  [View all saved exams →]

  ── COMPLETED ─────────────────────────────────────────────────────────
  TSPSC Group 4 2023 — Not selected (cutoff missed by 4 marks)
  AP Police Constable 2022 — Selected ✅ (awaiting joining)
```

---

## 2. Exam-Level Progress Tracker

```
PROGRESS DETAIL — APPSC Group 2 2025
[Drill-down within My Exams]

  SYLLABUS COVERAGE  [from syllabus_nodes × user_topic_progress]
    Paper 1 — General Studies         72%  ████████████████░░░░
      Indian History                  90%  ██████████████████░░
      AP & TS History                 55%  ███████████░░░░░░░░░  ← do this
      Indian Polity                   85%
      AP Economy                      40%  ████████░░░░░░░░░░░░  ← weak
      Geography (India + AP/TS)       80%
      Science & Technology            70%
    Paper 2 — General English/Telugu  68%  █████████████░░░░░░░
    Paper 3 — Mental Ability          60%  ████████████░░░░░░░░

  MOCK TEST HISTORY (APPSC Group 2):
    Mock #   │ Date       │ Score    │ Rank    │ Percentile │ Change
    ─────────┼────────────┼──────────┼─────────┼────────────┼────────
    Mock 1   │ 15 Nov 25  │  96/200  │ 28,420  │  93.4%     │  —
    Mock 5   │ 20 Dec 25  │ 108/200  │ 18,640  │  95.6%     │  ↑
    Mock 10  │ 25 Jan 26  │ 116/200  │ 10,280  │  97.6%     │  ↑
    Mock 14  │ 29 Mar 26  │ 124/200  │  4,820  │  98.9%     │  ↑

  MY STUDY PLAN (AI-generated, editable):
    Today (Apr 1):   AP Economy — Chapter 3: Industrial Policy (Notes)
    Apr 2:           AP Economy — Chapter 4: Agriculture Schemes (Notes)
    Apr 3:           Mock Test #15 — Full Length APPSC Group 2
    Apr 5–6:         Medieval AP History — Vijayanagara Empire
    Apr 7:           Sectional test — AP Economy (10 Qs)
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/my-exams/` | All exams for logged-in user (active + saved + completed) |
| 2 | `POST` | `/api/v1/exam/my-exams/` | Add exam to My Exams (`{ exam_id, status: active|saved }`) |
| 3 | `GET` | `/api/v1/exam/my-exams/{exam_id}/progress/` | Syllabus coverage + mock history for this exam |
| 4 | `PATCH` | `/api/v1/exam/my-exams/{exam_id}/` | Update status (active → completed, save application number) |
| 5 | `DELETE` | `/api/v1/exam/my-exams/{exam_id}/` | Remove exam from My Exams |
| 6 | `GET` | `/api/v1/exam/my-exams/study-plan/` | AI-generated study plan across all active exams |

---

## 5. Business Rules

- Syllabus coverage is computed per exam: `user_topic_progress` stores a record for each `(user_id, syllabus_node_id)` with a completion percentage; the exam-level coverage is the weighted average across all `syllabus_nodes` for that exam, weighted by `weightage`; a topic with 15% weightage (Caselet DI in SSC CGL Quant) contributes more to the coverage score than a 2% weightage topic; this prevents a false sense of completion where a student has "finished 90% of topics" but the remaining 10% is 40% of the exam's marks
- Mock rank shown (2,14,000 / 36,40,000 for SSC CGL) is relative to all EduForge users who attempted that mock, not the actual exam applicant pool; EduForge's user base skews toward more motivated aspirants (those who proactively use a preparation platform); the actual exam rank for a score of 138/200 may be different from EduForge's mock rank for the same score; the UI displays "EduForge rank" with a tooltip explaining the difference; the rank predictor (F-03) converts mock performance to estimated actual exam rank using historical correlation data
- "Weak areas" flagged in My Exams are identified from: (a) topic-wise score in mock analysis below the user's overall percentile; (b) topics where the user has 0% syllabus coverage; (c) topics where error rate in sectional tests is > 40%; weak areas are updated after every mock attempt; a topic that was weak but improved to 75% accuracy in the latest mock is removed from weak areas; weak areas drive both the study plan and the recommendation for next content to consume (G-01 study material)
- Multi-exam study plans (user preparing for APPSC Group 2 AND SSC CGL simultaneously) create scheduling conflicts; the AI study planner allocates prep time based on: days remaining to each exam, current coverage gap, mock score gap vs expected cut-off, and user's past daily study hours (inferred from session data); when APPSC Group 2 is 152 days away and SSC CGL is 120 days away, and SSC application needs action, SSC gets priority in the near-term plan; the planner adapts when dates change (exam postponed) without user intervention
- Application number field in My Exams (`Regd No: APPSC-2025-G2-482840`) is user-entered; EduForge stores it as a reference for the user's own records — it is not validated against APPSC's database; storing application numbers in My Exams reminds aspirants of their registration details without having to dig through emails; this field is personal to the user and is encrypted at rest; EduForge does not share application numbers with third parties or use them for any purpose other than displaying back to the user

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division A*
