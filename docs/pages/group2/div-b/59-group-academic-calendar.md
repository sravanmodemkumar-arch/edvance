# 59 — Group Academic Calendar

> **URL:** `/group/acad/calendar/`
> **File:** `59-group-academic-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Academic Calendar Manager G3 · CAO G4 · Academic Director G3 · All Div-B roles (view) · Branch staff (view, local events via branch portal)

---

## 1. Purpose

The Group Academic Calendar is the master calendar of all academic events across the institution group — the single authoritative source from which all branches derive their own academic schedules. In a large group with 50 branches, the risk of calendaring chaos is high: branches scheduling PTMs on exam days, sports events clashing with unit tests, holidays declared without group awareness. This page eliminates that chaos by providing a centrally-managed master calendar with two tiers of events: mandatory group-wide events that branches cannot modify or delete, and optional events that branches may choose to follow or override.

Mandatory events — annual examination dates, board practical examination schedules, PTM dates, and NCPCR-required parent sessions — are locked once published. Branches can see these events in their branch portal calendar but cannot remove or reschedule them. Optional events — CPD days, inter-school sports meets, cultural programmes — are visible to branches as suggestions, and branches may adopt, modify, or skip them locally.

The calendar is the dependency hub for several other pages in Division B: the Group Exam Calendar (page 22) feeds its exam dates here; the Holiday & Working Day Manager (page 61) marks holidays on this calendar; the PTM Schedule Manager (page 60) adds PTM events; and Branch Calendar Compliance (page 62) measures how faithfully each branch adheres to the mandatory events set here. Any event created on this page that is tagged "mandatory" is immediately propagated to all branch portal calendars in scope.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Approve mandatory events | Mandatory events require CAO approval before publication |
| Group Academic Director | G3 | ✅ Full | ✅ View + coordinate | Can propose events; cannot publish mandatory without CAO |
| Group Curriculum Coordinator | G2 | ✅ View | ❌ | Read-only |
| Group Exam Controller | G3 | ✅ View | ❌ | Read-only |
| Group Results Coordinator | G3 | ✅ View | ❌ | Read-only |
| Stream Coordinators (all) | G3 | ✅ View | ❌ | Read-only |
| Group JEE/NEET Integration Head | G3 | ✅ View | ❌ | Read-only |
| Group IIT Foundation Director | G3 | ✅ View | ❌ | Read-only |
| Group Olympiad & Scholarship Coord | G3 | ✅ View | ❌ | View olympiad-tagged events |
| Group Special Education Coordinator | G3 | ✅ View | ❌ | Read-only |
| Group Academic MIS Officer | G1 | ✅ View | ❌ | Read-only |
| Group Academic Calendar Manager | G3 | ✅ Full | ✅ Full CRUD | Primary owner of this page |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Academic Calendar Management  ›  Group Academic Calendar
```

### 3.2 Page Header
```
Group Academic Calendar                               [+ New Event]  [Export Calendar ↓]
Academic Year [YYYY–YY] · [Group Name]                          (Calendar Manager, CAO)
```

**View toggle:** [Month] (default) | [Week] | [List]

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Events This Year | Count |
| Mandatory Events | Count — blue |
| Optional Events | Count — teal |
| Events This Month | Count |
| Upcoming Events (Next 7 Days) | Count |
| Branches Confirmed (Mandatory Events) | X / Y branches |

---

## 4. Main Content

### 4.1 Calendar View (Month — Default)

Standard month-grid calendar with events shown as chips:
- **Exam events:** Red chips
- **PTM events:** Blue chips
- **Holiday events:** Grey chips
- **Sports events:** Green chips
- **Cultural events:** Orange chips
- **CPD events:** Purple chips
- **Mandatory badge:** Gold lock icon on mandatory events

**Navigation:** Previous month / Next month / Today · Academic year selector

**Click on event chip:** Opens `event-view` drawer (480px)
**Click on empty day:** If Calendar Manager, opens `calendar-event-create` drawer

### 4.2 Week View

7-day grid with time slots (8:00 AM – 8:00 PM). Events plotted as blocks.

### 4.3 List View (Table)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Calendar Manager only |
| Event Name | Text | ✅ | |
| Type | Badge | ✅ | Exam / PTM / Holiday / Sports / Cultural / CPD |
| Date | Date | ✅ | |
| Duration | Text | ✅ | e.g. "1 day" / "2–4 March" |
| Branch Scope | Text | ❌ | All / Zone / [Branches] |
| Mandatory | Badge | ✅ | Yes (lock) / No |
| Notification Sent | Badge | ✅ | Yes / No |
| Actions | — | ❌ | Role-based |

