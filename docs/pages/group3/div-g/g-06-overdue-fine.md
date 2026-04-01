# G-06 — Overdue & Fine Management

> **URL:** `/school/library/overdue/`
> **File:** `g-06-overdue-fine.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Librarian (S3) — manage · Library Assistant (S2) — view · Academic Coordinator (S4) — fine waiver · Principal (S6) — policy changes

---

## 1. Purpose

Tracks overdue books and manages fine computation, collection, and waiver. Fine policies encourage timely returns and fund library operations.

---

## 2. Page Layout

### 2.1 Header
```
Overdue Books & Fines                                [Send Overdue Reminders]  [Export]
Today: 27 March 2026

Overdue Books: 28  ·  Members with overdue: 18
Total fines outstanding: ₹1,240
Fine collections this month: ₹480
```

### 2.2 Overdue List
```
Member       Class  Book                  Issued    Due       Days OD  Fine   Action
Vijay S.     X-B    Atomic Habits         1 Mar 26  15 Mar 26  12 days  ₹12   [Remind] [Waive]
Meena D.     XII-A  Wings of Fire         10 Feb 26 24 Feb 26  31 days  ₹31   [Remind] [Escalate]
Suresh K.    IX-A   The Alchemist (×2)    5 Feb 26  19 Feb 26  36 days  ₹72   [Remind] [Block]
```

---

## 3. Fine Policy Configuration

```
Fine Policy (configured by Academic Coordinator):

  Fine rate:           ₹1.00 per book per day overdue
  Grace period:        0 days (fine starts from day after due date)
  Maximum fine:        ₹50 per book (cap — beyond this, book is considered lost)
  Fine for lost book:  Replacement cost (from G-07)

Fine collection methods:
  ☑ At library counter (cash) — Librarian receives and issues receipt
  ☑ Add to student fee ledger (D-07) — collected at D-04 fee counter
  ○ Online payment via parent portal

Block on issue: ☑ Block new issue if outstanding fine > ₹50 (configurable threshold)

[Edit Fine Policy] — Academic Coordinator approval required
```

---

## 4. Overdue Reminder Workflow

```
[Send Overdue Reminders]

Recipients: 18 members with overdue books
Message (WhatsApp T-Overdue):
  "Dear Parent, [Name]'s library book '[Title]' was due on [Date].
   It is now [N] days overdue. A fine of ₹[amount] has accrued.
   Please return the book at the earliest. — School Library"

Escalation levels:
  1-7 days overdue: Auto-WhatsApp reminder (weekly)
  8-30 days: Librarian flags to Class Teacher for in-person follow-up
  30+ days: Escalate to Academic Coordinator; fine = replacement cost (treat as lost)
  At TC issuance: TC blocked until cleared (C-13 gate)
```

---

## 5. Fine Receipt & Waiver

```
Fine Collection — Vijay S. (X-B) — ₹12

Fine breakdown: Atomic Habits — 12 days × ₹1 = ₹12
Collection: Cash ₹12

[Issue Fine Receipt] → Library Fine Receipt LFR/2026/084
                      → Auto-linked to D-07 fee ledger (credit entry)

Waiver (if applicable):
  Reason: ○ Medical  ○ Hardship  ● Error in due date  ○ Other
  Approved by: [Librarian] (< ₹20 waiver) / [Academic Coordinator] (≥ ₹20)
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/overdue/?days={min}` | Overdue list |
| 2 | `GET` | `/api/v1/school/{id}/library/overdue/{member_id}/` | Member overdue detail |
| 3 | `POST` | `/api/v1/school/{id}/library/fines/collect/` | Collect fine payment |
| 4 | `POST` | `/api/v1/school/{id}/library/fines/{issue_id}/waive/` | Waive fine |
| 5 | `POST` | `/api/v1/school/{id}/library/overdue/send-reminders/` | Bulk WhatsApp reminders |
| 6 | `GET` | `/api/v1/school/{id}/library/fines/config/` | Fine policy |
| 7 | `PATCH` | `/api/v1/school/{id}/library/fines/config/` | Update fine policy |

---

## 7. Business Rules

- Fine computation is automatic (daily cron job); fine amount is recomputed each time the overdue page is accessed — it is not a stored field to avoid stale data
- Fine receipts are issued from a sequential series (LFR/YEAR/SEQ); these are library-specific receipts linked to D-07 as a credit entry
- A fine that has been waived is recorded with the waiver reason and approver; it is not deleted from the audit trail
- Books 30+ days overdue and unpaid are flagged for the "lost book" workflow (G-07) — the student is charged replacement cost instead of daily fine
- Fine revenue is tracked in D-15 daily collection report under "Library Fines" sub-head

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
