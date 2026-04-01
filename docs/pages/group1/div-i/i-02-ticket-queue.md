# I-02 — Ticket Queue

**Route:** `GET /support/tickets/`
**Method:** Django CBV (`ListView`) + HTMX part-loads
**Primary roles:** L1 (#48), L2 (#49), L3 (#50), Support Manager (#47)
**Also sees (read-only):** Support Quality Lead (#108) — no ticket actions

---

## Purpose

The primary worklist for all support agents. Displays assigned and unassigned tickets filtered by the agent's tier. SLA countdown timers are live. Support Manager sees all queues simultaneously. L1/L2/L3 agents see only their tier's queue.

At scale, this page must handle 5,700+ tickets/month (normal) and 25,000+ during exam-day surges while maintaining sub-second filter response.

---

## Data Sources

- `support_ticket` with JOINs on `institution`, `user` (assigned_to, created_by)
- Server-side pagination: 25 rows default; 50/100 options
- **No caching** — SLA timers require fresh data; tickets update constantly

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `?status` | `OPEN`, `IN_PROGRESS`, `PENDING_CUSTOMER`, `ESCALATED`, `RESOLVED`, `CLOSED` (comma-sep) | Filter by status |
| `?priority` | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` (comma-sep) | Filter by priority |
| `?tier` | `L1`, `L2`, `L3` | Filter by tier; Support Manager and Support Quality Lead (#108) only (both see all tiers read-only) |
| `?category` | Any `support_ticket.category` value | Filter by category |
| `?assigned` | `me`, `unassigned`, or user_id | Filter by assignee |
| `?institution_id` | integer | Filter by institution |
| `?institution_type` | `SCHOOL`, `COLLEGE`, `COACHING`, `GROUP` | Filter by institution type |
| `?exam_day` | `true` | Show only exam-day incident tickets |
| `?sla_status` | `AT_RISK`, `BREACHED`, `OK` | Filter by SLA health |
| `?q` | text | Full-text search on subject and ticket_number |
| `?created_after` | `YYYY-MM-DD` | Date range filter |
| `?created_before` | `YYYY-MM-DD` | Date range filter |
| `?sort` | `sla_asc`, `created_desc`, `priority_desc`, `updated_desc` | Sort order; default `sla_asc` |
| `?quality_audit_pending` | `true` | Show only tickets where `quality_audit_score IS NULL AND status IN ('RESOLVED','CLOSED') AND resolved_at >= now() - interval '14 days'`; used by I-01 [Start Auditing →] link; Support Quality Lead and Support Manager only |
| `?page` | integer | Pagination offset |
| `?per_page` | `25`, `50`, `100` | Rows per page |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| Ticket table rows | `?part=table` | Page load, filter change, pagination click |
| Stats bar | `?part=stats` | Page load; auto-refresh every 60s |
| Active filter pills | `?part=filter_pills` | Filter apply |
| Quick Reply inline form | `?part=quick_reply&ticket_id={id}` | [Quick Reply] row button click; loads 200-char textarea inline within the row; HTMX swap target = row reply area |
| Inline priority update | `?part=row&ticket_id={id}` | [Change Priority ▼] dropdown change; refreshes the single row in-place (HTMX `hx-swap="outerHTML"` on the `<tr>`) |

---

## Page Layout

```
┌───────────────────────────────────────────────────────────────┐
│  Ticket Queue               [+ New Ticket]   [Bulk Actions ▼] │
├───────────────────────────────────────────────────────────────┤
│  STATS BAR: Open (142) | At Risk (8) | Breached (2) | Mine(31)│
├───────────────────────────────────────────────────────────────┤
│  SEARCH BAR + FILTER ROW                                      │
│  ACTIVE FILTER PILLS                                          │
├───────────────────────────────────────────────────────────────┤
│  TICKET TABLE                                                 │
├───────────────────────────────────────────────────────────────┤
│  PAGINATION                                                   │
└───────────────────────────────────────────────────────────────┘
```

---

## Components

### Stats Bar

Five inline stat chips above the table. Each is a clickable link that applies the corresponding filter.

| Chip | Query | Colour |
|---|---|---|
| Open | status=OPEN; tier scoped to current user's tier | Grey |
| At Risk | sla_breach_at BETWEEN now() AND now()+1h; open | Amber |
| Breached | sla_breach_at < now(); open | Red (pulsing if >0) |
| Mine | assigned_to_id = current user; open | Blue |
| Unassigned | assigned_to_id IS NULL; open; current user's tier | Orange |

Support Manager sees totals across all tiers. L1/L2/L3 see their tier only.

---

### Search Bar + Filter Row

**Search bar (full-width):** searches `ticket_number` (prefix match) and `subject` (icontains). Triggers HTMX table reload on input (300ms debounce).

**Quick filter chips (always visible):**
- [All] [Open] [In Progress] [Pending] [Escalated] [Resolved] — status quick-select
- [My Tickets] [Unassigned]
- [CRITICAL] [HIGH] — priority quick-select

**[Advanced Filters] button** → expands filter panel below:

| Filter | Type | Options |
|---|---|---|
| Status | Multi-checkbox | OPEN, IN_PROGRESS, PENDING_CUSTOMER, ESCALATED, RESOLVED, CLOSED |
| Priority | Multi-checkbox | CRITICAL, HIGH, MEDIUM, LOW |
| Category | Multi-checkbox | All 11 categories |
| Tier | Radio (Support Manager only) | All / L1 / L2 / L3 |
| Institution | Autocomplete search | Searches institution name |
| Institution type | Radio | All / School / College / Coaching / Group |
| Assigned to | Autocomplete search | Searches agent name |
| SLA status | Radio | All / OK / At Risk (< 1h) / Breached |
| Created date range | Date range picker | — |
| Exam day only | Checkbox | Filters `exam_day_incident=true` |
| Sort by | Dropdown | SLA (soonest first), Created (newest), Priority, Last updated |

[Apply Filters] button → HTMX reloads `?part=table`. [Clear All] resets to defaults.

Active filters shown as dismissible pills below the filter row.

---

### Ticket Table

**Columns:**

| Column | Content | Sortable |
|---|---|---|
| ☐ | Checkbox for bulk selection | — |
| # | `ticket_number` (e.g., SUP-20241105-000342); links to I-03 | — |
| Priority | Badge: CRITICAL (red), HIGH (orange), MEDIUM (blue), LOW (grey) | Yes |
| Category | Readable label (e.g., "Login Issue") | Yes |
| Subject | First 80 chars of subject; full text on hover tooltip | No |
| Institution | Institution name; links to I-04; truncated at 30 chars | Yes |
| Status | Colour-coded badge | Yes |
| Tier | L1/L2/L3 badge | Yes (Manager only) |
| SLA | Countdown timer or "Breached Xh ago" | Yes |
| Assigned | Avatar + name; "Unassigned" in orange if null | Yes |
| Last Reply | Relative time ("3 min ago") | Yes |
| Actions | Row-level action buttons (see below) | — |

**SLA column colouring:**
- `sla_breach_at > now() + 4h` → green text "Xh Ym left"
- `sla_breach_at BETWEEN now() + 1h AND now() + 4h` → amber text
- `sla_breach_at BETWEEN now() AND now() + 1h` → red bold text (pulsing)
- `sla_breach_at < now()` → red background "Breached Xh Ym ago"

**PENDING_CUSTOMER rows:** SLA paused; shown with grey italic text "SLA paused (awaiting customer)"

**Exam-day incident rows:** left border = red; EXAM DAY badge before ticket number.

**Row click:** opens I-03 (ticket detail) — full page navigation.

---

### Row-Level Actions

Shown on row hover; collapsed into [···] menu:

| Action | Who Sees It | Behaviour |
|---|---|---|
| [Assign to me] | Any agent when ticket unassigned or assigned to another | Sets `assigned_to_id`; HTMX row refresh. **Special case for ESCALATED tickets**: if ticket status is `ESCALATED`, [Assign to me] also transitions status to `IN_PROGRESS` (the agent is accepting the escalation — the ESCALATED state is exited). This matches the state machine: ESCALATED exits when the new-tier agent first acts. |
| [Quick Reply] | Assigned agent only | Opens inline reply drawer (200-char max; for simple acknowledgements only); full reply in I-03 |
| [Escalate] | Assigned agent when in their tier | Opens escalation modal; see Workflow 2 in pages-list |
| [Change Priority] | Support Manager only | Dropdown inline; no modal needed |
| [Close] | Support Manager; assigned agent when status=RESOLVED | Confirms close; CSAT auto-sent |
| [View →] | All | Links to I-03 |

---

### Bulk Actions

Checkbox selects rows. [Bulk Actions ▼] dropdown:

| Action | Who Can Use | Behaviour |
|---|---|---|
| Assign to … | Support Manager | Select agent from list; assigns all selected |
| Change Priority | Support Manager | Set priority for all selected |
| Change Tier | Support Manager | Move selected tickets to different tier queue |
| Close (resolved) | Support Manager | Mass-close; requires confirmation modal "Close {N} tickets?" |
| Export Selected | Support Manager, Support Quality Lead | Downloads CSV of selected tickets; **Support Manager**: full export including institution name, category, resolution time, CSAT (no student PII — emails masked); **Quality Lead**: exports ticket metadata only (ticket_number, category, tier, quality_score, resolution_time) — no requester fields at all; logged to audit trail |

All bulk actions are **audit-logged**: each affected ticket gets a SYSTEM message inserted into its thread: e.g., "Bulk assigned to Rahul Kumar by Priya (Support Manager) via bulk action on 5 Nov 2024 at 2:15 PM". This ensures every ticket has a complete history of who touched it and when.

Bulk action bar appears at the bottom of the screen as a fixed bar when ≥1 ticket selected:
```
[3 tickets selected]  [Assign to ▼]  [Change Priority ▼]  [Close Selected]  [Export]  [✕ Clear]
```

---

### [+ New Ticket] Button

**Access**: L1, L2, L3, Support Manager. Onboarding Specialist can create `ONBOARDING_HELP` category only. Training Coordinator and Support Quality Lead (#108) have no [+ New Ticket] button.

Opens a Create Ticket drawer (not modal — wider form needed):

**Step 1 — Requester lookup:**
- Institution search (autocomplete)
- "This is an internal ticket" checkbox (skips institution lookup)
- After institution selected: shows requester name + email fields

**Step 2 — Ticket details:**
- Subject (required, max 500 chars)
- Category (dropdown with all 11 values)
- Priority (dropdown; default MEDIUM; Support Manager can set CRITICAL)
- Tier (Support Manager only; auto-assigned for others)
- Linked exam (optional; autocomplete for exam name)
- Description (textarea, markdown supported)
- Attachments (drag-and-drop; max 10MB per file, 3 files total; stored in R2)

**Step 3 — Assignment:**
- [Assign to me] checkbox (default checked)
- Or: search for specific agent

[Create Ticket] button → POST `/support/tickets/create/`; shows spinner on button during submit (button disabled, text "Creating…"); on success: toast "Ticket SUP-YYYYMMDD-NNNNNN created ✓" (green, auto-dismiss 4s); drawer closes; table reloads via `?part=table`. On error: 400 → inline field errors under each invalid field; 429 → toast "Too many tickets from this institution. Please wait before submitting another." (amber, persists until dismissed); 500 → toast "Something went wrong. Please try again or contact Platform Admin." (red).

Validation:
- Subject: required
- Category: required
- Requester email: valid email format if provided
- Priority CRITICAL: confirmation modal "Creating a CRITICAL ticket. This will alert the full L1 team. Confirm?"

---

### Pagination

Server-side. Controls at bottom:
```
← Prev   [1] [2] [3] ... [47]   Next →      Showing 26–50 of 1,164    [25 ▼] per page
```

Page size selector: 25 / 50 / 100. Default 25.

---

## Empty States

| Scenario | Message |
|---|---|
| No tickets match filters | "No tickets match your filters. [Clear filters]" |
| All tickets resolved (current user's queue empty) | "All clear — no open tickets in your queue." with green checkmark icon |
| Unassigned queue empty | "No unassigned tickets. Queue is healthy." |
| Search returns no results | "No tickets found for '{query}'. Try a shorter search term or ticket number." |

---

## Edge Cases

1. **SLA timer precision**: Countdown shows `Xh Ym` for ≥1h remaining; shows `Xm Ys` for <1h remaining. Counts down client-side via JS; does not depend on HTMX refresh.
2. **PENDING_CUSTOMER ticket SLA**: SLA timer shows "Paused" with the total pause duration. Effective SLA = `sla_breach_at + sla_pause_duration_seconds`. Timer resumes on next customer reply.
3. **L1 agent tries to view L2 ticket URL directly**: Returns 403 with "This ticket is in the L2 queue. You don't have access." — does not silently show ticket.
4. **Exam day: >500 CRITICAL tickets open**: Table auto-applies `priority=CRITICAL&exam_day=true` filter with a banner "Exam day mode active. Showing critical tickets only. [Show all]". If surge threshold exceeded (>200 EXAM_DAY_INCIDENT open), Support Manager sees [Activate Triage Mode] button — see Workflow 1 in pages-list.
5. **Agent has 0 assigned tickets and no unassigned in their queue**: "No open tickets in your queue. [Check unassigned tickets →]" button links to `?assigned=unassigned&tier={agent_tier}`.
5a. **Sort order fallback for CLOSED/RESOLVED tickets**: when filtering by `?status=RESOLVED,CLOSED`, default sort switches from `sla_asc` to `created_desc` (CLOSED tickets have no SLA countdown). Applied automatically by server when all items in result set have `status IN ('RESOLVED','CLOSED')`. Sort header shows "Created (newest first)" as active sort indicator.
6. **Support Quality Lead (#108) row actions**: All row action buttons hidden; no create button shown. Only [View →] available.
7. **Ticket number search**: `?q=SUP-20241105` matches all tickets with that date prefix — useful for bulk exam-day lookup.
8. **Export while filters active**: Export applies current filter state; downloaded file name includes filter summary: `tickets_export_L1_CRITICAL_20241105.csv`.

---

## Notifications

- Assignment notification: when Support Manager assigns a ticket to an agent → F-06 push to agent: "Ticket #SUP-... assigned to you by {manager}"
- **Bulk assign notification**: each agent receiving tickets from a bulk-assign action gets one consolidated F-06 push: "{N} tickets assigned to you by {manager}" (not one push per ticket)
- Queue becomes empty: no notification (intentional — don't interrupt agent rest)
- Breached ticket assigned to agent: F-06 push on assignment ("⚠ Breached ticket assigned to you")
- **Role demotion**: if an agent is demoted to a role with no I-02 access (e.g., L1 → Training Coordinator), their existing ticket assignments are NOT auto-cleared. Platform Admin must manually re-assign orphaned tickets. Celery Task 6 (`alert_unassigned_queue`) does not surface these (they still have `assigned_to_id` set). Support Manager must periodically check for "assigned but inactive" agents via I-07 agent performance table (agents with 0 activity in the last 7 days while having open tickets).
