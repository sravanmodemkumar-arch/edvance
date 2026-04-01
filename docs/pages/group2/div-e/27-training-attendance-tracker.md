# 27 — Training Attendance Tracker

- **URL:** `/group/hr/training/attendance/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Training & Development Manager (Role 45, G2)

---

## 1. Purpose

The Training Attendance Tracker is the record-of-evidence layer for all CPD session attendance across the group. While the Session Manager (page 26) handles session scheduling and enrollment, this page provides the Training & Development Manager with a session-by-session, staff-by-staff audit trail of attendance. It is the source of truth for CPD hour crediting, certificate eligibility, and compliance follow-up. Without accurate attendance records, the group cannot demonstrate regulatory compliance for mandatory training programs, and staff cannot receive CPD credits toward their promotion eligibility.

Attendance recording operates differently depending on session delivery mode. For in-person sessions, attendance is recorded manually per staff member — the T&D Manager or session facilitator marks each enrolled participant as Present, Absent, or Late. Late arrivals are tracked with a threshold: arriving within the first 15 minutes is treated as "Present with note"; arriving after 15 minutes is "Late" and receives partial CPD credit (configurable as 50% or 75% of session credit hours). For online sessions, attendance is auto-tracked via login duration. A participant who is logged in for 75% or more of the session duration is counted as Present; below 75% is counted as Absent, regardless of whether they were physically watching. The 75% threshold is the standard used by most credentialing bodies and aligns with the CPD credit calculation rules in the catalog.

Compliance-critical sessions (POCSO, child protection, fire safety) have elevated consequences for non-attendance. When a staff member in a mandatory compliance program misses a session, this page automatically generates an alert to the HR Director and to the POCSO Coordinator (for POCSO specifically). The alert is persistent — it remains until the staff member completes a make-up session or the T&D Manager records a documented exception. This automated escalation removes the need for the T&D Manager to manually chase non-compliant staff, reducing administrative load while maintaining accountability.

CPD hours are only credited after attendance is confirmed on this page — not at enrollment, not at session completion, only after the individual's attendance status has been marked Present or Late (with partial credit). This prevents the common fraud of staff enrolling in sessions they never attend and then claiming CPD hours. The attendance-to-certificate pipeline is clearly defined: mark attendance → (optional) complete assessment → generate certificate → CPD hours credited to staff profile. Each step requires deliberate T&D Manager action, with the exception of online auto-tracking which runs server-side.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access | Receives compliance non-attendance alerts |
| Group HR Manager (42) | G3 | Read-only | Can view attendance for HR analytics |
| Group Recruiter — Teaching (43) | G0 | No access | — |
| Group Recruiter — Non-Teaching (44) | G0 | No access | — |
| Group Training & Dev Manager (45) | G2 | Full CRUD | Primary owner of attendance records |
| Group Performance Review Officer (46) | G1 | Read-only | Views attendance records for appraisal context |
| Group Staff Transfer Coordinator (47) | G3 | No access | — |
| Group BGV Manager (48) | G3 | No access | — |
| Group BGV Executive (49) | G3 | No access | — |
| Group POCSO Coordinator (50) | G3 | Read-only — POCSO sessions only | Receives non-attendance alerts for POCSO |
| Group Disciplinary Committee Head (51) | G3 | No access | — |
| Group Employee Welfare Officer (52) | G3 | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Training & Development → Training Attendance Tracker`

### 3.2 Page Header
- Title: "Training Attendance Tracker"
- Subtitle: "Record and review attendance for all CPD training sessions."
- Primary CTA: "Mark Attendance" (opens session selector)
- Secondary CTAs: "Export Attendance Report" | "Generate Certificates for Session" | "Upload Attendance CSV"

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Mandatory compliance sessions with absentees — unresolved | "[N] staff member(s) missed mandatory compliance training. HR Director and POCSO Coordinator notified." | Red |
| Sessions completed but attendance not yet marked > 48 hours | "[N] completed session(s) have no attendance recorded yet." | Orange |
| Certificates not generated for sessions with attendance marked > 7 days | "[N] session(s) are ready for certificate generation but certificates have not been issued." | Yellow |
| CSV upload failed | "Attendance CSV upload failed. Review format and retry." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Sessions with Attendance Recorded | Count of completed sessions with attendance marked | Neutral blue | — |
| Total Staff Attended This Month | Sum of Present + Late across all sessions this month | Green if > 0 | — |
| Mandatory Training Absentees | Count of staff who missed mandatory sessions (unresolved) | Red if > 0 | Filters to mandatory absentees |
| Certificates Generated | Count of certificates issued this month | Green | Filters to certificate view |
| CPD Hours Credited (This Month) | Sum of CPD hours credited to staff this month | Green | — |
| Absentees Needing Reschedule | Count of absent staff from mandatory sessions with no make-up scheduled | Orange if > 0 | Filters to reschedule queue |

