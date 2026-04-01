# G-02 — Notes Viewer

> **URL:** `/exam/study/{material-id}/`
> **File:** `g-02-notes-viewer.md`
> **Priority:** P1
> **Data:** `study_material` — renders PDF or HTML notes with bilingual toggle, bookmarks, progress tracking

---

## 1. Notes Viewer

```
NOTES VIEWER — AP Economy: Industrial Corridors
APPSC Group 2 2025 | Telugu & English | 18 pages | ⭐ 4.4/5.0 (842 ratings)

  ┌──────────────────────────────────────────────────────────────────────┐
  │  [◄ Back to Study Material]            Language: [తెలుగు ▼] [EN]   │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                      │
  │  ┌────────────────────────────────────────────────────────────┐     │
  │  │                                                            │     │
  │  │   ఆంధ్రప్రదేశ్ పారిశ్రామిక కారిడార్లు                     │     │
  │  │                                                            │     │
  │  │   1. విశాఖపట్నం-చెన్నై పారిశ్రామిక కారిడార్ (VCIC)       │     │
  │  │      - 800 కి.మీ. పొడవు                                    │     │
  │  │      - Asian Development Bank సహాయంతో                      │     │
  │  │      - మూడు పారిశ్రామిక నోడ్స్: శ్రీకాకుళం,               │     │
  │  │        విశాఖపట్నం, కృష్ణపట్నం                              │     │
  │  │   …                                                        │     │
  │  │                                                 Page 4/18  │     │
  │  └────────────────────────────────────────────────────────────┘     │
  │                                                                      │
  │  [◄ Prev]  [Page 4 of 18]  [Next ►]   [🔖 Bookmark]  [📥 Download] │
  │  Progress: ████████░░░░ 22% read                                     │
  ├──────────────────────────────────────────────────────────────────────┤
  │  QUICK PRACTICE: 12 questions on this topic [Start →]               │
  │  RELATED VIDEO: "AP Industrial Policy 2023-24" (28 min) [Watch →]  │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/study/{mid}/content/` | Note content (HTML or PDF URL) |
| 2 | `PATCH` | `/api/v1/exam/study/{mid}/progress/` | Update reading progress |
| 3 | `POST` | `/api/v1/exam/study/{mid}/bookmark/` | Bookmark a page |

---

## 5. Business Rules

- PDF notes are rendered in-browser (no download required for viewing); the viewer supports pinch-zoom on mobile, page navigation, and text search (for HTML notes); PDF downloads are available for offline reading but are DRM-protected (watermarked with user ID) to prevent mass redistribution; a user who shares their downloaded PDF has their user ID visible in the watermark, creating accountability without blocking legitimate personal offline use
- Reading progress is tracked at the page level; a user who reads pages 1–4 of an 18-page document shows 22% progress; this progress feeds into the syllabus coverage tracker (A-05) — reading this AP Economy PDF marks progress on the "AP Economy → Industrial Corridors" syllabus node; the connection is: `study_material.syllabus_node_ids → user reads → progress on that syllabus_node updates`; this makes progress tracking automatic — the user doesn't manually mark topics as "done"
- The "Quick Practice" widget at the bottom links to topic-wise practice (E-04) for the same syllabus node; after reading about AP Industrial Corridors, the student can immediately test their retention with 12 questions; this read → practice → review loop is the core learning cycle; the viewer and practice engine are integrated — not separate systems that the student has to navigate between manually
- Bilingual toggle allows the student to switch between Telugu and English on the same page without reloading; for HTML notes, both language versions are loaded and CSS toggles visibility; for PDF notes, separate Telugu and English PDFs are stored and the toggle switches the rendered PDF; a student who reads the Telugu version but encounters a difficult term can toggle to English for that page and toggle back — this is how bilingual exam aspirants actually study

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division G*
