# E-02 — Student Revenue Management

> **URL:** `/tsp/admin/billing/student-revenue/`
> **File:** `e-02-student-revenue.md`
> **Priority:** P1
> **Roles:** TSP Admin · TSP Finance Manager · EduForge Finance Team

---

## 1. Student Pricing Configuration

```
STUDENT PRICING — TopRank Academy
Configure what you charge your students

  ── SUBSCRIPTION PLANS (STUDENT-FACING) ─────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  # │ Plan Name         │ Price    │ Duration │ Exams     │ Status      │
  │ ───┼───────────────────┼──────────┼──────────┼───────────┼─────────────│
  │  1 │ APPSC Basic       │ ₹199/mo  │ Monthly  │ APPSC     │ ✅ Active   │
  │  2 │ APPSC Premium     │ ₹499/mo  │ Monthly  │ APPSC     │ ✅ Active   │
  │  3 │ SSC Complete      │ ₹299/mo  │ Monthly  │ SSC CGL,  │ ✅ Active   │
  │    │                   │          │          │ SSC CHSL  │             │
  │  4 │ Banking Pro       │ ₹399/mo  │ Monthly  │ IBPS PO,  │ ✅ Active   │
  │    │                   │          │          │ SBI PO,   │             │
  │    │                   │          │          │ RBI Asst  │             │
  │  5 │ All-Access Pass   │ ₹699/mo  │ Monthly  │ All exams │ ✅ Active   │
  │  6 │ APPSC Annual      │ ₹1,999/yr│ Annual   │ APPSC     │ ✅ Active   │
  │  7 │ All-Access Annual │ ₹4,999/yr│ Annual   │ All exams │ ✅ Active   │
  │  8 │ Free Trial        │ ₹0       │ 7 days   │ APPSC     │ ✅ Active   │
  └──────────────────────────────────────────────────────────────────────────┘

  [+ Create New Plan]   [Bulk Edit Prices]   [Preview Student Checkout Page]

  ── PLAN EDITOR ─────────────────────────────────────────────────────────────

  Editing: SSC Complete

  Plan name:         [ SSC Complete                    ]
  Internal code:     [ ssc-complete-monthly            ] (auto-generated)
  Price:             [ ₹299  ] per [ Month ▼ ]
  Strike-through:    [ ₹499  ] (shown as original price on checkout)
  Discount label:    [ 40% OFF — Limited Time          ]
  Valid from:        [ 01 Apr 2026 ] to [ 30 Jun 2026 ] (or ☐ No end date)

  Included exams:    [ ✅ SSC CGL  ✅ SSC CHSL  ○ SSC MTS  ○ SSC GD ]
  Included features: [ ✅ Mock tests  ✅ Question bank  ✅ Previous papers ]
                     [ ○ Live classes  ○ Doubt clearing  ✅ Daily quizzes ]

  Payment options:   [ ✅ Razorpay  ✅ Paytm  ○ Bank transfer ]
  Auto-renewal:      (●) Yes, auto-renew  (○) One-time purchase
  Trial period:      [ 0 ] days (0 = no trial)
  Refund window:     [ 7 ] days from purchase

  Max students:      [ 0 ] (0 = unlimited for this plan)
  Coupon compatible: (●) Yes  (○) No

  [Save Plan]  [Preview Checkout]  [Deactivate Plan]
```

---

## 2. Payment Collection Dashboard

