# 60 — PTM Schedule Manager

> **URL:** `/group/acad/ptm/`
> **File:** `60-ptm-schedule-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Calendar Manager G3 · CAO G4 · Academic Director G3 · Branch staff (report attendance via branch portal)

---

## 1. Purpose

The PTM (Parent-Teacher Meeting) Schedule Manager ensures that every branch in the group conducts Parent-Teacher Meetings on schedule, that parents are notified in advance, and that attendance and outcomes are recorded for each PTM. In CBSE-affiliated schools, holding at least two PTMs per year (one per term) is a compliance requirement, and for groups aspiring to NAAC or NCPCR standards, PTM documentation is an inspectable record.

Without a central scheduling tool, PTMs at different branches happen on different dates, parent notifications are sent ad hoc by branch staff, and no group-level officer knows whether all branches have held their PTMs until a manual survey is conducted. This page eliminates that ambiguity by allowing the Calendar Manager to schedule PTMs for all branches simultaneously (respecting each branch's local working calendar), triggering automated parent notifications, and tracking whether each PTM has been held and whether a report has been submitted.

The automated reminder system sends WhatsApp and SMS notifications to registered parents 7 days before the PTM and again on the morning of the PTM — using the notification templates configured by the Calendar Manager. After the PTM, the branch principal or designated staff member submits an attendance count and a feedback summary through the branch portal; this data appears in the PTM report drawer on this page.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ❌ No create | Oversight view |
| Group Academic Director | G3 | ✅ Full | ❌ No create | Advisory view |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ❌ | ❌ | No access |
| Group Academic Calendar Manager | G3 | ✅ Full | ✅ Full CRUD | Primary owner |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Academic Calendar Management  ›  PTM Schedule Manager
```

