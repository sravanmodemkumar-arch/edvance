# D-16 — Student Question Feedback Queue

> **Route:** `/content/director/feedback/`
> **Division:** D — Content & Academics
> **Primary Roles:** Content Director (18) · Question Approver (29)
> **File:** `d-16-feedback-queue.md`
> **Priority:** P2 — Needed once first exam is delivered and student flags begin arriving
> **Status:** ⬜ Not started
> **Amendments:** G2 (post-publish unpublish flow → Amendment Review state — feedback is a primary trigger for G2 actions)

---

## 1. Page Name & Route

**Page Name:** Student Question Feedback Queue
**Route:** `/content/director/feedback/`
**Part-load routes:**
- `/content/director/feedback/?part=feedback-table` — main feedback list
- `/content/director/feedback/?part=flag-counts` — live flag count badges per severity level
- `/content/director/feedback/?part=question-detail&question_id={uuid}` — feedback detail drawer content
- `/content/director/feedback/?part=resolve-confirm&question_id={uuid}&action={action}` — resolution confirmation panel
- `/content/director/feedback/?part=escalation-alerts` — auto-escalation alerts panel

---

## 2. Purpose (Business Objective)

When 74,000 students sit a concurrent exam, some fraction will flag questions — a wrong answer key, an ambiguous option, an outdated fact in a GK question, a rendering error. Without a structured feedback pipeline, these flags accumulate unread, student trust erodes, and errors can persist across multiple exam sittings.

D-16 collects all question flags raised during exams (via the Div F student exam interface), triages them by flag volume and severity, and routes them to the Director + Approver for action. The action options range from dismissal (false flag) to G2 emergency unpublish → amendment review.

The critical design principle: a single student flag is usually noise; 10+ flags on the same question are almost certainly a real problem. D-16's auto-escalation logic surfaces the signal from the noise.

**What this page does NOT do:** It does not handle general platform feedback (UI bugs, performance complaints, login issues). It handles only question-specific academic feedback — flags raised against specific MCQs during exam sessions.

**Business goals:**
- Aggregate student flags per question across all exams in which it appeared
- Surface high-flag questions immediately regardless of exam status
- Enable Director and Approver to investigate, dismiss, or trigger G2 amendment review directly from this page
- Track resolution history — every flag investigation has a documented outcome
- Feed post-publish issue data to D-13 Quality Analytics (Post-Publish Issues tab)

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full — all flags visible, all resolution actions except Unpublish |
| Question Approver (29) | Full — all flags visible + Unpublish action (G2) |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Filters

- H1: "Student Question Feedback Queue"
- Severity filter tabs (with count badges, auto-refreshed via HTMX every 60s):
  - 🔴 Critical (≥ 50 flags or Director/Approver manually escalated)
  - 🟠 High (10–49 flags)
  - 🟡 Medium (3–9 flags)
  - ⚪ Low (1–2 flags)
  - ✅ Resolved (closed this month)
- Global filters:
  - Subject (multi-select)
  - Exam Type (multi-select)
  - Date range (flagged date — default: last 30 days)
  - Status: Open · Under Investigation · Dismissed · Resolved (Unpublished) · Resolved (No Action)
- "Auto-Escalation Alerts" panel: collapsible, shown at top when any Critical-tier questions exist (see Section 5)

---

### Section 2 — Feedback Table

**Default view:** Shows Open + Under Investigation items, sorted by flag count descending (highest flags first).

**Table columns:**

| Column | Description |
|---|---|
| Question ID | UUID short (8 chars) — click opens detail drawer |
| Subject | — |
| Exam Type | — |
| Flag Count | Total flags across all exam instances — colour badge: red ≥ 50 · orange 10–49 · yellow 3–9 · grey 1–2 |
| Flag Reasons | Aggregated: "Wrong Answer (12) · Ambiguous (8) · Outdated Fact (3)" — top 3 reasons shown inline, full list in drawer |
| Exams Affected | Number of distinct exam sessions where this question was flagged |
| Students Reached | Total student count across all exams that included this question (from Div F `exam_question_usage` table) |
| First Flagged | Date of first flag |
| Last Flagged | Date of most recent flag |
| Status | Open · Under Investigation · Dismissed · Resolved |
| Assigned To | Content Director / Approver role label if under investigation |

