# 05 — Mess Manager Dashboard

> **URL:** `/group/hostel/mess/`
> **File:** `05-mess-manager-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Mess / Cafeteria Manager (Role 71, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Mess / Cafeteria Manager. Covers food quality standards, weekly menu management, hygiene audit tracking, caterer/vendor contracts, mess fee monitoring, and nutritional compliance across all hostel mess halls in all branches. The Manager ensures that every hostel mess — from a 50-student rural branch to a 3,000-student city campus — meets the same food quality and hygiene standard.

Key operational cadence:
- **Daily:** Review yesterday's meal feedback logs and today's menu confirmation from each branch
- **Weekly:** Review upcoming weekly menus submitted by branch wardens; approve or request changes
- **Monthly:** Conduct or review hygiene audit scores for every mess; flag failing branches
- **Quarterly:** Review caterer performance and contract renewal status

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Mess Manager | G3 | Full — all branches, all mess sections | Exclusive dashboard |
| Group Hostel Director | G3 | View (mess summary on own dashboard) | Not this URL |
| Group Hostel Welfare Officer | G3 | View (mess hygiene on welfare panel) | Not this URL |
| Branch Mess Supervisor | Branch role | Report only — branch EduForge login | Separate branch portal |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Mess Manager Dashboard
```

### 3.2 Page Header
```
Welcome back, [Manager Name]              [Export Mess Report ↓]  [Add Quality Audit +]  [Settings ⚙]
Group Mess / Cafeteria Manager · AY [current academic year]
[N] Mess Halls Across [N] Branches · Avg Hygiene Score: [N]%
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Mess hygiene audit score < 60% at any branch | "HYGIENE FAIL: [Branch] mess scored [N]% in latest audit. Immediate corrective action required." | Red |
| Menu not submitted for upcoming week by branch | "[N] branches have not submitted next week's mess menu. Deadline: [date]." | Amber |
| Caterer contract expiring in ≤ 30 days | "Caterer contract at [Branch] expires in [N] days. Initiate renewal." | Amber |
| Food complaint Severity 1 (suspected food poisoning) | "CRITICAL: Food poisoning complaint at [Branch]. Suspend mess operations until investigation." | Red |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Mess Halls | Branches with active mess | Blue always | → Page 21 (vendor list) |
| Average Hygiene Score | Mean score across all branches (latest audit) | Green ≥ 80% · Yellow 60–80% · Red < 60% | → Page 20 |
| Failing Mess Halls | Branches with last audit score < 60% | Green = 0 · Red > 0 | → Page 20 (filtered: Fail) |
| Menus Approved (This Week) | Branches with weekly menu approved | Green = 100% · Yellow < 100% | → Page 19 |
| Food Complaints (Open) | Unresolved food quality complaints | Green = 0 · Yellow 1–5 · Red > 5 | → Page 22 (type: Food) |
| Contracts Expiring (30 days) | Caterer contracts expiring soon | Green = 0 · Amber > 0 | → Page 21 |

**HTMX:** `hx-trigger="every 10m"` → KPI auto-refresh.

---

## 5. Sections

### 5.1 Mess Health Matrix

> All mess halls with hygiene and operational metrics.

**Search:** Branch name, city, caterer name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches with mess |
| Hygiene | Radio | Any / Pass (≥ 60%) / Fail (< 60%) / Not Audited |
| Menu Status | Radio | Any / Approved / Pending / Overdue |
| Complaint Status | Checkbox | Has open food complaints |
| Caterer Contract | Checkbox | Expiring in 30 days |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → mess detail drawer |
| Capacity | ✅ | Meals per sitting |
| Caterer | ✅ | Vendor name |
| Last Hygiene Score | ✅ | % + Pass/Fail badge |
| Last Audit Date | ✅ | Date (red if > 30 days) |
| Menu This Week | ✅ | ✅ Approved / ⚠ Pending / ❌ Missing |
| Open Complaints | ✅ | Count |
| Caterer Contract Expires | ✅ | Date (amber if ≤ 30 days) |
| Actions | ❌ | View · New Audit · Review Menu |

**Default sort:** Last hygiene score ascending (worst first).

**Pagination:** Server-side · 25/page.

---

### 5.2 This Week's Menu Status

> Overview of which branches have their weekly menus approved.

**Display:** Card grid — 1 card per branch showing: Branch name · Days approved (Mon–Sun checkboxes) · Approval status · [Review →]

---

### 5.3 Hygiene Audit Trend Chart

**Chart — Branch Hygiene Scores (Last 6 months)**
- Multi-series line chart (top 5 best and 5 worst branches)
- X: Month. Y: Hygiene score %.
- Target line at 80% (group standard). Red zone below 60%.

---

### 5.4 Food Complaints Queue

> Unresolved food quality complaints from hostelers/wardens.

**Quick table:** Branch · Hosteler / Reporter · Complaint Type · Severity · Date · Status · [View →]

Complaint types: Food Quality / Foreign Object / Portion Size / Unhygienic / Suspected Contamination / Menu Not Followed.

"View All →" → Page 22 (filter: type = Food).

---

## 6. Drawers

### 6.1 Drawer: `mess-branch-detail`
- **Width:** 640px
- **Tabs:** Overview · Menu · Hygiene History · Vendor · Complaints
- **Menu tab:** Current week day-by-day menu (breakfast/lunch/dinner/snacks) with nutrition notes
- **Hygiene History:** Last 12 audits with scores, photos, corrective actions
- **Vendor tab:** Current caterer details, contract dates, payment status

### 6.2 Drawer: `mess-menu-create` (create/review weekly menu)
- **Trigger:** "Review Menu" button or Menu Manager page → + Create
- **Width:** 560px (see Page 19 — Mess Menu Manager for full spec)

### 6.3 Drawer: `quality-audit-create`
- **Trigger:** Mess Health Matrix → New Audit
- **Width:** 600px (see Page 20 — Mess Quality Audit for full spec)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Menu approved | "Weekly menu for [Branch] approved." | Success | 4s |
| Menu change requested | "Menu revision requested for [Branch]. Warden notified." | Info | 4s |
| Audit submitted | "Hygiene audit for [Branch] submitted. Score: [N]%." | Success | 4s |
| Audit failed alert | "HYGIENE FAIL at [Branch] — score [N]%. Hostel Director notified." | Warning | 6s |
| Food complaint logged | "Food complaint logged for [Branch]." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No mess halls configured | "No Mess Halls Found" | "No mess halls configured for this group." | [Contact IT Admin] |
| All hygiene scores passing | "All Mess Halls Passing Hygiene Standards" | "Every branch scored ≥ 60% in the latest audit." | [View Audit Records →] |
| All menus approved | "All Branch Menus Approved This Week" | — | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + mess table (8 rows) + menu status grid + chart placeholder |
| Table filter/search | Inline skeleton rows |
| KPI auto-refresh | Shimmer on card values |
| Audit drawer submit | Spinner on Submit; table row refreshes |

---

## 10. Role-Based UI Visibility

| Element | Mess Manager G3 | Hostel Director G3 | Welfare Officer G3 |
|---|---|---|---|
| Create New Audit | ✅ | ✅ | ❌ |
| Approve Menu | ✅ | ✅ | ❌ |
| View Complaints | ✅ | ✅ | ✅ (read-only) |
| Edit Vendor Contract | ✅ | ❌ | ❌ |
| Export Report | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/mess/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/mess/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/mess/branches/` | JWT (G3+) | Mess health table |
| GET | `/api/v1/group/{group_id}/hostel/mess/branches/{id}/detail/` | JWT (G3+) | Branch detail drawer |
| GET | `/api/v1/group/{group_id}/hostel/mess/menus/this-week/` | JWT (G3+) | Weekly menu status |
| POST | `/api/v1/group/{group_id}/hostel/mess/menus/{id}/approve/` | JWT (G3+) | Approve branch menu |
| POST | `/api/v1/group/{group_id}/hostel/mess/menus/{id}/request-revision/` | JWT (G3+) | Request menu change |
| GET | `/api/v1/group/{group_id}/hostel/mess/hygiene-trends/` | JWT (G3+) | 6-month hygiene trend |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 10m` | GET `.../mess/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Mess table search | `input delay:300ms` | GET `.../mess/branches/?q={val}` | `#mess-table-body` | `innerHTML` |
| Menu status grid | `load` | GET `.../mess/menus/this-week/` | `#menu-grid` | `innerHTML` |
| Approve menu | `click` | POST `.../menus/{id}/approve/` | `#menu-card-{id}` | `outerHTML` |
| Open branch detail | `click` | GET `.../mess/branches/{id}/detail/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
