# C-15 — Student ID Card Generator

> **URL:** `/school/students/id-cards/`
> **File:** `c-15-student-id-card.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Administrative Officer (S3) — full · Class Teacher (S3) — own class (request) · Principal (S6) — full

---

## 1. Purpose

Generates photo identity cards for all enrolled students. Student ID cards serve multiple purposes in Indian schools:
- **School security:** All students must show ID at gate — security guard verifies identity
- **Transport:** Bus students show ID to driver; transport card (if separate) cross-references with student ID
- **Library:** Library card may reference the same student ID
- **Competitive exams:** JEE/NEET application asks for school ID card scan
- **Police verification:** If a student is found outside school during school hours, police ask for ID
- **Cash-less transactions:** Canteen, sports kit purchase — ID with barcode enables cashless payment

ID cards are issued at the start of every academic year (fresh cards for new students) and on replacement (lost card). A school of 500 students generates ~500 ID cards per year plus ~50 replacements.

---

## 2. Page Layout

### 2.1 Header
```
Student ID Cards — 2026–27                    [Generate Cards]  [Bulk Print]  [Export List]
Generated: 312 / 380 students  ·  Pending: 68  ·  Replacements: 8
```

### 2.2 Class-wise Status
| Class | Students | Cards Generated | Distributed | Pending |
|---|---|---|---|---|
| Nursery | 40 | 40 | 38 | 2 |
| LKG | 38 | 38 | 36 | 2 |
| Class I | 41 | 41 | 40 | 1 |
| Class XI-A | 38 | 32 | 30 | 8 |
| Class XI-B | 36 | 36 | 34 | 2 |

---

## 3. ID Card Template

### 3.1 Front Side
```
┌──────────────────────────────────────────────────┐
│  [School Logo]    [SCHOOL NAME]     2026–27       │
│               [Address — City]                   │
│  ┌───────┐                                        │
│  │       │  Name:  ARJUN SHARMA                  │
│  │ Photo │  Class: XI-A  Roll: 15                │
│  │ 35×45 │  Adm No: GVS/2026/0187               │
│  └───────┘  DOB: 12 Apr 2008                     │
│             Blood Grp: B+                        │
│  [Barcode / QR Code — Student ID: STU-0001187]   │
│  Emergency Contact: Rajesh Sharma  9876543210     │
└──────────────────────────────────────────────────┘
```

### 3.2 Back Side
```
┌──────────────────────────────────────────────────┐
│  If found, please return to:                     │
│  [SCHOOL NAME]                                   │
│  [Full Address with PIN]                         │
│  Phone: [School Phone]                           │
│                                                   │
│  School Timings: 8:00 AM – 3:30 PM               │
│  [School Website] · [School Email]               │
│                                                   │
│  Validity: Academic Year 2026–27                 │
│  ________________________                        │
│  Signature of Principal                          │
└──────────────────────────────────────────────────┘
```

### 3.3 Template Customisation
School can configure:
- Card size: CR-80 (standard credit card 85.6×53.98mm) or custom
- Background colour / design (upload template image)
- Which fields appear on front/back
- Barcode vs QR code (QR code encodes Student ID URL for quick scan)
- Transport route field (optional; shows bus route number)
- House name field (optional)
- School motto or tagline (optional)

---

## 4. Generate Cards

### 4.1 Single Card
From student profile (C-08) → [Generate ID Card] → PDF of 1 card generated.

### 4.2 Class-wise Bulk Generation
[Generate Cards] → select class:
```
Generate ID Cards — Class XI-A

Students needing new cards: 38
Prerequisites:
  ✅ Photos uploaded for all 38 students
  ✅ Enrollment complete

Card size: [CR-80 (Standard) ▼]
Cards per A4 sheet: [8 ▼] (3 rows × 2 columns)

[Generate 38 Cards — Download as PDF]
```

Output: A4 PDF with 8 cards per page (5 pages for 38 students). Print on CR-80 card stock or cut from A4 sheet. Includes crop marks.

### 4.3 Photo Check
If any student in the selected class has no photo uploaded → warning:
```
⚠️ 3 students missing photos:
  Suresh M. (Roll 24) — [Upload Photo Now]
  Kavya P. (Roll 31) — [Upload Photo Now]
  Dinesh R. (Roll 38) — [Upload Photo Now]

You can generate cards for the remaining 35 students now and
generate for these 3 once photos are uploaded.

[Generate for 35 students]  [Wait for all photos]
```

---

## 5. Distribution Tracking

After cards are printed and distributed:
```
Class XI-A — Distribution

Roll  Name           Card Generated  Distributed   Collected (for replacement)
01    Anjali Das     ✅ 5 Apr         ✅ 6 Apr      —
02    Arjun Sharma   ✅ 5 Apr         ✅ 6 Apr      —
15    Suresh M.      ✅ 12 Apr        ⬜ —          —   [Mark Distributed]
```

[Bulk Mark Distributed] → marks entire class as distributed on a given date.

---

## 6. Replacement Cards

Lost, damaged, or expired ID card:
```
[Request Replacement] — Arjun Sharma (STU-0001187)

Original card: Generated 5 Apr 2026
Reason for replacement: Lost — parent declaration form submitted
Replacement fee: ₹100 (charged in fee module)
Fee Receipt No.: R/2026/8421

[Generate Replacement Card]
```

Replacement cards are marked "DUPLICATE" in small print at the bottom (school-configurable).

---

## 7. QR Code on Card

QR code encodes: `eduforge://student/STU-0001187`

When scanned by school security app (if configured):
- Shows student photo, name, class — for instant verification
- Records gate entry/exit time (integrates with gate management if enabled)
- Alerts if student is suspended or has a flag on their record

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/id-cards/?class_id={id}&year={year}` | ID card status |
| 2 | `POST` | `/api/v1/school/{id}/students/id-cards/generate/` | Generate single or bulk cards |
| 3 | `GET` | `/api/v1/school/{id}/students/id-cards/{student_id}/pdf/` | Fetch card PDF |
| 4 | `PATCH` | `/api/v1/school/{id}/students/id-cards/{student_id}/distribute/` | Mark as distributed |
| 5 | `POST` | `/api/v1/school/{id}/students/id-cards/{student_id}/replacement/` | Issue replacement |
| 6 | `GET` | `/api/v1/school/{id}/students/id-cards/template/` | Get current card template config |
| 7 | `PATCH` | `/api/v1/school/{id}/students/id-cards/template/` | Update card template |

---

## 9. Business Rules

- ID card cannot be generated without a student photo — the system enforces this; the photo field is mandatory in C-05 enrollment
- Cards are generated for the current academic year only; at year-end (after promotion in C-10), new cards are generated for the new year for all students
- Class XII graduates receive their last ID card but it becomes invalid after graduation (validity says "2026–27" only)
- Replacement card fee is school-configurable; the fee collection is handled in div-d (not in this module)
- If a student is transferred internally (C-11) to a different section after card generation, the card still shows the old section — a replacement must be issued if the class name on the card matters (most schools don't bother for section changes)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
