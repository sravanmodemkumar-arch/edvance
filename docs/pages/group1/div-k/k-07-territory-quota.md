# K-07 — Territory & Quota Management

**Route:** `GET /group1/k/territory/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** B2B Sales Manager (#57)
**Also sees:** Sales Ops Analyst (#95 — read-only full), Sales Executives #58–60 (own quota + territory rows only, read-only), Inside Sales Executive (#97 — own quota row only, read-only)

---

## Purpose

**Viewport:** Desktop-only (minimum 1280px recommended for attainment gauge strip with multiple exec rows). No mobile layout provided.

Territory assignment and quota management hub for the Sales division. The B2B Sales Manager defines which Sales Executive owns which geographic territories and institution segments, then sets monthly or quarterly deal-count and ARR targets for each. Real-time attainment tracking — backed by live actuals from `sales_lead` and pre-computed gauges from Celery — lets the Manager spot underperforming territories and rebalance headcount or leads before a quarter-end shortfall becomes irreversible. At scale with 2,050 institutions spread across 28 states, territory clarity prevents duplicate outreach and ensures every institution has a single accountable owner. Executives see their own row only; they cannot view peers' quotas. The Sales Ops Analyst has full read access across all executives and periods and can export quota reports.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Quota targets + period actuals | `sales_quota` JOIN `sales_lead` (won_at within period) | 15 min |
| Territory assignments | Derived from `sales_lead.territory` + `owner_id` grouping | 10 min |
| Attainment gauges | Celery `compute_quota_attainment` task result (refreshed nightly, stored in cache) | Until next Celery run |
| Historical performance chart | `analytics_sales_funnel` filtered by `period_date` | 1 hour |
| Exec roster | `auth_user` WHERE role IN (58, 59, 60, 97) | 15 min |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?period_type` | `monthly`, `quarterly` | `monthly` | Sets period granularity; drives attainment gauge and quota table |
| `?period_year` | 4-digit integer | Current year | Year portion of period |
| `?period_num` | 1–12 (monthly) or 1–4 (quarterly) | Current period | Period number |
| `?view` | `quota`, `territory` | `quota` | Active view tab |
| `?exec` | `user_id` | — | Filter quota table and gauges to single exec (Manager/Ops only) |

---

## HTMX Part-Load Routes

**HTMX refresh hierarchy:**
Period change (← [Mar 2026] → click) triggers ALL three partials simultaneously via hx-include targeting the period form inputs. Auto-refresh (every 15 min) only refreshes `#k-quota-table` and `#k-attainment-gauges` — NOT the historical chart (nightly data, no point refreshing). The period change and auto-refresh are independent: changing period resets the 15-min timer.

| Route | Component | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| `htmx/k/territory/quota-table/` | Quota attainment table | Period change + save | 15 min | `#k-quota-table` |
| `htmx/k/territory/attainment-gauges/` | Gauge strip | Period change + save | 15 min | `#k-attainment-gauges` |
| `htmx/k/territory/territory-table/` | Territory assignment table | view=territory toggle | None | `#k-territory-table` |
| `htmx/k/territory/historical-chart/` | Historical performance chart | Period change | None (nightly data) | `#k-historical-chart` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  TERRITORY & QUOTA MANAGEMENT   [◀ Mar 2026 ▶]  [Monthly ▼]    │
│  [◼ Quota View]  [☐ Territory View]                             │
├─────────────────────────────────────────────────────────────────┤
│  ATTAINMENT GAUGES                                              │
│  Rahul  (Schools)   ████████░░  80%   8/10 deals  ₹28L/₹35L    │
│  Priya  (Colleges)  ██████░░░░  60%   6/10 deals  ₹21L/₹35L    │
│  Suresh (Coaching)  ██████████ 100%   5/5 deals   ₹25L/₹25L ✓  │
│  Arjun  (Inbound)   ███████░░░  70%  14/20 deals  ₹35L/₹50L    │
│  TEAM TOTAL         ████████░░  79%  33/55 deals  ₹109L/₹145L  │
├─────────────────────────────────────────────────────────────────┤
│  QUOTA TABLE                              [Set / Edit Quotas]   │
│  Exec   │ Seg     │ Target │ Actual │  Δ  │ Target ARR │ Actual │
│  Rahul    SCHOOL    10       8      -2     ₹35L         ₹28L    │
│  Priya    COLLEGE   10       6      -4     ₹35L         ₹21L    │
│  Suresh   COACHING   5       5       0     ₹25L         ₹25L ✓  │
│  Arjun    INBOUND   20      14      -6     ₹50L         ₹35L    │
├─────────────────────────────────────────────────────────────────┤
│  HISTORICAL CHART  (last 6 periods — target vs actual, by exec) │
└─────────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Period Selector

