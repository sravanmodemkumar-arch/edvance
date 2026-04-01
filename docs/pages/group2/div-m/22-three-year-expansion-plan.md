# Page 22: Three-Year Expansion Plan

**Division:** M — Analytics & MIS
**URL:** `/group/analytics/expansion-plan/`
**Primary Role:** 107 — Strategic Planning Officer
**Supporting Roles:** 102 (Analytics Director)
**Read-only access:** 103 (MIS Officer)
**Restricted:** Roles 104, 105, 106 — no access
**Access Level:** G1 (read-only on all operational data; write on Division M expansion plans, milestones, and strategic notes)

---

## 1. Purpose

Provides a structured planning workspace where the Strategic Planning Officer creates and manages a three-year institutional expansion roadmap. Plans are built from approved feasibility studies (page 21), enriched with timelines, milestones, budget allocations, and capacity targets. The page provides a Gantt-style timeline view, progress tracking, and exportable board-level planning reports.

---

## 2. Roles & Permissions Matrix

| UI Element | Role 102 | Role 103 | Role 107 |
|---|---|---|---|
| KPI bar (5 cards) | View | View | View |
| Expansion plan list | View | View | View |
| Plan detail drawer | View | View | View |
| Create expansion plan | — | — | Create |
| Edit draft/active plan | — | — | Edit (own) |
| Delete draft plan | — | — | Delete (own, draft only) |
| Add / edit milestones | — | — | Create/Edit/Delete |
| Mark milestone complete | — | — | Update |
| Add strategic note | — | — | Create/Edit/Delete |
| Generate board report | View | View | Create |
| Export (CSV / PDF) | Download | Download | Download |

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ Breadcrumb: Analytics & MIS > Three-Year Expansion Plan             │
│ Title: "Three-Year Expansion Plan"   [Export ▼]  [+ New Plan]      │
├─────────────────────────────────────────────────────────────────────┤
│  KPI BAR (5 cards)                                                   │
│  Total Plans | Active Plans | Milestones Due (30d) | Budget          │
│              |              |                      │ Allocated | On- │
│              |              |                      │ Track %         │
├─────────────────────────────────────────────────────────────────────┤
│  FILTER BAR                                                          │
│  Status [All ▼]  Plan Year [All ▼]  Phase [All ▼]  [Search…]       │
│  [Apply]  [Clear]                                                    │
├─────────────────────────────────────────────────────────────────────┤
│  EXPANSION PLAN TABLE (sortable, paginated)  [+ New Plan]           │
├──────────────────────────────────┬──────────────────────────────────┤
│  TIMELINE GANTT VIEW             │  BUDGET ALLOCATION CHART         │
│  (Chart.js bar with date axis)   │  (Stacked bar per plan/year)     │
└──────────────────────────────────┴──────────────────────────────────┘
```

---

## 4. KPI Bar

Five stat cards. Auto-refresh `hx-trigger="every 300s"`, `hx-target="#expansion-kpi-bar"`.

| # | Label | Value | Sub-label | Highlight |
|---|---|---|---|---|
| 1 | Total Plans | All expansion plans | "All time" | — |
| 2 | Active Plans | Plans in "Active" status | "Currently executing" | `bg-blue-50` |
| 3 | Milestones Due (30d) | Milestones with target ≤ 30 days away | "Next 30 days" | `bg-amber-50` if > 0 |
| 4 | Budget Allocated | Sum of all active plan budgets (INR Cr) | "Across active plans" | — |
| 5 | On-Track % | % of active milestones on/ahead of schedule | "Based on target dates" | Colour: ≥ 80% green, 60-79% amber, < 60% red |

---

## 5. Filter Bar

| Control | Type | Options |
|---|---|---|
| Status | Select | All / Draft / Active / Completed / On Hold / Cancelled |
| Plan Year | Select | All / Year 1 / Year 2 / Year 3 (relative to plan start) |
| Phase | Select | All / Pre-launch / Setup / Operational / Expansion |
| Search | Text | Plan name, location, reference |

---

## 6. Expansion Plan Table

### 6.1 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Integer | No | — |
| Plan Name | Text | Yes | Truncated 60 chars |
| Target Location | Text | Yes | City, State |
| Plan Type | Badge | Yes | New Branch / Expansion / Relocation |
| Status | Badge | Yes | Draft / Active / Completed / On Hold / Cancelled |
| Start Date | Date | Yes | — |
| End Date | Date | Yes | — |
| Total Budget (INR Cr) | Decimal | Yes | — |
| Milestones | Progress bar | Yes | Completed / Total e.g. "7 / 12" |
| Overall Progress | Progress bar % | Yes | Colour-coded |
| Actions | Buttons | No | [View] [Edit] [Delete] (role-gated) |

### 6.2 Status Colour Codes

| Status | Badge |
|---|---|
| Draft | Grey (`bg-gray-100`) |
| Active | Blue (`bg-blue-100 text-blue-800`) |
| Completed | Green (`bg-green-100 text-green-800`) |
| On Hold | Amber (`bg-amber-100 text-amber-800`) |
| Cancelled | Red (`bg-red-100 text-red-800`) |

### 6.3 Row Actions

- **[Edit]:** Role 107, Draft or Active only.
- **[Delete]:** Role 107, Draft only → confirm modal.
- **[View]:** All permitted roles.
- Row click → View detail drawer.

---

## 7. Create / Edit Expansion Plan Drawer

**ID:** `expansion-plan-drawer`
**Width:** 760px
**Tabs:** 4 tabs

### Tab 1 — Plan Overview

| Field | Type | Validation |
|---|---|---|
| Plan Name | Text (max 200 chars) | Required |
| Plan Type | Select: New Branch / Branch Expansion / Relocation | Required |
| Target Location | Text (City, State) | Required |
| Pincode | Text (6 digits) | Required |
| Linked Feasibility Study | Select (approved studies from page 21) | Optional but recommended |
| Plan Reference No | Auto-generated (read-only) | — |
| Plan Start Date | Date picker | Required |
| Plan End Date | Date picker (must be 1–3 years after start) | Required |
| Academic Year Target | Select (year when branch opens/expands) | Required |
| Plan Description | Textarea (max 1000 chars) | Required, min 30 chars |
| Lead Officer | Read-only (current user) | — |
| Secondary Contact | Select (other Division M users) | Optional |

### Tab 2 — Budget & Capacity

| Field | Type | Validation |
|---|---|---|
| Year 1 Budget (INR lakhs) | Decimal | Required, > 0 |
| Year 2 Budget (INR lakhs) | Decimal | Required, > 0 |
| Year 3 Budget (INR lakhs) | Decimal | Required, > 0 |
| Total Budget (INR lakhs) | Auto-calculated (sum of above); read-only | — |
| Budget Source | Select: Internal Funds / Bank Loan / Investor / Mixed | Required |
| Year 1 Target Student Capacity | Number | Required |
| Year 2 Target Student Capacity | Number | Required |
| Year 3 Target Student Capacity | Number | Required |
| Year 1 Target Staff Count | Number | Required |
| Year 2 Target Staff Count | Number | Required |
| Year 3 Target Staff Count | Number | Required |
| Expected Break-even Month | Number (months from start) | Required |
| Budget Notes | Textarea (max 500 chars) | Optional |

### Tab 3 — Milestones

Dynamic milestone list (add / edit / delete rows inline).

**Default milestones auto-populated based on Plan Type** (can be edited/deleted):
- New Branch: Site Identification → Regulatory Approvals → Construction → Staff Recruitment → IT Infrastructure → Trial Run → Official Launch
- Expansion: Capacity Assessment → Approval → Infrastructure Work → Staff Addition → Operational Update → Launch

**Milestone Row Fields:**

| Field | Type | Validation |
|---|---|---|
| Milestone Name | Text (max 150 chars) | Required |
| Phase | Select: Pre-launch / Setup / Operational / Expansion | Required |
| Target Date | Date picker | Required |
| Owner | Select (staff / management roles in group) | Required |
| Dependency | Select: None / Select prior milestone | Optional |
| Status | Select: Not Started / In Progress / Completed / Delayed | Default: Not Started |
| Notes | Text (max 300 chars) | Optional |

**[+ Add Milestone]** appends a blank row.
Drag-to-reorder milestones (HTML5 drag-and-drop; order is persisted).
[Delete row] removes milestone (confirm only if status = Completed).

### Tab 4 — Risks & Notes

| Field | Type | Validation |
|---|---|---|
| Primary Risk 1 | Textarea (max 300 chars) | Required |
| Primary Risk 2 | Textarea (max 300 chars) | Optional |
| Primary Risk 3 | Textarea (max 300 chars) | Optional |
| Mitigation Plan | Textarea (max 1000 chars) | Required if any risk filled |
| Success Metrics | Textarea (max 500 chars) | Required |
| Board Notes | Textarea (max 1000 chars) — included in board report export | Optional |
| Internal Notes | Textarea (max 1000 chars) — Division M only | Optional |
| Status | Select: Draft / Active / On Hold / Cancelled | Required |

**Form Submit (Create):** POST `/api/v1/analytics/expansion-plans/` → success toast → row prepended to table.
**Form Submit (Edit):** PUT `/api/v1/analytics/expansion-plans/{id}/` → success toast → row updated.

---

## 8. Expansion Plan Detail Drawer

**ID:** `expansion-detail-drawer`
**Width:** 760px
Same 4-tab layout as create/edit but read-only.

Additional read-only fields:
- Created Date / Last Updated Date.
- Milestone completion timeline.
- Linked feasibility study (clickable link → opens feasibility detail drawer).

**Milestone Progress Section (within Tab 3 in detail view):**

Interactive milestone timeline showing:
- Each milestone as a row: Name | Phase | Target Date | Status badge | Owner | Days overdue (if delayed).
- [Mark Complete] button for Role 107 on In-Progress milestones.
- Milestones highlighted in red if past target date with status ≠ Completed.
- Milestones highlighted in amber if target date is within 7 days.

**[Generate Board Report]** button in drawer footer — available to Roles 102, 103, 107. Async PDF export.

---

## 9. Timeline Gantt Chart

**Type:** Horizontal bar chart (Chart.js 4.x Bar with time-scale x-axis)
**Canvas ID:** `expansionGanttChart`
**Height:** 320px (auto-grows with plan count)

- Y-axis: Plan names.
- X-axis: Date axis (from earliest plan start to latest plan end, capped at 3 years).
- Bars: one bar per plan, from start to end date, coloured by status.
- Milestone markers: diamond-shaped data points on each bar at milestone target dates.
- Tooltip on bar: `{Plan Name}: {Start} → {End}, {N} milestones, {progress}% complete`.
- Tooltip on milestone marker: `{Milestone Name}: {Target Date} ({Status})`.
- Clicking a bar opens the plan detail drawer.
- Legend: status colour key.
- Chart scrolls horizontally if > 12 months span (container is scrollable).

---

## 10. Budget Allocation Chart

**Type:** Grouped bar chart (Chart.js 4.x Bar)
**Canvas ID:** `budgetAllocationChart`
**Height:** 300px

- X-axis: Plan names.
- Y-axis: Budget (INR lakhs).
- Groups: Year 1 (dark blue), Year 2 (medium blue), Year 3 (light blue).
- Tooltip: `{Plan} Year {N}: ₹{value} lakhs`.
- Summary line overlay: cumulative total per plan (secondary y-axis).
- Clicking a bar opens the plan detail drawer.

---

## 11. Mark Milestone Complete — Modal

Triggered by [Mark Complete] action (Role 107 only).

| Field | Type | Validation |
|---|---|---|
| Milestone | Read-only | — |
| Completion Date | Date picker (default: today) | Required |
| Completion Notes | Textarea (max 500 chars) | Required, min 10 chars |
| Notify Stakeholders | Checkbox: In-app / Email | Optional |

PATCH `/api/v1/analytics/expansion-plans/{plan_id}/milestones/{id}/complete/` → milestone status updates to "Completed" → overall plan progress recalculates → toast.

---

## 12. Strategic Notes Panel (Role 107 write; Roles 102/103 read)

Freeform notes panel below the table. Not tied to specific plans.

**Notes Table:** Title | Note (truncated) | Plan Link | Added By | Date | Actions (Edit/Delete — own only).

**[+ Add Note] Drawer (Role 107):**

| Field | Validation |
|---|---|
| Title (max 100 chars) | Required |
| Note Text (max 1500 chars) | Required |
| Linked Plan (optional) | Optional |
| Visibility: Division M only / Visible to Analytics Director | Required |

---

## 13. Export

| Option | Endpoint | Notes |
|---|---|---|
| Export Plan List (CSV) | GET `/api/v1/analytics/expansion-plans/export/?format=csv` | With active filters |
| Export Milestones (CSV) | GET `/api/v1/analytics/expansion-plans/{id}/milestones/export/` | Per-plan |
| Generate Board Report (PDF) | POST `/api/v1/analytics/expansion-plans/{id}/board-report/` | Async job |
| Export All Plans Summary (PDF) | POST `/api/v1/analytics/expansion-plans/export/` | Async, all active plans |

**Board Report PDF** includes: plan overview, budget table, Gantt snapshot (static image from Chart.js), milestone table, risks, success metrics, board notes.

---

## 14. Toast Notifications

| Trigger | Type | Message |
|---|---|---|
| Plan created | Success | "Expansion plan '{name}' created." |
| Plan updated | Success | "Plan updated." |
| Plan deleted | Info | "Draft plan removed." |
| Milestone completed | Success | "Milestone '{name}' marked as complete." |
| Note saved | Success | "Strategic note saved." |
| Note deleted | Info | "Note removed." |
| Form validation fail | Error | "Please fill in all required fields." |
| Date validation fail | Error | "End date must be 1–3 years after start date." |
| Export started | Info | "Preparing export…" |
| Export ready | Success | "Export ready. Click to download." |
| Export failed | Error | "Export failed. Please try again." |

---

## 15. Empty States

| Context | Message | CTA |
|---|---|---|
| No plans created | "No expansion plans created yet. Begin by creating your first three-year plan." | "+ New Plan" (Role 107) |
| No results for filters | "No plans match the selected filters." | "Reset Filters" |
| No active plans | "No plans are currently active." | — |
| No milestones due (30d) | "No milestones due in the next 30 days." | — |
| No strategic notes | "No strategic notes added yet." | "+ Add Note" (Role 107) |

---

## 16. Loader States

| Element | Loader |
|---|---|
| Initial page load | 5 card shimmer + filter shimmer + table shimmer (20 rows) + Gantt placeholder + budget chart placeholder |
| Table reload | Table body shimmer (20 rows) |
| KPI bar refresh | Individual card shimmer |
| Drawer open | Spinner centred in drawer |
| Tab switch | Tab content shimmer |
| Gantt + budget chart reload | Canvas grey overlay with spinner |
| Board report generation | Progress indicator in drawer footer |

---

## 17. HTMX Patterns

| Pattern | Target | Endpoint | Trigger |
|---|---|---|---|
| Table + chart reload | `#expansion-main-section` | `/group/analytics/expansion-plan/data/` | Apply filter |
| KPI auto-refresh | `#expansion-kpi-bar` | `/group/analytics/expansion-plan/kpis/` | `every 300s` |
| Table search | `#expansion-table-section` | `/group/analytics/expansion-plan/table/` | `keyup changed delay:300ms` |
| Table pagination | `#expansion-table-section` | `/group/analytics/expansion-plan/table/?page={n}` | Page nav |
| Plan POST/PUT | `#expansion-plan-drawer` | `/api/v1/analytics/expansion-plans/` | Form submit |
| Detail drawer open | `#expansion-detail-drawer` | `/group/analytics/expansion-plan/{id}/detail/` | Row click / [View] |
| Milestone complete PATCH | `#milestone-complete-modal` | `/api/v1/analytics/expansion-plans/{p}/milestones/{m}/complete/` | Modal confirm |
| Note POST | `#strategic-note-form` | `/api/v1/analytics/expansion-plans/notes/` | Form submit |
| Board report poll | `#export-status` | `/api/v1/analytics/export-jobs/{id}/status/` | `every 5s` (stop on complete) |

