# 26 — Training Session Manager

- **URL:** `/group/hr/training/sessions/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Training & Development Manager (Role 45, G2)

---

## 1. Purpose

The Training Session Manager is the operational layer between the CPD catalog and actual staff attendance. While the catalog (page 25) defines what programs are available, this page manages the scheduling and execution of specific instances — a session is a real event on a real date with real participants. The Training & Development Manager uses this page to plan and deliver training across all branches, managing registrations, materials, and the transition from enrollment to assessment to certification.

Each session is an instance of a program from the catalog. Creating a session requires selecting the program, defining which branch or branches it covers (some programs may be run for multiple branches in one go), setting the date, time, venue or online link, maximum participant capacity, and the enrollment window (when branch staff can register). The T&D Manager can also bulk-enroll specific staff groups directly — useful for mandatory compliance programs where waiting for voluntary registration would not be reliable enough. Bulk enrollment is based on role filters: "Enroll all Class Teachers at Branch X" or "Enroll all wardens group-wide."

The session lifecycle has clear stages: Scheduled (session created, enrollment not yet open) → Enrollment Open (staff can register) → Enrollment Closed (registration cut-off reached or max capacity hit) → Completed (session date has passed and it was conducted) → Assessment Pending (if the program requires a post-session test) → Closed (attendance marked, assessments scored, certificates generated). Each stage transition is a deliberate action by the T&D Manager, not an automatic time-based trigger, because real-world training delivery involves delays, postponements, and reschedules that need human judgement. The exception is that sessions past their scheduled date automatically surface a "Mark as Completed or Postponed" prompt to the T&D Manager.

Sessions with low enrollment (below 50% of capacity at the time enrollment closes) are flagged as a KPI alert. Low enrollment may indicate poor communication, inconvenient scheduling, or lack of relevance — all of which the T&D Manager should address before the session runs. The page also tracks assessments: once a session is marked Completed, an assessment can be uploaded (a form link or document). Staff who complete the assessment pass or fail, and passing is a prerequisite for certificate generation. For compliance programs (POCSO, fire safety), the certificate is also linked to the staff member's compliance record.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access | Policy oversight; can cancel any session |
| Group HR Manager (42) | G3 | Read-only | Can view sessions for HR planning |
| Group Recruiter — Teaching (43) | G0 | No access | — |
| Group Recruiter — Non-Teaching (44) | G0 | No access | — |
| Group Training & Dev Manager (45) | G2 | Full CRUD | Primary owner of session management |
| Group Performance Review Officer (46) | G1 | Read-only | Views sessions for appraisal context |
| Group Staff Transfer Coordinator (47) | G3 | No access | — |
| Group BGV Manager (48) | G3 | No access | — |
| Group BGV Executive (49) | G3 | No access | — |
| Group POCSO Coordinator (50) | G3 | Read-only — Compliance sessions only | Monitors POCSO session delivery |
| Group Disciplinary Committee Head (51) | G3 | No access | — |
| Group Employee Welfare Officer (52) | G3 | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Training & Development → Training Session Manager`

### 3.2 Page Header
- Title: "Training Session Manager"
- Subtitle: "Schedule, manage, and track CPD training sessions across all branches."
- Primary CTA: "+ Schedule Session"
- Secondary CTAs: "Export Sessions Report" | "Bulk Enroll Staff"

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Sessions past scheduled date with no completion or postpone action | "[N] session(s) are past their scheduled date with no status update. Mark as Completed or Postponed." | Red |
| Sessions with enrollment < 50% at enrollment close | "[N] session(s) have low enrollment (< 50% capacity)." | Orange |
| Assessments pending for completed sessions > 7 days | "[N] session(s) have assessments pending for over 7 days." | Yellow |
| Mandatory sessions with 0 enrollment | "[N] mandatory session(s) have no registrations yet." | Orange |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Sessions This Month | Count of sessions scheduled in current month | Neutral blue | Filters to current month |
| Total Enrolled (All Active) | Sum of enrolled staff across all active sessions | Neutral | — |
| Sessions With Low Enrollment | Count with enrolled < 50% of max capacity | Red if > 0 | Filters to low enrollment |
| Sessions Completed | Count with status = Completed (this month) | Green | Filters to completed |
| Assessments Pending | Count with status = Assessment Pending | Amber if > 0 | Filters to assessment pending |
| Certificates Generated | Count of certificates issued (this month) | Green | — |

---

