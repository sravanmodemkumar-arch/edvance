# 09 — Board Report Generator

> **URL:** `/group/mis/board-report/`
> **File:** `09-board-report-generator.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Role 102 (Group Analytics Director), Role 103 (Group MIS Officer), Role 104 (Group Academic Data Analyst), Role 105 (Group Exam Analytics Officer), Role 106 (Group Hostel Analytics Officer), Role 107 (Group Strategic Planning Officer)

---

## 1. Purpose

The Board Report Generator is a specialised tool for producing high-quality, visually rich presentation-style PDF documents intended for quarterly board meetings and annual review presentations. Unlike the monthly MIS reports which are tabular data exports, board reports are designed to impress and inform non-technical Board members — they include charts, callout highlights, achievement summaries, and strategic commentary laid out in a structured document format suitable for projection or printing. The generator allows the MIS Officer and Analytics Director to configure exactly what content appears (Group Performance Summary, Financial Snapshot, Academic Highlights, Toppers and Awards, Hostel and Welfare Summary, HR Summary, and Upcoming Strategic Priorities), add manually curated highlight callouts, apply the group's branding, and produce either a formatted PDF or a slide-deck-style PDF. The page also surfaces the Group Master Calendar's upcoming board meeting dates so the Officer can plan report generation with appropriate lead time.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Analytics Director | 102 | G1 | Full — configure templates, generate, send, delete | Co-owner with MIS Officer |
| Group MIS Officer | 103 | G1 | Full — configure templates, generate, send, delete | Co-owner with Analytics Director |
| Group Academic Data Analyst | 104 | G1 | View only — templates, generated reports, upcoming meetings | Cannot create, edit, or generate |
| Group Exam Analytics Officer | 105 | G1 | View only | Cannot create, edit, or generate |
| Group Hostel Analytics Officer | 106 | G1 | View only | Cannot create, edit, or generate |
| Group Strategic Planning Officer | 107 | G1 | View only | Cannot create, edit, or generate |

**Access enforcement note:** All mutation endpoints are guarded by `@require_role([102, 103])`. View-only roles receive server-rendered HTML with no interactive buttons rendered. Attempting to POST to create/edit/generate endpoints as Roles 104–107 returns HTTP 403.

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Dashboard > Analytics & MIS > Board Report Generator
```

### 3.2 Page Header

- **Title:** `Board Report Generator`
- **Subtitle:** `Create and manage presentation-style reports for Board meetings and annual reviews`
- **Header actions (Roles 102–103):** `[+ New Board Report Config]` button (primary, opens `board-report-config` drawer)
- **Header actions (all roles):** `[Upcoming Board Meetings]` link button that scrolls to Section 5.3

### 3.3 Alert Banners (conditional, each individually dismissible)

| Condition | Colour | Message |
|---|---|---|
| Next board meeting date is within 14 days and no board report has been generated for that meeting | Red | "Board meeting in [N] days — no report has been generated yet. Create one now." with [Generate Now] CTA |
| A board report has been generated but has no distribution events (never sent) | Amber | "A board report has been generated but not distributed to the Board. Send it now." with [View Report] CTA |

---

## 4. KPI Summary Bar

| KPI | Description | Format |
|---|---|---|
| Active Board Report Configs | Count of configured templates with status Active | Integer |
| Reports Generated This AY | Count of generated board reports in current academic year | Integer |
| Next Board Meeting | Date of the next upcoming board meeting from calendar | Date string ("in N days") |
| Avg Sections per Report | Average number of sections included across all generated reports | Decimal (e.g. 6.2) |
| Total Board Reports (All Time) | Total count across all AYs | Integer |
| Pending Distribution | Generated reports not yet sent | Integer, amber if > 0 |

KPI bar scrollable on mobile. Data source: `/api/v1/mis/board-report/kpis/` on page load.

---

## 5. Sections

### 5.1 Board Report Templates

Configured board report templates — the reusable configs that define report structure.

