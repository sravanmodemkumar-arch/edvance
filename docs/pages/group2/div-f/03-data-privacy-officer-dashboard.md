# 03 — Group Data Privacy Officer Dashboard

- **URL:** `/group/it/privacy/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Data Privacy Officer (Role 55, G1)

---

## 1. Purpose

The Group Data Privacy Officer (DPO) Dashboard provides a read-only oversight interface for monitoring DPDP Act 2023 compliance across all branches. The DPO is responsible for ensuring the group meets its obligations under India's Digital Personal Data Protection Act 2023 — covering lawful consent collection, data subject rights (DSR) processing, personal data breach reporting, Privacy Impact Assessments (PIA), and data residency requirements.

This page is intentionally read-only. The DPO's remit is to observe, audit, and flag — not to directly modify branch configurations. Any deficiency identified on this dashboard must be communicated to the Group IT Admin or IT Director via the platform's escalation mechanism (a "Flag for Action" button that creates an internal task), and those roles make the actual configuration changes.

The dashboard surfaces the most compliance-critical signals: whether branches are collecting valid consent at point of data collection, how quickly Data Subject Requests (DSR — right to access, right to erasure, right to correction) are being processed, whether any breach incidents are open beyond the mandatory 72-hour reporting window, and whether all Privacy Impact Assessments required before new data-processing activities are completed.

Regulatory context: Under DPDP Act 2023, a data breach that is not reported to the Data Protection Board within 72 hours of discovery carries significant penalties. The DPO must be alerted immediately when any breach incident exceeds this threshold on any branch.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Data Privacy Officer | G1 | Read-only; Flag for Action only | Primary role; no create/edit/delete |
| Group IT Director | G4 | Full read | Receives escalations from DPO |
| Group IT Admin | G4 | Full read | Actions DPO-raised flags |
| Group Cybersecurity Officer | G1 | Read-only (breach incidents only) | Collaborates on breach response |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Data Privacy Officer Dashboard
```

### 3.2 Page Header
- **Title:** `Group Data Privacy Officer Dashboard`
- **Subtitle:** `DPDP Act 2023 Compliance — All Branches · Last updated: [timestamp]`
- **Role Badge:** `Group Data Privacy Officer`
- **Right-side controls:** `Export Compliance Report (PDF)` · `Notification Bell`
- **Note:** No create/edit buttons visible anywhere on this page. All action buttons are "View" or "Flag for Action" only.

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Breach incident open > 72 hours (DPDP mandatory reporting window) | "CRITICAL: Data breach at [Branch Name] has been open for [N] hours. DPDP mandatory reporting window may be exceeded. Escalate immediately." | Red (non-dismissible) |
| Consent collection rate drops below 80% at any branch | "Consent collection rate at [Branch Name] has dropped to [N]%. This may indicate a consent flow misconfiguration." | Red |
| DSR pending > 30 days (DPDP statutory response window) | "[N] Data Subject Request(s) at [Branch Name] have exceeded the 30-day statutory response window." | Red |
| PIA overdue for a new data-processing activity | "[N] Privacy Impact Assessment(s) are overdue. New data processing activities cannot proceed without PIA completion." | Amber |

**Critical DPDP Notification Rules:**
- Breach incident open > 72h: Data Privacy Officer (in-app non-dismissible + email + WhatsApp) + IT Director (in-app + email) + Cybersecurity Officer (email)
- Consent collection < 80%: Data Privacy Officer (in-app) + IT Admin (email)
- DSR pending > 30 days: Data Privacy Officer (in-app + email) + IT Admin (email)
- PIA overdue: Data Privacy Officer (in-app amber) + IT Admin (email)

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Consent Collection Rate % | Group-wide average consent collection rate at point of data collection | Green ≥ 90%, Amber 80–89%, Red < 80% | Opens consent trend chart |
| Open Data Subject Requests | Total open DSR requests across all branches (access / erasure / correction) | Green = 0, Amber 1–5, Red > 5 | Filters table to branches with open DSR |
| Breach Incidents (Open) | Count of personal data breach incidents currently open | Green = 0, Amber = 1, Red ≥ 2 | Filters table to breached branches |
| PIAs Completed | Count of Privacy Impact Assessments completed (current AY) | Blue (informational, no colour threshold) | Opens PIA status detail |
| Data Residency Non-Compliant Items | Count of data items stored outside approved residency boundaries | Green = 0, Amber 1–3, Red > 3 | Opens residency detail |
| Privacy Policy Acknowledgement Rate | % of staff who have acknowledged the current privacy policy version | Green ≥ 95%, Amber 85–94%, Red < 85% | Filters table by policy acknowledgement |

