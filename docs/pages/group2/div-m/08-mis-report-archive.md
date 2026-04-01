# 08 — MIS Report Archive

> **URL:** `/group/mis/archive/`
> **File:** `08-mis-report-archive.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Role 102 (Group Analytics Director), Role 103 (Group MIS Officer), Role 104 (Group Academic Data Analyst), Role 105 (Group Exam Analytics Officer), Role 106 (Group Hostel Analytics Officer), Role 107 (Group Strategic Planning Officer)

---

## 1. Purpose

The MIS Report Archive is the permanent, searchable record of every management information report ever generated for the group across all academic years. It serves as the organisation's compliance record for management reporting, providing verifiable proof that reports were dispatched to the Chairman and Board at the required intervals. The MIS Officer (Role 103) and Analytics Director (Role 102) can retrieve any historical report, re-send it to original or updated recipients, download original files, and in rare cases delete erroneous records. Every generated report retains full metadata — the generating user, the time of generation, the date range covered, which sections were included, which branches were in scope, who received it, when, and how many recipients downloaded or opened the report. All other Division M roles may browse and view the archive but may not take any action. Senior governance roles (G4/G5) who have been explicitly granted cross-division read access via the governance module may also view the archive without modification rights.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Analytics Director | 102 | G1 | View, download, re-send, filter | Cannot delete |
| Group MIS Officer | 103 | G1 | Full — view, download, re-send, delete | Primary manager of archive |
| Group Academic Data Analyst | 104 | G1 | View and download only | Read-only |
| Group Exam Analytics Officer | 105 | G1 | View and download only | Read-only |
| Group Hostel Analytics Officer | 106 | G1 | View and download only | Read-only |
| Group Strategic Planning Officer | 107 | G1 | View and download only | Read-only |
| Senior governance roles (G4/G5) | — | G4/G5 | View and download only (if cross-division read granted) | Via governance module permission |

**Access enforcement note:** The delete action and re-send action are server-side guarded. Delete is restricted to Role 103. Re-send is restricted to Roles 102 and 103. All download links are signed Cloudflare R2 pre-signed URLs that expire in 15 minutes; they are generated on demand rather than stored as permanent public links.

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Dashboard > Analytics & MIS > MIS Report Archive
```

### 3.2 Page Header

- **Title:** `MIS Report Archive`
- **Subtitle:** `Complete history of all generated MIS and Board reports across all academic years`
- **Header actions (Role 103 only):** [Delete Selected] bulk action button (shown only when rows are checked)
- **Header actions (Roles 102–103):** [Re-send Selected] bulk action button (shown only when rows are checked)
- **Header actions (all roles):** [Export Archive Index] button — downloads a CSV listing of all report metadata (not the report files themselves)

### 3.3 Alert Banners (conditional, each individually dismissible)

| Condition | Colour | Message |
|---|---|---|
| Any report generated in the last 30 days has zero distribution events (never sent) | Amber | "Some recently generated reports have not been sent to any recipients. Review distribution." with [View Unsent] CTA |
| Archive contains reports older than 5 years (approaching auto-archival policy threshold) | Blue | "Reports older than 5 years are flagged for archival review per your data retention policy." with [Review] CTA |

---

## 4. KPI Summary Bar

| KPI | Description | Format |
|---|---|---|
| Total Reports Archived | Count of all reports in archive (all time) | Integer |
| Reports This Academic Year | Count of reports generated in current AY | Integer |
| Reports Never Sent | Count of reports with no distribution event | Integer, amber if > 0 |
| Unique Report Types | Count of distinct report types in archive | Integer |
| Total Recipients (All Time) | Distinct recipient email addresses across all reports | Integer |
| Oldest Report | Date of earliest archived report | Date string |

KPI cards are horizontally scrollable on mobile. Data fetched from `/api/v1/mis/archive/kpis/` on page load with skeleton loader during fetch.

---

## 5. Sections

### 5.1 Report Archive Table

The primary table listing every generated report in the archive.

