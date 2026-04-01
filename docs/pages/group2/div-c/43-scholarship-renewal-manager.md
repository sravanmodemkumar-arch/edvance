# 43 — Scholarship Renewal Manager

> **URL:** `/group/adm/scholarship-renewals/`
> **File:** `43-scholarship-renewal-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Group Scholarship Manager (Role 27) — primary

---

## 1. Purpose

Most scholarships are not one-time awards — they are renewed each academic year or each term, contingent on the student maintaining the performance or eligibility standard defined in their scheme. A merit scholarship holder who drops below 75% in their annual examination may lose their award for the following year. A need-based scholarship student must resubmit current income documentation annually for the entitlement to continue. An RTE-quota beneficiary must continue to meet government-defined criteria. The Scholarship Renewal Manager is the centralised page where all of these renewal cycles across all active schemes and all 50 branches are processed in a single workflow — eliminating the need for the Scholarship Manager to communicate with each branch separately or manage renewal decisions through spreadsheets.

At the start of each renewal window (as configured in the scheme's renewal settings in the Scholarship Registry, Page 22), the system automatically identifies every scholarship holder due for renewal and generates a renewal batch for the current cycle. The Scholarship Manager opens this page to see the full batch in the Renewal Batch Table (Section 5.1), where each student's latest academic performance data — pulled live from the results module — is displayed alongside the scheme's renewal threshold. Students who clearly meet the criteria are marked "Meets Criteria: Yes"; those who clearly fall below are marked "No"; those within 3 percentage points of the threshold are marked "Borderline" and routed automatically to the dedicated Borderline Cases Queue (Section 5.3). The Manager batch-approves the clearly eligible group, applies focused individual review to borderline cases (granting grace extensions where the academic record and trajectory support it), and discontinues awards for students who cannot be retained within scheme rules.

Managing renewals for over 1,000 scholarship holders across 50 branches requires tools that make bulk operations both fast and safe. The batch approval confirmation modal requires the Manager to review the total renewal financial commitment before confirming — preventing accidental mass-approval without financial awareness. The Renewal Notification Status panel (Section 5.5) tracks which students have been informed of their renewal outcome and which are still awaiting communication, ensuring no student is left uninformed about the continuation or discontinuation of a financial award they depend on.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Manager (Role 27) | G3 | Full access — approve, discontinue, extend grace, adjust amounts, notify | Primary operator |
| Group Admissions Director (Role 23) | G3 | View all + override any decision | Cannot initiate batch; can override individual renewals |
| CFO / Finance | G3+ | View only — renewal amounts and financial summary | Read-only; only sees Scheme Summary (5.2) and financial columns in 5.1 |
| Group Admission Counsellor (Role 25) | G3 | View own assigned students' renewal status only | Read-only; no decision actions |
| School Principal (Branch) | G2 | View own branch students' renewal status only | Read-only; scoped to their branch via portal |
| Group Admission Coordinator (Role 24) | G3 | No access | Not in scope |

> **Enforcement:** `@role_required(['scholarship_manager', 'admissions_director', 'cfo', 'counsellor', 'branch_principal'])` at the Django view level. Approve, discontinue, and grace-extension endpoints require `request.user.role in ['scholarship_manager', 'admissions_director']`. CFO queryset presents only financial columns with `renewal_readonly=True` in template context. Counsellor queryset filtered: `RenewalRecord.objects.filter(student__assigned_counsellor=request.user)`. Branch Principal queryset filtered: `RenewalRecord.objects.filter(student__branch=request.user.branch)`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal › Admissions › Scholarships › Scholarship Renewal Manager
```

### 3.2 Page Header
- **Title:** Scholarship Renewal Manager
- **Subtitle:** Annual renewal processing for all active scholarship holders — `{current_renewal_cycle_name}`
- **Right-side controls:**
  - `[Approve All Eligible →]` (Scholarship Manager only — batch approves all "Meets Criteria: Yes" pending records)
  - `[Export Renewal List ↓]`
  - `[Send Notifications to All Decided →]` (Scholarship Manager only)
  - `[Refresh ↺]`

### 3.3 Alert Banner

Collapsible panel above the KPI row. `bg-red-50 border-l-4 border-red-500` for Critical; `bg-yellow-50 border-l-4 border-yellow-400` for Warning; `bg-blue-50 border-l-4 border-blue-400` for Info.

