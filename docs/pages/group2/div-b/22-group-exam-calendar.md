# 22 — Group Exam Calendar

> **URL:** `/group/acad/exam-calendar/`
> **File:** `22-group-exam-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** CAO G4 · Exam Controller G3 · Results Coordinator G3 · Stream Coords G3 · Academic Calendar Manager G3 · Academic MIS Officer G1

---

## 1. Purpose

The Group Exam Calendar is the master scheduling authority for all formal examinations across every branch in the group. Dates set here are binding — branches inherit exam dates and cannot override them. This includes Unit Tests, Mid-term exams, Annual exams, Olympiad dates, Mock Tests, and Integrated Coaching assessments. The calendar coordinates up to 50 branches running exams simultaneously, ensuring that no branch deviates from the group schedule.

For a group where concurrent branch exams are the norm — all 50 branches sitting the same Mid-term Physics paper on the same date — the calendar is a mission-critical operational tool. The Exam Controller creates and manages exam entries. The CAO approves and publishes them to branches. The Academic Calendar Manager monitors for conflicts with other group-level events like PTMs, annual days, or public holidays. The system detects scheduling conflicts automatically: any exam whose date/time overlaps with another exam at the same branch immediately triggers a conflict alert.

The calendar is presented in both Month/Week/List view modes. Month view gives a visual density picture; List view is best for reviewing detailed exam configurations. Every exam entry links directly to its exam paper status — whether the paper is in Draft, pending approval, or ready — so the Exam Controller can track operational readiness without switching pages.

---

## 2. Role Access

| Role | Level | Can View | Can Create | Can Edit | Can Cancel | Can Publish | Notes |
|---|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | ✅ | ✅ | Full authority |
| Group Academic Director | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | View-only |
| Group Curriculum Coordinator | G2 | ✅ All | ❌ | ❌ | ❌ | ❌ | View-only |
| Group Exam Controller | G3 | ✅ All | ✅ | ✅ | ✅ | ✅ | Operational ownership |
| Group Results Coordinator | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | View — plan result timelines |
| Stream Coord — MPC | G3 | ✅ MPC | ❌ | ❌ | ❌ | ❌ | Own stream only |
| Stream Coord — BiPC | G3 | ✅ BiPC | ❌ | ❌ | ❌ | ❌ | Own stream only |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC | ❌ | ❌ | ❌ | ❌ | Own stream only |
| JEE/NEET Integration Head | G3 | ✅ JEE/NEET | ❌ | ❌ | ❌ | ❌ | View coaching exams |
| IIT Foundation Director | G3 | ✅ Foundation | ❌ | ❌ | ❌ | ❌ | View Foundation exams |
| Olympiad & Scholarship Coord | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | View olympiad dates |
| Special Education Coordinator | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | Plan exam accommodations |
| Academic MIS Officer | G1 | ✅ All | ❌ | ❌ | ❌ | ❌ | Read-only |
| Academic Calendar Manager | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | View + coordinate — propose conflict resolutions |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Group Exam Calendar
```

### 3.2 Page Header (with action buttons — role-gated)
```
Group Exam Calendar                       [+ Schedule Exam]  [Export XLSX ↓]  [Month | Week | List]
[Group Name] · Master exam schedule                         (CAO / Exam Controller only for create)
```

Action button visibility:
- `[+ Schedule Exam]` — CAO, Exam Controller
- `[Export XLSX ↓]` — All roles with view access
- `[Month | Week | List]` toggle — All roles (view preference saved per user)

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Scheduled Exams | Count this academic year |
| Upcoming (Next 30 Days) | Count |
| Pending Approval | Count of unpublished exams |
| Live / In Progress | Count of exams happening today |
| Unresolved Conflicts | Count (red if > 0) |
| Papers Not Ready | Count of exams without an approved paper |

Stats bar refreshes on page load. "Unresolved Conflicts" links to Exam Conflict Monitor (page 26).

---

## 4. Main Calendar / Table

