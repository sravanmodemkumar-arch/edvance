# D-20 — Content Configuration

> **Route:** `/content/director/config/`
> **Division:** D — Content & Academics
> **Roles:** Content Director (18) only — all other roles receive 403
> **File:** `d-20-config.md`
> **Priority:** P2 — Required before exam type / subject codes are created; unlocks D-08/D-09 taxonomy management
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Content Configuration
**Route:** `/content/director/config/`
**Part-load routes:**
- `/content/director/config/?part=exam-type-list` — exam type table (HTMX into tab body)
- `/content/director/config/?part=subject-list` — subject table (HTMX into tab body)
- `/content/director/config/?part=ai-thresholds` — AI triage threshold form (HTMX into tab body)
- `/content/director/config/?part=reviewer-targets` — reviewer performance target form (HTMX into tab body)

---

## 2. Purpose (Business Objective)

Division D's entire taxonomy rests on two reference tables: **Exam Types** and **Subjects**. Without a UI to manage these, the Director must request database changes from engineering — creating bottlenecks every time a new exam or subject is added, or a deprecated code needs to be retired.

D-20 centralises all platform-wide configuration decisions that only the Content Director should make:
- Creating and deprecating exam type codes (used across D-02, D-07, D-09, D-11, D-12)
- Creating and archiving subject codes (used as the primary taxonomy axis in all content pages)
- Setting AI triage thresholds that govern D-08 auto-rejection and D-08 similarity scoring
- Setting reviewer performance targets referenced in D-13 and D-15

**Business goals:**
- Allow Content Director to onboard new competitive exams in minutes, not days
- Enforce safe deprecation — prevent deletion of codes still in use by published questions
- Give Director visibility and control over AI-assisted quality thresholds without engineering involvement
- Define SLA/accuracy targets per reviewer so D-13 shows meaningful benchmarks

---

## 3. Page Layout

**Tab bar (sticky below page header):**

| Tab # | Label | Route anchor |
|---|---|---|
| 1 | Exam Types | `#exam-types` |
| 2 | Subjects | `#subjects` |
| 3 | AI Triage Thresholds | `#ai-thresholds` |
| 4 | Reviewer Performance Targets | `#reviewer-targets` |

Active tab highlighted. HTMX swaps tab body on click.

**Page header:**
- H1: "Content Configuration"
- Breadcrumb: Dashboard → Content Configuration
- Last-modified timestamp: "Last updated {date} by Content Director" (shown below H1, greyed)

---

## 4. Section-Wise Detailed Breakdown

---

### Tab 1 — Exam Type Manager

**Route anchor:** `#exam-types`

#### 4.1.1 Exam Type Table

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Code | ✅ | Short code (e.g. `UPSC`, `JEE`, `NEET`). Unique. Immutable after creation. |
| Display Name | ✅ | Full name shown in UI dropdowns and exports |
| Category | ✅ | Civil Services · Engineering · Medical · Law · Banking · State PSC · Other |
| Question Count | ✅ | Count of `content_question` rows with this exam type (any status) |
| Published Count | — | Count of `PUBLISHED` questions only |
| Status | ✅ | Active · Deprecated |
| Created | ✅ | Date created |
| Actions | — | Edit · Deprecate/Reactivate |

**Default sort:** Display Name ASC.
**Pagination:** 25 rows per page, numbered controls.
**Search:** Inline search on Code + Display Name. Debounced 300ms.
**Filter:** Status filter (Active / Deprecated / All). Default: Active.

---

#### 4.1.2 Create Exam Type — Drawer

**Trigger:** "+ New Exam Type" button (top-right of tab).
**Drawer width:** 480px (mobile: full-screen bottom sheet).

**Form fields:**

| Field | Type | Validation |
|---|---|---|
| Code | Text input | Required. Max 20 chars. Uppercase enforced. Pattern: `[A-Z0-9_]+`. Unique — real-time availability check (HTMX debounce 500ms). |
| Display Name | Text input | Required. Max 100 chars. |
| Category | Select | Required. Options: Civil Services · Engineering · Medical · Law · Banking · State PSC · Other |
| Description | Textarea | Optional. Max 300 chars. Shown in D-09 taxonomy tooltips. |

**On save:**
- `content_exam_type` record created.
- Code is immutable from this point — shown greyed with "(immutable after creation)" hint on edit.
- D-09 taxonomy dropdowns refresh from `content_exam_type` (cache invalidated).
- Toast: ✅ "Exam type '{Code}' created" (Success 4s).

