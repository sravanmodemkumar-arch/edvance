# [17] — Grievance Legal Escalations

> **URL:** `/group/legal/grievance-escalations/`
> **File:** `n-17-grievance-legal-escalations.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Legal Dispute Coordinator (Role 128, G1) — grievances escalated to consumer forum, court, or legal stage

---

## 1. Purpose

The Grievance Legal Escalations page tracks student, parent, and staff grievances that have escalated beyond the internal grievance redressal mechanism to external legal forums — consumer courts, High Court writs, district courts, ombudsman bodies, or regulatory complaints to CBSE/state boards. This is the interface between Division K (Welfare & Safety — Grievance Redressal, page 92) and Division N (Legal & Compliance).

When a grievance cannot be resolved internally and the complainant files a complaint with the District Consumer Disputes Redressal Commission, CBSE grievance portal, State Education Ombudsman, or any court, it graduates to a "Legal Escalation" and is tracked here. The Group Legal Dispute Coordinator records these escalations, monitors response deadlines (consumer forums require a written response within 30 days), tracks hearing dates, and ensures the group's legal position is defended.

Grievance legal escalations are distinct from pure contract/property litigation (tracked in N-09) — they arise from service delivery failures (fee disputes, admission cancellations, result issues, discrimination complaints) rather than commercial disputes.

Scale: 5–50 branches · 5–50 grievance escalations per year · Consumer forum being the most common; HC writs rare but high-stakes

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Handles court appearances externally |
| Group Compliance Manager | 109 | G1 | Read — Regulatory complaints | Views escalations from CBSE/state board |
| Group RTI Officer | 110 | G1 | No Access | Not relevant |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Not relevant |
| Group POCSO Reporting Officer | 112 | G1 | Read — Child welfare escalations | Views escalations related to child protection |
| Group Data Privacy Officer | 113 | G1 | Read — DPDP complaints | Views escalations to Data Protection Board |
| Group Contract Administrator | 127 | G3 | No Access | Not relevant |
| Group Legal Dispute Coordinator | 128 | G1 | Full Read + Record + Update | Primary user |
| Group Insurance Coordinator | 129 | G1 | Read — Insurance-covered escalations | Views escalations with insured liability |

> **Access enforcement:** `@require_role(roles=[109,112,113,128,129], min_level=G1)`. G4/G5 full access.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Grievance Legal Escalations
```

### 3.2 Page Header
```
Grievance Legal Escalations                     [+ Record Escalation]  [Export ↓]
Group Legal Dispute Coordinator — [Name]
[Group Name] · [N] Active Escalations · [N] Response Deadlines This Month
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Consumer forum response overdue | "[N] consumer forum response(s) are overdue — penalty and ex-parte order risk." | Critical (red) |
| Hearing today or tomorrow | "Hearing today/tomorrow: [Case ID] at [Forum]. Advocate confirmed?" | Critical (red) |
| Response deadline within 5 days | "[N] escalation(s) require written response within 5 days." | High (amber) |
| High Court writ filed | "New High Court writ filed against [Branch Name] — immediate legal review required." | Critical (red) |

---

## 4. KPI Summary Bar (7 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Escalations | Count | COUNT WHERE status NOT IN ('disposed','settled','withdrawn') | Blue | `#kpi-active` |
| 2 | Consumer Forum Cases | Count | COUNT WHERE forum_type = 'consumer_forum' AND status = 'active' | Amber if > 5 | `#kpi-consumer` |
| 3 | Response Deadlines (7 Days) | Count | COUNT WHERE response_due BETWEEN TODAY AND TODAY+7 | Red > 0, Green = 0 | `#kpi-deadlines` |
| 4 | Hearings This Month | Count | COUNT WHERE next_hearing within current month | Blue | `#kpi-hearings` |
| 5 | High Court / SC Matters | Count | COUNT WHERE forum_type IN ('high_court','supreme_court') AND status = 'active' | Red > 0, Green = 0 | `#kpi-high-court` |
| 6 | Resolved This FY | Count | COUNT WHERE status IN ('disposed','settled') AND fy = current | Green | `#kpi-resolved` |
| 7 | Est. Penalty Exposure | Sum (₹) | SUM estimated_penalty WHERE status = 'active' | Red > ₹10L, Amber 1–10L, Green 0 | `#kpi-exposure` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/grievance-escalations/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Escalations Table

