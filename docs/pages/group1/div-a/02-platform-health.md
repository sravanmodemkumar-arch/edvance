# div-a-02 — Platform Health Detail

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Schools | 1,000 · avg 1,000 students · max 5,000 |
| Colleges | 800 · avg 500 · max 2,000 |
| Coaching centres | 100 · avg 10,000 · max 15,000 |
| Groups | 150 · each owns 5–50 child institutions |
| Total institutions | 2,050 · Total students 2.4M–7.6M |
| Peak concurrent users | 500,000 |
| Services monitored | 6 core + 12 sub-services |
| Metrics collected | ~800 (infra + app + business) |
| Alert evaluations/min | ~1,600 (30s interval × 800 metrics) |
| SLA tiers | Standard 99.5% · Professional 99.7% · Enterprise 99.9% |
| Enterprise ARR at risk | ₹15 Cr (coaching centres) |

**Architect's note:** 1 minute of P0 downtime at 500K concurrent peak = 500K disrupted students. A 30-minute P1 for an Enterprise coaching centre = SLA breach → up to ₹1 Cr+ credit obligation. Every metric on this page must have a pre-computed cache with < 5-second staleness during incidents. The page itself must never be the bottleneck during an incident.

---

## 2. Institution Taxonomy — Health Impact

| Type | SLA tier | Breach trigger | Credit rate |
|---|---|---|---|
| School | Standard 99.5% | Downtime > 219 min/month | 5% of MRR per 0.1% below |
| College | Professional 99.7% | Downtime > 131 min/month | 7% of MRR per 0.1% below |
| Coaching centre | Enterprise 99.9% | Downtime > 44 min/month | 10% of MRR per 0.1% below |
| Group | Professional/Enterprise | Inherits tier of majority children | Same as tier |

---

## 3. Page Metadata

| Field | Value |
|---|---|
| Route | `/exec/platform-health/` |
| **Single page API** | **All partials from `/exec/platform-health/?part={name}`** |
| View | `PlatformHealthView` |
| Template | `exec/platform_health_page.html` |
| Priority | P0 |
| Nav group | Operations |
| Roles | `exec`, `ops`, `superadmin` |
| HTMX poll | Stats strip: every 30s · Services grid: every 30s · Incidents: every 60s |

---

## 4. Full Page Wireframe

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ Platform Health              [↺ Refresh]  [Export Report]  [📅 Last 24h ▾] ║
╠══════════╦══════════╦══════════╦══════════╦══════════╦════════════════════╣
║ Platform ║ Avg      ║ P1/P2    ║ SLA      ║ Active   ║ MTTR               ║
║ Uptime   ║ Latency  ║ Incidents║ Breaches ║ Alerts   ║ (30d avg)          ║
║ 99.94%   ║ 142 ms   ║ 0 / 2    ║ 0 (MTD)  ║ 7        ║ 24 min             ║
╠══════════╩══════════╩══════════╩══════════╩══════════╩════════════════════╣
║ SERVICES HEALTH GRID                          [Group by: Service ▾]        ║
║ ┌─────────────────┬──────────┬──────────┬──────────┬──────────────────┐   ║
║ │ Service         │ Status   │ Uptime % │ Latency  │ Error Rate       │   ║
║ ├─────────────────┼──────────┼──────────┼──────────┼──────────────────┤   ║
║ │ ● Exam Engine   │ ✅ OK    │ 99.97%   │ 138ms    │ 0.02%  ████████░ │   ║
║ │ ● Auth Service  │ ✅ OK    │ 99.99%   │  42ms    │ 0.00%  ██████████│   ║
║ │ ● File Storage  │ ⚠ Deg.  │ 99.82%   │ 312ms    │ 0.18%  ███████░░ │   ║
║ │ ● API Gateway   │ ✅ OK    │ 99.96%   │  88ms    │ 0.01%  ██████████│   ║
║ │ ● Email/SMS     │ ✅ OK    │ 99.98%   │ 220ms    │ 0.04%  ████████░ │   ║
║ │ ● Proctoring    │ ✅ OK    │ 99.91%   │ 480ms    │ 0.12%  ████████░ │   ║
║ └─────────────────┴──────────┴──────────┴──────────┴──────────────────┘   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ LATENCY CHART                              [Service ▾] [Range ▾]           ║
║ Chart.js Line · P50 / P95 / P99 · SLA threshold overlay                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ RECENT INCIDENTS                                        [+ New Incident]   ║
║ INC# │ Title │ Severity │ Service │ Status │ Started │ Duration │ ⋯       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 5. Sections — Deep Specification

