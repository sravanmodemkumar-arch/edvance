# G-01 — Book Catalogue

> **URL:** `/school/library/catalogue/`
> **File:** `g-01-book-catalogue.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Librarian (S3) — full management · Library Assistant (S2) — add/edit books · Academic Coordinator (S4) — collection review · All Staff — search · Students/Parents — search via parent/student portal (title/author only)

---

## 1. Purpose

The searchable catalogue of all books in the school library. The catalogue is the backbone of library management — every issue, return, reservation, and stock audit references the catalogue entry. Indian school library considerations:
- **Accession Register:** Mandatory under most state education rules; every book must have a unique accession number; the physical accession register was traditionally the primary record; EduForge digitises this
- **Dewey Decimal Classification (DDC):** Standard for Indian school libraries; subject-based shelf location
- **MARC 21 format:** Modern library systems use Machine-Readable Cataloguing; supports ISBN-based auto-fetch
- **Multi-copy books:** A school may have 5 copies of a class textbook — each copy has its own barcode; the catalogue record is one entry with 5 copy records

---

## 2. Page Layout

### 2.1 Header
```
Book Catalogue                                       [+ Add Book]  [Bulk Import]  [Export]
Total Titles: 4,280  ·  Total Copies: 7,840  ·  Available Now: 6,920  ·  Issued: 920
```

### 2.2 Catalogue Search
```
Search: [__________________________________]  [Search]
Filter: Category [All ▼]  Language [All ▼]  Status [All ▼]  Class Level [All ▼]

Sort by: ● Accession No.  ○ Title A-Z  ○ Recent Acquisitions  ○ Most Borrowed

Results (showing 20 of 4,280):

Acc. No.  Title                            Author          DDC      Copies  Avail  Status
0001      Wings of Fire                    A.P.J. Abdul K. 954.9    3       2      ✅ Available
0002      The Alchemist                    Paulo Coelho    863.64   2       1      🟡 1 issued
0003      Science Textbook Class X (NCERT) NCERT           500      8       8      ✅ Available
0004      Discovery of India              Jawaharlal Nehru 954.03  4       4      ✅ Available
0005      Maths Puzzle Book               R.D. Sharma     510      2       0      🔴 All issued
```

---

## 3. Add Book

```
[+ Add Book]

Method:
  ● Scan ISBN barcode → auto-fetch from OpenLibrary/Google Books API
  ○ Enter ISBN manually → auto-fetch
  ○ Manual entry (for books without ISBN — old/regional language books)

After ISBN scan (0-14-028329-0):
  Auto-fetched from Open Library:
  Title:     The Alchemist
  Author(s): Paulo Coelho (translated by Alan Clarke)
  Publisher: HarperCollins India
  Year:      1999 (first Indian edition)
  ISBN:      978-81-7223-305-2
  Language:  English
  Pages:     197
  Genre:     Fiction — Philosophy

  [Confirm auto-filled data] or [Edit manually]

Catalogue fields:
  Accession Number: [Auto: 4281]  ← sequential; editable if books being entered retroactively
  Title: [The Alchemist]
  Author(s): [Paulo Coelho]  [Add author]
  Publisher: [HarperCollins India]
  Edition: [1st Indian, 1999]
  Year of Publication: [1999]
  ISBN: [978-81-7223-305-2]
  Language: [English ▼]
  Subject Category: [Fiction — General ▼]  (dropdown with common school categories)
  DDC Number: [863.64]  (Dewey Decimal Classification — auto-suggested from ISBN)
  CBSE Subject Linkage: [—] (if this is a textbook/reference for a specific subject)
  Section: [Fiction ▼]  (Lending / Reference / Rare / Periodicals)
  Class Level: [General ▼]  (Nursery–V / VI–VIII / IX–X / XI–XII / Teacher Ref / General)
  Price: [₹295]
  Source: ● Purchased  ○ Donated  ○ Government (NCERT supply)

Number of copies being added: [2]
  Copy 1: Barcode [LIB2026001] — auto or [Scan existing barcode]
  Copy 2: Barcode [LIB2026002]
  Condition: ● Good  ○ Fair  ○ Poor

