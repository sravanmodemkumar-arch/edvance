# 44 — Employee Welfare Events

- **URL:** `/group/hr/welfare/events/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Employee Welfare Officer (Role 52, G3)

---

## 1. Purpose

The Employee Welfare Events page manages the planning, execution, and reporting of welfare initiatives and events for staff across all branches in the group. Staff welfare is a deliberate institutional investment — organisations with structured welfare programmes consistently report higher retention, lower absenteeism, and better staff morale. This page gives the Group Employee Welfare Officer a single control surface to create welfare events, invite branches, track participation, and reconcile spend against the welfare budget.

Welfare events covered include: Staff Health Camps (basic medical screening — blood pressure, blood sugar, BMI, eye checkup — conducted by empanelled healthcare providers), Annual Staff Sports Day (cross-branch or branch-wise athletic and recreational competition), Teacher Appreciation Events (recognition ceremonies, awards, certificates of excellence), Staff Anniversary Recognition (service milestone recognition — 5, 10, 15, 20+ years), Mental Health Awareness Workshops (counsellor-led sessions on stress, burnout, and work-life balance), Staff Family Day (event where staff families are invited to the campus), and Emergency Financial Aid disbursement events (one-time hardship fund grants for staff facing personal financial crisis — medical emergency, natural disaster, bereavement).

Each event has a designated branch scope (single branch, selected branches, or all branches), a budget allocation, a welfare officer as owner, and participation data by branch. After the event, the Welfare Officer logs actual participation numbers and actual spend. Budget utilisation and participation coverage are the two primary measures of welfare programme effectiveness. Welfare events data feeds the annual welfare report submitted to the HR Director and Board.

The page also serves a planning function: the Welfare Officer can view upcoming events in a calendar view, identify branches that have had no welfare events in the last quarter, and flag branches at risk of welfare neglect. Staff welfare investment has a direct correlation with staff retention rates — this connection is surfaced in the HR Analytics Dashboard (page 47) using data generated from this page.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Employee Welfare Officer | G3 | Full CRUD + Publish + Budget | Primary operator |
| Group HR Director | G3 | Read-only + Export | Oversight and budget approval |
| Group HR Manager | G3 | Read-only | Coordination support |
| Branch Principal | G3 | Read-only (own branch events only) | Cannot create or edit events |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › Employee Welfare › Events
```

### 3.2 Page Header

- **Title:** Employee Welfare Events
- **Subtitle:** Plan, track, and report welfare initiatives across all branches
- **View Toggle:** Table View (default) / Calendar View (month grid)
- **Primary CTA:** `+ Create Event` (Welfare Officer only)
- **Secondary CTA:** `Export` (CSV/PDF)
- **Header badge:** Events scheduled in current month shown as count chip

### 3.3 Alert Banner (conditional)

- **Amber:** `[N] branches have had no welfare events in the last 90 days.` Action: `View Branches`
- **Amber:** `[N] events are upcoming this week with no participant list confirmed.` Action: `Review`
- **Red:** `Welfare budget for [Quarter] is 90% utilised.` Action: `View Budget`
- **Blue:** `[N] emergency aid disbursements pending approval this week.`
- **Green:** All branches covered and budget within normal range — shown when no active alerts

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Events This Quarter | Count of events with date in current academic quarter | Blue always | Filter table to current quarter |
| Total Staff Participated | Sum of participant_count across all completed events this academic year | Green always | No drill-down |
| Branches Covered | Count of distinct branches with ≥ 1 completed event this quarter | Amber if < total_branches × 0.75, else green | Filter to covered branches |
| Welfare Budget Utilised (₹) | Sum of actual_spend; shown as ₹X of ₹Y budget (progress bar) | Green if ≤ 80%, amber 81–90%, red > 90% | Open budget breakdown view |
| Health Camp Beneficiaries | Sum of participants for events of type Health Camp this academic year | Blue always | Filter to health camp events |
| Emergency Aid Cases This Month | Count of Emergency Financial Aid events with disbursement in current month | Amber if > 0, blue if 0 | Filter to aid events |

---

