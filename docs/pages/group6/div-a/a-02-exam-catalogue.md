# A-02 — Exam Catalogue

> **URL:** `/exam/catalogue/`
> **File:** `a-02-exam-catalogue.md`
> **Priority:** P1
> **Data:** `exam` + `conducting_body` tables — fully dynamic, paginated, filterable

---

## 1. Catalogue View

```
EXAM CATALOGUE — EduForge
All Exams  |  Showing 1–20 of 198 exams  |  [Grid ▦] [List ≡]

  FILTER PANEL (left sidebar):
  ┌──────────────────────────────────┐
  │  EXAM TYPE                       │
  │  [✅] Central Government (32)    │
  │  [✅] State Government (48)      │
  │  [✅] PSU (18)                   │
  │  [✅] Banking & Finance (14)     │
  │  [✅] Teaching (12)              │
  │  [✅] Defence (9)                │
  │  [  ] Railway (8)               │
  │  [  ] Insurance (6)             │
  │  [  ] University Entrance (22)  │
  │  [  ] Police (16)               │
  │  [  ] Municipal & Civic (5)     │
  │  [  ] Revenue Dept (8)          │
  │  [  ] Professional (8)          │
  ├──────────────────────────────────┤
  │  STATE / LEVEL                   │
  │  [✅] National / Central         │
  │  [✅] Andhra Pradesh             │
  │  [✅] Telangana                  │
  │  [  ] Karnataka                 │
  │  [  ] Tamil Nadu                │
  │  [  ] Maharashtra               │
  │  [  ] Rajasthan                 │
  │  [  ] Uttar Pradesh             │
  │  [  ] + 18 more states          │
  ├──────────────────────────────────┤
  │  QUALIFICATION                   │
  │  [  ] 10th Pass                 │
  │  [  ] 12th Pass                 │
  │  [✅] Graduate                  │
  │  [  ] Post Graduate             │
  │  [  ] Diploma                   │
  │  [  ] B.Ed / D.El.Ed            │
  │  [  ] B.E / B.Tech              │
  ├──────────────────────────────────┤
  │  APPLICATION STATUS              │
  │  (●) All  (○) Open  (○) Upcoming│
  ├──────────────────────────────────┤
  │  LANGUAGE MEDIUM                 │
  │  [✅] Telugu  [✅] English       │
  │  [  ] Hindi  [  ] Tamil         │
  └──────────────────────────────────┘

  EXAM CARDS  [rendered from exam table — one card per record]
  ┌─────────────────────────────────────────────────────────────────────┐
  │  [APPSC Logo]  APPSC GROUP 2 — 2025          STATE | AP | TELUGU   │
  │  Andhra Pradesh Public Service Commission                           │
  │  Posts: Junior Asst · Surveyor · Revenue Inspector · 60+ more      │
  │  Vacancies: 897 | Qualification: Graduate | Age: 18–42 | OBC +3    │
  │  Application: Closed (Oct–Nov 2025) | Exam: Aug 2026 (tentative)   │
  │  Mock tests: 28 available | 4,28,000 aspirants preparing           │
  │  [View Details]  [Take Free Mock]  [+ Save]  🔔 [Set Alert]        │
  ├─────────────────────────────────────────────────────────────────────┤
  │  [TSPSC Logo]  TSPSC GROUP 1 — 2024          STATE | TS | TELUGU   │
  │  Telangana State Public Service Commission                          │
  │  Posts: Deputy Collector · DSP · Regional Transport Officer · more  │
  │  Vacancies: 563 | Qualification: Graduate | Age: 18–44             │
  │  Application: Closed | Mains: In progress (Apr 2026)               │
  │  Mock tests: 32 available | 2,84,000 aspirants                     │
  │  [View Details]  [Take Free Mock]  [+ Save]  🔔 [Set Alert]        │
  ├─────────────────────────────────────────────────────────────────────┤
  │  [SSC Logo]    SSC CGL — 2026              CENTRAL | NATIONAL | EN  │
  │  Staff Selection Commission                                          │
  │  Posts: Inspector · Auditor · ASO · JSO · 20+ more                 │
  │  Vacancies: ~18,000 | Qualification: Graduate | Age: 18–32         │
  │  Application: Open (Apr–Jun 2026) ⏰ | Tier-I: Jul–Aug 2026        │
  │  Mock tests: 48 available | 36,40,000 aspirants                    │
  │  [View Details]  [Take Free Mock]  [+ Save]  🔔 [Set Alert]        │
  └─────────────────────────────────────────────────────────────────────┘
  [Load more exams...]  |  Page 1 of 10  [← 1 2 3 … 10 →]
```

