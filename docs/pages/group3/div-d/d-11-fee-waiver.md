# D-11 — Fee Waiver Register

> **URL:** `/school/fees/waivers/`
> **File:** `d-11-fee-waiver.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accountant (S3) — draft · Administrative Officer (S3) — draft · Academic Coordinator (S4) — approve (< ₹5,000) · Principal (S6) — full approve

---

## 1. Purpose

Records full or partial fee waivers granted to students on a case-by-case basis — distinct from ongoing concessions/scholarships (D-02). Waivers are exceptional, one-time decisions for circumstances such as:
- Family financial hardship (job loss, medical emergency)
- Parent passes away mid-year — school waives remaining year's fees
- Natural disaster (flood, COVID-type situation)
- School's goodwill gesture for long-standing families

Every waiver requires documented justification and Principal approval — because waivers reduce the school's revenue and must be auditable.

---

## 2. Page Layout

### 2.1 Header
```
Fee Waiver Register — 2026–27               [+ Request Waiver]  [Export Register]
Total Waivers: 8  ·  Full Waiver: 2  ·  Partial: 6  ·  Total Value: ₹2,84,000
```

### 2.2 Waiver Register
| Student | Class | Waiver Type | Amount Waived | Reason | Approved By | Date |
|---|---|---|---|---|---|---|
| Ravi Kumar | IX-A | Full (remaining year) | ₹21,000 | Father passed away — Feb 2026 | Principal | 28 Feb 2026 |
| Meena Devi | VII-B | Partial (50% tuition) | ₹15,000 | Mother hospitalised, single income | Principal | 15 Jan 2026 |
| Priya S. | VI-A | Small (late fee waiver) | ₹400 | Medical hospitalisation proof | Accountant | 10 Nov 2025 |

---

## 3. Request Waiver Form

[+ Request Waiver] → drawer:

| Field | Value |
|---|---|
| Student | [Search] |
| Waiver Type | Full (all remaining dues) · Partial (% or fixed ₹) · Late fee only |
| Amount to Waive | ₹21,000 (all remaining 2026–27 dues) |
| Reason Category | Financial Hardship · Parent Death · Natural Disaster · Medical Emergency · School Discretion |
| Detailed Justification | Father Mr. Ravi Kumar passed away on 22 Feb 2026. Mother is unemployed. Requesting full fee waiver for remaining Q3 and Q4. |
| Supporting Documents | Death certificate / medical record / income proof [Upload] |
| Requested By | Class Teacher / Parent (form submitted at office) |
| Approval Level | Academic Coordinator (< ₹5,000) / Principal (≥ ₹5,000) |

---

## 4. Approval Workflow

```
Waiver Request → Accountant reviews documents → Send to Principal
                                                      ↓
                                         Principal reviews and approves/rejects
                                                      ↓
                                     Approved → Fee ledger updated → Parent notified
                                     Rejected → Reason communicated to parent
```

---

## 5. Ledger Impact

When waiver is approved:
```
Ravi Kumar — Fee Ledger Update
Date: 28 Feb 2026 | Waiver ref: FW/2026/001

Q3 Tuition (Oct 2026)    ₹5,000 → Waived (FW/2026/001)
Q4 Tuition (Jan 2027)    ₹5,000 → Waived (FW/2026/001)
Remaining misc charges   ₹11,000 → Waived
Total waived: ₹21,000

Note on receipt: "Fee waived by order of Principal dated 28 Feb 2026 — Ref FW/2026/001"
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/waivers/?year={year}` | Waiver register |
| 2 | `POST` | `/api/v1/school/{id}/fees/waivers/` | Request waiver |
| 3 | `PATCH` | `/api/v1/school/{id}/fees/waivers/{waiver_id}/approve/` | Approve/reject waiver |
| 4 | `GET` | `/api/v1/school/{id}/fees/waivers/export/?year={year}` | Export for audit |

---

## 7. Business Rules

- Waivers are immutably logged — the Principal cannot "quietly" waive fees without it appearing in the register
- Waivers are permanent — they cannot be reversed once approved (if a student's situation changes, they must pay going forward; past waived amounts are not recoverable)
- A school inspection may audit waivers to ensure they are genuine — supporting documents must be archived

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
