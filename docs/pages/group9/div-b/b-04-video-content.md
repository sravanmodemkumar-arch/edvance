# B-04 — Video Content Upload

> **URL:** `/content-partner/author/video-content`
> **File:** `b-04-video-content.md`
> **Priority:** P2
> **Roles:** Content Partner · EduForge Editorial Team (review queue)

---

## Overview

The Video Content Upload module allows content partners to contribute lecture videos, topic walkthroughs, and problem-solving sessions to the EduForge platform. Dr. Venkat Rao records quantitative aptitude lectures from his home studio in Visakhapatnam — covering topics like HCF & LCM shortcuts, Remainder Theorem tricks, and Data Interpretation approaches — which are then encoded for adaptive streaming, tagged to syllabus topics, and made available to students preparing for APPSC, SSC CGL, and Banking exams.

---

## Mockup 1 — Video Upload Form

```
+------------------------------------------------------------------+
| EduForge Content Partner Portal                   Dr. Venkat Rao  |
+------------------------------------------------------------------+
| Dashboard > Author > Video Content > New Upload                   |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------------------------------------------------+  |
|  | VIDEO CONTENT UPLOAD                                        |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  Video Title:                                               |  |
|  |  [ HCF & LCM — Shortcut Methods for Competitive Exams  ]   |  |
|  |                                                             |  |
|  |  +------------------------------------------------------+  |  |
|  |  |                                                       |  |  |
|  |  |        Drag & drop your video file here, or click     |  |  |
|  |  |                                                       |  |  |
|  |  |              [ Browse Files... ]                      |  |  |
|  |  |                                                       |  |  |
|  |  |  Accepted: .mp4, .mov, .avi, .mkv                     |  |  |
|  |  |  Max size: 2 GB | Max duration: 90 min                |  |  |
|  |  |  Recommended: 1080p, H.264/H.265, 30fps               |  |  |
|  |  |                                                       |  |  |
|  |  +------------------------------------------------------+  |  |
|  |                                                             |  |
|  |  Uploaded: hcf_lcm_shortcuts_vr.mp4                         |  |
|  |  Size: 845 MB | Duration: 42:18 | Resolution: 1920x1080    |  |
|  |  Codec: H.264 | Audio: AAC 48kHz stereo                     |  |
|  |                                                             |  |
|  |  Language:  (o) English  ( ) Telugu  ( ) Hindi               |  |
|  |                                                             |  |
|  |  SYLLABUS MAPPING:                                          |  |
|  |  Exam(s):   [x] APPSC Group 1/2  [x] SSC CGL               |  |
|  |             [ ] SSC CHSL  [x] IBPS PO  [ ] RRB NTPC        |  |
|  |  Subject:   [ Quantitative Aptitude    v ]                  |  |
|  |  Topic:     [ Number Systems           v ]                  |  |
|  |  Sub-Topic: [ HCF & LCM               v ]                  |  |
|  |                                                             |  |
|  |  Difficulty Level: [ Intermediate          v ]              |  |
|  |                                                             |  |
|  |  Description:                                               |  |
|  |  +------------------------------------------------------+  |  |
|  |  | In this lecture, Dr. Venkat Rao explains 5 shortcut   |  |  |
|  |  | methods for solving HCF and LCM problems that         |  |  |
|  |  | frequently appear in APPSC, SSC CGL, and Banking      |  |  |
|  |  | exams. Includes 12 solved examples with step-by-step  |  |  |
|  |  | approaches and time-saving tricks.                     |  |  |
|  |  +------------------------------------------------------+  |  |
|  |                                                             |  |
|  +------------------------------------------------------------+  |
|  |  [ Continue to Thumbnail & Transcript ]                     |  |
|  +------------------------------------------------------------+  |
|                                                                   |
+------------------------------------------------------------------+
```

---

## Mockup 2 — Thumbnail Selection & Transcript Upload

