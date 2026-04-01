# 10 — Group POCSO Coordinator Dashboard

- **URL:** `/group/hr/pocso/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group POCSO Coordinator (Role 50, G3)

---

## 1. Purpose

The Group POCSO Coordinator Dashboard is the central command for compliance with the Protection of Children from Sexual Offences Act across all branches of the group. POCSO compliance is a legal obligation with serious institutional consequences for non-compliance: CBSE affiliation can be revoked, individual staff members can face prosecution, and the institution can be liable under the Act if it fails to maintain mandatory safeguards. The coordinator is the designated officer responsible for ensuring that every branch meets these obligations continuously, not just at the time of inspection.

The coordinator's work covers three primary domains. First, mandatory POCSO awareness training for all staff — not just teachers but every individual who interacts with or is physically present around students. This includes kitchen staff, drivers, security guards, and administrative personnel. Training must be delivered annually, attendance must be documented, and certificates must be issued. Second, incident management: any complaint alleging child abuse or inappropriate conduct must be formally registered, investigated by the Internal Complaints Committee, and reported to the appropriate authorities (police, NCPCR, CBSE) within the mandated timelines. Third, child safety audits: periodic inspections of each branch to assess the physical environment, staff conduct norms, complaint mechanisms, and CCTV coverage.

Incident management is the highest-priority function on this dashboard. Any active POCSO incident — from a complaint received to an investigation underway — triggers a red non-dismissible alert that is simultaneously shown on the HR Director's dashboard and sent to the Chairman via the platform's notification system. The coordinator must update the incident status at least every 48 hours during an active investigation. If an update is not logged within 48 hours, the platform escalates automatically.

The compliance status table provides a branch-by-branch view that the coordinator can share with the HR Director during board meetings or use to respond to regulatory inquiries. Branches that are "Non-Compliant" (training < 80%, no audit in past 6 months, or open incident without formal registration) are highlighted in red and require an intervention plan within 7 days.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group POCSO Coordinator | G3 | Full read + write on POCSO data | Primary role |
| Group HR Director | G3 | Full read + receives all incident escalations | Automatic escalation recipient |
| Group HR Manager | G3 | Read + incident registration initiation | Can log a complaint; Coordinator manages |
| Group Training & Development Manager | G2 | Read-only on training completion data | For training coordination |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → POCSO Compliance
```

### 3.2 Page Header
- **Title:** `Group POCSO Compliance Dashboard`
- **Subtitle:** `[N] Branches · [X]% Fully Compliant · [N] Active Incidents · AY [current academic year]`
- **Role Badge:** `Group POCSO Coordinator`
- **Right-side controls:** `+ Log Incident` · `Schedule Training` · `+ Log Audit` · `Export Compliance Report`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Active POCSO incident with no update > 48 hours | "🔴 CRITICAL: Active incident at [Branch] has not been updated for more than 48 hours. Immediate status update required. HR Director and Chairman have been notified." | Red (non-dismissible) |
| Any active POCSO incident (general) | "⚠ Active POCSO incident registered at [Branch]. Monitoring required. Click to view." | Red (non-dismissible) |
| Branch with no POCSO audit in > 6 months | "[N] branch(es) have not had a child safety audit in more than 6 months. Schedule immediately." | Amber |
| Training completion < 80% at any branch | "[N] branch(es) have POCSO training completion below 80%. Training must be completed immediately." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| POCSO Trained Staff % | Percentage of all staff with current valid POCSO training | Green ≥ 95%, Amber 80–95%, Red < 80% | Training completion list |
| Training Due This Month | Staff whose POCSO training is scheduled or due to be scheduled this month | Blue | Training calendar |
| Active Incidents | Currently open incident investigations | Red if > 0 (always red) | Incident list |
| Incidents Resolved (This AY) | Incidents formally closed in the current academic year | Blue | Resolved incident log |
| Audits Completed This Year | Child safety audits completed in current calendar year | Blue | Audit log |
| Branches Fully Compliant | Branches meeting all three compliance criteria (training ≥ 95%, audit ≤ 6 months, no open incidents) | Green (informational) | Compliance table |

---

