# 47 — IEP Manager

> **URL:** `/group/acad/special-ed/iep/`
> **File:** `47-iep-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Special Education Coordinator G3 · CAO G4 · Academic Director G3 (view) · Branch Counsellor (branch portal, view own branch IEPs)

---

## 1. Purpose

The IEP Manager is the lifecycle management system for Individual Education Plans — the legally and pedagogically required documents that define personalised learning goals, teaching strategies, accommodation provisions, and review schedules for each student with special educational needs. In the Indian context, CBSE's Inclusive Education guidelines and NCPCR standards require every identified student to have a documented IEP that is reviewed at least annually, and more frequently for students with severe or complex needs.

An IEP is not a static document. It begins with an initial plan created by the Special Education Coordinator in consultation with the branch counsellor, teacher, and parent. Over the academic year it must be reviewed — typically once per term — to assess progress against each goal, update strategies that are not working, and set new targets. Goals must be written in SMART format (Specific, Measurable, Achievable, Relevant, Time-bound) so that progress can be assessed objectively rather than subjectively.

This page manages the full IEP lifecycle: create, review, update, and close. It flags overdue reviews with a red badge count in the navigation bar so the Coordinator never loses track of compliance obligations. It sends automated email reminders 14 days before each scheduled review. When an IEP is exported as PDF for sharing with parents, internal reviewer notes and psychological assessment details are automatically redacted — parents receive a clean, constructive plan document. Every action on every IEP is immutably audited.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full — all IEPs, full names | ✅ Sign-off only | Provides formal sign-off on IEP completion |
| Group Academic Director | G3 | ✅ View all IEPs | ❌ No create/edit | Advisory oversight |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | Accesses accommodations via page 48 |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ✅ Full | ✅ Full CRUD + review | Primary owner |
| Group Academic MIS Officer | G1 | ✅ Anonymised count only | ❌ | Count of IEPs per status only — no student PII |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |
| Branch Counsellor | Branch portal | ✅ Own branch IEPs only | ❌ (submit progress notes) | Access via branch portal, not this group page |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Special Education  ›  IEP Manager
```

### 3.2 Page Header
```
IEP Manager                                             [+ New IEP]  [Export IEP Register ↓]
Individual Education Plans — [Group Name]                          (Special Ed Coord only)
```

**Nav badge:** Red badge on "IEP Manager" nav item showing count of overdue IEPs. Persists until all overdue IEPs are reviewed.

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Active IEPs | Count |
| Reviews Overdue | Count — red |
| Reviews Due This Month | Count — amber |
| Reviews Due Next Month | Count |
| IEPs Completed / Closed This Year | Count |
| CAO Sign-off Pending | Count — amber |

---

## 4. Main Content

### 4.1 Search
- Full-text across: IEP ID, Student Name (G3+ only), Student ID
- 300ms debounce · Highlights match in ID column

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Status | Multi-select | Active · Review Due · Overdue · Completed · Discontinued |
| Review Due | Select | Overdue / Due this month / Due next month / Upcoming (next 3 months) |
| Goals Met % | Select | < 25% · 25–50% · 50–75% · ≥ 75% |
| CAO Sign-off | Select | Pending / Completed |
| Created in Academic Year | Select | Current + last 3 years |

Active filter chips dismissible. "Clear All" link. Filter count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Bulk select (Special Ed Coord only) |
| IEP ID | Text | ✅ | System-generated e.g. IEP-2025-00142 |
| Student Name | Text | ✅ | Masked for G3 Academic Dir; full for Spec Ed Coord and CAO |
| Student ID | Text | ✅ | |
| Branch | Text | ✅ | |
| Class | Badge | ✅ | |
| Created Date | Date | ✅ | |
| Last Review | Date | ✅ | Red if > 12 months ago |
| Next Review Due | Date | ✅ | Red if overdue; amber if ≤ 14 days |
| Goals Met % | Progress bar + % | ✅ | Calculated from last review |
| Status | Badge | ✅ | Active / Review Due / Overdue / Completed / Discontinued |
| CAO Sign-off | Badge | ✅ | Pending / Done |
| Actions | — | ❌ | Role-based |

**Default sort:** Status (Overdue first, then Review Due, then Active), then Next Review Due ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Action | Notes |
|---|---|---|---|---|
| View IEP | Eye | Special Ed Coord, CAO, Academic Dir | `iep-view` drawer 560px | Full plan read-only |
| Conduct Review | Clipboard | Special Ed Coord | `iep-review` drawer 640px | Only active when status = Review Due or Overdue |
| Edit IEP | Pencil | Special Ed Coord | `iep-create` drawer 680px (pre-filled) | Edit plan between reviews |
| Export PDF | Download | Special Ed Coord, CAO | PDF download | Parent-safe version — internal notes redacted |
| Sign Off | Check | CAO only | Confirm modal | Marks IEP as CAO-approved |
| Discontinue | Stop | Special Ed Coord | Confirm modal | Closes IEP — requires reason |

