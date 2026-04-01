# Module 48 — AI Content Generation

## 1. Purpose & Scope

AI Content Generation turns EduForge into a content factory. A teacher chooses a chapter, specifies the Bloom's level and difficulty mix, clicks "Generate", and receives publication-ready MCQs, summaries, flashcards, lesson plans, or a complete exam paper — reviewed and approved in minutes rather than hours.

The system is always teacher-in-the-loop: every AI-generated item enters DRAFT status and requires human review before it is published to any student-facing surface. This preserves quality, accountability, and curriculum alignment.

**Content types produced:**

| Category | Formats |
|----------|---------|
| Questions | MCQ, MSQ, Short Answer, Long Answer, Fill-in-Blank, True/False, Assertion-Reason, Match-Following, Case Study, Numerical Integer, Reading Comprehension, Diagram-based |
| Study material | Chapter summary, Key formulae sheet, Flashcard set, Mind map outline, Compare/contrast table, Timeline, Worked example, Common mistakes guide, Revision checklist |
| Teaching material | Lesson plan, Discussion questions, Lab guide, End-of-period quiz, Homework draft, Video script outline |

**Integration scope:**
- Approved questions published to Module 17 (Question Bank)
- Approved summaries/flashcards published to Module 16 (Notes)
- Generated exam papers imported into Module 18 (Exam Paper Builder)
- Content gap alerts from Module 47 trigger generation jobs automatically

---

## 2. AI Model Stack

| Tier | Model | Bedrock ID | Use Case | Cost per MCQ |
|------|-------|-----------|----------|-------------|
| Fast | Claude Haiku 4.5 | `anthropic.claude-haiku-4-5-20251001` | Flashcards, fill-blank, simple factual MCQs | Rs. 0.05 |
| Standard | Claude Sonnet 4.6 | `anthropic.claude-sonnet-4-6` | MCQ, short answer, summaries, lesson plans | Rs. 0.55 |
| Deep | Claude Opus 4.6 | `anthropic.claude-opus-4-6` | JEE Advanced numerical, UPSC essay, complex derivation | Rs. 2.80 |

**Model routing:** same DistilBERT complexity classifier as Module 46 — scores (subject, class, difficulty_target) → routes to appropriate tier.

**Prompt caching:** `cache_control: {"type": "ephemeral"}` applied to system prompt (curriculum context block, NCERT terminology glossary, quality rules) — saves ~80% of input token cost across bulk jobs.

### Guaranteed JSON Output

All generation calls use Claude tool use (structured output mode) to enforce JSON schema:

```python
tools = [{
    "name": "submit_question",
    "description": "Submit the generated exam question",
    "input_schema": {
        "type": "object",
        "required": ["question_text","options","answer_explanation",
                     "bloom_level","difficulty","concept_tags","ai_quality_score"],
        "properties": {
            "question_text":          {"type": "string"},
            "options": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "label":      {"type": "string", "enum": ["A","B","C","D"]},
                        "text":       {"type": "string"},
                        "is_correct": {"type": "boolean"}
                    }
                }
            },
            "answer_explanation":     {"type": "string", "minLength": 50},
            "distractor_rationale":   {"type": "object"},
            "bloom_level":            {"type": "string",
                                       "enum": ["Knowledge","Comprehension","Application",
                                                "Analysis","Evaluation","Synthesis"]},
            "difficulty":             {"type": "string",
                                       "enum": ["Easy","Medium","Hard","Very Hard"]},
            "estimated_solve_time_minutes": {"type": "integer"},
            "concept_tags":           {"type": "array", "items": {"type": "string"}},
            "source_reference":       {"type": "string"},
            "ai_quality_score":       {"type": "integer", "minimum": 1, "maximum": 5},
            "ai_quality_reasoning":   {"type": "string"}
        }
    }
}]

response = bedrock.invoke_model(
    modelId = "anthropic.claude-sonnet-4-6",
    body = json.dumps({
        "messages": messages,
        "tools":    tools,
        "tool_choice": {"type": "tool", "name": "submit_question"},
        "max_tokens": 2000
    })
)
```

