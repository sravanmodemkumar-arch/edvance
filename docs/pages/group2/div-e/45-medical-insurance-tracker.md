# 45 — Staff Medical Insurance Tracker

- **URL:** `/group/hr/welfare/insurance/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Employee Welfare Officer (Role 52, G3)

---

## 1. Purpose

The Staff Medical Insurance Tracker manages the group's corporate health insurance policy for all permanent employees. The group maintains a Group Health Insurance (GHI) policy with a single insurance provider that covers all permanent staff members and their immediate family unit — defined as legal spouse plus up to two dependent children. This page is the operational interface for enrolling eligible staff, tracking their coverage, logging insurance claims, and monitoring policy renewal timelines.

Coverage tiers are standardised: standard permanent staff receive annual coverage of ₹2 lakh per year per family; senior staff at HOD grade and above receive ₹5 lakh per year per family. Premium payment is managed centrally by Group HR Finance — this page does not process payments but tracks premium due dates and alerts the Welfare Officer in advance of renewal deadlines. The policy is renewed annually and the Welfare Officer coordinates the group-wide enrolment update prior to each renewal.

Non-permanent staff — contract staff, visiting faculty, part-time staff, temporary appointees — are explicitly excluded from the GHI policy. The system enforces this at the enrolment stage by checking the staff's employment type field from the staff directory. Attempting to enrol a non-permanent staff member results in a blocking validation error with a clear message. This enforcement protects the group from invalid claims and premium disputes with the insurer.

The claims tracking section monitors hospitalisation claims and OPD claims submitted under the policy. Each claim has a status lifecycle: Submitted → Under Review (by insurer) → Approved or Rejected → Settled (if approved). The Welfare Officer tracks this lifecycle on behalf of staff, follows up with the insurer for delayed decisions, and communicates outcomes to the staff member. Outstanding claims (submitted but not yet settled) are tracked with their estimated value to monitor financial exposure. All data is maintained as records in the application database — policy documents and claim proofs are stored as uploaded files.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Employee Welfare Officer | G3 | Full CRUD + Enroll + Claim Management | Primary operator |
| Group HR Director | G3 | Read-only + Export | Policy oversight |
| Group HR Manager | G3 | Read-only + Initiate Claim | Operational support |
| Branch Principal | G3 | Read-only (own branch staff only) | View enrollment status of branch staff |
| Group Finance Head (if applicable) | G3 | Read-only (premium + claims value) | Budget tracking |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › Employee Welfare › Medical Insurance
```

### 3.2 Page Header

- **Title:** Staff Medical Insurance Tracker
- **Subtitle:** Group Health Insurance — enrolment, claims, and policy management
- **Tab Navigation:**
  - **Staff Enrolment** (default tab)
  - **Claims Register**
  - **Policy Details**
- **Primary CTA:** `+ Enrol Staff` (on Enrolment tab)  /  `+ Initiate Claim` (on Claims tab)
- **Secondary CTA:** `Export` (CSV/PDF, context-sensitive to active tab)

### 3.3 Alert Banner (conditional)

- **Red:** `Policy renewal is due in [N] days. Action required before [renewal_date].` Action: `View Policy`
- **Amber:** `[N] staff members enrolled have missing dependent details.` Action: `Review`
- **Amber:** `[N] claims have been pending insurer decision for > 30 days.` Action: `View Pending`
- **Blue:** `[N] staff members are newly permanent this month and eligible for enrolment.`
- **Green:** Policy active, all enrolled, no overdue claims — shown when no active alerts

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Enrolled Staff | Count of active enrolments in policy | Blue always | Switch to Enrolment tab |
| Policy Renewal Date | Days remaining until policy_end_date | Green if > 30 days, amber 15–30, red < 15 | Open Policy Details tab |
| Claims This Month | Count of claims with submitted_date in current month | Blue always | Switch to Claims tab, filter to current month |
| Claims Settled | Count of claims with status = Settled in last 90 days | Green always | Filter to settled claims |
| Claims Rejected | Count with status = Rejected in last 90 days | Red if > 0, else grey | Filter to rejected claims |
| Outstanding Claims Value (₹) | Sum of claimed_amount where status not in (Settled, Rejected) | Amber if > ₹5 lakh, red if > ₹15 lakh | Filter to outstanding claims |

---

