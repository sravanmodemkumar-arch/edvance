# P-07 — Branch Inspection Scheduler

> **URL:** `/group/audit/inspections/scheduler/`
> **File:** `p-07-branch-inspection-scheduler.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Inspection Officer (Role 123, G3) — primary operator

---

## 1. Purpose

The Branch Inspection Scheduler plans and tracks physical visits to branches by the audit team. In Indian education groups, the gap between what a branch reports digitally and what actually exists on the ground is often enormous — a branch claims 100% CCTV coverage but 3 cameras are non-functional; a branch shows 95% attendance but the physical headcount reveals 15% ghost entries; a branch claims a fully equipped science lab but half the apparatus is broken. Physical inspection is the only way to verify ground truth.

The problems this page solves:

1. **No systematic visit rotation:** Without a scheduler, some branches go uninspected for 2+ years while the inspector visits convenient nearby branches repeatedly. The scheduler enforces rotation — every branch must be visited at least once per quarter for large groups, once per semester for small groups. Branches with open critical findings get priority scheduling.

2. **Surprise vs scheduled visit management:** CBSE and RTE norms recommend surprise inspections. But surprise inspections require secrecy — if the branch knows the date, they'll clean up temporarily. The scheduler manages two visit types: scheduled (branch notified 7 days prior — for document review) and surprise (only Audit Head and assigned inspector know — for ground reality check). The ratio should be 40:60 (surprise:scheduled).

3. **Inspector travel optimization:** In a group with 30 branches across Telangana, inspecting all branches requires travel planning. Branches in the same district should be clubbed into a single trip. The scheduler shows geographic clustering and suggests multi-branch visit routes to minimize travel time and cost.

4. **Visit outcome tracking:** An inspection visit without documented outcomes is wasted. The scheduler enforces: every visit must produce a report (P-09) with findings, photos, and scores within 48 hours of the visit. Visits without reports are flagged as incomplete.

5. **Regulatory inspection preparation:** When CBSE sends an inspection committee or the state education department sends a flying squad, branches need preparation time. The scheduler tracks external regulatory inspections separately — date, committee members, requirements — so branches can prepare documentation in advance.

**Scale:** 5–50 branches · 3–5 inspectors · 60–200 visits/year · 40% surprise ratio · 48-hour report deadline

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Inspection Officer | 123 | G3 | Full — schedule visits, record outcomes, manage calendar | Primary scheduler |
| Group Internal Audit Head | 121 | G1 | Full — approve surprise visits, override schedule | Oversight |
| Group Academic Quality Officer | 122 | G1 | Read + request academic inspection | Requests visits |
| Group Affiliation Compliance Officer | 125 | G1 | Read + request affiliation inspection | Pre-renewal visits |
| Group Compliance Data Analyst | 127 | G1 | Read — inspection data for analytics | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read — upcoming visits for CAPA verification | Plans follow-ups |
| Group CEO / Chairman | — | G4/G5 | Read — inspection schedule overview | Governance |
| Branch Principal | — | G3 | Read (own branch) — scheduled visits only (not surprise) | Preparation |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Branch Principals see ONLY scheduled visits for their branch — surprise visits are hidden until 24 hours before.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Inspections  ›  Scheduler
```

