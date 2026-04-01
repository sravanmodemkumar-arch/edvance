# H-04 — Faculty Appraisal & API Scoring

> **URL:** `/college/hr/appraisal/`
> **File:** `h-04-appraisal.md`
> **Priority:** P1
> **Roles:** Faculty (S3) · HOD (S4) · Dean Academics (S5) · Principal/Director (S6)

---

## 1. Annual Appraisal Process

```
ANNUAL APPRAISAL — GCEH 2026–27
(Academic year ending June 2027)

APPRAISAL TIMELINE:
  April: Faculty submit self-appraisal (EduForge portal)
  May:   HOD review and rating
  June:  Dean Academics / Principal review
  July:  Appraisal finalised; feedback communicated to faculty

APPRAISAL DIMENSIONS (weighted):

  A. TEACHING & EVALUATION (40%):
     A1. Classes taken vs scheduled (attendance regularity): /10
     A2. Syllabus completion %: /10
     A3. Student feedback score (avg): /10
     A4. Assessment quality (CIE papers, student marks distribution): /10

  B. RESEARCH & PUBLICATIONS (30%):
     B1. Publications this year (Scopus/WoS/UGC-CARE): /10
     B2. Funded projects (PI/Co-PI status): /10
     B3. PhD supervision progress: /5
     B4. Patents/consultancy: /5

  C. ADMINISTRATIVE & INSTITUTIONAL CONTRIBUTIONS (20%):
     C1. Committee membership + active participation: /10
     C2. Events organized / industry interactions: /5
     C3. Mentoring students (documentation quality): /5

  D. PROFESSIONAL DEVELOPMENT (10%):
     D1. FDP/workshops attended: /5
     D2. Online certifications / new skills: /5

TOTAL: 100 marks
```

---

## 2. Appraisal Records

```
FACULTY APPRAISAL — Dr. Suresh K. (CSE, Assoc. Prof.)
Academic Year: 2026–27

SELF-APPRAISAL SUBMITTED: 2 April 2027

A. TEACHING & EVALUATION:
  A1. Classes taken: 184 / 188 scheduled (97.9% — 4 classes: 2 duty leave, 2 FDP)
      Score: 9.5/10
  A2. Syllabus completion: CS201 (98%), CS301 (96%), CS401 (100%) → avg 98%
      Score: 9.8/10
  A3. Student feedback: 4.2/5 (84% satisfaction)
      Score: 8.4/10
  A4. CIE quality: Question paper reviewed by HOD (Bell curve: 72% pass) ✅
      Score: 8.0/10
  A TOTAL: 35.7 / 40

B. RESEARCH:
  B1. Publications: 4 papers (1 Q1, 2 Q2, 1 UGC-CARE)
      Score: 9.0/10
  B2. Funded projects: PI on SERB grant (₹28.4L) — active Year 2
      Score: 10/10
  B3. PhD scholars: 4 scholars (all on track; 2 papers published by scholars)
      Score: 4.5/5
  B4. Consultancy: ₹7.2L (Cyient project completed); 1 patent filed
      Score: 4.5/5
  B TOTAL: 28.0 / 30

C. ADMINISTRATIVE:
  C1. NAAC Coordinator contribution + Departmental exam coordinator
      Score: 8.5/10
  C2. Organized 1 industry workshop; 3 guest lectures facilitated
      Score: 4.0/5
  C3. Mentoring: 15 student pairs; quarterly meeting logs complete ✅
      Score: 4.5/5
  C TOTAL: 17.0 / 20

D. PROFESSIONAL DEVELOPMENT:
  D1. ATAL FDP (5 days); IEEE Conf (Singapore — paper presented)
      Score: 5.0/5
  D2. AWS Cloud Practitioner certification (Dec 2026)
      Score: 4.5/5
  D TOTAL: 9.5 / 10

SELF-APPRAISAL TOTAL: 90.2 / 100

HOD REVIEW (Dr. Priya M. — HOD CSE):
  HOD assessment: 89.0/100 (minor downward adjustment on A4 — CIE variance pattern)
  HOD comment: "Dr. Suresh is a high performer; research output excellent;
                slight concern on CIE question difficulty variation across sections"
  HOD recommendation: Increment + recognition at annual faculty day ✅

PRINCIPAL REVIEW: 89/100 (accepted HOD assessment) | Date: 28 June 2027
FINAL APPRAISAL: 89/100 (Outstanding — top quartile)
```

