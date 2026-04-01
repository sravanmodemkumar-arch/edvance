# M-06 — Compliance & Regulatory Calendar

> **URL:** `/coaching/operations/compliance/`
> **File:** `m-06-compliance-calendar.md`
> **Priority:** P2
> **Roles:** Director (K7) · Branch Manager (K6) · Accounts Manager (K5)

---

## 1. Compliance Calendar

```
COMPLIANCE CALENDAR — AY 2025–26
Toppers Coaching Centre | Legal & Regulatory Obligations

  MONTHLY RECURRING:
    Due Date      │ Obligation                           │ Owner    │ Status (Mar 26)
    ──────────────┼──────────────────────────────────────┼──────────┼────────────────
    7th of month  │ TDS remittance (Section 194C/J/H)   │ Accounts │ ✅ Done (7 Mar)
    10th of month │ PF ECR filing + challan payment      │ Accounts │ ✅ Done (10 Mar)
    15th of month │ ESI challan payment                  │ Accounts │ ✅ Done (15 Mar)
    20th of month │ GST-3B filing + payment              │ Accounts │ ✅ Done (20 Mar)
    25th of month │ GSTR-1 filing (outward supplies)     │ Accounts │ ✅ Done (25 Mar)

  QUARTERLY:
    Apr 30, 2026  │ TDS return Form 26Q (Q4 FY 25-26)   │ Accounts │ ⏳ Due
    Apr 30, 2026  │ TDS return Form 24Q (salary TDS Q4)  │ Accounts │ ⏳ Due
    Jun 15, 2026  │ Advance tax (1st instalment FY26-27) │ Accounts │ 📅 Upcoming

  ANNUAL:
    Mar 31, 2026  │ Financial year close (FY 2025–26)   │ Accounts │ ✅ Today
    Jul 31, 2026  │ ITR filing (Income Tax Return)       │ CA       │ 📅 Upcoming
    Sep 30, 2026  │ Statutory audit completion           │ CA firm  │ 📅 Upcoming
    Jan 2026      │ Fire NOC renewal                     │ Ops Mgr  │ ✅ Done
    Dec 2025      │ Shop & Establishment Act renewal     │ Director │ ✅ Done
    Ongoing       │ FSSAI licence (hostel mess vendor)   │ Ops Mgr  │ ✅ Valid

  OPERATIONAL COMPLIANCE:
    Feb 2026      │ POCSO awareness session (new batches)│ Counsellr│ ✅ Done
    Mar 2026      │ Women's safety self-defence session  │ Counsellr│ ✅ Done
    Apr 2026      │ AC annual service (pre-summer)       │ IT/Ops   │ ⚠️ Overdue
```

---

## 2. Compliance Status Dashboard

```
COMPLIANCE STATUS — 31 March 2026 (End of FY 2025–26)

  CATEGORY              │ Items │ ✅ Done │ ⚠️ Due Soon │ ❌ Overdue │ Risk Level
  ──────────────────────┼───────┼─────────┼─────────────┼────────────┼────────────
  Tax (GST, TDS, IT)    │  12   │   11    │      1      │     0      │ LOW ✅
  Labour law (PF, ESI)  │   8   │    8    │      0      │     0      │ LOW ✅
  Licences & permits    │   6   │    5    │      0      │     1 (AC) │ MEDIUM 🟡
  Student welfare (POCSO│   4   │    4    │      0      │     0      │ LOW ✅
  Data protection (DPDPA│   5   │    5    │      0      │     0      │ LOW ✅
  Fire & safety         │   3   │    3    │      0      │     0      │ LOW ✅
  ──────────────────────┴───────┴─────────┴─────────────┴────────────┴────────────
  TOTAL                 │  38   │   36    │      1      │     1      │ LOW ✅

  OVERDUE ITEM:
    AC annual service (before summer) — technician booked Apr 1, 2026 ✅ (in progress)

  UPCOMING (next 30 days):
    Apr 7:  TDS payment (April salary TDS)
    Apr 10: PF ECR filing
    Apr 20: GST-3B (March 2026 returns)
    Apr 30: TDS returns Form 26Q + 24Q (Q4 FY 25-26)
```

---

## 3. Regulatory Reference

