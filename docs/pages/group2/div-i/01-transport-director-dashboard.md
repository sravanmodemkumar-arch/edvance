# 01 — Transport Director Dashboard

> **URL:** `/group/transport/director/`
> **File:** `01-transport-director-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Transport Director (Role 79, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Transport Director. Single-screen command centre for the entire transport system across all branches — fleet health, route coverage, GPS live status, driver/conductor compliance, transport fee collection, safety incidents, and fitness/permit expiry alerts.

The Transport Director owns fleet policy, approves new routes, monitors GPS tracking, and escalates safety incidents to the Group COO. Large groups run 200–500 buses across all branches; this dashboard gives a real-time picture of the entire fleet. Day scholars depend on transport — any bus breakdown, route gap, or driver absence creates an immediate student safety issue.

Scale: 200–500 buses · 300–800 routes · 3,000–15,000 day scholars on transport · 500–1,000 drivers and conductors.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Director | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group Fleet Manager | G3 | ❌ No access — own dashboard at /fleet/ | Redirect to Page 02 |
| Group Route Planning Manager | G3 | ❌ No access — own dashboard at /routes/ | Redirect to Page 03 |
| Group Transport Fee Manager | G3 | ❌ No access — own dashboard at /fees/ | Redirect to Page 04 |
| Group Driver/Conductor HR | G0 | ❌ No EduForge login | See Page 05 |
| Group Transport Safety Officer | G3 | ❌ No access — own dashboard at /safety/ | Redirect to Page 06 |
| Group Chairman / CEO | G5 / G4 | View — via governance reports only | Not this URL |
| Group COO | G4 | View — via operations portal | Not this URL |

> **Access enforcement:** Django view decorator `@require_role('transport_director')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Director Dashboard
```

### 3.2 Page Header
```
Welcome back, [Director Name]                    [Export Daily Transport Report ↓]  [Settings ⚙]
[Group Name] — Group Transport Director · Last login: [date time]
AY [current academic year]  ·  [N] Buses  ·  [N] Routes  ·  [N] Branches
```

### 3.3 Alert Banner (conditional — critical items requiring same-day action)

| Condition | Banner Text | Severity |
|---|---|---|
| Vehicle fitness cert expired | "[N] vehicles have expired fitness certificates. Cannot operate legally." | Red |
| Vehicle insurance expired | "[N] vehicles have expired insurance policies. Immediate renewal required." | Red |
| Accident/incident reported last 24h | "Transport incident reported at [Branch] — [N] students involved. Review incident log." | Red |
| GPS device offline > 30 min during school hours | "[N] GPS devices offline during school hours. Safety monitoring gap." | Red |
| Driver license expired | "[N] drivers have expired licences. Cannot operate." | Red |
| Route without driver assignment | "[N] routes have no assigned driver for tomorrow." | Amber |
| Transport fee collection < 70% for any branch | "[Branch] transport fee collection is only [N]% this month." | Amber |
| Permit expiry within 7 days | "[N] vehicle permits expiring in 7 days. Renew immediately." | Amber |

Max 5 alerts visible. Alert-type links route to relevant pages. "View all audit events → Transport Audit Log (Page 33)" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Buses (Active) | Count of operational fleet | Blue always | → Page 07 |
| Routes Operational | Routes with assigned bus + driver today | Green = 100% · Yellow < 100% · Red < 90% | → Page 11 |
| GPS Live Coverage | % of buses transmitting GPS signal now | Green ≥ 95% · Yellow 80–95% · Red < 80% | → Page 18 |
| Transport Fee Collection % | This month | Green ≥ 85% · Yellow 65–85% · Red < 65% | → Page 21 |
| Compliance Score | % vehicles with valid fitness + permit + insurance | Green ≥ 95% · Yellow 85–95% · Red < 85% | → Page 31 |
| Open Safety Incidents | Unresolved incidents | Green = 0 · Yellow 1–5 · Red > 5 | → Page 23 |
| Drivers on Duty Today | Count vs required | Green = 100% · Yellow < 100% | → Page 15 |
| Buses Requiring Maintenance | Scheduled + overdue | Yellow > 0 · Red > 10 | → Page 08 |

**HTMX:** `hx-trigger="every 5m"` → GPS coverage and incident counts auto-refresh.

---

## 5. Sections

### 5.1 Fleet Status Overview (Branch-wise Table)

> Per-branch fleet health — Director's primary monitoring table.

**Search:** Branch name, city. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Fleet Compliance | Radio | All / Fully Compliant / Issues Found |
| Has Incidents | Checkbox | Show branches with open incidents only |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → branch transport detail drawer |
| Total Buses | ✅ | Assigned to this branch |
| Operational Today | ✅ | Buses on routes today |
| GPS Coverage | ✅ | % buses with live GPS; colour-coded |
| Compliance | ✅ | % vehicles compliant (fitness/permit/insurance) |
| Routes | ✅ | Active route count |
| Fee Collection % | ✅ | This month |
| Open Incidents | ✅ | Red if > 0 |
| Actions | ❌ | View · Route Map · Incidents |

**Default sort:** Open Incidents descending (worst first).
**Pagination:** Server-side · 25/page.

---

### 5.2 Live GPS Feed (Mini Map Panel)

> Real-time bird's-eye view of all buses currently in operation.

- Embedded map (Leaflet.js) showing all bus markers colour-coded:
  - 🟢 Green = On route, GPS live
  - 🟡 Yellow = Delayed > 10 min
  - 🔴 Red = GPS offline / emergency alert
- Each marker tooltip: Bus No · Route · Driver · ETA at next stop
- "View Full Live Tracking →" → Page 18
- Map refreshes every 30 seconds via HTMX partial update.

---

### 5.3 Compliance Expiry Alerts Table

> Vehicles with fitness cert / permit / insurance expiring within 30 days.

**Columns:** Bus No · Branch · Compliance Type · Expiry Date · Days Remaining · Status · [Renew →]

**Default sort:** Days remaining ascending.
"View full compliance dashboard →" → Page 31.

---

### 5.4 Recent Safety Incidents

> Last 10 incidents across all branches.

**Columns:** Date · Branch · Bus No · Incident Type · Students Involved · Status · [View →]

"View all incidents →" → Page 23.

---

### 5.5 Quick Action Shortcuts

| Action | Target |
|---|---|
| Approve New Route | → Page 11 (route approval queue) |
| View GPS Live Map | → Page 18 |
| Review Driver Compliance | → Page 16 |
| Export Fleet Status Report | Download CSV |
| Transport Policy Manager | → Page 32 |
| Transport Analytics | → Page 29 |
| Monthly MIS Report | → Page 30 |
| Compliance Dashboard | → Page 31 |

---

## 6. Drawers

### 6.1 Drawer: `branch-transport-detail`
- **Width:** 640px
- **Tabs:** Fleet · Routes · GPS Status · Incidents · Fee Collection
- **Fleet:** All buses at branch, compliance status per vehicle
- **Routes:** Active routes with driver assignment status
- **GPS Status:** Live status of each bus at this branch
- **Incidents:** Open + recent closed incidents
- **Fee Collection:** Monthly collection vs target

> **Audit trail:** All actions on this page (route approval, GPS acknowledgement, incident escalation) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Route approved | "Route [Name] approved for [Branch]." | Success | 4s |
| Route approval failed | "Route approval failed. Check route details and retry." | Error | 5s |
| GPS alert acknowledged | "GPS alert acknowledged. Operations team notified." | Info | 4s |
| GPS acknowledgement failed | "Failed to acknowledge GPS alert. Please refresh and retry." | Error | 5s |
| Incident escalated | "Incident escalated to Group COO." | Warning | 6s |
| Incident escalation failed | "Escalation failed. Retry or contact IT support." | Error | 5s |
| Compliance renewal triggered | "Renewal reminder sent for [N] vehicles." | Info | 4s |
| Reminder failed | "Reminder failed to send. Check notification configuration." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches configured | "No Branches with Transport" | "No branches have transport configured yet." | [Configure Branch Transport] |
| No incidents | "No Open Incidents" | "All transport safety incidents are resolved." | — |
| Fleet table — no filter results | "No Branches Match Filters" | "Adjust compliance or incident filters." | [Clear Filters] |
| Fleet table — no search results | "No Branches Found for '[term]'" | "Check the branch name or city." | [Clear Search] |
| No compliance expiry alerts | "No Expiry Alerts" | "All vehicle documents are valid for more than 30 days." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + fleet table + mini map placeholder + alerts |
| Table filter | Inline skeleton rows |
| KPI auto-refresh | Shimmer on card values |
| GPS mini map refresh | Map overlay fade transition |
| Branch detail drawer | 640px drawer skeleton; tabs load lazily |

---

## 10. Role-Based UI Visibility

| Element | Transport Director G3 | Fleet Manager G3 | Safety Officer G3 | Fee Manager G3 |
|---|---|---|---|---|
| Approve Route | ✅ | ❌ | ❌ | ❌ |
| View GPS Map | ✅ | ✅ | ✅ | ❌ |
| View Fee Collection | ✅ | ❌ | ❌ | ✅ |
| Escalate Incident | ✅ | ❌ | ✅ | ❌ |
| Export Report | ✅ | ✅ | ✅ | ✅ |
| Transport Policy Manager | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/transport/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/transport/fleet-status/` | JWT (G3+) | Branch fleet status table |
| GET | `/api/v1/group/{group_id}/transport/gps/live/` | JWT (G3+) | Live GPS feed for mini map |
| GET | `/api/v1/group/{group_id}/transport/compliance-alerts/` | JWT (G3+) | Expiry alerts |
| GET | `/api/v1/group/{group_id}/transport/incidents/recent/` | JWT (G3+) | Last 10 incidents |
| GET | `/api/v1/group/{group_id}/transport/branches/{id}/detail/` | JWT (G3+) | Branch detail drawer |
| GET | `/api/v1/group/{group_id}/transport/fleet-status/export/` | JWT (G3+) | Async CSV export of fleet status |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../transport/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| GPS mini map refresh | `every 30s` | GET `.../transport/gps/live/` | `#gps-mini-map` | `innerHTML` |
| Fleet table search | `input delay:300ms` | GET `.../transport/fleet-status/?q={val}` | `#fleet-table-body` | `innerHTML` |
| Fleet table sort | `click` on header | GET `.../transport/fleet-status/?sort={col}&dir={asc/desc}` | `#fleet-table-section` | `innerHTML` |
| Fleet table pagination | `click` | GET `.../transport/fleet-status/?page={n}` | `#fleet-table-section` | `innerHTML` |
| Filter apply | `click` | GET `.../transport/fleet-status/?{filters}` | `#fleet-table-section` | `innerHTML` |
| Open branch drawer | `click` | GET `.../transport/branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Export report | `click` | GET `.../transport/fleet-status/export/` | `#export-btn` | `outerHTML` (shows spinner then download link) |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