### 4.1 Search
- Full-text across: Exam Name, Stream, Class
- 300ms debounce · In list view: highlights match · In calendar view: filters events shown
- Scope: Current academic year by default

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Exam Type | Multi-select | Unit Test · Mid-term · Annual · Olympiad · Mock Test · Coaching Assessment · Practical |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated JEE · Integrated NEET |
| Class | Multi-select | Class 6–12 |
| Branch | Multi-select | All branches |
| Status | Multi-select | Draft · Pending Approval · Approved · Published · Completed · Cancelled |
| Date Range | Date range | From / To |
| Paper Status | Multi-select | No Paper · Draft Paper · Paper Approved · Paper Published |
| Has Conflicts | Checkbox | Show only exams with unresolved conflicts |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Calendar View (Month / Week)
- **Month view:** Events shown as colour-coded pills on date cells. Overflow: "+N more" link expands.
- **Week view:** Time-slotted grid — each exam block shows name, stream, duration.
- **Event colour coding:**
  - Unit Test: Blue
  - Mid-term: Orange
  - Annual: Red
  - Olympiad: Purple
  - Mock Test: Teal
  - Coaching Assessment: Grey
  - Practical: Green
- **Conflict indicator:** Red border on any event with an unresolved conflict.
- **Click event:** Opens `exam-schedule-view` drawer 560px.

### 4.4 List View (Table)

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | CAO, Exam Controller | Row select for bulk export |
| Exam Name | Text + link | ✅ | All | Opens exam-schedule-view drawer |
| Stream | Badge | ✅ | All | Stream name |
| Class | Text | ✅ | All | e.g. Class 12 |
| Date | Date | ✅ | All | Exam date |
| Duration | Text | ✅ | All | e.g. 3 hours |
| Branches | Number | ✅ | All | Count of branches this exam applies to |
| Status | Badge | ✅ | All | Draft · Pending Approval · Approved · Published · Completed · Cancelled |
| Paper Status | Badge | ✅ | CAO, Exam Controller | No Paper · Draft · Approved · Published |
| Conflicts | Badge | ✅ | All | Red badge if ≥ 1 unresolved conflict |
| Actions | — | ❌ | Role-based | See Row Actions |

**Default sort:** Date ascending (next exam first).

**Pagination (list view):** Server-side · Default 25/page · Selector 10/25/50/All.

### 4.5 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| View Details | Eye | All | `exam-schedule-view` drawer 560px | Full detail + branches + paper status |
| Edit | Pencil | CAO, Exam Controller | `exam-schedule-edit` drawer 680px | Edit all fields before publication |
| Publish to Branches | Broadcast | CAO, Exam Controller | `publish-confirm` modal 420px | Publishes exam to branch portals |
| Resolve Conflict | Warning | CAO, Exam Controller | Navigates to Exam Conflict Monitor filtered to this exam | |
| Cancel | X | CAO, Exam Controller | `cancel-confirm` modal 420px | Requires reason — audited |

### 4.6 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | All with view access | Exam schedule export |
| Publish Selected | CAO, Exam Controller | Batch publish approved exams |

---

## 5. Drawers & Modals

### 5.1 Drawer: `exam-schedule-create` — Schedule New Exam
- **Trigger:** [+ Schedule Exam] header button
- **Width:** 680px
- **Tabs:** Identity · Date & Time · Branch Scope · Paper Assignment · Notification

#### Tab: Identity
| Field | Type | Required | Validation |
|---|---|---|---|
| Exam Name | Text | ✅ | Min 3 chars, max 200, unique within academic year |
| Exam Type | Select | ✅ | Unit Test · Mid-term · Annual · Olympiad · Mock Test · Coaching Assessment · Practical |
| Stream | Multi-select | ✅ | At least 1 stream |
| Class | Multi-select | ✅ | At least 1 class |
| Subject | Multi-select | ✅ | Filtered by stream/class from Subject-Topic Master |
| Academic Year | Select | ✅ | Current or next academic year |
| Description | Textarea | ❌ | Max 300 chars |

#### Tab: Date & Time
| Field | Type | Required | Validation |
|---|---|---|---|
| Exam Date | Date picker | ✅ | Must be within academic year. Cannot be on a declared holiday. |
| Start Time | Time picker | ✅ | |
| Duration | Number (hours/minutes) | ✅ | Min 30 minutes |
| Reporting Time | Time picker | ❌ | When students must arrive |
| Hall Ticket Required | Toggle | ❌ | Default on for Annual/Mid-term |