**Search:** Case ID, complainant name, branch, forum. Debounced 350ms.

**Filters:**
- Forum Type: `All` · `Consumer Forum` · `CBSE Portal` · `State Edu Ombudsman` · `District Court` · `High Court` · `Supreme Court` · `Data Protection Board` · `Labour Tribunal` · `Other`
- Grievance Type: `All` · `Fee Dispute` · `Admission Cancellation` · `Result/Marks` · `Discrimination` · `Staff Misconduct` · `Child Welfare` · `Data Privacy` · `Other`
- Status: `All` · `Active` · `Stay Granted` · `Disposed` · `Settled` · `Withdrawn`
- Branch: dropdown

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Escalation ID | Monospace | Yes | AUTO: GRV-YYYY-NNNN |
| Original Grievance ID | Link | Yes | Links to Division K grievance record |
| Forum / Court | Text | Yes | |
| Forum Type | Badge | Yes | |
| Branch | Text | Yes | |
| Complainant | Text | Yes | Name; student/parent/staff |
| Grievance Type | Badge | Yes | |
| Filed Date | Date | Yes | |
| Response Due | Date | Yes | Red if < 7d or overdue |
| Next Hearing | Date | Yes | Red if today/tomorrow |
| Est. Penalty (₹) | Currency | Yes | |
| Status | Badge | Yes | |
| Actions | Buttons | No | [View] · [Update] (Role 128) |

**Default sort:** Response Due ASC (most urgent first)
**Pagination:** Server-side · Default 25/page

---

## 6. Drawers & Modals

### 6.1 Drawer: `escalation-detail` (720px)
- **Tabs:** Overview · Background · Proceedings · Documents · Resolution · Timeline
- **Overview:** Escalation ID, original grievance link, forum, type, branch, complainant, filed date, current status, assigned advocate
- **Background tab:** Original grievance details (fetched from Division K), escalation trigger, initial group response
- **Proceedings tab:** Hearing history table + [+ Add Hearing] + response deadlines tracker
- **Documents tab:** Court notice, written response filed, order/judgement, settlement agreement
- **Resolution tab:** Outcome type (disposed in favour/against/settled/withdrawn), settlement terms, compensation paid
- **Timeline:** Full audit log

### 6.2 Modal: `record-escalation` (640px)
| Field | Type | Required |
|---|---|---|
| Original Grievance ID | Search/Select (from Div K) | No (may not exist in system) |
| Forum Type | Select | Yes |
| Forum / Court Name | Text | Yes |
| Case / Reference Number | Text | No |
| Branch | Select | Yes |
| Complainant Name | Text | Yes |
| Complainant Type | Select | Yes — Student / Parent / Staff |
| Grievance Type | Select | Yes |
| Filed Date | Date | Yes |
| Response Due | Date | No |
| Assigned Advocate | Text | No |
| Estimated Penalty | Number | No |
| Description | Textarea | Yes |

**Footer:** Cancel · Record Escalation

---

## 7. Charts

