# P-01 — Audit & Quality Dashboard

> **URL:** `/group/audit/dashboard/`
> **File:** `p-01-audit-quality-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Internal Audit Head (Role 121, G1) — primary viewer

---

## 1. Purpose

The Audit & Quality Dashboard is the central command centre for the entire audit and compliance function of an Institution Group. In Indian education, audit is not a back-office luxury — it's the mechanism that prevents affiliation loss, financial irregularity, safety violations, and academic quality erosion across 5–50 branches. The Internal Audit Head opens this dashboard every morning to answer: "Which branches are at risk? Which audits are overdue? Which findings haven't been fixed? Which affiliations are expiring?"

The problems this dashboard solves:

1. **Scattered compliance visibility:** Without a central dashboard, the Audit Head relies on WhatsApp messages from inspectors, Excel reports from branch principals, and email threads about affiliation documents. A 30-branch group generates 500–2,000 audit findings per year across financial, academic, and operational dimensions. The dashboard consolidates everything into one real-time view.

2. **Overdue finding blindness:** Audit findings are useless if corrective actions aren't tracked. In many Indian education groups, 40–60% of audit findings from the previous year remain unresolved because no one tracks closure. The dashboard prominently displays open findings by age, severity, and branch — making non-closure impossible to ignore.

3. **Affiliation risk early warning:** CBSE affiliation renewal requires 6–12 months of preparation. If the dashboard doesn't alert the Audit Head 12 months before expiry, the branch scrambles at the last minute, documents are incomplete, and renewal is delayed or denied. The dashboard shows affiliations expiring within 12 months with readiness percentage.

4. **CEO-ready compliance snapshot:** The Chairman/CEO expects a single view: "Are our branches compliant?" The Branch Compliance Scorecard section provides A+/A/B/C/D ratings per branch — instantly visible, colour-coded, drillable.

5. **Inspection coverage tracking:** In a 30-branch group, each branch should be inspected at least once per quarter (surprise) plus once per year (comprehensive). The dashboard tracks inspection coverage — branches that haven't been visited in 90+ days are flagged.

**Scale:** 5–50 branches · 150–400 audits/year · 500–2,000 findings/year · 50–200 open CAPAs at any time · 20–50 affiliations tracked · 100–300 regulatory filings/year

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Internal Audit Head | 121 | G1 | Full read — all audit data, all branches | Primary dashboard viewer |
| Group Academic Quality Officer | 122 | G1 | Read — academic audit section only | Filtered to academic dimension |
| Group Inspection Officer | 123 | G3 | Read — inspection section + own assignments | Sees own upcoming inspections |
| Group ISO / NAAC Coordinator | 124 | G1 | Read — certification section only | Filtered to quality certifications |
| Group Affiliation Compliance Officer | 125 | G1 | Read — affiliation section only | Filtered to affiliation compliance |
| Group Grievance Audit Officer | 126 | G1 | Read — grievance section only | Filtered to complaint patterns |
| Group Compliance Data Analyst | 127 | G1 | Full read — all audit data, all branches | Analytics and MIS generation |
| Group Process Improvement Coordinator | 128 | G3 | Read — CAPA section + own assigned items | Focuses on corrective actions |
| Group CEO / Chairman | — | G4/G5 | Full read — all sections | Strategic oversight |
| Group COO | 59 | G4 | Full read — all sections | Operational oversight |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Dashboard data is read-only; no create/edit/delete actions on the dashboard itself — all actions route to detail pages.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Dashboard
```

### 3.2 Page Header
```
Audit & Quality Dashboard                                    [Schedule Audit]  [Start Inspection]  [Export]
Audit Head — K. Ramachandra Rao
Sunrise Education Group · FY 2025-26 · 28 branches · Overall Compliance: 81% (Grade A)
```

**Header KPI ribbon:**
```
Last Audit: 2 days ago · Next Scheduled: Tomorrow (Kukatpally Branch) · Open Findings: 142 · Overdue CAPAs: 23
```

---

