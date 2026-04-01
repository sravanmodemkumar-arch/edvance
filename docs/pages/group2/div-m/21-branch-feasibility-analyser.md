# Page 21: Branch Feasibility Analyser

**Division:** M — Analytics & MIS
**URL:** `/group/analytics/feasibility/`
**Primary Role:** 107 — Strategic Planning Officer
**Supporting Roles:** 102 (Analytics Director)
**Read-only access:** 103 (MIS Officer) — can view studies but not create or edit
**Restricted:** Roles 104, 105, 106 — no access
**Access Level:** G1 (read-only on all operational data; write on Division M feasibility studies and strategic notes)

---

## 1. Purpose

Provides a structured workspace for evaluating whether a new branch location is viable, or whether an existing branch should be expanded, restructured, or closed. The Strategic Planning Officer creates feasibility studies by pulling live data from all operational divisions (population, infrastructure, competition, finance, academic capacity) and generates scored recommendation reports for management review.

---

## 2. Roles & Permissions Matrix

| UI Element | Role 102 | Role 103 | Role 107 |
|---|---|---|---|
| KPI bar (5 cards) | View | View | View |
| Study list table | View | View | View |
| Study detail drawer | View | View | View |
| Create feasibility study | — | — | Create |
| Edit draft study | — | — | Edit (own) |
| Delete draft study | — | — | Delete (own, draft only) |
| Submit study for review | — | — | Submit (own) |
| Add strategic note | — | — | Create/Edit/Delete (own) |
| Generate PDF report | View | View | Create |
| Export (CSV) | Download | Download | Download |

Studies in "Submitted" or "Approved" status cannot be edited or deleted by any role.

---

