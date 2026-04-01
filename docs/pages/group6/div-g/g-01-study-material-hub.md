# G-01 — Study Material Hub

> **URL:** `/exam/{slug}/study/`
> **File:** `g-01-study-material-hub.md`
> **Priority:** P1
> **Data:** `study_material` linked to `syllabus_node` — renders material for any exam based on its syllabus tree

---

## 1. Study Material Hub (Per Exam)

```
STUDY MATERIAL — APPSC Group 2 2025
All resources mapped to your syllabus | Telugu + English

  BROWSE BY SYLLABUS TOPIC  [follows B-02 syllabus tree]
  ┌──────────────────────────────────────────────────────────────────────┐
  │  TOPIC                    │ Notes │ Videos │ PYQs │ Practice │ Status│
  ├───────────────────────────┼───────┼────────┼──────┼──────────┼───────┤
  │  ▼ Indian History          │   8   │   12   │  48  │   120    │ ✅   │
  │    Ancient India           │   2   │    4   │  16  │    40    │ Done  │
  │    Medieval India          │   2   │    3   │  14  │    36    │ Done  │
  │    Modern India            │   4   │    5   │  18  │    44    │ 🟡   │
  │  ▼ AP & TS History         │   4   │    6   │  18  │    84    │ 🟡   │
  │  ▼ Indian Polity           │   6   │    8   │  42  │   184    │ ✅   │
  │  ► Geography               │   4   │    6   │  28  │    96    │ ❌   │
  │  ► AP & TS Economy         │   4   │    6   │  18  │    84    │ ❌   │
  │  ► Science & Technology    │   6   │    8   │  36  │   124    │ 🟡   │
  │  ► Current Affairs         │ 12/mo │    4/mo│   —  │    40/mo │ ♻️   │
  │  ► Mental Ability          │   4   │    8   │  36  │   148    │ 🟡   │
  └───────────────────────────┴───────┴────────┴──────┴──────────┴───────┘
  Total: 48 note sets · 58 videos · 226 PYQs · 880 practice Qs

  MATERIAL TYPES:
  ┌─────────┬────────────────────────────────────────────────────────────┐
  │  📚 Notes│ PDF + HTML notes (Telugu & English) — topic-wise          │
  │  ▶ Video│ Lecture recordings — 15–45 min each — topic-wise          │
  │  📋 PYQ │ Previous year questions digitised + explained             │
  │  📝 Prac│ Practice questions tagged to topic (E-04 integration)    │
  │  📰 CA  │ Monthly current affairs capsule (auto-refreshed)          │
  └─────────┴────────────────────────────────────────────────────────────┘

  FILTER:  [All types ▼]  [Free only ▼]  [Telugu ▼]  [Not started ▼]
```

---

## 2. Study Material Data Model

```
study_material {
  id,
  title_en, title_regional,
  type,                    ← "notes_pdf" | "notes_html" | "video" | "pyq_set" | "current_affairs"
  syllabus_node_ids[],     ← FK to syllabus_node — maps to topic(s)
  exam_tags[],             ← which exams this material is relevant for
  language[],              ← ["te", "en"]
  content_url,             ← URL or storage path (PDF URL, video embed, HTML path)
  duration_minutes,        ← for videos
  page_count,              ← for PDFs
  difficulty,              ← beginner | intermediate | advanced
  is_free,
  published_at,
  created_by,
  reviewed,
  download_count,
  rating_avg,              ← 1–5 from user ratings
  rating_count,
}
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/{slug}/study/?type=notes_pdf&topic={node_id}` | Study material for an exam by type/topic |
| 2 | `GET` | `/api/v1/exam/{slug}/study/coverage/?uid={uid}` | User's material consumption progress |
| 3 | `GET` | `/api/v1/exam/study/search/?q=AP+economy&lang=te` | Search across all study material |
| 4 | `POST` | `/api/v1/exam/study/{mid}/rate/` | Rate material (1–5) |

---

## 5. Business Rules

- Study material is mapped to syllabus nodes (B-02), not directly to exams; a PDF on "Indian Polity — Fundamental Rights" is mapped to the `syllabus_node: Fundamental Rights`; this node exists in APPSC Group 2, TSPSC Group 1, SSC CGL, and UPSC CSE syllabi; the material appears on all four exam study hubs automatically; when a student accesses APPSC Group 2's study material page, the system queries `study_material WHERE syllabus_node_ids INTERSECT exam's syllabus_nodes`; this node-based mapping maximises content reuse across exams
- Telugu-first content for AP and TS exams is non-negotiable; a PDF on "AP Economy — GSDP Trends" that exists only in English is unusable for 60%+ of APPSC aspirants who study in Telugu medium; the content team must produce Telugu notes as native content (not translation of English notes); Telugu-medium aspirants read content structured differently — they expect Telugu administrative terminology, Telugu numerical formatting, and references to Telugu sources; machine-translated Telugu content is detectable and damages trust
- Current affairs material has a monthly refresh cycle; the content team publishes a "Monthly CA Capsule" (Telugu + English) covering national and state-level current affairs relevant to the exam's syllabus; AP and TS state-specific current affairs (CM decisions, state budget highlights, major scheme launches, significant appointments) are included in state exam capsules but not in central exam capsules; a student preparing for APPSC Group 2 needs AP-specific CA; a student preparing for SSC CGL does not
- Material quality is controlled through the same create → review → publish workflow as questions (E-05); notes written by a subject expert are reviewed by a second expert before publishing; the review checks: factual accuracy, relevance to the exam syllabus, language quality (Telugu and English), and absence of copyright violations (content must be original or properly attributed); material sourced from NCERT, government reports, or public domain is clearly attributed; material plagiarised from competitive platforms is a legal and ethical violation
- Download counts and ratings (`rating_avg`, `download_count`) are surfaced on the material listing to help aspirants identify the most useful content; a notes PDF with 1,24,000 downloads and 4.6/5.0 rating is socially validated as high-quality; a newly published video with 200 views and no ratings is less validated but may be excellent — the system adds a "New" badge for recently published material to encourage early engagement; ratings below 3.0/5.0 trigger a content team review for quality issues

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division G*
