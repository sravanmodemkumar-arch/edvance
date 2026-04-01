# J-03 — Account Profile

**Route:** `GET /csm/accounts/{institution_id}/`
**Breadcrumb:** Customer Success › [Institution Portfolio](/csm/accounts/) › [Institution Name]
**Method:** Django `DetailView` + HTMX tab switching + part-loads
**Primary roles:** CSM (#53), Account Manager (#54)
**Also sees:** Escalation Manager (#55), Renewal Executive (#56), CS Analyst (#93), ISM (#94)

---

## Purpose

The deepest view of a single institution's CS relationship. Everything the CSM needs to manage the account is on this page: health breakdown, engagement metrics, touchpoint history, active playbooks, renewal status, escalations, and feedback. This is the primary workspace for account management, QBR preparation, and at-risk triage.

---

## Data Sources

| Tab/Section | Source | Cache TTL |
|---|---|---|
| Institution header | `institution` JOIN `csm_institution_health` JOIN `csm_account_assignment` | 5 min |
| Health breakdown | `csm_institution_health` (single row) | 5 min |
| Engagement metrics | `csm_institution_health` (aggregated columns) | 5 min |
| Health score history chart | `csm_health_history` — daily rows retained for 90 days; inserted nightly by Task J-1 | 10 min |
| Touchpoints tab | `csm_touchpoint` WHERE institution_id = X ORDER BY created_at DESC | 2 min |
| Playbooks tab | `csm_playbook_instance` + `csm_playbook_template` WHERE institution_id = X | 5 min |
| Renewals tab | `csm_renewal` WHERE institution_id = X ORDER BY created_at DESC | 5 min |
| Escalations tab | `csm_escalation` WHERE institution_id = X ORDER BY opened_at DESC | 1 min |
| Feedback tab | `csm_nps_survey` WHERE institution_id = X ORDER BY sent_at DESC | 5 min |
| Contacts tab | `institution_user` WHERE institution_id = X AND role IN ('ADMIN','PRIMARY_CONTACT') | 10 min |
| Support summary strip | `support_ticket` WHERE institution_id = X aggregated | 5 min |

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `?tab` | `overview`, `touchpoints`, `playbooks`, `renewals`, `escalations`, `feedback`, `contacts` | Active tab; default `overview` |
| `?period` | `30d`, `60d`, `90d` | Engagement metrics window for Overview tab; default `30d` |
| `?nocache` | `true` | Bypass Memcached (CSM #53 only) |

Tab selection updates URL via `hx-push-url` without full page reload.

**HTMX out-of-band (OOB) swaps after write operations:**
After any POST/PATCH that changes institution health, renewal, or touchpoint data, the response includes `hx-swap-oob` targets to keep the always-visible header current:
- Touchpoint logged → `hx-swap-oob="#institution-header-team-strip"` refreshes next_action_date in header
- Renewal stage updated → `hx-swap-oob="#institution-header-renewal-strip"` refreshes renewal stage + days
- Escalation created → `hx-swap-oob="#institution-header-escalation-badge"` refreshes open escalation count
All OOB swaps use the `?part=header` partial restricted to the specific section.

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| Institution header | `?part=header` | Page load |
| Overview tab content | `?part=overview&period=30d` | Tab select / period toggle |
| Touchpoints tab | `?part=touchpoints` | Tab select |
| Playbooks tab | `?part=playbooks` | Tab select |
| Renewals tab | `?part=renewals` | Tab select |
| Escalations tab | `?part=escalations` | Tab select |
| Feedback tab | `?part=feedback` | Tab select |
| Contacts tab | `?part=contacts` | Tab select |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  INSTITUTION HEADER (always visible)                                │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ [Logo/Initials]  Delhi Public School — SCHOOL               │    │
│  │ State: Delhi · ID: 1042 · Enrolled: 2,400                   │    │
│  │ Health: 61/100 [████████░░] AT_RISK ↓-7 vs last week       │    │
│  │ Churn risk: 28%   Days to renewal: 45d (₹2.8L)             │    │
│  │                                                             │    │
│  │ CSM: Ananya K.   AM: Ravi S.   ISM: — (past 90d)           │    │
│  │                                                             │    │
│  │ [Log Touchpoint]  [Start Playbook]  [Create Escalation]     │    │
│  │ [View Support Tickets ↗]  [View Billing ↗]                  │    │
│  └─────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────┤
│  TABS: [Overview] [Touchpoints] [Playbooks] [Renewals]              │
│        [Escalations] [Feedback] [Contacts]                          │
├─────────────────────────────────────────────────────────────────────┤
│  TAB CONTENT (HTMX-swapped)                                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Institution Header (always visible)

### Left side
- Initials circle (2-letter abbreviation, coloured by institution type — blue=school, violet=college, orange=coaching, slate=group)
- Institution name (h1) + type badge
- State/City · Institution ID · Enrolled count
- Health score: gauge/progress bar (0–100), tier badge, score delta vs last week

### Right side — Key Metrics row
- Churn probability % — colour: green < 15%, amber 15–35%, red > 35%
- Days to renewal — "45d" or "Overdue" (red)
- ARR — ₹X.XL or ₹X.XCr
- Renewal stage badge

### Team strip
- CSM: [Avatar + name] or "Unassigned" (clickable → Assign drawer for CSM #53)
- AM: [Avatar + name] or "Unassigned"
- ISM: [Avatar + name] + "Active (Day 34/90)" if within 90 days. "Handoff complete — AM took over [date]" if past `ism_tenure_end_date`. "—" if never assigned.
  - **ISM tenure end — mid-playbook handling:** If ISM has active playbook instances when tenure ends (Day 90), Task J-6 auto-reassigns `csm_playbook_instance.assigned_to_id` → `account_manager_id`. This is shown in the header: "Playbook 'AT_RISK_RECOVERY' transferred to [AM name] on [date]" as a one-time informational banner (dismissible).
- Open escalations: "2 open" badge in red (links to Escalations tab) or "—"

### Quick Action buttons
- **[Log Touchpoint]** — opens Touchpoint Drawer; visible to CSM, AM, ISM
- **[Start Playbook]** — opens Playbook Start modal; visible to CSM, ISM
- **[Create Escalation]** — opens Escalation Drawer; visible to CSM, Escalation Manager (#55)
- **[View Support Tickets ↗]** — links to `/support/institutions/{id}/` (new tab); all roles
- **[View Billing ↗]** — links to `/billing/institution/{id}/` (new tab); CSM + AM only

### Support summary strip
Mini strip below actions. Read-only. Shows:
- Open tickets: `N` (link to support page)
- CSAT (30d): `X.X / 5.0`
- Resolved (30d): `N`
- SLA breaches (30d): `N` (red if > 0)

---

## Tab 1: Overview

### Period toggle
```
Period: [30d]  [60d]  [90d]   (button group; hx-get with ?period=30d)
```

### Health Score Breakdown

Two-part layout:

**Left: Component bars** — 5 progress bars with labels and scores:
```
Product Adoption   [████████░░] 18/25
Engagement Depth   [██████████] 23/25
Support Burden     [████░░░░░░] 9/20
Payment Health     [████████░░] 16/20
Relationship       [████░░░░░░] 4/10
                              ──────
                   TOTAL:     70/100
```
Each bar coloured by score as % of max: ≥ 75% of max = green, 50–74% = amber, < 50% = red.

**Right: Health trend mini-chart** — Line chart showing daily health scores for last 90 days. Threshold reference lines at 45 (CRITICAL boundary) and 65 (AT_RISK boundary). Hover: tooltip shows date + score + tier.

### Key Metrics (period-relative)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 1,842        │ │ 12.4         │ │ 8            │ │ 420 hrs      │ │ 2,240        │
│ Active Users │ │ DAU avg (7d) │ │ Exams Created│ │ Content Used │ │ Sessions     │
│ (30d)        │ │              │ │ (30d)        │ │ (video, 30d) │ │ (30d)        │
│ 76.7% of 2.4K│ │ 0.67% of 2.4K│ │              │ │              │ │ ~0.9/user    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

Sub-labels show percentage of enrolled or per-user rates for context.

### Active Playbooks strip

Compact 2-column list of active `csm_playbook_instance` rows:
```
AT_RISK_RECOVERY playbook   ████████░░  6/10 tasks   Due: 28 Mar   Assigned: Ananya K.
```
If no active playbooks: "No active playbooks." with [Start Playbook] button.

### Recent Touchpoints strip

Last 3 touchpoints as timeline items:
```
●  CALL (Outbound)        15 Mar    Ananya K.     "Discussed Q2 plan; positive"
●  EMAIL (Outbound)       8 Mar     Ravi S.       "Sent renewal quote"
●  INTERNAL_NOTE          3 Mar     Ananya K.     "Health dropped — monitoring"
```
[View all touchpoints →] links to Touchpoints tab.

### Next Action reminder
If latest `csm_touchpoint.next_action_date` is populated:
```
⚑  Next action due: 22 Mar (tomorrow)
   "Follow up on Q2 budget approval — Ananya K."
```
Red if past due, amber if today, green if future.

---

## Tab 2: Touchpoints

### Filter bar
```
Type: [All ▼]  Direction: [All ▼]  From: [YYYY-MM-DD]  To: [YYYY-MM-DD]  [Apply]
```

### Timeline

Each touchpoint rendered as a card in reverse-chronological order:

```
┌──────────────────────────────────────────────────────────────────┐
│  ● CALL (Outbound)   15 Mar 2026  10:45 AM   Ananya K. (CSM)     │
│  Subject: Quarterly check-in — Q2 renewal discussion             │
│                                                                  │
│  Notes:                                                          │
│  Principal confirmed budget approved for renewal. Keen to add    │
│  hosteler module. Requested product demo for exam analytics.     │
│                                                                  │
│  Outcome: Positive — renewal expected.                           │
│  Next action: Send expansion pricing sheet by 22 Mar.            │
│  Next action date: 22 Mar 2026                                   │
│                                                                  │
│  [Edit]  [Delete]                                                │
└──────────────────────────────────────────────────────────────────┘
```

Type icons: CALL=phone, EMAIL=envelope, EBR=calendar-star, QBR=chart-bar, TRAINING=academic-cap, ESCALATION_UPDATE=exclamation, ONBOARDING_CHECKIN=check-circle, RENEWAL_DISCUSSION=arrows-repeat, INTERNAL_NOTE=pencil.

[Edit] opens Touchpoint Drawer with pre-filled fields (CSM, AM, ISM who own the record).
[Delete] shows confirm dialog; soft-delete sets `is_deleted=true` on `csm_touchpoint` (record retained for audit). CSM (#53) can delete any touchpoint; AM (#54) and ISM (#94) can delete only their own. Hard-delete is not permitted.

### Add Touchpoint button
```
[+ Log Touchpoint]   (top-right of tab, always visible to CSM/AM/ISM)
```

### Touchpoint Drawer (Add / Edit)

```
┌─────────────────────────────────────────────────────────────────┐
│  Log Touchpoint — Delhi Public School                           │
├─────────────────────────────────────────────────────────────────┤
│  Type*          [CALL              ▼]                           │
│  Direction*     ○ Outbound  ○ Inbound  ○ Internal               │
│  Subject*       [___________________________________]           │
│                                                                 │
│  Notes          [Markdown-supported textarea                   ] │
│                 [3 rows; expandable                            ] │
│  Outcome        [Short outcome summary                         ] │
│  Next action    [What happens next?                            ] │
│  Next action    [YYYY-MM-DD        ]                           │
│  date                                                           │
│  Ad-hoc NPS     [__ /10]  (visible only if type = CALL/EBR/QBR) │
│                                                                 │
│  [Cancel]                              [Save Touchpoint]       │
└─────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Type: required; must be one of the 10 enum values
- Direction: required
- Subject: required; min 5 chars, max 500 chars
- Notes: optional; max 5,000 chars
- Outcome: optional; max 200 chars
- Next action date: optional; must be ≥ today
- Ad-hoc NPS: optional; integer 0–10

POST to `/csm/accounts/{id}/touchpoints/` — returns 201 and HTMX swap of the timeline partial.

**Empty state (no touchpoints):**
"No touchpoints logged yet. Log your first touchpoint to start building the account history."

---

## Tab 3: Playbooks

### Active instances table

| Column | Description |
|---|---|
| Playbook | Template name + trigger type badge |
| Progress | X/Y tasks · progress bar |
| Assigned To | Avatar + name |
| Status | Badge: ACTIVE/COMPLETED/ABANDONED |
| Started | Date |
| Next Task | Next incomplete task title + due date; amber if today, red if overdue |
| Actions | [View Tasks] [Abandon] |

[View Tasks] expands an inline accordion showing the full task checklist:
```
  Step 1  ✓  Welcome call scheduled       Done 3 Mar · Ananya K.
  Step 2  ✓  Portal walkthrough session   Done 5 Mar · Ananya K.
  Step 3  ◻  Send exam setup guide        Due 25 Mar
  Step 4  ◻  First exam scheduled         Due 1 Apr
  ...
```
Checkbox click marks task complete (POST to `/csm/playbooks/instances/{id}/tasks/{step}/complete/`). CSM and playbook-assigned user only.

### Completed playbooks (collapsed by default)

Collapsed section showing: template name + completed date + tasks_completed/tasks_total.

### Start Playbook Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Start Playbook — Delhi Public School                            │
├──────────────────────────────────────────────────────────────────┤
│  Template*   [AT_RISK_RECOVERY — Recovery for at-risk inst. ▼]  │
│  Assign to*  [Ananya K. (CSM)                              ▼]    │
│  Notes       [Optional notes for this instance              ]    │
│                                                                  │
│  PREVIEW: AT_RISK_RECOVERY — 10 tasks · ~30 days                 │
│  ── Step 1: Urgent check-in call (Day 1)                         │
│  ── Step 2: Root cause analysis note (Day 2)                     │
│  ── Step 3: Health score review with AM (Day 3)                  │
│  ... (show first 3; [+7 more tasks] link to expand)              │
│                                                                  │
│  [Cancel]                    [Start Playbook]                    │
└──────────────────────────────────────────────────────────────────┘
```

POST to `/csm/accounts/{id}/playbooks/start/`. Creates `csm_playbook_instance`. Returns HTMX swap of Playbooks tab.

**Empty state (no instances):** "No playbooks started for this account." with [Start Playbook] button.

---

## Tab 4: Renewals

### Renewal pipeline mini-view

Stage bar showing current stage with fill:
```
IDENTIFIED → OUTREACH_SENT → QUOTE_SENT → NEGOTIATING → COMMITTED → [RENEWED]
                                   ↑ current
```

### Current Renewal card

```
┌──────────────────────────────────────────────────────────────────┐
│  Current Renewal                                                 │
│  Plan: School Pro · Seats: 2,400 · ARR: ₹2.8L                   │
│  Renewal date: 5 May 2026 (45 days)                              │
│  Stage: QUOTE_SENT                           [Update Stage ▼]    │
│  Probability: 70%                            [Edit Probability]  │
│  Assigned AM: Ravi S.   Renewal Exec: Pooja M.                   │
│                                                                  │
│  Churn reason: —   Expansion ARR: —                              │
│                                                                  │
│  Notes:                                                          │
│  "Principal approved in-principle. Awaiting CFO sign-off."       │
│  [Edit Notes]                                                    │
└──────────────────────────────────────────────────────────────────┘
```

**[Update Stage ▼]** — dropdown (AM, CSM, Renewal Exec). HTMX POST to `/csm/renewals/{id}/stage/`. If stage = CHURNED, churn reason field appears (required). If stage = RENEWED or EXPANSION, "won_at" timestamp set. Shows confirmation toast.

**[Edit Probability]** — inline edit; integer 0–100; AM, CSM, Renewal Exec.

**Won/Lost gate:** Stage = RENEWED or CHURNED requires CSM or AM confirmation (Renewal Exec can only go to COMMITTED).

### Renewal history table

Previous renewals (stage = RENEWED or CHURNED) in collapsed accordion:
- Renewal year · Plan · ARR · Outcome · Closed date

**Empty state:** "No renewal record exists for this institution." with note "Celery Task J-1 creates renewal records automatically on next nightly run."

---

## Tab 5: Escalations

### Active escalations table

| Column | Description |
|---|---|
| Severity | P1/P2/P3 badge |
| Title | Truncated (link opens Escalation Detail drawer) |
| Status | Badge |
| Assigned To | Escalation Manager name |
| Days Open | Integer; red if P1 > 1d, P2 > 3d |
| ARR at Risk | ₹ amount or "—" |
| Account at Risk | 🔴 flame icon if true |
| Support Tickets | Count of linked tickets |

[Create Escalation] button — top right; CSM and Escalation Manager only.

### Escalation Detail Drawer (opens on row click)

```
┌──────────────────────────────────────────────────────────────────┐
│  P1 CRITICAL Escalation                            [Close ×]     │
│  "Portal login failure impacting 400+ students"                  │
├──────────────────────────────────────────────────────────────────┤
│  Status: IN_PROGRESS      Opened: 18 Mar 2026 (3 days ago)       │
│  Assigned: Kartik M. (Escalation Manager)                        │
│  Commit date: 21 Mar 2026       ARR at risk: ₹2.8L               │
│  Account at risk: Yes  🔴                                         │
│                                                                  │
│  Description:                                                    │
│  "Login failures starting 18 Mar 08:30 IST. ~420 users           │
│  affected. L3 identified as JWT secret rotation issue."          │
│                                                                  │
│  Root cause: JWT secret rotated without notifying portal cache   │
│  Resolution: Cache flushed + new secret propagated              │
│                                                                  │
│  Linked Support Tickets: SUP-20260318-001234, -001241            │
│                                                                  │
│  Cross-Division Coordination:                                    │
│  ● Engineering · Backend Eng · RESOLVED · "Cache cleared 18 Mar" │
│  ● Division I · L3 Eng · RESOLVED · "Root ticket closed"         │
│                                                                  │
│  [Update Status ▼]  [Edit Root Cause]  [Add Division Note]       │
└──────────────────────────────────────────────────────────────────┘
```

**Resolved escalations** — shown in collapsed section below active table.

**Empty state:** "No escalations raised for this institution." — with note about P1 auto-creation from Div-I.

---

## Tab 6: Feedback

### NPS/CSAT survey list

Table with columns: Survey Type · Sent To · Sent Date · Score · Category · Responded · Follow-up · Verbatim

Score column:
- NPS: number 0–10 with PROMOTER/PASSIVE/DETRACTOR colour badge
- CSAT: number 1–5 with star icon

Verbatim column: truncated to 80 chars; expand button shows full text in tooltip.

Follow-up column: checkbox (follow_up_required); yellow flag if true but not yet actioned.

### Send Survey button

[Send NPS Survey] — top-right; CSM (#53) and ISM (#94) only.

```
┌──────────────────────────────────────────────────────────────────┐
│  Send Survey — Delhi Public School                               │
├──────────────────────────────────────────────────────────────────┤
│  Survey type*   [QUARTERLY_NPS                           ▼]      │
│  Send to*       [principal@dpsdelhi.edu     ] Name: [_______]    │
│  Custom message [Optional personalised intro            ]        │
│                                                                  │
│  Survey expires 14 days after sending.                           │
│                                                                  │
│  [Cancel]                              [Send Survey]             │
└──────────────────────────────────────────────────────────────────┘
```

Validation: email required + valid format; name required; survey_type required.
Guard: cannot send to same email if non-expired survey already pending.

### NPS mini-chart

Small line chart showing this institution's NPS scores over time (only if ≥ 2 responses). Y-axis 0–10.

**Empty state:** "No surveys sent to this institution yet. Send the first survey to start collecting feedback."

---

## Tab 7: Contacts

### Key contacts table

Read from `institution_user` table. Shows institution admins and primary contacts only.

| Column | Description |
|---|---|
| Name | Full name |
| Role at Institution | Admin / Primary Contact / Staff |
| Email | — |
| Phone | If available in institution_user |
| Last Active | Last portal login from institution_user.last_login_at |
| Primary Contact | Star icon if designated primary; editable by CSM/AM |

**Primary contact designation:** Only one user can be primary contact. Clicking star on another user shows confirmation: "Set [Name] as primary contact? This will remove the designation from [Current Primary]." POST to `/csm/accounts/{id}/contacts/{user_id}/set_primary/`.

**No create/edit/delete** — contacts are managed in the tenant admin section. This tab is read-only from the CS perspective (shows a note: "To add or modify institution contacts, use the Institution Admin section.").

**Empty state:** "No admin contacts found for this institution."

---

## Create Escalation Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  Create Escalation — Delhi Public School                         │
├──────────────────────────────────────────────────────────────────┤
│  Title*          [____________________________________________]   │
│  Severity*       ○ P1 CRITICAL  ○ P2 HIGH  ○ P3 MEDIUM           │
│  Description*    [Textarea; min 50 chars                      ]  │
│  Root cause      [Optional at creation                        ]  │
│  Commit date     [YYYY-MM-DD  ] (must be ≥ today)               │
│  Assigned to*    [Kartik M. (Escalation Manager)           ▼]    │
│  Support tickets [Search and link tickets...               ]     │
│                  SUP-20260318-001234 [×]                        │
│  Account at risk ○ Yes  ○ No                                     │
│  ARR at risk     [₹ 2,80,000    ] (appears if account_at_risk=Y) │
│  Cross-division  [+ Add division coordination note]             │
│                                                                  │
│  [Cancel]                         [Create Escalation]           │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Title: required; min 10 chars
- Severity: required
- Description: required; min 50 chars
- Assigned to: required; must be a user with Escalation Manager role
- Commit date: optional but recommended for P1
- ARR at risk: required if account_at_risk = Yes; positive integer in ₹ (converted to paise on save)

POST to `/csm/escalations/` — returns 201 and notification sent to assigned Escalation Manager.

---

## Permissions Summary

| Action | 53 CSM | 54 AM | 55 Escalation | 56 Renewal | 93 Analyst | 94 ISM |
|---|---|---|---|---|---|---|
| View all tabs | Yes | Yes | Yes (restricted) | Yes (restricted) | Yes (read) | Yes (restricted) |
| Log touchpoint | Yes | Yes | No | No | No | Yes (own) |
| Edit touchpoint | Own + team | Own | No | No | No | Own |
| Delete touchpoint | Own + team | Own | No | No | No | Own |
| Start playbook | Yes | No | No | No | No | Yes (own) |
| Complete playbook task | Yes (assigned) | No | No | No | No | Yes (assigned) |
| Abandon playbook | Yes | No | No | No | No | No |
| Update renewal stage | Yes | Yes | No | Up to COMMITTED | No | No |
| Win/lose renewal | Yes | Yes | No | No | No | No |
| Create escalation | Yes | No | Yes | No | No | No |
| Update escalation | Yes | Yes | Yes (full) | No | No | No |
| Send survey | Yes | Own accounts | No | No | No | Own accounts |
| Mark follow-up required | Yes | Yes | No | No | No | No |
| Set primary contact | Yes | Yes | No | No | No | No |
| Export account data | Yes | No | No | No | Yes | No |
| Assign CSM/AM | Yes (CSM role) | No | No | No | No | No |