**Default sort:** Date ascending.

**Pagination:** Server-side · Default 25/page in list view · Selector 10/25/50/All.

### 4.4 Search (List view only)
- Full-text across: Event name
- 300ms debounce

### 4.5 Advanced Filters (slide-in drawer)

| Filter | Type | Options |
|---|---|---|
| Event Type | Multi-select | Exam / PTM / Holiday / Sports / Cultural / CPD |
| Mandatory | Select | Yes / No |
| Branch Scope | Select | All branches / Zone / Specific branch |
| Month | Month picker | |
| Notification Status | Select | Sent / Not sent |

### 4.6 Row Actions (List view) / Click actions (Calendar view)

| Action | Visible To | Drawer | Notes |
|---|---|---|---|
| View | All roles | `event-view` drawer 480px | Full event details + branch confirmation |
| Edit | Calendar Manager | `calendar-event-create` drawer (pre-filled) | Cannot edit mandatory after CAO approval |
| Cancel | Calendar Manager | Confirm modal | Audited; mandatory cancellation reason + notify |
| Duplicate | Calendar Manager | `calendar-event-create` pre-filled | Copy to another date |
| Notify Branches | Calendar Manager | Confirm modal | Re-send notification to branch contacts |

### 4.7 Bulk Actions (Calendar Manager, List view only)

| Action | Notes |
|---|---|
| Export Selected (CSV/XLSX) | Selected events |
| Notify Selected Branches | Bulk notification for selected events |

---

## 5. Drawers & Modals

### 5.1 Drawer: `calendar-event-create` — New / Edit Event
- **Trigger:** [+ New Event] button or empty day click or Edit action
- **Width:** 520px

| Field | Type | Required | Validation |
|---|---|---|---|
| Event Name | Text | ✅ | Min 3, max 200 chars |
| Event Type | Select | ✅ | Exam / PTM / Holiday / Sports / Cultural / CPD / Other |
| Start Date | Date | ✅ | Within current academic year |
| End Date | Date | ✅ | ≥ Start date |
| Start Time | Time | ❌ | If time-specific event |
| End Time | Time | Conditional | Required if Start Time set |
| Description | Textarea | ❌ | Max 500 chars |
| Branch Scope | Multi-select | ✅ | All branches / Zone / Specific branches |
| Mandatory | Toggle | ✅ | Default off; toggling on shows CAO-approval notice |
| Notify branches on save | Toggle | ✅ | Default on |
| Notification channel | Select | Conditional | Email / WhatsApp / Both — required if Notify on |

**Mandatory event notice:** If Mandatory toggle = on: "This event will be locked on all branch calendars and cannot be removed by branches. CAO approval is required before publication."

- **Submit:** "Save Event" (Calendar Manager — saves as draft if mandatory) / "Submit for CAO Approval" (if mandatory)
- **On success:** Event appears on calendar · Notifications queued if toggle on

### 5.2 Drawer: `event-view`
- **Width:** 480px
- **Content:**
  - Event name · Type badge · Date/time · Duration · Mandatory badge (if applicable)
  - Branch scope
  - Branch confirmation status: Table of branches in scope — Confirmed / Pending / Not required
  - Description
  - Notification log: When sent · Channel · Recipients count
  - [Edit Event] button (Calendar Manager only)

### 5.3 Modal: `cancel-event-confirm`
- **Width:** 420px
- **Content:** "Cancel [Event Name] on [Date]?"
- **Fields:** Reason (required, min 20 chars) · Notify branches (checkbox, default on) · Channel (Email/WhatsApp/Both)
- **Buttons:** [Confirm Cancel] (danger) · [Cancel]
- **On confirm:** Event marked cancelled (shown in red strikethrough on calendar) · Branches notified · Audit log

### 5.4 Modal: `cao-approval-mandatory`
- **Trigger:** Calendar Manager submits a mandatory event
- **Width:** 420px (shown to CAO as a pending action)
- **Content:** "[Calendar Manager Name] has submitted [Event Name] on [Date] as a mandatory event for [N] branches."
- **Fields:** Approve note (optional) / Reject reason (if rejecting, required)
- **Buttons:** [Approve & Publish] (green) · [Reject] (danger) · [Cancel]
- **On approve:** Event published; branches notified immediately

---

## 6. Charts