### 4.5 Bulk Actions (Special Ed Coord only)

| Action | Notes |
|---|---|
| Send Review Reminder — Selected | Emails branch counsellors for selected IEPs due for review |
| Export IEP Register (XLSX) — Selected | Export selected IEP summary rows |

---

## 5. Drawers & Modals

### 5.1 Drawer: `iep-create` — Create / Edit IEP
- **Trigger:** [+ New IEP] header button or Edit row action
- **Width:** 680px
- **Tabs:** Student Link · Learning Goals · Teaching Strategies · Support Hours · Assessment Accommodations · Review Schedule · Sign-off

#### Tab: Student Link
| Field | Type | Required | Notes |
|---|---|---|---|
| Student | Search + select | ✅ | Searches Special Needs Registry (page 46); only registered students |
| IEP Version | Auto | — | System-assigned; increments on each new IEP for the same student |
| Effective From | Date | ✅ | |
| Academic Year | Select | ✅ | |
| Primary Teacher | Search + select | ✅ | From branch teacher roster |
| Branch Counsellor | Search + select | ✅ | From branch staff |
| Parent/Guardian Involvement | Textarea | ❌ | Notes on parent participation in IEP creation |

#### Tab: Learning Goals
- **Goal builder:** Repeater — add up to 10 goals
- **Each goal row:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Goal Title | Text | ✅ | Brief label e.g. "Reading fluency" |
| Domain | Select | ✅ | Academic / Social / Communication / Motor / Behavioural |
| SMART Goal Statement | Textarea | ✅ | Full SMART-format goal; min 30 chars; tooltip shows SMART guide |
| Baseline | Text | ✅ | Current level before intervention |
| Target | Text | ✅ | Measurable outcome |
| Target Date | Date | ✅ | Cannot exceed review schedule dates |
| Measurement method | Text | ✅ | How progress will be measured (e.g. "Weekly reading test score") |
| Success criteria | Text | ✅ | e.g. "Reads 60 words per minute with < 5 errors" |

- [+ Add Goal] button · [Remove] icon per goal row

#### Tab: Teaching Strategies
| Field | Type | Required | Notes |
|---|---|---|---|
| Strategies for each goal | Textarea per goal | ✅ | Auto-linked to goals from previous tab |
| Classroom modifications | Textarea | ❌ | Seating, lighting, noise reduction etc. |
| Assistive technology | Toggle | ❌ | If on: type of technology used |
| Internal reviewer notes | Textarea | ❌ | **Redacted in parent PDF export** |

#### Tab: Support Hours
| Field | Type | Required | Notes |
|---|---|---|---|
| In-class support hours/week | Number | ✅ | |
| Pull-out sessions (specialist) hours/week | Number | ❌ | |
| Support staff name | Text | ❌ | |
| External support provider | Text | ❌ | Therapist/specialist name if external |

#### Tab: Assessment Accommodations
| Field | Type | Required | Notes |
|---|---|---|---|
| Extra time | Select | ❌ | None / +30 min / +60 min |
| Scribe | Toggle | ❌ | |
| Separate exam room | Toggle | ❌ | |
| Large font paper | Toggle | ❌ | |
| Oral exam option | Toggle | ❌ | |
| Reader | Toggle | ❌ | |
| Other accommodations | Textarea | ❌ | Max 300 chars |
| Approving authority | Text | ❌ | Psychologist/medical authority |

Accommodations auto-propagate to Accommodation Tracker (page 48) for exam scheduling.

#### Tab: Review Schedule
| Field | Type | Required | Notes |
|---|---|---|---|
| Review frequency | Select | ✅ | Monthly / Term (every 3–4 months) / Half-yearly / Annual |
| Next review date | Date | ✅ | Auto-calculated based on frequency; editable |
| Subsequent review dates | Auto-generated list | — | Shows all review dates for the year |
| Remind N days before review | Select | ✅ | 7 / 14 / 21 days; default 14 |
| Remind who | Multi-select | ✅ | Special Ed Coord · Branch Counsellor · Primary Teacher · Parent |

