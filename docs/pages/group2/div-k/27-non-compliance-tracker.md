# 27 — Non-Compliance Tracker

> **URL:** `/group/welfare/safety-audit/non-compliance/`
> **File:** `27-non-compliance-tracker.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Safety Audit Officer (Role 96, G1)

---

## 1. Purpose

Tracks all non-compliance items identified across inspection reports and monitors their corrective action status from identification to verified resolution. Every Non-Compliant or Partial checklist item from an inspection report (page 26) auto-generates a non-compliance record here at the moment of report submission.

Each non-compliance record contains: severity classification, corrective action required, responsible party (the role within the branch responsible for fixing the issue), target resolution date (computed from severity SLA), current status, and a full activity log from creation through to verification and closure.

**Resolution SLA by severity:**

| Severity | Label | Example Issues | Resolution SLA |
|---|---|---|---|
| Critical | Immediate safety threat | Blocked fire exit, missing extinguisher in a lab, exposed live wiring, structural crack in load-bearing wall | 30 days |
| High | Significant safety gap | Expired extinguishers, faulty fire alarm, unsafe sports equipment, pest infestation in kitchen | 60 days |
| Medium | Maintenance deficiency | Drainage issue, worn playground surface, overloaded extension cords, poor lighting in hostel corridor | 90 days |
| Low | Minor or cosmetic | Missing signage, minor documentation gap, single worn-out floor marking | 120 days |

**The Safety Audit Officer (G1) cannot directly fix issues** — they cannot edit the branch's operational systems. Their role is: monitor, annotate, verify reported resolutions, and escalate overdue items to the Group COO. Branch Principals (or their designated maintenance/department heads) update resolution status in their branch portal. The Safety Audit Officer verifies that reported resolutions are genuine.

**Automatic escalation:** Critical items open for > 30 days are automatically escalated to the Group COO. This escalation is also available as a manual action.

Scale: Each inspection report generates 2–30 NC items. Across 20–50 branches with full audits + targeted visits, this means 100–1,500 active NC records at any point in the year.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Safety Audit Officer | G1 | Read all + add annotation notes + verify resolved items + escalate | Cannot update item status (that is branch role) |
| Branch Principal | Branch | Read own branch NCs + update status (In Progress / Resolved) | Cannot update other branches' items |
| Branch Maintenance Head | Branch | Read own branch NCs + update status | Delegated by Branch Principal for maintenance-category items |
| Group COO | G4 | Read all + receive escalation notifications | No create; no status update |
| All other roles | — | No access | — |

> **Access enforcement:** `@require_role('safety_audit_officer', 'branch_principal', 'branch_maintenance_head', 'coo')`. Branch Principal and Branch Maintenance Head see only their own branch's records (queryset filtered by `branch_id`). Status update endpoints enforce branch ownership — a PATCH from Branch Principal to another branch's NC returns 403.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Safety Audit  ›  Non-Compliance Tracker
```

### 3.2 Page Header
- **Title:** `Non-Compliance Tracker`
- **Subtitle:** `[N] Open NCs · [N] Critical · [N] Overdue · Last updated [timestamp]`
- **Right controls:** `Advanced Filters` · `Export CSV` (Safety Audit Officer + COO)

> **Note:** No "create" button — NC records are only generated automatically from inspection report submissions.

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Critical NC open > 30 days | "[N] Critical non-compliance items are overdue (> 30 days). COO has been auto-notified. Verify status urgently." | Red (persistent) |
| High NC open > 60 days | "[N] High-severity non-compliance items have breached their 60-day SLA." | Red |
| Branch with most overdue NCs | "[Branch] has the most overdue non-compliance items ([N]). A site follow-up visit may be required." | Amber |
| No update in 14 days (High/Critical) | "[N] Critical or High NCs have had no status update in over 14 days." | Amber |

---

## 4. KPI Summary Bar

Eight cards in a responsive 4×2 grid.

