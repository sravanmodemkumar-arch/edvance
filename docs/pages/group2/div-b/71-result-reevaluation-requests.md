# 71 — Result Re-evaluation Request Manager

> **URL:** `/group/acad/reevaluation/`
> **File:** `71-result-reevaluation-requests.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Controller G3 (full) · Results Coordinator G3 (view + decide) · CAO G4 (override)

---

## 1. Purpose

Manages the complete lifecycle of student requests to have subjective answer scripts re-checked.
Requests originate from students via the branch portal and route to the group Exam Controller for assignment
and review.

Without this page, mark disputes are handled via emails and phone calls — no audit trail, no SLA tracking,
and mark changes are not systematically propagated back to rank computation.

**Integration:** Approved mark changes automatically propagate to Result Moderation (Page 27) and
re-trigger Group Rank Computation (Page 30) if policy allows.

---

## 2. Role Access

| Role | Level | Can Assign | Can Review | Can Decide | Can Override | Notes |
|---|---|---|---|---|---|---|
| Exam Controller | G3 | ✅ | ✅ | ✅ | ❌ | Primary owner |
| Results Coordinator | G3 | ❌ | ✅ | ✅ | ❌ | View + publish final decision |
| CAO | G4 | ❌ | ✅ | ❌ | ✅ | Override exceptional cases only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Re-evaluation Requests
```

### 3.2 Page Header
```
Result Re-evaluation Request Manager                    [Export CSV ↓]
AY 2025–26 · [N] Open Requests · [M] Overdue
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Requests (this AY) | 284 |
| Open | 47 |
| Overdue (>15 working days) | 8 |
| Resolved — No Change | 198 |
| Resolved — Mark Revised | 39 |
| Overturned by CAO | 3 |

---

## 4. Main Table

### 4.1 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Request ID | Text | ✅ | Auto-generated |
| Student | Text (masked) | ❌ | Masked per DPDP |
| Branch | Text | ✅ | |
| Exam | Text | ✅ | Exam name |
| Subject | Badge | ✅ | |
| Original Mark | Number | ✅ | |
| Requested By | Text | ❌ | Student or Parent |
| Submitted Date | Date | ✅ | |
| Assigned To | Text | ✅ | Reviewer name |
| SLA Status | Badge | ✅ | On Track · At Risk · Overdue (red) |
| Status | Badge | ✅ | Submitted · Assigned · Under Review · Decision Pending · Resolved |
| Actions | — | ❌ | Assign · Review · View |

### 4.2 Filters

| Filter | Type | Options |
|---|---|---|
| Status | Multi-select | Submitted · Assigned · Under Review · Decision Pending · Resolved |
| Branch | Multi-select | Branch names |
| Subject | Multi-select | All subjects |
| Exam | Multi-select | Exam names |
| SLA | Select | On Track · Overdue |
| Date range | Date range | Submitted date range |

### 4.3 Search
- Full-text: Request ID, branch name
- 300ms debounce

---

## 5. Status Flow

```
Submitted (by student via branch portal)
   ↓
Assigned (Exam Controller assigns to a reviewer)
   ↓
Under Review (reviewer accesses answer script)
   ↓
Decision Pending (reviewer submits recommendation, awaiting final approval)
   ↓
