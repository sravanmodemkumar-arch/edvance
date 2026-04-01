# J-01 — Customer Success Dashboard

**Route:** `GET /csm/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** Customer Success Manager (#53)
**Also sees (restricted view):** Account Manager (#54), Escalation Manager (#55), Renewal Executive (#56), CS Analyst (#93), Implementation Success Manager (#94)

---

## Purpose

Real-time health overview of the entire 2,050-institution portfolio. Surfaces at-risk accounts, renewal urgency, open escalations, and NPS trends in a single command-centre view. The CSM's first screen every morning and the pivot point for daily prioritisation across the team.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `csm_institution_health` + `csm_renewal` + `csm_nps_survey` | 5 min |
| Health heatmap | `csm_institution_health` aggregated by tier + institution_type | 5 min |
| At-risk feed | `csm_institution_health` WHERE engagement_tier IN ('AT_RISK','CRITICAL','CHURNED_RISK') ORDER BY health_score ASC | 3 min |
| Renewal strip | `csm_renewal` WHERE renewal_date ≤ today + 30d AND stage NOT IN ('RENEWED','CHURNED') ORDER BY renewal_date ASC | 5 min |
| Escalation feed | `csm_escalation` WHERE status NOT IN ('RESOLVED','CLOSED') ORDER BY severity ASC, opened_at ASC | 1 min |
| NPS trend chart | `csm_nps_survey` grouped by month WHERE survey_type='QUARTERLY_NPS' last 6 months | 60 min |
| Playbook status strip | `csm_playbook_instance` WHERE status='ACTIVE' grouped by assigned_to_id | 10 min |
| My portfolio panel | `csm_account_assignment` + `csm_institution_health` WHERE csm_id or account_manager_id or ism_id = current_user | 5 min |
| Anomaly panel (Analyst only) | `csm_institution_health` WHERE ABS(score_delta) ≥ 10 last 24h | 5 min |

All caches bypass with `?nocache=true` (CSM #53 only).

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `?segment` | `all`, `school`, `college`, `coaching`, `group` | Filter entire dashboard to one institution type; default `all` |
| `?csm_id` | user_id | Filter to one CSM's portfolio (CSM #53 only — can view any portfolio; all other roles see own accounts only) |
| `?nocache` | `true` | Bypass Memcached (CSM #53 only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| KPI strip | `?part=kpi` | Page load + auto-refresh every 5 min |
| Health heatmap | `?part=health_heatmap` | Page load + filter change |
| At-risk feed | `?part=at_risk_feed` | Page load + auto-refresh every 3 min |
| Renewal strip | `?part=renewal_strip` | Page load + auto-refresh every 10 min |
| Escalation feed | `?part=escalation_feed` | Page load + auto-refresh every 60s |
| NPS trend | `?part=nps_trend` | Page load |
| Playbook status | `?part=playbook_status` | Page load + auto-refresh every 10 min |
| My portfolio | `?part=my_portfolio` | Page load; refresh on user action |
| Anomaly panel | `?part=anomaly` | Page load + auto-refresh every 5 min (CS Analyst #93 only; omitted from response for other roles) |

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────┐
│  Customer Success   Segment: [All ▼]   [Today: Sat 21 Mar '26] │
├────────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 tiles)                                           │
├───────────────────────────┬────────────────────────────────────┤
│  HEALTH HEATMAP           │  AT-RISK FEED (top 10)             │
│  (stacked bar + donut)    │                                    │
├───────────────────────────┴────────────────────────────────────┤
│  RENEWAL STRIP (horizontal cards, scrollable)                  │
├───────────────────────────┬────────────────────────────────────┤
│  ESCALATION FEED          │  NPS TREND CHART (6 months)        │
├───────────────────────────┴────────────────────────────────────┤
│  PLAYBOOK STATUS STRIP                                         │
├────────────────────────────────────────────────────────────────┤
│  MY PORTFOLIO PANEL (role-filtered)                            │
└────────────────────────────────────────────────────────────────┘
```

---

