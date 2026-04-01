# 12 — Special Education Coordinator Dashboard

> **URL:** `/group/acad/special-ed/`
> **File:** `12-special-ed-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Special Education Coordinator (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Special Education Coordinator. This role manages the welfare, academic accommodations, and Individual Education Plans (IEPs) of students with special needs — including learning disabilities (dyslexia, dyscalculia, ADHD), physical disabilities, and hearing/vision impairments — across all branches in the group.

The coordinator's core responsibilities are: ensuring that every student with a special need has an active, current IEP; that exam accommodation requests are processed in time before each exam; that branch-level caseloads are monitored for overload; and that POCSO/welfare incidents involving special needs students are tracked and escalated appropriately. The dashboard is built around these four flows.

**Data Privacy Notice — DPDP Act 2023 Compliance:** This dashboard handles sensitive personal data of minor students covered under the Digital Personal Data Protection Act 2023 (DPDP Act). Student names, disability type details, and IEP content are classified as sensitive personal data. Access controls are strictly enforced:
- G3 (this role) and G4 (CAO): Full data — names visible, disability details visible, IEP content accessible.
- G1/G2 (MIS Officer, Curriculum Coordinator): Student names are masked (replaced with Student Code). Disability category is shown (e.g., "Learning Disability") but specific condition is hidden. IEP content is not accessible.
- All other roles: No access to this page.

Data masking is applied server-side in Django. No unmasked data is ever sent to G1/G2 clients.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Special Education Coordinator | G3 | Full — all sections, all actions, all student data visible | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | Full read + override actions, full student data visible | Full oversight |
| Group Academic Director | G3 | Read — IEP compliance and branch caseload sections only | Academic oversight — student names visible (G3 level) |
| Group Exam Controller | G3 | Read — exam accommodation queue only | Exam scheduling coordination — student names visible (G3 level) |
| Group Academic MIS Officer | G1 | Read-only — IEP compliance and caseload sections only | **Names masked — DPDP Act compliance** |
| Group Curriculum Coordinator | G2 | — | No access |
| All Stream Coordinators | G3 | — | No access |
| Group Olympiad & Scholarship Coord | G3 | Read — scholarship section (special needs scholarship pathways) only | Coordination — student names visible (G3 level) |
| Group JEE/NEET Integration Head | G3 | — | No access |
| Group IIT Foundation Director | G3 | — | No access |
| Group Academic Calendar Manager | G3 | — | No access |

> **Access enforcement:** Django view decorator `@require_role('special_ed_coord')` with DPDP masking middleware applied at G1/G2 data serialization level. All role-permission checks and data masking are server-side only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Special Education  ›  Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                          [New IEP +]  [Settings ⚙]
Group Special Education Coordinator  ·  Last login: [date time]  ·  [Group Logo]
```

**DPDP notice strip (below header, always visible for G3+):**
> `🔒 This dashboard contains sensitive personal data of students with special needs. All data is governed by the DPDP Act 2023. Do not share screenshots or exports outside authorised personnel.`
> Background: `bg-blue-50 border-l-4 border-blue-400` · Non-dismissible.

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel above KPI row (below DPDP notice strip)
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all →" link

