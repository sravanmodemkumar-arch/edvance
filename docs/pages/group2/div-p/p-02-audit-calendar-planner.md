# P-02 — Audit Calendar & Planner

> **URL:** `/group/audit/calendar/`
> **File:** `p-02-audit-calendar-planner.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Internal Audit Head (Role 121, G1) — primary operator

---

## 1. Purpose

The Audit Calendar & Planner is the annual planning tool that schedules every audit — financial, academic, operational, safety, comprehensive — across every branch in the group. In Indian education, an unplanned audit programme means some branches get audited three times while others go untouched for two years. The Audit Head creates the Annual Audit Plan (AAP) at the start of each financial year (April), gets it approved by the CEO/Chairman, and uses this page to track execution throughout the year.

The problems this page solves:

1. **No structured audit plan:** Most Indian education groups conduct audits reactively — after a complaint, after a fee dispute, after a newspaper exposé. Proactive, risk-based audit planning is rare. This page enforces a structured approach: the AAP specifies which branches get which audits in which month, based on risk assessment (branch size, previous findings, affiliation renewal timing, complaint history).

2. **Auditor workload imbalance:** In a 30-branch group with 3–5 inspectors, workload must be distributed evenly. Without planning, the senior inspector does all metro branches while the junior one gets only rural branches. The calendar visualizes auditor assignments and flags workload imbalances.

3. **Surprise vs scheduled audit mix:** Indian regulatory norms (RTE Act, CBSE Manual) recommend a mix of surprise and scheduled audits. The platform tracks this ratio — recommended: 40% surprise, 60% scheduled — and alerts if the mix is skewed.

4. **Season-awareness:** Certain audits make sense only at certain times — financial audits after fee collection (Aug–Sep, Jan–Feb), academic audits mid-term (Oct, Feb), safety audits before monsoon (May–Jun), affiliation audits before renewal window (Oct–Dec). The calendar enforces season-appropriate scheduling.

5. **CEO/Board visibility:** The approved AAP becomes a governance document. The CEO can see at any point: "Are we on track with the audit plan?" The Board can verify: "Were all planned audits conducted?" This is critical for Trust Act compliance and CAG audits (for government-aided institutions).

**Scale:** 5–50 branches · 150–400 planned audits/year · 3–10 auditors · 12-month rolling plan · quarterly review cycles

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Internal Audit Head | 121 | G1 | Full — create AAP, schedule audits, assign auditors, modify plan | Primary planner |
| Group Academic Quality Officer | 122 | G1 | Read + create academic audits only | Academic audit scheduling |
| Group Inspection Officer | 123 | G3 | Read — view own assignments, mark availability | Field execution |
| Group ISO / NAAC Coordinator | 124 | G1 | Read — view certification-related audits | Certification audit timing |
| Group Affiliation Compliance Officer | 125 | G1 | Read + create affiliation audits | Affiliation inspection scheduling |
| Group Compliance Data Analyst | 127 | G1 | Read — audit plan data for MIS | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read — upcoming audits for CAPA follow-up | Plans verification visits |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve AAP | Annual plan approval authority |
| Group COO | 59 | G4 | Read — operational audit schedule | Operational coordination |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. AAP creation: 121 or G4+. AAP approval: G4/G5 only. Audit scheduling: 121, 122, 125.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Audit Calendar & Planner
```

### 3.2 Page Header
```
Audit Calendar & Planner                          [+ Create Audit Plan]  [+ Schedule Audit]  [Export Plan]
Audit Head — K. Ramachandra Rao
Sunrise Education Group · FY 2025-26 · AAP Status: ✅ Approved · 342 audits planned · 218 completed (64%)
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Audits Planned (FY) | Integer | COUNT(audits) WHERE fy = current AND plan_status = 'approved' | Static blue | `#kpi-planned` |
| 2 | Audits Completed | Integer | COUNT(audits) WHERE status = 'completed' AND fy = current | Green if on track (≥ expected by month), Amber within 10%, Red below | `#kpi-completed` |
| 3 | Completion Rate | Percentage | Completed / planned for months elapsed × 100 | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-rate` |
| 4 | This Month | Integer / Integer | Completed / planned for current month | Green if 100%, Amber ≥ 50%, Red < 50% | `#kpi-month` |
| 5 | Surprise Audit Ratio | Percentage | Surprise audits / total audits × 100 | Green 30–50%, Amber outside, Red < 20% or > 60% | `#kpi-surprise` |
| 6 | Unscheduled Branches | Integer | Branches with no audit scheduled in next 90 days | Red > 5, Amber 1–5, Green = 0 | `#kpi-unscheduled` |

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Calendar View** — Visual month/week calendar with audit events
2. **Annual Audit Plan** — Full AAP table with approval status
3. **Auditor Workload** — Per-auditor assignment and capacity
4. **Risk Matrix** — Branch risk assessment driving audit frequency

