# E-09 — Test Series Package Management

> **URL:** `/coaching/tests/packages/`
> **File:** `e-09-test-series-packages.md`
> **Priority:** P3
> **Roles:** Test Series Coordinator (K4) · Branch Manager (K6) · Accounts (K5)

---

## 1. Active Test Series Packages

```
TEST SERIES PACKAGES — Toppers Coaching Centre
As of 30 March 2026

  Package Name                    │ Tests │ Price    │ Active Subscribers │ Revenue (Mar)
  ────────────────────────────────┼───────┼──────────┼────────────────────┼───────────────
  SSC CGL Full Test Series 2026   │  30   │ ₹ 1,499  │        842         │ ₹ 12,62,658
  SSC CHSL Test Series 2026       │  20   │ ₹   999  │        384         │ ₹  3,83,616
  SSC CGL Sectional Sprints       │  48   │ ₹ 1,299  │        628         │ ₹  8,15,772
  Banking PO + Clerk Combo        │  44   │ ₹ 1,799  │        512         │ ₹  9,21,088
  RRB NTPC + Group D Combo        │  36   │ ₹ 1,199  │        440         │ ₹  5,27,560
  GK Weekly Series (52 tests/yr)  │  52   │ ₹   599  │      1,240         │ ₹  7,42,760
  All-in-One SSC + Banking        │ 100   │ ₹ 2,999  │        186         │ ₹  5,57,814
  Foundation Package (SSC/RRB)    │  24   │ ₹   799  │        320         │ ₹  2,55,680
  ────────────────────────────────┴───────┴──────────┴────────────────────┴───────────────
  TOTAL                                                     4,552         ₹ 55,66,948

  Note: Enrolled batch students get assigned packages as part of course fee (not listed above)
  Above subscribers: External / standalone online purchasers
```

---

## 2. Package Configuration

```
EDIT PACKAGE — SSC CGL Full Test Series 2026

  Package Name:    SSC CGL Full Test Series 2026
  Series linked:   [SSC CGL Full Mock 2026 ▼]
  Total tests:     30 (auto-filled from series)
  Price:           ₹ 1,499
  GST:             18% (SAC 9992 — Online Educational Services)
  Price incl. GST: ₹ 1,768.82 (shown to student at checkout)

  ACCESS PERIOD:    [12 months] from purchase date
  Auto-renew:       ( ) Yes  (●) No (student must repurchase)
  Trial tests:      [Free: Mock #1 only ▼] (unlocked before purchase)

  INCLUDED:
    [✓] All 30 full mocks (published on schedule)
    [✓] Solutions and video explanations
    [✓] Rank among all TCC subscribers (not just classroom students)
    [✓] Score trend chart and section analysis
    [✗] Live doubt sessions (classroom only)
    [✗] Study materials (classroom only)

  COMBO DISCOUNT:  If SSC CGL Full + Sectional Sprints → ₹ 2,499 (save ₹ 299)
  GST Invoice:     Auto-generated on purchase for B2C (DPDPA-compliant)

  [Save]   [Unpublish Package]   [View Subscriber List]
```

---

## 3. Package Revenue Dashboard

```
PACKAGE REVENUE — March 2026

  GROSS REVENUE:         ₹ 55,66,948
  GST Collected (18%):   ₹  8,50,143  (to be remitted by 20 Apr 2026)
  NET REVENUE:           ₹ 47,16,805

  NEW SUBSCRIBERS (March):   386
  Churned (access expired):   42
  NET NEW:                   344

  TOP ACQUISITION CHANNEL:
    YouTube (TCC free content):  48%
    Organic search:              24%
    Student referral:            18%
    Instagram ads:               10%

  GEOGRAPHIC SPREAD:
    Telangana:   44%
    AP:          18%
    Karnataka:    9%
    Maharashtra:  8%
    Others:      21%

  CONVERSION (free trial → paid):  62% (trial test → purchase within 7 days)
  Avg revenue per subscriber:      ₹ 1,222 (blended across all packages)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/test-packages/` | All active packages with subscriber count |
| 2 | `POST` | `/api/v1/coaching/{id}/test-packages/` | Create new test series package |
| 3 | `PATCH` | `/api/v1/coaching/{id}/test-packages/{pid}/` | Update package details / price |
| 4 | `GET` | `/api/v1/coaching/{id}/test-packages/{pid}/subscribers/` | List of package subscribers |
| 5 | `GET` | `/api/v1/coaching/{id}/test-packages/revenue/?month=2026-03` | Package revenue report |
| 6 | `POST` | `/api/v1/coaching/{id}/test-packages/{pid}/discount/` | Apply combo or promo discount |

---

## 5. Business Rules

- Test series packages are sold to external (non-enrolled) students at the listed price; enrolled classroom students receive the relevant package as part of their course fee and are not charged separately; if an enrolled student accidentally purchases a standalone package, TCC's policy is to issue a full refund within 7 days without deducting GST (GST is reversed via credit note); the accounts team processes this and the reversal is logged in the GST reconciliation
- All test package sales to individuals (B2C) must be accompanied by a GST-compliant invoice showing the buyer's name, address, the SAC code (9992 for online education), and the GST amount; the invoice is auto-generated at purchase and emailed to the buyer's registered email; TCC cannot omit the GST invoice even for small transactions — every online educational service transaction is taxable under GST since the 2021 amendment that removed the education exemption for coaching institutes
- Package pricing changes must not affect existing subscribers for the current access period; if TCC raises the SSC CGL Full Test Series price from ₹1,499 to ₹1,799, all subscribers who paid ₹1,499 continue to access the package at no extra charge until their access period expires; this is a basic consumer-protection principle and is also stated in TCC's terms of service; coordinators cannot revoke access from existing subscribers due to pricing changes
- Free trial access (one mock test from a series) is a conversion tool; the trial is available without registration to reduce friction; however, the trial test's results are not stored (no student profile created without consent) — the student sees their score at the end of the session and is prompted to create an account to save their result; this design complies with DPDPA 2023 (no data collected before consent) while still demonstrating product value
- The package revenue figure (₹55.66 lakh / month) is separate from classroom course fee revenue (tracked in Finance, Division G); the test series business is a distinct revenue line that TCC is growing as a scalable, non-location-bound income stream; the Director (A-01) monitors both streams; test series revenue at 15%+ of total revenue triggers a review of whether TCC should invest in a dedicated EdTech product team vs continuing to manage it through the test coordinator

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division E*
