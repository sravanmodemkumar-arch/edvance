# Page 14 — Offer Letter Manager

- **URL:** `/group/adm/offer-letters/`
- **Template:** `portal_base.html`
- **Theme:** Light

---

## 1. Purpose

The Offer Letter Manager is responsible for generating, personalising, tracking, and dispatching admission offer letters to every allocated student. An offer letter is not merely a formality — it is the legal instrument through which the institution extends a conditional or unconditional offer of admission, specifies the fee payable, states the joining date, and sets the deadline for document submission. It must carry the branch's official letterhead, be addressed correctly to the student and their guardian, and accurately reflect the terms of their specific allocation (stream, hostel type, scholarship conditions if any).

For large groups operating across multiple branches, offer letter generation must be bulk-capable. The Coordinator cannot hand-craft individual letters for hundreds of students during peak admission season. This page provides batch generation tools: the Bulk Dispatch Panel (Section 5.5) allows the Coordinator to select all allocated students within a date range or branch, preview the count, and generate and send all letters in a single action. Individual letters can always be previewed before sending and can be edited for special circumstances using the template editor.

Tracking whether a letter has been sent, acknowledged, and acted upon is as important as generating it. The Sent Letters Tracker (Section 5.2) provides a live view of letter status — allowing the Coordinator to see at a glance which students have acknowledged receipt, which have paid the initial fee, and which have gone silent. Letters that receive no response within 7 days are automatically surfaced in the Expired Letters Alert (Section 5.3), with action buttons to send a reminder, extend the deadline, or cancel the offer and free up the seat for the waitlist. This tight loop between offer issuance and waitlist management maximises seat fill rates.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | View all letters + cancel offers | Cannot generate or edit templates; can cancel offers and trigger waitlist |
| Group Admission Coordinator (Role 24) | G3 | Full access — generate, edit, send, track, extend, cancel | Primary operator of this page |
| Group Admission Counsellor (Role 25) | G3 | View own students' letters only | Cannot generate, send, or cancel |
| CEO / Executive | G3+ | View only | Summary and status tracking |

> **Enforcement:** Letter generation, template editing, and bulk dispatch endpoints enforce `request.user.role in ['coordinator']` at the Django view layer. The Director's cancel-offer endpoint requires `request.user.role == 'admissions_director'`. Counsellor queryset is filtered: `OfferLetter.objects.filter(student__assigned_counsellor=request.user)`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Offer Letter Manager
```

### 3.2 Page Header
- **Title:** Offer Letter Manager
- **Subtitle:** Generate, send, and track admission offer letters — `{current_cycle_name}`
- **Right-side actions:** `[+ Generate Letters →]` (Coordinator) · `[Bulk Dispatch →]` (Coordinator) · `[Refresh ↺]`

### 3.3 Alert Banner

| Trigger | Message |
|---|---|
| Offer letters pending generation > 0 | "{N} allocated students are waiting for offer letters to be generated." |
| Expired letters (no response in 7 days) > 0 | "{N} offer letter(s) have expired with no response. Seats may need to be freed." |
| Letters sent but fee not paid > 10 days | "{N} students accepted offers but have not paid the initial fee within 10 days." |
| Template missing for a branch | "Offer letter template is missing for {Branch}. Letters cannot be generated until a template is configured." |
| Bulk dispatch completed | "{N} offer letters generated and sent successfully." |

---

## 4. KPI Summary Bar

> Auto-refreshes every 5 minutes via HTMX: `hx-get="/api/v1/group/{group_id}/adm/offer-letters/kpis/" hx-trigger="every 5m" hx-target="#offer-letter-kpi-bar" hx-swap="innerHTML"`

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Letters Pending Generation | Allocated students without an offer letter record | Computed | Amber if > 0; green if 0 | Filters to offer letter queue (5.1) |
| Generated Today | Offer letters created today | `created_at__date=today` | Green if > 0 | Filters sent letters tracker to today |
| Letters Sent | Letters with `sent_at IS NOT NULL` (WhatsApp + email combined) | Model count | Neutral (blue) | Filters tracker to sent |
| Acknowledged / Accepted | Letters with `acknowledged=True` | Model count | Green | Filters tracker to acknowledged |
| Expired (no response ≥ 7 days) | Letters with `sent_at <= today − 7 days` and `acknowledged=False` | Computed | Red if > 0; green if 0 | Opens expired letters alert (5.3) |
| Fee Paid After Acceptance | Accepted letters where initial fee payment is confirmed | `fee_paid=True` | Green | Filters tracker to fee paid |

---

## 5. Sections

### 5.1 Offer Letter Queue

**Display:** Table of allocated students for whom offer letters have not yet been generated. Sortable. 20 rows per page, server-side pagination.

**Columns:**

| Column | Notes |
|---|---|
| ☐ Checkbox | Select for bulk generation/send |
| Student Name | Name |
| Branch | Allocated branch |
| Stream | Allocated stream |
| Allocation Date | `DD MMM YYYY` |
| Letter Type | Conditional / Unconditional badge |
| Actions | `[Preview]` (if template exists) · `[Generate]` · `[Send]` (enabled after generation) |

**Bulk Actions (Coordinator):** `[Generate All Selected]` · `[Send All Selected via WhatsApp]`

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/offer-letters/queue/"` `hx-trigger="load"` `hx-target="#offer-queue-table-body"` `hx-swap="innerHTML"`. Pagination: `hx-target="#offer-queue-table-wrapper"`. `[Preview]` click: `hx-get="/api/v1/group/{group_id}/adm/offer-letters/{student_id}/preview/"` `hx-target="#offer-letter-preview-drawer"` `hx-swap="innerHTML"`. `[Generate]`: `hx-post` with student ID. `[Send]`: `hx-post` to send endpoint.

