# P-17 — Branch Improvement Plan Builder

> **URL:** `/group/audit/improvement-plans/`
> **File:** `p-17-branch-improvement-plan.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Process Improvement Coordinator (Role 128, G3) — primary operator

---

## 1. Purpose

The Branch Improvement Plan Builder is the strategic layer above individual CAPA items. While CAPA (P-15) handles one finding at a time, a Branch Improvement Plan (BIP) is a structured, time-bound plan that addresses a cluster of related weaknesses at a branch holistically — covering root causes, interdependent actions, milestones, resource requirements, training needs, and success metrics.

A Branch Improvement Plan is typically triggered when:
- A branch has accumulated 10+ open CAPA items (signal of systemic failure)
- A branch's compliance scorecard drops below 70 (Band C — At Risk)
- A branch has had the same audit finding recur 3+ times
- An annual audit reveals multiple weaknesses across 3+ categories simultaneously
- A CEO or Chairman-level escalation demands a formal recovery plan

The problems this page solves:

1. **CAPA fragmentation vs systemic improvement:** Closing individual CAPA items does not always translate to lasting improvement. A branch that fixes 20 individual findings but never addresses the underlying culture of non-compliance will generate 20 new findings next cycle. The BIP treats the branch as a whole system, not a collection of discrete problems.

2. **No accountability for sustained improvement:** Without a formal improvement plan with milestones and named owners, progress reviews are informal and easily deferred. The BIP creates a structured review cadence — fortnightly check-ins, monthly milestone reviews, and a formal closure assessment.

3. **Resource and training gaps ignored:** Many branch compliance failures are not failures of will but failures of capacity — the branch doesn't have the staff, the tools, or the training to comply. CAPA action items rarely surface these systemic resource gaps. A BIP explicitly captures what resources, training, and support the branch needs from the group.

4. **No learning across branches:** When one branch goes through a successful improvement plan and achieves sustained compliance, that playbook should be available for other similar branches facing the same problems. The BIP library preserves completed plans as reusable templates.

5. **CEO and Board visibility:** The CEO needs to know which branches are "on a plan" — formally recognized as needing intensive support — vs which are in normal operation. The BIP dashboard provides this at a glance, with plan status, milestone completion, and score trajectory.

**Scale:** 5–50 branches · 3–10 active improvement plans at any time (large group) · 1–3 (small group) · 3–6 month typical plan duration · Quarterly milestone reviews

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Process Improvement Coordinator | 128 | G3 | Full — create, edit, manage all BIPs | Primary operator |
| Group Internal Audit Head | 121 | G1 | Read all + Approve BIP initiation and closure | Quality gate |
| Group Academic Quality Officer | 122 | G1 | Read + contribute academic improvement actions | Academic input |
| Group Affiliation Compliance Officer | 125 | G1 | Read + contribute compliance improvement actions | Compliance input |
| Group Compliance Data Analyst | 127 | G1 | Read — BIP metrics for MIS | Reporting |
| Zone Director | — | G4 | Read (own zone) + Approve zone-level resource commitments | Zone sponsor |
| Branch Principal | — | G3 | Read (own branch) + Update action item progress | Branch owner |
| Group CEO / Chairman | — | G4/G5 | Read all + Override + Close plans + Final approval | Executive sponsor |

> **Access enforcement:** `@require_role(min_level=G3, division='P')`. Branch staff see only their branch BIP. BIP creation requires 128 + Audit Head (121) approval. Closure requires CEO sign-off for Critical-trigger plans.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Improvement Plans
```

### 3.2 Page Header
```
Branch Improvement Plans                        [+ New Improvement Plan]  [Plan Templates]  [Export]
Process Improvement Coordinator — K. Venkatesh
Sunrise Education Group · 28 branches · 6 active plans · 2 on track · 3 delayed · 1 critical
```