---

#### 4.1.3 Edit Exam Type — Drawer

**Trigger:** "Edit" row action.
**Same drawer, pre-filled.**

**Editable fields:** Display Name, Category, Description only.
**Code field:** Greyed, read-only. Tooltip: "Code cannot be changed after creation — it is used as a foreign key across the question bank."

**On save:**
- `content_exam_type` record updated.
- Toast: ✅ "Exam type '{Code}' updated" (Success 4s).

---

#### 4.1.4 Deprecate Exam Type

**Trigger:** "Deprecate" row action (shown for Active exam types).

**Guard check (server-side before showing confirmation modal):**
- If `Question Count > 0` and any question is in `DRAFT`, `UNDER_REVIEW`, or `AMENDMENT_REVIEW` state → **Block deprecation**.
  - Modal: "Cannot deprecate — {N} questions are in active workflow states (Draft, Under Review, Amendment Review). Resolve these questions before deprecating this exam type."
  - Actions: "View Active Questions" (→ D-11 filtered to this exam type + active states) · "Cancel".
- If all questions are `PUBLISHED`, `ARCHIVED`, or `REJECTED` → **Allow with warning**.
  - Confirmation modal: "Deprecate '{Display Name}'? This exam type will be hidden from all new question creation dropdowns. Existing {N} published questions will be unaffected. This action can be reversed by reactivating."
  - Actions: "Confirm Deprecate" · "Cancel".

**On confirm:**
- `content_exam_type.status` set to `Deprecated`.
- Exam type removed from all creation/filter dropdowns in D-02, D-07, D-09.
- Still visible in D-11 Bank and D-12 Version History as a read-only label.
- Toast: ⚠️ "Exam type '{Code}' deprecated — new question creation for this type is disabled" (Warning 8s).

---

#### 4.1.5 Reactivate Exam Type

**Trigger:** "Reactivate" row action (shown for Deprecated exam types).
**No guard check required.**
**Confirmation modal:** "Reactivate '{Display Name}'? It will reappear in all exam type dropdowns."
**On confirm:** Status → Active. Toast: ✅ "Exam type '{Code}' reactivated" (Success 4s).

---

### Tab 2 — Subject Manager

**Route anchor:** `#subjects`

#### 4.2.1 Subject Table

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Code | ✅ | Short code (e.g. `GK`, `MATH`, `CHEM`). Unique. Immutable after creation. |
| Display Name | ✅ | Full subject name |
| Applicable Exam Types | — | Pills showing which exam types include this subject (many-to-many via `content_subject_exam_type`) |
| SME Count | — | Count of SME users whose profile includes this subject |
| Question Count | ✅ | Total questions for this subject (any status) |
| Published Count | — | Published questions only |
| Status | ✅ | Active · Archived |
| Created | ✅ | Date created |
| Actions | — | Edit · Archive/Restore |

**Default sort:** Display Name ASC.
**Pagination:** 25 rows per page.
**Search:** Code + Display Name. Debounced 300ms.
**Filter:** Status (Active / Archived / All). Default: Active.

---

#### 4.2.2 Create Subject — Drawer

**Drawer width:** 560px (mobile: full-screen).

**Form fields:**

| Field | Type | Validation |
|---|---|---|
| Code | Text input | Required. Max 20 chars. Uppercase. Pattern `[A-Z0-9_]+`. Unique — real-time check. |
| Display Name | Text input | Required. Max 100 chars. |
| Applicable Exam Types | Multi-select checkbox | Required — at least one. Lists all Active exam types. |
| Default Monthly Quota | Number input | Required. Min 1. Max 500. Default 10. Applied to new SMEs assigned to this subject. |
| Description | Textarea | Optional. Max 300 chars. |

**On save:**
- `content_subject` and `content_subject_exam_type` junction records created.
- D-09 taxonomy tree rebuilt (cache invalidated).
- Toast: ✅ "Subject '{Code}' created" (Success 4s).

---

#### 4.2.3 Edit Subject — Drawer

**Trigger:** "Edit" row action.
**Editable:** Display Name, Applicable Exam Types, Default Monthly Quota, Description.
**Code:** Read-only (immutable).

**On exam type removal:** If removing an exam type that has published questions in this subject:
- Inline warning below the checkbox: "{N} published questions exist for {ExamType} + {Subject}. Removing this link does not affect existing questions — only new question creation."
- Allow removal — no hard block.

