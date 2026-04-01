# K-11 — School Calendar Compliance (220 Days)

> **URL:** `/school/compliance/calendar/`
> **File:** `k-11-school-calendar-compliance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Coordinator (S4) — primary manager · Principal (S6) — approve and sign calendar · Administrative Officer (S3) — maintain working day count · Compliance Officer (S4) — CBSE compliance verification

---

## 1. Purpose

Ensures the school meets the CBSE mandatory 220 working days requirement per academic year, and that the school calendar is properly planned, published, and documented. This is both a compliance requirement (CBSE deducts marks from defaulting schools and may raise affiliation concerns) and an academic planning necessity.

Key CBSE requirements:
- **220 working days** per academic year (school day = school in session with instruction; not examination-only days, cultural days without instruction, or holidays)
- **Holidays:** National holidays (compulsory); state government holidays (as notified); school-declared holidays (limited)
- **Working day definition:** 5.5 hours of instruction minimum per working day for secondary schools
- **Calendar submission:** CBSE may require schools to submit the academic calendar to the regional office; state education departments also require calendar notification

---

## 2. Calendar Compliance Dashboard

```
School Calendar Compliance — 2026–27                 [View Full Calendar]  [Export for CBSE]
Academic Year: April 2026 – March 2027

Working days target: 220
Working days completed (as of 27 Mar 2026): 210
Remaining working days (school year ends 31 Mar 2027 for Classes I–XI): 10
Projected total: 220 ✅ (on track — exactly at target)

Class XII: Practical exams included; Board exam period from March 2026 — practical count includes
  Board practical days as working days for those classes.

Upcoming school closure risks:
  None anticipated — last 10 days are regular school days.

Summary:
  Working days: 210 confirmed + 10 planned = 220 ✅
  Holidays taken: 82 (national 14 + state 10 + summer vacation 45 + other 13)
  Emergency closures: 2 (1 flood warning Aug 2025; 1 bandh Sep 2025)
```

---

## 3. Working Day Count — Month by Month

```
Working Day Register — 2026–27

Month         Total Days  Holidays  Working Days  Running Total  Status
April 2026       30         7           23           23           ✅
May 2026         31        14           17           40           ✅
June 2026        30         4           26           66           ✅ (year start)
July 2026        31         5           26           92           ✅
August 2026      31         6           25           117          ✅
September 2026   30         6           24           141          ✅
October 2026     31        10           21           162          ✅ (Diwali + Dussehra)
November 2026    30         5           25           187          ✅
December 2026    31        14           17           204          ✅ (winter break)
January 2027     31         4           27           231          ✅ (above target)
February 2027    28         5           23           254          — (if continued)
...

Note: Working day count shown above is the full-year projected; individual school
  years end at Class XII Board exam; for Classes I–XI, the school year continues
  to March 2027 target.

Wait — standard Telangana CBSE school calendar:
  Classes I–XI: April 2026 to March 2027 — 220 days planned
  Class XII: April 2026 to February 2027 (Board practical in Feb; written in March)

Revised count (up to March 2027 for I–XI):
  Working days: 220 ✅

Emergency days recovered:
  Aug 2025 flood closure (1 day): Recovered by working on substitute Saturday (22 Aug) ✅
  Sep 2025 bandh (1 day): Recovered on substitute Saturday (27 Sep) ✅

[Export working day register]
```

---

## 4. Calendar Publication

```
Academic Calendar — 2026–27 Publication Status

Published: ✅ 15 March 2026 (before academic year start)

Published to:
  ☑ School website (public) ✅
  ☑ Parent portal (N-module) ✅
  ☑ F-01 notice board (physical + digital) ✅
  ☑ WhatsApp to all parents (F-03) ✅ (sent 20 March 2026)
  ☑ State education department (as required by TS Edu rules) — submitted Apr 2026

