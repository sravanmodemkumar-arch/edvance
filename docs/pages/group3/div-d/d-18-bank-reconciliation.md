# D-18 — Bank Reconciliation

> **URL:** `/school/fees/bank-reconciliation/`
> **File:** `d-18-bank-reconciliation.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Accountant (S3) — full · Principal (S6) — full

---

## 1. Purpose

Matches EduForge fee records (what the system says was collected) with the school's bank statement (what actually appeared in the bank). Discrepancies arise from:
- Cheques not yet cleared
- Online payments with pending gateway settlement
- Cash deposited but not yet credited by bank
- Rare errors (wrong amount deposited, etc.)

---

## 2. Page Layout

### 2.1 Header
```
Bank Reconciliation — March 2026             [Upload Bank Statement]  [Auto-match]  [Export]
EduForge Cash/NEFT total:    ₹28,42,000
Bank Statement total:        ₹27,98,000
Difference:                   ₹44,000  (2 cheques pending clearance)
Status: ⚠️ 2 items unmatched
```

### 2.2 Reconciliation Table
| EduForge Ref | Amount | Mode | Date | Bank Match | Status |
|---|---|---|---|---|---|
| R/2026/7834 | ₹5,350 | UPI | 26 Mar | ✅ RPY-98421 | Matched |
| R/2026/0022 | ₹22,000 | Cheque | 5 Mar | ⏳ Not cleared | Pending |
| R/2026/0023 | ₹22,000 | Cheque | 5 Mar | ⏳ Not cleared | Pending |

---

## 3. Bank Statement Upload

[Upload Bank Statement] → CSV from bank:
- SBI, HDFC, ICICI, Axis — standard CSV format
- System auto-matches by amount + date + mode
- Unmatched items flagged for Accountant review

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/bank-reconciliation/?month={month}&year={year}` | Reconciliation status |
| 2 | `POST` | `/api/v1/school/{id}/fees/bank-reconciliation/upload/` | Upload bank statement |
| 3 | `POST` | `/api/v1/school/{id}/fees/bank-reconciliation/auto-match/` | Run auto-matching |
| 4 | `PATCH` | `/api/v1/school/{id}/fees/bank-reconciliation/{item_id}/match/` | Manual match |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
