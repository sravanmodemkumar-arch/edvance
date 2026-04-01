# 06 — Board Trustee Dashboard

> **URL:** `/group/gov/board/`
> **File:** `06-board-trustee-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Board Member / Trustee (G1) — exclusive landing page

---

## 1. Purpose

Read-only governance view for Board Members and Trustees. Trustees have G1 access — they can
view all financial, academic, and compliance data across branches, but cannot edit, approve, or
trigger any action on the platform.

Primary use cases:
- View group-level KPIs before and after board meetings
- Download the quarterly board pack PDF
- Access board meeting agendas and minutes
- Review compliance status and audit outcomes

**Critical rule:** No write controls are rendered for G1 on this page or any linked page. Every
`[Edit]`, `[Approve]`, `[+ New]` button is hidden server-side for G1 role.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Board Member / Trustee | G1 | Read-only — all sections visible, zero write controls | Up to 3–4 Trustees per group |
| Chairman | G5 | Read (can also visit this view to see Trustee perspective) | |
| MD | G5 | Read | |
| CEO | G4 | Read | |
| President | G4 | Read | |
| VP | G4 | Read | |
| Exec Secretary | G3 | — | Cannot access |
| Advisor | G1 | — | Has own dashboard |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Board Governance Dashboard
```

### 3.2 Page Header
```
Board & Governance Overview — [Trustee Name]           [Download Board Pack (Q1 2026) ↓]
[Group Name] · Board Member since: [year] · Last login: [date time]
```

> All action buttons suppressed — only [Download Board Pack] is allowed (read access to a PDF).

---

## 4. KPI Summary Bar (6 cards — all read-only)

| Card | Metric | Notes |
|---|---|---|
| Total Students | `82,340 enrolled` · ↑2.3% YoY | Group-wide |
| Annual Revenue | `₹84.2 Cr` (current FY) · ↑11.4% YoY | Read-only — from Finance aggregation |
| Total Staff | `3,247 across 50 branches` | Including Teaching + Non-Teaching |
| Exam Pass Rate | `94.8%` last exam cycle | Cross-branch average |
| Compliance Score | `87 / 100` | Composite — CBSE + POCSO + BGV + Safety |
| Board Meetings (FY) | `4 held · 2 planned` | |

> No click-through drill-down for G1 on financial cards — view is read-only aggregate only.
> Cards do not have trend click links. Academic + Compliance cards link to read-only views.

---

## 5. Sections

### 5.1 Group Performance Summary

> Strategic health of the institution group — read-only.

**Display:** 3-column card grid — Financial, Academic, Operations.

#### Financial Health Card
| Metric | Value | Trend |
|---|---|---|
| Annual Revenue | ₹84.2 Cr | ↑11.4% YoY |
| Fee Collection Rate | 94.2% | ↓0.8% vs last month |
| Outstanding Fees | ₹1.2 Cr | — |
| Scholarship Disbursed | ₹42L | FY to date |

#### Academic Health Card
| Metric | Value | Trend |
|---|---|---|
| Avg Exam Score | 72.3% | ↑1.1% vs last cycle |
| Pass Rate | 94.8% | ↑0.4% |
| Curriculum On-Track | 68% branches | — |
| NTSE / Olympiad Enrolments | 1,240 | — |

#### Operational Health Card
| Metric | Value | Trend |
|---|---|---|
| Active Branches | 48 / 50 | — |
| BGV Compliance | 87% | ↑3% vs last quarter |
| POCSO Training | 92% | — |
| Open Grievances | 12 | — |

---

### 5.2 Board Meeting Schedule + Minutes

> View upcoming and past board meetings. Read-only access to agendas and minutes PDFs.

**Display:** Table.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Meeting # | Text | ✅ | e.g. BM-2026-Q1 |
| Date | Date | ✅ | |
| Type | Badge | ✅ | Annual General · Quarterly Review · Emergency |
| Venue | Text | ❌ | |
| Status | Badge | ✅ | Upcoming · Completed · Cancelled |
| Attendees | Number | ❌ | Count |
| Resolutions | Number | ❌ | Count of resolutions passed |
| Agenda | Link | ❌ | "Download PDF" — read-only |
| Minutes | Link | ❌ | "Download PDF" — available after meeting |
| Actions | — | ❌ | [View] only — no create, no edit |

**Default sort:** Date descending (most recent first).

**Pagination:** 10/page (board meetings are infrequent).

**[View] action:** Opens 640px read-only drawer — full meeting details including agenda items,
attendee list, RSVP status, and resolutions (all read-only, no edit controls).

---

### 5.3 Compliance Overview (read-only)

> Traffic-light view of group compliance — cannot take action from here.

**Display:** Grid of compliance areas with status badges.

| Compliance Area | Status | Last Checked | Details |
|---|---|---|---|
| CBSE Affiliation | ✅ Compliant | March 2026 | Renewal due: March 2027 |
| State Board (BSEAP) | ✅ Compliant | Feb 2026 | — |
| POCSO Training | ⚠ In Progress | March 2026 | 92% — 8% pending |
| BGV Completion | ⚠ Warning | March 2026 | 87% — 42 pending |
| Fire Safety NOC | ✅ Compliant | Jan 2026 | — |
| DPDP Act (Data Privacy) | ✅ Compliant | Feb 2026 | — |
| RTE Quota | ✅ Compliant | April 2025 | — |

**Click area:** Opens 480px read-only drawer — detail per compliance area per branch (branch
name + status + last updated). No action buttons.

**"View Full Compliance →"** link to page 27 (read-only for Trustee).

---

### 5.4 Academic Performance Overview (read-only)

> Branch-wise academic performance — no filter/search controls for G1.

