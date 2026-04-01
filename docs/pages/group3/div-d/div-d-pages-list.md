# Group 3 — Division D: Fee & Finance
## Pages Master List

> **Division:** D — Fee & Finance
> **Group:** 3 — School Portal
> **Total Pages:** 20
> **Roles Served:** Accountant (S3) · Fee Clerk (S2) · Administrative Officer (S3) · Academic Coordinator (S4) · Principal (S6)

---

## Roles in this Division

| Role | Access Level | Primary Responsibility |
|---|---|---|
| **Fee Clerk** | S2 | Counter fee collection, receipt printing, daily cash report |
| **Accountant** | S3 | Fee structure setup, defaulter tracking, scholarship management, financial reports, bank reconciliation |
| **Administrative Officer** | S3 | Fee waivers, RTE reimbursement coordination, vendor payments |
| **Academic Coordinator** | S4 | Fee policy input, scholarship approvals up to threshold |
| **Principal** | S6 | Fee structure approval, waiver above threshold, financial overview |

---

## Page List

### Cluster 1 — Fee Structure & Configuration

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| D-01 | `d-01-fee-structure.md` | Fee Structure Manager | P0 | Annual fee heads, amounts, installment schedule — approved by Principal |
| D-02 | `d-02-concessions-scholarships.md` | Concessions & Scholarships | P1 | Merit/need-based/RTE/sibling/staff-ward discounts |
| D-03 | `d-03-late-fee-config.md` | Late Fee Configuration | P1 | Grace period, fine per day/lump-sum, waiver rules |

### Cluster 2 — Fee Collection

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| D-04 | `d-04-fee-collection-counter.md` | Fee Collection Counter | P0 | Cash/online/DD; receipt generation; daily collection summary |
| D-05 | `d-05-online-payment-portal.md` | Online Payment Portal | P1 | Parent-initiated online payments via Razorpay/PhonePe; auto-reconcile |
| D-06 | `d-06-fee-receipt-manager.md` | Fee Receipt Manager | P1 | Receipt register, duplicate receipt, cancellation with approval |

### Cluster 3 — Student Fee Accounts

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| D-07 | `d-07-student-fee-ledger.md` | Student Fee Ledger | P0 | Per-student complete fee account (dues, payments, receipts, balance) |
| D-08 | `d-08-class-fee-summary.md` | Class-wise Fee Summary | P1 | Collection vs dues by class/section |
| D-09 | `d-09-fee-defaulters.md` | Fee Defaulters Register | P1 | Overdue students; auto-alerts; escalation workflow |
| D-10 | `d-10-fee-demand-notice.md` | Fee Demand Notice | P1 | Generate demand letters; send via WhatsApp/post |

### Cluster 4 — Special Fee Operations

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| D-11 | `d-11-fee-waiver.md` | Fee Waiver Register | P1 | Full/partial waiver; Principal approval; audit trail |
| D-12 | `d-12-rte-reimbursement.md` | RTE Reimbursement Tracker | P1 | Links to C-07; quarterly claim tracking; government receipt |
| D-13 | `d-13-scholarship-payments.md` | Scholarship Payment Tracker | P2 | PM scholarship, ST/SC pre-matric; government disbursement to student |
| D-14 | `d-14-security-deposit.md` | Security Deposit Register | P2 | Track deposits collected and refunds on student exit |

### Cluster 5 — Financial Reports

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| D-15 | `d-15-daily-collection-report.md` | Daily Collection Report | P1 | Day-end cash + online summary; matches A-20 |
| D-16 | `d-16-monthly-fee-summary.md` | Monthly Fee Summary | P1 | Month-wise collection, dues, scholarship adjustments |
| D-17 | `d-17-annual-fee-report.md` | Annual Fee Report | P1 | Year-end full financial summary; for FRA/Trust audit |
| D-18 | `d-18-bank-reconciliation.md` | Bank Reconciliation | P2 | Match EduForge fee records with bank statement |

### Cluster 6 — Vendor & Petty Cash

| Page ID | File | Title | Priority | Notes |
|---|---|---|---|---|
| D-19 | `d-19-vendor-payments.md` | Vendor Payment Register | P2 | Stationery, printing, maintenance payments; GST invoice capture |
| D-20 | `d-20-petty-cash.md` | Petty Cash Register | P2 | Day-to-day small expenses; balance maintained by accountant |

---

## Role → Page Access Matrix

| Page | Fee Clerk (S2) | Accountant (S3) | Admin Officer (S3) | Academic Coord (S4) | Principal (S6) |
|---|---|---|---|---|---|
| D-01 Fee Structure | Read | Draft | Read | Read | Full (approve) |
| D-02 Concessions | Read | Draft | Draft | Approve (<threshold) | Full |
| D-03 Late Fee Config | — | Draft | — | — | Approve |
| D-04 Collection Counter | Full (collect) | Full | Read | Read | Full |
| D-05 Online Portal | — | Full | — | — | Full |
| D-06 Receipt Manager | Read | Full | Read | — | Full |
| D-07 Student Ledger | Read | Full | Read | Read | Full |
| D-08 Class Summary | Read | Full | Read | Full | Full |
| D-09 Defaulters | Read | Full | Read | Read | Full |
| D-10 Demand Notice | — | Full | Full | — | Full |
| D-11 Waiver | — | Draft | Draft | Approve (<5k) | Full |
| D-12 RTE Reimb. | — | Full | Full | Read | Full |
| D-13 Scholarship | — | Full | Full | Read | Full |
| D-14 Security Deposit | Read | Full | Full | — | Full |
| D-15 Daily Report | Read (own shifts) | Full | Read | Read | Full |
| D-16 Monthly Summary | — | Full | Read | Read | Full |
| D-17 Annual Report | — | Full | Read | Read | Full |
| D-18 Bank Recon | — | Full | — | — | Full |
| D-19 Vendor Payments | — | Full | Full | — | Full |
| D-20 Petty Cash | — | Full | — | — | Full |

---

## Key Regulatory Context

- **GST:** Schools are exempt from GST (education services under SAC 9992/9993). However, if a school has a coaching/extra classes component, that is taxable at 18%. Fee receipts must state "Education service — GST Exempt" or "Coaching — 18% GST applicable" correctly.
- **State Fee Regulatory Authority (FRA):** States like Maharashtra, Karnataka, Tamil Nadu have FRAs that cap annual fee increases (typically 8–15% per year). EduForge tracks year-on-year fee increases and flags if the increase exceeds the FRA ceiling.
- **RTE:** No fee to be charged from RTE students (enforced in D-04 counter — blocks collection from RTE-flagged students).
- **CBSE:** Schools must not withhold TC for fee dues (CBSE Affiliation Bye-Laws); D-11 waiver + D-10 demand notice workflows align with this.
- **7-year audit trail:** All fee transactions retained 7 years (per financial audit norms); no deletion.

---

## Data Dependencies

| Depends On | For |
|---|---|
| C-05 Enrollment | Student list for fee ledger initialisation |
| C-07 RTE Admissions | RTE student flag (no fee charged) |
| C-10 Class Promotion | Updating fee structure when student moves to new class |
| C-20 Sibling Linkage | Sibling discount computation |
| A-08 Class & Section | Class-wise fee reports |
| A-10 Academic Calendar | Installment due dates |
| B-33 Board Exam Registration | Board exam fee component |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
