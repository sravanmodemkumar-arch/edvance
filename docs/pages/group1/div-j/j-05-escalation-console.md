# J-05 — Escalation Console

**Route:** `GET /csm/escalations/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** Escalation Manager (#55)
**Also sees:** CSM (#53) full, Account Manager (#54) read-only, CS Analyst (#93) read-only, ISM (#94) read-only, Renewal Executive (#56) no access

---

## Purpose

Single pane of glass for all open CS-level escalations across 2,050 institutions. The Escalation Manager owns this page — triaging severity, coordinating cross-division resolution, tracking commit dates, and ensuring account-threatening issues are resolved before they cause churn. Different from Division I's support ticket queue: escalations are higher-level account-health events that require executive attention and cross-team coordination.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Escalation KPI strip | `csm_escalation` aggregated by status + severity | 1 min |
| Escalation table | `csm_escalation` JOIN `institution` JOIN `csm_institution_health` | 1 min |
| Resolution trend chart | `csm_escalation` closed in last 90 days grouped by week + severity | 15 min |
| ARR at risk summary | `csm_escalation` WHERE status NOT IN ('RESOLVED','CLOSED') AND account_at_risk=true | 1 min |
| Cross-division status | `csm_escalation.cross_division_notes` (parsed from JSONB) | 1 min |

Cache key includes all filter params. `?nocache=true` for CSM (#53) and Escalation Manager (#55).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?q` | string (≥ 2 chars) | — | Full-text search on `csm_escalation.title` (ILIKE) and `institution.name` (ILIKE); 300ms debounce; min 2 chars |
| `?severity` | `p1`, `p2`, `p3` (comma-sep) | `all` | Filter by severity |
| `?status` | `open`, `in_progress`, `pending_institution`, `pending_division`, `resolved`, `closed` (comma-sep) | `open,in_progress,pending_institution,pending_division` | Filter by status (default excludes resolved/closed) |
| `?assigned_to` | user_id | `all` | Filter to one escalation manager |
| `?type` | `school`, `college`, `coaching`, `group` | `all` | Filter by institution type |
| `?account_at_risk` | `1` | — | Show only account_at_risk=true |
| `?has_support_tickets` | `1` | — | Show only escalations with linked tickets |
| `?arr_min` | integer (₹) | — | Minimum ARR at risk |
| `?sort` | `severity_asc`, `days_open_desc`, `arr_desc`, `opened_at_desc`, `commit_date_asc` | `severity_asc` | Sort order |
| `?page` | integer | `1` | Page number |
| `?show_closed` | `1` | — | Include RESOLVED + CLOSED in results |
| `?nocache` | `true` | — | Bypass Memcached (CSM + Escalation Manager only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| KPI strip | `?part=kpi` | Page load + auto-refresh every 60s |
| Escalation table | `?part=table` | Page load + filter change + sort + page |
| Resolution trend chart | `?part=trend_chart` | Page load |
| ARR at risk summary | `?part=arr_at_risk` | Page load + auto-refresh every 5 min |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Escalation Console   [+ Create Escalation]                          │
├──────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (4 tiles)                                                 │
├──────────────────────────────────────────────────────────────────────┤
│  SEARCH BAR                                                          │
│  [🔍 Search escalation title or institution name...]                  │
├──────────────────────────────────────────────────────────────────────┤
│  FILTERS                                                             │
│  Severity: [All ▼]  Status: [Open/Active ▼]  Assigned: [All ▼]      │
│  Type: [All ▼]  [Account at Risk □]  [Has Tickets □]  [Clear]        │
├──────────────────────────────────────────────────────────────────────┤
│  SORT + ROW COUNT: Sort: [Severity ▲]   Showing 28 open escalations  │
├──────────────────────────────────────────────────────────────────────┤
│  ESCALATION TABLE                                                    │
├──────────────────────────────────────────────────────────────────────┤
│  PAGINATION                                                          │
├───────────────────────────────┬──────────────────────────────────────┤
│  RESOLUTION TREND CHART       │  ARR AT RISK SUMMARY                │
└───────────────────────────────┴──────────────────────────────────────┘
```

---

## KPI Strip (4 tiles)

```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ 28              │ │ 4               │ │ ₹8.2Cr          │ │ 76%             │
│ Open Escalations│ │ P1 CRITICAL     │ │ Total ARR       │ │ On-time         │
│                 │ │ (need action    │ │ at Risk         │ │ Resolution Rate │
│ 4P1 · 11P2 · 13P3│ │ today)          │ │ (account_at_risk│ │ (last 90 days)  │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
```

- **Open Escalations:** All status NOT IN ('RESOLVED','CLOSED'). Sub-label shows severity breakdown.
- **P1 CRITICAL:** Count where severity='P1_CRITICAL' and status NOT RESOLVED/CLOSED. Red tile if > 0.
- **ARR at Risk:** Sum of `arr_at_risk_paise` where `account_at_risk=true` and not resolved. Formatted ₹X.XCr.
- **On-time Resolution Rate:** Percentage of escalations in last 90 days resolved within SLA commit date. Green if ≥ 85%, amber if 70–84%, red if < 70%.

---

## Escalation Table

| Column | Sortable | Description |
|---|---|---|
| Severity | Yes | P1=red badge, P2=orange badge, P3=amber badge |
| Title | No | Truncated to 60 chars; full title on hover tooltip |
| Institution | No | Name (link → J-03 escalations tab) + type badge |
| Health | No | Score + tier badge (from `csm_institution_health`) |
| ARR at Risk | Yes | ₹ value or "—". Flame icon if `account_at_risk=true` |
| Status | No | Inline status dropdown (Escalation Manager + CSM only); others see badge |
| Assigned To | No | Escalation Manager avatar + name |
| Linked Tickets | No | Count with link icon ("3 tickets" → opens ticket list tooltip) |
| Commit SLA | No | Countdown to `commit_sla_at`: "3h 12m" · "14h left" · "BREACHED" in red. Tick icon if manually set `commit_date` is before `commit_sla_at`. Hidden on RESOLVED/CLOSED rows |
| Resolve SLA | No | Countdown to `resolve_sla_at`: same format. "BREACHED" shown in red with strikethrough elapsed time. Hidden on RESOLVED/CLOSED rows |
| Commit Date | Yes | Manually set date or "—"; amber badge "due today"; red if past and not RESOLVED |
| Days Open | Yes | Integer; red if P1 > 1d, P2 > 3d, P3 > 7d |
| Actions | No | [View Details] [Resolve] (Escalation Manager only) |

**Pagination:** 25 rows per page. Page size fixed (no per-page selector). Pagination controls re-render with the `?part=table` partial.

**Row click:** Opens Escalation Detail Drawer (right-side panel, HTMX-loaded).

**Status inline dropdown (Escalation Manager + CSM only):**
- Dropdown replaces status badge on hover
- HTMX POST to `/csm/escalations/{id}/status/`
- Transitions: OPEN → IN_PROGRESS → PENDING_INSTITUTION | PENDING_DIVISION → RESOLVED → CLOSED
- Transition to RESOLVED: requires resolution text (modal)
- Transition to CLOSED: requires institution confirmation note

**Colour coding:**
- P1 rows: background red-50 with left border red-500
- P2 rows: background orange-50 with left border orange-400
- Rows past commit date: additional striped pattern on commit date cell
- `account_at_risk=true`: flame icon in red next to institution name

---

## Escalation Detail Drawer

Right-side panel, 480px wide, opens without full page reload.

```
┌──────────────────────────────────────────────────────────────────────┐
│  P1 CRITICAL                              [Close ×]    [Edit]        │
│  "Portal login failure — 400+ students affected"                     │
│  Opened: 18 Mar 2026, 08:42 AM  ·  Day 3                            │
├──────────────────────────────────────────────────────────────────────┤
│  Institution: Delhi Public School (SCHOOL)   Health: 61/100 AT_RISK  │
│  ARR at Risk: ₹2.8L         Account at Risk: Yes  🔴                 │
│  Status: IN_PROGRESS        Assigned: Kartik M. (Escalation Manager) │
│  Commit SLA:  ⏱ BREACHED (P1: 4h · was due 18 Mar 12:42)    🔴     │
│  Resolve SLA: ⏱ BREACHED (P1: 24h · was due 19 Mar 08:42)   🔴     │
│  Commit date (manual): 21 Mar 2026  (overdue by 0 days — due today)  │
├──────────────────────────────────────────────────────────────────────┤
│  DESCRIPTION                                                         │
│  Login failures starting 18 Mar 08:30 IST. JWT token expiry         │
│  mismatch after secret rotation. ~420 institution users locked out.  │
│  Student access blocked. Exam scheduled for 19 Mar at risk.         │
├──────────────────────────────────────────────────────────────────────┤
│  ROOT CAUSE                          [Edit]                          │
│  JWT secret rotated by Security Eng on 17 Mar without clearing      │
│  portal-side JWT verification cache. Cache TTL = 24h, so users      │
│  received cached "invalid token" rejections until cache expired.     │
├──────────────────────────────────────────────────────────────────────┤
│  RESOLUTION                          [Edit]                          │
│  Cache manually cleared 18 Mar 11:20 IST. New JWT secret propagated. │
│  Added cache-invalidation step to secret rotation runbook (Div-C).   │
├──────────────────────────────────────────────────────────────────────┤
│  LINKED SUPPORT TICKETS (2)                                          │
│  SUP-20260318-001234  L3  IN_PROGRESS  [View ↗]                      │
│  SUP-20260318-001241  L2  RESOLVED     [View ↗]                      │
│  [Link another ticket]                                               │
├──────────────────────────────────────────────────────────────────────┤
│  CROSS-DIVISION COORDINATION                                         │
│  ● Engineering · Backend Eng  RESOLVED  "Cache cleared 18 Mar 11:20" │
│  ● Division I · L3 Eng        RESOLVED  "Root ticket resolved"       │
│  [+ Add coordination note]                                           │
├──────────────────────────────────────────────────────────────────────┤
│  ACTIONS (Escalation Manager + CSM)                                  │
│  [Update Status ▼]   [Update Commit Date]   [Escalate to CSM]        │
│  [Mark Resolved →]                                                   │
└──────────────────────────────────────────────────────────────────────┘
```

### Escalate to CSM action

**[Escalate to CSM]** — visible to Escalation Manager (#55) only. Used when the escalation requires the account's assigned CSM to take hands-on account-management action (beyond the Escalation Manager's technical resolution scope — e.g., relationship salvage, expedited renewal conversation, executive contact).

Clicking opens a small inline confirmation:
```
Flag this escalation for immediate CSM attention?
Note for CSM: [____________________________________________]
[Cancel]  [Notify CSM]
```
POST to `/csm/escalations/{id}/notify_csm/`. Sends an in-app notification to assigned CSM: "Escalation Manager flagged [Title] for your immediate attention: [note]." Sets no status change — purely a notification action. The [Escalate to CSM] button becomes "CSM Notified (N min ago)" after firing and cannot be re-triggered for 60 min.

### Edit fields (Escalation Manager + CSM only)

Inline edit buttons for: root_cause, resolution, commit_date, assigned_to.

Each edit opens a small textarea/input below the field (not a separate modal). Save via [✓] button → HTMX PATCH to `/csm/escalations/{id}/`.

### Link support ticket

Input field searching `support_ticket.ticket_number` prefix. Returns matching open tickets. Selected tickets appended to `support_ticket_ids[]`. PATCH to `/csm/escalations/{id}/link_tickets/`.

### Add cross-division coordination note

```
Division:  [Engineering              ▼]
Contact:   [Backend Engineer         ]
Status:    [RESOLVED                 ▼]  (PENDING / IN_PROGRESS / RESOLVED / BLOCKED)
Note:      [Cache cleared 18 Mar ... ]

[Save Note]
```

PATCH to `/csm/escalations/{id}/coordination/`. Appends to `cross_division_notes` JSONB array.

### Mark Resolved action

```
┌────────────────────────────────────────────────────────┐
│  Resolve Escalation                                    │
├────────────────────────────────────────────────────────┤
│  Resolution summary*                                   │
│  [Describe how this was resolved for the institution ] │
│                                                        │
│  Institution confirmed:  ○ Yes  ○ No  ○ Pending       │
│                                                        │
│  [Cancel]              [Mark as Resolved]              │
└────────────────────────────────────────────────────────┘
```

POST to `/csm/escalations/{id}/resolve/`. Sets `resolved_at = now()` and `status = RESOLVED`.
If `account_at_risk = true`: sends in-app notification to assigned CSM: "Escalation resolved for [Institution] — please confirm ARR is no longer at risk."

---

## Create Escalation Drawer (from console)

Same form as J-03 Create Escalation Drawer. Institution field is required (searchable dropdown of all 2,050 institutions). No pre-fill.

[+ Create Escalation] button visible to CSM (#53) and Escalation Manager (#55) only.

---

## Resolution Trend Chart

Line chart showing weekly escalation resolution metrics over last 90 days.

Three lines:
- P1 opened (red)
- P2 opened (orange)
- All resolved (green)

Y-axis: count per week. X-axis: week labels.

Hover: tooltip shows week + counts.

Note: helps Escalation Manager identify if P1 volume is trending up (infra instability) or if resolution rate is deteriorating.

---

## ARR at Risk Summary

Right panel below table:

```
┌──────────────────────────────────────────────┐
│  ARR at Risk (account_at_risk = true)         │
│                                              │
│  ₹8.2Cr total across 4 institutions          │
│                                              │
│  Delhi Coaching Hub   ₹12.4L   P1  Day 3    │
│  Sunrise Academy      ₹2.8L    P2  Day 7    │
│  Excel Institute      ₹6.2L    P1  Day 1    │
│  Victory College      ₹1.4L    P2  Day 12   │
└──────────────────────────────────────────────┘
```

Each row links to the escalation detail drawer. Sorted by ARR desc. Updates every 5 min via HTMX.

If no account_at_risk escalations: "No accounts are currently flagged as at-risk due to escalations." (green checkmark).

---

## Empty States

| Condition | Message |
|---|---|
| No open escalations | "No open escalations. Portfolio is clean." with shield-check icon |
| Filter returns no results | "No escalations match the current filters." with [Clear Filters] button |
| No P1 open | P1 KPI tile shows "0" with green background |

---

## Toast Messages

| Action | Toast |
|---|---|
| Status updated | "Escalation status updated to [STATUS]." (green) |
| Escalation resolved | "Escalation resolved. Assigned CSM notified." (green) |
| Escalation closed | "Escalation closed." (grey) |
| Ticket linked | "Support ticket SUP-XXXX linked." (blue) |
| Coordination note added | "Coordination note added." (blue) |
| Escalation created | "P[N] escalation created and assigned to [Name]." (amber/red based on severity) |
| CSM notified (Escalate to CSM) | "CSM [Name] notified of urgent escalation attention needed." (amber) |

---

## Export CSV

Available to CSM (#53) and CS Analyst (#93) only via `GET /csm/escalations/?export=csv` (URL parameter triggers download).

Filename: `eduforge_escalations_YYYY-MM-DD.csv`

Columns: escalation_id, institution_id, institution_name, institution_type, severity, status, title, opened_by, assigned_to, opened_at, commit_date, resolved_at, closed_at, commit_sla_at, resolve_sla_at, commit_sla_breached, resolve_sla_breached, account_at_risk, arr_at_risk_paise, churn_reason, linked_ticket_count, days_open

Export applies current `?severity`, `?status`, `?assigned_to`, and `?show_closed` filters. Async (email link) for > 500 rows; inline download for ≤ 500 rows.

---

## Notifications Generated by This Page

| Action | Notification sent to | Channel |
|---|---|---|
| Escalation created | Assigned Escalation Manager | In-app + Email |
| Escalation status → RESOLVED | Assigned CSM + AM | In-app |
| Escalation resolved with `account_at_risk=true` | CSM | In-app + Email |
| Commit date passes with status not RESOLVED | Assigned Escalation Manager + CSM | In-app |
| Escalation Manager flags for CSM attention (`notify_csm`) | Assigned CSM (#53) | In-app |

---

## Role-Based UI Visibility Summary

| Element | 53 CSM | 54 AM | 55 Escalation | 56 Renewal | 93 Analyst | 94 ISM |
|---|---|---|---|---|---|---|
| Full table | Yes | Read | Yes | No access | Read | Read |
| Create escalation | Yes | No | Yes | No | No | No |
| Status dropdown (inline) | Yes | No | Yes | No | No | No |
| Resolve action | Yes | No | Yes | No | No | No |
| Edit root_cause/resolution | Yes | No | Yes | No | No | No |
| Link support tickets | Yes | No | Yes | No | No | No |
| Add coordination note | Yes | No | Yes | No | No | No |
| Escalate to CSM (notify_csm) | No | No | Yes | No | No | No |
| ARR at risk panel | Yes | Yes | Yes | No | Yes | No |
| Resolution trend chart | Yes | No | Yes | No | Yes | No |
| [?nocache=true] | Yes | No | Yes | No | No | No |
