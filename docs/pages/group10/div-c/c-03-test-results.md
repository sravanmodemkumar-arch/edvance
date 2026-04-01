# C-03 — Test Results & Solution Review

> **URL:** `/student/tests/{test_id}/result`
> **File:** `c-03-test-results.md`
> **Priority:** P1
> **Roles:** Student (S2–S6) · Parent (score summary for minors)

---

## Overview

Post-test analysis — the page students spend the most time on after the test-taking interface itself. Shows score, rank, section-wise breakdown, question-by-question review with correct answers and detailed explanations, time analysis per question, and comparison with toppers. The result page is the primary learning surface — students learn more from reviewing mistakes than from taking more tests. Free students see score + rank; Premium students get full question-level analysis, time tracking, and topper comparison.

---

## 1. Result Summary

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  TEST RESULT — JEE Mains Mock #25                                            │
│  Submitted: 01-Apr-2026, 12:48 PM · Duration: 2h 48m / 3h 00m              │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐│
│  │ 📊 Score     │  │ 🏆 AIR       │  │ 📈 %ile      │  │ ✅ Accuracy     ││
│  │ 204 / 300    │  │ 3,847        │  │ 97.91        │  │ 82.3%           ││
│  │ ↑ from 198   │  │ ↑ from 4,231 │  │ ↑ from 97.70 │  │ 58 of 70 att.  ││
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘│
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  Section Breakdown                                                     │  │
│  │  ┌──────────────────┬──────┬──────┬────────┬────────┬───────────────┐ │  │
│  │  │ Section          │ Score│ Max  │ Correct│ Wrong  │ Section Rank  │ │  │
│  │  ├──────────────────┼──────┼──────┼────────┼────────┼───────────────┤ │  │
│  │  │ Physics          │  72  │ 100  │ 20     │ 3      │ 4,102         │ │  │
│  │  │ Chemistry        │  48  │ 100  │ 14     │ 6      │ 11,847        │ │  │
│  │  │ Mathematics      │  84  │ 100  │ 24     │ 4      │ 2,198         │ │  │
│  │  ├──────────────────┼──────┼──────┼────────┼────────┼───────────────┤ │  │
│  │  │ TOTAL            │ 204  │ 300  │ 58     │ 13     │ AIR 3,847     │ │  │
│  │  └──────────────────┴──────┴──────┴────────┴────────┴───────────────┘ │  │
│  │                                                                       │  │
│  │  Unattempted: 4 · Marked for review: 3 (2 were correct)             │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [Download Rank Card ↓]  [Share Result →]  [View Detailed Analysis ↓]      │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Question-by-Question Review (Premium)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  SOLUTION REVIEW — Physics                          [All ▼] [Wrong only]    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  Q.12  ✅ Correct  (+4 marks)  Time: 2m 15s (avg: 2m 48s)           │  │
│  │  ─────────────────────────────────────────────────────────────────   │  │
│  │  A block of mass 2 kg is placed on a frictionless inclined plane     │  │
│  │  making an angle of 30° with horizontal. Find minimum F...           │  │
│  │                                                                       │  │
│  │  Your answer: (A) 11.55 N  ✅                                        │  │
│  │  Correct answer: (A) 11.55 N                                         │  │
│  │                                                                       │  │
│  │  [Show Solution ▼]                                                    │  │
│  │  ┌────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Solution:                                                      │  │  │
│  │  │  For equilibrium on the incline:                                │  │  │
│  │  │  F cos30° = mg sin30°                                           │  │  │
│  │  │  F × (√3/2) = 2 × 10 × (1/2) = 10                            │  │  │
│  │  │  F = 10 / (√3/2) = 20/√3 = 11.55 N                           │  │  │
│  │  │                                                                 │  │  │
│  │  │  Topic: Mechanics — Laws of Motion on Inclined Plane           │  │  │
│  │  │  Difficulty: Medium · 68% students got this correct            │  │  │
│  │  │  📺 Related video: "Inclined Plane Problems" [Watch 8m →]     │  │  │
│  │  └────────────────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  Q.15  ❌ Incorrect  (-1 mark)  Time: 4m 32s (avg: 2m 48s) ⚠️ Slow │  │
│  │  ─────────────────────────────────────────────────────────────────   │  │
│  │  A Carnot engine operating between temperatures T₁ = 600K and       │  │
│  │  T₂ = 300K. Find the efficiency...                                  │  │
│  │                                                                       │  │
│  │  Your answer: (B) 40%  ❌                                            │  │
│  │  Correct answer: (C) 50%                                             │  │
│  │                                                                       │  │
│  │  [Show Solution ▼]                                                    │  │
│  │  ┌────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Solution:                                                      │  │  │
│  │  │  Carnot efficiency = 1 - T₂/T₁ = 1 - 300/600 = 0.5 = 50%    │  │  │
│  │  │  Common mistake: Using T₁-T₂/T₁ without proper notation.      │  │  │
│  │  │                                                                 │  │  │
│  │  │  Topic: Thermodynamics — Carnot Cycle 🔴 (your weak topic)    │  │  │
│  │  │  Difficulty: Easy · 84% students got this correct              │  │  │
│  │  │  ⚠️ You spent 4m 32s — this is a 1-step formula question.    │  │  │
│  │  │  📺 Related video: "Carnot Engine in 10 min" [Watch →]       │  │  │
│  │  │  📝 Practice: 10 similar questions [Start →]                  │  │  │
│  │  └────────────────────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Showing 2 of 25 Physics questions · [Load All →]                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Time Analysis (Premium)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  TIME ANALYSIS                                       [Premium ⭐ Feature]    │
│                                                                              │
│  Total time: 2h 48m / 3h 00m · Avg per question: 2m 14s                   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  Time Distribution by Outcome                                         │  │
│  │                                                                       │  │
│  │  ┌────────────────────────────────┐ ┌──────────────────────────────┐ │  │
│  │  │ Correct answers    1h 42m     │ │ Avg time: 1m 46s            │ │  │
│  │  │ ████████████████████████████  │ │ vs Topper avg: 1m 32s       │ │  │
│  │  └────────────────────────────────┘ └──────────────────────────────┘ │  │
│  │  ┌────────────────────────────────┐ ┌──────────────────────────────┐ │  │
│  │  │ Wrong answers      48m        │ │ Avg time: 3m 42s            │ │  │
│  │  │ ██████████████                │ │ ⚠️ Spending too long on Qs  │ │  │
│  │  └────────────────────────────────┘ │    you got wrong            │ │  │
│  │  ┌────────────────────────────────┐ └──────────────────────────────┘ │  │
│  │  │ Unattempted        18m        │                                  │  │
│  │  │ █████                         │ Left 4 Qs unattempted            │  │
│  │  └────────────────────────────────┘                                  │  │
│  │                                                                       │  │
│  │  ── SLOWEST QUESTIONS (time sinks) ───────────────────────────────  │  │
│  │  Q.42 Chemistry: 6m 12s (wrong) — Organic mechanism question       │  │
│  │  Q.15 Physics:   4m 32s (wrong) — Carnot efficiency (easy!)        │  │
│  │  Q.68 Maths:     4m 08s (correct) — Integration (tough but solved)  │  │
│  │                                                                       │  │
│  │  AI tip: "You spent 48 min on 13 wrong answers. If you had           │  │
│  │  skipped after 2 min each, you'd have saved 22 min — enough to       │  │
│  │  attempt the 4 questions you left blank."                             │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/student/tests/{test_id}/result` | Result summary (score, rank, sections) |
| 2 | `GET` | `/api/v1/student/tests/{test_id}/result/questions` | All questions with answers + solutions |
| 3 | `GET` | `/api/v1/student/tests/{test_id}/result/questions?filter=wrong` | Only incorrect questions |
| 4 | `GET` | `/api/v1/student/tests/{test_id}/result/time-analysis` | Time spent per question (Premium) |
| 5 | `GET` | `/api/v1/student/tests/{test_id}/result/topper-comparison` | Your answers vs topper's (Premium) |
| 6 | `GET` | `/api/v1/student/tests/{test_id}/result/topic-breakdown` | Result grouped by topic (Premium) |
| 7 | `POST` | `/api/v1/student/tests/{test_id}/result/questions/{q_id}/practice-similar` | Generate practice set of similar Qs |

