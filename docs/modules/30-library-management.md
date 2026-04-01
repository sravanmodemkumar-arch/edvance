# Module 30 — Library Management

## 1. Purpose

Module 30 owns the complete library lifecycle within EduForge institutions — from catalogue management and book acquisition through member management, issue/return, digital resources, fine collection, NAAC/NIRF compliance reporting, and strategic reading analytics. It serves physical libraries, digital libraries, and hybrid setups across all 16 institution types.

The module aligns with UGC Library Committee guidelines, NAAC Criterion 4.2 (Library, ICT and Physical Infrastructure), NIRF library data requirements, INFLIBNET N-LIST programme, and GST zero-rating for books (HSN 4901). It integrates with Module 07 (Student Profile), Module 08 (Staff Management), Module 05 (Academic Calendar), Module 15 (Syllabus), Module 25 (Fee Collection), Module 28 (Hostel Checkout), Module 32 (Counselling), Module 35 (Notifications), and Module 42 (Audit Log).

---

## 2. Library Configuration

### 2.1 Library Types & Multi-Library Support

Each institution can operate multiple library units under a single tenant:

| Library Unit | Description |
|-------------|-------------|
| Central library | Primary collection; all members |
| Departmental library | Subject-specific; faculty + students of that department |
| Hostel reading room | Basic collection; hostellers; limited borrowing |
| Digital library lab | e-resource access terminals; no physical lending |
| Rare book room | Restricted access; reference only |

Each unit has its own catalogue, staff, rules, and seating capacity. Cross-unit catalogue search available through unified OPAC.

### 2.2 Library Master Configuration

| Parameter | Options |
|-----------|---------|
| Library type | Physical / Digital / Hybrid |
| Classification system | Dewey Decimal Classification (DDC) / UDC (for technical colleges) |
| Barcode vs RFID | Barcode scanner / RFID reader (anti-theft) / Both |
| OPAC access | Public (no login) / Members only |
| Seating capacity | Reading hall seats tracked |
| Library hours | Per day per shift; sync with Module 05 calendar |
| Holiday closure | Automatic from Module 05 academic calendar |
| INFLIBNET membership | N-LIST subscription; credential reference stored |

### 2.3 OPAC (Online Public Access Catalogue)

Public-facing catalogue search — no login required:
- Search by title, author, subject, ISBN, keyword, DDC class
- Results show: title, author, availability (copies available / all issued), shelf location
- Reservations: logged-in members can place holds from OPAC
- New arrivals feed: last 30 days
- Subject browse: DDC hierarchy → titles
- Mobile app OPAC: same search in student/staff app

### 2.4 UGC Library Committee

- Members list: names, designations, role (Chairperson / Member / Member Secretary)
- Meeting schedule: minimum 2 meetings per year (UGC requirement)
- Meeting minutes: recorded in-app (date, agenda, attendance, resolutions)
- Annual library report: auto-generated from module data; submitted to Principal + UGC committee
- NAAC visit readiness: committee records viewable in compliance dashboard

---

## 3. Catalogue & Book Master

### 3.1 Book Record Structure

| Field | Detail |
|-------|--------|
| Title | Full title including subtitle |
| Author(s) | Up to 5 authors; first author used for sorting |
| Publisher | Publisher name + city |
| Edition | Edition number (1st, 2nd …) |
| Year of publication | 4-digit year |
| ISBN | ISBN-13 (preferred) / ISBN-10 |
| DDC class | Primary DDC number (e.g., 519.5 for Statistics) |
| Sub-classification | Division and section within DDC |
| Subject / Keywords | Free-text tags for full-text search |
| Language | English / Hindi / regional language |
| Series | Series name + volume number (if applicable) |
| Physical description | Pages, dimensions (cm), illustrated (Y/N) |
| Acquisition source | Purchased / Donated / Government grant / ILL |
| Acquisition date | Date added to library |
| Purchase price | Per copy cost (₹) |
| Vendor | Supplier name from vendor master |
| Budget head | Fund from which acquired |
| Reference-only flag | Non-circulating; reading room use only |
| Restricted flag | Faculty/staff access only |
| Rare book flag | Special handling; insured value stored |

### 3.2 Copy Record (Per Physical Book)

Each title may have multiple copies. Each copy carries:

| Field | Detail |
|-------|--------|
| Accession number | Sequential, year-prefixed (e.g., 2024-00347) |
| Copy number | Copy 1, Copy 2, … of same title |
| Barcode / QR | Generated on accession; printable label |
| RFID tag number | If RFID-enabled library |
| Shelf location | Rack ID + shelf number + position |
| Condition | New / Good / Fair / Poor / Withdrawn |
| Status | Available / Issued / Reserved / Lost / Withdrawn / In repair / In bindery |
| Date withdrawn | If permanently removed |
| Withdrawal reason | Damaged beyond repair / Lost / Outdated / Weeded |

