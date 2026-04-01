# 20 — Vendor Master

> **URL:** `/group/ops/procurement/vendors/`
> **File:** `20-vendor-master.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full CRUD) · Operations Manager G3 (view + performance update)

---

## 1. Purpose

Maintains the approved vendor registry for all procurement categories. Only vendors in this
registry can be used in Purchase Orders. Tracks vendor contracts, performance ratings,
bank details, and blacklist status. Prevents unauthorized vendor use.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Procurement  ›  Vendor Master
```

### 2.2 Page Header
```
Vendor Master                          [+ Add Vendor]  [Export ↓]
[N] active vendors · [N] contracts expiring in 30d · [N] blacklisted
```

---

## 3. Search & Filters

**Search:** Vendor name, GST number, contact. 300ms debounce.

**Filters:** Category · State · Status (Active/Inactive/Blacklisted) · Contract Expiring (30d/60d/90d)

---

## 4. Vendor Table

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| ☐ | Checkbox | |
| Vendor Name | ✅ | Link → `vendor-detail` drawer |
| GST Number | ✅ | |
| Categories | ❌ | Badges: Books / Uniforms / Lab / IT / Other |
| State | ✅ | Operating state |
| Rating | ✅ | ★★★★☆ (1–5) |
| Active POs | ✅ | Count |
| Contract Expiry | ✅ | Red if <30d · Yellow if <60d |
| Total Spend (YTD) | ✅ | ₹ |
| Status | ✅ | Active · Inactive · Blacklisted |
| Actions | — | View · Edit · Performance · Blacklist |

**Pagination:** Server-side · 25/page.

---

## 5. Vendor Create / Edit Drawer

- **Width:** 640px
- **Tabs:** Profile · Categories · Bank Details · Contract · Documents

**Profile tab:**
| Field | Type |
|---|---|
| Vendor Name | Text (required) |
| GST Number | Text (15-char validation) |
| PAN Number | Text |
| Registered Address | Textarea |
| Contact Person | Text |
| Phone | Tel |
| Email | Email |
| Website | URL (optional) |

**Categories tab:** Multi-select checkboxes for procurement categories + max order value per category.

**Bank Details tab:** Account name · Account number · IFSC · Bank name · Branch · UPI ID (optional).

**Contract tab:** Contract start date · Contract end date · Payment terms (Net 15/30/45) · Credit limit.

**Documents tab:** Upload: GST Certificate · PAN · MSME Certificate · ISO Certificate · Cancelled Cheque.

---

## 6. Vendor Performance Drawer

- **Width:** 520px
- **Tabs:** Ratings · PO History · Issues

**Ratings tab:**
- Delivery Time Rating (1–5)
- Quality Rating (1–5)
- Price Competitiveness (1–5)
- Communication (1–5)
- Composite Rating (weighted average)
- [Update Rating] button (COO/Ops Mgr after PO completion)

**PO History tab:**
- All POs with this vendor: PO# · Amount · Delivery Status · Delivered On Time? · Rating given

**Issues tab:**
- Reported issues: short delivery, damaged goods, price disputes, late delivery

---

## 7. Blacklist Workflow

- **Trigger:** Vendor row → [Blacklist]
- **Modal (480px):** Reason (required, min 30 chars) · Duration (permanent / 6 months / 1 year) · [Confirm Blacklist]
- **Effect:** Vendor removed from PO creation dropdown · Existing POs with vendor flagged for review
- **Audit:** Full audit log entry with reason, date, blacklisted by

---

## 8. Contract Expiry Alert

- Page summary strip shows expiring contracts
- 60-day warning banner on vendor row
- Email alert to COO 60 days before expiry

---

## 9. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Vendor created | "Vendor [Name] added to approved list" | Success · 4s |
| Vendor updated | "Vendor [Name] updated" | Success · 4s |
| Vendor blacklisted | "Vendor [Name] blacklisted — all active POs flagged" | Warning · 6s |
| Rating saved | "Vendor performance rating saved" | Success · 4s |

---

## 10. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No vendors | "No vendors registered" | [+ Add Vendor] |
| No search results | "No vendors match search" | [Clear Filters] |
| No expiring contracts | "No contracts expiring soon" | — |

---

## 11. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 |
|---|---|---|
| [+ Add Vendor] | ✅ | ❌ |
| [Edit] vendor | ✅ | ❌ |
| [Blacklist] | ✅ | ❌ |
| [Update Rating] | ✅ | ✅ |
| Bank Details tab | ✅ | ❌ Hidden |
| Export | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/procurement/vendors/` | JWT (G3+) | Vendor list |
| POST | `/api/v1/group/{id}/procurement/vendors/` | JWT (G4) | Create vendor |
| PUT | `/api/v1/group/{id}/procurement/vendors/{vid}/` | JWT (G4) | Edit vendor |
| GET | `/api/v1/group/{id}/procurement/vendors/{vid}/` | JWT (G3+) | Vendor detail |
| POST | `/api/v1/group/{id}/procurement/vendors/{vid}/blacklist/` | JWT (G4) | Blacklist |
| POST | `/api/v1/group/{id}/procurement/vendors/{vid}/rating/` | JWT (G3+) | Update rating |
| GET | `/api/v1/group/{id}/procurement/vendors/export/?format=csv` | JWT (G3+) | Export |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
