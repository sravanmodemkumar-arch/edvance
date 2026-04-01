# 45 — Scholarship Exam Manager

> **URL:** `/group/acad/olympiad/scholarship-exams/`
> **File:** `45-scholarship-exam-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Olympiad & Scholarship Coord G3 · CAO G4 · Exam Controller G3 · Results Coordinator G3 · Finance/Div-C (view disbursement)

---

## 1. Purpose

The Scholarship Exam Manager handles the group's own internally-run scholarship entrance examinations — distinct from external olympiads. These are merit, need-based, or sports scholarships the institution itself awards to eligible students. Examples include annual merit scholarships for students entering Class 11, foundation-to-senior promotion scholarships for IIT Foundation completers, and government-sponsored fee-waiver exams the group administers for its own students.

Managing a scholarship exam is operationally complex: it begins with announcing the exam and opening a registration window, then moves through paper creation, conduct, result publication, and finally award disbursement — a pipeline that spans three to four months and involves multiple divisions. This page tracks each scholarship exam as a card on a Kanban pipeline so that the Olympiad Coordinator and CAO can see, at a glance, which exams are at which stage and what action is required.

The integration with Division-C (Group Scholarship Manager) ensures that once awards are decided here, disbursement — whether as fee waiver, cash transfer, or in-kind support — is tracked by the Finance division without requiring manual communication. Award revocation, which must happen when a student leaves the institution mid-year or violates conditions, is a controlled action requiring confirmation and a mandatory reason, so that it is always auditable.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Approve scholarship exams | Final approver for exam publish and awards |
| Group Academic Director | G3 | ❌ | ❌ | No access |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ Paper tab only | ✅ Assign exam paper | Access scoped to paper assignment |
| Group Results Coordinator | G3 | ✅ Results tab | ✅ Publish results | Publishes results once marks uploaded |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ✅ Full | ✅ Full CRUD | Primary owner of this page |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ❌ | ❌ | No access |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |
| Finance / Div-C Staff | Cross-div | ✅ Disbursement data | ❌ No CUD | View-only access to award amounts and recipients |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Olympiad & Scholarships  ›  Scholarship Exam Manager
```

### 3.2 Page Header
```
Scholarship Exam Manager                                    [+ New Scholarship Exam]
Internal scholarship exams — pipeline and award management          (Olympiad Coord only)
```
Toggle view: **[Kanban]** (default) | **[Table]**

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Active Exams | Count in pipeline (not yet at "Awards Given") |
| Announced | Count at first Kanban stage |
| Registration Open | Count currently accepting registrations |
| Results Published | Count awaiting awards |
| Awards Given | Total awards disbursed this year |
| Total Award Value | ₹ X (sum of all awards given this academic year) |

---

## 4. Main Content

### 4.1 Kanban View (Default)

Five columns — each scholarship exam appears as a card:

| Stage | Meaning | Card colour |
|---|---|---|
| **Announced** | Exam declared; registration not yet open | Blue |
| **Registration Open** | Students actively registering | Amber |
| **Exam Scheduled** | Registration closed; exam date confirmed | Purple |
| **Results Published** | Marks uploaded and results published | Teal |
| **Awards Given** | Disbursement initiated in Div-C | Green |

**Each Kanban card contains:**
- Scholarship Exam Name
- Type badge: Merit / Need-based / Sports / Government-sponsored
- Registration deadline (if in Registration Open stage)
- Exam date (if in Exam Scheduled / Results Published stage)
- Eligible student count
- Registered student count (if applicable)
- Action button contextual to stage (e.g. "Open Registration" / "Schedule Exam" / "Publish Results" / "Initiate Awards")
- Three-dot menu: View Detail · Edit · Move Stage

**Drag and drop:** Olympiad Coord can drag cards between stages; a confirm modal appears before stage change if moving backward.

