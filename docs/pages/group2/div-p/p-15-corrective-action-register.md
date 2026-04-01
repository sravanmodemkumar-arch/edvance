# P-15 — Corrective Action Register (CAPA)

> **URL:** `/group/audit/capa/`
> **File:** `p-15-corrective-action-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Process Improvement Coordinator (Role 128, G3) — primary operator

---

## 1. Purpose

The Corrective Action Register — formally called CAPA (Corrective Action / Preventive Action) — is the enforcement backbone of Division P. Every audit finding, every inspection failure, every compliance gap, every non-conformance from any module in the platform ends up here. This page ensures that findings are not just documented but closed — with root cause analysis, corrective actions, deadlines, implementation verification, and formal closure.

The fundamental problem in Indian education quality management: findings are found and then forgotten. The internal auditor visits a branch, produces a report listing 15 problems, emails it to the principal, and nothing happens. Six months later, the same auditor visits and finds 12 of the same 15 problems still unresolved. This cycle repeats year after year, creating an illusion of quality management while producing no improvement. CAPA breaks this cycle by making every finding a tracked work item with an owner, a deadline, and a verification requirement before closure.

The problems this page solves:

1. **Finding lifecycle without closure:** A finding raised in February should not still be "open" in October without explanation. CAPA tracks age of every open finding. Auto-escalation ensures that findings approaching or past their deadline surface to the right level of authority — principal, zone director, or CEO depending on severity and age.

2. **Root cause superficiality:** In Indian education, corrective actions tend to be cosmetic — "staff counselled", "principal warned", "circular issued". These actions address symptoms, not causes. CAPA enforces root cause analysis as a mandatory step before accepting a corrective action plan. The five-why methodology is embedded in the workflow.

3. **Verification gap:** A corrective action is useless unless verified. The CAPA workflow requires the Inspection Officer (123) or the Process Improvement Coordinator (128) to physically verify — through a follow-up visit, document review, or system check — that the corrective action was actually implemented, not just claimed.

4. **Preventive action neglect:** CAPA stands for "Corrective AND Preventive". Most Indian education systems only do corrective. Prevention means asking: what other branches have the same vulnerability? What systemic change prevents this problem from recurring anywhere? The CAPA module captures preventive actions explicitly.

5. **Cross-finding pattern blindness:** If the same type of finding recurs across five branches, it signals a systemic weakness — a policy gap, a training failure, or a resource constraint. The aggregate view shows finding patterns across branches and over time, enabling system-level improvement rather than branch-level firefighting.

6. **Severity mis-classification:** Not all findings are equal. A missing fire drill record is different from a fire exit blocked by furniture, which is different from a fire NOC expired by 2 years. CAPA classifies findings into Critical, Major, and Minor, with different escalation timelines and authority levels for each.

**Scale:** 5–50 branches · 500–2,000 findings/year (large group) · 50–200 (small group) · 15–25 finding categories · 6-dimension audit coverage

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Process Improvement Coordinator | 128 | G3 | Full — create, assign, update, verify, close CAPA items | Primary operator |
| Group Inspection Officer | 123 | G3 | Create findings from inspection reports; update finding status | Field source |
| Group Internal Audit Head | 121 | G1 | Read all + Approve closure of Major/Critical findings | Quality gate |
| Group Academic Quality Officer | 122 | G1 | Read + Create findings from academic audits | Academic source |
| Group Affiliation Compliance Officer | 125 | G1 | Read + Create findings from affiliation/regulatory gaps | Compliance source |
| Group Grievance Audit Officer | 126 | G1 | Read + Create findings from grievance pattern analysis | Grievance source |
| Group Compliance Data Analyst | 127 | G1 | Read — CAPA metrics for MIS reports | Reporting |
| Branch Principal | — | G3 | Read (own branch) + Update corrective action status (own branch) | Branch executor |
| Zone Director | — | G4 | Read (own zone) + Approve escalated findings | Escalation point |
| Group CEO / Chairman | — | G4/G5 | Read all + Override + Final closure of Critical items | Executive oversight |

> **Access enforcement:** `@require_role(min_level=G3, division='P')`. Branch staff see only own branch CAPA items. Finding creation: 128, 123, 122, 125, 126. Closure approval: 128 (Minor) · 121 approval required (Major) · CEO/Chairman approval required (Critical).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  CAPA Register
```

