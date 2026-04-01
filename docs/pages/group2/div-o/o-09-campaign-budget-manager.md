# O-09 — Campaign Budget Manager

> **URL:** `/group/marketing/campaigns/budget/`
> **File:** `o-09-campaign-budget-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary budget owner; G4/G5 approves

---

## 1. Purpose

The Campaign Budget Manager is the financial control centre for all marketing and admission campaign spend across the group. It provides a unified view of the season's total marketing budget, how it's allocated across phases, channels, branches, and individual campaigns, how much has been spent, what's remaining, and where the ROI is best versus worst. In essence, it answers the question every CEO asks: "Where is my marketing money going, and is it working?"

For a large Indian education group spending ₹2–10 Cr annually on marketing, budget discipline is critical. Without centralised tracking:
- Branch-level managers overspend on newspaper ads because they don't see the group-wide picture
- The Campaign Manager commits 80% of the budget to Phases 2–3 (November–February) and has nothing left for the critical Phase 4 walk-in season (March–April)
- WhatsApp campaigns cost ₹0.50/message but get blasted to 5L contacts weekly, burning ₹10L/month without conversion tracking
- Outdoor hoardings on annual rental keep renewing automatically because nobody reviews whether they generate leads
- The CFO gets a surprise ₹15L invoice from a newspaper agency that nobody approved

This page prevents all of that by implementing:
1. **Budget hierarchy:** Season → Phase → Channel → Campaign → Line item
2. **Approval workflow:** Any spend above ₹1L requires Campaign Manager approval; above ₹5L requires CEO approval
3. **Real-time tracking:** Every expense is logged against a campaign and channel, visible immediately
4. **ROI attribution:** Spend is linked to leads and conversions, enabling CPA/CPL calculation per rupee spent

**Scale:** ₹10L–₹10Cr annual budget · 15–60 campaigns · 7 phases · 8+ channels · 5–50 branches

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — allocate, log expenses, reallocate, approve < ₹5L | Primary budget owner |
| Group Admission Data Analyst | 132 | G1 | Read + Export | Views all budget data, generates reports |
| Group CFO / Finance Director | 30 | G1 | Read only (cross-division) | Monitors marketing spend from finance perspective |
| Group CEO | — | G4 | Read + Approve ≥ ₹5L | Approves high-value allocations |
| Group Chairman | — | G5 | Read + Approve + Override | Final authority on budget changes |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Expense logging: role 119 or G4+. Approval thresholds enforced server-side.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Campaign Planning  ›  Budget Manager
```

### 3.2 Page Header
```
Campaign Budget Manager                        [Log Expense]  [Reallocate]  [Budget Request]  [Export]
Campaign Manager — Ramesh Venkataraman
Season 2026-27 · Total Budget: ₹5,60,00,000 · Spent: ₹2,78,50,000 (49.7%) · Remaining: ₹2,81,50,000
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Total spend > 90% of budget | "Marketing budget at [X]%. Only ₹[Y] remaining for [Z] months of season." | Critical (red) |
| Any campaign > 100% of its budget | "Campaign '[Name]' has exceeded allocated budget by ₹[X]." | Critical (red) |
| Any phase > 95% of allocated budget | "Phase [N] budget nearly exhausted ([X]%). Reallocate or request top-up." | High (amber) |
| Pending expense approvals > 5 | "[N] expenses pending approval totalling ₹[X]" | Medium (yellow) |
| Budget request pending CEO approval | "Budget reallocation of ₹[X] awaiting CEO approval" | Info (blue) |

---

## 4. KPI Summary Bar (8 cards)

### Row 1 — Budget Overview (4 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Budget | ₹ Amount | Season approved budget | Static blue | `#kpi-total-budget` |
| 2 | Total Spent | ₹ Amount + % | SUM(expenses) / total_budget × 100 | Green < 80%, Amber 80–95%, Red > 95% | `#kpi-total-spent` |
| 3 | Remaining | ₹ Amount | Total − Spent | Red < 10% remaining, Amber 10–20%, Green > 20% | `#kpi-remaining` |
| 4 | Burn Rate | ₹/day | SUM(expenses last 30 days) / 30 | Amber if projected exhaustion before season end | `#kpi-burn-rate` |

