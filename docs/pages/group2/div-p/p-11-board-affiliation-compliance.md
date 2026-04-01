# P-11 — Board Affiliation Compliance Tracker

> **URL:** `/group/audit/affiliation/`
> **File:** `p-11-board-affiliation-compliance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Affiliation Compliance Officer (Role 125, G1) — primary operator

---

## 1. Purpose

The Board Affiliation Compliance Tracker monitors every requirement that CBSE, ICSE, or state education boards mandate for school affiliation — and tracks each branch's compliance against those requirements. In Indian education, affiliation is existential: without valid CBSE affiliation, a school cannot conduct board exams for Class 10 and 12. Loss of affiliation means 500–3,000 students cannot appear for their board exams — a catastrophe for the school, the group, and the families.

The problems this page solves:

1. **CBSE affiliation has 40+ mandatory requirements:** Teacher-student ratio ≤ 1:30, minimum playground area (as per norms), functional science labs, library with minimum books, fire safety NOC, building stability certificate, CCTV installation, IT infrastructure, trained counsellor on staff, compliance with RTE norms, and more. A single missed requirement can delay affiliation renewal by 6–12 months. This tracker ensures nothing is missed.

2. **Multiple boards, multiple norms:** A group may have branches affiliated to CBSE (central norms), BSEAP (Andhra Pradesh state board), BSETS (Telangana state board), ICSE, or even multiple boards at the same branch (CBSE up to Class 10, state board for Class 11–12). Each board has different requirements. The tracker maintains separate compliance matrices per board.

3. **Renewal timelines:** CBSE affiliation is granted for 5 years. If a group has 30 branches, 6 branches come up for renewal every year. The tracker shows: which branches are due when, readiness percentage, gap analysis, and time remaining — so preparation starts 12 months before expiry, not 2 months.

4. **Document readiness:** Affiliation renewal requires submitting 25–40 documents: school recognition order, land ownership/lease deed, building stability certificate, fire NOC, audited balance sheet, teacher qualification certificates, fee structure approval, and more. The tracker maintains a per-branch document checklist with upload, expiry, and verification status.

5. **Post-inspection compliance:** After CBSE inspection, the committee may issue conditional compliance requirements: "Install 5 additional CCTV cameras within 90 days." The tracker tracks these conditions with deadlines and evidence submission.

**Scale:** 5–50 branches · 3–5 board types · 40+ requirements per board · 25–40 documents per branch · 5-year renewal cycles · 12-month preparation window

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Affiliation Compliance Officer | 125 | G1 | Full — manage requirements, track readiness, upload documents | Primary operator |
| Group Internal Audit Head | 121 | G1 | Read + oversight — affiliation risk in scorecard | Cross-functional |
| Group Inspection Officer | 123 | G3 | Read + update — mark requirements as verified during visits | On-site verification |
| Group ISO / NAAC Coordinator | 124 | G1 | Read — cross-reference with quality certification | Coordination |
| Group Compliance Data Analyst | 127 | G1 | Read — affiliation data for MIS | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read + CAPA — for gap closure tracking | Drives remediation |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — affiliation decisions, budget for compliance | Final authority |
| Branch Principal | — | G3 | Read (own branch) + Upload documents | Branch-level compliance execution |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Document uploads: 125, 123, Branch Principal. Requirement verification: 123, 125.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Board Affiliation Compliance
```

