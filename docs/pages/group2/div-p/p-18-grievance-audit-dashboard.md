# P-18 — Grievance Audit Dashboard

> **URL:** `/group/audit/grievances/`
> **File:** `p-18-grievance-audit-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Grievance Audit Officer (Role 126, G1) — primary operator

---

## 1. Purpose

The Grievance Audit Dashboard is the audit lens on top of the group's grievance system. It does not replace the operational grievance management system (which lives in the branch-level welfare and admin modules) — instead, it reads grievance data across all branches and applies audit intelligence: Are complaints being resolved on time? Are the same types of complaints recurring at the same branches? Are there branches where serious grievances (POCSO, harassment, safety) are being under-reported or quietly closed without proper investigation? Are resolution quality standards being met, or are branches marking complaints "closed" without genuine resolution?

In Indian education — particularly for groups running schools, coaching centres, and hostels — grievances are a governance and reputational risk. A single unresolved POCSO complaint that eventually reaches media or NCPCR (National Commission for Protection of Child Rights) can destroy a 30-branch group's reputation and trigger regulatory action. A pattern of fee-related complaints that goes unnoticed can signal misappropriation. A hostel safety complaint that isn't escalated can precede a serious incident.

The problems this page solves:

1. **Resolution time SLA breaches:** Every grievance type has a mandated resolution timeline — POCSO complaints within 7 days under law; general academic complaints within 15 working days per RTE; fee disputes within 30 days. The dashboard flags every SLA breach by category and branch.

2. **Re-opened complaints hiding systemic failure:** Branches that close complaints quickly but have high re-open rates are not resolving — they're suppressing. The re-open rate is a key quality signal that branches cannot game easily.

3. **Under-reporting detection:** A branch with 2,000 students but only 3 complaints in a year is statistically unlikely. Either students have no mechanism to complain, or complaints are not being formally recorded. Under-reporting heatmap identifies anomalies.

4. **Complaint category pattern by branch type:** Teaching quality complaints cluster at coaching centres; fee disputes at private unaided schools; hostel safety at residential schools. The dashboard shows whether each branch is receiving complaint types appropriate to its institution type.

5. **High-severity complaint tracking:** POCSO, harassment, safety, and discrimination complaints need direct Grievance Audit Officer visibility. These are tracked in a separate high-severity stream with mandatory audit officer acknowledgement.

6. **Resolution quality vs resolution speed:** A complaint resolved in 3 days with a dismissive response is worse than one resolved in 15 days with a genuine remedy. The platform captures complainant satisfaction score (1–5) as part of closure — the audit dashboard tracks satisfaction trends alongside speed.

**Scale:** 5–50 branches · 200–1,000 complaints/year (large group) · 30–100 (small group) · 8 complaint categories · 4 severity levels · SLA varies by category

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Grievance Audit Officer | 126 | G1 | Full read access — all branches, all complaint categories, all severity levels | Primary operator |
| Group Internal Audit Head | 121 | G1 | Read — grievance audit data in audit scope | Cross-functional |
| Group Compliance Data Analyst | 127 | G1 | Read — grievance metrics for MIS | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read + Create CAPA from grievance patterns | Remediation |
| Branch Principal | — | G3 | Read own branch only — summary view, no individual complainant details | Branch awareness |
| Zone Director | — | G4 | Read own zone — all branches in zone | Zone oversight |
| Group CEO / Chairman | — | G4/G5 | Read all + High-severity complaint alerts | Executive |
| Legal / Compliance Advisor (external) | — | G1 (restricted) | Read only POCSO / harassment / legal category complaints | Compliance review |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Individual complainant identity (name, contact) is NOT accessible from this audit dashboard — it is masked to protect complainant privacy (DPDPA compliance). The audit officer sees complaint category, branch, date, severity, status, and resolution outcome only. Identity is accessible only to the branch-level operational grievance system.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Grievance Audit
```

### 3.2 Page Header
```
Grievance Audit Dashboard                          [Export]  [Raise CAPA from Pattern]
Grievance Audit Officer — M. Srinivas
Sunrise Education Group · 28 branches · 847 complaints (FY) · 34 open · 12 SLA breached · 3 high-severity
```

