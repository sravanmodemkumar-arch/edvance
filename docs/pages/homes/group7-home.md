# Home Page: Group 7 — TSP (Test Series Platform) Portal
**Route:** `/home`
**Domain:** `www.narayana-tests.com` (operator's own domain) or `[brand].testpro.in`
**Access:** TSP Operator and their team — NOT students directly (students have separate view)
**Portal type:** White-label test series platform — operator's own branded exam engine

---

## Overview

| Property | Value |
|---|---|
| Purpose | Operator's command center to run their branded test series |
| Who uses it | TSP Owner, Content team, Test Ops, Student support, Finance |
| Key difference | This is the OPERATOR's home — not student's home. Operator manages everything here. |
| Branding | 100% operator's brand. No EduForge branding (white-label). |
| Example | Narayana's team logs into `narayana-tests.com/home` to manage their test series |

---

## Role-Based Home View Matrix

| Role | Home Shows |
|---|---|
| TSP Owner / Director | Revenue, total students, test performance, EduForge fee owed |
| TSP Admin | Platform health, user counts, upcoming tests, system config |
| Content Head | MCQ bank status, review queue, approval pipeline |
| Test Series Manager | Upcoming tests calendar, live tests, results pending |
| Student Support Lead | Login issues, result queries, open tickets |
| Finance Manager | Subscription revenue, Razorpay settlements, EduForge SaaS fee |

---

## Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Top Navigation | Operator's branding (their logo, their colors) |
| 2 | Sidebar | TSP module navigation |
| 3 | TSP KPI Bar | Operator's key metrics |
| 4 | Alert Banner | Live test alerts, content issues, BGV warnings |
| 5 | Live Tests Monitor | Currently running tests |
| 6 | Upcoming Tests Calendar | Next 7 days test schedule |
| 7 | Content Pipeline | Review / approval queue |
| 8 | Student Acquisition | Subscription + enrollment trends |
| 9 | Revenue Snapshot | Income, EduForge SaaS fee |
| 10 | Activity Feed | Platform events |

---

## Section 1 — Top Navigation (Operator's Brand)

| Element | Spec |
|---|---|
| Logo | **Operator's logo** — e.g., Narayana Tests logo. EduForge logo NOT shown (white-label). |
| Platform name | Operator-defined: "Narayana Test Series" |
| Tag line | Operator-defined: "Excellence in JEE/NEET Preparation" |
| Search | Search students, tests, results |
| Notifications | Live test alerts, student issues, content approvals |

---

## Section 3 — TSP KPI Bar

| Card | Metric | Sub-info |
|---|---|---|
| 1 | Total Subscribers | Active paid + free trial students |
| 2 | Revenue MTD | This month's subscriptions. vs last month. |
| 3 | Tests Published | Active test series count |
| 4 | MCQ Bank | Total questions published. Pending review: X. |
| 5 | Avg Score (Last Test) | Mean score of all students in last test |
| 6 | EduForge Fee Due | SaaS fee owed to EduForge this month |

---

## Section 5 — Live Tests Monitor

```
┌──────────────────────────────────────────────────────────────────────┐
│  🔴 LIVE TESTS                                       [War Room →]   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  JEE Mock #24 — Narayana Test Series                         │   │
│  │  Started: 10:00 AM · Ends: 11:05 AM · 65 min remaining       │   │
│  │  Online: 12,847 students · Submitted: 2,341                   │   │
│  │  Errors: 0 ✅                                                │   │
│  │  [Monitor Live]  [Extend Time]  [Broadcast Message]          │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  No other tests running currently.                                   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 6 — Upcoming Tests Calendar

```
┌──────────────────────────────────────────────────────────────────────┐
│  Upcoming Tests                                    [+ Schedule Test]│
│                                                                      │
│  TODAY, 19 MAR                                                       │
│  ● 10:00 AM  JEE Mock #24 (LIVE NOW)          12,847 registered    │
│  ● 02:00 PM  NEET Mock #18                     8,231 registered     │
│                                                                      │
│  TOMORROW, 20 MAR                                                    │
│  ● 10:00 AM  Foundation Mock #11               3,400 registered     │
│                                                                      │
│  22 MAR                                                              │
│  ● 09:00 AM  JEE Advanced Mock #8              6,200 registered     │
│                                                                      │
│  [View Full Calendar]                                               │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 7 — Content Pipeline

```
┌──────────────────────────────────────────────────────────────────────┐
│  Content Pipeline                                [View All →]       │
│                                                                      │
│  ┌────────────────────┐  ┌────────────────────┐  ┌───────────────┐ │
│  │  📝 In Review      │  │  ✅ Awaiting Apprv  │  │  📤 Published │ │
│  │  47 questions      │  │  23 questions       │  │  12,847 total │ │
│  │  [Review Queue →]  │  │  [Approve →]        │  │  [Browse →]   │ │
│  └────────────────────┘  └────────────────────┘  └───────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 8 — Student Acquisition

```
┌──────────────────────────────────────────────────────────────────────┐
│  Students & Subscriptions                                            │
│                                                                      │
│  Total students: 24,700   ↑ 12% from last month                     │
│  Active paid:    18,420                                              │
│  Free trial:      3,280   [Convert 847 trial expiring this week]    │
│  Churned MTD:       420                                              │
│                                                                      │
│  Enrollment trend (last 6 months)                                   │
│  [Bar chart]                                                         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 9 — Revenue Snapshot

```
┌──────────────────────────────────────────────────────────────────────┐
│  Revenue — March 2024                       [Full Report →]         │
│                                                                      │
│  Gross Revenue:       ₹18,47,000                                    │
│  Razorpay fees:         -₹18,470  (1%)                              │
│  EduForge SaaS fee:     -₹92,350  (5% per student)                  │
│  Net Revenue:         ₹17,36,180                                    │
│                                                                      │
│  EduForge fee due by 31 Mar: ₹92,350   [Pay Now via Razorpay]      │
│                                                                      │
│  [Download Invoice]  [Razorpay Settlement]                          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Student View — TSP Portal (Student Side)

> When students log into `narayana-tests.com`, they see the STUDENT view (not operator view).

```
┌──────────────────────────────────────────────────────────────────────┐
│  [Narayana Tests Logo]                              [👤 Akhil Kumar]│
│  JEE Advanced Subscriber · Premium Plan                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────┐  ┌──────────────────────────────────────┐ │
│  │  🔴 LIVE TEST        │  │  📊 MY PERFORMANCE                   │ │
│  │  JEE Mock #24        │  │  Last Test: Mock #23                  │ │
│  │  65 min remaining    │  │  Score: 198/300  AIR: 4,231           │ │
│  │  [Attempt Now →]     │  │  Weak: Organic Chem, Integration      │ │
│  └──────────────────────┘  └──────────────────────────────────────┘ │
│                                                                      │
│  UPCOMING TESTS                                                      │
│  ● Tomorrow 2PM: NEET Mock #18     ● 22 Mar: JEE Adv Mock #8       │
│                                                                      │
│  RECENT RESULTS                                                      │
│  Mock #23: 198/300 · AIR 4,231 · [Solutions] [Detailed Analysis]   │
│  Mock #22: 187/300 · AIR 4,892                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## API Calls

| Section | Endpoint |
|---|---|
| KPI Bar | `GET /api/v1/tsp/home/kpis` |
| Live tests | `GET /api/v1/tsp/tests?status=live` |
| Upcoming tests | `GET /api/v1/tsp/tests?status=upcoming&days=7` |
| Content pipeline | `GET /api/v1/tsp/content/pipeline` |
| Revenue snapshot | `GET /api/v1/tsp/finance/snapshot` |
| Student home | `GET /api/v1/tsp/student/home` |
