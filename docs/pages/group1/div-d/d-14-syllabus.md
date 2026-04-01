# D-14 — Exam Type & Syllabus Coverage

> **Route:** `/content/director/syllabus/`
> **Division:** D — Content & Academics
> **Primary Role:** Content Director (18) — full access including exam date config and syllabus change management
> **Read Access:** SME ×9 (19–27) — own subject view only
> **File:** `d-14-syllabus.md`
> **Priority:** P2 — Needed before first exam series configured by Div F
> **Status:** ⬜ Not started
> **Amendments:** G5 (Content Freshness tab — GK question expiry tracking) · G12 (Pool Adequacy tab — concurrent exam demand vs published pool depth)

---

## 1. Page Name & Route

**Page Name:** Exam Type & Syllabus Coverage
**Route:** `/content/director/syllabus/`
**Part-load routes:**
- `/content/director/syllabus/?part=coverage-tree&exam_type={code}&subject_id={id}` — coverage tree for selected exam + subject
- `/content/director/syllabus/?part=difficulty-distribution&exam_type={code}&subject_id={id}` — difficulty distribution bars
- `/content/director/syllabus/?part=access-level-distribution&exam_type={code}` — access level breakdown
- `/content/director/syllabus/?part=freshness-tab&exam_type={code}` — content freshness data (G5)
- `/content/director/syllabus/?part=pool-adequacy&exam_type={code}` — pool adequacy analysis (G12)

---

## 2. Purpose (Business Objective)

D-14 answers the Director's core production questions: "Do we have enough published questions to run a balanced exam for SSC CGL Mathematics? Do our GK Current Affairs questions have a healthy shelf life? Is our Coaching Only content deep enough, or are coaching centres getting the same questions repeatedly?"

At 8 exam types × 9 subjects × multiple difficulty levels × 4 access tiers × 2,050 tenant institutions × 74,000 peak concurrent exam submissions — the question "do we have enough questions?" is not a simple count. It requires understanding coverage relative to syllabus targets, difficulty distribution relative to exam-specific requirements, access level distribution relative to tenant composition, freshness relative to question expiry rates, and pool depth relative to concurrent exam demand (G12).

D-14 provides all five dimensions. Without this page, the Content Director is operating on intuition rather than data — and at this scale, intuition breaks down.

**Business goals:**
- Per exam type: show published question count vs target by topic, colour-coded
- Difficulty distribution: verify published questions match required exam-specific difficulty ratios
- Access Level distribution: ensure no exam type is disproportionately restricted
- Content Freshness: GK and Current Affairs question expiry tracking with bulk-archive capability (G5)
- Pool Adequacy: calculate whether the published pool is deep enough for concurrent exam demand without excessive question repetition (G12)
- Syllabus change management: Director marks topics as removed/added for next exam cycle

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full — all tabs, exam date config, syllabus change management, difficulty target editing, bulk archive |
| SME ×9 (19–27) | Read — own subject topics for their assigned exam types · coverage view only (no difficulty target editing, no access level view, no pool adequacy) |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Selectors

- H1: "Syllabus Coverage & Exam Analysis"
- **Exam Type selector (left panel, fixed):** SSC CGL · SSC CHSL · RRB NTPC · RRB Group D · AP State Board · TS State Board · UPSC Prelims · Online. One exam type active at a time.
- **Subject sub-filter (below exam type):** Filter the right panel to a specific subject within the selected exam type — "All Subjects" or one of the 9 subjects. SMEs see only their own subject.
- **Tabs (right panel content area):** Coverage · Difficulty Distribution · Access Level Distribution · Content Freshness · Pool Adequacy · Exam Date Config

---

### Section 2 — Tab: Coverage (Default)

**Purpose:** Syllabus topic tree for the selected exam type — published question count vs target per topic.

**Coverage Tree:**
3-level tree (Subject → Topic → Subtopic) for topics mapped to the selected exam type (from D-09 Exam Type Mapping).

Per topic/subtopic node:
- Published question count: bold number
- Target count (set by Director in this tab)
- Coverage % = (published / target) × 100%
- Coverage bar: horizontal progress bar — green ≥ 100% · amber 50–99% · red < 50%
- In-pipeline count (in parentheses): "(+12 in pipeline)" — gives the Director visibility that coverage is improving even before publish

**"Set Target" inline edit (Director only):**
Click the target count on any node → inline integer input → save. Updates `content_syllabus_target`. Target applies to this topic for this exam type combination.

