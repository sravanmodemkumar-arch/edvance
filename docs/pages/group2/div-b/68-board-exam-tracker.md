# 68 — Board Exam Tracker

> **URL:** `/group/acad/board-exams/`
> **File:** `68-board-exam-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Controller G3 (full) · CAO G4 (view + approve) · Academic Director G3 (view) · MIS Officer G1 (read)

---

## 1. Purpose

Central tracking page for CBSE and State Board (BSEAP/BSETS/CBSE) Class 10 and Class 12 board examinations
across all branches. Covers the full lifecycle: registration → hall ticket distribution → exam day coordination
→ result entry → mark verification.

Without this, board exam logistics are managed via spreadsheets and phone calls — registration deadlines are
missed, hall tickets not distributed in time, and board results not reconciled with internal data.

Board exams affect all Class 10 and 12 students (potentially 15,000–30,000 students in a large group).

---

## 2. Role Access

| Role | Level | Can View | Can Edit | Can Publish Results | Notes |
|---|---|---|---|---|---|
| Exam Controller | G3 | ✅ Full | ✅ Full | ✅ | Primary owner |
| CAO | G4 | ✅ Full | ❌ | ❌ | View + approve escalations |
| Academic Director | G3 | ✅ Full | ❌ | ❌ | View only |
| MIS Officer | G1 | ✅ Read | ❌ | ❌ | Read-only for reports |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Board Exam Tracker
```

