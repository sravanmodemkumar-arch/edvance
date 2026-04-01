# 56 — Dropout Signal Monitor

> **URL:** `/group/acad/dropout-signals/`
> **File:** `56-dropout-signal-monitor.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Director G3 · CAO G4 · Special Education Coordinator G3 (own students) · Academic MIS Officer G1 (read-only)

---

## 1. Purpose

The Dropout Signal Monitor is the group's early intervention system for identifying students at risk of leaving school before completing their education. In India's competitive private education sector, a student dropout is simultaneously a welfare failure and a financial loss — one that often occurs gradually over weeks before it becomes irreversible. By the time a branch principal notices that a student has stopped attending, the family has often already made the decision to leave.

This page runs four automated signal algorithms against live platform data daily and flags students who exhibit one or more risk signals. The four signals are: attendance below 75% for two consecutive weeks (attendance signal); marks below the pass threshold in two or more subjects in the most recent exam (academic signal); fee payment overdue by 30 or more days (financial signal); and no login to the student portal for 30 days (engagement signal). Students are then assigned a risk level: Low (1 signal), Medium (2 signals), High (3 or more signals).

The page allows the Academic Director to assign a counsellor to each high-risk student, log intervention notes, and track whether the intervention is working over time. For students who are also registered in the Special Needs Registry (page 46), the Special Education Coordinator has visibility into their own students' dropout signals as a safeguard. The MIS Officer sees aggregated counts for reporting purposes but cannot see individual student names.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ❌ No create | Supervisory; can view all student signals |
| Group Academic Director | G3 | ✅ Full | ✅ Full — assign counsellors, log interventions | Primary owner |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ✅ Own special-needs students only | ❌ No create | View-only for own-registry students |
| Group Academic MIS Officer | G1 | ✅ Read-only aggregate | ❌ | Branch-level counts, no student PII |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Academic MIS & Analytics  ›  Dropout Signal Monitor
```

### 3.2 Page Header
```
Dropout Signal Monitor                                   [Export At-Risk List ↓]
Early intervention — [Group Name] · Last signal scan: [datetime]
```

**Signal scan frequency:** Daily automated scan. Manual re-scan button available to Academic Dir.

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Students Flagged | Count |
| High Risk (3+ signals) | Count — red |
| Medium Risk (2 signals) | Count — amber |
| Low Risk (1 signal) | Count — yellow |
| Counsellor Assigned | Count — green |
| Resolved This Month | Count |

---

## 4. Main Content

### 4.1 Search
- Academic Director, CAO: Full-text across student name, student ID, branch name
- MIS Officer: Branch name only (no student PII)
- 300ms debounce

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Risk Level | Multi-select | High / Medium / Low |
| Signal Type | Multi-select | Attendance / Academic / Fee / Engagement |
| Class | Multi-select | Class 6–12 |
| Counsellor Assigned | Select | Yes / No |
| Status | Select | Active / Resolved / False Positive |

MIS Officer: only Branch filter available (others hidden).

Active filter chips dismissible. "Clear All". Badge count on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible To | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | Academic Dir | Bulk select |
| Student ID | Text | ✅ | All | |
| Student Name | Text | ✅ | Academic Dir, CAO, Spec Ed Coord (own) | Hidden from MIS |
| Branch | Text | ✅ | All | |
| Class | Badge | ✅ | All | |
| Signal Count | Number + badge | ✅ | All | 1 / 2 / 3+ |
| Signals Triggered | Tags | ❌ | Academic Dir, CAO | Attendance · Academic · Fee · Engagement |
| Risk Level | Badge | ✅ | All | High (red) · Medium (amber) · Low (yellow) |
| Counsellor Assigned | Text | ✅ | Academic Dir, CAO | Name or "Not assigned" |
| Status | Badge | ✅ | Academic Dir, CAO | Active / Resolved / False Positive |
| Actions | — | ❌ | Role-based | |

**Default sort:** Risk Level (High first), then Signal Count descending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer | Notes |
|---|---|---|---|---|
| View Detail | Eye | Academic Dir, CAO, Spec Ed Coord (own) | `student-risk-detail` drawer 560px | Full signal history |
| Assign Counsellor | Person | Academic Dir | Inline select | From branch staff |
| Mark Resolved | Check | Academic Dir | Confirm modal | Clears from active list |
| Mark False Positive | Flag | Academic Dir | Confirm modal | Removes from list; signal algorithm noted |
| Escalate to Principal | Alert | Academic Dir | Confirm modal | Sends alert to branch principal |

