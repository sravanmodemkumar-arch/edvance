# Module 46 — AI Doubt Solver

## 1. Purpose & Scope

The AI Doubt Solver gives every student on EduForge instant, curriculum-aligned, step-by-step explanations for any question — through text, image, voice, or drawing — in their own language, at any hour. It is the always-on teaching assistant that no institution can otherwise afford.

At EduForge's scale (50 million students), the system must be economically viable at Rs. 0.08 per doubt resolved. It achieves this through a three-tier LLM routing strategy, a semantic cache that serves 60 %+ of doubts without any LLM call, and a pre-built canonical answer bank of 50,000 common NCERT / JEE / NEET questions.

The solver covers:

- **All NCERT subjects, Class 1–12** — Physics, Chemistry, Biology, Mathematics, English, Hindi, Social Science, Computer Science
- **Competitive exams** — JEE Main + Advanced, NEET, UPSC, SSC, Banking, Railway, State PSC
- **Commerce & Humanities** — Accountancy, Economics, Business Studies, History, Geography, Political Science, Sociology, Psychology
- **Regional language subjects** — Hindi, Gujarati, Tamil, Telugu, Kannada, Marathi, Bengali, Malayalam, Sanskrit
- **Coaching batch doubts** — custom syllabi imported from Module 15

Scope exclusions: live exam session doubt blocking (handled by Module 19); in-class real-time doubt queue display (handled by Module 45); post-doubt performance analytics aggregation (handled by Module 47).

---

## 2. Input Modes

| # | Mode | Tech | Max Size | Notes |
|---|------|------|----------|-------|
| 1 | **Text** | Markdown textarea, inline LaTeX | 2,000 chars | `$\frac{d}{dx}$` renders |
| 2 | **Image** | Flutter `camera` + gallery | 3 images × 5 MB | OCR + Vision LLM |
| 3 | **Camera capture** | Flutter `camera` (no gallery round-trip) | 5 MB | Instant base64 |
| 4 | **Voice** | Flutter `flutter_sound` 30 s | 2 MB | AWS Transcribe async |
| 5 | **Equation keyboard** | Custom Flutter widget | — | ∫ Σ √ α β γ π θ ∂ |
| 6 | **Drawing / rough work** | Flutter `painter` canvas | PNG 1 MB | Geometry / circuit diagrams |
| 7 | **Crop & annotate** | Flutter image crop | — | Circle the specific question |
| 8 | **Multi-image** | Up to 3 images | 15 MB total | Q + diagram + own attempt |
| 9 | **Context attachment** | Chapter / video timestamp picker | — | Fetches summary + transcript |
| 10 | **Previous attempt** | Paste own working | 1,000 chars | AI does error diagnosis |

### Image Pre-Processing Pipeline

```
Flutter Client
  └─ ML Kit On-Device OCR pre-scan
  └─ Image normalise (max 1024×1024, greyscale boost, deskew)
  └─ EXIF strip (remove GPS + device metadata — DPDPA)
  └─ Upload to R2 presigned URL

Lambda `doubt_processor`
  ├─ AWS Rekognition DetectModerationLabels (threshold 0.85) ── if NSFW → reject
  ├─ AWS Textract AnalyzeDocument (FORMS + TABLES) ─────────── structured OCR
  └─ Build LLM vision payload (base64 or R2 presigned URL)
```

### Voice Transcription Pipeline

```
Flutter records 30 s WAV (16 kHz mono)
  └─ Upload to R2 presigned URL (voice/{tenant}/{doubt_id}.wav)
  └─ POST /doubts/ with voice_r2_key

Lambda `doubt_processor`
  └─ AWS Transcribe StartTranscriptionJob (language: auto-detect Hindi/English)
  └─ Poll TranscriptionJob (max 60 s) → extract transcript text
  └─ Continue as text doubt with transcript_text populated
```

---

## 3. Architecture

```
Student (Flutter / Web)
        │
        │  POST /api/v1/doubts/   (multipart: text + images + voice_key)
        ▼
API Gateway → Lambda `doubt_ingress`
        ├─ Validate student, rate-limit check (DynamoDB token bucket)
        ├─ Image pre-processing (Rekognition moderation)
        ├─ Generate embedding via Bedrock Titan Text V2
        ├─ pgvector cosine similarity search (top-5, scope: tenant+subject+class)
        │     ├─ cosine ≥ 0.92 → CACHE HIT → return stored answer immediately
        │     └─ cosine < 0.92 → enqueue to SQS `doubt-processing.fifo`
        └─ Return {doubt_id, sse_url} to client

SQS `doubt-processing.fifo`
        ▼
Lambda `doubt_processor`
        ├─ DistilBERT complexity classifier → route: Haiku / Sonnet / Opus
        ├─ Build system prompt (curriculum anchor: class + board + chapter)
        ├─ Build RAG context (top-5 similar solved doubts from pgvector)
        ├─ Call Bedrock InvokeModelWithResponseStream (SSE back to client)
        ├─ Store answer in `doubt_answers`
        ├─ Upsert embedding for new doubt
        └─ Emit event to Module 42 audit log

Client SSE stream
        └─ Flutter StreamBuilder / HTMX hx-ext="sse"
              └─ Tokens rendered progressively (flutter_math_fork for LaTeX)
```

---

## 4. AI Model Stack & Cost Optimisation

### Model Routing

