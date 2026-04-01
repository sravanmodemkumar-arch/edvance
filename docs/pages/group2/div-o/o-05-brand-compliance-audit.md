# O-05 — Brand Compliance Audit

> **URL:** `/group/marketing/brand/compliance/`
> **File:** `o-05-brand-compliance-audit.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Campaign Content Coordinator (Role 131, G2) — primary auditor

---

## 1. Purpose

The Brand Compliance Audit page tracks whether every branch in the group is correctly using the approved brand identity — logos, colours, fonts, signage, stationery, digital presence, and marketing materials. In a 30-branch education group, brand drift is inevitable: a branch prints pamphlets with the 2019 logo, another uses a completely wrong shade of blue on their gate board, a third misspells the tagline, and a fourth puts up a flex banner claiming "No. 1 in Telangana" without any substantiation — which violates ASCI (Advertising Standards Council of India) guidelines and can attract legal action.

This page provides a structured audit framework where the Content Coordinator conducts periodic branch audits (quarterly for large groups, biannually for small groups), scores each branch on a set of brand compliance checkpoints, records photographic evidence of violations, assigns corrective actions with deadlines, and tracks resolution. The audit results feed into the Brand Compliance Score visible on the O-01 Dashboard and the O-02 Brand Standards KPI card.

**Scale:** 5–50 branches audited · 15–25 checkpoints per audit · Quarterly cycle · Resolution tracked until closure

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Campaign Content Coordinator | 131 | G2 | Full CRUD — create audits, score, assign actions | Primary auditor |
| Group Admissions Campaign Manager | 119 | G3 | Read + Assign corrective actions | Can assign tasks to branch staff |
| Group Admission Data Analyst | 132 | G1 | Read only | View scores and trends |
| Branch Principal | — | G3 | Read (own branch) + Respond to actions | Sees own branch audit; responds to findings |
| Branch Admin | — | G2 | Read (own branch) + Upload evidence | Uploads corrective photos |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Branch users filtered to own branch.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Brand & Content  ›  Brand Compliance Audit
```

### 3.2 Page Header
```
Brand Compliance Audit                         [Start New Audit]  [Schedule Audit Cycle]  [Export Report]
Content Coordinator — Meena Raghavan
Sunrise Education Group · Last audit cycle: Q4 2025 · Group avg score: 84%
```

---

## 4. KPI Summary Bar (5 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Group Avg Score | Percentage | AVG(branch_audit_score) latest cycle | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-avg-score` |
| 2 | Branches Audited | N / Total | COUNT audited this cycle / total branches | Green = 100%, Amber < 100% | `#kpi-audited` |
| 3 | Open Findings | Integer | COUNT(findings) WHERE status = 'open' | Red > 20, Amber 10–20, Green < 10 | `#kpi-open-findings` |
| 4 | Overdue Actions | Integer | COUNT(actions) WHERE due_date < TODAY AND status ≠ 'resolved' | Red > 0, Green = 0 | `#kpi-overdue` |
| 5 | Fully Compliant Branches | Integer | COUNT branches WHERE score = 100% | Static green | `#kpi-fully-compliant` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/brand/compliance/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Audit Cycle Overview

**Filter:** Audit cycle (dropdown): Current / Q4 2025 / Q3 2025 / etc.

**Branch Scores Table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Branch | Text | Yes | Branch name + city |
| Audit Date | Date | Yes | When audit was conducted |
| Auditor | Text | Yes | Who conducted the audit |
| Score | Progress bar + % | Yes | 0–100; green ≥ 90, amber 70–89, red < 70 |
| Findings | Integer | Yes | Total non-compliance findings |
| Open | Integer | Yes | Unresolved findings |
| Critical | Integer | Yes | Severity = Critical findings (red badge) |
| Trend | Arrow | No | ↑ improved / → same / ↓ declined vs previous cycle |
| Status | Badge | Yes | Completed / In Progress / Scheduled / Overdue |
| Actions | Button | No | [View Audit →] |

**Default sort:** Score ASC (worst first)
**Pagination:** Server-side · 25/page

### 5.2 Audit Checklist Template

The standard checklist used for every branch audit. Customisable by G4/G5.

**Checkpoint Categories & Items:**

