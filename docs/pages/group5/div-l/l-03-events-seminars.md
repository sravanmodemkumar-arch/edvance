# L-03 — Events & Seminars

> **URL:** `/coaching/marketing/events/`
> **File:** `l-03-events-seminars.md`
> **Priority:** P2
> **Roles:** Marketing Coordinator (K3) · Branch Manager (K6) · Student Counsellor (K3)

---

## 1. Events Calendar

```
EVENTS & SEMINARS CALENDAR — Q4 AY 2025–26
April – June 2026 | Toppers Coaching Centre

  Date        │ Event                              │ Type          │ Audience    │ Venue        │ Status
  ────────────┼────────────────────────────────────┼───────────────┼─────────────┼──────────────┼──────────
  Apr 3, 2026 │ SSC CGL 2026 Free Seminar          │ Prospect      │ New students│ TCC Hall A   │ 📅 Upcoming
  Apr 5, 2026 │ Faculty Development Meeting (Q4)   │ Internal      │ Faculty     │ Conference Rm│ 📅 Upcoming
  Apr 10, 2026│ Demo Class — IBPS PO Batch 2026   │ Demo          │ Prospects   │ Room 3       │ 📅 Upcoming
  Apr 15, 2026│ Alumni Meet — Hyderabad Main       │ Alumni        │ Alumni      │ TCC Hall A   │ 📅 Upcoming
  Apr 20, 2026│ Parent Orientation — New Batches  │ Parent        │ Parents     │ TCC Hall A   │ 📅 Upcoming
  May 1, 2026 │ Summer Foundation Batch Launch    │ New batch     │ Class 10+2  │ All rooms    │ 📅 Upcoming
  May 10, 2026│ Motivational Talk — IRS Officer   │ Guest speaker │ All students│ TCC Hall A   │ 📅 Planned
  Jun 15, 2026│ End-of-Year Award Ceremony        │ Institutional │ All students│ External hall│ 📅 Planned
  ────────────┴────────────────────────────────────┴───────────────┴─────────────┴──────────────┴──────────

  PAST EVENTS (Q3 — Completed):
    Mar 28: Result Celebration — SSC CGL 2024 selected students (42 attended) ✅
    Mar 15: Free Seminar "How to crack SSC CGL in first attempt" (186 attended) ✅
    Mar 10: Parent-Teacher Meeting (82% parent attendance) ✅
```

---

## 2. Event Detail — SSC CGL Free Seminar

```
EVENT: SSC CGL 2026 Free Seminar
Date: 3 April 2026, 10:00 AM – 1:00 PM
Venue: TCC Hall A, Hyderabad Main Branch (capacity: 200)

  REGISTRATION STATUS:
    Registered:    184 (as of 31 Mar)  ✅
    Walk-in quota:  16 (reserved)
    Capacity:      200

  AGENDA:
    10:00 – 10:15  Welcome & TCC introduction (Branch Manager)
    10:15 – 11:00  "SSC CGL 2026 exam pattern & strategy" (Mr. Suresh K., Quant)
    11:00 – 11:45  "English section — do's and don'ts" (Ms. Kavita M.)
    11:45 – 12:00  Break
    12:00 – 12:30  "Mock test importance — Akhil Kumar's journey" (Alumni)
    12:30 – 12:50  Q&A session
    12:50 – 13:00  Batch details, fee structure, enrollment process (Counsellor)

  PROMOTIONS:
    On-the-day enrollment offer: ₹2,000 discount (valid until Apr 5 only)
    Free mock test voucher: for all attendees (regardless of enrollment)

  LOGISTICS:
    Hall setup:      Chairs, projector, whiteboard ✅
    Refreshments:    Tea & snacks (₹1,200 budget)
    Registration:    QR code entry verification (app-based)
    Follow-up:       WhatsApp message + call within 24 hrs for non-enrollees

  EXPECTED CONVERSIONS: 28–35 enrollments (historical 15–19% from seminar attendees)
```

---

## 3. Post-Event Analytics

