# Page 23: Data Quality Dashboard

**Division:** M — Analytics & MIS
**URL:** `/group/analytics/data-quality/`
**Primary Role:** 103 — MIS Officer
**Supporting Roles:** 102 (Analytics Director), 104 (Academic Data Analyst)
**Limited access:** 105 (Exam Analytics Officer) — exam data quality tiles only
**Restricted:** 106 (Hostel Analytics Officer), 107 (Strategic Planning Officer) — no access
**Access Level:** G1 (read-only on data quality metrics from all operational divisions; write on Division M quality flags and remediation tickets)

---

## 1. Purpose

Provides a real-time overview of data completeness, accuracy, and freshness across all operational divisions (Academic, Exam, Finance, Hostel, Attendance, etc.). The MIS Officer uses this dashboard to identify data gaps that compromise analytics accuracy, raise remediation tickets to responsible division heads, and track resolution. Data quality score feeds directly into the Branch Health Scorecard (page 11) as the "Data Quality" dimension (10% weight).

---

## 2. Roles & Permissions Matrix

| UI Element | Role 102 | Role 103 | Role 104 | Role 105 |
|---|---|---|---|---|
| Group-level quality score | View | View | View | — |
| Division-level tiles (all) | View | View | View | — |
| Exam division tile only | — | — | — | View |
| Branch quality table | View | View | View | — |
| Remediation ticket list | View | View | View | View (own division) |
| Create remediation ticket | — | Create | — | — |
| Edit / close ticket | — | Own only | — | — |
| Data quality trend chart | View | View | View | — |
| Export (CSV / PDF) | Download | Download | Download | — |

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ Breadcrumb: Analytics & MIS > Data Quality Dashboard                │
│ Title: "Data Quality Dashboard"   [Export ▼]  [Refresh]            │
├─────────────────────────────────────────────────────────────────────┤
│  GROUP QUALITY SCORE BANNER                                          │
│  Overall Group Data Quality Score: [██████████ 84 / 100]            │
│  Last computed: 2026-03-22 06:00 IST                                 │
├─────────────────────────────────────────────────────────────────────┤
│  DIVISION QUALITY TILES (2×4 grid)                                   │
│  Academic | Exam | Finance | Attendance | Hostel | HR | MIS | Other  │
├─────────────────────────────────────────────────────────────────────┤
│  FILTER BAR                                                          │
│  Division [All ▼]  Branch [All ▼]  Status [All ▼]  Date [This M ▼] │
├──────────────────────────────────┬──────────────────────────────────┤
│  BRANCH QUALITY TABLE            │  QUALITY TREND CHART             │
│  (sortable, paginated)           │  (Line — 12 months)              │
├──────────────────────────────────┴──────────────────────────────────┤
│  REMEDIATION TICKETS TABLE   [+ Raise Ticket] (Role 103)            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Group Quality Score Banner

Full-width card at the top of the page.

| Element | Details |
|---|---|
| Score label | "Overall Group Data Quality Score" |
| Score display | Large number (e.g. "84") + "/100" + colour badge (≥ 80 green, 60–79 amber, < 60 red) |
| Progress bar | Full-width, colour-coded |
| Computation time | "Last computed: {datetime}" |
| Refresh trigger | `[Refresh]` button → `hx-get="/group/analytics/data-quality/score/"` `hx-target="#quality-score-banner"` |
| Auto-refresh | `hx-trigger="every 300s"` |

Score components (shown as a sub-row of 8 small tiles below the main score):
Completeness (30%) | Accuracy (25%) | Freshness (20%) | Consistency (15%) | Timeliness (10%).

Each component shows its weighted sub-score as a mini progress bar.

---

## 5. Division Quality Tiles

Eight tiles in a 2×4 grid (wraps to 2-col on tablet, 1-col on mobile).

| Tile | Division | Data Sources |
|---|---|---|
| Academic | Division B | Student records, class assignments, syllabus data |
| Exam | Division D | Exam schedules, result uploads, mark sheets |
| Finance | Division F | Fee records, payment uploads, concession data |
| Attendance | Division K | Daily attendance records, night roll call |
| Hostel | Division H | Occupancy records, welfare incident logs |
| HR / Staff | Division C | Staff profiles, attendance, payroll linkage |
| MIS / Reports | Division M (own) | Report submissions, distribution logs |
| Compliance | Cross-division | Regulatory submissions, audit trails |

**Each tile shows:**
- Division name + icon.
- Quality score: 0–100 (colour-coded progress bar).
- Critical issues count: red badge if > 0.
- Missing records count.
- Last data refresh timestamp.
- Click → opens Division Quality Detail drawer.

