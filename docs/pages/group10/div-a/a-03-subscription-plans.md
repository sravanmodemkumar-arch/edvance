# A-03 — Subscription & Plans

> **URL:** `/student/subscription`
> **File:** `a-03-subscription-plans.md`
> **Priority:** P1
> **Roles:** Student (S3–S6) · Parent (can pay for minor) · Institution Admin (bulk gifting)

---

## Overview

Manages the student's subscription state across all exam domains. A student's subscription applies **platform-wide** — Premium unlocks unlimited tests, AI study plan, video library, and advanced analytics across every exam domain they've added. The page handles upgrades, downgrades, renewals, payment history, and institution-gifted premium access. Suresh (28, Vijayawada, working professional, SSC + IBPS + APPSC) who upgrades to Premium for ₹299/month gets unlimited access to all three domains — not ₹299 per domain. Ravi (18, JEE coaching student) has institution-gifted Premium via TopRank Academy and does not need to pay separately.

---

## 1. Current Plan Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MY SUBSCRIPTION                                                             │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  Current Plan: FREE                                                    │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │  Mock tests:    3 of 5 remaining this month (resets 1-Apr-2026)      │  │
│  │  Domains:       SSC CGL · IBPS Clerk · APPSC Group 2                 │  │
│  │  AI study plan: ❌ (Premium only)                                     │  │
│  │  Video library: ❌ (Premium only)                                     │  │
│  │  Analytics:     Basic (score + rank only)                             │  │
│  │                                                                       │  │
│  │  ⭐ Unlock everything — ₹299/month or ₹2,499/year (save 30%)       │  │
│  │  [Upgrade to Premium →]                                               │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ── WHAT YOU'RE MISSING ─────────────────────────────────────────────────   │
│                                                                              │
│  Last month, Premium students in your exam domains scored                    │
│  23% higher on average. Here's what they used:                              │
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐  │
│  │ 📊 AI Study Plan │  │ 🎥 Video Library │  │ 🔬 Topic-wise Analysis  │  │
│  │ Personalised     │  │ 4,200+ hours     │  │ 500+ topics covered     │  │
│  │ daily schedule   │  │ all subjects     │  │ pinpoint weak areas     │  │
│  │ [Preview →]      │  │ [Preview →]      │  │ [Preview →]             │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Plan Comparison Table

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  COMPARE PLANS                                                               │
│                                                                              │
│  ┌────────────────────────┬───────────────┬───────────────┬──────────────┐  │
│  │ Feature                │ Free (₹0)     │ Premium       │ Institution  │  │
│  │                        │               │ (₹299/mo)     │ Gifted       │  │
│  ├────────────────────────┼───────────────┼───────────────┼──────────────┤  │
│  │ Mock tests / month     │ 5             │ Unlimited     │ Unlimited    │  │
│  │ Sectional tests        │ ❌            │ Unlimited     │ Unlimited    │  │
│  │ Previous year papers   │ ✅            │ ✅            │ ✅           │  │
│  │ Notes access           │ Read-only     │ Read+Download │ Read+Download│  │
│  │ Video library          │ ❌            │ 4,200+ hrs    │ 4,200+ hrs   │  │
│  │ AI study plan          │ ❌            │ ✅            │ ✅           │  │
│  │ Doubt resolution       │ Community     │ Priority      │ Priority     │  │
│  │ Performance analytics  │ Basic         │ Advanced      │ Advanced     │  │
│  │ Topic-wise analysis    │ ❌            │ ✅            │ ✅           │  │
│  │ All India Rank (AIR)   │ Rank only     │ Rank+Percentile│ Full        │  │
│  │ Current affairs digest │ Weekly        │ Daily         │ Daily        │  │
│  │ Offline mode           │ ❌            │ ✅            │ ✅           │  │
│  │ Exam domains           │ Unlimited     │ Unlimited     │ As per inst. │  │
│  │ Certificate download   │ ❌            │ ✅            │ ✅           │  │
│  │ Ad-free experience     │ ❌            │ ✅            │ ✅           │  │
│  └────────────────────────┴───────────────┴───────────────┴──────────────┘  │
│                                                                              │
│              [Start Free]    [₹299/month]     [Enter Code]                  │
│                              [₹2,499/year]                                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Payment Flow (Premium Upgrade)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  UPGRADE TO PREMIUM                                                          │
│                                                                              │
│  Choose your billing cycle:                                                  │
│                                                                              │
│  ( ) Monthly — ₹299/month                                                   │
│      Billed monthly. Cancel anytime. Next billing: 1-May-2026              │
│                                                                              │
│  (o) Annual — ₹2,499/year (₹208/month — save ₹1,089!)                     │
│      ⭐ MOST POPULAR — 68% of Premium students choose annual               │
│      Billed once. Valid: 1-Apr-2026 to 31-Mar-2027                         │
│                                                                              │
│  ( ) Quarterly — ₹799/quarter (₹266/month — save ₹398)                    │
│      Billed every 3 months. Next billing: 1-Jul-2026                       │
│                                                                              │
│  ── APPLY COUPON ────────────────────────────────────────────────────────   │
│  [ FIRST50          ] [Apply]  ✅ ₹50 off! New total: ₹2,449/year         │
│                                                                              │
│  ── PAYMENT METHODS ─────────────────────────────────────────────────────   │
│  (o) UPI — GPay / PhonePe / Paytm / BHIM                                   │
│  ( ) Debit Card                                                              │
│  ( ) Credit Card                                                             │
│  ( ) Net Banking                                                             │
│  ( ) Wallet — Paytm / Amazon Pay                                            │
│                                                                              │
│  UPI ID: [ sureshbabu@ybl                                              ]    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  Order Summary                                                         │  │
│  │  Premium Annual Plan             ₹2,499                               │  │
│  │  Coupon (FIRST50)                 -₹50                                │  │
│  │  GST (18%)                        ₹440.82                             │  │
│  │  ──────────────────────────────────────                               │  │
│  │  Total                            ₹2,889.82                           │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ☐ I agree to auto-renewal. Cancel anytime from Settings.                   │
│                                                                              │
│                        [ Pay ₹2,889.82 → ]                                  │
│                                                                              │
│  🔒 Secure payment via Razorpay. 100% refund within 7 days if unsatisfied. │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Subscription Management (Active Premium)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MY SUBSCRIPTION                                                             │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  ⭐ PREMIUM — Annual Plan                                              │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │  Started: 1-Apr-2026 · Expires: 31-Mar-2027 (365 days remaining)    │  │
│  │  Paid: ₹2,889.82 (incl. GST) on 1-Apr-2026 via UPI                 │  │
│  │  Auto-renewal: ON · Next charge: 1-Apr-2027                         │  │
│  │                                                                       │  │
│  │  [Download Invoice]  [Turn off auto-renewal]  [Change plan]          │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ── USAGE THIS MONTH ────────────────────────────────────────────────────   │
│  Mock tests taken:    18 (unlimited)                                        │
│  Sectional tests:     42                                                    │
│  Video hours watched: 14.5 hrs                                              │
│  AI study plan days:  28 of 31                                              │
│  Doubts resolved:     7 (avg response: 2.3 hrs)                            │
│  Notes downloaded:    12                                                    │
│                                                                              │
│  ── PAYMENT HISTORY ─────────────────────────────────────────────────────   │
│  ┌──────────┬──────────────────────┬───────────┬────────────┬────────────┐  │
│  │ Date     │ Description          │ Amount    │ Method     │ Invoice    │  │
│  ├──────────┼──────────────────────┼───────────┼────────────┼────────────┤  │
│  │ 01-Apr-26│ Premium Annual       │ ₹2,889.82│ UPI        │ [PDF ↓]   │  │
│  │ 01-Jan-26│ Premium Monthly      │ ₹352.82  │ UPI        │ [PDF ↓]   │  │
│  │ 01-Dec-25│ Premium Monthly      │ ₹352.82  │ Paytm      │ [PDF ↓]   │  │
│  └──────────┴──────────────────────┴───────────┴────────────┴────────────┘  │
│                                                                              │
│  ── INSTITUTION-GIFTED (shown if applicable) ────────────────────────────   │
│  TopRank JEE Academy has gifted Premium access for your JEE preparation.    │
│  Valid: Apr 2025 – Mar 2026. If institution stops, your personal             │
│  subscription (if any) takes over automatically.                             │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Scholarship & Subsidised Access

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  SCHOLARSHIP & SUBSIDISED ACCESS                                             │
│                                                                              │
│  ── MERIT SCHOLARSHIP ───────────────────────────────────────────────────   │
│  Score 80%+ in your first 3 mock tests → 6 months Premium FREE              │
│  Your status: 2 of 3 qualifying tests completed                             │
│  Test 1: SSC CGL Mock #3 — 82.5% ✅                                        │
│  Test 2: SSC CGL Mock #5 — 79.0% ❌ (need 80%+)                            │
│  Test 3: Not attempted yet                                                   │
│  [Take qualifying test →]                                                    │
│                                                                              │
│  ── SC/ST/EWS SUBSIDY ──────────────────────────────────────────────────   │
│  If you belong to SC/ST/EWS category, you may be eligible for               │
│  Premium at ₹99/year (67% subsidy).                                        │
│  [Apply with income certificate →]                                          │
│                                                                              │
│  ── GOVERNMENT SCHEME ───────────────────────────────────────────────────   │
│  PMKVY / Skill India / AP Yuva Nestham participants:                        │
│  Full Premium access sponsored by scheme. Enter scheme ID:                  │
│  [ ________________ ] [Verify & Activate →]                                 │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/student/subscription` | Current plan, expiry, usage stats |
| 2 | `GET` | `/api/v1/plans` | All available plans with pricing |
| 3 | `POST` | `/api/v1/student/subscription/upgrade` | Initiate upgrade (returns Razorpay order_id) |
| 4 | `POST` | `/api/v1/student/subscription/verify-payment` | Verify Razorpay payment signature |
| 5 | `PUT` | `/api/v1/student/subscription/auto-renew` | Toggle auto-renewal on/off |
| 6 | `POST` | `/api/v1/student/subscription/cancel` | Cancel subscription (effective at period end) |
| 7 | `POST` | `/api/v1/student/subscription/apply-coupon` | Validate and apply coupon code |
| 8 | `GET` | `/api/v1/student/subscription/invoices` | List all payment invoices |
| 9 | `GET` | `/api/v1/student/subscription/invoices/{id}/pdf` | Download invoice PDF |
| 10 | `POST` | `/api/v1/student/subscription/scholarship/apply` | Apply for merit/subsidy scholarship |
| 11 | `POST` | `/api/v1/student/subscription/redeem-scheme` | Redeem government scheme ID |

---

## 7. Business Rules

- Premium subscription is **platform-wide, not domain-specific** — paying ₹299/month unlocks unlimited access across every exam domain the student has added (SSC + Banking + Railways + State PSC, all included); this is a deliberate pricing strategy to maximize student engagement and reduce churn — students who prepare for multiple exams simultaneously have 3.2x lower churn rate than single-domain students; the only exception is institution-gifted access, which may be scoped to specific domains as defined by the institution's bulk licence agreement (e.g., TopRank buys JEE-only licences, their students get Premium for JEE but Free for SSC unless they self-purchase).

- Payment processing uses Razorpay as the primary gateway with Paytm as fallback — 62% of payments are via UPI (GPay, PhonePe, Paytm), 18% debit card, 12% net banking, 8% wallets; the payment flow is optimized for ₹8,000 Android phones where Razorpay's standard checkout handles UPI intent seamlessly; for annual plans, EMI options are shown for credit cards (3/6/9 month no-cost EMI on HDFC, ICICI, SBI cards over ₹2,000); all prices include 18% GST — the displayed price (₹299) is exclusive of tax, and the checkout shows the GST-inclusive total (₹352.82) before payment confirmation.

- The 7-day refund policy is unconditional — a student who upgrades and requests a refund within 7 calendar days receives a full refund to the original payment method within 5–7 business days; after 7 days, no refund is issued but the student can cancel to prevent future billing; cancellation takes effect at the end of the current billing period (students keep Premium until the paid period expires); the "cancel" action requires a single-click confirmation ("Are you sure? You'll keep Premium until [date]") — no multi-step retention funnel, no dark patterns.

- Coupon codes are managed by EduForge marketing (Group 1, Division L) and can be: (a) percentage discount (e.g., `FIRST50` = ₹50 off), (b) extended trial (e.g., `TRIAL30` = 30-day free trial instead of 7), (c) free months (e.g., `APPSC3FREE` = 3 months free for APPSC aspirants during notification season); coupons have validity periods, usage limits (global and per-user), and can be scoped to specific exam domains or geographies (e.g., AP/TS-only coupons for regional campaigns); a student can apply exactly one coupon per transaction.

- Institution-gifted Premium takes precedence over self-purchased — if Ravi has both institution-gifted (via TopRank) and a self-purchased monthly plan, the institution-gifted access is primary and the self-purchased plan is paused (billing suspended) until the institution gift expires; if the institution revokes access (e.g., student expelled or batch ends), the self-purchased plan auto-resumes from the next billing cycle; this prevents double-charging and ensures students don't lose their personal subscription when linking to an institution.

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division A*