[Save to Catalogue]  [Print Barcode Labels]
```

---

## 4. Book Detail View

```
The Alchemist — Paulo Coelho

Accession No.: 0002 (master)  ·  DDC: 863.64  ·  Section: Fiction
Class Level: General  ·  Language: English  ·  Publisher: HarperCollins India
ISBN: 978-81-7223-305-2  ·  Price: ₹295  ·  Added: 15 Jun 2023

2 Copies:
  Copy 1 (LIB2023045): Status: ✅ Available  ·  Condition: Good  ·  Shelf: F-12
  Copy 2 (LIB2023046): Status: 🟡 Issued     ·  Due back: 30 Mar 2026 (Arjun Sharma, XI-A)

Circulation Statistics:
  Total issues this year: 18  ·  Total issues all time: 47
  Most borrowed by: Class XI (11 times), Class X (8 times)
  Average hold time: 12 days

[Edit]  [Add Copy]  [Mark Copy Lost/Damaged]  [View Full Issue History]
```

---

## 5. Bulk Import

```
[Bulk Import] → CSV/Excel upload:

Supported columns (required*):
  accession_no*, title*, author*, publisher, year, isbn, language*,
  category*, ddc, section*, class_level, price, copies*

Template: [Download CSV Template]

Upload: [Choose File]
Preview first 5 rows before import: ✅
Duplicate ISBN handling: ● Update existing  ○ Create new entry  ○ Skip

Status after import:
  Imported: 245 titles  ·  Skipped (duplicate): 12  ·  Error: 3 (missing required fields)
  [Download error report]
```

---

## 6. Catalogue Export (CBSE Inspection)

```
[Export] → options:

Format: ● XLSX  ○ CSV  ○ PDF (printed catalogue)
Content: ● Full catalogue  ○ New acquisitions this year  ○ Reference section only

For CBSE inspection, the catalogue export shows:
  - Total titles: 4,280
  - Total volumes (copies): 7,840
  - Collection by subject (Science: 840, Social Studies: 620, Languages: 1,200, Fiction: 1,400, Reference: 980...)
  - NCERT textbooks: 380 volumes
  - Periodicals: 24 subscriptions

CBSE affiliation minimum collection requirement: ≥ 1,500 titles for primary; ≥ 3,000 for senior secondary
Current: 4,280 titles ✅ Meets requirement
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/catalogue/?search={q}&category={c}&available={bool}` | Catalogue search |
| 2 | `POST` | `/api/v1/school/{id}/library/catalogue/` | Add book |
| 3 | `GET` | `/api/v1/school/{id}/library/catalogue/{book_id}/` | Book detail |
| 4 | `PATCH` | `/api/v1/school/{id}/library/catalogue/{book_id}/` | Edit book record |
| 5 | `POST` | `/api/v1/school/{id}/library/catalogue/bulk-import/` | Bulk CSV import |
| 6 | `GET` | `/api/v1/school/{id}/library/catalogue/isbn-lookup/?isbn={isbn}` | ISBN auto-fetch |
| 7 | `GET` | `/api/v1/school/{id}/library/catalogue/export/?format={xlsx|csv|pdf}` | Export catalogue |
| 8 | `GET` | `/api/v1/school/{id}/library/catalogue/stats/` | Collection statistics |

---

## 8. Business Rules

- Accession numbers are sequential and permanent; a deaccessioned book's number is not reused (gap in register is acceptable; the book is marked as "Deaccessioned")
- Each physical copy has a unique barcode; the barcode is used for scan-based issue/return in G-03
- Reference section books are catalogued but not issuable outside library; they are marked as Section=Reference and the system prevents issue
- Books donated by alumni or parents are accepted and catalogued; source is recorded as "Donated" with donor name for acknowledgement
- ISBN-based auto-fetch uses OpenLibrary API (free, no key needed) with Google Books API as fallback; for books without ISBNs (old regional language books), manual entry is required
- CBSE affiliation reports require collection statistics — the export must exactly match the physical stock count; hence annual stock verification (G-12) is required

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
