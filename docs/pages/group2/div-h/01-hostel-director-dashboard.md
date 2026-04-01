# 01 — Hostel Director Dashboard

> **URL:** `/group/hostel/director/`
> **File:** `01-hostel-director-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Hostel Director (Role 67, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Hostel Director. Single-screen command centre for the entire hostel system across all branches — occupancy, admissions, fee health, welfare incident status, mess hygiene scores, security alerts, medical room status, and discipline cases. The Hostel Director sees every hostel's operational health at a glance and can escalate or act on critical issues directly from this dashboard.

The Hostel Director is the group-level policy owner: they set hostel welfare standards, approve hostel admissions, escalate Severity 1 welfare incidents to the Group COO and Chairman, and liaise with Boys/Girls Hostel Coordinators on warden discipline. This dashboard reflects all that operational authority in one place.

Scale: a large group may have 20–50 hostel campuses (Boys + Girls separate), 5,000–30,000 hostelers, and 50–200 welfare incidents per month requiring daily review.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Hostel Director | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group Chairman / CEO | G5 / G4 | View — via governance reports only | Not this URL |
| Group COO | G4 | View — via operations portal only | Not this URL |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('hostel_director')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Director Dashboard
```

### 3.2 Page Header
```
Welcome back, [Director Name]                    [Export Daily Hostel Report ↓]  [Settings ⚙]
[Group Name] — Group Hostel Director · Last login: [date time]
AY [current academic year]  ·  [N] Hostel Campuses  ·  [N] Branches
```

### 3.3 Alert Banner (conditional — critical items requiring same-day action)

| Condition | Banner Text | Severity |
|---|---|---|
| Severity 1 welfare incident unresolved > 2h | "CRITICAL: Severity 1 welfare incident at [Branch] — [N] hours unresolved. Immediate action required." | Red |
| Severity 2 welfare incident unresolved > 8h | "[N] Severity 2 welfare incidents unresolved > 8 hours." | Amber |
| Hostel fee defaulters > 30 days with 0 payment | "[N] hostelers have zero fee payment for > 30 days." | Amber |
| Mess hygiene audit failed in last 7 days | "Mess hygiene audit FAILED at [Branch]. Immediate inspection required." | Red |
| Security incident reported last 24h | "Security incident reported at [Branch] last night. Review security log." | Red |
| Medical emergency in last 24h | "Medical emergency recorded at [Branch]. Check medical tracker." | Amber |
| Discipline case open > 30 days | "[N] discipline cases open for > 30 days without resolution." | Amber |

Max 5 alerts visible. Alert-type links route to the relevant operational page: Welfare alerts → Page 22 · Security alerts → Page 24 · Fee alerts → Page 18 · Medical alerts → Page 27 · Discipline alerts → Page 28 · Mess alerts → Page 20. "View all audit events → Hostel Audit Log (Page 33)" link always shown below the alert list.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Hostelers | Cross-branch count (Boys + Girls, all types) | Blue always | → Page 12 |
| Occupancy Rate | Filled beds / Total beds across all hostels | Green ≥ 85% · Yellow 70–85% · Red < 70% | → Page 13 |
| Welfare Incidents (Open) | Open incidents today (Severity 1–4 combined) | Green = 0 · Yellow 1–5 · Red > 5 | → Page 22 |
| Mess Hygiene Score | Average score across all branches (last audit) | Green ≥ 80% · Yellow 60–80% · Red < 60% | → Page 20 |
| Fee Collection Rate | Fees collected / Total billed (current month) | Green ≥ 90% · Yellow 70–90% · Red < 70% | → Page 18 |
| Security Alerts (Open) | Unresolved security alerts today | Green = 0 · Yellow 1–2 · Red > 2 | → Page 24 |
| Medical Visits Today | Medical room visits logged today | Blue always | → Page 27 |
| Discipline Cases (Open) | Active discipline cases across all branches | Green = 0 · Yellow 1–5 · Red > 5 | → Page 28 |

