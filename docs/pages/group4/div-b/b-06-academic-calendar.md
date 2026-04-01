# B-06 — Academic Calendar (Semester-Wise)

> **URL:** `/college/academic/calendar/`
> **File:** `b-06-academic-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Dean Academics (S5) — create and publish · Academic Coordinator (S4) · All staff + students — view

---

## 1. Purpose

The academic calendar defines the semester schedule — from orientation day to convocation — including class dates, mid-term exams, university exams, holidays, and key deadlines. Published before the semester begins.

NAAC requirement: Academic calendar must be prepared and published in advance; it is a basic academic governance indicator (criterion 2.1).

---

## 2. Academic Calendar — Odd Semester 2026–27

```
ACADEMIC CALENDAR — ODD SEMESTER 2026–27
Greenfields College of Engineering
AICTE Approved | JNTU Hyderabad Affiliated

Semester start: 8 July 2026 (Wednesday)
Semester end: 30 November 2026 (Sunday)
Working days (theory): 90 days ✅ (UGC: ≥90 working days per semester)

KEY DATES:
  8 Jul 2026    Orientation Day — I Year students
  8 Jul 2026    Regular classes begin — II/III/IV year students
  28–29 Jul     Freshers' Welcome (evening events)
  15 Aug 2026   Independence Day — Holiday
  2 Sep 2026    Ganesh Chaturthi — Holiday (TS)
  1–5 Sep 2026  Mid-I Exams (theory + lab)
  14–18 Sep     Re-mid (for genuinely absent students with medical proof)
  2 Oct 2026    Gandhi Jayanti — Holiday
  20–26 Oct     Mid-II Exams (theory + lab)
  27 Oct        Dussehra — Holiday (if applicable)
  3 Nov         CIE marks entry deadline (for all faculty)
  4 Nov         CIE marks HOD approval deadline
  7 Nov         CIE submission to JNTU
  2 Nov 2026    Diwali — Holiday
  25 Nov        Last class day (Odd Semester)
  26–30 Nov     Study holidays (students self-study)
  1–10 Dec 2026 University Exams (JNTU Hyderabad)
  Jan 2027      Results (expected)

TOTAL ACADEMIC DAYS:
  Theory classes: 90 working days ✅
  Lab sessions: 30 sessions ✅
  Holidays: 12 (public) + 3 (college events) = 15

[Download calendar PDF]  [Export ICS for device calendar]
[Publish to all students and faculty] ← Principal approval required before publish
```

---

## 3. Even Semester 2026–27

```
ACADEMIC CALENDAR — EVEN SEMESTER 2026–27

Semester start: 8 January 2027 (Friday)
Semester end: 30 May 2027

KEY DATES:
  8 Jan 2027    Even semester classes begin
  26 Jan 2027   Republic Day — Holiday
  15–20 Feb     Mid-I Exams
  20 Mar        Ugadi — Holiday (TS)
  22–28 Mar     Mid-II Exams
  31 Mar        CIE marks entry deadline
  4 Apr         CIE submission to JNTU
  10 Apr        Last theory class day
  14 Apr        Dr. Ambedkar Jayanti — Holiday
  11–25 Apr     Study holidays
  1–20 May 2027 University Exams (JNTU)
  July 2027     Results
  Aug 2027      Supplementary exams (JNTU)

WORKING DAYS: 90 theory + 30 lab ✅
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/academic/calendar/` | Academic calendar (current year) |
| 2 | `POST` | `/api/v1/college/{id}/academic/calendar/` | Create calendar (Dean Academics) |
| 3 | `GET` | `/api/v1/college/{id}/academic/calendar/holidays/` | Holiday list |
| 4 | `GET` | `/api/v1/college/{id}/academic/calendar/ics/` | ICS export |
| 5 | `PATCH` | `/api/v1/college/{id}/academic/calendar/publish/` | Publish calendar (Principal approval) |

---

## 5. Business Rules

- Academic calendar must be published before the semester begins (NAAC criterion 2.1); a calendar published mid-semester is a process gap; EduForge shows the publication date and timestamp (NAAC assessors check this)
- Working days per semester: UGC mandates ≥90 working days per semester (180/year) for degree programmes; a semester with fewer than 90 working days must be reported to the affiliating university; the system counts actual working days (excluding holidays and exam days that are not teaching days) and alerts when the projection falls below 90
- Any deviation from the published calendar (holiday change, exam rescheduling) must be communicated to students at least 3 days in advance; last-minute changes cause operational chaos; EduForge's notification system sends bulk WhatsApp/email to all affected students when a calendar change is made

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division B*
