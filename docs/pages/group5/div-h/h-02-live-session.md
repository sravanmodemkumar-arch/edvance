# H-02 — Live Session Management

> **URL:** `/coaching/online/live/`
> **File:** `h-02-live-session.md`
> **Priority:** P1
> **Roles:** Online Coordinator (K4) · Faculty (K2) · Branch Manager (K6)

---

## 1. Live Session Schedule & Control

```
LIVE SESSION MANAGEMENT
30 March 2026  |  Upcoming: 7:00 PM

  SCHEDULED SESSIONS (Today Evening):

  Session               │ Batch            │ Faculty      │ Zoom ID        │ Start  │ Status
  ──────────────────────┼──────────────────┼──────────────┼────────────────┼────────┼──────────────
  Quant — Caselet DI    │ SSC CGL Live     │ Suresh K.    │ 842-111-2345   │ 7:00 PM│ ⏳ Scheduled
  Reasoning — Puzzles   │ Banking Online   │ Mohan R.     │ 842-111-3456   │ 7:00 PM│ ⏳ Scheduled
  Reasoning — Seating   │ SSC CGL Live     │ Mohan R.     │ 842-111-4567   │ 8:00 PM│ ⏳ Scheduled
  Quant — Percentage    │ Banking Online   │ Suresh K.    │ 842-111-5678   │ 8:00 PM│ ⏳ Scheduled
  GK/CA — March 2026    │ RRB Online       │ Ravi S.      │ 842-111-6789   │ 9:00 PM│ ⏳ Scheduled

  PRE-SESSION CHECKLIST (7:00 PM sessions):
    [✓] Zoom links sent to enrolled students (WhatsApp + push, 6:30 PM) ✅
    [✓] Faculty confirmed availability (Mr. Suresh K. — confirmed 4 PM) ✅
    [✓] Recording auto-start configured ✅
    [✓] Co-host (Online Coordinator) ready to join ✅
    [ ] Waiting room approved students list loaded — due 6:55 PM
```

---

## 2. Session Launch & Monitor

```
SESSION LAUNCH — Quant: Caselet DI
SSC CGL Live Online | 7:00 PM – 8:00 PM | Faculty: Mr. Suresh Kumar

  ZOOM SETTINGS (pre-configured):
    Recording:    Cloud auto-record ✅ (mandatory)
    Waiting room: Enabled — coordinator admits students
    Chat:         All participants enabled
    Q&A panel:    Enabled (questions queue visible to faculty)
    Screen share: Host only
    Background:   TCC branded background loaded ✅

  LIVE STATUS (if session in progress):
    ┌────────────────────────────────────────────────────────────────────────┐
    │  🔴 LIVE — 00:24:18 elapsed | 00:35:42 remaining                      │
    │  Participants: 146 / 186  (78.5%)  |  Recording: ✅                   │
    │  Q&A raised: 8  |  Answered: 6  |  Pending: 2                         │
    │  Late joiners (> 5 min): 12                                            │
    │                                                                         │
    │  [Send message to all] [Admit from waiting room] [Mute all] [End]     │
    └────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Substitute Faculty Management

```
SUBSTITUTE FACULTY — Emergency (Unplanned Absence)

  SCENARIO: Mr. Mohan Rao (Reasoning) is ill — cannot take 7:00 PM Banking Online session

  SUBSTITUTE OPTIONS:
    Faculty         │ Subject Match │ Availability (7PM) │ Notified │ Response
    ────────────────┼───────────────┼────────────────────┼──────────┼──────────────
    Ms. Kavita M.   │ Reasoning ✅  │ Available          │ 5:12 PM  │ ✅ Confirmed
    Mr. Suresh K.   │ Quant only ❌  │ Teaching at 7 PM   │ —        │ —
    Mr. Ravi S.     │ GK/Reasoning  │ Available          │ 5:14 PM  │ Pending

  SUBSTITUTE CONFIRMED: Ms. Kavita Menon
  Student notification: "Tonight's Banking Online Reasoning class will be taken
  by Ms. Kavita Menon instead of Mr. Mohan Rao. Zoom link unchanged." — Sent 5:22 PM ✅

  Session recorded and marked as SUBSTITUTE in system (affects faculty load calc)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/online/live/schedule/?date=2026-03-30` | Today's live session schedule |
| 2 | `POST` | `/api/v1/coaching/{id}/online/live/` | Create a new live session |
| 3 | `GET` | `/api/v1/coaching/{id}/online/live/{sid}/status/` | Real-time session status |
| 4 | `POST` | `/api/v1/coaching/{id}/online/live/{sid}/substitute/` | Assign substitute faculty |
| 5 | `POST` | `/api/v1/coaching/{id}/online/live/{sid}/end/` | End session and trigger recording upload |
| 6 | `GET` | `/api/v1/coaching/{id}/online/live/checklist/?session={sid}` | Pre-session checklist status |

---

## 5. Business Rules

- Every live session must be cloud-recorded automatically; faculty cannot disable recording; the recording is the backup for students who miss the live session and the evidence for complaint resolution if a student claims a session didn't happen; a session without a recording is an incomplete delivery record; the Online Coordinator monitors recording status post-session and alerts the Academic Director if a session ended without a recording (technical failure) — an emergency re-recording or makeup session is arranged
- Substitute faculty for online sessions must be notified at least 2 hours before the session; a substitute confirmed less than 2 hours before risks an unprepared or substandard session; if no qualified substitute is available within 2 hours, the session is rescheduled and students are notified; a rescheduled live session must be offered within 48 hours; the original recorded session from a previous week on the same topic can be shared as a temporary measure, but this does not count as delivery — only a live or makeup session counts
- The waiting room is mandatory for all live sessions; students enter the waiting room and the coordinator (co-host) admits them; students who are not enrolled in the batch cannot be admitted even if they have the Zoom link (their name is not on the admitted list); this access control prevents students from sharing Zoom links to outsiders (common in coaching batch groups); the coordinator's admitted list is synced with the EduForge enrollment database
- Live session Q&A is monitored by the Online Coordinator as co-host; questions that faculty cannot answer during class are logged and assigned to the doubt management system (C-07) automatically; the faculty is not expected to answer all questions live — the coordinator routes complex doubts to the post-session queue; this prevents sessions from being derailed by one student's extensive doubting while others wait
- Faculty who conduct live sessions from home (WFH arrangement) must use TCC's branded virtual background (provided as a file) to maintain professional appearance; using a messy home background or an informal personal setting during live sessions with 200+ students represents the TCC brand; the Online Coordinator can see all faculty video feeds during the session and may message the faculty privately if background or audio quality is substandard

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division H*