## 4. KPI Summary Bar (8 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Overall Compliance | Percentage | Weighted average of all branch compliance scores | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-compliance` |
| 2 | Audits Completed (FY) | Integer / Target | COUNT(audits) WHERE status = 'completed' AND fy = current / total planned | Green ≥ 80% of plan, Amber 60–79%, Red < 60% | `#kpi-audits` |
| 3 | Open Findings | Integer | COUNT(findings) WHERE status IN ('open', 'in_progress') | Red > 100, Amber 50–100, Green < 50 | `#kpi-findings` |
| 4 | Overdue CAPAs | Integer | COUNT(capa) WHERE due_date < today AND status != 'closed' | Red > 20, Amber 5–20, Green < 5 | `#kpi-overdue` |
| 5 | Affiliation Expiring (12m) | Integer | COUNT(affiliations) WHERE expiry_date BETWEEN today AND today + 365 | Red > 5, Amber 1–5, Green = 0 | `#kpi-affiliation` |
| 6 | Inspection Coverage | Percentage | Branches inspected in last 90 days / total branches × 100 | Green ≥ 80%, Amber 50–79%, Red < 50% | `#kpi-inspection` |
| 7 | CAPA Closure Rate | Percentage | Closed CAPAs within deadline / total CAPAs due × 100 | Green ≥ 80%, Amber 60–79%, Red < 60% | `#kpi-capa-rate` |
| 8 | Regulatory Filings Due (30d) | Integer | COUNT(filings) WHERE due_date BETWEEN today AND today + 30 AND status != 'filed' | Red > 5, Amber 1–5, Green = 0 | `#kpi-filings` |

---

## 5. Sections

### 5.1 Tab Navigation

Six tabs:
1. **Compliance Overview** — Branch compliance scores at a glance
2. **Audit Activity** — Recent and upcoming audits
3. **Open Findings** — All unresolved findings across branches
4. **Affiliation & Regulatory** — Affiliation status + filing deadlines
5. **Inspection Map** — Branch inspection coverage visual
6. **Alerts & Escalations** — Items needing immediate attention

### 5.2 Tab 1: Compliance Overview

**Branch compliance heatmap grid:**

```
┌──────────────────────────────────────────────────────────────┐
│  Branch Compliance Scorecard — 28 Branches                   │
│                                                              │
│  [Kukatpally]  [Dilsukhnagar]  [Miyapur]     [Ameerpet]    │
│    92% A         88% A           74% B          96% A+       │
│    🟢              🟢              🟡              🟢          │
│                                                              │
│  [Secunderabad] [LB Nagar]     [Uppal]       [Karimnagar]  │
│    67% C          81% A          45% D          85% A        │
│    🔴              🟢              ⚫              🟢          │
│                                                              │
│  ... (all branches shown as cards)                           │
└──────────────────────────────────────────────────────────────┘
```

**Also shown as table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch Name | Text (link) | Yes | Opens P-10 scorecard |
| Financial Score | Percentage | Yes | From P-03 |
| Academic Score | Percentage | Yes | From P-04 |
| Safety Score | Percentage | Yes | From P-05 |
| Affiliation Score | Percentage | Yes | From P-11 |
| CAPA Closure | Percentage | Yes | From P-15 |
| Grievance Score | Percentage | Yes | From P-18 |
| Overall Score | Percentage | Yes | Weighted composite |
| Grade | Badge | Yes | A+ / A / B / C / D |
| Trend | Arrow | Yes | ↑ Improving / → Stable / ↓ Declining (vs previous quarter) |
| Open Findings | Integer | Yes | Unresolved count |
| Last Inspection | Date | Yes | Most recent visit |

### 5.3 Tab 2: Audit Activity

**Upcoming Audits (next 30 days):**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Audit Name | Text (link) | Yes | Opens audit detail |
| Type | Badge | Yes | Financial / Academic / Operational / Safety / Comprehensive |
| Branch | Text | Yes | — |
| Scheduled Date | Date | Yes | — |
| Auditor(s) | Text | No | Assigned inspectors |
| Status | Badge | Yes | Scheduled / In Progress / Completed / Cancelled |
| Priority | Badge | Yes | Routine / High / Critical |

**Recent Audits (last 30 days):**

Same columns plus:
| Findings Count | Integer | Yes | Total findings from this audit |
| Critical Findings | Integer | Yes | Severity 1 findings |
| Score | Percentage | Yes | Audit score if applicable |

### 5.4 Tab 3: Open Findings

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Finding ID | Text (link) | Yes | Auto-generated: FIN-2026-001 |
| Finding | Text (truncated) | No | Description (first 100 chars) |
| Audit Type | Badge | Yes | Financial / Academic / Operational / Safety |
| Branch | Text | Yes | — |
| Severity | Badge | Yes | Critical (S1) / Major (S2) / Minor (S3) / Observation (S4) |
| Found Date | Date | Yes | — |
| Age (days) | Integer | Yes | Days since found |
| CAPA Status | Badge | Yes | Open / Assigned / In Progress / Verification / Closed |
| Assigned To | Text | Yes | Person responsible for correction |
| Due Date | Date | Yes | CAPA deadline |
| Overdue | Badge | Yes | Yes (red) / No (green) / Due Soon (amber) |