### 5.2 Tab 1: Calendar View

**FullCalendar.js integration (month/week/day views):**

- Each audit = coloured event block
  - Financial: Blue
  - Academic: Green
  - Operational: Orange
  - Safety: Red
  - Comprehensive: Purple
- Surprise audits: Dashed border (branch name hidden until 24 hours before)
- Click event → opens audit detail drawer
- Drag-and-drop to reschedule (Role 121 only)
- Filter by: Audit type · Branch · Auditor · Status (Scheduled/Completed/Cancelled)

**Legend bar above calendar:**
```
🔵 Financial  🟢 Academic  🟠 Operational  🔴 Safety  🟣 Comprehensive  ⬜ Cancelled  ┊┊ Surprise
```

### 5.3 Tab 2: Annual Audit Plan (AAP)

**AAP Summary:**
```
Annual Audit Plan — FY 2025-26
Status: ✅ Approved by CEO on 15 Apr 2025
Total Planned: 342 audits across 28 branches
Quarterly Split: Q1: 82 · Q2: 94 · Q3: 88 · Q4: 78
```

**AAP Table — Branch × Audit Type Matrix:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | Row per branch |
| Financial Audits | Integer + schedule | Yes | Planned count + months (e.g., "3 — Aug, Dec, Mar") |
| Academic Audits | Integer + schedule | Yes | Planned count + months |
| Operational Audits | Integer + schedule | Yes | Planned count + months |
| Safety Audits | Integer + schedule | Yes | Planned count + months |
| Comprehensive | Integer + schedule | Yes | Planned count + months (usually 1/year) |
| Total Audits | Integer | Yes | Sum for this branch |
| Risk Level | Badge | Yes | High / Medium / Low (drives frequency) |
| Completion | Percentage | Yes | Completed / planned |
| Status | Badge | Yes | On Track / Behind / At Risk |

**Plan approval workflow:** Draft → Submitted for Approval → Approved / Revision Requested → Approved

### 5.4 Tab 3: Auditor Workload

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Auditor Name | Text | Yes | — |
| Role | Badge | Yes | Inspection Officer / Academic QO / etc. |
| Assigned This Month | Integer | Yes | Audits assigned |
| Completed This Month | Integer | Yes | Audits completed |
| Assigned This FY | Integer | Yes | Total FY |
| Completed This FY | Integer | Yes | Total FY completed |
| Upcoming (Next 30d) | Integer | Yes | Scheduled |
| Availability | Badge | Yes | Available / On Leave / Busy |
| Workload Score | Badge | Yes | Light / Balanced / Heavy / Overloaded |

**Workload balance indicator:**
```
Ideal: ~8–10 audits/auditor/month
Light: < 5 · Balanced: 5–10 · Heavy: 11–15 · Overloaded: > 15
```

### 5.5 Tab 4: Risk Matrix

**Branch Risk Assessment Table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Student Count | Integer | Yes | Scale indicator |
| Previous Findings | Integer | Yes | Open + closed findings last FY |
| Critical Findings (open) | Integer | Yes | S1 findings still open |
| Compliance Score | Percentage | Yes | Current branch score from P-10 |
| Affiliation Due | Date | Yes | Nearest affiliation renewal |
| Complaint Volume | Integer | Yes | Grievances in last 12 months |
| Financial Risk | Badge | Yes | High / Medium / Low |
| Academic Risk | Badge | Yes | High / Medium / Low |
| Safety Risk | Badge | Yes | High / Medium / Low |
| Overall Risk | Badge | Yes | Composite: High / Medium / Low |
| Recommended Frequency | Text | No | e.g., "Monthly" / "Quarterly" / "Semi-annual" |
| Planned Frequency | Text | No | From AAP |
| Gap | Badge | No | ✅ Adequate / ⚠️ Under-audited / 🔴 Missing |

