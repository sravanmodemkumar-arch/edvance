# P-19 — Complaint Pattern Analyzer

> **URL:** `/group/audit/grievances/patterns/`
> **File:** `p-19-complaint-pattern-analyzer.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Grievance Audit Officer (Role 126, G1) — primary operator

---

## 1. Purpose

The Complaint Pattern Analyzer is the analytical intelligence layer of the grievance audit function. While P-18 provides the operational dashboard — open complaints, SLA status, acknowledgements — this page answers the deeper strategic question: what is the system telling us? Patterns in grievance data reveal systemic failures that no individual complaint captures. A single complaint about homework overload is a signal; 87 complaints about homework overload across 12 branches in the same academic month is a curriculum policy failure that needs group-level intervention, not branch-level counselling.

This page is used by the Grievance Audit Officer to build the quarterly pattern analysis report submitted to the CEO and Board — a document that identifies the top 5–10 systemic issues affecting student experience, parent satisfaction, and institutional risk across the group, with evidence, root cause hypothesis, and recommended interventions.

The problems this page solves:

1. **Complaint data is rich but unread:** Operational grievance systems close individual complaints. No one reads across them to find the pattern. This analyzer does that automatically — clustering complaints by category, keyword, branch type, time of year, and teacher/staff involvement.

2. **Seasonal patterns ignored:** Fee-related complaints spike every April (new academic year fee hike), June (late fee penalties), and October (half-yearly fee deadlines). Academic quality complaints spike November–December (board exam pressure). Safety complaints spike during monsoon (infrastructure failures). These seasonal patterns are predictable and preventable if the pattern is identified and acted on before the season arrives.

3. **Staff-specific complaint patterns hidden:** When the same staff member's conduct generates complaints at every branch they've worked at (coaching institutes transfer staff across branches regularly), the pattern is a staff problem, not a branch problem. The analyzer can surface staff-linked patterns (name masked in display — identified only by staff ID to HR separately).

4. **Branch-type-specific vulnerabilities:** Coaching institutes have different complaint profiles than residential schools. Residential schools have different profiles than day schools. Pattern analysis by institution type allows targeted policy interventions — e.g., hostels consistently generating food quality complaints need a hostel food policy review, not individual-branch CAPAs.

5. **Complaint language clustering:** Even when complaint categories are properly tagged, the free-text description of complaints contains additional signal. Keyword frequency analysis identifies issues that don't fit neatly into predefined categories — e.g., sudden spike in the word "unsafe" or "threatening" in complaint descriptions signals something that a category dropdown couldn't capture.

6. **Intervention effectiveness measurement:** After a group-level policy change (e.g., a new homework policy in response to complaint patterns), does the complaint volume in that category actually drop? Pre/post comparison measures whether interventions worked.

**Scale:** 5–50 branches · 200–1,000 complaints/year · 8 categories · 12 months rolling window · Keyword corpus: 500–5,000 free-text entries per year

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Grievance Audit Officer | 126 | G1 | Full — all analytics, pattern reports, intervention tracking | Primary operator |
| Group Internal Audit Head | 121 | G1 | Read — pattern reports and recommended interventions | Strategic oversight |
| Group Compliance Data Analyst | 127 | G1 | Read — pattern data for MIS | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read + Create CAPAs from patterns | Remediation |
| Group CEO / Chairman | — | G4/G5 | Read — executive summary and pattern reports | Strategic |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. All complaint data is identity-masked. Staff-linked patterns display staff ID only — branch HR resolves to name internally. No complainant identity exposed at any point.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Grievance Audit  ›  Pattern Analyzer
```

### 3.2 Page Header
```
Complaint Pattern Analyzer                      [Generate Pattern Report]  [Export]
Grievance Audit Officer — M. Srinivas
Sunrise Education Group · Analysis period: Apr 2025 – Mar 2026 · 847 complaints analysed
```

### 3.3 Filter Bar
```
Period: [This FY ▼]  [Custom: From ___ To ___]
Branch: [All / Select ▼]    Institution Type: [All / School / Coaching / Hostel / College ▼]
Category: [All / Academic / Fee / Safety / POCSO / Harassment / Infrastructure / Staff Conduct / Other ▼]
Severity: [All / Critical / High / Medium / Low ▼]    Zone: [All / Zone 1 / Zone 2 / Zone 3 ▼]
                                                                        [Analyse]
```

