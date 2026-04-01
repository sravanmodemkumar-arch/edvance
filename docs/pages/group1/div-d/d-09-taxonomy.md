# D-09 — Subject-Topic Taxonomy Manager

> **Route:** `/content/director/taxonomy/`
> **Division:** D — Content & Academics
> **Primary Role:** Content Director (18) — full edit access including Style Guide + Bulk Retag
> **Read Access:** All Div D roles — SMEs (19–27) for tagging + Style Guide reference; Reviewer (28) for Style Guide; Approver (29) for Style Guide + read; Notes Editor (30) for tagging
> **File:** `d-09-taxonomy.md`
> **Priority:** P1 — Taxonomy must exist before any SME tags questions
> **Status:** ⬜ Not started
> **Amendments:** G10 (Bulk Retag action — bulk reassign questions when taxonomy nodes are archived or restructured)

---

## 1. Page Name & Route

**Page Name:** Subject-Topic Taxonomy Manager
**Route:** `/content/director/taxonomy/`
**Part-load routes:**
- `/content/director/taxonomy/?part=tree&subject_id={id}` — taxonomy tree for a subject
- `/content/director/taxonomy/?part=edit-panel&node_id={id}&node_type={subject|topic|subtopic}` — right edit panel
- `/content/director/taxonomy/?part=gap-view&subject_id={id}` — gap view table
- `/content/director/taxonomy/?part=retag-progress&job_id={uuid}` — bulk retag Celery progress
- `/content/director/taxonomy/?part=style-guide&subject_id={id}` — style guide content

---

## 2. Purpose (Business Objective)

The taxonomy is the structural backbone of the entire content platform. Every question ever authored, every note ever structured, every exam paper ever built — all reference this Subject → Topic → Subtopic hierarchy. D-09 is where that hierarchy is defined, maintained, and evolved.

Without the taxonomy:
- SMEs cannot tag questions (D-02 topic dropdown is empty)
- Syllabus coverage cannot be measured (D-14 has no structure to report against)
- Notes cannot be categorised (D-06 structuring form has no topics)
- Exam pattern builders in Div B cannot select topic weightings
- Pool adequacy analysis (G12 in D-14) has no topic nodes to compute against

At 9 subjects × ~300 topics × ~1,500 subtopics, the taxonomy is not small. It evolves annually as exam boards update syllabi. D-09 manages this evolution carefully: nodes can be archived (soft-deleted) but never hard-deleted, and archiving a node with live questions requires a bulk retag operation (G10) that moves those questions to the restructured taxonomy before archiving is permitted.

The Style Guide tab embedded in D-09 stores per-subject authoring standards — the quality contract between the Content Director and the 9 SMEs.

**Business goals:**
- Maintain an authoritative Subject → Topic → Subtopic hierarchy for all 9 subjects
- Enable safe taxonomy evolution (syllabus changes, restructuring) via soft-archive + bulk retag (G10)
- Track coverage gaps per topic node (questions with < 10 published = amber, < 3 = red)
- Map exam types to topics — which exam types include which topics
- Store and display per-subject Style Guides for quality calibration
- Provide Memcached-cached taxonomy for fast dropdown population in D-02, D-06, D-07

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full — add/edit/archive nodes · Style Guide edit · Bulk Retag trigger (G10) · Exam Type Mapping edit |
| SME ×9 (19–27) | Read — taxonomy for own subject (dropdown source in D-02) · Style Guide for own subject (reference) |
| Question Reviewer (28) | Read — full taxonomy (for context) · Style Guide (all subjects) |
| Question Approver (29) | Read + Bulk Retag trigger (G10) — Approver can initiate bulk retag for published questions |
| Notes Editor (30) | Read — taxonomy (dropdown source in D-06) |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header

- H1: "Taxonomy Manager"
- Subject selector (left-side tab bar or dropdown): 9 subjects — each click loads that subject's tree
- "Add Root Topic" button (Content Director only) — adds a new top-level topic to the selected subject
- "Export Taxonomy CSV" button — exports the full taxonomy for the selected subject as CSV: subject / topic_code / topic_name / subtopic_code / subtopic_name / published_question_count / active_status

