# G-06 — Refund Requests & Policy

> **URL:** `/coaching/finance/refunds/`
> **File:** `g-06-refunds.md`
> **Priority:** P2
> **Roles:** Accounts (K5) · Branch Manager (K6) · Director (K7)

---

## 1. Refund Policy

```
REFUND POLICY — Toppers Coaching Centre (AY 2026–27)
Effective: 1 April 2026 | Approved by: Director

  WITHDRAWAL TIMING     │ REFUND AMOUNT                    │ PROCESSING TIME
  ──────────────────────┼──────────────────────────────────┼──────────────────
  Within 7 days of      │ 100% of fee paid (incl. GST)     │ 7 business days
  enrollment (cooling   │ — no deductions                   │
  off period)           │                                   │
  ──────────────────────┼──────────────────────────────────┼──────────────────
  After 7 days, before  │ 75% of base fee (no GST refund)  │ 14 business days
  batch start           │                                   │
  ──────────────────────┼──────────────────────────────────┼──────────────────
  After batch start,    │ 50% of base fee                   │ 14 business days
  within first month    │ (pro-rated for days attended)     │
  ──────────────────────┼──────────────────────────────────┼──────────────────
  After 30 days of      │ No refund (course is non-          │ N/A — declined
  batch attendance      │ refundable after 30 days)          │
  ──────────────────────┼──────────────────────────────────┼──────────────────
  Medical emergency     │ 90% of remaining fee (any stage)  │ 21 business days
  (hospitalisation)     │ requires doctor's certificate +   │ (Director approval)
                        │ hospital discharge summary         │
  ──────────────────────┴──────────────────────────────────┴──────────────────

  GST REFUND NOTE: GST refund requires TCC to file a credit note and adjust
  the subsequent GSTR-1/3B filing. GST refund after 90 days requires GST portal
  amendment — contact Accounts team for timeline.
```

---

## 2. Refund Request Form

```
REFUND REQUEST — #REF-2026-048
Submitted: 28 March 2026 | Accounts team handling: Ms. Revathi

  STUDENT DETAILS:
    Student:   Deepak Reddy (TCC-2488)
    Batch:     SSC CGL Morning (May 2026) — batch starts May 4
    Enrolled:  15 March 2026 (13 days ago)

  FEE PAID:
    Instalment 1:   ₹ 10,620 (paid 15 Mar 2026, UPI: UTR 304120AAAAA)
    Instalment 2:   ₹ 10,620 (not yet paid — due Aug 2026)
    Total paid:     ₹ 10,620

  REASON FOR WITHDRAWAL:
    "Got a government job (TNPSC Group I — result declared Mar 26).
     No longer need SSC CGL coaching. Happy with TCC but must leave."

  REFUND CALCULATION:
    Policy applicable: After 7 days, before batch start → 75% of base fee
    Base fee paid:      ₹ 9,000  (₹10,620 ÷ 1.18)
    75% of base:        ₹ 6,750
    GST:                Not refunded (within 90 days — credit note pending)
    REFUND AMOUNT:      ₹ 6,750

  APPROVAL:
    Accounts review:     ✅ Verified (batch not yet started, 13 days since enrollment)
    Branch Manager:      ✅ Approved (standard policy — no special circumstances)
    Director:            N/A (not required for standard policy refund)

  BANK TRANSFER DETAILS:
    Bank: SBI | A/C: XXXXXX4567 | IFSC: SBIN0020388
    Transfer initiated: 30 Mar 2026 | ETA: Apr 4 (5 business days)

  [Complete Refund Processing]   [Issue Cancellation Acknowledgement]
```

---

## 3. Refund Register

