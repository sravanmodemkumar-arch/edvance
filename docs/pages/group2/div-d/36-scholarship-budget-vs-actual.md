# 36 — Scholarship Budget vs Actual

- **URL:** `/group/finance/scholarship/budget/`
- **Template:** `portal_base.html`
- **Priority:** P2
- **Role:** Scholarship Finance Officer G3 · CFO G1 · Finance Manager G1

---

## 1. Purpose

Tracks the group's scholarship budget allocation against actual disbursements and government grant receipts for the academic year. The Finance Officer monitors whether scholarship spending is within the sanctioned budget and flags over-disbursement risk before it happens.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Scholarship Finance Officer | G3 | Full read + edit budget |
| Group CFO | G1 | Read |
| Group Finance Manager | G1 | Read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Scholarship Finance → Scholarship Budget vs Actual
```

### 3.2 Page Header
- **Title:** `Scholarship Budget vs Actual`
- **Subtitle:** `AY [Year] · Budget: ₹[X] · Disbursed: ₹[Y] · [Z]% Utilised`
- **Right-side controls:** `[AY ▾]` `[+ Enter Budget]` `[Export ↓]`

---

## 4. Budget Table

| Scholarship Category | Annual Budget | Q1 Actual | Q2 Actual | Q3 Actual | Q4 Actual | YTD Total | Variance | % Used |
|---|---|---|---|---|---|---|---|---|
| Merit Scholarship | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Need-Based Scholarship | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Staff Ward Scholarship | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| RTE Scholarship (Group-funded) | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | % |
| Govt Scholarship (Pass-through) | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | ₹ | — |
| **Total** | **₹** | **₹** | **₹** | **₹** | **₹** | **₹** | **₹** | **%** |

Colour: Green < 90% · Amber 90–100% · Red > 100%

**Government Grant Offset:**
| Grant Received | ₹[X] |
| Net Group Cost (Disbursed − Grant Received) | ₹[Y] |

---

## 5. Drawers

### 5.1 Drawer: `budget-entry` — Enter/Edit Scholarship Budget

| Field | Type | Required |
|---|---|---|
| AY | Select | ✅ |
| Merit Budget | Number | ✅ |
| Need-Based Budget | Number | ✅ |
| Staff Ward Budget | Number | ✅ |
| RTE Budget | Number | ✅ |
| Board Resolution / Reference | Text | ❌ |

- [Cancel] [Save Budget]

---

## 6. Charts

### 6.1 Budget vs Actual by Category (Bar)
### 6.2 Cumulative Disbursement vs Budget (Line — monthly)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Budget saved | "Scholarship budget for AY [Year] saved." | Success | 4s |
| Over-budget warning | "Merit scholarship budget exceeded by ₹[X]." | Warning | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No budget | "No scholarship budget" | "Enter the scholarship budget for this AY." | [+ Enter Budget] |

---

## 9. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/scholarship/budget/` | JWT (G1+) | Budget vs actual |
| POST | `/api/v1/group/{id}/finance/scholarship/budget/` | JWT (G3) | Create/update budget |
| GET | `/api/v1/group/{id}/finance/scholarship/budget/export/` | JWT (G1+) | Export |

---

## 10. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| AY switch | `change` | GET `.../scholarship/budget/?ay=` | `#budget-body` | `innerHTML` |
| Budget entry | `click` | GET `.../scholarship/budget/entry-form/` | `#drawer-body` | `innerHTML` |
| Save budget | `submit` | POST `.../scholarship/budget/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
