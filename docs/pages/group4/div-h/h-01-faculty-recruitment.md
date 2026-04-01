# H-01 — Faculty Recruitment & Appointment

> **URL:** `/college/hr/recruitment/`
> **File:** `h-01-faculty-recruitment.md`
> **Priority:** P1
> **Roles:** HR Officer (S3) · HOD (S4) · Dean Academics (S5) · Principal/Director (S6) · Governing Body (S7)

---

## 1. Recruitment Process

```
FACULTY RECRUITMENT — GCEH 2026–27

OPEN POSITIONS (March 2027):
  CSE:  1 Assistant Professor (PhD preferred — to improve TLR2/NIRF)
  EEE:  1 Associate Professor (PhD required — NBA deficiency correction)
  Mech: 1 Assistant Professor (NBA deficiency — 4 faculty without PhD flagged)

MINIMUM QUALIFICATIONS (UGC Minimum Qualifications Regulations 2018 + AICTE 2019):
  Assistant Professor:
    Must have: PG with ≥55% + NET/SET (UGC/CSIR/SET of state) OR
               PhD with NET/SET exemption (UGC 2009 notification)
    AICTE add-on: B.Tech + M.Tech (for engineering disciplines)
    Desirable: PhD; teaching experience; publications

  Associate Professor:
    Must have: PhD in relevant subject
    Must have: 8 years post-PhD teaching/research experience
    Must have: API score ≥300 (across categories, per UGC promotion guidelines)
    AICTE: Total experience ≥10 years including 3 as Assistant Prof.

  Professor:
    PhD + 10 years experience (5+ years as Assoc. Prof.) + API ≥400

RECRUITMENT PROCESS:
  Step 1: HOD submits vacancy report to Principal (with justification)
  Step 2: Principal approves; HR Officer drafts advertisement
  Step 3: Governing Body approves (for Assoc. Prof. and above)
  Step 4: Advertisement published:
            GCEH website, AICTE portal, naukri.com/academic portals, newspaper (local)
  Step 5: Applications screened by Selection Committee
  Step 6: Selection Committee constituted per UGC norms:
            Chairperson: Principal
            Subject expert (external, from university/reputed institution): 1
            Subject HOD: 1
            Senior faculty: 1
            SC/ST/OBC representative (if applicable): 1
  Step 7: Written test (if many applicants) + demo lecture + interview
  Step 8: Selection committee minutes → Principal → Governing Body ratification
  Step 9: Appointment letter issued
```

---

## 2. Selection Committee Record

```
SELECTION COMMITTEE MEETING — Assistant Professor (CSE)
Date: 20 March 2027

COMMITTEE:
  Chairperson: Dr. R. Venkataraman (Principal, GCEH)
  External Expert: Dr. Sunita R. (Professor, IIT Hyderabad — CSE)
  HOD CSE: Dr. Suresh K.
  Senior Faculty: Dr. Priya M.
  SC/ST Representative: Dr. Anand R.

APPLICATIONS RECEIVED: 28
SHORTLISTED (UGC qualifications met): 18
CALLED FOR INTERVIEW: 6 (shortlist after preliminary screening by HOD)

CANDIDATES INTERVIEWED:
  Candidate 1: Mr. Arun K. (PhD from JNTU, 3 yrs exp) — Demo: ML Basics
    Technical: 78/100  |  Demo: 82/100  |  Communication: 80/100
    Total: 80/100 (average) | API score: 280 (strong for Asst. Prof.)

  Candidate 2: Ms. Priya T. (M.Tech, NET qualified, 2 yrs exp) — Demo: DS
    Technical: 72/100  |  Demo: 88/100  |  Communication: 85/100
    Total: 80/100 | API score: 110 (NET + teaching; no publications)

  Candidate 3: Dr. Deepak R. (PhD 2024, 1 yr exp, 3 Scopus papers) — Demo: AI
    Technical: 90/100  |  Demo: 86/100  |  Communication: 82/100
    Total: 86/100 ← HIGHEST | API: 360 (publications + PhD + teaching)

  ...

RECOMMENDATION: Dr. Deepak R. (Score: 86/100)
  Justification: PhD qualification improves college NIRF score; publications strengthen
                 NAAC Criterion 3; excellent technical score

GOVERNING BODY RATIFICATION: Required (meeting scheduled 5 April 2027)

WAITLIST: Arun K. (2nd rank — 80/100) — to be offered if Deepak declines
```

---

## 3. Appointment Process

