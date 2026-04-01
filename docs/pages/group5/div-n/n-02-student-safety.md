# N-02 — Student Safety & POCSO

> **URL:** `/coaching/compliance/safety/`
> **File:** `n-02-student-safety.md`
> **Priority:** P1
> **Roles:** Director (K7) · Student Counsellor (K3) · Branch Manager (K6)

---

## 1. Student Safety Framework

```
STUDENT SAFETY FRAMEWORK — Toppers Coaching Centre

  SAFETY PILLARS:
    1. Physical safety:      Secure premises, CCTV, visitor register, fire safety
    2. Emotional safety:     Anti-bullying, anti-harassment, counselling access
    3. Gender safety:        Women's safety initiative, POCSO awareness, female staff
    4. Digital safety:       Safe LMS use, no student data exposure, online conduct rules
    5. Financial safety:     Transparent fees, no coercive collection, refund policy

  RESPONSIBLE PERSONS:
    POCSO Designated Contact:  Ms. Anitha R. (Student Counsellor)
    Women's Safety Officer:    Ms. Anitha R. (Student Counsellor)
    Emergency Contact (24/7):  Branch Manager mobile: +91-98765-XXXXX
    Fire Warden (1st floor):   Mr. Rajan K. (trained — Jan 2026 drill)
    Fire Warden (2nd/3rd):     Mr. Suman G. + Ms. Saroja T.

  EMERGENCY NUMBERS (posted in all rooms, hostel corridors):
    Police:          100
    Fire:            101
    Ambulance:       108
    Women's helpline: 181
    TCC Emergency:   +91-98765-XXXXX (Branch Manager)
    Hostel Warden (M): +91-XXXXX-XXXXX | (F): +91-XXXXX-XXXXX
```

---

## 2. POCSO Compliance

```
POCSO — PROTECTION OF CHILDREN FROM SEXUAL OFFENCES ACT 2012

  APPLICABILITY TO TCC:
    TCC admits students as young as 16–17 in its Foundation Batch (Class 10+2)
    These are "children" under POCSO (persons under 18 years of age)
    TCC is therefore an "institution" covered under POCSO awareness requirements
    The Principal/Director is responsible for institution-level compliance

  DESIGNATED POCSO CONTACT:
    Name:       Ms. Anitha R. (Student Counsellor)
    Training:   POCSO awareness training (online — Dec 2025) ✅
    Contact:    counsellor@tcc.in | +91-XXXXX-XXXXX (confidential line)
    Backup:     Branch Manager (K6) if designated contact is unavailable

  AWARENESS SESSIONS (mandatory for all staff):
    Last conducted:  February 2026 (new batch orientation) ✅
    Next:            August 2026 (new AY intake)
    Content:         POCSO definitions, reporting obligations, support for child disclosures
    Attendance:      All teaching + non-teaching staff (44 attended, 44/44 = 100%) ✅

  REPORTING OBLIGATION (Section 19, POCSO Act):
    If ANY person (staff, student, parent) suspects or is aware of a sexual
    offence against a child, they MUST report to the local police (or SJPU)
    Failure to report is itself a criminal offence (Section 21 POCSO)
    TCC does NOT conduct its own investigation — police authority is paramount

  CURRENT STATUS: No POCSO-related complaints or incidents this AY ✅
```

---

## 3. Hostel Safety Protocols

