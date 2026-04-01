# 04 — Emergency Response Officer Dashboard

> **URL:** `/group/health/emergency/`
> **File:** `04-emergency-response-officer-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Emergency Response Officer (Role 89, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Emergency Response Officer. Command centre for monitoring emergency readiness across all branches — drill completion compliance, Standard Operating Procedure (SOP) availability and review status, hospital tie-up coverage, first responder training currency, and live emergency incident monitoring.

The Emergency Response Officer is responsible for ensuring that every branch is prepared to respond to fire, medical, seismic, and security emergencies. They maintain the group-wide emergency framework, run mandatory drill schedules, ensure every branch has hospital agreements, and coordinate the live response to any active emergency anywhere in the group. Any gap in drill compliance or expired first responder certification represents a regulatory and safety liability. Scale: 20–50 branches × 4 mandatory drill types = 80–200 drills/year · 5–50 actual emergency incidents per year.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Emergency Response Officer | G3 | Full — all sections, incident management, SOP management | Exclusive dashboard |
| Group Medical Coordinator | G3 | View — medical incidents and hospital directory only | No SOP edit access |
| Group CEO / COO | G5 / G4 | View all sections + escalate authority | Not this URL (governance portal) |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('emergency_response_officer')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Emergency Response Dashboard
```

### 3.2 Page Header
```
Welcome back, [Officer Name]                   [Export Readiness Report ↓]  [🚨 Report Incident]  [Settings ⚙]
[Group Name] — Group Emergency Response Officer · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  Drill Compliance: [N]%  ·  Open Incidents: [N]
```

### 3.3 Alert Banner (conditional — critical safety items)

| Condition | Banner Text | Severity |
|---|---|---|
| Active emergency incident | "🚨 ACTIVE EMERGENCY: [Type] at [Branch] — reported [N] minutes ago. [View Incident →]" | Red (persistent, flashing border) |
| First responder certification expired | "[N] first responders across [N] branches have expired certifications. Cannot legally respond." | Red |
| Drill overdue > 30 days | "[Branch] fire drill is [N] days overdue. Compliance breach." | Red |
| Branch missing ambulance contact | "[N] branches have no ambulance contact registered. Emergency response gap." | Red |
| SOP not reviewed > 6 months | "[N] SOPs across [N] branches have not been reviewed in 6+ months." | Amber |
| Hospital tie-up missing | "[N] branches have no hospital tie-up agreement registered." | Amber |
| Drill scheduled but not completed (within 3 days of due date) | "[Branch] [Type] drill is due in [N] days and not yet scheduled." | Amber |

Max 5 alerts visible. Active emergency alert is always shown at top, cannot be dismissed. "View full incident log →" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Drill Compliance % (This Year) | % of scheduled drills completed across all branches | Green ≥ 90% · Yellow 70–90% · Red < 70% | → Section 5.3 |
| Branches with All Drills Complete | Count of branches with all 4 drill types done this year | Green = all branches · Yellow < 90% · Red < 75% | → Section 5.1 |
| Open Emergency Incidents | Active/unresolved incidents across all branches | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.2 |
| Branches Missing Hospital Tie-up | Branches with no registered hospital agreement | Green = 0 · Yellow 1–2 · Red > 2 | → Section 5.1 |
| First Responders Trained % | Staff with current (non-expired) first responder certification | Green ≥ 90% · Yellow 75–90% · Red < 75% | → Section 5.1 |
| SOPs Published & Active | Total active SOPs across all branches and types | Blue always | → SOP Library |
| Drills Overdue | Scheduled drills whose due date has passed, not completed | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.4 |
| Branches with Expired First Aid Certifications | Branches where any first responder cert is expired | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.1 |

**HTMX:** `hx-trigger="every 2m"` → Open incidents and active emergency auto-refresh. `hx-trigger="every 10m"` → All other KPIs.

---

## 5. Sections

### 5.1 Branch Emergency Readiness Matrix

> Comprehensive per-branch grid of all emergency readiness dimensions. This is the Officer's primary status board.

