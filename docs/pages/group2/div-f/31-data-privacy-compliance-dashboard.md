# 31 — Data Privacy Compliance Dashboard

- **URL:** `/group/it/privacy/compliance/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Data Privacy Officer (Role 55, G1) — Read-only command centre

---

## 1. Purpose

The Data Privacy Compliance Dashboard is the Group Data Privacy Officer's primary command centre for evidencing and monitoring DPDP Act 2023 compliance across every branch in the group. The DPDP Act (Digital Personal Data Protection Act 2023) places statutory obligations on the group as a Data Fiduciary: obtaining explicit consent before collecting personal data, responding to Data Subject Requests (DSRs) within 30 days, notifying the Data Protection Board of India within 72 hours of a significant data breach, completing Privacy Impact Assessments for new data processing activities, and ensuring personal data of Indian residents is stored within India's borders.

This dashboard aggregates compliance signals from five domains — consent management, DSR handling, breach incident records, PIA completion, and data residency — into a single view with a per-branch compliance score. The Data Privacy Officer uses this page daily to monitor whether any branch has fallen behind on legal obligations, whether any breach requires urgent notification filing, and whether the group as a whole has improving or deteriorating compliance trends over time.

The Data Privacy Officer holds a G1 (read-only) role for a deliberate reason: the DPO must be independent of the day-to-day operations they oversee. They cannot create, modify, or delete records — only review them. This ensures the DPO's assessment of compliance is based on what actually exists in the system, not what they have written themselves. The IT Admin (G4) handles operational data entry; the DPO provides the governance oversight and escalates to IT Director or Group Chairman when legal obligations are at risk.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Data Privacy Officer | G1 | Read-only — all sections visible | Sole intended user; all actions are view-only |
| Group IT Admin | G4 | Read-only | Can view for operational awareness; manages data in other pages |
| Group IT Director | G4 | Read-only | Senior oversight |
| All other Division F roles | — | Hidden | No access |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Data Privacy → Compliance Dashboard
```

### 3.2 Page Header
- **Title:** `DPDP Compliance Dashboard`
- **Subtitle:** `DPDP Act 2023 · [N] Branches · Last refreshed: [timestamp]`
- **Role Badge:** `Group Data Privacy Officer`
- **Right-side controls:** `Export Compliance Report` (downloads full PDF report from Cloudflare R2 or generates on-demand)

### 3.3 Alert Banner (conditional — non-dismissible for legal obligations)

| Condition | Banner | Severity |
|---|---|---|
| Open breach incident >4h without 72h notification filed | "LEGAL REQUIREMENT: Breach #[N] at [Branch] has been open for [N] hours without a 72h notification filed. DPDP Act requires Board notification within 72h of discovery." | Red (non-dismissible) |
| DSR overdue >30 days | "[N] Data Subject Request(s) are overdue beyond the 30-day resolution limit. DPDP Act breach — immediate escalation required." | Red (non-dismissible) |
| Breach notification filed but response outstanding >72h | "72h notification filed for breach #[N] but Data Protection Board response is outstanding. Monitor for Board directions." | Amber |
| PIA pending review >30 days without action | "[N] Privacy Impact Assessment(s) have been waiting for review for more than 30 days. Action required." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Overall Consent Rate % | Weighted average consent rate across all branches | Green ≥95%, Amber 85–94%, Red <85% | Link to Consent Management page |
| Open DSRs | Count of open (unresolved) Data Subject Requests | Red if >0, Green if 0 | Link to DSR Manager |
| Open Breach Incidents | Count of breach incidents with status Open or Investigating | Red if >0, Green if 0 | Link to Breach Register |
| PIAs Pending | Count of Privacy Impact Assessments in Draft or Submitted or Under Review | Amber if >0 | Link to PIA page |
| Data Residency Non-Compliant | Count of data assets flagged as Non-Compliant for Indian residency | Red if >0, Green if 0 | Link to Data Residency Tracker |
| Privacy Policy Acceptance Rate % | % of active branch principals who have acknowledged latest privacy policy version | Green ≥90%, Amber 70–89%, Red <70% | Link to Privacy Policy Manager |

