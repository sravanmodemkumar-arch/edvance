# 03 — Branch Coordinator Dashboard

> **URL:** `/group/ops/coordinator/`
> **File:** `03-branch-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Branch Coordinator (G3) — exclusive landing page

---

## 1. Purpose

Post-login landing for the Group Branch Coordinator. Shows only the branches assigned to
this coordinator — not all branches. Coordinators are the liaison between Group HQ and
branch principals. Their primary actions are: view branch status, schedule visits, relay
communications, raise issues, and submit post-visit reports.

> **Scoping rule:** Branch Coordinator sees ONLY their assigned branches. Platform enforces
> this at the API level — `branch.coordinator_id == current_user.id`.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Branch Coordinator | G3 | Full — own branches only | Exclusive dashboard |
| Group Operations Manager | G3 | View all coordinators' dashboards | Via Page 09 |
| Group COO | G4 | View | Has own dashboard |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Branch Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                   [Message Principals ✉]  [Settings ⚙]
Group Branch Coordinator · Assigned Branches: [N] · Last login: [date time]
```

### 3.3 Alert Banner
- Shown when: Branch with overdue compliance task · Unresolved issue >7 days · Missed scheduled visit
- Max 3 alerts; dismissible per session

---

## 4. KPI Summary Bar (5 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| My Branches | `8 assigned` | Static count | → My Branch Table below |
| Visits This Month | `5 done / 8 planned` | Green ≥75% · Yellow 50–75% · Red <50% | → Page 10 |
| Open Issues | `3 raised by me · 1 overdue` | Green = none overdue · Red = any overdue | → Page 12 |
| Messages Sent This Week | `12 sent` | Informational | — |
| Next Scheduled Visit | `[Branch Name] on [Date]` | Green if ≥3d away · Yellow 1–2d · Red = today/overdue | → Page 10 |

**HTMX:** `every 5m` → `hx-get="/api/v1/group/{id}/coordinator/{coord_id}/kpi-cards/"` → `#kpi-bar`

---

## 5. Sections

### 5.1 My Assigned Branches

> Core working table — coordinator sees their branches only.

**Search:** Branch name / city. Debounce 300ms.

**Advanced Filters:**
| Filter | Options |
|---|---|
| Status | Active · Inactive · Onboarding |
| Issue Status | Has Open Issues · No Issues |
| Visit Status | Overdue · On Track · Not Scheduled |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | Link → `branch-ops-detail` drawer |
| City | ✅ | |
| Type | ✅ | Day Scholar / Hostel / Both |
| Principal Name | ❌ | Click → open compose message |
| Last Visit | ✅ | Red if >30 days |
| Next Visit | ✅ | Yellow if within 3 days |
| Open Issues | ✅ | Count — mine + branch-raised |
| Compliance Score | ✅ | % |
| Actions | ❌ | View · Schedule Visit · Raise Issue · Message Principal |

**Default sort:** Last Visit ascending (overdue visits first).

**Pagination:** Server-side · 10/25 · "Showing X–Y of Z branches".

---

### 5.2 Upcoming Visits Calendar

**Display:** 2-week mini-calendar with visit markers.

- Green dot: scheduled visit
- Red dot: overdue visit (past scheduled date, not yet completed)
- Grey: no visit scheduled

Clicking a date opens visit detail or creates new visit schedule.

**Link:** [Full Visit Scheduler →] → Page 10.

---

### 5.3 Recent Issues I Raised

> Issues/escalations raised by this coordinator across their branches.

**Columns:** Issue Type · Branch · Priority · Status · Days Open · Actions (View/Update)

**Max rows:** 5. [View All →] → Page 12.

---

### 5.4 Communication Feed

> Recent messages sent to principals and responses received.

**Display:** Timeline list, 5 most recent.
- Sent circular to [Branch Name] — [date]
- Reply from [Principal Name] — [date] — [message preview]
- [View All Communications →] link

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-ops-detail`
- **Width:** 640px
- **Tabs:** Overview · Issues · Visit History · Compliance
- **Coordinator can see:** branch ops metrics, their own issues, their visit reports
- **Coordinator cannot see:** other coordinators' data, finance details, staff BGV

### 6.2 Drawer: `visit-schedule-create`
- **Width:** 560px
- **Fields:** Branch (pre-filled to my branches) · Visit Type (Routine/Audit/Emergency/Follow-up) · Date (date picker) · Estimated Duration · Checklist Template · Notes
- **Validation:** Date must be future · Branch must be in my assignment

### 6.3 Drawer: `escalation-create` (Raise Issue)
- **Width:** 640px
- **Fields:** Issue Type · Branch (pre-filled) · Priority (P1–P4) · Description (min 50 chars) · Evidence (file upload) · Suggested Owner
- **Note:** Coordinator raises issue; Ops Manager/COO assigns and resolves

### 6.4 Drawer: `compose-message`
- **Width:** 560px
- **Fields:** To (Principal at branch — pre-filled) · CC (optional) · Subject · Message (rich text) · Attach file
- **Send via:** EduForge internal message + WhatsApp notification

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Visit scheduled | "Visit scheduled for [Branch] on [Date]" | Success | 4s |
| Issue raised | "Issue raised — Operations Manager notified" | Success | 4s |
| Message sent | "Message sent to [Principal Name]" | Success | 4s |
| Visit report submitted | "Visit report submitted successfully" | Success | 4s |

---

## 8. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No assigned branches | "No branches assigned yet" | "Contact your Operations Manager to get branch assignments" | — |
| No upcoming visits | "No visits scheduled" | "Schedule your first visit" | [Schedule Visit] |
| No open issues | "No open issues" | "All issues resolved" | — |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPI bar + branch table (5 rows) + calendar + feed |
| Branch table filter | Inline skeleton rows |
| Drawer open | Spinner in drawer body |
| Message send | Spinner in Send button + disabled |

---

## 10. Role-Based UI Visibility

| Element | Coordinator (own branches) | Ops Mgr / COO (viewing) |
|---|---|---|
| Branch table | Own branches only | Not accessible here (use Page 07) |
| [Message Principal] | ✅ Enabled | N/A |
| [Raise Issue] | ✅ Enabled | N/A |
| [Schedule Visit] | ✅ Enabled | N/A |
| Finance / Fee data columns | ❌ Hidden (G3 — no finance access) | N/A |
| Staff BGV columns | ❌ Hidden | N/A |

> Coordinator branch scoping enforced at API: `?coordinator_id={current_user.id}` appended server-side.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/coordinator/{coord_id}/dashboard/` | JWT (G3 own / G4 any) | Full dashboard data |
| GET | `/api/v1/group/{id}/coordinator/{coord_id}/kpi-cards/` | JWT (G3 own) | KPI auto-refresh |
| GET | `/api/v1/group/{id}/ops/branches/?coordinator_id={coord_id}` | JWT (G3 own) | My branches |
| GET | `/api/v1/group/{id}/visits/?coordinator_id={coord_id}&upcoming=true` | JWT (G3) | Upcoming visits |
| POST | `/api/v1/group/{id}/visits/` | JWT (G3) | Create visit schedule |
| POST | `/api/v1/group/{id}/escalations/` | JWT (G3) | Raise issue |
| GET | `/api/v1/group/{id}/escalations/?raised_by={coord_id}` | JWT (G3) | Issues I raised |
| POST | `/api/v1/group/{id}/messages/` | JWT (G3) | Send message to principal |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Branch search | `input delay:300ms` | `/api/.../branches/?coordinator_id={}&q={val}` | `#coord-branch-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../branches/?coordinator_id={}&filters={}` | `#coord-branch-table-section` | `innerHTML` |
| KPI auto-refresh | `every 5m` | `/api/.../coordinator/{id}/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Open branch detail | `click` | `/api/.../branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| Calendar date click | `click` | `/api/.../visits/?date={date}&coordinator_id={}` | `#visit-detail-panel` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
