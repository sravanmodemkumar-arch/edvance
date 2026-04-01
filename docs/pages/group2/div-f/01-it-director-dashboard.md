# 01 — Group IT Director Dashboard

- **URL:** `/group/it/director/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group IT Director (Role 53, G4)

---

## 1. Purpose

The Group IT Director Dashboard is the command centre for the senior-most technology authority in the group. It provides a unified, real-time view of every branch portal's operational health — covering integration status, support ticket SLA performance, data privacy and cybersecurity compliance KPIs, and pending IT policy approvals — across all 50 branches simultaneously.

This dashboard eliminates the need for the IT Director to poll individual branch administrators or rely on manually collated reports. Systemic risk surfaces immediately: a branch portal offline for more than an hour, a widespread integration failure, or an unresolved DPDP breach are each escalated to the Director's attention via non-dismissible alert banners before they can silently compound into larger incidents.

The page also serves as an executive approval gateway. IT policy changes initiated by the Group IT Admin — feature rollouts, role-permission changes, notification config changes — require Director sign-off before they propagate to branches. Pending approvals older than 48 hours are highlighted amber; those older than 72 hours are flagged red. The Director is expected to use this page as their daily morning review screen and their primary incident-monitoring interface.

From a technology-strategy perspective, the feature adoption rate KPI allows the Director to measure whether investments in new EduForge capabilities are actually reaching branch staff and students, enabling ROI conversations with group leadership. Integration failure counts give early warning of third-party API degradation before branch operations are impacted.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Director | G4 | Full read + approve/reject IT policies | Primary role; sees all 50 branches |
| Group IT Admin | G4 | Full read | Cannot action Director-level policy approvals |
| Group Cybersecurity Officer | G1 | Read-only (security KPIs only) | Cannot view portal config or integration details |
| Group Data Privacy Officer | G1 | Read-only (DPDP KPI only) | Cannot view portal config or integration details |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 — dashboard for IT Director only |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 — dashboard for IT Director only |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → IT Director Dashboard
```

### 3.2 Page Header
- **Title:** `Group IT Director Dashboard`
- **Subtitle:** `Technology Health — All Branches · [Active Portals] / [Total Portals] active · AY [current academic year]`
- **Role Badge:** `Group IT Director`
- **Right-side controls:** `Export Report (PDF)` · `Pending IT Approvals ([count])` · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any branch portal offline > 1 hour | "[Branch Name] portal has been offline for [N] hours. Immediate investigation required." | Red (non-dismissible) |
| Integration failure affecting > 5 branches | "Integration failure: [Integration Name] is affecting [N] branches. View incident." | Red (non-dismissible) |
| DPDP breach unresolved > 4 hours | "DPDP breach incident at [Branch Name] has been open for [N] hours without resolution." | Red (non-dismissible) |
| Cybersecurity incident Severity 1 | "Severity 1 security incident reported at [Branch Name]. IT Director escalation required." | Red (non-dismissible) |
| Pending IT approvals > 72 hours old | "[N] IT policy approval(s) have been pending for more than 72 hours. Review now." | Amber |

**Alert Notification Rules:**
- Portal offline > 1 hour: IT Director (in-app non-dismissible + email)
- Integration failure > 5 branches: Integration Manager + IT Director (in-app + email)
- DPDP breach countdown active: Data Privacy Officer + IT Director (in-app non-dismissible + email)
- Severity 1 security incident: Cybersecurity Officer + IT Director (in-app non-dismissible + email)
- Pending approvals > 72h: IT Director (in-app amber + email)
- Policy approved: IT Admin notified via in-app notification

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Branch Portals | Active portal count / Total portal count (e.g., 48 / 50) | Green if all active, Amber if < 95%, Red if < 90% | Links to Branch Portal Manager (`/group/it/portals/`) |
| Open Support Tickets | Total open tickets across all branches | Green < 20, Amber 20–50, Red > 50 | Links to IT Support queue |
| Integration Failures (24h) | Count of failed integration health checks in last 24 hours | Green = 0, Amber 1–5, Red > 5 | Links to Integration Manager Dashboard |
| DPDP Compliance Score | Group-wide average DPDP compliance percentage across branches | Green ≥ 90%, Amber 75–89%, Red < 75% | Links to Data Privacy Officer Dashboard |
| Cybersecurity Alerts | Count of open security alerts (all severities) | Green = 0, Amber 1–3, Red > 3 | Links to Cybersecurity Officer Dashboard |
| Feature Adoption Rate | % of enabled features actively used in the last 30 days | Green ≥ 70%, Amber 50–69%, Red < 50% | Links to Feature Toggle Manager |

---

