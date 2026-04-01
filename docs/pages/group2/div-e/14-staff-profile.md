# 14 — Staff Profile — Individual Record

- **URL:** `/group/hr/staff/{staff_id}/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group HR Director (Role 41, G3), Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Staff Profile page is the single authoritative record for every individual staff member within the group. It consolidates all HR-relevant information into one place: personal details, employment history, current branch and role assignment, qualifications, uploaded compliance documents (Aadhaar, PAN, degree certificates, experience letters), BGV status with a full timeline, POCSO training completion record, appraisal history, transfer history, disciplinary notes, leave balance (read-only pulled from the Leave module), and insurance/ESI/PF details. Any HR role navigating from the Staff Directory or search reaches this page for deep inspection.

This page is the canonical "single staff truth" — every other HR module links back to or forwards to this record. If a staff member's BGV is pending, the BGV tab surfaces it here. If a disciplinary notice was issued, the Disciplinary tab logs it. If a transfer was requested, the Transfers tab timestamps the full chain. This prevents information from being siloed across separate modules and ensures every HR decision is traceable to a named individual with a full audit log.

The page protects against compliance failures by surfacing incomplete mandatory records immediately. If POCSO training is not completed and the staff member is assigned a student-contact role, a persistent red alert banner appears at the top of the profile. If a document upload is missing, the Documents tab flags it with a warning icon. These proactive surface-level alerts reduce the risk of non-compliant staff being placed in roles before completing mandatory requirements.

Access to this page is tiered: Group HR Director and Group HR Manager can edit core employment fields; the BGV Manager and BGV Executive can update only the BGV tab fields; the POCSO Coordinator can update only the POCSO tab; the Performance Review Officer can view the Appraisals tab read-only; other roles have read-only access to tabs within their functional scope. All edits are timestamped and attributed to the editing user for full auditability.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full edit — all tabs | Can edit core profile, view all tabs |
| Group HR Manager (42) | G3 | Full edit — all tabs | Same as Director for profile fields |
| Group Recruiter — Teaching (43) | G0 | No access | Redirected to pipeline |
| Group Recruiter — Non-Teaching (44) | G0 | No access | Redirected to pipeline |
| Group Training & Dev Manager (45) | G2 | Read — Overview, POCSO, Appraisals | Cannot edit core fields |
| Group Performance Review Officer (46) | G1 | Read — Appraisals tab only | No edit access |
| Group Staff Transfer Coordinator (47) | G3 | Read — Overview, Transfers tab | Can create transfer requests |
| Group BGV Manager (48) | G3 | Edit — BGV tab only | Core fields read-only |
| Group BGV Executive (49) | G3 | Edit — BGV tab only | Core fields read-only |
| Group POCSO Coordinator (50) | G3 | Edit — POCSO tab only | Core fields read-only |
| Group Disciplinary Committee Head (51) | G3 | Read — Disciplinary tab, full view | Can add disciplinary notes |
| Group Employee Welfare Officer (52) | G3 | Read — Overview, Insurance tab | Cannot edit employment fields |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Staff Directory → [Staff Full Name] (Staff ID)`

### 3.2 Page Header
- Staff name (large), Staff ID badge, Department chip, Branch chip
- Profile photo placeholder with upload button (HR Director/Manager only)
- Status badge: Active / On Leave / Suspended / Exited
- Quick action buttons: Edit Profile | Download Staff Card | Initiate BGV | Assign Training | Transfer Request | Show-Cause Notice
- Tab bar: Overview | Documents | BGV | POCSO | Appraisals | Transfers | Disciplinary | Insurance

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| POCSO training not completed, staff in student-contact role | "POCSO training incomplete — staff must not have student contact until completed." | Red / Critical |
| BGV not initiated within 30 days of joining | "BGV not yet initiated — compliance deadline breached." | Red |
| Any mandatory document missing | "One or more mandatory documents are missing. Upload required." | Orange |
| Contract expired or missing | "No active contract on file for this staff member." | Orange |
| Probation review overdue | "Probation review is overdue. Branch Principal has not submitted." | Yellow |
| Staff exited — profile is read-only | "This staff member has exited. Profile is archived and read-only." | Blue / Info |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Documents on File | Count of uploaded docs / total required | Red if any missing, Green if complete | Scrolls to Documents tab |
| BGV Status | Current BGV stage label | Red = Not Initiated, Amber = In Progress, Green = Cleared | Opens BGV tab |
| POCSO Status | Completed / Not Completed | Red if not completed + student-contact role, Green if done | Opens POCSO tab |
| CPD Hours (YTD) | Hours completed this academic year | Amber if < 10, Green if ≥ 20 | Opens Appraisals tab |
| Days Since Last Appraisal | Integer days | Red if > 365, Green if ≤ 365 | Opens Appraisals tab |
| Leave Balance | Remaining annual leave days (from Leave module) | Informational blue | External link to Leave module |