| Tier | Model | Bedrock ID | Use Case | Cost per 1M tokens (in+out) |
|------|-------|-----------|----------|----------------------------|
| Fast | Claude Haiku 4.5 | `anthropic.claude-haiku-4-5-20251001` | Single-step factual, vocabulary, date facts | $0.25 in + $1.25 out |
| Standard | Claude Sonnet 4.6 | `anthropic.claude-sonnet-4-6` | Multi-step maths, derivations, coding, essay analysis | $3 in + $15 out |
| Deep | Claude Opus 4.6 | `anthropic.claude-opus-4-6` | JEE Advanced, UPSC Mains, research-level | $15 in + $75 out |

### Complexity Classifier

```python
# Lambda: doubt_complexity_classifier
# DistilBERT fine-tuned on 50k labelled EduForge doubts
# Labels: SIMPLE (→ Haiku), MODERATE (→ Sonnet), COMPLEX (→ Opus)
# Model size: 50 MB, cold start: 400 ms, warm: 8 ms

from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="s3://eduforge-models/doubt-complexity-distilbert/",
    device="cpu"
)

def route_model(question: str) -> str:
    label = classifier(question[:512])[0]["label"]
    return {
        "SIMPLE":   "anthropic.claude-haiku-4-5-20251001",
        "MODERATE": "anthropic.claude-sonnet-4-6",
        "COMPLEX":  "anthropic.claude-opus-4-6",
    }[label]
```

### Prompt Caching

```python
# Anthropic cache_control on system prompt — saves ~800 tokens per call
system_prompt_blocks = [
    {
        "type": "text",
        "text": SYSTEM_PROMPT_CURRICULUM,      # ~600 tokens — constant
        "cache_control": {"type": "ephemeral"}  # cached for 5 minutes
    },
    {
        "type": "text",
        "text": f"Student class: {student.class_level}\n"
                f"Board: {student.board}\n"
                f"Subject: {detected_subject}\n"
                f"Chapter: {chapter.title if chapter else 'General'}",
    }
]
```

### RAG Semantic Cache

```sql
-- pgvector similarity search
-- Scoped to tenant + subject + class_level to prevent cross-tenant leakage

SELECT da.answer_md, d.raw_text,
       1 - (de.embedding <=> $1::vector) AS similarity
FROM   doubt_embeddings de
JOIN   doubts d  ON d.doubt_id = de.doubt_id
JOIN   doubt_answers da ON da.doubt_id = d.doubt_id
WHERE  de.tenant_id  = $2
  AND  d.subject     = $3
  AND  d.class_level = $4
  AND  da.answer_source != 'expert'    -- exclude expert-only answers from cache
ORDER  BY de.embedding <=> $1::vector
LIMIT  5;

-- Index: IVFFlat with lists=100 for fast ANN search
CREATE INDEX doubt_embed_ivf
ON doubt_embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### Cost at 50M Scale

| Component | Monthly doubts | Unit cost | Monthly cost (INR) |
|-----------|---------------|-----------|-------------------|
| Cache hits (60 %) | 30,000,000 | Rs. 0 | Rs. 0 |
| Haiku (30 %) | 15,000,000 | Rs. 0.06 | Rs. 9,00,000 |
| Sonnet (9 %) | 4,500,000 | Rs. 0.25 | Rs. 11,25,000 |
| Opus (1 %) | 500,000 | Rs. 2.00 | Rs. 10,00,000 |
| Expert escalation (0.5 %) | 250,000 | Rs. 10 (payout) | Rs. 25,00,000 |
| **Total** | **50,000,000** | **Rs. 0.11 avg** | **Rs. ~55,25,000** |

Monthly platform subscription revenue at Rs. 0.60/student/year ÷ 12 = Rs. 0.05/student/month × 50M = Rs. 2.5 crore. AI cost = Rs. 55 lakh = 22 % of revenue — acceptable for a premium feature.

---

## 5. Answer Generation Engine

### System Prompt Structure

```
You are EduForge AI Tutor — a patient, expert Indian teacher.

RULES:
1. Always show step-by-step working. Never give just the final answer.
2. Use NCERT standard terminology for {subject}.
3. Curriculum scope: Class {class_level}, Board {board}, Chapter: {chapter}.
4. For physics/chemistry: always include dimensional analysis in last step.
5. Flag any prerequisite concepts the student needs to review.
6. Point out the most common mistake students make on this type of question.
7. For homework questions: give hints only — 3 progressive hints, then solution.
8. Respond in {language}. Use proper {script} script.
9. End with: one related practice question the student can try next.
10. Self-assess your confidence (0–100). If < 60, say "I recommend asking your teacher."

CONTEXT — similar solved doubts from this class:
{rag_context}

STUDENT'S QUESTION:
{question_text}
{image_description_if_any}
{student_attempt_if_provided}
```

### Answer Format

```markdown
## Step-by-step Solution

> **Prerequisite check**: You need to know [concept]. Quick recap: …

### Step 1: Identify the knowns
…

### Step 2: Choose the formula
$$F = ma$$
where F = net force, m = mass, a = acceleration.

### Step 3: Substitute and solve
…

### Step 4: Dimensional analysis ✓
$[F] = kg \cdot m \cdot s^{-2} = N$ ✓

> ⚠️ **Common mistake**: Students often forget to convert grams to kg here.

