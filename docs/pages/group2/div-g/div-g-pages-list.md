# Division G — Group Operations: Page Index

**Total Pages:** 33
**URL Base:** `/group/ops/`
**Tech Stack:** Django 4.2 + HTMX 1.9 + Tailwind CDN · FastAPI · PostgreSQL 16

> **Division scope:** Day-to-day operational management of all branches — SLA enforcement,
> zone-layer management (large groups), bulk procurement, facilities/maintenance, grievance
> resolution, and operational intelligence. Six roles have EduForge access (G3–G4).
> Procurement Manager (G0) and Facilities Manager (G0) use external tools; their work is
> visible through COO/Operations Manager views inside EduForge.

---

## Scale Context

| Dimension | Value |
|---|---|
| Institution Groups | 150 |
| Branches per large group | 20–50 |
| Branches per small group | 5–10 |
| Zones (large groups only) | 3–5 zones · 10–15 branches per zone |
| Staff per large group | 3,000+ |
| Buses per large group | 200–500 |
| Procurement categories | Books · Uniforms · Lab Equipment · IT Hardware · Stationery · Furniture |
| Facility assets | 5–20 buildings per branch · total 100–1,000 assets per large group |
| Maintenance tickets/month | 50–300 across all branches |
| Grievances/month | 20–100 escalated to group level |

---

## Division G — Role Summary

| # | Role | Level | Large | Small | Post-Login URL |
|---|---|---|---|---|---|
| 59 | Group COO | G4 | ✅ Dedicated | ❌ CEO covers | `/group/ops/coo/` |
| 60 | Group Operations Manager | G3 | ✅ Dedicated | ❌ | `/group/ops/manager/` |
| 61 | Group Branch Coordinator | G3 | ✅ Multiple | ✅ 1 | `/group/ops/coordinator/` |
| 62 | Group Zone Director | G4 | ✅ Large only | ❌ | `/group/ops/zone-director/` |
| 63 | Group Zone Academic Coordinator | G3 | ✅ Large only | ❌ | `/group/ops/zone-academic/` |
| 64 | Group Zone Operations Manager | G3 | ✅ Large only | ❌ | `/group/ops/zone-ops/` |
| 65 | Group Procurement Manager | G0 | ✅ Dedicated | ❌ | NO PLATFORM ACCESS — external tools |
| 66 | Group Facilities Manager | G0 | ✅ Dedicated | ❌ | NO PLATFORM ACCESS — external tools |

> G0 roles (Procurement Manager, Facilities Manager) do not log in to EduForge. Their work
> is tracked and visible through COO/Operations Manager views in pages 18–30.

---

## Section 1 — Role Dashboards

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 01 | COO Dashboard | `/group/ops/coo/` | `01-coo-dashboard.md` | P0 | ✅ |
| 02 | Operations Manager Dashboard | `/group/ops/manager/` | `02-ops-manager-dashboard.md` | P0 | ✅ |
| 03 | Branch Coordinator Dashboard | `/group/ops/coordinator/` | `03-branch-coordinator-dashboard.md` | P0 | ✅ |
| 04 | Zone Director Dashboard | `/group/ops/zone-director/` | `04-zone-director-dashboard.md` | P0 | ✅ |
| 05 | Zone Academic Coordinator Dashboard | `/group/ops/zone-academic/` | `05-zone-academic-coordinator-dashboard.md` | P0 | ✅ |
| 06 | Zone Operations Manager Dashboard | `/group/ops/zone-ops/` | `06-zone-ops-manager-dashboard.md` | P0 | ✅ |

---

## Section 2 — Branch Operations Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 07 | Branch Operations Overview | `/group/ops/branches/` | `07-branch-operations-overview.md` | P0 | ✅ |
| 08 | Branch SLA Tracker | `/group/ops/branches/sla/` | `08-branch-sla-tracker.md` | P1 | ✅ |
| 09 | Branch Coordinator Hub | `/group/ops/coordinators/` | `09-branch-coordinator-hub.md` | P1 | ✅ |
| 10 | Branch Visit Scheduler | `/group/ops/visits/` | `10-branch-visit-scheduler.md` | P1 | ✅ |
| 11 | Grievance Resolution Centre | `/group/ops/grievances/` | `11-grievance-resolution-centre.md` | P1 | ✅ |
| 12 | Operational Escalation Tracker | `/group/ops/escalations/` | `12-operational-escalation-tracker.md` | P1 | ✅ |
| 13 | Branch Operational Compliance Checklist | `/group/ops/compliance/` | `13-branch-operational-compliance.md` | P1 | ✅ |

