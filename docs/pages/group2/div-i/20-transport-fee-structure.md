# 20 — Transport Fee Structure

> **URL:** `/group/transport/fees/structure/`
> **File:** `20-transport-fee-structure.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Transport Fee Manager (primary) · Transport Director · CFO (view)

---

## 1. Purpose

Defines and manages transport fee plans across all branches. Transport fees are charged based on route distance zones, bus type (AC/non-AC), or specific route. A student's transport fee is determined by their assigned route's fee plan.

Fee plans are configured per branch and per zone/route. Small groups may have one flat fee per branch; large groups may have 10–20 distance slabs per branch. The Fee Manager creates and updates fee plans; changes take effect from the next billing cycle (term or month).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Fee Manager | G3 | Full — create, edit, activate fee plans | Primary owner |
| Group Transport Director | G3 | View + approve major revisions | Oversight |
| Group CFO | G1 | Read-only — cost review | View only |
| Group Route Planning Manager | G3 | Read — fee per route reference | View only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Transport Fee Structure
```

### 3.2 Page Header
- **Title:** `Transport Fee Structure`
- **Subtitle:** `[N] Active Plans · [N] Branches · AY [current]`
- **Right controls:** `+ New Fee Plan` · `Copy Plans from Last AY` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Routes with no fee plan | "[N] active routes have no fee plan — students cannot be billed." | Red |
| Fee plan not set for new AY | "[N] branches have no fee plan configured for AY [next]." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Fee Plans | Active across all branches | Blue |
| Branches with All Routes Covered | % | Green = 100% · Red < 100% |
| Routes Without Fee Plan | Must-fix | Red > 0 |
| Avg Fee per Student/Month | ₹ across all plans | Blue |
| Highest Fee Plan | ₹/month | Blue (informational) |
| Lowest Fee Plan | ₹/month | Blue (informational) |

---

## 5. Main Table — Fee Plans

**Search:** Branch, plan name, route. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Fee Type | Radio | All / Zone-based / Route-specific / Flat |
| Status | Radio | All / Active / Draft / Retired |
| Academic Year | Select | Current AY / Past AYs |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | |
| Plan Name | ✅ | Link → plan detail drawer |
| Fee Type | ✅ | Zone / Route / Flat |
| Zone / Route | ✅ | Applicable scope |
| Fee Per Month (₹) | ✅ | |
| Fee Per Term (₹) | ✅ | × 4 months per term |
| Annual Fee (₹) | ✅ | |
| Students Enrolled | ✅ | On this plan |
| AY | ✅ | |
| Status | ✅ | Active / Draft / Retired badge |
| Actions | ❌ | View · Edit · Clone · Retire |

**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `create-fee-plan`
- **Trigger:** + New Fee Plan
- **Width:** 600px
- **Fields:** Branch · Plan Name · Academic Year · Fee Type (Zone-based / Route-specific / Flat) · Route(s) applicable (multi-select) · Fee Per Month (₹) · Billing Frequency (Monthly / Per Term / Annual) · Late Payment Penalty (₹/day after due date) · Grace Period (days) · Effective From (date) · Notes
- **Validation:** Fee must be > 0 · At least one route must be selected unless Flat type

### 6.3 Drawer: `copy-plans-from-last-ay`
- **Trigger:** Copy Plans from Last AY button
- **Width:** 540px
- **Content:** "Copying fee plans from AY [prev] → AY [current]. The following plans will be duplicated (as Draft status)."
- **Fields:** Source AY (auto-filled) · Target AY (auto-filled) · Branches (All / Select — multi-select) · Include fee amounts as-is (checkbox — if unchecked, amounts are set to 0 for manual update) · Review before activating (checkbox, default checked)
- **Preview table:** Shows plan name, branch, current fee, status after copy
- **On confirm:** All plans cloned as Draft for target AY; redirects to fee plan list filtered by Draft status
- **Validation:** Cannot copy if target AY plans already exist (warns, allows overwrite with confirmation)

> **Audit trail:** All write actions (create, edit, clone, retire fee plan) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

