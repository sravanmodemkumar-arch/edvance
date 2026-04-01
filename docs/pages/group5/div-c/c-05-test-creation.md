# C-05 — Test Creation

> **URL:** `/coaching/faculty/tests/create/`
> **File:** `c-05-test-creation.md`
> **Priority:** P1
> **Roles:** Faculty (K2) · Test Series Coordinator (K4) · Course Head (K5)

---

## 1. Test Builder

```
CREATE TEST — Mr. Suresh Kumar
As of 30 March 2026

STEP 1: TEST DETAILS

  Test Name:       [SSC CGL Quant Sprint #18 — Mensuration & DI     ]
  Test Type:       (●) Subject Sprint  ( ) Full Mock  ( ) Chapter Test  ( ) GK Weekly
  Target Exam:     [SSC CGL ▼]
  Assign to Batch: [✓] SSC CGL Morning  [✓] SSC CGL Evening  [ ] Others
  Scheduled:       [05/04/2026  10:00]
  Duration:        [45] minutes
  Total Marks:     [50]
  Negative Marking:( ) None  (●) -0.25 per wrong  ( ) -0.5 per wrong

STEP 2: SECTION STRUCTURE

  Section 1: Mensuration (25 marks)
    Questions: 25  |  Marks per Q: 1  |  Negative: -0.25

  Section 2: Data Interpretation (25 marks)
    Questions: 25  |  Marks per Q: 1  |  Negative: -0.25

  [+ Add Section]

STEP 3: ADD QUESTIONS (Section 1 — Mensuration)

  Source:  (●) My question bank  ( ) TCC full bank  ( ) Manual add

  Auto-select by criteria:
    Topic:       [Mensuration ▼]   Sub-topics: [✓] 2D  [✓] 3D  [ ] Area formulas only
    Difficulty:  [ ] Easy(5)  [✓] Medium(15)  [✓] Hard(5)   Total: 25 ✅
    Exclude:     Questions used in last 4 tests  [✓]
    [Auto-Select 25 Questions]

  SELECTED QUESTIONS PREVIEW:
    Q1. A cone of radius 7cm and height 24cm... [Medium] [Mensuration-3D] [Used: 2×]
    Q2. The perimeter of a rectangle is...      [Easy]   [Mensuration-2D] [Used: 1×]
    Q3. A frustum with...                       [Hard]   [Mensuration-3D] [Used: 0×]
    ... (22 more)

  [Shuffle question order: ✓]  [Shuffle options: ✓]

STEP 4: REVIEW & PUBLISH

  Total questions: 50 | Total marks: 50 | Duration: 45 min
  Difficulty mix: Easy 10 (20%) | Medium 28 (56%) | Hard 12 (24%)
  Avg time per Q (from bank): 42 seconds (should fit in 45 min) ✅

  [Save as Draft]   [Submit for Review]   [Publish Immediately] (K4+ only)
```

---

## 2. Test Scheduling Calendar

```
TEST SCHEDULE — April 2026 (SSC CGL Batches)

  #  │ Test Name                    │ Date/Time       │ Duration │ Status
  ───┼──────────────────────────────┼─────────────────┼──────────┼──────────────
  1  │ Quant Sprint #18             │ Apr 5, 10:00    │ 45 min   │ ⬜ Draft
  2  │ English Sprint #12           │ Apr 6, 10:00    │ 45 min   │ ✅ Published
  3  │ SSC CGL Full Mock #24        │ Apr 7, 09:00    │ 60 min   │ ✅ Published
  4  │ GK Weekly #16                │ Apr 9, 08:00    │ 15 min   │ ✅ Published
  5  │ Reasoning Sprint #10         │ Apr 11, 10:00   │ 45 min   │ ⬜ Not started
  6  │ Full Mock #25 (Pre-Exam)     │ Apr 14, 09:00   │ 60 min   │ ⬜ Not started

  Gap check: ✅ No two tests on the same day for same batch
  Note: No new tests scheduled after Apr 18 (exam proximity rule)
```

---

## 3. Question Randomisation Settings

```
RANDOMISATION & ANTI-CHEATING SETTINGS

  Question order:    (●) Randomised per student  ( ) Fixed order
  Option order:      (●) Randomised per student  ( ) Fixed order
  Paper variants:    (●) Auto-generate 4 variants (A, B, C, D)
                         Each variant: same questions, different order
  Section lock:      (●) Students must complete Section 1 before Section 2
  Tab switch:        (●) Warn at 1st switch  (●) Flag at 2nd switch
                         (●) Auto-submit at 3rd switch
  Copy-paste:        (●) Disabled in test window
  Screen share:      (●) Blocked (browser restriction notified)
  Calculator:        (●) Basic calculator provided (for Banking tests)
                     ( ) No calculator (SSC/RRB tests — standard)
  Timer:             (●) Visible to student  ( ) Hidden
  Review answers:    ( ) After each question  (●) At end before submit  ( ) Disabled
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/coaching/{id}/tests/` | Create new test |
| 2 | `GET` | `/api/v1/coaching/{id}/tests/?faculty={fid}&status=draft` | My draft tests |
| 3 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/questions/auto-select/` | Auto-select questions by criteria |
| 4 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/publish/` | Publish test (K4+ only) |
| 5 | `GET` | `/api/v1/coaching/{id}/tests/schedule/?batch={bid}&month=2026-04` | Test calendar for batch |
| 6 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/preview/` | Preview test as student would see it |

---

## 5. Business Rules

- Faculty can create tests but cannot publish them; a Test Series Coordinator (K4) or Course Head (K5) must review and publish; this two-person approval ensures the test difficulty, marks distribution, and scheduling are consistent with the batch's curriculum progress; a faculty who publishes a test covering topics not yet taught damages student confidence and generates complaints
- The 4-variant auto-generation (A, B, C, D) is mandatory for all online tests; students in the same room or Zoom session see different question orders and cannot copy from their neighbour; the system assigns variants randomly; all variants are scored identically (same questions, different order) so variant assignment has no effect on a student's score
- Question exclusion rule (exclude questions used in the last 4 tests) prevents repetition which students memorise; a student who sees the same "Pipes & Cisterns" question in 3 consecutive tests doesn't learn — they just remember the answer; EduForge's auto-select algorithm respects the exclusion window; faculty who manually add a recently-used question receive a warning but can override with a reason
- Test timing calibration must be validated before publishing; if the average question time from the bank predicts 62 minutes for a 45-minute test, the test has too many time-consuming questions; either the time limit must be extended or the question count reduced; publishing an unreasonably timed test causes mass "time out" submissions and skews all performance analytics
- Tests cannot be rescheduled within 24 hours of the scheduled time; students who have prepared their schedule around a test time cannot adapt to last-minute changes; exceptions (power outage, platform maintenance) require Branch Manager approval and a 24-hour notice communication to all enrolled students via WhatsApp

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division C*
