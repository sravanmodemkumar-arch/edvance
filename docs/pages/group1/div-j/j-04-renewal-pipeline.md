# J-04 — Renewal Pipeline

**Route:** `GET /csm/renewals/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side Kanban data
**Primary roles:** Account Manager (#54), Renewal Executive (#56)
**Also sees:** CSM (#53) full access, Escalation Manager (#55) read-only, CS Analyst (#93) read + export

---

## Purpose

Revenue retention command centre. All upcoming and in-flight renewals across 2,050 institutions in one view. The AM and Renewal Executive own this page daily — tracking which deals need a nudge, which are at risk of churn, and how the quarter's ARR looks. The CSM uses it for weekly pipeline reviews with the team.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| ARR summary strip | `csm_renewal` aggregated by stage + period | 5 min |
| Kanban columns | `csm_renewal` JOIN `institution` JOIN `csm_institution_health` grouped by stage | 5 min |
| List view table | Same + pagination | 5 min |
| Revenue waterfall chart | `csm_renewal` closed in current quarter (won + churned) | 10 min |
| Churn risk breakdown | `csm_institution_health.churn_probability_pct` for at-renewal institutions | 5 min |

Cache key includes all active filter params. `?nocache=true` for CSM (#53) only.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?view` | `kanban`, `list` | `kanban` | Layout toggle |
| `?period` | `this_month`, `next_month`, `this_quarter`, `next_quarter`, `custom` | `this_quarter` | Renewal due window for filtering |
| `?from` | `YYYY-MM-DD` | — | Custom period start |
| `?to` | `YYYY-MM-DD` | — | Custom period end |
| `?am_id` | user_id | `mine` (AM/Renewal Exec see own) | Filter by assigned AM |
| `?stage` | comma-separated stage values | `all` | Filter by stage (list view) |
| `?type` | `school`, `college`, `coaching`, `group` | `all` | Filter by institution type |
| `?arr_min` | integer (₹) | — | Minimum ARR filter |
| `?arr_max` | integer (₹) | — | Maximum ARR filter |
| `?risk` | `high`, `medium`, `low` | `all` | Filter by churn probability: high > 35%, medium 15–35%, low < 15% |
| `?sort` | `renewal_date_asc`, `arr_desc`, `probability_asc`, `institution_name` | `renewal_date_asc` | List view sort |
| `?page` | integer | `1` | List view page |
| `?export` | `csv` | — | Export current filtered renewals (CSM + CS Analyst) |
| `?nocache` | `true` | — | Bypass Memcached (CSM #53 only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| ARR summary strip | `?part=arr_summary` | Page load + filter change |
| Kanban board | `?part=kanban` | View = kanban + filter change |
| List table + pagination | `?part=list_table` | View = list + filter change + sort + page |
| Revenue waterfall chart | `?part=waterfall` | Page load |
| Churn risk breakdown | `?part=churn_risk` | Page load |
| Stage update (inline) | POST `/csm/renewals/{id}/stage/` | Stage dropdown change on card |

---

## Page Layout

```
┌───────────────────────────────────────────────────────────────────┐
│  Renewal Pipeline    Period: [This Quarter ▼]   AM: [Mine ▼]      │
│  Type: [All ▼]  Risk: [All ▼]  ARR: [₹___ – ₹___]  [Apply]       │
│  [Kanban ■] [List ☐]                              [Export CSV]    │
├───────────────────────────────────────────────────────────────────┤
│  ARR SUMMARY STRIP                                                │
├───────────────────────────────────────────────────────────────────┤
│  KANBAN BOARD (or LIST TABLE)                                     │
├────────────────────────────┬──────────────────────────────────────┤
│  REVENUE WATERFALL CHART   │  CHURN RISK BREAKDOWN               │
└────────────────────────────┴──────────────────────────────────────┘
```

---

## ARR Summary Strip

6 tiles:

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ ₹14.2Cr      │ │ ₹4.1Cr       │ │ ₹9.6Cr       │ │ 72%          │ │ ₹1.8Cr       │ │ ₹0.4Cr       │
│ Total ARR    │ │ ARR Committed│ │ ARR at Risk  │ │ Forecast GRR │ │ Expansion    │ │ Churn (closed│
│ in period    │ │ (Q1 2026)    │ │ (not committed│ │ (committed/  │ │ ARR (this Q) │ │ this Q so far│
│              │ │              │ │ + at-risk inst│ │ total due)   │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

- **Total ARR in period:** Sum of `arr_value_paise` for renewals in selected period window
- **ARR Committed:** Sum where stage IN ('COMMITTED', 'RENEWED')
- **ARR at Risk:** Sum where stage NOT IN ('COMMITTED', 'RENEWED', 'CHURNED') AND churn_probability_pct > 35%
- **Forecast GRR:** ARR_committed / ARR_total × 100 — green if ≥ 85%, amber if 70–84%, red if < 70%
- **Expansion ARR:** Sum of `expansion_arr_paise` for EXPANSION renewals in period
- **Churn (closed):** Sum where stage = 'CHURNED' and `lost_at` in current period

---

## Kanban Board View

7 columns, one per stage. Horizontal scroll for smaller screens.

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ IDENTIFIED   │  │ OUTREACH     │  │ QUOTE SENT   │  │ NEGOTIATING  │  │ COMMITTED    │  │  RENEWED     │  │  CHURNED     │
│ ₹3.2Cr (12) │  │ SENT         │  │ ₹4.1Cr (9)  │  │ ₹2.8Cr (7)  │  │ ₹4.1Cr (14) │  │  ₹6.8Cr (23) │  │  ₹0.4Cr (3)  │
│              │  │ ₹1.8Cr (6)  │  │              │  │              │  │              │  │              │  │              │
│ [card]       │  │ [card]       │  │ [card]       │  │ [card]       │  │ [card]       │  │ [card]       │  │ [card]       │
│ [card]       │  │ [card]       │  │ [card]       │  │ [card]       │  │ [card]       │  │ [card]       │  │ [card]       │
│ ...          │  │ ...          │  │ ...          │  │ ...          │  │ ...          │  │ ...          │  │ ...          │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

Column header: stage name + total ARR + count.

RENEWED and CHURNED columns are "closed" stages — cards are collapsed by default (show 3, [+N more] to expand). No drag-and-drop to/from closed columns.

### Kanban Card

```
┌──────────────────────────────────────┐
│ Delhi Public School           SCHOOL │
│ ₹2.8L · 2,400 seats                  │
│ Due: 5 May (45d)        Prob: 70%    │
│ AM: Ravi S.        [Risk: MEDIUM]    │
│ Last touch: 6d ago                   │
│ [Update Stage ▼]   [View Account →]  │
└──────────────────────────────────────┘
```

Card colour band (left border): green=HEALTHY, amber=AT_RISK, red=CRITICAL or CHURNED_RISK.
Due date: red if ≤ 7 days, amber if 8–30 days.
Risk badge: High (red), Medium (amber), Low (green) — based on churn_probability_pct.

**[Update Stage ▼]** dropdown: lists valid next stages. Constrained by role:
- Renewal Exec (#56): IDENTIFIED → OUTREACH_SENT → QUOTE_SENT → NEGOTIATING → COMMITTED only
- AM (#54) + CSM (#53): all stages including RENEWED and CHURNED

Stage transition to CHURNED: shows churn reason modal (required). Stage to RENEWED: shows confirm dialog with ARR value.

Stage transition to EXPANSION: shows expansion ARR input (required). Creates a note: "Expansion: +₹X.XL".

**[View Account →]** navigates to J-03.

**Card drag-and-drop (AM + CSM only):**
- Implemented using **SortableJS** (`Sortable.create(columnEl, {...})`) — already used elsewhere in portal for similar list reordering. No Alpine.js required; vanilla JS + SortableJS + HTMX pattern.
- On drop: fires `fetch()` POST to `/csm/renewals/{id}/stage/` with new stage; on success triggers `htmx.trigger('#kanban-board', 'renewal-updated')` to refresh column headers (ARR totals).
- CHURNED and RENEWED columns: `group: { put: false }` in SortableJS config to reject incoming drags. Server also validates and returns 400 with `HX-Retarget` error toast if bypassed via API.
- Optimistic UI: card moves immediately; reverts to original column on POST failure with error toast.
- **Responsive behaviour:** Kanban (7 columns) requires ≥ 1,100px viewport width. Below 1,100px, the page automatically switches to list view (`?view=list`) via CSS media query detection: `<script>if(window.innerWidth < 1100 && !url.includes('view=list')){ window.location.search = '?view=list'; }</script>` on page load. A banner informs the user: "Switched to list view — screen too narrow for Kanban. [Switch to Kanban ↗]"

---

## List View

Shown when `?view=list`. Server-side paginated table.

| Column | Sortable | Description |
|---|---|---|
| Institution | Yes | Name (link → J-03) + type badge |
| ARR | Yes | ₹ value |
| Renewal Date | Yes | Date + relative days + colour |
| Stage | No | Dropdown to update stage (inline HTMX) |
| Probability | No | % with colour band |
| Risk | No | High/Medium/Low badge |
| Assigned AM | No | Name |
| Renewal Exec | No | Name |
| Last Touchpoint | Yes | Relative time |
| Health | No | Score + tier badge |
| Actions | No | [View] [Log Touch] |

Default sort: `renewal_date_asc`. 25 rows/page.

---

## Revenue Waterfall Chart

Bar chart (Chart.js) showing ARR composition for current period:

```
₹ Cr
  18 │     ┌───┐
  16 │     │ + │  ┌───┐  ┌───┐
  14 │     │ C │  │ E │  │ R │
  ...│─────│ a │──│ x │──│ e │──── ₹13.8Cr (period end)
   0 │ 14.2│ r │  │ p │  │ n │
     │ (prev│ r │  │ a │  │ e │
     │ ARR) │ y │  │ n │  │ w │
     └──────────────────────────
       Start Churn Expansion Renewed
```

Shows: Starting ARR → Churn (red bar down) → Expansion (green bar up) → Renewed ARR (ending bar).
Hover tooltip: precise ₹ value.

**Note:** Only shows committed/closed data — does not forecast uncommitted renewals.

---

## Churn Risk Breakdown

Two side-by-side displays:

**Donut chart** — 3 segments: High risk (>35%), Medium (15–35%), Low (<15%). Counts and ARR in legend.

**Mini table** — Top 5 highest-churn-risk renewals in current period:
```
Delhi Coaching Hub        ₹12.4L   Due 8 Apr   Risk: 78%   Stage: IDENTIFIED
Excel Institute           ₹6.2L    Due 15 Apr  Risk: 62%   Stage: OUTREACH_SENT
...
```
[View all high-risk renewals →] applies `?risk=high` filter.

---

## Stage Update — Churn Reason Modal

Appears when stage → CHURNED (required):

```
┌──────────────────────────────────────────────────────┐
│  Mark as Churned — Delhi Coaching Hub                │
│  ARR: ₹12.4L                                         │
├──────────────────────────────────────────────────────┤
│  Churn reason*  [PRICING                        ▼]   │
│                                                      │
│  Notes          [What happened? Any save attempt?  ] │
│                                                      │
│  ⚠  This marks ₹12.4L as lost ARR for Q1 2026.      │
│     This action is logged and visible to the CSM.    │
│                                                      │
│  [Cancel]               [Confirm Churn]              │
└──────────────────────────────────────────────────────┘
```

Churn reason enum: PRICING · BUDGET_CUT · SWITCHED_COMPETITOR · PRODUCT_FIT · LOW_USAGE · ADMIN_TURNOVER · INSTITUTION_CLOSURE · DELAYED_DECISION · UNKNOWN

POST to `/csm/renewals/{id}/stage/` with `stage=CHURNED&churn_reason=PRICING`. Sets `lost_at = now()`.

---

## Create / Edit Renewal Drawer

Accessed via [+ Add Renewal] (CSM only; for institutions with no existing renewal record).

```
┌──────────────────────────────────────────────────────┐
│  Add Renewal Record                                  │
├──────────────────────────────────────────────────────┤
│  Institution*   [Search institution...       ]       │
│  Renewal date*  [YYYY-MM-DD   ]                      │
│  ARR (₹)*       [__________]                         │
│  Plan name*     [School Pro                 ]        │
│  Seats*         [2400  ]                             │
│  Stage*         [IDENTIFIED                 ▼]       │
│  Probability    [50  ]%                              │
│  Assigned AM    [Ravi S.                    ▼]       │
│  Renewal Exec   [Pooja M.                   ▼]       │
│  Notes          [_______________________________]    │
│                                                      │
│  [Cancel]             [Save Renewal]                 │
└──────────────────────────────────────────────────────┘
```

Validation: Institution required + must not already have an active renewal. Date ≥ today. ARR > 0. Plan and seats required.

---

## Export CSV

Filename: `eduforge_renewals_YYYY-MM-DD.csv`

Columns: institution_id, institution_name, type, enrolled, arr_value, plan_name, seats, stage, probability_pct, renewal_date, days_to_renewal, assigned_am, renewal_executive, churn_risk_tier, churn_probability_pct, health_score, last_touchpoint_date, notes_summary

Available to CSM (#53) and CS Analyst (#93). Max 2,050 rows. Async for > 500 rows (same pattern as J-02 export). Served at `GET /csm/renewals/export/` (`csm:renewal_export`).

---

## Empty States

| Condition | Message |
|---|---|
| No renewals in selected period | "No renewals due in this period. Adjust the period filter or add a renewal record manually." |
| Kanban column empty | Column shows dashed border with "No renewals in this stage" |
| AM filter = specific AM with no renewals | "No renewals assigned to this Account Manager for the selected period." |
| Churn risk panel: no high-risk renewals | "No high-risk renewals in the current period. " |

---

## Toast Messages

| Action | Toast |
|---|---|
| Stage updated | "Stage updated to [STAGE] for [Institution]." (green) |
| Stage → CHURNED | "Marked as churned. ₹X.XL removed from ARR forecast." (red) |
| Stage → RENEWED | "Renewal confirmed. ₹X.XL won for [period]." (green) |
| Stage → EXPANSION | "Expansion logged. +₹X.XL added to NRR." (teal) |
| Drag-and-drop to closed column | "Cannot move to RENEWED or CHURNED via drag. Use Update Stage dropdown." (amber) |
| Export queued | "Export is processing. You'll be notified when it's ready." (blue) |

---

## Role-Based UI Visibility Summary

| Element | 53 CSM | 54 AM | 55 Escalation | 56 Renewal | 93 Analyst | 94 ISM |
|---|---|---|---|---|---|---|
| Full Kanban/List | Yes | Own + team | Read only | All | Read only | Read own strip |
| Stage update (dropdown) | Yes | Yes | No | Up to COMMITTED | No | No |
| Win/lose renewal | Yes | Yes | No | No | No | No |
| Drag Kanban cards | Yes | Yes | No | No | No | No |
| Churn reason modal | Yes | Yes | No | No | No | No |
| Create renewal record | Yes | No | No | No | No | No |
| Export CSV | Yes | No | No | No | Yes | No |
| AM filter (all CSMs) | Yes | Own only | Own only | Own only | All | Own only |
| ARR summary strip | Full | Full | Full | Full | Full | Renewal strip only |
