# D-17 — Notes Analytics & Usage

> **Route:** `/content/notes/analytics/`
> **Division:** D — Content & Academics
> **Primary Roles:** Content Director (18) · Notes Editor (30)
> **Scoped Access:** Notes Editor — own notes only (ORM-scoped)
> **File:** `d-17-notes-analytics.md`
> **Priority:** P3 — Meaningful once ≥ 50 notes published and student engagement data available
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Notes Analytics & Usage
**Route:** `/content/notes/analytics/`
**Part-load routes:**
- `/content/notes/analytics/?part=overview-kpis` — top KPI strip
- `/content/notes/analytics/?part=usage-table` — notes usage table
- `/content/notes/analytics/?part=coverage-gaps` — topic gap analysis panel
- `/content/notes/analytics/?part=engagement-chart&subject={id}` — per-subject engagement trend
- `/content/notes/analytics/?part=create-request-form` — note request creation form

---

## 2. Purpose (Business Objective)

Notes are the study material layer of the content platform — a well-structured PDF note for a syllabus topic reduces student dependency on external resources and keeps them within the platform ecosystem. But a notes library without usage analytics is a filing cabinet: content accumulates without knowing what students are actually reading, what subjects are under-resourced, or whether the Notes Editor's production is targeting the right topics.

D-17 answers the questions:
- Which notes are students actually downloading and reading?
- Which syllabus topics have no notes at all?
- Which topics have notes but low engagement (possibly poor quality, wrong depth, or outdated)?
- Which Notes Editor is producing the most-used content?
- Where should the Director prioritise new notes creation?

**Business goals:**
- Surface notes usage data (downloads, view time) from Div F student analytics
- Identify topic coverage gaps (syllabus topics with no published notes)
- Enable Director to create formal "Note Requests" — tasks assigned to a Notes Editor with a target topic, deadline, and priority
- Give Notes Editors visibility into how their own notes are being used (own-data only)
- Track notes quality signals: low-engagement notes despite high topic importance may indicate quality or relevance issues

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full — all subjects, all editors, all topics, gap analysis, note request creation |
| Notes Editor (30) | Scoped — own notes only. Sees usage stats for notes they personally authored. Cannot see other editors' data or the full gap analysis. |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Filters

- H1: "Notes Analytics & Usage"
- Global filters:
  - Subject (multi-select)
  - Exam Type (multi-select)
  - Date range (usage date — default: last 90 days)
  - Notes Editor (Director only — multi-select, all editors visible)
- Notes Editor view shows only: "Your Notes Analytics" heading with no editor filter (scoped to self automatically)

---

### Section 2 — Overview KPI Strip

**Director view:**

| KPI | Description |
|---|---|
| Total Notes Published | All-time count across all subjects |
| Notes Published (period) | In selected date range |
| Total Topic Downloads | Sum of all download events in period |
| Avg Downloads per Note | Downloads ÷ published notes (period) |
| Topics with Zero Notes | COUNT of syllabus topics (from `content_taxonomy_topic`) with no published note — amber if > 20% of topics |
| Topics with Stale Notes | Notes not updated in > 6 months with active syllabus coverage — amber |

**Notes Editor view (own metrics only):**

| KPI | Description |
|---|---|
| My Notes Published | All-time count |
| Total Downloads (my notes) | Sum for this editor's notes |
| Avg Downloads per Note | Own average |
| My Most Downloaded Note | Title + download count |
| Notes with < 10 Downloads | Count — notes that may need quality review or better topic targeting |

---

### Section 3 — Notes Usage Table

**Default sort:** Downloads (period) descending — most-used notes first.

**Table columns:**

