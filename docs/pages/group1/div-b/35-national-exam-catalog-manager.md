# B-35 — National Exam Catalog Manager

## 1. Page Metadata

| Field | Value |
|---|---|
| **Route** | `GET /product/exam-catalog/` |
| **Django View** | `ExamCatalogListView` · `ExamCatalogDetailView` (`/product/exam-catalog/<exam_id>/`) |
| **Template** | `portal_base_dark.html` → `product/exam_catalog.html` |
| **Primary Role** | PM Exam Domains (Role 6, Level 3) |
| **Also Accessible** | Platform Admin (10) · Analytics Manager (42, read only) |
| **Priority** | P1 |
| **Status** | ⬜ Not started |
| **Module Reference** | Module 49 — National Exam Catalog (Group 6) |
| **Polling** | No auto-poll (catalog data is updated manually, not streaming) |

---

## 2. Purpose & Business Logic

Module 49 defines the platform's comprehensive **National Exam Catalog** — 300+ competitive examinations covering central government, state government, entrance tests, banking, railways, defence, teaching, and professional certifications. This catalog is what millions of competitive exam aspirants browse to find which exams they're eligible for, understand exam patterns, check cutoffs, and start preparation.

**The catalog management problem:**
- 300+ exams, each with multiple stages, papers, cutoff years, salary grades
- Exam dates change every year (notification, application, hall ticket, exam, result)
- Cutoffs change every year × category (UR/OBC/SC/ST/EWS/PH) × post
- Salary pay-level data follows 7th Pay Commission but changes with promotions/revisions
- State PSC exam patterns differ significantly across 30 states
- New exams are announced (e.g. CUET launched 2022), old exams discontinued
- Preparation roadmaps need to link to specific test series in Module 22 and syllabus nodes in Module 15

**Who uses this catalog from the student side:**
- Students on the EduForge app browse exam catalog (Group 6: Competitive Exam Aspirants)
- They check eligibility (age, education qualification, nationality)
- They track application dates and receive smart alerts
- They see cutoff history to gauge their chances
- They start a test series linked to this exam

**Who manages this catalog — PM Exam Domains (Role 6)** is responsible for:
- Creating and updating exam entries
- Setting eligibility criteria
- Entering cutoff history data (manually or via CSV import)
- Linking exams to test series and syllabus nodes
- Managing the exam date lifecycle each year
- Archiving discontinued exams

---

## 3. User Roles & Access

| Role | Access |
|---|---|
| PM Exam Domains (6) | Full CRUD — create/edit/archive exams · manage cutoffs · link test series · set dates |
| Platform Admin (10) | Full — same as PM Exam Domains + hard delete on exams with 0 enrollments |
| Analytics Manager (42) | Read-only — can see enrollment counts and preparation roadmap performance |

---

## 4. Page Layout

### 4.1 Header

```
Product / National Exam Catalog Manager
[+ Add Exam]    [Bulk Import Exams CSV]    [Export Catalog CSV]
```

---

### 4.2 KPI Strip (4 tiles)

| Tile | Value | Logic |
|---|---|---|
| Total Active Exams | Count `status=ACTIVE` | Neutral |
| Exams With Upcoming Dates | Count where any date in next 60 days | Green if > 0; highlights active season |
| Exams Needing Update | Count where `last_updated_at < today - 90d` | Amber if > 0 (stale catalog entries) |
| Student Enrollments Linked | Total active applications tracked across all exams | Neutral |

---

### 4.3 Filter Bar

```
[Search exam name or code...] [Category ▾] [Conducting Body ▾] [State ▾] [Status ▾] [Level ▾]
```

Filters:
- **Category**: Civil Services · SSC · Banking · Railways · Defence · Teaching · Insurance · Medical · Technical · Higher Education Entrance · Law · Management · State Government
- **Conducting Body**: UPSC · SSC · IBPS · SBI · RRB · NDA · CTET/CBSE · NTA · State PSC (dropdown per state)
- **State** (for state exams): All States + 30 state options
- **Level**: Central Government · State Government · National Entrance · Others
- **Status**: Active · Discontinued · Upcoming (announced but not yet conducting) · All

---

### 4.4 Exam Cards Grid

Default: list view (examinations are text-heavy). Card view toggle available.

**List row format:**

