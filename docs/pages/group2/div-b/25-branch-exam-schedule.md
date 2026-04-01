# 25 — Branch Exam Schedule

> **URL:** `/group/acad/branch-exam-schedule/`
> **File:** `25-branch-exam-schedule.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Exam Controller G3 · Results Coordinator G3 · Academic Calendar Manager G3

---

## 1. Purpose

The Branch Exam Schedule page gives the group academic team a per-branch operational view of every scheduled exam — showing exactly how prepared each branch is to run each exam it has been assigned. While the Group Exam Calendar (page 22) is the authoritative scheduling authority, this page answers the operational question: for each exam, which branches have confirmed their venue, assigned invigilators, and generated hall tickets — and which have not?

For a group with 50 branches each running the same set of group exams, the Exam Controller must know — at a glance — which branches are ready and which are at risk. This page makes that visible. Branches confirm their readiness through the branch portal; those confirmations are aggregated here. The "At Risk" status is automatically applied to any branch that has not confirmed readiness within 24 hours of the exam. An automated WhatsApp and email alert fires to that branch's principal 48 hours before exam time for any branch still in Pending status.

The Exam Controller or CAO can send manual reminders per branch, view detailed setup information in the branch-exam-detail drawer, or mark a branch's readiness status as overridden (e.g. if the branch confirmed verbally and the portal confirmation is delayed). All overrides are audited.

---

## 2. Role Access

| Role | Level | Can View | Can Send Reminders | Can Override Status | Notes |
|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All branches | ✅ | ✅ | Full override authority |
| Group Academic Director | G3 | ✅ All branches | ❌ | ❌ | View-only |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ All branches | ✅ | ✅ | Operational ownership |
| Group Results Coordinator | G3 | ✅ All branches | ❌ | ❌ | View for result planning |
| Stream Coord — MPC | G3 | ✅ MPC exams only | ❌ | ❌ | View own stream exam branches |
| Stream Coord — BiPC | G3 | ✅ BiPC exams only | ❌ | ❌ | View own stream exam branches |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC exams only | ❌ | ❌ | View own stream exam branches |
| JEE/NEET Integration Head | G3 | ✅ JEE/NEET exams | ❌ | ❌ | View coaching exam branches |
| IIT Foundation Director | G3 | ✅ Foundation exams | ❌ | ❌ | View Foundation branches |
| Olympiad & Scholarship Coord | G3 | ❌ | ❌ | ❌ | No access |
| Special Education Coordinator | G3 | ✅ All branches | ❌ | ❌ | View to check exam accommodations |
| Academic MIS Officer | G1 | ❌ | ❌ | ❌ | No access |
| Academic Calendar Manager | G3 | ✅ All branches | ❌ | ❌ | View for scheduling coordination |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Branch Exam Schedule
```

### 3.2 Page Header (with action buttons — role-gated)
```
Branch Exam Schedule                      [Send Bulk Reminder]  [Export XLSX ↓]
[Group Name] · Per-branch exam readiness monitor          (CAO / Exam Controller only for reminders)
```

Action button visibility:
- `[Send Bulk Reminder]` — CAO, Exam Controller (sends reminder to all Pending branches for selected exam)
- `[Export XLSX ↓]` — CAO, Exam Controller, Results Coordinator, Calendar Manager

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Upcoming Exams (Next 7 Days) | Count of exam-branch combinations |
| Confirmed | Count of branch-exam combinations with Confirmed status |
| Pending | Count with Pending status |
| At Risk | Count with At Risk status (< 24h before exam, still Pending) |
| Auto-Alerts Sent Today | Count of automated reminders dispatched |
| Overrides This Week | Count of manual override actions (CAO/Exam Ctrl) |

Stats bar refreshes on page load. "At Risk" count shown in red if > 0.

---

## 4. Main Branch Exam Schedule Table