---
**Try this next**: [related question from QB]
**Confidence**: 94/100
```

### Hint Mode (Homework)

```python
# Teacher sets assignment.hint_mode = True
# Lambda checks this flag before calling LLM

HINT_PROMPT = """
The student is working on a homework problem. Do NOT solve it for them.
Give ONLY Hint {hint_level} of 3 (where 3 is the most direct).
Hint 1: A broad direction / concept to think about.
Hint 2: The specific formula or approach to use.
Hint 3: The first step of the solution (not the full solution).
"""
```

### Error Diagnosis Mode

When `input_type == 'previous_attempt'`:
```
You are reviewing the student's attempt below.
DO NOT solve the problem from scratch.
IDENTIFY the exact step where the error occurred.
EXPLAIN why it is wrong.
GUIDE them to correct that specific step only.

Student's attempt:
{student_attempt}
```

### Confidence Scoring

```python
# Post-process LLM response
import re

def extract_confidence(response_text: str) -> int:
    match = re.search(r'Confidence[:\s]+(\d{1,3})/100', response_text)
    if match:
        score = int(match.group(1))
        return min(max(score, 0), 100)
    return 75  # default if not present

# Auto-escalation if confidence < 60
if confidence < 60:
    trigger_expert_escalation(doubt_id)
```

---

## 6. Multilingual Engine

```
Input text
    └─ langdetect.detect() → language code
          ├─ 'en'        → English system prompt, English response
          ├─ 'hi'        → Hindi system prompt, Devanagari response
          ├─ 'ta','te',
             'kn','ml',
             'gu','mr',
             'bn'        → regional system prompt + AWS Translate post-processing
          └─ 'ur'        → Urdu with RTL flag set
```

### Language Switch

Student can tap "हिंदी में उत्तर दें" / "Answer in English" button:

```python
# API: POST /api/v1/doubts/{doubt_id}/translate
# Body: {"target_language": "hi"}
# Calls AWS Translate TranslateText on stored answer_md
# Stores translated version in doubt_answers (answer_source = 'translated_hi')
```

### NCERT Terminology Anchoring

Each subject has a terminology glossary injected into the system prompt:

```python
NCERT_TERMS = {
    "physics": {
        "en": {"velocity": "velocity", "momentum": "momentum"},
        "hi": {"velocity": "वेग", "momentum": "संवेग", "acceleration": "त्वरण"},
    },
    "chemistry": {
        "hi": {"mole": "मोल", "valency": "संयोजकता", "element": "तत्व"},
    },
    # ... all subjects
}
```

---

## 7. Human Expert Escalation

### Escalation Triggers

1. Student taps "Ask an Expert" (voluntary)
2. AI confidence score < 60 (automatic)
3. AI answer rated ≤ 2 stars (offer escalation)
4. Input type = `voice` + language = regional (lower AI accuracy)

### Expert Queue Flow

```
doubt_expert_assignments row created
    └─ SQS expert-queue.fifo message: {doubt_id, subject, class_level, sla_deadline}
          └─ Lambda expert_notifier:
                SELECT expert_id FROM doubt_experts
                WHERE subject = ANY($1) AND is_available = true AND online_now = true
                ORDER BY doubts_pending ASC LIMIT 3
                → FCM push to top-3 available experts
                → First to claim wins (optimistic locking on `claimed_by`)
```

### Expert Response Interface (Staff Portal)

```html
<!-- HTMX expert claim + respond -->
<div hx-get="/expert/doubts/{{ assignment_id }}/detail/" hx-trigger="load">
  <!-- Doubt text, images, student attempt shown -->
</div>

<form hx-post="/expert/doubts/{{ assignment_id }}/respond/"
      hx-target="#answer-status">
  <textarea name="response_md" class="markdown-editor"></textarea>
  <input type="submit" value="Submit Answer">
</form>
```

### SLA Monitoring

```python
# EventBridge rule: every 15 minutes
# Lambda: sla_monitor

overdue = db.execute("""
    SELECT dea.assignment_id, dea.expert_id, d.subject, dea.sla_deadline
    FROM   doubt_expert_assignments dea
    JOIN   doubts d ON d.doubt_id = dea.doubt_id
    WHERE  dea.responded_at IS NULL
      AND  dea.sla_deadline < NOW() + INTERVAL '30 minutes'
""").fetchall()

for row in overdue:
    notify_manager(row.expert_id, row.assignment_id)
    update(doubt_expert_assignments, sla_breached=True)
    re_assign_to_next_expert(row.doubt_id)
```

### Expert Compensation

- Per-answer payout: configurable Rs. 5–20 (set in `doubt_experts.per_answer_rate`)
- Monthly earnings written to Module 27 payroll as `income_type = 'doubt_solving'`
- New expert answers reviewed by senior tutor within 2 hours before student delivery (`needs_review = True` for first 30 answers)

---

## 8. Anti-Abuse & Safety

### Rate Limiting

```python
# DynamoDB token bucket (no Redis)
# Key: student_id#YYYY-MM-DD
# Attributes: count (INT), tier (free/standard/premium)

DAILY_LIMITS = {"free": 10, "standard": 50, "premium": 9999}
BURST_LIMIT   = 5  # per minute

def check_rate_limit(student_id: str, tier: str) -> bool:
    today = date.today().isoformat()
    item  = dynamodb.get_item(Key={"pk": f"{student_id}#{today}"})
    count = item.get("count", 0)
    return count < DAILY_LIMITS[tier]