**Filters:** Branch (multi-select) · Audit Type · Severity · Status · Age range · Assigned to

### 5.5 Tab 4: Affiliation & Regulatory

**Affiliation Status:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Board | Badge | Yes | CBSE / ICSE / BSEAP / BSETS / Other |
| Affiliation No. | Text | No | — |
| Valid Until | Date | Yes | Expiry date |
| Months Remaining | Integer | Yes | Colour-coded: Red < 6m, Amber 6–12m, Green > 12m |
| Requirements Met | Fraction | Yes | e.g., 38/42 |
| Readiness | Percentage | Yes | Requirements met % |
| Status | Badge | Yes | Active / Renewal Due / Under Review / Expired / Provisional |

**Regulatory Filings Due:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Filing | Text | Yes | UDISE+, AISHE, RTE Return, Fire Safety NOC, etc. |
| Branch | Text | Yes | — |
| Due Date | Date | Yes | — |
| Days Until Due | Integer | Yes | Red < 7d, Amber 7–30d, Green > 30d |
| Status | Badge | Yes | Not Started / In Progress / Filed / Overdue |
| Filed By | Text | Yes | Person responsible |

### 5.6 Tab 5: Inspection Map

**Interactive map (Leaflet.js):**
- Branch markers colour-coded by last inspection recency:
  - Green: Inspected within 30 days
  - Amber: Inspected 31–90 days ago
  - Red: Not inspected in 90+ days
  - Grey: Never inspected
- Click marker → popup with branch name, last inspection date, score, next scheduled
- Layer toggles: All / Financial / Academic / Safety inspections

**Inspection coverage table below map:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Last Inspection | Date | Yes | — |
| Days Since | Integer | Yes | Red > 90, Amber 60–90, Green < 60 |
| Inspections This FY | Integer | Yes | Count |
| Target | Integer | No | Based on audit plan |
| Coverage | Percentage | Yes | Actual / target |
| Next Scheduled | Date | Yes | — |
| Inspector | Text | Yes | Assigned person |

### 5.7 Tab 6: Alerts & Escalations

**Alert cards — sorted by urgency:**

```
┌─────────────────────────────────────────────────────────────┐
│ 🔴 CRITICAL — Affiliation Expired: Karimnagar Branch BSETS  │
│    Expired: 15 Mar 2026 · Students affected: 1,200          │
│    Action: Renewal application pending with state board      │
│    Escalated to: CEO on 10 Mar 2026                         │
│    [View Details]  [Add Note]                                │
├─────────────────────────────────────────────────────────────┤
│ 🟡 HIGH — 15 CAPAs overdue > 30 days: Dilsukhnagar Branch  │
│    Oldest: Fire extinguisher replacement (45 days overdue)   │
│    Assigned: Branch Principal                                │
│    [View CAPAs]  [Escalate to CEO]                          │
├─────────────────────────────────────────────────────────────┤
│ 🟡 HIGH — UDISE+ filing deadline in 5 days: 8 branches     │
│    Filed: 20/28 · Remaining: 8 branches                     │
│    [View Branches]  [Send Reminder]                         │
└─────────────────────────────────────────────────────────────┘
```

