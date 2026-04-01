# E-03 — Live Test Monitor

> **URL:** `/coaching/tests/live/`
> **File:** `e-03-live-test-monitor.md`
> **Priority:** P1
> **Roles:** Test Series Coordinator (K4) · Invigilator (K2) · Branch Manager (K6)

---

## 1. Live Test Control Panel

```
LIVE TEST MONITOR — SSC CGL Full Mock #25
5 April 2026 | 09:00 AM – 11:00 AM  |  200 marks / 60 min

  STATUS: 🔴 LIVE — 00:42:18 elapsed | 00:17:42 remaining

  PARTICIPATION:
    Total enrolled:      1,240  (online + offline)
    Started test:        1,186  (95.6%) ✅
    Currently active:    1,142  (91.9%)
    Submitted early:        44   (3.5%)
    Not started:            54   (4.4%) ← auto-absent after window closes

  SECTION PROGRESS (avg, active students):
    Section 1 — Quant (25 Qs):       Completed 100% | Avg score: 16.2/25
    Section 2 — English (25 Qs):     Completed 100% | Avg score: 17.4/25
    Section 3 — Reasoning (25 Qs):   Completed 88%  | In progress
    Section 4 — GK (25 Qs):          Completed 0%   | Not yet unlocked

  LIVE ALERTS:
    🟡 Tab-switch warning issued: 38 students (1st warning)
    🔴 Tab-switch flag: 12 students (2nd warning — invigilator notified)
    ⚠️ Auto-submit triggered: 3 students (3rd tab-switch — submitted forcibly)
    🔴 Duplicate IP detected: TCC-2801 and TCC-2802 on same IP (Hall B) — check
```

---

## 2. Invigilator View

```
INVIGILATOR PANEL — Hall A (Offline) | Full Mock #25
Invigilator: Mr. Ganesh Reddy

  OFFLINE STUDENTS PRESENT:  186 / 200  (93%)
  PAPER DISTRIBUTED:          (●) Variant A: 48 | Variant B: 46 | Variant C: 46 | Variant D: 46
  PHYSICAL SUBMISSION COUNT:  12 students submitted so far (early exit permitted)

  INCIDENTS:
    09:14 — Ravi Singh (TCC-2403): asked for extra rough sheet (given ✅)
    09:28 — Mohammed R. (TCC-2406): left hall (stated stomach ache, signed exit form ✅)
    09:42 — Anitha K. (TCC-2408): tab-switch flag (was on phone — phone collected)

  CHEAT DETECTION (online students — AI-assisted):
    Unusual time pattern (Q answered in < 2 sec):  8 instances flagged for review
    Copy-paste attempted:                           0
    Screen share detected:                          2 (Priya R., Kiran N.) — flagged

  [Add Incident]   [Message Online Proctor]   [Emergency End Test]
```

---

## 3. Test Window Management

```
TEST WINDOW CONTROLS — SSC CGL Full Mock #25

  Scheduled window:  9:00 AM – 11:00 AM (10:00 AM → time remaining countdown)
  Current time:      9:42:18 AM

  WINDOW EXTENSIONS (per-student):
    Reason required:  Power cut / ISP issue / device failure (with proof)
    Max extension:    15 minutes (non-extendable beyond 11:30 AM hard cutoff)
    Extensions granted: 4 students (today)
      TCC-2912: +12 min (ISP outage — proof: Jio down in Warangal 9:00–9:12) ✅
      TCC-2788: + 8 min (power cut — self-declaration, no proof — still granted) ⚠️

  BULK ACTIONS:
    [Add 5 min to ALL online students]     → Requires Academic Director OTP
    [Pause test for all]                   → Emergency only (logs reason + timestamp)
    [End test 15 min early]                → Requires Academic Director approval + reason

  HARD CUTOFF:  11:00 AM — all active sessions auto-submit at exactly 11:00:00
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/live/` | Live test stats (refreshes every 30 sec) |
| 2 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/live/alerts/` | Real-time alerts (tab-switch, IP flags) |
| 3 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/live/extend/` | Grant time extension to a student |
| 4 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/live/incident/` | Log an invigilator incident |
| 5 | `POST` | `/api/v1/coaching/{id}/tests/{tid}/live/end/` | Force-end test (emergency, requires auth) |
| 6 | `GET` | `/api/v1/coaching/{id}/tests/{tid}/live/cheat-flags/` | Cheat detection flags for review |

---

## 5. Business Rules

- The live monitor auto-refreshes every 30 seconds during the test window; coordinators must keep the monitor open throughout the test; alerts (tab-switch, duplicate IP, screen-share detection) appear in real time; a coordinator who is not monitoring during the live test and misses a cheating incident has no record of the event; the platform logs coordinator login/activity during the test window — "coordinator was online" is part of the integrity certification for each test
- Time extensions granted to individual students must be logged with a reason; extensions without documentation ("I just gave them extra time") are invalid; the extension log is an evidence record if a student later claims unfair treatment; extensions beyond 15 minutes (e.g., a student whose device crashed and lost 25 minutes) require Academic Director approval and are treated as a makeup test, not an extension; this prevents coordinators from arbitrarily giving time to preferred students
- Auto-submit at the hard cutoff (11:00:00 AM) is absolute and cannot be overridden by any coordinator or director after the fact; the hard cutoff ensures that students who were in a different time zone or started the test 5 minutes late cannot see the paper after other students' results have been processed; cheating by "starting late and having extra time while others discuss answers" is eliminated by the hard cutoff
- The "3 tab-switches = auto-submit" rule is disclosed to students in the test instructions page before the test begins; students must acknowledge this rule before the test starts; if a student's test is auto-submitted due to tab-switches, they cannot request a retest citing "I didn't know"; the acknowledged rule forms part of the test integrity agreement; coordinators can review the tab-switch log to confirm the auto-submit was correct before rejecting any appeal
- Cheat detection flags (unusual answer timing, screen share, copy-paste) are reviewed post-test, not during the test; no student is disqualified during a live test based solely on AI flags; the coordinator reviews all flags after the test and presents confirmed cases to the Academic Director for decision; a first confirmed offence results in a warning with the test score voided; a second confirmed offence results in batch suspension pending a hearing; this graduated response avoids false positives causing student distress during exam preparation

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division E*
