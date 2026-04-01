# 23 — Notification Delivery Monitor

- **URL:** `/group/it/notifications/delivery/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4)

---

## 1. Purpose

The Notification Delivery Monitor is the cross-channel delivery audit log for all notifications sent from EduForge across the group. Every OTP, fee reminder, attendance alert, exam notification, and admission confirmation sent via WhatsApp, SMS, Email, or In-App channel is recorded here. This page allows the IT Admin to diagnose delivery failures, audit notification volumes, identify consistently unreachable recipients, and verify that critical notifications (OTPs, POCSO alerts, fee overdue reminders) were actually delivered.

This is a read-and-investigate page — no new notifications are sent from here. When a branch reports "students didn't receive the exam notification", the IT Admin uses this page to find the exact send event, check delivery status, view the error code if delivery failed, and identify whether the failure was at the provider level, the template level, or the recipient's device.

The monitor covers the last 90 days of notifications by default. Older records are archived to Cloudflare R2 and remain available via export.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full — view all delivery logs, export, investigate failures | Primary owner |
| Group IT Director | G4 | Read-only view | Oversight and auditing |
| Group EduForge Integration Manager | G4 | Read — integration-related notifications only | Useful for debugging webhook vs. notification issues |
| Group Cybersecurity Officer (Role 56, G1) | G1 | No access | Not applicable |
| Group Data Privacy Officer (Role 55, G1) | G1 | No access | PII in delivery logs is IT Admin scope only |
| Group IT Support Executive (Role 57, G3) | G3 | Read — for ticket investigation only | Can view delivery status for a specific user when resolving a support ticket |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal › IT & Technology › Notifications › Delivery Monitor`

### 3.2 Page Header
- **Title:** Notification Delivery Monitor
- **Subtitle:** Cross-channel delivery audit — last 90 days
- **Actions (top-right):**
  - `Export Delivery Report` (secondary button — CSV/XLSX)
  - `Refresh` (icon button — reloads table without full page reload via HTMX)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| WhatsApp delivery failure rate >10% in last hour | "WhatsApp delivery degraded — [N]% failure rate in the last hour. Check provider status." | Red — dismissible after investigation |
| OTP delivery failure rate >5% | "OTP delivery failures detected. Users may be unable to log in. Check Auth notification logs immediately." | Red — non-dismissible |
| SMS DLT template rejection causing delivery failures | "SMS delivery blocked — DLT template not registered. Update template registration." | Red — non-dismissible |
| Email bounce rate >5% in last 24h | "High email bounce rate ([N]%). Review sender domain and suppression list." | Amber — dismissible |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Sent (24h) | Count of all notification events in last 24 hours | Blue (informational) | Filters table to last 24h |
| Delivered (24h) | Count of confirmed delivered in last 24h | Green if ≥ 95%, Amber 85–94%, Red < 85% | Filters to Delivered status |
| Failed (24h) | Count of failed delivery events in last 24h | Red if > 0, Green if 0 | Filters to Failed status |
| OTP Success Rate | % of OTP notifications delivered in last 24h | Green ≥ 99%, Amber 95–98%, Red < 95% | Filters to OTP category |
| Channel Breakdown | Mini-icons: WhatsApp / SMS / Email / In-App counts | — | Click channel icon to filter |

---

## 5. Main Table — Delivery Log

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Notification ID | Monospace text | No | No |
| Sent At | DateTime | Yes | Yes — date range picker |
| Channel | Badge (WhatsApp/SMS/Email/In-App) | Yes | Yes — multi-select |
| Category | Badge (OTP/Fee/Exam/Attendance/Admission/POCSO/General) | Yes | Yes — multi-select |
| Branch | Text | Yes | Yes — multi-select dropdown |
| Recipient Type | Badge (Student/Parent/Staff) | No | Yes — multi-select |
| Recipient (masked) | Last 4 digits of phone / first char of email | No | No — masked for privacy |
| Template Name | Text | No | Yes — dropdown |
| Status | Badge (Delivered/Failed/Pending/Bounced/Read) | Yes | Yes — multi-select |
| Provider Response | Short code (e.g., `DELIVERED`, `INVALID_NUMBER`, `OPTED_OUT`) | No | No |
| Actions | Icon button | No | No |

