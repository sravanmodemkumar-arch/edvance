# 52 — CPD Tracker

> **URL:** `/group/acad/cpd/`
> **File:** `52-cpd-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Director G3 · CAO G4 · Stream Coordinators G3 · Training & Development Manager/Div-E · Academic MIS Officer G1

---

## 1. Purpose

The CPD (Continuous Professional Development) Tracker monitors whether every teacher across all branches is meeting their mandatory annual training hours requirement. In Indian education, CBSE and NCTE (National Council for Teacher Education) mandate ongoing professional development for school teachers — typically a minimum of 50 hours per academic year for in-service teachers, with specific categories of training required. Without systematic tracking at the group level, branches either self-report inconsistently or compliance is verified only during inspection visits.

This page tracks CPD completions at the individual teacher level: each training session is logged with the provider, the number of hours, the type of training (online course, offline workshop, certification programme, or in-service day), and a certificate upload where applicable. Teachers who are "At Risk" (completed < 50% of required hours by the midpoint of the year) are flagged automatically, and the Academic Director can send bulk reminders prompting branch counsellors to encourage their teachers to complete training.

The CPD completion rate feeds directly into the composite performance score computed by the Teacher Performance Tracker (page 50) — specifically into the overall professional development dimension. A teacher who consistently completes CPD above the required threshold receives a higher professional development rating. This creates a positive incentive loop where CPD is not merely a compliance burden but is actively visible in performance records.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ❌ No create | Supervisory view |
| Group Academic Director | G3 | ✅ Full | ✅ Full CRUD + reminders | Primary owner |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coord — MPC | G3 | ✅ MPC teachers | ❌ | View own stream |
| Stream Coord — BiPC | G3 | ✅ BiPC teachers | ❌ | View own stream |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC teachers | ❌ | View own stream |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Read-only | ❌ | Branch-level summaries only |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |
| Training & Development Mgr (Div-E) | Cross-div | ✅ Full | ✅ Full CRUD | Co-manages CPD records with Academic Dir |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Teacher Performance & CPD  ›  CPD Tracker
```

