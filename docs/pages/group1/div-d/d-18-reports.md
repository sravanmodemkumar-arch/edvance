# D-18 — Question Export & Content Reports

> **Route:** `/content/director/reports/`
> **Division:** D — Content & Academics
> **Primary Role:** Content Director (18) — full access
> **Limited Access:** Question Approver (29) — export actions only (no scheduled reports)
> **File:** `d-18-reports.md`
> **Priority:** P2 — Needed once content bank exceeds 1,000 published questions and management reporting begins
> **Status:** ⬜ Not started

---

## 1. Page Name & Route

**Page Name:** Question Export & Content Reports
**Route:** `/content/director/reports/`
**Part-load routes:**
- `/content/director/reports/?part=report-list` — scheduled and recent reports list
- `/content/director/reports/?part=export-builder` — ad-hoc export configuration panel
- `/content/director/reports/?part=scheduled-config` — scheduled report configuration
- `/content/director/reports/?part=report-status&batch_id={uuid}` — Celery export job status
- `/content/director/reports/?part=download-ready&batch_id={uuid}` — download link when ready

---

## 2. Purpose (Business Objective)

The Content Director is accountable to school principals, college academic coordinators, coaching center heads, and the platform's own management for the quality and volume of the question bank. D-18 provides the reporting and export infrastructure to support this accountability:

**Ad-hoc exports:** Director or Approver needs to export a filtered slice of the question bank — say, all Hard-difficulty Mathematics questions tagged SSC CGL that were published in the last 6 months — as a CSV for offline analysis or as a PDF for a management review meeting. D-11 handles single-question export via the drawer; D-18 handles bulk export with full filter control.

**Scheduled reports:** Management reporting should not require manual effort every month. D-18's scheduled report system runs configured reports automatically (nightly Celery beat) and deposits the output to a designated S3 path. The Director sees a report inbox with all recent and historical outputs.

**Coverage reports:** "We have 12,000 questions, but how many per subject? Are we covering all SSC CGL topics? How many Hard questions do we have in Mathematics vs the exam's requirement?" These are coverage gap reports — not analytics in the D-13 sense, but structured snapshots of the question bank's composition against the syllabus requirements.

**Production velocity reports:** "How many questions did we publish this quarter? What was our rejection rate? How does this month compare to the same month last year?" These are management-facing production metrics.

**DPDPA compliance:** No author identity (name, email, IP) appears in any export. All exports are role-label attributed. Export events are logged in D-12 audit history per question.

**Business goals:**
- Provide Director with ad-hoc export capability across the full question bank with fine-grained filters
- Automate monthly and weekly management reports via scheduled Celery jobs
- Generate structured coverage gap reports per subject, topic, and exam type
- Generate production velocity reports for management accountability
- Enforce DPDPA on all exports (no PII, no author identity)
- Provide Approver with export access limited to on-demand runs (no scheduled configuration)

---

## 3. User Roles

| Role | Access |
|---|---|
| Content Director (18) | Full — ad-hoc exports, scheduled report configuration, all report types |
| Question Approver (29) | Ad-hoc export only — can run an export with filters but cannot configure scheduled reports or view the Director's scheduled report inbox |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header

- H1: "Question Export & Content Reports"
- Tab navigation:
  - Ad-hoc Export
  - Scheduled Reports (Director only)
  - Coverage Reports
  - Production Velocity Reports
  - Export History

---

### Section 2 — Tab: Ad-hoc Export

**Purpose:** One-time filtered export of question bank data. The most commonly used feature on this page.

**Export Builder panel:**

**Step 1 — Select Data:**

| Filter | Options |
|---|---|
| Content Type | Questions · Questions + Explanations · Questions + Options + Explanations (full) · Metadata Only (no question text) |
| Subject | Multi-select (all subjects or specific) |
| Topic | Multi-select (filtered by selected subjects) |
| Exam Type | Multi-select |
| Difficulty | Easy · Medium · Hard · All |
| Access Level (G4) | Platform-Wide · Institution-Restricted · Group-Restricted · All |
| Source | Human-Authored · AI-Generated · AI-Edited · Bulk Import · All |
| State | Published only (default) · Published + Archived · Published + Amendment Review |
| Date Range | Published between: date picker pair |
| Content Type | Evergreen · Current Affairs · Time-Sensitive · All |
| Valid Until Status (G5) | All · Active only (not expired) · Expiring within 30 days |
| Exam Usage | Unused (never included in an exam) · Used · All |

