# Page 18: Topic Gap Analysis

**Division:** M — Analytics & MIS
**URL:** `/group/analytics/topic-gaps/`
**Primary Role:** 105 — Exam Analytics Officer
**Supporting Roles:** 102 (Analytics Director), 103 (MIS Officer), 104 (Academic Data Analyst)
**Access Level:** G1 (read-only on exam + academic data from Divisions D and B; write only on Division M gap records and escalations)

---

## 1. Purpose

Surfaces **topic-level performance gaps** — where students across branches consistently under-perform on specific syllabus topics within a subject. Aggregates wrong-answer patterns, low-score clusters, and teacher-reported coverage flags into a ranked gap list. Allows the Exam Analytics Officer to create remediation recommendations and escalate persistent gaps to branch principals or academic teams.

---

## 2. Roles & Permissions Matrix

| UI Element | Role 102 | Role 103 | Role 104 | Role 105 |
|---|---|---|---|---|
| KPI bar (5 cards) | View | View | View | View |
| Filter bar | View + use | View + use | View + use | View + use |
| Topic gap table | View | View | View | View |
| Gap detail drawer | View | View | View | View |
| Create remediation plan | — | — | — | Create |
| Edit / delete own remediation | — | — | — | Edit/Delete |
| Escalate gap to branch | — | — | — | Create |
| Mark gap as resolved | — | — | — | Update |
| Export (CSV / PDF) | Download | Download | Download | Download |

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ Breadcrumb: Analytics & MIS > Topic Gap Analysis                    │
│ Title: "Topic Gap Analysis"    [Export ▼]  [Refresh]                │
├─────────────────────────────────────────────────────────────────────┤
│  KPI BAR (5 cards)                                                   │
│  Topics Analysed | Avg Gap Score | Critical Gaps | Resolved (YTD) | │
│                  |               |               | Remediations    │
├─────────────────────────────────────────────────────────────────────┤
│  FILTER BAR                                                          │
│  Subject [All ▼]  Class [All ▼]  Stream [All ▼]  Branch [All ▼]    │
│  Exam Cycle [All ▼]  Gap Severity [All ▼]  Status [Open ▼]         │
│  [Search topics…]  [Apply]  [Clear]                                  │
├─────────────────────────────────────────────────────────────────────┤
│  TOPIC GAP TABLE (sortable, paginated)                               │
│  [+ Create Remediation Plan]  (Role 105 only)                        │
├─────────────────────────────────────────────────────────────────────┤
│  SUBJECT-LEVEL GAP SUMMARY CHART                                     │
│  Stacked bar: Critical / High / Medium / Low gaps per subject        │
├─────────────────────────────────────────────────────────────────────┤
│  TOP RECURRING TOPICS CHART                                          │
│  Horizontal bar: Top 10 topics by combined gap score                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. KPI Bar

Five stat cards, auto-refresh `hx-trigger="every 300s"`, `hx-get="/group/analytics/topic-gaps/kpis/"`, `hx-target="#gap-kpi-bar"`.

| # | Label | Value | Sub-label | Highlight |
|---|---|---|---|---|
| 1 | Topics Analysed | Count of distinct topics in filter scope | "This cycle" | — |
| 2 | Avg Gap Score | Mean gap score (0–100, higher = bigger gap) | "Across all subjects" | Colour badge |
| 3 | Critical Gaps | Topics with severity = Critical | "Need immediate action" | `bg-red-50` if > 0 |
| 4 | Resolved (YTD) | Topics marked resolved this academic year | "vs last year" | `bg-green-50` |
| 5 | Active Remediations | Count of open remediation plans | "In progress" | — |

---

## 5. Filter Bar

| Control | Type | Options |
|---|---|---|
| Subject | Select | All + subject list |
| Class | Select | All / 9 / 10 / 11 / 12 |
| Stream | Select | All / Science / Commerce / Arts / Vocational |
| Branch | Multi-select pill | All branches in group |
| Exam Cycle | Select | All cycles + specific cycle names |
| Gap Severity | Select | All / Critical / High / Medium / Low |
| Status | Select | Open / In Remediation / Resolved / All |
| Search | Text input | Searches topic name and subject |

