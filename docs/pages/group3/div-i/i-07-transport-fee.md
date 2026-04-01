# I-07 — Transport Fee

> **URL:** `/school/transport/fees/`
> **File:** `i-07-transport-fee.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Transport In-Charge (S3) — configure route rates · Accounts Officer (S3) — billing and collection · Administrative Officer (S3) — view · Parent (via Parent Portal N-10) — view own dues and pay

---

## 1. Purpose

Transport fee is a separate billing component from tuition — it is charged only to students enrolled on school bus routes (I-03). Key billing characteristics:
- Charged per term (or monthly in some schools — configurable)
- Fee varies by route (distance/fuel cost determines rate)
- Mid-term enrollments are prorated from enrollment date
- Mid-term discontinuations are refunded proportionally (school policy — configurable)
- Fee is collected via D-04/D-07 (fee collection module); this page manages configuration and tracking
- Outstanding transport dues block TC issuance (C-13)

---

## 2. Page Layout

### 2.1 Header

```
Transport Fee Management                             [+ New Rate Card]  [Generate Bills]
Academic Year: [2026–27 ▼]  Term: [Term 1 (Apr–Jun) ▼]

Billing summary — Term 1, 2026–27:
  Students enrolled on transport: 240
  Total transport fee billed: ₹10,94,400
  Collected: ₹9,82,000 (89.7%)
  Outstanding: ₹1,12,400 (10.3%)
  Defaulters (>30 days overdue): 8 students
```

### 2.2 Route Rate Card

```
Route Rate Configuration — 2026–27

Route  Name                   Monthly Rate  Per-Term (3 mo)  Annual     Stops  Distance
R01    Chaitanyapuri–School   ₹1,500        ₹4,500           ₹13,500    5      18 km
R02    LB Nagar–School        ₹1,400        ₹4,200           ₹12,600    6      15 km
R03    Dilsukhnagar–School    ₹1,600        ₹4,800           ₹14,400    5      20 km
R04    Vanasthalipuram–School ₹1,667        ₹5,000           ₹15,000    7      24 km
R05    Nagole–School          ₹1,200        ₹3,600           ₹10,800    4      12 km
Staff  Staff transport (Van)  ₹800          ₹2,400           ₹7,200     —      various

Note: Two-way (pickup + drop) is the default rate.
      Pickup-only or drop-only: 60% of full rate (configurable).
```

---

## 3. Student Transport Fee Ledger

### 3.1 Individual Student View

```
Transport Fee — Arjun Sharma (XI-A)  ·  Route R01 (Chaitanyapuri)
Academic Year: 2026–27

Enrollment: Effective 1 April 2026 (full year — two-way)
Annual fee: ₹13,500  ·  Billing mode: Per term

Term         Amount   Due Date     Paid        Receipt No.     Status
Term 1 (Apr) ₹4,500   5 Apr 2026   ₹4,500      TRF/2627/0041   ✅ Paid — 3 Apr 2026
Term 2 (Jul) ₹4,500   5 Jul 2026   ₹4,500      TRF/2627/0188   ✅ Paid — 4 Jul 2026
Term 3 (Oct) ₹4,500   5 Oct 2026   —           —               ⬜ Pending

Fee ledger link: D-07 — General Fee Ledger
```

### 3.2 Transport Fee Collection List

```
Filter: Route [All ▼]  Status [All ▼]  Overdue [Any ▼]

Student         Class  Route  Term 3 Fee  Due Date    Status           Days Overdue
Arjun Sharma    XI-A   R01    ₹4,500      5 Oct 2026  ⬜ Pending       —
Priya Venkat    XI-A   R01    ₹4,500      5 Oct 2026  ⬜ Pending       —
Meena V.        VII-B  R04    ₹5,000      5 Oct 2026  ⬜ Pending       —
Rahul P.        IX-A   R02    ₹4,200      5 Oct 2026  ⚠️ Overdue       18 days
Kiran S.        VIII-A R05    ₹3,600      5 Oct 2026  ⚠️ Overdue       32 days → TC blocked
...

[Send reminder to all pending]  [Export overdue list]  [Bulk generate demand notices]
```

---

## 4. Generate Transport Fee Bills

```
Generate Transport Fee Bills — Term 3 (Oct–Dec 2026)

Generate for: ● All transport students (240)
              ○ Specific route: [R01 ▼]
              ○ Selected students: [Select ▼]

Bill date: [5 October 2026]
Due date: [5 October 2026] (same day — configurable; some schools give 5-day window)

Preview:
  240 bills will be generated
  Total amount: ₹10,94,400

  Route breakdown:
    R01: 44 students × ₹4,500 = ₹1,98,000
    R02: 38 students × ₹4,200 = ₹1,59,600
    R03: 30 students × ₹4,800 = ₹1,44,000
    R04: 55 students × ₹5,000 = ₹2,75,000
    R05: 32 students × ₹3,600 = ₹1,15,200
    Staff: 8 × ₹2,400 = ₹19,200

