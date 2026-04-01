# 76 — Teacher-Subject-Class Assignment Matrix

> **URL:** `/group/acad/teacher-assignments/`
> **File:** `76-teacher-subject-class-matrix.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Director G3 (full) · CAO G4 (view + escalate) · Stream Coordinators G3 (own stream)

---

## 1. Purpose

Group-level master grid showing which teacher is assigned to teach which subject in which class-section
at each branch. Enables Academic Director to identify gaps (unassigned slots) and ensure every class-section
has a qualified teacher for each subject.

**Distinction from other pages:**
- Page 53 (Teaching Load): shows how many periods a teacher has — workload/overload detection
- Page 70 (Vacancy Monitor): shows unfilled sanctioned posts at subject level
- This page: shows the actual class-level assignment — **who teaches Class 11A Physics at Branch X?**

---

## 2. Role Access

| Role | Level | Can View | Can Assign | Can Escalate | Notes |
|---|---|---|---|---|---|
| Academic Director | G3 | ✅ All branches | ✅ | ✅ | Primary owner |
| CAO | G4 | ✅ All | ❌ | ✅ | View + escalate critical gaps |
| Stream Coord MPC | G3 | ✅ MPC classes | ❌ | ❌ | Own stream only |
| Stream Coord BiPC | G3 | ✅ BiPC classes | ❌ | ❌ | |
| Stream Coord MEC/CEC | G3 | ✅ MEC/CEC | ❌ | ❌ | |
| Stream Coord HEC | G3 | ✅ HEC | ❌ | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Teacher Assignment Matrix
```

### 3.2 Page Header
```
Teacher-Subject-Class Assignment Matrix              [Export Matrix ↓]  [Escalate Gaps]
AY 2025–26 · [N] Branches · [M] Unassigned Slots · [P] Guest Faculty Covering
```

### 3.3 Summary Stats Bar

| Stat | Value | Color |
|---|---|---|
| Total Class-Subject Slots | 4,820 | — |
| Assigned (Regular Teacher) | 4,531 | Green |
| Covered by Guest Faculty | 187 | Amber |
| Unassigned | 102 | Red |
| Branches with 0 Gaps | 32 | — |
| Branches with Critical Gaps (core subject) | 7 | Red |

---

## 4. Main Matrix View

### 4.1 View: Branch Selector + Matrix

1. **Select Branch** from dropdown or branch list
2. Matrix appears for selected branch:
   - **Rows:** Class + Section (e.g. Class 11A · Class 11B · Class 12A)
   - **Columns:** Subjects (filtered by stream/class)
   - **Cell:** Assigned teacher name · or "⚠ Unassigned" (red) · or "Guest: [Name]" (amber)
   - **Cell click:** Opens slot assignment drawer

### 4.2 Cross-Branch Gap Summary Table (alternative view)

When no branch is selected, shows summary across all branches:

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| Stream | Badge | ✅ | |
| Class | Badge | ✅ | |
| Subject | Badge | ✅ | |
| Sections | Number | ✅ | |
| Assigned Sections | Number | ✅ | |
| Unassigned Sections | Number | ✅ | Red if > 0 |
| Guest Faculty Sections | Number | ✅ | |
| Assignment Type | Badge | ✅ | Regular / Guest / Mixed / Unassigned |
| Actions | — | ❌ | Assign · View |

### 4.3 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | Branch names |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / HEC / Common |
| Class | Multi-select | 6–12 |
| Subject | Multi-select | Subject names |
| Assignment Status | Multi-select | Fully Assigned · Partially Assigned · Unassigned |
| Assignment Type | Multi-select | Regular · Guest · Shared |

---

## 5. Drawers

### 5.1 Drawer: `slot-assign` — Assign Teacher to Slot
- **Trigger:** Cell click (unassigned) or Edit from detail view
- **Width:** 480px

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Read-only | — | Pre-filled from context |
| Class + Section | Read-only | — | Pre-filled |
| Subject | Read-only | — | Pre-filled |
| Assignment Type | Select | ✅ | Regular · Guest Faculty · Shared from Another Branch |
| Teacher | Search + select | ✅ | From branch teacher pool (filtered by subject qualification) |
| Effective From | Date | ✅ | |
| Effective Until | Date | Conditional | Required for Guest Faculty |
| Notes | Text | ❌ | e.g. "Covering while permanent teacher on leave" |

**Validation:** System checks if assigning this teacher exceeds their max periods/week (from Teaching Load Monitor, Page 53) — shows warning, not block.

### 5.2 Drawer: `slot-detail`
- **Trigger:** Click assigned cell
- **Width:** 480px
- **Content:** Teacher name · Qualification · Effective from/until · Assignment type · History of who taught this slot · [Edit] · [Remove]

