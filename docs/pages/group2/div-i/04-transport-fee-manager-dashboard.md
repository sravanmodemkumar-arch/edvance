# 04 — Transport Fee Manager Dashboard

> **URL:** `/group/transport/fees/`
> **File:** `04-transport-fee-manager-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Transport Fee Manager (Role 82, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Transport Fee Manager. Manages the complete transport fee lifecycle across all branches — fee structure configuration per route/zone/distance, fee collection tracking, defaulter management, bus pass issuance, and monthly reconciliation to the Group CFO.

Transport fees are charged per route, per distance zone, or per term — separate from tuition. A student's transport fee depends on their assigned route and the distance slab. The Fee Manager configures fee plans per branch, tracks collection, and escalates persistent defaulters to branch accountants.

Scale: 3,000–15,000 students on transport · ₹2,000–₹8,000 per student per month · crores in annual transport fee revenue.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Fee Manager | G3 | Full — all branches, all fee types | Exclusive dashboard |
| Group Transport Director | G3 | View — fee collection summary | Via own dashboard |
| Group Fleet Manager | G3 | ❌ No access — own dashboard at /fleet/ | Redirect to Page 02 |
| Group Route Planning Manager | G3 | Read — fee plan per route | Route creation context |
| Group Driver/Conductor HR | G0 | ❌ No EduForge login | See Page 05 |
| Group Transport Safety Officer | G3 | ❌ No access — own dashboard at /safety/ | Redirect to Page 06 |
| Group CFO | G1 | Read-only — revenue view | Via finance portal |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Fee Manager Dashboard
```

