# 24 — Staff Exit & Offboarding Manager

- **URL:** `/group/hr/exit/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Staff Exit & Offboarding Manager governs the structured departure process for every staff member leaving the group, regardless of the reason. A poorly managed exit is one of the most common sources of institutional harm: unrevoked system access leads to data breaches, unreturned assets (keys, laptops, ID cards) create security gaps, unhandled student record transitions disrupt academic continuity, and unpaid final settlements create labour disputes. This page exists to ensure that every exit, from resignation to retirement, is tracked through a complete clearance and settlement process.

The exit types handled here are: voluntary resignation, involuntary termination (with cause, post disciplinary process), retirement (age or VRS), end of fixed-term or visiting contract, and absconding (staff who abandon their post without serving notice). Each exit type carries different procedural requirements. A voluntary resignation requires a formal acceptance letter, notice period tracking, and exit interview. A termination follows from the disciplinary process (page 11) and requires HR Director approval before the exit record is created. Absconding is flagged separately because absconding staff do not receive a formal experience letter, and their final settlement is adjusted per the employment contract terms.

The notice period is enforced as a system-level constraint: teachers must give 30 days' notice, non-teaching staff 15 days. If a staff member attempts to exit before serving their full notice (short-notice exit), the system flags it and prompts the HR Manager to either waive the notice or deduct the equivalent salary. Notice period buy-out (paying salary in lieu of notice) is also handled here with a specific field in the exit record.

The clearance checklist is as important as the onboarding checklist in reverse. Before final settlement is processed, the system requires confirmation of: system access revocation (IT clearance), ID card return, student records and attendance registers handed over, physical keys returned (hostel, classroom, staff room), library clearance (no pending books), accounts clearance (no pending advances or dues), and all assets listed in the staff's asset register returned. Only when all mandatory clearance items are marked complete does the system unlock the "Initiate Final Settlement" action.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access + termination approval | Must approve involuntary termination exits |
| Group HR Manager (42) | G3 | Full CRUD | Primary owner of exit management |
| Group Recruiter — Teaching (43) | G0 | No access | — |
| Group Recruiter — Non-Teaching (44) | G0 | No access | — |
| Group Training & Dev Manager (45) | G2 | No access | — |
| Group Performance Review Officer (46) | G1 | No access | — |
| Group Staff Transfer Coordinator (47) | G3 | Read-only | Can view exits for planning context |
| Group BGV Manager (48) | G3 | No access | — |
| Group BGV Executive (49) | G3 | No access | — |
| Group POCSO Coordinator (50) | G3 | No access | — |
| Group Disciplinary Committee Head (51) | G3 | Read-only | Can view termination exits linked to disciplinary action |
| Group Employee Welfare Officer (52) | G3 | Read-only | Can view final settlement and welfare benefit info |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Exit & Offboarding → Staff Exit Manager`

### 3.2 Page Header
- Title: "Staff Exit & Offboarding Manager"
- Subtitle: "Manage staff exits, clearance, and final settlement across all branches."
- Primary CTA: "+ Initiate Exit"
- Secondary CTAs: "Export Exit Report" | "View Absconding Records"

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Clearance overdue (any item > 7 days past last working day) | "[N] exit(s) have overdue clearance items. System access may still be active." | Red |
| Staff system access not revoked after last working day | "[N] exited staff still have active system accounts. IT clearance required immediately." | Red |
| Final settlement pending > 30 days | "[N] final settlement(s) have been pending for over 30 days." | Orange |
| Exit interviews not completed for resigned staff | "[N] resigned staff have not completed exit interviews." | Yellow |
| Absconding staff marked Active in system | "[N] absconding staff are still marked Active. Update status immediately." | Orange |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Exits in Progress | Count with exit status = In Progress (clearance ongoing) | Neutral blue | Filters to in-progress |
| Clearance Overdue | Count with ≥ 1 clearance item past due | Red if > 0 | Filters to overdue clearance |
| Final Settlement Pending | Count with clearance complete but settlement not processed | Orange if > 0 | Filters to settlement pending |
| Notice Period Running | Count currently serving notice period | Amber | Filters to notice period |
| Exit Interviews Completed | Count with exit interview done (this month) | Green | — |
| Turnover Rate This Month | (Exits this month / Total active staff) × 100 % | Red if > 5%, Green if < 2% | Opens export/detail view |

