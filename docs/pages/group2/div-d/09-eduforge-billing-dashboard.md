# 09 — Group EduForge Billing Coordinator Dashboard

- **URL:** `/group/finance/eduforge-billing/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group EduForge Billing Coordinator (Role 38, G3)

---

## 1. Purpose

The EduForge Billing Dashboard manages the group's subscription to the EduForge SaaS platform. Every branch in the group is on an EduForge plan — the coordinator ensures plans are renewed before expiry (a lapsed branch loses portal access, disrupting operations), manages plan upgrades when a branch grows, raises support tickets for technical issues, and monitors platform usage to ensure license compliance.

This role is the primary commercial interface between the institution group and EduForge (the SaaS provider). Unlike other finance pages that track student fees or vendor payments, this page tracks the group's own SaaS cost — often ₹50,000–₹5,00,000/month depending on branch count and plan tier.

Support ticket management here is critical: when a branch reports a platform bug, the billing coordinator raises a ticket centrally (not each branch separately) to ensure SLAs are enforced.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group EduForge Billing Coordinator | G3 | Full read + manage plans + raise tickets | Primary owner |
| Group IT Admin | G4 | Read + technical ticket details | Collaborates on tech tickets |
| Group CFO | G1 | Read — billing cost + renewal dates | Financial oversight |
| Group IT Director | G4 | Read — all sections | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → EduForge Billing Dashboard
```