**Reference links (top-right, visible to Content Director only):**

> **Manage Subjects →** [D-20 — Content Configuration, Subjects tab]
> **Manage Exam Types →** [D-20 — Content Configuration, Exam Types tab]

D-09 manages the **topic/subtopic** layer of the taxonomy (what the question is about, within a subject). The **subject** and **exam type** reference tables are managed in D-20. These links provide in-context discovery for Directors who want to add a new subject or exam type code before building the taxonomy tree under it.

**Subject selector behaviour with Deprecated/Archived codes:**
- The Subject selector tab bar in D-09 shows all subjects from `content_subject`, including Archived ones (shown with a grey "Archived" badge and italicised name).
- Archived subjects: taxonomy is visible for audit purposes, but "Add Root Topic" is disabled with tooltip: "This subject is archived. Reactivate it in D-20 to add new taxonomy nodes."
- Deprecated Exam Types in the Exam Type Mapping tab (Section 6) are shown with a strikethrough label — the mapping is retained for historical reference but new mappings to deprecated exam types are blocked.

---

### Section 2 — Tree Panel (Left 35%)

**Purpose:** Collapsible 3-level tree showing the full taxonomy for the selected subject.

**Layout:** Left panel, fixed 35% width, vertically scrollable.

**Subject level (1):**
Subject name (e.g. "Mathematics") as the root.

**Topic level (2):**
Each topic node:
- Expand/collapse triangle
- Topic name
- Published question count badge (e.g. "247 ✓") — clicking badge shows breakdown by difficulty
- Active / Archived status dot (green = active, grey = archived)
- If archived: shown with strikethrough text, greyed out

**Subtopic level (3) — visible when topic expanded:**
Each subtopic node:
- Subtopic name
- Published question count badge
- Active / Archived status

**Node click:** Loads the Edit Panel in the right 65% for that node.

**Add child node:** "+" icon on hover beside each topic node — opens a "New Subtopic" inline form within the tree.

**Coverage indicators (per node):**
- ≥ 30 published: subtle green tint
- 10–29: neutral
- 3–9: amber tint
- < 3: red tint (critical gap)

---

### Section 3 — Edit Panel (Right 65%)

**Purpose:** Edit a selected taxonomy node's name, description, syllabus reference, status, and parent.

**Header:** "Editing: [Topic Name]" or "Editing: [Subtopic Name]"

**Fields:**

| Field | Type | Notes |
|---|---|---|
| Name | Text input | Required · max 200 chars |
| Code | Read-only (auto-generated on create: `MATH_001`, `MATH_001_01`) | Used in D-07 CSV template |
| Description | Textarea | Optional — helps SMEs understand the exact scope of this topic |
| Official Syllabus Reference | Text input | e.g. "SSC CGL 2024 Notification §3.2.1 — Arithmetic" · Optional but strongly recommended |
| Parent Node | Read-only display + "Move to Different Parent" action — see below | — |
| Status | Toggle: Active / Archived | — |

**"Move to Different Parent" action:**
Changes the parent topic of a subtopic (or parent subject of a topic). Opens a tree selector modal: "Select new parent". On confirm: the node moves in the tree + all questions tagged to this node retain their tag (the tag now resolves to the new parent location). Logged in `content_taxonomy_audit_log`.

**Statistics panel (below fields, read-only):**
- Published question count (with link to D-11 filtered to this topic)
- In-pipeline count (UNDER_REVIEW + PENDING_APPROVAL)
- Notes with this topic tag (with link to D-11 Notes tab)
- Subtopic count (if this is a topic node)

**"Archive" button:**

When the Director clicks "Archive":
1. System checks: does this node have published questions tagged to it?
   - If 0 published questions: archive immediately — status → Archived. Dropdown in D-02/D-06 will no longer show this node.
   - If > 0 published questions: **Bulk Retag required first** (G10) — see Section 4.

2. Archive constraints:
   - Cannot archive a Subject node (9 subjects are permanent — syllabus changes affect topics/subtopics, not subjects themselves)
   - Can archive a Topic or Subtopic
   - Archived node shown in tree with strikethrough — can be restored (toggle Active) if archived incorrectly

