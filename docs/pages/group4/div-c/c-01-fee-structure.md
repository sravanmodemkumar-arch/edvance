# C-01 — Fee Structure & AFRC Compliance

> **URL:** `/college/fees/structure/`
> **File:** `c-01-fee-structure.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Finance Manager (S4) · Registrar (S4) · Principal/Director (S6) — approve

---

## 1. Purpose

College fee structures are regulated by the AFRC (Admissions and Fee Regulatory Committee) in Telangana and equivalent bodies in other states. The fee structure must:
- Be within AFRC-approved limits for each programme and quota
- Be displayed publicly (AICTE, AFRC, college website requirements)
- Distinguish between tuition and non-tuition components (only tuition is capped by AFRC)
- Be uniform within a quota (no individual negotiation allowed)

---

## 2. Fee Structure — 2026–27

```
FEE STRUCTURE — APPROVED BY AFRC (Telangana) 2026–27
Greenfields College of Engineering

PROGRAMME: B.Tech (All branches)

                              Convener Quota    Management Quota
AFRC Approved Tuition Fee:    ₹85,000/year      ₹1,40,000/year
Development Fee (non-tuition): ₹10,000/year      ₹10,000/year
Exam Fee (JNTU):              ₹2,000/year       ₹2,000/year
Library Fee:                  ₹2,000/year       ₹2,000/year
Lab Fee:                      ₹3,000/year       ₹3,000/year
Caution Deposit (refundable): ₹5,000 (once)     ₹5,000 (once)
─────────────────────────────────────────────────────────────
Total (Year 1 — excl. deposit):₹1,02,000/year   ₹1,57,000/year
Total (Year 2–4):              ₹1,02,000/year   ₹1,57,000/year

AFRC COMPLIANCE:
  ✅ Tuition fee within AFRC cap (₹85,000 conv / ₹1,40,000 mgmt)
  ✅ No capitation fee collected
  ✅ Fee structure published on college website ✅
  ✅ AFRC certificate available (K-series compliance docs)

HOSTEL FEE (if applicable):
  AC Double-occupancy: ₹80,000/year
  Non-AC: ₹55,000/year
  Note: Hostel fee is separate from academic fee; NOT AFRC regulated

FEE PAYMENT SCHEDULE:
  Semester 1: 50% of annual fee → by 15 August
  Semester 2: 50% of annual fee → by 15 January
  (Students may request annual lump-sum payment for discount consideration)
```

---

## 3. Fee Display Requirements

```
PUBLIC FEE DISPLAY (AICTE/AFRC mandatory):

Published on:
  ✅ College website (updated annually) — Fees page
  ✅ AICTE portal (College profile → Fee section)
  ✅ Admission prospectus (printed + digital)
  ✅ Notice board at admissions office
  ✅ AFRC website (AFRC publishes approved fee for all colleges)

PROHIBITED:
  ✗ Charging more than AFRC-approved fee (criminal offence — TS CapitationFee Act)
  ✗ Demanding "donations", "building fund", "development fund" above AFRC limit
  ✗ Differential pricing within the same quota (all management quota students
    pay the same; no individual negotiation)
  ✗ Undisclosed additional charges (every charge must be in the published structure)

AICTE MANDATORY DISCLOSURE:
  Fee structure must be on AICTE dashboard (AICTE portal login)
  Annual update required by 30 June each year
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/fees/structure/` | Fee structure by year and quota |
| 2 | `PUT` | `/api/v1/college/{id}/fees/structure/` | Update fee structure (annual) |
| 3 | `GET` | `/api/v1/college/{id}/fees/structure/afrc-compliance/` | AFRC compliance status |
| 4 | `GET` | `/api/v1/college/{id}/fees/structure/public/` | Public-facing fee display (no auth) |

---

## 5. Business Rules

- AFRC sets the maximum fee; the college can charge LESS but not more; many colleges charge exactly the AFRC maximum; charging above AFRC is a criminal offence under the Telangana Capitation Fee Act and can result in criminal prosecution of the management
- Development fee, library fee, lab fee, and exam fee are components ABOVE tuition; AFRC does not cap these ancillary fees but expects them to be "reasonable and non-exploitative"; AICTE can investigate if these are used to circumvent tuition fee caps
- Fee structure must be fixed at the start of the academic year; it cannot be changed mid-year after admissions are done; students who were admitted based on the published fee structure have a contractual right to that fee for their programme duration (fee revision is prospective — only for new admissions)

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division C*
