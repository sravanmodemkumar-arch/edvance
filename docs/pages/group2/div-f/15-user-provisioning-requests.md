# 15 — User Provisioning Requests

- **URL:** `/group/it/users/provisioning/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) — Primary owner

---

## 1. Purpose

The User Provisioning Requests page is the structured gateway through which branches request new EduForge user accounts. A core governance decision in EduForge is that branch principals and branch IT administrators cannot create group-level accounts autonomously — every new account that requires G3 or G4 access must be requested through this workflow and reviewed by the Group IT Admin before the account is provisioned. This ensures that every user account in the group is traceable to an approved, documented request.

The queue on this page represents all such requests across all branches — pending review, under clarification, approved and provisioned, or rejected. For standard account requests (branch teacher, support staff), the IT Admin reviews the request and either approves it (triggering immediate provisioning via the Account Manager backend) or rejects it with a documented reason. For urgent requests (principal marks Priority: Urgent), the system flags the request with an amber banner and the IT Admin is expected to act within 4 hours.

This page also creates accountability on the requesting side: branch principals can only request roles and access levels appropriate to the position described in their justification. The IT Admin can request clarification if the access level requested seems disproportionate. All communication is logged within the request record.

The provisioning flow connects directly to the Account Manager (File 13): when a request is approved, the system either auto-provisions the account (if all fields are complete) or opens the Create Account drawer pre-filled with the request details, requiring the IT Admin to confirm before finalising. This two-click approval-to-provisioning path reduces friction while preserving human oversight.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + write (review, approve, reject, provision) | Primary operator |
| Group IT Director | G4 | Full read + escalation visibility | Can view all requests; approves escalated cases |
| Group IT Support Executive | G3 | Read-only | Can view status of requests for support purposes |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → User Management → Provisioning Requests
```

### 3.2 Page Header
- **Title:** `User Provisioning Requests`
- **Subtitle:** `[N] Pending · [N] Approved Today · [N] Total This Month`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `Export` · `Advanced Filters`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Urgent requests pending > 4 hours | "[N] Urgent provisioning request(s) have been waiting more than 4 hours. Immediate review required." | Amber |
| Standard requests pending > 48 hours | "[N] provisioning request(s) have been pending for more than 48 hours without action." | Red |
| Requests in "Pending Clarification" > 72 hours with no branch response | "[N] requests are awaiting branch clarification for more than 72 hours. Follow up or close." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Pending Requests | Requests with status = Pending (awaiting review) | Red if > 10, Amber if > 5, Green if ≤ 5 | Filtered by Pending |
| Approved Today | Requests approved on today's date | Blue | Filtered by Approved + today |
| Rejected | Requests with status = Rejected (all time, or current month toggle) | Blue | Filtered by Rejected |
| Avg Processing Time | Average hours between Submitted and Approved/Rejected for last 30 days | Green if < 4h, Amber if 4–24h, Red if > 24h | No drill-down |

---

## 5. Main Table — Provisioning Requests

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Request # | Text (e.g., PRQ-00142) | Yes | No |
| Branch | Text | Yes | Yes (multi-select) |
| Requested By | Text (Branch Principal or Branch IT Admin name + role) | Yes | No |
| Role Requested | Text | Yes | Yes (text search) |
| User Name | Text (name of person to be provisioned) | Yes | Yes (text search) |
| Email | Text (partially masked) | No | No |
| Submitted At | DateTime (relative: "2 hours ago") | Yes | Yes (date range) |
| Priority | Badge (Standard / Urgent) | Yes | Yes |
| Status | Badge (Pending / Under Review / Pending Clarification / Approved / Rejected / Provisioned) | Yes | Yes (multi-select) |
| Actions | Review / Approve / Reject | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All group branches |
| Status | Checkbox | Pending / Under Review / Pending Clarification / Approved / Rejected / Provisioned |
| Priority | Checkbox | Standard / Urgent |
| Submitted Date Range | Date range picker | Any range |
| Access Level Requested | Checkbox | G0 / G1 / G2 / G3 / G4 / G5 |

### 5.2 Search
- Full-text search: Request #, User Name, Requested By, Role Requested, Branch
- 300ms debounce

### 5.3 Pagination
- Server-side · 25 rows/page · Sorted by Submitted At descending by default (newest first)

---

## 6. Drawers

