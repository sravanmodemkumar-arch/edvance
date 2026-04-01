# 01 — Child Protection Officer Dashboard

> **URL:** `/group/welfare/child-protection/`
> **File:** `01-child-protection-officer-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Child Protection Officer (Role 90, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Child Protection Officer. Single-screen command centre for child safety and POCSO (Protection of Children from Sexual Offences) compliance across all branches — open POCSO complaints and their stage in the mandated 90-day resolution cycle, staff POCSO training completion rates, ICC (Internal Complaints Committee) composition status at every branch, NCPCR mandatory report submissions, child safety policy acknowledgment, and welfare incidents flagged with child safety markers.

The Child Protection Officer owns child safety policy group-wide. They handle every POCSO complaint through the four-stage resolution pipeline (Filed → Acknowledged → Investigation → Finding → Closure), ensure every branch has a lawfully constituted ICC as required under POCSO Section 19, submit annual mandatory reports to NCPCR (National Commission for Protection of Child Rights), and drive 100% staff awareness on child protection obligations. Any POCSO complaint that crosses the 90-day window, any branch that lacks an ICC, or any overdue NCPCR report creates both legal liability and child welfare risk. The dashboard surfaces these gaps immediately upon login.

Scale: 20–50 branches · 1–5 POCSO complaints/year · 3,000–10,000 staff requiring POCSO training · annual NCPCR compliance cycle.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Child Protection Officer | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group Chairman / CEO | G5 / G4 | View — POCSO compliance summary via governance report only | Not this URL |
| Group COO | G4 | View — complaint status and escalation section only | Read-only |
| Branch Principal | G2 | View — own branch ICC and complaint status only | Branch-scoped view, not this URL |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('child_protection_officer')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Child Protection Officer Dashboard
```

### 3.2 Page Header
```
Welcome back, [Officer Name]                  [Export Compliance Report ↓]  [Settings ⚙]
[Group Name] — Group Child Protection Officer · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  [N] Open Complaints  ·  NCPCR Reports: [N] Submitted
```

### 3.3 Alert Banner (conditional — critical items requiring same-day action)

| Condition | Banner Text | Severity |
|---|---|---|
| POCSO complaint overdue > 90 days | "POCSO complaint [ID] at [Branch] has exceeded the 90-day statutory resolution window. Immediate action required." | Red |
| ICC not constituted at a branch | "[N] branch(es) have no constituted ICC: [Branch list]. Legal non-compliance — constitute immediately." | Red |
| NCPCR report overdue | "NCPCR mandatory report for [period] is overdue. Submission deadline was [date]." | Red |
| POCSO complaint in investigation > 60 days | "Complaint [ID] has been in Investigation stage for [N] days. Review progress before 90-day deadline." | Amber |
| Staff POCSO training < 80% at any branch | "[Branch] has only [N]% POCSO training compliance. Mandatory training drive required." | Amber |

Max 5 alerts visible. Alert links route to the relevant section or complaint record. "View all compliance events → POCSO Audit Log" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| POCSO Complaint Compliance % | % of open complaints on-track within 90-day statutory window | Green ≥ 90% · Yellow 60–89% · Red < 60% | → Section 5.2 |
| Open POCSO Complaints | Total active complaints across all branches | Green = 0 · Yellow 1–2 · Red > 2 | → Section 5.2 |
| POCSO Training Compliance % | Staff trained this academic year as % of total staff | Green ≥ 95% · Yellow 80–94% · Red < 80% | → Section 5.3 |
| Branches with ICC Constituted | Branches with a lawfully constituted ICC / total branches | Green = all branches · Red if any branch missing | → Section 5.1 |
| NCPCR Reports Submitted This Year | Count of reports submitted to NCPCR in current AY | Blue always (informational) | → Section 5.1 |
| NCPCR Reports Overdue | Reports due but not yet submitted | Green = 0 · Red if any overdue | → Section 5.1 |
| Child Safety Policy Acknowledgment % | Staff who have digitally acknowledged the policy this AY | Green ≥ 95% · Yellow < 95% | → Section 5.1 |
| Branches with Zero POCSO Training This Year | Branches where no staff have completed POCSO training this AY | Green = 0 · Red if any | → Section 5.3 |