### 4.5 Bulk Actions (Academic Director only)

| Action | Notes |
|---|---|
| Assign Counsellor — Selected | Bulk counsellor assignment |
| Export At-Risk List (XLSX) | Selected students' signal data |
| Escalate Selected to Principals | Batch alert to branch principals |

---

## 5. Drawers & Modals

### 5.1 Drawer: `student-risk-detail`
- **Trigger:** View Detail row action
- **Width:** 560px
- **Tabs:** Signal History · Performance Graph · Fee Status · Counsellor Notes · Intervention Log

**Tab: Signal History**
Table: Signal type · Date first triggered · Date last updated · Current value · Threshold · Status
Example row: Attendance · 2026-03-01 · 2026-03-19 · 68% avg (2 weeks) · < 75% threshold · Active

**Tab: Performance Graph**
Mini line chart: Last 6 exam scores per subject. Horizontal pass threshold line per subject.

**Tab: Fee Status**
Fee due: ₹X · Fee paid: ₹X · Outstanding: ₹X · Overdue since: [Date]. Link to Div-C/Finance for fee history.

**Tab: Counsellor Notes**
Assigned counsellor: [Name or "Not assigned"]. Chronological notes log: date, note, author. [+ Add Note] textarea + submit (Academic Dir only).

**Tab: Intervention Log**
All interventions: Type (phone call / parent meeting / class teacher alert / fee discussion) · Date · Outcome · Next action. [+ Log Intervention] (Academic Dir only).

### 5.2 Modal: `assign-counsellor`
- **Width:** 420px
- **Content:** "Assign a counsellor to [Student Name / ID] at [Branch]?"
- **Fields:** Counsellor (search from branch staff) · Note (optional)
- **Buttons:** [Assign] · [Cancel]

### 5.3 Modal: `mark-resolved`
- **Width:** 420px
- **Content:** "Mark [Student ID] as resolved?"
- **Fields:** Resolution outcome (Select): Signals corrected — student on track / Student left institution / Transfer confirmed / Other · Notes (Textarea, required, min 20 chars)
- **Buttons:** [Confirm Resolved] · [Cancel]

### 5.4 Modal: `escalate-to-principal`
- **Width:** 420px
- **Content:** "Send escalation alert to [Branch] principal for [Student ID]?"
- **Fields:** Message preview (editable) · Channel (Email / WhatsApp / Both)
- **Buttons:** [Send Escalation] · [Cancel]

---

## 6. Charts

### 6.1 Dropout Signal Count by Branch (Bar)
- **Type:** Vertical bar chart, stacked by risk level
- **Data:** Count of flagged students per branch, stacked: High / Medium / Low
- **Tooltip:** Branch · High: N · Medium: N · Low: N · Total: N
- **Export:** PNG

### 6.2 Risk Level Distribution (Donut)
- **Type:** Donut
- **Data:** Count split by High / Medium / Low / Resolved
- **Centre text:** Total flagged
- **Tooltip:** Level · Count · %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Counsellor assigned | "Counsellor [Name] assigned to [Student ID]" | Success | 4s |
| Student resolved | "[Student ID] marked as resolved. Signals cleared." | Success | 4s |
| False positive logged | "[Student ID] marked as false positive. Algorithm feedback recorded." | Info | 4s |
| Escalation sent | "Escalation sent to [Branch] principal" | Success | 4s |
| Bulk escalation sent | "Escalation alerts sent for [N] students to [N] principals" | Success | 4s |
| Manual re-scan triggered | "Signal scan running… table will refresh in ~30 seconds" | Info | 30s |
| Export started | "Export preparing… download will start shortly" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No students flagged | "No at-risk students detected" | "The daily signal scan has not flagged any students. Keep monitoring." | — |
| No High Risk students | "No High Risk students" | "No students currently have 3 or more active signals" | — |
| No results match filters | "No students match" | "Clear filters to see all flagged students" | [Clear Filters] |
| Counsellor Notes tab — no notes | "No counsellor notes" | "Add the first note after speaking with the student or parent" | [+ Add Note] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) + chart areas |
| Table filter/search/sort/page | Inline skeleton rows |
| Student risk detail drawer | Spinner → tabs load |
| Performance graph tab | Skeleton line chart |
| Manual re-scan | Full stats bar spinner → refreshes after 30s |
| Export trigger | Spinner in button |

