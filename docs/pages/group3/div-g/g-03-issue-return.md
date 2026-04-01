# G-03 — Issue & Return

> **URL:** `/school/library/issue-return/`
> **File:** `g-03-issue-return.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Librarian (S3) — full · Library Assistant (S2) — issue/return (supervised) · Class Teacher (S3) — class-level issue (for class library sets)

---

## 1. Purpose

The primary daily transaction screen for issuing books to members and receiving returned books. P0 because this is the core library operation — happens multiple times every school day. Design requirements:
- **Speed:** A library counter must process one transaction in under 10 seconds (scan + confirm)
- **Barcode-first workflow:** Scan member card, then scan book barcode — two scans and done
- **Standing fine alert:** If a member has outstanding fines, alert before issue (some libraries block issue until fine is cleared)
- **Limit enforcement:** Each member has a borrowing limit (e.g., 2 books at a time for students, 5 for staff)
- **Due date auto-set:** Based on library policy (typically 14 days for students)
- **Class sets:** For class library visits (G-10), a class of 40 students can each issue 1 book in a batch operation

---

## 2. Page Layout

### 2.1 Issue Counter
```
Issue / Return                                       [Batch Issue (Class Visit)]  [Manual Entry]
Mode: ● Issue  ○ Return

Scan Member Card: [________________] ← tap/scan
  OR  Search: [Student name / Admission No.]

─────────────────────────────────────────────────────────────────────────
Scanned: Arjun Sharma (STU-0001187) — Class XI-A — Member since: Jun 2023

Member Status: ✅ Active  ·  Books currently issued: 1/2 (limit: 2)
Outstanding fine: ₹0  ·  Eligible to borrow: ✅ Yes (1 more book allowed)

Currently issued:
  LIB2023046 — The Alchemist (Paulo Coelho) — Due: 30 Mar 2026 (3 days left)

Now scan book barcode: [________________]
─────────────────────────────────────────────────────────────────────────

Scanned book: LIB2026001 — Atomic Habits (James Clear) — Available ✅

Issue confirmation:
  Member: Arjun Sharma (XI-A)
  Book: Atomic Habits — Copy 1 (Barcode: LIB2026001)
  Issue Date: 27 March 2026
  Due Date: 10 April 2026 (14 days)
  [Confirm Issue ✓]  [Cancel]
```

After confirmation:
```
✅ Book Issued

Arjun Sharma — Atomic Habits (LIB2026001)
Due: 10 April 2026

Receipt: [Print Slip]  [WhatsApp to parent: "Book issued: Atomic Habits. Due 10 Apr"]

[Next Transaction]
```

---

## 3. Return Workflow

```
Mode: ○ Issue  ● Return

Scan Book Barcode: LIB2026001

Book: Atomic Habits — Copy 1
Issued to: Arjun Sharma (XI-A) on 27 Mar 2026
Due: 10 Apr 2026

Today: 9 Apr 2026 — Returned on time ✅

Condition check:
  ● Good  ○ Minor damage  ○ Major damage  ○ Lost (report)

[Confirm Return]
```

Return with overdue:

```
Book: The Alchemist — Copy 2 (LIB2023046)
Issued to: Suresh Kumar (IX-A) on 1 Mar 2026
Due: 15 Mar 2026
Today: 27 Mar 2026

⚠️ OVERDUE by 12 days

Fine calculation (as per G-06 policy — ₹1/day):
  12 days × ₹1 = ₹12 overdue fine

Options:
  ● Collect fine now (cash)  ○ Add to fee ledger (D-07)  ○ Waive (Librarian approval)

[Confirm Return + Fine: ₹12]  [Waive Fine]
```

---

## 4. Member Block on Issue Attempt

```
Scanned: Meena Devi (XI-A, STU-0001245)

Member Status: 🔴 BLOCKED — Cannot issue books

Reason(s):
  ● Outstanding fine: ₹45 (3 books overdue)
  ● Already at borrowing limit: 2/2 books issued, both overdue

Action required:
  → Student must return overdue books + pay fine before new issue
  [View overdue details]  [Accept fine payment + unblock]
```

---

## 5. Batch Issue (Class Library Visit)

For G-10 class library periods:

```
[Batch Issue — Class Visit]

Class: [XI-A ▼]  ·  Date: 27 Mar 2026  ·  Librarian: Ms. Kavitha

Mode: ● Each student picks own book (scan each student + book pair)
      ○ Teacher assigns books (bulk assign from class list)

Sequential scan:
  Scan student card → scan book barcode → auto-proceed to next

Status:
  Issued: 32/45 students  ·  Not collected: 13 (absent or didn't pick)
  Time: 12 minutes elapsed

[Complete Batch]  [View Batch Summary]
```

---

## 6. Renewal

```
Book Renewal — Arjun Sharma — The Alchemist

Current due date: 10 Apr 2026 (not yet overdue)
Max renewals allowed: 1 (per policy)
Renewals used: 0

New due date after renewal: 24 Apr 2026 (14 more days)

Condition: No reservation for this copy → Renewal allowed ✅

[Confirm Renewal]

If renewal denied (book is reserved by another member):
  "This copy is reserved by Priya Venkat (XI-A). Renewal not permitted.
   Please return by 10 Apr 2026 or ask Priya to use a different copy."
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/school/{id}/library/issue/` | Issue book |
| 2 | `POST` | `/api/v1/school/{id}/library/return/` | Return book |
| 3 | `POST` | `/api/v1/school/{id}/library/renew/` | Renew book |
| 4 | `POST` | `/api/v1/school/{id}/library/issue/batch/` | Batch issue (class visit) |
| 5 | `GET` | `/api/v1/school/{id}/library/member/{member_id}/current-issues/` | Member's current issues |
| 6 | `GET` | `/api/v1/school/{id}/library/issue-history/?member_id={id}&from={date}&to={date}` | Issue history |

---

## 8. Business Rules

- Borrowing limit is configurable per member type: Students (default 2), Staff (5), Class Teachers for classroom sets (20)
- Overdue fine is configured in G-06; default ₹1/day; fine applies from the day after due date
- A student with an outstanding fine is warned but NOT blocked by default (configurable — some schools block, others don't); for blocking, the Principal must enable the setting
- Reference section books (Section = Reference in G-01) cannot be issued — the system raises a hard error: "This is a reference book and cannot be issued"
- Renewal is allowed if: book is not reserved by another member AND max renewals not exceeded AND book is not overdue (must renew before due date)
- TC issuance (C-13) is blocked if any books are currently issued or any fine is outstanding — library clearance is required for TC

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