**Table columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Checkbox | Checkbox | No | Bulk select |
| Config Name | Text link | Yes | Opens `board-report-config` edit drawer (Roles 102–103) or read-only view (others) |
| Period Type | Badge | Yes | Quarterly (blue) / Annual (green) / Custom (grey) |
| Sections Included | Count | No | e.g. "7 sections" with tooltip listing them |
| Style Theme | Text | No | Group brand colour name |
| Last Generated | Datetime | Yes | Relative time with absolute on hover |
| Status | Badge | Yes | Active (green) / Draft (grey) / Archived (light grey) |
| Actions | Button group | No | [Generate Now] (Roles 102–103), [Edit] (Roles 102–103), [Delete] (Roles 102–103) |

**Table behaviour:**
- Default sort: Last Generated DESC then Status ASC
- Rows per page: 10 / 25 / 50 / All (default 25)
- Mobile (<768px): card layout with Config Name, Period Type badge, Status badge, and "..." action menu

**Search:** Full-text on Config Name. 300ms debounce. `hx-get="/api/v1/mis/board-report/configs/"` with `?q=`. Placeholder: "Search board report configurations…"

**Advanced Filters (slide-in drawer, 360px):**

| Filter | Type | Options |
|---|---|---|
| Period Type | Multi-select | Quarterly, Annual, Custom |
| Status | Multi-select | Active, Draft, Archived |
| Sections Included | Multi-select | All 7 section options + Custom Pages |
| Last Generated (range) | Date range | From – To |

**Empty state:** Illustration of a presentation document. Heading: "No board report configurations." Description: "Create your first board report configuration to produce presentation-ready reports for the Board." CTA: [+ New Board Report Config] (Roles 102–103 only).

**Loader:** 4-row skeleton, 7-column bars.

---

### 5.2 Generated Board Reports

History of all generated board reports.

**Table columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Checkbox | Checkbox | No | Bulk select |
| Report Title | Text link | Yes | Opens archive/detail view or download |
| Config Used | Text | No | Config name at time of generation |
| Period | Text | Yes | e.g. "Q3 2025-26" or "Annual 2025-26" |
| Generated By | Text | No | User display name |
| Generated At | Datetime | Yes | |
| Pages | Number | No | Total pages in PDF |
| Format | Badge | No | PDF / Slide PDF / Both |
| Distribution | Badge | No | Sent (green) / Unsent (amber) / Failed (red) |
| Actions | Button group | No | [Download] (all), [Re-send] (Roles 102–103), [Delete] (Roles 102–103) |

**Table behaviour:**
- Default sort: Generated At DESC
- Rows per page: 10 / 25 / 50 / All (default 25)
- Mobile: card layout

**Search:** Full-text on Report Title and Period. 300ms debounce.

**Empty state:** Heading: "No board reports generated yet." Description: "Use the Generate Now button on an active configuration." CTA: — (no CTA since generation requires an existing config)

---

### 5.3 Upcoming Board Meetings

Calendar data pulled from the Group Master Calendar (Division D or equivalent). Read-only display panel.

**Display format:** Simple card list with up to 5 upcoming board meetings, each card showing:
- Meeting name (e.g. "Q3 Board Meeting 2025-26")
- Date and time
- Venue (if configured)
- Agenda summary (truncated to 100 chars)
- Status of board report for this meeting: "Not Generated" (red tag) / "Generated, Not Sent" (amber tag) / "Sent" (green tag)
- [Prepare Report] button linking to the generator (Roles 102–103 only)

If no board meetings are configured in the calendar: message "No upcoming board meetings found in the Group Master Calendar. Configure them in Calendar Settings."

Data source: `/api/v1/group/calendar/events/?type=board_meeting&upcoming=true&limit=5`

---

## 6. Drawers & Modals

### 6.1 Drawer: `board-report-config`

**Width:** 680px. Slides in from right. 5-tab layout. Tab navigation tracks completion with green checkmark / grey dot indicators.

---

**Tab 1 — Cover**

