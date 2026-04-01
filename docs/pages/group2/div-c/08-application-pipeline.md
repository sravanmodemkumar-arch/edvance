# Page 08 — Application Pipeline

- **URL:** `/group/adm/pipeline/`
- **Template:** `portal_base.html`
- **Theme:** Light

---

## 1. Purpose

The Application Pipeline page is the operational backbone of the entire admissions function for the group. Every student enquiry that matures into a formal application is tracked here, across every branch and every admission cycle the group runs. The pipeline provides a single authoritative view of where each application stands — from initial submission through screening, counselling, offer, and final enrolment — eliminating the need for branch-level spreadsheets or fragmented tracking.

The Group Admission Coordinator owns the day-to-day management of this page. They triage incoming applications, assign counsellors, move applications through stages, and trigger reminders for stalled records. The Group Admissions Director uses this page for oversight — monitoring throughput, identifying bottlenecks, and performing bulk operations during peak admission season. The pipeline design acknowledges that large groups process thousands of applications simultaneously and therefore prioritises performance: server-side pagination, HTMX partial refreshes, and stage-level filtering keep the interface snappy even at scale.

Stage integrity is enforced at the data layer. An application cannot skip stages; it must pass through each gate in sequence (Submitted → Under Review → Counselled → Offered → Enrolled or Rejected). Every stage transition is timestamped and logged to the application timeline, giving the Director and auditors a complete history of how each application was handled and by whom. Applications that linger too long in a stage trigger automatic bottleneck alerts so the Coordinator can intervene before deadlines are missed.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | Read + Bulk Actions + Export | Cannot edit individual application data; can override stage moves |
| Group Admission Coordinator (Role 24) | G3 | Full CRUD | Assign counsellors, move stages, bulk operations, export |
| Group Admission Counsellor (Role 25) | G3 | Own assigned applications only | Cannot move stages without Coordinator confirmation |
| Group Scholarship Exam Manager (Role 26) | G3 | Read only | Visible only for scholarship-tagged applications |
| Group Scholarship Manager (Role 27) | G3 | Read only | Visible only for scholarship-tagged applications |
| Group Demo Class Coordinator (Role 29) | G3 | Read only | Visible only for demo-sourced applications |
| CEO / Executive | G3+ | Read only | All applications, all branches |

