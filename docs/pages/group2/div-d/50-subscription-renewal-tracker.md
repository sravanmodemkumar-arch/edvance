# 50 — Subscription Renewal Tracker

- **URL:** `/group/finance/eduforge-billing/renewals/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** EduForge Billing Coordinator G3 (primary) · CFO G1

---

## 1. Purpose

The Subscription Renewal Tracker monitors upcoming, in-progress, and completed EduForge subscription renewals for all branches in the group. It gives the Billing Coordinator a proactive view of which renewals need action — quote generation, payment processing, invoice reconciliation — to prevent service interruptions.

Renewals are tracked from 30 days before the renewal date through to payment confirmation. Overdue renewals trigger escalation alerts. The tracker also records year-on-year cost changes and plan changes made during renewal.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group EduForge Billing Coordinator | G3 | Full read + process renewals |
| Group CFO | G1 | Read — cost summary |
| Group Finance Manager | G1 | Read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → EduForge Billing → Subscription Renewal Tracker
```

### 3.2 Page Header
- **Title:** `Subscription Renewal Tracker`
- **Subtitle:** `[N] Renewals Due This Month · Total Value: ₹[X]`
- **Right-side controls:** `[Month ▾]` `[Status ▾]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| Renewal overdue | "[N] subscription(s) have expired — services may be restricted." | Red |
| Renewal due ≤ 3 days | "[N] renewal(s) due in ≤ 3 days. Act now." | Red |
| Renewal due ≤ 7 days | "[N] renewal(s) due within 7 days." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Renewals This Month | Count | Neutral |
| Completed | Count | Green |
| Pending | Count | Amber if > 0 |
| Overdue | Count | Red if > 0 |
| Total Renewal Value | ₹ | Neutral |
| YoY Cost Change | ₹ / % | Red if increase > 10% |

---

## 5. Main Table — Renewal Pipeline

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text | ✅ | ✅ |
| Current Plan | Badge | ✅ | ✅ |
| Renewal Date | Date | ✅ | — |
| Days to Renewal | Number (colour-coded) | ✅ | — |
| Renewal Type | Badge: Same Plan · Upgrade · Downgrade | ✅ | ✅ |
| Renewal Amount | ₹ | ✅ | — |
| Previous Amount | ₹ | ✅ | — |
| Change | ₹ / % | ✅ | — |
| Status | Badge: Upcoming · Quote Sent · Payment Received · Renewed · Overdue | ✅ | ✅ |
| Renewal Period | Text (12 months / 1 month) | ✅ | ✅ |
| Invoice No | Text | ✅ | — |
| Actions | Process · View Invoice · Send Reminder | — | — |

### 5.1 Filters
- Branch · Status · Renewal Month · Plan type

### 5.2 Search
- Branch name · Invoice number

### 5.3 Pagination
- 20 rows/page · Sort: Renewal Date asc

---

## 6. Drawers

### 6.1 Drawer: `renewal-process` — Process Renewal
- **Trigger:** Process action
- **Width:** 680px

**Renewal Summary:**
- Branch · Current Plan · Renewal Date
- New Plan (if changed) · Renewal Period
- Amount: ₹[X] (including any seat adjustments or plan changes)

**Payment Recording:**

| Field | Type | Required |
|---|---|---|
| Payment Date | Date | ✅ |
| Payment Mode | Select: NEFT/RTGS · Credit Card · UPI · Cheque | ✅ |
| Reference / UTR | Text | ✅ |
| Amount Paid | Number | ✅ |
| Invoice No | Auto-generated | — |
| Payment Proof | File upload | ❌ |

- [Cancel] [Confirm Renewal]

### 6.2 Drawer: `renewal-detail` — Renewal History
- **Width:** 720px

**History (last 3 renewals):**
| Renewal Date | Plan | Amount | Payment Date | Mode | Invoice |
|---|---|---|---|---|---|
| [Date] | [Plan] | ₹ | [Date] | NEFT | [Download] |

**Plan Change Log:**
- Any upgrades/downgrades made at renewal time

### 6.3 Drawer: `send-reminder` — Send Renewal Reminder
| Field | Type | Required |
|---|---|---|
| Recipient | Text (billing contact email) | ✅ |
| Message | Textarea (pre-filled template) | ✅ |
| Attach Invoice | Toggle | — |

- [Send Reminder]

---

## 7. Charts

### 7.1 Renewal Pipeline by Month (Bar — Next 6 Months)
- **Series:** Upcoming · Completed · Overdue

### 7.2 Cost Trend YoY (Line)
- **Y-axis:** Total annual renewal value

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Renewal confirmed | "[Branch] subscription renewed for [N] months." | Success | 4s |
| Reminder sent | "Renewal reminder sent to [Branch] billing contact." | Info | 3s |
| Overdue alert | "[Branch] subscription is overdue. Services may be restricted." | Warning | 5s |
| Export | "Renewal tracker exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| All renewed | "All renewals complete" | "All subscriptions are current for this month." |
| No renewals | "No renewals this month" | "No subscription renewals due in the selected period." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table |
| Drawer | Spinner |

---

## 11. Role-Based UI Visibility

| Element | Billing Coordinator G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [Process Renewal] | ✅ | ❌ | ❌ |
| [Send Reminder] | ✅ | ❌ | ❌ |
| [View Invoice] | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/billing/renewals/` | JWT (G1+) | Renewal list |
| GET | `/api/v1/group/{id}/finance/billing/renewals/{rid}/` | JWT (G1+) | Renewal detail |
| POST | `/api/v1/group/{id}/finance/billing/renewals/{rid}/confirm/` | JWT (G3) | Confirm renewal |
| POST | `/api/v1/group/{id}/finance/billing/renewals/{rid}/remind/` | JWT (G3) | Send reminder |
| GET | `/api/v1/group/{id}/finance/billing/renewals/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Month filter | `change` | GET `.../renewals/?month=&status=` | `#renewal-table` | `innerHTML` |
| Process drawer | `click` | GET `.../renewals/{id}/process-form/` | `#drawer-body` | `innerHTML` |
| Detail drawer | `click` | GET `.../renewals/{id}/` | `#drawer-body` | `innerHTML` |
| Confirm renewal | `submit` | POST `.../renewals/{id}/confirm/` | `#renewal-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
