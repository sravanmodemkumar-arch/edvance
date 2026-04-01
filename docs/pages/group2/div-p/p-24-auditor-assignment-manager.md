# P-24 — Auditor Assignment & Workload Manager

> **URL:** `/group/audit/assignments/`
> **File:** `p-24-auditor-assignment-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Internal Audit Head (Role 121, G1) — primary operator

---

## 1. Purpose

The Auditor Assignment & Workload Manager handles the operational planning of who audits which branch, when, and how frequently — while enforcing the two core constraints that protect audit integrity: auditor rotation and conflict-of-interest prevention.

In a group with 5–10 auditors and 28 branches, assignment management seems simple until you account for the constraints. An auditor should not audit the same branch two consecutive times (familiarity bias — the auditor starts overlooking things they've seen before). An auditor should not audit a branch where they previously worked, where they have family members, or where they have a prior personal relationship with the principal (conflict of interest). An auditor who has been doing financial audits for the last three quarters needs exposure to academic audits. And no auditor should be assigned so many simultaneous visits that quality suffers.

Without a system, these constraints are managed informally (or ignored). The Audit Head keeps a mental note or an Excel sheet. When a new person joins the audit team, institutional memory is lost. This page makes assignment management systematic, auditable, and verifiable.

The problems this page solves:

1. **Assignment tracking:** A central view of who is assigned to which branch for which audit type and when — replacing scattered email assignments.

2. **Rotation enforcement:** The system flags when an auditor has visited the same branch twice consecutively and requires the Audit Head to override with a documented reason before allowing re-assignment.

3. **Conflict-of-interest detection:** Each auditor profile lists branches where they previously worked, family relationships, or declared personal connections. The system auto-flags any assignment that involves a conflict and blocks assignment without Audit Head override.

4. **Workload balancing:** Shows each auditor's current assignment load — branches assigned this quarter, audit days committed, estimated completion. Prevents overloading one auditor while others are underutilised.

5. **Specialisation matching:** Some auditors have specific expertise — a CA-qualified auditor is better suited for financial audits; a former teacher is better suited for academic quality audits. The system records auditor specialisations and recommends appropriate assignments.

**Scale:** 3–10 auditors · 28 branches · 3–5 audit types · Quarterly assignment cycle · Conflict-of-interest registry

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Internal Audit Head | 121 | G1 | Full — create, modify, approve all assignments | Primary operator |
| Group Compliance Data Analyst | 127 | G1 | Read — workload metrics for MIS | Reporting |
| Inspection Officers / Auditors | 123, 122, 125, 126 | G1/G3 | Read — own assignments only | Assigned staff |
| Group CEO / Chairman | — | G4/G5 | Read — assignment overview | Executive |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Auditors see only their own assignments. The Audit Head sees all assignments and conflict-of-interest flags.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Auditor Assignments
```

### 3.2 Page Header
```
Auditor Assignment & Workload Manager                   [+ New Assignment]  [Auto-Assign]  [Export]
Internal Audit Head — T. Subramaniam
Sunrise Education Group · Q4 FY 2025-26 · 8 auditors · 34 assignments this quarter · 2 conflict flags
```

### 3.3 Filter Bar
```
Auditor: [All / Select ▼]    Branch: [All / Select ▼]    Audit Type: [All / Financial / Academic / Inspection / Affiliation / Grievance ▼]
Quarter: [Q4 FY 2025-26 ▼]    Status: [All / Planned / In Progress / Completed / Cancelled ▼]
                                                                            [Reset]
```

### 3.4 KPI Summary Bar

| # | KPI | Colour Logic |
|---|---|---|
| 1 | Auditors Active (this quarter) | Neutral blue |
| 2 | Assignments This Quarter | Neutral |
| 3 | Assignments Completed | Neutral green |
| 4 | Conflict-of-Interest Flags | 0 green · ≥ 1 red |
| 5 | Rotation Violations (same branch 2× consecutive) | 0 green · ≥ 1 amber |
| 6 | Overloaded Auditors (> 8 assignments/quarter) | 0 green · ≥ 1 amber |
| 7 | Branches with No Auditor Assigned (this quarter) | 0 green · ≥ 1 amber |

