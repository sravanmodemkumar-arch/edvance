# P-06 — Audit Finding Tracker

> **URL:** `/group/audit/findings/`
> **File:** `p-06-audit-finding-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Internal Audit Head (Role 121, G1) — primary viewer

---

## 1. Purpose

The Audit Finding Tracker is the central register of ALL findings from ALL audit types — financial, academic, operational, safety — across ALL branches. This is the page the Audit Head opens when the CEO asks: "How many unresolved issues do we have?" or when the Board wants a summary of audit observations for the quarterly governance meeting. In Indian education groups, audit findings are the leading indicator of institutional risk — a pattern of unresolved safety findings predicts accidents, a pattern of financial findings predicts fraud, and a pattern of academic findings predicts poor board results.

The problems this page solves:

1. **Finding fragmentation:** Without centralisation, financial findings live in P-03, academic findings in P-04, safety findings in P-05. The Audit Head needs a single view across all types to identify patterns — e.g., a branch with 15 findings across three audit types is a systemic problem, not three isolated issues.

2. **Ageing and escalation blindness:** A finding that's 90 days old and unresolved is a governance failure. The tracker prominently displays finding age, overdue status, and escalation level. Auto-escalation rules ensure: 7 days overdue → reminder to assigned person; 14 days → escalation to Branch Principal; 30 days → escalation to Zone Director; 60 days → escalation to CEO. Critical (S1) findings escalate faster: immediate CEO notification.

3. **Repeat finding detection:** The same issue found at the same branch in consecutive audits is a repeat finding — it means the corrective action failed or was never implemented. The tracker flags repeat findings and links them to previous occurrences, making recurrence impossible to hide.

4. **CAPA linkage:** Every finding that requires corrective action (S1, S2, and some S3) links to the CAPA register (P-15). The tracker shows CAPA status inline — open, in progress, verification pending, closed — so the Audit Head can see at a glance which findings are being actively addressed.

5. **Board reporting:** The tracker generates summaries in the format Indian Trust boards expect: findings by severity, by type, by branch, with ageing analysis and closure rates — ready for the quarterly Board of Trustees meeting.

**Scale:** 500–2,000 findings/year · 50–200 open at any time · 4 severity levels · 5 audit types · 5–50 branches

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Internal Audit Head | 121 | G1 | Full read + manage escalations + sign-off closures | Primary finding manager |
| Group Academic Quality Officer | 122 | G1 | Read + edit academic findings | Own-type findings |
| Group Inspection Officer | 123 | G3 | Read + create findings + update status | Field reporter |
| Group Compliance Data Analyst | 127 | G1 | Read — analytics and trend reporting | MIS |
| Group Process Improvement Coordinator | 128 | G3 | Read + CAPA linkage — manage corrective actions | Links to P-15 |
| Group Affiliation Compliance Officer | 125 | G1 | Read — affiliation-related findings | Filtered view |
| Group Grievance Audit Officer | 126 | G1 | Read — grievance-linked findings | Filtered view |
| Group CEO / Chairman | — | G4/G5 | Read — escalated findings, summary view | Governance oversight |
| Branch Principal | — | G3 | Read (own branch) — see findings assigned to their branch | Action required |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Branch Principals see only their branch's findings via branch-scoped API filter.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Audit Finding Tracker
```

