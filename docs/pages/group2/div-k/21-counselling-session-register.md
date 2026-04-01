# 21 — Counselling Session Register

> **URL:** `/group/welfare/counselling/sessions/`
> **File:** `21-counselling-session-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Primary Role:** Group Counselling Head (Role 94, G3)
> **Secondary Role:** Individual Counsellors (view own sessions only)

---

## 1. Purpose

Complete log of all counselling sessions conducted across all branches — individual and group sessions. Individual sessions are confidential: student identity is visible only to the assigned counsellor and the Counselling Head; all other roles see only an anonymised Student Code ([S-XXXX]). Group sessions are non-confidential (program name, branch, attendance count visible to all authorised roles).

Each session record includes: counsellor, branch, session type (Individual / Group / Peer / Family / Crisis), presenting concern category (Academic stress / Career anxiety / Peer conflict / Bullying / Family issues / Mental health / Trauma / Other), session duration, outcome (Ongoing plan / Referred to psychiatrist / Resolved / Dropped out / Crisis escalated), and next session date.

The Counselling Head uses this to track counsellor productivity, identify high-demand concern categories requiring structural response, and flag students with crisis escalations requiring immediate follow-up. DPDP Act 2023 compliance: all identifiable individual session data is access-controlled, consent is documented at first session, and no data export includes student names except for authorised G3 exports with audit logging.

Scale: 500–3,000 individual sessions per year · 200–1,000 group sessions per year.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Counselling Head | G3 | Full — all branches, all sessions, full student identity visible, can log/edit sessions, view crisis escalations, export | Primary owner |
| Branch Counsellor | G2 | Own sessions only — can log new sessions, update outcomes, view own student names and caseload; cannot see other counsellors' sessions | Strict object-level permission |
| Group COO | G4 | View — aggregate statistics only (count by type, category, branch); no individual session records | No student identifiers at any level |
| Branch Principal | G2 | View — own branch aggregate only: session count by type and month; no individual records | No student identifiers |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('counselling_head', 'branch_counsellor')` with strict queryset filter for G2 counsellors (`sessions.filter(counsellor__user=request.user)`). Student identity fields returned only for G3 and the session's assigned counsellor.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Counselling  ›  Counselling Session Register
```

### 3.2 Page Header
```
Counselling Session Register                  [+ Log Session]  [Export Sessions ↓]  [Settings ⚙]
[Group Name] — Group Counselling Head · Last updated: [timestamp]
[N] Sessions This Month  ·  [N] Individual  ·  [N] Group  ·  [N] Crisis Escalated Open
```

### 3.3 Alert Banner (conditional — crisis and compliance items)

| Condition | Banner Text | Severity |
|---|---|---|
| Crisis escalation unacknowledged > 2 hours | "Crisis escalation from session [ID] at [Branch] has not been acknowledged by the Counselling Head for [N] hours. Immediate review required." | Red |
| Student referred to psychiatrist — no follow-up logged in 14 days | "Student [S-XXXX] referred to psychiatrist in session [ID] at [Branch] on [date]. No follow-up session logged in [N] days. Review required." | Red |
| Counsellor near/over monthly session capacity | "Counsellor [Name] at [Branch] has conducted [N] individual sessions this month — approaching maximum sustainable caseload. Review workload." | Amber |
| Student with 3+ crisis sessions in 30 days | "Student [S-XXXX] at [Branch] has had [N] sessions flagged as Crisis type in the last 30 days. Multi-agency review recommended." | Red |
| Branch with no sessions logged in > 14 days | "[Branch] counsellor has logged no sessions in [N] days. Confirm counsellor is active and sessions are being recorded." | Amber |

Max 5 alerts visible. Alert links route to the relevant session record or student code filter. "View full crisis log →" shown below alerts.

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Sessions This Month | Total sessions (all types) across all branches this calendar month | Blue always (informational) | → Main table filtered to current month |
| Individual Sessions This Month | Count of Type = Individual sessions | Blue always (informational) | → Main table filtered to type=Individual, current month |
| Group Sessions This Month | Count of Type = Group sessions this month | Blue always (informational) | → Main table filtered to type=Group, current month |
| Crisis Escalated Open | Sessions flagged as crisis type with outcome = Crisis escalated and not yet resolved | Green = 0 · Yellow 1–2 · Red > 2 | → Main table filtered to outcome=Crisis escalated |
| Referred to Psychiatrist (No Follow-up) | Students referred to psychiatrist with no follow-up session logged in > 14 days | Green = 0 · Yellow 1–3 · Red > 3 | → Main table filtered to outcome=Referred, no follow-up |
| Top Concern Category This Month | Category with highest session count this month | Informational — category name displayed | → Section 5.2 chart |
| Avg Session Duration (mins) | Mean duration across all individual sessions this month | Blue always (informational) | — |
| Branches with Active Sessions This Month | Count of branches where at least 1 session logged this month | Green = all branches with counsellors · Amber if any gap | → Section 5.2 branch panel |

**HTMX:** `hx-trigger="every 5m"` → Crisis Escalated Open and Referred (No Follow-up) auto-refresh.

---

## 5. Sections

### 5.1 Session Register Table (Primary Table)

> All counselling sessions. Individual sessions show anonymised student identity to non-authorised roles.

**Confidentiality note:** Column header "Attendees / Student Code" shows:
- G3 (Counselling Head): Full student name + student ID.
- G2 (Assigned Counsellor for that session): Full student name + student ID.
- G2 (Other counsellors or branch principal): Not visible at all; session not in their queryset.
- G4 (COO): Not visible; COO sees aggregate view only (Section 5.2).

**Search:** Session ID, counsellor name, branch, concern category, Student Code (anonymised — search by S-XXXX). 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Counsellor | Searchable dropdown | All active counsellors (G3); own name only (G2) |
| Date Range | Date range picker | Default: Current month; max 365 days |
| Session Type | Checkbox | Individual / Group / Peer / Family / Crisis |
| Concern Category | Checkbox | Academic stress / Career anxiety / Peer conflict / Bullying / Family issues / Mental health / Trauma / Other |
| Outcome | Checkbox | Ongoing plan / Referred to psychiatrist / Resolved / Dropped out / Crisis escalated |
| Crisis Flag | Toggle | Show only crisis-flagged sessions |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Session Date | ✅ | Date |
| Branch | ✅ | Branch name |
| Counsellor | ✅ | Counsellor name |
| Type | ✅ | Badge: Individual (Blue) · Group (Green) · Peer (Teal) · Family (Purple) · Crisis (Red) |
| Category | ✅ | Concern category badge |
| Duration (mins) | ✅ | Integer; blank for group sessions (use Attendee Count instead) |
| Attendees / Student Code | ✅ | Individual: Student name (G3/own counsellor) or "Student [S-XXXX]" (other auth roles); Group: "Group — [N] attendees" |
| Outcome | ✅ | Ongoing plan (Blue) · Referred (Amber) · Resolved (Green) · Dropped out (Grey) · Crisis escalated (Red) |
| Next Session | ✅ | Date or "—" if none scheduled |
| Actions | ❌ | View · Update Outcome · Escalate Crisis |

**Default sort:** Session Date descending (most recent first).
**Pagination:** Server-side · 25/page.

---

### 5.2 Analytics Section

**Display:** Two-column layout on desktop (each chart takes 50% width); stacked on mobile.

**Chart 1 — Bar Chart: Sessions by Concern Category (Current Month)**
- X-axis: Concern categories.
- Y-axis: Session count.
- Colour: Each category gets a distinct colour.
- Tooltip: Category name · Count · % of total individual sessions.
- Data: Individual sessions only (group sessions categorised separately).

**Chart 2 — Line Chart: Monthly Session Volume Trend (Last 12 Months)**
- X-axis: Month labels.
- Y-axis: Session count.
- Two lines: Individual sessions (Blue solid) · Group sessions (Green dashed).
- Tooltip: Month · Individual count · Group count.

**Branch Activity Panel (below charts):**
- Table: Branch · Counsellor(s) · Individual Sessions This Month · Group Sessions This Month · Crisis Sessions · Last Session Date
- Default sort: Individual sessions descending.
- Pagination: 25/page.

---

## 6. Drawers / Modals

### 6.1 Drawer: `session-detail`
- **Trigger:** "View" action on any session row in the main table
- **Width:** 660px
- **Tabs:** Session · Outcome · Next Steps · History
- **Confidential:** Student name and ID visible only to G3 or the assigned counsellor. All other fields visible to all authorised roles that can access the drawer.

**Session tab:**
| Field | Notes |
|---|---|
| Session ID | System-generated read-only |
| Session Date | Read-only |
| Session Time | Start time, read-only |
| Branch | Read-only |
| Counsellor | Name + link to counsellor profile |
| Session Type | Type badge |
| Concern Category | Category badge |
| Duration | Minutes (Individual) or N/A (Group) |
| Student Name | Visible to G3 and own counsellor only; else "Confidential — [S-XXXX]" |
| Student ID | Visible to G3 and own counsellor only |
| Consent Documented | Yes ✅ / No ❌ (consent form signed at first session) |
| Presenting Issue | Session notes — visible to G3 and own counsellor only; else hidden with "Confidential — access restricted" |
| Session Notes (Encrypted) | Full clinical notes — G3 and own counsellor only; AES-256 encrypted at rest |
| Group Program Name | For Group type: program/session name |
| Attendee Count | For Group type: number of attendees |
| Group Session Objectives | For Group type: non-confidential |

**Outcome tab:**
| Field | Notes |
|---|---|
| Outcome | Current outcome badge |
| Outcome Notes | Counsellor notes on session outcome (G3 and own counsellor only) |
| Risk Level | Low / Moderate / High / Immediate — set by counsellor at end of session |
| Referred To | If outcome = Referred: psychiatrist name/facility, referral date |
| Follow-up Confirmed | Toggle: referral appointment confirmed Yes/No |
| Crisis Escalated | Yes / No; if Yes: escalation timestamp and escalated to (Counselling Head / Medical Coordinator / Both) |

**Next Steps tab:**
| Field | Notes |
|---|---|
| Next Session Date | Scheduled date |
| Next Session Focus | Brief (non-confidential heading — topic area) |
| Action Items for Student | If any; G3 and own counsellor only |
| Action Items for Counsellor | If any; G3 and own counsellor only |
| Parental Notification Required | Yes / No; DPDP Act — note: parental notification for minors in crisis situations |
| Parental Notification Date | If Yes: date sent |

**History tab:**
- Full session history for this student (Individual sessions) or program (Group sessions):
  - Date · Counsellor · Type · Category · Outcome · Duration
- Visible to G3 and own counsellor only (student-level history is confidential).
- Paginated if > 10 sessions.

**Footer actions:**
- [Update Outcome] — inline edit of outcome fields (G3 and own counsellor)
- [Escalate Crisis] — opens `crisis-escalation` drawer (G3 and own counsellor)
- [Schedule Next Session] — opens date/time picker inline and saves next session date

---

### 6.2 Drawer: `new-session`
- **Trigger:** [+ Log Session] button in page header
- **Width:** 600px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Searchable dropdown | Required |
| Counsellor | Searchable dropdown (counsellors at selected branch) | Required; G2 counsellor sees only themselves |
| Session Date | Date picker | Required; cannot be future date |
| Session Time (Start) | Time picker | Required |
| Session Type | Radio | Individual / Group / Peer / Family / Crisis · Required |
| Concern Category | Select | Full list · Required |
| Duration (minutes) | Number · 15–180 | Required for Individual/Family/Crisis · Optional for Group |
| Student Code or Name (Individual/Family/Crisis) | Searchable — student directory (shows name to G3/own counsellor; returns student code) | Required for Individual/Family/Crisis |
| Consent Documented | Toggle | Required for first session with this student; system auto-checks if consent already on record |
| Group Program Name (Group/Peer) | Text · max 100 chars | Required for Group/Peer |
| Attendee Count (Group/Peer) | Number · 1–100 | Required for Group/Peer |
| Group Session Objectives (Group/Peer) | Textarea · max 300 chars | Required for Group/Peer |
| Presenting Issue | Textarea · max 1000 chars | Required for Individual/Family/Crisis; encrypted at rest |
| Session Notes | Textarea · max 2000 chars | Optional; encrypted at rest; for Individual/Family/Crisis |
| Outcome | Select | Ongoing plan / Referred to psychiatrist / Resolved / Dropped out / Crisis escalated · Required |
| Risk Level | Radio | Low / Moderate / High / Immediate · Required for Individual/Family/Crisis |
| Referral Details (if Referred) | Textarea · max 300 chars | Required if outcome = Referred |
| Crisis Escalation (if Crisis escalated) | Auto-opens `crisis-escalation` sub-form inline | Required if outcome = Crisis escalated |
| Next Session Date | Date picker | Optional |

**Validation:**
- Student Code/Name required for Individual, Family, Crisis types.
- Group Program Name required for Group, Peer types.
- If outcome = Crisis escalated, a crisis escalation form must be completed before session can be saved.
- Presenting Issue and Session Notes are encrypted client-side before transmission using the group's encryption key (AES-256).
- Session date cannot be in the future.

**Footer:** [Cancel] [Log Session →]

---

### 6.3 Drawer: `crisis-escalation`
- **Trigger:** "Escalate Crisis" action in `session-detail` drawer footer, or outcome = "Crisis escalated" in new-session form
- **Width:** 480px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Session ID | Read-only pre-filled | — |
| Student Code | Read-only pre-filled (S-XXXX) | — |
| Branch | Read-only pre-filled | — |
| Risk Level | Radio | High / Immediate · Required |
| Nature of Crisis | Select | Self-harm risk / Harm to others risk / Severe mental health episode / Trauma disclosure / Family violence disclosure / Suicidal ideation / Other · Required |
| Crisis Description | Textarea · max 800 chars | Required · min 50 chars; encrypted at rest |
| Immediate Safety Plan | Textarea · max 500 chars | Required; steps taken immediately |
| Escalate To | Checkbox group | Counselling Head (default, always checked) · Branch Principal · Medical Coordinator · Both Parents (if minor, with parental consent on file) · Mandatory reporter (POCSO — if applicable) |
| Counselling Head Notification | Checkbox | Required; cannot uncheck — Counselling Head must always receive crisis notifications |
| Parent / Guardian Notification | Toggle | Default: OFF for non-critical; ON for Immediate risk; record notification date if sent |
| External Referral Required | Toggle | Default: OFF |
| External Referral Details | Textarea · max 300 chars | Required if External Referral = ON (psychiatrist / hospital / helpline) |
| Follow-up Session Date | Date picker | Required; must be within 7 days of crisis session |

**Validation:**
- Crisis Description minimum 50 characters.
- Counselling Head notification cannot be unchecked.
- Follow-up session date must be within 7 calendar days.
- If Nature of Crisis = Suicidal ideation: system forces External Referral = ON and prompts mandatory referral to a mental health professional.

**On submit:** POST to crisis endpoint · Portal notification pushed to all selected escalation recipients · Email sent to Counselling Head · Session outcome updated to "Crisis escalated" · Follow-up session placeholder created in session register · Crisis flag set on student record.

**Footer:** [Cancel] [Submit Crisis Escalation →]

---

### 6.4 Drawer: `group-session-detail`
- **Trigger:** "View" on a Group or Peer type session row in the main table
- **Width:** 560px
- **Non-confidential:** All content in this drawer is non-confidential and visible to all authorised roles.

**Fields:**
| Field | Notes |
|---|---|
| Session ID | System-generated read-only |
| Session Date | Read-only |
| Branch | Read-only |
| Counsellor | Name |
| Type | Group / Peer badge |
| Program Name | Session/program title |
| Program Objectives | Freetext; what the session aimed to achieve |
| Topics Covered | Freetext; actual topics discussed |
| Attendee Count | Number |
| Duration (minutes) | If recorded |
| Materials Used | Freetext (optional) |
| Session Outcome / Feedback | Freetext summary |
| Next Group Session Date | If planned |
| Session Resources | Uploaded handouts or links (non-confidential) |

**Footer actions:**
- [Edit Session] — opens inline editable fields (G3 and own counsellor)
- [Log Follow-up Session] — pre-fills new-session form with same program name and counsellor

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Session logged | "Session logged for [Counsellor Name] at [Branch] on [date]. Type: [type]." | Success | 4s |
| Crisis escalation submitted | "Crisis escalation submitted for Student [S-XXXX]. Counselling Head and [N] other recipients notified." | Warning | 8s (persistent) |
| Outcome updated | "Session [ID] outcome updated to [outcome]." | Success | 3s |
| Follow-up session scheduled | "Follow-up session scheduled for [date]. Calendar entry created." | Success | 4s |
| Next session date saved | "Next session date saved for Student [S-XXXX] — [date]." | Success | 3s |
| Session exported (G3 only) | "Session export is being prepared. Audit entry recorded. Download will begin shortly." | Info | 4s |
| Crisis acknowledged | "Crisis escalation [ID] acknowledged. Follow-up required by [date]." | Info | 4s |
| Consent documented | "Consent for Student [S-XXXX] documented for this session and all future sessions." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No sessions logged yet | "No Counselling Sessions Logged" | "No sessions have been logged for the selected period and branch." | [+ Log Session] |
| No sessions for selected filters | "No Sessions Found" | "No sessions match your selected filters or search terms." | [Clear Filters] |
| No crisis escalations open | "No Open Crisis Escalations" | "There are no unresolved crisis escalations across any branch." | — |
| No sessions for counsellor (own view) | "No Sessions Logged Yet" | "You have not logged any counselling sessions. Start by logging your first session." | [+ Log Session] |
| No referred-without-follow-up | "All Referrals Followed Up" | "All students referred to psychiatrists have had a follow-up session logged within 14 days." | — |
| No analytics data | "Not Enough Data for Charts" | "No sessions have been logged this month. Charts will appear once sessions are recorded." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + session table (15 rows × 10 columns) + analytics charts + alerts |
| Table filter/search | Inline skeleton rows (8 rows × 10 columns) |
| KPI auto-refresh | Shimmer on Crisis Escalated Open and Referred (No Follow-up) card values |
| Session detail drawer open | 660px drawer skeleton with 4-tab bar; each tab loads lazily |
| History tab | List skeleton (8 rows with date + outcome placeholders) |
| New session form open | 600px drawer skeleton with 18 field skeletons; conditional fields animate in on type selection |
| Crisis escalation drawer | 480px drawer with 12 field skeletons |
| Group session detail drawer | 560px drawer with field skeletons |
| Analytics bar chart | Chart area grey rectangle with shimmer gradient (full-width, 280px tall) |
| Analytics line chart | Chart area grey rectangle with shimmer gradient |
| Branch activity panel | Table skeleton (10 rows × 6 columns) |

---

## 10. Role-Based UI Visibility

| Element | Counselling Head G3 | Group COO G4 | Branch Counsellor G2 (own sessions) | Branch Principal G2 |
|---|---|---|---|---|
| View All Sessions (All Branches) | ✅ | ❌ (aggregate only) | Own sessions only | ❌ (aggregate only) |
| View Student Name in Table | ✅ | ❌ | ✅ (own sessions) | ❌ |
| View Session Notes (Encrypted) | ✅ | ❌ | ✅ (own sessions) | ❌ |
| Log New Session | ✅ | ❌ | ✅ | ❌ |
| Update Outcome | ✅ | ❌ | ✅ (own sessions) | ❌ |
| Escalate Crisis | ✅ | ❌ | ✅ | ❌ |
| Acknowledge Crisis Escalation | ✅ | ❌ | ❌ | ❌ |
| View Crisis Description | ✅ | ❌ | ✅ (own sessions) | ❌ |
| Export Session Register | ✅ (with audit log) | ❌ | ❌ | ❌ |
| View Analytics Charts | ✅ | ✅ (no student IDs) | ✅ (own branch aggregate) | ✅ (own branch aggregate) |
| View History Tab (Student) | ✅ | ❌ | ✅ (own student sessions) | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/counselling/sessions/` | JWT (G3, G2-own) | Session register table; params: `branch_id`, `counsellor_id`, `date_from`, `date_to`, `session_type`, `category`, `outcome`, `crisis_flag`, `q`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/counselling/sessions/kpi-cards/` | JWT (G3+) | KPI auto-refresh payload |
| GET | `/api/v1/group/{group_id}/welfare/counselling/sessions/analytics/category-bar/` | JWT (G3+) | Sessions by concern category bar chart data |
| GET | `/api/v1/group/{group_id}/welfare/counselling/sessions/analytics/monthly-trend/` | JWT (G3+) | 12-month session volume trend data |
| GET | `/api/v1/group/{group_id}/welfare/counselling/sessions/analytics/branch-panel/` | JWT (G3+) | Branch activity panel table |
| GET | `/api/v1/group/{group_id}/welfare/counselling/sessions/{session_id}/` | JWT (G3, G2-own) | Session detail drawer payload; role-gated fields |
| POST | `/api/v1/group/{group_id}/welfare/counselling/sessions/` | JWT (G3, G2-own) | Log new session; Presenting Issue and Session Notes encrypted before storage |
| PATCH | `/api/v1/group/{group_id}/welfare/counselling/sessions/{session_id}/outcome/` | JWT (G3, G2-own) | Update session outcome |
| POST | `/api/v1/group/{group_id}/welfare/counselling/sessions/{session_id}/crisis-escalate/` | JWT (G3, G2-own) | Submit crisis escalation; triggers multi-recipient notifications |
| PATCH | `/api/v1/group/{group_id}/welfare/counselling/sessions/{session_id}/crisis-acknowledge/` | JWT (G3) | Acknowledge open crisis escalation |
| POST | `/api/v1/group/{group_id}/welfare/counselling/sessions/{session_id}/next-session/` | JWT (G3, G2-own) | Schedule next session date |
| GET | `/api/v1/group/{group_id}/welfare/counselling/sessions/{student_code}/history/` | JWT (G3, G2-own) | Full session history for a student (confidential) |
| GET | `/api/v1/group/{group_id}/welfare/counselling/sessions/export/` | JWT (G3 only) | Async export; audit log entry mandatory; student names included only in G3 export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../sessions/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Session table search | `input delay:300ms` | GET `.../sessions/?q={val}` | `#session-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../sessions/?{filters}` | `#session-table-section` | `innerHTML` |
| Session type filter | `change` | GET `.../sessions/?session_type={val}` | `#session-table-section` | `innerHTML` |
| Crisis flag toggle | `change` | GET `.../sessions/?crisis_flag=true` | `#session-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../sessions/?page={n}` | `#session-table-section` | `innerHTML` |
| Open session detail drawer | `click` on View action | GET `.../sessions/{id}/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch (lazy) | `click` on tab | GET `.../sessions/{id}/?tab={name}` | `#drawer-tab-content` | `innerHTML` |
| New session — type change | `change` on Type radio | GET `.../sessions/new/?type={val}` (partial form) | `#conditional-fields` | `innerHTML` |
| Update outcome submit | `click` | PATCH `.../sessions/{id}/outcome/` | `#session-row-{id}` | `outerHTML` |
| Crisis escalation submit | `click` | POST `.../sessions/{id}/crisis-escalate/` | `#session-row-{id}` | `outerHTML` |
| Schedule next session | `click` | POST `.../sessions/{id}/next-session/` | `#next-session-display-{id}` | `innerHTML` |
| Category bar chart load | `load` | GET `.../sessions/analytics/category-bar/` | `#category-chart` | `innerHTML` |
| Monthly trend chart load | `load` | GET `.../sessions/analytics/monthly-trend/` | `#trend-chart` | `innerHTML` |
| Branch activity panel load | `load` | GET `.../sessions/analytics/branch-panel/` | `#branch-panel` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
