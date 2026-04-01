# E-01 — Content Performance Dashboard

> **URL:** `/content-partner/analytics/dashboard/`
> **File:** `e-01-performance-dashboard.md`
> **Priority:** P1
> **Roles:** Content Partner (own content metrics) · EduForge Content Team (aggregate view)

---

## 1. Portfolio Performance Summary

```
EDUFORGE — CONTENT PERFORMANCE DASHBOARD
Partner: Dr. Venkat Rao (Individual SME)                   Period: Mar 2026
Expertise: Quantitative Aptitude, Reasoning
Exams: SSC CGL Tier 1 Quant · APPSC Group 2 Prelims · IBPS PO Prelims Reasoning

  ┌─── PORTFOLIO OVERVIEW ──────────────────────────────────────────────────┐
  │                                                                         │
  │   Total Questions         18,500                                        │
  │   Active in Live Tests     14,820  (80.1%)                              │
  │   Retired / Archived        3,680  (19.9%)                              │
  │                                                                         │
  │   ┌───────────── KEY METRICS (Last 30 Days) ─────────────────────────┐  │
  │   │                                                                   │  │
  │   │   Total Attempts          12,40,000   (+8.2% vs prev month)      │  │
  │   │   Avg Accuracy Rate            64.2%  (pool avg: 61.8%)          │  │
  │   │   Avg Time per Question        72 sec  (pool avg: 78 sec)        │  │
  │   │   Skip Rate                     2.3%  (pool avg: 3.9%)           │  │
  │   │   Avg Student Rating            4.1/5  (pool avg: 3.8/5)         │  │
  │   │   Error Reports Pending            14  (need response)            │  │
  │   │                                                                   │  │
  │   └───────────────────────────────────────────────────────────────────┘  │
  │                                                                         │
  │   QUALITY SCORE:  87 / 100  [=============================···]          │
  │   Pool Average:   72 / 100                                              │
  │   Status: "Top Contributor" badge active                                │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Exam-Wise Breakdown & Trend Charts

```
EXAM-WISE PERFORMANCE BREAKDOWN — Dr. Venkat Rao

  ┌─────────────────────────┬──────────┬───────────┬──────────┬──────────┬────────┐
  │ Exam                    │ Questions│ Attempts  │ Accuracy │ Avg Time │ Rating │
  ├─────────────────────────┼──────────┼───────────┼──────────┼──────────┼────────┤
  │ SSC CGL Tier 1 Quant    │    7,200 │  5,28,000 │   62.8%  │   74 sec │  4.0   │
  │ APPSC Group 2 Prelims   │    5,800 │  3,65,000 │   66.1%  │   68 sec │  4.2   │
  │ IBPS PO Prelims Reason. │    3,400 │  2,14,000 │   63.9%  │   76 sec │  4.1   │
  │ SSC CHSL Tier 1 Quant   │    1,200 │    88,000 │   68.4%  │   65 sec │  4.2   │
  │ RRB NTPC Quant           │      900 │    45,000 │   71.2%  │   58 sec │  3.9   │
  ├─────────────────────────┼──────────┼───────────┼──────────┼──────────┼────────┤
  │ TOTAL                    │   18,500 │ 12,40,000 │   64.2%  │   72 sec │  4.1   │
  └─────────────────────────┴──────────┴───────────┴──────────┴──────────┴────────┘

  MONTHLY ACCURACY TREND (Last 6 Months)

  68% |
  67% |                                              *
  66% |                                    *
  65% |                          *
  64% |              *                               ·····  64.2% (current)
  63% |    *
  62% |
  61% | ·····································································  pool avg 61.8%
  60% |
      +----+----------+----------+----------+----------+----------+---
       Oct       Nov       Dec       Jan       Feb       Mar

  MONTHLY ATTEMPT VOLUME (Lakhs)

  14L |                                                        ___
  12L |                                              ___      |12.4|
  10L |                                    ___      |11.5|    |____|
   8L |                          ___      |10.2|    |____|
   6L |              ___        | 9.6|    |____|
   4L |    ___      | 8.1|     |____|
   2L |   | 7.4|   |____|
   0L +   |____|
       Oct       Nov       Dec       Jan       Feb       Mar