### Row 2 — ROI Metrics (4 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 5 | Cost per Lead (CPL) | ₹ Amount | Total spend / Total leads | Green ≤ ₹400, Amber ₹401–₹800, Red > ₹800 | `#kpi-cpl` |
| 6 | Cost per Admission (CPA) | ₹ Amount | Total spend / Total enrollments | Green ≤ ₹2,000, Amber ₹2,001–₹5,000, Red > ₹5,000 | `#kpi-cpa` |
| 7 | ROI Multiple | Decimal | (Enrolled × Avg annual fee) / Total spend | Green > 10x, Amber 5–10x, Red < 5x | `#kpi-roi` |
| 8 | Pending Approvals | Integer | COUNT(expenses) WHERE status = 'pending_approval' | Red > 5, Amber 1–5, Green = 0 | `#kpi-pending-approvals` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/budget/kpis/"` → `hx-trigger="load, every 300s"`

---

## 5. Sections

### 5.1 Budget Allocation — Phase-wise

Master budget table showing allocation and utilisation per phase.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Phase | Text + Badge | Yes | Phase 1–7 with name |
| Allocated | ₹ Amount | Yes | Budget allocated to this phase |
| Spent | ₹ Amount | Yes | Actual spend |
| Utilisation % | Progress bar + % | Yes | Spent / Allocated × 100 |
| Remaining | ₹ Amount | Yes | Allocated − Spent |
| Campaigns | Integer | Yes | Number of campaigns in this phase |
| Leads | Integer | Yes | Leads from campaigns in this phase |
| CPA | ₹ Amount | Yes | Phase-level CPA |
| Status | Badge | Yes | Active (current phase) / Completed / Upcoming |
| Actions | Button | No | [View Breakdown] [Reallocate] |

### 5.2 Budget Allocation — Channel-wise

| Channel | Allocated | Spent | Util % | Leads | CPL | CPA | ROI |
|---|---|---|---|---|---|---|---|
| Newspaper | ₹1,68,00,000 | ₹92,00,000 | 54.8% | 4,200 | ₹2,190 | — | — |
| Digital (Google/Meta) | ₹84,00,000 | ₹38,00,000 | 45.2% | 2,800 | ₹1,357 | — | — |
| WhatsApp / SMS | ₹56,00,000 | ₹28,00,000 | 50.0% | 3,100 | ₹903 | — | — |
| Outdoor / BTL | ₹56,00,000 | ₹42,00,000 | 75.0% | 800 | ₹5,250 | — | — |
| Events (Open Day/Fair) | ₹42,00,000 | ₹32,00,000 | 76.2% | 1,400 | ₹2,286 | — | — |
| Referral Incentives | ₹28,00,000 | ₹18,00,000 | 64.3% | 900 | ₹2,000 | — | — |
| Email | ₹5,60,000 | ₹2,50,000 | 44.6% | 400 | ₹625 | — | — |
| Other / Misc | ₹20,40,000 | ₹26,00,000 | 127.5% | — | — | — | — |

### 5.3 Budget Allocation — Campaign-wise

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Campaign | Text | Yes | Campaign name — click opens O-08 |
| Channel(s) | Badge(s) | Yes | Multi-channel badges |
| Phase | Badge | Yes | Phase number |
| Allocated | ₹ Amount | Yes | Campaign budget |
| Spent | ₹ Amount | Yes | Actual spend |
| Util % | Progress bar | Yes | Spent / Allocated |
| Leads | Integer | Yes | Campaign leads |
| Conversions | Integer | Yes | Campaign enrollments |
| CPL | ₹ Amount | Yes | Campaign CPL |
| CPA | ₹ Amount | Yes | Campaign CPA |
| Status | Badge | Yes | Active / Completed / Scheduled |
| Actions | Buttons | No | [View] [Edit Budget] [Close] |

**Default sort:** Spent DESC (highest spending first)
**Pagination:** Server-side · 25/page
**Filter:** Phase / Channel / Status / Budget range