| # | Card | Metric | Colour Rule |
|---|---|---|---|
| 1 | Total Open NCs | Count of all NCs with status ≠ Closed | Red > 50 · Yellow 20–50 · Green < 20 |
| 2 | Critical Open | Count of Critical NCs with status ≠ Closed | Red > 0 · Green = 0 |
| 3 | High Priority Open | Count of High NCs with status ≠ Closed | Red > 5 · Yellow 1–5 · Green = 0 |
| 4 | Overdue Count | Count where today > target_date and status ≠ Resolved/Closed | Red > 0 · Green = 0 |
| 5 | Resolved This Month | Count of NCs moved to Resolved in current calendar month | Green always |
| 6 | Avg Days to Resolve (Critical) | Mean days from NC creation to Resolved status for Critical items closed this year | Green ≤ 20 · Yellow 20–30 · Red > 30 |
| 7 | Branches with Most Open NCs | Mini bar chart — top 5 branches by open NC count | Visual only |
| 8 | Open NCs by Severity | Mini donut: Critical / High / Medium / Low proportions | Visual only |

---

## 5. Main Table — Non-Compliance Records

### 5.1 Search
Full-text search on: NC ID, Branch Name, Item Description, Inspection Report ID. Debounce 300 ms, minimum 2 characters.

### 5.2 Advanced Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Category | Checkbox | Fire · Building · Electrical · Playground · Hostel · Transport · Food · Lab |
| Severity | Checkbox | Critical · High · Medium · Low |
| Status | Checkbox | Open · In Progress · Resolved · Verified · Closed · Overdue |
| Overdue Only | Toggle | Yes / No |
| Date Range (Target Date) | Date picker | From – To |
| Responsible Party | Multi-select | Branch Principal / Maintenance Team / IT / Kitchen Staff / Transport Team / Other |
| Academic Year | Single-select | Current + 2 prior years |
| Days Overdue Range | Number inputs | From – To |

### 5.3 Table Columns

| Column | Sortable | Notes |
|---|---|---|
| NC ID | ✅ | System-generated (e.g., NC-2026-00412); auto-created on report submission |
| Branch | ✅ | |
| Report ID | ✅ | Link to inspection report (page 26) |
| Category | ✅ | Tag badge |
| Item Description | ❌ | Truncated to 80 chars; full text on hover |
| Severity | ✅ | Critical (red) · High (orange) · Medium (amber) · Low (grey) bold badge |
| Responsible Party | ✅ | Role label |
| Target Date | ✅ | DD-MMM-YYYY; red if overdue |
| Days Overdue | ✅ | Integer (shown only if overdue); "−" if within SLA |
| Status | ✅ | Open (blue) · In Progress (purple) · Resolved (green) · Verified (teal) · Closed (dark grey) · Overdue (red) badge |
| Last Update | ✅ | Relative time |
| Actions | ❌ | View · Add Note · Verify · Escalate (Safety Audit Officer) / Update Status (Branch roles) |

**Default sort:** Severity descending (Critical → Low), then Days Overdue descending, then Target Date ascending.
**Pagination:** Server-side · 25 rows/page.
**Row highlight:** Overdue rows have a red left border; Critical open rows have a persistent red left border.

### 5.4 Charts Panel (collapsible, above table)

- **Bar chart (open NCs by branch):** Horizontal bars — each branch, bar length = open NC count, colour = proportion of critical (red sub-bar)
- **Pie chart (open NCs by severity):** Critical / High / Medium / Low donut
- **Trend line (new vs resolved, 12 months):** Two lines — "New NCs Created" and "NCs Resolved" per month; gap between lines = backlog growth; ideal state is lines overlapping

---

## 6. Drawers / Modals

### 6.1 Drawer — `nc-detail` (640px, right side)

Triggered by **View** in Actions column.

**Header:** NC ID · Severity badge · Status badge · Branch

| Field | Notes |
|---|---|
| NC ID | Read-only |
| Created Date | Date NC was auto-generated (= inspection report submission date) |
| Source Inspection Report | Link to report (page 26) |
| Source Checklist Item | Item reference + full description |
| Branch | |
| Category | |
| Severity | Badge with label |
| Item Description | Full text of the non-compliant checklist item |
| Inspector Notes (at time of inspection) | Free text from inspection report |
| Photos from Inspection | Thumbnail gallery (view-only); same photos as in inspection report for this item |
| Corrective Action Required | Inspector's recommended action |
| Responsible Party | |
| Target Resolution Date | Computed: creation date + SLA days by severity |
| Days Overdue | If applicable |
| Current Status | Badge |

**Activity Log section (below fields):**
Chronological, immutable timeline — all status updates, notes, verification actions.

| Column | Notes |
|---|---|
| Timestamp | DD-MMM-YYYY HH:MM |
| Actor | Name + Role |
| Action | Status Change / Note Added / Escalated / Verified / Photo Added |
| Detail | Free text or old → new status change description |

