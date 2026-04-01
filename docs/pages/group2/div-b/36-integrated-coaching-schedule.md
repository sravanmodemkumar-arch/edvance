# 36 — Integrated Coaching Schedule

> **URL:** `/group/acad/jee-neet/schedule/`
> **File:** `36-integrated-coaching-schedule.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** JEE/NEET Integration Head G3 · CAO G4 · Stream Coordinators (MPC/BiPC) G3

---

## 1. Purpose

The Integrated Coaching Schedule manages the most operationally delicate aspect of JEE/NEET preparation in a traditional school group: the overlap between regular class timetables and coaching periods. A student in Class 11 MPC preparing for JEE must attend regular CBSE/State Board classes for board exams while also attending JEE coaching periods for competitive exam preparation. These two timetables exist in the same school day and must be coordinated without putting students in two places at once.

For a group with 50 branches, each potentially running different timetables for different sections, the scheduling complexity is significant. This page provides a branch-by-branch, week-by-week visual timetable grid showing how coaching slots integrate with the regular timetable. Conflicts — where a coaching period overlaps a mandatory regular class period — are shown in red, making them immediately visible. The JEE/NEET Integration Head can then resolve conflicts by shifting the coaching slot or coordinating with the Stream Coordinator to temporarily suspend the overlapping regular period.

The weekly grid view is the primary interaction surface. It shows each school day (Monday–Saturday for most Indian institutions), each period slot, and whether that slot is occupied by regular class, coaching, or both (conflict). The colour coding — grey for regular, blue for coaching, red for conflict — provides an instant visual density map that shows how heavy the coaching load is relative to the regular curriculum in any given week.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All branches | ✅ View · Override approve | Can approve resolution decisions |
| Group Academic Director | G3 | ✅ All branches | ❌ | Read-only — monitoring |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Group Stream Coord — MPC | G3 | ✅ Branches with MPC JEE coaching | ❌ | Read-only — coordination awareness |
| Group Stream Coord — BiPC | G3 | ✅ Branches with BiPC NEET coaching | ❌ | Read-only — coordination awareness |
| Group Stream Coord — MEC/CEC | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ✅ All branches | ✅ Full — create · edit · delete slots · resolve conflicts | Primary operator |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ All branches | ❌ | Read-only — monitoring |
| Group Academic Calendar Manager | G3 | ✅ All branches | ❌ | Read-only — conflict awareness for calendar |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  JEE/NEET  ›  Integrated Coaching Schedule
```

### 3.2 Page Header
```
Integrated Coaching Schedule                        [+ Add Coaching Slot]  [Export Schedule ↓]
[Group Name] — Branch: [Branch Selector ▾] · Week: [Week Picker ◀ ▶]     JEE/NEET Head only — actions
```

### 3.3 Summary Stats Bar (for selected branch and week)

| Stat | Value |
|---|---|
| Branch | [Selected Branch Name] |
| Week | [Date Range — Mon DD MMM to Sat DD MMM YYYY] |
| Coaching Periods This Week | 14 |
| Regular Periods This Week | 36 |
| Conflicts Detected | 2 (shown in amber/red) |
| Unresolved Conflicts | 1 |
| Coaching Hours (Week) | 14 hrs |

---

## 4. Main Content — Weekly Timetable Grid

### 4.1 Grid Layout

```
           Monday     Tuesday    Wednesday  Thursday   Friday     Saturday
Period 1   [Regular]  [Coaching] [Regular]  [Regular]  [Regular]  [Regular]
Period 2   [Coaching] [Regular]  [CONFLICT] [Coaching] [Regular]  [Regular]
Period 3   [Regular]  [Regular]  [Regular]  [Regular]  [Coaching] [Coaching]
Period 4   [Regular]  [Regular]  [Coaching] [Regular]  [Regular]  [Regular]
Period 5   [Coaching] [Coaching] [Regular]  [CONFLICT] [Regular]  [—Break—]
Period 6   [Regular]  [Regular]  [Regular]  [Coaching] [Regular]  [—Break—]
Period 7   [Coaching] [Regular]  [Regular]  [Regular]  [Coaching] [Regular]
Period 8   [Regular]  [Regular]  [Regular]  [Regular]  [Regular]  [Regular]
```

