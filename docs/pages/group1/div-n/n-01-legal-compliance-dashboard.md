# N-01 — Legal & Compliance Dashboard

**Route:** `GET /legal/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Legal Officer (#75), Data Privacy Officer (#76)
**Also sees (restricted strips):** Regulatory Affairs Exec (#77) — filings strip; POCSO Reporting Officer (#78) — POCSO strip; Contract Coordinator (#103) — contracts strip; Data Compliance Analyst (#104) — DSR strip

---

## Purpose

Morning command view for the Legal & Compliance division. At 2,050 institutions, manual compliance tracking fails — this page surfaces the critical items that need attention today. Legal Officer uses it to monitor contract expiry risk, check for new breaches, and verify no filings are overdue. DPO uses it to track open DSR resolution timelines (DPDP Act 30-day clock) and breach notification status (72-hour clock). Other roles see only their relevant strip, eliminating context-switching to N-02 through N-07 for daily status checks.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `legal_contract` counts + `dpdp_dsr` open counts + `pocso_incident` open counts + `regulatory_filing` overdue counts | 5 min |
| Contract status donut | `legal_contract` GROUP BY status | 30 min |
| DSR resolution trend | `dpdp_dsr` GROUP BY month: opened_count, resolved_count, avg_resolution_days | 60 min |
| Breach alert banner | `dpdp_breach_incident` WHERE status NOT IN ('RESOLVED') | 1 min |
| Upcoming deadlines | `legal_compliance_deadline` WHERE due_date <= today+14d AND status NOT IN ('COMPLETED') | 5 min |
| Expiring contracts | `legal_contract` WHERE status='ACTIVE' AND expiry_date <= today+30d ORDER BY expiry_date ASC | 10 min |
| Regulatory filing strip | `regulatory_filing` WHERE due_date <= today+30d OR status='OVERDUE' ORDER BY due_date ASC | 10 min |
| POCSO open incidents | `pocso_incident` WHERE status NOT IN ('CLOSED') ORDER BY date_reported_to_eduforge ASC | 2 min |
| DSR clock strip | `dpdp_dsr` WHERE status IN ('OPEN','IN_PROGRESS') ORDER BY due_at ASC | 2 min |

Cache keys scoped to `(role_id, user_id)`. `?nocache=true` available to Legal Officer (#75) and DPO (#76) only.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?nocache` | `true` | — | Bypass Memcached (Legal Officer + DPO only) |
| `?period` | `this_month`, `last_month`, `this_quarter`, `ytd` | `this_month` | Affects DSR trend chart and KPI period deltas |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| KPI strip | `?part=kpi` | Page load | 5 min | `#n-kpi-strip` |
| Contract status donut | `?part=contract_donut` | Page load | 30 min | `#n-contract-donut` |
| DSR resolution trend | `?part=dsr_trend` | Page load + period change | 60 min | `#n-dsr-trend` |
| Breach alert banner | `?part=breach_alert` | Page load | 1 min | `#n-breach-alert` |
| Upcoming deadlines | `?part=deadlines` | Page load | 5 min | `#n-deadlines` |
| Expiring contracts | `?part=expiring_contracts` | Page load | 10 min | `#n-expiring-contracts` |
| Regulatory filing strip | `?part=filings_strip` | Page load | 10 min | `#n-filings-strip` |
| POCSO strip | `?part=pocso_strip` | Page load | 2 min | `#n-pocso-strip` |
| DSR clock strip | `?part=dsr_clock` | Page load | 2 min | `#n-dsr-clock` |

