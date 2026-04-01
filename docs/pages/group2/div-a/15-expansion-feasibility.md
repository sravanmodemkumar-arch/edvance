# 15 — Expansion Feasibility

> **URL:** `/group/gov/expansion/`
> **File:** `15-expansion-feasibility.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Chairman G5 · MD G5 · CEO G4 (full) · Advisor G1 (read + download)

---

## 1. Purpose

Data-driven tool for evaluating the viability of opening new branches in target locations.
Each feasibility study collects demographic, competitive, and financial data for a proposed
location and produces a structured recommendation for the Chairman.

Key inputs per study: Population data, student-age cohort, existing competitor schools, demand
signals (inquiry volume, local govt plans), and projected financial break-even.

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| Chairman | Full — create, view, approve/proceed | Final decision maker |
| MD | Full — create, edit, publish | Study author |
| CEO | Full — create, edit | |
| Advisor | Read-only + download report | Research role |
| Others | ❌ | President/VP/Trustee cannot access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Expansion Feasibility
```

### 3.2 Page Header
```
Expansion Feasibility Studies                          [+ New Study]  [Export All ↓]
[N] studies · [N] completed · [N] in progress         (Chairman/MD/CEO only)
```

---

## 4. Studies Table

**Search:** Location name, district, state. Debounce 300ms.

**Filters:** Status (Draft/In Progress/Complete/Archived) · State · Recommendation · Year.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Location | Text + link | ✅ | City/Town + District |
| State | Badge | ✅ | |
| Study Status | Badge | ✅ | Draft · In Progress · Complete · Archived |
| Demand Score | Number + bar | ✅ | 0–100 · Green >70 · Yellow 40–70 · Red <40 |
| Competition | Badge | ✅ | Low · Medium · High |
| Population (catchment) | Number | ✅ | |
| Est. Enrollment Y1 | Number | ✅ | Projected Year 1 |
| Break-even (months) | Number | ✅ | |
| Recommendation | Badge | ✅ | ✅ Proceed · ⚠ Conditional · ❌ Not Recommended |
| Last Updated | Date | ✅ | |
| Actions | — | ❌ | View · Edit · Delete · Download Report |

**Default sort:** Demand Score descending (highest opportunity first).

**Pagination:** 25/page.

**Row actions:**
| Action | Visible To | Notes |
|---|---|---|
| View | All | Opens `expansion-study-view` drawer |
| Edit | Chairman/MD/CEO | Opens study form drawer |
| Delete | Chairman/MD | Confirm modal |
| Download Report | All | PDF of complete study |

---

## 5. Drawers & Modals

### 5.1 Drawer: `expansion-study-create` / `expansion-study-edit`
- **Trigger:** [+ New Study] or Edit row action
- **Width:** 760px
- **Tabs:** Location · Demographics · Competition · Financials · Recommendation

#### Tab: Location
| Field | Type | Required | Validation |
|---|---|---|---|
| Study Name | Text | ✅ | e.g. "Guntur North — Phase 2" |
| City / Town | Text | ✅ | |
| District | Text | ✅ | |
| State | Select | ✅ | Indian states |
| Pincode | Text | ✅ | 6 digits |
| GPS Coordinates | Text | ❌ | lat,lng format |
| Site Availability | Select | ✅ | Owned · Lease Under Negotiation · Not Identified |
| Site Area (sq ft) | Number | ❌ | |
| Study Initiated By | Text | ❌ | Auto-filled with current user |
| Study Date | Date | ✅ | |

#### Tab: Demographics
| Field | Type | Required | Validation |
|---|---|---|---|
| Total Population (catchment 10km) | Number | ✅ | |
| Student-age Population (6–18 yrs) | Number | ✅ | |
| Est. School-going Children | Number | ✅ | |
| Income Group Mix | Multi-select | ✅ | Lower · Middle · Upper-Middle · High |
| Language Medium Demand | Multi-select | ✅ | Telugu · English · Hindi |
| Notes | Textarea | ❌ | Max 500 chars |

#### Tab: Competition
**Table (add rows):** School Name · Board · Enrollment · Fee Range · Distance from Site · Reputation (1–5 stars).

**[+ Add Competitor]** button adds a new row to the table.

Competition summary:
| Field | Value |
|---|---|
| Total competitor schools in 10km | [auto-counted] |
| Market leader | [name] with [N] students |
| Avg competitor fee | ₹[amount]/year |
| Estimated total served demand | [N] students |
| Estimated unserved demand | [N] students (calculated) |

#### Tab: Financials
| Field | Type | Required | Validation |
|---|---|---|---|
| Setup Cost (Infrastructure) | Currency | ✅ | |
| Year 1 Operating Cost | Currency | ✅ | |
| Year 2 Operating Cost | Currency | ✅ | |
| Year 3 Operating Cost | Currency | ✅ | |
| Projected Enrollment Y1 | Number | ✅ | |
| Projected Enrollment Y2 | Number | ✅ | |
| Projected Enrollment Y3 | Number | ✅ | |
| Proposed Fee Structure | Currency/year | ✅ | |
| Projected Revenue Y1 | Auto-calc | — | Enrollment × Fee |
| Projected Revenue Y2 | Auto-calc | — | |
| Projected Revenue Y3 | Auto-calc | — | |
| Break-even Month | Auto-calc | — | When cumulative revenue > total cost |