```
+------------------------------------------------------------------+
| VIDEO CONTENT — Thumbnail & Transcript                            |
+------------------------------------------------------------------+
|                                                                   |
|  Video: HCF & LCM — Shortcut Methods for Competitive Exams       |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | THUMBNAIL                                                   |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  Auto-generated thumbnails (select one):                    |  |
|  |                                                             |  |
|  |  +----------+  +----------+  +----------+  +----------+    |  |
|  |  |          |  |          |  |          |  |          |    |  |
|  |  | [00:00]  |  | [10:32]  |  | [21:15]  |  | [35:40]  |    |  |
|  |  |  Frame 1 |  |  Frame 2 |  |  Frame 3 |  |  Frame 4 |    |  |
|  |  |          |  |          |  |          |  |          |    |  |
|  |  +----------+  +--[SEL]---+  +----------+  +----------+    |  |
|  |       ( )           (o)           ( )           ( )         |  |
|  |                                                             |  |
|  |  Or upload custom thumbnail:                                |  |
|  |  [ Browse... ]  (JPG/PNG, 1280x720 recommended, max 1 MB)  |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | TRANSCRIPT                                                  |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  (o) Auto-generate transcript (speech-to-text)              |  |
|  |  ( ) Upload transcript file (.srt, .vtt)                    |  |
|  |  ( ) No transcript                                          |  |
|  |                                                             |  |
|  |  Auto-generate options:                                     |  |
|  |  Primary language: [ English   v ]                          |  |
|  |  [x] Generate Telugu subtitles (auto-translate)             |  |
|  |  [x] Generate Hindi subtitles (auto-translate)              |  |
|  |                                                             |  |
|  |  Note: Auto-generated transcripts take 10-15 minutes.       |  |
|  |  You can review and edit the transcript after generation.    |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | CHAPTER MARKERS (Optional)                                  |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  Timestamp | Title                         | [+ Add]       |  |
|  |  ----------|-------------------------------|               |  |
|  |  00:00     | Introduction                   | [x]           |  |
|  |  02:15     | Method 1: Prime Factorization  | [x]           |  |
|  |  08:40     | Method 2: Division Method      | [x]           |  |
|  |  15:20     | Method 3: LCM via HCF         | [x]           |  |
|  |  22:05     | Method 4: Shortcut for Exams   | [x]           |  |
|  |  30:10     | Method 5: Back-substitution    | [x]           |  |
|  |  36:45     | Practice Problems              | [x]           |  |
|  |  41:00     | Summary & Key Takeaways        | [x]           |  |
|  |                                                             |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  [ Back ]  [ Save Draft ]  [ Submit for Review ]                  |
+------------------------------------------------------------------+
```

---

## Mockup 3 — Streaming Configuration & Video Library

```
+------------------------------------------------------------------+
| VIDEO CONTENT — My Library                         Dr. Venkat Rao |
+------------------------------------------------------------------+
|                                                                   |
|  +------------------------------------------------------------+  |
|  | ENCODING & STREAMING STATUS                                 |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  Video: HCF & LCM — Shortcut Methods                       |  |
|  |  Upload: Complete | Encoding: In Progress                   |  |
|  |                                                             |  |
|  |  Adaptive Bitrate Encoding (HLS):                           |  |
|  |  [x] 360p  (640x360,  800 kbps)    -- Done                 |  |
|  |  [x] 480p  (854x480,  1.5 Mbps)    -- Done                 |  |
|  |  [#] 720p  (1280x720, 3.0 Mbps)    -- Encoding (67%)       |  |
|  |  [ ] 1080p (1920x1080, 5.0 Mbps)   -- Queued               |  |
|  |                                                             |  |
|  |  Transcript: Generating... (ETA: 8 min)                     |  |
|  |  Thumbnail: Selected (Frame at 10:32)                       |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | MY VIDEO LIBRARY                               8 videos    |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  | Title                      | Duration | Status  | Views   |  |
|  |----------------------------|----------|---------|---------|  |
|  | HCF & LCM — Shortcuts      | 42:18    | Encoding| --      |  |
|  | Percentage — Fast Methods   | 38:45    | Approved| 3,412   |  |
|  | Profit & Loss — All Types   | 55:20    | Approved| 5,891   |  |
|  | Time & Work — 10 Tricks     | 47:10    | Approved| 4,227   |  |
|  | SI & CI — Quick Formulas    | 35:55    | Approved| 2,894   |  |
|  | Averages & Mixtures         | 40:30    |In Review| --      |  |
|  | Ratio & Proportion          | 33:15    | Approved| 1,956   |  |
|  | DI — Bar & Pie Charts       | 52:40    | Approved| 6,103   |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  +------------------------------------------------------------+  |
|  | VIDEO STATISTICS (All Approved)                              |  |
|  +------------------------------------------------------------+  |
|  |                                                             |  |
|  |  Total Videos:          7 approved, 1 encoding              |  |
|  |  Total Duration:        5h 3m 35s                           |  |
|  |  Total Views:           24,483                              |  |
|  |  Average Watch Time:    28m 14s (73% completion)            |  |
|  |  Average Rating:        4.5 / 5.0 (1,847 ratings)          |  |
|  |  Top Video:             DI — Bar & Pie Charts (6,103 views) |  |
|  +------------------------------------------------------------+  |
|                                                                   |
|  [ Upload New Video ]                                             |
+------------------------------------------------------------------+
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/content-partner/author/video-content` | List all videos for the logged-in partner |
| POST | `/api/v1/content-partner/author/video-content` | Initiate a new video upload (returns upload URL and video ID) |
| PUT | `/api/v1/content-partner/author/video-content/{id}/upload` | Upload video file via chunked/resumable upload |
| GET | `/api/v1/content-partner/author/video-content/{id}` | Retrieve video metadata and processing status |
| PUT | `/api/v1/content-partner/author/video-content/{id}` | Update video metadata (title, description, syllabus mapping) |
| DELETE | `/api/v1/content-partner/author/video-content/{id}` | Delete a draft or encoding video (cannot delete approved) |
| POST | `/api/v1/content-partner/author/video-content/{id}/submit` | Submit an encoded video for editorial review |
| POST | `/api/v1/content-partner/author/video-content/{id}/thumbnail` | Upload a custom thumbnail image |
| GET | `/api/v1/content-partner/author/video-content/{id}/thumbnails` | Get auto-generated thumbnail candidates |
| POST | `/api/v1/content-partner/author/video-content/{id}/transcript` | Upload a transcript file (SRT/VTT) or trigger auto-generation |
| GET | `/api/v1/content-partner/author/video-content/{id}/transcript` | Retrieve the generated or uploaded transcript |
| PUT | `/api/v1/content-partner/author/video-content/{id}/transcript` | Edit the auto-generated transcript |
| PUT | `/api/v1/content-partner/author/video-content/{id}/chapters` | Set or update chapter markers with timestamps |
| GET | `/api/v1/content-partner/author/video-content/{id}/encoding-status` | Get real-time adaptive bitrate encoding progress |
| GET | `/api/v1/content-partner/author/video-content/{id}/stats` | Get view, watch-time, and rating statistics |