### 3.3 Filter Bar
```
Branch: [All / Select ▼]    Status: [All / Draft / Active / On Track / Delayed / Completed / Abandoned ▼]
Trigger: [All / High CAPA Count / Low Compliance Score / Repeat Findings / Annual Audit / CEO Directive ▼]
Zone: [All / Zone 1 / Zone 2 / Zone 3 ▼]    FY: [2025-26 ▼]
                                                                        [Reset Filters]
```

### 3.4 KPI Summary Bar

| # | KPI | Source | Colour Logic |
|---|---|---|---|
| 1 | Active Plans | Plans with status = Active | Neutral blue |
| 2 | On Track | Active plans where milestone completion ≥ schedule | Green |
| 3 | Delayed | Active plans with ≥ 1 overdue milestone | ≤ 1 amber · > 1 red |
| 4 | Critical (Off Track) | Plans > 30% behind schedule | 0 green · 1 amber · ≥ 2 red |
| 5 | Avg Improvement in Score | Mean compliance score delta from plan start to current (active plans) | ≥ +10pts green · +5–9 amber · < +5 or negative red |
| 6 | Plans Completed (FY) | Closed plans with sustained improvement | Neutral green |
| 7 | Plans Abandoned (FY) | Abandoned before completion | 0 green · ≥ 1 red |

### 3.5 Tab Navigation

```
[Plan Dashboard]    [Active Plans]    [Plan Library]
```

---

### Tab 1 — Plan Dashboard (default)

Visual overview of all active branch improvement plans.

**Card grid layout:** One card per active BIP (3 cards per row on desktop).

**Card layout:**
```
┌──────────────────────────────────────────────────────────┐
│  Sunrise Miyapur Branch                    🟠 Delayed     │
│  Plan: BIP-2026-004 · Started: 01-Jan-2026               │
│  Trigger: Low Compliance Score (62%) + 14 open CAPAs     │
│  Duration: 6 months · Target Completion: 30-Jun-2026     │
│                                                           │
│  Compliance Score Trend:                                  │
│  Jan: 62% ──── Feb: 67% ──── Mar: 71%  ↑ +9 pts          │
│                                                           │
│  Milestone Progress:                                      │
│  ████████████░░░░░░░░  4 / 8 milestones complete (50%)   │
│  Expected at this date: 62%                               │
│                                                           │
│  Open Actions: 12  ·  Overdue Actions: 3                 │
│  Owner: R. Prakash (Principal)                            │
│  Coordinator: K. Venkatesh                                │
│                                                           │
│       [View Plan]  [Update Progress]  [Review Meeting]    │
└──────────────────────────────────────────────────────────┘
```

**Status badge colours:**
- 🟢 On Track — milestone completion ≥ expected
- 🟠 Delayed — milestone completion < expected by < 20%
- 🔴 Critical — milestone completion < expected by ≥ 20% or CEO-level escalation active
- ⚫ Draft — plan created, not yet activated
- ✅ Completed — all milestones achieved, plan formally closed

---

### Tab 2 — Active Plans

Table view of all active plans with sortable columns.

**Table columns:**

| # | Column | Width | Content |
|---|---|---|---|
| 1 | Plan ID | 80px | `BIP-2026-004` |
| 2 | Branch | 140px | Branch name |
| 3 | Zone | 90px | Zone name |
| 4 | Trigger | 150px | Cause of plan initiation |
| 5 | Start Date | 90px | Plan activation date |
| 6 | Target End | 90px | Planned completion date |
| 7 | Duration | 70px | Months |
| 8 | Score at Start | 70px | Compliance score when plan began |
| 9 | Current Score | 70px | Latest compliance score (colour-coded) |
| 10 | Score Delta | 70px | +/− from start |
| 11 | Milestones | 100px | 4 / 8 (50%) with mini progress bar |
| 12 | Open Actions | 70px | Count |
| 13 | Overdue Actions | 80px | Count · red if > 0 |
| 14 | Status | 90px | Badge |
| 15 | Actions | 80px | [View] · [Update] |

