# Home Page: Group 9 — B2B Partner Portal
**Route:** `/home`
**Domain:** `partners.eduforge.in`
**Access:** B2B tech partners, API integrators, content publishers, government bodies
**Portal type:** Developer / API partner dashboard

---

## Overview

| Property | Value |
|---|---|
| Purpose | Partner's dashboard to manage their EduForge API integration — usage, keys, billing, data |
| Who uses it | EdTech companies, HR assessment firms, SCERT/NCERT bodies, content publishers |
| Key features | API key management, webhook config, usage analytics, sandbox, billing |
| Role splits | Partner Tech Lead (API config), Partner PM (analytics), Partner Billing (invoices) |

---

## Role-Based Home View Matrix

| Role | Home Shows |
|---|---|
| Partner CTO / Tech Lead | API health, error rates, webhook status, sandbox |
| Integration Developer | API call logs, endpoint docs, test environment |
| Partner Product Manager | Usage metrics, student count synced, test results delivered |
| Partner Account Manager | Contract status, SLA health, renewal date |
| Partner Billing Admin | Monthly usage invoice, payment status |

---

## Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Top Navigation | Partner branding + EduForge partner badge |
| 2 | Sidebar | API / Integration module nav |
| 3 | Partnership KPI Bar | Usage, health, billing metrics |
| 4 | Alert Banner | API errors, quota warnings, billing due |
| 5 | API Health Monitor | Real-time endpoint status |
| 6 | Usage Analytics | API call volume, success rates |
| 7 | Integration Status | Which integrations are live vs pending |
| 8 | Billing Summary | Current period invoice |
| 9 | Quick Links | API docs, sandbox, webhook tester |

---

## Section 3 — Partnership KPI Bar

| Card | Metric | Who Sees |
|---|---|---|
| 1 | API Calls Today | 14,247 calls. ↑ 12% from yesterday. | Tech Lead |
| 2 | Success Rate | 99.87% · 18 errors today | Tech Lead |
| 3 | Students Synced | 12,450 total active student records | PM |
| 4 | Data Freshness | "Last sync: 4 min ago" | Tech Lead |
| 5 | Monthly Usage | 2.4M calls / 5M plan (48%) | Billing |
| 6 | Invoice Due | ₹24,500 due in 8 days | Billing |

---

## Section 5 — API Health Monitor

```
┌──────────────────────────────────────────────────────────────────────┐
│  API Health                              Last checked: 2 min ago     │
│                                                                      │
│  Endpoint               Status    Latency   Uptime (30d)            │
│  ────────────────────────────────────────────────────────────────── │
│  POST /auth/otp/send    🟢 OK      42ms      99.98%                  │
│  GET  /students         🟢 OK      87ms      99.97%                  │
│  POST /results          🟢 OK      124ms     99.95%                  │
│  GET  /attendance       🟡 SLOW    892ms ⚠️  99.91%                  │
│  POST /enrollments      🟢 OK      156ms     100%                    │
│                                                                      │
│  ⚠️ GET /attendance is slow (>500ms SLA). [View Logs] [Raise Ticket]│
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 6 — Usage Analytics

```
┌────────────────────────────────────────────────────────────────────┐
│  API Usage — March 2024                   [Export] [Period: MTD ▼] │
│                                                                    │
│  ┌────────────────────────────────┐  ┌──────────────────────────┐ │
│  │  Daily Call Volume             │  │  Calls by Endpoint       │ │
│  │  [Line chart — 30 days]        │  │  /students     42%       │ │
│  │  Peak: 87,420 (Mar 15)         │  │  /attendance   28%       │ │
│  │  Avg:  14,200/day              │  │  /results      18%       │ │
│  └────────────────────────────────┘  │  /auth          8%       │ │
│                                      │  /other         4%       │ │
│  Error Rate: 0.13%  (below 1% SLA) ✅│  [View all →]            │ │
│                                      └──────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

---

## Section 7 — Integration Status

```
┌──────────────────────────────────────────────────────────────────────┐
│  Active Integrations                               [+ New API Key]  │
│                                                                      │
│  Integration            API Key          Status    Last Active      │
│  ────────────────────────────────────────────────────────────────── │
│  Production (Main)      ef_live_xxx···   🟢 Active  2 min ago       │
│  Staging Environment    ef_test_xxx···   🟢 Active  1 hr ago        │
│  Mobile App             ef_mob_xxx···    🟢 Active  Yesterday       │
│  Analytics Webhook      ef_wh_xxx···     🟡 Warning  3 days ago     │
│                                                                      │
│  ⚠️ Analytics webhook hasn't delivered in 3 days. [Debug →]        │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 8 — Billing Summary

```
┌──────────────────────────────────────────────────────────────────────┐
│  Billing — March 2024                          [Download Invoice]   │
│                                                                      │
│  Plan: Enterprise — 5M API calls/month · ₹24,500/month             │
│                                                                      │
│  Usage: 2,412,847 / 5,000,000 calls   (48.3%)  ████████░░░░       │
│                                                                      │
│  Invoice #INV-2024-0347:  ₹24,500                                   │
│  Due: 31 March 2024  (8 days remaining)                             │
│                                                                      │
│  [Pay Now — Razorpay]    [View Invoice]    [Download PDF]           │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 9 — Quick Links

```
┌──────────────────────────────────────────────────────────────────────┐
│  Developer Resources                                                 │
│                                                                      │
│  [📚 API Documentation]   [🧪 Sandbox Environment]                  │
│  [🔔 Webhook Tester]       [📋 Changelog]                           │
│  [💬 DevRel Support]       [📊 SLA Report]                          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## API Calls

| Section | Endpoint |
|---|---|
| KPI bar | `GET /api/v1/partner/home/kpis` |
| API health | `GET /api/v1/partner/health` |
| Usage analytics | `GET /api/v1/partner/usage?period=mtd` |
| Integration status | `GET /api/v1/partner/integrations` |
| Billing | `GET /api/v1/partner/billing/current` |
