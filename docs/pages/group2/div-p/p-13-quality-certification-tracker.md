# P-13 — Quality Certification (ISO/NAAC) Tracker

> **URL:** `/group/audit/certifications/`
> **File:** `p-13-quality-certification-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group ISO / NAAC Coordinator (Role 124, G1) — primary operator

---

## 1. Purpose

The Quality Certification Tracker manages the entire lifecycle of voluntary and mandatory quality certifications for institutions within the group — ISO 9001:2015 (Quality Management System), NAAC (National Assessment and Accreditation Council for colleges), QCI (Quality Council of India), NABET (National Accreditation Board for Education and Training), and state-specific quality awards. In Indian higher education, NAAC accreditation is no longer optional — UGC mandates it for colleges seeking government grants, fee autonomy, and certain affiliations. For schools, ISO 9001 certification and NABET accreditation signal quality to parents and regulators.

The problems this page solves:

1. **Certification lifecycle complexity:** NAAC accreditation is a 12–18 month process: institutional data submission via IIQA (Institutional Information for Quality Assessment), Self-Study Report (SSR) preparation covering 7 criteria and 34 key indicators, data validation and verification (DVV), peer team visit (2–3 days), grading (A++, A+, A, B++, B+, B, C), and validity for 5 years. Managing this across 5–20 colleges in a group — each at a different stage — is impossible without a central tracker.

2. **Multiple certification standards, different requirements:** ISO 9001 has different clauses (10 clauses, 306 requirements). NAAC has 7 criteria with different weights for affiliated vs autonomous colleges. NABET has its own 7 domains. A group pursuing multiple certifications per institution needs a unified view of where each institution stands.

3. **Self-assessment gap analysis:** Before applying for NAAC or ISO, institutions must honestly assess where they stand. The SSR requires quantitative metrics: student-teacher ratio, PhD-qualified faculty percentage, research publications per faculty, placement rate, ICT-enabled classrooms, library books per student, and dozens more. The tracker maintains these metrics, computes readiness, and highlights gaps requiring remediation before the assessment team visits.

4. **Document and evidence management:** NAAC SSR requires extensive evidence — policy documents, meeting minutes, audit reports, student feedback analysis, faculty development records, placement data, financial statements. The tracker links each criterion to its required evidence with upload, versioning, and completeness tracking.

5. **Renewal and re-accreditation planning:** NAAC grade validity is 5 years. ISO 9001 certification requires annual surveillance audits and re-certification every 3 years. A group with 15 colleges has 3 NAAC renewals per year. The tracker shows upcoming renewals, preparation timelines, and ensures the 12-month preparation window is respected.

**Scale:** 5–50 institutions · 3–5 certification types · 12–18 month certification cycles · 5-year renewal periods · 7 NAAC criteria × 34 key indicators per institution · 10 ISO clauses × 306 requirements

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group ISO / NAAC Coordinator | 124 | G1 | Full — manage certifications, track criteria, upload evidence | Primary operator |
| Group Internal Audit Head | 121 | G1 | Read — certification status feeds compliance scorecard | Cross-functional |
| Group Affiliation Compliance Officer | 125 | G1 | Read — cross-reference certifications with affiliation | Coordination |
| Group Academic Quality Officer | 122 | G1 | Read + Contribute — academic data for NAAC criteria | Subject matter |
| Group Compliance Data Analyst | 127 | G1 | Read — certification metrics for MIS reports | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read + CAPA — drives gap closure | Remediation |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — certification applications, budgets | Final authority |
| College Principal / Director | — | G3 | Read (own institution) + Upload evidence | Institution-level owner |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. College Principals see only their own institution. Evidence upload: 124, 122, College Principal. Application decisions: G4/G5.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Quality Certifications
```

### 3.2 Page Header
```
Quality Certification Tracker                    [+ Add Certification]  [Gap Analysis]  [Export]
ISO / NAAC Coordinator — Dr. V. Subramaniam
Sunrise Education Group · 8 colleges · 22 schools · NAAC: 5 active · ISO 9001: 3 active · 2 renewals due this year
```

