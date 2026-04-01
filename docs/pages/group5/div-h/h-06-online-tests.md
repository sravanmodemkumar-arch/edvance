# H-06 — Online Test Delivery

> **URL:** `/coaching/online/tests/`
> **File:** `h-06-online-tests.md`
> **Priority:** P2
> **Roles:** Online Coordinator (K4) · Test Series Coordinator (K4) · Faculty (K2)

---

## 1. Online Test Interface Overview

```
ONLINE TEST DELIVERY — Student Experience Preview
SSC CGL Full Mock #25 | Apr 5, 2026 | 9:00 AM – 11:00 AM

  STUDENT VIEW (preview mode):
  ┌───────────────────────────────────────────────────────────────────────────┐
  │  SSC CGL FULL MOCK #25            Time Remaining: 01:22:48               │
  │  ─────────────────────────────────────────────────────────────────────── │
  │  SECTION: QUANTITATIVE APTITUDE  (1–25)    Score: 16 | Attempted: 18    │
  │                                                                           │
  │  Q.14  [Hard]  Mensuration — Frustum                                     │
  │  A frustum has slant height 13 cm, smaller radius 5 cm, larger...       │
  │                                                                           │
  │  (A) 390π cm²   ●  ← selected                                            │
  │  (B) 1,170π cm²                                                           │
  │  (C) 520π cm²                                                             │
  │  (D) 845π cm²                                                             │
  │                                                                           │
  │  [Mark for Review]  [Clear Response]  [Save & Next →]                   │
  │  ─────────────────────────────────────────────────────────────────────── │
  │  Palette: Sections [QA] [EN] [RE] [GK]  Questions: [1-25 grid view]     │
  └───────────────────────────────────────────────────────────────────────────┘

  GRID LEGEND:
    ✅ Answered  ✏️ Answered + marked for review  ⬜ Not visited
    🔲 Visited, not answered  🔴 Marked for review, not answered
```

---

## 2. Anti-Cheat Settings

```
ANTI-CHEAT CONFIGURATION — Online Test Delivery

  ACTIVE PROTECTIONS FOR SSC CGL FULL MOCK #25:
    [✓] Tab-switch detection (3 strikes = auto-submit)
    [✓] Screen share detection (AI-based — flags for review)
    [✓] Copy-paste blocked (question text, options)
    [✓] Right-click disabled on question page
    [✓] Back-button blocked during test (browser lock)
    [✓] Duplicate IP detection (alert if 2 students on same IP)
    [✓] Dynamic watermark (student name + roll no visible on screen)
    [✓] Time-per-question logging (unusually fast answers flagged)
    [ ] AI proctoring (live webcam) — Not enabled for this test (optional add-on)
    [ ] Lockdown browser (full-screen only) — Not required for this level

  NOTES:
    For competitive franchise tests or high-stakes selection tests: enable AI proctoring
    Lockdown browser adds friction for home-based students — avoided for standard mocks
    All flags are reviewed post-test (E-03) before any action is taken
```

---

## 3. Test Delivery Modes

```
TEST MODES AVAILABLE

  Mode                │ Use Case                     │ Proctoring   │ Result
  ────────────────────┼──────────────────────────────┼──────────────┼──────────────────
  Live Test           │ Scheduled batch exam          │ Tab-switch   │ After window closes
  Practice Test       │ Self-paced anytime            │ None         │ Immediate
  Timed Practice      │ Simulates exam conditions     │ Timer only   │ After submit
  Sectional Test      │ One subject only              │ Tab-switch   │ After window
  Previous Year Paper │ PYQ practice (unlocked for all│ None         │ Immediate
  Instant Quiz        │ 10-Q quick check (post-class) │ None         │ Immediate

  ACTIVE MODES FOR SSC CGL LIVE ONLINE:
    ✅ Live Test (Full Mocks and Sectionals on schedule)
    ✅ Practice Test (unlimited, anytime)
    ✅ Timed Practice (available 24/7)
    ✅ Previous Year Papers (SSC CGL 2019–2025)
    ✅ Instant Quiz (after each live session, 10 Qs on session topic)
    ✅ Sectional Test (subject-specific, any time)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/online/tests/{tid}/interface/` | Test UI configuration |
| 2 | `GET` | `/api/v1/coaching/{id}/online/tests/{tid}/question/{qnum}/` | Fetch question (with timer sync) |
| 3 | `POST` | `/api/v1/coaching/{id}/online/tests/{tid}/response/` | Save student response |
| 4 | `POST` | `/api/v1/coaching/{id}/online/tests/{tid}/submit/` | Submit test |
| 5 | `GET` | `/api/v1/coaching/{id}/online/tests/modes/?batch={bid}` | Available test modes for batch |
| 6 | `POST` | `/api/v1/coaching/{id}/online/tests/{tid}/cheat-event/` | Log a cheat detection event |

---

## 5. Business Rules

- Test questions are fetched one-by-one via API with each response submitted immediately; the student's work is never lost even if their browser crashes mid-test; when the student reopens the test within the window, they are placed at the last unanswered question with all previous responses intact; the server-side response log is the authoritative record, not the student's browser state; this server-first architecture eliminates "my browser crashed and I lost everything" complaints
- Copy-paste blocking and right-click disabling are JavaScript-level protections that prevent casual sharing of question text; determined students can bypass these with developer tools; TCC's position is that deterrence (not prevention) is the goal for home-based practice mocks; the real protection against question leaking is question bank rotation (no question appears in more than 2 tests per year) and post-test solution release (after release, the question is already public); AI proctoring is reserved for high-stakes scenarios
- The "Instant Quiz" (10 questions immediately after a live session) has a pedagogical basis — testing retention within 20 minutes of learning improves recall significantly (spaced repetition effect); the Online Coordinator triggers the Instant Quiz from the session management dashboard (H-02) at session end; faculty prepare 10 quiz questions as part of their session prep and upload them to the question bank tagged with the session; the quiz is unproctored and result is immediate — it is a learning tool, not an assessment
- Previous year papers (PYQ, 2019–2025 SSC CGL) are made available as practice tests at the start of the course; PYQ papers have officially-released answer keys; TCC's question bank stores them with verified keys; PYQ practice is the single highest-value preparation activity for SSC exams (questions are repeated in similar form); the Online Coordinator must ensure PYQs are added for each new year's paper within 30 days of SSC's official answer key release
- Test response data is stored with millisecond timestamps; a student who answers Q.14 in 1.2 seconds (while the question has 86 words) is flagged — reading + processing + clicking takes at minimum 25 seconds; these fast-answer flags are reviewed alongside other cheat signals in the post-test review (E-08); a cluster of fast answers (Q.11, Q.12, Q.13, Q.14 all answered in < 3 sec) is a stronger signal than a single instance; the coordinator documents the review and the decision before any action

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division H*