### 3.3 Special Material Types

| Type | Additional Fields |
|------|-----------------|
| Journal / Periodical | ISSN, volume, issue, date, subscription period |
| Newspaper | Title, daily/weekly, vendor |
| Thesis / Dissertation | Student name, guide name, department, year, degree |
| AV Material | Media type (DVD/CD/Map), format, duration |
| eBook (institutional) | Access URL (time-limited), licence seats, platform |
| Rare book | Condition report, insured value, humidity requirement |

### 3.4 Barcode & QR Label Generation

On accession:
- System generates unique barcode (Code 128 or Code 39) per copy
- QR label embeds: accession number + title + shelf location
- Print-ready label format (3.5cm × 2.5cm Avery-compatible)
- Bulk print: librarian can queue 50+ labels for one print run
- Student scanning a shelf QR label → sees all titles on that shelf in app

### 3.5 Book Withdrawal (Weeding) Register

Annual weeding process:
- Librarian marks copies as Withdrawn with reason
- Withdrawal register: accession number, title, copy, date, reason, disposal method (Sold as waste / Donated / Destroyed)
- Disposed copies removed from available inventory; historical accession record retained
- Books > 20 years old and not issued in 5 years → auto-flag for weeding review

---

## 4. Member Management

### 4.1 Membership Auto-Creation

- On student enrolment (Module 07) → library member record auto-created
- On staff joining (Module 08) → library member record auto-created
- Member type inherits from source: Student / Teaching Staff / Non-teaching Staff / Research Scholar
- Additional types: Alumni (manual creation, fee applicable) / Guest (fixed-duration, manual)

### 4.2 Borrowing Rules by Member Type

| Member Type | Borrowing Limit | Loan Period | Renewals |
|-------------|----------------|-------------|----------|
| Student (School) | 2 books | 14 days | 1 |
| Student (College) | 3 books | 14 days | 2 |
| Research Scholar | 5 books | 30 days | 3 |
| Teaching Staff | 10 books | 30 days | 3 |
| Non-teaching Staff | 3 books | 14 days | 1 |
| Alumni | 2 books | 14 days | 1 |
| Guest | 1 book | 7 days | 0 |

All limits configurable per institution.

### 4.3 Library Member Card

- Member photo, name, ID number, member type, validity period
- Barcode / QR unique per member per academic year
- Digital card: available in student/staff app
- Physical card: printable if needed

### 4.4 Member Status

| Status | Trigger |
|--------|---------|
| Active | Default for enrolled students / active staff |
| Suspended | 3+ overdue books unreturned > 30 days; fine outstanding > threshold |
| Inactive | Student de-enrolled / staff exited (auto) |
| Expired | Alumni/guest membership past validity date |

Suspended members: cannot borrow new books; can return and pay fine; status auto-restored on clearance.

### 4.5 Library Clearance at Exit

Library NOC required before:
- Student checkout from hostel (Module 28)
- Transfer Certificate issuance (Module 39)
- Staff full-and-final settlement (Module 27)

NOC logic: no books outstanding + no fines outstanding → NOC auto-issued. If either pending → NOC blocked; librarian notified.

### 4.6 Member Borrowing History

Full issue/return history stored per member:
- Book title, accession number, issue date, due date, return date, fine paid
- Student can view own history in app (last 3 years)
- Faculty can view own history
- Librarian can view any member's history (audit-logged access)
- History used for reading analytics

---

## 5. Issue & Return Operations

### 5.1 Issue Workflow

```
Librarian scans member card (or searches by name/ID)
  → Member validation checks:
      ✓ Member status = Active?
      ✓ Borrowing limit not exceeded?
      ✓ No suspension?
      ✓ No fine outstanding above threshold?
  → Librarian scans book barcode / RFID
  → Book validation checks:
      ✓ Copy status = Available?
      ✓ Not reference-only?
      ✓ Not restricted (if student)?
  → Issue recorded:
      issue_date = today
      due_date = today + loan period (holidays excluded from Module 05)
  → Due date notification sent to member (app + SMS)
  → Copy status → Issued
```

### 5.2 Due Date Calculation

- Loan period in calendar days
- Holidays from Module 05 academic calendar are excluded (due date shifted forward if it falls on holiday)
- Semester break: if due date falls in declared break, automatically extended to first working day after break
- Staff: Sunday not excluded (staff are full-time members)

### 5.3 Return Workflow