**HTMX:** `hx-trigger="every 5m"` → Open POCSO Complaints and NCPCR Reports Overdue auto-refresh.

---

## 5. Sections

### 5.1 Branch POCSO Compliance Matrix

> Per-branch overview of all four POCSO compliance dimensions — Coordinator's primary audit table.

**Search:** Branch name, city, zone. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| ICC Status | Checkbox | Constituted / Not Constituted / Expired |
| Training Compliance | Radio | All / ≥ 95% / 80–94% / < 80% |
| NCPCR Report Status | Checkbox | Submitted / Overdue / Not Due |
| Open Complaints | Checkbox | Show branches with open complaints only |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → `branch-pocso-detail` drawer |
| ICC Status | ✅ | Constituted ✅ / Not Constituted ❌ / Expired ⚠ |
| ICC Last Renewed | ✅ | Date; Red if > 2 years ago |
| Training Compliance % | ✅ | Colour: Green ≥ 95% · Yellow 80–94% · Red < 80% |
| Open Complaints | ✅ | Count; Red if > 0 |
| Last NCPCR Report Date | ✅ | Date or — if none submitted |
| Policy Acknowledgment % | ✅ | % of branch staff who signed this AY |
| Actions | ❌ | View · Submit Report · Send Training Reminder |

**Default sort:** ICC Status (Not Constituted first), then Training Compliance ascending.
**Pagination:** Server-side · 25/page.

---

### 5.2 Open Complaints Tracker

> All active POCSO complaints across every branch, with stage progress and SLA countdown.

**Search:** Complaint ID, branch, stage. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Stage | Checkbox | Filed / Acknowledged / Investigation / Finding / Closure |
| SLA Status | Radio | All / On Track / At Risk (> 60 days) / Overdue (> 90 days) |
| Days Open | Radio | All / < 30 days / 30–60 days / 60–90 days / > 90 days |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Complaint ID | ✅ | System-generated; link → `complaint-quick-view` drawer |
| Branch | ✅ | |
| Date Filed | ✅ | Date of complaint registration |
| Stage | ✅ | Colour-coded stage badge: Filed (Grey) → Acknowledged (Blue) → Investigation (Amber) → Finding (Orange) → Closure (Green) |
| Days Open | ✅ | Red if > 90 · Orange if 60–90 · Green if < 60 |
| SLA Status | ✅ | On Track ✅ / At Risk ⚠ / Overdue ❌ |
| Assigned ICC Member | ✅ | Name of presiding officer |
| Last Activity | ✅ | Date of most recent stage change or note |
| Actions | ❌ | View · Update Stage · Escalate |

**Default sort:** Days Open descending (most overdue first).
**Pagination:** Server-side · 25/page.

---

### 5.3 Training Compliance Chart

> Visual representation of POCSO training completion across all branches and group-wide totals.

**Display:** Two charts rendered side-by-side on desktop, stacked on mobile.

**Chart 1 — Bar Chart (branch-wise):**
- X-axis: Branch names (abbreviated)
- Y-axis: Training completion % (0–100)
- Colour bands: Green fill ≥ 95% · Yellow fill 80–94% · Red fill < 80%
- Tooltip: Branch name · Trained count · Total staff · Completion %
- Click on bar → opens `branch-pocso-detail` drawer at Training tab

**Chart 2 — Pie Chart (group-wide):**
- Segments: Trained (Green) vs Untrained (Red)
- Centre label: "[N]% Group-wide compliance"
- Legend: Trained: [N] staff · Untrained: [N] staff

"View full training log →" links to staff training registry filtered to POCSO training category.

---

### 5.4 Quick Actions

| Action | Target |
|---|---|
| New Complaint | Opens complaint registration form modal |
| View ICC Registry | → `/group/welfare/pocso/icc-registry/` — ICC composition across all branches (Page 29) |
| Submit NCPCR Report | → NCPCR report submission form |
| Export Compliance Report | Download CSV/XLSX — all branches, all dimensions, current AY |
| View Policy Library | → Child safety policy document library |

---

## 6. Drawers / Modals

