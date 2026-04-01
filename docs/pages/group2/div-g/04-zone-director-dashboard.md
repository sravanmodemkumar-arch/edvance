# 04 — Zone Director Dashboard

> **URL:** `/group/ops/zone-director/`
> **File:** `04-zone-director-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Zone Director (G4) — exclusive landing page
> **Applicable:** Large groups only (20–50 branches with zone layer)

---

## 1. Purpose

Post-login landing for the Group Zone Director. A zone contains 10–15 branches. The Zone
Director is the management layer between Group HQ and branch principals within their zone.
They oversee ops + academic health of their zone branches, escalate to COO when needed,
and coordinate with Zone Academic and Zone Operations Managers under them.

> **Scoping rule:** Zone Director sees ONLY their assigned zone's branches.
> Platform enforces via `zone.director_id == current_user.id`.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Zone Director | G4 | Full — own zone | Exclusive dashboard |
| Group COO | G4 | View all zones | Has own dashboard |
| Group Operations Manager | G3 | View | |
| Zone Academic Coordinator | G3 | — | Own dashboard |
| Zone Operations Manager | G3 | — | Own dashboard |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Zone Director Dashboard  ›  Zone [Name]
```

### 3.2 Page Header
```
Zone [Name] — Zone Director                        [Escalate to COO ⬆]  [Zone Report ↓]
[Director Name] · [N] Branches · [N] Students · Last login: [date time]
```

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Branches in Zone | `12 branches · 11 active` | Green all active · Yellow 1 down · Red ≥2 | → Page 17 |
| Zone Enrollment | `18,400 students` + trend | Informational | → Page 17 |
| Zone SLA Compliance | `91.2%` | Green ≥95% · Yellow 85–95% · Red <85% | → Page 15 |
| Zone Academic Score | `78.3% avg` | Green ≥80% · Yellow 70–80% · Red <70% | → Page 16 |
| Open Escalations (Zone) | `4 open · 1 P1` | Green =0 P1 · Red ≥1 P1 | → Page 12 |
| Compliance Issues | `6 issues across zone` | Green =0 · Yellow 1–3 · Red ≥4 | → Page 13 |

**HTMX:** `every 5m` → `/api/v1/group/{id}/zone/{zone_id}/director/kpi-cards/` → `#kpi-bar`

---

## 5. Sections

### 5.1 Zone Branch Health Matrix

> All branches in this zone — Zone Director's working table.

**Search:** Branch name, city. Debounce 300ms.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | Link → `branch-ops-detail` drawer |
| Students | ✅ | |
| SLA % | ✅ | Colour-coded |
| Academic Score | ✅ | Avg marks/grade % |
| Open Issues | ✅ | Count |
| Last Visit | ✅ | Red if >30d |
| Compliance Score | ✅ | % |
| Status | ✅ | Active/Inactive |
| Actions | ❌ | View · Escalate · Visit |

**Default sort:** SLA % ascending.

**Pagination:** 25/page. Server-side.

---

### 5.2 Zone Academic vs Operations Split View

**Display:** Two side-by-side summary cards with key metrics:

- Left (Academic): Exam calendar compliance, avg marks this term, attendance %, dropout signals
- Right (Ops): Maintenance open, grievances open, coordinator visit rate, procurement delivery status

**Links:** [Zone Academic Dashboard →] Page 16 · [Zone Ops Dashboard →] Page 15.

---

### 5.3 Zone Escalation Feed

> Last 10 escalations in this zone, newest first.

**Columns:** Priority badge · Branch · Type · Age · Status · [View →]

**Link:** [All Zone Escalations →] → Page 12 filtered to zone.

---

### 5.4 Zone Performance Trend Chart

**Type:** Multi-line — Zone SLA % + Zone Academic Score + Enrollment — over 12 months.

**Library:** Chart.js 4.x. Colorblind-safe. Legend. PNG export.

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-ops-detail` (Zone Director view)
- **Width:** 640px
- **Tabs:** Overview · Academic · Ops · Escalations · Visit History
- **Zone Director can see:** All branch data within zone
- **Cannot see:** Finance details (G4 ops scope, not finance) · Staff individual salary

### 6.2 Drawer: `escalation-create`
- **Width:** 640px
- **Auto-fill:** Branch (from selected row) · Zone (own zone)
- **Note:** Zone Director can raise escalation to COO, or assign to Zone Ops Manager

---

## 7. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Escalation raised | "Escalation raised — COO notified" | Success · 4s |
| Zone report exported | "Zone report export started" | Info · 4s |
| Dashboard refreshed | "Dashboard refreshed" | Info · 4s |

---

## 8. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No zone assigned | "No zone assigned" | "Contact your COO to assign a zone" |
| No open escalations | "Zone operating smoothly" | — |
| No branches in zone | "Zone has no branches" | — |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPI bar + branch table + 2 summary cards + chart |
| Table filter | Inline skeleton rows |
| KPI refresh | Shimmer |
| Drawer open | Spinner in drawer |

---

## 10. Role-Based UI Visibility

| Element | Zone Director G4 | COO G4 (viewing) | Ops Mgr G3 |
|---|---|---|---|
| Own zone data | ✅ Full | ✅ Full | ✅ Read |
| Other zones | ❌ Blocked | ✅ Full | ✅ Read |
| [Escalate to COO] button | ✅ | ✅ | ❌ |
| [Zone Report] export | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/zone/{zone_id}/director/dashboard/` | JWT (G4 zone-scoped) | Full page data |
| GET | `/api/v1/group/{id}/zone/{zone_id}/director/kpi-cards/` | JWT (G4) | KPI cards |
| GET | `/api/v1/group/{id}/ops/branches/?zone_id={zone_id}` | JWT (G4) | Zone branches |
| GET | `/api/v1/group/{id}/zone/{zone_id}/academic-ops-split/` | JWT (G4) | Split view data |
| GET | `/api/v1/group/{id}/escalations/?zone_id={zone_id}&limit=10` | JWT (G4) | Zone escalations |
| GET | `/api/v1/group/{id}/zone/{zone_id}/trend/` | JWT (G4) | 12-month trend |
| POST | `/api/v1/group/{id}/escalations/` | JWT (G4) | Raise zone escalation |
| GET | `/api/v1/group/{id}/zone/{zone_id}/report/?format=pdf` | JWT (G4) | Export zone report |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get | hx-target | hx-swap |
|---|---|---|---|---|
| Branch search | `input delay:300ms` | `/api/.../branches/?zone_id={}&q={val}` | `#zone-branch-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../branches/?zone_id={}&filters={}` | `#zone-branch-table-section` | `innerHTML` |
| KPI auto-refresh | `every 5m` | `/api/.../zone/{id}/director/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Open branch detail | `click` | `/api/.../branches/{id}/detail/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