**On save:** Toast: ✅ "Subject '{Code}' updated" (Success 4s).

---

#### 4.2.4 Archive Subject

**Same guard logic as Exam Type deprecation.** Active workflow states block archival. Published-only allows archival with warning.

**On archive:**
- Subject removed from creation dropdowns.
- Existing SME-subject assignments retained (SME can still edit DRAFT questions for archived subjects).
- Toast: ⚠️ "Subject '{Code}' archived — new assignments for this subject are disabled" (Warning 8s).

---

### Tab 3 — AI Triage Thresholds

**Route anchor:** `#ai-thresholds`

#### 4.3.1 Purpose

D-08 (AI Triage) uses two configurable threshold sets:
1. **Auto-rejection thresholds** — If AI confidence that a question is low quality exceeds this %, the question is auto-rejected without human review.
2. **Similarity threshold** — If cosine similarity between a new question and an existing published question exceeds this %, the question is flagged as a potential duplicate in D-08.

These thresholds are currently hardcoded. D-20 Tab 3 allows the Director to tune them based on observed false-positive/negative rates.

---

#### 4.3.2 Threshold Form

**Layout:** Single column form, grouped by threshold category.

**Group 1 — Auto-Rejection Thresholds:**

| Field | Type | Default | Validation | Description |
|---|---|---|---|---|
| Language Quality — Auto-Reject % | Number (slider + input) | 85 | Min 50, Max 99 | If AI language quality score < (100 − this %) → auto-reject |
| Factual Accuracy — Auto-Reject % | Number (slider + input) | 90 | Min 50, Max 99 | If AI factual confidence score < (100 − this %) → auto-reject |
| Formatting Compliance — Auto-Reject % | Number (slider + input) | 95 | Min 50, Max 99 | If AI formatting compliance score < (100 − this %) → auto-reject |
| Bloom's Level Mismatch — Auto-Reject % | Number (slider + input) | 80 | Min 50, Max 99 | If AI Bloom's level confidence < (100 − this %) → auto-reject |

**Group 2 — Similarity / Duplicate Detection:**

| Field | Type | Default | Validation | Description |
|---|---|---|---|---|
| Duplicate Flag Threshold (cosine similarity) | Number (slider + input) | 0.85 | Min 0.50, Max 0.99, step 0.01 | Questions with cosine similarity ≥ this value are flagged as potential duplicates in D-08 |
| High-Confidence Duplicate Threshold | Number (slider + input) | 0.95 | Min 0.80, Max 0.99, step 0.01 | Questions with cosine similarity ≥ this value are treated as confirmed duplicates (auto-rejected) |

**Group 3 — Committee Review Trigger:**

| Field | Type | Default | Validation | Description |
|---|---|---|---|---|
| Reviewer Disagreement → Committee Review | Checkbox | ✅ ON | — | If Reviewer 1 and Reviewer 2 verdicts conflict, escalate to Committee Review (D-15 config) |
| Committee Review: Min Flags to Trigger | Number input | 3 | Min 1, Max 10 | Number of student feedback flags that also triggers committee review (in addition to D-16) |

**Impact preview (read-only, below form):**

> Based on current thresholds: **Last 30 days — {N} questions auto-rejected** · **{M} flagged as duplicates** · **{K} sent to committee review**

HTMX updates this preview whenever a threshold slider changes (debounced 1s). Uses aggregate counts from `content_ai_triage_log`.

**Save button:** "Save Threshold Configuration"
**Reset button:** "Reset to Defaults" — resets all fields to default values (confirmation modal: "Reset all thresholds to factory defaults?").

**On save:**
- `content_ai_threshold_config` record updated (single row — upsert).
- `updated_at` and `updated_by` stamped.
- D-08 triage pipeline uses new thresholds on next run (no restart needed — read at task execution time).
- Toast: ✅ "AI thresholds saved — new questions will be evaluated against updated thresholds" (Success 4s).

**Audit:** Every save appends to `content_ai_threshold_audit_log` with before/after values and director user ID.

---

#### 4.3.3 Threshold Change History

**Collapsed section below the form** (expandable toggle): "View Change History"

**Table:** Last 20 threshold changes.

| Column | Notes |
|---|---|
| Changed At | Timestamp |
| Changed By | Role label ("Content Director") — not name (DPDPA) |
| Field Changed | Which threshold |
| Old Value | Previous value |
| New Value | New value |

---