**Alert trigger examples:**
- IEP review overdue by > 30 days for any student
- Exam accommodation not set up for a student with approved accommodation with exam < 72 hrs away
- POCSO/welfare incident involving a special needs student flagged from branch level and unresolved > 24 hrs
- Branch caseload > 50 special needs students with no dedicated support teacher
- New special needs student enrolled without an IEP created within 14 days of enrollment

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Active IEPs | Total · Due for review this month · Overdue reviews | IEP module | Green = no overdue · Yellow 1–5 overdue · Red > 5 overdue | → Section 5.1 Active IEPs |
| Accommodation Requests | Pending / Approved / Implemented across all branches | Accommodation module | Green = all implemented · Yellow pending > 0 · Red pending > 5 or exam < 48 hrs | → Section 5.3 Accommodation Requests |
| Branch Caseload | Total special needs students across all branches · Branches with caseload > 50 highlighted | Enrollment module | Green = all branches < 50 · Yellow = 1–2 branches > 50 · Red ≥ 3 branches > 50 | → Section 5.5 Branch Caseload |
| IEP Review Compliance | `XX%` branches have reviewed all IEPs due this month | IEP module | Green ≥ 95% · Yellow 80–95% · Red < 80% | → Section 5.4 IEP Review Heatmap |
| Welfare Incidents | Open POCSO/welfare incidents involving special needs students | Incident module | Green = 0 · Yellow = 1 · Red ≥ 2 (pulsing badge) | → Section 5.6 Welfare Incidents |
| Upcoming Exam Accommodations | Students with approved accommodations with exams in next 14 days · Setup confirmed Y/N | Exam calendar + accommodation module | Green = all setup confirmed · Yellow 1–3 not confirmed · Red > 3 | → Section 5.3 Accommodation Queue |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/special-ed/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Active IEPs

> Overview of all active Individual Education Plans across the group.

**Display:** Stat card + filterable table.

**Stat card (above table):** Total Active IEPs: [N] · Due for review this month: [N] · Overdue: [N] (red if > 0) · New this month: [N]

**Table columns:**

| Column | Sortable | Notes |
|---|---|---|
| Student Code | ✅ | Actual name shown G3+ · Masked for G1 |
| Branch | ✅ | |
| Class | ✅ | |
| Stream | ✅ | |
| Disability Category | ✅ | Learning Disability · Physical Disability · Hearing Impairment · Vision Impairment · Multiple |
| Specific Condition | ✅ | Dyslexia / Dyscalculia / ADHD / etc. — **masked for G1 — shown as "See IEP"** |
| IEP Created | ✅ | Date |
| Last Reviewed | ✅ | Date |
| Next Review Due | ✅ | Date — red if past due |
| Status | ✅ | Active · Under Review · Pending Approval · Closed |
| Actions | ❌ | [View IEP →] [Edit IEP] [Log Review] — **all hidden for G1** |

**Filters:** Branch · Disability category · Review status (overdue / due this month / up to date) · Class · Stream

**[+ New IEP] button** (top-right of section): Opens IEP creation wizard.

**Drawer: `iep-view-edit`**
- Width: 720px
- Tabs: Student Details · Disability Profile · Academic Goals · Accommodations · Review History · Contacts
- Student Details: Code, branch, class, stream, enrollment date, support teacher assigned
- Disability Profile: Category, specific condition, diagnosis date, external assessment reference
- Academic Goals: Subject-by-subject goals for this IEP period, progress notes
- Accommodations: Exam accommodations approved, classroom accommodations, technology aids
- Review History: All past review log entries with date, reviewer, outcome
- Contacts: Parent/guardian contact, external therapist/psychologist if applicable
- **DPDP note:** Full IEP content access G3+ only. G1 sees this drawer with all sensitive fields replaced by "[Restricted — DPDP Act 2023]"

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/special-ed/ieps/"` · filter changes trigger `hx-get` · `hx-target="#iep-section"`.

---

### 5.2 Student Type Breakdown

> Distribution of special needs students by disability category across the group.

**Display:** Donut chart (Chart.js 4.x) + supporting table.

**Donut chart segments:**
- Learning Disability (dyslexia, dyscalculia, ADHD, etc.) — Blue
- Physical Disability (mobility, orthopaedic) — Orange
- Hearing Impairment — Purple
- Vision Impairment — Green
- Multiple Disabilities — Red
- Unclassified / Under Assessment — Grey

**Centre label:** Total students: [N]

**Tooltip:** Category name · Count · % of total

**Supporting table (below chart):**

| Column | Description |
|---|---|
| Category | Disability category |
| Count | Number of students |
| % of Total | Percentage |
| Branches Affected | How many branches have students in this category |
| Avg per Branch | Average caseload for this category |

**Filter:** Branch filter (view breakdown for one branch vs group-wide)