### 3.3 Filter Bar
```
Branch: [All / Select ▼]    Category: [All / Academic / Fee / Safety / POCSO / Harassment / Infrastructure / Staff Conduct / Other ▼]
Severity: [All / Critical (Legal/POCSO) / High / Medium / Low ▼]
Status: [All / Open / Under Investigation / Resolved / Re-opened / Closed ▼]
SLA: [All / Within SLA / SLA Breached / Due Today ▼]
Period: [This FY ▼]    Month: [All / Jan / Feb … ▼]
                                                                        [Reset Filters]
```

### 3.4 KPI Summary Bar

| # | KPI | Source | Colour Logic |
|---|---|---|---|
| 1 | Total Complaints (FY) | Count all complaints raised in current FY | Neutral blue |
| 2 | Open Complaints | Status = Open or Under Investigation | ≤ 5 green · 6–15 amber · > 15 red |
| 3 | SLA Breached | Past resolution deadline, not closed | 0 green · 1–5 amber · > 5 red |
| 4 | High-Severity Open | Critical/High severity, not closed | 0 green · 1–2 amber · ≥ 3 red |
| 5 | Avg Resolution Time | Mean days from complaint raised to closed | ≤ SLA green · SLA+3 amber · > SLA+3 red |
| 6 | Re-open Rate | % complaints re-opened after first closure | ≤ 5% green · 6–15% amber · > 15% red |
| 7 | Complainant Satisfaction Score | Mean satisfaction rating (1–5) at closure | ≥ 4.0 green · 3.0–3.9 amber · < 3.0 red |
| 8 | Under-reporting Flags | Branches flagged for anomalously low complaint volume | 0 green · ≥ 1 amber |

### 3.5 Tab Navigation

```
[Overview]    [Branch Comparison]    [High-Severity Stream]    [SLA Compliance]    [Trends]
```

---

### Tab 1 — Overview (default)

**Section A — Complaint Volume by Category (horizontal bar)**
Categories ranked by total complaints (FY):
Academic Quality (245) · Fee Disputes (187) · Staff Conduct (142) · Infrastructure (98) · Safety (75) · Harassment (52) · POCSO (24) · Other (24)

Each bar split by status: Resolved (green) / Under Investigation (blue) / Open (amber) / Re-opened (red).

**Section B — Branch Complaint Heatmap (matrix)**
Branches as rows · Months as columns · Cell = complaint count.
Colour: White (0) → Light amber (1–5) → Orange (6–15) → Red (16+).
Cells with SLA breaches have a red border. Under-reporting flags shown as dotted grey cell.

**Section C — SLA Status Summary**

| Category | SLA Mandate | Total This FY | Within SLA | Breached | Breach Rate |
|---|---|---|---|---|---|
| POCSO | 7 days (statutory) | 24 | 21 | 3 | 12.5% 🔴 |
| Safety | 3 days (group policy) | 75 | 70 | 5 | 6.7% 🟠 |
| Harassment | 10 days (group policy) | 52 | 49 | 3 | 5.8% 🟠 |
| Fee Disputes | 30 days (group policy) | 187 | 182 | 5 | 2.7% 🟢 |
| Academic | 15 days (RTE-aligned) | 245 | 238 | 7 | 2.9% 🟢 |
| Staff Conduct | 21 days (group policy) | 142 | 135 | 7 | 4.9% 🟢 |
| Infrastructure | 14 days (group policy) | 98 | 91 | 7 | 7.1% 🟠 |

**Section D — Top 5 Complaint Issues (text list)**
Most frequent specific complaint descriptions (after category analysis by P-19):
1. "Homework overload / insufficient rest time" — 87 complaints across 12 branches
2. "Fee receipt not provided" — 65 complaints across 8 branches
3. "Teacher behaviour — verbal reprimand in front of class" — 48 complaints across 15 branches
4. "Hostel food quality / hygiene" — 41 complaints (hostel branches only)
5. "No response from admin to previous complaint" — 38 complaints — meta-complaint indicating systemic non-response

---