**Exam-linked export guard:** Questions that are scheduled for inclusion in an upcoming exam (not yet sat) are blocked from export by default. A toggle: "Include questions scheduled for upcoming exams" — disabled by default, requires the Director to explicitly enable it. This prevents inadvertent paper leak via export.

**Step 2 — Select Format:**

| Format | Max Questions | Notes |
|---|---|---|
| CSV | 10,000 | Question metadata + content fields. Author identity excluded (ORM-level). |
| PDF — Question Paper Format | 500 | Formatted as a printable question paper (question body + options only, no explanations, no answer key). For review meetings. |
| PDF — Answer Key Format | 500 | Question body + options + correct answer + explanation. For internal review only. |
| XLSX | 5,000 | Same content as CSV but Excel-formatted with frozen header row. |

**Step 3 — Preview & Export:**

"Preview Filter Result" → `?part=export-builder` HTMX call → shows:
- Estimated question count matching filters
- Sample of first 5 rows (truncated — ID + Subject + Topic + Difficulty)
- Warnings:
  - "Export includes {N} questions scheduled for upcoming exams — confirm this is intentional" (if upcoming exam guard override is active)
  - "Export exceeds {format max} limit — only first {max} questions will be included, sorted by Published Date descending"

"Run Export" button → Celery async export job:
- `content_export_batch` record created
- HTMX polls `?part=report-status&batch_id={uuid}` every 3 seconds
- Progress bar with step: "Querying question bank… · Applying DPDPA filters… · Generating {format}… · Uploading to S3…"
- On completion: `?part=download-ready&batch_id={uuid}` → download button + expiry notice: "Download link expires in 24 hours."
- File stored in S3 `content-exports/` with private ACL — download via CloudFront signed URL (24h TTL)
- Per-question audit log entry: `content_question_audit_log · action: Exported · batch_id: {uuid}`

---

### Section 3 — Tab: Scheduled Reports (Director Only)

**Purpose:** Configure recurring reports that run automatically and land in the report inbox.

**Report Scheduler:**

"Create Scheduled Report" → configuration form:

| Field | Options |
|---|---|
| Report Name | Free text |
| Report Type | Coverage Gap Report · Production Velocity Report · SME Quality Summary · Reviewer Performance Summary · Expiry Monitor Report · Question Bank Snapshot |
| Frequency | Daily · Weekly (day of week picker) · Monthly (day of month picker) |
| Filters | Same filter set as Ad-hoc Export (subset relevant to report type) |
| Format | CSV · XLSX · PDF |
| S3 Destination | Auto: `content-scheduled-reports/{report_name}/{YYYY-MM-DD}/` |
| Active | Toggle — paused reports do not run but retain config |

**Scheduled Reports list:**

| Column | Description |
|---|---|
| Report Name | — |
| Report Type | — |
| Frequency | Daily · Weekly · Monthly |
| Last Run | Timestamp + status (✅ Success · ❌ Failed) |
| Next Run | Estimated next run time |
| Last Output Size | File size of most recent run |
| "Download Latest" | Direct download link to most recent S3 output |
| Actions | Edit · Pause · Delete |

**Report Inbox:**
Below the scheduler, a list of the 20 most recent report outputs (all scheduled reports combined):
- Report Name · Run Date · File Size · Download · Status

---

### Section 4 — Tab: Coverage Reports

**Purpose:** Structured snapshots of the question bank composition against syllabus requirements — the "do we have enough questions?" question, answered with data.

**Coverage Report types (Director selects and generates):**

**Report 1: Question Count by Subject/Topic**
- Table: Subject > Topic > Subtopic · Published Count · Archived Count · In Pipeline (DRAFT + UNDER_REVIEW + PENDING_APPROVAL) count
- Filter: Exam Type (shows counts only for questions tagged to selected exam type)
- Comparison: vs D-14 syllabus targets (questions_target from `content_syllabus_target`) — shows shortfall per topic
- Output: downloadable CSV or on-page rendered table

