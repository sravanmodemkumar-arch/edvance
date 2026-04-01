# H-09 — Export Manager

> **Route:** `/analytics/exports/`
> **Division:** H — Data & Analytics
> **Primary Role:** All Division H roles — self-serve data export management
> **Supporting Roles:** Platform Admin (10) — full
> **File:** `h-09-export-manager.md`
> **Priority:** P2 — self-serve export reduces dependency on Data Engineer for raw data requests

---

## 1. Page Name & Route

**Page Name:** Export Manager
**Route:** `/analytics/exports/`
**Part-load routes:**
- `/analytics/exports/?part=export-list` — all export requests for current user
- `/analytics/exports/?part=new-export` — new export request form
- `/analytics/exports/{export_id}/?part=detail` — export detail drawer

---

## 2. Purpose

H-09 is the **self-serve data export centre** for all Division H roles. Instead of asking a Data Engineer to run an ad-hoc query and email a spreadsheet, any Division H role can request structured exports from the pre-aggregated analytics schema. Exports are processed asynchronously by the `process_export_request` Celery task (Queue: `exports`) and made available as downloadable CSV/XLSX files via R2 signed URLs (48h expiry).

**Export types available:**
1. **Question Stats Export** — CTT metrics for all questions matching filters (domain/subject/topic/quality flag)
2. **Institution Engagement Export** — engagement scores, churn risk, exam frequency for all institutions matching filters
3. **Student Cohort Export** — cohort retention data by dimension (domain/type/region)
4. **Exam Performance Export** — exam-level performance data (matching H-05 filter state)
5. **AI Batch Summary Export** — batch-level AI generation stats (AI Gen Manager only)
6. **Daily Metrics Export** — `analytics_daily_snapshot` raw data for custom analysis (Data Engineer only)

**Who needs this page:**
- Data Analyst (44) — primary user; requests exports for offline analysis and reporting
- Analytics Manager (42) — exports for stakeholder decks and leadership briefs
- AI Generation Manager (45) — AI Batch Summary exports for cost/quality reporting
- Report Designer (46) — exports to verify data before building report templates
- Data Engineer (43) — Daily Metrics Export for deep-dive investigations

---

