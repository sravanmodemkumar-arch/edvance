# G-12 — Stock Verification

> **URL:** `/school/library/stock-verify/`
> **File:** `g-12-stock-verification.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Librarian (S3) — conduct verification · Library Assistant (S2) — physical scan · Academic Coordinator (S4) — review report · Principal (S6) — approve write-offs

---

## 1. Purpose

Annual (or periodic) physical verification of the library stock — scanning all books on the shelf and reconciling against the catalogue. Required because:
- **CBSE affiliation inspection:** Inspectors verify that the physical collection matches the catalogue
- **Audit trail:** The accession register (G-01) must match the physical count; discrepancies require explanation
- **Missing books detection:** Books not on shelf and not issued may have been misplaced or stolen
- **Condition assessment:** Old/damaged books identified for repair, binding, or withdrawal

---

## 2. Page Layout

### 2.1 Header
```
Stock Verification                                   [Start New Verification]
Academic Year: [2026–27 ▼]

Last Verification: 20 April 2025 (11 months ago)
Books verified: 7,800/7,840 ·  Discrepancy: 40 books (0.5%) — resolved
Next scheduled verification: April 2026 (Annual)

Current Status: No verification in progress
```

---

## 3. Conduct Stock Verification

```
[Start New Verification]

Verification type:
  ● Annual full stock verification
  ○ Spot check (section-specific)

Scope: ● All sections  ○ Lending only  ○ Reference only

Method:
  ● Barcode scanner (fastest — 2 staff, 2 days for 7,840 books)
  ○ Manual count (section-by-section, fallback if scanner fails)

[Start Verification — Freeze Catalogue]
  → Catalogue frozen during verification (no new issues/returns until complete)
  → Pending issues will be queued and processed after verification
  → Duration estimate: 2 days (based on last year)

Phase 1: Physical scan
  Progress: ████████░░ 82% (6,420/7,840 scanned)
  Not yet scanned sections: Reference (800 books), Periodicals storage

Expected: 7,840 books
Scanned: 6,420 on shelf
Currently issued (G-03): 920 books
To scan: 7,840 − 920 issued = 6,920 on shelf
```

### After Full Scan:
```
Stock Verification Report — April 2026

Expected on shelf: 6,920 (7,840 total − 920 currently issued)
Physically found: 6,882

Discrepancy: 38 books unaccounted for

Breakdown:
  In catalogue, not found, not issued: 38 books  ← Investigation required
  Found on shelf but not in catalogue: 2 books   ← Unregistered books (add to catalogue)
  Condition issues found:
    Poor condition (needs repair/binding): 45 books
    Damaged beyond use: 8 books → [Initiate G-07 write-off]

Discrepancy investigation:
  Of 38 missing:
  - 12 likely misplaced in wrong section (Librarian to search manually)
  - 18 listed in old register but probably earlier unreported losses (history > 3 years)
  - 8 cannot be accounted for → [Report as lost; no member charged — school loss]

[Generate Verification Report]  [Approve Write-offs (Principal)]  [Resume Normal Operations]
```

---

## 4. Verification Report (CBSE Format)

```
LIBRARY STOCK VERIFICATION REPORT
Greenfields School  ·  Affiliation: AP2000123
Conducted: 15–16 April 2026

Total catalogue entries: 4,280 titles / 7,840 copies
Verified on shelf: 6,882 / 6,920 expected on shelf
Currently issued: 920 copies (cross-checked against G-03)
Verified as issued + on shelf: 7,802/7,840 (99.5%)
Unaccounted: 38 copies (0.5%)

Disposition of unaccounted copies:
  Misplaced (recovered on re-search): 12
  Historical losses (> 3 years old): 18  → Written off after Principal approval
  Current year unexplained: 8  → Under investigation

Condition assessment:
  Good: 6,680 copies
  Fair: 840 copies (usable, minor wear)
  Poor (repair needed): 45 copies
  Deaccession recommended: 8 copies

New additions since last verification: 245 books (ACQ/2026/1, 2, 3)

Certified by: [Principal]  [Librarian]  Date: 20 April 2026  Seal: [SCHOOL SEAL]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/stock-verify/history/` | Past verifications |
| 2 | `POST` | `/api/v1/school/{id}/library/stock-verify/start/` | Start new verification |
| 3 | `POST` | `/api/v1/school/{id}/library/stock-verify/{verify_id}/scan/` | Submit scanned barcodes |
| 4 | `GET` | `/api/v1/school/{id}/library/stock-verify/{verify_id}/discrepancy/` | Discrepancy report |
| 5 | `POST` | `/api/v1/school/{id}/library/stock-verify/{verify_id}/complete/` | Finalise verification |
| 6 | `GET` | `/api/v1/school/{id}/library/stock-verify/{verify_id}/pdf/` | CBSE format report PDF |

---

## 6. Business Rules

- Stock verification is conducted annually (April — after academic year end); for large collections (> 10,000 books), section-wise verification across multiple days is permitted
- During verification, the catalogue is frozen (no new issues/returns); a clearly visible notice is placed at the library counter
- Books found damaged during verification are handled via G-07 (damaged book process) — if the last borrower is identifiable, replacement charge may be applied; if not, it's a school write-off
- The verification report must be signed by the Librarian and Principal, and a copy is filed for CBSE affiliation renewal
- Unaccounted books > 1% of collection trigger an enhanced investigation (section-by-section re-scan) before write-off approval

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