**HTMX:** `hx-trigger="every 5m"` → `hx-get="/api/v1/group/{id}/hostel/director/kpi-cards/"` → `hx-target="#kpi-bar"` `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Critical Hostel Queue

> Incidents, alerts, and unresolved items requiring Director action today.

**Display:** Card list, max 5. "View all →" → Page 22.

**Card fields:**
- Severity badge (1 = Red, 2 = Orange, 3 = Yellow, 4 = Blue)
- Type icon (Welfare / Security / Medical / Mess / Discipline)
- Branch + Hostel type (Boys / Girls)
- Age of incident (highlighted red if Severity 1 > 2h, Severity 2 > 8h)
- Raised by (warden / coordinator name)
- [Escalate →] [View Details →]

---

### 5.2 Hostel Branch Health Matrix

> All hostel campuses with key metrics — Director's primary working table.

**Search:** Full-text across branch name, city, zone. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All group branches with hostel |
| Hostel Type | Checkbox | Boys Only / Girls Only / Boys + Girls |
| Room Type | Checkbox | AC / Non-AC / Both |
| Welfare Status | Radio | Any / Has Open Severity 1 / Has Open Severity 2 / Clean |
| Fee Collection | Radio | Any / On Track / At Risk (>20% default) |
| Mess Score | Radio | Any / Pass / Fail |

Active filter chips: dismissible, "Clear All", count badge.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → `hosteler-detail` branch summary drawer |
| Hostel Type | ✅ | Boys / Girls / Both |
| Capacity | ✅ | Total beds (AC + Non-AC) |
| Occupied | ✅ | Count + % |
| Welfare (Open) | ✅ | Count badge, red if Severity 1 > 0 |
| Mess Score | ✅ | % from latest audit; Red if < 60% |
| Fee Collection % | ✅ | Colour-coded |
| Medical Visits (Month) | ✅ | Count |
| Security Alerts (Open) | ✅ | Count |
| Discipline Cases (Open) | ✅ | Count |
| Actions | ❌ | View · Escalate |

**Default sort:** Welfare (Open) descending — highest-risk branch first.

**Pagination:** Server-side · 25/page · 10/25/50/All · page jump.

**Row select:** Checkbox + select-all · Bulk export CSV.

---

### 5.3 Hostel Trend Charts

**Chart 1 — Welfare Incidents by Severity (12 months)**
- Stacked bar chart: Severity 1 (Red) · Severity 2 (Orange) · Severity 3 (Yellow) · Severity 4 (Blue)
- X: Months. Y: Count.
- Filter: Branch or group-wide.

**Chart 2 — Occupancy Trend (12 months)**
- Multi-line: Total capacity vs Occupied (Boys) vs Occupied (Girls)
- X: Months. Y: Student count.

**Chart 3 — Fee Collection Trend (12 months)**
- Line chart: Collection % per month
- Target line at 90%.
- Red zone shaded below 70%.

Library: Chart.js 4.x. Colorblind-safe palette. PNG export.

---

### 5.4 Boys vs Girls Hostel Comparison

> Side-by-side metric card — Director's quick equity check.

| Metric | Boys Hostels | Girls Hostels |
|---|---|---|
| Total Capacity | [N] beds | [N] beds |
| Occupancy | [N] (%) | [N] (%) |
| Open Welfare Incidents | [N] | [N] |
| Mess Hygiene Score | [N]% | [N]% |
| Fee Collection Rate | [N]% | [N]% |
| Security Alerts Open | [N] | [N] |

[View Boys Details →] → Page 02 | [View Girls Details →] → Page 03

---

### 5.5 Quick Access Grid

8 tiles (2×4):
| Tile | Label | Link |
|---|---|---|
| 1 | Hosteler Registry | `/group/hostel/hostelers/` |
| 2 | Occupancy Overview | `/group/hostel/occupancy/` |
| 3 | Welfare Incidents | `/group/hostel/welfare/incidents/` |
| 4 | Mess Operations | `/group/hostel/mess/` |
| 5 | Fee Collection | `/group/hostel/fees/collection/` |
| 6 | Security Dashboard | `/group/hostel/security/dashboard/` |
| 7 | Hostel MIS Report | `/group/hostel/reports/mis/` |
| 8 | Hostel Policy Manager | `/group/hostel/policy/` |

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-hostel-detail`
- **Trigger:** Branch Health Matrix → branch name or Actions → View
- **Width:** 640px
- **Tabs:** Overview · Welfare · Mess · Security · Medical · Discipline
- **Overview tab:** Capacity, occupancy, fee collection %, room breakdown
- **Welfare tab:** Open incidents list with severity + age
- **Mess tab:** Latest audit score, menu this week, last inspection date
- **Security tab:** Guard roster, open alerts, CCTV coverage %
- **Medical tab:** Last 7 days visits, doctor schedule
- **Discipline tab:** Open cases list

