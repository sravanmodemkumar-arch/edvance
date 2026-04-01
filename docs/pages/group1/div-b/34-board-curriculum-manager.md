# B-34 — Board & Curriculum Manager

## 1. Page Metadata

| Field | Value |
|---|---|
| **Route** | `GET /product/boards/` |
| **Django View** | `BoardCurriculumListView` (main) · `BoardDetailView` (`/product/boards/<board_id>/`) |
| **Template** | `portal_base_dark.html` → `product/boards.html` |
| **Primary Role** | PM Exam Domains (Role 6, Level 3) |
| **Also Accessible** | Content Director (18, Level 2 — read + syllabus mapping only) · Platform Admin (10) |
| **Priority** | P1 |
| **Status** | ⬜ Not started |
| **Polling** | No auto-poll (static reference data, changes rare) |

---

## 2. Purpose & Business Logic

India has one of the most fragmented educational board ecosystems in the world. A single platform serving 1,000 schools and 800 colleges must simultaneously understand:

- **CBSE** (Central Board of Secondary Education) — 25,000+ affiliated schools nationally; Classes 1–12; NCERT textbooks; two main exams (Class 10 Board + Class 12 Board)
- **ICSE/ISC** (Council for the Indian School Certificate Examinations) — Classes 1–10 (ICSE) + 11–12 (ISC); own curriculum, not NCERT
- **28 State Boards** — each with its own syllabus, textbooks, medium (English/Hindi/Regional), and grading system:
  - AP Board (BSEAP) — Telugu + English medium; Classes 1–12
  - TS Board (BSETS) — Telugu + English medium; Classes 1–12
  - Maharashtra Board (MSBSHSE) — Marathi + English medium; SSC (Std X) + HSC (Std XII)
  - Karnataka Board (KSEEB) — Kannada + English medium; SSLC (10th) + PUC (11th–12th)
  - Tamil Nadu Board (TNBSE) — Tamil + English medium; Classes 10–12
  - UP Board (UPMSP) — Hindi medium primarily; Classes 9–12
  - Rajasthan Board (RBSE) — Hindi + English; Classes 8–12
  - Bihar Board (BSEB) — Hindi medium; Classes 10–12
  - MP Board (MPBSE) — Hindi medium; Classes 10–12
  - West Bengal Board (WBBSE/WBCHSE) — Bengali + English; Madhyamik (10th) + HS (12th)
  - Odisha Board (CHSE/BSE) — Odia + English
  - Kerala Board (DHSE/SSLC) — Malayalam + English
  - Gujarat Board (GSEB) — Gujarati + English
  - Punjab Board (PSEB) — Punjabi + English
  - Haryana Board (HBSE) — Hindi + English
  - Jharkhand Board (JAC) — Hindi + English
  - Chhattisgarh Board (CGBSE) — Hindi medium
  - Uttarakhand Board (UBSE) — Hindi + English
  - HP Board (HPBOSE) — Hindi + English
  - J&K Board (JKBOSE) — Urdu + English
  - Goa Board (GBSHSE) — English + Konkani
  - Assam Board (SEBA/AHSEC) — Assamese + English
  - Manipur Board (BSE/COHSEM) — Manipuri + English
  - Meghalaya Board (MBOSE) — English medium
  - Nagaland Board (NBSE) — English medium
  - Mizoram Board (MBSE) — Mizo + English
  - Tripura Board (TBSE) — Bengali + English
  - Sikkim Board (SBSE) — English medium
- **International Boards:** IB (Diploma Programme/Middle Years Programme), IGCSE/Cambridge A-Levels, CBSE International, American High School Diploma
- **Open Schooling:** NIOS (National Institute of Open Schooling) — distance learning for Classes 10 and 12

Each board has:
- Different grade/class naming conventions (Class vs Standard vs Grade)
- Different subject names for the same topic (Mathematics vs Maths vs HS Mathematics)
- Different chapter sequences within subjects
- Different examination dates and patterns
- Different language mediums
- Different grading systems (CGPA vs Marks vs Grade)

The **Board & Curriculum Manager** is the configuration foundation for everything content-related in EduForge:
- Without correct board configuration, the Syllabus Builder (B-10) has no hierarchy to build upon
- Without correct grade structure, the Question Bank (D-11) cannot filter questions by grade level
- Without medium settings, SMEs (Division D) cannot tag which language version a question is for
- Without board exam calendar, the Content Freeze system (D-10) cannot identify when to halt new content entry