### 3.3 Filter Bar
```
Institution: [All / Select ▼]    Certification: [All / NAAC / ISO 9001 / NABET / QCI / State Award ▼]
Stage: [All / Planning / Self-Assessment / Applied / Under Review / Certified / Renewal Due ▼]
Grade: [All / A++ / A+ / A / B++ / B+ / B / C / Not Graded ▼]
[Search by institution name]                                                    [Reset Filters]
```

### 3.4 KPI Summary Bar

| # | KPI | Source | Colour Logic |
|---|---|---|---|
| 1 | Active Certifications | Count of valid certifications | Neutral blue |
| 2 | NAAC Accredited | Count of NAAC-accredited institutions | All institutions done = green · else amber |
| 3 | ISO Certified | Count of ISO 9001 certified | Neutral blue |
| 4 | Renewals Due (12 months) | Certifications expiring within 1 year | 0 green · 1–2 amber · > 2 red |
| 5 | In Progress | Applications/assessments underway | Neutral blue |
| 6 | Average NAAC Grade | Average CGPA across accredited colleges | ≥ 3.0 green · 2.5–2.9 amber · < 2.5 red |
| 7 | Gap Items Open | Open gaps from self-assessment | 0 green · 1–20 amber · > 20 red |
| 8 | Evidence Completeness | % of required evidence uploaded | ≥ 95% green · 80–94% amber · < 80% red |

### 3.5 Tab Navigation

```
[Certification Portfolio]    [NAAC Manager]    [ISO 9001 Manager]    [Renewal Pipeline]
```

---

### Tab 1 — Certification Portfolio (default)

Overview of all certifications across all institutions. One row per institution × certification combination.

**Table columns:**

| # | Column | Width | Content |
|---|---|---|---|
| 1 | Institution | 180px | College/school name + code |
| 2 | Type | 80px | K–12 / College / University |
| 3 | Certification | 100px | NAAC / ISO 9001 / NABET / QCI |
| 4 | Current Grade/Status | 100px | NAAC: A++/A+/A/B++/B+/B/C · ISO: Certified/Not · Badge colours |
| 5 | CGPA (NAAC) | 70px | e.g., 3.42 — only for NAAC |
| 6 | Valid From | 90px | dd-MMM-yyyy |
| 7 | Valid Until | 90px | dd-MMM-yyyy · red if < 12 months |
| 8 | Stage | 120px | Pipeline badge: Planning → Self-Assessment → Applied → Peer Visit → Graded → Certified |
| 9 | Readiness % | 80px | Self-assessment readiness percentage |
| 10 | Open Gaps | 60px | Count of gap items needing remediation |
| 11 | Actions | 80px | [View] · [Timeline] |

**Row click:** Opens Certification Detail Drawer.

**Summary row (bottom):**
```
Total: 30 institutions · 18 certifications active · 8 in progress · 4 not started · Average NAAC CGPA: 3.12
```

---

### Tab 2 — NAAC Manager

Dedicated view for NAAC accreditation — the most complex certification. Shows all institutions' NAAC status with criterion-level detail.

**Sub-section A — Institution NAAC Status Cards:**

Card grid (1 card per institution with NAAC accreditation active or in progress):

```
┌─────────────────────────────────────────────────┐
│ Sunrise College of Engineering, Hyderabad       │
│ Grade: A+ (3.42 CGPA)   Valid: 15-Mar-2024 to 14-Mar-2029  │
│ Cycle: 2nd   Stage: ✅ Certified                │
│ Renewal in: 1,085 days                          │
│ [View SSR]  [Criterion Scores]  [Evidence]       │
└─────────────────────────────────────────────────┘
```

**Sub-section B — Criterion-wise Performance (expandable per institution):**

When institution card is expanded, shows NAAC's 7 criteria:

| # | Criterion | Weight | Institution Score | Group Avg | Key Indicators |
|---|---|---|---|---|---|
| 1 | Curricular Aspects | 150 | 132 (88%) | 125 (83%) | 8 KIs |
| 2 | Teaching-Learning & Evaluation | 200 | 178 (89%) | 165 (83%) | 10 KIs |
| 3 | Research, Innovations & Extension | 150 | 98 (65%) | 105 (70%) | 7 KIs |
| 4 | Infrastructure & Learning Resources | 100 | 92 (92%) | 88 (88%) | 4 KIs |
| 5 | Student Support & Progression | 100 | 85 (85%) | 82 (82%) | 5 KIs |
| 6 | Governance, Leadership & Management | 100 | 88 (88%) | 84 (84%) | 5 KIs |
| 7 | Institutional Values & Best Practices | 100 | 75 (75%) | 78 (78%) | 5 KIs |
| | **Total** | **1000** | **748 (3.42 CGPA)** | **727 (3.12 CGPA)** | **44 KIs** |

**Click on criterion row → expands to show Key Indicators (KIs)** with score, evidence status, and gap items.

**Sub-section C — NAAC Application Pipeline:**

Kanban-style horizontal pipeline for institutions currently in the NAAC process:

```
[IIQA Submitted] → [SSR Draft] → [SSR Submitted] → [DVV Complete] → [Peer Visit Scheduled] → [Peer Visit Done] → [Grade Received]
```

Each card in the pipeline shows institution name, days in current stage, and blockers.

---

### Tab 3 — ISO 9001 Manager

Dedicated view for ISO 9001:2015 certification. Shows clause-level compliance.

**Sub-section A — ISO Status Cards:**

Similar card grid as NAAC but for ISO-certified institutions.

```
┌─────────────────────────────────────────────────┐
│ Sunrise International School, Gachibowli        │
│ ISO 9001:2015 Certified   Cert#: QS-2024-IN-4523│
│ CB: Bureau Veritas   Valid: 01-Jul-2024 to 30-Jun-2027│
│ Next Surveillance: Sep-2025 (6 months away)      │
│ [View Certificate]  [Clause Compliance]  [Audit Schedule]│
└─────────────────────────────────────────────────┘
```

**Sub-section B — Clause Compliance Matrix:**

| Clause | Title | Sub-clauses | Compliant | Partially | Non-Compliant | Evidence |
|---|---|---|---|---|---|---|
| 4 | Context of the Organization | 4 | 4 | 0 | 0 | ✅ Complete |
| 5 | Leadership | 3 | 3 | 0 | 0 | ✅ Complete |
| 6 | Planning | 3 | 2 | 1 | 0 | ⚠️ 1 gap |
| 7 | Support | 5 | 4 | 1 | 0 | ⚠️ 1 gap |
| 8 | Operation | 7 | 5 | 1 | 1 | ❌ 2 gaps |
| 9 | Performance Evaluation | 3 | 3 | 0 | 0 | ✅ Complete |
| 10 | Improvement | 3 | 2 | 1 | 0 | ⚠️ 1 gap |

**Click on clause → expands to show sub-clauses** with compliance status, evidence links, and CAPA items.

**Sub-section C — Surveillance Audit Schedule:**

| Institution | Certification Body | Last Audit | Next Audit | Days Until | Readiness |
|---|---|---|---|---|---|
| Sunrise Intl Gachibowli | Bureau Veritas | 15-Sep-2024 | 15-Sep-2025 | 173 | 78% |
| Sunrise Intl Kondapur | TÜV SÜD | 01-Dec-2024 | 01-Dec-2025 | 250 | 65% |

---

### Tab 4 — Renewal Pipeline

Shows all certifications approaching renewal with preparation tracking.

**Pipeline table:**

| # | Column | Content |
|---|---|---|
| 1 | Institution | Name + type |
| 2 | Certification | NAAC / ISO 9001 / NABET |
| 3 | Current Grade | Current status/grade |
| 4 | Expiry Date | Certification end date |
| 5 | Days Remaining | Countdown with colour |
| 6 | Preparation Stage | Not Started → Planning → Self-Assessment → Applied → Under Review |
| 7 | Readiness % | Based on evidence and gap closure |
| 8 | Open Gaps | Count of items to fix |
| 9 | Budget Required | Estimated cost for renewal (application fee + consultant + remediation) |
| 10 | Assigned To | Who is managing this renewal |
| 11 | Actions | [View Plan] · [Timeline] |