**Report 2: Difficulty Distribution**
- Per-subject: % Easy / Medium / Hard vs target ratios from D-14
- Per-exam-type: same
- Flag: topics where Hard question count < 10% of target (insufficient challenge depth)
- Output: CSV + visual bar chart on page

**Report 3: Coverage Gap Summary**
- Topics with zero published questions (complete gaps)
- Topics with < 5 questions (insufficient depth for exam rotation)
- Topics with questions that are all archived or expiring (effective gap)
- Grouped by subject and exam type
- Output: CSV for planning assignment

**Report 4: Pool Adequacy Report (G12)**
- Full Pool Adequacy snapshot from D-14: per exam type, concurrent exam count, questions per paper, safety factor, minimum pool required, actual pool, adequacy %
- Includes projected adequacy for next 30 / 60 / 90 days (based on current pipeline × expected publish rate from D-10 quotas)
- Output: PDF formatted for management presentation

**Report 5: Content Freshness Report (G5)**
- All published questions with a `valid_until` date: counts expiring within 30 / 60 / 90 days per subject per exam type
- Questions already expired but not archived: flagged in red
- Impact on pool adequacy: "If all questions expiring in 30 days are archived, {Subject} pool for {Exam Type} drops from {N} to {N} ({adequacy}% → {adequacy}%)"
- Output: CSV + on-page rendered table

All reports render inline (HTMX into the right content area) + offer a "Download as CSV/PDF" button.

---

### Section 5 — Tab: Production Velocity Reports

**Purpose:** Management-facing production metrics — volume, quality, and trend over time.

**Report 1: Monthly Production Summary**
Period selector: month/year.

| Metric | Value |
|---|---|
| Questions Published | {N} (vs target: {N} · {N}%) |
| Questions Returned to SME | {N} (return rate: {N}%) |
| Questions Unpublished Post-Publish | {N} (post-publish issue rate: {N}%) |
| Avg Days Draft to Publish | {N} days |
| AI Questions Accepted | {N} ({N}% of AI batch) |
| Notes Published | {N} |
| By Subject | Table: each subject's published count vs quota |

**Report 2: Quarter-over-Quarter Comparison**
Two period selectors (Q1 vs Q2, etc.) → side-by-side comparison of all Monthly Summary metrics. Variance columns (absolute + %).

**Report 3: SME Production Report**
Per-SME (role label), per-month:
- Questions authored vs quota
- Return rate
- Avg days draft to publish
- Published count vs all-time total

DPDPA: SME personal name never shown — role labels only.

**Report 4: Annual Content Bank Growth**
12-month chart: published question count by subject, stacked area chart. Shows how the bank has grown over the year and which subjects drove growth.

All production velocity reports are generated as on-page renders (HTMX) + downloadable CSV/PDF.

---

### Section 6 — Tab: Export History

**Purpose:** Audit trail of all export operations — both ad-hoc and scheduled — for DPDPA compliance and administrative accountability.

**Table:**

| Column | Description |
|---|---|
| Export ID | UUID — links to per-question audit log batch |
| Date / Time | — |
| Exported By | Role label (Content Director / Question Approver) — not personal name |
| Type | Ad-hoc · Scheduled (report name) |
| Format | CSV · PDF · XLSX |
| Question Count | Actual count exported |
| Filters Summary | Truncated filter description |
| Status | ✅ Completed · ⏳ In Progress · ❌ Failed |
| Download | Link (24h expiry for ad-hoc) · "Expired" if > 24h |

**Retention:** Export history records kept for 12 months. After 12 months, the `content_export_batch` record is retained (for audit continuity) but the S3 file is deleted (Celery cleanup task). The per-question audit log entries (`content_question_audit_log`) are INSERT-only and permanent.

**Search:** Free text search on Filters Summary + date range filter.

---

## 5. Data Models

