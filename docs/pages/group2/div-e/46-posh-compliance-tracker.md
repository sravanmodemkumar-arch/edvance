# 46 — POSH Compliance Tracker

- **URL:** `/group/hr/posh/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Director (Role 41, G3)

---

## 1. Purpose

The POSH Compliance Tracker ensures every branch in the group meets its statutory obligations under the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 — commonly referred to as the POSH Act. This legislation mandates that every organisation with ten or more employees must constitute an Internal Complaints Committee (ICC), display the POSH policy prominently in the workplace, conduct annual POSH awareness training for all staff, and submit an annual report to the District Officer by 31st January each year. Non-compliance carries criminal penalties for the employer and responsible officer.

The POSH Compliance Tracker is operated by the Group HR Director — who holds institutional accountability for POSH compliance across the group — and provides a branch-by-branch compliance dashboard. For each branch, the tracker records: whether an ICC has been constituted, the ICC constitution date, the ICC term expiry date (ICC terms are three years; reconstitution before expiry is mandatory), whether the POSH policy is posted in the branch, the last POSH training date, the count of complaints received in the current year, and the status of the annual report submission.

It is critical to note the distinction between POSH and POCSO: POSH governs workplace sexual harassment between adults (staff-to-staff), while POCSO governs child sexual abuse (staff or anyone toward a student). These are separate legal frameworks, separate processes, and separate pages in this system. A POSH complaint involves the ICC process — investigation by the committee, report to employer within 90 days, employer action within 60 days thereafter. POCSO complaints are handled on the POCSO Complaint Register page (page 38).

The page provides operational tools for the HR Director to register ICC members, record POSH training completions, log any complaints that arise, record outcomes, and confirm annual report submission to the District Officer. The system continuously monitors ICC term expiry across all branches and raises pre-emptive alerts when reconstitution is due. Any branch with an expired ICC or a missed annual report deadline is flagged with a red alert and appears at the top of the compliance table.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director | G3 | Full CRUD + Submit Report + Manage ICC | Primary operator |
| Group HR Manager | G3 | Read-only + Record Training | Operational support |
| Group POCSO Coordinator | G1 | Read-only | Contextual awareness only |
| Branch Principal | G3 | Read-only (own branch row only) | Cannot edit compliance data |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › POSH Compliance
```

### 3.2 Page Header

- **Title:** POSH Compliance Tracker
- **Subtitle:** Prevention of Sexual Harassment Act — branch-wise compliance register
- **Primary CTA:** `+ Register ICC` (add or update ICC for a branch)
- **Secondary CTA:** `Export Compliance Report` (PDF — formatted for regulatory submission)
- **Header badge:** Count of non-compliant branches shown in red; count of fully compliant branches shown in green

### 3.3 Alert Banner (conditional)

- **Red (hard block):** `[N] branches have expired ICC. This is a statutory violation. Reconstitute immediately.` Action: `View Branches`
- **Red (hard block):** `Annual POSH Report not submitted for [N] branches. Deadline: 31st January.` Action: `View Pending`
- **Amber:** `[N] branches have ICC expiring within 60 days. Schedule reconstitution.`
- **Amber:** `[N] branches have not completed POSH training in the last 12 months.`
- **Green:** All branches compliant — shown only when no active alerts exist

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Branches with ICC Constituted | Count where icc_status = Active, out of total branches | Red if < 100%, green if 100% | Filter table to ICC active rows |
| ICC Reconstitution Due | Count where icc_expiry_date within next 60 days or already expired | Red if any expired, amber if expiring soon, grey if none | Filter to due/expired rows |
| POSH Training Completed % | % of branches with last_training_date within last 12 months | Green if 100%, amber if 75–99%, red if < 75% | Filter to untrained branches |
| Complaints Received This Year | Total complaints across all branches in current calendar year | Amber if > 0, grey if 0 | Filter table to branches with complaints |
| Complaints Resolved | Count with outcome_recorded = true in current year | Green if all resolved, amber if any open | Filter to open complaints |
| Annual Report Submitted | Count of branches with annual_report_submitted = true for current year | Red if any missing by 31 Jan deadline, green if all submitted | Filter to missing report rows |

---

