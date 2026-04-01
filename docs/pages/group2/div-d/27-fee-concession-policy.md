# 27 — Fee Concession Policy Manager

- **URL:** `/group/finance/fee-structure/concessions/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Fee Structure Manager G3 (primary) · CFO G1 (view)

---

## 1. Purpose

The Fee Concession Policy Manager defines and manages all group-level concession policies that are automatically applied to eligible students at billing time. Unlike ad-hoc waivers (which require case-by-case approval on Page 30), concession policies are pre-approved rules: sibling discounts, staff ward concessions, merit concessions (top 5 rank = 25% concession), RTE quota (100% concession), and EWS concessions.

By centralising concession policies at the group level, the platform ensures consistent application across all branches and prevents branch-level arbitrary concessions that reduce revenue without approval.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Structure Manager | G3 | Full CRUD + activate/deactivate |
| Group CFO | G1 | Read — active policies |
| Group Scholarship Manager (Div C) | G3 | Read — scholarship-linked policies |
| Group Finance Manager | G1 | Read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Structure → Concession Policy Manager
```

### 3.2 Page Header
- **Title:** `Fee Concession Policy Manager`
- **Subtitle:** `[N] Active Policies · [N] Branches · AY [Year]`
- **Right-side controls:** `[AY ▾]` `[+ New Policy]` `[Export ↓]`

---

## 4. Main Table

| Column | Type | Sortable |
|---|---|---|
| Policy Name | Text | ✅ |
| Policy Type | Badge: Sibling · Staff Ward · Merit · RTE · EWS · Sports · Other | ✅ |
| Discount % | % | ✅ |
| Applicable Branches | Count | ✅ |
| Applicable Fee Components | Text | ✅ |
| Eligibility Criteria | Text | ✅ |
| AY | Text | ✅ |
| Status | Badge: Active · Inactive · Draft | ✅ |
| Students Using (current) | Count | ✅ |
| Actions | View · Edit · Activate/Deactivate · Clone | — |

### 4.1 Filters
- Policy Type · Status · Branch · AY

### 4.2 Search
- Policy name

### 4.3 Pagination
- 20 rows/page

---

## 5. Drawers

### 5.1 Drawer: `policy-create` — Create Concession Policy
- **Trigger:** [+ New Policy]
- **Width:** 680px

| Field | Type | Required | Validation |
|---|---|---|---|
| Policy Name | Text | ✅ | |
| Policy Type | Select | ✅ | |
| Academic Year | Select | ✅ | |
| Applicable Branches | Multi-select | ✅ | Default: All |
| Discount Type | Radio: Percentage · Fixed Amount | ✅ | |
| Discount % / Amount | Number | ✅ | 0–100% or ₹ |
| Applicable Fee Components | Multi-select | ✅ | Tuition · Hostel · Mess · Transport |
| Cap Amount | Number | ❌ | Max concession regardless of % |
| Eligibility Criteria | Textarea | ✅ | E.g., "Second sibling of enrolled student" |
| Eligibility Auto-detect | Toggle | ❌ | If ON: system auto-applies based on student record |
| Stackable | Toggle | ❌ | Can this policy combine with other policies? |
| Priority | Number | ✅ | Lower = applied first when stackable = OFF |
| Effective From | Date | ✅ | |
| Effective To | Date | ❌ | Leave blank for indefinite |

- [Cancel] [Save Draft] [Activate Policy]

### 5.2 Drawer: `policy-detail` — View Policy Detail
- Shows all fields + students currently benefiting + financial impact (₹ total concession given)

---

## 6. Policy Impact Summary

Below the table: summary bar showing total concession value applied across all active policies for current AY.

| Policy Type | Students | Total Concession ₹ |
|---|---|---|
| Sibling Discount | [N] | ₹ |
| Staff Ward | [N] | ₹ |
| Merit | [N] | ₹ |
| RTE | [N] | ₹ |
| **Total** | **[N]** | **₹** |

---

## 7. Charts

### 7.1 Concession by Type (Donut)
- **Segments:** Each policy type
- **Centre:** "₹[Total] total concession AY [Year]"

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Policy created | "Concession policy '[Name]' created." | Success | 4s |
| Policy activated | "Policy '[Name]' is now active for [N] branches." | Success | 4s |
| Policy deactivated | "Policy '[Name]' deactivated. No new applications." | Warning | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No policies | "No concession policies" | "Create concession policies to auto-apply discounts." | [+ New Policy] |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table + impact summary skeleton |
| Policy drawer | Spinner + form skeleton |

---

## 11. Role-Based UI Visibility

| Element | Fee Struct Mgr G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [+ New Policy] | ✅ | ❌ | ❌ |
| [Activate/Deactivate] | ✅ | ❌ | ❌ |
| [Edit] | ✅ | ❌ | ❌ |
| View all policies | ✅ | ✅ | ✅ |
| Impact summary | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/fee-structure/concessions/` | JWT (G1+) | Policy list |
| POST | `/api/v1/group/{id}/finance/fee-structure/concessions/` | JWT (G3) | Create policy |
| GET | `/api/v1/group/{id}/finance/fee-structure/concessions/{pid}/` | JWT (G1+) | Policy detail |
| PUT | `/api/v1/group/{id}/finance/fee-structure/concessions/{pid}/` | JWT (G3) | Update policy |
| POST | `/api/v1/group/{id}/finance/fee-structure/concessions/{pid}/activate/` | JWT (G3) | Activate |
| POST | `/api/v1/group/{id}/finance/fee-structure/concessions/{pid}/deactivate/` | JWT (G3) | Deactivate |
| GET | `/api/v1/group/{id}/finance/fee-structure/concessions/impact/` | JWT (G1+) | Impact summary |
| GET | `/api/v1/group/{id}/finance/fee-structure/concessions/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../concessions/?q=` | `#policy-table-body` | `innerHTML` |
| Filter | `change` | GET `.../concessions/?type=&status=` | `#policy-section` | `innerHTML` |
| Create drawer | `click` | GET `.../concessions/create-form/` | `#drawer-body` | `innerHTML` |
| Detail drawer | `click` | GET `.../concessions/{id}/` | `#drawer-body` | `innerHTML` |
| Activate | `click` | POST `.../concessions/{id}/activate/` | `#policy-row-{id}` | `outerHTML` |
| Deactivate | `click` | POST `.../concessions/{id}/deactivate/` | `#policy-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
