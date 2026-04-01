# I-06 — PwD / CWSN Student Support

> **URL:** `/college/welfare/pwd/`
> **File:** `i-06-cwsn.md`
> **Priority:** P1
> **Roles:** PwD Coordinator (S4) · Welfare Officer (S4) · Principal/Director (S6)

---

## 1. PwD Student Register

```
PwD STUDENTS — GCEH 2026–27
(Persons with Disabilities — RPwD Act 2016)

ENROLLED PwD STUDENTS: 3
  Roll: 226J1A0315 — Arjun V. (B.Tech CSE, Year 1)
    Disability: Locomotor (right arm — partial paralysis post-accident)
    Certificate: UDID card 123456789 (Andhra Pradesh; 42% disability)
    Accommodation:
      Hostel: Ground floor room (Block B-G01) ✅
      Scribal assistance: For JNTU exams (applied via JNTU PwD cell)
      Seating: Front-row seat in all lectures ✅
      Lab: Modified workstation (trackball mouse, voice input) — procured ✅
      Extra time: +30 min per 90-min exam (JNTU PwD norm)

  Roll: 225J1A0822 — Priya S. (B.Tech ECE, Year 2)
    Disability: Visual impairment (partial — 40% in right eye)
    Certificate: UDID card 987654321 (Telangana; 40% disability)
    Accommodation:
      Large-print study material: Faculty provide lecture slides in 16pt font ✅
      Seating: Front row + sufficient lighting ✅
      JNTU exam: Enlarged question paper + extra 20 min
      Lab partner: Assigned a consistent lab partner for safety ✅

  Roll: 224J1A0412 — Ravi K. (B.Tech CSE, Year 3)
    Disability: Hearing impairment (bilateral)
    Certificate: UDID card 456789123 (Telangana; 60% disability)
    Accommodation:
      Front-row seating ✅
      Written instructions from faculty (not just verbal) ✅
      Sign language interpreter: Not available — college is exploring (funding constraint)
      Subtitled video content: All lab demo videos have auto-subtitles ✅
      JNTU exam: Written question reading (no verbal assistance needed — already written)

PwD ADMISSION PREFERENCE:
  EAPCET: 3% horizontal reservation for PwD ← all 3 students admitted via PwD quota
  Management quota: PwD applications given equal consideration + accommodation guarantee
```

---

## 2. Reasonable Accommodation Process

```
REASONABLE ACCOMMODATION (RPwD Act 2016 — Section 3)

DEFINITION: "Necessary and appropriate modification and adjustments... to ensure
             persons with disabilities enjoy or exercise rights and freedoms"

ACCOMMODATION REQUEST PROCESS:
  Student submits: UDID card + specific accommodation need + medical professional letter
  PwD Coordinator reviews: Within 7 days
  Accommodation plan: Documented (signed by student + PwD Coordinator)
  Faculty notification: HOD informs all relevant faculty (disability type only — not full medical)
  JNTU notification: College sends PwD accommodation request to JNTU before each exam

GCEH ACCOMMODATION PORTFOLIO (all currently provided):
  Physical access:   ✅ Ramps, accessible toilets, ground-floor hostel rooms
  Seating:           ✅ Front-row reserved (no "first-come" policy overriding PwD students)
  Extended exam time:✅ (JNTU approves — college facilitates)
  Scribe arrangement:✅ (JNTU approved — GCEH identifies suitable scribe)
  Modified lab setup:✅ (procurement from lab budget)
  Large print:       ✅ Faculty instructed
  Digital accessibility:✅ EduForge WCAG 2.1 AA compliant ← key for blind/low-vision
  Lift access:       ✅ Lifts available (for mobility-impaired students)

NOT YET AVAILABLE:
  Sign language interpreter (full-time): Budget constraint; exploring government support
    GCEH application to RPwD Cell (state): For funding under Accessible India Campaign
  Braille library: Limited materials available; DAISY books for some subjects (IGNOU)
  Note: "Reasonable accommodation" is limited by resources; but effort and good faith required
```

