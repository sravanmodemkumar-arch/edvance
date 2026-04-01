# G-07 — GST Compliance & Accounts

> **URL:** `/coaching/finance/gst/`
> **File:** `g-07-gst-accounts.md`
> **Priority:** P2
> **Roles:** Accounts (K5) · Branch Manager (K6) · Director (K7)

---

## 1. GST Overview

```
GST COMPLIANCE DASHBOARD — Toppers Coaching Centre Pvt Ltd
GSTIN: 36AABCT1234F1Z8 | State: Telangana | March 2026

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  OUTPUT GST (collected from students):    ₹  8,42,316                  │
  │  INPUT TAX CREDIT (ITC on purchases):     ₹    62,840                  │
  │  NET GST PAYABLE (Mar 2026):              ₹  7,79,476                  │
  │  GSTR-1 due: 11 Apr 2026  |  GSTR-3B due: 20 Apr 2026                 │
  └──────────────────────────────────────────────────────────────────────────┘

  OUTPUT TAX SUMMARY:
    Revenue stream               │ Taxable Value  │ GST @ 18%   │ SAC Code
    ─────────────────────────────┼────────────────┼─────────────┼──────────
    Classroom coaching (main)    │ ₹ 35,46,800   │ ₹ 6,38,424  │ 9992
    Test series packages (online)│ ₹  7,92,248   │ ₹ 1,42,605  │ 9992
    Study material (printed)     │ ₹    28,500   │ ₹    5,130  │ 4901
    Hostel (if applicable)       │ ₹  3,15,896   │ ₹    56,861 │ 9963 (12%)
    ─────────────────────────────┴────────────────┴─────────────┴──────────
    TOTAL                        │ ₹ 46,83,444   │ ₹ 8,43,020  │

  INPUT TAX CREDIT (ITC):
    Office supplies / stationery:  ₹  8,240  (18%)
    Computer hardware / software:  ₹ 22,800  (18%)
    Printing & materials:          ₹ 14,200  (18%)
    Zoom / cloud services:         ₹  7,600  (18%)
    Electricity (commercial rate): ₹  9,500  (5% — partial ITC)
    TOTAL ITC:                     ₹ 62,840
```

---

## 2. GSTR-1 Filing Preparation

```
GSTR-1 PREPARATION — March 2026
Due: 11 April 2026 | Prepared by: Ms. Revathi (Accounts)

  B2C SUMMARY (all invoices to individuals — students):
    Total invoices:    1,842  (all coaching fee receipts issued in March)
    Total taxable:     ₹ 46,83,444
    IGST:              ₹       0  (all transactions within Telangana — CGST+SGST)
    CGST (9%):         ₹  4,21,510
    SGST (9%):         ₹  4,21,510
    Total GST:         ₹  8,43,020

  HSN/SAC SUMMARY TABLE:
    SAC 9992 (coaching):  ₹ 46,83,444 taxable  |  ₹ 8,43,020 tax
    SAC 4901 (printed):   Included above (part of coaching bundle)

  AMENDMENTS (from previous months):
    Credit notes issued (Mar 2026):   6 (refunds — see G-06)
    Total credit note value:          ₹ 1,14,480 (taxable)
    GST on credit notes:              ₹    20,606  (to be deducted)
    Net output GST after amendments:  ₹  8,22,414

  STATUS:
    [✓] All invoices uploaded to EduForge GST module ✅
    [✓] Credit notes matched to original invoices ✅
    [ ] Final review by CA/Branch Manager — due Apr 8
    [ ] File GSTR-1 on GST portal — due Apr 11
```

---

## 3. Accounts Ledger Summary

