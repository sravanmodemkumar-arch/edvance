# B-15 — Answer Script Management

> **URL:** `/school/academic/exams/<exam_id>/scripts/`
> **File:** `b-15-answer-script-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Cell Head (S4) — full · Principal (S6) — view

---

## 1. Purpose

Manages the lifecycle of answer scripts (answer booklets) from distribution before the exam through collection, evaluation (marking), return to students, and retention/disposal. The Exam Cell Head is accountable for knowing exactly how many answer scripts were issued, collected, and evaluated — a miscount is a serious examination integrity issue. In many state boards and CBSE schools, scripts must be retained for a defined period before disposal. Students also have the right to request a copy of their evaluated script (RTI/CBSE circular provision). This page provides the custody chain for all scripts.

---

## 2. Page Layout

### 2.1 Header
```
Answer Script Management — Annual Exam 2025–26    [Stationery Issue]  [Script Count Log]
Exam: Annual Exam 2025–26  ·  Date Range: 1–20 Mar 2026
Total Sessions: 14  ·  Scripts Issued (all sessions): 18,442  ·  Scripts Collected: 18,430  ·  Missing: 12 ⚠️
```

---

## 3. Session-wise Script Register

| Date | Subject | Classes | Expected Scripts | Issued | Collected | Difference | Status | Evaluator | Evaluation |
|---|---|---|---|---|---|---|---|---|---|
| 1 Mar | English | VI–XI | 2,182 | 2,182 | 2,178 | -4 ⚠️ | Collecting | Class Teachers | In progress |
| 3 Mar | Mathematics | VI–XI | 1,980 | 1,980 | 1,980 | 0 | Collected ✅ | Subject Teachers | In progress |
| 4 Mar | Physics | IX, XI | 316 | 316 | 316 | 0 | Collected ✅ | Ms. Lakshmi | Complete |
| 4 Mar | Science | VI–VIII | 580 | 580 | 579 | -1 ⚠️ | Investigating | Subject Teachers | Pending |

**Difference** — discrepancy between issued and collected scripts. Any shortfall is a serious issue:
- Immediate investigation launched (which hall, which invigilator, which students)
- Principal notified automatically if shortfall > 0
- Resolution options: Student submitted late (added to collected), Script miscount at issuance, Possible retention by student (hall invigilator to check)

---

## 4. Script Distribution (Pre-Exam)

Before each exam session, the Exam Cell issues answer booklets to hall invigilators:

[Stationery Issue] → opens the daily stationery distribution log:

| Hall | Invigilator | Students Expected | Blank Scripts Issued | Extra Issued | Received By | Time |
|---|---|---|---|---|---|---|
| Hall A | Ms. Suma | 45 | 50 (+5 extra) | ✅ | Ms. Suma (sign) | 09:50 |
| Hall B | Mr. Rajan | 45 | 50 (+5 extra) | ✅ | Mr. Rajan (sign) | 09:52 |
| Hall C | Ms. Leela | 44 | 49 (+5 extra) | ✅ | Ms. Leela (sign) | 09:55 |

Standard practice: issue (expected + 5 extra) scripts per hall; extras returned after exam.

---

## 5. Script Collection (Post-Exam)

After each session:
1. Invigilators count scripts in their hall before sealing the bundle
2. Bundle submitted to Exam Cell with hall record slip
3. Exam Cell Head counts and logs:

**Post-session collection log (1 Mar, English):**

| Hall | Scripts Expected (Students Present) | Scripts Received | Signed by Invigilator | Notes |
|---|---|---|---|---|
| Hall A | 43 (2 absent) | 43 | Ms. Suma ✅ | — |
| Hall B | 44 (1 absent) | 44 | Mr. Rajan ✅ | — |
| Hall C | 44 | 43 | Ms. Leela ✅ | 1 script extra time (special needs) — collected separately |
| Hall D | 46 | 46 | Dr. Anand ✅ | — |

---

## 6. Script Distribution for Evaluation

After collection, scripts are distributed to evaluating teachers:

| Subject | Class | Scripts Count | Assigned Evaluator | Date Given | Date Expected Return | Status |
|---|---|---|---|---|---|---|
| English (VI-A) | 42 | Ms. Suma | 2 Mar | 7 Mar | ✅ Returned |
| English (VI-B) | 40 | Ms. Parvathi | 2 Mar | 7 Mar | ✅ Returned |
| Physics (XI-A) | 38 | Ms. Lakshmi | 5 Mar | 10 Mar | ✅ Returned |
| Mathematics (IX-A) | 42 | Mr. Arjun | 4 Mar | 9 Mar | 🔄 In progress |

Return deadline tracking: evaluators who miss return deadline get an automated reminder via WhatsApp.

---

## 7. Student Script Photocopy Request

Per CBSE circular (2022), students or parents can request a photocopy of their evaluated answer script:

**Request log:**

| Student | Class | Subject | Request Date | Fee Paid | Status | Dispatch |
|---|---|---|---|---|---|---|
| Arjun Sharma | XI-A | Physics | 22 Mar | ₹200 (paid) | ✅ Dispatched | Handed to parent 24 Mar |
| Priya V | X-B | Mathematics | 23 Mar | ₹200 (paid) | ⏳ Preparing | — |

Process:
1. Parent submits written request + prescribed fee (₹200 per subject)
2. Exam Cell Head retrieves the evaluated script from storage
3. Photocopy made, self-attested by Exam Cell Head
4. Handed to parent/student (parent ID proof required)
5. Logged with date of request, date of dispatch, received-by name

---

## 8. Script Retention & Disposal

| Subject | Exam | Evaluation Complete | Retention Period | Disposal Date | Status |
|---|---|---|---|---|---|
| All subjects | Annual 2023–24 | Yes | 1 year | Apr 2025 | ✅ Disposed |
| All subjects | Annual 2024–25 | Yes | 1 year | Apr 2026 | ⏳ Pending disposal |
| All subjects | Annual 2025–26 | In progress | 1 year | Apr 2027 | — |

**Retention policy:** CBSE recommends 1 year; state boards vary (some require 3 years for X/XII). Principal can extend retention.

**Disposal log:** When scripts are disposed (shredded), the Exam Cell Head logs the disposal with count, date, method, and witness (usually another senior staff member).

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/scripts/` | Script management overview |
| 2 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/scripts/sessions/` | Session-wise register |
| 3 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/scripts/sessions/{session_id}/stationery/` | Log stationery issue |
| 4 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/scripts/sessions/{session_id}/collection/` | Log script collection |
| 5 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/scripts/distribute-evaluation/` | Assign scripts to evaluators |
| 6 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/scripts/{assignment_id}/return/` | Mark scripts as returned |
| 7 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/scripts/photocopy-requests/` | Photocopy request list |
| 8 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/scripts/photocopy-requests/` | Create photocopy request |
| 9 | `PATCH` | `/api/v1/school/{id}/exams/{exam_id}/scripts/photocopy-requests/{req_id}/` | Update photocopy status |

---

## 10. Business Rules

- Any shortfall in script count (issued vs collected) must be resolved before marks entry opens for that session — the system blocks marks entry until the discrepancy is resolved or Principal overrides with a written explanation
- Evaluated scripts cannot be given directly to students — only photocopies; original scripts are retained
- Photocopy requests must be fulfilled within 10 working days (CBSE norm)
- Script disposal must be witnessed and logged; bulk disposal (annual) is treated as an event in the Audit Log (A-34)
- Board exam answer scripts (CBSE, ISC) are evaluated and retained by the board — schools have no custody; they are excluded from this page

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
