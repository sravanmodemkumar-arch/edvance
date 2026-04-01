# E-01 — Daily Attendance (Class Teacher)

> **URL:** `/school/attendance/daily/{class_id}/`
> **File:** `e-01-daily-attendance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Class Teacher (S3) — own class (full) · Subject Teacher (S3) — read own class · Administrative Officer (S3) — full (corrections via E-03) · Academic Coordinator (S4) — read all · Principal (S6) — full

---

## 1. Purpose

The daily morning attendance marking interface for Class Teachers. In Indian schools, attendance is marked first thing in the morning (8:00–8:30 AM) as the Class Teacher takes roll call. This is a P0 operation — every downstream module (attendance reports, exam eligibility, parent notifications, CBSE compliance) depends on daily attendance data.

Key features needed for Indian school context:
- **Speed:** Class Teacher needs to mark 40 students in under 3 minutes. Grid layout with keyboard navigation (arrow keys + P/A/L) is essential
- **Absent alert:** As soon as a student is marked absent, a WhatsApp/SMS alert fires to parent (configurable delay: instant / 9 AM batch / 10 AM batch)
- **Late arrival:** Students who arrive after roll call can be updated to "Late" during the day
- **Offline support:** If the school has poor connectivity, attendance should work offline and sync when connectivity returns (IndexedDB/service worker)
- **Holiday lock:** On holidays/Sundays, marking is blocked
- **Previous day catch-up:** Class Teacher can mark attendance for previous working day (if they forgot) up to 48 hours back — requires Academic Coordinator approval beyond 48 hours
- **Half-day:** Some schools mark morning + afternoon separately (especially for half-day sessions on Saturdays)

---

## 2. Page Layout

### 2.1 Header
```
Daily Attendance — Class XI-A                 Thursday, 27 March 2026
Class Teacher: Ms. Anita Reddy   ·   Students: 38   ·   Working Day #198 of 220

[Mark Attendance]  [Copy Previous Day]  [View Report]  [Export]

Status: ⬜ Not yet marked today (8:05 AM — mark before 9:30 AM)
```

### 2.2 Quick Summary Bar
```
Yesterday (26 Mar):  Present: 35  ·  Absent: 2  ·  Late: 1  ·  Attendance: 92.1%
This Week (Mon–Wed): Avg 91.4%   ·   This Month (Mar): Avg 89.8%
```

### 2.3 Attendance Grid

```
Class XI-A — 27 March 2026 (Thursday)

Roll  Name                  Status    Remarks
──────────────────────────────────────────────────────────────────────
01    Anjali Das            [P][A][L]  _______________
02    Arjun Sharma          [P][A][L]  _______________
03    Bharath Kumar         [P][A][L]  _______________
04    Chandana Rao          [P][A][L]  _______________
05    Dinesh Reddy          [P][A][L]  _______________
...
38    Zara Ahmed            [P][A][L]  _______________
──────────────────────────────────────────────────────────────────────
```

**Keyboard shortcuts:**
- `P` = Present, `A` = Absent, `L` = Late
- Arrow Down / Enter = move to next student
- `Ctrl+P` = Mark all Present (bulk; still shows each row)
- `Ctrl+S` = Save draft (auto-saves every 30 seconds)

**Status colour coding:**
- Present = green row
- Absent = red row + parent notification queued
- Late = amber row
- Holiday = grey (no marking)

### 2.4 Bulk Actions
```
[Mark All Present]  [Mark All Absent]  [Reset All]
Apply to selected: [☑ Select All]
```

---

## 3. Save & Submit

Two-stage save:
1. **Draft (auto-save every 30s):** Saves without locking; Class Teacher can still edit
2. **Submit:** Locks the attendance for the day; triggers parent notifications; feeds analytics

```
Submit Attendance — 27 March 2026

Summary:
  Present: 36  ·  Absent: 2  ·  Late: 0  ·  Not marked: 0
  Attendance %: 94.7%

Absent students — notifications will be sent:
  • Arjun Sharma — parent notified via WhatsApp (9876543210)
  • Rohit Kumar — parent notified via WhatsApp (9876501234)

[Confirm Submit]  [Back to Edit]
```

After submit: form is read-only; any corrections go through E-03 (Attendance Correction Register).

---

## 4. Absent Student Detail

Clicking an absent student's row shows:
```
Arjun Sharma — Roll 02 — 27 Mar 2026 — ABSENT

Attendance This Month (March 2026):
  Present: 14/17 (82.4%)  ·  Absent: 3  ·  Late: 0

Consecutive absences: 1 day (today only)