System auto-checks conflict on date change: shows inline conflict warning if overlap detected.

#### Tab: Branch Scope
| Field | Type | Required | Notes |
|---|---|---|---|
| Apply to All Branches | Toggle | ✅ | On = all branches inherit this exam |
| Select Specific Branches | Multi-select | Conditional | Required if "All Branches" is off |
| Exclude Branches | Multi-select | ❌ | Exclude specific branches from an otherwise group-wide exam |

#### Tab: Paper Assignment
| Field | Type | Required | Notes |
|---|---|---|---|
| Link Exam Paper | Search + select | ❌ | Search from Exam Paper Builder (page 24) |
| Paper Status (read-only) | — | — | Shows current status of linked paper |
| Create New Paper | Button | ❌ | Opens Exam Paper Builder for this exam |

#### Tab: Notification
| Field | Type | Required | Notes |
|---|---|---|---|
| Notify Branch Principals | Toggle | ✅ | Default on — WhatsApp + email on publish |
| Notify Branch Exam Coordinators | Toggle | ❌ | Default on |
| Student Hall Ticket Notification | Toggle | ❌ | Default on — triggers hall ticket generation flow |
| Advance Notice (days) | Number | ❌ | Default 14 days before exam |

**Submit:** "Schedule Exam" — saved as Draft. Conflict check runs on submit. If conflicts detected: warning modal lists conflicts before save completes.

### 5.2 Drawer: `exam-schedule-edit` — Edit Exam
- **Width:** 680px — same tabs as `exam-schedule-create`, pre-filled
- **Restriction:** Cannot edit Date or Branch Scope after exam is Published. Must cancel and reschedule.

### 5.3 Drawer: `exam-schedule-view` — View Exam Detail
- **Trigger:** View Details row action or calendar event click
- **Width:** 560px
- **Tabs:** Overview · Branches · Paper Status · Conflicts · History

#### Tab: Overview
Displays all fields: exam name, type, stream, class, subject, date, time, duration, academic year, status.

#### Tab: Branches
Table: Branch Name · Readiness Status · Invigilator Assigned · Venue Confirmed · Hall Tickets Generated.
Links to Branch Exam Schedule (page 25) for detailed per-branch view.

#### Tab: Paper Status
Shows linked paper: title, creator, status, last modified. [Open Paper] button → navigates to Exam Paper Builder.

#### Tab: Conflicts
Lists all conflicts involving this exam: conflict ID, type, other exam affected, severity, status.
[Resolve] button per conflict → navigates to Exam Conflict Monitor.

#### Tab: History
Audit trail: timestamp · actor · action · changes made.

### 5.4 Modal: `cancel-confirm`
- **Width:** 420px
- **Content:** "Cancel '[Exam Name]' scheduled for [Date]? All branches will be notified."
- **Fields:** Cancellation reason (required, min 30 chars) · Notification channel (WhatsApp / Email / Both)
- **Buttons:** [Confirm Cancellation] (danger red) + [Keep Exam]
- **On confirm:** Status → Cancelled · All branch principals notified · Audit entry created

### 5.5 Modal: `publish-confirm`
- **Width:** 420px
- **Content:** "Publish '[Exam Name]' to [N] branches? Branches will see this exam immediately."
- **Checklist (auto-checked):** Paper assigned? · No unresolved conflicts? · Date within academic year?
- **Warning items:** Items not passing checklist show as amber warnings (can override for Publish)
- **Buttons:** [Publish to Branches] (primary) + [Cancel]

---

## 6. Charts

### 6.1 Exam Density per Month (Bar Chart)
- **Type:** Vertical bar chart
- **Data:** Count of exams per month across academic year
- **X-axis:** Month (Apr–Mar)
- **Y-axis:** Exam count
- **Colour:** Stacked by exam type
- **Tooltip:** Month · Total: N · By type breakdown
- **Export:** PNG

