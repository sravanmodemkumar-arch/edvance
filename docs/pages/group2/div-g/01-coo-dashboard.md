# 01 — COO Dashboard

> **URL:** `/group/ops/coo/`
> **File:** `01-coo-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group COO (G4) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group COO. Single-screen command view of all branch
operations — SLA compliance, escalations, procurement, facilities, and zone health. The COO
sees every branch's operational status and can act on critical issues from this one page.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group COO | G4 | Full — all sections, all actions | Exclusive dashboard |
| Group Operations Manager | G3 | — | Own dashboard at `/group/ops/manager/` |
| Group Branch Coordinator | G3 | — | Own dashboard |
| Group Zone Director | G4 | — | Own dashboard |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('coo')`. Any other role redirected.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  COO Dashboard
```

### 3.2 Page Header
```
Welcome back, [COO Name]                           [Export Daily Report ↓]  [Settings ⚙]
[Group Name] — Chief Operating Officer · Last login: [date time]
```

### 3.3 Alert Banner (conditional — shown only when critical alerts exist)
- Collapsible panel above KPI row
- `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch/zone name + [Take Action →] link
- Max 5 alerts; "View all X alerts →" link to page 12

**Alert trigger examples:**
- SLA breach unresolved >24h for P1 escalation
- Facility safety certificate expired (fire NOC, building permit)
- CAPEX project overrun >20%
- Procurement delivery delayed >14 days past expected date
- Maintenance ticket Critical unresolved >4h

---

## 4. KPI Summary Bar (7 cards)

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| SLA Compliance | `94.2%` this month + trend | Ops aggregation | Green ≥95% · Yellow 85–95% · Red <85% | → Page 08 |
| Open Escalations | `12 open` + `3 P1` | Escalation DB | Green =0 P1 · Yellow 1–2 P1 · Red ≥3 P1 | → Page 12 |
| Active Branches | `48 / 50` operational | Branch status | Green = all active · Yellow 1–2 down · Red 3+ down | → Page 07 |
| Procurement Spend YTD | `₹1.4Cr / ₹2.0Cr budget` + % | Procurement | Green ≤80% · Yellow 80–95% · Red >95% | → Page 18 |
| Open Maintenance | `23 tickets` + `2 Critical` | Facilities | Green = 0 Critical · Yellow 1–2 · Red ≥3 | → Page 26 |
| Coordinator Coverage | `All 50 branches assigned` | Coordinator DB | Green = 100% · Yellow <100% · Red gaps >7d | → Page 09 |
| Compliance Certs | `3 expiring in 30d` | Facilities Compliance | Green = none · Yellow 1–3 expiring · Red ≥4 or expired | → Page 30 |

**HTMX:** `hx-trigger="every 5m"` → `hx-get="/api/v1/group/{id}/coo/kpi-cards/"` → `hx-target="#kpi-bar"` `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Critical Ops Queue

> Issues requiring COO decision today — P1 escalations, SLA breaches >12h, procurement approvals >₹5L.

**Display:** Card list, max 5. "View all →" → Page 12.

**Card fields:** Severity badge | Type | Branch/Zone | Raised by | Age (red if >12h for P1) | [Act →] [View Details →]

**Act → button:** Opens `escalation-detail` drawer.

---

### 5.2 Branch Operations Health Matrix

> All branches with operational metrics — COO's primary working table.

**Search:** Full-text across branch name, city, zone. Debounce 300ms.

**Advanced Filters:**
| Filter | Type |
|---|---|
| Zone | Multi-select |
| State | Multi-select |
| Branch Type | Day Scholar / Hostel / Both |
| SLA Status | Compliant / At Risk / Breached |
| Maintenance | Has Critical tickets checkbox |
| Coordinator | Select coordinator |

Active filter chips: dismissible, "Clear All", count badge.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | Link → `branch-ops-detail` drawer |
| Zone | ✅ | Large groups only |
| Coordinator | ✅ | Assigned coordinator name |
| SLA % | ✅ | Colour-coded |
| Open Escalations | ✅ | Count badge, red if >0 P1 |
| Open Grievances | ✅ | Count |
| Maintenance Tickets | ✅ | Open tickets count |
| Last Visit | ✅ | Date, red if >30 days |
| Compliance Score | ✅ | % out of checklist items |
| Status | ✅ | Active / Inactive / Onboarding |
| Actions | ❌ | View · Assign Coordinator |

**Default sort:** SLA % ascending (worst first).

**Pagination:** Server-side · 25/page · 10/25/50/All · page jump.

**Row select:** Checkbox + select-all · Bulk export CSV.

---

### 5.3 Ops Trend Chart

**Type:** Multi-line chart — SLA Compliance %, Escalations Resolved, Maintenance Tickets Closed — over 12 months.

**Library:** Chart.js 4.x. Colorblind-safe. Legend. Tooltip. PNG export.

**X-axis:** Months (Apr–Mar). **Y-axis:** % (SLA) + count (escalations, maintenance).

**Filter:** Branch filter (all / specific branch or zone) + Year selector.

---

### 5.4 Procurement Snapshot

Summary card row (not a table):
- Pending Requests: `18` awaiting approval
- POs In Transit: `7` active POs
- Delayed Deliveries: `2` past expected date
- Budget Utilization: `70% of ₹2.0Cr annual`

[View Procurement →] → Page 18.

---

### 5.5 Facilities Snapshot

Summary card row:
- Open Maintenance: `23` tickets (2 Critical, 8 High, 13 Medium/Low)
- Expiring Certs: `3` in next 30 days
- CAPEX Active: `4` ongoing projects

[View Facilities →] → Page 25.

---

### 5.6 Quick Access Grid

6 tiles (2×3):
| Tile | Label | Link |
|---|---|---|
| 1 | Branch Operations | `/group/ops/branches/` |
| 2 | Escalation Tracker | `/group/ops/escalations/` |
| 3 | Procurement | `/group/ops/procurement/` |
| 4 | Facilities | `/group/ops/facilities/` |
| 5 | Zone Management | `/group/ops/zones/` |
| 6 | Ops MIS Report | `/group/ops/reports/mis/` |

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-ops-detail`
- **Width:** 640px
- **Tabs:** Ops Metrics · SLA · Coordinator · Escalations · Visit History
- **Ops Metrics tab:** Enrollment, attendance %, fee %, staff count
- **SLA tab:** Per-metric SLA compliance table with breach history
- **Coordinator tab:** Assigned coordinator, last visit, scheduled next visit
- **Escalations tab:** All open escalations for this branch
- **Visit History tab:** Last 5 visits with report summaries