```

---

## 3. Topic-Level Heatmap & Skip-Rate Alerts

```
TOPIC-LEVEL HEATMAP — SSC CGL Tier 1 Quant (Dr. Venkat Rao)

  Topic                      Qs     Attempts    Accuracy    Skip    Rating   Status
  ─────────────────────────────────────────────────────────────────────────────────
  Profit & Loss              820     62,400       59.3%     1.8%     4.0     OK
  Time & Work                740     55,200       61.7%     2.1%     4.1     OK
  Percentage                 680     51,800       66.4%     1.5%     4.2     OK
  SI / CI                    650     48,900       63.8%     2.4%     4.0     OK
  Number System              620     46,100       58.2%     3.8%     3.8     REVIEW
  Speed, Distance & Time     590     44,300       60.5%     2.0%     4.1     OK
  Ratio & Proportion         560     42,100       67.1%     1.6%     4.3     OK
  Mensuration                520     38,700       55.1%     4.2%     3.7     ALERT
  Algebra                    480     35,600       62.3%     2.9%     3.9     OK
  Trigonometry               440     32,800       70.2%     1.2%     4.4     OK
  Data Interpretation        400     29,500       68.9%     1.4%     4.2     OK
  Mixture & Alligation       350     26,200       64.6%     2.6%     4.0     OK
  Geometry                   300     14,400       52.8%     5.1%     3.5     ALERT
  ─────────────────────────────────────────────────────────────────────────────────

  ALERTS:
  [!] Mensuration — Skip rate 4.2% exceeds threshold (3.5%). 12 questions flagged
      for unclear diagrams. Consider adding diagram descriptions.
  [!] Geometry — Skip rate 5.1% exceeds threshold (3.5%). Accuracy 52.8% is lowest
      across all topics. 8 questions have difficulty parameter > +2.0 — may be too
      hard for SSC CGL level. Review recommended.
  [i] Number System — Skip rate 3.8% slightly above threshold. 4 questions flagged
      for ambiguous wording. Monitor next cycle.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/content-partner/analytics/dashboard/summary/` | Portfolio summary (totals, averages, quality score) |
| 2 | `GET` | `/api/v1/content-partner/analytics/dashboard/exam-breakdown/` | Exam-wise performance breakdown |
| 3 | `GET` | `/api/v1/content-partner/analytics/dashboard/trend/` | Monthly trend data (accuracy, attempts, rating) |
| 4 | `GET` | `/api/v1/content-partner/analytics/dashboard/topic-heatmap/` | Topic-level heatmap for a given exam |
| 5 | `GET` | `/api/v1/content-partner/analytics/dashboard/alerts/` | Active alerts (high skip rate, low accuracy, pending reports) |
| 6 | `GET` | `/api/v1/content-partner/analytics/dashboard/export/` | Export dashboard data as CSV or PDF |
| 7 | `GET` | `/api/v1/content-partner/analytics/dashboard/compare-pool/` | Compare partner metrics against pool averages |
| 8 | `GET` | `/api/v1/content-partner/analytics/dashboard/quality-score/` | Quality score computation breakdown |

---

## 5. Business Rules

- The Content Performance Dashboard is the default landing page for all content partners after login, displaying a 30-day rolling window by default with the option to switch to 7-day, 90-day, or custom date ranges; the dashboard must load within 2 seconds for partners with up to 50,000 questions, and all heavy aggregations (total attempts, accuracy rate, average time, skip rate) are pre-computed nightly by a background ETL pipeline that processes the previous day's attempt logs from the mock test engine; for Dr. Venkat Rao with 18,500 questions and 12,40,000 monthly attempts, the pre-aggregation ensures the dashboard does not trigger expensive real-time queries against the attempts table, which contains over 85 crore rows across all partners; intra-day metrics are approximated using a 15-minute refresh cache until the nightly pipeline finalises the numbers.

- The quality score displayed on the dashboard is a composite metric computed as a weighted average of five factors: accuracy rate relative to pool average (25% weight), discrimination index across questions (25% weight), student rating (20% weight), skip rate inverse (15% weight), and error report resolution rate (15% weight); Dr. Venkat Rao's score of 87/100 reflects his above-pool accuracy (64.2% vs 61.8%), strong discrimination indices (median a=0.78), high student rating (4.1/5), low skip rate (2.3% vs 3.9% pool), and 91% error report resolution rate; this score is recalculated daily and directly impacts the partner's revenue share tier — partners with quality score above 85 receive the premium tier rate (22% revenue share vs standard 18%), making the quality score both an informational metric and a financial incentive.

- Topic-level heatmap alerts are triggered automatically when any topic exceeds the configurable skip rate threshold (default 3.5%) or drops below the minimum accuracy threshold (default 50%) sustained over a 14-day window; alerts are classified as "ALERT" (immediate action recommended) when the metric exceeds the threshold by more than 1 percentage point, and "REVIEW" (monitor and assess) when within 1 percentage point of the threshold; Dr. Venkat Rao's Geometry topic at 5.1% skip rate and 52.8% accuracy triggers a dual ALERT, while Number System at 3.8% skip rate triggers only a REVIEW; partners who do not acknowledge or act on ALERT-level flags within 14 days will see affected questions automatically deprioritised in the test generation algorithm, reducing their appearance frequency by 50% until the partner addresses the issue.

- Dashboard data is scoped strictly to the authenticated partner's own content — Dr. Venkat Rao can never see another partner's question-level performance or raw metrics; the "pool average" comparison figures shown on the dashboard are anonymised aggregates across all active partners in the same exam category and subject, computed by the EduForge Content Team's analytics pipeline; these pool averages include at least 10 partners per category to prevent reverse-engineering of any individual partner's performance; the EduForge Content Team has access to a separate admin-level analytics view that shows cross-partner comparisons with identifying information, used for partner success outreach and content quality management, but this view is never exposed to partner accounts.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division E*
