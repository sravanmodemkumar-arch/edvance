# G-07 — Lost / Damaged Books

> **URL:** `/school/library/lost-damaged/`
> **File:** `g-07-lost-damaged-books.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Librarian (S3) — report and manage · Academic Coordinator (S4) — approve write-off · Principal (S6) — expensive book write-off · Administrative Officer (S3) — fee recovery

---

## 1. Purpose

Handles books that are returned damaged or reported lost. Determines replacement cost, charges the responsible member, removes the copy from active catalogue when unrecoverable, and maintains the audit record.

---

## 2. Page Layout

### 2.1 Header
```
Lost & Damaged Books                                 [Report Lost Book]  [Report Damage]
Academic Year: [2026–27 ▼]

Lost this year: 8 books  ·  Damaged: 12 books
Replacement charges collected: ₹3,200  ·  Outstanding: ₹1,850
Write-offs (unrecoverable): 3 books
```

---

## 3. Report Lost Book

```
[Report Lost Book]

Triggered when: student reports book lost  OR  book overdue 60+ days with no return

Book: [Scan barcode or search] → LIB2023046 — The Alchemist (Paulo Coelho)
Currently issued to: Suresh Kumar (IX-A) — overdue 36 days
Last issue date: 5 Feb 2026  ·  Due: 19 Feb 2026

Lost declaration:
  Declared lost by: ● Student (parent signed declaration)  ○ Staff

Replacement cost:
  Original purchase price: ₹295
  Current market price (auto-estimated): ₹295 (no inflation adjustment — policy)
  Charge to student: ₹295

Payment options:
  ○ Pay at library counter now (cash)
  ● Add to fee ledger (D-07) — collected at D-04

Action on copy record:
  → Copy LIB2023046 status set to "Lost"
  → Removed from available inventory (not deleted — retains history)
  → Issue record closed: "Lost — replacement charge raised ₹295"
  → Accession register note: "Copy 2 lost by STU-0001220 on 27 Mar 2026; charged ₹295"

[Process Lost Book + Raise Charge]
```

---

## 4. Report Damage on Return

```
Damage Assessment — Returned book

Book: Wings of Fire (LIB2023012) — returned by Ravi Kumar (IX-A)

Librarian assessment:
  ● Minor damage (torn page, stain) — no charge  [minor damage threshold: ₹50]
  ○ Moderate damage (cover damage, water stain affecting multiple pages) — partial charge
  ○ Severe damage (spine broken, multiple pages missing) — full replacement charge

Minor damage: [Mark as Minor Damage — No Charge]
  → Book condition updated to "Fair" in catalogue
  → Still issuable

Moderate damage: Charge = ₹100 (fixed for moderate category)

Severe damage: Charge = ₹295 (replacement cost)
  → Copy removed from issuable inventory
  → Status: "Damaged — Deaccessioned"

[Process Damage Assessment]
```

---

## 5. Recovery Tracking

```
Outstanding Replacement Charges — 2026–27

Student         Book                  Charge  Raised      Paid    Status
Suresh K. IX-A  The Alchemist         ₹295   15 Mar 26   ₹0      ⬜ Outstanding
Meena D. XII-A  Discovery of India    ₹250   20 Feb 26   ₹0      ⬜ Outstanding
Ravi R. VII-B   Wings of Fire         ₹180   10 Jan 26  ₹180     ✅ Paid

Outstanding: ₹545  ·  Collected: ₹3,200

[Send Reminder to Outstanding Members]
[Block TC until cleared] — TC (C-13) is already gated on this
```

---

## 6. Write-Off (Unrecoverable)

```
Write-Off — Copy LIB2018034

Book: Science Textbook Class X (2018 edition, outdated)
Reason: ● New edition published; old copy no longer used  ○ Student did not return
Charge status: N/A (school decision to write off — not member's loss)

Approved by: Academic Coordinator + Principal (value ₹240)

Write-off entry:
  → Copy removed from catalogue (status: Deaccessioned)
  → Annual stock verification count reduced by 1
  → Accession register note: "Written off — superseded edition, 27 Mar 2026"

[Process Write-Off]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/lost-damaged/?year={y}` | Lost/damaged register |
| 2 | `POST` | `/api/v1/school/{id}/library/lost-damaged/lost/` | Report lost book |
| 3 | `POST` | `/api/v1/school/{id}/library/lost-damaged/damage/` | Report damage on return |
| 4 | `POST` | `/api/v1/school/{id}/library/lost-damaged/write-off/` | Deaccession write-off |
| 5 | `GET` | `/api/v1/school/{id}/library/lost-damaged/outstanding-charges/` | Unpaid replacement charges |

---

## 8. Business Rules

- Replacement charge is the original purchase price (from G-01 catalogue); no inflation surcharge unless the school configures one; the charge is raised as a library-specific fine in D-07
- A student who pays the replacement cost takes ownership of no rights — the book is simply "written off lost" and the payment is revenue to the library (used for replacement purchase)
- Write-off requires Academic Coordinator approval for books ≤ ₹500; Principal for > ₹500 (to prevent informal disposal of library assets)
- TC clearance requires: all books returned AND all charges paid; even a ₹10 fine blocks TC (G-03 clearance check)
- If a "lost" book is found and returned by the student after paying replacement cost, the school may refund or credit at the Principal/Academic Coordinator's discretion; no automatic refund

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
