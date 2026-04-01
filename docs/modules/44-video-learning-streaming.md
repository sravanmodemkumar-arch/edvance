# Module 44 — Video Learning & Streaming

## 1. Purpose

Video has become the primary medium for learning across all institution types in India — from a Class 6 teacher recording a lecture on their phone for rural students who miss class, to a Delhi coaching institute delivering structured IIT-JEE video series to 50,000 concurrent students. The two failure modes are equally damaging: over-engineered expensive platforms (Zoom+Vimeo+LMS glued together) that institutions cannot afford, and under-engineered uploads (YouTube links in WhatsApp groups) that have no access control, no progress tracking, and no analytics.

EduForge Module 44 is the institution-grade video learning system built on Cloudflare R2 + AWS MediaConvert, designed to deliver video at the Rs. 0.60/student/year cost target. It covers the full lifecycle: in-app recording and upload, multi-resolution HLS transcoding, AES-128 DRM + dynamic student watermarking, a feature-rich Flutter + web player, progress tracking, in-video notes/bookmarks/Q&A, subtitle generation via AWS Transcribe, content moderation, offline downloads with device binding, and teacher analytics showing second-by-second drop-off curves. Video discovery is tied to the syllabus hierarchy (Module 15) so every video has a curriculum address, not just a filename.

---

## 2. Content Taxonomy

### 2.1 Video Types

| Type | Created By | Typical Length | Access |
|---|---|---|---|
| Lecture recording | Teacher | 20–60 min | Class/batch |
| Tutorial / worked example | Teacher | 5–20 min | Class/batch |
| Lab demonstration | Teacher | 5–30 min | Class/batch |
| Animation / explainer | Admin / external | 2–10 min | Subject-wide |
| Short concept clip | Teacher | 1–3 min | Class/batch/public preview |
| Screen-share recording | Teacher | 10–60 min | Class/batch |
| Live class archive | System (Module 45) | Variable | Class/batch |
| Guest lecture | Admin | Variable | Institution-wide |
| Student project video | Student | 5–20 min | Teacher review only |
| Documentary clip (curated) | Admin | Variable | Subject-wide |

### 2.2 Publication States

```
UPLOADING → PROCESSING (transcoding) → REVIEW_PENDING (content check)
         → DRAFT (ready; teacher can preview)
         → SCHEDULED (publish at future date/time)
         → PUBLISHED (students can access)
         → ARCHIVED (hidden from students; retained for teacher access)
```

---

## 3. Storage Architecture

### 3.1 Cloudflare R2 Layout

```
videos/
  {tenant_id}/
    {video_uuid}/
      raw/
        original.{ext}              # original upload; retained 30 days post-transcode
      hls/
        master.m3u8                 # master manifest (all resolutions)
        360p/
          segment_000.ts
          segment_001.ts
          ...
          prog.m3u8
        480p/ ...
        720p/ ...
        1080p/ ...
      thumbnails/
        thumb_01.jpg ... thumb_10.jpg
        selected_thumb.jpg
      preview/
        animated_preview.mp4        # 4-second preview clip
      subtitles/
        en.vtt                      # English subtitles (auto or uploaded)
        hi.vtt                      # Hindi subtitles
      transcript/
        transcript.json             # AWS Transcribe full output
        transcript.vtt              # Timestamp-synced transcript VTT
      offline/
        {student_device_hash}/
          encrypted.mp4             # AES-256 encrypted offline package
          {session_token}.key       # Key file; bound to device fingerprint
```

Private bucket — all access via signed URLs.

### 3.2 Cost Architecture

| Cost Component | Rate | Estimated Monthly (100 hrs of video, 10,000 students) |
|---|---|---|
| R2 Storage (1 TB at 4 resolutions) | $0.015/GB/month | $15 |
| R2 Class A operations (upload/list) | $4.50 per million | $1 |
| MediaConvert transcoding (720p) | $0.0075/min | $45 |
| AWS Transcribe (Hindi+English) | $0.024/min | $144 (optional) |
| Rekognition moderation | $0.001/image × 10 frames | $0.50/video |
| Cloudflare CDN egress from R2 | **$0** | $0 (R2 → CDN zero egress) |
| **Total** | — | **~$205/month** |

