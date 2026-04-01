# N-05 — School Diary & Messages (Parent View)

> **URL:** `/parent/diary/`
> **File:** `n-05-diary-communication.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P)

---

## 1. Purpose

The school diary is the primary communication channel between teachers and parents. Traditionally a physical notebook carried by the student, EduForge's digital diary covers:
- Homework assignments and due dates
- Class Teacher messages (announcements, reminders)
- Subject teacher messages (project deadlines, test schedules)
- Principal/VP messages (school-wide communications)
- Parent-to-teacher replies (limited — parents can reply to Class Teacher only)

The diary is the async communication backbone; for urgent communication, WhatsApp/SMS is used (I-10 template mechanism); for formal escalations, the grievance system (N-10) is used.

---

## 2. Diary Inbox — Parent View

```
SCHOOL DIARY — Rahul Rao (Class X-A)
27 March 2026 | Inbox

  ──────────────────────────────────────────────────────────────────────────
  📚 HOMEWORK — Maths — Mr. Deepak C.              27 Mar 2026  NEW
     "Complete Exercise 12.3 (Q1–Q8) by Monday, 30 March.
      Refer to NCERT examples 12.4 and 12.5 before attempting."
     Due: 30 March 2026 (Monday)  |  Subject: Mathematics
  ──────────────────────────────────────────────────────────────────────────
  📋 CLASS TEACHER — Mr. Deepak C.                  25 Mar 2026
     "Dear Parents, Unit Test 1 report cards have been released on the portal.
      Please review and sign the acknowledgement by 28 March.
      For any queries, meet me during the upcoming PTM on 6 April."
     [Acknowledge →]  |  Status: Unacknowledged ⚠ (due 28 Mar)
  ──────────────────────────────────────────────────────────────────────────
  📢 PRINCIPAL — Ms. Meena Rao                      22 Mar 2026
     "Annual Day rehearsals begin Saturday, 5 April, 2–4 PM.
      All students should report to the school hall. Uniform mandatory.
      Refreshments provided."
  ──────────────────────────────────────────────────────────────────────────
  📚 HOMEWORK — Science — Mr. Ravi K.               20 Mar 2026
     "Science project on 'Renewable Energy' — submit by 3 April.
      Format: A4 chart (min 6 points). Can work in pairs."
     Due: 3 April 2026  |  Status: Submitted ✅ (teacher marked)
  ──────────────────────────────────────────────────────────────────────────

[View all diary messages →]  [Search by subject / teacher / date]
```

---

## 3. Message Types and Permissions

```
DIARY MESSAGE TYPES:

Homework (Subject Teacher → Parent):
  Teacher enters homework with due date and subject
  Parent sees it in diary inbox + push notification
  Parent can mark "seen" (optional acknowledgement)
  Parent CANNOT reply directly to subject teachers (reply goes to CT queue)

Class Teacher Message (CT → All section parents):
  Announcements, reminders, individual notes
  Parent can REPLY to Class Teacher (limited to 200 characters)
  CT reply visible in diary; not a full messaging system

School-Wide Message (Principal/VP → All parents):
  Read-only for parents; acknowledgement optional
  Sent via both diary AND WhatsApp push

Test Schedule (Academic Coordinator → All parents of a class):
  Formatted test schedule with dates, subjects, chapters
  [See F-09 integration]

PARENT-INITIATED MESSAGES:
  Parent can message CLASS TEACHER only (not subject teachers directly)
  Subject: Text only (max 300 characters)
  Purpose: Quick questions ("Rahul was absent yesterday due to fever — please excuse")
  Formal complaints and escalations → N-10 grievance

  Not allowed:
    ✗ Parent cannot message VP or Principal directly via diary
       (They can request a meeting → PTM booking N-07 or front office phone)
    ✗ Parent cannot message other parents via diary
```

---

## 4. Homework Tracker

```
HOMEWORK TRACKER — Rahul Rao

  Subject    Assigned    Due       Description                    Status
  Maths      27 Mar      30 Mar    Ex 12.3 Q1–Q8                 Pending
  Science    20 Mar      3 Apr     Renewable Energy project       Submitted ✅
  English    18 Mar      21 Mar    Essay: "My Ideal India"        Submitted ✅
  Social Sci 15 Mar      18 Mar    Map work Ch 6                  Submitted ✅
  Hindi      14 Mar      17 Mar    Grammar exercise p. 84–85      Submitted ✅

PENDING THIS WEEK: 1 homework (Maths — due Monday)

[Filter: Pending / All / This week / This month]
```

---

## 5. Acknowledgement Tracking

```
DIARY ACKNOWLEDGEMENTS — Required from Parents

  Date      Message                          Deadline   Status
  25 Mar    "UT-1 report card reviewed"      28 Mar     ⚠ Pending
  15 Feb    "Half-yearly revision schedule"  20 Feb     ✅ Acknowledged (18 Feb)
  10 Jan    "Board exam admit card process"  15 Jan     ✅ Acknowledged (12 Jan)

Pending acknowledgements are highlighted in the inbox.
Class Teacher receives a list of parents who have not acknowledged.
(This replaces the physical diary "parent signature" verification.)
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/diary/` | Diary inbox (paginated) |
| 2 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/diary/homework/` | Homework list with status |
| 3 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/diary/{msg_id}/acknowledge/` | Acknowledge message |
| 4 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/diary/message/` | Send message to Class Teacher |
| 5 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/diary/pending-ack/` | Unacknowledged messages |

---

## 7. Business Rules

- Parents can only initiate messages to their child's Class Teacher — not to subject teachers, VP, or Principal directly through the diary; this is by design to maintain appropriate communication hierarchy and prevent teachers from being overwhelmed by direct parent messages outside professional boundaries
- Homework entries by teachers are date-stamped and immutable once created; a teacher can add a follow-up entry but cannot delete a homework entry (audit trail for "teacher gave too much homework" complaints)
- Parent message to Class Teacher is limited to 300 characters — this enforces brevity and discourages the diary being used for lengthy complaints or disputes (which belong in N-10 grievance); it is a communication tool, not a complaint channel
- Acknowledgement (parent signature equivalent) is tracked by CT for parents who have not confirmed receipt of important notices; repeated non-acknowledgement is not penalised but is noted in the CT's student communication log
- All diary communications are stored for 3 years (standard school communication retention); DPDPA: parent messages to school are school records; students' homework entries are deleted after the academic year closes (July of following year)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