**Auto-alerts:**
- 18 months before NAAC expiry → "Start SSR preparation"
- 12 months before ISO re-certification → "Begin internal audit"
- 6 months before → "Application must be submitted"
- 3 months before → "Critical — escalate to CEO if not applied"

---

## 4. KPI Summary Bar

(Defined in Section 3.4 above)

---

## 5. Sections

| # | Section | Location | Purpose |
|---|---|---|---|
| 1 | Certification Portfolio | Tab 1 | All certifications across all institutions |
| 2 | NAAC Manager | Tab 2 | NAAC-specific criterion and pipeline management |
| 3 | ISO 9001 Manager | Tab 3 | ISO clause compliance and surveillance schedule |
| 4 | Renewal Pipeline | Tab 4 | Upcoming renewals with preparation tracking |
| 5 | Certification Detail Drawer | Right drawer | Full certification view with criteria and evidence |
| 6 | Add Certification Modal | Modal | Register new certification for an institution |
| 7 | Gap Analysis Modal | Modal | Self-assessment readiness and gaps |
| 8 | Evidence Upload Panel | Within drawer | Upload evidence for criteria/clauses |

---

## 6. Drawers & Modals

### Drawer 1 — Certification Detail Drawer (right, 780px)

**Trigger:** Click any certification row in Tab 1 or institution card in Tab 2/3.

**Header:**
```
Certification Detail — NAAC Accreditation                      [✕]
Sunrise College of Engineering, Hyderabad · Grade A+ (3.42 CGPA) · Valid until 14-Mar-2029
```

**Sections within drawer:**

**Section A — Overview**

| Field | Value |
|---|---|
| Certification | NAAC (National Assessment and Accreditation Council) |
| Cycle | 2nd Cycle |
| Grade | A+ |
| CGPA | 3.42 / 4.00 |
| Valid From | 15-Mar-2024 |
| Valid Until | 14-Mar-2029 |
| Application Date | 10-Sep-2023 |
| Peer Visit Date | 05-Feb-2024 – 07-Feb-2024 |
| Team Chair | Prof. R.K. Sharma, IIT Delhi |
| Certificate Number | NAAC/HE/2024/A+/HYD/0087 |

**Section B — Criterion Scores (NAAC) / Clause Compliance (ISO)**
- Expandable accordion for each criterion/clause
- Each item shows: score, evidence count, gap count
- Click to view Key Indicators or sub-clauses

**Section C — Evidence Repository**
- List of all uploaded evidence documents per criterion
- Status: ✅ Uploaded · ❌ Missing · ⚠️ Outdated
- `[Upload]` button per item

**Section D — Timeline / History**
- Vertical timeline of all events: application, SSR submission, DVV queries, peer visit, grade announcement
- Each event shows date, description, linked documents

**Section E — Actions**
```
[Edit Details]  [Download Certificate]  [Start Renewal Process]  [View SSR]
```

---

### Modal 1 — Add Certification

**Trigger:** `[+ Add Certification]` button.

**Form fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Institution | Dropdown (searchable) | Yes | College/school name |
| Certification Type | Dropdown | Yes | NAAC / ISO 9001:2015 / NABET / QCI / State Award / Other |
| Certification Body | Text / Dropdown | Conditional | NAAC: auto-filled. ISO: Bureau Veritas, TÜV SÜD, BSI, DNV, etc. |
| Cycle / Version | Number | No | 1st / 2nd / 3rd cycle for NAAC; 2015 for ISO |
| Application Date | Date picker | No | When application was/will be submitted |
| Target Grade | Dropdown | No | For NAAC: A++ / A+ / A / B++ etc. For ISO: Certified |
| Current Stage | Dropdown | Yes | Planning → Self-Assessment → Applied → Under Review → Certified |
| Assigned Coordinator | Dropdown | Yes | Person responsible from 124 or institution |
| Budget Allocated | Currency (₹) | No | Total budget for this certification |
| Notes | Textarea | No | Context |

**Actions:** `[Add Certification]` `[Cancel]`

---

### Modal 2 — Gap Analysis

**Trigger:** `[Gap Analysis]` button from header or certification drawer.

**Content:**