**Actions for Director only:** Save · Archive · Restore (if archived). For read-only roles: all fields are read-only, buttons hidden.

---

### Section 4 — Bulk Retag Action (Amendment G10)

**Trigger:** Director or Approver clicks "Archive" on a node that has published questions tagged to it.

**Purpose:** Before archiving a taxonomy node, all questions tagged to it must be moved to a valid alternative node. This operation can affect thousands of questions — a batch Celery task handles it without freezing the UI.

**Bulk Retag workflow:**

**Step 1 — Retag Required dialog:**
"This node has {N} published questions tagged to it. Before archiving, you must reassign all questions to another topic/subtopic. This is required to maintain question discoverability and coverage analysis accuracy."

"Select Target Node" — dropdown/tree selector:
- Source: same subject only (cannot retag across subjects — a Math question cannot be retagged to Physics)
- Dropdown shows all Active topic/subtopic nodes for this subject (excluding the current node being archived)
- Each option shows the published question count already in that target node
- Recommended targets shown first (topics in the same subject area)

**Step 2 — Impact summary:**
"Retagging will move {N} questions from '{Source Topic}' to '{Target Topic}'. This includes:
- {N_published} Published questions — questions remain active, tags updated
- {N_review} Questions in review/pending approval — tags updated, no workflow interruption
- {N_draft} Draft questions — tags updated

No questions will be returned to SMEs. No re-review will be triggered. All tag changes will be logged in D-12 as 'Taxonomy Retag' events."

**Step 3 — Confirm + Execute:**
"Retag and Archive" button → Celery task `portal.tasks.content.bulk_retag_taxonomy` is queued.

Task logic (batch UPDATE in Django ORM):
```python
# Retag all questions from old_topic_id to new_topic_id
content_question.objects.filter(
    topic_id=old_topic_id  # source node
).update(
    topic_id=new_topic_id,  # target
    subtopic_id=new_subtopic_id or None,
    updated_at=now()
)
# Log each update in content_question_audit_log with action='TaxonomyRetag'
```

**Step 4 — Progress:**
HTMX polls `?part=retag-progress&job_id={uuid}` every 2s.
"Retagging… 847 / 2,341 questions complete"

**Step 5 — Completion:**
"✅ Bulk retag complete. 2,341 questions moved from '{Source Topic}' to '{Target Topic}'. Now archiving the source node."
The source taxonomy node is archived automatically after the retag completes.

**Audit trail:**
- Per-question: `content_question_audit_log` entry with `action: TaxonomyRetag · before: {old_topic} · after: {new_topic} · task_id: {uuid}`
- Batch: `content_taxonomy_retag_job` record with source + target + question counts + Celery task ID + duration

**Data model:**
### `content_taxonomy_retag_job`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `source_node_id` | UUID | topic or subtopic being archived |
| `source_node_type` | varchar | topic / subtopic |
| `target_node_id` | UUID | replacement topic/subtopic |
| `initiated_by` | FK → auth.User | Director or Approver |
| `celery_task_id` | varchar | — |
| `total_questions` | int | — |
| `completed_questions` | int | — |
| `status` | varchar | Pending · Running · Completed · Failed |
| `created_at` | timestamptz | — |
| `completed_at` | timestamptz | Nullable |

---

### Section 5 — Gap View Tab

**Purpose:** Topic nodes across the selected subject where the published question count is below healthy levels — prioritised list for the Director to identify which topics need more SME attention.

**Table:**

| Column | Description |
|---|---|
| Topic | Topic name |
| Subtopic | Subtopic name (if showing at subtopic level) |
| Published | COUNT of published questions |
| In Pipeline | COUNT in UNDER_REVIEW or PENDING_APPROVAL |
| Gap Severity | 🔴 Critical (< 3) · 🟠 Low (3–9) · 🟡 Developing (10–29) |
| Exam Types | Which exam types this topic is mapped to |
| "Assign SME" action | Pre-fills a D-10 quota adjustment for this subject+topic — Director navigates to D-10 with this topic highlighted |

