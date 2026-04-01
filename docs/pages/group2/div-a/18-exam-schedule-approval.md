# 18 — Exam Schedule Approval

> **URL:** `/group/gov/exam-approval/`
> **File:** `18-exam-schedule-approval.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** President G4 (approve) · Chairman G5 (override) · CEO G4 (view)

---

## 1. Purpose

Dedicated page for the Group President (Academic) to review and approve exam schedules
submitted by branch Exam Controllers. Includes automatic conflict detection when two branches
have overlapping exams for the same stream/class within a 3-day window.

Fairness mandate: A student who transfers between branches mid-year must not face two exams on
consecutive days. The conflict detector enforces this group-wide standard.

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| President | Full — approve, reject, request modification | Primary owner |
| Chairman | Override any decision + view all | |
| CEO | View only — no approve/reject | Operational awareness |
| MD | View only | |
| Others | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Exam Schedule Approval
```

### 3.2 Page Header
```
Exam Schedule Approval                                 [Approve All Non-Conflicting ▼]  [Export Schedule ↓]
[N] pending · [N] conflicts detected · Term: [current term]
```

### 3.3 Quick Stats Bar
| Stat | Value |
|---|---|
| Pending Approval | N |
| Conflicts Detected | N (red badge if >0) |
| Approved This Term | N |
| Rejected This Term | N |
| Avg Days to Approve | N.N days |

---

## 4. Exam Schedule Table

### 4.1 Tabs
```
Pending ([N])  |  Conflicting ([N])  |  Approved  |  Rejected
```

**Conflicting tab:** Shows only pending exams with conflict flags — prioritised for President's attention.

### 4.2 Search
Full-text: Branch name, exam name, stream. Debounce 300ms.

### 4.3 Advanced Filters
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated |
| Class | Multi-select | Class 6–12 + Integrated Batch |
| Date Range | Date range | Exam date |
| Conflict Status | Select | All · Conflict · No Conflict |
| Question Paper | Select | All · Uploaded · Not Uploaded |

### 4.4 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| Exam Name | Text | ✅ | e.g. "Quarterly Exam 3 — BiPC Class 11" |
| Stream | Badge | ✅ | MPC, BiPC etc. |
| Class | Badge | ✅ | |
| Exam Date | Date | ✅ | Red if within 5 days |
| Exam Time | Time | ❌ | |
| Duration | Text | ❌ | e.g. "3 hrs" |
| Question Paper | Badge | ✅ | ✅ Uploaded · ⚠ Pending |
| Submitted By | Text | ❌ | Branch Exam Controller |
| Days Pending | Number | ✅ | Red if >5 |
| Conflict | Badge | ✅ | ⚠ Conflict · ✅ Clear |
| Status | Badge | ✅ | Pending · Approved · Rejected · Modification Requested |
| Actions | — | ❌ | [Approve] [Reject] [Modify] [View Details] |

**Default sort:** Conflict flag (conflicts first), then Exam Date ascending.

**Pagination:** 25/page.

**[Approve] inline:** `hx-post` → row status changes to "Approved" · branch notified · audit log.

**[Reject] inline:** Opens inline reason field below row (300ms expand animation). Required reason.

**[Modify] inline:** Opens inline comment field. Sends modification request to branch.

**Row checkbox + bulk approve:** Select non-conflicting pending exams → [Approve Selected N]. Opens bulk-approve modal.

---

## 5. Conflict Detection Logic

**Auto-triggered:** When a new exam schedule is submitted by a branch.

**Conflict rule:** Same stream AND same class AND exam dates within 3 days of another branch's
exam for the same stream/class.

**Example:**
- Branch A: BiPC Class 11 Exam on March 10
- Branch B: BiPC Class 11 Exam on March 12 (same stream, 2 days apart → CONFLICT)

**Why it matters:** A student transferring between branches mid-year, or a student who moves
branches, will face two exams in 2 days. Also, group toppers comparison is unfair if exam
difficulty varies across clustered dates.

**Conflict badge in table:** ⚠ orange badge → click opens Conflicts tab in `exam-approval` drawer.

**Auto-resolution suggestions:**
The system suggests: "Move [Branch B]'s exam to March 15 or later to resolve this conflict."

---

## 6. Exam Load Calendar

> Visual of exam density across branches — helps President identify clusters.

**Display:** Week-by-week table — next 12 weeks.

**Rows:** Streams (MPC, BiPC, MEC, CEC, Integrated).

**Columns:** Week date ranges.

**Cells:** Count of exams for that stream in that week. Colour: Green 0–1 · Yellow 2 · Red 3+ (overloaded).

**Click cell:** Opens list of exams for that stream+week combination.

---

## 7. Drawers & Modals

### 7.1 Drawer: `exam-approval` (detailed view + action)
- **Trigger:** Row → [View Details]
- **Width:** 640px
- **Tabs:** Schedule · Conflicts · History · Action

#### Tab: Schedule
Full exam details:
- Branch, Exam Name, Stream/Class, Date, Time, Duration, Venue
- Question Paper: [View PDF] link if uploaded, else "Not yet uploaded"
- Instructions to students (if provided by branch)
- Submitted by (name, role) + submitted date
- Branch's notes/reason for this exam date

#### Tab: Conflicts
- Timeline view: All exams for the same stream/class in a 3-week window around this exam's date
- This exam highlighted in blue
- Conflicting exams highlighted in red
- Non-conflicting approved exams in green
- Conflict explanation: "2-day gap between this and [Branch X] — minimum 4 days required"
- System suggestion: "Shift to [date] to resolve"
- If no conflicts: "✅ No conflicts detected. This exam can be safely approved."

