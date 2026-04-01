# 03 — Grievance Redressal Dashboard

> **URL:** `/group/welfare/grievance/`
> **File:** `03-grievance-redressal-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Grievance Redressal Officer (Role 92, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Grievance Redressal Officer. Command centre for all student and parent grievances escalated from branches across all group campuses — managing the complete grievance lifecycle from escalation receipt to final resolution, tracking SLA compliance, monitoring category-wise volume patterns, and ensuring no complaint goes unaddressed at the group level.

The Group Grievance Redressal Officer receives grievances that branch-level officers could not resolve within their own SLA window. Upon escalation, the Group Officer takes ownership: acknowledging within 7 days, coordinating with relevant department heads (academic, hostel, transport, finance, HR) to drive resolution within 30 days, and — in extreme cases — escalating to the COO or CEO. Repeat grievances from the same student or parent on the same issue are treated as a systemic signal requiring root-cause investigation, not just case-by-case resolution. The dashboard surfaces all live escalations, SLA health, and trend patterns in one screen.

Scale: 20–50 branches · 100–500 escalated grievances/year · 7-day acknowledgment SLA · 30-day resolution SLA.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Grievance Redressal Officer | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group COO | G4 | View — open grievances and escalations section | Read-only |
| Group Chairman / CEO | G5 / G4 | View — escalated-to-CEO cases only | Not this URL |
| Branch Grievance Officer | G2 | View — own branch escalated grievances only | Branch-scoped, not this URL |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('grievance_redressal_officer')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Grievance Redressal Dashboard
```

### 3.2 Page Header
```
Welcome back, [Officer Name]                   [Export Grievance Report ↓]  [Settings ⚙]
[Group Name] — Group Grievance Redressal Officer · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  [N] Open Grievances  ·  SLA Breach Rate: [N]%
```

### 3.3 Alert Banner (conditional — critical items requiring same-day action)

| Condition | Banner Text | Severity |
|---|---|---|
| Acknowledgment overdue > 7 days | "Grievance [ID] from [Branch] has not been acknowledged in [N] days. 7-day SLA breached." | Red |
| Resolution overdue > 30 days | "Grievance [ID] has exceeded the 30-day resolution SLA. [N] days elapsed. Escalate immediately." | Red |
| Grievance escalated to CEO unresolved > 7 days | "CEO-escalated grievance [ID] has been open for [N] days without resolution. Immediate action required." | Red |
| Repeat grievance from same student | "Repeat grievance received from [Student Name] at [Branch] — same issue as [previous grievance ID]. Root-cause review required." | Amber |
| Grievance escalated to COO | "Grievance [ID] has been escalated to the Group COO. Ensure COO is briefed." | Amber |

Max 5 alerts visible. Alert links route to the relevant grievance record or section. "View all grievance events → Grievance Audit Log" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Grievances | Total active grievances at group level across all branches | Green = 0 · Yellow 1–10 · Red > 10 | → Section 5.1 |
| SLA Breach Rate % | % of grievances with either acknowledgment or resolution SLA breached, this AY | Green < 5% · Yellow 5–15% · Red > 15% | → Section 5.1 |
| Avg Resolution Time | Average days from escalation receipt to closure for cases resolved this AY | Green < 15 days · Yellow 15–25 days · Red > 25 days | → Section 5.3 |
| Escalated to CEO/COO This Month | Grievances escalated beyond Group Officer level this calendar month | Green = 0 · Amber if any | → Section 5.1 |
| Grievances Resolved This Month | Total grievances closed this calendar month | Blue always (informational) | → Section 5.1 |
| Repeat Grievances | Grievances filed by the same student/parent on the same issue | Green = 0 · Amber if any | → Section 5.1 |
| Category with Highest Volume | Category label with count — shows which issue type is most common this AY | Informational (Blue label) | → Section 5.2 |
| Branches with Most Open Grievances | Branch name and count of its open escalated grievances | Informational; Red if branch count > 5 | → Section 5.1 |