---

## 6. Bulk Assignment

- Select multiple class-sections (same subject) → Assign same teacher to all
- Useful for: Language subjects, optional subjects taught by one teacher across sections

---

## 7. Alert Logic

| Condition | Alert | Recipient |
|---|---|---|
| Core subject (Maths/Physics/Chemistry/Biology/Economics) slot unassigned | In-app alert | Academic Director |
| Unassigned slot for > 14 days | Red badge + escalation alert | Academic Director + CAO |
| Guest faculty assignment expiring in 7 days with no replacement | Warning badge | Stream Coordinator |

---

## 8. Charts

### 8.1 Assignment Completeness by Branch (Bar)
- **Data:** % of slots assigned (regular + guest) per branch
- **Color:** Green ≥ 95% · Amber 85–94% · Red < 85%
- **Export:** PNG

### 8.2 Unassigned Slots by Subject (Bar)
- **Data:** Count of unassigned slots per subject across all branches
- **Export:** PNG

---

## 9. Export

| Export | Format | Content |
|---|---|---|
| Branch Assignment Sheet | PDF | Formatted grid: Class × Subject → Teacher — for branch notice board |
| Group Gap Report | CSV | All unassigned slots: Branch · Class · Section · Subject |
| Full Assignment Matrix | CSV | All slots with assignment status |

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Assignment saved | "[Teacher] assigned to Class [N][Section] [Subject] at [Branch]." | Success | 4s |
| Assignment removed | "Assignment removed. Slot is now unassigned." | Warning | 4s |
| Escalation sent | "Critical gap escalated to CAO." | Info | 4s |
| Overload warning | "[Teacher] is near their max period limit. Proceeding anyway." | Warning | 5s |

---

## 11. Empty States

| Condition | Heading | Description |
|---|---|---|
| No branch selected | "Select a Branch" | "Choose a branch to view its assignment matrix." |
| No gaps | "All slots assigned" | "Every class-section has an assigned teacher." |
| Filter empty | "No unassigned slots match filters" | "Try clearing filters." |

---

## 12. Loader States

| Trigger | Loader |
|---|---|
| Branch matrix load | Spinner in matrix area |
| Gap summary table | Skeleton rows |
| Slot detail drawer | Spinner + skeleton |

---

## 13. Role-Based UI Visibility

| Element | Academic Dir G3 | CAO G4 | Stream Coords G3 |
|---|---|---|---|
| All branches matrix | ✅ | ✅ | ❌ Own stream |
| [Assign Teacher] | ✅ | ❌ | ❌ |
| [Remove Assignment] | ✅ | ❌ | ❌ |
| [Escalate Gaps] | ✅ | ✅ | ❌ |
| Charts | ✅ | ✅ | ✅ (own stream) |
| Export | ✅ | ✅ | ✅ (own stream) |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/teacher-assignments/` | JWT (G3+) | Cross-branch gap summary |
| GET | `/api/v1/group/{id}/acad/teacher-assignments/stats/` | JWT (G3+) | Summary stats |
| GET | `/api/v1/group/{id}/acad/teacher-assignments/branch/{bid}/` | JWT (G3+) | Branch matrix data |
| GET | `/api/v1/group/{id}/acad/teacher-assignments/slot/{sid}/` | JWT (G3+) | Slot detail |
| POST | `/api/v1/group/{id}/acad/teacher-assignments/slot/{sid}/assign/` | JWT (G3, AcadDir) | Assign teacher |
| DELETE | `/api/v1/group/{id}/acad/teacher-assignments/slot/{sid}/assign/` | JWT (G3, AcadDir) | Remove assignment |
| POST | `/api/v1/group/{id}/acad/teacher-assignments/escalate/` | JWT (G3+) | Escalate gaps to CAO |
| GET | `/api/v1/group/{id}/acad/teacher-assignments/export/?format=csv` | JWT (G3+) | Export gap report |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Select branch | `change` | GET `.../teacher-assignments/branch/{id}/` | `#assignment-matrix` | `innerHTML` |
| Filter gap table | `click` | GET `.../teacher-assignments/?filters=` | `#gap-table-section` | `innerHTML` |
| Slot cell click | `click` | GET `.../teacher-assignments/slot/{id}/` | `#drawer-body` | `innerHTML` |
| Assign teacher submit | `submit` | POST `.../slot/{id}/assign/` | `#slot-cell-{id}` | `outerHTML` |
| Remove assignment | `click` | DELETE `.../slot/{id}/assign/` | `#slot-cell-{id}` | `outerHTML` |
| Escalate | `click` | POST `.../escalate/` | `#escalate-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
