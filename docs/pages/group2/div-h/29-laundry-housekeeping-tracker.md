# 29 — Laundry & Housekeeping Tracker

> **URL:** `/group/hostel/housekeeping/`
> **File:** `29-laundry-housekeeping-tracker.md`
> **Template:** `portal_base.html`
> **Priority:** P2
> **Role:** Group Hostel Director (primary) · Hostel Welfare Officer (view)

---

## 1. Purpose

Tracking of housekeeping standards and laundry services across hostel campuses. The Group Laundry / Housekeeping Coordinator (Role 77, G0) has NO EduForge access — their work is tracked here by the Hostel Director based on reports from Branch Wardens. The Director can see scheduled cleaning cycles, housekeeping quality inspection results, laundry service schedules, and contractor details.

This page does not replace the coordinator's work — it makes their output visible and accountable in the EduForge system.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Laundry & Housekeeping
```

### 2.2 Page Header
- **Title:** `Laundry & Housekeeping Tracker`
- **Subtitle:** `[N] Hostel Campuses · [N] Housekeeping Schedules Active · [N] Inspections This Month`
- **Right controls:** `+ New Schedule` · `+ Log Inspection` · `Export`

---

## 3. Housekeeping Schedule Table

> Cleaning and housekeeping schedules per campus area.

**Columns:** Branch | Hostel | Area (Rooms/Corridor/Washrooms/Common Areas/Kitchen) | Frequency | Contractor | Last Done | Next Due | Status | Actions

Status: ✅ On schedule / ⚠ Due today / ❌ Overdue

---

## 4. Housekeeping Inspection Log

> Quality inspection records logged by Branch Wardens.

**Search:** Branch name. 300ms debounce.

**Filters:** Branch · Area · Result (Pass/Fail) · Date range.

**Columns:**
| Column | Sortable |
|---|---|
| Branch | ✅ |
| Date | ✅ |
| Area Inspected | ✅ |
| Inspector (Warden) | ✅ |
| Score (0–10) | ✅ |
| Issues Found | ❌ |
| Corrective Action | ✅ |
| Status | ✅ |
| Actions | ❌ |

---

## 5. Laundry Service Table

> Laundry contractor details and schedule per campus.

**Columns:** Branch | Hostel | Contractor | Service Days | Collection Time | Return Time | Contract Expires | Actions

---

## 6. Drawers

### 6.1 Drawer: `housekeeping-schedule-create`
- **Trigger:** + New Schedule
- **Width:** 480px
- **Fields:** Branch · Hostel · Area · Frequency (Daily/Weekly/Bi-weekly/Monthly) · Contractor / In-house · Next due date · Notes

### 6.2 Drawer: `inspection-log-create`
- **Trigger:** + Log Inspection
- **Width:** 480px
- **Fields:** Branch · Hostel · Date · Areas inspected (checkboxes) · Per-area score (0–10) · Issues found (textarea) · Corrective action required (checkbox + deadline) · Photos (optional upload)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Schedule created | "Housekeeping schedule created for [Branch]." | Success | 4s |
| Inspection logged | "Housekeeping inspection logged for [Branch]." | Success | 4s |
| Corrective action flagged | "Corrective action required at [Branch]. Warden notified." | Warning | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No schedules | "No Housekeeping Schedules Configured" | "Set up cleaning schedules for all hostel campuses." | [+ New Schedule] |
| No inspections this month | "No Inspections Logged This Month" | — | [+ Log Inspection] |

---

## 9. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/housekeeping/schedules/` | JWT (G3+) | Housekeeping schedules |
| POST | `/api/v1/group/{group_id}/hostel/housekeeping/schedules/` | JWT (G3+) | Create schedule |
| GET | `/api/v1/group/{group_id}/hostel/housekeeping/inspections/` | JWT (G3+) | Inspection log |
| POST | `/api/v1/group/{group_id}/hostel/housekeeping/inspections/` | JWT (G3+) | Log inspection |
| GET | `/api/v1/group/{group_id}/hostel/housekeeping/laundry/` | JWT (G3+) | Laundry schedules |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
