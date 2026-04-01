# 27 — Hostel Medical Tracker

> **URL:** `/group/hostel/medical/tracker/`
> **File:** `27-hostel-medical-tracker.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Hostel Medical Coordinator (primary) · Hostel Director · Welfare Officer (view)

---

## 1. Purpose

Complete medical room visit log and health monitoring system for all hostelers across all branches. Every medical room visit — from a routine headache complaint to a medical emergency — is recorded here with the attending doctor/nurse, diagnosis, prescription, and follow-up plan. The Medical Tracker also maintains the list of hostelers on ongoing medical watch (chronic conditions, post-emergency monitoring).

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Medical  ›  Medical Tracker
```

### 2.2 Page Header
- **Title:** `Hostel Medical Tracker`
- **Subtitle:** `Medical Visits Today: [N] · Active Emergencies: [N] · On Medical Watch: [N] · Medical Rooms Operational: [N/N]`
- **Right controls:** `+ Log Medical Visit` · `+ Schedule Doctor Visit` · `Advanced Filters` · `Export`

---

## 3. KPI Cards

| Card | Metric | Colour Rule |
|---|---|---|
| Medical Rooms Operational | Online / Total | Green = All · Red < All |
| Active Emergencies | | Green = 0 · Red > 0 |
| Medical Visits Today | | Blue |
| Medical Visits This Month | | Blue |
| On Medical Watch | | Yellow > 0 |
| Prescriptions Pending Pickup | | Yellow > 0 |

**HTMX:** `hx-trigger="every 5m"` → KPI auto-refresh.

---

## 4. Medical Room Status Table

> Operational status per hostel medical room.

**Columns:** Branch | Hostel | Medical Room Status | Nurse on Duty | Last Stocking Date | Equipment Status | Actions

Columns are configurable; rows with issues (no nurse, equipment fault) shown in amber/red.

---

## 5. Medical Visit Log Table

> All medical visits — searchable and filterable.

**Search:** Hosteler name, branch, doctor name. 300ms debounce.

**Filters:** Branch · Gender · Severity · Date range · Doctor · On Medical Watch filter.

**Columns:**
| Column | Sortable |
|---|---|
| Visit # | ✅ |
| Date / Time | ✅ |
| Hosteler Name | ✅ |
| Gender | ✅ |
| Branch | ✅ |
| Complaint | ✅ |
| Doctor / Nurse | ✅ |
| Diagnosis | ❌ (truncated) |
| Prescription | ❌ (truncated) |
| Severity | ✅ |
| Follow-up Date | ✅ |
| Prescription Collected | ✅ |
| Actions | ❌ |

**Pagination:** Server-side · 25/page.

---

## 6. Medical Watch List

> Hostelers requiring ongoing health monitoring.

**Columns:** Hosteler | Branch | Hostel | Condition | Doctor | Last Check | Next Check | Status | Actions

Red rows for hostelers whose next check date has passed without a logged visit.

---

## 7. Doctor Visit Schedule

> Upcoming and past doctor visits across all campuses.

**Columns:** Branch | Doctor Name | Specialty | Date | Time | Hostel | Recurring | Status | Actions

**Actions:** View report · Mark completed · Reschedule.

---

## 8. Drawers

### 8.1 Drawer: `medical-visit-detail`
- **Width:** 560px
- **Tabs:** Overview · Prescription · Follow-up · History
- **Overview:** Hosteler details, complaint, doctor notes, diagnosis
- **Prescription tab:** Full prescription with drug name, dose, frequency, duration · [Mark Collected] button
- **Follow-up:** Next visit date if required, notes for next visit
- **History:** Previous 5 medical visits for the same hosteler

### 8.2 Drawer: `medical-visit-create` (see Page 10 Section 6.1)

### 8.3 Drawer: `medical-watch-add`
- **Trigger:** + Add to Medical Watch
- **Width:** 480px
- **Fields:** Hosteler · Condition (text) · Medications (repeatable) · Check frequency (Daily / Every 2 days / Weekly) · Doctor assigned · Start date · Notes

---

## 9. Medical Emergency Protocol

> When a visit is logged as "Emergency" severity:
1. Emergency flag auto-set on hosteler record
2. Group Emergency Response Officer alerted via WhatsApp
3. Parent contacted via WhatsApp: "Your child [Name] at [Branch] hostel has been taken to [Medical facility]. Please contact [number]."
4. Branch Principal alerted
5. Medical Emergency entry created in audit log (immutable)
6. Follow-up flag set: coordinator must log a "Emergency Resolved" event within 24h

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Visit logged | "Medical visit logged for [Hosteler Name]." | Success | 4s |
| Emergency flagged | "MEDICAL EMERGENCY: Emergency Response Officer and parent notified." | Error | Manual dismiss |
| Doctor visit scheduled | "Doctor visit scheduled at [Branch] for [date]." | Success | 4s |
| Prescription collected | "Prescription marked as collected by [Hosteler Name]." | Success | 3s |
| Medical watch added | "[Hosteler Name] added to medical watch. Check due: [date]." | Info | 5s |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/medical/visits/` | JWT (G3+) | Visit log (paginated, filtered) |
| POST | `/api/v1/group/{group_id}/hostel/medical/visits/` | JWT (G3+) | Log visit |
| GET | `/api/v1/group/{group_id}/hostel/medical/visits/{id}/` | JWT (G3+) | Visit detail |
| PATCH | `/api/v1/group/{group_id}/hostel/medical/visits/{id}/prescription-collected/` | JWT (G3+) | Mark prescription collected |
| GET | `/api/v1/group/{group_id}/hostel/medical/watch-list/` | JWT (G3+) | Medical watch list |
| POST | `/api/v1/group/{group_id}/hostel/medical/watch-list/` | JWT (G3+) | Add to watch |
| GET | `/api/v1/group/{group_id}/hostel/medical/doctor-schedule/` | JWT (G3+) | Doctor visit schedule |
| POST | `/api/v1/group/{group_id}/hostel/medical/doctor-schedule/` | JWT (G3+) | Schedule doctor visit |
| GET | `/api/v1/group/{group_id}/hostel/medical/rooms/` | JWT (G3+) | Medical room status |
| POST | `/api/v1/group/{group_id}/hostel/medical/visits/{id}/emergency/` | JWT (G3+) | Flag as emergency |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
