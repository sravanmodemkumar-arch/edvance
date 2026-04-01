# Module 45 — Live Classes

## 1. Purpose

Live online classes have become the primary mode of instruction for coaching institutes, the supplementary mode for schools during disruptions, and the default for distance-learning colleges. The failure mode of most institutions is using a consumer video call tool (Google Meet, Zoom) with no integration to their student management system — no automatic enrollment-gated access, no attendance tracking, no recording archival to the course library, no engagement analytics, no low-bandwidth adaptation for rural students.

EduForge Module 45 is the institution-native live class system built on Agora.io's SD-RTN for real-time communication. It supports interactive classes (≤ 200 participants with full two-way video/audio), doubt sessions (≤ 30 with student screen-share), and large webinars (200–10,000 via HLS broadcast path). Every class is enrollment-gated, attendance is auto-tracked with configurable thresholds, recordings are auto-archived to Module 44 (Video Library), whiteboard sessions save to Module 16 (Notes), in-class quizzes feed Module 21 (Results), and engagement scores feed Module 32 (Student Welfare EWS). India-specific: low-bandwidth mode (360p/3G) and audio-only mode (2G) are first-class features, not afterthoughts.

---

## 2. Class Type Matrix

| Mode | Max Participants | Student A/V | Key Features | Infrastructure |
|---|---|---|---|---|
| Interactive Class | 200 | Bidirectional (teacher-controlled) | Hand-raise, screen share, breakout rooms, whiteboard | Agora SFU |
| Doubt Session | 30 | Full bidirectional | Student screen share, teacher annotation on student screen | Agora SFU |
| Lab Session | 100 | Student audio only | Teacher screen share + simulation, annotation | Agora SFU |
| Group Discussion | 100 | Full in breakout rooms | Pre-configured groups, breakout rooms | Agora SFU |
| Webinar | 10,000 | Teacher only | HLS audience stream, moderated Q&A, hand-raise queue | Agora + Cloudflare HLS |
| Parent Orientation | 5,000 | Teacher only | Formal, moderated, institutional branding | Agora + Cloudflare HLS |
| Guest Lecture | 5,000 | Speaker + co-host | External speaker join, moderated student Q&A | Agora + Cloudflare HLS |

---

## 3. RTC Infrastructure

### 3.1 Agora.io SD-RTN

**Why Agora:**
- India data centre nodes (Mumbai, Chennai) — latency < 300ms for India-to-India
- SFU architecture — server forwards streams without re-encoding; lower latency, lower server cost than MCU
- Simulcast support — teacher sends 240p/480p/720p; Agora sends appropriate quality per student
- Agora Cloud Recording — direct-to-S3 recording without running separate recording servers
- India-wide CDN coverage — manages TURN/STUN globally; handles restrictive NAT/firewalls in school/college networks

**Cost Optimisation:**
| Quality | Cost per 1000 min | At 30 students, 1hr class |
|---|---|---|
| HD Video (720p) | $0.042 | $0.076/class |
| SD Video (480p, default) | $0.018 | $0.032/class |
| Audio only | $0.0099 | $0.018/class |

Default session quality: **480p** — saves 57% vs HD with negligible quality difference on mobile screens.

### 3.2 Session Token Architecture

```python
# FastAPI — generate Agora token (RTC Token Builder)
from agora_token_builder import RtcTokenBuilder, Role_Publisher, Role_Subscriber

def generate_student_token(session_id: str, student_uid: int) -> str:
    token = RtcTokenBuilder.buildTokenWithUid(
        app_id=settings.AGORA_APP_ID,
        app_certificate=settings.AGORA_APP_CERT,
        channel_name=session_id,
        uid=student_uid,
        role=Role_Subscriber,      # students are subscribers
        privilege_expired_ts=int(time.time()) + 7200  # 2-hour token
    )
    return token

def generate_teacher_token(session_id: str, teacher_uid: int) -> str:
    return RtcTokenBuilder.buildTokenWithUid(..., role=Role_Publisher, ...)
```

Student UID: `hash(student_id, session_id) % 100000` — deterministic, session-scoped, non-reversible to student_id.

Token issued only after:
1. Student is enrolled in the session's subject/batch
2. Session status is LIVE or IN_LOBBY (not ENDED)
3. Student is not kicked from this session

