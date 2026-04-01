# A-01 — Director / Owner Dashboard

> **URL:** `/coaching/admin/dashboard/`
> **File:** `a-01-director-dashboard.md`
> **Priority:** P1
> **Roles:** Director/Owner (K7) · Operations Director (K6)

---

## 1. Executive KPI Banner

```
TOPPERS COACHING CENTRE (TCC) — DIRECTOR DASHBOARD
As of 30 March 2026  |  Mr. Vikram Reddy, Director

  ┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
  │  1,840       │  ₹48.2L      │  24          │  AIR ~312    │  12          │  3           │
  │  Total       │  Revenue MTD │  Active      │  Avg mock    │  Dropout     │  BGV         │
  │  Students    │  (tgt ₹52L)  │  Batches     │  rank (CGL)  │  Risk ⚠️     │  Pending     │
  │              │  ▼ 7.3%      │              │  top 5 batch │  flagged     │  (faculty)   │
  └──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘

ALERT STRIP:
  🔴 BGV pending: Rajesh Varma (GK), Meena Iyer (English), Sunil Das (Reasoning) — action req.
  🟡 Revenue gap: ₹3.8L short of monthly target — 2 batch EMIs overdue (42 students)
  🟡 12 dropout-risk students flagged by system (3+ absences + fee overdue)
  🟢 SSC CGL Morning batch: 18/240 students scored >180/200 in last mock — on track
```

---

## 2. Branch Performance Table

```
BRANCH PERFORMANCE SUMMARY — MARCH 2026

  ┌─────────────────────┬──────────┬─────────┬──────────────┬────────────┬─────────────┐
  │ Branch              │ Students │ Faculty │ Revenue MTD  │ Attendance │ Status      │
  ├─────────────────────┼──────────┼─────────┼──────────────┼────────────┼─────────────┤
  │ Main (Himayatnagar) │    820   │   18    │  ₹22.4L      │  82.6%     │ ✅ On track │
  │ Dilsukhnagar        │    480   │   11    │  ₹13.1L      │  79.4%     │ ✅ On track │
  │ Kukatpally          │    360   │    8    │  ₹9.2L       │  77.1%     │ ⚠️ Low att. │
  │ Online (TCC Live)   │    180   │    3    │  ₹3.5L       │  68.3%     │ ⚠️ Low att. │
  ├─────────────────────┼──────────┼─────────┼──────────────┼────────────┼─────────────┤
  │ TOTAL               │  1,840   │   40    │  ₹48.2L      │  79.9%     │             │
  └─────────────────────┴──────────┴─────────┴──────────────┴────────────┴─────────────┘

  Branch Mgr (Main): Ms. Priya Sharma    |  Academic Dir: Mr. Suresh Kumar
  Dilsukhnagar Mgr:  Mr. Anil Verma      |  Kukatpally Mgr: Ms. Kavitha Rao
```

---

## 3. Revenue Trend — Last 6 Months

```
REVENUE TREND (₹ in Lakhs)   Oct 2025 – Mar 2026

  60 ┤
  55 ┤                  ████
  52 ┤  ────────────────────────────────── Target ₹52L
  50 ┤  ████            ████  ████
  48 ┤                              ████ ← Mar (₹48.2L, ongoing)
  45 ┤        ████
  40 ┤
     └────────────────────────────────────
       Oct    Nov    Dec    Jan    Feb    Mar

  Oct: ₹50.1L  ✅   |  Jan: ₹53.8L  ✅
  Nov: ₹44.6L  ⚠️   |  Feb: ₹51.4L  ✅
  Dec: ₹55.2L  ✅   |  Mar: ₹48.2L  ⚠️ (month not closed)

  YTD Revenue (Oct–Feb): ₹255.1L  |  Target: ₹260L  |  Gap: ₹4.9L
  New admissions this month: 38    |  Renewals: 214   |  Dropouts: 7
```

---

## 4. Today's Operations Snapshot