```
PAYMENT COLLECTION — TopRank Academy
Period: March 2026

  ── REVENUE SUMMARY ─────────────────────────────────────────────────────────

  ┌────────────────────────────────────────────────────────────────────────┐
  │                         MARCH 2026 OVERVIEW                          │
  │                                                                      │
  │  Gross collections:     ₹8,97,000    (3,000 students avg ₹299)      │
  │  Razorpay fees (2%):  - ₹  17,940                                   │
  │  GST on Razorpay fee: - ₹   3,229    (18% on gateway fee)           │
  │  Refunds processed:   - ₹  14,950    (50 refunds)                   │
  │  ──────────────────────────────────                                  │
  │  Net collections:       ₹8,60,881                                   │
  │                                                                      │
  │  Settlement to bank:    ₹8,60,881    (HDFC Bank ****4521)           │
  │  Settlement cycle:      T+2 business days (Razorpay standard)       │
  │  Next settlement:       02 Apr 2026 — ₹1,42,300 (pending)          │
  └────────────────────────────────────────────────────────────────────────┘

  ── DAILY COLLECTIONS (MARCH 2026) ─────────────────────────────────────────

  Day  │ New Subs │ Renewals │ Gross       │ Refunds  │ Net
  ─────┼──────────┼──────────┼─────────────┼──────────┼───────────
  01   │   45     │  120     │ ₹49,335     │ ₹  598   │ ₹48,737
  02   │   38     │   95     │ ₹39,767     │ ₹  299   │ ₹39,468
  03   │   52     │  108     │ ₹47,840     │ ₹    0   │ ₹47,840
  ...  │   ...    │  ...     │ ...         │ ...      │ ...
  30   │   41     │  102     │ ₹42,771     │ ₹  897   │ ₹41,874
  31   │   55     │  134     │ ₹56,511     │ ₹  299   │ ₹56,212
  ─────┼──────────┼──────────┼─────────────┼──────────┼───────────
  TOTAL│ 1,280    │ 3,420    │ ₹8,97,000   │ ₹14,950  │ ₹8,60,881

  ── PAYMENT METHOD BREAKDOWN ────────────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────────┐
  │  Razorpay UPI:          58%  ████████████████████████░░░░  ₹5,20,260│
  │  Razorpay Cards:        22%  █████████░░░░░░░░░░░░░░░░░░░  ₹1,97,340│
  │  Razorpay Net Banking:  12%  █████░░░░░░░░░░░░░░░░░░░░░░░  ₹1,07,640│
  │  Paytm Wallet:           5%  ██░░░░░░░░░░░░░░░░░░░░░░░░░░  ₹  44,850│
  │  Razorpay Wallets:       3%  █░░░░░░░░░░░░░░░░░░░░░░░░░░░  ₹  26,910│
  └───────────────────────────────────────────────────────────────────────┘

  ── FAILED PAYMENTS & RECOVERY ──────────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────────┐
  │  Failed transactions this month:     342                            │
  │  Auto-retry successful:              198 (57.9%)                    │
  │  Manual retry (student re-attempted): 89 (26.0%)                   │
  │  Permanently failed (churned):        55 (16.1%)                   │
  │                                                                     │
  │  RECOVERY ACTIONS:                                                  │
  │  ✅ Auto-retry: Razorpay retries failed auto-debits on Day 1, 3, 5 │
  │  ✅ SMS reminder: Sent to student on payment failure                │
  │  ✅ WhatsApp nudge: "Your TopRank subscription expired — renew now" │
  │  ✅ In-app banner: "Subscription expired" shown on student login    │
  │  ✅ Grace period: 3 days access after failure before content lock   │
  │                                                                     │
  │  [View Failed Payments]  [Send Bulk Reminder]  [Export CSV]         │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## 3. Razorpay Integration Settings

```
PAYMENT GATEWAY — TopRank Academy
Razorpay Integration Configuration

  ── RAZORPAY ACCOUNT ────────────────────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────────┐
  │  Account type:     Razorpay Standard (Route enabled)                │
  │  Merchant ID:      rzp_live_TopRank2024xxxx                         │
  │  API Key ID:       rzp_live_*************Xk3                        │
  │  API Key Secret:   ****************************                     │
  │  Webhook URL:      https://toprank.eduforge.in/api/v1/payments/     │
  │                    razorpay/webhook/                                 │
  │  Webhook Secret:   ****************************                     │
  │                                                                     │
  │  STATUS: ✅ Connected — last webhook received 31 Mar 2026 23:47 IST │
  │                                                                     │
  │  Settlement account: HDFC Bank                                      │
  │  Account no: ****4521 | IFSC: HDFC0001234                           │
  │  Settlement cycle: T+2 business days                                │
  │  Auto-settlement: ✅ Enabled                                        │
  │                                                                     │
  │  [Edit API Keys]  [Test Connection]  [View Webhook Logs]            │
  └───────────────────────────────────────────────────────────────────────┘

  ── RAZORPAY SUBSCRIPTIONS CONFIG ───────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────────┐
  │  Auto-debit mandates:                                               │
  │  • UPI Autopay: ✅ Enabled (RBI e-mandate compliant)                │
  │  • Card recurring: ✅ Enabled (RBI recurring payment rules)         │
  │  • Emandate (net banking): ✅ Enabled                               │
  │                                                                     │
  │  RBI compliance notes:                                              │
  │  • All recurring payments require explicit customer consent         │
  │  • Pre-debit notification sent 24h before charge (RBI mandate)      │
  │  • Max auto-debit ₹15,000/txn without additional factor auth       │
  │  • Transactions > ₹15,000 require additional authentication        │
  │                                                                     │
  │  Retry logic:                                                       │
  │  • 1st retry: 24 hours after failure                                │
  │  • 2nd retry: 72 hours after failure                                │
  │  • 3rd retry: 120 hours after failure                               │
  │  • After 3rd failure: subscription marked "halted"                  │
  │                                                                     │
  │  [Configure Retry Logic]  [View Active Mandates: 2,847]            │
  └───────────────────────────────────────────────────────────────────────┘

  ── PAYTM (SECONDARY GATEWAY) ──────────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────────┐
  │  Merchant ID:      TopRank_Edu_XXXXX                                │
  │  Status:           ✅ Active (fallback only)                        │
  │  Used when:        Razorpay UPI fails or student selects Paytm      │
  │  March volume:     ₹44,850 (5% of collections)                     │
  │  Settlement:       T+1 business day to Paytm Payments Bank         │
  │                                                                     │
  │  [Edit Paytm Config]  [Test Connection]                             │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/tsp/billing/student-plans/` | List all student-facing subscription plans |
| 2 | `POST` | `/api/v1/tsp/billing/student-plans/` | Create a new student subscription plan |
| 3 | `PATCH` | `/api/v1/tsp/billing/student-plans/{plan_id}/` | Update student plan pricing or features |
| 4 | `DELETE` | `/api/v1/tsp/billing/student-plans/{plan_id}/` | Deactivate a student plan (soft delete) |
| 5 | `GET` | `/api/v1/tsp/billing/collections/` | Get payment collection summary for period |
| 6 | `GET` | `/api/v1/tsp/billing/collections/daily/` | Daily collection breakdown with filters |
| 7 | `GET` | `/api/v1/tsp/billing/collections/failed/` | List failed payments with recovery status |
| 8 | `POST` | `/api/v1/tsp/billing/collections/failed/{txn_id}/retry/` | Manually retry a failed payment |
| 9 | `GET` | `/api/v1/tsp/billing/gateway/razorpay/status/` | Check Razorpay integration health |
| 10 | `POST` | `/api/v1/tsp/billing/gateway/razorpay/webhook/` | Razorpay webhook receiver (payment events) |
| 11 | `GET` | `/api/v1/tsp/billing/settlements/` | List payment settlements to TSP bank account |
| 12 | `POST` | `/api/v1/tsp/billing/student-plans/{plan_id}/coupons/` | Create discount coupon for a student plan |

---

## 5. Business Rules

- TSP student pricing is entirely controlled by the TSP Admin; EduForge does not dictate what a TSP charges its students, but the platform provides guardrails — minimum plan price is ₹49/month (to prevent race-to-bottom pricing that degrades the ecosystem), maximum plan price is ₹9,999/month (to prevent accidental overcharging), and free plans are allowed only as time-limited trials (max 30 days); the TSP keeps 100% of student revenue — EduForge's revenue comes from the platform subscription and content licence fees, not from a revenue share on student payments; this "pure SaaS" model (vs. marketplace commission model) is a key selling point for TSPs because they have full control over their revenue and customer relationships

- Razorpay is the primary payment gateway and all student payments flow through the TSP's own Razorpay account, not through EduForge's account; this is critical for regulatory compliance — since the TSP is the merchant of record, the TSP's GSTIN appears on student payment receipts, the TSP handles refund disputes, and Razorpay settlements go directly to the TSP's bank account; EduForge assists with Razorpay integration during onboarding (A-02) but does not have access to the TSP's Razorpay API secret key; the webhook URL points to the TSP's white-label domain (e.g., toprank.eduforge.in) and EduForge's platform processes webhook events to update subscription status; Paytm is offered as a secondary gateway because some students in tier-2 and tier-3 cities prefer Paytm wallet payments, and having a fallback gateway improves overall payment success rate by 3-5%

- Failed payment recovery is automated using a 3-tier retry system compliant with RBI's recurring payment framework (RBI/2020-21/17); the first retry occurs 24 hours after failure, the second at 72 hours, and the third at 120 hours; between retries, students receive SMS and WhatsApp notifications with a direct payment link; students retain access during a 3-day grace period after the first failure to avoid disrupting active learners (a student in the middle of a mock test should not be locked out); after the 3rd failed retry, the subscription status changes to "halted" and content access is restricted to free-tier features only; the TSP Admin can configure the grace period (1-7 days) and choose which notification channels to use; recovery rate benchmarks show that 58% of failed payments are recovered on auto-retry, 26% on manual retry after notification, and 16% result in permanent churn

- Refund processing follows a strict 7-day window from the date of purchase unless the TSP Admin configures a different window (configurable from 0 to 30 days); refunds are processed back to the original payment method through Razorpay's refund API — UPI refunds are instant, card refunds take 5-7 business days, and net banking refunds take 7-10 business days; partial refunds are supported (e.g., student paid ₹299 for monthly plan, used 10 days, refund ₹199 for unused 20 days); the TSP Admin can approve or reject refund requests manually, or enable auto-approval for refunds within the configured window; Razorpay charges no additional fee for refunds but the original transaction fee (2% + GST) is not returned, so a ₹299 refund costs the TSP approximately ₹7 in non-recoverable gateway fees; all refunds are logged for GST credit note generation

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division E*