### 4.2 Table View (alternate)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Bulk select |
| Scholarship Exam | Text | ✅ | |
| Type | Badge | ✅ | Merit / Need / Sports |
| Exam Date | Date | ✅ | |
| Eligible | Number | ✅ | |
| Registered | Number | ✅ | |
| Appeared | Number | ✅ | |
| Results Published | Badge | ✅ | Yes / No |
| Awards Given | Number | ✅ | Count of awardees |
| Award Value (Total) | ₹ | ✅ | |
| Stage | Badge | ✅ | Kanban stage |
| Actions | — | ❌ | |

### 4.3 Search
- Full-text across: Scholarship Exam name, Type
- 300ms debounce

### 4.4 Advanced Filters (slide-in drawer)

| Filter | Type | Options |
|---|---|---|
| Stage | Multi-select | Kanban stages |
| Type | Multi-select | Merit / Need-based / Sports / Government |
| Academic Year | Select | Current + last 3 years |
| Exam Date range | Date range picker | |

### 4.5 Row Actions (Table view) / Card Menu (Kanban)

| Action | Visible To | Notes |
|---|---|---|
| View Detail | All roles | `scholarship-exam-view` drawer 640px |
| Edit | Olympiad Coord | `scholarship-exam-create` drawer 640px (pre-filled) |
| Move Stage | Olympiad Coord | Confirm modal |
| View Award List | Olympiad Coord, CAO, Div-C | `award-list` drawer 480px |
| Revoke Award | Olympiad Coord | `award-revoke-confirm` modal |

### 4.6 Bulk Actions (Table view)

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | Olympiad Coord, CAO | Selected exam summary |

---

## 5. Drawers & Modals

### 5.1 Drawer: `scholarship-exam-create` — New / Edit Scholarship Exam
- **Trigger:** [+ New Scholarship Exam] header button or Edit action
- **Width:** 640px
- **Tabs:** Identity · Eligibility Criteria · Registration Window · Exam Paper · Award Structure

#### Tab: Identity
| Field | Type | Required | Validation |
|---|---|---|---|
| Scholarship Exam Name | Text | ✅ | Min 5, max 150 chars |
| Type | Select | ✅ | Merit / Need-based / Sports / Government-sponsored |
| Academic Year | Select | ✅ | |
| Description | Textarea | ✅ | Max 500 chars |
| Announcement Date | Date | ✅ | Cannot be in the past |
| Branches in Scope | Multi-select | ✅ | All / Zone / Specific branches |
| Classes Eligible | Multi-select | ✅ | Class 6–12 |

#### Tab: Eligibility Criteria
| Field | Type | Required | Notes |
|---|---|---|---|
| Minimum % in last exam | Number (%) | ❌ | e.g. 60% for merit |
| Maximum annual family income | ₹ Number | Conditional | Required for need-based |
| Stream restrictions | Multi-select | ❌ | MPC / BiPC / All |
| Attendance minimum | Number (%) | ❌ | |
| Additional criteria | Textarea | ❌ | Free text, max 500 chars |

#### Tab: Registration Window
| Field | Type | Required | Notes |
|---|---|---|---|
| Registration Opens | Date | ✅ | Must be after Announcement Date |
| Registration Closes | Date | ✅ | Must be after Opens |
| Registration Fee | ₹ Number | ✅ | Enter 0 if free |
| Application form required | Toggle | ✅ | If on, branches upload completed forms |

#### Tab: Exam Paper
| Field | Type | Required | Notes |
|---|---|---|---|
| Exam Date | Date | ✅ | Must be after registration close |
| Exam Duration | Number (minutes) | ✅ | |
| Paper | Search + select | Conditional | Links to Exam Paper Builder (page 24) — Exam Controller assigns |
| Venue | Select | ✅ | All branches simultaneously / Central venue |