| Column | Description |
|---|---|
| Note Title | Truncated title — click opens detail drawer |
| Subject | — |
| Topic | — |
| Subtopic | — |
| Version | Current version number |
| Published Date | — |
| Last Updated | Date of most recent version publish |
| Downloads (period) | Total download events in selected date range |
| Unique Students (period) | Distinct students who downloaded (from Div F) |
| Avg View Duration | Average minutes spent viewing (from Div F PDF viewer telemetry — where available) |
| Exam Types Covered | Which exam types this note is tagged to |
| Editor | Role label (Notes Editor role — not personal name per DPDPA) — Director view only |
| Engagement Score | Composite: `(downloads × 0.5) + (unique_students × 0.3) + (avg_view_duration_normalized × 0.2)` — displayed as 0–100 score, colour-coded |

**Engagement Score colour thresholds:**
- Green ≥ 70: High engagement
- Amber 30–69: Moderate
- Red < 30: Low engagement — note may need attention

**Row quick actions (Director):**
- "View Details" → opens note detail drawer (Section 5)
- "Create Update Request" → pre-fills a Note Request (Section 6) with this note's topic + editor + "Update" type

**Row quick actions (Notes Editor — own notes only):**
- "View Details" → own notes detail drawer (engagement stats only, no other editor comparison)

---

### Section 4 — Coverage Gap Analysis (Director Only)

**Purpose:** Systematic identification of syllabus topics with insufficient notes coverage — the highest-value planning tool in D-17.

**Gap classification rules:**

| Gap Type | Definition |
|---|---|
| No Coverage | Topic exists in taxonomy (D-09) but has zero published notes |
| Single Note Only | Topic has exactly 1 note — fragile coverage (if that note is outdated or wrong, there is no fallback) |
| Stale Coverage | Topic has notes but all were published > 6 months ago AND the topic has had syllabus updates (tracked in `content_taxonomy_topic.last_syllabus_update`) |
| Low Engagement | Topic has notes but engagement score < 30 AND the topic is high-importance (importance derived from exam question frequency in D-14 Syllabus Coverage page) |
| Exam-Type Mismatch | Topic has notes but they are not tagged to the correct exam types for this topic's coverage |

**Coverage Gap Table:**

| Column | Description |
|---|---|
| Subject | — |
| Topic | — |
| Gap Type | No Coverage · Single Note · Stale · Low Engagement · Exam-Type Mismatch |
| Importance Score | From D-14: how many published questions exist for this topic. Topics with many questions but no notes = high priority gap. |
| Exam Types Needing Coverage | Which exam types this topic appears in, where notes are missing |
| Existing Notes Count | 0, 1, or N |
| Last Note Published | Date — "—" if no notes |
| "Create Note Request" | Button — see Section 6 |

**Filter:** Gap type filter (default: No Coverage + Single Note Only — the most actionable gaps). "Show All Gaps" toggle includes Stale and Low Engagement.

**Export:** "Export Gap Report" → CSV of current view — used by Director to plan production assignments for Notes Editors.

---

### Section 5 — Note Detail Drawer

**Trigger:** Click any row in the Usage Table.

**Drawer width:** 680px. Two sub-tabs:

#### Sub-tab 1: Engagement Details

**Usage over time:** Line chart — downloads per week for the last 12 weeks. Shows spikes (likely before exams) and troughs.

**Student segment breakdown (where available from Div F):**
- School students: {N} downloads
- College students: {N} downloads
- Coaching students: {N} downloads

**Exam type association:** "Students who downloaded this note were most frequently sitting: SSC CGL Mock (67%) · SSC CHSL Mock (23%) · Other (10%)"

**Avg view duration by segment:** If Div F PDF viewer telemetry is available: "School students: avg 4.2 min · Coaching students: avg 11.8 min" — coaching students spend longer (expected: more thorough study).

**Quality signals:**
- Download-to-view ratio: "Downloaded by {N} students · {N}% opened and read for > 1 minute" — a note downloaded but not read is either not relevant or the file is too large/unreadable
- Bounce rate: "Downloaded and immediately closed (< 30 seconds): {N}%" — high bounce may indicate the note doesn't match the topic expectation or the format is poor

#### Sub-tab 2: Note Info