- `[Apply]` triggers `hx-get="/group/analytics/topic-gaps/table/"` replacing `#gap-table-section`.
- `[Clear]` resets all controls to defaults and re-applies.
- Active filter count badge shown on `[Apply]` button when filters are non-default.
- Branch multi-select uses a dropdown checklist with "Select All / Clear All" options.

---

## 6. Topic Gap Table

### 6.1 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Integer | No | Row number |
| Topic | Text | Yes | Truncated at 50 chars, full text in tooltip |
| Subject | Badge | Yes | Colour by subject |
| Class | Text | Yes | — |
| Stream | Text | No | — |
| Affected Branches | Integer | Yes | Count of branches with this gap |
| Avg Gap Score | Progress bar + number | Yes | 0–100; colour by severity tier |
| Severity | Badge | Yes | Critical (red) / High (orange) / Medium (yellow) / Low (blue) |
| Status | Badge | Yes | Open / In Remediation / Resolved |
| Exam Cycles | Text | No | "3 cycles" — consecutive cycles with this gap |
| Last Updated | Date | Yes | — |
| Actions | Buttons | No | [View] [Escalate] [Resolve] (role-gated) |

### 6.2 Severity Tiers

| Gap Score | Severity | Badge Colour |
|---|---|---|
| ≥ 70 | Critical | Red (`bg-red-100 text-red-800`) |
| 50–69 | High | Orange (`bg-orange-100 text-orange-800`) |
| 30–49 | Medium | Yellow (`bg-yellow-100 text-yellow-800`) |
| < 30 | Low | Blue (`bg-blue-100 text-blue-800`) |

Gap Score is computed as: `(1 - avg_correct_rate) × 100 × recency_weight × frequency_weight`. Recency weight is 1.0 for current cycle, 0.7 for previous, 0.4 for 2 cycles ago.

### 6.3 Table Controls

- **Sortable columns:** click header to sort ASC, click again for DESC. HTMX replaces tbody.
- **Pagination:** 20 rows per page, server-side. Page controls: `<< < [1] [2] [3] > >>`.
- **Row click:** opens gap detail drawer (same as `[View]`).
- **[Escalate]:** Role 105 only — opens drawer directly to Escalation tab.
- **[Resolve]:** Role 105 only — opens confirm modal → PATCH endpoint → status badge updates inline.
- **Bulk actions:** Checkbox column appears for Role 105. Bulk actions: "Bulk Escalate", "Bulk Mark Resolved".

### 6.4 Pagination

```
hx-get="/group/analytics/topic-gaps/table/"
hx-target="#gap-table-section"
hx-swap="outerHTML"
hx-include="#gap-filter-form"
```

---

## 7. Gap Detail Drawer

**ID:** `topic-gap-detail-drawer`
**Width:** 680px slide-in from right
**Header:** `{Topic Name}` — `{Subject}` — Severity badge

### Tab 1 — Gap Overview

| Section | Content |
|---|---|
| Gap Score Breakdown | Horizontal stacked bar: Avg correct rate per branch, sorted ascending |
| Consecutive Cycles | Timeline pills showing which exam cycles this gap appeared in |
| Wrong Answer Patterns | Top 5 wrong answer categories (from MCQ item analysis if available): "Conceptual Error", "Calculation Error", "Misread Question", "Careless Error", "Not Attempted" — shown as donut mini-chart |
| Affected Student Count | Total students who scored < threshold on this topic across all branches |
| Top Affected Branches | Table: Branch | Avg Score | Students Affected | Severity |
| Teacher Coverage Flag | "Reported as not covered" count from teacher syllabus completion data (Division B read-only) |

**Score Trend Mini-Chart:** Line chart showing topic avg score across last 6 exam cycles. Canvas id: `gapTrendMini`.

### Tab 2 — Remediation Plans

List of all remediation plans for this topic, ordered by creation date descending.

**Plan Card:**

