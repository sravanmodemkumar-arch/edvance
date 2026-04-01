# 02 — Anti-Ragging Committee Dashboard

> **URL:** `/group/welfare/anti-ragging/`
> **File:** `02-anti-ragging-committee-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Anti-Ragging Committee Head (Role 91, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Anti-Ragging Committee Head. Command centre for anti-ragging policy and UGC regulatory compliance across all branches — open anti-ragging complaints through their investigation lifecycle, UGC-mandated affidavit collection from students and parents at the start of every academic year, complaint committee constitution at every branch, awareness program delivery, and penalty and resolution outcomes.

The Group Anti-Ragging Committee Head is the single point of accountability for UGC Anti-Ragging Regulations 2009 compliance across the entire group. They own anti-ragging policy, coordinate investigations ensuring the mandated 7-day preliminary inquiry and 30-day full investigation cycle are met, ensure UGC-mandated affidavits are collected from 100% of students and parents at admission and at the start of every new academic year, monitor awareness program delivery at every branch, and liaise with branch principals on prevention. Any branch missing its complaint committee, any preliminary inquiry exceeding 7 days, or any affidavit collection falling below 90% constitutes a regulatory breach. The dashboard makes all gaps visible in one screen.

Scale: 20–50 branches · 0–10 anti-ragging complaints/year · 20,000–1,00,000 student affidavits per year · 100% parent affidavit collection mandatory.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Anti-Ragging Committee Head | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group COO | G4 | View — complaints and UGC compliance score only | Read-only |
| Group Chairman / CEO | G5 / G4 | View — via governance reports only | Not this URL |
| Branch Principal | G2 | View — own branch committee status and complaints only | Branch-scoped, not this URL |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('anti_ragging_committee_head')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Welfare & Safety  ›  Anti-Ragging Committee Dashboard
```

### 3.2 Page Header
```
Welcome back, [Head Name]                    [Export UGC Report ↓]  [Settings ⚙]
[Group Name] — Group Anti-Ragging Committee Head · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  [N] Open Complaints  ·  Affidavits: [N]% Collected
```

### 3.3 Alert Banner (conditional — critical items requiring same-day action)

| Condition | Banner Text | Severity |
|---|---|---|
| Preliminary inquiry overdue > 7 days | "Complaint [ID] at [Branch]: preliminary inquiry has exceeded the 7-day UGC mandate. Immediate action required." | Red |
| Full investigation overdue > 30 days | "Complaint [ID] at [Branch]: full investigation has exceeded the 30-day UGC mandate. Escalate immediately." | Red |
| Branch missing complaint committee | "[N] branch(es) have no constituted anti-ragging committee: [Branch list]. Constitute immediately — UGC non-compliance." | Red |
| Affidavit collection < 90% at any branch | "[Branch] student affidavit collection is only [N]%. Minimum 90% required before classes commence." | Amber |
| Parent affidavit collection < 95% | "[Branch] parent affidavit collection is [N]%. Drive required to reach compliance." | Amber |

Max 5 alerts visible. Alert links route to relevant section or complaint record. "View all compliance events → Anti-Ragging Audit Log" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Anti-Ragging Complaints | Total active complaints across all branches | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.2 |
| Complaints Resolved Within 30 Days % | Closed complaints that met the 30-day investigation window, this AY | Green ≥ 90% · Red < 75% | → Section 5.4 |
| Student Affidavit Collection % | Students who have submitted signed affidavits, group-wide | Green ≥ 98% · Yellow 90–97% · Red < 90% | → Section 5.3 |
| Parent Affidavit Collection % | Parents who have submitted signed affidavits, group-wide | Green ≥ 98% · Yellow < 98% | → Section 5.3 |
| Branches with Committee Constituted | Branches with a validly constituted anti-ragging committee / total | Green = all · Red if any branch missing | → Section 5.1 |
| Awareness Programs This Year | Count of awareness sessions conducted across all branches this AY | Blue always (informational) | → Section 5.1 |
| Complaints Under Investigation | Complaints currently in preliminary inquiry or full investigation stage | Green = 0 · Amber if any | → Section 5.2 |
| UGC Compliance Score % | Composite score: committee constitution + affidavit collection + timely resolution + programs | Green ≥ 90% · Yellow 70–89% · Red < 70% | → Section 5.1 |