### 3.2 Page Header
```
Corrective Action Register (CAPA)                   [+ New Finding]  [Import Findings]  [Export]
Process Improvement Coordinator — K. Venkatesh
Sunrise Education Group · 28 branches · 342 open findings · 47 overdue · 12 critical
```

### 3.3 Filter Bar
```
Branch: [All / Select ▼]    Source: [All / Financial Audit / Academic Audit / Inspection / Affiliation / Grievance / Manual ▼]
Category: [All / Fire Safety / Infrastructure / Academic / HR / Finance / Hygiene / Records / Governance ▼]
Severity: [All / Critical / Major / Minor ▼]
Status: [All / Open / Root Cause Pending / Action Planned / In Progress / Verification Pending / Closed / Overdue ▼]
Assigned To: [All / Select ▼]    FY: [2025-26 ▼]    Due: [All / Overdue / Due This Week / Due This Month ▼]
                                                                                    [Reset Filters]
```

### 3.4 KPI Summary Bar

| # | KPI | Source | Colour Logic |
|---|---|---|---|
| 1 | Total Open Findings | Count with status ≠ Closed | Neutral blue |
| 2 | Critical Open | Severity = Critical, status ≠ Closed | 0 green · 1–2 amber · ≥ 3 red |
| 3 | Overdue | Past due date, not closed | 0 green · 1–10 amber · > 10 red |
| 4 | Avg Resolution Time | Mean days from raised to closed (closed items, current FY) | ≤ 14 days green · 15–30 amber · > 30 red |
| 5 | Closure Rate (FY) | % closed / total raised (current FY) | ≥ 90% green · 70–89% amber · < 70% red |
| 6 | Verification Pending | Corrective action done, awaiting verification | ≤ 10 green · 11–25 amber · > 25 red |
| 7 | Repeat Findings | Findings where same category recurred at same branch within 12 months | 0 green · 1–5 amber · > 5 red |
| 8 | Branches with Zero Overdue | Branches with no overdue CAPA items | = total branches green · else amber |

### 3.5 Tab Navigation

```
[CAPA Register]    [Kanban Board]    [Branch Summary]    [Pattern Analysis]
```

---

### Tab 1 — CAPA Register (default)

Full table of all CAPA items with lifecycle tracking.

**Table columns:**

| # | Column | Width | Content |
|---|---|---|---|
| 1 | CAPA ID | 80px | Auto-generated: `CAPA-2026-00342` |
| 2 | Branch | 130px | Branch name |
| 3 | Finding | 220px | Short description (truncated at 60 chars; hover for full) |
| 4 | Source | 100px | Icon + label: 🔍 Audit · 🏫 Inspection · 📋 Affiliation · ⚠️ Grievance |
| 5 | Category | 100px | Fire Safety / Infrastructure / Academic / HR / Finance / Hygiene / Records / Governance |
| 6 | Severity | 80px | Badge: 🔴 Critical · 🟠 Major · 🟡 Minor |
| 7 | Raised Date | 90px | dd-MMM-yyyy |
| 8 | Due Date | 90px | dd-MMM-yyyy · red if past due |
| 9 | Days Remaining | 70px | "+5 days" or "-12 days" (red) |
| 10 | Status | 110px | Badge with stage (see Status Flow below) |
| 11 | Assigned To | 110px | Branch Principal / staff member name |
| 12 | Actions | 80px | [View] · [Update] |

