# Page 24: Analytics Export Centre

**Division:** M — Analytics & MIS
**URL:** `/group/analytics/export-centre/`
**Primary Role:** 103 — MIS Officer
**Supporting Roles:** 102 (Analytics Director), 104 (Academic Data Analyst), 105 (Exam Analytics Officer), 106 (Hostel Analytics Officer), 107 (Strategic Planning Officer)
**Access Level:** G1 (read-only on all analytics data; write on export job creation and export schedule management)

---

## 1. Purpose

Provides a centralised interface for creating, scheduling, downloading, and managing all analytics data exports across Division M. Instead of exporting from individual analytics pages one at a time, the Export Centre allows the MIS Officer and other roles to compose multi-section exports, schedule recurring report distributions, track export job statuses, and maintain a downloadable archive of past exports. All exports are scoped to the authenticated user's institution group.

---

## 2. Roles & Permissions Matrix

| UI Element | Role 102 | Role 103 | Role 104 | Role 105 | Role 106 | Role 107 |
|---|---|---|---|---|---|---|
| Export job list | Own | All | Own | Own | Own | Own |
| Create export job | Create | Create | Create | Create | Create | Create |
| Cancel pending job | Own | All | Own | Own | Own | Own |
| Download completed export | Own | All | Own | Own | Own | Own |
| Delete export record | Own (30d) | All | Own (30d) | Own (30d) | Own (30d) | Own (30d) |
| Export schedules list | Own | All | Own | Own | Own | Own |
| Create schedule | Create | Create | Create | Create | Create | Create |
| Edit / delete schedule | Own | All | Own | Own | Own | Own |
| Export archive (all users) | View | View | — | — | — | — |

**Data scope per role:** Each role's export jobs automatically scope to data they are permitted to view on individual analytics pages (e.g. Role 106 exports only include hostel-related columns; teacher performance data in exports is filtered to Role 105's restricted view).

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ Breadcrumb: Analytics & MIS > Analytics Export Centre               │
│ Title: "Analytics Export Centre"   [+ New Export]                   │
├─────────────────────────────────────────────────────────────────────┤
│  KPI BAR (5 cards)                                                   │
│  Pending Jobs | Completed (Today) | Failed | Scheduled | Storage Used│
├─────────────────────────────────────────────────────────────────────┤
│  TABS: [Export Jobs] [Schedules] [Archive]                           │
├─────────────────────────────────────────────────────────────────────┤
│  [TAB CONTENT — see sections below]                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. KPI Bar

Five stat cards. Auto-refresh `hx-trigger="every 60s"` (faster than other pages due to job status changes), `hx-target="#export-kpi-bar"`.

| # | Label | Value | Sub-label | Highlight |
|---|---|---|---|---|
| 1 | Pending Jobs | Jobs in queue / processing | "In progress" | `bg-amber-50` if > 0 |
| 2 | Completed (Today) | Jobs completed today | "Ready to download" | `bg-green-50` |
| 3 | Failed | Failed jobs in last 7 days | "Need attention" | `bg-red-50` if > 0 |
| 4 | Scheduled | Active recurring schedules | "Auto-running" | — |
| 5 | Storage Used | Total storage used by exports (MB/GB) | "of {quota} MB" | Amber if > 80% quota |

---

## 5. Tab 1 — Export Jobs

### 5.1 Filter Bar

| Control | Options |
|---|---|
| Status | All / Pending / Processing / Completed / Failed / Cancelled |
| Export Type | All / CSV / PDF / Excel |
| Report Type | All + report type list |
| Date | Today / This Week / This Month / Custom |
| Created By | All / Me only (Role 103 sees all; others see own by default) |

### 5.2 Export Jobs Table

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Integer | No | — |
| Job Ref | Text | No | e.g. EXP-2026-04312 |
| Report Name | Text | Yes | User-provided or auto-named |
| Report Type | Badge | Yes | e.g. "Attendance Analytics", "Fee Collection" |
| Format | Badge | Yes | CSV / PDF / Excel |
| Status | Badge | Yes | Pending / Processing / Completed / Failed / Cancelled |
| Created By | Text | Yes | Name + role |
| Created At | Datetime | Yes | — |
| Completed At | Datetime | Yes | — or "—" |
| File Size | Text | No | e.g. "2.4 MB" or "—" |
| Expires At | Date | No | Export file retention (30 days) |
| Actions | Buttons | No | [Download] [Retry] [Cancel] [Delete] (role-gated) |

### 5.3 Action Gating

| Action | Condition |
|---|---|
| [Download] | Status = Completed; scoped by role |
| [Retry] | Status = Failed; own jobs (Role 103 all) |
| [Cancel] | Status = Pending or Processing; own jobs |
| [Delete] | Any status, own jobs (within 30 days); Role 103 deletes any |

