# P-05 — Operational & Safety Audit

> **URL:** `/group/audit/operational/`
> **File:** `p-05-operational-safety-audit.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Inspection Officer (Role 123, G3) — primary operator

---

## 1. Purpose

The Operational & Safety Audit page manages all non-financial, non-academic audits — infrastructure condition, fire safety, CCTV coverage, hygiene, staffing adequacy, electrical safety, building stability, playground maintenance, drinking water quality, and transport safety. In Indian education, safety audits are mandated by multiple authorities: the local municipal corporation (fire NOC, building stability), CBSE/state board (infrastructure norms for affiliation), RTE Act (minimum infrastructure), POCSO (child safety infrastructure), and insurance companies (safety for claim validity).

The problems this page solves:

1. **Fire safety non-compliance:** The 2004 Kumbakonam school fire (94 children dead) led to mandatory fire safety norms, but enforcement is patchy. Many branches have expired fire extinguishers, blocked emergency exits, missing fire alarm systems, and no fire drill records. A fire safety audit every 6 months catches these before the municipal inspector does — or worse, before an actual fire.

2. **CCTV coverage gaps:** POCSO guidelines and most state education departments mandate CCTV at entry/exit points, corridors, common areas, and transport vehicles. The audit verifies: camera count matches layout requirement, all cameras functional (not just installed), recording retention ≥ 30 days, blind spots identified, and DVR/NVR accessible to authorised personnel only.

3. **Building and infrastructure decay:** Many Indian school buildings are 20–40 years old. The audit checks: structural cracks, roof leakage, electrical wiring condition, railing stability (critical for multi-storey buildings), toilet cleanliness and count (CBSE norm: 1 toilet per 40 students), drinking water quality (tested quarterly), and playground safety (no exposed metal, proper surfacing).

4. **Staffing adequacy:** RTE mandates minimum teacher-student ratios and support staff. The operational audit verifies: actual teacher count vs sanctioned posts, teacher qualifications match CBSE/board requirements (B.Ed mandatory), non-teaching staff adequacy (peon, sweeper, security guard, lab attendant), and POCSO-compliant background verification for all staff with student access.

5. **Transport safety:** For groups running 50–500 buses, transport safety is a daily life-and-death concern. The audit checks: driver license validity, vehicle fitness certificate, GPS functionality, first-aid kit on bus, fire extinguisher on bus, attendant presence (mandatory for primary school buses), speed governor calibration, and emergency contact display.

**Scale:** 5–50 branches · 50–500 classrooms · 50–500 buses · Semi-annual safety audits per branch · 100–500 safety findings/year

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Inspection Officer | 123 | G3 | Full — create audits, conduct inspections, fill checklists, upload evidence | Primary field operator |
| Group Internal Audit Head | 121 | G1 | Read + oversight — view all operational audits | Cross-functional visibility |
| Group Academic Quality Officer | 122 | G1 | Read — infrastructure impacting academics (labs, library) | Cross-check |
| Group Compliance Data Analyst | 127 | G1 | Read — operational audit data for analytics | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read + CAPA — create corrective actions | Drives fixes |
| Group Safety Audit Officer (Div K) | 96 | G1 | Read — cross-reference with Division K safety data | Coordination |
| Group Transport Director (Div I) | 79 | G3 | Read — transport safety audit results | Transport coordination |
| Group CEO / Chairman | — | G4/G5 | Read — safety overview | Liability awareness |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Reads from Division H (hostel), Division I (transport), Division K (welfare) for cross-reference.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Operational & Safety Audit
```

