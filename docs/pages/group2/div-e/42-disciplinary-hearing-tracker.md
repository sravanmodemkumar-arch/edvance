# 42 — Disciplinary Hearing Tracker

- **URL:** `/group/hr/disciplinary/hearings/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Disciplinary Committee Head (Role 51, G3)

---

## 1. Purpose

The Disciplinary Hearing Tracker manages the scheduling, conduct, and outcome recording of formal disciplinary hearings for cases that have progressed beyond the Show-Cause Notice (SCN) stage. Once a staff member's SCN response is deemed unsatisfactory — or when no response is received within the stipulated period — the Disciplinary Committee Head initiates the hearing process by constituting an Enquiry Committee. This page is the central control surface for all hearing activity across the group.

A valid Enquiry Committee must comprise at least three members: the Disciplinary Committee Head (who chairs proceedings), one neutral Head of Department from a branch unrelated to the case, and one representative from Group HR. For cases involving POCSO-related charges, an external member from the District Legal Services Authority (DLSA) is mandatory — the system flags these cases distinctly and prevents hearing scheduling until the external member is confirmed. The accused staff member must be notified at least seven calendar days before the first hearing, and a copy of the charges must be served along with the notice.

Hearings are categorised as First Hearing (initial presentation of charges and response), Adjourned Hearing (continuation from a prior session where proceedings were incomplete), or Final Hearing (closing arguments and committee deliberation). The committee must record all proceedings in writing. The written hearing report — detailing charges, evidence, staff response, and committee findings — must be submitted within 15 days of the final hearing. Delays in report submission represent compliance risk and are surfaced on this page.

The page provides full lifecycle management: scheduling hearings, tracking committee composition, recording minutes, logging outcomes, and monitoring report submission. It also flags hearings that have not been held within 30 days of the SCN being issued — a procedural lapse that can weaken the institution's position in any subsequent appeal. The tracker is accessible to the Group Disciplinary Committee Head (full operations) and to the Group HR Director (read-only oversight). All actions are audit-logged.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Disciplinary Committee Head | G3 | Full CRUD + Schedule + Record | Primary operator of this page |
| Group HR Director | G3 | Read-only + Export | Oversight and compliance monitoring |
| Group HR Manager | G3 | Read-only | Coordination support |
| Group POCSO Coordinator | G3 | Read-only (POCSO cases only) | Filtered view for POCSO-flagged hearings |
| Branch Principal | G3 | Read-only (own branch cases only) | Row-level filter by branch |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › Disciplinary › Hearings
```

### 3.2 Page Header

- **Title:** Disciplinary Hearing Tracker
- **Subtitle:** Schedule, conduct, and close formal hearings across all branches
- **Primary CTA:** `+ Schedule Hearing` (Disciplinary Committee Head only)
- **Secondary CTA:** `Export` (CSV/PDF dropdown)
- **Header meta:** Current open hearings count shown as badge; last sync timestamp

### 3.3 Alert Banner (conditional)

- **Red:** One or more hearings are past due — not held within 30 days of SCN issuance. Lists case IDs. Action: `Review Now`
- **Amber:** Hearing reports pending submission past 15-day deadline. Lists hearing IDs.
- **Blue:** POCSO-linked hearings awaiting DLSA external member confirmation. Action: `Confirm Members`
- **Green:** All hearings within SLA — shown only when no active alerts exist

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Hearings Scheduled This Week | Count of hearings with scheduled date in current ISO week | Blue always | Filter table to this week's schedule |
| Hearings Pending Committee Formation | Count where committee_confirmed = false | Amber if > 0, else grey | Filter to unconfirmed committee rows |
| Hearings Past Due (>30 days from SCN) | Count where (today − scn_issued_date) > 30 and hearing_status ≠ Completed | Red if > 0, else green | Filter to overdue rows |
| POCSO Hearings — External Member Required | Count of POCSO-flagged hearings | Red if external_member_confirmed = false, blue otherwise | Filter to POCSO rows |
| Reports Pending Submission | Count where final_hearing_completed = true and report_submitted = false | Amber if > 0, else grey | Filter to report-pending rows |
| Cases Closed Post-Hearing | Count of hearings with outcome_recorded = true in last 30 days | Green always | Filter to closed cases |

---