### `content_export_batch`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `export_type` | varchar | AdHoc · Scheduled |
| `scheduled_report_id` | FK → content_scheduled_report | Nullable — for scheduled exports |
| `requested_by` | FK → auth.User | Director or Approver |
| `requested_at` | timestamptz | — |
| `filters` | jsonb | Complete filter config snapshot |
| `format` | varchar | CSV · PDF · XLSX |
| `question_count` | int | Actual count exported |
| `celery_task_id` | varchar | For progress polling |
| `status` | varchar | Pending · InProgress · Completed · Failed |
| `s3_key` | varchar | Nullable — set on completion |
| `signed_url_expires_at` | timestamptz | Nullable — 24h from generation |
| `completed_at` | timestamptz | Nullable |
| `error_message` | text | Nullable — for Failed status |

### `content_scheduled_report`
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `name` | varchar | Director-given name |
| `report_type` | varchar | CoverageGap · ProductionVelocity · SMEQuality · ReviewerPerformance · ExpiryMonitor · BankSnapshot · PoolAdequacy |
| `frequency` | varchar | Daily · Weekly · Monthly |
| `frequency_detail` | jsonb | `{day_of_week: 1}` or `{day_of_month: 1}` |
| `filters` | jsonb | Same structure as export_batch.filters |
| `format` | varchar | CSV · PDF · XLSX |
| `s3_destination_prefix` | varchar | Auto-generated |
| `is_active` | boolean | — |
| `created_by` | FK → auth.User | Director |
| `created_at` | timestamptz | — |
| `last_run_at` | timestamptz | Nullable |
| `last_run_status` | varchar | Nullable |
| `next_run_at` | timestamptz | Computed by Celery beat |

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | `PermissionRequiredMixin(permission='content.view_reports')` — Roles 18 + 29 |
| Ad-hoc export | Roles 18 + 29 |
| Scheduled Reports tab | Role 18 only — Approver receives 403 on `?part=scheduled-config` |
| Coverage Reports | Role 18 only |
| Production Velocity Reports | Role 18 only |
| Export History | Role 18 sees all history · Role 29 sees only their own exports (ORM-scoped: `requested_by = request.user`) |
| DPDPA enforcement | `content_question` ORM queries in export path explicitly exclude `author_id`, `author_name`, `author_email` fields at the serializer level — excluded before Celery task serialisation. Actor in audit log stored by FK but displayed as role title only. |
| Upcoming exam guard | Both roles: questions in upcoming unfinalised exams blocked from export by default. Override requires Director role (`permission='content.export_exam_questions'`). |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Ad-hoc export filter returns 0 questions | Preview shows "No questions match the selected filters." Export button disabled. |
| Export job exceeds format max (e.g. 12,000 questions for a 10,000-row CSV) | Preview warning shown before run. On run, first 10,000 questions (sorted Published Date descending) are included. Output file header row notes: "Truncated to 10,000 rows — apply narrower filters for a complete export." |
| Celery export job fails mid-run (S3 upload failure, OOM) | Status → Failed. Error message stored in `content_export_batch.error_message`. Director sees "Export failed — {error summary}. Please retry or contact your system administrator." Retry button re-queues the same job. |
| Scheduled report runs but generates 0 rows (e.g. Coverage Gap report when no gaps exist) | Report is generated as a 0-row file with header + a note: "No gaps found as of {date}." S3 file written as normal. Last Run Status = ✅ Success. This is intentional — a zero-gap report is a positive signal worth recording. |
| Director deletes a scheduled report while a run is in progress | Delete is blocked: "Cannot delete a report that is currently running. Wait for the current run to complete or cancel the Celery task from the system admin." Director can pause the report (stops future runs) immediately. |
| Download link expired (> 24h for ad-hoc) | "Re-download" button re-generates a new signed URL from the existing S3 file (file is not regenerated — only the signed URL is refreshed). S3 file is retained for 12 months regardless of signed URL expiry. If the S3 file has been deleted (> 12 months), the re-download button shows: "Export file has expired — please re-run the export." |
| Export includes questions in AMENDMENT_REVIEW state (if Director explicitly selects this state in filters) | These questions are included in the export with a warning column: `amendment_status: UnderReview`. The export note (CSV header comment) includes: "Some questions in this export are currently under amendment review and may be modified or archived." |

---

## 8. Integration Points