## Components

### KPI Strip (5 tiles)

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ 2,050       │ │ 72          │ │ 143         │ │ ₹4.2Cr      │ │ +38         │
│ Total Inst. │ │ Avg Health  │ │ At-Risk /   │ │ ARR Due     │ │ NPS Score   │
│             │ │ Score  ↓3   │ │ Critical    │ │ ≤30d        │ │ (last qtr)  │
│ [All Types] │ │ [vs last wk]│ │ [247 total] │ │ [32 inst.]  │ │ [54 resp.]  │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

**Tile 1 — Total Institutions:** Count by segment (from `csm_institution_health` count). Shows segment breakdown on hover as tooltip. Sub-label shows "N unassigned" in amber if any institutions have no assigned CSM — query: `SELECT COUNT(*) FROM institution LEFT JOIN csm_account_assignment USING (institution_id) WHERE csm_account_assignment.csm_id IS NULL OR csm_account_assignment.institution_id IS NULL` (LEFT JOIN ensures institutions with no assignment row at all are also counted). Clicking filters J-02 to `?csm_id=unassigned`.

**Tile 2 — Avg Health Score:** Platform-wide average health score. Shows `↑+X` or `↓-X` delta vs last week's snapshot in `csm_weekly_snapshot`. Color: green if score ≥ 65, amber if 45–64, red if < 45.

**Tile 3 — At-Risk + Critical:** Combined count of institutions with tier IN ('AT_RISK','CRITICAL','CHURNED_RISK'). Sub-label shows full tier breakdown on hover: "AT_RISK: 89 · CRITICAL: 34 · CHURNED_RISK: 20".

**Tile 4 — ARR Due ≤30d:** Sum of `csm_renewal.arr_value_paise` where `renewal_date ≤ today + 30d` and stage NOT IN ('RENEWED','CHURNED'). Formatted as ₹X.XCr or ₹X.XL. Sub-label: "N institutions".

**Tile 5 — NPS Score:** Most recent quarterly NPS calculation from `csm_weekly_snapshot.nps_score`. Shows `null` as "— (no data)" if < 10 responses. Delta vs previous quarter. Color: green if ≥ 40, amber if 20–39, red if < 20.