---

## 3. Generation Pipelines

### 3.1 Single Question (Synchronous, SSE)

```
POST /api/v1/content/generate/question/
    │
    ├─ Validate teacher permissions + rate limit
    ├─ Fetch syllabus node text (NCERT paragraph) → RAG context
    ├─ Fetch 3 gold-standard few-shot examples from QB
    ├─ Build system prompt (curriculum + rules + few-shots)
    ├─ Route to model tier
    ├─ Call Bedrock InvokeModelWithResponseStream
    ├─ Stream JSON tokens back via SSE
    ├─ Validate JSON schema on completion
    ├─ Similarity check (pgvector) → if ≥ 0.90 → flag duplicate
    ├─ Hallucination guard (fact DB check)
    └─ Save to generated_content (status='draft') + content_body
```

### 3.2 Bulk Generation (Async SQS)

```
POST /api/v1/content/generate/bulk/
    └─ Create content_generation_jobs record (status='queued')
    └─ Enqueue to SQS content-generation.fifo (group: tenant_id)
    └─ Return {job_id}

SQS → Lambda content_bulk_generator
    ├─ Process in batches of 10 (Lambda invocation per batch)
    ├─ For each item: full generation pipeline (same as single)
    ├─ Update job.output_count after each successful item
    ├─ SSE push to teacher: "Item {n} of {total} ready for review"
    └─ Set job.status = 'completed' when done
```

### 3.3 Exam Paper Generation

```
POST /api/v1/content/generate/exam-paper/
Body: {
  "title": "Chapter 5-8 Unit Test",
  "blueprint": [
    {"chapter_id": "uuid-ch5", "section": "A", "type": "mcq", "count": 10, "marks_each": 1},
    {"chapter_id": "uuid-ch6", "section": "B", "type": "short_answer", "count": 5, "marks_each": 3},
    {"chapter_id": "uuid-ch7", "section": "C", "type": "long_answer", "count": 2, "marks_each": 10}
  ],
  "total_marks": 50,
  "duration_minutes": 90
}
```

Lambda `exam_paper_generator`:
1. For each blueprint row → generate `count` questions
2. Assemble into paper structure (sections A/B/C)
3. AI generates time estimate + marking instructions
4. Store in `generated_content` (type=`exam_paper`) with body = full paper JSON
5. Return `{gen_id}` → teacher reviews → approve → `POST /api/v1/content/drafts/{gen_id}/publish-to-module18`

---

## 4. Prompt Engineering

### MCQ System Prompt

```
You are an expert Indian exam question setter with 25+ years of experience in
CBSE/ICSE/State board and competitive exams (JEE, NEET, UPSC).

CURRICULUM SCOPE:
Subject: {subject}
Class: {class_level}
Board: {board}
Chapter: {chapter_title}
Topic: {topic}
Bloom's target: {bloom_level}
Difficulty target: {difficulty}

NCERT REFERENCE TEXT:
{ncert_paragraph}   ← injected from syllabus node

SIMILAR EXISTING QUESTIONS (avoid repeating these concepts):
{rag_similar_questions}

RULES:
1. Create an ORIGINAL question — do not reproduce NCERT text verbatim.
2. Each distractor must represent a specific student misconception. Label each distractor's rationale.
3. Answer explanation: minimum 60 words, step-by-step.
4. Use proper LaTeX for all mathematical expressions.
5. Do NOT use culturally biased names or stereotyped professions.
6. Do NOT mention competitor EdTech platforms.
7. Do NOT include questions that require students to draw (describe diagrams in text only).
8. Self-assess quality on scale 1–5 and explain your rating.

FEW-SHOT EXAMPLES:
{gold_standard_examples_from_qb}
```

### Distractor Quality Rules

The most common failure mode in AI-generated MCQs is poor distractors — options that are obviously wrong. The system prompt enforces:

- Each distractor represents a named misconception (e.g., "Confuses velocity with speed")
- Distractors are numerically close to the correct answer (for numerical questions)
- No "None of the above" or "All of the above" options
- Each option is similar in length and grammatical form

### Hallucination Guard (Fact Database)

```python
# ai_fact_database: 50,000 key NCERT facts (atomic weights, constants, dates, etc.)
# Quick lookup before saving generated content

def check_facts(question_text: str, answer_explanation: str, subject: str) -> list[str]:
    suspicious_facts = extract_numerical_claims(question_text + answer_explanation)
    violations = []
    for claim in suspicious_facts:
        db_fact = db.scalar("""
            SELECT fact_value FROM ai_fact_database
            WHERE subject = $1 AND fact_key ILIKE $2
        """, subject, f"%{claim.key}%")
        if db_fact and abs(float(claim.value) - float(db_fact)) / float(db_fact) > 0.05:
            violations.append(f"Possible factual error: {claim.key} = {claim.value}, "
                              f"expected ~{db_fact}")
    return violations

# Violations stored in content_similarity_flags (flag_type='factual_warning')
# Shown as yellow warning badge to reviewer — not blocked
```

---

## 5. Quality Review Workflow

```
AI generates item → status = 'draft'
        │
        ▼
Teacher Review Queue (Content Studio)
        ├─ View item (MathJax rendered)
        ├─ See: AI quality score (1–5), duplicate flag, factual warning
        │
        ├─── APPROVE ──────────────────────────────────────────────────────►
        │     └─ status = 'approved'                                        │
        │     └─ content published to target module (QB / Notes / etc.)    │
        │                                                                   │
        ├─── EDIT → APPROVE ───────────────────────────────────────────────►
        │     └─ teacher edits inline (HTMX contenteditable)               │
        │     └─ edit_distance computed and stored                         │
        │                                                                   │
        ├─── REQUEST REVISION ──────────────────────────────────────────────►
        │     └─ teacher types instruction: "Make harder / rephrase"       │
        │     └─ AI generates new version (revision_number + 1)            │
        │     └─ revision history preserved                                │
        │                                                                   │
        └─── REJECT ─────────────────────────────────────────────────────► archived
              └─ rejection_reason_code stored
              └─ feeds prompt improvement pipeline
```

### Review Queue Django View

```python
# views.py
class ContentDraftListView(TeacherRequired, ListView):
    template_name = "content/draft_list.html"
    paginate_by   = 20

    def get_queryset(self):
        qs = GeneratedContent.objects.filter(
            tenant   = self.request.tenant,
            creator  = self.request.user,
            status   = 'draft',
        ).select_related("syllabus_node")

        subject    = self.request.GET.get("subject")
        content_type = self.request.GET.get("type")
        min_quality  = self.request.GET.get("min_quality")

        if subject:      qs = qs.filter(subject=subject)
        if content_type: qs = qs.filter(content_type=content_type)
        if min_quality:  qs = qs.filter(ai_quality_score__gte=min_quality)

        return qs.order_by("-ai_quality_score", "-created_at")
```

### Inline Edit (HTMX)

```html
<!-- Each draft card in teacher review queue -->
<div class="draft-card" id="draft-{{ gen_id }}">
  <!-- Rendered question with MathJax -->
  <div contenteditable="true"
       hx-patch="/api/v1/content/drafts/{{ gen_id }}/"
       hx-trigger="blur"
       hx-include="closest .draft-card"
       hx-target="#draft-{{ gen_id }}"
       class="question-text math-rendered">
    {{ question_text }}
  </div>

  <!-- Action buttons -->
  <button hx-post="/api/v1/content/drafts/{{ gen_id }}/approve"
          hx-target="#draft-{{ gen_id }}"
          hx-swap="outerHTML"
          class="btn btn-success">✓ Approve</button>

  <button hx-post="/api/v1/content/drafts/{{ gen_id }}/reject"
          hx-prompt="Rejection reason:"
          hx-target="#draft-{{ gen_id }}"
          hx-swap="outerHTML"
          class="btn btn-danger">✗ Reject</button>

  <button class="btn btn-secondary"
          hx-get="/api/v1/content/drafts/{{ gen_id }}/revise-modal/"
          hx-target="#modal-container">
    ↻ Revise
  </button>
</div>
```

