# 08 — Branch SLA Tracker

> **URL:** `/group/ops/branches/sla/`
> **File:** `08-branch-sla-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 · Operations Manager G3 · Zone Director G4 (zone) · Zone Ops Manager G3 (zone)

---

## 1. Purpose

Defines, monitors, and enforces the Group's SLA (Service Level Agreement) framework across
all branches. For each defined SLA metric, shows per-branch compliance, breach history, and
enables the Operations Manager to raise remediation actions. The SLA framework is the
backbone of operational accountability.

---

## 2. SLA Framework Definitions

> These are the platform-enforced SLA metrics. Configurable by COO.

| SLA ID | Metric | Target | P-Level if Breached |
|---|---|---|---|
| SLA-01 | Daily attendance submitted by 9:30 AM | 100% of school days | P3 if missed 3+ consecutive days |
| SLA-02 | Fee defaulter follow-up within 7 days of due date | 100% | P2 if overdue 14+ days |
| SLA-03 | Exam results published within 5 days of exam | 95% | P2 if >7 days |
| SLA-04 | Grievances acknowledged within 24h | 100% | P1 if child safety · P2 otherwise |
| SLA-05 | Grievances resolved within 7 days | 90% | P2 if >14 days |
| SLA-06 | Maintenance Critical tickets resolved within 4h | 100% | P1 if >4h |
| SLA-07 | Maintenance High tickets resolved within 24h | 95% | P2 if >48h |
| SLA-08 | Staff BGV completed before branch access granted | 100% | P1 if any unapproved access |
| SLA-09 | Parent communication (PTM notice) sent 14 days ahead | 100% | P3 |
| SLA-10 | Coordinator visit completed at least once per month | 100% | P3 if missed 2 consecutive months |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Branch SLA Tracker
```

### 3.2 Page Header
```
Branch SLA Tracker                    [+ Configure SLA]  [Export Report ↓]  [⚙ Settings]
Group-wide SLA compliance · Academic Year [current year] · Updated: [timestamp]
```

### 3.3 Summary Strip
| Card | Value |
|---|---|
| Overall SLA Compliance | `92.4%` group average |
| Branches Fully Compliant | `34 / 50` |
| Active SLA Breaches | `12 current breaches` |
| P1 Breaches | `2` (red badge, pulsing if >0) |

---

## 4. Search & Filters

**Search:** Branch name, SLA metric name. 300ms debounce.

**Advanced Filters:**
| Filter | Options |
|---|---|
| Zone | Multi-select |
| SLA Metric | Multi-select (SLA-01 through SLA-10) |
| Compliance Status | Compliant · At Risk · Breached |
| Breach Severity | P1 · P2 · P3 |
| Date Range | This month · Last 3 months · Custom |

---

## 5. SLA Compliance Table

> Rows = Branches · Columns = SLA metrics. Heat-map view.

**Table View (default):**

| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | Link → branch SLA detail drawer |
| Zone | ✅ | |
| Overall SLA % | ✅ | Composite score |
| SLA-01 Attendance | ✅ | ✅ / ⚠ / ❌ icon |
| SLA-02 Fee Follow-up | ✅ | ✅ / ⚠ / ❌ |
| SLA-03 Results | ✅ | |
| SLA-04 Grievance Ack | ✅ | |
| SLA-05 Grievance Res | ✅ | |
| SLA-06 Critical Maint | ✅ | |
| SLA-07 High Maint | ✅ | |
| SLA-08 BGV | ✅ | |
| SLA-09 PTM Notice | ✅ | |
| SLA-10 Coordinator Visit | ✅ | |
| Actions | ❌ | View Details · Raise Breach Alert |

**Colour coding:**
- ✅ Green: Compliant (≥ target)
- ⚠ Yellow: At Risk (within 5% of target)
- ❌ Red: Breached (below target)

**Toggle view:** Table / Heat-map Grid — heat-map shows same data as colour grid, compact.

**Pagination:** Server-side · 25/page · 10/25/50/All.

---

## 6. Active Breaches Table

> Dedicated section below the main table for all current SLA breaches.