**HTMX:** `hx-trigger="every 5m"` → Open Grievances and SLA Breach Rate auto-refresh.

---

## 5. Sections

### 5.1 Open Grievances Table

> All active escalated grievances at group level — primary working table for the Group Grievance Redressal Officer.

**Search:** Grievance ID, student/parent name, branch, category. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Category | Checkbox | Academic / Hostel / Transport / Fees / Staff Conduct / Infrastructure / Safety / Other |
| Status | Checkbox | Open / Acknowledged / In Progress / Escalated to COO / Escalated to CEO / Awaiting Resolution |
| SLA Status | Radio | All / Acknowledgment Overdue / Resolution Overdue / Both / On Track |
| Days Open | Radio | All / < 7 days / 7–15 days / 15–30 days / > 30 days |
| Repeat | Checkbox | Show repeat grievances only |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Grievance ID | ✅ | System-generated; link → `grievance-detail` drawer |
| Branch | ✅ | |
| Category | ✅ | Colour-coded badge |
| Raised By | ✅ | Student / Parent name (masked to initials for non-relevant viewers) |
| Escalated Date | ✅ | Date received at group level |
| Days Open | ✅ | Red > 30 · Orange 15–30 · Yellow 7–15 · Green < 7 |
| Assigned To | ✅ | Group Officer, department head, or "Unassigned" (Red) |
| SLA Badge | ✅ | On Track ✅ / Ack Overdue ⚠ / Res Overdue ❌ / Both Overdue ❌❌ |
| Status | ✅ | Colour-coded stage badge |
| Repeat | ❌ | 🔁 badge if this student/parent has filed same issue before |
| Actions | ❌ | View · Assign · Resolve · Escalate |

**Default sort:** Days Open descending (longest open first), then SLA Breach status.
**Pagination:** Server-side · 25/page.

---

### 5.2 Grievance Volume by Category

> Bar chart showing number of escalated grievances per category, current AY, all branches combined.

**Chart type:** Horizontal bar chart (categories on Y-axis, count on X-axis).

**Categories and colours:**
| Category | Colour |
|---|---|
| Academic | Blue |
| Hostel | Purple |
| Transport | Orange |
| Fees | Green |
| Staff Conduct | Red |
| Infrastructure | Yellow |
| Safety | Dark Red |
| Other | Grey |

- Tooltip: Category · Count this AY · Count last AY · % change
- Click bar → filters Section 5.1 table to that category
- Below chart: text stat "Top category this month: [Category] — [N] grievances"

---

### 5.3 SLA Performance Trend

> Line chart showing monthly average resolution time in days for the past 12 months.

**Chart type:** Line chart with dual series.

- Series 1: Avg days to acknowledgment (target: 7 days — shown as dotted red line)
- Series 2: Avg days to resolution (target: 30 days — shown as dotted orange line)
- X-axis: Last 12 months (abbreviated month-year labels)
- Y-axis: Days (0–60)
- Tooltip: Month · Avg ack days · Avg resolution days · Grievances closed that month
- Hover month label → inline mini-table of grievances closed that month

---

### 5.4 Quick Actions

| Action | Target |
|---|---|
| New Grievance Entry | Opens new grievance registration drawer |
| Assign / Reassign | Opens `assign-grievance` modal with officer / department selector |
| Export Grievance Report | Download CSV/XLSX — open and closed, date range selector |
| Escalate to COO | Opens escalation confirmation modal for selected grievance |
| View Closed Grievances | Navigates to full closed grievance history view |

---

## 6. Drawers / Modals

### 6.1 Drawer: `grievance-detail`
- **Trigger:** Grievance ID link in Section 5.1 table
- **Width:** 680px
- **Tabs:** Detail · Timeline · Resolution · History

