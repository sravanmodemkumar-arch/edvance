# Page 50: System Health Monitor

**URL:** `/group/it/monitoring/health/`
**Roles:** Group IT Director (Role 53, G4); Group EduForge Integration Manager (Role 58, G4)
**Priority:** P0
**Division:** F — Group IT & Technology

---

## 1. Purpose

Real-time overview of all EduForge system components' health and operational status. This is the primary command dashboard for understanding whether the EduForge platform is functioning correctly across all services. It is used during incidents to identify which components are affected and to track recovery progress.

**Services monitored:**

| Service | Type | Description |
|---------|------|-------------|
| Auth API (Lambda) | AWS Lambda | Authentication service — JWT issuance and validation |
| Tenant API (Lambda) | AWS Lambda | Tenant configuration and routing |
| Home API (Lambda) | AWS Lambda | Home/landing page service |
| Student Portal | Django (EC2/Container) | Main student-facing portal |
| Admin Portal | Django (EC2/Container) | Staff and admin portal (this portal) |
| Identity Service | FastAPI | User identity, role management, token service |
| PostgreSQL DB | RDS/Managed DB | Primary database for all tenant data |
| Cloudflare R2 | Object Storage | Document and media storage |
| Cloudflare CDN | CDN | Static assets and cached content delivery |

The page auto-refreshes every 2 minutes via HTMX polling to reflect the latest service status. Metrics are sourced from health check endpoints and stored in PostgreSQL (not cached).

IT Director (Role 53), IT Admin (Role 54), and Integration Manager (Role 58) use this page during incidents, for daily operational checks, and for reporting uptime to management.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Director (Role 53, G4) | Full access | View + acknowledge incidents + export reports |
| Group EduForge Integration Manager (Role 58, G4) | Full access | View + acknowledge integration-related incidents |
| Group IT Admin (Role 54, G4) | View + acknowledge | Can view and acknowledge alerts |
| Group Cybersecurity Officer (Role 56, G1) | Read-only | View current status; cannot acknowledge |
| All other roles | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | View-only | Can view health status; cannot acknowledge alerts or create incidents |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > System Monitoring > Health Monitor`

**Page Header:**
- Title: `System Health Monitor`
- Subtitle: `Real-time service status — EduForge platform`
- Right: `Last Refreshed: [timestamp]` (auto-updates on each HTMX poll) + `Refresh Now` button + `Export Uptime Report (PDF)`

**Auto-Refresh Notice (below header):**
Small info chip: `Auto-refreshing every 2 minutes. Last refresh: [time].`

**Alert Banners:**

1. **Service DOWN** (red, non-dismissible):
   - Condition: any service with status = DOWN
   - Text: `SERVICE DOWN — [Service Name] is not responding. Incident auto-logged. Investigate immediately. [View Active Incidents →]`
   - Auto-links to incident register (Page 40) with pre-filled incident

2. **Service DEGRADED >10 Minutes** (amber, non-dismissible while degraded):
   - Condition: service with status = DEGRADED and first_degraded_at < now - 10 minutes
   - Text: `[Service Name] has been degraded for [X] minutes. Users may experience slow performance. Monitor closely.`

**Page Structure:**
1. Alert banners (top)
2. Status Grid (service cards)
3. Active Incidents strip
4. Service Health History Table
5. Charts (bottom)

---

## 4. KPI Summary Bar

No traditional KPI cards on this page. Instead, the top section is the **Status Grid** which serves as both KPI indicator and primary visual focus.

**Aggregate status line (above status grid):**
- `All Services Operational` (green chip) OR `[X] Services DOWN, [Y] Degraded` (red/amber chips)
- `Overall Uptime (30d): [X]%`

Clicking the "[X] Services DOWN" or "[Y] Degraded" chips filters the Service Health History table to show only DOWN or DEGRADED entries respectively.

---

## 5. Main Table — Service Health History

**Positioned below the Status Grid and Active Incidents section.**

**Table Title:** `Service Health History`
**Description:** Paginated log of health check results for all services.

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Service | Text + badge | Service name with service type badge |
| Timestamp | DateTime | When health check was performed |
| Status | Badge | Operational (green) / Degraded (amber) / Down (red) / Unknown (grey) |
| Response Time (ms) | Number | Response time for health check ping; red if > 3000ms |
| Error Code | Text | HTTP error code or error type if not Operational; `—` if OK |
| Note | Text | Auto-generated note (e.g., "Timeout after 30s") or manual note |
| Actions | Button | `View Full Detail` |

### Filters

- **Service:** All / specific service dropdown
- **Status:** All / Operational / Degraded / Down
- **Date Range:** From/to datetime

### Search

No search on this table (structured data, filter-based navigation).

### Pagination

Server-side, 50 rows per page. `hx-get="/group/it/monitoring/health/history/?page=N"`, targets `#health-history-table`.