```
POST-EVENT REPORT — Free Seminar "How to crack SSC CGL"
Event Date: 15 March 2026

  ATTENDANCE:
    Registered:   210  │  Attended:  186 (88.6%)  │  Walk-ins: 18
    Faculty:        3  │  Staff:       4

  LEAD QUALITY:
    Enquiry forms filled (at event):   164
    CRM entries created:               164
    Same-day enrollments:                8
    Enrollments within 7 days:          22
    Enrollments within 30 days:         36
    Total attributed to this event:     36 (19.4% conversion rate) ✅

  SATISFACTION SURVEY (n=148 of 186):
    Content quality:         4.4/5.0 ✅
    Speaker quality:         4.5/5.0 ✅
    Duration appropriate:    4.2/5.0 ✅
    Venue & comfort:         4.1/5.0 ✅
    Would recommend:        94.6% ✅

  COST:
    Venue/setup:    ₹ 2,400
    Refreshments:   ₹ 1,800
    Promotion:      ₹ 4,200  (ads driving registrations)
    TOTAL:          ₹ 8,400  │  Cost per enrollment: ₹233 ✅ (excellent)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/marketing/events/` | Events calendar |
| 2 | `POST` | `/api/v1/coaching/{id}/marketing/events/` | Create new event |
| 3 | `POST` | `/api/v1/coaching/{id}/marketing/events/{eid}/register/` | Register attendee |
| 4 | `GET` | `/api/v1/coaching/{id}/marketing/events/{eid}/attendance/` | Attendance tracking |
| 5 | `GET` | `/api/v1/coaching/{id}/marketing/events/{eid}/report/` | Post-event analytics report |
| 6 | `GET` | `/api/v1/coaching/{id}/marketing/events/conversions/?event={eid}` | Enrollment conversions from event |

---

## 5. Business Rules

- Free seminars are TCC's highest-converting marketing activity (19.4% seminar attendee-to-enrollment in March); they work because: (a) the attendee has self-selected as interested in the exam and coaching; (b) they experience TCC's quality directly through the faculty presentation; (c) the on-the-spot offer reduces friction; (d) the free mock test voucher creates a follow-up touchpoint; the seminar is not just a sales event — it delivers genuine value (exam strategy, faculty insights), which builds trust before the enrollment conversation
- The on-day enrollment discount (₹2,000 valid for 2 days) creates urgency without being exploitative; the discount is real (not artificially inflated before the offer) and time-limited; Consumer Protection Act 2019 prohibits "bait-and-switch" pricing where the pre-discount price is artificially inflated to make the discount appear larger; TCC's standard fee must be the actual fee charged to non-seminar students; the discount offer is documented in the event materials and the CRM so it can be audited
- Alumni guest speakers (like Akhil Kumar in the upcoming seminar) are the most credible element of any seminar; a current student or placed alumnus speaking authentically about their experience is more persuasive than any sales pitch from faculty or management; alumni speakers are briefed on the format and duration but not scripted — their genuine story is the asset; TCC compensates alumni speakers with a gift voucher or informal recognition, never with cash (which would create a taxable commission relationship under Section 194H)
- Event registration data (name, phone, email) collected at seminars is governed by DPDPA 2023; the registration form must include a notice that TCC will contact registrants with enrollment information and offers; pre-checked opt-in boxes are not valid consent under DPDPA; the registrant must actively opt in; event attendees who do not enroll are followed up for 30 days only; after 30 days, non-responding leads are moved to a "cold" status and contact frequency drops to once per quarter (newsletter-only); leads are not retained indefinitely
- Post-event conversion attribution (36 enrollments attributed to the March 15 seminar) is tracked in the CRM by asking all new enrollees "how did you hear about TCC?"; CRM agents verify that the seminar attendee appears in the event attendance log before attributing the enrollment; a student who attended the seminar but also came from a Google Ad click is attributed to the seminar (first-touch vs. last-touch debate); TCC uses first-touch attribution for seminar events to measure the event's reach; the attribution methodology is documented and consistent year-over-year

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division L*