```
APPOINTMENT LETTER — Dr. Deepak R.
(Conditional — subject to Governing Body approval)

APPOINTMENT DETAILS:
  Designation: Assistant Professor
  Department: Computer Science & Engineering
  Pay: ₹57,700/month (AICTE scale — Entry Level 10: ₹57,700 basic)
    Pay band: Academic Grade Pay ₹6,000 (7th CPC rationalized)
  Starting date: 1 June 2027 (tentative — after current job notice period)
  Type: Regular (permanent post)
  Probation: 1 year (extendable by 1 year if unsatisfactory)

DOCUMENTS TO SUBMIT AT JOINING:
  ✅ Original degree certificates (PhD, M.Tech, B.Tech)
  ✅ PhD certificate from university (JNTU)
  ✅ UGC-NET certificate (or PhD exemption notification)
  ✅ Experience certificates (all previous employers)
  ✅ Relieving letter from current employer
  ✅ Passport photo (6 copies)
  ✅ Aadhaar, PAN (for payroll/TDS)
  ✅ Bank account details (NEFT for salary)
  ✅ Medical fitness certificate

BACKGROUND VERIFICATION:
  Degree verification: JNTU degree portal check ✅
  Previous employer verification: Email to prior HR + Digi-signed confirmation
  Criminal records: Police verification (form submitted to local station)

SERVICE BOOK CREATED: On joining (H-03 process)
EPF ENROLLMENT: On joining (H-02 process)
```

---

## 4. Roster / Reservation Compliance

```
RESERVATION ROSTER — GCEH (Non-minority private institution)

APPLICABILITY:
  Private unaided institutions: Not legally required to follow SC/ST/OBC reservation
                                 for faculty recruitment (no government grant)
  HOWEVER: NAAC and AICTE strongly encourage diversity; many institutions follow
            voluntarily as best practice

GCEH POLICY:
  Faculty reservation: Voluntary alignment with 50% OBC + 15% SC + 7.5% ST norm
  Current faculty diversity (62 faculty):
    General/OC: 38 (61.3%)
    OBC:        16 (25.8%)
    SC:          6 (9.7%)
    ST:          2 (3.2%)

  NAAC OI criterion rewards diversity — EduForge tracks and reports
  Selection criteria: Merit-based; reservation considered if equal scores

NON-TEACHING STAFF RECRUITMENT:
  Following similar process (HR Officer + Principal; no Governing Body for Grade IV)
  Notice period: 30 days
  Current vacancies: 2 lab assistants (ECE lab)

BACKGROUND VERIFICATION (non-teaching):
  Police verification mandatory (particularly security staff and hostel staff)
  School/college certificate verification
  Previous employment check (2-year minimum)
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hr/recruitment/positions/` | Open positions |
| 2 | `POST` | `/api/v1/college/{id}/hr/recruitment/application/` | Candidate application |
| 3 | `GET` | `/api/v1/college/{id}/hr/recruitment/applications/` | All applications (screened) |
| 4 | `POST` | `/api/v1/college/{id}/hr/recruitment/selection/` | Record selection committee result |
| 5 | `POST` | `/api/v1/college/{id}/hr/recruitment/appointment/` | Issue appointment letter |

---

## 6. Business Rules

- UGC Minimum Qualifications 2018 are mandatory for all colleges seeking UGC recognition; a college that appoints faculty without NET/PhD qualification (for Assistant Professor) is in violation and the appointments can be challenged; NAAC Criterion 2.4 specifically assesses faculty qualification — appointments without minimum qualifications reduce this score significantly; EduForge's recruitment module hard-validates minimum qualifications before allowing an appointment letter to be generated
- The Selection Committee must include an external subject expert (not from GCEH); an entirely internal selection committee for faculty appointments lacks independence and is a UGC violation; the external expert from a reputed institution brings academic credibility to the selection; their signature on the selection committee minutes is evidence that the process was independent
- Demo lectures are not optional for teaching faculty selection; a candidate who performs well in a written test but cannot explain concepts to students clearly is unsuitable; the demo lecture should be evaluated by the committee and weighted appropriately in the final score; EduForge's selection scorecard includes demo lecture as a mandatory component
- Appointment letters must clearly state: pay, probation period, service conditions, notice period, and the legal basis (AICTE scales); vague appointment letters that say only "as per college rules" create disputes; courts have awarded damages to faculty dismissed without following their own appointment letter terms
- For private unaided colleges, the Governing Body's ratification of senior appointments is governance best practice and is required by the UGC recognition conditions; appointments made without Governing Body approval can be challenged as unauthorized acts of the Principal; EduForge's workflow ensures Governing Body ratification step is mandatory for Assoc. Prof. and above

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division H*