| Field | Type | Required | Validation |
|---|---|---|---|
| Report Title | Text input | Yes | Min 5, max 150 chars; unique within AY |
| Subtitle | Text input | No | Max 100 chars |
| Period Type | Select | Yes | Options: Quarterly, Annual, Custom |
| Quarter | Select | Conditional | Required if Quarterly; options: Q1, Q2, Q3, Q4 |
| Academic Year | Select | Yes | From group AY config |
| Report Date | Date picker | Yes | The date to be printed on the cover page |
| Chairman Name | Text input | Yes | Auto-populated from group config; editable |
| CEO / Principal Secretary Name | Text input | No | For cover attribution |
| Group Logo | Read-only display | — | Auto-pulled from tenant config; shows preview; note "Update in Group Settings" |
| Cover Background | Select | No | Options: Default White, Brand Colour, Dark (navy) |

---

**Tab 2 — Sections**

Checklist of sections to include with drag-and-drop reordering:

| Section | Toggle (Include/Exclude) | Config Options |
|---|---|---|
| Group Performance Summary | Toggle (default ON) | — |
| Financial Snapshot | Toggle (default ON) | Select: Full Detail / Summary Only |
| Academic Highlights | Toggle (default ON) | Select exams to highlight (multi-select from AY exams); select which streams (MPC/BiPC/MEC/All) |
| Toppers & Awards | Toggle (default ON) | Select: Top N students (number input, 1–20, default 5); include branch-wise toppers toggle |
| Hostel & Welfare Summary | Toggle (default ON) | Select: All hostels / Specific hostel locations |
| HR Summary | Toggle (default ON) | Select: Include vacancies toggle; include salary bands toggle |
| Upcoming Strategic Priorities | Toggle (default ON) | Textarea for brief description (auto-populated from Strategic Planning if available) |
| Custom Page 1 | Toggle (default OFF) | Title field (max 80 chars), content textarea (max 1000 chars), optional image upload (JPG/PNG < 2MB) |
| Custom Page 2 | Toggle (default OFF) | Same as Custom Page 1 |

**Drag handle:** Each section row has a ☰ drag handle on the left. Drag reorders sections. Order is saved as an integer sequence.

---

**Tab 3 — Highlights**

Manually curated highlight callouts that appear as prominent pull-quote boxes in the report.

| Field | Type | Required | Validation |
|---|---|---|---|
| Highlight 1 | Textarea | No | Max 200 chars; counter shown |
| Highlight 2 | Textarea | No | Max 200 chars |
| Highlight 3 | Textarea | No | Max 200 chars |
| Award Winners to Feature | Multi-select typeahead | No | Student search; adds names as chip list; max 10 |
| Branches to Spotlight | Multi-select | No | Branch dropdown; max 3 |
| Spotlight Reason | Text input per branch | Conditional | Required if branch selected; max 100 chars; explains why this branch is spotlighted (e.g. "Highest attendance improvement") |

---

**Tab 4 — Style**

| Field | Type | Required | Validation |
|---|---|---|---|
| Page Orientation | Radio | Yes | Portrait (default) / Landscape |
| Colour Theme | Select | Yes | Options pulled from group brand config (Primary Colour, Secondary Colour, Neutral/White); shows colour swatch preview |
| Font Size | Radio | Yes | Standard (default) / Large (accessibility) |
| Show Page Numbers | Toggle | No | Default: On |
| Show Group Watermark | Toggle | No | Default: Off |
| Header on Every Page | Toggle | No | Default: On; shows group name and report title in header |
| Footer on Every Page | Toggle | No | Default: On; shows confidentiality notice and page number |

---

**Tab 5 — Generate**

- **[Preview First 3 Pages]** button — POST to `/api/v1/mis/board-report/configs/{id}/preview/`; returns thumbnail images of pages 1–3; displayed in an image carousel within the tab; button shows spinner while generating ("Generating preview… ~15 seconds")
- Preview area: 3-panel horizontal image carousel (approx. 200px tall each); scroll-snap
- **[Generate Full Report]** button (primary) — POST to `/api/v1/mis/board-report/configs/{id}/generate/`; opens `board-report-generation-progress` modal
- **[Schedule for Board Meeting Date]** toggle — when enabled:
  - Dropdown: "Link to board meeting" — selects from upcoming board meetings in the calendar
  - Shows selected meeting date and a note: "Report will be auto-generated 48 hours before this meeting if not already generated"
  - Save stores this linkage; does NOT trigger generation immediately

