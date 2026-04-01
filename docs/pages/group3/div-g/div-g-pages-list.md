# Division G — Library Management — Pages List

> **Group:** 3 — School Portal
> **Division:** G — Library Management
> **Total Pages:** 14
> **Directory:** `docs/pages/group3/div-g/`

---

## Purpose

Manages the school library — book catalogue, issue/return, digital resources, and member management. Indian school library context:
- **CBSE Affiliation Requirement:** Affiliation Bye-Laws mandate a functional school library with minimum collection size; libraries are inspected during affiliation visits
- **NCERT/NBT books:** Many school libraries stock NCERT textbooks, NBT (National Book Trust) publications, and state board texts alongside general fiction/non-fiction
- **Digital resources:** Post-NEP 2020, schools are encouraged to integrate digital libraries (e-Prashikshan, DIKSHA, eBooks)
- **Reading programme:** CBSE's "Reading for Joy" programme requires tracking of student reading habits
- **Lost/damaged books:** Fee recovery for lost/damaged library books; outstanding library dues block TC issuance (C-13)
- **Reference section:** Reference books cannot be issued outside; lending section has different rules
- **Dewey Decimal System:** Indian school libraries typically use DDC (Dewey Decimal Classification); library software must support DDC-based catalogue

---

## Roles (new to this division)

| Role | Code | Level | Description |
|---|---|---|---|
| Librarian | S3 | S3 | Primary library staff — catalogue, issue/return, member management |
| Library Assistant | S2 | S2 | Data entry — book entry, stock updates; no approval authority |
| Class Teacher | S3 | S3 | View own class members' borrowing; library class visit |
| Academic Coordinator | S4 | S4 | Library policy, budget, collection development |
| Principal | S6 | S6 | Library fee waiver, policy approval |

---

## Pages

| Page ID | Title | URL Slug | Priority | Key Function |
|---|---|---|---|---|
| G-01 | Book Catalogue | `library/catalogue/` | P1 | Searchable catalogue; DDC; MARC records |
| G-02 | Book Acquisition | `library/acquisition/` | P2 | Purchase orders; new books; stock entry |
| G-03 | Issue & Return | `library/issue-return/` | P0 | Daily issue/return counter; barcode scan |
| G-04 | Member Management | `library/members/` | P1 | Member cards; borrowing limits; class teacher assign |
| G-05 | Reservations & Holds | `library/reservations/` | P2 | Book reservation queue; notification |
| G-06 | Overdue & Fine | `library/overdue/` | P1 | Overdue list; auto-fine; fee recovery |
| G-07 | Lost / Damaged Books | `library/lost-damaged/` | P1 | Replacement cost; recovery; ledger entry |
| G-08 | Periodicals & Newspapers | `library/periodicals/` | P2 | Magazine/newspaper subscriptions |
| G-09 | Digital Library | `library/digital/` | P2 | e-Books, DIKSHA, e-Prashikshan links |
| G-10 | Library Class Visit | `library/class-visits/` | P2 | Schedule class library periods |
| G-11 | Reading Programme | `library/reading-programme/` | P2 | CBSE Reading for Joy; student reading log |
| G-12 | Stock Verification | `library/stock-verify/` | P1 | Annual stock audit; missing books |
| G-13 | Library Reports | `library/reports/` | P2 | Circulation statistics; most-borrowed; low-circulation |
| G-14 | Library Card Printing | `library/cards/` | P2 | Member library card with barcode/QR |

---

## Key Integrations

- **C-05 Student Enrollment:** Auto-creates library member on enrollment; deactivates on withdrawal
- **C-13 TC Generator:** TC blocked if outstanding library dues > ₹0 or books not returned
- **D-04 Fee Collection:** Library fines collected at fee counter; receipt linked to library record
- **C-17 UDISE:** Library collection count reported in UDISE infrastructure section
- **A-10 Academic Calendar:** Library closed on holidays; reduced hours during exam season

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
