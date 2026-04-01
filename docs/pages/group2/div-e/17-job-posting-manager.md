# 17 — Job Posting Manager

- **URL:** `/group/hr/recruitment/job-postings/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Job Posting Manager is the entry point for the entire recruitment lifecycle. Every open position across all branches originates here as a formal job posting before any candidate applications can be received. This enforces structured hiring: no branch can begin informal recruitment without a Group HR–approved job posting, ensuring that all openings are tracked, budgeted, and aligned with the group's staffing plan.

A job posting captures the complete hiring intent: which branch needs the role, the role title and category (teaching or non-teaching), subject specialisation for teachers, class level (Primary/Middle/Secondary/Senior Secondary), the number of openings, required qualifications and minimum experience, the salary band from which the offer will be drawn, and the application deadline. The HR Manager also specifies which channels the posting should be published to: the EduForge Careers Portal (public-facing), integration placeholders for external job boards (Naukri, Indeed), and internal notice boards for in-house transfers. Once a posting is published, it is visible in the Recruitment Pipeline pages (18 and 19) where recruiters begin receiving and processing candidates.

This page prevents a common school-group HR failure: the same role being advertised at different salary bands at different branches, creating inequity and legal exposure. Because every posting references a grade band from the Grade Bands & Compensation Manager (page 15), salary consistency is enforced at the point of posting creation. If an HR Manager tries to post a role with a salary outside the band, the system blocks the submission and requires HR Director approval.

The postings table gives the HR Manager a complete operational view: how many applications have been received for each posting, how many days the position has been open, which postings are close to their deadline, and which have been filled. The "Average Days to Fill" KPI is a key efficiency metric — if positions are taking too long to fill, it signals that the sourcing strategy or salary bands need adjustment.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access + approval rights | Can create, edit, close; approves salary exceptions |
| Group HR Manager (42) | G3 | Full CRUD | Primary owner of this page |
| Group Recruiter — Teaching (43) | G0 | Read-only — teaching postings only | Cannot create or edit |
| Group Recruiter — Non-Teaching (44) | G0 | Read-only — non-teaching postings only | Cannot create or edit |
| Group Training & Dev Manager (45) | G2 | No access | — |
| Group Performance Review Officer (46) | G1 | No access | — |
| Group Staff Transfer Coordinator (47) | G3 | Read-only | Views postings relevant to transfer decisions |
| Group BGV Manager (48) | G3 | No access | — |
| Group BGV Executive (49) | G3 | No access | — |
| Group POCSO Coordinator (50) | G3 | No access | — |
| Group Disciplinary Committee Head (51) | G3 | No access | — |
| Group Employee Welfare Officer (52) | G3 | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Recruitment → Job Posting Manager`

### 3.2 Page Header
- Title: "Job Posting Manager"
- Subtitle: "Create and manage job openings across all branches."
- Primary CTA: "+ Create Job Posting" (HR Director / Manager)
- Secondary CTAs: "Export Postings Report" | "View Filled Positions Archive"

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Postings closing in ≤ 3 days | "[N] job posting(s) close within 3 days. Review applications now." | Red |
| Postings open > 60 days with 0 applications | "[N] posting(s) have been open for over 60 days with no applications. Consider revising." | Orange |
| Postings on hold > 30 days | "[N] posting(s) are On Hold for over 30 days. Please review or close." | Yellow |
| Salary exception awaiting HR Director approval | "[N] job posting(s) require salary band exception approval." | Orange |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Job Postings | Count with status = Active | Neutral blue | Filters table to Active |
| Applications Received Today | Count of applications submitted today | Green if > 0 | — |
| Postings Closing in 7 Days | Count with deadline ≤ 7 days | Red if > 0 | Filters table to closing soon |
| Filled Positions This Month | Count closed as Filled in current month | Green | Filters to Filled archive |
| Avg Days to Fill | Mean days from posting date to filled date (last 90 days) | Amber if > 45, Green if ≤ 30 | — |
| Total Applications (All Active) | Sum of applications across all active postings | Neutral | — |

