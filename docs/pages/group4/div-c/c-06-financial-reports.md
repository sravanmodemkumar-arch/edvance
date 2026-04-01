# C-06 — Financial Reports & MIS

> **URL:** `/college/fees/reports/`
> **File:** `c-06-financial-reports.md`
> **Priority:** P1
> **Roles:** Finance Manager (S4) · Principal/Director (S6) · Trust/Management (S7)

---

## 1. Annual Financial Summary

```
ANNUAL FINANCIAL SUMMARY — 2025–26
GREENFIELDS COLLEGE OF ENGINEERING

REVENUE:
  Tuition fee collected:         ₹8,24,00,000  (332 mgmt + 224 conv × fee)
  Development + ancillary fees:  ₹1,12,00,000
  Hostel fee:                    ₹1,44,00,000
  University exam fee collected: ₹3,58,560
  AICTE Pragati scholarship:     ₹16,00,000
  Other (canteen licence, ads):     ₹8,40,000
  ─────────────────────────────────────────────
  TOTAL REVENUE:                ₹11,07,98,560

  Government receivable (TS ePASS):  ₹34,50,000 (not yet received — receivable)

EXPENDITURE:
  Staff payroll (teaching + non-teaching): ₹5,84,20,000 (50+ teaching, 30+ non-teaching)
  Infrastructure & maintenance:            ₹1,24,60,000
  Hostel operations:                       ₹88,40,000
  Laboratory & equipment:                  ₹38,20,000
  Library (books, journals, e-resources):  ₹24,80,000
  Marketing & admissions:                  ₹18,40,000
  Administrative:                          ₹42,60,000
  JNTU exam fee remittance:                ₹3,58,560
  Research & faculty development:          ₹12,40,000
  Capital expenditure:                     ₹64,00,000 (new lab equipment)
  ─────────────────────────────────────────────────────
  TOTAL EXPENDITURE:                      ₹9,01,18,560

NET SURPLUS:                              ₹2,06,80,000

Applicable as: Trust non-distribution surplus (ploughed back)
12A/80G: All surplus reinvested — no distribution to founders ✅
Form 10B (audit): Filed by CA — 28 Sep 2026 ✅

NOTES:
  Revenue basis: ~556 students × ₹2L average annual fee = ₹11.12Cr (approx match ✅)
  Surplus 18.7% of revenue — healthy for reinvestment in infrastructure ✅
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/fees/reports/annual/` | Annual financial summary |
| 2 | `GET` | `/api/v1/college/{id}/fees/reports/monthly/?month=2026-03` | Monthly fee collection report |
| 3 | `GET` | `/api/v1/college/{id}/fees/reports/receivables/` | All receivables (govt + students) |

---

## 3. Business Rules

- College income and expenditure must be presented to the affiliating university and AICTE in the mandatory disclosure; AICTE's "Mandatory Disclosure" (published on AICTE portal) includes financial data; a college that shows consistently high surpluses without reinvestment in infrastructure attracts scrutiny (suggests fee exploitation)
- 12A/80G (tax exemption) compliance requires that no surplus is distributed to promoters; the entire surplus must be used for educational purposes; this is verified by the statutory auditor and submitted via Form 10B/10BB to Income Tax annually by 30 September

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division C*
