# 14 — NSS Programme Tracker

> **URL:** `/group/nss/programmes/`
> **File:** `14-nss-programme-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Group NSS/NCC Coordinator (Role 100, G3) — full; Group Cultural Activities Head (Role 99, G3) — view

---

## 1. Purpose

Central tracker for the National Service Scheme (NSS) across all branches in the group. Each branch may operate one or more NSS units, each affiliated with a university and led by a Programme Officer. NSS requires enrolled volunteers to accumulate 240 hours of community service per academic year (April 1 – March 31). Failure to meet the 240-hour threshold means a student does not receive the NSS certificate, which is a mandatory credential for certain government jobs, postgraduate admissions, and state-level awards.

The Group NSS/NCC Coordinator uses this page to: monitor enrolment counts across all branches; track activity logging and volunteer-hour accumulation; identify branches where volunteers are falling behind the 240-hour target; verify activity records submitted by branch Programme Officers; manage NSS unit registrations (unit code, university affiliation, officer details); and export data for submission to the state NSS directorate. The Cultural Activities Head has view-only access to monitor calendar overlap with cultural events.

Scale: Large groups operate 2,000–8,000 NSS volunteers spread across all branches. Activity logging is frequent (multiple activities per branch per month), so pagination, bulk operations, and server-side filtering are critical. Hour accumulation is recalculated on each activity verification to keep volunteer progress current.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group NSS/NCC Coordinator | 100 | G3 | Full — view all branches, create/edit NSS units, log activities, verify records, export, generate reports | Primary owner |
| Group Cultural Activities Head | 99 | G3 | View only — branch summary table, activity list, KPI cards; no write actions, no verification | Calendar cross-reference use case |
| Group Sports Director | 97 | G3 | No access | Redirected to own dashboard |
| Group Library Head | 101 | G2 | No access | Redirected to own dashboard |
| All other roles | — | — | No access | Redirected to own dashboard |

> **Access enforcement:** Django decorator `@require_role(['nss_ncc_coordinator', 'cultural_head'])` gates page load. Write endpoints (`/api/nss/activities/create/`, `/api/nss/units/create/`, `/api/nss/activities/verify/`) further restricted to `nss_ncc_coordinator` via `@require_role(['nss_ncc_coordinator'])`. Cultural Head queries use the same ORM querysets but all action buttons are suppressed by server-side role check before template render.

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group HQ  ›  Sports & Extra-Curricular  ›  NSS  ›  NSS Programme Tracker
```

### 3.2 Page Header

```
NSS Programme Tracker                          [+ Log Activity]  [+ Register Unit]  [Export ↓]
Group NSS/NCC Coordinator — [Officer Name]
AY [YYYY-YY]  ·  [N] Branches  ·  [N] NSS Units  ·  [N] Volunteers  ·  [N]% Reached 240h
```

`[+ Log Activity]` — opens `nss-activity-log` drawer (Coordinator only; hidden for Cultural Head).
`[+ Register Unit]` — opens `nss-unit-create` drawer (Coordinator only; hidden for Cultural Head).
`[Export ↓]` — downloads filtered branch NSS summary to XLSX or PDF; available to both roles but Cultural Head export excludes volunteer PII.

### 3.3 Alert Banners (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any branch with no NSS unit registered | "[N] branch(es) have no registered NSS unit for this AY. Register a unit to begin tracking." | Yellow |
| Group 240h completion rate < 50% and AY > 70% elapsed | "Overall 240h completion rate is [N]%. Only [N] months remain in the academic year." | Red |
| Activities not logged in any branch for > 30 days | "[N] branch(es) have had no NSS activity in the last 30 days." | Yellow |
| Unverified activities > 20 group-wide | "[N] activities are pending verification." | Blue |

---

## 4. KPI Summary Bar

Six KPI cards rendered in a horizontal scrollable bar. All values scoped to the selected academic year. Values fetched via HTMX on page load; each card independently re-fetchable.

