# Page 20: Hostel Welfare Trend Analytics

**Division:** M — Analytics & MIS
**URL:** `/group/analytics/hostel-welfare/`
**Primary Role:** 106 — Hostel Analytics Officer
**Supporting Roles:** 102 (Analytics Director), 103 (MIS Officer)
**Restricted Roles:** 104 (Academic Data Analyst), 105 (Exam Analytics Officer) — **no access** (welfare data is sensitive; academic/exam roles excluded)
**Access Level:** G1 (read-only on hostel welfare data from Division H; write only on Division M's own welfare trend notes and escalations)

---

## 1. Purpose

Tracks hostel welfare incidents, health events, complaints, and disciplinary records over time across all branches and hostels. Allows the Hostel Analytics Officer to identify welfare trend spikes, compare branch welfare profiles, and raise escalation alerts to hostel wardens and management. Data is drawn from Division H (Hostel Management) operational records via read-only G1 access.

---

## 2. Roles & Permissions Matrix

| UI Element | Role 102 | Role 103 | Role 106 |
|---|---|---|---|
| KPI bar (6 cards) | View | View | View |
| Filter bar | View + use | View + use | View + use |
| Welfare trend charts | View | View | View |
| Incident table | View | View | View |
| Incident detail drawer | View | View | View |
| Welfare trend note (add/edit/delete) | — | — | Own only |
| Escalate incident cluster | — | — | Create |
| Export (CSV / PDF) | Download | Download | Download |
| Boys/Girls filter | View (combined by default) | View | View (can separate) |

**Server-side rule:** Role 106 can only see data for hostels belonging to their assigned branches (same as page 05 and 15 enforcement). Roles 102 and 103 see all branches in the group.

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ Breadcrumb: Analytics & MIS > Hostel Welfare Trend Analytics        │
│ Title: "Hostel Welfare Trend Analytics"   [Export ▼]  [Refresh]     │
├─────────────────────────────────────────────────────────────────────┤
│  KPI BAR (6 cards)                                                   │
│  Total Incidents | Open Cases | Avg Resolution Days | Health Events │
│  Complaints (MTD) | Disciplinary (MTD)                               │
├─────────────────────────────────────────────────────────────────────┤
│  FILTER BAR                                                          │
│  Branch [All ▼]  Hostel Type [Boys/Girls/All ▼]  Category [All ▼]  │
│  Severity [All ▼]  Status [All ▼]  Date Range [This Month ▼]        │
│  [Search…]  [Apply]  [Clear]                                         │
├──────────────────────────────────┬──────────────────────────────────┤
│  WELFARE INCIDENT TREND CHART    │  CATEGORY BREAKDOWN CHART        │
│  (Line — incidents/month, 12mo)  │  (Donut — by incident category)  │
├──────────────────────────────────┴──────────────────────────────────┤
│  BRANCH WELFARE COMPARISON BAR CHART                                 │
│  (Grouped bar: incident types per branch)                            │
├─────────────────────────────────────────────────────────────────────┤
│  INCIDENT TABLE (sortable, paginated)  [+ Add Welfare Note]          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. KPI Bar

Six stat cards. Auto-refresh `hx-trigger="every 300s"`, `hx-get="/group/analytics/hostel-welfare/kpis/"`, `hx-target="#welfare-kpi-bar"`.

| # | Label | Value | Sub-label | Highlight |
|---|---|---|---|---|
| 1 | Total Incidents | Count in date range | "Selected period" | — |
| 2 | Open Cases | Currently unresolved | "Awaiting action" | `bg-red-50` if > 5 |
| 3 | Avg Resolution Days | Mean days to close | "vs last month" | Colour delta |
| 4 | Health Events | Medical / health-related incidents | "This month" | `bg-amber-50` if > 0 |
| 5 | Complaints (MTD) | Student/parent complaints | "Month to date" | — |
| 6 | Disciplinary (MTD) | Disciplinary incidents | "Month to date" | `bg-orange-50` if > 0 |

Cards 2 and 4 display in highlighted state when counts exceed safe thresholds (configurable at institution group level, default: Open > 5, Health > 0).

---

## 5. Filter Bar

| Control | Type | Options |
|---|---|---|
| Branch | Select | All + branch list (server-filtered for Role 106) |
| Hostel Type | Select | All / Boys / Girls |
| Category | Select | All / Medical / Disciplinary / Mental Health / Complaint / Accident / Fire Safety / Other |
| Severity | Select | All / Low / Medium / High / Critical |
| Status | Select | All / Open / In Progress / Resolved / Escalated |
| Date Range | Select | This Week / This Month / Last 3 Months / Last 6 Months / This Academic Year / Custom |
| Search | Text | Searches incident description and reference number |

- Date Range "Custom" reveals two date pickers (From / To). Max span: 365 days.
- `[Apply]` fires `hx-get="/group/analytics/hostel-welfare/data/"` replacing `#welfare-main-section`.
- Hostel Type default is "All" for Roles 102 and 103; default is "All" for Role 106 too but Boys/Girls toggle is prominent.

---

## 6. Welfare Incident Trend Chart

**Type:** Multi-line chart (Chart.js 4.x Line)
**Canvas ID:** `welfareTrendChart`
**Height:** 280px

- X-axis: Months (last 12 months, oldest → newest).
- Y-axis: Incident count.
- Lines: Medical (amber), Disciplinary (red), Complaints (blue), Other (grey).
- Data points: circles, hover tooltip: `{Category}: {count} in {Month}`.
- Legend: top, horizontal.
- Clicking a data point filters the incident table to that month + category.
- If "Boys / Girls" split is active (Hostel Type filter), lines are shown as solid (Boys) and dashed (Girls).

---

## 7. Category Breakdown Chart

**Type:** Donut chart (Chart.js 4.x Doughnut)
**Canvas ID:** `welfareCategoryChart`
**Height:** 280px

- Slices: one per incident category within filter scope.
- Colorblind-safe Okabe-Ito palette.
- Centre label: total incident count.
- Tooltip: `{Category}: {count} ({percent}%)`.
- Clicking a slice filters the incident table to that category.
- Legend: right side, vertical.

---

## 8. Branch Welfare Comparison Chart

**Type:** Grouped bar chart (Chart.js 4.x Bar)
**Canvas ID:** `branchWelfareChart`
**Height:** 300px

- X-axis: Branch names.
- Y-axis: Incident count.
- Groups: Medical (amber), Disciplinary (red), Complaints (blue).
- Horizontal orientation if > 6 branches (switches to `indexAxis: 'y'`).
- Tooltip: `{Branch} — {Category}: {count}`.
- Clicking a branch bar filters the incident table to that branch.

---

## 9. Incident Table

### 9.1 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Integer | No | Row number |
| Ref No | Text | No | e.g. HW-2026-00341 |
| Branch | Text | Yes | — |
| Hostel | Text | Yes | Boys/Girls + block |
| Category | Badge | Yes | Colour-coded |
| Severity | Badge | Yes | Low/Med/High/Critical |
| Description | Text | No | Truncated 80 chars; full in tooltip |
| Reported Date | Date | Yes | — |
| Status | Badge | Yes | Open / In Progress / Resolved / Escalated |
| Resolution Days | Integer | Yes | Null if unresolved |
| Actions | Buttons | No | [View] [Escalate] (Role 106) |

### 9.2 Controls

- **Search:** `hx-get` with `delay:300ms` on `keyup changed`.
- **Sort:** HTMX replaces tbody on header click.
- **Pagination:** 20 rows per page, server-side.
- **Row click:** opens incident detail drawer.
- **[Escalate]:** Role 106 only — opens drawer on Escalation tab.

### 9.3 Pagination

```
hx-get="/group/analytics/hostel-welfare/incidents/"
hx-target="#welfare-incident-tbody"
hx-swap="outerHTML"
hx-include="#welfare-filter-form"
```

---

## 10. Incident Detail Drawer

**ID:** `welfare-incident-detail-drawer`
**Width:** 640px slide-in from right
**Header:** `[Severity badge] {Ref No} — {Category}`

### Tab 1 — Incident Overview

| Field | Value |
|---|---|
| Reference No | Text |
| Branch | Text |
| Hostel | Text (type + block) |
| Student Ref | Masked: "Hostel Student #4421" (name hidden for privacy; full name visible only in Division H portal) |
| Category | Badge |
| Severity | Badge |
| Date Reported | Formatted datetime |
| Reported By | Role label (e.g. "Hostel Warden") |
| Description | Full text |
| Action Taken | Text (from Division H; read-only) |
| Status | Badge |
| Resolution Date | Date or "—" |
| Resolution Notes | Text or "—" |
| Days to Resolve | Integer or "Open" |

**Privacy note banner:** "Student identity is masked per welfare data privacy policy. Full details available to Division H staff only." — shown as a blue `bg-blue-50` info banner at the top of this tab.

### Tab 2 — Branch Welfare Context

Shows the welfare profile of the branch for contextual comparison:

| Metric | Value |
|---|---|
| Total Incidents (YTD) | Integer |
| Open Cases | Integer |
| Most Common Category | Text + badge |
| Avg Resolution Days | Float |
| Welfare Score | 0–100 (from Branch Health Scorecard, Welfare dimension) |

**Mini trend chart:** Bar chart showing this branch's monthly incident count for last 6 months. Canvas id: `branchContextChart`.

**Similar Incidents:** Table of last 5 incidents of the same category in this branch: Ref No | Date | Status.

### Tab 3 — Escalation

**Role 106 only** — others see read-only list of existing escalations for this incident.

**Existing escalations:** table: Level | Assigned To | Status | Date | Resolution.

**Create Escalation form:**

| Field | Type | Validation |
|---|---|---|
| Incident Ref | Read-only | — |
| Escalation Level | Select: Branch Warden / Principal / Management / External Authority | Required |
| Urgency | Select: Routine / Urgent / Emergency | Required |
| Summary | Textarea (max 500 chars) | Required, min 20 chars |
| Recommended Action | Textarea (max 500 chars) | Required |
| Assign To | Select (relevant roles based on level selected) | Required |
| Target Response Date | Date picker (min: today, max: today + 30 days) | Required |
| Notify via | Checkbox: In-app / Email | ≥ 1 required |

Submit: POST `/api/v1/analytics/hostel-welfare/escalations/` → toast → escalation row prepended to list.

---

## 11. Welfare Trend Notes

Below the incident table. Allows Role 106 to attach analytical notes to a branch-month combination (e.g. "Spike in April due to exam stress period").

**Notes Table Columns:**

| Column | Notes |
|---|---|
| Branch | Text |
| Period | Month-Year |
| Category | Badge |
| Note | Truncated 120 chars |
| Added By | Name |
| Date Added | Formatted date |
| Actions | Edit / Delete (Role 106 own notes only) |

**Pagination:** 10 rows per page.

**[+ Add Welfare Note] Drawer (Role 106 only):**

| Field | Type | Validation |
|---|---|---|
| Branch | Select | Required |
| Hostel Type | Select: Boys / Girls / Both | Required |
| Period (Month-Year) | Month picker | Required |
| Category | Select (incident category list) | Required |
| Note Text | Textarea (max 600 chars) | Required, min 20 chars |
| Visibility | Radio: "Division M only" / "Visible to Division H" | Required |

Submit: POST `/api/v1/analytics/hostel-welfare/notes/` → success toast → row prepended.
Edit: PUT endpoint (same form pre-filled).
Delete: confirm modal → DELETE → row removed + toast.

---

## 12. Export Modal

| Option | Endpoint |
|---|---|
| Export Incident List (CSV) | GET `/api/v1/analytics/hostel-welfare/export/?format=csv` |
| Export Trend Report (PDF) | POST `/api/v1/analytics/hostel-welfare/export/` → async job |
| Export Category Breakdown (CSV) | GET `/api/v1/analytics/hostel-welfare/categories/export/` |
| Export Escalations (CSV) | GET `/api/v1/analytics/hostel-welfare/escalations/export/` |

PDF export follows standard async pattern: POST → job_id → poll every 5s → download on complete.

Privacy notice in PDF: "This report contains aggregated welfare data. Individual student identities are not included."

---

## 13. Toast Notifications

| Trigger | Type | Message |
|---|---|---|
| Escalation created | Success | "Escalation raised for {Ref No}. Assigned to {Assignee}." |
| Note saved | Success | "Welfare note saved for {Branch} — {Period}." |
| Note updated | Success | "Note updated." |
| Note deleted | Info | "Note removed." |
| Form validation fail | Error | "Please fill in all required fields." |
| Export started | Info | "Preparing export…" |
| Export ready | Success | "Export ready. Click to download." |
| Export failed | Error | "Export failed. Please try again." |
| Data load error | Error | "Failed to load welfare data. Retrying in 30s." |

---

## 14. Empty States

| Context | Message | CTA |
|---|---|---|
| No incidents in filter scope | "No welfare incidents found for the selected filters." | "Reset Filters" |
| No open cases | "No open welfare cases. All incidents resolved." with green checkmark | — |
| No escalations for incident | "No escalations raised for this incident." | "Create Escalation" (Role 106) |
| No welfare notes | "No trend notes added yet for this period." | "+ Add Note" (Role 106) |
| Branch data unavailable | "Welfare data for this branch is not available for the selected period." | — |

---

## 15. Loader States

| Element | Loader |
|---|---|
| Initial page load | Full skeleton: 6 card shimmer + filter shimmer + 3 chart placeholders + table shimmer (20 rows) |
| Table reload (filter/sort/page) | Table body shimmer (20 rows) |
| KPI bar refresh | Individual card shimmer |
| Drawer open | Spinner centred in drawer |
| Tab switch | Tab content shimmer |
| Chart refresh | Canvas grey overlay with spinner |
| PDF export | Progress indicator in modal |

---

## 16. HTMX Patterns

| Pattern | Target | Endpoint | Trigger |
|---|---|---|---|
| Full section reload on Apply | `#welfare-main-section` | `/group/analytics/hostel-welfare/data/` | Apply button |
| KPI auto-refresh | `#welfare-kpi-bar` | `/group/analytics/hostel-welfare/kpis/` | `every 300s` |
| Incident table search | `#welfare-incident-tbody` | `/group/analytics/hostel-welfare/incidents/` | `keyup changed delay:300ms` |
| Incident table pagination | `#welfare-incident-tbody` | `/group/analytics/hostel-welfare/incidents/?page={n}` | Page nav |
| Incident table sort | `#welfare-incident-tbody` | `/group/analytics/hostel-welfare/incidents/?sort={col}&dir={asc/desc}` | Header click |
| Drawer open | `#welfare-incident-detail-drawer` | `/group/analytics/hostel-welfare/incidents/{id}/detail/` | Row click / [View] |
| Escalation POST | `#escalation-form` | `/api/v1/analytics/hostel-welfare/escalations/` | Form submit |
| Note POST | `#welfare-note-form` | `/api/v1/analytics/hostel-welfare/notes/` | Form submit |
| Notes pagination | `#welfare-notes-tbody` | `/group/analytics/hostel-welfare/notes/?page={n}` | Page nav |
| Export poll | `#export-status` | `/api/v1/analytics/export-jobs/{id}/status/` | `every 5s` (stop on complete) |

---

## 17. API Endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | `/api/v1/analytics/hostel-welfare/` | Full page data | G1 (106 filtered) |
| GET | `/api/v1/analytics/hostel-welfare/kpis/` | KPI values | G1 |
| GET | `/api/v1/analytics/hostel-welfare/incidents/` | Paginated incident list | G1 |
| GET | `/api/v1/analytics/hostel-welfare/incidents/{id}/detail/` | Incident detail + context | G1 |
| GET | `/api/v1/analytics/hostel-welfare/charts/` | Chart datasets | G1 |
| GET | `/api/v1/analytics/hostel-welfare/escalations/` | Escalation list | G1 |
| POST | `/api/v1/analytics/hostel-welfare/escalations/` | Create escalation | Role 106 |
| GET | `/api/v1/analytics/hostel-welfare/notes/` | Notes list | G1 |
| POST | `/api/v1/analytics/hostel-welfare/notes/` | Add note | Role 106 |
| PUT | `/api/v1/analytics/hostel-welfare/notes/{id}/` | Edit note | Role 106 (own) |
| DELETE | `/api/v1/analytics/hostel-welfare/notes/{id}/` | Delete note | Role 106 (own) |
| GET | `/api/v1/analytics/hostel-welfare/export/` | CSV export | G1 |
| POST | `/api/v1/analytics/hostel-welfare/export/` | Async PDF export | G1 |
| GET | `/api/v1/analytics/hostel-welfare/categories/export/` | Category breakdown CSV | G1 |
| GET | `/api/v1/analytics/hostel-welfare/escalations/export/` | Escalations CSV | G1 |
| GET | `/api/v1/analytics/export-jobs/{id}/status/` | Poll export job | G1 |

---

## 18. Mobile (Flutter + Riverpod)

| Screen | Description |
|---|---|
| `HostelWelfareHomeScreen` | KPI cards + category donut chart |
| `WelfareIncidentListScreen` | Filterable, searchable incident list with severity badges |
| `WelfareIncidentDetailScreen` | Incident overview tab (Tab 1 only); masked student identity |
| `BranchWelfareSummaryScreen` | Branch comparison bar chart |

State provider: `hostelWelfareProvider` (Riverpod). Pull-to-refresh. No write actions on mobile.

---

## 19. Accessibility & Responsiveness

- "Boys" and "Girls" split is communicated with both colour (blue/pink) and text labels — never colour alone.
- Incident severity badges use colour + text + `aria-label`.
- Table scrolls horizontally on mobile; essential columns (Category, Severity, Status, Date) remain visible, others hidden on < 768px.
- Privacy banner (`role="note"`) is always visible before student-related fields.
- Drawer closes on `Escape`; focus trap active while drawer open.
- All form fields: visible labels, `aria-required`, inline error messages.
- Chart canvases: `role="img"`, descriptive `aria-label`.
