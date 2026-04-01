# O-19 — Lead Assignment & Distribution

> **URL:** `/group/marketing/leads/assignment/`
> **File:** `o-19-lead-assignment-distribution.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary operator

---

## 1. Purpose

The Lead Assignment & Distribution page manages how incoming enquiries are routed from the central lead pool to individual telecallers and branch counsellors. In a large education group, 500–2,000 new leads arrive daily during peak season from 10+ channels. Without automated distribution, leads pile up unassigned while some telecallers sit idle and others are overwhelmed. Assignment speed is critical — studies in Indian education admissions show that leads contacted within 30 minutes of enquiry are 5× more likely to convert than leads contacted after 24 hours.

The problems this page solves:

1. **Speed-to-contact:** Auto-assignment rules ensure every new lead gets a telecaller within minutes, not hours. Round-robin, load-balanced, and skill-based routing eliminate manual assignment delays.

2. **Fair distribution:** Without rules, the Campaign Manager unconsciously assigns better leads (walk-ins, referrals) to favoured telecallers. The system ensures equitable distribution with configurable weighting.

3. **Skill matching:** A Telugu-speaking parent calling about Jr Inter MPC should be routed to a telecaller who speaks Telugu and knows the MPC programme — not to a Hindi-speaking telecaller handling degree enquiries. Skill-based routing matches lead attributes to telecaller capabilities.

4. **Branch routing:** Leads should ideally be handled by telecallers at or near the target branch, who know the local market, can invite for walk-ins, and speak the local language.

5. **Overflow handling:** When a telecaller is at capacity (queue full), leads overflow to the next available telecaller or to a branch pool for manual pickup.

**Scale:** 500–2,000 leads/day during peak · 5–50 telecallers · 5–50 branches · 3–5 assignment rules active simultaneously

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — configure rules, manual assign, override auto-assignments | Primary assignment manager |
| Group Admission Telecaller Executive | 130 | G3 | Read (own assignments only) — view own queue, cannot reassign | Sees result of assignment |
| Group Admission Data Analyst | 132 | G1 | Read — assignment analytics, distribution reports | Analytics |
| Group CEO / Chairman | — | G4/G5 | Read + Override — full visibility, can reassign any lead | Emergency override |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Rule configuration: role 119 or G4+. Manual assignment: role 119 or G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Lead Management  ›  Lead Assignment & Distribution
```

### 3.2 Page Header
```
Lead Assignment & Distribution                      [+ New Rule]  [Manual Assign]  [Re-distribute]  [Export]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · 8 telecallers active · 3 auto-rules running · 42 unassigned leads · Avg assignment time: 8 min
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Unassigned Leads | Integer | COUNT WHERE assigned_to IS NULL AND stage IN active | Red > 50, Amber 10–50, Green < 10 | `#kpi-unassigned` |
| 2 | Avg Assignment Time | Duration | AVG(assigned_at − created_at) for today's leads | Green ≤ 15 min, Amber 15–60 min, Red > 60 min | `#kpi-avg-time` |
| 3 | Auto-Assigned Today | Integer | COUNT WHERE assignment_method = 'auto' AND date = today | Static blue | `#kpi-auto` |
| 4 | Manual-Assigned Today | Integer | COUNT WHERE assignment_method = 'manual' AND date = today | Static grey | `#kpi-manual` |
| 5 | Queue Balance | Ratio | MAX(queue) / MIN(queue) across telecallers | Green ≤ 1.5, Amber 1.5–2.5, Red > 2.5 (imbalance) | `#kpi-balance` |
| 6 | Reassigned Today | Integer | COUNT WHERE reassigned = true AND date = today | Static amber | `#kpi-reassigned` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/leads/assignment/kpis/"` → `hx-trigger="load, every 60s"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Assignment Rules** — Configure auto-assignment logic
2. **Queue Overview** — Live telecaller queue sizes and balance
3. **Unassigned Pool** — Leads awaiting assignment
4. **Assignment Log** — History of all assignments and reassignments

### 5.2 Tab 1: Assignment Rules