### 3.2 Page Header
```
Operational & Safety Audit                          [+ New Safety Audit]  [Checklist Library]  [Export]
Inspection Officer — M. Venkatesh
Sunrise Education Group · FY 2025-26 · 28 branches · Safety Index: 82% · Fire NOC: 24/28 valid
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Safety Index (Group) | Percentage | Weighted AVG of all branch safety scores | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-safety` |
| 2 | Fire NOC Valid | Fraction | Branches with valid fire NOC / total | Green = all, Amber ≥ 80%, Red < 80% | `#kpi-fire` |
| 3 | CCTV Coverage | Percentage | Branches with 100% CCTV coverage / total | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-cctv` |
| 4 | Open Safety Findings | Integer | COUNT(findings) WHERE category IN safety categories AND status != 'closed' | Red > 20, Amber 5–20, Green < 5 | `#kpi-findings` |
| 5 | Building Stability Cert | Fraction | Branches with valid stability certificate / total | Green = all, Red < all | `#kpi-building` |
| 6 | Transport Compliance | Percentage | Vehicles with all safety requirements met / total fleet | Green ≥ 95%, Amber 85–94%, Red < 85% | `#kpi-transport` |

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Audit List** — All operational/safety audits
2. **Fire & Electrical Safety** — Fire NOC, extinguishers, electrical wiring, drill records
3. **Infrastructure & Hygiene** — Building condition, toilets, water, playground
4. **CCTV & Security** — Camera coverage, recording, guard deployment
5. **Transport Safety** — Vehicle fitness, driver compliance, GPS

### 5.2 Tab 1: Audit List

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Audit ID | Text (link) | Yes | OSA-2026-001 |
| Branch | Text | Yes | — |
| Audit Type | Badge | Yes | Fire Safety / Infrastructure / CCTV / Transport / Comprehensive |
| Date | Date | Yes | — |
| Inspector | Text | Yes | — |
| Status | Badge | Yes | Scheduled / In Progress / Report Pending / Reviewed / Closed |
| Findings | Integer | Yes | — |
| Critical | Integer | Yes | S1 findings |
| Safety Score | Percentage | Yes | — |
| Actions | Buttons | No | [View] [Start] [Submit Report] |

### 5.3 Tab 2: Fire & Electrical Safety

**Branch-wise fire safety matrix:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Fire NOC | Badge | Yes | ✅ Valid (expiry date) / 🔴 Expired / ⚠️ Expiring < 3m |
| Extinguishers | Badge | Yes | ✅ All functional / ⚠️ N expired / 🔴 Missing |
| Fire Alarm | Badge | Yes | ✅ Functional / 🔴 Non-functional / ⚠️ Partial |
| Emergency Exits | Badge | Yes | ✅ Clear / 🔴 Blocked / ⚠️ Missing signage |
| Fire Drill (Last) | Date | Yes | Red > 6 months ago, Amber 3–6m, Green < 3m |
| Electrical Wiring | Badge | Yes | ✅ Compliant / ⚠️ Aging / 🔴 Hazardous |
| MCB/ELCB Installed | Badge | Yes | ✅ Yes / 🔴 No |
| Earthing Tested | Badge | Yes | ✅ Yes (date) / 🔴 Not tested |
| Overall Fire Score | Percentage | Yes | Composite |

### 5.4 Tab 3: Infrastructure & Hygiene

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Building Age (years) | Integer | Yes | — |
| Stability Certificate | Badge | Yes | ✅ Valid / 🔴 Expired / ⚠️ Expiring |
| Structural Issues | Badge | Yes | ✅ None / ⚠️ Minor cracks / 🔴 Major issues |
| Toilets (Student) | Fraction | Yes | Available / CBSE norm (1:40) |
| Toilet Cleanliness | Rating | Yes | 1–5 stars |
| Drinking Water | Badge | Yes | ✅ Tested OK / 🔴 Not tested / ⚠️ Failed |
| Water Test Date | Date | Yes | Red > 3 months |
| Playground Condition | Rating | Yes | 1–5 stars |
| Roof Condition | Badge | Yes | ✅ Good / ⚠️ Leakage / 🔴 Unsafe |
| Railing/Parapet | Badge | Yes | ✅ Secure / 🔴 Damaged / ⚠️ Below height norm |
| Hygiene Score | Percentage | Yes | Composite |

