# 66 — Stream Coordinator HEC Dashboard

> **URL:** `/group/acad/stream/hec/`
> **File:** `66-stream-hec-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Stream Coord — HEC G3 (full) · CAO G4 (view) · Academic Director G3 (view)

---

## 1. Purpose

Post-login landing page for the Group Stream Coordinator — HEC (Humanities, Economics, Commerce).
Provides a command view of all branches offering HEC-stream subjects (History, Economics, Civics, Commerce,
Accounts, Political Science, Sociology) across the institution group.

HEC is the humanities and commerce stream offered at Class 11–12 level. A large group may have 15–25 branches
with HEC, each with 1–3 sections per class. The Stream Coordinator owns curriculum quality, teaching standards,
and performance tracking for all HEC subjects across the group.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Edit | Notes |
|---|---|---|---|---|
| Stream Coord — HEC | G3 | ✅ Full dashboard | ✅ Upload content, flag branches | Own role post-login page |
| CAO | G4 | ✅ Read-only summary | ❌ | Via cross-role nav |
| Academic Director | G3 | ✅ Read-only summary | ❌ | Via cross-role nav |
| Other Stream Coords | G3 | ❌ | ❌ | No cross-stream access |
| MIS Officer | G1 | ❌ | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Stream HEC Dashboard
```

### 3.2 Page Header
```
HEC Stream Dashboard                          [Upload Lesson Plan Template]  [Export Report ↓]
[Group Name] · Humanities, Economics & Commerce · [N] branches · AY 2025–26
```

### 3.3 Summary Stats Bar

| Stat | Value | Notes |
|---|---|---|
| HEC Branches | 22 | Branches actively running HEC |
| Total HEC Students | 8,430 | Across all classes |
| Class 11 Sections | 38 | Active sections |
| Class 12 Sections | 35 | Active sections |
| Branches On Track | 19 | Syllabus coverage ≥ 85% |
| Branches Critical | 3 | Syllabus coverage < 70% |

---

## 4. Main Widgets

### 4.1 Syllabus Coverage by Branch (Primary Widget)
- **Type:** Horizontal bar chart
- **X-axis:** % Syllabus completed (current term)
- **Y-axis:** Branch names
- **Color:** Green ≥ 85% · Amber 70–84% · Red < 70%
- **Click:** Opens branch syllabus detail drawer

### 4.2 Subject Performance Heatmap
- **Type:** Grid heatmap
- **Rows:** Branches
- **Columns:** HEC subjects (Economics, History, Commerce, Accounts, Civics, Political Science, Sociology)
- **Cell value:** Average marks % in last internal exam
- **Color scale:** Dark green (90%+) → Red (<40%)
- **Click:** Drill into branch × subject detail

### 4.3 Toppers in HEC Stream

| Column | Type | Notes |
|---|---|---|
| Rank | Number | Cross-group HEC rank |
| Student Name | Text + masked | Masked to initials for privacy |
| Branch | Text | |
| Class | Text | 11 or 12 |
| Score % | Number | Overall HEC subjects avg |
| Improvement | Badge | ↑↓ vs previous term |

- **Rows:** Top 10 across group
- **CTA:** [View Full Topper List →] → Page 31

### 4.4 Low Performer Alert List

| Column | Type | Notes |
|---|---|---|
| Student | Text (masked) | Initials only |
| Branch | Text | |
| Weakest Subject | Badge | Subject with lowest marks |
| Score % | Number | Red if < 40% |
| Status | Badge | At Risk · Remedial Enrolled · Improved |

- **Threshold:** Students below 40% in any HEC subject
- **CTA per row:** [Flag for Remedial] → triggers notification to branch

### 4.5 Teacher Vacancies (HEC Subjects)
- **Type:** Compact alert list
- **Content:** Branch · Subject · Days Vacant · Covering Arrangement
- **Link:** [View All Vacancies →] → Page 70

### 4.6 Pending Content Reviews
- **Type:** Count badge + compact list
- **Content:** Files in Content Library (Page 17) awaiting review from HEC stream coordinator
- **CTA:** [Review Now →] → Page 21 filtered to HEC

### 4.7 Lesson Plan Compliance
- **Type:** Donut chart
- **Data:** Branches that have uploaded lesson plans this week vs. branches that haven't
- **Tooltip:** Branch name · Last uploaded
- **CTA:** [Send Reminder] → WhatsApp/portal notification to non-compliant branches

---

## 5. Branch Detail Drawer

**Trigger:** Click any branch row in heatmap or coverage chart
**Drawer:** `hec-branch-detail`
**Width:** 640px

### Tabs

