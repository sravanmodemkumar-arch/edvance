# F-09 — Student Diary / Planner Messages

> **URL:** `/school/diary-messages/`
> **File:** `f-09-diary-messages.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Class Teacher (S3) — assign homework/messages for own class · Subject Teacher (S3) — homework for own subject · Administrative Officer (S3) — school diary notices · Parent — view diary messages and sign off via parent portal

---

## 1. Purpose

The physical school diary (student planner) is a deeply embedded institution in Indian schooling — it's the channel through which teachers send homework assignments, school notices, and parent communication for acknowledgement. EduForge digitises this:
- **Homework assignment** by teachers posted to the diary daily
- **School notices** typed in diary for parent reading and signature
- **Parent signature tracking** (parent signs the diary daily — digital acknowledgement replaces physical signature in the parent portal)
- **Long-term planner** view for students (what's due this week, upcoming exams)

This is especially important for primary classes (Nursery to Class V) where parents monitor the diary daily, and for boarding schools where diary is the teacher-parent bridge.

---

## 2. Page Layout

### 2.1 Teacher View
```
Diary Messages — Class XI-A                      [+ Homework Assignment]  [+ Class Notice]
Today: 27 March 2026 (Friday)

Subject   Assignment                            Due Date   Signed By Parents (45)  Status
Physics   Chapter 12 — Numericals 1-10          30 Mar     38/45 (84%)             ✅ Sent
Chemistry Lab report — Titration experiment     28 Mar     41/45 (91%)             ✅ Sent
Maths     Exercise 8.3 — Q1 to Q15             31 Mar     35/45 (78%)             ✅ Sent

Notice: Exam schedule PDF shared (CIR/2026/049)  27 Mar    42/45 (93%)            ✅ Signed
```

### 2.2 Student / Parent Portal View
```
Diary — Arjun Sharma (XI-A)
Week of 27 March 2026

FRIDAY 27 Mar
  📚 Physics: Numericals 1-10 (Ch. 12) — due Monday
  📚 Chemistry: Lab report (Titration) — due Saturday
  📚 Maths: Exercise 8.3 Q1-Q15 — due Tuesday

  📋 Notice: Annual Exam Schedule attached [View PDF]

  Parent acknowledgement: ☑ Signed (Father — 27 Mar, 7:45 PM)

THURSDAY 26 Mar
  📚 English: Essay draft — due Friday ✅ Completed
  📚 Physics: Chapter 11 revision

  Parent acknowledgement: ☑ Signed (Father — 26 Mar, 8:12 PM)

[Previous week]  [Next week ▼]  [View Full Year Planner]
```

---

## 3. Homework Assignment

```
[+ Homework Assignment] → drawer:

Subject: [Physics ▼]  (only own subjects for Subject Teacher)
Class: XI-A  (auto-set; can add multiple classes if shared assignment)
Date: [27 March 2026]  (today — diary date)
Due Date: [30 March 2026]

Assignment:
  Type: ● Written  ○ Reading  ○ Project  ○ Practical  ○ Online (link)
  Description:
    [Chapter 12 — Numericals 1 to 10. Show all steps clearly.]

Attachments: [+ Add PDF / Image] (reference material, worksheet)
  Attached: ch12_numericals.pdf (210 KB)

Parent signature required: ☑ Yes (acknowledgement that parent saw this)

Notify via:
  ☑ Parent app/portal notification
  ☑ WhatsApp (if school has WhatsApp integration enabled for diary)
  ☐ SMS

[Save & Send]
```

---

## 4. Class Notice via Diary

```
[+ Class Notice]

Notice type: ○ School circular  ● Class-specific notice  ○ Reminder
Message:
  "Dear Parent, kindly note that Physics Unit Test will be held on
   2 April 2026. Chapters 10-12 are in syllabus. Please ensure your
   ward revises thoroughly. — Ms. Anita, Class Teacher"

Parent action required: ☑ Sign (acknowledge) by: 29 March 2026
Attach document: [Attach unit test syllabus]

[Send to Class XI-A parents]
```

---

## 5. Unsigned Diary Alert

```
Unsigned Diary Alert — 27 March 2026 — Class XI-A

Parents who have NOT signed today's diary (7 students as of 9 PM):

  Roll 03 — Chandana Rao — Parent not signed (3rd consecutive day)
  Roll 08 — Vijay S. — Parent not signed (today only)
  ...

Auto-reminder sent at 7 PM to unsigned parents: ✅ Sent (WhatsApp)

Chandana Rao — 3 days unsigned:
  → Escalate to Class Teacher for phone call
  → Note in F-13 communication log

[Send Reminder Again]  [Call Log (Chandana's parent)]
```

---

## 6. Long-Term Planner

```
Student Planner — Arjun Sharma — April 2026

Week      Mon        Tue        Wed        Thu        Fri
Mar 30    Physics    Chemistry  Maths      English    Phy.Edu
          Numerals   Lab Rpt due Exer. 8.3             —
           due       ↑ submit

Apr 6     Holiday   Exam begins  Physics   Chemistry  Maths
          (Ram Nav)  (1 Apr)     Exam       Exam       Exam
                     10-12 AM

Upcoming:
  1 Apr 2026  — Annual Exam begins
  30 Apr 2026 — Last exam
  1 May 2026  — Summer vacation starts
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/diary/?class_id={id}&date={date}` | Diary entries for class/date |
| 2 | `POST` | `/api/v1/school/{id}/diary/homework/` | Create homework assignment |
| 3 | `POST` | `/api/v1/school/{id}/diary/notice/` | Create class diary notice |
| 4 | `POST` | `/api/v1/school/{id}/diary/{entry_id}/acknowledge/` | Parent acknowledge |
| 5 | `GET` | `/api/v1/school/{id}/diary/student/{student_id}/?from={date}&to={date}` | Student diary view |
| 6 | `GET` | `/api/v1/school/{id}/diary/unsigned/?class_id={id}&date={date}` | Unsigned diary report |
| 7 | `GET` | `/api/v1/school/{id}/diary/planner/{student_id}/?month={m}&year={y}` | Month planner view |

---

## 8. Business Rules

- Homework entries are date-stamped and immutable after 24 hours; corrections become a new entry with a note referencing the original
- Parent acknowledgement is tracked per day; a student with 5+ consecutive unsigned diary days triggers an alert to the Class Teacher
- The diary is visible to the parent only for their own child — a parent with 3 children (C-20 family linkage) sees all 3 children's diaries from a single login but cannot see other families' entries
- For primary classes (Nursery–Class V), parent signature is mandatory (school policy); for secondary classes, it is best practice but configurable
- Homework analytics (how many assignments per week, subject-wise load) are available in the Communication Analytics dashboard (F-16) to help coordinators monitor teacher workload consistency

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