#### Tab: Award Structure
| Field | Type | Required | Notes |
|---|---|---|---|
| Total awards | Number | ✅ | |
| Award type | Select | ✅ | Fee waiver / Cash / Merit certificate / In-kind |
| Award tiers | Repeater | ✅ | Rank range · Award value (₹ or % fee waiver) · Conditions |
| Award duration | Select | ✅ | One-time / Per term / Per year / Full course |
| Revocation conditions | Textarea | ❌ | Conditions under which award can be revoked |

- **Submit:** "Save Scholarship Exam" — disabled until all required tabs valid (tab dot indicators).
- **On success:** Card appears in Kanban at "Announced" stage.

### 5.2 Drawer: `scholarship-exam-view`
- **Width:** 640px
- **Tabs:** Overview · Registrations · Results · Awards · Audit Trail

**Tab: Overview** — All identity, eligibility, registration window, and exam details read-only.

**Tab: Registrations** — Table: Branch · Eligible · Registered · Applications submitted · Fee collected (₹). [Download Registration Report] button.

**Tab: Results** — Marks upload status per branch · Published results table: Rank · Student Name · Branch · Score · Award Tier.

**Tab: Awards** — Award list (see 5.3 below). Integration link: "View disbursement in Div-C →".

**Tab: Audit Trail** — Every stage change, edit, and award action logged with actor and timestamp.

### 5.3 Drawer: `award-list`
- **Trigger:** "View Award List" action
- **Width:** 480px

| Column | Type | Notes |
|---|---|---|
| Rank | Number | |
| Student Name | Text | |
| Branch | Text | |
| Class | Badge | |
| Score | Number | |
| Award Tier | Text | e.g. "Rank 1–3: 100% Fee Waiver" |
| Award Value | ₹ | |
| Disbursement Status | Badge | Pending / Initiated / Disbursed |
| Actions | — | Revoke |

- **Footer:** [Export Award List XLSX] · [Send to Div-C for Disbursement] (Olympiad Coord only)

### 5.4 Modal: `award-revoke-confirm`
- **Trigger:** Revoke action on award-list row
- **Width:** 420px
- **Content:** "You are revoking the scholarship award for [Student Name]. This action is audited and cannot be undone without re-issuing the award."
- **Fields:**
  - Reason (required, Select): Student left institution / Academic condition not met / Conduct issue / Administrative error / Other
  - Details (Textarea, required, min 20 chars)
  - Notify student's branch? (checkbox, default on)
- **Buttons:** [Confirm Revocation] (danger red) · [Cancel]
- **On confirm:** Award status updated to "Revoked" · Audit entry created · Div-C notified to halt disbursement · Branch notified

### 5.5 Modal: `stage-change-confirm`
- **Width:** 420px
- **Trigger:** Moving card backward in Kanban
- **Content:** "Moving [Exam Name] back from [Current Stage] to [Target Stage]. This may affect notifications already sent."
- **Fields:** Reason (required, min 10 chars)
- **Buttons:** [Confirm Stage Change] · [Cancel]

---

## 6. Charts

### 6.1 Scholarship Pipeline (Funnel)
- **Type:** Funnel chart (horizontal)
- **Data:** Count of exams at each Kanban stage
- **Stages:** Announced → Registration Open → Exam Scheduled → Results Published → Awards Given
- **Tooltip:** Stage name · Count of exams
- **Export:** PNG