Actions:
  [View full attendance history]
  [Apply Leave on behalf] → links to E-04
  [Call parent now — 9876543210]
  [Mark as Late (if arrived after roll call)]
```

---

## 5. Late Arrival Update

After morning roll call, if a student arrives late:
```
[Update Late Arrival] → search student by name/roll
  Arjun Sharma — arrived 9:45 AM (marked Absent at 8:15 AM)
  Update to: ● Late (arrived 9:45 AM)  ○ Present (was at school event)
  Reason: Dental appointment — parent note submitted
  [Update]
```
Late arrival updates are recorded in E-06 Late Arrival Register automatically.

---

## 6. Half-Day Attendance (Saturday / Short Day)

If academic calendar (A-10) marks the day as "Half Day":
```
Half-Day Session — Saturday, 28 March 2026

Mark: ● Full Present  ○ Morning Only  ○ Absent

Note: Half-day counts as 0.5 working day in attendance percentage computation.
```

---

## 7. Previous Day Catch-up

If a Class Teacher missed marking attendance:
```
⚠️ Attendance not marked for Wednesday, 25 March 2026 (2 days ago)

[Mark 25 March Attendance]
Note: Marking attendance for previous day requires Academic Coordinator approval.
Reason for delay: [________________________________]
[Submit for Approval → Academic Coordinator]
```

Within 24 hours: no approval needed.
24–48 hours: Accountant-level override (configurable).
Beyond 48 hours: Academic Coordinator approval required.

---

## 8. Offline Mode

When school WiFi is unavailable:
```
⚠️ You are offline. Attendance will be saved locally and synced when connected.
[Mark Attendance Offline]
```
Uses browser IndexedDB to store attendance locally. On reconnect, auto-syncs to server. Conflict detection: if another teacher marked the same class online, show merge prompt.

---

## 9. Holiday / Sunday Lock

If the day is a holiday (from A-11 Holiday Calendar):
```
⛔ Today (25 Dec 2026) is marked as HOLIDAY: Christmas Day.
Attendance cannot be marked on holidays.

If this is actually a working day (school has compensatory classes),
contact the Academic Coordinator to remove the holiday marking in A-11.
```

---

## 10. CBSE Register View

The attendance grid has a [CBSE Register] toggle which shows the legal register format:

```
ADMISSION AND WITHDRAWAL REGISTER — CBSE Format
School: [Name]  ·  Class: XI-A  ·  Academic Year: 2026–27
Class Teacher: Ms. Anita Reddy

Roll  Name           Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec  Jan  Feb  Mar  Total  %
01    Anjali Das      22   19   20   22   21   20   22   18   20   22   20   12   218   94.4
02    Arjun Sharma    20   18   19   21   20   18   21   17   19   20   18   10   201   87.0
...
```

---

## 11. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/daily/{class_id}/?date={date}` | Attendance for class + date |
| 2 | `POST` | `/api/v1/school/{id}/attendance/daily/{class_id}/` | Submit attendance (initial mark) |
| 3 | `PATCH` | `/api/v1/school/{id}/attendance/daily/{class_id}/{date}/` | Update late arrival / individual correction |
| 4 | `GET` | `/api/v1/school/{id}/attendance/daily/{class_id}/summary/?month={m}&year={y}` | Monthly summary for class |
| 5 | `POST` | `/api/v1/school/{id}/attendance/daily/{class_id}/offline-sync/` | Sync offline attendance batch |
| 6 | `GET` | `/api/v1/school/{id}/attendance/daily/{class_id}/cbse-register/?year={y}` | CBSE format register |
| 7 | `GET` | `/api/v1/school/{id}/attendance/daily/{class_id}/export/?month={m}&year={y}` | Export class attendance sheet |

---

## 12. Business Rules

- Attendance can only be marked for enrolled, active students (C-05 status = Active)
- Attendance for a given date cannot be marked on Sundays or on days marked as holidays in A-11; this is a hard block, not a warning
- Once submitted, attendance is locked for that date; any change requires E-03 Correction Register (with reason + approver); this ensures audit integrity
- A student on approved leave (E-04) is shown in the grid with a 🏖 icon; the Class Teacher still marks Present/Absent (leave doesn't auto-mark present — actual presence is what matters); leave affects condonation eligibility in E-11 exam eligibility
- If a Class Teacher has not submitted attendance by 10:30 AM, Academic Coordinator gets an automated alert
- Each present/absent/late mark is a separate immutable record with timestamp and teacher ID; the Class Teacher's identity is logged (audit trail for any disputes)
- Working day count for CBSE 220-day compliance is incremented only when at least one class in the school has attendance marked for that day

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