### 6.2 Branch Load over Calendar Year (Heatmap)
- **Type:** Calendar heatmap (GitHub-style)
- **Data:** Number of exams per branch per day
- **Colour intensity:** Low (1 exam) → High (5+ exams on same day)
- **Tooltip:** Date · Branch · Exam count · Conflict flag
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exam scheduled | "'[Exam Name]' scheduled for [Date]." | Success | 4s |
| Exam published | "'[Exam Name]' published to [N] branches." | Success | 4s |
| Exam updated | "'[Exam Name]' updated." | Success | 4s |
| Exam cancelled | "'[Exam Name]' cancelled. Branches notified." | Warning | 6s |
| Conflict detected | "Scheduling conflict detected for [Date]. Review before saving." | Warning | Manual |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No exams scheduled | "No exams on the calendar" | "Schedule the first exam to populate the group calendar." | [+ Schedule Exam] |
| No exams in view range | "No exams in this period" | "Navigate to a different month or remove date filters." | [Clear Date Filter] |
| Filter returns empty | "No exams match your filters" | "Try removing some filters." | [Clear All Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + calendar/list skeleton |
| Calendar month navigation | Spinner overlay on calendar grid |
| List filter/search/sort/page | Inline skeleton rows (10) |
| exam-schedule-create drawer open | Spinner in drawer body |
| exam-schedule-view drawer open | Spinner + skeleton tabs |
| Publish confirm | Spinner in confirm button |
| Cancel confirm | Spinner in confirm button |
| Charts load | Skeleton chart placeholders |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Exam Controller G3 | Results Coord G3 | Stream Coords G3 | Calendar Mgr G3 | MIS Officer G1 |
|---|---|---|---|---|---|---|
| [+ Schedule Exam] button | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| [Export XLSX] button | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Edit row action | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Publish row action | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Cancel row action | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Resolve Conflict action | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Paper Status column | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Conflicts column | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Branch Scope tab | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ❌ (own only) | ✅ | ✅ |
| Charts section | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/exam-calendar/` | JWT | List exams (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/exam-calendar/calendar/` | JWT | Calendar view data (events per date range) |
| POST | `/api/v1/group/{group_id}/acad/exam-calendar/` | JWT (CAO/Exam Ctrl) | Schedule new exam |
| GET | `/api/v1/group/{group_id}/acad/exam-calendar/{exam_id}/` | JWT | Exam detail |
| PUT | `/api/v1/group/{group_id}/acad/exam-calendar/{exam_id}/` | JWT (CAO/Exam Ctrl) | Update exam |
| POST | `/api/v1/group/{group_id}/acad/exam-calendar/{exam_id}/publish/` | JWT (CAO/Exam Ctrl) | Publish to branches |
| POST | `/api/v1/group/{group_id}/acad/exam-calendar/{exam_id}/cancel/` | JWT (CAO/Exam Ctrl) | Cancel exam |
| GET | `/api/v1/group/{group_id}/acad/exam-calendar/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/exam-calendar/export/` | JWT | XLSX export |
| GET | `/api/v1/group/{group_id}/acad/exam-calendar/charts/density/` | JWT | Monthly density bar chart data |
| GET | `/api/v1/group/{group_id}/acad/exam-calendar/charts/branch-load/` | JWT | Branch load heatmap data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Exam search (list view) | `input delay:300ms` | GET `.../exam-calendar/?q=` | `#exam-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../exam-calendar/?filters=` | `#exam-table-section` | `innerHTML` |
| Sort column (list) | `click` | GET `.../exam-calendar/?sort=&dir=` | `#exam-table-section` | `innerHTML` |
| Pagination (list) | `click` | GET `.../exam-calendar/?page=` | `#exam-table-section` | `innerHTML` |
| Calendar month navigate | `click` | GET `.../exam-calendar/calendar/?month=` | `#calendar-grid` | `innerHTML` |
| Event click (calendar) | `click` | GET `.../exam-calendar/{id}/` | `#drawer-body` | `innerHTML` |
| View detail drawer | `click` | GET `.../exam-calendar/{id}/` | `#drawer-body` | `innerHTML` |
| Create drawer open | `click` | GET `.../exam-calendar/create-form/` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../exam-calendar/` | `#drawer-body` | `innerHTML` |
| Publish confirm | `click` | POST `.../exam-calendar/{id}/publish/` | `#exam-row-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../exam-calendar/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