At 10,000 students: **$0.02/student/month = ₹2/student/year** — within the cost target. Transcript can be disabled for basic tier.

---

## 4. Transcoding Pipeline

### 4.1 Pipeline Flow

```
Raw file arrives in R2
        ↓
SQS message: { video_id, tenant_id, r2_raw_path }
        ↓
Transcode Lambda triggered
        ↓
AWS MediaConvert job created (4 outputs in parallel):
  → 360p/40p/720p/1080p HLS
  → AES-128 key generated and stored in AWS KMS
  → Audio normalization (EBU R128)
  → Silence trimming (leading/trailing > 3s)
  → Black frame chapter detection
  → Thumbnail extraction (10 frames)
  → Animated preview clip (4 sec at 50% mark)
        ↓
MediaConvert completion event → Lambda webhook
        ↓
HLS segments → R2 (under /hls/)
        ↓
AWS Transcribe job kicked off (async)
        ↓
AWS Rekognition moderation frames scanned (async)
        ↓
DB: video.status = REVIEW_PENDING
        ↓
Content review queue notification → Institution reviewer
```

### 4.2 MediaConvert Job Template

```json
{
  "OutputGroups": [
    {
      "OutputGroupSettings": { "Type": "HLS_GROUP_SETTINGS",
        "HlsGroupSettings": { "SegmentLength": 6, "DirectoryStructure": "SINGLE_DIRECTORY",
          "Encryption": { "EncryptionMethod": "AES128", "StaticKeyProvider": {
            "KeyFormat": "identity", "Url": "https://api.eduforge.io/video-keys/{video_id}"
          }}
        }
      },
      "Outputs": [
        { "VideoDescription": { "Width": 1280, "Height": 720,
            "CodecSettings": { "Codec": "H_264", "H264Settings": { "Bitrate": 1500000 }}},
          "AudioDescriptions": [{ "AudioNormalizationSettings": {
            "Algorithm": "ITU_BS_1770_3", "TargetLkfs": -23 }}],
          "NameModifier": "_720p"
        },
        { "VideoDescription": { "Width": 854, "Height": 480, "CodecSettings": { ... }}, "NameModifier": "_480p" },
        { "VideoDescription": { "Width": 640, "Height": 360, "CodecSettings": { ... }}, "NameModifier": "_360p" }
      ]
    }
  ]
}
```

### 4.3 Chapter Detection

Black frame analysis during transcoding identifies natural scene breaks. Output:

```json
{ "suggested_chapters": [
    { "timestamp_seconds": 0, "label": "Introduction" },
    { "timestamp_seconds": 420, "label": "Chapter 2" },
    { "timestamp_seconds": 1140, "label": "Chapter 3" }
]}
```

Teacher reviews suggestions in the metadata editor → confirms or edits chapter titles → chapter markers saved in `video_chapters` table.

---

## 5. CDN Delivery & Signed URLs

### 5.1 Signed URL Architecture

```
Student requests video
        ↓
App calls: GET /api/v1/videos/{id}/play-url/
        ↓
API verifies: student enrolled in this video's subject/batch
        ↓
API generates signed URL:
  base_url = https://cdn.eduforge.io/videos/{tenant}/{video_uuid}/hls/master.m3u8
  token = HMAC-SHA256(video_id + student_id + session_id + expiry, SECRET)
  signed_url = base_url + ?token={token}&exp={expiry_unix}
        ↓
Cloudflare Worker at CDN edge validates token + enrollment on every request
        ↓
Segments served from Cloudflare R2 via CDN (cached)
```

### 5.2 HLS Key Delivery

For AES-128 encrypted segments:

```
Player fetches key URI from HLS manifest:
  #EXT-X-KEY:METHOD=AES-128,URI="https://api.eduforge.io/video-keys/{video_id}"

Key endpoint:
  GET /api/v1/video-keys/{video_id}/
  Authorization: Bearer {session_token}
  → Returns 16-byte AES key ONLY for enrolled, authenticated student
  → Key response cached for 2 hours (matches signed URL expiry)
```

### 5.3 Cloudflare Worker Token Validation

```javascript
// Cloudflare Worker — runs at edge for every video segment request
export default {
  async fetch(request, env) {
    const url = new URL(request.url)
    const token = url.searchParams.get('token')
    const exp = parseInt(url.searchParams.get('exp'))

    if (Date.now() / 1000 > exp) return new Response('URL expired', { status: 403 })

    const videoId = extractVideoId(url.pathname)
    const studentId = await validateToken(token, videoId, env.SIGNING_SECRET)
    if (!studentId) return new Response('Unauthorized', { status: 403 })

    // Check enrollment from KV cache (refreshed every 5 min from DB)
    const enrolled = await env.ENROLLMENT_KV.get(`${studentId}:${videoId}`)
    if (!enrolled) return new Response('Not enrolled', { status: 403 })

    return fetch(request) // pass through to R2 origin
  }
}
```

---

## 6. DRM & Content Protection

### 6.1 Dynamic Watermarking

Student's name and roll number watermarked on video at Cloudflare Worker level — injected as a text overlay in the video player response:

- Position: randomly alternates between 4 corners every 30 seconds
- Style: white text, 20% opacity, 12pt Roboto font
- If watermark is cropped out in recording → only one corner visible → still identifies student from watermark pattern

Watermark text: `{Student Name} | {Roll No} | {Date}`

### 6.2 Screen Recording Prevention

**Android:**
```dart
// Flutter — Android FLAG_SECURE
import 'package:flutter/services.dart';
class VideoPlayerScreen extends StatefulWidget {
  @override
  void initState() {
    super.initState();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    // Set FLAG_SECURE via platform channel
    platform.invokeMethod('setSecureFlag', true);
  }
}
```

**iOS:** AVFoundation's `allowsExternalPlayback` set to false in DRM mode; screen record triggers black screen.

**Detection:** `WidgetsBinding.instance.addObserver` + screenshot callback — on detection: video pauses, toast shown: "Screen recording detected — video paused for content protection."

### 6.3 Offline Download Package

```
Server-side offline packaging:
1. Fetch source HLS segments from R2 (720p for offline)
2. Decrypt segments (remove HLS key encryption)
3. Burn watermark into video frames (ffmpeg text filter)
4. Re-encrypt with AES-256 using device-specific key
5. Device-specific key = HMAC-SHA256(video_id + device_fingerprint, MASTER_SECRET)
6. Package: {video_id}_offline.mp4 + {token}.key
7. Upload to R2 under /offline/{device_hash}/ with 30-day expiry
8. Student downloads both files to app's private storage (inaccessible to other apps)
```

Device fingerprint: Android — `Build.FINGERPRINT` + KeyStore-backed attestation; iOS — `identifierForVendor` + Secure Enclave attestation.

---

## 7. Video Player

### 7.1 Feature Set

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│                   [VIDEO FRAME]                        │
│                                                        │
│  Arjun M | R-245 | 26 Mar 2026     ← watermark        │
│                                                        │
├────────────────────────────────────────────────────────┤
│ [◄10] [❙❙] [►10]  ══════●══════════════  12:34/45:20  │
│  Ch1        Ch2        Ch3          Ch4    ← chapters  │
├────────────────────────────────────────────────────────┤
│ [⚙️ 1×] [CC] [🔖] [📝] [Q&A] [⬇️] [⛶]  [🔊] [⛶Full]│
└────────────────────────────────────────────────────────┘
```

Controls:
- **◄10 / ►10**: 10-second skip (single tap); 30-second skip (double tap on video area)
- **❙❙ / ►**: Play/Pause
- **⚙️ 1×**: Speed selector (0.5× to 2×)
- **CC**: Caption toggle + language selector
- **🔖**: Bookmark current position
- **📝**: Add timestamp note
- **Q&A**: Open Q&A panel (questions at nearby timestamps shown)
- **⬇️**: Download for offline
- **🔊**: Volume + mute
- **⛶Full**: Fullscreen

### 7.2 Seek Bar Details

```
0:00                                               45:20
 ├──●──────────────┬──────────────┬──────────────────┤
 │ ▲ 12:34         │ Ch2          │ Ch3              │
 │                 │              │                  │
 │ chapter marker  │ bookmark     │ Q&A hotspot      │
 │ (teacher)       │ (student)    │ (speech bubble)  │
