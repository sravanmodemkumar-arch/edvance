# D-04 — Fee Collection Counter

> **URL:** `/school/fees/collect/`
> **File:** `d-04-fee-collection-counter.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Fee Clerk (S2) — full (collect + receipt) · Accountant (S3) — full · Principal (S6) — full

---

## 1. Purpose

The primary fee collection interface — used at the school's fee counter daily. Fee Clerk searches a student, sees outstanding dues, selects payment mode, and generates a receipt. This is a high-volume, high-stakes operation: a school of 400 students collecting quarterly fees sees 400 transactions in a 15-day window. Speed, accuracy, and receipt printing are critical.

Key considerations for Indian school fee counters:
- Both cash and online (UPI/NEFT/RTGS) must be handled
- Receipts must be GST-compliant (even if fee is exempt, "GST-exempt" must be stated)
- Physical receipt printer (thermal or dot matrix) integration
- Daily closing: cash balance reconciliation is done every evening
- Some parents pay for multiple children in one visit → split receipts or combined receipt
- During peak collection days (April 1–15), 50+ transactions per day at a single counter

---

## 2. Page Layout

### 2.1 Header
```
Fee Collection Counter                        Today: 26 Mar 2026
Collected Today: 38 receipts  ·  ₹3,84,200  (Cash: ₹1,24,000 · Online: ₹2,60,200)
[Day Close Report]  [Float Entry]  [Shift Handover]
```

### 2.2 Student Search
```
Search Student:  [________________]  Search by: ● Name  ○ Roll/Adm No.  ○ Phone
[Search]
```

---

## 3. Fee Collection Flow

### Step 1: Student Search + Fee Display
```
Student: Arjun Sharma (STU-0001187)
Class: XI-A  ·  Father: Rajesh Sharma  ·  Phone: 9876543210

Outstanding Fee — 2026–27:
────────────────────────────────────────────────────────────────────────
Fee Head           Q1 (Apr)   Q2 (Jul)   Q3 (Oct)   Q4 (Jan)   Status
────────────────────────────────────────────────────────────────────────
Tuition (Science)  ₹7,000     ₹7,000     ₹7,000     ₹7,000     Q3, Q4 pending
Development Fee    ₹8,000       —           —           —        ✅ Paid
Lab Fee            ₹1,500       —           —           —        ✅ Paid
Computer Lab Fee   ₹1,000       —           —           —        ✅ Paid
Exam Fee           ₹500         —           —           —        ✅ Paid
Library Fee        ₹500         —           —           —        ✅ Paid
Annual Day         —          ₹1,200       —           —        ✅ Paid
Board Exam Fee     —          ₹1,500       —           —        ✅ Paid
────────────────────────────────────────────────────────────────────────
Currently Due:     Q3 Tuition: ₹7,000  +  Late Fee: ₹100  =  ₹7,100
Q4 Tuition due Jan 1: ₹7,000 (can pay in advance)

Merit Scholarship (25%): Applied → Tuition ₹7,000 → Effective ₹5,250/quarter
                          Outstanding (Q3): ₹5,250 + Late Fee ₹100 = ₹5,350

[Collect Q3 ₹5,350]  [Collect Q3 + Q4 (advance) ₹10,500]  [Custom Amount]
```

### Step 2: Payment Mode
```
Payment Mode:
● Cash        Amount: ₹5,350     Notes: [                ]
○ Cheque      Cheque No.:        Bank:       Date:
○ DD          DD No.:            Bank:       Date:
○ NEFT/RTGS   UTR No.:           Date:       Bank:
○ UPI         UPI Ref.:          Date:
○ Online (auto-reconciled from D-05)