### Tab 2 — Branch Comparison

Full table — one row per branch — for comparative grievance metrics.

**Table columns:**

| # | Column | Content |
|---|---|---|
| 1 | Branch | Branch name |
| 2 | Institution Type | School / Coaching / Hostel / College |
| 3 | Total Complaints (FY) | Count |
| 4 | Complaints per 100 Students | Normalised rate (accounts for branch size) |
| 5 | Open | Currently open |
| 6 | SLA Breached | Count with SLA violation |
| 7 | Critical/High Open | Count of high-severity open |
| 8 | Re-open Rate | % re-opened after first closure |
| 9 | Avg Resolution (days) | Mean days to close |
| 10 | Satisfaction Score | Mean complainant satisfaction (1–5) |
| 11 | Under-reporting Flag | ⚠️ if flagged |
| 12 | Trend | ↑ ↓ → vs prior quarter |
| 13 | Actions | [View Branch Detail] |

**Under-reporting flag logic:**
```
Flag if: (complaints per 100 students) < (0.4 × group median for same institution type)
Note: A coaching branch with 500 students and 1 complaint vs a median of 8.5 complaints/100 students
      for similar branches = under-reporting flag
```

**Sorting:** By SLA Breached descending (worst first) — default.

---

### Tab 3 — High-Severity Stream

Dedicated view for Critical and High severity complaints only. Every complaint in this tab requires Grievance Audit Officer acknowledgement.

**Table columns:**

| # | Column | Content |
|---|---|---|
| 1 | Complaint ID | `GRV-2026-00234` (masked — no complainant info) |
| 2 | Branch | Branch name |
| 3 | Category | POCSO / Harassment / Safety / Staff Conduct |
| 4 | Severity | 🔴 Critical / 🟠 High |
| 5 | Raised Date | dd-MMM-yyyy |
| 6 | SLA Deadline | Date · Highlighted red if past |
| 7 | Days Remaining / Overdue | +N days or −N days overdue |
| 8 | Status | Open / Under Investigation / Resolved / Re-opened |
| 9 | Audit Acknowledged | ✅ Yes / ❌ No |
| 10 | Investigation Officer | Assigned internal investigator |
| 11 | Actions | [Acknowledge] · [View] · [Escalate] |

**Unacknowledged complaints** (column 9 = ❌) show a persistent amber banner at page top:
```
⚠️ 3 high-severity complaints require your acknowledgement — scroll down or click here
```

**POCSO-specific panel (always visible in this tab):**
```
POCSO Complaint Status — FY 2025-26
Total Filed: 24 · Resolved within 7 days: 21 · Breached: 3
Internal Committee (IC) constituted: ✅ All 28 branches
Last IC meeting logged: Sunrise Miyapur — 15-Feb-2026 (42 days ago ⚠️ — IC must meet quarterly)
```

---

### Tab 4 — SLA Compliance

Granular view of SLA performance by branch and category.

**Section A — SLA Compliance Matrix**
Branches (rows) × Complaint categories (columns). Each cell shows:
- Complaint count in that category for this branch
- Compliance rate (green/amber/red)

Example cell: `7 complaints · 85% on time`

**Section B — SLA Breach Detail Table**

| Complaint ID | Branch | Category | Raised | SLA Deadline | Days Overdue | Current Status |
|---|---|---|---|---|---|---|
| GRV-2026-00234 | Sunrise Miyapur | POCSO | 01-Mar-2026 | 08-Mar-2026 | 18 days | Under Investigation |
| GRV-2026-00301 | Sunrise Begumpet | Safety | 05-Mar-2026 | 08-Mar-2026 | 12 days | Open |
| … | | | | | | |

**Each row:** [Escalate] · [View CAPA]

**Section C — SLA Policy Reference**

