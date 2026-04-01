# 23 — Branch Fee Comparison

- **URL:** `/group/finance/fee-structure/comparison/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Fee Structure Manager G3 · CFO G1 · Finance Manager G1

---

## 1. Purpose

The Branch Fee Comparison page enables side-by-side comparison of fee structures across all branches for a given academic year. The Group Fee Structure Manager uses this to ensure that fee differences between branches are intentional and justified (e.g., urban branches charging more than rural branches) rather than accidental gaps in configuration.

It also supports the CFO's governance requirement: the Board needs to know that fees are standardised where intended and differentiated where appropriate, with documented rationale. The comparison highlights outliers — branches charging significantly above or below the group average — for management review.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Structure Manager | G3 | Full read + export |
| Group CFO | G1 | Full read + export |
| Group Finance Manager | G1 | Read |
| Group Chairman | G5 | Read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Structure Manager → Branch Fee Comparison
```

### 3.2 Page Header
- **Title:** `Branch Fee Comparison`
- **Subtitle:** `AY [Year] · [N] Branches · [Student Type]`
- **Right-side controls:** `[AY ▾]` `[Student Type ▾]` `[Stream ▾]` `[Export ↓]`

---

## 4. Main Comparison Table

Rows = Fee Components | Columns = Branches

| Fee Component | Branch A | Branch B | Branch C | ... | Group Min | Group Max | Group Avg |
|---|---|---|---|---|---|---|---|
| Tuition Fee (Annual) | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ |
| Hostel Fee — Non-AC (Monthly) | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ |
| Hostel Fee — AC (Monthly) | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ |
| Mess Fee (Monthly) | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ |
| Transport Fee (Monthly) | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ |
| Exam Fee | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ |
| Lab Fee | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ |
| **Total Annual (Day Scholar)** | **₹** | **₹** | **₹** | **₹** | **₹** | **₹** | **₹** |

**Colour coding per cell:**
- Green = within ±10% of group average
- Amber = 10–25% above/below average
- Red = > 25% above/below average
- Grey = Not configured / Not applicable

### 4.1 Branch Selector
- Toggle which branches to include in comparison (default: all)
- Max 10 branches visible side-by-side; scroll horizontally for more

### 4.2 Filters
- Student Type · Stream · AY

---

## 5. Outlier Panel

Right-side panel listing branches with fees > 25% above or below group average per component:

| Branch | Component | Branch Fee | Group Avg | Variance % | Status |
|---|---|---|---|---|---|
| [Branch X] | Tuition Fee | ₹ | ₹ | +32% | ⚠️ High |
| [Branch Y] | Mess Fee | ₹ | ₹ | -28% | ⚠️ Low |

---

## 6. Charts

### 6.1 Tuition Fee by Branch (Bar)
- **Sort:** Desc
- **Benchmark line:** Group average
- **Export:** PNG

### 6.2 Total Annual Fee Distribution (Box Plot)
- Min · Q1 · Median · Q3 · Max across branches

### 6.3 Year-on-Year Fee Change by Branch (Grouped Bar)
- **Series:** AY [Previous] vs AY [Current] total

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export | "Branch fee comparison exported." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| No templates for AY | "No fee structures" | "No branches have published fee structures for this AY." |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton comparison table |
| Filter change | Table skeleton |
| AY switch | Full table skeleton |

---

## 10. Role-Based UI Visibility

| Element | Fee Structure Mgr G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| Full comparison table | ✅ | ✅ | ✅ |
| Outlier panel | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/fee-structure/comparison/` | JWT (G1+) | Comparison matrix |
| GET | `/api/v1/group/{id}/finance/fee-structure/comparison/outliers/` | JWT (G1+) | Outlier list |
| GET | `/api/v1/group/{id}/finance/fee-structure/comparison/charts/` | JWT (G1+) | Chart data |
| GET | `/api/v1/group/{id}/finance/fee-structure/comparison/export/` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| AY switch | `change` | GET `.../comparison/?ay=&type=` | `#comparison-table` | `innerHTML` |
| Student type change | `change` | GET `.../comparison/?type=` | `#comparison-section` | `innerHTML` |
| Branch selector | `change` | GET `.../comparison/?branches=` | `#comparison-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
