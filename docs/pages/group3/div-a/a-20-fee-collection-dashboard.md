# A-20 — Fee Collection Dashboard

> **URL:** `/school/admin/finance/fee-dashboard/`
> **File:** `a-20-fee-collection-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — view · Promoter (S7) — full · VP Admin (S5) — view · Accountant (S4 Finance) — full

---

## 1. Purpose

Real-time overview of the school's fee collection status — this month, this term, and this academic year. The leadership uses this page to see if the school's revenue is on track. The Accountant uses it to identify defaulters and manage collection. This is a read-only summary page (for leadership); the detailed fee collection operations (receipts, payment modes, defaulter follow-up) are handled in div-e (Fee & Finance division).

---

## 2. Page Layout

### 2.1 Header
```
Fee Collection Dashboard — 2025–26          [View Full Fee Module →]  [Export Summary]
Academic Year: 2025–26 ▼     Month: March 2026 ▼
```

### 2.2 KPI Strip (6 cards)

| Card | Metric | Colour Rule |
|---|---|---|
| Annual Fee Demand | ₹1.24 Cr (total fees payable this year) | Blue |
| Collected (Year-to-date) | ₹1.02 Cr (82.3%) | Green ≥85% · Amber 70–84% · Red <70% |
| Outstanding | ₹22.4L remaining | Green <15% of demand · Red >20% |
| This Month Collected | ₹8.2L | — |
| Students with Dues > 60 days | 42 | Green = 0 · Amber 1–20 · Red >20 |
| RTE Reimbursement Pending | ₹1.62L | Blue |

---

## 3. Main Sections

### 3.1 Collection Trend (line/bar chart)

| Month | Demand | Collected | % | Trend |
|---|---|---|---|---|
| Apr 2025 | ₹18.5L | ₹17.9L | 96.8% | ↑ |
| May 2025 | ₹8.2L | ₹8.0L | 97.6% | ↑ |
| Jun 2025 | ₹8.2L | ₹7.8L | 95.1% | ↓ |
| … | … | … | … | … |
| Mar 2026 | ₹8.5L | ₹8.2L | 96.5% (in progress) | — |

Bar chart with target line. Hover: month details.

---

### 3.2 Collection by Fee Type

| Fee Type | Annual Demand | Collected | Outstanding | Collection % |
|---|---|---|---|---|
| Tuition Fee | ₹82.4L | ₹68.1L | ₹14.3L | 82.6% |
| Admission Fee (once) | ₹6.24L | ₹6.24L | — | 100% |
| Exam Fee | ₹4.18L | ₹3.9L | ₹0.28L | 93.3% |
| Transport Fee | ₹9.6L | ₹8.4L | ₹1.2L | 87.5% |
| Hostel Fee (Boys) | ₹8.28L | ₹6.8L | ₹1.48L | 82.1% |
| Hostel Fee (Girls) | ₹6.6L | ₹5.4L | ₹1.2L | 81.8% |
| Lab/Activity Fee | ₹3.36L | ₹2.9L | ₹0.46L | 86.3% |
| **Total** | **₹1.24 Cr** | **₹1.02 Cr** | **₹22.4L** | **82.3%** |

---

### 3.3 Collection by Class

| Class | Students | Annual Fee | Collected | Outstanding | Collection % |
|---|---|---|---|---|---|
| LKG | 78 | ₹7.02L | ₹6.8L | ₹0.22L | 96.9% |
| Class I | 142 | ₹15.62L | ₹12.8L | ₹2.82L | 81.9% |
| … | … | … | … | … | … |
| Class XII | 73 | ₹12.41L | ₹9.8L | ₹2.61L | 79.0% |

Click any class → class-wise fee detail drawer (students with outstanding amounts).

---

### 3.4 Top Defaulters

| # | Student | Class | Outstanding | Days Overdue | Last Payment | Action |
|---|---|---|---|---|---|---|
| 1 | Aryan Sharma | XII MPC | ₹42,000 | 87 days | 10 Dec 2025 | [Send Notice] [View] |
| 2 | Deepika Roy | XI BiPC | ₹36,500 | 74 days | 25 Dec 2025 | [Send Notice] [View] |
| … | … | … | … | … | … | … |

[Send Notice] → sends fee reminder via WhatsApp to parent.
[View] → opens student fee detail in div-e.

---

### 3.5 Payment Mode Analysis (current month)

| Mode | Count | Amount | % of Total |
|---|---|---|---|
| Online (Razorpay/PhonePe/PayU) | 148 | ₹6.2L | 75.6% |
| Cash | 42 | ₹1.1L | 13.4% |
| Cheque/DD | 12 | ₹0.62L | 7.6% |
| NEFT/Bank Transfer | 8 | ₹0.28L | 3.4% |

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/finance/fee-dashboard/` | Full dashboard data |
| 2 | `GET` | `/api/v1/school/{id}/finance/fee-collection-trend/` | Monthly collection chart |
| 3 | `GET` | `/api/v1/school/{id}/finance/fee-by-type/` | Fee type breakdown |
| 4 | `GET` | `/api/v1/school/{id}/finance/fee-by-class/` | Class-wise collection |
| 5 | `GET` | `/api/v1/school/{id}/finance/top-defaulters/?days=30` | Defaulter list |
| 6 | `GET` | `/api/v1/school/{id}/finance/payment-modes/` | Payment mode analysis |
| 7 | `POST` | `/api/v1/school/{id}/finance/send-fee-reminder/{student_id}/` | Send fee reminder |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