| Category | SLA | Authority | Consequence of Breach |
|---|---|---|---|
| POCSO | 7 days | POCSO Act 2012, Sec 19 | Criminal liability for non-reporting; mandatory IC inquiry |
| Safety incident | 3 days | Group policy + state safety norms | CAPA raised + CEO alert |
| Harassment | 10 days | Group policy aligned to UGC policy | CAPA raised + Audit Head alert |
| Academic quality | 15 working days | Group policy (RTE-aligned) | CAPA raised if breached repeatedly |
| Fee dispute | 30 days | Group policy | CAPA raised if breached |
| Staff conduct | 21 days | Group policy | CAPA raised; HR involvement |
| Infrastructure | 14 days | Group policy | Branch maintenance ticket escalated |

---

### Tab 5 — Trends

Long-term trend analysis for strategic audit insight.

**Section A — Monthly Complaint Volume (line chart)**
Monthly complaint count across all branches. Shows if complaint volume is growing (may indicate improving culture of reporting or genuine increase in problems) or shrinking (may indicate suppression).

**Section B — Resolution Time Trend (line chart)**
Average resolution time per month by category. Tracks whether the group is getting better or worse at resolving grievances.

**Section C — Re-open Rate Trend (line chart)**
Monthly re-open rate. Rising re-open rate signals that "resolutions" are superficial.

**Section D — Satisfaction Score Trend (line chart)**
Mean complainant satisfaction per month. Declining trend warrants investigation even if resolution speed is good.

**Section E — Complaint Category Shift (stacked bar — annual)**
How the mix of complaint categories has changed year over year. Shift toward POCSO/harassment = serious governance concern. Shift toward fee disputes = financial governance issue.

---

## 4. KPI Summary Bar

(Defined in Section 3.4 above)

---

## 5. Sections

| # | Section | Location | Purpose |
|---|---|---|---|
| 1 | Overview | Tab 1 | Volume by category, branch heatmap, SLA summary, top issues |
| 2 | Branch Comparison | Tab 2 | Normalised metrics per branch with under-reporting flags |
| 3 | High-Severity Stream | Tab 3 | POCSO, harassment, safety — requires active audit attention |
| 4 | SLA Compliance | Tab 4 | Granular SLA tracking by branch and category |
| 5 | Trends | Tab 5 | Long-term patterns for strategic insight |
| 6 | Complaint Detail Drawer | Right drawer | Individual complaint detail (identity masked) |
| 7 | Escalate to CAPA Modal | Modal | Raise a CAPA finding from a grievance pattern |
| 8 | Acknowledge Modal | Modal | Record audit officer acknowledgement of high-severity complaint |
| 9 | Export Modal | Modal | Export grievance audit report |

---

## 6. Drawers & Modals

### Drawer 1 — Complaint Detail Drawer (right, 760px)

**Trigger:** Click any row in SLA Breach table or High-Severity stream.

**Header:**
```
Complaint Detail — GRV-2026-00234                               [Acknowledge] [Escalate] [✕]
Sunrise Miyapur · POCSO · 🔴 Critical · Raised: 01-Mar-2026
```

**Content (identity-masked):**

| Field | Value |
|---|---|
| Complaint ID | GRV-2026-00234 |
| Branch | Sunrise Miyapur |
| Category | POCSO |
| Severity | 🔴 Critical |
| Raised On | 01-Mar-2026 |
| Raised By | [Student — identity masked per DPDPA] |
| Nature of Complaint | [Summary only — "Physical contact by staff member in classroom — further details in IC file"] |
| IC Constituted | ✅ Yes — 02-Mar-2026 |
| Internal Investigator | K. Latha (Vice Principal) |
| SLA Deadline | 08-Mar-2026 · 18 days overdue |
| Current Status | Under Investigation |
| Last Update | 15-Mar-2026 — "IC meeting 2 held; witness statements recorded" |
| Audit Acknowledged | ✅ M. Srinivas · 02-Mar-2026 |
| CAPA Linked | CAPA-2026-00412 (IC process compliance audit) |

**Important note displayed:**
```
ℹ️ Complainant identity and detailed IC proceedings are confidential. Access restricted to
   Branch IC members and Group Legal Advisor. This view shows audit-level summary only.
```

**Actions:**
```
[Escalate to CEO]  [Request IC Report]  [Raise CAPA]  [Add Audit Note]
```

---

### Modal 1 — Raise CAPA from Pattern

