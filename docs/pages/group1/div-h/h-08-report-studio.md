# H-08 — Report Studio

> **Route:** `/analytics/report-studio/`
> **Division:** H — Data & Analytics
> **Primary Role:** Report Designer (46) — template creation and scheduling
> **Supporting Roles:** Analytics Manager (42) — approval and publishing; Data Analyst (44) — read + preview; Platform Admin (10) — full
> **File:** `h-08-report-studio.md`
> **Priority:** P2 — automated institution reports; critical for retention signalling and data democratisation

---

## 1. Page Name & Route

**Page Name:** Report Studio
**Route:** `/analytics/report-studio/`
**Part-load routes:**
- `/analytics/report-studio/?part=template-list` — report template library
- `/analytics/report-studio/?part=delivery-log` — recent delivery log
- `/analytics/report-studio/templates/{template_id}/?part=builder` — template builder (full-page editor)
- `/analytics/report-studio/templates/{template_id}/?part=preview` — report preview with sample data
- `/analytics/report-studio/deliveries/{delivery_id}/?part=detail` — delivery detail drawer

---

## 2. Purpose

H-08 is the **Report Designer's (46) workspace** for building institution-facing MIS reports and scheduling their automated delivery. Institutions are customers — giving them data about how their students are performing increases platform stickiness and gives them business value beyond just "running exams."

**Types of reports built in H-08:**
1. **Monthly Performance Summary** — sent to all institution admins on the 1st of each month. Shows: exam count, student attempts, avg score, pass rate, subject breakdown, comparison to platform avg.
2. **Quarterly Domain Report** — domain-specific coaching centres: SSC, RRB, NEET, JEE performance breakdown.
3. **Annual Learning Outcomes Report** — comprehensive yearly analysis for institutional leadership.
4. **Ad-hoc Intervention Report** — manually triggered for high-churn-risk institutions (requested by CSM or Analytics Manager).
5. **BGV Coverage Report** — for institutions needing to see their staff BGV status summary.

**Who needs this page:**
- Report Designer (46) — builds, tests, schedules all templates
- Analytics Manager (42) — approves templates before they go live; reviews delivery success rates
- Data Analyst (44) — read-only; reviews reports delivered to specific institutions for quality check

---

## 3. Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Page header: "Report Studio"   [+ New Template]                  │
├────────────────────────────────────────────────────────────────────┤
│  Tabs: [Template Library] [Delivery Log] [Schedule Overview]      │
├────────────────────────────────────────────────────────────────────┤
│  [Template Library tab — default]                                 │
│  Template Cards Grid (one card per template)                      │
│  ┌─────────────────────┐  ┌─────────────────────┐                 │
│  │ Monthly Performance │  │ Quarterly Domain    │                 │
│  │ PUBLISHED           │  │ DRAFT               │                 │
│  │ Monthly · 2,050 inst│  │ Quarterly · Coaching│                 │
│  │ Last sent: 1 Nov    │  │ Never sent          │                 │
│  │ [Edit] [Preview]    │  │ [Edit] [Preview]    │                 │
│  └─────────────────────┘  └─────────────────────┘                 │
└────────────────────────────────────────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Template Library Tab

**Filter bar:** [All] / [Published] / [Draft] / [Archived] status filter + [Institution Type] filter.

**Template cards:**

Each card shows:
- Template name
- Status badge: `PUBLISHED` (green) / `DRAFT` (amber) / `PENDING_APPROVAL` (blue, pulsing) / `DRAFT_WITH_FEEDBACK` (orange — Analytics Manager returned with comments) / `ARCHIVED` (grey). State transitions: DRAFT → PENDING_APPROVAL (via [Submit for Approval]) → PUBLISHED or DRAFT_WITH_FEEDBACK → DRAFT (Report Designer edits) → PENDING_APPROVAL again → eventually → ARCHIVED.
- Target audience: INSTITUTION_ADMIN / INTERNAL_EXEC / DIVISION_H_ONLY
- Institution types: ALL / SCHOOL / COLLEGE / COACHING
- Schedule: Monthly · 1st / Quarterly / Annual / Manual
- Output formats: PDF · CSV · XLSX icon badges
- Estimated recipient count: "{N} institutions match criteria"
- Last delivered: "{date}" or "Never"
- [Edit] — opens builder (Report Designer and Analytics Manager)
- [Preview] — renders template with sample data
- [Duplicate] — creates a copy as DRAFT
- [Archive] (Analytics Manager only) — moves to Archived state; stops scheduled delivery

