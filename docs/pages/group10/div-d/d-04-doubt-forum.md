# D-04 — Doubt Forum & Q&A

> **URL:** `/student/learn/doubts`
> **File:** `d-04-doubt-forum.md`
> **Priority:** P2
> **Roles:** Student (S2–S6) · Mentor/Educator (answers doubts) · AI (auto-answers common doubts)

---

## Overview

Students submit doubts arising from practice questions, mock tests, notes, or videos and receive answers from three sources: (1) **AI auto-answer** — instant response for common doubts using EduForge's content pool and solution database, (2) **Community** — other students answer (upvote-based quality), (3) **Expert** — Premium students get priority routing to subject matter experts (content partners from Group 9) with a 4-hour SLA. Free students get community + AI answers; Premium students get all three with expert priority. Average doubt resolution: 22 minutes (AI), 2.3 hours (community), 4 hours (expert).

---

## 1. My Doubts Dashboard

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MY DOUBTS                                    [Ask a Doubt →]  [Search 🔍]  │
│                                                                              │
│  [My Doubts ●] [Bookmarked] [Browse Popular]                               │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  ✅ Resolved · 2 hours ago                                            │  │
│  │  "Why is SN1 favoured in tertiary carbon but SN2 in primary?"        │  │
│  │  Subject: Chemistry · Topic: Organic — Reaction Mechanisms           │  │
│  │  Answered by: 🤖 AI (instant) + Community (3 upvotes)               │  │
│  │  [View Answer →]                                                      │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  ⏳ Pending · Submitted 45 min ago                                    │  │
│  │  "How to solve this integration problem?" [image attached]           │  │
│  │  Subject: Maths · Topic: Calculus — Integration                      │  │
│  │  🤖 AI answer available · Waiting for expert review (Premium)       │  │
│  │  [View AI Answer →]                                                   │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Total: 12 doubts asked · 10 resolved · 2 pending                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Ask a Doubt

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ASK A DOUBT                                                                 │
│                                                                              │
│  Subject *     [ Chemistry ▼ ]                                              │
│  Topic         [ Organic Chemistry ▼ ] (auto-detected from context)         │
│                                                                              │
│  Your Question:                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │ Why does Cannizzaro reaction only work with aldehydes that don't     │  │
│  │ have alpha-hydrogens? What happens if there ARE alpha-hydrogens?     │  │
│  │                                                                       │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Attach image: [📷 Camera] [📁 Upload] — for handwritten work or diagrams │
│                                                                              │
│  Context (optional — helps get better answers):                             │
│  ☐ From mock test: [ JEE Mock #25, Q.42 ▼ ]                               │
│  ☐ From practice: [ Organic Practice #3, Q.18 ▼ ]                         │
│  ☐ From notes: [ Organic Chemistry Revision Notes, Page 12 ]               │
│                                                                              │
│  [Submit Doubt →]                                                            │
│                                                                              │
│  ── SIMILAR DOUBTS (shown before submit) ────────────────────────────────   │
│  🤖 AI found 3 similar previously answered doubts:                         │
│  1. "Cannizzaro vs Aldol — when to apply which?" (142 upvotes) [View →]   │
│  2. "Why no alpha-hydrogen condition in Cannizzaro?" (89 upvotes) [View →]│
│  3. "Disproportionation reactions explained" (67 upvotes) [View →]        │
│                                                                              │
│  Does any of these answer your question?  [Yes, resolved!]  [No, submit]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/student/doubts` | List student's doubts (with filters) |
| 2 | `POST` | `/api/v1/student/doubts` | Submit a new doubt |
| 3 | `GET` | `/api/v1/student/doubts/{doubt_id}` | Doubt detail with all answers |
| 4 | `POST` | `/api/v1/student/doubts/{doubt_id}/resolve` | Mark doubt as resolved |
| 5 | `GET` | `/api/v1/student/doubts/similar?q={query}` | Find similar already-answered doubts |
| 6 | `POST` | `/api/v1/student/doubts/{doubt_id}/answers/{answer_id}/upvote` | Upvote an answer |
| 7 | `GET` | `/api/v1/student/doubts/popular?subject={subject}` | Browse popular doubts |

---

## 4. Business Rules

- The "Similar Doubts" feature is shown before the student submits — this deflects 38% of new doubts by surfacing existing answers, reducing the load on expert answerers and providing the student with an instant resolution; the similarity search uses semantic embedding (not just keyword match) — "Why can't Cannizzaro work with alpha-H aldehydes?" matches "Cannizzaro reaction alpha hydrogen condition" even though the wording is different.

- AI auto-answers use EduForge's solution database (solutions from 18,42,000+ questions) combined with a fine-tuned LLM that generates explanations; the AI answer is marked with a "🤖 AI-generated" label and includes a confidence score; high-confidence answers (>90%) are shown instantly; medium-confidence (60–90%) answers are shown with "This is an AI-generated answer — verify with an expert" disclaimer; low-confidence (<60%) doubts skip AI and go directly to community/expert queue.

- Premium expert routing: doubts from Premium students are flagged for priority and routed to subject-matter experts (content partners from Group 9) who earn ₹15 per doubt answered; the SLA is 4 hours for a first response; expert answers are reviewed by the EduForge content team for quality before being marked as "Expert Verified ✅"; this creates a quality feedback loop where content partners earn additional revenue by answering doubts, and students get authoritative answers.

- Image upload for doubts supports handwritten work — students in Tier-2/3 towns often solve problems on paper and photograph their work to ask "where did I go wrong?"; the image is passed to the AI engine which uses OCR + mathematical expression recognition to parse the handwritten solution and identify the error step; this hybrid image+text doubt resolution is a significant differentiator for EduForge.

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division D*