---

## 6. Similarity & Plagiarism Safety

### Internal Duplicate Check

```python
def check_duplicate(question_text: str, subject: str, class_level: int,
                    tenant_id: str) -> float:
    embedding = generate_embedding(question_text)  # Bedrock Titan

    max_similarity = db.scalar("""
        SELECT MAX(1 - (de.embedding <=> $1::vector)) AS sim
        FROM   doubt_embeddings de          -- reusing same pgvector infra
        JOIN   question_bank_items qbi ON qbi.item_id = de.resource_id
        WHERE  de.resource_type = 'question'
          AND  qbi.tenant_id    = $2
          AND  qbi.subject      = $3
          AND  qbi.class_level  = $4
    """, embedding, tenant_id, subject, class_level)

    return max_similarity or 0.0

# similarity >= 0.90 → flag as DUPLICATE (reviewer sees orange badge)
# similarity >= 0.97 → suggest "This question already exists — use existing?"
```

### NCERT Verbatim Detection

```python
import re

# Rabin-Karp rolling hash for fast substring match
def check_ncert_verbatim(generated_text: str, ncert_text: str,
                         threshold_words: int = 30) -> bool:
    gen_words  = generated_text.lower().split()
    ncert_words = ncert_text.lower().split()

    # Sliding window of `threshold_words` consecutive words
    ncert_hashes = set()
    for i in range(len(ncert_words) - threshold_words + 1):
        window = tuple(ncert_words[i:i+threshold_words])
        ncert_hashes.add(hash(window))

    for i in range(len(gen_words) - threshold_words + 1):
        window = tuple(gen_words[i:i+threshold_words])
        if hash(window) in ncert_hashes:
            return True  # verbatim match found

    return False
```

---

## 7. Multilingual Content Generation

### Direct Generation

```python
LANGUAGE_SYSTEM_PROMPTS = {
    "hi": "प्रश्न हिंदी में लिखें। NCERT की मानक शब्दावली प्रयोग करें।",
    "ta": "தமிழில் கேள்வி எழுதுக. NCERT சொற்களஞ்சியம் பயன்படுத்துக.",
    "te": "తెలుగులో ప్రశ్న రాయండి. NCERT పరిభాష వాడండి.",
    "gu": "ગુજરાતીમાં પ્રશ્ન લખો. NCERT ના પ્રમાણભૂત શબ્દો વાપરો.",
}

def build_system_prompt(language: str, subject: str, ...) -> list[dict]:
    base_rules   = GENERATION_RULES_ENGLISH
    lang_addon   = LANGUAGE_SYSTEM_PROMPTS.get(language, "")
    ncert_terms  = NCERT_TERMS[subject][language]

    return [
        {
            "type": "text",
            "text": base_rules + "\n\n" + lang_addon + "\n\nTerminology:\n" + ncert_terms,
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": f"Subject: {subject}, Class: {class_level}, Chapter: {chapter}"
        }
    ]
```

### Bilingual Mode

When `bilingual=True`, generate question in both English and Hindi in parallel via two Bedrock calls:

```python
async def generate_bilingual(prompt_data: dict) -> dict:
    en_task = asyncio.create_task(generate_question(prompt_data, language="en"))
    hi_task = asyncio.create_task(generate_question(prompt_data, language="hi"))
    en_result, hi_result = await asyncio.gather(en_task, hi_task)
    return {"english": en_result, "hindi": hi_result}
```

---

## 8. Lesson Plan Generator

### Input

```json
POST /api/v1/content/generate/lesson-plan/
{
  "topic": "Laws of Motion — Newton's Third Law",
  "class_level": 9,
  "board": "CBSE",
  "duration_minutes": 45,
  "teaching_style": "activity_based"
}
```

