# 39 — Quarterly Branch Audit Planner

- **URL:** `/group/finance/audit/planner/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Internal Auditor G1 (primary) · Finance Manager G1

---

## 1. Purpose

The Quarterly Branch Audit Planner manages the schedule of internal financial audits across all branches for the financial year. The Internal Auditor must audit every branch at least once per quarter — for large groups with 50 branches, this means scheduling ~200 audit events per year. The planner ensures no branch is missed, manages auditor assignment, tracks audit readiness, and sends pre-audit notices to branches.

Each audit is planned with start date, end date, assigned auditor(s), checklist template, and scope (full audit / targeted / surprise). The planner auto-calculates which branches are overdue for their quarterly audit and highlights them for priority scheduling.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Internal Auditor | G1 | Full read + schedule + assign |
| Group Finance Manager | G1 | Read + sign off on completed audits |
| Group CFO | G1 | Read — status overview |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Internal Audit → Quarterly Audit Planner
```

### 3.2 Page Header
- **Title:** `Quarterly Audit Planner`
- **Subtitle:** `FY [Year] · Q[N] · [N] Scheduled · [X] Completed · [Y] Overdue`
- **Right-side controls:** `[FY ▾]` `[Quarter ▾]` `[Branch ▾]` `[+ Schedule Audit]` `[Export ↓]`

---

## 4. Main Table — Audit Schedule

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Q1 Status | Badge: Scheduled · In Progress · Completed · Overdue | ✅ |
| Q1 Dates | Date range | ✅ |
| Q2 Status | Badge | ✅ |
| Q2 Dates | Date range | ✅ |
| Q3 Status | Badge | ✅ |
| Q3 Dates | Date range | ✅ |
| Q4 Status | Badge | ✅ |
| Q4 Dates | Date range | ✅ |
| Auditor Assigned | Text | ✅ |
| Open Findings | Count | ✅ |
| Actions | Schedule · View Report | — |

**Filters:** Branch · Quarter · Status
**Search:** Branch name
**Pagination:** 25 rows/page

---

## 5. Calendar View

Toggle: `[Table ↔ Calendar]`

Calendar view: Monthly calendar showing all scheduled audit periods across branches.
- Each audit shown as a coloured bar: Scheduled (blue) · In Progress (amber) · Completed (green) · Overdue (red)
- Hover: Branch name + auditor

---

## 6. Drawers

### 6.1 Drawer: `audit-schedule` — Schedule Audit
- **Trigger:** Schedule action or [+ Schedule Audit]
- **Width:** 640px

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | ✅ | |
| Quarter | Select | ✅ | Q1/Q2/Q3/Q4 |
| Audit Type | Select | ✅ | Quarterly · Surprise · Targeted |
| Start Date | Date | ✅ | ≥ Today |
| End Date | Date | ✅ | > Start date · ≤ Quarter end |
| Auditor(s) | Select (multi) | ✅ | From auditor list |
| Audit Scope | Multi-select | ✅ | Fee Collection · Procurement · Payroll · Assets · All |
| Checklist Template | Select | ✅ | Links to Page 42 |
| Pre-audit Notice to Branch | Toggle | — | Default: ON |
| Notice Days Before | Number | ❌ | Default: 5 |
| Notes | Textarea | ❌ | |

- [Cancel] [Schedule Audit]

### 6.2 Drawer: `audit-view` — View Scheduled Audit
- Audit details + status + checklist completion + findings list
- [Start Audit] → marks as In Progress
- [Complete Audit] → marks as Completed (requires checklist completion %)

---

## 7. Overdue Alert Panel

Panel below header showing all branches where a quarterly audit is overdue (not yet scheduled for the current quarter and past quarter midpoint).

| Branch | Quarter | Days Overdue | Last Audited |
|---|---|---|---|
| [Branch X] | Q2 | 15 | [Date] |

---

## 8. Charts

### 8.1 Audit Completion Progress (Progress bars — one per quarter)
- Q1: [Completed/Total] · Q2: [Progress bar] etc.

### 8.2 Branch Audit Frequency Heatmap
- Branches × Quarters grid showing completion status

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit scheduled | "Audit scheduled for [Branch] — Q[N] [Date range]." | Success | 4s |
| Notice sent | "Pre-audit notice sent to [Branch] Principal." | Info | 3s |
| Audit started | "Audit marked as In Progress for [Branch]." | Info | 3s |
| Audit completed | "Audit completed for [Branch]. [N] findings raised." | Success | 4s |
| Export | "Audit plan exported." | Info | 3s |

---

## 10. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No audits scheduled | "No audits scheduled" | "Schedule quarterly audits for all branches." | [+ Schedule Audit] |
| Quarter complete | "Quarter fully audited" | "All branches audited for Q[N]." | — |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Quarter switch | Table skeleton |
| Schedule drawer | Spinner + form |

---

## 12. Role-Based UI Visibility

| Element | Internal Auditor G1 | Finance Mgr G1 | CFO G1 |
|---|---|---|---|
| [+ Schedule Audit] | ✅ | ❌ | ❌ |
| [Start/Complete Audit] | ✅ | ❌ | ❌ |
| Calendar view | ✅ | ✅ | ✅ |
| Overdue panel | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/audit/planner/` | JWT (G1+) | Audit schedule |
| POST | `/api/v1/group/{id}/finance/audit/planner/` | JWT (G1) | Schedule audit |
| GET | `/api/v1/group/{id}/finance/audit/planner/{aid}/` | JWT (G1+) | Audit detail |
| PUT | `/api/v1/group/{id}/finance/audit/planner/{aid}/start/` | JWT (G1) | Start audit |
| PUT | `/api/v1/group/{id}/finance/audit/planner/{aid}/complete/` | JWT (G1) | Complete audit |
| GET | `/api/v1/group/{id}/finance/audit/planner/overdue/` | JWT (G1+) | Overdue list |
| GET | `/api/v1/group/{id}/finance/audit/planner/calendar/` | JWT (G1+) | Calendar data |
| GET | `/api/v1/group/{id}/finance/audit/planner/export/` | JWT (G1+) | Export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Quarter filter | `change` | GET `.../planner/?quarter=` | `#audit-table` | `innerHTML` |
| Calendar toggle | `click` | GET `.../planner/calendar/` | `#planner-view` | `innerHTML` |
| Schedule drawer | `click` | GET `.../planner/schedule-form/` | `#drawer-body` | `innerHTML` |
| Submit schedule | `submit` | POST `.../planner/` | `#drawer-body` | `innerHTML` |
| View audit | `click` | GET `.../planner/{id}/` | `#drawer-body` | `innerHTML` |
| Start audit | `click` | PUT `.../planner/{id}/start/` | `#audit-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
