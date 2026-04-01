# N-07 — Parent-Teacher Meeting Booking (Parent View)

> **URL:** `/parent/ptm/`
> **File:** `n-07-ptm-booking.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P)

---

## 1. Purpose

Parents book PTM slots online instead of queuing at school. The booking integrates with F-05 (PTM Management) on the school side. Key features:
- View upcoming PTM dates and available time slots
- Book a 10-minute slot with the Class Teacher
- Optionally book additional slots with subject teachers (if school enables this)
- Receive confirmation and reminders
- View past PTM notes (if Class Teacher enters feedback after the meeting)

---

## 2. PTM Schedule View

```
PTM BOOKING — Rahul Rao (Class X-A)
Class Teacher: Mr. Deepak C.

UPCOMING PTM:
  PTM for Class X: Monday, 6 April 2026
  Venue: School — Section X-A Classroom (Room 8)
  PTM hours: 9:00 AM – 12:30 PM

YOUR BOOKING STATUS: ⚠ Not yet booked

AVAILABLE SLOTS — 6 April 2026 (Mr. Deepak C., Room 8):
  9:00 AM  — Available
  9:10 AM  — Available
  9:20 AM  — BOOKED
  9:30 AM  — Available  ← [Book this slot]
  9:40 AM  — Available
  9:50 AM  — BOOKED
  10:00 AM — Available
  [... 12:20 PM — Available]

  [Book 9:30 AM slot for Rahul Rao + parent (Mrs. Sunita Rao)] ← Tap to confirm

SUBJECT TEACHER SLOTS (optional — if school enables):
  Mr. Ravi K. (Physics): 10:00–11:00 AM — 4 slots available [Book →]
  Ms. Priya M. (Maths): 11:00 AM–12:00 PM — 6 slots available [Book →]
```

---

## 3. Booking Confirmation

```
PTM BOOKING CONFIRMED ✅

  Meeting: Class X PTM — 6 April 2026
  Time: 9:30 AM – 9:40 AM (10 minutes)
  Teacher: Mr. Deepak C. (Class Teacher, X-A)
  Room: Room 8
  Parent: Mrs. Sunita Rao
  Student: Rahul Rao (Class X-A)

Reminders will be sent:
  ✅ 2 days before: 4 April (WhatsApp)
  ✅ 2 hours before: 6 April, 7:30 AM (WhatsApp)

[Cancel booking] ← Available until 5 April 12:00 noon
[Add to calendar] ← ICS file download for Google Calendar / Apple Calendar

PREPARATION TIPS:
  ● Review Rahul's report card (N-03) before the meeting
  ● Note any specific subjects or concerns to discuss
  ● 10 minutes — focus on 2–3 key topics
```

---

## 4. Past PTM Feedback

```
PAST PTM RECORDS — Rahul Rao

  Date         Teacher        Notes from Meeting
  ─────────────────────────────────────────────────────────────────────────
  15 Nov 2025  Mr. Deepak C.  "Rahul is performing well overall. Hindi needs
                               attention — suggest additional practice at home.
                               Attendance is good. Active in class."
               [Parent feedback to school: "Will work on Hindi. Thank you."]

  12 Aug 2025  Mr. Deepak C.  "Good start to the year. Needs to be more regular
                               with homework submission. Science project was excellent."

  (Previous PTM notes available for last 2 academic years)
```

---

## 5. Virtual PTM (if school enables)

```
VIRTUAL PTM OPTION (schools may enable for parents who cannot attend in person)

  Virtual PTM: Schools can enable Google Meet / Jitsi Meet links for remote PTM
  Parent books slot as normal; receives video call link instead of room number
  [Join Meeting at 9:30 AM] ← link active 5 minutes before slot
  Note: Most CBSE schools in India prefer in-person PTM; virtual is supplementary
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/ptm/upcoming/` | Upcoming PTM events and slots |
| 2 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/ptm/slots/?date={date}&teacher={id}` | Available slots |
| 3 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/ptm/book/` | Book a PTM slot |
| 4 | `DELETE` | `/api/v1/parent/{parent_id}/child/{student_id}/ptm/booking/{booking_id}/` | Cancel booking |
| 5 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/ptm/history/` | Past PTM records and notes |

---

## 7. Business Rules

- Slot booking is first-come, first-served; once booked, the slot is locked for that parent; double-booking is prevented at the data level
- Cancellations are allowed until noon of the day before the PTM; after that, the slot is freed back to the pool but the parent cannot rebook (the slot may be taken by a walk-in parent); this prevents last-minute no-shows that waste the teacher's time
- PTM meeting notes entered by the Class Teacher after the meeting are visible to the parent in the past PTM history (N-07) and to the school in the F-05 module; the teacher has the discretion to keep internal notes (for their own reference) separate from the notes shared with parents; only the shared notes appear in the parent view
- A parent who has not booked a PTM slot within 48 hours of the PTM receives a reminder push notification and WhatsApp message ("PTM is coming up — book your slot now [link]"); this ensures maximum participation
- PTM attendance by parents is tracked at the school level (F-05); a parent who has missed 3 or more consecutive PTMs for the same child may be flagged for welfare follow-up (some absence from PTM correlates with disengaged parenting and student welfare issues)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
