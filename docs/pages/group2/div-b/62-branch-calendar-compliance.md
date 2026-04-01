# 62 — Branch Calendar Compliance

> **URL:** `/group/acad/calendar-compliance/`
> **File:** `62-branch-calendar-compliance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Calendar Manager G3 · CAO G4 · Academic Director G3

---

## 1. Purpose

The Branch Calendar Compliance page is the monitoring control that ensures branches are actually following the group academic calendar — not diverging unilaterally by skipping mandatory events, rescheduling exams without notification, or declaring unilateral holidays. In a decentralised institution group, branches have considerable operational autonomy. This page exists to detect when that autonomy crosses into non-compliance with group directives.

The compliance calculation compares each branch's actual calendar (as recorded in the branch portal) against the group's published mandatory event list. For each mandatory event in scope for a branch, the system checks whether that event has been confirmed, scheduled at the correct date, and (where post-event reporting is required) whether a report has been submitted. Deviations — events scheduled on wrong dates, events not scheduled at all, or extra events scheduled that conflict with mandatory ones — are counted as deviations.

A branch with more than three deviations triggers an automatic alert to the Calendar Manager and the CAO. Branches with perfect compliance are visually distinguished with a green badge. The side-by-side view in the branch calendar detail drawer — group calendar events on the left, branch calendar events on the right, deviations highlighted in amber — makes it immediately clear to the Calendar Manager what conversation to have with the branch principal.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ❌ No create | Escalation recipient |
| Group Academic Director | G3 | ✅ Full | ❌ No create | Advisory oversight |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ❌ | ❌ | No access |
| Group Academic Calendar Manager | G3 | ✅ Full | ✅ Send reminders · Escalate | Primary owner |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Academic Calendar Management  ›  Branch Calendar Compliance
```

### 3.2 Page Header
```
Branch Calendar Compliance                                          [Export Report ↓]
Compliance vs Group Academic Calendar · [Academic Year]    Alerts: [N] branches >3 deviations
```

**Alert banner (conditional):** If any branch has > 3 deviations:
> "⚠ [N] branches have more than 3 calendar deviations. CAO has been notified. Review below."

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Branches Monitored | Count |
| Fully Compliant (0 deviations) | Count — green |
| Minor Deviations (1–3) | Count — amber |
| High Deviations (> 3) | Count — red |
| Mandatory Events This Term | Count |
| Avg Compliance Score (Group) | % |

---

## 4. Main Content

### 4.1 Search
- Full-text across: Branch name, Branch code
- 300ms debounce

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Zone | Multi-select | Group zones |
| Compliance Score Band | Select | Compliant (100%) / Minor issues (70–99%) / Non-compliant (< 70%) |
| Deviations | Select | 0 / 1–3 / > 3 |
| Month | Month picker | |

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| Mandatory Events in Scope | Number | ✅ | How many group mandatory events apply to this branch |
| Events Confirmed | Number | ✅ | Branch has confirmed scheduling |
| Deviation Count | Number | ✅ | Events not on schedule or wrong date |
| Compliance Score | Progress bar + % | ✅ | (Confirmed / Total) × 100 |
| PTMs Held | Badge | ✅ | All / Some / None |
| Working Day Count | Number | ✅ | From Holiday Manager (page 61) |
| Last Sync | Datetime | ✅ | When branch portal data was last updated |
| Actions | — | ❌ | |

**Compliance Score colour:** Green ≥ 90% · Amber 70–89% · Red < 70%

