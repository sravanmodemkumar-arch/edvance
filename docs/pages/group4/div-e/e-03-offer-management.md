# E-03 — Offer Letters & Acceptance

> **URL:** `/college/placement/offers/`
> **File:** `e-03-offer-management.md`
> **Priority:** P1
> **Roles:** Placement Officer (S3) · Training & Placement Coordinator (S4) · Student (S1)

---

## 1. Offer Letter Management

```
OFFER LETTER — Provisional Offer
(From company to student via placement cell)

OFFER DETAILS — Aditya Kumar (226J1A0101)
Company: Amazon Development Centre (India) Pvt. Ltd.
Role: Software Development Engineer I (SDE-1)
Team: Prime Video — Content Platform
Location: Hyderabad, Telangana
CTC: ₹18,50,000/yr

CTC BREAKUP:
  Fixed (base salary):    ₹12,00,000/yr (₹1,00,000/month)
  Sign-on bonus:           ₹1,50,000 (one-time, Year 1 only)
  Annual bonus (variable): ₹1,50,000 (target; performance-linked)
  RSUs (stock):            $20,000 (~₹16,60,000) over 4 years (vest: 5%/15%/40%/40%)
  Note: Headline CTC often includes full 4-year RSU annual amortisation + signing bonus
        Real Year-1 cash: ₹12L base + ₹1.5L signing + ₹1.5L bonus = ₹15L (not ₹18.5L)
        Placement cell clearly explains this to all students ✅

Joining date: 7 July 2027 (tentative — after JNTU final exams)
Bond: None
Background verification: Criminal record + education verification + employment (if any)
Condition: Must clear all subjects before joining; no active backlogs at joining

OFFER LETTER DOCUMENT:
  Type: Provisional (final = after BGV clearance)
  Issue date: 15 October 2026
  Validity: Student must accept/decline by 22 October 2026 (7-day window)
  Digital signature: Amazon HR (DocuSign)
  Student counter-sign: Via EduForge → Offer Acceptance Portal

STATUS: ACCEPTED ✅ by Aditya Kumar, 18 October 2026
```

---

## 2. Offer Register

```
OFFER REGISTER — 2026–27 Season
(All offers received — Placement Officer view)

Offer ID | Student          | Company        | Role               | CTC    | Status
──────────────────────────────────────────────────────────────────────────────────────────
OFF-0001 | Aditya K. (0101) | Amazon         | SDE-1              | 18.5L  | ✅ Accepted
OFF-0002 | Bhavana M. (0102)| TCS            | Systems Engineer   | 3.36L  | ✅ Accepted
OFF-0003 | Charan R. (0103) | Goldman Sachs  | Technology Analyst | 22.0L  | 🔄 Pending BGV
OFF-0004 | Deepa S. (0104)  | Infosys        | Systems Engineer   | 3.6L   | ✅ Accepted
OFF-0005 | Eshwar T. (0105) | Wipro          | Project Engineer   | 3.5L   | ❌ Declined (CTC)
OFF-0006 | Priya R. (0201)  | Deloitte       | Analyst            | 7.0L   | ✅ Accepted
OFF-0007 | Kiran S. (0312)  | TCS            | Systems Engineer   | 3.36L  | ✅ Accepted
OFF-0008 | Kiran S. (0312)  | HCL            | Graduate Engineer  | 3.5L   | ❌ Declined (prefer TCS)
...

SUMMARY:
  Total offers made: 312 (some students have multiple offers)
  Offers accepted: 241
  Offers declined: 48
  Pending (BGV/joining confirmation): 23
  Unique students with at least 1 accepted offer: 224

MULTIPLE OFFERS:
  Students with 2 accepted offers: 31 ← must release one before joining
  Students with 3+ offers: 7 ← placement cell follow-up required
```

---

## 3. Background Verification (BGV) Tracking

