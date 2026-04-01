# D-06 — Discipline Register & Incident Management

> **URL:** `/college/hostel/discipline/`
> **File:** `d-06-discipline.md`
> **Priority:** P1
> **Roles:** Warden (S3) · Chief Warden (S4) · Principal/Director (S6) · Anti-Ragging Committee (S5)

---

## 1. Hostel Code of Conduct

```
HOSTEL CODE OF CONDUCT — GCEH
(Displayed at hostel notice board; acknowledged at check-in)

PROHIBITED CONDUCT:
  Category A (Major — immediate hostel expulsion):
    1. Ragging in any form (UGC Anti-Ragging Regulations — zero tolerance)
    2. Possession/consumption of alcohol or narcotics
    3. Possession of weapons (knives, clubs, any weapon)
    4. Physical assault on another student or staff
    5. Theft of college/hostel property or fellow student's belongings
    6. CCTV tampering or security compromise
    7. Serious sexual harassment (POSH Act / IPC sections)

  Category B (Moderate — hostel probation / outpass suspension):
    1. Smoking inside hostel premises (can smoke only in designated outside area)
    2. Cooking in rooms (fire hazard — NBC 2016 fire safety)
    3. Late return >3 instances (after 2 warnings)
    4. Noise disturbance after 11 PM (3+ instances)
    5. Damaging hostel property intentionally
    6. Bringing visitors inside hostel block without permission
    7. Using hostel room for commercial activity

  Category C (Minor — verbal/written warning):
    1. Missed night roll call without prior outpass
    1. Untidy room during inspection
    2. Mess rule violation (taking food outside mess area habitually)
    3. Mobile phone usage in mess (distraction; 3+ instances)
    4. Late return (1st, 2nd instance)

PUNISHMENTS:
  Written warning → Outpass suspended (30 days) → Hostel probation (1 semester) →
  Hostel expulsion → College disciplinary committee (academic consequences)
  Ragging: Immediate suspension pending inquiry → Expulsion + FIR (mandatory)
```

---

## 2. Incident Register

```
INCIDENT REGISTER — 2026–27 (Chief Warden accessible)

Incident ID | Date       | Student          | Category | Nature             | Status
────────────────────────────────────────────────────────────────────────────────────────
INC-2701    | 15 Sep '26 | Rahul T. (312)   | A        | Alcohol found (beer) | Expelled
INC-2702    | 28 Oct '26 | Arun K. (511)    | B        | Cooking in room      | Warning ✅
INC-2703    | 12 Nov '26 | Suresh V. (318)  | C        | Noise after 11 PM    | Verbal warning ✅
INC-2704    | 3 Jan '27  | Deepak P. (622)  | B        | Late return ×3       | Outpass suspended 30d ✅
INC-2705    | 20 Feb '27 | [Anonymous]      | —        | Ragging complaint    | Under inquiry ⬜
INC-2706    | 15 Mar '27 | Vikram L. (715)  | C        | Room untidy ×2       | Written warning ✅

INCIDENT INC-2701 DETAIL:
  Reported by: Night supervisor Gangadhar (during rounds)
  Finding: 6 beer cans in student's wardrobe (open room inspection — student consent +
           warden witness per UGC guidelines; no arbitrary search)
  Action:
    1. Chief Warden informed (11 PM call)
    2. Student confronted with 2 witnesses
    3. Parents called (father — next morning)
    4. Hostel Disciplinary Committee convened within 48 hours
    5. Decision: Expelled from hostel; allowed to complete semester from day school
    6. Written communication to student + parents ✅
    7. College Disciplinary Committee notified (for academic records annotation)

INCIDENT INC-2705 DETAIL (Ragging — Under Inquiry):
  Complaint source: Anonymous (via Anti-Ragging Committee helpline — routed to hostel)
  Nature: Reported verbal ragging of first-year student in common room
  Complainant identity: Not disclosed (protected — UGC Reg 4.2)
  Accused: Not yet identified (CCTV review in progress — 20 Feb 2027 9 PM, Block A common room)
  Status: Anti-Ragging Committee inquiry; CCTV footage preserved (Chief Warden lock)
  Timeline: Must complete inquiry within 30 days (UGC timeline)
```

---

## 3. Hostel Disciplinary Committee