### 3.5 Tab Navigation
```
[Assignment Board]    [Auditor Workload]    [Conflict-of-Interest Registry]    [Rotation History]
```

---

### Tab 1 — Assignment Board

Matrix view: Auditors as rows · Branches as columns (or months — toggle).

**Branch × Auditor matrix:**

| Auditor | Sunrise HITEC City | Sunrise Jubilee Hills | Sunrise Miyapur | … | Total |
|---|---|---|---|---|---|
| S. Reddy (123) | 🔍 Inspection (Apr) | — | 🔍 Inspection (May) | … | 4 visits |
| T. Latha (122) | — | 📚 Academic (Apr) | — | … | 3 audits |
| K. Ravi (125) | 📋 Affiliation (Apr) | — | — | … | 5 audits |
| … | | | | | |

**Cell icons:**
- 🔍 Inspection visit
- 📚 Academic quality audit
- 💰 Financial audit
- 📋 Affiliation compliance audit
- ⚠️ Grievance audit (special)

**Cell colour:**
- Planned: Light blue
- In Progress: Amber
- Completed: Green
- Conflict flagged: Red border
- Same auditor as prior quarter: Orange warning border

**Cell click:** Opens Assignment Detail Drawer.

---

### Tab 2 — Auditor Workload

One row per auditor.

| Auditor | Role | Specialisation | Assignments (Q4) | Days Committed | % Capacity | Status |
|---|---|---|---|---|---|---|
| S. Reddy | Inspection Officer (123) | Physical inspection, fire safety | 8 | 16 days | 80% | ✅ Balanced |
| T. Latha | Academic Quality Officer (122) | Academic audit, teaching observation | 6 | 12 days | 60% | ✅ Balanced |
| K. Ravi | Affiliation Officer (125) | Affiliation compliance, regulatory filings | 7 | 14 days | 70% | ✅ Balanced |
| M. Srinivas | Grievance Audit Officer (126) | Grievance audit | 4 | 8 days | 40% | 🔵 Underutilised |
| P. Sunitha | Data Analyst (127) | Analytics, MIS — no field visits | 0 | 0 | 0% | N/A (non-field) |

**Capacity definition:** Each auditor has a configurable quarterly capacity in audit days. Default: 20 days/quarter (field-based roles). 100% = 20 days assigned. Colour: ≤ 80% green · 81–100% amber · > 100% red (overloaded).

**`[Auto-Assign]`** button — system suggests balanced assignment spread based on workload capacity + rotation rules + conflict-of-interest + specialisation matching.

---

### Tab 3 — Conflict-of-Interest Registry

Per auditor: list of branches where they have a declared or system-detected conflict.

**Conflict types:**
- Previously employed at branch (source: HR records)
- Family member currently employed at branch (declared)
- Personal relationship with Branch Principal (declared)
- Prior involvement in disciplinary action at branch (source: HR records)

**Table:**

| Auditor | Branch | Conflict Type | Source | Declared On | Status |
|---|---|---|---|---|---|
| S. Reddy (123) | Sunrise KPHB | Previously employed (2020–2022) | HR records | Auto-detected | Active — no assignment allowed |
| T. Latha (122) | Sunrise Begumpet | Family member (spouse — teacher) | Self-declared | 15-Jan-2026 | Active — no assignment allowed |
| K. Ravi (125) | Sunrise Jubilee Hills | Personal relationship with principal | Self-declared | 01-Mar-2026 | Active — no assignment allowed |

**`[+ Declare Conflict]`** — Auditor (or Audit Head on their behalf) declares a conflict for a branch.

**Override (Audit Head only):** If a conflict must be overridden (e.g., only one qualified auditor for a specific audit type), Audit Head can override with mandatory reason documentation. Override is logged permanently.

---

### Tab 4 — Rotation History

Shows which auditor visited which branch in prior quarters — used to enforce rotation.

**Matrix: Branches (rows) × Last 4 Quarters (columns)**

| Branch | Q1 FY 2025-26 | Q2 FY 2025-26 | Q3 FY 2025-26 | Q4 FY 2025-26 (planned) |
|---|---|---|---|---|
| Sunrise HITEC City | S. Reddy | K. Ravi | S. Reddy ⚠️ | → Recommend: T. Latha |
| Sunrise Jubilee Hills | T. Latha | T. Latha ⚠️ | K. Ravi | → Recommend: S. Reddy |
| Sunrise Miyapur | K. Ravi | S. Reddy | S. Reddy ⚠️ | → Recommend: K. Ravi (if no conflict) |

