# P-04 — Academic Quality Audit

> **URL:** `/group/audit/academic/`
> **File:** `p-04-academic-quality-audit.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Academic Quality Officer (Role 122, G1) — primary operator

---

## 1. Purpose

The Academic Quality Audit page manages the systematic evaluation of teaching quality, syllabus coverage, examination standards, and learning outcomes across all branches. In Indian education, academic quality varies enormously between branches of the same group — the flagship Hyderabad branch has experienced teachers and delivers 100% syllabus coverage by January, while the newly opened rural branch struggles with teacher vacancies and covers only 70% by March. The Academic Quality Officer's job is to detect and close these gaps before they show up in board exam results.

The problems this page solves:

1. **Lesson plan compliance:** Division B (Academic Leadership) sets standardised lesson plans — daily topics, weekly assessments, monthly tests. But compliance at the branch level is inconsistent. The academic audit verifies: was the prescribed topic taught on the prescribed day? Were the assigned worksheets given? Were the weekly assessments conducted? In large groups, the gap between the planned curriculum and actual classroom delivery is the single biggest factor in branch-to-branch result variation.

2. **Exam paper quality:** In centralised exam systems, the Group Exam Controller (Role 12) sets question papers. But some branches conduct internal tests with locally-set papers of poor quality — questions outside syllabus, incorrect answer keys, unbalanced difficulty. The audit evaluates paper quality: blueprint adherence (marks distribution across chapters), difficulty balance (easy 30% / medium 50% / hard 20%), language clarity, and answer key accuracy.

3. **Result moderation verification:** After exams, the Group Results Coordinator (Role 13) runs cross-branch moderation. The academic audit verifies that moderation was applied correctly — no branch inflated marks, no selective grace marks, and the moderation formula was consistent.

4. **Teaching hours verification:** RTE Act mandates minimum instructional hours (800 hours for primary, 1000 for upper primary). CBSE mandates minimum periods per subject. The audit verifies: actual teaching hours (from timetable + attendance) match requirements, free periods aren't excessive, and substitution arrangements exist for absent teachers.

5. **Lab and practical compliance:** CBSE and state boards mandate practical hours for science subjects. Many branches conduct "paper practicals" — students write experiments without actually performing them. The audit checks lab log books, equipment utilisation records, and student practical files.

**Scale:** 5–50 branches · 100–5,000 teachers · 500–5,000 lesson plans per branch per term · 5–20 exam cycles per year · 100–300 academic findings/year

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Academic Quality Officer | 122 | G1 | Full — create audits, review findings, evaluate quality | Primary academic auditor |
| Group Internal Audit Head | 121 | G1 | Read + oversight — view all academic audits | Cross-functional visibility |
| Group Inspection Officer | 123 | G3 | Execute — conduct on-site academic inspections | Classroom visits, lab checks |
| Group Compliance Data Analyst | 127 | G1 | Read — academic audit data for analytics | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read + CAPA — create corrective actions | Improvement tracking |
| Chief Academic Officer (Div B) | 9 | G4 | Read — audit results for academic policy decisions | Cross-division stakeholder |
| Group Academic Director (Div B) | 10 | G3 | Read — audit feedback on syllabus/curriculum | Cross-division stakeholder |
| Group CEO / Chairman | — | G4/G5 | Read — academic quality overview | Strategic oversight |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Reads Division B data (lesson plans, exam papers, results, timetables) but cannot modify it.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Academic Quality Audit
```

### 3.2 Page Header
```
Academic Quality Audit                             [+ New Academic Audit]  [Quality Score Card]  [Export]
Academic Quality Officer — Dr. Lakshmi Devi
Sunrise Education Group · FY 2025-26 · 28 branches · Academic Quality Index: 78% (Grade A)
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Avg Lesson Plan Compliance | Percentage | AVG(lesson_plan_compliance_%) across all branches this term | Green ≥ 90%, Amber 75–89%, Red < 75% | `#kpi-lesson` |
| 2 | Avg Syllabus Coverage | Percentage | AVG(syllabus_coverage_%) across all branches as of today | Green ≥ pro-rated target, Amber within 10%, Red > 10% behind | `#kpi-syllabus` |
| 3 | Exam Paper Quality Score | Percentage | AVG(paper_quality_score) across last exam cycle | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-paper` |
| 4 | Open Academic Findings | Integer | COUNT(findings) WHERE audit_type = 'academic' AND status != 'closed' | Red > 30, Amber 10–30, Green < 10 | `#kpi-findings` |
| 5 | Teaching Hours Compliance | Percentage | Branches meeting RTE minimum hours / total × 100 | Green ≥ 95%, Amber 85–94%, Red < 85% | `#kpi-hours` |
| 6 | Lab Practical Completion | Percentage | AVG(practical_completion_%) across science departments | Green ≥ 90%, Amber 75–89%, Red < 75% | `#kpi-lab` |

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Audit List** — All academic audits with status
2. **Lesson Plan Compliance** — Branch × subject compliance matrix
3. **Exam Quality Review** — Paper quality evaluation
4. **Teaching Hours** — Instructional hours verification
5. **Lab & Practical Audit** — Practical completion tracking

