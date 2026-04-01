# Module 25 — Fee Collection & Receipts

## 1. Purpose

Receive, record, receipt, reconcile, and refund all fee payments across every institution type on
EduForge — schools (CBSE/state board/KVS/NVS/government), colleges (UGC/AICTE/university-affiliated),
coaching institutes (JEE/NEET/UPSC/Banking/SSC), skill centres (NCVT/PMKVY/DDU-GKY), and online
programmes. Enforce Section 269ST cash limit (Rs. 2 lakh hard block), GST compliance (SAC 9993,
18% coaching, exempt education), UGC refund rules, coaching 48-hour refund, DPDPA 2023 data
handling, 7-year immutable audit retention, SFT reporting (Rule 114E), Section 80C annual
certificate generation, and full passthrough remittance tracking for board exam fees. Module 25
owns demand generation, payment posting, receipt issuance, refund processing, and reconciliation
only. Module 24 owns structure and configuration. Module 26 owns defaulter tracking and recovery.
Module 57 owns payment gateway configuration (BYOG).

---

## 2. Module Boundaries

### 2.1 What This Module Owns
- Fee demand generation (per student, per instalment, per academic year)
- All payment mode handling (cash, cheque, DD, NEFT, UPI, gateway, NACH, BBPS, virtual account)
- Receipt generation and delivery
- Student fee ledger (Dr/Cr postings)
- Refund processing and credit notes
- Daily, monthly, and annual reconciliation
- GST invoice and credit note generation
- Chart of accounts / GL mapping
- Year-end demand lock and transfer to Module 26

### 2.2 What This Module Reads (Never Writes Back)
| Source | Data Read |
|---|---|
| Module 24 | Instalment schedule, due dates, head amounts, approved concessions, late fee config |
| Module 07 | Student admission category, class, section, RTE flag, scholarship flag |
| Module 09 | Parent/guardian details, payment split (court order), NRI flag |
| Module 28 | Hostel room assignment — drives hostel demand amount |
| Module 29 | Transport zone assignment — drives transport demand amount |
| Module 31 | Admission enquiry → provisional fee at CRM stage |

### 2.3 What This Module Writes (Other Modules Read)
| Destination | Data Written |
|---|---|
| Module 26 | Outstanding balance after each posting; year-end locked outstanding |
| Module 39 | Fee clearance flag (no-dues prerequisite for TC / certificate) |
| Module 21 | Fee clearance flag (result hold release) |
| Module 19 | Fee clearance flag (hall ticket release) |
| Module 30 | Fee clearance flag (library card release) |

---

## 3. Fee Demand Generation

### 3.1 Automatic Demand Creation
- Demand generated per student per fee head per instalment at academic year start (batch process)
- Demand entity: student_id, fee_head_id, instalment_number, amount, due_date, academic_year_id,
  branch_id, concession_id (if any), scheme_id (if any), is_passthrough, status
- Demand status lifecycle: `DRAFT → ACTIVE → PARTIALLY_PAID → PAID → WAIVED → CANCELLED → LOCKED`
- Only one ACTIVE demand per student per head per instalment per academic year

### 3.2 Demand Calculation Rules
| Scenario | Rule |
|---|---|
| Full-year student | All instalments generated at year start per Module 24 schedule |
| Mid-year admission | Pro-rata from join month only; past months not demanded |
| Batch transfer (coaching) | Recalculate from transfer date; old batch demands cancelled |
| Day scholar → Hosteller | Hostel demand raised from room assignment date; Module 28 trigger |
| Category change | Fee structure re-applied; difference demand raised or credit issued |
| Student transfers out (TC) | All future demands suppressed immediately on TC issue date |
| Sibling leaves institution | Sibling discount on remaining student auto-recalculated; demand revised |

### 3.3 RTE & Government Scheme Demands
- RTE students: tuition demand = Rs. 0 (zero); other heads (transport, exam) as applicable
- Government reimbursement amount tracked separately in passthrough ledger
- PM-POSHAN eligible: food/meal charge demand = Rs. 0; govt allocation tracked
- NSP / state scholarship: demand reduced by sanctioned scholarship amount; balance demand on student
- PMKVY / DDU-GKY: full fee demand = Rs. 0; government pays institution directly via scheme
- OBC/SC/ST reimbursement model A: institution raises full demand → student pays → state reimburses institution
- OBC/SC/ST reimbursement model B: state pays directly → zero demand on student
- Both models supported; institution selects model during onboarding (Module 04)

### 3.4 Passthrough Demands
- Board exam fees (CBSE, NTA, State Board, University exam fee): `is_passthrough = TRUE`
- Passthrough demands shown separately in student account; not included in institution revenue
- Passthrough ledger: amount collected vs amount remitted to board; variance flagged
- Passthrough authority: CBSE / NTA / State Board / University — stored for reconciliation

### 3.5 Demand Revision
- Mid-year demand revision: Accountant proposes → Principal approves → system creates revised demand
- Old demand archived (CANCELLED status); new demand ACTIVE; both accessible for audit
- Revision reason mandatory; audit log immutable
- Fee revision communication: all affected parents notified via WhatsApp + in-app; old vs new amount shown

### 3.6 Fee Escalation (Annual Increase Clause)
- Institutions with annual % increase clause in admission letter (common in private schools)
- System stores escalation % in Module 24 fee structure
- On academic year rollover: new demands auto-calculated with escalation applied
- Parent notification: "Fee revised by X% for 2026-27 as per admission terms"

---

## 4. Payment Modes

### 4.1 Supported Payment Modes
| Mode | Code | Where Used | Notes |
|---|---|---|---|
| Cash | CASH | Counter only | Section 269ST Rs. 2L hard block |
| Cheque — Local | CHQ_LOCAL | Counter | 2-3 day clearing |
| Cheque — Outstation | CHQ_OUT | Counter | 15-21 day clearing |
| Demand Draft | DD | Counter | Validity check mandatory |
| NEFT | NEFT | Counter / bank | UTR number captured |
| RTGS | RTGS | Counter / bank | Min Rs. 2 lakh; UTR captured |
| IMPS | IMPS | Counter / online | 24×7; UTR captured |
| UPI (manual) | UPI | Counter / online | Transaction reference captured |
| UPI AutoPay | UPI_AUTO | Auto-debit | NPCI recurring mandate |
| Card — Debit | CARD_D | Counter POS | Last 4 digits + approval code |
| Card — Credit | CARD_C | Counter POS | Last 4 digits + approval code |
| Payment Gateway | PG | Online | Module 57 (Razorpay/PhonePe/PayU) |
| Virtual Account | VACT | Auto-reconcile | Bank-level per-student account |
| NACH / ECS | NACH | Auto-debit | Physical or e-NACH |
| BBPS | BBPS | Parent self-service | Institution as BBPS biller |
| Education Loan | ELOAN | Counter | Bank-to-institution disbursement |
| Scholarship / DBT | SCHOL | Manual posting | Accountant posts on receipt |
| SWIFT (NRI/foreign) | SWIFT | Counter | FEMA compliance flag |
| Sponsor / CSR | SPONSOR | Counter / online | Receipt to sponsor |
| Sibling credit | SIB_CR | Auto-applied | Overpayment from sibling account |
| Waiver | WAIVER | System | Settles demand without payment |

---

## 5. Counter Collection

### 5.1 Multi-Counter Setup
- Institution configures fee counters: name, branch, type (main / hostel / transport / exam)
- Each counter assigned to one or more cashiers
- Cashier login: collection tagged to cashier_id; cashier cannot view other cashiers' sessions

### 5.2 Shift Management
- Shift open: cashier enters opening balance (cash denomination-wise)
- All transactions during shift tagged to shift_id
- Shift close: cashier counts cash denomination-wise; system compares with expected; variance flagged
- Shift handover receipt: cashier hands cash + summary to Accountant; both sign; stored in system
- Cash above counter threshold (institution-configures, e.g., Rs. 50,000): alert to Accountant to collect

### 5.3 Cheque & DD Handling
| Field | Cheque | DD |
|---|---|---|
| Number | Cheque number | DD number |
| Date | Cheque date | Issue date |
| Bank | Drawer's bank | Issuing bank |
| Branch | Drawer's branch | Issuing branch |
| Amount | Face value | Face value |
| MICR | MICR code | — |
| Validity | 3 months from date | 3 months from date |
| Clearing type | Local / Outstation | — |
| Expected clearance | 2–3 days (local); 7–10 days (outstation) | 2–3 days |