---

### Tab 3 — Plan Library

Repository of completed plans. Reusable as templates for similar situations.

**Table columns:**

| # | Column | Content |
|---|---|---|
| 1 | Plan ID | `BIP-2025-002` |
| 2 | Branch | Branch that executed this plan |
| 3 | Trigger | Reason plan was initiated |
| 4 | Duration | Actual months taken |
| 5 | Score Improvement | +N points from start to close |
| 6 | Key Actions | Summary of top 3 improvement initiatives |
| 7 | Outcome | Sustained / Reverted (score fell again within 6 months) |
| 8 | Lessons Learned | Key insights captured at closure |
| 9 | Actions | [View] · [Use as Template] |

---

## 4. KPI Summary Bar

(Defined in Section 3.4 above)

---

## 5. Sections

| # | Section | Location | Purpose |
|---|---|---|---|
| 1 | Plan Dashboard Cards | Tab 1 | Visual card grid for all active BIPs |
| 2 | Active Plans Table | Tab 2 | Sortable table view of active plans |
| 3 | Plan Library | Tab 3 | Completed plans as reusable templates |
| 4 | BIP Detail Page | Sub-page (full page) | Complete plan detail — goals, milestones, actions, score chart, reviews |
| 5 | New Plan Modal | Modal | Initiate a new improvement plan |
| 6 | Update Progress Modal | Modal | Record milestone/action completion |
| 7 | Review Meeting Modal | Modal | Log a formal review meeting outcome |
| 8 | Close Plan Modal | Modal | Formally close a completed plan |
| 9 | Plan Template Modal | Modal | Browse and apply a plan from the library |

---

## 6. BIP Detail Sub-Page

**URL:** `/group/audit/improvement-plans/{plan_id}/`

This is a full-page view (not a drawer) due to the volume of content.

### Header
```
Branch Improvement Plan — Sunrise Miyapur                    [Edit Plan]  [Log Review]  [Close Plan]
BIP-2026-004 · 🟠 Delayed · 01-Jan-2026 → 30-Jun-2026 (6 months)
Trigger: Compliance score 62% (Band C) + 14 open CAPA items
Plan Owner: R. Prakash (Principal) · Coordinator: K. Venkatesh · Sponsor: Zone Director V. Krishnamurthy
```

### Section 1 — Plan Overview

| Field | Value |
|---|---|
| Plan ID | BIP-2026-004 |
| Branch | Sunrise Miyapur |
| Status | 🟠 Delayed |
| Trigger | Compliance score dropped to 62% in Q3 FY26 audit; 14 open CAPA items; 3 repeat findings (Fire Safety × 2, Record Keeping × 1) |
| Plan Goal | Achieve compliance score ≥ 85% (Band A) within 6 months; close all open CAPA items; eliminate repeat findings for 12 months |
| Plan Duration | 01-Jan-2026 to 30-Jun-2026 (6 months) |
| Review Cadence | Fortnightly check-in (Coordinator + Principal); Monthly milestone review (Coordinator + Zone Director); Quarterly formal review (CEO + Audit Head) |
| Approved By | T. Subramaniam (Audit Head, 121) · 28-Dec-2025 |
| CEO Briefed | P. Ramaiah · 02-Jan-2026 |

### Section 2 — Compliance Score Trajectory

**Line chart:**
- X-axis: Months from plan start to target end
- Y-axis: Compliance score (%)
- Series: Actual score (solid blue) · Target trajectory (dashed green) · Minimum acceptable (dashed red at 70%)
- Actual: Jan 62 → Feb 67 → Mar 71
- Target: Jan 62 → Feb 68 → Mar 74 → Apr 80 → May 83 → Jun 85
- Gap at Mar: Actual 71 vs target 74 — 3 points behind → Delayed status

### Section 3 — Focus Areas

