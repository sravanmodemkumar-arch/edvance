# A-04 — Initial Content Setup (Import / Licence)

> **URL:** `/partner/onboard/content/`
> **File:** `a-04-content-setup.md`
> **Priority:** P1
> **Roles:** TSP Owner · TSP Faculty (content upload) · EduForge Content Team (licence activation)

---

## 1. Content Setup Dashboard

```
CONTENT SETUP — TopRank Academy
Step 4 of 6

  CONTENT SOURCES:
  ┌─────────────────────────────────────────────────────────────────────┐
  │ ① OWN QUESTIONS (Upload)          ② EDUFORGE POOL (Licence)       │
  │                                                                     │
  │  Uploaded:   4,312 questions        Licensed:  0 questions          │
  │  Exams:      APPSC (2,100)          Plan:      Not activated        │
  │              SSC (2,212)             Available: 18,42,000+ questions │
  │  Errors:     23 (formatting)                                        │
  │                                     [Activate Content Licence →]    │
  │  [📁 Upload More]  [Fix Errors]                                     │
  └─────────────────────────────────────────────────────────────────────┘

  CONTENT READINESS:
    Questions:   ✅ 4,312 own questions uploaded
    Mock tests:  ✅ 3 mock tests created (APPSC Prelims #1, #2; SSC CGL #1)
    Study notes: 🟡 0 uploaded (optional — can add later)
    Videos:      🟡 0 linked (optional — can add later)

  [← Back]  [Save & Continue →]
```

---

## 2. Question Upload (CSV/Excel)

```
UPLOAD QUESTIONS — TopRank Academy

  FORMAT: CSV or Excel (.xlsx)  |  [📥 Download Template]

  TEMPLATE COLUMNS:
  ┌──────────────────────────────────────────────────────────────────────┐
  │ exam | subject | topic | question_text | option_a | option_b |      │
  │ option_c | option_d | correct_option | explanation | difficulty |   │
  │ language | year | source                                            │
  └──────────────────────────────────────────────────────────────────────┘

  UPLOAD STATUS:
  ┌──────────────────────────────────────────────────────────────────────┐
  │ File: appsc_prelims_questions.xlsx                                   │
  │ Total rows: 2,123                                                    │
  │ ✅ Parsed: 2,100                                                     │
  │ ❌ Errors: 23                                                        │
  │                                                                      │
  │ ERROR DETAILS:                                                       │
  │  Row 45:  Missing correct_option (required field)                    │
  │  Row 112: option_c is empty but correct_option = C                   │
  │  Row 389: Duplicate — matches existing question (hash collision)     │
  │  ... 20 more [View All Errors]                                       │
  │                                                                      │
  │ [📥 Download Error Report]  [Fix & Re-upload]  [Skip Errors & Save] │
  └──────────────────────────────────────────────────────────────────────┘

  BILINGUAL SUPPORT:
    Primary language:    [ English ▼ ]
    Secondary language:  [ Telugu ▼ ]  (optional — for bilingual question display)
    If secondary language: upload one row per question with `language` = en or te
```

---

## 3. EduForge Content Licence

```
EDUFORGE CONTENT LICENCE — TopRank Academy

  AVAILABLE TIERS:
  ┌──────────────┬──────────────┬──────────────┬──────────────────────┐
  │ Tier         │ Questions    │ Per Student   │ Includes             │
  │              │              │ Per Month     │                      │
  ├──────────────┼──────────────┼──────────────┼──────────────────────┤
  │ Basic        │ 2,00,000     │ ₹5/student   │ MCQs only            │
  │ Standard     │ 8,00,000     │ ₹12/student  │ MCQs + explanations  │
  │ Premium      │ 18,42,000+   │ ₹20/student  │ Full pool + CA + PYQ │
  └──────────────┴──────────────┴──────────────┴──────────────────────┘

  SELECTED: Standard (₹12/student/month)
  Estimated cost: 3,000 students × ₹12 = ₹36,000/month

  EXAM COVERAGE (Standard tier):
    ✅ APPSC Group 1, 2, 3, 4    ✅ SSC CGL, CHSL, MTS
    ✅ Banking (IBPS PO/Clerk)    ✅ RRB NTPC, Group D
    ○ UPSC CSE (Premium only)     ○ GATE (Premium only)

  CONTENT RULES:
    • Licensed content appears under TSP's brand (no EduForge watermark)
    • TSP cannot export or resell licensed content
    • Content is read-only — TSP cannot edit EduForge questions
    • TSP's own questions are always their property (can export anytime)

  [Activate Licence]  [Skip — own content only]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/partner/content/upload/` | Upload question CSV/Excel |
| 2 | `GET` | `/api/v1/partner/content/upload/{job_id}/status/` | Upload processing status |
| 3 | `GET` | `/api/v1/partner/content/upload/{job_id}/errors/` | Upload error details |
| 4 | `GET` | `/api/v1/partner/content/stats/` | Content stats (counts by exam, source) |
| 5 | `POST` | `/api/v1/partner/content/licence/activate/` | Activate EduForge content licence |
| 6 | `GET` | `/api/v1/partner/content/licence/` | Current licence tier and usage |

---

## 5. Business Rules

- Question upload uses async processing because large CSV files (50,000+ rows) take 30–90 seconds to parse, validate, and deduplicate; the TSP uploads the file, gets a job ID, and polls for status; the UI shows a progress bar; this prevents HTTP timeouts and lets the TSP continue other onboarding steps while questions process in the background
- Duplicate detection uses a normalised text hash (lowercased, whitespace-collapsed, punctuation-stripped) of question_text; if a TSP uploads the same question twice (common when re-uploading after fixing errors), the system skips duplicates silently rather than erroring; cross-TSP deduplication does not happen — if TSP-1 and TSP-2 both upload the same question, both keep their own copy, because content isolation between tenants is absolute
- The "Skip Errors & Save" option exists because most TSPs have messy spreadsheets and insisting on 100% clean data before proceeding blocks onboarding; a TSP with 2,100 clean questions and 23 errors can go live with the 2,100 and fix the 23 later; the error report is downloadable so the TSP can fix offline and re-upload; no question is partially saved — a row either passes all validations or is entirely rejected
- Content licence billing is per-active-student-per-month, not per-question or per-download; "active student" means a student who logged in at least once in the billing month; this prevents the TSP from being charged for students who enrolled but never used the platform; the count is computed on the 1st of each month based on the previous month's login data; the TSP can see a real-time estimate on their billing dashboard (E-03)

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division A*