## 5. Main Table — Branch IT Health

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text (link to branch IT detail drawer) | Yes | Yes (multi-select) |
| Portal Status | Badge: Active (green) / Degraded (amber) / Inactive (red) | Yes | Yes (status checkbox) |
| Custom Domain | Badge: Yes (green) / No (grey) | No | Yes (Yes/No) |
| SSO Enabled | Badge: Yes (green) / No (grey) | No | Yes (Yes/No) |
| Feature Toggles Active | Integer (count of enabled features) | Yes | No |
| Last Config Change | Relative datetime (e.g., "3 days ago") | Yes | Yes (date range) |
| Support Tickets Open | Integer | Yes | Yes (> N) |
| Security Alerts | Integer | Yes | Yes (> 0) |
| Actions | Icon buttons | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Portal Status | Checkbox group | Active / Degraded / Inactive |
| Custom Domain | Checkbox | Yes / No |
| SSO Enabled | Checkbox | Yes / No |
| Support Tickets Above | Numeric threshold input | Integer (e.g., > 5) |
| Security Alerts | Checkbox | Any Open / None |
| Last Config Change | Date range picker | From / To |

### 5.2 Search
- Full-text: Branch name
- 300ms debounce, triggers HTMX GET with `?search=` query param

### 5.3 Pagination
- Server-side · 20 rows/page · Shows total record count and current page indicator

---

## 6. Drawers

### 6.1 Drawer: `it-director-branch-detail` — View Branch IT Detail
- **Trigger:** Click branch name or Actions → View
- **Width:** 720px
- **Tabs within drawer:**
  - **Portal Config:** Portal URL, status, custom domain, SSL expiry, feature toggle count, last config change date, who made the last change
  - **Integrations:** List of active integrations for this branch (SSO, API, Webhooks), last health check per integration, error count in 24h
  - **Support:** Open ticket count, tickets by priority (P1/P2/P3), oldest open ticket age, last resolved ticket date
  - **Security:** Security score, open incidents, last phishing simulation date, training compliance %, last security audit date

### 6.2 Drawer: `it-director-policy-approval` — Approve IT Policy
- **Trigger:** Click Pending IT Approvals count or Actions → Approve from notification
- **Width:** 560px
- **Fields shown:** Policy change title, change description, proposed by (Group IT Admin), date submitted, branches affected (list), risk level (Low/Medium/High auto-assessed), IT Director notes (textarea, required) (max 1000 characters, plain text)
- **Action buttons:** Approve Policy · Reject · Request Clarification
- **Note:** Approval is logged to IT Audit Log with Director user ID and timestamp

**Audit:** All policy approvals, rejections, and clarification requests are logged to IT Audit Log with IT Director user ID and timestamp.

### 6.3 Drawer: `it-director-incident-detail` — Incident Detail
- **Trigger:** Click on security alert or DPDP breach count
- **Width:** 560px
- **Shows:** Incident type, affected branch, severity, opened at, description, escalation trail, current status, assigned to, resolution notes field (read-only for Director at G4 — delegates resolution to IT Admin/Cybersecurity Officer)

**Audit:** Alert acknowledgments are logged to IT Audit Log with IT Director user ID and timestamp.

---

## 7. Charts

### 7.1 Integration Health Over Time (Line Chart)
- **X-axis:** Last 30 days (daily)
- **Y-axis:** % of integrations passing health check
- **Series:** Group-wide average line (blue) + line per integration type (SSO, API, Webhooks) — toggleable via legend
- **Threshold line:** 95% SLA target shown as dashed green line
- **Data source:** GET `/api/v1/it/director/charts/integration-health/`

### 7.2 Support Ticket Trend (Bar Chart)
- **X-axis:** Last 12 weeks (weekly)
- **Y-axis:** Ticket count
- **Series:** Opened (blue bar) vs. Resolved (green bar) per week — grouped bars
- **Annotation:** Weeks where open > resolved are highlighted with amber bar border
- **Data source:** GET `/api/v1/it/director/charts/ticket-trend/`