## 5. Main Table — Branch POSH Compliance Register

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text | Yes (A–Z) | Yes — text search |
| ICC Constitution Date | Date (or "Not Constituted" in red) | Yes | Yes — constituted/not toggle |
| ICC Expiry Date | Date + status chip (Active / Expiring Soon / Expired) | Yes | Yes — status dropdown |
| POSH Policy Posted | Boolean badge (Yes / No) | No | Yes — Yes/No toggle |
| Last Training Date | Date (or "Never") + recency chip | Yes | Yes — overdue toggle |
| Complaints This Year | Numeric (0 shown in grey, > 0 in amber) | Yes | No |
| Annual Report Status | Badge (Submitted / Not Submitted / Not Required) | No | Yes — status dropdown |
| Compliance Status | Badge (Compliant / Action Required / Non-Compliant) | No | Yes — dropdown |
| Actions | Icon buttons: View / Edit ICC / Record Training / Log Complaint / Submit Report | No | No |

### 5.1 Filters

- **Compliance Status:** Compliant / Action Required / Non-Compliant / All
- **ICC Status:** Active / Expiring Soon (< 60 days) / Expired / Not Constituted / All
- **Training Status:** Completed (within 12 months) / Overdue / Never / All
- **Annual Report:** Submitted / Not Submitted / All
- **Has Complaints:** Yes / No / All
- **Reset Filters** button

### 5.2 Search

Text search on Branch name. Min 2 characters, 400 ms debounce.

### 5.3 Pagination

Server-side. Default 20 rows per page. Options: 10 / 20 / 50. "Showing X–Y of Z branches."

---

## 6. Drawers

### 6.1 Register ICC Members (Create / Reconstitute)

Triggered by `+ Register ICC` or "Edit ICC" action in row.

**Fields:**
- Branch (dropdown — list of all branches)
- ICC Constitution Date (date picker)
- ICC Term Duration (locked to 36 months; expiry auto-calculated)
- ICC Presiding Officer: Name + Designation (searchable staff — must be senior woman employee)
- ICC Member 2: Name + Designation (staff dropdown)
- ICC Member 3: Name + Designation (staff dropdown — may be non-teaching)
- External Member: Name + Organisation (required — must be from NGO or legal background per Act; not an employee)
- Notes (textarea, optional)
- Upload ICC Constitution Order (PDF, required, max 5 MB)

**Validation:** Presiding officer must be a woman. External member is mandatory. At least one ICC member must be from a different department than the accused (enforced at complaint stage, flagged here as a reminder). If reconstituting, prior ICC record is archived automatically.

**Submit:** `Register ICC` → POST `/api/hr/posh/icc/` or PATCH `/api/hr/posh/icc/{branch_id}/`

### 6.2 Record Training

**Fields:**
- Branch (dropdown — multi-select to log training for multiple branches from one session)
- Training Date (date picker)
- Training Mode (dropdown: In-Person / Online / Hybrid)
- Trainer Name / Organisation (text)
- Staff Attended Count (numeric)
- Topics Covered (checkboxes: What is POSH / ICC Process / How to File a Complaint / Bystander Response / Legal Provisions)
- Upload Attendance Sheet (PDF/image, required)
- Upload Training Materials (PDF, optional, max 10 MB)

**Submit:** `Record Training` → POST `/api/hr/posh/training/`

### 6.3 Log Complaint

**Fields:**
- Branch (dropdown)
- Complainant Name (text — may be kept confidential; "Anonymous" option available)
- Respondent Name (text)
- Date of Incident (date picker)
- Date Complaint Filed (date picker, defaults to today)
- Complaint Description (textarea, min 100 characters)
- Evidence Upload (optional, PDF/image, max 5 MB)
- ICC Notified: Yes / No; if Yes → notification date

**Note:** This logs receipt of complaint; investigation and outcome are tracked separately via the complaint ID. This is not a POCSO log — system warns if POCSO-like details appear (e.g., student involved) and prompts to use POCSO page instead.

**Submit:** `Log Complaint` → POST `/api/hr/posh/complaints/`

### 6.4 Record Outcome

**Fields:**
- Complaint ID (locked, from existing complaint record)
- ICC Report Date (date — must be within 90 days of complaint filing)
- ICC Finding (dropdown: Complaint Substantiated / Not Substantiated / Malicious Complaint)
- Recommended Action (dropdown: Warning / Suspension / Termination / Apology / No Action / Referred to Police)
- Employer Action Date (date — must be within 60 days of ICC report)
- Employer Action Taken (textarea)
- Upload ICC Report (PDF, required)
- Complaint Status (auto-set to Closed on save)

**Submit:** `Record Outcome` → PATCH `/api/hr/posh/complaints/{id}/outcome/`

### 6.5 Submit Annual Report Confirmation