---

## 5. Main Table — Tab: Overview (Employment Details)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Field Label | Static text | No | No |
| Field Value | Editable (HR Dir / Mgr) or read-only text | No | No |

### 5.1 Filters
Not applicable — this is a single-record profile page, not a list.

### 5.2 Search
Not applicable at the profile level; search occurs at the Staff Directory page (13).

### 5.3 Pagination
Not applicable for profile view. Tab content with long history (Appraisals, Transfers, Disciplinary) uses server-side pagination within each tab panel (10 records per page, standard nav controls).

---

## 6. Drawers

### 6.1 Drawer: Edit Profile (Core Fields)
Triggered by "Edit Profile" button (HR Director / Manager only).
Fields: Full Name, Date of Birth, Gender, Nationality, Personal Email, Emergency Contact Name, Emergency Contact Number, Permanent Address, Current Address, Highest Qualification, Specialisation, Total Experience (years), Group Experience (years), Current Role Title, Department, Branch Assignment, Employee Category (Permanent / Contract / Visiting), Date of Joining, Reporting Manager.
Validation: All required fields must be non-empty; DoB must be at least 18 years ago; experience fields numeric; email format validated.
On Save: HTMX patch to API, toast "Profile updated", drawer closes, page header refreshes.

### 6.2 Drawer: View Document
Triggered from Documents tab — "View" action per document.
Displays: Document type label, Upload date, Uploaded by, Expiry date (if applicable), inline PDF/image preview or download link.
No edit inside this drawer; editing is done via Upload action.

### 6.3 Drawer: Initiate BGV
Triggered by "Initiate BGV" quick action button.
Fields: BGV Agency (dropdown from configured agencies), Priority Level (Normal/Urgent), Components to verify (Education, Employment History, Criminal Record, Address, Reference Check — checkboxes), Internal Notes.
On Submit: POST to BGV API, creates BGV record, sets BGV tab status to "Initiated", sends notification to BGV Manager.

### 6.4 Modal: Show-Cause Notice
Triggered by "Show-Cause Notice" quick action.
Fields: Incident Date, Incident Description (textarea), Basis for Notice (dropdown: Attendance / Misconduct / Policy Violation / Academic / Other), Deadline to Respond (date picker, default 7 days).
Confirmation prompt: "Are you sure you want to issue a Show-Cause Notice to [Name]? This action will be logged."
On Confirm: POST to disciplinary API, creates notice record in Disciplinary tab, sends system notification to Disciplinary Committee Head.

---

## 7. Charts

No charts on this page — it is a pure profile/record view. Visual status indicators (coloured chips, progress rings on the KPI bar) convey status without chart overhead.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Profile saved | "Staff profile updated successfully." | Success | 4s |
| Document uploaded | "Document uploaded and saved." | Success | 4s |
| Document upload failed (size/type) | "Upload failed — max 5 MB, PDF/JPG/PNG only." | Error | 6s |
| BGV initiated | "BGV initiated and sent to BGV Manager." | Success | 4s |
| Show-Cause Notice issued | "Show-Cause Notice recorded and notification sent." | Warning | 5s |
| Transfer request created | "Transfer request submitted." | Success | 4s |
| Training assigned | "Training program assigned to staff member." | Success | 4s |
| Unauthorised edit attempt | "You do not have permission to edit this section." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No documents uploaded | "No Documents on File" | "Upload mandatory documents to maintain compliance." | Upload Document |
| BGV never initiated | "BGV Not Started" | "Initiate background verification for this staff member." | Initiate BGV |
| No appraisal history | "No Appraisals Recorded" | "No formal appraisal has been conducted for this staff member." | — |
| No transfer history | "No Transfers" | "This staff member has not been transferred." | — |
| No disciplinary records | "Clean Record" | "No disciplinary actions have been recorded." | — |
| POCSO tab — no record | "POCSO Not Completed" | "POCSO training has not been scheduled or completed for this staff member." | Assign Training |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: header skeleton + 6 KPI card skeletons + tab skeleton |
| Tab switch | Tab content area skeleton (3 row skeletons) |
| Drawer open | Drawer panel with form field skeletons |
| Document preview load | Inline spinner in preview pane |
| Save / Submit action | Button spinner, button disabled until response |