### 5.4 Expense Log

Detailed ledger of every expense recorded against campaigns.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Date | Date | Yes | Expense date |
| Campaign | Text | Yes | Which campaign |
| Channel | Badge | Yes | Channel type |
| Vendor / Payee | Text | Yes | Who was paid (newspaper agency, printing vendor, etc.) |
| Description | Text | No | What was the expense for |
| Amount | ₹ Amount | Yes | Expense amount |
| Invoice # | Text | No | Vendor invoice reference |
| Receipt | Download | No | Uploaded receipt/invoice scan |
| Approved By | Text | Yes | Who approved (auto/manager/CEO) |
| Approval Status | Badge | Yes | Approved / Pending / Rejected |
| Branch | Text | Yes | If branch-specific expense |
| Actions | Buttons | No | [View] [Edit] [Approve/Reject] |

**Default sort:** Date DESC
**Pagination:** Server-side · 50/page
**Filter:** Campaign / Channel / Vendor / Approval status / Date range / Amount range

### 5.5 Approval Queue (Campaign Manager / CEO)

Shows expenses pending approval. Campaign Manager sees items ≤ ₹5L. CEO sees items > ₹5L.

**Columns:** Same as Expense Log + [Approve ✅] [Reject ❌] buttons

### 5.6 Budget Forecast

Projection of remaining budget based on current burn rate.

| Metric | Value |
|---|---|
| Current burn rate | ₹[X]/day (based on last 30 days) |
| Days remaining in season | [N] days |
| Projected total spend | ₹[X] (burn rate × days remaining + current spend) |
| Budget surplus / deficit | ₹[X] surplus / ₹[X] deficit |
| Projected exhaustion date | [Date] (if current rate continues) |
| Recommendation | "Reduce daily spend by ₹[X] to last until season end" or "Budget sufficient — ₹[X] headroom" |

---

## 6. Drawers & Modals

### 6.1 Modal: `log-expense` (560px)
- **Title:** "Log Marketing Expense"
- **Fields:**
  - Campaign (dropdown, required)
  - Channel (dropdown, required)
  - Date (date, default today)
  - Vendor / Payee (text or dropdown from vendor master)
  - Description (text, required — e.g., "Eenadu Hyderabad half-page ad — 15 Jan")
  - Amount (₹, required)
  - Invoice number (text, optional)
  - Receipt upload (file, PDF/JPG, max 10 MB)
  - Branch (dropdown — if branch-specific, otherwise "Group")
  - Notes (textarea)
- **Buttons:** Cancel · Submit Expense
- **Auto-approval:** If amount ≤ ₹50,000 and user is role 119 → auto-approved. Otherwise → pending.
- **Threshold rules:**
  - ≤ ₹50,000: Auto-approved (role 119)
  - ₹50,001–₹5,00,000: Campaign Manager approval (role 119)
  - > ₹5,00,000: CEO approval (G4/G5)

### 6.2 Modal: `reallocate-budget` (560px)
- **Title:** "Reallocate Budget"
- **Fields:**
  - From: Phase/Channel/Campaign (dropdown + amount to move)
  - To: Phase/Channel/Campaign (dropdown)
  - Amount (₹, required)
  - Reason (textarea, required)
  - Approval required: auto-calculated based on amount threshold
- **Buttons:** Cancel · Submit Reallocation
- **Behaviour:** If below threshold → instant. If above → pending approval.

### 6.3 Modal: `budget-request` (480px)
- **Title:** "Request Budget Top-Up"
- **Fields:**
  - Additional amount requested (₹)
  - Phase / Campaign to allocate to
  - Justification (textarea, required — e.g., "Phase 4 walk-ins exceeding forecast, need additional newspaper budget")
  - Supporting data (auto-populated: current spend, lead velocity, conversion rate)
- **Buttons:** Cancel · Submit Request
- **Behaviour:** Sent to G4/G5 for approval → notification

