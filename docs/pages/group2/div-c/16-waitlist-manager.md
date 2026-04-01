# Page 16 — Waitlist Manager

- **URL:** `/group/adm/waitlist/`
- **Template:** `portal_base.html`
- **Theme:** Light

---

## 1. Purpose

The Waitlist Manager governs the fair and timely handling of applicants who meet all admission criteria but cannot be admitted immediately because the relevant branch-stream combination is full. Waitlisting is not a dead end — it is a managed queue that actively converts to enrolments when seats become available. A confirmed student who withdraws, an offer that expires without acceptance, a cross-branch transfer that frees a seat: all of these events should trigger an automatic check of the waitlist and prompt promotion of the highest-ranked eligible student within 24 hours.

For competitive branches, waitlists can grow to 50–100 candidates and must be managed with documented fairness. Position on the waitlist is typically determined by entrance test score, interview rank, application date, or a combination thereof. Arbitrary or undocumented promotions create institutional risk — a parent who believes their child was skipped over unfairly can challenge the admission. This page therefore requires a clear rationale for every promotion decision: automated promotions (by rank) are logged automatically; manual overrides require a documented reason and are visible in the Promotion History (Section 5.3).

The Waitlist by Branch chart (Section 5.4) is a strategic tool. If Branch A has 60 students on the MPC waitlist while Branch B has 15 empty MPC seats, that data should prompt the Coordinator to reach out to waitlisted students about Branch B availability. The Bulk Notification Panel (Section 5.5) enables this: the Coordinator can compose a WhatsApp or email to all waitlisted MPC students across specific branches inviting them to consider Branch B, turning a waitlist management exercise into a seat-filling opportunity. Promotions are never assumed to be accepted — every promoted student receives an offer letter (integrated with Page 14) and must formally accept within a configurable window.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | View all + override promotions | Can manually promote a student out of sequence with documented reason |
| Group Admission Coordinator (Role 24) | G3 | Full waitlist management — all branches | Primary operator; promote, notify, remove, bulk notify |
| Group Admission Counsellor (Role 25) | G3 | View only — own students' waitlist position | Read-only; cannot promote or remove |
| CEO / Executive | G3+ | Read only | Demand intelligence overview |

