# 04 — Hostel Welfare Officer Dashboard

> **URL:** `/group/hostel/welfare/`
> **File:** `04-hostel-welfare-officer-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Hostel Welfare Officer (Role 70, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Hostel Welfare Officer. Dedicated to daily welfare monitoring of all hostelers across all branches — both boys and girls. The Welfare Officer tracks every welfare event from its initial logging by a warden through escalation to the Hostel Director or POCSO Coordinator. The core operational cadence is daily: every morning the Officer reviews overnight incidents, every evening they clear the day's queue.

**Welfare severity classification:**
- **Severity 1 (Critical):** Physical harm, medical emergency, POCSO concern, missing student — SLA: escalate within 2 hours
- **Severity 2 (High):** Bullying, mental health crisis, family emergency — SLA: resolve or escalate within 8 hours
- **Severity 3 (Medium):** Conflict between hostelers, homesickness requiring counselling — SLA: resolve within 48 hours
- **Severity 4 (Low):** Routine welfare check, minor complaint, food preference issues — SLA: log and close within 7 days

The dashboard shows all severity levels, with Severity 1 and 2 always on top as the primary action queue.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Hostel Welfare Officer | G3 | Full — all genders, all branches | Exclusive dashboard |
| Group Hostel Director | G3 | View (via own dashboard) | Can see welfare summary |
| Group Boys Hostel Coordinator | G3 | View — boys incidents only | Via branch detail |
| Group Girls Hostel Coordinator | G3 | View — girls incidents only | Via branch detail |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Welfare Officer Dashboard
```

### 3.2 Page Header
```
Welcome back, [Officer Name]                   [Export Welfare Report ↓]  [Settings ⚙]
Group Hostel Welfare Officer · Today: [date]
Open Incidents: [N]  ·  Severity 1: [N]  ·  Severity 2: [N]  ·  SLA Breaches: [N]
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Any Severity 1 incident open > 2h | "SLA BREACH: [N] Severity 1 incident(s) unresolved > 2 hours." | Red |
| Any Severity 2 incident open > 8h | "[N] Severity 2 incidents approaching SLA breach (8h limit)." | Amber |
| Welfare log not submitted from any branch today | "[Branch] has not submitted today's welfare log. Follow up immediately." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Incidents Total | All active welfare incidents | Green = 0 · Yellow 1–10 · Red > 10 | → Page 22 |
| Severity 1 Open | Critical incidents unresolved | Green = 0 · Red > 0 always | → Page 22 (Sev 1 filter) |
| Severity 2 Open | High priority incidents | Green = 0 · Yellow 1–3 · Red > 3 | → Page 22 (Sev 2 filter) |
| SLA Breaches Today | Incidents that missed their SLA | Green = 0 · Red > 0 always | → Page 22 (SLA filter) |
| Incidents Closed This Week | Resolved in last 7 days | Blue always | → Page 22 (closed filter) |
| Branches Pending Welfare Log | Branches that haven't submitted today's log | Green = 0 · Red > 0 | — |

**HTMX:** `hx-trigger="every 3m"` → KPI auto-refresh (welfare changes rapidly throughout the day)

---

## 5. Sections

### 5.1 Priority Action Queue — Severity 1 & 2

> Every Severity 1 and 2 incident requires personal intervention today.

**Display:** Vertical card list. Max visible: 10. "View all →" → Page 22.

**Card fields:**
- Severity badge (1 = Red, 2 = Orange)
- Incident type (Welfare / Medical / Bullying / Missing / POCSO / Mental Health)
- Hosteler name + gender icon (M/F) + branch
- Time elapsed (bold red if SLA breached)
- Last action logged + actor
- [Update Status →] [Escalate to Director →] [Log Action →]

**Status update drawer:** Inline status dropdown (In Progress / Escalated / Resolved) + note textarea + submit.

---

### 5.2 All Incidents Table

> Full welfare incident table with all severities.

**Search:** Hosteler name, branch, incident type, warden name. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Severity | Checkbox | 1 / 2 / 3 / 4 |
| Status | Checkbox | Open / In Progress / Escalated / Resolved / Closed |
| Gender | Radio | All / Boys / Girls |
| Branch | Multi-select | All branches |
| Date Range | Date picker | Opened between |
| SLA | Checkbox | SLA Breached |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Incident # | ✅ | Auto-generated ID |
| Severity | ✅ | Colour badge |
| Hosteler Name | ✅ | Link → incident detail drawer |
| Gender | ✅ | M/F icon |
| Branch | ✅ | |
| Type | ✅ | Category |
| Opened At | ✅ | Date + time |
| Age | ✅ | Time elapsed (red if SLA breached) |
| Status | ✅ | Badge |
| Assigned To | ✅ | Staff name |
| SLA | ✅ | ✅ Within SLA / ⚠ At Risk / ❌ Breached |
| Actions | ❌ | View · Update · Escalate |

**Bulk actions:** Bulk close Severity 4 (resolved) with note.

**Pagination:** Server-side · 25/page.

---

### 5.3 Daily Welfare Log Submission Status

> Which branches have submitted today's welfare log (required for all hostel branches daily).

**Display:** Table — Branch | Submitted? | Submitted by | Time | Incidents Logged | [View →]

Red highlight on rows where log not submitted and it is past 9 AM.

---

### 5.4 Welfare Trend Chart

**Chart 1 — Incidents by Severity (Last 30 days)**
- Stacked area chart: Severity 1 (red) · 2 (orange) · 3 (yellow) · 4 (blue)
- X: Last 30 days. Y: Count per day.

**Chart 2 — Resolution Time Distribution (Last 30 days)**
- Bar chart: < 2h / 2–8h / 8–24h / 24–48h / > 48h
- Grouped by severity.

---

## 6. Drawers

### 6.1 Drawer: `welfare-incident-detail`
- **Trigger:** Incident table → row or incident #
- **Width:** 640px
- **Tabs:** Overview · Timeline · Actions · Escalation · Resolution
- **Overview:** Hosteler details, incident type, severity, branch, warden who raised it
- **Timeline:** All status changes + actor + timestamp (chronological, immutable)
- **Actions:** Add note, update status, assign to staff, request hostel director review
- **Escalation:** Escalation chain history; button to escalate to next level
- **Resolution:** Resolution note, closed by, closure timestamp, follow-up required flag

### 6.2 Drawer: `welfare-incident-create`
- **Trigger:** + New Incident button
- **Width:** 600px
- **Fields:** Branch · Hostel Type (Boys/Girls) · Hosteler (search autocomplete) · Incident Type · Severity · Description (textarea, min 50 chars) · Immediate Action Taken · Follow-up Required (checkbox) · Notify Warden (checkbox, default checked) · Notify Hostel Director (checkbox, auto-checked if Sev 1/2)
- **On submit:** POST `.../incidents/`; incident created; **drawer remains open** displaying the success toast (enables rapid multi-incident creation — coordinator can log multiple incidents without reopening the drawer each time); Priority Action Queue (`#priority-queue`) and incident table (`#incident-table-section`) refresh via HTMX in background; audit log entry created; WhatsApp notification sent to assigned parties.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Incident created | "Welfare incident #[ID] logged for [Hosteler Name]." | Success | 4s |
| Status updated | "Incident #[ID] status updated to [Status]." | Success | 4s |
| Escalated to Director | "Incident #[ID] escalated to Hostel Director." | Warning | 6s |
| Incident closed | "Incident #[ID] closed. Resolution logged." | Success | 4s |
| SLA breach alert | "SLA BREACH: Incident #[ID] has exceeded the [N]-hour limit." | Error | Manual dismiss |
| Welfare log submitted | "Welfare log for [Branch] submitted successfully." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open incidents | "All Clear — No Open Welfare Incidents" | "All hostelers are currently accounted for and safe." | — |
| No results for filters | "No Incidents Match Filters" | "Adjust severity, branch, or date range filters." | [Clear Filters] |
| All logs submitted | "All Branch Welfare Logs Submitted Today" | — | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + priority queue (3 cards) + incident table (10 rows) + chart placeholders |
| Table filter/search | Inline skeleton rows |
| KPI auto-refresh (every 3m) | Shimmer over cards only |
| Incident create drawer submit | Spinner on Submit; drawer stays open with result |
| Status update | Button spinner; row refreshes in-place |