### Tab 4 — Reviewer Performance Targets

**Route anchor:** `#reviewer-targets`

#### 4.4.1 Purpose

D-13 (Reviewer Performance Calibration) shows reviewer metrics vs. benchmarks. Those benchmarks come from D-20 Tab 4. Without configuring them, D-13 shows metrics with no reference line — making the data unactionable.

---

#### 4.4.2 Global Targets Form

**Group 1 — Throughput Targets:**

| Field | Type | Default | Validation |
|---|---|---|---|
| Minimum Reviews per Month | Number input | 30 | Min 1, Max 500 |
| Target Reviews per Month | Number input | 50 | Min 1, Max 500 — must be ≥ Minimum |
| Maximum Reviews per Month (burnout guard) | Number input | 100 | Min 1, Max 500 — must be ≥ Target |

**Group 2 — Quality Targets:**

| Field | Type | Default | Validation |
|---|---|---|---|
| Target Accuracy Rate (%) | Number input | 90 | Min 50, Max 100 |
| Minimum Accuracy Rate (%) | Number input | 75 | Min 50, Max 100 — must be ≤ Target |
| Target Inter-Reviewer Agreement Rate (%) | Number input | 80 | Min 50, Max 100 |
| Escalation Rate Ceiling (%) | Number input | 10 | Min 1, Max 50 — if reviewer escalates > this % of questions, flag in D-13 |

**Group 3 — SLA Targets:**

| Field | Type | Default | Validation |
|---|---|---|---|
| Standard Review SLA (hours) | Number input | 48 | Min 1, Max 168 |
| Priority Review SLA (hours) | Number input | 24 | Min 1, Max 48 — must be ≤ Standard |
| Amendment Review SLA (hours) | Number input | 12 | Min 1, Max 24 — must be ≤ Priority |
| Committee Review SLA (hours) | Number input | 72 | Min 1, Max 168 |

**Save button:** "Save Performance Targets"

**On save:**
- `content_reviewer_performance_target` record updated (single row — upsert).
- D-13 calibration charts immediately reference new values on next page load (no cache needed — read at render time).
- Toast: ✅ "Performance targets saved — D-13 Calibration will reflect updated benchmarks" (Success 4s).

---

#### 4.4.3 Per-Reviewer Overrides (Advanced)

**Expandable section:** "Per-Reviewer Target Overrides" (collapsed by default).

**Purpose:** Some reviewers may handle specialist subjects (rare exam types) where global throughput targets are inappropriate.

**Override table:**

| Column | Notes |
|---|---|
| Reviewer | Role label (e.g. "Reviewer — GK") — no personal name |
| Subject Override | Which subject this override applies to |
| Min Reviews / Month | Override value — blank = use global |
| Target Reviews / Month | Override value |
| Max Reviews / Month | Override value |
| Target Accuracy (%) | Override value |
| Actions | Edit · Clear Override |

**"+ Add Override" button:** Opens drawer with Reviewer selector (role-label dropdown), Subject selector, and the 4 override fields (all optional — blank means inherit global).

**On save override:** Toast: ✅ "Override saved for {ReviewerLabel} — {Subject}" (Success 4s).
**On clear override:** Confirmation modal "Remove override for {ReviewerLabel}? They will revert to global targets." → Toast: ✅ "Override cleared" (Success 4s).

---

## 5. Data Models

### `content_exam_type`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `code` | varchar(20) | Unique. Immutable after creation. |
| `display_name` | varchar(100) | — |
| `category` | varchar(30) | Enum: CivilServices · Engineering · Medical · Law · Banking · StatePSC · Other |
| `description` | text | Nullable |
| `status` | varchar(12) | Active · Deprecated |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |

### `content_subject`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `code` | varchar(20) | Unique. Immutable. |
| `display_name` | varchar(100) | — |
| `default_monthly_quota` | integer | Default for new SME assignments |
| `description` | text | Nullable |
| `status` | varchar(10) | Active · Archived |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |

### `content_subject_exam_type`
| Field | Type | Notes |
|---|---|---|
| `subject_id` | FK → content_subject | — |
| `exam_type_id` | FK → content_exam_type | — |
| Primary key: `(subject_id, exam_type_id)` | — | — |