**Table columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Checkbox | Checkbox | No | Bulk select; select-all in header |
| Report Name | Text link | Yes | Opens `report-detail` drawer |
| Type | Badge | Yes | Monthly MIS (blue), Board Report (purple), Custom (grey) |
| Academic Year | Text | Yes | Format: 2025-26 |
| Period | Text | Yes | Month name (e.g. "January 2026") or quarter (e.g. "Q3 2025-26") |
| Generated By | Text | No | User display name; "(Auto)" suffix for scheduled jobs |
| Generated At | Datetime | Yes | Display: "DD MMM YYYY HH:mm"; relative on hover |
| Branches Covered | Text | No | "All Branches" or count e.g. "12 of 18 branches" |
| Format | Badge | No | PDF (green), XLSX (blue), Both (purple) |
| Status | Badge | Yes | Sent (green), Portal Only (blue), Failed (red) |
| Recipients | Number | No | Count of configured recipients at time of dispatch |
| Actions | Button group | No | [View] (all roles), [Download] (all roles), [Re-send] (Roles 102–103), [Delete] (Role 103) |

**Table behaviour:**
- Default sort: Generated At DESC
- Rows per page: 10 / 25 / 50 / All (default 25)
- Clicking the Report Name cell opens the `report-detail` drawer
- Row hover highlights with light blue background
- Failed status rows have a light red row tint
- On mobile (<768px): card layout showing Report Name, Type badge, Period, Generated At, Status badge, and an action menu ("...")

**Search:** Full-text search across Report Name, Generated By, and Period. 300ms debounce. Targets `hx-get="/api/v1/mis/archive/"` with `?q=` param. Placeholder: "Search by report name, period, or author…"

**Advanced Filters (slide-in drawer, 360px):**

| Filter | Type | Options |
|---|---|---|
| Report Type | Multi-select checkbox | Monthly MIS, Board Report, Custom |
| Academic Year | Multi-select checkbox | All AYs in archive (dynamically populated) |
| Month / Period | Month range picker | From month – To month |
| Branch Coverage | Select | All Branches / Specific Branches / Partial Coverage |
| Status | Multi-select checkbox | Sent, Portal Only, Failed |
| Format | Multi-select checkbox | PDF, XLSX, Both |
| Generated By | Typeahead | User search within group |
| Never Sent | Toggle | Show only reports never distributed |

Active filter chips displayed below table toolbar. [Clear All] resets all filters.

**Empty state:** Illustration of an empty filing cabinet. Heading: "No archived reports found." Description: "Generated reports will automatically appear here. Adjust your filters to find a specific report." CTA: [Clear Filters] (if filters active) or [Go to Report Builder] (if no reports at all).

**Loader state:** 5-row skeleton with column-width bars; KPI bar shows 6 skeleton cards.

---

### 5.2 Download & Distribution History

This section exists within the `report-detail` drawer (Tab 2 and Tab 3) rather than as a standalone page section. See Section 6.1 for the full drawer spec.

For the archive table, the Actions column provides [Download] which triggers a pre-signed URL generation for immediate file download without opening the drawer.

---

## 6. Drawers & Modals

### 6.1 Drawer: `report-detail`

**Width:** 680px. Slides in from right. Overlay backdrop.

**Drawer header:** Report Name (h2), Type badge, Status badge, Period text, [Close] button.

---

**Tab 1 — Overview**

Displays a structured card layout of all report metadata:

| Field | Value |
|---|---|
| Report Name | Full name |
| Report Type | Badge |
| Academic Year | e.g. 2025-26 |
| Period Covered | e.g. January 2026 |
| Date Range | From [date] to [date] |
| Sections Included | Bulleted list of all sections (Enrollment & Admissions, Fee Collection, etc.) |
| Branches Covered | "All Branches" or named list |
| Generated By | User display name + role |
| Generated At | Full datetime |
| Generation Duration | e.g. "47 seconds" |
| Template Used | Link to template (if template still exists) |
| File Format(s) | PDF / XLSX / Both with file size |
| Generation Log | Expandable pre-formatted text block with raw job log (last 50 lines) |

