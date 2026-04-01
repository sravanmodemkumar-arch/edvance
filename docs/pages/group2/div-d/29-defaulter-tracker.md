# 29 — Defaulter Tracker

- **URL:** `/group/finance/collection/defaulters/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Fee Collection Head G3 (primary) · Finance Manager G1 · CFO G1

---

## 1. Purpose

The Defaulter Tracker maintains a consolidated, cross-branch list of students who have not paid their fees beyond the due date. It provides aging analysis (0–30, 31–60, >60 days overdue), identifies repeat defaulters (students who defaulted in multiple terms), and enables the Fee Collection Head to take targeted action — sending reminders, scheduling calls, or escalating to branch principals.

The defaulter list is also used by the Group Scholarship Manager (Division C) to flag students applying for scholarships who have outstanding dues — scholarships are not disbursed to students with pending fees.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Collection Head | G3 | Full read + action (reminders, escalation) |
| Group Finance Manager | G1 | Read |
| Group CFO | G1 | Read — summary |
| Group Accounts Manager | G1 | Read — for ledger reconciliation |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Collection → Defaulter Tracker
```

### 3.2 Page Header
- **Title:** `Defaulter Tracker`
- **Subtitle:** `[N] Defaulters · Total Outstanding: ₹[X] · AY [Year] · Term [N]`
- **Right-side controls:** `[AY ▾]` `[Term ▾]` `[Branch ▾]` `[Export ↓]`

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Defaulters | Count | Red if > 0 |
| Total Outstanding | ₹ | Red |
| 0–30 Days Overdue | Count + ₹ | Amber |
| 31–60 Days Overdue | Count + ₹ | Orange |
| >60 Days Overdue | Count + ₹ | Red |
| Repeat Defaulters (>2 terms) | Count | Red |

---

## 5. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Student Name | Text | ✅ | — |
| Student ID | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Class / Stream | Text | ✅ | ✅ |
| Student Type | Badge: Day Scholar · Hosteler | ✅ | ✅ |
| Due Amount | ₹ | ✅ | — |
| Days Overdue | Number (colour-coded) | ✅ | — |
| Terms Defaulted | Count | ✅ | — |
| Last Payment Date | Date | ✅ | — |
| Waiver Request Status | Badge: None · Pending · Approved | ✅ | ✅ |
| Actions | View · Send Reminder · Escalate to Principal | — | — |

### 5.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| Age Bucket | Select: All · 0–30 · 31–60 · >60 days |
| Student Type | Multi-select |
| Class | Multi-select |
| Repeat Defaulter | Toggle |
| Waiver Status | Multi-select |

### 5.2 Search
- Student name · Student ID · 300ms debounce

### 5.3 Pagination
- Server-side · 25 rows/page · Default sort: Days Overdue desc

### 5.4 Bulk Actions
- Select rows → [Send Bulk Reminder] · [Export Selected] · [Escalate to Principals]

---

## 6. Drawers

### 6.1 Drawer: `defaulter-detail` — Student Defaulter Profile
- **Trigger:** View action
- **Width:** 680px

**Tab: Outstanding Fees**

| Term | Fee Component | Billed | Paid | Outstanding | Overdue Days |
|---|---|---|---|---|---|
| Term 1 | Tuition | ₹ | ₹ | ₹ | [N] |
| Term 2 | Hostel | ₹ | ₹ | ₹ | [N] |

**Tab: Payment History**
- All payments made by this student this AY

**Tab: Communication Log**
- Reminders sent, dates, channels, read status

**Tab: Waiver History**
- Previous waiver requests and outcomes

**Actions:**
- [Send Reminder] — WhatsApp / SMS / In-app
- [Initiate Waiver Request] — links to Page 30
- [Escalate to Branch Principal]

### 6.2 Drawer: `escalate` — Escalate to Branch Principal
| Field | Type | Required |
|---|---|---|
| Branch | Read-only | — |
| Students Selected | Read-only | — |
| Escalation Note | Textarea | ✅ |
| Deadline for Response | Date | ✅ |

---

## 7. Charts

### 7.1 Defaulter Count by Branch (Bar)
- **Sort:** Desc
- **Colour:** Red

### 7.2 Outstanding Amount by Aging Bucket (Stacked Bar — by branch)
- **Stacks:** 0–30 · 31–60 · >60

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reminder sent | "Fee reminder sent to [N] defaulters." | Info | 4s |
| Bulk reminder | "Reminders sent to [N] defaulters across [M] branches." | Info | 4s |
| Escalation sent | "Escalation sent to [N] branch principal(s)." | Warning | 4s |
| Export | "Defaulter list exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No defaulters | "No defaulters" | "All students have paid their fees for this term." |
| Filter returns none | "No defaulters match" | "Adjust filters to see defaulters." |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + table skeleton |
| Filter change | Table skeleton |
| Detail drawer | Spinner + skeleton tabs |
| Bulk reminder | Progress bar: sending |

---

## 11. Role-Based UI Visibility

| Element | Collection Head G3 | Finance Mgr G1 | CFO G1 |
|---|---|---|---|
| [Send Reminder] | ✅ | ❌ | ❌ |
| [Escalate] | ✅ | ❌ | ❌ |
| [Initiate Waiver] | ✅ | ❌ | ❌ |
| Bulk actions | ✅ | ❌ | ❌ |
| View full list | ✅ | ✅ | ✅ (summary) |
| Export | ✅ | ✅ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/collection/defaulters/` | JWT (G1+) | Defaulter list |
| GET | `/api/v1/group/{id}/finance/collection/defaulters/{sid}/` | JWT (G1+) | Student detail |
| POST | `/api/v1/group/{id}/finance/collection/defaulters/send-reminder/` | JWT (G3) | Send reminder |
| POST | `/api/v1/group/{id}/finance/collection/defaulters/escalate/` | JWT (G3) | Escalate |
| GET | `/api/v1/group/{id}/finance/collection/defaulters/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../defaulters/?q=` | `#defaulter-table-body` | `innerHTML` |
| Filter | `change` | GET `.../defaulters/?branch=&age=` | `#defaulter-section` | `innerHTML` |
| Detail drawer | `click` | GET `.../defaulters/{sid}/` | `#drawer-body` | `innerHTML` |
| Bulk reminder | `click` | POST `.../defaulters/send-reminder/` | `#bulk-action-bar` | `outerHTML` |
| Pagination | `click` | GET `.../defaulters/?page=` | `#defaulter-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