### 7.1 Escalations by Forum Type — Donut

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Active Escalations by Forum Type" |
| Data | Count per forum type |
| Tooltip | "[Forum Type]: [N] active escalations" |
| API endpoint | `GET /api/v1/group/{id}/legal/grievance-escalations/by-forum-type/` |
| HTMX | `hx-get` on load → `hx-target="#chart-by-forum"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Escalations by Branch — Bar

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Grievance Escalations by Branch — Current FY" |
| Data | Count per branch |
| Colour | Red if > 5, Amber 2–5, Blue 1 |
| Tooltip | "[Branch]: [N] escalations this FY" |
| API endpoint | `GET /api/v1/group/{id}/legal/grievance-escalations/by-branch/` |
| HTMX | `hx-get` on load → `hx-target="#chart-by-branch"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Escalation recorded | "Escalation [GRV-YYYY-NNNN] recorded." | Success | 4s |
| Hearing added | "Hearing on [date] added to [GRV-YYYY-NNNN]." | Success | 3s |
| HC writ alert | "High Court writ filed — [GRV-YYYY-NNNN]. Immediate legal review required." | Error | Sticky |
| Response overdue | "Response deadline passed for [GRV-YYYY-NNNN]." | Error | 6s |
| Status updated | "Escalation [GRV-YYYY-NNNN] status updated." | Success | 3s |
| Export triggered | "Generating escalations export…" | Info | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No escalations | `scale` | "No Legal Escalations" | "No grievances have been escalated to legal forums." | — |
| Filter returns no results | `search` | "No Matching Escalations" | | Clear Filters |
| No HC/SC matters | `check-circle` | "No High Court Matters" | "No cases are pending before High Court or Supreme Court." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 7 KPI + 8-row table |
| Filter/search | Spinner overlay |
| Charts | Grey canvas + spinner |
| Drawer open | Right-slide skeleton |

---

## 11. Role-Based UI Visibility

| Element | Legal Dispute (128) | Compliance Mgr (109) | DPO (113) | POCSO Officer (112) | CEO/Chairman |
|---|---|---|---|---|---|
| Full escalations table | Visible | CBSE/regulatory only | DPDP escalations | Child welfare only | Full |
| [+ Record Escalation] | Visible | Not visible | Not visible | Not visible | Visible |
| [Update] button | Visible | Not visible | Not visible | Not visible | Visible |
| Penalty exposure KPI | Visible | Not visible | Not visible | Not visible | Visible |
| Charts | Both | Not visible | Not visible | Not visible | Both |
| Export | Visible | Not visible | Not visible | Not visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/grievance-escalations/` | G1+ (scoped) | Paginated list |
| POST | `/api/v1/group/{id}/legal/grievance-escalations/` | Role 128, G4+ | Record escalation |
| GET | `/api/v1/group/{id}/legal/grievance-escalations/{gid}/` | G1+ (scoped) | Detail |
| PATCH | `/api/v1/group/{id}/legal/grievance-escalations/{gid}/` | Role 128, G4+ | Update |
| POST | `/api/v1/group/{id}/legal/grievance-escalations/{gid}/hearings/` | Role 128, G4+ | Add hearing |
| GET | `/api/v1/group/{id}/legal/grievance-escalations/kpis/` | G1+ | KPIs |
| GET | `/api/v1/group/{id}/legal/grievance-escalations/by-forum-type/` | Role 128, G4+ | Chart data |
| GET | `/api/v1/group/{id}/legal/grievance-escalations/by-branch/` | Role 128, G4+ | Chart data |
| POST | `/api/v1/group/{id}/legal/grievance-escalations/export/` | Role 128, G4+ | Async export |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | KPI container | GET `.../grievance-escalations/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Table load | Table body | GET `.../grievance-escalations/` | `#esc-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search/filter | Input/chips | GET with params | `#esc-table-body` | `innerHTML` | Debounce 350ms |
| Open drawer | [View] | GET `.../grievance-escalations/{gid}/` | `#right-drawer` | `innerHTML` | |
| Record modal | [+ Record] | GET `/htmx/legal/grievance-escalations/record-form/` | `#modal-container` | `innerHTML` | |
| Charts | Chart containers | GET chart endpoints | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination | GET with `?page={n}` | `#esc-table-body` | `innerHTML` | |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