### 3.2 Page Header
```
Audit Finding Tracker                                    [+ Log Finding]  [Bulk Update]  [Export]
Audit Head — K. Ramachandra Rao
Sunrise Education Group · FY 2025-26 · 142 open findings · 23 overdue · 8 critical (S1)
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Open | Integer | COUNT(findings) WHERE status != 'closed' | Red > 100, Amber 50–100, Green < 50 | `#kpi-open` |
| 2 | Critical (S1) | Integer | COUNT WHERE severity = 'S1' AND status != 'closed' | Red > 0, Green = 0 | `#kpi-critical` |
| 3 | Overdue | Integer | COUNT WHERE capa_due_date < today AND status NOT IN ('closed', 'verified') | Red > 10, Amber 1–10, Green = 0 | `#kpi-overdue` |
| 4 | Avg Age (Open) | Days | AVG(today − found_date) for open findings | Red > 45d, Amber 21–45d, Green < 21d | `#kpi-age` |
| 5 | Closure Rate (FY) | Percentage | Closed findings / (closed + open) × 100 for this FY | Green ≥ 80%, Amber 60–79%, Red < 60% | `#kpi-closure` |
| 6 | Repeat Findings | Integer | COUNT WHERE is_repeat = true AND status != 'closed' | Red > 5, Amber 1–5, Green = 0 | `#kpi-repeat` |

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **All Findings** — Master list with filters
2. **By Branch** — Branch-wise grouping with totals
3. **Ageing Analysis** — Age distribution and escalation status
4. **Trends & Patterns** — Finding trends over time, repeat detection

### 5.2 Tab 1: All Findings

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Finding ID | Text (link) | Yes | Auto: FIN-2026-001, ACA-2026-001, OSA-2026-001 |
| Title | Text (truncated) | No | First 80 chars of description |
| Audit Type | Badge | Yes | Financial / Academic / Operational / Safety / Affiliation |
| Branch | Text | Yes | — |
| Severity | Badge | Yes | S1 (Critical) / S2 (Major) / S3 (Minor) / S4 (Observation) |
| Found Date | Date | Yes | — |
| Age (days) | Integer | Yes | Auto-calculated |
| CAPA Status | Badge | Yes | Open / Assigned / In Progress / Verification / Closed / N/A |
| Assigned To | Text | Yes | Person responsible for correction |
| Due Date | Date | Yes | CAPA deadline |
| Overdue? | Badge | Yes | Yes (days) / No / N/A |
| Escalation Level | Badge | Yes | None / L1 (Reminder) / L2 (Principal) / L3 (Zone) / L4 (CEO) |
| Repeat? | Badge | Yes | 🔁 Yes (Nth occurrence) / — |
| Monetary Impact (₹) | Amount | Yes | If financial finding |
| Actions | Buttons | No | [View] [Update] [Escalate] [Close] |

**Filters:** Audit type · Branch · Severity · Status · Assigned to · Age range · Overdue only · Repeat only · Escalation level

**Bulk actions (checkbox select):** Bulk assign · Bulk escalate · Bulk update status · Export selected

### 5.3 Tab 2: By Branch

**Grouped view:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Total Open | Integer | Yes | All open findings |
| S1 (Critical) | Integer | Yes | — |
| S2 (Major) | Integer | Yes | — |
| S3 (Minor) | Integer | Yes | — |
| S4 (Observation) | Integer | Yes | — |
| Overdue | Integer | Yes | — |
| Avg Age | Days | Yes | Average age of open findings |
| Closure Rate | Percentage | Yes | Closed / (closed + open) for this branch |
| Repeat Count | Integer | Yes | Repeat findings at this branch |
| Worst Category | Badge | No | Audit type with most findings |
| Risk Level | Badge | Yes | High (> 15 open) / Medium (5–15) / Low (< 5) |

**Expandable rows:** Click branch → inline expand showing individual findings

### 5.4 Tab 3: Ageing Analysis

**Age distribution buckets:**

```
┌────────────────────────────────────────────────────┐
│  Finding Age Distribution (Open Items)             │
│                                                    │
│  0–7 days:   ██████████████████████  38 (27%)     │
│  8–14 days:  ████████████████       28 (20%)      │
│  15–30 days: ██████████████         24 (17%)      │
│  31–60 days: ███████████            19 (13%)      │
│  61–90 days: ████████               14 (10%)      │
│  90+ days:   ██████████████████     19 (13%) ⚠️   │
└────────────────────────────────────────────────────┘
```