### 3.2 Page Header
```
PTM Schedule Manager                                  [+ Schedule PTM]  [Schedule All Branches ↓]
Parent-Teacher Meetings — all branches                               (Calendar Manager only)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total PTMs Scheduled (This Year) | Count |
| Upcoming PTMs (Next 30 Days) | Count |
| PTMs Held (This Year) | Count |
| PTMs with Report Submitted | Count |
| Branches Missing PTM This Term | Count — red |
| Parent Notification Delivery Rate | % |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Branch name
- 300ms debounce

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| PTM Type | Multi-select | Term 1 / Term 2 / Annual / Emergency |
| Month | Month picker | |
| Notification Status | Select | Sent / Not sent |
| Report Submitted | Select | Yes / No |
| Status | Select | Scheduled / Completed / Cancelled / Missed |

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Calendar Manager |
| Branch | Text | ✅ | |
| PTM Type | Badge | ✅ | Term 1 / Term 2 / Annual / Emergency |
| Scheduled Date | Date | ✅ | |
| Time | Text | ✅ | e.g. "10:00 AM – 1:00 PM" |
| Status | Badge | ✅ | Scheduled (blue) / Completed (green) / Cancelled (red) / Missed (red) |
| Parent Notification | Badge | ✅ | Sent / Not sent / Failed |
| Attendance % | Number | ✅ | Submitted by branch after PTM; "—" if not yet |
| Report | Badge | ✅ | Submitted / Pending / Not applicable |
| Actions | — | ❌ | Role-based |

**Default sort:** Scheduled Date ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

### 4.4 Row Actions

| Action | Visible To | Drawer | Notes |
|---|---|---|---|
| View / View Report | Calendar Mgr, CAO, Acad Dir | `ptm-report` drawer 480px | PTM details + attendance + feedback |
| Edit | Calendar Manager | `ptm-create` drawer (pre-filled) | Before PTM date only |
| Send Reminder | Calendar Manager | Inline confirm | Manual re-send parent notification |
| Mark Completed | Calendar Manager | Inline confirm | After PTM date; marks as completed |
| Mark Missed | Calendar Manager | Confirm modal | Marks as missed; reason required |
| Cancel | Calendar Manager | Confirm modal | Reason required; notify branches |

### 4.5 Bulk Actions (Calendar Manager)

| Action | Notes |
|---|---|
| Send Notification to Selected | Bulk parent notification for selected PTMs |
| Export PTM Schedule (XLSX) | Selected or all PTMs |
| Schedule PTM for All Branches | Opens `ptm-create` bulk-schedule flow |

---

## 5. Drawers & Modals

### 5.1 Drawer: `ptm-create` — Schedule PTM
- **Trigger:** [+ Schedule PTM] button or Edit action
- **Width:** 480px

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch(es) | Multi-select | ✅ | Single or multiple branches |
| PTM Type | Select | ✅ | Term 1 / Term 2 / Annual / Emergency |
| Academic Year | Select | ✅ | |
| Date | Date | ✅ | Must be a working day per branch calendar |
| Start Time | Time | ✅ | |
| End Time | Time | ✅ | |
| Agenda | Textarea | ✅ | Max 500 chars; will be included in parent notification |
| Parent notification | Toggle | ✅ | Default on |
| Notification channel | Select | Conditional | Email / WhatsApp / SMS / All — required if notify on |
| Notification template | Select | Conditional | Pre-set templates from group notifications config |
| Reminder: 7 days before | Toggle | ✅ | Default on |
| Reminder: Day of PTM | Toggle | ✅ | Default on |

- **Submit:** "Schedule PTM"
- **On success:** PTM rows appear for each branch · Notifications queued if toggle on · Events added to Group Academic Calendar (page 59)

### 5.2 Drawer: `ptm-report`
- **Trigger:** View / View Report row action
- **Width:** 480px
- **Sections:**

**Section 1 — PTM Details** (read-only)
Branch · PTM Type · Date · Time · Agenda · Status

**Section 2 — Parent Notification**
Sent at · Channel · Delivery stats: Sent N · Delivered N · Failed N

**Section 3 — Attendance & Feedback** (filled by branch via branch portal)
| Field | Notes |
|---|---|
| Total parents expected | Auto: enrolled student count × 1 |
| Parents attended | Submitted by branch |
| Attendance % | Computed |
| Key issues raised | Text submitted by branch — max 1000 chars |
| Branch principal feedback | Text — max 500 chars |
| Action items from PTM | Repeater — item, owner, due date |

**Footer:** [Download PTM Report PDF] button — formatted single-PTM report

### 5.3 Modal: `cancel-ptm-confirm`
- **Width:** 420px
- **Content:** "Cancel PTM for [Branch] on [Date]?"
- **Fields:** Reason (required, min 20 chars) · Notify parents (checkbox, default on)
- **Buttons:** [Confirm Cancel] (danger) · [Cancel]

### 5.4 Modal: `mark-missed-confirm`
- **Width:** 420px
- **Content:** "Mark PTM as missed for [Branch] on [Date]?"
- **Fields:** Reason (optional) · Follow-up action (optional)
- **Buttons:** [Mark as Missed] · [Cancel]

---

## 6. Charts

### 6.1 PTM Completion Rate by Branch (Horizontal Bar)
- **Type:** Horizontal bar
- **Data:** % of scheduled PTMs completed per branch this academic year
- **Colour:** Green ≥ 100% · Amber 50–99% · Red < 50%
- **Tooltip:** Branch · Completed: N / Scheduled: N · %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| PTM scheduled | "PTM scheduled for [Branch] on [Date]" | Success | 4s |
| Bulk scheduled | "PTMs scheduled for [N] branches" | Success | 4s |
| PTM updated | "PTM updated" | Success | 4s |
| PTM cancelled | "PTM cancelled. Parents notified." | Warning | 6s |
| PTM marked missed | "PTM marked as missed for [Branch]" | Warning | 6s |
| Reminder sent | "Parent reminder sent for [Branch] PTM on [Date]" | Success | 4s |
| Bulk notification sent | "Notifications sent for [N] PTMs" | Success | 4s |
| Export started | "Export preparing…" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No PTMs scheduled | "No PTMs scheduled" | "Schedule the first Parent-Teacher Meeting for all branches" | [Schedule All Branches] |
| No upcoming PTMs | "No upcoming PTMs in the next 30 days" | "All scheduled PTMs for this period have been completed or are further out" | — |
| No results match filters | "No PTMs match" | "Clear filters to see all PTMs" | [Clear Filters] |
| Report drawer — no data | "No report submitted" | "The branch has not yet submitted PTM attendance and feedback" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) |
| Table filter/search | Inline skeleton rows |
| PTM create drawer | Spinner |
| Report drawer | Spinner → sections render |
| Bulk schedule | Full-page overlay "Scheduling PTMs…" |
| Notification send | Spinner in confirm button |

---

## 10. Role-Based UI Visibility

| Element | Calendar Mgr G3 | CAO G4 | Academic Dir G3 |
|---|---|---|---|
| [+ Schedule PTM] | ✅ | ❌ | ❌ |
| [Schedule All Branches] | ✅ | ❌ | ❌ |
| Edit action | ✅ | ❌ | ❌ |
| Send Reminder | ✅ | ❌ | ❌ |
| Mark Completed / Missed / Cancel | ✅ | ❌ | ❌ |
| View / View Report | ✅ | ✅ | ✅ |
| Bulk actions | ✅ | ❌ | ❌ |
| Export | ✅ | ✅ | ✅ |
| Charts | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/ptm/` | JWT | List PTMs |
| GET | `/api/v1/group/{group_id}/acad/ptm/stats/` | JWT | Stats bar |
| POST | `/api/v1/group/{group_id}/acad/ptm/` | JWT (G3 Cal Mgr) | Schedule PTM(s) |
| PUT | `/api/v1/group/{group_id}/acad/ptm/{id}/` | JWT (G3 Cal Mgr) | Update PTM |
| PATCH | `/api/v1/group/{group_id}/acad/ptm/{id}/status/` | JWT (G3 Cal Mgr) | Mark completed/missed/cancelled |
| POST | `/api/v1/group/{group_id}/acad/ptm/{id}/notify/` | JWT (G3 Cal Mgr) | Send/resend notification |
| POST | `/api/v1/group/{group_id}/acad/ptm/bulk-notify/` | JWT (G3 Cal Mgr) | Bulk notification |
| GET | `/api/v1/group/{group_id}/acad/ptm/{id}/report/` | JWT | PTM report + attendance |
| GET | `/api/v1/group/{group_id}/acad/ptm/{id}/report/download-pdf/` | JWT | PTM report PDF |
| GET | `/api/v1/group/{group_id}/acad/ptm/export/?format=xlsx` | JWT | Export |
| GET | `/api/v1/group/{group_id}/acad/ptm/charts/completion-by-branch/` | JWT | Bar chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../ptm/?q=` | `#ptm-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../ptm/?filters=` | `#ptm-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../ptm/?sort=&dir=` | `#ptm-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../ptm/?page=` | `#ptm-table-section` | `innerHTML` |
| Schedule drawer | `click` | GET `.../ptm/create-form/` | `#drawer-body` | `innerHTML` |
| Schedule submit | `submit` | POST `.../ptm/` | `#drawer-body` | `innerHTML` |
| Report drawer | `click` | GET `.../ptm/{id}/report/` | `#drawer-body` | `innerHTML` |
| Mark status | `click` | PATCH `.../ptm/{id}/status/` | `#ptm-row-{id}` | `outerHTML` |
| Send reminder | `click` | POST `.../ptm/{id}/notify/` | `#toast-container` | `beforeend` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