**HTMX:** `hx-trigger="every 5m"` → Open Complaints and Complaints Under Investigation auto-refresh.

---

## 5. Sections

### 5.1 Branch Compliance Matrix

> Per-branch summary of all UGC anti-ragging compliance dimensions.

**Search:** Branch name, city, zone. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Committee Status | Checkbox | Constituted / Not Constituted / Expired |
| Student Affidavit % | Radio | All / ≥ 98% / 90–97% / < 90% |
| Parent Affidavit % | Radio | All / ≥ 98% / < 98% |
| Programs Conducted | Checkbox | Show branches with zero programs only |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → `branch-anti-ragging-detail` drawer |
| Committee Status | ✅ | Constituted ✅ / Not Constituted ❌ / Expired ⚠ |
| Committee Last Renewed | ✅ | Date; Red if > 1 year |
| Student Affidavit % | ✅ | Colour: Green ≥ 98% · Yellow 90–97% · Red < 90% |
| Parent Affidavit % | ✅ | Colour: Green ≥ 98% · Yellow < 98% |
| Open Complaints | ✅ | Count; Red if > 0 |
| Awareness Programs This AY | ✅ | Count; Amber if 0 |
| UGC Score % | ✅ | Composite; colour-coded badge |
| Actions | ❌ | View · Send Affidavit Reminder · Add Program |

**Default sort:** Committee Status (Not Constituted first), then UGC Score ascending.
**Pagination:** Server-side · 25/page.

---

### 5.2 Active Complaints Tracker

> All open anti-ragging complaints across every branch with stage progress and UGC timeline compliance.

**Search:** Complaint ID, branch, complaint type. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Stage | Checkbox | Received / Preliminary Inquiry / Full Investigation / Finding / Closure |
| SLA Status | Radio | All / On Track / At Risk / Overdue |
| Complaint Type | Checkbox | Physical / Verbal / Cyber / Sexual / Economic / Other |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Complaint ID | ✅ | System-generated; link → `complaint-summary` drawer |
| Branch | ✅ | |
| Date Received | ✅ | |
| Complaint Type | ✅ | Badge |
| Stage | ✅ | Colour-coded: Received (Grey) · Preliminary Inquiry (Blue) · Full Investigation (Amber) · Finding (Orange) · Closure (Green) |
| Days Elapsed | ✅ | Total days from receipt; Red if > 30 · Orange if 21–30 · Green if < 21 |
| Inquiry Days Used | ✅ | Days in preliminary inquiry stage; Red if > 7 |
| SLA Status | ✅ | On Track ✅ / At Risk ⚠ / Overdue ❌ traffic light |
| Presiding Officer | ✅ | Name of committee member leading inquiry |
| Actions | ❌ | View · Update Stage · Escalate |

**Default sort:** Days Elapsed descending (most overdue first).
**Pagination:** Server-side · 25/page.

---

### 5.3 Affidavit Collection Chart

> Visual breakdown of student and parent affidavit collection per branch with group-wide totals.

**Display:** Two charts side-by-side on desktop, stacked on mobile.

**Chart 1 — Bar Chart (branch-wise, dual series):**
- X-axis: Branch names
- Y-axis: Collection % (0–100)
- Series: Student Affidavit % (solid bar) + Parent Affidavit % (outline bar)
- Colour: Green ≥ 98% · Yellow 90–97% · Red < 90%
- Tooltip: Branch · Student collected / enrolled · Parent collected / enrolled · %
- Click bar → `branch-anti-ragging-detail` drawer at Affidavits tab

**Chart 2 — Pie Chart (group-wide):**
- Segment 1: Students with affidavit (Green)
- Segment 2: Students without affidavit (Red)
- Centre: "[N]% Group Student Compliance"
- Below: Parent affidavit summary as text stat

"View affidavit register →" links to full affidavit collection register for bulk download.

---

### 5.4 Recent Resolutions

> Last 10 closed anti-ragging complaints — outcomes, penalties imposed, and days taken to resolve.

**Columns:** Complaint ID · Branch · Closed Date · Complaint Type · Days Taken · SLA Met (✅ / ❌) · Outcome (Warning / Suspension / Expulsion / Acquitted / Referred to Police / Withdrawn) · Penalty Details