### 3.2 Page Header
```
CPD Tracker                                         [+ Add CPD Record]  [Export ↓]  [Send Reminders]
Continuous Professional Development — all branches            (Academic Dir / Div-E T&D Mgr)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Teachers Tracked | Count |
| On Track (≥ 50% hours) | Count — green |
| At Risk (25–49% hours) | Count — amber |
| Overdue (< 25% hours by mid-year) | Count — red |
| Average CPD Hours Completed (Group) | Hours |
| Required Hours per Teacher | Configurable (default 50 hrs/year) |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Teacher name, Teacher ID, Branch name
- 300ms debounce · Highlights match in Teacher Name column

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Subject | Multi-select | |
| Status | Multi-select | On Track / At Risk / Overdue |
| Academic Year | Select | Current + last 3 years |
| Training type completed | Multi-select | Online / Offline / Workshop / Certification |

Active filter chips dismissible. "Clear All". Filter badge count.

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Bulk select |
| Teacher ID | Text | ✅ | |
| Teacher Name | Text | ✅ | Hidden for MIS (shows anonymised count) |
| Branch | Text | ✅ | |
| Subject | Text | ✅ | |
| CPD Hours Completed | Number | ✅ | |
| CPD Hours Required | Number | ✅ | Group-configured requirement |
| % Complete | Progress bar + % | ✅ | |
| Last Training Date | Date | ✅ | |
| Status | Badge | ✅ | On Track (green) · At Risk (amber) · Overdue (red) |
| Actions | — | ❌ | Role-based |

**Default sort:** Status (Overdue first, then At Risk, then On Track), then % Complete ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · Page jump input.

### 4.4 Row Actions

| Action | Visible To | Drawer | Notes |
|---|---|---|---|
| View CPD History | All roles | `teacher-cpd-history` drawer 480px | Chronological CPD record |
| Add CPD Record | Academic Dir, Div-E T&D | `cpd-record-add` drawer 480px | New training record for this teacher |
| Send Reminder | Academic Dir | Inline action | Email to teacher's branch contact |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Send Reminder to At Risk | Academic Dir | Bulk email/WhatsApp to branches with At Risk teachers |
| Export Selected (XLSX) | Academic Dir, Div-E T&D, CAO | CPD data for selected teachers |

---

## 5. Drawers & Modals

### 5.1 Drawer: `cpd-record-add` — Add CPD Record
- **Trigger:** [+ Add CPD Record] header button or row "Add CPD Record" action
- **Width:** 480px

| Field | Type | Required | Validation |
|---|---|---|---|
| Teacher | Search + select | ✅ | From branch rosters |
| Training name | Text | ✅ | Min 5, max 200 chars |
| Provider / Organisation | Text | ✅ | Institution or platform name |
| Training type | Select | ✅ | Online / Offline / Workshop / Certification / In-service day |
| Date(s) of training | Date range | ✅ | Cannot be future |
| Hours | Number | ✅ | Min 0.5; max 200 for a single record |
| Certificate | File upload | Conditional | Required for Certification type; PDF/image, max 5 MB |
| Notes | Textarea | ❌ | Max 300 chars |

- **Submit:** "Save CPD Record"
- **On success:** Record added to teacher's CPD history · Hours total updated · Status recomputed · Toast

### 5.2 Drawer: `teacher-cpd-history`
- **Trigger:** View CPD History row action
- **Width:** 480px
- **Header:** `[Teacher Name] — CPD History — [Academic Year]`

**Summary strip:** Hours completed: X · Required: X · % Complete: X% · Status: [badge]

**History table:**
| Column | Notes |
|---|---|
| Date | |
| Training Name | |
| Provider | |
| Type | Badge |
| Hours | |
| Certificate | PDF icon if uploaded |
| Added By | |

- **Tabs:** Current Year · All Years
- **Footer:** [Download CPD Record PDF] — formatted certificate summary

### 5.3 Modal: `send-bulk-reminder`
- **Trigger:** [Send Reminders] header button or bulk action
- **Width:** 420px
- **Content:** "Send CPD completion reminder to branches with [N] At Risk / Overdue teachers?"
- **Fields:** Message preview (editable, max 400 chars) · Channel (Email / WhatsApp / Both)
- **Buttons:** [Send Reminder] · [Cancel]
- **On confirm:** Notifications queued · Toast

---

## 6. Charts

### 6.1 CPD Completion Rate by Branch (Bar)
- **Type:** Vertical bar chart
- **Data:** Average % CPD completion per branch
- **Colour:** Green ≥ 75% · Amber 50–74% · Red < 50%
- **Tooltip:** Branch · Avg completion: X%
- **Export:** PNG

### 6.2 CPD Hours by Training Type (Donut)
- **Type:** Donut chart
- **Data:** Total hours split by type — Online / Offline / Workshop / Certification / In-service
- **Centre text:** Total hours (group)
- **Tooltip:** Type · Hours · %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| CPD record added | "CPD record added for [Teacher Name]. Hours updated." | Success | 4s |
| CPD record updated | "CPD record updated" | Success | 4s |
| CPD record deleted | "CPD record removed" | Warning | 6s |
| Reminder sent | "CPD reminder sent to [N] branches" | Success | 4s |
| Export started | "Export preparing… download will start shortly" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No CPD records | "No CPD records yet" | "Add training records for teachers to track completion" | [+ Add CPD Record] |
| No At Risk teachers | "All teachers on track" | "No teachers are currently at risk of missing CPD targets" | — |
| No records match filters | "No records match" | "Clear filters to see all CPD records" | [Clear Filters] |
| History drawer — no history | "No CPD history" | "No training records have been added for this teacher yet" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) + chart areas |
| Table filter/search/sort/page | Inline skeleton rows |
| Add record drawer open | Spinner → form |
| History drawer open | Spinner → table |
| Charts load | Skeleton chart areas |
| Export trigger | Spinner in button |

---

## 10. Role-Based UI Visibility

| Element | Academic Dir G3 | CAO G4 | Stream Coord G3 | Div-E T&D G3 | MIS G1 |
|---|---|---|---|---|---|
| Full teacher table | ✅ | ✅ | ✅ (own stream) | ✅ | ❌ (stats bar) |
| Teacher names | ✅ | ✅ | ✅ | ✅ | ❌ |
| [+ Add CPD Record] | ✅ | ❌ | ❌ | ✅ | ❌ |
| Add CPD row action | ✅ | ❌ | ❌ | ✅ | ❌ |
| Send Reminder | ✅ | ❌ | ❌ | ❌ | ❌ |
| Bulk actions | ✅ | ❌ | ❌ | ✅ | ❌ |
| Export | ✅ | ✅ | ❌ | ✅ | ❌ |
| Charts | ✅ | ✅ | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/cpd/` | JWT | List CPD records (teacher-level) |
| GET | `/api/v1/group/{group_id}/acad/cpd/stats/` | JWT | Stats bar |
| GET | `/api/v1/group/{group_id}/acad/cpd/{teacher_id}/history/` | JWT (G3+) | Teacher CPD history |
| POST | `/api/v1/group/{group_id}/acad/cpd/records/` | JWT (G3 Acad Dir, Div-E) | Add CPD record |
| PUT | `/api/v1/group/{group_id}/acad/cpd/records/{id}/` | JWT (G3 Acad Dir, Div-E) | Update record |
| DELETE | `/api/v1/group/{group_id}/acad/cpd/records/{id}/` | JWT (G3 Acad Dir, Div-E) | Delete record |
| POST | `/api/v1/group/{group_id}/acad/cpd/bulk-remind/` | JWT (G3 Acad Dir) | Send reminders |
| GET | `/api/v1/group/{group_id}/acad/cpd/export/?format=xlsx` | JWT (G3/G4) | Export |
| GET | `/api/v1/group/{group_id}/acad/cpd/charts/completion-by-branch/` | JWT | Bar chart |
| GET | `/api/v1/group/{group_id}/acad/cpd/charts/hours-by-type/` | JWT | Donut chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../cpd/?q=` | `#cpd-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../cpd/?filters=` | `#cpd-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../cpd/?sort=&dir=` | `#cpd-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../cpd/?page=` | `#cpd-table-section` | `innerHTML` |
| Add record drawer | `click` | GET `.../cpd/records/create-form/` | `#drawer-body` | `innerHTML` |
| Add record submit | `submit` | POST `.../cpd/records/` | `#drawer-body` | `innerHTML` |
| History drawer | `click` | GET `.../cpd/{tid}/history/` | `#drawer-body` | `innerHTML` |
| Send reminder inline | `click` | POST `.../cpd/bulk-remind/?teacher={tid}` | `#toast-container` | `beforeend` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