Resolved (final decision recorded)
```

---

## 6. Drawers

### 6.1 Drawer: `request-review`
- **Trigger:** Review / View row action
- **Width:** 680px

**Tab: Request Details**

| Field | Value |
|---|---|
| Request ID | Auto |
| Student | Masked name + Roll No |
| Branch | Branch name |
| Exam | Exam name + date |
| Subject | Subject name |
| Original Mark | N / Max |
| Submission Date | Date |
| Student's Reason | Text (student-entered reason) |

**Tab: Answer Script**
- Scanned answer script upload (PDF/image) — uploaded by branch coordinator
- If not uploaded: [Request Upload from Branch] button — sends notification to branch
- Preview: embedded PDF viewer

**Tab: Reviewer Notes**

| Field | Type | Required |
|---|---|---|
| Assign to Reviewer | Search + select user | ✅ (to advance to Under Review) |
| Reviewer Notes | Rich text | ✅ (on decision) |
| Marks Breakdown | Per-question mark entry (Q1: N/Max, Q2: N/Max...) | Optional |
| Recommended Mark | Number | ✅ (on decision) |

**Tab: Decision**

| Field | Type | Required |
|---|---|---|
| Decision | Select | No Change · Mark Revised · Re-paper (full re-exam) | ✅ |
| New Mark | Number | Conditional (required if Mark Revised) | |
| Reason | Text | ✅ Min 50 chars |
| Notify Student? | Toggle | Default: On |
| Notify Branch? | Toggle | Default: On |

- **[Submit Decision]** button — finalises and propagates mark change
- **[CAO Override]** — visible to CAO only, allows reversal of Resolved decisions

**Tab: Audit Trail**
- Complete immutable log: Status changes · Who changed · When · Mark history
- Read-only for all roles

---

## 7. Mark Change Propagation

When decision = "Mark Revised":
1. Updated mark sent to Result Moderation (Page 27) as an override entry
2. If policy allows: Group Rank Computation (Page 30) re-triggered for the affected exam
3. Updated result visible in Cross-Branch Results Publisher (Page 29) with "Revised" tag
4. Student notified via portal + WhatsApp

---

## 8. SLA Tracking

| SLA Rule | Detail |
|---|---|
| Resolution window | 15 working days from submission |
| At Risk | 12–14 working days elapsed |
| Overdue | 15+ working days — red badge, alert to CAO |
| Auto-escalation | Overdue request auto-escalated to CAO after 15 days |

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Request assigned | "Request [ID] assigned to [Reviewer]." | Success | 4s |
| Decision submitted — No Change | "Decision recorded: No change for [Student] in [Subject]." | Success | 4s |
| Decision submitted — Revised | "Mark revised to [N]. Rank recomputation triggered." | Success | 5s |
| CAO override | "CAO override applied. Decision reversed." | Warning | 6s |
| Answer script upload requested | "Upload request sent to [Branch] Principal." | Info | 4s |
| SLA overdue | "8 requests are overdue. Review immediately." | Error | Manual |

---

## 10. Empty States

| Condition | Heading | Description |
|---|---|---|
| No requests | "No re-evaluation requests" | "No students have submitted mark dispute requests this year." |
| Filter empty | "No requests match filters" | "Try clearing filters." |
| No answer script | "Answer script not uploaded" | "Branch has not uploaded the answer script." |

---

## 11. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: stats bar + 8 table rows |
| Filter/search/sort | Inline skeleton rows |
| Review drawer open | Spinner + skeleton tabs |
| Answer script preview | Spinner in PDF viewer area |

---

## 12. Role-Based UI Visibility

| Element | Exam Ctrl G3 | Results Coord G3 | CAO G4 |
|---|---|---|---|
| [Assign reviewer] | ✅ | ❌ | ❌ |
| [Submit Decision] | ✅ | ✅ | ❌ |
| [CAO Override] | ❌ | ❌ | ✅ |
| [Request Script Upload] | ✅ | ❌ | ❌ |
| Audit Trail tab | ✅ | ✅ | ✅ |
| Student name (unmasked) | ✅ | ✅ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/reevaluation/` | JWT (G3+) | Request list |
| GET | `/api/v1/group/{id}/acad/reevaluation/stats/` | JWT (G3+) | Summary stats |
| GET | `/api/v1/group/{id}/acad/reevaluation/{rid}/` | JWT (G3+) | Request detail (all tabs) |
| PUT | `/api/v1/group/{id}/acad/reevaluation/{rid}/assign/` | JWT (G3, ExamCtrl) | Assign reviewer |
| PUT | `/api/v1/group/{id}/acad/reevaluation/{rid}/decide/` | JWT (G3) | Submit decision |
| PUT | `/api/v1/group/{id}/acad/reevaluation/{rid}/override/` | JWT (G4) | CAO override |
| POST | `/api/v1/group/{id}/acad/reevaluation/{rid}/request-script/` | JWT (G3) | Request script from branch |
| GET | `/api/v1/group/{id}/acad/reevaluation/export/?format=csv` | JWT (G3+) | Export CSV |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../reevaluation/?q=` | `#reeval-table-body` | `innerHTML` |
| Filter | `click` | GET `.../reevaluation/?filters=` | `#reeval-section` | `innerHTML` |
| Pagination | `click` | GET `.../reevaluation/?page=` | `#reeval-section` | `innerHTML` |
| Open review drawer | `click` | GET `.../reevaluation/{id}/` | `#drawer-body` | `innerHTML` |
| Assign reviewer | `submit` | PUT `.../assign/` | `#drawer-tab-body` | `innerHTML` |
| Submit decision | `submit` | PUT `.../decide/` | `#drawer-tab-body` | `innerHTML` |
| CAO override | `click` | PUT `.../override/` | `#drawer-tab-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