| Card | Metric | Calculation | HTMX Target | Empty State |
|---|---|---|---|---|
| Total NSS Volunteers | Count of all enrolled volunteers across all branches this AY | `NSSEnrolment.objects.filter(ay=current_ay).count()` | `#kpi-total-volunteers` | "0" with grey badge |
| Branches with Active NSS Unit | Count of branches with at least one registered NSS unit | `NSSUnit.objects.filter(ay=current_ay, is_active=True).values('branch').distinct().count()` | `#kpi-active-units` | "0 / [N]" |
| 240h Achievers (This AY) | Volunteers whose accumulated hours ≥ 240 | `NSSVolunteer.objects.filter(total_hours__gte=240, ay=current_ay).count()` | `#kpi-achievers` | "0" |
| Activities This Month | Count of logged activities (any status) in current calendar month | `NSSActivity.objects.filter(date__month=today.month).count()` | `#kpi-activities-month` | "0" |
| Special Camp Participation Rate | % of enrolled volunteers who attended ≥ 1 Special Camp this AY | Computed as `(special_camp_attendees / total_volunteers) * 100` | `#kpi-special-camp` | "—" if no camps logged |
| Branches Without NSS Unit | Branches in group with no active NSS unit this AY | `Branch.objects.exclude(nssunit__ay=current_ay, nssunit__is_active=True).count()` | `#kpi-no-unit` | "0" in green badge |

**HTMX pattern:** On page load, each card fires `hx-get` to its dedicated endpoint with `hx-trigger="load"` and `hx-swap="innerHTML"`. Each card shows a skeleton loader (grey animated rectangle, 48px tall) until data arrives. AY selector at top-right of KPI bar triggers `hx-get` with `hx-include="[name=ay]"` to refresh all six cards simultaneously via out-of-band swap (`hx-swap-oob="true"`).

---

## 5. Sections

### 5.1 Branch NSS Unit Summary

Main overview table. One row per branch (branches without a unit still appear, flagged). Server-side paginated at 25 rows/page.

**Table Columns:**

| Column | Field | Notes |
|---|---|---|
| Branch | `branch.name` | Sortable; clickable link opens branch NSS detail |
| NSS Unit Code | `NSSUnit.unit_code` | Text; "—" if no unit registered; badge "Not Registered" (orange) if missing |
| Programme Officer | `NSSUnit.officer_name` | Text; "—" if no unit |
| Volunteers Enrolled | `NSSUnit.volunteer_count` | Integer; sortable |
| Avg Hours Completed | Average of `NSSVolunteer.total_hours` for that unit | Decimal (1dp); colour: green ≥ 200, yellow 100–199, red < 100 |
| 240h Achievers | Count of volunteers in unit with `total_hours ≥ 240` | Integer |
| Activities This Month | Count of `NSSActivity` records for this unit in current month | Integer |
| Last Activity Date | `max(NSSActivity.date)` for unit | Date; red text if > 30 days ago; "Never" (red) if no activities |
| Actions | Inline action buttons | "View Unit", "Add Activity", "View Volunteers" |

**Inline Actions:**
- `View Unit` — opens `volunteer-list-view` drawer scoped to that branch's unit.
- `Add Activity` — opens `nss-activity-log` drawer with Branch pre-filled (Coordinator only; hidden for Cultural Head).
- `View Volunteers` — opens `volunteer-list-view` drawer on Enrolled Volunteers tab.

**Filter Drawer (hx-get `/api/nss/units/` with params):**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select checkbox | All branches in group |
| Has NSS Unit | Radio | All / Yes / No |
| Avg Hours Completion | Radio | All / High (> 200h) / Medium (100–200h) / Low (< 100h) |

Active filters rendered as dismissible chips below the filter bar. "Clear All" removes all chips and resets table.

**Search:** Free-text on Branch name, Programme Officer name. `hx-trigger="keyup changed delay:400ms"`.

**Pagination:** `hx-get` with `page` param; `hx-target="#unit-summary-table-body"`.

---

### 5.2 Recent Activities (Last 30 Days)

Table of all NSS activities logged group-wide in the last 30 calendar days. Server-side paginated at 25 rows/page. Default sort: Date DESC.

**Table Columns:**

| Column | Field | Notes |
|---|---|---|
| Activity Name | `NSSActivity.name` | Truncated at 40 chars; tooltip on hover for full name |
| Activity Type | `NSSActivity.activity_type` | Colour-coded badge: Community Service (blue), Environmental (green), Blood Donation (red), Health Awareness (teal), Literacy Drive (purple), Special Camp (gold), Disaster Preparedness (orange), Voter Awareness (indigo), Digital Literacy (cyan) |
| Branch | `activity.unit.branch.name` | Text |
| Date | `NSSActivity.date` | DD MMM YYYY |
| Participants | `NSSActivity.participant_count` | Integer |
| Hours Credit | `NSSActivity.hours_credit_per_volunteer` | Integer (per volunteer) |
| Logged By | `NSSActivity.logged_by.full_name` | Name of user who created the record |
| Verification Status | `NSSActivity.verification_status` | Badge: Logged (grey) / Verified (green) / Rejected (red) |
| Actions | Inline | "View" always visible; "Verify" and "Reject" visible for Coordinator only when status = Logged |