**Footer actions:**
- Safety Audit Officer: `Add Note` · `Verify Resolved` · `Escalate to COO`
- Branch Principal / Maintenance Head: `Update Status`

---

### 6.2 Drawer — `add-nc-note` (400px, right side)

Triggered by **Add Note** in Actions column or NC detail footer. Safety Audit Officer only.

| Field | Type | Validation |
|---|---|---|
| NC ID | Read-only | |
| Branch | Read-only | |
| Current Status | Read-only badge | |
| Note | Textarea (max 1,000 chars) — progress observation, site follow-up note, communication record | Required |
| Note Category | Radio: Progress Observation · Communication with Branch · Follow-up Visit Note · Verification Query | Required |
| Share with Branch Principal | Toggle (default: Yes) | Optional |
| Attachment | File upload (PDF/JPG/PNG, max 5 MB) | Optional |

**Footer:** `Cancel` · `Add Note`

**Behaviour:** Note appended to Activity Log; if Share = Yes, Branch Principal receives notification with note text.

---

### 6.3 Drawer — `verify-resolved` (440px, right side)

Triggered by **Verify** in Actions column (appears when branch has set status = Resolved). Safety Audit Officer only.

| Field | Type | Validation |
|---|---|---|
| NC ID | Read-only | |
| Item Description | Read-only | |
| Branch's Resolution Note | Read-only — what the branch said they did | |
| Branch Resolution Date | Read-only | |
| Branch Photo Evidence | View-only gallery (photos submitted by branch as resolution proof) | |
| Verification Decision | Radio: Verified — Close NC · Not Verified — Reopen · Needs Site Visit | Required |
| Verification Notes | Textarea (max 1,000 chars) | Required |
| Site Visit Required | Toggle (shown if Needs Site Visit selected) | Conditional |
| Site Visit Planned Date | Date picker | Required if Site Visit = Yes |

**Footer:** `Cancel` · `Save Verification`

**Behaviour:**
- If Verified: Status → Closed; Branch Principal notified; NC removed from open counts
- If Not Verified: Status → Open; branch notified with reason; Days Overdue counter continues
- If Needs Site Visit: Status → In Progress (Verification Pending); follow-up inspection plan entry suggested

---

### 6.4 Modal — `escalate-overdue` (400px, centred)

Triggered by **Escalate** in Actions column or automatically when Critical NC > 30 days. Safety Audit Officer only.

| Field | Type | Validation |
|---|---|---|
| NC ID | Read-only | |
| Branch | Read-only | |
| Item Description | Read-only | |
| Severity | Read-only badge | |
| Days Overdue | Read-only | |
| Escalation Type | Read-only: Manual / Auto | |
| Escalation Note | Textarea (max 500 chars) — what the coordinator wants to communicate to the COO | Required |
| Escalate To | Read-only: Group COO (always); checkbox to also notify Branch Principal | |

**Footer:** `Cancel` · `Send Escalation`

**Behaviour:** Escalation notification sent to COO + optionally Branch Principal. Escalation record appended to Activity Log. NC Status updated to "Overdue — Escalated". Auto-escalation: same logic triggered server-side by a scheduled background task running every 30 minutes; escalation note is auto-filled as: *"Auto-escalation: this Critical non-compliance item has been open for [N] days, exceeding the 30-day resolution SLA."*

**Branch status update drawer** (shown to Branch Principal and Branch Maintenance Head — not Safety Audit Officer):

### 6.5 Drawer — `update-nc-status` (420px, right side)

Shown in Actions column as **Update Status** for Branch roles only.

| Field | Type | Validation |
|---|---|---|
| NC ID | Read-only | |
| Item Description | Read-only | |
| Current Status | Read-only badge | |
| New Status | Radio: In Progress · Resolved | Required; cannot select Open, Verified, or Closed (those are Safety Audit Officer states) |
| Action Taken | Textarea (max 1,000 chars) — what the branch has done | Required |
| Completed Date | Date picker | Required if Resolved |
| Photo Evidence | File upload (up to 3 photos, JPEG/PNG, max 5 MB each) | Required if Resolved |
| Acknowledgment | Checkbox: "I confirm that the corrective action has been completed and the issue is resolved." | Required if Resolved |

**Footer:** `Cancel` · `Save Update`

