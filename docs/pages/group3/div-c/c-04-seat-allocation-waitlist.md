# C-04 — Seat Allocation & Waitlist

> **URL:** `/school/admissions/seat-allocation/`
> **File:** `c-04-seat-allocation-waitlist.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Admission Officer (S3) — full · Academic Coordinator (S4) — full · Principal (S6) — full

---

## 1. Purpose

Manages the final seat confirmation process — deciding which candidates from the merit list get seats, which go on the waitlist, and which are rejected. For Indian schools, this is more nuanced than a simple cutoff because:
- Multiple category reservations (SC/ST/OBC-NCL) operate simultaneously
- RTE 25% seats are already allocated via C-07 and must be excluded from general calculation
- Sibling priority candidates may bypass merit rank
- Management quota seats (a discretionary pool, school-configurable) may exist
- For Class XI, seats may be split across streams (Science/Commerce/Arts) with different cutoffs

This page also manages the waitlist, which is critical because Indian parents often confirm at multiple schools and withdraw last-minute (especially after CBSE board results in May, when XI seat requests spike). The Admission Officer must be able to quickly move a waitlisted candidate to confirmed when a seat opens.

---

## 2. Page Layout

### 2.1 Header
```
Seat Allocation — 2026–27                     [Allocate Seats]  [Move Waitlist]  [Export]
Class: [All ▼]

Class    Total  RTE  General  Mgmt  Filled  Waitlisted  Available
Nursery    40    10    25      5      38        6           2
LKG        40    10    25      5      28        4          12
Class I    40    10    25      5      40        8           0  ← FULL
Class IX   60     0    55      5      51        7           4
XI-Science 60     0    55      5      52        9           3
XI-Commerce 40    0    35      5      30        5           5
```

---

## 3. Class-wise Seat Allocation View

Clicking a class row opens the detailed allocation view:

```
Class XI — Science Stream  |  Total Seats: 60  |  Confirmed: 52  |  Available: 8
──────────────────────────────────────────────────────────────────────────────────

Category Breakdown:
  General (merit):  45 seats  |  Filled: 38  |  Available: 7
  SC:                5 seats  |  Filled:  4  |  Available: 1
  ST:                2 seats  |  Filled:  2  |  Available: 0
  OBC-NCL:           3 seats  |  Filled:  3  |  Available: 0
  Management Quota:  5 seats  |  Filled:  5  |  Available: 0

Merit List (General — Confirmed):
Rank  Applicant        Score   Category  Status         Confirmation Deadline
1     Priya Venkat     192/230  General  ✅ Confirmed   —
2     Arjun Sharma     161/230  OBC-NCL  ✅ Confirmed   —
3     Meera Sharma     156/230  General  ✅ Confirmed   —
...
38    Kavya P.         118/230  General  ✅ Confirmed   —

Pending Confirmation:
39    Suresh K.        115/230  General  ⏳ Offer Made  [Confirm] [Reject]  Deadline: 28 Mar
40    Ravi T.          112/230  General  ⏳ Offer Made  [Confirm] [Reject]  Deadline: 28 Mar

Waitlist:
WL-1  Anitha S.       108/230  General  ⏳ Waitlist    [Offer Seat]
WL-2  Dinesh R.       105/230  General  ⏳ Waitlist    [Offer Seat]
WL-3  Preethi M.      104/230  General  ⏳ Waitlist    [Offer Seat]
```

---

## 4. Offer Letter Generation

When a candidate is selected from the merit list, an offer letter is generated and sent:

```
ADMISSION OFFER LETTER
[School Logo]

Dear Mr./Ms. [Parent Name],

We are pleased to inform you that [Student Name] has been selected for admission
to Class XI — Science Stream for the academic year 2026–27.

Seat Details:
  Class: XI — Science Stream (PCM)
  Merit Rank: 39 (General Category)
  Offer Valid Until: 28 March 2026

To confirm admission, please:
1. Visit the school office and pay the admission fee of ₹25,000
2. Submit all original documents (see checklist attached)
3. Collect the enrollment form

Note: Your seat will be forfeited if not confirmed by 28 March 2026.
Waitlisted candidates will be offered your seat automatically.

