# H-09 — Hostel Fees & Billing

> **URL:** `/school/hostel/fees/`
> **File:** `h-09-hostel-fees-billing.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Hostel Accountant (S3) — billing · Administrative Officer (S3) — payment collection · Chief Warden (S4) — billing approval · Principal (S6) — fee structure changes

---

## 1. Purpose

Manages hostel-specific fee billing — distinct from school tuition fees (D-04). Hostel charges are more complex than school fees because they include multiple variable components and are adjusted monthly based on actual usage (mess rebates, medical extras, laundry).

---

## 2. Hostel Fee Structure

```
Hostel Fee Structure — 2026–27

Component               Frequency  Boys Double  Boys Dorm  Girls Single  Notes
Hostel accommodation    Termly     ₹12,000      ₹9,000     ₹15,000      Per bed category
Mess charges            Monthly    ₹3,000       ₹3,000     ₹3,000       3 meals/day
Laundry                 Monthly    ₹400         ₹400       ₹400         Optional (configurable)
Amenities               Termly     ₹500         ₹500       ₹500         Electricity, water share
Hostel caution deposit  One-time   ₹5,000       ₹5,000     ₹5,000       D-14 Security Deposit
Medical room (basic)    Included   —            —          —            Basic medicines free
Medical extras          As used    Actual cost  Actual     Actual        Hospital visits, Rx drugs

Annual hostel cost (Double room): ₹12,000×3 terms + ₹3,000×12 + ₹400×12 + ₹500×3
                                  = ₹36,000 + ₹36,000 + ₹4,800 + ₹1,500 = ₹78,300/year
```

---

## 3. Monthly Bill Generation

```
Monthly Hostel Bill — March 2026 — Arjun Sharma (XI-A, Room 101-A)

Component              Amount    Notes
Mess charges           ₹3,000
Less: Leave rebate      -₹90    (3 days × 3 meals × ₹10 = ₹90 — weekend leave 28–30 Mar)
Laundry                 ₹400
Medical extras          ₹150    (Hospital transport: Apollo visit 5 Mar — ₹150)
Late fee (mess)           ₹0    (No outstanding)
─────────────────────────────────────────────────────────────────────
Total March Hostel Bill: ₹3,460

Term fee (Termly — billed in April): ₹12,000 accommodation + ₹500 amenities = ₹12,500
                                     (not on monthly bill — separate term billing)

[Generate Bill]  [Send to Parent]  [Raise in D-07 Ledger]
```

---

## 4. TC Clearance Certificate

```
Hostel Clearance — Arjun Sharma (Withdrawal)

Outstanding hostel dues: ₹3,460 (March bill — due 31 Mar)
Room vacated: ⬜ Not yet
Bedding returned (H-11): ⬜ Not yet
Locker cleared: ⬜ Not yet
Mess card returned: ⬜ Not yet

Caution deposit refund (D-14):
  Deposited: ₹5,000 (15 Jun 2023)
  Deductions: ₹200 (pillow damaged, H-11)
  Refund: ₹4,800

Clearance status: ❌ Pending (dues not paid; room not vacated)
→ TC (C-13) is blocked until hostel clearance is complete

[Mark Items Complete]  [Issue Hostel Clearance Certificate]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/fees/structure/?year={y}` | Fee structure |
| 2 | `GET` | `/api/v1/school/{id}/hostel/fees/bill/{student_id}/?month={m}&year={y}` | Monthly bill |
| 3 | `POST` | `/api/v1/school/{id}/hostel/fees/bill/{student_id}/generate/` | Generate and add to D-07 |
| 4 | `GET` | `/api/v1/school/{id}/hostel/fees/clearance/{student_id}/` | TC clearance status |
| 5 | `POST` | `/api/v1/school/{id}/hostel/fees/clearance/{student_id}/issue/` | Issue clearance certificate |

---

## 6. Business Rules

- Hostel fees are billed via D-07 student fee ledger — they appear as a separate charge category (Hostel) alongside tuition fees; payment is collected at D-04 fee counter
- Mess rebate is automatically computed from H-04 leave records; the rebate is applied only for approved leave days (not unplanned meal skips)
- Medical extras (hospital visits, prescription drugs) are charged at actual cost with receipts attached; no markup
- Caution deposit (D-14) is held for the duration of the student's stay in the hostel; it is refunded (less deductions) when the student exits hostel; deductions must be itemised and supported by H-11 inventory records
- FRA (Fee Regulatory Authority) oversight: In some states, hostel fees are also regulated by FRA; fee increases above the regulated ceiling (typically 10%/year) require FRA approval

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
