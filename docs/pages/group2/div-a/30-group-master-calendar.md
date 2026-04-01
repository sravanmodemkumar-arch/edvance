# 30 — Group Master Calendar

> **URL:** `/group/gov/master-calendar/`
> **File:** `30-group-master-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 · CEO G4 · President G4 · VP G4 · Exec Secretary G3 · Trustee G1 (read) · Advisor G1 (read)

---

## 1. Purpose

Group-wide unified calendar aggregating all institutional events: academic milestones (term dates,
exams, results), operational events (compliance renewals, board meetings, audits), communications
(circulars, announcements), and custom group events. Serves as the single source of truth for
group scheduling and prevents date conflicts.

Branch-level events are visible (read-only at group level). Group-level events propagate down to
branches. Chairman/MD/Exec Secretary create and manage group events.

---

## 2. Role Access

| Role | Create Events | Edit Events | Delete Events | View All | View Notes |
|---|---|---|---|---|---|
| Chairman | ✅ | ✅ | ✅ | ✅ | ✅ |
| MD | ✅ | ✅ | ✅ | ✅ | ✅ |
| CEO | ✅ | ✅ | ❌ | ✅ | ✅ |
| President | ✅ Academic | ✅ Academic | ❌ | Academic + Group | ✅ |
| VP | ✅ Ops | ✅ Ops | ❌ | Ops + Group | ✅ |
| Exec Secretary | ✅ | ✅ | ❌ | ✅ | ✅ |
| Trustee | ❌ | ❌ | ❌ | ✅ | ❌ |
| Advisor | ❌ | ❌ | ❌ | ✅ | ❌ |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Group Master Calendar
```

### 3.2 Page Header
```
Group Master Calendar                                  [+ Add Event]  [Export Calendar ↓]
[Academic Year: Apr 2025 – Mar 2026]  [N] events this month    (role-based button visibility)
```

### 3.3 View Controls
```
[Month]  [Week]  [List]  |  ← [Mar 2026] →  |  [Today]  |  [Jump to Date]
```

### 3.4 Filter Bar (persistent, above calendar)
**Event Type filters (toggle chips):**
```
[Academic] [Exam] [Fee] [Board Meeting] [Compliance] [Communication] [Operational] [Holiday] [Custom]
```

**Branch filter:** All Branches (default) · Group-level Only · Select Branch (dropdown).

---

## 4. Calendar Views

### 4.1 Month View

**Grid:** Standard calendar month grid — 6 rows × 7 columns.

**Event display per day cell:**
- Max 3 events shown + "[+N more]" overflow link → tooltip listing all
- Event chips: coloured by type, truncated with full tooltip on hover
- Today: highlighted cell background
- Current academic year term boundaries: subtle shaded background per term

**Event colour coding:**
| Type | Colour |
|---|---|
| Academic Milestone | Blue (`bg-blue-100 border-blue-400`) |
| Exam | Orange (`bg-orange-100 border-orange-400`) |
| Fee Event | Yellow (`bg-yellow-100 border-yellow-400`) |
| Board Meeting | Purple (`bg-purple-100 border-purple-400`) |
| Compliance Deadline | Red (`bg-red-100 border-red-400`) |
| Communication (Circular/Announcement) | Green (`bg-green-100 border-green-400`) |
| Operational | Slate (`bg-slate-100 border-slate-400`) |
| Holiday | Gray (`bg-gray-100 border-gray-400`) |
| Custom | Indigo (`bg-indigo-100 border-indigo-400`) |

**Click on day cell (empty):** Opens `calendar-event-create` drawer with date pre-filled.

**Click on event chip:** Opens `calendar-event-detail` drawer.

### 4.2 Week View

**Hours grid:** 06:00 – 22:00 (rows) × 7 days (columns).

**All-day events:** Shown in banner row above the time grid.

**Event blocks:** Height proportional to duration. Overlapping events shown side-by-side.

**Click on time slot:** Opens `calendar-event-create` drawer with date + time pre-filled.

### 4.3 List View

**Display:** Chronological list — grouped by month header.

**Columns per event row:**