**Trigger:** `[Raise CAPA from Pattern]` button in page header or from Overview tab.

**Form:**
```
Pattern Identified:
  [Text: e.g., "3 SLA-breached POCSO complaints in Sunrise Miyapur in 30 days"]

Select Related Complaints: [Multi-select from list — masked IDs only]

CAPA Details:
  Branch: [Auto-filled]
  Severity: [Critical / Major / Minor ▼]
  Category: [POCSO / Safety / Staff Conduct / Process ▼]
  Finding Description: [Auto-populated from pattern + editable]
  Due Date: [Date]
  Assigned To: [Branch Principal ▼]

Escalate Simultaneously:
  ☐ Zone Director   ☐ Audit Head   ☐ CEO
```

**Actions:** `[Raise CAPA]` `[Cancel]`

---

### Modal 2 — Acknowledge High-Severity Complaint

**Trigger:** `[Acknowledge]` in High-Severity stream.

**Form:**
```
Complaint: GRV-2026-00234 · POCSO · Sunrise Miyapur · 01-Mar-2026

I, M. Srinivas (Grievance Audit Officer), acknowledge receipt of this complaint and confirm:
  ☐ IC has been constituted at the branch (mandatory for POCSO)
  ☐ Investigation is underway
  ☐ SLA timeline has been communicated to the branch
  ☐ I will monitor this complaint until resolution

Acknowledgement Date: [Today — auto-filled]
Notes: [___________________________]
```

**Actions:** `[Confirm Acknowledgement]` `[Cancel]`

---

## 7. Charts

### Chart 1 — Complaint Volume by Category (horizontal bar)
- **Type:** Horizontal stacked bar (Chart.js 4.x)
- **X-axis:** Complaint count
- **Y-axis:** Category
- **Stack:** Resolved (green) · Under Investigation (blue) · Open (amber) · Re-opened (red)
- **API:** `GET /api/v1/group/{id}/audit/grievances/charts/by-category/`

### Chart 2 — Branch Heatmap (matrix)
- **Type:** Matrix heatmap (chartjs-chart-matrix plugin)
- **X-axis:** Months
- **Y-axis:** Branches
- **Colour:** White → Amber → Red by complaint count
- **API:** `GET /api/v1/group/{id}/audit/grievances/charts/branch-heatmap/`

### Chart 3 — Monthly Volume Trend (line)
- **Type:** Line (Chart.js 4.x)
- **X-axis:** Months (Apr–Mar, current FY)
- **Y-axis:** Complaint count
- **Series:** Total (blue) · High/Critical (red) · Resolved (green)
- **API:** `GET /api/v1/group/{id}/audit/grievances/charts/monthly-trend/`

