# 04 — Group Cybersecurity Officer Dashboard

- **URL:** `/group/it/security/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Cybersecurity Officer (Role 56, G1)

---

## 1. Purpose

The Group Cybersecurity Officer Dashboard provides a read-only security oversight interface for monitoring device policy compliance, phishing simulation results, security training completion rates, incident severity trends, and access anomalies across all branches of the group.

Like the Data Privacy Officer, the Cybersecurity Officer operates at G1 access level — they observe, analyse, and escalate, but do not directly modify system configurations. Their primary tools are the Flag for Action mechanism (which routes to the IT Admin or IT Director) and the Comment/Escalation field on incidents. This separation of observation from administration is intentional: it ensures security decisions are auditable and go through the proper approval chain.

The dashboard is built for daily monitoring use. The Cybersecurity Officer begins each morning by reviewing the KPI bar for new incidents, checking if any branches have fallen below device compliance thresholds, reviewing the latest phishing simulation results, and scanning the incident log for severity changes overnight. The rolling 12-month incident trend chart provides the longer-term view needed for board-level cybersecurity reports.

The platform follows the principle that all students and staff are potential targets of phishing and social engineering. Phishing simulation click rates above 10% at any branch trigger an immediate amber alert and auto-flag for mandatory re-training. Rates above 20% trigger a red alert. Security training completion below 80% is similarly flagged because untrained users are the primary attack vector in edtech environments that handle sensitive student and parent data.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Cybersecurity Officer | G1 | Read-only; Flag/Escalate only | Primary role; no edit/create/delete |
| Group IT Director | G4 | Full read | Receives security escalations |
| Group IT Admin | G4 | Full read | Actions security-related config changes |
| Group Data Privacy Officer | G1 | Read-only (breach incidents only) | Collaborates on data breach response |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Cybersecurity Officer Dashboard
```

### 3.2 Page Header
- **Title:** `Group Cybersecurity Officer Dashboard`
- **Subtitle:** `Security Health — All Branches · Last updated: [timestamp]`
- **Role Badge:** `Group Cybersecurity Officer`
- **Right-side controls:** `Export Security Report (PDF)` · `Notification Bell`
- **Note:** No create/edit buttons visible anywhere. Only "View" and "Flag/Escalate" actions.

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Severity 1 (critical) security incident open | "CRITICAL: Severity 1 security incident at [Branch Name] is active. Immediate escalation required." | Red (non-dismissible) |
| Device compliance below 80% at any branch | "[Branch Name] device compliance has dropped to [N]%. Unmanaged devices may be active on the network." | Red |
| Phishing click rate > 20% at any branch | "Phishing simulation at [Branch Name] yielded a [N]% click rate. Mandatory re-training required." | Red |
| Security training completion below 70% | "Security training compliance at [Branch Name] is [N]%. Below acceptable threshold." | Amber |
| Overdue access reviews > 5 | "[N] access reviews are overdue across the group. Privilege creep risk increasing." | Amber |

**Security Alert Notification Rules:**
- Severity 1 incident open: Cybersecurity Officer (in-app non-dismissible + email + WhatsApp) + IT Director (in-app non-dismissible + email) + IT Admin (email)
- Device compliance < 80%: Cybersecurity Officer (in-app) + IT Admin (email)
- Phishing click rate > 20%: Cybersecurity Officer (in-app) + IT Director (email) + IT Admin (email)
- Training completion < 70%: Cybersecurity Officer (in-app amber) + IT Admin (email)

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Security Incidents (Open) | Total count of open security incidents across all branches (all severities) | Green = 0, Amber 1–3, Red ≥ 4 | Filters table to branches with open incidents |
| Devices Compliant % | % of registered devices that meet the group device policy (MDM enrolled, patched, encrypted) | Green ≥ 90%, Amber 80–89%, Red < 80% | Opens device compliance detail |
| Staff Security Training % | % of staff (across all branches) who have completed the current mandatory security training module | Green ≥ 90%, Amber 80–89%, Red < 80% | Opens training breakdown detail |
| Phishing Click Rate % | Group-wide average click rate from the most recent phishing simulation campaign | Green < 5%, Amber 5–15%, Red > 15% | Opens phishing results by branch |
| High Severity Vulnerabilities | Count of open Severity 1 + Severity 2 incidents | Green = 0, Amber 1, Red ≥ 2 | Filters table to high-severity branches |
| Overdue Access Reviews | Count of user access reviews that are past their scheduled review date | Green = 0, Amber 1–5, Red > 5 | Opens access review list |

