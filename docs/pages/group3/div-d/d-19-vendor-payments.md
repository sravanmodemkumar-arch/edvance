# D-19 — Vendor Payment Register

> **URL:** `/school/fees/vendor-payments/`
> **File:** `d-19-vendor-payments.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Accountant (S3) — full · Administrative Officer (S3) — full (entry) · Principal (S6) — full (approve)

---

## 1. Purpose

Tracks payments to vendors — stationery suppliers, printing vendors, maintenance contractors, internet provider, cleaning service, security agency, etc. This is the school's expenditure register. Required for the annual audit and CBSE financial inspection.

GST invoices must be collected from GST-registered vendors (ITC may be claimed by the school trust if registered under GST, though school services themselves are exempt).

---

## 2. Page Layout

### 2.1 Header
```
Vendor Payment Register — 2025–26            [+ Add Payment]  [Export]
Total Payments: ₹42,18,000 (this year)
Pending Approval: 3 invoices (₹1,24,000)
```

### 2.2 Payment Register
| Voucher No. | Vendor | Description | Invoice No. | Amount | GST | Total | Date | Status |
|---|---|---|---|---|---|---|---|---|
| VP/2026/042 | Krishna Stationery | Answer sheets, question papers | KST/2026/184 | ₹12,000 | ₹2,160 (18%) | ₹14,160 | 25 Mar 2026 | ✅ Paid |
| VP/2026/041 | Jio Fiber | Internet — March 2026 | JIO/2026/8421 | ₹4,999 | ₹900 | ₹5,899 | 20 Mar 2026 | ✅ Paid |
| VP/2026/043 | ABC Plumbing | Toilet repair — Main Block | ABC/2026/22 | ₹8,500 | ₹0 | ₹8,500 | 26 Mar 2026 | ⏳ Pending |

---

## 3. Add Payment

| Field | Value |
|---|---|
| Vendor | [Select from vendor master or add new] |
| Description | Answer sheets bulk purchase — Q3 exams |
| Invoice No. | KST/2026/184 |
| Invoice Date | 24 Mar 2026 |
| Amount (pre-GST) | ₹12,000 |
| GST % | 18% (auto from vendor GST registration) |
| Total with GST | ₹14,160 |
| Payment Mode | NEFT · Cheque · Cash (≤ ₹10,000) |
| Approved By | Principal (A-25 Procurement approval) |
| Upload Invoice | [PDF, max 2MB] |

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/vendor-payments/?year={year}` | Vendor payment register |
| 2 | `POST` | `/api/v1/school/{id}/fees/vendor-payments/` | Add payment |
| 3 | `PATCH` | `/api/v1/school/{id}/fees/vendor-payments/{vp_id}/approve/` | Approve payment |
| 4 | `GET` | `/api/v1/school/{id}/fees/vendor-payments/export/?year={year}` | Export register |

---

## 5. Business Rules

- Cash payments > ₹10,000 are flagged — income tax provisions require cheque/NEFT for amounts above ₹10,000 in a single day to a single vendor
- All vendor payments require a Principal-approved purchase request (A-25 Procurement) before the payment can be entered — prevents unauthorised spending

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
