# D-07 — Online Batch Management

> **URL:** `/coaching/batches/online/`
> **File:** `d-07-online-batch.md`
> **Priority:** P2
> **Roles:** Batch Coordinator (K4) · Branch Manager (K6) · Online Faculty (K2)

---

## 1. Online Batch Overview

```
ONLINE BATCH MANAGEMENT — SSC CGL Live Online
As of 30 March 2026  |  Coordinator: Ms. Priya Nair

  Batch Type:      Live Online (Zoom + EduForge LMS)
  Enrolled:        186 students  (across India: 60% Telangana, 40% others)
  Batch time:      Mon–Sat  7:00 PM – 9:00 PM IST
  Platform:        Zoom (class delivery) + EduForge (material, tests, attendance)

  LIVE SESSION STATUS (today, 30 Mar 7 PM):
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │  🔴 LIVE — SSC CGL Quant (7:00–8:00 PM)                                   │
  │  Faculty: Mr. Suresh Kumar | Zoom ID: 842-xxx-xxxx                         │
  │  Participants: 142/186 (76.3%) | Recording: ✅ Active (auto)               │
  │  Chat messages: 38 | Q&A raised: 12 | Answered: 9 | Pending: 3            │
  │                                                                             │
  │  [Join as Observer]   [Send Alert to Absentees]   [End Session Early]      │
  └─────────────────────────────────────────────────────────────────────────────┘

  RECORDING LIBRARY (last 7 sessions):
    30 Mar — Quant: Mensuration 3D        [Processing...] (uploaded in ~20 min)
    29 Mar — English: Cloze Test          [✅ Available] 168 views
    28 Mar — Reasoning: Blood Relations   [✅ Available] 154 views
    27 Mar — GK: Economy Current Affairs  [✅ Available] 132 views
    26 Mar — Quant: DI Caselets          [✅ Available] 178 views
    25 Mar — English: Error Spotting      [✅ Available] 144 views
    24 Mar — Reasoning: Coding-Decoding   [✅ Available] 126 views
```

---

## 2. Online Attendance Tracking

```
ONLINE ATTENDANCE — SSC CGL Live Online
30 March 2026, 7:00–8:00 PM  (Quant session)

  Attendance source: Zoom participant log (auto-import at session end)

  Join time analysis:
    Joined before 7:05:   128 (68.8%) — On time
    Joined 7:05–7:20:      14 ( 7.5%) — Late
    Joined after 7:20:       0 ( 0.0%)
    Not joined:             44 (23.7%) — Absent

  MINIMUM DURATION RULE: Students who joined but left before 30 min (of 60 min):
    Flagged as "Partial Attend":  6 students
    Counted as: Absent (< 30 min = no attendance credit)

  OVERALL:
    Present (full):    128
    Late:               14
    Partial (flagged):   6 → counted absent
    Absent:             44
    ATTENDANCE RATE: 76.3% (128 + 14 = 142/186 with late credit)

  [Auto-import complete ✅ | Corrections window: until 10:00 PM tonight]
```

---

## 3. Online Batch Settings

```
ONLINE BATCH SETTINGS — SSC CGL Live Online

  ZOOM INTEGRATION:
    Zoom Account:       tcc.zoom@toppers.in (Pro, 1,000 participant limit)
    Auto-record:        (●) Cloud recording — enabled for all sessions
    Recording access:   EduForge LMS only (download disabled for students)
    Waiting room:       (●) Enabled — host admits participants
    Chat:               (●) Enabled (host + participants)
    Screen share:       (●) Host only during class; ( ) All

  ATTENDANCE RULES (Online):
    Min. join time:     First 20 minutes of session
    Min. duration:      30 minutes (of 60 min session) for attendance credit
    Late threshold:     5 minutes after session start
    Auto-import:        (●) Zoom log imported at session end + 5 min

  RECORDING EXPIRY:
    Available to students: 90 days after session date
    After 90 days: Archived (coordinator can extend per session)
    Download by students: ❌ Disabled — streaming only (signed URL, 4-hr expiry)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/online/sessions/?date=2026-03-30` | Today's online session status |
| 2 | `POST` | `/api/v1/coaching/{id}/batches/{bid}/online/attendance/import/` | Import Zoom participant log for attendance |
| 3 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/online/recordings/` | Recording library for batch |
| 4 | `PATCH` | `/api/v1/coaching/{id}/batches/{bid}/online/recordings/{rid}/expiry/` | Extend recording expiry |
| 5 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/online/settings/` | Online batch configuration |
| 6 | `POST` | `/api/v1/coaching/{id}/batches/{bid}/online/alert/absentees/` | Send alert to students not yet joined |

---

## 5. Business Rules

- Online attendance is auto-imported from the Zoom participant log at session end; the minimum duration rule (30 minutes out of 60) prevents students from briefly joining to register attendance and then disconnecting; the coordinator has a correction window (2 hours after session end) to manually adjust attendance for technical issues (student's internet dropped and they reconnected) — corrections after the window require Branch Manager approval
- All Zoom sessions are cloud-recorded automatically; recordings are not optional — a session without recording violates TCC's online commitment to students who missed the live session; faculty cannot disable recording; if a faculty member has an objection to being recorded (rare, but occurs), they must raise it with the Academic Director before the batch starts — it cannot be toggled per-session
- Recording access is governed by the same signed URL mechanism as study material (C-03); students can stream but not download; recordings are available for 90 days; expired recordings are archived but can be reactivated by the coordinator for students who were enrolled during that period (e.g., a student who missed March recordings due to illness can request reactivation in April); reactivation is logged
- Online batches must maintain the same curriculum and test schedule as equivalent offline batches (SSC CGL Online must cover the same topics in the same sequence as SSC CGL Morning offline); if a live session is cancelled due to faculty unavailability or technical failure, a makeup session must be scheduled within 72 hours and all enrolled students notified; the coordinator cannot skip the session and "cover it next week" without approval
- Students in online batches who fall below 60% online attendance receive the same restrictions as offline students (reduced test access) and the same counsellor referral; "I had internet issues" is addressed through the technical exception process — the student submits proof (ISP downtime, power cut notice) and the coordinator can reclassify up to 3 sessions per month as "excused absences"; beyond 3, the rule applies regardless of reason

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division D*