**Verify / Reject flow:** Clicking "Verify" triggers `hx-post` to `/api/nss/activities/{id}/verify/`. On success, row's Verification Status badge swaps to "Verified" (green) via `hx-swap="outerHTML"` on that row. Clicking "Reject" opens a small inline input for Rejection Reason, then `hx-post` to `/api/nss/activities/{id}/reject/`.

---

### 5.3 240-Hour Achievement Tracker

Summary section combining a compact chart and a data table. Shows distribution of volunteers by hours-completion tier across all branches.

**Compact Stats (above table):**

Four inline stat chips:
- Volunteers ≥ 240h — green badge
- Volunteers 200–239h — yellow badge
- Volunteers 100–199h — orange badge
- Volunteers < 100h — red badge

**Table Columns:**

| Column | Field | Notes |
|---|---|---|
| Branch | `branch.name` | Sortable |
| Enrolled | Total volunteers in unit | Integer |
| Completed 240h | Count with `total_hours ≥ 240` | Integer |
| 200–239h | Count in range | Integer |
| 100–199h | Count in range | Integer |
| < 100h | Count in range | Integer |
| Completion % | `(240h count / enrolled) * 100` | Percentage; colour: green > 70% / yellow 40–70% / red < 40% |

This table is not paginated (branch-level, typically ≤ 50 rows). Sortable on all numeric columns.

---

### 5.4 NSS Certificate Readiness Tracker

> Year-end critical section. The NSS Certificate (government-recognised credential) is issued to volunteers who complete 240 verified hours AND have attended at least 1 mandatory Special Camp. This section surfaces certificate-readiness at a glance and provides the bulk-generate workflow. For full certificate management, see **Page 22 — NSS Certificate Management** (`/group/nss/certificates/`).

**Quick Stats (4 inline chips above table):**
- Completed 240h + Special Camp → **Eligible** (green)
- Completed 240h but no Special Camp → **Hours OK, Camp Missing** (amber)
- 200–239h (reachable this AY) → **Close to Target** (yellow)
- < 200h (at risk) → **At Risk** (red)

**Table Columns:**

| Column | Notes |
|---|---|
| Branch | Branch name |
| Enrolled | Total volunteers |
| Eligible (240h + Camp) | Count meeting both criteria — green |
| 240h Only (no camp) | Count with hours done but no special camp — amber |
| Close (200–239h) | Count in 200–239h range — yellow |
| At Risk (<200h) | Count below 200h — red |
| Certificates Generated | Count with certificate already generated |
| Actions | [View Eligible List] · [Generate Certificates] (opens Page 22 workflow) |

**[Generate All Certificates →]** button (Coordinator only) — navigates to Page 22 (`/group/nss/certificates/`) for the full bulk certificate generation workflow, state directorate export, and download management.

---

### 5.5 NSS Programme Officer Directory

> Cross-branch view of all NSS Programme Officers (POs). A large group with 50 branches has up to 50 Programme Officers. Monitoring their training status, term dates, and university affiliation from a single view is essential for programme quality. For full management, see **Page 22 — NSS Certificate Management** which includes the full Programme Officer registry with edit capability.

**Display:** Compact table — all branches.

| Column | Notes |
|---|---|
| Branch | Branch name (link) |
| NSS Unit Code | Text; "Not Registered" (orange badge) if missing |
| Programme Officer | Name; "—" if no unit |
| University | Affiliated university |
| Training Status | Badge: Trained (green) / Pending (amber) / Overdue (red) |
| Term End Date | Date; red if expired or < 30 days remaining |
| Actions | [Edit] (opens `nss-officer-edit` drawer 480px) · [Send Reminder] |

`[Send Reminder]` — opens modal with WhatsApp/email reminder template pre-filled; sends to Programme Officer and CC: Branch Principal.

**Filter:** Branch (multi-select), Training Status (multi-select).

---