> **Enforcement:** `[Promote →]`, `[Notify →]`, `[Remove →]` controls render only for `request.user.role in ['coordinator', 'admissions_director']`. Manual override promotions (out-of-sequence) enforce `request.user.role == 'admissions_director'` with a mandatory reason field. Counsellor queryset filters to `WaitlistEntry.student.assigned_counsellor = request.user`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Waitlist Manager
```

### 3.2 Page Header
- **Title:** Waitlist Manager
- **Subtitle:** Manage waitlisted applicants across all branches — `{current_cycle_name}`
- **Right-side actions:** `[Bulk Notify →]` (Coordinator) · `[Export Waitlist →]` · `[Refresh ↺]`

### 3.3 Alert Banner

| Trigger | Message |
|---|---|
| Seats just opened (waitlist promotions available) | "{N} seat(s) opened. {N} waitlisted student(s) can be promoted now." |
| Waitlist students with alternative offers > 0 | "{N} waitlisted students have accepted alternative offers elsewhere. Review for removal." |
| Promotions offered but not accepted in > 48 hours | "{N} promoted student(s) have not accepted their offer in over 48 hours." |
| Average waitlist age > 14 days | "Average waitlist duration is {N} days — above the 14-day guideline. Review promotion pace." |
| Waitlist-to-enrolment conversion < 30% | "Waitlist conversion rate is {X}% this cycle — below the 30% target." |

---

## 4. KPI Summary Bar

> Auto-refreshes every 5 minutes via HTMX: `hx-get="/api/v1/group/{group_id}/adm/waitlist/kpis/" hx-trigger="every 5m" hx-target="#waitlist-kpi-bar" hx-swap="innerHTML"`

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Waitlisted (Group-wide) | Count of Active waitlist entries | `WaitlistEntry.status='active'` | Neutral (blue) | Filters table to active entries |
| Branches with Waitlists | Count of distinct branch-stream combos with at least 1 active waitlist entry | Computed | Neutral (indigo) | Opens waitlist by branch chart (5.4) |
| Promotions Available Now | Count of seats that just opened matched to waitlist entries | Computed — triggered when `OfferLetter` is cancelled or seat freed | Red if > 0 (urgent) | Scrolls to Seats Just Opened panel (5.2) |
| Promotions Completed Today | `WaitlistEntry.promoted_at__date = today` | Count | Green if > 0 | Filters promotion history to today |
| Avg Waitlist Age (days) | Mean of `(today - waitlisted_at)` for Active entries | Computed | Green ≤ 7; amber 8–14; red > 14 | Filters table to oldest entries |
| With Alternative Offers | Waitlisted students who have indicated alternative school offer | `alternative_offer=True` | Amber if > 0 | Filters table to `alternative_offer=True` |

---

## 5. Sections

### 5.1 Waitlist Table

**Display:** Sortable, server-side paginated table. 20 rows per page. Checkbox column for bulk notify.

**Columns:**

| Column | Notes |
|---|---|
| ☐ Checkbox | Select for bulk notifications |
| Position | Waitlist rank for this branch+stream (1 = next to be promoted) |
| Student Name | Clickable — opens waitlist-student-detail drawer |
| Branch | Branch name |
| Stream | Stream name |
| Waitlist Date | `DD MMM YYYY` — date added to waitlist |
| Waitlist Reason | Why placed on waitlist (e.g., "MPC seats full at Branch A") |
| Score / Rank | Entrance test score or rank used for ordering |
| Alternative Offer | Yes (amber badge) / No |
| Days on Waitlist | Integer; colour: green ≤ 7, amber 8–14, red > 14 |
| Status | Badge: Active (blue) / Offered (amber) / Withdrew (grey) / Promoted (green) |
| Actions | `[Promote →]` · `[Notify →]` · `[Remove →]` |

**Filters:** Branch (multi-select), Stream (multi-select), Status (multi-select)

**HTMX Pattern:** Filter changes: `hx-get="/api/v1/group/{group_id}/adm/waitlist/?{filters}"` `hx-target="#waitlist-table-body"` `hx-swap="innerHTML"` `hx-trigger="change"`. Pagination: `hx-target="#waitlist-table-wrapper"`. `[Promote →]` click: opens promote-to-seat-modal. `[Remove →]` click: opens remove-from-waitlist-modal. Row name click: opens waitlist-student-detail drawer.

**Empty State:** Illustration of empty queue. Heading: "No Students on Waitlist." Description: "No applicants are currently waitlisted for the current cycle." CTA: —

---

### 5.2 Seats Just Opened

**Display:** High-priority alert section. Appears dynamically when a confirmed student withdraws or an offer expires, freeing a seat in a branch-stream combination that has a waitlist. Each alert card shows:
- Branch + Stream where seat opened
- Reason seat opened (Withdrawal / Offer Expired / Transfer / Other)
- Time seat opened (e.g., "12 minutes ago")
- Top waitlisted student: Name, Position 1, Score/Rank
- `[Promote Now →]` — opens promote-to-seat-modal pre-filled with this seat and student

If no promotions are available, the panel collapses to a single-line indicator: "No new seats available for waitlist promotion."

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/waitlist/seats-opened/"` `hx-trigger="load, every 60s"` `hx-target="#seats-opened-panel"` `hx-swap="innerHTML"` (60-second poll for near-real-time responsiveness without background processing dependencies)

**Empty State:** "No seats currently available for immediate promotion."

---

### 5.3 Promotion History

**Display:** Paginated table of past promotions.