### 3.2 Page Header
```
Board Affiliation Compliance Tracker               [+ Add Board Affiliation]  [Gap Analysis]  [Export]
Affiliation Compliance Officer — S. Padmavathi
Sunrise Education Group · 28 branches · CBSE: 22 · BSEAP: 4 · BSETS: 2 · 3 renewals due in 12 months
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Affiliations | Integer | COUNT(affiliations) WHERE status = 'active' | Static blue | `#kpi-active` |
| 2 | Renewals Due (12m) | Integer | COUNT WHERE expiry_date BETWEEN today AND today + 365 | Red > 5, Amber 1–5, Green = 0 | `#kpi-renewals` |
| 3 | Avg Readiness | Percentage | AVG(requirements_met_%) across branches due for renewal | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-readiness` |
| 4 | Expired Affiliations | Integer | COUNT WHERE expiry_date < today AND status != 'renewed' | Red > 0, Green = 0 | `#kpi-expired` |
| 5 | Pending Conditions | Integer | Post-inspection conditions not yet fulfilled | Red > 5, Amber 1–5, Green = 0 | `#kpi-conditions` |
| 6 | Documents Expiring (30d) | Integer | Branch documents expiring within 30 days (Fire NOC, stability cert, etc.) | Red > 5, Amber 1–5, Green = 0 | `#kpi-docs` |

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Affiliation Status** — All branches with affiliation details
2. **Requirements Matrix** — Board requirement compliance per branch
3. **Document Tracker** — Per-branch document readiness
4. **Renewal Pipeline** — Branches in renewal process

### 5.2 Tab 1: Affiliation Status

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text (link) | Yes | — |
| Board | Badge | Yes | CBSE / ICSE / BSEAP / BSETS / Other |
| Affiliation No. | Text | No | — |
| Granted Date | Date | Yes | — |
| Valid Until | Date | Yes | — |
| Months Remaining | Integer | Yes | Red < 6, Amber 6–12, Green > 12 |
| Status | Badge | Yes | Active / Renewal Due / Under Review / Provisional / Expired / New Application |
| Readiness | Percentage | Yes | Requirements met % |
| Conditions Pending | Integer | Yes | Post-inspection conditions |
| Last Inspection | Date | Yes | Board inspection date |
| Actions | Buttons | No | [View] [Gap Analysis] [Initiate Renewal] |

### 5.3 Tab 2: Requirements Matrix

**Board selector** (CBSE / ICSE / State Board) — loads board-specific requirements.

**Matrix view: Branch (rows) × Requirement (columns)**

Each cell: ✅ Met / 🔴 Not Met / ⚠️ Partial / ➖ N/A

**CBSE requirement categories (example):**
1. **Infrastructure:** Classroom size, playground, labs, library, computer room, sick room
2. **Staff:** Teacher-student ratio, qualified teachers (B.Ed/M.Ed), counsellor, librarian, lab attendant
3. **Safety:** Fire NOC, building stability, CCTV, first aid, emergency exits
4. **Academic:** Prescribed curriculum, NCERT books, continuous assessment, PTM records
5. **Governance:** School management committee, fee structure transparency, anti-ragging
6. **IT & Digital:** Computer lab, internet connectivity, ERP/LMS, digital records
7. **Compliance:** RTE quota (25%), POCSO compliance, CCTV data retention, AISHE/UDISE filing

### 5.4 Tab 3: Document Tracker

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Document | Text | Yes | e.g., "Fire Safety NOC" |
| Category | Badge | Yes | Infrastructure / Staff / Safety / Financial / Governance / Legal |
| Status | Badge | Yes | ✅ Uploaded (valid) / ⚠️ Expiring < 3m / 🔴 Expired / ❌ Missing |
| Upload Date | Date | Yes | — |
| Valid Until | Date | Yes | — |
| Verified By | Text | Yes | Who verified the document |
| Verification Date | Date | Yes | — |
| File | Link | No | View/download |
| Actions | Buttons | No | [Upload] [Verify] [Replace] |

**Documents required per branch (typical CBSE):**
- School recognition order
- Society/Trust registration certificate
- Land ownership/lease deed (≥ 30 years)
- Building completion certificate
- Building stability certificate (≤ 5 years old)
- Fire safety NOC (annual)
- Drinking water test report (quarterly)
- Audited balance sheet (last 3 years)
- Fee structure (approved by committee)
- Teacher qualification certificates (all teachers)
- Staff BGV certificates
- POCSO compliance certificate
- CCTV installation certificate
- IT infrastructure report
- Library stock register