---

## 5. Main Table — Staff Exits

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text (link to exit record drawer) | Yes | Yes (search) |
| Branch | Text | Yes | Yes (dropdown) |
| Role | Text | Yes | Yes (search) |
| Exit Type | Chip (Resignation / Termination / Retirement / Contract End / Absconding) | Yes | Yes |
| Last Working Date | Date | Yes | Yes (date range) |
| Notice Period End | Date / "Waived" / "N/A" | No | No |
| Clearance % | Progress bar + percentage | Yes | Yes (< 100% filter) |
| Exit Interview Status | Chip (Pending / Scheduled / Completed / Waived) | No | Yes |
| Final Settlement | Chip (Pending / Processed / N/A) | No | Yes |
| Actions | View / Edit / Clearance Checklist / Generate Experience Letter | No | No |

### 5.1 Filters
- Exit Type: All | Resignation | Termination | Retirement | Contract End | Absconding
- Clearance Status: All | Complete | In Progress | Overdue
- Final Settlement: All | Pending | Processed
- Exit Interview: All | Pending | Completed | Waived
- Branch: All branches (dropdown)
- Date Range: This Month | Last 30 Days | Last 90 Days | Custom

### 5.2 Search
Search by staff name or employee ID. Minimum 2 characters, 400ms debounce.

### 5.3 Pagination
Server-side pagination, 20 records per page. Standard navigation with total exit count shown.

---

## 6. Drawers

### 6.1 Drawer: Initiate Exit
Fields: Staff Member (typeahead — searches active staff), Exit Type (dropdown), Resignation Date / Termination Date (date picker), Last Working Date (auto-calculated from notice period; overridable with reason), Exit Reason (text — for HR records, not shown in experience letter), Notice Period (pre-filled from contract — 30 days / 15 days), Notice Buy-Out (checkbox — if checked: salary deduction amount field), Exit Interview Scheduled Date (date picker), Special Notes (textarea).
Absconding-specific: Absconding Date, Last Known Location (optional), Police Report Filed (checkbox).
On Save: exit record created, clearance checklist auto-generated, staff status updated to "Exiting", IT clearance notification sent.

### 6.2 Drawer: View / Edit Exit Record
All fields from initiation, plus clearance checklist status. Edit available while exit is In Progress. Cannot edit Last Working Date after clearance checklist is marked 100% complete.

### 6.3 Drawer: Clearance Checklist
Categories and items: System Access (Portal / Email / Biometric Deactivated), Physical Assets (ID Card Returned / Keys Returned / Laptop/Tablet Returned), Academic Handover (Student Records Transferred / Attendance Register Submitted / Lesson Plan Archive Submitted), Financial Clearance (Salary Account Settled / Advances Cleared / Library Dues Cleared), Exit Interview (Completed / Waived with reason).
Each item: Status (Pending / Cleared), Cleared By (username), Cleared On (date), Notes. HR Manager marks each item. "Initiate Final Settlement" button becomes active only when all mandatory items are Cleared.

### 6.4 Drawer: Generate Experience Letter
Available once final settlement is processed. Template auto-fills: staff name, role, branch, date of joining, last working date, and a standard conduct description. HR Manager can add custom achievements paragraph. Preview PDF before finalising. On Save: PDF generated and linked to staff profile.

### 6.5 Modal: Mark as Absconding
Triggered separately for staff who have abandoned their post. Confirmation prompt with last seen date, notice waiver note, and experience letter withholding acknowledgement. On Confirm: exit record created with type = Absconding.

---

## 7. Charts

