# B-01 — TSP Admin Dashboard

> **URL:** `/tsp/admin/dashboard/`
> **File:** `b-01-tsp-dashboard.md`
> **Priority:** P1
> **Roles:** TSP Admin · TSP Manager · EduForge Support

---

## 1. Dashboard Overview Cards

```
TSP ADMIN DASHBOARD — TopRank Academy (toprank.eduforge.in)
Vijayawada, AP | Plan: Standard | Since: Apr 2026

  ── KEY METRICS (Today: 31 Mar 2026) ─────────────────────────────────────

  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
  │  TOTAL STUDENTS  │  │  ACTIVE TODAY    │  │  REVENUE (MTD)   │  │  TESTS TAKEN     │
  │     3,042        │  │     1,287        │  │   Rs.4,28,600    │  │     18,340       │
  │  +126 this month │  │  42.3% of total  │  │  +12% vs Feb     │  │  +2,100 vs Feb   │
  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘

  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
  │  MOCK TESTS      │  │  FACULTY         │  │  AVG SCORE       │  │  RENEWAL RATE    │
  │     84 published │  │     12 active    │  │     62.4%        │  │     78%          │
  │  +6 this month   │  │  3 content roles │  │  +1.2% vs Feb    │  │  target: 85%     │
  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## 2. Activity Feed & Quick Actions

```
RECENT ACTIVITY                                          QUICK ACTIONS
                                                         ─────────────────────
  31 Mar 10:42  84 students attempted APPSC Gr2          [+ Create Mock Test]
                Prelims Mock #12                         [+ Add Students]
  31 Mar 09:15  Faculty Lakshmi uploaded 120              [+ Invite Faculty]
                Banking questions                         [View Reports]
  30 Mar 22:30  Bulk import: 45 new students             [Portal Settings]
                (SSC batch — Mar 2026)
  30 Mar 18:00  Mock "SSC CGL Tier-I #8"
                published by Ravi K.
  30 Mar 14:22  Revenue: Rs.12,400 collected
                (28 new subscriptions)
  29 Mar 11:00  Student Priya M. scored 142/150
                on APPSC Prelims Mock #11 (top 1%)

  ── UPCOMING ─────────────────────────────────────────
  01 Apr  APPSC Group 2 Prelims Mock #13 scheduled (auto-publish 6:00 AM)
  03 Apr  SSC CGL Tier-I Full Mock #9 — content review pending
  05 Apr  Monthly student performance report auto-generated
  07 Apr  Subscription renewal batch: 340 students due

  ── ALERTS ───────────────────────────────────────────
  [!] 23 students have not logged in for 15+ days — consider engagement push
  [!] Faculty Ravi K. has 8 questions flagged for review
  [!] Storage usage: 4.2 GB / 10 GB (42%) — video uploads consuming space
```

---

## 3. Revenue & Student Trend Charts

```
STUDENT GROWTH (Last 6 Months)                   REVENUE TREND (Last 6 Months)

  Students                                         Revenue (Rs.)
  3,100 |                              *           4,50,000 |                           *
  3,000 |                         *                4,00,000 |                      *
  2,900 |                    *                     3,50,000 |                 *
  2,800 |               *                          3,00,000 |            *
  2,700 |          *                                2,50,000 |       *
  2,600 |     *                                    2,00,000 |  *
        └──────────────────────────                        └──────────────────────────
         Oct   Nov   Dec   Jan   Feb   Mar                  Oct   Nov   Dec   Jan   Feb   Mar

  EXAM-WISE STUDENT DISTRIBUTION                   REVENUE BY SOURCE
  ┌────────────────────────────┐                   ┌────────────────────────────┐
  │ APPSC Group 2    1,180 39% │ ████████████      │ Subscriptions   Rs.3,42,800│ 80%
  │ SSC CGL/CHSL      840 28% │ ████████          │ Test Series      Rs.64,200 │ 15%
  │ Banking IBPS       620 20% │ ██████            │ Study Material   Rs.21,600 │  5%
  │ RRB NTPC           280  9% │ ███               └────────────────────────────┘
  │ Other              122  4% │ █
  └────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/tsp/admin/dashboard/summary/` | Dashboard summary metrics (students, revenue, tests) |
| 2 | `GET` | `/api/v1/tsp/admin/dashboard/activity/` | Recent activity feed (paginated) |
| 3 | `GET` | `/api/v1/tsp/admin/dashboard/trends/?period=6m` | Student growth and revenue trend data |
| 4 | `GET` | `/api/v1/tsp/admin/dashboard/alerts/` | Active alerts and action items |
| 5 | `GET` | `/api/v1/tsp/admin/dashboard/exam-distribution/` | Student distribution by exam category |

---

## 5. Business Rules

- The TSP dashboard is scoped exclusively to the tenant's own data; TopRank Academy sees only its 3,042 students, its 84 mock tests, and its Rs.4,28,600 revenue — never any data from other TSPs on the EduForge platform; this tenant isolation is enforced at the database query level using the `tsp_id` filter on every API call; even if a TSP admin manipulates the API request, the middleware injects the authenticated TSP's ID and overrides any tenant parameter; a data leak between TSPs would be a catastrophic breach of trust and a potential legal liability under India's DPDP Act 2023
- Revenue figures on the dashboard reflect the TSP's gross collection minus EduForge's platform fee; if a student pays Rs.499 for a TopRank subscription, the dashboard shows Rs.499 as revenue because the TSP owner needs to see what their students paid; EduForge's 15–25% commission (depending on plan tier) is shown separately in the monthly settlement report (B-05); displaying net revenue on the dashboard would confuse the TSP owner because the amount would not match their Razorpay/payment gateway records
- The "students not logged in for 15+ days" alert is a retention-critical signal; in Indian exam prep, students who go inactive for more than two weeks during preparation season have a 60% probability of churning; the alert threshold is configurable per TSP (default: 15 days) because preparation intensity varies by exam cycle — APPSC aspirants may go inactive between Prelims and Mains (3-month gap), which is expected; the TSP admin can send a bulk WhatsApp or SMS nudge directly from this alert card
- Dashboard data is cached with a 5-minute TTL for performance; a TSP with 3,000 students generates significant query load if every dashboard refresh hits the database; the summary cards (student count, revenue, test count) are computed by a background job every 5 minutes and served from Redis; the activity feed is real-time (event-sourced from the activity log); the TSP admin sees a "Last updated: 10:42 AM" timestamp on the cached cards so they know the data is near-real-time, not stale; a manual refresh button forces a cache invalidation for the current TSP

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division B*