**[+ New Template]** button → opens New Template Wizard (Section D).

---

### Section B — Template Builder (Full-Page Editor)

Opens when [Edit] is clicked on a template. This is a **section-based report builder** — not a free-form drag-and-drop (that would be too complex). Instead, it works with predefined "section types" that the Report Designer assembles in order.

**Builder layout:**
```
┌──────────────────────────────┬─────────────────────────────────────┐
│  SECTION PALETTE             │  REPORT CANVAS                      │
│  [+ KPI Bar]                 │  ┌───────────────────────────────┐  │
│  [+ Score Chart]             │  │  §1 — KPI Bar                │  │
│  [+ Subject Heatmap]         │  │  Metrics: Attempts, Avg Score │  │
│  [+ Cohort Table]            │  │  [Configure] [↑] [↓] [✕]    │  │
│  [+ Ranking Table]           │  ├───────────────────────────────┤  │
│  [+ Comparison Bar]          │  │  §2 — Score Distribution     │  │
│  [+ Trend Line]              │  │  Chart type: Line · 30 days   │  │
│  [+ Text Block]              │  │  [Configure] [↑] [↓] [✕]    │  │
│  [+ Page Break]              │  └───────────────────────────────┘  │
│                              │  [+ Add Section]                    │
├──────────────────────────────┴─────────────────────────────────────┤
│  [Preview with Sample Data]  [Save as Draft]  [Submit for Approval]│
└─────────────────────────────────────────────────────────────────────┘
```

**Available section types:**

| Section Type | Description | Config Options |
|---|---|---|
| KPI Bar | Row of metric tiles | Select metrics from list; choose period (MTD/last 30D/last 90D); number of tiles (2–8) |
| Score Distribution | Histogram of exam scores | Period; domain filter; bar colour |
| Subject Performance Heatmap | Subject × score band grid | Domain; top N subjects |
| Cohort Retention | Retention waterfall chart | Starting cohort period; dimension (institution type/domain) |
| Exam History Table | Table of institution's recent exams | Columns to show; number of rows (5–20); period |
| Domain Breakdown | Table comparing domains | Which domains; which metrics |
| Trend Chart | Line chart of any metric over time | Metric; period; show vs platform avg toggle |
| Ranking Table | Institution's rank vs peers | Metric (select: exam_attempts / avg_score / completion_rate / engagement_score); peer group definition: auto (same type + tier + region) or manual override (select: same region only / same tier only / national / custom state list); minimum peer group size = 5 (section shows "Insufficient peers" if < 5 institutions match the peer group definition) |
| Text Block | Static text / commentary | Markdown text; can reference template variables like `{institution_name}`, `{period}` |
| Page Break | Force new page in PDF output | Position in section list |
| BGV Summary | Staff BGV coverage snapshot for the recipient institution | Reads from `bgv_institution_compliance` table (Division G schema) — read-only. Shows: total staff count, verified count, pending count, flagged count, coverage %. Note: BGV data lag may be up to 24h (synced nightly). |

**Section configuration:**
Each section has a [Configure] button that opens a slide-out panel with the section's config options. Changes immediately reflected in the canvas preview.

**Template variables** (available in Text Blocks and section headers):
- `{institution_name}` — recipient institution name
- `{institution_type}` — School / College / Coaching
- `{period_start}` / `{period_end}` — reporting period dates
- `{generated_date}` — date report was generated
- `{platform_avg_score}` — platform average for comparison

**Section ordering:** [↑] [↓] arrows on each section. Drag-and-drop not required (arrow-based reordering is simpler and keyboard-accessible). Each section also has a [⊕ Duplicate] button — creates a copy of that section immediately below (useful for showing the same KPI bar for two different time periods).

