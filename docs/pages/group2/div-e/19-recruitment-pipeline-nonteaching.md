# 19 — Recruitment Pipeline — Non-Teaching Staff

- **URL:** `/group/hr/recruitment/pipeline/nonteaching/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Recruitment Pipeline — Non-Teaching Staff page manages the end-to-end recruitment process for all non-teaching roles across the group's branches. Non-teaching roles are operationally critical: a school without a warden, security guards, or support staff cannot function safely. This page ensures that all non-teaching vacancies are filled in a structured, compliant manner, with the same disciplined tracking that applies to teaching recruitment.

Non-teaching roles span a wide operational spectrum: Warden (Boys/Girls) for residential facilities, Office Assistant, Security Guard, Driver, Cook/Mess Staff, Electrician, Plumber, Lab Assistant, Librarian, and Counsellor. Each role category has distinct verification requirements that shape the pipeline stages. Drivers require a valid driving licence and a practical driving test. Cooks undergo a food preparation skills test and kitchen hygiene assessment. Security Guards require police verification before joining. Hostel Wardens require background checks and POCSO clearance because of their proximity to minor students. These role-specific requirements are built into the pipeline as mandatory stage gates.

The non-teaching pipeline is simpler than the teaching pipeline — there is no Demo Class stage — but it adds a BGV Check stage before an offer is made. This is because many non-teaching roles involve physical access to school premises, residential facilities, or financial assets. An unverified security guard or driver poses a direct safety risk. The BGV Check stage triggers the BGV module (pages 8/9) and blocks the pipeline from moving to "Offer Sent" until BGV status is at least "In Progress." For roles requiring police verification (Security, Driver), BGV must be "Cleared" before offer.

The Group Recruiter — Non-Teaching (Role 44, G0) manages day-to-day candidate movement through stages but cannot access salary information, close postings, or see other recruiters' pipelines. The Group HR Manager has full oversight across all non-teaching recruitment. This division of responsibility allows recruiters to operate efficiently without accessing sensitive compensation and policy data.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access — all candidates | Can override stage, approve exceptions |
| Group HR Manager (42) | G3 | Full access — all candidates | Primary owner |
| Group Recruiter — Teaching (43) | G0 | No access | See page 18 |
| Group Recruiter — Non-Teaching (44) | G0 | Assigned candidates only | Limited stage actions; no salary info |
| Group Training & Dev Manager (45) | G2 | No access | — |
| Group Performance Review Officer (46) | G1 | No access | — |
| Group Staff Transfer Coordinator (47) | G3 | No access | — |
| Group BGV Manager (48) | G3 | Read-only — BGV stage candidates | Can update BGV status for candidates in BGV Check stage |
| Group BGV Executive (49) | G3 | Read-only — BGV stage candidates | Same as BGV Manager, scoped to their assigned cases |
| Group POCSO Coordinator (50) | G3 | No access | — |
| Group Disciplinary Committee Head (51) | G3 | No access | — |
| Group Employee Welfare Officer (52) | G3 | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Recruitment → Non-Teaching Staff Pipeline`

### 3.2 Page Header
- Title: "Recruitment Pipeline — Non-Teaching Staff"
- Subtitle: "Track all non-teaching candidates from application to joining."
- View toggle: "Table View" | "Kanban View"
- Primary CTA: "+ Add Candidate Manually" (HR Director / Manager only)
- Secondary CTAs: "Export Pipeline" | "Reassign Recruiter"

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Candidates in BGV Check stage with BGV not yet initiated | "[N] candidate(s) in BGV Check stage have no BGV record. Initiate BGV immediately." | Red |
| Roles requiring police verification with BGV not cleared | "[N] candidate(s) for security/driver roles have not cleared police verification." | Red |
| Candidates with overdue next action | "[N] candidates have overdue next actions." | Orange |
| Candidates stalled > 30 days | "[N] candidates have not progressed in over 30 days." | Yellow |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Applicants | All candidates ever entered | Neutral blue | — |
| Currently In Pipeline | Active (excl. Joined / Rejected / Declined) | Neutral | Filters to active |
| Interviews This Week | Count with interview date in current week | Green if confirmed, Amber if pending | Filters to Interview Scheduled |
| BGV Check Pending | Count in BGV Check stage or BGV not yet cleared | Red if > 0 | Filters to BGV stage |
| Offers Pending | Count in Offer Sent stage | Orange if > 5 | Filters to Offer Sent |
| Time-to-Hire (Avg Days) | Mean days from Applied to Joined (last 90 days) | Amber if > 30, Green if ≤ 21 | — |