#### Tab: Sign-off
| Field | Type | Required | Notes |
|---|---|---|---|
| Parent/Guardian acknowledgement | Toggle | ✅ | Confirms parent was involved in IEP creation |
| Parent signature date | Date | Conditional | Required if acknowledgement = Yes |
| Teacher acknowledgement | Toggle | ✅ | Primary teacher has read the plan |
| CAO sign-off | Display only | — | Shows "Pending" or "Signed off by [Name] on [Date]" |

- **Submit:** "Save IEP" — all required tabs must be valid (tab dot indicators)
- **On success:** IEP created with status Active · Auto-reminder schedule created · Toast

### 5.2 Drawer: `iep-review`
- **Trigger:** "Conduct Review" row action
- **Width:** 640px
- **Tabs:** Progress on Each Goal · Updated Strategies · Review Notes · Next Review Date · Approve

#### Tab: Progress on Each Goal
- One section per goal from the current IEP
- **Each section:**
  - Goal statement (read-only display)
  - Progress status: Select → On Track / Met / Partially Met / Not Met / No Longer Applicable
  - Evidence / observation notes: Textarea (required, min 20 chars)
  - % achievement: Number (0–100)

#### Tab: Updated Strategies
- For goals rated "Not Met" or "Partially Met" only
- Updated strategy textarea per affected goal
- New target date if goal extended

#### Tab: Review Notes
| Field | Type | Required | Notes |
|---|---|---|---|
| Overall summary | Textarea | ✅ | Review narrative; min 50 chars |
| Parent was present | Toggle | ✅ | |
| Student was present | Toggle | ✅ | |
| Key decisions made | Textarea | ✅ | |
| Internal reviewer notes | Textarea | ❌ | **Redacted from parent PDF** |

#### Tab: Next Review Date
| Field | Type | Required | Notes |
|---|---|---|---|
| Next review date | Date | ✅ | Auto-suggested based on frequency |
| Adjust review frequency | Select | ❌ | Can change cadence at review |
| Remind who | Multi-select | ✅ | Pre-filled from original schedule |

#### Tab: Approve
- Summary: Goals Met % (calculated), Status recommendation (Continue / Close / Modify significantly)
- [Submit Review] button — requires all tabs complete
- On submit: IEP status updated · Review logged in version history · Next reminder scheduled · CAO notified for sign-off if goals met ≥ 80%

### 5.3 Drawer: `iep-view`
- **Width:** 560px
- **Tabs:** Current Plan · Version History
- **Current Plan:** All IEP fields read-only; goals, strategies, accommodations, review schedule
- **Version History:** Table of all past reviews — date, reviewer, Goals Met %, status change. Click any row to view that version read-only.

### 5.4 Modal: `cao-signoff-confirm`
- **Width:** 420px
- **Content:** "Confirm sign-off on IEP [ID] for [Student Name]?"
- **Fields:** Sign-off notes (optional, textarea)
- **Buttons:** [Confirm Sign-off] · [Cancel]
- **On confirm:** IEP sign-off date/name recorded · Status badge updated · Audit log

### 5.5 Modal: `discontinue-confirm`
- **Width:** 420px
- **Content:** "Discontinue IEP [ID] for [Student Name]? This will archive the plan."
- **Fields:** Reason (Select): Student left institution / Goals all met — transitioning out / No longer eligible / Other · Details (Textarea, min 30 chars)
- **Buttons:** [Confirm Discontinue] (danger) · [Cancel]

---

## 6. Charts

### 6.1 IEP Review Compliance by Branch (Heatmap)
- **Type:** Heatmap table
- **Rows:** Branches
- **Columns:** Academic months
- **Cell value:** % of IEPs reviewed on time in that month for that branch
- **Colour:** Red < 50% · Amber 50–80% · Green > 80%
- **Tooltip:** Branch · Month · Reviews due: N · Reviewed: N · %
- **Export:** PNG

### 6.2 Goals Achievement Distribution (Donut)
- **Type:** Donut
- **Data:** Goals split by: Met / Partially Met / Not Met / On Track / No Longer Applicable
- **Tooltip:** Category · Count · %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| IEP created | "IEP created for [Student ID]. Review scheduled." | Success | 4s |
| IEP updated | "IEP updated for [Student ID]" | Success | 4s |
| Review submitted | "IEP review recorded. Next review: [Date]. Reminders scheduled." | Success | 4s |
| CAO sign-off complete | "IEP [ID] signed off by CAO" | Success | 4s |
| IEP discontinued | "IEP [ID] discontinued. Record archived." | Warning | 6s |
| Review reminder sent | "Review reminder sent to [N] contacts" | Success | 4s |
| Auto-reminder (system) | "Reminder: IEP review for [Student ID] is due in 14 days" | Info | — (email only) |
| PDF exported | "IEP PDF exported (internal notes redacted)" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No IEPs yet | "No IEPs created" | "Create the first IEP for a student registered in the Special Needs Registry" | [+ New IEP] |
| No IEPs match filters | "No IEPs match your filters" | "Clear filters to see all IEPs" | [Clear Filters] |
| No overdue IEPs | "All IEPs are on track" | "No overdue reviews — keep monitoring the upcoming reviews" | — |
| Version history — no past reviews | "No previous reviews" | "This IEP was created but not yet reviewed" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) + nav badge |
| Table filter/search/sort/page | Inline skeleton rows |
| iep-create drawer open | Spinner → tabbed form |
| iep-review drawer open | Spinner → goal sections load |
| iep-view drawer open | Spinner → read-only content |
| Charts load | Skeleton chart placeholders |
| PDF export | Spinner in export button |

