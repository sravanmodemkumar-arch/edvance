# G-04 — Current Affairs Engine

> **URL:** `/exam/current-affairs/`
> **File:** `g-04-current-affairs.md`
> **Priority:** P1
> **Data:** `current_affair` table — daily entries tagged by category, state, exam relevance

---

## 1. Current Affairs Hub

```
CURRENT AFFAIRS — EduForge Exam Hub
Daily updates · Monthly capsule · Exam-tagged · Telugu + English

  FILTER: [All ▼]  [National]  [AP]  [Telangana]  [International]
          [Polity]  [Economy]  [Science]  [Sports]  [Awards]  [Schemes]
  LANGUAGE: [తెలుగు ▼]  [English]

  TODAY'S HIGHLIGHTS (31 March 2026):
  ┌──────────────────────────────────────────────────────────────────────┐
  │  📰 India's FY 2025–26 GDP growth revised to 7.2% (RBI estimate)   │
  │     Tags: [Economy] [National] [Banking exams] [UPSC]               │
  │     One-liner: RBI revised India's FY26 GDP growth to 7.2% from 6.8│
  │     [Read detail + MCQ →]                                            │
  ├──────────────────────────────────────────────────────────────────────┤
  │  📰 AP CM launches "Jagananna Amma Vodi Phase 3" — ₹15,000/student │
  │     Tags: [AP Schemes] [APPSC exams] [AP Economy]                   │
  │     One-liner: Phase 3 covers 82 lakh students; budget ₹6,450 crore│
  │     [Read detail + MCQ →]                                            │
  ├──────────────────────────────────────────────────────────────────────┤
  │  📰 Telangana declares "Industrial Policy 2024–29" — TS-iPASS 2.0  │
  │     Tags: [TS Economy] [TSPSC exams] [Industry]                     │
  │     One-liner: New policy targets ₹5 lakh crore investment by 2029  │
  │     [Read detail + MCQ →]                                            │
  └──────────────────────────────────────────────────────────────────────┘

  MONTHLY CAPSULE:
    [📥 March 2026 CA Capsule — Telugu (42 pages)] 🆓
    [📥 March 2026 CA Capsule — English (38 pages)] 🆓
    [📥 AP & TS State CA Capsule — March 2026 (18 pages)] 🆓

  CA QUIZ:
    [📝 March 2026 CA Quiz — 50 Qs] — Test your current affairs retention
```

---

## 2. Current Affair Entry Detail

```
CA DETAIL — AP CM launches "Jagananna Amma Vodi Phase 3"

  DATE: 28 March 2026
  CATEGORY: Government Schemes · AP State
  EXAM RELEVANCE: APPSC Group 1/2/3/4 · AP Police · AP DSC

  DETAIL (Telugu + English):
    ── Telugu ──
    ఆంధ్రప్రదేశ్ ముఖ్యమంత్రి 'జగనన్న అమ్మ ఒడి' పథకం మూడో దశను
    ప్రారంభించారు. ఈ దశలో 82 లక్షల విద్యార్థుల తల్లులకు సంవత్సరానికి
    ₹15,000 అందించబడుతుంది. బడ్జెట్: ₹6,450 కోట్లు. ...

    ── English ──
    AP Chief Minister launched Phase 3 of 'Jagananna Amma Vodi' scheme.
    ₹15,000 per student annually to 82 lakh student mothers.
    Budget: ₹6,450 crore. The scheme aims to reduce school dropout rates...

  EXAM-READY MCQ:
    Q. Jagananna Amma Vodi scheme Phase 3 budget allocation is:
    (A) ₹4,200 crore  (B) ₹5,800 crore  (●) ₹6,450 crore  (D) ₹7,200 crore
    ✅ Correct!

  KEY FACTS TO REMEMBER:
    • Launched: March 2026 (Phase 3)
    • Beneficiaries: 82 lakh students' mothers
    • Amount: ₹15,000/year per student
    • Objective: Reduce dropout, promote girl child education
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/current-affairs/?date=2026-03-31&state=AP` | Daily CA entries |
| 2 | `GET` | `/api/v1/exam/current-affairs/capsule/?month=2026-03&lang=te` | Monthly capsule download |
| 3 | `GET` | `/api/v1/exam/current-affairs/quiz/?month=2026-03` | Monthly CA quiz |
| 4 | `GET` | `/api/v1/exam/current-affairs/{id}/` | Single CA entry detail with MCQ |

---

## 5. Business Rules

- Current affairs is the single highest-effort, highest-frequency content type; the content team publishes 5–10 entries daily (national + AP + TS); each entry must be: factually verified (from PIB, official government press releases, or established news sources), tagged by category and state, tagged to relevant exams, available in Telugu and English, and include at least 1 exam-ready MCQ; this is a 365-day-a-year commitment — there are no "off days" for current affairs
- AP and Telangana state-specific current affairs are the highest-value differentiator for state exam aspirants; national-level CA platforms (Oliveboard, Testbook) cover central government events well but miss AP/TS state CM decisions, state budget details, industrial policies, welfare scheme launches, district-level developments, and state cabinet reshuffles; EduForge's dedicated AP + TS CA coverage is what makes it indispensable for APPSC and TSPSC aspirants
- Monthly capsules compile all daily entries into a downloadable PDF (Telugu + English); the capsule is free because it drives subscription adoption — an aspirant who downloads the free CA capsule and finds it useful is more likely to subscribe for mock tests; the capsule is published by the 5th of the following month (March capsule available by April 5); late publication reduces its value because aspirants need it for month-end revision
- Exam-tagging of CA entries ("this entry is relevant for APPSC Group 1/2/3/4 and AP Police") enables personalised CA feeds; a student whose My Exams includes APPSC Group 2 sees AP-relevant CA in their daily digest; an SSC CGL student sees national CA; a student preparing for both sees a merged feed with no duplicates; the tagging is done by the content team at the time of publishing — it is not automated because exam relevance requires editorial judgment
- CA quiz questions have a short shelf life — they are relevant for 6–12 months after the event; a question about "who was appointed as the new RBI Governor in March 2026?" is valid for mocks conducted in 2026 but becomes trivial (common knowledge) by 2028; the content team retires CA questions older than 12 months from active mock tests and practice banks; they remain accessible in the "historical CA" archive for aspirants studying for exams that test 2-year current affairs windows

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division G*