```
REFUND REGISTER — AY 2026–27 (as of 30 Mar 2026)

  Ref No.       │ Student          │ Reason             │ Paid  │ Refund │ Status
  ──────────────┼──────────────────┼────────────────────┼───────┼────────┼──────────────────
  REF-2026-001  │ Ravi Kumar (2210)│ Medical emergency  │ ₹21K  │ ₹17K  │ ✅ Completed
  REF-2026-018  │ Anitha M. (2310) │ Job (7-day cooling)│ ₹10K  │ ₹10K  │ ✅ Completed
  REF-2026-032  │ Suresh P. (2390) │ Relocation         │ ₹21K  │ ₹13K  │ ✅ Completed
  REF-2026-047  │ Kavitha R. (2481)│ Exam cleared       │ ₹10K  │ ₹ 7K  │ ⏳ Processing
  REF-2026-048  │ Deepak R. (2488) │ Exam cleared       │ ₹10K  │ ₹ 7K  │ ⏳ Processing
  ...  (43 more)

  TOTALS (AY 2026–27):
    Total refunds processed:   48
    Total amount refunded:     ₹ 4,82,400
    Avg refund as % of fee:    42.8%  (expected — most are 50–75% policy refunds)
    Refunds > 7 days late:     3  ⚠️ (SLA breach — to be reviewed)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/finance/refunds/policy/` | Current refund policy |
| 2 | `POST` | `/api/v1/coaching/{id}/finance/refunds/request/` | Submit refund request |
| 3 | `PATCH` | `/api/v1/coaching/{id}/finance/refunds/{rid}/approve/` | Approve or reject refund |
| 4 | `POST` | `/api/v1/coaching/{id}/finance/refunds/{rid}/process/` | Mark refund as transferred |
| 5 | `GET` | `/api/v1/coaching/{id}/finance/refunds/register/?year=2026-27` | Full refund register |
| 6 | `GET` | `/api/v1/coaching/{id}/finance/refunds/stats/?year=2026-27` | Refund rate and SLA stats |

---

## 5. Business Rules

- The 7-day cooling-off period is TCC's consumer-protection commitment aligned with Consumer Protection Act 2019 guidelines for service contracts; during this period, the student can cancel for any reason and receive a full refund including GST; TCC processes this within 7 business days; the 7-day period begins from the enrollment date (not the payment date); a student who enrolled on March 15 has until March 22 for a full refund; a student who paid on March 10 but enrolled on March 15 has the same window
- GST refund on coaching fees is technically complex: when a student is refunded, TCC must issue a credit note under CGST Rules 53; the credit note reduces the output GST liability in the period it is issued; if the original invoice was in a different GSTR-1 period (e.g., enrolled in March, refunded in April), the credit note must reference the original invoice; TCC's Accounts team must ensure the credit note is included in the month's GSTR-1 and the tax reduction is reflected in GSTR-3B; this is why GST refunds sometimes take longer than the base fee refund
- Medical emergency refunds (90% of remaining fee, at any stage) are a compassionate policy; the "remaining fee" means the fee for the months of the course not yet attended; a student who completed 4 months of a 10-month course before hospitalisation is eligible for 90% of the remaining 6 months' fee; the Accounts team calculates the pro-rated amount; the 90% (rather than 100%) covers TCC's administrative cost and is disclosed in the enrollment terms; the doctor's certificate and hospital discharge summary are stored in the student's document folder
- Refund processing SLA (7 business days for cooling-off, 14 business days for other cases) is monitored by the Branch Manager; three late refunds in a quarter triggers an accounts team process review; students who have not received their refund within the stated period have a formal escalation right (written complaint to the Director); TCC's reputation depends on honouring refund commitments promptly — coaching centres that delay refunds are frequently featured negatively on education forums
- The "no refund after 30 days of attendance" rule does not apply if TCC itself fails to deliver the promised service (e.g., batch cancelled without replacement, faculty permanently unavailable, branch closes); in such cases, a pro-rated refund of the undelivered service is mandatory under Consumer Protection Act 2019 Section 2(47) (deficiency of service); the Director must authorise such refunds and the reason is disclosed as "service deficiency" in the refund register

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division G*
