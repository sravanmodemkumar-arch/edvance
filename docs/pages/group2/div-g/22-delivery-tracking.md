# 22 — Delivery Tracking

> **URL:** `/group/ops/procurement/deliveries/`
> **File:** `22-delivery-tracking.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** COO G4 · Operations Manager G3

---

## 1. Purpose

Tracks all active and completed deliveries from vendors to branch campuses. Enables the
Operations Manager to identify delayed deliveries, record received items, report shortfalls
and damage, and ensure every branch receives what was ordered.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Procurement  ›  Delivery Tracking
```

### 2.2 Summary Strip
| Card | Value |
|---|---|
| Active Deliveries | Count |
| Overdue Deliveries | Count (red if >0) |
| Deliveries This Month | Count |
| Shortfall Reports | Count |

---

## 3. Deliveries Table

**Status Tabs:** `[All]  [Expected]  [In Transit]  [Partially Received]  [Fully Received]  [Overdue]  [Issue Reported]`

**Search:** PO number, vendor name, branch, item. 300ms debounce.

**Filters:** Status · Branch · Zone · Vendor · Category · Date range.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| PO Number | ✅ | Link → PO detail (Page 21) |
| Vendor | ✅ | |
| Category | ✅ | |
| Branch | ✅ | Delivery destination |
| Items | ❌ | Count |
| Expected Date | ✅ | Red if past + not received |
| Received Date | ✅ | Actual date |
| Status | ✅ | |
| Shortfall | ✅ | Items not delivered |
| Issues | ✅ | Damage / wrong items |
| Actions | — | View · Receive · Report Issue |

---

## 4. Receive Delivery Drawer

- **Width:** 560px
- **Fields:**
  - Items list with: Ordered Qty · Received Qty (editable input) · Condition (Good / Damaged / Wrong Item)
  - Overall receipt date
  - Receiver name at branch
  - Photos (up to 5)
  - Notes

**Shortfall auto-detection:** If Received Qty < Ordered Qty → shortfall flag raised → vendor notification.

---

## 5. Report Issue Drawer

- **Width:** 480px
- **Fields:** Issue Type (Short Delivery / Damaged Goods / Wrong Items / Quality Issues) · Description · Photos · Vendor response required by (date)

---

## 6. Toast / Empty / Loader

Standard division G. Skeleton: summary + table.

---

## 7. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/procurement/deliveries/` | JWT (G3+) | Delivery list |
| GET | `/api/v1/group/{id}/procurement/deliveries/{del_id}/` | JWT (G3+) | Detail |
| POST | `/api/v1/group/{id}/procurement/deliveries/{del_id}/receive/` | JWT (G3+) | Record receipt |
| POST | `/api/v1/group/{id}/procurement/deliveries/{del_id}/issue/` | JWT (G3+) | Report issue |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