---

## 5. Main Table — Branch DPDP Compliance Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text (link to branch DPDP detail view — read-only) | Yes | Yes (multi-select) |
| Consent Rate % | Percentage with colour bar | Yes | Yes (below threshold) |
| DSR Pending | Integer (count of open DSRs) | Yes | Yes (> 0) |
| Breach History (last 12m) | Integer (count of reported breaches in last 12 months) | Yes | Yes (> 0) |
| PIA Status | Badge: Complete / Pending / Overdue | No | Yes (status) |
| Residency Compliant | Badge: Yes (green) / No (red) / Partial (amber) | No | Yes (compliant/non-compliant) |
| Compliance Score | Score out of 100 with colour coding (Green ≥ 80, Amber 60–79, Red < 60) | Yes | Yes (below threshold) |
| Actions | `View Detail` · `Flag for Action` icon buttons only | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| PIA Status | Checkbox group | Complete / Pending / Overdue |
| Residency Compliant | Checkbox | Yes / No / Partial |
| Compliance Score Below | Numeric threshold input | Score value (e.g., 80) |
| Breach History | Checkbox | Any breach / No breach |
| Open DSR | Checkbox | Has open DSR / No open DSR |

### 5.2 Search
- Full-text: Branch name
- 300ms debounce, triggers HTMX GET with `?search=` query param

### 5.3 Pagination
- Server-side · 20 rows/page · Shows total count

---

## 6. Drawers

### 6.1 Drawer: `dpo-branch-detail` — Branch DPDP Detail (Read-Only)
- **Trigger:** Actions → View Detail on any row
- **Width:** 720px
- **Content:** Branch name, compliance score breakdown (how the score is calculated), consent collection timeline, DSR list (type, date received, status, age), breach history log (date, type, severity, reported to authorities Y/N, resolution date), PIA list (activity, status, completion date), residency compliance status, privacy policy version acknowledged by staff, DPO notes field (append-only — DPO can add notes but cannot edit portal config)
- **No edit controls** — all fields are display-only

**Audit:** DPO note appends are logged to DPO Audit Log with timestamp and DPO user ID. Notes cannot be edited or deleted once appended.

### 6.2 Drawer: `dpo-flag-action` — Flag for Action
- **Trigger:** Actions → Flag for Action button on any row
- **Width:** 480px
- **Fields:** Branch Name (pre-filled), Issue Category (dropdown: Consent / DSR / Breach / PIA / Residency / Policy), Issue Description (required, textarea, max 2000 characters, plain text), Urgency (High / Medium / Low), Notify (multi-select: IT Director, IT Admin), Submit Flag button
- **On submit:** Creates an internal action item in the IT Admin's queue and sends an email notification to selected recipients. Logged to DPO Audit Log.
- **Note:** This is the only "write" action available to the G1 DPO role

---

## 7. Charts

### 7.1 Consent Rates Trend — Last 12 Months (Line Chart)
- **X-axis:** Month labels (rolling 12 months)
- **Y-axis:** Consent collection rate %
- **Series:** Group average line (blue) + individual branch lines for branches below 85% (red dashed) — others greyed out
- **Threshold line:** 90% target shown as dashed green line
- **Data source:** GET `/api/v1/it/privacy/charts/consent-trend/`

### 7.2 DSR Resolution Time Distribution (Bar Chart)
- **X-axis:** Resolution time buckets: 0–7 days / 8–15 days / 16–30 days / 30+ days (overdue)
- **Y-axis:** Count of DSRs resolved in each bucket (last 12 months)
- **Colour:** Green for 0–7, Blue for 8–15, Amber for 16–30, Red for 30+ (overdue)
- **Annotation:** DPDP 30-day statutory limit shown as reference line
- **Data source:** GET `/api/v1/it/privacy/charts/dsr-resolution/`

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Flag submitted | "Action flag submitted. IT Admin and IT Director have been notified." | Success | 4s |
| Flag submission error | "Failed to submit flag. Please try again or contact IT Admin directly." | Error | 6s |
| Export triggered | "Compliance report is being generated. You will be notified when ready." | Info | 5s |
| DPO note saved | "Note appended to branch compliance record." | Success | 3s |
| Export error | Error: `Failed to generate compliance report. Please try again.` | Error | 6s |
| DPO note save error | Error: `Failed to save note. Please try again.` | Error | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches configured | "No Branch Data Available" | "No branch compliance data is available. Branch portals must be configured before DPDP monitoring begins." | — (DPO cannot create portals) |
| All branches fully compliant | "Full DPDP Compliance" | "All branches meet DPDP Act 2023 compliance thresholds. No flags are outstanding." | — |
| No open DSRs or breaches | "No Active Privacy Incidents" | "No open Data Subject Requests or breach incidents across any branch." | View Compliance History |
| Search returns no results | "No Branches Match" | "No branches match your search or filter criteria." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer (6 cards) + table skeleton (8 rows) + chart shimmer |
| Branch DPDP detail drawer open | Drawer-scoped spinner while detail data loads |
| Flag for Action drawer open | Drawer-scoped spinner |
| Flag submission | Submit button spinner + form fields disabled |
| Chart data fetch | Chart area shimmer with "Loading data…" label |
| Table filter/search | Table area overlay shimmer |