### 5.1 Filters

| Filter | Type |
|---|---|
| Date Range | Date picker (max 90-day range) |
| Channel | Multi-select: WhatsApp / SMS / Email / In-App |
| Category | Multi-select: OTP / Fee / Exam / Attendance / Admission / POCSO / General / System |
| Branch | Multi-select dropdown |
| Status | Multi-select: Delivered / Failed / Pending / Bounced / Read |
| Recipient Type | Multi-select: Student / Parent / Staff |
| Template | Dropdown |

Active filter chips: Yes — dismissible. "Clear All" link. Count badge on filter button.

### 5.2 Search
- Free-text search on: Notification ID (exact), Template Name
- Debounced `hx-get` on keyup (400ms)

### 5.3 Pagination
- Server-side · Default 50 rows/page · Selector: 25 / 50 / 100
- "Showing X–Y of Z records"

---

## 6. Drawers

### 6.1 Drawer: `delivery-detail` — Notification Event Detail
- **Trigger:** Click on any row (eye icon or row click)
- **Width:** 560px
- **Content:**
  - Notification metadata: ID, sent at (exact ms timestamp), channel, category, branch
  - Recipient info: masked phone/email, recipient type
  - Template: name, channel, full rendered body (with variables substituted showing actual sent text)
  - Provider info: provider name, message ID from provider, provider response code, raw provider response body
  - Delivery timeline: Queued → Sent to Provider → Delivered / Failed — with timestamp at each stage
  - If Failed: error code explanation (human-readable), suggested fix
  - If Bounced (email): bounce type (hard/soft), bounce reason
  - Retry history: how many times retried, timestamps
- **Actions (IT Admin only):** `Retry Send` (re-queues the notification — only for Failed status) · `Flag for Investigation` (adds a manual flag tag)

### 6.2 Drawer: `channel-failure-analysis` — Failure Analysis for a Channel
- **Trigger:** Click on a failed-count KPI card or via "Analyse Failures" button in alert banner
- **Width:** 600px
- **Tabs:** Last Hour · Last 24h · Last 7d
- **Content per tab:** Failure count + rate, top error codes (bar chart of error codes by frequency), affected branches, top failed templates, timeline of failure events
- **Action:** Export failure analysis as CSV

---

## 7. Charts

### 7.1 Delivery Success Rate by Channel (Line Chart — Last 7 Days)
- **X-axis:** Day labels (last 7 days)
- **Y-axis:** Success rate %
- **Series:** WhatsApp (blue), SMS (orange), Email (green), In-App (purple)
- **Tooltip:** Date · Channel · Sent count · Delivered count · Success %
- **Export:** PNG button top-right of chart card