def increment_counter(student_id: str):
    dynamodb.update_item(
        Key={"pk": f"{student_id}#{date.today().isoformat()}"},
        UpdateExpression="ADD #c :one",
        ExpressionAttributeNames={"#c": "count"},
        ExpressionAttributeValues={":one": 1},
    )
```

### Homework / Exam Protection

```python
# doubt_ingress Lambda
def validate_context(student_id: str, doubt_input: dict) -> None:
    # Block during active exam
    active_exam = db.scalar("""
        SELECT 1 FROM exam_attempts ea
        JOIN exam_sessions es ON es.session_id = ea.session_id
        WHERE ea.student_id = $1
          AND ea.status = 'IN_PROGRESS'
          AND es.end_time > NOW()
    """, student_id)
    if active_exam:
        raise HTTPException(403, "Exam in progress — doubt solver disabled.")

    # Force hint mode if homework
    if doubt_input.get("homework_assignment_id"):
        assignment = get_assignment(doubt_input["homework_assignment_id"])
        if assignment.hint_mode_only:
            doubt_input["force_hint_mode"] = True
```

### Content Safety Pipeline

```python
# Step 1: AWS Rekognition for images
rek_result = rekognition.detect_moderation_labels(
    Image={"S3Object": {"Bucket": "eduforge-docs", "Name": image_key}},
    MinConfidence=85.0
)
if rek_result["ModerationLabels"]:
    raise HTTPException(422, "Image contains inappropriate content.")

# Step 2: AWS Comprehend toxicity for text
comprehend_result = comprehend.detect_toxic_content(
    TextSegments=[{"Text": doubt_text}],
    LanguageCode="en"
)
toxicity_score = comprehend_result["ResultList"][0]["Toxicity"]
if toxicity_score > 0.8:
    raise HTTPException(422, "Inappropriate query.")

# Step 3: Prompt injection sanitisation
import html, re
safe_text = html.escape(doubt_text)
safe_text = re.sub(r'<[^>]+>', '', safe_text)  # strip any HTML tags
# Detect override attempts
override_patterns = [
    r'ignore (previous|above|all) instructions',
    r'you are now',
    r'system prompt',
    r'DAN mode',
]
for pattern in override_patterns:
    if re.search(pattern, safe_text, re.IGNORECASE):
        raise HTTPException(422, "Invalid input.")
```

### PII Scrubbing in Responses

```python
PII_PATTERNS = [
    (r'\b\d{10}\b',                'PHONE_REDACTED'),        # mobile
    (r'\b[A-Z]{5}\d{4}[A-Z]\b',   'PAN_REDACTED'),          # PAN
    (r'\b\d{4}\s\d{4}\s\d{4}\b',  'AADHAAR_REDACTED'),      # Aadhaar
    (r'\S+@\S+\.\S+',             'EMAIL_REDACTED'),         # email
]

def scrub_pii(text: str) -> str:
    for pattern, replacement in PII_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text

# Applied to every LLM response before storage and delivery
answer_md = scrub_pii(raw_llm_output)
```

---

## 9. Integration Map

| Module | Integration Point |
|--------|------------------|
| **15 — Syllabus** | Doubt auto-tagged to `syllabus_node_id` on ingest; chapter context fetched for RAG |
| **16 — Notes** | Relevant notes section deep-linked in AI answer sidebar |
| **17 — Question Bank** | 3 related practice MCQs suggested post-resolution (same concept tag) |
| **18 — Exam Paper Builder** | Most-doubted concepts auto-surfaced as exam question suggestions |
| **19 — Exam Session** | Doubt solver blocked (403) during active exam window |
| **21 — Results** | Wrong answers auto-generate pre-filled doubt requests ("Why did I get Q12 wrong?") |
| **22 — Mock Tests** | Post-mock doubt session triggered from wrong-answer list |
| **14 — Homework** | Solver runs in hint-only mode when called from homework context |
| **44 — Video Learning** | Relevant video timestamp (start–end seconds) deep-linked in answer |
| **45 — Live Classes** | In-class doubt queue sidebar; teacher sees student doubts in real-time |
| **27 — Payroll** | Expert per-answer earnings written as `doubt_solving` income |
| **42 — DPDPA Audit** | Every doubt submit + model call + expert access logged |
| **47 — AI Analytics** | Doubt tags + resolution quality feed performance analytics weak-area model |

---

## 10. Analytics & Teacher Dashboard

### Doubt Heatmap

```python
# GET /api/v1/teacher/doubts/heatmap/
# Returns chapter × week matrix of doubt counts for teacher's classes

SELECT
    sn.chapter_title,
    DATE_TRUNC('week', d.created_at) AS week,
    COUNT(*) AS doubt_count,
    AVG(da.rating) AS avg_satisfaction
FROM doubts d
JOIN doubt_answers da ON da.doubt_id = d.doubt_id
JOIN syllabus_nodes sn ON sn.node_id = d.context_chapter_id
WHERE d.tenant_id = $1
  AND d.class_id  = ANY($2)   -- teacher's classes
  AND d.created_at >= NOW() - INTERVAL '8 weeks'
GROUP BY sn.chapter_title, week
ORDER BY week DESC, doubt_count DESC;
```

### Daily Teacher Digest (SES Email)

```
EventBridge schedule: cron(30 6 * * ? *)   ← 6:30 AM IST daily