**Default sort:** Deviation Count descending (most non-compliant first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

### 4.4 Row Actions

| Action | Visible To | Drawer | Notes |
|---|---|---|---|
| View Compliance Detail | All roles | `branch-calendar-detail` drawer 480px | Side-by-side comparison |
| Send Reminder | Calendar Manager | Confirm modal | Reminder to branch principal |
| Escalate to CAO | Calendar Manager | Confirm modal | Triggers CAO notification |

### 4.5 Bulk Actions (Calendar Manager)

| Action | Notes |
|---|---|
| Send Reminder to Non-Compliant | Sends reminders to all branches with > 0 deviations |
| Export Compliance Report (XLSX) | All branches in current filter |

---

## 5. Drawers & Modals

### 5.1 Drawer: `branch-calendar-detail`
- **Trigger:** View Compliance Detail row action
- **Width:** 480px
- **Header:** `[Branch Name] — Calendar Compliance — [Month/Term]`

**Side-by-side comparison panel:**
Two columns — **Group Calendar** | **Branch Calendar**

Each mandatory event listed as a row:
| Group Event | Group Date | Branch Status | Branch Date | Deviation |
|---|---|---|---|---|
| Term 1 PTM | 15 Aug 2025 | ✅ Confirmed | 15 Aug 2025 | None |
| Unit Test 1 — MPC | 20 Aug 2025 | ⚠ Wrong date | 23 Aug 2025 | +3 days |
| Annual Sports Day | 10 Sep 2025 | ❌ Not scheduled | — | Not scheduled |

**Deviations highlighted in amber/red.**

**Footer buttons:** [Send Reminder to Branch] · [Escalate to CAO]

### 5.2 Modal: `send-reminder-confirm`
- **Width:** 420px
- **Content:** "Send compliance reminder to [Branch] principal?"
- **Fields:** Message preview (editable, max 400 chars) · Channel (Email / WhatsApp / Both)
- **Buttons:** [Send Reminder] · [Cancel]

### 5.3 Modal: `escalate-to-cao-confirm`
- **Width:** 420px
- **Content:** "Escalate [Branch]'s [N] calendar deviations to the CAO?"
- **Fields:** Notes to CAO (Textarea, optional)
- **Buttons:** [Escalate] · [Cancel]
- **On confirm:** CAO notification sent · Audit log entry

---

## 6. Charts

### 6.1 Compliance Score by Branch (Horizontal Bar)
- **Type:** Horizontal bar
- **Data:** Compliance score % per branch
- **Reference line:** At 90% (compliant threshold)
- **Colour:** Green ≥ 90% · Amber 70–89% · Red < 70%
- **Tooltip:** Branch · Score: X% · Deviations: N
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Reminder sent | "Compliance reminder sent to [Branch] principal" | Success | 4s |
| Bulk reminders sent | "Reminders sent to [N] non-compliant branches" | Success | 4s |
| Escalated to CAO | "[Branch] escalated to CAO. CAO has been notified." | Success | 4s |
| Auto-alert (system) | "[Branch] has > 3 deviations. CAO notified automatically." | Warning | — (system) |
| Export started | "Compliance report export preparing…" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No deviations detected | "All branches are compliant" | "No calendar deviations detected across any branch. Keep monitoring." | — |
| No branches in scope | "No branches to monitor" | "No mandatory events have been published for this period" | — |
| No results match filters | "No branches match" | "Clear filters to see all branches" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + alert banner + table (10 rows) |
| Table filter/search/sort/page | Inline skeleton rows |
| Compliance detail drawer | Spinner → side-by-side table renders |
| Charts load | Skeleton bar chart |

---

## 10. Role-Based UI Visibility

| Element | Calendar Mgr G3 | CAO G4 | Academic Dir G3 |
|---|---|---|---|
| Full compliance table | ✅ | ✅ | ✅ |
| View detail drawer | ✅ | ✅ | ✅ |
| Send Reminder | ✅ | ❌ | ❌ |
| Escalate to CAO | ✅ | ❌ | ❌ |
| Bulk actions | ✅ | ❌ | ❌ |
| Export | ✅ | ✅ | ✅ |
| Charts | ✅ | ✅ | ✅ |
| Alert banner | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/calendar-compliance/` | JWT | Branch compliance list |
| GET | `/api/v1/group/{group_id}/acad/calendar-compliance/stats/` | JWT | Stats bar + alert data |
| GET | `/api/v1/group/{group_id}/acad/calendar-compliance/{branch_id}/` | JWT | Branch detail + side-by-side data |
| POST | `/api/v1/group/{group_id}/acad/calendar-compliance/{branch_id}/remind/` | JWT (G3 Cal Mgr) | Send reminder |
| POST | `/api/v1/group/{group_id}/acad/calendar-compliance/{branch_id}/escalate/` | JWT (G3 Cal Mgr) | Escalate to CAO |
| POST | `/api/v1/group/{group_id}/acad/calendar-compliance/bulk-remind/` | JWT (G3 Cal Mgr) | Bulk reminders |
| GET | `/api/v1/group/{group_id}/acad/calendar-compliance/export/?format=xlsx` | JWT | Export |
| GET | `/api/v1/group/{group_id}/acad/calendar-compliance/charts/score-by-branch/` | JWT | Bar chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../calendar-compliance/?q=` | `#compliance-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../calendar-compliance/?filters=` | `#compliance-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../calendar-compliance/?sort=&dir=` | `#compliance-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../calendar-compliance/?page=` | `#compliance-table-section` | `innerHTML` |
| Detail drawer | `click` | GET `.../calendar-compliance/{bid}/` | `#drawer-body` | `innerHTML` |
| Send reminder confirm | `click` | POST `.../calendar-compliance/{bid}/remind/` | `#toast-container` | `beforeend` |
| Escalate confirm | `click` | POST `.../calendar-compliance/{bid}/escalate/` | `#toast-container` | `beforeend` |
| Bulk remind | `click` | POST `.../calendar-compliance/bulk-remind/` | `#toast-container` | `beforeend` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
