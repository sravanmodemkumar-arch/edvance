# 28 — Student Welfare Case Manager

> **URL:** `/group/welfare/cases/`
> **File:** `28-student-welfare-case-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Welfare Events Coordinator (Role 95, G3) — primary; case opener roles include Counselling Head, Hostel Warden, Branch Medical Officer

---

## 1. Purpose

Case management system for individual students with ongoing, complex welfare needs requiring coordinated attention across multiple teams simultaneously. This page fills a specific organisational gap: welfare events (page 23) handle one-off incidents, and counselling sessions (page 13, Division J) handle therapeutic programme records — but neither provides a longitudinal, multi-department coordination record for a student who needs sustained, structured support over weeks or months.

**What is a welfare case?**
A welfare case is opened when a student's situation requires coordinated effort across two or more of: Counsellor + Hostel Warden + Medical Room + Class Teacher + Parents + Academic Tutor. A case is not for every student who has a problem — it is for students whose issues are complex enough that a single department cannot manage alone.

**Example scenarios triggering a welfare case:**
- A Class 11 hosteler with repeated homesickness episodes, declining appetite, weight loss, and academic drop — requiring simultaneous input from the hostel warden (room change), medical room (nutrition monitoring), counsellor (weekly sessions), class teacher (academic flexibility), and parents (weekend visits)
- A Class 10 student with a suspected eating disorder escalated by the Branch Medical Officer, requiring counsellor + parents + external referral coordination
- A student who has been a victim of bullying (welfare event raised) who now needs ongoing multi-department support and parental communication management
- A student with a family crisis (parental separation, bereavement) affecting hostel behaviour, academics, and mental health — requiring a joined-up response

**Case lifecycle:**
1. Case Opened → by Welfare Coordinator / Counselling Head / Hostel Warden / Branch Medical Officer
2. Departments Engaged → relevant teams notified and added to the case
3. Active Management → regular interventions, notes, parent communications logged
4. Monitoring → student improving; reduced intervention frequency
5. Discharged → student stable; formal closure with discharge summary

A case can also be transferred (to another institution if student leaves) or closed prematurely if the student withdraws.

**DPDP Act 2023 compliance:**
- Student identity (name, ID) visible only to: Welfare Coordinator + assigned Counsellor + Branch Medical Officer on the case
- Other authorised case participants (Hostel Warden, Class Teacher) see Student Code only, not the name
- Student (or guardian for minors) consent for case opening is documented in the system
- Consent is a required field before any case notes can be added beyond the initial assessment
- Audit log records every access to personally identifiable fields

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Welfare Events Coordinator | G3 | Full — read all cases, open case, assign departments, add interventions, log parent communications, discharge | Case manager; sees all cases across branches; student name visible |
| Group Counselling Head | G3 | Read all cases + open case + add counselling interventions | Student name visible |
| Branch Counsellor | Branch | Read cases where assigned + add counselling interventions | Student name visible for own cases only |
| Branch Medical Officer | Branch | Read cases involving their branch + add medical interventions | Student name visible; can open case |
| Branch Hostel Warden | Branch | Read cases involving their hostel + add hostel notes | Student Code only (not name); can open case |
| Branch Principal | Branch | Read all cases at own branch (aggregate view + case list) | Student Code only |
| All other roles | — | No access | — |

> **Access enforcement:** `@require_role(...)` with queryset filters per role. Student name/ID are masked at the PostgreSQL view layer — not just the UI — for roles where name is not permitted. Every read of the student identity fields is logged to `case_identity_access_audit` table: user ID, case ID, timestamp, field accessed.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Cases  ›  Student Welfare Case Manager
```

### 3.2 Page Header
- **Title:** `Student Welfare Case Manager`
- **Subtitle:** `[N] Active Cases · [N] High/Critical · [N] Stagnant (no update > 7 days) · [N] Discharged This Month`
- **Right controls:** `+ Open New Case` (Welfare Coordinator / Counselling Head / Branch Medical Officer / Branch Hostel Warden) · `Advanced Filters` · `Export CSV` (Welfare Coordinator + Counselling Head)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Active High / Critical case with no update > 7 days | "[N] High or Critical welfare cases have had no update in over 7 days. Stagnation alert." | Red |
| Case open > 90 days without discharge review | "[N] cases have been open for over 90 days. A formal review and discharge assessment is recommended." | Amber |
| Consent not documented within 48h of opening | "[N] recently opened cases are missing student/guardian consent documentation." | Amber |
| Critical case with no intervention in 14 days | "[N] Critical cases have no recorded intervention in the past 14 days." | Red |

