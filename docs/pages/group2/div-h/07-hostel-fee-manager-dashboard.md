# 07 — Hostel Fee Manager Dashboard

> **URL:** `/group/hostel/fees/`
> **File:** `07-hostel-fee-manager-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Hostel Fee Manager (Role 73, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Hostel Fee Manager. Manages the complete hostel fee lifecycle across all branches — fee plan configuration (AC/Non-AC, Boys/Girls, with mess charges and extra charges), fee collection tracking, defaulter management, late fee calculation, waiver approvals, and monthly reconciliation reports to the Group CFO.

Hostel fees are significantly more complex than day scholar fees. A hosteler's total charge comprises: Tuition (shared with day scholars) + Hostel accommodation (AC/Non-AC rate) + Mess charges (daily rate × days) + Optional extras (laundry, AC maintenance, excursion). All must be tracked separately and reconciled monthly.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Hostel Fee Manager | G3 | Full — all branches, all fee types | Exclusive dashboard |
| Group Hostel Director | G3 | View — fee collection summary | Via own dashboard |
| Group CFO | G1 | Read-only — revenue view | Via finance portal |
| Group Hostel Admission Coordinator | G3 | View — fee plan selection during admission | Read-only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Fee Manager Dashboard
```

### 3.2 Page Header
```
Welcome back, [Manager Name]          [+ New Fee Plan]  [Export Defaulter List ↓]  [Settings ⚙]
Group Hostel Fee Manager · AY [current academic year] · [Month]
Collected: ₹[N]  ·  Outstanding: ₹[N]  ·  Collection Rate: [N]%  ·  Defaulters: [N]
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Defaulters with 0 payment for > 60 days | "[N] hostelers have made zero payment in > 60 days. Fee hold / exit notice required." | Red |
| Defaulters > 30 days | "[N] hostelers with outstanding dues for > 30 days. Send reminders." | Amber |
| Fee collection < 70% for any branch this month | "[Branch] fee collection is only [N]% this month. Requires branch accountant follow-up." | Amber |
| Fee plan not set for a hostel type at any branch | "Fee plan missing: [Branch] has no fee plan configured for [hostel type]. Students cannot be admitted." | Red |

---

## 4. KPI Summary Bar (7 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Hostel Fee Billed (Month) | ₹ total billed to all hostelers this month | Blue always | → Page 18 |
| Collected (Month) | ₹ received | Blue always | → Page 18 |
| Collection Rate (Month) | % collected vs billed | Green ≥ 90% · Yellow 70–90% · Red < 70% | → Page 18 |
| Outstanding Amount | ₹ total due across all hostelers | Yellow > 0 always | → Page 18 (outstanding filter) |
| Defaulters (30+ days) | Count of hostelers with >30d outstanding | Green = 0 · Yellow 1–20 · Red > 20 | → Page 18 (defaulter filter) |
| Active Fee Plans | Count of configured hostel fee plans | Blue always | → Page 17 |
| Waivers Approved (Month) | Count of waivers granted this month | Blue always | → Page 18 (waivers filter) |

**HTMX:** `hx-trigger="every 10m"` → KPI auto-refresh.

---

## 5. Sections

### 5.1 Branch Fee Collection Table

> Per-branch fee collection summary — Manager's working table.

**Search:** Branch name, city. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches with hostel |
| Collection Rate | Radio | Any / ≥ 90% / 70–90% / < 70% |
| Has Defaulters | Checkbox | Show only branches with defaulters |
| Fee Plan Status | Radio | All configured / Missing plan |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → branch fee detail drawer |
| Hostelers | ✅ | Total enrolled |
| Billed (Month) | ✅ | ₹ amount |
| Collected (Month) | ✅ | ₹ amount |
| Collection % | ✅ | Colour-coded |
| Outstanding | ✅ | ₹ amount (red if > ₹50,000) |
| Defaulters (30d+) | ✅ | Count |
| Last Reminder Sent | ✅ | Date |
| Fee Plan Status | ✅ | ✅ Configured / ❌ Missing |
| Actions | ❌ | View · Send Reminder · View Defaulters |

**Default sort:** Collection % ascending (worst first).

**Pagination:** Server-side · 25/page.

---

### 5.2 Defaulter Quick List

> Cross-branch defaulter list sorted by outstanding days.

**Columns:** Hosteler · Branch · Hostel Type · Days Outstanding · Amount Due · Last Payment · [Action →]

Action options: Send WhatsApp Reminder · Mark Fee Hold · Initiate Exit Notice.

"View All →" → Page 18 (defaulter filter).

---

### 5.3 Monthly Fee Collection Chart

**Chart — Collection Trend (12 months)**
- Grouped bar chart: Billed (₹) vs Collected (₹) per month
- Line overlay: Collection % per month
- Target line at 90% on % axis

**Chart — Fee Type Breakdown (Pie)**
- Accommodation / Mess / Laundry / AC Maintenance / Extras
- Shows composition of total hostel fees billed

---

### 5.4 Fee Plan Summary Table

> All configured hostel fee plans — Manager's reference.

**Columns:** Branch · Hostel Type (AC/Non-AC) · Gender · AY · Accommodation/mo · Mess/mo · Extras/mo · Total/mo · Active · Actions

[Manage Fee Plans →] → Page 17.

---

## 6. Drawers

### 6.1 Drawer: `branch-fee-detail`
- **Width:** 640px
- **Tabs:** Collection Summary · Defaulters · Waivers · Fee Plan · History
- **Collection Summary:** Month-by-month collection, outstanding trend
- **Defaulters:** All defaulters for this branch with action options
- **Waivers:** Granted waivers this AY with reason and approver

### 6.2 Modal: Send Bulk Reminder
- **Trigger:** "Send Reminder" in branch row
- **Type:** Centred modal (480px)
- **Content:** "This will send a WhatsApp payment reminder to all defaulters at [Branch]. [N] messages will be sent."
- **Fields:** Message template selector · Custom note (optional)
- **On confirm:** POST to reminder endpoint; WhatsApp messages queued; audit log entry

### 6.3 Modal: Fee Hold / Exit Notice
- **Trigger:** Defaulter list → Mark Fee Hold / Initiate Exit Notice
- **Type:** Centred modal (480px)
- **Content:** Hosteler name, outstanding amount, days overdue
- **Fields:** Action: Fee Hold / Hostel Exit Notice · Reason · Notify Parent (checkbox) · Notify Branch Principal (checkbox)
- **On confirm:** Status updated; notifications sent; audit log

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Fee plan created | "Fee plan created for [Branch] — [Hostel Type] [AY]." | Success | 4s |
| Reminder sent | "Payment reminders sent to [N] defaulters at [Branch]." | Info | 4s |
| Fee hold applied | "Fee hold applied for [Hosteler Name]. Parent notified." | Warning | 6s |
| Exit notice issued | "Hostel exit notice issued for [Hosteler Name]." | Warning | 6s |
| Waiver approved | "Fee waiver approved for [Hosteler Name]." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No defaulters | "All Hostel Fees Current" | "No defaulters across all branches this month." | — |
| No fee plans configured | "No Hostel Fee Plans Found" | "Create fee plans for each hostel type and branch before admissions." | [+ New Fee Plan] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 7 KPI cards + collection table + defaulter list + charts |
| Table filter/search | Inline skeleton rows |
| KPI auto-refresh | Shimmer on card values |
| Reminder modal confirm | Spinner on Send; modal closes on success |

---

## 10. Role-Based UI Visibility

| Element | Fee Manager G3 | Hostel Director G3 | CFO G1 |
|---|---|---|---|
| Create Fee Plan | ✅ | ❌ | ❌ |
| Send Reminder | ✅ | ❌ | ❌ |
| Apply Fee Hold | ✅ | ✅ (requires Fee Manager co-auth) | ❌ |
| Issue Exit Notice | ✅ | ✅ | ❌ |
| Approve Waiver | ✅ | ✅ | ❌ |
| View collection data | ✅ | ✅ (summary) | ✅ (read-only) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/fees/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/fees/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/fees/branches/` | JWT (G3+) | Branch collection table |
| GET | `/api/v1/group/{group_id}/hostel/fees/defaulters/` | JWT (G3+) | Cross-branch defaulter list |
| POST | `/api/v1/group/{group_id}/hostel/fees/reminders/bulk/` | JWT (G3+) | Send bulk reminders |
| POST | `/api/v1/group/{group_id}/hostel/fees/hostelers/{id}/fee-hold/` | JWT (G3+) | Apply fee hold |
| POST | `/api/v1/group/{group_id}/hostel/fees/hostelers/{id}/exit-notice/` | JWT (G3+) | Issue exit notice |
| GET | `/api/v1/group/{group_id}/hostel/fees/collection-trends/` | JWT (G3+) | 12-month trend chart data |
| GET | `/api/v1/group/{group_id}/hostel/fees/branches/{id}/detail/` | JWT (G3+) | Branch fee detail drawer |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 10m` | GET `.../fees/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch table search | `input delay:300ms` | GET `.../fees/branches/?q={val}` | `#fee-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../fees/branches/?{filters}` | `#fee-table-section` | `innerHTML` |
| Open branch detail | `click` | GET `.../fees/branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Send reminder confirm | `click` | POST `.../fees/reminders/bulk/` | `#defaulter-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