```

Hover (web): animated preview of that timestamp appears above seek bar.

### 7.3 Transcript View

Below the player on web; collapsible on mobile:

```
[00:00] Welcome to Chapter 5 — Electromagnetism.
[00:04] Today we'll cover Faraday's law and its applications.
[00:12] Let's start with the concept of magnetic flux...  ← clickable → jumps to 0:12
```

Clicking any line jumps the video to that timestamp. Full transcript is searchable (Ctrl+F on web).

---

## 8. In-Video Interactive Features

### 8.1 Timestamp Notes

```sql
CREATE TABLE video_notes (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id    UUID NOT NULL REFERENCES videos(id),
  student_id  UUID NOT NULL REFERENCES students(id),
  timestamp_s INT NOT NULL,           -- seconds from start
  note_text   TEXT NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT now(),
  updated_at  TIMESTAMPTZ DEFAULT now()
);
```

Notes are private to the student. Exportable as PDF: `{timestamp} — {note}` for all notes in a video.

### 8.2 Q&A on Video

```sql
CREATE TABLE video_qa (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id      UUID NOT NULL REFERENCES videos(id),
  asked_by_id   UUID NOT NULL REFERENCES users(id),
  timestamp_s   INT NOT NULL,
  question_text TEXT NOT NULL,
  is_resolved   BOOLEAN DEFAULT FALSE,
  created_at    TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE video_qa_replies (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  question_id UUID NOT NULL REFERENCES video_qa(id),
  replied_by_id UUID NOT NULL REFERENCES users(id),
  reply_text  TEXT NOT NULL,
  is_teacher  BOOLEAN DEFAULT FALSE,
  created_at  TIMESTAMPTZ DEFAULT now()
);
```

Q&A speech-bubble markers on seek bar. Teacher sees all unanswered questions across all their videos in a "Pending Q&A" dashboard.

### 8.3 Teacher Annotations

Teacher can mark specific timestamps with annotation type and text:
- ⭐ Important (exam-relevant)
- ⚠️ Common Mistake
- 💡 Key Insight
- 🔗 Reference (link to another video or topic)

Annotations appear as coloured markers on all students' seek bars.

### 8.4 Embedded Poll

Teacher inserts a poll (MCQ, 2–4 options) at a specific timestamp. When a student reaches that point:
- Video pauses automatically
- Poll appears as an overlay
- Student answers; sees aggregate result after submitting
- Teacher sees per-student responses in video analytics

### 8.5 Auto-Quiz (Chapter Comprehension)

Teacher inserts 1–3 MCQ questions at a timestamp. Video pauses; student answers. If incorrect: option to re-watch the preceding 2 minutes. If correct: video resumes. Skip option available (tracked — teacher can see who skipped).

---

## 9. Teacher Upload Flow

### 9.1 Mobile In-App Recording

1. Open camera from "Add Video" screen
2. Select recording mode: Front / Rear / Screen (screen mirror with device camera)
3. Record up to 30 minutes (longer → user prompted to upload from gallery)
4. Review clip before upload
5. Upload immediately to R2 via tus; progress bar

### 9.2 Web Desktop Upload

- Drag-and-drop area with file browser fallback
- tus resumable upload client — if internet drops, resumes from last byte on reconnect
- Progress: per-file upload percentage + estimated time
- Batch: multiple files upload simultaneously (max 5 parallel)

### 9.3 Screen + Webcam Recording (Web)

```javascript
// Dual stream: screen share + webcam
const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true })
const cameraStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })

// Canvas compositing: screen on left, camera in bottom-right corner (PiP)
// MediaRecorder → WebM → upload via tus
```

### 9.4 Metadata Form

After upload / recording:

```
Title:         [Chapter 5 — Faraday's Law — Part 1]
Description:   [Covers magnetic flux, EMF, and applications to AC generators]
Subject:       [Physics ▾] → Chapter: [Electromagnetism ▾] → Topic: [Faraday's Law ▾]
Class / Batch: [Class XII-A ▾] (multi-select for multiple classes)
Tags:          [faraday, EMF, AC generator, flux]
Access Level:  ● Class-wide  ○ Specific batch  ○ All enrolled students  ○ Public preview
Publish:       ● Now  ○ Schedule: [date/time picker]
[Save as Draft]   [Submit for Review]
```

---

## 10. Content Moderation

### 10.1 Automated Screening

AWS Rekognition `DetectModerationLabels` called on 10 evenly-spaced keyframes (every 10% of video duration):

| Category | Action |
|---|---|
| Explicit nudity (confidence > 80%) | Block + CRITICAL alert to Super Admin |
| Suggestive content (confidence > 70%) | Route to human reviewer |
| Violence (confidence > 70%) | Route to human reviewer |
| Hate symbols (confidence > 60%) | Block + alert |
| Drug / tobacco reference | Route to human reviewer |

### 10.2 Human Review Queue

Institution admin or designated content reviewer:
- Sees video thumbnail + flagged timestamps
- Jumps to flagged sections (player auto-seeks to flagged timestamps)
- Decision: Approve / Reject (reason required) / Request Edit
- On rejection: teacher notified with timestamp and reason
- On approval: video moves to PUBLISHED (or stays DRAFT for teacher to schedule)

### 10.3 Trust Tiers

| Institution Trust Level | Review Policy |
|---|---|
| New (< 6 months on platform) | All videos reviewed before publish |
| Standard | Spot-check (20% reviewed); rest auto-publish with post-publish scan |
| Trusted (verified, > 2 years) | Auto-publish; Rekognition scan in background; human review only on flag |

---

## 11. Subtitle & Transcript System

### 11.1 AWS Transcribe Integration

After transcoding:
```python
transcribe_client.start_transcription_job(
    TranscriptionJobName=f"video-{video_id}",
    Media={'MediaFileUri': f"s3://r2-equivalent/{tenant}/{video_uuid}/raw/original.mp4"},
    MediaFormat='mp4',
    LanguageCode='hi-IN',           # Primary language
    OutputBucketName='...',
    Settings={
        'ShowSpeakerLabels': True,
        'MaxSpeakerLabels': 3,
        'ShowAlternatives': True
    }
)
```

Output: JSON with word-level timestamps → converted to WebVTT by a Lambda.

### 11.2 Subtitle Quality

| Audio Quality | Expected Transcribe Accuracy |
|---|---|
| Clear professional mic, English | 90–95% |
| Clear mic, Hindi standard | 85–90% |
| Mobile phone mic, Hinglish mix | 70–80% |
| Multiple speakers, noisy | 60–70% |

Teacher can download auto-generated VTT, edit in any text editor, re-upload. Corrected VTT replaces auto-generated.

### 11.3 Multi-Language Subtitles

Teacher uploads subtitle files for regional languages (Telugu, Tamil, Kannada, etc.). System stores all in R2 under `/subtitles/{language_code}.vtt`. Player shows language selector when multiple tracks available.

---

## 12. Access Control Matrix

### 12.1 Video Access Rules

```python
def can_student_access_video(student_id, video_id):
    video = get_video(video_id)

    # 1. Enrollment check
    if not is_enrolled(student_id, video.subject_id):
        return False, "NOT_ENROLLED"

    # 2. Class/batch gate
    if video.class_id and student.class_id != video.class_id:
        return False, "WRONG_CLASS"

    # 3. Time gate
    if video.available_from and now() < video.available_from:
        return False, "NOT_YET_AVAILABLE"

    # 4. Expiry gate
    if video.expires_at and now() > video.expires_at:
        return False, "EXPIRED"

    # 5. Payment gate (coaching)
    if video.requires_payment and not has_paid(student_id, video.course_id):
        return False, "PAYMENT_REQUIRED"

    # 6. Publication state
    if video.status != 'PUBLISHED':
        return False, "NOT_PUBLISHED"

    return True, "ALLOWED"
```

Free preview: first N minutes always allowed regardless of enrollment (served via a different CDN path without student-bound token).

---

## 13. Progress Tracking & Completion

### 13.1 Progress Schema

```sql
CREATE TABLE video_progress (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id    UUID NOT NULL REFERENCES students(id),
  video_id      UUID NOT NULL REFERENCES videos(id),
  position_s    INT NOT NULL DEFAULT 0,         -- last resume position
  watched_s     INT NOT NULL DEFAULT 0,          -- unique seconds watched
  total_s       INT NOT NULL,                    -- video duration
  watch_pct     NUMERIC GENERATED ALWAYS AS (
                  ROUND(watched_s::NUMERIC / total_s * 100, 1)
                ) STORED,
  is_watched    BOOLEAN DEFAULT FALSE,           -- true when watch_pct >= 80%
  last_session_at TIMESTAMPTZ,
  session_count INT DEFAULT 0,
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now(),
  UNIQUE (student_id, video_id)
);

CREATE INDEX idx_progress_student ON video_progress(student_id);
CREATE INDEX idx_progress_video ON video_progress(video_id);
```

### 13.2 Unique Second Tracking

The app sends playback events every 10 seconds with the current timestamp range played (`from_s`, `to_s`). Server merges these into a sorted set of watched intervals and computes union (no double-counting of rewatched segments).

```python
def merge_intervals(intervals):
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    for start, end in sorted_intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return sum(end - start for start, end in merged)
```

---

## 14. Teacher Analytics Dashboard

### 14.1 Drop-Off Curve

```
Viewers vs. Time — "Faraday's Law Part 1" (45:20)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

120 ┤████████████████████████████████████████░░░░░░
 90 ┤████████████████████████████████████░░░░░░░░░░
 60 ┤██████████████████████████████░░░░░░░░░░░░░░░░
 30 ┤██████████████████████░░░░░░░░░░░░░░░░░░░░░░░░
  0 ┼──────────────────────────────────────────────
    0:00   10:00   20:00   30:00   40:00   45:20

Drop at 22:00: 38 students left here
→ This is where you introduce the integral formula
→ Consider splitting this into a separate video
```

### 14.2 Engagement Heatmap

Seek bar coloured red-yellow-green where:
- Red = most-replayed segment (students rewatch this)
- Yellow = moderately replayed
- Green = watched once

Teacher interprets: high rewatch = either very important OR very confusing. Combine with Q&A data.

### 14.3 Class Completion Matrix

```
Chapter 5 — Video Completion Matrix
         V1  V2  V3  V4  V5
Arjun    ██  ██  ██  █░  ░░   78%
Priya    ██  ██  ██  ██  ██  100%
Rahul    ██  ░░  ░░  ░░  ░░   20%  ← at-risk
Sneha    ██  ██  ██  ██  ░░   80%
...

Legend: ██ = watched (>80%)  █░ = partial  ░░ = not started
```

Teacher can click Rahul's row → see detailed watch history → initiate counsellor flag (Module 32).

---

## 15. Database Schema

```sql
CREATE TABLE videos (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id         UUID NOT NULL REFERENCES tenants(id),
  title             TEXT NOT NULL,
  description       TEXT,
  video_type        TEXT NOT NULL DEFAULT 'lecture',
  status            TEXT NOT NULL DEFAULT 'UPLOADING',
  subject_id        UUID REFERENCES subjects(id),
  chapter_id        UUID REFERENCES chapters(id),
  topic_id          UUID REFERENCES topics(id),
  class_id          UUID REFERENCES classes(id),
  batch_id          UUID REFERENCES batches(id),
  duration_s        INT,
  r2_raw_path       TEXT,
  r2_hls_path       TEXT,       -- base path for HLS segments
  thumbnail_r2_path TEXT,
  preview_r2_path   TEXT,
  has_transcript    BOOLEAN DEFAULT FALSE,
  has_subtitles     BOOLEAN DEFAULT FALSE,
  subtitle_languages TEXT[],
  max_resolution    TEXT DEFAULT '720p',
  requires_drm      BOOLEAN DEFAULT TRUE,
  access_level      TEXT DEFAULT 'class',
  available_from    TIMESTAMPTZ,
  expires_at        TIMESTAMPTZ,
  requires_payment  BOOLEAN DEFAULT FALSE,
  free_preview_s    INT DEFAULT 300,    -- first N seconds as free preview
  tags              TEXT[],
  view_count        INT DEFAULT 0,
  uploaded_by_id    UUID REFERENCES staff(id),
  moderation_status TEXT DEFAULT 'PENDING',
  published_at      TIMESTAMPTZ,
  created_at        TIMESTAMPTZ DEFAULT now(),
  updated_at        TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_videos_tenant ON videos(tenant_id);
CREATE INDEX idx_videos_subject ON videos(subject_id);
CREATE INDEX idx_videos_status ON videos(status);
CREATE INDEX idx_videos_published ON videos(published_at);

CREATE TABLE video_chapters (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id    UUID NOT NULL REFERENCES videos(id),
  timestamp_s INT NOT NULL,
  title       TEXT NOT NULL,
  sort_order  INT NOT NULL
);

CREATE TABLE video_offline_packages (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id        UUID NOT NULL REFERENCES videos(id),
  student_id      UUID NOT NULL REFERENCES students(id),
  device_hash     TEXT NOT NULL,
  r2_package_path TEXT NOT NULL,
  r2_key_path     TEXT NOT NULL,
  expires_at      TIMESTAMPTZ NOT NULL,
  downloaded_at   TIMESTAMPTZ DEFAULT now(),
  UNIQUE (video_id, student_id, device_hash)
);

CREATE TABLE video_annotations (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id    UUID NOT NULL REFERENCES videos(id),
  teacher_id  UUID NOT NULL REFERENCES staff(id),
  timestamp_s INT NOT NULL,
  type        TEXT NOT NULL,    -- important / mistake / insight / reference
  text        TEXT NOT NULL,
  visible     BOOLEAN DEFAULT TRUE
);

CREATE TABLE video_polls (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id    UUID NOT NULL REFERENCES videos(id),
  timestamp_s INT NOT NULL,
  question    TEXT NOT NULL,
  options     JSONB NOT NULL,   -- [{"id": "A", "text": "..."}, ...]
  correct_option TEXT,
  is_skippable BOOLEAN DEFAULT FALSE
);

CREATE TABLE video_poll_responses (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  poll_id     UUID NOT NULL REFERENCES video_polls(id),
  student_id  UUID NOT NULL REFERENCES students(id),
  selected    TEXT NOT NULL,
  responded_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (poll_id, student_id)
);
```

---

## 16. API Reference

```
# Video management
POST   /api/v1/videos/upload-url/               # Get tus upload URL (resumable)
POST   /api/v1/videos/                          # Create video record (post-upload)
GET    /api/v1/videos/{id}/                     # Video metadata
PATCH  /api/v1/videos/{id}/                     # Edit metadata
DELETE /api/v1/videos/{id}/                     # Archive video
GET    /api/v1/videos/{id}/play-url/            # Get signed HLS URL + key URL
POST   /api/v1/videos/{id}/publish/             # Publish video

# Progress
PUT    /api/v1/videos/{id}/progress/            # Update watch progress (every 10s)
GET    /api/v1/videos/{id}/progress/            # Get resume position

# Notes & bookmarks
POST   /api/v1/videos/{id}/notes/               # Add timestamp note
GET    /api/v1/videos/{id}/notes/               # List notes
DELETE /api/v1/videos/{id}/notes/{note_id}/     # Delete note
POST   /api/v1/videos/{id}/bookmarks/           # Add bookmark
GET    /api/v1/videos/{id}/bookmarks/           # List bookmarks

# Q&A
POST   /api/v1/videos/{id}/qa/                  # Post question
GET    /api/v1/videos/{id}/qa/                  # List Q&A threads
POST   /api/v1/videos/{id}/qa/{q_id}/replies/   # Reply to question

# Offline
POST   /api/v1/videos/{id}/offline-download/    # Request offline package
GET    /api/v1/videos/{id}/offline-key/         # Get decryption key (device-bound)

# Teacher analytics
GET    /api/v1/videos/{id}/analytics/           # Full video analytics
GET    /api/v1/videos/{id}/dropoff-curve/       # Second-by-second viewer count
GET    /api/v1/videos/{id}/completion-matrix/   # Per-student completion

# Content review
GET    /api/v1/admin/content-review-queue/      # Pending review queue
PATCH  /api/v1/admin/content-review/{id}/approve/  # Approve
PATCH  /api/v1/admin/content-review/{id}/reject/   # Reject with reason

# Video key endpoint (secure; auth required)
GET    /api/v1/video-keys/{video_id}/           # AES-128 HLS decryption key
```

---

## 17. RBAC Matrix

| Action | Student | Teacher | Content Reviewer | Admin | Super Admin |
|---|---|---|---|---|---|
| Watch enrolled videos | ✅ | ✅ | ✅ | ✅ | ✅ |
| Watch free preview | ✅ (unenrolled) | ✅ | ✅ | ✅ | ✅ |
| Add notes/bookmarks | ✅ | ✅ | ❌ | ❌ | ❌ |
| Post Q&A question | ✅ | ✅ | ❌ | ❌ | ❌ |
| Reply to Q&A | ✅ (peers) | ✅ | ❌ | ❌ | ❌ |
| Download offline | ✅ | ✅ | ❌ | ❌ | ❌ |
| Upload video | ❌ | ✅ (own subjects) | ❌ | ✅ | ✅ |
| Publish video | ❌ | ✅ (if trusted tier) | ✅ | ✅ | ✅ |
| Review content queue | ❌ | ❌ | ✅ | ✅ | ✅ |
| View video analytics | ❌ | ✅ (own videos) | ❌ | ✅ | ✅ |
| View student watch data | ❌ | ✅ (own class) | ❌ | ✅ | ✅ |
| Delete/archive video | ❌ | ✅ (own, unpublished) | ❌ | ✅ | ✅ |

---

## 18. Cross-Module Integration Map

| Module | Integration |
|---|---|
| Module 10 — Timetable | Scheduled video lessons appear in student timetable as video-type events |
| Module 14 — Homework | Teacher assigns video as homework with watch-by date; completion tracked |
| Module 15 — Syllabus | Videos tagged to syllabus topics; topic view shows linked video count |
| Module 22 — Test Series (Coaching) | Batch-gated video library; video access tied to coaching batch enrollment |
| Module 32 — Student Welfare | Teacher can flag low-completion student to counsellor from completion matrix |
| Module 39 — Certificates | Course completion certificate triggered on full video course completion (all required videos watched) |
| Module 45 — Live Classes | Live class recordings auto-archived into this module post-session |
| Module 46 — AI Doubt Solver | Doubt submitted from a video timestamp; AI references video transcript for answer |
| Module 47 — AI Performance Analytics | Video watch % and streak as engagement signals in performance model |
| Module 48 — AI Content Generation | AI generates lecture scripts from syllabus; teacher records against script |
| Module 50 — Subscription | Video library access, max resolution, and download quota controlled by subscription tier |
| Module 53 — Platform Analytics | Institution-wide video engagement stats; completion rates by subject |

---

*Module 44 — Video Learning & Streaming — EduForge Platform Specification*
*Version 1.0 | 2026-03-26*
