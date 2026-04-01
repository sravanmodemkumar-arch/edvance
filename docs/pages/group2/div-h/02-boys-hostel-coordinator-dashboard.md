# 02 — Boys Hostel Coordinator Dashboard

> **URL:** `/group/hostel/boys/`
> **File:** `02-boys-hostel-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Boys Hostel Coordinator (Role 68, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Boys Hostel Coordinator. Focused entirely on **boys-only hostel campuses** across all branches — warden supervision, discipline oversight, welfare incidents for male hostelers, room occupancy, daily attendance (morning + night roll call), and security coordination. The Boys Coordinator is the senior accountability point for every boys warden in every branch.

The Boys Coordinator cannot access girls hostel data and does not see girls hosteler records. This separation is enforced at the database query level (hosteler records filtered by `gender = M`). The dashboard surfaces problems across all boys hostels so the Coordinator can intervene before they escalate to the Hostel Director.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Boys Hostel Coordinator | G3 | Full — boys hostels only | Exclusive dashboard |
| Group Hostel Director | G3 | View — all branches via own dashboard | Not this URL |
| Group Girls Hostel Coordinator | G3 | No access | Gender separation enforced |
| All other roles | — | — | Redirected to own dashboard |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Boys Hostel Coordinator
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]               [Export Boys Report ↓]  [Settings ⚙]
[Group Name] — Boys Hostel Coordinator · AY [current academic year]
[N] Boys Hostel Campuses · [N] Male Hostelers (AC: [N] | Non-AC: [N])
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Night roll call discrepancy at any branch | "Night roll call mismatch at [Branch] — [N] boys unaccounted for. Verify immediately." | Red |
| Severity 1 welfare incident (male) unresolved > 2h | "CRITICAL: Severity 1 welfare incident (male hosteler) at [Branch] unresolved." | Red |
| Warden absent without replacement today | "Warden absent at [Branch Boys Hostel] — no substitute assigned." | Amber |
| Discipline suspension pending > 24h | "[N] discipline suspensions pending final order for > 24 hours." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Male Hostelers | Across all branches | Blue always | → Page 12 (filtered: Boys) |
| Boys Occupancy Rate | Filled / Total boys beds | Green ≥ 85% · Yellow 70–85% · Red < 70% | → Page 13 (filtered: Boys) |
| Night Roll Call Status | Branches with full roll call today | Green = All clear · Red = any discrepancy | → Page 24 |
| Open Welfare Incidents (Boys) | Open incidents for male hostelers | Green = 0 · Yellow 1–3 · Red > 3 | → Page 22 (filtered: Boys) |
| Discipline Cases (Active, Boys) | Open discipline cases for male hostelers | Green = 0 · Yellow 1–3 · Red > 3 | → Page 28 (filtered: Boys) |
| AC Occupancy | Filled / Total AC beds (boys) | Blue always | → Page 14 (filtered: Boys AC) |

**HTMX:** `hx-trigger="every 5m"` → `hx-get="/api/v1/group/{id}/hostel/boys/kpi-cards/"` → `hx-target="#kpi-bar"` `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Boys Hostel Branch Table

> All boys hostel campuses — Coordinator's working list.

**Search:** Branch name, city, zone. Debounce 300ms.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches with boys hostel |
| Room Type | Checkbox | AC / Non-AC |
| Welfare Status | Radio | Any / Has Open Welfare / Clean |
| Night Roll Call | Checkbox | Discrepancy today |
| Warden Status | Checkbox | Warden absent |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → branch detail drawer |
| Total Boys | ✅ | Count |
| Occupancy % | ✅ | Colour-coded |
| AC / Non-AC split | ✅ | "120 AC / 80 Non-AC" |
| Night Roll Call | ✅ | ✅ Clear / ⚠ Discrepancy / — Not submitted |
| Warden on Duty | ✅ | Name or "Absent" (red) |
| Open Welfare | ✅ | Count (red if > 0 Severity 1) |
| Open Discipline | ✅ | Count |
| Last Inspection | ✅ | Date (red if > 30 days) |
| Actions | ❌ | View · Escalate · Contact Warden |

**Default sort:** Night roll call discrepancy first, then open welfare descending.

**Pagination:** Server-side · 25/page.

---

### 5.2 Today's Night Roll Call Status

> Quick view of which boys hostel branches have submitted today's night roll call.

**Display:** Card grid (1 card per branch). Status: ✅ Submitted — All Clear · ⚠ Submitted — Discrepancy · ❌ Not submitted yet.

**If discrepancy card:** Shows count of unaccounted boys + [Contact Warden] button.

---