**Role 105 visibility:** only the "Exam" tile is visible. Other tiles are hidden via `{% if role in [102, 103, 104] %}` server-side template guard.

---

## 6. Filter Bar

| Control | Type | Options |
|---|---|---|
| Division | Select | All + division list (role-filtered; Role 105 sees Exam only) |
| Branch | Select | All + branches in group |
| Status | Select | All / Critical / Warning / Good |
| Date | Select | This Week / This Month / Last 3 Months / This Academic Year |

`[Apply]` triggers HTMX reload of `#quality-data-section` (branch table + trend chart + tickets table).

---

## 7. Branch Quality Table

### 7.1 Columns

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | Yes |
| Overall Score | Progress bar + number | Yes |
| Academic | Score badge | Yes |
| Exam | Score badge | Yes |
| Finance | Score badge | Yes |
| Attendance | Score badge | Yes |
| Hostel | Score badge | Yes |
| Status | Badge: Good / Warning / Critical | Yes |
| Critical Issues | Integer | Yes |
| Last Sync | Datetime | Yes |
| Actions | [View] | — |

### 7.2 Score Badges

| Score | Badge |
|---|---|
| ≥ 80 | `bg-green-100 text-green-800` |
| 60–79 | `bg-yellow-100 text-yellow-800` |
| < 60 | `bg-red-100 text-red-800` |

### 7.3 Controls

- Sort: HTMX header click.
- Pagination: 20 rows per page.
- Row click → Branch Quality Detail drawer.
- Overall score column is colour-coded by status.

---

## 8. Branch Quality Detail Drawer

**ID:** `branch-quality-detail-drawer`
**Width:** 640px
**Header:** `{Branch Name} — Data Quality`

### Tab 1 — Score Breakdown

| Section | Content |
|---|---|
| Overall Score | Large progress bar (0–100) with colour band |
| Dimension Scores | 5-row table: Dimension | Score | Weight | Weighted Contribution |
| Critical Issues | Expandable list of current critical quality issues |
| Warning Issues | Expandable list of warnings |

**Score Breakdown Chart:** Radar chart showing 5 quality dimensions. Canvas id: `branchQualityRadar`.

### Tab 2 — Issues Log

Table of specific data quality issues for this branch:

| Column | Notes |
|---|---|
| Issue Type | Badge: Missing / Stale / Duplicate / Invalid / Inconsistent |
| Division | Which division's data |
| Description | Short description |
| Affected Records | Count |
| Severity | Critical / Warning / Info |
| Detected Date | Date |
| Status | Open / In Remediation / Resolved |
| Actions | [Raise Ticket] (Role 103) |

Pagination: 10 rows per page.

### Tab 3 — Remediation History

List of all past remediation tickets for this branch:

| Column | Notes |
|---|---|
| Ticket Ref | e.g. DQ-2026-00112 |
| Issue Type | Badge |
| Raised By | Name |
| Status | Open / In Progress / Resolved / Closed |
| Raised Date | Date |
| Resolution Date | Date or — |
| [View] | Opens ticket detail |

---

## 9. Division Quality Detail Drawer

**ID:** `division-quality-detail-drawer`
**Width:** 680px
**Triggered by:** Clicking a division tile.
**Header:** `{Division Name} — Data Quality`

### Tab 1 — Metrics

| Metric | Value | Benchmark |
|---|---|---|
| Completeness % | {value} | ≥ 95% |
| Accuracy % | {value} | ≥ 98% |
| Freshness (avg data age hours) | {value} | ≤ 24h |
| Duplicate Record Rate | {value}% | ≤ 0.5% |
| Missing Required Fields | {count} records | 0 |
| Last Full Sync | Datetime | — |
| Last Partial Sync | Datetime | — |

Progress bars for each metric. Red if below benchmark.

### Tab 2 — Issue Breakdown by Branch

Heatmap-style table: Rows = branches, Cols = issue types (Missing / Stale / Duplicate / Invalid). Cell = issue count, colour-coded (0 = green, > 5 = red).

### Tab 3 — Quality Trend (this division)

Line chart showing this division's quality score over last 12 months. Canvas id: `divisionTrendChart`.

---

## 10. Quality Trend Chart (Main Page)

**Type:** Multi-line chart (Chart.js 4.x Line)
**Canvas ID:** `groupQualityTrendChart`
**Height:** 280px

