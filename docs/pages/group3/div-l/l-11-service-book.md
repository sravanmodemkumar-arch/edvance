# L-11 — Service Book

> **URL:** `/school/hr/service-book/`
> **File:** `l-11-service-book.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** HR Officer (S4) — maintain · Principal (S6) — certify and sign annual entries · Staff (S3–S5) — view own service book only

---

## 1. Purpose

The service book is a permanent employment record for each employee — modelled on government service books, and required by most state education departments for recognised schools. It is the official record of:
- Date of joining, designation, and initial salary
- All increments and promotions (with dates and authority)
- All leave taken (type, duration, approving authority)
- Disciplinary actions (if any)
- Training and professional development
- Annual appraisal ratings (summary)
- Separation details

The service book is a legal document; entries must never be erased — only corrected with strikethrough, date, and authorising signature.

---

## 2. Service Book — Structure

```
SERVICE BOOK

School: GREENFIELDS SCHOOL, Hyderabad
CBSE Affiliation No.: 1200XXX

Employee: Ms. Geeta Sharma
Employee ID: TCH-031
Date of Birth: 12 April 1984
Date of Joining: 10 July 2018

SECTION 1: PERSONAL DETAILS
  Father's name: Mr. Suresh Sharma
  Permanent address: Flat 4, Lakeview Apts, Dilsukhnagar, Hyderabad 500036
  Emergency contact: Mr. Ramesh Sharma (husband) — +91 9765-XXXXX
  Educational qualifications: B.A. (History) Osmania 2005; B.Ed. HCU 2007
  CTET: Certificate CTET/2018/XXXX ✅

SECTION 2: APPOINTMENT & INCREMENTS
  Date       Entry                                     Authority          Basic (₹)
  10 Jul 2018 Joined as Teacher — T-2 Band              Principal           32,000
  10 Jul 2019 Probation confirmed — permanent service   Principal           32,000
  1 Apr 2019  Annual increment                          Principal           34,000
  1 Apr 2020  Annual increment                          Principal           36,000
  1 Apr 2021  Annual increment                          Principal           38,000
  1 Apr 2022  Annual increment + merit                  Principal           41,000
  1 Apr 2023  Annual increment                          Principal           43,000
  1 Apr 2024  Annual increment                          Principal           45,000
  1 Apr 2025  Promotion: T-2 → T-3 (Senior Teacher)    Principal           48,000
  1 Apr 2025  Annual increment (T-3)                    Principal           48,000
  1 Apr 2026  Annual increment (T-3, merit)             Principal           51,000

SECTION 3: LEAVE RECORD
  Year     EL    CL    SL    Mat.  LOP   Notes
  2018–19   0     2     1     0     0
  2019–20   3     4     0     0     0
  2020–21   0     2     5     0     0     COVID period — special leave
  2021–22   2     3     0     0     0
  2022–23   1     2     2     0     0
  2023–24   4     4     0     0     0
  2024–25   2     2     1     0     0
  2025–26   2     2     0     0     0

SECTION 4: DISCIPLINARY RECORD
  No disciplinary action taken in service ✅

SECTION 5: TRAINING
  [Summary of L-07 training record — POCSO, CBSE orientations, external workshops]

SECTION 6: APPRAISAL
  2018–19: Meets Expectations  ·  2019–20: Exceeds Expectations
  2020–21: Meets Expectations (COVID disruptions)
  2021–22: Exceeds Expectations  ·  2022–23: Exceeds Expectations
  2023–24: Exceeds Expectations  ·  2024–25: Outstanding (→ promotion trigger)
  2025–26: Exceeds Expectations

Annual certification by Principal:
  Each year end: "I certify that the entries in Sections 1–6 for the year [YYYY–YY]
  are complete and accurate."
  Principal signature + date

[Download service book PDF]  [Export CBSE format]
```

---

## 3. Service Book Maintenance Rules

```
Service Book — Maintenance Standards

Entries:
  ✅ Every entry must be dated and signed by the authorising officer (typically Principal)
  ✅ Entries are made in ink (physical books) or digitally with audit trail (EduForge)
  ✅ No erasure; corrections: single strikethrough + initial of authorising officer + date
  ✅ Annual certification by Principal at year-end

Physical vs Digital:
  EduForge maintains the digital service book (all entries, audit trail)
  Many state education departments still require a physical service book (register format)
  EduForge generates a printable physical service book PDF annually for schools
  that require the physical version.

On separation:
  Physical service book (if maintained): Returned to employee on request
  Digital record: Archived in EduForge for 7 years post-separation

On transfer to another school:
  Service book is transferred with the employee (physical copy)
  Digital record: School generates a "service certificate" PDF export for the new employer
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hr/service-book/{staff_id}/` | Service book |
| 2 | `POST` | `/api/v1/school/{id}/hr/service-book/{staff_id}/entry/` | Add service book entry |
| 3 | `POST` | `/api/v1/school/{id}/hr/service-book/{staff_id}/certify/` | Principal annual certification |
| 4 | `GET` | `/api/v1/school/{id}/hr/service-book/{staff_id}/export/` | Export service book PDF |

---

## 5. Business Rules

- The service book is a permanent legal document; it is never deleted from EduForge, even after separation; data retention: 7 years minimum post-separation (Income Tax Act requirement for employment records)
- Every increment, promotion, and salary revision must be entered in the service book by the Principal; entries without Principal authorisation are invalid
- Disciplinary entries (warnings, PIP, suspension) must be entered by the Principal; an employee can note their objection in the service book if they disagree with an entry (standard service record practice)
- Annual certification: the Principal certifies each year's entries are complete; this is the Principal's attestation that the record is accurate; a service book without annual certification is considered incomplete for CBSE inspection
- In case of dispute (gratuity claim, increment claim), the service book is the authoritative record; courts accept service books as primary evidence

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division L*