**DPDP note:** Chart and table show aggregate counts only — no individual identifiers. Safe for G1 access.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/special-ed/breakdown/"` · branch filter change triggers `hx-get` · `hx-target="#breakdown-section"`.

---

### 5.3 Exam Accommodation Queue

> Students with approved exam accommodations — tracks setup status before upcoming exams.

**Display:** Alert list + table.

**Alert strip (above table):** "X students have approved accommodations with exams in the next 14 days. Y of X confirmations pending." — red strip if Y > 0.

**Table columns:**

| Column | Sortable | Notes |
|---|---|---|
| Student Code | ✅ | Name visible G3+ · Masked for G1 |
| Branch | ✅ | |
| Exam Name | ✅ | |
| Exam Date | ✅ | Red text if < 48 hrs |
| Accommodation Type | ✅ | Extra time · Scribe · Separate room · Large print · Oral examination |
| Approved By | ✅ | |
| Setup Confirmed | ✅ | Yes (green) / No (red) |
| Actions | ❌ | [Confirm Setup →] [Edit Accommodation] [Send Reminder to Branch] — **hidden for G1** |

**[Confirm Setup →]:** POST to mark setup as confirmed + log timestamp + notifier.

**[Send Reminder to Branch]:** POST to send WhatsApp/email reminder to branch coordinator.

**Filters:** Exam date range · Branch · Accommodation type · Setup status (confirmed / not confirmed)

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/special-ed/accommodations/"` · filter changes trigger `hx-get` · `hx-target="#accommodation-section"`.

---

### 5.4 IEP Review Compliance Heatmap

> Branch-level compliance: have all IEPs due for review this month been reviewed?

**Display:** Heatmap grid

**Rows:** Branches (alphabetically sorted)

**Columns:** Month (last 6 months, current month highlighted)

**Cell colours:**
- Dark green: 100% of IEPs reviewed on time this month
- Light green: 80–99% reviewed
- Amber: 60–80% reviewed
- Red: < 60% reviewed
- Grey: No special needs students in this branch this month

**Interaction:** Click any cell → opens branch IEP compliance drawer for that month.

**Drawer: `branch-iep-compliance`**
- Width: 560px
- Content: List of IEPs due for review in selected month for selected branch — Student Code · Due Date · Review Status (Done/Overdue) · Reviewer name (G3+) · [Log Review] (G3 only)
- **DPDP: Student names masked for G1**

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/special-ed/iep-compliance-heatmap/"` · `hx-trigger="load"` · `hx-target="#compliance-heatmap-section"` · cell click triggers drawer load.

---

### 5.5 Branch Caseload

> Count of special needs students per branch — helps identify branches with disproportionately high caseloads.

**Display:** Bar chart (Chart.js 4.x) + table toggle.

**Bar chart:**
- X-axis: Branches (sorted by caseload descending)
- Y-axis: Number of special needs students
- Colour: Green < 30 · Amber 30–50 · Red > 50
- Reference line: Group average caseload (dashed grey)

**Tooltip:** Branch name · Total special needs students · Dedicated support teachers count · Ratio (students per support teacher) · Flag if ratio > 20:1

**Table toggle view (same data):**

| Column | Sortable |
|---|---|
| Branch | ✅ |
| Total Special Needs Students | ✅ |
| Learning Disability | ✅ |
| Physical Disability | ✅ |
| Hearing Impairment | ✅ |
| Vision Impairment | ✅ |
| Support Teachers | ✅ |
| Student : Teacher Ratio | ✅ |

**Filter:** Branch · Disability category · Ratio threshold alert (> 20:1)

**DPDP note:** Aggregate counts only — no individual identifiers. Safe for all permitted roles.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/special-ed/caseload/"` · `hx-trigger="load"` · `hx-target="#caseload-section"` · chart/table toggle: `hx-get` with `?view=chart` or `?view=table`.

---

### 5.6 POCSO / Welfare Incident Coordination

> Special needs students involved in POCSO or welfare incidents flagged from branch level.

**Display:** Alert strip (if open incidents > 0) + incident table.

**Alert strip:** Red background if any incident Severity 1 · "X open welfare incidents involving students with special needs. Immediate attention required." — [View All →]

