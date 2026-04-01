# B-02 — Syllabus & Topic Tree

> **URL:** `/exam/{exam-slug}/syllabus/`
> **File:** `b-02-syllabus-view.md`
> **Priority:** P1
> **Data:** `syllabus_node` table — tree structure per exam, per stage; links to study material + question bank

---

## 1. Syllabus Tree View

```
SYLLABUS — {exam.name}
[Example render: APPSC Group 2 — 2025]
Tab: [Syllabus] active

  STAGE SELECTOR:  [Prelims ▼]  [Mains Paper 1]  [Mains Paper 2]  [Mains Paper 3]

  ── PRELIMS — General Studies & Mental Ability (150 Qs, 150 marks, 150 min) ──

  TOPIC TREE  [rendered from syllabus_node WHERE exam_id AND stage = 'Prelims']
  ┌──────────────────────────────────────────────────────────────────────┐
  │  ▼ INDIAN HISTORY                              Weightage: 12%  │
  │    ├── Ancient India (Indus, Vedic, Maurya, Gupta)   5 Qs avg       │
  │    │   📚 Notes (3)  📝 Practice (120 Qs)  ▶ Video (8)             │
  │    ├── Medieval India (Sultanate, Mughal, Vijayanagara)  4 Qs avg   │
  │    │   📚 Notes (2)  📝 Practice (96 Qs)  ▶ Video (6)              │
  │    └── Modern India (British, Freedom Movement)  6 Qs avg           │
  │        📚 Notes (4)  📝 Practice (184 Qs)  ▶ Video (12)            │
  │  {user logged in: progress bar → 90% complete}                      │
  ├──────────────────────────────────────────────────────────────────────┤
  │  ▼ AP & TELANGANA HISTORY                      Weightage: 8%   │
  │    ├── Satavahana, Kakatiya dynasties                  3 Qs avg     │
  │    ├── AP Separation Movement & Telangana Movement     4 Qs avg     │
  │    ├── AP & TS formation, statehood events             2 Qs avg     │
  │    └── Cultural heritage (temples, literature)         2 Qs avg     │
  │  {user: 55% complete — 🟡 needs attention}                          │
  ├──────────────────────────────────────────────────────────────────────┤
  │  ▼ INDIAN POLITY & GOVERNANCE                  Weightage: 10%  │
  │    ├── Constitution — Fundamental Rights, DPSP, Duties              │
  │    ├── Parliament, State Legislature, Judiciary                     │
  │    ├── Panchayati Raj, Municipalities (73rd/74th Amendments)        │
  │    ├── Commissions, Tribunals, Statutory Bodies                     │
  │    └── AP & TS State Governance, Local Bodies                       │
  ├──────────────────────────────────────────────────────────────────────┤
  │  ► GEOGRAPHY (India + AP/TS)                    Weightage: 8%   │
  │  ► ECONOMY (Indian + AP/TS)                     Weightage: 10%  │
  │  ► SCIENCE & TECHNOLOGY                         Weightage: 10%  │
  │  ► CURRENT AFFAIRS (last 12 months)             Weightage: 15%  │
  │  ► MENTAL ABILITY & REASONING                   Weightage: 18%  │
  │  ► DATA INTERPRETATION                          Weightage: 9%   │
  └──────────────────────────────────────────────────────────────────────┘
  Total: 150 marks | {syllabus_nodes.count} topics | {questions tagged} Qs in bank
```

---

## 2. Topic Detail Drill-Down

```
TOPIC DETAIL — AP & Telangana Economy (APPSC Group 2, Mains Paper 1)
[User clicked into a leaf node]

  TOPIC:      AP & Telangana Economy
  Stage:      Mains Paper 1 — General Studies
  Weightage:  ~12 marks (6 Qs at 2 marks each)
  Difficulty: Medium–High (frequently tested, data-heavy)

  SUBTOPICS:
    ✅ GSDP of AP and Telangana — growth trends
    ✅ Irrigation projects — Polavaram, Kaleshwaram, Nagarjuna Sagar
    🟡 AP industrial corridors — Vizag-Chennai, Donakonda, Kopparthi
    ❌ TS IT/ITES sector — Hyderabad's contribution to national IT exports
    ❌ AP & TS budgets — key allocations (2025–26)
    ❌ Welfare schemes — Rythu Bharosa, Amma Vodi (AP), Rythu Bandhu (TS)

  RESOURCES FOR THIS TOPIC:
    📚 Study notes: 4 PDFs (Telugu + English)  [View]
    📝 Practice questions: 84 MCQs (tagged to this topic)  [Practice Now]
    ▶ Video lectures: 3 sessions (2.5 hours total)  [Watch]
    📊 Previous year Qs: 18 questions from last 5 APPSC cycles  [Solve]

  {Authenticated user:}
  Your progress: 2 of 6 subtopics done (33%)
  Recommended: Start with "AP industrial corridors" — highest weightage remaining
```

