# D-01 — Fee Structure Manager

> **URL:** `/school/fees/structure/`
> **File:** `d-01-fee-structure.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Accountant (S3) — draft · Principal (S6) — approve + publish

---

## 1. Purpose

Defines the complete fee structure for the academic year — all fee heads (Tuition, Development, Lab, Library, Exam, Transport, Hostel, Activity, etc.), their amounts per class, and the installment schedule. Every other fee operation in div-d depends on this structure being defined and approved first.

In Indian private schools, fee structures are nuanced:
- Different classes pay different amounts (Class I ≠ Class XI)
- Different streams pay different amounts (Science students pay more for labs)
- Different installment schedules (quarterly / termly / monthly / annual)
- Some fee heads are one-time (admission fee), some recurring (tuition), some optional (hostel, transport)
- State Fee Regulatory Authority (FRA) caps: schools in FRA states must not increase fees by more than the FRA-approved percentage year-on-year

Fee structure must be published before the start of the academic year (typically by February for April admission) so parents can see it during admission enquiry.

---

## 2. Page Layout

### 2.1 Header
```
Fee Structure Manager — 2026–27               [+ Add Fee Head]  [Copy from 2025–26]  [Publish]
Status: Draft  ·  Last Modified: 26 Mar 2026 by Accountant Ravi
Principal Approval: ⬜ Pending
FRA Compliance: ✅ Average increase 8.2% (FRA ceiling: 10%)
```

### 2.2 Fee Heads Table

```
Fee Head         Type        Applies To              Amount (Recurring)  Installment
─────────────────────────────────────────────────────────────────────────────────────
Admission Fee    One-time    New students only        ₹25,000            At admission
Tuition Fee      Monthly     All classes (class-wise)  See below         Monthly
Development Fee  Annual      All classes              ₹8,000             Q1 (Apr)
Library Fee      Annual      Classes I–XII            ₹500               Q1
Lab Fee          Annual      Classes VI–XII            ₹1,500            Q1
Computer Lab     Annual      Classes III–XII           ₹1,000            Q1
Exam Fee         Annual      All classes              ₹500               Q1
Annual Day       Annual      All classes              ₹1,200             Q2 (Jul)
Sports Fee       Annual      All classes              ₹800               Q1
Transport Fee    Monthly     Transport opt-in only    Route-wise         Monthly
Hostel Fee       Monthly     Hostel opt-in only       ₹12,000            Monthly
Board Exam Fee   Annual      Class X & XII only       ₹1,500             Q2 (Oct)
```

---

## 3. Tuition Fee — Class-wise

| Class | Monthly Tuition | Annual Tuition |
|---|---|---|
| Nursery–UKG | ₹3,500 | ₹42,000 |
| Class I–II | ₹4,000 | ₹48,000 |
| Class III–V | ₹4,500 | ₹54,000 |
| Class VI–VIII | ₹5,000 | ₹60,000 |
| Class IX–X | ₹5,500 | ₹66,000 |
| Class XI–XII Science | ₹7,000 | ₹84,000 |
| Class XI–XII Commerce | ₹6,000 | ₹72,000 |
| Class XI–XII Arts | ₹5,500 | ₹66,000 |

---

## 4. Installment Schedule

```
2026–27 Installment Schedule

Quarter 1 (Apr 2026):  Tuition (Apr) + Development + Library + Lab + Sports + Exam
Quarter 2 (Jul 2026):  Tuition (Jul) + Annual Day + Board Exam Fee (X, XII only)
Quarter 3 (Oct 2026):  Tuition (Oct)
Quarter 4 (Jan 2027):  Tuition (Jan)

Monthly fee heads (Tuition, Transport, Hostel) are also available as monthly installments.

Grace Period: 15 days after due date before late fee kicks in.
```

---

## 5. Fee Head Configuration

Adding / editing a fee head:

| Field | Value |
|---|---|
| Fee Head Name | Development Fee |
| Fee Head Code | DEV (for reports) |
| Type | One-time · Annual · Monthly · Per-event |
| Applicability | All classes · Specific classes (select) · New students only |
| Amount | ₹8,000 |
| Class-wise Override | Yes → enter per-class amounts |
| Installment Quarter | Q1 |
| GST Applicable | No (education exempt) / Yes → % |
| Refundable on Exit | No · Yes (with conditions) |
| FRA Category | Tuition · Development · Other |

---

## 6. FRA Compliance Check

For states with Fee Regulatory Authority:

```
FRA Compliance Check — 2026–27

State: Telangana  ·  FRA Ceiling: 10% increase over 2025–26

Fee Head        2025–26    2026–27   Increase  Status
Tuition (I–II)  ₹3,700     ₹4,000    8.1%      ✅ Within ceiling
Dev Fee         ₹7,500     ₹8,000    6.7%      ✅
Lab Fee         ₹1,200     ₹1,500    25.0%     ❌ EXCEEDS FRA ceiling — reduce or document reason

You must resolve FRA violations before publishing the fee structure.
```

---

## 7. Transport Fee (Route-wise)

Transport fee varies by route distance:

| Route | Area | Monthly Fee |
|---|---|---|
| Route 1 | Kukatpally 0–3 km | ₹1,200 |
| Route 2 | Miyapur 4–7 km | ₹1,600 |
| Route 3 | Bachupally 8–12 km | ₹2,000 |
| Route 4 | Patancheru 13–18 km | ₹2,400 |

---

## 8. Copy from Previous Year

[Copy from 2025–26] → imports last year's structure with option:
- Keep same amounts (for review and manual update)
- Apply inflation % (e.g., 8%) to all amounts automatically
- Show comparison table before confirming

---

## 9. Publish

[Publish] → requires Principal approval (A-23 workflow):
1. Accountant clicks [Send for Principal Approval]
2. Principal reviews fee structure
3. Principal clicks [Approve & Publish]
4. Fee structure becomes active for 2026–27

Once published:
- Parent portal shows the fee structure when they enquire
- Fee ledgers initialise for all enrolled students
- Fee collection (D-04) becomes active for the year

---

## 10. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/structure/?year={year}` | Fee structure for year |
| 2 | `POST` | `/api/v1/school/{id}/fees/structure/` | Create fee structure |
| 3 | `PATCH` | `/api/v1/school/{id}/fees/structure/{year}/` | Update fee structure |
| 4 | `POST` | `/api/v1/school/{id}/fees/structure/{year}/copy-from/{from_year}/` | Copy from previous year |
| 5 | `GET` | `/api/v1/school/{id}/fees/structure/{year}/fra-check/` | FRA compliance check |
| 6 | `POST` | `/api/v1/school/{id}/fees/structure/{year}/publish/` | Publish (Principal) |
| 7 | `GET` | `/api/v1/school/{id}/fees/structure/{year}/transport/` | Transport routes + fees |

---

## 11. Business Rules

- Fee structure must be published before fee collection (D-04) can begin for the year
- Once published, individual fee head amounts can be changed only by Principal with a reason note (logged); if the FRA has approved the structure, changes require re-approval
- RTE students have ₹0 across all fee heads — the system enforces this by zeroing out all amounts for students flagged as RTE in C-07; any attempt to collect fee from an RTE student triggers an alert
- Transport fee is only charged to students where transport = opted-in (C-05 enrollment field); others are not billed for transport
- Admission fee (one-time) is collected during C-04 seat confirmation and is non-refundable; it does not appear in the recurring installment schedule after first year

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
