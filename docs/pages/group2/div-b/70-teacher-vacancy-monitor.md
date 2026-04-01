# 70 — Teacher Adequacy & Vacancy Monitor

> **URL:** `/group/acad/teacher-vacancies/`
> **File:** `70-teacher-vacancy-monitor.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Director G3 (full) · CAO G4 (view + escalate) · Stream Coordinators G3 (own stream)

---

## 1. Purpose

Tracks unfilled teacher positions across all branches and subjects. Distinct from Teaching Load Monitor
(Page 53) which handles overload (too many periods for filled positions). This page handles **shortages**:
vacancies, subject-level gaps, and how they are being covered (or not).

A large group with 50 branches and 3,000+ teachers will have 50–150 vacancies at any point. Critical
subject vacancies (Maths, Physics, Chemistry, Biology) left uncovered for >30 days directly impact student
outcomes and require Academic Director escalation.

---

## 2. Role Access

| Role | Level | Can View | Can Escalate | Can Export | Notes |
|---|---|---|---|---|---|
| Academic Director | G3 | ✅ All branches | ✅ | ✅ | Primary owner |
| CAO | G4 | ✅ All branches | ✅ (to HR/Chairman) | ✅ | View + escalate critical |
| Stream Coord MPC | G3 | ✅ MPC subjects | ❌ | ✅ | Own stream only |
| Stream Coord BiPC | G3 | ✅ BiPC subjects | ❌ | ✅ | Own stream only |
| Stream Coord MEC/CEC | G3 | ✅ MEC/CEC subjects | ❌ | ✅ | Own stream only |
| Stream Coord HEC | G3 | ✅ HEC subjects | ❌ | ✅ | Own stream only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Teacher Vacancy Monitor
```

### 3.2 Page Header
```
Teacher Adequacy & Vacancy Monitor                    [Export CSV ↓]  [Escalate to HR]
AY 2025–26 · As of [Today's Date]
```

### 3.3 Summary Stats Bar

| Stat | Value | Color |
|---|---|---|
| Sanctioned Posts | 3,450 | — |
| Filled Posts | 3,287 | — |
| Total Vacancies | 163 | Orange |
| Vacancy % | 4.7% | — |
| Critical Vacancies (>20% in subject) | 12 | Red |
| Branches with 0 Vacancies | 23 | Green |
| Avg Days Vacant | 47 | — |

---

## 4. Main Table

### 4.1 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text + link | ✅ | Opens branch detail |
| Subject | Badge | ✅ | Subject name |
| Stream | Badge | ✅ | MPC / BiPC / MEC / HEC / Common |
| Class Level | Badge | ✅ | Lower (6–8) · Middle (9–10) · Senior (11–12) |
| Sanctioned | Number | ✅ | Total sanctioned posts |
| Filled | Number | ✅ | Posts with confirmed teacher |
| Vacant | Number | ✅ | Unfilled posts |
| Vacancy % | Progress bar | ✅ | Red if > 20%, Amber 10–20% |
| Longest Vacant (days) | Number | ✅ | Max days any one post has been vacant |
| Covering Arrangement | Badge | ✅ | Guest Faculty · Peer Cover · None |
| Actions | — | ❌ | View Detail |

### 4.2 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | Branch names |
| Subject | Multi-select | All subjects |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / HEC / Common |
| Severity | Select | Critical (>20%) · Moderate (10–20%) · Low (<10%) |
| Covering | Multi-select | Guest Faculty · Peer Cover · None (uncovered) |
| Days Vacant | Range | Min–Max days |

### 4.3 Search
- Full-text across branch name, subject name
- 300ms debounce

### 4.4 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Escalate Selected | Academic Director · CAO | Creates escalation record, notifies HR |
| Export Selected | All with export | CSV of selected rows |

---

## 5. Drawers

### 5.1 Drawer: `vacancy-detail`
- **Trigger:** View row action
- **Width:** 560px

| Section | Content |
|---|---|
| **Header** | Branch · Subject · Stream · Class level |
| **Sanctioned vs Filled** | Gauge: N/M filled |
| **Vacancy Timeline** | Date first vacant · Days vacant · Escalation history |
| **Covering plan** | Type · Covering teacher/arrangement · Effective from · Planned end |
| **Impact** | Number of students affected · Sections without permanent teacher |
| **Escalation history** | List: Date · Escalated by · Action taken |
| **Actions** | [Mark Filled] · [Update Covering Plan] · [Escalate] |

