# I-04 — Institution Support Profile

**Route:** `GET /support/institutions/{institution_id}/`
**Method:** Django CBV (`DetailView`) + HTMX part-loads
**Primary roles:** Support Manager (#47), Onboarding Specialist (#51)
**Also sees (read):** L1 (#48), L2 (#49), L3 (#50), Support Quality Lead (#108)
**No access:** Training Coordinator (#52)

---

## Purpose

Per-institution view aggregating all support context: open tickets, full ticket history, onboarding status, contact directory, and institution metadata. Reduces time-to-context for agents handling tickets from repeat institutions. Linked from I-02 (institution column), I-03 (institution context panel), and I-05 (onboarding tracker).

At scale: some institutions (coaching centres with 10,000–15,000 students) will accumulate hundreds of tickets per year. This page must handle large history sets efficiently via server-side pagination.

---

## Data Sources

| Section | Source |
|---|---|
| Institution metadata | `institution` + `institution_subscription` (Division M) |
| Support KPIs | Aggregated from `support_ticket` WHERE `institution_id=` |
| Active tickets table | `support_ticket` WHERE `institution_id=` AND status NOT IN (RESOLVED, CLOSED) |
| Ticket history | `support_ticket` WHERE `institution_id=`; paginated; sorted by `created_at` desc |
| Onboarding status | `onboarding_instance` WHERE `institution_id=` |
| Contact directory | `institution_contact` (institution-level contact records) |
| Institution notes | `institution_support_note` (support-team-only notes about this institution) |

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `?tab` | `active`, `history`, `onboarding`, `contacts` | Opens specific tab; default `active` |
| `?status` | Any ticket status | Pre-filters history tab |
| `?category` | Any category | Pre-filters history tab |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| KPI strip | `?part=kpi` | Page load |
| Subscription badge | `?part=subscription` | Page load; `?part=subscription&nocache=true` on [↻ Refresh] click (Support Manager only) |
| Active tickets | `?part=active_tickets` | Tab switch to active |
| Ticket history table | `?part=history&page={n}` | Tab switch + pagination |
| Onboarding panel | `?part=onboarding` | Tab switch to onboarding |
| Contacts panel | `?part=contacts` | Tab switch to contacts |
| Institution notes | `?part=notes` | Page load; after [+ Add Note] POST completes (HTMX swap refreshes the notes section in-place) |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────┐
│  ← Back   INSTITUTION HEADER                                 │
├──────────────────────────────────────────────────────────────┤
│  KPI STRIP (4 tiles)                                         │
├──────────────────────────────────────────────────────────────┤
│  [Active Tickets] [Ticket History] [Onboarding] [Contacts]   │
├──────────────────────────────────────────────────────────────┤
│  TAB CONTENT (varies per tab)                                │
└──────────────────────────────────────────────────────────────┘
```

---

## Components

### Institution Header

```
┌──────────────────────────────────────────────────────────────┐
│  [Logo or initials avatar]  Sunrise Public School            │
│  Type: School  ·  Region: Hyderabad  ·  ID: INST-1042       │
│  Subscription: ACTIVE (expires 15 Mar 2025)                  │
│  Admin: Meena Reddy (m.reddy@sunrise.edu.in)                 │
│                          [Add Note]  [Create Ticket for Inst]│
└──────────────────────────────────────────────────────────────┘
```

Logo display: if institution has a logo uploaded (from institution portal), show 48×48px thumbnail. If no logo: show a square avatar with the institution name initials (e.g., "SP" for Sunrise Public School) on a colour derived from the institution ID hash (consistent colour per institution).

Subscription status badge:
- ACTIVE → green
- TRIAL → blue
- EXPIRED → red
- SUSPENDED → red + "Billing issue" tooltip

**Near-expiry warning**: If `subscription_expires_at` is within 30 days and status is ACTIVE, show an amber inline label: "⚠ Expires in N days" directly after the expiry date. At ≤7 days: red bold "⚠ Expires in N days — renewal required".

**Subscription data freshness**: Subscription data is fetched from Division M (read-only, 30-min Memcached TTL). The subscription line in the header is wrapped in a dedicated `<div id="subscription-badge">` HTMX target (separate from the rest of the static header). A small [↻ Refresh] link appears next to the subscription badge (Support Manager only); clicking triggers `hx-get="?part=subscription&nocache=true"` targeting only `#subscription-badge` — does NOT reload the full header. If Division M is unreachable, subscription section shows "Status unavailable — data may be stale" (amber) regardless of cached value.

[Create Ticket for Inst] opens the New Ticket drawer (from I-02) pre-filled with this institution.

If institution has a flag note (from `institution_support_note` with `is_pinned=true`): shown as a yellow banner below the header.

---

### KPI Strip

| Tile | Value | Notes |
|---|---|---|
| Open Tickets | COUNT status NOT IN (RESOLVED, CLOSED) | Links to active tab |
| Total Tickets | COUNT all time | — |
| Avg Resolution Time | AVG (resolved_at - created_at - sla_pause_duration) for RESOLVED/CLOSED tickets | Last 90 days |
| CSAT Score | AVG csat_score for this institution | Last 90 days; "No data" if <5 responses |

---

### Tab 1 — Active Tickets

Table of all open/in-progress/pending/escalated tickets for this institution.

Columns: Ticket # | Priority | Category | Subject | Status | Tier | Assigned To | SLA | Last Reply

Same SLA colour coding as I-02.

If 0 active tickets: "No open tickets for this institution." green empty state.

Row click: opens I-03.

---

### Tab 2 — Ticket History

Full paginated ticket history (25 per page, sorted by `created_at` desc).

**Filter row above table:**
- Status: multi-checkbox
- Category: multi-checkbox
- Priority: multi-checkbox
- Date range picker
- [Apply] [Clear]

Columns: Ticket # | Category | Subject | Priority | Status | Tier | Assigned To | Created | Resolved/Closed | CSAT

Closed/Resolved rows: faded (70% opacity) but fully clickable.

CSAT column: star rating (1–5); blank if not submitted; grey dash if ticket not yet closed.

[Export History] button (Support Manager only): downloads CSV of all tickets for this institution (PII included — flagged in audit log). Requires confirmation: "This export includes requester contact details. It will be logged to the audit trail. Proceed?"

---

### Tab 3 — Onboarding

Shown if `onboarding_instance` exists for this institution; otherwise shows "This institution has no onboarding record." with [Create Onboarding Record] button (Support Manager + Onboarding Specialist only).

If record exists:

```
┌──────────────────────────────────────────────────────────────┐
│  Onboarding Status: ADMIN_TRAINED                            │
│  Specialist: Arun Nair · Started: 12 Oct 2024               │
│  Target go-live: 20 Nov 2024 (15 days away)                 │
│  [View Full Onboarding Tracker →]                           │
├──────────────────────────────────────────────────────────────┤
│  STAGE PROGRESS                                              │
│  ✓ INITIATED → ✓ SETUP_CALL → ✓ PORTAL_CONFIGURED →        │
│  ✓ ADMIN_TRAINED → ○ FIRST_EXAM → ○ LIVE → ○ COMPLETED     │
├──────────────────────────────────────────────────────────────┤
│  CURRENT STAGE CHECKLIST (ADMIN_TRAINED)                    │
│  ✓ Portal walkthrough completed                             │
│  ✓ Exam creation demo done                                  │
│  ○ Student management explained  ← incomplete               │
│  ○ Results workflow explained   ← incomplete                │
│                                [View in Tracker →]          │
├──────────────────────────────────────────────────────────────┤
│  UPCOMING TRAINING SESSIONS                                  │
│  · 15 Nov · Results Workflow Walkthrough · Arun Nair        │
│  [Schedule Training →]                                      │
└──────────────────────────────────────────────────────────────┘
```

[View Full Onboarding Tracker →] links to I-05 filtered to this institution.
[Schedule Training →] opens the training session modal (same as I-05).

If onboarding is STALLED: red banner "⚠ Onboarding stalled since 3 Nov 2024 (12 days). No checklist activity detected."

---

### Tab 4 — Contacts

Directory of institution contacts stored for support purposes.

**Contact card:**
```
Meena Reddy
Role: Institution Admin · Primary contact
Email: m.reddy@sunrise.edu.in
Phone: +91-98765-43210
Preferred contact: Email
Last contacted: 5 Nov 2024
```

Actions per contact (Support Manager + Onboarding Specialist):
- [Edit] → inline edit fields; fields become editable in-place; [Save] / [Cancel] buttons appear
- [Delete] → confirmation modal "Delete this contact permanently? This cannot be undone." → hard-delete from `institution_contact`; row removed via HTMX swap; audit log entry created

[+ Add Contact] button → adds a new contact card with fields: Name, Role, Email, Phone, Preferred contact (Email/Phone/WhatsApp), Notes.

Contact data stored in `institution_contact` table (separate from institution admin accounts — this is the support team's operational directory, may include finance contacts, IT contacts, etc.).

---

### Institution Support Notes

Below the tabs (always visible, not tabbed):

```
Internal Notes (Support Team Only)
─────────────────────────────────
📌 [PINNED] This institution has a slow IT setup — always allow extra time for portal config tasks. (Added by Arun Nair · 12 Oct 2024)

⚠ Billing sensitive — institution admin gets upset about payment queries. Route billing tickets to Senior L1 only. (Added by Support Manager · 3 Nov 2024)

[+ Add Note]
```

Note types: PINNED (always shown at top with push-pin icon), WARNING (orange ⚠), INFO (grey).

[+ Add Note] → inline text field + type selector + [Save]. No character limit. Notes are internal-only (not visible to institution).

Visible to: all support staff (L1, L2, L3, Support Manager, Quality Lead, Onboarding Specialist). Hidden from institution admins.

---

## Edge Cases

1. **Institution with 0 tickets**: KPI strip shows all zeros; Active Tickets tab shows empty state; History tab shows empty state with "No support history for this institution."
2. **New institution (not yet active)**: Subscription badge shows TRIAL; onboarding tab likely in early stage.
3. **Institution with expired subscription**: Red "EXPIRED" badge in header; tooltip "Subscription expired on {date}. Billing queries should route to Division M."
4. **Coaching centre with thousands of tickets**: History tab server-side pagination handles scale; default 25 per page with max 100 option.
5. **Multiple pinned notes**: Shown in reverse chronological order; all pinned notes shown before non-pinned.
6. **Onboarding record exists but stage=COMPLETED**: Onboarding tab shows completed status in green; no active checklist. Shows `actual_go_live_at` and `completed_at` timestamps.
6a. **Multiple onboarding instances (re-onboarding)**: When an institution has more than one `onboarding_instance` (original + re-onboarding), Tab 3 shows **the most recent instance** ordered by `started_at DESC`. If the most recent instance is COMPLETED, it shows the COMPLETED view; if there's a newer ACTIVE re-onboarding instance in progress, that takes precedence. A "(Re-onboarding N)" badge is appended to the stage header. A "View previous onboarding →" link at the bottom links to I-05 filtered to all instances for this institution.
7. **Support Quality Lead access**: Can read all tabs and notes; cannot create tickets, add contacts, or add notes. [Add Note] and [Create Ticket for Inst] buttons hidden.
8. **L1 agent access**: Can read all tabs. Cannot export ticket history, add contacts, or create institution notes. [Export History] and [Add Note] hidden.

---

## Notifications

No page-level notifications. Actions on this page (ticket creation, note addition) generate standard ticket notifications in I-03.