### 3.3 Webinar Mode HLS Path

For sessions with > 200 expected attendees:

```
Teacher (Agora Publisher)
        ↓
Agora RTMP Push → Cloudflare Stream / Custom HLS origin
        ↓
HLS transcode: 360p / 480p / 720p manifests
        ↓
Cloudflare CDN edge caching
        ↓
Student browser / app fetches HLS stream (10–20s delay)
```

Real-time interactions (Q&A, polls, hand-raise) go via WebSocket (not Agora) — low-latency even for CDN audience.

---

## 4. Scheduling

### 4.1 Creating a Live Class

From Module 10 (Timetable) or directly:

```
Schedule Live Class
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:          [Chapter 5 — Live Revision]
Subject:        [Physics ▾]
Class / Batch:  [XII-A ▾]  [XII-B ▾]  (multi-select)
Date:           [26 Mar 2026]
Start Time:     [10:00 AM]
Duration:       [60 minutes ▾]
Mode:           ● Interactive  ○ Webinar  ○ Doubt Session
Auto-record:    ✅
Co-host:        [+ Add co-host]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Schedule Class]   [Start Now]
```

### 4.2 Recurring Classes

Timetable slot → all future class instances auto-created:
- Regular weekly class → 40 sessions created for the term
- Each instance can be individually cancelled/postponed
- Instance-level rescheduling: "Postpone this occurrence only" or "All future occurrences"

### 4.3 Postponement & Cancellation

**Postpone:**
1. Teacher selects class → "Postpone" → new date/time
2. System: updates class record, sends push + SMS to all enrolled students and parents
3. Calendar invite updated (ICS file emailed)

**Cancel:**
1. Teacher → "Cancel" → reason (optional)
2. Push + SMS to all students: "[Class Name] scheduled for [time] has been cancelled"
3. Timetable slot freed

---

## 5. Pre-Class Setup

### 5.1 Teacher Pre-Class Checklist

Shown 10 minutes before class:

```
Pre-Class Checklist                    ← 10 min to class
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Camera working (preview shown)
✅ Microphone working (level indicator)
⬜ Whiteboard initialized
⬜ Materials shared (click to attach)
⬜ Poll prepared (click to create)
⬜ Breakout rooms configured

[Open Lobby]   [Start Class]
```

### 5.2 Lobby (Waiting Room)

Teacher opens lobby 10 minutes before start:
- Students can enter lobby and wait
- Teacher sees student list: "Arjun M (12:34:01), Priya S (12:35:47)..."
- Teacher can chat with students in lobby (text only)
- Teacher chooses: "Admit All" or individual admits
- Students in lobby see: "Your teacher will let you in soon — [X] students waiting"

### 5.3 Co-Host Invitation

- Teacher adds co-host by email/name — searches staff directory
- Co-host receives push + email: "You've been added as co-host for [Class] — Join Link: [link]"
- Co-host has same controls as teacher (mute/unmute, whiteboard, kick); cannot end the session

---

## 6. In-Class Controls

### 6.1 Teacher Control Panel

```
┌─────────────────────────────────────────────────────────────┐
│ Physics — Chapter 5 Revision    🔴 Recording  ⏱ 23:45      │
├────────────────────┬────────────────────────────────────────┤
│ 👥 32/35 joined   │                                         │
│                    │          [VIDEO AREA]                   │
│ 🙋 Hand queue (3) │                                         │
│ ▸ Arjun Mehta     │  Teacher Video (large)                  │
│ ▸ Priya Sharma    │                                         │
│ ▸ Rahul K.        │  [Student Grid: 6 thumbnails + ⊕ more] │
│                    │                                         │
│ 💬 Chat (12 msgs) │                                         │
├────────────────────┴────────────────────────────────────────┤
│ [🔇 Mute All] [📷 Disable Video] [📊 Poll] [📋 Quiz]       │
│ [🏠 Breakout] [📌 Spotlight] [🔒 Lock] [⏹ End]            │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Hand-Raise Management

```
Hand Queue
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Arjun Mehta    [Unmute] [Spotlight] [Dismiss]
2. Priya Sharma   [Unmute] [Spotlight] [Dismiss]
3. Rahul K.       [Unmute] [Spotlight] [Dismiss]
                  [Dismiss All]