Subject: [EduForge] Your Class X-A Doubt Digest — 26 Mar 2026

Top 5 doubts from your students yesterday:
1. "What is the difference between speed and velocity?" (asked 8 times)
2. "How to find the range of a function?" (asked 6 times)
...

3 chapters with most unresolved doubts:
• Chapter 12: Thermodynamics (23 doubts, avg satisfaction 3.1/5 ⚠️)
...

View full analytics → https://app.eduforge.in/teacher/doubts/
```

### Unsatisfied Doubt Cluster Detection

```python
# Weekly Lambda: find clusters of low-rated (≤2 stars) doubts
# Uses pgvector cosine similarity to group similar complaints

SELECT da.doubt_id, da.answer_md, da.rating
FROM doubt_answers da
JOIN doubts d ON d.doubt_id = da.doubt_id
WHERE d.tenant_id = $1
  AND da.rating   <= 2
  AND da.answer_source LIKE 'ai_%'
  AND da.rated_at >= NOW() - INTERVAL '7 days';

# Then cluster by embedding similarity (DBSCAN epsilon=0.15)
# Output: {cluster_label, centroid_question, count, avg_rating, subject, chapter}
# → Notify academic head: "12 similar Physics doubts on Thermodynamics unsatisfied this week"
```

---

## 11. Flutter App — UX Details

### Floating "?" FAB

Available on every study screen (notes reader, video player, homework, mock-test review):

```dart
// Contextual doubt entry
FloatingActionButton.extended(
  onPressed: () => _openDoubtSheet(context,
    contextChapterId: widget.chapterId,   // pre-filled if available
    contextVideoId: widget.videoId,
    contextVideoTs: _videoController.position.inSeconds,
  ),
  icon: const Icon(Icons.help_outline),
  label: const Text('Ask a Doubt'),
)
```

### Streaming Answer Rendering

```dart
// SSE stream → StreamBuilder → progressive token display
StreamBuilder<String>(
  stream: doubtProvider.answerStream(doubtId),
  builder: (context, snapshot) {
    final accumulated = snapshot.data ?? '';
    return MarkdownBody(
      data: accumulated,
      builders: {
        'math': MathBuilder(),  // flutter_math_fork
        'code': CodeBuilder(),  // flutter_highlight
      },
    );
  },
)
```

### Equation Keyboard

```dart
// Custom keyboard overlay with math symbols
const kMathSymbols = [
  '∫', 'Σ', '√', '≤', '≥', '≠', 'α', 'β', 'γ', 'π', 'θ', 'λ',
  '∂', '∞', '±', '×', '÷', '∈', '∉', '∪', '∩', '⊂', '⊃', '↔',
  r'\frac{}{}', r'\sqrt{}', r'\sum_{}^{}', r'\int_{}^{}',
];
```

### Offline Doubt Queue

```dart
// WorkManager background task
@pragma('vm:entry-point')
void callbackDispatcher() {
  Workmanager().executeTask((task, inputData) async {
    if (task == 'sync_pending_doubts') {
      final pending = await DoubtLocalDb.getPendingDoubts();
      for (final d in pending) {
        try {
          final response = await DoubtApi.submit(d);
          await DoubtLocalDb.markSynced(d.localId, response.doubtId);
          await NotificationService.showAnswerAvailable(d);
        } catch (_) {}
      }
    }
    return Future.value(true);
  });
}
```

---

## 12. Web Interface (Django + HTMX)

### Embeddable Doubt Widget

Any Django template can embed the doubt widget with one line:

```html
{% include "doubts/widget_snippet.html" with chapter_id=chapter.id %}

<!-- widget_snippet.html -->
<div id="doubt-panel"
     hx-get="/doubts/widget/?chapter={{ chapter_id }}"
     hx-trigger="load"
     hx-swap="innerHTML">
  Loading doubt panel…
</div>
```

### SSE Streaming in HTMX

```html
<!-- HTMX SSE extension -->
<div hx-ext="sse"
     sse-connect="/api/v1/doubts/{{ doubt_id }}/stream"
     hx-swap="beforeend"
     id="answer-container">
</div>

<!-- Answer tokens arrive as SSE events: data: {"token": "The"} -->
<script>
htmx.on("htmx:sseMessage", function(evt) {
  const data = JSON.parse(evt.detail.data);
  document.getElementById("answer-container").innerHTML += data.token;
  MathJax.typesetPromise(); // re-render LaTeX after each chunk
});
</script>
```

### Teacher Moderation View

```python
# views.py
class TeacherDoubtListView(LoginRequiredMixin, ListView):
    template_name = "doubts/teacher_list.html"
    paginate_by   = 30

    def get_queryset(self):
        qs = Doubt.objects.filter(
            tenant=self.request.tenant,
            class_id__in=self.request.user.teaching_class_ids,
        ).select_related("student", "doubt_answers")
        subject = self.request.GET.get("subject")
        if subject:
            qs = qs.filter(subject=subject)
        rating  = self.request.GET.get("max_rating")
        if rating:
            qs = qs.filter(doubt_answers__rating__lte=rating)
        return qs.order_by("-created_at")
```

---

## 13. Pre-Built Canonical Answer Bank

```python
# popular_answers table — 50,000 rows pre-loaded from NCERT + JEE + NEET archives