## 5. Main Table — Welfare Events Register

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Event Name | Text (link — opens View drawer) | Yes (A–Z) | Yes — text search |
| Type | Badge (Health Camp / Sports Day / Appreciation / Anniversary / Mental Health / Family Day / Emergency Aid) | No | Yes — checkbox group |
| Date | Date | Yes | Yes — date range |
| Branches | Count badge + tooltip (e.g., "4 branches") | No | Yes — branch dropdown |
| Venue / Online | Text + Online chip if virtual | No | No |
| Budget (₹) | Numeric, right-aligned | Yes | No |
| Participants | Numeric (actual vs. target if post-event) | Yes | No |
| Completion Status | Badge (Planned / Confirmed / In Progress / Completed / Cancelled) | No | Yes — checkbox group |
| Welfare Officer | Text | No | Yes — dropdown |
| Actions | Icon buttons: View / Edit / Cancel / Mark Completed | No | No |

### 5.1 Filters

- **Event Type:** Checkboxes — all 7 event types
- **Branch:** Multi-select dropdown
- **Status:** Checkboxes — Planned, Confirmed, In Progress, Completed, Cancelled
- **Date Range:** From / To date picker
- **Quarter:** Dropdown — Q1, Q2, Q3, Q4 of current academic year
- **Budget Range:** Min / Max (₹) inputs
- **Reset Filters** button

### 5.2 Search

Text search on Event Name. 2-character minimum, 400 ms debounce.

### 5.3 Pagination

Server-side. Default 20 rows. Options: 10 / 20 / 50. "Showing X–Y of Z events."

---

## 6. Drawers

### 6.1 Create Event

Triggered by `+ Create Event`. Right slide-in drawer.

**Fields:**
- Event Name (text, max 100 characters)
- Event Type (dropdown — 7 types)
- Date (date picker)
- Time (time picker — start and end)
- Venue (text input)
- Online Event: toggle; if toggled → Meeting Link field appears
- Scope (radio: Single Branch / Selected Branches / All Branches)
  - If Single / Selected → branch multi-select appears
- Target Participants (numeric)
- Budget Allocated (₹, numeric)
- Welfare Officer (dropdown, defaults to current user)
- Description / Programme Details (textarea)
- External Vendor / Service Provider (text, optional — e.g., hospital name for health camp)
- Invitation / Circular Upload (PDF, optional, max 5 MB)

**Validation:** Date must be ≥ today; budget > 0; branch selection required for Single/Selected scope.

**Submit:** `Create Event` → POST `/api/hr/welfare/events/`

### 6.2 View Attendance

Triggered by attendance/eye icon on completed or in-progress events.

**Displays:**
- Event details (name, type, date, venue)
- Branch-wise participation breakdown (table: Branch / Target / Actual / Attendance %)
- Total participation summary
- Health camp: If health camp type → lists screening results summary (optional upload)
- Photos / Report upload section (post-event documentation)
- Actual spend logged vs. budget

**Actions:** Upload attendance report (CSV template download available), Update actual participants, Upload photos

### 6.3 Edit Event

Available for Planned and Confirmed status events. Not available for Completed or Cancelled.

**Fields:** Same as Create, all editable except Event Type (immutable after creation).

**Submit:** `Save Changes` → PATCH `/api/hr/welfare/events/{id}/`

### 6.4 Cancel Event

**Fields:**
- Event ID (locked)
- Cancellation Reason (textarea, min 50 characters)
- Notify Branches: checkbox (triggers notification to branch principals)
- Budget to Release: auto-calculated from budget_allocated − actual_spend_to_date

**Submit:** `Cancel Event` → PATCH `/api/hr/welfare/events/{id}/cancel/`

### 6.5 Mark Completed (Post-Event Reporting)

**Fields:**
- Event ID (locked)
- Completion Date (date — defaults to event date)
- Actual Participants (numeric, per branch if multi-branch)
- Actual Spend (₹, numeric)
- Spend Breakdown (textarea — optional line items)
- Outcome Summary (textarea, min 100 characters)
- Upload Event Report (PDF, optional)
- Upload Photos (images, optional, max 5 files × 5 MB each)

**Submit:** `Mark Completed` → PATCH `/api/hr/welfare/events/{id}/complete/`

---

## 7. Charts

Two charts displayed below the main table. Visible in Table View; hidden in Calendar View.

### Chart A — Welfare Events by Branch (Bar Chart)

- **Type:** Grouped vertical bar chart
- **X-axis:** Branch names
- **Y-axis:** Number of completed welfare events
- **Time filter:** Dropdown — This Quarter / This Academic Year
- **Bars:** Colour-coded by event type (stacked if stacked mode enabled)
- **Tooltip:** On hover shows branch name, event count, participant total
- **Export:** PNG button top-right of chart

### Chart B — Welfare Budget vs. Actual Spend (Line Chart)

