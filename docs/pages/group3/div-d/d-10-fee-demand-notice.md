# D-10 — Fee Demand Notice

> **URL:** `/school/fees/demand-notices/`
> **File:** `d-10-fee-demand-notice.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Accountant (S3) — full · Administrative Officer (S3) — full · Principal (S6) — full

---

## 1. Purpose

Generates formal demand notices (written payment reminders) for fee defaulters. Demand notices are more formal than WhatsApp reminders — they are official letters on school letterhead that parents must acknowledge. For chronic defaulters, they serve as pre-legal notice documentation.

---

## 2. Page Layout

### 2.1 Header
```
Fee Demand Notices — 2026–27                 [+ Generate Notices]  [Track Delivery]  [Export]
Notices Generated: 48  ·  Delivered: 38  ·  Undelivered: 10  ·  Acknowledged: 22
```

---

## 3. Generate Notices

[+ Generate Notices] → select defaulter pool:

```
Generate Demand Notices

Defaulter Filter:
  ● All defaulters > 30 days (22 students)
  ○ Specific class: [Select]
  ○ Amount > ₹10,000 (8 students)

Notice Level:
  ● Level 1 (First reminder — polite)
  ○ Level 2 (Second notice — firm)
  ○ Level 3 (Final notice — warning of consequences)

Delivery Mode:
  ☑ WhatsApp (all with WhatsApp enabled)
  ☑ Print (for physical delivery via student)
  ☐ Registered Post (for chronic defaulters)

[Generate 22 Notices]
```

---

## 4. Notice Format (Level 1)

```
[SCHOOL LOGO]
[School Name] | [Address] | [Phone] | [Date]

NOTICE FOR FEE PAYMENT

Dear Mr./Ms. [Parent Name],

This is a gentle reminder that the following fee for your ward
[Student Name], Class [X], is overdue:

  Q3 Installment (Due: 1 October 2026)    ₹5,250
  Late Fee (55 days × ₹100/month)          ₹200
  ─────────────────────────────────────────────
  Total Outstanding                         ₹5,450

Kindly pay the above amount at the school fee counter at your
earliest convenience. For online payment, visit [parent portal URL].

For any queries, please contact the school office.

Regards,
Principal
[School Name]
```

---

## 5. Delivery Tracking

| Notice No. | Student | Amount | Sent Date | Mode | Status | Acknowledged |
|---|---|---|---|---|---|---|
| DN/2026/048 | Arjun Sharma | ₹5,450 | 25 Nov | WhatsApp | ✅ Delivered | ✅ 26 Nov |
| DN/2026/047 | Priya Kumar | ₹4,200 | 25 Nov | Print | ⬜ Not confirmed | — |
| DN/2026/022 | Vijay Nair | ₹6,500 | 10 Nov | Regd. Post | ✅ Delivered | ❌ Not ack. |

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/fees/demand-notices/?year={year}` | Notice register |
| 2 | `POST` | `/api/v1/school/{id}/fees/demand-notices/generate/` | Generate notices (bulk) |
| 3 | `GET` | `/api/v1/school/{id}/fees/demand-notices/{notice_id}/pdf/` | Notice PDF |
| 4 | `PATCH` | `/api/v1/school/{id}/fees/demand-notices/{notice_id}/acknowledge/` | Mark acknowledged |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division D*
