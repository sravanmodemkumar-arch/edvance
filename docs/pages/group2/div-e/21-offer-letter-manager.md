# 21 — Offer Letter Manager

- **URL:** `/group/hr/recruitment/offers/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Offer Letter Manager is the penultimate stage of the recruitment process — the formal moment when the group extends a job offer to a selected candidate. A well-managed offer process is critical to conversion: candidates who receive offers but don't receive follow-up, or who wait too long for paperwork, frequently accept competing offers before responding. This page gives the Group HR Manager a complete view of all outstanding offers, their status, and the actions required to move candidates from "Offer Sent" to "Joined."

Each offer letter is generated from a template that incorporates: the role title, target branch, salary (drawn from the grade band, not entered ad hoc), start date, reporting manager, key terms and conditions, and any special conditions negotiated during the interview process. Because salary is linked to grade bands, the system validates that the offered amount is within the permissible range. If an HR Manager attempts to offer a salary above the band maximum, the system flags the record and requires HR Director approval before the letter can be sent. This prevents unilateral salary exceptions from creating compensation inequity.

The offer response window is 7 days from the date the offer is sent. If a candidate does not respond within 7 days, the offer is automatically marked as Expired and the candidate record is flagged for recruiter follow-up. Declines are always accompanied by a mandatory reason capture (Better Offer Received / Location Constraint / Salary Insufficient / Personal Reasons / Other), which feeds a running analysis of why the group loses candidates at the offer stage. This data helps the HR Director identify whether salary bands need to be revised or whether location-based incentives are needed for certain branches.

When an offer is accepted, the system automatically creates an onboarding checklist for the candidate in the Onboarding Tracker (page 22) and transitions the candidate's pipeline record to "Offer Accepted → Joined" status. This automatic trigger eliminates the gap between acceptance and onboarding initiation that often results in new joiners arriving without accounts, IDs, or contracts ready.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access + salary exception approval | Can generate, approve, revoke offers |
| Group HR Manager (42) | G3 | Full CRUD | Primary owner of offer management |
| Group Recruiter — Teaching (43) | G0 | No access | — |
| Group Recruiter — Non-Teaching (44) | G0 | No access | — |
| Group Training & Dev Manager (45) | G2 | No access | — |
| Group Performance Review Officer (46) | G1 | No access | — |
| Group Staff Transfer Coordinator (47) | G3 | No access | — |
| Group BGV Manager (48) | G3 | No access | — |
| Group BGV Executive (49) | G3 | No access | — |
| Group POCSO Coordinator (50) | G3 | No access | — |
| Group Disciplinary Committee Head (51) | G3 | No access | — |
| Group Employee Welfare Officer (52) | G3 | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Recruitment → Offer Letter Manager`

### 3.2 Page Header
- Title: "Offer Letter Manager"
- Subtitle: "Generate and track offer letters for selected candidates."
- Primary CTA: "+ Generate Offer Letter"
- Secondary CTAs: "Export Offers Report" | "View Acceptance Rate Trend"

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Offers expiring today (7-day window closing) | "[N] offer(s) expire today. Follow up with candidates immediately." | Red |
| Salary exception awaiting HR Director approval | "[N] offer(s) are pending HR Director approval for salary exception." | Orange |
| Offers with no response > 5 days | "[N] offer(s) have received no response in over 5 days." | Yellow |
| Offer accepted — onboarding not yet initiated | "[N] accepted offer(s) have no onboarding checklist created." | Orange |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Offers Generated | Total offers created (all time / this month toggle) | Neutral blue | — |
| Offers Accepted | Count accepted (this month) | Green | Filters to Accepted |
| Offers Declined | Count declined (this month) | Red if > accepted | Filters to Declined |
| Awaiting Response | Count in Pending status (within 7-day window) | Amber if > 5 | Filters to Pending |
| Expired (No Response) | Count auto-expired (past 7 days with no action) | Red if > 0 | Filters to Expired |
| Acceptance Rate % | (Accepted / Sent) × 100 in last 90 days | Amber if < 60%, Green if ≥ 75% | Opens trend chart |

---