For NAAC: Shows all 7 criteria × 34 Key Indicators with:
- Current data/score (from self-assessment)
- Required benchmark
- Gap (deficit)
- Remediation action needed
- Estimated cost
- Estimated time

For ISO: Shows all 10 clauses × sub-requirements with compliance status.

**Summary panel at top:**
```
Overall Readiness: 72%
Critical Gaps: 4 (must fix before applying)
Major Gaps: 8 (should fix for higher grade)
Minor Gaps: 12 (nice to have)
Estimated Remediation Cost: ₹18.5L
Estimated Remediation Time: 8 months
```

**Actions:** `[Export Gap Report (PDF)]` `[Create CAPA Items for All Gaps]` `[Close]`

---

### Modal 3 — Evidence Upload

**Trigger:** `[Upload]` button from evidence list in drawer.

**Form fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Criterion / Clause | Pre-filled | Yes | From context |
| Key Indicator | Pre-filled | Yes | From context |
| Evidence Title | Text | Yes | e.g., "Faculty Qualification Matrix 2024-25" |
| Evidence Type | Dropdown | Yes | Document / Data Sheet / Photo / Video Link / External URL |
| File Upload | Drag-drop | Conditional | If document/photo; Max 10 MB |
| External URL | URL field | Conditional | If video link or external URL |
| Description | Textarea | No | Context for the evidence |

**Actions:** `[Upload Evidence]` `[Cancel]`

---

### Modal 4 — Start Renewal Process

**Trigger:** `[Start Renewal Process]` from drawer.

**Content:** Wizard (3 steps):

**Step 1 — Renewal Details:**
- Certification (pre-filled)
- Target grade (if applicable)
- Planned application date
- Assigned coordinator
- Budget allocation

**Step 2 — Preparation Timeline:**
- Auto-generated milestone timeline based on certification type:
  - NAAC: IIQA → SSR preparation (6 months) → SSR submission → DVV → Peer Visit → Grading
  - ISO: Internal audit → Management review → Application → Stage 1 → Stage 2 → Certification
- Each milestone has a target date (editable)

**Step 3 — Gap Assessment:**
- Quick self-assessment checklist
- Identifies major gaps from previous cycle
- Creates CAPA items for each gap

**Actions:** `[Initiate Renewal]` `[Save Draft]` `[Cancel]`

---

## 7. Charts

### Chart 1 — NAAC Grade Distribution (horizontal bar)
- **Type:** Horizontal bar chart (Chart.js 4.x)
- **X-axis:** Count of institutions
- **Y-axis:** Grade bands (A++, A+, A, B++, B+, B, C, Not Accredited)
- **Colour:** Gradient — A++ dark green → C red → Not Accredited grey
- **Purpose:** Shows group's NAAC grade profile at a glance
- **Location:** Tab 2 header
- **API:** `GET /api/v1/group/{id}/audit/certifications/charts/naac-grade-distribution/`

### Chart 2 — Certification Readiness Radar (radar)
- **Type:** Radar chart (Chart.js 4.x)
- **Axes:** 7 NAAC criteria (or 10 ISO clauses)
- **Series:** Selected institution (solid) vs Group average (dashed) vs Target (dotted at 100%)
- **Purpose:** Visual gap identification — which criteria are weakest
- **Location:** Tab 2, within institution expansion
- **API:** `GET /api/v1/group/{id}/audit/certifications/charts/readiness-radar/?institution={id}&type={naac|iso}`

### Chart 3 — Renewal Timeline (Gantt-style horizontal bar)
- **Type:** Horizontal bar/timeline chart (Chart.js 4.x with custom plugin)
- **X-axis:** Timeline (months, next 3 years)
- **Y-axis:** Institutions
- **Bars:** Current certification validity period (green) → Renewal preparation period (amber) → Application window (blue)
- **Markers:** Expiry dates (red diamonds), application deadlines (blue triangles)
- **Purpose:** Shows when each certification expires and when preparation must start
- **Location:** Tab 4 header
- **API:** `GET /api/v1/group/{id}/audit/certifications/charts/renewal-timeline/`