- Full title · Version history (version N published on {date})
- Topic mapping: Subject > Topic > Subtopic
- Exam types tagged
- "View in D-06" link → opens the note in D-06 Notes Management for editing (Director or Notes Editor for own note)
- "View File" → opens the published PDF (S3 CloudFront URL — new tab)
- Notes Editor: role label (not personal name)

---

### Section 6 — Note Request System

**Purpose:** Director creates formal assignments for new notes or updates to existing notes — structured task management for the Notes Editors.

**"Create Note Request" button:** Always visible to Director (also accessible inline from the Coverage Gap Table per-row action).

**Note Request form:**

| Field | Description |
|---|---|
| Request Type | New Note · Update Existing Note · Urgent (exam in < 30 days) |
| Subject | Dropdown |
| Topic | Filtered dropdown based on Subject |
| Subtopic | Optional |
| Exam Types | Multi-select — which exam types this note should cover |
| Target Editor | Dropdown — all active Notes Editors (Director selects who will do this) |
| Deadline | Date picker — validates: must be ≥ 3 days from today |
| Priority | High · Medium · Low |
| Scope Note | Free text — "Focus on last 3 years Current Affairs for GK · approx 8–12 pages" |
| Reference Questions | Optional: paste up to 5 question UUIDs from D-11 — the editor can see these as context for what depth is needed |

**On submit:**
- `content_note_request` record created
- In-app notification to the assigned Notes Editor: "New note request assigned: [Topic] — due [date]. View in D-06."
- D-06 Notes Management shows the request in the Notes Editor's "Incoming Queue" tab as a pre-filled task card (not a question, but a production task)

**Note Request list (Director view — below the Create form):**

| Column | Description |
|---|---|
| Topic | — |
| Editor | Role label |
| Type | New / Update / Urgent |
| Deadline | — |
| Status | Open · In Progress · Published · Overdue |
| Days Until Deadline | — red if overdue |
| Priority | — |
| Actions | Edit · Cancel (if not yet In Progress) |

**Status transitions:**
- Open: request created, editor notified
- In Progress: editor begins working (D-06 converts request card to an active note draft)
- Published: editor publishes the note — request auto-closed
- Overdue: deadline passed without publish — Director receives D-05 alert

---

## 5. Data Models

D-17 is primarily read-heavy analytics. Reads from Div F tables (via Celery sync) and Div D taxonomy/notes tables.

### `content_notes_usage_aggregate` (synced from Div F)
| Field | Type | Notes |
|---|---|---|
| `note_id` | FK → content_notes | One row per note |
| `period_month` | date | First day of month |
| `download_count` | int | — |
| `unique_student_count` | int | — |
| `avg_view_duration_seconds` | int | Nullable — from Div F telemetry where available |
| `exam_type_breakdown` | jsonb | `{exam_type_code: count}` |
| `student_segment_breakdown` | jsonb | `{school: N, college: N, coaching: N}` |
| `last_synced_at` | timestamptz | — |

**Sync mechanism:** Celery `sync_notes_usage` task — runs nightly (low priority, no SLA requirement for notes analytics). Reads from Div F `student_notes_access_log` table.

### `content_note_request`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `request_type` | varchar | New · Update · Urgent |
| `subject_id` | FK → content_taxonomy_subject | — |
| `topic_id` | FK → content_taxonomy_topic | — |
| `subtopic_id` | FK → content_taxonomy_subtopic | Nullable |
| `exam_type_codes` | jsonb | Array of exam type codes |
| `assigned_editor_id` | FK → auth.User | Notes Editor |
| `deadline` | date | — |
| `priority` | varchar | High · Medium · Low |
| `scope_note` | text | Nullable |
| `reference_question_ids` | jsonb | Nullable — array of UUIDs |
| `status` | varchar | Open · InProgress · Published · Overdue · Cancelled |
| `created_by` | FK → auth.User | Director |
| `created_at` | timestamptz | — |
| `closed_at` | timestamptz | Nullable — when status → Published or Cancelled |
| `resulting_note_id` | FK → content_notes | Nullable — populated when editor publishes the note |