## 5. Main Table — Offer Letters

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Candidate Name | Text (link to view drawer) | Yes | Yes (search) |
| Applied Role | Text | Yes | Yes (dropdown) |
| Branch | Text | Yes | Yes (dropdown) |
| Offer Date | Date | Yes | Yes (date range) |
| Salary Offered (₹) | Currency | Yes | No |
| Status | Chip (Pending / Accepted / Declined / Expired / Revoked) | Yes | Yes |
| Days Since Offer | Integer (computed) | Yes | Yes (> N filter) |
| Decline Reason | Text / "—" | No | Yes (when status = Declined) |
| Onboarding Created | Boolean chip (Yes/No) | No | Yes |
| Actions | View / Edit / Resend / Revoke | No | No |

### 5.1 Filters
- Status: All | Pending | Accepted | Declined | Expired | Revoked
- Branch: All branches (dropdown)
- Days Since Offer: Any | > 3 | > 5 | > 7
- Onboarding Created: All | Yes | No (highlights accepted offers without onboarding)

### 5.2 Search
Search by candidate name. Minimum 2 characters, 400ms debounce.

### 5.3 Pagination
Server-side pagination, 20 records per page. Standard navigation controls. Total count displayed above table.

---

## 6. Drawers

### 6.1 Drawer: Generate Offer Letter (Create)
Fields: Candidate (typeahead — filters to candidates in "Offer Sent" pipeline stage or manually selectable), Branch (auto-populated), Role Title (auto-populated), Reporting Manager (dropdown — branch staff), Start Date (date picker, must be future), Salary (₹ — numeric with grade band reference shown: "Band [Code]: ₹[Min] – ₹[Max]"; input validates against band), Allowances (HRA / DA / Transport auto-populated from band; editable with justification), Probation Period (months — default 6 for permanent, 0 for contract), Special Conditions (textarea), Offer Expiry Date (auto-set to today + 7 days; adjustable with reason), Internal Notes (not included in offer letter).
Salary Exception Flow: If salary > band max, a warning banner appears inside the drawer: "This salary exceeds the grade band maximum. Saving will flag for HR Director approval before letter is sent."
Preview Button: Renders offer letter PDF preview in new browser tab (GET `/api/v1/hr/recruitment/offers/preview/`).
On Save: POST to API, offer record created, letter generated as PDF, status = Draft. "Send Offer" button becomes active.

### 6.2 Drawer: View Offer
Read-only. All offer fields, PDF download link, response timeline (sent date, response date, response type). Audit trail. If status = Declined: decline reason and notes displayed.

### 6.3 Drawer: Edit Offer (Draft only)
Available only for Draft or Pending offers where letter has not yet been accepted. All fields editable. Reason for change (textarea, required). Editing a Pending offer generates a revised letter and re-notifies the candidate.

