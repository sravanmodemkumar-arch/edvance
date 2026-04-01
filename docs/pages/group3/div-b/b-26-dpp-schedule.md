# B-26 — DPP Schedule Manager

> **URL:** `/school/academic/coaching/dpp/`
> **File:** `b-26-dpp-schedule.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Coordinator (S4) — full · Subject Teacher (S3) — read/upload DPP · Class Teacher (S3) — read · Principal (S6) — full

> ⚡ **Feature Flag:** Visible only for schools with `coaching_integration: true` in school settings.

---

## 1. Purpose

Manages the Daily Practice Problem (DPP) schedule for coaching-integrated schools — residential schools and day schools that run a dual curriculum of CBSE board preparation alongside JEE/NEET/foundation coaching. A DPP is a short daily problem set (10–20 problems) assigned to students covering concepts taught that day or the previous day, usually as homework or morning class work. In coaching schools, DPPs are as routine as textbooks — every evening students solve the DPP for tomorrow's review. The Academic Coordinator must balance DPP load across subjects to prevent student overload, ensure DPP content aligns with the school syllabus (not ahead or behind), and track which teacher uploaded today's DPP.

---

## 2. Page Layout

### 2.1 Header
```
DPP Schedule Manager                              [+ Upload DPP]  [Weekly Overview]  [Analytics]
Week: [24–28 Mar 2026 (Week 12) ▼]  Class: [XI-A (JEE Foundation) ▼]
DPPs this week: 15/15 uploaded  ·  Avg problems/day: 45  ·  Student completion: 82%
```

---

## 3. Weekly DPP Calendar

| Day | Physics DPP | Chemistry DPP | Mathematics DPP | Biology DPP | Status |
|---|---|---|---|---|---|
| Mon 24 Mar | DPP-P-12-01 (15 probs) | DPP-C-12-01 (12 probs) | DPP-M-12-01 (18 probs) | — | ✅ All uploaded |
| Tue 25 Mar | DPP-P-12-02 (15 probs) | DPP-C-12-02 (10 probs) | DPP-M-12-02 (15 probs) | — | ✅ All uploaded |
| Wed 26 Mar | DPP-P-12-03 (12 probs) | DPP-C-12-03 (12 probs) | DPP-M-12-03 (20 probs) | — | ✅ All uploaded |
| Thu 27 Mar | DPP-P-12-04 (15 probs) | ⬜ Not uploaded | DPP-M-12-04 (15 probs) | — | ⚠️ Chemistry missing |
| Fri 28 Mar | ⬜ Not uploaded | ⬜ Not uploaded | ⬜ Not uploaded | — | ⬜ Tomorrow |

---

## 4. DPP Upload Workflow

**Daily by subject teachers before 4:00 PM:**

[+ Upload DPP] → drawer:

| Field | Value |
|---|---|
| Class | XI-A (JEE Foundation) |
| Subject | Chemistry |
| DPP Number | DPP-C-12-04 (auto-generated: Chem, Week 12, Day 4) |
| Date | 27 Mar 2026 |
| Topics Covered | Electrochemistry — Nernst Equation, Concentration Cells |
| Difficulty | Easy: 3 · Medium: 7 · Hard: 2 (total 12 problems) |
| DPP File | Upload PDF [Browse] |
| Answer Key | Upload separate PDF [Browse] |
| Source | AAKASH / Allen / HC Verma / School-created / NCERT Exemplar |
| Estimated Time | 25 minutes |

Answer key is uploaded separately and only accessible to teachers — students get DPP questions only via the student portal.

---

## 5. DPP Load Analysis

Monitors the daily problem load per student to prevent over-burdening:

| Day | Physics | Chemistry | Mathematics | Total Problems | Time Estimate |
|---|---|---|---|---|---|
| Monday | 15 | 12 | 18 | 45 | ~90 min |
| Tuesday | 15 | 10 | 15 | 40 | ~80 min |
| Wednesday | 12 | 12 | 20 | 44 | ~88 min |
| Thursday | 15 | 0 | 15 | 30 | ~60 min |
| Week Avg | 14.25 | 8.5 | 17 | 39.75 | ~80 min/day |

**Advisory limits (school-configurable):**
- Max problems per day: 50
- Max study time estimate: 100 min for DPPs
- Alert if > 55 problems on any single day

---

## 6. Student DPP Access

Students access DPPs through the Student/Parent portal. DPP tracking (not a core EduForge feature — needs the Student App module):

- DPP released to students at 4:00 PM daily
- Submission tracking: student submits answers (for online DPPs) or class teacher marks "DPP checked" for physical submissions
- Completion rate shown in this page (% of students who submitted that day's DPP)

---

## 7. DPP Content Calendar (Advance Planning)

Academic Coordinator maintains a 4-week advance DPP topic plan:

| Week | Physics Topics | Chemistry Topics | Maths Topics |
|---|---|---|---|
| Week 13 | Wave Optics — HDP, Interference | Solution Thermodynamics | Integration — by parts, substitution |
| Week 14 | Modern Physics — Photoelectric | Electrochemistry Completion | Differential Equations |
| Week 15 | Revision: Optics + Modern | Revision: Thermodynamics | Revision: Calculus |
| Week 16 | Pre-JEE Mock Test Week | — | — |

Topic plan is shared with coaching teachers at the start of each month so DPP content is prepared in advance.

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/coaching/dpp/?week={date}&class_id={id}` | Weekly DPP calendar |
| 2 | `POST` | `/api/v1/school/{id}/coaching/dpp/` | Upload DPP |
| 3 | `GET` | `/api/v1/school/{id}/coaching/dpp/{dpp_id}/` | DPP detail |
| 4 | `GET` | `/api/v1/school/{id}/coaching/dpp/{dpp_id}/answer-key/` | Answer key (teacher only) |
| 5 | `GET` | `/api/v1/school/{id}/coaching/dpp/load-analysis/?week={date}&class_id={id}` | Load analysis |
| 6 | `GET` | `/api/v1/school/{id}/coaching/dpp/topic-calendar/?month={month}&class_id={id}` | Topic calendar |

---

## 9. Business Rules

- DPPs are only visible to classes with coaching curriculum enabled — regular classes don't see DPP content
- Answer keys are accessible only to Subject Teachers and above; never to students directly
- If a teacher hasn't uploaded by 4:00 PM, the Academic Coordinator and teacher get an automated reminder
- DPP load > 55 problems/day triggers a warning to Academic Coordinator and the responsible teachers
- DPP content must be curriculum-aligned — uploading DPPs with topics not yet taught (per B-03 Syllabus Tracker) triggers a curriculum alignment warning

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