**Detail tab:**
| Field | Notes |
|---|---|
| Grievance ID | System-generated |
| Branch | Branch where original grievance was filed |
| Category | |
| Raised By | Name, type (Student / Parent), contact |
| Original Complaint Date | Date filed at branch level |
| Escalated to Group Date | Date received by Group Officer |
| Days Open (Group Level) | |
| SLA Status | Acknowledgment SLA · Resolution SLA — each with status badge |
| Assigned To | Current assignee at group level |
| Current Status | |
| Repeat Flag | Yes / No — with link to previous grievance if yes |
| Priority | Normal / High / Critical (set by Officer) |
| Grievance Description | Full text of complaint |
| Supporting Documents | File links — view/download only |

**Timeline tab:**
- Chronological log: Date · Event type (Filed / Escalated / Acknowledged / Assigned / Note Added / Stage Changed / Resolved) · Actor · Note text

**Resolution tab:**
- Resolution notes field (editable by Officer)
- Resolution category: Fully Resolved / Partially Resolved / Resolved with Compensation / Closed (Withdrawn) / Closed (Unresolvable)
- Department action taken summary
- Resolution date picker
- [Mark Resolved] button

**History tab:**
- Previous grievances from the same student/parent (if any): Grievance ID · Date · Category · Status · Resolution outcome

---

### 6.2 Modal: `assign-grievance`
- **Trigger:** "Assign / Reassign" quick action or Actions → Assign on table row
- **Width:** 480px
- **Mode:** Modal overlay (not drawer)

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Grievance ID | Display-only | Pre-filled |
| Assign To | Select | Choose from Group Officers, HODs (Academic / Hostel / Transport / Finance / HR) |
| Priority | Radio | Normal / High / Critical |
| Assignment Note | Textarea | Optional; max 500 chars |
| Internal Deadline | Date | Must be ≤ 30 days from escalation date |
| Notify Assignee | Toggle | Default: On — sends email + portal notification |

**Validation:** Assignee must be selected · Internal Deadline is required.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Grievance acknowledged | "Grievance [ID] acknowledged. [Raised By] will be notified." | Success | 4s |
| Grievance assigned | "Grievance [ID] assigned to [Name]." | Success | 4s |
| Grievance resolved | "Grievance [ID] marked resolved. Student/parent will be notified." | Success | 5s |
| Grievance escalated to COO | "Grievance [ID] escalated to Group COO." | Warning | 6s |
| Grievance escalated to CEO | "Grievance [ID] escalated to Group CEO. Chairman has been notified." | Warning | 6s |
| New grievance registered | "Grievance [ID] registered and assigned to [Name]." | Success | 4s |
| Report exported | "Grievance report export prepared. Download ready." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open grievances | "No Open Grievances" | "All escalated grievances are resolved. Excellent SLA compliance." | — |
| No grievances this month | "No Grievances This Month" | "No grievances have been escalated to group level this month." | — |
| No results from search/filter | "No Grievances Found" | "No grievances match your current search or filters." | [Clear Filters] |
| No SLA breaches | "All Grievances Within SLA" | "All open grievances are within their acknowledgment and resolution SLA windows." | — |
| No branches configured | "No Branches Found" | "No branches are configured in the welfare system." | [Add Branch] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + open grievances table (15 rows × 10 columns) + bar chart + line chart + alerts |
| Table filter/search | Inline skeleton rows (8 rows) |
| KPI auto-refresh | Shimmer on individual card values; labels preserved |
| Bar chart load | Chart area skeleton (grey rectangle with animated gradient) |
| Line chart load | Chart area skeleton |
| Grievance detail drawer open | 680px drawer skeleton; tabs load lazily on first click |
| Assign grievance modal open | 480px modal form skeleton |

---

## 10. Role-Based UI Visibility

