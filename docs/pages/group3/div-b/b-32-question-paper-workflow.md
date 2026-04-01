# B-32 — Question Paper Workflow

> **URL:** `/school/academic/exams/<exam_id>/question-papers/`
> **File:** `b-32-question-paper-workflow.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Cell Head (S4) — full · HOD (S4) — own dept review/approve · Subject Teacher (S3) — submit draft · Principal (S6) — full

---

## 1. Purpose

Manages the question paper's journey from teacher-drafted document to sealed examination-ready set. B-04 stores individual questions; B-32 manages the assembled question paper document. The custody chain — who drafted it, who reviewed it, when it was approved, how many copies were printed, who received them, and when the cover was opened — is a critical examination integrity requirement. CBSE has explicit guidelines on question paper confidentiality. Any leak or security breach in the QP process is a serious disciplinary matter. This page provides the documented trail.

**Stages:** Draft → HOD Review → HOD Approved → Exam Cell Received → Printing → Copies Counted → Sealed → Dispatched to Halls → Cover Opened (Day-of)

---

## 2. Page Layout

### 2.1 Header
```
Question Paper Workflow — Annual Exam 2025–26     [Export Custody Log]
Exam: Annual Exam 2025–26  ·  Classes: VI–XI
Total QPs Required: 82  ·  Approved: 68  ·  Pending HOD Review: 8  ·  Submitted: 6  ·  Overdue: 4
Status: ⚠️ 4 QPs overdue (exam in 8 days)
```

---

## 3. QP Status Board

| Subject | Class | Assigned Teacher | Draft Submitted | HOD Review | Exam Cell | Printing | Sealed | Status |
|---|---|---|---|---|---|---|---|---|
| English | VI–VIII | Ms. Suma | ✅ 18 Feb | ✅ 20 Feb | ✅ 21 Feb | ✅ 24 copies | ✅ 25 Feb | ✅ Ready |
| Mathematics | VI–VIII | Mr. Arjun | ✅ 19 Feb | ✅ 21 Feb | ✅ 22 Feb | ✅ 24 copies | ✅ 26 Feb | ✅ Ready |
| Physics | IX, XI | Ms. Lakshmi | ✅ 21 Feb | 🔄 With HOD | — | — | — | 🔄 HOD Review |
| Chemistry | IX, XI | Mr. Ravi | ⬜ Not submitted | — | — | — | — | 🔴 Overdue |
| Biology | IX, XI | Ms. Anjali | ⬜ Not submitted | — | — | — | — | 🔴 Overdue |
| History | XI | Mr. Suresh | ✅ 20 Feb | ✅ 22 Feb | ✅ 23 Feb | ✅ 8 copies | ✅ 26 Feb | ✅ Ready |

---

## 4. QP Draft Submission (Teacher View)

Teachers submit question papers for HOD review:

[Submit QP Draft] → drawer:

| Field | Value |
|---|---|
| Exam | Auto-filled from exam context |
| Subject | Dropdown |
| Class(es) | Multi-select (can submit one paper for multiple classes) |
| Paper type | Written / MCQ / Mixed |
| Total Marks | Number |
| Duration | Minutes |
| Method | Upload PDF / Compose from Question Bank (B-04) |
| Confidentiality | ✅ Marked confidential (default — restricts access) |
| Set (optional) | Set A / Set B / Set C (for multiple paper sets) |

**Upload PDF path:** Teacher uploads the question paper as a password-protected PDF (EduForge accepts the password at upload and stores it encrypted). The PDF is stored in Cloudflare R2 with restricted access.

**Compose from B-04 path:** Pulls the draft paper assembled in B-04's "Generate Paper" wizard.

---

## 5. HOD Review & Approval Drawer (`qp-review-approval`, 680px)

HOD clicks [Review] on any pending QP:

### Drawer: Physics — Classes IX, XI — Annual Exam

```
QP Review: Physics · Class IX & XI
Submitted by: Ms. Lakshmi Devi · 21 Feb 2026 · 8:14 PM

[Preview Paper PDF]  [Download for Review]