Six improvement dimensions with current score, target, and weight:

| Dimension | Score at Start | Current | Target | Weight | Actions Planned |
|---|---|---|---|---|---|
| Financial Compliance | 55% | 72% | 90% | 20% | 4 actions (2 done) |
| Academic Quality | 70% | 74% | 88% | 25% | 3 actions (1 done) |
| Safety & Infrastructure | 48% | 65% | 90% | 20% | 6 actions (2 done) |
| Affiliation Compliance | 75% | 78% | 90% | 15% | 2 actions (1 done) |
| CAPA Closure Rate | 42% | 60% | 90% | 10% | Ongoing — target 14 CAPAs closed |
| Grievance Resolution | 68% | 71% | 85% | 10% | 2 actions (0 done) |

### Section 4 — Milestones

| # | Milestone | Target Date | Status | Completion Date | Notes |
|---|---|---|---|---|---|
| 1 | All fire exit corridors cleared and verified | 15-Jan-2026 | ✅ Done | 12-Jan-2026 | Inspection verified 13-Jan |
| 2 | Fire drill conducted and recorded | 31-Jan-2026 | ✅ Done | 28-Jan-2026 | — |
| 3 | 8 oldest CAPA items closed | 28-Feb-2026 | ✅ Done | 02-Mar-2026 | 2 days late |
| 4 | Fee reconciliation audit cleared | 28-Feb-2026 | ✅ Done | 25-Feb-2026 | — |
| 5 | Staff training — record keeping completed | 15-Mar-2026 | 🟠 Delayed | — | Trainer availability issue |
| 6 | All remaining 6 CAPA items closed | 31-Mar-2026 | ⬜ Pending | — | — |
| 7 | Compliance score reaches 80% | 30-Apr-2026 | ⬜ Pending | — | — |
| 8 | Final audit — score ≥ 85% (formal closure) | 30-Jun-2026 | ⬜ Pending | — | — |

**Milestone progress bar:** 4 / 8 (50%) — Expected at this date: 5 / 8 (62%). Status: Delayed.

### Section 5 — Action Items

Full table of all improvement actions (more granular than milestones).

| # | Action | Dimension | Owner | Deadline | Status | Linked CAPA |
|---|---|---|---|---|---|---|
| 1 | Clear fire exit corridor B | Safety | R. Prakash | 12-Jan | ✅ Done | CAPA-2026-00289 |
| 2 | Repair fire exit door B | Safety | Maintenance | 20-Jan | ✅ Done | CAPA-2026-00289 |
| 3 | Conduct emergency fire drill | Safety | R. Prakash | 31-Jan | ✅ Done | — |
| 4 | Install fire extinguisher in lab corridor | Safety | Admin | 28-Feb | ✅ Done | CAPA-2026-00301 |
| 5 | Fee ledger reconciliation for Apr–Sep | Finance | Accountant | 28-Feb | ✅ Done | CAPA-2026-00310 |
| 6 | Staff record-keeping training workshop | Records | K. Venkatesh | 15-Mar | 🟠 Delayed | — |
| 7 | Install CCTV in corridor 3 | Safety | Admin | 31-Mar | 🔄 In Progress | CAPA-2026-00318 |
| 8 | Update lesson plan submission process | Academic | HoD Sciences | 31-Mar | ⬜ Pending | CAPA-2026-00325 |
| 9 | Close 6 remaining CAPA items | Multiple | R. Prakash | 31-Mar | ⬜ Pending | Multiple |
| 10 | Parent grievance response SLA training | Grievance | Admin | 30-Apr | ⬜ Pending | — |
| 11 | CBSE affiliation document bundle refresh | Affiliation | 125 | 30-Apr | ⬜ Pending | — |
| 12 | Final compliance re-audit | All | S. Reddy (123) | 25-Jun | ⬜ Pending | — |

**`[+ Add Action Item]`** button for adding actions mid-plan.

### Section 6 — Resources Required