---

## 5. Main Table — Session Attendance Summary

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Session Name | Text (link to per-session roster drawer) | Yes | Yes (search) |
| Date | Date | Yes | Yes (date range) |
| Branch | Text | Yes | Yes (dropdown) |
| Enrolled | Integer | Yes | No |
| Attended (Present + Late) | Integer | Yes | No |
| Attendance % | Percentage (Attended / Enrolled × 100) | Yes | Yes (< 75% filter) |
| Certificates Generated | Integer / "—" | No | Yes (generated / not generated) |
| Mandatory | Boolean chip (Yes / No) | Yes | Yes |
| Status | Chip (Attendance Marked / Not Marked / Certificates Issued) | Yes | Yes |
| Actions | View Roster / Mark Attendance / Generate Certificates / Download Report | No | No |

### 5.1 Filters
- Status: All | Attendance Marked | Attendance Not Marked | Certificates Issued
- Mandatory: All | Mandatory Only | Optional Only
- Branch: All branches (dropdown)
- Attendance %: All | Below 75% | Below 50%
- Date Range: This Month | Last 30 Days | Last 90 Days | Custom

### 5.2 Search
Search by session name. Minimum 2 characters, 400ms debounce.

### 5.3 Pagination
Server-side pagination, 20 sessions per page. Navigation controls with total session count displayed.

---

## 6. Drawers

### 6.1 Drawer: Per-Session Attendance Roster
Triggered by "View Roster" or session name click. Shows enrolled staff list for the selected session. Columns: Staff Name, Branch, Role, Attendance Status (Present / Absent / Late / Not Marked), Marked By, Marked At, CPD Hours Credited, Certificate Status (Issued / Pending / Not Eligible). If Mandatory session: non-attendance flagged in red with "Needs Reschedule" label. Edit icon per row to update status (Present / Absent / Late). "Bulk Mark All Present" and "Bulk Mark All Absent" buttons for initial data entry. For Online sessions: auto-tracked status shown with login duration (e.g., "Auto: Present — 92 min / 90 min session"). Override available with reason.

### 6.2 Drawer: Mark Attendance (Session Select + Batch Entry)
Step 1: Select Session (dropdown of Completed sessions with no attendance marked). Step 2: Choose input method — Manual (individual toggles, same as roster drawer) or CSV Upload (download template, upload file). Step 3: Review summary before saving. On Submit: all attendance records saved, CPD hours credited for eligible staff, compliance alerts fired for mandatory absentees.

### 6.3 Drawer: Generate Certificates (Per Session)
Triggered from "Generate Certificates" action. Shows list of attendance-eligible staff (attendance ≥ 75%). Checkbox list for selection (all checked by default). Certificate preview available (PDF). "Generate for Selected" button. On Submit: certificates created, linked to staff profiles (page 14 Documents tab), CPD hours confirmed credited, session status → Certificates Issued.

### 6.4 Drawer: Reschedule Make-Up Session
Triggered from absentee list for mandatory sessions. Fields: Select Absentee Staff (pre-filled), Select Make-Up Session (dropdown of upcoming sessions for same program), Notes. On Save: staff enrolled in make-up session, original non-attendance alert linked to make-up enrollment (alert resolves once make-up attendance is marked Present).

### 6.5 Modal: Compliance Non-Attendance Alert Confirmation
Triggered automatically when a mandatory session attendance is saved with any Absent records. Lists all absent staff names. "Send Alert to HR Director and POCSO Coordinator" (pre-checked, cannot uncheck for POCSO sessions). Confirm / Cancel.

---

## 7. Charts