---

## 3. JNTU PwD Exam Support

```
JNTU PwD EXAM ACCOMMODATIONS (2026–27)

JNTU PROCESS:
  College must submit PwD accommodation request to JNTU Controller of Examinations
  Required: UDID certificate + disability certificate + medical recommendation
  Deadline: 30 days before examination
  Approved accommodations (JNTU norms):
    >40% locomotor: Scribe + extra 20 min/hour
    >40% visual: Enlarged paper + extra 20 min/hour
    >75% any disability: Writer + extra time
    40–75% other: Extra 20 min/hour without scribe (case-by-case)

GCEH SUBMISSIONS 2026–27 (Semester II):
  Arjun V.: Scribal assistance + extra time ← submitted to JNTU ✅ (Mar 2027 exams)
  Priya S.: Enlarged question paper + extra time ✅
  Ravi K.: No scribe (hearing impairment — written exam unaffected)
           Extra time: Not required (performance unaffected by time)

SCRIBE SELECTION (Arjun V.):
  Scribe must be: From lower-qualification stream (JNTU says "graduate level scribe for PG;
                  12th-pass scribe for UG students")
  GCEH: Identified 2 scribes from final-year B.Sc. college nearby
  Scribe training: 1-hour orientation with Arjun before exam (JNTU requirement)
  Scribe declaration: Both sign JNTU declaration form (scribe will write what student dictates)

EXAM ROOM ARRANGEMENT:
  PwD students: Separate exam room (one-student or small group)
  Invigilator: Familiar with PwD protocols (Welfare Officer + trained invigilator)
  No assistance beyond approved accommodation (scribe cannot suggest answers)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/welfare/pwd/students/` | PwD student register |
| 2 | `POST` | `/api/v1/college/{id}/welfare/pwd/accommodation/` | New accommodation request |
| 3 | `GET` | `/api/v1/college/{id}/welfare/pwd/accommodation/{student_id}/` | Student's accommodation plan |
| 4 | `POST` | `/api/v1/college/{id}/welfare/pwd/jntu-request/` | Generate JNTU PwD request document |

---

## 5. Business Rules

- UDID (Unique Disability Identity Card) is the mandatory document for PwD benefits under RPwD Act 2016; older disability certificates (from civil surgeon etc.) are not accepted by JNTU for exam accommodations; the college must guide students to obtain UDID cards (through online portal — swavlambancard.gov.in) and track their validity; EduForge alerts when a student's UDID card is expiring (they must be renewed)
- Refusing reasonable accommodation for a PwD student is a violation of RPwD Act 2016 Section 3 and can attract action under the Act (Section 89 — punishment for violations); the test is "reasonable" — a college with limited resources that makes genuine effort but cannot provide all accommodations is in a better position than one that makes no effort; documentation of the effort and good faith is critical
- Faculty must be briefed on each PwD student's accommodation needs without disclosing the specific medical diagnosis; the correct disclosure is "Arjun needs front-row seating and enlarged digital slides" — not "Arjun has right-arm partial paralysis due to accident"; minimal necessary disclosure protects both the student's dignity and the institution's DPDPA compliance
- JNTU PwD accommodation requests must be submitted well before the exam deadline; late submissions are typically rejected (JNTU's view: accommodation is a planning requirement, not a last-minute request); EduForge creates a recurring reminder 45 days before each exam period for PwD accommodation submissions
- Sign language interpretation is a reasonable accommodation for students with hearing impairment above the legally significant threshold; a college that cannot fund a full-time interpreter should explore government schemes (Accessible India Campaign funding, Disability Commissioner support), IGNOU material, and interim alternatives (written + visual instruction supplemented by video); avoiding the issue entirely and expecting hearing-impaired students to "manage" is not reasonable accommodation

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division I*