**Default sort:** Closed Date descending.
**No pagination** — fixed 10-row view. "View all closed complaints →" links to full history.

---

## 6. Drawers / Modals

### 6.1 Drawer: `branch-anti-ragging-detail`
- **Trigger:** Branch name link in Section 5.1 table
- **Width:** 640px
- **Tabs:** Committee · Complaints · Affidavits · Programs

**Committee tab:**
- Committee name, constitution date, last renewal, total members, chairperson
- Member list: Name · Designation · Type (Teaching Staff / Non-Teaching / Student Representative / External) · Date Appointed · Status
- Warning badge if composition does not meet UGC minimum (must include student representative and external member)

**Complaints tab:**
- All complaints for this branch: Complaint ID · Stage · Days Elapsed · SLA Status · Presiding Officer
- Each row links to `complaint-summary` drawer

**Affidavits tab:**
- Academic year selector
- Student affidavit: Collected / Total enrolled / % / Pending list (Name · Class · Contact)
- Parent affidavit: Collected / Total parents / % / Pending list
- [Send Reminder] button → bulk SMS/email to pending parents and students

**Programs tab:**
- Awareness programs this AY: Date · Type (Orientation / Workshop / Video / Guest Lecture) · Audience · Attendee count · Facilitator
- [Add Program] button

---

### 6.2 Drawer: `complaint-summary`
- **Trigger:** Complaint ID link in Section 5.2 table or from `branch-anti-ragging-detail` Complaints tab
- **Width:** 560px
- **Mode:** Read-only summary

**Content:**
| Field | Notes |
|---|---|
| Complaint ID | System-generated |
| Branch | |
| Date Received | |
| Complaint Type | Category badge |
| Complainant Type | Student / Staff / Anonymous / Parent |
| Nature of Ragging | Brief description — display-only |
| Current Stage | Stage badge |
| Stage History | Timeline: stage · entered date · entered by · days in stage |
| Presiding Officer | Name · Contact |
| Days Elapsed | With colour coding |
| SLA Status | On Track / At Risk / Overdue badge |
| Last Activity Note | Latest update — date, note text |

- Footer: "View Full Record →" button → full complaint management page
- "Update Stage" button visible only to Anti-Ragging Committee Head (G3)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Complaint stage updated | "Complaint [ID] moved to [Stage] stage at [Branch]." | Success | 4s |
| Complaint escalated | "Complaint [ID] escalated to Group COO." | Warning | 6s |
| Affidavit reminder sent | "Affidavit collection reminder sent to [N] pending students/parents at [Branch]." | Info | 4s |
| Awareness program added | "Awareness program recorded for [Branch] on [date]." | Success | 4s |
| UGC report exported | "UGC compliance report export prepared. Download ready." | Info | 4s |
| Committee record updated | "Anti-ragging committee updated for [Branch]." | Success | 4s |
| Bulk affidavit reminder sent | "Bulk reminder sent to [N] branches with affidavit shortfall." | Info | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open complaints | "No Open Anti-Ragging Complaints" | "All anti-ragging complaints across all branches are resolved. Group is UGC compliant." | — |
| No branches configured | "No Branches Found" | "No branches are configured in the welfare system." | [Add Branch] |
| All affidavits collected | "Affidavit Collection 100% Complete" | "All students and parents have submitted signed affidavits for this academic year." | — |
| Search returns no results | "No Results Found" | "No branches or complaints match your search or filters." | [Clear Filters] |
| No programs recorded | "No Awareness Programs Recorded" | "No awareness programs have been logged for this academic year. Record the first program." | [Add Program] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + compliance matrix table (15 rows × 9 columns) + complaints table + charts + alerts |
| Table filter/search | Inline skeleton rows (8 rows) |
| KPI auto-refresh | Shimmer on individual card values; labels preserved |
| Affidavit chart load | Chart area skeleton with animated gradient |
| Branch detail drawer open | 640px drawer skeleton; tabs load lazily on first click |
| Complaint summary drawer open | 560px drawer skeleton with timeline (5 rows) |

---

## 10. Role-Based UI Visibility