```
ACCOUNTS SUMMARY — March 2026

  INCOME:
    Coaching fee (collected):      ₹ 46,83,444  (base, before GST)
    Test series packages:          ₹  7,92,248
    Hostel revenue:                ₹  3,15,896
    Franchise royalty received:    ₹  4,28,400  (6 franchises × avg ₹71,400)
    ───────────────────────────────────────────
    TOTAL INCOME:                  ₹ 62,19,988

  EXPENSES:
    Faculty salaries:              ₹ 18,40,000
    Non-teaching salaries:         ₹  4,20,000
    Hall rent:                     ₹  3,80,000
    Utilities (electricity, etc.): ₹  1,24,000
    Marketing / ads:               ₹  2,48,000
    Printing & materials:          ₹    84,000
    Software / platform:           ₹    46,000
    Miscellaneous:                 ₹    38,000
    ───────────────────────────────────────────
    TOTAL EXPENSES:                ₹ 31,80,000

  EBITDA:  ₹ 30,39,988  (48.9% margin) ✅
  GST payable (not expense, pass-through): ₹ 7,79,476
  Net cash retained (EBITDA - GST):       ₹ 22,60,512
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/finance/gst/summary/?month=2026-03` | GST output/input summary |
| 2 | `GET` | `/api/v1/coaching/{id}/finance/gst/gstr1/?month=2026-03` | GSTR-1 preparation data |
| 3 | `GET` | `/api/v1/coaching/{id}/finance/gst/credit-notes/?month=2026-03` | Credit notes for the month |
| 4 | `GET` | `/api/v1/coaching/{id}/finance/accounts/ledger/?month=2026-03` | P&L summary for the month |
| 5 | `GET` | `/api/v1/coaching/{id}/finance/gst/filing-calendar/` | GST filing due dates |
| 6 | `POST` | `/api/v1/coaching/{id}/finance/gst/gstr1/submit/` | Mark GSTR-1 as filed (with filing reference) |

---

## 5. Business Rules

- GSTR-1 must be filed by the 11th of the following month for regular taxpayers (annual turnover > ₹5 crore); TCC's annual turnover (~₹6+ crore) places it in the regular filer category; GSTR-3B (tax payment) is due by the 20th; late filing attracts a penalty of ₹50/day for regular returns (₹100/day for nil returns); TCC's Accounts team has a 3-stage reminder (7th, 10th, 11th) to ensure timely filing; the Branch Manager reviews the GSTR-1 before filing to catch mismatches between the fee collection report (G-02) and the GST return
- Input Tax Credit (ITC) on business purchases (computers, software, stationery) is available to TCC as a registered GST taxpayer; the ITC reduces the net GST payable; ITC cannot be claimed on: personal expenses, food and beverages, motor vehicles (unless for official transport), and construction services (capital improvement); the Accounts team maintains a GST-eligible purchase register; an unregistered vendor's invoice cannot generate ITC — all significant purchases must be from GST-registered suppliers, with invoices showing GSTIN
- Credit notes issued for refunds must be filed in the same month's GSTR-1 to reduce output tax; a credit note issued in March for an enrollment from February reduces March's output tax; the original invoice's GSTIN and invoice number must be referenced; if TCC issues a credit note but doesn't file it in GSTR-1, it will appear to have overcollected GST; this discrepancy can attract a GST audit; the credit note register (G-06) feeds directly into the GSTR-1 preparation
- The franchise royalty received (15% of franchise gross fee) is income for TCC's main entity; GST implications on the royalty depend on the franchise agreement structure; if the royalty is a "licensing fee" it attracts GST at 18% on the royalty amount; the Accounts team ensures the franchise invoices TCC's management entity for royalty with proper GST; inter-state franchises (outside Telangana) attract IGST on the royalty; this is handled in TCC's annual CA review and is outside the scope of daily accounts
- Annual accounts are audited by a Chartered Accountant firm; the EduForge platform's GST module generates all required data for the audit; the auditors require: complete invoice register (all receipts), all credit notes, ITC register, bank statements, and salary payment records; the Accounts team maintains all of these digitally in EduForge; paper-based accounts maintenance is phased out; the digital audit trail ensures no invoice can be retroactively created or deleted without a system log entry

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division G*
