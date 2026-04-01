# G-01 — AICTE Inspection & Extension of Approval

> **URL:** `/college/compliance/aicte/`
> **File:** `g-01-aicte-inspection.md`
> **Priority:** P1
> **Roles:** Compliance Officer (S4) · Principal/Director (S6) · Trust/Management (S7)

---

## 1. AICTE EoA (Extension of Approval) Status

```
AICTE EXTENSION OF APPROVAL — GCEH
Academic Year: 2026–27

EoA STATUS:
  Application submitted: 31 October 2025 (AICTE portal — aicte-india.org)
  Fee paid: ₹1,05,000 (GCEH — 556 students approved intake equivalent)
  Scrutiny completed: ✅ December 2025
  EoA issued: ✅ 28 February 2026
  EoA validity: 2026–27 academic year

APPROVED INTAKE (2026–27):
  B.Tech CSE:    180 seats   |  Actual admitted: 176 (97.8%)
  B.Tech ECE:    120 seats   |  Actual admitted: 112 (93.3%)
  B.Tech EEE:     60 seats   |  Actual admitted: 54 (90.0%)
  B.Tech Mech:    60 seats   |  Actual admitted: 58 (96.7%)
  M.Tech CSE:     24 seats   |  Actual admitted: 18 (75.0%)
  MBA:            60 seats   |  Actual admitted: 52 (86.7%)
  MCA:            60 seats   |  Actual admitted: 38 (63.3%) ← below 66% → flag
  Total:         564 seats   |  Total admitted: 508 (90.1%)

MCA BELOW 66% ALERT:
  AICTE requires intake reduction if admissions are consistently below 66%
  MCA: 3rd consecutive year below 66%
  Action: College filed voluntary intake reduction application (60→30) for 2027–28
  EoA 2027–28: MCA intake 30 (pending AICTE approval)

DEFICIENCY COMPLIANCE STATUS (from last inspection):
  Deficiency noted 2024: Shortage of 3 faculty in CSE (below AICTE PTR of 1:15)
  Corrective action: 3 faculty appointed June 2025 ✅
  Current CSE PTR: 180 students / 14 faculty = 12.9:1 ← within 1:15 limit ✅
```

---

## 2. AICTE Inspection

```
AICTE INSPECTION — GCEH (Last: April 2025)

INSPECTION TYPES:
  1. EoA processing inspection: Scrutiny committee visits if deficiencies found
  2. Suo-motu inspection: AICTE-triggered on complaint or random selection
  3. Compliance inspection: Post-deficiency to verify corrective action

APRIL 2025 INSPECTION DETAIL:
  Type: Compliance inspection (post-deficiency on CSE faculty)
  Date: 14 April 2025 (3 weeks notice given)
  Inspectors: Dr. Ravi Shankar (JNTU) + AICTE Regional Officer

INSPECTION FINDINGS:
  Area                          | Finding                        | Status
  ─────────────────────────────────────────────────────────────────────────────
  CSE Faculty count             | 3 faculty added — deficiency    | ✅ Cleared
                                | resolved                        |
  Lab equipment (CSE lab)       | 3 workstations outdated (>5 yr) | Partially cleared
                                | 12 replaced; 3 pending          | ⚠️
  Library books (CSE branches)  | 2,400 new titles needed         | Ongoing
                                | (AICTE norm: 1 title/student)   |
  Faculty PhD qualification     | 4 faculty without PhD in Mech   | Action plan noted
                                | (UGC norms: PhD preferred)      |
  NBA Criterion (OBE)           | Outcome-based curriculum docs   | Submitted ✅
                                | missing for 2 programmes        |

  Overall finding: "Satisfactory — minor deficiencies to be resolved within 6 months"
  Final EoA: Approved without conditions

INSPECTION CHECKLIST (EduForge pre-inspection module):
  ✅ All faculty service books up to date
  ✅ Staff registers (teaching + non-teaching) ready
  ✅ Lab inventories (equipment list with purchase proof)
  ✅ Library catalogue (SOUL software print + AICTE form)
  ✅ Building completion certificate + fire NOC
  ✅ Student enrollment data (EAPCET certificates)
  ✅ Financial statements (last 3 years)
  ✅ Fee structure (AFRC approved) displayed
  ✅ Mandatory disclosure link active on website
  ⚠️ 3 workstations replacement pending (procurement in process)
```

---

## 3. AICTE Mandatory Disclosure (Web)

```
AICTE MANDATORY DISCLOSURE — Online Status

URL: www.gceh.ac.in/mandatory-disclosure (live link — AICTE requirement)
AICTE portal link: Updated on aicte-india.org ✅
Last updated: 15 July 2026 (must update at start of each academic year)

REQUIRED SECTIONS (AICTE format):
  Section A: Institution details (name, address, contact, map)
  Section B: AICTE approval (EoA number, date, validity)
  Section C: Academic programmes (approved intake, fees, admission criteria)
  Section D: Faculty details (name, qualification, designation, experience)
  Section E: Infrastructure (buildings, labs, library, hostels)
  Section F: Placement data (prior year — E-04 data feeds here)
  Section G: Financial details (last year P&L summary)
  Section H: Fee structure (AFRC-approved — C-01 data feeds here)

COMPLIANCE CHECK:
  ✅ All 8 sections present and updated
  ✅ Fee structure matches AFRC approval (₹85,000 convener, ₹1,40,000 management)
  ✅ Faculty count matches service book records
  ⚠️ 1 faculty qualification mismatch (Dr. X updated PhD this year — auto-update pending)

AICTE PENALTY FOR NON-DISCLOSURE:
  Non-publication or outdated mandatory disclosure → EoA rejection risk
  AICTE has rejected EoA for colleges that did not update mandatory disclosure for 2+ years
  EduForge sends automated annual reminder (15 June) to update mandatory disclosure
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/compliance/aicte/eoa/` | Current EoA status |
| 2 | `GET` | `/api/v1/college/{id}/compliance/aicte/inspection/` | Inspection history |
| 3 | `GET` | `/api/v1/college/{id}/compliance/aicte/checklist/` | Pre-inspection checklist |
| 4 | `GET` | `/api/v1/college/{id}/compliance/aicte/disclosure/status/` | Mandatory disclosure status |
| 5 | `POST` | `/api/v1/college/{id}/compliance/aicte/disclosure/update/` | Update disclosure section |

---

## 5. Business Rules

- EoA application must be filed by 31 October each year without exception; late filing results in late fees and risks EoA non-renewal which means the college cannot admit students for that academic year — this is an existential risk; EduForge triggers reminders from 1 October and escalates to Principal and Trust by 15 October if not submitted
- When intake is consistently below 66% for 3 years, proactive voluntary intake reduction is better than waiting for AICTE to impose reduction; voluntary reduction demonstrates institutional self-awareness and regulatory good faith; forced reduction after audit is more damaging reputationally and often comes with additional conditions
- AICTE inspectors verify physical presence of listed faculty against service books and salary records; ghost faculty (listed on paper but not actually employed) is a serious fraud that results in cancellation of approval and criminal proceedings; EduForge's payroll-service book integration ensures faculty listed in AICTE records are the same as payroll-active faculty
- Mandatory disclosure must reflect actual fee structures — if students were charged differently from the AFRC-approved fee during the year, and the mandatory disclosure shows the approved fee, the institution is exposed to consumer complaints; the mandatory disclosure is public-facing evidence of the college's commitments
- The AICTE Approval Process Handbook changes annually; the compliance requirements for 2027–28 may differ from 2026–27; GCEH must download the new handbook in November and review changes before the EoA filing; EduForge links to the handbook's official URL for quick reference

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division G*
