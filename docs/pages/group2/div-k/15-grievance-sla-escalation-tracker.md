# 15 — Grievance SLA & Escalation Tracker

> **URL:** `/group/welfare/grievances/escalations/`
> **File:** `15-grievance-sla-escalation-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Grievance Redressal Officer (Role 92, G3)

---

## 1. Purpose

Dedicated SLA monitoring dashboard and escalation management page for grievances. While the Grievance Register shows all grievances, this page specifically focuses on: (a) grievances at risk of breaching SLA, (b) grievances that have already breached SLA, (c) grievances escalated to CEO/COO, and (d) grievances that have been stagnant (no update in last 5 days). The Grievance Redressal Officer uses this daily to action the most critical items — send reminders to department heads, initiate escalations, and draft formal responses to complainants.

SLA rules in force across all branches:
- **Acknowledgment SLA:** Within 7 days of complaint receipt.
- **Resolution SLA:** Within 30 days of complaint receipt.
- **CEO-COO Escalated SLA:** Must be resolved within 7 days of escalation.

The page surfaces only at-risk and breached records — it is an operational action queue, not a historical archive. Each row demands a response: send a reminder, force an escalation, or record a resolution. The Grievance Redressal Officer reviews this page every morning and must clear all red items before end of business day. Scale: 20–50 branches · 10–200 grievances active at any time across the group.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Grievance Redressal Officer | G3 | Full — all sections, all actions including force-escalate and send-reminder | Primary owner |
| Group COO | G4 | View — CEO-COO escalated items section only; read-only | Cannot send reminders or escalate |
| Group Chairman / CEO | G5 | View — CEO-COO escalated items only via governance report | Not this URL directly |
| Branch Grievance Coordinator | G2 | View — own branch rows only; no escalation actions | Branch-scoped read-only |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('grievance_officer', 'coo')` with branch-scope filter applied for G2.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Grievance Management  ›  SLA & Escalation Tracker
```

### 3.2 Page Header
```
Grievance SLA & Escalation Tracker                  [Export Breach Report ↓]  [Settings ⚙]
[Group Name] — Grievance Redressal Officer · Last refreshed: [timestamp]
AY [current academic year]  ·  [N] At-Risk Grievances  ·  [N] SLA Breached  ·  [N] CEO-COO Escalated Open
```

### 3.3 Alert Banner (conditional — items requiring same-day action)

| Condition | Banner Text | Severity |
|---|---|---|
| Any grievance > 90 days unresolved | "[N] grievance(s) have exceeded 90 days without resolution. Immediate escalation to COO required." | Red |
| CEO-COO escalated grievance > 7 days unresolved post-escalation | "Escalated grievance [ID] has been with CEO-COO for [N] days without resolution — breach of 7-day escalated SLA." | Red |
| Acknowledgment SLA breached (> 7 days unacknowledged) | "[N] grievance(s) have not been acknowledged within the 7-day SLA. Action required immediately." | Red |
| Stagnant grievances (no update > 5 days) | "[N] grievance(s) have had no activity for more than 5 days. Send reminders to assigned officers." | Amber |
| Grievances approaching 30-day resolution deadline (25–30 days) | "[N] grievance(s) are within 5 days of breaching the 30-day resolution SLA." | Amber |

Max 5 alerts visible. Each alert text is a link routing to the corresponding filtered table view. "View full grievance log → Grievance Register" always shown below alerts.

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| SLA Breach Rate | % of closed grievances this month that missed the 30-day SLA | Green < 5% · Yellow 5–15% · Red > 15% | → Section 5.1 filtered to breached |
| Acknowledgment Pending > 7 Days | Count of grievances unacknowledged past the 7-day SLA | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.1 filtered to ack-breached |
| Resolution Pending > 30 Days | Count of open grievances past the 30-day resolution SLA | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.1 filtered to resolution-breached |
| Stagnant (No Update > 5 Days) | Count of grievances with no status change or note for over 5 days | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.1 filtered to stagnant |
| CEO-COO Escalated Open | Count of currently open grievances at CEO/COO escalation level | Green = 0 · Yellow 1–2 · Red > 2 | → Section 5.2 |
| Branches with SLA Breach This Month | Branches that have at least one resolution SLA breach in current month | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.3 |
| Reminders Sent This Week | Count of reminder notifications dispatched via this page this week | Blue always (informational) | — |
| Avg Days Open (Open Grievances) | Mean age in days of all currently open grievances across all branches | Green < 10d · Yellow 10–20d · Red > 20d | → Section 5.1 sorted by age |

**HTMX:** `hx-trigger="every 3m"` → All 8 KPI cards auto-refresh silently.

---

## 5. Sections

### 5.1 SLA Tracker Table (Primary Table)

> All grievances that are: SLA at-risk, SLA breached, stagnant, or CEO-COO escalated. Normal on-track grievances do not appear here — they remain in the Grievance Register.

**Search:** Grievance ID, complainant name, branch name, assigned officer name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Category | Multi-select | Academic / Fee / Staff Conduct / Facilities / Transport / Hostel / Safety / Other |
| Stage | Checkbox | Filed / Acknowledged / Under Review / Pending Response / Escalated / Resolved |
| SLA Status | Radio | All · Acknowledgment Breached · Resolution Breached · At Risk (25–30 days) · On Track |
| Escalation Level | Checkbox | Branch / Group / CEO-COO |
| Stagnant Only | Toggle | Show only grievances with no update > 5 days |
| Days Open | Radio | All · < 10 days · 10–20 days · 20–30 days · > 30 days |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Grievance ID | ✅ | System-generated; link → `sla-breach-detail` drawer |
| Branch | ✅ | Branch name |
| Category | ✅ | Colour-coded category badge |
| Complainant | ✅ | Name (anonymised to initials for non-officer roles) |
| Stage | ✅ | Stage badge: Filed (Grey) · Acknowledged (Blue) · Under Review (Amber) · Pending Response (Orange) · Escalated (Red) · Resolved (Green) |
| Days Open | ✅ | Number; Red > 30 · Orange 25–30 · Yellow 15–24 · Green < 15 |
| Acknowledgment SLA | ❌ | Icon: ✅ Acknowledged within 7d · ⚠ At risk (5–7d, unacknowledged) · ❌ Breached (> 7d, unacknowledged) |
| Resolution SLA | ❌ | Icon: ✅ On track (< 25d) · ⚠ At risk (25–30d open) · ❌ Breached (> 30d open, unresolved) |
| Last Update | ✅ | Days since last note/status change; Red if > 5d (stagnant) |
| Assigned To | ✅ | Officer name |
| Escalation Level | ✅ | Badge: Branch (Grey) · Group (Amber) · CEO-COO (Red) |
| Actions | ❌ | View · Send Reminder · Force Escalate |

**Default sort:** Resolution SLA (Breached first, then At Risk), then Days Open descending.
**Pagination:** Server-side · 25/page.

---

### 5.2 CEO-COO Escalated Grievances Panel

> Dedicated view of all grievances currently at CEO/COO escalation level — highest priority items.

**Display:** Card list (not table) — each card shows full context at a glance for rapid action.

**Each card shows:**
- Grievance ID · Branch · Category badge
- Complainant name · Days since escalation to CEO-COO level
- Escalation reason (brief text)
- Resolution SLA countdown: "[N] days remaining" or "BREACHED — [N] days overdue" (Red)
- Assigned officer at CEO-COO level
- Last update note (date + text snippet)
- Actions: [View Full Record] [Update Resolution] [Draft Response]

**Default sort:** Days since escalation descending (longest-pending first).

"View all CEO-COO escalated history →" opens a paginated list modal.

---

### 5.3 SLA Performance by Branch

> Branch-level breakdown of SLA compliance for the current month and last 3 months.

**Display:** Bar chart — branches on X-axis, SLA compliance % on Y-axis. Grouped bars: Acknowledgment SLA % (Blue) and Resolution SLA % (Green). Branches below 85% threshold highlighted with Red border on their bar group.

**Below chart:** Summary table:
| Column | Notes |
|---|---|
| Branch | Branch name |
| Grievances This Month | Total count |
| Ack SLA Met % | % acknowledged within 7 days |
| Resolution SLA Met % | % resolved within 30 days |
| Avg Days Open | Mean days across all grievances this month |
| Trend | Up ↑ / Down ↓ / Stable → vs last month |

**Pagination:** Server-side · 25/page.

---

### 5.4 Monthly Breach Trend Chart

> 12-month rolling line chart showing SLA breach rate trend across all branches.

**Chart:** Line chart (Recharts-compatible JSON from API).
- X-axis: Month labels (last 12 months).
- Y-axis: Breach rate % (0–100).
- Two lines: Acknowledgment Breach Rate (Blue dashed) and Resolution Breach Rate (Red solid).
- Reference line at 10% (policy target threshold — Amber dashed).
- Tooltip: Month · Ack breach % · Res breach % · Total grievances that month.

**Below chart:** Three-number summary: Best month · Worst month · Current month vs same period last year.

---

### 5.5 Grievance Stage Funnel

> Funnel visualisation of all currently open grievances by stage — identifies where grievances are getting stuck.

**Display:** Horizontal funnel (SVG rendered from API data).
- Stages (left to right): Filed → Acknowledged → Under Review → Pending Response → Escalated → Resolved.
- Width of each band proportional to count.
- Tooltip: Stage name · Count · Avg days in this stage.

**Below funnel:** Text insight: "Most grievances stall at [stage name] — avg [N] days. [N] grievances have been in this stage for > 10 days."

---

## 6. Drawers / Modals

### 6.1 Drawer: `sla-breach-detail`
- **Trigger:** Grievance ID link in Section 5.1 table
- **Width:** 560px
- **Tabs:** Overview · SLA Timeline · Activity Log · Assigned Officers

**Overview tab:**
| Field | Notes |
|---|---|
| Grievance ID | System-generated, read-only |
| Branch | Branch name |
| Category | Category badge |
| Sub-category | If applicable |
| Date Filed | Date the grievance was originally submitted |
| Complainant | Full name (role-gated: visible to G3+ only) |
| Complainant Type | Student / Parent / Staff / Anonymous |
| Current Stage | Stage badge with date entered |
| Assigned To | Current assigned officer name and contact |
| Escalation Level | Branch / Group / CEO-COO badge |
| Days Open | With SLA colour coding |
| Acknowledgment SLA | ✅ / ⚠ / ❌ icon + date acknowledged or "Not yet acknowledged" |
| Resolution SLA | ✅ / ⚠ / ❌ icon + days remaining or days overdue |
| Last Update | Date and synopsis of most recent activity |
| Description | Full grievance text (read-only) |

**SLA Timeline tab:**
- Visual timeline of key SLA events:
  - Date Filed → Acknowledgment Date (or Overdue marker) → Latest Activity → Resolution Date (or Projected breach date)
- Each event node: date, action taken, by whom
- Red markers for any SLA breach point
- Green markers for SLA met points

**Activity Log tab:**
- Chronological list of all status changes and notes:
  - Date · Action (Status change / Note added / Reminder sent / Escalated) · Performed By · Note text
- Paginated if > 20 entries

**Assigned Officers tab:**
- Officer name · Role · Branch · Date Assigned · Contact (phone/email)
- Reassign button (G3 only) → opens inline reassignment form

**Footer actions (G3 only):**
- [Send Reminder] → opens `send-reminder` drawer prefilled with this grievance
- [Force Escalate] → opens `force-escalate` drawer prefilled with this grievance
- [Mark Resolved] → confirm dialog → PATCH resolution endpoint

---

### 6.2 Drawer: `send-reminder`
- **Trigger:** "Send Reminder" action button in table row or drawer footer
- **Width:** 400px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Grievance ID | Read-only pre-filled | — |
| Branch | Read-only pre-filled | — |
| Assigned Officer | Read-only pre-filled (name + email) | — |
| Reminder Type | Radio | Action Required (default) / Final Warning / Acknowledgment Reminder / Resolution Deadline |
| Additional Deadline | Date picker | Must be today or future; required for "Final Warning" type |
| Message to Officer | Textarea · max 500 chars | Required · min 20 chars |
| CC to Branch Head | Toggle | Default: ON |
| CC to Group Grievance Head | Toggle | Default: OFF |
| Send Method | Checkbox group | Email (always checked, disabled) · Portal notification (default ON) · SMS (optional) |

**Validation:**
- Message field required.
- "Final Warning" type requires Additional Deadline date.
- Cannot send duplicate reminder to same officer on the same grievance within 24 hours — system shows warning: "A reminder was already sent to [Name] for this grievance [N] hours ago. Send again?" with Confirm / Cancel.

**Footer:** [Cancel] [Send Reminder →]

**On submit:** POST to reminder endpoint · drawer closes · toast success · grievance row "Last Update" refreshes in-place via HTMX.

---

### 6.3 Drawer: `force-escalate`
- **Trigger:** "Force Escalate" action button in table row or drawer footer
- **Width:** 440px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Grievance ID | Read-only pre-filled | — |
| Branch | Read-only pre-filled | — |
| Current Escalation Level | Read-only pre-filled | — |
| Escalate To | Radio | Group Level · CEO-COO Level | Cannot de-escalate; must escalate upward |
| Reason for Force Escalation | Select | SLA Breach · Stagnant > 5 Days · Complainant Dissatisfaction · Severity Upgrade · Management Directive |
| Escalation Note | Textarea · max 600 chars | Required · min 30 chars |
| Assign To | Searchable dropdown | Officers at the target escalation level |
| New Resolution Deadline | Date picker | Required; auto-suggests today + SLA days for level (7 days for CEO-COO) |
| Notify Complainant | Toggle | Default: ON — auto-generates acknowledgment letter draft |
| Complainant Notification Message | Textarea · max 400 chars | Visible and required if "Notify Complainant" is ON |

**Validation:**
- Cannot escalate a grievance already at CEO-COO level (button hidden for those rows).
- Escalation Note minimum 30 characters enforced client-side and server-side.
- New Resolution Deadline must be after today.
- Assign To is required.

**Confirmation step:** After clicking "Escalate", show a summary panel within the drawer before final submission:
- Summary: Grievance ID · Branch · Escalating to · Assigned to · New deadline · Notify complainant: Yes/No
- Buttons: [Back — Edit] [Confirm Escalation →]

**Footer:** [Cancel] [Escalate →]

**On submit:** POST to escalation endpoint · grievance row updates badge to new escalation level · toast warning notification · KPI card "CEO-COO Escalated Open" increments in-place.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reminder sent successfully | "Reminder sent to [Officer Name] for Grievance [ID]." | Success | 4s |
| Reminder blocked — too soon | "A reminder was already sent for this grievance within the last 24 hours." | Warning | 5s |
| Grievance escalated to Group level | "Grievance [ID] has been escalated to Group level and assigned to [Officer Name]." | Warning | 6s |
| Grievance escalated to CEO-COO | "Grievance [ID] has been escalated to CEO-COO level. Complainant notified." | Warning | 6s |
| Grievance marked resolved | "Grievance [ID] marked as resolved. SLA compliance recorded." | Success | 4s |
| Breach report exported | "Breach report is being prepared. Download will begin shortly." | Info | 4s |
| SLA detail drawer opened | — (no toast; silent navigation) | — | — |
| Duplicate escalation prevented | "Grievance [ID] is already at [Level] escalation level. Cannot escalate further." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No SLA breaches or at-risk grievances | "All Grievances Within SLA" | "No grievances are currently breaching or at risk of breaching acknowledgment or resolution SLAs." | — |
| No CEO-COO escalated grievances | "No CEO-COO Escalations Open" | "There are currently no grievances escalated to the CEO or COO level." | — |
| No stagnant grievances | "No Stagnant Grievances" | "All open grievances have had activity within the last 5 days." | — |
| Search returns no results | "No Grievances Found" | "No grievances match your search terms or applied filters." | [Clear Filters] |
| No grievances at all (fresh system) | "No Grievance Data Yet" | "No grievances have been registered in the system. The SLA tracker will populate when grievances are filed." | — |
| No breach history (monthly chart) | "No Breach History Available" | "Not enough historical data to show a monthly trend. Data will appear after the first full month." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + main SLA table (15 rows × 12 columns) + CEO-COO escalated cards panel (3 card skeletons) + branch performance table + chart areas |
| Table filter/search | Inline skeleton rows (8 rows × 12 columns) |
| KPI auto-refresh (every 3m) | Shimmer on individual card values only; card labels and icons preserved |
| Section 5.2 CEO-COO panel load | 3 card skeletons with animated gradient; each card 80px tall |
| SLA breach detail drawer open | 560px drawer skeleton with timeline skeleton (5 nodes) and tab bar |
| Send reminder drawer open | 400px drawer skeleton with 6 field skeletons |
| Force escalate drawer open | 440px drawer skeleton with 8 field skeletons |
| Monthly trend chart load | Chart area grey rectangle with shimmer gradient (full-width, 280px tall) |
| Stage funnel load | Funnel skeleton — 6 horizontal grey bands with animated gradient |
| Branch SLA table load | Table skeleton 10 rows × 6 columns |
| Drawer tab switch | Inline content skeleton (tab-specific; 300ms) |

---

## 10. Role-Based UI Visibility

| Element | Grievance Redressal Officer G3 | Group COO G4 | Chairman / CEO G5 | Branch Grievance Coordinator G2 |
|---|---|---|---|---|
| View All Branches SLA Table | ✅ | ❌ (CEO-COO escalated only) | ❌ (CEO-COO escalated only) | Own branch only |
| Send Reminder | ✅ | ❌ | ❌ | ❌ |
| Force Escalate | ✅ | ❌ | ❌ | ❌ |
| Mark Resolved | ✅ | ❌ | ❌ | ❌ |
| View Complainant Name | ✅ | ✅ (escalated items) | ✅ (escalated items) | ❌ (initials only) |
| View Activity Log | ✅ | ✅ (escalated items) | ✅ (escalated items) | Own branch, own cases |
| Export Breach Report | ✅ | ✅ | ✅ | ❌ |
| View SLA Charts | ✅ | ✅ (read-only) | ✅ (read-only) | ❌ |
| Reassign Grievance | ✅ | ❌ | ❌ | ❌ |
| KPI Summary Bar | ✅ (all cards) | ✅ (CEO-COO card only) | ✅ (CEO-COO card only) | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/grievances/sla-tracker/` | JWT (G3+) | Full page data: KPI cards + SLA table + CEO-COO panel |
| GET | `/api/v1/group/{group_id}/welfare/grievances/sla-tracker/kpi-cards/` | JWT (G3+) | KPI auto-refresh payload (8 cards) |
| GET | `/api/v1/group/{group_id}/welfare/grievances/sla-tracker/table/` | JWT (G3+) | SLA table rows; params: `branch_id`, `category`, `stage`, `sla_status`, `escalation_level`, `stagnant`, `days_open_range`, `q`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/grievances/sla-tracker/ceo-coo-panel/` | JWT (G3+) | CEO-COO escalated cards panel |
| GET | `/api/v1/group/{group_id}/welfare/grievances/sla-tracker/branch-performance/` | JWT (G3+) | Branch-level SLA compliance table data |
| GET | `/api/v1/group/{group_id}/welfare/grievances/sla-tracker/breach-trend/` | JWT (G3+) | 12-month breach rate time series |
| GET | `/api/v1/group/{group_id}/welfare/grievances/sla-tracker/stage-funnel/` | JWT (G3+) | Stage funnel count data |
| GET | `/api/v1/group/{group_id}/welfare/grievances/{grievance_id}/sla-detail/` | JWT (G3+) | Single grievance SLA detail drawer payload |
| POST | `/api/v1/group/{group_id}/welfare/grievances/{grievance_id}/send-reminder/` | JWT (G3) | Send reminder notification to assigned officer |
| POST | `/api/v1/group/{group_id}/welfare/grievances/{grievance_id}/escalate/` | JWT (G3) | Force-escalate grievance to next level |
| PATCH | `/api/v1/group/{group_id}/welfare/grievances/{grievance_id}/resolve/` | JWT (G3) | Mark grievance as resolved |
| GET | `/api/v1/group/{group_id}/welfare/grievances/sla-tracker/export/` | JWT (G3+) | Async breach report export (CSV/XLSX) |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 3m` | GET `.../sla-tracker/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| SLA table search | `input delay:300ms` | GET `.../sla-tracker/table/?q={val}` | `#sla-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../sla-tracker/table/?{filters}` | `#sla-table-section` | `innerHTML` |
| Stagnant toggle | `change` | GET `.../sla-tracker/table/?stagnant=true` | `#sla-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../sla-tracker/table/?page={n}` | `#sla-table-section` | `innerHTML` |
| Open SLA detail drawer | `click` on Grievance ID | GET `.../grievances/{id}/sla-detail/` | `#drawer-body` | `innerHTML` |
| Send reminder submit | `click` | POST `.../grievances/{id}/send-reminder/` | `#grievance-row-{id}` | `outerHTML` |
| Force escalate confirm | `click` (confirmation step) | POST `.../grievances/{id}/escalate/` | `#grievance-row-{id}` | `outerHTML` |
| Mark resolved | `click` | PATCH `.../grievances/{id}/resolve/` | `#grievance-row-{id}` | `outerHTML` |
| CEO-COO panel refresh | `every 3m` | GET `.../sla-tracker/ceo-coo-panel/` | `#ceo-coo-panel` | `innerHTML` |
| Stage funnel load | `load` | GET `.../sla-tracker/stage-funnel/` | `#stage-funnel` | `innerHTML` |
| Branch performance table load | `load` | GET `.../sla-tracker/branch-performance/` | `#branch-perf-section` | `innerHTML` |
| Breach trend chart load | `load` | GET `.../sla-tracker/breach-trend/` | `#breach-trend-chart` | `innerHTML` |
| Drawer tab switch | `click` on tab | GET `.../grievances/{id}/sla-detail/?tab={name}` | `#drawer-tab-content` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