---

## 4. KPI Summary Bar

Eight cards in a responsive 4×2 grid. Metrics apply to all selected filters; default is all branches, all active cases.

| # | Card | Metric | Colour Rule |
|---|---|---|---|
| 1 | Active Cases | Count of cases with status = Active | Blue always |
| 2 | High / Critical Cases | Count of Active cases with severity = High or Critical | Red > 5 · Yellow 1–5 · Green = 0 |
| 3 | Cases Open > 90 Days | Count of Active cases where (today − open date) > 90 | Red > 5 · Yellow 1–5 · Green = 0 |
| 4 | Discharged This Month | Count of cases discharged in current calendar month | Green always |
| 5 | Avg Case Duration (days) | Mean (discharge date − open date) for all discharged cases in current year | Green ≤ 45 · Yellow 45–90 · Red > 90 |
| 6 | Stagnant Cases (> 7 days) | Cases with status = Active and no case note / intervention in > 7 days | Red > 0 · Green = 0 |
| 7 | Active Cases Trend | Mini line chart — count of Active cases per month for past 12 months | Visual only |
| 8 | Concern Distribution | Mini donut: Academic / Emotional / Physical / Family / Peer / Hostel / Multiple | Visual only |

---

## 5. Main Table — Welfare Cases

### 5.1 Search
Full-text search on: Case ID, Student Code (name is masked to Student Code in search for non-authorised roles), Branch Name, Counsellor Assigned. Debounce 300 ms, minimum 2 characters.

Student name search is available only for Welfare Coordinator and Counselling Head — returns `Student Code` in result for other roles.

### 5.2 Advanced Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Status | Checkbox | Active · Monitoring · Discharged · Transferred |
| Severity | Checkbox | Low · Medium · High · Critical |
| Primary Concern | Checkbox | Academic · Emotional · Physical · Family · Peer · Hostel · Multiple |
| Departments Involved | Multi-select | Counselling · Medical · Hostel · Academic · Parent |
| Class | Checkbox | Class 6 – Class 12 |
| Hostel Status | Radio | All · Hostel Only · Day Scholar Only |
| Days Since Last Update | Range | Min – Max (integer) |
| Case Duration (days) | Range | Min – Max |
| Academic Year | Single-select | Current + 2 prior |

### 5.3 Table Columns

| Column | Sortable | Notes |
|---|---|---|
| Case ID | ✅ | System-generated (e.g., WC-2026-00089) |
| Student Code | ✅ | Student Code shown to all roles; name visible only to authorised roles (shown in tooltip or adjacent cell) |
| Branch | ✅ | |
| Hostel / Day | ✅ | Hostel (blue) / Day Scholar (grey) badge |
| Class / Stream | ✅ | |
| Counsellor Assigned | ✅ | Name or "Unassigned" |
| Case Open Date | ✅ | DD-MMM-YYYY |
| Primary Concern | ✅ | Tag badge |
| Severity | ✅ | Low (grey) · Medium (amber) · High (red) · Critical (flashing red) badge |
| Departments Involved | ❌ | Tag cluster: Counselling · Medical · Hostel · Academic · Parent |
| Days Open | ✅ | Integer; amber if > 60; red if > 90 |
| Last Update | ✅ | Relative time; red if > 7 days |
| Status | ✅ | Active (blue) · Monitoring (green) · Discharged (dark grey) · Transferred (purple) badge |
| Actions | ❌ | View · Add Intervention · Log Parent Contact · Discharge |

**Default sort:** Severity descending (Critical → Low), then Last Update ascending (longest-stagnant first within severity).
**Pagination:** Server-side · 25 rows/page.
**Row highlight:** Critical cases have a red left border; Stagnant (> 7 days no update) have an amber left border.

---

## 6. Drawers / Modals

### 6.1 Drawer — `case-detail` (800px, right side)

Triggered by **View** in Actions column. Largest drawer in the welfare system — required for multi-department case management.

