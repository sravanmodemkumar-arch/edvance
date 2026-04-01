# C-19 — CWSN Register

> **URL:** `/school/students/cwsn/`
> **File:** `c-19-cwsn-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Class Teacher (S3) — own class · Administrative Officer (S3) — full · Principal (S6) — full

---

## 1. Purpose

Maintains the register of Children With Special Needs (CWSN) — students with physical, visual, hearing, intellectual, or multiple disabilities enrolled in the school. Under:
- **RTE Act 2009 Section 3:** Every child with disability has the right to free and compulsory education in an inclusive setting (regular school)
- **RPwD Act 2016 (Rights of Persons with Disabilities):** Mandates inclusive education; 21 categories of disability recognised; schools must provide "reasonable accommodations"
- **CBSE Guidelines:** CWSN students registered with CBSE get exam accommodations — extra time (20–60 minutes), scribe, large print question paper, rest breaks. The school must submit the CWSN list to CBSE before board exam registration (B-33)
- **UDISE:** CWSN count is a mandatory field in UDISE submission (C-17)

This register is not just a document — it drives operational decisions: exam hall seating (B-13 — ramp access, front row), timetable (B-07 — no stairs for wheelchair users), exam configuration (B-11 — accommodation codes), and report card notes.

---

## 2. Page Layout

### 2.1 Header
```
CWSN Register                                 [+ Add Student]  [Export for CBSE]  [Export for UDISE]
Total CWSN Students: 5  ·  Board Exam CWSN: 2 (Classes IX–XII)  ·  Accommodation Letters Issued: 2
```

### 2.2 CWSN Register Table
| Roll/Class | Student | Disability Type | Severity | IEP | Exam Accom. | CBSE Reg. | Status |
|---|---|---|---|---|---|---|---|
| IX-A / 12 | Ravi M. | Visual (Low Vision) | Moderate | ✅ | Extra Time 30 min | ✅ Registered | Active |
| X-B / 08 | Meena S. | Hearing (SNHL) | Moderate | ✅ | No audio component | ✅ Registered | Active |
| VI-A / 22 | Arun D. | Intellectual (Mild ID) | Mild | ✅ | N/A (not board class) | — | Active |
| III-B / 15 | Priya T. | Locomotor | Moderate | ✅ | Ground floor class | — | Active |
| I-A / 05 | Kavya R. | Autism Spectrum | Mild | ✅ | Resource room access | — | Active |

---

## 3. CWSN Student Record

### 3.1 Disability Details
| Field | Value |
|---|---|
| Student | Ravi Menon (STU-0001050) |
| Disability Type | Visual Impairment — Low Vision |
| Disability Sub-type | Low Vision (not blind) |
| RPwD Category | Visual Impairment (Category 01 — RPwD Act 2016) |
| Severity | Moderate |
| Disability Certificate No. | APDC/2024/08421 |
| Certificate Issuing Authority | SADGURU Netralay, Hyderabad |
| Certificate Date | 15 Aug 2024 |
| Certificate Valid Until | 15 Aug 2027 |
| Disability % | 48% |
| Certificate Uploaded | ✅ [View PDF] |

### 3.2 Functional Profile
| Aspect | Description |
|---|---|
| Reads large print | Yes (font size 18pt minimum) |
| Uses magnifier | Yes — personal magnifier device |
| Mobility | Independent |
| Communication | Normal — speaks and writes |
| Learning Needs | Needs large-print worksheets; extra time for reading tasks |
| Support Person | No dedicated aide |

### 3.3 IEP (Individualized Education Plan)
```
IEP — Ravi Menon — 2026–27

Goal 1: Improve reading fluency using magnifier
  Responsible: English Teacher (Ms. Anita)
  Progress Review: Monthly

Goal 2: Mathematics problem completion with extra time
  Responsible: Math Teacher (Ms. Priya)
  Progress Review: Monthly

Goal 3: Use low-vision aids independently
  Responsible: Resource Teacher + Class Teacher
  Progress Review: Quarterly