### 6.2 Drawer: `fee-plan-detail`
- **Width:** 600px
- **Tabs:** Plan Details · Routes Linked · Students · History
- **Plan Details:** All fee configuration fields
- **Routes Linked:** All routes using this plan with student counts
- **Students:** All students on this fee plan
- **History:** AY-by-AY fee history, revision log

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Fee plan created | "Fee plan [Name] created for [Branch]." | Success | 4s |
| Fee plan create failed | "Failed to create fee plan. Check for duplicate plan for this route." | Error | 5s |
| Fee plan updated | "Fee plan updated. Changes effective from [date]." | Info | 4s |
| Fee plan update failed | "Failed to update fee plan. Please retry." | Error | 5s |
| Plans copied from last AY | "[N] fee plans copied to AY [current] as Draft. Review and activate." | Info | 5s |
| Copy plans failed | "Failed to copy fee plans. Please retry." | Error | 5s |
| Plan cloned | "Fee plan cloned for AY [next year]. Review and activate." | Info | 4s |
| Clone failed | "Failed to clone fee plan. Please retry." | Error | 5s |
| Plan retired | "Fee plan [Name] retired. Affected students: [N]." | Warning | 5s |
| Retire failed | "Failed to retire fee plan. Please retry." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No fee plans | "No Transport Fee Plans" | "Create fee plans for each branch before billing students." | [+ New Fee Plan] |
| No routes without plans | "All Routes Have Fee Plans" | "Every active route has a fee plan configured." | — |
| No filter results | "No Fee Plans Match Filters" | "Adjust branch, fee type, status, or academic year filters." | [Clear Filters] |
| No search results | "No Fee Plans Found for '[term]'" | "Check the branch, plan name, or route." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + fee plan table |
| Filter/search | Table body skeleton |
| Create / detail drawer | 600px skeleton |

---

## 10. Role-Based UI Visibility

| Element | Fee Manager G3 | Transport Director G3 | CFO G1 | Route Planning Mgr G3 |
|---|---|---|---|---|
| Create Fee Plan | ✅ | ✅ (major revision) | ❌ | ❌ |
| Edit Fee Plan | ✅ | ❌ | ❌ | ❌ |
| Retire Fee Plan | ✅ | ✅ | ❌ | ❌ |
| View All Plans | ✅ | ✅ | ✅ | ✅ |
| Clone to Next AY | ✅ | ❌ | ❌ | ❌ |
| Export | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/fees/plans/` | JWT (G3+) | Fee plan list |
| POST | `/api/v1/group/{group_id}/transport/fees/plans/` | JWT (G3+) | Create plan |
| GET | `/api/v1/group/{group_id}/transport/fees/plans/{id}/` | JWT (G3+) | Plan detail |
| PATCH | `/api/v1/group/{group_id}/transport/fees/plans/{id}/` | JWT (G3+) | Update plan |
| POST | `/api/v1/group/{group_id}/transport/fees/plans/{id}/clone/` | JWT (G3+) | Clone for next AY |
| POST | `/api/v1/group/{group_id}/transport/fees/plans/{id}/retire/` | JWT (G3+) | Retire plan |
| POST | `/api/v1/group/{group_id}/transport/fees/plans/copy-from-ay/` | JWT (G3+) | Bulk copy plans from previous AY |
| GET | `/api/v1/group/{group_id}/transport/fees/plans/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/fees/plans/export/` | JWT (G3+) | Async CSV/XLSX export |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../plans/?q={val}` | `#fee-plan-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../plans/?{filters}` | `#fee-plan-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../plans/?sort={col}&dir={asc/desc}` | `#fee-plan-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../plans/?page={n}` | `#fee-plan-table-section` | `innerHTML` |
| Open plan detail drawer | `click` on Plan Name | GET `.../plans/{id}/` | `#drawer-body` | `innerHTML` |
| Create plan submit | `click` | POST `.../plans/` | `#fee-plan-table-section` | `innerHTML` |
| Clone plan confirm | `click` | POST `.../plans/{id}/clone/` | `#fee-plan-table-section` | `innerHTML` |
| Retire plan confirm | `click` | POST `.../plans/{id}/retire/` | `#plan-row-{id}` | `outerHTML` |
| Copy from last AY confirm | `click` | POST `.../plans/copy-from-ay/` | `#fee-plan-table-section` | `innerHTML` |
| Export | `click` | GET `.../plans/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