### 6.4 Drawer: `expense-detail` (640px, right-slide)
- **Tabs:** Details · Receipt · Approval History
- **Details tab:** All expense fields, linked campaign, channel, vendor
- **Receipt tab:** Full-size view of uploaded receipt/invoice
- **Approval History tab:** Status changes with timestamps, approver, comments
- **Footer:** [Edit] [Approve] [Reject] [Delete] (role-dependent)

---

## 7. Charts

### 7.1 Budget Burn Curve (Area Chart)

| Property | Value |
|---|---|
| Chart type | Area (Chart.js 4.x) |
| Title | "Budget Burn — Actual vs Projected" |
| Data | Cumulative daily spend (actual line) + linear projected spend (dashed) + budget ceiling (horizontal) |
| X-axis | Date (season start → end) |
| Y-axis | ₹ Cumulative spend |
| Colour | Actual: `#3B82F6` blue fill / Projected: `#9CA3AF` grey dashed / Ceiling: `#EF4444` red horizontal |
| Tooltip | "[Date]: ₹[X] spent (₹[Y] projected) — Budget: ₹[Z]" |
| API | `GET /api/v1/group/{id}/marketing/budget/analytics/burn-curve/` |

### 7.2 Channel Spend Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut |
| Title | "Spend by Channel — Current Season" |
| Data | Actual spend per channel |
| Colour | Channel-specific palette |
| Tooltip | "[Channel]: ₹[X] ([Y]%)" |
| API | `GET /api/v1/group/{id}/marketing/budget/analytics/spend-by-channel/` |

### 7.3 CPL by Channel (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Cost per Lead by Channel" |
| Data | CPL per channel (spend / leads) |
| Colour | Green ≤ ₹500, Amber ₹501–₹2,000, Red > ₹2,000 per bar |
| Tooltip | "[Channel]: CPL ₹[X] ([N] leads from ₹[Y] spend)" |
| API | `GET /api/v1/group/{id}/marketing/budget/analytics/cpl-by-channel/` |

