# Home Page: Group 2 — Institution Group Portal
**Route:** `[group-slug].eduforge.in/home` or `www.institutiongroup.com/home`
**Domain:** Custom domain (e.g., `www.narayana-group.ac.in`) or EduForge subdomain
**Access:** Group 2 roles — Chain owners, Zone heads, Group admins
**Portal type:** Multi-institution management — oversees all branches

---

## Overview

| Property | Value |
|---|---|
| Purpose | Command center for institution groups/chains managing 5–500+ branches |
| Who sees it | Chain directors, zone managers, group admins, finance heads |
| Key difference | This portal is ABOVE individual schools/coaching — aggregate view across ALL branches |
| Example users | Narayana Group Director seeing all 200+ branches, SR Group COO |

---

## Role-Based Home View Matrix

| Role | What They See on Home |
|---|---|
| Group Chairman / Owner | Revenue P&L across all branches, enrollment trends, top/bottom branches |
| Group CEO / COO | Operational KPIs — attendance, fee collection, exam performance, staff BGV |
| Zone Manager | Only their zone's branches (e.g., Hyderabad Zone: 15 branches) |
| Group Academic Director | Academic performance across all branches, exam results, content quality |
| Group Finance Head | Fee collection, outstanding dues, Razorpay settlements per branch |
| Group HR Manager | Staff headcount, BGV status, vacancies across all branches |
| Group IT Admin | Portal health, user counts, API usage, subscription status per branch |
| Franchise Manager | Franchise branches only — their territory |

---

## Page Sections

| # | Section | Visible To | Purpose |
|---|---|---|---|
| 1 | Top Navigation | All | Group portal nav with group logo |
| 2 | Sidebar | All | Module navigation — role filtered |
| 3 | Group KPI Bar | All (role-filtered) | Aggregate numbers across all branches |
| 4 | Alert Banner | All | Critical issues across the group |
| 5 | Branch Performance Map | CEO / Zone Mgr | Geographic + performance view |
| 6 | Branch Cards Grid | All | Individual branch summary cards |
| 7 | Comparative Analytics | Director / COO | Branch vs branch comparison charts |
| 8 | Quick Actions | Role-specific | Shortcuts to most-used actions |
| 9 | Recent Activity | All | Group-level event feed |

---

## Section 1 — Top Navigation

→ Component: [06-navigation.md](../components/06-navigation.md)

| Element | Spec |
|---|---|
| Logo | Group/chain logo (e.g., Narayana Group logo) — not individual branch logo |
| Portal name | "[Group Name] — Group Portal" |
| Branch switcher | Dropdown: "All Branches ▼" or "Switch to Branch [Branch Name]" — click goes to that branch portal |
| Global search | Searches across ALL branches: students, staff, exams, fees |
| Notifications | Group-level alerts (BGV breach across group, exam failures, subscription issues) |

---

## Section 2 — Sidebar Navigation

| Nav Item | Min Role | What It Shows |
|---|---|---|
| 🏠 Dashboard | All | Home page |
| 🏫 Branches | All | All branches list — zone filtered for Zone Mgrs |
| 📊 Analytics | Director / COO | Cross-branch performance comparisons |
| 👥 Staff (Group-wide) | HR Manager / COO | All staff across all branches |
| 🎓 Students (Group-wide) | COO / Academic Dir | Enrollment, performance trends |
| 💰 Finance (Group-wide) | Finance Head / COO | Revenue, collection, dues — all branches |
| 📅 Exam Calendar | Academic Dir | Group-wide exam schedule |
| 🔍 BGV | HR Manager | Pending verifications across all branches |
| 📝 Content Library | Academic Dir | Shared MCQ bank, notes, videos |
| ⚙️ Group Settings | Owner / CEO | Branding, subscriptions, domains per branch |

---

## Section 3 — Group KPI Bar

→ Component: [07-data-display.md](../components/07-data-display.md) — Stat Card

> 6 cards. Data aggregated across ALL branches in the group (or zone-filtered for Zone Managers).