## 6. Drawers & Modals

### 6.1 Drawer: `nss-activity-log` (480px, slides from right)

**Trigger:** `[+ Log Activity]` button or inline "Add Activity" in Section 5.1.

**4 Tabs:**

#### Tab 1 — Activity

| Field | Type | Validation | Notes |
|---|---|---|---|
| Activity Name | Text input | Required; min 3, max 150 chars | Placeholder: "e.g. Blood Donation Camp — March 2026" |
| Activity Type | Select | Required | Options: Community Service / Environmental (Tree Plantation/Cleanliness) / Blood Donation Camp / Health Awareness / Literacy Drive / Special Camp / Disaster Preparedness / Voter Awareness / Digital Literacy |
| Start Date | Date picker | Required; must not be in future | |
| End Date | Date picker | Required; ≥ Start Date | |
| Duration | Text input | Required; max 50 chars | Placeholder: "e.g. 1 Day, 3 Hours, 2 Weeks" |
| Description | Textarea | Optional; max 500 chars | Character counter displayed |

#### Tab 2 — Branch

| Field | Type | Validation | Notes |
|---|---|---|---|
| Branch | Select | Required | Dropdown of all branches with active NSS units |
| NSS Unit Code | Text (read-only) | Auto-filled | Populated via `hx-get="/api/nss/units/by-branch/?branch={id}"` on Branch selection |
| Programme Officer | Text (read-only) | Auto-filled | Same HTMX call as above |
| Venue | Text input | Optional; max 200 chars | |

#### Tab 3 — Participants

| Field | Type | Validation | Notes |
|---|---|---|---|
| Participant Count | Number input | Required; min 1; integer | |
| Hours Credit Per Volunteer | Number input | Required; min 1, max 24 | Hours each participant earns |
| Upload Attendance Sheet | File upload | Optional; PDF or Excel (.xlsx); max 5 MB | Stored in `/media/nss/attendance/` |
| Volunteer Names | Textarea | Optional; max 2000 chars | Free text list; note shown: "Or link individual records via 'View Volunteers'" |

#### Tab 4 — Hours

| Field | Type | Validation | Notes |
|---|---|---|---|
| Certificate Issued? | Toggle | Default Off | |
| Certificate Upload | File upload | Conditional — shown only if Certificate Issued is On; PDF only; max 5 MB | |
| Verification Notes | Text input | Optional; max 300 chars | For verifier to note observations |
| Internal Notes | Textarea | Optional; max 500 chars | Not visible to branch officers |

**Footer Buttons:** `[Save Draft]` — status = Logged; `[Save & Verify]` — status = Verified (Coordinator only); `[Cancel]`.

---

### 6.2 Drawer: `nss-unit-create` (480px, slides from right)

**Trigger:** `[+ Register Unit]` button. Coordinator only.

| Field | Type | Validation | Notes |
|---|---|---|---|
| Branch | Select | Required | Only branches without an active NSS unit for this AY shown |
| Programme Officer Name | Text input | Required; max 150 chars | |
| Officer Employee ID | Text input | Required; max 50 chars | Must match HR system employee ID format |
| NSS Unit Registration No | Text input | Optional; max 100 chars | Assigned by affiliated university |
| University Affiliation | Text input | Optional; max 200 chars | |
| Year Established | Year select | Optional | Range: 1969 – current year |
| Max Volunteer Capacity | Number input | Optional; min 1 | If blank, no cap enforced |
| Notes | Textarea | Optional; max 500 chars | |

**Footer Buttons:** `[Register Unit]`; `[Cancel]`.

On success: toast "NSS unit registered for [Branch Name]." and row appears in Section 5.1 table via `hx-swap-oob="true"` on `#unit-summary-table-body`.

---

### 6.3 Drawer: `volunteer-list-view` (560px, slides from right)

**Trigger:** "View Unit" or "View Volunteers" inline actions in Section 5.1.

**Header:** Branch name, Unit Code, Programme Officer name, Enrolled count.

**2 Tabs:**

#### Tab 1 — Enrolled Volunteers

Paginated table (25/page):

| Column | Notes |
|---|---|
| Name | Student full name |
| Class / Year | e.g. "B.Sc. III Year" |
| Roll No | Student roll number |
| Hours Accumulated | `NSSVolunteer.total_hours`; colour: green ≥ 240, yellow 100–239, red < 100 |
| Activities Count | Number of activities the volunteer has participated in this AY |
| 240h Status | Badge: Achieved (green check) / In Progress (yellow) / At Risk (red x) |
| Actions | "View Hours Log" — opens nested modal `volunteer-hours-log` |

