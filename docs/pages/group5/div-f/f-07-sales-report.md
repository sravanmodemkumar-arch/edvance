# F-07 — Sales & Conversion Report

> **URL:** `/coaching/admissions/reports/`
> **File:** `f-07-sales-report.md`
> **Priority:** P2
> **Roles:** Branch Manager (K6) · Admissions Counsellor (K3 — own data) · Director (K7)

---

## 1. Monthly Sales Summary

```
SALES REPORT — March 2026
Toppers Coaching Centre, Hyderabad Main Branch

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  NEW ENROLLMENTS:  112  │  REVENUE: ₹ 14.2 Lakh  │  CONV RATE: 39.4%  │
  │  vs Feb 2026:       98  │  vs Feb:  ₹ 12.4 Lakh  │  vs Feb: 36.8%     │
  │  Growth: +14.3% ✅      │  Growth: +14.5% ✅      │  Growth: +2.6% ✅  │
  └──────────────────────────────────────────────────────────────────────────┘

  FUNNEL:
    Enquiries:     284  →  Demo attended: 168 (59.2%)  →  Enrolled: 112 (39.4%)
    Demo→Enroll:   66.7% conversion post-demo

  COURSE-WISE BREAKDOWN:
    Course            │ Enquiries │ Enrolled │ Conv.% │ Revenue
    ──────────────────┼───────────┼──────────┼────────┼────────────
    SSC CGL           │    98     │    42    │ 42.9%  │ ₹ 7,56,000
    Banking PO        │    62     │    28    │ 45.2%  │ ₹ 5,60,000
    RRB NTPC          │    54     │    18    │ 33.3%  │ ₹ 2,52,000
    SSC CHSL          │    38     │    14    │ 36.8%  │ ₹ 1,96,000
    Foundation        │    20     │     8    │ 40.0%  │ ₹    80,000
    Others            │    12     │     2    │ 16.7%  │ ₹    28,000

  SOURCE-WISE PERFORMANCE:
    Source       │ Enquiries │ Enrolled │ Conv.%  │ Quality
    ─────────────┼───────────┼──────────┼─────────┼──────────────
    Walk-in      │    64     │    36    │  56.3%  │ ✅ Best
    Referral     │    42     │    26    │  61.9%  │ ✅ Best
    YouTube      │    82     │    28    │  34.1%  │ 🟡 Moderate
    Instagram    │    48     │    12    │  25.0%  │ ⚠️ Low
    Organic SEO  │    36     │    10    │  27.8%  │ 🟡 Moderate
    Others       │    12     │     0    │   0.0%  │ 🔴 Review

  ⚠️ Instagram leads: 25% conversion — high volume, low quality; discuss with marketing
```

---

## 2. Counsellor Performance

```
COUNSELLOR PERFORMANCE — March 2026

  Counsellor       │ Leads │ Demos │ Enrolled │ Conv.% │ Rev (₹L) │ SLA Breach │ Rating
  ─────────────────┼───────┼───────┼──────────┼────────┼──────────┼────────────┼────────
  Ananya Roy       │  102  │  64   │    44    │ 43.1%  │   5.8L   │     1      │  4.6/5
  Rohan Sharma     │   94  │  56   │    36    │ 38.3%  │   4.8L   │     3      │  4.2/5
  Sita Rao         │   88  │  48   │    32    │ 36.4%  │   3.6L   │     6      │  3.8/5
  ─────────────────┴───────┴───────┴──────────┴────────┴──────────┴────────────┴────────

  INSIGHTS:
    Ananya Roy:   Best converter — referred leads handled well (62% referral conv)
    Rohan Sharma: Good volume but 3 SLA breaches (2-hr follow-up rule)
    Sita Rao:     Lower conv (36.4%) + 6 SLA breaches — needs coaching
    Action:       Sita Rao scheduled for admissions process coaching (Apr 2)
```

---

## 3. Revenue Trend