### 5.5 Tab 4: CCTV & Security

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Cameras Required | Integer | Yes | Based on layout |
| Cameras Installed | Integer | Yes | — |
| Cameras Functional | Integer | Yes | Working at last check |
| Coverage | Percentage | Yes | Functional / required |
| Recording Retention | Badge | Yes | ✅ ≥ 30 days / ⚠️ < 30 days / 🔴 No recording |
| Blind Spots | Integer | Yes | Identified blind spots |
| Entry/Exit Covered? | Badge | Yes | ✅ All / 🔴 Gaps |
| Night Vision? | Badge | Yes | ✅ Yes / 🔴 No |
| Security Guards | Fraction | Yes | Deployed / required |
| Visitor Register | Badge | Yes | ✅ Maintained / 🔴 Not maintained |
| CCTV Score | Percentage | Yes | Composite |

### 5.6 Tab 5: Transport Safety

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Vehicle No. | Text | Yes | — |
| Branch | Text | Yes | Primary branch |
| Fitness Certificate | Badge | Yes | ✅ Valid / 🔴 Expired |
| Insurance | Badge | Yes | ✅ Valid / 🔴 Expired |
| GPS Functional | Badge | Yes | ✅ Yes / 🔴 No |
| Driver License | Badge | Yes | ✅ Valid / 🔴 Expired / ⚠️ Expiring < 30d |
| Driver BGV | Badge | Yes | ✅ Cleared / 🔴 Pending / ⚠️ Failed |
| Speed Governor | Badge | Yes | ✅ Calibrated / 🔴 Missing |
| First Aid Kit | Badge | Yes | ✅ Present / 🔴 Missing |
| Fire Extinguisher | Badge | Yes | ✅ Present / 🔴 Missing |
| Attendant (Primary) | Badge | Yes | ✅ Assigned / 🔴 Missing (mandatory for primary) |
| Emergency Contact | Badge | Yes | ✅ Displayed / 🔴 Not displayed |
| Overall | Percentage | Yes | Composite compliance |

---

## 6. Drawers & Modals

### 6.1 Modal: `create-safety-audit` (640px)

- **Title:** "New Operational / Safety Audit"
- **Fields:**
  - Branch (dropdown, required)
  - Audit type (dropdown): Fire Safety / Infrastructure / CCTV & Security / Transport / Hygiene / Comprehensive
  - Scheduled date (date picker)
  - Inspector(s) (multi-select)
  - Checklist template (dropdown — from P-08 library; auto-selected based on audit type)
  - Surprise? (toggle)
  - Priority (radio): Routine / High / Critical / Emergency
  - Linked to incident? (toggle + incident ID — e.g., post-fire-drill findings, post-accident)
  - Special instructions (textarea)
- **Buttons:** Cancel · Schedule
- **Access:** Role 123, 121, G4+

### 6.2 Drawer: `safety-audit-detail` (780px, right-slide)

- **Title:** "Safety Audit — [Type] · [Branch] · [Date]"
- **Tabs:** Overview · Checklist · Photos · Findings · Report · History
- **Overview tab:** Type, branch, date, inspector, status, overall score
- **Checklist tab:** Interactive checklist — inspector fills during visit:
  - Each item: Compliant ✅ / Non-compliant 🔴 / Partial ⚠️ / Not Applicable
  - Comment field per item
  - Photo upload per item (evidence)
- **Photos tab:** Gallery of all photos taken during audit — geotagged, timestamped
- **Findings tab:** Findings generated from non-compliant checklist items
- **Report tab:** Audit report with score breakdown
- **History tab:** Previous audits at this branch for comparison
- **Footer:** [Add Finding] [Submit Report] [Export PDF]
- **Access:** G1+ (Division P roles)

### 6.3 Modal: `photo-evidence` (480px)