---

## 3. User Roles & Access

| Role | Access | Notes |
|---|---|---|
| PM Exam Domains (6) | Full CRUD — create/edit/archive boards, configure curriculum, set exam calendars, manage medium settings | Cannot delete boards that have published questions tagged to them |
| Content Director (18) | Read + Syllabus Mapping tab only — cannot add/edit board metadata | Uses this page to understand taxonomy for coordinating SME assignments |
| Platform Admin (10) | Full — same as PM Exam Domains + hard delete option | Hard delete only permitted if 0 questions tagged AND 0 institutions use the board |

---

## 4. Page Layout

### 4.1 Breadcrumb & Header

```
Product / Board & Curriculum Manager
[+ Add Board]        [Bulk Import Boards CSV]
```

**[+ Add Board]** — opens Create Board drawer (640px)
**[Bulk Import Boards CSV]** — opens bulk import modal (for initial data load of 30+ boards)

---

### 4.2 Filter Bar

```
[Search board name or code...] [Board Type ▾] [Medium ▾] [Status: Active/Archived ▾] [Country ▾]
```

Filters:
- **Board Type**: Central (CBSE/ICSE/NIOS) · State Board · International (IB/Cambridge) · Open Schooling
- **Medium**: English · Hindi · Regional (Telugu/Tamil/Kannada/Marathi/Gujarati/Bengali/Odia/Punjabi/Assamese/Malayalam/Urdu/Konkani/Mizo/Manipuri) · All mediums
- **Status**: Active (default) · Archived · All
- **Country**: India · International · All

---

### 4.3 KPI Strip

Four tiles, updated on page load (Memcached 10-min TTL):

| Tile | Value | Colour Logic |
|---|---|---|
| Total Active Boards | Count of `board_status = ACTIVE` | Always neutral |
| Boards with Full Syllabus | Count where syllabus_coverage_pct ≥ 95% | Green if ≥ 80% of active boards |
| Boards with No Questions | Count where published_question_count = 0 | Red if > 0; nudge to prioritise content |
| Boards Needing Review | Count where `last_reviewed_at < today - 365d` | Amber if > 0 |

---

### 4.4 Board Cards Grid

Default: **card grid** (3 columns on desktop, 2 on tablet, 1 on mobile). Toggle to list view via icon at top-right.

**Each board card:**
```
┌─────────────────────────────────────────────┐
│ [Board Logo/Shield]  CBSE                   │
│ Central Board of Secondary Education        │
│ ─────────────────────────────────────────── │
│ Type: Central    Medium: English + Hindi     │
│ Grades: Class 1–12                          │
│ Subjects: 14 active                         │
│ Published Questions: 3,40,000               │
│ Syllabus Coverage: 94% ▓▓▓▓▓▓▓▓▓░           │
│ Last Reviewed: 2026-01-15                   │
│ Status: ● Active                            │
│ [View Details →]      [Edit ✎]              │
└─────────────────────────────────────────────┘
```

- Board logo/shield: SVG upload; default = auto-generated shield with board code initials
- Syllabus Coverage bar: green ≥ 95% · amber 70–94% · red < 70%
- Status dot: green = Active · grey = Archived

---

## 5. Board Detail Page — `/product/boards/<board_id>/`

Full sub-page (not a drawer — boards have complex nested data).

### 5.1 Page Header

```
← Back to Board List
CBSE — Central Board of Secondary Education
[Central Board] [Classes 1–12] [English + Hindi] [● Active]
[Edit Board Metadata]  [Archive Board]
```

### 5.2 Tab Navigation

**Tab 1: Overview**
**Tab 2: Grade Structure**
**Tab 3: Subjects & Curriculum**
**Tab 4: Mediums & Languages**
**Tab 5: Exam Calendar**
**Tab 6: Affiliated Institutions**
**Tab 7: Audit Log**

---

### Tab 1: Overview

Core board metadata display:

| Field | Value |
|---|---|
| Board Code | `CBSE` (unique, used in ORM filtering) |
| Full Name | Central Board of Secondary Education |
| Governing Body | Ministry of Education, Govt. of India |
| Affiliation Number Pattern | e.g. 1930000–2000000 for schools |
| Headquarters | Delhi |
| Official Website | (static text only — never hyperlinked to prevent stale links) |
| Curriculum Framework | NCERT |
| Grading System | CGPA + Marks (10-point CGPA for Board exams) |
| Board Type | Central |
| Primary Mediums | English · Hindi |
| Supported Regional Mediums | — (CBSE has limited regional medium schools) |
| Active Since on Platform | 2024-01-01 |
| Last Syllabus Review | 2026-01-15 |
| Reviewed By | PM Exam Domains name (masked in export — DPDPA) |
| Notes | Free text — e.g. "NCERT 2023 revised syllabus for Classes 9–12 implemented from April 2024" |

**Quick Stats panel (right side):**
- Published questions: 3,40,000
- Active subjects: 14
- Grades configured: 12
- Institutions on platform using this board: 650

---

### Tab 2: Grade Structure

Define the class/grade hierarchy for this board.

**Grade table:**

| Grade Code | Display Name | Stage | Description | Sort Order | Active |
|---|---|---|---|---|---|
| `CBSE-1` | Class 1 | Primary (1–5) | Foundational · FLN | 1 | ✅ |
| `CBSE-6` | Class 6 | Middle (6–8) | — | 6 | ✅ |
| `CBSE-9` | Class 9 | Secondary (9–10) | — | 9 | ✅ |
| `CBSE-10` | Class 10 | Secondary | Board Exam Year | 10 | ✅ |
| `CBSE-11` | Class 11 | Senior Secondary (11–12) | Stream bifurcation | 11 | ✅ |
| `CBSE-12` | Class 12 | Senior Secondary | Board Exam Year | 12 | ✅ |

**Stage groupings:** Each board has named stages (e.g. CBSE: Foundational/Preparatory/Middle/Secondary/Senior Secondary per NEP 2020).

**Add/Edit Grade row inline.** Cannot delete a grade if questions are tagged to it — must archive.

**NEP 2020 Stage Config (CBSE-specific panel):**
For CBSE, map grades to NEP stages:
- Foundational: Class 1–2 (3–5 years) + Nursery/UKG/LKG if applicable
- Preparatory: Class 3–5
- Middle: Class 6–8
- Secondary: Class 9–10
- Senior Secondary: Class 11–12

---

### Tab 3: Subjects & Curriculum

This is the most critical tab — maps subjects to grades and syllabus nodes.

**Subject-Grade Matrix (left panel):**
Rows = subjects · Columns = grades. Cell = ✅ (active) / — (not applicable).

Example for CBSE:

| Subject | Cl.1 | Cl.2 | Cl.3–5 | Cl.6–8 | Cl.9 | Cl.10 | Cl.11 | Cl.12 |
|---|---|---|---|---|---|---|---|---|
| Mathematics | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (Std + Applied) | ✅ |
| Science | — | — | ✅ (General) | ✅ | ✅ | ✅ | — (splits to Phy/Chem/Bio) | — |
| Physics | — | — | — | — | — | — | ✅ | ✅ |
| Chemistry | — | — | — | — | — | — | ✅ | ✅ |
| Biology | — | — | — | — | — | — | ✅ | ✅ |

