# 28 — Integration Health Monitor

- **URL:** `/group/it/integrations/health/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group EduForge Integration Manager (Role 58, G4) — Primary; Group IT Director (Role 53, G4) — Read-only

---

## 1. Purpose

The Integration Health Monitor is the real-time operational dashboard for all EduForge integrations. While the Integration Registry (page 24) provides configuration and management, this page provides the live view: is everything working right now? It answers that question for every integration simultaneously, auto-refreshing every 2 minutes without manual intervention.

The monitor displays uptime percentages, live latency readings, error counts in the last 1 and 24 hours, and a chronological incident timeline for the last 20 events across all integrations. When any integration fails, the IT Director and Integration Manager receive an immediate in-app notification. On this page, failed integrations are shown prominently at the top of the table regardless of sort order, with red status indicators.

This page is designed for incident response. When a branch calls to report that fee payments are failing or that WhatsApp notifications are not going out, the IT Director's first action is to open this page. Within seconds they can see the affected integration's status, latency spike, and error count — and decide whether to escalate to the Integration Manager for remediation or contact the third-party provider.

The page does not stream data via WebSockets. Auto-refresh is implemented via HTMX polling (`hx-trigger="every 2m"`) which re-fetches the integration status data from PostgreSQL health_check_log records. The polling interval is deliberately set at 2 minutes rather than lower to avoid excessive read load on the database from health check logging writes occurring simultaneously.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group EduForge Integration Manager | G4 | Full read + trigger health checks | Can trigger "Test Now" manually |
| Group IT Director | G4 | Read-only | Can view all health data; cannot trigger tests |
| Group IT Admin | G4 | Read-only | Informational access for operational awareness |
| Group Cybersecurity Officer (Role 56, G1) | G1 | Read-only (status and uptime only) | Error log content not visible |
| Group Data Privacy Officer (Role 55, G1) | G1 | Hidden | No access |
| Group IT Support Executive (Role 57, G3) | G3 | Hidden | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Integrations → Health Monitor
```

### 3.2 Page Header
- **Title:** `Integration Health Monitor`
- **Subtitle:** `Auto-refreshes every 2 minutes · Last updated: [timestamp] · [N] Integrations monitored`
- **Role Badge:** `Group EduForge Integration Manager`
- **Right-side controls:** `Refresh Now` button · `Test All Integrations` button (Integration Manager only)
- **Auto-refresh indicator:** Small spinning icon with "Live" badge while polling is active

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any integration currently Failed | "[N] integration(s) are CURRENTLY FAILING. Immediate action required. Affected integrations: [list]." | Red (non-dismissible) |
| Any integration Degraded (high latency or elevated errors) | "[N] integration(s) showing degraded performance. Review health table." | Amber |
| An integration has been failing for >30 minutes | "Integration '[Name]' has been failing for [N] minutes. Consider contacting provider or disabling." | Red (non-dismissible) |
| No health check data for >10 minutes | "Health monitoring data is stale. Last successful fetch was [N] minutes ago. Monitoring may be impaired." | Red |

---

## 4. KPI Summary Bar

One status card per integration type, showing the health of the most critical integration within each type:

| Card | Integration Type | Metric Shown | Colour Rule |
|---|---|---|---|
| WhatsApp API | Communication | Status + Uptime (7d) % | Green/Amber/Red |
| SMS Gateway | Communication | Status + Uptime (7d) % | Green/Amber/Red |
| Payment Gateway | Finance | Status + Uptime (7d) % | Green/Amber/Red |
| Cloudflare R2 Storage | Storage | Status + Uptime (7d) % | Green/Amber/Red |
| Auth API (Google/SSO) | Identity | Status + Uptime (7d) % | Green/Amber/Red |
| Government APIs | Gov/Compliance | Status + Uptime (7d) % | Green/Amber/Red |

Each card is a coloured circle (green = operational, amber = degraded, red = down) with the integration name, uptime %, and current latency in ms. Cards are ordered by criticality (Payment Gateway first as its failure has highest operational impact). Clicking a status card filters the main table to show only that integration type.

---

