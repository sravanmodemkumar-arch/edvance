# K-01 — Analytics Dashboard

> **URL:** `/coaching/analytics/`
> **File:** `k-01-analytics-dashboard.md`
> **Priority:** P2
> **Roles:** Branch Manager (K6) · Director (K7) · Academic Director (K5)

---

## 1. Dashboard Overview

```
ANALYTICS DASHBOARD — Toppers Coaching Centre
Hyderabad Main Branch | As of 31 March 2026 | AY 2025–26

  ┌─────────────────────────────────────────────────────────────────────┐
  │  EXECUTIVE SUMMARY                            [Export PDF] [Share]  │
  ├─────────────────┬─────────────────┬─────────────┬───────────────────┤
  │  STUDENTS        │  REVENUE         │  TESTS       │  SATISFACTION     │
  │  1,840 enrolled  │  ₹1.48 Cr (YTD) │  28 full     │  4.2 / 5.0        │
  │  ↑ 12% vs LY     │  ↑ 18% vs LY    │  mocks run   │  ↑ 0.2 vs Q2      │
  │  856 active      │  ₹14.2 L / mo   │  avg score   │  75% response      │
  │  (Mar batch)     │  (Mar 2026)     │  142 / 200   │  rate (Q3)         │
  ├─────────────────┴─────────────────┴─────────────┴───────────────────┤
  │  TREND (Last 6 Months)                                               │
  │                                                                      │
  │  Enrolled:  Oct:1,610  Nov:1,680  Dec:1,720  Jan:1,780  Feb:1,820  Mar:1,840
  │  Revenue:   Oct:11.8L  Nov:12.4L  Dec:13.1L  Jan:13.6L  Feb:14.0L  Mar:14.2L
  │  Attendance:Oct:82%   Nov:84%   Dec:85%   Jan:86%   Feb:87%   Mar:87.3%   │
  │  Avg Score: Oct:128   Nov:132   Dec:136   Jan:138   Feb:140   Mar:142     │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Key Metrics Panels

```
KEY METRICS — 31 March 2026

  ┌─────────────────────────────────────┐  ┌─────────────────────────────────────┐
  │  ENROLLMENT HEALTH                  │  │  ACADEMIC HEALTH                    │
  │  Total batches:           14        │  │  Avg mock score:     142/200 (71%)  │
  │  Avg batch size:         131        │  │  Top 10% threshold:  168/200        │
  │  Capacity utilisation:  87.3%       │  │  Students below 50%:   84 (4.6%)   │
  │  New admissions (Mar):   128        │  │  At-risk flagged:       18          │
  │  Dropout (Mar):            6        │  │  Doubt resolution SLA:  91.2%      │
  │  Net growth (Mar):       +122       │  │  Faculty avg rating:    4.2/5.0    │
  └─────────────────────────────────────┘  └─────────────────────────────────────┘

  ┌─────────────────────────────────────┐  ┌─────────────────────────────────────┐
  │  FINANCIAL HEALTH                   │  │  OPERATIONS HEALTH                  │
  │  Monthly revenue:   ₹14.2 L        │  │  Hostel occupancy:      84/108 (78%)│
  │  Collection rate:       92.3%       │  │  Open grievances:         4         │
  │  Defaulters (>30d):      38         │  │  Maintenance tickets:     7 open    │
  │  EMI adherence:         88.6%       │  │  Survey response rate:   75.2%      │
  │  Refunds (Mar):      ₹28,500       │  │  Alumni network size:    4,840      │
  │  Scholarships active:   295         │  │  Staff attendance:       96.8%      │
  └─────────────────────────────────────┘  └─────────────────────────────────────┘
```

---

## 3. Alerts & Exceptions

```
ALERTS & EXCEPTIONS — Requires Attention

  PRIORITY  │ Area              │ Alert                                  │ Action
  ──────────┼───────────────────┼────────────────────────────────────────┼──────────────────────
  🔴 HIGH   │ Finance           │ 38 students >30 days overdue (₹3.8L)  │ [View Defaulters]
  🔴 HIGH   │ Student Affairs   │ 3 grievances past 7-day review mark   │ [View Grievances]
  🟡 MEDIUM │ Academic          │ 18 at-risk students (score <50%)       │ [View At-Risk]
  🟡 MEDIUM │ Hostel            │ 5 maintenance requests >7 days open    │ [View Requests]
  🟡 MEDIUM │ Online Delivery   │ Online batch experience survey open    │ [Send Reminders]
  🟢 LOW    │ Faculty           │ Mr. Ravi S. rating 3.8 — action item  │ [View Feedback]
  🟢 LOW    │ Admissions        │ 12 leads >7 days without follow-up    │ [View CRM]

  EXCEPTIONS (Month):
    Batch over-capacity:     SSC CGL Evening — 138/130 (106%) ⚠️
    Staff absent >3 days:    None
    SLA breach (grievance):  GRV-0041 (5 days without resolution)
    Revenue below target:    None (₹14.2L vs ₹13.5L target) ✅
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/analytics/dashboard/` | Executive dashboard summary |
| 2 | `GET` | `/api/v1/coaching/{id}/analytics/dashboard/metrics/?period=monthly` | KPI metrics by period |
| 3 | `GET` | `/api/v1/coaching/{id}/analytics/alerts/` | Active alerts and exceptions |
| 4 | `GET` | `/api/v1/coaching/{id}/analytics/trends/?from=2025-10&to=2026-03` | Trend data for charts |
| 5 | `POST` | `/api/v1/coaching/{id}/analytics/dashboard/export/` | Export dashboard as PDF |

---

## 5. Business Rules

- The analytics dashboard is the Branch Manager's single-pane-of-glass view of TCC's operational health; it aggregates data from all functional modules (admissions, finance, academic, hostel, student affairs) and presents it as a coherent executive summary; the Branch Manager uses this daily to identify problems before they escalate; a metric that turns red (e.g., collection rate dropping below 85%) prompts an immediate review of the underlying module; the dashboard does not replace module-level management but complements it
- Alerts are generated automatically by the system when a metric crosses a predefined threshold; thresholds are set at the start of each academic year by the Director in consultation with the Branch Manager; an alert at 38 defaulters (₹3.8 lakh overdue) does not mean the Branch Manager takes personal collection action — it means the Accounts team is notified and the standard escalation process is triggered; the alert system prevents oversight gaps when staff are managing high workloads
- The dashboard is role-sensitive: the Branch Manager sees all metrics across all departments; the Academic Director sees only academic and faculty metrics; the Accounts Manager sees only financial metrics; this role-based filtering ensures that staff see what is relevant to their function without overwhelming them with data outside their scope; the Director sees everything plus franchise-level comparisons that the Branch Manager cannot access
- Month-over-month and year-over-year trends are more meaningful than point-in-time snapshots; a March 2026 attendance rate of 87.3% means little without context — but knowing it has improved from 82% in October 2025 shows a positive trend; the dashboard stores 24 months of historical data to enable meaningful trend analysis; trend data informs decisions like whether to adjust batch size, add sections, or change the study schedule
- Dashboard export (PDF/Excel) is used for Board presentations, franchise performance reviews, and regulatory submissions; the exported report includes a timestamp and the role of the person who generated it; an export generated by "K. Reddy, Branch Manager, 31 March 2026 14:30" is an official management report; modifications to exported data outside the system are not permissible; the system maintains a log of all dashboard exports for audit purposes

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division K*
