# C-03 — Admission Test & Interview

> **URL:** `/school/admissions/tests/`
> **File:** `c-03-admission-test-interview.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Admission Officer (S3) — full · Academic Coordinator (S4) — full · Principal (S6) — full

---

## 1. Purpose

Manages the admission test and/or interview process for shortlisted applicants. CBSE regulations for Classes I–VIII prohibit formal entrance tests (per RTE Act 2009 — no screening for admission under age 14), but many schools conduct informal "interaction sessions" or "parent interaction" to assess readiness. For Classes IX and XI, formal written tests and interviews are standard practice. This page schedules test sessions, records marks, and generates the merit list that feeds into the seat allocation process (C-04).

**Class-wise test approach in CBSE schools:**
- **Nursery–Class II:** Parent-child interaction (no written test — RTE mandates this). School assesses conversational ability, age-appropriateness, and parent interview.
- **Classes III–VIII:** Many schools conduct informal "assessment" (they call it interaction, not test). Often 30-minute reading + arithmetic check. Not legally a test.
- **Class IX:** Written test — English, Maths, Science, Social Studies. 90 minutes. Marks matter.
- **Class XI:** Subject test based on stream applied (Science: PCM/PCB, Commerce: Maths/Accounts, Arts: English/chosen subjects) + personality interview. Competition is high for Science seats.

---

## 2. Page Layout

### 2.1 Header
```
Admission Test & Interview — 2026–27          [+ Schedule Session]  [Export Merit List]
Classes with Sessions Scheduled: 4
Total Candidates Scheduled: 142  ·  Appeared: 86  ·  Pending: 56
```

### 2.2 Session List
| Session | Class | Type | Date & Time | Venue | Candidates | Appeared | Status |
|---|---|---|---|---|---|---|---|
| ADT-2026-001 | Class I | Parent Interaction | 20 Mar 2026, 10AM | Hall B | 48 | 42 | ✅ Done |
| ADT-2026-002 | Class IX | Written Test | 22 Mar 2026, 9AM | Exam Hall | 56 | 52 | ✅ Done |
| ADT-2026-003 | Class XI-Science | Written Test + Interview | 28 Mar 2026, 9AM | Exam Hall | 38 | — | ⏳ Upcoming |
| ADT-2026-004 | Class XI-Commerce | Written Test | 29 Mar 2026, 10AM | Exam Hall | 24 | — | ⏳ Upcoming |

---

## 3. Schedule Test Session

[+ Schedule Session] → form:

| Field | Value |
|---|---|
| Session Name | ADT-2026-003 (auto) |
| Class | XI — Science stream |
| Type | Written Test · Parent Interaction · Interview · Written + Interview |
| Date | 28 Mar 2026 |
| Time | 9:00 AM – 12:00 PM |
| Venue | Examination Hall (select from room list) |
| Max Candidates per Session | 40 |
| Test Structure (if Written) | Subjects + marks per subject |
| Interview Panel (if Interview) | Staff members |
| Hall Ticket Required | Yes / No |
| Admit Criteria | Min 50% in Class X (for XI admissions) |

### 3.1 Written Test Structure

For written tests, define the paper:

| Subject | Max Marks | Duration |
|---|---|---|
| Physics | 50 | shared 2 hours |
| Chemistry | 50 | shared |
| Mathematics | 50 | shared |
| **Total** | **150** | **2 hours** |

---

## 4. Candidate List for a Session

Clicking a session row shows candidates:

```
ADT-2026-002 — Class IX Written Test — 22 Mar 2026

Form No.     Applicant          Mobile         Call Letter  Appeared  Test Score  Remarks
ADM/2026/012  Arjun Sharma      9876543210      ✅ Sent      ✅ Yes    138/200     —
ADM/2026/015  Priya Venkat      9876512345      ✅ Sent      ✅ Yes    164/200     —
ADM/2026/018  Rohit Kumar       8765432109      ✅ Sent      ✅ Yes    92/200      ⚠️ Low score
ADM/2026/022  Anjali Das        7654321098      ✅ Sent      ❌ Absent  —          Rescheduled
```

---

## 5. Call Letter Generation

[Send Call Letters] → generates and delivers:
- PDF call letter with: student name, session date/time, venue, instructions (what to bring — pencils, ruler, ID proof)
- Delivery: WhatsApp + Email
- Bulk: sends to all candidates in the session
- Manual: individual [Send] button per candidate

**Call letter content:**
```
ADMISSION TEST CALL LETTER
[School Logo and Name]

This is to inform that [Student Name], Application No. ADM/2026/012,
has been shortlisted for the Admission Test/Interaction for Class IX.

Date: 22 March 2026 (Sunday)
Time: 9:00 AM – 11:00 AM (Please arrive by 8:45 AM)
Venue: Examination Hall, [School Name], [Address]

Kindly bring:
- This call letter (printed or on mobile)
- Student's Aadhaar card
- Stationery (pencil, pen, eraser, scale)

