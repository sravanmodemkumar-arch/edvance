# 63 — Academic Standardisation Audit

> **URL:** `/group/acad/standardisation-audit/`
> **File:** `63-standardisation-audit.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Director G3 · CAO G4 · Group Inspection Officer/Div-P (full create)

---

## 1. Purpose

The Academic Standardisation Audit page addresses a fundamental gap in academic governance: the ability to verify that branches are actually following group standards — not just receiving them. In a group that has invested in defining a common syllabus, lesson plan format, and assessment methodology, the question that follows is always: how do we know branches are adhering to them? Annual board inspections are too infrequent and too high-stakes. This page enables systematic, rolling internal audits conducted by the Academic Director and Group Inspection Officers.

Each audit assesses a branch against a 15-item rubric covering three domains: curriculum alignment (is the syllabus being taught as prescribed?), lesson plan format compliance (are lesson plans submitted in the required format and on time?), and assessment methodology (are assessment types and frequency matching group standards?). Each rubric item is rated Compliant / Partially Compliant / Non-Compliant, and the system computes an overall audit score as a percentage. Items rated Non-Compliant automatically generate corrective action items with a due date and owner (branch principal).

For groups that seek NAAC accreditation, ISO 21001 certification, or similar quality recognition, this audit log provides the internal quality assurance evidence required. The audit score trend per branch — tracked over multiple audit cycles — shows whether a branch is improving its academic standardisation over time or whether repeated non-compliance warrants a more intensive intervention.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Initiate audits | Can also initiate; view all results |
| Group Academic Director | G3 | ✅ Full | ✅ Full CRUD | Primary academic owner |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ❌ | ❌ | No access |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |
| Group Inspection Officer (Div-P) | Cross-div | ✅ Full | ✅ Full CRUD | Creates and conducts audits |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Gap-Fill  ›  Academic Standardisation Audit
```