---

## 3. Appraisal Distribution

```
APPRAISAL DISTRIBUTION — 2026–27 (All 62 Faculty)

RATING DISTRIBUTION:
  Outstanding (85–100):   14 faculty (22.6%)
  Excellent (70–84):      26 faculty (41.9%)
  Good (55–69):           16 faculty (25.8%)
  Satisfactory (40–54):    5 faculty (8.1%)
  Needs Improvement (<40): 1 faculty (1.6%) ← under performance management plan

BELL CURVE CHECK:
  Too many "Outstanding" would indicate grade inflation; NAAC expects realistic distribution
  GCEH distribution: Top quartile 22.6% is defensible (strong research culture in CSE)
  Finance impact: Top rating = increment + ₹5,000 recognition award (GCEH policy)

ADVERSE APPRAISAL:
  Faculty rated "Needs Improvement": Mr. Anil K. (Mech, 11 yrs exp — 0 publications, poor feedback)
    Score breakdown: Teaching 28/40, Research 8/30, Admin 6/20, Dev 2/10 = 44/100
    Action: PIP (Performance Improvement Plan) issued:
      Target: 1 paper submitted + attendance regularisation + feedback improvement
      Review: 3-month check-in (Oct 2027)
      Consequence if no improvement: Annual increment withheld (formal order)

APPRAISAL DISCLOSURE:
  Faculty sees their own rating + HOD comments: ✅
  Faculty does NOT see other faculty ratings: Confidential
  DPDPA: Appraisal data is sensitive personal data; HR Officer + HOD + Principal only
  NAAC evidence: Aggregate distribution (anonymised) submitted — not individual ratings
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hr/appraisal/cycle/{year}/` | Appraisal cycle status |
| 2 | `POST` | `/api/v1/college/{id}/hr/appraisal/{faculty_id}/self/` | Submit self-appraisal |
| 3 | `POST` | `/api/v1/college/{id}/hr/appraisal/{faculty_id}/hod-review/` | HOD review |
| 4 | `GET` | `/api/v1/college/{id}/hr/appraisal/distribution/` | Aggregate distribution (anonymised) |
| 5 | `GET` | `/api/v1/college/{id}/hr/appraisal/{faculty_id}/history/` | Multi-year appraisal history |

---

## 5. Business Rules

- Faculty appraisal must have a formal response mechanism; faculty who receive an appraisal they disagree with must have a documented channel to raise objections (to Dean Academics or a Review Committee) within 15 days; arbitrary appraisals with no appeal mechanism have been challenged in courts successfully; EduForge includes a "dispute appraisal" button with a 15-day window after result publication
- HOD self-appraisal for their own teaching must be reviewed by the Principal (not by the HOD themselves); a self-assessed HOD appraisal without independent review creates a conflict of interest; similarly, the Principal's appraisal must be reviewed by the Governing Body — this chain of accountability is a NAAC Criterion 6 requirement
- Performance Improvement Plans (PIPs) must be specific, measurable, and time-bound; a PIP that says "improve research output" is too vague to enforce; a PIP that says "submit 1 Scopus-eligible paper to a listed journal by 31 October 2027 and achieve student feedback ≥3.5/5 in next semester" is actionable; EduForge's PIP module structures this correctly
- Appraisal data is among the most sensitive HR data; access must be restricted to the specific faculty member (own data only), their HOD, and HR/Principal; a faculty member accidentally seeing another colleague's appraisal data can trigger workplace friction and legal action; EduForge enforces row-level data isolation in the appraisal module
- The connection between appraisal and CAS (Career Advancement Scheme) must be clear; API scoring (which drives CAS promotion) is computed from the same data that drives the appraisal; a faculty member who gets "Outstanding" in appraisal year after year but somehow doesn't qualify for promotion due to low API is experiencing a governance inconsistency; EduForge aligns the appraisal scoring with API computation to prevent this disconnect

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division H*