## 5. Main Table — Training Sessions

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Session Name | Text (Program name + date suffix, link to view) | Yes | Yes (search) |
| Program | Text (from catalog) | Yes | Yes (dropdown) |
| Branch(es) | Text (comma-separated or "Group-Wide") | Yes | Yes (dropdown) |
| Date | Date + Time | Yes | Yes (date range) |
| Mode | Chip (In-Person / Online / Hybrid) | Yes | Yes |
| Enrolled / Max | Text (e.g., "18 / 30") | Yes | Yes (low enrollment filter) |
| Status | Chip (Scheduled / Enrollment Open / Enrollment Closed / Completed / Assessment Pending / Closed) | Yes | Yes |
| Facilitator | Text | No | No |
| Actions | View Enrolled / Mark Attendance / Upload Assessment / Generate Certificates / Edit / Cancel | No | No |

### 5.1 Filters
- Status: All | Scheduled | Enrollment Open | Enrollment Closed | Completed | Assessment Pending | Closed
- Mode: All | In-Person | Online | Hybrid
- Branch: All branches (dropdown)
- Date Range: This Month | Next 7 Days | Custom
- Enrollment: All | Low (< 50%) | Full (= 100%)
- Program Category: All | Pedagogy | Subject | Technology | Leadership | Compliance

### 5.2 Search
Search by session name or program name. Minimum 2 characters, 400ms debounce.

### 5.3 Pagination
Server-side pagination, 20 sessions per page. Standard navigation with total session count.

---

## 6. Drawers

### 6.1 Drawer: Schedule Session (Create)
Fields: Program (dropdown from Active catalog programs), Session Name (auto-suggested: "[Program Name] — [Date]", editable), Branch(es) (multi-select — or "Group-Wide" checkbox), Date (date picker), Start Time / End Time (time pickers), Venue / Online Link (text), Max Participants (integer), Enrollment Opens (date/time picker — default: now), Enrollment Closes (date/time picker — must be before session date), Facilitator (auto-populated from program; overridable), Pre-reading Material (upload or link — optional), Notes.
On Save: session created with status = Scheduled. If enrollment open date is today: status immediately → Enrollment Open. Notification sent to relevant branch HR contacts.

### 6.2 Drawer: View Enrolled Staff
List of all registered participants for the session. Columns: Staff Name, Branch, Role, Enrolled Date, Attendance Status (auto-shows after attendance marking). Actions: Remove from Session (Enrollment Open status only). "Bulk Enroll" button at top: opens role-based filter to add multiple staff in one action.

### 6.3 Drawer: Mark Attendance
Available when status = Completed. Shows enrolled staff list with per-staff attendance toggle (Present / Absent / Late). For online sessions: note that auto-tracking occurs via login duration (> 75% = Present) — manual override available. "Save Attendance" button. On Save: triggers CPD hour crediting for Present/Late staff (if Late: partial credit configurable).

### 6.4 Drawer: Upload Assessment
Fields: Assessment Type (Online Form Link / Uploaded Document), Pass Mark % (integer), Assessment Deadline (date picker). Upload field or URL input. On Save: assessment linked to session, status → Assessment Pending, enrolled staff notified.

### 6.5 Drawer: Generate Certificates
Available when attendance is marked. Shows staff with attendance ≥ 75% (eligible). T&D Manager can deselect individuals. "Generate for All Eligible" button. On Submit: certificates generated as PDFs, linked to staff profiles, CPD hours credited, status → Closed.

### 6.6 Modal: Cancel Session
Reason (dropdown: Facilitator Unavailable / Insufficient Enrollment / Emergency / Postponed / Other) + Notes + Notify Enrolled Staff (checkbox). On Confirm: status → Cancelled, enrolled staff notified if checkbox checked.

---

## 7. Charts

