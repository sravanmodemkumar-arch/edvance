# 22 — Welfare Incident Tracker

> **URL:** `/group/hostel/welfare/incidents/`
> **File:** `22-welfare-incident-tracker.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Hostel Welfare Officer (primary) · Hostel Director · Boys/Girls Coordinators · Discipline Committee (view)

---

## 1. Purpose

The authoritative log of all welfare incidents across all hostel campuses — both historical and active. This page is the full-detail companion to the Welfare Officer Dashboard (Page 04): the dashboard shows today's queue; this page is the complete searchable archive with advanced filtering, trend analytics, and SLA compliance tracking.

Every welfare event — from a minor food complaint (Severity 4) to a child safety concern requiring POCSO escalation (Severity 1) — is created, tracked, and closed here. All entries are immutable once closed; status changes and notes create timeline entries that cannot be deleted.

**Severity SLAs:**
- S1 (Critical): Escalation within 2h · Resolution/handover within 24h
- S2 (High): Action within 8h · Resolution within 48h
- S3 (Medium): Action within 24h · Resolution within 7 days
- S4 (Low): Log and close within 14 days

> **Cross-reference:** SLA thresholds are also shown on the Welfare Officer Dashboard (Page 04) for quick reference. This page (Page 22) is the authoritative source for SLA definitions.

---

## 2. Role Access

| Role | Access |
|---|---|
| Group Hostel Welfare Officer | Full — create, update, close, all genders |
| Group Hostel Director | Full — all incidents |
| Group Boys Hostel Coordinator | Full — boys incidents; read-only girls |
| Group Girls Hostel Coordinator | Full — girls incidents; read-only boys |
| Group Hostel Discipline Committee | Read-only — welfare incidents linked to discipline cases |
| Group Hostel Security Coordinator | Read-only — security-linked incidents |
| Group Hostel Medical Coordinator | Read-only — medical-linked incidents |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Welfare  ›  Incident Tracker
```

### 3.2 Page Header
- **Title:** `Welfare Incident Tracker`
- **Subtitle:** `[N] Open · [N] In Progress · [N] Escalated · [N] Closed (This Month)`
- **Right controls:** `+ New Incident` · `Advanced Filters` · `Export` · `SLA Report`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| Any S1 incident open > 2h | "SLA BREACH: [N] Severity 1 incident(s) have exceeded the 2-hour escalation SLA." | Red |
| S2 incident open > 8h | "[N] Severity 2 incidents nearing 8h SLA limit." | Amber |

---

## 4. KPI Cards

| Card | Metric | Colour Rule |
|---|---|---|
| Open S1 | | Red if > 0 |
| Open S2 | | Yellow if > 0 |
| Open S3+S4 | | Blue |
| SLA Breaches (Month) | | Red if > 0 |
| Resolved Today | | Green |
| Branches with Open S1/S2 | | Red if > 0 |

---

## 5. Main Table — All Incidents

**Search:** Incident #, hosteler name, branch, keyword. 300ms debounce.

**Advanced Filters:**
| Filter | Type |
|---|---|
| Severity | Checkbox: 1/2/3/4 |
| Status | Checkbox: Open/In Progress/Escalated/Resolved/Closed |
| Gender | Radio: All/Boys/Girls |
| Branch | Multi-select |
| Incident Type | Multi-select |
| POCSO Linked | Checkbox |
| SLA Status | Checkbox: Within SLA / At Risk / Breached |
| Date Range | Date picker |
| Assigned To | Dropdown: All staff |

**Columns:**
| Column | Sortable |
|---|---|
| Incident # | ✅ |
| Severity | ✅ |
| Hosteler Name | ✅ |
| Gender | ✅ |
| Branch | ✅ |
| Type | ✅ |
| Opened At | ✅ |
| Age | ✅ (red if SLA breached) |
| Status | ✅ |
| Assigned To | ✅ |
| SLA | ✅ |
| POCSO | ✅ |
| Actions | ❌ |

**Pagination:** Server-side · 25/page.

---

## 6. Incident Type Reference

| Type | Typical Severity | POCSO Trigger |
|---|---|---|
| Physical Injury (accident) | S1/S2 | No |
| Physical Harm (assault) | S1 | Yes if child involved |
| Bullying (physical) | S2 | No |
| Bullying (verbal/cyber) | S3 | No |
| Mental Health Crisis | S1/S2 | No |
| Family Emergency | S2/S3 | No |
| Medical Emergency | S1 | No (handled via Medical tracker) |
| Homesickness | S3/S4 | No |
| Conflict (peer) | S3 | No |
| Food Complaint | S4 | No |
| POCSO Concern | S1 | Yes — mandatory |
| Missing Hosteler | S1 | Yes |
| Unauthorized Absence | S2 | No |
| Welfare Check (routine) | S4 | No |

---

## 7. Drawers

### 7.1 Drawer: `welfare-incident-detail` (see Page 04 Section 6.1 for full spec)

### 7.2 Drawer: `welfare-incident-create` (see Page 04 Section 6.2 for full spec)

---

## 8. SLA Report View

> Toggle from table to SLA compliance report.

**SLA Report displays:**
- Resolution time distribution histogram (< 2h / 2–8h / 8–24h / 24–72h / > 72h)
- SLA breach count by severity, by branch, by month
- Average resolution time trend (12 months)

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Incident created | "Welfare incident #[ID] created." | Success | 4s |
| Status updated | "Incident #[ID] updated to [Status]." | Success | 3s |
| POCSO escalation | "POCSO escalation triggered. POCSO Coordinator notified." | Warning | 6s |
| Incident closed | "Incident #[ID] closed. Timeline locked." | Success | 4s |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/welfare/incidents/` | JWT (G3+) | All incidents (paginated, filtered) |
| GET | `/api/v1/group/{group_id}/hostel/welfare/incidents/{id}/` | JWT (G3+) | Incident detail + timeline |
| POST | `/api/v1/group/{group_id}/hostel/welfare/incidents/` | JWT (G3+) | Create incident |
| PATCH | `/api/v1/group/{group_id}/hostel/welfare/incidents/{id}/` | JWT (G3+) | Update status / add note |
| POST | `/api/v1/group/{group_id}/hostel/welfare/incidents/{id}/close/` | JWT (G3+) | Close (immutable) |
| POST | `/api/v1/group/{group_id}/hostel/welfare/incidents/{id}/pocso-alert/` | JWT (G3+) | Raise POCSO alert |
| GET | `/api/v1/group/{group_id}/hostel/welfare/incidents/sla-report/` | JWT (G3+) | SLA compliance data |
| GET | `/api/v1/group/{group_id}/hostel/welfare/incidents/export/` | JWT (G3+) | Export |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
