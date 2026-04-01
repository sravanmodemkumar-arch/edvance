# 09 — Parent Visit Coordinator Dashboard

> **URL:** `/group/hostel/parent-visits/`
> **File:** `09-parent-visit-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Parent Visit Coordinator (Role 75, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Parent Visit Coordinator. Manages scheduled parent visits to hostels across all branches — visit slot scheduling, pre-approved visitor registration (biometric gate clearance), adherence to visiting hour policies, and restricted calling hour compliance for hostelers.

In residential educational institutions, parent visits are tightly regulated:
- **Visiting hours:** Typically Sunday 10 AM–4 PM (varies by branch policy)
- **Authorised visitors:** Only registered parents/guardians with valid ID — no siblings below 18 without guardian
- **Girls hostel:** Father / male guardian entry requires additional verification; female relatives preferred
- **Biometric clearance:** Parents must be pre-registered for biometric gate entry — walk-in denied
- **Calling hours:** Hostelers can call parents only during designated slots (typically evening, 20 minutes per day) — compliance tracked

This coordinator ensures all 20–50 branch hostels follow the same visit protocol and reports violations to the Hostel Director.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Parent Visit Coordinator | G3 | Full — all branches | Exclusive dashboard |
| Group Boys Hostel Coordinator | G3 | View — boys hostel visit data | Via own dashboard |
| Group Girls Hostel Coordinator | G3 | View — girls hostel visit data | Via own dashboard |
| Group Hostel Security Coordinator | G3 | View — biometric gate + unauthorized visitor data | Via own dashboard |
| Group Hostel Director | G3 | View — visit summary | Via own dashboard |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Parent Visit Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]           [+ Schedule Visit Day]  [Export Report ↓]  [Settings ⚙]
Group Parent Visit Coordinator · Today: [date]
Upcoming Visits: [N]  ·  This Week Visits: [N]  ·  Calling Violations (Week): [N]
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Unauthorized parent entry logged at any branch | "Unauthorized parent entry at [Branch] [Girls/Boys] Hostel — parent not pre-registered." | Red |
| Visiting hours violation (after-hours entry) | "After-hours visitor entry at [Branch] — [N] incidents in the last 7 days." | Amber |
| Visit day not scheduled for any branch this month | "[Branch] has no parent visit day scheduled this month. Parents may raise complaints." | Amber |
| Calling hour violations > 10 this week | "[Branch] recorded [N] calling hour violations this week. Warden action required." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Upcoming Visit Days (Next 30d) | Count of scheduled visit days across all branches | Blue always | → Page 26 |
| Pre-registered Visitors (Active) | Parents/guardians with biometric clearance | Blue always | → Page 25 |
| Unauthorized Entries (This Month) | Visitors denied or flagged as unauthorized | Green = 0 · Yellow 1–5 · Red > 5 | → Page 25 |
| Calling Violations (This Week) | Hostelers who called outside designated hours | Green = 0 · Yellow 1–10 · Red > 10 | — (calling log section) |
| Branches with No Visit Scheduled (This Month) | Branches that haven't set a visit day | Green = 0 · Amber > 0 | → Page 26 |
| Visit Requests Pending (Parental Requests) | Parent requests for ad hoc visits pending approval | Yellow > 0 | → Page 26 |

**HTMX:** `hx-trigger="every 10m"` → KPI auto-refresh.

---

## 5. Sections

### 5.1 Upcoming Visit Days Calendar

> Visual 30-day calendar showing scheduled visit days per branch.

**Display:** Calendar grid. Each visit day shown as a colored dot on the date:
- Blue = Boys hostel visit day
- Pink = Girls hostel visit day
- Purple = Both on same day

Click on a date → opens `parent-visit-schedule` drawer for that date.

---

### 5.2 Branch Visit Status Table

> Per-branch visit scheduling and compliance status.

**Search:** Branch name, city. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches with hostel |
| Gender | Radio | All / Boys / Girls |
| Visit Scheduled | Radio | Any / Yes / No (this month) |
| Compliance | Radio | Any / Has Violations / Clean |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → visit detail drawer |
| Next Visit Day | ✅ | Date or "Not Scheduled" (red) |
| Pre-registered Visitors | ✅ | Count (Boys + Girls) |
| Last Visit (Boys) | ✅ | Date |
| Last Visit (Girls) | ✅ | Date |
| Unauthorized Entries (Month) | ✅ | Count (red if > 0) |
| Calling Violations (Week) | ✅ | Count |
| Visit Policy Status | ✅ | ✅ Compliant / ⚠ Issues / ❌ Not Scheduled |
| Actions | ❌ | View · Schedule · Log Violation |

**Pagination:** Server-side · 25/page.

---

### 5.3 Pending Parental Visit Requests

> Ad hoc parent visit requests (outside scheduled visit days) awaiting coordinator approval.

**Columns:** Request # · Parent Name · Hosteler Name · Branch · Gender · Reason · Requested Date · [Approve] [Decline]

---

### 5.4 Calling Hour Compliance Log

> Log of calling hour violations per branch this week.

**Quick table:** Branch | Date | Hosteler Name | Violation Type (Called after hours / Called unauthorised number / Exceeded time limit) | Action Taken | Warden Name

"This Week" filter active by default. [View Historical →] expands date range.

---

## 6. Drawers

### 6.1 Drawer: `branch-visit-detail`
- **Width:** 640px
- **Tabs:** Scheduled Visits · Pre-registered Visitors · Violations · Calling Compliance · Policy
- **Scheduled Visits tab:** Next 3 visit days, historical visits with attendance count
- **Pre-registered Visitors tab:** Table of all cleared parents/guardians with biometric status
- **Violations tab:** Unauthorized entries and calling hour violations
- **Policy tab:** Branch-specific visiting hours, calling hours, visitor rules

### 6.2 Drawer: `parent-visit-schedule`
- **Trigger:** + Schedule Visit Day or calendar date click
- **Width:** 560px
- **Fields:**
  - Branch (multi-select for bulk scheduling)
  - Hostel Type (Boys / Girls / Both)
  - Visit Date (date picker — must be Sunday by default, overridable)
  - Visit Slots: Start time / End time (default 10 AM–4 PM)
  - Max Visitors per Slot (number)
  - Pre-registration Deadline (date, default 3 days before)
  - Special Note (e.g., "Parents must bring Aadhaar + last fee receipt")
  - Notify All Parents (checkbox — WhatsApp broadcast to all hosteler parents)
- **On submit:** Visit day created in all selected branches; parent notifications queued

### 6.3 Drawer: `visitor-register-create` (pre-registration)
- **Trigger:** Via Page 25 Visitor Management → Pre-registered Visitor List section → `+ Pre-register Visitor` button (distinct from the `+ New Entry` button which logs a day-of visitor entry)
- **Width:** 520px
- **Fields:** Parent/Guardian name · Relation · Mobile · Aadhaar/ID type + number · Hosteler search (autocomplete) · Biometric registration date · Photo upload

### 6.4 Modal: Approve/Decline Ad Hoc Visit Request
- **Type:** Centred modal (480px)
- **Approve fields:** Date · Time slot · Security note
- **Decline fields:** Reason (required)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Visit day scheduled | "Parent visit day scheduled at [N] branches for [date]. Parents will be notified." | Success | 4s |
| Ad hoc visit approved | "Visit approved for [Parent Name] to see [Hosteler Name] on [date]." | Success | 4s |
| Visit declined | "Visit request declined. Parent notified with reason." | Info | 4s |
| Violation logged | "Calling hour violation logged for [Hosteler Name] at [Branch]." | Warning | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No upcoming visit days | "No Parent Visit Days Scheduled" | "Schedule parent visit days for all hostel branches to avoid parent complaints." | [+ Schedule Visit Day] |
| No pending visit requests | "No Pending Visit Requests" | — | — |
| No calling violations this week | "No Calling Hour Violations This Week" | — | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + calendar + branch table (8 rows) + calling log |
| Calendar month change | Calendar shimmer |
| Branch table filter | Inline skeleton rows |
| Schedule drawer submit | Spinner on Schedule; calendar refreshes |

---

## 10. Role-Based UI Visibility

| Element | Parent Visit Coordinator G3 | Boys Coordinator G3 | Girls Coordinator G3 | Hostel Director G3 |
|---|---|---|---|---|
| Schedule visit day | ✅ All branches | ✅ Boys branches | ✅ Girls branches | ✅ |
| Approve ad hoc visit | ✅ | ❌ | ❌ | ✅ |
| Pre-register visitor | ✅ | ✅ Boys | ✅ Girls | ✅ |
| Log calling violation | ✅ | ✅ Boys | ✅ Girls | ✅ |
| View girls hostel data | ✅ | ❌ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/parent-visits/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/parent-visits/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/parent-visits/scheduled/` | JWT (G3+) | Upcoming visit days |
| POST | `/api/v1/group/{group_id}/hostel/parent-visits/schedule/` | JWT (G3+) | Schedule new visit day |
| GET | `/api/v1/group/{group_id}/hostel/parent-visits/requests/` | JWT (G3+) | Ad hoc requests |
| POST | `/api/v1/group/{group_id}/hostel/parent-visits/requests/{id}/approve/` | JWT (G3+) | Approve request |
| POST | `/api/v1/group/{group_id}/hostel/parent-visits/requests/{id}/decline/` | JWT (G3+) | Decline request |
| GET | `/api/v1/group/{group_id}/hostel/parent-visits/calling-violations/` | JWT (G3+) | Calling hour violations |
| POST | `/api/v1/group/{group_id}/hostel/parent-visits/calling-violations/` | JWT (G3+) | Log new violation |
| GET | `/api/v1/group/{group_id}/hostel/parent-visits/branches/` | JWT (G3+) | Branch visit status table |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 10m` | GET `.../parent-visits/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Calendar month navigate | `click` on next/prev | GET `.../parent-visits/scheduled/?month={M}&year={Y}` | `#visit-calendar` | `innerHTML` |
| Calendar date click | `click` on date | GET `.../parent-visits/scheduled/?date={date}` | `#drawer-body` | `innerHTML` |
| Branch table filter | `click` | GET `.../parent-visits/branches/?{filters}` | `#branch-table-section` | `innerHTML` |
| Schedule visit submit | `click` on Schedule | POST `.../parent-visits/schedule/` | `#visit-calendar` | `innerHTML` |
| Approve ad hoc visit | `click` on Approve | POST `.../requests/{id}/approve/` | `#request-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