**Filter:** Gap Severity (show only Critical / show Critical + Low / show all)

**Sort:** Default — Gap Severity (Critical first), then published count ascending.

---

### Section 6 — Exam Type Mapping Tab

**Purpose:** For each topic in the selected subject, define which exam types include it. This mapping drives D-14 coverage analysis — a topic not mapped to an exam type will not appear in that exam type's coverage report.

**Layout:** Topic list (left) + Exam Type checkboxes (right panel for selected topic).

Per selected topic:
- 8 exam type checkboxes (SSC CGL · SSC CHSL · RRB NTPC · RRB Group D · AP Board · TS Board · UPSC Prelims · Online)
- "Save Mapping" — updates `content_taxonomy_topic_exam_mapping` table + invalidates D-14 coverage cache

**Bulk mapping:** "Apply to all subtopics" checkbox — when saving a topic's mapping, apply the same mapping to all its subtopics (saves time when all subtopics share the same exam type inclusion as their parent topic).

---

### Section 7 — Style Guide Tab

**Purpose:** Per-subject quality standards — the authoring contract between the Content Director and SMEs. What constitutes Easy/Medium/Hard in this subject? What formatting rules apply? What are common mistake patterns?

**Content:** Per-subject rich text document (bold, italic, tables, ordered lists, code blocks for CS subject).

**Standard sections (template for each subject):**
1. Difficulty Calibration Rubric — specific criteria for Easy / Medium / Hard with examples
2. Formatting Conventions — LaTeX standards, image quality requirements, code block rules (CS), molecular formula notation (Chemistry)
3. Bloom's Taxonomy Application — how Bloom's levels map to this subject's question types
4. Common Mistake Patterns — recurring errors seen in returned questions (maintained by Director as returns accumulate)
5. Exam-Specific Requirements — special formatting or scope notes per exam type (e.g. "UPSC Prelims: avoid direct recall questions — always apply/analyse level")
6. Example Questions — 2–3 example questions at each difficulty level showing what "good" looks like for this subject
7. Telugu Script Standards (Regional Language subject only) — Unicode block requirements, common transliteration errors

**Access:**
- Content Director: edit mode (rich text editor with autosave)
- All other Div D roles: read-only rendered view (same content, no edit controls)

**Version history:** Each save creates a `content_style_guide_version` record. Director can view and restore previous versions. The current version is displayed at the top of the tab: "Style Guide v7 — Last updated: 15 March 2026 by Content Director."

---

## 5. Data Models

### `content_taxonomy_subject`
| Field | Type | Notes |
|---|---|---|
| `id` | int | Small fixed set (9 rows) |
| `name` | varchar | Mathematics · Physics · etc. |
| `code` | varchar | MATH · PHYS · CHEM · etc. |

### `content_taxonomy_topic`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `subject_id` | FK → content_taxonomy_subject | — |
| `code` | varchar | e.g. MATH_001 — auto-generated |
| `name` | varchar | — |
| `description` | text | Nullable |
| `syllabus_reference` | varchar | Nullable |
| `active` | boolean | Default true — archived = false |
| `created_at` | timestamptz | — |

### `content_taxonomy_subtopic`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `topic_id` | FK → content_taxonomy_topic | — |
| `code` | varchar | e.g. MATH_001_01 |
| `name` | varchar | — |
| `description` | text | Nullable |
| `syllabus_reference` | varchar | Nullable |
| `active` | boolean | Default true |

### `content_taxonomy_topic_exam_mapping`
| Field | Type | Notes |
|---|---|---|
| `topic_id` | FK → content_taxonomy_topic | — |
| `exam_type_code` | varchar | SSC_CGL · RRB_NTPC · etc. |

### `content_style_guide`
| Field | Type | Notes |
|---|---|---|
| `subject_id` | FK → content_taxonomy_subject | One per subject |
| `content` | text | Rich text HTML — current version |
| `version` | int | Incremented on each save |
| `updated_by` | FK → auth.User | Director |
| `updated_at` | timestamptz | — |