---

## 5. Main Table — Branch Security Health

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text (link to branch security detail drawer) | Yes | Yes (multi-select) |
| Security Score (/100) | Numeric score with colour badge (Green ≥ 80, Amber 60–79, Red < 60) | Yes | Yes (below threshold) |
| Devices Compliant % | Percentage bar | Yes | Yes (below threshold) |
| Open Incidents | Integer (all severities) | Yes | Yes (> 0) |
| Last Phishing Sim Date | Date | Yes | Yes (date range) |
| Training Compliance % | Percentage bar | Yes | Yes (below threshold) |
| Last Security Audit Date | Date | Yes | Yes (date range, overdue) |
| Actions | `View Detail` · `Flag/Escalate` icon buttons only | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Security Score Below | Numeric threshold input | Score value (e.g., 70) |
| Open Incidents | Checkbox | Any open / None |
| Device Compliance Below | Numeric threshold input | Percentage value |
| Training Compliance Below | Numeric threshold input | Percentage value |
| Phishing Sim Date | Date range picker | Last run within N days |
| Last Security Audit | Date range picker | Overdue > N days |

### 5.2 Search
- Full-text: Branch name
- 300ms debounce, triggers HTMX GET with `?search=` query param

### 5.3 Pagination
- Server-side · 20 rows/page · Shows total count and current range

---

## 6. Drawers

### 6.1 Drawer: `security-branch-detail` — Branch Security Detail (Read-Only)
- **Trigger:** Actions → View Detail on any row
- **Width:** 720px
- **Content (vertical sections):**
  - Security score breakdown (how the 0–100 score is calculated: device compliance weight 30%, training weight 25%, incident history 25%, audit recency 20%)
  - Open incident list (Severity, type, date opened, status, assigned to in IT team)
  - Device compliance breakdown (compliant / non-compliant / unregistered counts)
  - Phishing simulation history (last 5 campaigns: date, send count, click count, click rate %)
  - Security training completion by department (Teaching / Non-Teaching / Admin / IT)
  - Last 3 security audit summaries (date, auditor, findings count, status)
  - Access review overdue list (user name, role, last reviewed date, days overdue)
- **No edit controls** — display-only

### 6.2 Drawer: `security-escalate` — Flag / Escalate
- **Trigger:** Actions → Flag/Escalate button
- **Width:** 480px
- **Fields:** Branch Name (pre-filled), Incident / Issue Type (dropdown: Device Non-Compliance / Phishing Risk / Training Gap / Open Incident / Access Review Overdue / Vulnerability / Other), Description (textarea, required), Severity Assessment (Required) (High / Medium / Low as assessed by Cybersecurity Officer), Notify (multi-select: IT Director, IT Admin, Data Privacy Officer — if breach-related), Submit Escalation button
- **On submit:** Creates an internal action item in IT Admin's queue with "Security" tag. Sends email notification to selected recipients. Logged to Security Audit Log.

---

## 7. Charts

### 7.1 Security Incident Trend — Rolling 12 Months (Line Chart)
- **X-axis:** Month labels (rolling 12 months)
- **Y-axis:** Incident count
- **Series:** Severity 1 (red line) / Severity 2 (orange line) / Severity 3 (blue line) — togglable via legend
- **Annotation:** Any month with a Severity 1 incident is marked with a red dot on the x-axis
- **Data source:** GET `/api/v1/it/security/charts/incident-trend/`

### 7.2 Phishing Click Rate per Branch (Bar Chart)
- **X-axis:** Branch names (all branches, sorted by click rate descending)
- **Y-axis:** Click rate %
- **Colour:** Green < 5% / Amber 5–15% / Red > 15%
- **Annotation:** Group average line shown across all bars
- **Data source:** GET `/api/v1/it/security/charts/phishing-rates/`