---

## Section 3 — Zone Management (Large Groups Only)

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 14 | Zone Overview | `/group/ops/zones/` | `14-zone-overview.md` | P1 | ✅ |
| 15 | Zone Operations Dashboard | `/group/ops/zones/<id>/ops/` | `15-zone-operations-dashboard.md` | P1 | ✅ |
| 16 | Zone Academic Dashboard | `/group/ops/zones/<id>/academic/` | `16-zone-academic-dashboard.md` | P1 | ✅ |
| 17 | Zone Branch Health Monitor | `/group/ops/zones/<id>/branches/` | `17-zone-branch-health-monitor.md` | P2 | ✅ |

---

## Section 4 — Procurement Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 18 | Procurement Dashboard | `/group/ops/procurement/` | `18-procurement-dashboard.md` | P1 | ✅ |
| 19 | Procurement Request Manager | `/group/ops/procurement/requests/` | `19-procurement-request-manager.md` | P1 | ✅ |
| 20 | Vendor Master | `/group/ops/procurement/vendors/` | `20-vendor-master.md` | P1 | ✅ |
| 21 | Purchase Order Manager | `/group/ops/procurement/purchase-orders/` | `21-purchase-order-manager.md` | P1 | ✅ |
| 22 | Delivery Tracking | `/group/ops/procurement/deliveries/` | `22-delivery-tracking.md` | P2 | ✅ |
| 23 | Procurement Calendar | `/group/ops/procurement/calendar/` | `23-procurement-calendar.md` | P2 | ✅ |
| 24 | Procurement Budget Monitor | `/group/ops/procurement/budget/` | `24-procurement-budget-monitor.md` | P1 | ✅ |

---

## Section 5 — Facilities Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 25 | Facilities Overview Dashboard | `/group/ops/facilities/` | `25-facilities-overview-dashboard.md` | P1 | ✅ |
| 26 | Maintenance Request Tracker | `/group/ops/facilities/maintenance/` | `26-maintenance-request-tracker.md` | P1 | ✅ |
| 27 | Building Infrastructure Register | `/group/ops/facilities/buildings/` | `27-building-infrastructure-register.md` | P2 | ✅ |
| 28 | Capital Expenditure Tracker | `/group/ops/facilities/capex/` | `28-capex-tracker.md` | P1 | ✅ |
| 29 | Utilities Monitor | `/group/ops/facilities/utilities/` | `29-utilities-monitor.md` | P2 | ✅ |
| 30 | Facilities Compliance Register | `/group/ops/facilities/compliance/` | `30-facilities-compliance-register.md` | P1 | ✅ |

---

## Section 6 — Operations Intelligence

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 31 | Operations MIS Report | `/group/ops/reports/mis/` | `31-operations-mis-report.md` | P1 | ✅ |
| 32 | Branch Operational Benchmarking | `/group/ops/reports/benchmarking/` | `32-branch-operational-benchmarking.md` | P1 | ✅ |
| 33 | Operations Audit Log | `/group/ops/audit-log/` | `33-operations-audit-log.md` | P1 | ✅ |

---

## Shared Drawers & Overlays (all div-g pages)