**Cell colours:**
- Light grey (`bg-gray-100`): Regular class period — subject and teacher shown
- Blue (`bg-blue-100 border-blue-400`): Coaching period — subject and coaching faculty shown
- Red (`bg-red-200 border-red-600 font-bold`): Conflict — coaching overlapping mandatory regular period

**Cell content (compact):**
- Regular: Subject abbreviation · Teacher initials
- Coaching: "JEE/Phy" or "NEET/Bio" · Faculty name
- Conflict: "CONFLICT" in bold red + both clashing entries below

**Cell tooltip (on hover):** Full details — Period time · Subject · Faculty · Type (Regular / Coaching) · For conflicts: "Coaching overlaps [Regular Subject] — resolve required"

**Cell click (Coaching or Conflict cells):** Opens `slot-detail` drawer or `conflict-resolve` drawer depending on cell type.

### 4.2 Branch Selector

Dropdown at top: Search branch by name. Single selection — one branch shown at a time.

**Why single branch:** The timetable grid is inherently branch-specific as each branch manages its own period schedule. A multi-branch view would require a fundamentally different UI (table of conflicts across branches — see Section 4.5 below).

### 4.3 Week Navigation

Week picker with Previous (◀) and Next (▶) arrows. Calendar dropdown for date jump. "This Week" quick-link button.

Weeks shown in standard Indian academic year format: April week 1 through March week last.

### 4.4 View Toggle (above grid)

| Toggle Option | Shows |
|---|---|
| Weekly Grid (default) | 6-day × 8-period grid for selected branch and week |
| List View | All coaching slots as a sortable table |
| Conflicts Only | Filtered view showing only conflict cells across all weeks for selected branch |

### 4.5 Cross-Branch Conflict Summary (below grid)

A separate read-only table for the JEE/NEET Head showing all conflicts across all branches:

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Day & Period | Text | ✅ |
| Coaching Subject | Badge | ✅ |
| Clashing Regular Subject | Text | ✅ |
| Date | Date | ✅ |
| Resolution Status | Badge | ✅ (Unresolved · Resolved · Ignored) |
| Actions | — | ❌ |

Default sort: Unresolved first, then by date.

### 4.6 Search / Filters for List View and Conflict Table

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Week | Date picker | |
| Subject | Multi-select | Physics · Chemistry · Maths · Biology · All coaching subjects |
| Conflict Status | Select | Unresolved · Resolved · All |
| Slot Type | Select | Coaching · Regular · Conflicts only |

---

## 5. Drawers & Modals

### 5.1 Drawer: `slot-create` — Add Coaching Slot
- **Trigger:** [+ Add Coaching Slot] header button or empty cell click in coaching column
- **Width:** 480px
- **Title:** "Add Coaching Slot"

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select / pre-filled | ✅ | Locked to currently selected branch |
| Day | Select | ✅ | Monday · Tuesday · Wednesday · Thursday · Friday · Saturday |
| Period | Select | ✅ | Period 1 through Period 8 (or branch-specific period count) |
| Start Time | Time | Auto | Populated from branch period timetable |
| End Time | Time | Auto | Populated from branch period timetable |
| Coaching Type | Select | ✅ | JEE Main · JEE Advanced · NEET-UG |
| Subject | Select | ✅ | Physics · Chemistry · Maths (JEE) · Biology (NEET) |
| Faculty | Search + Select | ✅ | Search from coaching faculty assigned to this branch |
| Stream | Auto | Auto | JEE → MPC class · NEET → BiPC class |
| Class | Select | ✅ | Class 11 · Class 12 |
| Applies From (Week) | Date | ✅ | Week start date |
| Applies Until (Week) | Date | ✅ | Week end date — allows recurring slot definition |
| Repeat Weekly | Toggle | ❌ | If on, slot repeats every week in the date range |

**Conflict detection:** On day/period selection, backend checks if that slot has a regular class. If yes:
- Yellow warning inline: "This period has a regular [Subject] class with [Teacher]. Saving will create a conflict."
- User can still save — conflict is flagged in grid.

**Submit:** [Add Slot] — creates slot for the defined week range.

---

