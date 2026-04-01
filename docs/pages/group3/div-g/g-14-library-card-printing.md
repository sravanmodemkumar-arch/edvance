# G-14 — Library Card Printing

> **URL:** `/school/library/cards/`
> **File:** `g-14-library-card-printing.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Librarian (S3) — print and issue · Library Assistant (S2) — print under supervision · Administrative Officer (S3) — bulk printing for new batch

---

## 1. Purpose

Generates and manages library member cards — the physical card that students and staff carry to the library for book issue/return. The card has a barcode or QR code that is scanned at the issue/return counter (G-03).

Distinct from the Student ID Card (C-15) — the student ID card is for general school identification; the library card is specific to library access and includes library-specific information (member ID, borrowing limit, issue history URL).

---

## 2. Page Layout

### 2.1 Header
```
Library Card Printing                                [Print New Cards]  [Print Replacement]
Academic Year: [2026–27 ▼]

Cards printed this year: 48 (new) + 8 (replacements)
Cards yet to print (new enrollments without card): 3
```

---

## 3. Card Design

```
Library Card — Front:

┌─────────────────────────────────────────────────────────────────┐
│  [School Logo]  GREENFIELDS SCHOOL LIBRARY CARD                 │
│                                                                  │
│  ┌──────────┐  Name:    ARJUN SHARMA                            │
│  │ [Photo]  │  Class:   XI-A   Roll: 02                         │
│  │          │  Member:  M-0001187                               │
│  └──────────┘  Limit:   2 books / 14 days                       │
│                                                                  │
│  [BARCODE: M-0001187]                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Library Card — Back:

┌─────────────────────────────────────────────────────────────────┐
│  Library Hours: Mon–Fri: 8:30 AM – 4:00 PM                     │
│                Saturday: 9:00 AM – 12:00 PM                     │
│                                                                  │
│  Fine: ₹1/day after due date                                    │
│  Report lost card immediately to librarian.                     │
│                                                                  │
│  [QR Code → library.greenfields.edu.in/member/M-0001187]        │
│  (scan to view your current issues and due dates)               │
│                                                                  │
│  Academic Year: 2026–27                                          │
└─────────────────────────────────────────────────────────────────┘

Card size: CR-80 (85.6 × 53.98 mm — standard wallet size)
Print: 8 cards per A4 sheet (same layout as C-15 student ID)
```

---

## 4. Print Workflow

```
[Print New Cards]

Select members:
  ● All new enrollments without cards (3 pending)
  ○ Entire class: [Select class ▼]
  ○ Individual: [Search member]

Cards to print: 3 cards (1 sheet)

Preview:
  [Card 1 preview — Arjun Sharma M-0001187]
  [Card 2 preview — Anjali Das M-0001188]
  [Card 3 preview — New student M-0001250]

Print settings:
  Paper: ● A4 (8 cards per sheet, cut manually)  ○ CR-80 card stock (direct print)
  Include photo: ☑ Yes (from C-05 enrollment photo)
  Lamination guide: Recommended for durability

[Print]  [Save PDF]
```

---

## 5. Replacement Card

```
[Print Replacement]

Member: [Chandana Rao — XI-A — M-0001190]
Reason: ● Lost  ○ Damaged  ○ Name change

Replacement card:
  → Same Member ID (M-0001190) — barcode/QR unchanged
  → Marked "DUPLICATE" in small text if required (configurable)
  → Previous card invalidated in system (if lost)

Charge: ₹20 replacement fee (configurable) → added to D-07 fee ledger

[Print Replacement Card]  [Issue Duplicate]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/cards/pending/` | Members without cards |
| 2 | `POST` | `/api/v1/school/{id}/library/cards/print/` | Print new cards (batch) |
| 3 | `POST` | `/api/v1/school/{id}/library/cards/replacement/` | Print replacement card |
| 4 | `GET` | `/api/v1/school/{id}/library/cards/pdf/?member_ids={ids}` | Card PDF for selected members |

---

## 7. Business Rules

- Library cards share the same photo and basic data as the Student ID Card (C-15) — sourced from C-05 enrollment; no separate photo upload needed
- Cards are valid for one academic year; at the start of each year, existing cards continue to be valid (same member ID) but new cards may be printed if the design is updated
- Lost card report must be logged in the system to invalidate the old barcode; if someone finds the old card and tries to issue a book, the system alerts "Card reported lost — verify member identity"
- The QR code on the back links to the member's current issue status — parents/students can scan to see what's borrowed and when it's due (read-only, public within the school network)
- Replacement card charge is configurable; the default ₹20 covers printing and lamination cost; collected via D-04 fee counter

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