### 6.1 Drawer: `branch-pocso-detail`
- **Trigger:** Branch name link in Section 5.1 table
- **Width:** 640px
- **Tabs:** ICC Composition · Training · Open Complaints · NCPCR Reports · Policy Acknowledgments

**ICC Composition tab:**
- Committee name, constitution date, last renewal date, total members, chairperson name and designation
- Member list: Name · Role · Designation · Type (Internal / External / NGO Representative) · Date Appointed · Status (Active / Expired)
- Warning badge if composition does not meet POCSO Section 4 minimum requirements (must include one external member from NGO or legal background)

**Training tab:**
- Total staff at branch, trained count, untrained count, completion %
- Training sessions held this AY: Date · Trainer · Mode (In-person / Online) · Attendees
- Untrained staff list: Name · Department · Last training date or — Never

**Open Complaints tab:**
- Complaint ID · Date Filed · Current Stage · Days Open · SLA Status · Assigned Member
- Each row links to `complaint-quick-view` drawer

**NCPCR Reports tab:**
- Report period · Due date · Submitted date · Submission reference number · Status (Submitted / Overdue / Not Due)

**Policy Acknowledgments tab:**
- Policy version · Acknowledgment period · Branch acknowledgment % · Unacknowledged staff list (Name · Department · Last reminded)

---

### 6.2 Drawer: `complaint-quick-view`
- **Trigger:** Complaint ID link in Section 5.2 table or from `branch-pocso-detail` Open Complaints tab
- **Width:** 560px
- **Mode:** Read-only summary

**Content:**
| Field | Notes |
|---|---|
| Complaint ID | System-generated |
| Branch | |
| Date Filed | |
| Complainant Type | Student / Parent / Staff / Anonymous |
| Nature of Complaint | Category per POCSO provisions — display-only |
| Current Stage | Stage badge |
| Stage History | Timeline: stage name · entered date · entered by · days in stage |
| ICC Member Assigned | Name · Contact |
| Days Open | With colour coding |
| SLA Status | On Track / At Risk / Overdue badge |
| Last Activity Note | Latest case note — date, note text |

- Footer: "View Full Record →" button → redirects to the full complaint management page (external to this dashboard)
- "Update Stage" button visible only to Child Protection Officer (G3)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Complaint stage updated | "Complaint [ID] moved to [Stage] stage." | Success | 4s |
| Complaint registered | "New POCSO complaint [ID] registered at [Branch]." | Success | 4s |
| NCPCR report submitted | "NCPCR report for [period] submitted successfully." | Success | 5s |
| Training reminder sent | "POCSO training reminder sent to [N] untrained staff at [Branch]." | Info | 4s |
| Complaint escalated | "Complaint [ID] escalated to Group COO." | Warning | 6s |
| Compliance report exported | "Compliance report export prepared. Download ready." | Info | 4s |
| ICC record updated | "ICC composition updated for [Branch]." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open POCSO complaints | "No Open POCSO Complaints" | "All POCSO complaints across all branches are resolved. Group is compliant." | — |
| No branches configured | "No Branches Found" | "No branches are configured in the welfare system yet." | [Add Branch] |
| No NCPCR reports due | "No NCPCR Reports Due" | "All mandatory NCPCR reports for this period have been submitted." | — |
| Search returns no results | "No Results Found" | "No branches or complaints match your search or filters." | [Clear Filters] |
| All branches training-compliant | "POCSO Training Fully Compliant" | "All branches have ≥ 95% POCSO training completion for this academic year." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + compliance matrix table (15 rows × 8 columns) + complaints table + charts + alerts |
| Table filter/search | Inline skeleton rows (8 rows) |
| KPI auto-refresh | Shimmer on individual card values only; labels preserved |
| Chart load | Chart area skeleton (grey rectangle with animated gradient) |
| Branch detail drawer open | 640px drawer skeleton; each tab loads lazily on first click |
| Complaint quick-view drawer open | 560px drawer skeleton with timeline skeleton (5 rows) |

---

## 10. Role-Based UI Visibility

