# 04 — Group Recruiter (Non-Teaching) Dashboard

- **URL:** `/group/hr/recruitment/nonteaching/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Recruiter — Non-Teaching (Role 44, G0)

---

## 1. Purpose

The Group Recruiter (Non-Teaching) role is responsible for sourcing, screening, and recommending candidates for all non-instructional positions across the group's branches. These roles span a wide functional range: administrative staff (office assistants, registrars, front-desk), hostel staff (wardens, matrons, attendants), transport staff (drivers, helpers), security personnel, kitchen and catering staff (cooks, canteen supervisors), laboratory assistants, librarians, housekeeping supervisors, and IT support staff. The group's dependency on a well-staffed non-teaching workforce is operationally critical — gaps in hostel supervision, security, or transport directly affect student safety.

Like the teaching recruiter, Role 44 is classified G0 — no default EduForge platform access. A limited portal view is provisioned explicitly by the HR Manager or HR Director in large-group configurations. This view is strictly scoped: the non-teaching recruiter sees only their assigned drives for non-teaching roles, their candidate pipeline, and their interview schedule. They cannot access teaching role data, BGV records, salary bands, HR policies, or any data outside their assigned branch scope.

A key operational difference from the teaching recruiter role is the sourcing channel: non-teaching hires frequently come from walk-in applicants, employee referrals, or local placement agents — not through the ATS. The candidate intake process therefore includes a "Source" field so the HR Manager can track recruitment channel effectiveness over time. Background check initiation for non-teaching hires is particularly important given POCSO obligations for any staff member (including kitchen and housekeeping staff) with physical access to minor students.

The BGV initiation flag in the pipeline table is a safety control: once a non-teaching candidate is offered a position, the recruiter is expected to flag them for BGV initiation before the joining date. This page surfaces candidates in the "Offered" stage who have not yet been flagged for BGV so the HR Manager can act.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Recruiter — Non-Teaching | G0 | Limited: own assigned non-teaching drives only | Requires explicit provisioning by HR Manager |
| Group HR Manager | G3 | Full read on this page's data | Manages recruiter assignments |
| Group HR Director | G3 | Full read | Oversight |
| Group BGV Manager | G3 | Read-only on BGV initiation flag column | Monitors pre-join BGV flagging |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Recruitment → Non-Teaching Recruiter View
```

### 3.2 Page Header
- **Title:** `My Assigned Non-Teaching Recruitment Drives`
- **Subtitle:** `Showing [N] active drive(s) assigned to you · AY [current academic year]`
- **Role Badge:** `Group Recruiter (Non-Teaching)`
- **Right-side controls:** `Submit Recommendation` (context-sensitive) · `Flag for BGV` (context-sensitive on Offered candidates)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Offered candidates not flagged for BGV | "[N] offered candidate(s) have not been flagged for background verification. Required before joining." | Red |
| Recommendation overdue > 2 days post-interview | "[N] candidate(s) are awaiting your recommendation for more than 2 days." | Amber |
| Drive closing in 7 days | "The [Role] drive at [Branch] is closing in 7 days. Finalize candidate recommendations." | Amber |
| Access provisioning expired | "Your portal access has expired. Contact the Group HR Manager." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| My Active Non-Teaching Drives | Count of open non-teaching drives assigned to this recruiter | Blue | Scrolls to drives table |
| Candidates Screened | Candidates at Screened or Shortlisted stage in assigned drives | Blue | Filtered candidate list |
| Interviews This Week | Confirmed interview slots in current week | Green | Interview schedule |
| Pending BGV Initiation | Offered candidates not yet flagged for background check | Red if > 0, Green if 0 | Filtered candidate list (Offered stage) |

---