No electronic devices allowed.
```

---

## 6. Marks Entry

After the test, Admission Officer or Academic Coordinator enters marks:

### Grid View
```
ADT-2026-002 — Marks Entry

Roll  Applicant        English  Maths  Science  Soc.Sci  Total  %
001   Arjun Sharma       42      38      32       26      138   69%
002   Priya Venkat       44      42      40       38      164   82%
003   Rohit Kumar        28      24      22       18       92   46%
004   Anjali Das         AB      AB      AB       AB      ABSENT
```

Tab key navigates between cells. Absent marked as "AB" → stored as NULL (not 0).

### Interview Scoring (if applicable)

| Criteria | Max | Arjun | Priya |
|---|---|---|---|
| Communication | 10 | 8 | 9 |
| Subject Awareness | 10 | 7 | 9 |
| General Knowledge | 5 | 4 | 5 |
| Confidence | 5 | 4 | 5 |
| **Total** | **30** | **23** | **28** |

---

## 7. Merit List Generation

After marks entry is complete:

[Generate Merit List] →

```
MERIT LIST — Class IX Admissions 2026–27
[School Name]

Rank  Form No.    Applicant       Written  Interview  Total   %      Category  Decision
1     ADM/2026/15  Priya Venkat   164      28         192     87.3%  General   ✅ Selected
2     ADM/2026/12  Arjun Sharma   138      23         161     73.2%  OBC-NCL   ✅ Selected
3     ADM/2026/24  Meera S.       148      —          148     74.0%  SC        ✅ Selected (quota)
...
22    ADM/2026/18  Rohit Kumar     92      12         104     47.3%  General   ❌ Not Selected
```

Merit list takes into account:
- Overall rank
- Category reservations (SC/ST/OBC-NCL as per school policy)
- Sibling priority (if school has sibling priority policy)
- RTE quota candidates are NOT on this list — they go through C-07

[Publish Merit List] → Available in parent-facing portal if configured.

---

## 8. Absent Candidate Handling

Candidates who were absent can be:
- **Rescheduled:** Added to a future session (if seats available)
- **No-show:** Marked absent; application moved to Withdrawn stage in C-01

---

## 9. Parent Interaction Record (Nursery–Class II)

For classes where written tests are legally not permitted, the parent interaction is documented qualitatively:

```
Parent Interaction Record
Student: Aditya Ravi   |  Class: Nursery (2026–27)  |  Date: 15 Mar 2026
Parent(s) Present: Mr. Ravi Kumar (Father), Mrs. Sunita Ravi (Mother)

Child Assessment:
  Language Response:    Good — responds to English and Telugu
  Motor Skills:         Age appropriate
  Social Interaction:   Comfortable with teacher
  Overall Readiness:    ✅ Ready for Nursery

Parent Interview:
  Expectations:         Academic + extracurricular balance
  Previous Exposure:    Playschool (1 year — Kidzee)
  Concerns:             Transport from Kondapur

Panel Notes: "Child is confident and communicative. Parents appear supportive and engaged.
              Recommend for admission."

Panel Members: Ms. Kavitha (Principal), Ms. Lakshmi (Nursery Coordinator)
Decision: ✅ Recommended for Admission
```

This is stored as a qualitative record — no numeric score.

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/admissions/test-sessions/?year={year}` | Session list |
| 2 | `POST` | `/api/v1/school/{id}/admissions/test-sessions/` | Schedule new session |
| 3 | `GET` | `/api/v1/school/{id}/admissions/test-sessions/{session_id}/` | Session detail + candidate list |
| 4 | `POST` | `/api/v1/school/{id}/admissions/test-sessions/{session_id}/call-letters/` | Generate + send call letters |
| 5 | `PATCH` | `/api/v1/school/{id}/admissions/test-sessions/{session_id}/marks/` | Enter/update marks |
| 6 | `GET` | `/api/v1/school/{id}/admissions/test-sessions/{session_id}/merit-list/` | Generate merit list |
| 7 | `POST` | `/api/v1/school/{id}/admissions/test-sessions/{session_id}/merit-list/publish/` | Publish merit list |
| 8 | `PATCH` | `/api/v1/school/{id}/admissions/test-sessions/{session_id}/interaction/{candidate_id}/` | Save parent interaction record |

---

## 11. Business Rules

- For Classes I–VIII, the system labels the event as "Parent Interaction" or "Assessment Session" rather than "Entrance Test" — in compliance with RTE Act which prohibits formal screening for admission
- Written test marks alone cannot be the basis for rejection in Classes I–VIII — the system enforces this by flagging if a school tries to set a "minimum marks cutoff" for these classes
- Merit list must consider category reservations if the school has declared a reservation policy; the system computes category-wise ranks automatically
- A candidate cannot appear more than once for the same class in the same admission year without Admission Officer override
- Interview scores can be optionally weighted against written marks; the weighting formula is school-configurable

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
