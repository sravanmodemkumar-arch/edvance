# G-04 — Member Management

> **URL:** `/school/library/members/`
> **File:** `g-04-member-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Librarian (S3) — full · Library Assistant (S2) — view + update · Academic Coordinator (S4) — policy settings · Administrative Officer (S3) — bulk enroll new class

---

## 1. Purpose

Manages library membership — every student and staff member of the school is a library member. Auto-enrolled on admission (C-05) or staff onboarding (L-01); deactivated on withdrawal (C-12) or staff exit (L-12). Tracks borrowing history, limits, and membership status.

---

## 2. Page Layout

### 2.1 Header
```
Library Members                                      [+ Enroll New Member]  [Bulk Enroll Class]
Total Members: 452  ·  Active: 448  ·  Inactive (withdrawn/left): 4
Students: 380  ·  Staff: 72
```

### 2.2 Member List
```
Filter: [Students ▼]  Class: [All ▼]  Status: [Active ▼]

Member Card  Name              Class  Books Out  Fine Due  Last Visit  Status
M-0001187    Arjun Sharma      XI-A   1          ₹0        27 Mar 26   ✅ Active
M-0001188    Anjali Das        XI-A   0          ₹0        22 Mar 26   ✅ Active
M-0001190    Chandana Rao      XI-A   0          ₹12       15 Mar 26   ⚠️ Fine due
M-0001205    Vijay S.          X-B    2          ₹45       10 Mar 26   🔴 Overdue
```

---

## 3. Member Profile

```
Member Profile — Arjun Sharma

Member ID: M-0001187  ·  Student ID: STU-0001187
Member Type: Student  ·  Class: XI-A  ·  Roll: 02
Enrolled: 15 Jun 2023  ·  Member Status: ✅ Active
Library Card: [View / Print]  (G-14)

Borrowing Profile:
  Limit: 2 books at a time
  Currently issued: 1 (Atomic Habits — due 10 Apr 2026)
  Total issues this year: 14  ·  Total all time: 38
  Overdue incidents this year: 1  ·  Fines paid all time: ₹8
  Outstanding fine: ₹0

Reading preference (inferred from issue history):
  Fiction: 12 issues  ·  Science: 10 issues  ·  General: 16 issues
  Favourite authors: Paulo Coelho (3×), A.P.J. Abdul Kalam (2×)

[View Issue History]  [View Fine History]  [Suspend Member]  [Print Library Card]
```

---

## 4. Borrowing Limits Configuration

```
Member Type        Borrowing Limit    Loan Period    Max Renewals
Student (I–V)       1 book              7 days           1
Student (VI–VIII)   2 books            14 days           1
Student (IX–XII)    2 books            14 days           2
Teaching Staff      5 books            30 days           3
Non-Teaching Staff  2 books            14 days           1
Principal           10 books           60 days           unlimited
Visiting Teacher    2 books            14 days           0

[Edit Configuration]  (Academic Coordinator approval required)
```

---

## 5. Auto-Enrollment & Deactivation

```
Auto-enrollment rules (from C-05):
  → When a student is enrolled (C-05 New Student Enrollment) → Library member auto-created
  → Member ID = Student ID prefix (M-XXXXXXX)
  → Default borrowing limit set by class level
  → Library card auto-generated (G-14)

Auto-deactivation rules:
  → Student withdrawal (C-12) → Library member status = Inactive
     Block: Cannot issue new books after withdrawal date
     But: Must still return pending books + pay fines (TC gate, C-13)
  → Staff exit (L-12 offboarding) → Library member deactivated
     All books must be returned at exit clearance
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/members/?type={student|staff}&status={active}` | Member list |
| 2 | `POST` | `/api/v1/school/{id}/library/members/` | Create member manually |
| 3 | `GET` | `/api/v1/school/{id}/library/members/{member_id}/` | Member profile |
| 4 | `PATCH` | `/api/v1/school/{id}/library/members/{member_id}/` | Update member |
| 5 | `POST` | `/api/v1/school/{id}/library/members/{member_id}/suspend/` | Suspend member |
| 6 | `GET` | `/api/v1/school/{id}/library/members/{member_id}/issue-history/` | Borrowing history |
| 7 | `GET` | `/api/v1/school/{id}/library/members/config/` | Borrowing limits config |
| 8 | `PATCH` | `/api/v1/school/{id}/library/members/config/` | Update limits (Coord approval) |

---

## 7. Business Rules

- Library member accounts are never deleted (preserves borrowing history for dispute resolution); deactivated members cannot borrow but their history is retained
- The Member ID (M-XXXXXXX) is derived from the Student ID and is permanent; even if a student transfers sections or classes, the same member ID persists
- Overdue alerts: if a member has a book overdue by more than 7 days, the system sends a WhatsApp reminder (via F-03 auto-trigger) once per week
- For CWSN students (C-19), loan period may be extended by the Librarian on a case-by-case basis (disability accommodation)
- Staff members are enrolled by the Librarian when L-01 staff onboarding is complete; their borrowing limit is higher and not counted against their salary deductions (different from student fines)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