## 5. Main Table — Candidate Pipeline (Non-Teaching Roles)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Candidate Name | Text | Yes | Yes (text search) |
| Role Category | Badge (Admin / Hostel / Transport / Security / Kitchen / Lab / Library / IT / Other) | Yes | Yes (dropdown) |
| Applied Branch | Text | Yes | Yes (multi-select) |
| Drive / Role Title | Text | Yes | Yes |
| Source | Badge (Walk-in / Referral / Portal / Agency) | Yes | Yes (checkbox) |
| Resume Status | Badge (Not Reviewed / Screened / Shortlisted / Rejected) | Yes | Yes |
| Interview Date | Date | Yes | Yes (date range) |
| Recommendation | Badge (Pending / Proceed / Hold / Do Not Proceed) | Yes | Yes |
| BGV Flagged | Boolean badge (Yes / No) | Yes | Yes (Yes/No) |
| Actions | Submit Recommendation / Flag BGV / View | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Role Category | Multi-select checkbox | Admin / Hostel / Transport / Security / Kitchen / Lab / Library / IT / Other |
| Source | Checkbox | Walk-in / Referral / Portal / Agency |
| Recommendation Status | Checkbox | Pending / Proceed / Hold / Do Not Proceed |
| BGV Flagged | Radio | All / Flagged / Not Flagged |
| Interview Date | Date range picker | Any range |

### 5.2 Search
- Full-text: Candidate name, role title, applied branch
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `nt-recommendation-submit` — Submit Candidate Recommendation
- **Trigger:** Actions → Submit Recommendation
- **Width:** 560px
- **Fields:**
  - Candidate Name (read-only)
  - Role Category (read-only)
  - Drive / Role Title (read-only)
  - Applied Branch (read-only)
  - Interview Date (read-only)
  - Source Channel (read-only)
  - Recommendation (required, radio: Proceed / Hold / Do Not Proceed)
  - Role Fit Rating (required, 1–5 stars)
  - Communication Rating (required, 1–5 stars)
  - Physical Fitness / Availability (required, 1–5 stars; relevant for transport, security roles)
  - Detailed Notes (required, textarea, min 40 chars)
  - Flagged for BGV (required, checkbox; must be checked for Proceed recommendations)
- **Validation:** BGV flag must be checked before submitting a Proceed recommendation

### 6.2 Drawer: `nt-candidate-view` — View Candidate Profile
- **Trigger:** Actions → View
- **Width:** 720px
- Shows: Name, contact (partially masked), role category, source, all interview rounds, recommendations, current stage, branch applied for, BGV flag status
- Does NOT show: Salary band, other candidates' data, HR policy details

### 6.3 Drawer: `bgv-flag` — Flag Candidate for BGV Initiation
- **Trigger:** Actions → Flag BGV (enabled only for Offered stage candidates)
- **Width:** 400px
- **Fields:**
  - Candidate Name (read-only)
  - Expected Joining Date (required, date picker)
  - ID Proof Type (required, dropdown: Aadhaar / PAN / Passport / Voter ID)
  - ID Proof Number (required, masked input)
  - Notes for BGV Team (optional textarea)
- On submit: creates a BGV initiation request routed to Group BGV Manager

### 6.4 Modal: Confirm Recommendation
- Confirmation: "Submit [Proceed / Hold / Do Not Proceed] recommendation for [Candidate Name] for [Role] at [Branch]? This will notify the HR Manager."
- Buttons: Confirm · Cancel

---

## 7. Charts

