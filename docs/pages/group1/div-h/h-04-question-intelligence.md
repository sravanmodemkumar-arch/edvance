# H-04 — Question Intelligence

> **Route:** `/analytics/questions/`
> **Division:** H — Data & Analytics
> **Primary Role:** Data Analyst (44) · Analytics Manager (42)
> **Supporting Roles:** Data Engineer (43) — archive execution; Platform Admin (10) — full
> **File:** `h-04-question-intelligence.md`
> **Priority:** P1 — question quality is foundational to exam fairness at 74K peak load

---

## 1. Page Name & Route

**Page Name:** Question Intelligence
**Route:** `/analytics/questions/`
**Part-load routes:**
- `/analytics/questions/?part=quality-summary` — quality health bar
- `/analytics/questions/?part=question-table` — main question analytics table
- `/analytics/questions/{question_id}/?part=detail-drawer` — question detail drawer

---

## 2. Purpose

H-04 is the analytical lens on the **2M+ question bank**. Every question that reaches a student was reviewed and approved by Division D — but psychometric quality only reveals itself at scale, through attempt data. A question that looks correct on paper can be:
- **Too easy** (everyone gets it right — wastes exam time, no discrimination)
- **Too hard** (everyone fails — demoralises students, no discrimination)
- **Negatively discriminating** (high-scorers get it wrong while low-scorers get it right — indicates a wrong answer key or ambiguous wording)
- **Dead** (published but never used in any exam — taking up bank space)
- **Distractor-broken** (one wrong option is never chosen — binary choice instead of 4-way)

**Who needs this page:**
- Data Analyst (44) — weekly question quality audit; flag poor questions for Division D review
- Analytics Manager (42) — question bank health KPIs; AI replacement commissioning decisions
- Data Engineer (43) — bulk archive execution based on Analyst flags

**Why this matters at 74K peak:** A single negatively-discriminating question at high weight can invalidate a rank for thousands of students. Catching it before the next exam cycle is critical.

---

## 3. Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Page header: "Question Intelligence"    [Export Quality Report]  │
│  Filters: Domain | Subject | Topic | Difficulty | Flag | Used     │
├────────┬────────┬────────┬────────┬────────┬────────┬─────────────┤
│ Total  │ Never  │ Poor   │Negative│ Stale  │Avg     │ Questions   │
│Questions│ Used  │Discrim.│ D     │(>90d)  │Difficulty│ w/ Issues  │
├────────┴────────┴────────┴────────┴────────┴────────┴─────────────┤
│  Quality Flag Distribution (pie chart)  │  CTT Scatter Plot      │
│  OK / POOR_D / ALL_CORRECT / etc.       │  Difficulty vs. Disc.  │
├─────────────────────────────────────────┴────────────────────────┤
│  Question Analytics Table (server-side paginated, 25 rows)       │
├──────────────────────────────────────────────────────────────────┤
│  Question Detail Drawer (slides in on row click)                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Filters

| Filter | Control | Notes |
|---|---|---|
| Domain | Multiselect: All / SSC / RRB / NEET / JEE / AP Board / TS Board | — |
| Subject | Multiselect: depends on selected domain | Cascading dropdown |
| Topic | Multiselect: depends on selected subject | Cascading dropdown |
| Difficulty Range | Range slider: 0.0–1.0 | Filter `difficulty_index` between two values |
| Discrimination Range | Range slider: -0.5–1.0 | Filter `discrimination_index` between two values |
| Quality Flag | Multiselect: OK / POOR_DISCRIMINATION / ALL_CORRECT / ALL_WRONG / NEGATIVE_D / NEVER_USED / STALE / INSUFFICIENT_ATTEMPTS | — |
| Usage Status | Toggle: All / Used / Never Used | `last_used_at IS NULL` = Never Used |
| Min Attempts | Number input | Only show questions with `attempt_count ≥ N` (default: 30) |

Filters persist in URL. [Reset All Filters] link.

---

### Section B — Quality Health Bar

Seven tiles sourced from `analytics_question_stats` (latest nightly computation).

