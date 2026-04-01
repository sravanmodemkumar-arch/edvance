# I-03 — Ticket Detail

**Route:** `GET /support/tickets/{id}/`
**Method:** Django CBV (`DetailView`) + HTMX part-loads
**Primary roles:** L1 (#48), L2 (#49), L3 (#50), Support Manager (#47)
**Also sees:** Support Quality Lead (#108) — read + quality annotation only; Onboarding Specialist (#51) — read only for `ONBOARDING_HELP` category tickets only; BGV Manager (#39) — read + reply for `BGV_QUERY` category tickets only (accessed via F-06 direct link; no other Division I pages accessible to BGV Manager)

---

## Purpose

Full ticket view with conversation thread, requester context, SLA tracker, escalation history, and all ticket actions. The primary workspace for resolving a ticket. Two-panel layout: left panel = conversation thread + reply box; right panel = ticket metadata, institution context, escalation history, KB suggestions.

---

## Data Sources

| Section | Source |
|---|---|
| Ticket metadata | `support_ticket` |
| Conversation thread | `support_ticket_message` ordered by `created_at` asc |
| Escalation history | `support_ticket_escalation` for this ticket |
| Institution context | `institution` + `onboarding_instance` (if exists) |
| KB suggestions | `kb_article` WHERE category matches ticket's `category`; `status=PUBLISHED` |
| Quality audit | `support_quality_audit` for this ticket (Quality Lead view) |
| Related tickets | `support_ticket` WHERE `institution_id=` same AND status NOT IN (CLOSED); limited to 5 |

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `?focus=reply` | — | Auto-focuses the reply textarea on load (from "Quick Reply" in I-02) |
| `?internal=true` | — | Pre-selects "Internal Note" tab in reply box |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| Thread messages | `?part=thread` | Page load; auto-refresh every 30s via `hx-trigger="every 30s"`; **suspended while reply textarea has focus** (implemented via `hx-trigger="every 30s [!document.activeElement.closest('.reply-form')]"` — HTMX conditional trigger); resumes immediately on textarea blur; `?part=thread&before={message_id}` for "Load earlier messages" — returns 50 messages chronologically BEFORE the given `message_id` (ascending order: oldest first within the batch, appended at TOP of thread); auto-scroll NOT triggered on earlier-message load (user stays at current scroll position) |
| SLA tracker | `?part=sla` | Page load; auto-refresh every 60s |
| Ticket metadata header | `?part=header` | After any status/priority/tier change, after [Link Exam] saves |
| KB suggestions | `?part=kb_suggestions` | Page load |
| Related tickets | `?part=related` | Page load |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  ← Back to Queue   SUP-20241105-000342   [CRITICAL] [L2] [ESCALATED] │
│  "Student cannot rejoin exam session after browser crash"             │
├──────────────────────────────────┬───────────────────────────────────┤
│                                  │  TICKET METADATA PANEL (right)    │
│  CONVERSATION THREAD (left)      │  SLA TRACKER                      │
│                                  │  INSTITUTION CONTEXT              │
│  [System] Ticket created         │  ESCALATION HISTORY               │
│  [Priya L1] Initial response     │  KB SUGGESTIONS                   │
│  [System] Escalated to L2        │  RELATED TICKETS                  │
│  [Rahul L2] Technical response   │  QUALITY AUDIT (Quality Lead only)│
│                                  │                                   │
│  REPLY BOX                       │                                   │
└──────────────────────────────────┴───────────────────────────────────┘
```

---

## Left Panel — Conversation Thread

### Thread Messages

Each message rendered in chronological order (oldest at top, newest at bottom). Auto-scroll to bottom on load.

**Reply message** (from support agent):
```
┌─────────────────────────────────────────────────┐
│  [Avatar] Rahul Kumar · L2 Support Engineer      │
│  Today, 2:34 PM                                  │
│                                                  │
│  Hi, I've investigated the session database.     │
│  The session token was invalidated after 20 min  │
│  of inactivity. Your student should be able to   │
│  rejoin using the original exam link.            │
│                                          [Edit]  │
└─────────────────────────────────────────────────┘
```

**Internal note** (only visible to support staff — not requester):
```
┌─────────────────────────────────────────────────┐
│  🔒 INTERNAL NOTE · Priya Sharma · L1            │
│  Today, 2:10 PM                                  │
│                                                  │
│  Session issue confirmed in logs. Escalating     │
│  because session table requires L2 DB read.      │
└─────────────────────────────────────────────────┘
```

Yellow background, lock icon, "not visible to requester" label.

**System message:**
```
  ── [System] Status changed: OPEN → IN_PROGRESS by Priya Sharma (2:10 PM) ──
  ── [System] Escalated to L2 by Priya Sharma (2:14 PM): "Technical investigation needed" ──
```

Grey italic, no avatar, centred.

**Quality annotation** (Support Quality Lead only):
```
┌──────────────────────────────────────────────────┐
│  ⭐ QUALITY ANNOTATION · Ananya (Quality Lead)   │
│  Today, 4:00 PM                                  │
│                                                  │
│  Good technical investigation. Tone appropriate. │
│  Suggest adding KB article for session timeout.  │
└──────────────────────────────────────────────────┘
```

Purple background. Visible to: Quality Lead and Support Manager always. **Also visible to the ticket's assigned agent** if `support_quality_audit.shared_with_agent=true` (the Quality Lead checked [Share with agent] when submitting). Agents who are NOT the assigned agent cannot see shared annotations.

---

### Reply Box

Tabbed interface below the thread:

**Tab 1: Reply (default)**
- Visible to requester: yes
- Textarea (markdown supported; preview toggle)
- Attachment upload (drag-and-drop; max 3 files, 10MB each; stored in R2)
- Suggested auto-responses (if KB articles linked to this category exist): small chips above textarea; click to insert boilerplate

**Tab 2: Internal Note**
- Visible to requester: no
- Textarea; no attachment limit restriction
- Label: "🔒 Only visible to support team"

**Tab 3: Quality Annotation** (Support Quality Lead only)
- Quality score selector (1–5 stars)
- Criteria scores: Tone / Accuracy / Speed / Resolution Quality (each 1–5)
- Notes textarea
- [Share with agent] checkbox (default unchecked; if checked, agent sees the annotation)

**[Send Reply] button** (Tab 1/2):
- Shows spinner on click ("Sending…"); button disabled during submit
- POST `/support/tickets/{id}/reply/`
- Validates: non-empty body (inline error "Reply cannot be empty"); attachments must all complete upload before [Send Reply] enabled
- On success: thread HTMX refresh; reply box clears; `first_response_at` set if this is first reply; toast "Reply sent ✓" (green, 3s auto-dismiss)
- If `status=OPEN` or `PENDING_CUSTOMER` and Tab 1 reply: status auto-changes to `IN_PROGRESS`; header part refreshes
- On 500 error: toast "Failed to send reply. Your message has been preserved in the text box. Please try again." (red, persists); text box NOT cleared

**[Submit Annotation] button** (Tab 3):
- POST `/support/tickets/{id}/quality-audit/`
- Creates `support_quality_audit` record
- If "Share with agent" checked: inserts system message in thread visible to assigned agent

---

## Right Panel — Metadata & Context

### Ticket Metadata Header

```
Status:    [IN_PROGRESS ▼]    Tier: [L2 ▼]
Priority:  [CRITICAL ▼]       Assigned: [Rahul Kumar ▼]
Category:  Technical Bug       Created: 5 Nov 2024, 2:05 PM
Source:    PORTAL              Created by: Meena Reddy (self-service)
Last updated: 2 min ago
```

`created_by_id`: if null → shows "Self-service / {source}"; if set → shows platform staff name. For `source=DIVISION_H_ALERT` or `DIVISION_F_ESCALATION`, shows the source system name instead of a user name. For `source=EMAIL`, shows "Email inbound".

Inline edit dropdowns (Support Manager or assigned agent):
- Status dropdown: allowed transitions shown only (can't skip to CLOSED from IN_PROGRESS without RESOLVED first)
- Priority: any agent can change (except to CRITICAL — Support Manager only)
- Tier: Support Manager only
- Assigned: Support Manager or agent can reassign

Changes POST to `/support/tickets/{id}/update/`; header HTMX refresh.

---

### SLA Tracker

```
┌─────────────────────────────────────────┐
│  SLA Status: AT RISK                     │
│  ████████████████░░░░  72% used          │
│                                          │
│  Resolution deadline: 2:45 PM (12 min)  │
│  First response SLA: 2:35 PM ✓ Met      │
│  (Responded at 2:10 PM — 25 min early)  │
│                                          │
│  SLA paused: 0h 14m (customer wait)     │
│  Effective deadline: 2:59 PM (adjusted) │
└─────────────────────────────────────────┘
```

Progress bar: green → amber → red as SLA depletes. Bar uses **effective** deadline (pause-adjusted).
If breached: shows red "BREACHED 2h 4m ago" with effective breach timestamp.
**First response**: compares `first_response_at` vs `first_response_sla_at` (both stored on ticket); green ✓ if `first_response_at ≤ first_response_sla_at`; red ✗ if missed, showing by how much.
**SLA paused**: shows accumulated `sla_pause_duration_seconds`; if currently in PENDING_CUSTOMER, also shows running elapsed time (JS client-side counter).
**Effective deadline**: `sla_breach_at + sla_pause_duration_seconds` — always shown when pause > 0.

---

### Institution Context

```
┌─────────────────────────────────────────┐
│  Sunrise Public School                   │
│  Type: School · Region: Hyderabad        │
│  Subscription: ACTIVE (expires Mar 2025) │
│  Open tickets: 3 · Total tickets: 47    │
│  [View Institution Profile →]            │
├─────────────────────────────────────────┤
│  Requester: Meena Reddy (Admin)          │
│  Email: m.reddy@sunrise.edu.in          │
│  Phone: +91-98765-43210                  │
└─────────────────────────────────────────┘
```

[View Institution Profile →] links to I-04.

If institution has `onboarding_instance` with stage ≠ COMPLETED: shows onboarding status badge ("Onboarding in progress: ADMIN_TRAINED stage").

---

### Ticket Actions (Action Bar)

Vertical list of action buttons on right panel, below institution context:

| Action | Who Sees It | Behaviour |
|---|---|---|
| [Escalate to L2] | L1 agents on L1 tickets | Opens escalation modal (see below) |
| [Escalate to L3] | L2 agents on L2 tickets | Opens escalation modal |
| [Override Tier] | Support Manager only | Moves to any tier without escalation record |
| [Change Status] | Assigned agent; Support Manager | Dropdown confirmation |
| [Link Exam] / [Unlink Exam] | Assigned agent; Support Manager | [Link Exam]: autocomplete exam search by exam name; sets `linked_exam_id`; header HTMX refresh after save. If already linked, button shows [Unlink Exam] — clears `linked_exam_id` (Support Manager only; agents cannot unlink once set); confirmation "Unlink exam from this ticket?" |
| [Merge with…] | Support Manager | Search for duplicate ticket; merges thread |
| [Mark as Duplicate] | Any agent | Links to canonical ticket; closes this one with note |
| [Reopen] | Support Manager only | Re-opens CLOSED ticket with required reason |
| [Close Ticket] | Assigned agent when RESOLVED; Support Manager any time | Confirmation modal "Close this ticket? The requester will be notified."; CSAT survey was already sent on RESOLVED — closing does NOT re-send CSAT. If customer has not submitted CSAT, they may still submit after ticket closes (link valid for 30 days). |

**Escalation Modal:**
```
Escalate Ticket

Destination tier: [L2 ▼]  ← Support Manager: can select L2 or L3 (skip allowed)
                            L1 agents: locked to L2 only (dropdown disabled)
                            L2 agents: locked to L3 only (dropdown disabled)
                            L3 tickets: [Escalate] button not shown at all

Reason type: [▼ Select type] (required)
  - Needs DB investigation
  - Technical bug confirmed
  - Requires code/config change
  - Customer requesting supervisor
  - SLA breach imminent
  - Tier skip — emergency (Support Manager only; logs warning)
  - Billing escalation
  - Other (specify)

Additional notes: [________________] (optional free-text; max 500 chars)

[Cancel]  [Escalate →]
```

`reason_type` maps to `support_ticket_escalation.reason_type` enum. `notes` becomes `reason` text in the escalation record.

POST `/support/tickets/{id}/escalate/`; creates `support_ticket_escalation` record; updates `tier` and `assigned_to_id` (clears assignment for L2 to pick up); inserts system message in thread; HTMX full panel refresh.

**Merge Ticket Modal:**
```
Merge with Duplicate

Search ticket number or subject: [______________]
[ SUP-20241105-000289 · "Exam rejoin issue" · Institution: Sunrise School ]

Merge direction:
○ Keep this ticket as primary (other ticket closes)
● Keep other ticket as primary (this ticket closes)

[Cancel]  [Merge Tickets]
```

Merged ticket thread is appended to primary ticket; merged ticket closed with "MERGED into #SUP-20241105-000289" note.

**Merge validation guards:**
- Cannot merge tickets from different institutions — search results are pre-filtered to same `institution_id` only; cross-institution merge is blocked server-side with 400 "Cannot merge tickets from different institutions."
- Cannot merge a ticket with itself — search excludes the current ticket number.
- Cannot merge a CLOSED ticket into an open ticket — the closed ticket is not searchable; Support Manager must [Reopen] it first if a merge is needed.
- Both tickets must be in a tier the current user has access to; Support Manager can merge across tiers.

---

### Escalation History

Shown only if `support_ticket_escalation` records exist for this ticket.

```
▲ L1 → L2 · Escalated by Priya Sharma · 5 Nov 2024, 2:14 PM
  Reason: Technical investigation needed
  Type: Needs DB investigation
```

Each escalation as a card. Newest first.

---

### KB Suggestions

Auto-populated from `kb_article WHERE linked_ticket_categories @> ARRAY['{category}'] AND status='PUBLISHED'`.

Up to 5 articles shown as clickable links. Opens in new tab.

```
📄 Suggested KB Articles:
  1. How to resolve exam session timeout errors →
  2. Student can't rejoin exam: step-by-step guide →
  3. Browser crash during exam: recovery steps →
```

If 0 matches: "No KB articles for this category. [Flag KB gap →]" — creates `kb_article_gap_flag` record.

---

### Related Tickets

Shows up to 5 tickets from same institution with status NOT IN (`CLOSED`).

```
🔗 Other open tickets from Sunrise Public School:
  · SUP-20241105-000310 · "OTP not received" · L1 · Open
  · SUP-20241104-000289 · "Billing query" · L1 · In Progress
```

Links to respective ticket detail pages.

---

### CSAT Panel

Shown on right panel below Related Tickets. Visible to assigned agent and Support Manager; hidden for Quality Lead and Onboarding Specialist.

**Before CSAT sent** (ticket status ≠ RESOLVED): "CSAT survey will be sent when ticket is resolved."

**After CSAT sent, not yet submitted** (`csat_sent_at` set, `csat_submitted_at` null):
```
Survey sent: 5 Nov 2024 at 2:45 PM
Awaiting customer response
[Resend CSAT ↻]  (Support Manager only)
```

**After customer submits** (`csat_submitted_at` set):
```
CSAT Score: ★★★★☆ (4/5)
Submitted: 5 Nov 2024 at 5:12 PM
Comment: "Quick response, thank you."
[Resend CSAT ↻]  (Support Manager only — score will be lost)
```

**[Resend CSAT]** — Support Manager only; shown when ticket is RESOLVED or CLOSED; clears `csat_submitted_at`, `csat_score`, `csat_comment`; sets `csat_sent_at=now()`, `csat_link_expires_at=now()+30d`. Requires confirmation: "Resend CSAT? The current score (if any) will be permanently lost." Old score not recoverable; I-07 weekly reports not retroactively corrected.

---

## Attachments Section

Below the thread, above the reply box:

All attachments across all messages listed in one panel:
```
📎 Attachments (3)
  · screenshot_error.png (142 KB) · Added by Meena Reddy · [Download]
  · session_log_export.csv (87 KB) · Added by Rahul Kumar · [Download]
```

Files served via R2 signed URL (24h validity). [Download] generates fresh signed URL.

**Attachment upload UX** (in reply box): drag-and-drop zone or [Browse files] button. During upload: progress bar per file ("Uploading… 67%"); file name shown with spinner. On completion: file chip with name + size + [✕ Remove] before sending reply. On error: inline chip error state ("File too large", "File type not allowed", "Scan failed") in red with [✕] to dismiss. Attachments are NOT uploaded on reply-box open — only when user explicitly adds files; upload begins immediately on file selection (before [Send Reply] click) and the R2 key is embedded in the form on completion.

---

## Edge Cases

1. **Ticket belongs to a different tier than current user**: 403 page with "This ticket is in the {tier} queue. Contact your Support Manager to reassign." No content shown.
2. **Assigned agent tries to escalate without selecting reason**: Escalation modal validates reason required; [Escalate] button disabled until reason filled.
3. **PENDING_CUSTOMER ticket**: Reply box shows banner "Awaiting customer response. SLA paused. Your reply will resume the SLA timer."
4. **CLOSED ticket**: All edit controls replaced with "This ticket is closed." grey banner; [Reopen] button shown to Support Manager only; thread is read-only for all.
5. **Ticket with `exam_day_incident=true`**: Red banner at top of left panel: "⚠ Exam-Day Incident — Escalation to L2 mandatory. L1 cannot close." Close button hidden for L1.
6. **L3 ticket with code change required**: L3 agent can add internal note with GitHub PR link; no formal code review flow inside this page — L3 links externally.
7. **Thread auto-refresh conflicts with typing**: Auto-refresh (`?part=thread`) is suspended while reply textarea has focus; resumes on blur.
8. **Merge creates orphan attachments**: Both tickets' attachments are moved to the primary ticket on merge; orphan records cleaned up by background job.
9. **Quality annotation on own ticket (Quality Lead is also the assigned agent)**: Not possible — Quality Lead (#108) cannot be assigned to tickets; this is enforced at **application level**: the ticket assignment API rejects `assigned_to_id` values where the target user has role=108; the dropdown in I-02/I-03 excludes role-90 users.
10. **CSAT already submitted**: CSAT section on right panel shows the submitted score and comment (read-only). [Resend CSAT] button: shown to Support Manager when ticket is RESOLVED or CLOSED. Resending clears `csat_submitted_at`, `csat_score`, `csat_comment`; sets `csat_sent_at=now()`, `csat_link_expires_at=now()+30d`; sends new survey. The old CSAT score is lost (no history table). Consequence: if old score was already factored into I-07 weekly report, the report is NOT retroactively corrected — this is a known trade-off.
11. **Thread pagination**: If a ticket has >100 messages, thread shows the last 50 by default with a "Load earlier messages (N more)" link at the top (HTMX: `?part=thread&before={message_id}`). Auto-scroll always to bottom on initial load.
12. **[Flag KB gap] access**: All roles with I-03 access (L1, L2, L3, Support Manager, Quality Lead, Onboarding Specialist) can click [Flag KB gap →] in the KB suggestions section. Creates `kb_article_gap_flag` record with ticket's category pre-filled as `ticket_category`, `gap_type=MISSING_ARTICLE`.

---

## Notifications (via F-06)

- First reply sent → notification to requester (email + in-app if institution admin)
- Status change to RESOLVED → CSAT survey push notification to requester
- Escalation → push to all L2/L3 agents (assigned queue alert) + Support Manager
- Quality annotation shared with agent → F-06 push to assigned agent
- Support Manager reopen → push to previously assigned agent