**Header:** Case ID · Severity badge · Status badge · Branch · Days Open

**Tabs:**

#### Tab 1 — Overview
| Field | Notes |
|---|---|
| Case ID | Read-only |
| Student Code | Read-only; name shown to authorised roles only (Welfare Coordinator / Counselling Head / Branch Counsellor (if assigned) / Branch Medical Officer on case) |
| Branch | |
| Class / Stream | |
| Hostel / Day Scholar | |
| Case Opened By | Name + Role |
| Case Open Date | |
| Counsellor Assigned | Name; editable by Welfare Coordinator |
| Primary Concern | Badge |
| Secondary Concerns | Tags |
| Severity | Badge + severity history (previous level if changed) |
| Departments Involved | Tags with engaged date per department |
| Initial Assessment | Free text — what was known at case opening |
| Consent Documented | Yes / No badge; Consent Date; Guardian name (for minors) |
| DPDP Consent Notes | Free text — method of consent, who consented |
| Case Status | Badge |
| Status History | Compact timeline |

#### Tab 2 — Concerns
Detailed breakdown of each concern area for this student.

| Concern Area | Fields |
|---|---|
| Academic | Current grades vs baseline, subjects of concern, teacher observations, exam attendance |
| Emotional / Mental Health | Mood observations, risk indicators, counsellor summary |
| Physical | Medical diagnoses or concerns, weight/appetite tracking, medical room visits |
| Family | Family situation summary, communication status, parental engagement level |
| Peer / Social | Peer relationship quality, social isolation indicators, incidents |
| Hostel | Room behaviour, warden observations, curfew compliance, room change history |

Each concern area is a collapsible accordion section. Each section has: a free-text summary field (editable by the department responsible for that concern area) and a "last updated by / date" stamp.

#### Tab 3 — Interventions
Chronological timeline of all actions taken across all departments.

| Column | Notes |
|---|---|
| Date | DD-MMM-YYYY |
| Department | Tag: Counselling · Medical · Hostel · Academic · Parent |
| Intervention Type | Counselling Session / Medical Review / Room Change / Academic Adjustment / Parent Meeting / External Referral / Other |
| Description | What was done, observed, or decided |
| Outcome | Result of this intervention |
| Next Steps | Planned follow-up |
| Added By | Name + Role |

**Footer:** `+ Add Intervention` — opens `add-intervention` drawer (pre-linked to this case).

Cross-department visibility: Each department sees all interventions but can only edit their own. The Welfare Coordinator sees and can annotate all.

#### Tab 4 — Department Notes
Segregated note areas per department. Each department area is a tab-within-tab accordion:

| Sub-section | Visible to |
|---|---|
| Counselling Notes | Welfare Coordinator + Counselling Head + assigned Counsellor |
| Medical Notes | Welfare Coordinator + Branch Medical Officer |
| Hostel Notes | Welfare Coordinator + Branch Hostel Warden + Branch Principal (own branch) |
| Academic Notes | Welfare Coordinator + Counselling Head + Branch Principal |
| Parent Communication Summary | Welfare Coordinator + Counselling Head |

Each sub-section shows: list of notes (date, author, text) with a "Add Note" inline form at the bottom (visible to authorised role only). Unauthorised sub-sections show: *"Notes in this section are restricted to [Department] staff."*

#### Tab 5 — Parent Communication
Log of all parent / guardian contacts.

| Column | Notes |
|---|---|
| Date | DD-MMM-YYYY |
| Mode | WhatsApp · Phone Call · In-Person Meeting · Email · Written Letter |
| Contact Made By | Name + Role |
| Parent / Guardian | Name + relationship |
| Summary | What was discussed |
| Parent Reaction | Cooperative / Concerned / Unresponsive / Hostile |
| Outcome | What was agreed or next step |
| Follow-up Required | Yes / No; Date if Yes |

**Footer:** `+ Log Parent Contact` — opens `parent-communication-log` drawer.

#### Tab 6 — Documents
File attachments for the case: consent forms, medical certificates, correspondence, referral letters, external assessment reports.

| Column | Notes |
|---|---|
| Document Name | |
| Type | Consent Form · Medical Certificate · External Report · Correspondence · Other |
| Uploaded By | |
| Upload Date | |
| Access | Who can see this document (role tags) |
| Actions | Download · Delete (uploader only, within 24h) |