- X-axis: Last 12 months.
- Y-axis: Quality score (0–100).
- Lines: Group Overall (thick black), Academic (blue), Exam (purple), Finance (green), Attendance (amber), Hostel (pink).
- Tooltip: `{Division}: {score} in {Month}`.
- Legend: bottom, scrollable if > 6 lines.
- Clicking a line filters to that division's issues in the branch table.

---

## 11. Remediation Tickets Table

### 11.1 Columns

| Column | Type | Sortable |
|---|---|---|
| Ticket Ref | Text | No |
| Branch | Text | Yes |
| Division | Badge | Yes |
| Issue Type | Badge | Yes |
| Description | Truncated 80 chars | No |
| Severity | Badge | Yes |
| Status | Badge | Yes |
| Raised By | Text | No |
| Raised Date | Date | Yes |
| Target Resolution | Date | Yes |
| Days Open | Integer | Yes |
| Actions | [View] [Close] (role-gated) | — |

### 11.2 Status Colour Codes

| Status | Badge |
|---|---|
| Open | `bg-red-100 text-red-800` |
| In Progress | `bg-amber-100 text-amber-800` |
| Resolved | `bg-green-100 text-green-800` |
| Closed | `bg-gray-100 text-gray-600` |

### 11.3 Controls

- Sort, search, pagination (20 rows per page).
- [Close] button: Role 103 own tickets → confirm modal → status → Closed.

---

## 12. Raise Remediation Ticket Drawer (Role 103)

**ID:** `remediation-ticket-drawer`
**Width:** 600px
**Triggered by:** `[+ Raise Ticket]` button or `[Raise Ticket]` in issue log.

| Field | Type | Validation |
|---|---|---|
| Ticket Ref | Auto-generated (read-only) | — |
| Branch | Select (branches in group) | Required |
| Division | Select (division list) | Required |
| Issue Type | Select: Missing Data / Stale Data / Duplicate Records / Invalid Values / Inconsistent Data / Sync Failure / Other | Required |
| Severity | Select: Critical / High / Medium / Low | Required |
| Description | Textarea (max 1000 chars) | Required, min 20 chars |
| Affected Records (estimated) | Number input | Optional |
| Assign To | Select (division head or data entry supervisor for that branch) | Required |
| Target Resolution Date | Date picker (min: today + 1 day) | Required |
| Supporting Evidence | Textarea (max 500 chars) | Optional |
| Notify via | Checkbox: In-app / Email | ≥ 1 required |

Submit: POST `/api/v1/analytics/data-quality/tickets/` → success toast → row prepended to ticket table.

---

## 13. View / Close Ticket Modal

**View:** Read-only version of raise-ticket form + resolution notes (if resolved).

**Close Ticket (Role 103 — own tickets):**
Adds a "Resolution Notes" textarea (required, min 20 chars) + "Confirmed resolved?" checkbox. PATCH `/api/v1/analytics/data-quality/tickets/{id}/close/` → status → Closed → toast.

---

## 14. Export

| Option | Endpoint | Notes |
|---|---|---|
| Export Branch Quality Table (CSV) | GET `/api/v1/analytics/data-quality/export/?format=csv` | With filters |
| Export Quality Report (PDF) | POST `/api/v1/analytics/data-quality/export/` | Async PDF |
| Export Tickets (CSV) | GET `/api/v1/analytics/data-quality/tickets/export/` | — |

PDF report includes: group score, dimension breakdown, branch quality table, trend chart snapshot, open tickets list.

---

## 15. Toast Notifications

| Trigger | Type | Message |
|---|---|---|
| Ticket raised | Success | "Remediation ticket {ref} raised for {Branch}." |
| Ticket closed | Success | "Ticket {ref} closed." |
| Form validation fail | Error | "Please fill in all required fields." |
| Score refreshed | Info | "Data quality scores refreshed." |
| Export started | Info | "Preparing export…" |
| Export ready | Success | "Export ready. Click to download." |
| Export failed | Error | "Export failed. Please try again." |
| Data load error | Error | "Failed to load quality data. Retrying in 30s." |

---

## 16. Empty States

| Context | Message | CTA |
|---|---|---|
| No issues found | "All data quality checks passed. No issues detected." with green checkmark | — |
| No tickets | "No remediation tickets raised yet." | "+ Raise Ticket" (Role 103) |
| No critical issues | "No critical data quality issues for the selected filters." | — |
| No branch data | "Data quality scores are not yet available for this branch." | — |

---

## 17. Loader States