```

When teacher clicks "Unmute" for Arjun: Agora API promotes Arjun from subscriber to publisher for that session; Arjun hears "You can speak now."

### 6.3 Student Panel

```
[🙋 Raise Hand] [😊 React] [💬 Chat] [📷 Camera] [🎤 Mic] [📶 Network]

Network quality: 🟢 Good (all streams at 480p)
[Switch to audio-only] (saves data)
```

Reactions visible to all for 5 seconds; name shown with reaction.

---

## 7. Attendance System

### 7.1 Event Tracking

Every join/leave event logged:

```sql
CREATE TABLE live_session_events (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id  UUID NOT NULL REFERENCES live_sessions(id),
  student_id  UUID NOT NULL REFERENCES students(id),
  event_type  TEXT NOT NULL,    -- JOIN / LEAVE / NETWORK_DROP / RECONNECT
  event_time  TIMESTAMPTZ NOT NULL DEFAULT now(),
  source      TEXT              -- agora_webhook / manual
);
```

Agora webhook fires on user join/leave events in real-time.

### 7.2 Attendance Computation

Run at session end (or on-demand by teacher):

```python
def compute_attendance(session_id: str, student_id: str) -> AttendanceStatus:
    events = get_events(session_id, student_id)  # sorted by time
    session = get_session(session_id)
    total_s = (session.ended_at - session.started_at).total_seconds()

    # Build intervals: [join → leave], [join → leave]...
    intervals = build_intervals(events, session.ended_at)
    time_in_s = sum_intervals(intervals)  # unique seconds (no overlap)
    first_join = min(e.event_time for e in events if e.event_type == 'JOIN')

    coverage = time_in_s / total_s
    late = (first_join - session.started_at).total_seconds() > 600  # 10 min

    if coverage >= session.attendance_threshold:   # default 0.60
        return 'LATE' if late else 'PRESENT'
    return 'ABSENT'
```

### 7.3 Threshold Configuration

| Setting | Default | Range |
|---|---|---|
| Minimum presence for PRESENT | 60% | 40–90% |
| Late join threshold | 10 minutes | 5–20 min |
| Early leave threshold | 10 minutes before end | 5–20 min |
| Network drop grace period | 3 minutes | 1–5 min |

### 7.4 Manual Override

```
Post-Class Attendance Review
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Student         Status    Duration  Override  Reason
─────────────────────────────────────────────────────────
Arjun Mehta     PRESENT   58/60m    —         —
Priya Sharma    LATE      54/60m    PRESENT ▾  [Network issue]
Rahul K.        ABSENT     8/60m    PRESENT ▾  [Power outage confirmed]
Sneha P.        PRESENT   60/60m    —         —
```

Override reason stored; logged in audit trail.

---

## 8. Recording

### 8.1 Agora Cloud Recording

```python
# Start composite recording
recording_client.start(
    channel=session_id,
    uid=0,  # server-side recording bot UID
    client_request={
        "recordingConfig": {
            "streamTypes": 2,      # audio + video
            "decryptionMode": 0,
            "audioProfile": 2,
            "videoStreamType": 0,  # HD
            "channelType": 1,      # communication mode
        },
        "storageConfig": {
            "vendor": 1,           # AWS S3
            "region": 14,          # ap-south-1
            "bucket": settings.RECORDING_BUCKET,
            "accessKey": ...,
            "secretKey": ...
        },
        "transcodeOptions": {
            "container": {"format": "mp4"},
            "transCodeVideo": {
                "fps": 15,
                "width": 1280, "height": 720,
                "layoutConfig": [
                    # Teacher: 70% width, full height, left
                    {"uid": teacher_uid, "x_axis": 0.0, "y_axis": 0.0, "width": 0.7, "height": 1.0, "zOrder": 1},
                    # Student grid: 30% width, right
                    # Dynamic based on active speakers
                ]
            }
        }
    }
)
```

### 8.2 Post-Session Pipeline

```
Session ends → Agora Cloud Recording uploads MP4 to S3
                      ↓
           Lambda triggered by S3 event
                      ↓
       Transfer MP4 from S3 to R2 (via pre-signed URL)
                      ↓
       Module 44 transcoding pipeline started
       (MediaConvert → HLS segments → R2)
                      ↓
       Video record created in videos table
       status = PROCESSING → PUBLISHED (auto, no review for recordings)
                      ↓
       Enrolled students notified (push + email):
       "Recording of [Class Name] is available"
