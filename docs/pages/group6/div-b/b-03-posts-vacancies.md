# B-03 — Posts, Vacancies & Salary

> **URL:** `/exam/{exam-slug}/posts/`
> **File:** `b-03-posts-vacancies.md`
> **Priority:** P1
> **Data:** `exam_post` table — linked to exam; each post is a separate record with vacancy, salary, category breakup

---

## 1. Posts & Vacancies View

```
POSTS & VACANCIES — {exam.name}
[Example: APPSC Group 2 — 2025]
Tab: [Posts/Salary] active

  TOTAL VACANCIES: 897 (Notification: Oct 2025)

  POST-WISE BREAKDOWN  [from exam_post WHERE exam_id = this exam]
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Post Name         │ Dept           │ Total│ OC │ BC │SC │ST │EWS│PH │
  ├────────────────────┼────────────────┼──────┼────┼────┼───┼───┼───┼───┤
  │  Junior Assistant   │ Revenue        │  184 │ 62 │ 48 │32 │ 12│18 │12 │
  │  Junior Assistant   │ Panchayat Raj  │  142 │ 48 │ 36 │24 │ 10│14 │10 │
  │  Surveyor (Gr-III)  │ Survey & Land  │   96 │ 32 │ 24 │18 │  8│ 8 │ 6 │
  │  Revenue Inspector  │ Revenue        │   84 │ 28 │ 22 │14 │  6│ 8 │ 6 │
  │  Asst Comm Dev Off. │ Rural Dev      │   68 │ 24 │ 18 │10 │  4│ 6 │ 6 │
  │  Excise Sub Insp.   │ Prohibition    │   54 │ 18 │ 14 │ 8 │  4│ 6 │ 4 │
  │  Librarian Gr-III   │ Libraries      │   42 │ 14 │ 10 │ 8 │  4│ 4 │ 2 │
  │  + 14 more posts    │ Various        │  227 │    see full list       │
  ├────────────────────┴────────────────┴──────┴────┴────┴───┴───┴───┴───┤
  │  TOTAL                               │  897 │306 │220 │138│ 60│ 86 │52│
  └──────────────────────────────────────────────────────────────────────┘
  [Download vacancy table as PDF]  [View official notification ↗]
```

---

## 2. Post Detail + Salary

```
POST DETAIL — Revenue Inspector (APPSC Group 2 — 2025)
[User clicked a post row]

  POST PROFILE:
    Post:              Revenue Inspector
    Department:        Revenue Department, Government of Andhra Pradesh
    Pay scale:         ₹28,940 – ₹78,910 (Pay Level 12, APRC 2015)
    Grade pay:         ₹4,400
    Gross salary (est):₹42,000 – ₹48,000/month (including DA, HRA Vizag/Tirupati)
    Retirement age:    60 years
    Probation:         2 years

    WORK PROFILE:
      Nature:          Revenue collection, land records, mutation, survey
      Posting:         Mandal level — AP districts (13 districts)
      Transfer policy: Zonal — within revenue division
      Reporting to:    Tahsildar (Mandal Revenue Officer)
      Career path:     RI → Deputy Tahsildar → Tahsildar → RDO → Joint Collector

    VACANCY HISTORY:
      Year     │ Vacancies │ Cut-off (General)│ Applicants │ Ratio
      ─────────┼───────────┼──────────────────┼────────────┼───────
      2024–25  │    84     │  TBD (current)    │  4,28,000  │ 5,095:1
      2022–23  │    72     │  268/600          │  3,80,000  │ 5,278:1
      2019–20  │    64     │  254/600          │  2,96,000  │ 4,625:1
```

---

## 3. Data Model

```
exam_post {
  id,
  exam_id,              ← FK to exam
  post_name,
  department,
  pay_scale,
  grade_pay,
  estimated_gross_salary,
  posting_scope,        ← "state-wide" | "district" | "mandal" | "pan-india"
  posting_states[],     ← for central exams: possible posting states
  career_path,
  work_description,
  vacancy_total,
  vacancy_breakup: {    ← JSON: { OC, BC_A, BC_B, BC_C, BC_D, BC_E, SC, ST, EWS, PH }
  },
  vacancy_year,
}
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/{slug}/posts/` | All posts with vacancy breakup |
| 2 | `GET` | `/api/v1/exam/{slug}/posts/{post_id}/` | Post detail — salary, career, work profile |
| 3 | `GET` | `/api/v1/exam/{slug}/posts/{post_id}/history/` | Historical vacancy and cut-off for this post |

---

## 5. Business Rules

- Category-wise vacancy breakup (OC, BC-A through BC-E, SC, ST, EWS, PH) is specific to each state and exam; AP follows the AP State Reservation policy (OC 50%, BC 25%, SC 15%, ST 6%, EWS 10% — overlapping with roster points); Telangana follows a different reservation matrix; Central exams follow OBC 27%, SC 15%, ST 7.5%, EWS 10%; the `vacancy_breakup` JSON field supports any reservation structure — it does not assume fixed categories; when a new reservation category is introduced (e.g., EWS was added in 2019), the JSON field accommodates it without schema change
- Salary shown is the starting basic pay from the relevant pay commission; for AP state posts, it is the AP Revised Pay Commission (APRC) 2015 scales; for Telangana posts, it is the PRC (Telangana) 2015 scales; for Central posts, it is the 7th CPC; estimated gross salary includes approximate DA and HRA for a typical posting location but the UI explicitly notes "estimates vary by posting location"; misleading salary figures (inflating to attract aspirants) would violate Consumer Protection Act 2019 guidelines for educational services
- Career path information (RI → Deputy Tahsildar → Tahsildar → RDO → Joint Collector) is sourced from service rules published by the respective government (AP Government GO Ms. No. series for revenue cadre); the content team references official service rules, not coaching centre brochures; career paths that are speculative ("you could become a Collector in 20 years") are not published — only documented promotion channels from official service rules are shown
- Post profiles for police exams include physical standards (height, weight, chest, running) which vary by state, gender, and category; the `exam_post` record for AP Police SI includes `physical_requirements: { male: { height: 167cm, chest: 86/91cm, running_1600m: 6min20s }, female: { height: 152cm, running_800m: 3min50s } }`; this data is rendered in the post detail page without hardcoding police-specific logic into the template — the physical requirements JSON is just another rendered field
- Vacancy history (B-03 post detail section) enables aspirants to estimate competition for a specific post over time; if Revenue Inspector vacancies have been 64 → 72 → 84 across three cycles with increasing applicants, the competition ratio is rising but vacancies are also increasing; this trend data helps an aspirant decide whether to target this post vs another post in the same exam; the data is sourced from official notification PDFs of previous cycles, archived by the content team

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division B*
