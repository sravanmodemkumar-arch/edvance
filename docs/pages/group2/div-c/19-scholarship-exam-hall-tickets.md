# Page 19: Scholarship Exam Hall Tickets

**URL:** `/group/adm/scholarship-exam/hall-tickets/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions · Scholarship Section

---

## 1. Purpose

The Hall Ticket Manager handles the end-to-end admit card lifecycle for all registered scholarship examination candidates. An admit card (hall ticket) is a mandatory entry document — it contains the candidate's name, assigned roll number, exam date and time, venue branch address, hall/room number, examination instructions, and a unique QR code that invigilators scan at the entry gate for verification. Without a valid hall ticket, a candidate cannot sit the exam.

For large scholarship drives — where a single group-wide exam may involve 5,000 or more candidates appearing across 30–40 branch venues simultaneously — individual manual dispatch is not feasible. This page provides bulk generation (all hall tickets for an exam in one batch operation), bulk WhatsApp dispatch via the group's messaging integration, and a download ZIP facility for branch-level batches so invigilators can collect and distribute physical copies where digital access is limited. The page also tracks the dispatch pipeline: which candidates have had tickets generated, which have been sent via WhatsApp, which have confirmed download, and which are stuck due to data issues.

Data quality is a key prerequisite: incomplete parent phone numbers, mismatched names, missing branch assignments, or unconfirmed venues will block hall ticket generation for affected candidates. The Data Issues List (Section 5.4) surfaces these records so the Exam Manager can resolve them before bulk dispatch. Countdown to exam date is shown prominently so the Manager can plan the dispatch window with adequate lead time.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Exam Manager (26) | G3 | Full — generate, send, download, resolve data issues | Primary operator of this page |
| Group Admissions Director (23) | G3 | View only — all status metrics and tables | Cannot generate or dispatch |
| Group Admission Coordinator (24) | G3 | View status only — per-exam summary | No generate/dispatch/download |
| Group Scholarship Manager (27) | G3 | No access | Not in exam function scope |
| Other Roles | G3 | No access | Page restricted to exam function |

**Enforcement:** Django view enforces `role in ['scholarship_exam_manager', 'admissions_director', 'admission_coordinator']`. WhatsApp dispatch and batch download APIs require JWT with `function == scholarship_exam` and `role == scholarship_exam_manager`. All candidate PII (phone numbers) rendered server-side only — no raw PII exposed in API JSON response to frontend.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarship Exams → Hall Tickets
```

### 3.2 Page Header
- **Title:** Scholarship Exam Hall Tickets
- **Subtitle:** Admit card generation and dispatch
- **Action Buttons (Exam Manager only):** `[Generate All]` · `[Send All via WhatsApp]` · `[Download Batch ZIP]`
- **Context:** Exam selector dropdown is the primary control — all content below updates on selection

### 3.3 Alert Banner
Triggers:
- **Red — Data Issues Blocking Generation:** "14 candidates have data issues. Hall tickets cannot be generated for them until resolved. [Fix Now →]"
- **Amber — Exam Close, Dispatch Incomplete:** "{Exam Name} is in 3 days. {n} candidates have not received their hall tickets. [Send Now →]"
- **Amber — WhatsApp Send Failures:** "8 WhatsApp dispatches failed (invalid phone numbers). [Retry Failed →]"
- **Green — All Dispatched:** "All {n} hall tickets for {Exam Name} have been generated and sent successfully."
- **Blue — Generation in Progress:** "Batch generation in progress for {Exam Name}. {progress}% complete."

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Candidates Registered | COUNT of registrations for selected exam | `exam_registration` filter by exam | Blue always | → full candidate table |
| Hall Tickets Generated % | (generated_count / total_registered) × 100 | `hall_ticket` aggregation | Green ≥100% · Amber 50–99% · Red <50% | → table filtered by generated = No |
| Hall Tickets Sent via WhatsApp % | (sent_count / generated_count) × 100 | `hall_ticket` aggregation | Green ≥100% · Amber 50–99% · Red <50% | → table filtered by sent = No |
| Tickets with Errors | COUNT where data_issue = True OR whatsapp_status = 'failed' | `hall_ticket` + `exam_registration` | Red > 0 · Green = 0 | → Section 5.4 data issues |
| Candidates Downloaded | COUNT where download_confirmed = True | `hall_ticket` aggregation | Blue always | → table filtered by downloaded = Yes |
| Days Until Exam | DATEDIFF(exam_date, today) | `scholarship_exam` | Red ≤ 2 · Amber 3–7 · Green > 7 | None (countdown chip) |