| Field | Value |
|---|---|
| Plan Title | Text |
| Target Branch(es) | Pill list |
| Created By | Name + role |
| Status | Open / Active / Completed |
| Target Completion | Date |
| Assigned Teacher(s) | Name list |
| Interventions | Bullet list (e.g. "Extra practice sessions", "Concept review worksheet") |
| Progress Note | Last update text |

**[+ Create Remediation Plan] — Role 105 only:**

Opens a sub-form within the drawer:

| Field | Type | Validation |
|---|---|---|
| Plan Title | Text input (max 200 chars) | Required |
| Target Branches | Multi-select (branches in group) | Required, ≥ 1 |
| Target Classes | Multi-select | Required |
| Assigned Teachers | Multi-select (teachers from Division B read) | Optional |
| Intervention Type | Checkbox: Extra Class / Worksheet / Online Module / Peer Tutoring / Parent Meeting | ≥ 1 required |
| Description | Textarea (max 1000 chars) | Required, min 20 chars |
| Target Completion Date | Date picker (min: today + 7 days) | Required |
| Success Metric | Text input (max 300 chars) | Required |
| Notify via | Checkbox: In-app / Email | ≥ 1 required |

Submit: POST `/api/v1/analytics/topic-gaps/remediations/` → success toast → plan card prepended to list.

**Edit Plan:** pencil icon → form pre-filled in same sub-form area (PUT endpoint).
**Delete Plan:** trash icon → confirm modal → DELETE endpoint → card removed with toast.

### Tab 3 — Escalations

List of escalations linked to this topic gap.

**Escalation record fields:** Branch | Severity | Status | Assigned To | Created Date | Resolution Date | [View Detail]

**[Create Escalation] — Role 105 only:**

| Field | Type | Validation |
|---|---|---|
| Target Branch | Select (branches showing this gap) | Required |
| Severity | Select: Low / Medium / High / Critical | Required |
| Root Cause | Select: Teaching Gap / Curriculum Issue / Student Preparedness / External Factors / Unknown | Required |
| Description | Textarea (max 1000 chars) | Required |
| Recommended Action | Textarea (max 500 chars) | Required |
| Assign To | Select (branch principals in group) | Required |
| Target Resolution Date | Date picker | Required |
| Notify via | Checkbox: In-app / Email | ≥ 1 required |

Submit: POST `/api/v1/analytics/topic-gaps/escalations/` → success toast.

---

## 8. Subject-Level Gap Summary Chart

**Type:** Stacked horizontal bar (Chart.js 4.x Bar, `indexAxis: 'y'`)
**Canvas ID:** `subjectGapSummaryChart`
**Height:** 260px

- Y-axis: Subject names.
- X-axis: Gap count.
- Stacks: Critical (red), High (orange), Medium (yellow), Low (blue).
- Tooltip: `{Subject}: {severity} — {count} topics`.
- Clicking a bar segment filters the table to that subject + severity combination.
- Legend: top-right, horizontal.

---

## 9. Top Recurring Topics Chart

**Type:** Horizontal bar chart (Chart.js 4.x)
**Canvas ID:** `topRecurringTopicsChart`
**Height:** 340px

- Y-axis: Top 10 topic names (truncated to 35 chars).
- X-axis: Combined gap score (sum of gap scores across all affected branches).
- Bar colour: severity gradient (red for highest, blue for lowest).
- Tooltip: `{Topic} ({Subject}): Combined score {value}, {n} branches affected`.
- Clicking a bar opens the gap detail drawer for that topic.

---

## 10. Create Remediation Plan (Standalone — Role 105)

The `[+ Create Remediation Plan]` button above the table opens a full-page drawer (not tied to a specific topic) allowing the Exam Analytics Officer to create a group-wide remediation initiative across multiple topics.

**Drawer ID:** `create-remediation-drawer`
**Width:** 720px