Calendar content:
  ● Working day calendar (month-wise)
  ● Holiday list (national + state + school declared)
  ● Term structure (Term 1: Jun–Sep; Term 2: Oct–Dec; Term 3: Jan–Mar)
  ● Examination schedule (Unit tests, mid-terms, annual)
  ● PTM schedule (F-05)
  ● Sports day, Annual day, cultural events
  ● Summer vacation dates (confirmed)
  ● Winter break dates (confirmed)

Mid-year calendar changes:
  Any change to the calendar (new holiday, date change) requires:
  ☑ Principal approval
  ☑ Parent notification via F-03 (5 days advance notice where possible)
  ☑ Working day count recalculation to ensure 220 is still achievable
  ☑ Updated calendar re-published on all channels

[View calendar as published]  [Modify calendar + recalculate days]
```

---

## 5. Holiday Classification

```
Holiday Classification — 2026–27

National Holidays (mandatory — cannot be school days):
  Independence Day (15 Aug), Republic Day (26 Jan), Gandhi Jayanti (2 Oct)
  Ambedkar Jayanti (14 Apr), Labour Day (1 May)
  Total: 5 mandatory national holidays ✅

State Holidays (as notified by TS Government):
  Ugadi, Sri Rama Navami, Eid ul-Fitr, Eid ul-Adha, Diwali, Muharram,
  Christmas, Bhogi, Sankranti, Milad-un-Nabi, etc.
  Total: ~15 state holidays (varies by year's notification) ✅

School-Declared Holidays:
  Annual Sports Day (no instruction — does not count as working day)
  Annual Day (no instruction — does not count)
  Exam days for students not appearing (school is open but affected classes are off)

Non-Working Days (scheduled):
  Summer vacation: 15 May – 15 June 2026 (32 days — state guideline for private schools)
  Diwali vacation: 28 Oct – 3 Nov 2026 (7 days)
  Winter break: 26 Dec – 2 Jan 2027 (8 days)

CBSE clarification: Days on which examinations are conducted AND instruction happens
  count as working days; days that are exclusively examination days (no teaching) are
  counted as working days per CBSE guidelines as long as the student's educational
  engagement is active.
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/compliance/calendar/dashboard/` | 220-day compliance status |
| 2 | `GET` | `/api/v1/school/{id}/compliance/calendar/working-days/` | Month-by-month working day count |
| 3 | `POST` | `/api/v1/school/{id}/compliance/calendar/holiday/` | Add holiday (recalculates count) |
| 4 | `DELETE` | `/api/v1/school/{id}/compliance/calendar/holiday/{id}/` | Remove holiday (recalculates) |
| 5 | `GET` | `/api/v1/school/{id}/compliance/calendar/export/` | Calendar export for CBSE/DEO |
| 6 | `POST` | `/api/v1/school/{id}/compliance/calendar/substitute-day/` | Log substitute working Saturday |

---

## 7. Business Rules

- The 220-day count in EduForge is the authoritative figure; if the school year-end projection drops below 220, a compliance alert is triggered and the Academic Coordinator must either add substitute working days or receive a compliance risk flag
- Emergency closures (flood, bandh, pandemic) that reduce the working day count must be "recovered" by scheduling substitute working Saturdays; each recovery day must be parent-notified via F-03 with ≥5 days notice
- Annual day and sports day: these are school events but they are NOT working days under CBSE definition unless substantive instruction occurs; schools that count event days as working days to reach 220 are misrepresenting the count — EduForge distinguishes "event days" from "working days"
- Calendar is published before the academic year starts (March of the prior year); CBSE requires this; a school that announces holidays at short notice (e.g., 1-day notice) without calendar authority is in violation of the advance parent notification requirement
- Working day counts are class-specific for Class XII (Board exam dates affect count); EduForge maintains separate counts for Classes I–XI and Class XII
- CBSE 220-day requirement is an absolute minimum; schools falling short must explain to the regional office; persistent shortfalls (2+ consecutive years) may attract affiliation conditions

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division K*
