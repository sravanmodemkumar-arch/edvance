# B-01 — Exam Detail Page (Master Template)

> **URL:** `/exam/{exam-slug}/` — one URL pattern, renders any exam
> **File:** `b-01-exam-detail.md`
> **Priority:** P1
> **Data:** All `exam` fields + `conducting_body` + `stages[]` + `syllabus_nodes[]` + `notifications[]` + `cut_offs[]`

---

## 1. Template Layout

```
EXAM DETAIL — Dynamic Template
URL: /exam/{slug}/  →  resolves to exam record from DB
Language: auto-detected from user preference OR exam.language_medium[0]

  ┌──────────────────────────────────────────────────────────────────────┐
  │  HEADER (rendered from exam + conducting_body)                       │
  │  ┌────────┐                                                          │
  │  │[CB Logo]│  {exam.name}                        {exam.type badge}   │
  │  └────────┘  {conducting_body.name}              {exam.state_code}   │
  │              Website: {conducting_body.website}                       │
  │                                                                      │
  │  STATUS RIBBON:                                                      │
  │  {computed from application_start, application_end, exam_dates[]}    │
  │  Example: 🔴 Application Open — Apply by {application_end}           │
  │  Example: 🟡 Exam scheduled — {exam_dates[0]}                       │
  │  Example: ✅ Results declared — {result_dates[latest]}                │
  │                                                                      │
  │  [Apply Now ↗]  [Take Mock]  [Save to My Exams]  [🔔 Set Alert]     │
  │  [Share]  [Compare with another exam]                                │
  └──────────────────────────────────────────────────────────────────────┘

  TAB NAVIGATION:
  ┌─────────┬──────────┬────────────┬──────────┬──────────┬──────────┐
  │Overview │ Syllabus │Posts/Salary│ Pattern  │ Cut-offs │ History  │
  │(B-01)   │ (B-02)   │ (B-03)     │ (B-04)   │ (F-02)   │ (B-05)   │
  └─────────┴──────────┴────────────┴──────────┴──────────┴──────────┘
```

---

## 2. Overview Tab (Default)

```
OVERVIEW — {exam.name}
[Example render: APPSC Group 2 — 2025]

  AT A GLANCE  [all fields from exam record]
  ┌─────────────────────┬──────────────────────────────────────────────┐
  │  Conducting Body     │  {conducting_body.name} ({abbreviation})    │
  │  Level               │  {exam.type} — {state_name or "National"}  │
  │  Qualification       │  {exam.qualification} (rendered as label)   │
  │  Age Limit           │  {age_min}–{age_max} years (General)       │
  │  Age Relaxations     │  {for each r in age_relaxations:            │
  │                      │    r.category: +r.extra_years years}        │
  │  Total Vacancies     │  {exam.vacancies} ({vacancy_year})          │
  │  Salary Range        │  {exam.salary_range}                        │
  │  Posting Scope       │  {exam.posting_scope}                       │
  │  Exam Stages         │  {stages[].name joined by " → "}           │
  │  Language Medium     │  {language_medium[] rendered as tags}       │
  │  Negative Marking    │  {from stages[].negative_marking}          │
  │  Domicile Required   │  {exam.domicile_required or "None"}         │
  └─────────────────────┴──────────────────────────────────────────────┘

  TIMELINE  [rendered from exam date fields — computed status per stage]
  ┌──────────────────────────────────────────────────────────────────────┐
  │  ● Notification: {notification_date}              ✅ Released        │
  │  ● Application:  {application_start}–{application_end}  🔴 Open     │
  │  ● Admit Card:   {admit_card_date or "TBA"}       ⏳ Pending        │
  │  ○ {stages[0].name}: {exam_dates[0] or "TBA"}     📅 Upcoming      │
  │  ○ {stages[1].name}: {exam_dates[1] or "TBA"}     📅 Upcoming      │
  │  ○ Results:      {result_dates[0] or "TBA"}        📅 Upcoming      │
  └──────────────────────────────────────────────────────────────────────┘

  PREPARATION RESOURCES (from exam_id joins)
    Mock tests available:    {mock_count} mocks  [View all →]
    Study material:          {material_count} resources  [View all →]
    Previous year papers:    {pyq_count} papers  [View all →]
    Aspirants on EduForge:   {aspirant_count formatted}
    Community threads:       {thread_count} discussions  [Join →]

  ELIGIBILITY QUICK CHECK  [rendered inline from exam rules + user profile]
    {if user logged in:}
      Based on your profile: ✅ Eligible / ❌ Not eligible (reason: {})
    {if guest:}
      [Check your eligibility →] (link to D-01)
```

