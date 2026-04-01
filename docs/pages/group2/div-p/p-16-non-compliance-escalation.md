# P-16 — Non-Compliance Escalation Manager

> **URL:** `/group/audit/capa/escalations/`
> **File:** `p-16-non-compliance-escalation.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Process Improvement Coordinator (Role 128, G3) — primary operator

---

## 1. Purpose

The Non-Compliance Escalation Manager governs the formal escalation workflow for CAPA items and compliance failures that are not being resolved within acceptable timelines or at the appropriate authority level. While the CAPA Register (P-15) tracks the lifecycle of every finding, this page is dedicated to the escalation sub-system — who escalated what, to whom, when, with what outcome, and whether the escalation itself triggered resolution.

In Indian education management, the most common failure mode is not the absence of a process but the absence of consequences when the process is ignored. A branch principal who knows that an overdue audit finding will never reach the CEO has little urgency to resolve it. Escalation changes this calculus: when the CEO starts receiving weekly emails listing unresolved findings at a branch, principals prioritise resolution. This page makes the escalation mechanism transparent, trackable, and systematic.

The problems this page solves:

1. **Invisible escalation history:** Without a dedicated escalation log, it is impossible to know whether an issue was ever escalated, to whom it went, what response came back, and whether the escalation drove resolution. This page creates a full audit trail for every escalation event.

2. **Escalation fatigue and bypass:** If too many items escalate to the CEO, the signal is lost in noise. The escalation rules enforce a hierarchy: Minor findings escalate to Branch Principal → Zone Director → CEO only if still unresolved after two levels. Critical findings skip directly to CEO. This page shows which escalations followed the correct path and which bypassed levels.

3. **Escalation without response tracking:** An escalation that receives no acknowledgement within 48 hours should itself trigger a higher-level escalation. The system tracks response time at each escalation level and re-escalates automatically if no response is recorded.

4. **Manual vs system escalation mix:** Some escalations are triggered automatically by the system (overdue rules), others are manually triggered by the Process Improvement Coordinator or Audit Head. This page tracks both with clear labelling.

5. **Escalation effectiveness measurement:** If the same item is escalated three times and still unresolved, the escalation mechanism itself is failing. Escalation effectiveness rate — percentage of escalations that result in finding closure within 14 days of escalation — is a key platform health metric.

6. **Branch-level escalation pattern:** A branch that consistently generates escalations (has findings that never resolve without CEO intervention) has a leadership problem, not a compliance problem. The branch escalation heat map makes this visible.

**Scale:** 5–50 branches · 50–300 escalations/year (large group) · 10–60 (small group) · 3-level escalation hierarchy · Auto-escalation rules engine

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Process Improvement Coordinator | 128 | G3 | Full — view all escalations, trigger manual escalations, record responses | Primary operator |
| Group Internal Audit Head | 121 | G1 | Read all + Receive escalations as target | Escalation recipient |
| Group Academic Quality Officer | 122 | G1 | Read all escalations | Advisory |
| Group Compliance Data Analyst | 127 | G1 | Read — escalation metrics for MIS | Reporting |
| Zone Director | — | G4 | Read (own zone) + Acknowledge + Respond to escalations addressed to them | Escalation target |
| Group CEO / Chairman | — | G4/G5 | Read all + Respond to all escalations + Override | Escalation target |
| Branch Principal | — | G3 | Read (own branch) — see escalations raised about their branch | Awareness |

> **Access enforcement:** `@require_role(min_level=G3, division='P')`. Branch staff see only read access for own branch escalations. Manual escalation trigger: 128, 121, G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  CAPA Register  ›  Escalations
```

### 3.2 Page Header
```
Non-Compliance Escalation Manager                   [+ Manual Escalation]  [Export]
Process Improvement Coordinator — K. Venkatesh
Sunrise Education Group · 28 branches · 34 active escalations · 8 awaiting response · 3 re-escalated
```

