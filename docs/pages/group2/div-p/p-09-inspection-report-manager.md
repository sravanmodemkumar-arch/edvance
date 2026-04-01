# P-09 — Inspection Report Manager

> **URL:** `/group/audit/inspections/reports/`
> **File:** `p-09-inspection-report-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Inspection Officer (Role 123, G3) — primary operator

---

## 1. Purpose

The Inspection Report Manager stores and manages the output of every branch inspection — the completed checklist, observations, photos, scores, findings, and recommendations. In Indian education, inspection reports serve multiple purposes: internal compliance tracking, evidence for the Trust Board, preparation documents for external audits (CBSE/State Board), and legal defence in case of incidents. A well-documented inspection report proves the group exercised due diligence.

The problems this page solves:

1. **Lost inspection data:** Without a central system, inspection notes are in personal notebooks, photos on inspector phones (deleted after 6 months), and reports in local Excel files. When a CBSE committee asks "When was your last safety audit at Branch X?", the group scrambles to find evidence. The Report Manager preserves everything permanently.

2. **48-hour report deadline enforcement:** An inspection without a timely report is wasted — the inspector forgets details, photos lose context, and branch corrections aren't tracked. The system enforces: report must be submitted within 48 hours of check-out. Overdue reports are flagged to the Audit Head.

3. **Standardised report format:** Different inspectors write reports in different formats — some write two paragraphs, others write ten pages. The Report Manager enforces a standardised template: executive summary, section-wise scores, detailed observations, photo evidence, findings generated, and recommendations.

4. **Comparative analysis:** When the same branch is inspected quarterly, the report should show improvement or degradation. The Report Manager auto-generates comparison with previous inspection — score trends, previously open findings (now closed?), new issues, and persistent problems.

5. **PDF export for Board:** Trust Board meetings require polished inspection reports. The system generates professional PDFs with group branding, photos, score charts, and finding summaries — ready for Board presentation without manual formatting.

**Scale:** 60–200 inspection reports/year · 10–50 photos per report · 48-hour submission deadline · permanent archive · PDF export

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Inspection Officer | 123 | G3 | Full — create, edit, submit reports | Primary author |
| Group Internal Audit Head | 121 | G1 | Full — review, approve, sign-off reports | Review authority |
| Group Academic Quality Officer | 122 | G1 | Read — academic inspection reports | Own-domain reports |
| Group Affiliation Compliance Officer | 125 | G1 | Read — affiliation inspection reports | Own-domain reports |
| Group Compliance Data Analyst | 127 | G1 | Read — all reports for analytics | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read — reports with findings for CAPA follow-up | CAPA linkage |
| Group CEO / Chairman | — | G4/G5 | Read — all reports | Governance |
| Branch Principal | — | G3 | Read (own branch) — signed-off reports only | Action and awareness |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Branch Principals see only their branch's signed-off reports (not draft or under-review).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Inspections  ›  Reports
```

### 3.2 Page Header
```
Inspection Report Manager                              [+ Create Report]  [Bulk Export]  [Report Templates]
Inspection Team
Sunrise Education Group · FY 2025-26 · 102 reports submitted · 8 pending · 3 overdue
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Reports Submitted (FY) | Integer | COUNT(reports) WHERE status IN ('submitted', 'reviewed', 'signed_off') AND fy = current | Static blue | `#kpi-submitted` |
| 2 | Pending Submission | Integer | Reports not submitted within 48h of visit | Red > 5, Amber 1–5, Green = 0 | `#kpi-pending` |
| 3 | Overdue Reports | Integer | Reports > 48h past visit with no submission | Red > 0, Green = 0 | `#kpi-overdue` |
| 4 | Avg Report Score | Percentage | AVG(overall_score) across all reports this FY | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-avg-score` |
| 5 | Findings Generated | Integer | Total findings auto-generated from reports this FY | Static blue | `#kpi-findings` |
| 6 | Reports Signed Off | Integer | Reports fully reviewed and signed off by Audit Head | Static blue | `#kpi-signedoff` |