> **Enforcement:** All access restrictions are enforced server-side in the Django view layer. Template blocks are conditionally rendered based on `request.user.role`. No client-side role checks are used. Counsellors receive a queryset filtered to `assigned_counsellor = request.user`; all other role filters are applied at the ORM level before rendering.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Application Pipeline
```

### 3.2 Page Header
- **Title:** Application Pipeline
- **Subtitle:** `{current_cycle_name}` — e.g., *Admission Cycle 2026–27*
- **Right-side actions:** `[+ New Application]` (Coordinator only) · `[Export All →]` · `[Refresh ↺]` (triggers HTMX KPI refresh)

### 3.3 Alert Banner

Displayed as a dismissible amber banner above KPI bar when triggered.

| Trigger | Message |
|---|---|
| Applications expiring in < 3 days | "{N} applications have deadlines in the next 3 days. Review and act before they expire." |
| Stage bottleneck detected (avg wait > 5 days) | "{Stage} stage has {N} applications averaging {X} days — possible bottleneck." |
| Bulk action completed | "{N} applications moved to {Stage} / assigned to {Counsellor}." |
| Counsellor unassigned applications > 20 | "{N} applications have no counsellor assigned. Assign to prevent delays." |
| System data freshness > 10 min | "Pipeline data was last refreshed {N} minutes ago. Click Refresh to update." |

---

## 4. KPI Summary Bar

> Auto-refreshes every 5 minutes via HTMX: `hx-get="/api/v1/group/{group_id}/adm/pipeline/kpis/" hx-trigger="every 5m" hx-target="#pipeline-kpi-bar" hx-swap="innerHTML"`

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Applications | Count of all applications in current cycle | `Application.objects.filter(cycle=active_cycle)` | Neutral (blue) | Clears all filters, shows full table |
| New Today | Applications created today (date = today) | `created_at__date=today` | Green if > yesterday's count; grey otherwise | Filters table to `created_at__date=today` |
| Submitted | Applications in Submitted stage | Stage filter | Grey (pending action) | Filters table to stage=Submitted |
| Under Review | Applications in Under Review stage | Stage filter | Blue | Filters table to stage=Under Review |
| Counselled | Applications in Counselled stage | Stage filter | Indigo | Filters table to stage=Counselled |
| Offered | Applications in Offered stage | Stage filter | Amber | Filters table to stage=Offered |
| Enrolled | Applications in Enrolled stage | Stage filter | Green | Filters table to stage=Enrolled |
| Rejected | Applications in Rejected stage | Stage filter | Red | Filters table to stage=Rejected |
| Avg Days in Pipeline | Mean of `(today - submitted_date)` across open applications | Computed at query time | Green ≤ 7 days; amber 8–14; red > 14 | Opens stage bottleneck panel (Section 5.3) |
| Expiring Soon | Applications with deadline < 3 days | `deadline__lte=today+3` | Red if > 0; green if 0 | Filters table to expiring applications |

---

## 5. Sections

### 5.1 Application Table

**Display:** Sortable, server-side paginated table. 20 rows per page. Checkbox column for bulk actions. Sticky header. Responsive horizontal scroll on small viewports.

**Columns:**

| Column | Notes |
|---|---|
| ☐ Checkbox | Select for bulk actions |
| Application ID | Clickable — opens application-detail drawer |
| Student Name | Clickable — opens application-detail drawer |
| Class Applying | e.g., Class 11, Class 6 |
| Stream | MPC / BiPC / MEC / CEC / General |
| Branch Preference 1 | Branch short name |
| Branch Preference 2 | Branch short name or "—" |
| Application Date | `DD MMM YYYY` |
| Stage Badge | Colour-coded pill: Submitted (grey) / Under Review (blue) / Counselled (indigo) / Offered (amber) / Enrolled (green) / Rejected (red) |
| Counsellor Assigned | Name or "Unassigned" (red text if unassigned) |
| Documents % | Progress bar pill (0–100%) |
| Days in Pipeline | Integer; colour: green ≤ 7, amber 8–14, red > 14 |
| Actions | `[View]` `[Move Stage]` `[Assign Counsellor]` |

**Search:** Live search by Student Name, Application ID, or Phone — `hx-trigger="keyup changed delay:400ms"` targeting `#application-table-body`.

**Filters:**
- Stage (multi-select checkboxes)
- Branch (multi-select)
- Stream (multi-select)
- Date range (from / to date pickers)
- Counsellor (dropdown — Coordinator/Director sees all; Counsellor sees only self)

**Bulk Actions (Coordinator / Director):**
- `[Assign Counsellor]` — opens assign-counsellor-modal for selected
- `[Move to Stage]` — opens move-stage-modal for selected
- `[Send Reminder]` — sends WhatsApp/email reminder to selected applicants
- `[Export Selected]` — CSV download of selected rows

**HTMX Pattern:**
- Filter/search changes: `hx-get="/api/v1/group/{group_id}/adm/pipeline/?{params}"` `hx-target="#application-table-body"` `hx-swap="innerHTML"` `hx-trigger="change"` on filter inputs
- Pagination: `hx-get` on page links, `hx-target="#application-table-wrapper"` `hx-swap="innerHTML"`
- Row [View]: `hx-get="/api/v1/group/{group_id}/adm/pipeline/{app_id}/detail/"` `hx-target="#application-detail-drawer"` `hx-swap="innerHTML"` triggers drawer open

**Empty State:** Illustration of empty inbox. Heading: "No applications found." Description: "No applications match your current filters. Try widening the date range or clearing stream filters." CTA: `[Clear Filters]`

---

### 5.2 Pipeline Stage Summary

**Display:** Horizontal strip of stage cards displayed above the application table. Each card shows the stage name, a count badge, and an optional trend arrow (vs yesterday). Clicking a stage card applies a filter to the table (Section 5.1) without a page reload.