**[Preview with Sample Data]:** Renders the report with realistic but synthetic sample data. Shows exactly how the report will look for a typical coaching centre. Opens in a new modal at full PDF dimensions (A4).

**[Save as Draft]:** Saves current builder state. Toast: "Draft saved."

**[Submit for Approval]:** Sends to Analytics Manager (42) for review. Status → PENDING_APPROVAL. Analytics Manager receives in-app notification: "Report template '{name}' submitted for approval by {designer_name}. [Review →]"

---

### Section C — Approval Workflow

**When status = PENDING_APPROVAL:**
- Analytics Manager (42) sees the template with an approval banner: "This template is awaiting your approval before it can be scheduled and delivered."
- Analytics Manager clicks [Preview] to review.
- [Approve & Publish] → status = PUBLISHED. Report Designer notified: "'{name}' approved and published by {manager_name}."
- [Request Changes] → opens comment textarea → status = `DRAFT_WITH_FEEDBACK`. Feedback stored in `analytics_report_template.feedback_note`. Report Designer notified: "'{name}' returned with feedback: '{note preview}'. [View feedback →]". When Report Designer opens the template, a yellow banner shows the feedback note prominently above the builder canvas. Template can be edited and re-submitted.

**Feedback loop:** Template can go through multiple DRAFT → PENDING_APPROVAL → DRAFT_WITH_FEEDBACK cycles. All feedback preserved in template history (Section G: Change Log tab in builder).

---

### Section D — New Template Wizard

Triggered by [+ New Template].

**Step 1 — Template Basics:**
| Field | Control | Notes |
|---|---|---|
| Template Name | Text (required) | Max 100 chars |
| Target Audience | Select: INSTITUTION_ADMIN / INTERNAL_EXEC / DIVISION_H_ONLY | Determines delivery channel |
| Institution Types | Multiselect: ALL / SCHOOL / COLLEGE / COACHING | — |
| Subscription Tiers | Multiselect: ALL / Starter–Enterprise | — |
| Output Formats | Multiselect: PDF / CSV / XLSX | PDF is always required; others optional |

**Step 2 — Schedule:**
| Field | Control | Notes |
|---|---|---|
| Schedule Type | Select: MANUAL / MONTHLY / QUARTERLY / ANNUAL | — |
| Delivery Day | Number 1–28 (if MONTHLY/QUARTERLY) | "Deliver on the {N}th of each month" |
| Reporting Period | Select: Previous month / Previous quarter / Custom offset | "Report covers the previous calendar month" |

**Step 3 — Template Builder:**
- Opens the full Section Builder (Section B) pre-seeded with 2 default sections (KPI Bar + Trend Chart) as a starting point
- Report Designer fills in all sections

**[Create Template]** → saves the template as DRAFT status, closes the wizard, and immediately opens the full Section Builder (Section B) for the newly created template. The wizard does not stay open alongside the builder. The URL transitions to `/analytics/report-studio/templates/{new_id}/?part=builder`.

---

### Section E — Delivery Log Tab

Shows all report deliveries (past and current). Source: `analytics_report_delivery`.

| Column | Sortable | Notes |
|---|---|---|
| Template | Yes | Template name + badge |
| Institution | Yes | Institution name |
| Type | No | SCHEDULED / MANUAL / TEST |
| Period | No | Report covers {start} to {end} |
| Format | No | PDF / CSV / XLSX badge |
| Status | Yes | PENDING · GENERATING · DELIVERED · FAILED |
| Delivered At | Yes (default: DESC) | Datetime |
| Actions | — | [Download] (if DELIVERED) · [Retry] (if FAILED) · [View Details →] |

**Filters:**
- Template (select)
- Institution (search)
- Status (multiselect)
- Date Range
- Delivery Type

**Summary strip above table:**
| Stat | Value |
|---|---|
| Delivered (this month) | {N} reports |
| Failed (this month) | {N} (red if > 0) |
| Pending | {N} |
| Scheduled for today | {N} |