| Tile | Description | Colour Rule |
|---|---|---|
| Total Questions | Questions in analytics (those with ≥ 1 attempt OR published) | Neutral |
| Never Used | `quality_flag = NEVER_USED` — published but never appeared in any exam | Amber if > 5% of total |
| Poor Discrimination | `discrimination_index < 0.2` (with ≥30 attempts) | Red if > 10% of total |
| Negative D | `discrimination_index < 0` — red flag: wrong key or ambiguous | Red — always |
| Stale (>90 days) | `last_used_at < NOW() - INTERVAL '90 days'` — **rolling 90-day window**, not a fixed calendar date. Resets immediately when a question is used in any new exam. `quality_flag` is set to `STALE` nightly by `compute_question_analytics`. | Amber if > 20% |
| Avg Difficulty | Mean `difficulty_index` across all questions with ≥30 attempts | Green if 0.45–0.65 (ideal range); Amber outside |
| Questions with Issues | Any `quality_flag != OK` | Red if > 15% of questions with ≥30 attempts |

Each tile is clickable — applies the corresponding quality flag filter to the table.

---

### Section C — Quality Flag Distribution (Pie Chart)

**Purpose:** Shows the proportion of the question bank in each quality state. A healthy bank has >85% in `OK` state.

**Implementation:** Chart.js Doughnut chart. Segments:
- `OK` — green
- `POOR_DISCRIMINATION` — amber
- `NEGATIVE_D` — red
- `ALL_CORRECT` — orange
- `ALL_WRONG` — dark red
- `NEVER_USED` — grey
- `STALE` — light grey
- `INSUFFICIENT_ATTEMPTS` — blue (not a quality issue — just not enough data)

Centre label: `{N} total · {M}% OK`

Clicking a segment: applies that quality flag filter to the table below.

---

### Section D — CTT Scatter Plot

**Purpose:** The single most powerful diagnostic chart for question quality. Each point is a question. X-axis = Difficulty Index (p-value). Y-axis = Discrimination Index (D).

```
    D (Discrimination)
1.0 │
    │                    ●●  ●●  ●● ●●●
0.5 │            ●●●●● ●●●● ●●●●●●●●●●●●
    │      ● ●●●●●●●●●●●●●●●●●●●●●●
0.3 │   ● ●●●●●●●●●●●●●●●●●●●●●●  (D=0.3 ideal floor)
    │ ●●●●●●●●●●●●    ●●●
0.0 │─────────────────────────────────────
    │ ●     ●      ●  ●         ← negative D — suspicious
-0.5│
    └────────────────────────────────────
      0.0         0.5          1.0
      (Hard)    (Medium)     (Easy)    p (Difficulty)
```

**Y-axis range:** -0.5 to 1.0 (matching the Discrimination Range slider in Section A). Questions with D < 0 must be visible below the zero line — never clipped.

**Zones:**
- **Ideal zone:** D > 0.3, p = 0.30–0.70 (medium difficulty, good discrimination) — shown with green shading
- **Acceptable zone:** D = 0.2–0.3, p = 0.20–0.80 — shown with yellow shading
- **Problem zone:** D < 0.2 — amber background
- **Danger zone:** D < 0 — red background

**Interactions:**
- Hover on a dot: tooltip with `question_id` + subject + p-value + D-value + attempt count
- Click on a dot: opens Question Detail Drawer for that specific question
- **Point selection** (click individual dots): clicking a dot in the scatter adds it to a staging selection list (dot turns orange). Multiple dots can be selected. **[Commission AI Replacements from Selection]** button appears when ≥ 1 dot is selected — navigates to `/analytics/ai-generation/?prefill=1&domain={comma_sep_domains}&subject={comma_sep_subjects}&topic={comma_sep_topics}&source_questions={comma_sep_question_ids}`. H-07 reads these URL params to pre-populate the batch creation wizard. Note: drag/box-select on HTML Canvas requires chartjs-plugin-zoom (`mode: 'x', dragToZoom: false, selectMode: 'point'`); if the plugin is not available, selection degrades to click-only mode with a banner: "Point selection only — drag selection unavailable."
- Legend toggle: [Show by Domain] — colour-codes dots by exam domain

---

### Section E — Question Analytics Table

Server-side paginated, 25 rows per page. Source: `analytics_question_stats`.