Annual Review Date: 15 Mar 2027
Parent Agreement: ✅ Signed (10 Apr 2026)
```

### 3.4 School Accommodations
| Accommodation | Details |
|---|---|
| Classroom Seating | Front row, near window / good lighting |
| Class assignments | Large print worksheets (18pt font) |
| Lab work | Paired with lab partner for measurement tasks |
| Sports / PE | Modified participation — no ball sports with fast-moving objects |
| Extra time in class tests | 10 minutes per 30-minute test |
| Floor preference | Ground floor class (in case of vision deterioration) |

### 3.5 Board Exam Accommodations (CBSE)
| Accommodation | CBSE Code | Approved |
|---|---|---|
| Extra time: 30 minutes | ET-30 | ✅ Approved by CBSE |
| Large print question paper (18pt) | LP | ✅ Approved |
| Own magnifier device | EQPT | ✅ Approved |

CBSE accommodation approval letter uploaded: ✅ [View PDF]

---

## 4. Disability Types Supported

| Category (RPwD 2016) | Examples | Common School Accommodations |
|---|---|---|
| Visual Impairment | Low vision, blindness | Extra time, scribe, large print, Braille |
| Hearing Impairment | SNHL, deafness | No audio component, sign language interpreter |
| Locomotor Disability | Wheelchair, polio, CP | Ground floor, ramp, extra time |
| Intellectual Disability | Mild/moderate ID, Down syndrome | Simplified language, extra time, scribe |
| Autism Spectrum | ASD (various levels) | Separate room, structured breaks, visual schedules |
| Learning Disability | Dyslexia, dyscalculia, dysgraphia | Scribe, extra time, oral examination option |
| Multiple Disabilities | Combination of above | Combined accommodations |
| Chronic Neurological | Epilepsy, cerebral palsy | Medical emergency plan, extra time |
| Specific Learning Disability | Dyslexia (CBSE specific category) | CBSE: scribe, extra time per board circular |

---

## 5. CBSE Board Exam Registration Link

For CWSN students in Classes IX–XII:

```
Board Exam CWSN Registration — 2026 (Class X Board)

Student: Ravi Menon  |  CWSN Type: Visual Impairment  |  Accommodation: ET-30 + LP

Required for CBSE LOC (B-33):
  ✅ Disability certificate uploaded
  ✅ Medical certificate from district medical board
  ✅ Accommodation request letter from school
  ✅ Submitted to CBSE via Saras portal

CBSE Approval Reference: CBSE/CWSN/2026/AP/08421
```

This data is pushed to B-33 (Board Exam Registration) automatically when B-33 LOC is being prepared.

---

## 6. Export for CBSE

[Export for CBSE] → generates the CBSE CWSN list in prescribed format:

```
CWSN LIST — [SCHOOL NAME] — CBSE Affiliation: AP2000123
For Board Examination: March 2026

S.No.  Student Name      Class  Roll  Disability     % Disability  Accommodation Requested
1      Ravi Menon        X-B    12    Visual (LV)    48%           ET-30, Large Print
2      Meena Sharma      X-A    08    Hearing (SNHL) 55%           No Audio Component
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/cwsn/?year={year}` | CWSN register |
| 2 | `POST` | `/api/v1/school/{id}/students/cwsn/` | Add CWSN student |
| 3 | `GET` | `/api/v1/school/{id}/students/cwsn/{student_id}/` | CWSN record detail |
| 4 | `PATCH` | `/api/v1/school/{id}/students/cwsn/{student_id}/` | Update CWSN record |
| 5 | `PATCH` | `/api/v1/school/{id}/students/cwsn/{student_id}/iep/` | Update IEP |
| 6 | `GET` | `/api/v1/school/{id}/students/cwsn/cbse-list/?year={year}` | CBSE exam CWSN list |
| 7 | `GET` | `/api/v1/school/{id}/students/cwsn/export/` | Export CBSE format list |

---

## 8. Business Rules

- A valid disability certificate from a competent authority (District Medical Board, SADGURU-recognised institution, or equivalent) is required before the student can be registered as CWSN in EduForge
- IEP must be reviewed at least annually; system alerts class teacher and Admin Officer 30 days before IEP review date
- CBSE exam accommodation requests must be submitted to CBSE by the date specified in the CBSE circular (typically November–December for March board exams); the system creates a task in A-23 Approval Workflow 60 days before the CBSE deadline
- Accommodation decisions (seating, floor, extra time) are pushed to B-11 Exam Configuration, B-13 Seating Arrangement, and B-35 Practical Exam Coordinator automatically when confirmed
- CWSN data is sensitive personal data under DPDPA 2023 (health/disability category) — access is restricted; no bulk download of CWSN data is permitted without Principal authorisation

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
