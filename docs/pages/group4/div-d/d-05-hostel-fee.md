# D-05 — Hostel Fee Collection & Accounts

> **URL:** `/college/hostel/fees/`
> **File:** `d-05-hostel-fee.md`
> **Priority:** P1
> **Roles:** Hostel Admin (S3) · Finance Manager (S4) · Chief Warden (S4) · Accounts Officer (S3)

---

## 1. Hostel Fee Structure

```
HOSTEL FEE STRUCTURE — 2026–27
(Approved by Hostel Committee; displayed at hostel office)

ACCOMMODATION FEE (Annual):
  Block A (3-bed standard, common bath):   ₹42,000/yr
  Block B (2-bed, semi-attached bath):     ₹48,000/yr
  Block C Girls (2-bed, semi-attached):    ₹48,000/yr
  PwD accessible room (ground floor):      ₹42,000/yr (no premium — equal cost)

MESS FEE (Annual):
  Full plan (3 meals/day):                 ₹38,400/yr
  Partial plan (lunch + dinner):           ₹25,200/yr

CAUTION DEPOSIT (one-time, refundable):
  Accommodation:                           ₹5,000
  Mess:                                    ₹2,000
  Total caution deposit:                   ₹7,000

MISCELLANEOUS (Annual):
  Electricity (metered — shared floor):    Actual; estimated ₹1,200/yr/student
  Laundry machine usage token:             ₹50/token (20 tokens ≈ ₹1,000/yr typical)

TOTAL ANNUAL COST (typical student, Block B, full mess):
  ₹48,000 + ₹38,400 + ₹7,000 (deposit, first year) + ₹2,200 (elec+laundry) = ₹95,600 (Year 1)
  Subsequent years (no deposit): ₹88,600/yr

PAYMENT SCHEDULE:
  Semester I: Due by 15 July (accommodation ₹24,000 + mess ₹19,200 = ₹43,200)
  Semester II: Due by 1 January (same amounts)
  Late fee: ₹100/week after due date (stops after 4 weeks → recovery process)
```

---

## 2. Fee Ledger

```
HOSTEL FEE LEDGER — Student: Kiran S. (226J1A0312)
Hostel Year: 2026–27 | Room: Block B-204

CHARGES:
  Accommodation (Full Year):       ₹48,000
  Mess (Full Year):                ₹38,400
  Caution Deposit:                 ₹7,000  (1st year)
  Total Charged:                   ₹93,400

PAYMENTS RECEIVED:
  15 Jul 2026: ₹43,200 (Semester I — UPI xxxxxxxxxx)  ✅
  10 Jan 2027: ₹43,200 (Semester II — UPI xxxxxxxxxx) ✅
  Deposits paid with Sem I payment: ₹7,000            ✅

BALANCE: ₹0 (fully paid)

EXTRA CHARGES:
  Nov 2026: Mess extra items (canteen counter):  ₹320  → Paid 30 Nov 2026 ✅
  Feb 2027: Electricity bill share:              ₹580  → Paid 5 Mar 2027 ✅

HOSTEL DEFAULTERS (Summary — March 2027):
  Total outstanding: ₹1,84,600 (14 students)
  Breakdown:
    Scholarship pending (TS ePASS): 8 students  ₹96,000 ← government delay
    Bank loan disbursement pending:  4 students  ₹64,000 ← bank processing
    Hardship (waiver applied):       2 students  ₹24,600 ← under review
  Policy: No eviction from hostel for pending cases with valid reason on file
          (denying shelter to students whose scholarship/loan is delayed is inhumane
           and would attract media and consumer complaints)
```

---

## 3. Hostel Fee Receipts

