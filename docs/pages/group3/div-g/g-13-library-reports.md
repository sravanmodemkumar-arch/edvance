# G-13 — Library Reports

> **URL:** `/school/library/reports/`
> **File:** `g-13-library-reports.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Librarian (S3) — view and generate · Academic Coordinator (S4) — full · Principal (S6) — full

---

## 1. Purpose

Analytics and reports for library management — helps the Librarian and Academic Coordinator understand usage patterns, improve collection development, and demonstrate library utilisation to CBSE inspectors and school management.

---

## 2. Page Layout

### 2.1 Header
```
Library Reports                                      [Generate Report]
Academic Year: [2026–27 ▼]

Total issues this year: 8,420  ·  Unique borrowers: 312/452 (69%)
Most active class: XI-A (180 issues)  ·  Least active: XII-B (42 issues)
Most borrowed book: Wings of Fire (67 issues)
```

### 2.2 Available Reports
```
Report Name                    Description                          Last Generated
Circulation Statistics         Issues per month/class/subject       15 Mar 2026  [Generate]
Most Borrowed Books            Top 20 by issue count                15 Mar 2026  [Generate]
Low Circulation Books          Books not borrowed in 2+ years       —            [Generate]
Member Activity Report         Top/bottom borrowers by class        —            [Generate]
Overdue Summary                Current overdue + fine summary       Daily auto   [View]
Fine Collection Report         Monthly fine revenue                 1 Mar 2026   [Generate]
CBSE Affiliation Report        Complete library data for inspection —            [Generate]
Annual Library Report          Year-end comprehensive report        —            [Generate]
```

---

## 3. Circulation Statistics

```
Monthly Issues — 2026–27

Month         Issues   Unique Members   Top Class    Top Book
April 2026      720         210          IX-A         Wings of Fire
May 2026        680         195          XI-A         The Alchemist
June 2026        95          45          Mixed        Vacation reading
July 2026       650         200          XI-A         Atomic Habits
...
March 2026      480         180          XI-A         Various

Annual total:   8,420 issues

By class level:
  Primary (I–V):   1,840 issues (22%)
  Middle (VI–VIII): 2,100 issues (25%)
  Secondary (IX–X): 2,480 issues (29%)
  Senior (XI–XII):  2,000 issues (24%)
```

### Subject/Genre breakdown:
```
Category         Issues    % of total   Trend
Fiction           3,360       40%       ↑ Increasing
Science & Nature  1,684       20%       → Stable
Biographies       1,262       15%       ↑ Increasing (Wings of Fire effect)
Social Studies      842       10%       → Stable
Reference           560        7%       ↓ Declining (digital access increasing)
Others              712        8%       → Stable
```

---

## 4. Low Circulation Report

```
Books not borrowed in last 24 months: 840 titles (20% of collection)

Examples:
  ACC  Title                         Category   Last Borrowed   Action
  0245 Encyclopaedia Britannica 2001 Reference  Never           ● Retain (reference)  ○ Deaccession
  1024 Computer Science Class XI 2012 Academic  Aug 2022        ● Deaccession (outdated)
  0876 Geography of Mesopotamia     Non-fiction  Feb 2022        ○ Retain  ○ Deaccession

Low circulation recommendations:
  → Deaccession outdated textbooks/encyclopaedias (replaced by digital)
  → Promote low-circulation fiction via reading programme recommended lists (G-11)
  → Purchase newer editions of frequently requested but outdated titles

[Bulk Deaccession Selected]  [Add to Reading Programme List]
```

---

## 5. CBSE Affiliation Library Report

```
[Generate CBSE Affiliation Report]

LIBRARY REPORT FOR CBSE AFFILIATION RENEWAL
Greenfields School  ·  2026–27

Section A: Collection
  Total titles: 4,280  ✅ (Requirement: ≥ 3,000 for senior secondary)
  Total volumes: 7,840
  New acquisitions this year: 245 titles
  Reference books: 980 volumes
  NCERT textbooks: 380 volumes
  Fiction: 1,400 volumes

Section B: Periodicals
  Newspaper subscriptions: 5 (English: 3, Telugu: 2)  ✅ (Min 5 required)
  Magazine subscriptions: 24  ✅ (Min 10 required)

Section C: Digital Resources
  DIKSHA: ✅ Connected  ·  NDLI: ✅ Registered
  e-Pathshala: ✅ Linked

Section D: Utilisation
  Average daily visits: 42 students
  Annual issues: 8,420
  Borrowers (% of students): 82%

Section E: Infrastructure (for manual entry — from UDISE)
  Library area: 120 sq. m  ·  Seating: 40 students
  Reading room: Yes  ·  Computer terminals: 5

Certified by: [Principal]  ·  Date: 27 Mar 2026
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/reports/circulation/?year={y}&month={m}` | Monthly circulation |
| 2 | `GET` | `/api/v1/school/{id}/library/reports/most-borrowed/?year={y}&limit={20}` | Top books |
| 3 | `GET` | `/api/v1/school/{id}/library/reports/low-circulation/?months={24}` | Under-utilised books |
| 4 | `GET` | `/api/v1/school/{id}/library/reports/member-activity/?year={y}` | Member activity |
| 5 | `GET` | `/api/v1/school/{id}/library/reports/cbse-affiliation/?year={y}` | CBSE affiliation report |
| 6 | `GET` | `/api/v1/school/{id}/library/reports/annual/?year={y}` | Annual comprehensive report PDF |

---

## 7. Business Rules

- Library reports are generated on-demand (not pre-scheduled) except the daily overdue summary, which is auto-generated and emailed to the Librarian each morning
- The CBSE affiliation report aggregates from G-01, G-08, G-09, and G-12 — all must be up-to-date before generating this report
- Low-circulation reports are used for collection weeding (removing outdated/unused books); the decision to deaccession requires Academic Coordinator approval (bulk) or Principal (individual high-value books)
- Report data older than the current academic year is archived; the previous 3 years remain accessible for trend comparison

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