### 6.1 Drawer: `provisioning-review` — Review Request
- **Trigger:** Actions → Review (or click Request # anywhere in table)
- **Width:** 480px
- **Content sections:**
  - **Request Summary:** Request #, submitted at, branch, submitted by (name + role + contact)
  - **Requested Account Details:**
    - Full Name (as to be created)
    - Mobile Number
    - Email Address
    - Desired Role / Designation
    - Requested Access Level (badge)
    - Requested Branch
  - **Justification:** Free-text justification provided by the branch
  - **Attachments:** Any documents uploaded (e.g., appointment letter, HR approval) with download links
  - **Requested Role Details:** Inline read-only view of what permissions the requested access level/role carries (pulled from permission matrix)
  - **Timeline:** All status changes for this request with timestamps and actors
  - **Communication Thread:** Existing clarification messages exchanged between IT Admin and branch
- **Action buttons at bottom:**
  - Approve → triggers Approve modal
  - Reject → triggers Reject modal
  - Request Clarification → opens inline message field; sends notification to branch principal

### 6.2 Modal: Approve Request
- **Trigger:** Approve button in review drawer
- **Type:** Centered modal (440px)
- **Content:** "Approve provisioning request PRQ-[N] for [User Name] at [Branch] with role [Role] (Access Level [G-level])?"
- **Option:** Auto-provision immediately (checkbox, default checked) — creates account and sends OTP automatically; if unchecked, status becomes Approved but admin manually provisions via Account Manager
- **Button:** Confirm Approval (green) · Cancel

### 6.3 Modal: Reject Request
- **Trigger:** Reject button in review drawer
- **Type:** Centered modal (440px)
- **Fields:**
  - Rejection Reason (required, dropdown: Inappropriate Access Level Requested / Duplicate Account Exists / Insufficient Justification / Role Not Recognised / Other)
  - Additional Notes (required if "Other", textarea) (required if Rejection Reason = "Other"; min 20 characters)
  - Notify Requesting Branch (checkbox, default checked)
- **Buttons:** Confirm Rejection (red) · Cancel

### 6.4 Inline Clarification (within review drawer)
- Not a separate drawer — part of the review drawer's communication thread section
- IT Admin types a question; branch principal receives a WhatsApp/in-app notification
- Branch principal's response appears in the thread on next drawer open (HTMX poll or manual refresh)
- Status changes to "Pending Clarification" while waiting

---

## 7. Charts

No dedicated chart on this page. KPI cards provide the essential metrics. The IT Analytics dashboard carries provisioning trend charts if required.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Request approved (auto-provision) | "Request PRQ-[N] approved. Account created for [Name] at [Branch]. OTP sent." | Success | 5s |
| Request approved (manual provision) | "Request PRQ-[N] approved. Proceed to Account Manager to provision the account." | Info | 5s |
| Request rejected | "Request PRQ-[N] rejected. Branch principal at [Branch] has been notified." | Warning | 4s |
| Clarification sent | "Clarification requested from [Branch]. Request status updated to Pending Clarification." | Info | 4s |
| Duplicate account detected on approval | "Approval blocked: an account for this mobile number already exists. Review in User Directory." | Error | 6s |
| Export triggered | "Provisioning requests export is being prepared." | Info | 3s |
| Approval failed | Error: `Could not approve PRQ-[N]. Review request details and try again.` | Error | 5s |
| Rejection failed | Error: `Could not reject PRQ-[N]. Please try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No pending requests | "All Clear — No Pending Requests" | "There are no provisioning requests awaiting review. All requests have been processed." | — |
| No results for filters | "No Matching Requests" | "No provisioning requests match the selected filters. Adjust branch, status, or date range." | Clear Filters |
| No requests ever (new deployment) | "No Provisioning Requests Yet" | "Provisioning requests submitted by branch principals will appear here for review." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 4 KPI shimmer cards + table skeleton (15 rows) |
| Filter / search applied | Table skeleton; KPI bar does not reload |
| Review drawer open | 480px drawer skeleton; sections load progressively (attachments loaded last) |
| Approve modal confirm | Button spinner; on success drawer closes, table row status badge updates to Approved/Provisioned |
| Reject modal confirm | Button spinner; modal closes, table row updates |
| Clarification send | Send button spinner; thread section reloads |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | IT Support Executive (G3) |
|---|---|---|---|
| Full table | Visible | Visible | Visible |
| Review action | Visible | Visible | Hidden (read-only view only) |
| Approve action | Visible | Visible | Hidden |
| Reject action | Visible | Visible | Hidden |
| Request Clarification | Visible | Visible | Hidden |
| Attached documents | Visible | Visible | Hidden |
| Requested Role permissions inline view | Visible | Visible | Hidden |
| Export button | Visible | Visible | Hidden |
| Pending Approvals banner | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/provisioning/` | JWT (G3+) | Paginated provisioning request list |
| GET | `/api/v1/it/provisioning/{id}/` | JWT (G3+) | Full request detail with communication thread |
| POST | `/api/v1/it/provisioning/{id}/approve/` | JWT (G4) | Approve request; optionally auto-provision |
| POST | `/api/v1/it/provisioning/{id}/reject/` | JWT (G4) | Reject request with reason |
| POST | `/api/v1/it/provisioning/{id}/clarify/` | JWT (G4) | Send clarification message to branch |
| GET | `/api/v1/it/provisioning/kpis/` | JWT (G3+) | KPI card values |
| GET | `/api/v1/it/provisioning/export/` | JWT (G4) | Async export of filtered request list |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/provisioning/kpis/` | `#kpi-bar` | `innerHTML` |
| Load requests table | `load` | GET `/api/v1/it/provisioning/` | `#requests-table` | `innerHTML` |
| Search requests | `input` (300ms debounce) | GET `/api/v1/it/provisioning/?q=...` | `#requests-table` | `innerHTML` |
| Apply filters | `change` | GET `/api/v1/it/provisioning/?branch=...&status=...` | `#requests-table` | `innerHTML` |
| Paginate | `click` on page control | GET `/api/v1/it/provisioning/?page=N` | `#requests-table` | `innerHTML` |
| Open review drawer | `click` on Request # | GET `/api/v1/it/provisioning/{id}/` | `#review-drawer` | `innerHTML` |
| Confirm approval | `click` on Confirm Approval | POST `/api/v1/it/provisioning/{id}/approve/` | `#requests-table` | `innerHTML` |
| Confirm rejection | `click` on Confirm Rejection | POST `/api/v1/it/provisioning/{id}/reject/` | `#requests-table` | `innerHTML` |
| Send clarification | `click` on Send | POST `/api/v1/it/provisioning/{id}/clarify/` | `#clarification-thread` | `afterbegin` |
| Poll clarification thread | `every 30s` (when drawer open) | GET `/api/v1/it/provisioning/{id}/clarification-thread/` | `#clarification-thread` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