## 5. Main Table — Hearings Register

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Hearing ID | Text (auto-generated, e.g., HRG-2526-0041) | No | No |
| Case ID | Text (linked to Disciplinary Case Tracker, page 40) | No | Yes — text search |
| Staff Name | Text | Yes (A–Z) | Yes — text search |
| Branch | Text | Yes | Yes — dropdown |
| Hearing Type | Badge (First / Adjourned / Final) | No | Yes — checkbox group |
| Committee Members | Count badge + tooltip listing names | No | No |
| Scheduled Date | Date | Yes | Yes — date range picker |
| Status | Badge (Scheduled / In Progress / Completed / Adjourned / Cancelled) | No | Yes — checkbox group |
| Report Submitted | Boolean badge (Yes / No / N/A) | No | Yes — Yes/No toggle |
| Outcome Pending | Boolean badge (Yes / No) | No | Yes — Yes/No toggle |
| Actions | Icon buttons: View / Edit / Record Minutes / Record Outcome | No | No |

### 5.1 Filters

- **Branch:** Multi-select dropdown populated from enrolled branches
- **Hearing Type:** Checkboxes — First Hearing, Adjourned Hearing, Final Hearing
- **Status:** Checkboxes — Scheduled, In Progress, Completed, Adjourned, Cancelled
- **POCSO Case:** Toggle — Yes / All
- **Report Submitted:** Toggle — Yes / No / All
- **Scheduled Date Range:** From / To date picker
- **Past Due Only:** Checkbox — shows only hearings past 30-day SCN window
- **Reset Filters** button clears all to default

### 5.2 Search

Global search bar searches across: Hearing ID, Case ID, Staff Name. Minimum 2 characters to trigger; results highlighted in yellow.

### 5.3 Pagination

Server-side pagination. Default 20 rows per page. Options: 10, 20, 50. Pagination controls: First / Previous / Page X of Y / Next / Last. Row count shown: "Showing 1–20 of 47 hearings."

---

## 6. Drawers

### 6.1 Schedule Hearing (Create)

Triggered by `+ Schedule Hearing` button. Slide-in drawer from right.

**Fields:**
- Case ID (searchable dropdown — pulls from open disciplinary cases past SCN stage)
- Staff Name (auto-filled from Case ID)
- Branch (auto-filled from Case ID)
- Hearing Type (dropdown: First Hearing / Adjourned Hearing / Final Hearing)
- Scheduled Date (date picker — must be at least 7 days from today for staff notification compliance)
- Scheduled Time (time picker)
- Venue (text input + Online toggle)
- Committee Member 1 — Disciplinary Committee Head (auto-filled, locked)
- Committee Member 2 — Neutral HOD (searchable staff dropdown, must be from different branch)
- Committee Member 3 — HR Representative (searchable staff dropdown, HR role required)
- External Member (DLSA) — shown only if case is POCSO-flagged; required field in that scenario
- Staff Notification Date (date — auto-suggested as scheduled_date − 7 days)
- Remarks (textarea, optional)

**Validation:**
- If POCSO-flagged, external member field is mandatory
- Scheduled date must be ≥ 7 days from today
- All three committee members must be distinct individuals
- Case must be in "SCN Reviewed" or "Hearing Required" status

**Submit:** `Schedule Hearing` button → POST `/api/hr/disciplinary/hearings/` → Refreshes table via HTMX

### 6.2 View Case File

Triggered by eye icon in Actions column. Full-width side drawer.

**Displays:**
- Case ID, Staff Name, Branch, Designation
- Original charge sheet summary
- SCN issued date and staff response summary
- All prior hearings in this case (list with dates and outcomes)
- Current hearing details
- Committee members confirmed
- Attendance record for prior hearings
- Documents attached to case (charge sheet, SCN copy, response, prior minutes)

**Actions available from this drawer:** Download Case File (PDF), Proceed to Record Minutes

### 6.3 Record Hearing Minutes (Edit)

Triggered from Actions column or from View Case File drawer.

**Fields:**
- Hearing ID (locked, auto-filled)
- Hearing Date (date — defaults to scheduled date, editable if rescheduled)
- Actual Start Time / End Time
- Attendance: Present / Absent for each committee member and accused staff
- Staff Brought Colleague Witness: Yes / No; if Yes → colleague name
- Proceedings Summary (rich textarea — minimum 100 characters required)
- Evidence Presented (textarea)
- Staff Response During Hearing (textarea)
- Adjournment Required: Yes / No; if Yes → reason and next date
- Hearing Status (auto-set: Completed or Adjourned based on adjournment field)
- Uploaded Minutes Document (file upload, PDF only, max 5 MB)

**Submit:** `Save Minutes` → PATCH `/api/hr/disciplinary/hearings/{id}/minutes/`

### 6.4 Record Outcome

Enabled only after Final Hearing minutes are saved.