```

Processing time: typically 30–60 minutes post-session.

### 8.3 Recording Access

Same enrollment gate as live session. Teacher can see per-student recording view stats in Module 44 analytics.

---

## 9. Whiteboard

### 9.1 Technology Stack

- Canvas: Konva.js (web) / Flutter CustomPainter (mobile)
- Real-time sync: Agora RTM (Real-Time Messaging) channel — low latency (< 100ms) operation broadcast
- Operations: JSON events `{type, tool, data, user_id, timestamp}`
- Conflict resolution: last-write-wins with vector clock (simple; concurrent edits on same object accepted)

### 9.2 Tools

| Tool | Shortcut (web) | Notes |
|---|---|---|
| Pen | P | Pressure-sensitive on tablet |
| Shapes | S | Rectangle, circle, triangle, line, arrow |
| Text | T | Font size, bold, italic |
| Eraser | E | Erases individual strokes |
| Selection | V | Move, resize, rotate elements |
| Laser pointer | L | Temporary red dot; not persistent |
| Math equation | M | LaTeX input → rendered equation |
| Graph plotter | G | f(x) plotter; Desmos-style |

### 9.3 Auto-Save to Notes

At session end, whiteboard state exported as PDF:
```python
# Server-side: render final whiteboard state
canvas_json = get_whiteboard_state(session_id)
pdf_bytes = render_canvas_to_pdf(canvas_json)
# Save to Module 16 (Notes & Study Material)
create_study_material(
    tenant_id=session.tenant_id,
    title=f"Whiteboard — {session.title} — {session.date}",
    subject_id=session.subject_id,
    class_id=session.class_id,
    content_type="PDF",
    r2_path=upload_to_r2(pdf_bytes)
)
# Notify students
send_push("Whiteboard from today's class is saved in Notes")
```

---

## 10. Polls & Quizzes

### 10.1 Poll Flow

```
Teacher clicks [📊 Poll] → selects pre-prepared or creates live
        ↓
Poll pushed to all participants via Agora RTM
        ↓
Participants see overlay: MCQ options
        ↓
Responses collected; bar chart updates in real-time
        ↓
Teacher closes poll; optionally shares results to participants
        ↓
Poll responses stored in DB; teacher views per-student answers in analytics
```

### 10.2 Quiz (Scored)

Teacher marks a poll as "Quiz" and enters correct answer. After all respond or timer expires:
- Each student sees: "✅ Correct! / ❌ Incorrect — Answer: [B]"
- Score recorded: +1 for correct, 0 for incorrect, -0.5 for skip (configurable)
- All quiz scores for a session → optionally fed to Module 21 as a classwork record

### 10.3 Schema

```sql
CREATE TABLE session_polls (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id  UUID NOT NULL REFERENCES live_sessions(id),
  question    TEXT NOT NULL,
  options     JSONB NOT NULL,         -- [{"id": "A", "text": "Newton"}, ...]
  correct_opt TEXT,                   -- null for opinion polls
  poll_type   TEXT DEFAULT 'poll',   -- poll / quiz / word_cloud / pulse
  started_at  TIMESTAMPTZ,
  ended_at    TIMESTAMPTZ
);

CREATE TABLE session_poll_responses (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  poll_id     UUID NOT NULL REFERENCES session_polls(id),
  student_id  UUID NOT NULL REFERENCES students(id),
  response    TEXT NOT NULL,
  response_ms INT,                    -- milliseconds to respond
  created_at  TIMESTAMPTZ DEFAULT now(),
  UNIQUE (poll_id, student_id)
);
```

---

## 11. Breakout Rooms

### 11.1 Configuration

```
Breakout Rooms Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rooms:  [5] ← 30 students ÷ 5 = 6 per room

Assignment: ● Auto (random)  ○ Manual

Room 1: Arjun M, Priya S, Rahul K, ...
Room 2: Sneha P, Aditya R, ...
...

Timer: [15] minutes

