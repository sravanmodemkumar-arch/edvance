# 04 — CCTV & Security Dashboard

> **URL:** `/group/welfare/security/`
> **File:** `04-cctv-security-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group CCTV & Security Head (Role 93, G3) — exclusive post-login landing (Large groups only)

---

## 1. Purpose

Primary post-login landing for the Group CCTV & Security Head. Command centre for physical security infrastructure across all branches — CCTV camera coverage status, security guard deployment against mandated minimums, visitor management policy compliance, and security incident monitoring and resolution. This dashboard is enabled only for groups operating 20 or more branches, where centralised security governance is mandated by the group board.

The Group CCTV & Security Head sets camera coverage standards — defining minimum coverage rules by area type (main gate, perimeter wall, corridors, classrooms, hostel blocks, parking areas, server rooms) — and audits every branch's compliance against those standards. They manage security guard vendor contracts at the group level, ensure guard counts at each branch meet the calculated deployment floor (derived from campus footprint and student count), monitor all security incidents reported by branches, and ensure visitor management systems are operational and used. Any branch with a non-functional gate camera, a guard count below 50% of required, or an unreported security incident within 24 hours triggers an immediate escalation obligation.

Scale: 20–50 branches · 10–100 cameras per branch · 500–5,000 cameras total across the group · 20–200 security guards · 5–100 security incidents/year.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group CCTV & Security Head | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group COO | G4 | View — incidents and overall compliance summary | Read-only |
| Group Chairman / CEO | G5 / G4 | View — via governance reports only | Not this URL |
| Branch Security Officer | G2 | View — own branch CCTV, guards, incidents | Branch-scoped, not this URL |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('cctv_security_head')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  CCTV & Security Dashboard
```

### 3.2 Page Header
```
Welcome back, [Head Name]                   [Export Security Report ↓]  [Settings ⚙]
[Group Name] — Group CCTV & Security Head · Last login: [date time]
[N] Branches  ·  [N] Total Cameras  ·  [N] Non-Functional  ·  [N] Open Incidents
```

### 3.3 Alert Banner (conditional — critical items requiring same-day action)

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with no functional gate camera | "[Branch] has no functional main gate camera. Gate security is unmonitored. Fix immediately." | Red |
| Security incident unreported > 24 hours | "[N] security incident(s) at [Branch] have not been formally reported within the 24-hour window." | Red |
| Guard count below 50% of required | "[Branch] has only [N] guards on duty against a required [N]. Immediate deployment required." | Red |
| Camera non-functional > 72 hours | "[N] camera(s) at [Branch] have been non-functional for over 72 hours. Maintenance escalation required." | Amber |
| Visitor management not in use | "[Branch] has not logged any visitors in the past 7 days. Visitor management compliance check required." | Amber |

Max 5 alerts visible. Alert links route to the relevant branch row or incident record. "View all security events → Security Audit Log" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Camera Coverage Compliance % | Branches meeting all minimum camera coverage standards / total branches | Green ≥ 90% · Yellow 70–89% · Red < 70% | → Section 5.1 |
| Cameras Non-Functional | Total non-functional cameras across all branches | Green = 0 · Yellow 1–10 · Red > 10 | → Section 5.1 |
| Branches with Guard Shortfall | Branches with live guard count below required deployment floor | Green = 0 · Red if any | → Section 5.4 |
| Open Security Incidents | Active unresolved security incidents across all branches | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.2 |
| Visitor Management Active Branches | Branches with active visitor log usage (≥ 1 visitor entry in last 7 days) / total | Green = all · Amber if any missing | → Section 5.1 |
| CCTV Audit Compliance % | Branches that have completed the annual CCTV compliance audit / total | Green ≥ 90% · Yellow 70–89% · Red < 70% | → Section 5.1 |
| Security Guards On Duty Now | Live headcount where biometric / GPS check-in data is available | Blue always (informational) | → Section 5.4 |
| Cameras Due for Maintenance | Cameras approaching scheduled maintenance date within next 14 days | Green = 0 · Amber if any | → Section 5.1 |

**HTMX:** `hx-trigger="every 5m"` → Cameras Non-Functional, Open Security Incidents, and Guards On Duty Now auto-refresh.

---

## 5. Sections

### 5.1 Branch CCTV & Security Matrix

