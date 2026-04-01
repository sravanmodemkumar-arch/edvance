# F-03 — Enquiry & Walk-in Form

> **URL:** `/coaching/admissions/enquiry/`
> **File:** `f-03-enquiry-form.md`
> **Priority:** P1
> **Roles:** Receptionist (K1) · Admissions Counsellor (K3) · Sales Executive (K2)

---

## 1. New Enquiry Form (Walk-in / Call)

```
NEW ENQUIRY FORM
Toppers Coaching Centre — Hyderabad Main Branch
Logged by: Ms. Sunita (Receptionist) | 30 March 2026, 11:28 AM

  CONTACT DETAILS:
    Name *:          [Vikram Goud                         ]
    Mobile *:        [+91-98760-12345                     ]  [Send OTP →]
    OTP Verified:    ✅ 6-digit OTP confirmed
    Email:           [vikram.goud@gmail.com                ] (optional)
    Age:             [23   ]   Gender: (●) Male  ( ) Female  ( ) Other

  COURSE INTEREST:
    Primary exam:    [RRB NTPC ▼]
    Secondary:       [None ▼]
    Exam target year:[2026 ▼]

  BACKGROUND:
    Qualification:   [B.Sc. (Physics) ▼]   Year of passing: [2025 ▼]
    Currently working: ( ) Yes  (●) No
    Preferred batch time: (●) Morning  ( ) Evening  ( ) Online

  SOURCE OF ENQUIRY:
    How did you hear about TCC?
    ( ) Walk-in (passed by)   (●) YouTube   ( ) Instagram   ( ) Google
    ( ) Friend referral [Referrer name: _____]   ( ) Newspaper   ( ) Other

  ADDITIONAL NOTES:
    [Student mentioned seeing TCC's RRB video on YouTube (Reasoning channel)]

  ASSIGN TO COUNSELLOR:   [Ms. Ananya Roy ▼]  (least-loaded today)
  BOOK DEMO:              [Apr 1 (Wed), 6:00 AM — SSC/RRB Morning ▼]

  [Save & Assign]   [Save & Print Token]   [Cancel]

  Lead ID assigned:   LEAD-1852 (auto-generated)
  Token number:       T-284  (for today's walk-in queue)
```

---

## 2. Walk-in Queue

```
TODAY'S WALK-IN QUEUE — 30 March 2026
Hyderabad Main Branch | 11:30 AM

  Token  │ Name             │ Time In  │ Course      │ Counsellor   │ Status
  ───────┼──────────────────┼──────────┼─────────────┼──────────────┼──────────────────
  T-281  │ Ravi Kumar       │ 09:40 AM │ SSC CGL     │ Ananya Roy   │ ✅ Done (10:15)
  T-282  │ Lakshmi Devi     │ 10:20 AM │ Banking PO  │ Rohan Sharma │ ✅ Done (10:58)
  T-283  │ Suresh Babu      │ 10:28 AM │ SSC CGL     │ Ananya Roy   │ ✅ Done (11:05)
  T-284  │ Vikram Goud      │ 11:28 AM │ RRB NTPC    │ Ananya Roy   │ ⏳ Waiting
  T-285  │ [Next walk-in]   │ —        │ —           │ —            │ —

  COUNSELLORS ON DUTY:
    Ms. Ananya Roy:   3 enquiries today (busy — T-284 next)
    Mr. Rohan Sharma: 2 enquiries today (available now)
    Ms. Sunita:       Receptionist only (not counsellor)

  Avg wait time today: 12 minutes ✅ (target: < 15 min)
```

---

## 3. Online Enquiry (Web Form Submission)

```
ONLINE ENQUIRY — Submitted via tcc.eduforge.in/enquire

  LEAD-1849: Meena Kapoor
  Submitted: 30 Mar 2026, 09:14 AM via website

  Name:          Meena Kapoor
  Mobile:        +91-77654-8765 (OTP verified via web form ✅)
  Email:         meena.k@outlook.com
  Exam:          SSC CGL + SSC CHSL
  City:          Bengaluru (online batch preferred)
  Message:       "I work full-time, can only attend evening or weekend classes.
                  Is online batch available for SSC CGL?"

  AUTO-RESPONSE SENT: ✅ (WhatsApp + Email — 09:14 AM)
    "Hi Meena! Thank you for enquiring at TCC. Our Online SSC CGL batch
     starts May 2026 (Mon–Sat, 7–9 PM). A counsellor will call you within
     2 hours. — TCC Hyderabad"

  ASSIGNED TO:   Mr. Rohan Sharma
  FOLLOW-UP:     Call due by 11:14 AM ⚠️ (2-hour SLA — 22 min remaining)
  STAGE:         New → [Acknowledge] → Counselling → Demo → Enrollment
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/coaching/{id}/admissions/enquiry/` | Create new enquiry (walk-in or online) |
| 2 | `GET` | `/api/v1/coaching/{id}/admissions/enquiry/queue/?date=2026-03-30` | Walk-in queue for a day |
| 3 | `POST` | `/api/v1/coaching/{id}/admissions/enquiry/otp/verify/` | Verify mobile OTP for lead |
| 4 | `POST` | `/api/v1/coaching/{id}/admissions/enquiry/{eid}/assign/` | Assign lead to counsellor |
| 5 | `GET` | `/api/v1/coaching/{id}/admissions/enquiry/online/` | Online web form submissions |

---

## 5. Business Rules

- Mobile number OTP verification is mandatory for all new enquiries; a lead with an unverified phone number cannot be converted to enrollment; the OTP serves two purposes — confirming the number is real (reducing fake leads) and obtaining a digital record of the student's consent to be contacted by TCC (required under DPDPA 2023 for marketing communications); the OTP confirmation is stored with the lead record as proof of consent
- Walk-in enquiries must be handled within 15 minutes of arrival; the token system ensures no student waits more than 15 minutes to see a counsellor; if all counsellors are busy, the receptionist acknowledges the student, gives a time estimate, and offers tea while waiting — this hospitality is part of TCC's admissions SOP; a 15-minute wait limit is monitored in the branch manager's daily report; consistently long waits indicate understaffing
- Online web form submissions trigger an automated WhatsApp response within 2 minutes and a counsellor call within 2 hours during working hours (9 AM to 7 PM); enquiries submitted outside working hours receive the automated response and a call the next morning by 10 AM; the 2-hour response SLA is published on TCC's website as a service commitment; breach of this SLA is tracked in the sales report (F-07)
- The "source of enquiry" field is mandatory; it feeds the marketing ROI analysis — TCC needs to know which channels generate leads to allocate the marketing budget (L-01); a counsellor who marks every enquiry as "Walk-in" to avoid filling the source field is degrading the marketing data; the Branch Manager audits source distribution monthly — if 80% of leads are marked "Walk-in" for a counsellor who handles many phone leads, the data is suspicious and will be investigated
- Referral source data (which existing student referred the enquiry) is captured to process the referral reward (F-08); the referring student's name and ID are recorded at enquiry creation; if the referred student enrolls, the referral reward is triggered automatically; a referral claim submitted after enrollment (not at enquiry stage) requires Branch Manager approval and supporting proof; late referral claims are common gaming attempts ("I forgot to mention my friend referred me")

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division F*