---

## 5. Sections

### 5.1 Tab Navigation

Three tabs:
1. **All Reports** — Master list with filters
2. **Pending Action** — Reports needing submission, review, or sign-off
3. **Branch History** — Per-branch inspection report archive with comparison

### 5.2 Tab 1: All Reports

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Report ID | Text (link) | Yes | Auto: RPT-2026-001 |
| Branch | Text | Yes | — |
| Visit Date | Date | Yes | — |
| Visit Type | Badge | Yes | Scheduled / Surprise / Follow-up / Pre-Affiliation |
| Inspector | Text | Yes | — |
| Checklist Used | Text | Yes | From P-08 |
| Overall Score | Percentage | Yes | Weighted composite |
| Findings | Integer | Yes | Count generated |
| Critical | Integer | Yes | S1 findings |
| Status | Badge | Yes | Draft / Submitted / Under Review / Revision Requested / Signed Off |
| Submitted | Date | Yes | Submission date |
| Within 48h? | Badge | Yes | ✅ Yes / 🔴 No (hours late) |
| Actions | Buttons | No | [View] [Edit] [Review] [Sign Off] [Export PDF] |

### 5.3 Tab 2: Pending Action

**Three sections:**

**Overdue Submissions (inspector action):**
- Visit date, branch, inspector, hours overdue, [Submit Now] button

**Awaiting Review (Audit Head action):**
- Report ID, branch, submitted date, inspector, [Review] button

**Revision Requested (inspector action):**
- Report ID, branch, reviewer notes, [Edit & Resubmit] button

### 5.4 Tab 3: Branch History

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Total Reports | Integer | Yes | All-time |
| This FY | Integer | Yes | — |
| Latest Score | Percentage | Yes | Most recent inspection |
| Score Trend | Sparkline | No | Last 4 inspections |
| Improvement | Arrow + % | Yes | Latest score vs previous |
| Persistent Issues | Integer | Yes | Findings found in ≥ 2 consecutive inspections |
| Last Visit | Date | Yes | — |

**Click branch → expands to show all reports for that branch chronologically**

---

## 6. Drawers & Modals

### 6.1 Drawer: `report-detail` (780px, right-slide)

- **Title:** "Inspection Report — [Branch] · [Date]"
- **Tabs:** Summary · Checklist Results · Observations · Photos · Findings · Comparison · Sign-off
- **Summary tab:**
  - Executive summary (auto-generated from scores + manually editable)
  - Visit metadata: date, time, duration, type, inspector, checklist used
  - Overall score with grade badge
  - Section-wise score breakdown (radar chart)
  - Key strengths (auto: highest-scoring sections)
  - Key concerns (auto: lowest-scoring sections + non-compliant items)
- **Checklist Results tab:**
  - Full completed checklist with item-by-item status
  - Green/Amber/Red per item
  - Inspector comments per item
  - Evidence links per item
- **Observations tab:**
  - Free-text observations organized by section
  - Inspector's detailed notes beyond checklist items
  - Recommendations
- **Photos tab:**
  - Gallery of all photos — geotagged, timestamped, linked to checklist items
  - Before/after pairs if follow-up visit
  - Captioned with observation notes
- **Findings tab:**
  - Auto-generated findings from non-compliant checklist items
  - Inspector can add/edit/remove before submission
  - Each finding linked to P-06 (Finding Tracker) and P-15 (CAPA)
- **Comparison tab:**
  - Side-by-side with previous inspection of same branch
  - Score comparison per section
  - Previously open findings: closed? still open?
  - New issues not in previous inspection
  - Improvement/degradation summary
- **Sign-off tab:**
  - Reviewer (Audit Head) comments
  - Approval/revision decision with notes
  - Digital sign-off with timestamp
  - Branch Principal acknowledgment status (notified → read → acknowledged)
- **Footer:** [Edit] [Submit for Review] [Request Revision] [Sign Off] [Export PDF]
- **Access:** G1+ (Division P roles)

### 6.2 Modal: `create-report` (560px)