| # | Category | Checkpoint | Weight | Evidence Required |
|---|---|---|---|---|
| 1 | Logo | Main gate board displays current logo version | 10 | Photo |
| 2 | Logo | Building facade logo matches approved variant | 8 | Photo |
| 3 | Logo | Printed materials (pamphlets, brochures) use correct logo | 6 | Sample scan |
| 4 | Logo | Digital presence (website, social media) uses correct logo | 6 | Screenshot |
| 5 | Logo | Staff ID cards show current logo | 4 | Photo |
| 6 | Colours | Gate board colours match brand palette | 8 | Photo |
| 7 | Colours | Interior signage uses approved colour scheme | 6 | Photo |
| 8 | Colours | Printed materials use correct colours | 5 | Sample |
| 9 | Typography | Signage fonts match brand specification | 6 | Photo |
| 10 | Typography | Printed materials use approved fonts | 5 | Sample |
| 11 | Signage | All signage in good physical condition | 5 | Photo |
| 12 | Signage | Direction signs present and correct | 3 | Photo |
| 13 | Signage | Classroom nameplates standardised | 3 | Photo |
| 14 | Signage | Bus branding matches template | 5 | Photo |
| 15 | Content | Branch name spelled correctly on all signage | 5 | Photo |
| 16 | Content | Contact number on signage is current and active | 3 | Verification |
| 17 | Content | Tagline matches approved version | 3 | Photo |
| 18 | Content | No unauthorised claims (No. 1, 100% results, etc.) | 5 | Photo / scan |
| 19 | Stationery | Letterhead uses current template | 2 | Sample |
| 20 | Stationery | Fee receipts use approved format | 2 | Sample |
| 21 | Digital | Google My Business listing has correct branding | 3 | Screenshot |
| 22 | Digital | WhatsApp Business profile pic is correct | 2 | Screenshot |
| 23 | Municipal | All outdoor signage has valid municipal permit | 5 | Permit copy |

**Total weight:** 100 points. Score = SUM(weighted points for passed checkpoints) / 100 × 100%.

### 5.3 Individual Branch Audit View

Opens when clicking "View Audit" from the scores table.

**Checklist Table:**

| Column | Type | Notes |
|---|---|---|
| # | Integer | Checkpoint number |
| Category | Badge | Logo / Colours / Typography / Signage / Content / Stationery / Digital / Municipal |
| Checkpoint | Text | Checkpoint description |
| Weight | Integer | Points |
| Status | Badge | ✅ Pass / ❌ Fail / ⚠️ Partial / ⏭️ N/A |
| Evidence | Thumbnail | Photo/screenshot uploaded by auditor |
| Finding | Text | Description of non-compliance (if Fail/Partial) |
| Severity | Badge | Critical (red) / Major (orange) / Minor (yellow) |
| Corrective Action | Text | Assigned action to fix |
| Assigned To | Text | Person responsible |
| Due Date | Date | Deadline |
| Resolution Status | Badge | Open / In Progress / Resolved / Overdue |

### 5.4 Corrective Action Tracker

Aggregated view of all open and overdue corrective actions across all branches.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | Branch name |
| Checkpoint | Text | Yes | Which checkpoint failed |
| Finding | Text | No | What's wrong |
| Severity | Badge | Yes | Critical / Major / Minor |
| Assigned To | Text | Yes | Responsible person |
| Due Date | Date | Yes | Deadline |
| Days Overdue | Integer | Yes | Red if positive |
| Status | Badge | Yes | Open / In Progress / Resolved |
| Evidence (Fix) | Thumbnail | No | Photo showing fix (uploaded by branch) |
| Actions | Buttons | No | [View] [Mark Resolved] |

**Default sort:** Days Overdue DESC (most overdue first)

---

## 6. Drawers & Modals

### 6.1 Modal: `start-audit` (560px)
- **Title:** "Start Branch Audit"
- **Fields:**
  - Branch (dropdown, required)
  - Audit date (date, default today)
  - Auditor name (auto-filled with current user, editable)
  - Audit cycle (dropdown — auto-selected to current cycle)
  - Use standard checklist (toggle, default ON) / Custom checklist (select from templates)
  - Notes (textarea)
- **Buttons:** Cancel · Start Audit
- **Behaviour:** Creates audit record → redirects to checklist scoring view

### 6.2 Modal: `schedule-cycle` (480px)
- **Title:** "Schedule Audit Cycle"
- **Fields:**
  - Cycle name (text — e.g., "Q1 2026")
  - Start date → End date
  - Branches to include: All / Select specific
  - Auditor assignment: Auto-rotate / Manual assignment per branch
  - Notification: Send audit schedule to branch principals (toggle)
- **Buttons:** Cancel · Schedule
- **Access:** G4/G5 only

### 6.3 Drawer: `finding-detail` (640px, right-slide)
- **Tabs:** Finding · Evidence · Timeline · Resolution
- **Finding tab:** Checkpoint, description of non-compliance, severity, auditor notes
- **Evidence tab:** Photos uploaded by auditor (before) and branch (after fix)
- **Timeline tab:** Status changes with timestamps
- **Resolution tab:** Resolution notes, evidence of fix, verified by auditor, closure date
- **Footer:** [Mark Resolved] [Escalate] [Edit] (role-dependent)

---

## 7. Charts

### 7.1 Group Compliance Score Trend (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Group Brand Compliance Score — Last 4 Cycles" |
| Data | Average brand compliance score per audit cycle |
| X-axis | Audit cycle (Q1 2025, Q2 2025, Q3 2025, Q4 2025) |
| Y-axis | Score (0–100%) |
| Colour | `#3B82F6` blue line; reference line at 90% target (dashed green) |
| API | `GET /api/v1/group/{id}/marketing/brand/compliance/analytics/score-trend/` |

