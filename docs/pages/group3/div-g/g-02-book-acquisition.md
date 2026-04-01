# G-02 — Book Acquisition

> **URL:** `/school/library/acquisition/`
> **File:** `g-02-book-acquisition.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Librarian (S3) — request and receive · Academic Coordinator (S4) — approve purchase · Principal (S6) — approve if above budget threshold · Library Assistant (S2) — entry after receipt

---

## 1. Purpose

Manages the complete book procurement workflow — from librarian identifying gaps in the collection, to raising a purchase request, to Academic Coordinator/Principal approval, to purchase order, to receipt and cataloguing. Integrates with D-19 vendor payments for the financial aspect.

---

## 2. Page Layout

### 2.1 Header
```
Book Acquisition                                     [+ New Acquisition Request]
Academic Year: [2026–27 ▼]

Annual Library Budget: ₹1,50,000  ·  Spent: ₹1,12,500  ·  Balance: ₹37,500
Pending Approval: 1 request (₹28,000)  ·  On Order: 2 batches
```

### 2.2 Acquisition Register
```
Req No.    Titles   Amount    Requested By   Status          Date
ACQ/2026/3  24      ₹28,000   Librarian      ⏳ Pending approval  22 Mar 2026
ACQ/2026/2  18      ₹22,000   Librarian      ✅ Received & catalogued  15 Feb 2026
ACQ/2026/1  30      ₹42,500   Librarian      ✅ Received & catalogued  10 Dec 2025
```

---

## 3. New Acquisition Request

```
[+ New Acquisition Request]

Request Type:
  ● Annual collection development (planned)
  ○ Urgent — syllabus update (new edition required)
  ○ Teacher recommendation
  ○ Student request (popular books)
  ○ CBSE compliance (minimum collection requirement)

Suggested books list:

  # | Title                           | Author         | Publisher      | ISBN           | Qty | Est. Price | Total
  1 | Atomic Habits                   | James Clear    | Random House   | 978-1-84794-950-9 | 2  | ₹599   | ₹1,198
  2 | Sapiens (Indian Edition)        | Yuval Harari   | Vintage/Aleph  | 978-93-86021-43-1 | 2  | ₹399   | ₹798
  3 | The Gene (Siddhartha Mukherjee) | S. Mukherjee   | Hamish Hamilton| 978-1-47670-316-7 | 1  | ₹699   | ₹699
  ...
  24 books  ·  Total: ₹28,000

Vendor: [National Book Depot / Strand Book Stall / Amazon India / Other]
Preferred vendor: [National Book Depot, Vijayawada — COD/Invoice]

Justification: "Annual supplement for Class XI Science reference section and
                popular fiction to encourage reading habit per CBSE Reading for Joy."

Budget check: ₹28,000 requested vs ₹37,500 available ✅

Approval threshold:
  ≤ ₹10,000: Academic Coordinator
  > ₹10,000: Principal approval required  ← ₹28,000 requires Principal

[Submit for Approval]
```

---

## 4. Approval & Purchase Order

```
Approval — ACQ/2026/3

Academic Coordinator reviewed: ✅ Approved (22 Mar 2026)
Principal review pending...

[Principal Approval]

Once approved:
  → Purchase Order (PO) auto-generated (linked to D-19 vendor payment)
  → PO Number: LIB-PO/2026/003
  → Vendor notified (email with PO PDF)
  → Expected delivery date tracked

Purchase Order:
  PURCHASE ORDER — LIB-PO/2026/003
  To: National Book Depot, Vijayawada
  Date: 27 Mar 2026

  [List of 24 books with ISBN, qty, unit price, total]

  Total: ₹28,000 (inclusive of all taxes)
  Payment terms: On delivery / 30-day credit

  [Signed by: Principal]
```

---

## 5. Receipt & Cataloguing

```
Receive Books — ACQ/2026/3

Delivery received: 25 Mar 2026
Invoice: NBD/INV/2026/8891  ·  Amount: ₹27,600 (2 books out of stock)

Reconciliation:
  Ordered: 24 titles  ·  Received: 22 titles  ·  Missing: 2 (out of stock at vendor)

  [Mark each received book]:
  1. Atomic Habits (2 copies) — ✅ Received, condition: Good
  2. Sapiens (2 copies) — ✅ Received, condition: Good
  3. The Gene (0 copies) — ❌ Out of stock → [Backorder / Cancel]
  ...

[Catalogue Received Books] → auto-creates G-01 entries with new accession numbers
  → Assigns barcodes: LIB2027001 to LIB2027044
  → Prints barcode labels

[Link to D-19 Vendor Payment] → ₹27,600 to National Book Depot
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/acquisition/?year={y}` | Acquisition register |
| 2 | `POST` | `/api/v1/school/{id}/library/acquisition/` | New acquisition request |
| 3 | `POST` | `/api/v1/school/{id}/library/acquisition/{req_id}/approve/` | Approve request |
| 4 | `POST` | `/api/v1/school/{id}/library/acquisition/{req_id}/receive/` | Mark books received |
| 5 | `GET` | `/api/v1/school/{id}/library/acquisition/{req_id}/po-pdf/` | Purchase order PDF |
| 6 | `GET` | `/api/v1/school/{id}/library/acquisition/budget/?year={y}` | Budget vs spend |

---

## 7. Business Rules

- Books costing > ₹10,000 per batch require Principal approval (linked to D-19 procurement approval in A-25)
- All book purchases are entered as vendor payments in D-19 (invoice-based); GSTIN of vendor required for purchases ≥ ₹5,000 per invoice (ITC purpose)
- Books received but not catalogued within 7 days are flagged to the Librarian — "received but not in catalogue" creates an audit gap
- If a book requested by a teacher/student is not purchased, a reason must be recorded (budget constraint / not age-appropriate / policy)
- Annual library budget allocation is set by the Principal and tracked against this module; overspending requires Principal override

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