# Serving canonical answers (zero LLM cost)
canonical = db.scalar("""
    SELECT pa.answer_md
    FROM   popular_answers pa
    WHERE  pa.subject = $1
      AND  pa.class_level = $2
      AND  1 - (pa.question_embedding <=> $3::vector) >= 0.95
      AND  pa.is_active = true
    ORDER  BY pa.question_embedding <=> $3::vector
    LIMIT  1
""", subject, class_level, question_embedding)

if canonical:
    store_answer(doubt_id, canonical, source='canonical', cost_inr=0)
    return canonical
```

### Auto-Promotion to Canonical

```python
# Lambda: popular_answer_promoter (runs every hour)

frequent = db.execute("""
    SELECT raw_text, subject, class_level, board,
           COUNT(*) AS ask_count,
           AVG(da.rating) AS avg_rating
    FROM   doubts d
    JOIN   doubt_answers da ON da.doubt_id = d.doubt_id
    WHERE  d.created_at >= NOW() - INTERVAL '7 days'
    GROUP  BY raw_text, subject, class_level, board
    HAVING COUNT(*) >= 5
       AND AVG(da.rating) >= 4.0
       AND NOT EXISTS (
           SELECT 1 FROM popular_answers pa
           WHERE 1 - (pa.question_embedding <=>
                 (SELECT embedding FROM doubt_embeddings
                  WHERE doubt_id = d.doubt_id LIMIT 1)) >= 0.95
       )
""").fetchall()

for row in frequent:
    # Take the highest-rated answer for this question cluster
    best_answer = get_best_answer_for_cluster(row.raw_text)
    insert_canonical(row, best_answer, source='auto_promoted')
```

---

## 14. Data Model

### Core Tables

```sql
-- doubts
CREATE TABLE doubts (
    doubt_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenants(tenant_id),
    student_id          UUID NOT NULL REFERENCES students(student_id),
    session_id          UUID REFERENCES doubt_sessions(session_id),
    subject             VARCHAR(50) NOT NULL,
    class_level         SMALLINT NOT NULL,          -- 1–12
    board               VARCHAR(20),                 -- CBSE / ICSE / State
    input_type          VARCHAR(20) NOT NULL
                        CHECK (input_type IN ('text','image','voice','drawing','multi')),
    raw_text            TEXT,
    image_r2_keys       TEXT[],                      -- up to 3 R2 object keys
    voice_r2_key        TEXT,
    transcript_text     TEXT,
    context_chapter_id  UUID REFERENCES syllabus_nodes(node_id),
    context_video_id    UUID REFERENCES videos(video_id),
    context_video_ts    INT,                         -- seconds
    force_hint_mode     BOOLEAN DEFAULT FALSE,
    status              VARCHAR(20) DEFAULT 'queued'
                        CHECK (status IN ('queued','processing','answered',
                                          'escalated','resolved','rejected')),
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    resolved_at         TIMESTAMPTZ
);

CREATE INDEX idx_doubts_tenant_student ON doubts (tenant_id, student_id);
CREATE INDEX idx_doubts_subject_class  ON doubts (subject, class_level);
CREATE INDEX idx_doubts_status         ON doubts (status) WHERE status != 'resolved';