**HTMX Refresh:** KPI bar refreshes every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar`. Exam selector change also refreshes KPIs immediately via `hx-trigger="change"`.

---

## 5. Sections

### 5.1 Exam Selector

**Display:** Prominent full-width card at top of page.

**Contents:**
- Dropdown: "Select Scholarship Exam" — lists all non-cancelled exams in current cycle (most recent first)
- On selection (HTMX): Quick stats appear below dropdown — Exam date, Mode, Branches, Total registered, Generation status, Days to exam countdown chip
- Persist selection in session so page refresh retains context

**HTMX Pattern:** `hx-trigger="change"` on selector → `GET /api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/exam/{exam_id}/summary/` targeting `#exam-quick-stats` with `hx-swap="innerHTML"`, then triggers dependent section loads.

---

### 5.2 Hall Ticket Status Table

**Display:** Sortable, selectable (checkbox), server-side paginated (20/page). Shown after exam is selected. Default sort: Roll No ASC.

**Columns:**

| Column | Notes |
|---|---|
| Roll No | Assigned roll number |
| Candidate Name | Full name |
| Branch | Branch where candidate appears |
| Class | Class level |
| Parent Phone | Masked: last 4 digits visible (e.g., ×××× ××3421) |
| Generated | Yes (green ✓) / No (red ✗) |
| Sent via WhatsApp | Yes (green ✓) / No (amber ✗) / Failed (red ✗) |
| Downloaded | Yes (green ✓) / No (grey –) |
| Data Issues | None (green) / Has issues (red flag — hover for detail) |
| Actions | `[Preview]` · `[Resend]` (if already sent) · `[Download]` |

**Filters:** Generated (Yes/No), Sent (Yes/No/Failed), Branch, Data Issues (Has Issues / No Issues)

**Bulk Actions (Exam Manager only):** `[Generate All]` · `[Send All via WhatsApp]` · `[Download Batch ZIP]` · `[Export List]`

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/` targeting `#hall-ticket-table-body`.

**Empty State:** Exam not selected. Message: "Select an exam above to view hall ticket status."

---

### 5.3 Generation & Dispatch Summary

**Display:** Row of stat cards below the exam selector — updates on exam selection.

**Cards (5 cards in a row):**
1. Generated — count (blue)
2. Sent — count (green if = total, else amber)
3. Delivered (WhatsApp delivery confirmed) — count (green)
4. Failed (send failed) — count (red if > 0, else green)
5. Pending (not yet generated) — count (amber if > 0, else green)

**HTMX Pattern:** `hx-trigger="load"` on section + event-triggered refresh after any generate/send action targeting `#dispatch-summary`.

---

### 5.4 Data Issues List

**Display:** Alert list (collapsible card, expanded when issues > 0). Each row = one candidate with an issue blocking generation.

**Columns:** Candidate Name · Branch · Roll No · Issue Description (e.g., "Parent phone missing", "Branch not confirmed as venue", "Name contains special characters") · `[Edit →]`

**`[Edit →]`:** Opens candidate-data-edit drawer.

**HTMX Pattern:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/data-issues/` targeting `#data-issues-list`. Refreshes after any data edit is saved.

**Empty State:** No data issues. Icon: check-circle. Heading: "No Data Issues". Description: "All candidates have complete data. Ready to generate."

---

### 5.5 Batch Download Panel

**Display:** Card — batch download tool for branch-level ZIP files.

**Content:**
- Branch multi-select (or "All Branches")
- Preview: "Selecting {n} branch(es) — {count} hall tickets"
- `[Download ZIP of Hall Tickets]` button (only active if tickets generated for selected branches)
- Progress indicator during ZIP preparation

**HTMX Pattern:** Branch selection → `hx-trigger="change"` → `GET /api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/batch-preview/?branches={ids}` targeting `#batch-preview-info` with `hx-swap="innerHTML"`. Download triggers a standard file download endpoint (Django view streams ZIP).

**Empty State:** "Select an exam and generate hall tickets first to enable batch download."

---

## 6. Drawers & Modals