**Escalation status table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Finding ID | Text (link) | Yes | — |
| Branch | Text | Yes | — |
| Severity | Badge | Yes | — |
| Age (days) | Integer | Yes | — |
| Escalation Level | Badge | Yes | Current escalation |
| Escalated To | Text | Yes | Person at current level |
| Escalation Date | Date | Yes | When escalated |
| Response? | Badge | Yes | ✅ Responded / 🔴 No response / ⚠️ Pending |
| Next Escalation | Date | Yes | When next auto-escalation triggers |

### 5.5 Tab 4: Trends & Patterns

**Repeat finding tracker:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Finding Pattern | Text | Yes | Category + description pattern |
| Branch | Text | Yes | — |
| Occurrences | Integer | Yes | Times this finding appeared |
| First Found | Date | Yes | — |
| Latest Found | Date | Yes | — |
| Status | Badge | Yes | Persistent / Intermittent / Resolved |
| Root Cause Identified? | Badge | Yes | ✅ Yes / 🔴 No |
| Systemic? | Badge | Yes | ✅ Multi-branch / Single branch |

---

## 6. Drawers & Modals

### 6.1 Drawer: `finding-detail` (720px, right-slide)

- **Title:** "Finding — [ID] · [Severity Badge]"
- **Tabs:** Details · Evidence · CAPA · Escalation · History · Related
- **Details tab:**
  - Full description, audit context (which audit generated this), branch, date found
  - Category: Financial discrepancy / Academic non-compliance / Safety hazard / etc.
  - Severity with justification
  - Monetary impact (if applicable)
  - Root cause (from CAPA if linked)
  - Responsible person
- **Evidence tab:** Photos, documents, screenshots attached as evidence
- **CAPA tab:** Linked CAPA item — corrective action, preventive action, status, timeline
- **Escalation tab:** Escalation history — each level, date, person, response
- **History tab:** Finding lifecycle: found → CAPA created → assigned → in progress → verification → closed
- **Related tab:** Previous occurrences (if repeat), related findings at same branch or same type across branches
- **Footer:** [Update Status] [Escalate] [Link CAPA] [Mark Verified] [Close Finding] [Export]
- **Access:** G1+ (Division P roles)

### 6.2 Modal: `log-finding` (560px)

- **Title:** "Log New Finding"
- **Fields:**
  - Audit type (dropdown): Financial / Academic / Operational / Safety / Affiliation / Other
  - Linked audit (optional — dropdown of recent audits)
  - Branch (dropdown, required)
  - Severity (radio): S1 / S2 / S3 / S4 with descriptions
  - Category (dropdown — varies by audit type):
    - Financial: Fee Discrepancy / Vendor Irregularity / Petty Cash / Unauthorized Concession / Budget Overrun / Missing Docs
    - Academic: Lesson Plan Gap / Exam Quality / Teaching Hours / Lab Non-compliance / Result Issue
    - Safety: Fire Safety / Electrical / Building / CCTV / Transport / Hygiene
    - Affiliation: Document Missing / Norm Breach / Infrastructure Gap
  - Title (text, required — concise summary)
  - Description (textarea, required — detailed observation)
  - Monetary impact (₹, optional)
  - Evidence (file upload — multiple)
  - CAPA required? (auto-toggle for S1/S2; manual for S3)
  - Assigned to (dropdown — branch principal or specific person)
  - CAPA due date (auto: S1=7d, S2=14d, S3=30d; manual override allowed)
  - Repeat of previous finding? (toggle + previous finding ID)
- **Buttons:** Cancel · Save Finding
- **Access:** Role 121, 122, 123, 125

### 6.3 Modal: `escalate-finding` (480px)

- **Title:** "Escalate Finding — [ID]"
- **Content:** Finding summary, current assignee, age, current escalation level
- **Fields:**
  - Escalate to (auto-suggested based on escalation matrix):
    - L1: Assigned person (reminder)
    - L2: Branch Principal
    - L3: Zone Director
    - L4: CEO
  - Escalation reason (textarea, required)
  - Deadline for response (date — default: 3 business days)
  - Notify via (checkboxes): Platform notification / Email / WhatsApp
