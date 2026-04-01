# H-05 — Content Upload & Management

> **URL:** `/coaching/online/content/`
> **File:** `h-05-content-upload.md`
> **Priority:** P2
> **Roles:** Online Coordinator (K4) · Faculty (K2) · Academic Director (K5)

---

## 1. Content Library

```
CONTENT LIBRARY — All Online Batches
As of 30 March 2026  |  Total items: 2,842

  BY TYPE:
    Type                │ Count  │ Storage   │ Avg Size   │ Last Added
    ────────────────────┼────────┼───────────┼────────────┼────────────────
    Video (recorded)    │ 1,240  │ 1.84 TB   │  1.52 GB   │ 30 Mar 2026
    Video (pre-produced)│   286  │ 0.42 TB   │  1.48 GB   │ 22 Mar 2026
    PDF (notes/theory)  │   468  │   4.2 GB  │  9.2 MB    │ 28 Mar 2026
    PDF (question sets) │   356  │   2.8 GB  │  8.1 MB    │ 27 Mar 2026
    Presentations (PPT) │   184  │   1.6 GB  │  8.7 MB    │ 25 Mar 2026
    Audio (revision)    │   154  │   3.2 GB  │ 21.0 MB    │ 18 Mar 2026
    Diagrams / Images   │   154  │   0.4 GB  │  2.7 MB    │ 20 Mar 2026
    ────────────────────┴────────┴───────────┴────────────┴────────────────
    TOTAL               │ 2,842  │ 2.84 TB   │            │

  BY SUBJECT (videos only):
    Quant:      428 videos | Reasoning: 382 videos | English: 268 videos
    GK/CA:      224 videos | Others:    224 videos
```

---

## 2. Upload New Content

```
UPLOAD CONTENT

  Title:        [Quant: Caselet DI — March 2026 Full Session         ]
  Subject:      [Quantitative Aptitude ▼]
  Topic:        [Caselet Data Interpretation ▼]
  Content type: (●) Video — Recorded session  ( ) PDF  ( ) Presentation  ( ) Audio

  FILE:         [Browse: caselet_di_30mar2026.mp4 ← Uploading... 68%]
  File size:    1.84 GB  |  Format: MP4  |  Quality: 720p
  Upload speed: 24 MB/s  |  ETA: 3 min 12 sec

  ACCESS:
    Available to batches: [✓] SSC CGL Live Online  [✓] SSC CGL Online (May 26)
                          [ ] Banking Online        [ ] All batches
    Access from:   [30 March 2026 ▼] (publish immediately after upload)
    Access until:  [Auto: 90 days → 28 June 2026 ▼]

  SECURITY:
    Watermark:     (●) Student name + roll no. on video (dynamic watermark) ✅
    Download:      ( ) Enabled  (●) Disabled — stream only
    HLS encrypt:   ✅ Enabled (AES-128)

  METADATA:
    Tags:          [caselet, DI, data interpretation, March 2026, Suresh Kumar]
    Curriculum link: [Unit 7: Data Interpretation > Caselet DI ▼]
    Difficulty:    [Medium ▼]

  [Upload]   [Save Draft]   [Cancel]

  ⚠️ After upload: transcript auto-generated (15–20 min) | Chapters: manual
```

---

## 3. Content Moderation Queue

```
CONTENT MODERATION — Pending Review (8 items)

  #  │ Submitted by   │ Type  │ Title                       │ Submitted    │ Status
  ───┼────────────────┼───────┼─────────────────────────────┼──────────────┼──────────────
  1  │ Suresh K.      │ Video │ Quant: Caselet DI (Mar 30)  │ 30 Mar 11 PM │ ⏳ Processing
  2  │ Kavita M.      │ PDF   │ English: Cloze Test Notes   │ 29 Mar 4 PM  │ ✅ Approved
  3  │ Mohan R.       │ PPT   │ Reasoning: Input-Output Ch6 │ 29 Mar 3 PM  │ ✅ Approved
  4  │ Ravi S.        │ PDF   │ GK: March 2026 CA Digest    │ 28 Mar 6 PM  │ ✅ Approved
  5  │ Suresh K.      │ Video │ Quant: Sprint #18 solution  │ 28 Mar 9 PM  │ ✅ Published
  6  │ Kavita M.      │ Audio │ Vocab Revision — Mar Week 4 │ 27 Mar 2 PM  │ ✅ Published
  7  │ Mohan R.       │ Video │ Reasoning: Complex Seating  │ 26 Mar 8 PM  │ ⚠️ Review
  8  │ Suresh K.      │ PDF   │ Quant: Formula Sheet Ch7–9  │ 25 Mar 5 PM  │ ✅ Published

  REVIEW ITEM #7: Complex Seating video
    Flagged by: Academic Director
    Reason: "Video runs 94 minutes — too long for a single session (standard: ≤ 70 min).
             Please split into Part 1 and Part 2."
    Action: Mr. Mohan Rao to re-upload as 2 parts by Apr 2.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/online/content/` | Content library with filters |
| 2 | `POST` | `/api/v1/coaching/{id}/online/content/` | Upload new content item |
| 3 | `GET` | `/api/v1/coaching/{id}/online/content/{cid}/` | Content item detail |
| 4 | `PATCH` | `/api/v1/coaching/{id}/online/content/{cid}/` | Update metadata or access settings |
| 5 | `GET` | `/api/v1/coaching/{id}/online/content/moderation/` | Content pending moderation |
| 6 | `POST` | `/api/v1/coaching/{id}/online/content/{cid}/approve/` | Approve or reject content |

---

## 5. Business Rules

- All uploaded content is moderated before being published to students; the Academic Director or Online Coordinator reviews the content for quality (audio, video clarity), accuracy (factual errors, wrong answer keys in PDFs), and length (videos over 70 minutes should be split); moderation is typically completed within 24 hours; faculty should upload content at least 24 hours before they need it published; emergency uploads (same-day) require Online Coordinator approval and skip the standard moderation queue
- Dynamic video watermarking (student's name and roll number overlaid on the video) deters screen-recording piracy; a student who records the screen and shares it online has their identity embedded in the video; TCC uses this evidence to take action (batch removal, legal notice for commercial piracy); the watermark is semi-transparent and positioned at a random location to prevent easy cropping; students are informed about the watermark in the platform's terms of use
- HLS (HTTP Live Streaming) with AES-128 encryption is the minimum content protection standard for all videos; unencrypted video files served via plain HTTPS are not acceptable; the HLS key is served from a separate authentication server that validates the student's session before serving the key; this means even if a student captures the HLS stream, they cannot decrypt it without a valid authenticated session; TCC's platform team must maintain the key server's uptime as a dependency of video access
- Content linked to the curriculum tracker (Unit 7 → Caselet DI) allows students to navigate to relevant recordings from the curriculum page; if a topic in the curriculum has no recording, the coordinator is alerted; curriculum coverage gaps (topics with classes in the schedule but no supporting recordings) are tracked as a content quality metric; the target is 90%+ curriculum coverage with supporting recordings or PDFs within 48 hours of the live class
- Faculty retain copyright in their uploaded study materials (PDFs, PPTs, self-created content) but grant TCC a non-exclusive licence to use, store, and distribute this content to enrolled students during the contract period; recordings of live sessions are TCC's property (facility provided by TCC, on TCC's platform); this distinction is clarified in the faculty employment contract; a faculty who leaves TCC can request removal of their self-created PDFs from the platform but cannot remove session recordings

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division H*
