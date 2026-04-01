# F-04 — Topper Analysis & Success Stories

> **URL:** `/exam/{slug}/toppers/` · `/exam/success-stories/`
> **File:** `f-04-topper-analysis.md`
> **Priority:** P2
> **Data:** `success_story` table — consented stories linked to exams; `exam_result` aggregate for topper stats

---

## 1. Topper Analysis (Per Exam)

```
TOPPER ANALYSIS — APPSC Group 2 — 2022
Who cleared, and how did they prepare?

  TOP 10 SELECTIONS (from published merit list — public data):
    Rank │ Score  │ Category │ Note
    ─────┼────────┼──────────┼────────────────────────────────
     1   │ 412/675│ General  │ District topper — Guntur
     2   │ 406/675│ General  │
     3   │ 398/675│ BC-B     │
    …10  │ 372/675│ General  │

  SCORE DISTRIBUTION (from published data):
    Selected candidates' score range: 228–412/675
    Average selected score (General): 324/675 (48% of total)
    Average selected score (BC-B):    286/675 (42% of total)

  EDUFORGE USERS WHO CLEARED (voluntary sharing):
    42 EduForge users confirmed their APPSC Group 2 2022 selection
    Their avg EduForge mock score: 128/150 (Prelims mocks)
    Their avg improvement over mocks: +32 marks (Mock #1 to #last)
```

---

## 2. Success Stories

```
SUCCESS STORIES — EduForge Users
[Consented testimonials linked to specific exams]

  ┌──────────────────────────────────────────────────────────────────────┐
  │  [Photo]  K. SRINIVAS — Revenue Inspector, Warangal                │
  │  TSPSC Group 2 — 2025 (selected, Rank 184, BC-B)                  │
  │  EduForge user since: Aug 2024                                      │
  │                                                                      │
  │  "నేను 14 మాసాలు EduForge మాక్ టెస్ట్‌లు చేశాను. మొదటి మాక్        │
  │  లో 96/150 వచ్చింది, చివరి మాక్ లో 138/150. ముఖ్యంగా AP Economy    │
  │  నోట్స్ చాలా helpful అయ్యాయి."                                      │
  │                                                                      │
  │  "I took EduForge mocks for 14 months. First mock: 96/150, last:   │
  │  138/150. AP Economy notes were especially helpful."                 │
  │                                                                      │
  │  Mock improvement: 96 → 138 (+42 marks) | Mocks taken: 22           │
  │  Consent: ✅ Full (name, photo, quote, exam data)                    │
  │                                                                      │
  │  [Read full story]  [Prepare like Srinivas — start TSPSC Gr2 prep] │
  └──────────────────────────────────────────────────────────────────────┘

  FILTER: Exam: [All ▼]  State: [AP ▼]  Year: [All ▼]  Language: [Telugu ▼]
  Total published stories: 6,840 | This month: 42 new
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/{slug}/toppers/?cycle=2022` | Topper stats from published results |
| 2 | `GET` | `/api/v1/exam/success-stories/?exam={slug}&state=AP` | Consented success stories |
| 3 | `POST` | `/api/v1/exam/success-stories/submit/` | Submit success story (with consent form) |

---

## 5. Business Rules

- Success stories require explicit DPDPA-compliant consent before publication; the consent form captures: name display (full / initials only), photo (yes/no), exam + score sharing (yes/no), quote (verbatim from submission), and scope (EduForge website, social media, print); consent can be withdrawn at any time — EduForge removes the story from all active channels within 30 days; stories without signed consent are stored as "draft" and never published
- Topper analysis data (merit list ranks, score ranges) uses only publicly published data from official result notifications; EduForge does not claim credit for a topper's success unless that specific individual submitted a success story through the consent process; a news article saying "APPSC Group 2 Rank 1 used EduForge" without that person's consent is not published by EduForge — it may be published by media independently but EduForge does not amplify it without consent
- The "42 EduForge users who cleared" statistic is computed from voluntary result-sharing: users who entered their actual exam result in My Exams (A-05) after results were declared; this number is always lower than the actual count of EduForge users who cleared (many users don't share results); EduForge publishes this as "42 confirmed EduForge users selected" not "42 users selected thanks to EduForge" — the distinction matters for advertising standards
- Bilingual success stories (Telugu + English) are critical for AP/TS aspirants who identify more strongly with stories told in their language; a Telugu-medium aspirant from a village near Guntur reading Srinivas's story in Telugu feels a stronger connection than reading the same story in English; the content team encourages story submission in the aspirant's preferred language and provides translation for the other language
- Success stories are linked to specific exams via `exam_id` so they appear on the correct exam detail page; a TSPSC Group 2 success story appears on the TSPSC Group 2 exam page, not the APPSC Group 2 page; cross-exam stories (an aspirant who cleared both SSC CGL and APPSC Group 2) are linked to both exams; this exam-level linking ensures that an aspirant browsing APPSC Group 2 sees only relevant success stories, not a generic wall of testimonials from unrelated exams

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division F*