| Element | Anti-Ragging Head G3 | Group COO G4 | Chairman / CEO G5 | Branch Principal G2 |
|---|---|---|---|---|
| View All Branches | ✅ | ✅ | ✅ | Own branch only |
| Update Complaint Stage | ✅ | ❌ | ❌ | ❌ |
| Escalate Complaint | ✅ | ❌ | ❌ | ❌ |
| Send Affidavit Reminder | ✅ | ❌ | ❌ | ❌ |
| Add Awareness Program | ✅ | ❌ | ❌ | ✅ (own branch) |
| Edit Committee Composition | ✅ | ❌ | ❌ | ❌ |
| View Complaint Details | ✅ | ✅ (summary) | ✅ (summary) | Own branch only |
| Export UGC Report | ✅ | ✅ | ✅ | ❌ |
| View Affidavit Register | ✅ | ✅ | ✅ | Own branch only |
| Delete Complaint Record | ❌ (no deletion) | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/welfare/anti-ragging/dashboard/` | JWT (G3+) | Full dashboard data payload |
| GET | `/api/v1/group/{group_id}/welfare/anti-ragging/kpi-cards/` | JWT (G3+) | KPI auto-refresh values |
| GET | `/api/v1/group/{group_id}/welfare/anti-ragging/branch-matrix/` | JWT (G3+) | Branch compliance matrix; params: `branch_id`, `committee_status`, `page` |
| GET | `/api/v1/group/{group_id}/welfare/anti-ragging/complaints/` | JWT (G3+) | Active complaints list; params: `stage`, `sla_status`, `complaint_type`, `branch_id`, `page` |
| PATCH | `/api/v1/group/{group_id}/welfare/anti-ragging/complaints/{complaint_id}/stage/` | JWT (G3) | Advance complaint stage |
| POST | `/api/v1/group/{group_id}/welfare/anti-ragging/complaints/{complaint_id}/escalate/` | JWT (G3) | Escalate to COO |
| GET | `/api/v1/group/{group_id}/welfare/anti-ragging/complaints/{complaint_id}/` | JWT (G3+) | Single complaint detail |
| GET | `/api/v1/group/{group_id}/welfare/anti-ragging/affidavits/` | JWT (G3+) | Affidavit collection data; params: `branch_id`, `type` (student/parent) |
| POST | `/api/v1/group/{group_id}/welfare/anti-ragging/affidavits/remind/` | JWT (G3) | Send affidavit reminder; body: `branch_id`, `type` |
| GET | `/api/v1/group/{group_id}/welfare/branches/{branch_id}/anti-ragging-detail/` | JWT (G3+) | Branch detail drawer payload |
| POST | `/api/v1/group/{group_id}/welfare/anti-ragging/programs/` | JWT (G3) | Log new awareness program |
| GET | `/api/v1/group/{group_id}/welfare/anti-ragging/resolutions/recent/` | JWT (G3+) | Last 10 closed complaints |
| GET | `/api/v1/group/{group_id}/welfare/anti-ragging/export/` | JWT (G3+) | Async UGC compliance report export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../anti-ragging/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch matrix search | `input delay:300ms` | GET `.../anti-ragging/branch-matrix/?q={val}` | `#branch-matrix-body` | `innerHTML` |
| Branch matrix filter | `click` | GET `.../anti-ragging/branch-matrix/?{filters}` | `#branch-matrix-section` | `innerHTML` |
| Branch matrix pagination | `click` | GET `.../anti-ragging/branch-matrix/?page={n}` | `#branch-matrix-section` | `innerHTML` |
| Complaints search | `input delay:300ms` | GET `.../anti-ragging/complaints/?q={val}` | `#complaints-table-body` | `innerHTML` |
| Complaints filter | `click` | GET `.../anti-ragging/complaints/?{filters}` | `#complaints-section` | `innerHTML` |
| Open branch drawer | `click` on branch name | GET `.../welfare/branches/{id}/anti-ragging-detail/` | `#drawer-body` | `innerHTML` |
| Open complaint drawer | `click` on complaint ID | GET `.../anti-ragging/complaints/{id}/` | `#drawer-body` | `innerHTML` |
| Advance complaint stage | `click` | PATCH `.../anti-ragging/complaints/{id}/stage/` | `#complaint-row-{id}` | `outerHTML` |
| Affidavit chart load | `load` | GET `.../anti-ragging/affidavits/` | `#affidavit-chart-section` | `innerHTML` |
| Send affidavit reminder | `click` | POST `.../anti-ragging/affidavits/remind/` | `#reminder-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