All parts respond with HTML fragments only. Non-primary roles only receive their permitted strips; all other parts return HTTP 204 No Content.

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Legal & Compliance   Period: [This Month ▼]          [?nocache]   │
├────────────────────────────────────────────────────────────────────┤
│  ⚠ BREACH ALERT BANNER (shown only when active breach exists)      │
├────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 tiles)                                               │
├──────────────────────────┬─────────────────────────────────────────┤
│  CONTRACT STATUS DONUT   │  DSR RESOLUTION TREND (12 months, line) │
│  (by status)             │                                         │
├──────────────────────────┴─────────────────────────────────────────┤
│  UPCOMING DEADLINES (next 14 days)                                 │
├──────────────────────────────┬─────────────────────────────────────┤
│  EXPIRING CONTRACTS          │  REGULATORY FILING STRIP            │
├──────────────────────────────┴─────────────────────────────────────┤
│  POCSO OPEN INCIDENTS     │   DSR CLOCK STRIP (30-day countdown)  │
└───────────────────────────┴────────────────────────────────────────┘
```

> Non-primary roles see only their relevant strip(s). All other sections are hidden via server-side rendering — no hidden DOM elements sent.

---

## Components

### Breach Alert Banner

Shown only when `dpdp_breach_incident` has rows with `status NOT IN ('RESOLVED')`.

```
┌────────────────────────────────────────────────────────────────────┐
│  ⚠  ACTIVE DATA BREACH — CERT-In report due in 4h 22m              │
│     Breach ID: BRN-2026-001 · Discovered: 21 Mar 2026 01:14 IST   │
│     Severity: HIGH · Affected: ~12,000 student records             │
│                                          [View Breach Detail →]    │
└────────────────────────────────────────────────────────────────────┘
```

- **Background:** red-50 with left red-600 border
- **Timer:** live countdown to CERT-In 6-hour deadline (from `discovered_at`). Switches to "DPDP authority notification due in Nh" once CERT-In is submitted (72h clock from `discovered_at`)
- **Multiple breaches:** shows the most critical (highest severity, nearest deadline). Chevron [+N more] expands to list all active breaches
- **[View Breach Detail →]:** links to N-03?tab=breaches&id=BRN-2026-001
- **Dismissed state:** cannot be dismissed — persists until `status='RESOLVED'`
- **Auto-refresh:** every 60 seconds (1-min TTL)

**Visible to:** Legal Officer (#75) and DPO (#76) only. Other roles do not see this banner.

---

### KPI Strip (5 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 2,050        │ │ 14           │ │ 7            │ │ 2            │ │ 0            │
│ Active       │ │ Expiring     │ │ Open DSRs    │ │ Open POCSO   │ │ Overdue      │
│ Contracts    │ │ < 30 days    │ │              │ │ Incidents    │ │ Filings      │
│ 98.2% cov.   │ │ ⚠ Action req.│ │ 3 near due   │ │ ⚠ 1 critical │ │ ✓ All filed  │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Active Contracts:** `COUNT(legal_contract) WHERE status='ACTIVE'`. Sub-label: "N% coverage" = active_contracts / 2050 × 100. Target ≥ 100% (every institution must have active contracts). Green if = 2,050, amber if ≥ 2,000, red if < 2,000. Clicking opens N-02.

**Tile 2 — Expiring < 30 Days:** `COUNT(legal_contract) WHERE status='ACTIVE' AND expiry_date <= today+30d`. Sub-label "⚠ Action req." if count > 0. Amber if 1–10, red if > 10. Clicking opens N-02?status=expiring_soon.

**Tile 3 — Open DSRs:** `COUNT(dpdp_dsr) WHERE status IN ('OPEN','IN_PROGRESS')`. Sub-label: "N near due" = count where `due_at <= today+3d`. Amber if any near due, red if any overdue. Clicking opens N-03?tab=dsr.

**Tile 4 — Open POCSO Incidents:** `COUNT(pocso_incident) WHERE status NOT IN ('CLOSED')`. Sub-label: "N critical" = count where `ncpcr_submitted_at IS NULL AND ncpcr_due_at <= today+4h`. Red if > 0 and any critical (< 4h to NCPCR deadline). Clicking opens N-05.

**Tile 5 — Overdue Filings:** `COUNT(regulatory_filing) WHERE status='OVERDUE'`. "✓ All filed" in green if 0. Red if > 0. Clicking opens N-04?status=overdue.

**Loading state:** Shimmer animation during HTMX load. On auto-refresh failure, stale values retained with grey border and "↻ Retry" link.

**Role-based tile behaviour:**
- Regulatory Affairs Exec (#77): Tile 5 only (overdue filings → N-04)
- POCSO Reporting Officer (#78): Tile 4 only (open POCSO incidents → N-05)
- Contract Coordinator (#103): Tile 1 + Tile 2 only (no POCSO, no DSR visibility)
- Data Compliance Analyst (#104): Tile 3 only (open DSRs, read-only link to N-03)

---

### Contract Status Donut

Donut chart (Chart.js) — distribution of all 2,050 institution contracts by status.

- **Segments:** ACTIVE (green-500) · EXPIRING_SOON (amber-500) · EXPIRED (red-500) · DRAFT (grey-300) · SENT_FOR_SIGNATURE (blue-400) · TERMINATED (red-800)
- **Centre label:** Total contracts count
- **Hover tooltip:** status label · count · % of total
- **Legend:** below chart, click to isolate segment
- **Coverage gap indicator:** if ACTIVE + EXPIRING_SOON < 2,050, shows "Gap: N institutions have no active contract" below chart in red

**Visible to:** Legal Officer (#75), DPO (#76), Contract Coordinator (#103).

---

### DSR Resolution Trend Chart

Line chart — 12 months showing DSR volume and resolution performance.

- **Lines:** New DSRs (solid blue-500) · Resolved DSRs (solid green-500) · Avg resolution days (dashed amber-400, right Y-axis scale 0–30 days)
- **X-axis:** month labels (MMM YY)
- **Left Y-axis:** DSR count (0 to max)
- **Right Y-axis:** avg resolution days (0–30). Reference line at 30 days (DPDP Act §12 limit — must resolve within 30 days of receipt). Red fill if avg exceeds 30 days for any month.
- **Hover tooltip:** month · new DSRs · resolved DSRs · avg days to resolve · oldest open DSR age
- **Null months:** gaps shown with "No DSRs" tooltip
- **Period selector:** respects `?period` URL param

**Finance Analyst (#104):** Additional toggle "Show by request type" — stacks bars by DSR type (ACCESS/ERASE/CORRECT/RESTRICT).

**Visible to:** Legal Officer (#75), DPO (#76), Data Compliance Analyst (#104).

---

### Upcoming Deadlines Panel

Sortable list of all compliance deadlines in the next 14 days across all categories.

```
  ⚠ CERT-In report           21 Mar 2026  Due: 21 Mar (in 4h)   REGULATORY  [View →]
  ⚠ Contract renewal         22 Mar 2026  Due: Tomorrow          CONTRACT    [View →]
    DPDP authority notify     24 Mar 2026  Due: in 3d             REGULATORY  [View →]
    DSR #DSR-2026-044         28 Mar 2026  Due: in 7d             DSR         [View →]
    GSTR Policy review        31 Mar 2026  Due: in 10d            STATUTORY   —
    TRAI DLT renewal          1 Apr 2026   Due: in 11d            REGULATORY  [View →]
