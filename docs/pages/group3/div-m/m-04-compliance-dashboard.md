# M-04 — Compliance Health Dashboard

> **URL:** `/school/mis/compliance/`
> **File:** `m-04-compliance-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full view · Compliance Officer (S4) — full view · MIS Coordinator (S4) — view and export · Trust/Management (S7) — cross-school compliance view

---

## 1. Purpose

The Compliance Health Dashboard aggregates the status of all regulatory compliance obligations across K-series (and related modules) into a single view. Unlike K-12 (which is the detailed compliance management tool), this MIS view provides:
- A composite compliance health score
- Domain-by-domain health (CBSE, Fire/Safety, RTE, BGV, Data Privacy)
- Critical alerts with days-to-action
- Historical compliance trend (are we improving year-on-year?)
- Inspection readiness assessment

---

## 2. Compliance Health Score

```
COMPLIANCE HEALTH — 27 March 2026
GREENFIELDS SCHOOL — OVERALL SCORE: 88/100 🟡

DOMAIN SCORES:
  Domain                    Score   Status   Trend
  CBSE Affiliation          18/20   ✅        ▲ (was 16/20 last year)
  RTE Compliance            16/20   🟡        ► (2 teachers pending TET)
  Fire & Safety             19/20   ✅        ▲ (NOC renewed Aug 2025)
  Staff BGV & POCSO         17/20   🟡        ► (3 BGV renewals due Aug 2026)
  Data Privacy (DPDPA)      18/20   ✅        ▲ (new — started this year)
  ────────────────────────────────────────────
  TOTAL                     88/100  🟡

SCORE INTERPRETATION:
  90–100: Fully compliant ✅ (CBSE Grade A expected)
  75–89:  Minor gaps — manage proactively 🟡
  60–74:  Significant gaps — immediate action 🔴
  <60:    Critical — escalate to Trust 🚨

YEAR-ON-YEAR TREND:
  2023–24: 81/100
  2024–25: 85/100
  2025–26: 88/100  ▲ Improving ✅
```

---

## 3. Critical Alerts — Next 90 Days

```
CRITICAL ALERTS — Next 90 Days (as of 27 March 2026)

🔴 CRITICAL (action required now):
  None currently 🎉

🟡 HIGH (action required within 30 days):
  ● BGV renewal due: 3 staff (due Aug 2026 — initiate now; 5-month lead time) [K-05]
  ● RTE TET compliance: 2 teachers must obtain TET by Dec 2026 — mid-point check [K-02]
  ● CBSE annual fee submission: 31 Oct 2026 — begin data collection [K-01]

🔵 UPCOMING (30–90 days):
  ● School bus RTO permits: 4 buses expire Aug 2026 — initiate renewal May 2026 [K-08]
  ● FSSAI license renewal: 15 July 2026 (hostel canteen) [K-08]
  ● Annual water quality test: Due June 2026 (IS 10500) [K-04]
  ● POCSO annual training: June 2026 (all staff) [K-05, L-07]
  ● Fire drill: Next scheduled June 2026 [K-03]
  ● CBSE inspection prep: Complete document indexing April 2026 [K-09]

GREEN (no action needed):
  ● Fire NOC: Valid until Sep 2026 ✅
  ● POCSO register: No active cases ✅
  ● 12A/80G exemption: Valid until March 2028 ✅
  ● Structural certificate: Valid until Jan 2027 ✅
```

---

## 4. Inspection Readiness

```
CBSE INSPECTION READINESS — Self-Assessment

Readiness Score: 87/100

DOCUMENT READINESS (K-06):
  67 required documents tracked
  Complete & current: 61/67  ✅
  Expiring soon (<90 days): 3
  Missing/expired: 3 (being addressed)

STAFF COMPLIANCE (K-05, L-series):
  TET compliance: 47/49 (Classes I–VIII teachers) — 2 in process ⚠
  BGV verified: 124/127 — 3 pending renewal ⚠
  POCSO trained (last year): 85/87 (97.7%) ✅

REGISTER COMPLETENESS (K-07):
  32 statutory registers
  Complete & signed: 29/32 ✅
  Needing attention: 3 (visiting teacher register, fire drill register)

INFRASTRUCTURE (K-04):
  Building certificate: ✅
  Fire extinguishers: 44/46 serviced (2 overdue — FE-07, FE-12) ⚠
  Water quality: Last test Jun 2025 — due for next ✅

INSPECTION SIMULATION SCORE:
  Academics:     18/20 ✅
  Infrastructure: 17/20 🟡
  Staff:          17/20 🟡
  Administration: 18/20 ✅
  Financial:      17/20 🟡
  ─────────────────
  Total: 87/100

[Generate CBSE Inspection Package (M-07) →]
```

---

## 5. Compliance Action Tracker

```
OPEN COMPLIANCE ACTIONS — 27 March 2026

Priority  Action                           Owner              Due        Status
HIGH      BGV renewal for 3 staff          Compliance Officer  Aug 2026   Not started ⚠
HIGH      Fire extinguisher FE-07, FE-12   Fire Safety Warden  15 Apr     In progress ✅
HIGH      Visiting teacher register update HR Officer          31 Mar     Due today ⚠
MEDIUM    Water quality test (next cycle)  Compliance Officer  Jun 2026   Scheduled ✅
MEDIUM    CBSE i-EXCEL (2 teachers)        Academic Coord.     Jun 2026   On track ✅
MEDIUM    TET for Mr. Suresh R.            HR Officer          Dec 2026   In process ✅
MEDIUM    Annual structural inspection     Compliance Officer  Jan 2027   Future
LOW       Library expansion certificate    Accounts Officer    Apr 2026   Pending docs ⚠

[7 open actions total: 0 critical · 3 high · 4 medium]
Closed this month: 4 actions ✅
Overdue: 0 ✅

MONTHLY SIGN-OFF: Principal review required by 31 March 2026
[Principal OTP sign-off → K-12] ← Pending ⚠
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/mis/compliance/score/` | Composite compliance health score |
| 2 | `GET` | `/api/v1/school/{id}/mis/compliance/alerts/` | Critical alerts with days-to-action |
| 3 | `GET` | `/api/v1/school/{id}/mis/compliance/inspection-readiness/` | CBSE inspection readiness score |
| 4 | `GET` | `/api/v1/school/{id}/mis/compliance/actions/` | Open compliance action tracker |
| 5 | `GET` | `/api/v1/school/{id}/mis/compliance/trend/` | Year-on-year compliance trend |
| 6 | `GET` | `/api/v1/school/{id}/mis/compliance/export/` | Export compliance dashboard PDF |

---

## 7. Business Rules

- The compliance health score is calculated nightly (not real-time) based on the state of all K-module and L-module compliance items; it is a lagging indicator — documents that expire today will appear in tomorrow's score
- A score below 75 triggers an automatic email to the Principal and the Trust/Management; this ensures that deteriorating compliance doesn't go unnoticed
- The "open actions" list is never auto-closed by the system; only a human (the assigned owner) can mark an action as complete; this prevents gaming the compliance score by auto-closing items
- Inspection readiness scores are conservative — the self-assessment is designed to highlight gaps, not to generate a flattering number; a school that scores 90/100 on the MIS self-assessment should genuinely be ready for an unannounced CBSE inspection
- The compliance trend (year-on-year improvement) is the most important metric for the Trust board; it shows whether the school is building a culture of compliance or just firefighting; a school that improves by 3+ points annually is demonstrating systemic improvement

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division M*