### 6.2 Modal: Escalate Welfare Incident
- **Trigger:** Critical Queue → Escalate →
- **Type:** Centred modal (480px)
- **Content:** Incident summary + escalation reason (required) + escalate to: Group COO / Group Chairman (radio)
- **On confirm:** POST to escalation endpoint; email/WhatsApp notification sent; audit log entry created

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| KPI bar loaded | — | — | Silent |
| Incident escalated | "Incident escalated to [Role]. They have been notified via WhatsApp." | Warning | 6s |
| Export triggered | "Daily hostel report export started. Ready shortly." | Info | 4s |
| KPI load error | "Failed to load KPI data. Retrying…" | Error | Manual dismiss |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No critical alerts | "All clear — hostels running normally" | "No Severity 1 or 2 welfare incidents are open." | — |
| No branches in table (filter) | "No hostel branches match your filters" | "Try adjusting branch or welfare status filters." | [Clear Filters] |
| No hostel data at all | "No Hostel Data Available" | "No hostel campuses have been configured for this group." | [Go to Settings] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: alert bar + 8 KPI cards + branch table (5 rows) + 3 chart placeholders |
| Table search / filter / page | Inline skeleton rows replace table body |
| KPI auto-refresh (every 5m) | Shimmer over card values only |
| Escalation modal confirm | Spinner on Confirm button; modal closes on success |
| Branch detail drawer open | Centred spinner in drawer; tabs load lazily |

---

## 10. Role-Based UI Visibility

| Element | Hostel Director G3 | Others |
|---|---|---|
| Page itself | ✅ Rendered | ❌ Redirected to own dashboard |
| Alert Banner | ✅ All severity alerts | N/A |
| Escalate → button | ✅ Enabled | N/A |
| Export Daily Report | ✅ Shown | N/A |
| Bulk export checkbox | ✅ Shown | N/A |
| Boys vs Girls comparison | ✅ Both sides | N/A |

> All visibility decisions rendered server-side in Django template. No client-side role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/director/dashboard/` | JWT (G3+) | Full dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/director/kpi-cards/` | JWT (G3+) | KPI cards (auto-refresh) |
| GET | `/api/v1/group/{group_id}/hostel/branches/` | JWT (G3+) | Hostel branch health table |
| GET | `/api/v1/group/{group_id}/hostel/branches/{branch_id}/detail/` | JWT (G3+) | Branch detail drawer |
| GET | `/api/v1/group/{group_id}/hostel/welfare/incidents/?severity=1,2&status=open` | JWT (G3+) | Critical incident queue |
| POST | `/api/v1/group/{group_id}/hostel/welfare/incidents/{id}/escalate/` | JWT (G3+) | Escalate incident |
| GET | `/api/v1/group/{group_id}/hostel/trends/` | JWT (G3+) | 12-month trend data for charts |
| GET | `/api/v1/group/{group_id}/hostel/gender-comparison/` | JWT (G3+) | Boys vs Girls comparison metrics |
| GET | `/api/v1/group/{group_id}/hostel/branches/export/?format=csv` | JWT (G3+) | Export branch health table |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../director/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch search | `input delay:300ms` | GET `.../hostel/branches/?q={val}` | `#hostel-branch-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../hostel/branches/?{filters}` | `#hostel-branch-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../hostel/branches/?page={n}` | `#hostel-branch-table-section` | `innerHTML` |
| Sort click | `click` | GET `.../hostel/branches/?sort={col}&dir={asc/desc}` | `#hostel-branch-table-section` | `innerHTML` |
| Open branch detail | `click` | GET `.../branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Escalate incident | `click` (form submit) | POST `.../incidents/{id}/escalate/` | `#critical-queue-section` | `innerHTML` |
| Chart filter change | `change` | GET `.../hostel/trends/?branch={}&year={}` | `#hostel-trend-chart-data` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