**Search:** Branch name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Drill Status | Checkbox | All Complete / Partial / None Complete |
| Hospital Tie-up | Radio | All / Present / Missing |
| First Responder Status | Radio | All / Certified / Expiring / Expired |
| Has Open Incident | Checkbox | Show branches with open incidents only |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → `branch-emergency-detail` drawer |
| Fire Drill | ✅ | ✅ Done (date) / ⚠ Due Soon / ❌ Overdue / — Not Scheduled |
| Medical Emergency Drill | ✅ | Same status pattern |
| Earthquake / Evacuation Drill | ✅ | Same status pattern |
| Security Emergency Drill | ✅ | Same status pattern |
| Hospital Tie-up | ✅ | ✅ Registered / ❌ Missing |
| Trained First Responders | ✅ | Count; colour: Green ≥ 3 · Yellow 1–2 · Red 0 |
| Cert Expiry (Earliest) | ✅ | Date of next expiring responder cert; Red if past |
| Last Incident | ✅ | Date of most recent incident or — |
| Actions | ❌ | View · Schedule Drill · View SOPs |

**Default sort:** Overall readiness score (worst first) — calculated as: 0 incomplete drills × weight + missing hospital × weight + expired certs × weight.
**Pagination:** Server-side · 25/page.

---

### 5.2 Active Incidents (Live)

> Live feed of any currently ongoing or recently reported emergency incidents.

> **HTMX auto-refresh:** `hx-trigger="every 2m"` on this section.

**Search:** Branch, incident type. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Status | Checkbox | Active / Monitoring / Contained / Resolved / Closed |
| Type | Checkbox | Fire / Medical Emergency / Earthquake / Security / Flood / Other |
| Severity | Radio | All / Minor / Moderate / Major / Critical |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Incident ID | ✅ | Auto-generated; link → incident detail drawer |
| Date & Time | ✅ | Reported timestamp |
| Branch | ✅ | |
| Type | ✅ | |
| Description | ❌ | Brief free-text (first 80 chars) |
| Severity | ✅ | Red badge for Critical/Major |
| Persons Affected | ✅ | Count of students/staff involved |
| Status | ✅ | Active (Red) / Monitoring (Orange) / Contained (Yellow) / Resolved (Green) |
| Response Lead | ✅ | Officer in charge at branch |
| Actions | ❌ | View · Update Status · Escalate |

**Default sort:** Status (Active first), then Date (most recent first).
No pagination — all active incidents displayed (typically < 10).

---

### 5.3 Drill Compliance Chart

> Visual summary of drill completion status across all branches for the current academic year.

**Chart type:** Two charts side by side:
1. **Pie chart** — Proportion of branches: Fully Compliant (all 4 drills) / Partially Compliant (1–3 drills) / Non-Compliant (0 drills)
2. **Bar chart** — Per-drill-type completion rate: Fire / Medical / Earthquake / Security — each bar shows % of branches completed

**Below charts:** Summary table:
| Drill Type | Branches Done | Branches Pending | Branches Overdue |
|---|---|---|---|
| Fire Drill | N | N | N |
| Medical Emergency Drill | N | N | N |
| Earthquake / Evacuation Drill | N | N | N |
| Security Emergency Drill | N | N | N |

"View and schedule all drills →" → Section 5.4.

---

### 5.4 Upcoming Drills Calendar

> All drills scheduled in the next 30 days across all branches.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Scheduled Date | ✅ | |
| Branch | ✅ | |
| Drill Type | ✅ | Fire / Medical / Earthquake / Security |
| Coordinator at Branch | ✅ | Branch-level coordinator name |
| Participants Expected | ✅ | Count |
| External Agency | ✅ | Fire Dept / Ambulance / Police or — |
| Status | ✅ | Scheduled / Confirmed / Completed / Cancelled |
| Actions | ❌ | View · Edit · Mark Complete · Cancel |

**Default sort:** Date ascending.
No pagination (30-day window).

---

### 5.5 Quick Actions