---

## 5. Main Table — Non-Teaching Pipeline Candidates

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Name | Text (link to candidate drawer) | Yes | Yes (search) |
| Applied Role | Text | Yes | Yes (dropdown) |
| Role Category | Chip (Warden / Security / Support / etc.) | Yes | Yes |
| Branch | Text | Yes | Yes (dropdown) |
| Stage | Chip (colour-coded per stage) | Yes | Yes (multi-select) |
| Recruiter | Text | Yes | Yes (dropdown) |
| Applied Date | Date | Yes | Yes (date range) |
| Days in Pipeline | Integer | Yes | Yes (> N filter) |
| BGV Status | Chip (Not Initiated / In Progress / Cleared / Failed) | No | Yes |
| Next Action | Text + date | Yes | Yes (overdue toggle) |
| Actions | Move Stage / Schedule Interview / BGV / Reject | No | No |

### 5.1 Filters
- Stage: All | Applied | Screened | Interview Scheduled | Interviewed | BGV Check | Offer Sent | Joined | Declined | Rejected
- Role Category: All | Warden | Security Guard | Driver | Cook | Office Assistant | Lab Assistant | Librarian | Counsellor | Other
- Branch: All branches (multi-select)
- BGV Status: All | Not Initiated | In Progress | Cleared | Failed
- Recruiter: All / specific (HR Manager/Director only)
- Days in Pipeline: Any | > 7 | > 14 | > 30

### 5.2 Search
Search by candidate name or email. Minimum 2 characters, 400ms debounce, HTMX live.

### 5.3 Pagination
Server-side pagination, 25 records per page. First / Prev / Page N / Next / Last. Total count shown.

---

## 6. Drawers

### 6.1 Drawer: Candidate Profile (View)
Tabs: Overview | Application | Skills Assessment | BGV | History.
Overview: Name, Photo, Phone, Email, Applied Role, Role Category, Branch, Stage, Recruiter.
Application: CV / documents, application answers, licence/certificate uploads if applicable.
Skills Assessment: Practical test result (Pass/Fail), test date, assessor name, notes (Driver: driving test; Cook: food test; others: general skills assessment if applicable).
BGV: BGV status, components verified, timeline (pulls from BGV module).
History: Full stage-change timeline.

### 6.2 Drawer: Move Stage
Dropdown: target stage selection. If moving to "BGV Check": pre-checks BGV module — if no BGV record exists, shows warning and prompt to initiate BGV before proceeding. For roles with mandatory police verification (Security Guard, Driver), system blocks move to "Offer Sent" if BGV not Cleared. If moving to "Interview Scheduled": date/time picker + interviewer assignment + notification. Stage change notes (optional).
On Submit: PATCH stage, history entry created, notifications sent.

### 6.3 Drawer: Add Candidate Manually
Fields: Full Name, Email, Phone, Applied Role (dropdown from active non-teaching postings), Role Category (auto-populated), Branch Preference, Source (Walk-in / Job Board / Referral / Internal), Documents uploaded (CV, ID proof, certificates), Practical Test Required (Yes/No — auto-suggested from role category), Notes.
On Save: candidate created in Applied stage.

### 6.4 Modal: Reject Candidate
Reason: Under-qualified / Failed Skills Test / Failed BGV / Failed Interview / Offer Declined / No Response / Other. Notes field. Confirm / Cancel.
On Confirm: stage → Rejected, record archived, candidate notification queued.

---

## 7. Charts