```
TODAY — MONDAY, 30 MARCH 2026

CLASSES TODAY:
  ┌──────────────────────────────┬─────────────┬──────────┬──────────────────────┐
  │ Batch                        │ Time        │ Faculty  │ Room / Status        │
  ├──────────────────────────────┼─────────────┼──────────┼──────────────────────┤
  │ SSC CGL Morning              │ 06:30–09:30 │ S. Kumar │ Hall A  ✅ Started   │
  │ Banking Morning              │ 07:00–10:00 │ R. Pillai│ Hall B  ✅ Started   │
  │ Foundation 9-10 (Morning)    │ 08:00–11:00 │ D. Naik  │ Room 4  ✅ Started   │
  │ SSC CHSL Evening             │ 17:00–20:00 │ P. Rao   │ Hall A  ⏳ Upcoming  │
  │ RRB NTPC Weekend (Makeup)    │ 18:00–21:00 │ K. Sharma│ Hall C  ⏳ Upcoming  │
  │ Dropper Batch (Special)      │ 10:00–13:00 │ M. Reddy │ Room 2  ✅ Started   │
  └──────────────────────────────┴─────────────┴──────────┴──────────────────────┘

ADMISSIONS TODAY: 3 walk-ins (2 SSC CGL, 1 Banking) | Counselling slots: 5 (2 pending)
TESTS SCHEDULED:  SSC CGL Morning — Mock #14 at 09:00 (200 students registered)
SUPPORT TICKETS:  4 open (2 fee, 1 material, 1 login issue)
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/admin/dashboard/` | Full director dashboard payload |
| 2 | `GET` | `/api/v1/coaching/{id}/admin/dashboard/kpis/` | KPI tiles only (for real-time refresh) |
| 3 | `GET` | `/api/v1/coaching/{id}/admin/dashboard/branches/` | Branch performance table |
| 4 | `GET` | `/api/v1/coaching/{id}/admin/dashboard/revenue/trend/` | 6-month revenue trend |
| 5 | `GET` | `/api/v1/coaching/{id}/admin/dashboard/operations/today/` | Today's class schedule & snapshot |
| 6 | `GET` | `/api/v1/coaching/{id}/admin/alerts/` | Active alert strip items |
| 7 | `PATCH` | `/api/v1/coaching/{id}/admin/alerts/{alert_id}/dismiss/` | Dismiss a specific alert |

---

## 6. Business Rules

- The Director dashboard is the single source of truth for the organisation; all KPIs visible here are computed in real time from underlying transactional data — student admissions, fee collections, attendance logs, and mock test scores — and any discrepancy between branch-level reports and this dashboard must be investigated using the audit trail; directors who rely on branch manager WhatsApp summaries rather than this dashboard risk acting on stale or selectively presented data.
- Revenue MTD vs target comparison is calculated against a pro-rated daily target; on the 30th of a 31-day month, the system calculates expected revenue as (30/31) × monthly target, not the full ₹52L; this avoids false alarms at the start of the month while still flagging genuine underperformance; the 7.3% gap visible today reflects a real shortfall driven by 42 students on delayed EMI — the system identifies them automatically.
- The dropout-risk flag is triggered by a composite score: a student with ≥3 consecutive absences AND a fee overdue ≥15 days AND a mock test score declining >15% over the last 3 tests is marked high-risk; students meeting only 2 of 3 conditions are medium-risk; the Director dashboard shows only the high-risk students; branch managers see both; the Academic Director sees the academic dimension of risk separately — this layered visibility ensures each stakeholder acts on the signals within their authority.
- BGV (Background Verification) pending status on faculty members is a compliance and reputational risk; a coaching centre that employs faculty without completed BGV exposes itself to liability especially for minor students in Foundation batches; the Director must enforce a hard policy that no faculty member interacts with students before BGV is cleared; EduForge enforces this by greying out the faculty member's schedule-creation capability until HR marks BGV complete.
- Franchise oversight is surfaced at the Director level specifically because franchise branch quality directly affects the TCC brand; if a franchise branch in Warangal delivers poor results, students in Hyderabad will hear about it; the Director dashboard therefore includes a franchise health indicator (not shown in this view but accessible via the Franchise tab) that aggregates result quality, fee collection compliance, and brand guideline adherence into a single franchise health score, reviewed monthly.

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division A*