| Exam Name | Category | Conducting Body | State | Posts | Exam Date | Cutoffs Updated | Enrollments | Status | Actions |
|---|---|---|---|---|---|---|---|---|---|
| UPSC Civil Services 2026 | Civil Services | UPSC | National | 1056 | May 2026 | 2026-01-15 | 12,340 | ● Active | [View] [Edit] |
| APPSC Group 1 2025 | State PSC | APPSC | Andhra Pradesh | 168 | Dec 2025 | 2025-12-01 | 8,920 | ● Active | [View] [Edit] |
| SSC CGL 2026 | SSC | SSC | National | 17,727 | Sep 2026 | — | 45,200 | ⬜ Dates Pending | [View] [Edit] |

- **Cutoffs Updated**: date when cutoff data was last entered — amber if > 6 months old
- **Enrollments**: students who added this exam to their tracker on EduForge — shows platform engagement
- Status dot: green = Active · grey = Discontinued · blue = Upcoming

---

## 5. Exam Detail Sub-Page — `/product/exam-catalog/<exam_id>/`

### 5.1 Page Header

```
← Back to Exam Catalog
UPSC Civil Services (IAS/IPS/IFS/IRS)
[National] [Civil Services] [UPSC] [2026 Cycle] [● Active]
[Edit Exam Metadata]   [Archive Exam]   [Copy to New Cycle]
```

### 5.2 Tabs

**Tab 1: Overview & Eligibility**
**Tab 2: Stages & Papers**
**Tab 3: Exam Dates**
**Tab 4: Cutoff History**
**Tab 5: Salary & Career**
**Tab 6: Preparation Resources**
**Tab 7: Analytics**
**Tab 8: Audit Log**

---

### Tab 1: Overview & Eligibility

**Basic metadata:**

| Field | Value |
|---|---|
| Exam Code | `UPSC_CSE` |
| Family | UPSC Civil Services |
| Full Name | Union Public Service Commission Civil Services Examination |
| Cycle Year | 2026 |
| Conducting Body | Union Public Service Commission |
| Level | Central Government |
| Category | Civil Services |
| Post Names | IAS · IPS · IFS · IRS · IPoS · IA&AS · IRAS · IDES · IRTS · IFS(Forests) · IDSE · IRSEE · IISaS · IRSME · IRSS · CSAT (listed individually) |
| Total Posts (2026) | 979 (UR: 473 · OBC: 263 · SC: 148 · ST: 71 · EWS: 98 + PH sub-quota) |
| Exam Mode | Offline (OMR-based Prelims) · Offline (Descriptive Mains) · In-Person (Interview) |

**Eligibility criteria:**

| Criterion | Value |
|---|---|
| Minimum Age | 21 years |
| Maximum Age | 32 (UR) · 35 (OBC) · 37 (SC/ST) · 42 (PH) · (Ex-servicemen relaxation) |
| Nationality | Indian citizen (certain posts accept Nepal/Bhutan/Tibetan refugee/PIO) |
| Educational Qualification | Bachelor's degree from recognized university (any discipline) |
| Attempts Limit | 6 (UR) · 9 (OBC) · Unlimited (SC/ST) · 9 (EWS) |
| Other Restrictions | Not already appointed to an IAS/IPS service through competitive exam |

**Eligibility Checker** (computed field — not manually entered):
Linked to student profile in Group 6 portal. When student views this exam, system auto-computes:
- Age eligibility: ✅ / ❌ / ⚠️ borderline
- Qualification: ✅ / ❌ / ⚠️ (final year student)
- Attempts remaining: shows remaining count if student has attempted before

---

### Tab 2: Stages & Papers

UPSC CSE has 3 stages with multiple papers:

**Stage table:**

| Stage # | Stage Name | Mode | Duration | Qualifying/Ranking | Papers |
|---|---|---|---|---|---|
| 1 | Preliminary (Prelims) | Offline OMR | 2 hours each | Qualifying (Prelims score not counted in final merit) | 2 |
| 2 | Mains | Offline Written | 3 hours each | Ranking (counts 1750/2025 marks) | 7 (4 GS + 2 Optional + Essay) |
| 3 | Personality Test (Interview) | In-Person | Variable | Ranking (275 marks) | 1 |

**Paper detail (expandable per stage):**