```
Librarian scans book barcode
  → System retrieves issue record
  → Due date check:
      If returned on or before due date → no fine
      If returned after due date → fine calculated:
          Fine = (return_date − due_date) × daily_rate
          (capped at replacement cost if cap enabled)
  → If fine > 0:
      Fine displayed; member pays via app (Module 25) or cash
      Fine receipt generated
  → Copy condition checked:
      If damaged → damage charge assessed
      If lost → replacement cost charged
  → Return recorded; copy status → Available (or Damaged/Lost)
```

### 5.4 Fine Calculation

| Scenario | Fine |
|----------|------|
| On time | ₹0 |
| 1–7 days late | ₹1/day (student); ₹2/day (staff) — configurable |
| 8–30 days late | Same daily rate |
| > 30 days | Same rate; fine cap at replacement cost |
| Lost | Replacement cost (purchase price or fixed rate ₹200 minimum) |
| Damaged | Cost of repair or replacement (librarian assessed) |

Fine cap: configurable per institution. Fine cannot exceed replacement cost of book.

### 5.5 Fine Waiver

Librarian can waive fine (partial or full) with mandatory reason:
- Medical leave covering due date
- Exam period grace
- Institutional policy (founder's day amnesty)
- Error in issue (system or librarian mistake)

Waiver logged: librarian name, reason, amount waived, date. Waiver requires Chief Librarian approval if amount > configurable threshold.

### 5.6 Renewal

Member can renew via:
- Self-service (student/staff app) — one tap
- Librarian counter

Renewal validation:
- Renewal count < limit (1–3 per institution setting)
- No active reservation / hold by another member on same copy
- Member not suspended
- Book not recalled

On renewal: due date extended by full loan period from new date; renewal count incremented.

### 5.7 Reservation / Hold

- Member reserves a copy of a fully-issued title
- Reservation queue: FIFO
- On return: first member in queue notified ("Book you reserved is now available. Hold valid for 3 days.")
- If not collected in 3 days → queue moves to next member
- Max simultaneous reservations per member: configurable (default 3)

### 5.8 Book Recall

Librarian initiates recall when:
- Reserved demand is high (5+ reservations on a title)
- Faculty urgently needs a reference book

Recall notice sent to current borrower:
- "Please return [Title] within 3 days. This book is in high demand."
- Failure to return in 3 days → overdue fine waived but suspension triggered
- Recall log: reason, notified to, returned on

### 5.9 Inter-Library Loan (ILL)

Book borrowed from partner institution's library:
- ILL request: member name, title requested, partner library name
- Dispatch and receipt dates tracked
- ILL due date: per agreement with partner
- Fine if not returned on time: charged to member
- ILL lending (outgoing): book from our library lent to partner; tracked separately

### 5.10 Bulk Return (Semester End)

- 10 days before semester end: bulk reminder to all members with outstanding books
- Semester-end grace period: configurable (e.g., 5 days post-semester); fines suspended during grace
- After grace: fines resume; NOC blocked for pending returns
- Bulk return counter: librarian processes high-volume returns efficiently via barcode scanner queue

---

## 6. Digital Library & eResources

### 6.1 Digital Resource Catalogue

| Resource Type | Examples | Notes |
|--------------|----------|-------|
| eBook platforms | Elsevier, Springer, Wiley, Taylor & Francis | Licence seats tracked |
| INFLIBNET N-LIST | 6,000+ eJournals, 3,00,000+ eBooks | Institutional login credentials (reference) |
| Open access | arXiv, DOAJ, PubMed, Shodhganga | No licence cost; links catalogued |
| Video lectures | NPTEL, Swayam, MOOC platforms | Links catalogued by subject |
| Institutional repository | Student theses, faculty papers, scanned rare books | Stored in Cloudflare R2 |

### 6.2 INFLIBNET N-LIST Integration

- Institutional membership details stored (membership number, renewal date)
- Member activation: student/staff email registered with N-LIST
- Access link displayed in library section of student/staff app
- Renewal alert: 90/60/30 days before subscription expiry
- Usage log: login count per month tracked (if N-LIST API available)

### 6.3 eBook Issue & Concurrent Access

For licensed eBooks with seat-count restrictions:
- Issue same as physical: member requests access → seat allocated → access link activated for loan period
- Concurrent access limit enforced: 4th request when 3 seats occupied → member added to wait queue
- Wait notification: "Access available" push when seat freed
- Auto-return: access expires at loan period end (no action needed)
- Loan period for eBooks: configurable (default 7 days; auto-return)

### 6.4 Institutional Repository

Faculty publications, student theses, project reports, scanned rare books:
- Uploaded in-app (camera capture for physical scanning; PDF for digital)
- Stored in Cloudflare R2; accessible via OPAC search
- Metadata: author, guide, department, year, degree, abstract, keywords
- Access control: public (open access) / institutional only / restricted
- Shodhganga submission support: thesis metadata formatted for Shodhganga upload

### 6.5 Course Reading Lists (Faculty-Curated)

Faculty links books and digital resources to course syllabus (Module 15 integration):
- Each course can have a required reading list and a recommended reading list
- Required books: system checks copy count vs enrolled students; shortage flagged (see §11.1)
- Students see their courses' reading lists in library section of app
- Reading list visible in OPAC under course code search

### 6.6 Resource Expiry Tracking

| Resource | Expiry Type | Alert Days |
|----------|-------------|-----------|
| eJournal subscription | Annual | 90 / 60 / 30 |
| eBook platform licence | Annual | 90 / 60 / 30 |
| N-LIST membership | Annual | 90 / 60 / 30 |
| Digital newspaper | Monthly / Annual | 30 / 15 |
| Database subscription | Annual | 90 / 60 / 30 |

---

## 7. Acquisition & Budget Management

### 7.1 Book Requisition Workflow

```
Department head submits title requisition (in-app):
  → Title, author, ISBN, estimated price, quantity, justification
  → Librarian reviews: duplicate check, budget check
  → Approved → Purchase Order raised
  → PO sent to vendor (email via Module 37 or printed)
  → Delivery received → GRN raised → accession
```

### 7.2 Vendor Master

| Field | Detail |
|-------|--------|
| Vendor name | Book supplier / distributor |
| GST number | For invoice processing |
| Contact details | Name, phone, email |
| Credit terms | Net 30 / Net 60 / Advance |
| Performance rating | On-time delivery %; quality of supply |
| Empanelment date | When added; renewal if required |

### 7.3 Purchase Order

| Field | Detail |
|-------|--------|
| PO number | Auto-generated |
| Vendor | From vendor master |
| Line items | Title, author, ISBN, quantity, unit price, total |
| PO total | Sum of all line items |
| GST | Books: 0% GST (HSN 4901); stationery/periodicals: 12%/18% |
| Expected delivery date | Agreed with vendor |
| Status | Draft / Sent / Partially received / Fully received / Cancelled |

### 7.4 Goods Receipt Note (GRN)

On delivery:
- Librarian opens PO → records received quantities per title
- Condition check: any damaged copies noted; returned to vendor
- Short supply: partial delivery; PO remains open; reminder to vendor
- GRN triggers accession process for received copies

### 7.5 Accession Process

On GRN confirmation:
1. Each copy assigned accession number (next in sequence; year-prefixed)
2. Barcode/QR label generated → printed → affixed to book
3. Property stamp recorded (physical stamping by staff on title page + fore-edge)
4. Catalogue entry created (or copy added to existing title record)
5. Shelf location assigned
6. Copy status → Available

### 7.6 Budget Management

| Fund Type | Purpose |
|-----------|---------|
| Purchase fund | General book buying; approved annual budget |
| Periodicals fund | Journal and newspaper subscriptions |
| Digital resources fund | eBook platforms, databases |
| Binding fund | Repair and binding of worn books |
| Equipment fund | Library technology (scanners, RFID readers) |

Budget dashboard:
- Allocated vs committed (POs raised) vs consumed (GRNs completed) per fund
- Remaining balance per fund
- Over-budget alert before PO approved
- Year-end utilisation report (critical for government-aided institutions)

### 7.7 GST Treatment

| Item | HSN | GST Rate |
|------|-----|---------|
| Books (print) | 4901 | 0% |
| Periodicals / journals | 4902 | 0% |
| Children's picture books | 4903 | 0% |
| Stationery | 4820 | 12% |
| Library furniture | 9403 | 18% |
| Digital subscription (eBook platform) | 9984 | 18% |

GST on zero-rated items not claimed; on taxable items, input tax credit tracked (if institution is GST-registered).

### 7.8 Government Grant Books

Books received under RUSA, UGC development grants, state government schemes:
- Separate accession series prefix (e.g., G-2024-00001)
- Grant reference number stored per copy
- Utilisation certificate: summary of books received under grant with total value; generated on demand for submission to funding body
- Grant-funded books cannot be withdrawn without prior approval

### 7.9 Donation Register

| Field | Detail |
|-------|--------|
| Donor name | Individual or organisation |
| Donation date | Date received |
| Titles donated | List with condition |
| Acknowledgement letter | Auto-generated; sent via Module 37 (email) |
| Accession | Donated copies accession-numbered with source = "Donated" |

---

## 8. Periodicals & Serials Management

### 8.1 Journal Subscription Master

| Field | Detail |
|-------|--------|
| Journal title | Full name |
| Publisher | Publisher name |
| ISSN | Print ISSN + Online ISSN |
| Frequency | Weekly / Monthly / Quarterly / Annual |
| Subscription period | Start date to end date |
| Subscription cost | Annual cost (₹) |
| Budget fund | Periodicals fund |
| Vendor | Subscription agent name |
| Format | Print / Online / Both |

### 8.2 Issue Receipt Log

For each expected issue (computed from frequency):
- Expected receipt date range
- Received date (librarian marks on receipt)
- Volume, issue number, date on cover
- Status: Received / Missing / Claimed / Received late

Missing issue detection: if expected issue not marked received within 14 days of expected window → auto-flag as Missing → claim workflow triggered.

### 8.3 Missing Issue Claim

- System generates claim letter to publisher/vendor: journal name, ISSN, volume, issue, subscription reference
- Letter sent via Module 37 (email) or printed
- Claim follow-up: if no resolution in 21 days → escalate to vendor; credit note or replacement expected
- Missing issue log maintained for NAAC audit

### 8.4 Newspaper Register

Daily newspapers:
- Expected titles per day (e.g., The Hindu, Times of India, Eenadu)
- Librarian marks each title as Received / Missing each morning
- Missing: vendor complaint raised (in-app log + phone call note)
- Retention policy: current month in reading room; previous 3 months in bound format; older → disposed

### 8.5 Binding Schedule

- Journals bound volume-wise annually (after full year's issues received)
- Binding log: journal, volume, sent to bindery, returned date, cost
- Bound volumes shelved in stacks; catalogue updated with "Bound volume, available" status
- Binding budget tracked against binding fund

### 8.6 Current Journals Display

Reading room journal rack:
- Librarian marks which issues are currently on display (latest issue per title)
- OPAC shows "Current issue on display" status
- Previous issues: stored in back-issue file; searchable

### 8.7 Periodical Routing

High-demand journals routed to faculty for reading:
- Routing list: faculty names in sequence per journal
- Faculty member receives issue → reads → passes to next in list → final return to library
- Routing tracked; if not passed within 7 days → nudge notification
- Routing log maintained for NAAC (shows breadth of journal usage)

---

## 9. Fine & Fee Management

### 9.1 Fine Accrual

- Daily batch job runs at midnight: calculates overdue days for all unreturned books past due date
- Fine balance per member updated automatically
- Member sees outstanding fine in app (library section)
- Fine accrual stops when book returned; accrued fine due for payment

### 9.2 Fine Collection Flow

Member pays fine via:
- **In-app payment** (Module 25): online payment; receipt auto-generated
- **Cash at counter**: librarian records cash receipt; fine marked paid; receipt printed

Fine receipt:
- Member name, book title, issue date, due date, return date, days overdue, fine amount, amount paid
- Receipt number linked to Module 25 transaction

### 9.3 Fine Outstanding Block

- If fine outstanding > configurable threshold (e.g., ₹50): new book issue blocked
- Librarian sees alert at counter: "Member has outstanding fine of ₹X. Please clear before issue."
- Suspension: if overdue books > 3 titles for > 30 days → member suspended
- Suspension auto-lifts on return of all overdue books + fine payment

### 9.4 Annual Fine Amnesty

Principal can declare a fine amnesty (e.g., on institution anniversary, Republic Day):
- All outstanding fines waived as of amnesty date
- Members notified via Module 35
- Amnesty logged: date, declared by, total amount waived, number of members benefited
- Books must still be returned; amnesty only covers monetary fine, not suspension for unreturned books

### 9.5 Damage & Replacement Charges

| Damage Level | Charge |
|-------------|--------|
| Minor (coffee stains, minor torn pages) | ₹20–₹50 (librarian assessed) |
| Major (multiple pages torn, spine broken) | 50% of purchase price |
| Destroyed (cannot be repaired) | Full replacement cost |
| Lost | Full replacement cost (min ₹200) |

Charges raised as ad-hoc fee in Module 25; paid like any other fee. Receipt generated.

### 9.6 Library Membership Fee (Alumni/Guest)

- Alumni membership: annual fee (e.g., ₹500/year) invoiced via Module 25
- Guest membership: fixed fee for duration; invoiced at creation
- Renewal: annual; fee invoiced 30 days before expiry

---

## 10. NAAC, NIRF & Compliance Reporting

### 10.1 NAAC Criterion 4.2 — Auto-Computed Data

| NAAC Metric | Source in Module 30 |
|------------|---------------------|
| Total book titles | Distinct title count in catalogue |
| Total volumes | Sum of all copy records |
| Journals subscribed | Active journal subscriptions count |
| eJournals | Digital resource catalogue count (type = eJournal) |
| eBooks | Digital resource count (type = eBook) |
| Library budget (annual) | Budget allocation records |
| Books issued per year | Issue log count for academic year |
| Members who borrowed | Distinct members with ≥1 issue in year |
| Digital resource logins | Usage analytics from digital catalogue |
| New titles added in year | Acquisitions in academic year |

NAAC report generation: one-click export in NAAC format for each criterion point.

### 10.2 NIRF Library Data Export

NIRF requires library data under "Infrastructure and Learning Resources":
- Total library books, journals, e-resources
- Library budget (last 3 years)
- Seating capacity
- Working hours per week
- Usage statistics

Module 30 generates NIRF-formatted export (CSV/Excel) with all required fields auto-populated.

### 10.3 Annual Stock Verification

Process run once per year (typically in April/May during summer break):
1. Export expected inventory: all accession numbers with status = Available / Issued
2. Physical scan: librarian walks stacks with barcode scanner; scans each book on shelf
3. System generates mismatch report:
   - Found on shelf but not in system → data entry error to fix
   - In system as Available but not found on shelf → Missing; flag for investigation
4. Investigation period: 30 days; warden/security check if books misplaced
5. After investigation: confirmed missing → marked Lost in catalogue
6. Two consecutive years missing → write-off approved by Principal; asset written off

### 10.4 Write-Off Process

- Missing copies written off after due diligence
- Write-off register: accession number, title, value at cost, write-off date, approval
- Budget impact: written-off value noted for asset register
- NAAC audit: write-off register produced as evidence of stock management

### 10.5 Accession Register Export

- Standard government accession register format
- Fields: S.No., Accession No., Date of entry, Title, Author, Publisher, Edition, Year, Pages, Price, Source, Class No., Shelf location, Remarks
- Exportable per year; printable for audit

### 10.6 Library Utilisation Rate (NAAC KPI)

```
Utilisation Rate = Members with ≥1 book borrowed in year ÷ Total active members × 100
```

Target: > 60% utilisation (NAAC expectation for A-grade institutions). Dashboard shows real-time rate; librarian can see who has never borrowed → targeted outreach.

### 10.7 Anti-Theft Gate Log

- RFID gate at library exit: alarm triggers if uncheckd-out book passes
- Event log: timestamp, which RFID tag triggered alarm, security response
- Monthly review: patterns of alarm (genuine theft attempts vs system errors)
- Gate malfunction log: maintenance request raised

---

## 11. Smart Acquisition & Analytics (Strategic Features)

### 11.1 Course-Linked Copy Shortage Alert

When faculty updates required reading list (Module 15 integration):
- System checks: enrolled students in course vs available copies of required titles
- If copies < 30% of enrolled students → shortage flag raised to librarian
- Librarian sees: "Course [CS301] needs 45 copies of 'Operating System Concepts' by Silberschatz. Currently 8 copies available."
- One-click raise acquisition requisition from alert
- Prevents semester-start scramble for textbooks

### 11.2 Smart Acquisition from Search Analytics

- OPAC searches with 0 results or all-issued results logged
- When a keyword/title searched 20+ times in 30 days with no available copy → auto-raise acquisition suggestion
- Suggestion card: search term, count, suggested titles (from ISBN database or librarian input), demand priority
- Librarian approves → requisition auto-created
- Outcome: library buys what students actually need, not just what was traditionally stocked

### 11.3 Overdue Prediction (ML)

Model trained on historical issue data:
- Features: member type, member past overdue rate, book category, loan period, semester week
- Output: probability this specific issue will go overdue
- If probability > 70% → proactive reminder sent 3 days before due date (not just on due date)
- Reduces overdue rate by catching at-risk issues early
- Model retrains monthly; accuracy reported to Chief Librarian

### 11.4 Reading Habit Analytics Per Student

- Books issued per student per term computed
- Reading habit score: 0–100 (frequency × variety × on-time return)
- Students with score < 30 → counsellor (Module 32) and parent receive "low reading engagement" nudge
- Top readers: featured on library notice board (with student permission)
- "Top 5 books in your course this semester" auto-recommendation for low-reading students

### 11.5 Textbook Demand Forecasting

Each June, before semester starts:
- Algorithm inputs: enrolment by course + course reading lists (Module 15)
- Output: expected demand per title per course
- Compares demand vs current copy count
- Generates purchase priority list: titles with highest shortage rank first
- Exported as acquisition plan for librarian + Principal sign-off

### 11.6 Reading Streak Gamification

- Student borrows books consistently and returns on time → earns "Reader Streak" badge
- Streak categories: 5 books on-time = Bronze; 15 = Silver; 30 = Gold; 50 = Platinum
- Badges displayed on student profile (Module 07)
- Top readers listed on library notice board (digital, in-app)
- Annual "Best Reader" recognition at prize day (integration with institution events)

### 11.7 Library Seat Booking

Peak exam season seating management:
- Student books reading hall seat in advance (date + time slot)
- Seat map: visual layout; student picks seat
- Seat hold: reserved for 15 minutes from booking start time; released if student doesn't check in
- In-app QR scan at library gate: confirms seat booking
- Seat utilisation analytics: peak hours, popular seats, average occupancy %
- Librarian can open additional seating (adjacent room) when occupancy > 85%

### 11.8 Inter-Campus Book Sharing

For multi-campus institutions:
- If book not available at student's campus library → OPAC shows "Available at [Branch Name] Library"
- Student requests inter-campus transfer: librarian at originating campus dispatches; transit tracked
- Transit status: Dispatched / In transit / Received at destination / Issued to student
- Transfer log: date, from campus, to campus, book, driver/courier reference
- Reduces need to duplicate expensive titles across campuses

### 11.9 QR-Linked Study Notes

- Faculty can pin course notes or chapter summaries to a specific book's catalogue record
- Student scans book QR → sees "Study notes by [Faculty Name] for [Course]" in app
- Notes stored in Cloudflare R2; accessible only to enrolled course students
- Drives library usage: students visit library to access richer content

---

## 12. Staff & Operations

### 12.1 Library Staff Roles

| Role | Responsibilities |
|------|----------------|
| Chief Librarian | Policy, NAAC, budget, acquisitions, committee |
| Assistant Librarian | Cataloguing, OPAC management, digital resources |
| Library Assistant | Issue/return counter, shelving, periodicals |
| Library Attendant | Shelving, housekeeping, security support |
| IT support (shared) | RFID/barcode system, network connectivity |

### 12.2 Shift Management

| Shift | Timing | Staff |
|-------|--------|-------|
| Morning | 08:00–14:00 | 1 librarian + 1 assistant |
| Afternoon | 14:00–20:00 | 1 assistant + 1 attendant |
| Evening (extended hours) | 20:00–22:00 | 1 attendant (reading room only; no issue/return) |

Shift handover: in-app handover note (pending requests, issues to follow up, equipment status).

### 12.3 Librarian Daily Dashboard (KPI)

One-screen shift summary:
- Books issued today / returned today
- Overdue books total count
- Fines collected today (₹)
- New accessions today
- OPAC searches today
- Reservations pending
- Reading hall current occupancy
- Pending maintenance requests
- Compliance alerts (subscriptions expiring, stock verification due)

### 12.4 Library Orientation

Annual induction for new students:
- Session date, duration, librarian in-charge
- Topics: OPAC use, borrowing rules, digital resources, fine policy
- Attendance recorded (student IDs scanned)
- Post-orientation quiz (optional): 5 questions; completion tracked

### 12.5 Library Survey

Annual student satisfaction survey:
- Categories: Collection adequacy, Staff helpfulness, OPAC ease, Digital resources, Seating comfort, Cleanliness
- Rating 1–5 per category + open comment
- Results: average per category; year-on-year trend
- Action plan: librarian documents 3 improvements based on survey; reviewed next year

### 12.6 Grievance Log

Student/staff library complaints:
- Category: Long wait at counter / Book not on shelf / System error / Staff behaviour / Facilities
- Response committed within 48 hours
- Resolution tracked
- Repeat grievance patterns → systemic fix

---

## 13. Integration Map

| Module | Integration |
|--------|------------|
| Module 05 — Academic Calendar | Holiday calendar for due date calculation; semester dates for bulk return |
| Module 07 — Student Profile | Auto-create library member on enrolment; reading habit linked to profile |
| Module 08 — Staff Management | Auto-create library member on joining; staff exit triggers clearance check |
| Module 15 — Syllabus & Curriculum | Course reading lists linked; copy shortage alerts |
| Module 25 — Fee Collection | Fine collection, damage charges, membership fees, acquisition invoices |
| Module 27 — Staff Payroll | Library clearance required for F&F settlement |
| Module 28 — Hostel Management | Library NOC required at hostel checkout |
| Module 32 — Counselling | Low reading habit score triggers counsellor referral |
| Module 35 — Notifications | Due date reminders, overdue alerts, reservation notifications, recall notices |
| Module 37 — Email (AWS SES) | Vendor PO emails, missing issue claims, donation acknowledgements |
| Module 39 — Certificates & TC | Library NOC required before TC issuance |
| Module 42 — DPDPA & Audit Log | Member data access, borrowing history access audited |

---

## 14. Data Model (Key Tables)

```
library_units
  id, tenant_id, name, type, classification_system, has_rfid,
  seating_capacity, inflibnet_membership_no, inflibnet_expiry,
  chief_librarian_id, created_at

library_titles
  id, unit_id, title, subtitle, authors, publisher, edition,
  year_published, isbn, ddc_class, ddc_subclass, subject_tags,
  language, series_name, series_volume, pages, illustrated,
  acquisition_source, reference_only, restricted, rare_book,
  insured_value, material_type, created_at

library_copies
  id, title_id, accession_no, barcode, rfid_tag, shelf_rack,
  shelf_number, shelf_position, condition, status, acquisition_date,
  purchase_price, vendor_id, budget_head, grant_ref, donor_name,
  withdrawn_on, withdrawal_reason, disposal_method

library_members
  id, student_id, staff_id, member_type, member_card_no,
  borrowing_limit, loan_period_days, max_renewals, status,
  joined_on, valid_until, fine_outstanding, suspended_on,
  suspension_reason, created_at

library_issues
  id, member_id, copy_id, issue_date, due_date, return_date,
  renewal_count, fine_accrued, fine_paid, fine_waived,
  waiver_reason, waiver_by, condition_on_return,
  damage_charge, loss_charge, issued_by, returned_by

library_reservations
  id, member_id, title_id, reserved_on, queue_position,
  notified_at, collected_by_date, status

library_fines
  id, issue_id, member_id, fine_type, amount, days_overdue,
  raised_on, paid_on, payment_ref, waived_on, waiver_by,
  waiver_reason

library_acquisitions
  id, unit_id, requisition_by, requisition_date, title,
  author, isbn, quantity, estimated_price, justification,
  status, po_id, grn_id

library_purchase_orders
  id, unit_id, po_number, vendor_id, po_date, total_amount,
  gst_amount, expected_delivery, status

library_po_items
  id, po_id, title_id, quantity_ordered, unit_price,
  quantity_received, grn_date

library_budget
  id, unit_id, academic_year, fund_type, allocated,
  committed, consumed, remaining

library_journals
  id, unit_id, journal_title, publisher, issn_print, issn_online,
  frequency, subscription_start, subscription_end, cost,
  vendor_id, format, budget_head, status

library_journal_issues
  id, journal_id, volume, issue_no, cover_date, expected_by,
  received_on, status, missing_claim_sent, claim_date

library_digital_resources
  id, unit_id, resource_type, name, platform, access_url,
  licence_seats, subscription_start, subscription_end,
  cost, budget_head, status

library_opac_searches
  id, unit_id, search_term, search_type, result_count,
  available_copies, searched_by, searched_at

library_seat_bookings
  id, unit_id, member_id, booking_date, slot_start, slot_end,
  seat_id, status, checked_in_at

library_stock_verifications
  id, unit_id, verification_year, started_on, completed_on,
  total_expected, total_scanned, missing_count, found_extra,
  conducted_by, status

library_write_offs
  id, copy_id, write_off_date, reason, approved_by,
  cost_value, asset_impact_noted

library_ill_requests
  id, unit_id, member_id, direction, partner_library,
  title_requested, dispatched_on, received_on, due_date,
  returned_on, status

library_compliance_docs
  id, unit_id, doc_type, reference_no, issue_date, expiry_date,
  alert_90, alert_60, alert_30, status
```

---

## Cross-Module References

- **Module 05**: Holiday dates for due date calculation; semester close dates for bulk return grace — read-only
- **Module 07**: Student enrolment triggers member creation; reading score feeds student profile — read + write
- **Module 08**: Staff joining triggers member creation; staff exit triggers clearance check — read + event
- **Module 15**: Course reading lists linked to catalogue; copy shortage alert raised — read-only
- **Module 25**: Fines, damage charges, membership fees, acquisitions invoiced — write via Module 25 API
- **Module 27**: Library NOC required before F&F settlement — event write
- **Module 28**: Library NOC required before hostel checkout — event write
- **Module 32**: Low reading habit score triggers counsellor referral — event write
- **Module 35**: All due date, overdue, reservation, recall notifications dispatched — write
- **Module 37**: Vendor POs, missing issue claims, donation acknowledgements emailed — write
- **Module 39**: Library NOC required before TC issuance — event write
- **Module 42**: Member data access, borrowing history, fine records audited — write

---

*Module 30 complete. Next: Module 31 — Admission & Enquiry CRM.*