**[Regenerate Report] button** (Role 103 only) — opens generation progress modal for this report configuration. Note: regeneration creates a new archive entry; it does not overwrite the original.

---

**Tab 2 — Distribution**

Table of all distribution events for this report:

| Column | Description |
|---|---|
| Recipient Name | Display name |
| Role | Recipient's role at time of sending |
| Email Address | Masked partially (e.g. j***@example.com) |
| Delivery Method | Email PDF / Email XLSX / Portal Only |
| Sent At | Datetime |
| Delivery Status | Delivered (green) / Failed (red) / Pending (amber) |
| Opened At | Datetime if opened; "—" if not tracked or not opened |
| Re-send | [Re-send] button per row (Roles 102–103 only) |

Below the table: **[+ Re-send to Original Recipients]** button (Roles 102–103) — sends to all recipients in the original list. **[+ Re-send to New Recipients]** button (Role 103 only) — opens a typeahead modal to select additional recipients and dispatch.

**[Re-send to New Recipients] Modal (420px):**
- Typeahead multi-select for recipient search (from group contacts)
- Delivery method checkbox group (Email PDF / Email XLSX / Portal Only)
- [Send] | [Cancel]

---

**Tab 3 — Download**

| Element | Description |
|---|---|
| Download PDF button | Generates pre-signed R2 URL; triggers browser download; shows spinner during URL generation |
| Download XLSX button | Same; only shown if XLSX format exists |
| File metadata | Size, generated at, MD5 checksum for integrity verification |
| [Regenerate Report] button | Role 103 only; same as Tab 1 action |
| Retention Notice | "This report is retained per your data retention policy. Auto-archival after [N] years." |

---

### 6.2 Modal: `report-delete-confirm`

**Width:** 420px. Centered overlay.

- **Title:** "Delete Archived Report"
- **Body:** "You are about to permanently delete the archived report **[Report Name]** for **[Period]**. The file will be removed from storage and the distribution history will be erased. This action cannot be undone and may affect compliance records."
- **Warning:** Amber callout box — "Deleting a sent report removes your proof of dispatch. Only proceed if this report was generated in error."
- **Confirmation input:** "Type **DELETE** to confirm" — [Delete] button disabled until user types "DELETE" exactly.
- **Footer:** [Delete] (red destructive) | [Cancel]

---

### 6.3 Modal: `re-send-progress`

**Width:** 420px. Triggered when re-sending to recipients.

- **In Progress:** Spinner + "Sending report to [N] recipient(s)…"
- **Completed:** "Report sent to [N] recipient(s) successfully." + timestamp
- **Partial Failure:** "Sent to [N] of [M] recipients. [K] deliveries failed." + list of failed addresses
- **Footer:** [Close]

---

## 7. Charts

### 7.1 Reports by Type — Donut Chart

- **Library:** Chart.js 4.x
- **Type:** Doughnut chart
- **Segments:** One per report type (Monthly MIS, Board Report, Custom) — colourblind-safe: blue #2563EB, purple #7C3AED, grey #6B7280
- **Centre label:** Total count of reports
- **Filter:** Academic Year dropdown above chart (defaults to "All Time"); changing AY re-fetches data via HTMX
- **Data source:** `/api/v1/mis/archive/charts/by-type/?ay=all`
- **Interactions:** Hover tooltip shows type name and count; click segment filters the archive table
- **Export:** PNG download button in chart header
- **Empty state:** "No archived reports to display." with empty doughnut outline
- **Loader:** Grey circular ring skeleton

### 7.2 Monthly Report Volume — Bar Chart

- **Library:** Chart.js 4.x
- **Type:** Vertical bar chart
- **X-axis:** Last 12 calendar months (rolling, most recent on right)
- **Y-axis:** Count of reports generated
- **Series:** Single series (total reports); optional toggle to split by type
- **Data source:** `/api/v1/mis/archive/charts/monthly-volume/?months=12`
- **Interactions:** Hover tooltip; click bar filters archive table to that month
- **Export:** PNG download button
- **Empty state:** "No reports generated in the last 12 months." with empty bar chart
- **Loader:** Grey skeleton rectangle (height 180px)

