# P-08 — Inspection Checklist Builder

> **URL:** `/group/audit/inspections/checklists/`
> **File:** `p-08-inspection-checklist-builder.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Inspection Officer (Role 123, G3) — primary operator

---

## 1. Purpose

The Inspection Checklist Builder is the tool that creates and manages standardised audit checklists used during branch inspections. In Indian education, different inspections require different checklists — a CBSE affiliation inspection has 42 mandatory requirements, a fire safety inspection has 28 checkpoints, an academic quality visit has 35 evaluation parameters. Without standardised checklists, inspectors rely on memory and personal judgment, leading to inconsistent audits — one inspector checks 40 items, another checks 15 for the same type of visit.

The problems this page solves:

1. **No standard inspection protocol:** Different inspectors check different things at different branches. The Checklist Builder creates master templates that every inspector must follow — ensuring consistency. A "CBSE Affiliation Readiness" checklist contains every item the CBSE inspection committee will verify, so the internal team catches gaps before the external committee arrives.

2. **Regulatory checklist changes:** CBSE updated its affiliation norms in 2024 (mandatory CCTV, digital infrastructure, sports facilities, counsellor). State boards update norms periodically. The Checklist Builder allows versioning — when norms change, a new version is published and all future inspections use the updated checklist. Old versions are archived for audit trail.

3. **Weighted scoring:** Not all checklist items are equal — a non-functional fire alarm is more critical than a missing suggestion box. The builder assigns weights to items (Critical = 10x, Important = 5x, Standard = 1x), enabling a weighted compliance score rather than a simple yes/no count.

4. **Evidence requirements:** Some items need photo evidence (CCTV camera installation), some need document upload (fire NOC copy), some are visual observation only. The builder specifies evidence type per item, ensuring inspectors collect the right proof.

5. **Branch-type variants:** A hostel branch needs hostel-specific items (mess hygiene, dormitory capacity, warden room). A transport-enabled branch needs transport items. The builder supports conditional sections that appear only for applicable branch types.

**Scale:** 10–25 checklist templates · 20–50 items per checklist · 5 inspection types · version history · used across 60–200 inspections/year

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Inspection Officer | 123 | G3 | Full — create, edit, version checklists | Template owner |
| Group Internal Audit Head | 121 | G1 | Full — approve checklist templates, manage library | Approval authority |
| Group Academic Quality Officer | 122 | G1 | Read + edit academic checklists | Academic-specific |
| Group Affiliation Compliance Officer | 125 | G1 | Read + edit affiliation checklists | Affiliation-specific |
| Group ISO / NAAC Coordinator | 124 | G1 | Read + edit certification checklists | ISO/NAAC-specific |
| Group Compliance Data Analyst | 127 | G1 | Read — checklist usage analytics | Reporting |
| Group CEO / Chairman | — | G4/G5 | Read — checklist standards overview | Governance |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Checklist creation: 123 or 121. Checklist approval: 121 or G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Inspections  ›  Checklist Builder
```

### 3.2 Page Header
```
Inspection Checklist Builder                       [+ Create Checklist]  [Import Template]  [Export All]
Inspection Team
Sunrise Education Group · 18 active checklists · 6 categories · Last updated: 2 days ago
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Checklists | Integer | COUNT(checklists) WHERE status = 'active' | Static blue | `#kpi-active` |
| 2 | Total Items (All) | Integer | SUM(items) across all active checklists | Static blue | `#kpi-items` |
| 3 | Pending Approval | Integer | COUNT(checklists) WHERE status = 'pending_approval' | Red > 3, Amber 1–3, Green = 0 | `#kpi-pending` |
| 4 | Times Used (FY) | Integer | COUNT(inspections) that used a checklist this FY | Static blue | `#kpi-used` |
| 5 | Avg Checklist Score | Percentage | AVG(checklist_score) across all inspections using checklists | Green ≥ 85%, Amber 70–84%, Red < 70% | `#kpi-avg-score` |
| 6 | Outdated Checklists | Integer | Checklists not updated in > 12 months | Red > 3, Amber 1–3, Green = 0 | `#kpi-outdated` |

