# 05 — Group IT Support Executive Dashboard

- **URL:** `/group/it/support/executive/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Support Executive (Role 57, G3)

---

## 1. Purpose

The Group IT Support Executive Dashboard is the primary work interface for the IT Support Executive — the person responsible for providing technical support to all branch staff using EduForge. This is a personal task-queue page, not an aggregate overview. It shows only tickets assigned to the logged-in Support Executive, prioritised by SLA urgency.

Unlike the Director and Admin dashboards that survey the whole group, this page is intentionally focused and actionable. Every item on screen requires the Support Executive to do something: respond to a ticket, resolve an issue, escalate a problem they cannot fix, or schedule a remote support session with a branch staff member.

The page is designed around the concept of SLA discipline. Every support ticket has a first-response SLA and a resolution SLA based on priority tier. P1 tickets (Portal Down or Login Completely Broken) have a 2-hour first-response SLA; P2 tickets have 8 hours; P3 tickets have 24 hours. The KPI bar makes the SLA health immediately visible at a glance — if the "Overdue (SLA Breached)" card is non-zero, the Support Executive knows they have a problem before they even look at the ticket list.

The ticket system does not use any external ticketing platform. All tickets are stored in and served from PostgreSQL. Branch staff create tickets through their branch portal's support form, which routes to the group IT support queue. The Support Executive can view full conversation threads, update ticket status, add internal notes (visible only to IT team), schedule remote support sessions, and escalate to IT Admin or IT Director when a ticket requires config-level intervention.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Support Executive | G3 | Full access to own assigned tickets; view/resolve/escalate | Primary role |
| Group IT Admin | G4 | Full read + reassign tickets | Can reassign tickets between support executives |
| Group IT Director | G4 | Read-only overview | Sees all tickets but does not action them directly |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → IT Support → My Queue
```

### 3.2 Page Header
- **Title:** `My Support Queue`
- **Subtitle:** `IT Support Executive — [Name] · [Tickets Assigned to Me] open tickets · SLA performance: [Avg First Response Time] hrs avg`
- **Role Badge:** `Group IT Support Executive`
- **Right-side controls:** `View All Tickets (IT Admin View)` (visible only if G4 admin is viewing) · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any P1 ticket assigned > 1 hour without first response | "P1 ticket #[N] has not received a first response in [X] hours. Respond immediately." | Red (non-dismissible) |
| Any ticket SLA breached | "[N] ticket(s) have breached their SLA. Immediate attention required." | Red |
| Remote session requested and not scheduled within 4 hours | "Remote session requested by [Branch] has not been scheduled. Please confirm." | Amber |
| Ticket queue > 20 assigned tickets | "Your queue has [N] open tickets. Consider requesting re-assignment assistance from IT Admin." | Amber |

**Alert Notification Rules:**
- P1 ticket without first response > 1h: Assigned Support Executive (in-app red non-dismissible + email)
- SLA breached tickets: Support Executive (in-app red) + IT Admin (email cc IT Director)
- Queue > 20 tickets: Support Executive (in-app amber) + IT Admin (email)

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Tickets Assigned to Me | Total open tickets assigned to the logged-in Support Executive | Blue (informational) | Scrolls to main table |
| Overdue (SLA Breached) | Tickets where first-response or resolution SLA has been missed | Green = 0, Amber 1–2, Red ≥ 3 | Filters table to overdue tickets |
| Resolved Today | Count of tickets closed by this Executive since 00:00 today | Blue (informational) | Filters table to today's resolved |
| Avg First Response Time (hrs) | Rolling 7-day average first response time in hours for this Executive | Green < 2hrs, Amber 2–4hrs, Red > 4hrs | No drill-down — informational |
| Pending Remote Session Requests | Count of tickets where branch has requested a remote support session not yet confirmed | Green = 0, Amber 1–2, Red ≥ 3 | Filters table to remote session pending |

---