| Card # | Metric | Sub-info | Role Visibility |
|---|---|---|---|
| 1 | Total Branches | Active / Total. e.g., "47 / 52" | All |
| 2 | Total Students | Across all branches. Trend ↑↓ | All |
| 3 | Avg Attendance | Group average. Color-coded. | All |
| 4 | Fee Collection MTD | ₹ collected vs ₹ target. Progress bar. | Finance Head / COO |
| 5 | BGV Pending | Staff without BGV. ⚠️ risk indicator. | HR / COO |
| 6 | Exams Today | Live + scheduled across all branches. | Academic Dir / COO |

---

## Section 4 — Alert Banner

→ Component: [03-alerts-toasts.md](../components/03-alerts-toasts.md)

| Priority | Example Alert |
|---|---|
| 🔴 Critical | "Branch: Dilsukhnagar has 0% attendance recorded today — check system" |
| 🔴 Critical | "47 staff across 12 branches have expired BGV — POCSO risk" |
| 🟠 Warning | "3 branches have subscription expiring in 7 days" |
| 🟡 Info | "Group exam results for JEE Mock #12 published — 14,200 students ranked" |

---

## Section 5 — Branch Performance Map

> Visual India map (SVG) with branch location pins.
> Each pin color-coded by performance score.

```
┌──────────────────────────────────────────────────────────────────┐
│  Branch Map                    [Map ▼]  [Heat Map]  [List View] │
│                                                                  │
│   ┌────────────────────────────────────────────────────────┐    │
│   │                                                        │    │
│   │       [Telangana / AP map outline]                     │    │
│   │                                                        │    │
│   │   📍 Hyderabad (12 branches)  ← cluster pin           │    │
│   │       └─ 🟢 8 performing well                         │    │
│   │       └─ 🟡 3 average                                 │    │
│   │       └─ 🔴 1 critical                                 │    │
│   │                                                        │    │
│   │   📍 Vijayawada (8 branches)                           │    │
│   │   📍 Visakhapatnam (5 branches)                        │    │
│   │                                                        │    │
│   └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Performance score = weighted avg of:                            │
│  Attendance (30%) + Fee collection (30%) + Exam scores (40%)    │
│                                                                  │
│  [🟢 >80%]  [🟡 60-80%]  [🔴 <60%]                             │
└──────────────────────────────────────────────────────────────────┘
```

> Click on a branch pin → opens branch detail drawer
> Hover on pin → tooltip: Branch name, student count, performance score, branch head

---

## Section 6 — Branch Cards Grid