### `content_ai_threshold_config`
| Field | Type | Notes |
|---|---|---|
| `id` | integer | Always 1 — single-row config |
| `language_quality_reject_pct` | integer | Default 85 |
| `factual_accuracy_reject_pct` | integer | Default 90 |
| `formatting_compliance_reject_pct` | integer | Default 95 |
| `blooms_mismatch_reject_pct` | integer | Default 80 |
| `duplicate_flag_threshold` | numeric(4,2) | Default 0.85 |
| `duplicate_confirmed_threshold` | numeric(4,2) | Default 0.95 |
| `committee_on_disagreement` | boolean | Default True |
| `committee_flag_trigger_count` | integer | Default 3 |
| `updated_at` | timestamptz | — |
| `updated_by` | FK → auth.User | — |

### `content_ai_threshold_audit_log`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `changed_at` | timestamptz | — |
| `changed_by` | FK → auth.User | — |
| `field_name` | varchar(60) | Which threshold changed |
| `old_value` | varchar(20) | Serialised previous value |
| `new_value` | varchar(20) | Serialised new value |

### `content_reviewer_performance_target`
| Field | Type | Notes |
|---|---|---|
| `id` | integer | Always 1 — single-row global config |
| `min_reviews_per_month` | integer | Default 30 |
| `target_reviews_per_month` | integer | Default 50 |
| `max_reviews_per_month` | integer | Default 100 |
| `target_accuracy_pct` | integer | Default 90 |
| `min_accuracy_pct` | integer | Default 75 |
| `target_agreement_pct` | integer | Default 80 |
| `escalation_rate_ceiling_pct` | integer | Default 10 |
| `standard_sla_hours` | integer | Default 48 |
| `priority_sla_hours` | integer | Default 24 |
| `amendment_sla_hours` | integer | Default 12 |
| `committee_sla_hours` | integer | Default 72 |
| `updated_at` | timestamptz | — |
| `updated_by` | FK → auth.User | — |

### `content_reviewer_target_override`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `reviewer_user_id` | FK → auth.User | — |
| `subject_id` | FK → content_subject | — |
| `min_reviews_per_month` | integer | Nullable — null = use global |
| `target_reviews_per_month` | integer | Nullable |
| `max_reviews_per_month` | integer | Nullable |
| `target_accuracy_pct` | integer | Nullable |
| Unique: `(reviewer_user_id, subject_id)` | — | One override per reviewer per subject |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | Content Director (Role 18) only. All other authenticated roles → 403 with message: "This page is restricted to Content Directors." |
| Exam Type create/edit/deprecate | Content Director only. No self-service for SMEs or Reviewers. |
| Subject create/edit/archive | Content Director only. |
| AI threshold config | Content Director only. Changes logged with director identity. |
| Performance targets | Content Director only. |
| Per-reviewer overrides | Content Director only. Reviewer identity never exposed — role label only. |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Exam Type code already exists | Real-time HTMX check shows inline error: "Code '{code}' is already taken — choose a unique code." Save button disabled until resolved. |
| Subject has SME assignments when archived | Warning (not block): "Archiving this subject will not remove {N} existing SME assignments. Those SMEs can still complete in-progress DRAFT questions. No new assignments will be made." |
| Auto-reject threshold set too high (> 95%) | Inline warning below slider: "At this threshold, the AI will auto-reject almost no questions. Human reviewers will receive maximum volume." No hard block. |
| Similarity threshold: confirmed > flag | Inline validation error: "Confirmed duplicate threshold must be ≥ Flag threshold." Save blocked. |
| Performance target: min > target | Inline error: "Minimum must be ≤ Target." Save blocked. |
| Performance target: target > max | Inline error: "Target must be ≤ Maximum." Save blocked. |
| D-09 retag job running when exam type deprecated | Guard check: if a bulk retag Celery task is actively running for this exam type → block deprecation with: "A bulk retag job is currently running for this exam type. Wait for it to complete before deprecating." |
| Director deletes own role | Not possible via this page. User management is out of scope for Div D. |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-02 Question Editor | D-20 → D-02 | Exam Type + Subject dropdowns populated from `content_exam_type` + `content_subject` | ORM query at page load; Memcached 10-min TTL |
| D-07 Bulk Import | D-20 → D-07 | Exam Type + Subject validation against `content_exam_type` + `content_subject` | Import validator reads active codes only |
| D-08 AI Triage | D-20 → D-08 | Auto-reject and similarity thresholds read from `content_ai_threshold_config` | Read at Celery task execution time (no cache) |
| D-09 Taxonomy | D-20 → D-09 | Exam Type + Subject tree sourced from `content_exam_type` + `content_subject` | Taxonomy tree cache invalidated on D-20 save |
| D-11 Question Bank | D-20 → D-11 | Exam Type filter options reflect active + deprecated types (deprecated shown with strikethrough label) | ORM query at filter load |
| D-13 Reviewer Calibration | D-20 → D-13 | Performance benchmarks for charts sourced from `content_reviewer_performance_target` + overrides | Read at render time |
| D-15 Reviewer Assignments | D-20 → D-15 | SLA config values referenced in SLA Config tab (D-15 reads `content_reviewer_performance_target.standard_sla_hours` as default) | Read at render time |