**Pipeline Funnel Chart** — vertical funnel showing candidate count per stage from Applied to Joined. Stage drop-off percentages displayed at each step. Colour: green for progress stages, amber for BGV/offer stages. Toggle: "Show Funnel / Hide". Positioned below the table.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Candidate stage moved | "Candidate moved to [Stage]." | Success | 4s |
| BGV initiated from pipeline | "BGV initiated for [Candidate Name]. BGV Manager notified." | Success | 5s |
| Practical test recorded | "Skills assessment result saved for [Candidate Name]." | Success | 4s |
| Candidate manually added | "Candidate [Name] added to non-teaching pipeline." | Success | 4s |
| BGV block — offer prevented | "Cannot proceed to Offer Sent: BGV not cleared for this role." | Error | 6s |
| Candidate rejected | "Candidate [Name] rejected." | Info | 4s |
| Pipeline exported | "Non-teaching pipeline report downloaded." | Success | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No candidates in pipeline | "No Candidates Yet" | "Publish non-teaching job postings to begin receiving applications." | View Job Postings |
| Filter returns no results | "No Matching Candidates" | "Adjust filters to find candidates in the pipeline." | Clear Filters |
| Role category filter — no matches | "No Candidates for This Role" | "No candidates have applied for the selected role category." | — |
| BGV filter — none pending | "No BGV Actions Pending" | "All candidates requiring BGV have been processed." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI card skeletons (6) + table row skeletons (15) |
| Filter change | Table body row skeletons |
| Candidate drawer open | Drawer tab + content skeletons |
| Stage move submit | Row shimmer + button spinner |
| Kanban view switch | Full kanban column skeletons |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) / Manager (42) | Recruiter Non-Teaching (44) | BGV Roles (48, 49) |
|---|---|---|---|
| All candidates visible | Yes | Assigned only | BGV stage candidates only |
| Add Candidate Manually | Visible + enabled | Hidden | Hidden |
| Recruiter filter / Reassign | Visible | Hidden | Hidden |
| Move Stage (full options) | Full | Applied → Screened → Interview Scheduled only | BGV status update only |
| BGV Initiate action | Visible | Hidden | Visible |
| Reject action | Visible | Hidden | Hidden |
| Offer Sent action | Visible | Hidden | Hidden |
| Export Pipeline | Visible | Hidden | Hidden |
| Compensation in drawer | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/recruitment/pipeline/nonteaching/` | JWT | List non-teaching pipeline candidates |
| POST | `/api/v1/hr/recruitment/pipeline/nonteaching/` | JWT | Add candidate manually |
| GET | `/api/v1/hr/recruitment/pipeline/nonteaching/{id}/` | JWT | Fetch candidate detail |
| PATCH | `/api/v1/hr/recruitment/pipeline/nonteaching/{id}/stage/` | JWT | Move candidate stage |
| PATCH | `/api/v1/hr/recruitment/pipeline/nonteaching/{id}/reject/` | JWT | Reject candidate |
| PATCH | `/api/v1/hr/recruitment/pipeline/nonteaching/{id}/bgv/initiate/` | JWT | Initiate BGV for candidate |
| GET | `/api/v1/hr/recruitment/pipeline/nonteaching/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/recruitment/pipeline/nonteaching/chart/` | JWT | Funnel chart data |
| GET | `/api/v1/hr/recruitment/pipeline/nonteaching/export/` | JWT | Export pipeline report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/recruitment/pipeline/nonteaching/?q={val}` | `#pipeline-table-body` | innerHTML |
| Stage filter | change | GET `/api/v1/hr/recruitment/pipeline/nonteaching/?stage={val}` | `#pipeline-table-body` | innerHTML |
| BGV filter | change | GET `/api/v1/hr/recruitment/pipeline/nonteaching/?bgv_status={val}` | `#pipeline-table-body` | innerHTML |
| Multi-filter | change | GET `/api/v1/hr/recruitment/pipeline/nonteaching/?category={}&branch={}` | `#pipeline-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/recruitment/pipeline/nonteaching/?page={n}` | `#pipeline-table-body` | innerHTML |
| Candidate drawer open | click | GET `/group/hr/recruitment/pipeline/nonteaching/{id}/drawer/` | `#drawer-container` | innerHTML |
| Move Stage drawer | click | GET `/group/hr/recruitment/pipeline/nonteaching/{id}/stage/drawer/` | `#drawer-container` | innerHTML |
| Add Candidate drawer | click | GET `/group/hr/recruitment/pipeline/nonteaching/add/drawer/` | `#drawer-container` | innerHTML |
| Stage move submit | submit | PATCH `/api/v1/hr/recruitment/pipeline/nonteaching/{id}/stage/` | `#candidate-row-{id}` | outerHTML |
| Reject modal | click | GET `/group/hr/recruitment/pipeline/nonteaching/{id}/reject/modal/` | `#modal-container` | innerHTML |
| Funnel chart toggle | click | GET `/group/hr/recruitment/pipeline/nonteaching/chart/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