**Row quick actions:**
- "Investigate" → sets status to Under Investigation + assigns to current user + opens detail drawer
- "Dismiss" → one-click dismissal for clearly invalid flags (tooltip: "Use for duplicate questions where the answer is clearly correct and flags are student errors. A dismiss note is required.")
- "Unpublish (G2)" → Approver only — triggers G2 amendment flow directly

**Bulk actions (Director only):**
- "Bulk Dismiss" — select multiple Low-flag questions → dismiss with a single reason note
- "Export Feedback Report" — CSV of all visible rows (flag counts, reasons, resolution status — no student identity data)

---

### Section 3 — Question Detail Drawer

**Trigger:** Click any row or "Investigate" action.

**Drawer width:** 760px. Three sub-tabs within the drawer:

#### Sub-tab 1: Question & Flags

**Left pane (55%):** Full question render — exactly as students saw it during the exam (subject-appropriate rendering: MathJax for LaTeX, SMILES for Chemistry, etc.)

**Right pane (45%):**

**Flag Summary:**
- Total flags: {N}
- Unique students who flagged: {N} (a student can flag once per question per exam session)
- Flag reason breakdown (bar chart):

| Reason | Count | % |
|---|---|---|
| Wrong Answer Key | 23 | 44% |
| Ambiguous Options | 12 | 23% |
| Outdated/Incorrect Fact | 8 | 15% |
| Question Not in Syllabus | 5 | 10% |
| Rendering Error | 4 | 8% |

**Exam instances where flagged:**
- SSC CGL Mock 12 (2026-03-14) — 31 flags · 1,240 students sat this exam
- SSC CGL Mock 9 (2026-03-08) — 21 flags · 890 students sat this exam

**% of students who flagged:** "52 out of 2,130 students who saw this question flagged it (2.4%)" — a high percentage (> 5%) is a strong signal of a real error.

**Correct Answer (as tagged):** Option B

**Student Answer Distribution (from Div F):**
- Option A: 18%
- Option B: 31% ← tagged correct
- Option C: 42% ← most students chose this
- Option D: 9%

If most students chose a different option than the tagged correct answer, this strongly suggests the answer key is wrong. Shown as: "⚠ Note: 42% of students chose Option C vs 31% who chose Option B (tagged correct). This pattern may indicate an incorrect answer key."

#### Sub-tab 2: Audit Trail Link

- Link to D-12 audit trail for this question — opens in new tab
- "View D-11 Entry" — link to the question in the Published Bank

#### Sub-tab 3: Resolution History

- Timeline of all previous investigation events for this question:
  - Prior dismissals (if any) — who dismissed it, when, note left
  - Prior investigations — what was found, what action was taken
  - Prior unpublish/amendment events

---

### Section 4 — Resolution Actions

**Available from the detail drawer:**

**1. Dismiss (Director + Approver)**
- Dropdown: Dismiss reason category
  - Student Error / Misread — question is correct
  - Duplicate Flag — same students flagging again from a prior exam
  - Off-topic Flag — student flagged wrong question
  - Verified Correct — reviewed and question is definitely correct
- Required note (≥ 30 chars)
- "Dismiss" → status → Resolved (No Action); audit log entry; feeds D-13 Post-Publish Issues as a "Dismissed Flag" event (not counted as unpublish)
- Director can re-open a dismissed flag if new flags arrive later (status reverts to Open)

**2. Mark Under Investigation (Director + Approver)**
- Adds a note: "Being investigated by [Role]"
- Status → Under Investigation
- Useful when the Director needs to review the question offline before deciding

**3. Request SME Clarification (Director)**
- Sends an in-app notification to the question's original SME (role-label communication, not by name internally):
  - "A question you authored has received {N} student flags indicating [reason]. Please review and provide clarification in the notes field below."
  - SME response field — SME cannot see student flag details (only the summary reason), and cannot take any action on the question. Their clarification note is visible only to Director + Approver in this drawer.
- This is an information-gathering step, not a workflow state change. The question remains in its current state.

**4. Unpublish + Amendment Review (Approver only — G2)**
- This is the primary escalation path for confirmed errors.
- Pre-filled with the flag reason as the unpublish reason.
- Unpublish reason category: "Student Flags — Answer Key Error" / "Student Flags — Factual Error" / "Student Flags — Ambiguous Question"
- Required reason note (≥ 30 chars) — pre-filled with flag summary, editable
- 2FA TOTP re-prompt (mandatory for all G2 unpublish actions)
- On confirm:
  - `content_question.state` → `AMENDMENT_REVIEW`
  - `content_question_audit_log` entry: `action: Unpublished · reason: StudentFlagEscalation · flag_count: {N} · unpublished_by: Approver Role`
  - Fast-track review assignment in D-03 (Amendment Reviews tab — highest priority)
  - D-16 feedback status → Resolved (Unpublished)
  - Director notified via D-05 alert: "Question {uuid} unpublished — {N} student flags. Now in fast-track amendment review."
  - Div F system notified (Celery task → `POST /div-f/api/question-status/` webhook): affected exam sessions can display "This question is under review" instead of showing the potentially wrong answer key in results