- **Buttons:** Cancel · Escalate
- **Access:** Role 121, 128, G4+

### 6.4 Modal: `close-finding` (480px)

- **Title:** "Close Finding — [ID]"
- **Fields:**
  - Closure type (radio): Resolved / Accepted Risk / Not Applicable / Duplicate
  - If Resolved:
    - Verification evidence (file upload — before/after photos, corrected documents)
    - Verified by (auto-filled or dropdown)
    - Verification date
    - Closure notes (textarea)
  - If Accepted Risk:
    - Risk acceptance justification (textarea, required)
    - Accepted by (must be G4/G5 for S1/S2)
    - Review date (when to re-evaluate — mandatory)
  - Preventive action implemented? (toggle + description)
- **Buttons:** Cancel · Close Finding
- **Validation:** S1/S2 findings require G4+ approval for closure
- **Access:** Role 121 (all findings), 128 (own CAPAs), G4+ (S1/S2 closure)

### 6.5 Modal: `bulk-update` (560px)

- **Title:** "Bulk Update — [N] Findings Selected"
- **Fields:**
  - Action (dropdown): Reassign / Change due date / Update status / Escalate / Add tag
  - If Reassign: New assignee (dropdown)
  - If Change due date: New date (date picker)
  - If Update status: New status (dropdown)
  - If Escalate: Escalation level and reason
  - If Add tag: Tag (text)
  - Reason for bulk update (textarea, required)
- **Buttons:** Cancel · Apply to All
- **Access:** Role 121, G4+

---

## 7. Charts

### 7.1 Finding Severity Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Open Findings by Severity" |
| Data | COUNT per severity: S1, S2, S3, S4 |
| Colours | S1: #EF4444, S2: #F97316, S3: #FBBF24, S4: #94A3B8 |
| Centre text | Total: N open |
| API | `GET /api/v1/group/{id}/audit/findings/analytics/severity-distribution/` |

### 7.2 Finding Age Distribution (Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar |
| Title | "Finding Age Distribution — Open Items" |
| Data | COUNT per age bucket (0–7d, 8–14d, 15–30d, 31–60d, 61–90d, 90d+) grouped by severity |
| API | `GET /api/v1/group/{id}/audit/findings/analytics/age-distribution/` |

### 7.3 Monthly Finding Trend (Stacked Area)

| Property | Value |
|---|---|
| Chart type | Stacked area |
| Title | "Findings — Monthly Trend (Found vs Closed)" |
| Data | Per month: new findings (area 1) vs closed findings (area 2) |
| Net indicator | Line showing net open change |
| API | `GET /api/v1/group/{id}/audit/findings/analytics/monthly-trend/` |

### 7.4 Branch Finding Load (Treemap)