[Open Rooms]
```

### 11.2 Breakout Room Controls

During breakout:
- Teacher main view shows: list of rooms, participants in each, timer countdown
- Teacher clicks room name → joins that room (students see "Teacher joined")
- Broadcast message: text sent to all rooms simultaneously
- "5 minutes remaining" broadcast auto-sent at 5 min

### 11.3 Bring Back

"End Breakout Rooms" button:
- All students get 10-second countdown: "Returning to main room in 10..."
- All students moved to main room automatically
- Whiteboard per room saved automatically before moving

---

## 12. Webinar Mode

### 12.1 Audience Experience

Students join via CDN stream (HLS):
- App fetches HLS manifest from Cloudflare CDN
- Adaptive quality: 720p / 480p / 360p based on bandwidth
- 10–20 second delay from teacher's live stream
- Video controls: quality selector, mute, fullscreen

### 12.2 Interaction Channels

| Channel | Mechanism | Latency |
|---|---|---|
| Chat Q&A | WebSocket → moderator screen | < 1 second |
| Poll | WebSocket push + response | < 1 second |
| Hand-raise | WebSocket → queue → Agora token grant | 5–10 seconds to speak |
| Reactions | WebSocket broadcast | < 1 second |

### 12.3 Moderation Flow

```
Student types question in chat
        ↓
Moderator (co-host) sees all questions
        ↓
Moderator marks question as "Show to Teacher"
        ↓
Question appears in teacher's Q&A panel
        ↓
Teacher reads/answers; response sent to all via chat + screen
```

---

## 13. Low-Bandwidth Adaptation

### 13.1 Quality Levels

| Mode | Video | Audio | Data/min |
|---|---|---|---|
| HD (manual) | 720p30 | Opus 48kHz | ~2.5 MB |
| Default (auto) | 480p30 | Opus 48kHz | ~1.5 MB |
| Low bandwidth | 360p15 | Opus 32kHz | ~0.8 MB |
| Audio only | None | Opus 32kHz | ~0.3 MB |
| Webinar audience | 360-720p (HLS) | AAC | ~0.5–1.5 MB |

### 13.2 Auto-Degradation Logic

Agora SDK provides network quality score (0–6) per participant:

```python
def handle_network_quality(student_uid, tx_quality, rx_quality):
    avg_quality = (tx_quality + rx_quality) / 2
    if avg_quality < 2:          # Poor
        set_video_profile("360p15")
        notify_student("Switched to low-bandwidth mode")
    elif avg_quality < 4:        # Fair
        set_video_profile("480p30")
    else:                        # Good
        set_video_profile("720p30")  # if user opted for HD
```

Teacher sees per-student quality indicator; can suggest audio-only in chat.

---

## 14. Session Security

### 14.1 Join Link

```
https://live.{tenant-domain}/join/{session_uuid}?t={signed_token}

signed_token = HMAC-SHA256(session_uuid + student_id + expiry_unix + "join", SECRET)
expiry: session_end_time + 30 minutes (allows late joins)
```

Token validated at API before issuing Agora RTC token. Token is per-student, per-session — cannot be forwarded.

### 14.2 Kick + Block

```sql
CREATE TABLE session_blocks (
  session_id  UUID NOT NULL REFERENCES live_sessions(id),
  student_id  UUID NOT NULL REFERENCES students(id),
  blocked_by  UUID NOT NULL REFERENCES users(id),
  blocked_at  TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (session_id, student_id)
);
```

Kicked student cannot rejoin: join API checks `session_blocks` before issuing token.

---

## 15. Engagement Analytics

### 15.1 Engagement Score

Per-student per-session:

```
Engagement Score = (
    (minutes_present / session_minutes) × 50     # Presence weight
  + (hand_raises × 3)                             # Active participation
  + (chat_messages × 1)                           # Text engagement
  + (poll_responses / polls_total × 20)           # Poll responsiveness
  + (quiz_correct / quiz_total × 20)              # Quiz performance
) / 100  → normalised 0–100
```

### 15.2 Class Engagement Dashboard

```
Chapter 5 Revision — 26 Mar 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Present: 31/35 (89%)    Avg engagement: 72/100