**Fields:**
- Hearing ID (locked)
- Committee Recommendation (dropdown: Warning / Suspension / Demotion / Termination / Exonerated / Referred for Further Inquiry)
- Recommendation Justification (textarea, minimum 150 characters)
- Report Submission Date (date — must be within 15 days of final hearing date)
- Upload Final Report (PDF, required, max 10 MB)
- Outcome Pending Management Decision: Yes / No

**Submit:** `Record Outcome` → PATCH `/api/hr/disciplinary/hearings/{id}/outcome/`

---

## 7. Charts

No dedicated charts section on this page. Visual data for disciplinary trends is consolidated in the HR Analytics Dashboard (page 47). This page is purely operational.

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Hearing scheduled successfully | Success | "Hearing HRG-XXXX scheduled for [date]. Staff notification due by [date−7]." |
| Minutes saved | Success | "Hearing minutes recorded for HRG-XXXX." |
| Outcome recorded | Success | "Outcome recorded. Case status updated to Closed Pending Approval." |
| POCSO external member missing | Error | "External DLSA member is required for POCSO-linked hearings." |
| Scheduled date too soon | Warning | "Scheduled date must be at least 7 days from today for staff notice compliance." |
| Save failed — server error | Error | "Failed to save. Please try again or contact system support." |
| Report submission overdue | Warning | "Report for HRG-XXXX is overdue. Submission deadline was [date]." |

---

## 9. Empty States

**No hearings in table:**
> Icon: calendar with gavel
> "No hearings have been scheduled yet."
> "Use '+ Schedule Hearing' to schedule the first formal hearing for a pending disciplinary case."
> CTA: `+ Schedule Hearing`

**Filtered results return nothing:**
> Icon: magnifying glass
> "No hearings match your current filters."
> CTA: `Reset Filters`

---

## 10. Loader States

- Page initial load: Full-width skeleton rows (5 rows × all columns) shown while API fetches
- Drawer open: Spinner centred in drawer while case details load
- Table refresh after action: Skeleton overlay on table body; header and filters remain visible
- KPI cards: Individual card shimmer while metrics compute

---

## 11. Role-Based UI Visibility

| UI Element | Disciplinary Committee Head | HR Director | POCSO Coordinator | Branch Principal |
|---|---|---|---|---|
| `+ Schedule Hearing` button | Visible | Hidden | Hidden | Hidden |
| Record Minutes action | Visible | Hidden | Hidden | Hidden |
| Record Outcome action | Visible | Hidden | Hidden | Hidden |
| Export button | Visible | Visible | Hidden | Hidden |
| POCSO filter | Visible | Visible | Auto-applied (POCSO only) | Hidden |
| Full case file view | Visible | Visible | Visible (POCSO cases) | Visible (own branch) |
| Delete/Cancel hearing | Visible | Hidden | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/disciplinary/hearings/` | Paginated list with filters |
| POST | `/api/hr/disciplinary/hearings/` | Schedule new hearing |
| GET | `/api/hr/disciplinary/hearings/{id}/` | Fetch single hearing details |
| PATCH | `/api/hr/disciplinary/hearings/{id}/` | Update hearing metadata |
| PATCH | `/api/hr/disciplinary/hearings/{id}/minutes/` | Save recorded minutes |
| PATCH | `/api/hr/disciplinary/hearings/{id}/outcome/` | Record final outcome |
| GET | `/api/hr/disciplinary/hearings/kpis/` | KPI summary bar data |
| GET | `/api/hr/disciplinary/cases/` | Open cases eligible for hearing (dropdown source) |
| DELETE | `/api/hr/disciplinary/hearings/{id}/` | Cancel hearing (soft delete) |

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| Table load | `hx-get` on page load | Fetches `/api/hr/disciplinary/hearings/` and renders rows |
| Filter change | `hx-get` on `change` event with `hx-include` for all filter inputs | Re-fetches table with updated query params |
| Pagination | `hx-get` on page buttons | Fetches specified page and swaps table body |
| Search input | `hx-get` with `hx-trigger="keyup changed delay:400ms"` | Debounced live search |
| Drawer open | `hx-get` + `hx-target="#drawer-container"` | Loads drawer HTML into right-panel container |
| Form submit (schedule) | `hx-post` with `hx-target="#table-body"` | Posts form, gets updated table HTML on success |
| Form submit (minutes/outcome) | `hx-patch` with `hx-target="#hearing-row-{id}"` | Updates individual row in place |
| Toast | `hx-swap-oob="true"` on `#toast-container` | Out-of-band swap injects toast notification |
| KPI refresh | `hx-get` on `#kpi-bar` after any mutation | Refreshes KPI figures after create/update |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