### 3.3 Filter Bar
```
Branch: [All / Select ▼]    Level: [All / Level 1 — Zone Director / Level 2 — Audit Head / Level 3 — CEO / Chairman ▼]
Type: [All / Auto / Manual ▼]    Status: [All / Sent / Acknowledged / Response Given / Resolved / Re-escalated / Ignored ▼]
CAPA Severity: [All / Critical / Major / Minor ▼]    Date Range: [This Month ▼]
                                                                                    [Reset Filters]
```

### 3.4 KPI Summary Bar

| # | KPI | Source | Colour Logic |
|---|---|---|---|
| 1 | Active Escalations | Escalations with status ≠ Resolved | Neutral blue |
| 2 | Awaiting Response | Sent but no acknowledgement within 48 hrs | 0 green · 1–5 amber · > 5 red |
| 3 | Re-escalated | Escalated again after no action | 0 green · 1–3 amber · > 3 red |
| 4 | Escalation Effectiveness Rate | % escalations where CAPA closed within 14 days of escalation | ≥ 80% green · 60–79% amber · < 60% red |
| 5 | Avg Response Time | Mean hours from escalation sent to acknowledgement | ≤ 24h green · 25–72h amber · > 72h red |
| 6 | CEO-Level Escalations (Active) | Escalations currently at CEO / Chairman level | 0 green · 1–3 amber · > 3 red |
| 7 | Branches with Repeat Escalations | Branches escalated 3+ times in rolling 6 months | 0 green · 1–3 amber · > 3 red |

### 3.5 Tab Navigation

```
[Active Escalations]    [Escalation History]    [Rules Engine]    [Analytics]
```

---

### Tab 1 — Active Escalations (default)

All currently unresolved escalations requiring attention.

**Table columns:**

| # | Column | Width | Content |
|---|---|---|---|
| 1 | Escalation ID | 80px | `ESC-2026-00089` |
| 2 | CAPA ID | 90px | Linked: `CAPA-2026-00289` |
| 3 | Branch | 130px | Branch name |
| 4 | Finding Summary | 200px | Truncated at 60 chars |
| 5 | CAPA Severity | 80px | 🔴 Critical · 🟠 Major · 🟡 Minor |
| 6 | Escalation Level | 100px | L1 (Zone Director) · L2 (Audit Head) · L3 (CEO) · L3+ (Chairman) |
| 7 | Escalated To | 130px | Person name + role |
| 8 | Escalated On | 90px | dd-MMM-yyyy HH:mm |
| 9 | Type | 70px | 🤖 Auto · ✋ Manual |
| 10 | Response Status | 120px | Badge: Sent / Acknowledged / Response Given / Ignored |
| 11 | Days Since Escalated | 70px | Number · red if > 3 days without acknowledgement |
| 12 | Actions | 80px | [View] · [Re-escalate] · [Mark Resolved] |

**Colour coding:** Rows escalated to CEO/Chairman have a distinct dark-red left border. Rows with no acknowledgement > 48 hours have amber background.

---

### Tab 2 — Escalation History

Full log of all escalations — active and resolved.

**Table:** Same columns as Tab 1 plus:
- **Resolution Date** — when underlying CAPA was closed
- **Resolution Time (days)** — from escalation to closure
- **Effective?** — ✅ Yes (closed ≤ 14 days) / ❌ No (closed > 14 days or still open)

**Pagination:** 100 rows per page.

---

### Tab 3 — Rules Engine

Configuration of the auto-escalation rules that drive the system. Managed by G4/G5 only.

**Rules table:**

