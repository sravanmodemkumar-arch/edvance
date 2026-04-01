# B-10 — IQAC & Continuous Improvement

> **URL:** `/college/academic/iqac/`
> **File:** `b-10-iqac.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** IQAC Coordinator (S4) · Principal/Director (S6) — chair · Dean Academics (S5) · All HODs · External IQAC members (S7-level view) · NAAC assessors (read-only during assessment)

---

## 1. Purpose

IQAC (Internal Quality Assurance Cell) is mandatory for all UGC/AICTE-affiliated colleges. Its functions:
- Continuous monitoring of academic quality
- Annual Quality Assurance Report (AQAR) submission to NAAC
- Preparation for NAAC accreditation / re-accreditation
- NBA accreditation support (for engineering programmes)
- Action taken reports on improvement initiatives
- Student satisfaction surveys and closing-the-loop documentation

---

## 2. IQAC Structure

```
IQAC — GREENFIELDS COLLEGE OF ENGINEERING
Constituted as per NAAC guidelines

COMPOSITION:
  Chairperson: Dr. P.K. Rao (Principal/Director)
  IQAC Coordinator: Dr. Anita K. (senior faculty)
  HODs (all 5 departments): Members
  2 senior faculty members: Dr. Ramesh M., Ms. Neeraja R.
  Administrative officer: Mr. V. Suresh (Registrar)
  1 industry expert: Mr. T. Kishore (Senior Engineer, TCS — external)
  2 alumni members: Mr. Rohan S. (2022–26 batch), Ms. Priya D. (2020–24 batch)
  1 student representative: Mr. Aakash Sharma (student council president)

MEETING FREQUENCY: Minimum 2 per semester (NAAC requirement)
Last meeting: 15 March 2027 ✅  |  Next: June 2027 (end of semester)
```

---

## 3. AQAR (Annual Quality Assurance Report)

```
AQAR — 2025–26
Submitted to NAAC: ✅ 15 September 2026 (deadline: 30 Sep)

AQAR CRITERION SCORES (self-assessment):
  Criterion 1 — Curricular Aspects:               3.42 / 4.00  ⚠
  Criterion 2 — Teaching-Learning & Evaluation:   3.68 / 4.00  ✅
  Criterion 3 — Research, Innovations & Extension: 2.84 / 4.00  ⚠
  Criterion 4 — Infrastructure & Learning Resources: 3.52 / 4.00  ✅
  Criterion 5 — Student Support & Progression:    3.64 / 4.00  ✅
  Criterion 6 — Governance, Leadership & Management: 3.71 / 4.00  ✅
  Criterion 7 — Institutional Values & Best Practices: 3.44 / 4.00  ⚠

COMPOSITE SCORE: 3.46 / 4.00 (B+ Grade estimate — NAAC scale)
Current NAAC grade: B+ (awarded 2024, valid until 2029)

GAPS IDENTIFIED (for improvement before re-accreditation 2029):
  C1: Curriculum not yet fully aligned with NEP 2020 (4-year structure approved but not yet fully deployed)
  C3: Research publications below target (3.2 publications/faculty/year; target: 4.0)
  C7: Green Campus initiatives — need ECBC (Energy Conservation Building Code) audit

ACTION PLAN 2026–27:
  C1: Complete NEP 2020 Year-1 and Year-2 curriculum review by Dec 2026 ← in progress
  C3: Mandate 1 NPTEL FDP per faculty; 2 publications per faculty → faculty appraisal incentive
  C7: Green audit scheduled July 2027 (external agency)
```

---

## 4. Quality Improvement Initiatives

```
QUALITY INITIATIVES DASHBOARD — 2026–27

Initiative                              Target     Status    Lead
─────────────────────────────────────────────────────────────────────
NEP 2020 curriculum rollout             Dec 2026   ✅ Done   Dean Academics
Industry MOU (3 new per year)           3 MOUs     2/3 ✅    Placement Cell
Research paper per faculty              ≥2/year    1.4 avg ⚠ HODs
NPTEL courses (student)                 ≥20/sem    24 ✅     NPTEL Coord.
Student satisfaction survey             ≥80%       82.4% ✅  IQAC Coord.
CIE Moderation (HOD review of marks)   100%        91% ⚠    All HODs
NBA criterion documentation (CSE dept)  Ready by Dec  In progress ← priority

STUDENT SATISFACTION SURVEY 2026–27:
  Overall satisfaction: 82.4% (satisfied or highly satisfied)
  Key positive areas: Campus infrastructure (89%), Library (86%), Faculty (84%)
  Improvement areas: Cafeteria (68%), Placement support (72%), Internet speed (71%)

ACTION TAKEN:
  Cafeteria: FSSAI complaint resolved; new vendor from Jun 2026 — satisfaction risen ✅
  Placement: Additional placement drives planned Q4 (8 companies added)
  Internet: 1Gbps upgrade from 500Mbps — Jan 2027 ✅
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/iqac/aqar/` | Annual Quality Assurance Report data |
| 2 | `POST` | `/api/v1/college/{id}/iqac/aqar/submit/` | Submit AQAR to NAAC |
| 3 | `GET` | `/api/v1/college/{id}/iqac/initiatives/` | Quality improvement initiatives tracker |
| 4 | `POST` | `/api/v1/college/{id}/iqac/meeting/` | Log IQAC meeting minutes |
| 5 | `GET` | `/api/v1/college/{id}/iqac/satisfaction-survey/` | Student satisfaction results |
| 6 | `GET` | `/api/v1/college/{id}/iqac/naac-readiness/` | Pre-NAAC readiness assessment |

---

## 6. Business Rules

- AQAR must be submitted to NAAC every year by 30 September for the previous academic year; a college that misses AQAR submission risks losing NAAC accreditation (NAAC can put colleges on "watch" for repeated AQAR failures)
- IQAC must have external members (industry + alumni + student representative) as per NAAC guidelines; an IQAC composed only of internal faculty is a NAAC gap; all members must be documented with their credentials
- The "closing the loop" evidence — "we identified a problem, we took an action, here is the result" — is what separates high-scoring from average-scoring institutions on NAAC criterion 6; EduForge's initiative tracker with target-status-lead structure directly generates this evidence

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division B*
