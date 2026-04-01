# G-01 — Fee Structure & Course Pricing

> **URL:** `/coaching/finance/fee-structure/`
> **File:** `g-01-fee-structure.md`
> **Priority:** P1
> **Roles:** Accounts (K5) · Branch Manager (K6) · Director (K7)

---

## 1. Current Fee Structure

```
FEE STRUCTURE — Toppers Coaching Centre
Academic Year 2026–27 | Effective: 1 April 2026

  COURSE               │ Duration  │ Base Fee    │ GST (18%)  │ Total Fee   │ Max Discount
  ─────────────────────┼───────────┼─────────────┼────────────┼─────────────┼─────────────
  SSC CGL Full Batch   │ 10 months │ ₹ 18,000   │ ₹  3,240   │ ₹ 21,240   │ ₹  2,000
  SSC CHSL Full Batch  │  8 months │ ₹ 14,000   │ ₹  2,520   │ ₹ 16,520   │ ₹  1,500
  Banking PO           │ 10 months │ ₹ 20,000   │ ₹  3,600   │ ₹ 23,600   │ ₹  2,000
  Banking Clerk        │  8 months │ ₹ 16,000   │ ₹  2,880   │ ₹ 18,880   │ ₹  1,500
  RRB NTPC             │  8 months │ ₹ 14,000   │ ₹  2,520   │ ₹ 16,520   │ ₹  1,500
  RRB Group D          │  6 months │ ₹ 10,000   │ ₹  1,800   │ ₹ 11,800   │ ₹  1,000
  Foundation Batch     │  6 months │ ₹ 10,000   │ ₹  1,800   │ ₹ 11,800   │ ₹  1,000
  Crash Course (3 mo.) │  3 months │ ₹  8,000   │ ₹  1,440   │ ₹  9,440   │ ₹    500
  ─────────────────────┴───────────┴─────────────┴────────────┴─────────────┴─────────────

  NOTES:
    GST: SAC 9992 — Commercial Training and Coaching (18% — no exemption)
    Discounts applied on base fee before GST calculation
    Online batch: same fee as offline (no discount for mode)
    Franchise branches: same fee (TCC brand standard — no variation allowed)
```

---

## 2. Approved Discounts

```
APPROVED DISCOUNT TYPES — AY 2026–27

  Type                    │ Amount   │ Eligibility                           │ Document Required
  ────────────────────────┼──────────┼───────────────────────────────────────┼────────────────────────
  Early-bird              │ ₹ 1,000  │ Enroll ≥ 60 days before batch start   │ None
  Alumni re-enroll        │ ₹   500  │ Previously enrolled at TCC            │ Old student ID
  Referral (referred)     │ ₹   500  │ Referred by existing student          │ Referrer ID logged
  SC/ST/OBC-NCL (BPL)     │ ₹ 2,000  │ BPL certificate / income < ₹3L/yr     │ BPL/Income cert.
  Defence / Ex-serviceman │ ₹ 1,000  │ CSD card / discharge certificate      │ CSD/Discharge cert.
  Sibling discount        │ ₹   500  │ Sibling currently enrolled at TCC     │ Sibling's student ID
  ────────────────────────┴──────────┴───────────────────────────────────────┴────────────────────────
  MAX COMBINABLE: One discount only per enrollment
  Custom discount (any):  Requires Branch Manager written approval + reason logged

  YEAR-ON-YEAR FEE REVISION HISTORY:
    AY 2024–25:  SSC CGL ₹ 16,000  (base)
    AY 2025–26:  SSC CGL ₹ 17,000  (+6.3%)
    AY 2026–27:  SSC CGL ₹ 18,000  (+5.9%)
    Avg annual increase: ~6% (tracks with CPI + faculty salary increments)
```

---

## 3. Fee Revision Workflow

```
FEE REVISION REQUEST — AY 2027–28

  PROPOSED REVISION:
    SSC CGL: ₹ 18,000 → ₹ 19,000 (+5.6%)  [Proposed by: Accounts team]
    Banking PO: ₹ 20,000 → ₹ 21,000 (+5.0%)
    Others: +5% across board

  JUSTIFICATION:
    Faculty salary increment (Apr 2027):  +8% budgeted
    Hall rent increase (lease renewal):   +10%
    Material printing cost:               +6%
    Blended cost increase:               ~7.2% → fee increase of 5–6% = margin compression

  APPROVAL WORKFLOW:
    Step 1: Accounts team drafts proposal → ✅ Done
    Step 2: Branch Manager review → ⏳ Pending (due: Apr 10)
    Step 3: Director approval → Pending
    Step 4: Update fee structure in system (effective 1 Apr 2027)
    Step 5: Notify enrolled students (price lock for existing enrollments) ✅ Policy

  NOTE: Students enrolled in AY 2026–27 are NOT affected by the fee revision.
  New fees apply only to new enrollments from 1 Apr 2027.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/finance/fee-structure/` | Current fee structure |
| 2 | `GET` | `/api/v1/coaching/{id}/finance/fee-structure/discounts/` | All approved discount types |
| 3 | `GET` | `/api/v1/coaching/{id}/finance/fee-structure/history/` | Year-on-year fee revision history |
| 4 | `POST` | `/api/v1/coaching/{id}/finance/fee-structure/revision/` | Submit fee revision proposal |
| 5 | `PATCH` | `/api/v1/coaching/{id}/finance/fee-structure/` | Update fee structure (Director role) |

---

## 5. Business Rules

- Fee structures are set at the beginning of each academic year and are price-locked for all enrollments made in that year; a student who enrolls in August 2026 and pays the 2026–27 fee rate continues at that rate for the entire 10-month course, even if fees increase in April 2027; this price-lock is a consumer protection commitment published in TCC's enrollment terms; violating the price-lock (charging enrolled students mid-course) has led to legal disputes at other coaching centres and is a reputational risk
- GST at 18% on coaching services is non-waivable; the base fee is exclusive of GST, and the total amount always includes GST; TCC cannot absorb GST internally to advertise a lower price without actually losing 18% of revenue per student; some competitors advertise "fees inclusive of GST" (meaning their base is lower, with GST baked in) — TCC must clearly communicate total cost to avoid comparison confusion; the enrollment confirmation shows both base fee and total (with GST) for transparency
- Discount eligibility is verified before application; the BPL/income certificate must be original or government-digitally-signed; a photocopy is insufficient; the original is verified by the admissions counsellor and a scan is uploaded to the student's document folder; if a student misrepresents their eligibility (claiming BPL discount without valid certificate), the discount is reversed and the full fee balance is due immediately; this is treated as a misrepresentation and noted in the student's record
- The annual fee revision process starts 3 months before the new academic year (January–March); the Accounts team prepares the cost analysis, the Branch Manager adds market intelligence (competitor pricing), and the Director makes the final decision; fee revisions are not arbitrary — they must be supported by a documented cost increase or strategic rationale; a fee increase larger than 10% in a single year requires the Director to brief the franchise owners, as it may affect franchise branch competitiveness
- Franchise branches must use TCC's standard fee structure — they cannot offer lower prices independently; this is a brand standard condition in the franchise agreement; a franchise that charges less than the standard fee is likely undermining the brand's quality positioning; a franchise that charges more is alienating students; franchise pricing deviation complaints trigger a franchise audit; the only permitted deviation is local payment mode (e.g., a franchise in a tier-3 city accepting post-dated cheques where UPI adoption is lower)

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division G*
