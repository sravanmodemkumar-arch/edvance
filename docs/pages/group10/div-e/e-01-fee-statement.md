# E-01 — Fee Statement (Cross-Institution)

> **URL:** `/student/fees`
> **File:** `e-01-fee-statement.md`
> **Priority:** P1
> **Roles:** Student (S3–S6) · Parent (full view + can pay for minors)

---

## Overview

Unified fee dashboard showing all dues, paid amounts, and upcoming payments across every institution and subscription the student is linked to. Ravi sees his school fee (Sri Chaitanya, ₹45,000/term), coaching fee (TopRank, ₹8,500/month), and EduForge Premium subscription (₹2,499/year) — all in one view. This eliminates the problem of juggling multiple institution portals for fee tracking. The parent (Mrs. Lakshmi Devi) sees the same view in the Parent Portal and can pay directly. Late fees, discounts, and instalment plans are shown per institution.

---

## 1. Fee Overview Dashboard

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MY FEES & PAYMENTS                                    Academic Year 2025-26│
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐│
│  │ 💰 Total Due │  │ ✅ Total Paid│  │ ⏰ Upcoming  │  │ ⚠️ Overdue      ││
│  │ ₹8,500       │  │ ₹1,42,499   │  │ ₹45,000      │  │ ₹8,500          ││
│  │ this month   │  │ this year    │  │ next month   │  │ TopRank Apr      ││
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘│
│                                                                              │
│  ── INSTITUTION-WISE BREAKDOWN ──────────────────────────────────────────   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  🏫 Sri Chaitanya Junior College, Kukatpally                          │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │  Annual fee: ₹90,000 · Paid: ₹45,000 · Due: ₹45,000 (Term 2)      │  │
│  │  Due date: 15-Apr-2026 · Status: ✅ On time                         │  │
│  │                                                                       │  │
│  │  ┌──────────────────┬──────────┬──────────┬───────────┬────────────┐ │  │
│  │  │ Item             │ Amount   │ Paid     │ Due       │ Date       │ │  │
│  │  ├──────────────────┼──────────┼──────────┼───────────┼────────────┤ │  │
│  │  │ Tuition (Term 1) │ ₹35,000  │ ₹35,000  │ ✅ Paid  │ 15-Jun-25  │ │  │
│  │  │ Lab fee (Term 1) │ ₹5,000   │ ₹5,000   │ ✅ Paid  │ 15-Jun-25  │ │  │
│  │  │ Library (Annual) │ ₹2,000   │ ₹2,000   │ ✅ Paid  │ 15-Jun-25  │ │  │
│  │  │ Exam fee (SA-2)  │ ₹3,000   │ ₹3,000   │ ✅ Paid  │ 10-Feb-26  │ │  │
│  │  │ Tuition (Term 2) │ ₹35,000  │ —        │ ₹35,000  │ 15-Apr-26  │ │  │
│  │  │ Lab fee (Term 2) │ ₹5,000   │ —        │ ₹5,000   │ 15-Apr-26  │ │  │
│  │  │ Sports fee       │ ₹5,000   │ —        │ ₹5,000   │ 15-Apr-26  │ │  │
│  │  └──────────────────┴──────────┴──────────┴───────────┴────────────┘ │  │
│  │                                                                       │  │
│  │  [Pay ₹45,000 →]  [Pay in 3 EMIs →]  [Download Statement ↓]        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  🎓 TopRank JEE Academy, Ameerpet                    ⚠️ OVERDUE      │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │  Monthly fee: ₹8,500 · Due: 01-Apr-2026 · Status: ⚠️ Overdue       │  │
│  │  Late fee after 10-Apr: ₹500 extra                                  │  │
│  │                                                                       │  │
│  │  ┌──────────────────┬──────────┬──────────┬───────────┬────────────┐ │  │
│  │  │ Month            │ Amount   │ Paid     │ Due       │ Status     │ │  │
│  │  ├──────────────────┼──────────┼──────────┼───────────┼────────────┤ │  │
│  │  │ January 2026     │ ₹8,500   │ ₹8,500   │ ✅ Paid  │ On time    │ │  │
│  │  │ February 2026    │ ₹8,500   │ ₹8,500   │ ✅ Paid  │ On time    │ │  │
│  │  │ March 2026       │ ₹8,500   │ ₹8,500   │ ✅ Paid  │ 3 days late│ │  │
│  │  │ April 2026       │ ₹8,500   │ —        │ ₹8,500   │ ⚠️ Due now│ │  │
│  │  └──────────────────┴──────────┴──────────┴───────────┴────────────┘ │  │
│  │                                                                       │  │
│  │  [Pay ₹8,500 Now →]  (pay before 10-Apr to avoid ₹500 late fee)    │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  ⭐ EduForge Premium Subscription                                     │  │
│  │  Plan: Annual · ₹2,889.82 (paid) · Valid until 31-Mar-2027          │  │
│  │  Auto-renewal: ON · [Manage Subscription →]                          │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Working Professional — Subscription Only

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MY FEES & PAYMENTS                                          Suresh Babu    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  ⭐ EduForge Premium — Monthly Plan                                   │  │
│  │  ₹352.82/month (incl. GST) · Auto-renewal: ON                       │  │
│  │  Next payment: 01-May-2026 via UPI (sureshbabu@ybl)                 │  │
│  │                                                                       │  │
│  │  [Change plan]  [Cancel auto-renewal]  [Payment history ↓]          │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  No institution fees — Suresh is self-registered on exam domains only.     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/student/fees/summary` | Total due, paid, upcoming, overdue |
| 2 | `GET` | `/api/v1/student/fees/institutions` | Fee breakdown per institution |
| 3 | `GET` | `/api/v1/student/fees/institutions/{id}/statement` | Detailed fee statement |
| 4 | `GET` | `/api/v1/student/fees/institutions/{id}/statement/pdf` | Download PDF statement |
| 5 | `GET` | `/api/v1/student/fees/subscription` | Subscription billing details |
| 6 | `GET` | `/api/v1/student/fees/payment-history` | All payments across all sources |

---

## 4. Business Rules

- The fee statement aggregates data from multiple sources: institution fees come from each institution's billing system via API (Group 2/3/4/5 portals manage fee structures), and subscription fees come from EduForge's billing system; the student sees ONE unified view — they don't need to log into Sri Chaitanya's portal and TopRank's portal separately; fee data refreshes every hour via a background sync job; instant refresh is triggered when a payment is made.

- Overdue detection and late fee calculation is handled by the institution — EduForge displays the institution's late fee policy but does not add its own late fees; each institution configures their grace period (typically 5–10 days) and late fee amount in their admin portal; the "⚠️ OVERDUE" badge and red styling appear on the student's dashboard starting from the day after the due date; the parent also receives a WhatsApp notification: "Coaching fee ₹8,500 is overdue. Pay now to avoid ₹500 late fee. [Pay →]"

- For minors (under 18), fee payments require parent's mobile OTP — the student can view the fee statement but the "Pay" button sends an OTP to the parent's registered mobile; this prevents minors from making unauthorized payments; for adults (18+), the student can pay directly using any supported payment method without parent involvement.

- EMI/instalment options are offered by the institution — if Sri Chaitanya allows term fees to be split into 3 monthly instalments, the "Pay in 3 EMIs" option appears; EduForge facilitates the display but the instalment agreement is between the student and the institution; EduForge Premium subscription does not offer EMI below ₹2,000 (annual plan at ₹2,499 shows no-cost EMI on credit cards only).

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division E*