**Footer actions:** [Save as Draft] | [Save & Activate] | [Cancel]

---

### 6.2 Drawer: `board-report-config-edit`

Same structure as `board-report-config` but all fields pre-populated. Drawer header shows "Edit Board Report Configuration" + Config Name. Change audit shows last edited by and when.

---

### 6.3 Modal: `board-report-generation-progress`

**Width:** 520px.

**In Progress state:**
- Title: "Generating Board Report…"
- Subtitle: Configuration name + Period
- Progress bar (indeterminate animated, not percentage-based since duration varies)
- Body: "This may take 60–120 seconds depending on the number of sections and data volume."
- Spinner centred
- Cannot be dismissed while in progress

**Completed state:**
- Title: "Board Report Ready"
- Body: Report title, period, page count, file size
- Thumbnail of cover page (if generation service provides it)
- Buttons: [Download PDF] | [Send to Board] (Roles 102–103) | [Close]

**Failed state:**
- Title: "Generation Failed"
- Body: Truncated error from job log
- Buttons: [Retry] (Roles 102–103) | [View Log] | [Close]

---

### 6.4 Modal: `board-report-delete-confirm`

**Width:** 420px.

- **Title:** "Delete Board Report"
- For config deletion: "Deleting this configuration will not remove previously generated reports. You can still access them in the archive."
- For generated report deletion: "This will permanently delete the board report **[Report Title]** and remove the file from storage."
- Confirmation: Toggle "I understand this cannot be undone" — Delete button enabled only when toggled On
- **Footer:** [Delete] (red) | [Cancel]

---

## 7. Charts

### 7.1 Board Reports Generated per AY (Bar Chart)

- **Library:** Chart.js 4.x
- **Type:** Vertical bar chart
- **X-axis:** Academic years (last 4 AYs or all if < 4)
- **Y-axis:** Count of board reports generated
- **Series:** Single bar series; colour: purple #7C3AED
- **Data source:** `/api/v1/mis/board-report/charts/by-ay/`
- **Interactions:** Hover tooltip showing count; click bar filters the Generated Reports table to that AY
- **Export:** PNG download
- **Empty state:** "No board reports generated yet." with empty bar chart
- **Loader:** Skeleton rectangle, height 200px

### 7.2 Sections Included Most Often (Horizontal Bar Chart)

- **Library:** Chart.js 4.x
- **Type:** Horizontal bar chart
- **Y-axis:** Section names (all 9 possible sections)
- **X-axis:** Percentage of reports that included each section (0–100%)
- **Colour:** Teal #0D9488 for sections included in ≥ 80% of reports; grey #9CA3AF for others
- **Data source:** `/api/v1/mis/board-report/charts/section-frequency/`
- **Interactions:** Hover tooltip showing exact percentage; no click action
- **Export:** PNG download
- **Empty state:** "Not enough reports to show section frequency." (requires ≥ 3 generated reports)
- **Loader:** Skeleton — 8 horizontal bars of varying widths, stacked vertically

---

## 8. Toast Messages

| Action | Success | Error |
|---|---|---|
| Config created (Save & Activate) | "Board report configuration created and activated." (4s) | "Failed to create configuration. [reason]" (manual dismiss) |
| Config created (Save as Draft) | "Configuration saved as draft." (4s) | "Failed to save draft." (manual dismiss) |
| Config updated | "Configuration updated." (4s) | "Failed to update configuration." (manual dismiss) |
| Config deleted | "Board report configuration deleted." (4s) | "Failed to delete configuration." (manual dismiss) |
| Preview generation started | "Generating preview pages…" (4s) | "Preview generation failed. [reason]" (manual dismiss) |
| Report generation started | "Board report generation started." (4s) | "Failed to start generation. [reason]" (manual dismiss) |
| Report generation completed | "Board report generated successfully." (4s) | — |
| Report generation failed | — | "Board report generation failed. [reason]" (manual dismiss) |
| Report sent to board | "Report sent to [N] Board members." (4s) | "Failed to send report to some recipients. [N] failures." (manual dismiss) |
| Report downloaded | "Download started." (4s) | "Failed to generate download link." (manual dismiss) |
| Schedule linked to board meeting | "Report scheduled 48 hours before [Meeting Name]." (4s) | "Failed to link to board meeting." (manual dismiss) |
| Report deleted | "Board report deleted." (4s) | "Failed to delete report." (manual dismiss) |