---

## 9. UI Patterns & Page-Specific Interactions

### Tab Navigation
- Active tab: bold text + 2px bottom border (brand blue).
- Tab change: HTMX `hx-get` with `?part=` URL. No full page reload.
- Browser back/forward works: URL hash updated (`#exam-types`, `#subjects`, etc.).

### Slider + Number Input (AI Thresholds)
- Slider and number input are linked: changing either updates the other in real-time.
- Range guardrails enforced on both sides — cannot slide past min/max.
- Impact preview updates 1s after any threshold change (Celery aggregate query).

### Immutable Code Fields
- Code inputs: show "(cannot be changed after creation)" hint text below field.
- On Edit drawer: Code field rendered as `<span>` (not `<input>`) with grey background — visually distinct from editable fields.

### Sortable Columns
- Code ASC/DESC, Display Name ASC/DESC, Question Count ASC/DESC, Status ASC/DESC.
- Sort state in URL: `?sort=code&dir=asc`.

### Search
- Searches Code + Display Name.
- Debounced 300ms. Clears to page 1 on new search.
- "X" clear button appears when search has value.

### Empty States
| State | Heading | Subtext |
|---|---|---|
| No exam types | "No exam types configured" | "Create your first exam type to begin building the question taxonomy." |
| No subjects | "No subjects configured" | "Create your first subject to enable question authoring." |
| No reviewer overrides | "No per-reviewer overrides" | "All reviewers use global targets. Add an override for reviewers with specialist subjects." |
| Search returns zero | "No matches found" | "Try a different code or name." |

### Toast Messages
| Action | Toast |
|---|---|
| Create exam type | ✅ "Exam type '{Code}' created" (Success 4s) |
| Edit exam type | ✅ "Exam type '{Code}' updated" (Success 4s) |
| Deprecate exam type | ⚠️ "Exam type '{Code}' deprecated" (Warning 8s) |
| Reactivate exam type | ✅ "Exam type '{Code}' reactivated" (Success 4s) |
| Create subject | ✅ "Subject '{Code}' created" (Success 4s) |
| Edit subject | ✅ "Subject '{Code}' updated" (Success 4s) |
| Archive subject | ⚠️ "Subject '{Code}' archived" (Warning 8s) |
| Save AI thresholds | ✅ "AI thresholds saved — new questions will be evaluated against updated thresholds" (Success 4s) |
| Reset AI thresholds to defaults | ✅ "Thresholds reset to factory defaults" (Success 4s) |
| Save performance targets | ✅ "Performance targets saved" (Success 4s) |
| Save reviewer override | ✅ "Override saved for {ReviewerLabel} — {Subject}" (Success 4s) |
| Clear reviewer override | ✅ "Override cleared — reviewer reverts to global targets" (Success 4s) |
| Deprecation blocked (active questions) | ❌ Error modal (not toast) — see Section 4.1.4 |

### Loading States
- Table: 5-row skeleton (shimmer rows).
- Form: Field skeletons (grey rectangles matching input widths).
- Impact preview: "Calculating…" spinner text during HTMX refresh.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full-width table. Form: two-column grid for threshold groups. |
| Tablet (768–1279px) | Table: hide Description and Created columns. Form: single column. |
| Mobile (<768px) | Table: show Code + Display Name + Status + Actions only. Drawer: full-screen bottom sheet. Tab bar: scrollable horizontal. |

### Role-Based UI
- Entire page is Director-only. Any non-Director hitting this route sees a full-page 403 message: "Access Restricted — Content Configuration is only available to Content Directors."
- No partial hiding — the entire page is blocked, not just individual elements.

---

*Page spec complete.*
*This page resolves: Critical Gap 6 (Exam Type Management UI) · Critical Gap 7 (Subject Management UI) · Important Gap 12 (AI Triage Threshold Config) · Important Gap 13 (Reviewer Performance Targets)*