### Output Structure

```markdown
## Lesson Plan — Newton's Third Law (Class 9, CBSE, 45 min)

### Learning Objectives (Bloom's Taxonomy)
- **Knowledge**: State Newton's Third Law of Motion
- **Comprehension**: Explain the concept of action-reaction pairs with daily-life examples
- **Application**: Identify action-reaction pairs in given scenarios

### Timing Breakdown
| Phase | Duration | Activity |
|-------|----------|----------|
| Hook | 5 min | Ask: "Why does a gun recoil when fired?" |
| Instruction | 15 min | Explain law + 3 examples (rocket, swimming, walking) |
| Activity | 10 min | Partner activity: push against wall — feel the reaction |
| Practice | 10 min | 5-question MCQ quiz (see attached) |
| Summary | 5 min | Exit ticket: "Give one example from your life" |

### Discussion Questions
1. …
2. …

### Homework
[auto-created as Module 14 draft]

### Bridge to Next Class
"Next class we will measure acceleration due to gravity…"
```

---

## 9. Video Script Outline Generator

```python
# POST /api/v1/content/generate/video-script/
# Output: JSON that teacher uses as recording guide

def generate_video_script(topic: str, duration_min: int, class_level: int) -> dict:
    prompt = f"""
Create a teaching video script outline for:
Topic: {topic}, Class {class_level}, Duration: {duration_min} minutes.

Output JSON:
{{
  "title": "...",
  "learning_objectives": ["..."],
  "sections": [
    {{
      "title": "Introduction",
      "start_time_sec": 0,
      "end_time_sec": 90,
      "key_points": ["..."],
      "demo_suggestion": "..."   // optional
    }},
    ...
  ],
  "discussion_questions": ["...", "...", "..."],
  "closing_cta": "..."
}}
"""
    # Returns structured JSON → teacher uses as recording checklist
    # Saved as generated_content (type='video_script') linked to syllabus node
    # When teacher creates video in Module 44, they attach this script
```

---

## 10. Content Gap Auto-Trigger (Module 47 → 48)

```python
# EventBridge rule: analytics.concept_gap_detected
# Fired by Module 47 when a concept has:
#   - mastery_level = RED for > 40% of a class AND
#   - QB question count < 5 for that concept

def handle_concept_gap_event(event: dict):
    concept_id  = event["detail"]["concept_id"]
    tenant_id   = event["detail"]["tenant_id"]
    notified_to = event["detail"]["admin_user_id"]

    # Create generation job automatically
    job = ContentGenerationJob(
        tenant_id    = tenant_id,
        requested_by = None,              # system-triggered
        content_type = "mcq",
        syllabus_node_id = concept_id,
        quantity     = 10,
        bloom_distribution = {"Application": 5, "Analysis": 3, "Comprehension": 2},
        difficulty_distribution = {"Medium": 6, "Hard": 4},
        status       = "queued",
    )
    db.add(job)
    db.commit()

    # Notify content head
    send_notification(notified_to,
        title="Content gap detected",
        body=f"Concept '{concept_name}' has few questions & 40%+ students struggling. "
             f"10 AI-generated questions ready for your review.",
        deep_link=f"/content/drafts/?node={concept_id}")
```

---

## 11. Acceptance Rate & Continuous Improvement

```python
# Weekly analytics: acceptance_rate by (subject, prompt_version)
SELECT
    subject,
    prompt_version,
    COUNT(*) FILTER (WHERE status = 'approved') AS approved,
    COUNT(*) FILTER (WHERE status = 'rejected') AS rejected,
    COUNT(*) TOTAL,
    ROUND(100.0 * COUNT(*) FILTER (WHERE status='approved') / COUNT(*), 1) AS acceptance_rate,
    AVG(edit_distance)  AS avg_edit_distance,   -- 0 = no edits, 1 = complete rewrite
    -- Top rejection reasons
    MODE() WITHIN GROUP (ORDER BY crl.rejection_reason_code) AS top_rejection_reason
FROM generated_content gc
LEFT JOIN content_review_log crl ON crl.gen_id = gc.gen_id
WHERE gc.created_at >= NOW() - INTERVAL '7 days'
GROUP BY subject, prompt_version
ORDER BY acceptance_rate ASC;   -- worst-performing subjects at top
```