---

## 5. Sections

### 5.1 Tab Navigation

Three tabs:
1. **Checklist Library** — All checklist templates
2. **Builder** — Create/edit checklist (active workspace)
3. **Usage Analytics** — Which checklists are used, scores, common failures

### 5.2 Tab 1: Checklist Library

**Card grid (2 columns) + table toggle:**

```
┌─────────────────────────────────────────┐
│ 📋 CBSE Affiliation Readiness          │
│ Category: Affiliation · Items: 42       │
│ Version: 3.2 · Updated: 15 Jan 2026    │
│ Status: ✅ Active · Used: 24 times      │
│ Avg Score: 78%                          │
│ [Edit] [Clone] [View History] [Archive] │
└─────────────────────────────────────────┘
```

**Table view:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Checklist Name | Text (link) | Yes | — |
| Category | Badge | Yes | Affiliation / Safety / Academic / Infrastructure / Hygiene / Transport / Comprehensive / Custom |
| Items | Integer | Yes | Total items count |
| Sections | Integer | Yes | Grouped sections count |
| Version | Text | Yes | e.g., 3.2 |
| Last Updated | Date | Yes | — |
| Status | Badge | Yes | Draft / Pending Approval / Active / Archived |
| Times Used | Integer | Yes | Inspections using this checklist |
| Avg Score | Percentage | Yes | Average compliance score |
| Lowest Item | Text | No | Item with lowest compliance across inspections |
| Actions | Buttons | No | [Edit] [Clone] [Archive] [Delete (draft only)] |

### 5.3 Tab 2: Builder

**Split-pane workspace:**

Left pane (40%): Section/item tree with drag-and-drop reordering
Right pane (60%): Item editor for selected item

**Section/item tree:**
```
📁 1. General Information (5 items)
  ├── 1.1 School recognition certificate displayed
  ├── 1.2 Affiliation number displayed at entrance
  ├── 1.3 Contact details board visible
  ├── 1.4 Fee structure displayed
  └── 1.5 Anti-ragging signage displayed
📁 2. Infrastructure (12 items)
  ├── 2.1 Classroom size ≥ 500 sq.ft [Critical]
  ├── 2.2 Teacher-student ratio ≤ 1:30 [Critical]
  ...
📁 3. Safety (8 items)
  ...
```

**Item editor (right pane):**
- Item number (auto-generated from position)
- Item text (textarea — the actual checklist statement)
- Category (inherited from section)
- Weight (dropdown): Critical (10x) / Important (5x) / Standard (1x)
- Response type (radio):
  - Compliant / Non-compliant / Partial / N/A
  - Yes / No / N/A
  - Rating 1–5
  - Numeric value (with threshold)
  - Text observation
- Evidence required (radio): None / Photo / Document / Photo + Document
- Applicable to (checkboxes): All branches / Day school only / Hostel branches / Transport branches / Primary only / Secondary only / Senior secondary only
- Reference (text — regulatory norm reference, e.g., "CBSE Affiliation Bye-Laws, Clause 3.4.2")
- Guidance notes (textarea — instructions for inspector on how to evaluate this item)
- Failure consequence (text — what happens if non-compliant, e.g., "Affiliation at risk")

### 5.4 Tab 3: Usage Analytics

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Checklist | Text | Yes | — |
| Times Used | Integer | Yes | — |
| Avg Score | Percentage | Yes | — |
| Item with Lowest Score | Text | No | Most frequently non-compliant item |
| Failure Rate (%) | Percentage | Yes | Percentage of inspections where this item was non-compliant |
| Most Common Finding | Text | No | Finding most often generated |
| Branches Below 70% | Integer | Yes | Count of branches scoring < 70% |

---

## 6. Drawers & Modals

### 6.1 Modal: `create-checklist` (640px)