### 5.4 Status Badge Colours

| Status | Badge |
|---|---|
| Pending | `bg-gray-100 text-gray-600` |
| Processing | `bg-blue-100 text-blue-800` (animated pulse) |
| Completed | `bg-green-100 text-green-800` |
| Failed | `bg-red-100 text-red-800` |
| Cancelled | `bg-gray-100 text-gray-400` |

### 5.5 Live Job Status Polling

For any job in "Pending" or "Processing" state, the table row polls automatically:
```
hx-get="/api/v1/analytics/export-jobs/{id}/status/"
hx-trigger="every 5s"
hx-target="#job-row-{id}"
hx-swap="outerHTML"
```
Polling stops automatically when status changes to Completed/Failed/Cancelled (server sets `HX-Trigger: stopPolling` response header or row re-renders without the `hx-trigger` attribute).

When a job completes: row status badge updates, [Download] button appears, success toast fires.

---

## 6. Create Export Job Drawer

**ID:** `create-export-drawer`
**Width:** 680px
**Triggered by:** `[+ New Export]` button.

### Step 1 — Select Report Type

Checklist of available report types, grouped by category. Each item shows the report name, description, and supported formats.

**Available Export Types:**

| Category | Report | Formats |
|---|---|---|
| Cross-Branch | Cross-Branch Performance Hub | CSV, PDF |
| Cross-Branch | Branch Health Scorecard | CSV, PDF |
| Academic | Dropout Signal Monitor | CSV, PDF |
| Academic | Rank Trend Analyser | CSV, PDF |
| Academic | Teacher Performance Analytics | CSV, PDF |
| Exam | Exam Performance Heatmap | CSV, PDF, PNG (chart) |
| Exam | Topic Gap Analysis | CSV, PDF |
| Attendance | Attendance Analytics | CSV, PDF, Excel |
| Finance | Fee Collection Analytics | CSV, PDF, Excel |
| Hostel | Hostel Occupancy Analytics | CSV, PDF |
| Hostel | Hostel Welfare Trend Analytics | CSV, PDF |
| Strategic | Branch Feasibility Analyser | PDF |
| Strategic | Three-Year Expansion Plan | CSV, PDF |
| MIS | Monthly MIS Report | PDF |
| MIS | Data Quality Dashboard | CSV, PDF |
| Custom | Custom Multi-Section Export | CSV, PDF |

User selects **one or more** report types (multi-select with checkboxes). Selecting multiple creates a "bundled" export job (single ZIP file containing all selected exports).

**Role filtering:** report types the user's role cannot access are greyed out and unselectable with a tooltip: "You do not have access to this report type."

### Step 2 — Configure Filters

For each selected report type, a collapsible filter section is shown. Filters are identical to those available on the individual analytics page.

Common filters shown for all report types:
- Branch: Multi-select (all branches in group).
- Date Range: Select (This Month / Last 3 Months / This Academic Year / Custom).
- Exam Cycle (if applicable): Select.
- Class / Stream (if applicable): Select.

Report-specific filters are shown within each report's collapsible section.

### Step 3 — Output Settings

| Field | Type | Validation |
|---|---|---|
| Export Name | Text (max 150 chars) — auto-filled: "{Report Type} — {Date}" | Optional to override |
| Format | Radio: CSV / PDF / Excel (options depend on report type selection) | Required |
| Include Charts | Checkbox (PDF only) | Default: checked for PDF |
| Date Stamp in Filename | Checkbox | Default: checked |
| Password Protection (PDF) | Toggle (default off) → password input if on | Optional; password min 8 chars |
| Notify when ready | Checkbox: In-app / Email | ≥ 1 required |

### Step 4 — Review & Submit

Summary card showing:
- Report types selected (list with remove buttons).
- Active filters per report.
- Output format + filename preview.
- Estimated file size (rough estimate from server: `GET /api/v1/analytics/export-jobs/estimate/`).
- Estimated processing time (rough: "< 30 seconds" / "1–2 minutes" / "3–5 minutes").

**[Create Export Job]** button: POST `/api/v1/analytics/export-jobs/` → job created → drawer closes → job row appears at top of table with "Pending" status → polling begins automatically.

---

## 7. Tab 2 — Schedules

Recurring export schedules that automatically trigger export jobs and distribute to configured recipients.

### 7.1 Schedules Table

| Column | Type | Sortable |
|---|---|---|
| Schedule Name | Text | Yes |
| Report Type(s) | Badge list | No |
| Format | Badge | Yes |
| Frequency | Badge | Yes |
| Next Run | Datetime | Yes |
| Last Run | Datetime | Yes |
| Last Status | Badge | Yes |
| Recipients | Integer (count) | No |
| Status | Toggle (Active / Paused) | Yes |
| Actions | [View] [Edit] [Pause/Resume] [Delete] | — |

