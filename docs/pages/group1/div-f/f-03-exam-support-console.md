# F-03 — Exam Support Console

> **Route:** `/ops/exam/support/`
> **Division:** F — Exam Day Operations
> **Primary Role:** Exam Support Executive (35) — full control
> **Supporting Roles:** Exam Operations Manager (34) — full (escalate to incidents, reassign); Results Coordinator (36) — read; Exam Integrity Officer (91) — read
> **File:** `f-03-exam-support-console.md`
> **Priority:** P0 — Active during all exam windows; SLA = 5 min for CRITICAL tickets

---

## 1. Page Name & Route

**Page Name:** Exam Support Console
**Route:** `/ops/exam/support/`
**Part-load routes:**
- `/ops/exam/support/?part=ticket-table` — open tickets list (polls every 60s during exam)
- `/ops/exam/support/?part=kpi` — KPI strip
- `/ops/exam/support/?part=ticket-drawer&id={id}` — ticket detail drawer
- `/ops/exam/support/?part=resolved-table` — resolved tickets tab
- `/ops/exam/support/?part=quick-actions` — quick actions reference tab
- `/ops/exam/support/?part=stats` — stats tab

---

## 2. Purpose

F-03 is the triage surface for student and institution issues during live exam windows. Support Executives (35) receive inbound reports — from institutions via phone/WhatsApp/email, or via the institution portal — and resolve them within SLA.