| Integration | Direction | What Flows | Mechanism |
|---|---|---|---|
| D-11 Published Bank | D-11 → D-18 | D-11's drawer Export button routes to D-18 Ad-hoc Export pre-filled with the question's filters (single question export uses D-11; bulk export uses D-18) | URL parameter: `/content/director/reports/?prefill_question={uuid}` |
| D-12 Audit History | D-18 → D-12 | Every export event generates a per-question audit log entry | `content_question_audit_log` INSERT (Celery task writes audit entries for all exported question IDs) |
| D-14 Syllabus Coverage | D-14 → D-18 | Pool Adequacy data + syllabus targets used in Coverage Reports | `content_pool_adequacy_cache` + `content_syllabus_target` ORM read |
| D-13 Quality Analytics | D-13 → D-18 | Quality metrics (return rate, post-publish issue rate) sourced for Production Velocity Reports | `content_question_review_log` + `content_question_audit_log` aggregated reads |
| Div F (S3) | D-18 → S3 | Export files stored in `content-exports/` with private ACL | Celery upload via boto3 to ap-south-1 S3 bucket |
| Celery Beat | D-18 → Celery | Scheduled reports trigger nightly/weekly/monthly export jobs | `content_scheduled_report.next_run_at` polled by Celery beat scheduler |

---

---

## 9. UI Patterns & Page-Specific Interactions

### Search
- **Export History tab:** Placeholder "Search exports by filter summary or date…". Searches: filters_summary field, requested_by role label, format. Debounced 300ms.
- **Scheduled Reports list:** Placeholder "Search scheduled reports…". Searches: report name, report type label.
- **Coverage/Production reports (inline):** Placeholder "Filter topics or subjects…" within each report's filter panel. Searches: topic name, subject name.

### Sortable Columns — Export History Table
| Column | Default Sort |
|---|---|
| Date / Time | **DESC (most recent first)** — default |
| Question Count | DESC |
| Format | ASC |
| Status | Custom: In Progress → Failed → Completed |

### Sortable Columns — Scheduled Reports Table
| Column | Default Sort |
|---|---|
| Next Run | **ASC (soonest next run first)** — default |
| Last Run | DESC |
| Report Name | ASC |
| Frequency | Custom: Daily → Weekly → Monthly |

### Sortable Columns — Report Inbox (recent outputs)
Default sort: **Run Date DESC** (newest output first).

### Pagination
- Export History: 50 rows, numbered controls.
- Scheduled Reports list: 25 rows, numbered controls.
- Report Inbox: 20 rows (last 20 outputs by default — "Show older" button appends more).

### Empty States
| Tab / Section | Heading | Subtext | CTA |
|---|---|---|---|
| Ad-hoc Export — zero results preview | "No questions match these filters" | "Try broadening your subject, topic, or date range filters." | — |
| Scheduled Reports — none | "No scheduled reports" | "Create a scheduled report to receive automated exports on a regular cadence." | "Create Scheduled Report" |
| Report Inbox — no outputs | "No reports generated yet" | "Scheduled reports will appear here after their first run." | — |
| Export History — none | "No exports yet" | "Ad-hoc and scheduled export records will appear here." | — |
| Coverage Gap report — no gaps | "No coverage gaps found" | "All topics meet their configured question targets as of {date}." | — |

### Toast Messages
| Action | Toast |
|---|---|
| Ad-hoc export started | ℹ "Export started — generating your {format} file…" (Info 6s) |
| Export ready (Celery complete) | ✅ "Export ready — [Download now]" (Success persistent — stays until clicked or manually dismissed) |
| Export failed | ❌ "Export failed — {reason}. [Retry]" (Error persistent) |
| Scheduled report created | ✅ "Scheduled report '{name}' created — first run {next_run_at}" (Success 4s) |
| Scheduled report paused | ✅ "Report paused — no further runs until reactivated" (Success 4s) |
| Scheduled report deleted | ✅ "Report deleted" (Success 4s) |
| Scheduled report delete blocked (running) | ❌ "Cannot delete a report that is currently running — pause it first" (Error persistent) |
| Coverage report generated | ✅ "Coverage report generated" (Success 4s — inline render) |
| Re-download signed URL refreshed | ✅ "Download link refreshed — expires in 24 hours" (Success 4s) |