| Drawer / Modal | Trigger | Width | Tabs / Content |
|---|---|---|---|
| `branch-ops-detail` | Branch table → eye icon | 640px | Ops Metrics · SLA · Coordinator · Escalations · Visit History |
| `sla-breach-detail` | SLA Tracker → breach row | 520px | Breach Info · Impact · Remediation Plan · Owner |
| `grievance-create` | Grievance Centre → + New | 560px | Category · Branch · Description · Priority · Attachment |
| `grievance-detail` | Grievance table → row | 640px | Overview · Timeline · Actions · Resolution · Escalation History |
| `escalation-create` | Escalation Tracker → + New | 640px | Type · Branch · Severity · Description · Assignment · Evidence |
| `escalation-detail` | Escalation table → row | 680px | Overview · Timeline · Actions · Owner · SLA status |
| `coordinator-assign` | Coordinator Hub → Assign | 480px | Coordinator select · Branches multi-select · Effective date |
| `visit-schedule-create` | Visit Scheduler → + Schedule | 560px | Branch · Visit Type · Date · Coordinator · Checklist Template |
| `visit-report-submit` | Visit Scheduler → Submit Report | 640px | Observations · Compliance · Issues Found · Photos · Follow-up |
| `zone-create` | Zone Overview → + New Zone | 560px | Zone Name · Director · Branches · Academic Coordinator · Ops Manager |
| `zone-edit` | Zone table → Edit | 560px | Same tabs |
| `vendor-create` | Vendor Master → + New Vendor | 640px | Profile · Categories · Bank Details · Contract · Documents |
| `vendor-edit` | Vendor table → Edit | 640px | Same tabs |
| `vendor-performance` | Vendor table → Performance | 520px | Delivery Rate · Quality Score · PO History · Issues |
| `po-create` | PO Manager → + New PO | 680px | Vendor · Line Items · Branches · Budget · Delivery Terms |
| `po-detail` | PO table → row | 680px | Summary · Line Items · Delivery Status · Payments · Documents |
| `delivery-receive` | Delivery Tracking → Receive | 560px | Items Received · Condition · Shortfall · Damage Report · Photos |
| `maintenance-create` | Maintenance Tracker → + New | 560px | Branch · Category · Priority · Description · Photos · Assign |
| `maintenance-detail` | Maintenance table → row | 640px | Details · Progress · Photos Before/After · Cost · Resolution |
| `building-create` | Infrastructure Register → + New | 600px | Branch · Building Type · Ownership · Documents · Condition |
| `capex-project-create` | CAPEX Tracker → + New | 640px | Project · Branch · Budget · Milestones · Vendor · Timeline |
| `capex-milestone-update` | CAPEX → milestone row | 480px | Status · Photos · Completion % · Notes |
| `compliance-cert-renew` | Facilities Compliance → Renew | 520px | Certificate Type · Renewal Date · Documents · Next Expiry |
| `ops-mis-schedule` | Operations MIS → Schedule | 480px | Recipients · Frequency · Sections · Delivery Channel |
| `audit-detail` | Audit Log → row | 520px | Event · Before/After · Actor · IP · Session · Context |

---

## UI Component Standard (all div-g pages)

| Component | Specification |
|---|---|
| **Tables** | Sortable all columns · Checkbox row select + select-all · Responsive (card on mobile < 768px) · Column visibility toggle · Row count badge |
| **Search** | Full-text, 300ms debounce, highlights match in results |
| **Advanced Filters** | Slide-in filter drawer · Active filters as dismissible chips · "Clear All" · Filter count badge |
| **Pagination** | Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z" · Page jump input |
| **Drawers** | Slide from right · Widths: 480/520/560/600/640/680px · Backdrop click closes (unsaved-changes guard) · ESC closes |
| **Modals** | Centred overlay · Confirm/delete only · Max 480px · Primary + cancel buttons |
| **Forms** | Inline validation on blur · Required `*` · Character counter on textareas · Disabled submit until valid · Server error summary at top |
| **Toasts** | Bottom-right · Success 4s · Error manual dismiss · Warning 6s · Info 4s · Max 3 stacked |
| **Loaders** | Skeleton screens matching layout · Spinner on action buttons · Full-page overlay for critical ops |
| **Empty States** | Illustration + heading + description + CTA · Separate "no data" vs "no search results" |
| **Charts** | Chart.js 4.x · Responsive · Colorblind-safe palette · Legend · Tooltip · PNG export |
| **Role-based UI** | Server-side rendering — G0 has no access · G1 read-only · G3 write within scope · G4 full |

---

## Role → Page Access Matrix