## 3. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ Breadcrumb: Analytics & MIS > Branch Feasibility Analyser           │
│ Title: "Branch Feasibility Analyser"   [Export ▼]  [+ New Study]   │
├─────────────────────────────────────────────────────────────────────┤
│  KPI BAR (5 cards)                                                   │
│  Total Studies | Draft | Under Review | Approved | Rejected         │
├─────────────────────────────────────────────────────────────────────┤
│  FILTER BAR                                                          │
│  Study Type [All ▼]  Status [All ▼]  Location State [All ▼]        │
│  Created By [All ▼]  Date Range [All ▼]  [Search…]  [Apply] [Clear] │
├─────────────────────────────────────────────────────────────────────┤
│  FEASIBILITY STUDY TABLE (sortable, paginated)                       │
├──────────────────────────────────┬──────────────────────────────────┤
│  VIABILITY SCORE DISTRIBUTION    │  STUDY TYPE BREAKDOWN            │
│  (Histogram — score buckets)     │  (Donut — New/Expand/Close/etc)  │
└──────────────────────────────────┴──────────────────────────────────┘
```

---

## 4. KPI Bar

Five stat cards. Auto-refresh `hx-trigger="every 300s"`, `hx-target="#feasibility-kpi-bar"`.

| # | Label | Value | Sub-label | Highlight |
|---|---|---|---|---|
| 1 | Total Studies | Count of all studies | "All time" | — |
| 2 | Draft | Studies in Draft status | "Awaiting submission" | — |
| 3 | Under Review | Submitted, awaiting approval | "In pipeline" | `bg-amber-50` |
| 4 | Approved | Approved studies | "This year" | `bg-green-50` |
| 5 | Rejected | Rejected studies | "This year" | — |

---

## 5. Filter Bar

| Control | Type | Options |
|---|---|---|
| Study Type | Select | All / New Branch / Expansion / Restructure / Closure / Relocation |
| Status | Select | All / Draft / Submitted / Under Review / Approved / Rejected |
| Location State | Select | All + Indian states list |
| Created By | Select | All + names (users who created studies) |
| Date Range | Select | This Month / This Quarter / This Year / Custom |
| Search | Text | Study title, location, reference number |

`[Apply]` triggers HTMX table + chart reload.

---

## 6. Feasibility Study Table

### 6.1 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Integer | No | — |
| Study Title | Text | Yes | Truncated 60 chars |
| Type | Badge | Yes | New/Expand/Close/etc — colour-coded |
| Location | Text | Yes | City, State |
| Viability Score | Progress bar + number | Yes | 0–100; colour by band |
| Status | Badge | Yes | Draft/Submitted/Approved/Rejected |
| Created By | Text | Yes | — |
| Created Date | Date | Yes | — |
| Last Updated | Date | Yes | — |
| Actions | Buttons | No | [View] [Edit] [Delete] [Submit] (role-gated) |

### 6.2 Viability Score Colour Bands

| Score | Band | Colour |
|---|---|---|
| ≥ 75 | Viable | `bg-green-100 text-green-800` |
| 55–74 | Moderate | `bg-yellow-100 text-yellow-800` |
| 35–54 | Marginal | `bg-orange-100 text-orange-800` |
| < 35 | Not Viable | `bg-red-100 text-red-800` |

### 6.3 Action Gating

- **[Edit]:** Role 107 only, Draft status only.
- **[Delete]:** Role 107 only, Draft status only → confirm modal.
- **[Submit]:** Role 107 only, Draft status only → confirm modal → status changes to "Submitted".
- **[View]:** All permitted roles.

### 6.4 Pagination

20 rows per page, HTMX-driven with `hx-include="#feasibility-filter-form"`.

---

## 7. Create / Edit Feasibility Study Drawer

**ID:** `feasibility-study-drawer`
**Width:** 800px (widest drawer used in Division M — study has 6 tabs of data)
**Header:** "New Feasibility Study" / "Edit: {Study Title}"
**Trigger:** `[+ New Study]` button or `[Edit]` action.

### Tab 1 — Study Basics

| Field | Type | Validation |
|---|---|---|
| Study Title | Text input (max 200 chars) | Required |
| Study Type | Select: New Branch / Expansion / Restructure / Closure / Relocation | Required |
| Target Location | Text input (City, State) | Required |
| Pincode | Text input (6 digits) | Required, numeric |
| Nearest Existing Branch | Select (branches in group) | Optional |
| Target Academic Year | Select (academic year list) | Required |
| Study Description | Textarea (max 1000 chars) | Required, min 30 chars |
| Lead Officer | Read-only (current user) | — |
| Study Reference No | Auto-generated (read-only after creation) | — |

### Tab 2 — Demand Analysis

| Field | Type | Validation |
|---|---|---|
| Estimated Student-Age Population (10 km radius) | Number input | Required |
| Source of Population Estimate | Select: Census 2011 / Census 2024 / Municipal Data / Survey / Estimate | Required |
| Current JEE/NEET aspirant density (if known) | Number input (optional) | Optional |
| Existing coaching institutes in area | Number input | Required |
| Primary competition institutions | Textarea (names, comma-separated, max 500 chars) | Optional |
| Estimated addressable market (students/year) | Number input | Required |
| Demand evidence notes | Textarea (max 800 chars) | Optional |

### Tab 3 — Financial Projections

| Field | Type | Validation |
|---|---|---|
| Estimated setup cost (INR lakhs) | Decimal input | Required, > 0 |
| Estimated monthly operating cost (INR lakhs) | Decimal input | Required, > 0 |
| Expected Year 1 student count | Number input | Required |
| Expected Year 2 student count | Number input | Required |
| Expected Year 3 student count | Number input | Required |
| Average fee per student per year (INR) | Number input | Required |
| Break-even timeline (months) | Number input | Required |
| Projected Year 3 revenue (INR lakhs) | Decimal input (auto-calculated from fields above; editable) | Required |
| Funding source | Select: Internal / Loan / Investor / Mixed | Required |
| Financial risk notes | Textarea (max 500 chars) | Optional |

Break-even months is auto-validated: if setup cost / (monthly revenue − monthly operating cost) differs from entered value by > 20%, a soft warning is shown ("Verify break-even estimate — computed value is {X} months").

### Tab 4 — Infrastructure Assessment

| Field | Type | Validation |
|---|---|---|
| Land / building status | Select: Owned / Leased / To be acquired / Unknown | Required |
| Total area (sq ft) | Number input | Required |
| Classroom count (initial) | Number input | Required |
| Lab availability | Checkbox: Physics / Chemistry / Biology / Computer | Optional |
| Hostel required? | Toggle (Yes / No) | Required |
| Hostel capacity (if Yes) | Number input (conditional on Yes) | Conditional required |
| Transport accessibility | Select: Excellent / Good / Moderate / Poor | Required |
| Infrastructure readiness score | Auto-calculated (0–100 based on inputs above; read-only) | — |
| Infrastructure notes | Textarea (max 500 chars) | Optional |

Infrastructure readiness score formula: Owned building (+30), Adequate area for projected students (+20), Labs present (+20), Good/Excellent transport (+15), Hostel if required (+15). Displayed as a progress bar.

### Tab 5 — Risk Assessment

| Field | Type | Validation |
|---|---|---|
| Regulatory risk | Select: Low / Medium / High | Required |
| Competition risk | Select: Low / Medium / High | Required |
| Financial risk | Select: Low / Medium / High | Required |
| Operational risk | Select: Low / Medium / High | Required |
| Staff availability risk | Select: Low / Medium / High | Required |
| Overall risk level | Auto-calculated from above (modal value); read-only | — |
| Risk mitigation notes | Textarea (max 1000 chars) | Required if any risk = High |
| Regulatory clearances required | Checkbox: CBSE / State Board / AICTE / Municipal / Fire NOC / Other | Optional |

### Tab 6 — Summary & Score

All fields in this tab are **read-only**, auto-computed from Tabs 2–5.

| Field | Value |
|---|---|
| Overall Viability Score | 0–100 (computed, colour-banded) |
| Score Breakdown | Progress bar for each dimension: Demand (25%), Financial (30%), Infrastructure (25%), Risk (20%) |
| Recommendation | Auto-text: "Viable — Recommend proceeding to planning phase" / "Moderate — Further analysis recommended" / "Marginal — Significant risks; further feasibility study needed" / "Not Viable — Not recommended at this time" |
| Key Strengths | Auto-generated bullet list from high-scoring fields |
| Key Risks | Auto-generated bullet list from high-risk fields |
| Officer Notes | Textarea (max 1000 chars) — editable by Role 107 | Optional |
| Submit Study | Button — only active in Draft status; triggers status change to "Submitted" |

---

## 8. Feasibility Study Detail Drawer

**ID:** `feasibility-detail-drawer`
**Width:** 800px
**Triggered by:** `[View]` action or row click.

Same 6-tab layout as the create/edit drawer but all fields are **read-only**. The Tab 6 summary is the focal point.

Additional read-only fields shown in Detail drawer:

| Field | Notes |
|---|---|
| Submission Date | Date (if submitted) |
| Review Notes | Text from management reviewer (if reviewed) |
| Approval / Rejection Date | Date |
| Approved / Rejected By | Name + role |

**[Generate PDF Report]** button in drawer footer — available to Roles 102, 103, 107. Triggers async PDF export: POST → job_id → poll every 5s → download link in drawer.

---

## 9. Viability Score Distribution Chart

**Type:** Histogram (Chart.js 4.x Bar)
**Canvas ID:** `viabilityHistogramChart`
**Height:** 260px

- X-axis: Score buckets: 0-9, 10-19, …, 90-100.
- Y-axis: Count of studies.
- Bar colour: gradient from red (low) to green (high) per bucket using viability bands.
- Tooltip: `{bucket} range: {count} studies`.
- Clicking a bar filters the table to that score range.

---

## 10. Study Type Breakdown Chart

**Type:** Donut chart (Chart.js 4.x Doughnut)
**Canvas ID:** `studyTypeDonutChart`
**Height:** 260px

- Slices: New Branch, Expansion, Restructure, Closure, Relocation.
- Colorblind-safe palette.
- Centre label: total studies.
- Tooltip: `{Type}: {count} ({percent}%)`.
- Clicking a slice filters the table to that study type.

---

## 11. Strategic Notes Panel

Below the table (Role 107 only — Roles 102/103 see notes as read-only list).

A freeform annotation layer for the Strategic Planning Officer to record market intelligence, observations, or meeting notes not tied to a specific study.

**Notes Table:**

| Column | Notes |
|---|---|
| Title | Short title (max 100 chars) |
| Note | Truncated 100 chars |
| Location Reference | City / State (optional) |
| Added By | Name |
| Date | Formatted |
| Actions | Edit / Delete (Role 107 own only) |

**[+ Add Strategic Note] Drawer (Role 107):**

| Field | Type | Validation |
|---|---|---|
| Title | Text (max 100 chars) | Required |
| Location Reference | Text (optional) | Optional |
| Note Text | Textarea (max 1500 chars) | Required |
| Linked Study | Select (optional — link to a feasibility study) | Optional |
| Visibility | Radio: Division M only / Visible to Analytics Director | Required |

Submit: POST → toast → row prepended to table.

---

## 12. Submit for Review — Confirm Modal

**Triggered by:** [Submit] button (Tab 6 or table action).

Modal content:
- "You are about to submit **{Study Title}** for management review. Once submitted, the study cannot be edited."
- Checklist: "I confirm all data is accurate" (must check before submitting).
- [Cancel] / [Submit Study] buttons.

On confirm: PATCH `/api/v1/analytics/feasibility-studies/{id}/submit/` → status changes to "Submitted" → toast → table row status badge updates.

---

## 13. Delete Confirm Modal

Simple confirm modal for Draft studies:
- "Delete this draft study? This action cannot be undone."
- [Cancel] / [Delete] buttons.
- DELETE `/api/v1/analytics/feasibility-studies/{id}/` → row removed → toast.

---

## 14. Export

| Option | Endpoint | Notes |
|---|---|---|
| Export Study List (CSV) | GET `/api/v1/analytics/feasibility-studies/export/?format=csv` | With active filters |
| Export Study PDF | POST `/api/v1/analytics/feasibility-studies/{id}/export/` | Async per-study PDF |
| Export All Approved (CSV) | GET `/api/v1/analytics/feasibility-studies/export/?status=approved` | Approved only |

PDF format: full 6-tab summary, viability score breakdown, recommendation, auto-generated key strengths and risks. Letterhead with institution group name and date.

---

## 15. Toast Notifications

| Trigger | Type | Message |
|---|---|---|
| Study created | Success | "Feasibility study '{title}' created as Draft." |
| Study updated | Success | "Study updated." |
| Study deleted | Info | "Draft study removed." |
| Study submitted | Success | "Study '{title}' submitted for review." |
| Note saved | Success | "Strategic note saved." |
| Note deleted | Info | "Note removed." |
| Form validation fail | Error | "Please fill in all required fields." |
| Score calculation | Info | "Viability score recalculated: {score}/100." |
| Export started | Info | "Preparing export…" |
| Export ready | Success | "Export ready. Click to download." |
| Export failed | Error | "Export failed. Please try again." |

---

## 16. Empty States

| Context | Message | CTA |
|---|---|---|
| No studies created | "No feasibility studies yet. Start by creating your first study." | "+ New Study" (Role 107) |
| No results for filters | "No studies match the selected filters." | "Reset Filters" |
| No approved studies | "No studies have been approved yet." | — |
| No strategic notes | "No strategic notes added yet." | "+ Add Note" (Role 107) |

---

## 17. Loader States

| Element | Loader |
|---|---|
| Initial page load | 5 card shimmer + filter bar shimmer + table shimmer (20 rows) + 2 chart placeholders |
| Table reload | Table body shimmer (20 rows) |
| KPI bar refresh | Individual card shimmer |
| Drawer open | Spinner centred in drawer |
| Tab switch within drawer | Tab content shimmer |
| Score recalculation | "Recalculating…" spinner below Tab 6 score |
| PDF generation | Progress indicator in drawer footer |

---

## 18. HTMX Patterns

| Pattern | Target | Endpoint | Trigger |
|---|---|---|---|
| Table + chart reload | `#feasibility-main-section` | `/group/analytics/feasibility/data/` | Apply filter |
| KPI auto-refresh | `#feasibility-kpi-bar` | `/group/analytics/feasibility/kpis/` | `every 300s` |
| Table search | `#feasibility-table-section` | `/group/analytics/feasibility/table/` | `keyup changed delay:300ms` |
| Table pagination | `#feasibility-table-section` | `/group/analytics/feasibility/table/?page={n}` | Page nav |
| Create/edit form POST/PUT | `#feasibility-study-drawer` | `/api/v1/analytics/feasibility-studies/` | Form submit |
| Viability score recalc | `#viability-score-section` | `/group/analytics/feasibility/score-preview/` | `change` on any Tab 2-5 field (debounced 600ms) |
| Detail drawer open | `#feasibility-detail-drawer` | `/group/analytics/feasibility/{id}/detail/` | Row click / [View] |
| Submit PATCH | `#submit-confirm-modal` | `/api/v1/analytics/feasibility-studies/{id}/submit/` | Modal confirm |
| Note POST | `#strategic-note-form` | `/api/v1/analytics/feasibility-studies/notes/` | Form submit |
| Export PDF poll | `#export-status` | `/api/v1/analytics/export-jobs/{id}/status/` | `every 5s` (stop on complete) |

