# B-36 — UFM (Unfair Means) Register

> **URL:** `/school/academic/exams/ufm/`
> **File:** `b-36-ufm-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Cell Head (S4) — full · Invigilator teachers — file report · Principal (S6) — full (UFM committee chair)

---

## 1. Purpose

The Unfair Means (UFM) register is the formal documentation system for exam malpractice incidents. When an invigilator catches a student copying, using mobile phones, carrying cheat material, or engaging in any form of exam fraud, they file a UFM report immediately. A school-level UFM committee (Principal + 2 senior teachers) reviews each case and decides the outcome. CBSE has a formal UFM policy that schools are required to follow. Outcomes range from a warning to cancellation of the paper. For board exams, CBSE itself handles the UFM process; this register handles internal school exam UFMs. The register is a legal document and must be maintained for audit purposes.

---

## 2. Page Layout

### 2.1 Header
```
UFM (Unfair Means) Register                       [+ File UFM Report]  [Export Register]
Academic Year: 2025–26
Total Cases: 8  ·  Decided: 6  ·  Pending: 2  ·  Board Referred: 0
```

---

## 3. UFM Cases List

| Case # | Exam | Date | Student | Class | Hall | Invigilator | UFM Type | Status | Outcome |
|---|---|---|---|---|---|---|---|---|---|
| UFM-2026-001 | Annual Exam | 1 Mar | Deepak M | IX-A | Hall B | Mr. Rajan | Cheat slip found | ✅ Decided | Warning issued |
| UFM-2026-002 | Annual Exam | 3 Mar | Anand T | VIII-B | Hall C | Ms. Leela | Copying from neighbour | ✅ Decided | Paper cancelled (Maths) |
| UFM-2026-003 | Annual Exam | 4 Mar | Suresh K | X-A | Hall A | Mr. Suresh | Mobile phone found (off) | ✅ Decided | Warning — mobile confiscated |
| UFM-2026-004 | Annual Exam | 6 Mar | Priya L | XI-B | Hall D | Dr. Anand | Communication device | ✅ Decided | Paper cancelled + parent meeting |
| UFM-2026-005 | Half-Yearly | 18 Oct | Rahul G | IX-B | Hall B | Ms. Suma | Cheat slip | ✅ Decided | Warning |
| UFM-2026-006 | Annual Exam | 9 Mar | Ajay M | XI-A | Hall A | Ms. Kavitha | Impersonation attempt | ⚠️ Under inquiry | — |
| UFM-2026-007 | Annual Exam | 11 Mar | Vijay K | VII-A | Hall C | Mr. Bala | Cheat slip | ⚠️ Committee pending | — |
| UFM-2026-008 | Annual Exam | 13 Mar | Kavitha R | XII-A | Hall B | Ms. Pooja | Unauthorized material | ⚠️ Committee pending | — |

---

## 4. File UFM Report (Invigilator)

[+ File UFM Report] → drawer (600px) — available to invigilators during/after exam:

```
UFM Report

Exam:          [Annual Exam 2025–26 ▼]
Date:          [1 Mar 2026]
Hall:          [Hall B ▼]
Period/Time:   [10:00 AM – 12:20 PM — Physics paper]

Student Name:  [Search student ▼]
Roll Number:   [Auto-filled]
Class:         [Auto-filled]

UFM Type: [Select ▼]
  → Cheat slip / written material found
  → Copying from neighbour
  → Mobile phone / electronic device
  → Communication with outside (signals, calls)
  → Impersonation (different person attempting)
  → Passing answers between students
  → Books / notes inside hall
  → Tampering with answer script
  → Other (specify)

Description of Incident:
[Student found with a paper slip tucked inside watch strap containing
formulae for Physics. Slip confiscated and attached. Student warned
verbally and allowed to continue under close watch.              ]

Material Confiscated: [Yes ▼]  Description: [Cheat slip — Physics formulae]
Student's Response/Statement: [Student denied initially, then admitted]

Witnesses:
  Co-invigilator / Reliever: [Ms. Kavitha Reddy ▼]

Attached Evidence: [Upload photo of confiscated material]