---

## 5. Main Table — Job Postings

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Job Title | Text (link to view drawer) | Yes | Yes (search) |
| Branch | Text | Yes | Yes (dropdown) |
| Category | Chip (Teaching / Non-Teaching) | Yes | Yes |
| Openings | Integer | No | No |
| Applications | Integer (link to application list) | Yes | No |
| Status | Chip (Active / On Hold / Closed / Filled / Cancelled) | Yes | Yes |
| Posted Date | Date | Yes | Yes (date range) |
| Deadline | Date | Yes | Yes (date range) |
| Days Open | Integer (computed: today − posted date) | Yes | No |
| Salary Band | Text (Grade Code) | No | Yes (dropdown) |
| Actions | View Applications / Edit / Close / Cancel | No | No |

### 5.1 Filters
- Status: All | Active | On Hold | Closed | Filled | Cancelled
- Category: All | Teaching | Non-Teaching
- Branch: All branches (multi-select dropdown)
- Deadline: Next 7 Days | Next 30 Days | Past deadline | Custom range

### 5.2 Search
Full-text search on Job Title. Minimum 2 characters, 400ms debounce, HTMX live search.

### 5.3 Pagination
Server-side pagination, 20 records per page. First / Prev / Page N / Next / Last navigation. Record count displayed above table.

---

## 6. Drawers

### 6.1 Drawer: Create Job Posting
Fields: Job Title (text), Branch (dropdown, multi-select allowed for group-wide postings), Role Category (Teaching / Non-Teaching — radio), Subject (visible only if Teaching — dropdown), Class Level (Primary / Middle / Secondary / Sr. Secondary / All — multi-select), Number of Openings (integer, min 1), Qualifications Required (rich text / multiline textarea), Minimum Experience (years — numeric), Salary Band (dropdown from grade bands, Grade Code + range shown), Application Deadline (date picker, must be future date), Publish Channels (checkboxes: EduForge Careers Portal / Internal Notice Board / Job Board Placeholder), Job Description (rich textarea), Internal Notes (textarea, not visible on careers portal).
Validation: All required fields; deadline in future; openings ≥ 1; salary band selection required.
On Save: POST to API, row prepended to table, toast shown. If "Publish to Careers Portal" checked, posting becomes live immediately.

### 6.2 Drawer: View Applications for Posting
Shows list of all candidates who applied for this specific posting. Columns: Candidate Name, Applied Date, Current Stage in Pipeline, Recruiter Assigned, Actions (View Candidate → links to pipeline page). Pagination within drawer (10 per page). "Export Applications" button.

### 6.3 Drawer: Edit Posting
Available only for Active or On-Hold postings. All fields editable except Branch (immutable after creation — requires close + re-create). Change Reason required. If deadline extended, system re-notifies subscribed recruiters.
On Save: PATCH to API, row updated in place.

### 6.4 Modal: Close / Cancel Posting
Close = position filled or deadline passed. Cancel = posting withdrawn. Both require a Reason (dropdown + notes). Close prompts: "Were all openings filled? [Yes/Partially/No]". On Confirm: status updated, row chip changed, filled positions count incremented if Yes.

---

## 7. Charts

**Applications per Posting — Bar Chart:** horizontal bar chart showing application count per active job posting. Sorted by application count descending. Rendered via Chart.js. Toggle: "Show Chart / Hide". Positioned below the main table.

