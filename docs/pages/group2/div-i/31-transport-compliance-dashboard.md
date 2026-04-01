# 31 — Transport Compliance Dashboard

> **URL:** `/group/transport/compliance/`
> **File:** `31-transport-compliance-dashboard.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Transport Director (primary) · Fleet Manager · Safety Officer

---

## 1. Purpose

Consolidated view of all compliance dimensions across the transport system — vehicle documents (fitness/permit/insurance), driver licences, driver BGV, training certification, GPS device coverage, and route approval status. A single compliance score is computed per branch and for the group as a whole.

This dashboard is the Transport Director's compliance control tower. Any red indicator here means immediate action is required — an expired fitness cert, a lapsed driver licence, or an incomplete BGV can expose the group to criminal liability.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Director | G3 | Full — view all compliance | Primary consumer |
| Group Fleet Manager | G3 | Full — vehicle compliance | Vehicles + GPS |
| Group Transport Safety Officer | G3 | Full — safety compliance | Driver + safety |
| Group CFO | G1 | View — insurance cost impact | Insurance only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Transport Compliance Dashboard
```

### 3.2 Page Header
```
Transport Compliance Dashboard                              [Export Compliance Report ↓]
AY [current academic year]  ·  Group Compliance Score: [N]%  ·  [N] Issues Outstanding
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Any expired vehicle document | "[N] vehicles have expired documents — operation is illegal." | Red |
| Drivers with expired licence on duty | "[N] drivers with expired licences are on active duty." | Red |
| BGV failures | "[N] staff have FAILED BGV — must be removed immediately." | Red |
| Overall compliance < 90% | "Group transport compliance score dropped below 90%." | Amber |

---

## 4. Overall Compliance Score Card

```
╔══════════════════════════════════════════╗
║   OVERALL TRANSPORT COMPLIANCE SCORE     ║
║              [N]%                        ║
║  Vehicle: [N]% · Driver: [N]% · GPS [N]% ║
╚══════════════════════════════════════════╝
```

Colour: Green ≥ 95% · Yellow 85–95% · Red < 85%.

---

## 5. Sections

### 5.1 Compliance by Category

| Category | Total Items | Compliant | Non-Compliant | Score % | Action |
|---|---|---|---|---|---|
| Vehicle Fitness Certs | [N] | [N] | [N] | [N]% | → Page 09 |
| Vehicle Insurance | [N] | [N] | [N] | [N]% | → Page 09 |
| Route Permits | [N] | [N] | [N] | [N]% | → Page 09 |
| Driver Licences | [N] | [N] | [N] | [N]% | → Page 16 |
| Driver BGV | [N] | [N] | [N] | [N]% | → Page 17 |
| Driver Training | [N] | [N] | [N] | [N]% | → Page 17 |
| GPS Coverage | [N] | [N] | [N] | [N]% | → Page 19 |
| Route Approvals | [N] | [N] | [N] | [N]% | → Page 11 |

---

### 5.2 Branch Compliance Scorecard

> Per-branch compliance across all categories.

**Filters:** Branch multi-select.

**Columns:** Branch · Vehicle % · Driver Licence % · BGV % · Training % · GPS % · Overall % · Actions (View Detail · Send Alert)

**Default sort:** Overall % ascending (worst first).
**Colour coding:** Green ≥ 95% · Yellow 85–95% · Red < 85%.

---

### 5.3 Critical Non-Compliance List

> Immediate attention items — expired documents, failed BGV, active non-compliant assets.

**Columns:** Type · Description · Branch · Bus No / Driver Name · Days Non-Compliant · Risk Level · [Action →]

**Default sort:** Days non-compliant descending.

---

### 5.4 Compliance Trend (Chart)

**Chart — 12-month compliance score trend (line chart)**
- Overall score · Vehicle score · Driver score
- Target line at 95%

---

## 6. Drawers

### 6.1 Drawer: `branch-compliance-detail`
- **Width:** 680px
- **Tabs:** Vehicles · Drivers · GPS · Actions Log
- All compliance items for this branch with status and expiry dates
- Actions log: reminders sent, renewals completed

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Compliance report exported | "Transport compliance report exported." | Info | 4s |
| Export failed | "Export failed. Please try again." | Error | 5s |
| Alert sent to branch | "Compliance alert sent to [Branch] transport in-charge." | Info | 4s |
| Alert send failed | "Failed to send compliance alert to [Branch]. Please retry." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| 100% compliance | "Full Transport Compliance" | "All vehicles, drivers, and devices are compliant." |
| No filter results (branch) | "No Branches Match Filters" | "Adjust the branch selection filter." | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: Score card + category table + branch table + chart |
| Branch filter | Table body skeleton |
| Branch detail drawer | 680px skeleton |

---

## 10. Role-Based UI Visibility

| Element | Transport Director G3 | Fleet Manager G3 | Safety Officer G3 | CFO G1 |
|---|---|---|---|---|
| View All Categories | ✅ | ✅ | ✅ | Insurance only |
| Send Compliance Alert | ✅ | ✅ | ✅ | ❌ |
| Export Report | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/compliance/score/` | JWT (G3+) | Overall compliance score |
| GET | `/api/v1/group/{group_id}/transport/compliance/categories/` | JWT (G3+) | Category-wise compliance |
| GET | `/api/v1/group/{group_id}/transport/compliance/branches/` | JWT (G3+) | Branch compliance scorecard |
| GET | `/api/v1/group/{group_id}/transport/compliance/critical-issues/` | JWT (G3+) | Critical non-compliance items |
| GET | `/api/v1/group/{group_id}/transport/compliance/trend/` | JWT (G3+) | 12-month trend chart data |
| GET | `/api/v1/group/{group_id}/transport/compliance/branches/{id}/detail/` | JWT (G3+) | Branch detail drawer |
| POST | `/api/v1/group/{group_id}/transport/compliance/branches/{id}/alert/` | JWT (G3+) | Send compliance alert |
| GET | `/api/v1/group/{group_id}/transport/compliance/export/` | JWT (G3+) | Export compliance report |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Score card auto-refresh | `every 300s` | GET `.../compliance/score/` | `#compliance-score-card` | `innerHTML` |
| Branch filter | `change` | GET `.../compliance/branches/?{filters}` | `#branch-scorecard-section` | `innerHTML` |
| Branch scorecard sort | `click` on header | GET `.../compliance/branches/?sort={col}&dir={asc/desc}` | `#branch-scorecard-section` | `innerHTML` |
| Open branch detail drawer | `click` on Branch | GET `.../compliance/branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Send compliance alert | `click` | POST `.../compliance/branches/{id}/alert/` | `#alert-btn-{id}` | `outerHTML` |
| Export report | `click` | GET `.../compliance/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