- **Type:** Dual-line chart
- **X-axis:** Months (academic year)
- **Y-axis:** ₹ amount
- **Line 1:** Cumulative budget allocated (blue, dashed)
- **Line 2:** Cumulative actual spend (green solid)
- **Overspend zone:** Area shaded red where actual > budget
- **Tooltip:** Month, budgeted ₹, actual ₹, variance
- **Export:** PNG button

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Event created | Success | "Welfare event '[Name]' created and scheduled for [date]." |
| Event updated | Success | "Event '[Name]' updated successfully." |
| Event cancelled | Warning | "Event '[Name]' cancelled. Budget of ₹[amount] released." |
| Event marked complete | Success | "Event '[Name]' marked complete. Participation and spend recorded." |
| Attendance report uploaded | Success | "Attendance data uploaded for '[Name]'." |
| Budget threshold warning | Warning | "Welfare budget for this quarter is 90% utilised." |
| Server error | Error | "Failed to save. Please try again or contact support." |
| Validation error | Error | "Please complete all required fields before submitting." |

---

## 9. Empty States

**No events in table:**
> Icon: calendar with star
> "No welfare events have been scheduled yet."
> "Use '+ Create Event' to plan the first staff welfare activity."
> CTA: `+ Create Event`

**No events for current filter:**
> Icon: magnifying glass
> "No welfare events match your current filters."
> CTA: `Reset Filters`

**Calendar view — no events in selected month:**
> Icon: empty calendar
> "No events scheduled for [Month Year]."
> CTA: `+ Create Event`

---

## 10. Loader States

- Page load: Skeleton KPI cards + skeleton table (6 rows) shown simultaneously
- Chart load: Chart placeholder with pulsing outline; "Loading chart data..." text centred
- Drawer open: Spinner centred while event detail fetches
- Attendance view: Spinner while branch participation data loads
- Calendar view switch: Full calendar skeleton (grid of grey boxes) while events load

---

## 11. Role-Based UI Visibility

| UI Element | Welfare Officer | HR Director | HR Manager | Branch Principal |
|---|---|---|---|---|
| `+ Create Event` button | Visible | Hidden | Hidden | Hidden |
| Edit action | Visible | Hidden | Hidden | Hidden |
| Cancel action | Visible | Hidden | Hidden | Hidden |
| Mark Completed action | Visible | Hidden | Hidden | Hidden |
| Budget column and KPI | Visible | Visible | Hidden | Hidden |
| Export button | Visible | Visible | Hidden | Hidden |
| Branch filter (all branches) | Yes | Yes | Yes | Own branch only |
| Charts | Visible | Visible | Visible | Hidden |
| Emergency Aid events | Visible | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/welfare/events/` | Paginated list with filters |
| POST | `/api/hr/welfare/events/` | Create new welfare event |
| GET | `/api/hr/welfare/events/{id}/` | Single event detail |
| PATCH | `/api/hr/welfare/events/{id}/` | Edit event metadata |
| PATCH | `/api/hr/welfare/events/{id}/cancel/` | Cancel event |
| PATCH | `/api/hr/welfare/events/{id}/complete/` | Mark event completed with actuals |
| POST | `/api/hr/welfare/events/{id}/attendance/` | Upload attendance data |
| GET | `/api/hr/welfare/events/kpis/` | KPI summary bar data |
| GET | `/api/hr/welfare/events/charts/by-branch/` | Branch event chart data |
| GET | `/api/hr/welfare/events/charts/budget-vs-spend/` | Budget vs. spend chart data |

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| Table load | `hx-get` on page render | Fetches events list |
| Filter/search change | `hx-get` + `hx-include` on filter form | Re-fetches table with all active filters |
| View toggle (Table/Calendar) | `hx-get` on toggle buttons | Swaps `#main-content` between table and calendar template |
| Pagination | `hx-get` on page buttons | Fetches page N of results |
| Drawer open | `hx-get` + `hx-target="#drawer"` | Loads drawer for specific event ID |
| Create event form | `hx-post` + `hx-target="#table-body"` | Posts form, refreshes table on success |
| Cancel / Complete actions | `hx-patch` + `hx-target="#row-{id}"` | Updates single row in place |
| Chart load | `hx-get` on `#chart-container` on page load | Fetches chart data and renders via JS chart library |
| Attendance upload | `hx-post` with file data + `hx-target="#attendance-section"` | Uploads file and refreshes participation summary |
| Toast | `hx-swap-oob` on `#toast-container` | Injects toast on any successful mutation |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