### `content_style_guide_versions` (version history)
| Field | Type | Notes |
|---|---|---|
| `subject_id` | FK → content_taxonomy_subject | — |
| `version` | int | — |
| `content` | text | Snapshot of this version |
| `created_by` | FK → auth.User | — |
| `created_at` | timestamptz | — |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.view_taxonomy')` — all Div D roles |
| Edit access | `permission='content.edit_taxonomy'` — Role 18 only |
| Bulk Retag trigger | Roles 18 + 29 — checked server-side on the Celery task dispatch endpoint |
| Style Guide edit | Role 18 only — other roles get read-only rendered view |
| Archive action | Role 18 only — with Bulk Retag enforcement (archive button disabled until retag completes) |

---

## 7. Cache Behaviour

Taxonomy tree data is the most frequently read data in the platform — every D-02 question authoring session, every D-06 notes structuring session, every D-07 import validation reads from the taxonomy.

**Cache strategy:** Memcached (django.core.cache) with 10-minute TTL per subject:
- Key: `taxonomy_tree_{subject_id}` — full annotated tree with published question counts
- `cache.delete(f'taxonomy_tree_{subject_id}')` is called on every node create, edit, archive, or bulk retag completion
- On cache miss: ORM query fetches full tree with `prefetch_related` + `annotate(published_count=...)` — < 200ms for a subject with 300 topics + 1,500 subtopics

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Archive node during active bulk retag | Archive button disabled ("Retag in progress — {N} / {total} complete") until the retag job completes |
| Bulk retag fails mid-execution (DB error) | Celery task catches the exception, marks `content_taxonomy_retag_job.status = 'Failed'`. Partial updates: some questions may have been retagged before the failure — the job records the `completed_questions` count. Director must investigate and re-trigger the retag for the remaining questions or restore the partially retagged questions via D-12 (if the target node was wrong). |
| Topic deleted on Div B side (exam pattern) | Div B reads taxonomy via shared DB — archiving a topic that Div B's exam patterns reference is blocked with: "This topic is referenced in {N} exam pattern configurations in Div B. Remove it from those patterns before archiving." |
| Style guide update while multiple SMEs have D-02 open | D-02 loads style guide tooltip content at page load. SMEs currently editing see the old version until they reload D-02. On next D-02 page load: fresh style guide content from Memcached. Acceptable for style guide — not real-time critical. |
| Two Directors edit the same taxonomy node simultaneously | Last-write-wins on the `name` / `description` fields (low-risk conflict). The audit log shows both saves. No optimistic locking for taxonomy node edits — the risk of harmful overwrites is low given only 1 Director role. |
| SME tries to tag a question to an archived topic | D-02 dropdown only shows Active topics — Archived topics are excluded from the cascade query. If a question was already tagged to a topic that is subsequently archived: the tag remains valid in the DB but the topic shows as "[Archived] Algebra — Basic" in D-01's My Questions table until the Director bulk-retags those questions. |

---

## 9. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-02 Question Editor | D-09 → D-02 | Subject/Topic/Subtopic dropdown data | ORM with Memcached 10-min cache — `taxonomy_tree_{subject_id}` |
| D-06 Notes Management | D-09 → D-06 | Subject/Topic/Subtopic dropdown for notes structuring | Same Memcached cache |
| D-07 Bulk Import | D-09 → D-07 | Topic code validation in CSV import | Direct ORM lookup — `content_taxonomy_topic.code` |
| D-14 Syllabus Coverage | D-09 → D-14 | Topic hierarchy + exam type mappings for coverage analysis | Shared DB tables read by D-14 |
| Div B Syllabus Builder (B-10) | B-10 reads | Official exam syllabus structures reference D-09 | Shared `content_taxonomy_topic` table |
| D-12 Audit History | D-09 → D-12 | Bulk Retag events logged per question | INSERT into `content_question_audit_log` with `action: TaxonomyRetag` |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- **Tree panel:** Search bar above the tree. Placeholder: "Search topics and subtopics…". Searches: node name, official syllabus reference code. Debounced 300ms. Matching nodes highlighted yellow inline within the tree — non-matching nodes collapsed but not hidden (show parent context). "Clear search" ✕ restores full tree.
- **Gap View tab:** Placeholder "Filter topics by subject or gap threshold…". Subject filter dropdown + gap severity filter (All / Critical < 3 / Low < 10).

