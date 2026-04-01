# 60 — Fee Due Calendar

- **URL:** `/group/finance/fee-structure/due-calendar/`
- **Template:** `portal_base.html`
- **Priority:** P2
- **Role:** Fee Structure Manager G3 (primary) · Fee Collection Head G3

---

## 1. Purpose

The Fee Due Calendar is a group-wide calendar of all fee instalment due dates configured in fee templates across all branches. It gives the Fee Structure Manager and Fee Collection Head a visual view of when fee collections are expected — enabling collection drive planning (Page 33), defaulter outreach timing, and cash flow forecasting.

The calendar integrates with fee templates (Page 22), showing each instalment's due date per student category (Day Scholar, Hosteler, Coaching). It also tracks whether automated reminders have been dispatched for each due date.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Structure Manager | G3 | Full read + edit instalment dates |
| Group Fee Collection Head | G3 | Read |
| Group CFO | G1 | Read |
| Group Finance Manager | G1 | Read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Structure → Fee Due Calendar
```

### 3.2 Page Header
- **Title:** `Fee Due Calendar`
- **Subtitle:** `AY [Year] · [N] Instalment Events · [X] Branches`
- **Right-side controls:** `[AY ▾]` `[Branch ▾]` `[Category ▾]` `[View: Calendar / List ▾]` `[Export ↓]`

---

## 4. Calendar View

**Month navigator:** `[< Prev]` Month Year `[Next >]`

**Calendar Grid:** Standard month view (Mon–Sun)

**Event tile format:**
```
[Branch] — [Category] Instalment [N]
₹[Amount] due
[Reminder: Sent ✅ / Pending ⏳]
```

**Colour coding:**
| Colour | Meaning |
|---|---|
| Blue | Upcoming (> 7 days) |
| Amber | Due within 7 days |
| Green | Due date passed — collection data available |
| Red | Due date passed — low collection rate (< 60%) |

Clicking an event tile opens the fee event detail drawer.

---

## 5. List View (alternate)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Due Date | Date | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Category | Badge: Day Scholar · Hosteler · Coaching · Special Needs | ✅ | ✅ |
| Instalment | Text (1st · 2nd · 3rd) | ✅ | ✅ |
| Amount Due | ₹ | ✅ | — |
| Students Eligible | Count | ✅ | — |
| Total Expected | ₹ | ✅ | — |
| Reminder Status | Badge: Sent · Not Sent · Scheduled | ✅ | ✅ |
| Days Until Due | Number | ✅ | — |
| Actions | View · Edit Date · Send Reminder | — | — |

### 5.1 Filters
- Branch · Category · Month · Reminder status

### 5.2 Pagination
- 30 rows/page · Sort: Due Date asc

---

## 6. Drawers

### 6.1 Drawer: `fee-event-detail` — Fee Due Event Detail
- **Width:** 720px

**Event Summary:**
- Branch · Category · Instalment No · Due Date
- Students Eligible · Total Expected (₹)
- From Fee Template: [Template Name] (link to Page 22)

**Collection Snapshot (if due date passed):**
| Metric | Value |
|---|---|
| Total Expected | ₹ |
| Total Collected | ₹ |
| Collection Rate | % |
| Outstanding | ₹ |
| Defaulters | Count |

**[View Defaulters for this Due Date]** — links to Page 29 with filter applied

**Reminder Status:**
- Auto-reminder sent on [Date] via SMS/WhatsApp to [N] parents
- Next reminder: [Date] (if not yet collected)

**[Send Manual Reminder Now]**

### 6.2 Drawer: `edit-due-date` — Edit Instalment Due Date
| Field | Type | Required |
|---|---|---|
| New Due Date | Date | ✅ |
| Reason for Change | Select: Academic Calendar Change · Holiday · Board Decision | ✅ |
| Notes | Textarea | ❌ |
| Notify Parents | Toggle (default ON) | — |

- Changes reflect in the fee template's payment schedule
- [Cancel] [Save Change]

### 6.3 Drawer: `bulk-reminder` — Send Bulk Reminders
- **Trigger:** [Send Reminder] on event tile
- **Width:** 600px

| Field | Type | Required |
|---|---|---|
| Target | Select: All defaulters · All eligible students · Custom filter | ✅ |
| Channel | Checkboxes: SMS · WhatsApp · Push Notification | ✅ |
| Message | Textarea (pre-filled with instalment details) | ✅ |
| Schedule | Radio: Send Now · Schedule for [Date/Time] | ✅ |

- [Preview Message] [Send]

---

## 7. Charts

### 7.1 Monthly Fee Due Calendar — Instalment Volume (Bar)
- **Y-axis:** Number of instalment events per month
- **Colour:** By category

### 7.2 Expected Collection by Month (Bar — Line overlay = Actual)
- Planning view for the year

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Due date updated | "Instalment due date updated for [Branch] — [Category]. Parents notified." | Success | 4s |
| Reminder sent | "Reminders sent to [N] parents for [Branch] [Instalment]." | Success | 4s |
| Export | "Fee due calendar exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No events | "No fee events" | "No instalment due dates configured for the selected period." |
| No templates | "Fee templates not found" | "Configure fee templates to populate the due calendar." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton calendar |
| Month switch | Calendar skeleton |
| Drawer | Spinner |

---

## 11. Role-Based UI Visibility

| Element | Fee Structure Mgr G3 | Fee Collection Head G3 | CFO G1 |
|---|---|---|---|
| [Edit Due Date] | ✅ | ❌ | ❌ |
| [Send Reminder] | ✅ | ✅ | ❌ |
| View all events | ✅ | ✅ | ✅ |
| Collection data | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/fee-structure/due-calendar/` | JWT (G1+) | Calendar events |
| GET | `/api/v1/group/{id}/finance/fee-structure/due-calendar/?month=YYYY-MM` | JWT (G1+) | Filter by month |
| PUT | `/api/v1/group/{id}/finance/fee-structure/due-calendar/{eid}/` | JWT (G3) | Update due date |
| POST | `/api/v1/group/{id}/finance/fee-structure/due-calendar/{eid}/remind/` | JWT (G3) | Send reminders |
| GET | `/api/v1/group/{id}/finance/fee-structure/due-calendar/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month navigation | `click` | GET `.../due-calendar/?month=YYYY-MM` | `#calendar-grid` | `innerHTML` |
| Event tile click | `click` | GET `.../due-calendar/{id}/` | `#drawer-body` | `innerHTML` |
| View toggle | `click` | GET `.../due-calendar/?view=list` | `#calendar-container` | `innerHTML` |
| Edit due date | `click` | GET `.../due-calendar/{id}/edit-form/` | `#drawer-body` | `innerHTML` |
| Save edit | `submit` | PUT `.../due-calendar/{id}/` | `#event-tile-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
