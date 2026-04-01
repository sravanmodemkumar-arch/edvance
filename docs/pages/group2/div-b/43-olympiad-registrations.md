# 43 — Olympiad Registration Manager

> **URL:** `/group/acad/olympiad/registrations/`
> **File:** `43-olympiad-registrations.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Olympiad & Scholarship Coord G3 · CAO G4 · Academic MIS Officer G1

---

## 1. Purpose

The Olympiad Registration Manager is the central coordination hub through which the Group Olympiad & Scholarship Coordinator tracks student registrations across all branches for every external competitive examination — NTSE, NMMS, NSO, IMO, KVPY, and state-level olympiads. In a large group with 50 branches, it is operationally impossible to gather registration status over phone calls or emails; this page provides a live, branch-by-branch, olympiad-by-olympiad status board.

The page serves two core needs: first, it ensures no eligible student is missed because their branch failed to register them — a common failure mode in decentralised institution groups. Second, it produces the consolidated registration data the exam body requires: roll-number lists, fee details, and hall-ticket generation confirmations, all of which must be submitted to NTSE/NMMS nodal offices and private olympiad bodies by hard deadlines.

In the Indian education context, missing a registration deadline for a competitive exam like NTSE can cost a meritorious student an entire year's opportunity. This page ensures that the Group Coordinator can see, at a glance, which branches are lagging, send targeted reminders, and export submission-ready files — without relying on manual compilation.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ❌ No create | Can view all branches, all olympiads |
| Group Academic Director | G3 | ❌ | ❌ | No access |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coord — MPC/BiPC/MEC-CEC | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ✅ Full | ✅ Full CRUD | Primary owner of this page |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Read-only | ❌ | Summary stats only, no student data |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Olympiad & Scholarships  ›  Registration Manager
```