```
REVENUE TREND — April 2025 – March 2026

  Month    │ Enrollments │ Revenue (₹L) │ vs Target │ Trend
  ─────────┼─────────────┼──────────────┼───────────┼──────────────────
  Apr 25   │    64       │    8.2       │   82%  ⚠️ │ Batch-start dip
  May 25   │   124       │   18.4       │  102%  ✅ │ New batch surge
  Jun 25   │    88       │   12.2       │   92%  ✅ │
  Jul 25   │    62       │    8.6       │   86%  ⚠️ │
  Aug 25   │    78       │   10.8       │   90%  ✅ │
  Sep 25   │    82       │   11.4       │   95%  ✅ │
  Oct 25   │    94       │   13.2       │  100%  ✅ │
  Nov 25   │    88       │   12.0       │   96%  ✅ │
  Dec 25   │    72       │    9.8       │   89%  ⚠️ │ Holiday dip
  Jan 26   │    84       │   11.6       │   97%  ✅ │
  Feb 26   │    98       │   12.4       │   99%  ✅ │ Pre-batch ramp
  Mar 26   │   112       │   14.2       │  102%  ✅ │ Strong close ✅

  ANNUAL TOTAL:  ₹ 1,42,60,000  (₹1.43 Cr) | Target: ₹1.40 Cr | +2.1% ✅
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/admissions/reports/monthly/?month=2026-03` | Monthly sales summary |
| 2 | `GET` | `/api/v1/coaching/{id}/admissions/reports/counsellors/?month=2026-03` | Counsellor performance breakdown |
| 3 | `GET` | `/api/v1/coaching/{id}/admissions/reports/funnel/?month=2026-03` | Conversion funnel data |
| 4 | `GET` | `/api/v1/coaching/{id}/admissions/reports/sources/?month=2026-03` | Lead source quality analysis |
| 5 | `GET` | `/api/v1/coaching/{id}/admissions/reports/trend/?from=2025-04&to=2026-03` | Annual revenue trend |

---

## 5. Business Rules

- Counsellor conversion rates are visible to the Branch Manager and the individual counsellor (own data only); counsellors cannot see each other's conversion rates or revenue contributions; this prevents competitive sabotage and focuses each counsellor on their own improvement; the Branch Manager uses the aggregate to identify training needs and best practices; the top performer's techniques (Ananya Roy's referral lead handling) should be shared as a case study in team meetings without revealing individual metrics
- The monthly sales report is reviewed by the Branch Manager with the Director by the 5th of the following month; if revenue is below target for two consecutive months, the Director joins the admissions review to identify structural issues (batch timing, fee level, competitor offering, marketing quality); the Director does not micromanage single-month dips — the two-month threshold avoids over-reaction to seasonal variation
- Source quality tracking (Instagram = 25% conversion vs Referral = 62%) directly informs the marketing budget; TCC should increase spend on channels with high conversion (referral activation, YouTube organic) and reduce or improve Instagram lead quality (likely wrong audience targeting); this data is shared with the Marketing team (Division L) monthly; the admissions team does not control the marketing budget but provides the conversion data that drives marketing decisions
- Lead reversal (a student who enrolled and then cancelled within 7 days) is tracked separately from "lost leads" (leads who never enrolled); a high reversal rate indicates over-promising in counselling sessions; the SLA breach count (a counsellor not following up within 2 hours) is a process metric; both reversal rate and SLA breach count are included in the counsellor's annual performance review; the target is < 5% reversal and 0 SLA breaches per month
- Annual revenue trend data is used in the franchise review (A-05) for franchise branches — franchise branches must submit their monthly enrollment and revenue data by the 5th of each month; TCC headquarters compares franchise branch conversion rates against owned branches; a franchise branch with a persistently lower conversion rate (< 30% vs 40% TCC average) triggers a support visit from the training team; the franchise contract specifies a minimum enrollment target per quarter

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division F*