### 3.2 Page Header
```
Academic Standardisation Audit                           [+ New Audit]  [Export ↓]
Internal quality assurance — branch compliance with group standards
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Audits Conducted (This Year) | Count |
| Branches Audited | Count / Total branches |
| Avg Audit Score (Group) | % |
| Branches with Score < 70% | Count — red |
| Open Corrective Actions | Count — amber |
| Overdue Corrective Actions | Count — red |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Branch name, Auditor name
- 300ms debounce

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Score Band | Select | Excellent (≥ 90%) / Good (70–89%) / Needs Improvement (< 70%) |
| Audit Status | Select | Completed / In Progress / Scheduled |
| Auditor | Multi-select | All auditors |
| Date range | Date range picker | |

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | |
| Branch | Text | ✅ | |
| Last Audit Date | Date | ✅ | Red if > 180 days ago |
| Auditor | Text | ✅ | |
| Audit Score | Number + badge | ✅ | % — green ≥ 90, amber 70–89, red < 70 |
| Next Audit Due | Date | ✅ | Amber if ≤ 30 days |
| Corrective Actions | Number | ✅ | Open count |
| Actions Overdue | Number | ✅ | Red if > 0 |
| Status | Badge | ✅ | Completed / Scheduled / Overdue |
| Actions | — | ❌ | |

**Default sort:** Audit Score ascending (lowest performers first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

### 4.4 Row Actions

| Action | Visible To | Drawer | Notes |
|---|---|---|---|
| View Audit | All roles | `audit-view` drawer 560px | Full rubric scores + actions |
| New Audit for Branch | Academic Dir, CAO, Div-P | `audit-create` drawer 640px | Pre-filled with branch |
| View Corrective Actions | All roles | `audit-view` drawer — Actions tab | Open corrective actions |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | Academic Dir, CAO, Div-P | Audit summary for selected branches |

---

## 5. Drawers & Modals

### 5.1 Drawer: `audit-create` — New Audit
- **Trigger:** [+ New Audit] header button or row action
- **Width:** 640px
- **Tabs:** Branch & Auditor · Checklist · Corrective Actions · Submit

#### Tab: Branch & Auditor
| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Select | ✅ | |
| Auditor | Search + select | ✅ | Academic Dir / Div-P Inspector / CAO |
| Audit Date | Date | ✅ | Cannot be future |
| Audit type | Select | ✅ | Internal / External / Surprise |
| Documents reviewed | Multi-select | ✅ | Lesson plans / Syllabus plan / Student assessment records / Observation logs |

#### Tab: Checklist (15 items, 3 domains)

**Domain A — Curriculum Alignment (5 items):**
| # | Item | Rating | Notes |
|---|---|---|---|
| A1 | Syllabus taught matches group-prescribed syllabus | Compliant / Partially / Non-compliant | Required |
| A2 | Topics completed are within 5% of group pacing guide | Compliant / Partially / Non-compliant | Required |
| A3 | Prescribed textbooks are in use | Compliant / Partially / Non-compliant | Required |
| A4 | Supplementary materials are group-approved | Compliant / Partially / Non-compliant | Required |
| A5 | Competitive exam topics (JEE/NEET/Board) are addressed proportionally | Compliant / Partially / Non-compliant | Required |

**Domain B — Lesson Plan Format (5 items):**
| # | Item | Rating | Notes |
|---|---|---|---|
| B1 | Lesson plans are submitted for all subjects and periods | Compliant / Partially / Non-compliant | Required |
| B2 | Plans follow group-prescribed template | Compliant / Partially / Non-compliant | Required |
| B3 | Plans include learning objectives in SMART format | Compliant / Partially / Non-compliant | Required |
| B4 | Plans include assessment for learning activities | Compliant / Partially / Non-compliant | Required |
| B5 | Plans are submitted within the required advance period | Compliant / Partially / Non-compliant | Required |

**Domain C — Assessment Methodology (5 items):**
| # | Item | Rating | Notes |
|---|---|---|---|
| C1 | Assessment frequency matches group standards | Compliant / Partially / Non-compliant | Required |
| C2 | Assessment types match prescribed mix (MCQ/subjective/practical) | Compliant / Partially / Non-compliant | Required |
| C3 | Student feedback is collected and documented | Compliant / Partially / Non-compliant | Required |
| C4 | Re-assessment provision is in place and followed | Compliant / Partially / Non-compliant | Required |
| C5 | Assessment records are maintained in required format | Compliant / Partially / Non-compliant | Required |

**Auto-computed score:** Compliant = 2 pts · Partially = 1 pt · Non-compliant = 0 pts · Max = 30 pts → displayed as %.

#### Tab: Corrective Actions
Auto-generated rows for each Non-compliant item. Each row editable:
| Field | Notes |
|---|---|
| Item reference (auto) | e.g. "B2 — Lesson plan template not followed" |
| Required action | Editable text — default action suggested |
| Due date | Required; default = 30 days from audit date |
| Owner | Default = Branch Principal; editable |
| Priority | High / Medium / Low |

[+ Add Custom Action] — for issues found outside the checklist.

#### Tab: Submit
- Audit summary: Score % · Compliant: N/15 · Partially: N/15 · Non-compliant: N/15
- Overall narrative: Textarea (required, min 50 chars)
- Notify branch principal: Toggle (default on)
- Buttons: [Save Audit] · [Cancel]

### 5.2 Drawer: `audit-view`
- **Width:** 560px
- **Tabs:** Rubric Scores · Corrective Actions · History

**Tab: Rubric Scores** — Read-only version of the checklist with scores and notes.

**Tab: Corrective Actions**
Table: Item · Action · Due Date · Owner · Status (Open / In Progress / Closed) · [Mark Done] button (Div-P / Academic Dir only for group-level items; Branch Principal marks done via branch portal).

**Tab: History** — All audits for this branch: Date · Auditor · Score · Trend (↑↓→)

---

## 6. Charts

### 6.1 Audit Score Trend by Branch (Line)
- **Type:** Multi-line chart
- **Data:** Audit score across all completed audits per branch (select up to 5 branches for overlay)
- **X-axis:** Audit dates
- **Y-axis:** Score %
- **Reference line:** At 70% (compliance threshold)
- **Tooltip:** Branch · Date · Score
- **Export:** PNG

### 6.2 Compliance % by Criterion (Bar)
- **Type:** Vertical bar
- **Data:** % of branches rated "Compliant" for each of the 15 criteria (group-wide)
- **Identifies:** Systemic weaknesses — criteria where most branches are non-compliant
- **Colour:** Green ≥ 75% · Amber 50–74% · Red < 50%
- **Tooltip:** Criterion · Compliant: X%
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit created | "Audit recorded for [Branch]. Score: [X]%. Corrective actions generated." | Success | 4s |
| Audit updated | "Audit updated" | Success | 4s |
| Corrective action closed | "Action '[item]' marked as done" | Success | 4s |
| Branch notified | "Audit report shared with [Branch] principal" | Info | 4s |
| Export started | "Export preparing…" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No audits yet | "No audits conducted" | "Conduct your first standardisation audit to begin tracking compliance" | [+ New Audit] |
| No audits match filters | "No audits match" | "Clear filters to see all audits" | [Clear Filters] |
| No corrective actions | "No corrective actions" | "No items rated Non-Compliant in this audit" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) + chart areas |
| Table filter/search/sort/page | Inline skeleton rows |
| Audit create drawer | Spinner → tabs load |
| Audit view drawer | Spinner → tabs |
| Charts load | Skeleton chart areas |

---

## 10. Role-Based UI Visibility

| Element | Academic Dir G3 | CAO G4 | Div-P Inspector |
|---|---|---|---|
| [+ New Audit] | ✅ | ✅ | ✅ |
| Create audit | ✅ | ✅ | ✅ |
| View all audits | ✅ | ✅ | ✅ |
| Mark corrective actions done | ✅ | ✅ | ✅ |
| Bulk export | ✅ | ✅ | ✅ |
| Charts | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/standardisation-audit/` | JWT | Audit schedule list |
| GET | `/api/v1/group/{group_id}/acad/standardisation-audit/stats/` | JWT | Stats bar |
| POST | `/api/v1/group/{group_id}/acad/standardisation-audit/` | JWT (G3 Dir, G4, Div-P) | Create audit |
| GET | `/api/v1/group/{group_id}/acad/standardisation-audit/{id}/` | JWT | Audit detail |
| PUT | `/api/v1/group/{group_id}/acad/standardisation-audit/{id}/` | JWT (owner) | Update audit |
| GET | `/api/v1/group/{group_id}/acad/standardisation-audit/{id}/actions/` | JWT | Corrective actions |
| PATCH | `/api/v1/group/{group_id}/acad/standardisation-audit/{id}/actions/{aid}/done/` | JWT | Mark action done |
| GET | `/api/v1/group/{group_id}/acad/standardisation-audit/export/?format=xlsx` | JWT | Export |
| GET | `/api/v1/group/{group_id}/acad/standardisation-audit/charts/score-trend/` | JWT | Line chart data |
| GET | `/api/v1/group/{group_id}/acad/standardisation-audit/charts/criterion-compliance/` | JWT | Bar chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../standardisation-audit/?q=` | `#audit-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../standardisation-audit/?filters=` | `#audit-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../standardisation-audit/?sort=&dir=` | `#audit-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../standardisation-audit/?page=` | `#audit-table-section` | `innerHTML` |
| Audit create drawer | `click` | GET `.../standardisation-audit/create-form/` | `#drawer-body` | `innerHTML` |
| Audit create submit | `submit` | POST `.../standardisation-audit/` | `#drawer-body` | `innerHTML` |
| Audit view drawer | `click` | GET `.../standardisation-audit/{id}/` | `#drawer-body` | `innerHTML` |
| Mark action done | `click` | PATCH `.../standardisation-audit/{id}/actions/{aid}/done/` | `#action-row-{aid}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