Principal
[School Name]
```

Delivery: WhatsApp message with PDF + Email (if available).

---

## 5. Waitlist Management

### 5.1 Waitlist Position
Each waitlisted candidate has a position (WL-1 is first to be offered when a seat opens).

### 5.2 Seat Opens (Withdrawal / No-Show)
When a confirmed candidate withdraws or the offer deadline passes without confirmation:
1. Seat marked Available
2. System auto-prompts: "[Class XI Science] Seat opened — WL-1 Anitha S. is next. [Offer Seat Now]"
3. Admission Officer clicks [Offer Seat] → offer letter sent to WL-1
4. WL-2 becomes WL-1

### 5.3 Waitlist Notification
Waitlisted candidates receive: "Dear [Parent], [Student Name] is on the waitlist for Class XI Science (Position: WL-3). You will be notified if a seat becomes available. Current confirmed count: 52/60."

---

## 6. Confirmation Deadline Tracking

| Status | Meaning | Auto-action |
|---|---|---|
| Offer Made | Seat offered; awaiting confirmation | Reminder 2 days before deadline |
| Deadline Passed (no confirm) | Parent didn't respond | Seat released; next on waitlist offered |
| Confirmed | Parent confirmed + fee paid | Enrollment in C-05 enabled |
| Withdrawn | Parent declined after offer | Seat released; next offered |

---

## 7. Management Quota

Schools (especially unaided private schools) may reserve a small number of seats for management discretion (trustees' nominees, staff children beyond normal priority, etc.). Management quota seats:
- Are displayed separately in the seat count
- Can only be allocated by Principal (not Admission Officer)
- Do NOT participate in merit-based allocation
- Require Principal note/justification when allocating

---

## 8. Class XI Stream Change

For Class XI, a student admitted to Science stream can request a switch to Commerce or Arts before formal enrollment if the desired stream has seats:
- [Allow Stream Switch] — Principal/Academic Coordinator action
- Original stream seat released to next on waitlist
- New stream seat allocated

---

## 9. Confirmation Summary Report

[Export] → Seat Allocation Report:
```
SEAT CONFIRMATION STATUS — 2026–27
[School Name]  |  As of 28 Mar 2026

Class       Total  RTE  Confirmed  Waitlisted  Available  Conversion%
Nursery       40    10      38          6           2         95%
LKG           40    10      28          4          12         70%
Class I       40    10      40          8           0        100%  FULL
Class IX      60     0      51          7           4         85%
XI-Science    60     0      52          9           8         87%
XI-Commerce   40     0      30          5          10         75%
──────────────────────────────────────────────────────────────────
TOTAL        280    30     239         39          36         85%
```

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/admissions/seat-allocation/?year={year}` | Seat summary all classes |
| 2 | `GET` | `/api/v1/school/{id}/admissions/seat-allocation/{class_id}/?year={year}` | Class-wise allocation detail |
| 3 | `POST` | `/api/v1/school/{id}/admissions/seat-allocation/{class_id}/offer/` | Send offer to candidate |
| 4 | `PATCH` | `/api/v1/school/{id}/admissions/seat-allocation/{candidate_id}/confirm/` | Mark candidate as confirmed |
| 5 | `PATCH` | `/api/v1/school/{id}/admissions/seat-allocation/{candidate_id}/withdraw/` | Withdraw candidate; trigger waitlist |
| 6 | `POST` | `/api/v1/school/{id}/admissions/seat-allocation/waitlist/{candidate_id}/offer/` | Offer seat to waitlisted candidate |
| 7 | `PATCH` | `/api/v1/school/{id}/admissions/seat-allocation/{candidate_id}/mgmt-quota/` | Allocate management quota seat (Principal only) |
| 8 | `GET` | `/api/v1/school/{id}/admissions/seat-allocation/export/?year={year}` | Export allocation report |

---

## 11. Business Rules

- RTE seats (25%) are managed separately in C-07 and are not part of this merit/waitlist pool; the available count shown here excludes RTE seats
- Management quota allocations require Principal-level action and are logged with justification note — CBSE inspectors may ask for management quota records
- Confirmation deadline is school-configurable (default: 7 days from offer letter date)
- If all general seats are filled but SC/ST seats remain unfilled (rare but possible), the system alerts the Academic Coordinator — unfilled reserved seats may need to be reported differently in UDISE
- A candidate cannot be on both General waitlist and SC/ST confirmed — category and rank determine the single allocation path

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