#### Tab 2 — Hours Progress

Sortable table (same volunteers, sorted by `total_hours` DESC by default):

| Column | Notes |
|---|---|
| Name | |
| Total Hours | Large numeric display |
| Hours This Month | Hours credited in current calendar month |
| Hours Needed | `max(0, 240 - total_hours)`; green if 0 (achieved) |
| Last Activity | Date of most recent activity participation |

**Footer:** `[Export Volunteer List]` — XLSX download scoped to this unit.

---

### 6.4 Modal: `volunteer-hours-log` (560px, centred)

**Trigger:** "View Hours Log" in Tab 1 of `volunteer-list-view`.

Displays a chronological log of all activities the volunteer participated in this AY:

| Column | Notes |
|---|---|
| Date | Activity date |
| Activity Name | |
| Activity Type | Badge |
| Hours Credited | |
| Verification Status | Badge |
| Certificate | "View" link if certificate was uploaded |

**Footer:** `[Close]`.

---

## 7. Charts

### 7.1 Monthly NSS Activity Count (Last 6 Months)

- **Type:** Vertical bar chart
- **X-axis:** Last 6 calendar months (e.g. Oct 2025 – Mar 2026)
- **Y-axis:** Count of NSS activities logged
- **Series:** Single series (all branches combined). Optionally toggled to per-branch stacked view via a "Breakdown by Branch" toggle above the chart.
- **Data endpoint:** `GET /api/nss/charts/monthly-activity-count/?ay={ay}&months=6`
- **HTMX:** `hx-get` on page load; `hx-trigger="load"`. Rendered as Chart.js canvas injected into `#chart-monthly-activity`.
- **Empty state:** "No activities logged in the last 6 months." with grey bar icons.

### 7.2 Hours Completion Distribution (Donut Chart)

- **Type:** Donut chart
- **Segments:** < 100h (red) / 100–199h (orange) / 200–239h (yellow) / 240h+ (green)
- **Centre label:** "Total Volunteers: [N]"
- **Legend:** Below chart, showing segment label + count + percentage.
- **Data endpoint:** `GET /api/nss/charts/hours-distribution/?ay={ay}`
- **HTMX:** `hx-get` on page load; `hx-trigger="load"`. Rendered into `#chart-hours-donut`.
- **Empty state:** Grey empty donut with "No volunteer hours recorded."

---

## 8. Toast Messages

All toasts appear bottom-right. Auto-dismiss after 4 seconds. Error toasts persist until manually dismissed.

| Trigger | Toast Text | Type |
|---|---|---|
| Activity logged successfully | "Activity '[Name]' logged for [Branch]." | Success |
| Activity verified | "Activity '[Name]' has been verified." | Success |
| Activity rejected | "Activity '[Name]' has been rejected." | Warning |
| NSS unit registered | "NSS unit registered for [Branch Name]." | Success |
| File upload exceeds 5 MB | "File too large. Maximum allowed size is 5 MB." | Error |
| Invalid file type uploaded | "Invalid file type. Please upload PDF or Excel only." | Error |
| Save draft failed (validation error) | "Please complete all required fields before saving." | Error |
| Export triggered | "Preparing export… You will be notified when ready." | Info |
| API error (non-2xx response) | "Something went wrong. Please try again or contact support." | Error |
| No NSS unit found for selected branch | "No active NSS unit found for this branch. Register a unit first." | Warning |

---

## 9. Empty States