-- doubt_answers
CREATE TABLE doubt_answers (
    answer_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doubt_id        UUID NOT NULL REFERENCES doubts(doubt_id) ON DELETE CASCADE,
    answer_source   VARCHAR(20) NOT NULL
                    CHECK (answer_source IN ('cache','haiku','sonnet','opus',
                                             'expert','canonical','translated_hi',
                                             'translated_regional')),
    answer_md       TEXT NOT NULL,
    tokens_input    INT,
    tokens_output   INT,
    cost_inr        NUMERIC(10,6),
    latency_ms      INT,
    model_version   VARCHAR(60),
    confidence_score SMALLINT,                       -- 0–100
    rating          SMALLINT CHECK (rating BETWEEN 1 AND 5),
    rated_at        TIMESTAMPTZ,
    is_helpful      BOOLEAN,
    feedback_text   TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- doubt_embeddings
CREATE TABLE doubt_embeddings (
    doubt_id     UUID PRIMARY KEY REFERENCES doubts(doubt_id) ON DELETE CASCADE,
    embedding    vector(1536) NOT NULL,
    subject      VARCHAR(50),
    class_level  SMALLINT,
    tenant_id    UUID NOT NULL REFERENCES tenants(tenant_id),
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX doubt_embed_ivf
ON doubt_embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- doubt_sessions (groups follow-up questions)
CREATE TABLE doubt_sessions (
    session_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id       UUID NOT NULL REFERENCES students(student_id),
    tenant_id        UUID NOT NULL REFERENCES tenants(tenant_id),
    started_at       TIMESTAMPTZ DEFAULT NOW(),
    last_activity_at TIMESTAMPTZ DEFAULT NOW(),
    doubt_count      INT DEFAULT 0
);

-- doubt_expert_assignments
CREATE TABLE doubt_expert_assignments (
    assignment_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doubt_id       UUID NOT NULL REFERENCES doubts(doubt_id),
    expert_id      UUID NOT NULL REFERENCES staff(staff_id),
    assigned_at    TIMESTAMPTZ DEFAULT NOW(),
    sla_deadline   TIMESTAMPTZ NOT NULL,
    claimed_at     TIMESTAMPTZ,
    responded_at   TIMESTAMPTZ,
    response_md    TEXT,
    sla_breached   BOOLEAN DEFAULT FALSE,
    student_rating SMALLINT CHECK (student_rating BETWEEN 1 AND 5)
);

-- doubt_experts (staff who handle escalations)
CREATE TABLE doubt_experts (
    expert_id         UUID PRIMARY KEY REFERENCES staff(staff_id),
    subjects          VARCHAR(50)[] NOT NULL,
    class_levels      SMALLINT[],
    per_answer_rate   NUMERIC(6,2) DEFAULT 10.00,    -- Rs.
    doubts_answered   INT DEFAULT 0,
    avg_rating        NUMERIC(3,2),
    earnings_inr      NUMERIC(12,2) DEFAULT 0,
    is_available      BOOLEAN DEFAULT TRUE,
    needs_review_count INT DEFAULT 30                -- new expert review threshold
);

-- popular_answers (canonical answer bank)
CREATE TABLE popular_answers (
    pa_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_text      TEXT NOT NULL,
    question_embedding vector(1536),
    subject            VARCHAR(50) NOT NULL,
    class_level        SMALLINT,
    board              VARCHAR(20),
    answer_md          TEXT NOT NULL,
    source             VARCHAR(20) DEFAULT 'canonical'
                       CHECK (source IN ('canonical','auto_promoted')),
    created_by         UUID REFERENCES staff(staff_id),
    view_count         INT DEFAULT 0,
    avg_rating         NUMERIC(3,2),
    is_active          BOOLEAN DEFAULT TRUE,
    created_at         TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX popular_answers_embed_ivf
ON popular_answers USING ivfflat (question_embedding vector_cosine_ops)
WITH (lists = 50);

-- doubt_limits (daily usage counter)
CREATE TABLE doubt_limits (
    student_id   UUID NOT NULL REFERENCES students(student_id),
    date         DATE NOT NULL,
    doubts_used  INT DEFAULT 0,
    tier         VARCHAR(20) DEFAULT 'free',
    PRIMARY KEY (student_id, date)
);

-- doubt_feedback
CREATE TABLE doubt_feedback (
    feedback_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doubt_id          UUID NOT NULL REFERENCES doubts(doubt_id),
    answer_id         UUID REFERENCES doubt_answers(answer_id),
    was_helpful       BOOLEAN,
    improvement_text  TEXT,
    submitted_at      TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 15. API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/api/v1/doubts/` | Student | Submit doubt (multipart: text + images + voice key) |
| `GET` | `/api/v1/doubts/{doubt_id}/stream` | Student | SSE stream — answer tokens |
| `GET` | `/api/v1/doubts/` | Student | Own doubt history (paginated; `?subject=&status=`) |
| `GET` | `/api/v1/doubts/{doubt_id}/` | Student | Single doubt + answer detail |
| `POST` | `/api/v1/doubts/{doubt_id}/escalate` | Student | Escalate to human expert |
| `POST` | `/api/v1/doubts/{doubt_id}/rate` | Student | Rate answer `{rating: 1–5, feedback_text}` |
| `GET` | `/api/v1/doubts/popular/` | Student | Search canonical answer bank |
| `PATCH` | `/api/v1/doubts/{doubt_id}/translate` | Student | Translate answer to `{target_language}` |
| `GET` | `/api/v1/teacher/doubts/` | Teacher | Class doubts list (filtered) |
| `GET` | `/api/v1/teacher/doubts/heatmap/` | Teacher | Chapter × week doubt density |
| `GET` | `/api/v1/teacher/doubts/clusters/` | Teacher | Unsatisfied doubt clusters |
| `POST` | `/api/v1/expert/doubts/{assignment_id}/respond` | Expert | Submit expert answer |
| `GET` | `/api/v1/admin/doubts/analytics/` | Admin | Platform doubt analytics |
| `DELETE` | `/api/v1/me/doubts/` | Student | DPDPA: erase all my doubts |

### Submit Doubt — Request

```json
POST /api/v1/doubts/
Content-Type: multipart/form-data

{
  "text": "Why does the kinetic energy change even when speed is constant?",
  "subject": "physics",
  "class_level": 11,
  "board": "CBSE",
  "context_chapter_id": "uuid-of-chapter-6",
  "input_type": "text",
  "force_hint_mode": false
}
```

### Submit Doubt — Response

```json
{
  "doubt_id": "d1a2b3c4-...",
  "status": "processing",
  "sse_url": "/api/v1/doubts/d1a2b3c4-.../stream",
  "cached": false,
  "model_routed_to": "sonnet"
}
```

---

## 16. Background Jobs

| Job | Trigger | Function |
|-----|---------|----------|
| `doubt_processor` | SQS `doubt-processing.fifo` | Classify → Route → Bedrock call → Store answer |
| `embedding_generator` | SQS `embedding-jobs.fifo` | Generate Titan embedding → pgvector upsert |
| `popular_answer_promoter` | EventBridge hourly | Detect 5+ identical doubts → create canonical answer |
| `sla_monitor` | EventBridge every 15 min | Alert experts nearing SLA deadline; re-assign breached |
| `teacher_digest` | EventBridge cron `30 6 * * ? *` | Generate + send daily digest email via SES |
| `doubt_retention_cleanup` | EventBridge monthly | Delete doubts older than 2 years; R2 images/voice after 30 days |
| `low_rating_detector` | EventBridge daily | Flag AI answers rated ≤ 2 for prompt improvement review |

---

## 17. Offline & Low-Bandwidth Support

### Pre-Downloaded Answer Cache

```dart
// On app launch (or during Wi-Fi background sync):
// Download top 50,000 canonical answers into SQLite

class CanonicalAnswerSync {
  static Future<void> syncIfStale() async {
    final lastSync = await prefs.getString('canonical_sync_date');
    if (lastSync == null || daysSince(lastSync) > 7) {
      final answers = await DoubtApi.downloadCanonicalPack(); // gzipped JSON
      await CanonicalDb.bulkInsert(answers);
      await prefs.setString('canonical_sync_date', today());
    }
  }
}
```

### Offline-First Flow

```
Student submits doubt (offline)
    └─ Stored in local SQLite: doubts_pending (status='pending_sync')
    └─ WorkManager task registered: 'sync_pending_doubts'

Network restored
    └─ WorkManager executes:
          POST /api/v1/doubts/ for each pending doubt
          → Receives doubt_id + SSE URL
          → Push notification when answer ready: "Your doubt on Thermodynamics is answered!"
```

### 2G Adaptation

```python
# API: detect X-Connection-Type header (set by Flutter)
# 'slow-2g' or '2g' → minimal response mode

if request.headers.get("X-Connection-Type") in ("slow-2g", "2g"):
    doubt_input["force_hint_mode"]      = True     # shorter response
    doubt_input["disable_latex_render"] = True     # plain text math
    doubt_input["max_tokens_override"]  = 300      # capped answer length
```

---

## 18. DPDPA & Compliance

| Obligation | Implementation |
|------------|---------------|
| **Retention** | Doubt text + answer: 2 years → auto-delete. Image / voice R2 objects: 30 days → lifecycle rule. |
| **Right to erasure** | `DELETE /api/v1/me/doubts/` cascades: `doubts`, `doubt_answers`, `doubt_embeddings`, `doubt_feedback`. Async job deletes R2 objects. Confirmation receipt sent via SES. |
| **No training without consent** | `student_profiles.allow_ai_training BOOL DEFAULT FALSE`. Pipeline `doubt_processor` checks this flag. No doubt data sent to any fine-tuning pipeline without explicit opt-in. |
| **Children's data (S.9)** | Students under 18: `is_minor = TRUE`. Minor doubts excluded from all analytics exports and canonical promotion pipelines. Parental consent required before any data sharing. |
| **Purpose limitation** | DB roles: `doubt_answering_role` can SELECT on `doubts` + `doubt_answers` only. `marketing_role` has no access to `doubts`. Enforced at PostgreSQL row-security level. |
| **Audit log** | Every doubt submit (`resource_type='doubt'`), model call, expert access, export, and deletion written to Module 42 `audit.events`. |
| **Data residency** | All doubt data in `ap-south-1` (AWS Mumbai). R2 bucket region: India. Bedrock inference: `ap-south-1`. AWS Transcribe: `ap-south-1`. |
| **Expert access log** | Every expert who opens a doubt logged: `INSERT INTO audit.events (actor_id, action='doubt.expert_view', resource_id=doubt_id)`. |
| **Consent for recording** | Voice input: explicit in-app consent dialog before mic access; consent event logged. |

---

## 19. Operational Excellence

### Provisioned Concurrency Scaling

```python
# Auto-scale PC before exam season
# EventBridge rule: trigger 2 weeks before major exam dates

def scale_provisioned_concurrency(expected_multiplier: float):
    baseline    = 20
    target_pc   = int(baseline * expected_multiplier)

    lambda_client.put_provisioned_concurrency_config(
        FunctionName  = "doubt-processor",
        Qualifier     = "live",
        ProvisionedConcurrentExecutions = target_pc
    )
```

### Cost Dashboard

```sql
-- Real-time cost per doubt by model (last 24 hours)
SELECT
    answer_source,
    COUNT(*)                    AS doubts_answered,
    SUM(cost_inr)               AS total_cost_inr,
    AVG(cost_inr)               AS avg_cost_inr,
    AVG(latency_ms)             AS avg_latency_ms,
    AVG(rating)                 AS avg_rating
FROM doubt_answers
WHERE created_at >= NOW() - INTERVAL '24 hours'
GROUP BY answer_source
ORDER BY total_cost_inr DESC;
```

### Cache Hit Rate Monitoring

```python
# CloudWatch metric: CacheHitRate
# Published every minute from doubt_ingress Lambda

cloudwatch.put_metric_data(
    Namespace  = "EduForge/DoubtSolver",
    MetricData = [{
        "MetricName": "CacheHitRate",
        "Value":      cache_hits / total_requests * 100,
        "Unit":       "Percent",
    }]
)
# Alert if cache hit rate drops below 50% (prompt model drift investigation)
```

### Alarm Setup

| Alarm | Threshold | Action |
|-------|-----------|--------|
| `DoubtCacheHitRate < 50%` | 5 min | PagerDuty → AI team |
| `DoubtLatencyP95 > 8s` | 3 data points | PagerDuty → Eng on-call |
| `ExpertSLABreachRate > 10%` | Daily | Email → Academic Head |
| `DailyAICost > Rs. 2,00,000` | Daily | Email → CTO |
| `DoubtRejectRate > 5%` | 30 min | PagerDuty → Safety team |