### 3.2 Page Header
- **Title:** `EduForge Billing Dashboard`
- **Subtitle:** `Platform Subscription Management · [N] Branches`
- **Role Badge:** `Group EduForge Billing Coordinator`
- **Right-side controls:** `[+ Raise Support Ticket]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any branch plan expiring within 30 days | "[N] branch plan(s) renewing within 30 days. Total: ₹[X]. Confirm payment." | Amber |
| Any branch plan expired / lapsed | "[N] branch(es) have lapsed plans. Portal access may be suspended." | Red |
| Open critical support ticket > 24 hours unresolved | "Critical ticket #[ID] unresolved for [N] hours. Escalate immediately." | Red |
| Usage exceeding license limits | "[N] branch(es) exceeding licensed user count. Upgrade required." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Branch Plans | Count | Green = all branches | → Page 49 |
| Expiring Within 30 Days | Count | Amber if > 0 | → Page 50 |
| Lapsed Plans | Count | Red if > 0 | → Page 50 |
| Monthly Platform Cost | ₹ | Informational | → Page 49 |
| Open Support Tickets | Count | Red if critical open | → Page 51 |
| License Overage Branches | Count | Red if > 0 | → Page 52 |

---

## 5. Section 5.1 — Branch Plan Overview

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Plan Tier | Badge: Starter · Growth · Enterprise | ✅ |
| Licensed Users | Number | ✅ |
| Active Users | Number | ✅ |
| Monthly Cost | ₹ | ✅ |
| Renewal Date | Date | ✅ |
| Status | Badge: Active · Expiring Soon · Lapsed · Suspended | ✅ |
| Actions | View · Renew · Upgrade | — |

**Filters:** Plan Tier · Status · Branch
**Search:** Branch name
**Pagination:** 20 rows/page

---

## 5.2 Section 5.2 — Support Tickets

| Column | Type | Sortable |
|---|---|---|
| Ticket ID | Text | ✅ |
| Branch | Text | ✅ |
| Subject | Text | ✅ |
| Priority | Badge: Critical · High · Medium · Low | ✅ |
| Status | Badge: Open · In Progress · Resolved · Closed | ✅ |
| Raised Date | Date | ✅ |
| SLA Due | Date (red if past) | ✅ |
| Actions | View · Comment · Escalate | — |

**[View All Tickets →]** links to Page 51.

---

## 6. Charts

### 6.1 Monthly Platform Cost Trend (Line)
- **X-axis:** Last 12 months
- **Y-axis:** ₹
- **Export:** PNG

### 6.2 Ticket Volume by Priority (Bar — Monthly)
- **Series:** Critical · High · Medium · Low

---

## 7. Drawers

### 7.1 Drawer: `raise-ticket` — Raise Support Ticket
- **Trigger:** [+ Raise Support Ticket]
- **Width:** 640px

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select (multi) | ✅ | |
| Subject | Text | ✅ | Max 200 chars |
| Priority | Select | ✅ | Critical · High · Medium · Low |
| Category | Select | ✅ | Login · Fee · Reports · Data · Performance · Other |
| Description | Textarea | ✅ | Min 50 chars |
| Attachments | File upload | ❌ | PNG/PDF/MP4 max 20MB |
| Expected Resolution | Date | ❌ | |

- [Cancel] [Raise Ticket]

### 7.2 Drawer: `renew-plan` — Renew Branch Plan
- **Trigger:** Renew action on branch
- **Width:** 580px

| Field | Value / Type |
|---|---|
| Branch | Read-only |
| Current Plan | Read-only |
| Renewal Period | Select: 1 month · 3 months · 6 months · 12 months |
| Amount | Auto-calculated ₹ |
| Payment Mode | Select: Bank Transfer · Cheque · Online |
| Payment Reference | Text |
| Renewal Date (new) | Auto-set = today + period |

- [Cancel] [Confirm Renewal]

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Ticket raised | "Support ticket #[ID] raised. SLA: [Date]." | Success | 4s |
| Plan renewed | "Plan renewed for [Branch] until [Date]." | Success | 4s |
| Ticket escalated | "Ticket #[ID] escalated to EduForge Account Manager." | Info | 4s |
| Export | "Billing report exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open tickets | "No open tickets" | "All support issues are resolved." | [+ Raise Support Ticket] |
| No expiring plans | "All plans current" | "No branch plans expiring in the next 30 days." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + 2 table skeletons |
| Ticket drawer | Spinner + skeleton form |
| Renew drawer | Spinner + skeleton fields |

---

## 11. Role-Based UI Visibility

| Element | Billing Coord G3 | IT Admin G4 | CFO G1 |
|---|---|---|---|
| [+ Raise Ticket] | ✅ | ✅ | ❌ |
| [Renew] plan | ✅ | ❌ | ❌ |
| [Upgrade] plan | ✅ | ❌ | ❌ |
| [Escalate] ticket | ✅ | ✅ | ❌ |
| View all sections | ✅ | ✅ | ✅ (cost only) |
| Export | ✅ | ❌ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/eduforge-billing/kpis/` | JWT (G1+) | KPI cards |
| GET | `/api/v1/group/{id}/finance/eduforge-billing/plans/` | JWT (G1+) | Branch plan list |
| POST | `/api/v1/group/{id}/finance/eduforge-billing/plans/{bid}/renew/` | JWT (G3) | Renew plan |
| POST | `/api/v1/group/{id}/finance/eduforge-billing/tickets/` | JWT (G3+) | Raise ticket |
| GET | `/api/v1/group/{id}/finance/eduforge-billing/tickets/` | JWT (G1+) | Ticket list |
| PUT | `/api/v1/group/{id}/finance/eduforge-billing/tickets/{tid}/escalate/` | JWT (G3+) | Escalate ticket |
| GET | `/api/v1/group/{id}/finance/eduforge-billing/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search branches | `input delay:300ms` | GET `.../plans/?q=` | `#plans-table-body` | `innerHTML` |
| Filter by status | `change` | GET `.../plans/?status=` | `#plans-section` | `innerHTML` |
| Raise ticket drawer | `click` | GET `.../tickets/form/` | `#drawer-body` | `innerHTML` |
| Submit ticket | `submit` | POST `.../tickets/` | `#drawer-body` | `innerHTML` |
| Renew drawer | `click` | GET `.../plans/{bid}/renew-form/` | `#drawer-body` | `innerHTML` |
| Confirm renewal | `submit` | POST `.../plans/{bid}/renew/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