**Table columns:**

| Column | Sortable | Notes |
|---|---|---|
| Incident # | ✅ | System ref |
| Student Code | ✅ | Name visible G3+ · **Masked for G1** |
| Branch | ✅ | |
| Incident Type | ✅ | POCSO · Bullying · Physical welfare · Mental health crisis |
| Severity | ✅ | S1 (Critical) · S2 (High) · S3 (Moderate) |
| Reported | ✅ | Date |
| Days Open | ✅ | Red if S1 > 4 hrs · S2 > 24 hrs · S3 > 72 hrs |
| Status | ✅ | Open · Under investigation · Resolved · Escalated |
| Actions | ❌ | [View →] [Escalate] [Log Update] — **hidden for G1** |

**Filters:** Severity · Status · Branch · Incident type

**[Escalate] action:** Opens escalation modal — escalates to Group VP Welfare / CAO / external authority with mandatory documented reason.

**[View →]:** Opens full incident detail drawer (G3+ only, not accessible to G1).

**Empty state:** "No open welfare incidents involving special needs students." — green checkmark.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/special-ed/incidents/"` · `hx-trigger="load"` · `hx-target="#incidents-section"`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `iep-view-edit`
- **Trigger:** [View IEP →] or [Edit IEP] in Section 5.1
- **Width:** 720px
- **Tabs:** Student Details · Disability Profile · Academic Goals · Accommodations · Review History · Contacts
- **DPDP:** Full content G3+ only; G1 sees restricted placeholders
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/special-ed/ieps/{iep_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `branch-iep-compliance`
- **Trigger:** Heatmap cell click in Section 5.4
- **Width:** 560px
- **Content:** IEPs due for selected branch/month; [Log Review] action (G3 only)
- **DPDP:** Student names masked for G1
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/special-ed/iep-compliance/{branch_id}/{month}/"` `hx-target="#drawer-body"`

### 6.3 Modal: `log-iep-review`
- **Trigger:** [Log Review] in IEP table or compliance drawer
- **Width:** 480px
- **Content:** Student code (read-only) · Review date · Reviewer role · Review outcome (Goals met / Partially met / Review needed · Goals revised) · Notes (required, min 50 chars) · [Submit Review] [Cancel]
- **On submit:** `hx-post="/api/v1/group/{group_id}/acad/special-ed/ieps/{iep_id}/review/"` → toast + table row updates

### 6.4 Modal: `escalate-incident`
- **Trigger:** [Escalate] in Section 5.6 incident table
- **Width:** 500px
- **Content:** Incident summary (read-only) · Escalation target (Group VP / CAO / Police / Child Welfare Committee) · Escalation reason (required, min 50 chars) · [Confirm Escalation] [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/special-ed/incidents/{incident_id}/escalate/"` → notifies targets → audit log entry → toast

### 6.5 Wizard: `iep-create` (opened from [New IEP +] header button or table)
- **Width:** 720px (full-height side panel)
- **Steps:** 1 Student Lookup → 2 Disability Profile → 3 Academic Goals → 4 Accommodations → 5 Support Plan → 6 Review & Publish
- **Step 1:** Search student by code/name (branch portal integration) · select class, stream, branch
- **Step 2:** Disability category · specific condition · diagnosis date · external assessment document upload
- **Step 3:** Subject-by-subject goals (predefined templates available per disability category)
- **Step 4:** Exam accommodations + classroom accommodations (multi-select with notes)
- **Step 5:** Assigned support teacher · Review frequency · Parent notification sent Y/N
- **Step 6:** Preview full IEP · [Save as Draft] [Publish IEP]
- **HTMX:** Multi-step: each step POST to save partial data, final [Publish] → `hx-post="/api/v1/group/{group_id}/acad/special-ed/ieps/"` → toast + IEP table refreshes

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| IEP published | "IEP created for Student [Code] — [Branch Name] notified" | Success (green) | 5s auto-dismiss |
| IEP review logged | "IEP review logged for Student [Code]" | Success | 4s |
| Accommodation setup confirmed | "Exam accommodation confirmed for Student [Code] — [Exam Name]" | Success | 4s |
| Reminder sent to branch | "Accommodation setup reminder sent to [Branch Name]" | Info (blue) | 4s |
| Incident escalated | "Incident #[N] escalated to [Target role] — audit log updated" | Warning (yellow) | 6s manual dismiss |
| Incident update logged | "Update logged for Incident #[N]" | Success | 4s |
| KPI load error | "Failed to load KPI data. Retrying…" | Error (red) | Manual dismiss |
| Accommodation edit saved | "Accommodation updated for Student [Code]" | Success | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No IEPs exist | Document outline | "No IEPs recorded yet" | "Create the first IEP for a student with special needs in your group" | [New IEP +] |
| No accommodations pending | Checkmark circle | "All accommodations confirmed" | "Every student with an approved accommodation has a confirmed setup for upcoming exams" | — |
| No overdue IEP reviews | Checkmark circle | "All IEP reviews up to date" | "No IEP reviews are overdue across any branch" | — |
| No welfare incidents | Checkmark circle | "No open welfare incidents" | "No POCSO or welfare incidents involving special needs students are open" | — |
| No students in branch (caseload) | Building outline | "No special needs students in this branch" | "This branch has no students with an active IEP" | — |
| Heatmap — all grey | Grid outline | "No IEPs due for review" | "No IEPs have review dates in the selected period" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + IEP table (5 skeleton rows) + breakdown chart placeholder |
| IEP table filter/sort | Inline skeleton rows — 5 rows, same column widths |
| Breakdown chart load | Spinner centred in chart/donut area |
| Accommodation table load | Skeleton table rows — 5 rows |
| Compliance heatmap load | Grey placeholder grid (branches × months) |
| Caseload chart load | Spinner centred in chart area |
| Incidents table load | Skeleton rows — 3 rows |
| IEP create wizard step transition | Step indicator progress animation + content fade |
| Drawer open | Skeleton rows inside drawer body (720px drawer skeletons for IEP tabs) |
| KPI auto-refresh | Subtle shimmer over existing card values |
| Escalate / log review button click | Spinner inside button + button disabled |

---

## 10. Role-Based UI Visibility

| Element | Special Ed Coord (G3) | CAO (G4) | Exam Controller (G3) | MIS Officer (G1) | All others |
|---|---|---|---|---|---|
| Page itself | ✅ Rendered (full) | ✅ Rendered (full) | ✅ Accommodation section only | ✅ Read-only (masked) | ❌ Redirected |
| DPDP notice strip | ✅ Shown | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| Student names in all tables | ✅ Visible (actual name) | ✅ Visible | ✅ Visible | ❌ Code only (masked) | N/A |
| Disability specific condition | ✅ Visible | ✅ Visible | ❌ Hidden | ❌ Hidden (masked) | N/A |
| IEP full content drawer | ✅ Full access | ✅ Full access | ❌ No access | ❌ Restricted placeholders | N/A |
| [New IEP +] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Edit IEP] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Log Review] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Confirm Setup →] accommodation | ✅ Shown | ✅ Shown | ✅ Shown | ❌ Hidden | N/A |
| [Escalate] incident | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| Welfare incidents section | ✅ Full access | ✅ Full access | ❌ Hidden | ✅ Counts only (masked) | N/A |