### 5.2 Tab 1: Audit List

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Audit ID | Text (link) | Yes | Auto-generated: ACA-2026-001 |
| Branch | Text | Yes | — |
| Term | Badge | Yes | Term 1 / Term 2 / Mid-Year / Annual |
| Audit Date | Date | Yes | — |
| Auditor | Text | Yes | — |
| Focus Areas | Badges | No | Lesson Plans / Exams / Practicals / Teaching Hours / Result Moderation |
| Status | Badge | Yes | Scheduled / In Progress / Report Pending / Reviewed / Closed |
| Findings | Integer | Yes | — |
| Quality Score | Percentage | Yes | Overall academic quality score |
| Actions | Buttons | No | [View] [Start] [Submit Report] |

### 5.3 Tab 2: Lesson Plan Compliance

**Branch × Subject matrix:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | Row per branch |
| English | Percentage | Yes | Lesson plan compliance % |
| Mathematics | Percentage | Yes | — |
| Physics | Percentage | Yes | — |
| Chemistry | Percentage | Yes | — |
| Biology | Percentage | Yes | — |
| Social Studies | Percentage | Yes | — |
| Hindi / Telugu / Regional | Percentage | Yes | Second language |
| Overall | Percentage | Yes | Average across subjects |
| Weakest Subject | Text | No | Subject with lowest compliance |
| Trend | Arrow | Yes | ↑↓→ vs previous term |

**Colour coding per cell:** Green ≥ 90%, Amber 75–89%, Red < 75%

**Drill-down:** Click cell → opens teacher-wise compliance for that branch + subject

### 5.4 Tab 3: Exam Quality Review

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Exam | Text (link) | Yes | Exam name/cycle |
| Branch | Text | Yes | — |
| Subject | Text | Yes | — |
| Class | Text | Yes | — |
| Blueprint Adherence | Percentage | Yes | Marks distribution matches prescribed blueprint |
| Difficulty Balance | Badge | Yes | ✅ Balanced / ⚠️ Skewed / 🔴 Poor |
| Language Clarity | Rating | Yes | 1–5 stars |
| Answer Key Accuracy | Percentage | Yes | Correct answers / total questions |
| Syllabus Alignment | Percentage | Yes | Questions within prescribed syllabus |
| Overall Quality | Percentage | Yes | Composite score |
| Reviewer | Text | Yes | Who reviewed the paper |
| Comments | Text (truncated) | No | Reviewer notes |

### 5.5 Tab 4: Teaching Hours

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Class | Text | Yes | — |
| Subject | Text | Yes | — |
| Required Hours (Term) | Integer | Yes | As per CBSE/Board norm |
| Actual Hours | Integer | Yes | From timetable + attendance |
| Compliance | Percentage | Yes | Actual / required × 100 |
| Free Periods (%) | Percentage | Yes | Unscheduled / total periods |
| Substitution Rate | Percentage | Yes | Teacher absent periods covered by substitutes |
| RTE Compliant? | Badge | Yes | ✅ Yes / 🔴 No |
| Gap (Hours) | Integer | Yes | Required − actual |

### 5.6 Tab 5: Lab & Practical Audit

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Subject | Badge | Yes | Physics / Chemistry / Biology / Computer Science |
| Class | Text | Yes | — |
| Prescribed Practicals | Integer | Yes | Board-mandated count |
| Completed | Integer | Yes | Verified from lab logbook |
| Completion % | Percentage | Yes | — |
| Lab Logbook Verified? | Badge | Yes | ✅ Yes / 🔴 Not checked / ⚠️ Discrepancy |
| Student Files Checked (sample) | Integer | Yes | N files sampled |
| Equipment Functional? | Badge | Yes | ✅ All / ⚠️ Partial / 🔴 Major gaps |
| Status | Badge | Yes | Compliant / Non-compliant / Pending Audit |

---

## 6. Drawers & Modals

### 6.1 Modal: `create-academic-audit` (640px)