| Paper Code | Paper Name | Marks | Questions | Sections | Negative Marking | Linked Syllabus |
|---|---|---|---|---|---|---|
| PRELIMS_GS1 | GS Paper 1 | 200 | 100 MCQs | Current Events · History · Geography · Polity · Economy · Science | 1/3 per wrong | Link → B-10 Syllabus |
| PRELIMS_CSAT | CSAT Paper 2 | 200 | 80 MCQs | Comprehension · Reasoning · Maths | 1/3 per wrong | Link → B-10 Syllabus |
| MAINS_ESSAY | Essay Paper | 250 | 2 Essays (choose 2 from 4) | — | No | — |
| MAINS_GS1 | GS Paper I | 250 | — | History · Heritage · Geography of World/India · Society | No | Link → B-10 Syllabus |

**[Link to Test Series]** button per paper: opens a picker to link to one or more test series from B-11 (Test Series Manager) — this is how students find relevant practice material from the exam detail page.

---

### Tab 3: Exam Dates

Timeline of all events for the current exam cycle (2026 cycle shown by default; dropdown to view past cycles):

```
Exam Dates — 2026 Cycle                                    [Previous cycles ▾]

  ● Notification Released              01 Feb 2026    ✅ Confirmed
  ● Application Opens                  01 Feb 2026    ✅ Confirmed
  ● Application Closes (without late)  21 Feb 2026    ✅ Confirmed
  ● Application Closes (with late fee) 27 Feb 2026    ✅ Confirmed
  ● Application Withdrawal             04–13 Mar 2026 ✅ Confirmed
  ◌ Admit Card Release                 —              ⬜ Not Set
  ◌ Prelims Exam Date                  25 May 2026    ⬜ Tentative
  ◌ Prelims Result                     Jul 2026       ⬜ Tentative
  ◌ Mains Application                  Jul 2026       ⬜ Not Set
  ◌ Mains Exam                         Sep–Oct 2026   ⬜ Tentative
  ◌ Interview (PT) Round               Feb–Apr 2027   ⬜ Tentative
  ◌ Final Result                       May 2027       ⬜ Tentative
```

**Date status**: Confirmed (officially announced) · Tentative (expected but not official) · Not Set (unknown)

**Student Calendar Integration**: When `status=Confirmed AND date ≤ today+60d`, date appears in student's exam calendar with auto-reminder (30d, 7d, 1d before each event). Students who have "Interested" or "Applied" status for this exam receive push notifications.

**[+ Add Date Event]** — form: event name · date · status (Confirmed/Tentative) · notes.
**[Set Smart Alert Threshold]** — configure how far in advance to notify students (default: 30 days for application open, 7 days for admit card, 2 days before exam).

---

### Tab 4: Cutoff History

Seven years of cutoff data across all categories and posts.

**Year selector**: [2019] [2020] [2021] [2022] [2023] [2024] [2025] (radio buttons)

**Cutoff table (per selected year):**

| Post | UR | OBC | SC | ST | EWS | PH-OH | PH-VH | PH-HH |
|---|---|---|---|---|---|---|---|---|
| IAS | 980 | 957 | 933 | 916 | 965 | 908 | — | — |
| IPS | 942 | 925 | 901 | 884 | 930 | 875 | — | — |
| IFS (Foreign) | 930 | 912 | 889 | 872 | 918 | — | — | — |
| IRS (IT) | 895 | 878 | 855 | 838 | 880 | 842 | — | — |

**Marks are out of 2025 (Mains 1750 + Interview 275).**

**[Import Cutoffs CSV]** — CSV template: `year, post_name, ur, obc, sc, st, ews, ph_oh, ph_vh, ph_hh, total_marks_out_of`. Validation: all numeric values ≤ total marks.

**Prelims cutoff (separate section):**
| Year | UR | OBC | SC | ST | EWS | CSAT Min (qualifying) |
|---|---|---|---|---|---|---|
| 2025 | 100.16 | 93.12 | 82.48 | 77.04 | 97.64 | 33% |

**Trend chart** (Chart.js line): UR cutoff trend 2019–2025. Helps students see whether cutoffs are rising/falling. Toggle per category.

---

### Tab 5: Salary & Career

Pay-level data per post (7th Pay Commission):

