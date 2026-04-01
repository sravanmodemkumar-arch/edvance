# 07 — Safety Audit Dashboard

> **URL:** `/group/welfare/safety-audit/`
> **File:** `07-safety-audit-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Safety Audit Officer (Role 96, G1) — exclusive post-login landing (Large groups only, read-only access G1)

---

## 1. Purpose

Primary post-login landing for the Group Safety Audit Officer. Command centre for the annual safety inspection program across all branches — managing the inspection calendar, recording findings across all seven safety category domains, tracking non-compliance items from discovery through corrective action to closure, and monitoring the overall safety posture of the group against minimum compliance thresholds.

The Safety Audit Officer holds a G1 read-only system role, meaning they cannot modify operational branch data, student records, or staff records. Their authority is scoped to: planning and scheduling inspections, recording inspection findings and scores, assigning corrective action owners and deadlines, adding notes to corrective action progress, and submitting the annual safety compliance report to the Group COO and Chairman. Every edit action on this dashboard is restricted to inspection-specific records — the officer cannot alter any data owned by other divisions. Inspections cover seven mandatory categories: fire safety, building structural safety, electrical safety, playground and sports facility safety, hostel safety (where applicable), transport yard safety, and food / kitchen safety. The full inspection cycle is completed once per academic year per branch, supplemented by surprise spot-check visits throughout the year.

Scale: 20–50 branches · 7 inspection categories per branch per year · 1 full cycle + 2–5 surprise visits per branch per year · corrective actions tracked to zero.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Safety Audit Officer | G1 | Restricted write — inspection records and corrective action notes only | Exclusive dashboard |
| Group COO | G4 | View — overall safety scores and critical non-compliances | Read-only |
| Group Chairman / CEO | G5 / G4 | View — annual safety compliance report summary | Not this URL |
| Branch Principal | G2 | View — own branch inspection status, non-compliances, and corrective actions | Branch-scoped |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('safety_audit_officer')`.
> **G1 write restriction enforced in all API endpoints:** write operations scoped to `inspection_records` and `corrective_action_notes` models only. All other models are read-only for this role.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Safety Audit Dashboard
```

### 3.2 Page Header
```
Welcome back, [Officer Name]                   [Export Safety Report ↓]  [Settings ⚙]
[Group Name] — Group Safety Audit Officer · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  Inspection Cycle: [N]% Complete  ·  Open Non-Compliances: [N]
```

### 3.3 Alert Banner (conditional — critical compliance items)

| Condition | Banner Text | Severity |
|---|---|---|
| Critical non-compliance unresolved > 30 days | "Critical non-compliance [ID] at [Branch] has been unresolved for [N] days. Corrective action escalation required." | Red |
| Branch not inspected in > 12 months | "[Branch] has not undergone a full safety inspection in [N] months. Inspection is overdue." | Red |
| Corrective action overdue > 60 days | "[N] corrective action(s) have exceeded their 60-day completion deadline. Review and escalate." | Red |
| Inspection due within 30 days not yet scheduled | "[N] branch inspection(s) are due within 30 days and have not been scheduled. Schedule now." | Amber |
| Overall safety score < 70% | "[Branch] overall safety score has fallen to [N]%. Targeted inspection recommended." | Amber |

Max 5 alerts visible. Alert links route to the relevant branch row or corrective action record. "View full audit log → Safety Audit History" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Inspection Completion % This Year | Branches that have completed their full annual inspection / total branches | Green ≥ 90% · Yellow 70–89% · Red < 70% | → Section 5.1 |
| Branches Inspected | Count of branches that have had at least one full inspection this AY / total | Green = all · Amber if some still pending | → Section 5.1 |
| Open Non-Compliance Items | Total active non-compliance findings across all branches not yet corrected | Green = 0 · Yellow 1–20 · Red > 20 | → Section 5.2 |
| Critical Non-Compliances | Non-compliance items classified as Critical severity | Green = 0 · Red if any | → Section 5.2 |
| Corrective Actions Overdue | Corrective actions past their assigned completion deadline | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.2 |
| Inspection Reports Submitted | Formal inspection reports submitted to Group COO this AY | Blue always (informational) | → Section 5.1 |
| Branches Pending First Inspection | Branches that have never been inspected under current AY cycle | Amber if any; Green = 0 | → Section 5.1 |
| Overall Safety Score % | Composite safety score averaged across all inspected branches | Green ≥ 85% · Yellow 70–84% · Red < 70% | → Section 5.3 |

**HTMX:** `hx-trigger="every 10m"` → Open Non-Compliance Items and Corrective Actions Overdue auto-refresh.

---

## 5. Sections

### 5.1 Branch Inspection Status Matrix

> Per-branch overview of the annual inspection cycle — primary audit planning and monitoring table.

**Search:** Branch name, city, zone. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Inspection Status | Radio | All / Fully Inspected / Partially Inspected / Not Inspected |
| Safety Score | Radio | All / ≥ 85% / 70–84% / < 70% |
| Open Non-Compliances | Checkbox | Show branches with any open items |
| Critical Non-Compliances | Checkbox | Show branches with critical items only |
| Next Inspection | Radio | All / Due Within 30 Days / Due Within 60 Days / Overdue |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → `branch-inspection-detail` drawer |
| Last Full Inspection Date | ✅ | Date; Red if > 12 months ago |
| Safety Score % | ✅ | Composite score; Green ≥ 85% · Yellow 70–84% · Red < 70% |
| Categories Inspected | ✅ | e.g., "6 / 7" — count of categories completed this AY |
| Open Non-Compliances | ✅ | Count; Red if any Critical |
| Critical Items | ✅ | Count; Red badge if > 0 |
| Next Scheduled Inspection | ✅ | Date or — if not scheduled; Amber if due within 30d |
| Report Submitted | ✅ | ✅ Submitted / ❌ Draft / — Not Started |
| Actions | ❌ | View · Schedule Inspection · View Non-Compliances |

> **G1 note:** No "Edit" or "Delete" buttons appear for operational branch data. "Schedule Inspection" opens the `schedule-inspection` form which creates an inspection_record only.

**Default sort:** Last Full Inspection Date ascending (longest overdue first).
**Pagination:** Server-side · 25/page.

---

### 5.2 Non-Compliance Tracker

> All open non-compliance findings with corrective action assignment and deadline monitoring.

**Search:** NC ID, branch, category, description keyword. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Category | Checkbox | Fire Safety / Building Structural / Electrical / Playground / Hostel / Transport Yard / Food Safety |
| Severity | Checkbox | Critical / Major / Minor |
| Status | Checkbox | Open / Corrective Action Assigned / In Progress / Overdue / Closed |
| Overdue | Checkbox | Show overdue only |
| Assigned To | Multi-select | All staff / department heads |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| NC ID | ✅ | System-generated; link → NC detail modal |
| Branch | ✅ | |
| Inspection Date | ✅ | Date of inspection when finding was recorded |
| Category | ✅ | Inspection domain badge |
| Severity | ✅ | Critical (Red) / Major (Orange) / Minor (Yellow) |
| Finding Description | ❌ | Truncated to 80 chars; full text in NC detail modal |
| Assigned To | ✅ | Name of branch staff or HOD accountable for correction |
| Due Date | ✅ | Corrective action deadline; Red if overdue · Amber if due within 7 days |
| Status | ✅ | Colour-coded badge |
| Overdue by | ✅ | Days overdue; Red badge if > 0 |
| Actions | ❌ | View · Add Note · Mark Closed |

> **G1 note:** "Mark Closed" is the only status-change permitted for the Safety Audit Officer; it represents formal sign-off that a corrective action has been verified as complete. "Add Note" appends a corrective action note only.

**Default sort:** Severity (Critical first), then Due Date ascending (most overdue first).
**Pagination:** Server-side · 25/page.

---

### 5.3 Safety Score Chart

> Bar chart comparing safety scores across all inspected branches, sorted worst to best.

**Chart type:** Vertical bar chart.

- X-axis: Branch names, sorted ascending by safety score (worst branch on left)
- Y-axis: Safety score % (0–100)
- Colour bands: Red fill < 70% · Yellow fill 70–84% · Green fill ≥ 85%
- Reference line: 85% target (dotted horizontal line)
- Tooltip: Branch · Overall score % · Category breakdown (7 scores) · Last inspection date · Inspector name
- Click bar → `branch-inspection-detail` drawer at Summary tab

Below chart: Table of category scores across all branches (branch rows × category columns) — a quick cross-view to identify which category type has the most widespread non-compliance.

---

### 5.4 Inspection Calendar

> Upcoming scheduled inspections for the next 60 days — planning view.

**Display:** Table format (calendar grid optional toggle on desktop).

**Columns:** Scheduled Date · Branch · Inspection Type (Full Annual / Surprise Visit / Re-Inspection / Category-Specific) · Inspector (name of audit officer conducting) · Status (Scheduled / Confirmed / In Progress / Completed / Cancelled) · Categories Covered

**Filters:** Date range (next 7d / next 30d / next 60d / custom) · Inspection Type · Branch

**Actions per row:** View · Reschedule · Cancel (all open `schedule-inspection` drawer pre-filled)

> **G1 note:** Safety Audit Officer can schedule, reschedule, and cancel inspection appointments. Cannot edit branch operational records or non-compliance items other than adding notes.

---

## 6. Drawers / Modals

### 6.1 Drawer: `branch-inspection-detail`
- **Trigger:** Branch name link in Section 5.1 table
- **Width:** 640px
- **Tabs:** Summary · Categories · Non-Compliances · Corrective Actions · History

**Summary tab:**
- Branch name · Last full inspection date · Inspector · Overall safety score %
- Score breakdown by category (bar or progress bar per category)
- Inspection report status · Submitted to COO date (if submitted)
- Next scheduled inspection date

**Categories tab:**
- One row per inspection category (7 total)
- Category · Inspection date · Score % · Items Checked · Non-compliances found · Status (Complete / Pending)
- Click category row → expands checklist of items with pass/fail/NA status

**Non-Compliances tab:**
- All NC items for this branch: NC ID · Category · Severity · Finding · Due Date · Status · Assigned To
- Sorted: Critical first, then by due date

**Corrective Actions tab:**
- Per NC item: NC ID · Action description · Assigned to · Due date · Progress notes (chronological) · Status
- [Add Note] button per action row (available to Safety Audit Officer only)

**History tab:**
- All past inspection records for this branch (beyond current AY): Date · Type · Inspector · Score · Report status

---

### 6.2 Drawer: `schedule-inspection`
- **Trigger:** "Schedule Inspection" action in Section 5.1 or from Section 5.4 calendar
- **Width:** 480px
- **Mode:** Create / Edit inspection record

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Select | Required |
| Inspection Type | Radio | Full Annual / Surprise Visit / Re-Inspection / Category-Specific |
| Scheduled Date | Date | Required; must be future date |
| Start Time | Time | Required |
| Inspector(s) | Multi-select | From safety audit team roster |
| Categories to Cover | Multi-checkbox | Fire / Building / Electrical / Playground / Hostel / Transport Yard / Food Safety — all selected by default for Full Annual |
| Pre-Inspection Notice | Toggle | If Yes: branch principal notification sent on save |
| Notice Days in Advance | Number | Conditional — appears if Pre-Inspection Notice = Yes; default 3 days |
| Notes | Textarea | Optional; internal planning notes |

**Validation:** Branch and date required · At least one category must be selected · Inspector required · For Surprise Visit, Pre-Inspection Notice must be set to No.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Inspection scheduled | "Inspection scheduled at [Branch] on [date]. [Branch Principal has been notified / Surprise — no notice sent]." | Success | 4s |
| Inspection rescheduled | "Inspection at [Branch] rescheduled to [new date]." | Info | 4s |
| NC note added | "Note added to non-compliance [NC ID] at [Branch]." | Success | 4s |
| NC marked closed | "Non-compliance [NC ID] at [Branch] closed. Corrective action verified." | Success | 5s |
| Report submitted | "Safety inspection report for [Branch] submitted to Group COO." | Success | 5s |
| Safety report exported | "Safety compliance report export prepared. Download ready." | Info | 4s |
| Inspection cancelled | "Inspection at [Branch] on [date] cancelled." | Warning | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open non-compliances | "Zero Open Non-Compliances" | "All non-compliance items across all branches have been corrected and closed." | — |
| No branches inspected yet | "No Inspections Completed This Year" | "The annual inspection cycle has not started. Schedule inspections for all branches." | [Schedule Inspection] |
| No upcoming inspections | "No Inspections Scheduled" | "No inspections are scheduled in the next 60 days. Plan the next inspection round." | [Schedule Inspection] |
| Search returns no results | "No Results Found" | "No branches or non-compliance items match your search or filters." | [Clear Filters] |
| No critical non-compliances | "No Critical Non-Compliances Open" | "All critical safety findings have been corrected across all branches." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + inspection matrix table (15 rows × 9 columns) + NC tracker table + score chart + calendar table + alerts |
| Table filter/search | Inline skeleton rows (8 rows) |
| KPI auto-refresh | Shimmer on individual card values; labels preserved |
| Safety score chart load | Chart area skeleton (grey rectangle, 600×250px placeholder with animated gradient) |
| Category cross-table load | Table skeleton (7 columns × 10 rows) |
| Branch detail drawer open | 640px drawer skeleton; each tab loads lazily on first click |
| Schedule inspection drawer open | 480px drawer form skeleton |

---

## 10. Role-Based UI Visibility

| Element | Safety Audit Officer G1 | Group COO G4 | Chairman / CEO G5 | Branch Principal G2 |
|---|---|---|---|---|
| View All Branches | ✅ | ✅ | ✅ | Own branch only |
| Schedule Inspection | ✅ | ❌ | ❌ | ❌ |
| Record Inspection Finding | ✅ | ❌ | ❌ | ❌ |
| Add Corrective Action Note | ✅ | ❌ | ❌ | ❌ |
| Close NC Item | ✅ | ❌ | ❌ | ❌ |
| Assign NC to Staff | ✅ | ❌ | ❌ | ❌ |
| Submit Inspection Report | ✅ | ❌ | ❌ | ❌ |
| View Inspection Reports | ✅ | ✅ | ✅ | Own branch only |
| Edit Branch Operational Data | ❌ (G1 restriction) | ❌ | ❌ | ✅ (own branch) |
| Export Safety Report | ✅ | ✅ | ✅ | ❌ |
| Delete Inspection Record | ❌ | ❌ | ❌ | ❌ |
| Cancel Inspection | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/safety-audit/dashboard/` | JWT (G1+) | Full dashboard data payload |
| GET | `/api/v1/group/{group_id}/welfare/safety-audit/kpi-cards/` | JWT (G1+) | KPI auto-refresh values |
| GET | `/api/v1/group/{group_id}/welfare/safety-audit/branch-matrix/` | JWT (G1+) | Branch inspection status matrix; params: `status`, `score_lt`, `has_critical`, `next_due_days`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/safety-audit/non-compliances/` | JWT (G1+) | NC tracker; params: `branch_id`, `category`, `severity`, `status`, `overdue`, `page` |
| POST | `/api/v1/group/{group_id}/welfare/safety-audit/non-compliances/{nc_id}/notes/` | JWT (G1) | Add note to corrective action |
| PATCH | `/api/v1/group/{group_id}/welfare/safety-audit/non-compliances/{nc_id}/close/` | JWT (G1) | Close NC item (verify corrective action complete) |
| GET | `/api/v1/group/{group_id}/welfare/safety-audit/schedule/` | JWT (G1+) | Inspection calendar; params: `from_date`, `to_date`, `branch_id`, `type` |
| POST | `/api/v1/group/{group_id}/welfare/safety-audit/schedule/` | JWT (G1) | Create inspection record; body: `branch_id`, `type`, `date`, `time`, `inspectors`, `categories`, `notice_sent` |
| PATCH | `/api/v1/group/{group_id}/welfare/safety-audit/schedule/{inspection_id}/` | JWT (G1) | Reschedule or update inspection |
| DELETE | `/api/v1/group/{group_id}/welfare/safety-audit/schedule/{inspection_id}/` | JWT (G1) | Cancel inspection (soft-delete with reason) |
| GET | `/api/v1/group/{group_id}/welfare/branches/{branch_id}/inspection-detail/` | JWT (G1+) | Branch inspection detail drawer payload |
| POST | `/api/v1/group/{group_id}/welfare/safety-audit/reports/submit/` | JWT (G1) | Submit inspection report to COO; body: `branch_id`, `inspection_id` |
| GET | `/api/v1/group/{group_id}/welfare/safety-audit/score-chart/` | JWT (G1+) | Branch safety score chart data |
| GET | `/api/v1/group/{group_id}/welfare/safety-audit/export/` | JWT (G1+) | Async safety compliance report export; params: `format`, `include_nc_detail` |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 10m` | GET `.../safety-audit/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch matrix search | `input delay:300ms` | GET `.../safety-audit/branch-matrix/?q={val}` | `#branch-matrix-body` | `innerHTML` |
| Branch matrix filter | `click` | GET `.../safety-audit/branch-matrix/?{filters}` | `#branch-matrix-section` | `innerHTML` |
| Branch matrix pagination | `click` | GET `.../safety-audit/branch-matrix/?page={n}` | `#branch-matrix-section` | `innerHTML` |
| NC tracker search | `input delay:300ms` | GET `.../safety-audit/non-compliances/?q={val}` | `#nc-table-body` | `innerHTML` |
| NC tracker filter | `click` | GET `.../safety-audit/non-compliances/?{filters}` | `#nc-section` | `innerHTML` |
| NC tracker pagination | `click` | GET `.../safety-audit/non-compliances/?page={n}` | `#nc-section` | `innerHTML` |
| Open branch drawer | `click` on branch name | GET `.../welfare/branches/{id}/inspection-detail/` | `#drawer-body` | `innerHTML` |
| Open schedule drawer (new) | `click` Schedule Inspection | GET `.../safety-audit/schedule/create-form/` | `#drawer-body` | `innerHTML` |
| Open schedule drawer (edit) | `click` Reschedule | GET `.../safety-audit/schedule/{id}/edit-form/` | `#drawer-body` | `innerHTML` |
| Submit new inspection | `click` Save | POST `.../safety-audit/schedule/` | `#calendar-section` | `innerHTML` |
| Add NC note | `click` Add Note | POST `.../safety-audit/non-compliances/{id}/notes/` | `#nc-notes-{id}` | `innerHTML` |
| Close NC item | `click` Mark Closed | PATCH `.../safety-audit/non-compliances/{id}/close/` | `#nc-row-{id}` | `outerHTML` |
| Safety score chart load | `load` | GET `.../safety-audit/score-chart/` | `#score-chart-section` | `innerHTML` |
| Calendar filter change | `change` | GET `.../safety-audit/schedule/?{filters}` | `#calendar-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
