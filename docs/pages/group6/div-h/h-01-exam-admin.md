# H-01 — Exam Record Management

> **URL:** `/admin/exam/exams/`
> **File:** `h-01-exam-admin.md`
> **Priority:** P1
> **Data:** `exam` table — CRUD for exam records; every change here propagates across the entire platform

---

## 1. Exam Admin List

```
EXAM MANAGEMENT — Admin
198 active exams | 24 draft/inactive

  SEARCH: [🔍 Search exam name...  ]
  FILTER: Type: [All ▼]  State: [All ▼]  Status: [Active ▼]

  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  Exam Name                │ Body   │ Type   │ State │ Active │ Updated     │ │
  ├───────────────────────────┼────────┼────────┼───────┼────────┼─────────────┤ │
  │  APPSC Group 2 2025       │ APPSC  │ State  │ AP    │ ✅     │ 30 Mar 2026 │ │
  │  SSC CGL 2026             │ SSC    │Central │ —     │ ✅     │ 2 Apr 2026  │ │
  │  TSPSC Group 1 2024       │ TSPSC  │ State  │ TS    │ ✅     │ 28 Mar 2026 │ │
  │  ONGC AEE 2026            │ ONGC   │ PSU    │ —     │ ✅     │ 25 Mar 2026 │ │
  │  [+ 194 more]             │        │        │       │        │             │ │
  └──────────────────────────────────────────────────────────────────────────────┘
  [+ Create New Exam]  [Import from CSV]  [Export all]
```

---

## 2. Exam Create / Edit Form

```
CREATE / EDIT EXAM

  ── BASIC INFO ──
  Name (English):       [ SSC CGL 2026                               ]
  Name (Regional):      [ ఎస్ఎస్సీ సీజీఎల్ 2026                     ]
  Slug:                 [ ssc-cgl-2026 ] (auto-generated, editable)
  Conducting Body:      [ SSC — Staff Selection Commission ▼ ]
  Type:                 [ Central ▼ ]
  State:                [ — (National) ▼ ]  (null for central exams)

  ── ELIGIBILITY ──
  Qualification:        [ Graduate ▼ ]
  Age min:              [ 18 ]   Age max: [ 32 ]
  Age relaxations:      [+ Add]
    OBC: +3 yrs | SC: +5 yrs | ST: +5 yrs | PH: +10 yrs | Ex-SM: +5 yrs
  Domicile required:    [ No ▼ ]
  Physical requirements:[ No ▼ ]

  ── DATES ──
  Notification date:    [ 2 Apr 2026 ]
  Application start:    [ 2 Apr 2026 ]   Application end: [ 30 Jun 2026 ]
  Exam dates:           [+ Add date]   [ Jul 2026 (Tier-I) ] [ Nov 2026 (Tier-II) ]
  Result dates:         [+ Add date]   (blank until available)

  ── EXAM DETAILS ──
  Vacancies:            [ 18517 ]   Vacancy year: [ 2026 ]
  Salary range:         [ ₹25,500 – ₹1,51,100 ]
  Posting scope:        [ Pan-India ▼ ]
  Language medium:      [ ✅ English  ✅ Hindi  ○ Telugu ]
  Tags:                 [ government-job, graduate, high-vacancies ]
  Active:               [ ✅ ]

  [Save Draft]  [Publish]  [Preview on portal]
```

---

## 3. Impact of Exam Record Changes

```
CHANGE IMPACT — What happens when you edit an exam record

  FIELD CHANGED           │ IMPACT
  ────────────────────────┼────────────────────────────────────────────
  application_end changed │ Calendar (C-02) auto-updates
                          │ Deadline alerts reschedule for subscribers
  exam_dates[] changed    │ Calendar updates; mock test schedule adjusts
  vacancies changed       │ Exam detail page (B-01) updates immediately
                          │ Cut-off predictor (F-03) recalculates
  qualification changed   │ Eligibility engine (D-01) recomputes for all users
                          │ Some users become eligible/ineligible ← significant
  stages[] changed        │ Mock tests may need restructuring ⚠️
                          │ Content team alerted for mock review
  active → false          │ Exam hidden from catalogue, calendar, search
                          │ Existing subscribers notified "exam deactivated"
  slug changed            │ ❌ PROHIBITED after publication (breaks URLs)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/admin/exam/exams/` | List all exams (admin view with drafts) |
| 2 | `POST` | `/api/v1/admin/exam/exams/` | Create new exam |
| 3 | `PUT` | `/api/v1/admin/exam/exams/{id}/` | Full update of exam record |
| 4 | `PATCH` | `/api/v1/admin/exam/exams/{id}/` | Partial update (e.g., just dates) |
| 5 | `DELETE` | `/api/v1/admin/exam/exams/{id}/` | Soft-delete (deactivate, preserve data) |

---

## 5. Business Rules

- The exam record is the single source of truth for every feature on the platform; changing `application_end` from "30 Jun" to "15 Jul" instantly updates the calendar, rescheduled deadline alerts, and the exam detail page — zero manual intervention required; this is the power of the data-driven architecture; however, it also means an incorrect edit (wrong date entered) propagates errors across the entire platform; every edit is validated (date format, logical consistency: `application_start < application_end < exam_dates[0]`) before save
- Slug immutability after publication is enforced at the system level; the slug `ssc-cgl-2026` becomes the permanent URL `/exam/ssc-cgl-2026/`; coaching institutes link to this URL, Google indexes it, aspirants bookmark it; changing the slug after publication breaks all inbound links and SEO ranking; the slug field is editable only while the exam is in "draft" status; after first publish, the slug field is locked; 301 redirects are set up only in exceptional cases (typo in slug discovered post-publish)
- Qualification changes are the most impactful eligibility-affecting edit; changing APPSC Group 2 from "Graduate" to "Post Graduate" would instantly make millions of users ineligible who were previously eligible; such changes are rare (conducting bodies rarely change qualification requirements) but when they happen, the system must: (a) recompute all users' eligible exam caches; (b) notify affected subscribers ("APPSC Group 2 eligibility has changed — check your eligibility"); (c) log the change in the audit trail with the admin's identity and timestamp
- The "Preview on portal" button lets the admin see exactly how the exam will appear to an aspirant before publishing; the preview renders the exam detail page (B-01) with all tabs (overview, syllabus, posts, pattern) using the current draft data; an admin who publishes without previewing may publish with missing data (no stages defined, no syllabus nodes) which creates a broken aspirant experience; the publish button checks for required fields and warns if critical data is missing
- Deactivation (active → false) is a soft delete; the exam record, all associated data (mocks, questions, cut-offs, notifications), and subscriber lists are preserved; the exam is simply hidden from the public catalogue, calendar, and search; it can be reactivated at any time; hard deletion is not supported — once an exam has been taken by even one user (mock attempts exist), its data must be preserved for analytics and the user's mock history

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division H*