> All UI visibility decisions and data masking made server-side in Django template and DRF serializers. No client-side JS role checks. DPDP masking applied at serializer level — G1 serializer never receives unmasked name or condition fields.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/special-ed/dashboard/` | JWT (G3+) | Full page data — DPDP masking applied per role |
| GET | `/api/v1/group/{group_id}/acad/special-ed/kpi-cards/` | JWT (G3+) | KPI card values only (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/special-ed/ieps/` | JWT (G3+) | IEP list — names masked for G1 |
| GET | `/api/v1/group/{group_id}/acad/special-ed/ieps/{iep_id}/` | JWT (G3) | Full IEP detail — G3+ only endpoint |
| POST | `/api/v1/group/{group_id}/acad/special-ed/ieps/` | JWT (G3) | Create new IEP |
| PATCH | `/api/v1/group/{group_id}/acad/special-ed/ieps/{iep_id}/` | JWT (G3) | Edit IEP |
| POST | `/api/v1/group/{group_id}/acad/special-ed/ieps/{iep_id}/review/` | JWT (G3) | Log IEP review |
| GET | `/api/v1/group/{group_id}/acad/special-ed/breakdown/` | JWT (G3+) | Student type breakdown — aggregate counts only |
| GET | `/api/v1/group/{group_id}/acad/special-ed/accommodations/` | JWT (G3+) | Exam accommodation queue — names masked for G1 |
| POST | `/api/v1/group/{group_id}/acad/special-ed/accommodations/{accommodation_id}/confirm/` | JWT (G3) | Confirm exam setup |
| POST | `/api/v1/group/{group_id}/acad/special-ed/accommodations/{accommodation_id}/remind/` | JWT (G3) | Send reminder to branch |
| GET | `/api/v1/group/{group_id}/acad/special-ed/iep-compliance-heatmap/` | JWT (G3+) | Heatmap data — aggregate per branch/month |
| GET | `/api/v1/group/{group_id}/acad/special-ed/iep-compliance/{branch_id}/{month}/` | JWT (G3+) | Branch-month IEP compliance drawer data — masked for G1 |
| GET | `/api/v1/group/{group_id}/acad/special-ed/caseload/` | JWT (G3+) | Branch caseload data — aggregate counts |
| GET | `/api/v1/group/{group_id}/acad/special-ed/incidents/` | JWT (G3) | Welfare incidents — G3+ only, names masked for G1 MIS |
| POST | `/api/v1/group/{group_id}/acad/special-ed/incidents/{incident_id}/escalate/` | JWT (G3) | Escalate incident |
| POST | `/api/v1/group/{group_id}/acad/special-ed/incidents/{incident_id}/update/` | JWT (G3) | Log incident update |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `/api/.../special-ed/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| IEP table filter/sort | `change` / `click` | GET `/api/.../ieps/?branch={}&category={}&status={}` | `#iep-section` | `innerHTML` |
| Open IEP drawer | `click` | GET `/api/.../ieps/{iep_id}/` | `#drawer-body` | `innerHTML` |
| Log IEP review submit | `click` | POST `/api/.../ieps/{id}/review/` | `#iep-section` | `innerHTML` |
| Breakdown branch filter | `change` | GET `/api/.../breakdown/?branch={}` | `#breakdown-section` | `innerHTML` |
| Accommodation filter | `change` | GET `/api/.../accommodations/?branch={}&type={}&status={}` | `#accommodation-section` | `innerHTML` |
| Confirm accommodation setup | `click` | POST `/api/.../accommodations/{id}/confirm/` | `#accommodation-section` | `innerHTML` |
| Send reminder to branch | `click` | POST `/api/.../accommodations/{id}/remind/` | `#toast-container` | `afterbegin` |
| Compliance heatmap load | `load` | GET `/api/.../iep-compliance-heatmap/` | `#compliance-heatmap-section` | `innerHTML` |
| Heatmap cell click | `click` | GET `/api/.../iep-compliance/{branch_id}/{month}/` | `#drawer-body` | `innerHTML` |
| Caseload view toggle (chart/table) | `click` | GET `/api/.../caseload/?view={chart|table}` | `#caseload-section` | `innerHTML` |
| Incidents filter | `change` | GET `/api/.../incidents/?severity={}&status={}&branch={}` | `#incidents-section` | `innerHTML` |
| Escalate incident confirm | `click` | POST `/api/.../incidents/{id}/escalate/` | `#incidents-section` | `innerHTML` |
| IEP wizard step submit | `click` | POST `/api/.../ieps/{draft_id}/step/{n}/` | `#wizard-body` | `innerHTML` |
| IEP wizard final publish | `click` | POST `/api/.../ieps/` | `#iep-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
