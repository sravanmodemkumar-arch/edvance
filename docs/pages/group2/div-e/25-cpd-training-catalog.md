# 25 — CPD Training Catalog

- **URL:** `/group/hr/training/catalog/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Training & Development Manager (Role 45, G2)

---

## 1. Purpose

The CPD Training Catalog is the master library of all Continuing Professional Development programs available across the group. It is the foundational configuration layer for the group's professional development strategy: no training session can be scheduled (page 26) or attendance tracked (page 27) without a corresponding program record in this catalog. The catalog gives the Group Training & Development Manager the ability to design, curate, and maintain a structured CPD framework that aligns with pedagogical goals, compliance requirements, and staff career development pathways.

Every program in the catalog is defined along five key dimensions: category, target audience, delivery mode, duration, and mandatory/optional status. Categories include Pedagogy (classroom management, lesson planning, assessment strategies), Subject Knowledge (content deepening workshops), Technology (EdTech tool training, LMS usage), Leadership (HOD/VP development programs), and Compliance (POCSO, fire safety, child protection — mandatory for all). Target audience is defined by role — a Leadership program targets HODs and Vice Principals; a Pedagogy workshop targets all class teachers; a POCSO refresher targets all staff in student-contact roles. This targeting ensures that CPD hours are credited appropriately and not inflated by irrelevant attendance.

The CPD hour tracking system is designed to drive career progression. Every teacher across the group must accumulate a minimum of 20 CPD hours per academic year to be eligible for annual promotion consideration. The catalog assigns credit hours to each program (typically equal to duration, but configurable). The Training & Development Manager can also assign a validity period to programs — for example, a fire safety certification is valid for 2 years, after which a staff member must re-attend. Expiry triggers an alert on the staff profile and appears in the onboarding tracker for new joiners.

The catalog also tracks facilitator assignment as a workflow step. Programs without assigned facilitators cannot be scheduled. Internal facilitators (existing senior staff or HODs) are assigned from the staff directory. External facilitators (third-party trainers) are entered manually with contact and organisation details. This prevents the Training & Development Manager from scheduling a session before confirming that a trainer is available, which is one of the most common reasons training sessions are cancelled at short notice.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access — can create and archive programs | Policy-level oversight of CPD framework |
| Group HR Manager (42) | G3 | Read-only | Can view catalog to understand training landscape |
| Group Recruiter — Teaching (43) | G0 | No access | — |
| Group Recruiter — Non-Teaching (44) | G0 | No access | — |
| Group Training & Dev Manager (45) | G2 | Full CRUD | Primary owner of catalog |
| Group Performance Review Officer (46) | G1 | Read-only | Views programs relevant to appraisal criteria |
| Group Staff Transfer Coordinator (47) | G3 | No access | — |
| Group BGV Manager (48) | G3 | No access | — |
| Group BGV Executive (49) | G3 | No access | — |
| Group POCSO Coordinator (50) | G3 | Read-only — Compliance category programs | Can view POCSO/child protection programs |
| Group Disciplinary Committee Head (51) | G3 | No access | — |
| Group Employee Welfare Officer (52) | G3 | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Training & Development → CPD Training Catalog`

### 3.2 Page Header
- Title: "CPD Training Catalog"
- Subtitle: "Manage the master library of professional development programs."
- Primary CTA: "+ Add Program" (T&D Manager / HR Director)
- Secondary CTAs: "Export Catalog" | "View CPD Hours Summary (by staff)"

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Mandatory programs with no scheduled sessions in current quarter | "[N] mandatory program(s) have no sessions scheduled this quarter." | Orange |
| Programs with no facilitator assigned | "[N] program(s) are awaiting facilitator assignment." | Yellow |
| Compliance program expired for active staff | "[N] staff member(s) have expired compliance certifications." | Red |
| Programs in Draft > 30 days | "[N] programs have been in Draft status for over 30 days." | Yellow |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Programs in Catalog | Count of Active programs | Neutral blue | — |
| Mandatory Programs | Count of programs with Mandatory = Yes | Neutral | Filters to mandatory |
| Optional Programs | Count with Mandatory = No | Neutral | Filters to optional |
| Programs Scheduled This Quarter | Count with at least 1 session in current quarter | Green if ≥ mandatory count | Filters to scheduled |
| Avg CPD Hours per Teacher (YTD) | Mean CPD hours credited across all teaching staff | Amber if < 10, Green if ≥ 20 | Opens CPD hours summary |
| Programs Awaiting Facilitator | Count with no facilitator assigned and status Active | Red if > 0 | Filters to unassigned |