> All branches shown as cards. Default: sorted by performance score.
> Filterable by zone, type (school/coaching), status, performance band.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  All Branches  (47 active)          [Search branches...]  [Filter ▼]   │
│  Sort: [Performance ▼]                                   [+ Add Branch] │
│                                                                         │
│  ┌────────────────────────────┐  ┌────────────────────────────┐        │
│  │ 🟢 Dilsukhnagar Branch     │  │ 🟡 Ameerpet Branch          │        │
│  │    Hyderabad · Coaching    │  │    Hyderabad · Coaching     │        │
│  │                            │  │                             │        │
│  │  Students:  1,247          │  │  Students:  986             │        │
│  │  Attendance: 94.2% ████░   │  │  Attendance: 78.3% ████░   │        │
│  │  Fee Coll:  98.1%  ████░   │  │  Fee Coll:  71.2%  ███░░   │        │
│  │  Exam Avg:  72.4           │  │  Exam Avg:  68.1            │        │
│  │                            │  │                             │        │
│  │  Branch Head: Ravi Kumar   │  │  Branch Head: Priya Sharma  │        │
│  │  [Open Portal →]           │  │  [Open Portal →]            │        │
│  └────────────────────────────┘  └────────────────────────────┘        │
│                                                                         │
│  ┌────────────────────────────┐  ┌────────────────────────────┐        │
│  │ 🔴 Kukatpally Branch       │  │ 🟢 Visakhapatnam Branch     │        │
│  │  ⚠️ Fee collection: 42%   │  │                             │        │
│  │  ⚠️ 3 BGV pending          │  │  ...                        │        │
│  │  [Open Portal →]  [Alert →]│  │  [Open Portal →]            │        │
│  └────────────────────────────┘  └────────────────────────────┘        │
│                                                                         │
│                        [Load more branches]                             │
└─────────────────────────────────────────────────────────────────────────┘
```

### Branch Card Elements

| Element | Spec |
|---|---|
| Status dot | 🟢 Green (>80%), 🟡 Yellow (60–80%), 🔴 Red (<60%) top-left corner |
| Branch name | Bold, 16px |
| City + Type | "Hyderabad · Coaching" or "Vijayawada · School" |
| Student count | With trend arrow |
| 3 metric bars | Attendance, Fee Collection, Exam Avg — mini progress bars |
| Branch Head | Name + 24px avatar |
| Warning icons | ⚠️ shown inline for issues (BGV pending, fee defaulters, low attendance) |
| [Open Portal →] | Opens that branch's portal in same tab. Sets branch context. |

### Branch Card Filters

| Filter | Options |
|---|---|
| Zone | All Zones / Hyderabad / Vijayawada / Visakhapatnam / Tirupati |
| Type | All / School / Coaching / College |
| Performance | All / High (>80%) / Medium / Low (<60%) |
| Status | Active / Suspended / Trial |
| Issues | Has Issues Only (BGV/Fee/Attendance problems) |

---

## Section 7 — Comparative Analytics

→ Component: [07-data-display.md](../components/07-data-display.md) — Charts

> 2 charts side by side. Visible to Director / COO / Academic Director.

```
┌─────────────────────────────────────────────┐  ┌────────────────────────────────────────┐
│  Fee Collection — Top 10 Branches           │  │  Student Enrollment Trend              │
│                                             │  │                                        │
│  Dilsukhnagar  ████████████████  98%        │  │  30K ┤          ●────────              │
│  Visakhapatnam ████████████████  96%        │  │  25K ┤     ●────                       │
│  Ameerpet      █████████████░░░  82%        │  │  20K ┤●────                            │
│  Kukatpally    ████████░░░░░░░░  42% ⚠️    │  │       Jan  Feb  Mar  Apr  May          │
│  ...                                        │  │                                        │
│                     [View all branches →]   │  │       [Breakdown by branch →]          │
└─────────────────────────────────────────────┘  └────────────────────────────────────────┘
```

---

## Section 8 — Quick Actions

| Role | Quick Actions |
|---|---|
| Group Chairman | [Revenue Report] [Top Branches] [Strategic Analytics] |
| COO | [Branches with Issues] [BGV Pending (47)] [Fee Defaulters] |
| Finance Head | [Outstanding ₹12.4L] [Generate Group Invoice] [Razorpay Settlements] |
| HR Manager | [BGV Pending (47)] [Vacancies (12)] [Bulk BGV Submit] |
| Academic Director | [Schedule Group Exam] [Publish Results] [Content Updates] |
| IT Admin | [Portal Health] [API Usage] [User Counts] [Add Branch] |

---

## Section 9 — Recent Activity

→ Component: [07-data-display.md](../components/07-data-display.md)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Group Activity                                         [Filter ▼] │
│  ─────────────────────────────────────────────────────────────────  │
│  🟢  2 min ago  · New student enrolled: Dilsukhnagar Branch (+12)  │
│  🟡  1 hr ago   · Fee reminder sent: Kukatpally (234 students)     │
│  🔵  2 hrs ago  · Exam results published: JEE Mock #14             │
│  🔴  3 hrs ago  · BGV expired: 3 staff — Ameerpet Branch           │
│  🟢  Yesterday  · New branch added: Karimnagar (trial period)      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Dynamic Content Rules

| Condition | Behavior |
|---|---|
| Zone Manager logs in | All sections auto-filtered to their zone only. "Zone: Hyderabad" badge on KPI bar. |
| Single branch group | Branch map and branch grid replaced with single-branch summary |
| No custom domain set | Left panel shows EduForge branding. Settings prompt: "Add your domain" |
| Trial branch | Branch card shows "Trial" badge. Limited features shown. |
| Branch subscription expired | Branch card shows ⛔ overlay. [Renew] button. Staff cannot login to that branch. |

---

## API Calls

| Section | Endpoint | Method |
|---|---|---|
| KPI Bar | `GET /api/v1/group/kpis?zone={zone}` | Zone-filtered |
| Alert banners | `GET /api/v1/group/alerts` | |
| Branch cards | `GET /api/v1/group/branches?zone={}&type={}&status={}` | Paginated |
| Branch map | `GET /api/v1/group/branches/geo` | Lat/lng + performance scores |
| Analytics charts | `GET /api/v1/group/analytics?metric={}&period={}` | |
| Activity feed | `WS /ws/group/activity` | Real-time |