### 6.2 Drawer: `escalation-detail`
- **Width:** 680px
- **Tabs:** Overview · Timeline · Actions · Resolution
- **Actions tab (COO):** Reassign owner · Change severity · Mark resolved · Escalate to CEO

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Escalation assigned | "Escalation assigned to [Name]" | Success | 4s |
| Escalation resolved | "Escalation marked resolved" | Success | 4s |
| Export triggered | "Export started — file ready shortly" | Info | 4s |
| KPI load error | "Failed to load KPI data. Retrying…" | Error | Manual dismiss |
| Dashboard refreshed | "Dashboard refreshed" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No critical alerts | "All clear — operations running smoothly" | "No critical issues require your attention" | — |
| No branches (search) | "No branches match your search" | "Try adjusting filters" | [Clear Filters] |
| No procurement data | "No procurement data" | "No procurement activity this period" | [Go to Procurement] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: KPI bar (7 cards) + branch table (5 skeleton rows) + chart placeholder |
| Table search/filter/page | Inline skeleton rows |
| KPI auto-refresh | Shimmer over card values |
| Escalation action | Spinner in button + disabled |
| Drawer open | Spinner centred in drawer while fetching |

---

## 10. Role-Based UI Visibility

| Element | COO G4 | Others |
|---|---|---|
| Page itself | ✅ Rendered | ❌ Redirected |
| Alert Banner | ✅ Shown | N/A |
| [Act →] in Ops Queue | ✅ Enabled | N/A |
| [Export Daily Report] header button | ✅ Shown | N/A |
| Bulk export checkbox | ✅ Shown | N/A |
| [Assign Coordinator] row action | ✅ Shown | N/A |

> All visibility decisions server-side in Django template. No client-side role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/coo/dashboard/` | JWT (G4) | Full page data |
| GET | `/api/v1/group/{group_id}/coo/kpi-cards/` | JWT (G4) | KPI cards only (auto-refresh) |
| GET | `/api/v1/group/{group_id}/ops/branches/` | JWT (G4) | Branch ops table with filters |
| GET | `/api/v1/group/{group_id}/ops/trend/` | JWT (G4) | 12-month ops trend data |
| GET | `/api/v1/group/{group_id}/ops/branches/{branch_id}/detail/` | JWT (G4) | Branch ops detail drawer |
| GET | `/api/v1/group/{group_id}/escalations/?priority=P1&status=open` | JWT (G4) | Critical escalations queue |
| POST | `/api/v1/group/{group_id}/escalations/{id}/assign/` | JWT (G4) | Assign escalation |
| POST | `/api/v1/group/{group_id}/escalations/{id}/resolve/` | JWT (G4) | Resolve escalation |
| GET | `/api/v1/group/{group_id}/ops/branches/export/?format=csv` | JWT (G4) | Export table |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Branch search | `input delay:300ms` | `/api/.../ops/branches/?q={val}` | `#ops-branch-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../ops/branches/?filters={…}` | `#ops-branch-table-section` | `innerHTML` |
| Pagination | `click` | `/api/.../ops/branches/?page={n}` | `#ops-branch-table-section` | `innerHTML` |
| Sort click | `click` | `/api/.../ops/branches/?sort={col}&dir={asc/desc}` | `#ops-branch-table-section` | `innerHTML` |
| KPI auto-refresh | `every 5m` | `/api/.../coo/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Open branch detail | `click` | `/api/.../branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Assign escalation | `click` (form submit) | POST `/api/.../escalations/{id}/assign/` | `#critical-ops-queue` | `innerHTML` |
| Chart filter change | `change` | `/api/.../ops/trend/?zone={}&year={}` | `#ops-trend-chart-data` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
