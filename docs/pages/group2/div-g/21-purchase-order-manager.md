# 21 — Purchase Order Manager

> **URL:** `/group/ops/procurement/purchase-orders/`
> **File:** `21-purchase-order-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full) · Operations Manager G3 (view + create ≤₹1L)

---

## 1. Purpose

Full lifecycle management of Purchase Orders (POs). A PO is the formal document issued
to a vendor after procurement request approval. Tracks from creation through delivery and
payment. Provides audit trail for all procurement spend.

---

## 2. PO Lifecycle

```
Draft → Approved → Sent to Vendor → Partially Delivered → Fully Delivered → Payment Due → Paid → Closed
```

**Approval thresholds:**
- ≤₹1L: Ops Manager can approve
- ₹1L–₹5L: COO approval required
- >₹5L: COO approval + Chairman notification

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Procurement  ›  Purchase Orders
```

### 3.2 Page Header
```
Purchase Order Manager                 [+ Create PO]  [Export ↓]
[N] active · [N] pending delivery · [N] payment due
```

### 3.3 Status Tabs
```
[All]  [Draft (N)]  [Approved (N)]  [Sent to Vendor (N)]  [In Delivery (N)]  [Delivered (N)]  [Payment Due (N)]  [Closed (N)]
```

---

## 4. Search & Filters

**Search:** PO number, vendor name, category, branch. 300ms debounce.

**Filters:** Status · Vendor · Category · Branch · Zone · Amount range · Date range · Approval status

---

## 5. PO Table

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| ☐ | Checkbox | |
| PO Number | ✅ | PO-YYYY-NNNNN · Link → drawer |
| Vendor | ✅ | |
| Category | ✅ | |
| Branches | ✅ | Count or name (if 1) |
| Total Amount | ✅ | ₹ |
| Created Date | ✅ | |
| Expected Delivery | ✅ | Red if overdue |
| Delivery Status | ✅ | Progress bar for partial |
| Payment Status | ✅ | Paid / Partial / Pending |
| Approved By | ✅ | Name |
| Status | ✅ | Colour badge |
| Actions | — | View · Edit (draft only) · Mark Delivered · Record Payment |

**Pagination:** Server-side · 25/page.

---

## 6. Create PO Drawer

- **Width:** 680px
- **Tabs:** Vendor & Items · Branches · Terms · Documents

**Vendor & Items tab:**
| Field | Type |
|---|---|
| Vendor | Searchable select (approved vendors only) |
| Category | Select |
| Line Items | Dynamic table: Item Name · Description · Qty · Unit · Unit Price · Total |
| Add Item | [+ Add Row] button |
| Grand Total | Auto-calculated |

**Branches tab:**
- Which branches this PO covers (multi-select)
- Delivery address per branch
- Quantity per branch for each item (split table)

**Terms tab:**
- Expected delivery date
- Payment terms (from vendor contract, editable)
- Special instructions
- Rush order toggle (if urgent)

**Documents tab:**
- Attach: quotations, vendor proforma invoice
- Note: PO PDF auto-generated on approval

**[Save as Draft] · [Submit for Approval]**

---

## 7. PO Detail Drawer

- **Width:** 680px
- **Tabs:** Summary · Line Items · Delivery · Payments · Documents · History

**Summary tab:** PO number, vendor, category, branches, amount, dates, status, approver.

**Line Items tab:** Full item table with quantities delivered vs ordered.

**Delivery tab:** Per-branch delivery status — items received, date, shortfall, damage notes.

**Payments tab:** Payment schedule, amounts paid, balance due, payment records.

**Documents tab:** PO PDF download, attachments, vendor acknowledgement.

**History tab:** Immutable status change log.

---

## 8. Approval Flow

- PO created as Draft → [Submit for Approval] → routes to approver based on amount
- Approver receives EduForge notification + WhatsApp
- Approver sees in their dashboard approval queue
- Approve: PO status → Approved → Sent to Vendor → vendor email notification sent
- Reject: required reason → PO back to Draft with rejection note

---

## 9. Toast Messages

| Action | Toast | Type |
|---|---|---|
| PO created | "PO [Number] created as draft" | Success · 4s |
| PO submitted | "PO submitted for approval — [Approver] notified" | Info · 4s |
| PO approved | "PO [Number] approved — vendor notified" | Success · 4s |
| PO rejected | "PO [Number] returned to draft with rejection notes" | Warning · 4s |
| Delivery recorded | "Delivery recorded for [Branch]" | Success · 4s |
| Payment recorded | "Payment of ₹[Amount] recorded" | Success · 4s |

---

## 10. Empty States

No POs in any status → appropriate empty state per tab.

---

## 11. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 |
|---|---|---|
| [Create PO] | ✅ | ✅ (≤₹1L) |
| [Approve PO] >₹1L | ✅ | ❌ |
| [Record Payment] | ✅ | ❌ |
| [Edit Draft PO] | ✅ | ✅ own |
| Export | ✅ | ✅ |
| Vendor bank details | ✅ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/procurement/pos/` | JWT (G3+) | PO list |
| POST | `/api/v1/group/{id}/procurement/pos/` | JWT (G3+) | Create PO |
| GET | `/api/v1/group/{id}/procurement/pos/{po_id}/` | JWT (G3+) | PO detail |
| PUT | `/api/v1/group/{id}/procurement/pos/{po_id}/` | JWT (G3+) | Edit draft PO |
| POST | `/api/v1/group/{id}/procurement/pos/{po_id}/submit/` | JWT (G3+) | Submit for approval |
| POST | `/api/v1/group/{id}/procurement/pos/{po_id}/approve/` | JWT (G4) | Approve PO |
| POST | `/api/v1/group/{id}/procurement/pos/{po_id}/reject/` | JWT (G4) | Reject PO |
| POST | `/api/v1/group/{id}/procurement/pos/{po_id}/delivery/` | JWT (G3+) | Record delivery |
| POST | `/api/v1/group/{id}/procurement/pos/{po_id}/payment/` | JWT (G4) | Record payment |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