| Resource | Type | Quantity / Cost | Status | Provided By |
|---|---|---|---|---|
| CCTV installation (corridor 3) | Infrastructure | ₹35,000 | ✅ Approved | Group HQ (Capex) |
| Fire extinguisher (lab corridor) | Infrastructure | ₹4,500 | ✅ Procured | Branch budget |
| Record-keeping training (external trainer) | Training | ₹15,000 | 🟠 Pending approval | Group HQ |
| Dedicated admin support (2 days/week for 2 months) | Staff | Internal | ✅ Assigned | Zone HR |

### Section 7 — Review Meeting Log

| # | Meeting Date | Attendees | Milestone Status at Meeting | Key Decisions | Next Steps |
|---|---|---|---|---|---|
| 1 | 15-Jan-2026 | K. Venkatesh, R. Prakash | 1 done / 8 · On Track | Fire exit cleared early — celebrate small win | Begin CAPA closure sprint |
| 2 | 01-Feb-2026 | K. Venkatesh, R. Prakash | 2 done / 8 · On Track | Fire drill completed — recorded | Focus on finance reconciliation |
| 3 | 15-Feb-2026 | K. Venkatesh, R. Prakash, V. Krishnamurthy (ZD) | 3 done / 8 · On Track | Monthly review — on track | Confirm training workshop date |
| 4 | 01-Mar-2026 | K. Venkatesh, R. Prakash | 4 done / 8 · Delayed by 1 | Milestone 5 delayed — trainer rescheduled | Reschedule to 25-Mar; request approval for ₹15K |
| 5 | 15-Mar-2026 | K. Venkatesh, R. Prakash | 4 done / 8 · Delayed | Training still pending — request expedited approval | CEO briefed; trainer confirmed for 25-Mar |

**`[+ Log Review Meeting]`** button.

### Section 8 — Lessons Learned (at closure)

Filled in when plan is formally closed.

Fields: What worked · What didn't work · Root systemic change achieved · Risk of regression · Recommended actions for sustainment · Share with: [Select branches similar in profile]

---

## 7. Modals

### Modal 1 — New Improvement Plan

**Trigger:** `[+ New Improvement Plan]` button.

**Form — Step 1: Plan Setup**

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Dropdown | Yes | One branch per plan |
| Trigger | Multi-select | Yes | High CAPA Count / Low Compliance Score / Repeat Findings / Annual Audit / CEO Directive |
| Compliance Score at Start | Number (auto-pulled from P-10) | Yes | Current branch compliance score |
| Open CAPAs at Start | Number (auto-pulled from P-15) | Yes | Count of open CAPA items |
| Plan Goal | Textarea | Yes | Target score, target CAPA closure, key outcomes |
| Plan Duration | Dropdown: 3 / 4 / 6 / 9 / 12 months | Yes | |
| Plan Start Date | Date picker | Yes | |
| Plan Owner (Branch) | Dropdown | Yes | Branch Principal or designated lead |
| Zone Sponsor | Dropdown (auto from branch zone) | Yes | Zone Director |
| Review Cadence | Multi-select | Yes | Fortnightly check-in / Monthly milestone / Quarterly formal |
| Load from Template | Dropdown | No | Pre-load milestones and actions from Plan Library |

**Form — Step 2: Milestones**
Add milestones in sequence with name, target date, success criteria.

**Form — Step 3: Action Items**
Add improvement actions linked to milestones with owner and deadline.

**Form — Step 4: Resources**
Declare resources required (infrastructure, training, staff support) with cost estimates and approval status.

**Form — Step 5: Review & Activate**
Summary of plan before activation. Requires Audit Head (121) approval to change status from Draft to Active.

---

### Modal 2 — Update Progress

**Trigger:** `[Update Progress]` from card or table row.