### 5.1 Page Header

```
[Platform Health]   [↺ Refresh]  [Export Report]  [📅 Last 24h ▾]
```

**[↺ Refresh]:** Fetches all partials. `hx-get="/exec/platform-health/?part=all"` `hx-target="#ph-body"` `hx-swap="innerHTML"`. Spin animation.

**[Export Report]:** Downloads PDF (WeasyPrint). Opens loading spinner, then file download. Async for report > 10 pages. URL: `/exec/platform-health/?part=export&format=pdf&range={{ range }}`

**[📅 Last 24h ▾] date range selector:**
Options: Last 1h · Last 6h · Last 24h (default) · Last 7d · Last 30d · Custom
URL param: `?range=24h`
Triggers `hx-get="/exec/platform-health/?part=all&range=24h"` on change — all sections update.

---

### 5.2 Stats Strip — KPI Cards

**HTMX:** `id="ph-stats"` `hx-get="/exec/platform-health/?part=stats&range={{ range }}"` `hx-trigger="load, every 30s[!document.querySelector('.drawer-open,.modal-open')]"` `hx-swap="innerHTML"`

**Cards:**

| # | Label | Formula | Alert |
|---|---|---|---|
| 1 | Platform Uptime | Weighted avg uptime across all services in range, weighted by request volume | < 99.5% = red; < 99.7% = amber |
| 2 | Avg Latency | P50 across all services in range | > 500ms = amber; > 1s = red |
| 3 | P1 / P2 Incidents | Count of P1 active / Count of P2 active (format: "0 / 2") | P1 > 0 = red card; P2 > 0 = amber |
| 4 | SLA Breaches (MTD) | Institutions where actual uptime < SLA target this month | ≥ 1 = red |
| 5 | Active Alerts | Alert rules currently in firing state | ≥ 5 = amber; ≥ 10 = red |
| 6 | MTTR (30d avg) | Avg time-to-resolve for all incidents in last 30d | > 30 min for P1 = red |

Cards auto-refresh every 30s. Pauses when drawer/modal open.

---

### 5.3 Services Health Grid

**HTMX:** `id="ph-services"` `hx-get="/exec/platform-health/?part=services&range={{ range }}"` `hx-trigger="load, every 30s[!document.querySelector('.drawer-open,.modal-open')]"` `hx-swap="innerHTML"`

**Group by dropdown (top-right of section):**
`[Group by: Service ▾]` — options: Service · Region · SLA Tier
Changes grouping of the table rows.