**Behaviour:** On save, Activity Log updated; Safety Audit Officer receives notification that the branch has reported a resolution — prompts verification step.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Note added | "Note added to NC [ID]." | Success |
| NC verified and closed | "NC [ID] verified. Non-compliance closed." | Success |
| NC reopened (not verified) | "NC [ID] has been reopened. Branch has been notified of the reason." | Warning |
| Verification requires site visit | "NC [ID] marked as needing a site visit. Follow-up inspection suggested." | Info |
| Escalation sent (manual) | "Escalation notification sent to Group COO for NC [ID]." | Warning |
| Auto-escalation triggered | "Auto-escalation sent for NC [ID] — [N] days overdue." | Warning |
| Branch status updated (In Progress) | "NC [ID] status updated to In Progress. Safety Audit Officer notified." | Success |
| Branch reported resolved | "NC [ID] reported as Resolved. Safety Audit Officer will verify." | Success |
| Photo evidence uploaded | "Photo evidence uploaded for NC [ID]." | Success |
| Export triggered | "Export is being prepared." | Info |
| Validation error | "Please complete all required fields before saving." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No NCs for current filters | "No non-compliance records match the current filters." | "Try adjusting or clearing your filters." | `Clear Filters` button |
| No open NCs | "No open non-compliance items." | "All identified non-compliances have been resolved and verified." | — |
| No Critical or High NCs | "No Critical or High severity items open." | "Only Medium and Low items remain, if any." | — |
| NC detail — no activity log entries yet | "No activity logged yet." | "Notes and status changes will appear here." | — |
| Verify drawer — no photo evidence | "The branch has not submitted photographic evidence." | "Request the branch to upload resolution photos before verifying." | — |
| Charts — no open NCs for bar chart | "No open NCs to display." | "All non-compliance items have been resolved." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 8 KPI cards + 3 chart placeholders + table (10 grey rows × 12 columns) |
| Filter / search apply | Table body spinner overlay; KPI + charts refresh after |
| NC detail drawer open | Drawer skeleton: 12 grey field rows + activity log skeleton (3 grey entries) |
| Activity log load | Skeleton: 5 grey timeline entries (alternating indent) |
| Photo evidence gallery load | Grid skeleton: 3 grey thumbnail rectangles |
| Add note submit | Drawer footer spinner; resolves to success toast + drawer close |
| Verify submit | Drawer footer spinner + "Processing verification…"; button disabled |
| Escalation submit | Modal footer spinner + "Sending notification…" |
| Update status submit (branch) | Drawer footer spinner + "Saving…" |
| Charts load | Bar: horizontal grey bars; Pie: grey donut; Trend: grey dual-line placeholder |

---

## 10. Role-Based UI Visibility