**Empty State:** Green checkmark graphic. Heading: "No Letters Pending." Description: "All allocated students have offer letters generated." CTA: —

---

### 5.2 Sent Letters Tracker

**Display:** Sortable, filterable table of all letters that have been generated and sent. 20 rows per page.

| Column | Notes |
|---|---|
| Student Name | Name |
| Branch | Branch name |
| Sent Via | WhatsApp / Email / Both — badge |
| Sent On | `DD MMM YYYY HH:MM` |
| Acknowledged | Yes (green) / No (grey) / Expired (red) |
| Fee Paid | Yes (green) / No (grey) / Partial (amber) |
| Actions | `[Resend]` (if not acknowledged) · `[View Letter →]` |

**Filters:** Status (Acknowledged/Not Acknowledged/Expired), Branch, Date sent, Fee paid status

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/offer-letters/sent/?{filters}"` `hx-target="#sent-tracker-table-body"` `hx-swap="innerHTML"` `hx-trigger="change"` on filter inputs. Pagination: `hx-target="#sent-tracker-wrapper"`.

**Empty State:** "No offer letters have been sent yet for the current cycle."

---

### 5.3 Expired Letters Alert

**Display:** Highlighted alert panel (red background). Lists letters with no acknowledgement for 7 or more days. Each row has three action options.

| Column | Notes |
|---|---|
| Student Name | Name |
| Branch | Branch name |
| Sent On | Date sent |
| Days Since Sent | Integer; always ≥ 7 in this panel |
| Actions | `[Send Reminder]` · `[Extend Deadline]` · `[Cancel Offer]` |

`[Send Reminder]` — resends the letter with a final reminder note.
`[Extend Deadline]` — opens expiry-action-modal to set new deadline (Coordinator only).
`[Cancel Offer]` — opens confirmation dialog; on confirm, voids the offer and triggers waitlist seat promotion (Director approval required if cancellation affects >5 seats at once).

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/offer-letters/expired/"` `hx-trigger="load, every 5m"` `hx-target="#expired-letters-panel"` `hx-swap="innerHTML"`

**Empty State:** "No expired letters. All offers have been acknowledged or are still within the response window."

---

### 5.4 Letter Template Manager