| Section / Component | Condition | Icon | Heading | Body Text | CTA |
|---|---|---|---|---|---|
| Section 5.1 — Branch NSS Unit Summary | No branches in group | clipboard-list | "No Branches Found" | "No branches are registered in this group." | — |
| Section 5.1 — filtered result empty | Active filters return no rows | filter | "No Matching Branches" | "Adjust your filters or search term." | [Clear Filters] |
| Section 5.2 — Recent Activities | No activities in last 30 days | calendar-x | "No Recent Activities" | "No NSS activities have been logged in the last 30 days." | [+ Log Activity] (Coordinator only) |
| Section 5.3 — 240h Tracker | No volunteer data | users | "No Volunteer Data" | "Enrol volunteers in NSS units to begin tracking hours." | — |
| `volunteer-list-view` drawer | Unit has no enrolled volunteers | user-plus | "No Volunteers Enrolled" | "No volunteers are enrolled in this NSS unit for this academic year." | — |
| `volunteer-hours-log` modal | Volunteer has no activity log | clock | "No Hours Logged" | "This volunteer has not participated in any recorded NSS activity this year." | — |
| Chart 7.1 | No activities logged in 6 months | bar-chart-2 | "No Activity Data" | "No NSS activities have been logged in the last 6 months." | — |
| Chart 7.2 | No volunteers enrolled | pie-chart | "No Volunteer Data" | "Enrol volunteers to begin tracking hour completion." | — |

---

## 10. Loader States

| Component | Loader Type | Duration Trigger |
|---|---|---|
| KPI cards (all 6) | Skeleton rectangle (48px tall, full card width, animated pulse) | Until `hx-get` response received |
| Section 5.1 table body | Skeleton rows (5 rows × column widths, animated pulse) | Until table data fetched |
| Section 5.2 table body | Skeleton rows (5 rows) | Until data fetched |
| Section 5.3 table body | Skeleton rows (3 rows) | Until data fetched |
| `nss-activity-log` drawer content | Spinner centred in drawer body | While branch unit auto-fill HTMX call in-flight |
| `volunteer-list-view` drawer | Skeleton rows in tab pane | Until volunteer list fetched |
| Chart 7.1 | Skeleton rectangle (200px tall, full width) | Until Chart.js render |
| Chart 7.2 | Skeleton circle (160px diameter) | Until Chart.js render |
| File upload in drawer | Inline progress bar below upload field | During upload |

---

## 11. Role-Based UI Visibility

| UI Element | NSS/NCC Coordinator (100) | Cultural Head (99) | Sports Director (97) | Library Head (101) |
|---|---|---|---|---|
| Page access | Yes | Yes (view only) | No — redirect | No — redirect |
| `[+ Log Activity]` button | Visible + active | Hidden | — | — |
| `[+ Register Unit]` button | Visible + active | Hidden | — | — |
| `[Export ↓]` button | Visible (full export) | Visible (no PII) | — | — |
| Section 5.1 — "Add Activity" inline action | Visible | Hidden | — | — |
| Section 5.2 — "Verify" / "Reject" actions | Visible | Hidden | — | — |
| `nss-activity-log` drawer — `[Save & Verify]` | Visible | — | — | — |
| `nss-unit-create` drawer | Accessible | Inaccessible (403 if direct URL) | — | — |
| Section 5.3 table | Visible | Visible | — | — |
| Alert banners | All visible | All visible | — | — |
| KPI cards | All 6 visible | All 6 visible | — | — |
| Export volunteer PII (names, roll no) | Included | Excluded | — | — |

---

## 12. API Endpoints

All endpoints under `/api/nss/`. Authentication: session cookie + CSRF token. Role enforcement: Django view-level decorator.