| Post | Pay Level | Basic Pay | HRA (X city) | TA | Gross (approx.) | Cadre |
|---|---|---|---|---|---|---|
| IAS (SDM) | Level 10 | ₹56,100 | ₹22,440 | ₹3,600 | ₹1,00,000+ | AGMUT / State cadres |
| IAS (Secy to GoI) | Level 17 | ₹2,25,000 (HAG+) | ₹90,000 | ₹7,500 | ₹3,50,000+ | GoI |
| IPS (DSP) | Level 10 | ₹56,100 | ₹22,440 | — | ₹95,000+ | State police / CRPF |
| IRS (Asst Commissioner) | Level 10 | ₹56,100 | ₹22,440 | ₹3,600 | ₹98,000+ | Income Tax / GST |

**Career Progression ladder** per post (visual timeline):
```
IAS Career Path:
SDM (Yr 1-5) → District Collector (Yr 6-12) → Joint Secretary GoI (Yr 15-20)
→ Additional Secretary (Yr 22-27) → Secretary to GoI (Yr 28-34) → Cabinet Secretary (apex)
```

**Benefits panel**: Central Government Health Scheme · LTC · Housing allotment · Vehicle allowance · Security cover · Staff on deputation

---

### Tab 6: Preparation Resources

Cross-links to platform content for this exam:

**Linked Test Series (from B-11):**
| Series Name | Total Tests | Enrolled Students | Series Status |
|---|---|---|---|
| UPSC Prelims GS 2026 — Full Test Series | 35 | 12,340 | Active |
| UPSC CSAT Crash Course — 15 Tests | 15 | 8,920 | Active |
| UPSC Mains GS Essay Practice | 8 | 4,100 | Active |

**[Link New Series]** — opens B-11 series picker (PM Exam Domains role)

**Syllabus Coverage (linked to B-10 Syllabus Builder):**
For each paper: % of syllabus topics with ≥ 10 published practice questions.

| Paper | Syllabus Topics | Topics Covered | Coverage % |
|---|---|---|---|
| GS Paper 1 (History) | 45 | 38 | 84% |
| GS Paper 1 (Geography) | 32 | 28 | 87% |
| GS Paper 2 (Polity) | 28 | 25 | 89% |
| CSAT (Reasoning) | 20 | 18 | 90% |

**Preparation Roadmap config:**
PM Exam Domains can configure a standard study plan timeline (e.g. "12-month UPSC preparation roadmap"):
- Month 1–3: NCERT foundation
- Month 4–6: Standard reference books per subject
- Month 7–9: Current affairs + previous year papers
- Month 10–11: Full mock tests
- Month 12: Revision + final mocks

Roadmap appears in student's learning path (Module 47).

**Previous Year Questions (PYQ) count:**
| Year | GS1 | GS2 | GS3 | GS4 | CSAT | Total |
|---|---|---|---|---|---|---|
| 2025 | 100 | 80 | 100 | 100 | 80 | 460 |
| 2024 | 100 | 80 | 100 | 100 | 80 | 460 |

---

### Tab 7: Analytics

Read-only. Analytics Manager (42) and PM Exam Domains (6) can view.

**Platform engagement metrics:**
- Total students who added this exam to tracker: 12,340
- Students currently active (attempted ≥ 1 test series question in last 30d): 8,920
- Average score in linked test series: 58.3% (GS1) · 64.1% (CSAT)
- Score distribution histogram (anonymous): shows where platform students rank relative to expected cutoff
- Peak engagement periods: Sep–Nov (Prelims prep), Jun–Aug (Mains prep)

**Cutoff Comparison widget:**
"Based on platform mock test scores — estimated % of EduForge students above 2025 Prelims cutoff: 34%"
(Useful for PM Exam Domains to assess exam difficulty calibration)

---

### Tab 8: Audit Log

All changes to this exam's data: who changed what, when.

---

## 6. Create/Edit Exam Drawer (720px)

**Step 1 — Basic Info:**
- Exam Code (UPPERCASE, unique: `UPSC_CSE`, `SSC_CGL`, `APPSC_GRP1`)
- Exam Family (e.g. "UPSC Civil Services" — groups all years)
- Full Name
- Category (multi-select from master list)
- Conducting Body
- Level: Central / State / National Entrance / Others
- State (for state exams)
- Exam Mode: Online · Offline · Hybrid
- Total Posts (editable per cycle)

**Step 2 — Stages:**
Add stages: Stage Name · Mode · Duration · Total Marks · Is Qualifying Only (Yes/No)
Per stage: add papers with marks, question count, sections config

