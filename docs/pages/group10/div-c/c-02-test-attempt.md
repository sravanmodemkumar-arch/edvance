# C-02 — Test Attempt Interface

> **URL:** `/student/tests/{test_id}/attempt`
> **File:** `c-02-test-attempt.md`
> **Priority:** P1
> **Roles:** Student (S2–S6)

---

## Overview

The test-taking interface — the **highest-traffic, most performance-critical page** in EduForge. During peak windows (SSC CGL Saturday mocks), 18,00,000 students are simultaneously on this page. The interface replicates the exact look and feel of real exam interfaces: NTA's interface for JEE/NEET, TCS iON for SSC/RRB, IBPS's interface for Banking. This ensures students develop muscle memory for the actual exam. The interface supports MCQ (single/multi correct), numerical answer, match-the-column, assertion-reasoning, and comprehension-based questions. Full offline resilience — responses are cached locally and synced when connectivity returns.

---

## 1. Test Interface — JEE Pattern (NTA Style)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  JEE Mains Mock #25                    Timer: 02:13:42          [Pause ⏸]  │
│  Section: Physics (Q12 of 25)          Answered: 11/75  Not visited: 38    │
│  ────────────────────────────────────────────────────────────────────────   │
│                                                                              │
│  ┌─── QUESTION PANEL ────────────────────────────────────┬── PALETTE ────┐ │
│  │                                                        │               │ │
│  │  Q.12  A block of mass 2 kg is placed on a            │  PHYSICS      │ │
│  │  frictionless inclined plane making an angle           │  ┌──┬──┬──┬──┐│ │
│  │  of 30° with the horizontal. A force F is             │  │●1│●2│●3│●4││ │
│  │  applied horizontally. Find the minimum               │  ├──┼──┼──┼──┤│ │
│  │  value of F (in N) to prevent the block from          │  │●5│●6│●7│●8││ │
│  │  sliding down.                                        │  ├──┼──┼──┼──┤│ │
│  │                                                        │  │●9│●10│●11│▶12│ │
│  │  Given: g = 10 m/s²                                   │  ├──┼──┼──┼──┤│ │
│  │                                                        │  │○13│○14│○15│○16│ │
│  │  ┌─────────────────────────────────────┐              │  ├──┼──┼──┼──┤│ │
│  │  │         /|                          │              │  │○17│○18│○19│○20│ │
│  │  │   F →  / |  mg                      │              │  ├──┼──┼──┼──┤│ │
│  │  │       /  |                          │              │  │○21│○22│○23│○24│ │
│  │  │      /30°|                          │              │  ├──┼──┼──┤  ││ │
│  │  │     /────|                          │              │  │○25│  │  │  ││ │
│  │  └─────────────────────────────────────┘              │  └──┴──┴──┴──┘│ │
│  │                                                        │               │ │
│  │  (A)  11.55 N                                         │  LEGEND:      │ │
│  │  (B)  13.46 N                                         │  ● Answered   │ │
│  │  (C)  15.00 N                                         │  ◐ Review     │ │
│  │  (D)  17.32 N                                         │  ○ Not visited│ │
│  │                                                        │  ▶ Current   │ │
│  │  Selected: (A) ●                                      │               │ │
│  │                                                        │  CHEMISTRY   │ │
│  │  [Clear Response]  [Mark for Review ◐]                │  [Go →]      │ │
│  │                                                        │               │ │
│  │                                                        │  MATHS       │ │
│  │                                                        │  [Go →]      │ │
│  └────────────────────────────────────────────────────────┴───────────────┘ │
│                                                                              │
│  [← Previous]  [Save & Next →]              [Submit Test]                   │
│                                                                              │
│  ── STATUS BAR ──────────────────────────────────────────────────────────   │
│  ● Answered: 11  ◐ Marked for Review: 3  ○ Not Visited: 38  ✗ Not Ans: 23│
│  Connection: ✅ Online · Auto-save: 12 sec ago · Language: [English ▼]     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. SSC CGL Pattern (TCS iON Style)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  SSC CGL Tier-I Mock #12                    Time Left: 00:42:18             │
│  Section: Quantitative Aptitude (Q8 of 25)                                  │
│  ────────────────────────────────────────────────────────────────────────   │
│                                                                              │
│  ┌─── SECTIONS TAB ─────────────────────────────────────────────────────┐  │
│  │  [Quant (12/25)] [Reasoning (0/25)] [English (0/25)] [GK (0/25)]    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Q.8  If the HCF of two numbers is 12 and their LCM is 360, and           │
│  one number is 60, find the other number.                                   │
│                                                                              │
│  (A)  48          ( )                                                       │
│  (B)  72          (●)  ← selected                                          │
│  (C)  84          ( )                                                       │
│  (D)  96          ( )                                                       │
│                                                                              │
│  Marking: +2 correct · -0.50 incorrect · 0 unanswered                      │
│                                                                              │
│  [Clear]  [Mark for Review]  [← Prev]  [Save & Next →]                    │
│                                                                              │
│  ── QUESTION PALETTE (Quant) ────────────────────────────────────────────  │
│  ●1 ●2 ●3 ●4 ●5 ●6 ●7 ▶8 ○9 ○10 ○11 ○12 ○13 ○14 ○15                   │
│  ○16 ○17 ○18 ○19 ○20 ○21 ○22 ○23 ○24 ○25                                 │
│                                                                              │
│  Note: In SSC CGL, you can switch between sections freely.                 │
│  Connection: ✅  · Auto-saved · Language: [Telugu ▼]                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Numerical Answer Type (JEE Advanced Pattern)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Q.18 (Numerical)                                                            │
│                                                                              │
│  A ball is thrown vertically upward with initial velocity 20 m/s.           │
│  Find the maximum height reached (in metres).                               │
│  Take g = 10 m/s².                                                          │
│                                                                              │
│  Answer: [ 20.00 ]  (up to 2 decimal places)                               │
│                                                                              │
│  Virtual keypad:                                                             │
│  ┌───┬───┬───┬───┐                                                          │
│  │ 7 │ 8 │ 9 │ ← │                                                          │
│  ├───┼───┼───┼───┤                                                          │
│  │ 4 │ 5 │ 6 │ . │                                                          │
│  ├───┼───┼───┼───┤                                                          │
│  │ 1 │ 2 │ 3 │ - │                                                          │
│  ├───┼───┼───┼───┤                                                          │
│  │ 0 │ C │   │ ✓ │                                                          │
│  └───┴───┴───┴───┘                                                          │
│                                                                              │
│  Marking: +4 correct · 0 incorrect · 0 unanswered (no negative marking)    │
│                                                                              │
│  [Clear]  [Mark for Review]  [← Prev]  [Save & Next →]                    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Offline Resilience & Auto-Save

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ⚠️ CONNECTION LOST                                                          │
│                                                                              │
│  Don't worry — your test continues normally.                                │
│                                                                              │
│  ✅ All 11 answered questions are saved locally                             │
│  ✅ Timer continues running (synced when reconnected)                       │
│  ✅ You can continue answering — responses saved to your device            │
│  ✅ When connection returns, all responses sync automatically              │
│                                                                              │
│  Auto-save frequency: Every response is saved instantly to local storage.   │
│  Last server sync: 2 minutes ago (11 responses synced)                     │
│                                                                              │
│  [Continue Test — I understand]                                              │
│                                                                              │
│  ── TECH DETAILS (collapsible) ──────────────────────────────────────────   │
│  Local storage: 11 responses (2.4 KB) stored in IndexedDB                  │
│  Service worker: Active — test assets cached offline                        │
│  Reconnection attempts: Every 5 seconds                                     │
│  If connection doesn't return within 30 minutes, responses will be          │
│  synced next time you open EduForge.                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Test Submission Confirmation

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  SUBMIT TEST — JEE Mains Mock #25                                            │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  Summary Before Submission                                             │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │                                                                       │  │
│  │  ┌──────────────────┬──────────┬──────────┬──────────┬────────────┐  │  │
│  │  │ Section          │ Answered │ Review   │ Not Ans  │ Not Visit  │  │  │
│  │  ├──────────────────┼──────────┼──────────┼──────────┼────────────┤  │  │
│  │  │ Physics          │ 22       │ 1        │ 2        │ 0          │  │  │
│  │  │ Chemistry        │ 18       │ 3        │ 4        │ 0          │  │  │
│  │  │ Mathematics      │ 24       │ 0        │ 1        │ 0          │  │  │
│  │  ├──────────────────┼──────────┼──────────┼──────────┼────────────┤  │  │
│  │  │ TOTAL            │ 64       │ 4        │ 7        │ 0          │  │  │
│  │  └──────────────────┴──────────┴──────────┴──────────┴────────────┘  │  │
│  │                                                                       │  │
│  │  Time remaining: 00:12:18                                            │  │
│  │  ⚠️ You have 7 unanswered questions. Review before submitting?      │  │
│  │                                                                       │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  [Go Back to Test]                    [Submit Final — I'm Done]             │
│                                                                              │
│  ⚠️ Once submitted, you cannot change your answers.                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `POST` | `/api/v1/student/tests/{test_id}/start` | Start test session (returns questions + session token) |
| 2 | `POST` | `/api/v1/student/tests/{test_id}/response` | Save single question response |
| 3 | `POST` | `/api/v1/student/tests/{test_id}/responses/sync` | Bulk sync offline-cached responses |
| 4 | `PUT` | `/api/v1/student/tests/{test_id}/response/{q_id}/mark-review` | Mark/unmark question for review |
| 5 | `GET` | `/api/v1/student/tests/{test_id}/status` | Current test status (time, answered count) |
| 6 | `POST` | `/api/v1/student/tests/{test_id}/submit` | Submit test (final, irreversible) |
| 7 | `GET` | `/api/v1/student/tests/{test_id}/question/{q_id}` | Get single question with assets |
| 8 | `POST` | `/api/v1/student/tests/{test_id}/language/{lang}` | Switch question language mid-test |
| 9 | `GET` | `/api/v1/student/tests/{test_id}/heartbeat` | Connection health check (every 30s) |

---

## 7. Business Rules

- The test interface is the single most performance-critical page — it must render the first question within 1.5 seconds on a ₹8,000 Android phone over 4G; questions and their assets (images, LaTeX-rendered equations) are pre-fetched in a 5-question lookahead window; the entire test payload (all 75 questions for JEE) is downloaded at test start (compressed: ~800 KB for text + images) and cached via Service Worker, so the student can continue even if they lose connectivity mid-test; LaTeX rendering uses KaTeX (not MathJax) for 10x faster rendering on low-end devices.

- Response auto-save follows a **local-first architecture** — every answer selection is immediately written to IndexedDB (local browser storage) with a timestamp; a background sync worker pushes responses to the server every 30 seconds or on every 5th response (whichever comes first); if the student's browser crashes or phone dies, reopening the test URL within the test window recovers all locally-saved responses and resumes from where they left off; the server reconciles local vs server state using timestamps (latest wins).

- The question palette replicates the exact visual language of the target exam — JEE uses NTA's green (answered), orange (marked for review), red (not answered), grey (not visited) colour scheme; SSC uses TCS iON's blue/red/green scheme; this match is deliberate: students who practise on EduForge should experience zero interface friction when they sit for the real exam; each domain's test interface is a separate React component that applies the appropriate theme.

- Language switching mid-test is supported for bilingual exams (SSC, Banking, State PSC) — the student can toggle between English and their preferred regional language (Telugu, Hindi, Tamil, etc.) at any time during the test; switching is per-question (not per-test), so a student can read a GK question in Telugu and a Quant question in English; the language toggle does not reset the timer or lose any responses; questions are pre-loaded in all available languages at test start.

- Timer management: the timer runs server-side (authoritative) and client-side (for display); every heartbeat (30 seconds) syncs the client timer with the server; if the client timer drifts more than 10 seconds from the server (e.g., due to device sleep), it auto-corrects; when the timer reaches zero, the test auto-submits all saved responses — the student receives a "Time's up! Your test has been submitted automatically" modal; early submission is allowed at any time with a confirmation dialog showing the summary.

- For students with accessibility needs (extra time approved via A-04 Settings), the timer shows the extended duration (e.g., 3h 60min instead of 3h for 33% extra time) and the question palette shows a small accessibility icon; the extra time is applied server-side so it cannot be manipulated client-side.

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division C*