**Risk scoring logic:**
```
Financial Risk = f(fee collection irregularities, vendor payment delays, scholarship misuse history)
Academic Risk = f(result quality, lesson plan compliance, exam paper leaks, teacher turnover)
Safety Risk = f(fire NOC status, CCTV coverage, POCSO incidents, infrastructure age)
Overall Risk = MAX(Financial, Academic, Safety) — worst dimension determines audit frequency
```

---

## 6. Drawers & Modals

### 6.1 Modal: `create-annual-plan` (720px)

- **Title:** "Create Annual Audit Plan — FY [Year]"
- **Fields:**
  - Financial year (auto-filled: next FY if creating in Q4, current FY if creating in Q1)
  - Plan name (text, auto-generated: "AAP-2026-27")
  - Branch selection (multi-select: All / Specific branches)
  - Audit types to include (checkboxes: Financial, Academic, Operational, Safety, Comprehensive)
  - Auto-generate plan? (toggle — uses risk matrix to auto-distribute audits)
  - If auto-generate:
    - High-risk branches: Monthly financial + quarterly academic + quarterly safety
    - Medium-risk: Quarterly financial + semi-annual academic + semi-annual safety
    - Low-risk: Semi-annual financial + annual academic + annual safety
    - All branches: Annual comprehensive
  - Manual override table (branch × month × audit type — checkboxes)
  - Notes for CEO (textarea)
- **Buttons:** Cancel · Save as Draft · Submit for Approval
- **Access:** Role 121, G4+

### 6.2 Modal: `schedule-audit` (560px)

- **Title:** "Schedule Audit"
- **Fields:**
  - Audit type (dropdown): Financial / Academic / Operational / Safety / Comprehensive / Special
  - Branch (dropdown, required)
  - Scheduled date(s) (date picker — single day or date range for multi-day)
  - Time (optional — default: full day)
  - Surprise visit? (toggle)
    - If surprise: Branch notification suppressed; only auditor and Audit Head know
    - Scheduled: Branch receives notification 7 days prior
  - Auditor(s) (multi-select, required)
  - Scope / focus areas (checkboxes):
    - Financial: Fee reconciliation / Vendor payments / Petty cash / Scholarship / Budget
    - Academic: Lesson plans / Exam papers / Syllabus coverage / Results / Teaching hours
    - Operational: Infrastructure / Staffing / Attendance accuracy / Lab equipment / Library
    - Safety: Fire safety / CCTV / First aid / Building stability / Electrical
  - Linked to: Previous finding (optional — for follow-up audits)
  - Priority (radio): Routine / High / Critical
  - Special instructions (textarea)
- **Buttons:** Cancel · Schedule
- **Validation:**
  - Auditor must be available on selected date (no conflicting assignments)
  - Cannot schedule same-type audit at same branch within 7 days
  - Comprehensive audit requires at least 2 auditors
- **Access:** Role 121, 122 (academic only), 125 (affiliation only), G4+

### 6.3 Drawer: `audit-detail` (720px, right-slide)

- **Title:** "Audit — [Type] · [Branch] · [Date]"
- **Tabs:** Overview · Scope · Team · Findings · Report · History
- **Overview tab:** Type, branch, date(s), status, surprise?, linked finding, priority
- **Scope tab:** Focus areas checklist, special instructions, documents to review
- **Team tab:** Assigned auditors with roles, availability confirmation
- **Findings tab:** Findings from this audit (if completed) — links to P-06
- **Report tab:** Audit report (if completed) — score, summary, recommendations
- **History tab:** Audit lifecycle: scheduled → notified → in-progress → report submitted → reviewed → closed
- **Footer:** [Edit] [Reschedule] [Cancel] [Mark In-Progress] [Submit Report]
- **Access:** G1+ (Division P roles)

