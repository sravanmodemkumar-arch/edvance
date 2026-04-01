# E-02 — Test Player (Exam Simulation Engine)

> **URL:** `/exam/mocks/{mock-id}/attempt/`
> **File:** `e-02-test-player.md`
> **Priority:** P1
> **Data:** `mock_test` + `question` + `mock_attempt` — renders any mock for any exam with the same player

---

## 1. Test Player Interface

```
TEST PLAYER — Universal Exam Simulator
[Same player renders SSC CGL, APPSC Group 2, IBPS PO, NEET, or any exam]

  ┌──────────────────────────────────────────────────────────────────────┐
  │  APPSC Group 2 — Prelims Mock #15                                    │
  │  Time Remaining: 01:42:18    │  Q: 48 / 150    │  Lang: [TE] [EN]   │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                      │
  │  SECTION: General Studies  (Q 1–75)                                  │
  │                                                                      │
  │  Q.48 —  కింది వాటిలో 73వ రాజ్యాంగ సవరణ ద్వారా ఏ వ్యవస్థ          │
  │          ప్రవేశపెట్టబడింది?                                         │
  │          Which of the following was introduced by the 73rd           │
  │          Constitutional Amendment?                                   │
  │                                                                      │
  │          (A) గ్రామ సభలు / Gram Sabhas                               │
  │          (●) పంచాయతీ రాజ్ / Panchayati Raj  ← selected              │
  │          (C) జిల్లా పరిషత్ / Zilla Parishad                        │
  │          (D) మున్సిపల్ కార్పొరేషన్ / Municipal Corporation          │
  │                                                                      │
  │  [★ Mark for Review]   [Clear Response]                              │
  ├──────────────────────────────────────────────────────────────────────┤
  │  QUESTION PALETTE:                                                   │
  │  ■ Answered (42)  □ Not Visited (68)  ★ Marked for Review (6)       │
  │  ■ Answered + Marked (3)  □ Not Answered (31)                        │
  │                                                                      │
  │  [1][2][3]…[48]…[75] | Section 2: [76]…[150]                        │
  ├──────────────────────────────────────────────────────────────────────┤
  │  [◄ Previous]       [Save & Next ►]       [Submit Test]             │
  └──────────────────────────────────────────────────────────────────────┘

  PLAYER ADAPTS TO EXAM PATTERN:
    SSC CGL (4 sections, 200 marks, 60 min):  section tabs + strict timer
    APPSC Group 2 (2 sections, 150 marks, 150 min):  2 section tabs
    IBPS PO (5 sections, sectional timing):  per-section countdown ⏰
    UPSC CSE (no sections, 100 Qs, 120 min):  no section tabs
    AP Police (1 section, 100 Qs, 90 min):   single section view
    → ALL rendered by same player, configured from mock_test.sections[]
```

---

## 2. Player Configuration (from mock_test record)

```
PLAYER CONFIGURATION — How the player adapts to any exam

  FROM mock_test RECORD:
    sections[] → renders section tabs (0 sections = no tabs, 5 sections = 5 tabs)
    duration_minutes → sets countdown timer
    total_questions → sets question palette size
    language[] → shows language toggle (1 lang = no toggle, 2+ = toggle visible)
    negative_marking → shows/hides "negative marking warning" in submit confirmation

  FROM exam_stage RECORD:
    sectional_timing → if true, each section has its own timer (IBPS style)
                       if false, single overall timer (SSC/APPSC style)

  EXAM-SPECIFIC BEHAVIOURS (configured, not hardcoded):
    Calculator:         shown if exam_stage.calculator_allowed = true (SSC Tier-II)
    Rough sheet:        shown if exam_stage.rough_sheet = true (digital notepad)
    Question booklet:   PDF reference shown if exam_stage.has_booklet = true
    Passage-based Qs:   rendered as group (passage + 5 Qs) if question.passage_id set

  RESULT:
    Zero exam-specific code in the player
    All behaviour configured from mock_test + exam_stage + question metadata
```

---

## 3. Attempt Data Model

```
mock_attempt {
  id,
  user_id,
  mock_test_id,
  started_at,
  submitted_at,           ← null if abandoned
  time_taken_seconds,
  responses[]: {
    question_id,
    selected_option_id (nullable),  ← null if not attempted
    marked_for_review,
    time_spent_seconds,    ← per-question time tracking
  },
  score,                   ← computed after submission
  correct, wrong, unattempted,
  percentile,              ← rank among all attempts for this mock
  section_scores[],        ← per-section breakdown
  status,                  ← "in_progress" | "submitted" | "abandoned"
}
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/exam/mocks/{mid}/start/` | Start attempt (creates mock_attempt, returns questions) |
| 2 | `PATCH` | `/api/v1/exam/mocks/attempt/{aid}/response/` | Save a response (auto-save every 30s) |
| 3 | `POST` | `/api/v1/exam/mocks/attempt/{aid}/submit/` | Submit test and trigger scoring |
| 4 | `GET` | `/api/v1/exam/mocks/attempt/{aid}/` | Get attempt status and config |

---

## 5. Business Rules

- The test player auto-saves responses every 30 seconds to prevent data loss from browser crashes, power failures, or accidental navigation; the `responses[]` array in `mock_attempt` is updated incrementally — each save only transmits the delta (questions answered since last save); a full 150-question mock with auto-save generates approximately 300 small API calls (one per answer + periodic saves); the backend must handle this efficiently without blocking the student's UI
- Per-question time tracking (`time_spent_seconds`) is the most valuable analytics signal; it reveals which questions took the longest (student struggled), which were answered instantly (student knew it or guessed), and which were skipped; this data powers the analysis page (E-03) and the study plan recommender; time tracking starts when a question is displayed and pauses when the student navigates away; multiple visits to the same question accumulate time
- Sectional timing (IBPS PO/Clerk exams use it) means the student cannot go back to a previous section after time expires; the player must enforce this strictly — if Section 1 has 20 minutes and the timer reaches 0, all unanswered questions in Section 1 are locked and the player moves to Section 2; this is different from SSC/APPSC where the student can navigate freely across sections within the overall time; the `sectional_timing` flag from `exam_stage` controls this behaviour
- The submit confirmation dialog shows: total answered, unanswered, marked for review, and a negative marking warning ("X wrong answers will result in −Y marks"); the student must explicitly confirm; auto-submission at timer expiry (when time runs out) submits the current state of `responses[]` without confirmation — the student loses the opportunity to review but all saved responses are scored
- The player must work reliably on mobile devices (80%+ of EduForge exam portal users are on Android); touch targets must be large enough (options, navigation buttons), the question palette must be scrollable, and the timer must be visible without scrolling; a student taking a 2.5-hour APPSC mock on their phone during a commute or at home (no laptop) must have an experience comparable to the actual CBT exam centre; the player is tested on 4-inch screens and 3G connections

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division E*