| Column | Notes |
|---|---|
| Student Name | Name |
| Branch | Branch promoted into |
| Stream | Stream |
| Promoted On | `DD MMM YYYY HH:MM` |
| Seat Opened Reason | What freed the seat |
| Time to Promotion | Duration between seat opening and promotion action (hours) |
| Promoted By | Coordinator / Director (manual) or "System (Auto)" |
| Accepted? | Yes (green) / No — Offer Pending (amber) / No — Declined (red) |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/waitlist/promotions/"` `hx-trigger="load"` `hx-target="#promotion-history-table-body"` `hx-swap="innerHTML"`. Pagination: `hx-target="#promotion-history-wrapper"`.

**Empty State:** "No promotions recorded this cycle."

---

### 5.4 Waitlist by Branch

**Display:** Grouped bar chart (Chart.js 4.x). X-axis: Branches. Grouped bars per branch by stream (one colour per stream). Y-axis: Waitlist count. Hover tooltip shows branch name, stream, count. Clicking a bar filters the Waitlist Table to that branch+stream. Branch filter dropdown to narrow displayed branches.

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/waitlist/by-branch/"` `hx-trigger="load"` `hx-target="#waitlist-branch-chart-data"` `hx-swap="innerHTML"`; bar click: `hx-get="/api/v1/group/{group_id}/adm/waitlist/?branch={id}&stream={id}"` `hx-target="#waitlist-table-body"` `hx-swap="innerHTML"`.

**Empty State:** "No waitlist data available for chart display."

---

### 5.5 Bulk Notification Panel

**Display:** Action panel accessible via `[Bulk Notify →]` header button or inline checkbox selection in the table. Workflow:
1. Select students (via table checkboxes, or filter-then-select-all)
2. Compose message: template dropdown (pre-written templates: "Seat Available", "Status Update", "Reminder") or custom text
3. Channel: WhatsApp / Email / Both
4. Preview: "Sending to {N} students across {M} branches"
5. `[Send →]` — confirmation dialog before dispatch

**HTMX Pattern:** Template selection: `hx-get="/api/v1/group/{group_id}/adm/waitlist/notification-templates/{template_id}/"` `hx-target="#notification-message-body"` `hx-swap="innerHTML"` `hx-trigger="change"` on template dropdown. `[Send →]`: `hx-post="/api/v1/group/{group_id}/adm/waitlist/bulk-notify/"` `hx-target="#bulk-notify-status"` `hx-swap="innerHTML"` `hx-confirm="Send notification to {N} waitlisted students?"`

---

## 6. Drawers & Modals

### 6.1 Waitlist Student Detail Drawer
- **Width:** 560px (right-side slide-in)
- **Trigger:** Click on Student Name in waitlist table
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/waitlist/{entry_id}/detail/`

**Content:** Student profile (name, class, stream, contact, guardian), entrance score and rank, application details link, waitlist position, waitlist date, all previous notifications sent (log), alternative offer status, notes from counsellor, `[Promote →]` button (Coordinator/Director), `[Remove from Waitlist →]` button.

---

### 6.2 Promote to Seat Modal
- **Width:** 480px (centred modal)
- **Trigger:** `[Promote →]` in table or `[Promote Now →]` in Seats Just Opened panel
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/waitlist/{entry_id}/promote/`

**Content:**
- Student name and current waitlist position (read-only)
- Seat details: Branch, Stream, Seat type (Day / Hosteler) — pre-filled from the opened seat
- Offer type: Conditional / Unconditional
- Offer acceptance deadline (date picker)
- Is this an out-of-sequence promotion? (toggle — Director only — if yes: mandatory reason field)
- Notify student on confirmation (toggle)
- `[Confirm Promotion → Generate Offer Letter]` · `[Cancel]`

---

### 6.3 Remove from Waitlist Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Remove →]` in table
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/waitlist/{entry_id}/remove/`

**Fields:** Removal reason (required dropdown: Student Withdrew / Accepted Alternative Offer / No Response After Multiple Contacts / Administrative / Other), Notes (optional), Notify student (toggle). `[Confirm Removal]` · `[Cancel]`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Student promoted | "{Student name} promoted from waitlist for {Branch} — {Stream}. Offer letter generation triggered." | Success | 5s |
| Manual override promotion | "{Student name} promoted out of sequence. Reason logged." | Warning | 5s |
| Student removed from waitlist | "{Student name} removed from waitlist. Reason: {reason}." | Info | 4s |
| Bulk notification sent | "Notification sent to {N} waitlisted students via {channel}." | Success | 5s |
| Promotion accepted | "{Student name} accepted their waitlist offer for {Branch}." | Success | 4s |
| Promotion offer expired | "Offer for {Student name} expired — no response in {N} hours. Position reopened." | Warning | 5s |
| Export started | "Waitlist export is being prepared. Download will start shortly." | Info | 5s |
| Promotion failed (no capacity) | "Cannot promote — {Branch} {Stream} seat no longer available." | Error | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No students on waitlist | Queue graphic | "No Waitlisted Students" | "No applicants are currently on the waitlist for the current cycle." | — |
| Filter returns no results | Search-miss graphic | "No Matching Entries" | "No waitlist entries match the selected branch, stream, or status." | `[Clear Filters]` |
| No seats just opened | Green shield graphic | "No Seats Available Right Now" | "When a confirmed student withdraws or an offer expires, available seats will appear here." | — |
| No promotion history | Archive graphic | "No Promotions Yet" | "Waitlist promotion history will appear here as promotions are made." | — |
| No waitlist branch data | Chart (empty) | "No Branch Data" | "Waitlist distribution will appear once students are added to the waitlist." | — |
| Counsellor — no assigned waitlist students | Person graphic | "No Students on Waitlist" | "None of your assigned students are currently on the waitlist." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton (table + KPI bar + seats panel shimmer) |
| KPI bar auto-refresh | Inline spinner on each KPI card |
| Waitlist table filter change | Table body skeleton (5-row shimmer) |
| Pagination click | Table body skeleton |
| Seats Just Opened panel poll | Panel skeleton (lightweight) |
| Promotion history table load | Table body skeleton |
| Waitlist by branch chart load | Chart area spinner |
| Waitlist student detail drawer open | Drawer content skeleton |
| Promote to seat modal open | Modal skeleton |
| Remove from waitlist modal open | Modal skeleton |
| Bulk notification template load | Message body shimmer |
| Bulk notify send action | Button spinner + "Sending…" overlay |
| Promote confirm action | Button spinner; row updates after success |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| Element | Dir (23) | Coord (24) | Counsellor (25) | CEO |
|---|---|---|---|---|
| [Promote →] action in table | Visible | Visible | Hidden | Hidden |
| [Notify →] action in table | Hidden | Visible | Hidden | Hidden |
| [Remove →] action in table | Visible | Visible | Hidden | Hidden |
| Out-of-sequence toggle in promote modal | Visible | Hidden | Hidden | Hidden |
| [Promote Now →] in Seats Just Opened | Visible | Visible | Hidden | Hidden |
| [Bulk Notify →] button | Hidden | Visible | Hidden | Hidden |
| Bulk checkbox column | Visible | Visible | Hidden | Hidden |
| Bulk Notification Panel | Hidden | Visible | Hidden | Hidden |
| Promotion History table | Visible | Visible | Hidden | Visible |
| Waitlist by Branch chart | Visible | Visible | Hidden | Visible |
| [Export Waitlist →] button | Visible | Visible | Hidden | Hidden |
| Waitlist Table | Visible (all) | Visible (all) | Own students only | Visible (all) |
| KPI bar | Visible | Visible | Hidden | Visible |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/waitlist/` | JWT G3+ | List waitlist entries with filters |
| GET | `/api/v1/group/{group_id}/adm/waitlist/kpis/` | JWT G3+ | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/waitlist/seats-opened/` | JWT G3+ | Seats that have just opened with matched waitlist candidates |
| GET | `/api/v1/group/{group_id}/adm/waitlist/promotions/` | JWT G3+ | Promotion history |
| GET | `/api/v1/group/{group_id}/adm/waitlist/by-branch/` | JWT G3+ | Waitlist counts by branch and stream (chart data) |
| GET | `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/detail/` | JWT G3+ | Student detail drawer content |
| GET | `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/promote/` | JWT G3 | Promote-to-seat modal form |
| POST | `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/promote/` | JWT G3 | Confirm promotion and trigger offer letter |
| GET | `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/remove/` | JWT G3 | Remove from waitlist modal form |
| DELETE | `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/` | JWT G3 | Remove student from waitlist with reason |
| POST | `/api/v1/group/{group_id}/adm/waitlist/bulk-notify/` | JWT G3 | Send bulk notification to selected waitlisted students |
| GET | `/api/v1/group/{group_id}/adm/waitlist/notification-templates/{template_id}/` | JWT G3 | Fetch notification template content |
| GET | `/api/v1/group/{group_id}/adm/waitlist/export/` | JWT G3+ | Export waitlist as CSV |
| POST | `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/notify/` | JWT G3 | Send notification to a single waitlisted student |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `/api/v1/group/{group_id}/adm/waitlist/kpis/` | `#waitlist-kpi-bar` | `innerHTML` |
| Waitlist table filter change | `change` | GET `/api/v1/group/{group_id}/adm/waitlist/?{filters}` | `#waitlist-table-body` | `innerHTML` |
| Waitlist table pagination click | `click` | GET `/api/v1/group/{group_id}/adm/waitlist/?page={n}&{filters}` | `#waitlist-table-wrapper` | `innerHTML` |
| Waitlist table sort click | `click` | GET `/api/v1/group/{group_id}/adm/waitlist/?sort={col}&order={dir}` | `#waitlist-table-body` | `innerHTML` |
| Student name click (open detail drawer) | `click` | GET `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/detail/` | `#waitlist-student-detail-drawer` | `innerHTML` |
| [Promote →] click | `click` | GET `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/promote/` | `#promote-to-seat-modal` | `innerHTML` |
| Promote form submit | `submit` | POST `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/promote/` | `#waitlist-table-body` | `innerHTML` |
| [Remove →] click | `click` | GET `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/remove/` | `#remove-waitlist-modal` | `innerHTML` |
| Remove form submit | `submit` | DELETE `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/` | `#waitlist-table-body` | `innerHTML` |
| Seats Just Opened panel poll | `load, every 60s` | GET `/api/v1/group/{group_id}/adm/waitlist/seats-opened/` | `#seats-opened-panel` | `innerHTML` |
| [Promote Now →] in seats panel | `click` | GET `/api/v1/group/{group_id}/adm/waitlist/{entry_id}/promote/` | `#promote-to-seat-modal` | `innerHTML` |
| Promotion history load | `load` | GET `/api/v1/group/{group_id}/adm/waitlist/promotions/` | `#promotion-history-table-body` | `innerHTML` |
| Promotion history pagination | `click` | GET `/api/v1/group/{group_id}/adm/waitlist/promotions/?page={n}` | `#promotion-history-wrapper` | `innerHTML` |
| Waitlist by branch chart load | `load` | GET `/api/v1/group/{group_id}/adm/waitlist/by-branch/` | `#waitlist-branch-chart-data` | `innerHTML` |
| Chart bar click (filter table) | `click` | GET `/api/v1/group/{group_id}/adm/waitlist/?branch={id}&stream={id}` | `#waitlist-table-body` | `innerHTML` |
| Notification template select | `change` | GET `/api/v1/group/{group_id}/adm/waitlist/notification-templates/{id}/` | `#notification-message-body` | `innerHTML` |
| Bulk notify send | `click` | POST `/api/v1/group/{group_id}/adm/waitlist/bulk-notify/` | `#bulk-notify-status` | `innerHTML` |
| Single-student notify | `click from:.btn-notify-single` | POST `.../waitlist/{id}/notify/` | `#toast-container` | `afterbegin` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