**Enrollment vs Capacity — Bar Chart per Active Session:** grouped bars showing enrolled count vs max capacity for each active session (sessions with Enrollment Open or Enrollment Closed status). Helps T&D Manager identify low-enrollment sessions at a glance. Toggle: "Show Chart / Hide". Rendered via Chart.js below the table.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Session scheduled | "Session '[Name]' scheduled for [Date]." | Success | 4s |
| Session status updated | "Session status updated to [Status]." | Success | 4s |
| Staff bulk-enrolled | "[N] staff members enrolled in '[Session Name]'." | Success | 4s |
| Attendance saved | "Attendance recorded for [Session Name]." | Success | 4s |
| Assessment uploaded | "Assessment linked to '[Session Name]'. Staff notified." | Success | 4s |
| Certificates generated | "[N] certificate(s) generated for '[Session Name]'." | Success | 5s |
| Session cancelled | "Session '[Name]' cancelled. Enrolled staff notified." | Warning | 5s |
| Low enrollment alert on save | "Warning: current enrollment is below 50% of capacity." | Warning | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No sessions scheduled | "No Training Sessions Scheduled" | "Schedule a session from the CPD catalog to start enrolling staff." | Schedule Session |
| Filter returns no results | "No Matching Sessions" | "Adjust your filters or date range to find sessions." | Clear Filters |
| Enrolled staff drawer — no registrations | "No Staff Enrolled Yet" | "Enrollment is open. Share the session with branch staff to register." | Bulk Enroll |
| Completed sessions — no certificates | "No Certificates Generated" | "Mark attendance and upload assessment results to generate certificates." | Mark Attendance |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI skeletons (6) + table row skeletons (12) |
| Filter change | Table body row skeletons |
| Schedule session drawer | Form field skeletons |
| Enrolled staff drawer | Staff row skeletons (10 rows) |
| Certificate generation | Spinner + "Generating certificates…" message |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) | T&D Manager (45) | Read-Only Roles (42, 46, 50) |
|---|---|---|---|
| Schedule Session button | Visible | Visible + enabled | Hidden |
| Edit session | Visible | Visible | Hidden |
| Cancel session | Visible | Visible | Hidden |
| Bulk Enroll | Visible | Visible | Hidden |
| Mark Attendance | Visible | Visible | Hidden |
| Upload Assessment | Visible | Visible | Hidden |
| Generate Certificates | Visible | Visible | Hidden |
| View Enrolled staff | Visible | Visible | Visible |
| Export Sessions Report | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/training/sessions/` | JWT | List all sessions (paginated) |
| POST | `/api/v1/hr/training/sessions/` | JWT | Create/schedule new session |
| GET | `/api/v1/hr/training/sessions/{id}/` | JWT | Fetch session detail |
| PATCH | `/api/v1/hr/training/sessions/{id}/` | JWT | Update session |
| PATCH | `/api/v1/hr/training/sessions/{id}/status/` | JWT | Change session status |
| GET | `/api/v1/hr/training/sessions/{id}/enrolled/` | JWT | List enrolled staff |
| POST | `/api/v1/hr/training/sessions/{id}/enroll/` | JWT | Bulk enroll staff |
| DELETE | `/api/v1/hr/training/sessions/{id}/enrolled/{staff_id}/` | JWT | Remove enrollee |
| POST | `/api/v1/hr/training/sessions/{id}/attendance/` | JWT | Submit attendance |
| POST | `/api/v1/hr/training/sessions/{id}/assessment/` | JWT | Upload/link assessment |
| POST | `/api/v1/hr/training/sessions/{id}/certificates/` | JWT | Generate certificates |
| PATCH | `/api/v1/hr/training/sessions/{id}/cancel/` | JWT | Cancel session |
| GET | `/api/v1/hr/training/sessions/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/training/sessions/chart/` | JWT | Enrollment vs capacity chart |
| GET | `/api/v1/hr/training/sessions/export/` | JWT | Export sessions report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/training/sessions/?q={val}` | `#sessions-table-body` | innerHTML |
| Status filter | change | GET `/api/v1/hr/training/sessions/?status={val}` | `#sessions-table-body` | innerHTML |
| Multi-filter apply | change | GET `/api/v1/hr/training/sessions/?mode={}&branch={}&category={}` | `#sessions-table-body` | innerHTML |
| Date range filter | change | GET `/api/v1/hr/training/sessions/?date_from={}&date_to={}` | `#sessions-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/training/sessions/?page={n}` | `#sessions-table-body` | innerHTML |
| Schedule session drawer | click | GET `/group/hr/training/sessions/schedule/drawer/` | `#drawer-container` | innerHTML |
| Enrolled staff drawer | click | GET `/group/hr/training/sessions/{id}/enrolled/drawer/` | `#drawer-container` | innerHTML |
| Mark Attendance drawer | click | GET `/group/hr/training/sessions/{id}/attendance/drawer/` | `#drawer-container` | innerHTML |
| Attendance submit | submit | POST `/api/v1/hr/training/sessions/{id}/attendance/` | `#session-row-{id}` | outerHTML |
| Certificate generate | click | POST `/api/v1/hr/training/sessions/{id}/certificates/` | `#session-row-{id}` | outerHTML |
| Cancel session modal | click | GET `/group/hr/training/sessions/{id}/cancel/modal/` | `#modal-container` | innerHTML |
| Chart toggle | click | GET `/group/hr/training/sessions/chart/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