| # | Rule Name | Trigger | Level | Recipient | Enabled |
|---|---|---|---|---|---|
| 1 | Critical Overdue — Day 1 | Critical CAPA past due date by 1+ day | L3 | CEO | ✅ |
| 2 | Major Overdue — Day 7 | Major CAPA past due date by 7+ days | L1 | Zone Director | ✅ |
| 3 | Major Overdue — Day 21 | Major CAPA past due date by 21+ days | L2 | Audit Head | ✅ |
| 4 | Major Overdue — Day 35 | Major CAPA past due date by 35+ days | L3 | CEO | ✅ |
| 5 | Minor Overdue — Day 14 | Minor CAPA past due date by 14+ days | L1 | Zone Director | ✅ |
| 6 | Minor Overdue — Day 45 | Minor CAPA past due date by 45+ days | L2 | Audit Head | ✅ |
| 7 | No Root Cause — Day 5 | CAPA raised 5+ days ago, root cause not submitted | L1 | Zone Director | ✅ |
| 8 | No Action Plan — Day 10 | Root cause submitted 10+ days ago, no action plan | L1 | Zone Director | ✅ |
| 9 | No Escalation Acknowledgement — 48 hrs | Escalation sent, no acknowledgement within 48 hours | L+ 1 | Next level up | ✅ |
| 10 | Repeat Finding — 3rd Occurrence | Same finding category at same branch for 3rd time | L2 | Audit Head | ✅ |

**Each rule row has:** [Edit] · [Disable/Enable] · [Test Rule]

**`[+ Add Custom Rule]`** — for group-specific escalation logic.

**Rule Edit Form fields:**
- Trigger condition (dropdown: Overdue days / No root cause / No action / Repeat finding / Manual)
- Severity filter (Critical / Major / Minor / All)
- Days threshold
- Escalation level (L1 / L2 / L3 / L3+)
- Recipients (role-based auto-resolve + manual override)
- Message template (editable)
- Include CAPA details in message (checkbox)
- CC recipients (optional)

---

### Tab 4 — Analytics

**Section A — Escalation Volume by Month (bar chart)**
Monthly count of escalations raised. Broken down by: Auto (blue) / Manual (purple). If escalation volume is trending up, it signals deteriorating CAPA closure discipline.

**Section B — Escalation by Level Distribution (doughnut)**
What percentage of escalations are at L1 / L2 / L3. A healthy distribution has most at L1, few at L3. Inverted distribution (most at CEO level) indicates systemic CAPA failure.

**Section C — Effectiveness Rate Trend (line)**
Escalation effectiveness rate (% closed within 14 days) per month. Target: ≥ 80%.

**Section D — Branch Escalation Heatmap (matrix)**
Branches × months matrix. Cell = count of escalations in that branch-month. Chronically hot cells (red) = branches with structural compliance leadership problems.

**Section E — Top Escalated Branches Table**
| Branch | Total Escalations (FY) | CEO-Level Escalations | Avg Response Time | Effectiveness Rate |
Sorted by total escalations descending.

---

## 4. KPI Summary Bar

(Defined in Section 3.4 above)

---

## 5. Sections

| # | Section | Location | Purpose |
|---|---|---|---|
| 1 | Active Escalations Table | Tab 1 | Real-time view of unresolved escalations |
| 2 | Escalation History | Tab 2 | Full historical log with effectiveness tracking |
| 3 | Rules Engine | Tab 3 | Configuration of auto-escalation triggers |
| 4 | Analytics | Tab 4 | Patterns, trends, and effectiveness measurement |
| 5 | Escalation Detail Drawer | Right drawer | Full detail for one escalation event |
| 6 | Manual Escalation Modal | Modal | Trigger a non-automated escalation |
| 7 | Record Response Modal | Modal | Log the recipient's response/action |
| 8 | Re-escalate Modal | Modal | Escalate to the next authority level |
| 9 | Rule Edit Modal | Modal | Configure or modify an escalation rule |

---

## 6. Drawers & Modals

### Drawer 1 — Escalation Detail Drawer (right, 780px)

**Trigger:** Click any row in Tab 1 or Tab 2.