### 5.2 Drawer: `slot-detail` — View/Edit Coaching Slot
- **Trigger:** Click on a blue coaching cell in the grid
- **Width:** 480px
- **Tabs:** Details · Edit

#### Tab: Details
All slot fields read-only + created by, created at, last modified.

#### Tab: Edit
Same form as slot-create, pre-filled. Available to JEE/NEET Head and CAO only.

**Delete slot:** [Remove Slot] button at bottom — danger style — confirm modal required.

---

### 5.3 Drawer: `conflict-resolve`
- **Trigger:** Click on a red conflict cell in the grid, or "Resolve" action in cross-branch conflict table
- **Width:** 480px
- **Title:** "Resolve Conflict — [Branch] — [Day] Period [N]"
- **Content:**
  - Conflict summary: "Coaching [Subject] overlaps Regular [Subject] on [Day] Period [N] — [Time range]"
  - Two options displayed as radio buttons:

**Option A:** Shift Coaching Slot
- Move coaching slot to: Day selector + Period selector
- Preview: New slot placement shown inline
- Conflict check: Runs immediately on selection — if new slot also conflicts, shows warning

**Option B:** Notify Faculty
- "Keep conflict as-is and notify coaching faculty to coordinate"
- Note recipient: Faculty name (auto-populated)
- Message field (pre-filled, editable): "Dear [Faculty], the coaching slot for [Subject] on [Day] conflicts with [Regular Subject] class. Please coordinate with [Teacher] or shift your session."
- Channel: WhatsApp (default) · Email

**Option C:** Ignore Conflict (with reason)
- Reason text (required, min 20 chars) — e.g. "Regular class replaced by coaching for this week due to board exam prep"
- Sets conflict status to "Ignored" — shows in conflict table with reason badge

**Submit:**
- Option A: [Shift Slot] — creates new slot, removes old slot, conflict resolved
- Option B: [Send Notification] — notification sent, conflict remains but flagged as "Acknowledged"
- Option C: [Ignore with Reason] — conflict suppressed with audit entry

---

## 6. Charts

### 6.1 Coaching Hours Per Week (Bar — Weekly Overview)
- **Type:** Vertical bar chart
- **X-axis:** Weeks in academic year (Apr–Mar)
- **Y-axis:** Total coaching hours per week for selected branch
- **Bars:** Stacked — JEE coaching hours (blue) + NEET coaching hours (green)
- **Annotation line:** "Recommended max" horizontal line at configured maximum coaching hours/week
- **Tooltip:** Week dates · JEE hrs · NEET hrs · Total · vs recommended
- **Export:** PNG
- **Shown:** In collapsible "Coaching Load" card below timetable grid