**Fields:**
- Branch (dropdown — multi-select)
- Reporting Year (dropdown: current or prior year)
- Submission Date (date picker — must be on or before 31st January)
- District Officer Name (text)
- Upload Report Acknowledgement (PDF, required)
- Complaints Count Reported (numeric, for accuracy — cross-checked against system count)

**Submit:** `Confirm Submission` → POST `/api/hr/posh/annual-report/`

---

## 7. Charts

No dedicated chart section on this page. Compliance summary charts are visible on the HR Analytics Dashboard (page 47) and HR Director Dashboard (page 01).

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| ICC registered | Success | "ICC registered for [Branch]. Term valid until [expiry_date]." |
| ICC reconstituted | Success | "ICC reconstituted for [Branch]. Previous ICC archived." |
| Training recorded | Success | "POSH training recorded for [N] branch(es) on [date]." |
| Complaint logged | Success | "Complaint logged. Complaint ID: POSH-XXXX." |
| Outcome recorded | Success | "Outcome recorded for POSH-XXXX. Complaint closed." |
| Annual report confirmed | Success | "Annual POSH report confirmed as submitted for [Branch]." |
| ICC expired alert | Warning | "ICC for [Branch] expired on [date]. Reconstitution required immediately." |
| Server error | Error | "Failed to save. Please retry or contact support." |

---

## 9. Empty States

**No branches in table (new group setup):**
> Icon: shield with checkmark
> "No branches registered in the POSH compliance register yet."
> "Branches are auto-populated from the Group Branch Register. Contact system admin if branches are missing."

**Filtered results return nothing:**
> Icon: magnifying glass
> "No branches match your current filters."
> CTA: `Reset Filters`

---

## 10. Loader States

- Page load: Skeleton KPI cards + skeleton table (all branches, full-width shimmer)
- Drawer open: Spinner while branch-specific ICC data loads
- Export: Loading spinner on Export button; disabled during generation
- Alert banner: Computed server-side on page load; no separate loading state

---

## 11. Role-Based UI Visibility

| UI Element | HR Director | HR Manager | POCSO Coordinator | Branch Principal |
|---|---|---|---|---|
| `+ Register ICC` button | Visible | Hidden | Hidden | Hidden |
| Record Training action | Visible | Visible | Hidden | Hidden |
| Log Complaint action | Visible | Hidden | Hidden | Hidden |
| Record Outcome action | Visible | Hidden | Hidden | Hidden |
| Submit Annual Report action | Visible | Hidden | Hidden | Hidden |
| Export Compliance Report | Visible | Visible | Hidden | Hidden |
| All branches view | Yes | Yes | Yes (read-only) | Own branch row only |
| Complaint details | Visible | Hidden | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/posh/` | Paginated branch compliance list |
| POST | `/api/hr/posh/icc/` | Register new ICC for branch |
| PATCH | `/api/hr/posh/icc/{branch_id}/` | Update/reconstitute ICC |
| GET | `/api/hr/posh/icc/{branch_id}/` | ICC details for branch |
| POST | `/api/hr/posh/training/` | Record POSH training |
| GET | `/api/hr/posh/complaints/` | List complaints |
| POST | `/api/hr/posh/complaints/` | Log new complaint |
| PATCH | `/api/hr/posh/complaints/{id}/outcome/` | Record complaint outcome |
| POST | `/api/hr/posh/annual-report/` | Confirm annual report submission |
| GET | `/api/hr/posh/kpis/` | KPI summary bar data |

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| Table load | `hx-get` on page render | Fetches branch compliance list |
| Filter change | `hx-get` + `hx-include` on filter form | Re-fetches table with active filters |
| Search | `hx-trigger="keyup changed delay:400ms"` | Debounced branch name search |
| Pagination | `hx-get` on page buttons | Fetches page N, swaps table body |
| Drawer open | `hx-get` + `hx-target="#drawer"` | Loads drawer for specific branch/complaint |
| Register ICC form | `hx-post` / `hx-patch` + `hx-target="#branch-row-{id}"` | Updates branch row after ICC registration |
| Record training form | `hx-post` + `hx-target="#table-body"` | Refreshes table after multi-branch training log |
| Log complaint form | `hx-post` with confirmation dialog | Creates complaint, updates complaint count in row |
| Annual report confirmation | `hx-post` + `hx-target="#branch-row-{id}"` | Updates annual report status badge in row |
| Toast | `hx-swap-oob` on `#toast-container` | Out-of-band toast injection |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