---

### Section 5 — Auto-Escalation Alerts Panel

**Purpose:** Flags are continuously arriving from live exams — the Director may not be watching D-16 in real-time. Auto-escalation ensures critical-threshold questions are surfaced immediately regardless of the Director's current page.

**Escalation thresholds (configurable in the panel):**

| Threshold | Default | Action |
|---|---|---|
| ≥ 10 flags on a single question | 10 | Status → High · D-05 Director Dashboard alert · In-app notification to Director and Approver |
| ≥ 50 flags on a single question | 50 | Status → Critical · D-05 urgent alert (red) · In-app notification + email notification to Director and Approver |
| > 5% of exam's students flagged the same question | 5% | Immediate Critical escalation regardless of absolute flag count — catches small exams where 10-flag threshold may not be hit but the signal is strong |

**Alert panel display (when Critical items exist):**
Red banner at top of D-16 (and in D-05 Director Dashboard):
> "🚨 Critical: {N} question(s) have exceeded the auto-escalation threshold. Immediate review required."

Lists each critical question with:
- UUID short · Subject · Flag Count · Top flag reason · "Investigate" button (one-click)

**Threshold configuration (Director):**
"Edit Thresholds" → inline form to change the numeric thresholds. Changes saved to `content_feedback_escalation_config` (single row table — only one config exists). New threshold applies to all subsequent flag events; does not retroactively re-classify existing feedback.

---

### Section 6 — Resolution Dashboard (Bottom of Page)

**Purpose:** Summary of feedback handling over the last 30 days — helps Director audit the team's response time and resolution quality.

**KPIs:**
- Total flags received: {N}
- Flags dismissed without action: {N} ({N}%)
- Flags that triggered unpublish (G2): {N} ({N}%)
- Avg time from first flag to resolution: {N} days
- Questions currently open > 7 days without resolution: {N} — red if > 0

**Resolution rate by subject:** Table showing flag counts, resolution rate, and avg resolution time per subject — helps Director see which subjects are generating the most feedback and whether they are being resolved promptly.

---

## 5. Data Models

D-16 reads from Div F's `exam_question_flag` table (student flags arrive via Celery sync task) and writes to `content_feedback_investigation_log` for resolution tracking.