> Per-branch summary of all security dimensions — primary monitoring and audit table.

**Search:** Branch name, city, zone. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Coverage Compliance | Radio | All / Compliant / Non-Compliant / Partially Compliant |
| Non-Functional Cameras | Checkbox | Show branches with any non-functional cameras |
| Guard Status | Radio | All / Fully Deployed / Shortfall / Critically Short |
| Visitor Management | Checkbox | Show branches not using visitor log |
| Audit Status | Checkbox | Audited / Not Audited / Audit Overdue |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → `branch-security-detail` drawer |
| Total Cameras | ✅ | Count |
| Functional / Total | ✅ | e.g., "48 / 50" — Red if any non-functional |
| Coverage Compliance | ✅ | Compliant ✅ / Non-Compliant ❌ / Partial ⚠ |
| Gate Camera Status | ✅ | Functional ✅ / Non-Functional ❌ — Red if non-functional |
| Guards Required | ✅ | Calculated floor from campus profile |
| Guards On Duty | ✅ | Current live count; Red if < 50% of required |
| Visitor Log Active | ✅ | Active ✅ / Inactive ❌ |
| Last Audit Date | ✅ | Date or — if never audited; Red if > 12 months |
| Open Incidents | ✅ | Count; Red if > 0 |
| Actions | ❌ | View · Log Incident · Schedule Audit |

**Default sort:** Coverage Compliance (Non-Compliant first), then Guards On Duty ascending.
**Pagination:** Server-side · 25/page.

---

### 5.2 Security Incidents (Live + Recent)

> All active security incidents plus incidents from the past 30 days for situational awareness.

**Search:** Incident ID, branch, incident type. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Incident Type | Checkbox | Trespass / Theft / Vandalism / Physical Altercation / Suspicious Person / Cyber / Fire / Other |
| Status | Checkbox | Open / Under Investigation / Resolved / Referred to Police |
| Date Range | Date picker | From / To |
| Severity | Checkbox | Low / Medium / High / Critical |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Incident ID | ✅ | System-generated; link → `incident-report` drawer in view mode |
| Date & Time | ✅ | Reported date and time |
| Branch | ✅ | |
| Incident Type | ✅ | Badge |
| Severity | ✅ | Critical (Red) / High (Orange) / Medium (Yellow) / Low (Grey) |
| Reported By | ✅ | Security officer / Principal / Staff name |
| Status | ✅ | Colour-coded badge |
| Reported Within 24h | ✅ | ✅ Yes / ❌ No (SLA compliance) |
| Police Involved | ❌ | ✅ Yes / — No |
| Actions | ❌ | View · Update · Escalate |

**Default sort:** Date & Time descending (most recent first); Open incidents pinned to top.
**Pagination:** Server-side · 25/page.

**Auto-refresh:** `hx-trigger="every 2m"` — new incidents appear without full page reload.

---

### 5.3 Coverage Compliance Chart

> Visual representation of camera coverage compliance across all branches.

**Display:** Two charts side-by-side on desktop, stacked on mobile.

**Chart 1 — Bar Chart (branch-wise):**
- X-axis: Branch names
- Y-axis: Coverage compliance % (0–100)
- Colour: Green ≥ 90% · Yellow 70–89% · Red < 70%
- Click bar → `branch-security-detail` drawer at CCTV Cameras tab

**Chart 2 — Pie Chart (overall):**
- Segment 1: Fully Compliant branches (Green)
- Segment 2: Partially Compliant branches (Yellow)
- Segment 3: Non-Compliant branches (Red)
- Centre: "[N] / [Total] branches compliant"

Below charts: "Coverage standard definitions →" link to the coverage policy document.

---

### 5.4 Guard Deployment Summary

> Branch-wise guard deployment table comparing required vs actual guard counts.

**Columns:** Branch · Campus Area (sq m) · Student Count · Guards Required (calculated) · Guards Contracted · Guards On Duty Now · Shortfall (negative = below floor) · Last Biometric Check-in · Vendor Name

**Colour rule:** Shortfall — Red if any shortfall · Amber if contracted < required even if on-duty OK · Green if on-duty ≥ required.

**Default sort:** Shortfall ascending (largest shortfall first).

---

## 6. Drawers / Modals