---

## 11. Role-Based UI Visibility

| Element | HR Director / Manager (41, 42) | BGV / POCSO / Disciplinary Roles (48–51) | Read-Only Roles (45, 46, 47, 52) |
|---|---|---|---|
| Edit Profile button | Visible + enabled | Hidden | Hidden |
| Download Staff Card | Visible | Visible | Visible |
| Initiate BGV button | Visible | Visible (BGV roles) | Hidden |
| Show-Cause Notice button | Visible | Hidden | Hidden |
| Transfer Request button | Visible | Hidden | Visible (47 only) |
| Assign Training button | Visible | Hidden | Visible (45 only) |
| All tab content | Full access | Scoped to role tab | Read-only |
| Document upload control | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/staff/{staff_id}/` | JWT | Fetch full staff profile |
| PATCH | `/api/v1/hr/staff/{staff_id}/` | JWT | Update core profile fields |
| GET | `/api/v1/hr/staff/{staff_id}/documents/` | JWT | List documents for staff |
| POST | `/api/v1/hr/staff/{staff_id}/documents/` | JWT | Upload new document |
| GET | `/api/v1/hr/staff/{staff_id}/bgv/` | JWT | Fetch BGV record and timeline |
| POST | `/api/v1/hr/staff/{staff_id}/bgv/initiate/` | JWT | Initiate BGV process |
| GET | `/api/v1/hr/staff/{staff_id}/pocso/` | JWT | Fetch POCSO status |
| PATCH | `/api/v1/hr/staff/{staff_id}/pocso/` | JWT | Update POCSO completion |
| GET | `/api/v1/hr/staff/{staff_id}/appraisals/` | JWT | List appraisal records |
| GET | `/api/v1/hr/staff/{staff_id}/transfers/` | JWT | List transfer history |
| POST | `/api/v1/hr/staff/{staff_id}/transfers/` | JWT | Create transfer request |
| GET | `/api/v1/hr/staff/{staff_id}/disciplinary/` | JWT | List disciplinary records |
| POST | `/api/v1/hr/staff/{staff_id}/disciplinary/notice/` | JWT | Issue show-cause notice |
| GET | `/api/v1/hr/staff/{staff_id}/insurance/` | JWT | Fetch insurance/ESI/PF details |
| GET | `/api/v1/hr/staff/{staff_id}/leave-balance/` | JWT | Read-only leave balance from Leave module |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | click | GET `/api/v1/hr/staff/{id}/[tab]/` | `#tab-content-panel` | innerHTML |
| Edit Profile drawer open | click | GET `/group/hr/staff/{id}/edit/drawer/` | `#drawer-container` | innerHTML |
| Profile save | submit | PATCH `/api/v1/hr/staff/{id}/` | `#profile-header` | outerHTML |
| Document upload | change (file input) | POST `/api/v1/hr/staff/{id}/documents/` | `#documents-list` | outerHTML |
| Initiate BGV drawer open | click | GET `/group/hr/staff/{id}/bgv/drawer/` | `#drawer-container` | innerHTML |
| BGV initiate submit | submit | POST `/api/v1/hr/staff/{id}/bgv/initiate/` | `#bgv-tab-content` | innerHTML |
| Show-Cause Notice modal | click | GET `/group/hr/staff/{id}/notice/modal/` | `#modal-container` | innerHTML |
| Transfer request submit | submit | POST `/api/v1/hr/staff/{id}/transfers/` | `#transfers-tab-content` | innerHTML |
| KPI bar refresh | load | GET `/api/v1/hr/staff/{id}/kpi/` | `#kpi-bar` | outerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