Fixed to top of page; drives all HTMX partial reloads below.

```
◀  [Mar 2026]  ▶    [Monthly ▼]
```

- **Period Type toggle:** Monthly / Quarterly. Switching resets `period_num` to current period of that type.
- **Period Navigator:** Left/right arrow buttons increment or decrement `period_num`; wraps into adjacent year automatically. Centre label displays "Mar 2026" (monthly) or "Q1 2026" (quarterly).
- Navigating to future periods: allowed — shows quota targets with "No actuals yet" in attainment columns.
- Navigating to periods before team's earliest quota record: shows empty state.
- All four HTMX parts refresh simultaneously on period change.

---

### 2. View Toggle

Tab strip below period selector.

```
[◼ Quota View]  [☐ Territory View]
```

- **Quota View** (default): Shows attainment gauge strip + quota table + historical chart.
- **Territory View:** Replaces quota table section with territory assignment table and rebalance controls. Gauge strip and historical chart are hidden in territory view.

Active tab highlighted; HTMX swaps the central content region only.

---

### 3. Attainment Gauge Strip (Quota View)

One row per active Sales Executive who has at least one record in `sales_quota` for the selected period. Sorted: Execs #58, #59, #60, #97, then Team Total row.

```
┌─────────────────────────────────────────────────────────────────────┐
│  Rahul Sharma  [SCHOOL]                                             │
│  ████████░░░░  80%   8 / 10 deals   ₹28L / ₹35L   On track ₹32L  │
├─────────────────────────────────────────────────────────────────────┤
│  Priya Nair  [COLLEGE]                                              │
│  ██████░░░░░  60%   6 / 10 deals   ₹21L / ₹35L   At risk ₹26L    │
├─────────────────────────────────────────────────────────────────────┤
│  Suresh Reddy  [COACHING]                                           │
│  ██████████  100%   5 / 5 deals   ₹25L / ₹25L  ✓ Quota met!       │
├─────────────────────────────────────────────────────────────────────┤
│  TEAM TOTAL  79%   33 / 55 deals   ₹109L / ₹145L                   │
└─────────────────────────────────────────────────────────────────────┘
```

**Per-row elements:**
- Exec name + segment badge (SCHOOL=blue / COLLEGE=teal / COACHING=amber / INBOUND=indigo)
- Horizontal progress bar: green fill if attainment ≥ 90%; amber if 70–89%; red if < 70%
- Percentage label (deals-based attainment: `actual_deals / target_deals × 100`)
- Deals fraction: "8 / 10 deals"
- ARR fraction: "₹28L / ₹35L"
- Green checkmark icon if attainment ≥ 100%
- End-of-period projection: linear extrapolation using `(actual_deals / elapsed_days_in_period) × total_days_in_period`. Shown as "On track for ₹32L" (green) or "At risk ₹26L" (amber) or "Needs ₹15L in 5 days" (red) based on whether projection ≥ target

**Team Total row:** aggregate sum of all exec targets vs actuals. Same bar / colour logic. No projection label.

**Clicking an exec row:** Scrolls page to quota table and expands a filtered view showing only that exec's row with deal-level breakdown. Manager and Ops only — exec cannot click other rows.

