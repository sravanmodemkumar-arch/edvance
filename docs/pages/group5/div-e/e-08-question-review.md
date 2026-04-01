# E-08 — Post-Test Question Review

> **URL:** `/coaching/tests/question-review/`
> **File:** `e-08-question-review.md`
> **Priority:** P2
> **Roles:** Test Series Coordinator (K4) · Faculty (K2) · Academic Director (K5)

---

## 1. Post-Test Review Queue

```
POST-TEST QUESTION REVIEW — Full Mock #25
Review window: 5 Apr 2026 – 7 Apr 2026  |  Raised by students: 18 challenges

  REVIEW QUEUE:
  #  │ Q#  │ Raised by         │ Claim                          │ Faculty     │ Status
  ───┼─────┼───────────────────┼────────────────────────────────┼─────────────┼────────────────
  1  │ Q58 │ TCC-2401 (Akhil)  │ Question from uncovered CA     │ GK — Ravi S │ ✅ Bonus awarded
  2  │ Q61 │ TCC-2402 (Priya)  │ PM speech quote needs source   │ GK — Ravi S │ ✅ Bonus awarded
  3  │ Q14 │ TCC-2428 (Pavan)  │ "Answer key wrong — see Arith."│ Quant— Suresh│ ⏳ Under review
  4  │ Q38 │ TCC-2403 (Ravi S) │ 5-variable seating: 2 possible │ Reason—Mohan│ ⏳ Under review
  5  │ Q19 │ TCC-2418 (Sravya) │ Two options grammatically OK   │ English—Kavita│⏳ Under review
  6  │ Q82 │ TCC-2408 (Anitha) │ CM of Jharkhand changed Dec 25 │ GK — Ravi S │ ⏳ Under review
  7  │ Q21 │ TCC-2405 (Karthik)│ Answer D is also valid inference│ English—Kavita│ ⏳ Under review
  ...  (11 more challenges)

  ⏳ 16 challenges pending review | Due: 7 Apr 2026, 11:59 PM
  Review SLA: All challenges must be resolved within 48 hours of test end
```

---

## 2. Question Challenge Detail

```
CHALLENGE REVIEW — Q14 (Quant — Mensuration 3D)

  QUESTION TEXT:
  "A frustum has slant height 13 cm, smaller radius 5 cm, larger radius 12 cm.
   Find its Total Surface Area."

  ANSWER KEY:  Option B — 1,170π cm²
  STUDENT CHALLENGE (TCC-2428, Pavan Reddy):
  "Sir, TSA = π(R+r)l + πR² + πr² = π(12+5)×13 + π×144 + π×25
   = 221π + 169π = 390π, not 1170π. I think the answer is option A (390π)."

  FACULTY REVIEW (Mr. Suresh Kumar — Quant):
    Reviewing student's working:
    TSA = π(R+r)l + πR² + πr²
        = π(17)(13) + 144π + 25π
        = 221π + 144π + 25π
        = 390π ✅ Student is CORRECT

    Answer key had π(R+r)l + π(R²+r²) without the r² term — TYPO in key entry.
    Correct answer: A (390π), not B (1,170π).

  FACULTY RECOMMENDATION:  Correct the answer key from B to A
  ACTION OPTIONS:
    (●) Correct answer key — regraded scores published  [Regraded: +2 pts for students who chose A]
    ( ) Award bonus to all  (use when ambiguous — not this case)
    ( ) Reject challenge   (student incorrect)

  [Submit Decision]  |  Impact: 386 students chose A — will gain +2 pts each

  REGRADE NOTIFICATION (auto):
  "Your score for Full Mock #25 has been updated (+2 marks). Reason: Q14 answer
   key corrected after faculty review. New score: [X]. — TCC Team"
```

---

## 3. Question Retirement

```
QUESTION BANK — Post-Review Actions (Full Mock #25)

  RETIRED QUESTIONS (this test):
    Q58 — GK: Feb Budget clause — Retired: Syllabus mismatch (covered post-test)
    Q61 — GK: PM speech detail — Retired: Factual inaccuracy in options
    Q14 — Quant: Mensuration TSA — Retired: Answer key error (corrected & re-tagged)

  QUESTIONS FLAGGED FOR REWORK (sent to faculty):
    Q19 — English: one-word substitution — ambiguous option wording
    Q38 — Reasoning: 5-var seating — second valid arrangement exists
    Q82 — GK: State CM — fact outdated (Dec 2025 change not reflected)

  QUESTION BANK HEALTH (this review):
    Correct & reusable:         94 / 100 (94%)
    Corrected & reusable:        1 / 100  (1%)
    Retired:                     3 / 100  (3%)
    Flagged for rework:          3 / 100  (3%)  → faculty must resubmit in 7 days
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/question-review/` | All challenges for a test |
| 2 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/question-review/{rid}/` | Challenge detail with faculty review |
| 3 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/question-review/{rid}/resolve/` | Resolve challenge (correct/bonus/reject) |
| 4 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/question-review/regrade/` | Regrade and re-publish results after key correction |
| 5 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/question-review/retired/` | Questions retired from this test |
| 6 | `POST` | `/api/v1/coaching/{id}/question-bank/{qid}/flag/` | Flag a question for rework in the bank |

---

## 5. Business Rules

- Every student has the right to challenge a question's answer key within 48 hours of result publication; challenges are submitted through the Student Portal (O-01) with a brief explanation and optionally a working/reference; the coordinator routes the challenge to the faculty who authored the question; the faculty must respond with a decision (correct key, award bonus, or reject) within 24 hours; a challenge with no faculty response within 24 hours is auto-escalated to the Academic Director
- Answer key corrections trigger automatic regrading of all submitted papers; the regraded results replace the original with a revision note ("score updated due to Q14 key correction"); all students who were affected (positively or negatively) receive a notification explaining the change; regrading that results in a rank change updates the leaderboard; coordinators cannot prevent a regrade once an answer key error is confirmed — retroactive fairness to all students is non-negotiable
- A faculty member whose question has 3 or more confirmed errors in a single month is required to complete a question-writing workshop; question errors (wrong answer key, ambiguous options, outdated facts) damage student trust; TCC's brand depends on accurate, high-quality test papers; recurring errors from a specific faculty signal a quality gap, not bad luck; the workshop is remedial, not disciplinary, but persistent errors after the workshop are addressed in the quarterly review
- Questions flagged for rework must be resubmitted within 7 days; flagged questions are removed from the active bank immediately and cannot appear in any test until resubmitted and approved; a faculty who does not resubmit within 7 days loses the question count from their bank contribution stats (C-04) for that period; the coordinator monitors the "pending resubmission" count in the question bank dashboard as a quality hygiene metric
- The entire challenge-review-regrade workflow is audited with timestamps, user IDs, and decision logs; if a student alleges that their challenge was ignored or dismissed unfairly, the Academic Director can review the full audit trail; the audit trail also protects faculty from false claims of "ignoring challenges"; TCC's internal disputes policy allows a student to escalate a rejected challenge to the Academic Director if they believe the faculty decision was wrong — but only with new evidence, not simply disagreement

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division E*