⚠️ = Same auditor as prior quarter — rotation violation. System recommendation shown.

**Rotation rule:**
- Same auditor at same branch in consecutive quarters: ⚠️ Warning — requires Audit Head override
- Same auditor at same branch 3 quarters in a row: 🔴 Block — hard stop, must change auditor

---

## 4. Drawers & Modals

### Drawer 1 — Assignment Detail Drawer (right, 720px)

**Trigger:** Click any matrix cell (Tab 1).

**Content:**
```
Assignment: S. Reddy (123) → Sunrise Miyapur
Type: Physical Inspection  ·  Quarter: Q4 FY 2025-26
Planned Date: 15-Apr-2026  ·  Status: Planned

Checklist: Branch Physical Inspection Checklist v3.2
Estimated Duration: 90 minutes

Conflict Check: ✅ No conflicts declared for this branch
Rotation Check: ⚠️ S. Reddy visited Sunrise Miyapur in Q3 also (rotation concern)
  Override reason on file: "Only qualified inspector available — K. Ravi on leave in Q4"

Prior Visits to This Branch (S. Reddy):
  Q3: Score 58%  ·  12 findings raised
  Q1: Score 52%  ·  18 findings raised

Actions:
[Edit Assignment]  [Cancel Assignment]  [Reassign to Different Auditor]
```

---

### Modal 1 — New Assignment

**Trigger:** `[+ New Assignment]`

**Form:**

| Field | Type | Notes |
|---|---|---|
| Auditor | Dropdown | Lists field auditors (123, 122, 125, 126) |
| Branch | Dropdown (multi-select for batch) | |
| Audit Type | Dropdown | Physical Inspection / Financial / Academic / Affiliation / Grievance |
| Checklist / Template | Dropdown (filtered by type) | |
| Planned Date | Date picker | |
| Quarter | Auto-filled from date | |
| Notes | Textarea | Special instructions |

**System auto-checks on selection:**
1. Conflict-of-interest flag → shows warning if conflict exists
2. Rotation check → shows warning if same auditor visited this branch last quarter
3. Workload check → shows auditor's current capacity %

If conflicts or rotation issues detected:
```
⚠️ Rotation concern: S. Reddy visited Sunrise Miyapur last quarter.
   Recommend: K. Ravi or T. Latha for this visit.
   Override reason (required if proceeding): [___________________________]
```

**Actions:** `[Create Assignment]` `[Cancel]`

---

### Modal 2 — Auto-Assign

**Trigger:** `[Auto-Assign]` button.

**System logic:**
1. For each branch requiring an audit this quarter (from P-02 Audit Calendar)
2. For each required audit type at that branch
3. Find eligible auditors: not conflicted + not assigned last quarter (rotation) + has capacity + has matching specialisation
4. Assign auditor with lowest current workload among eligible

**Preview screen before finalising:**
```
Auto-Assignment Preview — Q4 FY 2025-26

28 branches · 34 audit assignments suggested

Conflicts detected: 0
Rotation concerns overridden: 2 (reason required before finalising)
  • Sunrise Miyapur → S. Reddy (no alternative qualified inspector — K. Ravi on leave)
  • Sunrise HITEC City → K. Ravi (only affiliation-qualified auditor)

Workload balance:
  S. Reddy: 8 assignments · 80% capacity ✅
  T. Latha: 6 assignments · 60% capacity ✅
  K. Ravi: 7 assignments · 70% capacity ✅

Unassigned branches (0): None — all covered ✅
```

**Actions:** `[Finalise Assignments]` `[Adjust Manually]` `[Cancel]`

---

## 5. Charts

### Chart 1 — Workload Gauge per Auditor
- **Type:** Gauge chart (one per auditor, 5 gauges in row)
- **Scale:** 0–120% capacity
- **Colour:** 0–80% green · 81–100% amber · 101%+ red