---

## 18. API Endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | `/api/v1/analytics/expansion-plans/` | List (paginated) | G1 |
| POST | `/api/v1/analytics/expansion-plans/` | Create plan | Role 107 |
| GET | `/api/v1/analytics/expansion-plans/{id}/` | Plan detail | G1 |
| PUT | `/api/v1/analytics/expansion-plans/{id}/` | Update plan | Role 107 (own) |
| DELETE | `/api/v1/analytics/expansion-plans/{id}/` | Delete draft | Role 107 (own draft) |
| GET | `/api/v1/analytics/expansion-plans/kpis/` | KPI values | G1 |
| GET | `/api/v1/analytics/expansion-plans/charts/` | Gantt + budget chart data | G1 |
| GET | `/api/v1/analytics/expansion-plans/{id}/milestones/` | Milestone list | G1 |
| PATCH | `/api/v1/analytics/expansion-plans/{p}/milestones/{m}/complete/` | Mark complete | Role 107 |
| GET | `/api/v1/analytics/expansion-plans/notes/` | Strategic notes | G1 |
| POST | `/api/v1/analytics/expansion-plans/notes/` | Add note | Role 107 |
| PUT | `/api/v1/analytics/expansion-plans/notes/{id}/` | Edit note | Role 107 (own) |
| DELETE | `/api/v1/analytics/expansion-plans/notes/{id}/` | Delete note | Role 107 (own) |
| GET | `/api/v1/analytics/expansion-plans/export/` | CSV export | G1 |
| POST | `/api/v1/analytics/expansion-plans/{id}/milestones/export/` | Milestones CSV | G1 |
| POST | `/api/v1/analytics/expansion-plans/{id}/board-report/` | Board report PDF | G1 |
| POST | `/api/v1/analytics/expansion-plans/export/` | All-plans PDF | G1 |
| GET | `/api/v1/analytics/export-jobs/{id}/status/` | Poll job | G1 |

---

## 19. Mobile (Flutter + Riverpod)

| Screen | Description |
|---|---|
| `ExpansionPlanHomeScreen` | KPI cards + plan list with status badges |
| `ExpansionPlanDetailScreen` | Read-only plan summary (vertical layout replacing tabs) |
| `MilestoneListScreen` | Scrollable milestone list with status badges and target dates |
| `BudgetSummaryScreen` | Budget per year as a simple card list |

No create/edit on mobile. State: `expansionPlanProvider` (Riverpod). Pull-to-refresh.

---

## 20. Accessibility & Responsiveness

- Table scrolls horizontally on mobile; columns Type, Budget, End Date hidden on < 768px.
- Gantt chart scrolls horizontally on small screens; plan name labels are sticky on the left.
- Milestone status badges use colour + text + `aria-label`.
- Drawer is full-screen on mobile; sticky tab bar at top.
- All form tabs: visible labels, `aria-required`, inline error messages.
- Tab navigation: `role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected`.
- Budget chart: `role="img"` with descriptive `aria-label`.
- Overdue milestone rows have `role="alert"` set on the overdue indicator span.