```
BGV TRACKING — for students with accepted offers

BGV initiated by: Company (typically via AuthBridge/CIBIL/Veriff/IDFY — third-party)
College role: Provide degree/mark verification response (Education BGV)

EDUCATION BGV PROCESS:
  Company's BGV agency sends verification request to college
  Route: placement@gceh.ac.in → Placement Officer → Registrar
  Information verified: Enrollment dates, degree (tentative for current students), marks
  Response timeline: 3 working days (GCEH commitment)
  Response method: Official letter on college letterhead + Registrar signature
                   OR EduForge verification portal (direct digital verification)

PENDING BGV RESPONSES:
  Goldman Sachs (for Charan R.): Education BGV pending — requested 20 Mar 2027
    Placed student still in final semester → provisional verification sent
    Final degree verification: After JNTU degree — July 2027
  Microsoft (for Vikram T.): Responded ✅ 22 Mar 2027
  Amazon (for Aditya K.): Completed ✅ December 2026

BGV FAILURE:
  If a student's academic credentials are found to be falsified:
    Offer revoked by company
    College notified
    College action: Disciplinary proceedings (fraudulent representation)
    JNTU notified (academic misconduct)

MARKSHEET VERIFICATION API:
  EduForge provides: Digitally signed mark verification endpoint
  Company BGV agency authenticates: GET /api/v1/verify/student/{roll}/{semester}/
  Response: Signed JSON (enrollment confirmed, marks, status)
  DPDPA: Student consented at offer acceptance stage for BGV data sharing ✅
```

---

## 4. Joining & Pre-Joining Tracking

```
PRE-JOINING CHECKLIST (Placement Cell → Students)

For students placed, going to join July 2027:
  ✅ Accept offer in EduForge (digital counter-signature)
  ✅ Update personal/bank details with company HR portal
  ✅ Complete company's pre-joining formalities (IT asset declaration, medical)
  ⬜ Clear all JNTU backlogs before joining (if any)
  ⬜ Obtain provisional degree certificate (JNTU issues before convocation)
  ⬜ Original documents for joining (marksheets, ID, Aadhaar, PAN, bank)

BACKLOG STUDENTS WITH OFFERS:
  Students with conditional offers (no active backlog at joining):
    Currently with offers but active backlogs: 12 students
    JNTU supplementary exam: April/May 2027 → results June 2027
    Placement cell: Following up on each student's backlog clearance
    Risk: If backlog not cleared → offer may be revoked by company

COMPANY JOINING CALENDAR:
  July 2027: Amazon, Goldman Sachs, Deloitte, Persistent
  August 2027: Infosys (batch onboarding — large company; monthly cycles)
  September 2027: TCS, Wipro, HCL (Q2 batch)
  Note: JNTU final exams typically May–June 2027; joining July/Aug is standard
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/placement/offers/` | All offers |
| 2 | `POST` | `/api/v1/college/{id}/placement/offers/` | Record new offer |
| 3 | `POST` | `/api/v1/college/{id}/placement/offers/{id}/accept/` | Student accepts offer |
| 4 | `POST` | `/api/v1/college/{id}/placement/offers/{id}/decline/` | Student declines offer |
| 5 | `GET` | `/api/v1/college/{id}/placement/bgv/pending/` | Pending BGV requests |
| 6 | `GET` | `/api/v1/verify/student/{roll}/{semester}/` | Digital education verification |

---

## 6. Business Rules

- CTC transparency obligation: Placement cell must present CTC accurately to students; presenting RSU-inflated or signing-bonus-inflated CTC as "annual salary" is misleading; SEBI has issued guidance on fair disclosure for listed companies' compensation; the placement cell, while not a SEBI-regulated entity, has a duty of care to students — a student who joins based on inflated CTC expectation and finds the reality different may blame the placement cell; clear CTC breakup explanation is both ethical and protective
- Conditional offer + backlog: Companies that make conditional offers requiring "no active backlogs at joining" are exercising a standard contractual right; the college cannot guarantee these students' employment — if a student has backlogs and the company's condition is not met, the offer lapses; the placement cell should proactively track these students and urge supplementary exam registration
- Education background verification (BGV) is a legal process; the college must respond accurately to BGV requests; providing a false verification (e.g., confirming degree when student has not graduated) is an act of fraud that can be criminally prosecuted; provisional verification for current students must clearly state "student is in final year; degree not yet awarded"
- Offer letter counter-signature by student creates a legal agreement; EduForge's digital acceptance with timestamp and IP log constitutes valid acceptance; for dispute purposes, the digital acceptance record is sufficient evidence of contract formation
- Students who accept offers and then do not join without prior communication cause reputational harm to the college; while the student has no legal obligation to join (employment offers are revocable), the college's future batches are affected; EduForge tracks "offer-to-joining" conversion per student and flags habitual offer-decline patterns for counselling by the placement coordinator

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division E*