### Sortable Columns — Gap View Table
| Column | Default Sort |
|---|---|
| Published Count | **ASC (fewest first)** — default (most urgent gaps first) |
| Subject | ASC |
| Topic | ASC |
| Gap Severity | Custom: Critical → Low |

### Pagination
- Tree panel: not paginated (tree structure, all nodes visible via collapse/expand).
- Gap View table: 50 rows, numbered controls.
- Exam Type Mapping table: typically < 20 topics shown per selection — no pagination.
- Style Guide tab: single document, no pagination.

### Empty States
| Section | Heading | Subtext |
|---|---|---|
| Tree — new subject, no topics | "No topics yet" | "Add the first topic for this subject using the '+' button above." |
| Gap View — no gaps | "No coverage gaps" | "All active topics meet the minimum question threshold." |
| Style Guide — not written yet | "No style guide yet" | "The Content Director hasn't written a style guide for this subject yet." |

### Toast Messages
| Action | Toast |
|---|---|
| Node created | ✅ "Topic created" / "Subtopic created" (Success 4s) |
| Node saved (edit) | ✅ "Changes saved" (Success 4s) |
| Node archived | ✅ "Topic archived" (Success 4s). If questions exist: ⚠ "Cannot archive — retag questions first" (Warning persistent) |
| Bulk Retag started (G10) | ℹ "Retagging {N} questions — you can navigate away and return" (Info 6s) |
| Bulk Retag complete (G10) | ✅ "Retag complete — {N} questions retagged. Topic archived." (Success 4s — via HTMX push) |
| Bulk Retag failed | ❌ "Retag failed at row {N} — {reason}. Questions remain on original topic." (Error persistent) |
| Style guide saved | ✅ "Style guide saved" (Success 4s) |
| Memcached invalidated | No user-visible toast — internal event |

### Loading States
- Tree panel: full tree skeleton (indented shimmer lines, 3 levels) on initial load. Subject switch: tree skeleton replaces current tree instantly.
- Edit panel: 4-field skeleton (shimmer rectangles) while node data loads after click.
- Gap View table: 8-row skeleton on tab open and filter apply.
- Bulk Retag progress: HTMX progress bar inside the retag confirmation panel. "Retagging {N} of {total}…" polled every 2s. Completes with green "✓ Retag complete — archiving topic now."

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | 35% tree panel + 65% edit panel, side-by-side. |
| Tablet | Tree panel collapses to a "Browse Topics" button → opens as 70% left overlay. Edit panel takes full width when tree is closed. |
| Mobile | Tree panel is a full-screen sheet (tap topic → closes sheet, loads edit panel). Edit panel full width. Gap View table: node name + gap count + action — horizontal scroll for other columns. |

### Charts
- **Gap View tab:** Horizontal bar chart per topic — Published Count (filled red/amber/green by threshold) vs Target (outline). Sorted by gap. Click any bar to navigate tree to that topic.
- **Exam Type Mapping tab:** Heatmap grid — Topics × Exam Types. Cell filled = topic is included in that exam type. Click cell to toggle. Colour: filled = included, empty = excluded.

### Role-Based UI
- **Add node / Edit node / Archive node:** Content Director (18) only. SMEs and Reviewers see tree as read-only. Edit panel shows fields as read-only text for non-Director roles.
- **Style Guide edit:** Director only. Read-only for all other roles.
- **Bulk Retag trigger:** Director and Approver. SMEs cannot trigger retag.
- **Exam Type Mapping toggle:** Director only. Other roles see read-only mapping.

---

*Page spec complete.*
*Amendments applied: G10 (Bulk Retag action — Celery async bulk question retag before archive + full audit trail per question)*
*Gap amendments: Gap 6 (Exam Type management — reference link to D-20 Exam Types tab in page header; Deprecated exam type handling in Exam Type Mapping tab) · Gap 7 (Subject management — reference link to D-20 Subjects tab in page header; Archived subject behaviour in subject selector)*
*Next file: `d-10-calendar.md`*