### Prompt Improvement Flywheel

```
Week N:
  Physics MCQ acceptance rate = 62% (target: 80%)
  Top rejection reason: "Poor distractor" (34% of rejections)

Prompt team action:
  - Add to system prompt: 3 new distractor-quality examples
  - Increase few-shot examples for Physics from 3 → 5
  - Raise min distractor_rationale from 10 words to 30 words

Deploy prompt_version = "phys_v3"

Week N+1:
  Physics MCQ acceptance rate = 78% ← improved
```

---

## 12. Data Model

```sql
-- generated_content: master record for each AI-generated item
CREATE TABLE content.generated_content (
    gen_id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id             UUID NOT NULL REFERENCES tenants(tenant_id),
    creator_id            UUID REFERENCES staff(staff_id),     -- NULL if system-triggered
    content_type          VARCHAR(20) NOT NULL
                          CHECK (content_type IN (
                            'mcq','msq','short_answer','long_answer','fill_blank',
                            'true_false','assertion_reason','match_following',
                            'case_study','numerical','comprehension','diagram',
                            'summary','flashcard_set','mind_map','formula_sheet',
                            'worked_example','lesson_plan','video_script','exam_paper'
                          )),
    subject               VARCHAR(50) NOT NULL,
    class_level           SMALLINT,
    board                 VARCHAR(20),
    syllabus_node_id      UUID REFERENCES syllabus_nodes(node_id),
    language              VARCHAR(10) DEFAULT 'en',
    status                VARCHAR(20) DEFAULT 'draft'
                          CHECK (status IN ('draft','in_review','approved','rejected','archived')),
    model_used            VARCHAR(60),
    prompt_version        VARCHAR(20),
    ai_quality_score      SMALLINT CHECK (ai_quality_score BETWEEN 1 AND 5),
    ai_quality_reasoning  TEXT,
    duplicate_similarity  NUMERIC(5,4),
    has_factual_warning   BOOLEAN DEFAULT FALSE,
    published_to_module   VARCHAR(20),   -- 'question_bank', 'notes', 'exam_paper'
    published_to_id       UUID,
    edit_distance         NUMERIC(5,4),  -- 0=unchanged, 1=fully rewritten
    created_at            TIMESTAMPTZ DEFAULT NOW(),
    reviewed_at           TIMESTAMPTZ,
    published_at          TIMESTAMPTZ
);

CREATE INDEX idx_gc_tenant_status  ON content.generated_content (tenant_id, status);
CREATE INDEX idx_gc_node_type      ON content.generated_content (syllabus_node_id, content_type);

-- generated_content_body: actual content (separate to avoid wide rows)
CREATE TABLE content.generated_content_body (
    body_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gen_id                UUID NOT NULL REFERENCES content.generated_content(gen_id) ON DELETE CASCADE,
    revision_number       SMALLINT NOT NULL DEFAULT 1,
    content_json          JSONB NOT NULL,    -- full structured content
    content_md            TEXT,              -- markdown representation (for quick preview)
    answer_key_json       JSONB,             -- separate answer key
    distractor_rationale  JSONB,             -- distractor → misconception map
    is_current            BOOLEAN DEFAULT TRUE,
    created_at            TIMESTAMPTZ DEFAULT NOW()
);

-- content_review_log: full audit of all teacher review actions
CREATE TABLE content.content_review_log (
    review_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gen_id                UUID NOT NULL REFERENCES content.generated_content(gen_id),
    reviewer_id           UUID NOT NULL REFERENCES staff(staff_id),
    action                VARCHAR(20) NOT NULL
                          CHECK (action IN ('approved','rejected','revision_requested','edited')),
    rejection_reason_code VARCHAR(40),
                          -- 'too_easy','too_hard','factual_error','poor_distractor',
                          -- 'biased','duplicate','off_curriculum','poor_language'
    revision_instruction  TEXT,             -- if action = 'revision_requested'
    review_note           TEXT,
    reviewed_at           TIMESTAMPTZ DEFAULT NOW()
);

-- content_generation_jobs: batch job tracker
CREATE TABLE content.content_generation_jobs (
    job_id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id             UUID NOT NULL REFERENCES tenants(tenant_id),
    requested_by          UUID REFERENCES staff(staff_id),
    content_type          VARCHAR(20) NOT NULL,
    syllabus_node_id      UUID REFERENCES syllabus_nodes(node_id),
    quantity              INT NOT NULL,
    bloom_distribution    JSONB,   -- {"Application": 5, "Analysis": 3}
    difficulty_distribution JSONB, -- {"Medium": 6, "Hard": 4}
    language              VARCHAR(10) DEFAULT 'en',
    status                VARCHAR(20) DEFAULT 'queued'
                          CHECK (status IN ('queued','processing','completed','failed','partial')),
    output_count          INT DEFAULT 0,
    failed_count          INT DEFAULT 0,
    started_at            TIMESTAMPTZ,
    completed_at          TIMESTAMPTZ,
    created_at            TIMESTAMPTZ DEFAULT NOW()
);

-- content_similarity_flags
CREATE TABLE content.content_similarity_flags (
    flag_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gen_id                UUID NOT NULL REFERENCES content.generated_content(gen_id),
    similar_to_id         UUID,             -- qbi_id or gen_id
    similar_to_type       VARCHAR(20),      -- 'question_bank_item' or 'generated_content'
    similarity_score      NUMERIC(5,4),
    flag_type             VARCHAR(30)
                          CHECK (flag_type IN ('internal_duplicate','cross_tenant',
                                               'ncert_verbatim','factual_warning')),
    auto_blocked          BOOLEAN DEFAULT FALSE,
    flagged_at            TIMESTAMPTZ DEFAULT NOW()
);

-- ai_fact_database: NCERT ground truth for hallucination guard
CREATE TABLE content.ai_fact_database (
    fact_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject               VARCHAR(50) NOT NULL,
    class_level           SMALLINT,
    fact_key              TEXT NOT NULL,     -- e.g., "speed_of_light"
    fact_value            TEXT NOT NULL,     -- e.g., "3 × 10^8 m/s"
    fact_value_numeric    NUMERIC,
    unit                  VARCHAR(30),
    source_reference      TEXT,             -- "NCERT Physics Class 11, Chapter 2"
    UNIQUE (subject, class_level, fact_key)
);
```