| Trigger | Severity | Message |
|---|---|---|
| Renewal deadline < 14 days with pending records remaining | Critical | "Renewal deadline is {N} days away — {X} students still have pending decisions. [View Pending →]" |
| Borderline cases > 0 with no action | Warning | "{N} borderline cases require individual review before the renewal deadline. [View Borderline Cases →]" |
| Students notified of discontinuation with no acknowledgement > 5 days | Warning | "{N} students discontinued from scholarships have not acknowledged the notification. [View →]" |
| Batch approval completed | Info | "Renewal approved for {N} eligible students. Total value: ₹{X}." |
| Bulk notification dispatch completed | Info | "Renewal decisions sent to {N} students via WhatsApp/Email." |
| Director override recorded | Info | "Director {Name} overrode renewal decision for {Student Name}: {Old Decision} → {New Decision}." |

---

## 4. KPI Summary Bar

Auto-refreshes every 5 minutes via HTMX:

```html
<div id="renewal-kpi-bar"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-renewals/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#renewal-kpi-bar"
     hx-swap="innerHTML">
  <!-- KPI cards rendered here -->
</div>
```

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Renewals Due This Cycle | Total scholarship holders in the current renewal batch | `renewal_record` for current cycle | Blue always | Filters 5.1 to all statuses |
| Approved This Cycle | COUNT where `status = 'approved'` in current cycle | `renewal_record` | Green if > 0; grey if 0 | Filters 5.1 to Approved |
| Under Review (Borderline) | COUNT where `meets_criteria = 'borderline'` and `status = 'pending'` | `renewal_record` | Amber if > 0; green if 0 | Scrolls to Borderline Cases Queue (5.3) |
| Scholarships Discontinued | COUNT where `status = 'discontinued'` in current cycle | `renewal_record` | Amber (informational) | Filters 5.1 to Discontinued |
| Renewal Deadline Approaching | Days until renewal_window_close_date | Scheme config | Red if ≤ 14 days; amber 15–30 days; green > 30 days | — |
| Students Not Yet Notified | COUNT where `status IN ('approved','discontinued')` AND `notified = False` | `renewal_record` | Red if > 0; green if 0 | Scrolls to Notification Status (5.5) |

---

## 5. Sections

### 5.1 Renewal Batch Table

**Display:** Sortable, row-selectable (checkbox), server-side paginated at 20 rows per page. Default sort: Meets Criteria ASC (Borderline first, then No, then Yes — puts items needing attention at the top), then student name ASC.

**Columns:**

| Column | Notes |
|---|---|
| ☐ Checkbox | Row selection for bulk actions |
| Student Name | Full name — click opens renewal-review-drawer |
| Branch | Branch name |
| Stream | Stream badge |
| Scheme | Scholarship scheme name |
| Last Academic Score | Percentage from most recent annual exam result (pulled from results module) |
| Scheme Criteria (Required %) | Threshold percentage defined in the scheme configuration |
| Meets Criteria | Yes (green) / No (red) / Borderline (amber) — computed from Score vs Criteria |
| Current Scholarship Amount | ₹ formatted — annual amount in current cycle |
| Renewal Amount | ₹ formatted — same as current (or adjusted if an amount-adjustment decision has been staged) |
| Status | Pending Review (grey) / Approved (green) / Discontinued (red) / Grace Extended (amber) / On Hold (blue) — badge |
| Actions | `[Review →]` (opens renewal-review-drawer) |

**Filters:**
- Scheme (dropdown — all schemes with active renewal batch)
- Branch (dropdown)
- Criteria Met (Yes / No / Borderline — multi-select)
- Status (multi-select)
- Score range (min % to max %)

**Bulk Actions (Scholarship Manager only, shown when ≥ 1 row selected):**
- `[Approve All Eligible (Meets Criteria)]` — applies only to rows where Meets Criteria = Yes and Status = Pending; opens batch-approve-confirm modal
- `[Discontinue All Ineligible]` — applies only to rows where Meets Criteria = No and Status = Pending; opens discontinue-confirm modal (requires reason)

**Export:** `[Export Renewal List ↓]` — exports current filtered result set as CSV.