### 6.4 Modal: `approve-annual-plan` (640px, G4/G5)

- **Title:** "Approve Annual Audit Plan — [FY]"
- **Content:** AAP summary — total audits, branch × type matrix, risk-based rationale, resource requirements
- **Comparison:** If previous FY plan exists, show year-over-year comparison
- **Actions:** Approve / Approve with Modifications / Request Revision (with notes)
- **Access:** G4/G5 only

### 6.5 Modal: `auditor-availability` (480px)

- **Title:** "Mark Availability — [Auditor Name]"
- **Fields:**
  - Date range (start–end)
  - Status: Available / On Leave / Training / Other Assignment
  - Notes (optional)
- **Buttons:** Cancel · Save
- **Access:** Role 123 (own availability), 121 (any auditor)

---

## 7. Charts

### 7.1 Audit Plan Progress (Gauge)

| Property | Value |
|---|---|
| Chart type | Gauge / Doughnut (Chart.js 4.x) |
| Title | "Annual Plan Progress — FY 2025-26" |
| Data | Completed / Total planned |
| Colours | Green segment (completed), Grey (remaining), Red needle if behind |
| Centre text | "64% Complete" |
| API | `GET /api/v1/group/{id}/audit/calendar/plan-progress/` |

### 7.2 Monthly Audit Distribution (Stacked Bar)

| Property | Value |
|---|---|
| Chart type | Stacked bar |
| Title | "Monthly Audit Schedule" |
| Data | Per month: COUNT per audit type (Financial, Academic, Operational, Safety, Comprehensive) |
| Overlay | Line showing completed vs planned |
| API | `GET /api/v1/group/{id}/audit/calendar/monthly-distribution/` |

### 7.3 Auditor Workload (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Auditor Workload — Current Month" |
| Data | Per auditor: assigned (bar) vs completed (overlay) |
| Colour | Green ≤ 10, Amber 11–15, Red > 15 |
| API | `GET /api/v1/group/{id}/audit/calendar/auditor-workload/` |

### 7.4 Branch Risk Heatmap (Matrix)