### 7.1 My Pipeline by Role Category (Horizontal Bar Chart)
- Y-axis: Role categories (Admin, Hostel, Transport, Security, etc.)
- X-axis: Candidate count
- Segmented by stage (Screened / Shortlisted / Interviewed / Offered)
- Scope: Only this recruiter's assigned candidates

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Recommendation submitted | "Recommendation submitted for [Candidate Name]. HR Manager notified." | Success | 4s |
| BGV flag submitted | "BGV initiation request submitted for [Candidate Name]. BGV Team notified." | Success | 4s |
| Proceed without BGV flag blocked | "Cannot submit Proceed recommendation without flagging candidate for BGV." | Error | 6s |
| Access expired | "Your portal access has expired. Contact the HR Manager." | Error | 8s |
| Validation error | "Please complete all required fields before submitting." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No drives assigned | "No Drives Assigned Yet" | "You have not been assigned to any non-teaching recruitment drive. Contact the HR Manager." | — |
| No candidates in pipeline | "No Candidates Yet" | "No candidates have entered your assigned drives. Begin walk-in or referral intake." | — |
| All recommended | "All Recommendations Submitted" | "You have submitted recommendations for all interviewed candidates. Well done." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Skeleton: 4 KPI cards shimmer + table skeleton (8 rows) |
| Candidate detail drawer open | Drawer spinner centred |
| Recommendation form submit | Button spinner + form fields disabled |
| BGV flag form submit | Button spinner + confirmation pending state |

---

## 11. Role-Based UI Visibility

| Element | Recruiter Non-Teaching (G0 — provisioned) | HR Manager (G3) | BGV Manager (G3) | Not provisioned (G0) |
|---|---|---|---|---|
| KPI Summary Bar | Visible (own data only) | Full manager view | Not on this page | Access denied (403) |
| Candidate Pipeline Table | Visible (assigned drives only) | Full view on manager dashboard | Read-only BGV column | Access denied (403) |
| Flag for BGV Button | Visible (Offered candidates only) | N/A | N/A | Hidden |
| Salary Band Data | Never shown | Shown on manager page | Not shown | Never shown |
| Submit Recommendation Button | Visible (pending candidates) | N/A | N/A | Hidden |
| BGV Flagged Column | Visible | Visible | Visible | Hidden |
| Teaching role data | Never shown | N/A | N/A | Never shown |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/recruitment/nonteaching/my-drives/` | JWT (G0 provisioned) | Drives assigned to this recruiter |
| GET | `/api/v1/hr/recruitment/nonteaching/candidates/` | JWT (G0 provisioned) | Candidates in assigned non-teaching drives |
| GET | `/api/v1/hr/recruitment/nonteaching/candidates/{id}/` | JWT (G0 provisioned) | Single candidate profile |
| POST | `/api/v1/hr/recruitment/recommendations/` | JWT (G0 provisioned) | Submit recommendation with BGV flag |
| POST | `/api/v1/hr/bgv/initiation-requests/` | JWT (G0 provisioned) | Submit BGV flag for an offered candidate |
| GET | `/api/v1/hr/recruitment/nonteaching/kpis/` | JWT (G0 provisioned) | Recruiter-scoped KPI values |
| GET | `/api/v1/hr/recruitment/nonteaching/charts/pipeline/` | JWT (G0 provisioned) | Pipeline by role category chart data |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/hr/recruitment/nonteaching/kpis/` | `#kpi-bar` | `innerHTML` |
| Load pipeline table | `load` | GET `/api/v1/hr/recruitment/nonteaching/candidates/` | `#pipeline-table` | `innerHTML` |
| Filter by role category | `change` on category filter | GET `/api/v1/hr/recruitment/nonteaching/candidates/?category=...` | `#pipeline-table` | `innerHTML` |
| Open BGV flag drawer | `click` on Flag BGV | GET `/api/v1/hr/recruitment/nonteaching/candidates/{id}/` | `#bgv-flag-drawer` | `innerHTML` |
| Submit recommendation | `click` on Confirm Submit | POST `/api/v1/hr/recruitment/recommendations/` | `#pipeline-table` | `innerHTML` |
| Submit BGV flag | `click` on Submit BGV Flag | POST `/api/v1/hr/bgv/initiation-requests/` | `#bgv-flag-result` | `innerHTML` |
| Search candidates | `input` (300ms debounce) | GET `/api/v1/hr/recruitment/nonteaching/candidates/?q=...` | `#pipeline-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