**Columns:**
| Column | Sortable |
|---|---|
| Branch | ✅ |
| SLA Metric | ✅ |
| Severity | ✅ |
| Breach Started | ✅ |
| Days Breached | ✅ (red if >7) |
| Assigned To | ✅ |
| Status | ✅ (Active / Remediation in Progress / Escalated) |
| Actions | — (View · Assign · Escalate · Resolve) |

---

## 7. SLA Trend Chart

**Type:** Multi-line — Overall SLA % per month (12 months), with overlay for breach count.

**Filter:** Zone selector · SLA metric selector (show one specific SLA trend).

**Library:** Chart.js 4.x. PNG export.

---

## 8. SLA Configuration (COO only)

**Sub-section at bottom of page (collapsed by default):**
- Configure SLA targets (edit target values per metric)
- Configure breach severity mapping
- Enable/disable specific SLA metrics per group
- [Save SLA Config] — audited action

---

## 9. Branch SLA Detail Drawer

- **Width:** 520px
- **Tabs:** Overview · Breach History · Remediation · Configure
- **Overview tab:** All 10 SLA metrics for this branch, current status, last breach date
- **Breach History tab:** All historical breaches with resolution times
- **Remediation tab:** Current remediation plan, owner, due date, actions
- **Configure tab (COO only):** Override specific SLA targets for this branch (e.g., remote branch has different attendance SLA)

---

## 10. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Breach assigned | "Breach remediation assigned to [Name]" | Success · 4s |
| Breach escalated | "Breach escalated — COO notified" | Warning · 6s |
| SLA config saved | "SLA configuration updated" | Success · 4s |
| Export done | "SLA report export started" | Info · 4s |

---

## 11. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No breaches | "All branches meeting SLA targets" | — |
| No branches | "No branches found" | [Clear Filters] |

---

## 12. Loader States

Page load: Skeleton summary strip + skeleton heat-map grid (5 rows × 10 columns) + breach table.

---

## 13. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Zone Dir G4 | Zone Ops G3 |
|---|---|---|---|---|
| All branches | ✅ | ✅ | Zone only | Zone only |
| [Configure SLA] button | ✅ | ❌ | ❌ | ❌ |
| [Assign] breach | ✅ | ✅ | ✅ zone | ✅ zone |
| [Escalate] breach | ✅ | ✅ | ✅ | ❌ |
| Export report | ✅ | ✅ | ✅ | ❌ |
| SLA Configure drawer tab | ✅ | ❌ | ❌ | ❌ |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/ops/sla/` | JWT (G3+) | SLA compliance table (all branches) |
| GET | `/api/v1/group/{id}/ops/sla/breaches/` | JWT (G3+) | Active breaches |
| GET | `/api/v1/group/{id}/ops/sla/trend/` | JWT (G3+) | 12-month trend chart |
| GET | `/api/v1/group/{id}/ops/sla/branches/{branch_id}/` | JWT (G3+) | Branch SLA detail |
| POST | `/api/v1/group/{id}/ops/sla/breaches/{breach_id}/assign/` | JWT (G3+) | Assign breach |
| POST | `/api/v1/group/{id}/ops/sla/breaches/{breach_id}/escalate/` | JWT (G3+) | Escalate breach |
| PUT | `/api/v1/group/{id}/ops/sla/config/` | JWT (G4) | Update SLA config (COO only) |
| GET | `/api/v1/group/{id}/ops/sla/export/?format=pdf` | JWT (G3+) | Export report |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | `/api/.../ops/sla/?q={}` | `#sla-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../ops/sla/?filters={}` | `#sla-table-section` | `innerHTML` |
| Sort | `click` | `/api/.../ops/sla/?sort={}&dir={}` | `#sla-table-section` | `innerHTML` |
| Toggle heat-map | `click` | `/api/.../ops/sla/?view=heatmap` | `#sla-view-container` | `innerHTML` |
| Branch SLA detail | `click` | `/api/.../ops/sla/branches/{id}/` | `#drawer-body` | `innerHTML` |
| Assign breach | `click` | POST `/api/.../sla/breaches/{id}/assign/` | `#breach-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
