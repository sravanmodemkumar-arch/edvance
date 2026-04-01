# G-11 — Reading Programme

> **URL:** `/school/library/reading-programme/`
> **File:** `g-11-reading-programme.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Librarian (S3) — manage programme · Class Teacher (S3) — assign reading and log completion · Academic Coordinator (S4) — set targets · Principal (S6) — approve programme design

---

## 1. Purpose

Manages structured reading programmes aligned with CBSE's "Reading for Joy" initiative and NEP 2020's emphasis on reading culture. Goes beyond issue/return tracking to focus on reading engagement:
- **Reading targets:** Each class has a monthly/annual reading target (e.g., Class I students should read 2 books/month)
- **Book lists:** Recommended reading lists curated per class level (CBSE recommended + school supplementary)
- **Reading logs:** Students record books read (with brief review/summary) — develops comprehension and articulation
- **Reading certificates:** Students who meet annual targets receive a reading achievement certificate
- **Summer reading challenge:** Many schools run summer reading programmes

---

## 2. Page Layout

### 2.1 Header
```
Reading Programme                                    [Set Targets]  [Issue Certificates]
Academic Year: [2026–27 ▼]

Programme: CBSE Reading for Joy (2026–27)
Overall progress: 68% of students on track to meet annual reading target
Top readers this month: 5 students (10+ books)
```

### 2.2 Class Progress
```
Class   Teacher       Target/Year  Avg Books Read  On Track  Behind
Nurs-A  Ms. Kavya     12 books     10.2 books      88%       12%
I-A     Ms. Radha     15 books      8.4 books      65%       35%   ⚠️
VI-A    Mr. Kishore   10 books      7.1 books      72%       28%
XI-A    Ms. Anita      8 books      6.8 books      85%       15%
XII-A   Ms. Lakshmi    6 books      5.2 books      87%       13%
```

---

## 3. Student Reading Log

```
Reading Log — Arjun Sharma (XI-A)

Annual target: 8 books  ·  Read this year: 7 books  ·  Status: On track ✅

Books read this year:
  1. Wings of Fire — A.P.J. Abdul Kalam
     Completed: 20 Apr 2026  ·  Review: "Inspiring biography about persistence and science."
     Rating: ★★★★★

  2. The Alchemist — Paulo Coelho
     Completed: 15 Jun 2026  ·  Review: "Philosophical but easy to read."
     Rating: ★★★★☆

  3. Atomic Habits — James Clear
     Currently reading  ·  Started: 27 Mar 2026  ·  (In progress)

[Add Book to Log]
```

---

## 4. Recommended Reading Lists

```
CBSE Recommended Reading List — Class XI

Category        Title                        Author
Fiction         The Kite Runner              Khaled Hosseini
Fiction         A Suitable Boy               Vikram Seth
Non-fiction     I am Malala                  Malala Yousafzai
Biography       Wings of Fire                A.P.J. Abdul Kalam
Science         A Brief History of Time      Stephen Hawking
Classics        Pride and Prejudice          Jane Austen
Indian Heritage  Discovery of India          Jawaharlal Nehru
Environmental   Silent Spring                Rachel Carson

School Supplementary List (added by Academic Coordinator):
  Atomic Habits — James Clear  (Personal development for Class XI-XII)
  Sapiens — Yuval Harari       (History, broad perspective)

[Edit Lists]  [Import CBSE 2026-27 Recommended List]
```

---

## 5. Reading Certificate

```
[Issue Certificates]

Students who met annual reading target (8 books for Class XI):

  Eligible: 38/45 students in Class XI-A
  Certificate template: CBSE Reading for Joy Certificate

Certificate text:
  "This is to certify that ARJUN SHARMA, Class XI-A, has successfully
   completed the annual reading programme by reading [N] books during
   the academic year 2026-27.

   Awarded in recognition of the joy of reading."

  [Principal Signature]  [Library Seal]  [Date]

[Print All Certificates]  [Send digital certificates via parent portal]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/reading-programme/?year={y}` | Programme overview |
| 2 | `GET` | `/api/v1/school/{id}/library/reading-programme/student/{student_id}/` | Student reading log |
| 3 | `POST` | `/api/v1/school/{id}/library/reading-programme/log/` | Add book to student log |
| 4 | `GET` | `/api/v1/school/{id}/library/reading-programme/recommended-lists/?class={level}` | Recommended book lists |
| 5 | `GET` | `/api/v1/school/{id}/library/reading-programme/certificates/` | Certificate eligible students |
| 6 | `GET` | `/api/v1/school/{id}/library/reading-programme/certificates/pdf/?class={id}` | Bulk certificate PDF |

---

## 7. Business Rules

- Reading logs are student-maintained (with teacher review for lower classes) — the system tracks when a log entry was made, but does not verify reading independently; the teacher/librarian may ask for a brief review/summary before confirming the log
- Annual reading targets are set per class level by the Academic Coordinator; CBSE provides a recommended minimum (e.g., Class I: 12 books, Class XII: 6 books) but schools may set higher
- Reading certificates are separate from academic result certificates (C-14 bonafide); they are generated here and issued via G-14 or as a digital certificate via the parent portal
- Books read as part of the regular syllabus (NCERT textbooks) are not counted toward the reading programme target — only supplementary/leisure reading qualifies
- The reading log data feeds into F-16 Communication Analytics for the "parent engagement with digital learning" metric

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