### 6.2 Awards by Type (Donut)
- **Type:** Donut chart
- **Data:** Award count split by type: Fee waiver / Cash / Merit certificate / In-kind
- **Centre text:** Total awards given this year
- **Tooltip:** Type · Count · Total value ₹
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exam created | "Scholarship exam '[Name]' created and announced" | Success | 4s |
| Exam updated | "Scholarship exam '[Name]' updated" | Success | 4s |
| Stage advanced | "[Exam Name] moved to [New Stage]" | Success | 4s |
| Stage reverted | "[Exam Name] moved back to [Stage] — reason logged" | Warning | 6s |
| Award revoked | "Award revoked for [Student Name]. Branch notified." | Warning | 6s |
| Awards sent to Div-C | "Award list sent to Finance (Div-C) for disbursement" | Success | 4s |
| Export started | "Export preparing… download will start shortly" | Info | 4s |
| Paper assigned | "Exam paper assigned to [Exam Name]" | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No scholarship exams yet | "No scholarship exams created" | "Create your first internal scholarship exam to begin tracking" | [+ New Scholarship Exam] |
| Kanban stage empty | "No exams at this stage" | Stage label shown; no cards visible | — |
| No awards yet | "No awards recorded for this exam" | "Awards will appear here after results are published and awardees confirmed" | — |
| No search results | "No exams match your search" | "Clear the search or adjust filters" | [Clear] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + Kanban columns (2 skeleton cards per column) |
| Table view load | Skeleton table rows (10) |
| Drawer open | Spinner → tab content renders |
| Stage change submit | Spinner in confirm button |
| Award revoke submit | Spinner in confirm button + row updates |
| Export trigger | Spinner in export button |

---

## 10. Role-Based UI Visibility

| Element | Olympiad Coord G3 | CAO G4 | Exam Controller G3 | Results Coord G3 | Div-C Finance |
|---|---|---|---|---|---|
| [+ New Scholarship Exam] | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit exam | ✅ | ❌ | ❌ | ❌ | ❌ |
| Move Kanban stage | ✅ | ✅ (approve only) | ❌ | ❌ | ❌ |
| Assign exam paper | ❌ (view only) | ❌ | ✅ | ❌ | ❌ |
| Publish results | ❌ (view only) | ✅ | ❌ | ✅ | ❌ |
| View award list | ✅ | ✅ | ❌ | ❌ | ✅ |
| Revoke award | ✅ | ✅ | ❌ | ❌ | ❌ |
| Send to Div-C | ✅ | ✅ | ❌ | ❌ | ❌ |
| Export | ✅ | ✅ | ❌ | ❌ | ✅ (award data) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/` | JWT | List exams (table/kanban) |
| GET | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/stats/` | JWT | Stats bar data |
| POST | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/` | JWT (G3) | Create scholarship exam |
| PUT | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/{id}/` | JWT (G3) | Update exam details |
| PATCH | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/{id}/stage/` | JWT (G3/G4) | Change Kanban stage |
| GET | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/{id}/awards/` | JWT | Award list |
| POST | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/{id}/awards/{aid}/revoke/` | JWT (G3/G4) | Revoke award |
| POST | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/{id}/send-to-divc/` | JWT (G3/G4) | Trigger Div-C disbursement |
| GET | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/{id}/audit/` | JWT | Audit trail |
| GET | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/export/?format=xlsx` | JWT | Export |
| GET | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/charts/pipeline/` | JWT | Funnel chart |
| GET | `/api/v1/group/{group_id}/acad/olympiad/scholarship-exams/charts/award-types/` | JWT | Donut chart |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search (table view) | `input delay:300ms` | GET `.../scholarship-exams/?q=` | `#exam-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../scholarship-exams/?filters=` | `#exam-table-section` | `innerHTML` |
| Kanban load | `load` | GET `.../scholarship-exams/?view=kanban` | `#kanban-board` | `innerHTML` |
| Stage change (drag confirm) | `click` | PATCH `.../scholarship-exams/{id}/stage/` | `#kanban-board` | `innerHTML` |
| View detail drawer | `click` | GET `.../scholarship-exams/{id}/` | `#drawer-body` | `innerHTML` |
| Award list drawer | `click` | GET `.../scholarship-exams/{id}/awards/` | `#drawer-body` | `innerHTML` |
| Create/edit form open | `click` | GET `.../scholarship-exams/create-form/` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../scholarship-exams/` | `#drawer-body` | `innerHTML` |
| Revoke confirm | `click` | POST `.../scholarship-exams/{id}/awards/{aid}/revoke/` | `#award-row-{aid}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