### `content_notes_coverage_gap` (computed — refreshed nightly by Celery)
| Field | Type | Notes |
|---|---|---|
| `topic_id` | FK → content_taxonomy_topic | One row per topic per gap type |
| `gap_type` | varchar | NoCoverage · SingleNoteOnly · StaleContent · LowEngagement · ExamTypeMismatch |
| `importance_score` | int | From D-14 question count for this topic |
| `computed_at` | timestamptz | — |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.view_notes_analytics')` — Roles 18 + 30 |
| Director | Full — all notes, all editors, gap analysis, note requests |
| Notes Editor | ORM-scoped: all queries filtered to `content_notes.editor_id = request.user.id`. Gap Analysis tab not rendered (403 on part-route). Note Request list shown as read-only: "Requests Assigned to Me." |
| Note Request creation | Role 18 only |
| Export | Role 18 only |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Div F usage sync not yet available (platform just launched) | Usage Table shows notes with 0 downloads + note: "Student usage data syncs nightly from Div F. No data is available yet — check back after the first exam session using platform notes." KPI strip shows "No usage data available." |
| A note has been published but is for a topic that was subsequently archived in D-09 | Note still appears in D-17 usage table with a "[Archived Topic]" label on the Topic column. Gap analysis excludes archived topics — they are not treated as gaps. Director can unpublish/archive the note via D-06. |
| Notes Editor's account is deactivated mid-cycle with open Note Requests | Open requests remain in the system with status Open. Director receives a D-05 alert: "Notes Editor [role label] has been deactivated — {N} open note requests are unassigned." Director can reassign via the Note Request edit action. |
| Engagement score calculation when avg_view_duration is null (Div F telemetry not available) | Engagement score computed from available components only (downloads × 0.65 + unique_students × 0.35). A "(partial data)" note is shown next to the score. |
| Director creates a Note Request for a topic that already has a recent, high-engagement note | Validation warning (not blocked): "This topic already has {N} notes with an engagement score of {N} (High). Consider reviewing existing coverage before creating a new request." Director can proceed or cancel. |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| Div F Student Analytics | Div F → D-17 | Notes download counts, view duration, student segment breakdown | Celery `sync_notes_usage` nightly from `student_notes_access_log` |
| D-06 Notes Management | D-17 → D-06 | Note Requests appear in D-06 Notes Editor's Incoming Queue as task cards | `content_note_request` table read by D-06 queue |
| D-14 Syllabus Coverage | D-14 → D-17 | Topic importance scores (question count per topic) used in gap analysis | `content_syllabus_target` + `content_question` aggregate read |
| D-09 Taxonomy | D-09 → D-17 | Topic tree defines the complete coverage map — D-17 compares published notes against this | `content_taxonomy_topic` read (all active, non-archived topics) |
| D-05 Director Dashboard | D-17 → D-05 | Overdue note requests + critical coverage gaps surface in D-05 Stale Alerts panel | D-05 reads `content_note_request` (status=Overdue) + `content_notes_coverage_gap` |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- **Usage Table:** Placeholder "Search notes by title or topic…". Searches: note title, topic name, subtopic name. Debounced 300ms.
- **Coverage Gap Table:** Placeholder "Search topics…". Searches: topic name, subject name.
- **Note Request List:** Placeholder "Filter requests by topic or status…". Searches: topic name, status label.

### Sortable Columns — Notes Usage Table
| Column | Default Sort |
|---|---|
| Downloads (period) | **DESC (most downloaded first)** — default |
| Unique Students | DESC |
| Avg View Duration | DESC |
| Engagement Score | DESC |
| Published Date | DESC |
| Last Updated | DESC |

### Sortable Columns — Coverage Gap Table
| Column | Default Sort |
|---|---|
| Importance Score | **DESC (most important topics first)** — default |
| Gap Type | Custom: No Coverage → Single Note → Stale → Low Engagement → Mismatch |
| Subject | ASC |
| Topic | ASC |