- **Title:** "Create Inspection Report"
- **Fields:**
  - Linked visit (dropdown — auto-lists visits without reports, required)
  - Or manual entry: Branch + Date + Inspector (if visit not logged in P-07)
  - Checklist used (auto-filled from visit, or manual select from P-08)
  - Executive summary (textarea — brief overview of inspection)
  - Observations by section (repeated per checklist section — textarea each)
  - Overall recommendation (dropdown): Satisfactory / Needs Improvement / Unsatisfactory / Critical Action Required
  - Attach photos (multi-file upload)
- **Buttons:** Cancel · Save Draft · Submit for Review
- **Validation:** At least 80% of checklist items must be filled before submission
- **Access:** Role 123

### 6.3 Modal: `review-report` (560px, Role 121)

- **Title:** "Review Report — [Report ID]"
- **Content:** Report summary, score, findings count, checklist completion %
- **Reviewer fields:**
  - Review notes (textarea)
  - Score adjustment? (toggle — reviewer can adjust ±5% with justification)
  - Finding review: Agree with all / Modify specific findings
  - Decision (radio): Approve / Request Revision / Reject
  - If Request Revision: Specific items to revise (textarea)
- **Buttons:** Cancel · Submit Review
- **Access:** Role 121, G4+

### 6.4 Modal: `export-report-pdf` (480px)

- **Title:** "Export Report as PDF"
- **Fields:**
  - Include sections (checkboxes): Summary / Checklist / Observations / Photos / Findings / Comparison / Sign-off
  - Include photos? (toggle — PDFs can get large with photos)
  - Photo quality (if included): High / Medium / Thumbnail
  - Include group branding header? (toggle — default yes)
  - Watermark (dropdown): None / CONFIDENTIAL / DRAFT / FOR INTERNAL USE
- **Buttons:** Cancel · Generate PDF
- **Output:** Download link when ready (async generation for large reports)
- **Access:** G1+ (Division P roles)

---

## 7. Charts

### 7.1 Score Distribution (Histogram)

| Property | Value |
|---|---|
| Chart type | Bar/Histogram (Chart.js 4.x) |
| Title | "Inspection Score Distribution — FY to Date" |
| Data | COUNT(reports) per score bucket: 0–50%, 51–60%, 61–70%, 71–80%, 81–90%, 91–100% |
| Colour | Red → Amber → Green gradient |
| API | `GET /api/v1/group/{id}/audit/inspections/reports/analytics/score-distribution/` |

### 7.2 Monthly Report Volume (Bar + Line)

| Property | Value |
|---|---|
| Chart type | Combo: bar (submitted) + line (avg score) |
| Title | "Monthly Inspection Reports — Volume & Quality" |
| Data | Per month: report count (bar) + avg score (line) |
| API | `GET /api/v1/group/{id}/audit/inspections/reports/analytics/monthly-volume/` |

### 7.3 Section Score Radar (Group Average)

