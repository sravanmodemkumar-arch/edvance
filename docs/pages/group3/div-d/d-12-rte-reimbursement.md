# D-12 — RTE Reimbursement Tracker

> **URL:** `/school/fees/rte-reimbursement/`
> **File:** `d-12-rte-reimbursement.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accountant (S3) — full · Administrative Officer (S3) — full · Principal (S6) — full

---

## 1. Purpose

Tracks the quarterly RTE reimbursement claims from the state government. Schools admitting students under RTE Section 12(1)(c) are entitled to reimbursement at the prescribed rate per student per month. This reimbursement often arrives late or partially — the Accountant must track what's been claimed vs received.

This page works in conjunction with C-07 (RTE Admission Manager) which maintains the RTE student roster. D-12 handles the financial tracking of claims.

---

## 2. Page Layout

### 2.1 Header
```
RTE Reimbursement Tracker — 2026–27          [Generate Claim]  [Export]
State Rate: ₹1,200/student/month (Telangana 2026–27)
RTE Students: 71 (across all years — Nursery through Class V)
```

### 2.2 Quarterly Claim Status
| Quarter | Students | Rate | Claim Amount | Filed On | Received | Status |
|---|---|---|---|---|---|---|
| Q1 Apr–Jun 2026 | 71 | ₹1,200×3 | ₹2,55,600 | 31 Jul 2026 | ₹2,55,600 | ✅ Full |
| Q2 Jul–Sep 2026 | 71 | ₹1,200×3 | ₹2,55,600 | 31 Oct 2026 | ₹2,16,000 | ⚠️ Partial (₹39,600 pending) |
| Q3 Oct–Dec 2026 | 71 | ₹1,200×3 | ₹2,55,600 | 31 Jan 2027 | — | ⏳ Filed, awaiting |
| Q4 Jan–Mar 2027 | 71 | ₹1,200×3 | ₹2,55,600 | Due: 30 Apr 2027 | — | ⬜ Not yet filed |

---

## 3. Generate Claim

[Generate Claim] → Q4 2026–27:

```
RTE Reimbursement Claim — Q4 (Jan–Mar 2027)

Period: 1 Jan 2027 – 31 Mar 2027  (3 months)
RTE Students in Entry Class:

Class    Students  Attendance %  Eligible Months  Amount
Nursery    10         92%             3           ₹36,000
LKG         9         94%             3           ₹32,400
UKG        10         88%             3           ₹36,000
Class I     9         91%             3           ₹32,400
Class II   10         89%             3           ₹36,000
Class III   9         86%             3           ₹32,400
Class IV    8         90%             3           ₹28,800
Class V     6         88%             3           ₹21,600
───────────────────────────────────────────────────────
Total:     71                                    ₹2,55,600

Note: Some states apply attendance-linked reimbursement (students with < 50% attendance may be excluded — state-configurable).

[Generate Claim PDF + Excel for DEO submission]
```

---

## 4. Pending Recovery Alert

```
⚠️ Q2 2026–27: ₹39,600 still pending from state government
  Filed: 31 Oct 2026  ·  Expected receipt: Dec 2026
  Action: Follow up with District Education Office (DEO)
  Contact: DEO Hyderabad — Mr. Srinivas — 9876501234
  [Log Follow-up]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/rte-reimbursement/?year={year}` | Claim status all quarters |
| 2 | `POST` | `/api/v1/school/{id}/fees/rte-reimbursement/claim/` | Generate quarterly claim |
| 3 | `PATCH` | `/api/v1/school/{id}/fees/rte-reimbursement/{quarter_id}/received/` | Mark payment received |
| 4 | `GET` | `/api/v1/school/{id}/fees/rte-reimbursement/export/?year={year}` | Export all claims |

---

## 6. Business Rules

- RTE reimbursement rate is government-declared each year; the school configures the current rate in school settings; EduForge does not store state-wise rate schedules (it varies by state)
- If a RTE student's Aadhaar is not seeded (C-09), the state government may reject the reimbursement claim for that student; D-12 shows a flag for unseeded Aadhaar students
- Reimbursement received is shown in A-21 Monthly Financial Summary as income

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