- **Title:** "Upload Photo Evidence"
- **Fields:**
  - Photo (camera capture or file upload — mobile-friendly)
  - Caption (text)
  - Checklist item linked (dropdown)
  - Location in branch (dropdown): Entrance / Corridor / Classroom / Lab / Library / Playground / Toilet / Kitchen / Hostel / Bus / Other
  - Severity indicator (radio): Compliant / Concern / Critical
- **Auto-capture:** GPS coordinates + timestamp embedded in metadata
- **Buttons:** Cancel · Upload
- **Access:** Role 123

### 6.4 Modal: `fire-drill-record` (480px)

- **Title:** "Record Fire Drill — [Branch]"
- **Fields:**
  - Date and time conducted
  - Total students evacuated (integer)
  - Evacuation time (minutes:seconds)
  - Assembly point reached? (Yes / No)
  - Fire department involved? (Yes / No)
  - Issues observed (textarea)
  - Photos (upload)
  - Compliant with norms? (toggle — CBSE: annual drill mandatory; evacuation < 3 minutes)
- **Buttons:** Cancel · Record
- **Access:** Role 123, 121

---

## 7. Charts

### 7.1 Branch Safety Score (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Branch Safety Score — All Branches" |
| Data | Safety score per branch, sorted descending |
| Colour | Green ≥ 85%, Amber 70–84%, Red < 70% |
| API | `GET /api/v1/group/{id}/audit/operational/analytics/branch-safety/` |

### 7.2 Safety Dimension Radar (Spider)

| Property | Value |
|---|---|
| Chart type | Radar/Spider |
| Title | "Safety Dimensions — Group Average" |
| Axes | Fire, Infrastructure, CCTV, Transport, Hygiene, Electrical |
| Data | Group average score per dimension |
| Overlay | Previous audit cycle for comparison |
| API | `GET /api/v1/group/{id}/audit/operational/analytics/dimension-radar/` |

### 7.3 Compliance Expiry Timeline (Gantt-style Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal timeline bars |
| Title | "Certificate & NOC Expiry Timeline" |
| Data | Fire NOC, Building Stability, Vehicle Fitness — per branch with expiry dates |
| Colour | Green (valid > 6m), Amber (expiring < 6m), Red (expired) |
| API | `GET /api/v1/group/{id}/audit/operational/analytics/expiry-timeline/` |

### 7.4 Finding Trend (Stacked Area)