| Property | Value |
|---|---|
| Chart type | Heatmap matrix (custom Canvas) |
| Title | "Branch Risk Matrix" |
| X-axis | Risk dimensions (Financial, Academic, Safety) |
| Y-axis | Branches |
| Cell colour | Green (Low), Amber (Medium), Red (High) |
| API | `GET /api/v1/group/{id}/audit/calendar/risk-matrix/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| AAP created | "Annual Audit Plan [FY] created — pending approval" | Success | 3s |
| AAP approved | "Annual Audit Plan [FY] approved by [CEO Name]" | Success | 4s |
| AAP revision requested | "Annual Audit Plan [FY] — revision requested: [Reason]" | Warning | 5s |
| Audit scheduled | "Audit scheduled — [Type] at [Branch] on [Date]" | Success | 3s |
| Audit rescheduled | "Audit rescheduled to [New Date]" | Info | 3s |
| Audit cancelled | "Audit cancelled" | Info | 3s |
| Auditor assigned | "[Auditor Name] assigned to [Branch] audit" | Success | 3s |
| Availability updated | "Availability updated for [Date Range]" | Info | 3s |
| Branch notification sent | "Branch [Name] notified of upcoming audit" | Info | 3s |
| Conflict detected | "⚠️ Auditor [Name] has conflicting assignment on [Date]" | Warning | 5s |
| Plan behind schedule | "⚠️ Audit plan is [N]% behind schedule for [Month]" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No AAP | 📋 | "No Annual Audit Plan" | "Create an Annual Audit Plan to structure your compliance programme." | Create Plan |
| No audits scheduled | 📅 | "No Audits Scheduled" | "Schedule audits based on the approved plan to begin compliance tracking." | Schedule Audit |
| No auditors | 👤 | "No Auditors Assigned" | "Assign inspection officers to begin field audits." | — |
| No risk data | ⚠️ | "Risk Assessment Pending" | "Complete at least one audit cycle to generate branch risk scores." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + calendar skeleton |
| Calendar navigation (month/week) | Calendar grid skeleton |
| AAP table load | Table skeleton with 30 rows |
| Auditor workload tab | Table skeleton + bar chart placeholder |
| Risk matrix tab | Heatmap placeholder |
| Audit detail drawer | 720px skeleton: 6 tabs |
| Create plan modal | Form skeleton |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/calendar/` | G1+ | Calendar events (audits) with date range filter |
| GET | `/api/v1/group/{id}/audit/calendar/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/audit/plans/` | G1+ | List annual audit plans |
| GET | `/api/v1/group/{id}/audit/plans/{plan_id}/` | G1+ | Plan detail |
| POST | `/api/v1/group/{id}/audit/plans/` | 121, G4+ | Create annual audit plan |
| PUT | `/api/v1/group/{id}/audit/plans/{plan_id}/` | 121, G4+ | Update plan |
| PATCH | `/api/v1/group/{id}/audit/plans/{plan_id}/approve/` | G4+ | Approve/revise plan |
| POST | `/api/v1/group/{id}/audit/audits/` | 121, 122, 125 | Schedule an audit |
| PUT | `/api/v1/group/{id}/audit/audits/{audit_id}/` | 121 | Update/reschedule audit |
| PATCH | `/api/v1/group/{id}/audit/audits/{audit_id}/cancel/` | 121, G4+ | Cancel audit |
| GET | `/api/v1/group/{id}/audit/audits/{audit_id}/` | G1+ | Audit detail |
| GET | `/api/v1/group/{id}/audit/calendar/auditor-workload/` | G1+ | Auditor workload data |
| PATCH | `/api/v1/group/{id}/audit/auditors/{user_id}/availability/` | 121, 123 | Update availability |
| GET | `/api/v1/group/{id}/audit/calendar/risk-matrix/` | G1+ | Branch risk assessment |
| GET | `/api/v1/group/{id}/audit/calendar/plan-progress/` | G1+ | AAP progress gauge data |
| GET | `/api/v1/group/{id}/audit/calendar/monthly-distribution/` | G1+ | Monthly distribution chart |
| POST | `/api/v1/group/{id}/audit/plans/{plan_id}/auto-generate/` | 121 | Auto-generate plan from risk matrix |
| GET | `/api/v1/group/{id}/audit/calendar/export/` | G1+ | Export plan as PDF/Excel |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../calendar/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Calendar render | Page load / navigation | Non-HTMX (FullCalendar.js) | — | — | JavaScript calendar init, fetches events via API |
| Tab switch | Tab click | `hx-get` with tab param | `#calendar-content` | `innerHTML` | `hx-trigger="click"` |
| Schedule audit | Form submit | `hx-post=".../audits/"` | `#schedule-result` | `innerHTML` | Toast + calendar refresh |
| Create plan | Form submit | `hx-post=".../plans/"` | `#plan-result` | `innerHTML` | Toast |
| Approve plan | Approve button | `hx-patch=".../plans/{id}/approve/"` | `#plan-status` | `innerHTML` | Toast + status badge update |
| Audit detail drawer | Calendar event click | `hx-get=".../audits/{id}/"` | `#right-drawer` | `innerHTML` | 720px drawer |
| Reschedule (drag-drop) | Calendar drag-drop | `hx-put=".../audits/{id}/"` | `#audit-{id}` | `innerHTML` | JavaScript → HTMX bridge |
| Filter calendar | Filter change | Non-HTMX (FullCalendar filter) | — | — | Client-side filtering |
| Auditor availability | Form submit | `hx-patch=".../auditors/{id}/availability/"` | `#availability-result` | `innerHTML` | Toast |
| Risk matrix load | Tab 4 shown | `hx-get=".../calendar/risk-matrix/"` | `#risk-content` | `innerHTML` | Heatmap render |
| Export plan | Button click | `hx-get=".../calendar/export/"` | `#export-result` | `innerHTML` | Download trigger |
| Auto-generate | Button click | `hx-post=".../plans/{id}/auto-generate/"` | `#plan-table` | `innerHTML` | Populates plan from risk matrix |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