**Table structure:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Service        │ Status   │ Uptime %  │ P50 Latency │ Error Rate │  ⋯  │
├────────────────┼──────────┼───────────┼─────────────┼────────────┼─────┤
│ ● Exam Engine  │ ✅ OK    │ 99.97%    │ 138 ms      │ 0.02%      │ ⋯  │
│ ● Auth Service │ ✅ OK    │ 99.99%    │ 42 ms       │ 0.00%      │ ⋯  │
│ ● File Storage │ ⚠ Degrad │ 99.82%    │ 312 ms      │ 0.18%      │ ⋯  │
```

**Column details:**

| Column | Type | Detail |
|---|---|---|
| Service | Text + status dot | 8px coloured circle: green/amber/red/grey. Click → Service Detail Drawer |
| Status | Badge | Operational `bg-green-900 text-green-300` · Degraded `bg-amber-900 text-amber-300` · Down `bg-red-900 text-red-300` |
| Uptime % | Text | 5 decimal places. Red if < SLA tier target. Tooltip: "SLA target: 99.9% · Current: 99.82% · Deficit: 0.08%" |
| P50 Latency | Text + inline sparkline | 40px sparkline (last 10 data points, 1 per hour) |
| Error Rate | Text + mini bar | Inline `<div>` bar, red if > 0.5% |
| ⋯ actions | Menu | View Detail · View Incidents · Create Alert · Add to Maintenance |

**Sort:** Default by Status (down → degraded → ok). Sortable by Uptime % and Latency (click header).

**Row hover:** `hover:bg-[#131F38]`

**Row click anywhere (not ⋯):** Opens Service Detail Drawer (§6.1)

**Loading skeleton:** 6 rows of pulse blocks, same height as real rows.

**Empty state:** Not applicable (always has 6 services, even if all "Unknown").

**Error state:** "⚠ Unable to fetch service health. Retrying…" grey row spanning all columns.

---

### 5.4 Latency Chart

**HTMX:** `id="ph-chart"` `hx-get="/exec/platform-health/?part=chart&service=all&range=24h"` `hx-trigger="load"` `hx-swap="innerHTML"`

**Service selector:** `[All Services ▾]` dropdown — shows all 6 services. Change triggers hx-get with new `service=` param.

**Range selector:** `[Last 1h] [Last 6h] [Last 24h ●] [Last 7d]` pills (same style as dashboard).

**Chart.js Line (v4.4.2):**
- `id="latency-chart"`, `width: 100%`, `height: 280px`
- X-axis: time labels (hourly for 24h, 6-hourly for 7d)
- Y-axis: ms, log scale option toggle
- Series: P50 `#22C55E` (2px solid) · P95 `#F59E0B` (2px solid) · P99 `#EF4444` (2px solid)
- SLA threshold line: `#EF4444` 1px dashed (e.g., 2,000ms = SLA breach threshold)
- Fill: P50→P99 band `rgba(99,102,241,0.05)`
- Tooltip: "14:00 IST | P50: 138ms | P95: 312ms | P99: 812ms"
- Legend: top-right, horizontal
- Grid: `color: 'rgba(255,255,255,0.04)'`
- Window._charts registry: destroy before recreate on HTMX swap

**Log scale toggle:** `[Linear ●] [Log]` button pair, top-left of chart.

---

### 5.5 Recent Incidents Table

**HTMX:** `id="ph-incidents"` `hx-get="/exec/platform-health/?part=incidents&range={{ range }}"` `hx-trigger="load, every 60s[!document.querySelector('.drawer-open,.modal-open')]"` `hx-swap="innerHTML"`

**[+ New Incident] button:** Opens Create Incident Modal (§7.1). `bg-[#6366F1] text-white px-3 py-1.5 rounded-lg text-sm`

**Table columns:**

| Column | Detail |
|---|---|
| INC # | "INC-2026-0047" format · link → `/exec/incidents/{id}/` |
| Title | Truncated 50 chars · tooltip for full · click → Incident Detail Drawer |
| Severity | P0–P4 badge · P0: `bg-red-900 text-red-300 animate-pulse` |
| Service | Tag chip |
| Status | Investigating / Identified / Monitoring / Resolved |
| Started | Relative time ("12 min ago") · absolute on hover |
| Duration | HH:MM if resolved; live counter if active (`text-red-400` if P1) |
| ⋯ actions | View · Update · Escalate · Resolve |

**Rows displayed:** Last 10 incidents (sorted by start desc). Pagination not needed here — full list is at `/exec/incidents/`.

**Row highlight:** P0/P1 active rows: `bg-red-950/40 border-l-4 border-red-500`
**Resolved rows:** `opacity-60`

**Sort:** By Started desc (default). No sort controls on this mini-table.

**[View All Incidents →]** text link to `/exec/incidents/`

---

## 6. Drawers

### 6.1 Service Detail Drawer (480 px)

**Open trigger:** Click any row in Services Health Grid OR any service circle anywhere on platform.

**HTMX:** `hx-get="/exec/platform-health/?part=service-drawer&service={{ slug }}"` `hx-target="#drawer-container"` `hx-swap="innerHTML"`

**Drawer structure:**
```
┌──────────────────────────────────────────────────────┐
│ Exam Engine                [✅ Operational]      [✕] │
│ ─────────────────────────────────────────────────── │
│ [Overview ●] [Latency] [Incidents] [Dependencies]   │
│ ─────────────────────────────────────────────────── │
│ (tab content — 380px scrollable body)               │
│ ─────────────────────────────────────────────────── │
│ [View Full Health →]          [Create Incident]     │
└──────────────────────────────────────────────────────┘
```

**Tab bar (within drawer):**
`[Overview ●] [Latency] [Incidents] [Dependencies]`
Click: `hx-get="/exec/platform-health/?part=service-tab&service={{ slug }}&tab=latency"` `hx-target="#service-tab-content"` `hx-swap="innerHTML"`
Active tab: `border-b-2 border-[#6366F1] text-white`. Inactive: `text-[#8892A4]`

**Tab: Overview**

2×2 metric grid (each: large number + 48px sparkline + label):

| Metric | Value example | Alert |
|---|---|---|
| Current P50 Latency | 138 ms | > 500ms = amber text |
| P99 Latency (1h) | 812 ms | > 2,000ms = red text |
| Error Rate (1h) | 0.02% | > 0.5% = amber; > 2% = red |
| Requests / min | 4,200 | Context only |

Uptime panel:
```
[24h ●] [7d] [30d]
99.97% uptime · 1m 18s downtime · SLA: ✅ Within 99.9% target
```
Clicking [7d] / [30d]: `hx-get="/exec/platform-health/?part=service-uptime&service={{ slug }}&range=7d"` `hx-target="#service-uptime-panel"` `hx-swap="innerHTML"`

Last incident:
```
Last incident: INC-2026-0041 · Mar 14, 2026 · 8m 22s · Resolved [View →]
```

**Tab: Latency**
Full-width Chart.js Line (within drawer, ~380px × 200px):
- P50 `#22C55E` · P95 `#F59E0B` · P99 `#EF4444`
- X-axis: last 24h, hourly
- Alert threshold dashed line
- Tooltip: "14:00 | P50: 138ms | P95: 312ms | P99: 812ms"

**Tab: Incidents**
Last 5 incidents for this service:
```
INC-2026-0041  Mar 14  8m 22s  P2  Resolved  [View →]
INC-2026-0038  Mar 10  2m 04s  P3  Resolved  [View →]
```
Each row clickable → navigates to `/exec/incidents/{id}/`
Empty: "No incidents for this service in the last 90 days. ✅"

**Tab: Dependencies**

Two sections:
- "Depends on" (upstream services this one calls): list of service names + status circles
- "Called by" (downstream services that call this): same format

If any upstream degraded → amber box: "Upstream degradation may be the root cause of current issues."

**Drawer footer (sticky):**
```
[View Full Platform Health →]          [Create Incident]
```
[View Full Platform Health →]: text link, `text-[#6366F1]`
[Create Incident]: `bg-[#6366F1] text-white rounded-lg px-3 py-1.5 text-sm` → opens Create Incident Modal

---

### 6.2 Incident Detail Drawer (600 px)

**Open trigger:** Click incident row title in Recent Incidents table.

**HTMX:** `hx-get="/exec/platform-health/?part=incident-drawer&id={{ id }}"` `hx-target="#drawer-container"` `hx-swap="innerHTML"`

Tabs: `[Summary ●] [Timeline] [Impact]` — same structure as dashboard §6.4. No duplication of spec here.

---

## 7. Modals

### 7.1 Create Incident Modal (640 px, centred)

**Trigger:** [+ New Incident] button in incidents section OR [Create Incident] in service drawer footer.

**Backdrop:** `bg-black/60` · Modal: `bg-[#0D1526] rounded-xl border border-[#1E2D4A] shadow-2xl`

**Header:** "Create Incident" 18px bold · [✕] top-right

**Form:**

| Field | Control | Validation |
|---|---|---|
| Title | `<input type="text" maxlength="100">` placeholder "e.g. Exam submission failures — South India" | Required |
| Severity | `<select>` with coloured options: P0 🔴 · P1 🔴 · P2 🟠 · P3 🟡 · P4 ⚪ | Required |
| Affected services | Multi-select chip group: [Exam Engine] [Auth] [Storage] [API Gateway] [Email/SMS] [Proctoring] | ≥ 1 required |
| Description | `<textarea rows="4" maxlength="1000">` | Required |
| Assigned to | Searchable `<select>` — ops team users | Defaults to current user |
| Status | `<select>` Investigating (default) / Identified / Monitoring | Required |
| Notify institutions | Toggle switch. Default: On for P0/P1, Off for P3/P4. Auto-switches when severity changes. | — |

**Field validation:**
- Inline validation on blur (not on-submit): red border `border-red-500` + error message below field 11px
- Submit blocked until all required fields valid: [Create Incident] button `opacity-50 cursor-not-allowed`

**Footer:**
```
[Cancel]                    [Create Incident]
```
Cancel: `bg-transparent border border-[#1E2D4A] text-[#8892A4]`
Create: `bg-[#6366F1] text-white` — shows spinner during POST

POST: `/exec/incidents/` (JSON body) → success: toast "INC-{id} created" + modal closes + incident table reloads

**P0 creation extra step:** After form submit but before final POST — confirmation step: "You are about to create a P0 incident. This will trigger PagerDuty, Slack, and institution notifications. Confirm?" [Back] [Confirm Create P0]

---

## 8. States & Edge Cases

| State | Behaviour |
|---|---|
| P0 active | Full-width red pulsing banner above stats strip. Stats strip P1/P2 card shows "P0 ACTIVE" in blinking red. |
| All services operational | Services grid all green; "✅ All systems operational" summary line |
| Service with no data (< 5 min uptime) | Show "Insufficient data" in Uptime and Latency cells |
| Export during high load | PDF generation queued async; "Export queued — email when ready" toast |
| Range = Last 7d, view = services | Uptime % for 7d period (not last 24h); column header shows "7d Uptime" |
| Single service outage | That service row: red bg, animated border, sorted to top regardless of default sort |
| SLA breach detected live | SLA Breaches KPI card turns red; individual institution SLA breach shown in drawer |
| Dependency cycle in drawer | "Circular dependency detected — data may be incomplete" amber notice |
| 6 services all down (P0) | Emergency mode: page polls every 10s instead of 30s |
| Mobile view | Services table becomes card-list (one card per service); chart shrinks to 180px height |

---

## 9. HTMX Architecture — One URL Per Page

**Page URL:** `/exec/platform-health/`
**All partials from:** `/exec/platform-health/?part={name}`

```python
class PlatformHealthView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "stats":           "exec/partials/ph_stats.html",
                "services":        "exec/partials/ph_services.html",
                "chart":           "exec/partials/ph_chart.html",
                "incidents":       "exec/partials/ph_incidents.html",
                "service-drawer":  "exec/partials/ph_service_drawer.html",
                "service-tab":     "exec/partials/ph_service_tab.html",
                "service-uptime":  "exec/partials/ph_service_uptime.html",
                "incident-drawer": "exec/partials/ph_incident_drawer.html",
            }
            if part == "all":
                return render(request, "exec/partials/ph_all.html", ctx)
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/platform_health_page.html", ctx)
```

| `?part=` | Poll | Trigger |
|---|---|---|
| `stats` | Every 30s (pauses drawer/modal) | Load + range change |
| `services` | Every 30s (pauses drawer/modal) | Load + range change + group-by change |
| `chart` | No | Load + service/range selector change |
| `incidents` | Every 60s (pauses drawer/modal) | Load |
| `service-drawer` | No | Service row click |
| `incident-drawer` | No | Incident row click |

---

## 10. API Endpoints

| Method | URL | Key params | Response |
|---|---|---|---|
| GET | `/exec/platform-health/` | `part`, `range`, `service`, `tab` | HTML |
| POST | `/exec/incidents/` | JSON body | `{id: "INC-..."}` |

---

## 11. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| `?part=stats` | < 300 ms | > 800 ms |
| `?part=services` | < 400 ms | > 1 s |
| `?part=chart` | < 600 ms | > 2 s |
| `?part=incidents` | < 400 ms | > 1 s |
| Service drawer load | < 500 ms | > 1.5 s |
| Chart render (browser) | < 200 ms | > 500 ms |
| Full page initial load | < 1.2 s | > 3 s |
| PDF export | < 30 s | > 60 s = async |

---

## 12. Keyboard Shortcuts

| Key | Action |
|---|---|
| `R` | Refresh all |
| `N` | New incident |
| `E` | Export report |
| `Esc` | Close drawer/modal |
| `↑` / `↓` | Navigate incidents table |
| `Enter` | Open incident detail drawer |
| `1`–`4` | Select service drawer tabs |
| `?` | Shortcut help |

---

## 13. HTMX Template Files

| File | Purpose |
|---|---|
| `exec/platform_health_page.html` | Page shell |
| `exec/partials/ph_stats.html` | Stats KPI strip |
| `exec/partials/ph_services.html` | Services health grid table |
| `exec/partials/ph_chart.html` | Latency line chart |
| `exec/partials/ph_incidents.html` | Recent incidents table |
| `exec/partials/ph_service_drawer.html` | Service Detail Drawer |
| `exec/partials/ph_service_tab.html` | Inner tab content |
| `exec/partials/ph_service_uptime.html` | Uptime panel (range-switchable) |
| `exec/partials/ph_incident_drawer.html` | Incident detail within this page |
| `exec/partials/ph_all.html` | Full refresh wrapper |

---

## 14a. Security Considerations

- Page access: `exec`, `ops`, `superadmin` roles only — no institution-level staff can view
- Service dependency graph: only service names shown (not internal IPs/hostnames)
- Create Incident (P0): extra confirmation step prevents accidental P0 creation; P0 creation is `SecurityAuditLog` event
- Export PDF: rate-limited 5/day per user; logged in `AuditLog`
- HTMX part parameter: validated server-side against allowed dispatch keys — unknown `?part=` returns 400
- All incident data: read from DB, not from Redis (Redis for metrics only) — prevents cache poisoning from affecting incident records

---

## 14b. Database Schema

```python
class ServiceHealthSnapshot(models.Model):
    """30-second metric snapshot per monitored service."""
    service_slug    = models.CharField(max_length=50, db_index=True)  # "exam_engine"
    service_label   = models.CharField(max_length=100)
    status          = models.CharField(max_length=20,
                        choices=[("ok","OK"),("degraded","Degraded"),("down","Down"),("unknown","Unknown")])
    uptime_pct      = models.FloatField()
    p50_latency_ms  = models.IntegerField()
    p95_latency_ms  = models.IntegerField()
    p99_latency_ms  = models.IntegerField()
    error_rate      = models.FloatField()   # percentage: 0.0–100.0
    requests_per_min= models.IntegerField()
    recorded_at     = models.DateTimeField(db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["service_slug","recorded_at"]),
        ]


class ServiceDependency(models.Model):
    """Upstream/downstream service dependency map."""
    service         = models.CharField(max_length=50)
    depends_on      = models.CharField(max_length=50)   # service calls this

    class Meta:
        unique_together = ("service","depends_on")
```

Redis keys used by this page:
- `ph:stats:{range}` TTL 25s — pre-computed KPI strip
- `ph:services:{range}` TTL 25s — services table data
- `ph:chart:{service}:{range}` TTL 60s — latency time series

---

## 14c. Validation Rules

| Action | Validation |
|---|---|
| Create Incident — Title | Required, max 100 chars |
| Create Incident — Severity | Required, must be P0–P4 |
| Create Incident — Affected Services | ≥ 1 service required |
| Create Incident — Description | Required, max 1,000 chars |
| Create Incident — P0 | Extra confirmation step; logged as `SecurityAuditLog` entry |
| Export range | Must be one of: `1h`, `6h`, `24h`, `7d`, `30d`; custom range max 90 days |
| `?part=` param | Must be in dispatch allowlist — unknown values return HTTP 400 |

---

## 14. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §5.2 stats strip |
| `ServiceHealthTable` | §5.3 |
| `ServiceStatusBadge` | §5.3, §6.1 |
| `InlineSparkline` | §5.3 latency column |
| `InlineBar` | §5.3 error rate column |
| `ChartLine` | §5.4, §6.1 Latency tab |
| `IncidentTable` | §5.5 |
| `SeverityBadge` | §5.5 |
| `DrawerPanel` | §6.1, §6.2 |
| `TabBar` | §6.1 drawer tabs |
| `ModalDialog` | §7.1 |
| `AlertBanner` | P0 banner |
| `LoadingSkeleton` | All sections |