| Column | Type | Notes |
|---|---|---|
| Date | Date | DD MMM YYYY (Day) |
| Time | Text | HH:MM – HH:MM or "All Day" |
| Event Title | Text + link | Opens event detail drawer |
| Type | Badge (coloured) | |
| Branch/Scope | Text | All Branches · Group · Branch Name |
| Category | Badge | |
| Created By | Text | |
| Actions | — | View · Edit · Delete |

**Default:** Current date forward (upcoming events).

**Toggle:** [Show Past Events] button to include historical.

**Pagination:** 50 events per page (list view only).

---

## 5. Drawers & Modals

### 5.1 Drawer: `calendar-event-create` / `calendar-event-edit`
- **Trigger:** [+ Add Event], day cell click, or [Edit] on event
- **Width:** 560px
- **Tabs:** Details · Recurrence · Branches · Notify

#### Tab: Details
| Field | Type | Required | Validation |
|---|---|---|---|
| Event Title | Text | ✅ | Min 3, max 150 chars |
| Event Type | Select | ✅ | Academic · Exam · Fee · Board Meeting · Compliance · Communication · Operational · Holiday · Custom |
| Category | Select | ✅ | Depends on type (e.g. Exam → Internal/Board/Competitive) |
| All Day | Toggle | ✅ | Default Off |
| Start Date | Date | ✅ | |
| Start Time | Time | Conditional | Hidden if All Day |
| End Date | Date | ✅ | ≥ Start date |
| End Time | Time | Conditional | Hidden if All Day; after Start Time |
| Description / Notes | Textarea | ❌ | Max 500 chars |
| Colour Override | Colour picker | ❌ | Override default type colour |
| Attachments | File upload | ❌ | PDF/DOCX/XLSX · Max 10MB · Multiple |

**Conflict detection (inline warning):**
- If another event of the same type overlaps for the same audience → yellow warning: "Conflict with [Event Name] on [date]. Proceed?"

#### Tab: Recurrence
| Field | Type | Required |
|---|---|---|
| Repeat | Toggle | ❌ |
| Frequency | Select | Conditional | Daily · Weekly (choose days) · Monthly (date/weekday) · Yearly · Custom |
| Repeat Until | Radio | Conditional | On Date · After N occurrences · Indefinitely |
| End Date | Date | Conditional | |
| Occurrences | Number | Conditional | Max 100 |

**Edit scope for recurring events:**
- On edit: "Edit this event only · This and future events · All events in series"

#### Tab: Branches
| Field | Type | Required |
|---|---|---|
| Apply To | Radio | ✅ | All Branches · Group Level Only · Select Branches |
| Select Branches | Multi-select | Conditional | |
| Visible To | Radio | ❌ | All Roles · Management Only |

#### Tab: Notify
| Field | Type | Required |
|---|---|---|
| Send Notification | Toggle | ❌ | Default Off |
| Notify Channel | Multi-select | Conditional | WhatsApp · Email · In-App |
| Notify Roles | Multi-select | Conditional | Chairman · MD · CEO · President · VP · Principal · Teacher · Parent · Student |
| Remind Before | Select | ❌ | 30 days · 14 days · 7 days · 3 days · 1 day · Day of |

**Submit:** [Create Event] / [Save Changes].

---

### 5.2 Drawer: `calendar-event-detail`
- **Trigger:** Event chip click or [View] in list view
- **Width:** 480px
- **Content:**
  - Event metadata (type badge, title, date/time, recurrence indicator, all-day flag)
  - Branch scope (All Branches / specific branches)
  - Description
  - Attachments (view/download)
  - Created By + Created On
  - Modified By + Modified On
  - Upcoming occurrences (if recurring — max 5 shown)
- **Actions (role-based):** [Edit] · [Delete] · [Delete All in Series] · [Export as .ics]

---

### 5.3 Modal: `event-delete-confirm`
- **Width:** 400px
- **For single:** "Delete [Event Name] on [Date]?"
- **For recurring:** "Delete this event only · All future events · All events in series"
- **Notify attendees:** Toggle (if notification was set)
- **Buttons:** [Delete] (danger) + [Cancel]

---

## 6. Academic Year Calendar Overlay

> Visible in Month and Week views as shaded background bands.