| Property | Value |
|---|---|
| Chart type | Treemap (Chart.js treemap plugin) |
| Title | "Open Findings by Branch" |
| Data | COUNT per branch — rectangle size proportional to finding count |
| Colour | Red for most findings, green for least |
| API | `GET /api/v1/group/{id}/audit/findings/analytics/branch-load/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Finding logged | "Finding [ID] logged — severity: [S1–S4]" | Success | 3s |
| Finding updated | "Finding [ID] updated" | Info | 3s |
| Finding escalated | "Finding [ID] escalated to [Role/Person]" | Warning | 4s |
| Finding closed | "Finding [ID] closed — [Resolution type]" | Success | 3s |
| Bulk update complete | "[N] findings updated" | Success | 3s |
| Critical auto-escalation | "🔴 Critical finding [ID] auto-escalated to CEO" | Error | 6s |
| Overdue alert | "⚠️ [N] findings overdue — oldest: [Age] days" | Warning | 5s |
| Repeat detected | "🔁 Repeat finding detected at [Branch] — [N]th occurrence" | Warning | 5s |
| CAPA created | "CAPA [ID] auto-created for finding [Finding ID]" | Info | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No findings | ✅ | "No Audit Findings" | "All audit observations have been resolved. Excellent compliance!" | — |
| No open findings | ✅ | "All Findings Resolved" | "All [N] findings from this fiscal year have been closed." | — |
| No escalated findings | 📋 | "No Escalations" | "All findings are being addressed within timelines." | — |
| No audits conducted | 🔍 | "No Audits Completed" | "Findings will appear after the first audit is completed." | Go to Audit Calendar |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + table skeleton |
| Tab switch | Tab content skeleton |
| Finding detail drawer | 720px skeleton: 6 tabs |
| Charts | Grey canvas placeholder per chart |
| Branch grouping expand | Inline table skeleton (5 rows) |
| Bulk update | Progress bar with count |
| Export | "Generating report…" spinner |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/findings/` | G1+ | List all findings with filters |
| GET | `/api/v1/group/{id}/audit/findings/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/audit/findings/{finding_id}/` | G1+ | Finding detail |
| POST | `/api/v1/group/{id}/audit/findings/` | 121, 122, 123, 125 | Log new finding |
| PUT | `/api/v1/group/{id}/audit/findings/{finding_id}/` | 121, 122, 123 | Update finding |
| PATCH | `/api/v1/group/{id}/audit/findings/{finding_id}/escalate/` | 121, 128, G4+ | Escalate finding |
| PATCH | `/api/v1/group/{id}/audit/findings/{finding_id}/close/` | 121, 128, G4+ | Close finding |
| POST | `/api/v1/group/{id}/audit/findings/bulk-update/` | 121, G4+ | Bulk update |
| GET | `/api/v1/group/{id}/audit/findings/by-branch/` | G1+ | Branch-grouped view |
| GET | `/api/v1/group/{id}/audit/findings/ageing/` | G1+ | Ageing analysis |
| GET | `/api/v1/group/{id}/audit/findings/repeats/` | G1+ | Repeat finding patterns |
| GET | `/api/v1/group/{id}/audit/findings/escalations/` | G1+ | Active escalations |
| GET | `/api/v1/group/{id}/audit/findings/analytics/severity-distribution/` | G1+ | Severity donut |
| GET | `/api/v1/group/{id}/audit/findings/analytics/age-distribution/` | G1+ | Age bar chart |
| GET | `/api/v1/group/{id}/audit/findings/analytics/monthly-trend/` | G1+ | Monthly trend area |
| GET | `/api/v1/group/{id}/audit/findings/analytics/branch-load/` | G1+ | Branch treemap |
| GET | `/api/v1/group/{id}/audit/findings/export/` | G1+ | Export findings |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../findings/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#findings-content` | `innerHTML` | `hx-trigger="click"` |
| Finding detail drawer | Row click | `hx-get=".../findings/{id}/"` | `#right-drawer` | `innerHTML` | 720px drawer |
| Log finding | Form submit | `hx-post=".../findings/"` | `#log-result` | `innerHTML` | Toast + table refresh |
| Escalate | Form submit | `hx-patch=".../findings/{id}/escalate/"` | `#escalation-result` | `innerHTML` | Toast |
| Close finding | Form submit | `hx-patch=".../findings/{id}/close/"` | `#close-result` | `innerHTML` | Toast + row update |
| Bulk update | Form submit | `hx-post=".../findings/bulk-update/"` | `#bulk-result` | `innerHTML` | Progress + toast |
| Filter | Filter change | `hx-get` with filter params | `#findings-table` | `innerHTML` | `hx-trigger="change"` |
| Branch expand | Row click (Tab 2) | `hx-get=".../findings/?branch={id}"` | `#branch-{id}-detail` | `innerHTML` | Inline expand |
| Sort | Header click | `hx-get` with sort param | `#findings-table` | `innerHTML` | `hx-trigger="click"` |
| Chart load | Tab shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |
| Auto-refresh KPIs | Every 5 min | `hx-get=".../findings/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="every 300s"` |
| Pagination | Page click | `hx-get` with page param | `#table-body` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