### 7.3 Security Training Completion by Role Type (Horizontal Bar Chart)
- **Y-axis:** Role categories: Teaching Staff / Non-Teaching Staff / Admin Staff / IT Staff / Leadership
- **X-axis:** Completion % (0–100%)
- **Colour:** Green ≥ 90% / Amber 70–89% / Red < 70%
- **Shows group-wide aggregate** — not per-branch
- **Data source:** GET `/api/v1/it/security/charts/training-by-role/`

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Escalation submitted | "Escalation submitted. IT Director and IT Admin have been notified." | Success | 4s |
| Escalation submission error | "Failed to submit escalation. Please try again." | Error | 6s |
| Export triggered | "Security report is being generated. You will be notified when ready." | Info | 5s |
| Export error | Error: `Failed to generate security report. Please try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches configured | "No Branch Security Data" | "No branch data is available for security monitoring. Branch portals must be configured by the IT Admin." | — |
| No open incidents | "No Active Security Incidents" | "No open security incidents across any branch. Continue monitoring." | View Incident History |
| All branches above security score threshold | "All Branches Secure" | "All branch security scores are above the 80-point threshold. No immediate action required." | View Training Dashboard |
| Search returns no results | "No Branches Match" | "No branches match your filter criteria. Try adjusting your filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer (6 cards) + table skeleton (8 rows) + chart shimmer (3 areas) |
| Branch security detail drawer open | Drawer-scoped spinner while full detail data loads |
| Escalation drawer open | Drawer-scoped spinner |
| Escalation submit | Submit button spinner + form fields disabled |
| Chart data fetch | Per-chart shimmer overlay with "Loading data…" label |
| Table filter/search | Table area overlay shimmer |

---

## 11. Role-Based UI Visibility

| Element | Cybersecurity Officer (G1) | IT Director (G4) | IT Admin (G4) | Data Privacy Officer (G1) |
|---|---|---|---|---|
| KPI Summary Bar | All 6 cards (read-only) | All 6 cards | All 6 cards | Security Incidents + High Severity only |
| Branch Security Table | Visible + View/Escalate | Visible + View/Escalate | Visible + View/Escalate | Open Incidents column only |
| + Create / Edit Buttons | Hidden — no edit buttons | Not on this page | Not on this page | Hidden |
| Escalation Drawer | Visible + submittable | Visible + submittable | Visible + submittable | Hidden |
| Branch Detail Drawer | Visible (read-only) | Visible (read-only) | Visible (read-only) | Incident list tab only |
| Alert Banners | All security banners | All banners | All banners | Breach-related banners only |
| Incident Trend Chart | Visible | Visible | Visible | Visible (severity 1 only) |
| Phishing Rate Chart | Visible | Visible | Visible | Hidden |
| Training by Role Chart | Visible | Visible | Visible | Hidden |
| Export PDF | Visible | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/security/kpis/` | JWT (G1+) | Returns all 6 KPI card values |
| GET | `/api/v1/it/security/branches/` | JWT (G1+) | Paginated branch security health table |
| GET | `/api/v1/it/security/branches/{branch_id}/` | JWT (G1+) | Single branch security detail for drawer |
| POST | `/api/v1/it/security/escalations/` | JWT (G1+) | Submit a security escalation/flag |
| GET | `/api/v1/it/security/charts/incident-trend/` | JWT (G1+) | 12-month incident trend line chart data |
| GET | `/api/v1/it/security/charts/phishing-rates/` | JWT (G1+) | Phishing click rate per branch bar chart data |
| GET | `/api/v1/it/security/charts/training-by-role/` | JWT (G1+) | Training completion by role horizontal bar data |
| GET | `/api/v1/it/security/export/` | JWT (G1+) | Triggers async PDF security report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/it/security/kpis/` | `#kpi-bar` | `innerHTML` |
| Load security table | `load` | GET `/api/v1/it/security/branches/` | `#security-table` | `innerHTML` |
| Open branch security detail drawer | `click` on View Detail | GET `/api/v1/it/security/branches/{id}/` | `#detail-drawer` | `innerHTML` |
| Open escalation drawer | `click` on Flag/Escalate | GET `/api/v1/it/security/escalations/new/?branch={id}` | `#escalate-drawer` | `innerHTML` |
| Submit escalation | `click` on Submit | POST `/api/v1/it/security/escalations/` | `#escalate-result` | `innerHTML` |
| Filter security table | `change` on filter controls | GET `/api/v1/it/security/branches/?score_below=70` | `#security-table` | `innerHTML` |
| Search branches | `keyup[debounce:300ms]` on search | GET `/api/v1/it/security/branches/?search=` | `#security-table` | `innerHTML` |
| Paginate table | `click` on page button | GET `/api/v1/it/security/branches/?page=N` | `#security-table` | `innerHTML` |
| Toggle chart series | `click` on legend item (JS event → HTMX programmatic) | GET `/api/v1/it/security/charts/incident-trend/?severity=1,2` | `#incident-chart` | `innerHTML` |

---

**Audit Trail:** All write operations on this page are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications:** Critical alerts on this page trigger in-app notifications to the relevant role owners as specified in the alert banner conditions above.

*Page spec version: 1.0 · Last updated: 2026-03-21*