---

## 8. Toast Messages

| Action | Success | Error |
|---|---|---|
| Open report detail drawer | — | "Failed to load report details. Please try again." (manual dismiss) |
| Download PDF | "Download started." (4s) | "Failed to generate download link. [reason]" (manual dismiss) |
| Download XLSX | "Download started." (4s) | "Failed to generate download link. [reason]" (manual dismiss) |
| Re-send to original recipients | "Report sent to [N] recipients." (4s) | "Failed to send report. [reason]" (manual dismiss) |
| Re-send to new recipients | "Report sent to [N] new recipients." (4s) | "Delivery failed for [N] recipients. Check distribution tab for details." (manual dismiss) |
| Delete report | "Report permanently deleted." (4s) | "Failed to delete report. [reason]" (manual dismiss) |
| Bulk delete | "[N] reports deleted." (4s) | "Bulk delete failed. [reason]" (manual dismiss) |
| Export archive index (CSV) | "Archive index exported." (4s) | "Export failed. Please try again." (manual dismiss) |
| Regenerate report | "Regeneration job started. A new archive entry will be created." (4s) | "Failed to start regeneration. [reason]" (manual dismiss) |
| Dismiss alert banner | — | "Failed to dismiss alert." (manual dismiss) |

---

## 9. Empty States

| Section | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| Archive Table (no reports) | Empty filing cabinet icon | "No reports in the archive." | "All generated MIS and Board reports will appear here automatically." | [Go to Report Builder] |
| Archive Table (filtered, no results) | Search with no results icon | "No reports match your filters." | "Try adjusting your filters or search terms to find what you're looking for." | [Clear Filters] |
| Distribution tab (no events) | Envelope with question mark | "This report was never sent." | "No distribution events were recorded for this report." | [Re-send Now] (Roles 102–103) |
| Chart 7.1 (no data) | Empty doughnut icon | "No data for selected period." | "Reports generated in this academic year will appear here." | — |
| Chart 7.2 (no data) | Empty bar chart icon | "No report volume data." | "Monthly generation counts will appear here as reports are generated." | — |

---

## 10. Loader States

| Element | Loader Type | Description |
|---|---|---|
| Archive Table | Skeleton | 5 rows; each has 11 column-width grey bars at varied widths |
| KPI Summary Bar | Skeleton | 6 card-shaped rectangles with animated shimmer |
| Report Detail Drawer (opening) | Skeleton | 3 tabs shown; Tab 1 content replaced by 8 label+value skeleton pairs |
| Distribution Table in Drawer | Skeleton | 4 rows, 7 columns |
| Download Button (URL generation) | Spinner | 16px spinner inside button; button text changes to "Preparing…" |
| Re-send Button | Spinner | 16px spinner; button disabled |
| Chart 7.1 | Skeleton | Circular grey ring (doughnut outline) |
| Chart 7.2 | Skeleton | Rectangle, height 180px, animated shimmer |
| Export CSV button | Spinner | Button text changes to "Exporting…"; spinner shown |

---

## 11. Role-Based UI Visibility

