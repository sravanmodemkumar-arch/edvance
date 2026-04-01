# D-05 — Current Affairs & Daily Updates

> **URL:** `/student/learn/current-affairs`
> **File:** `d-05-current-affairs.md`
> **Priority:** P1
> **Roles:** Student (S2–S6) — Free: weekly digest; Premium: daily digest + MCQs + audio

---

## Overview

Daily current affairs updates essential for government exam preparation (SSC, Banking, Railways, UPSC, State PSC). Covers national affairs, international events, economy, science & technology, awards, sports, and appointments. Each item is tagged by exam relevance — an RBI policy change is tagged "Banking + SSC + UPSC" while a sports award is tagged "SSC + Railways." Updates are available as: (1) text digest, (2) MCQs (practice immediately), (3) audio summary (for commute listening), (4) monthly PDF compilation. This is the #1 daily engagement driver for the 2,80,00,000 government exam students on EduForge.

---

## 1. Today's Current Affairs

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  CURRENT AFFAIRS — 01 April 2026              [Today ●] [This Week] [Month] │
│                                                                              │
│  🎧 Listen to today's summary (12 min audio)  [Play ▶ ⭐ Premium]          │
│                                                                              │
│  ── TOP 10 NEWS TODAY ───────────────────────────────────────────────────   │
│                                                                              │
│  1. RBI maintains repo rate at 6.25% in April monetary policy               │
│     Exams: [Banking] [SSC] [UPSC]  Importance: 🔴 High                    │
│     Key fact: Repo 6.25%, Reverse repo 3.35%, CRR 4.5%, SLR 18%          │
│     [Read full →]  [Practice MCQ →]                                        │
│                                                                              │
│  2. India launches Aditya-L2 solar observation mission                     │
│     Exams: [SSC] [Railways] [UPSC] [State PSC]  Importance: 🔴 High      │
│     Key fact: Launched from SDSC-SHAR, Sriharikota. India's first          │
│     dedicated solar observatory at Lagrange Point L1.                       │
│     [Read full →]  [Practice MCQ →]                                        │
│                                                                              │
│  3. APPSC Group-2 2026 notification released — 1,200 vacancies             │
│     Exams: [APPSC]  Importance: 🔴 Critical (for AP students)             │
│     Key fact: Last date: 15-May-2026. Age: 18-42. Qualifying: Degree.     │
│     [Read full →]  [View notification →]                                    │
│                                                                              │
│  4. Supreme Court landmark ruling on Right to Privacy (Article 21)         │
│  5. Union Cabinet approves National Digital Health Mission Phase 2          │
│  6. Padma Awards 2026 announced — full list                                │
│  ... [View all 10 →]                                                        │
│                                                                              │
│  ── PRACTICE TODAY'S NEWS ───────────────────────────────────────────────   │
│  📝 10 MCQs from today's current affairs  [Start Quiz →]                   │
│  Takes 5 min. Tests all 10 news items above.                               │
│                                                                              │
│  ── MONTHLY COMPILATION ─────────────────────────────────────────────────   │
│  📄 March 2026 — Complete Monthly Digest (42 pages)                        │
│  Covers all 310 news items from March + 150 MCQs                           │
│  [Download PDF ↓ ⭐ Premium]  [Read Online →]                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Exam-Filtered View (SSC CGL Focus)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  CURRENT AFFAIRS — SSC CGL Relevant Only          Suresh Babu, Vijayawada  │
│                                                                              │
│  Filter: [All ▼] → [SSC CGL only ●]                                       │
│                                                                              │
│  Items relevant to SSC CGL Tier-I GK section:                              │
│                                                                              │
│  1. RBI repo rate 6.25% — expected in Economy section                      │
│     Previous year: SSC CGL 2025 had 2 questions on RBI policy              │
│     [Quick note →]  [MCQ →]                                                │
│                                                                              │
│  2. Aditya-L2 — expected in Science & Technology section                   │
│     Tip: Remember Lagrange Point L1 (not L2 — common trap!)               │
│     [Quick note →]  [MCQ →]                                                │
│                                                                              │
│  3. Padma Awards — Padma Vibhushan, Padma Bhushan, Padma Shri             │
│     Tip: SSC frequently asks "Who received Padma Vibhushan in [year]?"    │
│     [Full list →]  [MCQ →]                                                 │
│                                                                              │
│  Today's SSC-relevant items: 6 of 10 · [View All →]                       │
│                                                                              │
│  ── WEEK IN REVIEW ──────────────────────────────────────────────────────   │
│  This week: 38 SSC-relevant news items                                     │
│  📝 Weekly quiz: 25 MCQs covering all 38 items  [Start →]                 │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/student/current-affairs/today` | Today's news items (with exam tags) |
| 2 | `GET` | `/api/v1/student/current-affairs/today?exam={exam}` | Filtered by exam relevance |
| 3 | `GET` | `/api/v1/student/current-affairs/quiz/today` | Today's current affairs MCQ quiz |
| 4 | `GET` | `/api/v1/student/current-affairs/weekly?week={date}` | Weekly compilation |
| 5 | `GET` | `/api/v1/student/current-affairs/monthly/{month}/pdf` | Monthly digest PDF (Premium) |
| 6 | `GET` | `/api/v1/student/current-affairs/audio/today` | Today's audio summary URL (Premium) |
| 7 | `GET` | `/api/v1/student/current-affairs/{item_id}` | Full article for a news item |

---

## 4. Business Rules

- Current affairs content is published daily by 6:00 AM IST — the EduForge content team (Group 1, Division D) curates 8–12 news items from the previous day, tags each with relevant exams, assigns importance level (High/Medium/Low), and writes a concise summary with key facts that students need to memorise for MCQs; each item includes 1–2 practice MCQs written in the style of actual exam questions; the publication pipeline runs from 4:00 AM (curation) to 5:30 AM (review) to 6:00 AM (publish).

- Free students receive a weekly digest (every Monday, covering the past 7 days); Premium students receive the daily digest, daily MCQ quiz, audio summary, and monthly PDF compilation; the daily current affairs quiz is the single highest-engagement daily activity — 42,00,000 students take the daily CA quiz, with an average completion time of 5 minutes; this is also the most commonly shared content on WhatsApp study groups, driving organic growth.

- Audio summaries are AI-narrated (text-to-speech with natural voice in English, Telugu, and Hindi) and optimised for commute listening — each daily summary is 10–15 minutes at normal speed; working professionals like Suresh listen during their morning/evening bus commute; the audio is downloadable for offline playback (Premium only); play speed can be adjusted (1x, 1.25x, 1.5x, 2x).

- Exam-specific filtering uses a tagging system where each news item is tagged with 1–5 exams where it's likely to appear as a question; the tags are based on historical analysis — if "RBI monetary policy" has appeared in 3 of the last 5 SSC CGL papers, it's tagged as "High importance for SSC CGL"; State PSC tags are further refined by state (APPSC-relevant vs TSPSC-relevant items may differ based on local governance news).

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division D*