| Column | Sortable | Notes |
|---|---|---|
| Question ID | No | Truncated display; full ID in tooltip |
| Domain | Yes | Badge |
| Subject | Yes | — |
| Topic | Yes | — |
| Attempts | Yes | Right-aligned. Grey if < 30 (INSUFFICIENT_ATTEMPTS) |
| Difficulty (p) | Yes | Progress bar: green ≥0.7 (easy), amber 0.4–0.7, red <0.4. Value shown |
| Discrimination (D) | Yes (default: ASC) | Colour: green >0.3, amber 0.2–0.3, red <0.2, dark red <0 |
| Omission Rate | Yes | Amber if > 20% (students are skipping this question) |
| Last Used | Yes | Date; grey if > 90 days |
| Quality Flag | Yes | Pill badge colour-coded per flag value |
| Actions | — | [View →] opens drawer; [Flag for Review] (marks for Division D review queue); [Archive] (Data Engineer and Platform Admin only — **disabled with tooltip "Archive requires Data Engineer access"** for other roles) |

**[Flag for Review]:** Sets a `division_d_review_flag = true` on the question (creates a content review task in Division D's question management page, visible to Content Director role 18 and relevant SME). Confirmation: "Flag '{question_id}' for Division D review? This will create a review task for the Content Director."

**[Archive]:** Data Engineer (43) and Platform Admin (10) only. Rendered as disabled button for Analytics Manager and Data Analyst (not hidden — they can see the action exists but cannot perform it). Moves question to `archived` status in question registry. Confirmation: "Archive question {id}? It will no longer appear in exam creation tools. This action can be reversed by Division D Content Director within 30 days." Not a hard delete.

**Bulk actions** (rows selected):
- [Bulk Flag for Division D Review] — flags all selected as needing review
- [Commission AI Replacements] — navigates to H-07 pre-filled with domain/subject/topic from selected questions; opens batch creation wizard
- [Export Selected CSV] — question stats for selected rows

---

### Section F — Question Detail Drawer

480px right drawer. Opens on row click or [View →].

**Drawer header:** `{question_id}` + Domain + Subject + Topic + Quality flag badge.

**Tabs: Stats | Question Preview | History | Similar Questions**

#### Stats Tab

**CTT metrics panel:**
| Metric | Value | Benchmark |
|---|---|---|
| Difficulty Index (p) | e.g., 0.32 | Platform avg for subject: 0.58 |
| Discrimination Index (D) | e.g., 0.18 | Ideal: > 0.3 |
| Omission Rate | e.g., 12% | Platform avg: 6% |
| Attempt Count | e.g., 4,200 | — |
| First Used | Date | — |
| Last Used | Date | — |
| Quality Flag | POOR_DISCRIMINATION | — |

**Distractor analysis panel:**
```
  Option A  ████████████████████   42% (correct)
  Option B  ████████████           28%
  Option C  ████████               18%
  Option D  ██                      8%
  Skipped   ██                      4%
```
Interpretation: Option D is barely used (8%). A good distractor should be chosen by 15–25% of students. If one option gets < 10%, it's a "give-away" distractor that effectively turns the question into a 3-choice question.

**Percentile chart:** Bar chart — "How did this question perform across score bands?" Shows % correct in each score decile (decile 1 = lowest scorers, decile 10 = highest). For a good question, higher scorers should get it right more often (upward slope). Negative D questions show a downward slope.

**DPDPA-compliant discrimination index computation:** The `discrimination_index` (point-biserial) is computed from **bucketed, aggregate data only** — no individual student IDs are used. The Celery task groups attempt records by score decile (10 buckets), then computes the correlation between decile-bucket membership (proportion correct per bucket) and decile rank. This approximation of point-biserial is DPDPA-compliant because: (1) student IDs never leave the tenant schema, (2) only per-question aggregate correct-counts per decile bucket are read, and (3) the analytics schema stores only the final computed `discrimination_index` value, not the underlying attempt records.

#### Question Preview Tab

Displays the full question text, all 4 options, the correct answer, and the explanation. Read-only.

Note: "Question content is read-only in Division H. To edit this question, navigate to Division D content management."

**[Open in Division D →]** — external link to the question edit page in the content module.

#### History Tab

Aggregate usage summary for this question across all tenants. **Not a per-exam list** — `analytics_question_stats` stores only pre-aggregated summary fields, not a row per exam. A per-exam history would require a separate `analytics_question_exam_history` table that does not currently exist; this tab shows the available aggregates only.

| Metric | Value | Source |
|---|---|---|
| Total exam appearances | {N} | `analytics_question_stats.attempt_count` (proxy — each attempt = one exam use) |
| First used in an exam | {date} | `analytics_question_stats.first_used_at` |
| Last used in an exam | {date} | `analytics_question_stats.last_used_at` |
| Domains this question has been used in | SSC, AP Board | `analytics_question_stats.domain` (single domain per question — question bank is domain-specific) |
| Avg score in exams where this appeared | {pct}% | `analytics_question_stats.difficulty_index` (inverse proxy: avg score ≈ p-value × 100%) |

**Note to devs:** If per-exam drill-down is needed in a future sprint, add an `analytics_question_exam_history` table (`question_id`, `exam_date`, `tenant_id` redacted for DPDPA, `attempt_count`, `pct_correct`) populated by Task 2. Until then, this tab shows the aggregated stats only.

#### Similar Questions Tab

List of up to 5 questions with the same Domain + Subject + Topic that have better quality flags (D > 0.3, p in 0.3–0.7 range). Helps the analyst identify if there are better alternatives already in the bank before commissioning AI replacements.

| Column | Notes |
|---|---|
| Question ID | — |
| Difficulty (p) | — |
| Discrimination (D) | — |
| Attempts | — |
| Quality Flag | — |

[Commission AI Replacement] — pre-fills H-07 batch creation with this question's domain/subject/topic.

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | Analytics Manager (42), Data Analyst (44), Data Engineer (43), Platform Admin (10) |
| [Flag for Review] | Data Analyst (44), Analytics Manager (42) |
| [Archive] | Data Engineer (43), Platform Admin (10) only — Analyst can flag but not archive |
| [Commission AI Replacements] | Analytics Manager (42) — initiates H-07 batch creation |
| [Export Quality Report] | Analytics Manager (42), Data Analyst (44) |
| Question preview content | All permitted roles — read-only |
| [Open in Division D →] | All permitted roles — navigates away to Div D |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Question has < 30 attempts | Quality flag = `INSUFFICIENT_ATTEMPTS`. Difficulty/Discrimination shown as "—". Distractor stats not shown (< 30 students — DPDPA minimum not met for any question stat display). Tooltip: "Minimum 30 student attempts required for reliable statistics and DPDPA compliance." The scatter plot excludes these questions from visible dots (they are shown only in the `INSUFFICIENT_ATTEMPTS` colour in the flag distribution pie chart). Filter default (Min Attempts = 30) enforces this at the table level. |
| Discrimination index = exactly 0 | Shows as "0.00" — theoretically possible if all students scored identically. Tooltip: "Zero discrimination — this question provided no information about student ability." |
| All 4 options have identical distractor rates | Distractor analysis panel shows warning: "⚠ All distractors equally attractive — this is unusual and may indicate question ambiguity." |
| Question archived in Division D but still in analytics | Quality flag = `ARCHIVED`. Row still shows in H-04 (historical data preserved). Badge: "ARCHIVED — not in active bank." |
| [Commission AI Replacements] for a question that already has pending AI batch | Warning: "There's already an AI batch in progress for {topic}. View existing batch in H-07 before creating another?" with [View] and [Create Anyway] options |
| Export > 50,000 rows | "Large export ({N} questions). Processing in background — estimated 3–5 min." |
| Pipeline not run today | Table shows last computed values with staleness indicator: "Stats as of: {date}" |

---

## 7. UI Patterns

### Loading States
- Quality bar: 7-tile shimmer
- Pie chart: circular shimmer
- Scatter plot: grey canvas with "Loading data..."
- Table: 10-row shimmer
- Drawer: header shimmer + 4 tab labels + stats panel skeleton

### Toasts
| Action | Toast |
|---|---|
| Question flagged | ✅ "Question {id} flagged for Division D review" (3s) |
| Question archived | ✅ "Question {id} archived — reversible within 30 days" (4s) |
| AI batch commissioned | ✅ "Redirecting to H-07 with pre-filled batch details" (2s, then redirect) |
| Export queued | ✅ "Quality report queued — notified when ready" (4s) |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full layout: pie + scatter side by side; full table |
| Tablet | Pie + scatter stacked. Table: 6 visible columns. |
| Mobile | Pie chart only (no scatter — too small to be useful). Table card view. |

---

*Page spec complete.*
*H-04 covers: quality health bar (7 flags) → CTT scatter plot (difficulty vs. discrimination — ideal/acceptable/problem/danger zones) → quality flag pie chart → question analytics table with bulk archive and AI replacement commissioning → question detail drawer (CTT stats / distractor analysis / percentile curve / question preview / similar questions).*
