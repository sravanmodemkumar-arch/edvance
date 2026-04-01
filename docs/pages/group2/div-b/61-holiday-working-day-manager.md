# 61 — Holiday & Working Day Manager

> **URL:** `/group/acad/holidays/`
> **File:** `61-holiday-working-day-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Calendar Manager G3 · CAO G4 · Academic Director G3 (view) · Branch staff (request local holidays via branch portal)

---

## 1. Purpose

The Holiday & Working Day Manager maintains the official holiday calendar for the academic year — covering national public holidays, state government holidays, group-declared holidays, and branch-specific local holidays approved by the Calendar Manager. For a group spanning multiple states, this page must handle state-specific holiday variations: Andhra Pradesh, Telangana, Karnataka, Maharashtra, and Tamil Nadu each have different state holidays, and a group with branches across these states cannot apply a single holiday list to all branches.

The manager works in two directions. Top-down: the Calendar Manager declares group-wide or zone-specific holidays that are automatically applied to all branches in scope. Bottom-up: individual branches can submit requests for local holidays (e.g. a local festival, a civic event, or a compensatory holiday after working on a Sunday) through the branch portal; these requests appear in a review queue on this page, where the Calendar Manager approves or rejects them.

An important operational feature is the working days counter: as holidays are added and approved, the system automatically recomputes the total working days remaining in the academic term for each branch, ensuring that branches with too many holidays are flagged before they fall below the CBSE minimum of 220 working days per year. Approved holidays are automatically marked on the Group Academic Calendar (page 59) and on individual branch calendars in the branch portal.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Approve national/group-level holidays | Final approval for group holidays |
| Group Academic Director | G3 | ✅ Full view | ❌ No create | Read-only; can see working day counts |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ❌ | ❌ | No access |
| Group Academic Calendar Manager | G3 | ✅ Full | ✅ Full CRUD + approve branch requests | Primary owner |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Academic Calendar Management  ›  Holiday & Working Day Manager
```

### 3.2 Page Header
```
Holiday & Working Day Manager                        [+ Add Holiday]  [Export Holiday List ↓]
Academic Year [YYYY–YY] · Working days counter by branch         (Calendar Manager, CAO)
```

**View tabs:** [Holiday List] (default) | [Working Days Counter] | [Branch Requests]

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Holidays Declared (Group) | Count |
| National Holidays | Count |
| State Holidays | Count (by state) |
| Group-Declared Holidays | Count |
| Pending Branch Requests | Count — amber |
| Branches Below 220 Working Days Risk | Count — red |

---

## 4. Main Content

### 4.1 Tab: Holiday List

#### Search
- Full-text: Holiday name, Type
- 300ms debounce

#### Advanced Filters
| Filter | Type | Options |
|---|---|---|
| Holiday Type | Multi-select | National / State / Group-declared / Branch-requested |
| Status | Multi-select | Approved / Pending / Rejected |
| Month | Month picker | |
| Branch scope | Multi-select | All / Zone / Specific branches |

#### Holiday List Table
| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Calendar Manager |
| Date | Date | ✅ | |
| Day | Text | ❌ | Monday, Tuesday, etc. |
| Holiday Name | Text | ✅ | |
| Type | Badge | ✅ | National / State / Group / Branch |
| Branches | Text | ✅ | "All" / Zone name / Branch list |
| Status | Badge | ✅ | Approved (green) / Pending (amber) / Rejected (red) |
| Compensatory Working Day | Date | ✅ | If declared; blank if none |
| Actions | — | ❌ | |

**Default sort:** Date ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

#### Row Actions
| Action | Visible To | Notes |
|---|---|---|
| Edit | Calendar Manager | Before holiday date only |
| Delete | Calendar Manager | Before holiday date; soft delete with reason |

### 4.2 Tab: Working Days Counter