**Coverage Summary (top of tab):**
"SSC CGL Mathematics: 47 of 63 mapped topics have ≥ target questions (74.6% adequate)."

**Gap Export:**
"Export Coverage Gaps" button → CSV download: exam type · subject · topic · subtopic · published count · target · gap · coverage %. Used for SME quota planning in D-10.

---

### Section 3 — Tab: Difficulty Distribution

**Purpose:** Verify the published question pool matches the required difficulty ratio for the selected exam type.

**Chart type:** Stacked bar chart — one bar per topic, divided into Easy / Medium / Hard published counts.

**Required ratio (editable by Director):**
Per exam type, the Director sets target ratios:
- SSC CGL Mathematics: 30% Easy / 50% Medium / 20% Hard
- UPSC Prelims GK: 10% Easy / 30% Medium / 60% Hard
- AP State Board Biology: 40% Easy / 40% Medium / 20% Hard

Ratio stored in `content_difficulty_target`. These targets are sourced from official exam analysis documents and the Director's content strategy.

**Visual:**
Each topic's stacked bar shows actual Easy/Medium/Hard ratios. Below each bar: ratio compliance indicator:
- ✅ Within 5% of target for each tier
- 🟡 5–15% deviation in any tier
- 🔴 > 15% deviation in any tier

**Deviation table (supplementary):**
Table view: Topic · Actual Easy% · Target Easy% · Deviation · Actual Medium% · Target Medium% · Deviation · Actual Hard% · Target Hard% · Deviation — sortable by any deviation column.

"Export Distribution Gap Report" → PDF automatically generated monthly on 1st of each month and emailed to Content Director. Also available on-demand.

---

### Section 4 — Tab: Access Level Distribution (Amendment G4)

**Purpose:** Ensure no exam type's question pool is accidentally over-restricted (e.g., 90% Coaching Only questions for SSC CGL would mean schools cannot run SSC CGL exams).

**Chart:** Per-subject, stacked pie chart or bar chart showing the distribution of published questions by access level:
- Platform-Wide: available to all 2,050 tenants
- School Only
- College Only
- Coaching Only

**Alert conditions:**
- If Platform-Wide questions < 50% for any subject in a school-tier exam type (AP Board, TS Board): Red alert — "Only {N}% of AP State Board Biology questions are Platform-Wide. School tenants may not have sufficient questions for exam construction."
- If Coaching Only questions > 30% for a non-coaching exam type: Amber alert — "30% of SSC CGL GK questions are Coaching Only. College tenants may have limited question pools for SSC CGL preparation."

**Director action:** These are informational alerts. The Director resolves them by either asking the Approver to change access levels on specific questions (D-11 / D-04 Access Level Change) or by ensuring new question submissions have the correct access level.

---

### Section 5 — Tab: Content Freshness (Amendment G5)

**Purpose:** Track the health of the Current Affairs and Time-Sensitive question pool for GK and other time-sensitive subjects.

**Freshness Overview:**
Three count tiles for the selected exam type:
- "Expiring in ≤ 30 days": red
- "Expiring in 31–90 days": amber
- "Expiring in 91–365 days": green
- "Already expired (archived)": grey (for reference)

**Freshness Table:**

| Column | Description |
|---|---|
| Topic | GK topic (Current Affairs · Polity · Economy · etc.) |
| Total Published | All published for this topic in this exam type |
| Expiring ≤ 30 days | COUNT |
| Expiring ≤ 90 days | COUNT |
| Net Fresh (> 90 days) | Published − Expiring ≤ 90 days — the "safe" pool |
| Target Fresh Questions | Configured by Director for this topic (minimum threshold) |
| Status | ✅ Adequate · 🟡 At Risk · 🔴 Critical |

**Bulk Archive Expired button:**
"Archive All Expired Questions" — archives all questions in this exam type past their `valid_until` date that the nightly Celery task has not yet processed. Same action as D-05 Expiry Monitor, but scoped to a specific exam type.

**Freshness trend chart:**
Per topic: line chart showing net fresh question count per month (last 12 months). A declining line means Current Affairs content is expiring faster than it is being replaced — Director can use this to adjust GK SME quotas in D-10.

**GK Director guidance note:**
A pinned note at the top of this tab (visible for the GK subject filter): "Current Affairs questions for competitive exams typically have a 6–12 month relevant window. Questions about Union Budget should be archived after the next budget is released. Questions about election results should be archived after the next election cycle."

---

### Section 6 — Tab: Pool Adequacy (Amendment G12)