### 7.2 Notification Volume by Category (Stacked Bar — Last 7 Days)
- **X-axis:** Day labels
- **Y-axis:** Notification count
- **Stacks:** OTP (blue), Fee (green), Exam (orange), Attendance (teal), General (grey)
- **Tooltip:** Date · Category · Count

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export started | "Delivery report export started. Download will begin shortly." | Info | 4s |
| Retry queued | "Notification re-queued for delivery. Check back in 60 seconds." | Success | 4s |
| Flag saved | "Notification flagged for investigation." | Info | 4s |
| Table refreshed | "Delivery log refreshed." | Info | 3s |
| Export error | "Export failed. Please try again." | Error | 6s |
| Export failed | Error: `Failed to export delivery data. Please try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No notifications in selected date range | "No notifications found" | "No delivery events match the current filters. Try broadening the date range or clearing filters." | [Clear Filters] |
| No failures in selected range | "No failures detected" | "All notifications in the selected period were delivered successfully." | — |
| Delivery log unavailable | "Log data unavailable" | "Delivery log data could not be loaded. Please try refreshing." | [Refresh] |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Skeleton: KPI bar shimmer (5 cards) + table skeleton (10 rows) |
| Filter / search / page change | Inline table skeleton (10 rows) — keeps column widths |
| Delivery detail drawer open | Spinner centred in drawer body |
| Chart data fetch | Chart area shimmer with "Loading chart…" label |
| Retry send button click | Spinner inside button + button disabled |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Integration Manager (G4) | IT Support Exec (G3) |
|---|---|---|---|---|
| Full delivery log table | ✅ All records | ✅ All records (read-only) | ✅ Integration notifications only | ✅ Per-ticket lookup only |
| Recipient (masked) | ✅ Masked always | ✅ Masked always | ✅ Masked always | ✅ Masked always |
| Drawer — Retry Send action | ✅ Shown | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| Drawer — Flag for Investigation | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden |
| Export Delivery Report | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden |
| Channel Failure Analysis drawer | ✅ Shown | ✅ Shown | ✅ Integration channels only | ❌ Hidden |
| Alert banners | ✅ Non-dismissible (G4 must act) | ✅ Read + dismiss | ❌ Not shown | ❌ Not shown |

> All UI visibility decisions enforced server-side in Django template. No client-side JS role checks.

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/notifications/delivery/` | JWT (G4) | Paginated delivery log — supports all filter and search params |
| GET | `/api/v1/it/notifications/delivery/kpis/` | JWT (G4) | KPI bar values (24h counts by status and channel) |
| GET | `/api/v1/it/notifications/delivery/{id}/` | JWT (G4) | Full event detail for drawer |
| POST | `/api/v1/it/notifications/delivery/{id}/retry/` | JWT (G4 IT Admin) | Re-queue a failed notification |
| POST | `/api/v1/it/notifications/delivery/{id}/flag/` | JWT (G4) | Flag event for investigation |
| GET | `/api/v1/it/notifications/delivery/charts/success-rate/` | JWT (G4) | 7-day success rate per channel (line chart data) |
| GET | `/api/v1/it/notifications/delivery/charts/volume/` | JWT (G4) | 7-day volume by category (stacked bar data) |
| GET | `/api/v1/it/notifications/delivery/failure-analysis/` | JWT (G4) | Failure analysis for channel — accepts `channel` and `period` params |
| GET | `/api/v1/it/notifications/delivery/export/` | JWT (G4) | Export delivery log as CSV/XLSX (async, returns download URL) |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Page load — KPI bar | `load` | GET `/api/v1/it/notifications/delivery/kpis/` | `#kpi-bar` | `innerHTML` |
| Page load — delivery table | `load` | GET `/api/v1/it/notifications/delivery/` | `#delivery-table` | `innerHTML` |
| Search input | `keyup changed delay:400ms` | GET `/api/v1/it/notifications/delivery/?q={val}` | `#delivery-table` | `innerHTML` |
| Filter change | `change` | GET `/api/v1/it/notifications/delivery/?{params}` | `#delivery-table` | `innerHTML` |
| Pagination click | `click` | GET `/api/v1/it/notifications/delivery/?page={n}` | `#delivery-table` | `innerHTML` |
| Sort column click | `click` | GET `/api/v1/it/notifications/delivery/?sort={col}&dir={dir}` | `#delivery-table` | `innerHTML` |
| Open delivery detail drawer | `click` on row | GET `/api/v1/it/notifications/delivery/{id}/` | `#drawer-container` | `innerHTML` |
| Retry send button | `click` | POST `/api/v1/it/notifications/delivery/{id}/retry/` | `#retry-result` | `innerHTML` |
| Manual refresh button | `click` | GET `/api/v1/it/notifications/delivery/` | `#delivery-table` | `innerHTML` |
| Load success-rate chart | `load` | GET `/api/v1/it/notifications/delivery/charts/success-rate/` | `#chart-success-rate` | `innerHTML` |
| Load volume chart | `load` | GET `/api/v1/it/notifications/delivery/charts/volume/` | `#chart-volume` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- OTP delivery failure rate > 10%: IT Admin + IT Director (in-app red non-dismissible + email) immediately
- Channel delivery failure rate > 20%: IT Admin (in-app amber + email)
- Notification volume spike > 200% normal: IT Admin (in-app amber)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