### Chart 2 — Assignment Distribution Heatmap
- **Type:** Matrix heatmap
- **X-axis:** Quarters (last 4)
- **Y-axis:** Branches
- **Cell colour:** Based on last auditor → shows rotation variety (good = varied colours per row)

---

## 6. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Assignment created | "S. Reddy assigned to Sunrise Miyapur — Physical Inspection · 15-Apr-2026" | Success (green) |
| Conflict flagged | "⚠️ Conflict detected: S. Reddy previously employed at Sunrise KPHB — assignment blocked" | Error (red) |
| Rotation warning | "⚠️ Rotation concern: S. Reddy visited Sunrise Miyapur last quarter — override required" | Warning (amber) |
| Override recorded | "Rotation override approved — reason documented: K. Ravi on leave" | Info (blue) |
| Auto-assign complete | "34 assignments auto-generated for Q4 FY 2025-26 · 0 conflicts · 2 overrides" | Success (green) |
| Conflict declared | "Conflict of interest declared — T. Latha excluded from Sunrise Begumpet assignments" | Info (blue) |

---

## 7. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No assignments (new quarter) | Calendar outline | "No assignments for Q4 FY 2025-26 yet. Use Auto-Assign to generate or add manually." | `[Auto-Assign]` `[+ New Assignment]` |
| No conflicts in registry | Shield | "No conflicts of interest declared. All auditors are eligible for any branch assignment." | `[+ Declare Conflict]` |

---

## 8. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Assignment matrix | Skeleton grid → populated | < 1s |
| Workload gauges | Placeholder circles → gauges | < 500ms |
| Conflict registry | Skeleton rows → data | < 500ms |
| Rotation history matrix | Grid skeleton → populated | < 1s |
| Auto-assign computation | "Computing optimal assignments…" spinner | 3–10s |

---

## 9. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/assignments/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | List all assignments for period | G1+ |
| 2 | POST | `/` | Create new assignment | 121 |
| 3 | PATCH | `/{assignment_id}/` | Update assignment | 121 |
| 4 | DELETE | `/{assignment_id}/` | Cancel assignment | 121 |
| 5 | POST | `/auto-assign/` | Trigger auto-assignment for quarter | 121 |
| 6 | GET | `/auto-assign/preview/` | Preview before finalising | 121 |
| 7 | POST | `/auto-assign/finalise/` | Confirm auto-assignment | 121 |
| 8 | GET | `/workload/` | Per-auditor workload summary | G1+ |
| 9 | GET | `/rotation-history/` | Auditor × branch × quarter matrix | G1+ |
| 10 | GET | `/conflicts/` | Conflict-of-interest registry | G1+ |
| 11 | POST | `/conflicts/` | Declare new conflict | 121 |
| 12 | PATCH | `/conflicts/{conflict_id}/` | Update conflict (override) | 121 |
| 13 | GET | `/kpis/` | KPI bar aggregates | G1+ |
| 14 | GET | `/export/` | Export assignment schedule | G1+ |

---

## 10. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../assignments/kpis/"` | `#kpi-bar` | `innerHTML` | — |
| Assignment matrix | Tab 1 load | `hx-get=".../assignments/"` | `#assignment-matrix` | `innerHTML` | — |
| Workload tab | Tab 2 load | `hx-get=".../assignments/workload/"` | `#workload-content` | `innerHTML` | Gauges |
| Conflict registry | Tab 3 load | `hx-get=".../assignments/conflicts/"` | `#conflicts-content` | `innerHTML` | — |
| Rotation history | Tab 4 load | `hx-get=".../assignments/rotation-history/"` | `#rotation-content` | `innerHTML` | Matrix |
| Assignment detail | Cell click | `hx-get=".../assignments/{id}/"` | `#right-drawer` | `innerHTML` | 720px drawer |
| New assignment modal | Button click | — | `#modal-content` | `innerHTML` | Modal |
| Submit assignment | Form submit | `hx-post=".../assignments/"` | `#assign-result` | `innerHTML` | Toast + matrix update |
| Auto-assign preview | Button click | `hx-get=".../assignments/auto-assign/preview/"` | `#modal-content` | `innerHTML` | Modal |
| Finalise auto-assign | Button click | `hx-post=".../assignments/auto-assign/finalise/"` | `#assign-result` | `innerHTML` | Toast + matrix refresh |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