| UI Element | Role 102 | Role 103 | Roles 104–107 | G4/G5 (read grant) |
|---|---|---|---|---|
| Delete button (per row) | Hidden | Visible | Hidden | Hidden |
| Bulk Delete button | Hidden | Visible | Hidden | Hidden |
| Re-send button (per row) | Visible | Visible | Hidden | Hidden |
| Re-send to Original | Visible | Visible | Hidden | Hidden |
| Re-send to New Recipients | Hidden | Visible | Hidden | Hidden |
| Export Archive Index (CSV) | Visible | Visible | Visible | Visible |
| Regenerate Report button | Hidden | Visible | Hidden | Hidden |
| Download buttons | Visible | Visible | Visible | Visible |
| Distribution tab | Visible | Visible | Visible (read) | Visible (read) |
| Bulk Re-send | Visible | Visible | Hidden | Hidden |
| Advanced filter drawer | Visible | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Path | Auth | Description | Query Params |
|---|---|---|---|---|
| GET | `/api/v1/mis/archive/` | Roles 102–107 | List all archived reports, paginated | `page`, `page_size`, `q`, `type`, `ay`, `period_from`, `period_to`, `branch_coverage`, `status`, `format`, `generated_by`, `never_sent` |
| GET | `/api/v1/mis/archive/{id}/` | Roles 102–107 | Retrieve single archived report full detail | — |
| DELETE | `/api/v1/mis/archive/{id}/` | Role 103 | Permanently delete archived report + R2 files | — |
| DELETE | `/api/v1/mis/archive/bulk-delete/` | Role 103 | Bulk delete by report ID list | Body: `{ids: []}` |
| GET | `/api/v1/mis/archive/{id}/download/` | Roles 102–107 | Generate pre-signed R2 URL for download | `format` (pdf \| xlsx) |
| POST | `/api/v1/mis/archive/{id}/resend/` | Roles 102–103 | Re-send to original recipients | — |
| POST | `/api/v1/mis/archive/{id}/resend-new/` | Role 103 | Re-send to new recipients | Body: `{recipients: [], delivery_method: []}` |
| GET | `/api/v1/mis/archive/{id}/distribution/` | Roles 102–107 | Distribution history for a report | — |
| POST | `/api/v1/mis/archive/{id}/regenerate/` | Role 103 | Trigger regeneration job (creates new archive entry) | — |
| GET | `/api/v1/mis/archive/kpis/` | Roles 102–107 | KPI summary bar data | — |
| GET | `/api/v1/mis/archive/charts/by-type/` | Roles 102–107 | Donut chart data by report type | `ay` |
| GET | `/api/v1/mis/archive/charts/monthly-volume/` | Roles 102–107 | Bar chart monthly volume data | `months` |
| GET | `/api/v1/mis/archive/export/` | Roles 102–107 | Export archive index as CSV | `ay`, `type`, `status` |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Archive table search | `input` (300ms debounce) | `hx-get="/api/v1/mis/archive/"` | `#archive-table-body` | `innerHTML` | Sends `q` param |
| Archive table pagination | `click` on page link | `hx-get="/api/v1/mis/archive/"` | `#archive-table-body` | `innerHTML` | Sends `page`, `page_size` |
| Apply advanced filters | `click` [Apply] | `hx-get="/api/v1/mis/archive/"` | `#archive-table-body` | `innerHTML` | Closes filter drawer; updates chips |
| Open report detail drawer | `click` on Report Name cell | `hx-get="/group/mis/archive/drawer/{id}/"` | `#drawer-container` | `innerHTML` | Loads drawer with Tab 1 active |
| Switch drawer tab | `click` on tab | `hx-get="/group/mis/archive/drawer/{id}/tab/{tab}/"` | `#drawer-tab-content` | `innerHTML` | Lazy-loads per-tab content |
| Generate download URL | `click` [Download] | `hx-get="/api/v1/mis/archive/{id}/download/?format=pdf"` | `#download-link-{id}` | `outerHTML` | Returns `<a href="...">` tag; triggers download |
| Re-send to original | `click` [Re-send] | `hx-post="/api/v1/mis/archive/{id}/resend/"` | `#resend-modal` | `innerHTML` | Opens progress modal |
| Delete report | `click` [Delete] in confirm modal | `hx-delete="/api/v1/mis/archive/{id}/"` | `#row-{id}` | `outerHTML` | Removes row; shows toast |
| AY filter on donut chart | `change` on AY dropdown | `hx-get="/api/v1/mis/archive/charts/by-type/"` | `#chart-by-type-data` | `innerHTML` | Sends `ay` param; Chart.js re-renders |
| Dismiss alert banner | `click` X button | `hx-delete="/group/mis/archive/alerts/{alert_id}/dismiss/"` | `#alert-{alert_id}` | `outerHTML` | Stores dismissal server-side per session |
| Bulk row select all | `click` header checkbox | JavaScript | All row checkboxes | — | Reveals bulk action toolbar |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