**[Pause/Resume] toggle:** PATCH `/api/v1/analytics/export-schedules/{id}/toggle/` → status updates inline.

### 7.2 Create / Edit Schedule Drawer

**ID:** `create-schedule-drawer`
**Width:** 680px

| Field | Type | Validation |
|---|---|---|
| Schedule Name | Text (max 150 chars) | Required |
| Report Types | Multi-select (same list as export creation) | ≥ 1 required |
| Format | Select: CSV / PDF / Excel | Required |
| Frequency | Select: Daily / Weekly / Monthly / Quarterly / Custom (cron) | Required |
| Day of Week (if Weekly) | Select: Monday–Sunday | Conditional |
| Day of Month (if Monthly) | Select: 1st–28th | Conditional |
| Time | Time picker (HH:MM IST) | Required |
| Filters | Collapsible filter sections (same as create job) | Optional |
| Recipients | Multi-select (users in group with email addresses) | ≥ 1 required |
| Email Subject Template | Text (max 200 chars) | Required |
| Email Body | Textarea (max 500 chars) | Optional |
| Include in In-App Archive | Checkbox | Default: checked |
| Active | Toggle | Default: on |

Submit: POST `/api/v1/analytics/export-schedules/` → success toast → row prepended.
Edit: PUT endpoint (same form).
Delete: confirm modal → DELETE → row removed.

---

## 8. Tab 3 — Archive

Read-only view of all completed export files across all users in the group (Roles 102 and 103 only; other roles see Tab 1 for their own jobs).

### 8.1 Archive Table

| Column | Type | Sortable |
|---|---|---|
| Job Ref | Text | No |
| Report Name | Text | Yes |
| Report Type(s) | Badge list | Yes |
| Format | Badge | Yes |
| Created By | Text | Yes |
| Created At | Datetime | Yes |
| File Size | Text | No |
| Expires At | Date | Yes |
| Download | Button | — |

- Expired exports show a greyed-out row with "Expired" badge instead of a download button.
- Pagination: 20 rows per page.
- Search: by report name and created-by name.

### 8.2 Archive Storage Policy Banner

Blue info banner at top of Archive tab:
"Export files are retained for **30 days** from creation. Files older than 30 days are automatically deleted from Cloudflare R2. Download important exports before they expire."

---

## 9. Download Behaviour

- `[Download]` button: `GET /api/v1/analytics/export-jobs/{id}/download/` → returns a short-lived pre-signed Cloudflare R2 URL (valid 5 minutes) → browser downloads the file directly from R2.
- For bundled/multi-section exports: downloads a ZIP file containing all sections.
- Password-protected PDFs: user prompted for password in browser's native PDF password dialog.
- Download is logged in the export job record (`last_downloaded_at`, `downloaded_by`).

---

## 10. Toast Notifications

| Trigger | Type | Message |
|---|---|---|
| Export job created | Info | "Export job created. You'll be notified when it's ready." |
| Export job completed | Success | "'{Report Name}' is ready. Click to download." |
| Export job failed | Error | "Export failed for '{Report Name}'. Click Retry." |
| Export job cancelled | Info | "Export job cancelled." |
| Export job retried | Info | "Retrying export job…" |
| Schedule created | Success | "Export schedule '{name}' created." |
| Schedule updated | Success | "Schedule updated." |
| Schedule deleted | Info | "Schedule removed." |
| Schedule paused | Info | "Schedule paused." |
| Schedule resumed | Success | "Schedule resumed." |
| Download link expired | Warning | "Download link expired. Re-download the export file." |
| Storage quota warning | Warning | "Export storage is at {percent}% capacity. Consider deleting old exports." |
| Form validation fail | Error | "Please fill in all required fields." |

---

## 11. Empty States

| Context | Message | CTA |
|---|---|---|
| No export jobs | "No export jobs yet. Create your first export." | "+ New Export" |
| No jobs matching filter | "No export jobs match the selected filters." | "Reset Filters" |
| No schedules | "No recurring export schedules configured." | "+ New Schedule" |
| No archive records | "No completed exports in the archive." | — |
| Archive export expired | "This export has expired and is no longer available." | — |

---

## 12. Loader States

| Element | Loader |
|---|---|
| Initial page load | 5 card shimmer + tab content shimmer (table 20 rows) |
| KPI bar refresh | Individual card shimmer |
| Tab switch | Tab content shimmer |
| Table reload (filter/sort/page) | Table body shimmer (20 rows) |
| Drawer open | Spinner centred in drawer |
| Estimate fetch (Step 4) | "Calculating estimate…" text placeholder |
| Job row live poll | Subtle animated pulse on status badge (no full-row shimmer) |