### 7.4 Monthly Spend Trend (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar |
| Title | "Monthly Marketing Spend — Current vs Previous Season" |
| Data | Monthly spend: current season (bar 1) vs previous season (bar 2) |
| Colour | Current: `#3B82F6` / Previous: `#D1D5DB` |
| Tooltip | "[Month]: Current ₹[X] / Previous ₹[Y] ([Z]% change)" |
| API | `GET /api/v1/group/{id}/marketing/budget/analytics/monthly-spend-trend/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Expense logged | "Expense of ₹[X] logged against '[Campaign]'" | Success | 3s |
| Expense auto-approved | "Expense auto-approved (below ₹50,000 threshold)" | Success | 3s |
| Expense pending approval | "Expense of ₹[X] submitted for approval" | Info | 3s |
| Expense approved | "Expense of ₹[X] approved by [Approver]" | Success | 3s |
| Expense rejected | "Expense of ₹[X] rejected — reason: [Reason]" | Warning | 5s |
| Budget reallocated | "₹[X] reallocated from [Source] to [Target]" | Success | 4s |
| Budget request submitted | "Budget top-up request of ₹[X] submitted for CEO approval" | Info | 4s |
| Budget top-up approved | "Budget top-up of ₹[X] approved — new total: ₹[Y]" | Success | 5s |
| Budget warning | "Marketing budget at [X]%. Review spend or request top-up." | Warning | 6s |
| Budget exceeded | "Campaign '[Name]' has exceeded allocated budget" | Error | 8s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No budget configured | 💰 | "No Budget Set" | "Set the season marketing budget to start tracking spend." | Configure Budget (O-07 Season Plan) |
| No expenses logged | 📝 | "No Expenses Recorded" | "Log your first marketing expense to start budget tracking." | Log Expense |
| No pending approvals | ✅ | "No Pending Approvals" | "All expenses have been reviewed and approved." | — |
| Budget fully spent | 🚫 | "Budget Exhausted" | "The marketing budget for this season has been fully utilised." | Request Top-Up |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 8 KPI shimmer cards (2 rows of 4) + table skeleton |
| Phase table load | 7-row table skeleton |
| Channel table load | 8-row table skeleton |
| Campaign table load | 10-row table skeleton |
| Expense log load | 15-row table skeleton |
| Expense detail drawer | Right-slide skeleton with receipt placeholder |
| Chart load | Grey canvas placeholder |
| Budget forecast | Card skeleton with metrics |
| Approval queue | 5-row table skeleton |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/budget/` | G1+ | Budget overview (allocations + spend) |
| GET | `/api/v1/group/{id}/marketing/budget/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/budget/phase-wise/` | G1+ | Phase allocation table |
| GET | `/api/v1/group/{id}/marketing/budget/channel-wise/` | G1+ | Channel allocation table |
| GET | `/api/v1/group/{id}/marketing/budget/campaign-wise/` | G1+ | Campaign budget table |
| POST | `/api/v1/group/{id}/marketing/budget/expenses/` | G3+ | Log new expense |
| GET | `/api/v1/group/{id}/marketing/budget/expenses/` | G1+ | Expense ledger (paginated) |
| GET | `/api/v1/group/{id}/marketing/budget/expenses/{expense_id}/` | G1+ | Single expense detail |
| PATCH | `/api/v1/group/{id}/marketing/budget/expenses/{expense_id}/` | G3+ | Update expense |
| PATCH | `/api/v1/group/{id}/marketing/budget/expenses/{expense_id}/approval/` | G3+ | Approve/reject expense |
| POST | `/api/v1/group/{id}/marketing/budget/reallocate/` | G3+ | Reallocate budget |
| POST | `/api/v1/group/{id}/marketing/budget/top-up-request/` | G3+ | Request budget increase |
| PATCH | `/api/v1/group/{id}/marketing/budget/top-up-request/{req_id}/` | G4+ | Approve/reject top-up |
| GET | `/api/v1/group/{id}/marketing/budget/forecast/` | G1+ | Budget forecast data |
| GET | `/api/v1/group/{id}/marketing/budget/pending-approvals/` | G3+ | Pending approval queue |
| GET | `/api/v1/group/{id}/marketing/budget/analytics/burn-curve/` | G1+ | Burn curve chart |
| GET | `/api/v1/group/{id}/marketing/budget/analytics/spend-by-channel/` | G1+ | Channel spend donut |
| GET | `/api/v1/group/{id}/marketing/budget/analytics/cpl-by-channel/` | G1+ | CPL bar chart |
| GET | `/api/v1/group/{id}/marketing/budget/analytics/monthly-spend-trend/` | G1+ | Monthly trend |
| POST | `/api/v1/group/{id}/marketing/budget/export/` | G1+ | Export budget report |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../budget/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Phase table | `<div id="phase-table">` | `hx-get=".../budget/phase-wise/"` | `#phase-table-body` | `innerHTML` | `hx-trigger="load"` |
| Channel table | `<div id="channel-table">` | `hx-get=".../budget/channel-wise/"` | `#channel-table-body` | `innerHTML` | `hx-trigger="load"` |
| Campaign table | `<div id="campaign-table">` | `hx-get=".../budget/campaign-wise/"` | `#campaign-table-body` | `innerHTML` | `hx-trigger="load"` |
| Expense log | `<div id="expense-log">` | `hx-get=".../budget/expenses/"` | `#expense-table-body` | `innerHTML` | `hx-trigger="load"` |
| Log expense | Form submit | `hx-post=".../budget/expenses/"` | `#log-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Approve expense | Approve button | `hx-patch=".../budget/expenses/{id}/approval/"` | `#expense-row-{id}` | `outerHTML` | Inline update |
| Expense detail drawer | Row click | `hx-get=".../budget/expenses/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Filter expenses | Filter controls | `hx-get` with filter params | `#expense-table-body` | `innerHTML` | `hx-trigger="change"` |
| Reallocate | Form submit | `hx-post=".../budget/reallocate/"` | `#reallocate-result` | `innerHTML` | Toast |
| Forecast load | `<div id="forecast">` | `hx-get=".../budget/forecast/"` | `#forecast-content` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#expense-table-body` | `innerHTML` | Table body |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