**Step 3 — Eligibility:**
- Minimum Age · Maximum Age (per category multi-entry table)
- Qualification Required
- Nationality requirement
- Attempts limit per category

**Step 4 — Links:**
- Link to Test Series (multi-select from B-11)
- Link to Syllabus (auto-suggests based on exam category)

**[Save & Add Dates →]** opens exam dates tab after save.

---

## 7. Bulk Import

CSV format for importing multiple exams or updating cutoffs:

**Exams import CSV columns:**
`exam_code, family, full_name, category, conducting_body, level, state, exam_mode, total_posts, min_age, max_age_ur, max_age_obc, max_age_sc_st, qualification, attempts_ur, attempts_obc`

**Cutoff import CSV columns:**
`exam_code, year, post_name, ur, obc, sc, st, ews, ph_oh, ph_vh, ph_hh, total_marks`

**Dates import CSV columns:**
`exam_code, cycle_year, event_name, event_date, status`

---

## 8. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/product/exam-catalog/` | List exams (paginated, filterable) |
| POST | `/api/v1/product/exam-catalog/` | Create exam |
| GET | `/api/v1/product/exam-catalog/<id>/` | Exam detail |
| PATCH | `/api/v1/product/exam-catalog/<id>/` | Update exam metadata |
| POST | `/api/v1/product/exam-catalog/<id>/archive/` | Archive |
| POST | `/api/v1/product/exam-catalog/<id>/copy-cycle/` | Copy exam to new cycle year |
| GET | `/api/v1/product/exam-catalog/<id>/stages/` | Stages + papers |
| POST | `/api/v1/product/exam-catalog/<id>/stages/` | Add stage |
| POST | `/api/v1/product/exam-catalog/<id>/dates/` | Add date event |
| PATCH | `/api/v1/product/exam-catalog/<id>/dates/<did>/` | Update date |
| GET | `/api/v1/product/exam-catalog/<id>/cutoffs/` | Cutoff history |
| POST | `/api/v1/product/exam-catalog/<id>/cutoffs/` | Add cutoff row |
| POST | `/api/v1/product/exam-catalog/<id>/cutoffs/bulk-import/` | Bulk cutoff CSV |
| GET | `/api/v1/product/exam-catalog/<id>/salary/` | Salary table |
| PATCH | `/api/v1/product/exam-catalog/<id>/salary/` | Update salary |
| POST | `/api/v1/product/exam-catalog/<id>/test-series/link/` | Link test series |
| DELETE | `/api/v1/product/exam-catalog/<id>/test-series/<sid>/` | Unlink series |
| GET | `/api/v1/product/exam-catalog/<id>/analytics/` | Engagement metrics |
| POST | `/api/v1/product/exam-catalog/bulk-import/` | Bulk exam import |
| GET | `/api/v1/product/exam-catalog/export/` | Export catalog CSV |

---

## 9. HTMX Patterns

```
Exam list (page load + filter change)
  → hx-get="/product/exam-catalog/?{filters}" hx-target="#exam-list" hx-swap="innerHTML"
  → hx-trigger="change from:.filter-input, keyup[delay=300ms] from:#search-input"

Tab switching on detail page
  → hx-get="/product/exam-catalog/<id>/tab/<tab_name>/" hx-target="#exam-tab-content"
    hx-swap="innerHTML" hx-indicator="#tab-loader"

Copy to New Cycle
  → hx-post="/api/v1/product/exam-catalog/<id>/copy-cycle/" hx-vals="js:{cycle_year: ...}"
  → On success: redirect to new cycle's detail page

Cutoff trend chart data
  → hx-get="/api/v1/product/exam-catalog/<id>/cutoffs/?years=7" hx-target="#cutoff-chart-data"
  → JS picks up data attribute and renders Chart.js line chart

Stale exams alert (KPI tile)
  → hx-get="/product/exam-catalog/kpi/" hx-target="#catalog-kpi" hx-swap="innerHTML"
  → hx-trigger="every 600s" (10-min refresh — catalog data rarely changes mid-session)
```

---

## 10. Database Models