---

## 10. Role-Based UI Visibility

| Element | Academic Dir G3 | CAO G4 | Spec Ed Coord G3 | MIS G1 |
|---|---|---|---|---|
| Full table with student names | ✅ | ✅ | ✅ (own) | ❌ (branch counts) |
| Signal type tags | ✅ | ✅ | ✅ | ❌ |
| Assign Counsellor | ✅ | ❌ | ❌ | ❌ |
| Mark Resolved | ✅ | ❌ | ❌ | ❌ |
| Escalate to Principal | ✅ | ❌ | ❌ | ❌ |
| View Detail drawer | ✅ | ✅ | ✅ (own) | ❌ |
| Add counsellor notes | ✅ | ❌ | ❌ | ❌ |
| Log Intervention | ✅ | ❌ | ❌ | ❌ |
| Bulk actions | ✅ | ❌ | ❌ | ❌ |
| Export | ✅ | ✅ | ❌ | ❌ |
| Charts | ✅ | ✅ | ❌ | ✅ (aggregate only) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/dropout-signals/` | JWT | List flagged students (role-filtered) |
| GET | `/api/v1/group/{group_id}/acad/dropout-signals/stats/` | JWT | Stats bar |
| GET | `/api/v1/group/{group_id}/acad/dropout-signals/{student_id}/` | JWT (G3 Dir, G4) | Student risk detail |
| POST | `/api/v1/group/{group_id}/acad/dropout-signals/{student_id}/assign-counsellor/` | JWT (G3 Dir) | Assign counsellor |
| POST | `/api/v1/group/{group_id}/acad/dropout-signals/{student_id}/resolve/` | JWT (G3 Dir) | Mark resolved |
| POST | `/api/v1/group/{group_id}/acad/dropout-signals/{student_id}/false-positive/` | JWT (G3 Dir) | Mark false positive |
| POST | `/api/v1/group/{group_id}/acad/dropout-signals/{student_id}/escalate/` | JWT (G3 Dir) | Escalate to branch principal |
| POST | `/api/v1/group/{group_id}/acad/dropout-signals/{student_id}/notes/` | JWT (G3 Dir) | Add counsellor note |
| POST | `/api/v1/group/{group_id}/acad/dropout-signals/{student_id}/interventions/` | JWT (G3 Dir) | Log intervention |
| POST | `/api/v1/group/{group_id}/acad/dropout-signals/rescan/` | JWT (G3 Dir) | Trigger manual signal scan |
| POST | `/api/v1/group/{group_id}/acad/dropout-signals/bulk-escalate/` | JWT (G3 Dir) | Bulk escalation |
| GET | `/api/v1/group/{group_id}/acad/dropout-signals/export/?format=xlsx` | JWT (G3/G4) | Export |
| GET | `/api/v1/group/{group_id}/acad/dropout-signals/charts/by-branch/` | JWT | Stacked bar data |
| GET | `/api/v1/group/{group_id}/acad/dropout-signals/charts/risk-distribution/` | JWT | Donut data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../dropout-signals/?q=` | `#dropout-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../dropout-signals/?filters=` | `#dropout-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../dropout-signals/?sort=&dir=` | `#dropout-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../dropout-signals/?page=` | `#dropout-table-section` | `innerHTML` |
| Student detail drawer | `click` | GET `.../dropout-signals/{sid}/` | `#drawer-body` | `innerHTML` |
| Assign counsellor confirm | `click` | POST `.../dropout-signals/{sid}/assign-counsellor/` | `#dropout-row-{sid}` | `outerHTML` |
| Mark resolved confirm | `click` | POST `.../dropout-signals/{sid}/resolve/` | `#dropout-row-{sid}` | `outerHTML` |
| Escalate confirm | `click` | POST `.../dropout-signals/{sid}/escalate/` | `#toast-container` | `beforeend` |
| Add note | `submit` | POST `.../dropout-signals/{sid}/notes/` | `#notes-list` | `beforeend` |
| Manual rescan trigger | `click` | POST `.../dropout-signals/rescan/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
