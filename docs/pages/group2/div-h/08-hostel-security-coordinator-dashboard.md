# 08 — Hostel Security Coordinator Dashboard

> **URL:** `/group/hostel/security/`
> **File:** `08-hostel-security-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Hostel Security Coordinator (Role 74, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Hostel Security Coordinator. Manages night security operations, CCTV policy and coverage status, security guard rosters, visitor entry protocols, and incident reporting across all hostel campuses. Hosteler safety is a 24/7 responsibility: boys and girls hostels each require separate security protocols, with girls hostels carrying stricter visitor restrictions and mandatory female security staff for night duty.

Key operational cadence:
- **Daily:** Verify CCTV operational status at all campuses; review overnight security incident reports
- **Weekly:** Review guard roster submissions from all branches; verify shift coverage
- **Monthly:** Audit visitor register compliance; security incident trend report to Hostel Director

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Hostel Security Coordinator | G3 | Full — all branches, both genders | Exclusive dashboard |
| Group Boys Hostel Coordinator | G3 | View — boys hostel security | Via own dashboard |
| Group Girls Hostel Coordinator | G3 | View — girls hostel security | Via own dashboard |
| Group Hostel Director | G3 | View — security summary | Via own dashboard |
| Group Hostel Welfare Officer | G3 | View — incidents with welfare link | Read-only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Security Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]             [+ New Security Alert]  [Export Report ↓]  [Settings ⚙]
Group Hostel Security Coordinator · [date time]
CCTV: [N/N] Online  ·  Security Alerts (Open): [N]  ·  Guard Shifts Covered: [N]%
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| CCTV offline at any hostel (especially girls) | "CCTV OFFLINE: [Branch] [Girls/Boys] Hostel — [N] cameras offline. Immediate escalation required." | Red |
| Security incident Severity 1 in last 24h | "Security incident at [Branch] — [description summary]. Review immediately." | Red |
| Guard shift uncovered (night shift) | "Night shift guard ABSENT at [Branch] hostel — no replacement assigned." | Red |
| Visitor log not submitted for > 24h at any branch | "[Branch] visitor register not updated for > 24 hours." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| CCTV Online Rate | Cameras online / Total cameras across all hostels | Green = 100% · Yellow < 100% · Red any offline | → Page 24 |
| Open Security Alerts | Unresolved security incidents | Green = 0 · Yellow 1–3 · Red > 3 | → Page 24 |
| Guard Coverage (Tonight) | Shifts covered / Total required shifts | Green = 100% · Yellow < 100% · Red < 90% | → Page 24 |
| Visitor Entries (Today) | Total visitor entries logged | Blue always | → Page 25 |
| Unauthorized Entries (24h) | Visitors without proper clearance | Green = 0 · Red > 0 | → Page 25 |
| Branches with Security Issues | Branches with open Severity 1 alerts | Green = 0 · Red > 0 | → Page 24 |

**HTMX:** `hx-trigger="every 5m"` → KPI auto-refresh (security is real-time).

---

## 5. Sections

### 5.1 CCTV Status Dashboard

> Real-time CCTV coverage across all hostel campuses.

**Display:** Table — Branch | Hostel Type | Total Cameras | Online | Offline | Blind Spots Reported | Last Checked | Status | [View →]

Status badge: ✅ Fully Operational / ⚠ Partial Coverage / ❌ Critical — Offline.

**Red row** for girls hostel with any camera offline (higher safety risk).

---

### 5.2 Security Alert Queue

> All open security incidents requiring coordinator action.

**Display:** Card list. Severity 1 at top always.

**Card fields:**
- Severity (1 = Red, 2 = Orange, 3 = Yellow)
- Incident type (Intruder / Unauthorized Access / Theft / Physical Altercation / Missing Student / Suspicious Activity / CCTV Tampered / Guard Dereliction)
- Branch + Hostel type (Boys/Girls)
- Time elapsed
- Last action + actor
- [Update →] [Escalate to Director →] [Close →]

"View All →" → Page 24.

---

### 5.3 Guard Roster Overview

> Tonight's guard shift coverage across all hostel campuses.

**Columns:** Branch | Hostel Type | Shift | Guards Required | Assigned | Status | Contact | [Actions]

Status: ✅ Fully Staffed / ⚠ Short-staffed / ❌ No guard assigned.

Shift types: Morning (6AM–2PM) / Afternoon (2PM–10PM) / Night (10PM–6AM). Night shift is mandatory for all hostel campuses.

---

### 5.4 Today's Visitor Summary

> Quick statistics on visitor entries today.

**Summary cards:** Total Entries · Boys Hostel Entries · Girls Hostel Entries · Unauthorized (without ID) · Pending Clearance.

[View Full Register →] → Page 25.

---

### 5.5 Security Trend Chart

**Chart — Security Incidents by Type (Last 6 months)**
- Stacked bar: Unauthorized Entry / Theft / Altercation / Suspicious Activity / CCTV Issues / Other
- X: Month. Y: Count.
- Filter: Boys vs Girls vs Both.

---

## 6. Drawers

### 6.1 Drawer: `security-branch-detail`
- **Width:** 640px
- **Tabs:** CCTV · Guard Roster · Incidents · Visitor Log · Audit
- **CCTV tab:** Camera list with location (Gate / Corridor / Common Room / Perimeter) and online status
- **Guard Roster tab:** All shifts + assigned guard names + contact numbers
- **Incidents tab:** Open + last 30 days closed incidents for this branch
- **Visitor Log tab:** Last 20 visitor entries
- **Audit tab:** Security-related audit actions (CCTV changes, guard assignments)

### 6.2 Drawer: `security-alert-create`
- **Trigger:** + New Security Alert
- **Width:** 560px
- **Fields:** Branch · Hostel Type (Boys/Girls) · Incident Type · Severity · Location (Gate/Corridor/Room/Perimeter/Outside campus) · Date/Time of Incident · Description (min 50 chars) · Immediate Action Taken · Evidence attached (photo upload) · Escalate to Hostel Director (checkbox, mandatory for Sev 1)

### 6.3 Modal: Report CCTV Offline
- **Trigger:** CCTV table → any offline entry
- **Type:** Centred modal (480px)
- **Content:** Branch + camera count offline + last known operational time
- **Actions:** Notify Branch IT Admin checkbox + Escalate to Girls/Boys Coordinator (if girls hostel) + Submit report
- **On confirm:** Alert logged; notifications sent; audit entry

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Security alert created | "Security alert #[ID] logged at [Branch]." | Success | 4s |
| Alert escalated | "Alert escalated to Hostel Director. Notified via WhatsApp." | Warning | 6s |
| Alert closed | "Security alert #[ID] closed. Resolution logged." | Success | 4s |
| CCTV report submitted | "CCTV offline report submitted for [Branch]. IT Admin notified." | Warning | 5s |
| Guard contact logged | "Contact with [Guard/Supervisor Name] logged." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open security alerts | "All Hostels Secure — No Open Alerts" | — | — |
| All CCTV online | "All CCTV Systems Fully Operational" | — | — |
| No visitor entries today | "No Visitor Entries Logged Today" | "No visitors have been recorded at any hostel campus today." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + CCTV table + alert queue + guard roster + visitor summary |
| CCTV table auto-refresh (5m) | Shimmer on CCTV table rows only |
| Alert card status update | Spinner on button; card refreshes in-place |
| Branch detail drawer | Centred spinner; tabs load lazily |

---

## 10. Role-Based UI Visibility

| Element | Security Coordinator G3 | Boys Coordinator G3 | Girls Coordinator G3 | Hostel Director G3 |
|---|---|---|---|---|
| Boys hostel data (CCTV, alerts, roster) | ✅ All | ✅ Boys only | ❌ Hidden | ✅ All |
| Girls hostel data (CCTV, alerts, roster) | ✅ All | ❌ Hidden | ✅ Girls only | ✅ All |
| Create Security Alert | ✅ All hostels | ✅ Boys hostels | ✅ Girls hostels | ✅ All |
| Escalate to Director | ✅ | ✅ | ✅ | — |
| Report CCTV Offline | ✅ | ✅ Boys | ✅ Girls | ✅ |
| Guard roster view | ✅ All | ✅ Boys | ✅ Girls | ✅ All |
| Visitor log — girls detail | ✅ | ❌ | ✅ | ✅ |
| POCSO Alert button (girls hostel incidents) | ✅ | ❌ | ✅ | ✅ |

> **Data isolation enforcement:** All Boys/Girls data separation is enforced server-side via Django queryset filters (`gender = M` / `gender = F` on hostel records). No client-side role check.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/security/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/security/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/security/cctv-status/` | JWT (G3+) | CCTV per-branch status |
| GET | `/api/v1/group/{group_id}/hostel/security/alerts/` | JWT (G3+) | All open alerts |
| POST | `/api/v1/group/{group_id}/hostel/security/alerts/` | JWT (G3+) | Create new alert |
| PATCH | `/api/v1/group/{group_id}/hostel/security/alerts/{id}/` | JWT (G3+) | Update alert |
| POST | `/api/v1/group/{group_id}/hostel/security/alerts/{id}/escalate/` | JWT (G3+) | Escalate alert |
| GET | `/api/v1/group/{group_id}/hostel/security/guard-roster/` | JWT (G3+) | Guard shift roster |
| GET | `/api/v1/group/{group_id}/hostel/security/visitors/today/` | JWT (G3+) | Today's visitor summary |
| GET | `/api/v1/group/{group_id}/hostel/security/branches/{id}/detail/` | JWT (G3+) | Branch security detail |
| GET | `/api/v1/group/{group_id}/hostel/security/trends/` | JWT (G3+) | 6-month incident trend |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../security/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| CCTV table refresh | `every 5m` | GET `.../cctv-status/` | `#cctv-table` | `innerHTML` |
| Alert queue refresh | `every 5m` | GET `.../alerts/?status=open` | `#alert-queue` | `innerHTML` |
| Create alert submit | `click` | POST `.../security/alerts/` | `#alert-queue` | `afterbegin` |
| Escalate alert | `click` | POST `.../alerts/{id}/escalate/` | `#alert-card-{id}` | `outerHTML` |
| Open branch detail | `click` | GET `.../security/branches/{id}/detail/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
