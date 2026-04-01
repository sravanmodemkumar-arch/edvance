# 06 — Transport Safety Officer Dashboard

> **URL:** `/group/transport/safety/`
> **File:** `06-transport-safety-officer-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Transport Safety Officer (Role 84, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Transport Safety Officer. Command centre for all transport safety operations across branches — GPS live tracking, accident/incident monitoring, driver safety compliance, safety inspections, emergency protocol management, and student safety alerts.

The Transport Safety Officer's primary mission: ensure no student is ever put at risk in a group vehicle. This means zero tolerance for expired licences, missing GPS devices, unresolved incidents, or uncertified drivers. They escalate all severity-1 safety incidents directly to the Group Transport Director and Group COO.

Scale: 200–500 buses · GPS monitoring for all buses during school hours · Safety inspections quarterly.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Safety Officer | G3 | Full — all safety sections | Exclusive dashboard |
| Group Transport Director | G3 | View — incidents and GPS | Via own dashboard |
| Group Fleet Manager | G3 | View — maintenance overlap with safety | Read only |
| Group Route Planning Manager | G3 | ❌ No access — own dashboard at /routes/ | Redirect to Page 03 |
| Group Transport Fee Manager | G3 | ❌ No access — own dashboard at /fees/ | Redirect to Page 04 |
| Group Driver/Conductor HR | G0 | ❌ No EduForge login | See Page 05 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Transport Safety Officer Dashboard
```