---

## 3. Syllabus Data Model

```
syllabus_node {
  id,
  exam_id,             ← FK to exam
  stage,               ← "Prelims" | "Mains Paper 1" | "Tier-I" | any string
  parent_id (nullable),← self-referencing FK for tree structure (null = root)
  name_en,
  name_regional,
  weightage_pct,       ← percentage of total marks (approximate)
  avg_questions,       ← historical average Qs from this topic
  difficulty,          ← easy | medium | hard
  sequence,            ← ordering within parent
  tags[],              ← for cross-exam topic mapping (e.g., "indian-polity" across CGL + APPSC)
}

TREE RENDERING:
  Root nodes (parent_id IS NULL) → collapsible sections
  Child nodes → indented items under parent
  Leaf nodes → link to resources (study material, question bank, videos)
  Depth: unlimited (but typically 2–3 levels)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/{slug}/syllabus/?stage=prelims` | Syllabus tree for an exam stage |
| 2 | `GET` | `/api/v1/exam/{slug}/syllabus/{node_id}/` | Topic detail with resources |
| 3 | `GET` | `/api/v1/exam/{slug}/syllabus/{node_id}/progress/?uid={uid}` | User's progress on a topic |
| 4 | `GET` | `/api/v1/exam/{slug}/syllabus/coverage/?uid={uid}` | Overall coverage % per stage |

---

## 5. Business Rules

- The syllabus tree is the backbone of the entire exam preparation system; every other feature — mock test question tagging (E-05), study material mapping (G-01), progress tracking (A-05), weak area detection — depends on the syllabus_node structure being correct and granular; a syllabus_node "History" with no children is useless for personalisation; the content team must break down each exam's syllabus into at least 2 levels of depth (subject → topic) and ideally 3 levels (subject → topic → subtopic) for high-weightage subjects
- The `tags[]` field on syllabus_node enables cross-exam topic mapping; "Indian Polity — Fundamental Rights" appears in SSC CGL, APPSC Group 2, TSPSC Group 1, UPSC CSE, IBPS PO — all as separate syllabus_nodes; but they share the tag `indian-polity-fundamental-rights`; this allows EduForge to recommend that a student preparing for APPSC Group 2 also practice "Indian Polity" questions from SSC CGL mocks because the content overlap is real; cross-exam tagging is the mechanism for maximising question bank utilisation
- Weightage percentages are approximate and based on historical analysis of previous year papers; the content team analyses the last 5 cycles of each exam and computes topic-wise question frequency; a weightage of "12%" for "AP & Telangana Economy" in APPSC Group 2 means approximately 12% of Mains Paper 1 marks have historically come from this topic; weightage is not published by APPSC — it is EduForge's analysis; the UI labels it "Approximate weightage based on PYQ analysis" to set correct expectations
- State-specific topics (AP History, Telangana Movement, AP/TS Economy, State Governance) are the differentiating content for state exam preparation; these topics are not found in SSC/UPSC central exam question banks; the content team must create dedicated study material, question banks, and video lectures for AP and TS specific topics in Telugu and English; this content is EduForge's competitive advantage for state exam aspirants and cannot be sourced from generic national-level prep platforms
- Syllabus changes by conducting bodies (SSC introduced new Tier-II pattern in 2023; APPSC modified Group 2 exam structure in 2024) must be reflected in the syllabus tree within 7 days of official announcement; the content team archives the old syllabus version (for aspirants still preparing for the previous cycle) and creates the new version; old mock tests tagged to deprecated syllabus nodes are re-tagged or retired; a student preparing with the old syllabus for a new-pattern exam will perform poorly — keeping the syllabus current is a critical content team responsibility

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division B*
