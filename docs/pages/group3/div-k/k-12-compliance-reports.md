# K-12 — Compliance Dashboard & Reports

> **URL:** `/school/compliance/reports/`
> **File:** `k-12-compliance-reports.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full dashboard · Compliance Officer (S4) — manage and action · Administrative Officer (S3) — document submissions

---

## 1. Purpose

The master compliance dashboard and report generator for Division K — aggregates compliance status across all sub-modules and generates a single view of the school's overall compliance health. The Principal uses this as the single source of truth for compliance oversight.

---

## 2. Compliance Health Dashboard

```
Compliance Health Dashboard — GREENFIELDS SCHOOL
27 March 2026  ·  Compliance Officer: Ms. Rekha Sharma

Overall compliance score: 88/100  ✅ Good

┌──────────────────────────────────────────────────────────────────────────────┐
│  Module              Score   Status   Critical Items                         │
│  CBSE Affiliation    22/25   ⚠️        Library area, History teacher TET     │
│  RTE Compliance      23/25   ⚠️        4 parent affidavits pending (minor)   │
│  Fire Safety         14/15   ⚠️        NOC renewal due in 34 days            │
│  Infrastructure      15/15   ✅        All clear                              │
│  Staff BGV           14/15   ⚠️        Raju Kumar (driver) BGV overdue       │
│  Documents           9/10    ⚠️        Fire NOC renewal pending              │
│  Registers           9/10    ⚠️        Visiting teacher register missing     │
│  NOC & Permits       8/10    ⚠️        Fire NOC renewal + hostel NOC (64d)  │
│  Audits              10/10   ✅        All clear; next audit June 2026        │
│  DPDPA               9/10    ⚠️        6 pending enrollment consents         │
│  Calendar (220 days) 10/10   ✅        220 days on track                     │
│                                                                              │
│  Overall: 143/155 = 92.3% — Interpretation: Good (above 85% = Good)        │
└──────────────────────────────────────────────────────────────────────────────┘

Priority actions this week:
  P0: None
  P1: Fire NOC renewal — application due 5 April
  P1: Raju Kumar driver BGV renewal — overdue (remove from duty until done)
  P2: Visiting teacher register — create and log last 3 months
  P2: 6 enrollment consents — follow up with parents
```

---

## 3. Open Compliance Actions

```
Open Compliance Actions — All Modules

#   Action                               Owner           Deadline      Priority   Status
1   Fire NOC renewal application         Admin Officer   5 Apr 2026    P1         ⏳ In process
2   FE-07 extinguisher replacement       Maintenance     28 Mar 2026   P1         ✅ Done today
3   Emergency lighting (GF West) repair  Maintenance     28 Mar 2026   P1         ⏳ Scheduled
4   Raju Kumar (driver) BGV renewal      Admin Officer   Immediate     P1         ⏳ Not started
5   Visiting teacher register — create   Admin Officer   30 Apr 2026   P2         ⬜ Not started
6   6 enrollment consents — follow up    Admin Officer   15 Apr 2026   P2         ⬜ Not started
7   Library renovation (CBSE condition)  Principal       By Mar 2027   P3         ⬜ Planning
8   History teacher TET training         HR/L module     By Dec 2026   P2         ⏳ Teacher enrolled
9   Anti-ragging 4 parent affidavits     Class Teacher   15 Apr 2026   P3         ⬜ Reminder sent

[Mark action complete]  [Reassign owner]  [Change deadline]
```

---

## 4. CBSE Affiliation Annual Submission Checklist

```
CBSE Annual Submissions — 2026–27

Annual Submission                      Deadline        Status          Submitted
Fee structure to CBSE (OASIS)          31 Oct 2026     ⬜ Pending       —
Annual report to CBSE                  31 Oct 2026     ⬜ Pending       —
UDISE data (state/MHRD portal)         30 Sep 2026     ⬜ Pending       —
LOC (List of Candidates) for X/XII     CBSE portal schedule ⬜ Pending  —
Exam fee collection return             Post-exam       ⬜ Pending       —
RTE reimbursement claim to DEO         30 Apr 2026     ✅ Submitted     30 Apr 2026
SMC annual report to DEO               Jun 2026        ⬜ Pending       —

Previous year submissions (2025–26):
  Fee structure: ✅ Filed 28 Oct 2025
  UDISE: ✅ Filed 25 Sep 2025
  LOC: ✅ Filed as per CBSE schedule
  RTE reimbursement: ✅ Filed 30 Apr 2025

[Set calendar reminders for all 2026–27 submissions]
```

---

## 5. Annual Compliance Calendar (Key Dates)

```
Compliance Calendar — 2026–27