## 5. Main Table — Branch POCSO Compliance Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text (link to branch detail) | Yes | Yes (multi-select) |
| Total Staff | Integer | Yes | No |
| POCSO Trained | Integer | Yes | No |
| Training Completion % | Percentage bar (Green ≥ 95%, Amber 80–95%, Red < 80%) | Yes | Yes (< threshold) |
| Last Training Date | Date | Yes | Yes (date range) |
| Incidents This AY | Integer | Yes | Yes (> 0) |
| Active Incidents | Integer (red if > 0) | Yes | Yes (> 0) |
| Last Audit Date | Date (red if > 6 months ago) | Yes | Yes (date range) |
| Compliance Status | Badge (Compliant / At Risk / Non-Compliant) | Yes | Yes |
| Actions | View / Schedule Training / Log Audit | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Compliance Status | Checkbox | Compliant / At Risk / Non-Compliant |
| Branch | Multi-select dropdown | All configured branches |
| Training Completion Below | Threshold input | Percentage value |
| Active Incidents | Toggle | Show branches with active incidents only |
| Last Audit Older Than | Dropdown | 3 months / 6 months / 1 year |

### 5.2 Search
- Full-text: Branch name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `pocso-incident-log` — Log New Incident
- **Trigger:** `+ Log Incident` button
- **Width:** 560px
- **Fields:**
  - Branch (required, dropdown)
  - Incident Date (required, date picker; cannot be in future)
  - Complaint Type (required, dropdown: Physical Abuse / Sexual Abuse / Emotional Abuse / Neglect / Cyberbullying / Other)
  - Complainant Category (required, radio: Student / Parent / Staff / Anonymous)
  - Brief Description (required, textarea, min 100 chars; encrypted at rest)
  - Accused Category (required, radio: Teaching Staff / Non-Teaching Staff / Student / External Party / Unknown)
  - ICC Registration Number (optional, text; filled after formal ICC meeting)
  - Immediate Action Taken (required, textarea)
  - Confidentiality Level (required, radio: Standard / High — High restricts access to Coordinator + Director + Chairman only)
- **Validation:** All required fields; description min 100 chars

### 6.2 Drawer: `pocso-branch-detail` — Branch Compliance Detail
- **Trigger:** Click on branch name
- **Width:** 720px
- Shows: Training completion breakdown by department/role category, list of untrained staff with names, training history (past sessions), audit history with findings, incident history (current AY), staff with expiring POCSO certificates

### 6.3 Drawer: `pocso-audit-log` — Log Child Safety Audit
- **Trigger:** `+ Log Audit` button or Actions → Log Audit
- **Width:** 560px
- **Fields:**
  - Branch (required, dropdown)
  - Audit Date (required, date picker)
  - Auditor Name(s) (required, text; can be internal or external)
  - Audit Areas Covered (checkboxes: Physical Safety / CCTV Coverage / Complaint Mechanism / Staff Conduct Training / Safe Zones / Emergency Protocols / ICC Notice Boards)
  - Overall Findings (required, textarea, min 80 chars)
  - Corrective Actions Required (optional, textarea)
  - Next Audit Scheduled Date (optional, date picker)
  - Audit Report Upload (optional, PDF, max 20MB)

### 6.4 Modal: Escalate Active Incident
- Confirmation: "This incident will be escalated to the Group HR Director, Group Chairman, and (if required) reported to NCPCR / local police. This action is logged and cannot be undone. Confirm escalation?"
- Buttons: Confirm Escalation · Cancel

---

## 7. Charts

### 7.1 POCSO Training Completion by Branch (Horizontal Bar Chart)
- Y-axis: Branch names
- X-axis: Completion % (0–100%)
- Colour-coded: Green ≥ 95%, Amber 80–95%, Red < 80%
- Sorted by completion ascending (worst at top)

