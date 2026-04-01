# 17 — Hostel Fee Structure

> **URL:** `/group/hostel/fees/structure/`
> **File:** `17-hostel-fee-structure.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Hostel Fee Manager (primary) · Hostel Director (view) · Admission Coordinator (view)

---

## 1. Purpose

Configuration and management of hostel fee structures across all branches. Fee plans are defined at the intersection of: Branch × Gender (Boys/Girls) × Room Type (AC/Non-AC) × Academic Year. Each plan specifies accommodation charges, mess charges, optional extras, and payment schedule.

Fee structures must be published and locked before hostel admissions open — once hostelers are admitted under a plan, the plan cannot be retroactively changed (only new plans for new academic years).

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Fee Management  ›  Fee Structure
```

### 2.2 Page Header
- **Title:** `Hostel Fee Structure — AY [current]`
- **Subtitle:** `[N] Active Fee Plans Across [N] Branches`
- **Right controls:** `+ New Fee Plan` · `Copy from Previous AY` · `Export All Plans`

### 2.3 Alert Banner
| Condition | Banner Text | Severity |
|---|---|---|
| Branch hostel has no fee plan configured | "[N] hostel types at [Branch] have no fee plan for AY [current]. Admissions are blocked." | Red |
| Fee plan for next AY not yet created | "Next academic year fee plans have not been published. Students admitted next month will have no fee plan." | Amber |

---

## 3. Fee Plan Table

**Search:** Branch name, plan name. 300ms debounce.

**Filters:** Branch · Gender · Room Type (AC/Non-AC) · AY · Status (Active/Draft/Archived).

**Columns:**
| Column | Sortable |
|---|---|
| Plan Name | ✅ |
| Branch | ✅ |
| Gender | ✅ |
| Room Type | ✅ |
| AY | ✅ |
| Accommodation / Month | ✅ |
| Mess / Month | ✅ |
| Extras / Month | ✅ |
| Total / Month | ✅ |
| Total / Year | ✅ |
| Hostelers on Plan | ✅ |
| Status | ✅ |
| Actions | ❌ |

**Pagination:** Server-side · 25/page.

---

## 4. Drawers

### 4.1 Drawer: `fee-plan-create`
- **Trigger:** + New Fee Plan
- **Width:** 560px
- **Fields:**
  - Plan Name (e.g., "Boys AC Full Year 2025-26")
  - Branch
  - Gender (Boys / Girls)
  - Room Type (AC / Non-AC)
  - Academic Year
  - **Fee Components (all ₹/month):**
    - Accommodation Fee
    - Mess Fee (standard)
    - Mess Fee — Veg only (if applicable)
    - Laundry (optional)
    - AC Maintenance Charge (only if AC)
    - Medical Room (per year, optional)
    - Study Material (optional)
    - Excursion / Events (optional)
    - Other extras (repeatable: name + amount)
  - **Payment Schedule:**
    - Frequency: Monthly / Quarterly / Half-yearly / Annual
    - Due Date: (e.g., 5th of each month)
    - Late Fee: ₹ per day after due date
  - Status: Draft / Active
- **Validation:** AC maintenance charge allowed only if Room Type = AC; cannot have same Branch × Gender × Type × AY combination as an existing active plan

### 4.2 Drawer: `fee-plan-edit`
- **Trigger:** Actions → Edit (only allowed on Draft status plans; Active plans are locked)
- **Width:** 560px (same fields as create)

### 4.3 Modal: Publish Fee Plan (Draft → Active)
- **Trigger:** Actions → Publish
- **Type:** Centred modal (480px)
- **Content:** "Publishing this fee plan will make it available for hostel admissions. Hostelers admitted under this plan cannot have retroactive fee changes. Confirm?"
- **On confirm:** Status = Active; plan locked from edits

### 4.4 Modal: Archive Fee Plan
- **Trigger:** Actions → Archive (only if no active hostelers on plan)
- **Type:** Centred modal (480px)
- **Confirmation required:** "No active hostelers" check; warning if hostelers exist

---

## 5. Fee Comparison View

> Side-by-side comparison of fee plans across branches.

**Display:** Pivot table — Branch in rows · Fee components in columns · Values filterable by Gender + Room Type + AY.

Useful for standardization audits — quickly spots branches where AC fee is significantly higher/lower than group average.

---

## 6. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Fee plan created | "Fee plan '[Name]' created as Draft." | Success | 4s |
| Fee plan published | "Fee plan '[Name]' is now Active. Admissions can proceed." | Success | 4s |
| Fee plan archived | "Fee plan '[Name]' archived." | Info | 4s |
| Copied from previous AY | "[N] fee plans copied from AY [previous] as Drafts." | Info | 5s |

---

## 7. Role-Based UI Visibility

| Element | Fee Manager G3 | Hostel Director G3 | Admission Coord G3 |
|---|---|---|---|
| Create Fee Plan | ✅ | ❌ | ❌ |
| Edit Draft | ✅ | ❌ | ❌ |
| Publish Plan | ✅ | ✅ (co-authorisation) | ❌ |
| Archive Plan | ✅ | ✅ | ❌ |
| View all plans | ✅ | ✅ | ✅ (read-only) |
| Comparison View | ✅ | ✅ | ✅ |

---

## 8. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/fees/plans/` | JWT (G3+) | All fee plans |
| POST | `/api/v1/group/{group_id}/hostel/fees/plans/` | JWT (G3+) | Create plan |
| PATCH | `/api/v1/group/{group_id}/hostel/fees/plans/{id}/` | JWT (G3+) | Edit draft plan |
| POST | `/api/v1/group/{group_id}/hostel/fees/plans/{id}/publish/` | JWT (G3+) | Publish plan |
| POST | `/api/v1/group/{group_id}/hostel/fees/plans/{id}/archive/` | JWT (G3+) | Archive plan |
| POST | `/api/v1/group/{group_id}/hostel/fees/plans/copy-from-previous-ay/` | JWT (G3+) | Copy plans to new AY |
| GET | `/api/v1/group/{group_id}/hostel/fees/plans/comparison/` | JWT (G3+) | Cross-branch comparison |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
