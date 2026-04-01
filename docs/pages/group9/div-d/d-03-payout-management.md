# D-03 — Payout Management

> **URL:** `/content-partner/revenue/payouts/`
> **File:** `d-03-payout-management.md`
> **Priority:** P1
> **Roles:** Content Partner (own payouts) · EduForge Finance Team (process payouts)

---

## 1. Bank Details & Payout Configuration

```
PAYOUT SETTINGS — Dr. Venkat Rao (Partner ID: CP-0472)

  ┌──────────────────────────────────────────────────────────────────────┐
  │  BANK ACCOUNT DETAILS                          [Edit]  [Verify]     │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                     │
  │  Account Holder  :  Dr. Venkat Rao                                  │
  │  Bank Name       :  State Bank of India                             │
  │  Branch          :  Main Branch, Visakhapatnam                      │
  │  Account Number  :  3456XXXXXXX789  (masked — last 3 visible)      │
  │  IFSC Code       :  SBIN0001234                                     │
  │  Account Type    :  Savings                                         │
  │  PAN             :  BNXPR1234A  (verified)                          │
  │  Verification    :  [VERIFIED] Penny-drop on 14-Jan-2025            │
  │                                                                     │
  │  Payout Mode     :  NEFT  [Change to IMPS]                         │
  │  Minimum Payout  :  Rs. 500 (system default — cannot be lowered)   │
  │                                                                     │
  │  ⚠ Changing bank details requires re-verification (1-2 business    │
  │    days) and payouts are held until verification completes.         │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Payout History

```
PAYOUT HISTORY — Dr. Venkat Rao
FY 2025-26 (April 2025 — March 2026)

  ┌─────┬───────────┬─────────┬─────────┬────────┬──────────┬──────────────────┐
  │  #  │ Month     │ Net Rev │ TDS 10% │ Payout │ Status   │ NEFT Reference   │
  ├─────┼───────────┼─────────┼─────────┼────────┼──────────┼──────────────────┤
  │  1  │ Apr 2025  │  32,400 │   3,240 │ 29,160 │ PAID     │ NEFT-20250508    │
  │  2  │ May 2025  │  33,200 │   3,320 │ 29,880 │ PAID     │ NEFT-20250609    │
  │  3  │ Jun 2025  │  31,800 │   3,180 │ 28,620 │ PAID     │ NEFT-20250708    │
  │  4  │ Jul 2025  │  34,600 │   3,460 │ 31,140 │ PAID     │ NEFT-20250807    │
  │  5  │ Aug 2025  │  35,500 │   3,550 │ 31,950 │ PAID     │ NEFT-20250909    │
  │  6  │ Sep 2025  │  36,200 │   3,620 │ 32,580 │ PAID     │ NEFT-20251008    │
  │  7  │ Oct 2025  │  34,120 │   3,412 │ 30,708 │ PAID     │ NEFT-20251107    │
  │  8  │ Nov 2025  │  36,800 │   3,680 │ 33,120 │ PAID     │ NEFT-20251209    │
  │  9  │ Dec 2025  │  42,550 │   4,255 │ 38,295 │ PAID     │ NEFT-20260108    │
  │ 10  │ Jan 2026  │  45,200 │   4,520 │ 40,680 │ PAID     │ NEFT-20260209    │
  │ 11  │ Feb 2026  │  49,100 │   4,910 │ 44,190 │ PAID     │ NEFT-20260309    │
  │ 12  │ Mar 2026  │  38,000 │   3,800 │ 34,200 │ PENDING  │ — (due 08-Apr)   │
  ├─────┴───────────┼─────────┼─────────┼────────┼──────────┴──────────────────┤
  │  FY TOTAL       │4,49,470 │  44,947 │4,04,523│ 11 paid + 1 pending        │
  └─────────────────┴─────────┴─────────┴────────┴────────────────────────────┘

  [Download CSV]  [Download PDF Statement]  [Raise Dispute]