**Monthly Exit Trend — Bar Chart:** X-axis = last 6 months, Y-axis = count of exits. Stacked by exit type (Resignation / Termination / Contract End / Retirement / Absconding). Rendered via Chart.js. Toggle: "Show Trend / Hide". Below KPI bar.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exit record initiated | "Exit initiated for [Staff Name]. Clearance checklist created." | Success | 5s |
| Clearance item marked cleared | "[Item] cleared for [Staff Name]." | Success | 4s |
| All clearance complete — settlement unlocked | "All clearance items complete. Final settlement can now be initiated." | Success | 5s |
| Final settlement processed | "Final settlement processed for [Staff Name]." | Success | 4s |
| Experience letter generated | "Experience letter generated for [Staff Name]." | Success | 4s |
| System access revocation notified | "IT clearance request sent for [Staff Name]." | Info | 4s |
| Absconding recorded | "[Staff Name] marked as absconding. Experience letter withheld." | Warning | 5s |
| Notice waiver recorded | "Notice period waived for [Staff Name]. Salary adjustment noted." | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No active exits | "No Exits in Progress" | "Active staff exits will appear here once initiated." | Initiate Exit |
| Filter returns no results | "No Matching Exit Records" | "Adjust your filters to find the exit record." | Clear Filters |
| Clearance all complete | "All Clearances Up to Date" | "No overdue clearance items. All exits progressing on schedule." | — |
| No exits this month | "No Exits This Month" | "No staff departures have been recorded this month." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI card skeletons (6) + table row skeletons (15) |
| Filter change | Table body row skeletons |
| Exit initiation drawer | Form field skeletons |
| Clearance checklist drawer | Checklist item skeletons (per category) |
| Experience letter generation | Spinner + "Generating…" button text |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) | HR Manager (42) | Read-Only Roles (47, 51, 52) |
|---|---|---|---|
| Initiate Exit button | Visible | Visible + enabled | Hidden |
| Termination exit type | Visible (approval required) | Creates pending Director approval | Hidden |
| Edit exit record | Visible | Visible | Hidden |
| Clearance checklist editing | Visible | Visible | Visible (read-only) |
| Initiate Final Settlement | Visible | Visible (when clearance complete) | Hidden |
| Generate Experience Letter | Visible | Visible | Hidden |
| Mark Absconding | Visible | Visible | Hidden |
| Turnover rate KPI | Visible | Visible | Visible (read-only) |
| Export Report | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/exit/` | JWT | List all exit records (paginated) |
| POST | `/api/v1/hr/exit/` | JWT | Initiate exit for staff member |
| GET | `/api/v1/hr/exit/{id}/` | JWT | Fetch exit record detail |
| PATCH | `/api/v1/hr/exit/{id}/` | JWT | Update exit record |
| GET | `/api/v1/hr/exit/{id}/clearance/` | JWT | Fetch clearance checklist |
| PATCH | `/api/v1/hr/exit/{id}/clearance/{item_id}/` | JWT | Update clearance item status |
| POST | `/api/v1/hr/exit/{id}/settlement/` | JWT | Initiate final settlement |
| POST | `/api/v1/hr/exit/{id}/experience-letter/` | JWT | Generate experience letter |
| PATCH | `/api/v1/hr/exit/{id}/abscond/` | JWT | Mark staff as absconding |
| GET | `/api/v1/hr/exit/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/exit/chart/` | JWT | Monthly exit trend chart data |
| GET | `/api/v1/hr/exit/export/` | JWT | Export exit report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/exit/?q={val}` | `#exit-table-body` | innerHTML |
| Filter apply | change | GET `/api/v1/hr/exit/?type={}&clearance={}&branch={}` | `#exit-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/exit/?page={n}` | `#exit-table-body` | innerHTML |
| Initiate Exit drawer open | click | GET `/group/hr/exit/initiate/drawer/` | `#drawer-container` | innerHTML |
| View/Edit drawer open | click | GET `/group/hr/exit/{id}/drawer/` | `#drawer-container` | innerHTML |
| Clearance checklist drawer | click | GET `/group/hr/exit/{id}/clearance/drawer/` | `#drawer-container` | innerHTML |
| Clearance item update | change | PATCH `/api/v1/hr/exit/{id}/clearance/{item_id}/` | `#clearance-item-{item_id}` | outerHTML |
| Final settlement initiate | click | POST `/api/v1/hr/exit/{id}/settlement/` | `#exit-row-{id}` | outerHTML |
| Experience letter drawer | click | GET `/group/hr/exit/{id}/experience-letter/drawer/` | `#drawer-container` | innerHTML |
| Chart toggle | click | GET `/group/hr/exit/chart/` | `#chart-container` | innerHTML |
| KPI refresh after clearance | after:PATCH | GET `/api/v1/hr/exit/kpis/` | `#kpi-bar` | outerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