| Field | Type | Validation |
|---|---|---|
| Initiative Title | Text (max 200 chars) | Required |
| Target Topics | Multi-select (searchable) from topic list | Required, ≥ 1 |
| Target Branches | Multi-select | Required |
| Target Classes | Multi-select | Required |
| Stream | Select | Required |
| Intervention Types | Checkbox group | ≥ 1 |
| Description | Textarea (max 1500 chars) | Required |
| Assigned Teachers | Multi-select | Optional |
| Start Date | Date picker | Required |
| Target Completion Date | Date picker (must be > Start Date) | Required |
| Success Criteria | Textarea (max 500 chars) | Required |
| Review Frequency | Select: Weekly / Bi-weekly / Monthly | Required |
| Notify via | Checkbox: In-app / Email | ≥ 1 |

Submit: POST `/api/v1/analytics/topic-gaps/remediations/` → success toast → drawer closes → table refreshes to show updated "In Remediation" status badges.

---

## 11. Mark as Resolved Modal

Triggered by `[Resolve]` action (Role 105 only).

| Field | Type | Validation |
|---|---|---|
| Topic | Read-only | — |
| Resolution Date | Date picker (default: today) | Required |
| Resolution Notes | Textarea (max 500 chars) | Required, min 20 chars |
| Evidence | Checkbox: "Attach latest exam data showing improvement" | Optional |
| Notify stakeholders | Checkbox: In-app / Email | Optional |

PATCH `/api/v1/analytics/topic-gaps/{id}/resolve/` → row status badge updates inline to "Resolved" → success toast.

---

## 12. Export Modal

| Option | Endpoint | Notes |
|---|---|---|
| Export Gap List (CSV) | GET `/api/v1/analytics/topic-gaps/export/?format=csv` | Includes active filters |
| Export Full Report (PDF) | POST `/api/v1/analytics/topic-gaps/export/` | Async job with polling |
| Export Remediations (CSV) | GET `/api/v1/analytics/topic-gaps/remediations/export/` | All plans |
| Export Escalations (CSV) | GET `/api/v1/analytics/topic-gaps/escalations/export/` | All escalations |

**PDF async flow:** same polling pattern as page 17 — POST → job_id → poll every 5s → download on complete.

Filename format: `topic-gap-analysis_{subject}_{class}_{cycle}_{date}.csv`.

---

## 13. Toast Notifications

| Trigger | Type | Message |
|---|---|---|
| Remediation created | Success | "Remediation plan created for {Topic}." |
| Remediation updated | Success | "Remediation plan updated." |
| Remediation deleted | Info | "Remediation plan removed." |
| Escalation created | Success | "Escalation raised for {Topic} at {Branch}. Assigned to {Principal}." |
| Gap marked resolved | Success | "{Topic} marked as resolved." |
| Form validation fail | Error | "Please fill in all required fields." |
| Export started | Info | "Preparing export…" |
| Export ready | Success | "Export ready. Click to download." |
| Export failed | Error | "Export failed. Please try again." |
| Data load error | Error | "Failed to load topic gaps. Retrying in 30s." |

---

## 14. Empty States

| Context | Message | CTA |
|---|---|---|
| No gaps in filter scope | "No topic gaps found for the selected filters." | "Reset Filters" |
| No critical gaps | "No critical gaps detected for this cycle. " | — |
| No remediation plans for topic | "No remediation plans created yet." | "+ Create Plan" (Role 105) |
| No escalations for topic | "No escalations for this topic yet." | "Create Escalation" (Role 105) |
| No exam item data | "Topic-level item analysis data is not available for this exam cycle." | — |

---

## 15. Loader States

| Element | Loader |
|---|---|
| Initial page load | Full skeleton: 5 card shimmer + filter bar shimmer + table shimmer (20 rows) + 2 chart placeholders |
| Table reload (filter/sort/page) | Table body shimmer (20 rows) |
| KPI bar refresh | Individual card shimmer |
| Drawer open | Spinner centred in drawer body |
| Tab switch within drawer | Tab content shimmer |
| Chart render | Canvas grey overlay with spinner |
| Export PDF generation | Progress indicator in modal |

---

## 16. HTMX Patterns

