# I-04 — Hostel Fee Management

> **URL:** `/coaching/hostel/fee/`
> **File:** `i-04-hostel-fee.md`
> **Priority:** P1
> **Roles:** Hostel Warden (K3) · Accounts (K5) · Branch Manager (K6)

---

## 1. Hostel Fee Structure

```
HOSTEL FEE STRUCTURE — AY 2026–27

  ROOM TYPE        │ Block │ Per Month  │ GST (12%)  │ Total/Month │ Security Dep.
  ─────────────────┼───────┼────────────┼────────────┼─────────────┼──────────────
  Triple Sharing   │ A & B │ ₹  7,000  │ ₹    840   │ ₹  7,840   │ ₹ 5,000
  Double Sharing   │ A & B │ ₹  9,000  │ ₹  1,080   │ ₹ 10,080   │ ₹ 7,000
  Single Room      │  A    │ ₹ 12,000  │ ₹  1,440   │ ₹ 13,440   │ ₹10,000
  (Single avail only for senior faculty — not students)
  ─────────────────┴───────┴────────────┴────────────┴─────────────┴──────────────

  INCLUDES:
    ✅ Room (bed, mattress, study table, chair, cupboard, shared bathroom)
    ✅ Wifi (100 Mbps shared, 4 GB/day limit per student)
    ✅ AC (Block A — all rooms, Block B — ground floor only)
    ✅ Security (24/7 guard, CCTV)
    ✅ Mess (3 meals/day included — see I-05)
    ✅ Study room access (6 AM – 11 PM)

  GST: SAC 9963 — Accommodation services (12%, not 18% like coaching)
  Exemption: Accommodation < ₹1,000/day is exempt from GST.
             ₹7,000/month = ₹233/day → EXEMPT FROM GST ✅
             ₹9,000/month = ₹300/day → EXEMPT FROM GST ✅
             GST only applies IF daily rate > ₹1,000 (above single-room threshold)
  NOTE: TCC's hostel fee is below the GST threshold — no GST on hostel fees
        GST shown above was hypothetical — HOSTEL FEES ARE GST-EXEMPT ✅
```

---

## 2. Hostel Fee Collection

```
HOSTEL FEE COLLECTION — March 2026

  OVERVIEW:
    Students on monthly fee:   108
    Standard fee (triple):      96 students  × ₹7,000 = ₹6,72,000
    Higher fee (double):        12 students  × ₹9,000 = ₹1,08,000
    GROSS MONTHLY FEE DUE:     ₹7,80,000

    Collected (by 30 Mar):     ₹7,20,000  (92.3%)
    Pending:                   ₹  60,000  (3 students — overdue > 7 days)
    Last month's carryover:    ₹  14,000  (2 students — now 30+ days overdue)

  PAYMENT MODE (March collections):
    UPI:   ₹ 5,04,000 (70.0%)
    Cash:  ₹ 1,44,000 (20.0%)
    NEFT:  ₹    72,000 (10.0%)

  HOSTEL FEE DEFAULTERS (this month):
    Student         │ Room   │ Amount  │ Overdue │ Action
    ────────────────┼────────┼─────────┼─────────┼─────────────────────────────
    Mohammed R.     │ A-12   │ ₹7,000  │ 12 days │ 2nd reminder sent 28 Mar
    Kiran Naidu     │ A-05   │ ₹7,000  │  8 days │ 1st reminder sent 25 Mar
    Sravya Rao      │ B-08   │ ₹7,000  │  9 days │ 1st reminder sent 26 Mar
    Pavan Reddy     │ A-04   │ ₹7,000  │ 35 days │ Combined with course fee overdue
```

---

## 3. Security Deposit Management

```
SECURITY DEPOSIT LEDGER — Active Residents (March 2026)

  Total deposits held:   ₹ 5,40,000  (108 students × ₹5,000 avg)
  Deposits to return (May–Jun 2026, batch ending):  ₹ 3,60,000 est.

  REFUND PROCESS:
    Room inspection (warden signs off): Required before deposit refund
    Damages deducted:   At market rate (documented with photos)
    Refund timeline:    14 days after departure
    Mode:               Bank transfer (no cash refunds for security deposits)

  RECENT REFUNDS:
    Mar 15 — Suresh P. (vacated Room A-07): ₹4,200 refunded (₹800 deducted for broken shelf)
    Mar 20 — Kavitha R. (vacated Room B-12): ₹5,000 full refund ✅ (no damages)

  DAMAGE DEDUCTION POLICY:
    Broken furniture:  Market replacement cost
    Wall damage:       ₹500–₹2,000 (assessed by maintenance)
    Lost key:          ₹300 per key
    Excessive cleaning: ₹200–₹500
    Normal wear:        No deduction (expected over 10 months)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/hostel/fee/structure/` | Fee structure by room type |
| 2 | `GET` | `/api/v1/coaching/{id}/hostel/fee/collections/?month=2026-03` | Monthly collection summary |
| 3 | `POST` | `/api/v1/coaching/{id}/hostel/fee/collect/` | Record a hostel fee payment |
| 4 | `GET` | `/api/v1/coaching/{id}/hostel/fee/defaulters/` | Hostel fee defaulters |
| 5 | `GET` | `/api/v1/coaching/{id}/hostel/fee/deposits/` | Security deposit ledger |
| 6 | `POST` | `/api/v1/coaching/{id}/hostel/fee/deposits/{did}/refund/` | Process deposit refund |

---

## 5. Business Rules

- Hostel fees are charged separately from coaching fees; a student can enroll in coaching without taking a hostel (day scholar) or can stay in the hostel without being enrolled (rare — only for students preparing independently); the two fee systems are linked in the student's profile but have independent collection workflows; a student in financial difficulty who is behind on coaching fees and hostel fees is flagged to the Branch Manager for a combined review (not two separate escalations)
- The hostel fee GST exemption (accommodation < ₹1,000/day) means TCC does not collect GST on hostel fees; this is a financial advantage for students and simplifies accounting (no GST on hostel invoices); however, if TCC were to raise fees to ₹31,000/month (₹1,000/day) or above, GST would become applicable; the fee structure must be reviewed against this threshold in annual pricing decisions; the accounts team verifies the daily equivalent calculation at each fee revision
- Security deposits are held in a separate designated bank account, not in TCC's operating account; this ensures the deposits are available for refund when students leave and are not accidentally used for operating expenses; the designated account balance is reconciled against the deposit ledger quarterly; a reconciliation mismatch (deposits collected > account balance) is a serious financial governance issue requiring Director-level investigation
- Room damage deductions from the security deposit must be documented with dated photographs taken at check-in AND check-out; the warden photographs every room at check-in to establish the baseline condition; a student who damages a room cannot dispute a deduction if TCC has photographic evidence of the damage that wasn't present at check-in; conversely, a student cannot be charged for pre-existing damage if it was photographed at check-in; this documentation system protects both parties
- A hostel student who is behind on hostel fee for more than 30 days is not immediately evicted; the process follows the same graduated escalation as coaching fee defaults (reminders, personal contact, management escalation); however, unlike coaching fee defaults (where only portal access is restricted), a hostel fee default ultimately risks the student losing their bed after 45 days if no payment or arrangement is made; the Branch Manager must approve any eviction decision; eviction of a minor requires parental notification and a 7-day notice period

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division I*
