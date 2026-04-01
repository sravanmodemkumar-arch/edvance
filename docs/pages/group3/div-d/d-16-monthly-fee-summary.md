# D-16 — Monthly Fee Summary

> **URL:** `/school/fees/reports/monthly/`
> **File:** `d-16-monthly-fee-summary.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accountant (S3) — full · Principal (S6) — full

---

## 1. Purpose

Month-wise fee collection summary — comparing expected revenue (billed) vs collected vs outstanding vs written-off (waivers). Used for monthly review meetings and for the school management committee.

---

## 2. Report Layout

```
Monthly Fee Summary — October 2026

                  Billed      Collected   Outstanding   Waived    Write-off
────────────────────────────────────────────────────────────────────────────
Q3 Tuition       ₹20,90,000  ₹14,18,000  ₹6,72,000    ₹21,000    ₹0
Late Fees             ₹0      ₹88,000       ₹0          ₹2,000     ₹0
Misc / Other       ₹84,000    ₹72,000      ₹12,000       ₹0        ₹0
────────────────────────────────────────────────────────────────────────────
TOTAL            ₹21,74,000  ₹14,78,000  ₹6,84,000    ₹23,000    ₹0
Collection %:       68.0%

YTD (Apr–Oct 2026):
  Billed: ₹62,48,000  ·  Collected: ₹52,42,000  ·  Outstanding: ₹10,06,000
  Collection Rate: 83.9%

RTE Reimbursement (Oct–Dec 2026 claim): ₹2,55,600 (filed 31 Jan 2027)
```

---

## 3. Chart View

- Line chart: Monthly collection vs target (Chart.js)
- Bar chart: Outstanding by class

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/reports/monthly/?year={year}&month={m}` | Monthly summary |
| 2 | `GET` | `/api/v1/school/{id}/fees/reports/monthly/export/?year={year}&month={m}` | Export PDF |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
