# D-17 — Annual Fee Report

> **URL:** `/school/fees/reports/annual/`
> **File:** `d-17-annual-fee-report.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accountant (S3) — full · Principal (S6) — full

---

## 1. Purpose

Year-end complete fee income report — used for the school trust's annual audit, FRA submission (in applicable states), CBSE inspection, and management decision-making on next year's fee revision.

---

## 2. Report Layout

```
Annual Fee Report — 2025–26
[School Name] · [Affiliation No.] · UDISE: [Code]

INCOME FROM FEES:
──────────────────────────────────────────────────────────────────────────────
Fee Head           Billed       Collected    Outstanding   Collection%
Tuition            ₹2,16,00,000 ₹2,04,42,000 ₹11,58,000    94.6%
Development Fee    ₹30,40,000   ₹30,12,000   ₹28,000       99.1%
Admission Fee      ₹18,75,000   ₹18,75,000   ₹0            100%
Lab / Computer     ₹9,52,000    ₹9,12,000    ₹40,000       95.8%
Transport          ₹22,80,000   ₹21,90,000   ₹90,000       96.1%
Annual Day / Misc  ₹4,56,000    ₹4,48,000    ₹8,000        98.2%
Board Exam Fee     ₹1,05,000    ₹1,05,000    ₹0            100%
──────────────────────────────────────────────────────────────────────────────
TOTAL             ₹3,03,08,000 ₹2,89,84,000 ₹13,24,000    95.6%

Concessions Granted:          -₹18,42,000
Waivers:                       -₹2,84,000
RTE Reimbursement:            +₹10,22,400
Late Fee Collected:            +₹3,84,000

NET FEE REVENUE:               ₹2,82,64,400

Student Count: 380 · Average fee per student: ₹74,380/year
```

---

## 3. 3-Year Trend

```
Year          Revenue         Students   Per Student   Growth
2023–24       ₹2,42,18,000    352        ₹68,800       —
2024–25       ₹2,64,82,000    366        ₹72,356       5.2%
2025–26       ₹2,82,64,400    380        ₹74,380       2.8%
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/reports/annual/?year={year}` | Annual report |
| 2 | `GET` | `/api/v1/school/{id}/fees/reports/annual/export/?year={year}` | Export for audit |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