### 3.2 Page Header
```
Branch Inspection Scheduler                    [+ Schedule Visit]  [+ Surprise Visit]  [Route Planner]  [Export]
Inspection Team Lead — M. Venkatesh
Sunrise Education Group · FY 2025-26 · 28 branches · 148 visits planned · 102 completed · Coverage: 89%
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Visits This Month | Integer / Planned | Completed / planned for current month | Green if 100%, Amber ≥ 60%, Red < 60% | `#kpi-month` |
| 2 | Branch Coverage (90d) | Percentage | Branches visited in last 90 days / total × 100 | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-coverage` |
| 3 | Surprise Visit Ratio | Percentage | Surprise visits / total visits this FY × 100 | Green 30–50%, Amber 20–29% or 51–60%, Red < 20% or > 60% | `#kpi-surprise` |
| 4 | Overdue Branches | Integer | Branches not visited in 90+ days | Red > 5, Amber 1–5, Green = 0 | `#kpi-overdue` |
| 5 | Pending Reports | Integer | Visits completed > 48h ago without submitted report | Red > 3, Amber 1–3, Green = 0 | `#kpi-pending` |
| 6 | Avg Inspection Score | Percentage | AVG(inspection_score) across completed visits this FY | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-score` |

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Calendar** — Visual month/week calendar of visits
2. **Visit List** — All visits in table format
3. **Branch Coverage** — Coverage status per branch
4. **External Inspections** — Regulatory/board inspections tracking

### 5.2 Tab 1: Calendar

**FullCalendar.js integration:**
- Scheduled visits: Solid colour blocks (blue)
- Surprise visits: Red blocks (visible only to 121, 123 — hidden from Branch Principals)
- Completed visits: Green
- Cancelled: Grey with strikethrough
- External regulatory: Purple
- Filter: Inspector · Branch · Visit type · Status
- Click event → drawer with visit details

### 5.3 Tab 2: Visit List

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Visit ID | Text (link) | Yes | Auto: INS-2026-001 |
| Branch | Text | Yes | — |
| Visit Type | Badge | Yes | Scheduled / Surprise / Follow-up / Pre-Affiliation / External |
| Date | Date | Yes | — |
| Inspector(s) | Text | No | — |
| Focus | Badges | No | Academic / Financial / Safety / Infrastructure / Comprehensive |
| Status | Badge | Yes | Planned / In Transit / On-Site / Completed / Report Pending / Closed |
| Report Submitted? | Badge | Yes | ✅ Yes / 🔴 No (with hours overdue) |
| Findings | Integer | Yes | — |
| Score | Percentage | Yes | — |
| Actions | Buttons | No | [View] [Check-In] [Submit Report] |

### 5.4 Tab 3: Branch Coverage

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| District / City | Text | Yes | For geographic grouping |
| Last Visit | Date | Yes | — |
| Days Since | Integer | Yes | Red > 90, Amber 60–90, Green < 60 |
| Visits This FY | Integer | Yes | Total |
| Scheduled Visits | Integer | Yes | Planned for this FY |
| Surprise Visits | Integer | Yes | Count this FY |
| Open Findings | Integer | Yes | Unresolved from previous visits |
| Risk Priority | Badge | Yes | High / Medium / Low (from P-02 risk matrix) |
| Next Scheduled | Date | Yes | — |
| Coverage Status | Badge | Yes | ✅ Adequate / ⚠️ Due / 🔴 Overdue |

### 5.5 Tab 4: External Inspections

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Authority | Text | Yes | CBSE / State Board / DEO / Municipal / Fire Dept / UGC |
| Branch | Text | Yes | — |
| Inspection Type | Badge | Yes | Affiliation / Routine / Complaint-based / Flying Squad |
| Scheduled Date | Date | Yes | — |
| Committee Members | Text | No | If known |
| Requirements | Text (link) | No | Documents/preparations needed |
| Preparation Status | Badge | Yes | Not Started / In Progress / Ready |
| Outcome | Badge | Yes | Pending / Satisfactory / Conditional / Unsatisfactory |
| Actions | Buttons | No | [View] [Update] [Prepare Checklist] |

---

## 6. Drawers & Modals

### 6.1 Modal: `schedule-visit` (560px)

- **Title:** "Schedule Branch Visit"
- **Fields:**
  - Branch (dropdown, required)
  - Visit type (radio): Scheduled / Surprise / Follow-up / Pre-Affiliation
  - Date(s) (date picker — single or multi-day)
  - Inspector(s) (multi-select, required)
  - Focus areas (checkboxes): Academic / Financial / Safety / Infrastructure / Comprehensive
  - Specific checklist (dropdown from P-08 — auto-suggested based on focus)
  - Purpose / notes (textarea)
  - Linked to previous finding? (toggle + finding ID)
  - If Surprise: Confirmation toggle — "I confirm this visit should NOT be visible to branch staff"
  - If Scheduled: Branch notification date (default: 7 days before)
- **Buttons:** Cancel · Schedule
- **Validation:** Inspector available on date; branch coverage rules met
- **Access:** Role 123, 121

### 6.2 Drawer: `visit-detail` (720px, right-slide)

- **Title:** "Inspection — [Branch] · [Date] · [Type Badge]"
- **Tabs:** Overview · Checklist · Photos · Findings · Report · Previous Visits
- **Overview tab:** Visit type, branch, date, inspectors, focus, status, duration
- **Checklist tab:** Active checklist with completion status (links to P-08/P-09)
- **Photos tab:** All photos taken during visit — geotagged, timestamped
- **Findings tab:** Findings generated from this visit
- **Report tab:** Inspection report with scores and recommendations
- **Previous Visits tab:** History of all visits to this branch — comparison
- **Footer:** [Check-In] [Check-Out] [Submit Report] [Add Finding]
- **Access:** G1+ (Division P roles)

### 6.3 Modal: `inspector-check-in` (400px)

- **Title:** "Check-In — [Branch]"
- **Auto-captured:** Current timestamp, GPS coordinates
- **Fields:**
  - Confirm branch (auto-detected from GPS or manual)
  - Arrival time (auto-filled, editable)
  - Branch contact met (text — principal or designated person)
  - Notes (textarea)
  - Selfie at entrance (camera capture — proof of physical presence)
- **Buttons:** Cancel · Check In
- **GPS validation:** Warning if GPS location > 500m from branch registered address
- **Access:** Role 123

### 6.4 Modal: `route-planner` (640px)

- **Title:** "Multi-Branch Visit Route Planner"
- **Fields:**
  - Start location (text or GPS)
  - Branches to visit (multi-select — suggested based on overdue branches in same district)
  - Date range (start–end)
  - Visit type per branch (Scheduled / Surprise)
- **Output:**
  - Optimized route on map (Leaflet.js)
  - Estimated travel time between branches
  - Suggested schedule: Day 1 → Branch A (AM), Branch B (PM); Day 2 → Branch C...
  - Total travel cost estimate (km × ₹8/km standard rate)
- **Buttons:** Close · Schedule All Visits
- **Access:** Role 123, 121

### 6.5 Modal: `external-inspection` (560px)

- **Title:** "Log External Inspection"
- **Fields:**
  - Authority (dropdown): CBSE / ICSE / State Board / DEO / Municipal / Fire Dept / UGC / NAAC / Other
  - Branch (dropdown)
  - Inspection type (dropdown): Affiliation / Routine / Complaint-based / Flying Squad / Accreditation
  - Scheduled date (date)
  - Committee members (text — if known)
  - Requirements / documents needed (textarea)
  - Preparation checklist (auto-generated based on authority type)
  - Internal notes (textarea — not visible to branch)
- **Buttons:** Cancel · Log Inspection
- **Access:** Role 121, 125, G4+

---

## 7. Charts

### 7.1 Branch Coverage Map (Leaflet.js)

| Property | Value |
|---|---|
| Chart type | Interactive map (Leaflet.js) |
| Title | "Branch Inspection Coverage" |
| Markers | Per branch: Green (visited < 30d), Amber (31–90d), Red (> 90d), Grey (never) |
| Click | Popup with branch name, last visit, score, next scheduled |
| API | `GET /api/v1/group/{id}/audit/inspections/coverage-map/` |

### 7.2 Visit Volume (Stacked Bar)

| Property | Value |
|---|---|
| Chart type | Stacked bar (Chart.js 4.x) |
| Title | "Monthly Visit Volume — By Type" |
| Data | Per month: Scheduled, Surprise, Follow-up, External counts |
| API | `GET /api/v1/group/{id}/audit/inspections/analytics/volume-trend/` |

### 7.3 Inspector Utilization (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Inspector Visits — FY to Date" |
| Data | Visit count per inspector |
| Target line | Expected visits based on equal distribution |
| API | `GET /api/v1/group/{id}/audit/inspections/analytics/inspector-utilization/` |

### 7.4 Coverage Gap (Heat Calendar)

| Property | Value |
|---|---|
| Chart type | Calendar heatmap (custom Canvas) |
| Title | "Visit Activity — Daily Heatmap" |
| Data | Visit count per day across the FY |
| Colour | White (0), Light green (1), Dark green (3+), Grey (holiday/weekend) |
| API | `GET /api/v1/group/{id}/audit/inspections/analytics/activity-heatmap/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Visit scheduled | "Visit scheduled — [Branch], [Date]" | Success | 3s |
| Surprise visit created | "Surprise visit scheduled — details hidden from branch" | Success | 3s |
| Check-in | "Checked in at [Branch] — [Time]" | Success | 3s |
| Check-out | "Checked out — visit duration: [Hours]h [Min]m" | Info | 3s |
| Report overdue | "⚠️ Report overdue for [Branch] visit on [Date] — [Hours]h past deadline" | Warning | 5s |
| Branch notified | "Branch [Name] notified of upcoming scheduled visit" | Info | 3s |
| External inspection logged | "External inspection logged — [Authority] at [Branch]" | Success | 3s |
| Route planned | "Route planned — [N] branches, [N] days, [Distance] km" | Success | 3s |
| GPS mismatch | "⚠️ GPS location does not match branch address" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No visits scheduled | 🔍 | "No Inspections Scheduled" | "Plan your first branch visit to begin on-ground verification." | Schedule Visit |
| No overdue branches | ✅ | "All Branches Covered" | "Every branch has been inspected within the last 90 days." | — |
| No external inspections | 🏛️ | "No External Inspections" | "Log external inspections when notified by CBSE/Board/DEO." | Log External |
| No inspectors assigned | 👤 | "No Inspectors Available" | "Assign inspection officers to begin field visits." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + calendar skeleton |
| Calendar render | Calendar grid skeleton |
| Visit list | Table skeleton with 10 rows |
| Branch coverage table | Table skeleton with branch rows |
| Visit detail drawer | 720px skeleton: 6 tabs |
| Map | Grey rectangle + "Loading map…" |
| Route planner | Map skeleton + form placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/inspections/` | G1+ | List all visits |
| GET | `/api/v1/group/{id}/audit/inspections/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/audit/inspections/calendar/` | G1+ | Calendar events |
| POST | `/api/v1/group/{id}/audit/inspections/` | 123, 121 | Schedule visit |
| PUT | `/api/v1/group/{id}/audit/inspections/{visit_id}/` | 123, 121 | Update visit |
| PATCH | `/api/v1/group/{id}/audit/inspections/{visit_id}/cancel/` | 121, G4+ | Cancel visit |
| GET | `/api/v1/group/{id}/audit/inspections/{visit_id}/` | G1+ | Visit detail |
| POST | `/api/v1/group/{id}/audit/inspections/{visit_id}/check-in/` | 123 | Check-in (GPS + timestamp) |
| POST | `/api/v1/group/{id}/audit/inspections/{visit_id}/check-out/` | 123 | Check-out |
| GET | `/api/v1/group/{id}/audit/inspections/coverage/` | G1+ | Branch coverage table |
| GET | `/api/v1/group/{id}/audit/inspections/coverage-map/` | G1+ | Map data |
| GET | `/api/v1/group/{id}/audit/inspections/external/` | G1+ | External inspections list |
| POST | `/api/v1/group/{id}/audit/inspections/external/` | 121, 125, G4+ | Log external inspection |
| PUT | `/api/v1/group/{id}/audit/inspections/external/{id}/` | 121, 125 | Update external inspection |
| POST | `/api/v1/group/{id}/audit/inspections/route-plan/` | 123, 121 | Generate route plan |
| GET | `/api/v1/group/{id}/audit/inspections/analytics/volume-trend/` | G1+ | Volume chart |
| GET | `/api/v1/group/{id}/audit/inspections/analytics/inspector-utilization/` | G1+ | Inspector utilization |
| GET | `/api/v1/group/{id}/audit/inspections/analytics/activity-heatmap/` | G1+ | Activity heatmap |
| GET | `/api/v1/group/{id}/audit/inspections/export/` | G1+ | Export data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../inspections/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Calendar render | Tab 1 shown | Non-HTMX (FullCalendar.js) | — | — | JS init, API fetch |
| Tab switch | Tab click | `hx-get` with tab param | `#inspection-content` | `innerHTML` | `hx-trigger="click"` |
| Schedule visit | Form submit | `hx-post=".../inspections/"` | `#schedule-result` | `innerHTML` | Toast + calendar refresh |
| Visit detail drawer | Row/event click | `hx-get=".../inspections/{id}/"` | `#right-drawer` | `innerHTML` | 720px drawer |
| Check-in | Form submit | `hx-post=".../inspections/{id}/check-in/"` | `#checkin-result` | `innerHTML` | Toast + GPS capture |
| Check-out | Button click | `hx-post=".../inspections/{id}/check-out/"` | `#checkout-result` | `innerHTML` | Toast |
| External inspection log | Form submit | `hx-post=".../inspections/external/"` | `#external-result` | `innerHTML` | Toast |
| Route planner | Form submit | `hx-post=".../inspections/route-plan/"` | `#route-output` | `innerHTML` | Map + schedule render |
| Filter | Filter change | `hx-get` with filters | `#visit-table` | `innerHTML` | `hx-trigger="change"` |
| Map load | Tab 3 shown | Non-HTMX (Leaflet.js) | — | — | JS map init |
| Pagination | Page click | `hx-get` with page param | `#table-body` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