### 6.1 Hall Ticket Preview Drawer
- **Width:** 640px (right slide-in)
- **Trigger:** `[Preview]` on table row
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/{registration_id}/preview/`
- **Content:** Rendered hall ticket preview — candidate photo (if uploaded), name, roll number, exam name, date, time, reporting time, venue branch name + address, hall/room, instructions, QR code image. Print button available. Download PDF button.
- **Footer Actions:** `[Download PDF]` · `[Send via WhatsApp]` · `[Close]`

### 6.2 Candidate Data Edit Drawer
- **Width:** 480px
- **Trigger:** `[Edit →]` in Section 5.4 Data Issues List
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/{registration_id}/data-edit/`
- **Content:** Editable fields relevant to the data issue — parent phone, candidate name (typo fix), class, branch assignment. Shows issue description at top.
- **Submit:** `hx-put` → `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/{registration_id}/` · on success: refreshes data issues list, refreshes table row, shows success toast

### 6.3 Resend Confirm Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Resend]` on table row
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/{registration_id}/resend-confirm/`
- **Content:** "Resend hall ticket to {Candidate Name} via WhatsApp ({masked phone})?" + `[Confirm Resend]` + `[Cancel]`
- **Submit:** `hx-post` → `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/{registration_id}/resend/` · on success: update row WhatsApp status, show toast

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Generation started (bulk) | "Generating hall tickets for {n} candidates. This may take a moment." | Info | 4 s |
| Generation complete | "Hall tickets generated for {n} candidates." | Success | 4 s |
| Generation partial (with errors) | "Hall tickets generated: {n} success, {e} errors. [View Issues →]" | Warning | 6 s |
| WhatsApp dispatch started | "Dispatching hall tickets to {n} candidates via WhatsApp." | Info | 4 s |
| WhatsApp dispatch complete | "Hall tickets sent: {n} delivered, {f} failed." | Success | 5 s |
| Single ticket resent | "Hall ticket resent to {Candidate Name}." | Success | 3 s |
| Candidate data saved | "Data updated for {Candidate Name}. Hall ticket regenerated." | Success | 4 s |
| Batch ZIP ready | "ZIP file ready. Download starting..." | Success | 3 s |
| Batch ZIP failed | "ZIP preparation failed. Please retry." | Error | 5 s |
| Data issue resolved | "Data issue resolved for {Candidate Name}." | Success | 3 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No exam selected | Select-box icon | "Select an Exam" | "Choose a scholarship exam from the dropdown to manage hall tickets." | None (points to selector) |
| No registrations for selected exam | Users icon | "No Registered Candidates" | "No candidates have registered for this exam yet." | `[Go to Exam Scheduler →]` |
| No data issues | Check-circle icon | "No Data Issues" | "All candidates have complete data." | None |
| All tickets generated and sent | Ticket icon (green) | "All Hall Tickets Dispatched" | "Every registered candidate has received their hall ticket." | `[Download Batch ZIP]` |
| Filter returns no results | Filter icon | "No Candidates Match Filters" | "Try adjusting your filter criteria." | `[Clear Filters]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: KPI shimmer (6 cards) + exam selector placeholder |
| Exam selector change | Section content overlay spinner; KPI bar shimmer |
| Table load after exam selection | Table body skeleton (10 row shimmer) |
| Table filter change | Table body skeleton (5 row shimmer) |
| Bulk generate button click | Full-width progress bar (estimated completion) + button spinner |
| Bulk WhatsApp dispatch | Progress bar with sent/total counter updating via HTMX polling |
| Preview drawer open | 640px drawer skeleton (layout shimmer + QR placeholder) |
| Data edit drawer open | 480px drawer with form field shimmers |
| Batch ZIP preparation | Spinner in download panel with "Preparing ZIP..." text |
| Data issues list load | List skeleton (3 row shimmers) |

---

## 10. Role-Based UI Visibility