| Action | Target |
|---|---|
| Report Incident | Opens `incident-report` drawer — immediate incident logging |
| Schedule Drill | Opens `drill-schedule` drawer — branch, type, date, participants |
| View SOP Library | → SOP Library overlay (filter by branch, category, review status) |
| Export Readiness Report | Download PDF/XLSX — full readiness matrix all branches |
| View Hospital Directory | → Hospital tie-up directory modal (all registered hospitals by branch) |

---

## 6. Drawers

### 6.1 Drawer: `branch-emergency-detail`
- **Trigger:** Branch name link in Section 5.1
- **Width:** 640px
- **Tabs:** Drills · SOPs · Hospital Directory · First Responders · Incidents

**Drills tab:**
- This year's drill log: type, scheduled date, actual date, status, participants count, external agency, observation notes
- Next upcoming drills (if scheduled)
- "Schedule Drill" button

**SOPs tab:**
- List of all SOPs applicable to this branch: name, category (Fire/Medical/Earthquake/Security/General), version, last reviewed, reviewed by, status (Active/Under Review/Archived)
- "Review SOP" action opens SOP content in a nested modal

**Hospital Directory tab:**
- Registered hospital tie-up(s): hospital name, address, contact person, emergency number, MOU date, MOU expiry, beds reserved, distance from branch
- "Add Hospital" button

**First Responders tab:**
- Staff certified as first responders: name, designation, certification type (Basic/Advanced First Aid / CPR / AED), certifying body, issue date, expiry date, status (Valid/Expiring/Expired)
- "Add Responder" button

**Incidents tab:**
- All incidents at this branch: date, type, severity, status, description, resolution summary
- "Report New Incident" button

### 6.2 Drawer: `incident-report`
- **Trigger:** "Report Incident" quick action or "Report New Incident" in branch drawer
- **Width:** 600px
- **Fields:** Branch (select) · Incident Date/Time (datetime; default now) · Type (select) · Severity (radio: Minor / Moderate / Major / Critical) · Location within campus (text) · Description (textarea) · Persons Affected (number) · Response Lead at Branch (text) · Immediate Actions Taken (textarea) · External Agencies Notified (checkboxes: Fire Dept / Ambulance / Police / Hospital) · Status (radio: Active / Monitoring / Contained) · Attachments (photos/files, optional)
- **Validation:** Branch, type, severity, description mandatory. If Critical severity → system auto-alerts Group COO and CEO.

### 6.3 Drawer: `drill-schedule`
- **Trigger:** "Schedule Drill" quick action or Drills tab button
- **Width:** 560px
- **Fields:** Branch (select) · Drill Type (select) · Scheduled Date (date) · Scheduled Time (time) · Duration (select: 30min/1hr/2hr) · Coordinator at Branch (select from staff) · Participants Expected (number) · External Agency (optional text + contact) · Pre-drill checklist (checkbox list of required preparations) · Notes

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Incident reported | "Emergency incident reported at [Branch]. Incident ID: [ID]." | Warning | 6s |
| Incident status updated | "Incident [ID] status updated to [Status]." | Info | 4s |
| Incident escalated to COO | "Incident [ID] at [Branch] escalated to Group COO." | Warning | 6s |
| Drill scheduled | "Drill scheduled: [Type] at [Branch] on [date]." | Success | 4s |
| Drill marked complete | "[Type] drill at [Branch] marked complete." | Success | 4s |
| Drill cancelled | "[Type] drill at [Branch] cancelled." | Warning | 5s |
| Readiness report exported | "Readiness report export ready. Download now." | Info | 4s |
| SOP reviewed | "SOP '[Name]' reviewed and updated. Next review: [date]." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No active incidents | "No Active Emergency Incidents" | "All branches are clear. No active emergencies being monitored." | — |
| No drills in next 30 days | "No Drills Scheduled" | "No emergency drills are scheduled in the next 30 days." | [Schedule Drill] |
| All drills compliant | "All Drills Completed" | "All branches have completed all required drills for this academic year." | — |
| No overdue drills | "No Overdue Drills" | "No drills are overdue across any branch." | — |
| Branch search no results | "No Branches Found" | "No branches match your search or filters." | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + readiness matrix table + active incidents table + chart placeholders + drill calendar + alerts |
| Active incidents auto-refresh | Shimmer overlay on incidents section only |
| KPI auto-refresh | Shimmer on card values |
| Readiness matrix filter | Table body skeleton (8 rows × 10 columns) |
| Branch detail drawer | 640px drawer skeleton; each tab loads lazily |
| Incident report drawer | 600px form skeleton |
| Drill compliance charts | Circular shimmer for pie + bar placeholder (300px × 200px each) |