---

## 10. Role-Based UI Visibility

| Element | Spec Ed Coord G3 | CAO G4 | Academic Dir G3 | MIS G1 |
|---|---|---|---|---|
| Full IEP table | ✅ | ✅ | ✅ (names masked) | ❌ (stats bar only) |
| [+ New IEP] button | ✅ | ❌ | ❌ | ❌ |
| Conduct Review action | ✅ | ❌ | ❌ | ❌ |
| Edit IEP action | ✅ | ❌ | ❌ | ❌ |
| Sign Off action | ❌ | ✅ | ❌ | ❌ |
| Discontinue action | ✅ | ❌ | ❌ | ❌ |
| Export PDF (parent version) | ✅ | ✅ | ❌ | ❌ |
| Version History tab | ✅ | ✅ | ✅ | ❌ |
| Internal reviewer notes (in drawers) | ✅ | ✅ | ❌ | ❌ |
| Nav badge (overdue count) | ✅ | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/special-ed/iep/` | JWT | List IEPs (paginated, filtered) |
| GET | `/api/v1/group/{group_id}/acad/special-ed/iep/stats/` | JWT | Stats bar data |
| GET | `/api/v1/group/{group_id}/acad/special-ed/iep/overdue-count/` | JWT | Nav badge count |
| POST | `/api/v1/group/{group_id}/acad/special-ed/iep/` | JWT (G3 Spec Ed) | Create IEP |
| GET | `/api/v1/group/{group_id}/acad/special-ed/iep/{id}/` | JWT (G3+) | IEP detail (triggers access log) |
| PUT | `/api/v1/group/{group_id}/acad/special-ed/iep/{id}/` | JWT (G3 Spec Ed) | Update IEP |
| POST | `/api/v1/group/{group_id}/acad/special-ed/iep/{id}/review/` | JWT (G3 Spec Ed) | Submit review |
| GET | `/api/v1/group/{group_id}/acad/special-ed/iep/{id}/versions/` | JWT (G3+) | Version history |
| POST | `/api/v1/group/{group_id}/acad/special-ed/iep/{id}/signoff/` | JWT (G4 CAO) | CAO sign-off |
| PATCH | `/api/v1/group/{group_id}/acad/special-ed/iep/{id}/discontinue/` | JWT (G3 Spec Ed) | Discontinue IEP |
| GET | `/api/v1/group/{group_id}/acad/special-ed/iep/{id}/export-pdf/` | JWT (G3/G4) | PDF export (redacted) |
| POST | `/api/v1/group/{group_id}/acad/special-ed/iep/bulk-remind/` | JWT (G3 Spec Ed) | Send review reminders |
| GET | `/api/v1/group/{group_id}/acad/special-ed/iep/charts/compliance-heatmap/` | JWT (G3+) | Heatmap data |
| GET | `/api/v1/group/{group_id}/acad/special-ed/iep/charts/goals-distribution/` | JWT (G3+) | Donut chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../iep/?q=` | `#iep-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../iep/?filters=` | `#iep-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../iep/?sort=&dir=` | `#iep-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../iep/?page=` | `#iep-table-section` | `innerHTML` |
| Create drawer open | `click` | GET `.../iep/create-form/` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../iep/` | `#drawer-body` | `innerHTML` |
| Review drawer open | `click` | GET `.../iep/{id}/review-form/` | `#drawer-body` | `innerHTML` |
| Review submit | `submit` | POST `.../iep/{id}/review/` | `#drawer-body` | `innerHTML` |
| View drawer | `click` | GET `.../iep/{id}/` | `#drawer-body` | `innerHTML` |
| Nav badge refresh | `load` | GET `.../iep/overdue-count/` | `#iep-nav-badge` | `innerHTML` |
| CAO sign-off confirm | `click` | POST `.../iep/{id}/signoff/` | `#iep-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