---

## 19. API Endpoints

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| GET | `/api/v1/analytics/feasibility-studies/` | List (paginated, filtered) | G1 |
| POST | `/api/v1/analytics/feasibility-studies/` | Create study | Role 107 |
| GET | `/api/v1/analytics/feasibility-studies/{id}/` | Study detail | G1 |
| PUT | `/api/v1/analytics/feasibility-studies/{id}/` | Update draft study | Role 107 (own draft) |
| DELETE | `/api/v1/analytics/feasibility-studies/{id}/` | Delete draft | Role 107 (own draft) |
| PATCH | `/api/v1/analytics/feasibility-studies/{id}/submit/` | Submit for review | Role 107 |
| GET | `/api/v1/analytics/feasibility-studies/kpis/` | KPI values | G1 |
| GET | `/api/v1/analytics/feasibility-studies/charts/` | Chart data | G1 |
| POST | `/api/v1/analytics/feasibility-studies/score-preview/` | Live score calculation | Role 107 |
| GET | `/api/v1/analytics/feasibility-studies/notes/` | Strategic notes | G1 |
| POST | `/api/v1/analytics/feasibility-studies/notes/` | Add note | Role 107 |
| PUT | `/api/v1/analytics/feasibility-studies/notes/{id}/` | Edit note | Role 107 (own) |
| DELETE | `/api/v1/analytics/feasibility-studies/notes/{id}/` | Delete note | Role 107 (own) |
| GET | `/api/v1/analytics/feasibility-studies/export/` | CSV export | G1 |
| POST | `/api/v1/analytics/feasibility-studies/{id}/export/` | Per-study PDF | G1 |
| GET | `/api/v1/analytics/export-jobs/{id}/status/` | Poll job | G1 |

---

## 20. Mobile (Flutter + Riverpod)

| Screen | Description |
|---|---|
| `FeasibilityHomeScreen` | KPI cards + study list with status badges |
| `FeasibilityStudyDetailScreen` | Read-only 6-tab summary (mobile layout: vertical sections, no tabs) |
| `ViabilityScoreScreen` | Score breakdown with progress bars per dimension |

No create/edit functionality on mobile. State: `feasibilityStudiesProvider` (Riverpod). Pull-to-refresh.

---

## 21. Accessibility & Responsiveness

- Table scrolls horizontally on mobile; essential columns (Title, Type, Score, Status) remain visible.
- Viability score progress bars include text value and colour-coded label (not colour alone).
- Drawer is full-screen on mobile (100vw, 100vh) with sticky tab bar.
- All form fields in the 6-tab drawer: visible labels, `aria-required`, inline errors via `aria-describedby`.
- Tab navigation uses `role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected`.
- Score recalculation is announced via `aria-live="polite"` region.
- Soft warning messages for break-even estimate use `role="alert"` with amber background.
