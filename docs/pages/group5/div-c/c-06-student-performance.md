# C-06 — Student Performance (Faculty View)

> **URL:** `/coaching/faculty/student-performance/`
> **File:** `c-06-student-performance.md`
> **Priority:** P2
> **Roles:** Faculty (K2) — subject-restricted view

---

## 1. Subject Performance Overview

```
STUDENT PERFORMANCE — Quantitative Aptitude
Mr. Suresh Kumar | SSC CGL Morning Batch | Last 5 Tests

BATCH OVERVIEW (236 students, last 5 tests):

  Test               │ Date    │ Avg/25 │ Top  │ <10/25 │ Median │ StdDev
  ───────────────────┼─────────┼────────┼──────┼────────┼────────┼───────
  Full Mock #23      │ 15 Mar  │ 16.4   │ 24   │  18    │ 17     │ 3.8
  Quant Sprint #17   │ 10 Mar  │ 15.8   │ 23   │  22    │ 16     │ 4.1
  Full Mock #22      │ 28 Feb  │ 15.2   │ 23   │  26    │ 15     │ 4.0
  Quant Sprint #16   │ 22 Feb  │ 14.6   │ 22   │  30    │ 15     │ 4.2
  Full Mock #21      │ 15 Feb  │ 14.2   │ 22   │  34    │ 14     │ 4.4
  ───────────────────────────────────────────────────────────────────────
  Trend: +2.2 points over 5 tests ✅ Improving | StdDev decreasing ✅
```

---

## 2. Topic Accuracy Heatmap

```
TOPIC ACCURACY — SSC CGL Morning (March 2026, 236 students)

  Topic                  │ Qs/Mock │ Accuracy │ vs Feb  │ Flag
  ───────────────────────┼─────────┼──────────┼─────────┼────────────────────
  Percentage             │   2–3   │  78.4%   │ +2.1%   │ ✅ Strong
  Profit & Loss          │   2–3   │  74.6%   │ +1.8%   │ ✅ Strong
  Time & Work            │   2–3   │  71.2%   │ +3.4%   │ ✅ Improving
  Simple / Comp. Interest│   1–2   │  68.8%   │ +0.4%   │ ✅ OK
  Ratio & Proportion     │   1–2   │  72.4%   │ +1.2%   │ ✅ OK
  Time, Speed, Distance  │   2–3   │  66.2%   │ -0.8%   │ ⚠️ Slight drop
  Mensuration 2D         │   2–3   │  64.8%   │ +4.2%   │ ✅ (was weak — improved)
  Mensuration 3D         │   1–2   │  52.4%   │ +8.6%   │ ⚠️ Still below 60%
  Data Interpretation    │   5–8   │  61.2%   │ +1.6%   │ ⚠️ Needs work
  Caselet DI             │   0–2   │  38.2%   │ -2.4%   │ 🔴 Critical gap
  Algebra                │   2–3   │  70.4%   │ +2.0%   │ ✅ OK
  Number Series          │   2–3   │  74.8%   │ +1.4%   │ ✅ Strong

  🔴 Caselet DI: only 38.2% — not covered enough. Adding 2 sessions in April.
```

---

## 3. Individual Student View (Faculty — Subject Only)

```
STUDENT: Akhil Kumar (TCC-2401) — Quant Performance Only

  Overall Quant scores (last 5 tests):
    Feb 15: 22/25 | Feb 22: 23/25 | Feb 28: 23/25 | Mar 10: 24/25 | Mar 15: 24/25
  Trend: ↑ Strong → consistently scoring 88–96%
  Rank in batch (Quant): #2 / 236

  WEAK TOPICS:
  • Caselet DI: 2/8 in last 3 tests (25%) — recommended: extra practice set
  • Trigonometry: 1/3 (33%) — only 1 question per test; not statistically significant

  NOTE: Faculty can see only Quant scores for this student.
        Reasoning, English, GK scores visible only to Batch Coordinator.
        Overall mock score visible only to Batch Coordinator and Counsellor.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/performance/faculty/{fid}/subject/?batch={bid}` | Subject accuracy overview |
| 2 | `GET` | `/api/v1/coaching/{id}/performance/faculty/{fid}/topics/?batch={bid}` | Topic-wise accuracy heatmap |
| 3 | `GET` | `/api/v1/coaching/{id}/performance/student/{sid}/subject/{subj}/` | One student's subject performance |
| 4 | `GET` | `/api/v1/coaching/{id}/performance/faculty/{fid}/trend/?tests=5` | Score trend over last N tests |

---

## 5. Business Rules

- Faculty access to student performance is strictly limited to their own subject; a Quant faculty cannot see a student's Reasoning or English scores; this subject-scoped view prevents faculty from making holistic judgements about students based on incomplete information ("Ravi is weak in English too — he'll never clear CGL") that are not within their domain; holistic student assessment is the Counsellor's role
- Topic accuracy below 50% in any topic covered by the faculty is a teaching accountability signal; if 38% of students can't solve Caselet DI questions despite the faculty claiming the topic was covered, either the teaching was inadequate or insufficient practice was provided; the faculty must take corrective action (additional session, new practice sets) without waiting for the Academic Director to notice
- The "standard deviation" metric in the batch overview is a teaching quality indicator; a high StdDev means the batch has a wide performance spread (some students doing very well, others very poorly); a decreasing StdDev over time indicates the faculty is successfully bringing weaker students up while maintaining strong students — which is the sign of quality batch teaching, not just top-student performance
- Individual student weakness data visible to faculty must only be used for academic improvement, not for any other purpose; faculty cannot share individual student performance data with parents, other staff, or external parties; any performance communication to parents must go through the Batch Coordinator or Counsellor role; this maintains the student's data privacy and prevents faculty from creating direct parent relationships that bypass institute communication channels
- Faculty performance data (their students' scores) is used in their quarterly review (C-07 Quality Review, B-07); a faculty who consistently shows topic-level improvements in their subject across batches has measurable impact; this objective data protects faculty who are technically strong from subjective student ratings that may be influenced by personality; both ratings and score improvements are used together in the Academic Director's evaluation

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division C*
