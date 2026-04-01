# 03 — Girls Hostel Coordinator Dashboard

> **URL:** `/group/hostel/girls/`
> **File:** `03-girls-hostel-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Girls Hostel Coordinator (Role 69, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Girls Hostel Coordinator. Focused entirely on **girls-only hostel campuses** across all branches — warden supervision, welfare incidents for female hostelers, night security, CCTV coverage adequacy, room occupancy, daily attendance (morning + night roll call), parent communication adherence, and restricted calling hours compliance.

Girls hostels carry additional safety mandates under POCSO and state residential school regulations. The Girls Coordinator monitors biometric gate compliance, visitor restrictions for girls hostels (father/guardian with ID verification only), and CCTV blind-spot reports. Any Severity 1 or 2 welfare incident involving a female hosteler triggers an automatic escalation path to the Girls Coordinator → Hostel Director → Group POCSO Coordinator.

Gender data isolation: Girls Coordinator cannot access boys hosteler records. Enforced at the database query level (`gender = F`).

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Girls Hostel Coordinator | G3 | Full — girls hostels only | Exclusive dashboard |
| Group Hostel Director | G3 | View — all branches via own dashboard | Not this URL |
| Group Boys Hostel Coordinator | G3 | No access | Gender separation enforced |
| Group POCSO Coordinator | G3 | View (welfare incidents only — cross-system) | Via own portal |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Girls Hostel Coordinator
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]               [Export Girls Report ↓]  [Settings ⚙]
[Group Name] — Girls Hostel Coordinator · AY [current academic year]
[N] Girls Hostel Campuses · [N] Female Hostelers (AC: [N] | Non-AC: [N])
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Night roll call discrepancy at any girls hostel | "Night roll call mismatch at [Branch Girls Hostel] — [N] girls unaccounted for. Verify immediately." | Red |
| Severity 1 welfare incident (female) unresolved > 2h | "CRITICAL: Severity 1 welfare incident (female hosteler) at [Branch]. POCSO escalation triggered." | Red |
| CCTV offline at girls hostel | "CCTV system offline at [Branch Girls Hostel]. Security risk — escalate to Branch Principal." | Red |
| Warden absent without replacement at girls hostel | "Warden absent at [Branch Girls Hostel] — no female substitute assigned." | Red |
| Unauthorised visitor entry recorded | "Unauthorised visitor entry at [Branch Girls Hostel] last 24h. Review log." | Amber |
| Restricted calling hours violation | "[N] calling hour violations logged this week at [Branch]." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Female Hostelers | Across all branches | Blue always | → Page 12 (filtered: Girls) |
| Girls Occupancy Rate | Filled / Total girls beds | Green ≥ 85% · Yellow 70–85% · Red < 70% | → Page 13 (filtered: Girls) |
| Night Roll Call Status | Branches with full roll call tonight | Green = All clear · Red = any discrepancy | → Page 24 |
| Open Welfare Incidents (Girls) | Open incidents for female hostelers | Green = 0 · Yellow 1–3 · Red > 3 | → Page 22 (filtered: Girls) |
| CCTV Compliance | Branches with 100% CCTV operational | Green = All · Yellow < 100% · Red any offline | → Page 24 |
| Visitor Compliance | Branches with 0 unauthorised visitor entry (24h) | Green = All clear · Red = violations | → Page 25 |

**HTMX:** `hx-trigger="every 5m"` → `hx-get="/api/v1/group/{id}/hostel/girls/kpi-cards/"` → `hx-target="#kpi-bar"` `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Girls Hostel Branch Table

> All girls hostel campuses — Coordinator's working list.

**Search:** Branch name, city, zone. Debounce 300ms.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches with girls hostel |
| Room Type | Checkbox | AC / Non-AC |
| Safety Status | Radio | Any / Has CCTV Offline / Has Welfare Open / Visitor Violation |
| Night Roll Call | Checkbox | Discrepancy today |
| Warden Status | Checkbox | Warden absent |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → branch detail drawer |
| Total Girls | ✅ | Count |
| Occupancy % | ✅ | Colour-coded |
| AC / Non-AC split | ✅ | "100 AC / 60 Non-AC" |
| Night Roll Call | ✅ | ✅ Clear / ⚠ Discrepancy / — Not submitted |
| CCTV Status | ✅ | ✅ Operational / ⚠ Partial / ❌ Offline |
| Warden on Duty | ✅ | Name (must be female) or "Absent" (red) |
| Open Welfare | ✅ | Count (red if Severity 1 > 0) |
| Visitor Violations (24h) | ✅ | Count (red if > 0) |
| Last Safety Inspection | ✅ | Date (red if > 14 days) |
| Actions | ❌ | View · Escalate · POCSO Alert |

**Default sort:** Safety alerts first (CCTV offline, Severity 1 welfare, roll call discrepancy).

**Pagination:** Server-side · 25/page.

---

### 5.2 Tonight's Roll Call & Biometric Status

> Real-time view of which girls hostel branches have submitted tonight's roll call and biometric gate status.

**Display:** Card grid (1 card per branch).
- ✅ Roll call submitted — All girls accounted for — Biometric gate locked
- ⚠ Roll call submitted — Discrepancy: [N] girls — [Contact Warden]
- ❌ Roll call not submitted — [N] minutes overdue — [Escalate]
- Biometric gate status: ✅ Active · ❌ Offline

---

### 5.3 Warden Supervision Panel (Girls Only)

> Female wardens assignment and supervision tracking.

**Columns:**
| Column | Type |
|---|---|
| Branch | Text |
| Female Warden Name | Text |
| Contact | Phone (click to reveal) |
| On Duty Tonight | Badge (Yes / Absent / Leave) |
| Night Duty Assigned | Yes / No |
| Last Visit by Coordinator | Date |
| Welfare Incidents Raised (Month) | Count |
| Actions | Contact · Schedule Inspection · Log Note |

> Important: Girls hostel wardens must always be female. If a branch reports a male warden on duty at girls hostel, this is an automatic Severity 1 alert.

---

### 5.4 CCTV & Safety Panel

> Quick status of girls hostel CCTV coverage per branch.

**Display:** Table — Branch · Cameras Total · Online · Offline · Last Check · Blind Spots Reported · [View →]

"View All →" → Page 24 (filtered: Girls Hostel).

---

### 5.5 Open Welfare Incidents (Girls)

**Quick table:** Severity | Branch | Hosteler Name | Age | POCSO Triggered? | Status | [View →]

"View All →" → Page 22 (filtered: Girls).

---

## 6. Drawers

### 6.1 Drawer: `girls-branch-detail`
- **Width:** 640px
- **Tabs:** Overview · Wardens · Welfare & Safety · CCTV · Roll Call History · Calling Hours
- **Calling Hours tab:** Log of girls' phone call slots (restricted hours adherence) per branch

### 6.2 Modal: POCSO Alert Escalation
- **Trigger:** Table → POCSO Alert button (appears for Severity 1 welfare incidents only)
- **Type:** Centred modal (480px)
- **Content:** Incident summary + "This action notifies Group POCSO Coordinator and logs a mandatory NCPCR-trackable event."
- **Required fields:** Reason + Confirmation checkbox ("I confirm this is a child safety concern")
- **On confirm:** POST to POCSO alert endpoint; POCSO Coordinator notified via WhatsApp + email

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| POCSO alert raised | "POCSO alert logged and Group POCSO Coordinator notified." | Warning | 6s |
| Warden contact logged | "Contact with [Warden Name] logged." | Success | 4s |
| Safety inspection logged | "Safety inspection logged for [Branch] Girls Hostel." | Success | 4s |
| CCTV offline reported | "CCTV offline at [Branch] escalated to Branch IT Admin." | Warning | 6s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No girls hostel branches | "No Girls Hostel Campuses" | "No girls hostel campuses configured." | [Contact IT Admin] |
| No open welfare incidents | "Girls Hostels — Welfare Clear" | "No open welfare incidents for female hostelers." | — |
| No CCTV issues | "All CCTV Systems Operational" | — | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + branch table + roll call grid + CCTV panel |
| Table filter/search | Inline skeleton rows |
| KPI auto-refresh | Shimmer over card values |
| POCSO alert modal confirm | Spinner on Confirm; modal closes on success |

---

## 10. Role-Based UI Visibility

| Element | Girls Coordinator G3 | Boys Coordinator G3 | Hostel Director G3 |
|---|---|---|---|
| Page itself | ✅ Rendered | ❌ No access | ❌ Own dashboard |
| Girls branch data | ✅ All girls branches | ❌ Hidden | N/A |
| Boys hosteler data | ❌ Hidden | N/A | N/A |
| POCSO Alert button | ✅ Shown (Severity 1 only) | N/A | N/A |
| CCTV panel | ✅ Girls hostels only | N/A | N/A |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/girls/dashboard/` | JWT (G3+ girls coordinator) | Dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/girls/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/girls/branches/` | JWT (G3+) | Girls branch table |
| GET | `/api/v1/group/{group_id}/hostel/girls/roll-call/tonight/` | JWT (G3+) | Tonight's roll call status |
| GET | `/api/v1/group/{group_id}/hostel/girls/cctv-status/` | JWT (G3+) | CCTV panel per branch |
| GET | `/api/v1/group/{group_id}/hostel/girls/wardens/` | JWT (G3+) | Female warden panel |
| POST | `/api/v1/group/{group_id}/hostel/welfare/incidents/{id}/pocso-alert/` | JWT (G3+) | Raise POCSO alert |
| GET | `/api/v1/group/{group_id}/hostel/girls/branches/{id}/detail/` | JWT (G3+) | Branch detail drawer |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../girls/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch search | `input delay:300ms` | GET `.../girls/branches/?q={val}` | `#girls-branch-table-body` | `innerHTML` |
| Roll call status refresh | `every 10m` | GET `.../girls/roll-call/tonight/` | `#roll-call-grid` | `innerHTML` |
| CCTV panel refresh | `every 15m` | GET `.../girls/cctv-status/` | `#cctv-panel` | `innerHTML` |
| Open branch detail | `click` | GET `.../girls/branches/{id}/detail/` | `#drawer-body` | `innerHTML` |
| POCSO alert confirm | `click` (form submit) | POST `.../incidents/{id}/pocso-alert/` | `#welfare-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