| Page | COO G4 | Ops Mgr G3 | Branch Coord G3 | Zone Dir G4 | Zone Acad G3 | Zone Ops G3 |
|---|---|---|---|---|---|---|
| 01 COO Dashboard | ✅ Full | — | — | — | — | — |
| 02 Ops Manager Dashboard | ✅ View | ✅ Full | — | — | — | — |
| 03 Branch Coord Dashboard | ✅ View | ✅ View | ✅ Full (own branches) | — | — | — |
| 04 Zone Director Dashboard | ✅ View | — | — | ✅ Full (own zone) | — | — |
| 05 Zone Academic Coord Dashboard | ✅ View | — | — | ✅ View | ✅ Full (own zone) | — |
| 06 Zone Ops Manager Dashboard | ✅ View | — | — | ✅ View | — | ✅ Full (own zone) |
| 07 Branch Ops Overview | ✅ All branches | ✅ All branches | ✅ Own branches | ✅ Zone branches | ✅ Zone branches | ✅ Zone branches |
| 08 Branch SLA Tracker | ✅ All | ✅ All | ✅ Own | ✅ Zone | ✅ Zone | ✅ Zone |
| 09 Coordinator Hub | ✅ Full | ✅ Full | ✅ View own | — | — | — |
| 10 Visit Scheduler | ✅ Full | ✅ Full | ✅ Own | ✅ Zone | — | ✅ Zone |
| 11 Grievance Centre | ✅ Full | ✅ Full | ✅ Own branches | ✅ Zone | — | ✅ Zone |
| 12 Escalation Tracker | ✅ Full | ✅ Full | ✅ Own raise/view | ✅ Zone | — | ✅ Zone |
| 13 Compliance Checklist | ✅ Full | ✅ Full | ✅ Own | ✅ Zone | ✅ Zone | ✅ Zone |
| 14 Zone Overview | ✅ Full | ✅ View | — | ✅ Own zone | — | — |
| 15 Zone Ops Dashboard | ✅ All zones | ✅ All zones | — | ✅ Own zone | — | ✅ Own zone |
| 16 Zone Academic Dashboard | ✅ All zones | ✅ View | — | ✅ Own zone | ✅ Own zone | — |
| 17 Zone Branch Health | ✅ All | ✅ All | — | ✅ Own | ✅ Own | ✅ Own |
| 18 Procurement Dashboard | ✅ Full | ✅ View | — | — | — | — |
| 19 Procurement Requests | ✅ Full | ✅ Approve | — | — | — | — |
| 20 Vendor Master | ✅ Full | ✅ View | — | — | — | — |
| 21 Purchase Order Manager | ✅ Full | ✅ View | — | — | — | — |
| 22 Delivery Tracking | ✅ Full | ✅ Full | — | — | — | — |
| 23 Procurement Calendar | ✅ Full | ✅ View | — | — | — | — |
| 24 Procurement Budget | ✅ Full | ✅ View | — | — | — | — |
| 25 Facilities Overview | ✅ Full | ✅ View | — | ✅ Zone | — | ✅ Zone |
| 26 Maintenance Tracker | ✅ Full | ✅ Full | ✅ Own | ✅ Zone | — | ✅ Zone |
| 27 Building Register | ✅ Full | ✅ View | — | ✅ Zone | — | — |
| 28 CAPEX Tracker | ✅ Full | ✅ View | — | — | — | — |
| 29 Utilities Monitor | ✅ Full | ✅ View | — | ✅ Zone | — | ✅ Zone |
| 30 Facilities Compliance | ✅ Full | ✅ Full | ✅ Own | ✅ Zone | — | ✅ Zone |
| 31 Ops MIS Report | ✅ Full | ✅ View/Schedule | — | ✅ Zone | — | — |
| 32 Benchmarking | ✅ Full | ✅ Full | — | ✅ Zone | ✅ Zone | ✅ Zone |
| 33 Ops Audit Log | ✅ Full | ✅ Full | ✅ Own actions | ✅ Zone | ✅ Own | ✅ Own |

---

## Full Functional Coverage Audit — Zero Gaps

