# G-05 — Fee Defaulters Management

> **URL:** `/coaching/finance/defaulters/`
> **File:** `g-05-defaulters.md`
> **Priority:** P1
> **Roles:** Accounts (K5) · Branch Manager (K6) · Batch Coordinator (K4 — read alerts only)

---

## 1. Defaulters Overview

```
FEE DEFAULTERS — Toppers Coaching Centre
As of 30 March 2026

  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  TOTAL DEFAULTERS: 62  │  AMOUNT OVERDUE: ₹ 5,87,200  │  Avg overdue: 26 d │
  └──────────────────────────────────────────────────────────────────────────────┘

  AGING BUCKETS:
    Bucket         │ Students │ Amount Due    │ Action Status
    ───────────────┼──────────┼───────────────┼────────────────────────────────
    1–15 days      │    32    │ ₹ 3,06,400   │ Auto-reminders active
    16–30 days     │    18    │ ₹ 1,72,800   │ Counsellor calls initiated
    31–60 days     │     8    │ ₹    72,000  │ Branch Manager escalated
    > 60 days      │     4    │ ₹    36,000  │ Final notice sent — deadline Apr 7
    ───────────────┴──────────┴───────────────┴────────────────────────────────

  BATCH-WISE DEFAULT DISTRIBUTION:
    SSC CGL Morning:   18 defaulters  |  ₹ 1,72,800
    Banking Morning:   11 defaulters  |  ₹ 1,03,400
    SSC CGL Evening:   12 defaulters  |  ₹ 1,14,000
    RRB NTPC:           9 defaulters  |  ₹    85,500
    Others:            12 defaulters  |  ₹ 1,11,500
```

---

## 2. Defaulter Detail

```
DEFAULTER PROFILE — Pavan Reddy (TCC-2428)
Batch: SSC CGL Morning | Overdue: 60 days | Amount: ₹ 9,000

  FEE HISTORY:
    Instalment 1 (Aug 2025):  ₹ 10,620 — ✅ PAID (on time)
    Instalment 2 (due Jan 26): ₹ 10,620 — ❌ OVERDUE (60 days)
    Total outstanding:         ₹ 10,620 (incl. GST) → ₹ 9,000 base + ₹ 1,620 GST

  COMMUNICATION LOG:
    Jan 28 — Auto SMS (Day +7): "₹9,000 due for Jan instalment. Pay to continue access."
    Feb 4  — Auto WhatsApp (Day +14): same message
    Feb 18 — Counsellor call (Day +28): "Will pay by Feb 28 (salary issue)"
    Mar 1  — No payment. Auto escalation to Branch Manager.
    Mar 10 — Branch Manager call: "Personal emergency — exams approaching, will pay Apr 1"
    Mar 29 — Final notice letter (Branch Manager approved): "Pay by Apr 7 or access restricted"

  ACADEMIC PERFORMANCE (for context):
    Attendance: 58.3% (below 60% cutoff — already on at-risk list)
    Test avg:   38.2/100 (weak)
    At-risk status: Multiple flags (attendance + score + fee)

  BRANCH MANAGER NOTE:
    "Student appears genuinely stressed (60-day overdue + poor academics).
     Recommend counsellor session before access restriction.
     If no payment by Apr 7, restrict test access (not class attendance)."

  [Send Reminder]   [Log Call]   [Restrict Access (after Apr 7)]   [Waive (with approval)]
```

---

## 3. Collection Campaign

```
COLLECTION CAMPAIGN — March 2026 End-of-Month Drive
Target: Recover ₹5,87,200 from 62 students

  CAMPAIGN ACTIONS:
    Mar 25: Batch-level SMS to all defaulters' batches (aggregate reminder)
    Mar 28: Personal WhatsApp to 30 students (1–30 day overdue)
    Mar 29: Counsellor call list generated for 18 students (16–30 days)
    Mar 30: Final notice letters dispatched for 4 students (> 60 days)
    Apr 1:  Auto-reminder for students with Apr 1–7 due dates

  CAMPAIGN RESULTS (so far):
    Amount recovered (Mar 25–30):  ₹ 1,24,600 from 14 students ✅
    Still outstanding:             ₹ 4,62,600 from 48 students

  RECOVERY TARGETS:
    By Apr 7:   ₹ 1,80,000  (20 students — includes final notice group)
    By Apr 15:  ₹ 2,40,000  (full month target)
    Remaining:  ₹    42,600  (chronic defaulters — escalation decisions needed)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/finance/defaulters/?batch={bid}` | Defaulters list by batch |
| 2 | `GET` | `/api/v1/coaching/{id}/finance/defaulters/{sid}/` | Detailed defaulter profile |
| 3 | `POST` | `/api/v1/coaching/{id}/finance/defaulters/{sid}/action/` | Log action (call, notice, restrict) |
| 4 | `POST` | `/api/v1/coaching/{id}/finance/defaulters/campaign/` | Launch collection campaign with bulk actions |
| 5 | `POST` | `/api/v1/coaching/{id}/finance/defaulters/{sid}/restrict/` | Apply access restriction |
| 6 | `GET` | `/api/v1/coaching/{id}/finance/defaulters/aging/` | Aging bucket summary |

---

## 5. Business Rules

- Fee defaulter management uses a graduated response protocol: automated reminders in the first two weeks, personal contact in weeks 3–4, management escalation after 30 days, and formal notice after 60 days; this escalation ladder gives students adequate opportunity to pay before any punitive action; bypassing the ladder (restricting access on day 8 because the accounts team was annoyed) is not permitted; the audit trail must show each escalation step was taken before the next was triggered
- Portal access restriction (blocking test access) is specifically NOT applied to classroom attendance; a student who cannot pay the fee still has the right to attend classes — the service partially rendered cannot be fully withheld; restricting classroom access would prevent the student from learning while waiting for a payment situation to resolve; however, new test access, new study material downloads, and live online sessions can be restricted; this balance is legal and ethical under consumer protection norms
- Fee waiver (reducing or eliminating an overdue balance) is a Director-level decision and cannot be made by the Branch Manager, Accounts team, or Batch Coordinator; the only exception is a court-ordered insolvency situation; a fee waiver permanently reduces TCC's revenue; the Director reviews waiver requests with the financial and student context before deciding; historically, waivers are granted for genuine medical emergencies (hospitalisation during the course) and deaths in the family, not for financial convenience
- A student who is both a fee defaulter AND academically at-risk (low attendance + low scores) is in a "dual-risk" category; the Branch Manager reviews dual-risk cases personally; the question is whether the financial hardship is causing the academic decline (student is stressed) or whether the student has disengaged and won't pay for a service they aren't using; the response is different: the first case warrants support and flexibility; the second case may need an honest conversation about whether the student should defer to the next batch
- Recovery rates (amount recovered as % of overdue) are tracked monthly; a consistent recovery rate below 60% means TCC's instalment plan is attracting students who cannot sustain the payment schedule; it may also indicate the Admissions team is enrolling students without adequate financial commitment check; the Branch Manager reviews both recovery rate and the "loss-to-dropout-with-outstanding-fee" rate (students who drop out and don't pay) to calibrate the admissions quality bar

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division G*