Branch-by-branch view of working day count:

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| State | Badge | ✅ | For state-holiday filtering |
| Total Calendar Days (Academic Year) | Number | ✅ | |
| Total Holidays (incl. Sundays) | Number | ✅ | |
| Working Days | Number | ✅ | = Calendar days − All holidays − Sundays |
| CBSE Minimum (220) | Reference | — | Shown as horizontal threshold |
| Status | Badge | ✅ | Safe (≥ 220) · At Risk (210–219) · Below Minimum (< 210) |

**Alert:** Branches with Working Days < 220 are flagged red with a warning icon.

### 4.3 Tab: Branch Requests

Branch-submitted holiday requests awaiting Calendar Manager review:

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Request ID | Text | ✅ | |
| Branch | Text | ✅ | |
| Date Requested | Date | ✅ | |
| Holiday Name | Text | ✅ | |
| Reason | Text (truncated) | ❌ | Full text in drawer |
| Compensatory Day? | Badge | ✅ | Yes / No |
| Submitted At | Datetime | ✅ | |
| Status | Badge | ✅ | Pending / Approved / Rejected |
| Actions | — | ❌ | |

**Row actions:** Review (drawer) · Quick Approve · Quick Reject (with reason)

---

## 5. Drawers & Modals

### 5.1 Drawer: `holiday-add` — Add Holiday
- **Trigger:** [+ Add Holiday] header button
- **Width:** 480px

| Field | Type | Required | Validation |
|---|---|---|---|
| Holiday Name | Text | ✅ | Min 3, max 200 chars |
| Date | Date | ✅ | Within current academic year |
| Holiday Type | Select | ✅ | National / State / Group-declared |
| State applicability | Multi-select | Conditional | Required for State type |
| Branch scope | Multi-select | ✅ | All branches / Zone / Specific branches |
| Reason | Textarea | ❌ | Max 300 chars |
| Compensatory working day | Toggle | ❌ | If on: date picker for compensatory day |
| Compensatory date | Date | Conditional | Must be a Sunday for compensatory to count |

- **Submit:** "Add Holiday"
- **On success:** Holiday added · Group Academic Calendar updated · Branch calendars updated

### 5.2 Drawer: `branch-request-review` — Review Branch Holiday Request
- **Trigger:** Review action on Branch Requests tab
- **Width:** 480px

**Content:**
- Branch name · Date requested · Holiday name · Reason (full text) · Submitted by · Submitted at
- Compensatory day proposed? (Yes/No + date if yes)
- Working days impact: "If approved, [Branch] will have [N] working days remaining"
- Branch's current working day count vs CBSE minimum

**Decision:**
| Field | Type | Required | Notes |
|---|---|---|---|
| Decision | Radio | ✅ | Approve / Reject / Partially approve (different date) |
| Rejection reason | Textarea | Conditional | Required if Reject |
| Alternate date | Date | Conditional | If partially approving |
| Notify branch | Toggle | ✅ | Default on |

- **Buttons:** [Save Decision] · [Cancel]
- **On approve:** Holiday added to branch calendar · Compensatory day added if proposed · Branch notified

### 5.3 Modal: `delete-holiday-confirm`
- **Width:** 420px
- **Content:** "Remove [Holiday Name] on [Date] from the holiday calendar?"
- **Fields:** Reason (required, min 15 chars) · Notify affected branches (checkbox, default on)
- **Buttons:** [Confirm Delete] (danger) · [Cancel]

---

## 6. Charts

