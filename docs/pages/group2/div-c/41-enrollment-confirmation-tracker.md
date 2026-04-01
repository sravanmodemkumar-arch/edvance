# 41 — Enrollment Confirmation Tracker

> **URL:** `/group/adm/enrollment-confirmation/`
> **File:** `41-enrollment-confirmation-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Admission Coordinator (Role 24) — primary

---

## 1. Purpose

After offer letters are sent and acknowledged (managed in Page 14 — Offer Letter Manager), students must take the definitive step of confirming their seat: paying the initial registration or seat-booking fee and submitting the required documentation package. The Enrollment Confirmation Tracker is the operational page that bridges "offer sent" and "student enrolled." Without this page, the admissions pipeline lacks visibility into who has actually confirmed versus who is still deciding — making it impossible to manage waitlist promotion timing accurately. Every confirmed seat translates directly into a class formation unit for the Academic Division and a projected fee record for the Finance Division; every unconfirmed seat that reaches its deadline silently blocks a waitlist candidate from taking that seat in time.

The Tracker consolidates every student with an active or recently expired offer letter into a single, status-segmented view. The four primary statuses — Confirmed & Paid, Documents Pending, Not Yet Responded, and Withdrawn — are surfaced both as KPI counts and as filterable rows in the main Confirmation Status Table (Section 5.1). The Coordinator uses this page daily during the peak admission window: scanning the Deadline Expiry Alert Strip (Section 5.3) each morning to dispatch urgent reminders to students expiring within 72 hours, reviewing the Document Checklist Status (Section 5.5) to follow up on incomplete document submissions, and acting on the Withdrawn Seats panel (Section 5.6) to trigger waitlist promotions the moment a seat is freed.

For the Group Admissions Director, this page is the authoritative enrollment count for the current cycle — not "offers sent" but actual confirmed enrollments with the initial fee paid. This number drives Academic class formation planning and the Finance team's fee revenue projections. The Coordinator Front-loads all follow-up activity through this single page, reducing the need to cross-reference the fee system or the document management module separately.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admission Coordinator (Role 24) | G3 | Full access — view all, send reminders, cancel offers, extend deadlines, trigger waitlist promotions, export | Primary operator |
| Group Admissions Director (Role 23) | G3 | View all + cancel offers + override deadline extensions | Cannot send individual reminders; can cancel offers and override |
| Group Admission Counsellor (Role 25) | G3 | View own assigned students only — no action buttons except [View →] | Read-only, scoped to their student list |
| CFO / Finance | G3+ | View — fee payment column and confirmed count only | Read-only, finance context; no student detail drawer |

> **Enforcement:** `@role_required(['coordinator', 'admissions_director', 'counsellor', 'cfo'])` at the Django view level. Counsellor queryset is filtered: `ConfirmationRecord.objects.filter(student__assigned_counsellor=request.user)`. Cancel-offer and override endpoints require `request.user.role == 'admissions_director'`. CFO receives a read-only template variant (`confirmation_readonly=True` in context) with fee columns only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal › Admissions › Enrollment Confirmation Tracker
```

### 3.2 Page Header
- **Title:** Enrollment Confirmation Tracker
- **Subtitle:** Seat confirmation status for all offer holders — `{current_cycle_name}`
- **Right-side controls:**
  - `[Send Reminder to All Pending]` (Coordinator only)
  - `[Cancel Expired Offers → Promote Waitlist]` (Coordinator only)
  - `[Export CSV ↓]`
  - `[Refresh ↺]`

### 3.3 Alert Banner

Collapsible panel, positioned above the KPI row. `bg-red-50 border-l-4 border-red-500` for Critical; `bg-yellow-50 border-l-4 border-yellow-400` for Warning; `bg-blue-50 border-l-4 border-blue-400` for Info.

