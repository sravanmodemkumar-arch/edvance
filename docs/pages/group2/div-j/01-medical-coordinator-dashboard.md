# 01 — Medical Coordinator Dashboard

> **URL:** `/group/health/coordinator/`
> **File:** `01-medical-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Medical Coordinator (Role 85, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Medical Coordinator. Single-screen command centre for the entire health and medical system across all branches — medical room operational status, doctor visit compliance, medicine stock alerts, patient consultation volumes, health screening coverage, and insurance status.

The Medical Coordinator owns health infrastructure policy, ensures every branch has an operational sick bay, coordinates visiting doctor schedules, monitors medicine stock levels, and escalates unresolved medical incidents to the Group COO. Large groups run 20–50 branches with 200–1,000 medical consultations per month; this dashboard provides a real-time picture of health readiness across the group. Any medical room going non-operational, medicine running critically low, or a doctor visit being missed creates an immediate student welfare risk.

Scale: 20–50 branches · 200–1,000 medical visits/month · 50–200 health events/year · 1–3 medical rooms per branch.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Medical Coordinator | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group School Medical Officer | G3 | View + consultation entry | Read-only on policy sections |
| Group Mental Health Coordinator | G3 | View — mental health section only | Cannot see prescription/stock data |
| Group Emergency Response Officer | G3 | View — incidents section only | Cannot see clinical data |
| Group Chairman / CEO | G5 / G4 | View — via governance reports only | Not this URL |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('medical_coordinator')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Medical Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                  [Export Health Report ↓]  [Settings ⚙]
[Group Name] — Group Medical Coordinator · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  [N] Medical Rooms  ·  [N] Consultations This Month
```

### 3.3 Alert Banner (conditional — critical items requiring same-day action)

| Condition | Banner Text | Severity |
|---|---|---|
| Medical room non-operational | "[N] medical rooms are non-operational. Branches affected: [list]. Immediate action required." | Red |
| Medicine stock critically low < 7 days | "Critical medicine shortage at [Branch] — [Item] has less than 7 days stock remaining." | Red |
| Doctor visit overdue > 14 days | "[Branch] has had no doctor visit in [N] days. Compliance breach." | Red |
| Unresolved medical incident | "[N] medical incidents remain unresolved. Review required." | Red |
| Insurance renewal due within 30 days | "Health insurance policy for [Branch] expires on [date]. Renewal action required." | Amber |
| No nurse assigned to branch | "[N] branches have no nurse assigned to their medical room." | Amber |
| Health screening coverage < 60% | "[Branch] health screening coverage is only [N]%. Drive required before [date]." | Amber |

Max 5 alerts visible. Alert-type links route to relevant sections or pages. "View all health events → Health Audit Log" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Medical Rooms | Count of operational rooms across all branches | Green = all branches covered · Yellow = 1–3 non-op · Red > 3 non-op | → Page 05 |
| Doctor Visit Compliance % | Scheduled vs actual visits this month, all branches | Green ≥ 90% · Yellow 70–90% · Red < 70% | → Page 07 |
| Medicine Stock Alerts | Branches with any item below minimum threshold | Green = 0 · Yellow 1–5 · Red > 5 | → Page 08 |
| Consultations This Month | Total patient consultations across all branches | Blue always (informational) | → Page 09 |
| Health Screening Coverage % | Students screened vs enrolled (current AY) | Green ≥ 80% · Yellow 60–80% · Red < 60% | → Page 11 |
| Insurance Policy Status | Policies active vs total group insurance policies | Green = all active · Yellow 1 expiring ≤ 30d · Red = expired | → Page 16 |
| Open Medical Incidents | Unresolved incidents across all branches | Green = 0 · Yellow 1–3 · Red > 3 | → Section 5.4 |
| Branches Missing Doctor Coverage | Branches with no scheduled doctor visit this week | Green = 0 · Yellow 1–2 · Red > 2 | → Page 07 |

**HTMX:** `hx-trigger="every 5m"` → Medicine stock alerts and open incidents auto-refresh.

---

## 5. Sections

### 5.1 Branch Medical Health Overview Table

> Per-branch summary of medical health status — Coordinator's primary monitoring table.

**Search:** Branch name, city. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Medical Room Status | Checkbox | Operational / Non-Operational / Under Renovation |
| Stock Alert | Checkbox | Show branches with stock issues only |
| Insurance Status | Radio | All / Active / Expiring Soon / Expired |
| Doctor Coverage | Radio | All / Covered / Missing |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → branch-medical-detail drawer |
| Medical Room Status | ✅ | Operational ✅ / Non-Operational ❌ / Renovation ⚠ |
| Last Doctor Visit | ✅ | Date + colour: Green ≤ 7d · Yellow 8–14d · Red > 14d |
| Nurse Assigned | ✅ | Name or ❌ None |
| Consultations This Month | ✅ | Count |
| Stock Alert | ✅ | ✅ All OK / ⚠ Low / 🔴 Critical |
| Insurance Status | ✅ | Active / Expiring / Expired |
| Actions | ❌ | View · Schedule Doctor · Stock Check |

**Default sort:** Medical Room Status (Non-Operational first), then Stock Alert (Critical first).
**Pagination:** Server-side · 25/page.

---

### 5.2 Doctor Visit Compliance Panel

> Branch-wise grid showing scheduled vs actual doctor visits this month. Colour-coded compliance bands.

**Display:** Grid of branch cards (3 columns on desktop, 1 on mobile). Each card shows:
- Branch name
- Scheduled visits: [N]
- Actual visits: [N]
- Compliance %: colour-coded badge — Green ≥ 90% · Yellow 70–89% · Red < 70%
- Last visit date
- Next scheduled visit

**Interaction:** Click card → opens `branch-medical-detail` drawer at Doctor Schedule tab.

"View full visit schedule →" → Page 07.

---

### 5.3 Medicine Stock Alert List

> Branches with any medicine or first aid item below minimum threshold.

**Columns:** Branch · Medical Room · Item Name · Category (Medicine/First Aid/Equipment) · Current Qty · Minimum Threshold · Days Remaining · Actions (Update Stock · Order)

**Default sort:** Days Remaining ascending (most critical first).
**Colour rule:** Days Remaining — Red ≤ 7 · Yellow 8–14 · Green > 14.

"View full inventory →" → Page 08.

---

### 5.4 Recent Medical Incidents

> Last 10 medical incidents across all branches requiring coordinator awareness.

**Columns:** Date · Branch · Incident Type (Injury / Illness / Allergic Reaction / Mental Health Crisis / Other) · Severity (Low / Medium / High / Critical) · Status (Open / Under Review / Resolved) · Actions (View · Escalate)

**Colour rule:** Severity — Critical = Red badge · High = Orange · Medium = Yellow · Low = Grey.

"View all incidents →" → Page 20 (Emergency Incident Register).

---

### 5.5 Quick Actions

| Action | Target |
|---|---|
| Schedule Doctor Visit | → Page 07 (visit create drawer) |
| Add Medical Room | → Page 05 (medical-room-create drawer) |
| View Insurance Status | → Insurance detail modal |
| Update Medicine Stock | → Page 08 (stock-update drawer) |
| Export Health Report | Initiates async export (CSV/XLSX) — all branches, current month. Toast shown when ready. Export logged to audit trail. |

---

## 6. Drawers

### 6.1 Drawer: `branch-medical-detail`
- **Trigger:** Branch name link in Section 5.1 table
- **Width:** 640px
- **Tabs:** Medical Room · Doctor Schedule · Consultations · Stock · Insurance

**Medical Room tab:**
- Room name, location, floor, operational status, nurse assigned, equipment compliance score (%), last inspection date, next inspection due

**Doctor Schedule tab:**
- Current month visit schedule — date, doctor, type (General/Specialist), planned vs actual status
- Next 4 scheduled visits

**Consultations tab:**
- This month: count, breakdown by complaint category (fever, injury, chronic, other)
- Last 5 individual consultations: date, patient type, doctor, outcome

**Stock tab:**
- Summary: OK items, Low items, Critical items
- Critical/Low items listed: name, current qty, threshold, days remaining

**Insurance tab:**
- Policy name, insurer, policy number, coverage type, premium, start date, expiry date, renewal contact

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Doctor visit scheduled | "Doctor visit scheduled at [Branch] on [date]." | Success | 4s |
| Stock alert acknowledged | "Stock alert acknowledged for [Branch]. Replenishment order created." | Info | 4s |
| Medical incident escalated | "Incident at [Branch] escalated to Group COO." | Warning | 6s |
| Insurance renewal triggered | "Insurance renewal reminder sent for [Branch]." | Info | 4s |
| Health report exported | "Health report export is being prepared. You'll be notified when ready." | Info | 4s |
| Medical room updated | "Medical room status updated for [Branch]." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches configured | "No Branches with Health Data" | "No branches have medical rooms configured yet." | [Add Medical Room] |
| No stock alerts | "All Stock Levels Healthy" | "All branches have medicine and first aid stock above minimum thresholds." | — |
| No open incidents | "No Open Medical Incidents" | "All medical incidents across all branches are resolved." | — |
| No doctor visits overdue | "Doctor Visit Compliance Good" | "All branches have received doctor visits within the compliance window." | — |
| Search returns no results | "No Branches Found" | "No branches match your search or filters." | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + branch table skeleton (15 rows × 8 columns) + compliance panel + alerts |
| Table filter/search | Inline skeleton rows (8 rows) |
| KPI auto-refresh | Shimmer on individual card values |
| Compliance panel load | Grid card skeletons (6 cards × 2 rows) |
| Branch detail drawer open | 640px drawer skeleton; tabs load lazily on tab click |
| Stock alert list | Table skeleton (5 rows × 8 columns) |

---

## 10. Role-Based UI Visibility

| Element | Medical Coordinator G3 | School Medical Officer G3 | Mental Health Coordinator G3 | Emergency Response Officer G3 | CEO/Chairman |
|---|---|---|---|---|---|
| Schedule Doctor Visit | ✅ | ✅ (own branch) | ❌ | ❌ | ❌ |
| Update Medicine Stock | ✅ | ✅ | ❌ | ❌ | ❌ |
| View Clinical Data | ✅ | ✅ | ❌ | ❌ | ❌ |
| View Incidents | ✅ | ✅ | ❌ | ✅ | ✅ |
| View Mental Health Section | ✅ | ❌ | ✅ | ❌ | ❌ |
| Escalate Incident | ✅ | ❌ | ❌ | ✅ | ❌ |
| Export Report | ✅ | ✅ | ❌ | ❌ | ✅ |
| Insurance Status | ✅ | ❌ | ❌ | ❌ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/coordinator/dashboard/` | JWT (G3+) | Full dashboard data payload |
| GET | `/api/v1/group/{group_id}/health/coordinator/kpi-cards/` | JWT (G3+) | KPI auto-refresh values |
| GET | `/api/v1/group/{group_id}/health/coordinator/branch-overview/` | JWT (G3+) | Branch medical health table |
| GET | `/api/v1/group/{group_id}/health/coordinator/compliance-panel/` | JWT (G3+) | Doctor visit compliance grid data |
| GET | `/api/v1/group/{group_id}/health/coordinator/stock-alerts/` | JWT (G3+) | Medicine stock alert list |
| GET | `/api/v1/group/{group_id}/health/coordinator/incidents/recent/` | JWT (G3+) | Last 10 incidents |
| GET | `/api/v1/group/{group_id}/health/branches/{branch_id}/medical-detail/` | JWT (G3+) | Branch detail drawer payload |
| POST | `/api/v1/group/{group_id}/health/incidents/{incident_id}/escalate/` | JWT (G3+) | Escalate incident to COO |
| POST | `/api/v1/group/{group_id}/health/coordinator/export/` | JWT (G3+) | Initiate async health report export; returns `{job_id}` |
| GET | `/api/v1/group/{group_id}/health/coordinator/export/status/{job_id}/` | JWT (G3+) | Poll export job status (`pending` / `ready` / `failed`) |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../coordinator/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch table search | `input delay:300ms` | GET `.../coordinator/branch-overview/?q={val}` | `#branch-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../coordinator/branch-overview/?{filters}` | `#branch-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../coordinator/branch-overview/?page={n}` | `#branch-table-section` | `innerHTML` |
| Open branch drawer | `click` on branch name | GET `.../health/branches/{id}/medical-detail/` | `#drawer-body` | `innerHTML` |
| Stock alert refresh | `every 5m` | GET `.../coordinator/stock-alerts/` | `#stock-alert-list` | `innerHTML` |
| Escalate incident | `click` | POST `.../health/incidents/{id}/escalate/` | `#incident-row-{id}` | `outerHTML` |
| Compliance panel load | `load` | GET `.../coordinator/compliance-panel/` | `#compliance-panel` | `innerHTML` |
| Initiate health report export | `click` | POST `.../coordinator/export/` | `#export-status` | `innerHTML` |
| Poll export status | `every 5s [!#export-done]` | GET `.../coordinator/export/status/{job_id}/` | `#export-status` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
