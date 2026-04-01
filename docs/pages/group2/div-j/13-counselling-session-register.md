# 13 — Counselling Session Register

> **URL:** `/group/health/sessions/`
> **File:** `13-counselling-session-register.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Mental Health Coordinator (primary) · Counsellors at branch level (own sessions only)

---

## 1. Purpose

Confidential log of all counselling sessions conducted across all branches in the group. Each session record captures: session type, presenting concern category, session notes, interventions used, risk assessment outcome, follow-up plan, and outcome code. The register is the clinical backbone of the group's mental health programme — it provides trend data for identifying systemic wellbeing issues (exam stress spikes, hostel adjustment problems, bullying clusters) without compromising individual student confidentiality.

Strict confidentiality architecture: identifiable student information (name, student ID) is visible only to the session counsellor who conducted the session and to the Group Mental Health Coordinator. All other roles who may have limited read access see only anonymised session IDs and aggregate counts. High-risk case flags and crisis escalation workflows are also managed through this register.

Scale: 200–1,000 sessions per month during examination periods. At large groups (50 branches, 100,000 students) with active counselling programmes, daily volumes can reach 50–100 sessions across branches. System must handle this load with server-side pagination and filtered queries only.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Mental Health Coordinator | G3 | Full view — all branches, student names visible, export | Primary owner and clinical supervisor |
| Branch Counsellor | Branch | Create + edit own sessions only (24h edit window) — student names visible for own sessions | No cross-branch visibility |
| Group Medical Coordinator | G3 | Session counts only — no clinical content, no student identifiers | Aggregate read only |
| Branch Principal | Branch | Branch aggregate session count only — no individual records | Dashboard widget only |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('mental_health_coordinator', 'branch_counsellor', 'medical_coordinator')` with branch-scoped queryset for Branch Counsellor and aggregate-only serialiser for Medical Coordinator. Student name/ID fields are masked at the PostgreSQL view layer for non-authorised roles — not just hidden in the UI.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Counselling Session Register
```

### 3.2 Page Header
- **Title:** `Counselling Session Register`
- **Subtitle:** `[N] Sessions This Month · [N] This Week · [N] Unique Students This Month`
- **Right controls:** `+ Log Session` (Branch Counsellor + Mental Health Coordinator) · `Advanced Filters` · `Export CSV` (Mental Health Coordinator only)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| High-risk student session overdue > 7 days | "[N] high-risk students have not had a session in over 7 days." | Red |
| Session not documented within 24 hours | "[N] sessions from yesterday or earlier remain undocumented." | Amber |
| Counsellor absent with active high-risk cases | "[Counsellor] is marked absent and has [N] active high-risk cases with no coverage assigned." | Red |
| Branch session volume spike > 100% week-over-week | "Unusual session volume spike at [Branch] this week (+[N]% vs last week). Review may be warranted." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Sessions This Month | Total session records in current calendar month | Blue always |
| Sessions This Week | Sessions in current calendar week (Mon–Sun) | Blue always |
| Unique Students This Month | Count of distinct students who have had at least one session this month | Blue always |
| High-Risk Cases (Active) | Students currently assigned High or Crisis risk level in active wellbeing cases | Green = 0 · Yellow 1–5 · Red > 5 |
| Follow-ups Completed % | (Follow-ups completed / Follow-ups due) × 100, current month | Green ≥ 90% · Yellow 70–89% · Red < 70% |
| Sessions by Type | Mini pie chart: Individual / Group / Crisis proportions | Visual only |
| Sessions by Branch | Mini bar chart: top 5 branches by session count this month | Visual only |

---

## 5. Main Table — Counselling Session Register

> **Confidentiality note:** Student name and student ID are visible only to the session counsellor (own sessions) and the Mental Health Coordinator. All other roles see `[RESTRICTED]` in those fields. This masking is enforced server-side.

**Search:** Session ID, branch name, counsellor name. 300ms debounce, minimum 2 characters.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Date Range | Date picker | From – To |
| Session Type | Checkbox | Individual / Group / Crisis |
| Concern Category | Checkbox | Academic / Family / Peer / Hostel / Identity / Trauma / Other |
| Risk Level | Checkbox | Low / Medium / High / Crisis |
| Outcome | Checkbox | Resolved / Ongoing / Referred / Escalated |
| Follow-up Pending | Radio | All / Yes / No |
| Counsellor | Single-select | All counsellors |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Session ID | ✅ | System-generated reference (e.g., SES-2026-08741) |
| Date | ✅ | DD-MMM-YYYY |
| Branch | ✅ | |
| Counsellor | ✅ | Counsellor name |
| Session Type | ✅ | Individual (blue) / Group (green) / Crisis (red) badge |
| Concern Category | ✅ | Badge |
| Duration (mins) | ✅ | |
| Risk Level | ✅ | Low (green) / Medium (amber) / High (red) / Crisis (flashing red) badge |
| Outcome | ✅ | Resolved / Ongoing / Referred / Escalated badge |
| Follow-up Scheduled | ✅ | Date, or None |
| Actions | ❌ | View Summary · Follow-up |

> **Student name and ID fields do not appear as columns in the main table.** They are visible only inside the session drawer's restricted tab.

**Default sort:** Date descending, then Risk Level descending (Crisis first within same date).
**Pagination:** Server-side · 25/page.
**Bulk actions:** Export CSV (Mental Health Coordinator only — student identifiers included in export; audit log records the export event).

---

## 6. Drawers / Modals

### 6.1 Drawer — `session-detail` (700px, right side)

Triggered by **View Summary** in Actions column. Risk level badge displayed in drawer header alongside Session ID.

**Tabs:**

#### Tab 1 — Session Notes
| Field | Notes |
|---|---|
| Date / Time | |
| Counsellor | Name + qualification |
| Session Type | Individual / Group / Crisis |
| Presenting Concerns | Free text — what the student described as their reason for coming |
| Session Summary | Rich text — what was discussed, key themes explored |
| Interventions Used | Checklist: CBT techniques / Active Listening / Psychoeducation / Problem-solving / Referral to doctor / Crisis intervention / Other (free text) |
| Homework / Task Given | Free text — any task assigned to student for next session |
| Session Outcome | Resolved / Ongoing / Referred / Escalated |
| Duration (mins) | |

#### Tab 2 — Student Profile (RESTRICTED)
> **Access:** Mental Health Coordinator and session counsellor (own session) only. All other roles see: *"You do not have access to identifiable student information for this session."*

| Field | Notes |
|---|---|
| Student Name | |
| Student ID | |
| Class / Section | |
| Branch | |
| Hostel / Day Scholar | |
| Referred By | Self / Teacher / Parent / Principal / Doctor / Peer |
| Referral Date | |
| Notes on Referral | Free text |

#### Tab 3 — Risk Assessment
| Field | Notes |
|---|---|
| Risk Level | Low / Medium / High / Crisis — editable by Mental Health Coordinator |
| Suicidal Ideation Screening | Yes / No / Not Assessed — with notes field |
| Self-Harm History | Yes / No / Not Assessed — with notes field |
| Protective Factors | Free text (e.g., "Strong family support, engaged in sports, has close friend group") |
| Previous Risk Level | For comparison if session is a follow-up |
| Recommended Action | Free text |

#### Tab 4 — Follow-up Plan
| Field | Notes |
|---|---|
| Next Session Date | Date |
| Next Session Type | Individual / Group |
| Assigned Counsellor for Next Session | (defaults to same counsellor) |
| Who to Inform | Multi-select: Parent / Principal / School Doctor — visible only for High/Crisis risk or with student consent |
| Referral to Psychiatrist | Yes / No — with referring institution if Yes |
| Referral Notes | Free text |
| External Resource Shared | Any leaflet, helpline, or resource given to student |

#### Tab 5 — History
All sessions for this student (anonymised for non-authorised views — shows session IDs only with dates).

| Column | Notes |
|---|---|
| Session ID | |
| Date | |
| Counsellor | |
| Session Type | |
| Risk Level | Badge |
| Outcome | |
| Follow-up Completed | Yes / No |

Risk level trend: sparkline chart showing risk level progression over time (available to Mental Health Coordinator only).

---

### 6.2 Drawer — `session-create` (680px, right side)

Triggered by **+ Log Session** button.

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select (auto-set for counsellor; selectable for Mental Health Coordinator) | Required |
| Student Search | Autocomplete — name shown to authorised roles only; ID shown if name restricted | Required; debounce 300ms |
| Counsellor | Single-select (auto-set for branch counsellor; selectable for Mental Health Coordinator) | Required |
| Date | Date picker (defaults to today) | Required |
| Time | Time picker (defaults to now) | Required |
| Session Type | Radio — Individual / Group / Crisis | Required |
| Concern Category | Single-select: Academic / Family / Peer / Hostel / Identity / Trauma / Other | Required |
| Presenting Concerns | Textarea (max 1,000 chars) | Required |
| Session Summary | Rich text editor (max 3,000 chars) | Required |
| Interventions Used | Checkbox list | Required; at least one |
| Homework / Task Given | Textarea (max 500 chars) | Optional |
| Duration (mins) | Number input | Required |
| Risk Level | Radio — Low / Medium / High / Crisis | Required |
| Suicidal Ideation Screening | Radio — Yes / No / Not Assessed | Required |
| Self-Harm History | Radio — Yes / No / Not Assessed | Required |
| Protective Factors | Textarea (max 500 chars) | Optional |
| Recommended Action | Textarea (max 500 chars) | Optional |
| Session Outcome | Radio — Resolved / Ongoing / Referred / Escalated | Required |
| Follow-up Required | Toggle — Yes / No | Required |
| Follow-up Date | Date picker | Required if follow-up = Yes |
| Referral to Psychiatrist | Toggle — Yes / No | Optional |
| Referral Institution | Text input | Required if referral = Yes |
| Referred By (original referral source) | Single-select: Self / Teacher / Parent / Principal / Doctor / Peer | Required |

> Selecting Risk Level = Crisis automatically highlights the "Escalate Crisis" section below the form with a warning banner: *"You are logging a Crisis session. Use the Escalate Crisis modal to trigger immediate notifications."*

**Footer:** `Cancel` · `Save Session`

---

### 6.3 Drawer — `session-edit` (680px, right side)

Same layout as `session-create`, pre-populated. Only available within 24 hours of session creation. After 24h, edit button is disabled and a note is shown: *"Sessions can only be edited within 24 hours of creation. Contact Mental Health Coordinator to request amendment."*

---

### 6.4 Modal — `escalate-crisis` (460px, centred)

Triggered by **Escalate Crisis** button in the session create form (when Risk Level = Crisis) or from the Actions Required tab. Available to both Branch Counsellor and Mental Health Coordinator.

| Field | Type | Validation |
|---|---|---|
| Session ID | Read-only | |
| Student ID | Read-only (name shown to authorised roles only) | |
| Branch | Read-only | |
| Nature of Crisis | Textarea (max 500 chars) | Required |
| Immediate Action Taken | Textarea (max 500 chars) | Required |
| Notify | Multi-select: Branch Principal / School Medical Officer / Parents / Emergency Services | Required; at least one |
| Additional Notes | Textarea (max 300 chars) | Optional |
| Timestamp | Read-only (auto-set to now) | |

**Footer:** `Cancel` · `Escalate — Log & Notify`

Triggers: notification sent to selected parties; escalation logged with timestamp in session record and in the Wellbeing Tracker; crisis badge applied to session row; alert banner updated.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Session logged | "Counselling session logged successfully." | Success |
| Session updated | "Session record updated." | Success |
| Follow-up scheduled | "Follow-up session scheduled for [Date]." | Success |
| Crisis escalated | "Crisis escalation logged and notifications sent to [roles]." | Warning (prominent) |
| 24h edit window expired | "Edit window has closed. Sessions can only be edited within 24 hours." | Error |
| Export triggered | "Export is being prepared. Audit log entry created." | Info |
| Session marked follow-up complete | "Follow-up marked as complete for Session [ID]." | Success |
| Save failed — validation | "Please complete all required fields before saving." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No sessions this period | "No sessions recorded for this period." | "Sessions will appear here once logged." | `+ Log Session` button |
| No results for current filters | "No sessions match your current filters." | "Try adjusting filters." | `Clear Filters` |
| No follow-ups pending | "No follow-ups pending." | "All session follow-ups are up to date." | — |
| No crisis cases | "No crisis cases active." | — | — |
| History tab — no prior sessions | "No previous sessions on record for this student." | "This is their first recorded session." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: KPI bar (7 cards — 5 number + 2 chart placeholders) + table (10 grey rows × 10 columns) |
| Filter / search apply | Table body spinner overlay; KPI bar charts update after |
| Session detail drawer open | Drawer skeleton: tab headers + content block skeleton |
| Student Profile tab (restricted) | Access check skeleton for 500ms; either content or access-denied message |
| Risk Assessment tab | Form skeleton with 4 grey field blocks |
| Session history sparkline | Chart placeholder spinner while loading |
| Crisis escalation modal submit | Modal footer spinner + "Sending notifications…" label; disabled until complete |
| Export generation | Button spinner + "Preparing export…"; audit log entry shown below button |

---

## 10. Role-Based UI Visibility

| UI Element | Mental Health Coordinator | Branch Counsellor | Medical Coordinator | Branch Principal |
|---|---|---|---|---|
| Full session list (all branches) | ✅ | Own branch only | ❌ (count widget) | ❌ (count widget) |
| Student name / ID in main table | ❌ (not shown in table columns) | ❌ (not shown in table columns) | ❌ | ❌ |
| Student Profile tab in drawer | ✅ (all sessions) | ✅ (own sessions only) | ❌ | ❌ |
| Session Notes tab | ✅ | ✅ (own sessions) | ❌ | ❌ |
| Risk Assessment tab | ✅ | ✅ (own sessions) | ❌ | ❌ |
| Follow-up Plan tab | ✅ | ✅ (own sessions) | ❌ | ❌ |
| Session History tab | ✅ (all sessions — student names visible) | ✅ (own student sessions — name visible) | ❌ | ❌ |
| + Log Session button | ✅ | ✅ | ❌ | ❌ |
| Edit session (within 24h) | ✅ | ✅ (own sessions only) | ❌ | ❌ |
| Escalate Crisis button | ✅ | ✅ | ❌ | ❌ |
| Export CSV button | ✅ | ❌ | ❌ | ❌ |
| KPI bar — full detail | ✅ | ✅ (own branch) | Counts only | Counts only |
| Alert banners | ✅ | ✅ (own branch alerts) | ❌ | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/sessions/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/sessions/` | List all sessions (paginated, filtered, masked by role) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/sessions/` | Create new session record | Mental Health Coordinator / Branch Counsellor |
| GET | `/api/v1/group/{group_id}/health/sessions/{session_id}/` | Retrieve session detail (role-masked) | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/sessions/{session_id}/` | Update session (24h window enforced) | Mental Health Coordinator / Session counsellor (own) |
| GET | `/api/v1/group/{group_id}/health/sessions/kpi/` | KPI summary bar data | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/sessions/{session_id}/escalate/` | Crisis escalation — log + notify | Mental Health Coordinator / Branch Counsellor |
| POST | `/api/v1/group/{group_id}/health/sessions/{session_id}/follow-up-complete/` | Mark follow-up as completed | Mental Health Coordinator / Branch Counsellor |
| GET | `/api/v1/group/{group_id}/health/sessions/{session_id}/history/` | All sessions for student linked to this session | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/sessions/student-search/` | Autocomplete student search (role-gated) | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/sessions/export/` | Export CSV with audit log entry | Mental Health Coordinator |
| GET | `/api/v1/group/{group_id}/health/sessions/alerts/` | Fetch active alert conditions | JWT + role check |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `date_from` | date | Start of date range |
| `date_to` | date | End of date range |
| `session_type` | str[] | `individual`, `group`, `crisis` |
| `concern_category` | str[] | Category slugs |
| `risk_level` | str[] | `low`, `medium`, `high`, `crisis` |
| `outcome` | str[] | `resolved`, `ongoing`, `referred`, `escalated` |
| `follow_up_pending` | bool | Filter by pending follow-up |
| `counsellor` | int | Filter by counsellor ID |
| `page` | int | Page number |
| `page_size` | int | 25 default, max 100 |
| `search` | str | Session ID, branch, or counsellor name |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Student search autocomplete | `hx-get="/api/.../sessions/student-search/?q={value}"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#student-search-results"` | Dropdown below input; student name shown to authorised roles; ID only to others |
| Filter form apply | `hx-get="/api/.../sessions/"` `hx-trigger="change"` `hx-target="#sessions-table-body"` `hx-include="#filter-form"` | Table body replaced; KPI bar updated |
| Pagination | `hx-get="/api/.../sessions/?page={n}"` `hx-target="#sessions-table-body"` `hx-push-url="true"` | Page swap |
| Session detail drawer open | `hx-get="/api/.../sessions/{session_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Session Notes tab default |
| Drawer tab switch | `hx-get="/api/.../sessions/{session_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped; access check run for restricted tabs |
| Student Profile tab access check | `hx-get="/api/.../sessions/{session_id}/?tab=student_profile"` `hx-target="#drawer-tab-content"` | Returns content or access-denied partial based on role |
| Session history tab load | `hx-get="/api/.../sessions/{session_id}/history/"` `hx-target="#session-history-content"` `hx-trigger="click[tab='history']"` | History loaded on tab click |
| Session create form submit | `hx-post="/api/.../sessions/"` `hx-target="#sessions-table-body"` `hx-on::after-request="closeDrawer(); fireToast();"` | New row prepended to table; drawer closed |
| Session edit form submit | `hx-patch="/api/.../sessions/{session_id}/"` `hx-target="#session-row-{session_id}"` `hx-swap="outerHTML"` | Row updated; drawer closed; toast fired |
| Crisis escalation modal submit | `hx-post="/api/.../sessions/{session_id}/escalate/"` `hx-target="#escalation-result"` `hx-indicator="#escalation-spinner"` | Result shown in modal; notifications dispatched; row risk badge updated |
| Follow-up complete button | `hx-post="/api/.../sessions/{session_id}/follow-up-complete/"` `hx-target="#followup-status-{session_id}"` `hx-swap="outerHTML"` | Follow-up cell updated to "Done" badge |
| KPI bar refresh | `hx-get="/api/.../sessions/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Alert banner load | `hx-get="/api/.../sessions/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional display |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