**Financial projection chart (inline preview):** Bar chart — Revenue vs Cost per year (Y1–Y3), break-even line.

#### Tab: Recommendation
| Field | Type | Required | Validation |
|---|---|---|---|
| Demand Score | Number 0–100 | ✅ | Auto-suggested from demographics/competition data; editable |
| Competition Level | Select | ✅ | Low · Medium · High |
| Risk Level | Select | ✅ | Low · Medium · High |
| Recommendation | Select | ✅ | Proceed · Conditional · Not Recommended |
| Conditions (if Conditional) | Textarea | Conditional | Required if Conditional |
| Risk Factors | Textarea | ✅ | Min 50 chars |
| Executive Summary | Textarea | ✅ | Min 100 chars, max 1000 |

**Submit:** "Save Study" — saves all tabs as draft. "Mark Complete" button appears when all tabs filled.

### 5.2 Modal: `study-delete-confirm`
- **Width:** 420px
- **Fields:** Reason (optional) — "This study will be archived, not permanently deleted"
- **Buttons:** [Archive Study] (primary) + [Cancel]

### 5.3 Drawer: `expansion-study-view` (read-only — for G1 Advisor)
- Same tabs as edit — all fields disabled, no edit icons

---

## 6. Charts

### 6.1 Demand vs Competition Matrix (Scatter)
- **Type:** Scatter chart
- **X-axis:** Competition Level (Low=1, Medium=2, High=3)
- **Y-axis:** Demand Score (0–100)
- **Each point:** One study location (labelled with city name)
- **Quadrant labels:** Top-left = "High Opportunity" (high demand, low competition) · Top-right = "Competitive Market" · Bottom = "Low Priority"
- **Tooltip:** Location · Demand: N · Competition: [Low/Med/High] · Recommendation
- **Export:** PNG

### 6.2 Financial Projection Chart (per study — in drawer)
- **Type:** Grouped bar + line
- **Bars:** Revenue (green) and Cost (red) per year
- **Line:** Cumulative net (break-even crosses zero)
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Study saved | "Feasibility study for [Location] saved" | Success | 4s |
| Study completed | "Study marked complete. Chairman notified." | Success | 4s |
| Study deleted/archived | "Study archived" | Info | 4s |
| Report downloaded | "Feasibility report downloading…" | Info | 4s |
| Competitor row added | "Competitor added to study" | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No studies | "No feasibility studies" | "Start a study for a potential new branch location" | [+ New Study] |
| No results (search) | "No studies match" | "Try different search terms" | [Clear Search] |
| Advisor — no studies | "No completed studies available" | "Completed feasibility studies will appear here" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: table (8 rows) |
| Study drawer open | Spinner in drawer, tab contents skeleton |
| Financial projection auto-calc | Shimmer on financial summary cards |
| PDF download | Spinner in download button |
| Scatter chart load | Chart area spinner |

---

## 10. Role-Based UI Visibility

| Element | Chairman/MD/CEO | Advisor G1 | Others |
|---|---|---|---|
| [+ New Study] | ✅ | ❌ | ❌ |
| Edit row action | ✅ | ❌ | ❌ |
| Delete / Archive | ✅ | ❌ | ❌ |
| Mark Complete button | ✅ | ❌ | ❌ |
| Download Report | ✅ | ✅ | ❌ |
| View (read-only) | ✅ | ✅ | ❌ |
| Scatter chart | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/expansion/` | JWT | All studies |
| POST | `/api/v1/group/{id}/expansion/` | JWT (G4/G5) | Create study |
| GET | `/api/v1/group/{id}/expansion/{sid}/` | JWT | Study detail |
| PUT | `/api/v1/group/{id}/expansion/{sid}/` | JWT (G4/G5) | Update study |
| POST | `/api/v1/group/{id}/expansion/{sid}/complete/` | JWT (G4/G5) | Mark complete |
| DELETE | `/api/v1/group/{id}/expansion/{sid}/` | JWT (G5/G4) | Archive study |
| GET | `/api/v1/group/{id}/expansion/{sid}/report/` | JWT | Download PDF report |
| GET | `/api/v1/group/{id}/expansion/scatter-chart/` | JWT | Scatter chart data |

---

## HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search studies | `input delay:300ms` | GET `.../expansion/?q=` | `#expansion-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../expansion/?status=&recommendation=&state=` | `#expansion-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../expansion/?sort=&dir=` | `#expansion-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../expansion/?page=` | `#expansion-table-section` | `innerHTML` |
| Open study create drawer | `click` | GET `.../expansion/new/` | `#drawer-body` | `innerHTML` |
| Open study detail / view drawer | `click` | GET `.../expansion/{sid}/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch | `click` | GET `.../expansion/{sid}/?tab=location\|demographics\|competition\|financials\|recommendation` | `#expansion-drawer-tab` | `innerHTML` |
| Add competitor row | `click` | GET `.../expansion/competitor-row/` | `#competitors-table-body` | `beforeend` |
| Financials auto-recalculate | `change` | GET `.../expansion/{sid}/financials/estimate/?inputs=` | `#financials-projections` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
