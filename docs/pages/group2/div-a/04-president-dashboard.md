# 04 — President Dashboard (Academic)

> **URL:** `/group/gov/president/`
> **File:** `04-president-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group President (Academic) (G4) — exclusive landing page

---

## 1. Purpose

Academic command centre for the Group President (Academic). The President's sole focus is
academic standardization and quality across all branches. Core responsibilities:
- Approve or reject exam schedules submitted by branches
- Detect and resolve exam scheduling conflicts between branches
- Monitor academic performance (scores, curriculum completion, topper lists) cross-branch
- Ensure a student in Branch A competes fairly with Branch B

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group President (Academic) | G4 | Full — all sections, all actions | Exclusive dashboard |
| Chairman / MD | G5 | — | Have own dashboards |
| CEO / VP | G4 | — | Have own dashboards |
| All others | G3/G1 | — | Redirected |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  President Dashboard (Academic)
```

### 3.2 Page Header
```
Academic Oversight — [President Name]                  [Approve All Non-Conflicting ▼]
Group President (Academic) · Last login: [date time]   [Download Topper Report ↓]
```

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Exam Schedules Pending | `4 awaiting approval` · pulsing badge | Red if >0 (requires action) | → Exam Schedule Approval page 18 |
| Avg Score Cross-branch | `72.3%` last exam cycle | Green ≥80% · Yellow 65–80% · Red <65% | → Inter-Branch Benchmarking page 16 |
| Curriculum Completion | `68% of branches on track` | Green ≥90% · Yellow 70–90% · Red <70% | → Benchmarking page 16 |
| Upcoming Exams (30d) | `12 exams` across all branches | Info | → Exam Approval page 18 |
| Toppers Report | `Report ready` or "Generating…" | Info | Download PDF inline |
| NTSE / Olympiad Enrolled | `1,240 students` registered | Info | → Governance Reports page 25 |

---

## 5. Sections

### 5.1 Exam Approval Queue

> Core section — the President's primary daily task.

**Display:** Table with action buttons inline.

**Search:** Exam name, branch name, class name. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation |
| Class | Multi-select | Class 6–12 + Integrated |
| Conflict Status | Select | All · Conflict detected · No conflict |
| Days Pending | Select | Any · 1–3 days · 4–7 days · >7 days |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| Exam Name | Text | ✅ | e.g. "Unit Test 3 — MPC Class 11" |
| Stream / Class | Badge | ✅ | MPC Class 11 |
| Exam Date | Date | ✅ | Red if within 3 days |
| Duration | Text | ❌ | e.g. "3 hours" |
| Question Paper | Badge | ✅ | Ready · Pending · Uploaded |
| Submitted By | Text | ❌ | Branch Exam Controller name |
| Days Pending | Number | ✅ | Red if >5 |
| Conflict? | Badge | ✅ | ✅ No Conflict · ⚠ Conflict Detected |
| Actions | — | ❌ | [Approve] [Reject] [View Details] |

**Conflict badge:** Auto-detected — another branch has an exam for the same stream/class within
3 days. Clicking conflict badge opens conflict timeline in `exam-approval` drawer.

**Bulk approve:** Select multiple non-conflicting rows → [Approve Selected N] header button.
Opens confirm modal listing all selected exams before submitting.

**Default sort:** Conflict status (conflicts first), then Exam Date ascending.

**Pagination:** Server-side · Default 25/page.

---

### 5.2 Academic Performance Overview

> Cross-branch academic performance table — last completed exam cycle.

**Search:** Branch name. Debounce 300ms.

**Filters:** Stream, Class, Date range.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text + link | ✅ | → Branch Detail academic tab |
| Last Exam | Text | ✅ | Exam name |
| Avg Score % | Number + bar | ✅ | Colour-coded |
| Pass % | Number | ✅ | Green ≥90% · Red <75% |
| Toppers (90%+) | Number | ✅ | |
| Curriculum % | Progress bar | ✅ | On-track / Behind |
| Trend vs Last | Arrow + Δ% | ✅ | ↑ green · ↓ red |
| Actions | — | ❌ | View Branch Detail |

**Default sort:** Avg Score ascending (lowest first — needs attention).

**Pagination:** 25/page server-side.

---

### 5.3 Exam Conflict Timeline (read section)

> Visual calendar of all approved/pending exams across branches — to see load clustering.

**Display:** Read-only week-by-week grid (next 8 weeks).

**Columns:** Week dates. **Rows:** Branches.

**Cells:** Number of exams scheduled that week per branch. Red background if 3+ exams in one week for one branch (overloaded). Click cell → opens list of exams for that branch-week.

**Legend:** Green = 0–1 exams · Yellow = 2 exams · Red = 3+ exams (overload warning).

---

### 5.4 Upcoming Exams List (next 30 days — approved only)

**Display:** Compact list (not table) — grouped by week.

**Fields per item:** Date · Branch · Exam Name · Stream/Class · Status badge (Approved/Pending).

**"View Full Exam Approval →"** link to page 18.

---

## 6. Drawers & Modals

### 6.1 Drawer: `exam-approval`
- **Trigger:** Exam table → [View Details] or row click
- **Width:** 560px
- **Tabs:** Schedule · Conflicts · History · Action

#### Tab: Schedule
| Field | Value |
|---|---|
| Branch | [Name] |
| Exam Name | [Name] |
| Date & Time | [datetime] |
| Duration | [hours] |
| Stream / Class | [badge] |
| Venue | [room/hall] |
| Question Paper | [View PDF link if uploaded] |
| Submitted by | [name + role] |
| Submitted on | [date] |
| Notes from branch | [text] |