---

## 2. Sort & Quick Filters

```
SORT & QUICK FILTERS

  Sort by:  [Relevance ▼]  Newest  |  Most Popular  |  Deadline Soon
            Vacancies (high→low)  |  Name A–Z

  QUICK FILTER TAGS (from exam.tags — rendered dynamically):
    [Government Job] [High Vacancies] [12th Pass] [Graduate] [No Age Limit]
    [Telugu Medium] [OBC Eligible] [Female Only] [Ex-Serviceman] [PWD]
    [Open Now] [Result Declared] [AP Domicile] [TS Domicile]

  ACTIVE FILTERS:  [Graduate ✕]  [Clear all]

  STATS BAR:
    198 exams total  |  24 with open applications  |  8 results declared this month
    3,84,000 AP aspirants  |  4,20,000 TS aspirants
```

---

## 3. Catalogue — Admin Data Flow

```
HOW AN EXAM APPEARS IN CATALOGUE (data flow)

  Admin adds exam record (H-01):
    name_en: "ONGC AEE 2026"
    type: "psu"
    conducting_body: ONGC (existing record)
    state_code: null  (national)
    qualification: ["be", "btech"]
    age_min: 18, age_max: 30
    stages: [ {name: "Written Test", marks: 200}, {name: "Interview", marks: 50} ]
    syllabus_nodes: [ petroleum engineering, general aptitude, english ]
    language_medium: ["en"]
    active: true

  → Immediately appears in catalogue under type=PSU, National
  → Eligible aspirants with qualification=BE get it in recommendations (D-01)
  → Notification alert subscription available (C-01)
  → Mock test questions can be tagged to this exam's syllabus_nodes (E-05)
  → Cut-off DB ready for result entry (F-02)
  → Study material can be mapped to syllabus nodes (G-01)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/catalogue/?type=state&state=AP&qual=graduate&page=1` | Paginated catalogue with filters |
| 2 | `GET` | `/api/v1/exam/catalogue/filters/` | Available filter options (counts per option) — from DB |
| 3 | `GET` | `/api/v1/exam/catalogue/tags/` | All active tags — from DB |
| 4 | `GET` | `/api/v1/exam/catalogue/stats/` | Summary counts (total, open, declared) |
| 5 | `POST` | `/api/v1/exam/catalogue/save/?exam_id={eid}` | Save exam to My Exams (auth) |

---

## 5. Business Rules

- Every filter option in the left panel is computed from live DB data: `SELECT type, COUNT(*) FROM exam WHERE active=true GROUP BY type`; if a content admin adds the first ever `type=municipal` exam, the "Municipal & Civic" tile appears in the browse grid and the filter panel automatically; if all exams of a type are deactivated, the type disappears from the filter — no frontend code change required; filter counts must never be hardcoded in the UI
- Exam cards display `vacancies` from the DB field which the content team updates when SSC or APPSC releases revised vacancy notifications; a card showing "18,000 vacancies" when SSC has revised to "14,500" is misleading to aspirants making career decisions; the content team has a daily review of vacancy figures for exams with open applications; the `updated_at` timestamp on the card ("vacancy data updated 2 days ago") maintains transparency about data freshness
- Application status badge ("Open", "Closed", "Upcoming") is computed from `application_start`, `application_end`, and `today`; not a stored field — it is always computed on read: `CASE WHEN application_start > today THEN 'Upcoming' WHEN application_end < today THEN 'Closed' ELSE 'Open' END`; a stored `status` field that admins must manually update will inevitably drift out of sync; computed status is always accurate
- Telugu medium filter (`language_medium CONTAINS 'te'`) is critically important for AP and TS aspirants; APPSC and TSPSC exams offer Telugu medium for most posts; filtering by Telugu medium shows exams where Telugu is a valid answer-writing option, not just the UI language; displaying a TSPSC Group 1 aspirant the SSC CGL exam (English/Hindi only) as a Telugu medium exam is wrong and confusing; the `language_medium[]` field in the exam record distinguishes between exam answer language and platform UI language
- The "Deadline Soon" sort (ascending `application_end WHERE application_end > today`) is the most actionable sort for an aspirant who is actively looking to apply; showing VRO/VRA AP with 9 days left before SSC CGL with 89 days left ensures the aspirant doesn't miss an imminent window; this sort is surfaced as the default sort for authenticated users who have added exams to My Exams — deadlines for their saved exams appear first

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division A*