## 5. Main Table — Staff Enrolment Register (Tab: Staff Enrolment)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text (link to staff profile) | Yes (A–Z) | Yes — text search |
| Branch | Text | Yes | Yes — dropdown |
| Role | Text | Yes | Yes — dropdown |
| Coverage Tier | Badge (Standard ₹2L / Senior ₹5L) | No | Yes — dropdown |
| Policy Number | Text (group policy number; same for all) | No | No |
| Enrollment Date | Date | Yes | Yes — date range |
| Active Claims | Count badge (0 = grey, > 0 = amber) | No | Yes — has claims toggle |
| Last Claim Date | Date (or "Never") | Yes | Yes — date range |
| Status | Badge (Active / Suspended / Lapsed / Pending Enrolment) | No | Yes — dropdown |
| Actions | Icon buttons: View Policy / Initiate Claim / Edit Enrolment / Suspend | No | No |

### 5.1 Filters

- **Branch:** Multi-select dropdown
- **Coverage Tier:** Standard / Senior / All
- **Enrolment Status:** Active / Suspended / Lapsed / Pending / All
- **Has Active Claims:** Toggle
- **Enrolment Date Range:** From / To
- **Reset Filters** button

### 5.2 Search

Text search on Staff Name. Min 2 characters, 400 ms debounce.

### 5.3 Pagination

Server-side. Default 20 rows per page. Options: 10 / 20 / 50. "Showing X–Y of Z enrolled staff."

---

## 6. Drawers

### 6.1 Enrol Staff

Triggered by `+ Enrol Staff`. Right slide-in drawer.

**Fields:**
- Staff Name (searchable dropdown — only shows permanent staff; non-permanent types greyed out with tooltip "Not eligible for GHI")
- Branch (auto-filled)
- Employment Type (auto-filled — read-only; must be "Permanent")
- Designation / Role (auto-filled)
- Coverage Tier (auto-determined by role — Senior for HOD+, Standard for others; read-only with override option for HR Director only)
- Enrolment Date (date picker, defaults to today)
- Policy Number (auto-filled from current active policy)
- Dependent 1 — Spouse: Name, DOB, Relationship (locked to "Spouse")
- Dependent 2 — Child 1: Name, DOB, Relationship (locked to "Child")
- Dependent 3 — Child 2: Name, DOB, Relationship (locked to "Child")
- Staff Photo (auto-pulled from staff profile)
- Employee ID / Staff Code (auto-filled)
- Enrolment Document Upload (PDF/image, optional)

**Validation:** Employment type must be Permanent. Maximum 2 children as dependants. Spouse DOB must result in age ≥ 18.

**Submit:** `Enrol Staff` → POST `/api/hr/welfare/insurance/enrolments/`

### 6.2 View Policy

Opens policy detail drawer showing insurer name, policy number, coverage period, sum insured per tier, premium amount, list of exclusions summary, and insurer contact details. Read-only. Download policy document (signed URL to uploaded PDF).

### 6.3 Initiate Claim

Triggered from Actions column or from `+ Initiate Claim` button on Claims tab.

**Fields:**
- Staff Name (searchable dropdown — only enrolled staff)
- Enrolment ID (auto-filled)
- Claim Type (dropdown: Hospitalisation / OPD / Surgery / Maternity / Dental / Vision)
- Patient Name (dropdown: Staff / Spouse / Child 1 / Child 2 — from enrolled dependants)
- Hospital / Clinic Name (text)
- Admission Date (date, if hospitalisation)
- Discharge Date (date, if hospitalisation)
- Claimed Amount (₹, numeric)
- Claim Description (textarea, min 50 characters)
- Upload Hospital Bills (PDF/image, up to 5 files × 5 MB each)
- Submission Date (defaults to today)
- Insurer Reference Number (text, optional — populated after submission to insurer)

**Submit:** `Initiate Claim` → POST `/api/hr/welfare/insurance/claims/`

### 6.4 Track Claim Status

Drawer for updating a claim's progress.

**Fields:**
- Claim ID (locked)
- Current Status (dropdown: Submitted / Under Review / Additional Docs Required / Approved / Rejected / Settled)
- Status Change Date (date, defaults to today)
- Insurer Response Note (textarea)
- Approved Amount (₹ — enabled only when status = Approved)
- Rejection Reason (required when status = Rejected)
- Settlement Date (date — required when status = Settled)
- Upload Insurer Response Document (PDF, optional)

**Submit:** `Update Status` → PATCH `/api/hr/welfare/insurance/claims/{id}/status/`

### 6.5 View Claims History

Opens from staff row on Enrolment tab. Lists all historical claims for that staff member in a scrollable list: claim ID, type, date, claimed amount, approved amount, status. Downloadable as PDF.