### 5.5 Tab 4: Renewal Pipeline

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | — |
| Board | Badge | Yes | — |
| Expiry Date | Date | Yes | — |
| Renewal Stage | Badge | Yes | Not Started / Preparation / Application Filed / Inspection Scheduled / Inspection Done / Conditional / Renewed |
| Readiness | Percentage | Yes | Requirements + documents met |
| Gap Count | Integer | Yes | Requirements not met |
| Critical Gaps | Integer | Yes | Gaps that block renewal |
| Application Fee Paid? | Badge | Yes | ✅ / 🔴 |
| Inspection Date | Date | Yes | If scheduled |
| Assigned To | Text | Yes | Person managing this renewal |
| Actions | Buttons | No | [View] [Update Stage] [Submit Application] |

---

## 6. Drawers & Modals

### 6.1 Drawer: `affiliation-detail` (780px, right-slide)

- **Title:** "Affiliation — [Branch] · [Board] · [Affiliation No.]"
- **Tabs:** Overview · Requirements · Documents · Conditions · Inspection History · Timeline
- **Overview tab:** Board, affiliation number, dates, status, readiness %, gap summary
- **Requirements tab:** Full checklist — each requirement with status, evidence, last verified date
- **Documents tab:** All required documents with upload status, expiry, verification
- **Conditions tab:** Post-inspection conditions (if any) with deadlines, evidence submission
- **Inspection History tab:** All board inspections at this branch — dates, committees, outcomes
- **Timeline tab:** Affiliation lifecycle: original grant → renewals → inspections → conditions → current status
- **Footer:** [Gap Analysis] [Initiate Renewal] [Upload Document] [Schedule Pre-Audit (P-07)]
- **Access:** G1+ (Division P roles), Branch Principal (own branch)

### 6.2 Modal: `add-affiliation` (560px)