Ordered list of assignment rules. Rules execute in priority order (top first). A lead matches the first rule it qualifies for.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Priority | Drag handle + # | Yes (drag) | Execution order |
| Rule Name | Text | No | Descriptive name |
| Condition | Text | No | "Source = Walk-in AND Branch = Kukatpally" |
| Assignment Method | Badge | No | Round Robin / Load Balanced / Specific Person / Branch Pool |
| Target | Text | No | Telecaller name(s) or branch |
| Max Queue | Integer | No | Max leads per telecaller before overflow |
| Leads Matched (Today) | Integer | No | How many leads hit this rule today |
| Status | Toggle | No | Active / Paused |
| Actions | Buttons | No | [Edit] [Pause/Resume] [Delete] |

**Default rules (pre-configured):**

| Rule | Condition | Method | Target |
|---|---|---|---|
| Walk-in leads | Source = Walk-in | Specific | Branch counsellor at walk-in branch |
| Hot leads (score ≥ 70) | Priority = Hot | Load Balanced | Top 3 performing telecallers |
| Branch-specific | Branch = X | Round Robin | Telecallers assigned to branch X |
| Catch-all | No condition (matches everything) | Round Robin | All active telecallers |

### 5.3 Tab 2: Queue Overview

Visual dashboard showing each telecaller's queue size and composition.

**Grid layout (1 card per telecaller):**

```
┌─────────────────────────────┐
│  Priya Reddy · Kukatpally   │
│  Status: 🟢 Online          │
│                              │
│  Queue: 62 leads             │
│  ████████████████░░░░ 78%    │
│  (Max: 80)                   │
│                              │
│  Hot: 8 · Warm: 34 · Cold: 20│
│  Overdue: 3 ⚠️               │
│                              │
│  Contact rate: 52%           │
│  Walk-ins today: 4           │
│                              │
│  [View Queue] [+ Assign]    │
└─────────────────────────────┘
```

**Queue balance bar:** Horizontal bar across all telecallers showing relative queue sizes. Ideal = equal bars. Imbalanced = visual skew.

### 5.4 Tab 3: Unassigned Pool

Leads not yet assigned to any telecaller.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Lead ID | Text | Yes | L-XXXX |
| Student Name | Text | Yes | — |
| Phone | Text | No | — |
| Branch | Text | Yes | Preferred branch |
| Source | Badge | Yes | — |
| Class | Badge | Yes | — |
| Priority | Badge | Yes | Hot / Warm / Cold |
| Created | DateTime | Yes | When lead arrived |
| Time Unassigned | Duration | Yes | How long waiting (red if > 1 hour) |
| Why Unassigned | Text | No | "No matching rule" / "All queues full" / "Off-hours" |
| Actions | Buttons | No | [Assign To ▾] |

**Bulk assign bar:** Select multiple leads → "Assign to [dropdown]" → Apply

### 5.5 Tab 4: Assignment Log

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Timestamp | DateTime | Yes | When assignment happened |
| Lead | Text | Yes | Student name + ID |
| Assigned To | Text | Yes | Telecaller name |
| Method | Badge | Yes | Auto (rule name) / Manual (by Campaign Manager) |
| Rule | Text | No | Which rule matched (if auto) |
| Previous Assignee | Text | No | If reassignment, who had it before |
| Time to Assign | Duration | Yes | Created → Assigned duration |
| Actions | Buttons | No | [View Lead] |

**Default sort:** Timestamp DESC
**Pagination:** 50/page

---

## 6. Drawers & Modals

### 6.1 Modal: `create-rule` (560px)