---

## 9. Empty States

| Section | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| Templates Table | Presentation document icon | "No board report configurations." | "Create a configuration to define what goes into your Board reports." | [+ New Board Report Config] (Roles 102–103) |
| Generated Reports Table | Stack of papers icon | "No board reports generated." | "Use Generate Now on any active configuration to produce your first board report." | — |
| Upcoming Board Meetings | Calendar icon | "No upcoming board meetings found." | "Configure board meeting dates in the Group Master Calendar to see them here." | [Open Calendar Settings] |
| Chart 7.1 | Empty bar chart | "No board reports across academic years." | "Generate reports to see AY-wise volume here." | — |
| Chart 7.2 | No data bar chart | "Not enough reports to show section frequency." | "Generate at least 3 board reports to see which sections are used most." | — |
| Preview pane (Tab 5) | Document preview placeholder | "Preview not yet generated." | "Click Preview First 3 Pages to see a sample of your report layout." | — |

---

## 10. Loader States

| Element | Loader Type | Description |
|---|---|---|
| Templates Table | Skeleton | 4 rows, 8 columns; animated shimmer |
| Generated Reports Table | Skeleton | 4 rows, 10 columns |
| KPI Summary Bar | Skeleton | 6 card rectangles |
| Upcoming Board Meetings panel | Skeleton | 3 meeting card skeletons; each 80px tall |
| Chart 7.1 | Skeleton | Rectangle, 200px tall |
| Chart 7.2 | Skeleton | Rectangle, 220px tall (taller for horizontal bars) |
| Drawer opening | Skeleton | Tab headers visible; Tab 1 content replaced by form field skeletons |
| Preview generation (Tab 5) | Full spinner | "Generating preview pages…" text with centred spinner; preview area shows 3 grey placeholder rectangles |
| Generate Full Report button | Spinner | Button text changes to "Generating…"; spinner inline; button disabled |
| Send to Board button | Spinner | Button text changes to "Sending…"; disabled during POST |

---

## 11. Role-Based UI Visibility