```

- Red row: due in ≤ 24 hours
- Amber row: due in 2–3 days
- Category badges colour-coded: CONTRACT (blue) · REGULATORY (purple) · STATUTORY (orange) · DSR (teal) · POCSO (red) · POLICY (indigo)
- [View →] links to the relevant sub-page
- **[View all →]** at bottom links to N-07 Compliance Calendar

**Visible to:** All Division N roles (scoped to their permitted categories):
- Legal Officer (#75): all categories
- DPO (#76): DSR + REGULATORY + POLICY categories
- Regulatory Affairs Exec (#77): REGULATORY only
- POCSO Reporting Officer (#78): POCSO only
- Contract Coordinator (#103): CONTRACT only
- Data Compliance Analyst (#104): DSR only

---

### Expiring Contracts

Compact table: institutions whose active contracts expire within 30 days.

```
  Delhi Public School      MSA          Expires: 22 Mar (in 1d)   [Initiate Renewal]
  Victory College          DPA          Expires: 25 Mar (in 4d)   [Initiate Renewal]
  Excel Coaching Hub       MSA + SLA    Expires: 28 Mar (in 7d)   [Initiate Renewal]
  [View all expiring →]
```

- Red row if expiring ≤ 1 day
- Amber row if expiring ≤ 7 days
- [Initiate Renewal]: Contract Coordinator (#103) or Legal Officer (#75) only → opens N-02 renewal drawer
- [View all expiring →]: links to N-02?status=expiring_soon

**Visible to:** Legal Officer (#75), Contract Coordinator (#103).

---

### Regulatory Filing Strip

Compact status list of upcoming and overdue regulatory filings.

```
  CERT-In   Incident Report #INC-2026-003   Due: 21 Mar (in 4h)   IN_PROGRESS  [View →]
  TRAI      DLT Entity Renewal 2026-27      Due: 1 Apr (in 11d)   UPCOMING     [View →]
  MeitY     Intermediary Compliance FY26    Due: 30 Apr (in 40d)  UPCOMING     —