**Footer:** `+ Upload Document`

#### Tab 7 — Discharge
Enabled once Welfare Coordinator initiates discharge. Read-only once submitted.

| Field | Type | Validation |
|---|---|---|
| Discharge Reason | Single-select: Resolved / Transferred to Another Institution / Student Left / Other | Required |
| Discharge Date | Date picker | Required; not future |
| Discharge Summary | Textarea (max 3,000 chars) — student's condition at discharge, progress made | Required |
| Departments Signed Off | Checklist — each involved department must be marked as having confirmed discharge readiness | Required; all departments checked |
| Follow-up Recommendations | Textarea (max 1,000 chars) | Optional |
| Transfer Institution (if applicable) | Text input | Required if reason = Transferred |
| Discharged By | Read-only (Welfare Coordinator) | Auto |

**Footer:** `Cancel` · `Discharge Case` (Welfare Coordinator only)

---

### 6.2 Drawer — `open-new-case` (640px, right side)

Triggered by **+ Open New Case** button.

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select (auto-set for branch roles) | Required |
| Student Search | Autocomplete (branch-scoped; name shown to authorised roles; code shown to others) | Required; debounce 300 ms |
| Hostel / Day Scholar | Radio (auto-populated from student record) | Read-only |
| Class / Stream | Read-only (from student record) | Auto |
| Primary Concern | Single-select: Academic · Emotional · Physical · Family · Peer · Hostel · Multiple | Required |
| Secondary Concerns | Multi-select (same options; exclude primary) | Optional |
| Initial Severity | Radio: Low · Medium · High · Critical | Required |
| Departments to Involve | Multi-select: Counselling · Medical · Hostel · Academic · Parent | Required; at least one |
| Counsellor to Assign | Single-select (branch counsellors list; auto-suggests if Counselling department selected) | Required if Counselling selected |
| Initial Assessment | Textarea (max 2,000 chars) — description of presenting situation | Required; min 100 chars |
| Consent Documented | Toggle: Yes / Not Yet | Required |
| Consent Date | Date picker | Required if Consent = Yes |
| Guardian Consent Name | Text input | Required for minors (under 18) |
| DPDP Consent Notes | Textarea (max 500 chars) — how consent was obtained | Required if Consent = Yes |

**Consent warning:** If Consent = Not Yet, a yellow inline alert is shown: *"Case can be opened without consent in an emergency, but consent must be documented within 48 hours. The system will alert you."*

**Footer:** `Cancel` · `Open Case`

**Validation:**
- Student search: must resolve to a specific student (not free text)
- Initial Assessment: minimum 100 characters
- Severity Critical: confirmation checkbox: "I confirm this student is in immediate danger or at critical risk warranting this severity."

---

### 6.3 Drawer — `add-intervention` (480px, right side)

Triggered by **Add Intervention** in Actions column or Interventions tab footer.

