# 37 — POCSO Training Tracker

- **URL:** `/group/hr/pocso/training/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group POCSO Coordinator (Role 50, G3)

---

## 1. Purpose

The POCSO Training Tracker is the compliance monitoring page for mandatory POCSO (Protection of Children from Sexual Offences) Act awareness training across all branches of the group. Under Indian law, every adult working in an institution that provides services to children is required to receive POCSO awareness training. Failure to ensure this training makes the institution — and specifically the management — legally liable. This page is therefore a P0 compliance page: it has direct legal implications and must be kept current at all times.

Two training obligations are tracked here. The first is pre-contact training for new joiners: every new staff member must complete the POCSO awareness module before they are permitted to have any contact with students. This is an absolute rule with no grace period. The system marks any new joiner who is in student-contact status without POCSO completion as a Critical case, and this page surfaces a non-dismissible red alert banner listing those staff members by name. The POCSO Coordinator must resolve these cases — either by immediately scheduling an emergency training session or by restricting the staff member's student contact until completion.

The second obligation is the annual refresher: all staff, regardless of when they were originally trained, must complete an annual POCSO refresher. The tracker shows which staff have completed the current year's refresher, who is overdue, and which branches have scheduled their refresher sessions. The annual refresher is typically conducted as a group session at each branch — the POCSO Coordinator coordinates with branch principals to schedule these. Training certificates are generated upon completion and stored in each staff member's record.

The page also tracks POCSO Compliance at the branch level: each branch is scored on its compliance percentage. Branches at 100% are shown in green; branches below 90% receive an amber flag; branches with Critical cases (untrained staff in student contact) receive a red status. The POCSO Coordinator can export the full compliance report for submission to regulatory bodies or for the annual POCSO audit (page 39).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group POCSO Coordinator | G3 | Full view + Schedule training + Export | Primary owner |
| Group HR Director | G3 | Full read + Acknowledgement | Receives critical alerts |
| Group HR Manager | G3 | Read Only | General oversight |
| Group Training & Development Manager | G2 | Read (new joiner POCSO module only) | Coordinates with induction programme |
| Group BGV Manager | G3 | Read (BGV-linked status only) | POCSO completion is a BGV pre-check |
| Group Performance Review Officer | G1 | No Access | Not applicable |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > POCSO Compliance > POCSO Training Tracker`

### 3.2 Page Header
- **Title:** POCSO Training Tracker
- **Subtitle:** Mandatory POCSO awareness training compliance across all branches
- **Actions (top-right):**
  - `Schedule Training Session` (primary button — opens scheduling drawer)
  - `Export Compliance Report` (secondary button)
  - View Toggle: `Branch Summary` / `Staff List`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| New joiner in student contact without POCSO training | "CRITICAL: [N] new staff member(s) are in student contact without completing POCSO training. This is a legal violation. Immediate action required. Staff: [Names listed]." | Red — non-dismissible |
| Staff with annual refresh overdue > 30 days | "OVERDUE: [N] staff member(s) are overdue for their annual POCSO refresher by more than 30 days." | Amber — dismissible |
| Branch below 90% compliance | "WARNING: [N] branch(es) are below 90% POCSO training compliance." | Amber — dismissible |
| All branches 100% compliant | "All branches are at 100% POCSO compliance. No action required." | Green — auto-dismiss 10s |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| POCSO Trained Staff % | (Trained staff / Total staff) × 100 | Green ≥ 95%, Amber 90–94%, Red < 90% | No drill-down |
| Training Due This Month | Count with annual refresh due in current month | Amber if > 0 | Filters to due this month |
| New Joiners Untrained (Critical) | Count in student contact without completion | Red if > 0, Green if 0 | Filters to critical |
| Annual Refresh Due | Total count with refresh overdue or due within 30 days | Amber if > 0 | Filters to refresh due |
| Certificates Issued | Total certificates issued (lifetime) | Blue always | No drill-down |
| Branches 100% Compliant | Count of branches at 100% | Green if = total branches | Filters to 100% compliant |

---

## 5. Main Table — Branch POCSO Compliance Summary

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text + drill-down link | Yes | Yes — dropdown |
| Total Staff | Integer | Yes | No |
| Trained | Integer | Yes | No |
| Untrained (Never) | Integer (red if > 0) | Yes | Yes (> 0 filter) |
| Refresh Due | Integer | Yes | Yes (> 0 filter) |
| Last Training Session Date | Date | Yes | Yes — date range |
| Compliance Status | Badge (Compliant / At Risk / Critical) | No | Yes — multi-select |
| Actions | Drill-down icon + Schedule Training | No | No |

### 5.1 Filters
- **Compliance Status:** Compliant / At Risk / Critical
- **Has Untrained Staff:** Yes / No
- **Training Due This Month:** checkbox
- **Branch:** multi-select

### 5.2 Search
Free-text search on Branch Name. Debounced `hx-get` on keyup (400 ms).

### 5.3 Pagination
Server-side, 20 rows per page (branch-level view). Shows `Showing X–Y of Z branches`.

---

## 6. Drawers