### 6.2 Conflict Count Over Time (Bar — Trend)
- **Type:** Vertical bar chart
- **X-axis:** Last 12 weeks (rolling)
- **Y-axis:** Count of conflicts
- **Bars:** Stacked — Unresolved (red) + Resolved (green) + Ignored (grey)
- **Tooltip:** Week · Total conflicts · Unresolved
- **Export:** PNG
- **Shown:** Below cross-branch conflict table

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Coaching slot created | "Coaching slot added for [Subject] — [Day] Period [N] — [Branch]." | Success | 4s |
| Slot created with conflict | "Coaching slot added. Conflict detected with [Regular Subject] — please resolve." | Warning | 6s |
| Slot edited | "Coaching slot updated." | Success | 4s |
| Slot deleted | "Coaching slot removed." | Warning | 4s |
| Conflict resolved — shifted | "Coaching slot shifted to [Day] Period [N]. Conflict resolved." | Success | 5s |
| Conflict notification sent | "Notification sent to [Faculty Name] regarding scheduling conflict." | Success | 4s |
| Conflict ignored | "Conflict marked as Ignored. Reason recorded." | Info | 4s |
| No coaching faculty assigned | "No coaching faculty assigned to this branch for [Subject]. Assign faculty first." | Error | Manual |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branch selected | "Select a Branch" | "Choose a branch to view its integrated coaching schedule" | [Select Branch ▾] |
| No coaching slots this week | "No Coaching Slots This Week" | "No JEE/NEET coaching slots are scheduled for this branch this week" | [+ Add Coaching Slot] |
| No conflicts | "No Conflicts Detected" | "All coaching slots are clear of regular class conflicts for this branch" | — |
| Cross-branch — no conflicts | "No Conflicts Across Branches" | "No scheduling conflicts detected across any branch this week" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + empty grid (row/column outlines) |
| Branch selector change | Full grid skeleton reload |
| Week navigation | Grid shimmer overlay while reloading |
| Slot-create/edit drawer open | Spinner in drawer body |
| Conflict-resolve drawer open | Spinner in drawer body |
| Conflict check on slot creation | Inline spinner next to day/period selectors |
| Cross-branch conflict table load | Skeleton table rows (10) |
| Chart load | Spinner centred in chart card |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | JEE/NEET Head G3 | CAO G4 | Stream Coords (MPC/BiPC) G3 | MIS G1 | Academic Dir G3 |
|---|---|---|---|---|---|
| [+ Add Coaching Slot] | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit Slot (in drawer) | ✅ | ✅ | ❌ | ❌ | ❌ |
| Delete Slot | ✅ | ✅ | ❌ | ❌ | ❌ |
| Conflict Resolve drawer | ✅ | ✅ | ❌ | ❌ | ❌ |
| Branch selector | All branches | All branches | Own stream branches | All branches | All branches |
| Cross-branch conflict table | ✅ | ✅ | ✅ (own stream) | ✅ | ✅ |
| Export Schedule | ✅ | ✅ | ❌ | ✅ | ❌ |
| Coaching Load chart | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/jee-neet/schedule/` | JWT | Weekly timetable grid data |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/schedule/stats/` | JWT | Summary stats bar for selected branch+week |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/schedule/slots/` | JWT (JEE/NEET Head) | Create coaching slot |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/schedule/slots/{slot_id}/` | JWT | Slot detail drawer data |
| PUT | `/api/v1/group/{group_id}/acad/jee-neet/schedule/slots/{slot_id}/` | JWT (JEE/NEET Head / CAO) | Update slot |
| DELETE | `/api/v1/group/{group_id}/acad/jee-neet/schedule/slots/{slot_id}/` | JWT (JEE/NEET Head / CAO) | Remove slot |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/schedule/conflicts/` | JWT | Cross-branch conflict list |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/schedule/conflicts/{conflict_id}/` | JWT | Conflict resolve drawer data |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/schedule/conflicts/{conflict_id}/resolve/` | JWT (JEE/NEET Head / CAO) | Resolve conflict (shift/notify/ignore) |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/schedule/check-conflict/` | JWT | Real-time conflict check for slot creation (query params: branch_id, day, period, week) |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/schedule/export/?format=xlsx` | JWT | Export schedule XLSX |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/schedule/charts/coaching-hours/` | JWT | Coaching hours per week chart |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/schedule/charts/conflict-trend/` | JWT | Conflict count trend chart |

Query params for grid endpoint: `branch_id`, `week_start` (ISO date of Monday).

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Branch selector change | `change` | GET `.../schedule/?branch_id=&week_start=` | `#schedule-page-body` | `innerHTML` |
| Week prev/next navigation | `click` | GET `.../schedule/?branch_id=&week_start=` | `#schedule-page-body` | `innerHTML` |
| Add slot drawer open | `click` | GET `.../schedule/slots/create-form/?branch_id=&day=&period=` | `#drawer-body` | `innerHTML` |
| Slot detail drawer open | `click` | GET `.../schedule/slots/{id}/` | `#drawer-body` | `innerHTML` |
| Conflict resolve drawer open | `click` | GET `.../schedule/conflicts/{id}/` | `#drawer-body` | `innerHTML` |
| Conflict check on day/period select | `change` | GET `.../schedule/check-conflict/?branch_id=&day=&period=&week=` | `#conflict-check-result` | `innerHTML` |
| Resolve submit | `click` | POST `.../schedule/conflicts/{id}/resolve/` | `#schedule-grid` | `innerHTML` |
| View toggle (grid/list/conflicts) | `click` | GET `.../schedule/?view=grid` or `?view=list` or `?view=conflicts` | `#schedule-main-content` | `innerHTML` |
| Cross-branch conflict filter | `click` | GET `.../schedule/conflicts/?filters=` | `#cross-branch-conflict-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