| # | Job to Be Done | Role | Page(s) |
|---|---|---|---|
| 1 | See all-branch operational health at a glance | COO | 01, 07 |
| 2 | Monitor SLA compliance across all branches | COO/Ops Mgr | 01, 08 |
| 3 | Manage and resolve operational escalations | COO/Ops Mgr | 01, 12 |
| 4 | Track and resolve grievances from all branches | Ops Mgr | 02, 11 |
| 5 | Assign/reassign branch coordinators | COO/Ops Mgr | 09 |
| 6 | Schedule coordinator visits to branches | Ops Mgr/Coordinator | 10 |
| 7 | Submit and review post-visit reports | Branch Coordinator | 10 |
| 8 | See only my assigned branches | Branch Coordinator | 03, 07 |
| 9 | Raise operational issues from branch observations | Branch Coordinator | 12 |
| 10 | Manage zone structure (large groups) | COO | 14 |
| 11 | Monitor zone-level operational KPIs | Zone Director/Ops Mgr | 04, 15 |
| 12 | Monitor zone-level academic performance | Zone Academic Coord | 05, 16 |
| 13 | View health of all branches in my zone | Zone Director | 17 |
| 14 | Manage all branch procurement requests | COO/Ops Mgr | 18, 19 |
| 15 | Consolidate multiple branch requests into bulk PO | COO | 19, 21 |
| 16 | Manage approved vendor registry | COO | 20 |
| 17 | Create, approve, and track purchase orders | COO | 21 |
| 18 | Track deliveries to branches and log shortfalls | Ops Mgr | 22 |
| 19 | Plan seasonal procurement (textbooks, uniforms) | COO | 23 |
| 20 | Monitor procurement budget vs actuals | COO | 24 |
| 21 | View facility health across all campuses | COO | 25 |
| 22 | Track maintenance requests and SLAs | Ops Mgr/Zone Ops | 26 |
| 23 | Maintain building and asset register | COO | 27 |
| 24 | Track CAPEX projects (renovation, construction) | COO | 28 |
| 25 | Monitor utility costs per branch | COO | 29 |
| 26 | Track facility compliance certs (fire NOC, etc.) | COO/Ops Mgr | 30 |
| 27 | Alert on expiring safety certificates | COO/Ops Mgr | 30 |
| 28 | Generate monthly operations MIS report | COO | 31 |
| 29 | Benchmark branches on operational metrics | COO/Ops Mgr | 32 |
| 30 | Immutable audit log of all ops actions | COO | 33 |
| 31 | Branch compliance checklist tracking | Ops Mgr | 13 |
| 32 | View coordinator performance (visits, issues, comms) | Ops Mgr | 09 |

---

## Functional Gaps — Fully Resolved

| Gap | Resolution |
|---|---|
| No post-login dashboards per ops role | Pages 01–06 — dedicated dashboard per role |
| No cross-branch SLA framework | Page 08 — SLA definitions + per-branch compliance table |
| No coordinator assignment/tracking system | Page 09 — Coordinator Hub with assignment + performance |
| No branch visit scheduling or post-visit reports | Page 10 — Visit Scheduler with report submission |
| Grievances only tracked at branch level, not group | Page 11 — Grievance Resolution Centre (escalated to group) |
| Escalations had no severity SLA | Page 12 — Severity 1–4 with SLA timers and breach alerts |
| No operational compliance checklist per branch | Page 13 — Branch Compliance Checklist with score |
| Zone management was only in Div-A as structure | Pages 14–17 — Full zone ops + academic dashboards |
| Procurement requests not visible in EduForge | Pages 18–24 — Full procurement lifecycle in platform |
| No vendor registry or PO tracking | Pages 20–21 — Vendor Master + PO Manager |
| Deliveries to branches untracked | Page 22 — Delivery Tracking with shortfall reporting |
| Procurement seasonal planning absent | Page 23 — Procurement Calendar |
| Facilities/maintenance invisible in EduForge | Pages 25–26 — Facilities Dashboard + Maintenance Tracker |
| No building asset register | Page 27 — Building Infrastructure Register |
| CAPEX projects tracked offline only | Page 28 — CAPEX Tracker with milestones |
| Utility cost monitoring absent | Page 29 — Utilities Monitor with anomaly alerts |
| Safety certificate expiry not tracked | Page 30 — Facilities Compliance Register with alerts |
| No operations MIS report | Page 31 — Auto-generated monthly MIS |
| No cross-branch operational benchmarking | Page 32 — Branch Operational Benchmarking |
| No ops-level audit log | Page 33 — Operations Audit Log |

---

## Implementation Priority

```
P0 — Before group operations portal goes live
  01–06   All 6 role dashboards
  07      Branch Operations Overview

P1 — Sprint 2
  08, 09, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 24, 25, 26, 28, 30, 31, 32, 33

P2 — Sprint 3
  17, 22, 23, 27, 29
```

---

*Last updated: 2026-03-21 · Total pages: 33 · Roles: 8 (6 with platform access) · Gaps resolved: 20 · Audit: zero gaps remaining*