## 3. Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Page header: "Export Manager"   [+ New Export Request]           │
├────────────────────────────────────────────────────────────────────┤
│  My Exports (current user's requests — server-side paginated)     │
│  Summary strip: {N} ready · {M} processing · {K} expired          │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ Export Type | Filters | Format | Status | Rows | Created   │  │
│  │ Question Stats | SSC·Math | CSV | ✅ READY | 12,400 | Nov 1│  │
│  │ Institution Eng. | All | XLSX | ⏳ PROCESSING | — | Nov 1  │  │
│  │ AI Batch Summary | Oct | CSV | ⌛ EXPIRED | 840 | Oct 15   │  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Export List

**Summary strip (above table):**
| Stat | Value |
|---|---|
| Ready to download | {N} (green) |
| Processing | {M} (blue, pulsing if any) |
| Expired (link gone) | {K} (grey) — [Re-request Available] |
| Failed | {L} (red if > 0) |

**Export table — all current user's requests:**

| Column | Sortable | Notes |
|---|---|---|
| Export Type | Yes | Badge: QUESTION_STATS · INSTITUTION_ENGAGEMENT · STUDENT_COHORT · EXAM_PERFORMANCE · AI_BATCH_SUMMARY · DAILY_METRICS |
| Filter Summary | No | Human-readable description: "SSC, Mathematics, Oct 2024" |
| Format | No | CSV / XLSX badge |
| Status | Yes | `QUEUED` (grey) · `PROCESSING` (blue) · `READY` (green) · `EXPIRED` (grey strikethrough) · `FAILED` (red) |
| Rows | Yes | Integer — populated when READY; "—" otherwise |
| File Size | No | Human-readable (e.g., "3.2 MB") — populated when READY |
| Created | Yes (default: DESC) | Relative timestamp ("2 hours ago") |
| Expires At | No | Countdown: "Expires in 41h" (amber if < 4h); "Expired" (grey) |
| Actions | — | [Download] (if READY and not expired) · [Re-request] (if EXPIRED or FAILED) · [Cancel] (if QUEUED) · [View →] opens detail drawer |

**[Re-request]:** Creates a new `analytics_export_request` with the same parameters. Previous expired/failed record remains in history. The new request appears at the top of the table immediately with `QUEUED` status.

**Access note:** Users only see their own export requests. Platform Admin (10) and Analytics Manager (42) can see exports from all Division H users via an [All Users] toggle. Data Engineer (43) can see all exports (needed for investigating processing failures).

---

### Section B — New Export Request Form

Triggered by [+ New Export Request]. Opens as a right-side drawer (600px) or full-width panel on desktop.

**Step 1 — Export Type:**

| Export Type | Available To | Description |
|---|---|---|
| Question Stats | 42, 43, 44, 10 | CTT metrics per question from `analytics_question_stats` |
| Institution Engagement | 42, 44, 10 | Engagement scores from `analytics_institution_engagement` latest snapshot |
| Student Cohort | 42, 44, 10 | Cohort retention data from `analytics_cohort_snapshot` |
| Exam Performance | 42, 44, 10 | Exam-level stats from `analytics_daily_snapshot` |
| AI Batch Summary | 45, 42, 10 | Batch-level AI generation stats from `analytics_ai_batch` |
| Daily Metrics Raw | 43, 10 | Raw `analytics_daily_snapshot` data for custom analysis |

**Step 2 — Filters (depend on export type):**

**Question Stats filters:**
| Filter | Control |
|---|---|
| Domain | Multiselect |
| Subject | Multiselect (cascades) |
| Topic | Text search |
| Quality Flag | Multiselect |
| Min Attempts | Number (default: 30) |
| Date range (last_used_at) | Date range picker |

**Institution Engagement filters:**
| Filter | Control |
|---|---|
| Institution Type | Multiselect |
| Subscription Tier | Multiselect |
| Region / State | Multiselect |
| Churn Risk | Multiselect |
| Engagement Score Range | Range slider (0–100) |

**Student Cohort filters:**
| Filter | Control |
|---|---|
| Cohort Month Range | Date range (month picker) |
| Dimension | Select: exam_domain / institution_type / region_state / none |

**Exam Performance filters:**
| Filter | Control |
|---|---|
| Period | Date range |
| Domain | Multiselect |
| Exam Type | Multiselect |
| Institution Type | Multiselect |

**AI Batch Summary filters:**
| Filter | Control |
|---|---|
| Date Range (created_at) | Date range |
| Domain | Multiselect |
| Status | Multiselect |
| Model Config | Multiselect |

**Daily Metrics Raw filters (Data Engineer only):**
| Filter | Control |
|---|---|
| Date Range (snapshot_date) | Date range. Max range: 90 days per export (larger ranges should be split) |
| Metric Key | Multiselect (all keys or specific) |
| Dimension Type | Multiselect |

**Step 3 — Output Format:**

| Format | Notes |
|---|---|
| CSV | Flat file, UTF-8 encoded, comma-separated. All formats produce same data. |
| XLSX | Excel-compatible, one sheet per export type. Column headers as first row. |

**Estimated row count preview:** After filters are set, shows "Estimated rows: ~{N}" (rough estimate from index stats). If estimated > 500,000 rows: warning "Very large export (~{N} rows). Generation may take 5–15 min. Consider narrowing filters." If estimated > 2,000,000 rows: hard warning + confirmation required.

**[Submit Export Request]:**
- Creates `analytics_export_request` record
- Triggers `process_export_request` Celery task immediately
- Drawer/panel closes with toast: "Export queued — you'll be notified when ready (est. {N} min)"
- New row appears at top of export list with QUEUED status

---

### Section C — Export Detail Drawer

Triggered by [View →] on any export row. 460px right drawer.

**Header:** Export type badge · Format badge · Status badge · Created at

**Filters applied:** Human-readable summary of all filters at request time:
```
Domain: SSC, RRB
Subject: Mathematics
Quality Flag: POOR_DISCRIMINATION, NEGATIVE_D
Min Attempts: 30
Date Range: Oct 1 – Oct 31 2024
```

**Result metrics (when READY):**
| Metric | Value |
|---|---|
| Rows exported | {N} |
| File size | {MB} |
| Processing time | {N} seconds |
| Generated at | {timestamp} |
| Download link expires | {datetime} (countdown) |

**[Download]** — triggers R2 signed URL download. Logged to `analytics_audit_log` (action=`EXPORT_DOWNLOADED`).

**[Regenerate Download Link]** — if expired (`expires_at < NOW()`): generates a fresh 48h signed URL. Logged in audit log (action=`DOWNLOAD_LINK_REGENERATED`).

**Error details (if FAILED):**
```
Error: Query exceeded memory limit during XLSX generation.
Suggestion: Try CSV format (lower memory) or narrow your filters.
```
[Re-request with Same Filters] — one-click re-request.

**Timeline:** QUEUED → PROCESSING (started at {time}) → READY/FAILED (completed at {time}, duration: {N}s)

---

### Section D — Shared Exports (Analytics Manager View)

Analytics Manager (42) and Platform Admin (10) see an additional tab: **[All Users' Exports]** toggle.

When toggled: table shows all Division H users' exports, with an added `Requested By` column.

**Use cases:**
- Analytics Manager reviews what exports Data Analysts are running (data governance)
- Platform Admin investigates large exports that may be impacting `exports` queue performance
- Data Engineer troubleshoots why an export failed for a specific user

**[Cancel] in All Users view:** Analytics Manager and Platform Admin can cancel any QUEUED export (not just their own). Used when a very large export is consuming queue capacity needed for pipeline tasks.

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | All Division H roles (42, 43, 44, 45, 46), Platform Admin (10) |
| View own exports | All permitted roles |
| View all users' exports | Analytics Manager (42), Data Engineer (43), Platform Admin (10) |
| Create export — Question Stats | 42, 43, 44, 10 |
| Create export — Institution Engagement | 42, 44, 10 |
| Create export — Student Cohort | 42, 44, 10 |
| Create export — Exam Performance | 42, 44, 10 |
| Create export — AI Batch Summary | 45, 42, 10 |
| Create export — Daily Metrics Raw | 43, 10 only — too large/raw for analyst use |
| Cancel own export (QUEUED) | All permitted roles |
| Cancel any export (QUEUED) | Analytics Manager (42), Platform Admin (10) |
| [Regenerate Download Link] | All permitted roles (own exports); Analytics Manager / Platform Admin (any export) |
| DPDPA minimum enforcement | All exports respect 30-student cohort minimum at query time; export request is rejected (not just filtered) if the result set has < 30 students in any cohort dimension |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Export result has 0 rows | Status → READY with `row_count = 0`. Download still available (empty file with headers). Toast: "Export ready — 0 rows matched your filters. Consider broadening criteria." |
| Export processing time > 15 minutes | Celery task hard timeout at 15 min. Status → FAILED with error: "Export timed out. Try narrowing filters or splitting into smaller date ranges." |
| Export request submitted during active nightly pipeline run | Allowed. Export reads from analytics schema (already written rows) — will reflect data as of last completed pipeline run. Export timestamp shows "Data as of: {last_computed_at}". |
| User has > 50 exports in history | Old EXPIRED/FAILED exports beyond the 50-record display limit are soft-deleted from the list (still in DB). Info banner: "Showing 50 most recent exports. Older exports have been removed from this view." |
| Two identical exports requested within 60 seconds | Warning on submit: "You already have an identical export request processing. Are you sure you want to create another?" [Cancel] or [Create Anyway]. |
| XLSX generation fails due to memory (very large export) | Specific error: "XLSX generation failed — file would exceed 100MB memory limit. Try CSV format instead (lower memory usage) or narrow your filters." [Re-request as CSV] shortcut button. |
| Download link expired before user could download | Link shows "Expired" in table. [Regenerate Download Link] creates a new 48h URL. The underlying R2 file is retained until `analytics_export_request.expires_at + 7 days` before cleanup. |
| Data Engineer exports > 2M rows (Daily Metrics Raw) | Pre-submission warning: "Large export ({N}M rows). This will consume significant `exports` queue capacity. Consider splitting into 30-day chunks. Continue?" Confirmation required. |

---

## 7. UI Patterns

### Loading States
- Export list: 10-row shimmer
- Summary strip: 4-tile shimmer
- New export form filters: skeleton per filter row
- Detail drawer: header shimmer + metrics table skeleton

### Toasts
| Action | Toast |
|---|---|
| Export queued | ✅ "Export queued — you'll be notified when ready (est. {N} min)" (4s) |
| Export ready (notification) | ✅ "Export ready: {type} — [Download] · Expires in 48h" (persistent until dismissed) |
| Export cancelled | ✅ "Export request cancelled" (3s) |
| Export re-requested | ✅ "New export request created with same filters" (3s) |
| Download link regenerated | ✅ "New download link valid for 48h" (4s) |

### Notifications
When a user's export transitions to READY or FAILED, an in-app notification is sent (via F-06 notification hub):
- READY: "Your {type} export is ready. Download within 48h. [Download →]"
- FAILED: "Your {type} export failed: {error_summary}. [Re-request →]"

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full layout with side-by-side form and list |
| Tablet | New export form: full-width panel. Table: 5 visible columns (Type, Status, Rows, Expires, Actions). |
| Mobile | Export list readable (card view). New export form accessible but filter complexity may be limited. [+ New Export Request] button always visible. |

---

*Page spec complete.*
*H-09 covers: self-serve export request creation (6 export types with role-based availability) → async processing via Celery `exports` queue → export list with READY/PROCESSING/EXPIRED/FAILED states → download management (48h R2 signed URLs with regeneration) → detail drawer with filter summary + error diagnosis → shared exports view for Analytics Manager oversight → DPDPA 30-student minimum enforcement at export query time.*