---

## 5. Main Table — CPD Programs

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Program Name | Text (link to view drawer) | Yes | Yes (search) |
| Category | Chip (Pedagogy / Subject / Technology / Leadership / Compliance) | Yes | Yes |
| Target Role | Text (comma-separated role targets) | No | Yes (dropdown) |
| Mode | Chip (In-Person / Online / Hybrid) | Yes | Yes |
| Duration | Text (e.g., "4 hours", "2 days") | Yes | No |
| Credit Hours | Decimal | Yes | No |
| Mandatory | Boolean chip (Yes / No) | Yes | Yes |
| Validity Period | Text (e.g., "2 years" / "Annual" / "One-time") | No | No |
| Facilitator | Text (Internal/External name) | No | Yes (assigned / unassigned) |
| Scheduled Sessions | Integer (count of future sessions) | Yes | No |
| Status | Chip (Active / Draft / Archived) | Yes | Yes |
| Actions | View / Edit / Schedule Session / Archive | No | No |

### 5.1 Filters
- Category: All | Pedagogy | Subject Knowledge | Technology | Leadership | Compliance
- Mandatory: All | Mandatory | Optional
- Status: All | Active | Draft | Archived
- Mode: All | In-Person | Online | Hybrid
- Facilitator: All | Assigned | Unassigned

### 5.2 Search
Search by program name. Minimum 2 characters, 400ms debounce.

### 5.3 Pagination
Server-side pagination, 20 programs per page. Navigation controls with total program count.

---

## 6. Drawers

### 6.1 Drawer: Add Program (Create)
Fields: Program Title (text, required), Category (dropdown), Program Description (textarea), Target Audience (multi-select role checkboxes: Class Teacher / Subject Teacher / HOD / Vice Principal / Principal / Warden / All Teaching Staff / All Staff / Custom), Delivery Mode (In-Person / Online / Hybrid), Duration (value + unit: Hours / Days), Credit Hours (decimal, default = duration in hours), Mandatory (Yes/No toggle), Validity Period (None / 6 Months / 1 Year / 2 Years / Academic Year), Facilitator Type (Internal / External), Internal Facilitator (typeahead — staff search, visible if Internal), External Facilitator Name + Organisation + Contact (fields visible if External), Pre-reading Material Upload (PDF, optional, max 10 MB), Status (Draft / Active).
Validation: Title required; Credit Hours > 0; if Mandatory = Yes and Compliance category, system verifies at least one target audience is selected.
On Save: POST to API, row prepended to table, toast shown.

### 6.2 Drawer: View Program
Read-only. All program fields, pre-reading material download link, upcoming scheduled sessions list (count + next session date). History of past sessions (count, total attendees, avg attendance %). "Schedule Session" shortcut button at drawer footer (opens Training Session Manager with this program pre-selected).

### 6.3 Drawer: Edit Program
All fields editable except Category (immutable after creation — must archive and recreate to change category). Change Reason (textarea, required). Warning displayed if program has active scheduled sessions: "Editing this program will affect [N] scheduled sessions. Participants will not be auto-notified — send notifications manually."
On Save: PATCH to API, row updated, drawer closes.

### 6.4 Modal: Archive Program
Confirmation: "Archiving [Program Name] will prevent new sessions from being created. Existing scheduled sessions are unaffected. Confirm?" Reason (textarea, required). On Confirm: status → Archived, row moves to Archived filter view.

---

## 7. Charts

