# 64 — Exam Paper Distribution Pipeline

> **URL:** `/group/acad/paper-distribution/`
> **File:** `64-paper-distribution.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Controller G3 · CAO G4 · Branch Principal (acknowledge + download via branch portal)

---

## 1. Purpose

The Exam Paper Distribution Pipeline is the secure, tracked workflow for delivering approved question papers from the group's central exam management system to individual branches before each examination. This page closes a critical gap: once a paper is approved by the Exam Controller and cleared for distribution, there was previously no mechanism to ensure its secure delivery, track who accessed it, when, and from which IP address, or confirm that every branch had acknowledged receipt before the exam started.

The security model is strict by design. Question papers represent high-value assets in the Indian education context — paper leakage is a serious criminal matter under the Prevention of Examination Malpractice Act, and institutions have faced significant reputational damage and legal consequences from leaks. This page implements a one-time-download-link model: each branch gets a unique, time-limited download link that becomes active only within the 24-hour window before the examination. The link is invalidated after first use. Branch must acknowledge receipt before the download is unlocked.

The pipeline status moves through five stages: Paper Approved (by Exam Controller) → Distributed to Branch (link generated and sent) → Branch Acknowledged (branch principal confirms they received the link) → Sealed (paper accessible but not yet downloaded; status during 24-hr pre-exam window) → Released (paper downloaded by branch). Branches that have not acknowledged receipt 12 hours before the exam receive an automatic red alert to the Exam Controller and the group's Exam Head.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ❌ No create | Oversight and audit view |
| Group Academic Director | G3 | ❌ | ❌ | No access |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ Full | ✅ Full — distribute, monitor | Primary owner |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ❌ | ❌ | No access |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |
| Branch Principal | Branch portal | ❌ (group page) | ❌ | Acknowledges and downloads via branch portal |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Gap-Fill  ›  Exam Paper Distribution Pipeline
```

### 3.2 Page Header
```
Exam Paper Distribution Pipeline                                    [Export Download Log ↓]
Secure paper delivery — tracked, one-time download links            (Exam Controller, CAO)
```

**Alert banner (conditional):** If any branch has not acknowledged receipt 12 hrs before exam:
> "🔴 [N] branches have not acknowledged paper receipt for exams starting in < 12 hours. Immediate action required."

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Papers Awaiting Distribution | Count |
| Distributed — Branch Acknowledged | Count |
| Distributed — Awaiting Acknowledgement | Count — amber |
| Not Acknowledged < 12 hrs | Count — red |
| Released (Downloaded) | Count |
| Exams in Next 24 Hours | Count |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Paper ID, Exam name, Branch name
- 300ms debounce

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Exam | Multi-select | Upcoming exams |
| Branch | Multi-select | All branches |
| Status | Multi-select | Paper Approved / Distributed / Acknowledged / Sealed / Released / Not Acknowledged Alert |
| Exam Date range | Date range picker | |
| Acknowledgement Status | Select | Acknowledged / Pending / Alert |

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Exam Controller |
| Paper ID | Text | ✅ | From Exam Paper Builder |
| Exam | Text | ✅ | |
| Stream | Badge | ✅ | |
| Branch | Text | ✅ | |
| Exam Date | Date | ✅ | |
| Exam Time | Time | ✅ | |
| Distributed At | Datetime | ✅ | When link was generated |
| Branch Acknowledged At | Datetime | ✅ | "—" if not yet |
| Download Window Opens | Datetime | ✅ | 24 hrs before exam start |
| Released At | Datetime | ✅ | When branch downloaded |
| Status | Badge | ✅ | Pipeline stage |
| Actions | — | ❌ | |

**Status badge colours:**
- Paper Approved: Blue
- Distributed: Teal
- Acknowledged: Green
- Sealed: Purple (in 24-hr window, not yet downloaded)
- Released: Grey
- Not Acknowledged Alert: Red (flashing)