### 4.1 Search
- Full-text across: Exam Name, Branch Name
- 300ms debounce · Highlights match in Exam Name and Branch columns
- Scope: Upcoming and ongoing exams by default (not completed or cancelled)

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches in group |
| Exam Name | Search input | From Group Exam Calendar |
| Date | Date range | From / To |
| Readiness Status | Multi-select | Confirmed · Pending · At Risk · Override (manually confirmed) |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · Foundation · Integrated JEE · NEET |
| Has Alert Sent | Toggle | Show only branches that have received an automated alert |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | CAO, Exam Controller | Row select for bulk reminder |
| Branch | Text + link | ✅ | All | Opens branch-exam-detail drawer |
| Exam Name | Text | ✅ | All | Exam name from Group Exam Calendar |
| Date | Date | ✅ | All | Exam date |
| Time | Time | ✅ | All | Exam start time |
| Venue | Text | ✅ | All | Venue name as entered by branch. "Not set" if missing |
| Invigilator Assigned | Text / Badge | ✅ | CAO, Exam Controller | Name or "Not Assigned" |
| Students Expected | Number | ✅ | All | Count enrolled for this exam |
| Hall Tickets Generated | Badge | ✅ | CAO, Exam Controller | Yes / No / Partial |
| Readiness Status | Badge | ✅ | All | Confirmed (green) · Pending (amber) · At Risk (red) · Override (blue) |
| Actions | — | ❌ | Role-based | See Row Actions |

**Column visibility toggle:** Gear icon top-right — saves preference per user.

**Default sort:** Date ascending, then Readiness Status (At Risk first, then Pending, then Confirmed).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z branch-exam pairs" · Page jump input.

**Row highlighting:** At Risk rows have a red left border. Pending rows have amber. Confirmed rows have no highlight.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| View Branch Detail | Eye | All | `branch-exam-detail` drawer 560px | Full setup information |
| Send Reminder | Bell | CAO, Exam Controller | Inline confirm toast | WhatsApp + email to branch principal |
| Mark Override | Checkmark | CAO, Exam Controller | Override modal 420px | Override to Confirmed — reason required — audited |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Send Readiness Reminder to Selected | CAO, Exam Controller | Sends reminder to all selected Pending branches |
| Export Selected (XLSX) | CAO, Exam Controller, Results Coord | Schedule data export |

---

## 5. Drawers & Modals

### 5.1 Drawer: `branch-exam-detail` — Branch Exam Detail
- **Trigger:** View Branch Detail row action or Branch column link
- **Width:** 560px
- **Tabs:** Setup · Invigilators · Hall Tickets · Venue · Issues

#### Tab: Setup
Read-only summary: Branch name, Exam name, Date, Time, Duration, Stream, Class, Students expected, Current readiness status, Last updated by (branch portal or override), Confirmation timestamp.

[Send Reminder] button (CAO/Exam Controller) — fires immediate WhatsApp + email to branch principal.
[Override to Confirmed] button (CAO/Exam Controller) — opens Override modal.

#### Tab: Invigilators
Table: Invigilator Name · Role · Room Assigned · Contact Number.
Populated from branch portal entry. Empty state if branch hasn't entered invigilators yet.

#### Tab: Hall Tickets
Status: Generated / Not Generated / Partial.
If Generated: Count of hall tickets issued, download link (PDF batch if CAO/Exam Controller).
If Not Generated: Warning note with timeline — "Hall tickets should be generated by [Date]".

#### Tab: Venue
Venue name, address, seating capacity, hall layout (if uploaded by branch), room allocation (if entered). Map link if address provided.

#### Tab: Issues
Any issues flagged by the branch (e.g. "Hall under renovation — using alternate venue", "Power backup not confirmed"). Free-text issue log from branch portal with timestamp.
[Log Issue] for branches; [Acknowledge Issue] for group staff.

### 5.2 Modal: Override Readiness
- **Width:** 420px
- **Content:** "Override readiness status for [Branch Name] — [Exam Name] to Confirmed?"
- **Warning:** "This is an audited action. Use only when verbal confirmation has been received."
- **Fields:** Reason for override (required, min 20 chars) · Confirmed by (who gave verbal confirmation — text input) · Notification to branch (checkbox — default on)
- **Buttons:** [Confirm Override] (primary) + [Cancel]
- **On confirm:** Status → Override (blue badge) · Audit log entry · Branch notified