### 6.1 Schedule Training Session
**Trigger:** `Schedule Training Session` button or per-branch Schedule icon
**Fields:**
- Branch(es) (multi-select)
- Training Type (radio: New Joiner Induction POCSO Module / Annual Refresher)
- Session Date and Time
- Session Format (radio: In-Person at Branch / Virtual)
- Trainer Name (text)
- Expected Attendees (auto-populated from selected branches' untrained staff list, editable)
- Notes
- Send Invite to Branch Principal (toggle)
- Schedule button → creates training session record and sends notification

### 6.2 Staff-Level Drill-Down
**Trigger:** Click branch row or drill-down icon
**Displays:** All staff in the selected branch with: Staff Name, Role, Training Type (Induction / Annual Refresh), Training Date, Certificate Number, Status (Trained / Untrained / Refresh Due). Filterable. Download Certificate action per trained staff. Mark Training Complete action (manual entry for offline sessions).

### 6.3 Mark Training Complete (Manual)
**Trigger:** Mark Complete button in staff drill-down or from Schedule view post-session
**Fields:**
- Select Staff (multi-select — for batch completion)
- Training Date (date picker)
- Trainer Name
- Certificate Number(s) (auto-generated or manual entry)
- Upload signed attendance sheet (optional, PDF)
- Confirm → updates training status, issues certificates, updates compliance %

### 6.4 View Certificate
**Trigger:** Certificate link in staff drill-down
**Action:** Renders the POCSO completion certificate as a PDF preview in an overlay. Download button available.

---

## 7. Charts

**POCSO Compliance Rate by Branch (Horizontal Bar Chart)**
- One bar per branch showing compliance %
- Red benchmark line at 100%
- Bars: Green (100%), Amber (90–99%), Red (< 90%)
- Sorted ascending (worst-performing branches at top)
- Tooltip: trained count, untrained count, refresh due count

**Training Completion Trend (Line Chart — last 12 months)**
- X-axis: Month
- Y-axis: Group-wide trained staff %
- Shows whether compliance is improving over time
- Spikes in training months (typically August for annual refresh) visible

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Training session scheduled | "POCSO training session scheduled for [Branch(es)] on [Date]." | Success | 4s |
| Training marked complete | "[N] staff member(s) marked as POCSO trained. Certificates issued." | Success | 5s |
| Certificate downloaded | "POCSO certificate downloaded for [Staff Name]." | Info | 3s |
| Critical case alert | "CRITICAL: [Staff Name] is in student contact without POCSO training. HR Director notified." | Error | Non-dismissible |
| Export started | "POCSO compliance report export started." | Info | 4s |
| Error marking complete | "Failed to mark training complete. Please check staff selection and date." | Error | 6s |

---

## 9. Empty States

- **No branches loaded:** "No branch data available."
- **All compliant:** "All branches are at 100% POCSO compliance. No training required this month."
- **No staff in drill-down:** "No staff found for this branch."
- **No training sessions scheduled:** "No upcoming POCSO training sessions. Click 'Schedule Training Session' to add one."

---

## 10. Loader States

- Branch table skeleton: 8 rows with shimmer.
- KPI cards: shimmer rectangles.
- Drill-down panel: spinner while staff-level training data loads.
- Chart area: placeholder with "Loading chart…" text.

---

## 11. Role-Based UI Visibility

| Element | POCSO Coordinator (G3) | HR Director (G3) | T&D Manager (G2) |
|---|---|---|---|
| Schedule Training Session button | Visible + enabled | Hidden | Hidden |
| Mark Training Complete | Visible + enabled | Hidden | Hidden |
| View Certificate | Visible | Visible | Hidden |
| Export Compliance Report | Visible | Visible | Hidden |
| Branch compliance table | Full view | Full view | New Joiner rows only |
| Critical alert banner | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/pocso/training/` | JWT G3 | Branch-level POCSO compliance summary |
| GET | `/api/v1/hr/pocso/training/{branch_id}/staff/` | JWT G3 | Staff-level training status for branch |
| POST | `/api/v1/hr/pocso/training/sessions/` | JWT G3 POCSO Coordinator | Schedule a training session |
| POST | `/api/v1/hr/pocso/training/complete/` | JWT G3 POCSO Coordinator | Mark batch training as complete |
| GET | `/api/v1/hr/pocso/training/certificates/{staff_id}/` | JWT G3 | Retrieve training certificate |
| GET | `/api/v1/hr/pocso/training/kpis/` | JWT G3 | KPI summary data |
| GET | `/api/v1/hr/pocso/training/charts/compliance/` | JWT G3 | Compliance rate by branch chart data |
| GET | `/api/v1/hr/pocso/training/charts/trend/` | JWT G3 | Compliance trend chart data |
| GET | `/api/v1/hr/pocso/training/export/` | JWT G3 | Export compliance report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search branch name | keyup changed delay:400ms | GET `/api/v1/hr/pocso/training/?q={val}` | `#pocso-table-body` | innerHTML |
| Filter change | change | GET `/api/v1/hr/pocso/training/?{params}` | `#pocso-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/pocso/training/?page={n}` | `#pocso-table-body` | innerHTML |
| Branch drill-down click | click | GET `/api/v1/hr/pocso/training/{branch_id}/staff/` | `#drill-down-panel` | innerHTML |
| Open schedule session drawer | click | GET `/api/v1/hr/pocso/training/sessions/new/` | `#drawer-container` | innerHTML |
| Submit schedule form | submit | POST `/api/v1/hr/pocso/training/sessions/` | `#pocso-table-body` | innerHTML |
| Submit mark-complete form | submit | POST `/api/v1/hr/pocso/training/complete/` | `#drill-down-panel` | innerHTML |
| Refresh KPI bar | htmx:afterRequest | GET `/api/v1/hr/pocso/training/kpis/` | `#kpi-bar` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