**Monthly Attendance Rate Trend — Line Chart:** X-axis = last 6 months; Y-axis = average attendance percentage across all sessions. A second line shows mandatory-only attendance rate. If mandatory attendance rate dips below 75%, line turns red. Rendered via Chart.js. Toggle: "Show Trend / Hide". Positioned below the table.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Attendance marked (manual) | "Attendance saved for '[Session Name]'. CPD hours credited." | Success | 5s |
| Attendance CSV uploaded | "Attendance CSV processed. [N] records updated." | Success | 5s |
| CSV upload error | "CSV upload failed. Check the format using the template and retry." | Error | 6s |
| Certificates generated | "[N] certificate(s) generated for '[Session Name]'." | Success | 5s |
| Compliance alert sent | "Non-attendance alert sent to HR Director and POCSO Coordinator." | Warning | 5s |
| Make-up session enrolled | "[Staff Name] enrolled in make-up session '[Session Name]'." | Info | 4s |
| Attendance status updated | "Attendance status updated for [Staff Name]." | Success | 4s |
| Report downloaded | "Attendance report downloaded." | Success | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No completed sessions | "No Completed Sessions Yet" | "Attendance can only be recorded for sessions that have been completed." | View Sessions |
| Filter returns no sessions | "No Matching Sessions" | "Adjust your filters to find the session you need." | Clear Filters |
| Session roster — no enrolled staff | "No Staff Were Enrolled" | "This session had no enrolled participants." | — |
| No mandatory absentees | "No Mandatory Training Absentees" | "All staff have attended their mandatory compliance training sessions." | — |
| No certificates pending | "All Certificates Issued" | "Certificates have been generated for all eligible staff." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI card skeletons (6) + table row skeletons (12) |
| Filter change | Table body row skeletons |
| Roster drawer open | Staff row skeletons (15 rows) |
| CSV upload processing | Progress bar + "Processing..." text |
| Certificate generation | Spinner + "Generating certificates..." with progress count |
| Compliance alert modal | Modal appears with spinner briefly before staff list renders |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) | T&D Manager (45) | POCSO Coordinator (50) | Read-Only Roles (42, 46) |
|---|---|---|---|---|
| Mark Attendance button | Visible | Visible + enabled | Hidden | Hidden |
| Upload CSV button | Visible | Visible + enabled | Hidden | Hidden |
| Generate Certificates | Visible | Visible | Hidden | Hidden |
| View Roster (read) | Visible | Visible | POCSO sessions only | Visible |
| Edit attendance status | Visible | Visible | Hidden | Hidden |
| Reschedule Make-Up | Visible | Visible | Hidden | Hidden |
| Compliance alerts view | Visible | Visible | Visible | Hidden |
| Export Attendance Report | Visible | Visible | Hidden | Hidden |
| CPD Hours Summary link | Visible | Visible | Hidden | Visible (46 only) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/training/attendance/` | JWT | List session attendance summaries |
| GET | `/api/v1/hr/training/attendance/{session_id}/roster/` | JWT | Fetch per-session attendance roster |
| POST | `/api/v1/hr/training/attendance/{session_id}/` | JWT | Submit manual attendance for session |
| PATCH | `/api/v1/hr/training/attendance/{session_id}/{staff_id}/` | JWT | Update individual attendance status |
| POST | `/api/v1/hr/training/attendance/{session_id}/csv/` | JWT | Upload attendance CSV |
| POST | `/api/v1/hr/training/attendance/{session_id}/certificates/` | JWT | Generate certificates for session |
| POST | `/api/v1/hr/training/attendance/{session_id}/alert/` | JWT | Send compliance non-attendance alert |
| POST | `/api/v1/hr/training/attendance/makeup/` | JWT | Enroll absentee in make-up session |
| GET | `/api/v1/hr/training/attendance/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/training/attendance/chart/` | JWT | Monthly attendance trend chart data |
| GET | `/api/v1/hr/training/attendance/export/` | JWT | Export attendance report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/training/attendance/?q={val}` | `#attendance-table-body` | innerHTML |
| Status filter | change | GET `/api/v1/hr/training/attendance/?status={val}` | `#attendance-table-body` | innerHTML |
| Mandatory filter | change | GET `/api/v1/hr/training/attendance/?mandatory={val}` | `#attendance-table-body` | innerHTML |
| Branch / date filter | change | GET `/api/v1/hr/training/attendance/?branch={}&date_from={}&date_to={}` | `#attendance-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/training/attendance/?page={n}` | `#attendance-table-body` | innerHTML |
| View Roster drawer | click | GET `/group/hr/training/attendance/{session_id}/roster/drawer/` | `#drawer-container` | innerHTML |
| Mark Attendance drawer | click | GET `/group/hr/training/attendance/mark/drawer/` | `#drawer-container` | innerHTML |
| Individual status update | change | PATCH `/api/v1/hr/training/attendance/{session_id}/{staff_id}/` | `#roster-row-{staff_id}` | outerHTML |
| Attendance submit (manual) | submit | POST `/api/v1/hr/training/attendance/{session_id}/` | `#session-row-{session_id}` | outerHTML |
| CSV upload | change (file input) | POST `/api/v1/hr/training/attendance/{session_id}/csv/` | `#upload-status` | innerHTML |
| Generate Certificates drawer | click | GET `/group/hr/training/attendance/{session_id}/certificates/drawer/` | `#drawer-container` | innerHTML |
| Certificate generate submit | submit | POST `/api/v1/hr/training/attendance/{session_id}/certificates/` | `#session-row-{session_id}` | outerHTML |
| Compliance alert modal | after:POST attendance | GET `/group/hr/training/attendance/{session_id}/alert/modal/` | `#modal-container` | innerHTML |
| Chart toggle | click | GET `/group/hr/training/attendance/chart/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
