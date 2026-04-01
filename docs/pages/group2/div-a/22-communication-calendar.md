# 22 — Communication Calendar

> **URL:** `/group/gov/comm-calendar/`
> **File:** `22-communication-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Exec Secretary G3 (full) · Chairman G5 · MD G5 · CEO G4 · President G4 · VP G4 (view)

---

## 1. Purpose

Calendar view of all planned and sent communications — circulars, announcements, exam
notifications, fee reminders, and board meeting notices. Prevents communication overload
(two major communications on the same day to parents) and ensures the group's communication
schedule is visible to all relevant leadership.

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| Exec Secretary | Full — create, edit, delete, reschedule | |
| Chairman/MD/CEO | View only | |
| President/VP | View only | |
| Trustee/Advisor | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Communication Calendar
```

### 3.2 Page Header
```
Communication Calendar                                 [+ Schedule Communication]  [Export ↓]
[Month/Year]                                           (Exec Secretary only)
```

### 3.3 View Toggle
- Month (default) · Week · List

### 3.4 Filter Bar (above calendar)
| Filter | Type | Options |
|---|---|---|
| Type | Checkbox group | Circular · Announcement · Exam Notice · Fee Reminder · Board Meeting · Emergency |
| Channel | Checkbox group | WhatsApp · SMS · Email · In-app |
| Branch | Multi-select | All branches (shows communications targeting specific branches) |

---

## 4. Calendar Views

### 4.1 Month View

**Grid:** Standard month grid — 7 columns (Mon–Sun) × 5–6 rows.

**Event chips:** Colour-coded by type, displayed within date cells.
- Circular: Blue
- Announcement: Green
- Exam Notification: Orange
- Fee Reminder: Yellow
- Board Meeting: Purple
- Emergency Alert: Red

**Event chip content:** Type icon + truncated title (max 25 chars).

**Max events per cell:** 3 visible + "+N more" link if >3. Click "+N more" → expands to list.

**Hover tooltip:** Full title · Type · Target · Channel · Time.

**Click event chip:** Opens `event-detail` drawer.

**Click empty date cell:** Opens `calendar-event-create` drawer pre-filled with that date (Exec Secretary only).

**Navigation:** Previous month ← · Current month · Next month → · Today button.

### 4.2 Week View

**Grid:** 7-column week grid with time slots (6am–10pm, 30min rows).

**Events:** Full-height block in their time slot, with colour and title.

**Same click interactions as month view.**

### 4.3 List View

**Display:** Grouped by date (ascending from today).

**Columns per event:** Date · Time · Type badge · Title · Target · Channel icons · Status · Actions.

**Search in list view:** Title search. Debounce 300ms.

**Pagination (list view):** 50 events per page.

---

## 5. Event Creation & Editing

### 5.1 Drawer: `calendar-event-create`
- **Trigger:** [+ Schedule Communication] or click empty date cell
- **Width:** 520px
- **Tabs:** Details · Branches · Recurrence · Notify

#### Tab: Details
| Field | Type | Required | Validation |
|---|---|---|---|
| Title | Text | ✅ | Max 100 chars |
| Type | Select | ✅ | Circular · Announcement · Exam Notice · Fee Reminder · Board Meeting · Emergency |
| Date | Date | ✅ | |
| Time | Time | ❌ | |
| Description | Textarea | ❌ | Max 300 chars |
| Linked Item | Select/search | ❌ | Link to a circular or announcement in the system |
| All-day event? | Toggle | ❌ | Hides time picker if on |

#### Tab: Branches
| Field | Type | Required | Validation |
|---|---|---|---|
| Applies To | Radio | ✅ | All Branches · Select Branches |
| Select Branches | Multi-select | Conditional | |

#### Tab: Recurrence
| Field | Type | Required | Validation |
|---|---|---|---|
| Recurrence | Select | ✅ | None · Daily · Weekly · Monthly · Custom |
| Repeat Every | Number | Conditional | e.g. "every 2 weeks" |
| End Date | Date | Conditional | Required for recurring |
| Recurrence Preview | Read-only | — | "This event will repeat on: [list of dates]" |

#### Tab: Notify
| Field | Type | Required | Validation |
|---|---|---|---|
| Notify Who | Multi-select | ❌ | Group Chairman · MD · CEO · President · VP · Exec Secretary · Branch Principals |
| Advance Notice | Select | ❌ | Same day · 1 day before · 3 days · 7 days |
| Notification Channel | Select | ❌ | WhatsApp · In-app |