- **Title:** "Create Inspection Checklist"
- **Fields:**
  - Checklist name (text, required — e.g., "CBSE Affiliation Readiness v4.0")
  - Category (dropdown): Affiliation / Safety / Academic / Infrastructure / Hygiene / Transport / Comprehensive / Custom
  - Description (textarea)
  - Applicable inspection types (checkboxes)
  - Start from (radio):
    - Blank — empty checklist
    - Clone existing — select existing checklist as base
    - Import — upload JSON/CSV template
    - Regulatory template — auto-populate from built-in regulatory norms:
      - CBSE Affiliation Bye-Laws 2024
      - RTE Infrastructure Norms
      - Fire Safety (NBC 2016)
      - NAAC Self-Study (colleges)
      - State Board [select state]
  - Version (auto: 1.0 for new, incremented for updates)
- **Buttons:** Cancel · Create Draft
- **Post-action:** Opens Tab 2 (Builder) with new checklist loaded
- **Access:** Role 123, 121

### 6.2 Drawer: `checklist-detail` (720px, right-slide)

- **Title:** "Checklist — [Name] · Version [X.Y]"
- **Tabs:** Items · Usage History · Version History · Analytics
- **Items tab:** Full checklist in read-only mode — all sections, items, weights, evidence requirements
- **Usage History tab:** List of inspections that used this checklist — date, branch, score
- **Version History tab:** All versions with change log — what items were added/removed/modified
- **Analytics tab:** Per-item compliance rate across all inspections — identifying weakest items
- **Footer:** [Edit] [Clone] [Export PDF] [Export JSON]
- **Access:** G1+ (Division P roles)

### 6.3 Modal: `approve-checklist` (480px, Role 121/G4+)

- **Title:** "Approve Checklist — [Name]"
- **Content:** Checklist summary: name, category, item count, sections, changes from previous version (diff)
- **Actions:** Approve / Request Revision (with notes) / Reject
- **Access:** Role 121, G4+

### 6.4 Modal: `import-template` (480px)

- **Title:** "Import Checklist Template"
- **Fields:**
  - File (JSON/CSV/Excel upload)
  - Format preview (auto-detected columns mapped to: Item text, Section, Weight, Evidence)
  - Mapping configuration (if column names differ)
- **Buttons:** Cancel · Import
- **Access:** Role 123, 121

---

## 7. Charts

### 7.1 Checklist Usage Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Checklist Usage — FY to Date" |
| Data | COUNT(inspections) per checklist template |
| Centre text | Total inspections: N |
| API | `GET /api/v1/group/{id}/audit/checklists/analytics/usage-distribution/` |

### 7.2 Item Failure Rate (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Top 15 Most Failed Items — Across All Inspections" |
| Data | Failure rate (%) per item, top 15 |
| Colour | Red > 50%, Amber 25–50%, Green < 25% |
| API | `GET /api/v1/group/{id}/audit/checklists/analytics/failure-rates/` |

### 7.3 Score Trend by Checklist Type (Line)