**Header:**
```
ESC-2026-00089  L3 — CEO Level  🤖 Auto                        [Re-escalate] [Mark Resolved] [✕]
CAPA-2026-00289 · Fire exit blocked · Sunrise Miyapur · 🔴 Critical
```

**Section A — Escalation Chain**
```
Timeline of escalations for this CAPA item:

L1  ─  Zone Director (V. Krishnamurthy)
        Escalated: 21-Feb-2026 (auto — Major overdue day 7)
        Acknowledged: 22-Feb-2026 (within 18 hours ✅)
        Response: "Spoke to principal. Will resolve by 28-Feb."
        Outcome: Not resolved by 28-Feb → triggered L2 escalation

L2  ─  Audit Head (T. Subramaniam)
        Escalated: 07-Mar-2026 (auto — Major overdue day 21)
        Acknowledged: 07-Mar-2026 (within 4 hours ✅)
        Response: "Visited branch on 09-Mar. Principal has ordered chairs cleared."
        Outcome: Not fully resolved → triggered L3 escalation

L3  ─  CEO (P. Ramaiah)    ← CURRENT
        Escalated: 21-Mar-2026 (auto — Major overdue day 35)
        Acknowledged: ❌ No acknowledgement (2 days — re-escalation pending)
        Response: —
        Outcome: Pending
```

**Section B — CAPA Summary**
Quick view of the linked finding, root cause, action plan status, and due date. Link to full CAPA item (P-15).

**Section C — Message Sent**
```
Subject: URGENT – Unresolved CAPA Finding · CAPA-2026-00289 · 35 Days Overdue · Sunrise Miyapur

Dear P. Ramaiah (CEO),

The following critical safety finding remains unresolved after 35 days:

Finding: Fire exit corridor (exit B) blocked — Sunrise Miyapur
Severity: CRITICAL
Raised: 05-Feb-2026   Due: 20-Mar-2026   Days Overdue: 35
Corrective Action Plan: Submitted (12-Feb-2026)
Current Status: In Progress — furniture disposal still pending

Previous escalations:
  ✅ L1 (Zone Director, 21-Feb): Acknowledged. Resolution promised by 28-Feb. Not delivered.
  ✅ L2 (Audit Head, 07-Mar): Acknowledged. Visit conducted 09-Mar. Still pending.

Action Required: Please direct Branch Principal R. Prakash to complete furniture disposal
and implement the full corrective action plan by 25-Mar-2026.

This is a fire safety risk and may affect CBSE affiliation standing.

— K. Venkatesh, Process Improvement Coordinator (Auto-triggered by rules engine)
```

**Section D — Actions**
```
[Record Response]  [Re-escalate to Chairman]  [Mark CAPA Resolved]  [Add Internal Note]
```

---

### Modal 1 — Manual Escalation

**Trigger:** `[+ Manual Escalation]` button.

**Form fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| CAPA Item | Searchable dropdown | Yes | Search by CAPA ID, branch, or finding |
| Escalation Level | Radio | Yes | L1 (Zone Director) / L2 (Audit Head) / L3 (CEO) / L3+ (Chairman) |
| Reason | Dropdown | Yes | No root cause submitted / No action plan / Insufficient action / Pattern of non-compliance / Urgent safety risk / Manual override |
| Message | Textarea | Yes | Pre-populated template; editable |
| CC | Multi-select roles | No | Additional recipients |
| Priority | Radio | No | Normal / Urgent (adds URGENT prefix to subject) |
| Attach CAPA Report | Checkbox | No | Attach full CAPA detail PDF to escalation email |

**Actions:** `[Send Escalation]` `[Cancel]`

---

### Modal 2 — Record Response

**Trigger:** `[Record Response]` from drawer.