**Submit:** "Add to Calendar" — success: event appears in calendar.

### 5.2 Drawer: `event-detail` — View / Edit Event
- **Trigger:** Click any event
- **Width:** 480px
- **Content (view mode — all roles):**
  - All Details tab fields displayed read-only
  - Linked circular / announcement link (if linked)
  - "Edit" button (Exec Secretary only)
  - "Delete" button (Exec Secretary only)
- **Edit mode (Exec Secretary):** Same fields as create, pre-filled. Recurring event edit: "Edit this event only" or "Edit all future events" radio.

### 5.3 Modal: `event-delete-confirm`
- **Width:** 380px
- **For recurring:** "Delete this event only" or "Delete this and all future occurrences"
- **Buttons:** [Delete] + [Cancel]

---

## 6. Conflict Detection

**Rule:** If two events of the same type targeting the same branch/audience are scheduled within
24 hours → yellow warning badge on both event chips.

**Example:** Two fee reminder circulars to all parents within the same day → "Communication
overload warning — two reminders to parents on [date]."

**Warning shown:** When event is created/moved — inline warning in the drawer.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "Communication scheduled on [date]" | Success | 4s |
| Event updated | "Calendar event updated" | Success | 4s |
| Event deleted | "Calendar event removed" | Warning | 4s |
| Recurring event created | "Recurring event created — [N] occurrences" | Info | 4s |
| Conflict detected | "Communication conflict detected on [date]" | Warning | 6s |
| Export started | "Calendar export preparing…" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No events in month | "No communications scheduled" | "Add communications to your calendar to track the group's schedule" | [+ Schedule Communication] |
| Filter shows 0 events | "No events match your filters" | "Try removing some filters" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: calendar grid (with shimmer cells) |
| Month navigation | Grid shimmer while loading new month |
| View switch | Full grid skeleton |
| Event create submit | Spinner in drawer submit button |
| Event detail open | Spinner in drawer (momentary) |

---

## 10. Role-Based UI Visibility

| Element | Exec Secretary | Chairman/MD/CEO/Pres/VP |
|---|---|---|
| [+ Schedule Communication] | ✅ | ❌ |
| Click empty cell → create | ✅ | ❌ (click opens detail of that day, not create) |
| [Edit] in event detail | ✅ | ❌ |
| [Delete] in event detail | ✅ | ❌ |
| View events | ✅ | ✅ |
| Filter controls | ✅ | ✅ |
| [Export] | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/calendar/communications/` | JWT | All events (month/week) |
| POST | `/api/v1/group/{id}/calendar/communications/` | JWT (G3 Sec) | Create event |
| GET | `/api/v1/group/{id}/calendar/communications/{eid}/` | JWT | Event detail |
| PUT | `/api/v1/group/{id}/calendar/communications/{eid}/` | JWT (G3 Sec) | Update event |
| DELETE | `/api/v1/group/{id}/calendar/communications/{eid}/` | JWT (G3 Sec) | Delete event |
| GET | `/api/v1/group/{id}/calendar/communications/export/` | JWT | Export calendar (iCal/PDF) |

**Query params for list:** `?start=YYYY-MM-DD&end=YYYY-MM-DD&type=circular,announcement&branch=all`

---

## HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| View switch (Month · Week · List) | `click` | GET `.../comm-calendar/?view=month\|week\|list` | `#comm-calendar-area` | `innerHTML` |
| Month navigation (← →) | `click` | GET `.../comm-calendar/?month=&year=&view=month` | `#comm-calendar-area` | `innerHTML` |
| Week navigation | `click` | GET `.../comm-calendar/?week=&view=week` | `#comm-calendar-area` | `innerHTML` |
| Event type filter toggle | `click` | GET `.../comm-calendar/?types=` | `#comm-calendar-area` | `innerHTML` |
| [Today] jump | `click` | GET `.../comm-calendar/?today=1&view=month` | `#comm-calendar-area` | `innerHTML` |
| Open event create drawer | `click` (day/slot) | GET `.../comm-calendar/new/?date=&time=` | `#drawer-body` | `innerHTML` |
| Open event detail drawer | `click` (event chip) | GET `.../comm-calendar/{eid}/` | `#drawer-body` | `innerHTML` |
| List view pagination | `click` | GET `.../comm-calendar/?view=list&page=` | `#comm-list-section` | `innerHTML` |
| Conflict check (on date change) | `change` | GET `.../comm-calendar/conflict-check/?date=&type=` | `#conflict-warning` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
