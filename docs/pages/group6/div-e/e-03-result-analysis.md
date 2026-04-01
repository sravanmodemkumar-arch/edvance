# E-03 — Result & Detailed Analysis

> **URL:** `/exam/mocks/attempt/{attempt-id}/analysis/`
> **File:** `e-03-result-analysis.md`
> **Priority:** P1
> **Data:** `mock_attempt` + `question` + `syllabus_node` — analysis computed post-submission

---

## 1. Result Summary

```
MOCK RESULT — APPSC Group 2 Prelims Mock #15
Ravi Kumar | Submitted: 31 Mar 2026, 11:42 AM | Time: 142 min / 150 min

  ┌──────────────────────────────────────────────────────────────────────┐
  │  SCORE: 124 / 150        RANK: 4,820 / 84,200      %ile: 94.3%    │
  │  ✅ Correct: 98   ❌ Wrong: 32   ⬜ Unattempted: 20                  │
  │  Negative marks: −10.67   Net: 98 − 10.67 = 87.33 → scaled: 124   │
  │                                                                      │
  │  CUT-OFF BENCHMARK:                                                  │
  │    Projected cut-off (General): ~78/150                              │
  │    Your score: 124/150 — ✅ ABOVE projected cut-off by 46 marks     │
  │    Your rank among EduForge users: Top 5.7%                          │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Section-wise & Topic-wise Analysis

```
SECTION-WISE BREAKDOWN:
  Section              │ Attempted│ Correct│ Wrong│ Score  │ Accuracy│ Time
  ─────────────────────┼──────────┼────────┼──────┼────────┼─────────┼──────
  General Studies       │   68/75  │   58   │  10  │ 54.67  │  85.3%  │ 82 min
  Mental Ability        │   62/75  │   40   │  22  │ 32.67  │  64.5%  │ 60 min
  ─────────────────────┴──────────┴────────┴──────┴────────┴─────────┴──────

TOPIC-WISE BREAKDOWN (top + bottom performers):
  ┌──────────────────────────────────────────────────────────────────────┐
  │  STRONGEST TOPICS:                                                   │
  │  ✅ Indian Polity:        12/12 correct (100%) — 14 min             │
  │  ✅ Modern History:        8/9  correct (88.9%) — 10 min            │
  │  ✅ Coding-Decoding:       6/6  correct (100%) — 5 min              │
  │                                                                      │
  │  WEAKEST TOPICS:                                                     │
  │  ❌ AP Economy:            3/8  correct (37.5%) — 12 min  ← focus   │
  │  ❌ Data Interpretation:   4/10 correct (40.0%) — 18 min  ← focus   │
  │  ❌ Non-verbal Reasoning:  2/6  correct (33.3%) — 8 min   ← focus   │
  │                                                                      │
  │  SKIPPED TOPICS:                                                     │
  │  ⬜ Science & Tech:        4 unattempted — ran out of time           │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Question-level Review

```
QUESTION REVIEW — Q.48

  Q.48  Which of the following was introduced by the 73rd Amendment?
        (A) Gram Sabhas
        (B) Panchayati Raj  ← YOUR ANSWER ✅ CORRECT
        (C) Zilla Parishad
        (D) Municipal Corporation

  TIME SPENT: 45 seconds
  DIFFICULTY: Easy (82% of test takers got this right)
  TOPIC: Indian Polity → Constitutional Amendments

  EXPLANATION:
    The 73rd Constitutional Amendment Act, 1992, provided constitutional status
    to the Panchayati Raj system. It added Part IX and Schedule 11 to the
    Constitution. Gram Sabhas (A) were part of Panchayati Raj but existed before.
    Municipal Corporations (D) were covered by the 74th Amendment.

  [Bookmark this question]  [Report error in question/answer]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/mocks/attempt/{aid}/result/` | Score, rank, percentile |
| 2 | `GET` | `/api/v1/exam/mocks/attempt/{aid}/analysis/sections/` | Section-wise breakdown |
| 3 | `GET` | `/api/v1/exam/mocks/attempt/{aid}/analysis/topics/` | Topic-wise accuracy |
| 4 | `GET` | `/api/v1/exam/mocks/attempt/{aid}/review/` | Question-by-question review with explanations |

---

## 5. Business Rules

- The analysis page is where mock tests deliver their educational value; the score alone (124/150) tells the aspirant very little; the topic-wise breakdown ("AP Economy: 37.5% accuracy") tells them exactly where to focus next; the time analysis ("Data Interpretation: 18 min for 10 Qs = 1.8 min/Q vs 1.0 min/Q target") reveals speed bottlenecks; the analysis converts a test-taking activity into a diagnostic activity; this is the primary reason aspirants subscribe — they can take free mocks elsewhere but EduForge's analysis depth is the differentiator
- Rank and percentile are computed against ALL users who attempted this specific mock (not just today's attempts); a mock with 84,200 lifetime attempts has a robust distribution; the aspirant's rank of 4,820 / 84,200 (94.3%ile) is meaningful because the comparison pool is large; for a newly published mock with only 200 attempts, the percentile is less reliable — the system adds a note: "Percentile based on 200 attempts so far — accuracy improves as more users attempt"
- Explanations for every question are the content team's largest investment per mock; a 150-question mock requires 150 well-written explanations (in Telugu + English = 300 explanations); explanations must cite the source (e.g., "Article 243 of the Constitution") and not just state the answer; an explanation that says "B is correct" without saying why is useless for learning; the content team's explanation quality is reviewed by subject experts; aspirant ratings on explanations ("Was this helpful? 👍 👎") feed back into content quality metrics
- The "Report error" button on each question is critical for quality assurance at scale; with 18,40,000 questions in the bank, errors are inevitable (wrong answer marked as correct, ambiguous question text, outdated data); each report creates a content team ticket; a question with 3+ error reports is flagged for urgent review; if confirmed as an error, the question is either corrected (with re-scoring of affected attempts) or retired; re-scoring updates the aspirant's score and rank retroactively — they receive a notification: "Your score for Mock #15 has been updated from 124 to 125 due to an answer key correction"
- The analysis page directly feeds the study plan (A-05) and recommendation engine (D-04); weak topics identified here (AP Economy at 37.5%) are flagged in the aspirant's My Exams dashboard and used to prioritise study material and practice questions; the connection is automatic — the aspirant does not need to manually note their weak topics and then search for material; the system does this: "Your AP Economy accuracy is 37.5% — here are 84 practice questions and 4 video lectures on AP Economy → [Start Practice]"

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division E*
