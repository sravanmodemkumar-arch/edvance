# 29 — Cross-Branch Results Publisher

> **URL:** `/group/acad/results/`
> **File:** `29-cross-branch-results-publisher.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** CAO G4 · Results Coordinator G3 · Exam Controller G3 · Academic MIS Officer G1

---

## 1. Purpose

The Cross-Branch Results Publisher is the authoritative publication control room for all group-wide exam results. Every result that reaches a student's portal or a parent's phone passes through this page — no branch can publish group-level results independently. For a group running 50 branches simultaneously with 80,000+ students, a single accidental early release or incorrect rank list can cause irreversible reputational damage and parent escalations. This page prevents that.

Each exam goes through a mandatory pipeline: marks uploaded by branch → moderated at group level → ranks computed → answer key finalised → CAO or Results Coordinator explicitly publishes. Only when all checklist items are green does the Publish button become active. This design makes partial or premature publication structurally impossible.

Every publish and unpublish action is recorded in an immutable audit trail — actor identity, timestamp, channel, and reason (for unpublish). This log feeds into compliance reporting and is accessible to the CAO and Chairman for governance reviews. The trail cannot be edited or deleted by any role in the system.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All columns | ✅ Full override — publish/unpublish/force | Can bypass checklist with documented reason |
| Group Academic Director | G3 | ✅ All columns | ❌ View only | No publish authority |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access to results section |
| Group Exam Controller | G3 | ✅ All columns | ✅ Trigger rank computation only | Cannot publish |
| Group Results Coordinator | G3 | ✅ All columns | ✅ Publish · Unpublish · Preview | Primary operator of this page |
| Group Stream Coord — MPC | G3 | ✅ Own stream rows | ❌ | Read-only, filtered to MPC |
| Group Stream Coord — BiPC | G3 | ✅ Own stream rows | ❌ | Read-only, filtered to BiPC |
| Group Stream Coord — MEC/CEC | G3 | ✅ Own stream rows | ❌ | Read-only, filtered to MEC/CEC |
| Group JEE/NEET Integration Head | G3 | ✅ JEE/NEET exams only | ❌ | Read-only |
| Group IIT Foundation Director | G3 | ✅ Foundation exams only | ❌ | Read-only |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ All columns | ❌ Read-only | Can view audit trail — no actions |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Results Publisher
```