| Trigger | Severity | Message |
|---|---|---|
| Students with confirmation deadline expiring in < 3 days > 0 | Critical | "{N} students have confirmation deadlines expiring within 3 days. [View Expiring →]" |
| Unconfirmed students with no contact for > 7 days > 0 | Warning | "{N} students have not responded for more than 7 days. [View Uncontacted →]" |
| Withdrawn offers with waitlist candidates available | Info | "{N} seats freed from withdrawals have eligible waitlist candidates ready. [Promote Now →]" |
| Documents incomplete for confirmed (fee-paid) students > 0 | Warning | "{N} confirmed students still have incomplete document submissions. [View →]" |
| Bulk reminder dispatch completed | Info | "Reminder sent to {N} pending students successfully." |
| Confirmation deadline batch-expired (nightly job) | Warning | "{N} offers auto-expired overnight. Seats are available for waitlist promotion." |

---

## 4. KPI Summary Bar

Auto-refreshes every 5 minutes via HTMX:

```html
<div id="enrollment-kpi-bar"
     hx-get="/api/v1/group/{group_id}/adm/enrollment-confirmation/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#enrollment-kpi-bar"
     hx-swap="innerHTML">
  <!-- KPI cards rendered here -->
</div>
```

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Offers Sent (Current Cycle) | COUNT of offer letters in current cycle | `offer_letter` table, current cycle | Blue always | Filters table to all statuses |
| Confirmed & Fee Paid | COUNT where `fee_paid=True AND status='confirmed'` | `confirmation_record` | Green if > 0; grey if 0 | Filters table to Confirmed |
| Documents Submitted (%) | `(docs_complete_count / confirmed_count) * 100` | Aggregated | Green ≥ 80%; Amber 60–79%; Red < 60% | Filters table to Documents Pending |
| Deadline Expiring Soon | COUNT where `confirmation_deadline - today < 3 days AND status != 'confirmed'` | Computed | Red if > 0; green if 0 | Scrolls to Deadline Expiry Alert Strip (5.3) |
| Withdrawn / Cancelled | COUNT where `status IN ('withdrawn', 'cancelled')` current cycle | `confirmation_record` | Amber if > 0; grey if 0 | Filters table to Withdrawn |
| Unconfirmed > 7 Days | COUNT where `offer_sent_date < today - 7 AND status NOT IN ('confirmed', 'withdrawn')` | Computed | Red if > 0; green if 0 | Filters table to Not Yet Responded |

---

## 5. Sections

### 5.1 Confirmation Status Table

**Display:** Sortable, row-selectable (checkbox), server-side paginated at 20 rows per page. Default sort: confirmation deadline ASC (most urgent first). Status badges use colour coding: Confirmed (green), Documents Pending (amber), Expiring Soon (red), Withdrawn (grey), Expired (dark red).

**Columns:**

| Column | Notes |
|---|---|
| ☐ Checkbox | Row selection for bulk actions |
| Student Name | Full name — click opens confirmation-detail drawer |
| Branch | Allocated branch name |
| Stream | Allocated stream (MPC / BiPC / MEC / CEC / etc.) |
| Student Type | Day Scholar / Hosteler AC / Hosteler Non-AC — badge |
| Offer Date | `DD MMM YYYY` |
| Confirmation Deadline | `DD MMM YYYY` — red text if < 3 days away |
| Fee Paid | Yes (green) / Partial (amber) / No (red) — badge |
| Documents Submitted | Yes (green) / Partial (amber) / No (red) — badge |
| Status | Confirmed / Documents Pending / Not Yet Responded / Expiring Soon / Withdrawn / Expired — colour badge |
| Actions | `[View →]` · `[Send Reminder]` (Coordinator only) · `[Cancel Offer]` (Director only) |

**Search:** Free-text search on student name and phone number; `hx-trigger="input delay:400ms"`.

**Filters:**
- Status (multi-select: Confirmed / Documents Pending / Not Yet Responded / Expiring Soon / Withdrawn / Expired)
- Branch (dropdown)
- Stream (dropdown)
- Student Type (Day Scholar / Hosteler AC / Hosteler Non-AC)
- Confirmation Deadline range (date picker — from/to)
- Fee Status (Paid / Partial / Not Paid)
- Documents Status (Submitted / Partial / Not Submitted)