---

## 5. Main Table — Branch DPDP Compliance Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text (link to View Report drawer) | Yes | Yes (text search) |
| Consent Rate % | Percentage — colour coded | Yes | No |
| DSRs Open | Number — red if >0 | Yes | No |
| DSRs Overdue (>30d) | Number — red if >0 | Yes | No |
| Breach Incidents (Open) | Number — red if >0 | Yes | No |
| PIA Status | Text ("All Done" / "[N] Pending") — amber if pending | Yes | No |
| Residency Compliant | Badge (Yes / No / Partial) — red if No | Yes | Yes (Yes/No/Partial) |
| Compliance Score (/100) | Number — green ≥80, amber 60–79, red <60 | Yes | No |
| Last Review Date | Date (relative) | Yes | Yes (date range) |
| Actions | View Report | No | No |

### 5.1 Compliance Score Calculation
The compliance score (/100) is computed server-side by a weighted formula:
- Consent Rate (25 points)
- DSR timeliness — no overdue DSRs (20 points)
- No open breach incidents (25 points)
- PIA completion for all active data processing activities (15 points)
- Data residency compliance (15 points)

Score is stored in a compliance_score_snapshot PostgreSQL table, updated nightly.

### 5.2 Filters
- Residency Compliant: Yes / No / Partial
- Compliance Score range: select threshold (e.g., "<60" shows non-compliant branches)
- Last Review Date: date range

### 5.3 Search
- Branch name; 300ms debounce

### 5.4 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `branch-compliance-report` — View Branch Compliance Report
- **Trigger:** Actions → View Report
- **Width:** 720px
- **Read-only full compliance report for the selected branch:**
  - Branch details: name, location, principal
  - Compliance score breakdown (by category with sub-scores)
  - Consent summary: total records, active %, withdrawn %, trend last 6 months
  - DSR summary: open count, overdue count, avg resolution time
  - Breach incidents: list of all incidents (open and resolved), notification status
  - PIA list: all PIAs for this branch's activities, approval status
  - Data residency summary: compliant vs non-compliant assets for this branch
  - Last audit date and auditor name
  - Notes section (DPO can add text notes — this is the only write action available to G1)

**Note field:** The DPO can add free-text review notes to a branch compliance report (stored in compliance_review_note table). This is explicitly designed as an audit trail mechanism — the DPO's written observation is part of the compliance record.

---

## 7. Charts

### 7.1 Consent Rate Trend — 12 Months (Line Chart)
- X-axis: Months (last 12)
- Y-axis: Consent rate % (group average)
- Reference line at 95% (target)
- Shows whether consent capture is improving or declining

### 7.2 DSR Resolution Time Average — Per Month (Bar Chart)
- X-axis: Months (last 12)
- Y-axis: Average resolution time in days
- Reference line at 30 (legal limit)
- Colour: Green bars below 20d, amber 20–28d, red 28–30d, very red >30d

### 7.3 Compliance Score Distribution Across Branches (Histogram)
- X-axis: Score ranges (0–19, 20–39, 40–59, 60–79, 80–100)
- Y-axis: Number of branches in each range
- Quick visual of how many branches are at risk
- Positioned beside the DSR chart

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Report export triggered | "Compliance report export is being prepared. Download will begin shortly." | Info | 4s |
| Review note saved | "Compliance review note saved for [Branch Name]." | Success | 3s |
| Report export failed | Error: `Failed to generate compliance report. Please try again.` | Error | 5s |
| Review note save failed | Error: `Failed to save note for [Branch Name]. Please try again.` | Error | 4s |

---