### 6.1 Working Days by Branch (Bar)
- **Type:** Horizontal bar
- **Data:** Working days per branch this academic year
- **Reference line:** At 220 (CBSE minimum)
- **Colour:** Green ≥ 220 · Amber 210–219 · Red < 210
- **Tooltip:** Branch · Working days: N
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Holiday added | "Holiday '[Name]' added on [Date]" | Success | 4s |
| Holiday deleted | "Holiday '[Name]' removed. Branches notified." | Warning | 6s |
| Branch request approved | "Holiday request approved for [Branch] on [Date]" | Success | 4s |
| Branch request rejected | "Holiday request rejected. Branch notified with reason." | Warning | 6s |
| Working day alert | "Warning: [Branch] is at risk of falling below 220 working days" | Warning | Manual dismiss |
| Export started | "Holiday list export preparing…" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No holidays declared | "No holidays declared" | "Add the academic year holiday calendar for your group" | [+ Add Holiday] |
| No pending branch requests | "No pending requests" | "All branch holiday requests have been reviewed" | — |
| No results match filters | "No holidays match" | "Clear filters to see all holidays" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + holiday table (10 rows) |
| Tab switch | Spinner → tab content renders |
| Holiday add drawer | Spinner |
| Branch request review drawer | Spinner → content |
| Working days counter load | Skeleton table |

---

## 10. Role-Based UI Visibility

| Element | Calendar Mgr G3 | CAO G4 | Academic Dir G3 |
|---|---|---|---|
| [+ Add Holiday] | ✅ | ✅ (national/group) | ❌ |
| Edit holiday | ✅ | ❌ | ❌ |
| Delete holiday | ✅ | ❌ | ❌ |
| Branch Requests tab | ✅ | ✅ (view only) | ✅ (view only) |
| Review branch request | ✅ | ✅ (override) | ❌ |
| Working Days Counter tab | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |
| Charts | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/holidays/` | JWT | Holiday list |
| GET | `/api/v1/group/{group_id}/acad/holidays/stats/` | JWT | Stats bar |
| POST | `/api/v1/group/{group_id}/acad/holidays/` | JWT (G3 Cal Mgr, G4) | Add holiday |
| PUT | `/api/v1/group/{group_id}/acad/holidays/{id}/` | JWT (G3 Cal Mgr) | Update holiday |
| DELETE | `/api/v1/group/{group_id}/acad/holidays/{id}/` | JWT (G3 Cal Mgr) | Delete holiday |
| GET | `/api/v1/group/{group_id}/acad/holidays/working-days/` | JWT | Working days counter per branch |
| GET | `/api/v1/group/{group_id}/acad/holidays/requests/` | JWT | Branch holiday requests |
| POST | `/api/v1/group/{group_id}/acad/holidays/requests/{id}/decide/` | JWT (G3 Cal Mgr, G4) | Approve/reject branch request |
| GET | `/api/v1/group/{group_id}/acad/holidays/export/?format=pdf` | JWT | Holiday list PDF |
| GET | `/api/v1/group/{group_id}/acad/holidays/charts/working-days/` | JWT | Bar chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tab: Holiday List | `click` | GET `.../holidays/?tab=list` | `#holiday-tab-content` | `innerHTML` |
| Tab: Working Days | `click` | GET `.../holidays/working-days/` | `#holiday-tab-content` | `innerHTML` |
| Tab: Branch Requests | `click` | GET `.../holidays/requests/` | `#holiday-tab-content` | `innerHTML` |
| Search | `input delay:300ms` | GET `.../holidays/?q=` | `#holiday-list-body` | `innerHTML` |
| Filter apply | `click` | GET `.../holidays/?filters=` | `#holiday-list-section` | `innerHTML` |
| Pagination | `click` | GET `.../holidays/?page=` | `#holiday-list-section` | `innerHTML` |
| Add holiday drawer | `click` | GET `.../holidays/create-form/` | `#drawer-body` | `innerHTML` |
| Add holiday submit | `submit` | POST `.../holidays/` | `#drawer-body` | `innerHTML` |
| Review request drawer | `click` | GET `.../holidays/requests/{id}/review-form/` | `#drawer-body` | `innerHTML` |
| Review decision submit | `submit` | POST `.../holidays/requests/{id}/decide/` | `#request-row-{id}` | `outerHTML` |
| Quick approve | `click` | POST `.../holidays/requests/{id}/decide/` | `#request-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