### Chart 4 — Satisfaction Score Trend (line)
- **Type:** Line (Chart.js 4.x)
- **X-axis:** Months
- **Y-axis:** Mean satisfaction score (1–5)
- **Benchmark:** Dashed line at 4.0 (target)
- **API:** `GET /api/v1/group/{id}/audit/grievances/charts/satisfaction-trend/`

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Audit acknowledged | "GRV-2026-00234 acknowledged — POCSO · Sunrise Miyapur · 01-Mar-2026" | Success (green) |
| CAPA raised | "CAPA-2026-00412 raised from grievance pattern — SLA breach POCSO · Sunrise Miyapur" | Info (blue) |
| Escalation sent | "GRV-2026-00234 escalated to CEO — POCSO · 18 days overdue" | Warning (amber) |
| High-severity alert | "⚠️ New POCSO complaint filed at Sunrise Miyapur — requires immediate acknowledgement" | Error (red) |
| Under-reporting flag | "⚠️ Under-reporting detected — Sunrise Kukatpally has 0.4 complaints per 100 students vs group median 8.2" | Warning (amber) |
| Export prepared | "Grievance audit report exported — 847 complaints · FY 2025-26" | Info (blue) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No complaints on record | Green shield | "No complaints recorded for this period. This may indicate excellent service — or under-reporting. Review branch complaint mechanisms." | `[Check Under-reporting]` |
| No SLA breaches | Clock with green tick | "All complaints resolved within SLA — excellent compliance." | — |
| No high-severity complaints | Shield with checkmark | "No high-severity complaints in this period." | — |
| Filter returns zero | Magnifying glass | "No complaints match your filters." | `[Reset Filters]` |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Page initial load | Skeleton: KPI bar + chart placeholders | < 1s |
| KPI bar | 8 grey pulse cards → populated | < 500ms |
| Category bar chart | Grey placeholder → Chart.js | < 500ms |
| Branch heatmap | Grid skeleton → populated | < 1.5s (large group) |
| SLA matrix (Tab 4) | Grid skeleton → populated | < 1s |
| High-severity table | Skeleton rows → data | < 500ms |
| Complaint detail drawer | Drawer skeleton → populated | < 500ms |
| Trend charts (Tab 5) | 4 chart placeholders → Chart.js | < 1s |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/grievances/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | Grievance audit data (paginated, filterable, identity-masked) | G1+ |
| 2 | GET | `/{complaint_id}/` | Individual complaint audit detail (masked) | G1+ |
| 3 | POST | `/{complaint_id}/acknowledge/` | Record audit officer acknowledgement | 126 |
| 4 | POST | `/{complaint_id}/escalate/` | Escalate high-severity complaint | 126, G4+ |
| 5 | GET | `/high-severity/` | Critical + High severity complaints only | G1+ |
| 6 | GET | `/sla-breaches/` | All complaints past SLA deadline | G1+ |
| 7 | GET | `/under-reporting-flags/` | Branches flagged for anomalously low volume | G1+ |
| 8 | GET | `/branch-comparison/` | Per-branch normalised metrics | G1+ |
| 9 | GET | `/sla-matrix/` | Branch × category SLA compliance matrix | G1+ |
| 10 | POST | `/raise-capa/` | Create CAPA from grievance pattern | 126, 128 |
| 11 | GET | `/kpis/` | KPI bar aggregates | G1+ |
| 12 | GET | `/charts/by-category/` | Chart 1 data | G1+ |
| 13 | GET | `/charts/branch-heatmap/` | Chart 2 data | G1+ |
| 14 | GET | `/charts/monthly-trend/` | Chart 3 data | G1+ |
| 15 | GET | `/charts/satisfaction-trend/` | Chart 4 data | G1+ |
| 16 | GET | `/export/` | Export grievance audit report (Excel/PDF) | G1+ |

> **Data privacy note:** All endpoints return identity-masked data (no complainant name, contact, or class details). Full identity and IC proceedings are accessible only via branch-level grievance system with appropriate role + DPDPA audit log.

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../grievances/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#grv-content` | `innerHTML` | — |
| Overview charts | Tab 1 load | `hx-get` multiple chart endpoints | `#chart-{name}` | `innerHTML` | Chart.js init |
| Branch comparison | Tab 2 load | `hx-get=".../grievances/branch-comparison/"` | `#branch-table` | `innerHTML` | Sortable |
| High-severity table | Tab 3 load | `hx-get=".../grievances/high-severity/"` | `#high-severity-table` | `innerHTML` | Auto-refresh 5min |
| SLA matrix | Tab 4 load | `hx-get=".../grievances/sla-matrix/"` | `#sla-matrix` | `innerHTML` | Grid render |
| Trend charts | Tab 5 load | `hx-get` chart endpoints | `#chart-{name}` | `innerHTML` | 4 charts |
| Filter change | Select change | `hx-get` with filters | `#grv-content` | `innerHTML` | Debounced |
| Complaint detail | Row click | `hx-get=".../grievances/{id}/"` | `#right-drawer` | `innerHTML` | 760px drawer |
| Acknowledge | Button click | `hx-post=".../grievances/{id}/acknowledge/"` | `#complaint-{id}-ack` | `innerHTML` | Toast + badge update |
| Escalate | Form submit | `hx-post=".../grievances/{id}/escalate/"` | `#escalate-result` | `innerHTML` | Toast |
| Raise CAPA | Form submit | `hx-post=".../grievances/raise-capa/"` | `#capa-result` | `innerHTML` | Toast + CAPA link |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