### 7.3 Branch Portal Status Distribution (Donut Chart)
- **Segments:** Active (green) / Degraded (amber) / Inactive (red)
- **Centre label:** Total portal count
- **Legend:** Count and percentage per segment
- **Click interaction:** Clicking a segment filters the main table to that status
- **Data source:** GET `/api/v1/it/director/charts/portal-status/`

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| IT Policy approved | "Policy approved and applied to [N] branch(es)." | Success | 4s |
| IT Policy rejected | "Policy change rejected. IT Admin has been notified." | Info | 4s |
| Clarification requested | "Clarification request sent to IT Admin." | Info | 4s |
| Export triggered | "Report is being generated. You will be notified when ready." | Info | 5s |
| Approval submission error | "Failed to process approval. Please try again." | Error | 6s |
| Alert acknowledged | "Incident acknowledged. Action logged against your profile." | Warning | 5s |
| IT Policy rejected (error) | Error: `Failed to reject policy. Please try again.` | Error | 5s |
| Clarification request (error) | Error: `Failed to send clarification request. Please try again.` | Error | 5s |
| Alert acknowledgment failed | Error: `Failed to acknowledge alert. Please try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches configured | "No Branch Portals Found" | "No branch portal data is available. Configure branch portals to begin IT oversight." | Configure Portals |
| All portals healthy, no alerts | "All Systems Operational" | "Every branch portal is active and all integrations are healthy. No action required." | View Full Portal List |
| No pending approvals | "No Pending Approvals" | "You are up to date. All IT policy change requests have been actioned." | — |
| No support tickets open | "No Open Tickets" | "All support tickets across branches have been resolved or are unassigned." | — |
| Filter/search returns no results | No Branches Match | No branch portals match your filter or search criteria. | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer (6 cards) + table skeleton (8 rows) + chart area shimmer |
| Branch IT detail drawer open | Drawer-scoped spinner centred in panel; tabs load independently with inline spinners |
| Approval submission | Button spinner + both action buttons disabled until response |
| Chart data fetch | Chart area shimmer overlay with "Loading data…" label centred |
| Table filter/search apply | Table area overlay shimmer while new results load |

---

## 11. Role-Based UI Visibility

| Element | IT Director (G4) | IT Admin (G4) | Cybersecurity Officer (G1) | Data Privacy Officer (G1) |
|---|---|---|---|---|
| KPI Summary Bar | Visible (all 6 cards) | Visible (all 6 cards) | Security Alerts card only | DPDP Compliance card only |
| Branch IT Health Table | Visible + View action | Visible (no approval action) | Hidden | Hidden |
| Policy Approval Drawer | Visible + Actionable | Visible (read-only) | Hidden | Hidden |
| Incident Detail Drawer | Visible (read-only) | Visible + editable | Security incidents only | DPDP incidents only |
| Export PDF Button | Visible | Visible | Hidden | Hidden |
| Alert Banners | All banners visible + dismissible post-action | All banners visible | Security banners only | DPDP banners only |
| Charts | All 3 charts visible | All 3 charts visible | Hidden | Hidden |
| Pending Approvals Count | Visible in header | Visible (own submissions only) | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/director/kpis/` | JWT (G4) | Returns all 6 KPI card values |
| GET | `/api/v1/it/director/branch-health/` | JWT (G4) | Paginated branch IT health table |
| GET | `/api/v1/it/director/branch-health/{branch_id}/` | JWT (G4) | Single branch IT detail for drawer |
| GET | `/api/v1/it/director/pending-approvals/` | JWT (G4) | List of pending IT policy approvals |
| POST | `/api/v1/it/policies/{id}/approve/` | JWT (G4) | Director approves an IT policy change |
| POST | `/api/v1/it/policies/{id}/reject/` | JWT (G4) | Director rejects an IT policy change |
| POST | `/api/v1/it/policies/{id}/clarify/` | JWT (G4) | Director requests clarification |
| GET | `/api/v1/it/director/charts/integration-health/` | JWT (G4) | 30-day integration health line chart data |
| GET | `/api/v1/it/director/charts/ticket-trend/` | JWT (G4) | 12-week support ticket trend bar chart data |
| GET | `/api/v1/it/director/charts/portal-status/` | JWT (G4) | Portal status donut chart data |
| GET | `/api/v1/it/director/export/` | JWT (G4) | Triggers async PDF export of full IT report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/it/director/kpis/` | `#kpi-bar` | `innerHTML` |
| Load branch IT health table | `load` | GET `/api/v1/it/director/branch-health/` | `#branch-table` | `innerHTML` |
| Open branch IT detail drawer | `click` on branch name | GET `/api/v1/it/director/branch-health/{id}/` | `#detail-drawer` | `innerHTML` |
| Switch drawer tab | `click` on tab label | GET `/api/v1/it/director/branch-health/{id}/?tab=integrations` | `#drawer-content` | `innerHTML` |
| Paginate branch table | `click` on page button | GET `/api/v1/it/director/branch-health/?page=N` | `#branch-table` | `innerHTML` |
| Search branches | `keyup[debounce:300ms]` on search input | GET `/api/v1/it/director/branch-health/?search=` | `#branch-table` | `innerHTML` |
| Filter by portal status | `change` on status filter | GET `/api/v1/it/director/branch-health/?status=degraded` | `#branch-table` | `innerHTML` |
| Submit policy approval | `click` on Approve button | POST `/api/v1/it/policies/{id}/approve/` | `#approval-result` | `innerHTML` |
| Dismiss alert banner post-action | `click` on Dismiss | POST `/api/v1/it/director/alerts/{id}/acknowledge/` | `#alert-banner` | `outerHTML` |
| Donut chart segment click filters table | `click` on chart segment (JS → hx-trigger programmatic) | GET `/api/v1/it/director/branch-health/?status={segment}` | `#branch-table` | `innerHTML` |

---

**Audit Trail:** All write operations on this page are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications:** Critical alerts on this page trigger in-app notifications to the relevant role owners as specified in the alert banner conditions above.

*Page spec version: 1.0 · Last updated: 2026-03-21*