---

## 3. How the Template Resolves

```
RENDERING FLOW — Zero Hardcoding

  REQUEST: GET /exam/tspsc-group-1-2024/

  STEP 1: Resolve slug
    SELECT * FROM exam WHERE slug = 'tspsc-group-1-2024' AND active = true
    → Returns exam record (id=482, name="TSPSC Group 1 — 2024", …)

  STEP 2: Load related data
    SELECT * FROM conducting_body WHERE id = exam.conducting_body_id
    SELECT * FROM exam_stage WHERE exam_id = 482 ORDER BY sequence
    SELECT * FROM syllabus_node WHERE exam_id = 482
    SELECT * FROM exam_notification WHERE exam_id = 482 ORDER BY date DESC
    SELECT * FROM cut_off WHERE exam_id = 482
    SELECT COUNT(*) FROM mock_test WHERE exam_id = 482
    SELECT COUNT(*) FROM user_exam_profile WHERE exam_id = 482

  STEP 3: Render template
    Template receives: { exam, body, stages, syllabus, notifications, cutoffs, counts }
    Every field is from DB — template has zero exam-specific logic
    If a field is null (e.g., admit_card_date), it renders "TBA"
    If stages[] has 2 items, 2 timeline nodes appear; if 5, then 5 appear

  RESULT:
    Same template renders TSPSC Group 1, SSC CGL, ONGC AEE, AP DSC, NEET, CLAT
    — any exam, any type, any state, any number of stages
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/{slug}/` | Full exam detail (overview tab data) |
| 2 | `GET` | `/api/v1/exam/{slug}/timeline/` | Status-annotated timeline |
| 3 | `GET` | `/api/v1/exam/{slug}/resources/` | Count of mocks, material, PYQs, aspirants |
| 4 | `GET` | `/api/v1/exam/{slug}/eligibility/?uid={uid}` | Eligibility check for a user |

---

## 5. Business Rules

- The exam detail page URL (`/exam/{slug}/`) is the single most important SEO page in the platform; "APPSC Group 2 2025" searches should land here; the slug is human-readable (`appsc-group-2-2025`) and immutable once created — changing slugs breaks search engine indexing and inbound links from coaching institutes; if an exam name changes slightly ("TGPSC" replaces "TSPSC"), the slug remains the same and the rendered name updates from the DB; 301 redirects are set up from any old slug to the current one
- The status ribbon computation is the heart of the page's urgency signalling; the status is computed from date fields, never stored; this guarantees correctness — an "Application Open" ribbon automatically flips to "Application Closed" the day after `application_end` with zero admin intervention; the content team only needs to enter correct dates; the system handles state transitions automatically; if `application_end` is null, the ribbon shows "Dates TBA" instead of showing a misleading "Closed"
- The "At a Glance" table renders every field from the exam record; fields that are null are either hidden (if the row is irrelevant — e.g., `domicile_required` for a national exam) or shown as "TBA"; the template uses conditional rendering: `{if exam.domicile_required: show row}` — not a hardcoded list of fields per exam type; when a new field is added to the exam model (e.g., `physical_test_required` for police exams), it appears in the template once the template adds that row's conditional render — one template change, all police exams show it
- Age relaxation rendering iterates over `exam.age_relaxations[]` which is a JSON array; each entry has `{ category, extra_years }`; if APPSC Group 2 has `[{OBC, 3}, {SC/ST, 5}, {PH, 10}, {Ex-Serviceman, 5}]`, all four are rendered; if SSC CGL has only `[{OBC, 3}, {SC/ST, 5}]`, only two are rendered; the template does not assume which categories exist — it renders whatever the DB record contains; this supports exams with unique relaxation categories (e.g., Telangana state exams with a "Telangana domicile + OBC" combined relaxation)
- The "Eligibility Quick Check" for logged-in users runs the eligibility engine (D-01) in real time against the user's profile and this exam's rules; it considers: age (user DOB vs exam age limits with category relaxation), qualification (user's highest qualification vs exam requirement), domicile (user's state vs exam's domicile requirement), and any special conditions (physical standards for police exams, subject prerequisites for GATE); the check result (eligible/not eligible with reason) is surfaced directly on the exam page without the user having to navigate to a separate eligibility page

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division B*
