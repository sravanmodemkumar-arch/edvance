# E-15 — Holiday & Working Day Manager

> **URL:** `/school/attendance/calendar-config/`
> **File:** `e-15-holiday-working-day-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Administrative Officer (S3) — propose holidays · Academic Coordinator (S4) — edit and manage · Principal (S6) — approve; only Principal can mark a working Saturday or change a notified holiday

---

## 1. Purpose

Defines which days are working days and which are holidays for the school. This is P0 because every other attendance calculation depends on this data:
- **E-01 daily attendance** is locked on holidays (cannot mark attendance on a holiday)
- **E-09 shortage alerts** uses remaining working days to compute max possible attendance
- **E-11 exam eligibility** computes 75% against this denominator
- **E-13 CBSE register** prints only working days
- **CBSE 220-day compliance** (E-10) counts against this calendar
- **A-10 Academic Year Planner** pulls from this as the authoritative working-day calendar

Any mistake in the holiday calendar cascades to exam eligibility, attendance certificates, and board exam registration — hence P0 and Principal approval required for changes.

---

## 2. Page Layout

### 2.1 Header
```
Holiday & Working Day Manager                    [+ Add Holiday]  [Add Working Day]  [Export Calendar]
Academic Year: [2026–27 ▼]

Working Days to Date: 198 / 220 (CBSE minimum)
Remaining Year: 2 days (28, 29 Mar 2026)
Projected Year-End: 200 days  ⚠️ 20 below CBSE 220 minimum
```

### 2.2 Calendar View Toggle
```
[Month View ▼]  ·  [List View]  ·  [CBSE 220-Day Counter]

MARCH 2026
Mo   Tu   We   Th   Fr   Sa   Su
                                1W   (W = working, standalone Saturday)
2W   3W   4W   5W   6W   7W   8—
9W  10W  11W  12W  13W  14W  15—
16W 17W  18W  19W  20W  21W  22—
23W 24W  25W  26W  27W  28W  29—
30H 31H                           (H = Holiday: Ram Navami + State holiday)

Legend: W=Working Day  H=Holiday  OH=Optional Holiday  WS=Working Saturday  —=Sunday
```

### 2.3 Holiday List
```
# | Date           | Day  | Holiday Name                  | Category       | Source      | Status
1 | 26 Jan 2026    | Mon  | Republic Day                  | National        | Central Govt | ✅ Published
2 | 14 Feb 2026    | Sat  | Pongal / Sankranti (state)    | State/Regional  | State Govt   | ✅ Published
3 | 29 Mar 2026    | Sun  | Good Friday (substitute Mon)  | National        | School       | ✅ Published
4 | 30 Mar 2026    | Mon  | Ram Navami                    | National        | Central Govt | ✅ Published
5 | 1 Apr 2026     | Wed  | Summer Vacation begins        | School closure  | School       | ✅ Published
  | 1 Apr–15 May   |      | Summer Vacation (45 days)     | School closure  | School       | ✅ Published

Working Saturdays:
1 | 7 Mar 2026     | Sat  | Compensation for Diwali extra | Principal order | School       | ✅ Published
2 | 14 Mar 2026    | Sat  | Compensation for Diwali extra | Principal order | School       | ✅ Published
```

---

## 3. Add Holiday

```
[+ Add Holiday] → drawer:

Date: [30 Mar 2026]
Holiday Name: [Ram Navami                          ]
Category:
  ● National Holiday (Negotiable Instruments Act / Gazette)
  ○ State Government Holiday (AP/TS/etc.)
  ○ Regional/Local Holiday (school discretion)
  ○ School Closure (administrative — e.g. Annual Day, Election duty)
  ○ Emergency Closure (flood, COVID, disaster)
  ○ Summer / Winter / Puja Vacation (multi-day)

Repeats: ○ One-time  ● Annual (auto-repeat next year with review)

Notification:
  ☑ Notify parents via WhatsApp / app: "School holiday on [Date] — [Name]"
  ☑ Notify staff
  Date to notify: [Immediately] / [3 days before] / [1 week before]

Effect:
  → E-01 daily attendance locked for this date
  → Not counted as working day in CBSE 220-day count
  → E-09 max-possible% recalculated for all at-risk students

Principal Approval: Required ☑

[Submit for Principal Approval]
```

---

## 4. Add Working Saturday / Compensatory Working Day

```
[Add Working Day] → drawer:

Date: [7 Mar 2026]   (Saturday — would normally be holiday)
Reason: [Compensation for extra Diwali break — Circular No. 45/2025]
Type:
  ● Working Saturday (attendance mandatory)
  ○ Optional Saturday (attendance counted if student comes, not penalised if absent)
  ○ Emergency working day (exam rescheduling, etc.)

Half day / Full day: ● Full day  ○ Half day (0.5 working day)

Classes: ● All classes  ○ Specific classes [XI-A, XI-B, XII-A, XII-B]

Announcement:
  ☑ Notify parents: "School will be open on [Date] — working Saturday"
  ☑ Notify all staff

Effect:
  → Added to E-01 as a working day (teachers must submit attendance)
  → Counted in CBSE 220-day total
  → E-09 max-possible% updated for all students