```

---

## 3. Payout Schedule & Processing

```
PAYOUT LIFECYCLE — Monthly Cycle

  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │  1st of Month          Usage calculation period closes              │
  │       │                (e.g., 1-Mar to 31-Mar usage finalised       │
  │       ▼                 on 01-Apr at 00:00 IST)                     │
  │                                                                     │
  │  1st – 3rd             Invoice auto-generated                       │
  │       │                Gross → Commission → Net → TDS → Payout Amt  │
  │       ▼                Partner notified via email + dashboard        │
  │                                                                     │
  │  3rd – 5th             Review window                                │
  │       │                Partner can raise dispute if usage seems low  │
  │       ▼                Finance team reviews flagged payouts          │
  │                                                                     │
  │  5th – 7th             Finance approval                             │
  │       │                Batch approved for NEFT processing            │
  │       ▼                                                             │
  │  By 10th               NEFT/IMPS payout executed                    │
  │       │                Rs. 34,200 credited to SBI A/c 3456XXX789    │
  │       ▼                UTR number recorded, partner notified        │
  │                                                                     │
  │  CURRENT STATUS (Mar 2026 payout):                                  │
  │  [=============================>          ] 75% — Finance Approval  │
  │  Expected credit: 08-Apr-2026                                       │
  └─────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/content-partner/revenue/payouts/bank-details/` | Retrieve masked bank account details for authenticated partner |
| 2 | `PUT` | `/api/v1/content-partner/revenue/payouts/bank-details/` | Update bank account (triggers re-verification) |
| 3 | `POST` | `/api/v1/content-partner/revenue/payouts/bank-details/verify/` | Initiate penny-drop verification for updated bank details |
| 4 | `GET` | `/api/v1/content-partner/revenue/payouts/history/?fy=2025-26` | Payout history for a financial year |
| 5 | `GET` | `/api/v1/content-partner/revenue/payouts/{payout_id}/` | Detail of a specific payout including UTR and status |
| 6 | `POST` | `/api/v1/content-partner/revenue/payouts/{payout_id}/dispute/` | Raise a dispute on a specific month's payout |
| 7 | `GET` | `/api/v1/content-partner/revenue/payouts/schedule/` | Current month's payout lifecycle status and expected date |

---

## 5. Business Rules

- Bank account verification is mandatory before any payout can be processed; EduForge uses a penny-drop verification method where a Rs. 1 test transaction is sent to the provided account, and the partner must confirm receipt (or the system auto-confirms via bank API callback within 24 hours); if a partner changes their bank details mid-cycle (e.g., switches from SBI Visakhapatnam to HDFC Hyderabad), all pending payouts are held until the new account is verified, and the partner is clearly informed that the hold is due to re-verification, not a payment delay; the system stores a complete audit trail of all bank detail changes with timestamps, IP addresses, and the old/new values (masked) for compliance and fraud prevention.

- The payout minimum threshold of Rs. 500 exists to avoid uneconomical NEFT transactions where the processing cost approaches the payout amount; if a partner's net earnings after commission and TDS fall below Rs. 500 in a given month (which can happen for new partners with few questions in the pool), the amount is carried forward to the next month and accumulated until the Rs. 500 threshold is met; the carried-forward amount is clearly shown on the dashboard with a label "Balance carried forward: Rs. XXX — will be included in next eligible payout," and the partner receives an email explaining the carry-forward rather than being left wondering why no payout was received.

- The dispute resolution mechanism allows a partner to challenge the usage count or revenue calculation for any month within 60 days of the invoice date; Dr. Venkat Rao, for example, might notice that his February 2026 usage count seems lower than expected given that a new TSP (Sri Chaitanya) started using his content in March — if he suspects the start date was actually mid-February, he can raise a dispute with supporting evidence; the EduForge finance team then pulls raw usage logs, cross-references with TSP activation dates, and either upholds the original figure with an explanation or issues a correction with a supplementary payout in the next cycle; disputes must be resolved within 15 business days, and the partner is kept informed at every stage via email and dashboard notifications.

- NEFT payouts are processed as a batch on business days only; if the 10th of the month falls on a Sunday or bank holiday, the payout is processed on the next business day; for partners who opt for IMPS instead of NEFT, the payout can be processed on any day including weekends and holidays, but IMPS has a per-transaction limit of Rs. 5,00,000 which is sufficient for the vast majority of content partners; the UTR (Unique Transaction Reference) number is recorded against each payout for reconciliation, and the partner can use this UTR to verify the credit with their bank independently; EduForge retains payout records for 8 financial years as required under the Income Tax Act for TDS-related documentation.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division D*