**Form:**
```
Plan: BIP-2026-004 · Sunrise Miyapur

Update Action Items:
  ☐ Staff record-keeping training workshop [Mark Done] [Reschedule]
  ☐ Install CCTV in corridor 3 [Mark Done] [Reschedule]
  ...

Update Milestones:
  [Milestone 5 — Staff training] — [Mark Done] / [Mark Delayed — new date: ___]

Compliance Score Update:
  Latest score from P-10: [Auto-pull] or [Enter manually: ____]

Notes: [___________________________]
```

---

### Modal 3 — Log Review Meeting

**Form:**
```
Meeting Date: [Date]    Type: [Fortnightly / Monthly / Quarterly ▼]
Attendees: [Multi-select roles + names]
Milestone Status at This Meeting: [Auto-pulled — editable]
Key Decisions: [___________________________]
Next Steps: [___________________________]
Issues Raised: [___________________________]
Next Review Date: [Date]
```

---

### Modal 4 — Close Plan

**Trigger:** `[Close Plan]` from BIP detail page.

**Form:**
```
Closure Type:
  ◉ Successfully Completed — all goals achieved
  ○ Partially Completed — closed with accepted partial outcome
  ○ Abandoned — plan not viable; new approach needed

Final Compliance Score: [___]  (auto-pulled from P-10)
Score Improvement: +N points from start
Milestones Completed: N / M
Open CAPAs at Closure: N (should ideally be 0)

Closure Assessment:
  ◉ Sustained improvement expected
  ○ Risk of regression — recommend enhanced monitoring for 6 months

Lessons Learned: [___________________________]
Share with Other Branches: ☐ Yes — add to Plan Library as template

Approved By: [Audit Head ▼] (required) + [CEO ▼] (required for critical-trigger plans)
```

---

## 8. Charts

### Chart 1 — Compliance Score Trajectory (line)
- **Type:** Line (Chart.js 4.x) — per-plan chart in BIP detail
- **Series:** Actual · Target · Minimum acceptable (70%)
- **Updates:** Monthly when new compliance score recorded

### Chart 2 — Milestone Completion Rate (horizontal bar — all active plans)
- **Type:** Horizontal bar
- **X-axis:** Completion % (0–100%)
- **Y-axis:** Branch names
- **Colour:** Green ≥ target · Amber < target by < 20% · Red < target by ≥ 20%
- **API:** `GET /api/v1/group/{id}/audit/improvement-plans/charts/milestone-rates/`

### Chart 3 — Score Improvement Across All Plans (grouped bar)
- **Type:** Grouped bar
- **X-axis:** Branches with active/completed plans
- **Y-axis:** Score (%)
- **Groups:** Score at start (grey) · Current score (blue) · Target score (dashed line)
- **API:** `GET /api/v1/group/{id}/audit/improvement-plans/charts/score-comparison/`

---

## 9. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Plan created | "BIP-2026-004 created for Sunrise Miyapur · 6-month plan · 8 milestones" | Success (green) |
| Plan activated | "BIP-2026-004 activated — improvement plan now live" | Success (green) |
| Milestone completed | "Milestone 3 completed — BIP-2026-004 · Sunrise Miyapur · 4 of 8 done" | Success (green) |
| Milestone delayed | "Milestone 5 marked delayed — new date: 25-Mar-2026" | Warning (amber) |
| Action item done | "Action: Staff training workshop marked complete" | Success (green) |
| Review meeting logged | "Review meeting logged — 15-Mar-2026 · 4 attendees" | Info (blue) |
| Plan completed | "BIP-2026-004 closed — Sunrise Miyapur · +23 points improvement · Goal achieved" | Success (green) |
| Plan critical alert | "⚠️ BIP-2026-004 is critically off track — CEO has been notified" | Error (red) |
| Resource approved | "₹15,000 training budget approved for BIP-2026-004" | Success (green) |

---