`[Analyse]` button triggers a fresh pattern computation — results update all sections below.

### 3.4 Analysis Summary Bar

| # | Metric | Value | Insight |
|---|---|---|---|
| 1 | Complaints Analysed | 847 | Scope of this analysis |
| 2 | Patterns Identified | 14 | Distinct recurring patterns found |
| 3 | Systemic Issues (3+ branches) | 6 | Issues affecting multiple branches |
| 4 | Seasonal Spikes | 3 | Categories with statistically significant seasonal elevation |
| 5 | Staff-Linked Patterns | 2 | Patterns linked to specific staff members (IDs masked) |
| 6 | Top Category | Academic (29%) | Most frequent complaint category |
| 7 | Fastest Growing | Safety (+34% vs last FY) | Category with largest YoY increase |
| 8 | Post-Intervention Reductions | 2 | Categories where prior interventions reduced complaints |

---

## 4. Page Sections

### Section 1 — Top Patterns (ranked list)

Automatically ranked patterns sorted by: (frequency × severity × branch spread).

**Pattern card layout:**

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  #1 — Homework Overload / Insufficient Rest Time                  📚 Academic  │
│  Frequency: 87 complaints · Branches: 12 of 28 · Severity: Medium             │
│  Peak period: Nov–Jan (board exam prep season)                                 │
│  Branch types affected: Coaching (74%) · School (26%)                          │
│                                                                                │
│  Pattern description: Parents and students report excessive daily homework     │
│  (4–6 hours) with insufficient time for rest, meals, or non-academic           │
│  activities. Highest volume in Class IX–XI coaching batches. Complaints        │
│  cluster in November (onset of revision schedule) and January (mock exam       │
│  season). Correlation: branches with daily 8+ hour batch schedules generate    │
│  3× more homework complaints than branches with 6-hour schedules.              │
│                                                                                │
│  Root cause hypothesis: No group-level policy on homework quantum per class    │
│  level. Individual teachers and HoDs set homework independently.               │
│                                                                                │
│  Recommended intervention: Issue group homework policy (max hours per          │
│  day by class level); include in teacher induction; measure reduction in       │
│  Q1 next FY.                                                                   │
│                                                                                │
│  Status: ⬜ No intervention initiated                                           │
│  [Raise CAPA]  [Create Policy Draft]  [Mark Addressed]  [Expand]              │
└────────────────────────────────────────────────────────────────────────────────┘
```

Pattern card fields:
- Pattern title (auto-generated from clustering algorithm + manual label option)
- Category badge
- Frequency + branch spread + severity distribution
- Peak period (seasonal analysis)
- Branch types affected (proportional)
- Pattern description (auto-generated summary + manual edit option)
- Root cause hypothesis (manual input by Grievance Audit Officer)
- Recommended intervention (manual input)
- Intervention status: No intervention / Intervention planned / Intervention in progress / Closed — measured

Action buttons per card:
- `[Raise CAPA]` → Opens CAPA form pre-filled
- `[Create Policy Draft]` → Opens document editor stub
- `[Mark Addressed]` → Record that intervention is underway
- `[Expand]` → Shows full complaint list (masked), timeline chart, branch breakdown

**Patterns ranked 1–14 displayed in scrollable list.**

---

### Section 2 — Cluster Analysis by Category

**Tab selector:** [Academic] [Fee] [Safety] [POCSO] [Harassment] [Infrastructure] [Staff Conduct] [Other]

Per-category deep analysis:

**Sub-section A — Volume Trend (line chart)**
Monthly complaint count for this category. Current FY vs prior FY overlay. Seasonal peaks annotated.

**Sub-section B — Branch Distribution (bar chart)**
Which branches generate the most complaints in this category, normalised per 100 students.

**Sub-section C — Sub-issue Breakdown**
Academic → Homework overload · Exam pressure · Teaching quality · Syllabus pace · Result errors
Fee → Late fee penalties · Receipt not provided · Fee hike without notice · Refund not processed · Wrong fee charged
Safety → Infrastructure/facility failure · Food/hygiene · Hostel safety · Transport safety · CCTV/security
...etc per category.

Shown as horizontal bar with count per sub-issue.

**Sub-section D — Keyword Cloud**
Top 30 keywords from free-text complaint descriptions in this category (stop words removed, Indian education vocabulary weighted). Size = frequency. Colour = sentiment weight (red = negative emotion words like "threatening", "unsafe", "unfair"; blue = process words like "delay", "no response", "overdue").

**Sub-section E — Resolution Quality for this Category**
- Avg resolution time (vs SLA)
- Re-open rate
- Mean satisfaction score
- Satisfaction score trend

---

### Section 3 — Seasonal Analysis

**Heatmap: Month × Category**
- Rows: 8 complaint categories
- Columns: 12 months (Apr–Mar)
- Cell colour: White (baseline) → Amber (1.5× baseline) → Red (2× baseline)
- Baseline: Average monthly volume for that category

**Seasonal spike table:**

| Category | Spike Month(s) | Spike Multiplier | Likely Cause | Pre-emptive Action |
|---|---|---|---|---|
| Academic quality | Nov, Jan | 2.3× | Board exam pressure; revision overload | Issue revised study schedule policy by Oct |
| Fee disputes | Apr, Jun, Oct | 2.8× | New year fee hike; late fee enforcement; half-yearly deadline | Fee communication SOP before each deadline |
| Safety | Jul, Aug | 1.7× | Monsoon — leaking roofs, slippery floors, flooded grounds | Monsoon readiness audit by June |
| Staff conduct | Apr, Jan | 1.4× | New teacher joins (April); exam pressure behaviour (January) | Induction + behaviour training schedule |

---

### Section 4 — Staff-Linked Patterns

> **Privacy note:** Staff are identified by internal ID only on this page. Resolution of ID to name is done via HR module by authorized personnel.

**Table:**

| Pattern ID | Staff ID | Branches Involved | Complaint Category | Complaint Count | Severity | Tenure Period Overlap |
|---|---|---|---|---|---|---|
| SP-001 | STF-00892 | Sunrise Miyapur, Sunrise Begumpet, Sunrise Kukatpally | Staff Conduct (verbal reprimand) | 23 complaints | High | Sep–Dec 2025 (at all 3 branches) |
| SP-002 | STF-01245 | Sunrise Hyderabad Central, Sunrise KPHB | Fee disputes (wrong fee charged) | 11 complaints | Medium | Aug–Mar 2026 |

**For each staff-linked pattern:**
```
[Flag to HR]   [View Anonymised Complaint Details]   [Create CAPA]
```

`[Flag to HR]` → Sends a flagged alert to the Group HR module (HR can then de-anonymise using their own access level). The Grievance Audit Officer never directly identifies the staff member to the HR system — they flag the pattern ID. HR resolves to name independently.

---

### Section 5 — Branch-Type Vulnerability Analysis

Complaint profiles by institution type — shows which institution types are most vulnerable to which complaint categories.

**Stacked bar chart per institution type:**

| Institution Type | Top 3 Complaint Categories |
|---|---|
| School (Day) | Academic quality (32%) · Fee disputes (28%) · Staff conduct (18%) |
| Coaching Institute | Academic quality (44%) · Fee disputes (22%) · Infrastructure (15%) |
| Residential School | Safety (38%) · Academic quality (28%) · Infrastructure (18%) |
| Junior College | Fee disputes (35%) · Academic quality (30%) · Staff conduct (20%) |

**Insight panel below chart:**
"Residential schools generate 3.8× more safety complaints per 100 students than day schools — expected due to 24/7 operations, but 2 residential branches are generating 7× the median, indicating a specific safety management gap."

---

### Section 6 — Pre/Post Intervention Measurement

For each recorded intervention (marked in Section 1 patterns), this section shows whether the intervention reduced complaint volume.

**Chart per intervention:** Line chart — monthly complaint volume in relevant category, with intervention date marked as a vertical line. Before vs after comparison.

**Table:**

| Intervention | Date | Target Category | Avg Monthly Complaints Before | Avg Monthly Complaints After | Change |
|---|---|---|---|---|---|
| New homework policy issued | Nov-2025 | Academic — Homework | 18.3/month | 9.1/month | −50% ✅ Effective |
| Fee receipt SOP communicated | Sep-2025 | Fee — Receipt not provided | 12.7/month | 14.2/month | +12% ❌ Not effective — follow up needed |

---

## 5. Sections

| # | Section | Location | Purpose |
|---|---|---|---|
| 1 | Top Patterns | Main body | Ranked pattern cards with intervention tracking |
| 2 | Cluster Analysis | Tab per category | Deep per-category analysis with charts and keywords |
| 3 | Seasonal Analysis | Heatmap section | Month × category spike detection |
| 4 | Staff-Linked Patterns | Table section | Privacy-safe staff pattern flagging |
| 5 | Branch-Type Vulnerability | Chart section | Institution-type complaint profiles |
| 6 | Pre/Post Intervention | Chart + table | Intervention effectiveness measurement |
| 7 | Pattern Report Generator | Modal | Auto-generate quarterly pattern analysis report |
| 8 | CAPA from Pattern Modal | Modal | Raise CAPA linked to a pattern |

---

## 6. Modals

### Modal 1 — Generate Pattern Report

**Trigger:** `[Generate Pattern Report]` button.

**Form:**
```
Report Type:
  ◉ Quarterly Pattern Analysis Report   ○ Annual Executive Summary   ○ Custom