### `exam_question_flag` (source: Div F — read only in Div D)
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_id` | FK → content_question | Cross-division FK |
| `exam_session_id` | FK → Div F exam session | — |
| `student_user_id` | FK → auth.User | PII — never surfaced in Div D UI |
| `flag_reason` | varchar | WrongAnswerKey · AmbiguousOptions · OutdatedFact · OffSyllabus · RenderingError · Other |
| `flag_note` | text | Nullable — student's optional free-text note |
| `flagged_at` | timestamptz | — |

**Celery sync task:** `sync_question_flags` — runs every 5 minutes (Celery beat), reads new rows from `exam_question_flag` since last sync, aggregates into `content_question_flag_aggregate` per question, triggers auto-escalation checks.

### `content_question_flag_aggregate`
| Field | Type | Notes |
|---|---|---|
| `question_id` | FK → content_question | One row per question |
| `total_flag_count` | int | Total across all exam sessions |
| `unique_student_count` | int | Distinct students who flagged |
| `exams_affected_count` | int | Distinct exam sessions |
| `top_flag_reason` | varchar | Most common reason |
| `flag_reason_breakdown` | jsonb | `{reason: count, ...}` |
| `first_flagged_at` | timestamptz | — |
| `last_flagged_at` | timestamptz | — |
| `escalation_status` | varchar | Low · Medium · High · Critical |
| `investigation_status` | varchar | Open · UnderInvestigation · Dismissed · Resolved |
| `last_updated` | timestamptz | — |

### `content_feedback_investigation_log`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `question_id` | FK → content_question | — |
| `actor_id` | FK → auth.User | Director or Approver |
| `action` | varchar | Opened · Dismissed · SMEClarificationRequested · Unpublished · ReopeneD |
| `dismiss_reason_category` | varchar | Nullable |
| `investigation_note` | text | Nullable |
| `flag_count_at_time` | int | Snapshot of flag count when action taken |
| `created_at` | timestamptz | — |

### `content_feedback_escalation_config`
| Field | Type | Notes |
|---|---|---|
| `id` | int | Always 1 — single config row |
| `high_flag_threshold` | int | Default: 10 |
| `critical_flag_threshold` | int | Default: 50 |
| `critical_percentage_threshold` | decimal | Default: 5.0 (%) |
| `updated_by` | FK → auth.User | Director |
| `updated_at` | timestamptz | — |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.view_feedback_queue')` — Roles 18 + 29 |
| Dismiss action | Roles 18 + 29 |
| Unpublish (G2) action | Role 29 only — `permission='content.publish_question'` checked at action endpoint |
| Student identity data | Never surfaced in Div D UI — `student_user_id` from `exam_question_flag` is excluded from all ORM queries in Div D. Div D reads only aggregated counts and reason categories. |
| Export | Role 18 only — CSV of aggregate data only (no student IDs, no student notes) |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| A question is flagged but has already been unpublished (state = AMENDMENT_REVIEW) | New flags for this question are still recorded in `content_question_flag_aggregate` but D-16 shows the question's status as "Already Under Amendment Review." No new escalation triggers fire — the question is already being handled. |
| Flag sync task fails (Div F API unavailable) | `sync_question_flags` Celery task retries up to 3 times with exponential backoff. If all retries fail, a system alert appears in D-05: "Question flag sync failed — flags from the last {N} minutes may not be reflected in D-16." Data is not lost — Div F stores the flags; they will sync on the next successful run. |
| A question is in a frozen exam (content freeze active) and gets critical flags | The unpublish action (G2) overrides the content freeze — the freeze applies to new question submissions, not to post-publish emergency actions. The Approver can still unpublish a frozen-exam question. Div F is notified via the webhook. |
| Bulk dismiss of 50 Low-flag questions — one question in the batch is subsequently escalated to Critical by a new flag arriving during the dismiss operation | Race condition: the dismiss is processed first (timestamp wins); the subsequent flag sync increments the count to Critical threshold, re-opens the investigation, and generates a Critical alert. The prior dismiss is recorded in the investigation log but the question returns to Open status. |
| Director clicks "Request SME Clarification" on a question whose original SME account has been deactivated | The in-app notification cannot be delivered (account inactive). D-16 shows: "Original SME account is deactivated. Contact Content Director to locate this SME or reassign the clarification." Director must resolve directly without SME input. |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| Div F Student Exam Interface | Div F → D-16 | Student flags per question per exam session | Celery `sync_question_flags` reads `exam_question_flag` every 5 minutes |
| D-04 Approval Queue (G2) | D-16 → D-04 | Unpublish + amendment review triggered from D-16 → question appears in D-04 Amendment Reviews tab (highest priority) | Direct `content_question.state` update → D-04 queue picks up via ORM |
| D-03 Review Queue (G2) | D-16 → D-03 | After unpublish, question enters D-03 Amendment Reviews tab for fast-track reviewer re-check | Same state transition triggers D-03 fast-track queue |
| D-13 Quality Analytics | D-16 → D-13 | Post-publish issue data (flag-triggered unpublishes + dismissed flags) feeds D-13 Post-Publish Issues tab | D-13 reads `content_feedback_investigation_log` + `content_question_audit_log` for Unpublished events |
| D-05 Director Dashboard | D-16 → D-05 | Auto-escalation alerts (Critical + High) surface in D-05 Stale Alerts panel | D-05 reads `content_question_flag_aggregate` where `escalation_status = Critical AND investigation_status = Open` |
| D-12 Audit History | D-16 → D-12 | Every D-16 resolution action (dismiss, unpublish) generates a D-12 audit log entry | `content_question_audit_log` INSERT on each resolution action |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- Placeholder: "Search by question ID, subject, or topic…".
- Searches: question UUID (short 8-char), subject name, topic name.
- Debounced 300ms. Results update the feedback table in place.
- Search available on all severity tabs (Critical / High / Medium / Low / Resolved).

### Sortable Columns — Feedback Table
| Column | Default Sort |
|---|---|
| Flag Count | **DESC (most flagged first)** — default |
| Last Flagged | DESC |
| Exams Affected | DESC |
| Students Reached | DESC |
| Status | Custom: Open → Under Investigation → Dismissed → Resolved |