**Status Flow badges:**

| Status | Badge Colour | Meaning |
|---|---|---|
| Open | Grey | Finding raised, not yet acknowledged |
| Root Cause Pending | Orange | Acknowledged; awaiting root cause analysis |
| Action Planned | Blue | Root cause accepted; corrective action plan submitted |
| In Progress | Purple | Corrective action being implemented |
| Verification Pending | Amber | Action claimed done; awaiting physical/document verification |
| Closed | Green | Verified and formally closed |
| Overdue | Red | Past due date; not yet in Verification Pending or Closed |

**Row colour coding:** Critical rows have a subtle red left-border. Overdue rows have amber background.

**Sorting:** By severity (Critical first), then due date (oldest first) — default. Also: branch, source, category, raised date, days remaining.

**Pagination:** 50 rows per page.

**Bulk actions toolbar:**
```
☐ Select All    [Bulk Reassign]  [Bulk Extend Deadline]  [Export Selected]
```

---

### Tab 2 — Kanban Board

Visual pipeline view of CAPA items across lifecycle stages.

**Columns (left to right):**
```
[Open]  →  [Root Cause Pending]  →  [Action Planned]  →  [In Progress]  →  [Verification Pending]  →  [Closed]
  47            28                       35                  89                  43                       100
```

Each column shows count of items in that stage.

**Card layout per item:**
```
┌─────────────────────────────────────────────┐
│ 🔴 CAPA-2026-00289                [Critical] │
│ Fire exit blocked — Sunrise Miyapur          │
│ Due: 20-Mar-2026  ⚠️ 5 days overdue          │
│ Assigned: R. Prakash (Principal)             │
│ Source: 🏫 Inspection · Fire Safety          │
└─────────────────────────────────────────────┘
```

**Drag and drop:** Drag card to next column to advance status. Dropping triggers confirmation modal with notes field.

**Filter strip above kanban:** Branch dropdown · Severity filter · Assigned To filter.

**Columns can be collapsed** (click column header) for space management.

---

### Tab 3 — Branch Summary

One row per branch showing CAPA health metrics.

**Table columns:**

| # | Column | Content |
|---|---|---|
| 1 | Branch | Branch name |
| 2 | Open | Total open findings |
| 3 | Critical Open | Count of critical open |
| 4 | Overdue | Count of overdue |
| 5 | Closure Rate (FY) | % closed / total raised |
| 6 | Avg Resolution Days | Mean days to close |
| 7 | Repeat Findings | Recurrence count in 12 months |
| 8 | Verification Pending | Awaiting verification |
| 9 | CAPA Score | Composite health score 0–100 |
| 10 | Trend | ↑ Improving / → Stable / ↓ Degrading (vs prior quarter) |
| 11 | Actions | [View Branch CAPAs] |

**CAPA Score logic:**
```
CAPA Score = 100
  − (Critical open × 15)
  − (Overdue × 5)
  − (Repeat findings × 10)
  + (Closure rate % × 0.5)
  − (Avg resolution days > 30 ? (avg_days − 30) × 0.5 : 0)
Min: 0, Max: 100
```

**Sorting:** By CAPA Score ascending (worst branch first) — default.

---

### Tab 4 — Pattern Analysis

Aggregate view for systemic insight across branches.

**Sub-sections:**

**Section A — Finding Frequency by Category (horizontal bar)**
Categories ranked by count of open findings: Fire Safety (87) · Records (65) · Hygiene (54) · Infrastructure (48) · Academic (42) · HR (28) · Finance (18) · Governance (15)

**Section B — Recurrence Matrix**
Branches × Categories matrix showing recurrence count (how many times same category appeared at same branch in last 2 years). Cells with ≥ 3 recurrences highlighted red — indicating a systemic problem not being fixed.

**Section C — Monthly Finding Trend (line chart)**
New findings raised vs findings closed per month. If "raised" line consistently above "closed" line, backlog is growing — alert state.