### Sorting

Default sort: Timestamp descending (most recent first). No user sorting.

---

## 6. Drawers

### A. Service Detail Drawer (560px, right-side)

Triggered by clicking a service card in the Status Grid or `View Full Detail` in history table.

**Drawer Header:** `[Service Name] — Health Detail`

**Sections:**

**Current Status:**
- Status badge (large) + Response time (last check)
- Uptime last 24h / 7d / 30d (calculated from history table)
- Last check: [timestamp]
- Last incident: [incident # + date] or `No recent incidents`

**Response Time Trend (last 24h):**
- Mini line chart within the drawer (last 24h, hourly data points)
- Marks any DOWN/DEGRADED periods in red/amber

**Recent Health Check Log (last 20 entries):**
- Timestamp / Status / Response Time (ms) / Error Code

**Active Incident (if any):**
- Link to incident in the Security Incident Register

**Footer:** `Close` | `Create Incident` (Role 53/54 — opens incident creation pre-filled with this service)

---

### B. Acknowledge Alert (inline — no drawer)

Alert banners have an `Acknowledge` button (Role 53/54 only). Acknowledgement records:
- Acknowledged by (actor)
- Timestamp
- Acknowledgement note (brief text field in a small modal)

Acknowledged alerts collapse to a smaller warning state but are not dismissed until the service is restored.

**Audit:** Alert acknowledgments are logged to the IT Audit Log with actor user ID, timestamp, service affected, and acknowledgement note.

---

## 7. Status Grid

**Positioned prominently at the top of the page content area, below the header.**

One card per service (9 cards total), in a 3-column responsive grid (collapses to 2 on tablet, 1 on mobile).

**Each Service Card contains:**
- Service name (bold)
- Service type (small text — Lambda / Django / FastAPI / PostgreSQL / Cloudflare)
- Status circle (large coloured dot): Green = Operational, Amber = Degraded, Red = Down, Grey = Unknown
- Status label: `Operational` / `Degraded` / `Down` / `Unknown`
- Uptime % (last 30 days): small text below status
- Response time (last check): `[X] ms` — red if > 3000ms
- `View Details` button → opens Service Detail Drawer

**Status Grid auto-refreshes every 2 minutes:**
```html
<div id="service-grid"
     hx-get="/group/it/monitoring/health/status-grid/"
     hx-trigger="load, every 2m"
     hx-target="#service-grid">
</div>
```

---

## 8. Active Incidents Strip

Below the Status Grid, a compact strip shows currently open incidents linked to system health (from the Security Incident Register filtered to type = Performance/Availability):

| Incident # | Service | Severity | Status | Duration | Actions |
|-----------|---------|---------|--------|---------|---------|
| INC-2026-042 | PostgreSQL DB | 2-High | Investigating | 1h 23m | View → |

If no active incidents: `No active system incidents.` (green text).

---

## 9. Charts

Two charts below the health history table in a 2-column grid.

### Chart 1: Response Time Trend Per Service (Last 24 Hours)
- **Type:** Multi-series line chart
- **Series:** One line per service (up to 9 services; toggleable legend to show/hide individual services)
- **X-axis:** Last 24 hours (hourly data points)
- **Y-axis:** Response time in milliseconds
- **Reference line:** 3000ms threshold (red dashed)
- **Purpose:** Identify degradation patterns across services — is one service consistently slow?
- **Data endpoint:** `/api/v1/it/monitoring/health/charts/response-trend/`
- **Filter:** Service multi-select

### Chart 2: Uptime Comparison (Last 30 Days)
- **Type:** Horizontal bar chart
- **Y-axis:** Service names
- **X-axis:** Uptime % (0–100%)
- **Colour:** Green ≥ 99.9%, amber 99–99.8%, red < 99%
- **Reference line:** 99.9% SLA target (dashed)
- **Purpose:** Compare all services' availability at a glance; identify chronic underperformers
- **Data endpoint:** `/api/v1/it/monitoring/health/charts/uptime-comparison/`

---

## 10. Toast Messages

| Action | Toast |
|--------|-------|
| Alert acknowledged | Info: `Alert acknowledged. Monitoring continues until service is restored.` |
| Manual refresh triggered | Info: `Health data refreshed.` |
| Export report initiated | Info: `Generating uptime report — please wait.` |
| Incident auto-created on DOWN | System: `Service DOWN detected. Incident [INC-#] auto-created and IT Admin notified.` |
| Service restored (auto) | Success: `[Service Name] is back to Operational status. (Auto-detected)` |
| Alert acknowledge failed | Error: `Failed to acknowledge alert. Please try again.` | Error | 5s |
| Manual refresh failed | Error: `Failed to refresh health data. Please try again.` | Error | 5s |
| Incident creation failed | Error: `Failed to create incident. Please try again.` | Error | 5s |

---

## 11. Empty States

| Condition | Message |
|-----------|---------|
| No health check data | Status grid shows all service cards with status = `Unknown`. Text: `Health check data not available. Ensure health monitoring service is running.` |
| History table empty (new deployment) | `No health history recorded yet. History will appear after the first monitoring cycle.` |
| Chart insufficient data | `Not enough data to display. Check back after monitoring runs for 24 hours.` |
| No active incidents | Active Incidents strip: `No active system incidents.` |

---

## 12. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| Status grid (initial load) | 9 skeleton service cards with shimmer |
| Status grid (auto-refresh) | Cards swap seamlessly — no full skeleton; changed cards briefly flash |
| Health history table | 5 skeleton rows |
| Service detail drawer | Spinner then content renders |
| Mini chart in drawer | Spinner then chart renders |
| Main charts | Spinner in chart containers |
| Export button | `Generating...` text + disabled |

---

## 13. Role-Based UI Visibility

| UI Element | Role 53/58 (G4) | Role 54 (G4) | Role 56 (G1) |
|------------|----------------|-------------|-------------|
| Status Grid | Visible | Visible | Visible |
| Alert banners | Visible | Visible | Visible |
| Acknowledge button | Visible | Visible | Hidden |
| Service Detail drawer | Visible | Visible | Visible |
| Create Incident (in drawer) | Visible | Visible | Hidden |
| Health History table | Visible | Visible | Visible |
| Charts | Visible | Visible | Visible |
| Export Uptime Report | Visible | Visible | Hidden |
| Active Incidents strip | Visible | Visible | Visible |

---

## 14. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/monitoring/health/status/` | Fetch current status for all services |
| GET | `/api/v1/it/monitoring/health/history/` | Fetch health check history (paginated) |
| GET | `/api/v1/it/monitoring/health/services/{service_id}/` | Fetch service detail + 24h history |
| POST | `/api/v1/it/monitoring/health/acknowledge/` | Acknowledge an alert |
| GET | `/api/v1/it/monitoring/health/incidents/active/` | Active incidents linked to health events |
| GET | `/api/v1/it/monitoring/health/charts/response-trend/` | Response time trend (24h) |
| GET | `/api/v1/it/monitoring/health/charts/uptime-comparison/` | 30-day uptime comparison |
| GET | `/api/v1/it/monitoring/health/export/pdf/` | Uptime report PDF |

**Health Check Data Collection:**
Health check data is collected by a background monitoring worker (Django management command or Celery task, runs every 2 minutes) that pings each service's `/health` endpoint and writes results to the `service_health_checks` PostgreSQL table. The frontend reads from this table — no live proxying of health checks through the frontend.

---

## 15. HTMX Patterns

```html
<!-- Status grid — auto-refresh every 2 minutes -->
<div id="service-grid"
     hx-get="/group/it/monitoring/health/status-grid/"
     hx-trigger="load, every 2m"
     hx-target="#service-grid"
     hx-swap="innerHTML"
     hx-indicator="#grid-loader">
  <div id="grid-loader" class="htmx-indicator"><!-- shimmer cards --></div>
</div>

<!-- Active incidents strip — auto-refresh every 2 minutes -->
<div id="active-incidents-strip"
     hx-get="/group/it/monitoring/health/active-incidents/"
     hx-trigger="load, every 2m"
     hx-target="#active-incidents-strip"
     hx-swap="innerHTML">
</div>

<!-- Last refreshed timestamp (updates with each auto-refresh) -->
<span id="last-refreshed"
      hx-get="/group/it/monitoring/health/last-refreshed/"
      hx-trigger="load, every 2m"
      hx-target="#last-refreshed"
      hx-swap="innerHTML">
</span>

<!-- Manual refresh -->
<button hx-get="/group/it/monitoring/health/status-grid/"
        hx-target="#service-grid"
        hx-swap="innerHTML"
        hx-on::after-request="updateLastRefreshed()">
  Refresh Now
</button>

<!-- Service detail drawer -->
<button hx-get="/group/it/monitoring/health/services/{{ service.id }}/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  View Details
</button>

<!-- Health history table -->
<div id="health-history-table"
     hx-get="/group/it/monitoring/health/history/"
     hx-trigger="load"
     hx-target="#health-history-table"
     hx-include="#health-filter-form">
</div>

<!-- Charts — load once on page load -->
<div id="chart-response-trend"
     hx-get="/group/it/monitoring/health/charts/response-trend/"
     hx-trigger="load"
     hx-target="#chart-response-trend">
</div>

<div id="chart-uptime"
     hx-get="/group/it/monitoring/health/charts/uptime-comparison/"
     hx-trigger="load"
     hx-target="#chart-uptime">
</div>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
