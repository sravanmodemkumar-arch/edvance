# 03 — Group Recruiter (Teaching) Dashboard

- **URL:** `/group/hr/recruitment/teaching/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Recruiter — Teaching (Role 43, G0)

---

## 1. Purpose

The Group Recruiter (Teaching) role operates primarily outside the EduForge platform, using an external Application Tracking System (ATS) for day-to-day candidate management. Role 43 carries a G0 access level, meaning these users are not provisioned with standard EduForge platform credentials. However, in large group configurations where multiple teaching recruiters are employed, a limited portal view may be provisioned to allow them to see their assigned drives and submit structured recommendations back to the HR Manager.

This page spec documents that limited, scoped view. It is NOT a full HR dashboard. The teaching recruiter sees only the job drives specifically assigned to them, only the candidates within those drives, and only the interview schedule relevant to their pipeline. They cannot see salary bands, BGV records, HR policies, disciplinary data, transfer records, or any data pertaining to branches outside their assigned scope. This access boundary is enforced both at the UI level and at the API level via role-scoped JWT claims.

The primary utility of this limited view is structured recommendation submission. After an interview, the recruiter must submit a formal recommendation (Proceed / Do Not Proceed / Hold) with notes that feed into the HR Manager's pipeline view. This eliminates email-based handoffs and creates an auditable trail. The recommendation becomes read-only once the HR Manager acts on it.

Access to this page must be explicitly provisioned by the Group HR Director or HR Manager. It is disabled by default for G0 roles. If a teaching recruiter attempts to access any URL outside their scoped paths, they receive a 403 screen with a clear message redirecting them to their assigned drives.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Recruiter — Teaching | G0 | Limited: own assigned drives only | Default G0 = no access; this view requires explicit provisioning |
| Group HR Manager | G3 | Full read on this page's data | Manages recruiter assignments |
| Group HR Director | G3 | Full read | Oversight |
| Other HR roles | G1–G3 | No access to this specific scoped view | Recruiter view is isolated by design |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Recruitment → Teaching Recruiter View
```

### 3.2 Page Header
- **Title:** `My Assigned Teaching Recruitment Drives`
- **Subtitle:** `Showing [N] active drive(s) assigned to you · AY [current academic year]`
- **Role Badge:** `Group Recruiter (Teaching)`
- **Right-side controls:** `Submit Recommendation` (context-sensitive, appears when a candidate row is selected)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Interview scheduled today | "You have [N] interview(s) scheduled today. Ensure feedback is submitted by EOD." | Blue (info) |
| Recommendation overdue > 2 days post-interview | "[N] candidate(s) are awaiting your recommendation for more than 2 days." | Amber |
| Drive closing in 7 days | "The [Role] drive at [Branch] is closing in 7 days. Finalize your candidate recommendations." | Amber |
| Access provisioning expired | "Your portal access has expired. Contact the Group HR Manager to renew." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| My Active Drives | Count of open job drives assigned to this recruiter | Blue | Scrolls to drives table |
| Candidates Screened Today | Resumes reviewed / screened in the current calendar day | Blue | Filtered candidate list |
| Interviews Scheduled This Week | Confirmed interview slots in current week | Green | Interview schedule view |
| Offers Pending | Candidates in "Offer Issued" stage awaiting acceptance/rejection | Amber if > 0 | Filtered candidate list |

---

## 5. Main Table — Candidate Pipeline (Teaching Roles)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Candidate Name | Text | Yes | Yes (text search) |
| Subject Specialisation | Text | Yes | Yes (dropdown) |
| Class Level | Text (e.g., Primary / Middle / Secondary / Senior Secondary) | Yes | Yes (dropdown) |
| Applied Branch | Text | Yes | Yes (multi-select) |
| Drive / Role | Text | Yes | Yes |
| Resume Status | Badge (Not Reviewed / Screened / Shortlisted / Rejected) | Yes | Yes |
| Interview Date | Date (future = highlighted blue, past without feedback = amber) | Yes | Yes (date range) |
| Recommendation | Badge (Pending / Proceed / Hold / Do Not Proceed) | Yes | Yes |
| Submitted By | Text (recruiter name) | No | No |
| Actions | Submit Recommendation (if pending) / View | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Drive / Role | Dropdown | Assigned drives only |
| Resume Status | Checkbox | Not Reviewed / Screened / Shortlisted / Rejected |
| Recommendation | Checkbox | Pending / Proceed / Hold / Do Not Proceed |
| Interview Date | Date range picker | Any date range |