---

## Business Rules

1. Video uploads use a chunked, resumable upload protocol (tus.io-compatible) to handle large files reliably over potentially unstable internet connections, which is especially important for partners in Tier-2 and Tier-3 cities like Visakhapatnam where broadband reliability can vary. The maximum file size is 2 GB and the maximum duration is 90 minutes; files exceeding either limit are rejected after the initial metadata extraction phase. Accepted container formats are MP4, MOV, AVI, and MKV, but the system strongly recommends H.264 or H.265 encoded MP4 files because these require the least transcoding overhead and produce the best quality-to-size ratio. Upon upload completion, the system extracts technical metadata (resolution, codec, bitrate, frame rate, audio channels) and displays it to the partner for verification. If the source video has a resolution below 720p or audio bitrate below 96 kbps, a quality warning is displayed recommending re-recording at higher quality settings, though the upload is not blocked because some partners may have hardware limitations that prevent higher-quality recording.

2. After a video is uploaded, the platform automatically triggers an adaptive bitrate encoding pipeline that produces four HLS (HTTP Live Streaming) variants: 360p at 800 kbps for mobile data-saver mode, 480p at 1.5 Mbps for standard mobile, 720p at 3.0 Mbps for tablets and laptops, and 1080p at 5.0 Mbps for desktop full-screen viewing. The encoding pipeline runs on dedicated GPU-accelerated workers (NVIDIA T4 instances) and typically completes within 1.5 times the video duration for a 1080p source. The partner can monitor encoding progress in real-time via the portal, and the system sends an in-app notification and optional email when all variants are ready. A video cannot be submitted for editorial review until encoding completes for at least the 360p and 720p variants, ensuring that students on both low-bandwidth and high-bandwidth connections can access the content. The encoded segments are stored on a CDN (CloudFront) with geo-distributed edge locations across India to minimize buffering for students in all states.

3. Transcript generation uses a speech-to-text pipeline powered by a fine-tuned Whisper model trained on Indian-accented English, Telugu, and Hindi academic lecture audio. The system achieves approximately 92 percent word-level accuracy for clearly spoken English lectures with minimal background noise, which is typical of Dr. Venkat Rao's home-studio recordings. After auto-generation, the transcript is presented to the partner in a synchronized editor where each text segment is linked to its timestamp, allowing the partner to play the corresponding audio segment and correct any transcription errors before finalizing. The finalized transcript serves three purposes: it generates SRT/VTT subtitle files for the video player, it is indexed for full-text search so students can find videos by spoken content (e.g., searching "remainder theorem shortcut" surfaces Dr. Venkat Rao's lecture at the exact timestamp where he discusses that topic), and it feeds into an automated translation pipeline that produces Telugu and Hindi subtitle tracks using neural machine translation with mathematical terminology preservation.

4. Chapter markers divide the video into navigable segments that appear as labeled sections in the student video player's progress bar, enabling students to jump directly to specific topics within a lecture. Partners can define chapter markers manually by entering timestamps and titles, or the system can suggest chapter boundaries by analyzing transcript content for topic transitions (detected via semantic shift in sentence embeddings). Each chapter marker can optionally be mapped to a specific syllabus sub-topic, which enables the platform to deep-link students directly to the relevant segment when they navigate from a syllabus topic page — for example, a student studying "LCM via HCF relationship" on the APPSC Maths topic page would see a link that opens Dr. Venkat Rao's video at 15:20 (Method 3: LCM via HCF) rather than at the beginning. Videos without chapter markers are still accepted but receive a lower discoverability score in search results because the platform cannot offer segment-level navigation or topic-specific deep linking, which reduces the content's utility for students who want to study specific sub-topics rather than watching entire lectures.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division B*