```

- Red row: overdue or < 24h
- Amber row: due ≤ 7 days
- Status badges: UPCOMING (grey) · IN_PROGRESS (blue) · SUBMITTED (green) · ACKNOWLEDGED (teal) · OVERDUE (red)
- [View →]: links to N-04 with filing pre-selected
- [View all →]: links to N-04

**Visible to:** Regulatory Affairs Exec (#77) full; Legal Officer (#75) and DPO (#76) read-only.

---

### POCSO Open Incidents Strip

```
  POCSO Open Incidents: 2

  POCSO-2026-001   Sunrise Academy   21 Mar 2026   NCPCR due: in 18h   UNDER_INVESTIGATION  [View →]
  POCSO-2026-002   Hyderabad Hub     19 Mar 2026   NCPCR submitted ✓   SUBMITTED_TO_NCPCR   [View →]
```

- Red row: NCPCR deadline < 4 hours away or already overdue
- Amber row: NCPCR deadline < 12 hours away
- Status badges: RECEIVED (grey) · ACKNOWLEDGED (blue) · UNDER_INVESTIGATION (amber) · SUBMITTED_TO_NCPCR (green) · CLOSED (teal)
- Victim details: fully anonymized (no names, no institution-identifying details in this strip — only Incident Code + institution name)
- [View →]: links to N-05 with that incident pre-selected

**Visible to:** POCSO Reporting Officer (#78) and Legal Officer (#75) only.

---

### DSR Clock Strip

Active data subject requests ordered by due date ascending (most urgent first).

```
  DSR Open: 7   |   3 due within 3 days

  #DSR-2026-044   ERASE    Delhi Public School   Due: 24 Mar (9 days left)   IN_PROGRESS  [View →]
  #DSR-2026-039   ACCESS   Excel Coaching Hub    Due: 28 Mar (13 days left)  IN_PROGRESS  [View →]
  #DSR-2026-031   CORRECT  Victory College       Due: 02 Apr (18 days left)  OPEN         [View →]
  [View all →]