## 5. Main Table — Integration Health Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Integration Name | Text | Yes | Yes (text search) |
| Status | Badge (Operational / Degraded / Failed / Inactive) — Failed rows pinned to top | Yes | Yes (multi-select) |
| Uptime (7d) % | Percentage — green ≥99%, amber 95–98.9%, red <95% | Yes | No |
| Avg Latency (ms) | Number — green <200ms, amber 200–500ms, red >500ms | Yes | No |
| Error Count (1h) | Number — green 0, amber 1–5, red >5 | Yes | No |
| Error Count (24h) | Number — green 0, amber 1–10, red >10 | Yes | No |
| Last Success | Datetime (relative — "12 min ago") | Yes | No |
| Last Failure | Datetime (relative — "3h ago" or "Never") | Yes | No |
| Actions | Test Now / View Incidents | No | No |

### 5.1 Filters
- Status: Operational / Degraded / Failed / Inactive
- Integration Type: WhatsApp / SMS / Payment / OAuth / Storage / Gov / LMS / Custom

### 5.2 Search
- Integration name; 300ms debounce

### 5.3 Pagination
- Server-side · 25 rows/page (typically all integrations fit on 1–2 pages)

### 5.4 Sort Behaviour
- Default sort: Failed first, then Degraded, then Operational — overrides other sort columns
- Secondary sort: Alphabetical by integration name within each status group

---

## 6. Drawers

### 6.1 Drawer: `integration-test` — Test Now
- **Trigger:** Actions → Test Now
- **Width:** 480px
- Same behaviour as described in Integration Registry (page 24) test drawer
- Shows: Integration name, type, last health check result
- Test button: triggers live connectivity check; result shown inline
- Saves result to health_check_log; updates main table row on close

### 6.2 Drawer: `integration-incidents` — View Incidents
- **Trigger:** Actions → View Incidents
- **Width:** 720px
- **Header:** Integration name, type, current status
- **Incident list:** All recorded incidents for this integration — most recent first
  - Each incident shows: Start time, End time (or "Ongoing"), Duration, Severity (Critical/High/Medium), Description, Resolution notes
- **Tabs within drawer:**
  - Incidents (default)
  - Latency History (last 24h — data table of hourly avg latency readings)
  - Error Log (last 50 error events — timestamp, error code, message)

---

## 7. Charts

### 7.1 Latency Trend per Integration (Line Chart)
- X-axis: Time (last 24h, hourly data points)
- Y-axis: Average latency in ms
- One line per integration (colour-coded)
- Reference lines: 200ms (amber threshold), 500ms (red threshold)
- Positioned below main table

### 7.2 Error Rate per Integration (Grouped Bar Chart)
- X-axis: Integration names (abbreviated)
- Y-axis: Error count
- Two bar groups per integration: Last 1h (darker) / Last 24h (lighter)
- Colour coded: green 0, amber 1–10, red >10
- Positioned beside latency trend chart

---

## 8. Incident Timeline

A dedicated section below the charts showing the last 20 incidents across ALL integrations in reverse chronological order:

| Column | Content |
|---|---|
| Time | Start datetime (relative + absolute on hover) |
| Integration | Integration name (link to View Incidents drawer) |
| Severity | Badge (Critical / High / Medium / Low) |
| Description | Brief incident description (max 120 chars) |
| Duration | Time between start and resolution (or "Ongoing") |
| Resolution | "Resolved" / "Ongoing" / "Auto-recovered" |

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Auto-refresh completed | (No toast — silent refresh; last updated timestamp updates) | — | — |
| Manual Refresh Now | "Health data refreshed." | Info | 2s |
| Test Now passed | "Health check passed for '[Name]'. Latency: [N]ms." | Success | 4s |
| Test Now failed | "Health check FAILED for '[Name]'. Error: [message]." | Error | 6s |
| Test All triggered | "Running health checks for all [N] integrations. Table will update on next refresh." | Info | 5s |

---