### 3.2 Page Header
```
Welcome back, [Manager Name]          [+ New Fee Plan]  [Export Defaulter List ↓]  [Settings ⚙]
Group Transport Fee Manager · AY [current academic year] · [Month]
Collected: ₹[N]  ·  Outstanding: ₹[N]  ·  Collection Rate: [N]%  ·  Defaulters: [N]
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Defaulters with 0 payment > 60 days | "[N] students have made zero transport fee payment in > 60 days." | Red |
| Collection < 70% for any branch | "[Branch] transport fee collection is only [N]% this month." | Amber |
| Fee plan missing for active route | "Fee plan missing for route [Name] at [Branch]. Students cannot be billed." | Red |
| Bus pass expired students still on route | "[N] students with expired bus passes are still allocated to routes." | Amber |

---

## 4. KPI Summary Bar (7 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Transport Fee Billed (Month) | ₹ total billed to all transport students | Blue always | → Page 21 |
| Collected (Month) | ₹ received | Blue always | → Page 21 |
| Collection Rate | % collected vs billed | Green ≥ 85% · Yellow 65–85% · Red < 65% | → Page 21 |
| Outstanding Amount | ₹ total due | Yellow > 0 | → Page 22 |
| Defaulters (30+ days) | Students with overdue fee | Green = 0 · Yellow 1–20 · Red > 20 | → Page 22 |
| Active Fee Plans | Configured transport fee plans | Blue always | → Page 20 |
| Bus Passes Issued | Current valid bus passes | Blue always | → Page 28 |

**HTMX:** `hx-trigger="every 10m"` → KPI auto-refresh.

---

## 5. Sections

### 5.1 Branch Fee Collection Table

> Per-branch transport fee collection — Manager's primary working table.

**Search:** Branch name, city. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Collection Rate | Radio | Any / ≥ 85% / 65–85% / < 65% |
| Has Defaulters | Checkbox | Branches with defaulters only |
| Fee Plan Status | Radio | All / Configured / Missing |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → branch fee detail drawer |
| Students on Transport | ✅ | Total enrolled |
| Billed (Month) | ✅ | ₹ amount |
| Collected (Month) | ✅ | ₹ amount |
| Collection % | ✅ | Colour-coded |
| Outstanding | ✅ | ₹ amount |
| Defaulters (30d+) | ✅ | Count |
| Last Reminder Sent | ✅ | Date |
| Fee Plan Status | ✅ | ✅ Configured / ❌ Missing |
| Actions | ❌ | View · Send Reminder · View Defaulters |

**Default sort:** Collection % ascending (worst first).
**Pagination:** Server-side · 25/page.

---

### 5.2 Defaulter Quick List

> Cross-branch defaulter list sorted by outstanding days.

**Columns:** Student Name · Branch · Route · Days Outstanding · Amount Due · Last Payment · [Action →]

Actions: Send WhatsApp Reminder · Suspend Bus Pass · Escalate to Branch.

"View All →" → Page 22.

---

### 5.3 Monthly Collection Trend (Chart)

**Chart — Collection Trend (12 months)**
- Grouped bar chart: Billed (₹) vs Collected (₹) per month
- Line overlay: Collection % per month
- Target line at 85%

---

### 5.4 Fee Plan Summary

> All configured transport fee plans across branches.

**Columns:** Branch · Zone / Route · Fee Per Month (₹) · Fee Per Term (₹) · AY · Active · Actions (Edit)

"Manage Fee Plans →" → Page 20.

---

## 6. Drawers

### 6.1 Drawer: `branch-fee-detail`
- **Width:** 640px
- **Tabs:** Collection Summary · Defaulters · Fee Plans · History
- Collection trend per branch, outstanding breakdown by route
- All defaulters with action options
- Configured fee plans by route/zone

### 6.2 Modal: Send Bulk Reminder
- **Trigger:** "Send Reminder" in branch row
- **Width:** 480px
- **Content:** "Sending WhatsApp payment reminders to [N] defaulters at [Branch]."
- **Fields:** Message template · Custom note (optional)
- **On confirm:** POST to reminder endpoint; WhatsApp messages queued; audit log entry

### 6.3 Modal: Suspend Bus Pass
- **Trigger:** Defaulter → Suspend Bus Pass
- **Width:** 480px
- **Fields:** Student Name · Outstanding Amount · Reason · Notify Parent (checkbox) · Effective Date
- **Warning:** "Student will not be permitted to board the bus from [date] until fee is paid."

> **Audit trail:** All write actions (fee plan create, reminders, bus pass suspension) are logged to [Transport Audit Log → Page 33].

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Fee plan created | "Fee plan created for [Branch] — Route [Name]." | Success | 4s |
| Fee plan create failed | "Failed to create fee plan. Check for duplicate plan for this route." | Error | 5s |
| Reminder sent | "Payment reminders sent to [N] students at [Branch]." | Info | 4s |
| Reminder send failed | "Failed to send reminders. Check WhatsApp notification configuration." | Error | 5s |
| Bus pass suspended | "Bus pass suspended for [Name]. Parent notified." | Warning | 6s |
| Bus pass suspension failed | "Failed to suspend bus pass. Please retry." | Error | 5s |
| Collection exported | "Fee collection report exported successfully." | Info | 4s |
| Export failed | "Export failed. Please try again." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No defaulters | "All Transport Fees Current" | "No defaulters this month." | — |
| No fee plans | "No Transport Fee Plans" | "Configure fee plans for each route before billing students." | [+ New Fee Plan] |
| Branch table — no filter results | "No Branches Match Filters" | "Adjust collection rate or fee plan filters." | [Clear Filters] |
| Branch table — no search results | "No Branches Found for '[term]'" | "Check the branch name." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 7 KPI cards + branch collection table + defaulter list + chart |
| Table filter/search | Inline skeleton rows |
| KPI auto-refresh | Shimmer on card values |
| Reminder modal confirm | Spinner on Send; modal closes on success |

---

## 10. Role-Based UI Visibility

| Element | Fee Manager G3 | Transport Director G3 | CFO G1 |
|---|---|---|---|
| Create Fee Plan | ✅ | ❌ | ❌ |
| Send Reminder | ✅ | ❌ | ❌ |
| Suspend Bus Pass | ✅ | ✅ | ❌ |
| Export Collection | ✅ | ✅ | ✅ (read-only) |
| View All Branches | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/fees/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/transport/fees/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/transport/fees/branches/` | JWT (G3+) | Branch collection table |
| GET | `/api/v1/group/{group_id}/transport/fees/defaulters/` | JWT (G3+) | Cross-branch defaulter list |
| POST | `/api/v1/group/{group_id}/transport/fees/reminders/bulk/` | JWT (G3+) | Send bulk reminders |
| POST | `/api/v1/group/{group_id}/transport/fees/students/{id}/suspend-pass/` | JWT (G3+) | Suspend bus pass |
| GET | `/api/v1/group/{group_id}/transport/fees/collection-trends/` | JWT (G3+) | 12-month trend data |
| GET | `/api/v1/group/{group_id}/transport/fees/branches/{id}/detail/` | JWT (G3+) | Branch fee drawer |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 10m` | GET `.../fees/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch table search | `input delay:300ms` | GET `.../fees/branches/?q={val}` | `#fee-table-body` | `innerHTML` |
| Branch table sort | `click` on header | GET `.../fees/branches/?sort={col}&dir={asc/desc}` | `#fee-table-section` | `innerHTML` |
| Branch table pagination | `click` | GET `.../fees/branches/?page={n}` | `#fee-table-section` | `innerHTML` |
| Filter apply | `click` | GET `.../fees/branches/?{filters}` | `#fee-table-section` | `innerHTML` |
| Open branch drawer | `click` | GET `.../fees/branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Send reminder confirm | `click` | POST `.../fees/reminders/bulk/` | `#defaulter-section` | `innerHTML` |
| Export defaulter list | `click` | GET `.../fees/defaulters/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