```python
class ExamFamily(models.Model):
    code        = models.CharField(max_length=20, unique=True)  # UPSC_CS, SSC, RRB, IBPS
    name        = models.CharField(max_length=100)  # UPSC Civil Services, Staff Selection Commission
    category    = models.CharField(max_length=50)  # Civil Services / SSC / Banking / Railways...
    is_active   = models.BooleanField(default=True)

class ExamCatalog(models.Model):
    exam_code   = models.CharField(max_length=30, unique=True)  # UPSC_CSE_2026
    family      = models.ForeignKey(ExamFamily, on_delete=models.PROTECT)
    full_name   = models.CharField(max_length=200)
    cycle_year  = models.PositiveSmallIntegerField()  # 2026
    conducting_body = models.CharField(max_length=100)
    level       = models.CharField(max_length=20)  # CENTRAL/STATE/NATIONAL_ENTRANCE/OTHER
    state       = models.CharField(max_length=50, blank=True)  # For state exams
    exam_mode   = models.CharField(max_length=20)  # ONLINE/OFFLINE/HYBRID
    total_posts = models.PositiveIntegerField(default=0)
    status      = models.CharField(max_length=20, default='ACTIVE')  # ACTIVE/DISCONTINUED/UPCOMING
    last_updated_at = models.DateTimeField(auto_now=True)
    updated_by  = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at  = models.DateTimeField(auto_now_add=True)

class ExamStage(models.Model):
    exam        = models.ForeignKey(ExamCatalog, related_name='stages', on_delete=models.PROTECT)
    stage_number = models.PositiveSmallIntegerField()
    stage_name  = models.CharField(max_length=100)  # Preliminary / Mains / Interview
    mode        = models.CharField(max_length=20)  # OFFLINE_OMR/OFFLINE_WRITTEN/ONLINE/IN_PERSON
    is_qualifying_only = models.BooleanField(default=False)
    total_marks = models.PositiveSmallIntegerField(default=0)

class ExamPaper(models.Model):
    stage       = models.ForeignKey(ExamStage, related_name='papers', on_delete=models.PROTECT)
    paper_code  = models.CharField(max_length=30)  # PRELIMS_GS1, MAINS_GS1
    paper_name  = models.CharField(max_length=100)
    total_marks = models.PositiveSmallIntegerField()
    total_questions = models.PositiveSmallIntegerField(default=0)
    negative_marking_factor = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.33'))
    duration_minutes = models.PositiveSmallIntegerField(default=120)
    syllabus_node_ids = models.JSONField(default=list)  # linked syllabus nodes from B-10

class ExamEligibility(models.Model):
    exam        = models.ForeignKey(ExamCatalog, related_name='eligibility', on_delete=models.PROTECT)
    min_age     = models.PositiveSmallIntegerField()
    max_age_ur  = models.PositiveSmallIntegerField()
    max_age_obc = models.PositiveSmallIntegerField()
    max_age_sc_st = models.PositiveSmallIntegerField()
    max_age_ews = models.PositiveSmallIntegerField(null=True)
    max_age_ph  = models.PositiveSmallIntegerField(null=True)
    max_age_ex_serviceman = models.PositiveSmallIntegerField(null=True)
    qualification = models.TextField()  # Free text describing educational qualification
    nationality = models.TextField()
    attempts_ur = models.PositiveSmallIntegerField(null=True)  # null = unlimited
    attempts_obc = models.PositiveSmallIntegerField(null=True)
    attempts_sc_st = models.PositiveSmallIntegerField(null=True)
    attempts_ews = models.PositiveSmallIntegerField(null=True)

class ExamDateEvent(models.Model):
    exam        = models.ForeignKey(ExamCatalog, related_name='dates', on_delete=models.PROTECT)
    event_name  = models.CharField(max_length=100)
    event_type  = models.CharField(max_length=30)  # NOTIFICATION/APP_OPEN/APP_CLOSE/ADMIT_CARD/EXAM/RESULT
    event_date  = models.DateField(null=True)
    end_date    = models.DateField(null=True)  # For date ranges
    status      = models.CharField(max_length=15, default='TENTATIVE')  # CONFIRMED/TENTATIVE/NOT_SET
    notes       = models.CharField(max_length=200, blank=True)
    sort_order  = models.PositiveSmallIntegerField(default=0)
    student_alert_days_before = models.PositiveSmallIntegerField(default=7)

class ExamCutoff(models.Model):
    exam        = models.ForeignKey(ExamCatalog, related_name='cutoffs', on_delete=models.PROTECT)
    year        = models.PositiveSmallIntegerField()
    post_name   = models.CharField(max_length=100)
    cutoff_type = models.CharField(max_length=20, default='FINAL')  # PRELIMS / MAINS / FINAL
    total_marks = models.PositiveSmallIntegerField()  # e.g. 2025 for UPSC Mains+Interview
    ur          = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    obc         = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    sc          = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    st          = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    ews         = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    ph_oh       = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    ph_vh       = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    ph_hh       = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    ex_sm       = models.DecimalField(max_digits=6, decimal_places=2, null=True)

class ExamSalaryData(models.Model):
    exam        = models.ForeignKey(ExamCatalog, related_name='salary_data', on_delete=models.PROTECT)
    post_name   = models.CharField(max_length=100)
    pay_level   = models.CharField(max_length=10)  # Level 10, Level 17, HAG+
    basic_pay   = models.PositiveIntegerField()  # in paise for precision
    hra_x_city_pct = models.PositiveSmallIntegerField(default=27)  # % of basic
    career_progression = models.JSONField(default=list)  # [{years: "0-5", designation: "SDM"}, ...]
    pay_commission = models.CharField(max_length=10, default='7CPC')

class ExamTestSeriesLink(models.Model):
    exam        = models.ForeignKey(ExamCatalog, on_delete=models.CASCADE)
    test_series_id = models.PositiveIntegerField()  # FK to test_series in Module 22
    linked_by   = models.ForeignKey(User, on_delete=models.PROTECT)
    linked_at   = models.DateTimeField(auto_now_add=True)
```

