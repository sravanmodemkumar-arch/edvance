# D-03 — Late Fee Configuration

> **URL:** `/school/fees/late-fee/`
> **File:** `d-03-late-fee-config.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accountant (S3) — draft · Principal (S6) — approve

---

## 1. Purpose

Configures the rules for late fee charges — when fees are not paid by the due date. Late fees serve as an incentive for timely payment; most Indian schools charge ₹50–₹200/month as late fee after a grace period.

This page also manages one-off late fee waivers (distinct from full fee waivers in D-11) — for example, waiving late fee for students who were absent during the collection period due to medical emergency.

---

## 2. Late Fee Policy Configuration

```
Late Fee Policy — 2026–27

Grace Period:         15 days after due date (no late fee during grace period)
Late Fee Type:        ○ Per Day  ●  Per Month (lump-sum after grace)
Late Fee Amount:      ₹100 per month (or part thereof) after grace period
Maximum Late Fee:     ₹500 (cap per installment)
Applies To:           All fee heads  OR  Tuition only (configurable)
Exemptions:           RTE students — never charged late fee
                     Students with active fee waiver (D-11) — late fee also waived

FRA Note: Some state FRAs cap late fee at ₹50–₹100/month. System checks.
```

---

## 3. Late Fee Schedule Display

```
Example: Q1 installment due April 1, 2026

April 1–15 (Grace):     No late fee
April 16–30:            ₹100 late fee
May 1–31:               ₹200 late fee (cumulative)
June 1–30:              ₹300 late fee (cumulative, max ₹500)
```

---

## 4. Auto-Application

Late fee is auto-computed by the system:
- When the Accountant opens D-07 Student Fee Ledger, outstanding late fees are shown
- When fee collection (D-04) is processed, late fee is automatically included in the total
- Parent portal shows outstanding fee = installment due + late fee (clearly labeled)

---

## 5. One-off Waiver

For exceptional cases (hospitalization, natural disaster, etc.):

```
Late Fee Waiver Request — Arjun Sharma (XI-A)

Outstanding Late Fee: ₹200 (Q4 Jan 2026 installment — 2 months late)
Reason for Waiver: Student was hospitalised Feb 1–15 (hospital certificate submitted)
Requested By: Class Teacher / Parent
Approval Required: Accountant (up to ₹200)  ·  Principal (above)
[Approve Waiver]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/late-fee-config/?year={year}` | Current late fee policy |
| 2 | `PATCH` | `/api/v1/school/{id}/fees/late-fee-config/{year}/` | Update policy (pending Principal approval) |
| 3 | `POST` | `/api/v1/school/{id}/fees/late-fee/waive/` | Request + record late fee waiver |
| 4 | `GET` | `/api/v1/school/{id}/fees/late-fee/outstanding/?class_id={id}` | Students with outstanding late fees |

---

## 7. Business Rules

- Late fee on late fee is not permitted — late fee accrues only on the original installment amount
- Late fee is waived automatically if the delay is caused by bank transfer failure (online payment attempt documented in D-05)
- CBSE prohibition: Schools cannot withhold result/report card solely for non-payment of late fee (only the TC can potentially be held for outstanding dues, with Principal override)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