```
HOSTEL FEE RECEIPT
Receipt No: GCEH/H/2026-27/1847
Date: 15 July 2026

Student: Kiran S.
Roll: 226J1A0312
Hostel: Block B, Room 204, Bed-01

PAYMENT DETAILS:
  Accommodation (Sem I):   ₹24,000
  Mess fee (Sem I):        ₹19,200
  Caution deposit:         ₹7,000
  Total:                   ₹50,200

Mode: UPI (PhonePe — Ref: PH20260715XXXXXXX)
Processed by: Hostel Admin

BREAKDOWN FOR INCOME TAX:
  Hostel accommodation fee: ₹24,000 — NOT eligible for Section 80C or any deduction
  (Hostel fees do not qualify as tuition fees under Section 80C;
   only tuition fee for full-time education qualifies — ITO clarification)
  Separate college tuition fee receipt (C-03) available for 80C purposes

[Print Receipt]  [Email Receipt]  [Download PDF]
```

---

## 4. Hostel Accounts Reconciliation

```
HOSTEL ACCOUNTS — Annual Summary 2025–26

INCOME:
  Accommodation fee:         ₹1,09,44,000  (228 students × avg ₹47,300)
  Mess fee:                  ₹88,00,000    (estimated; net after mess-leave deductions)
  Caution deposits received: ₹14,00,000    (200 new students × ₹7,000)
  Electricity charges:       ₹2,80,000
  Total Income:              ₹2,14,24,000

EXPENDITURE:
  Mess contractor payment:   ₹88,00,000
  Maintenance (rooms):       ₹12,40,000
  Housekeeping staff wages:  ₹18,60,000
  Electricity:               ₹8,20,000
  Security (hostel portion):  ₹9,60,000
  Warden honorarium:         ₹3,60,000    (₹5,000/month per warden × 6 wardens × 12)
  Capital expenses:          ₹14,00,000   (bed replacement, furniture, RO)
  Total Expenditure:         ₹1,54,40,000

SURPLUS (hostel P&L):       ₹59,84,000
  Allocated to: Hostel capital improvement fund (new block construction planning)
  Caution deposits held:     ₹62,30,000 (liability — to be refunded at check-out)

NOTE: Hostel P&L is part of overall college P&L (Form 10B); not a separate trust
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hostel/fees/structure/` | Fee structure for current year |
| 2 | `GET` | `/api/v1/college/{id}/hostel/fees/ledger/{student_id}/` | Student hostel fee ledger |
| 3 | `GET` | `/api/v1/college/{id}/hostel/fees/defaulters/` | Defaulter list with reasons |
| 4 | `POST` | `/api/v1/college/{id}/hostel/fees/payment/` | Record hostel fee payment |
| 5 | `GET` | `/api/v1/college/{id}/hostel/fees/accounts/annual/` | Annual hostel accounts |
| 6 | `GET` | `/api/v1/college/{id}/hostel/fees/deposits/` | Caution deposit register |

---

## 6. Business Rules

- Hostel fee is a separate contractual obligation from college tuition fee; a student who has paid tuition fee but not hostel fee can be asked to vacate the hostel (within reasonable notice), but this does not affect their academic standing — hostel provision is a separate service, not a prerequisite for academic participation
- Caution deposits are held in trust for the student; they must not be commingled with college operating funds or invested in fixed deposits under the college's name without proper segregation; on check-out, the deposit must be refunded within 5 working days after deducting documented damage (if any)
- Hostel fee receipts must clearly separate accommodation fee from mess fee; for income tax purposes, Section 80C allows deduction only for tuition fees; a parent/student who claims hostel fee as 80C deduction is making a false claim — the receipt must not call it "educational fee" to avoid facilitating this
- Electricity billing must be metered and actual-cost-based; flat-rate electricity charges that are significantly higher than actual consumption are considered extra charges beyond approved fee and can be challenged as unlawful collection; metered billing is both fair and legally safer
- The warden honorarium is typically paid as an allowance to faculty; TDS implications: if paid as part of salary, TDS under Section 192 applies; if paid as a separate honorarium to a professional, TDS under Section 194J (10%) applies; EduForge routes this through payroll to ensure correct TDS treatment

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division D*
