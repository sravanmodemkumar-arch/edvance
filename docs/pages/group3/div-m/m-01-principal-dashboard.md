# M-01 — Principal Executive Dashboard

> **URL:** `/school/mis/dashboard/`
> **File:** `m-01-principal-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full dashboard · Vice Principal (S5) — operational panels only · MIS Coordinator (S4) — view and export

---

## 1. Purpose

The Principal's Executive Dashboard is the operational and strategic control centre — a single page where the Principal sees the live health of the school across academics, finance, compliance, welfare, and HR. It is designed for a 5-minute morning review before the school day starts, and a 15-minute weekly deep-dive.

Design philosophy:
- Actionable: Every metric has a drill-down and a suggested action
- Red/Amber/Green (RAG) status on all key indicators — no interpretation needed at a glance
- Today's priorities surface automatically based on rule engine
- Comparison: Current month vs last month, current year vs last year

---

## 2. Today's Snapshot Panel

```
PRINCIPAL DASHBOARD — 27 March 2026 (Friday)
GREENFIELDS SCHOOL, Hyderabad

┌─────────────── TODAY'S SNAPSHOT ───────────────────────────────────────────┐
│                                                                             │
│  🟢 School open  |  Students present: 1,184 / 1,240 (95.5%)               │
│  🟢 Staff present: 123 / 127 (96.9%)  |  4 absent (3 approved, 1 unintimated)│
│                                                                             │
│  TODAY'S ALERTS (requires action):                                          │
│  🔴 Substitute gap: VI-C, Period 8 — no free teacher [Action →]            │
│  🟡 Ms. Radha N. (Art): absent, no intimation — 3rd this month [View →]    │
│  🟡 Fee reminder: 42 students with fees due today (D-01) [View →]          │
│  🟢 No compliance alerts today                                              │
│                                                                             │
│  UPCOMING THIS WEEK:                                                        │
│  Mon 30 Mar: PTM — Class VI (F-05)                                         │
│  Tue 31 Mar: Fee due date — Term 3 (D-02)                                  │
│  Thu 2 Apr:  BGV renewal due — Mr. Suresh R. (K-05)                       │
│  Fri 3 Apr:  CBSE inspection prep meeting (K-09)                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Academic Pulse

```
┌─────────────── ACADEMIC PULSE ──────────────────────────────────────────────┐
│                                                                              │
│  STUDENT PERFORMANCE — Unit Test 1 (Feb 2026):                              │
│  Overall pass rate: 89.4%  |  School average score: 71.2/100               │
│                                                                              │
│  Subject performance (school-wide average):                                  │
│  Mathematics:    68.4% ⚠ (below target 70%)  [Drill-down →]                │
│  Science:        74.1% ✅                                                    │
│  Social Science: 72.8% ✅                                                    │
│  English:        76.3% ✅                                                    │
│  Languages:      69.1% ⚠ (Telugu — improving, +2% vs last test)            │
│                                                                              │
│  CLASSES BELOW 70% AVERAGE (any subject):                                   │
│  VII-C: Mathematics 61.2% — [Remedial arranged by HOD] ✅                   │
│  IX-B:  English 64.8% — [Flagged to HOD English — pending action] ⚠        │
│  XI-A:  Physics 58.3% — [Class XI Chemistry also weak — pattern?] 🔴       │
│                                                                              │
│  BOARD EXAM READINESS (Class X, XII):                                       │
│  Class X: 3 students below 33% in at least 1 subject (at risk) [View →]    │
│  Class XII: 2 students at risk (Physics, Chemistry) [View →]                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Financial Health Panel

```
┌─────────────── FINANCIAL HEALTH ────────────────────────────────────────────┐
│                                                                              │
│  FEE COLLECTION — March 2026 (Term 3):                                      │
│  Billed: ₹18,24,000  |  Collected: ₹14,18,000 (77.7%)  |  Outstanding: ₹4,06,000│
│  Defaulters >90 days: 12 students (₹1,82,400) [View D-01 →]               │
│  Today's collections: ₹34,500 (18 transactions)                             │
│                                                                              │
│  ANNUAL FEE COLLECTION (2025–26 YTD):                                       │
│  Target: ₹2,04,00,000  |  Collected: ₹1,86,20,000 (91.3%)                 │
│  Outstanding: ₹17,80,000 — 60-day collection projection: ₹14,20,000       │
│                                                                              │
│  PAYROLL (March 2026): ₹47,32,840 disbursed on 7 Mar ✅                    │
│  EPF challan: ₹5,18,640 — submitted to EPFO ✅                              │
│                                                                              │
│  BUDGET vs ACTUAL (2025–26, 11 months):                                     │
│  Revenue: 98.4% of budget ✅                                                 │
│  Expenses: 94.2% of budget ✅ (₹3.2L underspent — training budget underused)│
│  Net surplus (projected): ₹8,40,000 (vs budget ₹6,20,000) ✅               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Compliance Health Panel

