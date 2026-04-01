# 18 — Recruitment Pipeline — Teaching Staff

- **URL:** `/group/hr/recruitment/pipeline/teaching/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Recruitment Pipeline — Teaching Staff page is the operational centre for managing all teaching staff candidates from application to joining across the entire group. Every candidate who applies for a teaching role — whether through the EduForge Careers Portal, a job board, or an internal referral — enters this pipeline and is tracked through every stage until they join or withdraw. This page exists because untracked candidate pipelines are the most common reason school groups lose quality teachers: a candidate is shortlisted, then forgotten, then accepts another offer.

The pipeline follows a clearly defined stage sequence: Applied → Resume Screened → Shortlisted → Demo Class Scheduled → Demo Evaluated → Interview Scheduled → Interviewed → Offer Sent → Offer Accepted → Joined. Terminal stages include Offer Declined and Rejected. The Demo Class stage is unique to teaching recruitment — a candidate must deliver a demonstration lesson at the target branch before an interview is scheduled. This requires coordination with the branch principal, who must confirm a date and class slot. The HR Manager oversees this coordination through this page.

Each candidate record in the pipeline carries: full name, applied role, subject specialisation, target branch, current stage, days in pipeline (a key performance indicator for recruiter efficiency), the recruiter assigned to the candidate, and the next action due date. Candidates whose next action is overdue (past due date) are surfaced prominently with red highlighting. This prevents candidates from stagnating in a stage because a recruiter forgot to follow up.

Access is tiered: the Group HR Manager sees all candidates across all postings, branches, and recruiters. The Group Recruiter — Teaching (Role 43, G0) sees only candidates assigned to them — they cannot see other recruiters' pipelines, bulk-move candidates, or access compensation information. This scoping prevents recruiter cross-contamination and protects candidate data confidentiality while still allowing recruiters to manage their workload effectively.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access — all candidates | Can override stage, reassign recruiter |
| Group HR Manager (42) | G3 | Full access — all candidates | Primary owner of pipeline |
| Group Recruiter — Teaching (43) | G0 | Assigned candidates only | Cannot see other recruiters' candidates; limited actions |
| Group Recruiter — Non-Teaching (44) | G0 | No access | See page 19 |
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
`Group HR → Recruitment → Teaching Staff Pipeline`

### 3.2 Page Header
- Title: "Recruitment Pipeline — Teaching Staff"
- Subtitle: "Track all teaching candidates from application to joining."
- View toggle: "Table View" | "Kanban View" (Kanban is read-only for G0 roles)
- Primary CTA: "+ Add Candidate Manually" (HR Director / Manager only)
- Secondary CTAs: "Export Pipeline" | "Reassign Recruiter" (bulk action)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Candidates with overdue next action > 5 | "[N] candidates have overdue actions in the pipeline. Review immediately." | Red |
| Demo classes pending principal confirmation > 3 | "[N] demo class slots are awaiting branch principal confirmation." | Orange |
| Candidates in pipeline > 45 days with no stage change | "[N] candidates appear stalled (>45 days without stage movement)." | Yellow |
| Offer sent but no response > 7 days | "[N] offer(s) have not received a response in over 7 days." | Orange |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Applicants | All candidates in pipeline + joined + declined | Neutral blue | — |
| Currently In Pipeline | Active candidates (Applied → Offer Accepted, excl. terminal) | Neutral | Filters to active |
| Demo Scheduled This Week | Count with demo date in current week | Green if confirmed, Amber if pending | Filters to Demo stage |
| Offers Pending | Count in Offer Sent stage | Orange if > 10 | Filters to Offer Sent |
| Offers Accepted | Count in Offer Accepted stage (this month) | Green | — |
| Conversion Rate | (Joined / Total Applicants) × 100 in last 90 days (%) | Amber if < 10%, Green if ≥ 15% | — |

---

## 5. Main Table — Teaching Pipeline Candidates

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Name | Text (link to candidate drawer) | Yes | Yes (search) |
| Applied Role | Text | Yes | Yes (dropdown) |
| Subject | Text | Yes | Yes (dropdown) |
| Branch | Text | Yes | Yes (dropdown) |
| Stage | Chip (colour-coded per stage) | Yes | Yes (multi-select) |
| Recruiter | Text | Yes | Yes (dropdown) |
| Applied Date | Date | Yes | Yes (date range) |
| Days in Pipeline | Integer | Yes | Yes (> N filter) |
| Next Action | Text (action label + date) | Yes | Yes (overdue filter) |
| Actions | Move Stage / Schedule Demo / Schedule Interview / Reject | No | No |

### 5.1 Filters
- Stage: All | Applied | Screened | Shortlisted | Demo Scheduled | Demo Evaluated | Interview Scheduled | Interviewed | Offer Sent | Offer Accepted | Joined | Declined | Rejected
- Branch: All branches (multi-select)
- Subject: All subjects (multi-select dropdown)
- Recruiter: All recruiters / specific recruiter (HR Manager only)
- Days in Pipeline: Any | > 7 | > 14 | > 30 | > 45
- Overdue Actions: Toggle (shows only candidates with past-due next actions)

### 5.2 Search
Search by candidate name or email. Minimum 2 characters, 400ms debounce.

### 5.3 Pagination
Server-side pagination, 25 records per page. Navigation controls with page count. Total candidates displayed above table.

---

## 6. Drawers

### 6.1 Drawer: Candidate Profile (View)
Tabs within drawer: Overview | Application | Assessment Notes | History.
Overview: Name, Photo, Phone, Email, Current Employer, Applied Role, Subject, Branch, Recruiter, Applied Date, Current Stage.
Application: CV download link, cover letter, application answers.
Assessment Notes: Demo evaluation score (if applicable), interview panel notes, individual assessor comments.
History: Full stage-by-stage timeline with timestamps and action-taker names.

### 6.2 Drawer: Move Stage
Triggered by "Move Stage" action. Dropdown: select target stage. If moving to "Demo Scheduled": date picker + branch confirmation request checkbox + class details field. If moving to "Interview Scheduled": links to Interview Scheduler (page 20). If moving to "Offer Sent": links to Offer Letter Manager (page 21). Stage change reason (optional textarea).
On Submit: PATCH stage, timeline entry created, recruiter notified.

### 6.3 Drawer: Add Candidate Manually
Fields: Full Name, Email, Phone, Applied Role (dropdown from active postings), Subject, Branch Preference, Source (Walk-in / Referral / Job Board / Internal), CV Upload (PDF, max 5 MB), Notes.
On Save: Candidate created in Applied stage, assigned to recruiter (auto or manual selection).

### 6.4 Modal: Reject Candidate
Reason dropdown: Under-qualified / Failed Demo / Failed Interview / No Response / Offer Declined / Other. Notes field. Confirmation prompt.
On Confirm: Stage → Rejected, candidate notified via system email, record archived.

---

## 7. Charts

**Pipeline Funnel Chart** — vertical funnel showing candidate count per stage, narrowing from Applied to Joined. Rendered via Chart.js. Shows drop-off at each stage as a percentage. Toggle: "Show Funnel / Hide". Positioned below the table.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Candidate stage moved | "Candidate moved to [Stage]." | Success | 4s |
| Demo class scheduled | "Demo class scheduled for [Date]. Principal notified." | Success | 5s |
| Candidate manually added | "Candidate [Name] added to pipeline." | Success | 4s |
| Candidate rejected | "Candidate [Name] marked as rejected." | Info | 4s |
| Recruiter reassigned | "Recruiter reassigned for [N] candidate(s)." | Success | 4s |
| Offer send triggered | "Candidate forwarded to Offer Letter Manager." | Info | 4s |
| Stale pipeline warning dismissed | "Pipeline alert dismissed for [N] candidates." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No candidates in pipeline | "No Candidates Yet" | "Active job postings will receive applications from the Careers Portal." | View Job Postings |
| Filter returns no results | "No Matching Candidates" | "Clear your filters to see all candidates in the pipeline." | Clear Filters |
| Recruiter view — no assigned candidates | "No Candidates Assigned" | "You have no candidates currently assigned to you." | — |
| Stage filter — no candidates in stage | "No Candidates in This Stage" | "No candidates are currently in the [Stage] stage." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI skeletons (6) + table row skeletons (15) |
| Filter / stage filter change | Table body skeleton |
| Candidate drawer open | Drawer skeleton (tabs + content) |
| Stage move submit | Button spinner + row shimmer update |
| Kanban view switch | Full kanban skeleton (stage columns) |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) / Manager (42) | Recruiter Teaching (43) |
|---|---|---|
| All candidates visible | Yes | Assigned candidates only |
| Add Candidate Manually | Visible + enabled | Hidden |
| Recruiter filter dropdown | Visible + enabled | Hidden |
| Reassign Recruiter bulk action | Visible + enabled | Hidden |
| Export Pipeline | Visible | Hidden |
| Move Stage action | Full stage options | Limited (Applied → Screened → Shortlisted only) |
| Reject action | Visible | Hidden |
| Offer Sent action | Visible | Hidden |
| Compensation fields in drawer | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/recruitment/pipeline/teaching/` | JWT | List teaching pipeline candidates |
| POST | `/api/v1/hr/recruitment/pipeline/teaching/` | JWT | Add candidate manually |
| GET | `/api/v1/hr/recruitment/pipeline/teaching/{id}/` | JWT | Fetch candidate detail |
| PATCH | `/api/v1/hr/recruitment/pipeline/teaching/{id}/stage/` | JWT | Move candidate to new stage |
| PATCH | `/api/v1/hr/recruitment/pipeline/teaching/{id}/reject/` | JWT | Reject candidate |
| PATCH | `/api/v1/hr/recruitment/pipeline/teaching/{id}/recruiter/` | JWT | Reassign recruiter |
| GET | `/api/v1/hr/recruitment/pipeline/teaching/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/recruitment/pipeline/teaching/chart/` | JWT | Funnel chart data |
| GET | `/api/v1/hr/recruitment/pipeline/teaching/export/` | JWT | Export pipeline report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/recruitment/pipeline/teaching/?q={val}` | `#pipeline-table-body` | innerHTML |
| Stage filter | change | GET `/api/v1/hr/recruitment/pipeline/teaching/?stage={val}` | `#pipeline-table-body` | innerHTML |
| Multi-filter apply | change | GET `/api/v1/hr/recruitment/pipeline/teaching/?branch={}&subject={}&recruiter={}` | `#pipeline-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/recruitment/pipeline/teaching/?page={n}` | `#pipeline-table-body` | innerHTML |
| Candidate drawer open | click | GET `/group/hr/recruitment/pipeline/teaching/{id}/drawer/` | `#drawer-container` | innerHTML |
| Move Stage drawer | click | GET `/group/hr/recruitment/pipeline/teaching/{id}/stage/drawer/` | `#drawer-container` | innerHTML |
| Add Candidate drawer | click | GET `/group/hr/recruitment/pipeline/teaching/add/drawer/` | `#drawer-container` | innerHTML |
| Stage move submit | submit | PATCH `/api/v1/hr/recruitment/pipeline/teaching/{id}/stage/` | `#candidate-row-{id}` | outerHTML |
| Reject modal | click | GET `/group/hr/recruitment/pipeline/teaching/{id}/reject/modal/` | `#modal-container` | innerHTML |
| Kanban view | click | GET `/group/hr/recruitment/pipeline/teaching/kanban/` | `#main-content` | innerHTML |
| Funnel chart toggle | click | GET `/group/hr/recruitment/pipeline/teaching/chart/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