**Role-based tile visibility:**
- Renewal Executive (#56): Tile 4 highlighted with border-amber; others greyed slightly
- Escalation Manager (#55): At-Risk tile highlighted; NPS/ARR greyed
- CS Analyst (#93): All tiles visible with additional "last computed" timestamp tooltip

---

### Health Heatmap

Two-part layout:

**Left: Stacked bar chart** (Chart.js) — 5 bars, one per institution type (All, School, College, Coaching, Group). Each bar stacked by tier (HEALTHY=green-600, ENGAGED=teal-500, AT_RISK=amber-500, CRITICAL=orange-500, CHURNED_RISK=red-600). Hover: shows exact count per tier per segment.

**Right: Donut chart** — Platform-wide tier distribution. Centre label shows avg health score. Legend below with count + %.

```
Stacked bars               Donut
┌──────────────────────┐   ┌─────────────────────┐
│ ████ School (1000)   │   │      ┌───┐           │
│ ██   College (800)   │   │    ╱  72 ╲           │
│ █    Coaching (100)  │   │   │  avg  │           │
│ ██   Groups (150)    │   │    ╲     ╱           │
│ ████ ALL (2050)      │   │      └───┘           │
└──────────────────────┘   └─────────────────────┘
  ■ Healthy ■ Engaged ■ At-Risk ■ Critical ■ Churned
```

Clicking a segment bar filters the At-Risk feed and Renewal strip to that segment (via `?segment=` param swap using `hx-push-url`).

**Last computed timestamp:** Small grey text below heatmap — "Health scores as of [csm_config['last_health_compute_at']]" — this single timestamp is set by Task J-1 at the moment it finishes computing all 2,050 institutions, giving a single authoritative freshness marker. If this timestamp is > 26 hours ago (Task J-1 likely failed or was delayed), shows amber warning: "Health data may be stale — scores from [timestamp]. Task J-1 may have failed." CSM (#53) can click to open `?nocache=true` live refresh. Do NOT use `MIN(computed_at)` from individual institution rows — that would falsely show the oldest-ever row, not the last batch run time.

---

### At-Risk Feed (top 10)

Table showing the 10 most critical institutions (lowest health score, excluding stage=CHURNED).

| Column | Description |
|---|---|
| Institution | Name (link → J-03) + Type badge |
| Health | Score with colour bar + delta arrow (`↓-12` in red) |
| Tier | Badge: AT_RISK/CRITICAL/CHURNED_RISK |
| Churn Risk | Churn probability % with colour band |
| Renewal | Date + "in X days" or "overdue" in red |
| CSM | Assigned CSM avatar + name |
| Last Touch | Relative time ("8 days ago") — red if > 30 days |
| Action | [Log Touchpoint] button |

**[View all at-risk →]** link → `/csm/accounts/?tier=at_risk,critical,churned_risk`

**Role visibility:**
- AM (#54): Only sees accounts where `account_manager_id = current_user`
- Renewal Exec (#56): Sees all but [Log Touchpoint] button hidden; replaced with [View Renewal]
- ISM (#94): Only sees accounts where `ism_id = current_user` and within first 90 days

---

### Renewal Strip

Horizontal scrollable row of cards — one per renewal due within 30 days. Sorted by `renewal_date ASC`.

```
┌──────────────────────────┐  ┌──────────────────────────┐
│ Sunrise Academy          │  │ Delhi Coaching Hub        │
│ ₹3.6L · 1,200 seats      │  │ ₹12.4L · 8,500 members   │
│ Due: 28 Mar (7 days)     │  │ Due: 2 Apr (12 days)      │
│ Stage: QUOTE_SENT        │  │ Stage: NEGOTIATING        │
│ AM: Priya S.             │  │ AM: Ravi K.               │
│ [Update Stage]           │  │ [Log Touchpoint]          │
└──────────────────────────┘  └──────────────────────────┘
```

Card border colour: red if ≤ 7 days, amber if 8–14 days, yellow if 15–30 days.

**[Update Stage]** opens inline stage selector (select element, HTMX POST to `/csm/renewals/{id}/stage/`). AM + CSM + Renewal Exec only.

**[View all renewals →]** link → J-04

Empty state: "No renewals due in the next 30 days." with green checkmark icon.

---

### Escalation Feed

Table of open P1/P2 escalations. Maximum 5 rows; **[+N more]** link to J-05.

| Column | Description |
|---|---|
| Severity | P1/P2/P3 badge with colour |
| Title | Truncated (link → J-05 filtered by this escalation) |
| Institution | Name + ARR at risk if `account_at_risk=true` |
| Assigned To | Escalation Manager name |
| Days Open | Integer; red if P1 > 1d, P2 > 3d, P3 > 7d |
| Status | Badge |

**Account at Risk flag:** If `account_at_risk=true`, shows red flame icon next to institution name.

Empty state: "No open escalations." with shield-check icon.

**Role visibility:**
- Escalation Manager (#55): [Resolve] action column visible
- CSM (#53): [Assign] action visible
- All others: read-only

---

### NPS Trend Chart

Line chart (Chart.js) — 6 months of monthly NPS scores. X-axis: month labels. Y-axis: -100 to +100. Reference lines at 0 (neutral), +40 (good), +70 (excellent). Points show response count on hover ("38 responses · Nov '25"). Null months shown as gap (broken line).

**Below chart:** Mini tiles — Current NPS · Response Rate % · Promoters % · Detractors %

**[Manage Surveys →]** link → J-07

**Role visibility:**
- CS Analyst (#93): Additional secondary line showing CSAT average (right Y-axis, 1–5 scale)
- Renewal Exec (#56): Chart hidden; replaced with "No access — NPS data is CSM/Analyst view"

---

### Playbook Status Strip

Three summary blocks:

```
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ 38 Active Playbooks  │  │ 7 Overdue Tasks      │  │ 12 Completed (7d)    │
│ [View all →]         │  │ [View overdue →]     │  │ [View →]             │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

Overdue = playbook instance with a task where `due_days_offset` from `started_at` has passed and `completed=false`.

**[View all →]** links to J-06.

**Role visibility:**
- Renewal Exec (#56): Strip hidden (no playbook access)
- ISM (#94): Shows only their own assigned instances

---

### My Portfolio Panel

Personalised section — visible to CSM, AM, ISM. Shows the current user's assigned accounts in a compact table.

| Column | Description |
|---|---|
| Institution | Name (link → J-03) |
| Type | Badge |
| Health | Score + tier badge |
| Delta | Score change vs last week |
| Next Renewal | Date |
| Last Touchpoint | Relative time |
| Open Escalation | Count badge (red) if > 0 |
| Next Action Due | From latest `csm_touchpoint.next_action_date`; amber if today, red if past |

Sorted by health_score ASC (most at-risk first).

**Header:** "My Portfolio (23 accounts)" — count reflects assigned accounts.

For ISM (#94): header reads "My Implementations (8 active · 3 in first 90 days)".

Empty state: "No accounts assigned to you yet. Contact your CS team lead to get assigned."

---

### Anomaly Panel (CS Analyst #93 only)

Extra panel shown below My Portfolio for CS Analyst.

Surfaces institutions with a health score delta of ±10 or more in the last 24h.

```
┌─────────────────────────────────────────────────────┐
│  Score Anomalies (last 24h)                         │
│  ↓ Drops ≥10: 3 institutions                        │
│  ↑ Gains ≥10: 1 institution                         │
│                                                     │
│  Delhi Public School       73 → 59  ↓-14  [View]   │
│  Excel Academy             81 → 68  ↓-13  [View]   │
│  Hyderabad Coaching Hub    45 → 32  ↓-13  [View]   │
│  Sunrise College           52 → 63  ↑+11  [View]   │
└─────────────────────────────────────────────────────┘
```

[View] links to J-03 Account Profile.

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| At-Risk Feed | All institutions HEALTHY or ENGAGED | "Portfolio is healthy — no institutions in AT_RISK or below." |
| Renewal Strip | No renewals due in 30 days | "No renewals due in the next 30 days." |
| Escalation Feed | No open escalations | "No open escalations." |
| My Portfolio | No accounts assigned | "No accounts assigned. Contact your CS team lead." |
| NPS Trend | Fewer than 3 months of data | "Not enough NPS history yet — data will appear after the first quarterly survey cycle." |

---

## Toast Messages

| Action | Toast |
|---|---|
| Stage updated via Renewal Strip | "Stage updated to [STAGE] for [Institution]." (green) |
| Touchpoint logged from at-risk feed | "Touchpoint logged." (green) |
| Page load with `?nocache=true` | "Cache bypassed — showing live data." (blue) |

---

## Role-Based UI Visibility Summary

| Element | 53 CSM | 54 AM | 55 Escalation | 56 Renewal | 93 Analyst | 94 ISM |
|---|---|---|---|---|---|---|
| Full KPI strip | Yes | Yes | Yes | Yes | Yes | Yes |
| Health heatmap | Yes | Yes | Yes | Yes | Yes | Yes |
| At-risk feed | All | Own only | All | All | All | Own only |
| Renewal strip | All | Own only | Read | All | Read | Strip hidden |
| Escalation feed | Full + Assign | Read | Full + Resolve | Read | Read | Read |
| NPS trend chart | Yes | Yes | Read | Hidden | Full + CSAT line | Read |
| Playbook strip | Yes | Yes | Yes | Hidden | Read | Own only |
| My portfolio | Yes | Yes | Yes | Yes | Yes | Yes (implementations) |
| Anomaly panel | Hidden | Hidden | Hidden | Hidden | Yes | Hidden |
| [?nocache=true] | Yes | No | No | No | No | No |