### 7.2 Branch Score Distribution (Bar Chart)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Branch-wise Brand Compliance Scores — Latest Cycle" |
| Data | Score per branch |
| Colour | Green ≥ 90, Amber 70–89, Red < 70 (per bar) |
| API | `GET /api/v1/group/{id}/marketing/brand/compliance/analytics/branch-scores/` |

### 7.3 Findings by Category (Donut)

| Property | Value |
|---|---|
| Chart type | Donut |
| Title | "Non-Compliance Findings by Category" |
| Data | COUNT findings per category (Logo, Colours, Typography, etc.) |
| Colour | Distinct per category |
| API | `GET /api/v1/group/{id}/marketing/brand/compliance/analytics/findings-by-category/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit started | "Audit started for [Branch] — complete checklist to generate score" | Success | 3s |
| Audit completed | "Audit for [Branch] completed — Score: [X]%. [N] findings recorded." | Success | 5s |
| Finding added | "Finding recorded: [Checkpoint] — Severity: [Level]" | Info | 3s |
| Action assigned | "Corrective action assigned to [Person] — due [Date]" | Success | 3s |
| Action resolved | "Finding resolved for [Branch] — [Checkpoint]" | Success | 3s |
| Cycle scheduled | "Audit cycle '[Name]' scheduled for [N] branches" | Success | 4s |
| Overdue alert | "[N] corrective actions overdue across [M] branches" | Warning | 6s |
| Export generated | "Brand Compliance Report ready for download" | Success | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No audits conducted | 📋 | "No Audits Yet" | "Start your first brand compliance audit to establish baseline scores." | Start Audit |
| No audit cycle scheduled | 📅 | "No Audit Cycle Active" | "Schedule an audit cycle to plan branch audits." | Schedule Cycle |
| No open findings | ✅ | "All Clear" | "No open brand compliance findings. All branches are on track." | — |
| Branch not yet audited this cycle | 🔍 | "Audit Pending" | "This branch has not been audited in the current cycle." | Start Audit |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 5 KPI shimmer cards + table skeleton (10 rows) |
| Branch audit view | Checklist skeleton: 23 rows with photo placeholders |
| Finding detail drawer | Right-slide skeleton with image placeholder + 4 tabs |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/brand/compliance/` | G1+ | List audit cycles and branch scores |
| GET | `/api/v1/group/{id}/marketing/brand/compliance/kpis/` | G1+ | KPI values |
| POST | `/api/v1/group/{id}/marketing/brand/compliance/audits/` | G2+ | Start new audit |
| GET | `/api/v1/group/{id}/marketing/brand/compliance/audits/{audit_id}/` | G1+ | Single audit detail (checklist + scores) |
| PUT | `/api/v1/group/{id}/marketing/brand/compliance/audits/{audit_id}/` | G2+ | Update audit (score checkpoints) |
| POST | `/api/v1/group/{id}/marketing/brand/compliance/audits/{audit_id}/findings/` | G2+ | Add finding |
| PATCH | `/api/v1/group/{id}/marketing/brand/compliance/findings/{finding_id}/` | G2+ | Update finding status |
| POST | `/api/v1/group/{id}/marketing/brand/compliance/findings/{finding_id}/evidence/` | G2+ | Upload evidence photo |
| POST | `/api/v1/group/{id}/marketing/brand/compliance/cycles/` | G4+ | Schedule audit cycle |
| GET | `/api/v1/group/{id}/marketing/brand/compliance/actions/` | G1+ | Corrective actions list |
| GET | `/api/v1/group/{id}/marketing/brand/compliance/analytics/score-trend/` | G1+ | Score trend data |
| GET | `/api/v1/group/{id}/marketing/brand/compliance/analytics/branch-scores/` | G1+ | Branch scores chart |
| GET | `/api/v1/group/{id}/marketing/brand/compliance/analytics/findings-by-category/` | G1+ | Findings breakdown |
| POST | `/api/v1/group/{id}/marketing/brand/compliance/export/` | G1+ | Export report |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../compliance/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Scores table load | `<div id="scores-table">` | `hx-get=".../compliance/?cycle={id}"` | `#scores-table-body` | `innerHTML` | `hx-trigger="load"` |
| Cycle filter | Cycle dropdown | `hx-get=".../compliance/?cycle={id}"` | `#scores-table-body` | `innerHTML` | `hx-trigger="change"` |
| View audit | Row click | `hx-get=".../compliance/audits/{id}/"` | `#audit-detail` | `innerHTML` | Full checklist view |
| Score checkpoint | Checkbox/dropdown in checklist | `hx-patch=".../audits/{id}/checkpoints/{n}/"` | `#checkpoint-row-{n}` | `outerHTML` | Inline update |
| Finding drawer | Finding row click | `hx-get=".../compliance/findings/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Upload evidence | Photo form | `hx-post=".../findings/{id}/evidence/"` | `#evidence-gallery` | `beforeend` | `hx-encoding="multipart/form-data"` |
| Mark resolved | Resolve button | `hx-patch=".../findings/{id}/" (status=resolved)` | `#finding-row-{id}` | `outerHTML` | Row updates in place |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
