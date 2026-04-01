# H-04 — Online Attendance & Engagement

> **URL:** `/coaching/online/attendance/`
> **File:** `h-04-online-attendance.md`
> **Priority:** P1
> **Roles:** Online Coordinator (K4) · Batch Coordinator (K4) · Academic Director (K5)

---

## 1. Online Attendance Overview

```
ONLINE ATTENDANCE — SSC CGL Live Online
March 2026 (26 sessions)  |  186 students enrolled

  LIVE SESSION ATTENDANCE:
    Avg live attendance:    76.3%  (142/186 per session avg)
    Target:                 75%  ✅ Met
    Best session:           87.1% (Mar 22 — Mensuration 3D — high-demand topic)
    Worst session:          62.4% (Mar 26 — GK/CA — less popular; now tracked)

  RECORDING CONSUMPTION (as proxy for missed-session catch-up):
    Students who missed live but watched recording:  28.4% of absentees ✅
    Students who missed live AND didn't watch:       71.6%  ⚠️ (= true absence)

  EFFECTIVE ATTENDANCE (live + recording):
    Effective attendance rate:  82.6%  (live 76.3% + recording catch-up 6.3%)
    Below 60% effective:         14 students  → counsellor flagged

  MONTHLY TREND:
    Jan: 72.4% → Feb: 74.8% → Mar: 76.3% ↑ ✅ Improving
```

---

## 2. Student-Level Attendance

```
ONLINE STUDENT ATTENDANCE — SSC CGL Live Online (March 2026)

  Student          │ Roll No    │ Live%  │ Recording│ Effective │ Last Login  │ Status
  ─────────────────┼────────────┼────────┼──────────┼───────────┼─────────────┼──────────────
  Akhil Kumar      │ TCC-2401   │  95.4% │   8 vids │   98.1%   │ 30 Mar      │ ✅ Active
  Priya Reddy      │ TCC-2402   │  88.2% │  12 vids │   92.4%   │ 29 Mar      │ ✅ Active
  Ravi Singh       │ TCC-2403   │  82.1% │  18 vids │   88.6%   │ 28 Mar      │ ✅ Active
  Divya Sharma     │ TCC-2404   │  90.8% │   6 vids │   93.2%   │ 30 Mar      │ ✅ Active
  Mohammed R.      │ TCC-2406   │  48.2% │   4 vids │   52.8%   │ 24 Mar      │ 🔴 At-Risk
  Sravya Rao       │ TCC-2418   │  58.4% │   6 vids │   62.4%   │ 22 Mar      │ 🟡 Watch
  Kiran Naidu      │ TCC-2419   │  32.1% │   2 vids │   34.8%   │ 19 Mar      │ 🔴 At-Risk
  ...  (179 more)

  AT-RISK SUMMARY:
    Live < 60%:             24 students
    Effective < 60%:        14 students
    Not logged in > 7 days:  8 students  → Coordinator WhatsApp follow-up due
```

---

## 3. Engagement Score

```
ENGAGEMENT SCORE — Top & Bottom Students (March 2026)

  COMPONENTS OF ENGAGEMENT SCORE (100 pts):
    Live attendance:       40 pts  (76.3% avg → 30.5/40)
    Recording watch %:     20 pts  (68.4% avg watch → 13.7/20)
    Test participation:    20 pts  (based on test completion rate)
    Doubt submission:      10 pts  (1 pt per doubt raised, max 10)
    Study material access: 10 pts  (reading/download activity)

  BATCH AVG ENGAGEMENT SCORE: 64.2 / 100

  TOP ENGAGERS:
    1. Akhil Kumar:   92/100 (live 97%, all recordings, 8 tests, 6 doubts)
    2. Divya Sharma:  88/100 (live 91%, 14 recordings, 8 tests, 4 doubts)
    3. Priya Reddy:   84/100 (live 88%, 18 recordings, 7 tests, 2 doubts)

  LOW ENGAGERS (< 40/100):
    1. Kiran Naidu:   22/100 (live 32%, 2 recordings, 3 tests, 0 doubts)
    2. Mohammed R.:   31/100 (live 48%, 4 recordings, 4 tests, 0 doubts)
    → Online counsellor intervention scheduled Apr 1

  [Export Engagement Report]   [Send Motivation Message to Low Engagers]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/online/attendance/?batch={bid}&month=2026-03` | Batch-level online attendance |
| 2 | `GET` | `/api/v1/coaching/{id}/online/attendance/student/{sid}/?month=2026-03` | Student online attendance detail |
| 3 | `GET` | `/api/v1/coaching/{id}/online/engagement/?batch={bid}&month=2026-03` | Engagement scores for batch |
| 4 | `GET` | `/api/v1/coaching/{id}/online/attendance/at-risk/?batch={bid}` | At-risk online students |
| 5 | `POST` | `/api/v1/coaching/{id}/online/engagement/alert/` | Send alert to low-engagement students |

---

## 5. Business Rules

- Online attendance is a composite measure of live session participation and recording consumption; a student who misses a live session but watches the full recording within 48 hours receives "effective attendance" credit; this reflects the real purpose of attendance tracking — ensuring students engage with the content; online-only students who rely entirely on recordings (never attending live) have lower engagement scores and weaker performance on tests (live discussions improve retention), which is reflected in the engagement score component weighting
- The "not logged in for 7 days" alert is the primary retention tool for online students; online dropout is a "silent" dropout — the student simply stops logging in without formally withdrawing; the Online Coordinator's WhatsApp follow-up script is: "Hi [Name], we noticed you haven't joined classes for a few days. Is everything okay? The March 2026 GK sessions and Caselet DI recordings are waiting for you. Let me know if you need any help — [Coordinator name], TCC Online Team"; this personal message has a 42% re-engagement rate (vs 8% for automated SMS)
- Engagement scores are shared with the batch coordinator for online-offline hybrid students; for purely online students, the Online Coordinator is the primary point of contact; engagement score below 40 triggers a call, not just a WhatsApp; a student who doesn't respond to 3 WhatsApp messages over 7 days is called; if the call is not answered in 3 attempts over 2 days, the student is marked as "disengaged — pending contact" and escalated to the Branch Manager for a decision on continuing the enrollment
- Engagement score data should not be shared with students in aggregate form (e.g., "your engagement score is 22/100") as it may feel punitive; instead, coordinators share specific action items ("you've missed 10 sessions this month — here are the 3 recordings most relevant to April's exam") and frame the conversation around the student's outcome, not TCC's metric; the engagement score is an internal tool for coordinator use, not a student-facing scorecard
- Effective attendance percentage (82.6% for the batch) is the KPI reported to the Academic Director; the live-only attendance (76.3%) would understate actual engagement by 6 percentage points; the Academic Director reports effective attendance in the branch MIS to the Director; franchise branches with online components must also report effective attendance; a franchise reporting only live attendance is misrepresenting engagement and will be corrected in the quarterly franchise review

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division H*