**Exec self-view:** Executives (#58–60, #97) see only their own row. Team Total row is hidden for exec role.

---

### 4. Quota Table (Quota View)

All active Sales Executives × current period. Loaded via HTMX. Manager sees all rows; Execs see own row only.

| Column | Detail |
|---|---|
| Exec Name | Full name + role badge |
| Segment | SCHOOL / COLLEGE / COACHING / INBOUND |
| Target Deals | `target_deals` from `sales_quota` for this period |
| Actual Deals | COUNT `sales_lead` WHERE `owner_id=exec` AND `stage='CLOSED_WON'` AND `won_at` within period |
| Δ Deals | Actual − Target; red if negative |
| Target ARR | `target_arr_paise` formatted |
| Actual ARR | SUM `arr_estimate_paise` on CLOSED_WON leads in period; formatted |
| Δ ARR | Actual − Target ARR; red if negative |
| Attainment % | Deals attainment % (primary KPI); colour coded same as gauges |
| Actions | Edit button (pencil icon) — Manager #57 only |

If no quota has been set for an exec in the current period, their row shows "—" for all targets with an orange "No quota set" badge. [Set Quota] link inline.

**[Set / Edit Quotas] button** (top-right of quota table, Manager only): Opens a multi-row batch quota modal showing all execs for the current period. Allows editing all quotas in one view before saving.

Sort by: exec name, attainment %, ARR actual. Default: attainment % ascending (lowest first, to surface underperformers).

---

### 5. Set / Edit Quota Modal

Per-exec quota setting. Accessible via row Edit button or [Set / Edit Quotas] batch button.

```
┌──────────────────────────────────────────────────────────────────┐
│  Set Quota — Rahul Sharma (Schools)                              │
├──────────────────────────────────────────────────────────────────┤
│  Exec Name          Rahul Sharma                 (read-only)     │
│  Period Type        Monthly                      (read-only)     │
│  Period             Mar 2026                     (read-only)     │
│  Segment            SCHOOL                       (read-only)     │
│                                                                  │
│  Target Deals*      [10   ]   (integer; min 1)                   │
│  Target ARR ₹L      [35   ]   (in lakhs; stored as paise)        │
│                                                                  │
│  ⚠ You are setting a quota for a past period (Feb 2026).         │
│    This is allowed but unusual. Confirm to proceed.              │
│                                                                  │
│  [Cancel]                          [Save Quota]                  │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Target Deals: required; integer; minimum 1; maximum 999.
- Target ARR: required; positive number entered in lakhs (₹L) on UI; multiplied by 1,00,000 × 100 before storing as paise.
- Past-period warning: "You are setting a quota for a past period ([period]). This is allowed but unusual." — shows warning but does not block submission. Requires confirmation checkbox.
- Cannot set quota for a user whose role is not Sales Executive or Inside Sales Exec (#97) (#57 can only set quotas for roles #58, #59, #60, #97).
- Duplicate handling: UPSERT on `UNIQUE(owner_id, period_type, period_year, period_num)` — editing an existing quota updates it.

On save: POST/PATCH to `/group1/k/territory/quota/save/`. Success toast. HTMX refreshes quota table and attainment gauges.

**Batch quota validation (when editing multiple execs in one view):**
If a "Set All Quotas" batch mode is available (multiple rows editable at once):
- Row-level inline validation: each row shows its own error state (red border + message) independently.
- Submit is blocked if ANY row has validation errors — form shows summary: "3 rows have errors. Fix them before saving."
- On successful batch save: "Quotas saved for [N] executives for [period]" toast. HTMX refreshes both the quota table and attainment gauges.

**Past-period edit threshold:** Any period before the first day of the current month triggers the warning. Example: editing Feb 2026 quota on 5 Mar 2026 shows: "You are editing a past period (Feb 2026). This will affect historical attainment reports. Confirm to proceed." Checkbox confirmation required.

---

### 6. Territory View

Activated by [Territory View] tab. Replaces gauge strip + quota table with territory assignment table.

**Territory assignment table** — derived from actual `sales_lead` data: distinct `(territory, owner_id)` combinations with counts.

| Column | Detail |
|---|---|
| Territory | Territory string (e.g., "TS — Hyderabad Zone") |
| Exec Assigned | Name + segment badge |
| Lead Count | Total leads WHERE `territory=this` AND `owner_id=exec`; all stages |
| Active Pipeline ARR | SUM `arr_estimate_paise` WHERE stage NOT IN (CLOSED_WON, CLOSED_LOST) |
| Won ARR (Period) | SUM `arr_estimate_paise` WHERE `stage=CLOSED_WON` AND won within period |
| Institution Types | Distinct institution_type badges present in this territory |
| Actions | [Rebalance] button — Manager only |

Territories without any leads show a soft grey "Unassigned" row if a Sales Exec has no leads in their expected territory (derived from exec role assignment). Manager can use Rebalance to move leads in.

**Rebalance Wizard** — opened by [Rebalance] row button or [Rebalance Territory] page button.

```
Step 1 of 4 — Select Source

  Source Exec:     [Rahul Sharma (Schools) ▼]
  Territory:       [TS — Hyderabad Zone ▼]
  Leads found:     24 active leads in this territory / exec combo

  [Next →]

─────────────────────────────────────────────────────────────────

Step 2 of 4 — Select Target

  Target Exec:     [Priya Nair (Colleges) ▼]
  ⚠ Priya already has 31 active leads. Adding leads may exceed
    recommended 30-lead cap.

  [← Back]  [Next →]

─────────────────────────────────────────────────────────────────

Step 3 of 4 — Preview

  Leads to reassign: 12 leads  (ARR: ₹28L)
  Stages: PROSPECT (4), CONTACTED (3), DEMO_SCHEDULED (3),
          DEMO_DONE (2)

  [Select individual leads to include / exclude]
  ☑ Sunrise Public School    DEMO_DONE   ₹4.2L
  ☑ Kerala Vidyalaya         CONTACTED   ₹2.8L
  ☐ DPS Hyderabad            PROSPECT    ₹3.5L   (deselected)
  ...

  [← Back]  [Next →]

─────────────────────────────────────────────────────────────────

Step 4 of 4 — Confirm

  You are reassigning 11 leads (₹24.5L ARR) from
  Rahul Sharma → Priya Nair in TS — Hyderabad Zone.

  A system activity note will be logged on each lead:
  "Reassigned from Rahul Sharma to Priya Nair by [Manager]
   on 21 Mar 2026."

  [← Back]  [Confirm Reassignment]
```

**On confirmation:** Bulk UPDATE `sales_lead.owner_id` for selected lead IDs. System activity note logged on each lead record. Toast shown. Territory table refreshes via HTMX.

**Warning threshold:** If target exec already has ≥ 30 active leads (non-terminal stages), show amber warning in Step 2. Does not block — Manager can proceed. Warning text: "Priya already has [N] active leads. Adding more may strain capacity."

**Rebalance validation rules:**
- Cannot leave source exec with 0 leads if they have an active quota for the current period. Shows warning: "Reassigning all leads will leave [Exec] with no active pipeline. Are you sure? Their quota will still show 0% attainment."
- Cannot exceed target exec's recommended capacity of 30 active leads. Shows: "Warning: [Target Exec] will have [N] active leads after reassignment (recommended max: 30). You can proceed, but flag this for manager review."
- Minimum 1 lead must be selected for reassignment (cannot submit with 0 leads selected in step 3).
- CLOSED_WON and CLOSED_LOST leads are excluded from reassignment pool automatically (greyed out in selection list with "(closed)" label).

---

### 7. Historical Performance Chart

Chart.js stacked bar chart. Last 6 periods of the current `period_type`. Visible in Quota View only.

```
Historical Performance — Last 6 Periods (Monthly)

₹L   ▲
 50  │     ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗
 40  │     ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║
 30  │     ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║
 20  │     ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║
 10  │     ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║
     └─────────────────────────────────── Period
          Oct  Nov  Dec  Jan  Feb  Mar
                                   ·····  Target line
```

- **X-axis:** Last 6 periods (month names or "Q1 2026" etc.)
- **Y-axis (left):** ARR in ₹L
- **Y-axis (right, line):** Deal count
- **Stacked bars:** One colour per exec (legend below chart). Bars represent actual ARR per exec per period
- **Target overlay:** Dotted horizontal line (or per-period dots) showing aggregate team target ARR
- **Deal count line:** Secondary axis line, right side, showing total deals closed per period
- **Legend toggles:** Click exec name in legend to show/hide their bar segment
- **Filter by exec:** If `?exec=` URL param is set, chart shows only that exec's data vs their individual target

Source: `analytics_sales_funnel` WHERE `period_date` spans last 6 periods. Falls back to live `sales_quota` + `sales_lead` query if analytics not yet populated.

---

## Empty States

| Condition | Message |
|---|---|
| No quota set for current period (Manager view) | "Quotas not yet set for [Mar 2026]. [Set Quotas →]" with CTA button |
| No quota set — exec self-view | "Your quota for [Mar 2026] hasn't been set yet. Contact your manager." |
| No territory data | "No leads in system for the selected period — assign leads to build the territory map." |
| Filter returns no territory rows | "No territory data matches the current filter." |
| No history data for chart | "Not enough data for the historical chart. At least 2 periods of quota history required." |
| Exec with no activity in period | Exec row shown greyed out with "0 / [target] deals — no activity this period" |

---

## Toast Messages

| Action | Toast |
|---|---|
| Quota saved (new) | "Quota set for Rahul Sharma — Mar 2026: 10 deals / ₹35L ARR" (green) |
| Quota updated | "Quota updated for Priya Nair — Mar 2026." (green) |
| Past-period quota saved | "Quota set for Feb 2026 (past period). Actuals already final." (amber) |
| Leads reassigned | "11 leads reassigned from Rahul Sharma to Priya Nair in TS — Hyderabad Zone" (green) |
| Rebalance cancelled | No toast — wizard closes silently |
| Capacity warning acknowledged | No toast — warning shown inline in wizard |

---

---

## Authorization

**Route guard:** `@division_k_required(allowed_roles=[57, 58, 59, 60, 95, 97])` applied to `TerritoryQuotaView`.

| Scenario | Behaviour |
|---|---|
| Sales Manager (#57) | Full access — view all execs, set/edit quotas, rebalance territories |
| Sales Execs (#58–60) | Queryset filtered to own quota rows only. Rebalance Wizard: 403 if accessed directly. |
| Inside Sales Exec (#97) | Own quota row only (read-only). Territory view not accessible. |
| Sales Ops (#95) | Read-only all. Export quota report allowed. All POST/PATCH return 403. |
| Quota UPSERT endpoint POST `/k/territory/quota/` | Only #57. Others return 403. |
| Territory reassignment POST `/k/territory/rebalance/` | Only #57. Others return 403. |
| Any other role | 403 Forbidden |

## Role-Based View Summary

| Feature | #57 Manager | #58–60 Execs | #95 Ops Analyst | #97 Inside Sales Exec | Others |
|---|---|---|---|---|---|
| View attainment gauges | All execs | Own row only | All execs | Own row only | No access |
| View quota table | All rows | Own row only | All rows | Own row only | No access |
| Set / Edit quotas | Yes — all execs | No | No | No | No |
| View territory table | All territories | Own territories | All territories | No | No |
| Rebalance territory (wizard) | Yes | No | No | No | No |
| Historical chart | All execs + toggle | Own data only | All execs | Own data only | No |
| Period selector | Full control | Read current only | Full control | Read current only | No |
| Export quota report | Yes | No | Yes | No | No |
| Exec filter (`?exec=`) | Yes | Own ID only | Yes | Own ID only | No |