Auto-notify parents:
  ☑ WhatsApp (F-03 template: TRANSPORT_BILL_GENERATED)
  ☑ Parent portal notification
  ☐ SMS (optional)

[Preview bill for one student]  [Generate All Bills]
```

---

## 5. Mid-Term Enrollment Billing (Prorated)

```
Mid-Term Enrollment — Proration Calculation

Student: Chandana Rao (XI-A)
Route: R03 (Dilsukhnagar) — enrolled effective 15 October 2026
Term 3: 1 October 2026 to 31 December 2026 (92 days)

Proration:
  Full term fee: ₹4,800
  Days remaining from enrollment: 77 days (out of 92)
  Prorated fee: ₹4,800 × (77/92) = ₹4,017.39 → rounded to ₹4,017

Bill generated: TRF/2627/0XX — ₹4,017 — due 15 October 2026

[Confirm and add to D-07 ledger]

Note: Rounding policy (up/down/nearest rupee) is configurable in school settings.
```

---

## 6. Mid-Term Discontinuation Refund

```
Transport Discontinuation Refund — Vijay S. (X-B)

Discontinuation effective: 1 April 2026 (Term 1)
Route R04: ₹5,000/term (Term 1: 1 Apr–30 Jun 2026 = 91 days)

Term 1 already paid: ₹5,000 (Receipt TRF/2627/0079)
Used: 27 March 2026 — 1 April 2026 = only 1 day (enrolling in April, discontinuing in April)

Actually: enrollment was for prior year; discontinuation starts from 1 Apr.
  Days used: 0 (no days in Term 1 2026-27)
  Refund: ₹5,000 (full)

School refund policy:
  ● Prorated refund (default — refund unused days)
  ○ No refund after term begins
  ○ 50% refund only

Refund method:
  ● Credit to student's D-14 security deposit
  ○ Direct bank transfer (requires parent bank details on file)
  ○ Adjust against future fee

[Generate refund voucher]  [Process in D-14]
```

---

## 7. Concession & Waiver

```
Transport Fee Concession — Policy

RTE (Right to Education) students on transport:
  Section 12(1)(c) students admitted under RTE: Transport fee is waived if transport
  is the barrier to school attendance. State government schemes may reimburse the school.
  [Apply RTE transport concession for student]

Sibling concession:
  School policy (configurable): 10% discount for second sibling using same route
  [Apply sibling concession]

Staff child:
  School policy: 25% discount on staff van route
  [Apply staff concession]

Waiver (individual case):
  Reason: [____________]
  Approved by: Principal required for >50% waiver
  [Request waiver → Principal approval queue]
```

---

## 8. GST on Transport Fee

```
GST Applicability — School Transport

CBSE school transport fee:
  Transport provided by school as part of education: GST-EXEMPT under S. No. 66
  of Notification 12/2017 Central Tax (Rate) — educational services exemption

  Condition: Transport must be within same academic institution
  If school outsources transport to a separate legal entity and charges students
  separately → may attract 5% GST (SAC 996411 — passenger transport services)

  EduForge default: Transport fee billed within school = exempt; no GST applied
  If school operates transport through a separate contractor (I-11): consult CA

GST report for transport: [Export]
```

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/fees/rate-card/` | Route rate cards |
| 2 | `POST` | `/api/v1/school/{id}/transport/fees/rate-card/` | Create/update rate card |
| 3 | `POST` | `/api/v1/school/{id}/transport/fees/generate-bills/` | Bulk generate term bills |
| 4 | `GET` | `/api/v1/school/{id}/transport/fees/student/{student_id}/` | Student transport fee ledger |
| 5 | `GET` | `/api/v1/school/{id}/transport/fees/outstanding/` | Outstanding fees list |
| 6 | `POST` | `/api/v1/school/{id}/transport/fees/prorate/` | Calculate prorated fee for mid-term enrollment |
| 7 | `POST` | `/api/v1/school/{id}/transport/fees/refund/` | Calculate and process refund |
| 8 | `POST` | `/api/v1/school/{id}/transport/fees/concession/` | Apply concession/waiver |

---

## 10. Business Rules

- Transport fee rate is configured per route (per-term and per-month equivalents stored); the per-month rate × 3 must equal per-term rate exactly (no rounding discrepancy)
- Transport enrollment (I-03) automatically triggers transport fee billing in D-07; the first bill is prorated from enrollment date
- Students on transport with unpaid fees >30 days: a system flag is set; TC clearance (C-13) is blocked until transport dues are cleared
- RTE-admitted students (Section 12(1)(c)): transport fee must be waived if the student's distance from school exceeds 1 km (primary) or 3 km (secondary) and transport is required for attendance; this is a legal requirement under RTE Act
- Refund computation uses calendar days (not school days) because the bus runs every school day but the term fee covers the term's calendar — school can configure to school-days-based if preferred
- GST: transport fee charged directly by school as part of education services is exempt; if a separate transport company invoices students, that company's GST status applies
- Parent can view transport dues and pay via the Parent Portal (N-10 fee payment page); payment is processed via D-04 payment gateway

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
