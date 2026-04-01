# F-02 — Lead Management (CRM)

> **URL:** `/coaching/admissions/leads/`
> **File:** `f-02-lead-management.md`
> **Priority:** P1
> **Roles:** Admissions Counsellor (K3) · Sales Executive (K2) · Branch Manager (K6)

---

## 1. Lead List

```
LEAD MANAGEMENT — CRM
As of 30 March 2026  |  Ms. Ananya Roy (Counsellor)

  Filter: [Stage: All ▼]  [Source: All ▼]  [Course: All ▼]  [Search: _____]

  ID        │ Name             │ Phone         │ Course Interest │ Source     │ Stage       │ Last Contact
  ──────────┼──────────────────┼───────────────┼─────────────────┼────────────┼─────────────┼─────────────
  LEAD-1842 │ Suresh Babu      │ +91-98765-4231│ SSC CGL 2026    │ Walk-in    │ 🔴 Hot      │ 29 Mar (demo)
  LEAD-1836 │ Renu Sharma      │ +91-91234-5678│ Banking PO      │ YouTube    │ 🔴 Hot      │ 28 Mar (call)
  LEAD-1821 │ Kavitha Devi     │ +91-88765-4321│ SSC CGL + CHSL  │ Referral   │ 🟡 Warm     │ 25 Mar (demo)
  LEAD-1829 │ Priya K.         │ +91-77654-3210│ Banking PO      │ Instagram  │ 🟡 Warm     │ 24 Mar (demo)
  LEAD-1812 │ Kiran Naidu      │ +91-99875-6432│ Foundation      │ Organic    │ 🟡 Warm     │ 21 Mar
  LEAD-1804 │ Deepak Reddy     │ +91-98711-2345│ RRB NTPC        │ Walk-in    │ 🔵 Cold     │ 18 Mar
  LEAD-1798 │ Sravya Menon     │ +91-77890-1234│ SSC CHSL        │ YouTube    │ 🔵 Cold     │ 15 Mar
  ...  (127 more leads assigned to this counsellor)

  PIPELINE SUMMARY (My Leads):
    🔴 Hot: 18 | 🟡 Warm: 34 | 🔵 Cold: 82 | ⬛ Closed (Won): 58 | ✖ Lost: 14

  [+ Add Lead]   [Import CSV]   [Export (with Manager approval)]
```

---

## 2. Lead Detail View

```
LEAD DETAIL — LEAD-1842: Suresh Babu
Created: 28 Mar 2026  |  Assigned to: Ms. Ananya Roy

  PROFILE:
    Name:         Suresh Babu Rao
    Phone:        +91-98765-4231 (verified)
    Email:        suresh.rao@gmail.com
    Age:          24  |  Qualification: B.Tech (Mech), JNTU 2024
    Location:     Dilsukhnagar, Hyderabad
    Source:       Walk-in (visited branch on 28 Mar)

  COURSE INTEREST:
    Primary:      SSC CGL 2026 (Tier-I in Apr 2026 — already registered!)
    Secondary:    SSC CGL 2027 (if doesn't clear this year)
    Budget:       ₹15,000–18,000 ("student loan approved")

  TIMELINE:
    28 Mar 10:30 AM — Walk-in enquiry, greeted by receptionist, assigned to Ananya
    28 Mar 11:00 AM — Counselling session (30 min): discussed batch, fee, schedule
    29 Mar 09:00 AM — Attended demo class (SSC CGL Morning) ✅
    29 Mar 11:30 AM — Post-demo call: "very impressed, deciding tonight"
    30 Mar 10:00 AM — [Appointment: Enrollment] ← TODAY

  NEXT ACTION:  Enrollment meeting at 10:00 AM today
  Notes: "SSC CGL already registered for Apr 2026 exam — may not join current batch;
          focus on 2026–27 batch (May start). Offer early-bird ₹500 discount."

  [Log Call]  [Add Note]  [Convert to Enrollment →]  [Mark as Lost]
```

---

## 3. Lead Activity Log

```
ACTIVITY LOG — LEAD-1842

  30 Mar 10:00 AM │ Appointment — Enrollment meeting (upcoming)
  29 Mar 11:30 AM │ Call (3 min) — Ananya Roy — "Very positive, enrolling tomorrow"
  29 Mar 09:00 AM │ Demo attended — SSC CGL Morning class (Quant session)
  28 Mar 11:00 AM │ Counselling session (30 min) — batch/fee/schedule covered
  28 Mar 10:30 AM │ Walk-in — first contact; assigned to Ananya Roy
  28 Mar 10:28 AM │ Lead created — source: Walk-in (receptionist logged)

  [+ Log Activity]
  Activity types:  Call · WhatsApp · Email · Meeting · Demo · Note · SMS
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/admissions/leads/?counsellor={uid}&stage=hot` | Leads filtered by stage/counsellor |
| 2 | `POST` | `/api/v1/coaching/{id}/admissions/leads/` | Create new lead |
| 3 | `GET` | `/api/v1/coaching/{id}/admissions/leads/{lid}/` | Lead detail with activity log |
| 4 | `PATCH` | `/api/v1/coaching/{id}/admissions/leads/{lid}/` | Update lead (stage, notes, assignment) |
| 5 | `POST` | `/api/v1/coaching/{id}/admissions/leads/{lid}/activity/` | Log an activity (call, demo, note) |
| 6 | `POST` | `/api/v1/coaching/{id}/admissions/leads/{lid}/convert/` | Convert lead to enrollment |

---

## 5. Business Rules

- Lead stage transitions are one-directional by default: Cold → Warm → Hot → Enrolled / Lost; a lead cannot move back from Hot to Cold through the UI (it would indicate a data entry error or system manipulation); if a hot lead goes silent for 7 days without response, it is automatically moved to "Dormant" (a separate state from Cold) — dormant leads are re-contacted after 30 days with a new promotion or batch announcement; this prevents the counsellor pipeline from being cluttered with stale hot leads that inflate the funnel metric
- Every counsellor-lead interaction must be logged in the activity log within the same business day; a lead with no activity for more than 48 hours (during working days) triggers an alert to the Branch Manager; unlogged interactions are a compliance and audit risk — if a student later disputes the admissions process ("I was promised X"), TCC must be able to show what was communicated and when; the activity log is TCC's evidence trail
- Lead assignment is done by the Branch Manager or a designated admissions coordinator, not self-selected by counsellors; this prevents counsellors from cherry-picking "easy" leads (walk-ins already decided to enrol) and avoiding difficult leads (phone enquiries who need more convincing); fair assignment is monitored in the monthly sales report (F-07) by comparing counsellors' lead quality (source, course interest) against their conversion rates
- Phone numbers are verified at lead creation by sending an OTP; unverified phone numbers are flagged in the CRM and cannot receive bulk SMS campaigns; this prevents junk data from accumulating in the CRM (wrong numbers, fake leads entered to inflate pipeline numbers); fake lead entry is a gaming behaviour some sales executives use to show a full pipeline — the OTP verification step reduces but does not eliminate this problem
- "Mark as Lost" must include a reason selected from a dropdown (competitor enrolled, fee too high, exam postponed, personal reasons, no response after 3 follow-ups, other); the reason data aggregated monthly tells TCC why they are losing students — if 40% of lost leads cite "fee too high", that informs pricing review; if 30% cite "competitor enrolled", that informs competitive analysis; the reason for loss is as valuable as the lead itself

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division F*