#### Tab: History
- Last 10 exam approvals/rejections for this branch
- Pass rate of last approved exam (context for this exam's quality)
- Pattern: "Branch X has had 3 conflict-related rejections this year"

#### Tab: Action
- [Approve] — green button
- [Reject with Reason] — red button, opens inline reason field
- [Request Modification] — orange button, opens comment field sent to branch
- [Approve with Condition] — grey button, approve but attach a note
- Only Approve/Reject/Modify visible for President. Chairman sees all + [Override] button.

### 7.2 Modal: `bulk-approve-exam`
- **Width:** 520px
- **Content:** List of selected exams (branch, name, date, conflict status)
- **Warning:** If any selected have conflicts → shown in red with option to deselect
- **Buttons:** [Approve [N] Exams] + [Cancel]

### 7.3 Modal: `reject-exam`
- **Width:** 420px
- **Fields:** Reason (required, min 30 chars, 500 limit with counter) · Suggest alternative date? (optional date picker)
- **Buttons:** [Reject with Reason] + [Cancel]
- **On reject:** Branch Exam Controller notified via WhatsApp with reason + suggested date

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exam approved | "Exam schedule approved. [Branch] Exam Controller notified." | Success | 4s |
| Exam rejected | "Rejection sent to [Branch] with reason and suggested date." | Success | 4s |
| Modification requested | "Modification request sent to [Branch]." | Info | 4s |
| Bulk approve | "[N] exam schedules approved" | Success | 4s |
| Conflict auto-detected | "Conflict detected with [Branch X] exam on [date]" | Warning | 6s |
| Override applied | "Chairman override applied for [Branch] exam" | Warning | 6s |
| Question paper missing | "Note: Question paper not uploaded for this exam" | Warning | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No pending exams | "No pending exam schedules" | "All submitted exam schedules have been reviewed" | — |
| No conflicts | (in Conflicting tab) "No conflicts detected" | "All pending exam schedules are conflict-free" | — |
| No exams approved | (in Approved tab) "No approved exams yet" | — | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) + calendar grid |
| Tab switch | Inline skeleton rows for new tab |
| Exam detail drawer | Spinner + tab skeleton in drawer |
| Approve/Reject inline | Spinner in row action button + row dims |
| Bulk approve submit | Full-page overlay "Processing [N] exam approvals…" |

---

## 11. Role-Based UI Visibility

| Element | President G4 | Chairman G5 | CEO G4 | MD G5 |
|---|---|---|---|---|
| Page | ✅ | ✅ | ✅ view | ✅ view |
| [Approve] inline | ✅ | ✅ | ❌ | ❌ |
| [Reject] inline | ✅ | ✅ | ❌ | ❌ |
| [Modify] inline | ✅ | ✅ | ❌ | ❌ |
| [Bulk Approve] | ✅ | ✅ | ❌ | ❌ |
| [Override] (in drawer) | ❌ | ✅ | ❌ | ❌ |
| [Export Schedule] | ✅ | ✅ | ✅ | ✅ |
| Conflict tab | ✅ | ✅ | ✅ | ✅ |
| History tab | ✅ | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/exam-schedules/?status=pending` | JWT | Pending schedules |
| GET | `/api/v1/group/{id}/exam-schedules/?has_conflict=true` | JWT | Conflicting schedules |
| GET | `/api/v1/group/{id}/exam-schedules/{eid}/` | JWT | Schedule detail |
| GET | `/api/v1/group/{id}/exam-schedules/{eid}/conflicts/` | JWT | Conflict analysis |
| POST | `/api/v1/group/{id}/exam-schedules/{eid}/approve/` | JWT (G4 Pres) | Approve |
| POST | `/api/v1/group/{id}/exam-schedules/{eid}/reject/` | JWT (G4 Pres) | Reject + reason |
| POST | `/api/v1/group/{id}/exam-schedules/{eid}/request-modification/` | JWT (G4 Pres) | Mod request |
| POST | `/api/v1/group/{id}/exam-schedules/bulk-approve/` | JWT (G4 Pres) | Bulk approve |
| POST | `/api/v1/group/{id}/exam-schedules/{eid}/override/` | JWT (G5 Chairman) | Override |
| GET | `/api/v1/group/{id}/exam-schedules/calendar/` | JWT | Exam load calendar data |
| GET | `/api/v1/group/{id}/exam-schedules/export/` | JWT | Export schedule PDF |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | GET `.../exam-schedules/?tab=pending\|conflicting\|approved\|rejected` | `#exam-tab-content` | `innerHTML` |
| Search | `input delay:300ms` | GET `.../exam-schedules/?q=` | `#exam-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../exam-schedules/?branch=&stream=&class=&conflict=` | `#exam-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../exam-schedules/?sort=&dir=` | `#exam-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../exam-schedules/?page=` | `#exam-table-section` | `innerHTML` |
| Open exam approval drawer | `click` | GET `.../exam-schedules/{eid}/` | `#drawer-body` | `innerHTML` |
| Approve inline | `click` | POST `.../exam-schedules/{eid}/approve/` | `#exam-row-{eid}` | `outerHTML` |
| Reject (inline expand) | `click` | GET `.../exam-schedules/{eid}/reject-form/` | `#exam-row-{eid}-actions` | `innerHTML` |
| Reject submit | `submit` | POST `.../exam-schedules/{eid}/reject/` | `#exam-table-section` | `innerHTML` |
| Bulk approve confirm | `click` | POST `.../exam-schedules/bulk-approve/` | `#exam-table-section` | `innerHTML` |
| Override (Chairman) | `click` | POST `.../exam-schedules/{eid}/override/` | `#exam-row-{eid}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