- System flags cheques / DDs approaching 3-month validity without clearance
- Batch cheque deposit: multiple cheques → one deposit slip; deposit slip number logged after bank deposit

### 5.4 Card Collection
- POS terminal ID stored; approval code captured
- Last 4 digits of card only (PCI-DSS; no full card number ever stored)
- MDR rate configured per card type; absorbed by institution or charged to parent (institution config)

### 5.5 Inter-Branch Payment
- Student of Branch A pays at Branch B counter (common — parent works near Branch B)
- System records: paying_branch_id ≠ student_branch_id
- Inter-branch reconciliation entry auto-created: Branch B owes Branch A
- Finance Head sees inter-branch payable/receivable in reconciliation report

### 5.6 Offline Collection (No Internet / Power Outage)
- Pre-printed paper receipt books issued by system; each book has a unique serial range
- Book issuance logged: cashier_id, serial range start–end, issue date
- Collection continues on paper during outage
- On reconnect: cashier batch-enters paper receipts; backdated to actual collection time
- Supervisor (Accountant) verifies paper stub vs digital entry before posting
- Discrepancy flagged; unresolved discrepancy escalated to Principal
- Used book returned to Accountant; serial completion verified

---

## 6. Post-Dated Cheque (PDC) Management

### 6.1 PDC Register
- Institution accepts full-year PDCs at admission time (common in CBSE schools)
- PDC record: student_id, cheque_number, bank, branch, date, amount, instalment_id, status
- Status: `RECEIVED → PENDING_PRESENTATION → PRESENTED → CLEARED → BOUNCED → REPLACED → STALE`
- All PDCs for a student visible to Accountant in one view with status

### 6.2 Presentation Workflow
- System alert to Accountant 3 days before each PDC presentation date
- Accountant presents cheque to bank; updates status to PRESENTED
- Provisional receipt issued on PRESENTED status (marked PROVISIONAL)
- On bank clearance confirmation: status → CLEARED; provisional receipt converted to FINAL receipt
- On bounce: status → BOUNCED; provisional receipt CANCELLED; bounce charge demand raised

### 6.3 Stale Cheque Handling
- Cheque becomes stale 3 months from cheque date (negotiable instrument law)
- System flags PDC 30 days before staleness: "PDC for Rs. X (instalment 4) becomes stale on DD MMM"
- Accountant requests replacement from parent; old PDC cancelled; new PDC collected
- Stale PDC not presented; parent prompted to issue fresh cheque

### 6.4 Re-presentation
- After bounce, institution may present cheque once more (second presentation) before raising charges
- Re-presentation flag: configurable per institution (default: one re-presentation allowed)
- Re-presentation attempt logged; if bounce again → bounce charges mandatory

### 6.5 Bounce Count Tracking
- Bounce count tracked per student per academic year
- 2+ bounces (configurable): cheque/DD payment mode automatically blocked for that student
- Block override: Principal approval; documented reason

---

## 7. Online Payment & Payment Gateway

### 7.1 Gateway Architecture
- Module 25 never calls a gateway directly
- All gateway calls routed through Payment Orchestration Layer (Module 57)
- Module 57 exposes: `POST /payment/initiate` → returns payment_session_id + checkout_url
- Module 57 exposes: `GET /payment/status/{session_id}` → PENDING / SUCCESS / FAILED
- Module 25 only knows: payment succeeded or failed — never which gateway was used
- Benefit: swap/add gateways in Module 57 without any change to Module 25

### 7.2 Payment Initiation
- Parent selects demands to pay (one or multiple heads, one or multiple instalments)
- Checkout created: demand_ids[], total_amount, student_id, parent_id, expiry (configurable; default 72 hours)
- QR code: generated per student per instalment at demand creation; amount pre-filled; parent scans from app
- Payment link: Accountant generates manually; shared via WhatsApp; link expires in 72 hours (configurable)
- Demand aggregation: parent with multiple children → single checkout covering all children's dues
- Receipts after payment: split per child per demand; combined payment, individual receipts

### 7.3 Webhook & Auto-Reconciliation
- Gateway webhook → idempotency check (transaction_id already processed?) → post payment → generate receipt → notify parent
- Webhook retry: SQS retry queue; max 5 attempts with exponential backoff
- Duplicate payment detection: same transaction_id from gateway → reject second posting; parent notified
- Webhook failure (gateway sends no webhook): polling fallback every 5 minutes for 30 minutes; then manual flag
- Failed payment: attempt logged (student_id, amount, timestamp, failure_reason, gateway_code); parent sees retry option in app

### 7.4 Gateway Reconciliation
- Settlement files auto-parsed: Razorpay (CSV), PhonePe (Excel), PayU (CSV)
- Each settlement transaction matched on: gateway_transaction_id ↔ system receipt_id
- Unmatched on gateway (money received, no receipt): alert Finance Head — "ghost transaction"
- Unmatched on system (receipt issued, money not received): alert Finance Head — "unconfirmed receipt"
- MDR deduction: system tracks gross collected + MDR charged; net settlement = gross − MDR
- Daily settlement report: expected settlement (T+1/T+2) vs actual bank credit

### 7.5 MDR Handling
| Option | Treatment |
|---|---|
| Institution absorbs MDR | Parent pays face value; MDR deducted from settlement; institution books as expense |
| MDR passed to parent | MDR % added at checkout; shown clearly before payment; on receipt as "Payment processing fee" |
| Digital payment incentive | Institution offers Rs. X discount for online payment to drive adoption; applied at checkout |

---

## 8. Virtual Account Number (Bank-Level Auto-Reconciliation)

### 8.1 How It Works
- Each student assigned a unique virtual bank account number via bank API (HDFC / ICICI / Kotak / Axis)
- Virtual account maps to institution's pooled bank account; bank routes credit by virtual account number
- Parent does NEFT / RTGS / IMPS to student's virtual account from any bank — no EduForge login needed, zero MDR
- Bank sends credit notification → system auto-reconciles → receipt generated → parent notified via WhatsApp
- Zero human intervention; no Accountant action needed

### 8.2 Setup & Lifecycle
- Virtual account provisioned at student enrolment (Module 07 trigger)
- One virtual account per student per academic year
- Account closed at year-end; new account for new academic year
- NRI parents pay via SWIFT to virtual account; FEMA compliance flag raised
- Corporate sponsors, government DBT disbursements also routed via virtual account

### 8.3 Scale Impact
- 1,000-student institution: virtual accounts eliminate ~80% of counter transactions
- No MDR on NEFT/IMPS payments (vs 1–2% on card/gateway)
- 1,000 students × Rs. 40,000 annual fee × 1.5% MDR saved = Rs. 6 lakh/year MDR saving per institution
- Setup via Module 57 (bank API config); Module 25 handles receipt + reconciliation

---

## 9. UPI AutoPay & NACH Mandate

### 9.1 UPI AutoPay (NPCI Recurring)
- Parent sets up mandate once on Google Pay / PhonePe / any UPI app
- System triggers debit request on due date; bank debits and confirms
- Best for monthly fee ≤ Rs. 15,000 (UPI transaction limit); fast setup; no physical form
- Mandate record: mandate_id, parent_id, student_id, amount, frequency, start_date, end_date, status

### 9.2 e-NACH (Digital Mandate)
- Parent signs mandate digitally via Aadhaar OTP or net banking
- Institution submits to NPCI via bank API; mandate_id returned
- Covers amounts above UPI AutoPay limits; suitable for hostel + tuition combined

### 9.3 Physical NACH
- Paper form signed by parent; submitted to bank; mandate_id returned after 3-7 days processing
- Used where parent is not digitally enabled (common in rural/semi-urban institutions)

### 9.4 Failure Handling
| Failure Type | System Action |
|---|---|
| Insufficient funds | NPCI returns failure code; treat as non-payment; WhatsApp to parent; Module 26 flag |
| Mandate revoked | Detected on next debit attempt; Accountant notified; parent asked to renew |
| Bank technical failure | Retry next working day; if 2nd failure → non-payment treatment |
| Mandate expired | System alert 30 days before expiry; parent asked to renew |

---

## 10. BBPS Integration

### 10.1 Institution as BBPS Biller
- Institution registered on BBPS (Bharat Bill Payment System) via Module 57
- Parents pay from any UPI app (Google Pay, PhonePe, Paytm, any bank app) by searching institution name
- No EduForge login required for parent — massive reach in Tier 2/3/4 cities and rural areas
- BBPS sends payment notification with student reference → system auto-reconciles → receipt generated