```
KEY REGULATIONS — TCC Compliance Obligations

  REGULATION               │ Authority  │ Obligation                     │ TCC Contact
  ─────────────────────────┼────────────┼────────────────────────────────┼────────────────
  Income Tax Act 1961       │ CBDT       │ ITR, TDS, advance tax          │ Accounts Mgr
  GST Act 2017              │ CBIC       │ GSTR-1, GSTR-3B, GST payment  │ Accounts Mgr
  EPFO (PF Act 1952)        │ EPFO       │ PF registration, monthly ECR   │ Accounts Mgr
  ESIC Act 1948             │ ESIC       │ ESI registration, monthly pay  │ Accounts Mgr
  Shops & Estab. Act (TS)   │ Labour Dept│ Registration, hours, holidays  │ Director
  POCSO Act 2012            │ NCPCR      │ Designated contact, awareness  │ Counsellor
  DPDPA 2023                │ DPDPB      │ Consent, data security, notice │ IT + Director
  FSSAI (Food Safety)       │ FSSAI      │ Vendor licence verification    │ Ops Coordinator
  Consumer Protection 2019  │ CCPA       │ Fair pricing, no misleading ads│ Director
  Fire Safety (TS)          │ Fire Dept  │ NOC, annual inspection         │ Ops Coordinator
  Building Plan Approval    │ GHMC       │ Construction NOC (Block C)     │ Director
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/operations/compliance/calendar/` | Compliance calendar |
| 2 | `GET` | `/api/v1/coaching/{id}/operations/compliance/status/` | Compliance status dashboard |
| 3 | `PATCH` | `/api/v1/coaching/{id}/operations/compliance/{cid}/complete/` | Mark compliance item complete |
| 4 | `GET` | `/api/v1/coaching/{id}/operations/compliance/overdue/` | Overdue compliance items |
| 5 | `POST` | `/api/v1/coaching/{id}/operations/compliance/reminders/` | Set compliance reminder |

---

## 5. Business Rules

- The compliance calendar is the Branch Manager's single most important risk management tool; a missed TDS payment (by one day) attracts interest at 1.5% per month; a missed GSTR-1 filing attracts ₹50/day penalty; a missed PF challan is a criminal offence; none of these are large individual amounts, but they accumulate and create a compliance history that damages TCC during tax audits or inspections; the accounts team must treat the compliance calendar as non-negotiable deadlines, not best-effort targets
- Year-end financial close (31 March 2026) triggers a cascade of compliance activities: the statutory auditor begins the annual audit (June–September), the CA prepares the ITR (due July 31), and all quarterly TDS returns for Q4 must be filed by April 30; the Branch Manager must ensure all March 2026 transactions are entered into Tally by April 5 to give the accounts team enough preparation time; a Branch Manager who approves late March expenses in April delays the entire year-end process
- DPDPA 2023 compliance is an ongoing operational commitment, not a one-time exercise; TCC must maintain: (1) a record of all consents (enrollment consent form, survey opt-in, marketing consent); (2) a data inventory showing what personal data is collected and for what purpose; (3) a data access log (M-04 IT systems); (4) a breach notification SOP; (5) privacy notices on all data collection forms; the EduForge platform handles technical compliance (encryption, access control) but TCC is the "data fiduciary" legally responsible for DPDPA compliance — TCC cannot outsource this accountability to EduForge
- POCSO compliance requires TCC to designate a POCSO contact (the Student Counsellor serves this role), conduct awareness sessions with every new batch of students, and have a documented process for reporting allegations; any allegation involving a minor student (Class 10+2 foundation batch students may be 16–17 years old) must be reported to the police within 24 hours without TCC conducting its own investigation first — investigation is the police's role; failure to report a POCSO allegation is itself a criminal offence; TCC's Director must be personally familiar with the POCSO escalation SOP
- The Block C construction requires a Building Plan Approval from GHMC (Greater Hyderabad Municipal Corporation) before construction begins; construction without approval is an unauthorised structure that can be demolished by GHMC and exposes TCC to heavy penalties; the Director confirms that GHMC approval was obtained before the construction contract was signed; occupancy of the new hostel rooms (August 2026) requires a separate occupancy certificate from GHMC and a new fire NOC that covers Block C; the Operations Coordinator must schedule these inspections 30 days before the planned occupancy date to allow for lead time

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division M*