**Display:** Card grid — one card per branch (and per stream if templates are stream-specific). Each card shows: Branch name, Stream (if stream-specific), template name, last updated date, status (Active / Draft / Missing).

| Card Action | Description |
|---|---|
| `[Preview]` | Opens rendered preview of template with sample data |
| `[Edit Template]` | Opens template-editor drawer |
| `[Set as Default]` | Marks this template as the default for the branch |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/offer-letters/templates/"` `hx-trigger="load"` `hx-target="#template-manager-grid"` `hx-swap="innerHTML"`. `[Edit Template]` click: `hx-get="/api/v1/group/{group_id}/adm/offer-letters/templates/{template_id}/edit/"` `hx-target="#template-editor-drawer"` `hx-swap="innerHTML"`.

**Empty State:** "No letter templates configured. Add a template for each branch to enable offer letter generation." CTA: `[+ Add Template]`

---

### 5.5 Bulk Dispatch Panel

**Display:** Action panel at the bottom of the page or accessible via `[Bulk Dispatch →]` header button. Step-by-step form:
1. Select date range of allocations to include
2. Select branches (multi-select — defaults to all)
3. Select letter type filter (Conditional / Unconditional / Both)
4. Preview count: "This will generate letters for {N} students across {M} branches."
5. Dispatch channel: WhatsApp / Email / Both
6. `[Generate & Send All]` — confirmation dialog before execution

**HTMX Pattern:** Step 1–3 inputs: `hx-get="/api/v1/group/{group_id}/adm/offer-letters/bulk/preview/?{params}"` `hx-target="#bulk-preview-count"` `hx-swap="innerHTML"` `hx-trigger="change"` (real-time count update). `[Generate & Send All]`: `hx-post="/api/v1/group/{group_id}/adm/offer-letters/bulk/dispatch/"` `hx-target="#bulk-dispatch-status"` `hx-swap="innerHTML"` `hx-confirm="Generate and send {N} offer letters? This cannot be undone."`

---

## 6. Drawers & Modals

### 6.1 Offer Letter Preview Drawer
- **Width:** 640px (right-side slide-in)
- **Trigger:** `[Preview]` in offer letter queue or sent tracker
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/offer-letters/{student_id}/preview/`

**Content:** Full rendered letter preview with:
- Branch letterhead (logo, address, contact)
- Student name and address block
- Admission details: Branch, Stream, Section, Joining Date
- Fee table: Tuition fee, hostel fee (if applicable), scholarship deduction, net payable, payment deadline
- Document submission checklist and deadline
- Conditional clauses (if conditional offer)
- Footer with signature block
- Actions: `[Generate PDF]` · `[Send via WhatsApp]` · `[Send via Email]` · `[Close]`

---

### 6.2 Template Editor Drawer
- **Width:** 640px
- **Trigger:** `[Edit Template]` in template manager
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/offer-letters/templates/{template_id}/edit/`

**Content:** Rich text editor with merge field support. Merge fields: `{{student_name}}`, `{{branch_name}}`, `{{stream}}`, `{{joining_date}}`, `{{fee_amount}}`, `{{document_deadline}}`, etc. Preview toggle. `[Save Template]` · `[Save as Draft]` · `[Cancel]`

---