- **Title:** "New Academic Quality Audit"
- **Fields:**
  - Branch (dropdown, required)
  - Term (dropdown): Term 1 / Term 2 / Mid-Year / Annual / Special
  - Audit date(s) (date picker)
  - Focus areas (checkboxes):
    - Lesson plan compliance (% of prescribed lessons delivered)
    - Syllabus coverage (chapters covered vs planned)
    - Exam paper quality review
    - Answer key verification
    - Result moderation check
    - Teaching hours verification
    - Lab practical completion
    - Student notebook/file review
    - Classroom observation (teaching methodology)
  - Subjects to audit (multi-select or "All")
  - Classes to audit (multi-select or "All")
  - Sample size — teachers (integer — how many teachers' records to check)
  - Sample size — students (integer — how many student files to check)
  - Auditor(s) (multi-select)
  - Special instructions (textarea)
- **Buttons:** Cancel · Schedule
- **Access:** Role 122, 121, G4+

### 6.2 Drawer: `academic-audit-detail` (780px, right-slide)

- **Title:** "Academic Audit — [Branch] · [Term]"
- **Tabs:** Overview · Lesson Plans · Exam Quality · Teaching Hours · Lab · Findings · Report
- **Overview tab:** Audit status, scope, team, progress (% complete), quality score
- **Lesson Plans tab:** Subject-wise compliance table with teacher drill-down
- **Exam Quality tab:** Paper-wise quality evaluation with reviewer comments
- **Teaching Hours tab:** Hours compliance per class per subject
- **Lab tab:** Practical completion with equipment status
- **Findings tab:** All findings with severity, CAPA status
- **Report tab:** Audit report — quality index, strengths, weaknesses, recommendations
- **Footer:** [Add Finding] [Submit Report] [Export PDF]
- **Access:** G1+ (Division P + B stakeholders)

### 6.3 Modal: `evaluate-exam-paper` (640px)

- **Title:** "Evaluate Exam Paper Quality"
- **Fields:**
  - Exam (dropdown — from Division B exam list)
  - Subject (dropdown)
  - Class (dropdown)
  - Branch (dropdown)
  - Blueprint adherence (slider 0–100%)
  - Difficulty distribution:
    - Easy questions: N (marks)
    - Medium questions: N (marks)
    - Hard questions: N (marks)
    - Expected ratio: 30:50:20 (auto-checks)
  - Language clarity (1–5 stars)
  - Syllabus alignment (slider 0–100%)
  - Answer key accuracy (incorrect answers found — integer)
  - Overall quality score (auto-calculated from above)
  - Detailed comments (textarea)
- **Buttons:** Cancel · Save Evaluation
- **Access:** Role 122, 121

### 6.4 Modal: `classroom-observation` (560px)

- **Title:** "Classroom Observation Form"
- **Fields:**
  - Branch + Class + Subject + Teacher (pre-filled or selected)
  - Date and period
  - Teaching methodology (checkboxes): Lecture / Interactive / Activity-based / Lab / Digital/PPT / Flipped
  - Student engagement (1–5 scale)
  - Content accuracy (1–5 scale)
  - Classroom management (1–5 scale)
  - Use of teaching aids (1–5 scale)
  - Pace appropriate? (Yes / Too fast / Too slow)
  - Syllabus topic covered? (Yes / No / Partially)
  - Assessment conducted in class? (Yes / No)
  - Overall observation rating (auto-calculated)
  - Strengths observed (textarea)
  - Areas for improvement (textarea)
  - Confidential? (toggle — if yes, not shared with teacher)
- **Buttons:** Cancel · Save Observation
- **Access:** Role 122, 123

---

## 7. Charts

### 7.1 Branch Academic Quality Index (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Branch Academic Quality Index" |
| Data | Overall quality score per branch, sorted descending |
| Colour | Green ≥ 85%, Amber 70–84%, Red < 70% |
| API | `GET /api/v1/group/{id}/audit/academic/analytics/branch-quality/` |

### 7.2 Lesson Plan Compliance Trend (Multi-Line)

| Property | Value |
|---|---|
| Chart type | Multi-line |
| Title | "Lesson Plan Compliance — Monthly Trend" |
| Data | Average compliance % per month, one line per branch tier (top 5, middle, bottom 5) |
| API | `GET /api/v1/group/{id}/audit/academic/analytics/lesson-trend/` |

### 7.3 Subject Quality Heatmap (Matrix)

| Property | Value |
|---|---|
| Chart type | Heatmap matrix (custom Canvas) |
| Title | "Subject Quality — Branch × Subject" |
| X-axis | Subjects |
| Y-axis | Branches |
| Cell colour | Green / Amber / Red based on quality score |
| API | `GET /api/v1/group/{id}/audit/academic/analytics/subject-heatmap/` |

### 7.4 Finding Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut |
| Title | "Academic Findings by Category" |
| Data | COUNT per category: Lesson Plans, Exam Quality, Teaching Hours, Lab, Result Moderation, Other |
| API | `GET /api/v1/group/{id}/audit/academic/analytics/finding-categories/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit created | "Academic audit scheduled — [Branch], [Term]" | Success | 3s |
| Paper evaluated | "Exam paper evaluated — Quality: [Score]%" | Success | 3s |
| Classroom observed | "Classroom observation recorded — [Teacher], [Subject]" | Success | 3s |
| Finding added | "Academic finding [ID] added — severity: [S1–S4]" | Success | 3s |
| Report submitted | "Academic audit report submitted — [Branch]" | Success | 3s |
| Low compliance alert | "⚠️ Lesson plan compliance < 75% at [Branch] — [Subject]" | Warning | 5s |
| Lab non-compliance | "🔴 Lab practical completion < 50% at [Branch] — [Subject]" | Error | 5s |
| Teaching hours gap | "⚠️ RTE teaching hours non-compliant at [Branch] — gap: [N] hours" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No academic audits | 📚 | "No Academic Audits" | "Schedule your first academic quality audit to begin evaluating teaching standards." | New Academic Audit |
| No exam evaluations | 📝 | "No Exam Paper Evaluations" | "Evaluate exam papers after each test cycle to maintain question quality." | Evaluate Paper |
| No observations | 🏫 | "No Classroom Observations" | "Conduct classroom observations to assess live teaching quality." | New Observation |
| No findings | ✅ | "No Academic Findings" | "All academic quality parameters are within acceptable thresholds." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + tab skeleton |
| Lesson plan matrix | Table skeleton with colour cells |
| Exam quality table | Table skeleton with 15 rows |
| Audit detail drawer | 780px skeleton: 7 tabs |
| Subject heatmap | Grey grid placeholder |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/academic/` | G1+ | List all academic audits |
| GET | `/api/v1/group/{id}/audit/academic/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/audit/academic/{audit_id}/` | G1+ | Audit detail |
| POST | `/api/v1/group/{id}/audit/academic/` | 122, 121, G4+ | Create academic audit |
| PUT | `/api/v1/group/{id}/audit/academic/{audit_id}/` | 122, 121 | Update audit |
| POST | `/api/v1/group/{id}/audit/academic/{audit_id}/findings/` | 122, 123 | Add finding |
| POST | `/api/v1/group/{id}/audit/academic/{audit_id}/report/` | 122 | Submit report |
| GET | `/api/v1/group/{id}/audit/academic/lesson-compliance/` | G1+ | Lesson plan compliance matrix |
| GET | `/api/v1/group/{id}/audit/academic/lesson-compliance/{branch_id}/{subject}/` | G1+ | Teacher-wise drill-down |
| GET | `/api/v1/group/{id}/audit/academic/exam-quality/` | G1+ | Exam paper quality list |
| POST | `/api/v1/group/{id}/audit/academic/exam-quality/` | 122, 121 | Evaluate exam paper |
| GET | `/api/v1/group/{id}/audit/academic/teaching-hours/` | G1+ | Teaching hours compliance |
| GET | `/api/v1/group/{id}/audit/academic/lab-audit/` | G1+ | Lab practical completion |
| POST | `/api/v1/group/{id}/audit/academic/classroom-observations/` | 122, 123 | Record observation |
| GET | `/api/v1/group/{id}/audit/academic/classroom-observations/` | G1+ | List observations |
| GET | `/api/v1/group/{id}/audit/academic/analytics/branch-quality/` | G1+ | Branch quality bar chart |
| GET | `/api/v1/group/{id}/audit/academic/analytics/lesson-trend/` | G1+ | Lesson plan trend |
| GET | `/api/v1/group/{id}/audit/academic/analytics/subject-heatmap/` | G1+ | Subject quality heatmap |
| GET | `/api/v1/group/{id}/audit/academic/analytics/finding-categories/` | G1+ | Finding category donut |
| GET | `/api/v1/group/{id}/audit/academic/export/` | G1+ | Export audit data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../academic/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#academic-content` | `innerHTML` | `hx-trigger="click"` |
| Audit detail drawer | Row click | `hx-get=".../academic/{id}/"` | `#right-drawer` | `innerHTML` | 780px drawer |
| Create audit | Form submit | `hx-post=".../academic/"` | `#create-result` | `innerHTML` | Toast |
| Evaluate paper | Form submit | `hx-post=".../exam-quality/"` | `#eval-result` | `innerHTML` | Toast |
| Classroom observation | Form submit | `hx-post=".../classroom-observations/"` | `#obs-result` | `innerHTML` | Toast |
| Lesson plan drill-down | Cell click | `hx-get=".../lesson-compliance/{branch}/{subject}/"` | `#drill-down` | `innerHTML` | Inline expand |
| Filter | Filter change | `hx-get` with filters | `#table-body` | `innerHTML` | `hx-trigger="change"` |
| Add finding | Form submit | `hx-post=".../academic/{id}/findings/"` | `#finding-result` | `innerHTML` | Toast |
| Chart load | Tab shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |
| Heatmap | Tab 2 load | `hx-get=".../analytics/subject-heatmap/"` | `#heatmap-container` | `innerHTML` | Custom render |
| Pagination | Page click | `hx-get` with page param | `#table-body` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
