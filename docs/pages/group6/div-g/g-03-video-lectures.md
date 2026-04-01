# G-03 — Video Lectures

> **URL:** `/exam/study/video/{video-id}/`
> **File:** `g-03-video-lectures.md`
> **Priority:** P1
> **Data:** `study_material WHERE type = 'video'` — linked to syllabus nodes, bilingual

---

## 1. Video Player

```
VIDEO LECTURE — Panchayati Raj System (73rd Amendment)
APPSC Group 2 | Indian Polity | Telugu | 32 min | ⭐ 4.6/5.0

  ┌──────────────────────────────────────────────────────────────────────┐
  │  ┌────────────────────────────────────────────────────────────────┐ │
  │  │                                                                │ │
  │  │                    [▶ VIDEO PLAYER]                            │ │
  │  │           73వ రాజ్యాంగ సవరణ — పంచాయతీ రాజ్                    │ │
  │  │                                                                │ │
  │  │  ▶  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━        │ │
  │  │  12:48 / 32:14    [1x ▼]  [CC]  [⛶ Fullscreen]               │ │
  │  └────────────────────────────────────────────────────────────────┘ │
  │                                                                      │
  │  CHAPTERS (auto-generated from timestamps):                          │
  │    00:00 — Introduction: Why 73rd Amendment?                         │
  │    04:20 — Three-tier structure: Village, Block, District           │
  │    12:48 — Gram Sabha: Powers and functions  ← currently playing    │
  │    18:35 — Elections: State Election Commission                     │
  │    24:10 — Reservations: SC/ST, Women (⅓)                          │
  │    28:40 — 11th Schedule: 29 subjects for Panchayats               │
  │    31:00 — Summary and exam tips                                    │
  │                                                                      │
  │  [📝 Take notes]  [🔖 Bookmark]  [📋 Practice Qs on this topic (14)]│
  │  [▶ Next: 74th Amendment — Municipalities (28 min)]                  │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/study/video/{vid}/` | Video metadata + stream URL |
| 2 | `PATCH` | `/api/v1/exam/study/video/{vid}/progress/` | Update watch progress (timestamp) |
| 3 | `GET` | `/api/v1/exam/study/video/{vid}/chapters/` | Chapter timestamps |

---

## 5. Business Rules

- Video lectures are hosted on EduForge's own infrastructure (or a CDN like Cloudflare Stream / Mux) — not YouTube; hosting on EduForge's own player ensures: no ads interrupting study, no algorithm-driven distractions ("recommended" videos), DRM protection against screen recording, and analytics (watch time, drop-off points); YouTube embeds are used only for free promotional content (seminar recordings, success stories)
- Telugu-language video lectures are recorded by Telugu-speaking subject experts — not dubbed from English recordings; the teaching style, examples, and cultural references are native to Telugu-medium learners; an English lecture translated to Telugu via voiceover is perceptibly different from a natively Telugu lecture; the content team hires Telugu-medium faculty for state exam content (APPSC, TSPSC) and English/Hindi faculty for central exam content
- Chapter timestamps enable non-linear viewing; a student who already knows "Three-tier structure" can skip directly to "Reservations: SC/ST, Women" (24:10); this is critical for revision — a student rewatching before the exam doesn't need 32 minutes; they need the 4-minute segment on the specific sub-topic they are weak in; chapters are created by the content team during the upload review process; auto-generated chapters (from audio transcription + AI) are used as a draft and refined manually
- Watch progress is tracked at the second level; a student who watches 12:48 of a 32:14 video shows 40% progress; resuming later starts from 12:48; this feeds into syllabus coverage (A-05) the same way note reading progress does — watching 100% of the Panchayati Raj video marks the corresponding syllabus node as partially covered; completion of both the video + associated practice questions marks the node as fully covered
- Playback speed control (0.5×, 1×, 1.25×, 1.5×, 2×) is essential for exam preparation; students revising a topic they already know prefer 1.5–2× speed; students learning a new concept for the first time may use 0.75× or 1×; the default is 1× and the player remembers the user's last-used speed across sessions; closed captions (CC) in both Telugu and English support hearing-impaired users and students studying in noisy environments

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division G*