**Audit Trail:** DPO notes saved via this dashboard are logged to the IT Audit Log with DPO user ID, timestamp, and branch identifier. Export actions are also logged.

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches | "No Branches Configured" | "No branch data is available for compliance monitoring." | — |
| All branches fully compliant | "All Branches Compliant" | "Every branch has a compliance score ≥80 with no open DSRs, breaches, or residency issues." | — |
| No results for filter | "No Matching Branches" | "No branches match the selected filters." | Clear Filters |
| Charts no data | "Insufficient Data" | "Not enough historical data to display this chart. Data will appear as records accumulate." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 6 KPI shimmer cards + table skeleton (10 rows) + 3 chart area shimmers |
| Filter / search | Table skeleton shimmer |
| View Report drawer | Drawer spinner; report sections load progressively (consent → DSR → breaches → PIA → residency) |
| Export report | Button spinner: "Generating report…" (can take 10–30s for large groups) |
| Chart load | Chart area shimmer with placeholder axes |

---

## 11. Role-Based UI Visibility

| Element | Data Privacy Officer (G1) | IT Admin (G4) | IT Director (G4) |
|---|---|---|---|
| Full compliance dashboard | Visible | Visible | Visible |
| View Report drawer | Visible | Visible | Visible |
| DPO Review Notes field | Visible + editable | Visible (read-only) | Visible (read-only) |
| Export Compliance Report | Visible | Visible | Visible |
| + Add / Edit / Delete actions | None (G1 = read-only) | None (read-only on this page) | None (read-only) |
| Alert banners | Visible | Visible | Visible |
| Charts | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/privacy/compliance/` | JWT (G1+) | Paginated branch compliance status table |
| GET | `/api/v1/it/privacy/compliance/kpis/` | JWT (G1+) | KPI card values |
| GET | `/api/v1/it/privacy/compliance/{branch_id}/report/` | JWT (G1+) | Full branch compliance report |
| POST | `/api/v1/it/privacy/compliance/{branch_id}/note/` | JWT (G1 — DPO only) | Save DPO review note for branch |
| GET | `/api/v1/it/privacy/compliance/charts/consent-trend/` | JWT (G1+) | 12-month consent rate trend |
| GET | `/api/v1/it/privacy/compliance/charts/dsr-resolution/` | JWT (G1+) | DSR avg resolution time per month |
| GET | `/api/v1/it/privacy/compliance/charts/score-distribution/` | JWT (G1+) | Compliance score histogram data |
| GET | `/api/v1/it/privacy/compliance/export/` | JWT (G1+) | Generate and download full compliance report (PDF via Cloudflare R2) |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/privacy/compliance/kpis/` | `#kpi-bar` | `innerHTML` |
| Load compliance table | `load` | GET `/api/v1/it/privacy/compliance/` | `#compliance-table` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/privacy/compliance/?residency=...` | `#compliance-table` | `innerHTML` |
| Search branches | `input` (300ms debounce) | GET `/api/v1/it/privacy/compliance/?q=...` | `#compliance-table` | `innerHTML` |
| Open View Report drawer | `click` on View Report | GET `/api/v1/it/privacy/compliance/{branch_id}/report/` | `#compliance-drawer` | `innerHTML` |
| Save DPO review note | `click` on Save Note | POST `/api/v1/it/privacy/compliance/{id}/note/` | `#note-save-result` | `innerHTML` |
| Load consent trend chart | `load` | GET `/api/v1/it/privacy/compliance/charts/consent-trend/` | `#consent-chart` | `innerHTML` |
| Load DSR resolution chart | `load` | GET `/api/v1/it/privacy/compliance/charts/dsr-resolution/` | `#dsr-chart` | `innerHTML` |
| Load score distribution | `load` | GET `/api/v1/it/privacy/compliance/charts/score-distribution/` | `#score-chart` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/privacy/compliance/?page=N` | `#compliance-table` | `innerHTML` |
| Export report | `click` on Export | GET `/api/v1/it/privacy/compliance/export/` | `#export-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