[Generate Receipt]
```

### Step 3: Receipt Preview + Print
```
┌──────────────────────────────────────────────────────┐
│           [SCHOOL LOGO]  FEE RECEIPT                 │
│        [School Name] · Affiliation: AP2000123        │
│                                                       │
│  Receipt No.: R/2026/7834        Date: 26 Mar 2026   │
│  Student: ARJUN SHARMA           Class: XI-A         │
│  Admission No.: GVS/2026/0187    Father: Rajesh S.   │
│                                                       │
│  Fee Details:                                         │
│  Q3 Tuition (Science XI)   ₹7,000                   │
│  Less: Merit Scholarship   -₹1,750 (25%)             │
│  Net Tuition               ₹5,250                    │
│  Late Fee                  ₹100                      │
│  ─────────────────────────────                       │
│  TOTAL PAID                ₹5,350                    │
│  Mode: Cash                                           │
│                                                       │
│  [Education service — GST Exempt u/s 2(y) IGST Act]  │
│  Cashier: Meera (Fee Clerk)                           │
│  [School Seal]                                        │
└──────────────────────────────────────────────────────┘

[Print Receipt]  [Send WhatsApp]  [Save & Continue]
```

---

## 4. RTE Student Block

If student is flagged as RTE (C-07):
```
⚠️ RTE STUDENT — NO FEE TO BE COLLECTED
Arjun Kumar is admitted under RTE Section 12(1)(c) quota.
Fee collection from RTE students is prohibited under RTE Act 2009.

[Close]
```
The [Generate Receipt] button is replaced with this block — no fee can be collected.

---

## 5. Multiple Students in One Visit

[+ Add Another Student] → allows collecting fee for 2–3 students (siblings) in one counter visit. Each student gets a separate receipt; payments are processed individually.

---

## 6. Day Close

[Day Close Report] at end of day:
```
Day Close — 26 Mar 2026

Mode          Receipts   Amount
Cash              12     ₹96,400
Cheque             2     ₹18,000
UPI               18    ₹1,42,600
NEFT               6     ₹1,27,200
─────────────────────────────────
TOTAL             38    ₹3,84,200

Cash: Opening Balance ₹10,000 + Collections ₹96,400 = ₹1,06,400
      Less: Float retained ₹10,000 = ₹96,400 to be deposited

[Generate Day Close Report PDF]  [Mark Day Closed]
```

---

## 7. Receipt Printer Integration

EduForge supports:
- **Thermal printer (80mm):** Common at school counters; receipt prints in 2 seconds
- **A4 laser print:** Full-page receipt for official purposes
- **WhatsApp receipt:** PDF sent to parent's WhatsApp (₹0 extra)
- **Email receipt:** PDF to parent's email

Receipt printer is configured in school settings (A-06); the system uses ESC/POS protocol for thermal printers.

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/students/{student_id}/outstanding/?year={year}` | Student outstanding fee breakdown |
| 2 | `POST` | `/api/v1/school/{id}/fees/collect/` | Record payment + generate receipt |
| 3 | `GET` | `/api/v1/school/{id}/fees/receipts/{receipt_id}/pdf/` | Fetch receipt PDF |
| 4 | `POST` | `/api/v1/school/{id}/fees/receipts/{receipt_id}/send-whatsapp/` | Send receipt to parent |
| 5 | `GET` | `/api/v1/school/{id}/fees/day-close/?date={date}` | Day close summary |
| 6 | `POST` | `/api/v1/school/{id}/fees/day-close/` | Mark day as closed |

---

## 9. Business Rules

- Receipts are numbered sequentially: `R/{YEAR}/{SEQ}` — no gaps allowed; voids are noted as "CANCELLED"
- A receipt once generated cannot be modified — only cancelled (with Principal approval in D-06); the original and cancelled copies both remain in the register
- Cash collected must equal cash deposited; shortfalls are logged as discrepancies and flagged to the Accountant
- No fee collection is possible if the fee structure for the current year (D-01) has not been published
- Cheques are marked as "collected" but revenue is booked only when the Accountant marks "cheque cleared" (D-18 bank reconciliation)
- Late fee is automatically included in the outstanding amount — the Fee Clerk cannot manually remove late fee; only a waiver (D-03) removes it

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