### 7.2 Incident Timeline (Scatter / Timeline Chart)
- X-axis: Date
- Y-axis: Branch
- Each incident plotted as a dot; colour = status (Active = red, Resolved = green, Reported to Authority = blue)
- Helps the coordinator see incident clustering by time or branch

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Incident logged | "Incident registered. ICC and HR Director notified immediately." | Warning | 6s |
| Audit logged | "Child safety audit recorded for [Branch]." | Success | 4s |
| Incident status updated | "Incident status updated. Log recorded." | Success | 3s |
| Escalation triggered | "Incident escalated. HR Director and Chairman notified. External reporting initiated." | Warning | 8s |
| Training scheduled | "POCSO training session scheduled for [Branch] on [Date]." | Success | 4s |
| Export triggered | "Compliance report is being generated." | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No incidents ever logged | "No POCSO Incidents Recorded" | "No incidents have been registered in the system. Maintain vigilance and ensure complaint mechanisms are in place at every branch." | Log Audit |
| All branches compliant | "All Branches Fully Compliant" | "Every branch meets POCSO training, audit, and incident management requirements." | Export Report |
| No audits this year | "No Safety Audits This Year" | "No child safety audits have been logged in the current year. Schedule audits immediately." | + Log Audit |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full skeleton: 6 KPI shimmer + table skeleton (10 rows) |
| Branch detail drawer open | Drawer spinner; training list and audit history load progressively |
| Incident log form submit | Button spinner; escalation notification dispatch in progress |
| Charts load | Shimmer overlay on both chart panels |

---

## 11. Role-Based UI Visibility

| Element | POCSO Coordinator (G3) | HR Director (G3) | HR Manager (G3) | T&D Manager (G2) |
|---|---|---|---|---|
| KPI Summary Bar | Visible (all 6) | Visible (all 6) | Visible (training + incidents) | Visible (training only) |
| Branch Compliance Table | Visible + all actions | Visible (read + escalate) | Visible (read-only) | Visible (training columns only) |
| + Log Incident Button | Visible | Visible | Visible (can initiate; Coordinator manages) | Hidden |
| Incident Details (High Confidentiality) | Visible | Visible | Hidden | Hidden |
| + Log Audit Button | Visible | Hidden | Hidden | Hidden |
| Escalation Button | Visible | Visible | Hidden | Hidden |
| Incident Timeline Chart | Visible | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/pocso/kpis/` | JWT (G3) | All 6 KPI values |
| GET | `/api/v1/hr/pocso/branch-compliance/` | JWT (G3) | Paginated branch compliance table |
| GET | `/api/v1/hr/pocso/branch-compliance/{branch_id}/` | JWT (G3) | Branch detail with training and audit history |
| POST | `/api/v1/hr/pocso/incidents/` | JWT (G3) | Log a new POCSO incident |
| GET | `/api/v1/hr/pocso/incidents/` | JWT (G3) | List all incidents |
| PATCH | `/api/v1/hr/pocso/incidents/{id}/` | JWT (G3) | Update incident status |
| POST | `/api/v1/hr/pocso/incidents/{id}/escalate/` | JWT (G3) | Formal escalation to Director + Chairman |
| POST | `/api/v1/hr/pocso/audits/` | JWT (G3) | Log a child safety audit |
| GET | `/api/v1/hr/pocso/charts/training/` | JWT (G3) | Training completion bar chart data |
| GET | `/api/v1/hr/pocso/charts/incidents/` | JWT (G3) | Incident timeline chart data |
| GET | `/api/v1/hr/pocso/export/` | JWT (G3) | Async compliance report export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/hr/pocso/kpis/` | `#kpi-bar` | `innerHTML` |
| Load compliance table | `load` | GET `/api/v1/hr/pocso/branch-compliance/` | `#compliance-table` | `innerHTML` |
| Open branch detail drawer | `click` on branch name | GET `/api/v1/hr/pocso/branch-compliance/{id}/` | `#branch-drawer` | `innerHTML` |
| Submit incident log form | `click` on Log Incident | POST `/api/v1/hr/pocso/incidents/` | `#incident-result` | `innerHTML` |
| Submit audit log form | `click` on Save Audit | POST `/api/v1/hr/pocso/audits/` | `#compliance-table` | `innerHTML` |
| Filter by compliance status | `change` on status filter | GET `/api/v1/hr/pocso/branch-compliance/?status=...` | `#compliance-table` | `innerHTML` |
| Confirm escalation | `click` on Confirm Escalation | POST `/api/v1/hr/pocso/incidents/{id}/escalate/` | `#escalation-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
