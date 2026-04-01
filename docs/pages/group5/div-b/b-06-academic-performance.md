# B-06 — Academic Performance Reports

> **URL:** `/coaching/academic/performance/`
> **File:** `b-06-academic-performance.md`
> **Priority:** P1
> **Roles:** Academic Director (K6) · Course Head (K5) · Branch Manager (K6)

---

## 1. Cross-Batch Performance Dashboard

```
ACADEMIC PERFORMANCE DASHBOARD — March 2026

BATCH COMPARISON — Last Full Mock (SSC CGL Mock #23, 15 Mar 2026):

  Batch                  │ Students │ Avg  │ Top Score │ >150/200 │ <100/200 │ vs Feb
  ───────────────────────┼──────────┼──────┼───────────┼──────────┼──────────┼────────
  SSC CGL Morning (Main) │   236    │  162 │   192     │  78 (33%)│  22 (9%) │ +4 ✅
  SSC CGL Evening (Dilsk)│   172    │  154 │   187     │  54 (31%)│  31(18%) │ -8 ⚠️
  SSC CHSL Morning (Main)│   178    │  141 │   172     │  38 (21%)│  28(16%) │ +2 ✅
  RRB NTPC Weekend (Main)│   314    │  158 │   190     │  98 (31%)│  42(13%) │ +6 ✅
  Banking Morning (Main) │   196    │  158 │   188     │  62 (32%)│  18 (9%) │ +3 ✅
  Foundation 9-10        │   118    │  78% │   96%     │  — (%)   │  — (%)   │ +2% ✅

OVERALL TREND — SSC CGL (3-month):
  Jan 2026:  avg 150/200 | Feb 2026: avg 158/200 | Mar 2026: avg 162/200 ← improving ✅
  Target for CGL exam (20 Apr): avg 170/200

🔴 ALERT: SSC CGL Evening (Dilsukhnagar) down 8 pts — investigation needed
```

---

## 2. Subject-Wise Analysis

```
SUBJECT-WISE PERFORMANCE — SSC CGL ALL BATCHES (March 2026)

  Subject             │ Total Qs │ Avg Correct │ Accuracy │ vs Last Month │ Flag
  ────────────────────┼──────────┼─────────────┼──────────┼───────────────┼──────────
  Quantitative Apt.   │    25    │   16.4      │  65.6%   │ +2.1%         │ ✅
  Reasoning           │    25    │   17.8      │  71.2%   │ +0.8%         │ ✅
  English Language    │    25    │   15.2      │  60.8%   │ -1.4%         │ ⚠️ drop
  General Knowledge   │    25    │   14.6      │  58.4%   │ +0.4%         │ ⚠️ low

  WEAK TOPICS (Accuracy < 50% across all students):
  🔴 Caselet DI:              38.2% — curriculum gap (add 2 more sessions)
  🔴 Sentence Rearrangement:  42.1% — English weakness; extra session planned
  🟡 Circle Theorems:         48.4% — revision needed
  🟡 Banking Awareness (int.) 46.2% — Banking batch only — new topic added

  STRONG TOPICS (Accuracy > 80%):
  ✅ Percentage, Profit/Loss:  84.2%
  ✅ Blood Relations:          83.6%
  ✅ Synonyms/Antonyms:        81.4%
```

---

## 3. Top Performers & At-Risk Students

```
TOP PERFORMERS — SSC CGL (Mock #23 Rank 1–10)

  Rank │ Student Name        │ Batch          │ Score │ AIR (national) │ Trend
  ─────┼─────────────────────┼────────────────┼───────┼────────────────┼───────
  1    │ Akhil Kumar         │ CGL Morning    │ 192   │ AIR 247        │ ↑ +890
  2    │ Priya Reddy         │ CGL Morning    │ 188   │ AIR 412        │ ↑ +320
  3    │ Ravi Singh          │ RRB NTPC Wknd  │ 190   │ AIR 389        │ ↑ +180
  4    │ Divya Nair (st.)    │ CGL Evening    │ 187   │ AIR 501        │ ↑ +88
  5    │ Karthik M.          │ Banking Morn   │ 188   │ (Banking AIR)  │ ✅
  ...  │ ...                 │                │       │                │

AT-RISK STUDENTS (Score < 100/200 for 2+ consecutive mocks):

  Name              │ Batch       │ Mock#22 │ Mock#23 │ Attendance │ Counsellor
  ──────────────────┼─────────────┼─────────┼─────────┼────────────┼────────────
  Suresh P.         │ CGL Morn    │  88     │  92     │  62% ⚠️    │ Flag: Yes
  Anitha K.         │ CGL Eve     │  76     │  84     │  78%       │ Flag: Yes
  Mohammed R.       │ CGL Eve     │  68     │  72     │  55% 🔴    │ Flag: Yes
  Lakshmi T.        │ CHSL Morn   │  94     │  91     │  84%       │ Flag: Yes
  ...8 more         │             │         │         │            │
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/performance/dashboard/` | Cross-batch performance summary |
| 2 | `GET` | `/api/v1/coaching/{id}/performance/subject-wise/?course=ssc-cgl` | Subject accuracy breakdown |
| 3 | `GET` | `/api/v1/coaching/{id}/performance/top-performers/?batch={id}` | Top 10 students per batch |
| 4 | `GET` | `/api/v1/coaching/{id}/performance/at-risk/` | Students flagged for 2+ consecutive low scores |
| 5 | `GET` | `/api/v1/coaching/{id}/performance/trend/?batch={id}&months=3` | 3-month score trend |

---

## 5. Business Rules

- Cross-batch performance comparison is useful for identifying systemic issues but must be interpreted carefully; batches starting at different times have different syllabus completion levels — a newer batch will naturally score lower than a batch in its final revision month; the Academic Director must filter comparisons by batch age (months since start) not just raw score; EduForge labels each batch's month number on the comparison chart
- The "at-risk" flag (2+ consecutive low scores) must trigger a counsellor session within 5 working days; students who score below 50% for multiple mocks without intervention typically drop out within 6 weeks; early intervention — understanding the root cause (weak foundation, personal issues, wrong batch selection) — has a 68% success rate in improving the student's performance or gracefully redirecting them to a more suitable batch or preparation strategy
- Subject-wise accuracy below 50% is a signal to the Course Head, not just the student; if 38% accuracy on Caselet DI is observed across 600 students, this is a curriculum delivery failure, not a student failure; the Course Head must investigate whether the topic was adequately taught, whether the questions were calibrated correctly, and whether sufficient practice material was provided
- Government exam selection rates (186 confirmed selections in FY 2025–26) are tracked separately from mock test performance; there is typically a 6–18 month lag between a student's enrollment, peak mock performance, and actual government exam selection; the Academic Director must track cohort outcomes (students who joined in June 2024 → what % cleared their target exam by March 2026) to understand true teaching effectiveness
- Performance reports are shared with the Academic Director and Branch Manager; individual student performance data is accessible to the student's Batch Coordinator and assigned Counsellor; raw score data is not shared with marketing or admissions teams — this prevents misuse of student data for testimonial marketing without explicit student consent per DPDPA 2023

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division B*