## 10. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No active plans | Branch with green badge | "No active improvement plans — all branches are in normal compliance operation." | `[+ New Improvement Plan]` |
| No completed plans (library) | Empty bookshelf | "No completed plans in the library yet. Completed plans become reusable templates." | — |
| Filter returns zero | Magnifying glass | "No improvement plans match your filters." | `[Reset Filters]` |

---

## 11. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Plan dashboard cards | 3 skeleton cards per row → populated | < 1s |
| KPI bar | 7 pulse cards → data | < 500ms |
| BIP detail page | Section skeletons with chart placeholders | < 1s |
| Score trajectory chart | Grey placeholder → Chart.js | < 500ms |
| Action items table | Skeleton rows → data | < 500ms |

---

## 12. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/improvement-plans/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | List improvement plans (filterable) | G1+ |
| 2 | GET | `/{plan_id}/` | BIP detail — full plan | G1+ |
| 3 | POST | `/` | Create new BIP | 128, G4+ |
| 4 | PATCH | `/{plan_id}/` | Update plan metadata | 128 |
| 5 | POST | `/{plan_id}/activate/` | Activate draft plan | 128 + 121 approval |
| 6 | GET | `/{plan_id}/milestones/` | Milestones list | G1+ |
| 7 | POST | `/{plan_id}/milestones/` | Add milestone | 128 |
| 8 | PATCH | `/{plan_id}/milestones/{m_id}/` | Update milestone (complete/delay) | 128, Branch Principal |
| 9 | GET | `/{plan_id}/actions/` | Action items list | G1+ |
| 10 | POST | `/{plan_id}/actions/` | Add action item | 128, Branch Principal |
| 11 | PATCH | `/{plan_id}/actions/{a_id}/` | Update action status | 128, Branch Principal |
| 12 | POST | `/{plan_id}/reviews/` | Log review meeting | 128 |
| 13 | GET | `/{plan_id}/reviews/` | Review meeting history | G1+ |
| 14 | POST | `/{plan_id}/close/` | Close plan | 128 + 121 + G4 (critical) |
| 15 | GET | `/library/` | Plan library (completed plans) | G1+ |
| 16 | POST | `/library/{plan_id}/use-as-template/` | Copy plan structure to new BIP | 128 |
| 17 | GET | `/kpis/` | KPI bar aggregates | G1+ |
| 18 | GET | `/charts/milestone-rates/` | Chart 2 data | G1+ |
| 19 | GET | `/charts/score-comparison/` | Chart 3 data | G1+ |
| 20 | GET | `/export/` | Export all BIPs as Excel | G1+ |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../improvement-plans/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#bip-content` | `innerHTML` | — |
| Plan dashboard | Tab 1 load | `hx-get=".../improvement-plans/?status=active"` | `#plan-cards` | `innerHTML` | Card grid |
| Active plans table | Tab 2 load | `hx-get=".../improvement-plans/?view=table"` | `#plan-table` | `innerHTML` | Sortable |
| Plan library | Tab 3 load | `hx-get=".../improvement-plans/library/"` | `#library-content` | `innerHTML` | — |
| BIP detail navigate | `[View Plan]` click | — | Full page navigation | — | Sub-page `/plans/{id}/` |
| Milestone update | Checkbox check + confirm | `hx-patch=".../milestones/{id}/"` | `#milestone-{id}` | `innerHTML` | Inline update |
| Action item update | Checkbox check | `hx-patch=".../actions/{id}/"` | `#action-{id}` | `innerHTML` | Inline update |
| New plan form | Button click | — | `#modal-content` | `innerHTML` | Multi-step modal |
| Submit plan | Form submit | `hx-post=".../improvement-plans/"` | `#plan-result` | `innerHTML` | Toast + card refresh |
| Log review | Form submit | `hx-post=".../plans/{id}/reviews/"` | `#review-result` | `innerHTML` | Toast + list update |
| Score chart | BIP detail load | `hx-get` chart endpoint | `#score-chart` | `innerHTML` | Chart.js |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