[Submit UFM Report]
```

Once submitted:
- Exam Cell Head is notified immediately
- Student is not removed from the exam unless the UFM type warrants it (Exam Cell Head decides)
- Parent notification is triggered (configurable — some schools prefer to notify after decision)

---

## 5. UFM Case Detail (`ufm-case-detail`, 600px)

### Case UFM-2026-002: Anand T — VIII-B — Annual Exam Maths

```
Filed by: Ms. Leela (Hall C Invigilator)  ·  Filed: 3 Mar 2026, 10:45 AM

Incident:   Copying from neighbour — student observed repeatedly looking at
            Rahul Kumar (Hall C, Seat C08) and copying answers.

Evidence:   Answer scripts compared — identical long-form answers for Q14 and Q16

Student Statement: "I was checking my own paper" (denied copying)
Neighbour (Rahul K) Statement: "I did not show my paper"

UFM Committee:
  Chair:    Principal Rajan T
  Member 1: Ms. Priya (HOD Maths)
  Member 2: Mr. Bala (HOD Physics)
  Meeting:  5 Mar 2026, 11:00 AM

Decision (5 Mar):  Paper CANCELLED — Mathematics
  Rationale: Evidence compelling (identical answers). Pattern identified.
  Additional:  Formal warning letter issued. Parent meeting on 7 Mar.
  Suspension:  No (first offence)

Parent Meeting: 7 Mar 2026 — Parent: Mr. Govind T (father)
  Outcome: Parent acknowledged, signed warning letter

Status: ✅ CLOSED
```

---

## 6. UFM Outcomes Reference

| Outcome | When Applied | CBSE Basis |
|---|---|---|
| Warning (verbal) | Minor offence, first time, material not used | CBSE UFM norms |
| Warning (written) + Parent meeting | Cheat material found but not used | CBSE norms |
| Cancellation of one paper | Evidence of actual copying in specific subject | CBSE norms |
| Cancellation of all papers | Systematic organised cheating | CBSE norms |
| Suspension from exam hall | Disruptive behaviour during exam | School authority |
| Expelled from exam centre | Extreme case (assault of invigilator, etc.) | School + CBSE escalation |
| Refer to CBSE | Board exam UFM — school's process ends here; CBSE takes over | CBSE UFM policy 2023 |

---

## 7. CBSE Board Exam UFM

For CBSE board exams, the school UFM process is:
1. Invigilator files report on CBSE's physical UFM form (Form UFM-1)
2. Exam Cell Head collects the form, seals it with the student's answer script
3. Submitted to CBSE examination centre coordinator
4. CBSE handles the investigation from this point
5. School logs the incident in EduForge as "Referred to CBSE" — outcome is received from CBSE later

---

## 8. Analytics

| Metric | Value |
|---|---|
| Total UFM cases (this year) | 8 |
| Most common type | Cheat slip (4 cases) |
| Most affected class | IX (3 cases) |
| Recidivism | 0 (no student has 2+ cases) |
| Paper cancellations | 2 |
| Board referrals | 0 |

Year-on-year trend (last 3 years) to spot if malpractice is increasing or decreasing.

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/ufm/?year={year}&exam_id={id}` | UFM cases list |
| 2 | `POST` | `/api/v1/school/{id}/ufm/` | File UFM report |
| 3 | `GET` | `/api/v1/school/{id}/ufm/{case_id}/` | Case detail |
| 4 | `PATCH` | `/api/v1/school/{id}/ufm/{case_id}/decision/` | Record committee decision |
| 5 | `POST` | `/api/v1/school/{id}/ufm/{case_id}/parent-meeting/` | Log parent meeting |
| 6 | `GET` | `/api/v1/school/{id}/ufm/analytics/` | UFM statistics |
| 7 | `GET` | `/api/v1/school/{id}/ufm/export/?year={year}` | Export register PDF |

---

## 10. Business Rules

- UFM reports cannot be deleted or edited after submission; only the committee's decision field is editable (by Principal/Exam Cell Head)
- The student whose paper is cancelled has their marks recorded as "UFM — Paper Cancelled" in B-16; marks entry for that subject-student is blocked
- Parent notification: for students below 18, parent is notified within 24 hours of a decision; for 18+ students, direct communication to student is primary
- UFM register is confidential — only Exam Cell Head, Principal, and VP Academic can see the full list; individual invigilators can only see cases they filed
- Repeat UFM offenders (2+ cases in different exams) are flagged for school disciplinary committee
- Export register generates in CBSE inspection format for compliance documentation

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