**Subject detail drawer (480px)** — opens on subject row click:
- Subject Name (as per board's official nomenclature)
- Subject Code (board's official code: e.g. CBSE Code 041 = Mathematics, 301 = English Core)
- Linked Platform Subject (maps to Division D taxonomy: Math, Physics, Chemistry, etc.)
- Textbook Series (e.g. NCERT Mathematics Class 9)
- Chapter Count (auto-counted from linked syllabus tree)
- Syllabus Nodes Linked (link to Syllabus Builder B-10 filtered for this board+subject+grade)
- Question Bank Coverage (% of syllabus nodes with ≥ 5 published questions)
- Internal Code (platform's own code for ORM filtering: `CBSE_MATH_9`)

**Stream Configuration** (for Class 11–12):
Boards with stream bifurcation at senior secondary level allow configuring:
- Science Stream: subjects available
- Commerce Stream: subjects available
- Arts/Humanities Stream: subjects available
- Vocational Stream: subjects available

Students at institution level select stream; question bank filtered accordingly.

**Chapter Alignment panel:**
For each subject × grade combination: expected chapter list (from board's official syllabus PDF — entered manually or imported from CSV). Displays:
- Chapter Name · Chapter Code · Topic Count (from D-09 taxonomy) · Published Question Count · Coverage %
- "Link to Syllabus Builder" opens B-10 pre-filtered for this board+subject+grade

---

### Tab 4: Mediums & Languages

Configure which language mediums this board supports and the platform's content availability per medium.

**Medium table:**

| Medium | Language | Script | Official Support | Platform Content Available | Priority |
|---|---|---|---|---|---|
| English | English | Latin | ✅ Official | ✅ Full coverage | Primary |
| Hindi | Hindi | Devanagari | ✅ Official | ✅ 60% coverage | Secondary |
| Telugu | Telugu | Telugu script | ✅ AP/TS schools | ⬜ Planned Q3 2026 | Tertiary |

**Per-medium settings:**
- **Question Bank Coverage Target**: % of questions that should have this-medium versions (e.g. for Hindi medium CBSE schools: 70% target)
- **Display Name Override**: how the board is displayed to Hindi-medium institutions (e.g. "केंद्रीय माध्यमिक शिक्षा बोर्ड")
- **IME Code**: which keyboard input method engine to use for regional scripts (e.g. `te-IN` for Telugu, `hi-IN` for Hindi)
- **Font**: which Unicode font to use for this script in question rendering

**SME Assignment for this medium** (links to Division D Role 27 SME Regional Language):
Shows which SME is assigned to create questions for this board in this medium.

---

### Tab 5: Exam Calendar

Board exam lifecycle for each academic year.

**Exam events table:**

| Event | Typical Month | 2025–26 Date | Configured? |
|---|---|---|---|
| Academic Session Start | April | 01 April 2025 | ✅ |
| Quarterly Exam / Unit Test | July | 15–22 July 2025 | ✅ |
| Half-Yearly Exam | September–October | 20 Sep – 5 Oct 2025 | ✅ |
| Pre-Board Exam | January | 10–25 January 2026 | ✅ |
| Board Practical Exams | January–February | 15 Jan – 14 Feb 2026 | ✅ |
| Board Theory Exam (Class 10) | February–March | 15 Feb – 18 Mar 2026 | ✅ |
| Board Theory Exam (Class 12) | February–March | 15 Feb – 5 Apr 2026 | ✅ |
| Result Announcement | May | 12 May 2026 | ⬜ |
| Compartment/Supplementary | July | July 2026 | ⬜ |
| Content Freeze Date (Board Exam) | January | 10 January 2026 | ✅ |

**Content Freeze Date** — feeds directly into D-10 (Content Calendar) and D-02 (Question Editor): after this date, new questions tagged to board exam exam type cannot be submitted.

**Bulk Add Academic Year** action: select "Copy from last year + 1 year" to quickly scaffold next AY events.

---

### Tab 6: Affiliated Institutions

Which institutions on the EduForge platform use this board.

**Read-only table:**
| Institution Name | Type | State | Tier | Enrolled Students | BGV Status | Last Active |
|---|---|---|---|---|---|---|

Filters: Type (School/College) · State · Tier (Starter/Standard/Professional/Enterprise).
Link to institution detail in Division A (05-institution-detail).

This is critical for understanding the impact of any board curriculum change — "if I update the Class 10 CBSE syllabus structure, which 650 schools are affected?"

---

### Tab 7: Audit Log

Immutable log of all changes to this board's configuration.

| Timestamp | Actor Role | Action | Field Changed | Before | After |
|---|---|---|---|---|---|
| 2026-01-15 14:32 IST | PM Exam Domains | Updated exam calendar | content_freeze_date | 2026-01-15 | 2026-01-10 |
| 2026-01-10 11:05 IST | PM Exam Domains | Added subject | Chemistry Class 11 | — | Added |

---

## 6. Create/Edit Board Drawer (640px)

**Section 1: Basic Info**
- Board Code (UPPERCASE, 3–10 chars, unique: `CBSE`, `MAHA`, `APBSE`, `IB`)
- Full Name
- Short Display Name (for dropdowns: "CBSE" vs "CBSE — Central Board of Secondary Education")
- Board Type (Central / State Board / International / Open Schooling)
- State (for state boards — dropdown of 28 states + UTs)
- Governing Body
- Curriculum Framework (NCERT / State Textbook / Cambridge / IB / NIOS / Other)
- Grading System (Marks % / CGPA / Grades / Mixed)

**Section 2: Mediums**
Multi-select: English · Hindi · Telugu · Tamil · Kannada · Marathi · Gujarati · Bengali · Odia · Punjabi · Assamese · Malayalam · Urdu · Konkani · Others

**Section 3: Grade Range**
From Grade: [dropdown] — To Grade: [dropdown] — includes options for Nursery/LKG/UKG for preschool

**Section 4: Platform Settings**
- Default Access Level (questions for this board: Platform-Wide / School Only / College Only)
- Active: toggle

**Footer**: [Save Draft] [Save & Configure Curriculum →] [Cancel]

---

## 7. Bulk Import — Board CSV

For initial setup of all 30+ boards. CSV template columns:
`board_code, full_name, short_name, board_type, state_code, curriculum_framework, grading_system, primary_mediums (pipe-separated), grade_from, grade_to, active`

Validation: duplicate board_code check · valid state_code · valid grade_from/to · valid board_type enum.
Error report CSV for failed rows. Successful rows create board records in `DRAFT` state pending PM Exam Domains review before activation.

---

## 8. Drawers & Modals

| Component | Trigger | Width | Content |
|---|---|---|---|
| Create Board Drawer | [+ Add Board] | 640px | As spec above |
| Edit Board Drawer | Card → [Edit] or Detail → [Edit Metadata] | 640px | Pre-filled create form |
| Subject Detail Drawer | Subject row click in Tab 3 | 480px | Subject metadata + textbook + chapter alignment |
| Archive Confirmation Modal | [Archive Board] | 480px | Impact summary: N questions affected · N institutions affected · Type "ARCHIVE" to confirm |
| Bulk Import Modal | [Bulk Import CSV] | 600px | Upload → validation report → confirm import |
| Grade Edit Modal | Grade row → edit pencil | 400px | Inline grade CRUD |

---

## 9. Toast Notifications

| Action | Toast | Type |
|---|---|---|
| Board saved (draft) | "Board saved as draft" | Success 4s |
| Board activated | "{Board Code} is now active and visible to Content team" | Success 4s |
| Board archived | "{Board Code} archived — questions remain in bank, new tagging disabled" | Warning 8s |
| Subject added | "Subject added to {Board} {Grade}" | Success 4s |
| Grade added | "Grade {name} added to {Board}" | Success 4s |
| Exam calendar saved | "Exam calendar updated for {AY}" | Success 4s |
| Content freeze date set | "Content freeze set to {date} — D-02 submit blocked for this board after this date" | Info 6s |
| Bulk import success | "{N} boards imported · {M} errors · Download error report" | Warning 8s |

---

## 10. Empty States

| Scenario | State Shown |
|---|---|
| No boards configured yet | Illustration + "No boards configured. Add your first board or bulk-import from CSV." |
| No boards match filters | "No boards match your filters. Clear filters to see all boards." |
| Board has no subjects | Tab 3 empty state: "No subjects configured. Start by adding subjects for each grade range." |
| Board has no exam calendar | Tab 5 empty state: "No exam dates added for this academic year. Add events to enable content freeze management." |

---

## 11. API Endpoints

| Method | Endpoint | Description | Role Gate |
|---|---|---|---|
| GET | `/api/v1/product/boards/` | List all boards (paginated, filterable) | PM Exam Domains (6) · Content Director (18) |
| POST | `/api/v1/product/boards/` | Create board | PM Exam Domains (6) |
| GET | `/api/v1/product/boards/<id>/` | Board detail + all sub-data | PM Exam Domains (6) · Content Director (18) |
| PATCH | `/api/v1/product/boards/<id>/` | Update board metadata | PM Exam Domains (6) |
| POST | `/api/v1/product/boards/<id>/archive/` | Archive board | PM Exam Domains (6) |
| GET | `/api/v1/product/boards/<id>/grades/` | List grades | All with board access |
| POST | `/api/v1/product/boards/<id>/grades/` | Add grade | PM Exam Domains (6) |
| PATCH | `/api/v1/product/boards/<id>/grades/<gid>/` | Edit grade | PM Exam Domains (6) |
| GET | `/api/v1/product/boards/<id>/subjects/` | List subjects × grades | All with board access |
| POST | `/api/v1/product/boards/<id>/subjects/` | Add subject | PM Exam Domains (6) |
| GET | `/api/v1/product/boards/<id>/mediums/` | List mediums | All with board access |
| PATCH | `/api/v1/product/boards/<id>/mediums/` | Update medium config | PM Exam Domains (6) |
| GET | `/api/v1/product/boards/<id>/calendar/` | Exam calendar | All with board access |
| POST | `/api/v1/product/boards/<id>/calendar/` | Add calendar event | PM Exam Domains (6) |
| PATCH | `/api/v1/product/boards/<id>/calendar/<eid>/` | Update event | PM Exam Domains (6) |
| POST | `/api/v1/product/boards/<id>/calendar/copy-from/<ay>/` | Copy AY calendar | PM Exam Domains (6) |
| GET | `/api/v1/product/boards/<id>/institutions/` | Affiliated institutions | PM Exam Domains (6) |
| GET | `/api/v1/product/boards/<id>/audit-log/` | Audit trail | PM Exam Domains (6) · Platform Admin (10) |
| POST | `/api/v1/product/boards/bulk-import/` | Bulk CSV import | PM Exam Domains (6) |
| GET | `/api/v1/product/boards/export/` | Export boards list CSV | PM Exam Domains (6) |

---

## 12. HTMX Patterns

```
Board Grid (page load)
  → hx-get="/product/boards/?{filters}" hx-target="#board-grid" hx-swap="innerHTML"
  → hx-trigger="change from:#board-type-filter, change from:#medium-filter, change from:#status-filter"

Create Board Drawer
  → hx-post="/api/v1/product/boards/" hx-target="#board-grid" hx-swap="outerHTML"
  → hx-vals="js:{board_code: boardCode.value, ...}"
  → On success: HTMX close-drawer event + toast trigger

Board Detail — Tab Switch
  → hx-get="/product/boards/<id>/tab/<tab_name>/" hx-target="#board-tab-content" hx-swap="innerHTML"
  → hx-indicator="#tab-loader"

Subject-Grade Matrix (Tab 3)
  → hx-get="/product/boards/<id>/subjects/" hx-target="#subject-matrix" hx-swap="innerHTML"
  → Inline edit cells: hx-patch="/api/v1/product/boards/<id>/subjects/<sid>/"
    hx-trigger="change" hx-target="closest tr" hx-swap="outerHTML"

Exam Calendar (Tab 5)
  → hx-post="/api/v1/product/boards/<id>/calendar/" hx-target="#calendar-table-body"
    hx-swap="afterbegin" (new row prepended)

Archive Board Modal
  → Confirmation input validates: hx-trigger="keyup[target.value=='ARCHIVE']"
  → Submit: hx-post="/api/v1/product/boards/<id>/archive/"
    hx-target="closest .board-card" hx-swap="outerHTML"
    → Swaps card to greyed "Archived" state inline
```

---

## 13. Database Models

All board configuration lives in the shared schema (`product` app):

```python
class Board(models.Model):
    board_code    = models.CharField(max_length=10, unique=True)  # e.g. CBSE, APBSE, IB
    full_name     = models.CharField(max_length=200)
    short_name    = models.CharField(max_length=50)
    board_type    = models.CharField(max_length=20)  # CENTRAL/STATE/INTERNATIONAL/OPEN
    state         = models.CharField(max_length=50, blank=True)
    curriculum    = models.CharField(max_length=50)  # NCERT/STATE_TEXTBOOK/CAMBRIDGE/IB/NIOS/OTHER
    grading_system = models.CharField(max_length=30)  # MARKS/CGPA/GRADES/MIXED
    logo_url      = models.URLField(blank=True)  # R2 CDN URL
    status        = models.CharField(max_length=10, default='ACTIVE')
    created_by    = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

class BoardGrade(models.Model):
    board         = models.ForeignKey(Board, related_name='grades', on_delete=models.PROTECT)
    grade_code    = models.CharField(max_length=20)  # e.g. CBSE-10
    display_name  = models.CharField(max_length=50)  # e.g. Class 10
    stage         = models.CharField(max_length=50)  # e.g. Secondary
    sort_order    = models.PositiveSmallIntegerField()
    is_board_exam_year = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)

class BoardSubject(models.Model):
    board         = models.ForeignKey(Board, on_delete=models.PROTECT)
    grade         = models.ForeignKey(BoardGrade, on_delete=models.PROTECT)
    subject_name  = models.CharField(max_length=100)  # Board's official subject name
    subject_code  = models.CharField(max_length=20, blank=True)  # Board's official code
    platform_subject = models.CharField(max_length=50)  # links to D-09 subject taxonomy
    stream        = models.CharField(max_length=30, blank=True)  # SCIENCE/COMMERCE/ARTS/VOCATIONAL
    textbook_series = models.CharField(max_length=200, blank=True)
    is_optional   = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)

class BoardMedium(models.Model):
    board         = models.ForeignKey(Board, related_name='mediums', on_delete=models.PROTECT)
    language_code = models.CharField(max_length=10)  # ISO 639-1: en, hi, te, ta, kn...
    language_name = models.CharField(max_length=50)
    script        = models.CharField(max_length=30)  # Latin, Devanagari, Telugu, Tamil...
    is_official   = models.BooleanField(default=True)
    platform_coverage_status = models.CharField(max_length=20)  # FULL/PARTIAL/PLANNED/NONE
    display_name_local = models.CharField(max_length=100, blank=True)  # Board name in this language
    coverage_target_pct = models.PositiveSmallIntegerField(default=0)
    priority      = models.PositiveSmallIntegerField(default=1)

class BoardExamCalendar(models.Model):
    board         = models.ForeignKey(Board, related_name='calendar_events', on_delete=models.PROTECT)
    academic_year = models.CharField(max_length=10)  # e.g. 2025-26
    event_type    = models.CharField(max_length=30)  # SESSION_START/QUARTERLY/HALF_YEARLY/PRE_BOARD/PRACTICAL/THEORY_EXAM/RESULT/CONTENT_FREEZE
    event_name    = models.CharField(max_length=100)
    for_grades    = models.JSONField(default=list)  # list of grade_codes this event applies to
    start_date    = models.DateField(nullable=True)
    end_date      = models.DateField(nullable=True)
    is_content_freeze_date = models.BooleanField(default=False)
    notes         = models.TextField(blank=True)

class BoardAuditLog(models.Model):
    board         = models.ForeignKey(Board, on_delete=models.PROTECT)
    action        = models.CharField(max_length=50)
    field_changed = models.CharField(max_length=100, blank=True)
    before_value  = models.TextField(blank=True)
    after_value   = models.TextField(blank=True)
    performed_by  = models.ForeignKey(User, on_delete=models.PROTECT)
    performed_at  = models.DateTimeField(auto_now_add=True)
    ip_hash       = models.CharField(max_length=64)
```

**Cache strategy:**
- Board list: `product:boards:list:{filters_hash}` · TTL 10 min · `cache.delete('product:boards:list:*')` on any board change
- Board detail: `product:boards:detail:{board_id}` · TTL 30 min
- Grade/subject tree: `product:boards:{board_id}:curriculum` · TTL 60 min · bust on curriculum edit
- KPI strip: `product:boards:kpi` · TTL 10 min

---

## 14. Security Considerations

- All CRUD endpoints require `role IN (6, 10)` enforcement at Django view layer (not just UI gate)
- `Content Director (18)` receives `HTTP 405` on any non-GET/non-read-permitted endpoint
- Archive requires confirmation token matching server-generated value (CSRF + HMAC-SHA256 of `board_id + user_id + timestamp`) — prevents CSRF-based archival
- All configuration changes logged to `BoardAuditLog` with IP hash (SHA-256) — DPDPA compliant
- Board codes once set cannot be changed (they're used as foreign-key references in `content_question.board_code`) — enforced at model layer
- Hard delete (Platform Admin only) validates zero questions tagged AND zero institutions affiliated — enforced with DB constraint check before delete

---

## 15. Performance & Scaling

- Board list: < 100 boards total — no pagination needed (single load ≤ 200ms)
- Board detail sub-tabs: each tab loads independently via HTMX — no full-page reload
- Subject-grade matrix: rendered server-side as HTML table — for 50 subjects × 12 grades = 600 cells, rendered in < 100ms
- Affiliated institutions count: cached separately to avoid counting join on every page load
- Audit log: paginated 25/page — never loads full history in single request
- Content freeze date propagation: when set/changed, Celery task `propagate_content_freeze_to_d10` notifies D-10 calendar and updates `content_exam_type_config.freeze_date` for all exam types linked to this board

---

*Page spec version: 1.0 · Created: 2026-03-26 · Division B — Product & Design*
*Indian Education Addition: covers CBSE, ICSE, 28 State Boards, IB/IGCSE, NIOS — essential for platforms serving 1,800+ Indian schools and colleges*