### 6.3 Expiry Action Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Extend Deadline]` or `[Cancel Offer]` in expired letters panel
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/offer-letters/{letter_id}/expiry-action/`

**Fields (Extend):** New deadline date picker, Note to student, Notify student (toggle).
**Fields (Cancel):** Reason for cancellation (dropdown: No Response / Fee Non-payment / Seat Needed for Waitlist / Other), Internal note, Trigger waitlist promotion (toggle).

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Offer letter generated | "Offer letter generated for {Student name}." | Success | 4s |
| Letter sent via WhatsApp | "Offer letter sent to {Student name} via WhatsApp." | Success | 4s |
| Letter sent via email | "Offer letter sent to {Student name} via email." | Success | 4s |
| Bulk letters generated and sent | "{N} offer letters generated and dispatched successfully." | Success | 5s |
| Reminder sent | "Reminder sent to {Student name}. Deadline extended to {date}." | Info | 5s |
| Deadline extended | "Offer deadline extended to {date} for {Student name}." | Info | 4s |
| Offer cancelled | "Offer cancelled for {Student name}. Seat freed for waitlist." | Warning | 5s |
| Template saved | "Offer letter template saved for {Branch}." | Success | 4s |
| Letter generation failed | "Could not generate letter for {Student name} — template missing for {Branch}." | Error | 6s |
| Bulk dispatch failed (partial) | "{N} letters sent; {M} failed. Download error report for details." | Warning | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No letters pending generation | Green checkmark | "Queue is Empty" | "All allocated students have offer letters generated." | — |
| No letters sent yet | Envelope graphic | "No Letters Sent Yet" | "Generate offer letters and dispatch them to start tracking responses." | `[+ Generate Letters →]` |
| No expired letters | Timer graphic | "No Expired Letters" | "All sent letters are within the response window or have been acknowledged." | — |
| No templates configured | Template graphic | "No Templates Found" | "Configure a letter template for each branch to enable generation." | `[+ Add Template]` |
| Counsellor — no letters for assigned students | Person + letter graphic | "No Offer Letters Yet" | "Offer letters for your assigned students will appear here once generated." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton (queue table + KPI bar shimmer) |
| KPI bar auto-refresh | Inline spinner on each KPI card |
| Offer letter queue load | Table body skeleton |
| Sent tracker filter change | Table body skeleton (5-row shimmer) |
| Sent tracker pagination | Table body skeleton |
| Expired letters panel refresh | Panel skeleton |
| Template manager grid load | Card grid shimmer |
| Offer letter preview drawer open | Drawer content skeleton (letter shimmer) |
| Template editor drawer open | Drawer content skeleton |
| Bulk preview count update (real-time) | Inline spinner next to count |
| Bulk dispatch execution | Full-panel progress bar "Generating and sending letters…" |
| Single letter generation | Button spinner |
| Single letter send | Button spinner |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| Element | Dir (23) | Coord (24) | Counsellor (25) | CEO |
|---|---|---|---|---|
| [+ Generate Letters →] button | Hidden | Visible | Hidden | Hidden |
| [Bulk Dispatch →] button | Hidden | Visible | Hidden | Hidden |
| Offer Letter Queue section | Hidden | Visible | Hidden | Hidden |
| [Generate] action in queue | Hidden | Visible | Hidden | Hidden |
| [Send] action in queue | Hidden | Visible | Hidden | Hidden |
| Sent Letters Tracker | Visible | Visible | Own students only | Visible |
| [Resend] action | Hidden | Visible | Hidden | Hidden |
| Expired Letters Alert | Visible | Visible | Hidden | Hidden |
| [Send Reminder] in expired panel | Hidden | Visible | Hidden | Hidden |
| [Extend Deadline] in expired panel | Hidden | Visible | Hidden | Hidden |
| [Cancel Offer] in expired panel | Visible | Hidden | Hidden | Hidden |
| Letter Template Manager | Hidden | Visible | Hidden | Hidden |
| Bulk Dispatch Panel | Hidden | Visible | Hidden | Hidden |
| Offer Letter Preview Drawer — [Send] buttons | Hidden | Visible | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/offer-letters/kpis/` | JWT G3+ | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/offer-letters/queue/` | JWT G3+ | List students pending offer letter generation |
| POST | `/api/v1/group/{group_id}/adm/offer-letters/generate/` | JWT G3 | Generate offer letter for a student |
| POST | `/api/v1/group/{group_id}/adm/offer-letters/send/` | JWT G3 | Send an offer letter via WhatsApp/email |
| GET | `/api/v1/group/{group_id}/adm/offer-letters/sent/` | JWT G3+ | List sent letters with filters |
| GET | `/api/v1/group/{group_id}/adm/offer-letters/expired/` | JWT G3+ | List expired letters (no response ≥ 7 days) |
| GET | `/api/v1/group/{group_id}/adm/offer-letters/{student_id}/preview/` | JWT G3+ | Rendered offer letter preview (HTML fragment) |
| PATCH | `/api/v1/group/{group_id}/adm/offer-letters/{letter_id}/extend/` | JWT G3 | Extend offer deadline |
| DELETE | `/api/v1/group/{group_id}/adm/offer-letters/{letter_id}/cancel/` | JWT G3 (Director) | Cancel offer and free seat |
| POST | `/api/v1/group/{group_id}/adm/offer-letters/{letter_id}/remind/` | JWT G3 | Send reminder for expired letter |
| GET | `/api/v1/group/{group_id}/adm/offer-letters/templates/` | JWT G3 | List letter templates |
| GET | `/api/v1/group/{group_id}/adm/offer-letters/templates/{template_id}/edit/` | JWT G3 | Template edit form |
| PATCH | `/api/v1/group/{group_id}/adm/offer-letters/templates/{template_id}/` | JWT G3 | Save template |
| GET | `/api/v1/group/{group_id}/adm/offer-letters/bulk/preview/` | JWT G3 | Preview count for bulk dispatch |
| POST | `/api/v1/group/{group_id}/adm/offer-letters/bulk/dispatch/` | JWT G3 | Bulk generate and send offer letters |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `/api/v1/group/{group_id}/adm/offer-letters/kpis/` | `#offer-letter-kpi-bar` | `innerHTML` |
| Offer letter queue load | `load` | GET `/api/v1/group/{group_id}/adm/offer-letters/queue/` | `#offer-queue-table-body` | `innerHTML` |
| Queue pagination click | `click` | GET `/api/v1/group/{group_id}/adm/offer-letters/queue/?page={n}` | `#offer-queue-table-wrapper` | `innerHTML` |
| Sent tracker filter change | `change` | GET `/api/v1/group/{group_id}/adm/offer-letters/sent/?{filters}` | `#sent-tracker-table-body` | `innerHTML` |
| Sent tracker pagination click | `click` | GET `/api/v1/group/{group_id}/adm/offer-letters/sent/?page={n}&{filters}` | `#sent-tracker-wrapper` | `innerHTML` |
| Expired letters panel refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/offer-letters/expired/` | `#expired-letters-panel` | `innerHTML` |
| [Preview] button click | `click` | GET `/api/v1/group/{group_id}/adm/offer-letters/{student_id}/preview/` | `#offer-letter-preview-drawer` | `innerHTML` |
| [Generate] single letter | `click` | POST `/api/v1/group/{group_id}/adm/offer-letters/generate/` | `#offer-queue-table-body` | `innerHTML` |
| [Send] single letter | `click` | POST `/api/v1/group/{group_id}/adm/offer-letters/send/` | `#sent-tracker-table-body` | `innerHTML` |
| Bulk generate + send | `click` | POST `/api/v1/group/{group_id}/adm/offer-letters/bulk/dispatch/` | `#bulk-dispatch-status` | `innerHTML` |
| Bulk preview count update | `change` | GET `/api/v1/group/{group_id}/adm/offer-letters/bulk/preview/?{params}` | `#bulk-preview-count` | `innerHTML` |
| Template manager load | `load` | GET `/api/v1/group/{group_id}/adm/offer-letters/templates/` | `#template-manager-grid` | `innerHTML` |
| [Edit Template] click | `click` | GET `/api/v1/group/{group_id}/adm/offer-letters/templates/{id}/edit/` | `#template-editor-drawer` | `innerHTML` |
| Template save | `submit` | PATCH `/api/v1/group/{group_id}/adm/offer-letters/templates/{id}/` | `#template-manager-grid` | `innerHTML` |
| Expiry action modal open | `click` | GET `/api/v1/group/{group_id}/adm/offer-letters/{letter_id}/expiry-action/` | `#expiry-action-modal` | `innerHTML` |
| Expiry action form submit | `submit` | PATCH/DELETE `/api/v1/group/{group_id}/adm/offer-letters/{letter_id}/...` | `#expired-letters-panel` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