HOD Review Checklist:
  ☑ Coverage: Are all syllabus units represented?
  ☑ Balance: Difficulty distribution — Easy: 32%, Medium: 48%, Hard: 20% ✅
  ☑ Marks: Total marks = 80 (as required)
  ☑ Section format: CBSE prescribed sections (A/B/C/D/E)
  ☑ Language: No ambiguous questions
  ☐ Answer key attached
  ☐ Marking scheme attached

HOD Notes:
[  Q14 (LA) is similar to Q in UT2 — suggest changing to avoid repetition   ]
[                                                                             ]

Action:
  [✅ Approve QP]   [🔄 Return for Revision]   [❌ Reject — Needs complete redo]
```

---

## 6. Exam Cell Processing

After HOD approval, Exam Cell Head takes over:

| Step | Action | Recorded By | Date |
|---|---|---|---|
| 1 | Received from HOD | Exam Cell Head | 22 Feb |
| 2 | Typesetting check | Office Staff | 23 Feb |
| 3 | Printing | Office/Press | 24 Feb — 24 copies |
| 4 | Copies counted | Exam Cell Head + 1 witness | 24 Feb — exact count: 24 |
| 5 | Sealed in envelopes | Exam Cell Head | 25 Feb |
| 6 | Stored (locked) | Exam Cell Head | 25 Feb — almirah no. 3 |
| 7 | Dispatched to invigilators | Hall-in-charge | 1 Mar, 9:50 AM |
| 8 | Cover opened | Invigilator (Hall A, Ms. Suma) | 1 Mar, 10:00 AM — student witness |

Each step is logged with timestamp, person responsible, and notes.

---

## 7. Seal & Custody Record

```
QP Seal Record: Physics · Class IX + XI

Copies Printed:    24
Seal Type:         Wax seal / Tamper-evident sticker ← school choice
Sealed By:         Mr. Exam Cell Head (Rajan Kumar)
Witness:           Mr. Suresh (HOD Science)
Date Sealed:       25 Feb 2026, 4:30 PM
Storage Location:  Exam Cell Almirah No. 3 (Key held by Principal)
```

**On exam day:**

```
Cover Opening Record: Physics · Hall A

Opened By:         Ms. Suma (Hall A Invigilator)
Student Witness:   Roll No. 001 (Arjun Sharma)
Time Opened:       10:00 AM (exam start time)
Condition:         Seal intact (no tampering)
Copies Distributed: 43 (present students)
Remaining:         1 (spare)
```

---

## 8. QP Security Incidents

If a QP security incident is reported (paper leaked before exam, seal broken prematurely):

[+ Report Incident] → triggers an immediate escalation:
- Principal notified in real-time
- Exam postponed for affected class (manual decision by Principal)
- Incident logged (feeds CBSE inquiry if required)
- Exam Cell Head cannot delete or modify incident report once created

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/question-papers/` | QP status board |
| 2 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/question-papers/` | Teacher submits QP draft |
| 3 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/question-papers/{qp_id}/` | QP detail |
| 4 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/question-papers/{qp_id}/hod-review/` | HOD review action |
| 5 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/question-papers/{qp_id}/exam-cell-step/` | Log Exam Cell step |
| 6 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/question-papers/{qp_id}/seal/` | Record sealing |
| 7 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/question-papers/{qp_id}/open-cover/` | Record cover opening |
| 8 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/question-papers/{qp_id}/incident/` | Report security incident |
| 9 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/question-papers/export/` | Custody log export |

---

## 10. Business Rules

- QP PDFs are stored encrypted (AES-256) in Cloudflare R2; only HOD and Exam Cell Head can download them — access logged in audit trail
- A teacher's QP PDF access is revoked once it is submitted to the HOD — they cannot access the file anymore (prevents accidental leak by the paper setter)
- Once sealed, the QP cannot be retrieved without triggering a "Seal Breach" flag requiring Principal acknowledgement
- HOD-rejected QPs (full reject) must be re-submitted fresh; a rejected paper cannot be revised and re-submitted — new paper required
- The custody log is immutable after 48 hours of each step being logged; corrections require Principal authorisation
- Board exam QPs (CBSE) are handled by the board — only cover-opening is logged here

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