**Section D — Top Repeating Findings Table**
| Finding Category | Branch | Times Recurred | Last Closed | Last Reopened |
Record keeping incomplete (Sunrise Miyapur, 4 times), Fire drill not conducted (Sunrise Begumpet, 3 times) …

---

## 4. KPI Summary Bar

(Defined in Section 3.4 above)

---

## 5. Sections

| # | Section | Location | Purpose |
|---|---|---|---|
| 1 | CAPA Register Table | Tab 1 | Full lifecycle tracking table |
| 2 | Kanban Pipeline | Tab 2 | Visual status pipeline for workflow management |
| 3 | Branch Summary | Tab 3 | Per-branch CAPA health metrics |
| 4 | Pattern Analysis | Tab 4 | Systemic finding patterns across the group |
| 5 | CAPA Detail Drawer | Right drawer | Full detail + history for one CAPA item |
| 6 | New Finding Modal | Modal | Raise a new finding manually |
| 7 | Root Cause Modal | Modal | Enter root cause analysis |
| 8 | Action Plan Modal | Modal | Submit corrective action plan |
| 9 | Verification Modal | Modal | Record verification outcome |
| 10 | Closure Modal | Modal | Formally close CAPA item |
| 11 | Escalation Modal | Modal | Escalate overdue or critical item |

---

## 6. Drawers & Modals

### Drawer 1 — CAPA Detail Drawer (right, 820px)

**Trigger:** Click any row in register or any kanban card.

**Header:**
```
CAPA-2026-00289  🔴 Critical                                   [Close] [✕]
Fire exit blocked — Sunrise Miyapur
Source: 🏫 Inspection · Fire Safety · Raised: 05-Feb-2026 · Due: 20-Mar-2026
```

**Section A — Status Timeline**
```
Stepper:
[✅ Raised 05-Feb]  →  [✅ Root Cause 10-Feb]  →  [✅ Action Planned 12-Feb]
→  [🔄 In Progress (since 12-Feb)]  →  [⬜ Verification Pending]  →  [⬜ Closed]
```

**Section B — Finding Details**