### Pagination
- Feedback Table: 50 rows per page, numbered controls.
- Resolved tab: 50 rows, numbered controls — resolved items accumulate rapidly.
- Resolution Dashboard (bottom): no pagination — summary KPIs and charts only.

### Row Selection — Bulk Dismiss
- Checkbox column visible to Director.
- Max 100 rows for bulk dismiss.
- Bulk action bar: "{N} selected · [Bulk Dismiss]".
- Bulk Dismiss modal: Dismiss reason category (dropdown, required) + shared dismiss note (required, ≥ 20 chars).
- "Select All on Page" + "Select All N Results" pattern available.

### Empty States
| Tab | Heading | Subtext |
|---|---|---|
| Critical | "No critical feedback" | "Questions receiving ≥50 student flags will appear here for immediate action." |
| High | "No high-priority feedback" | "Questions with 10–49 flags will appear here." |
| Medium | "No medium feedback" | "Questions with 3–9 flags will appear here." |
| Low | "No feedback yet" | "Student question flags from exams will appear here as they arrive." |
| Resolved | "No resolved feedback" | "Dismissed and resolved flags will appear here after action is taken." |

### Toast Messages
| Action | Toast |
|---|---|
| Mark Under Investigation | ✅ "Marked as under investigation" (Success 4s) |
| Dismiss | ✅ "Feedback dismissed" (Success 4s) |
| Bulk Dismiss | ✅ "{N} feedback items dismissed" (Success 4s) |
| Request SME Clarification | ✅ "Clarification request sent to original SME" (Success 4s) |
| Unpublish (G2, Approver) | ✅ "Question unpublished — amendment review created" (Success 4s) |
| Re-open dismissed feedback | ✅ "Feedback re-opened" (Success 4s) |
| Threshold saved | ✅ "Escalation thresholds updated" (Success 4s) |
| Flag sync delayed (> 5 min) | ⚠ "Flag sync delayed — data may be up to {N} minutes behind" (Warning 8s) |

### Loading States
- Feedback Table: 8-row skeleton on initial load, tab switch, filter apply, and 60s auto-refresh.
- Auto-escalation alert panel: 3-row skeleton on initial load. HTMX poll every 60s — panel fades to 60% during refresh.
- Question Detail drawer: 5-line skeleton while question and flag data loads.
- Flag reason breakdown chart (drawer): chart-area shimmer.
- Student answer distribution panel (drawer): bar chart shimmer.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Full feedback table all columns. Drawer 760px. Auto-escalation panel at top. |
| Tablet | Table: Flag Count badge, Subject, Status, Action — others in row expand. Drawer 80%. |
| Mobile | Table: Subject, Flag Count (large badge), Investigate button. Tap row to open drawer. Drawer full screen. Bulk select: long-press to activate selection mode (mobile UX convention). |

### Charts (Drawer)
- **Flag Reason Breakdown (drawer, sub-tab 1):** Horizontal bar chart — Wrong Answer / Ambiguous / Outdated / Off-Syllabus / Rendering. Values: count + %. Sorted by count DESC.
- **Student Answer Distribution (drawer, sub-tab 1):** Horizontal bar chart — A / B / C / D option counts. Correct option bar highlighted green. If most students picked a different option: amber "Most students chose Option {X}" callout.
- **Resolution Dashboard (page bottom):** Pie chart — Dismissed vs Unpublished vs Under Investigation (open) vs Open. 12-month bar chart: flags received per month vs flags resolved per month.

### Auto-Escalation Alert Panel — Interaction
- Shown at top of page when Critical items exist (always visible, not collapsible when critical).
- Collapsed by default when no Critical items.
- Per-critical item: UUID · Subject · Flag Count · Top Reason · "Investigate" button → opens drawer directly.
- "Edit Thresholds" link → opens a small modal with numeric inputs for High/Critical thresholds and percentage threshold.

### Role-Based UI
- Unpublish (G2) action button: Approver (29) only. Director (18) sees "Unpublish" button greyed with tooltip "Only the Question Approver can unpublish questions."
- "Request SME Clarification": Director only. Approver does not see this option.
- Bulk Dismiss: Director only.
- Student identity: never shown (student_user_id excluded from all ORM queries in Div D layer).
- Export CSV: Director only.

---

*Page spec complete.*
*Next file: `d-17-notes-analytics.md`*