Period: [Q3 FY 2025-26 — Oct–Dec 2025 ▼]

Include Sections:
  ☑ Top 5 patterns with recommendations
  ☑ Seasonal analysis
  ☑ Branch comparison
  ☑ SLA compliance summary
  ☑ Intervention effectiveness (if any)
  ☐ Staff-linked patterns (include: ◉ Anonymised IDs only ○ Exclude entirely)

Executive Summary (auto-draft — editable):
  [Text area with auto-generated summary from pattern data]

Format: ◉ PDF   ○ Word (.docx)   ○ Both

Recipients: ☑ Audit Head (121)   ☑ CEO   ☐ Board (Chairman only)   ☐ Zone Directors
```

**Actions:** `[Generate & Send]` `[Generate & Download]` `[Cancel]`

---

### Modal 2 — CAPA from Pattern

**Pre-fills from the pattern card:**
- Branch(es) affected (multi-select where pattern spans multiple branches)
- Category
- Severity (derived from pattern severity)
- Finding description (auto-filled from pattern description)

Coordinator edits and submits → CAPA raised in P-15.

---

## 7. Charts

### Chart 1 — Pattern Frequency vs Branch Spread (bubble chart)
- **Type:** Bubble chart (Chart.js 4.x)
- **X-axis:** Number of branches affected
- **Y-axis:** Complaint frequency
- **Bubble size:** Mean severity (larger = more severe)
- **Colour:** Category colour coding
- **Purpose:** Quadrant view — top-right bubble (high frequency + many branches) = highest priority systemic issue
- **API:** `GET /api/v1/group/{id}/audit/grievances/patterns/charts/bubble/`

### Chart 2 — Seasonal Heatmap (matrix)
- **Type:** Matrix heatmap (chartjs-chart-matrix plugin)
- **X-axis:** 12 months
- **Y-axis:** 8 categories
- **Colour:** White → Amber → Red by spike multiplier
- **API:** `GET /api/v1/group/{id}/audit/grievances/patterns/charts/seasonal/`

### Chart 3 — Pre/Post Intervention (line per intervention)
- **Type:** Line (Chart.js 4.x)
- **Intervention date:** Vertical dashed line annotation
- **API:** `GET /api/v1/group/{id}/audit/grievances/patterns/charts/intervention/{intervention_id}/`

### Chart 4 — Category Share by Institution Type (grouped bar)
- **Type:** Grouped bar (Chart.js 4.x)
- **X-axis:** Institution types
- **Y-axis:** % of complaints in each category
- **Groups:** 8 categories per institution type
- **API:** `GET /api/v1/group/{id}/audit/grievances/patterns/charts/by-institution-type/`

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Analysis run | "Pattern analysis complete — 847 complaints · 14 patterns identified · FY 2025-26" | Success (green) |
| CAPA raised from pattern | "CAPA-2026-00450 raised — Academic: Homework Overload · 12 branches" | Info (blue) |
| Staff pattern flagged | "Pattern SP-001 flagged to HR — STF-00892 · Staff conduct · 3 branches" | Warning (amber) |
| Pattern marked addressed | "Pattern #1 marked as addressed — Homework Policy intervention recorded" | Success (green) |
| Report generated | "Quarterly Pattern Analysis Report generated — Q3 FY 2025-26 · sent to Audit Head + CEO" | Success (green) |
| New seasonal spike | "⚠️ Seasonal spike detected: Safety complaints 2.4× above baseline this month" | Warning (amber) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No patterns found (< 20 complaints) | Graph with dotted line | "Not enough data to identify patterns. Patterns emerge after 20+ complaints across multiple branches." | — |
| No staff-linked patterns | Shield icon | "No staff-linked complaint patterns detected in this period." | — |
| No seasonal spikes | Calendar with green marks | "No significant seasonal spikes detected — complaint distribution is relatively even across months." | — |
| No interventions recorded | Lightbulb outline | "No interventions recorded yet. Use [Mark Addressed] on patterns to track interventions and measure effectiveness." | — |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Page initial load (no analysis run) | Empty state with [Analyse] prompt | Instant |
| Analysis computation | Progress bar: "Analysing 847 complaints…" | 3–8s (server-side) |
| Pattern cards | Skeleton cards → populated | < 1s after analysis |
| Keyword cloud | Placeholder → D3.js or Chart.js word cloud | < 1s |
| Seasonal heatmap | Grid skeleton → populated | < 1s |
| Bubble chart | Placeholder → Chart.js | < 500ms |
| Report generation | "Generating report… compiling 14 patterns" progress | 5–15s |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/grievances/patterns/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | POST | `/analyse/` | Run pattern analysis for given filters/period | 126, G1+ |
| 2 | GET | `/` | Retrieve cached pattern results | G1+ |
| 3 | GET | `/{pattern_id}/` | Pattern detail with full complaint list (masked) | G1+ |
| 4 | PATCH | `/{pattern_id}/` | Update pattern — root cause, recommendation, intervention status | 126 |
| 5 | POST | `/{pattern_id}/raise-capa/` | Raise CAPA from pattern | 126, 128 |
| 6 | POST | `/{pattern_id}/flag-to-hr/` | Flag staff-linked pattern to HR module | 126 |
| 7 | POST | `/{pattern_id}/mark-addressed/` | Record intervention | 126 |
| 8 | GET | `/staff-linked/` | Staff-linked patterns (IDs only) | 126, G4+ |
| 9 | GET | `/seasonal/` | Seasonal spike analysis | G1+ |
| 10 | GET | `/interventions/` | Intervention effectiveness data | G1+ |
| 11 | POST | `/report/generate/` | Generate quarterly/annual pattern report | 126 |
| 12 | GET | `/charts/bubble/` | Chart 1 data | G1+ |
| 13 | GET | `/charts/seasonal/` | Chart 2 data | G1+ |
| 14 | GET | `/charts/intervention/{id}/` | Chart 3 data | G1+ |
| 15 | GET | `/charts/by-institution-type/` | Chart 4 data | G1+ |
| 16 | GET | `/export/` | Export pattern analysis as Excel/PDF | G1+ |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Run analysis | `[Analyse]` click | `hx-post=".../patterns/analyse/"` | `#pattern-results` | `innerHTML` | Progress bar during computation |
| Pattern cards load | After analysis | `hx-get=".../patterns/"` | `#pattern-cards` | `innerHTML` | Auto-triggered |
| Category tab switch | Tab click | `hx-get=".../patterns/?category={cat}"` | `#category-content` | `innerHTML` | — |
| Seasonal heatmap | Section shown | `hx-get=".../patterns/charts/seasonal/"` | `#seasonal-chart` | `innerHTML` | Chart.js |
| Staff patterns | Section shown | `hx-get=".../patterns/staff-linked/"` | `#staff-patterns` | `innerHTML` | — |
| Expand pattern | `[Expand]` click | `hx-get=".../patterns/{id}/"` | `#pattern-{id}-detail` | `innerHTML` | Inline expand |
| Mark addressed | Button click | `hx-post=".../patterns/{id}/mark-addressed/"` | `#pattern-{id}-status` | `innerHTML` | Toast + badge update |
| Raise CAPA modal | Button click | — | `#modal-content` | `innerHTML` | Modal |
| Submit CAPA | Form submit | `hx-post=".../patterns/{id}/raise-capa/"` | `#capa-result` | `innerHTML` | Toast |
| Generate report | Form submit | `hx-post=".../patterns/report/generate/"` | `#report-result` | `innerHTML` | Progress → toast |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
