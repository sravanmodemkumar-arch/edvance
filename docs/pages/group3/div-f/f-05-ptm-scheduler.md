# F-05 — PTM Scheduler

> **URL:** `/school/ptm/schedule/`
> **File:** `f-05-ptm-scheduler.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Communication Coordinator (S3) — schedule · Class Teacher (S3) — own class slot management · Academic Coordinator (S4) — school-wide coordination · Principal (S6) — approve schedule, opening address slot · Parent — book slot via parent portal

---

## 1. Purpose

PTM (Parent-Teacher Meeting) is a critical school-parent engagement event. CBSE recommends a minimum of 2 PTMs per academic year (typically after mid-term results and before annual exams). Many schools conduct 3-4 PTMs. Indian PTM characteristics:
- **Slot-based scheduling:** Each parent gets a 10-15 minute slot with the class teacher; overflow is managed by limiting slots per teacher
- **Multiple teachers:** For Classes IX–XII, parents may want to meet subject teachers (Physics, Chemistry, Mathematics) in addition to the class teacher
- **Virtual PTM option:** Post-COVID, some schools offer hybrid PTM (in-person + video call slots)
- **Result review:** PTM typically coincides with report card distribution — parents see marks and discuss with teacher
- **Absentee parents:** 20-30% of parents typically don't attend PTM; follow-up is required for students with academic/attendance concerns
- **PTM is mandatory for students in CBSE condonation zone** (E-11): parents of such students must meet the Principal

---

## 2. Page Layout

### 2.1 Header
```
PTM Scheduler                                        [+ Schedule New PTM]  [View All PTMs]
Academic Year: [2026–27 ▼]

Next PTM: Annual PTM — 9 Mar 2026 (Today)
  Status: In progress  ·  Slots confirmed: 312/380 (82%)  ·  In progress: 12 slots

Completed PTMs this year: 2 (Term 1 PTM in Sep 2026, Pre-exam PTM in Dec 2026)
```

### 2.2 PTM List
```
PTM Name                     Date(s)       Type        Slots   Confirmed  Status
Annual PTM 2026-27           9 Mar 2026    In-person   380     312/380    🟢 In Progress
Pre-Board PTM (X & XII)      20 Jan 2027   In-person   160     155/160    ✅ Completed
Term 1 Result PTM            22 Oct 2026   In-person   380     290/380    ✅ Completed
```

---

## 3. Create PTM

```
[+ Schedule New PTM] → multi-step form:

Step 1 — Basic Details
  PTM Name: [Annual PTM 2026-27                    ]
  Date: [9 March 2026]  ·  Day: Sunday (recommended — parents available)
  Duration: [9:00 AM] to [1:00 PM]

  Type:
    ● In-person (at school)
    ○ Virtual (video call — Google Meet / Zoom)
    ○ Hybrid (in-person + virtual slots)

  Scope:
    ● All classes
    ○ Specific sections: [Select classes]

  Report card distribution: ☑ Yes (reports distributed during PTM)

Step 2 — Slot Configuration
  Slot duration: [15 minutes ▼]
  Break after every: [5 slots] → 5-minute break
  Class Teacher slots per class: [auto: based on class strength + duration]
    → XI-A (45 students, 15 min slots) = 45 × 15 min = 11.25 hours
    → Actual window: 4 hours → 16 slots × 15 min = 240 min = 4 hours
    → Students per slot: 3 (group batching) OR individual (if time permits)
    → Individual slots: ☑ Yes (recommended for Classes X and XII)

  Subject teacher meetings (for Classes IX–XII):
    ☑ Add subject teacher slots (optional — parents choose up to 2 subject teachers)
    Available teachers: [Physics — Mr. Arun  ·  Chemistry — Ms. Priya  ·  ...]
    Subject slot duration: [10 minutes]

Step 3 — Room Assignment
  Class XI-A   →  Room 101 (Ms. Anita Reddy)
  Class XI-B   →  Room 102 (Mr. Ravi Kumar)
  Class XII-A  →  Room 201 (Ms. Lakshmi)
  [+ Assign Rooms]

Step 4 — Invitation
  ☑ Send WhatsApp invitation with booking link (F-03)
  ☑ Post on F-01 Notice Board
  Send 7 days before PTM: 2 March 2026

  [Preview Invitation]

Step 5 — Special requirements
  ☑ Flag parents of below-75% attendance students (E-09) — mandatory attendance note in their invite
  ☑ Flag parents of academically at-risk students (B-18) — "Your presence is especially requested"
  ☑ Require Principal meeting for: condonation zone students (E-11)

[Save Draft]  [Publish & Send Invitations]
```

---

## 4. Slot Booking (Parent Portal Side)

Parents book their own slot via the parent portal:

```
Annual PTM — Slot Booking (Parent Portal View)
Arjun Sharma — Class XI-A — 9 March 2026