```
HOSTEL SAFETY PROTOCOLS — TCC Hyderabad

  ACCESS CONTROL:
    Entry:  Biometric for residents | Sign-in register for authorised visitors
    Exit:   Curfew 9 PM (female hostel), 10 PM (male hostel)
    CCTV:   All corridors, entry/exit — NOT in rooms or bathrooms ✅
    Keys:   Master key held only by Warden + Branch Manager (physical safe)

  VISITOR POLICY (I-06 Hostel Visitor Register):
    Allowed:   Parents/guardians on the approved list (submitted at admission)
    Not allowed: Non-registered visitors without warden approval
    Visit hours: 9 AM – 7 PM (male visitors to female hostel: reception area only)

  FEMALE STUDENT SAFETY (additional):
    Female warden on duty 24/7 ✅
    Women's safety helpline number posted in all female bathrooms ✅
    Self-defence workshop: 2 sessions/year (last: Feb 2026) ✅
    Female-only counsellor option available ✅
    CCTV: Entry/exit of Block B only — no internal cameras ✅

  FIRE DRILL:
    Last conducted:   January 2026 (all students + staff participated) ✅
    Evacuation time:  7 minutes (target: < 10 minutes) ✅
    Next drill:       August 2026 (new AY)

  MEDICAL EMERGENCY:
    First aid kit:    Stocked and checked monthly ✅
    Nearest hospital: Apollo Hospitals, 1.2 km from TCC ✅
    Ambulance on call: 108 (national) | TCC has agreement with local clinic
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/compliance/safety/framework/` | Safety framework and contacts |
| 2 | `GET` | `/api/v1/coaching/{id}/compliance/safety/pocso/` | POCSO compliance status |
| 3 | `POST` | `/api/v1/coaching/{id}/compliance/safety/incident/` | Report a safety incident |
| 4 | `GET` | `/api/v1/coaching/{id}/compliance/safety/incidents/` | Incident log (restricted) |
| 5 | `GET` | `/api/v1/coaching/{id}/compliance/safety/drills/` | Fire drill and safety drill records |

---

## 5. Business Rules

- POCSO reporting is mandatory and unconditional; when TCC becomes aware of a possible sexual offence against a student below 18, the Designated Contact (Ms. Anitha R.) must file a report with the police/SJPU (Special Juvenile Police Unit) within 24 hours — the law does not allow TCC to first investigate, verify, or assess the credibility of the complaint; the legal standard for mandatory reporting is "reason to believe", not "conclusive proof"; TCC's internal investigation (if any) must happen parallel to the police process, never instead of it; the student making the disclosure must be treated with care and assured of support throughout
- A student who discloses a POCSO-relevant incident must be believed and supported regardless of who the alleged perpetrator is; if the allegation is against a faculty member, the faculty must be placed on administrative leave immediately pending the police investigation — NOT just counselled privately; TCC's natural instinct to protect a long-serving faculty from the accusation must be overridden by the legal obligation and the child's protection; a faculty on administrative leave continues to receive salary during the investigation; the Director makes this decision within 2 hours of receiving the complaint
- The CCTV coverage policy (corridors and common areas only, no cameras in rooms, bathrooms, or counselling rooms) balances safety monitoring with student privacy; cameras in bathrooms or bedrooms would be voyeurism, a criminal offence; the counselling room camera exclusion protects the confidentiality of student disclosures; a student who is afraid to speak to the counsellor because "they might be recording this" would not seek help; the camera-free zones are also a DPDPA 2023 compliance requirement (capturing intimate spaces is a prohibited data processing activity)
- Women's safety is not just a compliance checkbox — it is a fundamental commitment to female students' right to study safely; TCC has over 400 female students (hostel residents and day scholars); a single incident of harassment or assault on TCC premises, if mishandled, destroys the institution's reputation and prevents future female enrollment; the investment in female warden (full-time), self-defence workshops, and helpline access is a fraction of the cost of one well-publicised safety failure; the Director reviews women's safety metrics (complaints, helpline usage, workshop attendance) quarterly
- The hostel curfew policy (9 PM females, 10 PM males) exists for safety, not control; the rationale is that late-night movement in a hostel of young adults creates safety risks (external threats, internal conflicts); students who have medical emergencies or genuine late-return situations can call the warden directly for gate access; the curfew is enforced firmly but the warden exercises judgment for genuine exceptions; a student returning from a hospital visit at 10:30 PM is not treated the same as a student returning from a social event at 2 AM; the warden documents all exceptions with the reason and time

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division N*