**HTMX Pattern:**
```html
<div id="renewal-batch-table-wrapper"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-renewals/batch/"
     hx-trigger="load"
     hx-target="#renewal-batch-table-wrapper"
     hx-swap="innerHTML">
</div>
```
Filter change: `hx-trigger="change"` on filter dropdowns → `hx-target="#renewal-batch-table-body"` `hx-swap="innerHTML"`. Pagination: `hx-target="#renewal-batch-table-wrapper"` `hx-swap="innerHTML"`.

**Empty State:** Checkmark graphic. Heading: "No Renewals Pending." Description: "All renewal decisions for the current cycle have been made." CTA: `[View Renewal History →]`

---

### 5.2 Renewal Summary by Scheme

**Display:** Summary table — one row per scholarship scheme that has an active renewal batch. Provides the Scholarship Manager and Director an at-a-glance financial and operational view of each scheme's renewal status. Not paginated — typically 5–15 schemes.

| Column | Notes |
|---|---|
| Scheme Name | Scheme name — links to Scholarship Registry (Page 22) |
| Type | Merit / Need-based / RTE / Govt-State / etc. — badge |
| Total Due | Students in renewal batch for this scheme |
| Approved | Count with status = Approved |
| Discontinued | Count with status = Discontinued |
| In Review | Count Borderline or On Hold |
| Pending | Count still at Pending Review |
| Total Renewal Value (₹) | SUM of renewal amounts for Approved records in this scheme — formatted ₹X,XX,XXX |

**HTMX Pattern:**
```html
<div id="renewal-scheme-summary"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-renewals/scheme-summary/"
     hx-trigger="load, every 5m"
     hx-target="#renewal-scheme-summary"
     hx-swap="innerHTML">
</div>
```

**Empty State:** "No active renewal batches for the current cycle."

---

### 5.3 Borderline Cases Queue

**Display:** Dedicated sub-table for students whose last academic score is within 3 percentage points of their scheme's renewal threshold (i.e. score between `threshold - 3%` and `threshold + 2.99%`). These students require individual human judgement rather than automated batch processing. Sorted by gap from threshold ASC (closest to the threshold first).

| Column | Notes |
|---|---|
| Student Name | Full name — click opens renewal-review-drawer |
| Branch | Branch name |
| Scheme | Scheme name |
| Last Score (%) | Percentage — colour: red if below threshold; amber if within 0–3% above |
| Threshold (%) | Required % from scheme |
| Gap | `Score − Threshold` — shown as "+1.2%" or "−0.8%" with colour |
| Previous Renewal Count | How many consecutive years this student has been renewed |
| Actions | `[Approve with Note]` · `[Grant Grace Extension]` · `[Discontinue]` |

`[Approve with Note]` — opens renewal-review-drawer pre-positioned on the Decision tab with "Approve" pre-selected and a required note field. `[Grant Grace Extension]` — opens grace-extension-modal. `[Discontinue]` — opens discontinue-confirm modal.

**HTMX Pattern:**
```html
<div id="borderline-cases-queue"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-renewals/borderline/"
     hx-trigger="load"
     hx-target="#borderline-cases-queue"
     hx-swap="innerHTML">
</div>
```

**Empty State:** "No borderline cases in the current renewal batch. All students clearly meet or do not meet their scheme criteria."

---

### 5.4 Criteria Performance Chart

**Display:** Stacked horizontal bar chart (Chart.js 4.x). One bar per scheme. Each bar is divided into three colour-coded segments:
- Green: "Clearly Met" — score ≥ threshold + 3%
- Amber: "Borderline" — score within ±3% of threshold
- Red: "Clearly Failed" — score < threshold − 3%

X-axis: percentage of students (0–100%). Y-axis: scheme names. Hovering on a segment shows absolute count and percentage. Scheme filter (dropdown) allows drilling into individual schemes. The chart reloads via HTMX on filter change.

**HTMX Pattern:**
```html
<div id="criteria-performance-chart"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-renewals/criteria-chart/"
     hx-trigger="load"
     hx-target="#criteria-performance-chart"
     hx-swap="innerHTML">
</div>
```
Scheme filter change: `hx-trigger="change"` → re-renders chart fragment.

**Empty State:** "No performance data available for charting yet."

---

### 5.5 Renewal Notification Status

**Display:** Table listing every student whose renewal decision has been made (status = Approved, Discontinued, or Grace Extended) and tracking whether the decision has been communicated to them. Sorted by: Not Notified first, then by decision date ASC.