### 6.1 Drawer: `branch-security-detail`
- **Trigger:** Branch name link in Section 5.1 table
- **Width:** 640px
- **Tabs:** CCTV Cameras · Guard Roster · Visitor Log · Incidents

**CCTV Cameras tab:**
- Total cameras: [N] | Functional: [N] | Non-Functional: [N] | Maintenance Due: [N]
- Camera list: Camera ID · Area Type (Gate / Corridor / Classroom / Hostel / Parking / Other) · Location Description · Status (Functional / Non-Functional / Under Repair) · Last Maintenance Date · Next Maintenance Due
- Non-functional cameras highlighted Red with days non-functional count

**Guard Roster tab:**
- Vendor name · Contract start/end dates · Contracted guard count · Required floor
- Guard list: Name · Shift (Morning / Evening / Night) · Check-in time (biometric if available) · Check-out · Status (Present / Absent / Late)

**Visitor Log tab:**
- Last 7 days summary: Total visitors · Today's visitor count
- Recent visitor log entries: Date · Visitor Name · Purpose · Host Staff · In Time · Out Time · Vehicle Number

**Incidents tab:**
- All incidents at this branch: Incident ID · Date · Type · Severity · Status
- Sorted by date descending

---

### 6.2 Drawer: `incident-report`
- **Trigger:** "Log Incident" action in Section 5.1 or "Update" action in Section 5.2; opens in edit mode for new / update, view mode for existing record
- **Width:** 600px
- **Mode:** Create / Edit / View

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Select | Required |
| Incident Date & Time | DateTime | Required; cannot be future |
| Incident Type | Select | Trespass / Theft / Vandalism / Physical Altercation / Suspicious Person / Cyber / Fire / Other |
| Severity | Radio | Low / Medium / High / Critical |
| Incident Description | Textarea | Required; min 50 chars |
| Location on Campus | Text | Area / block / camera zone |
| Persons Involved | Textarea | Names, roles, descriptions |
| Reported By | Text | Auto-filled from logged-in user; editable |
| Reported Within 24 Hours | Toggle | If No: reason required |
| Police Involved | Toggle | If Yes: FIR number field appears |
| FIR Number | Text | Conditional — required if Police Involved = Yes |
| Immediate Action Taken | Textarea | Required; describe immediate response |
| Status | Select | Open / Under Investigation / Resolved / Referred to Police |
| Resolution Notes | Textarea | Required when Status = Resolved |
| Attachments | File upload | Images, CCTV screenshots — max 5 files, 10MB each |

**Validation:** Branch, date/time, type, severity, description, and immediate action are required · FIR number required if police involved · Resolution notes required on status change to Resolved.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Incident logged | "Security incident [ID] logged at [Branch]." | Success | 4s |
| Incident updated | "Incident [ID] status updated to [Status]." | Success | 4s |
| Incident escalated | "Incident [ID] escalated to Group COO." | Warning | 6s |
| Audit scheduled | "Security audit scheduled at [Branch] on [date]." | Info | 4s |
| Security report exported | "Security report export prepared. Download ready." | Info | 4s |
| Maintenance alert sent | "Maintenance alert sent to vendor for [N] non-functional cameras at [Branch]." | Info | 4s |
| Guard deployment flag raised | "Guard deployment shortfall flag raised for [Branch]. Vendor notified." | Warning | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open incidents | "No Open Security Incidents" | "All security incidents across all branches are resolved. Group is secure." | — |
| No non-functional cameras | "All Cameras Operational" | "All cameras across all branches are functional." | — |
| No guard shortfalls | "Guard Deployment Meeting Requirements" | "All branches have the required number of security guards on duty." | — |
| Search returns no results | "No Results Found" | "No branches or incidents match your search or filters." | [Clear Filters] |
| No incidents in past 30 days | "No Security Incidents This Month" | "No security incidents have been reported in the past 30 days." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + branch security matrix (15 rows × 10 columns) + incidents table + charts + alerts |
| Table filter/search | Inline skeleton rows (8 rows) |
| KPI auto-refresh | Shimmer on individual card values; labels preserved |
| Incidents auto-refresh | Shimmer overlay on incidents table body only |
| Coverage chart load | Chart area skeleton with animated gradient |
| Branch detail drawer open | 640px drawer skeleton; tabs load lazily on first click |
| Incident report drawer open | 600px drawer form skeleton |