- **Title:** "Create Assignment Rule"
- **Fields:**
  - Rule name (text, required)
  - Priority order (auto-set to next; adjustable via drag later)
  - **Conditions (AND logic, add multiple):**
    - Field: Source / Branch / Class / Priority / Lead Score Range / Pin Code Range / Time of Day
    - Operator: Equals / Not Equals / In List / Greater Than / Less Than
    - Value: dropdown or text based on field
  - **Assignment method:**
    - Round Robin — evenly distribute across target telecallers
    - Load Balanced — assign to telecaller with smallest current queue
    - Specific Person — always assign to one telecaller
    - Branch Pool — assign to any telecaller at the lead's branch
    - Weighted — distribute with configurable weight per telecaller (e.g., senior gets 40%, junior gets 20%)
  - **Target telecallers:** Multi-select (or "All Active" or "Branch-Based")
  - **Max queue per telecaller:** Integer (default 80; overflow goes to next rule)
  - **Active hours:** Time range (e.g., 8 AM–8 PM; leads outside hours pool until next morning)
  - **Fallback:** What happens if all target queues are full? → Overflow to unassigned pool / Overflow to next rule
- **Buttons:** Cancel · Save
- **Access:** Role 119 or G4+

### 6.2 Modal: `manual-assign` (480px)

- **Title:** "Manual Lead Assignment"
- **Fields:**
  - Select leads: From unassigned pool (multi-select) or specific lead ID
  - Assign to: Telecaller dropdown (shows current queue size)
  - Override max queue: Toggle (if telecaller is at capacity)
  - Reason: Dropdown (Language Match / Specialist / VIP Lead / Rebalancing / Other)
- **Buttons:** Cancel · Assign
- **Access:** Role 119 or G4+

### 6.3 Modal: `redistribute` (560px)

- **Title:** "Redistribute Leads"
- **Purpose:** Rebalance queues when a telecaller is absent, overloaded, or underperforming
- **Fields:**
  - Source: Specific telecaller (redistribute their leads) OR "All leads" (full rebalance)
  - Target: All active telecallers / Specific subset
  - Method: Round Robin / Load Balanced
  - Include overdue only: Toggle (only redistribute leads not contacted in N days)
- **Preview:** Before/after queue sizes per telecaller
- **Buttons:** Cancel · Redistribute
- **Access:** Role 119 or G4+

### 6.4 Drawer: `telecaller-queue-detail` (640px, right-slide)

- **Tabs:** Queue · Performance · Rules Matched
- **Queue tab:** Full list of this telecaller's assigned leads with priority, stage, last action
- **Performance tab:** Key metrics — contact rate, conversion, avg response time
- **Rules Matched tab:** Which auto-assignment rules are sending leads to this telecaller
- **Footer:** [Reassign Selected] [Pause Assignments] [View in Telecalling Manager]

---

## 7. Charts

### 7.1 Queue Distribution (Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Current Queue Size by Telecaller" |
| Data | Queue size per telecaller |
| Colour | Green (< 70% capacity), Amber (70–90%), Red (> 90%) |
| Max line | Dotted vertical line at max queue capacity |
| API | `GET /api/v1/group/{id}/marketing/leads/assignment/analytics/queue-distribution/` |

### 7.2 Assignment Speed (Line)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Average Time to Assignment — Last 30 Days" |
| Data | Daily average minutes from lead creation to assignment |
| Colour | `#3B82F6` blue |
| Benchmark | 15-minute target (dashed green line) |
| API | `GET /api/v1/group/{id}/marketing/leads/assignment/analytics/assignment-speed/` |

### 7.3 Auto vs Manual Assignment (Donut)