### 5.3 Warden Supervision Panel

> Coordinator's tool to manage warden assignments and supervision.

**Columns:**
| Column | Type |
|---|---|
| Branch | Text |
| Boys Warden Name | Text |
| Contact | Phone (click to reveal) |
| On Duty Today | Badge (Yes / Absent) |
| Last Visit by Coordinator | Date |
| Issues Reported This Month | Count |
| Actions | Contact · Schedule Visit · Log Inspection |

---

### 5.4 Boys Welfare Incidents (Open)

> Filtered view of open welfare incidents for male hostelers.

**Quick table:** Severity | Branch | Hosteler Name | Age | Status | [View →]

"View All →" → Page 22 filtered for Boys.

---

### 5.5 Discipline Cases Snapshot

> Active discipline cases for male hostelers.

**Quick table:** Case # | Branch | Hosteler | Incident Type | Age | Status | [View →]

"View All →" → Page 28 filtered for Boys.

---

## 6. Drawers

### 6.1 Drawer: `boys-branch-detail`
- **Trigger:** Branch table → row name
- **Width:** 640px
- **Tabs:** Overview · Wardens · Welfare · Roll Call History · Discipline
- **Overview:** Capacity, occupancy, AC/Non-AC split, room utilization
- **Wardens:** All assigned wardens, on-duty schedule, last coordinator inspection
- **Welfare:** Open incidents for this branch (boys only), last 30 days trend
- **Roll Call History:** Last 7 nights — submitted / discrepancy / missing
- **Discipline:** Open cases list

### 6.2 Modal: Contact Warden
- **Trigger:** Warden panel → Contact button
- **Type:** Centred modal (400px)
- **Content:** Warden name, phone, last contact date
- **Action:** Log contact note (textarea required) + [Mark Contacted]
- **On confirm:** POST to warden contact log; audit trail entry

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Inspection logged | "Inspection logged for [Branch] Boys Hostel." | Success | 4s |
| Warden contact logged | "Contact with [Warden Name] logged." | Success | 4s |
| Incident escalated | "Welfare incident at [Branch] escalated to Hostel Director." | Warning | 6s |
| Export triggered | "Boys hostel report export started." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No boys hostel branches | "No Boys Hostel Campuses" | "No boys hostel campuses have been configured." | [Contact IT Admin] |
| No open welfare incidents | "All Boys Hostels — Welfare Clear" | "No open welfare incidents for male hostelers." | — |
| No roll call discrepancies | "All Roll Calls Submitted and Clear" | — | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + branch table (5 rows) + roll call grid + warden panel |
| Table filter/search | Inline skeleton rows |
| KPI auto-refresh | Shimmer over card values |
| Branch detail drawer open | Centred spinner; tabs load lazily on click |

---

## 10. Role-Based UI Visibility

| Element | Boys Coordinator G3 | Hostel Director G3 | Girls Coordinator G3 |
|---|---|---|---|
| Page itself | ✅ Rendered | ❌ Own dashboard | ❌ No access |
| Boys branch table | ✅ All boys branches | N/A | N/A |
| Girls hosteler data | ❌ Hidden | N/A | N/A |
| Warden contact action | ✅ Shown | N/A | N/A |
| Roll call detail | ✅ Boys only | N/A | N/A |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/boys/dashboard/` | JWT (G3+ boys coordinator) | Dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/boys/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/boys/branches/` | JWT (G3+) | Boys branch table |
| GET | `/api/v1/group/{group_id}/hostel/boys/roll-call/today/` | JWT (G3+) | Today's roll call status per branch |
| GET | `/api/v1/group/{group_id}/hostel/boys/wardens/` | JWT (G3+) | Warden supervision panel |
| POST | `/api/v1/group/{group_id}/hostel/wardens/{id}/contact-log/` | JWT (G3+) | Log warden contact |
| GET | `/api/v1/group/{group_id}/hostel/welfare/incidents/?gender=M&status=open` | JWT (G3+) | Open boys welfare incidents |
| GET | `/api/v1/group/{group_id}/hostel/boys/branches/{id}/detail/` | JWT (G3+) | Branch detail drawer |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../boys/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch search | `input delay:300ms` | GET `.../boys/branches/?q={val}` | `#boys-branch-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../boys/branches/?{filters}` | `#boys-branch-table-section` | `innerHTML` |
| Roll call status refresh | `every 10m` | GET `.../boys/roll-call/today/` | `#roll-call-grid` | `innerHTML` |
| Open branch detail | `click` | GET `.../boys/branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Log warden contact | `click` (form submit) | POST `.../wardens/{id}/contact-log/` | `#warden-panel` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
