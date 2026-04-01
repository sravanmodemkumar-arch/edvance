# A-25 — Procurement & Purchase Requests

> **URL:** `/school/admin/procurement/`
> **File:** `a-25-procurement-requests.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** VP Admin (S5) — full · Admin Officer (S3) — create requests · Principal (S6) — approve · Promoter (S7) — approve major purchases

---

## 1. Purpose

Manages the school's procurement process — from identifying a need to receiving goods/services and closing the purchase. Provides an audit trail for all spending (CBSE and state board compliance requires schools to maintain purchase records). Enforces the "3-quotation rule" for purchases above a defined threshold, which is a common school governance norm.

---

## 2. Page Layout

### 2.1 Header
```
Procurement & Purchase Requests             [+ New Request]  [Vendor Master]  [Export]
Open Requests: 8 · Pending Approval: 3 · GRN Pending: 2 · Closed This Month: 14
```

### 2.2 Request Pipeline

```
DRAFT → SUBMITTED → QUOTATION STAGE → APPROVED → PO ISSUED → GOODS RECEIVED → INVOICE PAID → CLOSED
```

---

## 3. Purchase Requests Table

| PR No | Item/Service | Category | Amount | Requested By | Date | Approval Required From | Status | Action |
|---|---|---|---|---|---|---|---|---|
| PR-2026-042 | 2 Split ACs (1.5 ton) | Infrastructure | ₹1.84L | VP Admin | 22 Mar | Principal + Promoter | Pending Approval | [View] |
| PR-2026-043 | Lab chemicals (Science) | Academic | ₹12,400 | HOD Science | 24 Mar | Principal | Quotation Stage | [View] |
| PR-2026-044 | Photocopy paper (10 reams) | Office | ₹4,200 | Admin Officer | 26 Mar | VP Admin | Approved | [View] |

**Categories:** Infrastructure · Academic / Teaching Aids · Office Supplies · Technology · Maintenance · Sports · Library · Hostel · Transport · Canteen · Events

---

## 4. Purchase Request Detail Drawer

**560px, tabs: Request · Quotations · Approval · GRN · Invoice**

**Request tab:** PR details + justification + budget code + photos (optional) + department
**Quotations tab:** 3 quotation slots (required for > ₹25,000); each: vendor, amount, PDF upload; comparison table auto-generated; [Select Vendor] per row
**Approval tab:** Approval chain status + approver notes
**GRN tab:** Goods Receipt Note — check received items against PO; [Mark Received] per item
**Invoice tab:** Invoice upload + invoice number + payment mode + payment date

---

## 5. Vendor Master

| Vendor | Category | Contact | GST No | Approved | Last PO | Rating |
|---|---|---|---|---|---|---|
| ABC Electronics | Technology/AC | 9876543210 | 36AABCA... | ✅ | 15 Jan 2026 | ⭐⭐⭐⭐ |
| Stationery World | Office Supplies | 9876543211 | 36AABCS... | ✅ | 10 Mar 2026 | ⭐⭐⭐ |

[+ Add Vendor] · [Edit] per vendor

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/procurement/` | PR list |
| 2 | `POST` | `/api/v1/school/{id}/procurement/` | Create PR |
| 3 | `GET` | `/api/v1/school/{id}/procurement/{pr_id}/` | PR detail |
| 4 | `PATCH` | `/api/v1/school/{id}/procurement/{pr_id}/` | Update PR |
| 5 | `POST` | `/api/v1/school/{id}/procurement/{pr_id}/quotations/` | Upload quotation |
| 6 | `POST` | `/api/v1/school/{id}/procurement/{pr_id}/grn/` | Submit GRN |
| 7 | `POST` | `/api/v1/school/{id}/procurement/{pr_id}/close/` | Mark invoice paid + close |
| 8 | `GET` | `/api/v1/school/{id}/procurement/vendors/` | Vendor master |
| 9 | `POST` | `/api/v1/school/{id}/procurement/vendors/` | Add vendor |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