**Stages displayed (left to right):** Submitted → Under Review → Counselled → Offered → Enrolled · Rejected (separated)

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/pipeline/?stage={stage}"` `hx-target="#application-table-body"` `hx-swap="innerHTML"` `hx-trigger="click"` on each stage card.

**Empty State:** If all stages show 0, display: "No applications in the current cycle. Start by adding a new application." with `[+ New Application]` CTA.

---

### 5.3 Stage Bottleneck Alert

**Display:** Collapsible panel (collapsed by default; expands when bottleneck exists). Lists stages where the average wait time exceeds 5 days. Each row shows: Stage name, average wait (days), count of stuck applications, branch breakdown (expandable).

| Column | Notes |
|---|---|
| Stage | Stage name |
| Avg Wait (days) | Computed from `stage_entered_at` to today |
| Applications Stuck | Count in this stage beyond threshold |
| Branches Affected | Comma-separated branch short names or expandable list |
| Action | `[Filter Table →]` jumps to filtered application table |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/pipeline/bottlenecks/"` `hx-trigger="load, every 5m"` `hx-target="#bottleneck-panel"` `hx-swap="innerHTML"`

**Empty State:** Green banner: "No stage bottlenecks detected. All applications are moving through the pipeline within expected timeframes."

---

### 5.4 Export & Reports

**Display:** Action card row with four options.

| Action | Description |
|---|---|
| Export CSV | Downloads all applications matching current filters as CSV |
| Export PDF Summary | Generates a one-page summary report of pipeline status with KPI bar snapshot |
| Print Batch Offer Letters | Triggers bulk PDF generation for all Offered-stage applications not yet sent |
| Download Bottleneck Report | PDF report of stage delays with branch attribution |

**HTMX Pattern:** Each export button triggers `hx-post` to the respective endpoint with current filter state; a spinner replaces the button while generating; on completion the file download is triggered via `HX-Redirect` header or `hx-on::after-request` JS hook.

---

## 6. Drawers & Modals