| Pattern | Target | Endpoint | Trigger |
|---|---|---|---|
| Table reload (filter/sort/page) | `#gap-table-section` | `/group/analytics/topic-gaps/table/` | Apply button / sort click / page nav |
| KPI auto-refresh | `#gap-kpi-bar` | `/group/analytics/topic-gaps/kpis/` | `every 300s` |
| Search input | `#gap-table-section` | `/group/analytics/topic-gaps/table/` | `keyup changed delay:300ms` |
| Drawer open | `#topic-gap-detail-drawer` | `/group/analytics/topic-gaps/{id}/detail/` | Row click / [View] |
| Remediation POST | `#remediation-form` | `/api/v1/analytics/topic-gaps/remediations/` | Form submit |
| Escalation POST | `#escalation-form` | `/api/v1/analytics/topic-gaps/escalations/` | Form submit |
| Resolve PATCH | `#resolve-modal` | `/api/v1/analytics/topic-gaps/{id}/resolve/` | Modal confirm |
| Export poll | `#export-status` | `/api/v1/analytics/export-jobs/{id}/status/` | `every 5s` (stop on complete) |
| Chart data reload | `#gap-charts-section` | `/group/analytics/topic-gaps/charts/` | Filter Apply |

---

## 17. API Endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | `/api/v1/analytics/topic-gaps/` | Gap list (paginated, filtered) | G1 |
| GET | `/api/v1/analytics/topic-gaps/kpis/` | KPI card values | G1 |
| GET | `/api/v1/analytics/topic-gaps/charts/` | Chart data | G1 |
| GET | `/api/v1/analytics/topic-gaps/{id}/detail/` | Gap detail + branches + trends | G1 |
| GET | `/api/v1/analytics/topic-gaps/remediations/` | Remediation plan list | G1 |
| POST | `/api/v1/analytics/topic-gaps/remediations/` | Create remediation plan | Role 105 |
| PUT | `/api/v1/analytics/topic-gaps/remediations/{id}/` | Update plan | Role 105 (own) |
| DELETE | `/api/v1/analytics/topic-gaps/remediations/{id}/` | Delete plan | Role 105 (own) |
| GET | `/api/v1/analytics/topic-gaps/escalations/` | Escalation list | G1 |
| POST | `/api/v1/analytics/topic-gaps/escalations/` | Create escalation | Role 105 |
| PATCH | `/api/v1/analytics/topic-gaps/{id}/resolve/` | Mark resolved | Role 105 |
| GET | `/api/v1/analytics/topic-gaps/export/` | CSV export | G1 |
| POST | `/api/v1/analytics/topic-gaps/export/` | Async PDF export | G1 |
| GET | `/api/v1/analytics/topic-gaps/remediations/export/` | Remediations CSV | G1 |
| GET | `/api/v1/analytics/topic-gaps/escalations/export/` | Escalations CSV | G1 |
| GET | `/api/v1/analytics/export-jobs/{id}/status/` | Poll export status | G1 |

---

## 18. Mobile (Flutter + Riverpod)

| Screen | Description |
|---|---|
| `TopicGapListScreen` | KPI cards + searchable, filterable gap list (severity badges) |
| `TopicGapDetailScreen` | Gap overview tab + score trend mini-chart |
| `RemediationListScreen` | Scrollable cards of active remediations for a topic |
| `TopicGapChartsScreen` | Subject summary chart + top recurring topics chart |

State provider: `topicGapProvider` (Riverpod). Pull-to-refresh. No write actions available on mobile (create/escalate is desktop-only for this page).

---

## 19. Accessibility & Responsiveness

- Table is horizontally scrollable on mobile; column visibility collapses: on < 768px, hide Stream, Exam Cycles, Last Updated columns.
- Severity badges use both colour and text label (not colour alone).
- Drawer closes on `Escape`; focus trap within drawer while open.
- All form fields have visible labels, `aria-required`, and inline error messages via `aria-describedby`.
- Chart canvases have `role="img"` with descriptive `aria-label` for screen readers.
- Stacked bar chart colours include pattern fills as a secondary encoding for colourblind users.