```

- Days-left calculation from `due_at` (= raised_at + 30 calendar days per DPDP Act §12)
- Red row if ≤ 5 days left
- Amber row if ≤ 10 days left
- "OVERDUE" badge in red if `due_at < now()` and status not RESOLVED/REJECTED
- [View →]: links to N-03?tab=dsr&id=DSR-2026-044
- [View all →]: links to N-03?tab=dsr

**Visible to:** DPO (#76) full; Legal Officer (#75) read-only; Data Compliance Analyst (#104) read-only.

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| Breach alert banner | No active breaches | Not shown — section hidden entirely |
| Expiring contracts | No contracts expiring ≤ 30 days | "No contracts expiring in the next 30 days." with green shield icon |
| Upcoming deadlines | No deadlines in next 14 days | "No compliance deadlines in the next 14 days." |
| POCSO strip | No open incidents | "No open POCSO incidents." with green checkmark |
| DSR clock strip | No open DSRs | "No open data subject requests." with green checkmark |
| Regulatory filing strip | No filings due within 30 days | "No regulatory filings due in the next 30 days." |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| `?nocache=true` used | "Cache bypassed — showing live compliance data." | Blue (info) |
| Period filter changed | "Dashboard updated to [period]." | Blue (info) |
| New breach incident created (real-time via Django Channels) | "⚠ Data breach incident created by [user]. CERT-In deadline: [time]." | Red (critical) |
| POCSO incident created (real-time) | "⚠ New POCSO incident logged. NCPCR deadline: [time]." | Red (critical) |
| Contract renewal initiated | "Renewal workflow started for [institution]." | Blue (info) |
| DSR resolved | "DSR #[id] resolved by [user]." | Green |
| Filing submitted | "[authority] filing submitted. Reference: [ref]." | Green |

---

## Authorization

**Route guard:** `@division_n_required(allowed_roles=[75, 76, 77, 78, 103, 104])` applied to `LegalDashboardView`.

| Scenario | Behaviour |
|---|---|
| Unauthenticated | Redirect to `/login/?next=/legal/` |
| Role not in allowed list | 403 redirect to `/403/` |
| POCSO strip | Only rendered for roles #75 and #78 — no DOM element generated for others |
| Breach alert banner | Only rendered for roles #75 and #76 |
| HTMX part requests for non-permitted strips | Return HTTP 204 No Content |
| `?nocache=true` | Allowed only for #75 and #76; others: 403 |

---

## Role-Based UI Visibility Summary

| Element | 75 Legal | 76 DPO | 77 Reg. Affairs | 78 POCSO | 103 Contract Coord. | 104 Data Analyst |
|---|---|---|---|---|---|---|
| Breach alert banner | Yes | Yes | No | No | No | No |
| KPI — Active Contracts | Yes | No | No | No | Yes | No |
| KPI — Expiring < 30d | Yes | No | No | No | Yes | No |
| KPI — Open DSRs | Yes | Yes | No | No | No | Yes (read) |
| KPI — Open POCSO | Yes | No | No | Yes | No | No |
| KPI — Overdue Filings | Yes | Yes | Yes | No | No | No |
| Contract status donut | Yes | Yes (read) | No | No | Yes | No |
| DSR resolution trend | Yes | Yes | No | No | No | Yes |
| Upcoming deadlines | All categories | DSR + Reg + Policy | Regulatory only | POCSO only | Contract only | DSR only |
| Expiring contracts panel | Yes (full) | No | No | No | Yes (initiate renewal) | No |
| Regulatory filing strip | Yes (read) | Yes (read) | Yes (full) | No | No | No |
| POCSO open incidents strip | Yes (read) | No | No | Yes (full) | No | No |
| DSR clock strip | Yes (read) | Yes (full) | No | No | No | Yes (read) |
| [?nocache=true] | Yes | Yes | No | No | No | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Initial page load (SSR) | < 2s P95 | All HTMX strips issued in parallel |
| Breach alert banner | < 500ms P95 (cache hit: 1 min) | Must be fast — breach clock is running |
| KPI strip | < 600ms P95 (cache hit: 5 min) | |
| POCSO strip | < 400ms P95 (cache hit: 2 min) | Sensitive data — no long caches |
| `?nocache=true` rebuild | < 8s | All parts re-fetched from DB |

---

## HTMX Error Handling

Applies to all auto-refreshing HTMX part-loads on this page.

| Scenario | HTTP Response | Fallback UI | Recovery |
|---|---|---|---|
| Part load timeout (DB slow / network) | 504 Gateway Timeout | Stale cached value retained with grey-400 border + "↻ Retry" link | Manual retry via link; next auto-refresh in normal TTL cycle |
| Database connection error | 503 Service Unavailable | Grey placeholder with "Service temporarily unavailable" message | Auto-retry once after 30s; if still failing, show static message |
| Permission error (role changed mid-session) | 403 Forbidden | Part replaced with "Session permissions changed — please refresh the page." | Full page refresh clears stale session |
| Part returns empty data (0 rows) | 200 OK (empty HTML) | Per-section empty state message (see Empty States section) | Normal — no retry needed |
| Breach alert banner fails to refresh | 503 | Retain last-known banner state with amber "⚠ Alert data stale" note | Critical path — auto-retry every 30s (1-min TTL may slip to 90s) |

**HTMX error handler (global, registered once on `<body>`):**
```javascript
document.body.addEventListener('htmx:responseError', function(evt) {
  const status = evt.detail.xhr.status;
  const target = evt.detail.target;
  if (status === 403) {
    target.innerHTML = '<p class="text-red-500 text-sm">Session expired — please refresh.</p>';
  } else if (status >= 500) {
    target.innerHTML = '<p class="text-gray-400 text-sm">Temporarily unavailable. <a href="#" onclick="location.reload()" class="underline">Retry</a></p>';
  }
});
```

---

## Responsive Design

**Primary target:** Desktop (≥ 1280px width).

| Breakpoint | Behaviour |
|---|---|
| ≥ 1280px | Full two-column layout as shown in Page Layout diagram |
| 1024–1279px | Charts stack vertically; KPI tiles remain single row (scrollable if needed) |
| 768–1023px | Single-column layout; all strips stack vertically; sidebar panels collapse to accordions |
| < 768px | Degraded — table horizontal scroll only; charts scale down; a "best viewed on desktop" banner shown |

No mobile-specific route — N-01 is a staff-facing operational dashboard; institution-facing portal has its own mobile app.

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `l` | Go to Legal Dashboard (N-01) |
| `g` `c` | Go to Contract Management (N-02) |
| `g` `d` | Go to Data Privacy / DPDP (N-03) |
| `g` `r` | Go to Regulatory Filings (N-04) |
| `g` `p` | Go to POCSO Registry (N-05) |
| `g` `o` | Go to Policy Repository (N-06) |
| `g` `z` | Go to Compliance Calendar (N-07) |
| `p` | Open period selector (focus the dropdown) |
| `r` | Trigger `?nocache=true` refresh (Legal Officer #75 + DPO #76 only) |
| `c` | Clear all filters and reset dashboard to default view |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |
