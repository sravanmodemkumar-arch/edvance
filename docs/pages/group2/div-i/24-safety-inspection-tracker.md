# 24 — Safety Inspection Tracker

> **URL:** `/group/transport/safety/inspections/`
> **File:** `24-safety-inspection-tracker.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Transport Safety Officer (primary) · Fleet Manager · Transport Director

---

## 1. Purpose

Manages periodic safety inspections for all vehicles — quarterly safety checks, annual roadworthiness inspections, and ad-hoc checks triggered after incidents or complaints. Each inspection logs the vehicle condition against a standardised checklist and generates a pass/fail result with required rectifications.

Safety inspections are a proactive safety measure separate from statutory fitness certificates (which are government-issued). Group-level inspections catch issues before they become accidents.

Inspection types:
- **Quarterly Safety Check** — Brakes, tyres, lights, seatbelts, fire extinguisher, GPS, first aid kit
- **Annual Roadworthiness Inspection** — Full mechanical + safety audit
- **Pre-season Inspection** — Before new academic year begins
- **Post-incident Inspection** — After any Severity 1–2 incident

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Safety Officer | G3 | Full — schedule, record, close | Primary owner |
| Group Fleet Manager | G3 | Full — mechanical findings | Shared ownership |
| Group Transport Director | G3 | View + approve grounding a vehicle | Oversight |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Safety Inspection Tracker
```

### 3.2 Page Header
- **Title:** `Safety Inspection Tracker`
- **Subtitle:** `[N] Scheduled · [N] Overdue · [N] Completed (AY) · [N] Failed Inspections`
- **Right controls:** `+ Schedule Inspection` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Failed inspection vehicles still on route | "[N] vehicles with failed inspections are still assigned to routes." | Red |
| Overdue quarterly inspections | "[N] vehicles have overdue quarterly safety inspections." | Red |
| Post-incident inspection pending | "[N] vehicles involved in recent incidents have not been inspected." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Inspections Due This Month | Scheduled or overdue | Yellow > 5 · Red > 15 |
| Overdue Inspections | Past due date | Red > 0 |
| Failed — Awaiting Rectification | Failed, vehicle on road | Red > 0 |
| Pass Rate (AY) | % inspections passed | Green ≥ 90% · Yellow < 90% |
| Completed (AY) | Total closed | Blue |
| Avg Days to Rectify | After fail to pass | Yellow > 7 · Red > 14 |

---

## 5. Main Table — Inspections

**Search:** Bus number, branch, inspector. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Inspection Type | Checkbox | Quarterly / Annual / Pre-season / Post-incident |
| Status | Checkbox | Scheduled / In Progress / Passed / Failed / Rectified / Overdue |
| Result | Radio | All / Pass / Fail |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Bus No | ✅ | |
| Branch | ✅ | |
| Inspection Type | ✅ | |
| Scheduled Date | ✅ | |
| Completed Date | ✅ | |
| Inspector | ✅ | |
| Result | ✅ | ✅ Pass · ❌ Fail badge |
| Failed Items | ✅ | Count if failed |
| Rectification Deadline | ✅ | If failed |
| Status | ✅ | |
| Actions | ❌ | View · Schedule · Record Result · Rectify |

**Pagination:** Server-side · 25/page.

---

## 6. Drawers

### 6.1 Drawer: `schedule-inspection`
- **Width:** 540px
- **Fields:** Bus No (searchable) · Inspection Type · Scheduled Date · Inspector Name · Location (workshop/campus) · Notes

### 6.2 Drawer: `record-inspection-result`
- **Width:** 680px
- **Fields:** Bus No · Inspector Name · Inspection Date · Mileage · Checklist (multi-row: Item / Pass/Fail/NA / Notes) · Checklist items: Brakes (front/rear) · Tyres (all 6/8) · Headlights · Indicators · Emergency lights · Seatbelts (driver + front) · Fire extinguisher (valid?) · First aid kit (stocked?) · GPS device (functioning?) · Horn · Windshield · Door mechanisms · Student emergency exit · Overall Result (auto: Pass if all critical items pass) · Inspector Signature (checkbox) · Upload Inspection Sheet (PDF)
- **On fail:** Rectification deadline auto-set to 7 days; vehicle status updated; Fleet Manager notified

### 6.3 Drawer: `rectification-record`
- **Trigger:** Actions → Rectify (after fail)
- **Width:** 540px
- **Fields:** Rectification Date · Items Rectified (checklist from fail) · Workshop Name · Re-inspection Date · Re-inspection Result (Pass/Fail)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Inspection scheduled | "Safety inspection scheduled for [Bus No] on [date]." | Info | 4s |
| Schedule failed | "Failed to schedule inspection. Check vehicle status." | Error | 5s |
| Inspection result recorded — pass | "[Bus No] inspection PASSED. Next due in 3 months." | Success | 4s |
| Inspection result recorded — fail | "[Bus No] inspection FAILED. [N] items need rectification. Fleet Manager notified." | Warning | 6s |
| Result recording failed | "Failed to record inspection result. Please retry." | Error | 5s |
| Rectification completed | "[Bus No] rectification completed. Re-inspection scheduled." | Info | 4s |
| Rectification failed | "Failed to record rectification. Please retry." | Error | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No inspections | "No Safety Inspections Scheduled" | "Schedule quarterly safety inspections for all vehicles." | [+ Schedule Inspection] |
| No failed vehicles | "No Failed Inspections" | "All completed inspections have passed." | — |
| No filter results | "No Inspections Match Filters" | "Adjust branch, inspection type, status, or result filters." | [Clear Filters] |
| No search results | "No Inspections Found for '[term]'" | "Check the bus number, branch, or inspector name." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + inspection table |
| Filter/search | Table body skeleton |
| Record result drawer | 680px skeleton (checklist items load progressively) |

---

## 10. Role-Based UI Visibility

| Element | Safety Officer G3 | Fleet Manager G3 | Transport Director G3 |
|---|---|---|---|
| Schedule Inspection | ✅ | ✅ | ✅ |
| Record Result | ✅ | ✅ | ❌ |
| Ground Vehicle (Fail) | ✅ (propose) | ✅ | ✅ (execute) |
| Record Rectification | ❌ | ✅ | ❌ |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/safety/inspections/` | JWT (G3+) | Inspection list |
| POST | `/api/v1/group/{group_id}/transport/safety/inspections/` | JWT (G3+) | Schedule inspection |
| PATCH | `/api/v1/group/{group_id}/transport/safety/inspections/{id}/` | JWT (G3+) | Record result |
| POST | `/api/v1/group/{group_id}/transport/safety/inspections/{id}/rectify/` | JWT (G3+) | Record rectification |
| GET | `/api/v1/group/{group_id}/transport/safety/inspections/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/transport/safety/inspections/export/` | JWT (G3+) | Async CSV/XLSX export |

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../inspections/?q={val}` | `#inspection-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../inspections/?{filters}` | `#inspection-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../inspections/?sort={col}&dir={asc/desc}` | `#inspection-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../inspections/?page={n}` | `#inspection-table-section` | `innerHTML` |
| Open detail drawer | `click` on Bus No | GET `.../inspections/{id}/` | `#drawer-body` | `innerHTML` |
| Schedule submit | `click` | POST `.../inspections/` | `#inspection-table-section` | `innerHTML` |
| Record result submit | `click` | PATCH `.../inspections/{id}/` | `#inspection-row-{id}` | `outerHTML` |
| Rectification submit | `click` | POST `.../inspections/{id}/rectify/` | `#inspection-row-{id}` | `outerHTML` |
| Export | `click` | GET `.../inspections/export/` | `#export-btn` | `outerHTML` |

> **Audit trail:** All write actions (schedule, record result, rectify) are logged to [Transport Audit Log → Page 33] with user, timestamp, and IP.

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