### Loading States
- Ad-hoc Export preview ("Preview Filter Result"): spinner on the "Preview" button while HTMX fetches the count and sample rows. Sample rows replace spinner on load.
- Export generation progress: step-by-step progress bar ("Querying question bank… → Applying DPDPA filters… → Generating {format}… → Uploading to S3…"). Each step checkmarks when complete.
- Coverage / Production reports (inline): chart-area shimmer + table skeleton while report data loads. These are ORM aggregations — expect 3–8s. Timeout > 10s: "Report is taking longer than expected. [Retry]".
- Scheduled Reports list: 6-row skeleton on page load.
- Export History: 8-row skeleton on tab open.

### Responsive Behaviour
| Breakpoint | Behaviour |
|---|---|
| Desktop | Ad-hoc export builder takes 50% width left pane; preview/progress right 50%. Tabs full width. |
| Tablet | Export builder: full width stacked (filters above, preview below). Scheduled Reports: report name + next run + status + actions. Export History: date, format, count, status, download. |
| Mobile | Export builder: full-width single column. All filter dropdowns are native mobile pickers. Tab nav: horizontal scroll. Export History: date + format + download icon — others in row expand. Scheduled Reports: report name + status badge + action menu (kebab). |

### Ad-hoc Export Builder — Form Validation
| Field | Validation |
|---|---|
| Subject | At least 1 required unless "All Subjects" toggle is on |
| Date range (Published Between) | From must be ≤ To |
| Format | Required (cannot run export without selecting format) |
| Upcoming exam guard override | Requires explicit toggle acknowledgement — a separate confirm checkbox: "I understand these questions are scheduled for upcoming exams" |

"Preview Filter Result" button disabled until at least one filter is selected (prevents accidental full-bank queries). "Run Export" button disabled until preview has been run (prevents blind large exports).

### Scheduled Report — Create/Edit Modal
- 480px center modal (desktop) / full-width (mobile).
- Fields: Report Name (required) · Report Type (dropdown) · Frequency (radio: Daily / Weekly / Monthly) · Day selector (appears when Weekly or Monthly is selected) · Format (dropdown) · Filters (subject multi-select, date range).
- "Save" button disabled until Report Name and Report Type are filled.
- Edit: same modal pre-filled. Saving edit does not trigger an immediate run.

### Charts (Coverage and Production Reports)
- **Coverage Gap report:** Per exam type, per subject — horizontal bar chart (published vs target). Sorted by coverage % ASC. Same colour coding as D-14.
- **Difficulty Distribution report:** Stacked bar chart per subject — Easy/Medium/Hard vs target ratios.
- **Production Velocity — Monthly Summary:** Grouped bar chart — Published / Returned / Rejected / AI Accepted per month.
- **Production Velocity — Quarter-over-Quarter:** Side-by-side bar chart, current quarter vs prior quarter.
- **Annual Content Bank Growth:** Stacked area chart — cumulative published question count by subject, 12 months.
- All charts: PNG download + CSV data download (top-right icon menu per chart).

### Role-Based UI
- Ad-hoc export: Director (18) and Approver (29).
- Scheduled Reports tab: Director only. Approver receives 403 on `?part=scheduled-config` — tab not rendered in Approver's HTML.
- Coverage Reports tab: Director only.
- Production Velocity Reports tab: Director only.
- Export History: Director sees all exports. Approver sees own exports only (ORM-scoped: `requested_by = request.user`).
- Upcoming exam guard override toggle: Director only. Approver cannot override the export block (DPDPA + exam secrecy constraint).

---

*Page spec complete.*
*Division D — Content & Academics: all 18 page specs complete (D-01 through D-18).*
*Amendments applied: G2 (post-publish amendment flow), G3 (Director notes review toggle), G4 (access level management), G5 (content expiry), G6 (difficulty calibration from exam data), G7 (committee review), G8 (emergency bulk unpublish), G9 (passage/linked question sets), G10 (bulk taxonomy retag), G11 (director announcements), G12 (pool adequacy monitoring)*