---

## 5. Business Rules

- Results are published at different timings based on test type: (a) on-demand tests — instant results upon submission (score + rank calculated within 2 seconds), (b) scheduled domain mocks (SSC Mega Mock) — results published 30 minutes after the test window closes to ensure all students are ranked together, (c) institution-scheduled tests — results released when the institution admin publishes them (may be delayed by days for manual verification); the result page shows "Results pending — estimated release: [time]" for delayed results.

- Question-by-question review with solutions is a **Premium feature** — Free students see their score, rank, and section breakdown, but solutions and explanations require Premium; the "Show Solution" area for Free students displays a blurred preview with "Upgrade to see full solutions — ₹299/month"; this is the second-highest Premium conversion surface (22% of upgrades) because the moment a student gets a question wrong and wants to understand why is the highest-intent moment for learning.

- Each solution includes: (a) step-by-step working, (b) the topic and sub-topic tag, (c) difficulty level, (d) percentage of students who got it correct (discriminative ability), (e) a link to a related video explanation, and (f) a "Practice 10 similar questions" button that generates a mini practice set from the question bank filtered by the same topic and difficulty; this connects the test result directly to remedial action — the student doesn't just see they were wrong, they understand why and have an immediate path to improvement.

- Time analysis flags questions where the student spent significantly more time than the average — a 4-minute answer on an "Easy" 1-step formula question (like Carnot efficiency) is flagged as a time sink; the AI insight at the bottom calculates the "wasted time" (time spent on wrong answers beyond a 2-minute skip threshold) and shows how many additional questions could have been attempted with that time; this trains students in time management, which is often the difference between qualifying and not in competitive exams.

- The topper comparison (Premium) shows anonymised data — the student sees "Topper attempted Q.15 in 48 seconds and chose (C)" but not who the topper is; this helps students benchmark their approach against the best performer; for questions where the student and topper both got the answer correct, the time comparison is most instructive — if the student took 3 minutes and the topper took 45 seconds, there's a more efficient method to learn.

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division C*
