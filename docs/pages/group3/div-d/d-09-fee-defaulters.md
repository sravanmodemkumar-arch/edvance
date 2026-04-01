# D-09 — Fee Defaulters Register

> **URL:** `/school/fees/defaulters/`
> **File:** `d-09-fee-defaulters.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accountant (S3) — full · Administrative Officer (S3) — read · Principal (S6) — full

---

## 1. Purpose

Lists all students with overdue fee payments — the starting point for the recovery workflow. After the grace period expires, students move from "outstanding" to "defaulter" status. The Accountant uses this register to:
- Send WhatsApp reminders (auto via D-10)
- Call parents for large defaulters
- Escalate to Principal for chronic defaulters
- Make data-driven decisions (are defaults concentrated in a class? Is there an economic pattern in a particular area?)

---

## 2. Page Layout

### 2.1 Header
```
Fee Defaulters Register — Q3 (Oct 2026)     [Send All Reminders]  [Generate Demand Notices]  [Export]
Total Defaulters: 68 students  ·  Total Outstanding: ₹32,66,000
Overdue > 30 days: 22 students  ·  Overdue > 60 days: 8 students  ·  > 90 days: 3 students
```

### 2.2 Defaulter List
| Student | Class | Due Date | Overdue Days | Outstanding | Late Fee | Total Due | Last Reminder | Action |
|---|---|---|---|---|---|---|---|---|
| Arjun Sharma | XI-A | 1 Oct | 55 days | ₹5,250 | ₹200 | ₹5,450 | 15 Nov | [Remind] [Call] |
| Priya Kumar | IX-B | 1 Oct | 55 days | ₹4,000 | ₹200 | ₹4,200 | 18 Nov | [Remind] |
| Rohit Mehta | XI-B | 1 Oct | 55 days | ₹5,250 | ₹200 | ₹5,450 | — | [Remind] |
| Vijay Nair | XII-A | 1 Oct | 85 days | ₹6,000 | ₹500 | ₹6,500 | 8 Nov | [Escalate] |

---

## 3. Defaulter Filters

```
Overdue:  [All ▼ / > 30 days / > 60 days / > 90 days]
Class:    [All ▼]
Amount:   [All ▼ / > ₹5,000 / > ₹10,000]
Last Reminder: [Never sent / > 7 days ago / > 14 days ago]
```

---

## 4. Escalation Levels

| Days Overdue | Status | Action |
|---|---|---|
| 1–15 | Grace period | No action |
| 16–30 | Defaulter (Level 1) | Auto WhatsApp reminder |
| 31–60 | Defaulter (Level 2) | Written demand notice (D-10) |
| 61–90 | Defaulter (Level 3) | Accountant personal call + demand notice |
| 90+ | Chronic Defaulter | Principal escalation; fee waiver review (D-11) or legal notice |

---

## 5. Chronic Defaulter Actions

For > 90-day defaulters, Principal sees them on A-20 dashboard and can:
- [Grant Fee Waiver] (links to D-11) — if family genuinely can't pay
- [Demand Final Notice] (generates strongly worded final notice)
- [Hold TC] — Principal override allowing TC to be withheld (only legally justifiable if not RTE student)
- [Refer to Trust / Management] — for management-level decision

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/defaulters/?year={year}&installment={q}&days_overdue={n}` | Defaulter list with filters |
| 2 | `POST` | `/api/v1/school/{id}/fees/defaulters/remind-bulk/` | Send WhatsApp reminders to all |
| 3 | `GET` | `/api/v1/school/{id}/fees/defaulters/export/?year={year}` | Export defaulter register |

---

## 7. Business Rules

- A student is never listed as a defaulter for RTE-flagged fees (they have ₹0 dues)
- Students with an approved fee waiver (D-11) are excluded from defaulter list for the waived amount
- Defaulter status does not affect: admission, attendance marking, exam participation, or report cards — CBSE prohibition on denying academic benefits for fee default
- TC (C-13) can be withheld only with Principal explicit override and logged reason — and only for non-RTE students with genuine outstanding dues

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