### 10.2 Student Reference on BBPS
- Parent enters student's admission number or registered mobile number as bill reference
- System validates reference; shows student name + pending amount for parent confirmation
- Parent confirms → payment processed → auto-reconciled in Module 25

### 10.3 BBPS Reconciliation
- BBPS settlement file received daily
- Auto-matched on BBPS transaction ID + student reference
- Unmatched transactions flagged to Accountant for manual resolution
- BBPS MDR: typically 0.5-1%; handled same as gateway MDR (Section 7.5)

---

## 11. Receipt Generation & Format

### 11.1 Receipt Entity
- receipt_id, receipt_number, student_id, academic_year_id, branch_id, cashier_id, payment_mode,
  payment_reference, total_amount, receipt_date, status, is_provisional, is_duplicate, gstin (coaching),
  created_at, created_by
- Status: `PROVISIONAL → FINAL → CANCELLED | DUPLICATE (parallel state)`

### 11.2 Receipt Number Format
- Format configurable: e.g., `{BRANCH_CODE}/{YEAR}/{SERIES}/{SEQUENCE}`
- Example: `RCP/2025-26/00001` or `DWK-FEE/25-26/04821`
- Separate receipt series per branch (multi-branch institutions)
- Sequence: institution-level; never reset mid-year; no gaps allowed

### 11.3 GST Treatment by Institution Type
| Institution Type | GST Treatment | Receipt Format |
|---|---|---|
| School (CBSE/State Board) | Exempt — Section 9 CGST Act | No tax lines; exemption stated |
| College (UGC/AICTE) | Exempt | No tax lines; exemption stated |
| Coaching (JEE/NEET/UPSC/Banking) | 18% GST (SAC 9993) | Full tax invoice with GSTIN, taxable value, CGST 9% + SGST 9% or IGST 18% |
| Coaching — NRI student | 18% IGST (inter-state) | IGST invoice |
| Skill centre (PMKVY) | Exempt (govt scheme) | No tax lines |
| ITI (NCVT) | Exempt | No tax lines |

