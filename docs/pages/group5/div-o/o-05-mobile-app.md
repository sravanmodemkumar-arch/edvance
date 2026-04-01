# O-05 — Mobile App (Student)

> **URL:** `/coaching/student-portal/app/` (app download + info page)
> **File:** `o-05-mobile-app.md`
> **Priority:** P2
> **Roles:** Student (self) · IT Coordinator (K3) · Branch Manager (K6)

---

## 1. App Overview

```
TCC STUDENT APP — EduForge Mobile
Version 4.2.1 (Android 8+, iOS 14+) | As of 31 March 2026

  DOWNLOADS:
    Google Play Store:   3,840 downloads (4.4★ — 286 ratings)
    Apple App Store:      620 downloads (4.3★ —  84 ratings)
    Active users (30-day): 1,248 / 1,840 students (67.8%) ✅
    Daily active users:      684

  APP FEATURES:
    Feature                          │ Available │ Usage (monthly avg)
    ─────────────────────────────────┼───────────┼────────────────────
    Dashboard (scores, attendance)   │ ✅        │ 1,248 users/mo
    Study material (PDF viewer)      │ ✅        │   842 users/mo
    Doubt submission                 │ ✅        │   480 uses/mo
    Mock test (full length, in-app)  │ ✅        │   640 per test
    Mock result + analysis           │ ✅        │   856 users/mo
    Schedule / timetable             │ ✅        │   984 users/mo
    Notifications                    │ ✅        │ Always-on for enrolled
    Fee status + receipts            │ ✅        │   240 users/mo
    Certificate download             │ ✅        │    84 uses/mo
    Digital ID card                  │ ✅        │   180 uses/mo
    Live online class (streaming)    │ ✅        │   196 online students
    Offline download (study material)│ ✅        │   420 downloads/mo
```

---

## 2. App Screen: Home & Test Experience

```
APP HOME SCREEN — Akhil Kumar (TCC-2401)
[TCC Logo] My Dashboard         [🔔 2]  [👤]

  ┌────────────────────────────────────┐
  │  ATTENDANCE   LAST SCORE   RANK    │
  │   95.4% ✅    186/200     #1 ✅   │
  └────────────────────────────────────┘

  UPCOMING:
    📝 Mock #26 — Apr 5, 2026 (5 days)   [Register]
    📅 Quant — DI Practice (Tomorrow 9AM)  [View]

  QUICK ACCESS:
  [📚 Study Material]   [❓ Submit Doubt]
  [📊 My Results]       [💳 Fee Status]

────────────────────────────────────────

APP MOCK TEST SCREEN:
  SSC CGL Mock Test #26
  Time remaining: 02:14:36  |  Q: 84/100

  SECTION: General Awareness
    84. Headquarters of International Solar Alliance is in:
        (A) New Delhi    (●) Gurugram, Haryana
        (C) Mumbai       (D) Chennai

  [Previous]    [Mark for review ★]    [Next]

  SECTION TABS: Quant (25) | English (25) | Reasoning (25) | GA (25/25)

  [Pause & Save]    [Submit Test ▶]
```

---

## 3. App Performance & Issues

```
APP PERFORMANCE METRICS — March 2026

  TECHNICAL:
    App crash rate:       0.4% (sessions) ✅ (target < 1%)
    Avg load time:        1.8 seconds ✅ (target < 3s)
    Offline availability: Study material + past results available offline ✅
    Test sync (offline):  Answers sync when connectivity resumes ✅

  KNOWN ISSUES (open bugs):
    BUG-284: PDF viewer does not scroll smoothly on iOS 15.x (rare)
    BUG-291: Notification sound plays twice on Android 14 (minor)
    BUG-298: Mock test timer pauses incorrectly after phone lock (medium) ⚠️

  USER FEEDBACK (App Store reviews — recent):
    ★★★★★ "Best coaching app — mock test quality is excellent" (Ravi T.)
    ★★★★  "Good but timer bug during mock is annoying" (K. Priya)
    ★★★   "PDF material downloads slowly on 4G" (Anand R.)

  APP UPDATES (recent):
    v4.2.1 (Mar 5):  Timer bug fix (partial — BUG-298 open still)
    v4.2.0 (Feb 10): Offline study material download feature
    v4.1.0 (Jan 8):  Live class streaming stability improvements

  NEXT RELEASE (v4.3.0 — targeted Apr 25):
    Full fix for BUG-298 (timer issue)
    AI doubt suggestion (show similar past doubts before submitting)
    Dark mode support
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-portal/app/info/` | App version and feature info |
| 2 | `GET` | `/api/v1/coaching/{id}/student-portal/app/metrics/` | App usage and performance metrics |
| 3 | `GET` | `/api/v1/coaching/{id}/student-portal/app/bugs/` | Known issues log |
| 4 | `POST` | `/api/v1/coaching/{id}/student-portal/app/feedback/` | Submit app feedback |
| 5 | `GET` | `/api/v1/coaching/{id}/student-portal/app/updates/` | App release history |

---

## 5. Business Rules

- The mobile app is the primary interface for 67.8% of students (1,248 of 1,840); investing in app quality is not optional — the app experience IS the student experience for the majority of users; a crash-prone or slow app reduces student engagement with study material and doubt submission, directly affecting academic outcomes; TCC's SLA with EduForge (the SaaS provider) must include mobile app performance metrics (crash rate < 1%, load time < 3 seconds, uptime 99.5%); a degraded app during a mock test is a critical service failure
- The mock test timer bug (BUG-298 — timer pauses incorrectly after phone lock) is a medium-severity issue because it can give some students more time than others if they lock their phones mid-test; in a high-stakes competitive environment where 1 mark can change a rank by 50 positions, a timer inaccuracy that benefits some students is a fairness issue; the Branch Manager must decide whether to continue conducting app-based mocks until the fix is released (v4.3.0, Apr 25) or revert to hall-based mocks with physical question papers for Mock #26; the decision should consider the frequency of the bug and its actual impact on results
- The offline study material feature (v4.2.0) is crucial for students in areas with poor internet connectivity; downloading a chapter to study on the metro or during a power cut addresses a real need for Indian students; the offline content must be governed by DRM (Digital Rights Management) to prevent students from sharing downloaded PDFs outside TCC; a downloaded PDF that can be freely shared would undermine TCC's study material exclusivity and the value of TCC enrollment; EduForge's DRM implementation should be reviewed by TCC's IT coordinator to confirm it prevents sharing
- App Store reviews are monitored weekly by the IT coordinator and marketing team; a negative review about a real issue (timer bug, slow download) is acknowledged with a public reply: "We are aware of this issue and the fix is included in v4.3.0 (April 25). Thank you for the feedback"; a negative review about a misunderstanding is addressed with a polite factual correction; TCC does not respond combatively to negative reviews even if the reviewer is wrong; the response is always professional and solution-oriented; reviews are also a source of feature requests that feed into the EduForge product roadmap
- The "AI doubt suggestion" feature (planned for v4.3.0) will show students similar previously-answered doubts before they submit a new one; this reduces duplicate doubts (where 10 students ask the same question about a Caselet DI formula), freeing faculty time for genuinely new questions; the AI matching algorithm works within the EduForge platform and uses TCC's doubt history (student name and context is stripped for matching — it matches question content, not student identity); this privacy-preserving design ensures that students see "a similar doubt was asked before" without seeing who asked it, protecting the earlier student's privacy

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division O*
