# 14 — Student Wellbeing Tracker

> **URL:** `/group/health/wellbeing/`
> **File:** `14-student-wellbeing-tracker.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Mental Health Coordinator (primary)

---

## 1. Purpose

Active monitoring dashboard for all students currently under mental health care or flagged as at-risk anywhere in the group. This page is the operational heartbeat of the mental health programme — it ensures no at-risk student falls through the cracks between sessions, no crisis case goes without action for 24 hours, and no counsellor is overburdened with high-risk cases beyond safe limits.

Where the Counselling Session Register is a historical log of what happened in each session, the Wellbeing Tracker is a live case-management view — showing current status, pending actions, risk escalations, and intervention progress. Each case in the tracker is a student whose wellbeing requires active, structured monitoring beyond a single counselling visit.

The tracker feeds from the session register: when a session is logged with Risk Level = Medium, High, or Crisis, a wellbeing case is automatically created or updated. Cases are closed only when the Mental Health Coordinator explicitly closes them with a documented outcome.

CONFIDENTIAL — restricted to Mental Health Coordinator at group level. Branch counsellors access their own branch cases via the branch-level portal. Student names are never shown to any other role.

Scale: 50–500 active cases during examination periods. Large groups may carry 100+ active cases simultaneously. System must support concurrent real-time updates as counsellors log new sessions.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Mental Health Coordinator | G3 | Full — view all cases with student names, create, update risk level, close cases | Primary owner |
| Branch Counsellor | Branch | Own branch cases — via branch portal (not this page) | Does not access this group-level page |
| Group Medical Coordinator | G3 | Case counts only — no clinical detail, no student identifiers | Aggregate view only |
| CEO / Chairman | Group | Aggregate counts only — no individual students | Executive summary widget only |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('mental_health_coordinator', 'medical_coordinator', 'ceo', 'chairman')` with role-based queryset and serialiser masks. Medical Coordinator and CEO/Chairman receive only aggregate count responses, never row-level records.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Student Wellbeing Tracker
```

### 3.2 Page Header
- **Title:** `Student Wellbeing Tracker`
- **Subtitle:** `[N] Active Cases · [N] High Risk · [N] Crisis · [N] Follow-ups Due Today`
- **Right controls:** `+ Open New Case` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity | Display Rule |
|---|---|---|---|
| Crisis case with no action in 24h | "URGENT: [N] crisis case(s) have had no action recorded in the last 24 hours." | Red — permanent, non-dismissable | Shown whenever condition is true; cannot be dismissed until case actioned |
| High-risk case with no session in 7 days | "[N] high-risk students have had no session in 7 or more days." | Red | |
| Multiple at-risk students from same branch/class | "Possible systemic issue: [N] at-risk students from [Branch/Class]. Investigation recommended." | Amber | Threshold: ≥ 3 students from same class |
| Counsellor handling > 20 active high-risk cases | "[Counsellor] has [N] active high-risk cases — above the recommended maximum of 20." | Amber | |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Active Cases | All cases with status = Active or Monitoring | Blue always |
| High Risk Cases | Active cases with risk level = High | Yellow if > 0 · Red if > 5 |
| Crisis Cases | Active cases with risk level = Crisis | Green = 0 · Red if any (critical) |
| Follow-ups Due Today | Cases where next session date = today and session not yet logged | Green = 0 · Yellow 1–5 · Red > 5 |
| Cases Closed This Month | Cases moved to Closed status in current calendar month | Blue always |
| Average Resolution Time (days) | Mean days from case open to close, cases closed this month | Green ≤ 30 · Yellow 31–60 · Red > 60 |

---

## 5. Main Table — Active Wellbeing Cases

> **Confidentiality note:** Student names are visible only to the Mental Health Coordinator. All other roles (if granted any access) see `[RESTRICTED]`. This is enforced at the API serialiser layer.

**Search:** Case ID, branch name, counsellor name. 300ms debounce.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Risk Level | Checkbox | Low / Medium / High / Crisis |
| Case Status | Checkbox | Active / Monitoring / Resolved / Referred Externally |
| Follow-up Due | Radio | All / Today / This Week / Overdue |
| Concern Category | Checkbox | Academic / Family / Peer / Hostel / Identity / Trauma / Other |
| Hostel / Day Scholar | Radio | All / Hostel / Day Scholar |
| Assigned Counsellor | Single-select | All counsellors |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Case ID | ✅ | System reference e.g. WB-2026-00341 |
| Branch | ✅ | |
| Class | ✅ | |
| Hostel / Day Scholar | ✅ | Hostel (blue) / Day Scholar (grey) badge |
| Risk Level | ✅ | Colour badge: Low (green) / Medium (amber) / High (red) / Crisis (flashing red with animation) |
| Primary Concern | ✅ | Concern category badge |
| Assigned Counsellor | ✅ | Name |
| Sessions Completed | ✅ | Count of sessions logged for this case |
| Next Session | ✅ | Date; red if today and not yet done; amber if tomorrow |
| Days Since Last Session | ✅ | Number; red if > 7 and risk ≥ High |
| Case Status | ✅ | Active / Monitoring / Resolved / Referred Externally — badge |
| Actions | ❌ | View · Update · Escalate · Close |

**Default sort:** Risk Level descending (Crisis first), then Days Since Last Session descending.
**Pagination:** Server-side · 25/page.
**Bulk actions:** Export selected (Mental Health Coordinator only, audit-logged).

---

## 6. Drawers / Modals

### 6.1 Drawer — `case-detail` (720px, right side)

Triggered by **View** or case ID link. Student name displayed in drawer header (Mental Health Coordinator only).

**Tabs:**

#### Tab 1 — Overview
| Field | Notes |
|---|---|
| Case ID | |
| Student Name | Mental Health Coordinator only; others see [RESTRICTED] |
| Student ID | |
| Class / Section / Branch | |
| Hostel / Day Scholar | |
| Case Opened Date | |
| Referred By | Self / Teacher / Parent / Principal / Doctor / Peer |
| Presenting Problem | Free text — initial reason for case opening |
| Student Background (Confidential) | Relevant contextual information (family situation, academic status, prior history) |
| Current Risk Level | Badge — with last-updated date and who updated |
| Assigned Counsellor | |
| Last Reviewed | Date and reviewer name |
| Case Status | Active / Monitoring / Resolved / Referred Externally |

#### Tab 2 — Intervention Plan
| Field | Notes |
|---|---|
| Counselling Goals | Numbered list — what the intervention aims to achieve |
| Planned Interventions | Checklist: CBT / Person-Centred / Crisis Management / Psychoeducation / Group Therapy / External Referral |
| Timeline | Expected duration and review milestones |
| Parent / Family Involvement | Yes / No / Partial — with notes |
| Academic Accommodations Recommended | Checkbox list: Exam postponement / Extra time in exams / Reduced workload / Excused from PE / Other (free text) |
| Academic Accommodation Status | Requested / Approved / Implemented / Not Required |
| External Referral Plan | Psychiatrist / NIMHANS / NGO — name + status |
| Intervention Plan Last Updated | Date + author |

#### Tab 3 — Session Timeline
All sessions logged for this case in reverse chronological order.

| Column | Notes |
|---|---|
| Session Date | |
| Duration (mins) | |
| Risk Level at Session | Badge |
| Session Type | Individual / Group / Crisis |
| Key Notes | 1–2 sentence summary from session notes |
| Outcome Code | Resolved / Ongoing / Referred / Escalated |
| Follow-up Done | Yes / No |

Link to full session record for each row (opens session drawer from session register).

#### Tab 4 — Risk History
| Feature | Notes |
|---|---|
| Risk Level Change Chart | Line chart: X = date, Y = risk level (1=Low, 2=Medium, 3=High, 4=Crisis). Each data point is a session or a manual risk update. |
| Change Log Table | Date · Changed From · Changed To · Reason · Changed By |
| Triggers for Escalation | Free text notes on what caused each upward shift |
| Triggers for De-escalation | Free text notes on improvements noted |

#### Tab 5 — Notifications
All notifications sent as part of this case.

| Column | Notes |
|---|---|
| Date / Time | |
| Sent To | Parent / Principal / School Doctor / Emergency Services |
| Sent By | |
| Method | In-platform message / Phone call logged / Email |
| Content Summary | First 100 chars of message |
| Acknowledged | Yes / No / Unknown |

"Send Notification" button at bottom of tab → opens `notify-principal` modal or a generic notification composer.

---

### 6.2 Drawer — `case-open` (640px, right side)

Triggered by **+ Open New Case**.

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select | Required |
| Student Search | Autocomplete (name + ID) | Required; debounce 300ms |
| Concern Category | Single-select: Academic / Family / Peer / Hostel / Identity / Trauma / Other | Required |
| Risk Level (Initial Assessment) | Radio — Low / Medium / High / Crisis | Required |
| Referred By | Radio: Self / Teacher / Parent / Principal / Doctor / Peer | Required |
| Referral Date | Date picker | Required |
| Presenting Problem | Textarea (max 1,500 chars) | Required |
| Student Background (Confidential) | Textarea (max 1,000 chars) | Optional |
| Assign Counsellor | Single-select (counsellors assigned to this branch) | Required |
| Schedule First Session | Date picker | Required |
| First Session Type | Radio — Individual / Group | Required |
| Parent / Family Involvement | Radio — Yes / No / To be discussed | Required |
| Initial Notes | Textarea (max 1,000 chars) | Optional |

> If Risk Level = Crisis: warning banner shown: *"You are opening a Crisis case. An escalation notification will be sent immediately upon saving."*

**Footer:** `Cancel` · `Open Case`

Opening a crisis case automatically triggers the same notifications as `escalate-crisis` in the session register.

---

### 6.3 Drawer — `risk-level-update` (480px, right side)

Triggered by **Update** action or Risk Level badge click in table.

| Field | Type | Validation |
|---|---|---|
| Case ID | Read-only | |
| Student (restricted) | Read-only | Name visible to Mental Health Coordinator |
| Current Risk Level | Read-only badge | |
| New Risk Level | Radio — Low / Medium / High / Crisis | Required |
| Reason for Change | Textarea (max 500 chars) | Required |
| Protective Factors (if de-escalating) | Textarea (max 300 chars) | Required if new level < current level |
| Actions Triggered by this Change | Auto-populated based on new level: e.g., "Crisis: notify Principal and parents" | Read-only; confirms actions |
| Log Note | Textarea (max 300 chars) | Optional |

**Footer:** `Cancel` · `Update Risk Level`

If escalating to Crisis: modal confirm step added before save: *"Escalating to Crisis will send immediate notifications. Confirm?"*

---

### 6.4 Modal — `close-case` (460px, centred)

Triggered by **Close** action.

| Field | Type | Validation |
|---|---|---|
| Case ID | Read-only | |
| Current Risk Level | Read-only | Must be Low or Medium to close; High/Crisis requires override reason |
| Closure Reason | Radio — Resolved / Transferred to External Provider / Student Left Institution / No Further Concern | Required |
| Outcome | Radio — Improved / Stable / Referred Externally / Unknown | Required |
| Final Notes | Textarea (max 1,000 chars) | Required |
| Follow-up Recommendation | Textarea (max 300 chars) | Optional — for future reference if student re-presents |
| Notify Counsellor | Toggle — Yes / No (default Yes) | Required |

**Footer:** `Cancel` · `Close Case`

After close: case moves to Resolved/Closed status; no longer appears in Active Cases table; available in case history/archive filter.

---

### 6.5 Modal — `notify-principal` (440px, centred)

Triggered from Notifications tab or automatically for High/Crisis risk level changes.

| Field | Type | Validation |
|---|---|---|
| Case ID | Read-only | |
| Branch Principal | Read-only — auto-identified from branch | |
| Auto-drafted Message | Editable textarea — pre-populated with: "A student at your branch is currently receiving counselling support with a [risk level] concern. No clinical details are shared. Please ensure a supportive environment is maintained. Contact the Mental Health Coordinator for more information." | Required |
| Mental Health Coordinator Review | Required confirmation toggle — "I have reviewed this message and it contains no identifiable clinical information." | Required |
| Send Method | Radio — In-platform message / Email | Required |

**Footer:** `Cancel` · `Send Notification`

After send: notification logged in Notifications tab with timestamp and coordinator name.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Case opened | "Wellbeing case opened. Counsellor notified." | Success |
| Case opened (Crisis) | "Crisis case opened. Escalation notifications sent." | Warning (prominent) |
| Risk level updated | "Risk level updated to [Level] for Case [ID]." | Success |
| Risk level escalated to Crisis | "Risk level escalated to Crisis. Notifications sent." | Warning (prominent) |
| Case closed | "Case [ID] closed. Outcome recorded." | Success |
| Principal notified | "Notification sent to Branch Principal at [Branch]." | Success |
| Follow-up session scheduled | "Next session scheduled for [Date] with [Counsellor]." | Success |
| Export triggered | "Export is being prepared. Audit log entry created." | Info |
| Save failed — high risk override missing | "Closing a High or Crisis case requires an override reason." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No active cases | "No active wellbeing cases." | "Active cases will appear here when opened via the Counselling Session Register or manually." | `+ Open New Case` button |
| No crisis cases | "No crisis cases active." | — | — |
| No follow-ups due today | "No follow-ups due today." | — | — |
| No results for current filters | "No cases match your current filters." | "Try adjusting your filters." | `Clear Filters` |
| Risk history — no changes | "No risk level changes recorded." | "Risk changes will appear here as the case progresses." | — |
| Notifications tab — none sent | "No notifications have been sent for this case." | — | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: crisis alert banner check (spinner) + KPI bar (6 grey cards) + table (8 grey rows × 11 columns) |
| Filter / search apply | Table body spinner overlay; KPI cards update separately |
| Case detail drawer open | Drawer skeleton with student name placeholder (loading) + 5 tab skeletons |
| Risk history chart (Tab 4) | Chart placeholder with spinner while time-series data loads |
| Session timeline tab | Table skeleton (5 rows) while sessions load |
| Risk level update drawer save | Submit button spinner; all inputs disabled |
| Crisis notification sending | Spinner in modal footer + "Sending crisis notifications…"; re-enabled after confirmation |
| Close case modal | Submit spinner; disabled to prevent double-close |

---

## 10. Role-Based UI Visibility

| UI Element | Mental Health Coordinator | Medical Coordinator | CEO / Chairman | Branch Counsellor (own branch) |
|---|---|---|---|---|
| Active cases table — full rows | ✅ | ❌ | ❌ | Via branch portal, not this page |
| Student names in table | ✅ | ❌ | ❌ | Via branch portal |
| Case Detail drawer — all tabs | ✅ | ❌ | ❌ | Via branch portal |
| Student Profile in Overview | ✅ | ❌ | ❌ | Via branch portal |
| Intervention Plan tab | ✅ | ❌ | ❌ | Via branch portal |
| Session Timeline tab | ✅ | ❌ | ❌ | Via branch portal |
| Risk History chart | ✅ | ❌ | ❌ | Via branch portal |
| Notifications tab | ✅ | ❌ | ❌ | Via branch portal |
| + Open New Case button | ✅ | ❌ | ❌ | Via branch portal |
| Update Risk Level | ✅ | ❌ | ❌ | Via branch portal |
| Close Case | ✅ | ❌ | ❌ | ❌ |
| Notify Principal | ✅ | ❌ | ❌ | ❌ |
| Export button | ✅ | ❌ | ❌ | ❌ |
| KPI bar | ✅ Full | Aggregate counts only | Aggregate counts only | Via branch portal |
| Crisis alert banner | ✅ | ❌ | ❌ | Via branch portal (own branch) |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/wellbeing/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/wellbeing/` | List active wellbeing cases (paginated, filtered, masked) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/wellbeing/` | Open a new wellbeing case | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/wellbeing/{case_id}/` | Retrieve full case detail | Mental Health Coordinator |
| PATCH | `/api/v1/group/{group_id}/health/wellbeing/{case_id}/` | Update case fields | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/wellbeing/kpi/` | KPI summary bar data | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/wellbeing/{case_id}/risk-level/` | Update risk level with reason | Mental Health Coordinator |
| POST | `/api/v1/group/{group_id}/health/wellbeing/{case_id}/close/` | Close case with outcome | Mental Health Coordinator |
| POST | `/api/v1/group/{group_id}/health/wellbeing/{case_id}/notify-principal/` | Send notification to branch principal | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/wellbeing/{case_id}/sessions/` | Session timeline for this case | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/wellbeing/{case_id}/risk-history/` | Risk level change history | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/wellbeing/{case_id}/notifications/` | Notification history for this case | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/wellbeing/student-search/` | Autocomplete for case opening | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/wellbeing/export/` | Export active cases CSV (audit-logged) | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/wellbeing/alerts/` | Fetch active alert conditions (including permanent crisis alert) | JWT + role check |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `risk_level` | str[] | `low`, `medium`, `high`, `crisis` |
| `status` | str[] | `active`, `monitoring`, `resolved`, `referred` |
| `follow_up_due` | str | `today`, `this_week`, `overdue` |
| `concern_category` | str[] | Category slugs |
| `hostel` | bool | Hostel / day scholar filter |
| `counsellor` | int | Filter by counsellor |
| `page` | int | Page number |
| `page_size` | int | 25 default, max 100 |
| `search` | str | Case ID, branch, or counsellor |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Filter form apply | `hx-get="/api/.../wellbeing/"` `hx-trigger="change"` `hx-target="#cases-table-body"` `hx-include="#filter-form"` | Table replaced; KPI bar updated |
| Pagination | `hx-get="/api/.../wellbeing/?page={n}"` `hx-target="#cases-table-body"` `hx-push-url="true"` | Page swap |
| Case detail drawer open | `hx-get="/api/.../wellbeing/{case_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Overview tab default |
| Drawer tab switch | `hx-get="/api/.../wellbeing/{case_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped |
| Risk history chart tab | `hx-get="/api/.../wellbeing/{case_id}/risk-history/"` `hx-target="#risk-chart-container"` `hx-trigger="click[tab='risk_history']"` | Chart data loaded and rendered on tab click |
| Session timeline tab | `hx-get="/api/.../wellbeing/{case_id}/sessions/"` `hx-target="#session-timeline-content"` | Session list loaded on tab click |
| Risk level update drawer save | `hx-patch="/api/.../wellbeing/{case_id}/risk-level/"` `hx-target="#risk-badge-{case_id}"` `hx-swap="outerHTML"` `hx-on::after-request="closeDrawer(); fireToast();"` | Risk badge in table row updated inline; drawer closed |
| Risk level escalation to Crisis — confirm step | Confirm dialog rendered via `hx-confirm` attribute before submit | User confirms before crisis escalation is posted |
| Case close modal submit | `hx-post="/api/.../wellbeing/{case_id}/close/"` `hx-target="#case-row-{case_id}"` `hx-swap="outerHTML"` | Row removed from active table (moved to closed); modal closed; toast fired |
| Notify principal modal submit | `hx-post="/api/.../wellbeing/{case_id}/notify-principal/"` `hx-target="#notification-result"` | Confirmation shown in modal; notification logged in Notifications tab |
| Student search autocomplete | `hx-get="/api/.../wellbeing/student-search/?q={value}"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#student-search-results"` | Dropdown for case-open form |
| Crisis alert banner refresh | `hx-get="/api/.../wellbeing/alerts/"` `hx-trigger="load, every 60s"` `hx-target="#alert-banner"` | Polled every 60s to catch new crisis cases; permanent banner non-dismissable if crisis present |
| KPI bar refresh | `hx-get="/api/.../wellbeing/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
