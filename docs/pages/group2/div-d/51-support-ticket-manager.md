# 51 — Support Ticket Manager

- **URL:** `/group/finance/eduforge-billing/support/`
- **Template:** `portal_base.html`
- **Priority:** P2
- **Role:** EduForge Billing Coordinator G3 (primary)

---

## 1. Purpose

The Support Ticket Manager tracks all support tickets raised with EduForge on behalf of branches — billing disputes, payment issues, plan queries, feature requests, and technical issues. The Billing Coordinator acts as the group's single point of contact with EduForge support, consolidating tickets from all branches, tracking status, and escalating SLA breaches.

This page does not duplicate EduForge's own ticket system; instead it mirrors/links ticket data (via API or manual entry) so the group has visibility of open issues across all branches without logging into EduForge's portal separately.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group EduForge Billing Coordinator | G3 | Full read + raise + close tickets |
| Group CFO | G1 | Read — open billing disputes only |
| Group Finance Manager | G1 | Read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → EduForge Billing → Support Ticket Manager
```

### 3.2 Page Header
- **Title:** `EduForge Support Ticket Manager`
- **Subtitle:** `[N] Open Tickets · [X] SLA Breached · [Y] Billing Disputes: ₹[Z]`
- **Right-side controls:** `[Branch ▾]` `[Type ▾]` `[Status ▾]` `[+ Raise Ticket]` `[Export ↓]`

### 3.3 Alert Banner

| Condition | Banner | Severity |
|---|---|---|
| SLA breached | "[N] ticket(s) have breached SLA. Escalate immediately." | Red |
| Unresponded > 48h | "[N] ticket(s) have not received a response in 48+ hours." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Open Tickets | Count | Red if SLA breach |
| Resolved This Month | Count | Neutral |
| Avg Resolution Time | Days | Red if > 5 |
| SLA Breached | Count | Red if > 0 |
| Billing Disputes | Count | Amber if > 0 |
| Dispute Value | ₹ | Amber if > 0 |

---

## 5. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Ticket ID | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Subject | Text | — | — |
| Type | Badge: Billing · Technical · Plan Query · Feature Request · Other | ✅ | ✅ |
| Priority | Badge: Critical · High · Medium · Low | ✅ | ✅ |
| Status | Badge: Open · In Progress · Awaiting Response · Resolved · Closed | ✅ | ✅ |
| Raised Date | Date | ✅ | — |
| Last Updated | Date | ✅ | — |
| Days Open | Number (red if > SLA) | ✅ | — |
| SLA Status | Badge: Within SLA · SLA Breached | ✅ | ✅ |
| Assigned To | Text (EduForge agent) | ✅ | — |
| Actions | View · Add Note · Close | — | — |

### 5.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| Type | Multi-select |
| Priority | Multi-select |
| Status | Multi-select |
| SLA Status | Select |
| Date Range | Date picker |

### 5.2 Search
- Ticket ID · Subject keyword

### 5.3 Pagination
- 25 rows/page · Sort: Priority + Raised Date (oldest critical first)

---

## 6. Drawers

### 6.1 Drawer: `ticket-raise` — Raise New Ticket
- **Trigger:** [+ Raise Ticket]
- **Width:** 680px

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | ✅ | |
| Subject | Text | ✅ | Max 200 chars |
| Type | Select | ✅ | |
| Priority | Select | ✅ | |
| Description | Textarea | ✅ | Min 50 chars |
| Attachments | File upload (multi) | ❌ | PDF/image/screenshot |
| EduForge Ref No | Text | ❌ | If already raised externally |

- [Cancel] [Raise Ticket]

### 6.2 Drawer: `ticket-detail` — Ticket Detail
- **Width:** 760px

**Ticket Summary:**
- ID · Branch · Type · Priority · Status · SLA Status

**Communication Thread:**
- Chronological messages between group coordinator and EduForge

**[Add Note / Reply]:**
| Field | Type | Required |
|---|---|---|
| Note | Textarea | ✅ |
| Attachment | File upload | ❌ |
| Mark as Internal | Toggle | — |

**Timeline:**
- Created → Acknowledged → Responded → Resolved

**Actions:**
- [Mark Resolved] [Mark Closed] [Escalate to Manager]

### 6.3 Drawer: `billing-dispute` — Billing Dispute Detail
- **Width:** 720px

For tickets of type "Billing":

| Field | Type |
|---|---|
| Invoice in Dispute | Select / Text |
| Dispute Amount | ₹ |
| Dispute Reason | Select: Overcharge · Wrong Plan · Seat Error · Other |
| Resolution Status | Badge: Open · Credit Applied · Refund Issued · Dispute Closed |

---

## 7. Charts

### 7.1 Ticket Volume by Type (Bar — Monthly)
### 7.2 Resolution Time Distribution (Histogram)
### 7.3 SLA Compliance Rate (Line — Monthly)

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Ticket raised | "Ticket [ID] raised for [Branch]." | Success | 4s |
| Note added | "Note added to Ticket [ID]." | Info | 3s |
| Ticket resolved | "Ticket [ID] marked as resolved." | Success | 3s |
| SLA breach | "Ticket [ID] has breached SLA. Escalate immediately." | Warning | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No tickets | "No support tickets" | "All branches are operating without open support issues." | [+ Raise Ticket] |

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
| [+ Raise Ticket] | ✅ | ❌ | ❌ |
| [Add Note] | ✅ | ❌ | ❌ |
| [Mark Resolved] | ✅ | ❌ | ❌ |
| View all tickets | ✅ | ✅ (billing only) | ✅ |
| Export | ✅ | ❌ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/billing/support/` | JWT (G1+) | Ticket list |
| POST | `/api/v1/group/{id}/finance/billing/support/` | JWT (G3) | Raise ticket |
| GET | `/api/v1/group/{id}/finance/billing/support/{tid}/` | JWT (G1+) | Ticket detail |
| POST | `/api/v1/group/{id}/finance/billing/support/{tid}/note/` | JWT (G3) | Add note |
| POST | `/api/v1/group/{id}/finance/billing/support/{tid}/resolve/` | JWT (G3) | Mark resolved |
| GET | `/api/v1/group/{id}/finance/billing/support/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter | `change` | GET `.../support/?type=&status=` | `#ticket-table` | `innerHTML` |
| Raise drawer | `click` | GET `.../support/raise-form/` | `#drawer-body` | `innerHTML` |
| Detail drawer | `click` | GET `.../support/{id}/` | `#drawer-body` | `innerHTML` |
| Submit note | `submit` | POST `.../support/{id}/note/` | `#ticket-thread-{id}` | `beforeend` |
| Resolve | `click` | POST `.../support/{id}/resolve/` | `#ticket-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