Principal Approval: Required ☑

[Submit for Principal Approval]
```

---

## 5. Emergency Closure

For unexpected closures (flood, cyclone, COVID protocol, election duty):

```
Emergency Closure — Instant Declaration

Date(s): [From: 14 Oct 2026] [To: 17 Oct 2026]
Reason: [Flood — District Collector order ref. Circular 2026/DC/142]
Authority ordering closure: ● District Collector  ○ State Government  ○ School decision

Retroactive: ☑ Yes (school already closed; now formalising in system)

Effect:
  → E-01 attendance for these dates: locked, status = Emergency Closure (EC)
  → Students marked neither Present nor Absent (EC days excluded from denominator)
  → CBSE 220-day count reduced — system will flag shortfall automatically
  → E-09 max-possible% recalculated

Principal (or Admin in emergency): Can apply without draft → approval → immediate effect

[Apply Emergency Closure Immediately]
```

---

## 6. CBSE 220 Working Days Compliance Tracker

```
CBSE 220 Working Days — 2026–27 — Live Count

Month        Planned  Conducted  Diff   Cumulative Conducted
April 2026     25        25       0          25
May 2026       20        20       0          45
June 2026      22        22       0          67
July 2026      24        24       0          91
August 2026    22        22       0         113
September 2026 21        21       0         134
October 2026   22        14      -8         148    ← Flood closure (14–17 Oct): -8 days
November 2026  22        22       0         170
December 2026  20        20       0         190
January 2027   23        23       0         213
February 2027  20        20       0         233    ← Crossed 220 ✅ (11 Feb 2027)
March 2027     20        —        —         —      (projected)

Compensatory working Saturdays added: 8
Adjusted year-end total (projected): 233

Status: ✅ CBSE 220-day requirement met (as of 11 Feb 2027)

Note: This projection uses A-10 academic calendar remaining holidays.
[View Shortfall Remediation Plan]  [Link to B-38 Academic Year Planner]
```

---

## 7. Vacation Period Manager

```
Vacation Periods — 2026–27

Name              From          To           Days   Effect
Summer Vacation   1 Apr 2026    15 May 2026   45    School closed; E-01 locked
Puja Holidays     1 Oct 2026    10 Oct 2026   10    School closed; E-01 locked
Diwali Break      2 Nov 2026    7 Nov 2026     6    School closed (2 extra days vs CBSE)
Winter Break      24 Dec 2026   3 Jan 2027    11    School closed
Term Break        1 Mar 2027    3 Mar 2027     3    Internal exam prep (working days)

[+ Add Vacation Period]
```

---

## 8. Calendar Publish & Communication

Once the academic year calendar is set:

```
[Publish Academic Calendar]

Publishing will:
  1. Lock E-01 on all holidays
  2. Send WhatsApp to all parents: "Academic Calendar 2026–27 attached"
  3. Post calendar PDF on parent portal (P-01)
  4. Update A-10 Academic Year Planner

Once published, individual holiday changes require Principal approval and parent re-notification.

[Generate Calendar PDF]  [Preview before Publish]  [Publish Now]
```

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/calendar/?year={y}` | Full calendar (working days + holidays) |
| 2 | `POST` | `/api/v1/school/{id}/attendance/calendar/holiday/` | Add holiday (requires Principal approval) |
| 3 | `POST` | `/api/v1/school/{id}/attendance/calendar/working-day/` | Add working Saturday/compensatory day |
| 4 | `POST` | `/api/v1/school/{id}/attendance/calendar/emergency-closure/` | Emergency closure (immediate) |
| 5 | `GET` | `/api/v1/school/{id}/attendance/calendar/220-day-count/?year={y}` | CBSE 220-day running count |
| 6 | `GET` | `/api/v1/school/{id}/attendance/calendar/working-days/?from={date}&to={date}` | Count working days in range |
| 7 | `POST` | `/api/v1/school/{id}/attendance/calendar/publish/?year={y}` | Publish calendar + notify parents |
| 8 | `GET` | `/api/v1/school/{id}/attendance/calendar/pdf/?year={y}` | Academic calendar PDF |

---

## 10. Business Rules

- A date once marked as holiday and published cannot be reversed without Principal approval — this is because parents have been notified and students may have made travel plans
- Emergency closures ordered by District Collector or State Government are entered by Admin Officer (Principal may be unavailable during the emergency); these are retroactively approved when normalcy returns
- Working Saturdays are mandatory working days; students absent on a working Saturday are marked absent in E-01 and the absence counts against their attendance percentage
- Optional Saturdays: student gets credit for attendance if present; not counted against them if absent (denominator excludes optional Saturdays by default unless student was present)
- CBSE 220-day requirement is computed from actual conducted working days, not planned; if the school falls short, CBSE may ask for explanation during affiliation renewal
- Summer, Puja, and other vacation periods automatically lock E-01 for all dates in the period; Class Teachers do not need to take attendance during vacations
- The calendar for the next academic year must be published before the new academic year begins (during April of the current year) so that fee structure, exam schedules, and PTM dates can be planned

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