---

## 10. Role-Based UI Visibility

| Element | CCTV & Security Head G3 | Group COO G4 | Chairman / CEO G5 | Branch Security Officer G2 |
|---|---|---|---|---|
| View All Branches | ✅ | ✅ | ✅ | Own branch only |
| Log Security Incident | ✅ | ❌ | ❌ | ✅ (own branch) |
| Update Incident Status | ✅ | ❌ | ❌ | ✅ (own branch) |
| Escalate Incident | ✅ | ❌ | ❌ | ❌ |
| Schedule CCTV Audit | ✅ | ❌ | ❌ | ❌ |
| Edit Camera Records | ✅ | ❌ | ❌ | ✅ (own branch) |
| View Visitor Log | ✅ | ✅ | ❌ | ✅ (own branch) |
| Guard Deployment Edit | ✅ | ❌ | ❌ | ❌ |
| Export Security Report | ✅ | ✅ | ✅ | ❌ |
| Coverage Standard Edit | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/security/dashboard/` | JWT (G3+) | Full dashboard data payload |
| GET | `/api/v1/group/{group_id}/welfare/security/kpi-cards/` | JWT (G3+) | KPI auto-refresh values |
| GET | `/api/v1/group/{group_id}/welfare/security/branch-matrix/` | JWT (G3+) | Branch security matrix; params: `coverage`, `guard_status`, `visitor_active`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/security/incidents/` | JWT (G3+) | Incidents list; params: `branch_id`, `type`, `status`, `severity`, `from_date`, `to_date`, `page` |
| POST | `/api/v1/group/{group_id}/welfare/security/incidents/` | JWT (G3) | Log new security incident |
| GET | `/api/v1/group/{group_id}/welfare/security/incidents/{incident_id}/` | JWT (G3+) | Single incident detail |
| PATCH | `/api/v1/group/{group_id}/welfare/security/incidents/{incident_id}/` | JWT (G3) | Update incident status or details |
| POST | `/api/v1/group/{group_id}/welfare/security/incidents/{incident_id}/escalate/` | JWT (G3) | Escalate incident to COO |
| GET | `/api/v1/group/{group_id}/welfare/security/guard-deployment/` | JWT (G3+) | Guard deployment summary all branches |
| GET | `/api/v1/group/{group_id}/welfare/branches/{branch_id}/security-detail/` | JWT (G3+) | Branch security detail drawer payload |
| GET | `/api/v1/group/{group_id}/welfare/security/coverage-chart/` | JWT (G3+) | Coverage compliance chart data |
| POST | `/api/v1/group/{group_id}/welfare/security/audits/` | JWT (G3) | Schedule CCTV audit; body: `branch_id`, `scheduled_date` |
| GET | `/api/v1/group/{group_id}/welfare/security/export/` | JWT (G3+) | Async security report export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../security/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Incidents auto-refresh | `every 2m` | GET `.../security/incidents/?status=open` | `#incidents-table-body` | `innerHTML` |
| Branch matrix search | `input delay:300ms` | GET `.../security/branch-matrix/?q={val}` | `#branch-matrix-body` | `innerHTML` |
| Branch matrix filter | `click` | GET `.../security/branch-matrix/?{filters}` | `#branch-matrix-section` | `innerHTML` |
| Branch matrix pagination | `click` | GET `.../security/branch-matrix/?page={n}` | `#branch-matrix-section` | `innerHTML` |
| Incidents filter | `click` | GET `.../security/incidents/?{filters}` | `#incidents-section` | `innerHTML` |
| Open branch drawer | `click` on branch name | GET `.../welfare/branches/{id}/security-detail/` | `#drawer-body` | `innerHTML` |
| Open incident drawer (view) | `click` on incident ID | GET `.../security/incidents/{id}/` | `#drawer-body` | `innerHTML` |
| Open incident drawer (new) | `click` Log Incident | GET `.../security/incidents/create-form/` | `#drawer-body` | `innerHTML` |
| Submit new incident | `click` Save | POST `.../security/incidents/` | `#incidents-section` | `innerHTML` |
| Update incident | `click` Save | PATCH `.../security/incidents/{id}/` | `#incident-row-{id}` | `outerHTML` |
| Coverage chart load | `load` | GET `.../security/coverage-chart/` | `#coverage-chart-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
