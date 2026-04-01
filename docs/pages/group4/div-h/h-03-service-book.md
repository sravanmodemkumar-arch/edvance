# H-03 — Service Book & Career Progression

> **URL:** `/college/hr/service-book/`
> **File:** `h-03-service-book.md`
> **Priority:** P1
> **Roles:** HR Officer (S3) · Finance Manager (S4) · HOD (S4) · Principal/Director (S6)

---

## 1. Service Book

```
SERVICE BOOK — Dr. Suresh K. (Associate Professor, CSE)
GCEH Service No: GCEH/CSE/2015/012

PERSONAL DETAILS:
  Name: Dr. Suresh Kumar
  DOB: 15 March 1982 (Age: 45 years 12 days)
  Gender: Male
  Category: OBC (Certificate: BC-A Telangana)
  Marital status: Married
  Permanent address: 14-5-301, Secunderabad — 500015
  Emergency contact: Wife — 9849XXXXXX

QUALIFICATIONS:
  B.Tech (CSE): JNTU Hyderabad, 2004 (79.2%)
  M.Tech (CSE): JNTU Hyderabad, 2006 (82.4%)
  PhD (CSE): IIT Hyderabad, 2012 ("Distributed Computing Security")
  NET: Qualified 2007 (UGC — Computer Science)

APPOINTMENT HISTORY:
  Entry: 15 July 2015 — Assistant Professor, Level 10 (₹15,600 + AGP ₹6,000)
  Promotion: 15 July 2021 — Associate Professor, Level 12 (API score 342 ✅)
  Current level: Level 12 (Stage 4) — Basic ₹1,12,400 (as of Jan 2026)

PAY INCREMENTS (annual — 1 July each year):
  Jul 2025: ₹1,07,100 → ₹1,12,400 (one increment: 3% under 7th CPC matrix)
  Jul 2026: ₹1,12,400 → ₹1,18,000 (projected — next increment)

LEAVE RECORD SUMMARY:
  EL (Earned Leave) balance: 42 days (max 300 — accumulates 15 days/6 months)
  CL (Casual Leave) availed 2026–27: 8 of 12 days used
  Academic Leave (FDP/conference): 12 days (2026–27)
  Duty Leave (duty purposes): 4 days (NAAC coordination)

DISCIPLINARY PROCEEDINGS: None

TRAINING / FDP ATTENDED:
  2023: SERB-sponsored workshop on Federated Learning (IIT Bombay, 5 days)
  2024: NAAC Coordinator training (NIT Warangal, 2 days)
  2025: IEEE-sponsored conference (Singapore — Best Paper Award)
  2026: AICTE ATAL FDP (Cybersecurity — 5 days)

PUBLICATIONS (for API): 18 papers (Scopus/UGC-CARE) in service
```

---

## 2. Career Progression (CAS)

```
CAREER ADVANCEMENT SCHEME (CAS) — UGC/AICTE
(Promotion based on API score — Academic Performance Indicator)

CAS CATEGORIES:
  Category I:   Teaching, Learning & Evaluation (max 125/year)
  Category II:  Research, Publications & Academic Contributions (max 150/year)
  Category III: Research Projects, Consultancy, Admin & Ext. Activities (max 75/year)
  Total maximum: 350/year

PROMOTION RULES:
  Asst. Prof. Level 10 → 11: 4 years in Level 10 + API ≥100 (last 4 years)
  Asst. Prof. Level 11 → 12 (Assoc. Prof.): 4 years + API ≥300 cumulative (8 years)
  Assoc. Prof. Level 12 → 13A: 3 years + API ≥100 (last 3 years)
  Assoc. Prof. → Professor: Minimum 10 years total + API ≥400 cumulative + Selection

API SCORE — Dr. Suresh K. (current year 2026–27):
  Category I (Teaching):
    Classes taught (26 periods/week × 6 months): 70 points
    Student feedback score (4.2/5 → 84%): 20 points
    Examination duties: 5 points
    Category I total: 95 / 125

  Category II (Research):
    Scopus papers (Q1 journal): 12 points × 1 = 12
    Scopus papers (Q2 journal): 8 points × 3 = 24
    Conference papers (Scopus proceedings): 4 × 2 = 8
    Funded project (PI, ₹28.4L SERB): 30 points
    PhD supervision: 5 points × 2 scholars = 10
    Category II total: 84 / 150

  Category III:
    Consultancy (₹7.2L revenue): 15 points
    Departmental admin (coordinator): 5 points
    FDP attended (5 days ATAL): 10 points
    Category III total: 30 / 75

  TOTAL API (2026–27): 209 / 350

CUMULATIVE API (since joining 2015):
  Previous years (11 years × avg 188): 2,068
  Current year: 209
  TOTAL: 2,277 ← comfortably above Professor threshold (400 cumulative needed at promotion time)
  Next promotion eligibility: Professor (if Level 13A available — depends on vacancy)
```

