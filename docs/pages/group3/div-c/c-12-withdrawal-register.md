# C-12 — Withdrawal & Dropout Register

> **URL:** `/school/students/withdrawals/`
> **File:** `c-12-withdrawal-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Administrative Officer (S3) — full · Academic Coordinator (S4) — full · Principal (S6) — full

---

## 1. Purpose

Maintains the register of students who have left the school mid-year or at year-end — covering voluntary withdrawals (family relocation, school change), dropouts (stopped attending without formal withdrawal), expulsions (rare), and students who completed Class XII and graduated.

This register serves several important purposes:
- **CBSE inspection:** Inspectors check that every student who appeared in rolls at start of year either appears in end-of-year rolls OR is accounted for in the withdrawal register
- **RTE compliance:** Dropout tracking is mandatory — schools must report dropout rates; high dropout rates (especially in Classes I–V for RTE students) trigger state government scrutiny
- **UDISE data:** Dropout count is a key metric in UDISE annual submission; under-reporting dropouts inflates UDISE student counts
- **Fee clearance:** Withdrawal is blocked if outstanding fees exist (or Principal override to issue TC despite dues, which is tracked)
- **TC issuance gate:** TC (C-13) can only be generated after the student is formally recorded as withdrawn

---

## 2. Page Layout

### 2.1 Header
```
Withdrawal & Dropout Register — 2025–26      [+ Record Withdrawal]  [Export Register]
Withdrawals Recorded: 18  ·  Dropouts: 3  ·  Graduated (XII): 34  ·  Expulsions: 0
```

### 2.2 Register Table
| W-No. | Student | Class | Withdrawal Type | Date | Fees Cleared | TC Status | Reason |
|---|---|---|---|---|---|---|---|
| W-2026-018 | Priya Das | VIII-A | Transfer (voluntary) | 20 Mar 2026 | ✅ Cleared | ✅ Issued | Family relocation — Bengaluru |
| W-2026-017 | Suresh K. | X-B | Transfer (voluntary) | 15 Mar 2026 | ✅ Cleared | ⏳ Pending | Father transferred to Chennai |
| W-2026-003 | Arun M. | VI-B | Dropout | 30 Jun 2025 | — | N/A | Stopped attending; unresponsive |
| W-2025-034 | All XII-A | XII-A | Graduation | 31 Mar 2026 | ✅ | N/A | Passed Class XII board exam |

---

## 3. Record Withdrawal

[+ Record Withdrawal] → form:

| Field | Value |
|---|---|
| Student | [Search] |
| Withdrawal Type | Voluntary Transfer · Dropout · Expulsion · Graduation · Death · Long Medical Absence |
| Date of Last Attendance | 19 Mar 2026 |
| Official Withdrawal Date | 20 Mar 2026 |
| Reason | Family relocation to Bengaluru |
| Destination School (if transfer) | DPS Bengaluru (if known) |
| Parent Request | Received (letter/verbal) |
| TC Requested | Yes / No |
| Fees Outstanding | ₹0 (Cleared) |
| Fee Dues | If outstanding: [View dues] — system shows amount from div-d |
| Allow TC despite dues | ⬜ (requires Principal override with note) |
| Principal Approval | Required for expulsion and TC despite dues |

---

## 4. Fee Clearance Check

Before withdrawal is confirmed:

```
Fee Clearance Check — Priya Das (STU-0001050)
Academic Year 2025–26:
  Total Due: ₹72,000
  Paid:      ₹72,000
  Outstanding: ₹0

Annual Charges:
  Library: ₹500    Paid ✅
  Exam:    ₹500    Paid ✅

Security Deposit: ₹5,000 → [Process Refund] (refunded on withdrawal)

Status: ✅ Fee account cleared — TC can be issued
```

If dues exist:
```
Outstanding: ₹18,000 (Q4 instalment — January 2026)

Options:
○ Collect fees before issuing TC
○ Principal override: Issue TC despite dues [Requires reason note]
   (This is logged permanently and visible in fee audit)
```

---

## 5. Dropout Tracking

For students who stopped attending without formal withdrawal:

```
Potential Dropout Alert — Arun M. (VI-B)
Last Attendance: 25 Jun 2025
Absent: 22 consecutive days

Attempts to Contact:
  28 Jun 2025: Class Teacher called father — number unreachable
  5 Jul 2025:  Home visit by class teacher — family left residence
  10 Jul 2025: Registered letter sent to address — returned undelivered

Status: Marked as Dropout
RTE Category: ✅ Was RTE student — Dropout reported to State DEO (OOSC register)
```

Dropouts are automatically:
1. Listed in the UDISE OOSC (Out-of-School Children) report
2. Reported to A-29 Compliance Dashboard
3. If RTE student — reported to state RTE coordinator

---

## 6. Class XII Graduation

At year-end, after CBSE results for Class XII are declared:
- Academic Coordinator bulk-marks all passed XII students as "Graduated"
- They are moved to Alumni Registry (C-22) automatically
- Their student profile is marked Inactive (but full historical record preserved)
- No TC is issued for graduates (TC is for mid-school transfers only)

```
Class XII Graduation — 2026
Students in Class XII: 34
CBSE Result: 34 Passed, 0 Compartment, 0 Failed
[Mark All as Graduated → Move to Alumni]
```

---

## 7. Withdrawal Register Export

[Export Register] → CBSE format:

```
WITHDRAWAL & LEAVERS' REGISTER — 2025–26
[School Name]  |  Affiliation No.: AP2000123

W-No.  Admission No.  Student Name  Class  Date of Admission  Date of Withdrawal  Reason  TC No.
W-001  GVS/2023/0124  Priya Das     VIII   01 Apr 2023        20 Mar 2026         Transfer TC/2026/018
...
```

This format matches the CBSE mandatory register format. CBSE inspectors check this during annual/periodic inspections.

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/withdrawals/?year={year}` | Withdrawal register |
| 2 | `POST` | `/api/v1/school/{id}/students/withdrawals/` | Record withdrawal |
| 3 | `GET` | `/api/v1/school/{id}/students/withdrawals/{withdrawal_id}/` | Withdrawal detail |
| 4 | `GET` | `/api/v1/school/{id}/students/withdrawals/{student_id}/fee-check/` | Fee clearance status before TC |
| 5 | `POST` | `/api/v1/school/{id}/students/withdrawals/graduation/bulk/` | Bulk graduation mark for Class XII |
| 6 | `GET` | `/api/v1/school/{id}/students/withdrawals/export/?year={year}` | Export CBSE format register |

---

## 9. Business Rules

- TC cannot be generated (C-13) for a student who is not recorded in the withdrawal register — this is a hard dependency
- Dropout (not voluntary withdrawal) students must have at least 2 documented contact attempts logged before being marked as dropout
- RTE student dropouts must be reported to the state education department within 15 days of marking as dropout
- A withdrawal entry cannot be deleted once created; it can be reversed (student re-enrolled) only through a new enrollment in C-05 with a fresh enrollment record
- Security deposit refund processing is triggered automatically when withdrawal is recorded; actual payment is processed through the fee module (div-d)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
