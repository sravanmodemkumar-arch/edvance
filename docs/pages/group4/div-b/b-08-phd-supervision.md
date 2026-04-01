# B-08 — Ph.D. Supervision Management

> **URL:** `/college/academic/phd/`
> **File:** `b-08-phd-supervision.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Ph.D. Supervisor (S4–S5 faculty with Ph.D. + publications) · Registrar (S4) · Dean Research (S5) · University Research Cell (external) · Ph.D. Scholar (S1-PhD)

---

## 1. Purpose

Colleges with university research centres host Ph.D. scholars under faculty supervisors. Ph.D. management involves:
- Scholar registration with university (JNTU Research Cell)
- Course work tracking (first-year Ph.D. course work is mandatory under UGC 2022 regulations)
- Progress reports (6-monthly) submitted to supervisors and university
- Pre-submission seminar management
- Thesis submission and evaluation
- Award of degree

---

## 2. Ph.D. Scholar Registry

```
PH.D. SCHOLARS — GCEH (Active)
Academic Year: 2026–27

Approved Research Supervisors (JNTU recognized): 8 faculty

ACTIVE SCHOLARS:
  Scholar ID   Name          Supervisor      Topic                        Year  Status
  PHD-GCEH-001 Ms. Roja P.   Dr. Anita K.    "Deep Learning for IoT"      3rd   Pre-submission ✅
  PHD-GCEH-002 Mr. Suresh N. Dr. Ramesh M.   "Cloud Computing Security"   2nd   Course work done ✅
  PHD-GCEH-003 Ms. Kavitha D. Dr. Anita K.  "NLP for Regional Languages" 1st   Course work Y1 ⏳
  PHD-GCEH-004 Mr. Arun T.    Dr. Ravi P.    "Renewable Energy Grid"      1st   Registration ⬜

SUPERVISOR LOAD (JNTU rule: max 8 scholars per supervisor):
  Dr. Anita K.:   2 scholars ✅ (max 8)
  Dr. Ramesh M.:  1 scholar ✅

UGC 2022 Ph.D. REGULATION:
  Mandatory: 1 year of coursework (12–16 credits)
  Mandatory: Publish minimum 1 paper in UGC-CARE listed journal before thesis submission
  Mandatory: Pre-submission seminar open to department
  Mandatory: Anti-plagiarism check (iThenticate/Turnitin < 10% similarity)
```

---

## 3. Scholar Progress Tracking

```
PH.D. PROGRESS — Ms. Roja P. (PHD-GCEH-001)
Supervisor: Dr. Anita K.  |  Topic: "Deep Learning for IoT"
Registration: JNTU/PHD/GCEH/2024/001  |  Registered: June 2024

COURSE WORK (Year 1 — 2024–25):
  Research Methodology: 4 credits — ✅ A grade
  Advanced Algorithms: 4 credits — ✅ B+ grade
  Elective (Machine Learning): 4 credits — ✅ A+ grade
  Total course credits: 12 ✅ (UGC minimum met)

PROGRESS REPORTS:
  6-monthly reports:
    Report 1 (Dec 2024): ✅ Submitted; Supervisor: "Good literature review"
    Report 2 (Jun 2025): ✅ Submitted; Supervisor: "Experiments completed"
    Report 3 (Dec 2025): ✅ Submitted; Supervisor: "Paper published"
    Report 4 (Jun 2026): ✅ Submitted; Supervisor: "Thesis draft in progress"
    Report 5 (Dec 2026): ✅ Submitted; Supervisor: "Pre-submission ready"

PUBLICATIONS:
  Paper 1: "IoT Data Classification using CNN" — IEEE IoT Journal (SCIE indexed) ✅
  Paper 2: "Edge Computing for Real-time IoT" — IJCA (UGC-CARE) ✅

ANTI-PLAGIARISM:
  Thesis draft checked: iThenticate — 7.2% similarity ✅ (under 10%)

STATUS: Ready for Pre-submission Seminar → Thesis submission Q1 2027
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/phd/scholars/` | All Ph.D. scholars |
| 2 | `GET` | `/api/v1/college/{id}/phd/scholars/{scholar_id}/` | Individual scholar progress |
| 3 | `POST` | `/api/v1/college/{id}/phd/progress-report/` | Submit 6-monthly progress report |
| 4 | `GET` | `/api/v1/college/{id}/phd/supervisor/{faculty_id}/scholars/` | Supervisor's scholars |
| 5 | `POST` | `/api/v1/college/{id}/phd/thesis/anti-plagiarism/` | Upload and check plagiarism report |

---

## 5. Business Rules

- UGC 2022 Ph.D. regulations are mandatory for all UGC-recognised universities and their affiliated research centres; course work, publications, and anti-plagiarism are non-negotiable; a thesis submitted without these checks will be rejected at the university's doctoral committee
- Maximum scholar load (8 per supervisor) is a UGC regulation; exceeding this is a compliance violation; supervisors with 8 scholars cannot take new registrations until one of their scholars submits; EduForge enforces this cap
- Publication in a UGC-CARE listed journal (not just any journal) is mandatory; predatory journal publications are not accepted; EduForge's publication tracker validates against a UGC-CARE list (updated periodically)

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division B*