**Postings by Category — Donut:** small donut chart showing split between Teaching and Non-Teaching active postings. Rendered inline in a side panel next to the KPI bar.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Job posting created | "Job posting '[Title]' created and published." | Success | 4s |
| Job posting updated | "Job posting updated successfully." | Success | 4s |
| Posting closed — filled | "Posting '[Title]' marked as filled." | Success | 4s |
| Posting cancelled | "Job posting '[Title]' cancelled." | Info | 4s |
| Salary band exception flagged | "Salary exceeds band maximum. HR Director approval required before publishing." | Warning | 6s |
| Export downloaded | "Job postings report downloaded." | Success | 3s |
| Deadline past — auto-close | "Posting '[Title]' has passed its deadline and been auto-closed." | Info | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No job postings created | "No Job Postings Yet" | "Create your first job posting to begin the recruitment process." | Create Job Posting |
| Filter returns no results | "No Postings Match Filters" | "Try clearing your filters to see all postings." | Clear Filters |
| No applications for a posting | "No Applications Yet" | "This posting has not received any applications yet." | — |
| Filled archive empty | "No Filled Positions" | "Filled positions from closed postings will appear here." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI card skeletons (6) + table row skeletons (12) |
| Filter/search change | Table body row skeletons |
| View applications drawer | Drawer skeleton (candidate row skeletons) |
| Create/edit drawer open | Form field skeletons (8 fields) |
| Submit action | Button spinner + disabled state |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) / HR Manager (42) | Recruiter Teaching (43) | Recruiter Non-Teaching (44) |
|---|---|---|---|
| Create Job Posting button | Visible + enabled | Hidden | Hidden |
| Edit action | Visible + enabled | Hidden | Hidden |
| Close / Cancel action | Visible + enabled | Hidden | Hidden |
| View Applications action | Visible | Visible (teaching only) | Visible (non-teaching only) |
| Export Report | Visible | Hidden | Hidden |
| Charts | Visible | Visible (read-only) | Visible (read-only) |
| Salary Band field in form | Visible | N/A | N/A |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/recruitment/job-postings/` | JWT | List all job postings (paginated) |
| POST | `/api/v1/hr/recruitment/job-postings/` | JWT | Create new job posting |
| GET | `/api/v1/hr/recruitment/job-postings/{id}/` | JWT | Fetch single posting |
| PATCH | `/api/v1/hr/recruitment/job-postings/{id}/` | JWT | Update posting |
| PATCH | `/api/v1/hr/recruitment/job-postings/{id}/close/` | JWT | Close posting |
| PATCH | `/api/v1/hr/recruitment/job-postings/{id}/cancel/` | JWT | Cancel posting |
| GET | `/api/v1/hr/recruitment/job-postings/{id}/applications/` | JWT | List applications for posting |
| GET | `/api/v1/hr/recruitment/job-postings/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/recruitment/job-postings/chart/` | JWT | Applications per posting chart data |
| GET | `/api/v1/hr/recruitment/job-postings/export/` | JWT | Export postings report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/recruitment/job-postings/?q={val}` | `#postings-table-body` | innerHTML |
| Filter apply | change | GET `/api/v1/hr/recruitment/job-postings/?status={}&category={}&branch={}` | `#postings-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/recruitment/job-postings/?page={n}` | `#postings-table-body` | innerHTML |
| Create drawer open | click | GET `/group/hr/recruitment/job-postings/create/drawer/` | `#drawer-container` | innerHTML |
| View applications drawer | click | GET `/group/hr/recruitment/job-postings/{id}/applications/drawer/` | `#drawer-container` | innerHTML |
| Edit drawer open | click | GET `/group/hr/recruitment/job-postings/{id}/edit/drawer/` | `#drawer-container` | innerHTML |
| Close modal | click | GET `/group/hr/recruitment/job-postings/{id}/close/modal/` | `#modal-container` | innerHTML |
| Create submit | submit | POST `/api/v1/hr/recruitment/job-postings/` | `#postings-table-body` | afterbegin |
| Edit submit | submit | PATCH `/api/v1/hr/recruitment/job-postings/{id}/` | `#posting-row-{id}` | outerHTML |
| Chart toggle | click | GET `/group/hr/recruitment/job-postings/chart/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
