# J-02 — Institution Portfolio

**Route:** `GET /csm/accounts/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side pagination
**Primary roles:** CSM (#53), Account Manager (#54)
**Also sees:** Escalation Manager (#55) read-only, Renewal Executive (#56) read-only, CS Analyst (#93) read + export, ISM (#94) own implementations only

---

## Purpose

Paginated, searchable, filterable view of all 2,050 institutions with health scores, renewal dates, ARR, and assigned CSM. The primary workspace for portfolio management — CSMs use this daily to triage at-risk accounts, identify upsell opportunities, and prioritise outreach. CS Analyst uses it for bulk exports.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Institution table | `institution` JOIN `csm_institution_health` JOIN `csm_renewal` JOIN `csm_account_assignment` | 5 min |
| Filter options (CSM dropdown) | `user` WHERE role = 53 or 54 | 60 min |
| Row count strip | Same query, COUNT only | 5 min |
| Segment KPI header | `csm_institution_health` aggregated by tier | 5 min |

Cache key includes all active filter params. `?nocache=true` bypasses for CSM (#53) only.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?q` | string (≥ 2 chars) | — | Search by institution name or ID |
| `?type` | `school`, `college`, `coaching`, `group` | `all` | Filter by institution type |
| `?tier` | `healthy`, `engaged`, `at_risk`, `critical`, `churned_risk` (comma-sep) | `all` | Filter by health tier |
| `?csm_id` | user_id | `all` (CSM+AM see own by default) | Filter to one CSM's portfolio |
| `?renewal_window` | `overdue`, `7d`, `30d`, `60d`, `90d`, `beyond_90d` | `all` | Filter by renewal due window |
| `?has_escalation` | `1` | — | Show only accounts with open escalations |
| `?size_band` | `micro` (<500), `small` (500–2000), `medium` (2000–5000), `large` (>5000) | `all` | Filter by enrolled student count |
| `?sort` | `name`, `health_asc`, `health_desc`, `renewal_asc`, `arr_desc`, `last_touch_asc` | `health_asc` | Sort column + direction |
| `?page` | integer ≥ 1 | `1` | Page number |
| `?per_page` | `25`, `50`, `100` | `25` | Rows per page (CS Analyst: max 100) |
| `?export` | `csv` | — | Download CSV of current filtered result (CS Analyst + CSM only; bypasses pagination) |
| `?nocache` | `true` | — | Bypass Memcached (CSM #53 only) |

All params persist in URL; browser back/forward works correctly. Filter state serialised to URL via `hx-push-url="true"` on filter form.

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| Segment KPI header | `?part=header_kpis` | Page load + filter change |
| Institution table + pagination | `?part=table` | Page load + filter change + sort + page change |

Table part includes row count. Pagination controls are inside the table partial so they re-render on filter change.

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Institution Portfolio   [+ Bulk Assign CSM]   [Export CSV]          │
├──────────────────────────────────────────────────────────────────────┤
│  SEGMENT KPI HEADER (5 tiles: total + 4 tiers highlighted)           │
├──────────────────────────────────────────────────────────────────────┤
│  SEARCH BAR                                                          │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ [🔍 Search institution name or ID...]                          │  │
│  └────────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────────┤
│  FILTER ROW                                                          │
│  Type: [All ▼]  Tier: [All ▼]  CSM: [All ▼]  Renewal: [All ▼]       │
│  [Has Escalation □]  Size: [All ▼]  [Clear Filters]                  │
├──────────────────────────────────────────────────────────────────────┤
│  SORT ROW + ROW COUNT                                                │
│  Sort: [Health ▲ ▼]  Showing 2,050 institutions · Page 1 of 82       │
├──────────────────────────────────────────────────────────────────────┤
│  INSTITUTION TABLE                                                   │
├──────────────────────────────────────────────────────────────────────┤
│  PAGINATION                                                          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Segment KPI Header

5 clickable tiles (act as quick-filters):

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ 2,050    │ │ 1,203    │ │ 604      │ │ 143      │ │  100     │
│ Total    │ │ Healthy  │ │ Engaged  │ │ At-Risk  │ │ Critical │
│          │ │ + Engaged│ │ (shown   │ │ + below  │ │ + Churned│
│          │ │ (green)  │ │ combined)│ │ (amber)  │ │ (red)    │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

Clicking a tier tile applies `?tier=` filter and highlights the active tile. "Total" clears tier filter.

---

## Institution Table

Columns (all sortable unless noted):

| Column | Sortable | Description |
|---|---|---|
| ☐ | No | Checkbox for bulk selection |
| Institution | Yes (`?sort=name`) | Name (link → J-03) + institution type badge (colour-coded) |
| Health | Yes (`?sort=health_asc`, `?sort=health_desc`) | Score 0–100 with inline progress bar (green/amber/red) + tier badge |
| Δ (Delta) | No | Score change vs last week — arrow icon + number. `↓-12` in red, `↑+8` in green |
| Enrolled | No | Total enrolled users from `csm_institution_health.total_enrolled` |
| CSM | No | Assigned CSM avatar (initials circle) + name. "Unassigned" in grey if null |
| Next Renewal | Yes (`?sort=renewal_asc`) | Date + relative ("in 12d" / "in 3m" / "overdue"). Red badge if overdue |
| ARR | Yes (`?sort=arr_desc`) | ₹X.XL or ₹X.XCr. "—" if no renewal record |
| Last Touchpoint | Yes (`?sort=last_touch_asc`) | Relative time. Red if > 45 days; amber if 30–45 days |
| Escalations | No | Count badge (red) if open escalations. "—" if none |
| Actions | No | Row action menu (see below) |

**Row hover:** Background tinted blue-50. Full row is clickable to J-03 (except checkbox and Actions column).

**Row selection:** Checkboxes enable bulk action bar at bottom of screen (see Bulk Actions).

**Inline badges:**
- Institution type: SCHOOL=blue, COLLEGE=violet, COACHING=orange, GROUP=slate
- Health tier: HEALTHY=green, ENGAGED=teal, AT_RISK=amber, CRITICAL=orange, CHURNED_RISK=red
- Renewal: green if > 30d, amber if 8–30d, red if ≤ 7d or overdue

---

## Row Action Menu

Right-click or click `···` column. Role-based visibility.

| Action | Visible To | Behaviour |
|---|---|---|
| View Account Profile | All | Navigate to `/csm/accounts/{id}/` |
| Log Touchpoint | CSM, AM, ISM | Opens Log Touchpoint drawer (inline HTMX) |
| Assign CSM | CSM (#53) | Opens inline CSM assignment modal |
| Start Playbook | CSM, ISM | Opens Start Playbook modal |
| Create Escalation | CSM, Escalation Manager | Opens Create Escalation drawer |
| View Support Tickets | All | Opens `/support/institutions/{id}/` in new tab |
| Export Account Data | CSM, CS Analyst | Downloads CSV of J-03 data for this account |

---

## Search

- Live search: triggers `?part=table` HTMX request on input (300ms debounce, minimum 2 chars)
- Searches: `institution.name` (ILIKE), `institution.code` (exact), `institution.id` (exact integer match)
- Highlights matching text in name column using `<mark>` tags
- Preserves all active filters — search is additive
- No partial word matching; uses PostgreSQL ILIKE pattern `%search_term%`

---

## Filters Detail

### Type filter
Multi-select via checkboxes in dropdown; default all checked. HTMX target = `?part=table`.

### Tier filter
Multi-select. Options: All · Healthy · Engaged · At Risk · Critical · Churned Risk. Default all.

### CSM filter
Single-select dropdown. Options:
- **All** — all institutions (Escalation Manager, Analyst default)
- **My Accounts** — `csm_id = current_user OR account_manager_id = current_user` (CSM/AM default)
- **Unassigned** — `csm_id IS NULL` (CSM #53 only; surfaces accounts with no CSM assigned; shown in amber in the dropdown to draw attention)
- Individual CSMs listed by name (CSM #53 only; shows portfolio count in parentheses: "Ananya K. (34)")

The "Unassigned" option is the primary mechanism for the CSM to identify and act on accounts that fell through assignment gaps (e.g., after a CSM departure). Selecting it shows bulk-assign action in the sticky bar.

### Renewal Window filter
Single-select:
- All
- Overdue (renewal_date < today, stage NOT RENEWED/CHURNED)
- Due ≤ 7 days
- Due ≤ 30 days
- Due 31–60 days
- Due 61–90 days
- Due > 90 days or No renewal record

### Has Open Escalation
Checkbox. Adds `WHERE EXISTS (SELECT 1 FROM csm_escalation WHERE institution_id = ... AND status NOT IN ('RESOLVED','CLOSED'))`.

### Size Band filter
Based on `csm_institution_health.total_enrolled`:
- Micro (< 500)
- Small (500–2,000)
- Medium (2,000–5,000)
- Large (> 5,000)

---

## Pagination

- Server-side; default 25 rows/page
- Controls: First · Prev · 1 2 3 ... 82 · Next · Last
- HTMX: pagination click swaps `?part=table` with updated `?page=N`; URL updated via `hx-push-url`
- Per-page selector: 25 / 50 / 100 (CS Analyst only can select 100)
- Row count strip: "Showing 25–50 of 143 results" updates on filter change

---

## Bulk Actions

Appears as a sticky bottom bar when ≥ 1 row is checked:

```
┌───────────────────────────────────────────────────────────────┐
│  23 accounts selected   [Assign CSM ▼]  [Start Playbook ▼]   │
│                         [Export Selected]  [Clear selection]  │
└───────────────────────────────────────────────────────────────┘
```

| Action | Visible To | Behaviour |
|---|---|---|
| Assign CSM | CSM (#53) | Opens modal; select CSM from dropdown; updates `csm_account_assignment.csm_id` for all selected |
| Start Playbook | CSM (#53), ISM (#94) | Opens modal; select template; creates `csm_playbook_instance` for all selected institutions |
| Export Selected | CSM (#53), CS Analyst (#93) | Downloads CSV with selected institutions' health data |

Maximum 100 institutions selectable for bulk action. If > 100 selected: "Maximum 100 accounts for bulk operations. Refine your selection."

---

## Export CSV

Triggered by `?export=csv` or [Export CSV] header button (current filters applied).

**Columns exported:**
institution_id, institution_name, type, health_score, engagement_tier, score_delta, total_enrolled, active_users_30d, dau_7d_avg, exams_created_30d, sessions_30d, payment_health_score, churn_probability_pct, renewal_date, arr_value_paise, renewal_stage, days_to_renewal, assigned_csm, assigned_am, last_touchpoint_date, last_touchpoint_type, open_escalations_count, computed_at

**Filename:** `eduforge_csm_portfolio_YYYY-MM-DD.csv`

**Who can export:** CSM (#53) and CS Analyst (#93). Maximum 2,050 rows (full portfolio). Export is async for > 500 rows: Celery task queued, in-app notification sent when ready with download link valid for 24h.

---

## Empty States

| Condition | Message |
|---|---|
| Search returns no results | "No institutions match '[search term]'. Try a shorter name or clear filters." with [Clear Search] button |
| Filters eliminate all results | "No institutions match your current filters." with [Clear All Filters] button |
| CSM filter set to specific CSM with no accounts | "No accounts assigned to this CSM." with [Assign Accounts] button (CSM #53 only) |
| ISM sees empty own portfolio | "No active implementations assigned to you." |

---

## Loading State

Skeleton rows (10) with shimmer animation while `?part=table` loads. Segment KPI header shows spinner overlay while `?part=header_kpis` loads.

---

## Role-Based UI Visibility Summary

| Element | 53 CSM | 54 AM | 55 Escalation | 56 Renewal | 93 Analyst | 94 ISM |
|---|---|---|---|---|---|---|
| Full table (all institutions) | Yes | Own + team | Yes (read) | Yes (read) | Yes (read) | Own impls |
| CSM filter | All CSMs | Own only | Own only | Own only | All CSMs | Own only |
| Log Touchpoint action | Yes | Yes | No | No | No | Yes (own) |
| Assign CSM action | Yes | No | No | No | No | No |
| Start Playbook action | Yes | No | No | No | No | Yes (own) |
| Create Escalation action | Yes | No | Yes | No | No | No |
| Export CSV | Yes | No | No | No | Yes | No |
| Bulk Assign CSM | Yes | No | No | No | No | No |
| Bulk Start Playbook | Yes | No | No | No | No | Yes (own) |
| per_page = 100 option | Yes | No | No | No | Yes | No |
