# E-04 — Result Processing & Publication

> **URL:** `/coaching/tests/results/`
> **File:** `e-04-result-processing.md`
> **Priority:** P1
> **Roles:** Test Series Coordinator (K4) · Academic Director (K5)

---

## 1. Result Processing Queue

```
RESULT PROCESSING — Post-Test Queue
As of 5 April 2026, 11:05 AM

  TEST: SSC CGL Full Mock #25 | Ended: 11:00 AM | Processing started: 11:00:01

  PROCESSING STATUS:
    Step 1 — Collect all submissions:           ✅ Done (11:00:05)
    Step 2 — Apply cheat-flag review hold:      ✅ Done (3 students flagged — pending review)
    Step 3 — Auto-grade MCQs:                   ✅ Done (11:00:48) — 1,183 papers graded
    Step 4 — Apply negative marking:            ✅ Done (11:01:02)
    Step 5 — Generate raw score sheet:          ✅ Done (11:01:18)
    Step 6 — Normalisation (if applicable):     N/A (single-paper test — no normalisation needed)
    Step 7 — Rank calculation:                  ✅ Done (11:02:44)
    Step 8 — Question error check (manual):     ⏳ Pending (coordinator must review)
    Step 9 — Publish results:                   ⏳ Waiting for Step 8 sign-off

  ETA FOR PUBLICATION: 11:30 AM (pending coordinator review)
  [Review Flagged Questions →]   [Sign Off & Publish]
```

---

## 2. Score Sheet Preview

```
SCORE SHEET PREVIEW — Full Mock #25 (1,183 graded students)

  SCORE DISTRIBUTION:
    Range       │ Count │  %    │ Cumulative %
    ────────────┼───────┼───────┼──────────────
    160–200     │   28  │  2.4% │   2.4%  (Top performers)
    140–159     │   82  │  6.9% │   9.3%
    120–139     │  188  │ 15.9% │  25.2%
    100–119     │  286  │ 24.2% │  49.4%
    80–99       │  328  │ 27.7% │  77.1%
    60–79       │  198  │ 16.7% │  93.8%
    < 60        │   73  │  6.2% │ 100.0%
    ────────────┴───────┴───────┴──────────────
    Avg: 106.4 / 200  |  Median: 102  |  Top: 186/200  |  StdDev: 28.4

  NEGATIVE MARKING IMPACT:
    Total wrong answers:   48,242  (avg 40.8/student)
    NM deducted:           12,060.5 marks total (avg 10.2/student)
    Students scoring lower due to NM:  641/1,183 (54.2%) — would have scored higher without NM

  CHEAT-FLAGGED (held, not published):
    TCC-2801:  Unusual timing + duplicate IP — score 164 — held ⚠️
    TCC-2802:  Duplicate IP — score 142 — held ⚠️
    TCC-2408:  Screen share detected — score 178 — held ⚠️ (review required)
```

---

## 3. Result Publication

```
PUBLISH RESULTS — Full Mock #25

  Publish to:   (●) All enrolled students (auto, via portal + notification)
                ( ) Specific batches only

  Notification: (●) Push notification  (●) WhatsApp  ( ) Email only
  Message:
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ Your SSC CGL Full Mock #25 result is live! Check your score, rank,         │
  │ and topic-wise analysis on the TCC portal: tcc.eduforge.in/student         │
  │ Batch avg: 106.4/200 | Your score: [personalised per student]              │
  └─────────────────────────────────────────────────────────────────────────────┘

  LEADERBOARD:  (●) Publish batch rank  ( ) Hide ranks (practice-mode test)
  SOLUTIONS:    (●) Publish after results  ( ) Publish after 24 hrs (prevent sharing)

  CHEAT-FLAGGED: 3 students excluded from published results
                 → Coordinator review: [TCC-2801] [TCC-2802] [TCC-2408]
                 → Must resolve within 48 hours; students notified of hold reason

  [Publish Now]   [Schedule: 11:30 AM]   [Preview Student View]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/results/status/` | Processing status (step-by-step) |
| 2 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/results/preview/` | Score distribution before publication |
| 3 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/results/publish/` | Publish results to students |
| 4 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/results/cheat-flags/` | Cheat-flagged submissions |
| 5 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/results/cheat-flags/{sid}/resolve/` | Resolve cheat flag (clear or void) |
| 6 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/results/student/{sid}/` | Individual student result |

---

## 5. Business Rules

- Results must be published within 3 hours of test end for regular sprint tests and within 6 hours for full mocks; students who have just given a 2-hour test are anxious about their performance; delayed results create frustration and reduce trust in the platform; the processing pipeline is automated (grading, NM, rank) and typically completes in under 5 minutes; the remaining time is for the coordinator's manual sign-off on question errors and cheat flags; a coordinator who delays sign-off beyond 2 hours for a full mock must log a reason
- If a question is found to have an incorrect answer key after publishing, TCC's policy is to award marks to all students who selected any answer for that question (benefit of doubt) rather than re-grading with the correct key; re-grading after publication creates confusion ("my score changed") and trust issues; the "award to all" policy is simple, predictable, and prevents repeated recalculation demands; the question is also retired from the active bank immediately and flagged for correction
- Cheat-flagged students' scores are held but the students are notified that their result is "under review" within 1 hour of test end; they are not told the specific reason (tab-switch, duplicate IP) to protect the integrity of the review process; the coordinator has 48 hours to review and decide: clear the flag (score published normally) or void the score (student notified with reason and right to appeal to Academic Director); a student whose score is voided without a review is a legal and reputation risk
- Negative marking impact data (shown in coordinator preview) is not published to students directly; it is used internally to assess paper difficulty and question quality; however, students can see their own wrong answer count in their detailed result; the aggregate NM impact data (54.2% scored lower due to NM) informs question difficulty calibration and helps faculty understand whether their test was appropriately challenging
- The batch rank published alongside the score is relative rank within the batch, not across all TCC students; a student who scores 120/200 in the CGL Morning batch gets rank 68/240; the same student who enrolled in both an offline and online batch would have separate ranks per batch; TCC does not publish an all-India rank for internal mocks — that would require normalisation across all TCC students and could misrepresent performance given varying question difficulty per series

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division E*