```
┌─────────────── COMPLIANCE HEALTH ───────────────────────────────────────────┐
│                                                                              │
│  OVERALL COMPLIANCE SCORE: 88/100 🟡                                        │
│  (K-12 composite — see K-module for detail)                                 │
│                                                                              │
│  CRITICAL ALERTS (P0):                                                      │
│  ✅ Fire NOC: Valid until 15 Sep 2026 (170 days remaining)                  │
│  ✅ BGV: 124/127 staff verified  |  3 pending renewal (due Aug 2026)        │
│  ✅ POCSO register: 0 active cases                                           │
│                                                                              │
│  UPCOMING RENEWALS (next 90 days):                                          │
│  🟡 School bus RTO permits: 4 buses — Aug 2026 (bulk renewal) [K-08]       │
│  🟡 CBSE Annual fee submission: 31 Oct 2026 [K-01]                         │
│  🟢 Building structural certificate: Jan 2027 (annual) [K-04]              │
│                                                                              │
│  OPEN COMPLIANCE ACTIONS: 7 (K-09)                                         │
│    Critical (30-day): 0                                                     │
│    High (60-day): 2                                                         │
│    Medium: 5                                                                 │
│  [View all open actions →]                                                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Welfare & Safeguarding Panel

```
┌─────────────── WELFARE & SAFEGUARDING ──────────────────────────────────────┐
│                                                                              │
│  ACTIVE WELFARE FLAGS: 8 students (J-11 triage dashboard) [View →]         │
│  ● 3 students: Attendance + grade drop pattern                              │
│  ● 2 students: Discipline incidents + counsellor referral                   │
│  ● 3 hostel students: Wellness check requested by warden                    │
│                                                                              │
│  COUNSELLING LOAD: 14 active cases (J-01) [Anonymous count only]           │
│  GRIEVANCES OPEN: 3 (J-05) — 1 overdue (SLA breach) ⚠ [View →]           │
│  POCSO: 0 active cases ✅                                                    │
│  ANTI-RAGGING: 0 active cases ✅                                             │
│                                                                              │
│  SPECIAL NEEDS (CWSN): 4 students with IEP                                 │
│  Board exam accommodations: 1 application pending (deadline 30 Sep 2026)   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. HR Quick Panel

```
┌─────────────── HR QUICK VIEW ───────────────────────────────────────────────┐
│                                                                              │
│  STAFF: 127 total  |  Vacancies: 2 open (History, Substitute pool) [L-08]  │
│  On notice: 1 (Ms. Priya Iyer — LWD 14 Apr 2026) [L-10]                   │
│  Probation reviews due: 1 (Ms. Anita Rao — Sep 30, 2026)                   │
│  PIP active: 1 (Mr. Vijay P. — review 30 Jul 2026) [L-06]                 │
│                                                                              │
│  TRAINING COMPLIANCE:                                                        │
│  POCSO 2025 session: 85/87 (97.7%) ⚠ — 2 pending [L-07]                  │
│  CBSE i-EXCEL: 12/12 required staff ✅                                      │
│                                                                              │
│  APPRAISAL CYCLE: Feb–Apr 2026 (in progress)                               │
│  VP submissions: 38/52 complete ⚠ — due 30 Apr [L-06]                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/mis/dashboard/` | Full principal dashboard data |
| 2 | `GET` | `/api/v1/school/{id}/mis/dashboard/alerts/` | Today's priority alerts |
| 3 | `GET` | `/api/v1/school/{id}/mis/dashboard/academic-pulse/` | Academic performance snapshot |
| 4 | `GET` | `/api/v1/school/{id}/mis/dashboard/financial/` | Financial health snapshot |
| 5 | `GET` | `/api/v1/school/{id}/mis/dashboard/compliance/` | Compliance health snapshot |
| 6 | `GET` | `/api/v1/school/{id}/mis/dashboard/welfare/` | Welfare and safeguarding snapshot |
| 7 | `GET` | `/api/v1/school/{id}/mis/dashboard/hr/` | HR quick view |

---

## 9. Business Rules

- The dashboard is read-only — it aggregates, it does not originate data; every number links back to the source module where the actual data is managed; clicking a metric takes the Principal to the relevant module
- Alert prioritisation: P0 (red) alerts are shown at the top regardless of category; a P0 alert (e.g., POCSO case, lapsed fire NOC, no substitute coverage) is never buried
- The dashboard refreshes every 15 minutes (not real-time) to avoid database load; for today's attendance, it pulls from E-01 attendance log as at last sync; real-time attendance is available in E-01 directly
- Principals of multi-branch schools see their own school's dashboard by default, with a school selector to switch; the Trust dashboard (M-06) shows the cross-school view
- All dashboard data is read-only for VP (no edit actions); MIS Coordinator can generate exports from dashboard but cannot modify underlying data; this separation of roles ensures the dashboard reflects actual operational data without dashboard-layer manipulation

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division M*