| Element | Exam Manager (26) | Director (23) | Coordinator (24) | Other Roles |
|---|---|---|---|---|
| `[Generate All]` button | Visible | Hidden | Hidden | No access |
| `[Send All via WhatsApp]` button | Visible | Hidden | Hidden | No access |
| `[Download Batch ZIP]` button | Visible | Hidden | Hidden | No access |
| Bulk action bar in table | Visible | Hidden | Hidden | No access |
| `[Resend]` on table row | Visible | Hidden | Hidden | No access |
| `[Preview]` on table row | Visible | Visible | Visible | No access |
| `[Edit →]` in Data Issues | Visible | Hidden | Hidden | No access |
| Section 5.4 Data Issues | Visible (edit) | Visible (read) | Visible (read) | No access |
| Section 5.5 Batch Download | Visible | Hidden | Hidden | No access |
| Parent phone (unmasked) | Masked (×× last 4) | Masked | Masked | No access |
| Page itself | Accessible | Accessible | Accessible | 403 redirect |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/kpis/` | JWT G3 | KPI bar data (requires exam_id param) |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/exam/{exam_id}/summary/` | JWT G3 | Exam quick stats on selector change |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/` | JWT G3 | Paginated candidate hall ticket status |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/generate-all/` | JWT G3 write | Bulk generate hall tickets |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/send-all-whatsapp/` | JWT G3 write | Bulk WhatsApp dispatch |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/{registration_id}/preview/` | JWT G3 | Hall ticket preview drawer fragment |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/{registration_id}/data-edit/` | JWT G3 | Candidate data edit drawer fragment |
| PUT | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/{registration_id}/` | JWT G3 write | Update candidate data |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/{registration_id}/resend-confirm/` | JWT G3 | Resend confirm modal fragment |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/candidates/{registration_id}/resend/` | JWT G3 write | Resend single hall ticket |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/data-issues/` | JWT G3 | Data issues list |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/batch-preview/` | JWT G3 | Batch download preview (count by branch) |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/batch-download/` | JWT G3 write | Stream ZIP of hall ticket PDFs |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/{exam_id}/dispatch-summary/` | JWT G3 | Generation & dispatch stat cards |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `.../hall-tickets/kpis/?exam_id={id}` | `#kpi-bar` | `innerHTML` |
| Exam selector change | `change` on exam dropdown | GET `.../hall-tickets/exam/{exam_id}/summary/` | `#exam-quick-stats` | `innerHTML` |
| Load candidate table after exam select | `htmx:afterSettle` from exam selector | GET `.../hall-tickets/{exam_id}/candidates/` | `#hall-ticket-table-container` | `innerHTML` |
| Filter candidate table | `change` on filter inputs | GET `.../hall-tickets/{exam_id}/candidates/?{filters}` | `#hall-ticket-table-body` | `innerHTML` |
| Paginate table | `click` on page link | GET `.../hall-tickets/{exam_id}/candidates/?page={n}` | `#hall-ticket-table-container` | `innerHTML` |
| Bulk generate all | `click` on `[Generate All]` | POST `.../hall-tickets/{exam_id}/generate-all/` | `#dispatch-summary` | `innerHTML` |
| Bulk WhatsApp send | `click` on `[Send All via WhatsApp]` | POST `.../hall-tickets/{exam_id}/send-all-whatsapp/` | `#dispatch-summary` | `innerHTML` |
| Open hall ticket preview drawer | `click` on `[Preview]` | GET `.../hall-tickets/{exam_id}/candidates/{reg_id}/preview/` | `#drawer-container` | `innerHTML` |
| Open candidate data edit drawer | `click` on `[Edit →]` in issues | GET `.../hall-tickets/{exam_id}/candidates/{reg_id}/data-edit/` | `#drawer-container` | `innerHTML` |
| Submit candidate data fix | `submit` on data edit form | PUT `.../hall-tickets/{exam_id}/candidates/{reg_id}/` | `#data-issues-list` | `innerHTML` |
| Open resend confirm modal | `click` on `[Resend]` | GET `.../hall-tickets/{exam_id}/candidates/{reg_id}/resend-confirm/` | `#modal-container` | `innerHTML` |
| Confirm resend | `click` on `[Confirm Resend]` | POST `.../hall-tickets/{exam_id}/candidates/{reg_id}/resend/` | `#table-row-{reg_id}` | `outerHTML` |
| Load data issues list | `load` on section | GET `.../hall-tickets/{exam_id}/data-issues/` | `#data-issues-list` | `innerHTML` |
| Branch selection for batch download | `change` on branch multi-select | GET `.../hall-tickets/{exam_id}/batch-preview/?branches={ids}` | `#batch-preview-info` | `innerHTML` |
| Load dispatch summary | `load` on section | GET `.../hall-tickets/{exam_id}/dispatch-summary/` | `#dispatch-summary` | `innerHTML` |
| Refresh dispatch summary after generate | `htmx:afterRequest` from generate/send calls | GET `.../hall-tickets/{exam_id}/dispatch-summary/` | `#dispatch-summary` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