**Bulk Actions (Coordinator only, shown when ≥ 1 row selected):**
- `[Send Reminder to All Pending]` — opens bulk-reminder-confirm modal
- `[Cancel Expired Offers → Promote from Waitlist]` — opens cancel-offer-confirm modal for selected rows

**Export:** `[Export CSV ↓]` — exports current filtered result set.

**HTMX Pattern:**
```html
<div id="confirmation-table-wrapper"
     hx-get="/api/v1/group/{group_id}/adm/enrollment-confirmation/?{filters}"
     hx-trigger="load"
     hx-target="#confirmation-table-wrapper"
     hx-swap="innerHTML">
</div>
```
Filter/search changes: `hx-trigger="change"` (dropdowns) or `hx-trigger="input delay:400ms"` (search) → same endpoint with updated query params → `hx-target="#confirmation-table-body"` `hx-swap="innerHTML"`. Pagination: `hx-get="...?page={n}&{filters}"` `hx-target="#confirmation-table-wrapper"` `hx-swap="innerHTML"`.

**Empty State:** Inbox-zero graphic. Heading: "No Students Match These Filters." Description: "Try adjusting your filters or search term to find confirmation records." CTA: `[Clear Filters]`

---

### 5.2 Confirmation Funnel

**Display:** Horizontal funnel chart (Chart.js 4.x) showing the progression through the confirmation pipeline. Four stages shown with absolute counts and percentage of the preceding stage:

```
Offered  →  Fee Paid  →  Documents Submitted  →  Seat Confirmed
  [N]   →    [N]     →        [N]             →       [N]
  100%       XX%              XX%                     XX%
```

Branch filter (dropdown) allows the Director to compare funnel conversion rates across branches. Chart updates via HTMX on filter change.

**Filters:** Branch (dropdown — defaults to All Branches)

**HTMX Pattern:**
```html
<div id="confirmation-funnel-chart"
     hx-get="/api/v1/group/{group_id}/adm/enrollment-confirmation/funnel/?branch={branch_id}"
     hx-trigger="load"
     hx-target="#confirmation-funnel-chart"
     hx-swap="innerHTML">
</div>
```
Branch filter change: `hx-trigger="change"` on branch dropdown → re-renders the chart fragment.

**Empty State:** "No funnel data available for the selected branch yet."

---

### 5.3 Deadline Expiry Alert Strip

**Display:** Fixed highlighted panel rendered at the top of the page body (below KPI bar, above the main table). Background: `bg-red-50 border border-red-300 rounded-md`. Lists students whose confirmation deadline falls within the next 3 days and who have not yet confirmed. Sorted by deadline ascending (most urgent first). Lazy-loads on page open and auto-refreshes every 5 minutes.

| Column | Notes |
|---|---|
| Student Name | Full name — links to confirmation-detail drawer |
| Branch | Branch name |
| Stream | Stream badge |
| Confirmation Deadline | `DD MMM YYYY` — days remaining shown in red (e.g. "2 days left") |
| Fee Status | Paid / Partial / Not Paid badge |
| Actions | `[Send Urgent Reminder]` · `[Extend Deadline]` · `[View →]` |

**HTMX Pattern:**
```html
<div id="expiry-alert-strip"
     hx-get="/api/v1/group/{group_id}/adm/enrollment-confirmation/expiring-soon/"
     hx-trigger="load, every 5m"
     hx-target="#expiry-alert-strip"
     hx-swap="innerHTML">
</div>
```

**Empty State:** Green banner. "No confirmation deadlines expiring in the next 3 days." (panel collapses to a thin success bar when empty)

---

### 5.4 Branch Confirmation Summary

**Display:** Summary table — one row per branch. Branch rows are expandable (click to show stream-level breakdown as nested rows). Default sort: Confirmation Rate % ASC (lowest-performing branches first).

| Column | Notes |
|---|---|
| Branch | Branch name — click to expand stream breakdown |
| Offers Sent | Total offer letters sent in current cycle |
| Confirmed | Count of fully confirmed (fee paid) students |
| Documents Pending | Confirmed but documents incomplete |
| Not Yet Responded | No response, deadline not yet reached |
| Withdrawn | Offers withdrawn or cancelled |
| Confirmation Rate % | `(Confirmed / Offers Sent) * 100` — colour: Green ≥ 70%; Amber 50–69%; Red < 50% |

