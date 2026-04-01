# Page 38: Cybersecurity Dashboard

**URL:** `/group/it/security/overview/`
**Role:** Group Cybersecurity Officer (Role 56, G1) — read-only
**Priority:** P0
**Division:** F — Group IT & Technology

---

## 1. Purpose

Read-only security posture overview across all branches of the EduForge group. Aggregates security incidents, device compliance rates, phishing simulation results, staff security training completion, access anomalies, and vulnerability exposure into a single command-centre view.

The Group Cybersecurity Officer (Role 56, G1) cannot make configuration changes — this is a monitoring and reporting page only. The Officer uses this dashboard to:
- Monitor the group's real-time security posture
- Identify branches that are underperforming on security metrics
- Write security reports for the IT Director and Board
- Recommend remediation actions to the Group IT Director (Role 53, G4) and Group IT Admin (Role 54, G4)

This page is the primary daily-check page for Role 56 and is accessible 24/7. All data is sourced directly from PostgreSQL — no caching layer.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group Cybersecurity Officer (Role 56, G1) | Read-only | No create/edit/delete actions anywhere on this page |
| Group IT Director (Role 53, G4) | Read + export | Can also view this page |
| Group IT Admin (Role 54, G4) | Read + export | Can also view this page |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

> G1 = read-only across the entire division. No action buttons are rendered for Role 56 anywhere on this page.

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > Cybersecurity > Overview`

**Page Header:**
- Title: `Cybersecurity Overview`
- Subtitle: `Group-wide security posture — read-only monitoring view`
- Right side: `Last Refreshed: [timestamp]` + `Refresh` button (triggers full page reload via HTMX `hx-get`)
- Export button: `Export Report (PDF)` — generates a printable summary report

**Alert Banners (top of page, before KPIs):**

1. **Active Severity 1 Incident** (red, non-dismissible):
   - Condition: any open incident with severity = 1 (Critical)
   - Text: `ACTIVE SEVERITY 1 INCIDENT — [Incident #] [Branch] — [Incident Type] — Opened [X] hours ago. View incident →`
   - Only dismissible by IT Admin/Director once the incident is resolved

2. **Low Group Security Training** (amber, dismissible per session):
   - Condition: group-wide security training completion < 80%
   - Text: `Security awareness training completion is [X]% group-wide — below the 80% mandatory threshold. [X] staff overdue.`

3. **High Phishing Click Rate** (amber, dismissible per session):
   - Condition: phishing click rate > 20% in any branch in the last simulation
   - Text: `[Branch Name] recorded a [X]% phishing click rate in the last simulation — above the 20% alert threshold.`

---

## 4. KPI Summary Bar

Six KPI cards, rendered in a 6-column responsive grid (collapses to 2-column on mobile).

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Security Score | Weighted average across all branches (0–100). Weights: incidents 30%, device compliance 25%, training 20%, phishing 15%, vulnerabilities 10% | Large number, colour coded: ≥80 green, 60–79 amber, <60 red |
| 2 | Open Incidents | Count of incidents with status ≠ Resolved/Closed | Large number, red if > 0 |
| 3 | Devices Compliant % | compliant_devices / total_registered_devices × 100 | % with progress ring, red if < 85% |
| 4 | Staff Security Training % | staff_completed_mandatory_training / total_staff_with_access × 100 | % with progress ring, amber if < 80% |
| 5 | Phishing Click Rate % | clicks / recipients × 100 from the most recent completed simulation | % — red if > 20%, amber if 10–20%, green if < 10% |
| 6 | High Severity Vulnerabilities | Count of open vulnerabilities with CVSS ≥ 7.0 (High + Critical) | Count, red if > 0 |

All KPI cards are read-only for Role 56. No click-through navigation for G1 (no action links rendered).

---

## 5. Main Table — Branch Security Health

**Table Title:** `Branch Security Health`
**Description:** One row per branch showing aggregated security metrics.

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Branch Name | Text | Branch display name |
| Security Score | Number (0–100) | Colour-coded badge: ≥80 green, 60–79 amber, <60 red |
| Incidents Open | Number | Count of open incidents for this branch |
| Devices Compliant % | % | Device compliance rate for branch |
| Training % | % | Security training completion rate for branch |
| Last Phishing Sim Date | Date | Date of most recent completed phishing simulation |
| Phishing Click % | % | Click rate from most recent simulation |
| Last Audit Date | Date | Date of most recent access control audit |
| Risk Level | Badge | Derived: Low (score ≥80) / Medium (60–79) / High (<60 or open Sev1 incident) |
| Actions | Buttons | `View Branch Detail` — opens View Drawer (Role 56: read-only) |

### Filters

- **Branch:** Multi-select dropdown (all branches)
- **Risk Level:** All / Low / Medium / High
- **Has Open Incidents:** Yes / No
- **Training Below 80%:** Toggle checkbox

### Search

Full-text search on branch name. `hx-trigger="keyup changed delay:400ms"`, targets `#branch-security-table`.

### Pagination

Server-side, 20 rows per page. Controls: Previous / Page X of Y / Next. `hx-get="/group/it/security/overview/table/?page=N"`, targets `#branch-security-table`.

### Sorting

Sortable columns: Security Score, Risk Level, Incidents Open, Devices Compliant %, Training %, Phishing Click %. Default sort: Security Score ascending (worst first).

---

## 6. Drawers

### View Branch Detail Drawer (560px, right-side)

Triggered by `View Branch Detail` button in table. Read-only for all roles on this page.

**Drawer Header:** `[Branch Name] — Security Detail`

**Sections:**

**Security Score Breakdown:**
- Score: [X]/100 (badge colour)
- Component scores: Incidents (X/30), Device Compliance (X/25), Training (X/20), Phishing (X/15), Vulnerabilities (X/10)

**Open Incidents:**
- List of open incidents for this branch: Incident #, Type, Severity badge, Opened Date, Status
- Link: `View All Incidents →` (navigates to `/group/it/security/incidents/` filtered by branch)

**Device Compliance:**
- Compliant: X devices
- Non-Compliant: X devices
- Unregistered: X devices
- Link: `View Device Register →`

**Training Summary:**
- Completion rate %
- Overdue count
- Link: `View Training →`

**Last Phishing Simulation:**
- Campaign name, date, click rate %, outcome
- Link: `View Simulation →`

**Vulnerabilities:**
- Open critical: X, Open high: X
- Link: `View Vulnerabilities →`

**Footer:** `Close` button only (no edit/save for G1 or on this page).

---

## 7. Charts

Three charts rendered below the main table, in a responsive 2-column grid (chart 1 spans full width, charts 2–3 side by side).

### Chart 1: Security Score Trend (Full Width)
- **Type:** Line chart
- **Series:** Group Average Score (solid line, blue), Worst Branch Score (dashed line, red)
- **X-axis:** Last 12 months (month labels)
- **Y-axis:** Score 0–100
- **Purpose:** Show whether group security posture is improving or deteriorating over time
- **Filter:** None (always shows group-level)

### Chart 2: Incident Severity Breakdown
- **Type:** Stacked bar chart
- **X-axis:** Last 6 months
- **Y-axis:** Incident count
- **Series (stacked):** Severity 1 (Critical — red), Severity 2 (High — orange), Severity 3 (Medium — amber), Severity 4 (Low — grey)
- **Purpose:** Track whether the group is experiencing more high-severity incidents over time

### Chart 3: Training Completion by Role Category
- **Type:** Horizontal bar chart
- **Y-axis:** Role categories (Academic, Administrative, Finance, Operations, IT, Management)
- **X-axis:** Completion % (0–100%)
- **Colour:** Green if ≥80%, amber if 60–79%, red if <60%
- **Purpose:** Identify which staff categories are most at-risk for security awareness gaps

All charts are rendered server-side data via HTMX fetch on page load. Chart data endpoint: `/group/it/security/overview/charts/`. No export on charts for Role 56.

---

## 8. Toast Messages

No create/edit/delete operations exist on this page (read-only for all users). Toasts are only triggered by:

| Action | Toast |
|--------|-------|
| Report export initiated | Info: `Generating PDF report — this may take a few seconds.` |
| Report export complete | Success: `Security overview report downloaded.` |
| Page refresh (manual) | Info: `Data refreshed as of [timestamp].` |
| Session alert dismissed | Info: `Alert hidden for this session.` |

---

**Audit Trail:** Alert acknowledgments from this dashboard are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications for Critical Events:**
- Severity 1 incident open: Cybersecurity Officer (in-app non-dismissible + email + WhatsApp) + IT Director (in-app + email) + IT Admin (email) immediately
- Device compliance < 80%: Cybersecurity Officer (in-app amber) + IT Admin (email)
- Phishing click rate > 20%: Cybersecurity Officer (in-app amber) + IT Director (email) + IT Admin (email)
- Training completion < 70%: Cybersecurity Officer (in-app amber) + IT Admin (email)

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No branches in system | Icon + `No branch data available. Contact IT Admin to configure branches.` |
| No phishing simulations run | Phishing columns show `—` with tooltip `No simulation run yet` |
| No incidents logged | Incidents columns show `0` (green badge) |
| Chart data unavailable (< 2 data points) | Chart area shows: `Insufficient data — requires at least 2 months of data to display trend.` |
| No vulnerabilities | `No open vulnerabilities logged.` in vulnerability section of branch drawer |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI cards | Skeleton shimmer cards (6 placeholders) during initial load |
| Branch security table | Skeleton rows (5 placeholder rows with shimmer animation) |
| Charts | Spinner centred in chart container with `Loading chart data...` label |
| Branch detail drawer | Spinner centred while data fetches; sections render progressively |
| Manual refresh button | Button shows `Refreshing...` and is disabled during fetch |

All loaders use Tailwind `animate-pulse` for skeleton states. HTMX `hx-indicator` targets dedicated `#kpi-loader`, `#table-loader` divs.

---

## 11. Role-Based UI Visibility

| UI Element | Role 56 (G1) | Role 53/54 (G4) |
|------------|-------------|-----------------|
| KPI cards | Visible, read-only | Visible, read-only |
| Branch security table | Visible, read-only | Visible, read-only |
| View Branch Detail button | Visible (read-only drawer) | Visible (read-only drawer) |
| Alert banners | Visible (cannot dismiss Sev1) | Visible (cannot dismiss Sev1) |
| Export PDF button | Visible | Visible |
| Any create/edit/delete | Hidden (not rendered) | Hidden (this page is read-only) |
| Chart filters | Not available | Not available |
| Refresh button | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/security/overview/kpis/` | Fetch 6 KPI values |
| GET | `/api/v1/it/security/overview/branches/` | Fetch branch security health table (paginated) |
| GET | `/api/v1/it/security/overview/branches/{branch_id}/` | Fetch branch detail for drawer |
| GET | `/api/v1/it/security/overview/charts/score-trend/` | Security score trend data (12 months) |
| GET | `/api/v1/it/security/overview/charts/incident-severity/` | Incident severity breakdown (6 months) |
| GET | `/api/v1/it/security/overview/charts/training-by-role/` | Training completion by role category |
| GET | `/api/v1/it/security/overview/export/pdf/` | Generate and return PDF report |
| GET | `/api/v1/it/security/overview/alerts/` | JWT (G1+) | Fetch active alert banners (Severity 1 incidents, training status, phishing rate) |

**Query Parameters (branches table):**
- `page` (int), `page_size` (int, default 20)
- `branch_id` (UUID, optional filter)
- `risk_level` (low/medium/high)
- `has_open_incidents` (bool)
- `training_below_80` (bool)
- `search` (string — branch name)
- `sort_by` (field name), `sort_dir` (asc/desc)

All endpoints require JWT authentication. Role 56 receives read-only data; no mutation endpoints are exposed to this role.

---

## 13. HTMX Patterns

```html
<!-- KPI bar — loads on page mount -->
<div id="kpi-bar"
     hx-get="/group/it/security/overview/kpis/"
     hx-trigger="load"
     hx-target="#kpi-bar"
     hx-indicator="#kpi-loader">
  <div id="kpi-loader" class="htmx-indicator"><!-- shimmer --></div>
</div>

<!-- Branch security table with search + filter -->
<div id="branch-security-table"
     hx-get="/group/it/security/overview/branches/"
     hx-trigger="load"
     hx-target="#branch-security-table"
     hx-include="#filter-form">
</div>

<!-- Search input — debounced -->
<input type="text" name="search" placeholder="Search branch..."
       hx-get="/group/it/security/overview/branches/"
       hx-trigger="keyup changed delay:400ms"
       hx-target="#branch-security-table"
       hx-include="#filter-form" />

<!-- Manual refresh button -->
<button hx-get="/group/it/security/overview/"
        hx-target="body"
        hx-swap="outerHTML">
  Refresh
</button>

<!-- View Branch Detail drawer trigger -->
<button hx-get="/group/it/security/overview/branches/{{ branch.id }}/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  View Branch Detail
</button>

<!-- Pagination -->
<button hx-get="/group/it/security/overview/branches/?page={{ next_page }}"
        hx-target="#branch-security-table"
        hx-include="#filter-form">
  Next →
</button>

<!-- Charts — load independently -->
<div id="chart-score-trend"
     hx-get="/group/it/security/overview/charts/score-trend/"
     hx-trigger="load"
     hx-target="#chart-score-trend">
</div>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
