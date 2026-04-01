# Page 45: IT Support Ticket Manager

**URL:** `/group/it/support/tickets/`
**Roles:** Group IT Support Executive (Role 57, G3) — full CRUD; Group IT Admin (Role 54, G4) — full access; Group IT Director (Role 53, G4) — read + escalation
**Priority:** P0
**Division:** F — Group IT & Technology

---

## 1. Purpose

Central ticket management system for all EduForge technology support requests raised by branch staff across the group. Branch staff encounter issues with portal login, feature functionality, data discrepancies, integrations, and account access. These requests are received via the branch staff portal's help widget, WhatsApp, or direct email, and are logged here as tickets.

**Support SLA Policy:**
- **P1 (Critical):** First response within 1 hour; resolution within 4 hours. Examples: portal completely inaccessible for a branch, data loss, exam/admission day system failure.
- **P2 (High):** First response within 2 hours; resolution within 8 hours. Examples: login issues for multiple staff, fee collection system errors, report generation failure.
- **P3 (Normal):** First response within 4 hours; resolution within 48 hours. Examples: navigation confusion, minor display issues, request for guidance on features.

The IT Support Executive (Role 57, G3) manages day-to-day ticket work — viewing, updating, and resolving tickets. The IT Admin (Role 54, G4) oversees all tickets, can reassign, and handles escalated cases. The IT Director (Role 53, G4) can view all tickets and escalate critical issues to external support.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Support Executive (Role 57, G3) | Full CRUD | Create, view, assign to self, update, resolve tickets assigned to them |
| Group IT Admin (Role 54, G4) | Full access | All ticket operations, reassignment, escalation |
| Group IT Director (Role 53, G4) | Read + escalation | View all; can escalate; cannot edit ticket details |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > IT Support > Ticket Manager`

**Page Header:**
- Title: `IT Support Ticket Manager`
- Subtitle: `EduForge technology support tickets — all branches`
- Right side: `+ Create Ticket` button (Role 54/57), `Export (CSV)` button (Role 54)
- My Tickets toggle (Role 57): `Show My Tickets Only` — filters table to assigned_to = current user

**Alert Banners:**

1. **P1 Ticket Unassigned >1 Hour** (red, non-dismissible):
   - Condition: P1 ticket with status = New and created_at < now - 1 hour
   - Text: `P1 UNASSIGNED — Ticket [#] from [Branch] opened [X] hours ago with no assignee. Assign immediately.`

2. **SLA Breached** (red, non-dismissible while breached):
   - Condition: any ticket past its SLA due time and not resolved
   - Text: `[X] ticket(s) have breached SLA. [View SLA Dashboard →]`

3. **Branch Ticket Backlog** (amber, dismissible per session):
   - Condition: any single branch with > 10 open tickets
   - Text: `[Branch Name] has [X] open tickets — consider assigning additional support resources.`

---

## 4. KPI Summary Bar

Five KPI cards in a 5-column responsive grid.

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Open Tickets | Count with status in (New, Assigned, In Progress, Waiting Branch) | Number — colour coded: red if > 50 |
| 2 | SLA Breached | Count where sla_due_at < now and status not in (Resolved, Closed) | Number — always red if > 0 |
| 3 | Resolved Today | Count where resolved_at date = today | Number, green |
| 4 | Avg First Response Time (hrs) | Average time from created_at to first_response_at for tickets created today | Hours — amber if > 2h, red if > 4h |
| 5 | Branch Pending Count | Name of branch with most open tickets + count | `[Branch]: [X] open` — amber if X > 10 |

---

## 5. Main Table — Ticket Register

**Table Title:** `Support Tickets`

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Ticket # | Text | Auto-generated: `TKT-YYYY-NNNNN` |
| Branch | Text | Branch that raised the ticket |
| Reporter | Text | Name + role of the staff member who raised it |
| Category | Badge | Portal Login / Feature Issue / Data Issue / Integration / Performance / Account / Other |
| Priority | Badge | P1 (red) / P2 (orange) / P3 (grey) |
| Status | Badge | New (blue) / Assigned (cyan) / In Progress (amber) / Waiting Branch (purple) / Resolved (green) / Closed (grey) |
| Opened At | DateTime | Ticket creation timestamp |
| SLA Due | DateTime | Colour coded: green (on track) / amber (< 2h remaining) / red (breached) |
| Assigned To | Text | Support Executive name; `Unassigned` in red if not yet assigned |
| Actions | Buttons | `View` / `Assign` (Role 54/57) / `Resolve` (Role 54/57) / `Escalate` (Role 53/54) |

### Filters

- **Branch:** Multi-select dropdown
- **Category:** Multi-select
- **Priority:** All / P1 / P2 / P3
- **Status:** All / New / Assigned / In Progress / Waiting Branch / Resolved / Closed
- **Assigned To:** Dropdown of support executives
- **SLA Status:** All / On Track / At Risk (< 2h remaining) / Breached
- **Date Range:** Opened date from/to

### Search

Search on Ticket #, reporter name, or description keyword. `hx-trigger="keyup changed delay:400ms"`, targets `#ticket-table`.

### Pagination

Server-side, 25 rows per page. `hx-get="/group/it/support/tickets/table/?page=N"`, targets `#ticket-table`.

### Sorting

Sortable: Priority, Opened At, SLA Due, Status. Default sort: Priority ascending (P1 first), then SLA Due ascending (most urgent first).

---

## 6. Drawers

### A. Create Ticket Drawer (560px, right-side — Role 54/57)

Triggered by `+ Create Ticket` button.

**Drawer Header:** `Create Support Ticket`

**Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Branch | Dropdown | Yes | Branch raising the ticket |
| Reporter Name | Text input | Yes | Name of staff member who reported the issue |
| Reporter Role | Dropdown | Yes | Staff role category |
| Reporter Contact | Text input | Yes | Phone/WhatsApp number for follow-up |
| Category | Dropdown | Yes | Portal Login / Feature Issue / Data Issue / Integration / Performance / Account / Other |
| Priority | Dropdown | Yes | P1 / P2 / P3 (with SLA guidance shown) |
| Subject | Text input | Yes | Brief issue title |
| Description | Textarea | Yes | Full description of the issue |
| Steps to Reproduce | Textarea | No | For feature/data issues |
| Attachments | File upload | No | Screenshots or error logs; upload to Cloudflare R2 (max 3 files, 10MB each) |
| Assign To | Dropdown | No | Assign immediately to a support executive |

**Footer:** `Create Ticket` / `Cancel`

On submit: `hx-post="/api/v1/it/support/tickets/"`. SLA clock starts. If P1 and unassigned, alert banner triggers. Toast: `Ticket [TKT-YYYY-NNNNN] created. SLA due: [datetime].`

---

### B. View / Update Ticket Drawer (720px, right-side — all roles)

Triggered by `View` button. Role 57 can update tickets assigned to them; Role 54 can update any ticket; Role 53 is read-only.

**Drawer Header:** `[Ticket #] — [Subject]`

**Header badges:** Priority, Status, Category, SLA status indicator

**Tabs:**

**Tab 1: Ticket Details (read section)**
- Branch, Reporter, Contact
- Category, Priority, Opened At, SLA Due
- Assigned To (with `Reassign` button for Role 54/57)
- Description (rendered)
- Attachments (downloadable — links to R2 signed URLs)

**Tab 2: Conversation Thread**
- Chronological log of all updates, messages, and status changes
- Each entry: timestamp, actor (role + name), update type, content
- New update input (for Role 54/57): textarea + status dropdown + `Add Update` button
- Can set status to: In Progress / Waiting Branch / Resolved
- Upload additional attachments to thread

**Tab 3: Resolution**
- Visible when status = Resolved or being resolved
- Resolution Summary (required when resolving): textarea
- Root Cause (optional): dropdown — User Error / Config Issue / Platform Bug / Integration Issue / Network / Training Gap / Other
- Time Spent (minutes): numeric input
- Satisfaction Rating: displayed if the reporter has submitted one (1–5 stars)

**Footer:** `Close` | `Resolve` (Role 54/57, if not yet resolved) | `Escalate` (Role 53/54)

---

### C. Escalate Ticket Drawer (440px — Role 53/54)

Triggered by `Escalate` button.

**Fields:**
- Escalate To: Group IT Director (if current handler is Support Exec) / External Vendor Support / EduForge Platform Support
- Escalation Reason (textarea, required)
- Priority Override: Upgrade to P1 (optional toggle)
- Notify Reporter via: WhatsApp / Email

**Footer:** `Escalate` / `Cancel`

On submit: status set to `In Progress`, assigned changed to escalation target. Toast: `Ticket [#] escalated to [target]. Reporter notified.`

---

### D. Assign Ticket Drawer (440px — Role 54/57)

Triggered by `Assign` button for unassigned tickets.

**Fields:**
- Assign To: Dropdown of support executives (shows each executive's current open ticket count)
- Assignment Note (optional textarea)

**Footer:** `Assign Ticket` / `Cancel`

On submit: status → Assigned, assigned_to updated. Toast: `Ticket [#] assigned to [Name].`

---

### E. Close Ticket — Resolved → Closed Lifecycle

**Automatic closure:** Tickets with status = Resolved are automatically moved to Closed after 7 days if no re-open request is received. An auto-close warning is sent to the reporter via WhatsApp on Day 5: "Your ticket [#] will be automatically closed in 2 days unless you re-open it."

**Manual closure (Role 54 only):** The IT Admin can manually close a resolved ticket at any time via the View/Update drawer footer: `Close Ticket` button (visible only when status = Resolved).
- **Confirmation modal (380px):** "Close ticket [#]? Once closed, the ticket cannot be re-opened. A satisfaction survey will be sent to the reporter."
- On confirm: status → Closed; satisfaction survey sent via WhatsApp to reporter (1–5 star rating + optional comment).

**Re-open (before auto-close):** Reporter can re-open within 7-day window by responding to the WhatsApp notification. This sets status back to In Progress and notifies the assigned executive. Re-open count is tracked (displayed in ticket detail).

**Closed ticket visibility:** Closed tickets appear in the table with a "Closed" grey badge. They are included in filter results when Status = Closed is selected. Closed tickets are read-only — no updates or re-opens possible.

**API endpoint:** `POST /api/v1/it/support/tickets/{id}/close/` — JWT (G4 for manual; system for auto-close).

---

## 7. Charts

No dedicated chart section on this operational tickets page. Charts are on the SLA Dashboard (Page 46). A mini summary strip below the KPI bar shows:

**Today's Ticket Volume by Category (horizontal mini-bar):**
- Shows ticket count by category for today
- Read-only, inline, no interaction

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Ticket created | Success: `Ticket [TKT-#] created. SLA due: [datetime].` |
| P1 ticket created | System alert: `P1 CRITICAL ticket created. Assign immediately — SLA: 4 hours.` |
| Ticket updated | Success: `Ticket [#] updated. Thread entry added.` |
| Ticket resolved | Success: `Ticket [#] resolved. Resolution logged.` |
| Ticket assigned | Success: `Ticket [#] assigned to [Name].` |
| Ticket escalated | Success: `Ticket [#] escalated to [target].` |
| Ticket closed (manual) | Info: `Ticket [#] closed. Satisfaction survey sent to reporter.` |
| Ticket auto-closed | Info: `Ticket [#] automatically closed after 7 days.` |
| Ticket re-opened | Warning: `Ticket [#] re-opened by reporter. Assigned executive notified.` |
| Attachment uploaded | Info: `Attachment uploaded.` |
| Export complete | Info: `Ticket export ready.` |
| Validation error | Error: `Please complete all required fields.` |
| File too large | Error: `File exceeds 10MB limit. Please compress and re-upload.` |
| Ticket creation failed | Error: `Failed to create ticket. Please check your connection and try again.` | Error | 5s |
| Escalation failed | Error: `Failed to escalate ticket. Please try again.` | Error | 5s |
| Assignment failed | Error: `Failed to assign ticket. Please try again.` | Error | 5s |
| Attachment upload failed | Error: `Attachment upload failed. File may be too large or connection lost.` | Error | 5s |

---

**Audit Trail:** All ticket lifecycle actions (create, reply, status change, escalate, assign, close, re-open) are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications for Critical Events:**
- P1 ticket open > 1h without first response: Assigned Support Executive (in-app red + email)
- SLA breached: Support Executive (in-app red) + IT Admin (email cc IT Director)
- Ticket auto-closed after 7 days resolved: Reporter notified via email

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No tickets yet | Icon + `No support tickets raised yet. Tickets appear here when branch staff report issues.` |
| No tickets match filters | `No tickets match the selected filters. Try adjusting priority or date range.` |
| My Tickets filter active with no tickets | `You have no tickets assigned. Check "All Tickets" view for unassigned tickets.` |
| No open tickets | Green banner: `No open tickets. All support requests have been resolved.` |
| Conversation thread empty | `No updates yet. Add the first update using the conversation thread.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 5 skeleton shimmer cards |
| Ticket table | 6 skeleton rows |
| Ticket detail drawer | Spinner then tab content renders |
| Conversation thread | Skeleton message bubbles (3 placeholders) |
| Attachment upload | Progress bar during upload to R2 |
| Create/update buttons | `Saving...` + disabled during request |
| Assign dropdown | Spinner while loading executive list with open counts |

---

## 11. Role-Based UI Visibility

| UI Element | Role 57 (G3) | Role 54 (G4) | Role 53 (G4) |
|------------|-------------|-------------|-------------|
| Create Ticket button | Visible | Visible | Hidden |
| My Tickets toggle | Visible | Visible (optional) | Not shown |
| Assign button | Visible (reassign own) | Visible (any) | Hidden |
| Update thread | Visible (own tickets) | Visible (any) | Hidden |
| Resolve button | Visible (own tickets) | Visible (any) | Hidden |
| Escalate button | Hidden | Visible | Visible |
| Export CSV | Hidden | Visible | Visible |
| Resolution tab | Visible | Visible | Visible (read-only) |
| Priority override (escalation) | Not applicable | Visible | Visible |

**Note:** Role 55 (DPO) and Role 56 (Cybersecurity Officer) have no access to this page (returns 403). All UI elements are hidden.

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/support/tickets/` | Fetch tickets (paginated, filtered) |
| POST | `/api/v1/it/support/tickets/` | Create ticket |
| GET | `/api/v1/it/support/tickets/{id}/` | Fetch ticket detail |
| PUT | `/api/v1/it/support/tickets/{id}/` | Update ticket header fields |
| POST | `/api/v1/it/support/tickets/{id}/updates/` | Add conversation thread entry |
| POST | `/api/v1/it/support/tickets/{id}/assign/` | Assign ticket |
| POST | `/api/v1/it/support/tickets/{id}/resolve/` | Mark resolved |
| POST | `/api/v1/it/support/tickets/{id}/escalate/` | Escalate ticket |
| POST | `/api/v1/it/support/tickets/{id}/close/` | Manually close a resolved ticket (G4) or auto-close (system) |
| POST | `/api/v1/it/support/tickets/{id}/reopen/` | Re-open a resolved ticket (within 7-day window) |
| POST | `/api/v1/it/support/tickets/{id}/attachments/` | Upload attachment to R2 |
| GET | `/api/v1/it/support/tickets/kpis/` | Fetch KPI values |
| GET | `/api/v1/it/support/tickets/today-summary/` | Today's category breakdown mini-bar |
| GET | `/api/v1/it/support/tickets/export/csv/` | Export tickets |

---

## 13. HTMX Patterns

```html
<!-- Ticket table with auto-refresh every 60s for live status -->
<div id="ticket-table"
     hx-get="/group/it/support/tickets/table/"
     hx-trigger="load, every 60s"
     hx-target="#ticket-table"
     hx-include="#ticket-filter-form">
</div>

<!-- My Tickets toggle -->
<input type="checkbox" name="my_tickets" id="my-tickets-toggle"
       hx-get="/group/it/support/tickets/table/"
       hx-trigger="change"
       hx-target="#ticket-table"
       hx-include="#ticket-filter-form" />

<!-- Create ticket drawer -->
<button hx-get="/group/it/support/tickets/create-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  + Create Ticket
</button>

<!-- Create submit -->
<form hx-post="/api/v1/it/support/tickets/"
      hx-target="#ticket-table"
      hx-swap="outerHTML"
      hx-encoding="multipart/form-data"
      hx-on::after-request="closeDrawer(); refreshKPIs()">
  <button type="submit">Create Ticket</button>
</form>

<!-- View ticket drawer -->
<button hx-get="/group/it/support/tickets/{{ ticket.id }}/detail/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  View
</button>

<!-- For any form that accepts file attachments, use hx-encoding="multipart/form-data" -->

<!-- Add thread update -->
<form hx-post="/api/v1/it/support/tickets/{{ ticket.id }}/updates/"
      hx-target="#thread-{{ ticket.id }}"
      hx-swap="beforeend"
      hx-encoding="multipart/form-data">
  <textarea name="content" placeholder="Add an update..."></textarea>
  <select name="new_status">...</select>
  <button type="submit">Add Update</button>
</form>

<!-- KPI auto-refresh -->
<div id="ticket-kpis"
     hx-get="/group/it/support/tickets/kpis/"
     hx-trigger="load, every 60s"
     hx-target="#ticket-kpis">
</div>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