---

## 11. Role-Based UI Visibility

| Element | DPO (G1) | IT Director (G4) | IT Admin (G4) | Cybersecurity Officer (G1) |
|---|---|---|---|---|
| KPI Summary Bar | All 6 cards (read-only) | All 6 cards | All 6 cards | Breach Incidents card only |
| Branch DPDP Table | Visible + View/Flag actions | Visible + View/Flag actions | Visible + View/Flag actions | Breach History column only |
| + Create / Edit Buttons | Hidden — no edit buttons anywhere | Not on this page | Not on this page | Hidden |
| Flag for Action Drawer | Visible + submittable | Visible + submittable | Visible + submittable | Hidden |
| Branch Detail Drawer | Visible (read-only) | Visible (read-only) | Visible (read-only) | Breach history tab only |
| Alert Banners | All DPDP banners visible | All banners visible | All banners visible | Breach banners only |
| Charts | Both charts visible | Both charts visible | Both charts visible | Hidden |
| Export PDF | Visible | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/privacy/kpis/` | JWT (G1+) | Returns all 6 KPI card values |
| GET | `/api/v1/it/privacy/branches/` | JWT (G1+) | Paginated branch DPDP compliance table |
| GET | `/api/v1/it/privacy/branches/{branch_id}/` | JWT (G1+) | Single branch DPDP detail for drawer |
| POST | `/api/v1/it/privacy/flags/` | JWT (G1+) | Create a Flag for Action item |
| POST | `/api/v1/it/privacy/branches/{branch_id}/notes/` | JWT (G1) | Append a DPO note to a branch record |
| GET | `/api/v1/it/privacy/charts/consent-trend/` | JWT (G1+) | 12-month consent rate line chart data |
| GET | `/api/v1/it/privacy/charts/dsr-resolution/` | JWT (G1+) | DSR resolution time distribution bar chart data |
| GET | `/api/v1/it/privacy/export/` | JWT (G1+) | Triggers async PDF compliance report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/it/privacy/kpis/` | `#kpi-bar` | `innerHTML` |
| Load compliance table | `load` | GET `/api/v1/it/privacy/branches/` | `#compliance-table` | `innerHTML` |
| Open branch DPDP detail drawer | `click` on View Detail | GET `/api/v1/it/privacy/branches/{id}/` | `#detail-drawer` | `innerHTML` |
| Open Flag for Action drawer | `click` on Flag for Action | GET `/api/v1/it/privacy/flags/new/?branch={id}` | `#flag-drawer` | `innerHTML` |
| Submit Flag for Action | `click` on Submit Flag | POST `/api/v1/it/privacy/flags/` | `#flag-result` | `innerHTML` |
| Filter compliance table | `change` on filter controls | GET `/api/v1/it/privacy/branches/?pia_status=overdue` | `#compliance-table` | `innerHTML` |
| Search branches | `keyup[debounce:300ms]` on search | GET `/api/v1/it/privacy/branches/?search=` | `#compliance-table` | `innerHTML` |
| Paginate table | `click` on page button | GET `/api/v1/it/privacy/branches/?page=N` | `#compliance-table` | `innerHTML` |
| Save DPO note | `click` on Save Note | POST `/api/v1/it/privacy/branches/{id}/notes/` | `#note-result` | `innerHTML` |

---

**Audit Trail:** All write operations on this page are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications:** Critical alerts on this page trigger in-app notifications to the relevant role owners as specified in the alert banner conditions above.

*Page spec version: 1.0 · Last updated: 2026-03-21*