**Alert types:**
- Affiliation expiry/expiring (< 6 months)
- CAPA overdue > 30 days
- Regulatory filing overdue or due within 7 days
- Branch compliance score dropped below C (< 50%)
- Branch not inspected in 90+ days
- Critical (S1) finding unresolved > 14 days
- Fire safety NOC expired
- Teacher-student ratio breach (CBSE/RTE norm)

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-compliance-detail` (720px, right-slide)

- **Title:** "Branch Compliance — [Branch Name]"
- **Tabs:** Overview · Financial · Academic · Safety · Affiliation · CAPA · History
- **Overview tab:**
  - Spider/radar chart: 6 compliance dimensions
  - Overall score with grade badge
  - Trend chart (last 4 quarters)
  - Open findings count by severity
  - Last inspection date and score
- **Financial tab:** Latest financial audit summary, findings, CAPA status
- **Academic tab:** Latest academic audit summary, lesson plan compliance %, exam quality score
- **Safety tab:** Safety checklist status, fire NOC, CCTV coverage, first aid
- **Affiliation tab:** Board affiliation status, requirements met/gap, documents uploaded
- **CAPA tab:** All open CAPAs for this branch with status and age
- **History tab:** All audits conducted at this branch — chronological
- **Footer:** [View Full Scorecard (P-10)] [Schedule Audit] [View Inspection Reports]
- **Access:** G1+ (Division P roles)

### 6.2 Modal: `schedule-quick-audit` (560px)

- **Title:** "Schedule Audit"
- **Fields:**
  - Audit type (dropdown): Financial / Academic / Operational / Safety / Comprehensive
  - Branch (dropdown, required)
  - Scheduled date (date picker, required)
  - Surprise visit? (toggle — if yes, branch is NOT notified)
  - Auditor(s) (multi-select from Division P team)
  - Priority (radio): Routine / High / Critical
  - Special focus areas (textarea, optional)
  - Linked to previous finding? (toggle + finding ID if yes)
- **Buttons:** Cancel · Schedule
- **Validation:** Cannot schedule two audits of same type at same branch within 7 days
- **Access:** Role 121, 123, G4+

### 6.3 Modal: `alert-detail` (480px)

- **Title:** "Alert — [Alert Type]"
- **Content:** Full alert details, affected branches, timeline, current status
- **Actions:** Acknowledge · Add Note · Escalate to CEO · Dismiss (with reason)
- **Access:** G1+ (Division P roles)

### 6.4 Drawer: `finding-quick-view` (640px, right-slide)

- **Title:** "Finding — [Finding ID]"
- **Content:** Finding description, audit context, severity, photos/evidence, CAPA status
- **CAPA section:** Assigned to, root cause, corrective action, deadline, progress notes
- **Footer:** [View Full Finding (P-06)] [Edit CAPA (P-15)] [Escalate]
- **Access:** G1+ (Division P roles)

---

## 7. Charts

### 7.1 Compliance Score Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Branch Compliance Grade Distribution" |
| Data | COUNT(branches) per grade band (A+, A, B, C, D) |
| Colours | A+: #10B981, A: #34D399, B: #FBBF24, C: #F97316, D: #EF4444 |
| Centre text | N branches total |
| API | `GET /api/v1/group/{id}/audit/dashboard/compliance-distribution/` |

### 7.2 Finding Severity Breakdown (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Open Findings by Severity" |
| Data | COUNT(findings) per severity (S1, S2, S3, S4) — stacked by status (Open, In Progress, Verification) |
| Colours | S1: #EF4444, S2: #F97316, S3: #FBBF24, S4: #94A3B8 |
| API | `GET /api/v1/group/{id}/audit/dashboard/findings-severity/` |

### 7.3 Audit Coverage Timeline (Stacked Area)

| Property | Value |
|---|---|
| Chart type | Stacked area |
| Title | "Monthly Audit Coverage — FY 2025-26" |
| Data | COUNT(audits) per month per type (Financial, Academic, Operational, Safety) |
| API | `GET /api/v1/group/{id}/audit/dashboard/coverage-trend/` |

### 7.4 Branch Compliance Trend (Multi-Line)

| Property | Value |
|---|---|
| Chart type | Multi-line |
| Title | "Branch Compliance Scores — Quarterly Trend" |
| Data | Overall compliance score per branch per quarter (last 4 quarters) |
| Line per branch | Top 5 and bottom 5 branches highlighted, rest greyed |
| API | `GET /api/v1/group/{id}/audit/dashboard/compliance-trend/` |

### 7.5 CAPA Ageing Distribution (Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar |
| Title | "CAPA Ageing — Open Items" |
| Data | COUNT(capa) by age bucket: 0–7d, 8–14d, 15–30d, 31–60d, 60d+ |
| Colour | Green → Amber → Red gradient by age |
| API | `GET /api/v1/group/{id}/audit/dashboard/capa-ageing/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit scheduled | "Audit scheduled — [Branch], [Date]" | Success | 3s |
| Alert acknowledged | "Alert acknowledged" | Info | 3s |
| Alert escalated | "Alert escalated to [CEO Name]" | Warning | 4s |
| Alert dismissed | "Alert dismissed" | Info | 3s |
| Finding escalated | "Finding [ID] escalated to [Role]" | Warning | 4s |
| Dashboard refreshed | "Dashboard data refreshed" | Info | 2s |
| Export started | "Exporting dashboard report — download will start shortly" | Info | 3s |
| Affiliation expiry alert | "⚠️ [Branch] affiliation expires in [N] days" | Warning | 6s |
| Critical finding alert | "🔴 Critical finding unresolved for [N] days at [Branch]" | Error | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No audits planned | 📋 | "No Audits Scheduled" | "Create an audit plan to begin tracking compliance across branches." | Schedule Audit |
| No findings | ✅ | "No Open Findings" | "All audit findings have been resolved. Great compliance!" | — |
| No branches configured | 🏫 | "No Branches Found" | "Branch data is required to begin auditing. Contact Group IT Admin." | — |
| No inspection data | 🔍 | "No Inspections Recorded" | "Schedule your first branch inspection to start building compliance data." | Start Inspection |
| No alerts | 🔔 | "No Active Alerts" | "All compliance metrics are within acceptable thresholds." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 8 KPI shimmer cards + tab skeleton |
| Tab switch | Tab content skeleton (table or chart placeholder) |
| Compliance heatmap | Card grid skeleton (N branch cards) |
| Branch detail drawer | 720px skeleton: radar chart placeholder + 7 tabs |
| Chart load | Grey canvas placeholder per chart |
| Map load | Grey map rectangle + "Loading map…" text |
| Finding list | Table skeleton with 10 rows |
| Alert cards | 3 card skeletons |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/dashboard/kpis/` | G1+ | All 8 KPI values |
| GET | `/api/v1/group/{id}/audit/dashboard/compliance-overview/` | G1+ | Branch compliance scores table |
| GET | `/api/v1/group/{id}/audit/dashboard/compliance-distribution/` | G1+ | Grade distribution chart data |
| GET | `/api/v1/group/{id}/audit/dashboard/compliance-trend/` | G1+ | Quarterly trend per branch |
| GET | `/api/v1/group/{id}/audit/dashboard/audit-activity/` | G1+ | Upcoming + recent audits |
| GET | `/api/v1/group/{id}/audit/dashboard/findings/` | G1+ | Open findings list with filters |
| GET | `/api/v1/group/{id}/audit/dashboard/findings-severity/` | G1+ | Severity breakdown chart data |
| GET | `/api/v1/group/{id}/audit/dashboard/affiliation-status/` | G1+ | Affiliation status table |
| GET | `/api/v1/group/{id}/audit/dashboard/regulatory-filings/` | G1+ | Filings due table |
| GET | `/api/v1/group/{id}/audit/dashboard/inspection-map/` | G1+ | Branch inspection coverage + map data |
| GET | `/api/v1/group/{id}/audit/dashboard/alerts/` | G1+ | Active alerts list |
| GET | `/api/v1/group/{id}/audit/dashboard/capa-ageing/` | G1+ | CAPA ageing chart data |
| GET | `/api/v1/group/{id}/audit/dashboard/coverage-trend/` | G1+ | Monthly audit coverage trend |
| POST | `/api/v1/group/{id}/audit/audits/` | G3+ | Quick-schedule an audit |
| PATCH | `/api/v1/group/{id}/audit/dashboard/alerts/{alert_id}/acknowledge/` | G1+ | Acknowledge alert |
| PATCH | `/api/v1/group/{id}/audit/dashboard/alerts/{alert_id}/escalate/` | G1+ | Escalate alert |
| PATCH | `/api/v1/group/{id}/audit/dashboard/alerts/{alert_id}/dismiss/` | G1+ | Dismiss alert (with reason) |
| GET | `/api/v1/group/{id}/audit/branches/{branch_id}/compliance/` | G1+ | Branch compliance detail |
| GET | `/api/v1/group/{id}/audit/dashboard/export/` | G1+ | Export dashboard as PDF/Excel |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../dashboard/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#dashboard-content` | `innerHTML` | `hx-trigger="click"` |
| Branch compliance drawer | Branch card/row click | `hx-get=".../branches/{id}/compliance/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Schedule audit | Form submit | `hx-post=".../audits/"` | `#schedule-result` | `innerHTML` | Toast on success |
| Alert acknowledge | Button click | `hx-patch=".../alerts/{id}/acknowledge/"` | `#alert-{id}` | `outerHTML` | Inline update |
| Alert escalate | Button click | `hx-patch=".../alerts/{id}/escalate/"` | `#alert-{id}` | `outerHTML` | Toast + inline update |
| Finding quick-view | Finding row click | `hx-get=".../findings/{id}/"` | `#right-drawer` | `innerHTML` | 640px drawer |
| Filter findings | Filter change | `hx-get` with filter params | `#findings-table` | `innerHTML` | `hx-trigger="change"` |
| Map load | Tab 5 shown | Non-HTMX (Leaflet.js) | — | — | JavaScript map init |
| Chart load | Tab shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js init |
| Auto-refresh | Every 5 min | `hx-get=".../dashboard/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="every 300s"` |
| Export | Button click | `hx-get=".../dashboard/export/"` | `#export-result` | `innerHTML` | Download trigger |
| Pagination | Page click | `hx-get` with page param | `#table-body` | `innerHTML` | Standard pagination |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
