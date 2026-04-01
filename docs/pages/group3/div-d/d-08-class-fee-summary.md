# D-08 — Class-wise Fee Summary

> **URL:** `/school/fees/class-summary/`
> **File:** `d-08-class-fee-summary.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Fee Clerk (S2) — read · Accountant (S3) — full · Academic Coordinator (S4) — read · Principal (S6) — full

---

## 1. Purpose

Shows the Accountant and Principal a bird's-eye view of fee collection status across all classes — which classes have the most outstanding dues, which installment is currently due, and what percentage of expected revenue has been collected. Useful for:
- Identifying which classes need follow-up (D-10 demand notices)
- Comparing collection progress week-over-week during peak collection periods
- Providing a quick dashboard number to the Principal each morning during fee season

---

## 2. Page Layout

### 2.1 Header
```
Class-wise Fee Summary — 2026–27             Q3 (October 2026)
Total Billed: ₹1,24,84,000  ·  Collected: ₹92,18,000 (73.8%)  ·  Outstanding: ₹32,66,000
```

### 2.2 Class-wise Table
| Class | Students | Q3 Billed | Q3 Collected | Q3 Outstanding | % Collected | Defaulters | Action |
|---|---|---|---|---|---|---|---|
| Nursery | 40 | ₹1,40,000 | ₹1,40,000 | ₹0 | 100% | 0 | — |
| LKG | 38 | ₹1,33,000 | ₹1,19,700 | ₹13,300 | 90% | 3 | [Remind] |
| Class I | 41 | ₹1,64,000 | ₹1,40,780 | ₹23,220 | 85.8% | 5 | [Remind] |
| Class IX-A | 38 | ₹2,09,000 | ₹1,46,300 | ₹62,700 | 70% | 8 | [Demand Notice] |
| Class XI-A | 38 | ₹2,66,000 | ₹1,77,300 | ₹88,700 | 66.7% | 12 | [Demand Notice] |
| Class XI-B | 36 | ₹2,52,000 | ₹1,51,200 | ₹1,00,800 | 60% | 15 | [Demand Notice] |

---

## 3. Installment Progress View

```
Installment Collection Progress — 2026–27

Q1 (Apr 2026):  ████████████████████░░  92% collected  ₹2,18,000 outstanding
Q2 (Jul 2026):  ██████████████████░░░░  88% collected  ₹1,84,000 outstanding
Q3 (Oct 2026):  █████████████░░░░░░░░░  74% collected  ₹32,66,000 outstanding  ← Current
Q4 (Jan 2027):  ░░░░░░░░░░░░░░░░░░░░░░  0%  (not yet due)
```

---

## 4. Quick Actions

[Remind] on a class row → sends WhatsApp reminders to all parents in that class with outstanding fees (auto-fetches from D-09 defaulter list for that class).

[Demand Notice] → opens D-10 for that class.

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/class-summary/?year={year}&installment={q}` | Class-wise summary |
| 2 | `GET` | `/api/v1/school/{id}/fees/class-summary/installment-progress/?year={year}` | Installment progress |
| 3 | `GET` | `/api/v1/school/{id}/fees/class-summary/export/?year={year}` | Export class-wise summary |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