**Delivery Detail Drawer (400px):**
- Delivery metadata (all columns from table)
- File size (`file_size_bytes` formatted as human-readable, e.g., "2.4 MB")
- Signed R2 download URL — [Download] button. If `download_url_expires_at < NOW()`: button replaced by [Regenerate Download Link] — generates a fresh 72h signed URL. Action logged to `analytics_audit_log` (action=`DOWNLOAD_LINK_REGENERATED`).
- Error message (if FAILED) — full error text including which template section caused failure
- Error type badge: `TRANSIENT` (safe to retry) / `DATA_ERROR` (fix template first) / `QUOTA_EXCEEDED` (contact Data Engineer)
- [Retry] — re-queues the report for generation. TRANSIENT errors: enabled immediately. DATA_ERROR: shows pre-flight warning "⚠ This failure is a data/template issue. Retrying without fixing the template will likely fail again. Continue?" QUOTA_EXCEEDED: button disabled.
- Timeline: PENDING → GENERATING (started at {time}) → DELIVERED/FAILED (completed at {time}, duration: {N}s)

---

### Section F — Schedule Overview Tab

**Purpose:** Shows the full calendar of upcoming scheduled report deliveries. Helps the Report Designer and Analytics Manager understand when institutions will receive reports and avoid clustering large batches.

**Calendar view:** Monthly calendar. Each day shows a badge with the number of reports scheduled for delivery on that day. Click a day → shows list of templates delivering that day + estimated recipient counts.

**Next 30 days summary table:**

| Date | Template | Recipient Count | Formats | Est. Generation Time |
|---|---|---|---|---|
| 1 Nov 2024 | Monthly Performance Summary | 2,050 | PDF, CSV | ~4 min |
| 1 Nov 2024 | Monthly Summary — Schools | 1,000 | PDF | ~2 min |
| 1 Dec 2024 | Quarterly Domain Report | 100 coaching | PDF | ~20 min |

**[Manual Send] button** on any scheduled delivery:
- Triggers a manual delivery of a published template to a specific institution or all matching institutions
- Used by Analytics Manager for ad-hoc intervention reports
- Opens modal: "Send '{template_name}' to: [Select institutions or 'All matching institutions']. Reporting period: [date range picker]. Format: [PDF/CSV/XLSX]"
- Confirmation: "Send {N} reports to {institutions}? This will immediately trigger report generation."

---

### Section G — Preview Modal

Opens from [Preview with Sample Data] in the builder or [Preview] on a template card.

**Sample data mode:** Uses synthetic data (a pre-seeded mock institution with realistic but non-real metrics). Shows the report exactly as it would appear to an institution admin.

**Institution preview mode:** Analytics Manager and Data Analyst can preview a published report for a specific real institution: [Preview for Institution] → institution search → renders report with that institution's actual data (uses last 30 days of pre-computed analytics).

**Preview output:**
- PDF: rendered as a paged document viewer (PDF.js embedded in modal). [Download] button.
- CSV: rendered as a table preview in modal. [Download CSV] button.
- XLSX: not previewable in browser — direct download only.