Common issue types:
- Student locked out (OTP failed, session expired before exam started)
- Session stuck (timer running but submission button unresponsive)
- Submission failed (network drop during final submit)
- Question not loading (media asset CDN failure)
- Timer mismatch (student's device shows different time than server)
- Login failure (wrong credentials, institution-side password reset needed)

At 74K concurrent, even a 0.1% issue rate = 74 tickets in 90 minutes. F-03 must support fast triage, one-click resolution for common issues, and clear escalation to F-02 incidents when issues affect > 1 student.

---

## 3. Tabs

| Tab | Label | HTMX |
|---|---|---|
| 1 | Open Tickets | `?part=ticket-table` (polls 60s during exam) |
| 2 | Resolved Tickets | `?part=resolved-table` |
| 3 | Quick Actions Reference | `?part=quick-actions` |
| 4 | Stats | `?part=stats` |

---

## 4. Section-Wise Detailed Breakdown

---

### KPI Strip (all tabs)

| # | KPI | Alert |
|---|---|---|
| 1 | Open Tickets | Amber if > 10; Red if any CRITICAL |
| 2 | Overdue (SLA breached) | Red if > 0 — any ticket past SLA |
| 3 | Resolved Today | — |
| 4 | Avg Resolution Time (today) | Amber if > 30 min |
| 5 | Active Exams (currently running) | — |
| 6 | CRITICAL Open | Red if > 0; pulsing |

---

### Tab 1 — Open Tickets

Polls every 60s during active exam window. Support Executive sees all tickets; tickets created by other sessions appear automatically.

#### Search & Filter Bar

**Search:** ticket number, institution name, description keywords. Debounced 300ms.

**Filters:**

| Filter | Control |
|---|---|
| Priority | Multi-select: Critical · High · Medium · Low |
| Ticket Type | Multi-select: Student Locked Out · Session Stuck · Submit Failed · Login Issue · Timer Mismatch · Question Not Loading · Result Not Visible · Other |
| Institution | Searchable select |
| Exam | Searchable select |
| Assigned To | Me / Unassigned / All |
| SLA Status | OK · Due Soon (< 5 min) · Overdue |

**Sort options:** Priority DESC (default) · Created ASC · SLA Due ASC

#### Open Tickets Table (Sortable, Selectable, Responsive)

| Column | Sortable | Notes |
|---|---|---|
| Ticket # | No | `FST-{YYYYMMDD}-{seq}` — clickable opens drawer |
| Priority | Yes | Pill: CRITICAL `bg-red-900` · HIGH `bg-amber-900` · MEDIUM `bg-blue-900` · LOW grey |
| Type | No | Ticket type label |
| Institution | Yes | Institution name |
| Exam | Yes | Exam name |
| Description (excerpt) | No | First 80 chars |
| Reported via | No | Phone · WhatsApp · Email · In-App icon |
| SLA Due | Yes | Countdown: "3 min 20s" (red if < 5 min) |
| Assigned To | No | Role label |
| Status | No | OPEN · IN_PROGRESS |
| Actions | — | [Open] · [Assign to Me] · [Resolve] · [Escalate] |

**SLA countdown logic:**
- CRITICAL: 5 min SLA (`support_sla_minutes_critical` from config)
- HIGH: 15 min
- MEDIUM: 30 min
- LOW: 60 min
- Countdown turns red when < 25% of SLA remaining

**SLA timer start:** `sla_due = created_at + priority_sla_minutes`. Timer starts at ticket creation (`created_at`), regardless of assignment or IN_PROGRESS transition. All datetime arithmetic in IST (Asia/Kolkata timezone). `sla_due` stored as tz-aware timestamptz. Display: if `sla_due - now() < 0`, show "OVERDUE by {N} min {S}s"; if positive, show "{N} min {S}s remaining".

**Row highlight:**
- CRITICAL: `bg-[#1A0505]` red-tinted
- Overdue: `bg-[#1A1200]` amber-tinted

**Bulk actions (on row selection):**
- Assign selected to me
- Reassign selected to [Role picker] — Support Execs (35) can reassign to any Support Exec. Ops Manager (34) can reassign to any Support Exec or Ops Manager. All reassignments logged: "Reassigned to {role} by {actor_role} at {time}." Bulk reassignment sends in-app notification to new assignees: "You have been assigned {N} ticket(s)."

**[+ New Ticket]** (header button): opens Create Ticket Modal (640px)

**Empty state:** "No open tickets right now. The exam window is running smoothly." (shown with green indicator)

---

### Ticket Drawer (640px)

**Header:** Ticket # · Priority pill · Status pill · [×]

#### Section A — Ticket Details

| Field | Read/Edit | Notes |
|---|---|---|
| Ticket Number | Read-only | Auto-generated |
| Exam | Read-only | Exam + Institution |
| Ticket Type | Editable | Can be corrected |
| Priority | Editable | Ops Manager (34) can escalate priority |
| Description | Editable | Full description |
| Student Ref | Read-only | Anonymised hash (DPDPA: not a name) or "Multiple / not identified" |
| Reported Via | Editable | Phone · WhatsApp · Email · In-App |
| Created At | Read-only | Absolute datetime |
| SLA Due | Read-only | Absolute datetime + countdown |

#### Section B — Assignment & Status

| Field | Notes |
|---|---|
| Assigned To | Assignee selector — Support Exec (35) roster |
| Status | OPEN → IN_PROGRESS → ESCALATED / RESOLVED → CLOSED |

**Status transition rules:**
- `OPEN → IN_PROGRESS`: when Support Exec clicks "Take" or assigns to self
- `IN_PROGRESS → RESOLVED`: requires Resolution field filled
- `IN_PROGRESS → ESCALATED`: opens escalation flow (escalates to `exam_session_incident`)
- `RESOLVED → CLOSED`: auto-close after 24h, or manual by Ops Manager

#### Section C — Resolution

| Field | Notes |
|---|---|
| Resolution Type | Select: Session Unlocked · Student Re-Authenticated · Submit Overridden · Informed Wait · No Action Required · Escalated to Incident · Other |
| Resolution Notes | Text area — required for RESOLVED |
| Time Taken | Auto-computed: `resolved_at - created_at` (shown after resolution) |

**Quick Resolution Buttons** (one-click standard resolutions):
- **[Unlock Session]** — calls `POST /ops/exam/support/unlock-session/{ticket_id}/` asynchronously. Button disables and shows spinner + "Unlocking session…". If response within 10s: ✅ "Session unlocked successfully" toast; ticket field "Session Status" → UNLOCKED. If timeout or error after 10s: ❌ "Session unlock failed — {error}" persistent toast; button re-enables for retry. Only available for `SESSION_STUCK` and `STUDENT_LOCKED_OUT` types.
- **[Mark Submit Received]** — marks the submission as received (manual override for `SUBMIT_FAILED` cases where submission actually landed). Requires confirmation.
- **[Inform: Will Resolve Naturally]** — for timer mismatch: notes that server time is authoritative, sets resolution = "Informed institution of server-side time authority". Resolves ticket.

**[Escalate to Incident]:** opens Escalation Modal. Links this ticket to an `exam_session_incident` record.

#### Section D — Activity Log

Timeline of all status changes, assignments, and notes:

| Entry | Notes |
|---|---|
| Created by {role} | With reported-via channel |
| Assigned to {role} | — |
| Status → IN_PROGRESS | — |
| Note added: {text} | Support Exec can add internal notes |
| Status → RESOLVED | Resolution type shown |

**[+ Add Note]** button — appends to activity log. Notes are internal (not shown to institution). Max 500 chars.

---

### Tab 2 — Resolved Tickets

Same table structure as Tab 1. Additional columns:

| Column | Notes |
|---|---|
| Resolved At | Datetime |
| Resolution Type | Type of resolution |
| Time Taken | Duration from open to resolved |

**Filters:** Date range (resolved at) · Institution · Type · Priority

**Export:** [Download CSV] — filtered, DPDPA-safe (student_ref = anonymised hash).

---

### Tab 3 — Quick Actions Reference

A reference guide for Support Executives listing standard resolution steps for each ticket type. Read-only.

| Ticket Type | SLA | Standard Steps | Escalate When |
|---|---|---|---|
| Student Locked Out | HIGH — 15 min | 1. Verify session exists. 2. Use [Unlock Session] if session stuck. 3. If OTP not received: escalate to L2 Support (Div I). 4. If institution-side: inform admin to reset student password. | If > 5 students affected → escalate to Incident |
| Session Stuck | HIGH — 15 min | 1. Check submission API logs. 2. Use [Unlock Session] if session record exists. 3. If JS error: inform student to force-refresh. | If > 10 students affected → escalate to Incident |
| Submit Failed | CRITICAL — 5 min | 1. Check if submission landed in DB (backend check). 2. If yes: use [Mark Submit Received]. 3. If no: ask student to retry. 4. If blocked by CDN: escalate to DevOps. | If submission data lost → CRITICAL Incident |
| Question Not Loading | MEDIUM — 30 min | 1. Confirm CDN status. 2. If CDN issue: escalate to Incident (DevOps). 3. If only 1 student: ask to force-refresh. | If > 3 institutions affected → Critical Incident |
| Timer Mismatch | LOW — 60 min | 1. Server time is authoritative. 2. Use [Inform: Will Resolve Naturally] resolution. 3. Note: timer discrepancy < 2 min is tolerable. | If mismatch > 5 min → escalate to Incident |
| Login Issue | MEDIUM — 30 min | 1. Verify student credentials in portal. 2. Institution admin can reset password. 3. If OTP system down: escalate to Incident. | If OTP system affecting > 50 students → Critical |
| Result Not Visible | MEDIUM — 30 min | 1. Check if results are published in F-04. 2. If published: ask student to refresh portal. 3. If not published: "Results not yet available — check F-04 for publication status." 4. If published but result shows WITHHELD: escalate to Ops Manager (integrity hold context). | If affecting > 10 students at once → escalate to Incident (publication issue). |
| Other | LOW — 60 min | 1. Clarify issue details with institution. 2. If reproducible technical issue: escalate to L2 Support (Div I) or Ops Manager with full description. 3. Log detailed notes for later analysis. | If blocking exam for > 1 student → upgrade to relevant type and escalate. |

---

### Tab 4 — Stats

Statistics for current exam session or date range.

**Date/Exam selector:** Date range picker · Exam filter

#### KPI Summary Cards

- Total tickets received
- By priority breakdown (pie chart)
- By type breakdown (bar chart)
- Avg resolution time
- % resolved within SLA
- Escalation rate (% escalated to incident)

#### Ticket Volume Over Time Chart

`LineChart` — tickets created per hour over the selected date range.
Annotated with exam start/end times.

#### Institution Heatmap

Which institutions generate most tickets. `BarChart` — institution name (anonymised if privacy needed) vs ticket count. Useful for identifying institutions that need extra training (Div I → Onboarding Specialist ref).

---

## 5. Modals

### Create Ticket Modal (640px)

| Field | Required | Notes |
|---|---|---|
| Exam Schedule | Yes | Searchable select — shows ACTIVE + SCHEDULED exams |
| Ticket Type | Yes | Select from enum |
| Priority | Yes | Select |
| Description | Yes | Text area; min 20 chars |
| Student Ref | No | Anonymised hash or "Unknown" — do NOT enter student name |
| Reported Via | Yes | Phone · WhatsApp · Email · In-App |
| Assign To | No | Default: self |

**DPDPA reminder (inline):** "⚠️ Do not enter student names. Use session reference numbers only."

**[Create Ticket]** → `exam_support_ticket` created. ✅ "Ticket created" toast 4s.

### Escalate Ticket to Incident Modal (480px)

"Escalate this ticket to an operational incident?"

| Field | Required | Notes |
|---|---|---|
| Incident Type | Yes | Mapped from ticket type |
| Severity | Yes | Pre-filled based on ticket priority (CRITICAL → CRITICAL) |
| Affected Student Count | Yes | Number estimate |
| Description | Pre-filled from ticket | Editable |

**[Escalate]** → creates `exam_session_incident` linked to ticket (`exam_support_ticket.escalated_to_incident_id`). Sets ticket status = ESCALATED. ✅ "Escalated to incident — #{ref}" toast 8s.

**Escalation failure handling:** If `exam_session_incident` creation fails (DB error): ❌ "Escalation failed — {error}. Retry?" Ticket status remains IN_PROGRESS (not ESCALATED). Ops Manager notified in-app. [Escalate] button re-enables. The SLA continuity between ticket and incident: when ticket status → ESCALATED, ticket's own SLA timer **stops** (ticket is no longer being directly resolved). The incident has no independent SLA — Ops Manager manages it. If incident resolves, linked ticket must be **closed manually** in F-03.

**Exam schedule window for ticket creation:** Create Ticket Modal shows ACTIVE + SCHEDULED exams and COMPLETED exams within last 24 hours (post-exam support window). Exams completed > 24h ago: not shown (contact L2 support via Div I). Rationale: F-03 SLAs only apply during live + immediate post-exam window.

---

## 6. Data Model Reference

Full models in `div-f-pages-list.md`:
- `exam_support_ticket` — full definition with SLA fields, DPDPA-safe student_ref

**`exam_support_ticket_note`** (F-03 only — internal notes):
| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `ticket_id` | FK → `exam_support_ticket` | — |
| `note` | text | Max 500 chars |
| `added_by_id` | FK → auth.User | — |
| `added_at` | timestamptz | — |

---

## 7. Access Control

| Gate | Rule |
|---|---|
| Page access | Support Exec (35), Ops Manager (34), Results Coordinator (36), Integrity Officer (91), Platform Admin (10) |
| Create/edit tickets | Support Exec (35), Ops Manager (34) |
| Use Quick Resolution buttons | Support Exec (35), Ops Manager (34) |
| Escalate to incident | Support Exec (35), Ops Manager (34) |
| Override priority | Ops Manager (34) only |
| Read-only | Results Coordinator (36), Integrity Officer (91) |
| Stats tab | All Div F roles |

---

## 8. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| [Unlock Session] API fails | ❌ "Session unlock failed — check session status or contact DevOps" (persistent toast). Ticket remains IN_PROGRESS. |
| Ticket SLA breached | Red row highlight. Ops Manager (34) notified in-app. Celery task `check_support_ticket_sla` fires every 5 min. |
| Duplicate ticket (same student ref + exam) | Warning on create: "A ticket for this session reference already exists (#{number}). Create anyway?" — not a hard block. |
| CRITICAL ticket older than 5 min unassigned | Celery task `check_support_ticket_sla` (runs every 5 min) auto-assigns to Support Exec with fewest open CRITICAL tickets. Assignee receives in-app notification: "CRITICAL ticket #{number} assigned to you — SLA due in {N} min." Newly assigned ticket highlights in their [Assigned To: Me] filter. |
| Create ticket when no active exams | Warning banner in Tab 1: "No exams are currently active. You can still log tickets for recently completed exams." |

---

## 9. UI Patterns

### Toasts

| Action | Toast |
|---|---|
| Ticket created | ✅ "Ticket created — #{number}" (4s) |
| Session unlocked | ✅ "Session unlocked successfully" (4s) |
| Submit marked received | ✅ "Submission marked as received" (4s) |
| Ticket resolved | ✅ "Ticket resolved in {time}" (4s) |
| Ticket escalated | ⚠️ "Escalated to incident — #{ref}" (8s) |
| SLA breach alert | ❌ "SLA breached — Ticket #{number} is overdue" (persistent until opened) |

### Loading States

- Ticket table: 8-row shimmer
- KPI strip: 6 tile shimmers
- Quick Actions tab: plain text (no shimmer — static content)

### Responsive

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full table; drawer 640px |
| Tablet (768–1279px) | Table: Ticket# + Priority + Type + SLA + Assigned + Actions only |
| Mobile (<768px) | Card per ticket — Ticket# · Type · Priority pill · SLA countdown · [Open] |

---

*Page spec complete.*
*F-03 covers: live ticket triage → SLA timer from created_at (IST timezone) → quick resolutions ([Unlock Session] async with timeout, mark submit received) → auto-assignment with notification → reassign role hierarchy → escalation to incident (failure handling, SLA stop) → Quick Actions Reference (all 8 types including Result Not Visible + Other) → support stats.*