| Element | Child Protection Officer G3 | Group COO G4 | Chairman / CEO G5 | Branch Principal G2 |
|---|---|---|---|---|
| View All Branches | ✅ | ✅ | ✅ | Own branch only |
| Register New Complaint | ✅ | ❌ | ❌ | ❌ |
| Update Complaint Stage | ✅ | ❌ | ❌ | ❌ |
| Escalate Complaint | ✅ | ❌ | ❌ | ❌ |
| Submit NCPCR Report | ✅ | ❌ | ❌ | ❌ |
| View Complaint Details | ✅ | ✅ (summary) | ✅ (summary) | Own branch only |
| Send Training Reminder | ✅ | ❌ | ❌ | ❌ |
| Export Compliance Report | ✅ | ✅ | ✅ | ❌ |
| Edit ICC Composition | ✅ | ❌ | ❌ | ❌ |
| View Policy Library | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/child-protection/dashboard/` | JWT (G3+) | Full dashboard data payload |
| GET | `/api/v1/group/{group_id}/welfare/child-protection/kpi-cards/` | JWT (G3+) | KPI auto-refresh values |
| GET | `/api/v1/group/{group_id}/welfare/child-protection/branch-matrix/` | JWT (G3+) | Branch POCSO compliance matrix |
| GET | `/api/v1/group/{group_id}/welfare/child-protection/complaints/` | JWT (G3+) | Open complaints list; params: `stage`, `sla_status`, `branch_id`, `days_open_gt`, `page` |
| POST | `/api/v1/group/{group_id}/welfare/child-protection/complaints/` | JWT (G3) | Register new POCSO complaint |
| GET | `/api/v1/group/{group_id}/welfare/child-protection/complaints/{complaint_id}/` | JWT (G3+) | Single complaint detail |
| PATCH | `/api/v1/group/{group_id}/welfare/child-protection/complaints/{complaint_id}/stage/` | JWT (G3) | Advance complaint to next stage |
| POST | `/api/v1/group/{group_id}/welfare/child-protection/complaints/{complaint_id}/escalate/` | JWT (G3) | Escalate complaint to COO |
| GET | `/api/v1/group/{group_id}/welfare/child-protection/training/` | JWT (G3+) | Training compliance data; params: `branch_id` |
| POST | `/api/v1/group/{group_id}/welfare/child-protection/training/remind/` | JWT (G3) | Send training reminder to untrained staff |
| GET | `/api/v1/group/{group_id}/welfare/branches/{branch_id}/pocso-detail/` | JWT (G3+) | Branch POCSO detail drawer payload |
| POST | `/api/v1/group/{group_id}/welfare/child-protection/ncpcr-reports/` | JWT (G3) | Submit NCPCR report |
| GET | `/api/v1/group/{group_id}/welfare/child-protection/export/` | JWT (G3+) | Async compliance report export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../child-protection/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch matrix search | `input delay:300ms` | GET `.../child-protection/branch-matrix/?q={val}` | `#branch-matrix-body` | `innerHTML` |
| Branch matrix filter | `click` | GET `.../child-protection/branch-matrix/?{filters}` | `#branch-matrix-section` | `innerHTML` |
| Branch matrix pagination | `click` | GET `.../child-protection/branch-matrix/?page={n}` | `#branch-matrix-section` | `innerHTML` |
| Complaints table search | `input delay:300ms` | GET `.../child-protection/complaints/?q={val}` | `#complaints-table-body` | `innerHTML` |
| Complaints filter | `click` | GET `.../child-protection/complaints/?{filters}` | `#complaints-section` | `innerHTML` |
| Open branch drawer | `click` on branch name | GET `.../welfare/branches/{id}/pocso-detail/` | `#drawer-body` | `innerHTML` |
| Open complaint drawer | `click` on complaint ID | GET `.../child-protection/complaints/{id}/` | `#drawer-body` | `innerHTML` |
| Advance complaint stage | `click` | PATCH `.../child-protection/complaints/{id}/stage/` | `#complaint-row-{id}` | `outerHTML` |
| Escalate complaint | `click` | POST `.../child-protection/complaints/{id}/escalate/` | `#complaint-row-{id}` | `outerHTML` |
| Training chart load | `load` | GET `.../child-protection/training/` | `#training-chart-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