Month    Date    Event                                         Action
Apr      30      RTE reimbursement claim to DEO               ✅ Done
May       1      Building safety cert renewal (schedule now)  [Schedule engineer visit]
Jun       1      FSSAI food licence renewal — initiate        [Apply by 15 Aug]
Jun      22      Annual POCSO + DPDPA training for all staff  [Schedule]
Jun      30      Staff BGV renewals due this year              [Process]
Aug       1      School bus permit renewal — apply             [Apply for all 5 buses]
Sep      30      UDISE annual data submission                  [Prepare data]
Oct      31      CBSE fee structure submission (OASIS)         [Prepare by 15 Oct]
Oct      31      CBSE annual report                            [Prepare by 15 Oct]
Nov      30      Financial audit for FY 2025–26 — complete    [Appoint auditors by Sep]
Dec      31      TET deadline for 5 pending teachers           [Monitor]
Mar      31      School calendar 220 days completion           [Track monthly]
```

---

## 6. Principal's Compliance Sign-Off (Monthly)

```
Principal Monthly Compliance Review — March 2026

I, Ms. Meena Rao, Principal of GREENFIELDS SCHOOL, have reviewed the compliance
status for March 2026 and certify the following:

  ✅ School was in session for [23] working days this month (cumulative: 210/220)
  ✅ Attendance registers have been maintained and are accurate
  ✅ No new POCSO or major discipline incidents unreported
  ⚠️ Fire NOC renewal in process — application to be filed by 5 April 2026
  ⚠️ Staff BGV renewal (driver) — action initiated
  ✅ Student fee collection in compliance with CBSE-filed fee structure
  ✅ No capitation fee collected
  ✅ RTE students: zero fees charged
  ✅ Data breach: None this month

Principal signature: _______________  Date: 31 March 2026

[Principal OTP sign-off]  [Export monthly compliance certificate]
```

---

## 7. NAAC / ISO (Optional — For Schools Pursuing Accreditation)

```
Quality Accreditation (Optional Track)

Some private schools pursue ISO 9001 (Quality Management) or NAAC (for +2 colleges).
EduForge supports documentation for these but does not mandate them.

If school has ISO 9001:
  Certification body: [___]  ·  Valid until: [___]
  Internal audit schedule: [___]
  Non-conformance log: [linked to K-09 audit module]

If school is pursuing NAAC (for schools with Class XII — A+ rating):
  Self-study report (SSR) generation: [EduForge can export data for SSR]
  Peer team visit preparation: Similar to CBSE inspection readiness

Note: Most CBSE schools do not pursue NAAC (which is primarily for colleges);
  they may pursue ISO 9001 for process quality differentiation.
  These are optional; compliance health score in K-12 covers mandatory items only.
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/compliance/reports/dashboard/` | Overall compliance dashboard |
| 2 | `GET` | `/api/v1/school/{id}/compliance/reports/actions/` | Open compliance action list |
| 3 | `PATCH` | `/api/v1/school/{id}/compliance/reports/actions/{id}/complete/` | Mark action complete |
| 4 | `GET` | `/api/v1/school/{id}/compliance/reports/annual-submissions/` | CBSE annual submission checklist |
| 5 | `GET` | `/api/v1/school/{id}/compliance/reports/calendar/` | Compliance calendar for year |
| 6 | `POST` | `/api/v1/school/{id}/compliance/reports/principal-signoff/` | Monthly Principal sign-off |
| 7 | `GET` | `/api/v1/school/{id}/compliance/reports/export/cbse/` | CBSE-format compliance bundle |
| 8 | `GET` | `/api/v1/school/{id}/compliance/reports/health-score/` | Detailed score breakdown |

---

## 9. Business Rules

- The compliance health score (0–100%) is computed by EduForge automatically from the status of all sub-modules; a score below 70% triggers a mandatory Principal review with action plan within 7 days
- Monthly Principal sign-off is mandatory; a month without sign-off generates an escalating reminder (day 1, day 3, day 7 of the following month); if month +1 also has no sign-off, the school account manager at EduForge is notified (account health flag)
- Compliance dashboard is not shared externally by EduForge; it is strictly internal to the school's Principal and Compliance Officer; EduForge does not report school compliance scores to CBSE or any government body
- All compliance dates in the annual calendar are pre-loaded for every school at the start of the year; school-specific dates (renewal dates from their own documents) overlay the standard calendar
- The "open actions" list is the single task list for compliance; every compliance issue generates an action; actions are never auto-closed without a human marking them complete; the system can send reminders but cannot close actions automatically
- CBSE annual submissions: EduForge generates the data packages (fee structure document, working day register, etc.) but the school's Compliance Officer / Principal must review and submit on the actual CBSE OASIS portal (external system); EduForge logs the submission date when the school confirms it was submitted

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division K*
