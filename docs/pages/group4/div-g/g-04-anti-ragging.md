# G-04 — Anti-Ragging Cell & UGC Compliance

> **URL:** `/college/compliance/anti-ragging/`
> **File:** `g-04-anti-ragging.md`
> **Priority:** P1
> **Roles:** Anti-Ragging Committee (S5) · Anti-Ragging Squad (S3) · Principal/Director (S6) · Warden (S3)

---

## 1. Anti-Ragging Framework

```
ANTI-RAGGING FRAMEWORK — GCEH
(UGC Regulations on Curbing the Menace of Ragging 2009)

MANDATORY REQUIREMENTS:
  ✅ Anti-Ragging Committee (ARC): Constituted ✅
  ✅ Anti-Ragging Squad (ARS): Constituted ✅
  ✅ Undertaking from every student at admission: Signed (digital + physical)
  ✅ Undertaking from every student at hostel check-in: Signed separately
  ✅ Undertaking from parents at admission: Signed
  ✅ UGC helpline number (1800-180-5522) displayed: ✅ (entry gate, classrooms, hostel)
  ✅ AICTE Anti-Ragging portal: College registered ✅
  ✅ Mentoring programme for first-year students: Active ✅

ANTI-RAGGING COMMITTEE:
  Chairperson: Principal (mandatory — UGC Regulation 7.1)
  Members:
    ✅ Faculty (4): Senior professors across departments
    ✅ Administrative staff (1): Registrar
    ✅ Non-teaching staff (1): Hostel warden
    ✅ Students (2): One senior + one junior year representative
    ✅ Parents representative (1): From Parent-Teacher Association
    ✅ Local police (1): SHO, Madhapur PS (or representative)
    ✅ NGO representative (1): Pratham Foundation (children's rights)
    ✅ Media (1): Local journalist (Deccan Chronicle)

ANTI-RAGGING SQUAD (Ground-level enforcement):
  Composition: 3 faculty members per shift (rotating)
  Duty: Physical monitoring of hostels, canteen, common areas
        Particularly first 3 months of academic year (highest risk period)
  Schedule: Morning (7–9 AM), Evening (5–7 PM), Night (9–11 PM)
  Reporting: Daily duty log to ARC Chairperson
```

---

## 2. Ragging Complaint Management

```
COMPLAINT CHANNELS:
  1. UGC Anti-Ragging Helpline: 1800-180-5522 (national — routed to college)
  2. AICTE portal (aicte-india.org/antiragging)
  3. EduForge app: Anonymous report → Hostel → Report Ragging
  4. Written complaint to Principal
  5. Verbal complaint to any faculty member (faculty duty to forward to ARC)

COMPLAINT HANDLING PROCESS:

Step 1: Receipt
  All complaints (anonymous or named): Registered by ARC Member-Secretary within 2 hours
  Priority: P0 (immediate) — physical injury, threat, sexual harassment component
            P1 (same day) — verbal/psychological ragging, coercion
            P2 (next working day) — borderline conduct, single incident reports

Step 2: Preliminary inquiry (within 24 hours)
  ARC Chairperson + 2 ARC members
  Interview complainant (if non-anonymous)
  CCTV review (if location identified)
  Interim measure: Accused student can be suspended from hostel pending inquiry
                   (accused remains enrolled and attends class — academic rights not suspended)

Step 3: Full inquiry (within 7 days)
  FIR mandatory if prima facie case of ragging (IPC Section 294, 323, 506, etc.)
  UGC Reg 9.1: College must file FIR — cannot take only internal action
  All parties heard (natural justice)
  Witnesses recorded

Step 4: Punishment (UGC Regulation 9.4):
  Cancellation of admission
  Suspension from college
  Withholding results/degree
  Expulsion from hostel
  Debarment from future exams
  Fine up to ₹25,000
  (Combination of above depending on gravity)

Step 5: Reporting
  Report to UGC Anti-Ragging Monitoring Cell (within 72 hours of FIR)
  Report on AICTE anti-ragging portal (within 24 hours of committee action)

COMPLAINT REGISTER 2026–27:
  Complaints received: 3
    INC-ARC-001: Feb 2027 — Anonymous (hostel) — under inquiry ⬜
    INC-ARC-002: Nov 2026 — Named (senior year verbal bullying) — Closed ✅ (warning)
    INC-ARC-003: Sep 2026 — AICTE portal routed — Investigated, no prima facie ✅
```