**Expanded Row (stream-level):** Branch, Stream, Offers Sent, Confirmed, Pending, Withdrawn, Rate %.

**HTMX Pattern:**
```html
<div id="branch-summary-table"
     hx-get="/api/v1/group/{group_id}/adm/enrollment-confirmation/branch-summary/"
     hx-trigger="load"
     hx-target="#branch-summary-table"
     hx-swap="innerHTML">
</div>
```
Row expand: `hx-get="/api/v1/group/{group_id}/adm/enrollment-confirmation/branch-summary/{branch_id}/streams/"` `hx-target="#branch-stream-rows-{branch_id}"` `hx-swap="innerHTML"` `hx-trigger="click"`.

**Empty State:** "No branch confirmation data available for the current cycle."

---

### 5.5 Document Checklist Status

**Display:** Filterable table showing the document submission status per student. Each row expands to show which individual documents have been submitted (green tick) versus are still pending (red cross). Required documents: Transfer Certificate (TC) / Birth Certificate / Mark Sheet (last exam) / Passport Photos / Medical Certificate / Hostel Agreement (only for Hostelers). Default filter: Documents Incomplete only.

| Column | Notes |
|---|---|
| Student Name | Full name |
| Branch | Branch name |
| Stream | Stream badge |
| Student Type | Day Scholar / Hosteler badge |
| TC | ✓ / ✗ |
| Birth Certificate | ✓ / ✗ |
| Mark Sheet | ✓ / ✗ |
| Photos | ✓ / ✗ |
| Medical Certificate | ✓ / ✗ |
| Hostel Agreement | ✓ / ✗ / N/A (for Day Scholars) |
| Overall | Complete (green) / Partial (amber) / None (red) |
| Actions | `[View / Upload →]` — opens confirmation-detail drawer on Documents tab |

**Filters:** Completeness (All / Complete / Partial / None), Branch, Stream, Student Type

**HTMX Pattern:**
```html
<div id="document-checklist-table"
     hx-get="/api/v1/group/{group_id}/adm/enrollment-confirmation/documents/?status=incomplete"
     hx-trigger="load"
     hx-target="#document-checklist-table"
     hx-swap="innerHTML">
</div>
```
Filter change: `hx-trigger="change"` on filter dropdowns → `hx-target="#document-checklist-body"` `hx-swap="innerHTML"`.

**Empty State:** Green checkmark. "All confirmed students have submitted the required documents."

---

### 5.6 Withdrawn Seats → Waitlist Action

**Display:** Alert list panel. Every offer that has been withdrawn or cancelled (status = 'withdrawn' or 'cancelled') within the current cycle is listed, paired with the top-ranked matching waitlist candidate for that branch/stream/student-type slot. One row per freed seat.

| Column | Notes |
|---|---|
| Freed Seat (Branch + Stream + Type) | e.g. "Hyderabad HQ — MPC — Day Scholar" |
| Withdrawn Student | Name + withdrawal reason badge |
| Withdrawal Date | `DD MMM YYYY` |
| Top Waitlist Candidate | Name + waitlist rank + contact number |
| Waitlist Position | Rank number in the branch/stream waitlist |
| Actions | `[Promote Waitlisted Student →]` — one-click; triggers offer letter flow for the waitlist candidate |

`[Promote Waitlisted Student →]` opens a confirmation dialog: "Promote {Candidate Name} (Rank #{N}) to fill the seat at {Branch} — {Stream}? This will trigger an offer letter." → `[Confirm Promote]` → HTMX POST.

**HTMX Pattern:**
```html
<div id="withdrawn-seats-panel"
     hx-get="/api/v1/group/{group_id}/adm/enrollment-confirmation/withdrawn-seats/"
     hx-trigger="load, every 5m"
     hx-target="#withdrawn-seats-panel"
     hx-swap="innerHTML">
</div>
```
Promote action: `hx-post="/api/v1/group/{group_id}/adm/enrollment-confirmation/promote-waitlist/"` `hx-target="#withdrawn-seats-panel"` `hx-swap="innerHTML"` `hx-confirm="Promote {name} to fill this seat?"`.