| Property | Value |
|---|---|
| Chart type | Multi-line |
| Title | "Average Inspection Score — Monthly Trend by Checklist Type" |
| Data | AVG score per month per checklist category |
| API | `GET /api/v1/group/{id}/audit/checklists/analytics/score-trend/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Checklist created | "Checklist '[Name]' created — version 1.0 (draft)" | Success | 3s |
| Checklist submitted | "Checklist '[Name]' submitted for approval" | Info | 3s |
| Checklist approved | "Checklist '[Name]' approved — now active" | Success | 4s |
| Checklist revision requested | "Checklist '[Name]' — revision requested: [Notes]" | Warning | 5s |
| Item added | "Item added to section [N]" | Info | 2s |
| Item deleted | "Item removed from checklist" | Info | 2s |
| Checklist cloned | "Checklist cloned from '[Source]'" | Success | 3s |
| Template imported | "Template imported — [N] items loaded" | Success | 3s |
| Checklist archived | "Checklist '[Name]' archived" | Info | 3s |
| Outdated alert | "⚠️ Checklist '[Name]' not updated in [N] months" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No checklists | 📋 | "No Checklists Created" | "Create your first inspection checklist to standardise branch audits." | Create Checklist |
| No items in checklist | ➕ | "Empty Checklist" | "Add sections and items to build your inspection checklist." | Add Section |
| No usage data | 📊 | "No Usage Data" | "Analytics will appear after checklists are used in inspections." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + card grid skeleton |
| Checklist library | Card grid or table skeleton |
| Builder workspace | Split-pane skeleton: tree + editor |
| Checklist detail drawer | 720px skeleton: 4 tabs |
| Analytics tab | Chart placeholders |
| Import processing | Progress bar with step indicator |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit/checklists/` | G1+ | List all checklists |
| GET | `/api/v1/group/{id}/audit/checklists/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/audit/checklists/{checklist_id}/` | G1+ | Checklist detail with items |
| POST | `/api/v1/group/{id}/audit/checklists/` | 123, 121 | Create checklist |
| PUT | `/api/v1/group/{id}/audit/checklists/{checklist_id}/` | 123, 121 | Update checklist |
| PATCH | `/api/v1/group/{id}/audit/checklists/{checklist_id}/status/` | 121, G4+ | Approve/archive/activate |
| POST | `/api/v1/group/{id}/audit/checklists/{checklist_id}/clone/` | 123, 121 | Clone checklist |
| DELETE | `/api/v1/group/{id}/audit/checklists/{checklist_id}/` | 121 | Delete (draft only) |
| POST | `/api/v1/group/{id}/audit/checklists/{checklist_id}/items/` | 123, 121 | Add item |
| PUT | `/api/v1/group/{id}/audit/checklists/{checklist_id}/items/{item_id}/` | 123, 121 | Update item |
| DELETE | `/api/v1/group/{id}/audit/checklists/{checklist_id}/items/{item_id}/` | 123, 121 | Delete item |
| PATCH | `/api/v1/group/{id}/audit/checklists/{checklist_id}/items/reorder/` | 123, 121 | Reorder items |
| POST | `/api/v1/group/{id}/audit/checklists/import/` | 123, 121 | Import template |
| GET | `/api/v1/group/{id}/audit/checklists/{checklist_id}/versions/` | G1+ | Version history |
| GET | `/api/v1/group/{id}/audit/checklists/{checklist_id}/usage/` | G1+ | Usage history |
| GET | `/api/v1/group/{id}/audit/checklists/analytics/usage-distribution/` | G1+ | Usage donut |
| GET | `/api/v1/group/{id}/audit/checklists/analytics/failure-rates/` | G1+ | Failure rate bar |
| GET | `/api/v1/group/{id}/audit/checklists/analytics/score-trend/` | G1+ | Score trend line |
| GET | `/api/v1/group/{id}/audit/checklists/regulatory-templates/` | G1+ | List built-in regulatory templates |
| GET | `/api/v1/group/{id}/audit/checklists/export/` | G1+ | Export all checklists |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../checklists/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#checklist-content` | `innerHTML` | `hx-trigger="click"` |
| Checklist detail drawer | Card/row click | `hx-get=".../checklists/{id}/"` | `#right-drawer` | `innerHTML` | 720px drawer |
| Create checklist | Form submit | `hx-post=".../checklists/"` | `#create-result` | `innerHTML` | Redirects to builder tab |
| Add item | Button click in builder | `hx-post=".../checklists/{id}/items/"` | `#item-tree` | `innerHTML` | Appends to tree |
| Update item | Form change in editor | `hx-put=".../checklists/{id}/items/{item_id}/"` | `#item-{id}` | `outerHTML` | Debounced auto-save |
| Delete item | Delete button | `hx-delete=".../checklists/{id}/items/{item_id}/"` | `#item-{id}` | `outerHTML` | Confirm dialog first |
| Reorder (drag-drop) | Drag-drop in tree | `hx-patch=".../checklists/{id}/items/reorder/"` | `#item-tree` | `innerHTML` | JS drag → HTMX |
| Approve | Button click | `hx-patch=".../checklists/{id}/status/"` | `#status-badge` | `innerHTML` | Toast |
| Clone | Button click | `hx-post=".../checklists/{id}/clone/"` | `#clone-result` | `innerHTML` | Toast + redirect |
| Import | File submit | `hx-post=".../checklists/import/"` | `#import-result` | `innerHTML` | Progress bar |
| Chart load | Tab 3 shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