**Default sort:** Exam Date ascending, then Status (Alert first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

### 4.4 Row Actions

| Action | Visible To | Drawer/Action | Notes |
|---|---|---|---|
| View Distribution Detail | Exam Controller, CAO | `distribution-detail` drawer 480px | Full download log + acknowledgement trail |
| Distribute Paper | Exam Controller | Inline confirm + generate link | Only shown if Status = Paper Approved |
| Resend Link | Exam Controller | Confirm modal | Generates new one-time link (invalidates old) |
| Send Acknowledgement Reminder | Exam Controller | Inline confirm | Sends WhatsApp/email to branch principal |
| View Download Log | Exam Controller, CAO | Inside `distribution-detail` drawer | Full IP log |

### 4.5 Bulk Actions (Exam Controller)

| Action | Notes |
|---|---|
| Distribute Selected Papers | Generates links for all selected rows |
| Send Reminder — Not Acknowledged | Sends reminders to all unacknowledged branches for selected exams |
| Export Download Log (XLSX) | Full access log for selected rows |

---

## 5. Drawers & Modals

### 5.1 Drawer: `distribution-detail`
- **Trigger:** View Distribution Detail row action
- **Width:** 480px
- **Header:** `[Paper ID] — [Exam Name] — [Branch] — [Exam Date]`

**Section 1 — Pipeline Status**
Visual step-indicator:
Paper Approved → Distributed → Acknowledged → Sealed → Released

Current stage highlighted.

**Section 2 — Distribution Details**
| Field | Value |
|---|---|
| Link generated at | Datetime |
| Link generated by | Staff name |
| Link valid from | 24 hrs before exam start |
| Link valid until | Exam start time |
| Link status | Active / Used / Expired / Invalidated |

**Section 3 — Acknowledgement Trail**
| Field | Value |
|---|---|
| Acknowledged at | Datetime |
| Acknowledged by | Branch Principal name |
| Acknowledgement method | Portal / Email receipt |

**Section 4 — Download Log (immutable)**
| Column | Notes |
|---|---|
| Attempt # | Sequential |
| Date & Time | |
| Action | Downloaded / Access Denied (wrong window) / Link already used |
| User | Branch portal user name |
| IP Address | Logged for security |
| Status | Success / Denied |

**Footer:** [Re-send Download Link] button (Exam Controller only) · [Export Log PDF] button

### 5.2 Modal: `distribute-confirm`
- **Width:** 420px
- **Content:** "Distribute [Paper ID] to [Branch] for [Exam Name] on [Date]? A one-time download link will be generated and sent to the branch principal."
- **Fields:** Notify branch principal via (Select: Email / WhatsApp / Both, default Both) · Message preview (editable)
- **Buttons:** [Confirm Distribute] · [Cancel]
- **On confirm:** Unique one-time link generated · Link stored with paper ID + branch ID + exam ID · Notification sent · Status updated to "Distributed"

### 5.3 Modal: `resend-link-confirm`
- **Width:** 420px
- **Content:** "Resend download link to [Branch]? The previous link will be invalidated. Reason is required."
- **Fields:** Reason (required, min 20 chars — e.g. "Branch principal reported link expired prematurely") · Channel (Email / WhatsApp / Both)
- **Buttons:** [Resend Link] · [Cancel]
- **On confirm:** Previous link invalidated (logged as "Invalidated" in download log) · New link generated · Notification sent

### 5.4 Alert: `not-acknowledged-12hrs`
**Triggered automatically by system at T-12 hours before exam:**
- Red persistent alert banner appears on page
- Email + WhatsApp sent to Exam Controller
- Entry created in distribution-detail drawer: "Auto-alert triggered at [datetime]"

---

## 6. Charts

### 6.1 Distribution Pipeline Status (Funnel)
- **Type:** Horizontal funnel / step count chart
- **Data:** Count of papers at each pipeline stage (current exam cycle)
- **Stages:** Approved → Distributed → Acknowledged → Sealed → Released
- **Tooltip:** Stage · Count
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Paper distributed | "Paper [ID] distributed to [Branch]. One-time link sent." | Success | 4s |
| Bulk distributed | "Papers distributed to [N] branches" | Success | 4s |
| Link resent | "New download link sent to [Branch]. Previous link invalidated." | Warning | 6s |
| Acknowledgement reminder sent | "Reminder sent to [Branch] principal" | Success | 4s |
| Branch acknowledged | "Branch [Name] acknowledged receipt at [time]" | Success | — (from branch portal event) |
| Paper downloaded | "Paper [ID] downloaded by [Branch] at [time]" | Info | — (from branch portal event) |
| Not-acknowledged alert | "ALERT: [N] branches have not acknowledged receipt. Exam < 12 hours." | Error | Manual dismiss |
| Export started | "Download log export preparing…" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No papers awaiting distribution | "No papers ready for distribution" | "Papers appear here once approved in the Exam Paper Builder" | — |
| No alerts | "All branches acknowledged" | "All branches with upcoming exams have acknowledged receipt" | — |
| No results match filters | "No papers match" | "Clear filters" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: alert banner check + stats bar + table (10 rows) |
| Table filter/search/sort/page | Inline skeleton rows |
| Distribution detail drawer | Spinner → sections render |
| Distribute confirm submit | Spinner in confirm button |
| Bulk distribute | Full-page overlay "Generating secure download links…" |

---

## 10. Role-Based UI Visibility

| Element | Exam Controller G3 | CAO G4 |
|---|---|---|
| Full pipeline table | ✅ | ✅ |
| Distribute Paper action | ✅ | ❌ |
| Resend Link action | ✅ | ❌ |
| Send Reminder action | ✅ | ❌ |
| View Distribution Detail | ✅ | ✅ |
| Download Log (in drawer) | ✅ | ✅ |
| Bulk actions | ✅ | ❌ |
| Export Download Log | ✅ | ✅ |
| Alert banner | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/paper-distribution/` | JWT | Pipeline list |
| GET | `/api/v1/group/{group_id}/acad/paper-distribution/stats/` | JWT | Stats bar + alert data |
| POST | `/api/v1/group/{group_id}/acad/paper-distribution/{id}/distribute/` | JWT (G3 Exam Ctrl) | Generate + send one-time link |
| POST | `/api/v1/group/{group_id}/acad/paper-distribution/bulk-distribute/` | JWT (G3 Exam Ctrl) | Bulk distribution |
| POST | `/api/v1/group/{group_id}/acad/paper-distribution/{id}/resend/` | JWT (G3 Exam Ctrl) | Resend (invalidate + new link) |
| POST | `/api/v1/group/{group_id}/acad/paper-distribution/{id}/remind/` | JWT (G3 Exam Ctrl) | Acknowledgement reminder |
| POST | `/api/v1/group/{group_id}/acad/paper-distribution/bulk-remind/` | JWT (G3 Exam Ctrl) | Bulk reminders |
| GET | `/api/v1/group/{group_id}/acad/paper-distribution/{id}/download-log/` | JWT (G3/G4) | Full download log (immutable read) |
| GET | `/api/v1/group/{group_id}/acad/paper-distribution/{id}/download-log/export/` | JWT | Log PDF export |
| GET | `/api/v1/group/{group_id}/acad/paper-distribution/export/?format=xlsx` | JWT | Full log export |
| GET | `/api/v1/group/{group_id}/acad/paper-distribution/charts/pipeline-status/` | JWT | Funnel chart |

**One-time download link endpoint (branch portal, time-gated):**
| GET | `/api/v1/group/{group_id}/acad/paper-distribution/download/{token}/` | JWT + token | Validates token, window, logs access, returns paper PDF |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../paper-distribution/?q=` | `#dist-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../paper-distribution/?filters=` | `#dist-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../paper-distribution/?sort=&dir=` | `#dist-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../paper-distribution/?page=` | `#dist-table-section` | `innerHTML` |
| Detail drawer | `click` | GET `.../paper-distribution/{id}/` | `#drawer-body` | `innerHTML` |
| Distribute confirm | `click` | POST `.../paper-distribution/{id}/distribute/` | `#dist-row-{id}` | `outerHTML` |
| Resend confirm | `click` | POST `.../paper-distribution/{id}/resend/` | `#dist-row-{id}` | `outerHTML` |
| Send reminder | `click` | POST `.../paper-distribution/{id}/remind/` | `#toast-container` | `beforeend` |
| Alert banner poll | `every 5m` | GET `.../paper-distribution/stats/` | `#alert-banner` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