---

## 13. API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/api/v1/content/generate/question/` | Teacher | Single question generation (SSE stream) |
| `POST` | `/api/v1/content/generate/bulk/` | Teacher | Bulk generation job → `{job_id}` |
| `GET` | `/api/v1/content/generate/jobs/{job_id}/status` | Teacher | Poll bulk job progress |
| `GET` | `/api/v1/content/generate/jobs/{job_id}/stream` | Teacher | SSE stream of job progress |
| `GET` | `/api/v1/content/drafts/` | Teacher | Review queue (`?subject=&type=&min_quality=`) |
| `PATCH` | `/api/v1/content/drafts/{gen_id}/` | Teacher | Inline edit |
| `POST` | `/api/v1/content/drafts/{gen_id}/approve` | Teacher | Approve → publish |
| `POST` | `/api/v1/content/drafts/{gen_id}/reject` | Teacher | Reject with reason |
| `POST` | `/api/v1/content/drafts/{gen_id}/revise` | Teacher | AI revision with instruction |
| `POST` | `/api/v1/content/drafts/bulk-approve` | Teacher | Approve selected list |
| `POST` | `/api/v1/content/generate/exam-paper/` | Teacher | Full exam paper from blueprint |
| `POST` | `/api/v1/content/generate/summary/` | Teacher | Chapter summary / flashcards / mind map |
| `POST` | `/api/v1/content/generate/lesson-plan/` | Teacher | Lesson plan |
| `POST` | `/api/v1/content/generate/video-script/` | Teacher | Video script outline |
| `POST` | `/api/v1/content/generate/variants/{gen_id}` | Teacher | 3 variants of existing question |
| `POST` | `/api/v1/content/improve/{qbi_id}` | Teacher | Improve existing QB question |
| `GET` | `/api/v1/admin/content/analytics/` | Admin | Acceptance rates, cost, prompt version metrics |

