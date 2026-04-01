# F-01 — Admissions Dashboard

> **URL:** `/coaching/admissions/dashboard/`
> **File:** `f-01-admissions-dashboard.md`
> **Priority:** P1
> **Roles:** Admissions Counsellor (K3) · Branch Manager (K6)

---

## 1. Admissions Overview

```
ADMISSIONS DASHBOARD — Toppers Coaching Centre, Hyderabad Main
As of 30 March 2026  |  Academic Year 2026–27 Admissions (Starting May 2026)

  ┌─────────────────────────────────────────────────────────────────────────────┐
  │  THIS MONTH (March 2026):                                                  │
  │  New Enquiries: 284   Demo Attended: 168   Enrolled: 112   Revenue: ₹14.2L │
  │  Conversion (Enquiry→Enroll): 39.4%   vs Last Month: 36.8%  ↑ +2.6% ✅    │
  └─────────────────────────────────────────────────────────────────────────────┘

  FUNNEL OVERVIEW:
    Enquiries received:     284
        ↓ (Demo shown)
    Demo attended:          168  (59.2%)
        ↓ (Follow-up)
    Counselling done:       142  (50.0%)
        ↓ (Enrolled)
    Enrolled:               112  (39.4%)
        ↓ (Active in batch)
    Active in batch:        106  (37.3%)  ← 6 enrolled but awaiting batch start

  PIPELINE — Leads in progress (not yet enrolled):
    Hot leads (followed up, demo done, fee pending):   34
    Warm leads (demo done, no decision):               42
    Cold leads (enquiry only, no response to follow-up): 68

  BATCH-WISE SEATS REMAINING (2026–27 batches):
    SSC CGL Morning (May 26):  40 seats left / 250  (16%)
    Banking Batch (May 26):    62 seats left / 200  (31%)
    RRB NTPC (Jun 26):        110 seats left / 200  (55%)
    Foundation (Jun 26):       90 seats left / 150  (60%)
```

---

## 2. Today's Counsellor Schedule

```
TODAY'S SCHEDULE — Ms. Ananya Roy (Admissions Counsellor)
30 March 2026

  Time     │ Appointment         │ Lead ID   │ Course Interest    │ Stage
  ─────────┼─────────────────────┼───────────┼────────────────────┼──────────────────
  10:00 AM │ Suresh Babu (walk-in)│ LEAD-1842 │ SSC CGL 2026       │ Demo → Enrollment
  11:00 AM │ Renu Sharma (phone) │ LEAD-1836 │ Banking PO          │ 2nd follow-up
  11:30 AM │ Vikram G. (walk-in) │ LEAD-1848 │ RRB NTPC            │ New enquiry
  02:00 PM │ Kavitha D. (online) │ LEAD-1821 │ SSC CGL + CHSL      │ Counselling
  03:30 PM │ Mohammed T. (walk-in)│ LEAD-1851 │ Foundation          │ New enquiry
  04:30 PM │ Priya K. (phone)    │ LEAD-1829 │ Banking PO          │ Closing call

  [+ Add Appointment]   [View All Leads →]   [Daily Summary Report]
```

---

## 3. Batch Seat Availability Alerts

```
SEAT AVAILABILITY ALERTS

  🔴 SSC CGL Morning (May 26): Only 40 seats left
     → Counsellors must prioritise this batch in conversations
     → No new walk-in demo slots after Apr 20 (risk of oversubscription)

  🟡 Banking Batch (May 26): 62 seats — moderate urgency
     → Continue normal admissions; monitor weekly

  ✅ RRB NTPC and Foundation: Ample seats — standard process

  OVERBOOKING POLICY:
    Hard cap = batch capacity (250 / 200 / 150 as configured)
    System blocks enrollment if batch is at capacity
    Waitlist: student enters waitlist; auto-offered next batch if seat opens
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/admissions/dashboard/` | Full dashboard data |
| 2 | `GET` | `/api/v1/coaching/{id}/admissions/funnel/?month=2026-03` | Monthly conversion funnel |
| 3 | `GET` | `/api/v1/coaching/{id}/admissions/seats/` | Remaining seats by batch |
| 4 | `GET` | `/api/v1/coaching/{id}/admissions/schedule/?counsellor={uid}&date=2026-03-30` | Counsellor's daily schedule |
| 5 | `GET` | `/api/v1/coaching/{id}/admissions/pipeline/` | Leads by funnel stage |

---

## 5. Business Rules

- The admissions dashboard is visible to all Admissions Counsellors and the Branch Manager; counsellors see only their own assigned leads and appointments; the Branch Manager sees the full branch funnel including all counsellors' pipelines and the aggregate conversion rate; individual counsellor conversion rates are used in the monthly sales review but are not visible peer-to-peer to prevent unhealthy competition
- Batch seat availability is enforced at the database level — the system rejects an enrollment attempt when a batch is at capacity regardless of how it is submitted (walk-in desk, online form, or direct API call); the waitlist is automatic; a student on the waitlist receives a notification when a seat opens (due to cancellation or capacity expansion) and has 48 hours to confirm before the seat is offered to the next person on the list
- The conversion funnel (39.4% enquiry-to-enrollment) is the primary admissions KPI; TCC's target is 40%; the Branch Manager reviews the funnel weekly; a drop below 35% triggers a review of counsellor scripts, demo class quality, and competitor pricing; the funnel data also shows where students drop off — a high demo attendance but low counselling rate means demos are good but the counselling follow-up is weak
- "Hot leads" (demo done, fee pending) must receive a follow-up call within 24 hours of the demo; this is tracked in the CRM (F-02); a lead that goes without follow-up for more than 48 hours after a demo drops to "warm" automatically; the system sends a reminder to the assigned counsellor at 24 hours; studies on coaching centre admissions show that a student who decides to enrol within 48 hours of the demo has a 3× higher chance of following through than one who delays
- Admissions data (student name, phone, email, course interest) is personal data under DPDPA 2023; leads who did not enrol have their data retained for 90 days for re-engagement purposes; after 90 days, the data is anonymised (name, phone, email replaced with hashes) unless the student gave explicit marketing consent; bulk export of lead data requires Branch Manager approval and is logged in the audit trail

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division F*