**Display:** Sortable table (G1 can sort but not filter/search — sort is client-side for G1).

**Columns:**

| Column | Type | Notes |
|---|---|---|
| Branch | Text | |
| Avg Score % | Number + bar | Colour-coded |
| Pass % | Number | |
| Toppers (90%+) | Number | |
| Trend vs Last | Arrow + Δ | |

**Rows:** All branches. No search, no filter, no export for G1.

---

### 5.5 Download Board Pack

> Prominent CTA card — Trustee's primary action.

**Display:** Highlighted card with last generated date and download button.

**Board Pack contents:**
- Group Summary Report (auto-generated)
- Financial Highlights (current FY)
- Academic Performance Report
- Compliance Status Report
- Branch Health Matrix
- Agenda for upcoming meeting (if available)

**Generate:** Board Pack is pre-generated by MD/CEO (via Governance Reports page 25). Trustee
can only download the already-generated pack.

**Download button:** `hx-get="/api/v1/group/{id}/board-pack/latest/"` → returns download URL
→ browser initiates PDF download.

**Toast:** "Board pack downloading…" (Info, 4s).

---

## 6. Drawers & Modals (Read-Only Only)

### 6.1 Drawer: `board-meeting-view` (read-only)
- **Trigger:** Board meetings table → [View]
- **Width:** 640px
- **Tabs:** Overview · Agenda · Attendees · Resolutions · Minutes
- **All tabs:** Read-only — no edit icons, no [+ Add] buttons
- **Minutes tab:** PDF viewer inline if available, else "Minutes not yet uploaded"

### 6.2 Drawer: `compliance-area-detail` (read-only)
- **Trigger:** Compliance grid → click area
- **Width:** 480px
- **Content:** Branch-by-branch compliance status for selected area — sortable table
- **No action buttons** — view only

---

## 7. Charts

### 7.1 Annual Revenue Trend (3 Years)
- **Type:** Bar chart
- **Data:** Annual revenue for 3 FYs (actual + current year projected)
- **X-axis:** FY labels
- **Y-axis:** ₹ Crores
- **Tooltip:** FY · Revenue: ₹X.XCr · Growth: +X%
- **Export:** PNG

### 7.2 Exam Pass Rate Trend (Last 4 Terms)
- **Type:** Line chart
- **Data:** Group-average pass rate per exam term (last 4 terms)
- **X-axis:** Term labels
- **Y-axis:** Pass rate %
- **Tooltip:** Term · Pass rate: X%
- **Export:** PNG

> **G1 charts:** All charts are read-only static renders. No filter controls on charts for Trustee.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Board pack download initiated | "Board pack downloading…" | Info | 4s |
| Board pack not available | "Board pack hasn't been generated yet. Contact the MD." | Warning | 6s |
| Meeting agenda PDF download | "Agenda downloading…" | Info | 4s |
| Minutes not yet available | "Meeting minutes haven't been uploaded yet" | Info | 4s |
| Session expired | "Your session has expired. Please log in again." | Error | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No board meetings | "No board meetings recorded" | "Board meeting history will appear here once entered by the Executive Secretary" | — |
| Board pack not generated | "Board pack not yet available" | "The MD or CEO will generate the board pack before the meeting" | — |
| No academic data | "Academic data not yet available" | "Academic performance will appear after the first exam cycle" | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 6 KPI cards + board meetings table (5 rows) + compliance grid |
| Board meeting drawer open | Spinner in drawer |
| Board pack download | Spinner in download button (momentary) |
| Chart load | Spinner centred in chart area |

---

## 11. Role-Based UI Visibility

| Element | Trustee G1 | G4 (reading this page) | G5 (reading this page) |
|---|---|---|---|
| Page | ✅ | ✅ Read-only view | ✅ Read-only view |
| [Download Board Pack] button | ✅ | ✅ | ✅ |
| [+ New Meeting] | ❌ hidden | ❌ hidden | ❌ (shown only on page 29) |
| [Edit] on any table row | ❌ hidden | ❌ hidden | ❌ hidden |
| Filter/search controls | ❌ hidden | ✅ | ✅ |
| Export table | ❌ hidden | ✅ | ✅ |
| Compliance action buttons | ❌ hidden | ❌ hidden | ❌ hidden (use page 27) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/board/dashboard/` | JWT (G1 Trustee) | Full board dashboard data |
| GET | `/api/v1/group/{id}/board-pack/latest/` | JWT (G1) | Download latest board pack PDF |
| GET | `/api/v1/group/{id}/board-meetings/` | JWT (G1) | Board meetings list |
| GET | `/api/v1/group/{id}/board-meetings/{mid}/` | JWT (G1) | Meeting detail (read-only) |
| GET | `/api/v1/group/{id}/compliance/overview/` | JWT (G1) | Compliance areas summary |
| GET | `/api/v1/group/{id}/academic/performance/` | JWT (G1) | Academic performance table |
| GET | `/api/v1/group/{id}/financial/revenue-trend/` | JWT (G1) | 3-year revenue chart data |
| GET | `/api/v1/group/{id}/academic/pass-rate-trend/` | JWT (G1) | Pass rate trend chart data |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Open meeting drawer (read) | `click` | GET `.../board-meetings/{id}/` | `#drawer-body` | `innerHTML` |
| Download board pack | `click` | GET `.../board-pack/latest/` | — | — (triggers download) |
| Open compliance drawer (read) | `click` | GET `.../compliance/{area}/branches/` | `#drawer-body` | `innerHTML` |
| Performance table sort (client) | `click` on header | Client-side sort only for G1 | `#perf-table-body` | `innerHTML` |
| Dashboard data refresh | `every 5m` | GET `.../board/dashboard/summary/` | `#trustee-summary` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