| Element | Grievance Officer G3 | Group COO G4 | Chairman / CEO G5 | Branch Grievance Officer G2 |
|---|---|---|---|---|
| View All Branches | ✅ | ✅ | ✅ | Own branch only |
| Register New Grievance | ✅ | ❌ | ❌ | ❌ |
| Assign / Reassign Grievance | ✅ | ❌ | ❌ | ❌ |
| Escalate to COO | ✅ | ❌ | ❌ | ❌ |
| Escalate to CEO | ✅ | ✅ | ❌ | ❌ |
| Mark Resolved | ✅ | ❌ | ❌ | ❌ |
| View Grievance Details | ✅ | ✅ (summary) | Escalated-to-CEO only | Own branch only |
| View Raised-By Identity | ✅ | ✅ | ✅ | Own branch only |
| Export Grievance Report | ✅ | ✅ | ✅ | ❌ |
| Delete Grievance Record | ❌ (no deletion) | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/grievance/dashboard/` | JWT (G3+) | Full dashboard data payload |
| GET | `/api/v1/group/{group_id}/welfare/grievance/kpi-cards/` | JWT (G3+) | KPI auto-refresh values |
| GET | `/api/v1/group/{group_id}/welfare/grievance/open/` | JWT (G3+) | Open grievances list; params: `branch_id`, `category`, `status`, `sla_status`, `days_open_gt`, `repeat`, `page` |
| POST | `/api/v1/group/{group_id}/welfare/grievance/` | JWT (G3) | Register new grievance |
| GET | `/api/v1/group/{group_id}/welfare/grievance/{grievance_id}/` | JWT (G3+) | Single grievance detail with timeline |
| PATCH | `/api/v1/group/{group_id}/welfare/grievance/{grievance_id}/assign/` | JWT (G3) | Assign / reassign grievance; body: `assigned_to`, `priority`, `note`, `internal_deadline` |
| POST | `/api/v1/group/{group_id}/welfare/grievance/{grievance_id}/resolve/` | JWT (G3) | Mark resolved; body: `resolution_notes`, `resolution_category` |
| POST | `/api/v1/group/{group_id}/welfare/grievance/{grievance_id}/escalate/` | JWT (G3+) | Escalate to COO or CEO; body: `level` (coo/ceo) |
| GET | `/api/v1/group/{group_id}/welfare/grievance/category-volume/` | JWT (G3+) | Category-wise volume for bar chart |
| GET | `/api/v1/group/{group_id}/welfare/grievance/sla-trend/` | JWT (G3+) | Monthly SLA performance for past 12 months |
| GET | `/api/v1/group/{group_id}/welfare/grievance/export/` | JWT (G3+) | Async grievance report export; params: `from_date`, `to_date`, `format` |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../grievance/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Grievances table search | `input delay:300ms` | GET `.../grievance/open/?q={val}` | `#grievances-table-body` | `innerHTML` |
| Grievances filter | `click` | GET `.../grievance/open/?{filters}` | `#grievances-section` | `innerHTML` |
| Grievances pagination | `click` | GET `.../grievance/open/?page={n}` | `#grievances-section` | `innerHTML` |
| Open grievance drawer | `click` on grievance ID | GET `.../grievance/{id}/` | `#drawer-body` | `innerHTML` |
| Open assign modal | `click` Assign button | GET `.../grievance/{id}/assign-form/` | `#modal-body` | `innerHTML` |
| Submit assignment | `click` Save | PATCH `.../grievance/{id}/assign/` | `#grievance-row-{id}` | `outerHTML` |
| Mark resolved | `click` Resolve | POST `.../grievance/{id}/resolve/` | `#grievance-row-{id}` | `outerHTML` |
| Escalate grievance | `click` | POST `.../grievance/{id}/escalate/` | `#grievance-row-{id}` | `outerHTML` |
| Category chart load | `load` | GET `.../grievance/category-volume/` | `#category-chart-section` | `innerHTML` |
| SLA trend chart load | `load` | GET `.../grievance/sla-trend/` | `#sla-trend-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