### 11.4 Receipt Components
**All institution types:**
- Institution name, logo, address, phone, email
- Branch name (if multi-branch)
- Receipt number, receipt date
- Student name, admission number, class/section/batch
- Academic year
- Payment mode + reference (cheque number / UTR / transaction ID)
- Table: fee head | amount | concession | net amount
- Total amount paid (in figures and words)
- Cashier name + employee ID
- Digital signature (institution's authorized signatory)
- "Thank you for your payment"

**Coaching only — additional:**
- Institution GSTIN
- SAC code: 9993
- Taxable value per head
- CGST / SGST / IGST amount
- Total tax
- Total invoice value
- "This is a Tax Invoice under CGST Act 2017"

**Passthrough fee — on receipt:**
- Passthrough section separate from regular fee
- "Collected on behalf of [CBSE/NTA/University] — not institution revenue"
- Passthrough amount excluded from institution total

### 11.5 Special Receipt Types
| Type | Trigger | Label |
|---|---|---|
| Provisional | Cheque / DD deposited; not yet cleared | "PROVISIONAL — subject to realisation" |
| Final | Cheque cleared / online payment confirmed | Standard receipt |
| Duplicate | Re-issued on request | "DUPLICATE — Original receipt No. XXXX dated DD/MM/YYYY" |
| Zero-amount | RTE / fully waived / fully scheme-covered | Rs. 0 receipt; waiver/scheme reference shown |
| Advance receipt voucher | Advance fee for next year collected | "ADVANCE RECEIPT — will be converted to tax invoice on [date]" |
| Credit note | Refund issued (coaching GST reversal) | GST credit note format; references original invoice |

### 11.6 Receipt Delivery
- WhatsApp: immediate on generation (MSG91 / Module 36)
- In-app notification: immediate
- Email: optional; parent preference
- PDF: WeasyPrint; stored on Cloudflare R2; download link valid 30 days (one of only 2 PDFs in the platform)
- Counter reprint: Accountant can reprint; reprints are NOT duplicate receipts (no audit flag)

### 11.7 Receipt Cancellation
- Requester: Accountant
- Approver: Principal (mandatory for all cancellations)
- Reason: mandatory (minimum 20 characters)
- Effect: original receipt status → CANCELLED; payment posting reversed; demand reopened
- Original receipt preserved in CANCELLED state — never deleted; never overwritten
- New payment entry required if collection to be re-recorded
- Cancellation logged: actor, approver, reason, timestamp, IP — immutable

### 11.8 Duplicate Receipt
- Accountant issues on parent request (lost receipt)
- Marked DUPLICATE clearly on face
- Original receipt number and date shown
- Issuance logged: requested by, issued by, timestamp

### 11.9 Zero-Amount Receipt
- Auto-generated when demand is settled via waiver / scheme / RTE — no payment received
- Purpose: audit completeness; prevents "ghost income" queries (inspector asks: "no receipt for this student?")
- Zero receipt references: waiver_id or scheme_id
- Delivered to parent in-app (not WhatsApp — no payment to confirm)

### 11.10 Receipt Branding & Language
- Institution customizes: header (logo + name + address), footer (authorized signatory), watermark
- Language: English default; Hindi and regional language option per institution (receipt text translated)
- QR code on receipt: parent scans to verify authenticity on EduForge platform (tamper detection)

---

## 12. Fee Ledger — Student Account

### 12.1 Ledger Structure
- One ledger per student per academic year
- Ledger row types:
  - `DEMAND` — Dr (amount owed by student)
  - `PAYMENT` — Cr (amount paid)
  - `WAIVER` — Cr (amount waived off)
  - `SCHEME_CREDIT` — Cr (scholarship / govt scheme)
  - `ADVANCE_CREDIT` — Cr (overpayment from earlier)
  - `REFUND` — Dr (amount refunded back)
  - `ADJUSTMENT` — Dr/Cr (correction entry; dual approval)
  - `PASSTHROUGH_DEMAND` — Dr (board exam fee)
  - `PASSTHROUGH_PAYMENT` — Cr (board exam fee paid)

### 12.2 Balance Calculation
```
Outstanding = Σ DEMAND − Σ (PAYMENT + WAIVER + SCHEME_CREDIT + ADVANCE_CREDIT) + Σ REFUND
```
- Calculated head-wise: tuition outstanding ≠ transport outstanding
- Aggregate outstanding = sum of all head-wise outstanding
- Passthrough outstanding shown separately from institution outstanding

### 12.3 Advance Credit
- Parent pays more than demanded: excess amount held as credit balance
- Auto-applied to next instalment demand on due date
- Manual application: Accountant can apply credit to a specific demand ahead of due date
- Credit balance refund: parent requests → Accountant proposes → Principal approves → refunded via original mode

### 12.4 Liability Heads (Caution / Security Deposit)
- Caution deposit, security deposit, lab breakage deposit: `is_liability = TRUE`
- Separate liability ledger: not shown as fee income; not included in collection reports
- Liability refund on no-dues clearance (Module 39 prerequisite)
- Liability balance shown to parent separately: "Refundable deposit: Rs. X"

### 12.5 Account Statement
- Full ledger available to parent / student anytime in-app
- Date range filter; head filter; type filter
- In-app table only — not PDF; shareable as a link
- Accountant view: all students' ledgers; filter by class, section, outstanding amount, overdue days
- Accountant can add internal notes to ledger (visible to staff only; not to parent)

---

## 13. Instalment & Partial Payment Rules

### 13.1 FIFO Enforcement
- Default: system applies payment to oldest outstanding demand first
- Example: instalment 1 outstanding + instalment 2 due → payment applied to instalment 1 first
- Institution can disable FIFO (coaching institutes often allow out-of-order payment)
- Out-of-order: cashier selects specific demand to apply payment against; reason logged

### 13.2 Partial Payment
- Allowed / not allowed: configured per fee head in Module 24
- If allowed: minimum partial threshold configurable (e.g., minimum 50% of instalment or Rs. 500)
- Partial receipt shows: "Paid Rs. X against demand of Rs. Y for [Head]. Balance Rs. Z."
- Balance demand stays ACTIVE with updated amount

### 13.3 Advance Payment
- Parent pays future instalment before due date
- Demand status updated to PAID; due date remains original (for report accuracy)
- Parent notified: "Advance payment accepted. Instalment 3 (due 1 Oct) is now cleared."

### 13.4 Multi-Instalment Single Payment
- Parent pays 2 or more instalments in one transaction
- Single receipt generated covering all instalments (receipt table has one row per instalment)
- All covered demands marked PAID

### 13.5 Multi-Child Single Payment
- Parent with 2+ children in same institution: single checkout covering all children's dues
- Single payment transaction splits into individual postings per child per demand
- Individual receipts generated per child; parent sees all receipts in-app
- Each receipt referenced to the combined payment_reference

---

## 14. Concession & Waiver at Collection Stage

### 14.1 Pre-Approved Concessions (from Module 24)
- Concession already approved in Module 24 auto-applied to demand at generation stage
- Accountant sees reduced amount at collection; no further action needed
- Concession source tagged on receipt: "Sibling concession — 10% on tuition"

### 14.2 Ad-Hoc Waiver at Collection Stage
- Accountant proposes waiver: student_id, demand_id, waiver_amount, reason
- Principal approves (mandatory for any waiver, no exception)
- Amount threshold for Management approval: institution configures (e.g., > Rs. 5,000 → Management also approves)
- Approved waiver: demand reduced; zero-amount receipt or adjusted receipt generated
- Waiver reversal: Finance Head + Management; rare; full audit trail

### 14.3 Late Fee Waiver
- Separate from main fee waiver
- Same approval chain (Accountant → Principal)
- Late fee exemption codes: MEDICAL / NATURAL_DISASTER / SYSTEM_DOWNTIME / MANAGEMENT_DISCRETION
- Exemption reason + supporting document reference logged

### 14.4 RTE Waiver
- System-enforced: cashier sees Rs. 0 tuition for RTE student; cannot collect
- No override by any role including Platform Admin (regulatory mandate)
- State reimbursement claim report: list of RTE students + fee foregone; generated for state submission

---

## 15. Late Fee Collection

### 15.1 Late Fee Calculation
- Auto-calculated per Module 24 config:
  - Flat: Rs. X per period of delay
  - Percentage: Y% of overdue amount per month
  - Per-day: Rs. Z per calendar day after grace period
- Grace period: configurable (default 5 days after due date)
- Late fee shown as separate demand line; separate receipt line

### 15.2 Late Fee GST
- Coaching: 18% GST on late fee (same rate as underlying service)
- School/college: exempt (same as underlying fee)
- Late fee GST shown on coaching receipt as separate line

### 15.3 Late Fee Waiver
- Principal approval required; audit-logged
- Waiver reason: medical / disaster / system downtime / management discretion
- Waived late fee amount tracked in waiver report (not in collection report)

---

## 16. Education Loan Handling

### 16.1 Loan Disbursement as Payment
- Bank disburses directly to institution's bank account (not to student)
- Accountant records: payment mode = ELOAN, UTR number, bank name, loan account number, student_id, disbursement date
- Provisional receipt on UTR confirmation; final on bank credit

### 16.2 Fee Demand Letter for Bank
- Student requests fee demand letter for bank loan sanction
- System generates on institution letterhead: student name, course, total fee, year-wise breakup, institution bank account details
- In-app view only; shareable as link; not PDF (platform policy)

### 16.3 Partial Loan
- Loan covers part of fee; student pays balance from own funds
- Two separate postings on same demand: ELOAN + CASH/UPI
- Single receipt covering both posting entries

### 16.4 Semester-Wise Disbursement
- Bank disburses per semester (B.Tech, MBBS multi-year courses)
- Each semester's demand matched to corresponding disbursement
- Undisbursed semester demands stay ACTIVE; no automatic deferral

---

## 17. Government Scheme & Scholarship Integration

### 17.1 Scholarship Verification Workflow
```
Parent uploads scholarship sanction letter (camera capture in app)
       │
Finance Head receives verification task
       │
Finance Head cross-checks: NSP portal / state scholarship portal / PFMS
       │
       ├── Verified → Credit posted to student ledger → Parent notified
       │
       └── Rejected → Full demand stays active → Parent notified with reason
```
- Partial disbursement: only disbursed amount credited; balance demand remains on student
- Scholarship disbursed to student bank (DBT): Accountant posts manually after student shows bank credit

### 17.2 State-Wise Scheme Handling
| Scheme | State | Model | System Action |
|---|---|---|---|
| AP Jagananna Vidya Deevena | Andhra Pradesh | Govt pays institution | Zero demand for eligible students |
| TS Vidya Deevena | Telangana | Govt pays institution | Zero demand for eligible students |
| Karnataka Rajyotsava Scholarship | Karnataka | DBT to student | Full demand; manual credit on proof |
| Maharashtra Govt Merit Scholarship | Maharashtra | Institution refunds student | Full collection; refund on sanction |
| NMMS (National) | All states | DBT to student | Full demand; manual credit on proof |
| NSP (National Scholarship Portal) | All states | DBT to student | Full demand; manual credit on proof |

### 17.3 State Reimbursement Claim Report
- Student-wise list: name, class, category, fee foregone / credited, scheme name, sanction reference
- Exported in state-prescribed format for online submission to state education portal
- Tracks: claimed amount vs received amount vs variance

---

## 18. Sponsored Student & CSR Fee Payment

### 18.1 Sponsor Types
- Corporate CSR (Section 135, Companies Act 2013)
- NGO / charitable trust
- Individual philanthropist
- Alumni association
- Government welfare scheme (distinct from regular scheme — ad-hoc)

### 18.2 Sponsor Payment Workflow
- Sponsor account created in system: sponsor_name, type, GSTIN (if corporate), contact, PAN
- Sponsor payment posted: amount, sponsorship_period, student_ids[] covered
- Amount split to individual student ledgers automatically
- Receipt generated for **sponsor** (not parent): sponsor name on receipt, students covered listed
- Parent sees: "Tuition covered by [Sponsor Name]. Balance due: Rs. 0"
- Sponsorship end: system reverts to regular demand on next instalment; parent notified 30 days before

### 18.3 Tax Implications
- Corporate sponsor paying as CSR donation: not a business expense under normal head; treated under Section 135 CSR expenditure; Finance Head flags for CA review
- Individual donor: may claim Section 80G deduction if institution has 80G registration; system generates donation receipt in 80G format

---

## 19. NRI & Foreign Student Collection

### 19.1 NRI Parent (SWIFT Transfer)
- SWIFT reference number captured
- Amount recorded in INR at RBI reference rate on payment date
- Original foreign currency amount and currency code noted in ledger
- FEMA compliance flag: foreign remittance receipt → flagged for FEMA reporting review

### 19.2 FCRA Compliance
- If institution receiving foreign funds: FCRA (Foreign Contribution Regulation Act) registration status check
- System flags any foreign payment for compliance review by Finance Head
- FCRA-registered institutions: foreign receipt logged in FCRA-compliant format for annual return

### 19.3 International Student
- Fee structure may include foreign national surcharge (institution configures in Module 24)
- FRRO (Foreigners Regional Registration Office) fee tracking: separate passthrough
- Receipt in English only (no regional language for international students)

---

## 20. Bulk Collection Operations

### 20.1 Bulk Collection Modes
| Mode | Trigger | Receipt |
|---|---|---|
| Class-wise bulk | Accountant selects class; sees all outstanding students | Individual receipts per student |
| Hostel fee bulk | All hostellers for a billing month | Individual receipts per student |
| Transport fee bulk | Zone-wise collection | Individual receipts per student |
| Board exam fee bulk | All eligible students | Individual passthrough receipts |
| Event fee bulk | Annual day / excursion participation | Individual receipts |

### 20.2 High-Volume Day Handling
- Year-end rush, fee deadline days: queue-based receipt generation (SQS)
- Parent sees "Payment received — receipt generating" status immediately
- Receipt delivered via WhatsApp within 60 seconds (SLA)
- No throttling on collection endpoints during high-volume periods
- Load tested target: 500 simultaneous counter collections + 2,000 simultaneous online payments

### 20.3 Bulk Receipt Download
- Accountant: download all receipts for a date range / class / branch as ZIP
- Individual PDFs inside ZIP; named as `{receipt_number}_{student_name}.pdf`
- Available within 5 minutes of request (async generation via SQS)

---

## 21. Refund Management

### 21.1 Refund Triggers
| Trigger | Rule |
|---|---|
| Admission cancellation — school/college | UGC refund rules apply (see below) |
| Admission cancellation — coaching | 48-hour full refund; after 48 hours — institution policy |
| Course withdrawal mid-year | UGC sliding scale |
| Cheque bounce reversal | Full reversal of provisional receipt amount |
| Duplicate payment | Full refund of second payment |
| Excess payment (advance credit) | On parent request; approval workflow |
| Advance fee cancellation | Full or partial per policy; GST credit note issued |
| Security / caution deposit | On no-dues clearance (Module 39 prerequisite) |
| Scholarship overcharge | After scholarship credit applied, if overpaid |

### 21.2 UGC Refund Rules (College — Automatic Enforcement)
| Withdrawal Timeline | Refund % | System Action |
|---|---|---|
| Before course start date | 100% | Full refund; system enforces |
| Within 15 days after start | 80% | System calculates; Accountant reviews |
| 16–30 days after start | 60% | System calculates |
| 31–45 days after start | 40% | System calculates |
| 46–60 days after start | 20% | System calculates |
| After 60 days | 0% | No refund; system blocks |
- System auto-calculates refund amount based on withdrawal date
- Cannot be overridden below statutory minimum without Management + Legal approval

### 21.3 Refund Approval Chain
| Amount | Approvers |
|---|---|
| ≤ Rs. 1,000 | Accountant self-approve |
| Rs. 1,001 – Rs. 10,000 | Accountant → Principal |
| Rs. 10,001 – Rs. 1,00,000 | Accountant → Principal → Management |
| > Rs. 1,00,000 | Accountant → Principal → Management → Finance Head |
- Thresholds configurable per institution

### 21.4 Refund Mode Rules
- Default: same as original payment mode
- Cash refund for cash payment
- NEFT/RTGS for online payment (bank details captured)
- Exception (different mode): Management approval required; reason mandatory
- Refund to education loan account: if student paid via loan, refund goes to bank, not student; institution + bank coordinate

### 21.5 GST Handling on Refund (Coaching)
- Full refund: GST credit note issued; GST reversed; GSTR-1 amendment entry generated
- Partial refund: proportional GST credit note
- Credit note reference: original invoice number, original date, reason for credit, GST reversed per rate
- GSTR-1 amendment data exported for CA / accountant filing

### 21.6 Security / Caution Deposit Refund
- Prerequisite: no-dues certificate from Module 39 (all modules cleared)
- Liability ledger entry reversed
- Refund via NEFT (not cash, regardless of original mode — for audit cleanliness)
- Timeline: 30 days from no-dues clearance (configurable; institution policy)

---

## 22. Cheque Bounce & Penalty

### 22.1 Bounce Processing
- Bank returns cheque with bounce memo
- Accountant marks PDC / cheque as BOUNCED in system
- Actions triggered automatically:
  1. Provisional receipt → CANCELLED
  2. Payment posting reversed (demand reopened)
  3. Bounce charge demand raised (configured amount in Module 24)
  4. WhatsApp notification to parent: "Cheque No. XXXXXX returned unpaid — [reason]. Please pay via [alternative mode]."
  5. Module 26 defaulter flag raised

### 22.2 Bounce Charges
- Configurable per institution (Rs. 500 / Rs. 750 / Rs. 1,500 — matches bank charges + institution penalty)
- Bounce charge demand: separate fee head; cannot be waived without Principal + Finance Head approval
- Bounce charge GST: 18% if coaching; exempt if school/college

### 22.3 Bounce Count & Payment Mode Restriction
| Bounce Count | Action |
|---|---|
| 1st bounce | WhatsApp alert; demand reopened; bounce charge raised |
| 2nd bounce | Cheque/DD mode blocked for this student for this academic year |
| 3rd bounce | Matter escalated to Module 26 legal recovery; Principal decision on admission continuation |
- Block override: Principal approval; documented reason

---

## 23. Cash Legal Compliance (Section 269ST)

### 23.1 Hard Block — Rs. 2 Lakh Cash Limit
- Section 269ST of Income Tax Act: no person shall receive cash above Rs. 2 lakh from a single person
  in a single day or for a single transaction or relating to one event/occasion
- Violation: penalty = 100% of amount received — institution is liable (not the payer)
- System checks: aggregate cash received from same parent/payer on same calendar day across ALL counters
- If aggregate would exceed Rs. 2 lakh: transaction HARD BLOCKED at cashier screen
- No override role — Principal, Management, EduForge support cannot bypass this block
- System message: "Cash payment blocked — daily cash limit of Rs. 2,00,000 reached for this parent. Please accept via NEFT / UPI / Cheque."

### 23.2 PAN Requirement (Rule 114B)
- PAN mandatory for any single cash transaction above Rs. 50,000
- System prompts cashier to enter PAN before posting
- If parent does not have PAN: Form 60 (no income) or Form 61 (agricultural income) must be captured
- Form 60/61 data stored in system; exportable for Income Tax reporting

### 23.3 PMLA / Anti-Money Laundering Register
- All cash transactions above Rs. 1 lakh logged in separate compliance register (beyond normal audit log)
- Register exportable for CA / Income Tax audit
- 7-year retention; immutable

### 23.4 SFT (Statement of Financial Transaction — Rule 114E)
- Institution must report to Income Tax Department if:
  - Aggregate cash receipt from any person ≥ Rs. 1 lakh in a financial year, OR
  - Aggregate receipt by any mode from any person ≥ Rs. 10 lakh in a financial year
- System auto-flags students/parents meeting either threshold
- SFT data file generated in ITD-prescribed XML format; exported for submission by May 31

---

## 24. Advance Fee for Next Academic Year

### 24.1 Collection
- February–April: seat-booking / advance admission fee collected for next academic year
- Tagged: academic_year = NEXT; type = ADVANCE
- Separate from current-year collection; excluded from current-year reconciliation

### 24.2 GST on Advance (Coaching)
- GST liability arises at time of advance receipt (not at service start) — Section 12 CGST Act
- System generates advance receipt voucher (not tax invoice) immediately
- GST paid to government in the month of collection
- When academic year starts: advance receipt voucher → converted to tax invoice
- GST already paid on advance; no double-counting

### 24.3 Student Doesn't Join
- Refund with GST credit note
- GST reversal: system generates GSTR-1 amendment entry
- Institution policy: full refund / partial forfeiture — configurable; UGC rules apply for college

---

## 25. Divorced Parent / Court-Order Fee Split

### 25.1 Split Demand Configuration
- Court order specifies fee split (e.g., Father: 60%, Mother: 40%)
- Stored in Module 09 (Parent Management) linked to student record
- Module 25 reads split ratio at demand generation; creates two sub-demands per instalment
- Demand A (Father's 60%) + Demand B (Mother's 40%) = Total demand

### 25.2 Collection & Receipts
- Each parent pays their own sub-demand; separate receipt per parent
- If Father pays but Mother does not: Module 26 flags only Mother's sub-demand as defaulter
- Child's access holds: triggered only if aggregate outstanding (both sub-demands) exceeds threshold

### 25.3 Data Privacy
- Court order document stored in Module 09; visible only to Principal + Admin
- Neither parent can see the other's payment status or receipt

---

## 26. Demand Notice & Pre-Defaulter Escalation

### 26.1 Escalation Sequence
| Day | Action | Delivery |
|---|---|---|
| Due date + 1 | Soft reminder: "Your fee of Rs. X was due yesterday" | WhatsApp + in-app |
| Due date + 7 | Formal demand notice (system-generated letterhead) | WhatsApp + in-app + email |
| Due date + 15 | Second formal notice with consequence statement | WhatsApp + in-app |
| Due date + 30 | Pre-legal notice; Module 26 hand-off | WhatsApp + in-app + registered email |

### 26.2 Demand Notice Content
- Student name, class/section, admission number
- Fee head-wise outstanding (not just total)
- Original due date; days overdue
- Late fee accrued to date
- Total amount to pay (fee + late fee)
- Payment modes and links
- "Failure to pay by [date] will result in [consequences per institution policy]"

### 26.3 Notice Register
- Every notice: date, type, delivery mode, recipient (parent name + contact), delivery status, acknowledgement
- Immutable log; exportable for legal proceedings if needed

---

## 27. Academic & Service Hold on Fee Default

### 27.1 Hold Triggers
- Configurable threshold: default 30 days past due date
- Institution can set different thresholds per hold type

### 27.2 Holds Applied
| Service | Module | Hold Action |
|---|---|---|
| Exam hall ticket | Module 19 | Blocked — cannot be generated |
| Result / marksheet access | Module 21 | Hidden from student/parent app |
| TC issuance | Module 39 | Blocked — admin cannot generate |
| Library card | Module 30 | Card suspended |
| Portal access | All modules | Login restricted to fee payment screen only |

### 27.3 What Is NEVER Blocked
- Attendance marking: teacher still marks attendance (legal obligation regardless of fee)
- Emergency notifications (safety, health)
- RTE students and fully government-scheme-covered students: never blocked
- CWSN (Children With Special Needs): configurable; default no block

### 27.4 Override
- Principal manually lifts hold for specific student
- Reason mandatory; duration specified (e.g., "Hold lifted for 7 days — parent has committed to pay")
- Override audit-logged; parent not notified of override reason
- Parent sees: "Temporary access restored. Please clear dues by [date]."

---

## 28. Year-End Demand Lock & Transfer to Module 26

### 28.1 Lock Process
- Trigger: academic year end (manual initiation by Finance Head)
- Pre-lock checklist:
  - All provisional receipts resolved (cleared or bounced)
  - All refunds processed or pending-documented
  - Monthly reconciliation locked for all months
  - Passthrough remittances completed or documented
- Dual approval: Principal + Finance Head
- Post-lock: no new payments accepted against current year's demands

### 28.2 Post-Lock Actions
- All outstanding demands: status → LOCKED
- Locked outstanding transferred to Module 26 as carried-forward_dues
- Year-end report generated: demands_raised | collected | outstanding | waived | scheme_covered — immutable
- Student promotion flag: institution configures whether carried-forward dues block class promotion (Module 07)

### 28.3 Post-Lock Corrections
- Only Finance Head + Management can reopen a locked demand
- Reason mandatory; extremely rare (audit-triggered correction only)
- Full audit trail; EduForge support notified of any post-lock correction

---

## 29. Reconciliation

### 29.1 Daily Reconciliation
- Auto-generated at day end (11:59 PM)
- Counter-wise: expected (opening balance + collections) vs actual (closing balance + deposits)
- Mode-wise: cash | cheque | DD | NEFT | UPI | gateway | NACH | BBPS | virtual account
- Cashier-wise: collection per cashier per shift
- Discrepancies automatically flagged to Accountant for next-day resolution

### 29.2 Bank Reconciliation
- System collection total vs bank statement credit (imported or manually entered)
- Variance categories: uncleared cheques | gateway settlement lag (T+1/T+2) | virtual account credit not yet arrived
- Cheque clearing tracker: pending cheques listed with expected clearance date; updated on actual clearance
- Cash deposit slip: generated by system (denomination-wise); deposit slip reference logged after bank deposit

### 29.3 Gateway Reconciliation
- Settlement files auto-parsed: Razorpay (CSV) / PhonePe (Excel) / PayU (CSV)
- Match on: gateway_transaction_id ↔ system receipt_id
- Match result types:
  - Matched: system receipt + gateway settlement — OK
  - Ghost transaction: money on gateway, no receipt → Finance Head alert; investigate immediately
  - Unconfirmed receipt: receipt in system, no gateway settlement → Finance Head alert; may be MDR-deducted or failed
- Net MDR: system tracks gross collected + MDR charged per transaction

### 29.4 NACH / UPI AutoPay Reconciliation
- NPCI settlement report vs system receipts; matched on mandate_id + debit date
- Failed debits reconciled: NPCI failure code vs system non-payment record

### 29.5 Passthrough Reconciliation
- CBSE / NTA / University exam fee: collected vs remitted
- Variance flagged if not remitted within 30 days of collection
- Remittance entry: Accountant posts remittance (UTR to board); passthrough balance reduced

### 29.6 Monthly Lock
- Finance Head reviews monthly reconciliation
- Locked after approval: no entries permitted after lock
- Month lock is prerequisite for year-end lock

---

## 30. Chart of Accounts / GL Mapping

### 30.1 GL Account Structure
- Every fee head mapped to a GL account code at Module 24 configuration stage
- Default GL accounts (pre-loaded; institution modifies names):

| GL Code | Account Name | Type |
|---|---|---|
| 4001 | Tuition Fee Income | Income |
| 4002 | Admission Fee Income | Income |
| 4003 | Development Fund Income | Income |
| 4004 | Exam Fee Income | Income |
| 4005 | Transport Fee Income | Income |
| 4006 | Hostel Fee Income | Income |
| 4007 | Laboratory Fee Income | Income |
| 4008 | Late Fee Income | Income |
| 4009 | Bounce Charge Income | Income |
| 2001 | Caution Deposit Liability | Liability |
| 2002 | Security Deposit Liability | Liability |
| 2003 | CBSE Board Fee Payable | Liability (passthrough) |
| 2004 | NTA Fee Payable | Liability (passthrough) |
| 2005 | University Exam Fee Payable | Liability (passthrough) |
| 1001 | Cash in Hand | Asset |
| 1002 | Bank Account — Current | Asset |
| 1003 | Cheques in Clearing | Asset |

### 30.2 Double-Entry Postings
| Transaction | Debit | Credit |
|---|---|---|
| Fee collected — cash | Cash in Hand (1001) | Fee Income GL (4xxx) |
| Fee collected — online | Bank Account (1002) | Fee Income GL (4xxx) |
| Cheque deposited | Cheques in Clearing (1003) | Fee Income GL (4xxx) |
| Cheque cleared | Bank Account (1002) | Cheques in Clearing (1003) |
| Caution deposit received | Cash / Bank | Caution Deposit Liability (2001) |
| Refund issued | Fee Income GL (4xxx) | Cash / Bank |
| Caution deposit refunded | Caution Deposit Liability (2001) | Cash / Bank |
| Passthrough collected | Cash / Bank | CBSE Board Fee Payable (2003) |
| Passthrough remitted | CBSE Board Fee Payable (2003) | Bank Account |

### 30.3 Output Reports Enabled by GL Mapping
- Fee Income Statement (P&L input)
- Outstanding Debtors Report
- Liability Statement (deposits held)
- Passthrough Payable Statement
- Tally-compatible export (GL code → Tally ledger mapping)

---

## 31. GST Compliance — Coaching Institutions

### 31.1 Tax Invoice Requirements
- Mandatory fields: institution GSTIN, institution name + address, SAC code 9993, invoice number,
  invoice date, student name + address (state for IGST determination), taxable value per head,
  CGST rate (9%) + amount or IGST rate (18%) + amount, total invoice value
- Invoice numbering: sequential; no gaps; new series per financial year (April–March)
- E-invoicing: mandatory if institution turnover > Rs. 5 crore; IRN from NIC IRP API; QR code on invoice

### 31.2 GST on Advance (Coaching)
- GST collected on advance receipt → paid in month of collection (not month of service)
- Advance receipt voucher: same format as tax invoice but labelled "Receipt Voucher"
- On service start: receipt voucher reference in tax invoice; no double GST

### 31.3 GST Returns Data Export
| Return | Frequency | Data from Module 25 |
|---|---|---|
| GSTR-1 | Monthly (by 11th) | Invoice-wise outward supply; credit notes |
| GSTR-3B | Monthly (by 20th) | Net tax liability after input credit |
| GSTR-9 | Annual | Aggregate supply + tax summary |

### 31.4 Input Tax Credit (ITC)
- Coaching institution can claim ITC on purchases (office supplies, infrastructure)
- Module 25 does not handle purchase invoices; but GSTR-3B export includes ITC column for Finance team to fill

### 31.5 Place of Supply (Intra vs Inter-State)
- Student's registered state = place of supply
- Student in same state as institution: CGST 9% + SGST 9%
- NRI student / student from different state: IGST 18%
- System auto-determines based on student address (Module 07)

---

## 32. Income Tax Compliance

### 32.1 Section 80C Annual Certificate
- Generated each April for previous financial year (not academic year)
- Shows: tuition fee ONLY (transport / hostel / activity / exam fee excluded — 80C covers tuition only)
- Financial year split: if academic year is June–May, the April–March certificate shows June–March only
  (May falls in next FY; separate certificate)
- Institution PAN printed (mandatory for parent's 80C claim)
- Multiple children: separate certificate per child; or consolidated per parent's preference
- Format: in-app view; shareable as link; NOT PDF (platform policy — parent screenshots or shares link)
- Auto-generated: system sends WhatsApp notification each April 1 to all parents: "Your fee certificate for FY 2025-26 is ready"

### 32.2 Section 10(23C) — Institution Income Tax Exemption
- Income tax exempt institutions (schools approved u/s 10(23C)): annual collection summary
  exported for CA / income tax audit in prescribed format

---

## 33. Financial Year vs Academic Year Reporting

### 33.1 Dual Tagging
- Every receipt tagged with BOTH: academic_year_id AND financial_year (April–March)
- Example: receipt dated January 15, 2026 → academic_year = 2025-26; financial_year = 2025-26 (April 2025 – March 2026)
- Example: receipt dated May 10, 2025 → academic_year = 2024-25 (if June-start school); financial_year = 2025-26

### 33.2 Report Slices
- Collection reports: available in both academic year and financial year view
- GST returns: financial year only (April–March)
- Section 80C certificate: financial year only
- Board audit / CBSE affiliation: academic year
- Income Tax / CA audit: financial year

---

## 34. Offline Collection (No Internet)

### 34.1 Paper Receipt Book
- Pre-printed receipt books: system issues serial ranges (e.g., Book 1: 00001–00100)
- Book issuance logged: cashier_id, serial range, issue date
- Each receipt page has: triplicate carbon copies (one each for parent, cashier, office)

### 34.2 Reconnect Sync
- Cashier batch-enters paper receipts after reconnect; backdated to actual collection time
- System validates: serial numbers within issued range; no duplicates; amounts match paper stubs
- Supervisor (Accountant) reviews batch entry vs paper stubs; approves posting
- Discrepancy: flagged; cashier explains; if unresolved → escalated to Principal

### 34.3 Used Book Return
- Completed book returned to Accountant; all serial numbers accounted for
- Unused serials in returned book: marked VOID in system

---

## 35. Re-Admission Dues Handling

- Student who previously left with outstanding dues (withdrew mid-year or non-payment TC)
- System detects prior outstanding on re-admission attempt (matched by Aadhaar / name+DOB+parent mobile)
- Old dues displayed to Admission staff before re-admission is processed
- Old dues must be cleared before re-admission (institution policy; configurable)
- Waiver of old dues: Management approval required; reason documented; audit-logged
- Old dues receipt: issued with historical academic year reference; separate from new year ledger

---

## 36. Stationery, Uniform & Books Sale at Counter

### 36.1 Separation from Fee Collection
- School store items (uniform, books, stationery) have different GST treatment than education fee
- Education fee = exempt; textbooks = 5% GST; stationery/uniform = 12% GST
- Cannot combine taxable and exempt items on a single GST invoice (CGST Act rule)
- System generates TWO separate receipts: fee receipt (exempt) + goods receipt (GST applicable)

### 36.2 School Store Module (Within Module 25 Scope)
- Items catalogue: item name, category (uniform/books/stationery), price, GST rate, stock quantity
- Stock auto-reduces on sale; low-stock alert to Admin
- Goods receipt format: institution GSTIN, item-wise HSN code, quantity, rate, GST amount, total

---

## 37. External / Walk-In Exam Candidate Fee

- Institution allows external students to appear for internal pre-boards / mock exams
- No admission number (not enrolled)
- Cashier selects "External Candidate" collection mode
- System generates temporary external_candidate_id for receipt purposes
- Minimum details: name, phone, exam name, amount
- Receipt issued without student ledger link
- External candidate collection: separate report; not mixed with enrolled student collection

---

## 38. Inter-Branch Fee Payment

- Student of Branch A pays at Branch B counter (parent's workplace near Branch B)
- System records: paying_branch_id, student_branch_id (different)
- Receipt issued normally; ledger posted to student's Branch A ledger
- Inter-branch entry: Branch B — Dr Inter-Branch Receivable; Cr Cash
  Branch A — Dr Cash; Cr Inter-Branch Payable
- Finance Head settles inter-branch entries periodically (weekly / monthly)
- HQ sees consolidated collection across all branches

---

## 39. Accounting Software Export (Tally)

### 39.1 Export Format
- Daily export in Tally XML format (Tally ERP 9 / TallyPrime compatible)
- Voucher type: Receipt
- Each posting → one voucher: Dr Cash/Bank GL → Cr Fee Income GL (per head)
- GST entries: CGST / SGST / IGST correctly mapped to Tally GST ledgers
- Passthrough: separate trust/liability ledger (Dr Cash → Cr Board Fee Payable)
- Refunds: Dr Fee Income → Cr Cash (reverse of collection)

### 39.2 Tally Ledger Mapping
- Module 25 GL codes mapped to Tally ledger names during institution setup
- Mapping table: eduforge_gl_code → tally_ledger_name (editable by Finance Head)
- Exported XML uses Tally ledger names directly; Tally imports without manual mapping

### 39.3 Export Frequency
- Daily auto-export: generated at 11:59 PM; emailed to Finance Head / Tally operator
- One-click manual export: any date range; downloadable from Finance Head dashboard
- Monthly export: all transactions in a calendar month in one XML file

---

## 40. Real-Time Collection Dashboard

### 40.1 Management / Owner View
- Today's total collection: updates every 5 minutes
- Counter-wise breakdown: Counter 1 | Counter 2 | Online | NACH | BBPS | Virtual Account
- Mode-wise: Cash X% | UPI X% | Cheque X% | Online X% | NACH X%
- Compare vs same day last year (YoY) and same day last month (MoM)
- Monthly target (Finance Head sets) vs actual: progress bar + % achieved
- Branch-wise for multi-branch groups: sortable by collection today / this month / outstanding

### 40.2 Accountant View
- Outstanding aging: 0–7 days | 8–30 days | 31–60 days | 60+ days — count + amount
- Top 10 highest outstanding students (for prioritised action)
- PDC presentation due in next 7 days
- Cheques pending clearance: count + amount + expected clearance dates
- Pending gateway reconciliation items
- Collection efficiency: % of demand collected by due date (this month vs last month)

### 40.3 Collection Efficiency Metric
- Collection rate = (amount collected by due date) / (total amount demanded) × 100
- Tracked per class / branch / institution / platform (Module 53)
- Institutions with collection rate < 70% by D+30 → Customer Success outreach trigger

---

## 41. Reports & MIS

### 41.1 Daily Reports (Auto-Generated)
| Report | Audience | Contents |
|---|---|---|
| Daily Collection Summary | Accountant, Principal | Total; counter-wise; mode-wise; cashier-wise |
| PDC Presentation Due | Accountant | PDCs to present in next 3 days |
| Failed Online Payments | Accountant | Gateway failures with retry status |
| Cheque Clearance Status | Accountant | Pending + cleared today |

### 41.2 Periodic Reports (On-Demand)
| Report | Contents |
|---|---|
| Head-wise Collection | Per fee head: demanded vs collected vs outstanding |
| Class/Batch-wise Collection | Per class or batch: same columns |
| Cashier-wise Collection | Per cashier: total collected; discrepancies |
| Concession & Waiver Report | Amount waived; approved by whom; reason codes |
| Refund Report | Refunds processed; approval chain; reason |
| Cheque Bounce Report | Bounce count per student; total bounce charge collected |
| PDC Register | All PDCs: status, due dates, clearance status |
| NACH / UPI AutoPay Status | Active mandates; failed debits; renewals due |
| Passthrough Collection + Remittance | Collected vs remitted per board; variance |
| Govt Scheme Adjustment | Scheme-wise credits; reimbursement claim status |
| Sponsor-wise Payment | Per sponsor: students covered; amount; period |
| External Candidate Collection | Walk-in collections |
| Outstanding Demand Aging | Feeds Module 26 daily |

### 41.3 Compliance Reports
| Report | Contents | Frequency |
|---|---|---|
| GST Liability Report | Invoice-wise; GSTR-1 input | Monthly |
| GSTR-3B Data | Net tax liability; ITC column | Monthly |
| SFT Report (Rule 114E) | Students/parents meeting Rs. 1L cash / Rs. 10L any mode threshold | Annual (by May 31) |
| Section 80C Certificate | Per parent; financial year; tuition only | Annual (April) |
| PMLA Cash Register | Cash transactions > Rs. 1 lakh | On-demand / Audit |
| Annual Collection Summary | Total; head-wise; for §10(23C) audit | Annual |
| Inter-Branch Reconciliation | Branch-wise payable/receivable | Monthly |
| Year-End Lock Report | Final snapshot; immutable | Annual |

---

## 42. Fee Dispute & Grievance

### 42.1 Dispute Workflow
```
Parent raises dispute from app (describes issue; attaches screenshot if needed)
       │
Dispute ticket created: dispute_id, student_id, demand_id, amount_in_dispute, description
       │
Assigned to Accountant (SLA: 48 hours to respond)
       │
       ├── Resolved by Accountant → closes ticket → parent notified
       │
       └── Unresolved → escalated to Principal (SLA: 48 more hours)
                │
                ├── Resolved by Principal
                │
                └── Unresolved → Finance Head → final resolution
```
- During dispute: demand stays ACTIVE; Module 26 defaulter clock PAUSED for disputed amount
- Consumer protection escalation: parent can escalate to state education department;
  system generates dispute history report for parent to submit

### 42.2 Dispute Resolution Outcomes
| Outcome | System Action |
|---|---|
| Dispute rejected (charge valid) | Demand stays; Module 26 clock resumes |
| Partial waiver | Demand reduced by waiver amount |
| Full waiver | Demand marked WAIVED; zero receipt generated |
| Error corrected | Wrong head demand cancelled; correct head demand raised |

---

## 43. Section 80C Annual Fee Certificate

### 43.1 Certificate Contents
- Student name, date of birth, admission number
- Institution name, address, PAN (mandatory for 80C claim)
- Financial year (April YYYY – March YYYY)
- Tuition fee paid in financial year (only tuition head; all other heads excluded)
- "This certificate is issued for the purpose of claiming deduction under Section 80C of the Income Tax Act, 1961"
- Institution authorized signatory name + designation

### 43.2 Multi-Year / Straddle Cases
- If academic year June–May and financial year April–March:
  - FY 2025-26 certificate shows: June 2025 – March 2026 tuition (9 months)
  - FY 2024-25 certificate shows: April 2025 – May 2025 tuition (2 months, paid in previous academic year)
- System calculates correctly using receipt dates (not instalment months)

### 43.3 Certificate Generation
- Auto-generated April 1 each year for previous FY
- WhatsApp notification to parent: "Your FY 2025-26 fee certificate is ready in your EduForge app"
- In-app view only; shareable as link (NOT PDF per platform policy)
- Multiple children: separate certificates; parent sees all in "Documents" section of app

---

## 44. Access Control

### 44.1 Role-Wise Permissions
| Action | Cashier | Accountant | Principal | Finance Head | Management | Parent |
|---|---|---|---|---|---|---|
| View student fee account | Own session only | ✅ All | ✅ All | ✅ All | ✅ All | Own child only |
| Collect payment (counter) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Issue receipt | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Cancel receipt | ❌ | Propose only | Approve | Approve | ❌ | ❌ |
| Issue duplicate receipt | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Apply ad-hoc waiver | ❌ | Propose | Approve | Approve | Approve | ❌ |
| Process refund | ❌ | Initiate | Approve | Approve | Final approval (high value) | ❌ |
| Lock monthly reconciliation | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Export GST data | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Override refund mode | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| View real-time dashboard | ❌ | ✅ (Accountant view) | ✅ | ✅ | ✅ (Management view) | ❌ |
| Lift academic hold | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| Year-end lock | ❌ | ❌ | Approve | Initiate | ❌ | ❌ |
| Generate 80C certificate | ❌ | ✅ | ✅ | ✅ | ❌ | View own only |
| Post inter-branch entry | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |

---

## 45. Notifications Triggered by This Module

| Event | Recipient | Channel | Timing |
|---|---|---|---|
| Receipt generated | Parent | WhatsApp + in-app | Immediate |
| Provisional receipt issued (cheque) | Parent | In-app only | Immediate |
| Provisional → Final (cheque cleared) | Parent | WhatsApp + in-app | On clearance |
| Cheque bounced | Parent | WhatsApp + in-app | Immediate |
| Advance credit auto-applied | Parent | In-app | On application |
| Refund processed | Parent | WhatsApp + in-app | Immediate |
| Scholarship credit posted | Parent | In-app | Immediate |
| Monthly statement available | Parent | In-app | 1st of each month |
| Payment gateway failure | Parent | In-app | Immediate (retry button) |
| PDC presentation due (3 days) | Accountant | In-app | 3 days before |
| PDC stale (30 days to expiry) | Accountant + Parent | WhatsApp + in-app | 30 days before |
| NACH / UPI AutoPay debit failed | Parent + Accountant | WhatsApp + in-app | Immediate |
| NACH mandate expiring (30 days) | Parent | In-app | 30 days before |
| Academic hold imposed | Parent | WhatsApp + in-app | Immediate |
| Academic hold lifted | Parent | In-app | Immediate |
| Year-end lock completed | Finance Head + Principal | In-app | Immediate |
| SFT threshold reached | Finance Head | In-app | On threshold hit |
| Section 80C certificate ready | Parent | WhatsApp + in-app | April 1 each year |
| Section 269ST cash block triggered | Cashier | Counter screen alert | Immediate (hard block) |
| Gateway reconciliation unmatched item | Finance Head | In-app | Daily |

---

## 46. Audit Trail & 7-Year Retention

### 46.1 Immutable Log Fields
Every transaction, cancellation, waiver, refund, adjustment, approval, override logs:
- action_type, actor_user_id, actor_name, actor_role
- student_id, demand_id, receipt_id (where applicable)
- amount_before, amount_after, delta
- timestamp (IST), IP address, device_id, browser/app version
- approver_user_id, approver_timestamp (for dual-approval actions)
- reason_text (for cancellations, waivers, overrides)

### 46.2 What Cannot Be Modified After Creation
- Original receipt (can be CANCELLED but not edited)
- Audit log entries (append-only; no update/delete via any API)
- Year-end lock report
- Monthly reconciliation after lock

### 46.3 Retention Policy
- All receipts, ledger entries, reconciliation reports, audit logs: stored on Cloudflare R2 with immutable flag
- Retention: 7 years from creation date (Income Tax Act §44AA requirement)
- Legal hold: disputed accounts → records preserved beyond 7 years until legal resolution
- DPDPA 2023: personal data (student/parent PII) — purpose limitation; retained only as long as required; financial records = 7-year statutory requirement overrides DPDPA shorter retention preference

---

## 47. Architect's Strategic Recommendations

### 47.1 Payment Orchestration Layer (Module 57 Responsibility)
Module 25 must NEVER call Razorpay / PhonePe / PayU directly. Module 57 exposes a single internal API:
- `POST /internal/payment/initiate` → returns checkout_url + session_id
- `POST /internal/payment/webhook` → verified + normalised payment result
- `GET /internal/payment/status/{session_id}` → PENDING / SUCCESS / FAILED
- Benefit: add/swap/remove gateways in Module 57 with zero change to Module 25
- Benefit: gateway failover (Razorpay down → PhonePe) invisible to Module 25
- Benefit: single reconciliation interface regardless of gateway count

### 47.2 Virtual Account as Default for Scale
For institutions with 1,000+ students, push virtual account as PRIMARY payment channel:
- Zero MDR (NEFT/IMPS vs 1.5-2% gateway) → Rs. 6 lakh/year saving per 1,000 students
- Zero manual reconciliation → Accountant time savings
- Works for NRI, corporate sponsors, government disbursements
- Counter collection becomes the exception for large institutions, not the norm
- Target: 70%+ of collections via virtual account for Tier 1 institutions within 2 years

### 47.3 Predictive Default Detection (Module 47 — AI Performance Analytics)
Train a lightweight model on:
- Days-since-last-payment history
- Historical payment pattern (always late? always on time?)
- Instalment number (last instalment defaulted more often than first)
- Family income category (scholarship flag)
- Bounce count history
Weekly scoring: flag "likely to default in next 14 days" students to Accountant.
Proactive WhatsApp outreach before default, not after.
Expected: 30-40% reduction in Module 26 escalations.

### 47.4 Collection Efficiency as Platform Health Signal
Collection rate (% of demand collected by due date) is the single most important institution health
metric. Build into Module 53 (Platform Analytics) as a key indicator:
- Institution collection rate < 70% by D+30 → Customer Success team outreach
- Collection rate trending down 3 months in a row → account health risk flag
- Collection rate by mode: helps identify adoption of digital channels
- Benchmark: show institution their collection rate vs platform average (anonymised)

### 47.5 Parent Payment Touchpoint as Engagement Opportunity
The fee receipt WhatsApp message is the highest-frequency parent-platform touchpoint.
Make it a mini-engagement moment:
```
✅ Fee paid — Rs. 4,500 received
Student: Arjun Sharma | Class 9-A
Next due: May 1, 2026 — Rs. 4,500 (Quarterly instalment)

📊 Arjun ranked #4 in last week's maths test
🎯 Attendance this month: 95%

[View Receipt] [Pay Next Instalment]
```
One message = payment confirmation + next due reminder + student achievement highlight.
Parents feel the platform is working for them. Reduces "when is next fee due?" support queries.
