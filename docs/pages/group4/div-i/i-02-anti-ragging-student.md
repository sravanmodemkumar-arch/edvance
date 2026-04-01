# I-02 — Anti-Ragging — Student Facing

> **URL:** `/college/welfare/anti-ragging/`
> **File:** `i-02-anti-ragging-student.md`
> **Priority:** P1
> **Roles:** Student (S1) · Welfare Officer (S4) · Anti-Ragging Committee (S5)

---

## 1. Student-Facing Interface

```
ANTI-RAGGING — STUDENT VIEW
(EduForge app → Welfare → Anti-Ragging)

HOME SCREEN DISPLAY (always visible):
  ┌─────────────────────────────────────────────────────┐
  │  REPORT RAGGING SAFELY                              │
  │  Anonymous reporting available                      │
  │  National Helpline: 1800-180-5522 (24×7, FREE)     │
  │  GCEH ARC: 040-2341-XXXX (Chief Warden/Principal)  │
  │  EduForge Anonymous Report: ↓                       │
  │  [REPORT NOW]    [Call Helpline]                    │
  └─────────────────────────────────────────────────────┘

ANONYMOUS REPORT FORM:
  What happened (text + optional audio note): _______
  Where it happened: [Hostel ▼] [Academic Block ▼] [Other ▼]
  When it happened: [Today ▼] [This week ▼] [Earlier ▼]
  Were there witnesses: [Yes / No]
  Are you willing to be contacted for more details: [Yes / No — if Yes, provide contact]

NOTE: If you choose "Yes" for contact, your identity will ONLY be shared with
      the Anti-Ragging Committee — never with the accused, other students, or staff.

SUBMIT → Encrypted to ARC via college security channel (not visible to general admins)
```

---

## 2. First-Year Orientation Content

```
ANTI-RAGGING ORIENTATION — First Year Students
(July 2026 — Mandatory attendance)

MODULE 1: WHAT IS RAGGING? (30 minutes)
  Legal definition (UGC Regulation 3):
    "Any conduct that has the effect of teasing, treating, or handling with rudeness
     a fresher or any other student; indulging in rowdy or undisciplined activities
     that cause annoyance, hardship or psychological harm or raising apprehension
     as to the security in the life of a fresher"

  Forms of ragging (examples given):
    Physical: Hitting, pushing, forced physical tasks
    Verbal: Insulting, abusing, humiliating references to caste/religion/region
    Sexual: Unwanted touching, sexual jokes, forced nudity
    Psychological: Intimidation, threats, forced performance
    Digital: Harassing via WhatsApp, social media, sharing embarrassing content
    "Forced interaction" under guise of seniority: Ragging even without physical contact

  Famous cases discussed: Aman Kachroo case (2009 Himachal — sparked UGC regulation)

MODULE 2: CONSEQUENCES (20 minutes)
  For the perpetrator:
    Cancellation of admission
    Suspension
    Debarment from exams
    FIR and criminal prosecution (IPC 294, 323, 506, 354 depending on nature)
    Permanent record mark affecting future employment BGV

  For the institution:
    UGC/AICTE action against the college
    Potential EoA cancellation
    Criminal prosecution of Principal if willful negligence

MODULE 3: HOW TO REPORT (10 minutes)
  Multiple channels shown (EduForge app demonstration)
  Anonymity guaranteed
  Outcome: 100% of complaints investigated; immediate interim protection

ATTENDANCE: 476/480 first-year students ✅ (96.7% attendance — 4 late joins)
```

---

## 3. Mentoring Programme

```
PEER MENTORING — Anti-Ragging + Academic Support

MENTORS ASSIGNED:
  Each first-year student: 1 senior mentor (3rd or 4th year, same branch)
  Mentor selection: Volunteers + faculty recommendation
  Trained mentors: 2-hour orientation (ARC Chairperson + counsellor)
  Total mentor pairs: 480 (all first-year × 1 mentor each)

MENTOR RESPONSIBILITIES:
  Academic: Subject guidance, JNTU exam preparation tips, college navigation
  Welfare: Informal check-in (monthly); "Is anyone bothering you?" question normalised
  Ragging gateway: First point of contact if student uncomfortable reporting directly
  Escalation: Mentor reports to Welfare Officer if concerning information shared

MENTOR-MENTEE MEETINGS:
  Frequency: Once/month (first semester); once/semester (second year onwards)
  Format: Informal (canteen, common room) — no structured agenda required
  EduForge: Mentor logs "meeting completed" (no content logging — privacy)
  Monitoring: Welfare Officer reviews completion rate monthly

MEETING COMPLETION (2026–27):
  August: 94% pairs met ✅
  September: 91% pairs met ✅ (some mentors on internship/exam — excused)
  October: 88% ✅
  January 2027: Pairs refreshed for Semester II (some mentors graduated early)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/welfare/ragging/report/` | Anonymous/named ragging report |
| 2 | `GET` | `/api/v1/college/{id}/welfare/ragging/my-complaint/` | Student checks own complaint status |
| 3 | `GET` | `/api/v1/college/{id}/welfare/mentoring/pairs/` | Mentor-mentee assignments |
| 4 | `POST` | `/api/v1/college/{id}/welfare/mentoring/log/` | Log mentor-mentee meeting |

---

## 5. Business Rules

- Anonymous reporting channels must genuinely protect anonymity; a "anonymous" form that logs the submitter's student ID in the backend is not anonymous — it is a security theatre that will be discovered and deter reporting; EduForge's anonymous report uses a separate submission path that strips identifying metadata before storing; the only traceable element is if the student voluntarily provides contact information
- The anti-ragging undertaking signed at admission is not consent to be ragged; it is a declaration that the student will not rag others and will report if ragged; the distinction matters because some first-year students believe signing the undertaking means they accepted the possibility of ragging — this misconception must be explicitly corrected in orientation
- Senior student mentors must be carefully screened; a mentor who was previously warned for ragging-adjacent behaviour is not an appropriate anti-ragging mentor; the ARC and Welfare Officer should cross-check mentor candidates against the incident register; a mentor who rags their own mentee — having access to them — is a catastrophic failure of the programme
- The orientation session must be in the regional language (Telugu for Telangana colleges) as well as English/Hindi; first-year students from rural backgrounds may not understand nuanced legal definitions in English; Telugu and Hindi explanations of what constitutes ragging, with concrete examples, are more effective; EduForge's orientation module supports multilingual content
- The anti-ragging information must remain visible throughout the academic year — not just in orientation week; EduForge places the ragging helpline number on the home screen permanently (not removable or collapsible); the physical notice board displays must be checked monthly by the ARS and their condition logged

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division I*