---

## 14. Flutter Teacher App

### Swipe-to-Review Cards

```dart
class ContentReviewCard extends StatelessWidget {
  final GeneratedContent item;

  @override
  Widget build(BuildContext context) {
    return Dismissible(
      key: Key(item.genId),
      background:       _approveBackground(),   // green ✓
      secondaryBackground: _rejectBackground(),  // red ✗
      confirmDismiss: (direction) async {
        if (direction == DismissDirection.startToEnd) {
          await ContentApi.approve(item.genId);
          return true;
        } else {
          final reason = await _showRejectDialog(context);
          if (reason != null) {
            await ContentApi.reject(item.genId, reason);
            return true;
          }
          return false;
        }
      },
      child: Card(
        child: Column(
          children: [
            // Quality score badge
            QualityScoreBadge(score: item.aiQualityScore),
            // Question with LaTeX rendering
            MathView(data: item.contentMd),
            // Duplicate warning
            if (item.duplicateSimilarity >= 0.90)
              DuplicateWarningBanner(similarity: item.duplicateSimilarity),
          ],
        ),
      ),
    );
  }
}
```

---

## 15. Background Jobs

| Job | Trigger | Function |
|-----|---------|----------|
| `content_bulk_generator` | SQS `content-generation.fifo` | Batch question generation (10 per invocation) |
| `exam_paper_generator` | SQS `exam-paper-jobs.fifo` | Full paper generation from blueprint |
| `concept_gap_trigger` | EventBridge `analytics.concept_gap_detected` | Auto-create generation job for weak concept |
| `draft_archive_cleanup` | EventBridge monthly | Archive unreviewed drafts > 30 days old |
| `acceptance_rate_report` | EventBridge weekly Sunday | Compute acceptance metrics → notify content head |
| `fact_db_sync` | Manual (quarterly) | Refresh NCERT fact database from latest NCERT PDFs |

---

## 16. Anti-Misuse, Safety & DPDPA

| Control | Implementation |
|---------|---------------|
| **No student data in prompts** | Lambda `content_generator` checks `prompt_data` for any `student_id` or `student_name` — raises `SecurityError` if found. |
| **No Module 47 analytics in prompts** | Content generation service has no IAM permissions to `analytics.*` tables — enforced at DB role level. |
| **AI origin labelling** | All approved AI content stored with `generated_by_ai = TRUE` in QB/Notes; visible to students. |
| **Gender bias check** | Post-generation regex scan for stereotyped profession-gender assignments; `GENDER_BIAS_WARNING` flag on item. |
| **Content moderation** | AWS Comprehend `DetectToxicContent` on every generated item before saving. |
| **Rate limiting** | Teacher: 500 generations/day (Standard), 50/day (Free). Institution daily cap: configurable (default 5,000). |
| **Factual warning** | Numerical facts in generated content validated against `ai_fact_database`; `has_factual_warning` flag shown to reviewer. |
| **Juvenile content** | Content intended for Classes 1–6: mandatory `content_head` review step (additional approval tier). |
| **Audit log** | Every generation job, approval, rejection, revision, and publication logged to Module 42 `audit.events`. |
| **DPDPA purpose limitation** | Generated content DB role: `content_generator_role` — SELECT on `syllabus_nodes`, `question_bank_items`. No access to student or analytics tables. |