---

## 10. Role-Based UI Visibility

| Element | Welfare Officer G3 | Boys Coordinator G3 | Girls Coordinator G3 | Hostel Director G3 |
|---|---|---|---|---|
| Create Incident | ✅ All | ✅ Boys only | ✅ Girls only | ✅ All |
| Escalate to Director | ✅ | ✅ | ✅ | — |
| Close Severity 1 | ✅ (with note) | ❌ | ❌ | ✅ |
| Bulk close Severity 4 | ✅ | ❌ | ❌ | ✅ |
| Export welfare report | ✅ | ✅ | ✅ | ✅ |
| Gender filter — both | ✅ | ❌ Boys only | ❌ Girls only | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/welfare/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/welfare/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/welfare/incidents/` | JWT (G3+) | All incidents (paginated, filtered) |
| GET | `/api/v1/group/{group_id}/hostel/welfare/incidents/{id}/` | JWT (G3+) | Incident detail |
| POST | `/api/v1/group/{group_id}/hostel/welfare/incidents/` | JWT (G3+) | Create new incident |
| PATCH | `/api/v1/group/{group_id}/hostel/welfare/incidents/{id}/` | JWT (G3+) | Update status / note |
| POST | `/api/v1/group/{group_id}/hostel/welfare/incidents/{id}/escalate/` | JWT (G3+) | Escalate incident |
| POST | `/api/v1/group/{group_id}/hostel/welfare/incidents/{id}/close/` | JWT (G3+) | Close with resolution |
| GET | `/api/v1/group/{group_id}/hostel/welfare/daily-log-status/` | JWT (G3+) | Branch log submission status |
| GET | `/api/v1/group/{group_id}/hostel/welfare/trends/` | JWT (G3+) | 30-day trend data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 3m` | GET `.../welfare/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Priority queue refresh | `every 3m` | GET `.../welfare/incidents/?severity=1,2&status=open` | `#priority-queue` | `innerHTML` |
| Incident search | `input delay:300ms` | GET `.../incidents/?q={val}` | `#incident-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../incidents/?{filters}` | `#incident-table-section` | `innerHTML` |
| Open incident detail | `click` on row | GET `.../incidents/{id}/` | `#drawer-body` | `innerHTML` |
| Status update | `click` on Update | PATCH `.../incidents/{id}/` | `#incident-row-{id}` | `outerHTML` |
| Create incident submit | `click` on Submit | POST `.../incidents/` | `#incident-table-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
