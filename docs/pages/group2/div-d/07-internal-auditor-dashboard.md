# 07 — Group Internal Auditor Dashboard

- **URL:** `/group/finance/audit/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Internal Auditor (Role 36, G1)

---

## 1. Purpose

The Internal Auditor Dashboard is the central hub for planning, executing, and tracking quarterly financial audits across all branches. The Group Internal Auditor (G1) conducts scheduled audits — at least once per quarter per branch — and raises findings when financial irregularities, compliance gaps, or internal control failures are detected.

This dashboard shows which branches are due for audit, which audits are in progress, which findings are open, and the overall irregularity trend. The auditor does not post transactions; instead, this read-write role drives the audit lifecycle: planning → fieldwork → findings → management response → closure.

Critical for: CBSE affiliation reviews, statutory auditor coordination, and maintaining group-level financial discipline across branches.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Internal Auditor | G1 | Read + write (audit lifecycle) | Primary owner |
| Group CFO | G1 | Read — all sections | |
| Group Finance Manager | G1 | Read — all sections | Sign-off authority on findings |
| Group Chairman | G5 | Read — audit summary only | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Internal Audit Dashboard
```

### 3.2 Page Header
- **Title:** `Internal Audit Dashboard`
- **Subtitle:** `FY [Year] · Q[N] · [N] Audits Completed · [N] Findings Open`
- **Role Badge:** `Group Internal Auditor`
- **Right-side controls:** `[FY ▾]` `[Quarter ▾]` `[+ Schedule Audit]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Branch not audited in > 90 days | "[N] branch(es) overdue for quarterly audit." | Red |
| High-severity finding open > 30 days | "[N] high-severity finding(s) without management response for 30+ days." | Red |
| Audit scheduled within next 7 days | "[N] branch audit(s) starting within 7 days. Confirm checklist ready." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Audits Completed (Quarter) | Count | Green = all branches | → Page 39 |
| Audits In Progress | Count | Informational | → Page 39 |
| Audits Overdue | Count | Red if > 0 | → Page 39 |
| Open Findings | Count | Red if > 0 | → Page 40 |
| High-Severity Findings Open | Count | Red if > 0 | → Page 40 |
| Avg Audit Closure Days | Days | Green < 30 · Red > 45 | → Page 43 |

---

## 5. Section 5.1 — Branch Audit Status Table

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Last Audit Date | Date | ✅ |
| Next Due | Date | ✅ |
| Q1 Status | Badge: Done · In Progress · Pending · Overdue | ✅ |
| Q2 Status | Badge | ✅ |
| Q3 Status | Badge | ✅ |
| Q4 Status | Badge | ✅ |
| Open Findings | Count (link) | ✅ |
| Actions | Schedule · View Report | — |

**Filters:** Branch · Quarter · Status
**Search:** Branch name
**Pagination:** 20 rows/page

---

## 5.2 Section 5.2 — Open Findings Summary

| Column | Type | Sortable |
|---|---|---|
| Finding ID | Text | ✅ |
| Branch | Text | ✅ |
| Category | Badge: Financial · Compliance · Operational · IT | ✅ |
| Severity | Badge: Critical · High · Medium · Low | ✅ |
| Raised Date | Date | ✅ |
| Days Open | Number (red if > 30) | ✅ |
| Status | Badge: Open · Response Received · Closed | ✅ |
| Actions | View · Close | — |

**[View All Findings →]** links to Page 40.

---

## 5.3 Section 5.3 — Irregularity Trend

Mini chart: irregularities raised per quarter for the FY, by severity.

**[View Irregularity Detection →]** links to Page 41.

---

## 6. Charts

### 6.1 Audit Completion by Quarter (Grouped Bar)
- **Groups:** Q1 · Q2 · Q3 · Q4
- **Series:** Completed · In Progress · Pending
- **Export:** PNG

### 6.2 Finding Severity Distribution (Donut)
- **Segments:** Critical (red) · High (orange) · Medium (amber) · Low (green)

### 6.3 Avg Closure Days by Branch (Bar)
- **Sort:** Desc (slowest closure first)

---

## 7. Drawers

### 7.1 Drawer: `audit-schedule` — Schedule New Audit
- **Trigger:** [+ Schedule Audit]
- **Width:** 580px

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | ✅ | |
| Audit Type | Select | ✅ | Quarterly · Special · Surprise |
| Quarter | Select | ✅ | Q1/Q2/Q3/Q4 |
| Start Date | Date | ✅ | ≥ Today |
| End Date | Date | ✅ | > Start |
| Audit Team | Text | ✅ | Auditor names |
| Checklist Template | Select | ✅ | Links to Page 42 |
| Pre-Audit Notice to Branch | Toggle | ❌ | Default: ON |

- [Cancel] [Schedule Audit]

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit scheduled | "Audit scheduled for [Branch] from [Date] to [Date]." | Success | 4s |
| Finding closed | "Finding [ID] closed for [Branch]." | Success | 3s |
| Export | "Audit report exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No audits scheduled | "No audits scheduled" | "Schedule a branch audit to begin." | [+ Schedule Audit] |
| No open findings | "No open findings" | "All audit findings are closed." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + 2 table skeletons + chart skeletons |
| Schedule drawer | Spinner + skeleton form |
| Quarter switch | Table skeleton |

---

## 11. Role-Based UI Visibility

| Element | Internal Auditor G1 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [+ Schedule Audit] | ✅ | ❌ | ❌ |
| [Close Finding] | ✅ | ❌ | ✅ (sign-off) |
| View all sections | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/audit/kpis/` | JWT (G1+) | KPI cards |
| GET | `/api/v1/group/{id}/finance/audit/branch-status/` | JWT (G1+) | Branch audit status |
| GET | `/api/v1/group/{id}/finance/audit/findings/?status=open` | JWT (G1+) | Open findings |
| POST | `/api/v1/group/{id}/finance/audit/schedule/` | JWT (G1) | Schedule audit |
| PUT | `/api/v1/group/{id}/finance/audit/findings/{fid}/close/` | JWT (G1) | Close finding |
| GET | `/api/v1/group/{id}/finance/audit/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Quarter switch | `change` | GET `.../audit/branch-status/?q=` | `#audit-table` | `innerHTML` |
| Schedule drawer | `click` | GET `.../audit/schedule/form/` | `#drawer-body` | `innerHTML` |
| Submit schedule | `submit` | POST `.../audit/schedule/` | `#drawer-body` | `innerHTML` |
| Close finding | `click` | PUT `.../findings/{id}/close/` | `#finding-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