### 3.2 Page Header
```
Welcome back, [Officer Name]              [Report Incident]  [Export Safety Report ↓]  [Settings ⚙]
Group Transport Safety Officer · AY [current academic year]
GPS Live: [N] buses online  ·  Open Incidents: [N]  ·  Compliance Score: [N]%
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Severity 1 incident (accident with injury) unresolved | "CRITICAL: Severity 1 incident at [Branch] — students injured. Immediate escalation required." | Red |
| GPS offline > 20 min during school hours | "[N] buses lost GPS signal for > 20 minutes during school hours. Safety gap." | Red |
| Driver with expired licence on duty | "[N] drivers with expired licences are currently on duty." | Red |
| Safety inspection overdue > 30 days | "[N] vehicles have overdue safety inspections." | Amber |
| Emergency protocol not updated > 90 days | "[N] branches have emergency protocols not updated in > 90 days." | Amber |

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| GPS Live Coverage | % buses with GPS now | Green ≥ 95% · Yellow 80–95% · Red < 80% | → Page 18 |
| Open Incidents | Unresolved accidents / incidents | Green = 0 · Yellow 1–5 · Red > 5 | → Page 23 |
| Severity 1 Open | Critical unresolved incidents | Red if > 0 | → Page 23 (Sev 1 filter) |
| Driver Licence Compliance | % drivers with valid licence | Green ≥ 98% · Yellow 90–98% · Red < 90% | → Page 16 |
| Safety Inspections Due | Vehicles needing inspection | Yellow > 5 · Red > 15 | → Page 24 |
| Student Safety Alerts (today) | Active alerts (late bus, etc.) | Yellow > 0 | → Page 26 |
| Incident-Free Days | Days since last incident | Green > 30 · Yellow 7–30 · Red < 7 | — |
| Emergency Protocols Updated | % branches up to date | Green ≥ 95% · Red < 95% | → Page 25 |

**HTMX:** `hx-trigger="every 3m"` → GPS and incidents auto-refresh.

---

## 5. Sections

### 5.1 Live GPS Status Panel

> Real-time GPS status overview — first thing Safety Officer checks.

- Count of buses currently online / offline / in geo-fence alert zone
- Buses offline > 10 min listed: Bus No · Branch · Last Known Location · Minutes Offline · [Escalate]
- "Open Full GPS Map →" → Page 18

---

### 5.2 Open Incidents Table

> All unresolved safety incidents across branches.

**Columns:** Date · Branch · Bus No · Incident Type · Severity (1–4) · Students Involved · Assigned To · Days Open · [View →]

**Default sort:** Severity ascending · Date descending within severity.
**Pagination:** Server-side · 25/page.

"View full incident register →" → Page 23.

---

### 5.3 Student Safety Alerts (Today)

> Active alerts for the current school day.

**Columns:** Alert Type · Branch · Bus No · Route · Time Triggered · Status · [Resolve]

Alert Types: Late Bus (> 15 min) · Geo-fence Breach · SOS Button Pressed · Overcrowding Alert · Bus Breakdown.

"View all alerts →" → Page 26.

---

### 5.4 Driver Safety Compliance Table (Branch-wise)

> Per-branch driver compliance at a glance.

**Columns:** Branch · Drivers Active Today · Licence Valid % · Training Current % · BGV Clear % · [View Details →]

"View driver licence tracker →" → Page 16.

---

### 5.5 Safety Inspection Status (Chart)

**Chart — Inspection Completion (Bar)**
- Branches vs % of fleet with completed quarterly inspection
- Red bar for branches < 80% complete

---

## 6. Drawers

### 6.1 Modal: `report-incident` — Quick Incident Report
- **Trigger:** Report Incident button
- **Width:** 520px
- **Fields:** Branch · Date/Time · Bus No · Route · Incident Type · Severity (1 Minor / 2 Moderate / 3 Serious / 4 Critical) · Location (free text + GPS coords if available) · Students Involved (count) · Injuries (Yes/No) · Driver Name · Description · Immediate Actions Taken · Notify COO (checkbox, mandatory for Sev 3–4) · Upload Photos
- **Validation:** Severity 3–4 requires COO notification
- **On save:** Incident created; notifications sent per severity

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Incident reported | "Incident [ID] recorded at [Branch]. Notifications sent." | Warning | 6s |
| GPS alert escalated | "GPS offline alert escalated to [Branch] transport in-charge." | Warning | 6s |
| Safety inspection scheduled | "Safety inspection scheduled for [N] vehicles at [Branch]." | Info | 4s |
| Alert resolved | "Safety alert resolved. Route [Name] back on track." | Success | 4s |
| Alert resolve failed | "Failed to resolve alert. Please retry." | Error | 5s |
| Incident report failed | "Failed to submit incident report. Please retry." | Error | 5s |
| Inspection schedule failed | "Failed to schedule inspection. Check vehicle status." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open incidents | "No Open Incidents" | "All transport safety incidents are resolved." | — |
| All GPS online | "Full GPS Coverage" | "All buses are transmitting GPS signal." | — |
| No alerts today | "No Safety Alerts Today" | "No active student safety alerts for today." | — |
| Incidents table — no filter results | "No Incidents Match Filters" | "Adjust severity, type, or branch filters." | [Clear Filters] |
| Incidents table — no search results | "No Incidents Found for '[term]'" | "Check the bus number or branch." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + GPS panel + incidents table + alerts + chart |
| GPS / incident refresh | Inline shimmer on those sections |
| Incident modal | Spinner on Save |

---

## 10. Role-Based UI Visibility

| Element | Safety Officer G3 | Transport Director G3 | Fleet Manager G3 |
|---|---|---|---|
| Report Incident | ✅ | ✅ | ❌ |
| Escalate to COO | ✅ | ✅ | ❌ |
| Schedule Safety Inspection | ✅ | ✅ | ✅ |
| View GPS Map | ✅ | ✅ | ✅ |
| View Driver Compliance | ✅ | ✅ | ❌ |
| Export Safety Report | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/safety/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/transport/safety/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/transport/gps/live/` | JWT (G3+) | GPS live status |
| GET | `/api/v1/group/{group_id}/transport/incidents/?status=open` | JWT (G3+) | Open incidents |
| GET | `/api/v1/group/{group_id}/transport/safety-alerts/today/` | JWT (G3+) | Today's alerts |
| GET | `/api/v1/group/{group_id}/transport/driver-compliance/branch-summary/` | JWT (G3+) | Driver compliance table |
| POST | `/api/v1/group/{group_id}/transport/incidents/` | JWT (G3+) | Create incident |
| POST | `/api/v1/group/{group_id}/transport/safety-alerts/{id}/resolve/` | JWT (G3+) | Resolve alert |
| GET | `/api/v1/group/{group_id}/transport/safety/inspection-chart/` | JWT (G3+) | Inspection chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI + GPS auto-refresh | `every 3m` | GET `.../safety/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| GPS panel refresh | `every 3m` | GET `.../gps/live/` | `#gps-status-panel` | `innerHTML` |
| Incidents table search | `input delay:300ms` | GET `.../incidents/?q={val}&status=open` | `#incidents-table-body` | `innerHTML` |
| Incidents table sort | `click` on header | GET `.../incidents/?sort={col}&dir={asc/desc}&status=open` | `#incidents-table-section` | `innerHTML` |
| Incidents table pagination | `click` | GET `.../incidents/?page={n}&status=open` | `#incidents-table-section` | `innerHTML` |
| Report incident submit | `click` | POST `.../incidents/` | `#incidents-section` | `innerHTML` |
| Resolve alert | `click` | POST `.../safety-alerts/{id}/resolve/` | `#alert-row-{id}` | `outerHTML` |
| Export safety report | `click` | GET `.../safety/dashboard/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
