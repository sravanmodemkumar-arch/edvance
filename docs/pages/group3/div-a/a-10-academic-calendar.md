# A-10 — Annual Academic Calendar

> **URL:** `/school/admin/calendar/`
> **File:** `a-10-academic-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — full · VP Academic (S5) — full · VP Admin (S5) — view + add events · Admin Officer (S3) — view · All staff (S3+) — view

---

## 1. Purpose

The master academic calendar for the school year. Every scheduled event — holidays, exam dates, PTM, sports day, annual day, competition dates, CBSE inspection visits, fee deadlines — lives here. The calendar drives:
- Attendance module (holidays = no attendance required)
- Exam module (exam dates auto-populated)
- Communication module (calendar events trigger reminders to parents and staff)
- Student and parent portal (they see a public-facing version of this calendar)
- Reporting (academic weeks worked, teaching days vs total days)

**Indian calendar complexity:**
- Academic year spans 2 fiscal years (April 2025 to March 2026)
- Multiple public holiday types: Central govt · State govt · School-declared
- Regional festivals vary by state: Ugadi/Gudi Padwa/Vishu/Poila Baishakh (all regional New Years on different dates)
- CBSE schools follow Central government holidays list + some state holidays
- State board schools follow state government holiday list
- Some schools have unique local holidays (e.g., Founder's Day, school patron's birthday)

---

## 2. Page Layout

### 2.1 Header
```
Annual Academic Calendar — 2025–26          [+ Add Event]  [Print Calendar]  [Export ICS]  [View]
                                                                                 [Month ▼] [Week] [List]
```

**[View] toggles between:**
- Month grid (default)
- Week view (for detailed planning)
- List/Agenda view (compact text list — useful for printing)

---

## 3. Calendar Views

### 3.1 Month View

Standard month grid. Events shown as colour-coded blocks:

| Colour | Event Type |
|---|---|
| 🔴 Red | Public Holiday (no school) |
| 🟠 Orange | School Holiday (school-declared, no classes) |
| 🔵 Blue | Examination |
| 🟢 Green | Special Event (Annual Day, Sports Day, Science Fair, etc.) |
| 🟡 Yellow | PTM / Parent Communication |
| 🟣 Purple | CBSE/Board Visit, External Event |
| ⚫ Dark | Teacher Training / Professional Development Day |
| 🩶 Grey | Fee Deadline |

Multi-day events shown as spanning blocks.

Today's date highlighted. Days with no school (holidays, Sundays) greyed out.

### 3.2 Week View

7-column time grid (8 AM – 5 PM). Shows:
- Regular school schedule as background
- Events as overlay blocks

### 3.3 List/Agenda View

| Date | Day | Event | Type | Duration | Target Audience |
|---|---|---|---|---|---|
| 1 Apr 2025 | Tue | New Academic Year Begins | School Event | — | All |
| 14 Apr 2025 | Mon | Dr. Ambedkar Jayanti (Central) | Public Holiday | 1 day | All |
| 14 Apr 2025 | Mon | Tamil New Year / Vishu / Baisakhi | Regional Holiday | 1 day | State-specific |
| 1 May 2025 | Thu | Maharashtra/Gujarat Formation Day | State Holiday (state-specific) | 1 day | Applicable states |
| 15 Aug 2025 | Fri | Independence Day | National Holiday | 1 day | All |
| 26 Sep 2025 | Fri | First Formative Assessment — Class VI–X | Examination | 5 days | VI–X |
| 5 Oct 2025 | Sun | World Teachers' Day | School Event | 1 day | Staff appreciation |
| 2 Nov 2025 | Sun | Diwali (Central/State) | Public Holiday | 3–5 days | All |
| 15 Jan 2026 | Thu | Makar Sankranti/Pongal/Uttarayan | Regional Holiday | 1–3 days | State-specific |
| 26 Jan 2026 | Mon | Republic Day | National Holiday | 1 day | All |
| 10 Mar 2026 | Tue | Holi (Central) | Public Holiday | 1 day | North India |
| 1–31 Mar 2026 | — | Board Practical Exams — Class XII | Board Exam | Multiple days | XII |
| 15–31 Mar 2026 | — | Final Term Exams — All Classes | Examination | 2 weeks | All |
| 31 Mar 2026 | Tue | Academic Year End | School Event | — | All |

---

## 4. Event Creation

**[+ Add Event] drawer (480px):**

| Field | Description |
|---|---|
| Event Name | Free text |
| Event Type | Holiday · Examination · PTM · Special Event · Board Visit · Fee Deadline · Teacher Training · Custom |
| Start Date | Date picker |
| End Date | Date picker (or single-day toggle) |
| Applies to | All classes · Specific classes (multi-select) · Specific streams · Staff only |
| School open? | Yes (event on school day) · No (holiday — no attendance) |
| Notify? | Parents · Staff · Both · None (toggle per group) |
| Notification advance | 7 days / 3 days / 1 day before (multi-select) |
| Note / Description | Free text |

**Recurring events:**
- Annual fixed: Independence Day, Republic Day (auto-populated from EduForge calendar)
- Custom recurring: [+ Add Recurrence Rule] (daily/weekly/monthly/annually)

---

## 5. Holiday Import

**[Import Holidays] button:**
- Select Board: CBSE · ICSE · TS State Board · AP State Board · …
- Select Year: 2025–26
- EduForge pre-loads the standard Central/State government holiday list for the board
- School reviews and can delete/modify before confirming import
- Regional holidays filtered by school's state (from institution profile)

---

## 6. Working Days Counter

**Persistent banner at top of calendar:**
```
Academic Year 2025–26:  220 Total Working Days  ·  78 Sundays  ·  21 Holidays  ·  67 days elapsed  ·  153 days remaining
```

CBSE requirement: minimum 220 working days per academic year. Counter turns red if working days < 220.

Per-class working days (for classes with different schedules):
- Pre-Primary: often 190–200 days
- Senior Secondary: full 220 days

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/calendar/` | All events for academic year |
| 2 | `POST` | `/api/v1/school/{id}/calendar/events/` | Create event |
| 3 | `PATCH` | `/api/v1/school/{id}/calendar/events/{event_id}/` | Update event |
| 4 | `DELETE` | `/api/v1/school/{id}/calendar/events/{event_id}/` | Delete event |
| 5 | `POST` | `/api/v1/school/{id}/calendar/import-holidays/` | Import board holiday list |
| 6 | `GET` | `/api/v1/school/{id}/calendar/working-days/` | Working days count |
| 7 | `GET` | `/api/v1/school/{id}/calendar/export.ics` | ICS file for calendar apps |

---

## 8. Business Rules

- Deleting a holiday that has already been communicated to parents → block with warning: "This holiday was sent to 842 parents. Deleting will not auto-notify them. Consider modifying instead."
- Examination events created here auto-populate in div-f Exam Module (not vice versa — exam module creates its own detailed exam schedule; calendar shows the block only)
- Holiday on which attendance was already marked → flag for Principal review (someone marked attendance on a holiday accidentally)
- Minimum 220 working days validation: if below threshold → amber warning on Principal Dashboard (A-02) + Promoter Dashboard (A-01)
- ICS export available to all staff (for syncing to personal calendar apps); parents see a read-only version in parent portal

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