## 10. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No integrations configured | "No Integrations to Monitor" | "Add integrations in the Integration Registry before monitoring health." | Go to Registry |
| No incidents recorded | "No Incidents" | "No incidents have been recorded across any integration." | — |
| All operational | "All Systems Operational" | "Every monitored integration is healthy with normal latency and zero errors." | — |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Status cards shimmer (6 cards) + table skeleton (8 rows) + chart area shimmer |
| Auto-refresh (every 2min) | Subtle table row shimmer; status cards flash briefly; charts update without full reload |
| Manual Refresh Now | Full table skeleton shimmer while data fetches |
| Test Now in drawer | Spinner: "Running health check…" |
| Test All | Top of page progress bar: "Checking [N] of [Total]…" |
| View Incidents drawer | Drawer spinner; incident list loads progressively |

---

## 12. Role-Based UI Visibility

| Element | Integration Manager (G4) | IT Director (G4) | IT Admin (G4) | Cybersecurity Officer (G1) |
|---|---|---|---|---|
| Test Now Action | Visible | Hidden | Hidden | Hidden |
| Test All Integrations button | Visible | Hidden | Hidden | Hidden |
| View Incidents Action | Visible | Visible | Visible | Hidden |
| Error Log in drawer | Visible | Visible | Visible | Hidden |
| Latency History in drawer | Visible | Visible | Visible | Hidden |
| Latency + Error Charts | Visible | Visible | Visible | Hidden |
| Incident Timeline section | Visible | Visible | Visible | Hidden |
| Uptime % (KPI cards) | Visible | Visible | Visible | Visible |
| Status badges | Visible | Visible | Visible | Visible |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/health/` | JWT (G4+) | Paginated health status for all integrations |
| GET | `/api/v1/it/health/kpis/` | JWT (G4+) | Status card data (one card per integration type) |
| POST | `/api/v1/it/health/{integration_id}/test/` | JWT (G4 — Integration Manager) | Trigger live health check |
| POST | `/api/v1/it/health/test-all/` | JWT (G4 — Integration Manager) | Test all integrations |
| GET | `/api/v1/it/health/{integration_id}/incidents/` | JWT (G4+) | Incident history for an integration |
| GET | `/api/v1/it/health/{integration_id}/latency-history/` | JWT (G4+) | Hourly avg latency for last 24h |
| GET | `/api/v1/it/health/{integration_id}/error-log/` | JWT (G4+) | Last 50 error events |
| GET | `/api/v1/it/health/incident-timeline/` | JWT (G4+) | Last 20 incidents across all integrations |
| GET | `/api/v1/it/health/charts/latency-trend/` | JWT (G4+) | Latency trend chart data (last 24h, all integrations) |
| GET | `/api/v1/it/health/charts/error-rate/` | JWT (G4+) | Error rate bar chart data (1h and 24h, all integrations) |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Auto-refresh status cards | `every 2m` | GET `/api/v1/it/health/kpis/` | `#status-cards` | `innerHTML` |
| Auto-refresh health table | `every 2m` | GET `/api/v1/it/health/` | `#health-table` | `innerHTML` |
| Auto-refresh incident timeline | `every 2m` | GET `/api/v1/it/health/incident-timeline/` | `#incident-timeline` | `innerHTML` |
| Manual Refresh Now | `click` on Refresh Now | GET `/api/v1/it/health/` | `#health-page-content` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/health/?status=...` | `#health-table` | `innerHTML` |
| Search integrations | `input` (300ms debounce) | GET `/api/v1/it/health/?q=...` | `#health-table` | `innerHTML` |
| Test Now in drawer | `click` on Test Now | POST `/api/v1/it/health/{id}/test/` | `#test-result-panel` | `innerHTML` |
| Open incidents drawer | `click` on View Incidents | GET `/api/v1/it/health/{id}/incidents/` | `#health-drawer` | `innerHTML` |
| Load latency history tab | `click` on tab | GET `/api/v1/it/health/{id}/latency-history/` | `#drawer-tab-content` | `innerHTML` |
| Load charts | `load` | GET `/api/v1/it/health/charts/latency-trend/` | `#latency-chart` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/health/?page=N` | `#health-table` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- Integration status changes to DOWN: Integration Manager + IT Admin (in-app red non-dismissible + email) immediately
- Latency > 500ms for any integration: Integration Manager (in-app amber + email)
- Incident severity escalated to Critical: Integration Manager + IT Director (in-app red non-dismissible + email + WhatsApp)
- Integration auto-recovered: Integration Manager (in-app green info + email)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