---

## 13. HTMX Patterns

| Pattern | Target | Endpoint | Trigger |
|---|---|---|---|
| KPI auto-refresh | `#export-kpi-bar` | `/group/analytics/export-centre/kpis/` | `every 60s` |
| Jobs table reload (filter) | `#export-jobs-section` | `/group/analytics/export-centre/jobs/` | Apply filter |
| Jobs table search | `#export-jobs-tbody` | `/group/analytics/export-centre/jobs/` | `keyup changed delay:300ms` |
| Jobs table pagination | `#export-jobs-tbody` | `/group/analytics/export-centre/jobs/?page={n}` | Page nav |
| Job status poll (per row) | `#job-row-{id}` | `/api/v1/analytics/export-jobs/{id}/status/` | `every 5s` (stop on terminal status) |
| Schedules table reload | `#schedules-tbody` | `/group/analytics/export-centre/schedules/` | Filter change |
| Schedule toggle PATCH | `#schedule-row-{id}` | `/api/v1/analytics/export-schedules/{id}/toggle/` | Toggle click |
| Archive table reload | `#archive-tbody` | `/group/analytics/export-centre/archive/` | Filter / page |
| Export estimate GET | `#export-estimate` | `/api/v1/analytics/export-jobs/estimate/` | Step 4 load |
| Create job POST | `#create-export-form` | `/api/v1/analytics/export-jobs/` | Form submit |
| Create schedule POST | `#create-schedule-form` | `/api/v1/analytics/export-schedules/` | Form submit |

---

## 14. API Endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | `/api/v1/analytics/export-jobs/` | Job list (role-scoped) | G1 |
| POST | `/api/v1/analytics/export-jobs/` | Create export job | G1 |
| GET | `/api/v1/analytics/export-jobs/{id}/status/` | Poll job status | G1 (own) |
| GET | `/api/v1/analytics/export-jobs/{id}/download/` | Get pre-signed download URL | G1 (own / Role 103) |
| PATCH | `/api/v1/analytics/export-jobs/{id}/cancel/` | Cancel pending job | G1 (own / Role 103) |
| PATCH | `/api/v1/analytics/export-jobs/{id}/retry/` | Retry failed job | G1 (own / Role 103) |
| DELETE | `/api/v1/analytics/export-jobs/{id}/` | Delete job record | G1 (own / Role 103) |
| GET | `/api/v1/analytics/export-jobs/estimate/` | File size + time estimate | G1 |
| GET | `/api/v1/analytics/export-jobs/kpis/` | KPI values | G1 |
| GET | `/api/v1/analytics/export-schedules/` | Schedule list | G1 |
| POST | `/api/v1/analytics/export-schedules/` | Create schedule | G1 |
| PUT | `/api/v1/analytics/export-schedules/{id}/` | Update schedule | G1 (own / Role 103) |
| DELETE | `/api/v1/analytics/export-schedules/{id}/` | Delete schedule | G1 (own / Role 103) |
| PATCH | `/api/v1/analytics/export-schedules/{id}/toggle/` | Pause / resume | G1 (own / Role 103) |
| GET | `/api/v1/analytics/export-archive/` | Archive list (Roles 102, 103) | G1 restricted |

---

## 15. Mobile (Flutter + Riverpod)

| Screen | Description |
|---|---|
| `ExportCentreHomeScreen` | KPI cards + job list with status badges |
| `ExportJobDetailScreen` | Job detail: report type, format, filters, status, download button |
| `ScheduleListScreen` | Scrollable schedule list with active/paused toggles |

No export creation on mobile (multi-step wizard is desktop-only). Download from mobile is supported for completed jobs. State: `exportCentreProvider` (Riverpod). Pull-to-refresh triggers KPI + job list refresh.

---

## 16. Accessibility & Responsiveness

- Multi-step create drawer uses `aria-current="step"` on active wizard step indicator.
- Status badges: colour + text; animated "Processing" pulse also has `aria-label="Processing"`.
- Table scrolls horizontally on mobile; essential columns (Report Name, Format, Status, Actions) remain.
- Job row live-polling rows: `aria-live="polite"` region wrapping the status badge so screen readers announce status changes without a full-page announcement.
- Drawer closes on `Escape`; focus trap active; focus returns to `[+ New Export]` on close.
- All form fields: visible labels, `aria-required`, inline error messages via `aria-describedby`.
- Archive tab storage policy banner: `role="note"` for screen readers.
- Download confirmation tooltip shown on hover with keyboard focus equivalent (`:focus-visible`).