| Property | Value |
|---|---|
| Chart type | Stacked area |
| Title | "Safety Findings — Monthly Trend" |
| Data | COUNT(findings) per month per category (Fire, Infrastructure, CCTV, Transport, Hygiene) |
| API | `GET /api/v1/group/{id}/audit/operational/analytics/finding-trend/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit created | "Safety audit scheduled — [Type] at [Branch]" | Success | 3s |
| Checklist item updated | "Checklist updated — [N] items completed" | Info | 2s |
| Photo uploaded | "Evidence photo uploaded" | Success | 2s |
| Finding added | "Safety finding [ID] added — severity: [S1–S4]" | Success | 3s |
| Critical finding | "🔴 Critical safety finding — immediate attention required at [Branch]" | Error | 6s |
| Fire NOC expired | "⚠️ Fire NOC expired at [Branch] — municipal penalty risk" | Warning | 6s |
| Report submitted | "Safety audit report submitted — [Branch]" | Success | 3s |
| Fire drill recorded | "Fire drill recorded — [Branch], evacuation: [time]" | Success | 3s |
| Vehicle non-compliant | "🔴 Vehicle [Number] non-compliant — [Issue]" | Error | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No safety audits | 🔍 | "No Safety Audits" | "Schedule your first operational safety audit." | New Safety Audit |
| No fire drills recorded | 🔥 | "No Fire Drills Recorded" | "Fire drills are mandatory every 6 months per CBSE norms." | Record Fire Drill |
| No transport data | 🚌 | "No Transport Data" | "Transport fleet data is required from Division I." | — |
| No findings | ✅ | "All Clear" | "No open safety findings. All branches are compliant." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + tab skeleton |
| Safety matrix | Table skeleton with badge placeholders |
| Photo gallery | Image grid placeholder |
| Audit detail drawer | 780px skeleton: 6 tabs |
| Checklist | Checkbox list skeleton |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/operational/` | G1+ | List all operational/safety audits |
| GET | `/api/v1/group/{id}/audit/operational/kpis/` | G1+ | KPI values |
| POST | `/api/v1/group/{id}/audit/operational/` | 123, 121, G4+ | Create safety audit |
| GET | `/api/v1/group/{id}/audit/operational/{audit_id}/` | G1+ | Audit detail |
| PUT | `/api/v1/group/{id}/audit/operational/{audit_id}/` | 123, 121 | Update audit |
| GET | `/api/v1/group/{id}/audit/operational/{audit_id}/checklist/` | G1+ | Get checklist |
| PATCH | `/api/v1/group/{id}/audit/operational/{audit_id}/checklist/{item_id}/` | 123 | Update checklist item |
| POST | `/api/v1/group/{id}/audit/operational/{audit_id}/photos/` | 123 | Upload photo evidence |
| GET | `/api/v1/group/{id}/audit/operational/{audit_id}/photos/` | G1+ | List photos |
| POST | `/api/v1/group/{id}/audit/operational/{audit_id}/findings/` | 123, 121 | Add finding |
| POST | `/api/v1/group/{id}/audit/operational/{audit_id}/report/` | 123 | Submit report |
| GET | `/api/v1/group/{id}/audit/operational/fire-safety/` | G1+ | Fire safety matrix |
| GET | `/api/v1/group/{id}/audit/operational/infrastructure/` | G1+ | Infrastructure matrix |
| GET | `/api/v1/group/{id}/audit/operational/cctv/` | G1+ | CCTV coverage matrix |
| GET | `/api/v1/group/{id}/audit/operational/transport/` | G1+ | Transport safety table |
| POST | `/api/v1/group/{id}/audit/operational/fire-drills/` | 123, 121 | Record fire drill |
| GET | `/api/v1/group/{id}/audit/operational/analytics/branch-safety/` | G1+ | Branch safety bar chart |
| GET | `/api/v1/group/{id}/audit/operational/analytics/dimension-radar/` | G1+ | Dimension radar chart |
| GET | `/api/v1/group/{id}/audit/operational/analytics/expiry-timeline/` | G1+ | Certificate expiry timeline |
| GET | `/api/v1/group/{id}/audit/operational/analytics/finding-trend/` | G1+ | Finding trend area chart |
| GET | `/api/v1/group/{id}/audit/operational/export/` | G1+ | Export audit data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../operational/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#operational-content` | `innerHTML` | `hx-trigger="click"` |
| Audit detail drawer | Row click | `hx-get=".../operational/{id}/"` | `#right-drawer` | `innerHTML` | 780px drawer |
| Create audit | Form submit | `hx-post=".../operational/"` | `#create-result` | `innerHTML` | Toast |
| Checklist update | Checkbox/select | `hx-patch=".../checklist/{item_id}/"` | `#checklist-item-{id}` | `outerHTML` | Inline update, debounced |
| Photo upload | Form submit | `hx-post=".../operational/{id}/photos/"` | `#photo-gallery` | `beforeend` | Appends new photo |
| Add finding | Form submit | `hx-post=".../operational/{id}/findings/"` | `#finding-result` | `innerHTML` | Toast |
| Fire drill record | Form submit | `hx-post=".../fire-drills/"` | `#drill-result` | `innerHTML` | Toast |
| Filter | Filter change | `hx-get` with filters | `#table-body` | `innerHTML` | `hx-trigger="change"` |
| Chart load | Tab shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |
| Submit report | Button click | `hx-post=".../operational/{id}/report/"` | `#report-status` | `innerHTML` | Toast |
| Pagination | Page click | `hx-get` with page param | `#table-body` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