| Property | Value |
|---|---|
| Chart type | Radar/Spider |
| Title | "Group Average — Inspection Score by Section" |
| Data | AVG score per checklist section across all reports |
| Overlay | Previous quarter for comparison |
| API | `GET /api/v1/group/{id}/audit/inspections/reports/analytics/section-radar/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Report draft saved | "Report draft saved" | Info | 2s |
| Report submitted | "Report [ID] submitted for review" | Success | 3s |
| Report approved | "Report [ID] approved and signed off" | Success | 4s |
| Revision requested | "Report [ID] — revision requested: [Notes preview]" | Warning | 5s |
| PDF generated | "PDF ready for download" | Success | 3s |
| Report overdue | "⚠️ Report overdue for visit on [Date] at [Branch]" | Warning | 5s |
| Branch notified | "Branch [Name] notified of signed-off report" | Info | 3s |
| Finding auto-generated | "[N] findings auto-generated from non-compliant items" | Info | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No reports | 📝 | "No Inspection Reports" | "Reports will appear after branch inspections are completed." | View Scheduler |
| No pending actions | ✅ | "All Reports Up to Date" | "No reports pending submission, review, or sign-off." | — |
| No branch history | 🏫 | "No Inspection History" | "Branch inspection history will build as visits are conducted." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + table skeleton |
| Report detail drawer | 780px skeleton: 7 tabs |
| Photo gallery | Image grid placeholder |
| Comparison view | Side-by-side skeleton |
| PDF generation | Progress spinner with "Generating…" |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/inspections/reports/` | G1+ | List all reports |
| GET | `/api/v1/group/{id}/audit/inspections/reports/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/audit/inspections/reports/{report_id}/` | G1+ | Report detail |
| POST | `/api/v1/group/{id}/audit/inspections/reports/` | 123 | Create report |
| PUT | `/api/v1/group/{id}/audit/inspections/reports/{report_id}/` | 123 | Update report |
| PATCH | `/api/v1/group/{id}/audit/inspections/reports/{report_id}/submit/` | 123 | Submit for review |
| PATCH | `/api/v1/group/{id}/audit/inspections/reports/{report_id}/review/` | 121, G4+ | Review (approve/revise/reject) |
| PATCH | `/api/v1/group/{id}/audit/inspections/reports/{report_id}/signoff/` | 121, G4+ | Sign off |
| GET | `/api/v1/group/{id}/audit/inspections/reports/{report_id}/comparison/` | G1+ | Comparison with previous |
| GET | `/api/v1/group/{id}/audit/inspections/reports/{report_id}/photos/` | G1+ | Photos for this report |
| POST | `/api/v1/group/{id}/audit/inspections/reports/{report_id}/photos/` | 123 | Upload photos |
| GET | `/api/v1/group/{id}/audit/inspections/reports/{report_id}/export/` | G1+ | Export as PDF |
| GET | `/api/v1/group/{id}/audit/inspections/reports/pending/` | G1+ | Pending action items |
| GET | `/api/v1/group/{id}/audit/inspections/reports/branch-history/` | G1+ | Branch history table |
| GET | `/api/v1/group/{id}/audit/inspections/reports/branch-history/{branch_id}/` | G1+ | Specific branch report history |
| GET | `/api/v1/group/{id}/audit/inspections/reports/analytics/score-distribution/` | G1+ | Score histogram |
| GET | `/api/v1/group/{id}/audit/inspections/reports/analytics/monthly-volume/` | G1+ | Monthly volume chart |
| GET | `/api/v1/group/{id}/audit/inspections/reports/analytics/section-radar/` | G1+ | Section radar chart |
| POST | `/api/v1/group/{id}/audit/inspections/reports/bulk-export/` | G1+ | Bulk export multiple reports |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../reports/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#reports-content` | `innerHTML` | `hx-trigger="click"` |
| Report detail drawer | Row click | `hx-get=".../reports/{id}/"` | `#right-drawer` | `innerHTML` | 780px drawer |
| Create report | Form submit | `hx-post=".../reports/"` | `#create-result` | `innerHTML` | Toast |
| Submit for review | Button click | `hx-patch=".../reports/{id}/submit/"` | `#status-badge` | `innerHTML` | Toast |
| Review report | Form submit | `hx-patch=".../reports/{id}/review/"` | `#review-result` | `innerHTML` | Toast |
| Sign off | Button click | `hx-patch=".../reports/{id}/signoff/"` | `#signoff-result` | `innerHTML` | Toast |
| Photo upload | Form submit | `hx-post=".../reports/{id}/photos/"` | `#photo-gallery` | `beforeend` | Append |
| Export PDF | Form submit | `hx-get=".../reports/{id}/export/"` | `#export-result` | `innerHTML` | Download link |
| Branch history expand | Row click (Tab 3) | `hx-get=".../branch-history/{id}/"` | `#branch-{id}-detail` | `innerHTML` | Inline expand |
| Filter | Filter change | `hx-get` with filters | `#report-table` | `innerHTML` | `hx-trigger="change"` |
| Chart load | Tab shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |
| Pagination | Page click | `hx-get` with page param | `#table-body` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