| Column | Notes |
|---|---|
| Student Name | Full name |
| Branch | Branch name |
| Scheme | Scheme name |
| Decision | Approved (green) / Discontinued (red) / Grace Extended (amber) — badge |
| Notified Via | WhatsApp (green) / Email (blue) / Both / Not Yet (red) — badge |
| Notification Date | `DD MMM YYYY HH:MM` or "—" |
| Acknowledged | Yes (green) / No (grey) |
| Actions | `[Send Notification]` (if not yet notified) · `[Resend]` (if already notified) |

**Bulk Actions:** `[Send Notifications to All Undecided]` — sends notification to all students with a decision but not yet notified. `[Resend Failures]` — resends to all where notification delivery failed.

**HTMX Pattern:**
```html
<div id="notification-status-table"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-renewals/notifications/"
     hx-trigger="load"
     hx-target="#notification-status-table"
     hx-swap="innerHTML">
</div>
```
`[Send Notification]`: `hx-post="/api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/notify/"` `hx-target="#notification-row-{record_id}"` `hx-swap="outerHTML"`. Bulk send: `hx-post` to bulk-notify endpoint → `hx-target="#notification-status-table"` `hx-swap="innerHTML"`.

**Empty State:** "No decisions made yet. Approve or discontinue renewals to enable notifications."

---

### 5.6 Renewal History

**Display:** Paginated table showing all past renewal decisions across all cycles. Searchable by student name. Default sort: decision date DESC.

| Column | Notes |
|---|---|
| Student Name | Full name |
| Branch | Branch name |
| Scheme | Scheme name |
| Academic Year | e.g. "2024-25" |
| Decision | Approved / Discontinued / Grace Extended / On Hold — badge |
| Amount (₹) | Renewal amount for that year |
| Decided By | Staff name |
| Decision Date | `DD MMM YYYY` |

**Search:** Free-text on student name.
**Filters:** Scheme (dropdown), Academic Year (dropdown), Decision (multi-select)

**HTMX Pattern:**
```html
<div id="renewal-history-table"
     hx-get="/api/v1/group/{group_id}/adm/scholarship-renewals/history/"
     hx-trigger="load"
     hx-target="#renewal-history-table"
     hx-swap="innerHTML">
</div>
```
Search: `hx-trigger="input delay:400ms"` → `hx-target="#renewal-history-body"` `hx-swap="innerHTML"`. Pagination: `hx-target="#renewal-history-table"` `hx-swap="innerHTML"`.

**Empty State:** "No renewal history found for the selected filters."

---

## 6. Drawers & Modals

### 6.1 Renewal Review Drawer
- **Width:** 640px (right-side slide-in)
- **Trigger:** `[Review →]` on any student row, student name click, or action buttons in Borderline Cases Queue
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/detail/`
- **Tabs:**
  1. **Student Profile** — name, class, branch, stream, contact details, parent details
  2. **Academic Performance** — last 2 years of annual exam scores rendered as a line chart (Chart.js 4.x); score trend with the scheme threshold overlaid as a horizontal reference line; subject-wise breakdown for the most recent year
  3. **Scheme Details** — scheme name, type, eligibility criteria, renewal conditions, award history table (year, amount, decision)
  4. **Current Scholarship** — current cycle amount, start date, expiry date, disbursement history (last 2 cycles), any linked fee waivers
  5. **Renewal Decision** — Radio: Approve / Discontinue / Grant Grace Extension / Amount Adjustment / On Hold. Each option shows contextual fields:
     - Approve: Optional note, Renewal amount (pre-filled; editable for adjustment), Notify student (toggle)
     - Discontinue: Reason required (dropdown), Internal note, Notify student (toggle)
     - Grace Extension: Extension period (1 term / 1 year), Condition note, Notify student (toggle)
     - Amount Adjustment: New amount field (with reason required), Notify student (toggle)
     - On Hold: Reason, Review date
  6. **Notification Draft** — Preview of the WhatsApp/email message that will be sent with the decision; editable before sending

Actions at drawer footer: `[Save Decision]` · `[Save and Notify Student]` · `[Cancel]`

---

### 6.2 Batch Approve Confirm Modal
- **Width:** 480px (centred modal)
- **Trigger:** `[Approve All Eligible (Meets Criteria)]` bulk action
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-renewals/batch-approve-form/`
- **Content:**
  - Summary: "Approve renewal for {N} eligible students?"
  - Breakdown table by scheme: Scheme Name | Count | Total Renewal Value (₹)
  - Grand total: "Total renewal commitment: ₹{X,XX,XXX}"
  - Checkbox: "Send renewal notifications to all approved students after confirmation"
  - `[Confirm Approve All →]` · `[Cancel]`

