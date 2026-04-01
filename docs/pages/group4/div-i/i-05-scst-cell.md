# I-05 — SC/ST/OBC Cell & Equal Opportunity

> **URL:** `/college/welfare/equal-opportunity/`
> **File:** `i-05-scst-cell.md`
> **Priority:** P1
> **Roles:** SC/ST Cell Coordinator (S4) · Welfare Officer (S4) · Principal/Director (S6)

---

## 1. SC/ST Cell

```
SC/ST CELL — GCEH
(UGC Equal Opportunity Guidelines + SC/ST Prevention of Atrocities Act 1989)

CELL COMPOSITION:
  Coordinator: Dr. Anand R. (Associate Professor, EEE) — SC category faculty
  Member: Ms. Deepa R. (Faculty, ECE) — ST category
  Member: Mr. Suresh M. (Contract Faculty, CSE)
  Student representative: Ravi K. (226J1A0412, SC category) ← annually elected

MANDATE:
  Monitor academic performance of SC/ST/OBC students
  Facilitate remedial coaching
  Handle caste-discrimination complaints
  Provide scholarship support (NSP, TS ePASS — see I-04)
  Conduct awareness programmes

STUDENT STATISTICS:
  SC students: 84 (15.1%) ← EAPCET 15% SC reservation
  ST students: 42 (7.6%)  ← EAPCET 7.5% ST reservation
  OBC students: 179 (32.2%)← EAPCET 27% OBC + 4% BC-E + 5% EWS overlap
  Total reserved category: 305 (54.9%)
  General/OC: 251 (45.1%)
```

---

## 2. Remedial Coaching

```
REMEDIAL COACHING PROGRAMME

PURPOSE:
  SC/ST/OBC students may enter with lower entrance scores (reservation advantage)
  Bridge the academic gap through supplementary teaching
  UGC Equal Opportunity guidelines encourage this explicitly

PROGRAMME STRUCTURE:
  Identification: First-month test scores + first CIE marks
    Threshold: Below 50% in Maths or Physics or Programming (first-year core subjects)
  Notification: Welfare Officer contacts student + parent (with sensitivity — not stigmatising)
  Enrolment: Voluntary (but strongly encouraged)

REMEDIAL CLASSES 2026–27 (First Year):
  Subjects: Maths-I (18 students enrolled), Physics (12), Programming in C (22)
  Timing: Saturday 2 PM – 4 PM (after regular classes)
  Faculty: Same subject teachers (extra duty — compensated ₹150/hour extra)
  Attendance: 74% average attendance ← lower than ideal (Saturday issue)
  Impact: Post-remedial CIE: Avg improvement 12 marks (50→62 out of 100)
  NAAC evidence: Criterion 5.1.1 (student learning support) ✅

COVERAGE:
  SC/ST enrolled in remedial: 78 of 126 (61.9%) — those who needed it
  OBC: 52 of 179 (29.1%)
  General: 0 (programme specifically for reservation-category students as equity measure)

NOTE ON LEGALITY:
  Offering remedial coaching ONLY to SC/ST/OBC students is permitted as
  "positive discrimination / affirmative action" — it is not reverse discrimination
  The purpose is equity, not exclusion of general category students from quality teaching
  General students are not prevented from attending — but are not specifically targeted
```

---

## 3. Discrimination Complaints

```
DISCRIMINATION COMPLAINT MECHANISM

CASTE-BASED DISCRIMINATION:
  Reported to: SC/ST Cell Coordinator (first level)
  Escalation: Principal → Governing Body
  External: National Commission for SC; National Commission for ST; MHRD (UGC)
  FIR: If offence under SC/ST Prevention of Atrocities Act 1989 → mandatory FIR

COMPLAINTS 2026–27:
  GRV-005 (Anonymous): Caste remark by lab instructor → Resolved (warning + sensitisation)
  1 verbal complaint (not formally lodged): Peer mockery about rural background
    → SC/ST Cell counsellor session; no formal complaint desired by student
    → Peer sensitisation workshop added to agenda

SENSITISATION PROGRAMMES:
  Constitution Day (26 November 2026): Special session on Dr. Ambedkar's legacy
    Speaker: External speaker from Dalit rights organisation (50 students attended)
  Anti-caste discrimination poster campaign: Campus posters (March 2026 — Phule's birthday)
  Faculty sensitisation: 1 session (included in DPDPA/POSH combined awareness session)

EQUAL OPPORTUNITY REGISTER (UGC requirement):
  Annual register: Available for inspection
  Contents: SC/ST/OBC enrolment, scholarship status, remedial coaching participation,
            complaints received and resolved
  Submitted to: UGC Equal Opportunity Cell (online portal) — ✅ Filed Nov 2026
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/welfare/equal-opportunity/statistics/` | SC/ST/OBC student data |
| 2 | `GET` | `/api/v1/college/{id}/welfare/remedial/enrolment/` | Remedial coaching register |
| 3 | `POST` | `/api/v1/college/{id}/welfare/equal-opportunity/complaint/` | Discrimination complaint |
| 4 | `GET` | `/api/v1/college/{id}/welfare/equal-opportunity/ugc-report/` | UGC EOC annual report data |

---

## 5. Business Rules

- The SC/ST Cell must have a faculty member from SC/ST category as coordinator; a cell coordinated entirely by general category faculty loses the trust of SC/ST students who may be reluctant to report discrimination to those who may not appreciate its impact; UGC guidelines recommend this and NAAC peer teams verify it during site visits
- Caste-based discrimination is a criminal offence under the SC/ST Prevention of Atrocities Act 1989; a college that investigates such complaints purely as an "internal matter" and issues only warnings without filing FIR (when the facts warrant it) is in violation; the Act requires FIR to be filed immediately on complaint if prima facie case exists — internal inquiry does not substitute for FIR
- Remedial coaching is an evidence-based intervention; merely providing it is not enough — its effectiveness must be measured (pre/post test scores); EduForge tracks remedial coaching attendance and cross-references it with subsequent CIE performance; this data is the NAAC evidence for Criterion 5.1.1 (student learning support effectiveness)
- UGC Equal Opportunity Cell (EOC) annual report must be submitted; non-submission for 2+ consecutive years can affect college's UGC recognition renewal; the EOC report requires disaggregated data (SC/ST/OBC separately, gender-wise, scholarship-wise) that EduForge generates automatically from enrollment and welfare records
- Stigma around remedial coaching must be actively managed; a "remedial coaching" programme that students feel identifies them as "inferior" will have poor attendance; renaming it "Bridge Programme" or "Academic Accelerator" and delivering it with respected faculty (not junior instructors) reduces stigma; the voluntary enrolment model (with strong encouragement but no mandatory labelling) is the right balance

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division I*
