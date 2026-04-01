# K-03 — Academic Performance MIS

> **URL:** `/coaching/analytics/academic/`
> **File:** `k-03-academic-performance-mis.md`
> **Priority:** P2
> **Roles:** Academic Director (K5) · Branch Manager (K6) · Faculty (K2)

---

## 1. Academic Performance Overview

```
ACADEMIC PERFORMANCE MIS — AY 2025–26
As of 31 March 2026 | All Batches

  SCORE DISTRIBUTION (Full Mocks — Mar 2026, n=856 students):
    Score Range  │ Students │   %   │ Bar
    ─────────────┼──────────┼───────┼──────────────────────────────────
    180–200      │    24    │  2.8% │ ██
    160–179      │    96    │ 11.2% │ ████████
    140–159      │   184    │ 21.5% │ ████████████████
    120–139      │   248    │ 29.0% │ ████████████████████
    100–119      │   184    │ 21.5% │ ████████████████
    80–99        │    84    │  9.8% │ ███████
    <80          │    36    │  4.2% │ ███
    ─────────────┴──────────┴───────┴──────────────────────────────────
    MEAN: 142.1/200  │  MEDIAN: 139/200  │  SD: ±26.4
    Top 10% cutoff:  168/200  │  Bottom 10% cutoff: 108/200

  BATCH AVERAGE SCORES (Mock #25 — Apr 2026):
    SSC CGL Morning:   154.2/200 ↑
    SSC CGL Evening:   148.6/200 ↑
    IBPS PO Batch A:   138.4/200 →
    Online SSC CGL:    144.8/200 ↑
```

---

## 2. Subject-Wise Analysis

```
SUBJECT PERFORMANCE — All SSC CGL Students (n=276, Mock #25)

  Subject           │ Avg Score │ Max Possible │ % Score │ vs Mock #1 │ Trend
  ──────────────────┼───────────┼──────────────┼─────────┼────────────┼───────
  Quantitative Apt. │  35.8     │    50        │  71.6%  │ +8.4 pts   │ ↑
  English Language  │  38.2     │    50        │  76.4%  │ +6.2 pts   │ ↑
  Reasoning Ability │  36.4     │    50        │  72.8%  │ +7.8 pts   │ ↑
  General Awareness │  31.7     │    50        │  63.4%  │ +5.2 pts   │ ↑ (slow)
  ──────────────────┴───────────┴──────────────┴─────────┴────────────┴───────
  TOTAL             │  142.1    │   200        │  71.1%  │ +27.6 pts  │ ↑

  IMPROVEMENT HIGHLIGHTS:
    Top gainer (batch):    Vijay P. TCC-2418 — +68 pts (Mock#1:106 → #25:174)
    Most consistent:       Akhil K. TCC-2401 — σ 4.2 (lowest variance)
    GK improvement lagging: Ravi G. TCC-2411 — only +2.4 pts in GK
    Q needing support:     Caselet DI (avg 6.8/15) — lowest item score

  WEAK AREAS (batch average <65%):
    Caselet DI (Quant):        56.3% → Recommend: Targeted DI sessions
    Reading Comprehension:     63.8% → Recommend: Daily RC practice
    Static GK:                 58.2% → Recommend: GK worksheet series
```

---

## 3. Faculty Impact Report

```
FACULTY IMPACT ANALYSIS — Q3 AY 2025–26

  Faculty           │ Subject  │ Avg class score │ Score gain vs Q1 │ Rating │ Correlation
  ──────────────────┼──────────┼─────────────────┼──────────────────┼────────┼────────────
  Mr. Suresh K.     │ Quant    │    35.8/50      │   +8.4 pts       │ 4.3/5  │ r=0.72 ✅
  Ms. Kavita M.     │ English  │    38.2/50      │   +6.2 pts       │ 4.6/5  │ r=0.81 ✅
  Mr. Mohan R.      │ Reasoning│    36.4/50      │   +7.8 pts       │ 4.1/5  │ r=0.68 ✅
  Mr. Ravi S.       │ GK/CA    │    31.7/50      │   +5.2 pts       │ 3.8/5  │ r=0.59 🟡

  NOTE: Correlation (r) measures relationship between session attendance
  and score gain in that subject. Higher = stronger teaching impact.

  Mr. Ravi S.'s GK correlation is lower — students attending his sessions
  show less improvement than in other subjects. Review assigned for Apr 5.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/analytics/academic/scores/?batch={bid}&mock={mid}` | Score distribution for a mock |
| 2 | `GET` | `/api/v1/coaching/{id}/analytics/academic/subject-analysis/?batch={bid}` | Subject-wise performance breakdown |
| 3 | `GET` | `/api/v1/coaching/{id}/analytics/academic/faculty-impact/` | Faculty score impact correlation |
| 4 | `GET` | `/api/v1/coaching/{id}/analytics/academic/trends/?student={sid}` | Individual student trend |
| 5 | `GET` | `/api/v1/coaching/{id}/analytics/academic/weak-areas/?batch={bid}` | Weak areas requiring intervention |

---

## 5. Business Rules

- Academic MIS distinguishes between score level and score improvement; a student scoring 160/200 from the start is excellent but not necessarily improving; a student who went from 106 to 174 (+68 points) demonstrates the highest learning gain and is TCC's strongest evidence of teaching effectiveness; both metrics matter: the absolute score for exam readiness, and the improvement for attributing teaching impact; marketing uses both ("our average student improves by 27 points") but must not conflate them
- Subject correlation analysis (r-values) is used with caution; correlation does not imply causation — a lower GK correlation may reflect that GK is harder to teach (depends on self-study) rather than a teaching quality failure; the Academic Director uses the correlation as one input in faculty review, not as the sole metric; a faculty with r=0.59 is not automatically underperforming if GK inherently has a lower teachability coefficient across all coaching centres
- Score distributions are shared with students only at the aggregate level (e.g., "your percentile in the batch is 78th"); individual students do not see other students' raw scores; the distribution chart allows students to contextualise their performance without identifying peers; sharing individual scores without consent violates DPDPA 2023 privacy norms and would damage trust in the student community
- Weak area reports (Caselet DI at 56.3%, Static GK at 58.2%) directly drive the academic calendar; when MIS identifies a weak area, the Academic Director schedules targeted sessions, assigns practice worksheets, and tracks the improvement in the next mock; the connection between MIS output and academic action is what makes MIS useful — a report that is read and filed without action is wasted effort; each weak area report must have a named owner and a next-review date
- The academic MIS is prepared monthly by the Academic Director and reviewed with the Branch Manager; it is shared with individual faculty members in their quarterly review (B-07) — each faculty sees only their own subject's data, not others'; the Director receives the full MIS including franchise comparisons; franchise branches' academic performance is benchmarked against the main branch to identify systemic issues (if every branch shows low GK scores, it's a material problem, not a local teaching issue)

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division K*