### 3.2 Page Header
```
Board Exam Tracker                              [+ Add Board Exam]  [Export Summary ↓]
AY 2025–26 · Class 10 & 12 · CBSE · BSEAP · BSETS
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Active Board Exams | 4 |
| Total Students Appearing | 18,340 |
| Registrations Completed | 47 / 50 branches |
| Hall Tickets Distributed | 38 / 47 registered branches |
| Results Entered | 2 / 4 completed exams |
| Overdue Actions | 3 branches |

---

## 4. Main Table

### 4.1 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Board | Badge | ✅ | CBSE · BSEAP · BSETS · ICSE |
| Class | Badge | ✅ | 10 · 12 |
| Exam Name | Text | ✅ | e.g. "CBSE Class 12 2025–26" |
| Exam Month | Date | ✅ | Month & Year |
| Branches Appearing | Number | ✅ | Branches with students in this exam |
| Students | Number | ✅ | Total students appearing |
| Registration Status | Progress bar | ✅ | N/M branches registered |
| Hall Tickets | Progress bar | ✅ | N/M distributed |
| Exam Day | Phase badge | ✅ | Upcoming · In Progress · Completed |
| Results | Progress bar | ✅ | N/M branches uploaded results |
| Phase | Badge | ✅ | Registration · Hall Tickets · Exam · Results · Verified |
| Actions | — | ❌ | View · Edit · Mark Phase |

### 4.2 Filters

| Filter | Type | Options |
|---|---|---|
| Board | Multi-select | CBSE · BSEAP · BSETS · ICSE |
| Class | Multi-select | 10 · 12 |
| Phase | Multi-select | Registration · Hall Tickets · Exam Day · Results · Verified |
| Branch | Multi-select | Branch names |
| Status | Select | On Track · At Risk · Overdue |

### 4.3 Search
- Full-text across exam name, board, branch name
- 300ms debounce

---

## 5. Drawers & Modals

### 5.1 Drawer: `board-exam-create` — Add Board Exam
- **Trigger:** [+ Add Board Exam] header button
- **Width:** 640px

| Field | Type | Required | Validation |
|---|---|---|---|
| Board | Select | ✅ | CBSE / BSEAP / BSETS / ICSE |
| Class | Select | ✅ | 10 / 12 |
| Exam Name | Text | ✅ | e.g. "CBSE Class 12 Annual 2026" |
| Exam Month | Month picker | ✅ | |
| Registration Deadline | Date | ✅ | Must be before exam month |
| Hall Ticket Deadline | Date | ✅ | Must be after registration, before exam |
| Applicable Branches | Multi-select | ✅ | Branches with relevant class/board |
| Stream Scope | Multi-select | ❌ | MPC / BiPC / MEC / CEC / HEC — filter by stream |
| Expected Student Count | Number | ❌ | Auto-calculated from enrollment |

### 5.2 Drawer: `board-exam-detail` — Exam Detail
- **Trigger:** View row action
- **Width:** 680px

**Tab: Overview**
- Board · Class · Exam Name · Exam Month · Registration Deadline · Hall Ticket Deadline
- Phase timeline bar showing completed/current/upcoming phases

**Tab: Branch Registration**

| Column | Type |
|---|---|
| Branch | Text |
| Students Registered | Number |
| Registration Number Range | Text |
| Registered By | Text (staff name) |
| Registered Date | Date |
| Status | Badge (Complete / Pending / Overdue) |

- **Actions:** [Mark Registered] · [Send Reminder]
- **Bulk:** Select all pending → [Send Bulk Reminder]

**Tab: Hall Tickets**

| Column | Type |
|---|---|
| Branch | Text |
| Hall Tickets Received | Number |
| Distribution Status | Badge |
| Distributed By | Text |
| Distribution Date | Date |
| Acknowledgement | Badge |

- **Actions:** [Mark Distributed] · [Upload Acknowledgement]

**Tab: Exam Day**
- Centre allocation per branch (exam centre address, invigilator-in-charge)
- Attendance % per branch (uploaded after exam day)
- Issues reported (absentees, malpractice, centre issues)

**Tab: Results**

| Column | Type |
|---|---|
| Branch | Text |
| Students Appeared | Number |
| Results Uploaded | Badge (Yes / Pending) |
| Pass % | Number |
| Distinction % | Number |
| Upload Date | Date |

- **Actions:** [Upload Results CSV] · [View Results] → links to Result Archive (Page 34)

**Tab: Verification**
- Board result vs. internal last exam comparison
- Significant deviation (>15% difference) flagged for investigation
- [Mark Verified] button after review

---

## 6. Alert Logic

| Condition | Alert | Recipient | Urgency |
|---|---|---|---|
| Registration deadline in 7 days, branch not registered | In-app + WhatsApp | Exam Controller + Branch Principal | High |
| Hall ticket deadline in 5 days, not distributed | In-app alert | Exam Controller | High |
| Exam day passed, results not uploaded in 30 days | In-app + email | Exam Controller + CAO | Medium |
| Board pass % < 60% | Alert badge on row | Exam Controller + Academic Director | Medium |
| Board vs. internal deviation > 15% | Flag on results tab | Exam Controller | Low |

---

## 7. Charts

### 7.1 Board Pass % by Branch
- **Type:** Horizontal bar chart
- **Data:** Branch pass % in most recent board exams
- **Benchmark line:** Group average
- **Export:** PNG

### 7.2 Board vs. Internal Exam Correlation
- **Type:** Scatter plot
- **X-axis:** Internal exam avg %
- **Y-axis:** Board exam avg %
- **Each point:** One branch
- **Quadrant labels:** Consistent High · Board Underperformer · Board Overperformer · Consistent Low
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Board exam created | "Board exam '[Name]' added. Branches notified." | Success | 4s |
| Registration marked | "Branch [Name] registration marked complete." | Success | 4s |
| Hall tickets marked | "Hall tickets marked distributed for [Branch]." | Success | 4s |
| Results uploaded | "Results uploaded for [Branch]. Pass %: [N]%." | Success | 4s |
| Reminder sent | "Reminder sent to [N] branches." | Info | 4s |
| Overdue alert | "3 branches have missed registration deadline." | Warning | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No board exams | "No board exams tracked" | "Add the first board exam to begin tracking." | [+ Add Board Exam] |
| No results | "No results uploaded yet" | "Results will appear once branches upload." | — |
| Filter empty | "No exams match filters" | "Try clearing filters." | [Clear Filters] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + 5 table rows |
| Table filter/sort/page | Inline skeleton rows |
| Drawer open | Spinner + skeleton tabs |
| Chart load | Spinner in chart area |

---

## 11. Role-Based UI Visibility

| Element | Exam Ctrl G3 | CAO G4 | Acad Dir G3 | MIS G1 |
|---|---|---|---|---|
| [+ Add Board Exam] | ✅ | ❌ | ❌ | ❌ |
| [Mark Registered / Distributed] | ✅ | ❌ | ❌ | ❌ |
| [Upload Results CSV] | ✅ | ❌ | ❌ | ❌ |
| [Mark Verified] | ✅ | ✅ (override) | ❌ | ❌ |
| [Send Reminder] | ✅ | ❌ | ❌ | ❌ |
| [Export Summary] | ✅ | ✅ | ✅ | ✅ |
| Charts | ✅ | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/board-exams/` | JWT (G1+) | List board exams |
| POST | `/api/v1/group/{id}/acad/board-exams/` | JWT (G3) | Create board exam |
| GET | `/api/v1/group/{id}/acad/board-exams/{eid}/` | JWT (G1+) | Board exam detail (all tabs) |
| PUT | `/api/v1/group/{id}/acad/board-exams/{eid}/` | JWT (G3) | Update board exam |
| POST | `/api/v1/group/{id}/acad/board-exams/{eid}/mark-registration/` | JWT (G3) | Mark branch registered |
| POST | `/api/v1/group/{id}/acad/board-exams/{eid}/mark-hall-tickets/` | JWT (G3) | Mark hall tickets distributed |
| POST | `/api/v1/group/{id}/acad/board-exams/{eid}/upload-results/` | JWT (G3) | Upload branch results CSV |
| POST | `/api/v1/group/{id}/acad/board-exams/{eid}/mark-verified/` | JWT (G3+) | Mark results verified |
| POST | `/api/v1/group/{id}/acad/board-exams/{eid}/send-reminder/` | JWT (G3) | Send reminder to pending branches |
| GET | `/api/v1/group/{id}/acad/board-exams/stats/` | JWT (G1+) | Summary stats bar |
| GET | `/api/v1/group/{id}/acad/board-exams/charts/pass-by-branch/` | JWT (G1+) | Pass % chart |
| GET | `/api/v1/group/{id}/acad/board-exams/charts/correlation/` | JWT (G3+) | Board vs internal scatter |
| GET | `/api/v1/group/{id}/acad/board-exams/export/?format=csv` | JWT (G1+) | Export summary |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Table search | `input delay:300ms` | GET `.../board-exams/?q=` | `#board-exam-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../board-exams/?filters=` | `#board-exam-section` | `innerHTML` |
| Pagination | `click` | GET `.../board-exams/?page=` | `#board-exam-section` | `innerHTML` |
| Row view | `click` | GET `.../board-exams/{id}/` | `#drawer-body` | `innerHTML` |
| Mark registration | `click` | POST `.../mark-registration/` | `#branch-row-{id}` | `outerHTML` |
| Upload results | `submit` | POST `.../upload-results/` | `#results-tab-body` | `innerHTML` |
| Send reminder | `click` | POST `.../send-reminder/` | `#reminder-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