**Form:**
```
Escalation: ESC-2026-00089  →  CEO (P. Ramaiah)
Escalated On: 21-Mar-2026

Response Received Via:
  ◉ Email   ○ WhatsApp   ○ Phone Call   ○ In-Person Meeting   ○ Platform Notification

Responded On: [Date] [Time]
Response Summary: [____________________________]
Committed Action: [____________________________]
Committed Deadline: [Date]
```

**Actions:** `[Save Response]` `[Cancel]`

---

### Modal 3 — Re-escalate

**Trigger:** `[Re-escalate]` from row or drawer.

**Form:**
```
Current Level: L2 — Audit Head (T. Subramaniam)
New Level: L3 — CEO (P. Ramaiah)  [auto-filled, editable]

Re-escalation Reason:
  ◉ No acknowledgement within 48 hours
  ○ Acknowledged but no action taken
  ○ Insufficient action — finding still unresolved
  ○ Manual re-escalation

Message: [Auto-template referencing prior escalation history — editable]
```

**Actions:** `[Re-escalate]` `[Cancel]`

---

## 7. Charts

### Chart 1 — Escalations by Month (grouped bar)
- **Type:** Grouped bar (Chart.js 4.x)
- **X-axis:** Months (Apr–Mar, current FY)
- **Y-axis:** Count
- **Groups:** Auto escalations (blue) vs manual escalations (purple)
- **Hover:** Month, auto count, manual count, total
- **API:** `GET /api/v1/group/{id}/audit/escalations/charts/monthly/`

### Chart 2 — Escalation Level Distribution (doughnut)
- **Type:** Doughnut (Chart.js 4.x)
- **Segments:** L1 Zone (green) · L2 Audit Head (amber) · L3 CEO (orange) · L3+ Chairman (red)
- **Centre text:** Total active escalations
- **API:** `GET /api/v1/group/{id}/audit/escalations/charts/level-distribution/`

### Chart 3 — Effectiveness Rate Trend (line)
- **Type:** Line (Chart.js 4.x)
- **X-axis:** Months
- **Y-axis:** Effectiveness rate (%)
- **Target:** Dashed line at 80%
- **Colour:** Green when ≥ 80%, amber 60–79%, red < 60%
- **API:** `GET /api/v1/group/{id}/audit/escalations/charts/effectiveness/`