---

## 3. Service Book Events

```
SERVICE BOOK EVENT LOG (EduForge — Dr. Suresh K.)

Event Type         | Date        | Details                              | Approved by
─────────────────────────────────────────────────────────────────────────────────────────
Joining            | 15 Jul 2015 | Asst. Prof., Level 10, Basic ₹15,600 | Principal ✅
Confirmation       | 15 Jul 2016 | Probation completed satisfactorily    | Principal ✅
Increment          | 1 Jul 2016  | ₹15,600 → ₹16,100                    | HR Office ✅
...
Promotion          | 15 Jul 2021 | Assoc. Prof., Level 12 (CAS — API 342)| Governing Body ✅
Increment          | 1 Jul 2021  | ₹1,01,500 (Level 12 start)            | HR Office ✅
...
Annual Increment   | 1 Jul 2026  | ₹1,12,400 → ₹1,18,000               | HR Office ✅
FDP Leave          | 14 Jan 2027 | ATAL FDP 14-18 Jan (duty leave 5 days)| Principal ✅
Conference Leave   | 12 Feb 2027 | IEEE Conf — Singapore (academic leave) | Principal ✅

PENDING EVENTS:
  ⬜ Annual Increment (1 Jul 2027): System auto-initiates in May 2027 for Jul approval
  ⬜ Promotion review (Level 12 → 13A): Eligible from 15 Jul 2024 (3 years in Level 12)
      API check: 2024–26 API = 387 (>100/year × 3 ✅) → eligible for review
      Action: Promotion committee to be constituted (after Governing Body meeting)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hr/service-book/{faculty_id}/` | Service book detail |
| 2 | `POST` | `/api/v1/college/{id}/hr/service-book/{faculty_id}/event/` | Add service book event |
| 3 | `GET` | `/api/v1/college/{id}/hr/api-score/{faculty_id}/` | API score computation |
| 4 | `GET` | `/api/v1/college/{id}/hr/promotions/eligible/` | Faculty eligible for promotion |
| 5 | `POST` | `/api/v1/college/{id}/hr/promotions/{faculty_id}/process/` | Initiate CAS promotion |

---

## 5. Business Rules

- Service book entries must be made within 7 working days of each event (joining, promotion, increment, leave record etc.); a service book that is months out of date is unreliable evidence in disputes; AICTE inspectors and NAAC peer teams verify that service books are current; EduForge auto-notifies the HR Officer to update the service book within 7 days of each payroll event
- CAS promotions cannot be denied if the faculty member meets the API threshold and has completed the minimum years; arbitrary denial of promotion without documented reason is an illegal act that courts have consistently ruled against; the Governing Body's role in CAS is ratification, not discretionary blocking; if the Selection Committee recommends promotion based on API, the Governing Body cannot reject without specific academic reasons
- Annual increments on 1 July each year are automatic (unless under disciplinary proceedings); withholding an increment without a formal written order (under service rules) is illegal; if the faculty member's performance is unsatisfactory, the proper process is a formal warning, then adverse entry in service book, then increment withholding order — not silent non-payment
- API self-assessment by faculty must be verified; faculty who inflate Category II scores (claiming Q1 publications for predatory journals, claiming consultancy amounts not actually received) during CAS evaluation are committing academic fraud; EduForge's API module cross-checks publications against Scopus DOI database and consultancy claims against finance records before allowing the API calculation to be finalised
- The service book is the primary employment record; it must survive beyond the faculty member's tenure; GCEH must maintain service books for 5 years after retirement; digital copies in EduForge supplement but do not replace the physical service book (courts typically require physical evidence in service disputes)

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division H*