## 5. Main Table — My Ticket Queue

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Ticket # | Text link (e.g., TKT-2024-0431) | Yes | No |
| Branch | Text (branch name) | Yes | Yes (multi-select) |
| Reporter Name | Text (name of branch staff who raised the ticket) | No | No |
| Category | Badge: Portal / Login / Feature / Integration / Other | No | Yes (checkbox group) |
| Priority | Badge: P1 (red) / P2 (amber) / P3 (blue) | Yes | Yes (checkbox group) |
| Status | Badge: Open / In Progress / Awaiting Reply / Resolved / Escalated | Yes | Yes (checkbox group) |
| Opened At | Datetime | Yes | Yes (date range) |
| SLA Due | Datetime with colour: Green (on time) / Amber (< 1hr remaining) / Red (breached) | Yes | Yes (overdue filter) |
| Actions | `View` · `Resolve` · `Escalate` · `Remote Session` icon buttons | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All branches in the group |
| Priority | Checkbox group | P1 / P2 / P3 |
| Category | Checkbox group | Portal / Login / Feature / Integration / Other |
| Status | Checkbox group | Open / In Progress / Awaiting Reply / Resolved / Escalated |
| SLA Status | Checkbox | Overdue / On Track |
| Opened Date | Date range picker | From / To |

### 5.2 Search
- Full-text: Ticket number, branch name, reporter name
- 300ms debounce, triggers HTMX GET with `?search=` query param

### 5.3 Pagination
- Server-side · 25 rows/page (slightly higher for an operational queue) · Shows total count
- Default sort: SLA Due ascending (most urgent first)

---

## 6. Drawers

### 6.1 Drawer: `support-ticket-detail` — Ticket Detail
- **Trigger:** Actions → View or click Ticket # link
- **Width:** 480px
- **Sections within drawer:**
  - **Header:** Ticket #, branch, reporter name, category badge, priority badge, status badge, opened at, SLA due
  - **Conversation Thread:** Scrollable list of all messages between reporter and support team, with timestamps and sender labels ("Branch Staff" / "IT Support"). Most recent at top.
  - **Add Response:** Textarea for new response message to reporter + Send Reply button (POST). Optionally mark as "Internal Note" (checkbox) — internal notes are not shown to the branch reporter.
  - **Status Update:** Status dropdown (Open / In Progress / Awaiting Reply / Resolved / Escalated) + Update Status button
  - **Remote Session:** "Schedule Remote Session" button — opens a sub-panel with date/time picker and a link-share field for the session tool (Google Meet / Zoom link — manual entry)
  - **Escalate:** Opens a confirmation section — Escalate To (IT Admin / IT Director), reason for escalation (textarea), Submit Escalation button

**Validation:** Reply (required if type = Reply; max 2000 chars). Internal note (max 1000 chars). Remote session date must be future date, business hours (08:00–18:00 branch timezone). Remote session link must be valid HTTPS URL if provided.

**Audit:** All ticket actions (replies, status updates, resolutions, escalations) are logged to IT Audit Log with Support Executive user ID and timestamp. Internal notes are logged separately.

### 6.2 Drawer: `support-resolve-confirm` — Resolve Ticket (Confirm Modal)
- **Trigger:** Actions → Resolve
- **Width:** 400px (narrower confirmation modal)
- **Content:** Ticket summary, resolution notes textarea (required — must describe what was done), Resolution Category (dropdown: Issue Fixed / User Trained / Config Change Needed / Known Bug — Escalated / Cannot Reproduce), Confirm Resolve button
- **On confirm:** Ticket status set to Resolved, resolution timestamp logged, reporter is notified by platform notification that their ticket has been closed

---

## 7. Charts