### 5.2 Search
- Full-text: Candidate name, subject specialisation
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `recommendation-submit` — Submit Candidate Recommendation
- **Trigger:** Actions → Submit Recommendation on a candidate row
- **Width:** 560px
- **Fields:**
  - Candidate Name (read-only, auto-filled)
  - Drive / Role (read-only)
  - Applied Branch (read-only)
  - Interview Date (read-only)
  - Interview Mode (read-only: In-Person / Video / Panel)
  - Recommendation (required, radio: Proceed / Hold / Do Not Proceed)
  - Subject Knowledge Rating (required, 1–5 stars)
  - Communication Rating (required, 1–5 stars)
  - Classroom Presence Rating (required, 1–5 stars)
  - Detailed Notes (required, textarea, min 50 chars)
  - Suggested Salary Expectation (₹, optional; recruiter captures candidate's stated expectation — not band)
- **Validation:** Recommendation + notes required; ratings required

### 6.2 Drawer: `candidate-view` — View Candidate Profile
- **Trigger:** Actions → View on any candidate row
- **Width:** 720px
- Shows: Candidate name, contact (partially masked), subject, class level, resume uploaded date, all interview rounds with dates, all recommendations submitted, current pipeline stage, branch applied for

### 6.3 Drawer: `drive-view` — View Assigned Drive Details
- **Trigger:** Click on drive name in KPI drill-down or table
- **Width:** 560px
- Shows: Role title, branch, number of openings, days open, number of candidates at each stage, target joining date, assigned recruiter (self)
- Does NOT show: Salary band, posting budget, HR notes, BGV fields

### 6.4 Modal: Confirm Recommendation Submission
- Confirmation: "You are submitting a [Proceed / Do Not Proceed / Hold] recommendation for [Candidate Name]. This will notify the HR Manager. Proceed?"
- Buttons: Confirm Submit · Cancel

---

## 7. Charts

### 7.1 My Pipeline Funnel (Funnel Chart)
- Stages limited to recruiter's scope: Applied → Screened → Shortlisted → Interviewed → Recommendation Submitted
- Shows only this recruiter's assigned candidates
- Helps recruiter see where their pipeline is bottlenecked

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Recommendation submitted | "Recommendation submitted for [Candidate Name]. HR Manager notified." | Success | 4s |
| Recommendation already submitted | "A recommendation was already submitted for this candidate. Contact HR to revise." | Warning | 5s |
| Candidate profile viewed | — (silent navigation) | — | — |
| Access expired error | "Your portal access has expired. Please contact the HR Manager." | Error | 8s |
| Form validation error | "Please complete all required fields and ratings before submitting." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No drives assigned | "No Drives Assigned Yet" | "You have not been assigned to any active recruitment drive. Contact the HR Manager." | — |
| No candidates in assigned drives | "No Candidates Yet" | "No candidates have applied to your assigned drives. Sourcing may be in progress." | — |
| All recommendations submitted | "All Caught Up" | "You have submitted recommendations for all interviewed candidates." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Skeleton: 4 KPI cards shimmer + table skeleton (8 rows) |
| Candidate detail drawer open | Drawer spinner, profile loads in sections |
| Recommendation form submission | Button spinner + all form fields disabled |
| Pipeline funnel chart load | Chart area shimmer overlay |

---

## 11. Role-Based UI Visibility

| Element | Recruiter Teaching (G0 — provisioned) | HR Manager (G3) | HR Director (G3) | Other G0 (not provisioned) |
|---|---|---|---|---|
| KPI Summary Bar | Visible (own data only) | Full visibility on manager dashboard | Full visibility on director dashboard | Access denied (403) |
| Candidate Pipeline Table | Visible (assigned drives only) | Full view on manager dashboard | Full view | Access denied (403) |
| Salary Band Data | Hidden (never shown) | Visible in manager view | Visible | Hidden |
| Submit Recommendation Button | Visible (for pending candidates) | Not applicable | Not applicable | Hidden |
| Pipeline Funnel Chart | Visible (own data) | Not applicable | Not applicable | Hidden |
| BGV / POCSO Data | Completely hidden | Not applicable | Not applicable | Completely hidden |
| Other branch data | Completely hidden (scoped) | Not applicable | Not applicable | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/recruitment/teaching/my-drives/` | JWT (G0 provisioned) | List drives assigned to this recruiter |
| GET | `/api/v1/hr/recruitment/teaching/candidates/` | JWT (G0 provisioned) | Candidates in recruiter's assigned drives only |
| GET | `/api/v1/hr/recruitment/teaching/candidates/{id}/` | JWT (G0 provisioned) | Single candidate profile (scoped) |
| POST | `/api/v1/hr/recruitment/recommendations/` | JWT (G0 provisioned) | Submit candidate recommendation |
| GET | `/api/v1/hr/recruitment/teaching/kpis/` | JWT (G0 provisioned) | Recruiter-scoped KPI values |
| GET | `/api/v1/hr/recruitment/teaching/interviews/` | JWT (G0 provisioned) | Scheduled interviews for this recruiter |
| GET | `/api/v1/hr/recruitment/teaching/charts/funnel/` | JWT (G0 provisioned) | Scoped pipeline funnel data |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/hr/recruitment/teaching/kpis/` | `#kpi-bar` | `innerHTML` |
| Load candidate pipeline table | `load` | GET `/api/v1/hr/recruitment/teaching/candidates/` | `#pipeline-table` | `innerHTML` |
| Open recommendation drawer | `click` on Submit Recommendation | GET `/api/v1/hr/recruitment/teaching/candidates/{id}/` | `#recommendation-drawer` | `innerHTML` |
| Submit recommendation form | `click` on Confirm Submit | POST `/api/v1/hr/recruitment/recommendations/` | `#pipeline-table` | `innerHTML` |
| Filter candidates by stage | `change` on Resume Status filter | GET `/api/v1/hr/recruitment/teaching/candidates/?status=...` | `#pipeline-table` | `innerHTML` |
| Search candidates | `input` (300ms debounce) | GET `/api/v1/hr/recruitment/teaching/candidates/?q=...` | `#pipeline-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