| Field | Value |
|---|---|
| CAPA ID | CAPA-2026-00289 |
| Branch | Sunrise Miyapur |
| Severity | 🔴 Critical |
| Category | Fire Safety |
| Sub-category | Fire Exit — Obstruction |
| Source | Branch Inspection (Visit #89) |
| Raised By | S. Reddy (Inspection Officer, 123) |
| Raised On | 05-Feb-2026 |
| Due Date | 20-Mar-2026 |
| Assigned To | R. Prakash (Branch Principal) |
| Finding Description | Fire exit corridor on ground floor (exit B) blocked by stacked chairs and discarded furniture. Exit door partially jammed. Students cannot evacuate through this route. Fire NOC condition #3 requires all exit routes clear at all times. |
| Evidence | 📎 inspection-photo-exit-b.jpg · 📎 inspection-report-visit89.pdf |
| Regulatory Reference | Tamil Nadu Fire Service Act, Section 14; CBSE Safety Norms 2022 Clause 8.3 |

**Section C — Root Cause Analysis**

```
Root Cause Method: 5-Why Analysis
Why 1: Fire exit blocked by chairs
  → Why: Storage space in classrooms ran out
  → Why: New furniture purchased in Jan; old furniture not disposed
  → Why: Furniture disposal process not followed
  → Why: No policy on furniture disposal timelines
  → Root Cause: Absence of infrastructure disposal policy + principal not tracking corridor compliance

Systemic Risk: Other branches may also have improper furniture storage in corridors.
Preventive Action: Audit all 28 branches for corridor obstruction during next inspection cycle.
```

Root cause submitted by: K. Venkatesh (128) · 10-Feb-2026

**Section D — Corrective Action Plan**

| # | Action Item | Owner | Deadline | Status |
|---|---|---|---|---|
| 1 | Remove all furniture from fire exit corridor immediately | R. Prakash (Principal) | 12-Feb-2026 | ✅ Done (12-Feb) |
| 2 | Repair fire exit door B — ensure functional release | Branch maintenance | 20-Feb-2026 | ✅ Done (18-Feb) |
| 3 | Conduct emergency furniture disposal via scrap dealer | Branch Admin | 28-Feb-2026 | 🔄 In Progress |
| 4 | Train all staff on corridor clearance policy (new policy P-014) | Branch Principal | 15-Mar-2026 | ⬜ Pending |

**Section E — Preventive Actions**

| Action | Scope | Owner | Deadline |
|---|---|---|---|
| Corridor obstruction audit — all 28 branches | Group-wide | S. Reddy (123) | 31-Mar-2026 |
| Issue infrastructure disposal policy (P-014) | Group-wide | K. Venkatesh (128) | 15-Feb-2026 |

**Section F — History**

| Date | Event | By |
|---|---|---|
| 20-Mar-2026 | Overdue alert sent to Zone Director | System (auto-escalation) |
| 18-Feb-2026 | Action item 2 marked complete | R. Prakash |
| 12-Feb-2026 | Action item 1 marked complete | R. Prakash |
| 12-Feb-2026 | Corrective action plan submitted | K. Venkatesh |
| 10-Feb-2026 | Root cause analysis submitted | K. Venkatesh |
| 05-Feb-2026 | Finding raised from Inspection Visit #89 | S. Reddy |

**Section G — Actions (context-sensitive by current status)**

When status = "In Progress":
```
[Mark Action Item Complete]  [Request Verification Visit]  [Escalate]  [Add Note]
```

When status = "Verification Pending":
```
[Record Verification]  [Return to In Progress]  [Escalate]
```

---

### Modal 1 — New Finding

**Trigger:** `[+ New Finding]` button.

**Form fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Dropdown | Yes | Multi-select allowed for group-wide findings |
| Severity | Radio: Critical / Major / Minor | Yes | Determines escalation and due date |
| Category | Dropdown | Yes | Fire Safety / Infrastructure / Academic / HR / Finance / Hygiene / Records / Governance |
| Sub-category | Dropdown (cascades from category) | No | |
| Source | Dropdown | Yes | Financial Audit / Academic Audit / Inspection / Affiliation / Grievance / Manual |
| Source Reference | Text / Link | No | Inspection visit ID, audit report ID, etc. |
| Finding Description | Textarea (min 50 chars) | Yes | Detailed description of non-conformance |
| Evidence | File upload (multi) | No | Photos, documents |
| Regulatory Reference | Text | No | Act/section/CBSE norm |
| Assigned To | Dropdown | Yes | Branch Principal / Staff |
| Due Date | Date picker | Yes | Auto-suggested: Critical = +7 days; Major = +30 days; Minor = +60 days |
| Notify | Checkbox list | No | Branch Principal / Zone Director / Audit Head |

**Actions:** `[Raise Finding]` `[Cancel]`

---

### Modal 2 — Root Cause Analysis

**Trigger:** `[Submit Root Cause]` from drawer when status = "Open".

**Form:**
```
5-Why Analysis
Why 1 (symptom): [_______________________]
  Why 2: [_______________________]
    Why 3: [_______________________]
      Why 4: [_______________________]
        Root Cause: [_______________________]

Summary Statement: [_______________________]

Systemic Risk Assessment:
  ☐ This problem likely exists at other branches — trigger preventive audit
  ☐ Isolated to this branch — no preventive action needed

Preventive Action (if systemic):
  Action: [_______________________]  Scope: [All branches / Zone / This branch]
  Owner: [___________]  Deadline: [Date]
```

**Actions:** `[Submit Root Cause]` `[Cancel]`

---

### Modal 3 — Action Plan

**Trigger:** `[Submit Action Plan]` when status = "Root Cause Pending".

**Form:** Dynamic list of action items. Each item:
```
Action Item: [_____________________]  Owner: [______]  Deadline: [Date]  [+ Add Another]
```

Minimum 1 item required.

**Actions:** `[Submit Plan]` `[Cancel]`

---

### Modal 4 — Record Verification

**Trigger:** `[Record Verification]` when status = "Verification Pending".

**Form:**
```
Verification Method:
  ◉ Physical Visit   ○ Document Review   ○ Photo Evidence   ○ System Check

Verified By: [K. Venkatesh (128) ▼]
Verification Date: [Today]
Visit Reference: [___________]  (if physical visit)

Outcome:
  ◉ Fully Resolved — all action items implemented and effective
  ○ Partially Resolved — some items done; re-plan required
  ○ Not Resolved — corrective actions were not implemented

Evidence: [Upload photos/documents]

Verification Notes: [___________________________]
```

If "Fully Resolved" and severity = Major/Critical → approval required (Audit Head 121 for Major; CEO/Chairman for Critical).

**Actions:** `[Submit Verification]` `[Cancel]`

---

### Modal 5 — Closure

**Trigger:** After successful verification + required approvals.

**Content:**
```
Confirm Closure — CAPA-2026-00289

Finding: Fire exit blocked — Sunrise Miyapur
Severity: 🔴 Critical
Raised: 05-Feb-2026 · Closed: 25-Mar-2026 · Resolution Time: 48 days

Verification: Physical visit · Verified by K. Venkatesh · 24-Mar-2026
Approved By: [CEO: P. Ramaiah ▼]  (required for Critical)

Closure Notes: [_________________________]
Lessons Learned: [_________________________]  (optional — feeds pattern analysis)

☐ Create preventive action for similar branches (if not already raised)
```

**Actions:** `[Close CAPA]` `[Cancel]`

---

### Modal 6 — Escalation

**Trigger:** `[Escalate]` from drawer or auto-triggered by system.

**Form:**
```
Escalate To:
  ◉ Zone Director (auto-selected based on branch)   ○ CEO   ○ Chairman

Reason:
  ◉ Overdue — [N days past deadline]
  ○ No response from assignee
  ○ Corrective action inadequate
  ○ Manual escalation

Message: [Auto-template with finding details + days overdue + requested action]

Send copy to: ☐ Audit Head   ☐ Process Improvement Coordinator
```

**Actions:** `[Send Escalation]` `[Cancel]`

---

## 7. Charts

### Chart 1 — Open vs Closed Trend (line)
- **Type:** Line chart (Chart.js 4.x)
- **X-axis:** Months (Apr–Mar, current FY)
- **Y-axis:** Count of findings
- **Series:** New findings raised (blue) + findings closed (green) + cumulative backlog (red)
- **If raised > closed sustained over 3 months:** Banner alert "CAPA backlog is growing — review capacity"
- **Location:** Tab 1 sidebar
- **API:** `GET /api/v1/group/{id}/audit/capa/charts/trend/`

### Chart 2 — Finding by Category (horizontal bar)
- **Type:** Horizontal bar (Chart.js 4.x)
- **X-axis:** Count of open findings
- **Y-axis:** Category
- **Colour:** Red for Critical-dominant categories · Orange for Major · Green for Minor
- **Hover:** Category, count, severity breakdown, avg resolution time
- **Location:** Tab 4 Pattern Analysis
- **API:** `GET /api/v1/group/{id}/audit/capa/charts/by-category/`

### Chart 3 — Resolution Time Distribution (histogram)
- **Type:** Bar chart (histogram buckets)
- **X-axis:** Resolution time buckets: 0–7 days · 8–14 · 15–30 · 31–60 · 60+ days
- **Y-axis:** Count of closed findings
- **Colour:** Green for fast resolution · Amber for moderate · Red for slow
- **Target line:** Dashed line at 30 days
- **Location:** Tab 1 sidebar or analytics panel
- **API:** `GET /api/v1/group/{id}/audit/capa/charts/resolution-distribution/`

### Chart 4 — Branch CAPA Score (bar)
- **Type:** Horizontal bar (Chart.js 4.x)
- **X-axis:** CAPA Score (0–100)
- **Y-axis:** Branch names
- **Colour:** Green ≥ 80 · Amber 50–79 · Red < 50
- **Target line:** Dashed at 80 (minimum acceptable)
- **Location:** Tab 3 Branch Summary top
- **API:** `GET /api/v1/group/{id}/audit/capa/charts/branch-scores/`

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Finding raised | "CAPA-2026-00342 raised for Sunrise Miyapur — due 20-Apr-2026" | Success (green) |
| Root cause submitted | "Root cause analysis submitted for CAPA-2026-00289" | Success (green) |
| Action plan submitted | "Corrective action plan submitted — 4 action items · due dates set" | Success (green) |
| Action item completed | "Action item 1 of 4 marked complete — CAPA-2026-00289" | Success (green) |
| Verification recorded | "Verification recorded — CAPA-2026-00289 awaiting approval for closure" | Info (blue) |
| CAPA closed | "CAPA-2026-00289 closed — 48 days · Fire exit cleared · Sunrise Miyapur" | Success (green) |
| Auto-escalation triggered | "CAPA-2026-00289 escalated to Zone Director — 5 days overdue" | Warning (amber) |
| Critical overdue | "⚠️ CRITICAL: CAPA-2026-00289 is overdue — immediate action required" | Error (red) |
| Repeat finding detected | "This finding type (Fire Safety) has occurred at Sunrise Miyapur 3 times — systemic issue flagged" | Warning (amber) |
| Bulk reassign | "12 CAPA items reassigned to K. Suresh" | Success (green) |
| Verification rejected | "Verification rejected — corrective actions not fully implemented. Returned to In Progress." | Warning (amber) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No findings (fresh setup) | Checklist with green checkmarks | "No CAPA items raised yet. Findings from audits, inspections, and compliance gaps will appear here." | `[+ Raise Finding]` |
| No open findings | Green shield icon | "Excellent — no open CAPA items. All findings have been resolved and verified." | — (positive state) |
| No findings for this branch | Branch icon with checkmark | "No CAPA items for {branch name}. This branch currently has a clean record." | — |
| No overdue findings | Clock with green tick | "No overdue CAPA items — all findings are within their resolution timeline." | — |
| Filter returns zero | Magnifying glass | "No CAPA items match your filters. Try adjusting severity, category, or status." | `[Reset Filters]` |
| No patterns found | Wavy line graph | "Not enough data to identify patterns. Patterns emerge after 3+ audit cycles." | — |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Page initial load | Skeleton: KPI bar + table rows | < 1s |
| KPI bar | 8 grey pulse cards → populated | < 500ms |
| CAPA register table | 10 skeleton rows → data | < 1s |
| Kanban board | 6 skeleton columns with cards | < 1.5s |
| Branch summary table | Skeleton rows → data | < 1s |
| Pattern analysis tab | Chart skeletons → rendered | < 1.5s |
| CAPA detail drawer | Drawer skeleton with sections | < 500ms |
| Status update | Spinner on button → confirmation | < 1s |
| Auto-escalation check | Background — no visible loader | Async |
| Chart rendering | Grey placeholder → Chart.js render | < 500ms |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/capa/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | List CAPA items (paginated, filterable) | G1+ |
| 2 | GET | `/{capa_id}/` | CAPA item detail with full history | G1+ |
| 3 | POST | `/` | Create new finding | 128, 123, 122, 125, 126, G4+ |
| 4 | PATCH | `/{capa_id}/` | Update (deadline, assigned to, status advance) | 128, Branch Principal |
| 5 | POST | `/{capa_id}/root-cause/` | Submit root cause analysis | 128 |
| 6 | POST | `/{capa_id}/action-plan/` | Submit corrective action plan | 128, Branch Principal |
| 7 | PATCH | `/{capa_id}/action-items/{item_id}/` | Mark action item complete | 128, Branch Principal |
| 8 | POST | `/{capa_id}/request-verification/` | Trigger verification workflow | 128, Branch Principal |
| 9 | POST | `/{capa_id}/verification/` | Record verification outcome | 128, 123 |
| 10 | POST | `/{capa_id}/close/` | Formally close CAPA item | 128, 121 (Major), G4+ (Critical) |
| 11 | POST | `/{capa_id}/escalate/` | Escalate to Zone Director / CEO | 128, G4+ |
| 12 | GET | `/{capa_id}/history/` | Full audit trail for CAPA item | G1+ |
| 13 | POST | `/bulk-reassign/` | Bulk reassign multiple items | 128 |
| 14 | GET | `/branch-summary/` | Per-branch CAPA health metrics | G1+ |
| 15 | GET | `/patterns/` | Finding pattern analysis | G1+ |
| 16 | GET | `/overdue/` | All overdue CAPA items | G1+ |
| 17 | GET | `/kanban/` | Kanban board data grouped by status | G1+ |
| 18 | GET | `/kpis/` | KPI bar aggregates | G1+ |
| 19 | GET | `/charts/trend/` | Chart 1 data | G1+ |
| 20 | GET | `/charts/by-category/` | Chart 2 data | G1+ |
| 21 | GET | `/charts/resolution-distribution/` | Chart 3 data | G1+ |
| 22 | GET | `/charts/branch-scores/` | Chart 4 data | G1+ |
| 23 | GET | `/export/` | Export CAPA register as Excel | G1+ |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../capa/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#capa-content` | `innerHTML` | `hx-trigger="click"` |
| Register table | Tab 1 load | `hx-get=".../capa/?page=1"` | `#capa-table-body` | `innerHTML` | Paginated |
| Filter change | Select/input change | `hx-get=".../capa/?branch={}&severity={}"` | `#capa-table-body` | `innerHTML` | Debounced |
| CAPA detail drawer | Row click | `hx-get=".../capa/{id}/"` | `#right-drawer` | `innerHTML` | 820px drawer |
| Kanban load | Tab 2 load | `hx-get=".../capa/kanban/"` | `#kanban-content` | `innerHTML` | JS drag-and-drop |
| Status advance (drag) | Kanban drop | `hx-patch=".../capa/{id}/"` | `#capa-{id}-status` | `innerHTML` | Toast + card update |
| Branch summary | Tab 3 load | `hx-get=".../capa/branch-summary/"` | `#branch-summary-content` | `innerHTML` | — |
| Pattern analysis | Tab 4 load | `hx-get=".../capa/patterns/"` | `#patterns-content` | `innerHTML` | Chart.js init |
| New finding form | `[+ New Finding]` click | — | `#modal-content` | `innerHTML` | Modal |
| Submit finding | Form submit | `hx-post=".../capa/"` | `#add-result` | `innerHTML` | Toast + table refresh |
| Root cause form | Button in drawer | `hx-get=".../capa/{id}/root-cause-form/"` | `#modal-content` | `innerHTML` | Modal |
| Submit root cause | Form submit | `hx-post=".../capa/{id}/root-cause/"` | `#capa-{id}-stage` | `innerHTML` | Toast + stepper update |
| Record verification | Button in drawer | `hx-get=".../capa/{id}/verification-form/"` | `#modal-content` | `innerHTML` | Modal |
| Escalate | Button in drawer | `hx-get=".../capa/{id}/escalate-form/"` | `#modal-content` | `innerHTML` | Modal |
| Chart load | Tab/section shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