### 6.1 Application Detail Drawer
- **Width:** 640px (right-side slide-in)
- **Trigger:** Click on Application ID or Student Name in table, or `[View]` action button
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/pipeline/{app_id}/detail/`
- **Lazy Load:** Drawer shell renders immediately; content loads via HTMX on open

**Tabs:**

| Tab | Content |
|---|---|
| Profile | Student name, DOB, class, stream, guardian details, contact info, branch preferences |
| Documents | Document checklist with upload status (% complete), individual file preview links, [Request Missing →] button |
| Timeline | Chronological log of all stage transitions, assignments, notes, and system events with timestamp and actor name |
| Notes | Internal notes thread (Coordinator/Director only add notes; Counsellor can read and add own notes); rich text input |
| Actions | Move Stage, Assign Counsellor, Send Reminder, Generate Offer Letter, Reject Application — all with confirmation dialogs |

---

### 6.2 Move Stage Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Move Stage]` action in table row or Actions tab in drawer
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/pipeline/{app_id}/move-stage/` (form); `POST` on submit

**Fields:**
- Current Stage (read-only display)
- New Stage (dropdown — only forward stages permitted; Director can move backward)
- Note (optional textarea — reason for stage move)
- Notify Applicant (checkbox — if checked, triggers WhatsApp/email notification on save)

---

### 6.3 Assign Counsellor Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Assign Counsellor]` action in table row or bulk action
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/pipeline/assign-counsellor/` (form); `POST` on submit

**Fields:**
- Counsellor dropdown — filtered by branch matching application's branch preference
- Note to counsellor (optional)
- Notify counsellor (checkbox — sends in-app notification)

---

### 6.4 Modal: `reject-application-confirm`
- **Width:** 400px
- **Trigger:** `[Reject Application]` action in Section 6.1 (Application Detail drawer, Actions tab)
- **Fields:**
  - Rejection reason (select, required): Below cut-off / Incomplete documents / Seat unavailable / Eligibility mismatch / Applicant withdrew / Other
  - Notes (textarea, optional)
  - Notify applicant via WhatsApp (checkbox, default checked)
- **Buttons:** `[Confirm Rejection]` (danger red) + `[Cancel]`
- **HTMX:** POST to `/api/v1/group/{group_id}/adm/pipeline/applications/{application_id}/reject/`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Application stage moved | "Application {ID} moved to {Stage}" | Success | 4s |
| Counsellor assigned | "{Counsellor name} assigned to {N} application(s)" | Success | 4s |
| Bulk stage move completed | "{N} applications moved to {Stage}" | Success | 5s |
| Reminder sent | "Reminder sent to {N} applicant(s)" | Success | 4s |
| Export started | "Your export is being prepared. Download will start shortly." | Info | 5s |
| Stage move failed (validation) | "Cannot move to {Stage}: required documents incomplete." | Error | 6s |
| Counsellor assignment failed | "Could not assign counsellor — please try again." | Error | 5s |
| Offer letter generated | "Offer letter generated for {Student name}" | Success | 4s |
| Application rejected | "Application {ID} marked as Rejected. Applicant notified." | Warning | 5s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No applications in current cycle | Empty inbox graphic | "No Applications Yet" | "No applications have been received for the current admission cycle." | `[+ Add Application]` |
| Search/filter returns no results | Search-miss graphic | "No Matching Applications" | "No applications match your current search or filter criteria." | `[Clear Filters]` |
| No unassigned applications | Checkmark graphic | "All Applications Assigned" | "Every application has a counsellor assigned." | — |
| No expiring applications | Calendar graphic | "No Deadlines Expiring Soon" | "No applications are approaching their deadline in the next 3 days." | — |
| Counsellor views — no assigned applications | Person graphic | "No Applications Assigned to You" | "Applications will appear here when assigned by the Coordinator." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton (table rows + KPI bar shimmer) |
| KPI bar auto-refresh (every 5m) | Inline spinner on each KPI card |
| Filter / search change | Table body skeleton (5-row shimmer) |
| Pagination click | Table body skeleton |
| Drawer open (lazy load) | Drawer content area skeleton (3-block shimmer) |
| Tab switch in drawer | Tab content area spinner |
| Bulk action submit | Button spinner + table overlay with "Processing…" text |
| Export generation | Button spinner; button disabled until complete |
| Move stage form load | Modal content skeleton |
| Assign counsellor form load | Modal content skeleton |
| Bottleneck panel refresh | Panel shimmer |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| Element | Dir (23) | Coord (24) | Counsellor (25) | Scholarship Mgr (27) | Demo Coord (29) | CEO |
|---|---|---|---|---|---|---|
| [+ New Application] button | Hidden | Visible | Hidden | Hidden | Hidden | Hidden |
| Bulk action toolbar | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| [Move Stage] action | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| [Assign Counsellor] action | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| [Reject Application] in drawer | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| Notes tab (add note) | Visible | Visible | Visible (own) | Hidden | Hidden | Hidden |
| Actions tab in drawer | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| Export All button | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| Bottleneck alert panel | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| Stage Summary strip (click-to-filter) | Visible | Visible | Visible | Visible | Visible | Visible |
| Application table | Visible (all) | Visible (all) | Own assigned only | Scholarship-tagged only | Demo-sourced only | Visible (all) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/pipeline/` | JWT G3+ | List applications with filters, search, pagination |
| POST | `/api/v1/group/{group_id}/adm/pipeline/` | JWT G3 | Create new application |
| GET | `/api/v1/group/{group_id}/adm/pipeline/kpis/` | JWT G3+ | KPI bar data (counts per stage, avg days, expiring) |
| GET | `/api/v1/group/{group_id}/adm/pipeline/bottlenecks/` | JWT G3+ | Stage bottleneck list (stages with avg wait > 5 days) |
| GET | `/api/v1/group/{group_id}/adm/pipeline/{app_id}/detail/` | JWT G3+ | Full application detail (profile, docs, timeline, notes) |
| PATCH | `/api/v1/group/{group_id}/adm/pipeline/{app_id}/move-stage/` | JWT G3 | Move application to a new stage |
| PATCH | `/api/v1/group/{group_id}/adm/pipeline/{app_id}/assign-counsellor/` | JWT G3 | Assign or reassign counsellor |
| POST | `/api/v1/group/{group_id}/adm/pipeline/{app_id}/notes/` | JWT G3 | Add note to application timeline |
| POST | `/api/v1/group/{group_id}/adm/pipeline/bulk/move-stage/` | JWT G3 | Bulk stage move for selected application IDs |
| POST | `/api/v1/group/{group_id}/adm/pipeline/bulk/assign-counsellor/` | JWT G3 | Bulk counsellor assignment |
| POST | `/api/v1/group/{group_id}/adm/pipeline/bulk/send-reminder/` | JWT G3 | Bulk send reminder to selected applicants |
| GET | `/api/v1/group/{group_id}/adm/pipeline/export/` | JWT G3+ | Export filtered applications as CSV |
| GET | `/api/v1/group/{group_id}/adm/pipeline/export/pdf-summary/` | JWT G3+ | Export pipeline summary as PDF |
| POST | `/api/v1/group/{group_id}/adm/pipeline/bulk/offer-letters/` | JWT G3 | Batch generate offer letters for Offered-stage apps |
| POST | `/api/v1/group/{group_id}/adm/pipeline/applications/{application_id}/request-documents/` | JWT G3 | Send document request notification to applicant |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `/api/v1/group/{group_id}/adm/pipeline/kpis/` | `#pipeline-kpi-bar` | `innerHTML` |
| Search input (name/ID/phone) | `keyup changed delay:400ms` | GET `/api/v1/group/{group_id}/adm/pipeline/?q={val}&{filters}` | `#application-table-body` | `innerHTML` |
| Filter change (stage/branch/stream/date/counsellor) | `change` | GET `/api/v1/group/{group_id}/adm/pipeline/?{filters}` | `#application-table-body` | `innerHTML` |
| Pagination click | `click` | GET `/api/v1/group/{group_id}/adm/pipeline/?page={n}&{filters}` | `#application-table-wrapper` | `innerHTML` |
| Stage summary card click (filter) | `click` | GET `/api/v1/group/{group_id}/adm/pipeline/?stage={stage}` | `#application-table-body` | `innerHTML` |
| Application row [View] / ID click | `click` | GET `/api/v1/group/{group_id}/adm/pipeline/{app_id}/detail/` | `#application-detail-drawer` | `innerHTML` |
| Drawer tab switch | `click` | GET `/api/v1/group/{group_id}/adm/pipeline/{app_id}/detail/?tab={tab}` | `#drawer-tab-content` | `innerHTML` |
| [Move Stage] button | `click` | GET `/api/v1/group/{group_id}/adm/pipeline/{app_id}/move-stage/` | `#move-stage-modal` | `innerHTML` |
| Move stage form submit | `submit` | POST `/api/v1/group/{group_id}/adm/pipeline/{app_id}/move-stage/` | `#application-table-body` | `innerHTML` |
| [Assign Counsellor] button | `click` | GET `/api/v1/group/{group_id}/adm/pipeline/assign-counsellor/` | `#assign-counsellor-modal` | `innerHTML` |
| Assign counsellor form submit | `submit` | POST `/api/v1/group/{group_id}/adm/pipeline/{app_id}/assign-counsellor/` | `#application-table-body` | `innerHTML` |
| Bottleneck panel refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/pipeline/bottlenecks/` | `#bottleneck-panel` | `innerHTML` |
| Bulk action submit | `click` | POST `/api/v1/group/{group_id}/adm/pipeline/bulk/{action}/` | `#application-table-wrapper` | `innerHTML` |
| Sort column header click | `click` | GET `/api/v1/group/{group_id}/adm/pipeline/?sort={col}&order={dir}&{filters}` | `#application-table-body` | `innerHTML` |
| Request missing documents | `click from:#btn-request-docs` | POST `.../pipeline/applications/{id}/request-documents/` | `#document-status` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