---

### 6.3 Discontinue Confirm Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Discontinue]` action in Borderline Cases Queue, or `[Discontinue All Ineligible]` bulk action
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/discontinue-form/`
- **Fields:**
  - Student name / count (read-only display)
  - Reason (required dropdown): Score Below Threshold / Non-submission of Documents / Student Request / Scheme Criteria Change / Other
  - Internal note (text area)
  - Notify student (Yes / No toggle — defaults to Yes)
  - `[Confirm Discontinue]` · `[Cancel]`

---

### 6.4 Grace Extension Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Grant Grace Extension]` in Borderline Cases Queue or within Renewal Review Drawer
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/grace-form/`
- **Fields:**
  - Student name (read-only display), current score, threshold (read-only)
  - Extend for: 1 Term / 1 Year (radio)
  - Condition: "Student must score ≥ __% in the next {term/annual} exam to retain the scholarship" (editable number field)
  - Note to student (text area — pre-filled with standard grace language; editable)
  - Notify student (Yes / No toggle — defaults to Yes)
  - `[Confirm Grace Extension]` · `[Cancel]`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Individual renewal approved | "Renewal approved for {Student Name} — {Scheme Name}." | Success | 4s |
| Batch approval completed | "Renewal approved for {N} eligible students. Total: ₹{X}." | Success | 5s |
| Renewal discontinued | "Scholarship discontinued for {Student Name} — {Scheme Name}." | Warning | 5s |
| Bulk discontinue completed | "Scholarship discontinued for {N} students." | Warning | 5s |
| Grace extension granted | "Grace extension granted for {Student Name} — valid for {period}." | Info | 5s |
| Amount adjusted | "Renewal amount adjusted to ₹{X} for {Student Name}." | Info | 4s |
| Notification sent (single) | "Renewal decision sent to {Student Name} via {Channel}." | Success | 4s |
| Bulk notifications sent | "Renewal notifications sent to {N} students." | Success | 5s |
| Notification failed | "Notification failed for {Student Name}. Check contact details." | Error | 6s |
| Director override recorded | "Decision overridden by Director for {Student Name}." | Info | 5s |
| Export ready | "CSV export is ready. Download will start shortly." | Success | 4s |
| Decision save failed | "Could not save decision for {Student Name}. Please try again." | Error | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No active renewal batch for current cycle | Calendar graphic | "No Renewal Batch Yet" | "A renewal batch is automatically generated at the start of each renewal window. Check back when the current renewal period opens." | — |
| All renewals decided | Checkmark graphic | "All Decisions Made" | "Every student in the renewal batch has a decision. Proceed to send notifications." | `[Send Notifications →]` |
| No borderline cases | Balance-scale graphic | "No Borderline Cases" | "All students clearly meet or do not meet their scheme's renewal criteria." | — |
| No renewal history | Archive graphic | "No History Available" | "Past renewal decisions will appear here after the first renewal cycle is completed." | — |
| No notifications pending | Envelope-check graphic | "All Students Notified" | "All students with renewal decisions have been notified." | — |
| Counsellor — no assigned students with renewals | Person graphic | "No Renewals for Your Students" | "None of your assigned students have renewals due in the current cycle." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton: KPI bar shimmer + table skeleton (8 rows) + scheme summary shimmer |
| KPI bar auto-refresh | Inline spinner on each KPI card |
| Renewal batch table load | Table body skeleton (8-row shimmer) |
| Filter change | Table body skeleton (5-row shimmer) |
| Table pagination | Table body skeleton |
| Scheme summary auto-refresh | Table skeleton |
| Borderline cases queue load | Sub-table skeleton (4-row shimmer) |
| Criteria performance chart load | Chart container spinner |
| Notification status table load | Table skeleton |
| Single notification send POST | Row-level button spinner |
| Bulk notification POST | Modal progress indicator "Sending notifications…" |
| Renewal history table load | Table skeleton |
| Renewal history search/filter | Table body skeleton |
| Renewal history pagination | Table body skeleton |
| Renewal review drawer open | Drawer skeleton: profile fields shimmer + tab content shimmer |
| Academic performance chart in drawer | Chart container spinner |
| Batch approve confirm modal open | Modal skeleton |
| Grace extension modal open | Modal skeleton |
| Decision save in drawer | Drawer footer button spinner |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| UI Element | Scholarship Manager (27) | Director (23) | CFO | Counsellor (25) | Branch Principal |
|---|---|---|---|---|---|
| `[Approve All Eligible →]` header button | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Send Notifications to All Decided →]` header button | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Export Renewal List ↓]` | Visible | Visible | Hidden | Hidden | Hidden |
| Renewal Batch Table — full columns | Visible | Visible | Financial cols only | Own students only | Own branch only |
| `[Review →]` per-row action | Visible | Visible | Hidden | Visible (view only) | Visible (view only) |
| Bulk approve action bar | Visible | Hidden | Hidden | Hidden | Hidden |
| Bulk discontinue action bar | Visible | Hidden | Hidden | Hidden | Hidden |
| Renewal Summary by Scheme | Visible | Visible | Visible | Hidden | Hidden |
| Borderline Cases Queue | Visible | Visible | Hidden | Hidden | Hidden |
| `[Approve with Note]` in borderline queue | Visible | Visible | Hidden | Hidden | Hidden |
| `[Grant Grace Extension]` in borderline queue | Visible | Visible | Hidden | Hidden | Hidden |
| `[Discontinue]` in borderline queue | Visible | Visible | Hidden | Hidden | Hidden |
| Criteria Performance Chart | Visible | Visible | Hidden | Hidden | Hidden |
| Renewal Notification Status table | Visible | Visible | Hidden | Hidden | Hidden |
| `[Send Notification]` per-row | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Resend]` per-row | Visible | Hidden | Hidden | Hidden | Hidden |
| `[Resend Failures]` bulk action | Visible | Hidden | Hidden | Hidden | Hidden |
| Renewal History table | Visible | Visible | Hidden | Own students | Own branch |
| Renewal Review Drawer — Decision tab | Full decision access | Full decision access (override) | Hidden | Hidden | Hidden |
| Renewal Review Drawer — Notification Draft tab | Visible | Hidden | Hidden | Hidden | Hidden |
| Batch Approve Confirm modal | Visible | Hidden | Hidden | Hidden | Hidden |
| Director Override action (in drawer) | Hidden | Visible | Hidden | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/kpis/` | JWT G3+ | KPI bar data for current cycle |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/batch/` | JWT G3+ | Paginated renewal batch table with filters |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/scheme-summary/` | JWT G3+ | Renewal summary by scheme |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/borderline/` | JWT G3+ | Borderline cases queue |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/criteria-chart/` | JWT G3+ | Criteria performance chart data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/notifications/` | JWT G3+ | Renewal notification status table |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/history/` | JWT G3+ | Renewal history (paginated, filterable) |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/detail/` | JWT G3+ | Renewal review drawer HTML fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/approve/` | JWT G3 | Approve individual renewal |
| POST | `/api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/discontinue/` | JWT G3 | Discontinue individual renewal (reason required) |
| POST | `/api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/grace-extension/` | JWT G3 | Grant grace extension |
| PATCH | `/api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/adjust-amount/` | JWT G3 | Adjust renewal amount (reason required) |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/batch-approve-form/` | JWT G3 | Batch approve confirm modal HTML fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-renewals/batch-approve/` | JWT G3 | Batch approve all eligible (Meets Criteria = Yes, Status = Pending) |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/discontinue-form/` | JWT G3 | Discontinue confirm modal HTML fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-renewals/batch-discontinue/` | JWT G3 | Batch discontinue all ineligible |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/grace-form/` | JWT G3 | Grace extension modal HTML fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/notify/` | JWT G3 | Send notification to single student |
| POST | `/api/v1/group/{group_id}/adm/scholarship-renewals/bulk-notify/` | JWT G3 | Send notifications to all decided-but-unnotified students |
| POST | `/api/v1/group/{group_id}/adm/scholarship-renewals/resend-failed-notifications/` | JWT G3 | Resend failed notifications |
| POST | `/api/v1/group/{group_id}/adm/scholarship-renewals/{record_id}/director-override/` | JWT G3 (Director) | Director overrides any renewal decision |
| GET | `/api/v1/group/{group_id}/adm/scholarship-renewals/export/` | JWT G3+ | Export current filtered batch as CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar initial load and auto-refresh | `load, every 5m` | GET `.../scholarship-renewals/kpis/` | `#renewal-kpi-bar` | `innerHTML` |
| Renewal batch table initial load | `load` | GET `.../scholarship-renewals/batch/` | `#renewal-batch-table-wrapper` | `innerHTML` |
| Filter dropdown change | `change` | GET `.../scholarship-renewals/batch/?{filters}` | `#renewal-batch-table-body` | `innerHTML` |
| Table pagination click | `click` | GET `.../scholarship-renewals/batch/?page={n}&{filters}` | `#renewal-batch-table-wrapper` | `innerHTML` |
| Scheme summary load and auto-refresh | `load, every 5m` | GET `.../scholarship-renewals/scheme-summary/` | `#renewal-scheme-summary` | `innerHTML` |
| Borderline cases queue load | `load` | GET `.../scholarship-renewals/borderline/` | `#borderline-cases-queue` | `innerHTML` |
| Criteria performance chart load | `load` | GET `.../scholarship-renewals/criteria-chart/` | `#criteria-performance-chart` | `innerHTML` |
| Criteria chart scheme filter change | `change` | GET `.../scholarship-renewals/criteria-chart/?scheme={id}` | `#criteria-performance-chart` | `innerHTML` |
| Notification status table load | `load` | GET `.../scholarship-renewals/notifications/` | `#notification-status-table` | `innerHTML` |
| Single `[Send Notification]` click | `click` | POST `.../scholarship-renewals/{record_id}/notify/` | `#notification-row-{record_id}` | `outerHTML` |
| `[Resend Failures]` bulk click | `click` | POST `.../scholarship-renewals/resend-failed-notifications/` | `#notification-status-table` | `innerHTML` |
| Renewal history table load | `load` | GET `.../scholarship-renewals/history/` | `#renewal-history-table` | `innerHTML` |
| Renewal history search (debounced) | `input delay:400ms` | GET `.../scholarship-renewals/history/?search={q}` | `#renewal-history-body` | `innerHTML` |
| Renewal history filter change | `change` | GET `.../scholarship-renewals/history/?{filters}` | `#renewal-history-body` | `innerHTML` |
| Renewal history pagination | `click` | GET `.../scholarship-renewals/history/?page={n}&{filters}` | `#renewal-history-table` | `innerHTML` |
| `[Review →]` / student name click | `click` | GET `.../scholarship-renewals/{record_id}/detail/` | `#renewal-review-drawer` | `innerHTML` |
| Drawer `[Save Decision]` submit | `click` | POST `.../scholarship-renewals/{record_id}/approve/` (or discontinue/grace) | `#renewal-batch-table-body` | `innerHTML` |
| `[Approve All Eligible →]` header click | `click` | GET `.../scholarship-renewals/batch-approve-form/` | `#batch-approve-modal` | `innerHTML` |
| Batch approve modal `[Confirm Approve All →]` | `click` | POST `.../scholarship-renewals/batch-approve/` | `#renewal-batch-table-wrapper` | `innerHTML` |
| `[Discontinue]` in borderline queue | `click` | GET `.../scholarship-renewals/{record_id}/discontinue-form/` | `#discontinue-modal` | `innerHTML` |
| Discontinue modal `[Confirm Discontinue]` | `click` | POST `.../scholarship-renewals/{record_id}/discontinue/` | `#renewal-batch-table-body` | `innerHTML` |
| `[Grant Grace Extension]` in borderline queue | `click` | GET `.../scholarship-renewals/{record_id}/grace-form/` | `#grace-extension-modal` | `innerHTML` |
| Grace modal `[Confirm Grace Extension]` | `click` | POST `.../scholarship-renewals/{record_id}/grace-extension/` | `#renewal-batch-table-body` | `innerHTML` |
| `[Send Notifications to All Decided →]` header | `click` | POST `.../scholarship-renewals/bulk-notify/` | `#notification-status-table` | `innerHTML` |
| Resend individual notification | `click from:.btn-resend-notify` | POST `.../scholarship-renewals/records/{id}/notify/` | `#notify-status-cell-{id}` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
