# N-07 — Compliance Calendar

**Route:** `GET /legal/calendar/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Legal Officer (#75), DPO (#76), Regulatory Affairs Exec (#77)
**Also sees:** POCSO Reporting Officer (#78) — POCSO deadlines only; Contract Coordinator (#103) — contract renewal deadlines only; Data Compliance Analyst (#104) — DSR deadlines only

---

## Purpose

Unified time-based view of every legal and compliance obligation across the entire Division N. At 2,050 institutions, the division manages contract renewals, regulatory filing deadlines, DSR 30-day clocks, POCSO 24-hour reporting windows, policy review cycles, and annual statutory audits simultaneously. A missed CERT-In deadline carries criminal liability; a missed TRAI DLT renewal silently breaks OTPs for 7.6M students; a ToS annual review lapse creates legal exposure in disputes. This calendar aggregates all `legal_compliance_deadline` entries — whether created manually or automatically by background tasks (N-1 through N-10) — into a single navigable, filterable view. It is the division's operational heartbeat.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `legal_compliance_deadline` aggregated by urgency bucket | 5 min |
| Calendar month data | `legal_compliance_deadline` WHERE due_date in [month range] | 10 min |
| Overdue list | `legal_compliance_deadline` WHERE status='OVERDUE' ORDER BY due_date ASC | 2 min |
| Upcoming list | `legal_compliance_deadline` WHERE due_date <= today+14d AND status='UPCOMING' ORDER BY due_date ASC | 5 min |
| Category breakdown chart | `legal_compliance_deadline` GROUP BY category, month for next 12 months | 60 min |
| Deadline detail | `legal_compliance_deadline` single row + linked records | no cache |

Cache keys scoped to `(user_id, filters, view_mode)`. `?nocache=true` for Legal Officer (#75) and DPO (#76) only.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?view` | `month`, `week`, `list` | `month` | Calendar view mode |
| `?month` | `YYYY-MM` | current month | Month to show in month/week view |
| `?category` | `contract`, `regulatory`, `statutory`, `dsr`, `pocso`, `policy`, `training`, `all` | `all` | Filter by deadline category |
| `?status` | `upcoming`, `due_soon`, `overdue`, `completed`, `all` | `all` | Filter by deadline status |
| `?responsible` | `legal`, `dpo`, `reg_affairs`, `pocso`, `all` | `all` | Filter by responsible role |
| `?q` | string | — | Search deadline title |
| `?sort` | `due_date_asc`, `due_date_desc`, `priority_desc`, `category` | `due_date_asc` | List view sort |
| `?page` | integer | `1` | List view pagination |
| `?export` | `csv`, `ical` | — | Export calendar (CSV or .ics for calendar apps) |
| `?nocache` | `true` | — | Bypass Memcached (Legal Officer + DPO only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| KPI strip | `?part=kpi` | Page load | 5 min | `#n7-kpi-strip` |
| Overdue alert strip | `?part=overdue_alert` | Page load | 2 min | `#n7-overdue-alert` |
| Calendar grid | `?part=calendar` | Page load + month navigation + filter change | — | `#n7-calendar` |
| Upcoming sidebar | `?part=upcoming` | Page load | 5 min | `#n7-upcoming-sidebar` |
| Category breakdown chart | `?part=breakdown_chart` | Page load | 60 min | `#n7-breakdown-chart` |
| Deadline detail | `?part=detail&id={uuid}` | Deadline click | — | `#n7-detail-panel` |

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Compliance Calendar   [Month ▼] [Week ▼] [List ▼]   [+ Add]      │
│  Category: [All ▼]  Status: [All ▼]  Responsible: [All ▼]  [Export]│
├────────────────────────────────────────────────────────────────────┤
│  ⚠ OVERDUE STRIP (shown when overdue items exist)                 │
├────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (4 tiles)                                               │
├────────────────────────────────────────────┬───────────────────────┤
│                                            │  UPCOMING DEADLINES  │
│  CALENDAR GRID (month / week / list)       │  (next 14 days)      │
│                                            │                      │
│                                            │  CATEGORY BREAKDOWN  │
│                                            │  CHART (12 months)   │
└────────────────────────────────────────────┴───────────────────────┘
```

---

## Components

### Overdue Alert Strip

Shown only when `legal_compliance_deadline` has `status='OVERDUE'` rows.

```
┌────────────────────────────────────────────────────────────────────┐
│  ⚠  2 deadlines are OVERDUE:                                      │
│  CERT-In #INC-2026-003 (3 days overdue) · MeitY Monthly Jan 2026  │
│  (5 days overdue)                  [View All Overdue →]            │
└────────────────────────────────────────────────────────────────────┘
```

Red background. Auto-refresh every 2 minutes. [View All Overdue →] filters to `?status=overdue`.

---

### KPI Strip (4 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 34           │ │ 7            │ │ 2            │ │ 12           │
│ Deadlines    │ │ Due This     │ │ OVERDUE      │ │ Completed    │
│ This Month   │ │ Week         │ │              │ │ This Month   │
│ 14 completed │ │ ⚠ Act now    │ │ ⚠ Urgent     │ │ 35% rate     │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Deadlines This Month:** `COUNT(legal_compliance_deadline) WHERE MONTH(due_date) = current_month AND YEAR(due_date) = current_year`. Sub-label: "N completed". Delta vs previous month. Clicking → `?month=[current]`.

**Tile 2 — Due This Week:** `COUNT(legal_compliance_deadline) WHERE due_date BETWEEN today AND today+7d AND status='UPCOMING'`. Amber if > 3, red if any today. Clicking → list view `?status=upcoming&sort=due_date_asc`.

**Tile 3 — Overdue:** `COUNT(legal_compliance_deadline) WHERE status='OVERDUE'`. "✓ Clear" green if 0. Pulsing red if > 0. Clicking → `?status=overdue`.

**Tile 4 — Completed This Month:** `COUNT(legal_compliance_deadline) WHERE status='COMPLETED' AND completed_at >= start_of_month`. Sub-label: "completion_rate%" = completed / total_this_month × 100. Green if ≥ 90%, amber if 70–89%, red if < 70%.

---

### Month Calendar View

Standard monthly calendar grid. March 2026 example:

```
         MARCH 2026
         [< February]                    [April >]

  Mon    Tue    Wed    Thu    Fri    Sat    Sun
                                               1
                                               ●DSR

   2      3      4      5      6      7      8
                                             ●MSA

   9     10     11     12     13     14     15
                         ●GST          ●TRAI

  16     17     18     19     20     21     22
                                    ●CERT ⚠BREACH

  23     24     25     26     27     28     29
   ●DPA   ●DSR                             ●ToS

  30     31
  ●NCPCR
```

**Deadline dots:**
- CONTRACT (blue dot ●) — contract renewals, DPA expirations
- REGULATORY (purple dot ●) — TRAI, CERT-In, MeitY
- DSR (teal dot ●) — data subject request due dates
- POCSO (red dot ●) — NCPCR submission deadlines
- POLICY (indigo dot ●) — policy review/publish dates
- STATUTORY (orange dot ●) — audit dates, annual reports
- TRAINING (grey dot ●) — compliance training sessions

**Dot states:**
- Normal: solid dot in category colour
- Due today: pulsing dot with amber ring
- Overdue: red ⚠ warning icon replaces dot
- Completed: grey dot with checkmark overlay

**Hover on dot:** Tooltip shows deadline title, due date, responsible role.
**Click on dot:** Loads Deadline Detail Panel in the right sidebar (HTMX partial into `#n7-detail-panel`).

**Multiple deadlines on same day:** First 3 shown as dots; "+N more" expands to list below the grid row.

**Month navigation:** [< Previous] and [Next >] buttons. HTMX partial-loads new month data without full page reload. `hx-push-url="true"` updates `?month=` in URL.

---

### Week Calendar View

7-column grid for the current week. Each day shows a vertical timeline (09:00–18:00 IST visible, rest collapsible). Deadlines shown as time-boxed blocks if they have a specific time (e.g. CERT-In 6-hour deadline); otherwise shown as all-day items at the top of the day column.

```
         THIS WEEK — 16–22 Mar 2026
   Mon 16   Tue 17   Wed 18   Thu 19   Fri 20   Sat 21   Sun 22

  ALL-DAY:
                                               CERT-In
                                               report
                                               (07:14 IST)
                                                          ToS
                                                          Review

  09:00 ─────────────────────────────────────────────────────────
           [DSR]
  ...
```

Useful for managing tight deadline days (e.g., when CERT-In 6h window falls on a day with other obligations).

---

### List View

Table view of all deadlines with full filter/sort capabilities.

| Column | Description |
|---|---|
| Title | Deadline description (e.g. "Contract renewal — Delhi Public School MSA") |
| Category | Badge: CONTRACT / REGULATORY / DSR / POCSO / POLICY / STATUTORY / TRAINING |
| Due Date | Date + time (IST) if time-specific. Red if overdue, amber if ≤ 3 days |
| Days Left | Countdown or "OVERDUE (Nd)" in red |
| Responsible | Role badge (Legal / DPO / Reg. Affairs / POCSO / Contract Coord. / Analyst) |
| Status | UPCOMING (grey) / DUE_SOON (amber) / OVERDUE (red) / COMPLETED (green) |
| Priority | HIGH / MEDIUM / LOW (derived from category + days left) |
| Linked Record | Link icon → N-02 (contracts), N-03 (DSR/breach), N-04 (filings), N-05 (POCSO incidents) |
| Actions | [View] [Mark Complete] [Snooze] |

**Snooze:** Moves deadline due date forward by 1–7 days (selector). Requires mandatory reason note. Legal Officer or responsible role only. Creates audit log entry. Max 1 snooze per deadline — cannot snooze twice. Red badge "⚠ Snoozed (original due: [date])" shown after snooze.

**[Mark Complete]:** Opens completion modal. Requires: completion notes (min 20 chars) + optional reference number. Sets `status='COMPLETED'`, `completed_at=now()`. Available to responsible role and Legal Officer.

---

### Deadline Detail Panel (right sidebar)

Loads inline when a calendar item is clicked. No page navigation required.

```
┌────────────────────────────────────────────────────────────────────┐
│  TRAI DLT Entity Renewal 2026-27                      [Close ×]   │
├────────────────────────────────────────────────────────────────────┤
│  Category: REGULATORY                                             │
│  Status: UPCOMING                                                  │
│  Due: 1 Nov 2026 (225 days)                                       │
│  Responsible: Regulatory Affairs Exec (#77)                        │
│  Priority: MEDIUM                                                  │
├────────────────────────────────────────────────────────────────────┤
│  Description:                                                     │
│  Annual renewal of TRAI DLT entity registration for sender ID      │
│  EDUFGE. Lapse causes complete OTP/SMS failure across platform.   │
├────────────────────────────────────────────────────────────────────┤
│  Linked Filing: TRAI-2026-001  [View in N-04 →]                   │
├────────────────────────────────────────────────────────────────────┤
│  [Mark Complete]  [Snooze]  [Edit]                                │
└────────────────────────────────────────────────────────────────────┘
```

---

### Add New Deadline Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Add Compliance Deadline                                         │
├──────────────────────────────────────────────────────────────────┤
│  Title*  [                                                ]       │
│  Category*  [Regulatory                                 ▼]       │
│  Due date*  [___ / ___ / _____]  Time (IST): [__:__] (optional) │
│  Recurrence  [None                                      ▼]       │
│    → None / Monthly / Quarterly / Half-Yearly / Annual           │
│  Responsible role*  [Regulatory Affairs Exec (#77)      ▼]       │
│  Priority  [Medium                                      ▼]       │
│  Description  [                                                  │
│                                                                  ]│
│  Link to record:  ○ Contract  ○ Filing  ○ DSR  ○ POCSO  ○ None  │
│  [Search record...                                        ]      │
│                                                                  │
│  [Cancel]                              [Add Deadline]            │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Title: required; min 5 chars
- Category: required
- Due date: required; cannot be more than 1 day in the past (to prevent cluttering with old items)
- Responsible role: required
- Recurrence: if set, `next_due_date` is computed automatically as `due_date + recurrence_offset_days` after completion

POST to `/legal/calendar/deadlines/create/`. Creates `legal_compliance_deadline` record.

---

### Upcoming Deadlines Sidebar

Persistent right-panel showing next 14 days of deadlines.

```
  Upcoming — next 14 days (7 items)

  TODAY — 21 Mar 2026
  ● [RED]   CERT-In BRN-2026-001     Due: 07:14 IST  [View]

  TOMORROW — 22 Mar 2026
  ● [BLUE]  MSA Renewal — DPS        Due: end of day  [View]
  ● [TEAL]  DSR-2026-044 deadline    Due: 09:14 IST   [View]

  MON 23 MAR
  ● [BLUE]  DPA Renewal — Victory    Due: end of day  [View]

  TUE 24 MAR
  ● [TEAL]  DSR-2026-039 deadline    Due: 11:00 IST   [View]

  ...
```

Colour-coded by category. Time shown for deadlines with specific times. [View] opens detail panel. "end of day" for date-only deadlines. Auto-refresh every 5 minutes.

---

### Category Breakdown Chart (12 months)

Stacked bar chart — count of deadlines by category per month for next 12 months.

- **Stacked segments per bar:** CONTRACT (blue) · REGULATORY (purple) · DSR (teal) · POCSO (red) · POLICY (indigo) · STATUTORY (orange) · TRAINING (grey)
- **X-axis:** month labels (MMM YY)
- **Y-axis:** count of deadlines
- **Hover tooltip:** month · total deadlines · breakdown by category
- **Click bar:** filters calendar to that month (`hx-push-url` updates `?month=`)

---

### Export

**[Export CSV]:** Legal Officer (#75) and DPO (#76). Downloads `eduforge_compliance_calendar_YYYY-MM-DD.csv`. Columns: deadline_id, title, category, due_date, status, responsible_role, priority, linked_record_type, linked_record_ref, completed_at, completion_notes.

**[Export .ics]:** All roles. Downloads an iCal `.ics` file for import into Google Calendar / Outlook. Scoped to user's permitted categories. Each deadline becomes a calendar event with VALARM 3-day advance reminder.

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| Overdue strip | No overdue items | Not shown |
| Calendar grid | Month has no deadlines | "No compliance deadlines in [Month Year]." with reassuring note |
| Upcoming sidebar | Nothing in next 14 days | "No deadlines in the next 14 days." with green checkmark |
| List view | No items match filters | "No deadlines found for the selected filters." with [Clear Filters] |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Deadline added | "[title] added to calendar. Due: [due_date]." | Blue |
| Marked complete | "[title] marked complete." | Green |
| Snoozed | "[title] snoozed to [new_due_date]. Reason logged." | Amber |
| Export CSV | "Calendar export downloaded." | Blue |
| Export .ics | "iCal file downloaded. Import into your calendar app." | Blue |
| Month navigation | "[Month Year]" (inline — no toast; calendar silently updates) | — |

---

## Authorization

**Route guard:** `@division_n_required(allowed_roles=[75, 76, 77, 78, 103, 104])` with category-level filtering applied server-side.

| Role | Visible Categories |
|---|---|
| Legal Officer (#75) | All categories |
| DPO (#76) | DSR, REGULATORY (CERT-In/DPDP), POLICY, STATUTORY |
| Regulatory Affairs Exec (#77) | REGULATORY only |
| POCSO Reporting Officer (#78) | POCSO only |
| Contract Coordinator (#103) | CONTRACT only |
| Data Compliance Analyst (#104) | DSR only |

Server-side queryset filter: `WHERE category IN (role_permitted_categories)`. No other categories rendered in any view, including calendar dots.

Add/Edit/Snooze/Complete actions available to:
- Legal Officer (#75): all categories
- Each role: only their permitted categories

---

## Role-Based UI Visibility Summary

| Element | 75 Legal | 76 DPO | 77 Reg. Affairs | 78 POCSO | 103 Contract | 104 Analyst |
|---|---|---|---|---|---|---|
| All deadline categories | Yes | Subset | Regulatory only | POCSO only | Contract only | DSR only |
| Month/week/list view | All 3 | All 3 | All 3 (filtered) | List (filtered) | List (filtered) | List (filtered) |
| Add deadline | Yes (all) | Yes (own) | Yes (own) | Yes (own) | Yes (own) | No |
| Mark complete | Yes (all) | Yes (own) | Yes (own) | Yes (own) | Yes (own) | No |
| Snooze deadline | Yes (all) | Yes (own) | Yes (own) | Yes (own) | Yes (own) | No |
| Overdue strip | Yes | Yes | Yes | Yes (filtered) | Yes (filtered) | No |
| Category breakdown chart | Yes | Yes (filtered) | Yes (filtered) | No | No | No |
| Export CSV | Yes | Yes | Yes | No | No | No |
| Export .ics | Yes | Yes | Yes | Yes | Yes | Yes |
| [?nocache=true] | Yes | Yes | No | No | No | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Calendar month view | < 800ms P95 (10 min TTL) | Index on `(due_date, status, category)` |
| Upcoming sidebar | < 400ms P95 (5 min TTL) | 14-day window, small result set |
| List view (paginated, 25 rows) | < 500ms P95 | Index on `(status, due_date, responsible_role_id)` |
| Category breakdown chart | < 600ms P95 (60 min TTL) | 12-month aggregation, pre-computed |
| Export CSV / .ics | < 5s | Typically < 500 rows total per user |

---

## Integration with Other Division N Pages

Every significant deadline-generating event in Division N automatically creates a `legal_compliance_deadline` entry visible in this calendar:

| Source Event | Deadline Created | Category |
|---|---|---|
| Contract approaching expiry (Task N-1) | "[Institution] [contract type] renewal" | CONTRACT |
| DSR logged (N-03) | "DSR [id] — 30-day resolution deadline" | DSR |
| Breach incident created (N-03) | "CERT-In 6h report — BRN-[id]" | REGULATORY |
| Breach incident created (N-03) | "DPDP authority 72h notification — BRN-[id]" | REGULATORY |
| POCSO incident logged (N-05) | "NCPCR 24h submission — POCSO-[code]" | POCSO |
| Regulatory filing created (N-04) | "[Authority] [filing type] — [period]" | REGULATORY |
| Policy document review due (Task N-10) | "[document name] — annual review due" | POLICY |
| Sub-processor DPA expiry approaching | "Sub-processor DPA renewal — [processor name]" | REGULATORY |

Completing these deadlines from the calendar also updates the source record (e.g., marking a POCSO NCPCR submission deadline as complete is blocked until N-05 has `ncpcr_submitted_at` set — the deadline resolves automatically when the submission is logged there).

---

## Snoozed Deadline — Cross-View Behaviour

When a deadline is snoozed, it must display consistently across all three view modes:

**Month calendar view:**
- On **original due date:** deadline shown with strikethrough text + grey "⏭" icon + tooltip "Snoozed to [new date] by [user] — reason: [reason]"
- On **new due date:** deadline shown as a normal dot/badge in its category colour (no indicator that it was previously snoozed)

**Week calendar view:**
- On **original date column:** greyed-out block with "⏭ Snoozed" label
- On **new date column:** normal time block with subtle amber outline to distinguish from non-snoozed items

**List view:**
- Status column shows: amber "⏭ Snoozed → [new due date]"
- Sort order: item appears at its NEW due date position (not original)
- [View] in detail panel shows both original and new due date

**Overdue strip:**
- Snoozed items are **excluded** from the overdue strip as long as `new_due_date > today`
- If new_due_date also passes without completion → item re-appears in overdue strip with "Previously snoozed" sub-label

**iCal export (.ics):**
- Exports the NEW due date as the event date
- Event description includes: "Originally due: [original date]. Snoozed to [new date]. Reason: [reason]."

---

## Recurring Deadline + Snooze Interaction

For recurring deadlines (Monthly / Quarterly / Half-Yearly / Annual):

**Snooze scope:** Only the **current instance** is snoozed. The next scheduled recurrence is not affected.

**Example:** Monthly contract review due 1 Mar → snoozed to 8 Mar.
- 8 Mar instance: shown as snoozed on 1 Mar, normal on 8 Mar
- 1 Apr instance: created normally on 1 Apr (unaffected)

**Snooze modal — scope selector:**
```
Snooze scope:  ● This instance only (default)
               ○ All future instances  [disabled — future feature]
```

**Data model for snooze:**
| Field | Value |
|---|---|
| `legal_compliance_deadline.original_due_date` | Preserved as the pre-snooze date |
| `legal_compliance_deadline.due_date` | Updated to new (snoozed) date |
| `legal_compliance_deadline.snoozed_at` | Timestamp of snooze action |
| `legal_compliance_deadline.snoozed_by_id` | FK to user who snoozed |
| `legal_compliance_deadline.snooze_reason` | Mandatory text (min 10 chars) |
| `legal_compliance_deadline.snooze_count` | Integer — max value 1 (cannot snooze twice) |
| `legal_compliance_deadline.next_recurrence_due_date` | Unchanged (recurrence series unaffected) |

**[Mark Complete] + recurring snooze:**
- Completing a snoozed recurring instance: `status = 'COMPLETED'`, snooze data preserved in history
- Next recurrence: auto-created with `due_date = original_due_date + recurrence_offset_days` (not snoozed new date + offset)
- Audit trail: completion record shows "[item] completed 3 days after original due date (snoozed)."

---

## Deadline Escalation — Responsible Person Unavailable

Critical deadlines (CERT-In 6h, POCSO NCPCR 24h, DSR 30-day) cannot wait for a person to return from leave. The following escalation rules apply:

**Escalation trigger conditions (checked by Task N-5 extension every 30 minutes when active deadline exists):**

| Responsible Role | Unavailability Signal | Escalation Target | Alert Type |
|---|---|---|---|
| DPO (#76) | `last_login_at < now() - 4h` AND active breach/DSR deadline | Legal Officer (#75) + CEO (#1) | Email + Django Channels real-time alert |
| Legal Officer (#75) | `last_login_at < now() - 4h` AND active POCSO/CERT-In deadline | CEO (#1) + COO (#3) | Email + SMS (Notification Manager #37 integration) |
| Regulatory Affairs Exec (#77) | `last_login_at < now() - 4h` AND filing due < 24h | Legal Officer (#75) | Email only |
| POCSO Reporting Officer (#78) | `last_login_at < now() - 4h` AND NCPCR deadline active | Backup Officer (N-05 designation) + Legal Officer (#75) + CEO (#1) | Email + SMS |
| Contract Coordinator (#103) | Unavailable during contract expiry | Legal Officer (#75) | Email only (lower urgency) |

**Alert message format:**
"⚠ URGENT: [Responsible role] [name] has been inactive for > 4 hours. [Deadline type] for [subject] is due in [time]. Immediate action required by [escalation target]."

**No auto-action:** System NEVER auto-submits, auto-signs, or auto-resolves any compliance deadline without human action. The escalation provides access and awareness only.

**Escalation access grant:** When Legal Officer is escalation target for a normally-DPO-only action (e.g., DSR resolution), a temporary "escalated access" flag (`dpdp_dsr.escalated_to_legal=true`) is set — Legal Officer gains resolve/reject access for that specific DSR for 48 hours.

**Audit trail:** Every escalation event logged in `legal_compliance_deadline.escalation_log` (JSON): `{escalated_at, escalated_to_role, escalated_to_user, reason, alert_sent_via}`.

---

## Keyboard Shortcuts (N-07)

| Key | Action |
|---|---|
| `g` `l` | Go to Legal Dashboard (N-01) |
| `g` `z` | Go to Compliance Calendar (this page) |
| `1` | Switch to Month view |
| `2` | Switch to Week view |
| `3` | Switch to List view |
| `←` | Previous month/week (in Month/Week view) |
| `→` | Next month/week (in Month/Week view) |
| `t` | Jump to today (Month/Week view) |
| `n` | Open Add Deadline modal |
| `/` | Focus deadline search (list view) |
| `Esc` | Close open detail panel or modal |
| `?` | Show keyboard shortcut help overlay |