### Chart 4 — Branch Escalation Heatmap (matrix)
- **Type:** Matrix heatmap (chartjs-chart-matrix plugin)
- **X-axis:** Months
- **Y-axis:** Branches
- **Cell colour:** White (0) → Light orange (1–2) → Red (3+) escalations
- **API:** `GET /api/v1/group/{id}/audit/escalations/charts/branch-heatmap/`

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Escalation sent (auto) | "ESC-2026-00089 auto-escalated to Zone Director — CAPA-2026-00289 overdue 7 days" | Warning (amber) |
| Escalation sent (manual) | "Manual escalation sent to CEO — CAPA-2026-00289" | Info (blue) |
| Response recorded | "Response recorded — P. Ramaiah committed to resolve by 25-Mar-2026" | Success (green) |
| Re-escalated | "ESC-2026-00089 re-escalated to Chairman — no CEO response in 48 hours" | Warning (amber) |
| Escalation resolved | "ESC-2026-00089 resolved — CAPA-2026-00289 closed · Sunrise Miyapur" | Success (green) |
| No acknowledgement alert | "⚠️ ESC-2026-00089 — no acknowledgement from CEO in 48 hours — re-escalation triggered" | Error (red) |
| Rule enabled | "Escalation rule 'Critical Overdue — Day 1' enabled" | Success (green) |
| Rule updated | "Escalation rule updated — Major Overdue threshold changed to 5 days" | Info (blue) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No active escalations | Shield with green tick | "No active escalations — all compliance issues are being resolved within timelines." | — (positive state) |
| No history | Timeline icon | "No escalation history yet. Escalations are triggered when CAPA findings are not resolved on time." | — |
| No rules configured | Gear icon | "No escalation rules configured. Without rules, non-compliance will not auto-escalate." | `[+ Add Rule]` |
| Filter returns zero | Magnifying glass | "No escalations match your filters." | `[Reset Filters]` |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Page initial load | Skeleton: KPI bar + table | < 1s |
| KPI bar | 7 grey pulse cards → populated | < 500ms |
| Active escalations table | 10 skeleton rows → data | < 1s |
| Rules engine table | Skeleton rows → data | < 1s |
| Analytics charts | Grey chart placeholders → Chart.js | < 1s |
| Escalation detail drawer | Drawer skeleton → populated | < 500ms |
| Manual escalation send | Spinner on button + "Sending…" | < 2s |
| Re-escalation send | Spinner on button | < 1s |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/escalations/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | List escalations (paginated, filterable) | G1+ |
| 2 | GET | `/{esc_id}/` | Escalation detail with full chain history | G1+ |
| 3 | POST | `/` | Trigger manual escalation | 128, 121, G4+ |
| 4 | POST | `/{esc_id}/response/` | Record recipient response | 128, G4+ |
| 5 | POST | `/{esc_id}/re-escalate/` | Escalate to next level | 128, G4+ |
| 6 | POST | `/{esc_id}/resolve/` | Mark escalation resolved | 128, G4+ |
| 7 | GET | `/active/` | Active escalations only | G1+ |
| 8 | GET | `/awaiting-response/` | Escalations past 48hr with no ack | G1+ |
| 9 | GET | `/rules/` | List escalation rules | G1+ |
| 10 | POST | `/rules/` | Create escalation rule | G4+ |
| 11 | PATCH | `/rules/{rule_id}/` | Update escalation rule | G4+ |
| 12 | PATCH | `/rules/{rule_id}/toggle/` | Enable/disable rule | G4+ |
| 13 | GET | `/kpis/` | KPI bar aggregates | G1+ |
| 14 | GET | `/charts/monthly/` | Chart 1 data | G1+ |
| 15 | GET | `/charts/level-distribution/` | Chart 2 data | G1+ |
| 16 | GET | `/charts/effectiveness/` | Chart 3 data | G1+ |
| 17 | GET | `/charts/branch-heatmap/` | Chart 4 data | G1+ |
| 18 | GET | `/export/` | Export escalation log as Excel | G1+ |
| 19 | POST | `/rules/test/` | Dry-run test a rule against current data | G4+ |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../escalations/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#esc-content` | `innerHTML` | `hx-trigger="click"` |
| Active table | Tab 1 load | `hx-get=".../escalations/?status=active"` | `#esc-table-body` | `innerHTML` | Paginated |
| Filter change | Select change | `hx-get` with filters | `#esc-table-body` | `innerHTML` | Debounced |
| Escalation detail drawer | Row click | `hx-get=".../escalations/{id}/"` | `#right-drawer` | `innerHTML` | 780px |
| Rules table | Tab 3 load | `hx-get=".../escalations/rules/"` | `#rules-content` | `innerHTML` | — |
| Rule toggle | Toggle switch | `hx-patch=".../escalations/rules/{id}/toggle/"` | `#rule-{id}-status` | `innerHTML` | Inline badge |
| Analytics | Tab 4 load | `hx-get=".../escalations/analytics/"` | `#analytics-content` | `innerHTML` | Chart.js init |
| Manual escalation form | Button click | — | `#modal-content` | `innerHTML` | Modal |
| Submit escalation | Form submit | `hx-post=".../escalations/"` | `#esc-result` | `innerHTML` | Toast + table refresh |
| Record response | Form submit | `hx-post=".../escalations/{id}/response/"` | `#esc-{id}-status` | `innerHTML` | Toast + inline update |
| Re-escalate | Form submit | `hx-post=".../escalations/{id}/re-escalate/"` | `#esc-{id}-row` | `innerHTML` | Toast + row update |
| Chart load | Section shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
