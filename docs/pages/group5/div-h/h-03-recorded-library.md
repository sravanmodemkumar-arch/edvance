# H-03 — Recorded Session Library

> **URL:** `/coaching/online/recordings/`
> **File:** `h-03-recorded-library.md`
> **Priority:** P1
> **Roles:** Online Coordinator (K4) · Faculty (K2) · Academic Director (K5)

---

## 1. Recording Library

```
RECORDED SESSION LIBRARY — SSC CGL Live Online
As of 30 March 2026  |  Total: 186 recordings  |  Storage: 1.24 TB

  Filter: [All Topics ▼]  [All Faculty ▼]  [Date ▼]  [Status ▼]  [Search: _____]

  #   │ Date       │ Topic                       │ Faculty     │ Duration │ Views  │ Status
  ────┼────────────┼─────────────────────────────┼─────────────┼──────────┼────────┼────────────
  1   │ 29 Mar 26  │ English: Cloze Test (Adv.)  │ Kavita M.   │ 58 min   │  168   │ ✅ Live
  2   │ 28 Mar 26  │ Reasoning: Blood Relations  │ Mohan R.    │ 62 min   │  154   │ ✅ Live
  3   │ 27 Mar 26  │ GK: Economy CA (Mar W4)     │ Ravi S.     │ 56 min   │  132   │ ✅ Live
  4   │ 26 Mar 26  │ Quant: DI Caselets Part 2   │ Suresh K.   │ 61 min   │  178   │ ✅ Live
  5   │ 25 Mar 26  │ English: Error Spotting     │ Kavita M.   │ 58 min   │  144   │ ✅ Live
  6   │ 24 Mar 26  │ Reasoning: Coding-Decoding  │ Mohan R.    │ 60 min   │  126   │ ✅ Live
  7   │ 22 Mar 26  │ Quant: Mensuration 3D       │ Suresh K.   │ 64 min   │  182   │ ✅ Live
  8   │ 20 Mar 26  │ GK: Polity — Parliament     │ Ravi S.     │ 54 min   │  116   │ ✅ Live
  ...  (178 more — view all)

  TOP VIEWED (last 30 days):
    1. Quant: DI Caselets Part 1 (Mar 12) — 224 views
    2. Reasoning: Blood Relations (Mar 28) — 154 views
    3. Quant: Mensuration 3D (Mar 22) — 182 views
    → High views = high-demand topics = candidates for repeat supplementary content
```

---

## 2. Recording Detail

```
RECORDING DETAIL — "Quant: DI Caselets Part 1" (12 Mar 2026)

  Faculty:     Mr. Suresh Kumar (Quant)
  Duration:    64 minutes
  Views:       224 (38 unique students × avg 5.9 sessions per student)
  Avg watch %: 68.4%  (students watch 44 of 64 minutes on average)
  Drop-off:    High at 38 min mark (after full DI solution; students stop)

  ACCESS:
    Available to:  SSC CGL Live Online batch (186 students)
    Expiry:        12 Jun 2026 (90 days from recording date)
    Download:      ❌ Disabled (stream only, signed URL, 4-hr expiry)
    Extended by:   — (not extended yet; expires Jun 12)

  QUALITY:
    Audio:         ✅ Clear
    Video:         ✅ 720p
    Chapters:      Not marked (auto-chapter in progress)
    Transcript:    ✅ Auto-generated (English, 88% accuracy)

  ACTIONS:
    [Extend Expiry to Sep 12]   [Mark Chapters]   [Download (Faculty only)]
    [Add to Supplementary Pack] [Flag for Review]  [Archive]
```

---

## 3. Content Expiry Management

```
RECORDING EXPIRY TRACKER — Upcoming Expirations

  Expiring in next 30 days (Apr 2026):
    Recording                     │ Expiry Date │ Views │ Action
    ──────────────────────────────┼─────────────┼───────┼──────────────────────────
    Quant: Percentage (Jan 12)    │ Apr 12 2026 │   88  │ [Extend] or [Archive]
    Reasoning: Series (Jan 14)    │ Apr 14 2026 │   76  │ [Extend] or [Archive]
    GK: Union Budget (Jan 15)     │ Apr 15 2026 │  142  │ [Extend] ← high views ⚠️
    English: Vocab Part 1 (Jan 18)│ Apr 18 2026 │   62  │ [Archive] (low views)
    Quant: Time & Work (Jan 20)   │ Apr 20 2026 │  104  │ [Extend]
    ...  (22 more)

  POLICY:
    Auto-archive after 90 days (default)
    Coordinator can extend by 30 or 90 days per recording
    Archived = retrievable within 24 hours if student requests
    Permanently deleted: 3 years after recording (regulatory retention period)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/online/recordings/?batch={bid}` | Recording library for a batch |
| 2 | `GET` | `/api/v1/coaching/{id}/online/recordings/{rid}/` | Recording detail and analytics |
| 3 | `GET` | `/api/v1/coaching/{id}/online/recordings/expiring/?days=30` | Recordings expiring soon |
| 4 | `PATCH` | `/api/v1/coaching/{id}/online/recordings/{rid}/expiry/` | Extend or update expiry |
| 5 | `GET` | `/api/v1/coaching/{id}/online/recordings/{rid}/stream/` | Get signed streaming URL (4-hr expiry) |
| 6 | `POST` | `/api/v1/coaching/{id}/online/recordings/{rid}/archive/` | Archive a recording |

---

## 5. Business Rules

- Recorded sessions are the most-consumed content in the online product; students who miss live sessions and students who want to re-watch specific topics both rely on recordings; the 90-day access window is a commercial decision — students who want permanent access can purchase the "all-access archive" add-on; the default 90 days covers the batch's revision period plus some buffer; extending access for high-view recordings (like DI Caselets with 224 views) retains value for students actively using the content
- Video streaming uses signed URLs that expire every 4 hours; when a student clicks "play," EduForge generates a signed URL valid for 4 hours; the student's app uses this URL to stream; if the URL is copied and shared, it expires quickly and is useless; if the student downloads the video using a screen-recording tool (technically possible), TCC cannot completely prevent this but the combination of low-quality DRM (digital rights management via HLS encryption) and platform monitoring (unusual download-speed patterns) reduces commercial piracy risk
- Watch percentage analytics (students watching 68.4% of a recording on average) identify where students stop engaging; a drop-off at minute 38 of a 64-minute session means the content after 38 minutes is either too advanced, too slow, or students feel they've learned enough; the faculty reviews drop-off data to identify whether the second half of a session needs restructuring; high drop-offs on a specific topic across multiple recordings confirm that the topic needs a different teaching approach
- Auto-generated transcripts (88% accuracy) serve two purposes: accessibility (for students with hearing impairments) and searchability (students can search for "frustum" within a transcript to jump to that portion of the recording); the coordinator's task is to review and correct transcripts for Quant terms (LaTeX-heavy, poor audio recognition) within 7 days of recording; uncorrected Quant transcripts with "freight some" instead of "frustum" make the search feature useless for those sessions
- The 3-year permanent retention policy is based on the limitation period for consumer complaints under the Consumer Protection Act 2019 (2-year limitation with a 1-year buffer); if a student files a complaint 2 years after completing the course claiming "TCC's content was faulty," TCC needs the original recordings as evidence; the coordinator must not delete or override the permanent deletion policy for any recording within the 3-year window, regardless of storage pressure

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division H*