### 5.2 Modal: `escalate-confirm`
- **Width:** 480px
- **Content:** "Escalate [Subject] vacancy at [Branch] to HR?"
- **Fields:** Reason · Priority (Critical / High / Medium) · Notify Chairman? (checkbox)
- **Buttons:** [Escalate] · [Cancel]
- **On confirm:** Escalation record created · HR notified · Audit entry

---

## 6. Alert Logic

| Condition | Alert | Recipient |
|---|---|---|
| New vacancy > 20% in core subject | In-app badge | Academic Director |
| Vacancy uncovered for > 30 days | Red row highlight + alert | Academic Director + CAO |
| No covering arrangement set for critical vacancy | ⚠ flag on row | Academic Director |
| Escalation not acted on in 14 days | Follow-up alert | CAO |

---

## 7. Charts

### 7.1 Vacancy by Subject (Bar)
- **Type:** Horizontal bar chart
- **Data:** Vacancy count per subject
- **Color:** Red if > 20% vacancy rate
- **Export:** PNG

### 7.2 Vacancy by Branch (Map / Bar)
- **Type:** Horizontal bar chart (sorted by vacancy %)
- **Export:** PNG

### 7.3 Vacancy Trend (Line)
- **Type:** Line chart
- **X-axis:** Months (last 6 months)
- **Y-axis:** Total vacancies
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Escalation created | "Vacancy escalated to HR. [Name] notified." | Success | 4s |
| Vacancy marked filled | "[Subject] at [Branch] marked filled." | Success | 4s |
| Covering plan updated | "Covering plan updated." | Success | 3s |
| Export started | "Export preparing…" | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No vacancies | "No vacancies found" | "All sanctioned teacher posts are filled." |
| Filter returns empty | "No vacancies match filters" | "Try clearing filters." |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + 8 table rows |
| Filter/sort/search | Inline skeleton rows |
| Vacancy detail drawer | Spinner + skeleton content |
| Chart render | Spinner in chart area |

---

## 11. Role-Based UI Visibility

| Element | Academic Dir G3 | CAO G4 | Stream Coords G3 |
|---|---|---|---|
| All branches | ✅ | ✅ | ❌ Own stream only |
| [Escalate to HR] | ✅ | ✅ | ❌ |
| [Mark Filled] (in drawer) | ✅ | ❌ | ❌ |
| [Update Covering Plan] | ✅ | ❌ | ❌ |
| Charts | ✅ | ✅ | ✅ (own stream) |
| Export | ✅ | ✅ | ✅ (own stream) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/teacher-vacancies/` | JWT (G3+) | Vacancy list (filtered/paginated) |
| GET | `/api/v1/group/{id}/acad/teacher-vacancies/stats/` | JWT (G3+) | Summary stats bar |
| GET | `/api/v1/group/{id}/acad/teacher-vacancies/{vid}/` | JWT (G3+) | Vacancy detail |
| PUT | `/api/v1/group/{id}/acad/teacher-vacancies/{vid}/` | JWT (G3, AcadDir) | Update vacancy / covering plan |
| POST | `/api/v1/group/{id}/acad/teacher-vacancies/{vid}/escalate/` | JWT (G3+) | Escalate vacancy |
| POST | `/api/v1/group/{id}/acad/teacher-vacancies/{vid}/mark-filled/` | JWT (G3, AcadDir) | Mark vacancy filled |
| GET | `/api/v1/group/{id}/acad/teacher-vacancies/charts/by-subject/` | JWT (G3+) | Subject vacancy chart |
| GET | `/api/v1/group/{id}/acad/teacher-vacancies/charts/by-branch/` | JWT (G3+) | Branch vacancy chart |
| GET | `/api/v1/group/{id}/acad/teacher-vacancies/charts/trend/` | JWT (G3+) | Trend chart data |
| GET | `/api/v1/group/{id}/acad/teacher-vacancies/export/?format=csv` | JWT (G3+) | Export CSV |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Table search | `input delay:300ms` | GET `.../teacher-vacancies/?q=` | `#vacancy-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../teacher-vacancies/?filters=` | `#vacancy-section` | `innerHTML` |
| Sort column | `click` | GET `.../teacher-vacancies/?sort=` | `#vacancy-section` | `innerHTML` |
| Pagination | `click` | GET `.../teacher-vacancies/?page=` | `#vacancy-section` | `innerHTML` |
| View detail drawer | `click` | GET `.../teacher-vacancies/{id}/` | `#drawer-body` | `innerHTML` |
| Mark filled | `click` | POST `.../mark-filled/` | `#vacancy-row-{id}` | `outerHTML` |
| Escalate confirm | `click` | POST `.../escalate/` | `#escalate-modal-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