| Element | Loader |
|---|---|
| Initial page load | Score banner shimmer + 8 tile shimmer + filter shimmer + table shimmer + chart placeholder |
| Division tiles refresh | 8 tile shimmer |
| Branch table reload | Table body shimmer (20 rows) |
| Drawer open | Spinner centred in drawer |
| Tab switch | Tab content shimmer |
| Trend chart load | Canvas grey overlay with spinner |
| Radar chart load | Canvas grey overlay with spinner |

---

## 18. HTMX Patterns

| Pattern | Target | Endpoint | Trigger |
|---|---|---|---|
| Score banner auto-refresh | `#quality-score-banner` | `/group/analytics/data-quality/score/` | `every 300s` |
| Division tiles auto-refresh | `#division-quality-tiles` | `/group/analytics/data-quality/tiles/` | `every 300s` |
| Data section reload | `#quality-data-section` | `/group/analytics/data-quality/data/` | Apply filter |
| Branch table search | `#branch-quality-tbody` | `/group/analytics/data-quality/branches/` | `keyup changed delay:300ms` |
| Branch table pagination | `#branch-quality-tbody` | `/group/analytics/data-quality/branches/?page={n}` | Page nav |
| Branch drawer open | `#branch-quality-detail-drawer` | `/group/analytics/data-quality/branches/{id}/detail/` | Row click |
| Division drawer open | `#division-quality-detail-drawer` | `/group/analytics/data-quality/divisions/{id}/detail/` | Tile click |
| Ticket table search | `#ticket-tbody` | `/group/analytics/data-quality/tickets/` | `keyup changed delay:300ms` |
| Ticket table pagination | `#ticket-tbody` | `/group/analytics/data-quality/tickets/?page={n}` | Page nav |
| Ticket POST | `#remediation-ticket-form` | `/api/v1/analytics/data-quality/tickets/` | Form submit |
| Ticket close PATCH | `#close-ticket-modal` | `/api/v1/analytics/data-quality/tickets/{id}/close/` | Modal confirm |
| Export poll | `#export-status` | `/api/v1/analytics/export-jobs/{id}/status/` | `every 5s` (stop on complete) |

---

## 19. API Endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | `/api/v1/analytics/data-quality/score/` | Group quality score | G1 |
| GET | `/api/v1/analytics/data-quality/tiles/` | Division tile data | G1 (role-filtered) |
| GET | `/api/v1/analytics/data-quality/branches/` | Branch quality table | G1 |
| GET | `/api/v1/analytics/data-quality/branches/{id}/detail/` | Branch detail | G1 |
| GET | `/api/v1/analytics/data-quality/divisions/{id}/detail/` | Division detail | G1 (role-filtered) |
| GET | `/api/v1/analytics/data-quality/charts/` | Trend chart data | G1 |
| GET | `/api/v1/analytics/data-quality/tickets/` | Ticket list | G1 |
| POST | `/api/v1/analytics/data-quality/tickets/` | Raise ticket | Role 103 |
| PATCH | `/api/v1/analytics/data-quality/tickets/{id}/close/` | Close ticket | Role 103 (own) |
| GET | `/api/v1/analytics/data-quality/export/` | CSV export | G1 |
| POST | `/api/v1/analytics/data-quality/export/` | Async PDF export | G1 |
| GET | `/api/v1/analytics/data-quality/tickets/export/` | Tickets CSV | G1 |
| GET | `/api/v1/analytics/export-jobs/{id}/status/` | Poll job | G1 |

---

## 20. Mobile (Flutter + Riverpod)

| Screen | Description |
|---|---|
| `DataQualityHomeScreen` | Group score banner + division tile cards (role-filtered) |
| `BranchQualityListScreen` | Sortable branch quality list with score badges |
| `BranchQualityDetailScreen` | Score breakdown per dimension (vertical layout) |
| `RemediationTicketListScreen` | Read-only ticket list with status badges |

No ticket creation on mobile. State: `dataQualityProvider` (Riverpod). Pull-to-refresh.

---

## 21. Accessibility & Responsiveness

- Group score progress bar has `aria-valuenow`, `aria-valuemin="0"`, `aria-valuemax="100"`, `aria-label="Overall Data Quality Score: {score}"`.
- Division tiles use `role="region"` with `aria-label="{Division} Data Quality"`.
- Score badges use colour + text — never colour alone.
- Branch table scrolls horizontally on mobile; essential columns (Branch, Score, Status) remain visible.
- Drawer: full-screen on mobile, `Escape` closes, focus trap active.
- Radar chart: `role="img"` with `aria-label="Branch quality radar chart showing 5 dimensions"`.
- All form fields: visible labels, `aria-required`, inline error messages.