**CPD Hours by Category — Horizontal Bar Chart:** shows total CPD hours delivered in the current academic year per category (Pedagogy / Subject / Technology / Leadership / Compliance). Rendered via Chart.js. Toggle: "Show Chart / Hide". Positioned below the table.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Program created | "Program '[Title]' added to the catalog." | Success | 4s |
| Program updated | "Program '[Title]' updated." | Success | 4s |
| Program archived | "Program '[Title]' archived." | Info | 4s |
| Session scheduled shortcut | "Redirecting to Session Manager with program pre-selected." | Info | 3s |
| Facilitator assigned | "Facilitator assigned to '[Program Title]'." | Success | 4s |
| Catalog exported | "CPD catalog downloaded." | Success | 3s |
| Duplicate title warning | "A program with this title already exists. Use a unique name." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| Catalog empty | "No Programs in Catalog" | "Add CPD programs to begin scheduling training sessions for staff." | Add Program |
| Filter returns no results | "No Matching Programs" | "Adjust filters or search term to find programs." | Clear Filters |
| Archived catalog empty | "No Archived Programs" | "Programs that are retired will appear here." | — |
| No mandatory programs | "No Mandatory Programs Defined" | "Mark compliance-critical programs as mandatory to enforce attendance." | Add Program |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI card skeletons (6) + table row skeletons (12) |
| Filter change | Table body row skeletons |
| Drawer open | Form field skeletons (8 fields) |
| Chart render | Spinner in chart container |
| File upload in form | Upload progress bar within file field |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) | T&D Manager (45) | Read-Only Roles (42, 46, 50) |
|---|---|---|---|
| Add Program button | Visible + enabled | Visible + enabled | Hidden |
| Edit action | Visible + enabled | Visible + enabled | Hidden |
| Archive action | Visible + enabled | Visible + enabled | Hidden |
| Schedule Session shortcut | Visible | Visible | Hidden |
| View drawer | Visible | Visible | Visible |
| CPD Hours Summary button | Visible | Visible | Visible (46 only) |
| Catalog export | Visible | Visible | Hidden |
| Facilitator assignment field | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/training/catalog/` | JWT | List all programs (paginated) |
| POST | `/api/v1/hr/training/catalog/` | JWT | Create new program |
| GET | `/api/v1/hr/training/catalog/{id}/` | JWT | Fetch program detail |
| PATCH | `/api/v1/hr/training/catalog/{id}/` | JWT | Update program |
| PATCH | `/api/v1/hr/training/catalog/{id}/archive/` | JWT | Archive program |
| GET | `/api/v1/hr/training/catalog/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/training/catalog/chart/` | JWT | CPD hours by category chart data |
| GET | `/api/v1/hr/training/catalog/export/` | JWT | Download catalog |
| GET | `/api/v1/hr/training/catalog/cpd-summary/` | JWT | CPD hours per teacher summary |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/training/catalog/?q={val}` | `#catalog-table-body` | innerHTML |
| Category filter | change | GET `/api/v1/hr/training/catalog/?category={val}` | `#catalog-table-body` | innerHTML |
| Multi-filter apply | change | GET `/api/v1/hr/training/catalog/?mandatory={}&mode={}&status={}&facilitator={}` | `#catalog-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/training/catalog/?page={n}` | `#catalog-table-body` | innerHTML |
| Add Program drawer | click | GET `/group/hr/training/catalog/add/drawer/` | `#drawer-container` | innerHTML |
| View drawer open | click | GET `/group/hr/training/catalog/{id}/view/drawer/` | `#drawer-container` | innerHTML |
| Edit drawer open | click | GET `/group/hr/training/catalog/{id}/edit/drawer/` | `#drawer-container` | innerHTML |
| Create submit | submit | POST `/api/v1/hr/training/catalog/` | `#catalog-table-body` | afterbegin |
| Edit submit | submit | PATCH `/api/v1/hr/training/catalog/{id}/` | `#program-row-{id}` | outerHTML |
| Archive modal | click | GET `/group/hr/training/catalog/{id}/archive/modal/` | `#modal-container` | innerHTML |
| Archive confirm | click | PATCH `/api/v1/hr/training/catalog/{id}/archive/` | `#program-row-{id}` | outerHTML |
| Chart toggle | click | GET `/group/hr/training/catalog/chart/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