---

## 10. Role-Based UI Visibility

| Element | Emergency Response Officer G3 | Medical Coordinator G3 | CEO / COO |
|---|---|---|---|
| Report Incident | ✅ | ❌ | ❌ |
| Update Incident Status | ✅ | ❌ | ❌ |
| Escalate Incident | ✅ | ✅ (medical incidents) | ✅ |
| Schedule Drill | ✅ | ❌ | ❌ |
| Manage SOPs | ✅ | ❌ | ❌ |
| View Hospital Directory | ✅ | ✅ | ✅ |
| Manage First Responders | ✅ | ❌ | ❌ |
| View Readiness Matrix | ✅ | ✅ | ✅ |
| Export Report | ✅ | ❌ | ✅ |
| View All Incidents | ✅ | ✅ (medical only) | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/emergency/dashboard/` | JWT (G3+) | Full dashboard data |
| GET | `/api/v1/group/{group_id}/health/emergency/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/health/emergency/readiness-matrix/` | JWT (G3+) | Branch readiness matrix |
| GET | `/api/v1/group/{group_id}/health/emergency/incidents/active/` | JWT (G3+) | Live active incidents |
| POST | `/api/v1/group/{group_id}/health/emergency/incidents/` | JWT (G3+) | Report new incident |
| PATCH | `/api/v1/group/{group_id}/health/emergency/incidents/{id}/` | JWT (G3+) | Update incident |
| POST | `/api/v1/group/{group_id}/health/emergency/incidents/{id}/escalate/` | JWT (G3+) | Escalate to COO |
| GET | `/api/v1/group/{group_id}/health/emergency/drill-compliance/` | JWT (G3+) | Drill compliance chart data |
| GET | `/api/v1/group/{group_id}/health/emergency/drills/upcoming/` | JWT (G3+) | Next 30 days drills |
| POST | `/api/v1/group/{group_id}/health/emergency/drills/` | JWT (G3+) | Schedule new drill |
| PATCH | `/api/v1/group/{group_id}/health/emergency/drills/{id}/` | JWT (G3+) | Update/complete/cancel drill |
| GET | `/api/v1/group/{group_id}/health/emergency/branches/{branch_id}/detail/` | JWT (G3+) | Branch emergency detail (all tabs) |
| GET | `/api/v1/group/{group_id}/health/emergency/export/` | JWT (G3+) | Async readiness report export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Active incidents refresh | `every 2m` | GET `.../incidents/active/` | `#active-incidents-section` | `innerHTML` |
| KPI refresh | `every 10m` | GET `.../emergency/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Readiness matrix search | `input delay:300ms` | GET `.../readiness-matrix/?q={val}` | `#matrix-table-body` | `innerHTML` |
| Readiness matrix filter | `click` | GET `.../readiness-matrix/?{filters}` | `#matrix-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../readiness-matrix/?page={n}` | `#matrix-table-section` | `innerHTML` |
| Open branch drawer | `click` on branch name | GET `.../branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Branch drawer tab switch | `click` | GET `.../branches/{id}/detail/?tab={name}` | `#drawer-tab-content` | `innerHTML` |
| Submit incident report | `click` | POST `.../incidents/` | `#active-incidents-section` | `innerHTML` |
| Update incident status | `click` | PATCH `.../incidents/{id}/` | `#incident-row-{id}` | `outerHTML` |
| Mark drill complete | `click` | PATCH `.../drills/{id}/` | `#drill-row-{id}` | `outerHTML` |
| Load drill chart data | `load` | GET `.../drill-compliance/` | `#drill-chart-container` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