**Cache strategy:**
- Exam list: `product:exam_catalog:list:{filters_hash}` · TTL 10 min
- Exam detail: `product:exam_catalog:{exam_id}` · TTL 30 min
- Cutoff data: `product:exam_catalog:{exam_id}:cutoffs` · TTL 1 hour (changes infrequently)
- Student-facing exam catalog (Group 6 portal): `public:exam_catalog:list` · TTL 30 min · separate cache key from management view

---

## 11. Background Tasks

| Task | Schedule | Purpose |
|---|---|---|
| `flag_stale_exam_entries` | Daily 09:00 IST | Mark entries with `last_updated_at < today - 90d` — shows in KPI tile "Needs Update" |
| `send_upcoming_exam_date_alerts` | Daily 07:00 IST | For `ExamDateEvent` rows where `event_date = today + student_alert_days_before AND status = CONFIRMED` → send push notification to all students who tracked this exam via Notification Hub |
| `check_exam_date_confirmation` | Weekly Mon 09:00 IST | For `status=TENTATIVE AND event_date < today + 30d` → alert PM Exam Domains in-app: "N exam dates tentative with <30 days — confirm or update" |
| `sync_exam_catalog_public_cache` | On any `ExamCatalog` save | Rebuilds public student-facing cache key `public:exam_catalog:*` so students see updated data within 60s of PM Exam Domains making changes |

---

## 12. Toast Notifications

| Action | Toast | Type |
|---|---|---|
| Exam created | "{Exam Code} created — add dates and cutoffs to complete" | Success 4s |
| Exam date confirmed | "Date confirmed: {event_name} on {date}" | Success 4s |
| Cutoffs imported | "{N} cutoff rows imported for {exam_code} {year}" | Success 4s |
| Exam archived | "{Exam Code} archived — students will see 'Exam discontinued'" | Warning 8s |
| Cycle copied | "{Exam Code} 2027 cycle created from 2026 — update dates before publishing" | Info 6s |
| Test series linked | "{Series Name} linked — students viewing this exam will see the series" | Success 4s |

---

## 13. Security Considerations

- Exam codes are immutable after creation — used as cross-system references in Module 49 student tracker and Module 22 test series
- Cutoff data: each import batch is logged (importer ID, timestamp, row count) — cannot be silently overwritten
- "Copy to New Cycle" creates a draft copy — new cycle is NOT visible to students until PM Exam Domains explicitly activates it (prevents accidentally publishing incomplete data)
- Salary data changes logged — pay level information is regulated; incorrect data misleads aspirants
- Archived exams: students who tracked the exam see "Exam Discontinued" notice; their test series results are preserved

---

*Page spec version: 1.0 · Created: 2026-03-26 · Division B — Product & Design*
*Indian Education Addition: covers UPSC/SSC/RRB/Banking/Railways/Defence/State PSC exam catalog management for 300+ competitive examinations*
