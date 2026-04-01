# 22 — Fee Template Builder

- **URL:** `/group/finance/fee-structure/template-builder/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Fee Structure Manager (G3)

---

## 1. Purpose

The Fee Template Builder is where fee structures are created from scratch or cloned from a previous academic year. A fee template defines all fee components applicable to a student type (Day Scholar / Hosteler / Integrated Coaching) in a given branch and academic year. Once built and published, it governs what the branch accountant can bill students.

Key design principle: fee templates are branch-specific but built centrally by the Group Fee Structure Manager. The manager can clone an existing template, apply a bulk percentage increase (e.g., 10% AY increase), and publish to all branches simultaneously. Individual branch modifications are not permitted without group-level approval.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Structure Manager | G3 | Full CRUD + publish |
| Group CFO | G1 | Read-only |
| Group Finance Manager | G1 | Read-only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Structure Manager → Fee Template Builder
```

### 3.2 Page Header
- **Title:** `Fee Template Builder`
- **Subtitle:** `AY [Year] · [N] Templates`
- **Right-side controls:** `[AY ▾]` `[+ New Template]` `[Clone from AY ▾]` `[Bulk AY Increase %]` `[Export ↓]`

---

## 4. Template List Table

| Column | Type | Sortable |
|---|---|---|
| Template Name | Text | ✅ |
| Branch | Text | ✅ |
| Student Type | Badge: Day Scholar · Hosteler · Integrated | ✅ |
| AY | Text | ✅ |
| Components | Count | ✅ |
| Total Annual Fee | ₹ | ✅ |
| Status | Badge: Draft · Published · Archived | ✅ |
| Actions | Edit · Clone · Publish · Archive · Delete (draft only) | — |

### 4.1 Filters
- Branch · Student Type · Status · AY

### 4.2 Search
- Template name · Branch name

### 4.3 Pagination
- 20 rows/page

---

## 5. Drawers

### 5.1 Drawer: `template-create` — Create New Template
- **Trigger:** [+ New Template]
- **Width:** 900px (wide — multi-section form)

**Step 1: Basic Info**

| Field | Type | Required |
|---|---|---|
| Template Name | Text | ✅ |
| Academic Year | Select | ✅ |
| Branch | Select (multi — apply to multiple branches) | ✅ |
| Student Type | Select | ✅ |

**Step 2: Fee Components — Day Scholar Template**

| Component | Amount (₹) | Frequency | Applicable Streams | Notes |
|---|---|---|---|---|
| Tuition Fee | Input | Term / Monthly / Annual | All / MPC / BiPC / MEC | |
| Admission Fee (one-time) | Input | One-time | All | |
| Registration Fee | Input | Annual | All | |
| Exam Fee | Input | Per exam | All | |
| Lab Fee | Input | Annual | Science streams | |
| Library Fee | Input | Annual | All | |
| Activity Fee | Input | Annual | All | |
| Computer Lab Fee | Input | Annual | All | |
| Sports Fee | Input | Annual | All | |
| ID Card | Input | Annual | All | |
| [+ Add Custom Component] | — | — | — | |

**Step 2b: Fee Components — Hosteler Template** (shows if Hosteler selected)

| Component | Boys Non-AC | Boys AC | Girls Non-AC | Girls AC |
|---|---|---|---|---|
| Hostel Admission (one-time) | ₹ | ₹ | ₹ | ₹ |
| Monthly Hostel Fee | ₹ | ₹ | ₹ | ₹ |
| Mess Fee (monthly) | ₹ | ₹ | ₹ | ₹ |
| Laundry (monthly) | ₹ | ₹ | ₹ | ₹ |
| Medical Fee (annual) | ₹ | ₹ | ₹ | ₹ |
| [+ Add Custom] | | | | |

**Step 2c: Transport Fee** (additional section for Day Scholar)

| Route | Distance (km) | Monthly Fee |
|---|---|---|
| [Route Name] | [km] | ₹ |
| [+ Add Route] | | |