High engagement: Priya S (95), Arjun M (88), Sneha P (82)
Low engagement:  Rahul K (12 ⚠️), Dev P (18 ⚠️), Meera T (22)
→ [Flag Rahul K for welfare check]  [Flag Dev P for welfare check]
```

Low-engagement students can be flagged directly to Module 32 (Student Welfare) from this screen.

### 15.3 Platform-Level Analytics

```
Concurrent Sessions — Peak (Today 10:00–11:00)
  Sessions: 1,247
  Participants: 38,400
  Network quality distribution:
    Good:   72%
    Fair:   21%
    Poor:    7%

Infrastructure health: ✅ All regions normal
```

---

## 16. Database Schema

```sql
CREATE TABLE live_sessions (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id         UUID NOT NULL REFERENCES tenants(id),
  title             TEXT NOT NULL,
  subject_id        UUID REFERENCES subjects(id),
  class_ids         UUID[],           -- classes/batches for this session
  teacher_id        UUID NOT NULL REFERENCES staff(id),
  co_host_ids       UUID[],
  mode              TEXT NOT NULL DEFAULT 'interactive',
  -- interactive / webinar / doubt / lab / group_discussion
  status            TEXT NOT NULL DEFAULT 'SCHEDULED',
  -- SCHEDULED / LOBBY_OPEN / LIVE / ENDED / CANCELLED / POSTPONED
  scheduled_at      TIMESTAMPTZ NOT NULL,
  duration_min      INT NOT NULL DEFAULT 60,
  started_at        TIMESTAMPTZ,
  ended_at          TIMESTAMPTZ,
  agora_channel     TEXT NOT NULL UNIQUE,
  agora_recording_uid TEXT,
  recording_status  TEXT DEFAULT 'NOT_STARTED',
  recording_r2_path TEXT,
  video_id          UUID REFERENCES videos(id),     -- Module 44 record after archive
  auto_record       BOOLEAN DEFAULT TRUE,
  attendance_threshold NUMERIC DEFAULT 0.60,
  max_participants  INT DEFAULT 200,
  password          TEXT,              -- optional; hashed
  is_locked         BOOLEAN DEFAULT FALSE,
  webinar_hls_url   TEXT,             -- for webinar mode CDN stream
  recurring_parent_id UUID REFERENCES live_sessions(id),
  notes             TEXT,
  created_at        TIMESTAMPTZ DEFAULT now(),
  updated_at        TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE live_session_attendance (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id    UUID NOT NULL REFERENCES live_sessions(id),
  student_id    UUID NOT NULL REFERENCES students(id),
  status        TEXT NOT NULL DEFAULT 'ABSENT',
  -- PRESENT / LATE / EARLY_LEAVE / ABSENT
  join_time     TIMESTAMPTZ,
  leave_time    TIMESTAMPTZ,
  total_s       INT DEFAULT 0,        -- unique seconds in session
  coverage_pct  NUMERIC,
  overridden    BOOLEAN DEFAULT FALSE,
  override_by   UUID REFERENCES staff(id),
  override_note TEXT,
  synced_to_attendance BOOLEAN DEFAULT FALSE,
  UNIQUE (session_id, student_id)
);

CREATE INDEX idx_attendance_session ON live_session_attendance(session_id);
CREATE INDEX idx_attendance_student ON live_session_attendance(student_id);

CREATE TABLE session_engagement (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id      UUID NOT NULL REFERENCES live_sessions(id),
  student_id      UUID NOT NULL REFERENCES students(id),
  hand_raise_count INT DEFAULT 0,
  chat_count      INT DEFAULT 0,
  poll_responses  INT DEFAULT 0,
  quiz_correct    INT DEFAULT 0,
  quiz_total      INT DEFAULT 0,
  reaction_count  INT DEFAULT 0,
  engagement_score NUMERIC,
  UNIQUE (session_id, student_id)
);

CREATE TABLE live_session_chat (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id  UUID NOT NULL REFERENCES live_sessions(id),
  sender_id   UUID NOT NULL REFERENCES users(id),
  message     TEXT NOT NULL,
  is_private  BOOLEAN DEFAULT FALSE,    -- private to teacher
  sent_at     TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE session_co_hosts (
  session_id  UUID NOT NULL REFERENCES live_sessions(id),
  staff_id    UUID NOT NULL REFERENCES staff(id),
  added_at    TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (session_id, staff_id)
);
```

---

## 17. API Reference

```
# Session management
POST   /api/v1/live-sessions/                    # Create session
GET    /api/v1/live-sessions/{id}/               # Session details
PATCH  /api/v1/live-sessions/{id}/               # Update (before start)
POST   /api/v1/live-sessions/{id}/start/         # Teacher starts class
POST   /api/v1/live-sessions/{id}/end/           # Teacher ends class
DELETE /api/v1/live-sessions/{id}/               # Cancel session

# Join
GET    /api/v1/live-sessions/{id}/join-token/    # Get Agora RTC token (enrollment checked)
POST   /api/v1/live-sessions/{id}/leave/         # Student leaves (signals event)

# Teacher controls
POST   /api/v1/live-sessions/{id}/mute-all/      # Mute all students
POST   /api/v1/live-sessions/{id}/kick/{uid}/    # Kick participant
POST   /api/v1/live-sessions/{id}/spotlight/{uid}/  # Spotlight participant
POST   /api/v1/live-sessions/{id}/lock/          # Lock room
POST   /api/v1/live-sessions/{id}/recording/pause/    # Pause recording
POST   /api/v1/live-sessions/{id}/recording/resume/   # Resume recording

# Attendance
GET    /api/v1/live-sessions/{id}/attendance/    # Attendance report
PATCH  /api/v1/live-sessions/{id}/attendance/{student_id}/  # Override

# Polls
POST   /api/v1/live-sessions/{id}/polls/         # Create/push poll
GET    /api/v1/live-sessions/{id}/polls/{p_id}/results/  # Poll results
POST   /api/v1/live-sessions/{id}/polls/{p_id}/respond/  # Student response

# Analytics
GET    /api/v1/live-sessions/{id}/analytics/     # Session analytics
GET    /api/v1/live-sessions/{id}/engagement/    # Per-student engagement

# Upcoming
GET    /api/v1/live-sessions/upcoming/           # Student's next classes
GET    /api/v1/live-sessions/teacher/upcoming/   # Teacher's upcoming classes

# Recording (webhook from Agora)
POST   /api/v1/webhooks/agora/recording/         # Recording complete event
```

---

## 18. RBAC Matrix

| Action | Student | Teacher | Co-Host | Admin | Super Admin |
|---|---|---|---|---|---|
| View upcoming classes | ✅ | ✅ | ✅ | ✅ | ✅ |
| Join session | ✅ (enrolled) | ✅ | ✅ | ✅ | ✅ |
| Create session | ❌ | ✅ | ❌ | ✅ | ✅ |
| Start/end session | ❌ | ✅ | ❌ | ✅ | ✅ |
| Mute all, kick, lock | ❌ | ✅ | ✅ | ✅ | ✅ |
| Override attendance | ❌ | ✅ (own class) | ❌ | ✅ | ✅ |
| View session analytics | ❌ | ✅ (own) | ❌ | ✅ | ✅ |
| View engagement scores | ❌ | ✅ (own class) | ❌ | ✅ | ✅ |
| View chat history | ❌ | ✅ | ✅ | ✅ | ✅ |
| Delete session | ❌ | ✅ (future only) | ❌ | ✅ | ✅ |

---

## 19. Cross-Module Integration Map

| Module | Integration |
|---|---|
| Module 10 — Timetable | Timetable slot creates recurring live class; timetable view shows "Join" button |
| Module 11 — School Attendance | Live class attendance auto-synced after session ends |
| Module 12 — Coaching Attendance | Batch live class attendance synced |
| Module 14 — Homework | Teacher assigns post-class homework from end-of-session screen |
| Module 16 — Notes & Study Material | Whiteboard auto-saved as study material |
| Module 21 — Results | In-class quiz scores fed as classwork record |
| Module 22 — Test Series (Coaching) | Live doubt sessions for test series batches |
| Module 32 — Student Welfare | Low engagement score triggers counsellor flag |
| Module 35 — Notifications | Reminders (30min/10min/1min before); recording availability |
| Module 44 — Video Library | Recording auto-archived; transcoded to HLS; published for enrolled students |
| Module 47 — AI Performance Analytics | Live class engagement as a performance signal |
| Module 50 — Subscription | Max concurrent students per session controlled by plan tier |

---

*Module 45 — Live Classes — EduForge Platform Specification*
*Version 1.0 | 2026-03-26*