**Tab: Syllabus**
- Subject × Chapter completion grid
- Planned vs actual completion date per chapter
- Link: [Open Chapter Progress Tracker →] → Page 75

**Tab: Performance**
- Last 3 exam results per HEC subject
- Class-wise breakdown (11 / 12)
- Term trend mini chart

**Tab: Teachers**
- HEC subject teachers assigned
- Vacancies flagged in red
- Link: [Open Assignment Matrix →] → Page 76

**Tab: Content**
- Content uploaded by this branch for HEC
- Review status (Approved / Pending / Rejected)

---

## 6. Charts

### 6.1 Enrollment by Class (HEC)
- **Type:** Stacked bar per branch
- **Segments:** Class 11 · Class 12
- **Tooltip:** Branch · Class 11: N · Class 12: N
- **Export:** PNG

### 6.2 Subject Pass Rate Trend (Last 3 Terms)
- **Type:** Multi-line chart
- **Lines:** One per HEC subject
- **X-axis:** Terms (T1 2024–25, T2 2024–25, T3 2024–25, T1 2025–26)
- **Y-axis:** Pass %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Content approved | "Content '[Name]' approved for HEC stream" | Success | 4s |
| Branch flagged for remedial | "Branch [Name] flagged. Branch Principal notified." | Info | 4s |
| Reminder sent | "Lesson plan reminder sent to [N] branches" | Success | 4s |
| Export triggered | "Report preparing… download will start shortly" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No HEC branches | "No HEC branches found" | "No branches in this group offer the HEC stream" | [Contact Admin] |
| No recent exam data | "No exam results yet" | "Results will appear after the first internal exam is published" | [Go to Exam Calendar] |
| No teacher vacancies | "All HEC positions filled" | "No open teacher vacancies in HEC subjects" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + 4 widget placeholders |
| Subject heatmap load | Spinner in heatmap area |
| Branch detail drawer open | Spinner + skeleton tabs |
| Chart render | Spinner in chart area |

---

## 10. Role-Based UI Visibility

| Element | HEC Stream Coord G3 | CAO G4 | Academic Director G3 |
|---|---|---|---|
| [Upload Lesson Plan Template] | ✅ | ❌ | ❌ |
| [Flag for Remedial] per row | ✅ | ❌ | ❌ |
| [Send Reminder] (lesson plans) | ✅ | ❌ | ❌ |
| [Export Report] | ✅ | ✅ | ✅ |
| Low performer student names | Masked (initials) | Masked | Masked |
| Full heatmap with drill-down | ✅ | ✅ Read | ✅ Read |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/stream/hec/dashboard/` | JWT (G3+) | Dashboard summary stats |
| GET | `/api/v1/group/{id}/acad/stream/hec/syllabus-coverage/` | JWT (G3+) | Branch-wise coverage data |
| GET | `/api/v1/group/{id}/acad/stream/hec/heatmap/` | JWT (G3+) | Subject performance heatmap |
| GET | `/api/v1/group/{id}/acad/stream/hec/toppers/` | JWT (G3+) | Top 10 HEC students |
| GET | `/api/v1/group/{id}/acad/stream/hec/low-performers/` | JWT (G3+) | Students below threshold |
| GET | `/api/v1/group/{id}/acad/stream/hec/vacancies/` | JWT (G3+) | Teacher vacancy data |
| GET | `/api/v1/group/{id}/acad/stream/hec/branches/{bid}/` | JWT (G3+) | Branch detail (all tabs) |
| POST | `/api/v1/group/{id}/acad/stream/hec/branches/{bid}/flag-remedial/` | JWT (G3) | Flag branch for remedial |
| POST | `/api/v1/group/{id}/acad/stream/hec/lesson-plan-reminder/` | JWT (G3) | Send reminder to branches |
| GET | `/api/v1/group/{id}/acad/stream/hec/charts/pass-trend/` | JWT (G3+) | Pass rate trend chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Page load stats | `load` | GET `.../stream/hec/dashboard/` | `#hec-stats-bar` | `innerHTML` |
| Heatmap load | `load` | GET `.../stream/hec/heatmap/` | `#hec-heatmap` | `innerHTML` |
| Heatmap cell click | `click` | GET `.../stream/hec/branches/{id}/` | `#drawer-body` | `innerHTML` |
| Branch coverage bar click | `click` | GET `.../stream/hec/branches/{id}/` | `#drawer-body` | `innerHTML` |
| Flag remedial | `click` | POST `.../flag-remedial/` | `#hec-low-performer-row-{id}` | `outerHTML` |
| Send lesson plan reminder | `click` | POST `.../lesson-plan-reminder/` | `#hec-reminder-btn` | `outerHTML` |
| Export report | `click` | GET `.../stream/hec/export/` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