**Step 3: Payment Schedule**
- Term-wise: Term 1 (%) · Term 2 (%) · Term 3 (%)
- OR: Monthly installments
- Late fee: ₹[X] per month after [N] days

**Step 4: Review & Save**
- Summary table of all components
- Total annual fee (auto-calculated)
- [Save as Draft] [Publish]

### 5.2 Drawer: `bulk-ay-increase` — Apply Bulk AY Increase
- **Trigger:** [Bulk AY Increase %]
- **Width:** 500px

| Field | Type | Required |
|---|---|---|
| Source AY | Select | ✅ |
| Target AY | Select | ✅ |
| Increase % | Number | ✅ |
| Apply to Branches | Multi-select | ✅ |
| Apply to Components | Multi-select (all or specific) | ✅ |
| Round to nearest | Select: ₹1 · ₹10 · ₹100 | ✅ |

Preview: shows before/after fee comparison per component.

- [Cancel] [Create Draft Templates]

---

## 6. Inline Editing
- Templates in Draft status can be edited inline (click cell → edit in place → auto-save)
- Published templates require [Edit → Revision] workflow (creates new draft, old stays published until new published)

---

## 7. Charts

### 7.1 Fee Template Coverage by Branch (Progress bars)
- Each branch: progress bar showing Draft / Published / Missing for current AY

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Template created | "Fee template '[Name]' created for [Branch]." | Success | 4s |
| Template published | "Fee template published for [Branch]. Students can now be billed." | Success | 4s |
| Bulk increase applied | "Fee templates created for [N] branches with [X]% increase." | Success | 4s |
| Draft saved | "Template saved as draft." | Info | 3s |
| Validation error | "[Component]: Amount must be > 0." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No templates for AY | "No fee templates" | "Create fee templates for this academic year." | [+ New Template] |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Template drawer | Spinner + skeleton multi-step form |
| Bulk increase preview | Spinner + table skeleton |

---

## 11. Role-Based UI Visibility

| Element | Fee Structure Mgr G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [+ New Template] | ✅ | ❌ | ❌ |
| [Clone from AY] | ✅ | ❌ | ❌ |
| [Bulk AY Increase] | ✅ | ❌ | ❌ |
| [Publish] | ✅ | ❌ | ❌ |
| [Edit draft] | ✅ | ❌ | ❌ |
| [Delete draft] | ✅ | ❌ | ❌ |
| View templates | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/fee-structure/templates/` | JWT (G1+) | Template list |
| POST | `/api/v1/group/{id}/finance/fee-structure/templates/` | JWT (G3) | Create template |
| GET | `/api/v1/group/{id}/finance/fee-structure/templates/{tid}/` | JWT (G1+) | Template detail |
| PUT | `/api/v1/group/{id}/finance/fee-structure/templates/{tid}/` | JWT (G3) | Update template |
| POST | `/api/v1/group/{id}/finance/fee-structure/templates/{tid}/publish/` | JWT (G3) | Publish |
| POST | `/api/v1/group/{id}/finance/fee-structure/templates/{tid}/clone/` | JWT (G3) | Clone |
| POST | `/api/v1/group/{id}/finance/fee-structure/templates/bulk-increase/` | JWT (G3) | Bulk AY increase |
| DELETE | `/api/v1/group/{id}/finance/fee-structure/templates/{tid}/` | JWT (G3) | Delete draft |
| GET | `/api/v1/group/{id}/finance/fee-structure/templates/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../templates/?q=` | `#template-table-body` | `innerHTML` |
| Filter | `change` | GET `.../templates/?branch=&type=` | `#template-section` | `innerHTML` |
| Create drawer | `click` | GET `.../templates/create-form/` | `#drawer-body` | `innerHTML` |
| Publish | `click` | POST `.../templates/{id}/publish/` | `#template-row-{id}` | `outerHTML` |
| Bulk increase drawer | `click` | GET `.../templates/bulk-increase-form/` | `#drawer-body` | `innerHTML` |
| Preview bulk increase | `submit` | POST `.../templates/bulk-increase/preview/` | `#preview-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