| UI Element | Role 102 | Role 103 | Roles 104–107 |
|---|---|---|---|
| "+ New Board Report Config" button | Visible | Visible | Hidden |
| Edit button (Templates table) | Visible | Visible | Hidden |
| Delete button (Templates table) | Visible | Visible | Hidden |
| Generate Now button | Visible | Visible | Hidden |
| Re-send button (Generated Reports) | Visible | Visible | Hidden |
| Delete button (Generated Reports) | Visible | Visible | Hidden |
| Send to Board button (in modal) | Visible | Visible | Hidden |
| Schedule for Board Meeting toggle | Visible | Visible | Hidden |
| Bulk action toolbar | Visible | Visible | Hidden |
| Download button | Visible | Visible | Visible |
| Prepare Report button (Meetings panel) | Visible | Visible | Hidden |
| Advanced filter drawer | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Path | Auth | Description | Query Params |
|---|---|---|---|---|
| GET | `/api/v1/mis/board-report/configs/` | Roles 102–107 | List all board report configurations | `page`, `page_size`, `q`, `period_type`, `status` |
| POST | `/api/v1/mis/board-report/configs/` | Roles 102–103 | Create board report configuration | — |
| GET | `/api/v1/mis/board-report/configs/{id}/` | Roles 102–107 | Retrieve single config detail | — |
| PUT | `/api/v1/mis/board-report/configs/{id}/` | Roles 102–103 | Full update config | — |
| PATCH | `/api/v1/mis/board-report/configs/{id}/` | Roles 102–103 | Partial update (e.g. status) | — |
| DELETE | `/api/v1/mis/board-report/configs/{id}/` | Roles 102–103 | Delete config | — |
| POST | `/api/v1/mis/board-report/configs/{id}/preview/` | Roles 102–103 | Generate 3-page preview images | — |
| POST | `/api/v1/mis/board-report/configs/{id}/generate/` | Roles 102–103 | Trigger full report generation | — |
| GET | `/api/v1/mis/board-report/reports/` | Roles 102–107 | List all generated board reports | `page`, `page_size`, `q`, `ay`, `period_type`, `distribution` |
| GET | `/api/v1/mis/board-report/reports/{id}/` | Roles 102–107 | Retrieve single generated report detail | — |
| DELETE | `/api/v1/mis/board-report/reports/{id}/` | Roles 102–103 | Delete generated report + R2 file | — |
| GET | `/api/v1/mis/board-report/reports/{id}/download/` | Roles 102–107 | Pre-signed R2 URL for download | `format` (pdf \| slide_pdf) |
| POST | `/api/v1/mis/board-report/reports/{id}/send/` | Roles 102–103 | Send report to configured recipients | Body: `{recipient_ids: [], delivery_method: []}` |
| GET | `/api/v1/mis/board-report/kpis/` | Roles 102–107 | KPI summary bar data | — |
| GET | `/api/v1/mis/board-report/charts/by-ay/` | Roles 102–107 | Reports per AY bar chart data | — |
| GET | `/api/v1/mis/board-report/charts/section-frequency/` | Roles 102–107 | Section inclusion frequency data | — |
| GET | `/api/v1/group/calendar/events/` | Roles 102–107 | Upcoming board meeting events | `type`, `upcoming`, `limit` |
| GET | `/api/v1/mis/jobs/{job_id}/status/` | Roles 102–107 | Poll generation job status | — |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Template table search | `input` 300ms debounce | `hx-get="/api/v1/mis/board-report/configs/"` | `#configs-table-body` | `innerHTML` | |
| Template table pagination | `click` page button | `hx-get="/api/v1/mis/board-report/configs/"` | `#configs-table-body` | `innerHTML` | |
| Open config drawer (create) | `click` [+ New Board Report Config] | `hx-get="/group/mis/board-report/drawer/create/"` | `#drawer-container` | `innerHTML` | |
| Open config drawer (edit) | `click` [Edit] | `hx-get="/group/mis/board-report/drawer/edit/{id}/"` | `#drawer-container` | `innerHTML` | |
| Save config draft | `click` [Save as Draft] | `hx-post="/api/v1/mis/board-report/configs/"` | `#configs-table-body` | `innerHTML` | Closes drawer on success |
| Generate Now | `click` [Generate Now] | `hx-post="/api/v1/mis/board-report/configs/{id}/generate/"` | `#generation-modal` | `innerHTML` | Opens generation progress modal |
| Poll generation status | `load` + `every 3s` | `hx-get="/api/v1/mis/jobs/{job_id}/status/"` | `#generation-modal-body` | `innerHTML` | Stops when Completed/Failed |
| Preview generation | `click` [Preview First 3 Pages] | `hx-post="/api/v1/mis/board-report/configs/{id}/preview/"` | `#preview-area` | `innerHTML` | Shows spinner; replaces with images |
| Generated reports search | `input` 300ms debounce | `hx-get="/api/v1/mis/board-report/reports/"` | `#reports-table-body` | `innerHTML` | |
| Generated reports pagination | `click` page button | `hx-get="/api/v1/mis/board-report/reports/"` | `#reports-table-body` | `innerHTML` | |
| Delete config confirm | `click` [Delete] in modal | `hx-delete="/api/v1/mis/board-report/configs/{id}/"` | `#config-row-{id}` | `outerHTML` | |
| Delete report confirm | `click` [Delete] in modal | `hx-delete="/api/v1/mis/board-report/reports/{id}/"` | `#report-row-{id}` | `outerHTML` | |
| Load upcoming meetings | `load` | `hx-get="/api/v1/group/calendar/events/?type=board_meeting&upcoming=true&limit=5"` | `#upcoming-meetings-panel` | `innerHTML` | Lazy-loads section |
| Dismiss alert banner | `click` X | `hx-delete="/group/mis/board-report/alerts/{alert_id}/dismiss/"` | `#alert-{alert_id}` | `outerHTML` | |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