### 5.3 Modal: Send Bulk Reminder
- **Width:** 420px
- **Content:** "Send readiness reminder to [N] selected branches?"
- **Fields:** Message preview (editable — default: "Your branch has a pending exam confirmation for [Exam Name] on [Date]. Please confirm readiness via the branch portal.") · Channel (WhatsApp / Email / Both — default Both)
- **Buttons:** [Send Reminders] (primary) + [Cancel]

---

## 6. Charts

No charts section. This is an operational monitoring page — the table and summary stats provide the necessary visibility. The Group Exam Calendar (page 22) provides the calendar-level density chart.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reminder sent (single) | "Reminder sent to [Branch Name] for [Exam Name]." | Info | 4s |
| Reminder sent (bulk) | "Reminders sent to [N] branches." | Info | 4s |
| Override confirmed | "[Branch Name] — [Exam Name] marked as Confirmed (Override). Audited." | Warning | 6s |
| Auto-alert sent (system) | "Automated alert sent to [N] At Risk branches." | Info | 4s |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No upcoming exams | "No exams scheduled in the next 7 days" | "All branch exam schedules are current. Check the Group Exam Calendar for future dates." | [View Exam Calendar] |
| Filter returns empty | "No branches match your filters" | "Try removing some filters." | [Clear All Filters] |
| No results for search | "No matches found" | "Try a different exam name or branch name." | [Clear Search] |
| All confirmed | "All branches confirmed" | "Every branch for [Exam Name] has confirmed readiness." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| branch-exam-detail drawer open | Spinner + skeleton tabs |
| Tab change inside drawer | Spinner in tab content area |
| Send reminder action | Spinner in reminder button |
| Override confirm | Spinner in confirm button |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Exam Controller G3 | Results Coord G3 | Stream Coords G3 | Calendar Mgr G3 |
|---|---|---|---|---|---|
| [Send Bulk Reminder] button | ✅ | ✅ | ❌ | ❌ | ❌ |
| [Export XLSX] button | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ |
| Send Reminder (row) | ✅ | ✅ | ❌ | ❌ | ❌ |
| Mark Override (row) | ✅ | ✅ | ❌ | ❌ | ❌ |
| Override modal access | ✅ | ✅ | ❌ | ❌ | ❌ |
| Invigilator Assigned column | ✅ | ✅ | ❌ | ❌ | ❌ |
| Hall Tickets column | ✅ | ✅ | ❌ | ❌ | ❌ |
| Invigilators tab (drawer) | ✅ | ✅ | ❌ | ❌ | ❌ |
| Hall Tickets tab (drawer) | ✅ | ✅ | ❌ | ❌ | ❌ |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ❌ (own only) | ✅ |
| Bulk checkbox (row select) | ✅ | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/branch-exam-schedule/` | JWT | List branch-exam pairs (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/branch-exam-schedule/{bex_id}/` | JWT | Branch-exam detail + tabs data |
| POST | `/api/v1/group/{group_id}/acad/branch-exam-schedule/{bex_id}/remind/` | JWT (CAO/Exam Ctrl) | Send reminder to branch |
| POST | `/api/v1/group/{group_id}/acad/branch-exam-schedule/{bex_id}/override/` | JWT (CAO/Exam Ctrl) | Override readiness status |
| POST | `/api/v1/group/{group_id}/acad/branch-exam-schedule/bulk-remind/` | JWT (CAO/Exam Ctrl) | Bulk reminder |
| GET | `/api/v1/group/{group_id}/acad/branch-exam-schedule/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/branch-exam-schedule/export/` | JWT | XLSX export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Schedule search | `input delay:300ms` | GET `.../branch-exam-schedule/?q=` | `#bes-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../branch-exam-schedule/?filters=` | `#bes-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../branch-exam-schedule/?sort=&dir=` | `#bes-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../branch-exam-schedule/?page=` | `#bes-table-section` | `innerHTML` |
| Branch detail drawer | `click` | GET `.../branch-exam-schedule/{id}/` | `#drawer-body` | `innerHTML` |
| Send reminder (row) | `click` | POST `.../branch-exam-schedule/{id}/remind/` | `#toast-container` | `beforeend` |
| Override confirm | `click` | POST `.../branch-exam-schedule/{id}/override/` | `#bes-row-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../branch-exam-schedule/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