### 6.4 Modal: Decline Reason Capture
Triggered when status changes to Declined (HR records candidate's response). Reason dropdown: Better Offer Received / Location Constraint / Salary Insufficient / Personal Reasons / Role Change / Other. Notes field (optional). On Confirm: decline recorded, pipeline stage updated to "Offer Declined".

### 6.5 Modal: Revoke Offer
Reason (Role Cancelled / Budget Freeze / Process Error / Other) + Notes + Confirmation prompt. On Confirm: offer status → Revoked, candidate notified, pipeline stage updated.

---

## 7. Charts

**Offer Acceptance Rate Trend — Monthly Bar Chart:** X-axis = last 6 months; Y-axis = percentage. Two bars per month: Acceptance Rate (green) and Decline Rate (red). Rendered via Chart.js. Positioned below the main table. Toggle: "Show Trend Chart / Hide".

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Offer letter created | "Offer letter for [Candidate] created. Preview before sending." | Success | 4s |
| Offer sent | "Offer letter sent to [Candidate]. Expires [Date]." | Success | 5s |
| Offer accepted | "[Candidate] has accepted the offer. Onboarding checklist created." | Success | 5s |
| Offer declined — reason saved | "Offer declined by [Candidate]. Reason recorded." | Info | 4s |
| Offer auto-expired | "Offer for [Candidate] expired (no response in 7 days)." | Warning | 5s |
| Salary exception flagged | "Salary exceeds band maximum. Awaiting HR Director approval." | Warning | 6s |
| Offer revoked | "Offer for [Candidate] has been revoked." | Info | 4s |
| PDF preview opened | "Offer letter preview opened in a new tab." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No offers generated | "No Offer Letters Yet" | "Generate offer letters for candidates who have passed the interview stage." | Generate Offer Letter |
| Filter returns no results | "No Matching Offers" | "Adjust filters to find the offer you're looking for." | Clear Filters |
| Declined tab empty | "No Declined Offers" | "No candidates have declined offers." | — |
| Expired tab empty | "No Expired Offers" | "All sent offers have received responses within the deadline." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI skeletons (6) + table row skeletons (12) |
| Filter change | Table body row skeletons |
| Drawer open | Form field skeletons |
| PDF preview generation | Spinner in preview button; new tab opens on completion |
| Offer send action | Button spinner + disabled state |
| Chart render | Spinner in chart container |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) | HR Manager (42) | All Other Roles |
|---|---|---|---|
| Generate Offer Letter button | Visible + enabled | Visible + enabled | Hidden |
| Edit offer | Visible | Visible | Hidden |
| Revoke offer | Visible | Visible | Hidden |
| Salary exception approval | Visible + actionable | Visible as warning only | Hidden |
| View offer detail | Visible | Visible | Hidden |
| Export Report | Visible | Visible | Hidden |
| Trend chart | Visible | Visible | Hidden |
| Salary field in offer form | Visible | Visible (validated) | N/A |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/recruitment/offers/` | JWT | List all offer letters |
| POST | `/api/v1/hr/recruitment/offers/` | JWT | Generate new offer letter |
| GET | `/api/v1/hr/recruitment/offers/{id}/` | JWT | Fetch offer detail |
| PATCH | `/api/v1/hr/recruitment/offers/{id}/` | JWT | Update offer letter |
| POST | `/api/v1/hr/recruitment/offers/{id}/send/` | JWT | Send offer to candidate |
| PATCH | `/api/v1/hr/recruitment/offers/{id}/accept/` | JWT | Record acceptance + trigger onboarding |
| PATCH | `/api/v1/hr/recruitment/offers/{id}/decline/` | JWT | Record decline with reason |
| PATCH | `/api/v1/hr/recruitment/offers/{id}/revoke/` | JWT | Revoke offer |
| GET | `/api/v1/hr/recruitment/offers/preview/` | JWT | Generate PDF preview |
| GET | `/api/v1/hr/recruitment/offers/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/recruitment/offers/chart/` | JWT | Acceptance rate trend chart data |
| GET | `/api/v1/hr/recruitment/offers/export/` | JWT | Export offers report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/recruitment/offers/?q={val}` | `#offers-table-body` | innerHTML |
| Status filter | change | GET `/api/v1/hr/recruitment/offers/?status={val}` | `#offers-table-body` | innerHTML |
| Branch / days filter | change | GET `/api/v1/hr/recruitment/offers/?branch={}&days={}` | `#offers-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/recruitment/offers/?page={n}` | `#offers-table-body` | innerHTML |
| Generate offer drawer open | click | GET `/group/hr/recruitment/offers/create/drawer/` | `#drawer-container` | innerHTML |
| View drawer open | click | GET `/group/hr/recruitment/offers/{id}/view/drawer/` | `#drawer-container` | innerHTML |
| Edit drawer open | click | GET `/group/hr/recruitment/offers/{id}/edit/drawer/` | `#drawer-container` | innerHTML |
| Create submit | submit | POST `/api/v1/hr/recruitment/offers/` | `#offers-table-body` | afterbegin |
| Edit submit | submit | PATCH `/api/v1/hr/recruitment/offers/{id}/` | `#offer-row-{id}` | outerHTML |
| Send offer action | click | POST `/api/v1/hr/recruitment/offers/{id}/send/` | `#offer-row-{id}` | outerHTML |
| Decline modal | click | GET `/group/hr/recruitment/offers/{id}/decline/modal/` | `#modal-container` | innerHTML |
| Revoke modal | click | GET `/group/hr/recruitment/offers/{id}/revoke/modal/` | `#modal-container` | innerHTML |
| Chart toggle | click | GET `/group/hr/recruitment/offers/chart/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