---

## 7. Charts

No dedicated charts on this page. Insurance spend vs. premium charts are visible in the HR Analytics Dashboard (page 47) and the Employee Welfare Officer Dashboard (page 12).

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Staff enrolled | Success | "[Name] enrolled in Group Health Insurance. Coverage: ₹[amount]." |
| Non-permanent enrolment blocked | Error | "[Name] is not eligible for GHI. Only permanent staff can be enrolled." |
| Claim initiated | Success | "Claim initiated for [Name]. Claim ID: CLM-XXXX." |
| Claim status updated | Success | "Claim CLM-XXXX status updated to [status]." |
| Claim rejected | Warning | "Claim CLM-XXXX has been rejected by the insurer. Reason: [reason]." |
| Policy renewal alert | Warning | "Group health insurance policy renews in [N] days." |
| Server error | Error | "Failed to save. Please retry or contact support." |

---

## 9. Empty States

**No staff enrolled (Enrolment tab):**
> Icon: shield with cross
> "No staff enrolled in the group health insurance policy yet."
> "Use '+ Enrol Staff' to begin enrolling permanent staff."
> CTA: `+ Enrol Staff`

**No claims (Claims tab):**
> Icon: document with checkmark
> "No insurance claims have been submitted yet."
> CTA: `+ Initiate Claim`

**No results for active filters:**
> Icon: magnifying glass
> "No records match your current filters."
> CTA: `Reset Filters`

---

## 10. Loader States

- Page load: Skeleton KPI cards + skeleton table rows
- Tab switch: Spinner in table area while new tab data loads
- Drawer open: Spinner while fetching staff or claim data
- Claims history: Inline spinner in the claims list within drawer
- Policy document loading: Skeleton in the document preview area

---

## 11. Role-Based UI Visibility

| UI Element | Welfare Officer | HR Director | HR Manager | Branch Principal |
|---|---|---|---|---|
| `+ Enrol Staff` button | Visible | Hidden | Hidden | Hidden |
| `+ Initiate Claim` button | Visible | Hidden | Visible | Hidden |
| Track Claim Status action | Visible | Hidden | Visible | Hidden |
| Suspend Enrolment action | Visible | Hidden | Hidden | Hidden |
| Export button | Visible | Visible | Hidden | Hidden |
| Coverage Tier override | Hidden | Visible | Hidden | Hidden |
| Outstanding Claims Value KPI | Visible | Visible | Hidden | Hidden |
| All branches | Yes | Yes | Yes | Own branch only |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/welfare/insurance/enrolments/` | Paginated enrolled staff list |
| POST | `/api/hr/welfare/insurance/enrolments/` | Create new enrolment |
| GET | `/api/hr/welfare/insurance/enrolments/{id}/` | Single enrolment detail |
| PATCH | `/api/hr/welfare/insurance/enrolments/{id}/` | Edit enrolment or suspend |
| GET | `/api/hr/welfare/insurance/claims/` | Paginated claims list |
| POST | `/api/hr/welfare/insurance/claims/` | Initiate new claim |
| GET | `/api/hr/welfare/insurance/claims/{id}/` | Single claim detail |
| PATCH | `/api/hr/welfare/insurance/claims/{id}/status/` | Update claim status |
| GET | `/api/hr/welfare/insurance/policy/` | Active policy details |
| GET | `/api/hr/welfare/insurance/kpis/` | KPI summary bar data |

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| Tab switch | `hx-get` on tab button + `hx-target="#tab-content"` | Fetches and renders active tab data |
| Table load | `hx-get` triggered on tab activation | Fetches respective list (enrolments or claims) |
| Filter change | `hx-get` + `hx-include` on filter form | Re-fetches table body with updated params |
| Pagination | `hx-get` on page navigation buttons | Fetches specified page |
| Drawer open | `hx-get` + `hx-target="#drawer"` | Loads drawer for specific enrolment/claim |
| Enrol staff form | `hx-post` + `hx-target="#table-body"` | Submits form, refreshes table |
| Claim update form | `hx-patch` + `hx-target="#claim-row-{id}"` | Updates row in place |
| KPI bar refresh | `hx-get` on `#kpi-bar` after mutations | Reloads KPI data |
| Toast | `hx-swap-oob` on `#toast-container` | Out-of-band toast injection |
| Alert banner | `hx-get` on `#alert-banner` on page load | Fetches active alert conditions |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