### 3.2 Page Header
```
Olympiad Registration Manager                    [Export Registration XLSX ↓]  [Send Reminders]
Track student registrations per olympiad per branch                            (Olympiad Coord only)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Active Olympiads | Count of olympiads with open registration windows |
| Total Registrations (Group) | Sum of all registered students across olympiads |
| Branches with Incomplete Registration | Count of branches not yet at 100% for any active olympiad |
| Registration Deadline — Next 7 Days | Count of olympiads closing within 7 days |
| Fee Collected (Group) | ₹ total registration fees paid this cycle |

Stats bar refreshes on page load; no live poll.

---

## 4. Main Content

### 4.1 Search
- Full-text search across: Olympiad name, Branch name
- 300ms debounce
- Highlights match in Olympiad and Branch columns

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Olympiad | Multi-select | Lists all active olympiads from Olympiad Registry (page 42) |
| Branch | Multi-select | All branches in group |
| Class | Multi-select | Class 6–12 |
| Registration Status | Multi-select | Not Started / In Progress / Submitted / Closed |
| Fee Status | Select | Paid / Unpaid / Partial |
| Deadline proximity | Select | Closing today / Closing in 3 days / Closing in 7 days |

Active filter chips are dismissible. Filter count badge appears on the filter button. "Clear All" link clears all active filters.

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Row select for bulk actions |
| Olympiad | Text + badge | ✅ | Links to Olympiad Registry detail |
| Branch | Text | ✅ | Branch name |
| Class | Badge | ✅ | Class the registration is for |
| Eligible Students | Number | ✅ | Students meeting age/class criteria |
| Registered | Number + progress | ✅ | Count + % of eligible registered |
| Form Submitted | Badge | ✅ | Yes / No / Partial |
| Fee Paid | Badge | ✅ | Yes / No / Partial |
| Hall Ticket | Badge | ✅ | Generated / Pending / Not Yet |
| Registration Deadline | Date | ✅ | Red if ≤ 3 days; amber if ≤ 7 days |
| Actions | — | ❌ | Role-based |

**Column visibility toggle:** Gear icon top-right — saves preference per user.

**Default sort:** Registration Deadline ascending (most urgent first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z registrations" · Page jump input.

**Row select:** Checkbox per row + select-all. Shows selected count badge.

### 4.4 Row Actions

| Action | Visible To | Drawer/Action | Notes |
|---|---|---|---|
| View Students | All roles | `student-registration-list` drawer 560px | Student-level breakdown |
| Send Reminder | Olympiad Coord | Inline action | Sends WhatsApp/email to branch contact |
| Download Branch Report | All roles | File download | Branch-level registration summary PDF |
| Mark Fee Paid | Olympiad Coord | Inline confirm | Updates fee status |

### 4.5 Bulk Actions (shown when rows selected)

| Action | Visible To | Notes |
|---|---|---|
| Send Registration Reminder | Olympiad Coord | Bulk WhatsApp/email to selected branch contacts |
| Export Selected (XLSX) | All with export access | Registration data for selected rows only |
| Mark Fee Paid — Selected | Olympiad Coord | Batch fee status update with confirmation |

---

## 5. Drawers & Modals

### 5.1 Drawer: `student-registration-list`
- **Trigger:** "View Students" row action
- **Width:** 560px
- **Header:** `[Branch Name] — [Olympiad Name] — Class [X] — Registration List`

**Student Table inside drawer:**

| Column | Type | Notes |
|---|---|---|
| Student Name | Text | |
| Roll Number | Text | Internal branch roll |
| Class & Section | Text | |
| Registered | Badge | Yes / No |
| Registration No. | Text | Exam body's registration number (if registered) |
| Fee Paid | Badge | Yes / No |
| Hall Ticket | Badge | Generated / Pending |
| Actions | — | Mark Registered · Mark Fee Paid |

- **Filters inside drawer:** Registered (All/Yes/No) · Fee Paid (All/Yes/No)
- **Footer buttons:** [Download Student List XLSX] · [Send Individual Reminders — Unregistered]

### 5.2 Drawer: `registration-summary-view`
- **Trigger:** Olympiad name click in table
- **Width:** 560px
- **Tabs:** Branch Summary · Fee Status · Hall Tickets · Timeline

**Tab: Branch Summary**
Table: Branch · Eligible · Registered · % · Submitted · Fee Paid · Status

**Tab: Fee Status**
Total fee collected: ₹ X · Outstanding: ₹ X · Per-branch breakdown table.

**Tab: Hall Tickets**
Table: Branch · Expected Hall Tickets · Generated · Downloaded · Pending.

**Tab: Timeline**
Key dates: Registration open date · Deadline · Exam date · Result expected. Colour-coded milestone strip.

### 5.3 Modal: `send-reminder-confirm`
- **Width:** 420px
- **Trigger:** "Send Reminders" header button or row action
- **Content:** "Send reminder to [N] branches with incomplete registration for [Olympiad Name]?"
- **Fields:** Message preview (editable, max 500 chars) · Channel (WhatsApp / Email / Both, default Both)
- **Buttons:** [Send Reminder] · [Cancel]
- **On confirm:** Notification queued · Toast: "Reminder sent to N branches"

---

## 6. Charts

### 6.1 Branch Registration Completion (Horizontal Bar)
- **Type:** Horizontal bar
- **Data:** % of eligible students registered per branch for selected olympiad
- **X-axis:** Registration %
- **Y-axis:** Branch names
- **Colour:** Green ≥ 90% · Amber 60–89% · Red < 60%
- **Tooltip:** Branch · Registered: N / Eligible: N · %
- **Export:** PNG

### 6.2 Olympiad Participation Rate (Multi-series Bar)
- **Type:** Grouped bar chart
- **Data:** Registered count per olympiad for current academic year
- **X-axis:** Olympiad names
- **Y-axis:** Student count
- **Series:** Eligible vs Registered
- **Tooltip:** Olympiad · Eligible: N · Registered: N · %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reminder sent | "Reminder sent to [N] branches for [Olympiad]" | Success | 4s |
| Fee marked paid | "Fee status updated for [Branch] — [Olympiad]" | Success | 4s |
| Export triggered | "Export preparing… download will start shortly" | Info | 4s |
| Student marked registered | "Student [Name] marked as registered" | Success | 4s |
| Bulk reminder sent | "Reminders sent to [N] selected branches" | Success | 4s |
| Action blocked (deadline passed) | "Registration window for [Olympiad] is closed" | Error | Manual dismiss |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No active olympiads | "No olympiads with open registration" | "Add olympiads to the Olympiad Registry to track registrations" | [Go to Olympiad Registry] |
| No results for search/filter | "No registrations match" | "Try different search terms or clear your filters" | [Clear Filters] |
| Branch has no eligible students | "No eligible students in this branch" | "No students in the selected class range for this olympiad" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar (5 cards) + table (10 skeleton rows) |
| Table filter / search / sort / page | Inline skeleton rows (10) |
| Student list drawer open | Spinner → skeleton table rows inside drawer |
| Summary view drawer open | Spinner → skeleton tabs |
| Send reminder submit | Spinner in confirm button |
| Export triggered | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | Olympiad Coord G3 | CAO G4 | MIS G1 G1 |
|---|---|---|---|
| [Export XLSX] button | ✅ | ✅ | ✅ (summary only) |
| [Send Reminders] header button | ✅ | ❌ | ❌ |
| "Send Reminder" row action | ✅ | ❌ | ❌ |
| "Mark Fee Paid" action | ✅ | ❌ | ❌ |
| Bulk actions bar | ✅ | ❌ | ❌ |
| Student names inside drawer | ✅ | ✅ | ❌ (count only) |
| Download Branch Report | ✅ | ✅ | ✅ |
| Filter drawer | ✅ (all filters) | ✅ (all filters) | ✅ (limited) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/olympiad/registrations/` | JWT | List registrations (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/olympiad/registrations/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/olympiad/registrations/{olympiad_id}/{branch_id}/students/` | JWT | Student-level list for drawer |
| POST | `/api/v1/group/{group_id}/acad/olympiad/registrations/{olympiad_id}/{branch_id}/remind/` | JWT (G3) | Send reminder to branch |
| POST | `/api/v1/group/{group_id}/acad/olympiad/registrations/bulk-remind/` | JWT (G3) | Bulk remind selected branches |
| PATCH | `/api/v1/group/{group_id}/acad/olympiad/registrations/{id}/fee-status/` | JWT (G3) | Update fee paid status |
| PATCH | `/api/v1/group/{group_id}/acad/olympiad/registrations/{id}/student/{sid}/registered/` | JWT (G3) | Mark student registered |
| GET | `/api/v1/group/{group_id}/acad/olympiad/registrations/export/?format=xlsx` | JWT | Export registration XLSX |
| GET | `/api/v1/group/{group_id}/acad/olympiad/registrations/charts/completion/` | JWT | Bar chart data |
| GET | `/api/v1/group/{group_id}/acad/olympiad/registrations/charts/participation/` | JWT | Multi-series bar data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../registrations/?q=` | `#registration-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../registrations/?filters=` | `#registration-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../registrations/?sort=&dir=` | `#registration-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../registrations/?page=` | `#registration-table-section` | `innerHTML` |
| Student list drawer | `click` | GET `.../registrations/{oid}/{bid}/students/` | `#drawer-body` | `innerHTML` |
| Summary view drawer | `click` | GET `.../registrations/{oid}/summary/` | `#drawer-body` | `innerHTML` |
| Mark fee paid (row) | `click` | PATCH `.../registrations/{id}/fee-status/` | `#reg-row-{id}` | `outerHTML` |
| Send reminder confirm | `click` | POST `.../registrations/{oid}/{bid}/remind/` | `#toast-container` | `beforeend` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