### 6.1 Event Density by Month (Bar)
- **Type:** Vertical bar (stacked by event type)
- **Data:** Count of events per month this academic year
- **Colour:** Each event type = its calendar colour
- **Tooltip:** Month · Event types breakdown
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "Event '[Name]' added to group calendar" | Success | 4s |
| Mandatory event submitted | "Mandatory event submitted for CAO approval" | Info | 4s |
| Mandatory event approved | "'[Name]' approved by CAO and published to all branches" | Success | 4s |
| Event updated | "Event '[Name]' updated" | Success | 4s |
| Event cancelled | "Event '[Name]' cancelled. Branches notified." | Warning | 6s |
| Notification sent | "Notification sent to [N] branches for '[Name]'" | Success | 4s |
| Event duplicated | "Event duplicated — edit the date in the drawer" | Info | 4s |
| Export started | "Calendar export preparing…" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No events this month | "No events this month" | "No academic events have been scheduled for this month" | [+ New Event] |
| No events match filters | "No events match your filters" | "Clear filters to see all events" | [Clear Filters] |
| Academic year not configured | "Academic year not set" | "Configure the academic year dates before adding events" | [Configure Academic Year] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + calendar grid (month placeholder) |
| Month navigation | Spinner in calendar grid → month renders |
| List view load | Skeleton table rows |
| Event create drawer | Spinner → form |
| Event view drawer | Spinner → content |
| Notification send | Spinner in confirm button |
| Export trigger | Spinner in export button |

---

## 10. Role-Based UI Visibility

| Element | Calendar Mgr G3 | CAO G4 | Academic Dir G3 | All other Div-B |
|---|---|---|---|---|
| [+ New Event] | ✅ | ❌ | ❌ | ❌ |
| Edit event | ✅ | ❌ | ❌ | ❌ |
| Cancel event | ✅ | ❌ | ❌ | ❌ |
| Approve mandatory events | ❌ | ✅ | ❌ | ❌ |
| Duplicate event | ✅ | ❌ | ❌ | ❌ |
| Notify branches | ✅ | ❌ | ❌ | ❌ |
| Bulk actions | ✅ | ❌ | ❌ | ❌ |
| Export | ✅ | ✅ | ✅ | ❌ |
| View (all views) | ✅ | ✅ | ✅ | ✅ |
| Branch confirmation status | ✅ | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/calendar/` | JWT | List / calendar events |
| GET | `/api/v1/group/{group_id}/acad/calendar/stats/` | JWT | Stats bar |
| POST | `/api/v1/group/{group_id}/acad/calendar/events/` | JWT (G3 Cal Mgr) | Create event |
| GET | `/api/v1/group/{group_id}/acad/calendar/events/{id}/` | JWT | Event detail |
| PUT | `/api/v1/group/{group_id}/acad/calendar/events/{id}/` | JWT (G3 Cal Mgr) | Update event |
| PATCH | `/api/v1/group/{group_id}/acad/calendar/events/{id}/cancel/` | JWT (G3 Cal Mgr) | Cancel event |
| POST | `/api/v1/group/{group_id}/acad/calendar/events/{id}/approve/` | JWT (G4 CAO) | CAO mandatory event approval |
| POST | `/api/v1/group/{group_id}/acad/calendar/events/{id}/notify/` | JWT (G3 Cal Mgr) | Send/resend notifications |
| GET | `/api/v1/group/{group_id}/acad/calendar/events/export/?format=xlsx` | JWT | Export |
| GET | `/api/v1/group/{group_id}/acad/calendar/charts/density-by-month/` | JWT | Density bar chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month navigate | `click` | GET `.../calendar/?month=&year=` | `#calendar-grid` | `innerHTML` |
| List view filter | `click` | GET `.../calendar/?view=list&filters=` | `#event-list-section` | `innerHTML` |
| List search | `input delay:300ms` | GET `.../calendar/?q=` | `#event-list-body` | `innerHTML` |
| Event create drawer | `click` (day click or button) | GET `.../calendar/events/create-form/?date=` | `#drawer-body` | `innerHTML` |
| Event create submit | `submit` | POST `.../calendar/events/` | `#drawer-body` | `innerHTML` |
| Event view drawer | `click` | GET `.../calendar/events/{id}/` | `#drawer-body` | `innerHTML` |
| Cancel confirm | `click` | PATCH `.../calendar/events/{id}/cancel/` | `#calendar-grid` | `innerHTML` |
| Notify branches | `click` | POST `.../calendar/events/{id}/notify/` | `#toast-container` | `beforeend` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