- **Title:** "Add Board Affiliation"
- **Fields:**
  - Branch (dropdown, required)
  - Board (dropdown): CBSE / ICSE / BSEAP / BSETS / BSEM / Other state board
  - Affiliation number (text, required)
  - Affiliation type (radio): Permanent / Provisional / Extension
  - Granted date (date)
  - Valid until (date)
  - Classes covered (multi-select): Primary (1–5) / Middle (6–8) / Secondary (9–10) / Senior Secondary (11–12)
  - Affiliation order (file upload — PDF of board's affiliation letter)
  - Notes (textarea)
- **Buttons:** Cancel · Save
- **Access:** Role 125, 121, G4+

### 6.3 Modal: `gap-analysis` (640px)

- **Title:** "Gap Analysis — [Branch] · [Board]"
- **Content:** Two-column layout:
  - Left: Requirements Met (green list with ✅)
  - Right: Requirements Not Met (red list with ❌ + remediation action + estimated cost + timeline)
- **Summary:**
  - Total requirements: N
  - Met: M (X%)
  - Not met: N−M (Y%)
  - Critical gaps (block renewal): List
  - Estimated remediation cost: ₹X
  - Estimated time to full readiness: N months
- **Buttons:** Close · Create Remediation Plan (links to P-17) · Export PDF
- **Access:** G1+ (Division P roles)

### 6.4 Modal: `upload-document` (480px)

- **Title:** "Upload Document — [Branch]"
- **Fields:**
  - Document type (dropdown from required documents list)
  - File (PDF/JPG/PNG upload, max 10MB)
  - Issue date (date)
  - Valid until (date — for time-bound documents like Fire NOC)
  - Issuing authority (text)
  - Reference number (text)
  - Notes (textarea)
- **Buttons:** Cancel · Upload
- **Post-upload:** Document status changes to "Uploaded — pending verification"
- **Access:** Role 125, 123, Branch Principal

### 6.5 Modal: `add-condition` (480px)

- **Title:** "Add Post-Inspection Condition — [Branch]"
- **Fields:**
  - Condition description (textarea, required)
  - Imposed by (text — CBSE Committee / DEO / Board)
  - Date imposed (date)
  - Deadline (date)
  - Category (dropdown): Infrastructure / Staff / Safety / Academic / Documentation / Other
  - Severity (radio): Must-fix (blocks renewal) / Should-fix / Advisory
  - Evidence required (text — what proof to submit)
- **Buttons:** Cancel · Save
- **Access:** Role 125, 121

---

## 7. Charts

### 7.1 Affiliation Status Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Affiliation Status — All Branches" |
| Data | COUNT per status: Active, Renewal Due, Under Review, Provisional, Expired |
| Colours | Active: green, Renewal Due: amber, Under Review: blue, Provisional: orange, Expired: red |
| Centre text | N affiliations |
| API | `GET /api/v1/group/{id}/audit/affiliation/analytics/status-distribution/` |

### 7.2 Readiness Heatmap (Matrix)

| Property | Value |
|---|---|
| Chart type | Heatmap matrix |
| Title | "Affiliation Readiness — Branch × Requirement Category" |
| X-axis | Requirement categories (Infrastructure, Staff, Safety, Academic, Governance, IT, Compliance) |
| Y-axis | Branches |
| Cell colour | Green ≥ 90%, Amber 70–89%, Red < 70% |
| API | `GET /api/v1/group/{id}/audit/affiliation/analytics/readiness-heatmap/` |

### 7.3 Renewal Timeline (Gantt)

| Property | Value |
|---|---|
| Chart type | Horizontal timeline bars |
| Title | "Affiliation Renewal Timeline — Next 36 Months" |
| Data | Per branch: current affiliation end date → renewal target |
| Colour | Green (> 12m), Amber (6–12m), Red (< 6m), Black (expired) |
| API | `GET /api/v1/group/{id}/audit/affiliation/analytics/renewal-timeline/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Affiliation added | "Affiliation added — [Branch], [Board]" | Success | 3s |
| Document uploaded | "Document '[Name]' uploaded for [Branch]" | Success | 3s |
| Document verified | "Document '[Name]' verified" | Success | 3s |
| Condition added | "Post-inspection condition added — deadline: [Date]" | Success | 3s |
| Condition fulfilled | "Condition fulfilled — evidence submitted" | Success | 3s |
| Renewal initiated | "Renewal process initiated for [Branch]" | Info | 3s |
| Affiliation expiry alert | "⚠️ [Branch] affiliation expires in [N] months — readiness: [X]%" | Warning | 6s |
| Affiliation expired | "🔴 [Branch] affiliation EXPIRED — immediate action required" | Error | 8s |
| Document expiring | "⚠️ [Document] at [Branch] expires in [N] days" | Warning | 5s |
| Condition overdue | "🔴 Post-inspection condition overdue at [Branch]" | Error | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No affiliations | 🏫 | "No Affiliations Tracked" | "Add your branches' board affiliations to begin compliance tracking." | Add Affiliation |
| No documents | 📄 | "No Documents Uploaded" | "Upload affiliation documents to track readiness." | Upload Document |
| No renewals due | ✅ | "No Renewals Due" | "All affiliations are valid for more than 12 months." | — |
| No conditions | ✅ | "No Pending Conditions" | "No post-inspection conditions outstanding." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + table skeleton |
| Requirements matrix | Matrix skeleton with coloured cells |
| Document tracker | Table skeleton with badge cells |
| Affiliation detail drawer | 780px skeleton: 6 tabs |
| Gap analysis | Two-column skeleton |
| Chart load | Grey canvas placeholder |
| Renewal pipeline | Pipeline stage skeleton |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/affiliation/` | G1+ | List all affiliations |
| GET | `/api/v1/group/{id}/audit/affiliation/kpis/` | G1+ | KPI values |
| POST | `/api/v1/group/{id}/audit/affiliation/` | 125, 121, G4+ | Add affiliation |
| GET | `/api/v1/group/{id}/audit/affiliation/{aff_id}/` | G1+ | Affiliation detail |
| PUT | `/api/v1/group/{id}/audit/affiliation/{aff_id}/` | 125, 121 | Update affiliation |
| GET | `/api/v1/group/{id}/audit/affiliation/{aff_id}/requirements/` | G1+ | Requirements matrix |
| PATCH | `/api/v1/group/{id}/audit/affiliation/{aff_id}/requirements/{req_id}/` | 125, 123 | Update requirement status |
| GET | `/api/v1/group/{id}/audit/affiliation/{aff_id}/documents/` | G1+ | Documents list |
| POST | `/api/v1/group/{id}/audit/affiliation/{aff_id}/documents/` | 125, 123, Branch Principal | Upload document |
| PATCH | `/api/v1/group/{id}/audit/affiliation/{aff_id}/documents/{doc_id}/verify/` | 125, 121 | Verify document |
| GET | `/api/v1/group/{id}/audit/affiliation/{aff_id}/conditions/` | G1+ | Post-inspection conditions |
| POST | `/api/v1/group/{id}/audit/affiliation/{aff_id}/conditions/` | 125, 121 | Add condition |
| PATCH | `/api/v1/group/{id}/audit/affiliation/{aff_id}/conditions/{cond_id}/fulfil/` | 125, 123 | Mark fulfilled |
| GET | `/api/v1/group/{id}/audit/affiliation/{aff_id}/gap-analysis/` | G1+ | Gap analysis |
| GET | `/api/v1/group/{id}/audit/affiliation/renewals/` | G1+ | Renewal pipeline |
| PATCH | `/api/v1/group/{id}/audit/affiliation/{aff_id}/renewal-stage/` | 125, 121 | Update renewal stage |
| GET | `/api/v1/group/{id}/audit/affiliation/analytics/status-distribution/` | G1+ | Status donut |
| GET | `/api/v1/group/{id}/audit/affiliation/analytics/readiness-heatmap/` | G1+ | Readiness heatmap |
| GET | `/api/v1/group/{id}/audit/affiliation/analytics/renewal-timeline/` | G1+ | Renewal timeline |
| GET | `/api/v1/group/{id}/audit/affiliation/export/` | G1+ | Export data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../affiliation/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#affiliation-content` | `innerHTML` | `hx-trigger="click"` |
| Affiliation detail drawer | Row click | `hx-get=".../affiliation/{id}/"` | `#right-drawer` | `innerHTML` | 780px drawer |
| Add affiliation | Form submit | `hx-post=".../affiliation/"` | `#add-result` | `innerHTML` | Toast |
| Upload document | Form submit | `hx-post=".../affiliation/{id}/documents/"` | `#doc-result` | `innerHTML` | Toast + table refresh |
| Verify document | Button click | `hx-patch=".../documents/{id}/verify/"` | `#doc-{id}-status` | `innerHTML` | Inline badge update |
| Update requirement | Select change | `hx-patch=".../requirements/{id}/"` | `#req-{id}-status` | `innerHTML` | Inline cell update |
| Gap analysis | Button click | `hx-get=".../affiliation/{id}/gap-analysis/"` | `#gap-modal` | `innerHTML` | Opens modal |
| Board selector (Tab 2) | Radio change | `hx-get=".../requirements/?board={board}"` | `#requirements-matrix` | `innerHTML` | Loads board-specific matrix |
| Renewal stage update | Select change | `hx-patch=".../affiliation/{id}/renewal-stage/"` | `#stage-badge` | `innerHTML` | Toast |
| Chart load | Tab shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |
| Pagination | Page click | `hx-get` with page param | `#table-body` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
