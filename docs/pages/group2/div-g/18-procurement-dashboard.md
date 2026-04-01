# 18 — Procurement Dashboard

> **URL:** `/group/ops/procurement/`
> **File:** `18-procurement-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full) · Operations Manager G3 (view + approve)

> **Note:** Group Procurement Manager (G0) does NOT have EduForge access. Their work is
> managed by COO/Ops Manager through this portal. The Procurement Manager coordinates
> offline and the COO approves POs in EduForge.

---

## 1. Purpose

Executive overview of all group procurement activity — budget utilization, pending requests
from branches, active POs, vendor performance, and delivery status. COO uses this as the
central procurement command screen before drilling into specific sub-pages.

---

## 2. Role Access

| Role | Access |
|---|---|
| COO G4 | Full — approve POs, manage vendors, view all |
| Operations Manager G3 | View + approve requests ≤₹1L · COO approval needed >₹1L |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Procurement Dashboard
```

### 3.2 Page Header
```
Procurement Dashboard                  [Export Annual Report ↓]
Financial Year [FY] · Updated: [timestamp]
```

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Budget Utilization | `₹1.4Cr / ₹2.0Cr (70%)` | Green ≤80% · Yellow 80–95% · Red >95% | → Page 24 |
| Pending Requests | `18 awaiting approval` | Green =0 · Yellow 1–10 · Red >10 | → Page 19 |
| Active POs | `7 in progress` | Informational | → Page 21 |
| Delayed Deliveries | `2 overdue` | Green =0 · Red ≥1 | → Page 22 |
| Approved Vendors | `34 active` | Informational | → Page 20 |
| Spend This Month | `₹12.4L` | vs budget target | → Page 24 |

**HTMX:** `every 5m` → `/api/v1/group/{id}/procurement/kpi-cards/` → `#kpi-bar`

---

## 5. Sections

### 5.1 Pending Approval Queue

> POs and requests requiring COO/Ops Mgr sign-off.

**Display:** Card list, max 5. "View all →" → Page 19.

**Card fields:** Request ID · Category · Branch(es) · Amount · Requested by · Days pending · [Approve ✓] [Reject ✗] [View Details →]

**Approve:** `hx-post="/api/v1/group/{id}/procurement/requests/{id}/approve/"` → toast + remove card.
**Reject:** Opens modal — required reason.

---

### 5.2 Spend by Category Chart

**Type:** Donut chart — spend by procurement category (Books, Uniforms, Lab Equipment, IT Hardware, Stationery, Furniture, Other).

**Library:** Chart.js 4.x. Legend. Tooltip with amount + %. PNG export.

---

### 5.3 Monthly Procurement Trend Chart

**Type:** Bar chart — monthly spend (₹) vs budget allocation.

**X-axis:** Months (Apr–Mar). **Y-axis:** ₹ Lakhs.

**Colour:** Blue (actual) · Grey (budget). Colorblind-safe.

---

### 5.4 Active POs Summary

Table: PO# · Vendor · Category · Branches · Amount · Expected Delivery · Status

**Link:** [View All POs →] → Page 21.

---

### 5.5 Top Vendors by Activity

Mini-table: Vendor Name · POs This Year · Total Amount · Rating · [View →] → Page 20.

---

### 5.6 Quick Navigation Grid

| Tile | Label | Link |
|---|---|---|
| 1 | Procurement Requests | `/group/ops/procurement/requests/` |
| 2 | Vendor Master | `/group/ops/procurement/vendors/` |
| 3 | Purchase Orders | `/group/ops/procurement/purchase-orders/` |
| 4 | Delivery Tracking | `/group/ops/procurement/deliveries/` |
| 5 | Procurement Calendar | `/group/ops/procurement/calendar/` |
| 6 | Budget Monitor | `/group/ops/procurement/budget/` |

---

## 6. Drawers & Modals

### 6.1 Request Approval Drawer (opened from pending queue)
- **Width:** 560px
- **Tabs:** Request Details · Budget Check · History
- **Request Details:** Category, items, quantities, branches, justification, amount
- **Budget Check:** Current budget remaining for this category, impact of approving
- **History:** Previous similar requests from this branch

### 6.2 Modal: Reject Request
- **Width:** 420px
- Required reason field · min 20 chars · [Confirm Rejection]

---

## 7. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Request approved | "Procurement request approved — vendor notification sent" | Success · 4s |
| Request rejected | "Request rejected with reason" | Warning · 4s |
| Export started | "Annual report export started" | Info · 4s |

---

## 8. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No pending requests | "No procurement requests pending" | — |
| No active POs | "No purchase orders in progress" | [+ Create PO] |
| No spend data | "No procurement activity this year" | — |

---

## 9. Loader States

Page load: Skeleton KPI bar + pending queue cards + 2 charts + PO table.
KPI refresh: Shimmer over values.
Approval action: Spinner in button + disabled.

---

## 10. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 |
|---|---|---|
| [Approve] ≤₹1L | ✅ | ✅ |
| [Approve] >₹1L | ✅ | ❌ (sees as "Pending COO Approval") |
| [Reject] | ✅ | ✅ ≤₹1L only |
| Export Annual Report | ✅ | ❌ |
| Budget configuration | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/procurement/dashboard/` | JWT (G3+) | Full dashboard |
| GET | `/api/v1/group/{id}/procurement/kpi-cards/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{id}/procurement/spend-category/` | JWT (G3+) | Donut chart data |
| GET | `/api/v1/group/{id}/procurement/monthly-trend/` | JWT (G3+) | Bar chart data |
| GET | `/api/v1/group/{id}/procurement/requests/?status=pending` | JWT (G3+) | Pending queue |
| POST | `/api/v1/group/{id}/procurement/requests/{id}/approve/` | JWT (G3+) | Approve request |
| POST | `/api/v1/group/{id}/procurement/requests/{id}/reject/` | JWT (G3+) | Reject request |
| GET | `/api/v1/group/{id}/procurement/pos/?status=active` | JWT (G3+) | Active POs |
| GET | `/api/v1/group/{id}/procurement/vendors/?sort=activity` | JWT (G3+) | Top vendors |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | `/api/.../procurement/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Open request detail | `click` | `/api/.../procurement/requests/{id}/` | `#drawer-body` | `innerHTML` |
| Approve request | `click` | POST `/api/.../requests/{id}/approve/` | `#pending-queue` | `innerHTML` |
| Chart category click | `click` | `/api/.../procurement/requests/?category={}` | Navigates to Page 19 | redirect |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
