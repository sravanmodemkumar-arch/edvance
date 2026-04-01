# 24 — Hostel Security Dashboard

> **URL:** `/group/hostel/security/dashboard/`
> **File:** `24-hostel-security-dashboard.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Hostel Security Coordinator (primary) · Hostel Director · Boys/Girls Coordinators (view)

---

## 1. Purpose

Full-detail security management page for all hostel campuses. While the Security Coordinator's dashboard (Page 08) shows the daily operational view, this page is the complete security operations centre — all CCTV status, guard rosters, all historical and active security incidents, and branch-level security compliance scores.

Girls hostel security receives separate tracking and stricter alerting — CCTV offline at a girls hostel is treated as a critical failure regardless of time of day.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Security  ›  Security Dashboard
```

### 2.2 Page Header
- **Title:** `Hostel Security Dashboard`
- **Subtitle:** `[N] Campuses · CCTV Online: [N/N] · Guard Shifts Covered: [N]% · Open Alerts: [N]`
- **Right controls:** `+ New Alert` · `Export Security Report` · `Advanced Filters`

---

## 3. KPI Cards

| Card | Metric | Colour Rule |
|---|---|---|
| CCTV Online (Total) | Online cameras / Total | Green = 100% · Red < 100% |
| CCTV Online — Girls Hostels | Online / Total (girls hostels only) | Green = 100% · Red < 100% (highest priority) |
| Guard Coverage Tonight | Shifts staffed / Required | Green = 100% · Red < 100% |
| Open Security Alerts | | Green = 0 · Red > 0 |
| Security Incidents (Month) | Total logged | Blue |
| Branches with Open Alerts | | Red > 0 |

**HTMX:** `hx-trigger="every 5m"` → KPI auto-refresh.

---

## 4. CCTV Status Table

> Per-campus CCTV coverage with camera-level detail on click.

**Columns:** Branch | Hostel | Total Cameras | Online | Offline | Blind Spots | Last Check | Status | Actions

**Actions:** View Camera List · Report Offline · Escalate (girls hostel only)

---

## 5. Guard Roster Table

> Shift coverage for all hostel campuses.

**Columns:** Branch | Hostel | Shift | Guards Required | Assigned | Names | Contact (click to reveal) | Status | Actions

**Shift types:** Morning / Afternoon / Night (mandatory for all hostels).

---

## 6. Security Incident Table

> All security incidents — active and historical.

**Search:** Incident #, branch, type. 300ms debounce.

**Filters:** Branch · Hostel Type (Boys/Girls) · Severity · Status · Date range · Incident Type.

**Columns:**
| Column | Sortable |
|---|---|
| Incident # | ✅ |
| Severity | ✅ |
| Branch | ✅ |
| Hostel Type | ✅ |
| Incident Type | ✅ |
| Occurred At | ✅ |
| Age / Days Open | ✅ |
| Status | ✅ |
| Actions | ❌ |

**Pagination:** Server-side · 25/page.

---

## 7. Night Roll Call Status

> Tonight's roll call completion status — updated in near real-time.

**Display:** Table — Branch | Boys Roll Call | Girls Roll Call | Submitted At | Discrepancy | Warden Action

Status: ✅ Submitted (All Clear) / ⚠ Submitted (Discrepancy: [N]) / ❌ Not Submitted.

**HTMX:** `hx-trigger="every 10m"` → roll call status auto-refresh.

---

## 8. Security Trend Chart

- Stacked bar: Incident types per month (6 months)
- Line: Guard coverage % per month
- Filter: Boys vs Girls.

---

## 9. Drawers

### 9.1 Drawer: `security-alert-create` (see Page 08 Section 6.2)
### 9.2 Drawer: `security-alert-detail`
- **Width:** 640px
- **Tabs:** Overview · Timeline · Evidence · Actions · Resolution

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Alert created | "Security alert #[ID] logged." | Success | 4s |
| Alert resolved | "Security alert #[ID] resolved." | Success | 4s |
| CCTV offline reported | "CCTV offline at [Branch] reported. IT Admin notified." | Warning | 5s |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/security/` | JWT (G3+) | Full security dashboard |
| GET | `/api/v1/group/{group_id}/hostel/security/kpis/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/security/cctv/` | JWT (G3+) | CCTV status all campuses |
| GET | `/api/v1/group/{group_id}/hostel/security/guard-roster/` | JWT (G3+) | Guard roster |
| GET | `/api/v1/group/{group_id}/hostel/security/alerts/` | JWT (G3+) | All incidents (paginated) |
| POST | `/api/v1/group/{group_id}/hostel/security/alerts/` | JWT (G3+) | Create alert |
| PATCH | `/api/v1/group/{group_id}/hostel/security/alerts/{id}/` | JWT (G3+) | Update |
| GET | `/api/v1/group/{group_id}/hostel/security/roll-call/tonight/` | JWT (G3+) | Roll call status |
| GET | `/api/v1/group/{group_id}/hostel/security/trends/` | JWT (G3+) | 6-month trend |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