### 3.2 Page Header
```
Cross-Branch Results Publisher                      [Export Audit Trail ↓]  [Settings ⚙]
[Group Name] · Academic Year [YYYY–YY]              Results Coordinator / CAO only
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Exams This Term | 24 |
| Fully Published | 11 |
| Pending Publication | 7 |
| Awaiting Moderation | 4 |
| Awaiting Upload | 2 |
| Unpublished (withdrawn) | 0 |

Stats bar refreshes on page load. No auto-refresh to prevent mid-action state changes.

---

## 4. Main Content

### 4.1 Search / Filters / Table

**Search:** Full-text across Exam Name — 300ms debounce, highlights match in Exam column.

**Advanced Filters (slide-in filter drawer):**

| Filter | Type | Options |
|---|---|---|
| Exam Type | Multi-select | Unit Test · Mid-Term · Annual · Mock Test · Coaching Test · Olympiad |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated JEE/NEET |
| Class | Multi-select | Class 6 through Class 12 |
| Publication Status | Multi-select | Awaiting Upload · Awaiting Moderation · Moderation Approved · Rank Computed · Ready to Publish · Published · Unpublished |
| Academic Year | Select | Current year · Previous year (archive view) |
| Date range | Date picker | Exam date range |

Active filter chips: Dismissible, "Clear All" link, count badge on filter button.

### 4.2 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | All | Row select for bulk actions |
| Exam Name | Text + link | ✅ | All | Opens publish-detail drawer |
| Stream | Badge | ✅ | All | MPC / BiPC etc. |
| Class | Text | ✅ | All | e.g. Class 11 |
| Branches Uploaded | Fraction | ✅ | All | e.g. 48/50 — red if incomplete |
| Moderation Status | Badge | ✅ | All | Pending · In Progress · Approved |
| Rank Computed | Badge | ✅ | All | Yes / No |
| Answer Key | Badge | ✅ | All | Not Uploaded · Published · Finalised |
| Publication Status | Badge | ✅ | All | Colour-coded — see below |
| Published At | Datetime | ✅ | All | Blank if not yet published |
| Published By | Text | ❌ | CAO · Results Coord | Actor name from audit trail |
| Actions | — | ❌ | Role-based | See row actions |

**Publication Status badge colours:**
- Awaiting Upload — Grey
- Awaiting Moderation — Amber
- Moderation Approved — Blue
- Rank Computed — Teal
- Ready to Publish — Green (pulsing outline)
- Published — Green solid
- Unpublished — Red

**Default sort:** Publication Status (Ready to Publish first), then Exam Name ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z exams" · Page jump input.

### 4.3 Row Actions

| Action | Icon | Visible To | Opens | Notes |
|---|---|---|---|---|
| View / Preview | Eye | All roles with access | `publish-detail` drawer 640px | Full pipeline status |
| Trigger Rank Computation | Calculator | Exam Controller · Results Coord · CAO | Confirm modal 420px | Only if all branches uploaded + moderated |
| Publish to Students | Broadcast | Results Coord · CAO | `publish-confirm` modal | Full checklist gate |
| Publish to Parents | Phone | Results Coord · CAO | `publish-parents-confirm` modal | SMS/WhatsApp channel |
| Unpublish | Lock | Results Coord · CAO | `unpublish-reason` modal | Reason mandatory — audited |
| View Audit Trail | Clock | CAO · Results Coord · MIS | `audit-trail-drawer` 560px | Immutable log entries |

### 4.4 Bulk Actions (shown when rows selected)

| Action | Visible To | Notes |
|---|---|---|
| Export Selected Audit Trail (CSV) | CAO · Results Coord · MIS | Exports audit entries for selected exams |
| Mark for Priority Processing | Results Coord · CAO | Flags selected exams for attention |

---

## 5. Drawers & Modals

### 5.1 Drawer: `publish-detail`
- **Trigger:** Eye icon row action or clicking Exam Name
- **Width:** 640px
- **Tabs:** Summary Stats · Per-Branch Status · Rank Distribution · Publish Channels · Audit Trail

#### Tab: Summary Stats
| Metric | Value |
|---|---|
| Total Students | N |
| Highest Score | N / Max N |
| Group Average | N% |
| Pass % (Group) | N% |
| Branches Included | N / 50 |
| Exam Date | DD MMM YYYY |

#### Tab: Per-Branch Status
Table: Branch Name · Students · Marks Uploaded (Y/N) · Upload Date · Moderation Status · Included in Rank (Y/N)

Rows where upload is missing shown in amber. Rows where moderation is rejected shown in red with rejection reason tooltip.

#### Tab: Rank Distribution
- Bar chart: Rank band buckets (1–10 · 11–50 · 51–100 · 101–500 · 500+) with student counts
- Percentile curve overlay (line chart)
- Rendered with Chart.js 4.x

#### Tab: Publish Channels
| Channel | Status | Last Published At | Action |
|---|---|---|---|
| Student Portal | Published / Not Published | Datetime | Publish / Unpublish |
| Parent SMS | Published / Not Published | Datetime | Publish / Unpublish |
| Parent WhatsApp | Published / Not Published | Datetime | Publish / Unpublish |

Each channel can be published/unpublished independently after initial group publish.

#### Tab: Audit Trail
Immutable table: Timestamp · Actor · Role · Action (Published / Unpublished / Rank Computed / Re-computed) · Channel · Reason (for unpublish) · IP Address

No edit, no delete, no filter — full chronological list.

---

### 5.2 Modal: `publish-confirm`
- **Trigger:** "Publish to Students" row action
- **Width:** 460px
- **Title:** "Publish Results — [Exam Name]"
- **Checklist (all must be green to enable Confirm):**
  - ✅ All branches have uploaded marks (shows N/50 uploaded)
  - ✅ All uploads moderation-approved
  - ✅ Group rank computed
  - ✅ Answer key finalised and published
  - ✅ CAO sign-off recorded (or you are the CAO)
- **Note if checklist items are red:** Shows which branches are missing, with [View Missing →] link
- **Optional comment:** Text field — "Add a note to this publication record (optional)"
- **Buttons:** [Confirm Publish] (primary green, disabled until all checklist green) + [Cancel]
- **On confirm:** Results published to student portal · Audit entry written · Toast shown · Row status updates to "Published"

**CAO override:** If CAO logs in, a "Publish with Override" secondary button appears with a mandatory reason field (min 30 chars). This allows publish even when checklist is incomplete.

---

### 5.3 Modal: `publish-parents-confirm`
- **Width:** 460px
- **Title:** "Notify Parents — [Exam Name]"
- **Channel selection:** SMS (checked by default) · WhatsApp (checked by default)
- **Preview:** Template of message sent to parents: "Dear Parent, [Student Name]'s result for [Exam Name] is now available. Score: [X/Y]. Rank: [N]. View details at [portal URL]."
- **Estimated reach:** N parents on SMS · N parents on WhatsApp
- **Buttons:** [Send Notifications] + [Cancel]
- **On confirm:** Notifications queued · Audit entry written · Toast: "Notifications sent to [N] parents"

---

### 5.4 Modal: `unpublish-reason`
- **Width:** 420px
- **Title:** "Unpublish Results — [Exam Name]"
- **Warning banner:** "Unpublishing removes student access immediately. This action is audited and cannot be reversed without re-publishing."
- **Fields:**
  - Reason (required, min 30 chars) — textarea
  - Notify students? (checkbox, default on)
  - Notify branch principals? (checkbox, default on)
- **Buttons:** [Confirm Unpublish] (danger red) + [Cancel]
- **On confirm:** Results hidden from student portal · Audit entry written with reason · Actor and timestamp logged · Toast shown

---

### 5.5 Modal: `rank-compute-confirm`
- **Width:** 420px
- **Title:** "Compute Group Rankings — [Exam Name]"
- **Shows:** Table of branches — Branch Name · Uploaded · Moderated · Students Count
- **Missing branches:** Listed in red with note "These branches are excluded from rank computation. Ranks will be computed for [N] branches only."
- **Fields:** Optional note (text) — reason for computing with partial data if applicable
- **Buttons:** [Compute Rankings] (primary) + [Cancel]
- **On confirm:** Rank computation job queued · Progress shown in row · Toast: "Rank computation started. This may take 2–5 minutes."
- **On completion:** Row status updates to "Rank Computed" via HTMX polling

---

### 5.6 Drawer: `audit-trail-drawer`
- **Trigger:** "View Audit Trail" row action
- **Width:** 560px
- **Content:** Immutable table — chronological, newest first
- **Columns:** Timestamp · Actor · Role · Action · Channel · Reason · IP Address
- **No actions available** — pure read display
- **Export:** "Download Audit Trail (CSV)" button at bottom of drawer — available to CAO, Results Coord, MIS Officer

---

## 6. Charts

### 6.1 Publication Pipeline Status (Funnel/Bar)
- **Type:** Horizontal stacked bar or funnel chart
- **Data:** Count of exams at each pipeline stage (Awaiting Upload / Awaiting Moderation / Ready / Published)
- **Colour:** Grey · Amber · Blue · Green (colorblind-safe)
- **Tooltip:** Stage name · Count · % of total exams
- **Export:** PNG

### 6.2 Results Published Per Month (Bar)
- **Type:** Vertical bar chart
- **X-axis:** Months (Apr–Mar)
- **Y-axis:** Count of result sets published
- **Tooltip:** Month · Count · Streams breakdown
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Rank computation triggered | "Rank computation started for [Exam Name]. Estimated time: 2–5 minutes." | Info | 6s |
| Rank computation complete | "Rankings computed for [Exam Name]. [N] students ranked." | Success | 5s |
| Results published to students | "Results for [Exam Name] published to student portal. [N] students notified." | Success | 5s |
| Parent notifications sent | "Notifications sent to [N] parents for [Exam Name]." | Success | 5s |
| Results unpublished | "Results for [Exam Name] unpublished. Reason recorded." | Warning | 6s |
| CAO override publish | "Results published with CAO override. Override reason recorded in audit trail." | Warning | 6s |
| Computation already running | "Rank computation already in progress for this exam." | Error | Manual |
| Export started | "Audit trail export preparing — download will begin shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No exams this term | "No exams scheduled this term" | "Exam results will appear here once exams are scheduled and marks are uploaded" | [View Exam Calendar →] |
| No results match search | "No results match" | "Try different search terms or clear filters" | [Clear Filters] |
| Filter returns empty | "No exams match your filters" | "Adjust your filters to see results in other states" | [Clear All Filters] |
| Audit trail empty | "No audit entries yet" | "Actions on this exam will be recorded here" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| Publish-detail drawer open | Spinner in drawer body · Skeleton tabs |
| Rank computation trigger | Progress spinner in row "Computing Rankings…" · Polling every 5s via HTMX |
| Publish confirm button | Spinner inside [Confirm Publish] button + button disabled |
| Unpublish confirm button | Spinner inside [Confirm Unpublish] button + button disabled |
| Audit trail drawer open | Spinner in drawer body |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Results Coord G3 | Exam Controller G3 | Stream Coords G3 | MIS G1 |
|---|---|---|---|---|---|
| [Export Audit Trail] header button | ✅ | ✅ | ❌ | ❌ | ✅ |
| Publish to Students action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Publish to Parents action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Unpublish action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Trigger Rank Computation | ✅ | ✅ | ✅ | ❌ | ❌ |
| CAO Override Publish button | ✅ | ❌ | ❌ | ❌ | ❌ |
| View Audit Trail action | ✅ | ✅ | ❌ | ❌ | ✅ |
| Published By column | ✅ | ✅ | ❌ | ❌ | ❌ |
| Filter drawer | ✅ | ✅ | ✅ | ✅ (stream filter locked to own stream) | ✅ |
| Per-Branch Status tab | ✅ | ✅ | ✅ | ❌ | ✅ |

> All role decisions enforced server-side in Django template context. No JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/results/` | JWT | Exam results list (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/results/stats/` | JWT | Summary stats bar |
| GET | `/api/v1/group/{group_id}/acad/results/{exam_id}/` | JWT | Publish-detail drawer data |
| GET | `/api/v1/group/{group_id}/acad/results/{exam_id}/per-branch/` | JWT | Per-branch status tab |
| GET | `/api/v1/group/{group_id}/acad/results/{exam_id}/rank-distribution/` | JWT | Rank distribution chart data |
| POST | `/api/v1/group/{group_id}/acad/results/{exam_id}/compute-ranks/` | JWT (G3+ Results/Exam/CAO) | Trigger rank computation |
| GET | `/api/v1/group/{group_id}/acad/results/{exam_id}/compute-status/` | JWT | Poll computation progress |
| POST | `/api/v1/group/{group_id}/acad/results/{exam_id}/publish/` | JWT (Results Coord/CAO) | Publish results (with channel param) |
| POST | `/api/v1/group/{group_id}/acad/results/{exam_id}/unpublish/` | JWT (Results Coord/CAO) | Unpublish with reason |
| POST | `/api/v1/group/{group_id}/acad/results/{exam_id}/notify-parents/` | JWT (Results Coord/CAO) | Trigger parent SMS/WhatsApp |
| GET | `/api/v1/group/{group_id}/acad/results/{exam_id}/audit-trail/` | JWT (CAO/Results Coord/MIS) | Immutable audit log |
| GET | `/api/v1/group/{group_id}/acad/results/export/audit/?format=csv` | JWT | Export audit trail CSV |
| GET | `/api/v1/group/{group_id}/acad/results/charts/pipeline-status/` | JWT | Pipeline funnel chart data |
| GET | `/api/v1/group/{group_id}/acad/results/charts/published-per-month/` | JWT | Publications per month chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Exam search input | `input delay:300ms` | GET `.../acad/results/?q=` | `#results-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../acad/results/?filters=` | `#results-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../acad/results/?sort=&dir=` | `#results-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../acad/results/?page=` | `#results-table-section` | `innerHTML` |
| Open publish-detail drawer | `click` | GET `.../acad/results/{id}/` | `#drawer-body` | `innerHTML` |
| Publish confirm | `click` | POST `.../acad/results/{id}/publish/` | `#results-row-{id}` | `outerHTML` |
| Unpublish confirm | `click` | POST `.../acad/results/{id}/unpublish/` | `#results-row-{id}` | `outerHTML` |
| Rank compute trigger | `click` | POST `.../acad/results/{id}/compute-ranks/` | `#results-row-{id}` | `outerHTML` |
| Poll computation status | `every 5s` (conditional) | GET `.../acad/results/{id}/compute-status/` | `#compute-status-{id}` | `innerHTML` |
| Open audit trail drawer | `click` | GET `.../acad/results/{id}/audit-trail/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
