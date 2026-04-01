# 26 — Parent Visit Scheduler

> **URL:** `/group/hostel/parent-visits/scheduler/`
> **File:** `26-parent-visit-scheduler.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Parent Visit Coordinator (primary) · Hostel Director · Boys/Girls Coordinators

---

## 1. Purpose

Full parent visit scheduling management — creating visit days, managing time slot bookings, tracking parent attendance, managing biometric gate clearance lists, and logging any violations (unauthorized entry, overstay, calling hour violations). This page is the detailed operational companion to the Parent Visit Coordinator's dashboard (Page 09).

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Parent Visits  ›  Scheduler
```

### 2.2 Page Header
- **Title:** `Parent Visit Scheduler`
- **Subtitle:** `[N] Visit Days This Month · [N] Upcoming · [N] Parent Registrations Pending`
- **Right controls:** `+ Schedule Visit Day` · `Bulk Schedule` · `Export`

---

## 3. Visit Day Calendar

> Full monthly calendar view of all scheduled parent visit days across all branches.

**Display:** Calendar grid (month view). Each visit day dot:
- Blue = Boys hostel visit day
- Pink = Girls hostel visit day
- Purple = Both genders same day
- Hover: Shows branch name + time slots + booked slots

**Actions on calendar:** Click date → View/Edit that day's schedule · Empty date + [+ Schedule] tooltip

---

## 4. Visit Day Table

> Table view with all scheduled visit days.

**Search:** Branch name. 300ms debounce.

**Filters:** Branch · Gender · Month · Status (Upcoming/Completed/Cancelled).

**Columns:**
| Column | Sortable |
|---|---|
| Branch | ✅ |
| Hostel Type | ✅ |
| Visit Date | ✅ |
| Day | ✅ (Sunday usually) |
| Time Slots | ❌ |
| Max Visitors/Slot | ✅ |
| Bookings | ✅ |
| Attendance | ✅ (post-visit only) |
| Status | ✅ |
| Actions | ❌ |

---

## 5. Drawers

### 5.1 Drawer: `parent-visit-day-detail`
- **Width:** 640px
- **Tabs:** Overview · Time Slots · Visitor List · Attendance · Biometric Gate List
- **Time Slots tab:** 10 AM–4 PM in 1-hour slots; each slot shows booked visitors vs capacity
- **Visitor List tab:** All pre-booked visitors with hosteler name, slot time, biometric status
- **Attendance tab:** Post-visit — mark which parents actually arrived (vs no-show)
- **Biometric Gate List tab:** Printable / exportable list of cleared visitors for security gate. **Export format:** Printable PDF (A4 portrait); one visitor per row; includes visitor photo (if uploaded during pre-registration), visitor name + relation, hosteler name + room number, assigned time slot, and QR code for biometric verification at gate. Large-font gate-ready layout for easy reading by security staff. Triggered via [Print Gate List] or [Download PDF] buttons within the tab.

### 5.2 Drawer: `parent-visit-schedule` (see Page 09 Section 6.2 for full spec)

### 5.3 Modal: Cancel Visit Day
- **Trigger:** Visit Day → Cancel
- **Fields:** Reason (required) · Notify all booked parents (checkbox) · Reschedule date (optional)
- **On confirm:** Status = Cancelled; parent notifications sent

---

## 6. Calling Hour Log

> Log of hostel calling hour slots and any violations per branch.

**Columns:** Branch | Designated Call Time | Hostelers with Violations (Week) | Avg Call Duration | [View Violations →]

**Violation detail drawer:** Hosteler name · Date · Violation type · Warden action.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Visit day scheduled | "Parent visit day scheduled at [Branch] for [date]. [N] parents will be notified." | Success | 4s |
| Visit day cancelled | "Visit day at [Branch] on [date] cancelled. Parents notified." | Warning | 5s |
| Attendance marked | "Attendance marked for [Branch] parent visit on [date]." | Success | 4s |
| Violation logged | "Calling hour violation logged for [Hosteler] at [Branch]." | Warning | 4s |

---

## 8. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/parent-visits/schedule/` | JWT (G3+) | All visit days |
| POST | `/api/v1/group/{group_id}/hostel/parent-visits/schedule/` | JWT (G3+) | Create visit day |
| GET | `/api/v1/group/{group_id}/hostel/parent-visits/schedule/{id}/` | JWT (G3+) | Visit day detail |
| PATCH | `/api/v1/group/{group_id}/hostel/parent-visits/schedule/{id}/` | JWT (G3+) | Edit |
| POST | `/api/v1/group/{group_id}/hostel/parent-visits/schedule/{id}/cancel/` | JWT (G3+) | Cancel |
| POST | `/api/v1/group/{group_id}/hostel/parent-visits/schedule/{id}/attendance/` | JWT (G3+) | Mark attendance |
| GET | `/api/v1/group/{group_id}/hostel/parent-visits/calling-violations/` | JWT (G3+) | Calling violations |
| POST | `/api/v1/group/{group_id}/hostel/parent-visits/calling-violations/` | JWT (G3+) | Log violation |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
