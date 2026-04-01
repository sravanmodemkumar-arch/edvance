# F-09 — Demo Class Management

> **URL:** `/coaching/admissions/demo/`
> **File:** `f-09-demo-class.md`
> **Priority:** P3
> **Roles:** Admissions Counsellor (K3) · Sales Executive (K2) · Branch Manager (K6)

---

## 1. Demo Class Schedule

```
DEMO CLASS SCHEDULE — Toppers Coaching Centre
April 2026

  DATE       │ TIME     │ BATCH TYPE          │ FACULTY         │ HALL    │ SEATS │ BOOKED
  ───────────┼──────────┼─────────────────────┼─────────────────┼─────────┼───────┼────────
  Apr 1 Wed  │ 6:00 AM  │ SSC CGL Morning     │ Mr. Suresh K.   │ Hall A  │  20   │  14 ✅
  Apr 1 Wed  │ 7:00 PM  │ SSC CGL Evening     │ Mr. Suresh K.   │ Hall A  │  20   │   8
  Apr 2 Thu  │ 6:30 AM  │ Banking PO Morning  │ Ms. Deepa S.    │ Hall B  │  15   │  12 ✅
  Apr 4 Sat  │ 10:00 AM │ Foundation Batch    │ Mr. Vikram N.   │ Hall C  │  20   │   6
  Apr 6 Mon  │ 6:00 AM  │ SSC CGL Morning     │ Mr. Suresh K.   │ Hall A  │  20   │   2
  Apr 7 Tue  │ 7:00 PM  │ RRB NTPC Evening    │ Mr. Mohan R.    │ Hall B  │  15   │   5
  Apr 8 Wed  │ 6:00 AM  │ SSC CGL Morning     │ Mr. Suresh K.   │ Hall A  │  20   │   0
  Apr 9 Thu  │ 6:30 AM  │ Banking PO Morning  │ Ms. Deepa S.    │ Hall B  │  15   │   1

  ONLINE DEMO:
    Apr 3 Fri │ 6:30 PM  │ SSC CGL Online Batch │ Mr. Suresh K. │ Zoom    │  50   │  18
    Apr 5 Sun │ 11:00 AM │ Banking Online       │ Ms. Deepa S.  │ Zoom    │  50   │   4

  [+ Schedule New Demo]   [View Full Calendar]   [Book Lead for Demo]
```

---

## 2. Book Lead for Demo

```
BOOK DEMO — LEAD-1852: Vikram Goud
Course: RRB NTPC | Preferred: Morning

  RECOMMENDED DEMOS (RRB / General batches):
    Apr 1 Wed 6:00 AM — SSC CGL Morning (closest to RRB level — 6 seats left) ✅
    Apr 7 Tue 7:00 PM — RRB NTPC Evening (exact match — 10 seats left)

  BOOKING: [Apr 1, 6:00 AM — SSC CGL Morning ▼]

  CONFIRMATION:
    WhatsApp reminder: T-24 hours (Mar 31, 6:00 AM) + T-1 hour (Apr 1, 5:00 AM)
    SMS confirmation: Sent now ✅

  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ Demo confirmation sent to +91-98760-12345:                                 │
  │ "Hi Vikram! Your demo class at TCC is confirmed for Apr 1 (Wed) at         │
  │  6:00 AM. Venue: Hall A, TCC Hyderabad Main, Dilsukhnagar.                 │
  │  Bring a pen and arrive 5 min early. — TCC Admissions"                    │
  └─────────────────────────────────────────────────────────────────────────────┘

  [Confirm Booking]   [Reschedule]   [Cancel Demo]
```

---

## 3. Post-Demo Follow-Up Tracker

```
POST-DEMO TRACKING — April 1, 2026 (6:00 AM Demo — SSC CGL Morning)
Demo faculty: Mr. Suresh Kumar | Attended: 14 / 14 booked ✅

  Lead ID  │ Name             │ Feedback (immediate) │ Follow-up  │ Status
  ─────────┼──────────────────┼──────────────────────┼────────────┼──────────────────
  LEAD-1842│ Suresh Babu      │ "Excellent — enrolling"│ Done ✅   │ ✅ Enrolled
  LEAD-1848│ Vikram Goud      │ "Good — thinking"     │ 1 Apr 4PM  │ 🟡 Warm
  LEAD-1836│ Renu Sharma      │ "Want online batch"   │ 1 Apr 11AM │ 🟡 Warm
  LEAD-1850│ Ajay Nair        │ "Comparing with other"│ 2 Apr 10AM │ 🟡 Warm
  LEAD-1844│ Sreekanth N.     │ "Fee too high"        │ 2 Apr (call)│ 🔴 Risk
  ...  (9 more)

  Demo conversion so far (5 days post-demo):
    Enrolled: 4 / 14 (28.6%)
    Warm/In-discussion: 7 / 14 (50.0%)
    Lost/dropped: 3 / 14 (21.4%)
    Expected final conversion: ~42% (based on pipeline stage)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/admissions/demo/schedule/?month=2026-04` | Demo class schedule |
| 2 | `POST` | `/api/v1/coaching/{id}/admissions/demo/book/` | Book a lead for a demo |
| 3 | `POST` | `/api/v1/coaching/{id}/admissions/demo/{did}/attendance/` | Mark demo attendance |
| 4 | `GET` | `/api/v1/coaching/{id}/admissions/demo/{did}/followup/` | Post-demo follow-up tracker |
| 5 | `POST` | `/api/v1/coaching/{id}/admissions/demo/{did}/feedback/` | Log immediate post-demo feedback |
| 6 | `GET` | `/api/v1/coaching/{id}/admissions/demo/analytics/?month=2026-04` | Demo attendance and conversion |

---

## 5. Business Rules

- Demo classes are held in the live batch environment — leads attend an actual class session with regular students; TCC does not run separate "demo batches" with curated content; this ensures the lead sees the genuine teaching environment, not a polished sales presentation; the batch faculty is informed of the number of demo attendees before class but treats the session as a normal class; a lead who is impressed by the real class is more likely to enroll and stay enrolled than one who was impressed by a special demo
- Demo attendance is logged separately from batch attendance; demo attendees are not counted in the batch's attendance statistics; if a demo attendee disrupts the class or behaves inappropriately, the counsellor (who sits in the hall during demos) can quietly remove them; the batch students' learning must not be compromised for the sake of admissions; leads are reminded of this in the demo briefing ("you are attending a real class — please respect the students")
- The 2-reminder system (24 hours + 1 hour before demo) reduces demo no-shows significantly; without reminders, 40–50% of booked leads don't show up; with the 2-reminder system, TCC's no-show rate is 12%; no-show leads are called within 30 minutes of the demo start to reschedule; a lead who doesn't show up without notice is moved to "warm" from "hot" but not immediately closed — they are offered one more demo opportunity before being deprioritised
- Immediate post-demo feedback collection (captured by the counsellor in conversation at the demo exit) is the most valuable data point in the funnel; a lead who says "excellent — I'm enrolling" after the demo has a 70%+ chance of actually enrolling within 48 hours; a lead who says "comparing with other institutes" needs a competitive differentiation conversation; the feedback data logged in the follow-up tracker guides the counsellor's next conversation approach, not a generic script
- Demo class capacity (20 seats per session) is set to ensure each demo attendee gets personal attention from the counsellor post-class; a demo with 50 attendees cannot get individual post-demo conversations; the 20-seat limit also prevents too many non-students in the classroom, which disrupts the batch; if demand exceeds capacity for a demo slot, additional demo sessions are added to the calendar — leads are not overbooked into existing slots

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division F*