**Purpose:** Determine whether the published question pool is deep enough to serve concurrent exam demand without excessive question repetition — the key operational readiness metric at 74,000 peak concurrent submissions.

**Background context:**
At 74,000 simultaneous exams, each exam selecting N questions from a given topic, the question pool must be deep enough that the same question does not appear in too many concurrent papers. If School A's student and Coaching Centre B's student happen to be taking the same exam simultaneously, and both get Question #1234, paper integrity is compromised.

**Pool Adequacy formula:**
```
Minimum Pool Required = Concurrent Exams × Questions Per Paper (for this topic) × Reuse Safety Factor
```
Where:
- **Concurrent Exams** = peak expected simultaneous exams for this exam type (from Div F's upcoming exam schedule)
- **Questions Per Paper (for this topic)** = configured in D-14 or read from Div F exam pattern (e.g. SSC CGL Math: 25 questions per paper)
- **Reuse Safety Factor** = default 3 (each question appears in at most 1-in-3 concurrent papers — configurable by Director)

**Example:**
SSC CGL Math at 500 simultaneous exams × 25 questions per paper × 3 = 37,500 minimum pool required. If only 8,000 Math questions published for SSC CGL: adequacy = 8,000 / 37,500 = 21.3% — critical.

**Pool Adequacy Table:**

| Column | Description |
|---|---|
| Subject | — |
| Topic | — |
| Published Pool | COUNT of published questions for this exam type + topic |
| Peak Concurrent Exams | From Div F API (upcoming exam schedule) |
| Questions Per Paper | From Div F exam pattern config |
| Safety Factor | Default 3 — Director can adjust per exam type |
| Minimum Pool Required | = Concurrent × Questions Per Paper × Safety Factor |
| Adequacy % | (Published Pool / Minimum Required) × 100% |
| Status | 🟢 ≥ 100% · 🟡 70–99% · 🔴 < 70% |

**Director actions per row:**
- "Assign SME to this topic" → pre-fills D-10 quota adjustment for this specific topic — opens D-10 with the topic highlighted and a suggested production target to reach 100% adequacy
- "Reduce Safety Factor" inline edit — Director can reduce the safety factor for a specific topic if the exam engine uses randomisation algorithms that provide sufficient diversity even with lower pool depth. Not recommended below 2.0.

**Adequacy Summary (top of tab):**
"SSC CGL Mathematics Pool Adequacy: 12 of 47 topics are fully adequate (> 100%). 23 topics are at risk (70–99%). 12 topics are critical (< 70%). Priority production targets auto-generated in D-05 Stale Alerts."

**Celery data refresh:**
Pool adequacy numbers depend on Div F's upcoming exam schedule (which is dynamic). Celery task `portal.tasks.content.refresh_pool_adequacy` runs nightly, reading from Div F's exam schedule API and updating `content_pool_adequacy_cache` table. Director can trigger a manual refresh with "Refresh Now" button (returns results in < 30s — small aggregation query).

---

### Section 7 — Tab: Exam Date Config

**Purpose:** Director configures official exam dates and content freeze dates per exam type — data feeds D-10 Calendar, D-05 Stale Alerts, and D-02 freeze enforcement.

**Table:** Same as D-10 Upcoming Exam Dates panel — these are in sync (D-14 and D-10 share the same `content_exam_freeze` table). Edits here propagate to D-10 and vice versa. This tab is an alternate access point for Directors who are in the D-14 syllabus context when they need to check or update exam dates.

**Syllabus Change Management section:**
Director marks topics as removed or added for the next exam cycle:
- Topic status: Active / Next-Cycle-Added / Next-Cycle-Removed
- "Next-Cycle-Removed" topics: shown in amber in D-09 taxonomy with a "Deprecating" badge. SMEs are warned in D-02 when they tag a next-cycle-removed topic: "This topic is being deprecated for the next exam cycle. New questions for this topic will not be included in future exam series."
- "Next-Cycle-Added" topics: new nodes created in D-09 taxonomy with "Upcoming" badge. SMEs can start authoring for them immediately.
- Director can trigger D-09 taxonomy archive flow for Next-Cycle-Removed topics (after sufficient lead time) — which triggers G10 bulk retag if questions are already tagged.

---

## 5. Data Models

### `content_syllabus_target`
| Field | Type | Notes |
|---|---|---|
| `topic_id` | FK → content_taxonomy_topic | — |
| `exam_type_code` | varchar | — |
| `target_count` | int | Minimum published questions target for this topic + exam type |
| `set_by` | FK → auth.User | Director |
| `set_at` | timestamptz | — |

### `content_difficulty_target`
| Field | Type | Notes |
|---|---|---|
| `exam_type_code` | varchar | — |
| `subject_id` | FK → content_taxonomy_subject | — |
| `easy_pct` | decimal | Target Easy % (e.g. 30.0) |
| `medium_pct` | decimal | Target Medium % |
| `hard_pct` | decimal | Target Hard % |
| `set_by` | FK → auth.User | Director |
| `set_at` | timestamptz | — |

### `content_pool_adequacy_cache`
| Field | Type | Notes |
|---|---|---|
| `topic_id` | FK → content_taxonomy_topic | — |
| `exam_type_code` | varchar | — |
| `published_pool_size` | int | Snapshot at last Celery refresh |
| `peak_concurrent_exams` | int | From Div F API at last refresh |
| `questions_per_paper` | int | From Div F exam pattern |
| `safety_factor` | decimal | Director-configured per topic, default 3.0 |
| `minimum_pool_required` | int | Computed |
| `adequacy_pct` | decimal | Computed |
| `refreshed_at` | timestamptz | When Celery last updated this row |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.view_syllabus_coverage')` — Roles 18 + 19–27 |
| SME subject scope | ORM filter: topic nodes shown only for SME's assigned subjects + assigned exam types |
| Edit actions (target, difficulty targets, exam dates, safety factor) | Role 18 only |
| Pool Adequacy tab | Role 18 only — not shown to SMEs |
| Access Level Distribution tab | Role 18 only |
| Bulk Archive (Content Freshness) | Role 18 only |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| No questions published for a topic | Coverage bar shows 0 / target — red. All downstream calculations (difficulty distribution, pool adequacy) show 0 with "No data" label |
| Div F API unavailable for pool adequacy refresh | Celery task fails gracefully — `content_pool_adequacy_cache` retains last successful refresh data. "Last updated: 3 days ago — Div F API unavailable" shown at top of Pool Adequacy tab |
| Director sets Safety Factor to 1.0 for a topic | Warning: "Safety Factor of 1.0 means each question may appear in every concurrent exam simultaneously. Minimum recommended: 2.0 for question integrity." Director must acknowledge before saving |
| Topic is mapped to an exam type but has no questions (new topic added for next cycle) | Shows 0/target with red bar + "Upcoming" badge (if next-cycle-added) or normal red (if existing topic that needs content) |
| SME tries to view Pool Adequacy tab | URL returns 403. SME sees Coverage and Difficulty Distribution tabs only. |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-09 Taxonomy | D-09 → D-14 | Topic hierarchy + exam type mappings | Shared `content_taxonomy_topic` + `content_taxonomy_topic_exam_mapping` |
| D-10 Calendar | D-14 ↔ D-10 | Exam date config shared | Same `content_exam_freeze` table — edits in either page propagate immediately |
| D-05 Director Dashboard | D-14 → D-05 | Pool Adequacy red alerts feed D-05 Stale Alerts panel | `content_pool_adequacy_cache` ORM read |
| D-02 Question Editor | D-10 (via D-14 dates) → D-02 | Content freeze enforcement on Submit | `content_exam_freeze` ORM read — real-time |
| Div F Exam Operations | Div F → D-14 | Peak concurrent exam count, questions per paper — for Pool Adequacy | Div F API call from Celery task → `content_pool_adequacy_cache` |
| Div B Exam Pattern Builder (B-12) | D-14 → B-12 | Difficulty distribution targets per exam type | Shared `content_difficulty_target` table |
| D-01 SME Dashboard | D-14 → D-01 | Coverage gaps (topic count) for SME's Coverage Gaps tab | Same `content_taxonomy_topic` published count aggregation |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- **Coverage tab (Gap View):** Placeholder "Search topics…". Searches: topic name, subtopic name. Instant filter within the topic tree.
- **Difficulty Distribution tab:** Placeholder "Filter topics…". Searches: topic name.
- **Content Freshness tab (G5):** Placeholder "Search by topic or question ID…". Searches: topic name, question UUID short.
- **Pool Adequacy tab (G12):** Placeholder "Search by exam type or topic…". Searches: exam type name, topic name.

### Sortable Columns — Gap View Table
| Column | Default Sort |
|---|---|
| Gap Severity | **Custom: Critical → Amber → OK** — default |
| Published Count | ASC |
| Target | — |
| Coverage % | ASC |

### Sortable Columns — Difficulty Distribution Table
Default sort: topics with **largest deviation from target ratio first** (most out-of-balance).

### Sortable Columns — Content Freshness Table
Default sort: **Valid Until ASC** (soonest expiring first).

### Sortable Columns — Pool Adequacy Table
Default sort: **Adequacy % ASC** (least adequate pools first — prioritise action).

### Pagination
- Coverage topic tree: not paginated (tree, collapse/expand).
- Gap View sub-table: 50 rows, numbered controls.
- Difficulty Distribution: 50 rows.
- Access Level Distribution: 25 rows (fewer topics needed for access level view).
- Content Freshness: 50 rows.
- Pool Adequacy: 50 rows.

### Empty States
| Tab / Section | Heading | Subtext |
|---|---|---|
| Coverage — no questions for topic | "No published questions" | "Add questions to this topic via D-02 or D-07." |
| Pool Adequacy — no Div F data | "No concurrent exam data yet" | "Pool adequacy populates after Div F exam schedules are configured and synced." |
| Content Freshness — nothing expiring | "No expiring content" | "No published Current Affairs questions are approaching their expiry date." |
| Difficulty Distribution — no target set | "No target configured" | "Set difficulty targets for this exam type using the 'Set Target' controls." |

### Toast Messages
| Action | Toast |
|---|---|
| Difficulty target saved | ✅ "Difficulty target saved" (Success 4s) |
| Safety Factor updated (G12) | ✅ "Safety factor updated — pool adequacy recalculated" (Success 4s) |
| Safety Factor below 2.0 | ⚠ "Safety factor below minimum recommended (2.0) — exam integrity risk increased" (Warning persistent) |
| Manual Pool Adequacy refresh | ℹ "Refreshing pool data from Div F — this may take up to 30 seconds" (Info 6s) |
| Bulk archive expired questions | ✅ "{N} questions archived" (Success 4s) |
| Syllabus change marked | ✅ "Topic marked as {Added/Removed} for next cycle" (Success 4s) |
| Assign SME from Pool Adequacy | ℹ "Redirecting to D-10 Calendar pre-filled with this topic" (Info 4s) |

### Loading States
- Coverage tree: full tree skeleton on exam type switch.
- Gap View sub-table: 8-row skeleton.
- Difficulty Distribution charts: chart-area shimmer.
- Pool Adequacy table: 8-row skeleton. "Refresh Now" button: spinner while Celery task runs, "Updated just now" timestamp on complete.
- Content Freshness table + line chart: table skeleton + chart shimmer.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Exam Type selector left (or tab strip top). Tab content full width. Pool Adequacy adequacy % bar visible in table. |
| Tablet | Exam Type as dropdown selector (not left panel). Tab content full width. Table columns reduced. |
| Mobile | Exam Type: dropdown at top. Tab nav: horizontal scroll. Trees: single-level list (collapse to topic only, no subtopic visible — tap topic for subtopic detail). Charts: stack vertically. Pool Adequacy: critical items list (not full table). |

### Charts
- **Coverage tab:** Horizontal progress bars per topic — Published (filled, colour-coded) vs Target (outline). Sorted by coverage % ASC.
- **Difficulty Distribution tab:** Stacked bar chart per topic — Easy (green), Medium (blue), Hard (red). Target ratio shown as horizontal dashed lines per difficulty. Deviation cells amber/red.
- **Access Level Distribution tab:** Pie chart per subject — Platform-Wide / School Only / College Only / Coaching Only proportions. Tooltip: "{N} questions ({%})".
- **Content Freshness tab:** 12-month rolling line chart — net fresh question count per month. Expiry events marked as negative spikes.
- **Pool Adequacy tab:** Adequacy % bar per exam-type/topic combination. Red threshold line at 70%. Green threshold at 100%.

### Role-Based UI
- Full access (all tabs + edit actions): Director (18).
- SME read access (Coverage tab + Difficulty Distribution tab for own subject): SME roles (19–27). Pool Adequacy and Access Level tabs not visible to SMEs (403 on part-routes).
- "Set Target" controls: Director only.
- "Bulk Archive Expired" action: Director and Approver.
- "Reduce Safety Factor" (G12): Director only with explicit confirmation.

---

*Page spec complete.*
*Amendments applied: G5 (Content Freshness tab — expiry tracking + bulk archive for Current Affairs questions) · G12 (Pool Adequacy tab — concurrent demand vs published pool depth, safety factor config, auto-refresh from Div F API)*
*Next file: `d-15-reviewer-assignments.md`*