| Method | Endpoint | Description | Role Required | Response |
|---|---|---|---|---|
| GET | `/api/nss/units/?ay={ay}&branch={ids}&has_unit={bool}&hours_tier={tier}&search={q}&page={n}` | Paginated branch NSS unit summary for Section 5.1 | 99, 100 | `{results: [...], count, next, previous}` |
| POST | `/api/nss/units/create/` | Register a new NSS unit | 100 | `{id, unit_code, branch, ...}` |
| GET | `/api/nss/units/{id}/` | Single unit detail | 99, 100 | Unit object |
| PATCH | `/api/nss/units/{id}/update/` | Update unit metadata | 100 | Updated unit object |
| GET | `/api/nss/units/by-branch/?branch={id}` | Fetch unit code + officer for Branch select in drawer | 100 | `{unit_code, officer_name}` or `{error: "no_unit"}` |
| GET | `/api/nss/activities/?ay={ay}&branch={ids}&status={s}&date_from={d}&date_to={d}&page={n}` | Recent activities for Section 5.2 | 99, 100 | Paginated activity list |
| POST | `/api/nss/activities/create/` | Log a new NSS activity | 100 | Created activity object |
| GET | `/api/nss/activities/{id}/` | Single activity detail | 99, 100 | Activity object |
| POST | `/api/nss/activities/{id}/verify/` | Verify an activity | 100 | `{status: "verified"}` |
| POST | `/api/nss/activities/{id}/reject/` | Reject an activity with reason | 100 | `{status: "rejected"}` |
| GET | `/api/nss/volunteers/?unit={id}&page={n}` | Enrolled volunteers for a unit (drawer) | 99, 100 | Paginated volunteer list |
| GET | `/api/nss/volunteers/{id}/hours-log/?ay={ay}` | Volunteer's activity-hour log | 99, 100 | List of log entries |
| GET | `/api/nss/hours-distribution/?ay={ay}` | Branch-level 240h tracker for Section 5.3 | 99, 100 | `[{branch, enrolled, tier_240, tier_200, tier_100, tier_low, pct}]` |
| GET | `/api/nss/kpi/?ay={ay}` | All 6 KPI card values | 99, 100 | `{total_volunteers, active_units, achievers, activities_month, special_camp_rate, no_unit_count}` |
| GET | `/api/nss/charts/monthly-activity-count/?ay={ay}&months=6` | Data for Chart 7.1 | 99, 100 | `[{month, count}]` |
| GET | `/api/nss/charts/hours-distribution/?ay={ay}` | Data for Chart 7.2 | 99, 100 | `[{tier, count}]` |
| GET | `/api/nss/export/?ay={ay}&format={xlsx\|pdf}&branch={ids}` | Export NSS summary | 99, 100 | Binary file download |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | `hx-get` / `hx-post` | `hx-target` | `hx-swap` | Notes |
|---|---|---|---|---|---|
| KPI card load | Each card container | `GET /api/nss/kpi/?ay={ay}` (per-card variant) | `#kpi-{card-id}` | `innerHTML` | `hx-trigger="load"` on each card |
| AY selector change refresh | `<select name="ay">` | `GET /api/nss/kpi/?ay={ay}` | Multiple targets via `hx-swap-oob="true"` | `outerHTML` | Refreshes KPI bar + all tables |
| Unit summary table load | `#unit-summary-table-body` | `GET /api/nss/units/` | `#unit-summary-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search input | `<input name="search">` in Section 5.1 | `GET /api/nss/units/?search={q}` | `#unit-summary-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:400ms"` |
| Filter drawer apply | `[Apply Filters]` button | `GET /api/nss/units/?{params}` | `#unit-summary-table-body` | `innerHTML` | Closes drawer after response |
| Section 5.1 pagination | Page number links | `GET /api/nss/units/?page={n}` | `#unit-summary-table-body` | `innerHTML` | |
| Section 5.2 table load | `#recent-activities-body` | `GET /api/nss/activities/?days=30` | `#recent-activities-body` | `innerHTML` | `hx-trigger="load"` |
| Activity verify | "Verify" button per row | `POST /api/nss/activities/{id}/verify/` | `#activity-row-{id}` | `outerHTML` | Swaps entire row with updated status |
| Activity reject | "Reject" button per row | `POST /api/nss/activities/{id}/reject/` | `#activity-row-{id}` | `outerHTML` | Inline reason input before post |
| Branch select in drawer (auto-fill) | `<select name="branch">` | `GET /api/nss/units/by-branch/?branch={id}` | `#drawer-unit-code, #drawer-officer` | `innerHTML` | `hx-trigger="change"` |
| Drawer open — volunteer list | "View Volunteers" link | `GET /api/nss/volunteers/?unit={id}` | `#drawer-volunteer-body` | `innerHTML` | Drawer slides open; data loaded on trigger |
| Drawer tab switch — Hours Progress | Tab 2 click | `GET /api/nss/volunteers/?unit={id}&sort=hours_desc` | `#drawer-tab-hours-body` | `innerHTML` | `hx-trigger="click"` on tab |
| Volunteer hours log modal | "View Hours Log" link | `GET /api/nss/volunteers/{id}/hours-log/` | `#modal-hours-body` | `innerHTML` | Modal opens; spinner shown until response |
| Chart 7.1 load | `#chart-monthly-activity` | `GET /api/nss/charts/monthly-activity-count/` | `#chart-monthly-activity` | `innerHTML` | Response is `<canvas>` + Chart.js init script |
| Chart 7.2 load | `#chart-hours-donut` | `GET /api/nss/charts/hours-distribution/` | `#chart-hours-donut` | `innerHTML` | Response is `<canvas>` + Chart.js init script |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