```
HOSTEL DISCIPLINARY COMMITTEE

COMPOSITION:
  Chief Warden (Chairperson)
  Warden of the relevant hostel
  One senior faculty member (nominated by Principal)
  One student representative (from Hostel Committee — not the accused's year)

PROCEDURES:
  Notice: 48-hour advance notice to student (written)
  Rights: Student may give written representation; may bring one student representative
          (not a lawyer — internal proceedings)
  Minutes: Signed by all members
  Decision: Majority; Chief Warden has casting vote
  Communication: Written decision within 7 days
  Appeal: To Principal/Director within 15 days

RECORDS:
  All proceedings documented in EduForge
  Available for NAAC (anti-ragging and student welfare criterion)
  Available for UGC Anti-Ragging Monitoring Cell (if escalated)

EXPELLED STUDENTS:
  Hostel exit record marked: "Expelled — Disciplinary"
  Allotment cancelled; room re-allocated
  Security deposit: Refunded net of any damage/dues
  Re-application: Barred for rest of academic year; may apply fresh next year
                  (for minor offences; major/ragging = barred permanently from hostel)
```

---

## 4. Property Damage Register

```
PROPERTY DAMAGE REGISTER

Damage ID | Date    | Room  | Student   | Description                | Recovery
──────────────────────────────────────────────────────────────────────────────────
DMG-4401  | Aug '26 | A-218 | Kiran T.  | Broken mirror              | ₹800 from deposit
DMG-4402  | Oct '26 | B-115 | Suresh M. | Chair backrest broken      | ₹600 from deposit
DMG-4403  | Jan '27 | C-207 | Priya K.  | Hole in wall (large, not   | ₹1,200 charged to
           |         |       |           | normal wear)               | account (paid)
DMG-4404  | Mar '27 | B-117 | Vinod K.  | Small picture-hanging hole | ₹200 deducted
           |         |       |           | (check-out)                | from deposit

TOTAL PROPERTY DAMAGE RECOVERED (2026–27 YTD): ₹2,600

NORMAL WEAR (Not charged):
  Paint scuffs, minor scratches on furniture, minor floor stains, small nail holes
  EduForge damage assessment guide: Photo-based; warden uses standardised charge table
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hostel/incidents/` | All incidents (Chief Warden) |
| 2 | `POST` | `/api/v1/college/{id}/hostel/incidents/` | Log new incident |
| 3 | `GET` | `/api/v1/college/{id}/hostel/incidents/{id}/` | Incident detail |
| 4 | `POST` | `/api/v1/college/{id}/hostel/incidents/{id}/action/` | Record disciplinary action |
| 5 | `GET` | `/api/v1/college/{id}/hostel/damage/` | Property damage register |
| 6 | `POST` | `/api/v1/college/{id}/hostel/damage/` | Record damage and recovery |

---

## 6. Business Rules

- Alcohol possession by students under 18 in hostel rooms is a criminal offence under the Telangana Prohibition Act; for students over 18 it is still a violation of hostel rules (hostel is college premises); however, the disciplinary response must be proportionate — first-time possession of small quantities warrants a serious warning + parental meeting; immediate FIR for first-time alcohol possession is disproportionate unless accompanied by another offence; expulsion from hostel is appropriate, but academic expulsion requires further process
- Room searches must follow due process; wardens cannot conduct arbitrary room searches; a search requires the student's presence (or a written notice if the student is unreachable) and must be done in the presence of at least two witnesses (another warden or senior staff); evidence found without due process may be challenged in a disciplinary appeal; EduForge's incident module captures the search procedure compliance checklist
- Ragging incidents where the complaint is received via anonymous helpline must still be investigated; the complainant's anonymity is protected under UGC Regulation 4.2; the institution cannot dismiss a complaint simply because the complainant is anonymous; CCTV footage and witness statements must be explored as alternative evidence
- The Hostel Disciplinary Committee must not include the accused student's department faculty as members to avoid conflicts of interest; impartiality is a due process requirement; decisions made by a biased committee can be set aside in a High Court writ
- Hostel expulsion does not automatically carry academic consequences; a student expelled from hostel can continue studies as a day scholar; conflating hostel misconduct with academic standing (e.g., marking attendance absent during hostel inquiry) is a violation of the student's academic rights

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division D*