**Preview feedback:** [Report an Issue] button on the preview modal — opens a text field for the reviewer to flag problems with data accuracy or layout. Feedback creates a comment on the template that the Report Designer can see.

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | Report Designer (46), Analytics Manager (42), Data Analyst (44), Platform Admin (10) |
| [+ New Template] | Report Designer (46), Analytics Manager (42), Platform Admin (10) |
| Edit template builder | Report Designer (46), Analytics Manager (42), Platform Admin (10) |
| [Submit for Approval] | Report Designer (46) — sends to Analytics Manager |
| [Approve & Publish] | Analytics Manager (42), Platform Admin (10) only |
| [Request Changes] | Analytics Manager (42), Platform Admin (10) only |
| [Archive] template | Analytics Manager (42), Platform Admin (10) only |
| [Manual Send] | Analytics Manager (42), Platform Admin (10) only — Report Designer cannot trigger deliveries |
| [Retry] failed delivery | Analytics Manager (42), Report Designer (46), Platform Admin (10) |
| Data Analyst (44) | Read-only: template list, delivery log, previews for specific institutions. Cannot create or edit templates. |
| Delivery download | Analytics Manager (42), Report Designer (46), Data Analyst (44), Platform Admin (10) |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Template approved but no institutions match the filter criteria | [Approve & Publish] shows warning: "This template currently matches 0 institutions with the selected type/tier filters. It will be published but will not deliver to anyone until institutions match. Continue?" |
| Report generation fails for 1 of 2,050 institutions | That delivery record: status = FAILED. All others: DELIVERED. Delivery summary shows "2,049 delivered, 1 failed." [Retry Failed] button bulk-retries all FAILED deliveries for this template+run. |
| Report generation timeout (very complex template on large institutions) | Celery task hard timeout: 10 minutes per institution report. If exceeded: FAILED with error "Report generation timeout — institution data too large. Simplify template or contact Data Engineer." |
| Report Designer submits a template with no sections | Validation: "Template must have at least 1 section before submitting for approval." |
| Analytics Manager is unavailable (out of office) for approval | No automatic override. Platform Admin (10) can approve. Report Designer should contact Analytics Manager directly. |
| Institution has insufficient data for a section (e.g., KPI Bar with no exam attempts) | Section renders with "Insufficient data for this period" placeholder rather than showing 0 values or breaking the layout. Each section independently handles its empty state. |
| Scheduled delivery day falls on a weekend | Report delivers on the next business day (configurable: "Deliver on: {day} or next business day if weekend"). |
| `schedule_day` = 28–31 and current month is shorter (e.g., February with 28 days) | Report delivers on the last day of the month. Example: `schedule_day = 31`, February — delivers on 28 Feb (or 29 Feb in leap year). This is enforced by the `generate_scheduled_reports` Celery task using `min(schedule_day, last_day_of_month)`. |
| Download URL expired before institution accessed the report | R2 signed URL in notification email/in-app link expires after 72h, but the underlying R2 file is retained for the full `analytics_report_delivery` retention period (1 year). [Regenerate Download Link] creates a fresh 72h URL — the file itself is never deleted until the retention cleanup job runs. |
| PDF generation fails due to chart rendering error | Error message includes which section failed: "Report failed at section '{section_name}' — chart data error. [View Details]" in delivery drawer. |
| Template variable `{institution_name}` used but recipient is anonymous (internal report) | Variable renders as "Platform Overview" for INTERNAL_EXEC reports. `{institution_type}` renders as "All Institution Types". `{period_start}` / `{period_end}` render as actual date range. `{platform_avg_score}` renders as actual platform average. `{generated_date}` renders as actual generation date. All fallback values documented in template variable reference tooltip (hover the `{variable}` syntax in Text Block config). |

---

## 7. UI Patterns

### Loading States
- Template cards: 4-card skeleton grid
- Delivery log table: 10-row shimmer
- Builder canvas: 3-section skeleton
- Preview modal: full-page spinner with "Generating preview..." message
- Schedule calendar: calendar skeleton with grey day tiles

### Toasts
| Action | Toast |
|---|---|
| Template draft saved | ✅ "Draft saved" (2s) |
| Submitted for approval | ✅ "Template submitted — Analytics Manager notified" (4s) |
| Template approved | ✅ "'{name}' published — scheduled delivery is now active" (4s) |
| Manual send triggered | ✅ "{N} reports queued for generation — delivery log will update shortly" (4s) |
| Report delivery retry | ✅ "Retrying {N} failed delivery/deliveries" (3s) |
| Template archived | ⚠ "Template archived — scheduled delivery stopped" (4s) |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full builder with section palette + canvas side by side |
| Tablet | Builder: palette collapsed to button row at top; canvas full-width. Template cards 2-per-row. |
| Mobile | Builder not supported on mobile — "Report Builder requires desktop." Template list and delivery log accessible (read-only). |

---

*Page spec complete.*
*H-08 covers: template library (PUBLISHED / DRAFT / ARCHIVED cards) → section-based report builder (10 section types, variable support, A4 preview) → approval workflow (Designer → Analytics Manager) → 3-step new template wizard → delivery log with retry → schedule overview calendar → manual send for ad-hoc intervention reports → institution-specific preview with actual data.*
