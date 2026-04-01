# K-03 — Account Profile

**Route:** `GET /group1/k/account/<lead_id>/`
**Method:** Django `DetailView` + HTMX tab switching + part-loads
**Primary roles:** B2B Sales Manager (#57), Sales Executive Schools (#58), Sales Executive Colleges (#59), Sales Executive Coaching (#60), Pre-Sales/Solutions Engineer (#96), Inside Sales Executive (#97)
**Also sees:** Demo Manager (#62 — view only), Pre-Sales Engineer (#96 — assigned leads only)

---

## Purpose

Single account deep-dive. Complete picture of one institution's sales journey — contact info, stage, all logged activities, demo tenant status, free-text notes, and quick actions to advance the deal. The working desk for any Sales Executive managing a live opportunity. Everything needed to prepare for a call, log an outcome, move the stage, or hand off to Pre-Sales is reachable in one place without navigating back to the pipeline list.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Account header | `sales_lead` WHERE id = lead_id | No cache — live |
| Activity timeline | `sales_activity` WHERE lead_id ORDER BY occurred_at DESC | No cache — live |
| Demo tenant card | `sales_demo_tenant` WHERE lead_id | 2 min |
| Owner / manager names | `auth_user` WHERE id IN (owner_id, manager_id) | 10 min |
| Pre-Sales assignment | `auth_user` WHERE id = presales_id | 5 min |
| Channel partner name | `channel_partner` WHERE id = channel_partner_id | 10 min |

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `lead_id` | UUID / integer path param | Identifies the lead record |
| `?tab` | `timeline`, `demos`, `notes` | Active tab; default `timeline` |

Tab selection updates URL via `hx-push-url` without full page reload.

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| Activity timeline | `htmx/k/account/<id>/timeline/` | After log activity (no auto-refresh) |
| Demo tenant card | `htmx/k/account/<id>/demo-status/` | After demo create / reset; 2 min auto-refresh |
| Stage progress bar | `htmx/k/account/<id>/stage-bar/` | After stage move |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back to Pipeline                                             │
│  KIMS High School, Hyderabad          [SCHOOL] [DEMO_DONE]      │
│  Contact: Ramesh Kumar · 9876543210 · ramesh@kims.edu           │
│  ARR: ₹1.2L   Students: ~800   Territory: TELANGANA             │
│  Owner: Rahul (Schools Exec)   Pre-Sales: Anika   Mgr: Vikram   │
├──PROSPECT──CONTACTED──DEMO_SCHEDULED──DEMO_DONE──●PROPOSAL_SENT──NEGOTIATION──CLOSED_WON──┤
│  Stage Progress Bar (current stage highlighted)                 │
│  [Move to Proposal →]   [Log Activity]   [Schedule Demo]        │
├─────────────────────────────────────────────────────────┬───────┤
│  [Timeline] [Demo Tenant] [Notes]                       │SIDEBAR│
│                                                         │       │
│  TIMELINE                                               │Quick  │
│  ● Today — Rahul — DEMO — 45 min — POSITIVE             │Actions│
│    "Strong interest in exam module"                     │       │
│    Next: Send proposal by Fri                           │[Email]│
│  ● 3d ago — Rahul — CALL — 12 min — POSITIVE            │[Call] │
│    "Decision maker confirmed, budget approved"          │[Demo] │
│  ● 5d ago — Rahul — EMAIL — NEUTRAL                     │[Prop.]│
│    "Sent product one-pager"                             │[Assign│
│                                                         │ PreS.]│
└─────────────────────────────────────────────────────────┴───────┘
```

---

## Components

### 1. Account Header

Top section, always visible regardless of active tab.

**Row 1 — Identity:**
- Back link "← Back to Pipeline" linking to `/group1/k/pipeline/`
- Institution name (h1) + city
- Type badge: SCHOOL=blue / COLLEGE=violet / COACHING=orange / GROUP=slate
- Stage badge: coloured by stage (see Stage Progress Bar section)

**Row 2 — Contact:**
- Contact name · Phone as `tel:` click-to-call link · Email as `mailto:` link
- If `is_channel_deal=True`: additional badge "Channel Deal" with channel partner name

**Row 3 — Deal metrics:**
- ARR Estimate (formatted ₹X.XL or ₹X.XCr)
- Student Count Estimate (formatted with ~prefix: "~800")
- Territory
- State

**Row 4 — Team:**
- Owner: name + role label (e.g., "Schools Exec")
- Pre-Sales: name if presales_id set, else "—"
- Manager: resolved via owner's manager_id from auth_user hierarchy
- Edit button (pencil icon) — visible to record owner and #57 Sales Manager

**CSM Assignment (CLOSED_WON leads only):** Row 4 appears only after stage = CLOSED_WON. Shows "CSM: [Name] (Div-J)" and "ISM: [Name] (Div-J)" auto-populated from the Div-J assignment created on close. Read-only in K-03 — assignment owned by Division J. If not yet assigned (Celery task pending), shows "CS assignment pending..." in grey.

---

### 2. Stage Progress Bar

Linear step bar showing all 8 pipeline stages in order:

```
PROSPECT → CONTACTED → DEMO_SCHEDULED → DEMO_DONE → PROPOSAL_SENT → NEGOTIATION → CLOSED_WON
                                                                                 ↘ CLOSED_LOST
```

- Current stage: filled circle (●) with highlighted label
- Completed stages: filled tick (✓) with muted colour
- Future stages: empty circle (○)
- CLOSED_WON and CLOSED_LOST shown as split branches at the end

**Click behaviour:**
- Clicking a future stage → opens Stage Move Modal with that stage pre-selected
- Clicking CLOSED_LOST at any time → opens Stage Move Modal with lost_reason field required
- Backward stage move (clicking earlier stage) → requires Manager (#57) approval; shows warning: "Moving backward requires Sales Manager approval. Continue?" — submits for approval rather than immediately updating

**Backward stage move when Manager is unavailable:** If no Manager is logged in for >24 hours, backward move request escalates to Platform COO (#3) via the same in-app notification. This escalation event ("Backward stage move escalated to COO") is logged in the Notification Events table in div-k-pages-list.md. Platform COO (#3) approves or rejects via their standard platform notification centre — they do not need access to Division K pages directly. The approval/rejection is a simple in-app action that updates the stage move request status. The request auto-expires (rejected) after 72 hours if no action — exec is notified "Stage move request expired. Resubmit when manager is available."

**Stage badge colours:** PROSPECT=grey / CONTACTED=blue / DEMO_SCHEDULED=cyan / DEMO_DONE=violet / PROPOSAL_SENT=amber / NEGOTIATION=orange / CLOSED_WON=green / CLOSED_LOST=red

---

### 3. Quick Actions Sidebar

Right-hand sidebar (fixed, not scrolled away on timeline scroll).

| Button | Action | Visible To |
|---|---|---|
| Log Activity | Opens Log Activity Drawer | Owner + #57 + #96 (assigned) |
| Move Stage | Opens Stage Move Modal | Owner + #57 |
| Schedule Demo | Opens Activity Drawer pre-filled type=DEMO | Owner + #57 + #62 |
| Assign Pre-Sales | Opens user dropdown modal; sets presales_id | #57 only |
| Convert to Won | Green CTA; confirms won_at=now, stage=CLOSED_WON; triggers notifications to Finance, Onboarding, CS | Owner + #57 |
| Convert to Lost | Red link; requires lost_reason selection | Owner + #57 |
| Edit Lead Info | Opens Edit Lead Drawer | Owner + #57 |

**Convert to Won confirmation modal:**
```
┌─────────────────────────────────────────────────────┐
│  Close Deal — KIMS High School                      │
│  Mark as WON?                                       │
│  ARR: ₹1.2L  ·  Stage will move to CLOSED_WON      │
│  This will notify Finance, Onboarding, and CS.      │
│  Won Date: [Today — 21 Mar 2026  ]                  │
│  [Cancel]                    [Confirm Won ✓]        │
└─────────────────────────────────────────────────────┘
```

On CLOSED_WON confirmation: (1) stage → CLOSED_WON, won_at = now(). (2) System creates csm_account_assignment (Div-J table) with institution_id + csm_id pre-populated from Sales Manager's default CSM map for that territory (editable in K-07). (3) Notification sent to: Sales Manager (#57), Onboarding Specialist (#51, Div-I), Billing Admin (#70, Div-M), ISM (#94, Div-J). (4) Division M integration: Billing Admin (#70) receives subscription activation task payload: { institution_id, arr_estimate_paise, plan_tier (derived from segment_size), deal_id, won_at }. This triggers subscription provisioning in Division M. See Integration Points in div-k-pages-list.md. (5) If no CSM is mapped to this territory, shows modal: "Assign Customer Success Manager before closing" with CSM dropdown — required before close can complete.

**Assign Pre-Sales modal:** Dropdown filtered to users with role #96. Shows name + current workload (N active PoCs). Saves to `sales_lead.presales_id`. Sends in-app notification to assigned Pre-Sales Engineer.

---

### 4. Tab: Activity Timeline

Default active tab. Chronological list, newest first.

**Filter bar (above timeline):**
```
Type: [All ▼]   Outcome: [All ▼]   Logged By: [All ▼]   [+ Log Activity]
```

**Each timeline entry:**
```
┌──────────────────────────────────────────────────────────────────┐
│  ● DEMO   21 Mar 2026 · 2:30 PM   Rahul Sharma (Schools Exec)   │
│  Duration: 45 min   Outcome: POSITIVE                            │
│                                                                  │
│  "Strong interest in the exam module. Principal was present.     │
│   Showed live test creation and result analytics."               │
│                                                                  │
│  Next: Send proposal with exam module pricing by Fri 24 Mar     │
│  [Edit]  [Delete]                                                │
└──────────────────────────────────────────────────────────────────┘
```

**Entry structure details:**
- Coloured left-border dot: CALL=blue / EMAIL=grey / MEETING=teal / DEMO=purple / WHATSAPP=green / SITE_VISIT=brown / PROPOSAL=amber / RFP_RESPONSE=indigo
- Activity type icon + label
- `logged_by` name + role label
- `occurred_at` formatted as "21 Mar 2026 · 2:30 PM"
- Duration (if set): "45 min"
- Outcome badge: POSITIVE=green / NEUTRAL=grey / NEGATIVE=red / NO_SHOW=amber / RESCHEDULED=orange
- Notes text: truncated to 3 lines with "Show more" expand link
- Next Action + Next Action Due: shown as "Next: [text] by [date]" — highlighted amber if due today, red if overdue
- [Edit] visible to the activity's logged_by user and #57
- [Delete] visible to #57 only; soft-delete with confirm dialog

**"Log Activity" button** at top right of tab; also shown as floating button if timeline has 5+ entries (so it stays in view).

**Empty state:** "No activities logged yet. Log the first touchpoint →" with [Log Activity] button.

---

### 5. Log Activity Drawer

Slide-in drawer from right. Title: "Log Activity — [Institution Name]".

```
┌─────────────────────────────────────────────────────────────────┐
│  Log Activity — KIMS High School                                │
├─────────────────────────────────────────────────────────────────┤
│  Activity Type*   [CALL  |EMAIL|MEETING|DEMO|WA|VISIT|PROP|RFP] │
│                   (segmented button row)                        │
│  Date & Time*     [2026-03-21  ]  [14:30  ]  (default: now)    │
│  Duration         [___] minutes  (optional)                     │
│  Outcome*         ○ POSITIVE  ○ NEUTRAL  ○ NEGATIVE             │
│                   ○ NO_SHOW   ○ RESCHEDULED                     │
│  Notes            [Textarea — what happened, what was said?   ] │
│                   [Supports plain text, max 2,000 chars       ] │
│  Next Action      [What's the next step?              ]  (opt.) │
│  Next Action Due  [YYYY-MM-DD  ]  (optional)                   │
│                                                                 │
│  [Cancel]                              [Save Activity]         │
└─────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Activity Type: required; one of 8 enum values
- Date & Time: required; `occurred_at` cannot be more than 5 minutes in the future
- Outcome: required
- Notes: optional; max 2,000 chars
- Next Action Due: optional; must be ≥ today if set

On save: POST to `sales_activity` table → HTMX retarget swaps timeline partial → stage bar OOB swap if stage was changed as a side-effect of activity type (e.g., logging a DEMO when stage is CONTACTED auto-prompts "Update stage to DEMO_DONE?").

**Stage auto-prompt on activity log (role-dependent):**
After saving an activity, the system evaluates whether to prompt a stage move based on activity type and current stage:
- DEMO activity logged on DEMO_SCHEDULED lead → prompts "Move to DEMO_DONE?" (all roles who own the lead)
- PROPOSAL activity logged → prompts "Move to PROPOSAL_SENT?" (all roles)
- CALL/EMAIL activity logged on PROSPECT → prompts "Move to CONTACTED?" (all roles)

Important: This is a **prompt only** — it does NOT auto-move stage. The user must explicitly confirm. Role #97 (Inside Sales) can confirm moves up to DEMO_SCHEDULED stage only. If the prompt suggests a move beyond DEMO_SCHEDULED for role #97, it shows: "Request stage advance to [Stage]? Your manager will be notified." — this creates an in-app notification for Sales Manager (#57) to approve.

---

### 6. Stage Move Modal

Triggered from sidebar "Move Stage" button or clicking a future stage in the progress bar.

```
┌─────────────────────────────────────────────────────────────────┐
│  Move Stage — KIMS High School                                  │
├─────────────────────────────────────────────────────────────────┤
│  Current Stage:   DEMO_DONE                                     │
│  Move to:         [PROPOSAL_SENT              ▼]                │
│                                                                 │
│  Reason / Notes   [Optional context for this stage move      ]  │
│                   (Required if moving to CLOSED_LOST)           │
│                                                                 │
│  Lost Reason      [Select reason...              ▼]             │
│  (CLOSED_LOST only: PRICE/COMPETITOR/NO_BUDGET/TIMING/OTHER)   │
│                                                                 │
│  [Cancel]                          [Confirm Stage Move]        │
└─────────────────────────────────────────────────────────────────┘
```

On confirm: PATCH `sales_lead.stage` + implicit `sales_activity` record logged (type=relevant action, logged_by=current user, outcome=POSITIVE for forward moves). Stage bar HTMX swap. Account header stage badge OOB swap.

---

### 7. Tab: Demo Tenant

Shows the linked `sales_demo_tenant` record if one exists for this lead.

**Demo tenant card (when tenant exists):**
```
┌─────────────────────────────────────────────────────────────────┐
│  Demo Tenant — KIMS High School                    [ACTIVE]     │
│  Tenant ID: edu-demo-4821                                       │
│  Demo Type: STANDARD   Template: SCHOOL_DEMO                    │
│  Created: 10 Mar 2026   Expires: 9 Apr 2026 (19 days)           │
│  Students Seeded: 50   Exams Seeded: 5                          │
│  Reset Count: 1   Last Reset: 15 Mar 2026                       │
│  Last Login: 20 Mar 2026 · 4:12 PM   Total Logins: 4            │
│                                                                 │
│  [Reset Demo Data]  [Extend Expiry ▼]  [Deactivate]            │
│  [Generate Access Link]                                         │
└─────────────────────────────────────────────────────────────────┘
```

**Action buttons visibility:**
- Reset Demo Data: #62 only; shows confirm: "Reset all demo data? Student progress, exam results, and customisations will be lost. This is irreversible."
- Extend Expiry (+7 / +14 / +30 days): #62 and #57
- Deactivate: #62 only; confirm: "Are you sure? The prospect will lose access immediately."
- Generate Access Link: #62 and record owner; creates 24-hour login token, copies to clipboard, sends email to `contact_email`

**Admin credentials display (masked):**
- Admin email shown as "ram***@kims.edu"
- [Copy Access Link] button

**When no tenant exists:**
"No demo tenant provisioned for this lead." + [Create Demo Tenant →] button (visible to #62 and #57). Clicking opens the Create Demo Tenant Wizard from K-04.

**Pre-Sales (#96) view:** Can see all tenant details (read-only) for leads where they are the assigned presales_id. Cannot perform actions.

---

### 8. Tab: Notes

Free-text notes field for the account, saved in `sales_lead.notes`.

```
┌─────────────────────────────────────────────────────────────────┐
│  Account Notes                            Last saved: 2 min ago │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Principal is very interested but procurement goes through │  │
│  │ district-level approval. Expect 3-4 week delay after      │  │
│  │ proposal submission. Key decision maker is VP Academics,  │  │
│  │ not the Principal...                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│  2,340 / 5,000 characters                                       │
└─────────────────────────────────────────────────────────────────┘
```

- Auto-saves on textarea blur (PATCH `sales_lead.notes`)
- "Last saved: [relative time]" shown top-right; turns amber if unsaved changes present
- Character count (max 5,000)
- Editable by record owner and #57; all other permitted roles see read-only rendered text

**Empty state:** "Add private notes for this account. Visible only to the sales team."

---

### 9. Edit Lead Drawer

Opens from header Edit button (pencil icon). Pre-fills all current lead values.

Fields: Institution Name · Institution Type · Segment Size · Stage (read-only in drawer; use Stage Move Modal) · Contact Name · Contact Phone · Contact Email · Student Count Estimate · ARR Estimate (₹) · Expected Close Date · Lead Source · Territory · State · City · Is Channel Deal (toggle) · Channel Partner (appears if is_channel_deal=True)

Visible to: record owner and #57.

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| Page not found | lead_id does not exist or user has no access | "Lead not found or you do not have access to this account." (404) |
| Activity Timeline | No sales_activity rows | "No activities logged yet. Log the first touchpoint →" |
| Demo Tenant tab | No sales_demo_tenant row | "No demo tenant provisioned for this lead." |
| Notes tab | sales_lead.notes is null or empty | "Add private notes for this account. Visible only to the sales team." |

---

## Toast Messages

| Action | Toast |
|---|---|
| Activity logged | "Activity logged: CALL with KIMS High School" (green) |
| Stage moved | "Stage updated to PROPOSAL_SENT for KIMS High School" (green) |
| Demo tenant created | "Demo tenant provisioned for KIMS High School" (green) |
| Demo data reset | "Demo data reset for KIMS High School. Seed data reloaded." (green) |
| Expiry extended | "Expiry extended to 19 Apr 2026 for KIMS High School" (green) |
| Demo deactivated | "Demo tenant deactivated for KIMS High School" (amber) |
| Access link generated | "Access link copied to clipboard. Valid for 24 hours." (blue) |
| Pre-Sales assigned | "Pre-Sales Engineer Anika assigned to KIMS High School" (green) |
| Lead converted to Won | "Deal closed! KIMS High School — ₹1.2L ARR" (green) |
| Lead converted to Lost | "KIMS High School marked as CLOSED_LOST" (red) |
| Notes saved | "Notes saved" (grey/silent) |
| Stage move requires approval | "Backward stage move submitted for Sales Manager approval" (amber) |

---

---

## Authorization

**Route guard:** `@division_k_required(allowed_roles=[57, 58, 59, 60, 61, 62, 95, 96, 97])` applied to `LeadDetailView`.

| Scenario | Behaviour |
|---|---|
| Sales Exec accessing own lead | 200 OK |
| Sales Exec accessing another exec's lead | 404 Not Found (not 403 — information leakage prevention) |
| Demo Manager (#62) accessing lead with no demo tenant | 200 OK — Demo Tenant tab shows "No demo tenant" empty state |
| Pre-Sales (#96) accessing non-assigned lead | 404 Not Found |
| Sales Ops (#95) accessing any lead | 200 OK — all edit actions hidden (read-only view) |
| Partnership Manager (#61) accessing lead | 200 OK — no edit controls shown; read-only header view |
| Unauthenticated | Redirect to login |

**Stage move authorization:** Stage advance PATCH `/group1/k/account/<id>/stage/` checks: (1) user is owner_id or manager_id. (2) For backward moves: additionally checks approval_status from pending approval record. Server returns 403 if neither condition met.

---

## Role-Based View Summary

| Feature | #57 Mgr | #58–60 Exec | #61 Partner | #62 Demo | #63 Channel | #95 Ops | #96 PreSales | #97 Inside |
|---|---|---|---|---|---|---|---|---|
| View header | Full | Own leads | No | View linked | No | Read | Assigned | Own inbound |
| Edit lead info | Yes | Own leads | No | No | No | No | No | Own |
| Stage progress bar (advance) | All leads | Own leads | No | No | No | No | Assigned (prompt only) | Own (up to DEMO_SCHED) |
| Stage progress bar (backward) | Approve | Request only | No | No | No | No | No | No |
| Log activity | All leads | Own leads | No | View only | No | No | Assigned leads | Own |
| View activity timeline | Full | Own leads | No | Demo tab only | No | Read | Assigned | Own |
| Demo tenant tab | View+extend | View linked | No | Full | No | No | View linked | No |
| Notes tab | Full | Own leads | No | No | No | Read | Assigned (read) | Own |
| Convert to Won | All leads | Own leads | No | No | No | No | No | No |
| Convert to Lost | All leads | Own leads | No | No | No | No | No | No |
| Assign Pre-Sales | Yes | No | No | No | No | No | No | No |
| Delete lead | Yes | No | No | No | No | No | No | No |
| View CSM assignment | Yes | Own leads | No | No | No | Yes | No | No |