**Empty State:** "No withdrawn seats with available waitlist candidates. All freed seats have already been actioned or no waitlist exists for the relevant slots."

---

## 6. Drawers & Modals

### 6.1 Confirmation Detail Drawer
- **Width:** 640px (right-side slide-in)
- **Trigger:** `[View →]` on any student row, or student name click anywhere on the page
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/detail/`
- **Tabs:**
  1. **Student Profile** — name, class, contact, parent contact, address
  2. **Offer Details** — offer letter reference, offer date, offer type (Conditional/Unconditional), deadline, branch, stream, student type, scholarship attached (if any)
  3. **Fee Payment** — initial fee amount due, amount paid, payment date, payment method, payment reference, partial payment detail (if applicable)
  4. **Documents Checklist** — per-document status with upload button for each pending document; uploaded files show filename + date + `[View]` link
  5. **Timeline** — chronological activity log: Offer Sent → Viewed → Reminder Sent → Fee Paid → Document Uploaded → Deadline Extended → etc.
  6. **Actions** — `[Extend Deadline]` (Coordinator) · `[Mark as Confirmed]` (Coordinator — manual override if fee recorded outside system) · `[Cancel Offer]` (Director only) · `[Send Reminder]` (Coordinator)

---

### 6.2 Send Reminder Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Send Reminder]` or `[Send Urgent Reminder]` on any student row
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/reminder-form/`
- **Fields:** Student name (read-only display), Channel (WhatsApp / SMS / Both — radio), Message preview (auto-generated template, editable), `[Send]` · `[Cancel]`

---

### 6.3 Cancel Offer Confirm Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Cancel Offer]` action (Director only)
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/cancel-form/`
- **Fields:** Student name (read-only display), Reason (required dropdown: No Response / Fee Non-payment / Student Withdrew / Seat Needed for Priority Candidate / Other), Internal note (text area), Checkbox: "Trigger automatic waitlist promotion for this seat"
- **Warning text:** "This will permanently cancel the offer and free the seat. This action cannot be undone without Director override."
- **Actions:** `[Confirm Cancel]` · `[Back]`

---

### 6.4 Bulk Reminder Confirm Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Send Reminder to All Pending]` header button or bulk action
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/enrollment-confirmation/bulk-reminder-form/`
- **Fields:** Count display "Send reminder to {N} pending students?", Preview of first 5 student names (truncated list with "…and {N-5} more"), Channel (WhatsApp / SMS / Both), `[Confirm Send]` · `[Cancel]`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reminder sent (single) | "Reminder sent to {Student Name} via {Channel}." | Success | 4s |
| Bulk reminder sent | "Reminders sent to {N} pending students via {Channel}." | Success | 5s |
| Offer cancelled | "Offer cancelled for {Student Name}. Seat freed for waitlist." | Warning | 5s |
| Waitlist promotion triggered | "{Candidate Name} promoted from waitlist. Offer letter being generated." | Success | 5s |
| Deadline extended | "Confirmation deadline extended to {date} for {Student Name}." | Info | 4s |
| Manual confirmation override | "{Student Name} marked as Confirmed by {Coordinator Name}." | Info | 5s |
| Document uploaded | "Document uploaded for {Student Name}: {Document Type}." | Success | 4s |
| Offer cancellation failed | "Could not cancel offer for {Student Name} — please try again." | Error | 6s |
| Export ready | "CSV export is ready. Download will start shortly." | Success | 4s |
| Reminder send failed | "Reminder failed for {Student Name}. Check contact details." | Error | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No offer letters in current cycle | Empty funnel graphic | "No Offers Sent Yet" | "Offer letters for the current cycle will appear here once sent from the Offer Letter Manager." | `[Go to Offer Letter Manager →]` |
| All students confirmed | Celebration graphic | "Everyone is Confirmed!" | "All students who received offers have confirmed their seats." | — |
| No expiring deadlines | Green timer | "No Urgent Deadlines" | "No confirmation deadlines are expiring in the next 3 days." | — |
| No withdrawn seats | Empty seat graphic | "No Freed Seats" | "No offers have been withdrawn or cancelled in this cycle." | — |
| Counsellor — no assigned students | Person graphic | "No Students Assigned" | "Students assigned to you will appear here once they receive offer letters." | — |
| Documents all complete | Checklist graphic | "All Documents Submitted" | "All confirmed students have completed their document submissions." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton: KPI bar shimmer + table skeleton (8 rows) + alert strip shimmer |
| KPI bar auto-refresh | Inline spinner on each KPI card |
| Confirmation table load | Table body skeleton (8-row shimmer) |
| Filter or search change | Table body skeleton (5-row shimmer) |
| Table pagination | Table body skeleton |
| Deadline expiry strip refresh | Strip skeleton (3-row shimmer) |
| Branch summary table load | Table skeleton |
| Branch row expand (stream breakdown) | Inline row-level spinner |
| Document checklist table load | Table skeleton |
| Withdrawn seats panel refresh | Panel skeleton (3-row shimmer) |
| Confirmation detail drawer open | Drawer skeleton: profile fields shimmer + tab content shimmer |
| Send reminder modal open | Modal skeleton |
| Promote waitlist POST | Button spinner + panel refresh spinner |
| Bulk reminder POST | Full modal progress indicator "Sending reminders…" |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| UI Element | Director (23) | Coordinator (24) | Counsellor (25) | CFO |
|---|---|---|---|---|
| `[Send Reminder to All Pending]` header button | Hidden | Visible | Hidden | Hidden |
| `[Cancel Expired Offers]` header button | Hidden | Visible | Hidden | Hidden |
| `[Export CSV ↓]` | Visible | Visible | Hidden | Hidden |
| Confirmation Status Table — all rows | Visible | Visible | Own students only | Visible (fee columns only) |
| `[Send Reminder]` per-row action | Hidden | Visible | Hidden | Hidden |
| `[Cancel Offer]` per-row action | Visible | Hidden | Hidden | Hidden |
| `[View →]` per-row action | Visible | Visible | Visible | Hidden |
| Deadline Expiry Alert Strip | Visible | Visible | Hidden | Hidden |
| `[Send Urgent Reminder]` in strip | Hidden | Visible | Hidden | Hidden |
| `[Extend Deadline]` in strip | Hidden | Visible | Hidden | Hidden |
| Branch Confirmation Summary | Visible | Visible | Hidden | Hidden |
| Document Checklist Status | Visible | Visible | Hidden | Hidden |
| `[View / Upload →]` in document checklist | Visible | Visible | Hidden | Hidden |
| Withdrawn Seats → Waitlist Action panel | Visible | Visible | Hidden | Hidden |
| `[Promote Waitlisted Student →]` | Hidden | Visible | Hidden | Hidden |
| Confirmation Detail Drawer — Actions tab | `[Cancel Offer]` only | `[Extend Deadline]`, `[Mark Confirmed]`, `[Send Reminder]` | Hidden | Hidden |
| Bulk Reminder Confirm modal | Hidden | Visible | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/kpis/` | JWT G3+ | KPI bar data (counts per status, % docs submitted) |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/` | JWT G3+ | Paginated confirmation status table with filters |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/expiring-soon/` | JWT G3+ | Students with deadline < 3 days and not confirmed |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/funnel/` | JWT G3+ | Funnel chart data (offered → paid → docs → confirmed) |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/branch-summary/` | JWT G3+ | Branch-level confirmation summary table data |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/branch-summary/{branch_id}/streams/` | JWT G3+ | Stream-level breakdown for a specific branch (row expand) |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/documents/` | JWT G3+ | Document checklist status table with filters |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/withdrawn-seats/` | JWT G3+ | Freed seats paired with top waitlist candidates |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/detail/` | JWT G3+ | Full confirmation detail drawer content (HTML fragment) |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/reminder-form/` | JWT G3 | Reminder form fragment for send-reminder modal |
| POST | `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/send-reminder/` | JWT G3 | Send WhatsApp/SMS reminder to single student |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/cancel-form/` | JWT G3 (Director) | Cancel offer form fragment |
| DELETE | `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/cancel-offer/` | JWT G3 (Director) | Cancel offer, free seat, optionally trigger waitlist |
| PATCH | `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/extend-deadline/` | JWT G3 | Extend confirmation deadline |
| PATCH | `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/mark-confirmed/` | JWT G3 | Manual confirmation override |
| POST | `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/upload-document/` | JWT G3 | Upload a document for a specific student |
| POST | `/api/v1/group/{group_id}/adm/enrollment-confirmation/promote-waitlist/` | JWT G3 | Promote top waitlist candidate to a freed seat |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/bulk-reminder-form/` | JWT G3 | Bulk reminder confirm modal form fragment |
| POST | `/api/v1/group/{group_id}/adm/enrollment-confirmation/bulk-reminder/` | JWT G3 | Send reminders to all selected/pending students |
| GET | `/api/v1/group/{group_id}/adm/enrollment-confirmation/export/` | JWT G3+ | Export current filtered result set as CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar initial load and auto-refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/kpis/` | `#enrollment-kpi-bar` | `innerHTML` |
| Confirmation table initial load | `load` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/` | `#confirmation-table-wrapper` | `innerHTML` |
| Filter dropdown change | `change` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/?{filters}` | `#confirmation-table-body` | `innerHTML` |
| Search input (debounced) | `input delay:400ms` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/?search={q}` | `#confirmation-table-body` | `innerHTML` |
| Table pagination click | `click` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/?page={n}&{filters}` | `#confirmation-table-wrapper` | `innerHTML` |
| Deadline expiry strip load and refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/expiring-soon/` | `#expiry-alert-strip` | `innerHTML` |
| Funnel chart load | `load` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/funnel/` | `#confirmation-funnel-chart` | `innerHTML` |
| Funnel branch filter change | `change` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/funnel/?branch={id}` | `#confirmation-funnel-chart` | `innerHTML` |
| Branch summary table load | `load` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/branch-summary/` | `#branch-summary-table` | `innerHTML` |
| Branch row expand (stream breakdown) | `click` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/branch-summary/{branch_id}/streams/` | `#branch-stream-rows-{branch_id}` | `innerHTML` |
| Document checklist table load | `load` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/documents/?status=incomplete` | `#document-checklist-table` | `innerHTML` |
| Document checklist filter change | `change` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/documents/?{filters}` | `#document-checklist-body` | `innerHTML` |
| Withdrawn seats panel load and refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/withdrawn-seats/` | `#withdrawn-seats-panel` | `innerHTML` |
| `[View →]` student row click | `click` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/detail/` | `#confirmation-detail-drawer` | `innerHTML` |
| `[Send Reminder]` click | `click` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/reminder-form/` | `#send-reminder-modal` | `innerHTML` |
| Reminder modal `[Send]` submit | `click` | POST `/api/v1/group/{group_id}/adm/enrollment-confirmation/{student_id}/send-reminder/` | `#send-reminder-modal` | `innerHTML` |
| `[Promote Waitlisted Student →]` click | `click` | POST `/api/v1/group/{group_id}/adm/enrollment-confirmation/promote-waitlist/` | `#withdrawn-seats-panel` | `innerHTML` |
| Bulk reminder `[Send Reminder to All Pending]` | `click` | GET `/api/v1/group/{group_id}/adm/enrollment-confirmation/bulk-reminder-form/` | `#bulk-reminder-modal` | `innerHTML` |
| Bulk reminder modal `[Confirm Send]` | `click` | POST `/api/v1/group/{group_id}/adm/enrollment-confirmation/bulk-reminder/` | `#bulk-reminder-modal` | `innerHTML` |
| Extend deadline from alert strip | `click from:.btn-extend-deadline-strip` | PATCH `.../enrollment-confirmation/{id}/extend-deadline/` | `#deadline-expiry-strip` | `innerHTML` |
| Confirm cancel offer (modal submit) | `click from:#btn-confirm-cancel-offer` | DELETE `.../enrollment-confirmation/{id}/cancel-offer/` | `#confirmation-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
