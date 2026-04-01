# G-05 — POSH Act — ICC & Complaints

> **URL:** `/college/compliance/posh/`
> **File:** `g-05-posh-icc.md`
> **Priority:** P1
> **Roles:** ICC Chairperson (S5) · ICC Members (S4) · Principal/Director (S6) · HR Officer (S3)

---

## 1. POSH Compliance Framework

```
POSH ACT 2013 — GCEH COMPLIANCE
(Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act 2013)

APPLICABILITY:
  "Workplace" under POSH: Educational institution is a workplace
  "Aggrieved woman": Student, faculty, non-teaching staff, contractual staff, visitors
  Employer liability: College (and its Governing Body) is liable for failure to comply
  Mandatory requirement: ICC constitution for workplaces with ≥10 employees

ICC (INTERNAL COMPLAINTS COMMITTEE) CONSTITUTION:
  Mandatory per Section 4 of POSH Act 2013

  Presiding Officer: Ms. Kavitha P. (Senior Lady Faculty — mandatory female Presiding Officer)
  Internal Members (3 minimum — majority women):
    Ms. Deepa R. (Faculty, ECE) — Women's Cell Coordinator
    Mr. Pradeep N. (Faculty, CSE) — gender sensitisation background
    Ms. Sunita K. (Accounts Officer, non-teaching staff)
  External Member (mandatory — NGO/legal/social worker background):
    Ms. Aruna V. (Advocate + Women's Rights NGO, Hyderabad)
    [Mandatory: Cannot be college employee; must have POSH/social work background]

ICC TERM: 3 years (members cannot be re-elected for same role consecutively)
ICC Formed: January 2025 (renewed from previous committee)

DISPLAY REQUIREMENTS (Section 19):
  ✅ ICC contact details on notice board (all locations)
  ✅ Name + email + phone of ICC Presiding Officer
  ✅ POSH Act summary poster (Hindi + Telugu + English — trilingual)
  ✅ On website: college/compliance/posh/icc-contact/
  Non-display is an offence under Section 26 (fine up to ₹50,000)
```

---

## 2. Complaint Management

```
COMPLAINT PROCESS (Section 9)

FILING A COMPLAINT:
  Who can file: Any aggrieved woman (student, faculty, staff, contractor, visitor)
  When: Within 3 months of incident (extendable to 6 months by ICC for good cause)
  How: Written complaint to ICC Presiding Officer
       EduForge: Confidential channel — Compliance → POSH → Report
  Note: Third party can file if aggrieved woman is incapacitated

COMPLAINT REGISTER (Confidential — ICC + Principal only):
  2026–27:
    Case ICC-2701: Filed September 2026 (student vs male faculty — inappropriate remarks)
      Status: Inquiry completed ✅; finding: harassment established (minor)
      Action: Written warning to faculty; mandatory sensitisation workshop
      Recommendation to Principal: Implemented ✅
      Record retained: 3 years (POSH Act requirement)

    Case ICC-2702: Filed January 2027 (staff vs staff — WhatsApp messages)
      Status: Under inquiry ⬜ (initiated February 2027)
      Interim relief granted: Complainant's workstation relocated (no face-to-face contact)
      Expected completion: April 2027 (within 90-day legal limit)

  2025–26: 1 case (resolved — no harassment finding; malicious complaint alert)
  2024–25: 0 cases

INQUIRY PROCESS (Sections 11–12):
  Step 1: ICC receives complaint → acknowledges within 7 days
  Step 2: Copy to accused (respondent) → respond within 10 days
  Step 3: Conciliation offered (if both parties agree — no penalty for complainant if conciliation fails)
  Step 4: Full inquiry: Both parties heard, witnesses examined, documents
  Step 5: Report to employer (Principal) within 90 days — recommended action
  Step 6: Employer implements within 60 days
  Step 7: Appeal: District Officer within 90 days of employer action

CONFIDENTIALITY (Section 16):
  Names of complainant, accused, witnesses: STRICTLY confidential
  Not to be disclosed in media, social media, or any public domain
  Violation: Fine up to ₹5,000 per POSH Act
  EduForge: POSH complaint records are isolated from regular compliance reports
             Only ICC members + Principal (with need-to-know) have access
```

---

## 3. Preventive Measures & Annual Report

```
PREVENTION PROGRAMME

GENDER SENSITISATION (Annual):
  Session 1 (July): All first-year students — what constitutes sexual harassment,
                    consent, reporting channels (2-hour session)
  Session 2 (August): All faculty and staff — POSH Act obligations, ICC process,
                       workplace conduct standards (1-hour mandatory)
  Session 3 (Women's Day — March 8): Annual awareness programme
  Attendance: 96% (faculty), 88% (staff), 100% (first-year students — orientation)

WOMEN'S CELL:
  Coordinator: Ms. Deepa R. (Faculty, ECE)
  Activities: Monthly meetings, grievance counselling (informal pre-complaint support),
              annual women's fest, legal awareness sessions
  Student membership: 45 students (self-nominated)
  Helpline: Internal extension + EduForge confidential chat

ANNUAL REPORT TO DISTRICT OFFICER (Section 21):
  Every employer must submit annual POSH compliance report
  To: District Officer, POSH, Rangareddy District (GCEH location)
  Contains: Number of complaints filed, disposed, pending; action taken
  Due: By 31 January (for prior calendar year)
  2026 annual report: ✅ Filed 28 January 2027
  Contents: 2 complaints received (2026), 1 disposed, 1 ongoing

FAILURE TO FILE ANNUAL REPORT:
  Section 21 non-compliance → fine ₹50,000 (first offence) → doubled for repeat
  EduForge reminder: Set at 1 December for January filing
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/compliance/posh/complaint/` | File POSH complaint (confidential) |
| 2 | `GET` | `/api/v1/college/{id}/compliance/posh/complaints/` | Complaints (ICC view only) |
| 3 | `GET` | `/api/v1/college/{id}/compliance/posh/compliance-status/` | POSH compliance checklist |
| 4 | `GET` | `/api/v1/college/{id}/compliance/posh/annual-report/` | Annual report data |

---

## 5. Business Rules

- The External Member of the ICC (from NGO/legal background) is mandatory under Section 4(2)(d) of the POSH Act; constituting an ICC without an external member makes the ICC invalid and any inquiry conducted by it can be challenged as void; the external member also brings independence — an ICC composed entirely of college employees has an inherent conflict of interest in cases involving senior faculty
- ICC members must be trained; many institutions constitute an ICC but provide no POSH training to members; an ICC member who is unfamiliar with inquiry procedures, natural justice requirements, or evidence standards conducts flawed inquiries; GCEH sends all ICC members for a 1-day POSH training (SHe-Box facilitated training available from MoWCD) annually
- The 90-day inquiry completion timeline is a hard legal requirement; delays beyond 90 days can be challenged in the High Court; EduForge sets escalating alerts at 60 and 80 days to ensure inquiries are completed on time; extensions require written documentation of reasons and the complainant's awareness
- Interim relief must be considered at the first meeting after complaint receipt; interim relief can include transfer of respondent, leave of absence, or workplace separation; denying interim relief when the complainant and respondent work in close proximity (or are in the same class) can constitute institutional negligence if the harassment continues during the inquiry period
- POSH applies to all women in the "extended workplace" including students on campus; the 2013 Act covers educational institutions explicitly; colleges that argue POSH does not apply to student-faculty situations are legally wrong and have been held liable by courts; GCEH's POSH policy explicitly covers student-faculty, faculty-faculty, and staff-staff interactions

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division G*