| Property | Value |
|---|---|
| Chart type | Donut |
| Title | "Assignment Method — This Month" |
| Data | Auto / Manual / Reassigned counts |
| Colour | Auto: green / Manual: blue / Reassigned: amber |
| API | `GET /api/v1/group/{id}/marketing/leads/assignment/analytics/method-split/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Rule created | "Assignment rule '[Name]' created — priority #[N]" | Success | 3s |
| Rule paused | "Rule '[Name]' paused — leads will skip this rule" | Warning | 3s |
| Leads assigned | "[N] leads assigned to [Telecaller]" | Success | 3s |
| Auto-assigned | "[N] leads auto-assigned via rule '[Rule]'" | Info | 2s |
| Redistributed | "[N] leads redistributed across [M] telecallers" | Success | 4s |
| Queue full | "Telecaller [Name] queue is full ([N]/[Max]) — overflow to next rule" | Warning | 5s |
| All queues full | "All telecaller queues full — [N] leads in unassigned pool" | Error | 6s |
| Rule conflict | "Rule '[A]' conflicts with '[B]' — check conditions" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No assignment rules | ⚙️ | "No Assignment Rules" | "Set up auto-assignment rules to distribute leads to telecallers." | Create Rule |
| No unassigned leads | ✅ | "All Leads Assigned" | "Every lead has been routed to a telecaller." | — |
| No telecallers configured | 👥 | "No Telecallers" | "Add telecaller executives before setting up assignment rules." | — |
| No assignment history | 📋 | "No Assignments Yet" | "Assignment history will appear as leads are distributed." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + tab bar + rules table skeleton |
| Queue overview | Telecaller card grid shimmer (8 cards) |
| Unassigned pool | Table skeleton (15 rows) |
| Rule creation | Form skeleton |
| Redistribute preview | Before/after comparison shimmer |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/leads/assignment/rules/` | G1+ | List assignment rules |
| POST | `/api/v1/group/{id}/marketing/leads/assignment/rules/` | G3+ | Create rule |
| PUT | `/api/v1/group/{id}/marketing/leads/assignment/rules/{rule_id}/` | G3+ | Update rule |
| PATCH | `/api/v1/group/{id}/marketing/leads/assignment/rules/{rule_id}/toggle/` | G3+ | Activate/pause rule |
| PUT | `/api/v1/group/{id}/marketing/leads/assignment/rules/reorder/` | G3+ | Reorder rule priorities |
| DELETE | `/api/v1/group/{id}/marketing/leads/assignment/rules/{rule_id}/` | G4+ | Delete rule |
| GET | `/api/v1/group/{id}/marketing/leads/assignment/queues/` | G1+ | Queue overview (all telecallers) |
| GET | `/api/v1/group/{id}/marketing/leads/assignment/queues/{user_id}/` | G1+ | Specific telecaller queue |
| GET | `/api/v1/group/{id}/marketing/leads/assignment/unassigned/` | G1+ | Unassigned lead pool |
| POST | `/api/v1/group/{id}/marketing/leads/assignment/assign/` | G3+ | Manual assign |
| POST | `/api/v1/group/{id}/marketing/leads/assignment/redistribute/` | G3+ | Redistribute leads |
| GET | `/api/v1/group/{id}/marketing/leads/assignment/log/` | G1+ | Assignment history |
| GET | `/api/v1/group/{id}/marketing/leads/assignment/kpis/` | G1+ | KPIs |
| GET | `/api/v1/group/{id}/marketing/leads/assignment/analytics/queue-distribution/` | G1+ | Queue chart |
| GET | `/api/v1/group/{id}/marketing/leads/assignment/analytics/assignment-speed/` | G1+ | Speed trend |
| GET | `/api/v1/group/{id}/marketing/leads/assignment/analytics/method-split/` | G1+ | Method donut |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../assignment/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 60s"` |
| Tab switch | Tab click | `hx-get` with tab param | `#assignment-content` | `innerHTML` | `hx-trigger="click"` |
| Rules list | Rules tab | `hx-get=".../assignment/rules/"` | `#rules-list` | `innerHTML` | Drag reorder via SortableJS |
| Rule toggle | Toggle switch | `hx-patch=".../assignment/rules/{id}/toggle/"` | `#rule-status-{id}` | `innerHTML` | Inline badge update |
| Queue overview | Queue tab | `hx-get=".../assignment/queues/"` | `#queue-grid` | `innerHTML` | `hx-trigger="load, every 60s"` |
| Unassigned pool | Pool tab | `hx-get=".../assignment/unassigned/"` | `#unassigned-table` | `innerHTML` | `hx-trigger="load"` |
| Manual assign | Assign form | `hx-post=".../assignment/assign/"` | `#assign-result` | `innerHTML` | Toast + pool refresh |
| Redistribute | Form submit | `hx-post=".../assignment/redistribute/"` | `#redist-result` | `innerHTML` | Toast + queue refresh |
| Assignment log | Log tab | `hx-get=".../assignment/log/"` | `#log-table` | `innerHTML` | Paginated |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