| Field | Type | Validation |
|---|---|---|
| Case ID | Read-only | |
| Student Code | Read-only | |
| Department | Single-select (defaults to role's department) | Required |
| Intervention Type | Single-select: Counselling Session · Medical Review · Room Change · Academic Adjustment · Parent Meeting · External Referral · Medication Change · Other | Required |
| Date | Date picker (defaults to today) | Required; not future |
| Description | Textarea (max 1,500 chars) | Required |
| Outcome | Textarea (max 1,000 chars) | Required |
| Next Steps | Textarea (max 500 chars) | Optional |
| Severity Reassessment | Radio: No change · Upgrade to [higher] · Downgrade to [lower] | Optional |
| Severity Change Reason | Textarea (max 300 chars) | Required if severity change selected |

**Footer:** `Cancel` · `Log Intervention`

**Behaviour:** On save, Intervention is appended to Interventions timeline; if severity changed, new severity badge shown in case header and notification sent to Welfare Coordinator. Status badge unchanged unless Coordinator explicitly changes it.

---

### 6.4 Drawer — `parent-communication-log` (440px, right side)

Triggered by **Log Parent Contact** in Actions column or Parent Communication tab footer.

| Field | Type | Validation |
|---|---|---|
| Case ID | Read-only | |
| Date | Date picker (defaults to today) | Required |
| Mode | Radio: WhatsApp · Phone Call · In-Person Meeting · Email · Written Letter | Required |
| Contact Made By | Read-only (logged-in user) | Auto |
| Parent / Guardian Name | Text input | Required |
| Relationship | Single-select: Father · Mother · Legal Guardian · Other | Required |
| Summary | Textarea (max 1,500 chars) — what was discussed | Required |
| Parent Reaction | Radio: Cooperative · Concerned · Unresponsive · Hostile | Required |
| Outcome | Textarea (max 500 chars) | Required |
| Follow-up Required | Toggle | Required |
| Follow-up Date | Date picker | Required if Follow-up = Yes |

**Footer:** `Cancel` · `Log Contact`

---

### 6.5 Drawer — `discharge-case` (480px, right side)

Triggered by **Discharge** in Actions column. Welfare Coordinator only.

Same fields as Tab 7 (Discharge) in the case-detail drawer. This is the standalone trigger for the discharge flow when accessed from the main table (rather than from within the case detail drawer).

**Departments sign-off checklist** displays all departments involved in the case, each with a checkbox that the Welfare Coordinator confirms is ready. This is the Welfare Coordinator's confirmation that they have checked with each department — individual department approval is not collected via system workflow (the coordinator is responsible for that coordination offline or via notes/interventions).

**Footer:** `Cancel` · `Discharge Case`

**Behaviour:** Status updated to Discharged; all involved departments notified; discharge summary stored; case moved to Discharged view (still searchable with Status = Discharged filter); student record unlocked from active-case flag.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Case opened | "Welfare case [ID] opened for [Student Code]. Departments notified." | Success |
| Case opened without consent | "Case [ID] opened. Consent must be documented within 48 hours." | Warning |
| Intervention logged | "Intervention logged for Case [ID]." | Success |
| Severity upgraded | "Case [ID] severity upgraded to [Level]. Welfare Coordinator notified." | Warning |
| Severity downgraded | "Case [ID] severity downgraded to [Level]." | Success |
| Parent contact logged | "Parent communication logged for Case [ID]." | Success |
| Document uploaded | "Document uploaded to Case [ID]." | Success |
| Case discharged | "Case [ID] has been discharged. All departments notified." | Success |
| Stagnation alert | "Case [ID] has had no update in [N] days. Coordinator attention required." | Warning |
| Consent deadline breach | "Case [ID] consent has not been documented within 48 hours. Action required." | Error |
| Validation error | "Please complete all required fields before saving." | Error |
| Identity access logged | (Silent — no toast) Audit log entry created. | — |
| Export triggered | "Export is being prepared." | Info |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No cases for current filters | "No welfare cases match the current filters." | "Try adjusting or clearing your filters." | `Clear Filters` button |
| No active cases | "No active welfare cases." | "Cases will appear here once opened." | `+ Open New Case` button |
| Interventions tab — no interventions | "No interventions recorded yet." | "Log the first intervention to begin the case management timeline." | `+ Add Intervention` |
| Parent Communication tab — no contacts | "No parent contacts logged." | "Log parent communications here to maintain a complete coordination record." | `+ Log Parent Contact` |
| Documents tab — no documents | "No documents attached to this case." | "Upload consent forms, medical certificates, or other case documents here." | `+ Upload Document` |
| Department Notes — no notes for a sub-section | "No [Department] notes yet." | "Notes will appear here once added by [Department] staff." | (Inline add-note form if authorised) |
| Discharge tab — departments not signed off | "Department sign-off required." | "Confirm all departments are ready before discharging." | (Checklist UI) |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 8 KPI cards + table (10 grey rows × 14 columns) |
| Filter / search apply | Table body spinner overlay; KPI + charts refresh after |
| Case detail drawer open | Drawer skeleton: tab bar + 10 grey field blocks |
| Interventions tab load | Timeline skeleton: 5 grey intervention entries |
| Department Notes tab load | Accordion skeleton: 5 grey department headers |
| Parent Communication tab load | Table skeleton: 5 grey rows |
| Documents tab load | File list skeleton: 3 grey file entries |
| Discharge tab | Form skeleton: 6 grey field blocks |
| Student name reveal (identity access) | Brief 200 ms spinner while audit log entry is created; then name is displayed |
| Add intervention submit | Drawer footer spinner + "Saving…"; resolves to success toast |
| Discharge submit | Modal spinner + "Processing discharge…"; button disabled |

---

## 10. Role-Based UI Visibility

| UI Element | Welfare Coordinator | Counselling Head | Branch Counsellor | Branch Medical Officer | Branch Hostel Warden | Branch Principal |
|---|---|---|---|---|---|---|
| Full cross-branch case list | ✅ | ✅ | Own branch, assigned cases | Own branch cases | Own branch cases | Own branch (code only) |
| Student name visible | ✅ | ✅ | Own assigned cases | Own branch cases | ❌ (code only) | ❌ (code only) |
| + Open New Case | ✅ | ✅ | ❌ | ✅ | ✅ (limited fields) | ❌ |
| Add Intervention | ✅ | ✅ (counselling) | ✅ (counselling) | ✅ (medical) | ✅ (hostel) | ❌ |
| Log Parent Contact | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Discharge button | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Counselling Notes sub-section | ✅ | ✅ | ✅ (own) | ❌ | ❌ | ❌ |
| Medical Notes sub-section | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Hostel Notes sub-section | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ (read) |
| Academic Notes sub-section | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ (read) |
| Parent Comm. tab | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Documents tab | ✅ | ✅ | ✅ (view) | ✅ (own docs) | ✅ (own docs) | ❌ |
| Export CSV | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| KPI bar — full detail | ✅ | ✅ | Own branch | Own branch | Own branch | Own branch |
| Alert banners | ✅ | ✅ | Own branch | Own branch | Own branch | Own branch |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/welfare/cases/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/cases/` | List welfare cases (paginated, filtered, role-scoped, name-masked) | JWT + role check |
| POST | `/api/v1/group/{group_id}/welfare/cases/` | Open new welfare case | Welfare Coordinator / Counselling Head / Branch Medical Officer / Branch Hostel Warden |
| GET | `/api/v1/group/{group_id}/welfare/cases/{case_id}/` | Retrieve case detail (role-masked fields) | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/welfare/cases/{case_id}/` | Update case metadata (counsellor assignment, severity, status) | Welfare Coordinator |
| POST | `/api/v1/group/{group_id}/welfare/cases/{case_id}/interventions/` | Log intervention | Authorised department roles |
| GET | `/api/v1/group/{group_id}/welfare/cases/{case_id}/interventions/` | List all interventions for a case | JWT + role check |
| POST | `/api/v1/group/{group_id}/welfare/cases/{case_id}/notes/` | Add department note | Authorised department roles (scoped to own department) |
| GET | `/api/v1/group/{group_id}/welfare/cases/{case_id}/notes/` | List notes (role-scoped to own department + Welfare Coordinator) | JWT + role check |
| POST | `/api/v1/group/{group_id}/welfare/cases/{case_id}/parent-communications/` | Log parent contact | Welfare Coordinator / Counselling Head |
| GET | `/api/v1/group/{group_id}/welfare/cases/{case_id}/parent-communications/` | List parent communications | Welfare Coordinator / Counselling Head |
| POST | `/api/v1/group/{group_id}/welfare/cases/{case_id}/documents/` | Upload document | All authorised roles on the case |
| GET | `/api/v1/group/{group_id}/welfare/cases/{case_id}/documents/` | List documents (role-scoped visibility) | JWT + role check |
| DELETE | `/api/v1/group/{group_id}/welfare/cases/{case_id}/documents/{doc_id}/` | Delete document (uploader, within 24h) | JWT + owner check |
| POST | `/api/v1/group/{group_id}/welfare/cases/{case_id}/discharge/` | Discharge case | Welfare Coordinator |
| GET | `/api/v1/group/{group_id}/welfare/cases/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/cases/charts/` | Active cases trend + concern distribution chart data | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/cases/alerts/` | Active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/cases/student-search/` | Student autocomplete (branch-scoped; name vs code by role) | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/cases/export/` | Export CSV (role-masked fields) | Welfare Coordinator / Counselling Head |

**Identity access audit:** Every GET of `case_id` detail that includes student name/ID fields appends a row to `case_identity_access_audit`: `{user_id, case_id, timestamp, fields_accessed, ip_address}`. This is enforced in the FastAPI response middleware, not in the HTMX layer.

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `status` | str[] | `active`, `monitoring`, `discharged`, `transferred` |
| `severity` | str[] | `low`, `medium`, `high`, `critical` |
| `primary_concern` | str[] | Concern slugs |
| `department` | str[] | `counselling`, `medical`, `hostel`, `academic`, `parent` |
| `class_level` | str[] | Class level slugs |
| `hostel_only` | bool | Filter to hostel students |
| `day_scholar_only` | bool | Filter to day scholars |
| `days_since_update_min` | int | Minimum days since last update |
| `days_since_update_max` | int | Maximum days since last update |
| `case_duration_min` | int | Minimum case open days |
| `case_duration_max` | int | Maximum case open days |
| `academic_year` | str | e.g., `2025-26` |
| `page` | int | Page number |
| `page_size` | int | Default 25, max 100 |
| `search` | str | Case ID, student code, branch, counsellor name |
| `sort_by` | str | Column name; prefix `-` for descending |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search input | `hx-get="/api/.../cases/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#cases-table-body"` `hx-include="#filter-form"` | Table body replaced |
| Filter apply | `hx-get="/api/.../cases/"` `hx-trigger="change"` `hx-target="#cases-table-body"` `hx-include="#filter-form"` | Table + KPI + charts refreshed |
| Pagination | `hx-get="/api/.../cases/?page={n}"` `hx-target="#cases-table-body"` `hx-push-url="true"` | Page swap |
| Case detail drawer open | `hx-get="/api/.../cases/{case_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Overview tab default; identity access audit entry created |
| Drawer tab switch | `hx-get="/api/.../cases/{case_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped |
| Interventions tab load | `hx-get="/api/.../cases/{case_id}/interventions/"` `hx-target="#interventions-content"` `hx-trigger="click[tab='interventions']"` | Timeline loaded on tab click |
| Add intervention submit | `hx-post="/api/.../cases/{case_id}/interventions/"` `hx-target="#interventions-content"` `hx-swap="afterbegin"` | New intervention prepended to timeline; toast fires |
| Department notes sub-section load | `hx-get="/api/.../cases/{case_id}/notes/?department={slug}"` `hx-target="#notes-{slug}"` `hx-trigger="click"` | Notes loaded for that department's accordion |
| Add department note | `hx-post="/api/.../cases/{case_id}/notes/"` `hx-target="#notes-list-{slug}"` `hx-swap="beforeend"` | Note appended; inline form cleared |
| Parent communication tab load | `hx-get="/api/.../cases/{case_id}/parent-communications/"` `hx-target="#parent-comms-content"` `hx-trigger="click[tab='parent']"` | Communication log loaded |
| Log parent contact submit | `hx-post="/api/.../cases/{case_id}/parent-communications/"` `hx-target="#parent-comms-list"` `hx-swap="afterbegin"` | New log entry prepended |
| Document upload | `hx-post="/api/.../cases/{case_id}/documents/"` `hx-encoding="multipart/form-data"` `hx-target="#documents-list"` `hx-swap="beforeend"` | New document row appended |
| Open new case submit | `hx-post="/api/.../cases/"` `hx-target="#cases-table-body"` `hx-on::after-request="closeDrawer(); fireToast();"` | New row prepended; drawer closes; departments notified |
| Discharge case submit | `hx-post="/api/.../cases/{case_id}/discharge/"` `hx-target="#case-row-{case_id}"` `hx-swap="outerHTML"` | Row status updated to Discharged; drawer closes; toast fires |
| Severity change (in intervention) | `hx-trigger="change from:#severity-reassessment"` `hx-target="#severity-change-fields"` | Severity reason textarea revealed if change selected |
| Student name reveal (authorised roles) | `hx-get="/api/.../cases/{case_id}/?include_identity=true"` `hx-trigger="click from:#reveal-name-btn"` `hx-target="#student-identity-cell"` | Name loaded; audit log entry created; button replaced with name |
| KPI bar refresh | `hx-get="/api/.../cases/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Charts load | `hx-get="/api/.../cases/charts/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#chart-panel"` | Trend + donut updated |
| Alert banner load | `hx-get="/api/.../cases/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional banner display |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