### Chart 4 — Evidence Completeness by Criterion (stacked bar)
- **Type:** Stacked bar chart (Chart.js 4.x)
- **X-axis:** Criteria / Clauses
- **Y-axis:** Evidence count
- **Stacks:** Uploaded (green), Missing (red), Outdated (amber)
- **Purpose:** Shows evidence gaps per criterion for active certification efforts
- **Location:** Within certification detail drawer
- **API:** `GET /api/v1/group/{id}/audit/certifications/charts/evidence-completeness/?certification_id={id}`

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Certification added | "NAAC accreditation added for Sunrise College of Engineering — stage: Planning" | Success (green) |
| Certification updated | "NAAC details updated — grade changed to A+ (3.42 CGPA)" | Success (green) |
| Evidence uploaded | "Faculty Qualification Matrix uploaded for Criterion 2 — 28/34 KIs now have evidence" | Success (green) |
| Gap analysis generated | "Gap analysis complete — 4 critical, 8 major, 12 minor gaps identified" | Info (blue) |
| CAPA items created from gaps | "24 CAPA items created from gap analysis — assigned to Process Improvement Coordinator" | Success (green) |
| Renewal process initiated | "NAAC 3rd cycle renewal initiated for Sunrise Engineering — target: A++ by Mar-2030" | Success (green) |
| Stage updated | "Sunrise Engineering moved to 'SSR Submitted' stage" | Info (blue) |
| Renewal alert | "2 certifications expiring within 12 months — preparation required" | Warning (amber) |
| Surveillance audit due | "ISO 9001 surveillance audit for Sunrise Intl Gachibowli due in 30 days" | Warning (amber) |
| Evidence missing | "Criterion 3 (Research): 5 of 7 KIs still missing evidence" | Warning (amber) |
| Budget exceeded | "ISO certification budget for Sunrise Intl exceeded by ₹1.2L — approval needed" | Warning (amber) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No certifications added | Certificate with dotted outline | "No quality certifications tracked yet. Add your institutions' NAAC, ISO, or other certifications to start tracking." | `[+ Add First Certification]` |
| No NAAC institutions (Tab 2) | NAAC logo greyed out | "No institutions with NAAC accreditation or in the NAAC pipeline. Add a NAAC certification to get started." | `[+ Add NAAC Certification]` |
| No ISO institutions (Tab 3) | ISO badge greyed out | "No institutions with ISO 9001 certification. Add an ISO certification to start tracking clause compliance." | `[+ Add ISO Certification]` |
| No renewals due (Tab 4) | Calendar with green checkmark | "No certifications due for renewal in the next 18 months. All certifications are current." | — (positive state) |
| No evidence for criterion | Empty document stack | "No evidence uploaded for this criterion yet. Upload documents, data sheets, or photo evidence." | `[Upload Evidence]` |
| Gap analysis — no gaps | Trophy icon | "No gaps found — this institution meets all criteria for the target grade. Ready to apply!" | `[Submit Application]` |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Page initial load | Skeleton: KPI cards + table rows | < 1s |
| KPI bar | 8 grey pulse cards → populated | < 500ms |
| Certification portfolio table | 10 skeleton rows → data | < 1s |
| NAAC criterion expansion | Inline spinner → criterion data | < 500ms |
| ISO clause expansion | Inline spinner → clause data | < 500ms |
| Gap analysis computation | Modal with progress bar: "Analysing 34 Key Indicators…" | 2–5s |
| Evidence upload | Progress bar per file | 1–5s per file |
| Renewal pipeline | Gantt chart skeleton → rendered | < 1.5s |
| Chart rendering | Grey chart placeholder → Chart.js render | < 500ms |
| SSR export | Spinner + "Generating Self-Study Report (87 pages)…" | 10–30s |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/certifications/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | List all certifications (filterable) | G1+ |
| 2 | GET | `/{cert_id}/` | Certification detail | G1+ |
| 3 | POST | `/` | Add new certification | 124, G4+ |
| 4 | PATCH | `/{cert_id}/` | Update certification details | 124 |
| 5 | DELETE | `/{cert_id}/` | Archive certification (soft delete) | G4+ |
| 6 | GET | `/{cert_id}/criteria/` | List criteria/clauses with scores | G1+ |
| 7 | GET | `/{cert_id}/criteria/{criterion_id}/` | Criterion detail with KIs | G1+ |
| 8 | PATCH | `/{cert_id}/criteria/{criterion_id}/` | Update criterion score/status | 124 |
| 9 | GET | `/{cert_id}/evidence/` | List all evidence for certification | G1+ |
| 10 | POST | `/{cert_id}/evidence/` | Upload evidence for a criterion | 124, 122, College Principal |
| 11 | GET | `/{cert_id}/evidence/{evidence_id}/download/` | Download evidence file | G1+ |
| 12 | DELETE | `/{cert_id}/evidence/{evidence_id}/` | Remove evidence | 124 |
| 13 | GET | `/{cert_id}/gap-analysis/` | Run gap analysis and return results | G1+ |
| 14 | POST | `/{cert_id}/gap-analysis/capa/` | Create CAPA items from gap analysis | 124, 128 |
| 15 | GET | `/{cert_id}/timeline/` | Certification lifecycle timeline | G1+ |
| 16 | POST | `/{cert_id}/renewal/` | Initiate renewal process | 124, G4+ |
| 17 | PATCH | `/{cert_id}/stage/` | Update certification stage | 124 |
| 18 | GET | `/renewal-pipeline/` | All certifications due for renewal | G1+ |
| 19 | GET | `/naac/grade-distribution/` | NAAC grade distribution across group | G1+ |
| 20 | GET | `/charts/naac-grade-distribution/` | Chart 1 data | G1+ |
| 21 | GET | `/charts/readiness-radar/` | Chart 2 data (per institution) | G1+ |
| 22 | GET | `/charts/renewal-timeline/` | Chart 3 data | G1+ |
| 23 | GET | `/charts/evidence-completeness/` | Chart 4 data (per certification) | G1+ |
| 24 | GET | `/kpis/` | KPI bar aggregates | G1+ |
| 25 | GET | `/export/` | Export certifications as Excel | G1+ |
| 26 | GET | `/{cert_id}/ssr-export/` | Export Self-Study Report as PDF | G1+ |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../certifications/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#cert-content` | `innerHTML` | `hx-trigger="click"` |
| Certification table | Tab 1 load | `hx-get=".../certifications/?page=1"` | `#cert-table-body` | `innerHTML` | Paginated |
| Filter change | Select/input change | `hx-get=".../certifications/?type={}&stage={}"` | `#cert-table-body` | `innerHTML` | `hx-trigger="change"` debounced |
| Certification detail drawer | Row click | `hx-get=".../certifications/{id}/"` | `#right-drawer` | `innerHTML` | 780px drawer |
| Criterion expand | Row click (Tab 2/3) | `hx-get=".../certifications/{id}/criteria/{cid}/"` | `#criterion-{cid}` | `innerHTML` | Accordion expand |
| Add certification | Form submit | `hx-post=".../certifications/"` | `#add-result` | `innerHTML` | Toast + table refresh |
| Update stage | Select change | `hx-patch=".../certifications/{id}/stage/"` | `#stage-badge-{id}` | `innerHTML` | Inline badge update |
| Evidence upload | Form submit | `hx-post=".../certifications/{id}/evidence/"` | `#evidence-list` | `innerHTML` | Toast + list refresh |
| Gap analysis | Button click | `hx-get=".../certifications/{id}/gap-analysis/"` | `#gap-modal` | `innerHTML` | Opens modal with results |
| Create CAPA from gaps | Button click | `hx-post=".../certifications/{id}/gap-analysis/capa/"` | `#capa-result` | `innerHTML` | Toast |
| Renewal pipeline | Tab 4 load | `hx-get=".../certifications/renewal-pipeline/"` | `#renewal-content` | `innerHTML` | — |
| Initiate renewal | Form submit | `hx-post=".../certifications/{id}/renewal/"` | `#renewal-result` | `innerHTML` | Toast + pipeline refresh |
| Chart load | Tab/section shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |
| Pagination | Page click | `hx-get` with page param | `#cert-table-body` | `innerHTML` | — |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
