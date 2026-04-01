# B-04 — Question Paper Bank & Exam Security

> **URL:** `/college/academic/qp/`
> **File:** `b-04-question-papers.md`
> **Template:** `portal_base.html` (light theme, high security)
> **Priority:** P1
> **Roles:** Examination Controller (S4) — full access · HOD (S4) — upload and review papers for own department · Faculty (S3) — upload own paper (sealed until exam) · Principal/Director (S6) — override access

---

## 1. Purpose

Manages the creation, secure storage, and controlled release of question papers for internal (CIE mid-term) exams. Question paper security is an institutional reputation issue — a leaked question paper invalidates the exam and creates legal and academic integrity risks.

Security model:
- Faculty uploads the question paper (sealed in encrypted form)
- HOD reviews for quality and syllabus coverage (without breaking the seal — uses a paper metadata review, not content review)
- Examination Controller prints and distributes on exam day (just-in-time)
- Access log is maintained for every view

---

## 2. Question Paper Upload

```
QUESTION PAPER UPLOAD — Dr. Anita K.
Course: CS201 — Data Structures & Algorithms
Exam: Mid-II (20 March 2027)
Max Marks: 30  |  Duration: 2 hours

PAPER STRUCTURE (JNTU format):
  Part A: 5 short questions × 2 marks = 10 marks (all compulsory)
  Part B: 5 questions with internal choice (answer any 1 from each) × 4 marks = 20 marks
  Total: 30 marks

COVERAGE:
  Unit III (Trees): 40% of paper ✅
  Unit IV (Graphs): 40% ✅
  Units I–II recall: 20% ✅
  [Syllabus coverage confirmed by faculty ✅]

UPLOAD:
  File: CS201_MidII_2027.pdf (encrypted on upload)
  Uploaded at: 10 March 2027, 2:15 PM (10 days before exam ✅)
  Status: Sealed 🔒 (only Examination Controller can open before exam day)

SECURITY:
  Access log: [Dr. Anita K. — uploaded — 10 Mar 2027 2:15 PM]
  Next access: [Examination Controller — printing — 20 Mar 2027 7:00 AM]

  WHO CAN ACCESS THIS PAPER:
    Dr. Anita K. (faculty): Upload only; cannot re-view after upload
    HOD: Metadata only (marks distribution, syllabus coverage) — NOT content
    Examination Controller: Full access for printing (audit logged)
    Principal: Emergency override access (full audit)
```

---

## 3. Examination Controller — Day-of-Exam View

```
EXAM DAY — 20 March 2027
Mid-II Examinations

PAPERS TO PRINT TODAY:
  Course   Class     Time      Copies  Status
  CS201    CSE-A+B   10:00 AM  80+5*   🔓 Released at 7:30 AM (90 min before exam)
  CS203    CSE-A+B   10:00 AM  80+5    🔓 Released at 7:30 AM
  CS205    CSE-C+D   10:00 AM  80+5    🔓 Released at 7:30 AM
  [...]
  * +5 = 5 extra copies (for latecomers, spares)

PAPER DISTRIBUTION PROTOCOL:
  7:00 AM: Examination Controller unlocks papers
  7:30 AM: Printed (college print room — only authorised staff)
  9:00 AM: Papers sealed in envelopes, handed to invigilators
  10:00 AM: Invigilators distribute to students in exam hall

MALPRACTICE PROTOCOL:
  If paper leak is suspected before exam:
    1. All copies recalled immediately
    2. Faculty prepares alternate paper (must be ready as backup)
    3. Exam delayed by 30 minutes maximum
    4. Enquiry initiated
  [Alternate paper option: Faculty uploads backup paper (sealed separately) ← recommended]
```

---

## 4. Question Paper Bank

```
QUESTION PAPER BANK — Archive (Past Papers)
[Available AFTER exams — released for student revision]

Course  Exam       Year      Status    Available
CS201   Mid-I      2026–27   ✅ Done   Released for students ✅
CS201   Mid-II     2026–27   ✅ Done   Released for students ✅
CS201   Annual*    2025–26   ✅ JNTU   Released by JNTU (public)
CS203   Mid-I      2026–27   ✅ Done   Released ✅

* JNTU previous year papers are public; college previous year internal papers
  are released after exam (end of semester)

NAAC EVIDENCE:
  Q-bank with last 5 years papers = NAAC criterion 2.3 evidence
  [Download NAAC evidence package]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/college/{id}/qp/upload/` | Upload question paper (encrypted, sealed) |
| 2 | `GET` | `/api/v1/college/{id}/qp/{qp_id}/metadata/` | Paper metadata (HOD view — no content) |
| 3 | `POST` | `/api/v1/college/{id}/qp/{qp_id}/release/` | Release paper for printing (EC only) |
| 4 | `GET` | `/api/v1/college/{id}/qp/archive/?course={code}` | Past paper archive (post-exam) |
| 5 | `GET` | `/api/v1/college/{id}/qp/{qp_id}/audit-log/` | Access log for the paper |

---

## 6. Business Rules

- Question papers are encrypted at rest (AES-256) immediately on upload; only the Examination Controller's credentials can decrypt for printing; this ensures that even if the EduForge database is compromised, encrypted papers are not readable
- Faculty cannot re-access their own uploaded paper after submission — this prevents the faculty from sharing the paper with students (the most common leak vector); if faculty needs to make a correction post-upload, they must contact the Examination Controller who can facilitate a controlled re-upload with a new version
- The 90-minute early release window (papers released 90 minutes before exam) is a deliberate design — enough time to print and distribute, but not enough time for a leak to spread to all students; same-day printing (vs. day-before printing) is standard anti-leak practice
- NAAC criterion 2.3 specifically requires evidence of a "question bank" and "examination reforms"; a digital, audited question paper system with encryption is evidence of examination system robustness that NAAC assessors appreciate

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division B*