| UI Element | Safety Audit Officer | Branch Principal | Branch Maintenance Head | COO |
|---|---|---|---|---|
| Full cross-branch NC list | ✅ | Own branch only | Own branch only | ✅ (read) |
| Add Note button | ✅ | ❌ | ❌ | ❌ |
| Verify button | ✅ | ❌ | ❌ | ❌ |
| Escalate button | ✅ | ❌ | ❌ | ❌ |
| Update Status button | ❌ | ✅ | ✅ | ❌ |
| Activity log (full) | ✅ | ✅ (own branch) | ✅ (own branch) | ✅ |
| Photo evidence (inspection) | ✅ | ✅ | ✅ | ✅ |
| Photo evidence upload (resolution) | ❌ | ✅ | ✅ | ❌ |
| KPI bar — full detail | ✅ | Own branch metrics | Own branch metrics | ✅ |
| Chart panel | ✅ | Own branch | Own branch | ✅ |
| Alert banners — all | ✅ | Own branch | Own branch | Critical / overdue |
| Export CSV | ✅ | ❌ | ❌ | ✅ |
| NC auto-escalation notifications | Triggered by + receives copy | ❌ | ❌ | Receives notification |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/welfare/safety/non-compliance/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/safety/non-compliance/` | List NC records (paginated, filtered, role-scoped) | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/safety/non-compliance/{nc_id}/` | Retrieve NC detail + activity log | JWT + role check |
| POST | `/api/v1/group/{group_id}/welfare/safety/non-compliance/{nc_id}/notes/` | Add note (Safety Audit Officer only) | Safety Audit Officer |
| POST | `/api/v1/group/{group_id}/welfare/safety/non-compliance/{nc_id}/verify/` | Verify resolved NC | Safety Audit Officer |
| POST | `/api/v1/group/{group_id}/welfare/safety/non-compliance/{nc_id}/escalate/` | Manual escalation to COO | Safety Audit Officer |
| PATCH | `/api/v1/group/{group_id}/welfare/safety/non-compliance/{nc_id}/status/` | Update NC status (branch roles: In Progress / Resolved only) | Branch Principal / Branch Maintenance Head |
| POST | `/api/v1/group/{group_id}/welfare/safety/non-compliance/{nc_id}/photos/` | Upload resolution photo evidence (branch roles) | Branch Principal / Branch Maintenance Head |
| GET | `/api/v1/group/{group_id}/welfare/safety/non-compliance/kpi/` | KPI summary bar | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/safety/non-compliance/charts/` | All 3 chart datasets (bar + pie + trend) | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/safety/non-compliance/alerts/` | Active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/welfare/safety/non-compliance/export/` | Export CSV | Safety Audit Officer / COO |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Filter by branch ID(s) |
| `category` | str[] | Category slugs |
| `severity` | str[] | `critical`, `high`, `medium`, `low` |
| `status` | str[] | `open`, `in_progress`, `resolved`, `verified`, `closed`, `overdue` |
| `overdue_only` | bool | Only overdue items |
| `target_date_from` | date | Target date range start |
| `target_date_to` | date | Target date range end |
| `responsible_party` | str[] | Responsible party slugs |
| `academic_year` | str | e.g., `2025-26` |
| `days_overdue_min` | int | Minimum days overdue |
| `days_overdue_max` | int | Maximum days overdue |
| `report_id` | str | Filter by source inspection report ID |
| `page` | int | Page number |
| `page_size` | int | Default 25, max 100 |
| `search` | str | NC ID, branch, item description, report ID |
| `sort_by` | str | Column name; prefix `-` for descending |

**Auto-escalation job:** A Django management command (`escalate_overdue_ncs`) runs every 30 minutes via a scheduled task. It queries Critical NCs where `status NOT IN ('resolved', 'verified', 'closed')` and `today > target_date` and `escalation_sent = False`. For each found: POST to `/api/.../non-compliance/{nc_id}/escalate/` with `type=auto`; sets `escalation_sent=True`.

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search input | `hx-get="/api/.../non-compliance/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#nc-table-body"` `hx-include="#filter-form"` | Table body replaced |
| Filter apply | `hx-get="/api/.../non-compliance/"` `hx-trigger="change"` `hx-target="#nc-table-body"` `hx-include="#filter-form"` | Table + KPI + charts refreshed |
| Pagination | `hx-get="/api/.../non-compliance/?page={n}"` `hx-target="#nc-table-body"` `hx-push-url="true"` | Page swap |
| NC detail drawer open | `hx-get="/api/.../non-compliance/{nc_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in |
| Activity log load | `hx-get="/api/.../non-compliance/{nc_id}/?tab=activity"` `hx-target="#activity-log-container"` `hx-trigger="load"` | Timeline loaded |
| Add note submit | `hx-post="/api/.../non-compliance/{nc_id}/notes/"` `hx-target="#activity-log-container"` `hx-swap="afterbegin"` | New note prepended to activity log; drawer stays open |
| Verify resolved submit | `hx-post="/api/.../non-compliance/{nc_id}/verify/"` `hx-target="#nc-row-{nc_id}"` `hx-swap="outerHTML"` | Row status badge updated; drawer closes; toast fires |
| Escalation submit | `hx-post="/api/.../non-compliance/{nc_id}/escalate/"` `hx-target="#escalation-result"` `hx-indicator="#escalation-spinner"` | Result shown in modal; modal closes on success |
| Branch status update submit | `hx-patch="/api/.../non-compliance/{nc_id}/status/"` `hx-target="#nc-row-{nc_id}"` `hx-swap="outerHTML"` | Row updated; drawer closes |
| Branch photo upload | `hx-post="/api/.../non-compliance/{nc_id}/photos/"` `hx-encoding="multipart/form-data"` `hx-target="#resolution-photo-gallery"` `hx-swap="beforeend"` | Thumbnail appended |
| KPI bar refresh | `hx-get="/api/.../non-compliance/kpi/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#kpi-bar"` | On load and post-filter |
| Charts load | `hx-get="/api/.../non-compliance/charts/"` `hx-trigger="load, filterApplied from:body"` `hx-target="#chart-panel"` | All 3 charts updated |
| Alert banner load | `hx-get="/api/.../non-compliance/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | Conditional banner |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