No charts on this page. This is an operational task-queue page where every pixel of screen space is devoted to the ticket list and actionable controls. Adding charts would distract from the core workflow. Aggregate support metrics are available on the IT Director Dashboard.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reply sent | "Reply sent to [Reporter Name] at [Branch]." | Success | 3s |
| Ticket resolved | "Ticket #[N] marked as resolved. Reporter notified." | Success | 4s |
| Ticket escalated | "Ticket #[N] escalated to [IT Admin / IT Director]." | Info | 4s |
| Remote session scheduled | "Remote session confirmed. Link shared with reporter." | Success | 4s |
| Status updated | "Ticket status updated to [Status]." | Success | 3s |
| Action error | "Failed to update ticket. Please try again." | Error | 6s |
| Escalation failed | Error: `Failed to escalate ticket. Please try again.` | Error | 5s |
| Status update failed | Error: `Failed to update ticket status. Please try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No tickets assigned | "Your Queue is Clear" | "No support tickets are currently assigned to you. Check back later or contact IT Admin if you expect assignments." | — |
| Resolved Today = 0 (end of day) | "No Resolutions Yet Today" | "You have not resolved any tickets today." | View Open Tickets |
| Search / filter returns no results | "No Tickets Match" | "No tickets match your search or filter criteria. Try adjusting your filters." | Clear Filters |
| No remote session requests pending | "No Pending Sessions" | "No remote support sessions are awaiting confirmation." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer (5 cards) + table skeleton (10 rows, taller row height) |
| Ticket detail drawer open | Drawer-scoped spinner while conversation thread loads |
| Send reply | Send button spinner + textarea disabled until response |
| Resolve confirmation | Confirm button spinner + disabled state |
| Escalation submit | Submit button spinner + form fields disabled |
| Table filter/search | Table area overlay shimmer |

---

## 11. Role-Based UI Visibility

| Element | IT Support Executive (G3) | IT Admin (G4) | IT Director (G4) |
|---|---|---|---|
| KPI Summary Bar | All 5 cards (own tickets only) | All 5 cards (all executives aggregated) | All 5 cards (read-only, all executives) |
| Ticket Queue Table | Own assigned tickets | All tickets (all executives) | All tickets (read-only) |
| Reply / Resolve / Escalate Actions | Visible + functional | Visible + functional | Read-only (no action buttons) |
| Remote Session Scheduling | Visible + functional | Visible + functional | Hidden |
| Internal Note Checkbox | Visible | Visible | Visible (read-only) |
| Reassign Ticket Action | Hidden | Visible | Hidden |
| Alert Banners | Own SLA alerts | All SLA alerts (group-wide) | All alerts (read-only) |
| "View All Tickets" Header Link | Hidden | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/support/my-kpis/` | JWT (G3) | Returns 5 KPI card values for logged-in executive |
| GET | `/api/v1/it/support/my-tickets/` | JWT (G3) | Paginated ticket queue for logged-in executive |
| GET | `/api/v1/it/support/tickets/{id}/` | JWT (G3) | Full ticket detail including conversation thread |
| POST | `/api/v1/it/support/tickets/{id}/reply/` | JWT (G3) | Add reply or internal note to ticket |
| PATCH | `/api/v1/it/support/tickets/{id}/status/` | JWT (G3) | Update ticket status |
| POST | `/api/v1/it/support/tickets/{id}/resolve/` | JWT (G3) | Resolve ticket with resolution notes |
| POST | `/api/v1/it/support/tickets/{id}/escalate/` | JWT (G3) | Escalate ticket to IT Admin or IT Director |
| POST | `/api/v1/it/support/tickets/{id}/session/` | JWT (G3) | Log remote session details for a ticket |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/it/support/my-kpis/` | `#kpi-bar` | `innerHTML` |
| Load ticket queue | `load` | GET `/api/v1/it/support/my-tickets/` | `#ticket-table` | `innerHTML` |
| Open ticket detail drawer | `click` on Ticket # or View | GET `/api/v1/it/support/tickets/{id}/` | `#ticket-drawer` | `innerHTML` |
| Send reply | `click` on Send Reply | POST `/api/v1/it/support/tickets/{id}/reply/` | `#conversation-thread` | `innerHTML` |
| Update status | `change` on status dropdown | PATCH `/api/v1/it/support/tickets/{id}/status/` | `#ticket-status-badge` | `outerHTML` |
| Resolve ticket | `click` on Confirm Resolve | POST `/api/v1/it/support/tickets/{id}/resolve/` | `#ticket-row-{id}` | `outerHTML` |
| Escalate ticket | `click` on Submit Escalation | POST `/api/v1/it/support/tickets/{id}/escalate/` | `#escalate-result` | `innerHTML` |
| Filter ticket table | `change` on filter controls | GET `/api/v1/it/support/my-tickets/?priority=P1` | `#ticket-table` | `innerHTML` |
| Search tickets | `keyup[debounce:300ms]` on search | GET `/api/v1/it/support/my-tickets/?search=` | `#ticket-table` | `innerHTML` |
| Paginate table | `click` on page button | GET `/api/v1/it/support/my-tickets/?page=N` | `#ticket-table` | `innerHTML` |
| Refresh KPI after resolve | `htmx:afterRequest` on resolve POST | GET `/api/v1/it/support/my-kpis/` | `#kpi-bar` | `innerHTML` |

---

**Audit Trail:** All write operations on this page are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications:** Critical alerts on this page trigger in-app notifications to the relevant role owners as specified in the alert banner conditions above.

*Page spec version: 1.0 · Last updated: 2026-03-21*