Available slots — Class Teacher Ms. Anita Reddy:
  ○ 9:00 AM – 9:15 AM  (2 of 3 slots taken)
  ● 9:15 AM – 9:30 AM  [Book This Slot]
  ○ 9:30 AM – 9:45 AM  (Available)
  ○ 10:00 AM – 10:15 AM (Available)
  [View all slots ▼]

Optional — Subject teacher slots (up to 2):
  ○ Physics (Mr. Arun):     9:00 AM / 9:10 AM / 9:20 AM ...
  ○ Mathematics (Ms. Kavitha): 9:00 AM / 9:10 AM ...
  ○ Chemistry (Ms. Priya):  9:30 AM / 9:40 AM ...

[Confirm Booking]
```

After booking:
```
✅ Slot Confirmed — Annual PTM

Class Teacher: Ms. Anita Reddy — XI-A
Your slot: 9:15 AM – 9:30 AM
Date: Sunday, 9 March 2026
Venue: Room 101, First Floor
Report card: Will be handed out during your slot.

[Add to Calendar]  [Get Directions]

A WhatsApp confirmation has been sent to +91 XXXXX XXXXX
```

---

## 5. Admin Slot Management View

```
Slot Status — Annual PTM — Class XI-A (Ms. Anita Reddy)
Room 101 · 9:00 AM – 1:00 PM · Total: 16 slots

Time       Student               Parent          Status       Notes
9:00 AM    Anjali Das            Mr. Raghav Das   ✅ Booked
9:15 AM    Arjun Sharma          Mr. Rajesh Sharma ✅ Booked
9:30 AM    Chandana Rao          Mrs. Vimala Rao   ⚠️ Booked (attendance alert — must attend)
9:45 AM    —                     —                 ⬜ Available
10:00 AM   Priya Venkat          Mrs. Geetha V.    ✅ Booked
...
12:45 PM   Kavya P.              —                 ❌ Not booked (parent not responded)

Unbooked slots: 4
Students whose parents haven't booked:
  Kavya P. (XI-A), Vijay S. (X-B)...
  [Send reminder to unbooked parents]  [Assign walk-in slots]
```

---

## 6. Walk-In & On-Day Management

```
PTM On-Day View — 9 March 2026 — Running

Currently in meeting: Ms. Anita — Arjun Sharma's parent (9:15 slot)
Next slot: 9:30 (Chandana Rao — flag: ⚠️ attendance concern)
Queue: 2 walk-in parents waiting

Walk-in token system:
  [Issue Walk-In Token]  → Token W-01, W-02...
  Walk-ins are assigned to available slots or post-regular slots

Check-in:
  [Check In Parent] → parent scans QR or staff marks arrival
  ✅ Arjun Sharma's parent — checked in 9:12 AM (3 min early)
  ❌ Chandana Rao's parent — not arrived yet (slot is 9:30)
    [Mark slot as missed → available for walk-in]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/ptm/?year={y}` | PTM list |
| 2 | `POST` | `/api/v1/school/{id}/ptm/` | Create PTM |
| 3 | `GET` | `/api/v1/school/{id}/ptm/{ptm_id}/slots/?class_id={id}` | Slot availability |
| 4 | `POST` | `/api/v1/school/{id}/ptm/{ptm_id}/slots/book/` | Book slot (parent/admin) |
| 5 | `DELETE` | `/api/v1/school/{id}/ptm/{ptm_id}/slots/{slot_id}/cancel/` | Cancel slot |
| 6 | `POST` | `/api/v1/school/{id}/ptm/{ptm_id}/check-in/` | Check in parent on the day |
| 7 | `GET` | `/api/v1/school/{id}/ptm/{ptm_id}/status/` | Real-time PTM status |
| 8 | `POST` | `/api/v1/school/{id}/ptm/{ptm_id}/remind-unbooked/` | Send reminders to unbooked |

---

## 8. Business Rules

- PTM slots are released to parents 7 days before the PTM; first-come first-serve booking
- For parents of students in the condonation zone (E-11) or academic at-risk list (B-18), booking is flagged as mandatory; if they don't book 2 days before PTM, an escalation WhatsApp is sent
- Walk-in parents are accommodated in available slots or after the scheduled session ends; they cannot displace booked parents
- Virtual PTM slots use auto-generated Google Meet links (one unique link per slot) — links expire 2 hours after the slot time
- PTM is recorded in F-07 PTM Outcome Register after the event; any parent who didn't attend has their key discussion points noted for follow-up communication
- DPDPA: Slot information is visible only to the relevant parent (parent cannot see other students' slots); teacher can see all slots for their class

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