---

## 3. Preventive Measures

```
PREVENTIVE ANTI-RAGGING MEASURES

ORIENTATION PROGRAMME (July — first week):
  ✅ Anti-ragging session for all first-year students (2 hours)
     Content: What constitutes ragging, consequences, reporting channels
     Speaker: Principal + police officer (SHO or sub-inspector)
     Attendance: 100% mandatory
  ✅ Anti-ragging session for senior students (1 hour)
     Content: Peer influence, legal consequences for accused, duty to report
  ✅ Parent session: Anti-ragging awareness for parents of first-year students
     Platform: Orientation day; also shared via EduForge parent portal

SENIOR-JUNIOR MIXING:
  ✅ Hostel floor allocation: First-years not isolated on separate floors
     Rationale: Isolation increases ragging risk; mixing with mature seniors reduces it
     Countermeasure: ARS monitoring on floors with first-year rooms

MENTORING PROGRAMME:
  ✅ Each first-year student assigned a senior student mentor (3rd/4th year)
     Ratio: 1:1 (same branch)
     Purpose: Academic guidance + safe reporting channel for ragging concerns
     Monthly meeting: Logged in EduForge

CCTV COVERAGE:
  ✅ All corridors, common rooms, canteen, hostel entry/exit
  ✅ Monitored by security desk (24×7)
  ✅ 30-day retention
  ✅ NOT in rooms/bathrooms (DPDPA + POCSO)

ANTI-RAGGING PLEDGES:
  Displayed on walls, website, student ID cards
  EduForge: Anti-ragging helpline always visible on student app home screen
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/compliance/anti-ragging/complaint/` | Submit ragging complaint |
| 2 | `GET` | `/api/v1/college/{id}/compliance/anti-ragging/complaints/` | All complaints (ARC view) |
| 3 | `GET` | `/api/v1/college/{id}/compliance/anti-ragging/squad-log/` | Daily squad duty log |
| 4 | `GET` | `/api/v1/college/{id}/compliance/anti-ragging/compliance-status/` | UGC compliance checklist |

---

## 5. Business Rules

- FIR (First Information Report) is mandatory when prima facie ragging is established — an institution cannot substitute its own internal punishment for a criminal complaint; many colleges that want to "protect their reputation" handle ragging internally without filing FIR; this is itself a criminal offence (misprision) under UGC Regulation 9.1 and has resulted in NCTE/UGC action against institutions; EduForge's complaint module flags when an FIR should be filed and creates an audit trail if it is not
- Confidentiality of the complainant is paramount in ragging cases; revealing the complainant's identity to the accused is a UGC violation and can expose the complainant to retaliation; in anonymous complaints, the anonymity must be maintained even if it makes the inquiry more difficult; CCTV footage, other witnesses, and physical evidence are the primary alternatives
- The Police representative on the Anti-Ragging Committee is not a formality; active police engagement means that when an FIR is filed, there is already an established relationship; many campus incidents (not just ragging) benefit from this relationship — a college where the SHO is a regular ARC member has faster response times
- Anti-ragging undertakings obtained at admission and hostel check-in serve as legal notice to students that ragging is an offence with specific consequences; a student who claims "I didn't know" cannot succeed with this defence; EduForge timestamps each student's digital signature on the undertaking, creating an immutable record
- The first 3 months of each academic year are statistically the highest-risk period for ragging; heightened ARS monitoring during July–September is not merely good practice — it is documented in UGC circulars as the period requiring special attention; colleges that relax monitoring after the first week of orientation and experience a ragging incident in September face the additional accusation of having abandoned preventive duty

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division G*