#### Tab: Conflicts
- Timeline showing all nearby exams from other branches for same stream/class
- Conflict highlighted in red on timeline
- Explanation: "Branch [X] has MPC Class 11 exam on [date] — 1 day apart"
- Recommendation: "Consider shifting this exam by 4+ days to avoid student perception of unfairness"

#### Tab: History
- Previous exam approvals/rejections for this branch (last 10)
- Pattern detection: "This branch has had 3 rejections in the last 2 months"

#### Tab: Action
- [Approve] button (green) — creates audit entry, notifies branch Exam Controller
- [Reject with Reason] button (red) — opens inline reason field (required, min 30 chars)
- [Request Modification] button (yellow) — sends modification request to branch with comments
- [Approve with Condition] button — approve with attached note (e.g. "Must reschedule if conflict worsens")

### 6.2 Modal: `bulk-approve-confirm`
- **Width:** 480px
- **Content:** List of all selected exams (branch, name, date) + "Approve all [N] exams?"
- **Conflict warning:** If any selected have conflicts, show warning and allow to deselect those
- **Buttons:** [Approve All] + [Cancel]

---

## 7. Charts

### 7.1 Academic Score Trend (Cross-branch, 6 months)
- **Type:** Multi-line chart
- **Data:** Average score % per branch per month (last 6 exam cycles)
- **X-axis:** Exam months
- **Y-axis:** Average score %
- **Lines:** Each branch (max 10 shown by default, toggle others via legend)
- **Tooltip:** Month · Branch · Avg: X% · Pass: Y% · Toppers: N
- **Export:** PNG

### 7.2 Curriculum Completion by Branch (this term)
- **Type:** Horizontal bar chart
- **Data:** Curriculum completion % per branch
- **Colour:** Green ≥90% · Yellow 70–90% · Red <70%
- **X-axis:** 0–100%
- **Benchmark line:** 80% (expected at this point in term)
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exam approved | "Exam schedule approved. [Branch] Exam Controller notified." | Success | 4s |
| Exam rejected | "Exam schedule rejected. Reason sent to branch." | Success | 4s |
| Exam modification requested | "Modification request sent to branch." | Info | 4s |
| Bulk approve | "[N] exam schedules approved" | Success | 4s |
| Bulk approve with conflicts skipped | "[N] approved · [M] skipped (conflicts) — review skipped items" | Warning | 6s |
| Toppers report ready | "Topper report generated — click to download" | Info | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No pending exam approvals | "No pending exam schedules" | "All submitted exam schedules have been reviewed" | — |
| No academic data | "No exam data available" | "Exam performance data will appear after the first exam cycle" | — |
| No branches found (search) | "No branches match" | "Try different search terms" | [Clear Search] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 6 KPI cards + exam table rows (8) + performance table (5) |
| Exam approval drawer open | Spinner in drawer until tabs load |
| Approve / Reject action | Spinner in button + button disabled |
| Bulk approve submit | Full-page overlay "Submitting [N] approvals…" |
| Chart load | Spinner centred in chart area |

---

## 11. Role-Based UI Visibility

| Element | President G4 | CEO G4 | Trustee G1 | Others |
|---|---|---|---|---|
| Page | ✅ | ❌ redirect | ❌ redirect | ❌ redirect |
| [Approve] / [Reject] in exam table | ✅ | ❌ | ❌ | ❌ |
| [Bulk Approve] button | ✅ | ❌ | ❌ | ❌ |
| [Download Topper Report] | ✅ | ❌ | ❌ | ❌ |
| Academic performance table (view) | ✅ | ✅ (read-only via CEO dashboard) | ✅ (via Board dashboard) | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/president/dashboard/` | JWT (G4 President) | Full dashboard data |
| GET | `/api/v1/group/{id}/exam-schedules/?status=pending` | JWT (G4) | Pending exam approval queue |
| GET | `/api/v1/group/{id}/exam-schedules/{eid}/conflicts/` | JWT (G4) | Conflict analysis for an exam |
| POST | `/api/v1/group/{id}/exam-schedules/{eid}/approve/` | JWT (G4 President) | Approve exam |
| POST | `/api/v1/group/{id}/exam-schedules/{eid}/reject/` | JWT (G4 President) | Reject with reason |
| POST | `/api/v1/group/{id}/exam-schedules/{eid}/request-modification/` | JWT (G4 President) | Request change |
| POST | `/api/v1/group/{id}/exam-schedules/bulk-approve/` | JWT (G4 President) | Bulk approve list |
| GET | `/api/v1/group/{id}/academic/performance/` | JWT (G4) | Branch-wise academic performance |
| GET | `/api/v1/group/{id}/academic/score-trend/` | JWT (G4) | 6-month score trend |
| GET | `/api/v1/group/{id}/academic/curriculum-completion/` | JWT (G4) | Curriculum completion by branch |
| GET | `/api/v1/group/{id}/academic/toppers/report/` | JWT (G4) | Generate/download toppers PDF |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Exam search | `input delay:300ms` | GET `.../exam-schedules/?q=` | `#exam-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../exam-schedules/?filters=` | `#exam-table-section` | `innerHTML` |
| Open exam drawer | `click` | GET `.../exam-schedules/{id}/` | `#drawer-body` | `innerHTML` |
| Approve inline | `click` | POST `.../approve/` | `#exam-row-{id}` | `outerHTML` |
| Bulk approve confirm | `click` | POST `.../bulk-approve/` | `#exam-table-section` | `innerHTML` |
| Performance table sort | `click` | GET `.../performance/?sort=` | `#perf-table-body` | `innerHTML` |
| KPI stats auto-refresh | `every 5m` | GET `.../president/dashboard/stats/` | `#president-stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