**Auto-populated from Group Settings → Academic Year:**
- Term 1 (e.g. Apr 1 – Sep 30): Light blue background
- Term 2 (Oct 1 – Dec 31): Light green background
- Term 3 (Jan 1 – Mar 31): Light orange background (if applicable)
- Exam periods: Crosshatch pattern overlay

**Holiday markers:** Public holidays shown as gray day cells (from Group Settings default holiday list).

---

## 7. Calendar Export

**[Export Calendar ↓] button:**
- **Options modal (380px):** Format (iCal .ics / CSV) · Date Range · Event Types to include
- **iCal export:** Standard RFC 5545 format — importable into Google Calendar, Outlook
- **CSV export:** All events as spreadsheet
- **Filename:** `group_calendar_{group_id}_{start}_{end}.{ext}`

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "[Title] added to calendar" | Success | 4s |
| Event updated | "Event updated" | Success | 4s |
| Event deleted | "Event deleted" | Warning | 4s |
| Recurring series deleted | "[N] events deleted from series" | Warning | 6s |
| Conflict detected | "Date conflict with [Event Name]. Review before saving." | Warning | 6s |
| Notification sent | "Event notification sent to [N] recipients" | Info | 4s |
| Calendar exported | "Calendar export ready" | Success | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No events in month | "No events this month" | "Add events to the group calendar" | [+ Add Event] |
| No events in filter | "No events match" | "Try different event type filters" | [Clear Filters] |
| No events in list | "No upcoming events" | "Your group has no scheduled events" | [+ Add Event] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: filter bar + calendar grid |
| Month/Week/List switch | Calendar area skeleton |
| Month navigation (← →) | Inline skeleton (calendar grid only) |
| Filter toggle | Inline skeleton |
| Event create drawer | Spinner in drawer |
| Event detail drawer | Spinner in drawer |
| Calendar export | Spinner in export button |

---

## 11. Role-Based UI Visibility

| Element | Chairman/MD | CEO | President/VP | Exec Sec | Trustee/Advisor |
|---|---|---|---|---|---|
| [+ Add Event] | ✅ | ✅ | ✅ (own types) | ✅ | ❌ |
| [Edit] event | ✅ | ✅ own | ✅ own | ✅ | ❌ |
| [Delete] event | ✅ | ❌ | ❌ | ❌ | ❌ |
| [Export Calendar] | ✅ | ✅ | ✅ | ✅ | ❌ |
| Event Notes / Description | ✅ | ✅ | ✅ | ✅ | ❌ |
| [Notify] tab in create | ✅ | ✅ | ✅ | ✅ | — |
| Branch filter (all) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Compliance events | ✅ | ✅ | ✅ | ✅ | ✅ read |
| Board Meeting events | ✅ | ✅ | ✅ | ✅ | ✅ read |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/calendar/` | JWT | Events list (date range, filters) |
| POST | `/api/v1/group/{id}/calendar/` | JWT (G3+) | Create event |
| GET | `/api/v1/group/{id}/calendar/{eid}/` | JWT | Event detail |
| PUT | `/api/v1/group/{id}/calendar/{eid}/` | JWT (G3+) | Update event |
| DELETE | `/api/v1/group/{id}/calendar/{eid}/` | JWT (G4/G5) | Delete event |
| DELETE | `/api/v1/group/{id}/calendar/{eid}/series/` | JWT (G4/G5) | Delete recurring series |
| GET | `/api/v1/group/{id}/calendar/export/` | JWT | Export iCal or CSV |
| GET | `/api/v1/group/{id}/calendar/academic-year/` | JWT | Academic year overlay data |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month navigate | `click` | GET `.../calendar/?month=&year=` | `#calendar-grid` | `innerHTML` |
| Filter toggle | `click` | GET `.../calendar/?types=&branch=` | `#calendar-grid` | `innerHTML` |
| View switch | `click` | GET `.../calendar/?view=month\|week\|list` | `#calendar-area` | `innerHTML` |
| Open event | `click` | GET `.../calendar/{id}/` | `#drawer-body` | `innerHTML` |
| Create event | `click` (day cell) | GET `.../calendar/new/?date=` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