### Sortable Columns — Note Request List
| Column | Default Sort |
|---|---|
| Deadline | **ASC (soonest deadline first)** — default |
| Priority | Custom: High → Medium → Low |
| Status | Custom: Overdue → Open → In Progress → Published |

### Pagination
- Usage Table: 50 rows, numbered controls.
- Coverage Gap Table: 50 rows, numbered controls.
- Note Request List: 25 rows, numbered controls.

### Empty States
| Section | Heading | Subtext | CTA |
|---|---|---|---|
| Usage Table — no data | "No usage data yet" | "Student usage data syncs nightly from Div F. Data appears after the first exam session using platform notes." | — |
| Usage Table — no notes published | "No notes published" | "Publish notes from D-06 to see them here." | "Go to Notes Management" → D-06 |
| Coverage Gap Table — no gaps | "No coverage gaps ✓" | "All active syllabus topics have at least one published note." | — |
| Note Request List — none | "No note requests" | "Create a note request to assign a specific topic to a Notes Editor." | "Create Request" |
| Note Detail Drawer — no engagement | "No engagement data yet" | "Data appears after students access this note via the platform." | — |

### Toast Messages
| Action | Toast |
|---|---|
| Note Request created | ✅ "Note request created — {Editor role} notified" (Success 4s) |
| Note Request cancelled | ✅ "Note request cancelled" (Success 4s) |
| Note Request deadline passed | ⚠ "Note request for '{topic}' is overdue — {N} days past deadline" (Warning — shown as D-05 Stale Alerts item, not inline toast) |
| Export Gap Report | ℹ "Export started — download link will appear when ready" (Info 6s) |

### Loading States
- Usage Table: 8-row skeleton on initial load, filter apply, tab switch.
- KPI strip (Overview): tile shimmer rectangles.
- Coverage Gap Table: 8-row skeleton.
- Note Detail Drawer: 5-line skeleton while engagement data loads. Engagement chart: chart-area shimmer.
- Coverage Gap nightly refresh: no loading indicator (background Celery task — data is from last compute). "Last computed: {timestamp}" shown below table header. "Refresh Now" button triggers immediate recompute (Director only) with spinner.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Usage Table full columns. Note Detail Drawer 680px. Coverage Gap Table full columns. |
| Tablet | Usage Table: Title, Subject, Downloads, Engagement Score, Action — others in row expand. Drawer 80%. |
| Mobile | Usage Table: Title (truncated), Downloads badge, Engagement colour dot, Action button. Tap row to open drawer. Drawer full screen. Coverage Gap: Topic, Gap Type badge, Create Request button. |

### Charts
- **Overview KPI strip:** No charts — metric tiles.
- **Usage Table — Engagement Score:** Coloured badge (green/amber/red) per row inline. Hover tooltip shows score components.
- **Note Detail Drawer — Engagement Over Time:** Line chart (weekly downloads, last 12 weeks). No-data: "Not enough data for a trend view yet."
- **Note Detail Drawer — Student Segment Breakdown:** Donut chart — School / College / Coaching proportions. No-data: segment breakdown text only.
- **Coverage Gap Table:** Importance Score column shown as a mini bar fill (width ∝ score) — visual scan aid.
- **Note Request List — Priority indicator:** Coloured dot (red=High, amber=Medium, grey=Low) before each row.

### Role-Based UI
- Director (18): full access — Usage Table (all notes), Coverage Gap analysis, Note Request create/cancel/edit, Export.
- Notes Editor (30): ORM-scoped — Usage Table shows own notes only. Coverage Gap tab not rendered (403 on part-route). Note Request List: read-only "Requests Assigned to Me" (cannot create or cancel requests — Director owns that workflow).
- "Create Note Request" button: Director only.
- "Export Gap Report" button: Director only.
- Engagement Score column: both Director and Notes Editor (for own notes).

---

*Page spec complete.*
*Next file: `d-18-reports.md`*
