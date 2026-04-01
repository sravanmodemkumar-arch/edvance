# G-04 — Scholarship Management

> **URL:** `/coaching/finance/scholarships/`
> **File:** `g-04-scholarships.md`
> **Priority:** P2
> **Roles:** Accounts (K5) · Branch Manager (K6) · Director (K7)

---

## 1. Scholarship Programs

```
SCHOLARSHIP PROGRAMS — TCC AY 2026–27

  Program                 │ Value     │ Eligibility                    │ Seats │ Applied │ Awarded
  ────────────────────────┼───────────┼────────────────────────────────┼───────┼─────────┼────────
  Vikram Reddy Merit      │ 100% fee  │ Top 3 in entrance test         │   3   │    —    │   3 ✅
  TCC Topper Scholarship  │  50% fee  │ Top 10% batch (prev. year)     │  10   │   14    │  10 ✅
  Government Employees    │  25% fee  │ Central/State Govt employee    │  No cap│  18    │  18 ✅
  SC/ST Category Support  │ ₹ 2,000  │ Valid caste certificate        │  No cap│  42    │  42 ✅
  BPL / EWS Support       │ ₹ 2,000  │ BPL card or income < ₹3L      │  No cap│  28    │  26 ✅
  Women in Government     │  10% fee  │ Female students (all courses)  │  No cap│ 188    │ 188 ✅
  Sports Quota            │  25% fee  │ State-level sports certificate │  No cap│   8    │   6 ✅
  ────────────────────────┴───────────┴────────────────────────────────┴───────┴─────────┴────────

  TOTAL SCHOLARSHIP VALUE DISBURSED (AY 2026–27 so far):
    Full fee waiver (Vikram Reddy):  3 × ₹18,000 = ₹54,000
    50% fee waiver (TCC Topper):    10 × ₹9,000  = ₹90,000
    Other cash discounts:                          = ₹1,68,400
    Women in Govt (10%):           188 × ₹1,800  = ₹3,38,400
    TOTAL:                                         = ₹6,50,800 (₹6.5 Lakh)
```

---

## 2. Scholarship Application

```
SCHOLARSHIP APPLICATION — AY 2026–27

  Student:     Kavitha Devi (LEAD-1821 — not yet enrolled)
  Applying for: TCC Topper Scholarship (50% fee waiver)

  ELIGIBILITY CHECK:
    [✓] Top 10% batch in previous year: Rank 8/240 in SSC CGL batch 2025–26 ✅
    [✓] Re-enrolling for 2026–27 course ✅
    [✓] Seat available (10 seats, 6 awarded so far) ✅

  DOCUMENTS:
    Last year's result/rank:  [Upload: rank_certificate_kavitha.pdf ✅]
    Photo ID (Aadhaar):       [Linked from existing student profile ✅]

  FEE AFTER SCHOLARSHIP:
    SSC CHSL 2026–27 base fee: ₹ 14,000
    50% scholarship:          -₹  7,000
    Payable base fee:          ₹  7,000
    GST (18% on ₹7,000):      ₹  1,260
    TOTAL PAYABLE:             ₹  8,260  (2 instalments: ₹4,130 each)

  [Submit Application]   [Approve (Branch Manager)]   [Reject with Reason]
```

---

## 3. Scholarship Ledger

```
SCHOLARSHIP LEDGER — AY 2026–27 (as of 30 Mar 2026)

  Name              │ Student ID  │ Program            │ Value       │ Status
  ──────────────────┼─────────────┼────────────────────┼─────────────┼──────────────
  Akhil Kumar       │ TCC-2401    │ TCC Topper 50%     │ ₹ 9,000    │ ✅ Applied
  Divya Sharma      │ TCC-2404    │ Women in Govt 10%  │ ₹ 1,800    │ ✅ Applied
  Ravi Singh        │ TCC-2403    │ SC/ST Support      │ ₹ 2,000    │ ✅ Applied
  Meena K.          │ TCC-2499    │ BPL Support        │ ₹ 2,000    │ ✅ Applied
  Lakshmi T.        │ TCC-2409    │ Women in Govt 10%  │ ₹ 1,800    │ ✅ Applied
  Pavan R.          │ TCC-2428    │ Vikram Reddy Merit │ ₹18,000    │ ✅ Applied
  ...  (289 more)

  TOTAL SCHOLARSHIP VALUE (applied to active enrollments): ₹ 6,50,800
  Impact on revenue:  6.1% of gross fee revenue

  [Download Scholarship Register]   [Reconcile with GST filings]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/finance/scholarships/programs/` | All active scholarship programs |
| 2 | `POST` | `/api/v1/coaching/{id}/finance/scholarships/apply/` | Submit scholarship application |
| 3 | `PATCH` | `/api/v1/coaching/{id}/finance/scholarships/{aid}/approve/` | Approve or reject scholarship |
| 4 | `GET` | `/api/v1/coaching/{id}/finance/scholarships/ledger/?year=2026-27` | Full scholarship ledger |
| 5 | `GET` | `/api/v1/coaching/{id}/finance/scholarships/summary/?year=2026-27` | Total scholarship value and impact |

---

## 5. Business Rules

- Scholarship awards are recorded as fee waivers in the accounting system, not as expenses; the GST is calculated on the post-scholarship fee amount (the amount actually received), not the full list price; if a student receives a 50% scholarship on a ₹14,000 course, they pay ₹7,000 + GST (₹1,260); TCC declares taxable turnover of ₹7,000 for this enrollment, not ₹14,000; the scholarship value is not an expense on TCC's P&L — it is a revenue reduction, which is the correct accounting treatment under Ind AS
- The Vikram Reddy Merit Scholarship (Director's named scholarship — 100% fee waiver) is a flagship programme that TCC uses in marketing; it creates a brand story ("we believe in talent regardless of financial background") that resonates with aspirants from lower-income families; the 3 seats per year are small enough to control cost but significant enough to generate brand equity; recipients are featured (with consent) on TCC's website and social media; this is the closest TCC gets to CSR activity in its core business
- Category scholarships (SC/ST, BPL) require original document verification before scholarship is applied; a post-enrollment discovery of a forged certificate leads to immediate reversal of the scholarship, full fee demand, and a police complaint for document forgery; TCC's verification process (Aadhaar for identity, government certificate scan via DigiLocker where possible) reduces fraud risk; franchise branches must follow the same verification process and cannot apply category scholarships without document evidence
- The "Women in Government" scholarship (10% fee waiver for all female students) is a strategic initiative to improve TCC's gender ratio (currently 34% female); it is not linked to financial need or academic merit; every female student is automatically offered this discount at enrollment; the discount is material enough (₹1,800 on SSC CGL) to influence the decision but small enough not to be the primary purchase driver; TCC tracks gender ratio by batch quarterly to assess whether the initiative is working
- Scholarship data is personal data (it reveals the student's category, financial situation, or academic standing); the scholarship register is accessible only to Accounts and the Branch Manager; faculty and batch coordinators do not know which students are on scholarship; a student on a BPL scholarship attending class alongside full-fee students has the same experience and the same respect — the scholarship is an admissions and finance matter, not a classroom matter; this privacy is non-negotiable

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division G*
