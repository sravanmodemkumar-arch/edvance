# 46 — Special Needs Student Registry

> **URL:** `/group/acad/special-ed/students/`
> **File:** `46-special-needs-registry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Special Education Coordinator G3 · CAO G4 · Academic Director G3 (summary view) · Academic MIS Officer G1 (anonymised stats only)

---

## 1. Purpose

The Special Needs Student Registry is the group-level centralised record of all students with identified disabilities, learning differences, or special educational needs across every branch. In a large institution group with 50 branches and potentially 100–500 students with active IEPs, maintaining this data in scattered branch-level files is a compliance failure and a service gap — students who transfer branches, sit for group-level exams, or need accommodations arranged at the group level require a single source of truth.

This page is designed for the Group Special Education Coordinator, who is responsible for ensuring every identified student has an active IEP, receives appropriate accommodations in exams, and is reviewed on schedule as per NCPCR guidelines. The registry also enables the group to meet its statutory obligations under the Rights of Persons with Disabilities Act (RPWD Act 2016) and the CBSE Special Exam Policy, which mandate documented accommodations and annual IEP reviews.

DPDP Act 2023 compliance is non-negotiable on this page: student identity data for special needs students is among the most sensitive categories of personal data under Indian law. Names and contact information are therefore masked for all roles below G3 — the MIS officer sees only anonymised counts. Every access to a student record in the drawer triggers an immutable access log. A consent banner appears every time the student-detail drawer is opened, reminding the user that they are accessing sensitive health-related data and that their access is logged.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full — full name visible | ❌ Cannot create/edit | Supervisory view; can view all detail |
| Group Academic Director | G3 | ✅ Summary only — no student PII | ❌ | Can see branch-level counts and IEP status |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access; accesses accommodations via page 48 |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ✅ Full — full name and all PII visible | ✅ Full CRUD | Primary owner of this page |
| Group Academic MIS Officer | G1 | ✅ Anonymised stats only — no student names | ❌ | Counts per branch, per disability type only |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

**DPDP Act 2023 compliance:**
- Student name and contact details are masked (shown as "Student ***") for all roles below G3.
- G1 (MIS Officer) cannot access the student-level table at all — only the summary stats bar.
- G3 Special Ed Coordinator and G4 CAO see full PII.
- G3 Academic Director sees the table but with names masked; drawer is blocked.
- Every opening of the student-detail drawer generates an immutable access log entry: user ID, role, timestamp, IP address, student ID accessed.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Special Education  ›  Student Registry
```

### 3.2 Page Header
```
Special Needs Student Registry                              [+ Add Student]  [Export Registry ↓]
Centralised cross-branch record — DPDP Act 2023 compliant        (Special Ed Coord only)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Registered Students | Count across all branches |
| Active IEPs | Count of students with active IEP |
| IEP Reviews Due This Month | Count |
| IEP Reviews Overdue | Count — highlighted red |
| Branches with 0 Special Needs Students | Count — may indicate under-identification |
| NCPCR Report Due | Days until next mandatory reporting date |

Stats bar visible to all roles with page access (MIS sees this stats bar only).

---

## 4. Main Content

> **MIS Officer (G1):** Sees only the summary stats bar above. The table and all student records are hidden. A notice reads: "Detailed student records are restricted. You can download anonymised branch-level summaries from Special Ed Reports (page 49)."

### 4.1 Search
- G3 Special Ed Coord: Full-text across Student ID and Student Name
- G4 CAO: Full-text across Student ID and Student Name
- G3 Academic Director: Student ID only (name search blocked, masked)
- 300ms debounce · Highlights match in ID column

### 4.2 Advanced Filters (slide-in drawer, active chips, Clear All)

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches in group |
| Disability Type | Multi-select | Learning Disability (Dyslexia/Dyscalculia/ADHD) · Physical Disability · Hearing Impairment · Visual Impairment · Speech Impairment · Autism Spectrum · Multiple Disabilities · Other |
| IEP Status | Multi-select | Active · Review Due · Overdue · Inactive / Completed |
| Class | Multi-select | Class 1–12 |
| Support Staff Assigned | Select | Yes / No |
| Added in last N days | Select | 30 / 60 / 90 days |

Active filter chips dismissible. "Clear All" link. Filter count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible To | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | Special Ed Coord | Bulk select |
| Student ID | Text | ✅ | All roles | Internal student ID |
| Name | Text | ✅ | G3 Spec Ed Coord, G4 CAO | Masked as "Student ***" for G3 Academic Dir |
| Branch | Text | ✅ | All roles | |
| Class | Badge | ✅ | All roles | |
| Disability Type | Badge | ✅ | G3 Spec Ed Coord, G4 CAO | Masked for Academic Dir |
| IEP Status | Badge | ✅ | All roles | Active (green) · Review Due (amber) · Overdue (red) · Inactive (grey) |
| Last Review | Date | ✅ | G3 Spec Ed Coord, G4 CAO | Red if > 12 months ago |
| Next Review Due | Date | ✅ | G3 Spec Ed Coord, G4 CAO | Amber if ≤ 30 days |
| Support Staff Assigned | Badge | ✅ | G3 Spec Ed Coord, G4 CAO | Name or "Not Assigned" |
| Actions | — | ❌ | G3 Spec Ed Coord only | |

**Default sort:** IEP Status (Overdue first, then Review Due, then Active).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z students" · Page jump input.

### 4.4 Row Actions

| Action | Visible To | Drawer | Notes |
|---|---|---|---|
| View | Special Ed Coord, CAO | `student-view` drawer 560px | Full profile — consent banner shown |
| Edit | Special Ed Coord | `student-add` drawer 640px (pre-filled) | Edit details |
| Create IEP | Special Ed Coord | Navigates to IEP Manager (page 47) | Only shown if no active IEP |
| Review IEP | Special Ed Coord | Navigates to IEP Manager review flow | Only shown if IEP status is Review Due or Overdue |
| Deactivate | Special Ed Coord | Confirm modal | When student leaves school or special ed services end |

### 4.5 Bulk Actions (shown when rows selected — Special Ed Coord only)

| Action | Notes |
|---|---|
| Export Selected (XLSX) | Selected students — DPDP-compliant export with access log |
| Send IEP Review Reminder — Selected Branches | Sends reminder to branch counsellors for selected student set |

---

## 5. Drawers & Modals

### 5.1 DPDP Consent Banner
**Triggered:** Every time the student-detail drawer (`student-view` or `student-add`) is opened.
**Display:** Full-width amber banner at top of drawer:
> "You are accessing sensitive personal and health data for a minor student. Access to this record is immutably logged under the Digital Personal Data Protection Act 2023. Only access this record for a legitimate educational purpose."

**[I Understand — Proceed]** button required before drawer content is visible. Cannot be bypassed.

### 5.2 Drawer: `student-add` — Add / Edit Student
- **Trigger:** [+ Add Student] header button or Edit row action
- **Width:** 640px
- **Tabs:** Identity · Disability Details · Support Needs · Initial Accommodations · Guardian Contact

#### Tab: Identity
| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | ✅ | All branches |
| Student (search from branch roster) | Search + select | ✅ | Must be enrolled student |
| Class & Section | Auto-populated | — | From student roster |
| Date of identification | Date | ✅ | Cannot be future date |
| Identified by | Text | ✅ | Psychologist/specialist name |

#### Tab: Disability Details
| Field | Type | Required | Validation |
|---|---|---|---|
| Primary Disability Type | Select | ✅ | See filter options above |
| Secondary Disability Type | Select | ❌ | Same options |
| Severity | Select | ✅ | Mild / Moderate / Severe |
| Medical / Psychological Certificate | File upload | ✅ | PDF, max 10 MB |
| Certificate issued by | Text | ✅ | Doctor/institution name |
| Certificate date | Date | ✅ | |
| Certificate valid until | Date | ❌ | If certificate has expiry |

#### Tab: Support Needs
| Field | Type | Required | Notes |
|---|---|---|---|
| Support required in class | Textarea | ✅ | Free text, max 500 chars |
| Support required in exams | Textarea | ✅ | Will auto-populate accommodation tracker (page 48) |
| Specialist sessions (speech/OT etc.) | Toggle | ❌ | If on: sessions per week + provider |
| Support staff assigned | Search + select | ❌ | From provisioned staff |

#### Tab: Initial Accommodations
| Field | Type | Required | Notes |
|---|---|---|---|
| Exam accommodations (pre-populate) | Multi-select | ❌ | Extra time 30 min / Extra time 60 min / Scribe / Separate room / Large font paper / Oral exam / Reader |
| Other accommodations | Textarea | ❌ | Max 300 chars |
| Approved by | Text | ❌ | Psychologist/medical authority |

#### Tab: Guardian Contact
| Field | Type | Required | Notes |
|---|---|---|---|
| Guardian name | Text | ✅ | |
| Relationship | Select | ✅ | Parent / Legal Guardian / Other |
| Phone | Text | ✅ | 10-digit Indian mobile |
| Email | Email | ❌ | |
| Consent to share IEP with guardian | Toggle | ✅ | DPDP consent — must be on for IEP PDF export |

- **Submit:** "Save Student Record"
- **On success:** Student added to registry · IEP creation prompted

### 5.3 Drawer: `student-view`
- **Width:** 560px
- **Tabs:** Profile · IEP · Accommodations · Progress · Incident History

**Tab: Profile** — All identity, disability, and guardian fields read-only.

**Tab: IEP** — Current IEP summary: goals count, % met, last review, next review due. [Open Full IEP →] link to IEP Manager.

**Tab: Accommodations** — All approved accommodations listed. Upcoming exam accommodation requests from page 48.

**Tab: Progress** — Chronological list of IEP reviews with goal achievement %. Mini line chart of goal achievement over time.

**Tab: Incident History** — POCSO/welfare incidents logged from branch level. Read-only.

### 5.4 Modal: `deactivate-confirm`
- **Width:** 420px
- **Content:** "Mark [Student ID] as inactive in the special needs registry?"
- **Fields:** Reason (Select): Transferred to another institution / Completed schooling / Support services no longer required / Other · Details (Textarea, min 20 chars)
- **Buttons:** [Confirm Deactivate] · [Cancel]

---

## 6. Charts

### 6.1 Branch Caseload (Horizontal Bar)
- **Type:** Horizontal bar
- **Data:** Count of active special needs students per branch
- **Colour:** Gradient (low = teal, high = amber/red)
- **Tooltip:** Branch · Students: N
- **Export:** PNG

### 6.2 Disability Type Distribution (Donut)
- **Type:** Donut
- **Data:** Count per disability type across group
- **Colorblind-safe palette**
- **Centre text:** Total students
- **Tooltip:** Type · Count · %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Student added | "Student record added to Special Needs Registry" | Success | 4s |
| Student updated | "Student record updated" | Success | 4s |
| Student deactivated | "Student marked inactive. Record archived." | Warning | 6s |
| IEP review reminder sent | "IEP review reminder sent to [N] branches" | Success | 4s |
| Export completed | "Export preparing… access will be logged" | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No students registered | "No special needs students registered" | "Add students from branches or ask branches to submit records via branch portal" | [+ Add Student] |
| No students match filters | "No students match your filters" | "Try clearing some filters" | [Clear Filters] |
| No search results | "No students found" | "Search by Student ID or name" | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) |
| Table filter/search/sort/page | Inline skeleton rows |
| Student-view drawer open | Consent banner → spinner → tab content |
| Student-add drawer open | Spinner → form tabs |
| Charts load | Skeleton chart areas |
| Export triggered | Spinner in export button |

---

## 10. Role-Based UI Visibility

| Element | Spec Ed Coord G3 | CAO G4 | Academic Dir G3 | MIS G1 |
|---|---|---|---|---|
| Full student table | ✅ | ✅ | ✅ (names masked) | ❌ (stats bar only) |
| Student name column | ✅ (full) | ✅ (full) | ❌ (masked) | ❌ |
| Disability type column | ✅ | ✅ | ❌ (masked) | ❌ |
| [+ Add Student] button | ✅ | ❌ | ❌ | ❌ |
| Edit row action | ✅ | ❌ | ❌ | ❌ |
| View row action | ✅ | ✅ | ❌ | ❌ |
| Deactivate action | ✅ | ❌ | ❌ | ❌ |
| Bulk actions | ✅ | ❌ | ❌ | ❌ |
| Export button | ✅ | ✅ | ❌ | ❌ |
| Charts | ✅ | ✅ | ✅ (anonymised) | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/special-ed/students/` | JWT | List students (role-filtered PII masking server-side) |
| GET | `/api/v1/group/{group_id}/acad/special-ed/students/stats/` | JWT | Stats bar (works for all roles including G1) |
| GET | `/api/v1/group/{group_id}/acad/special-ed/students/{id}/` | JWT (G3+) | Student detail — triggers access log |
| POST | `/api/v1/group/{group_id}/acad/special-ed/students/` | JWT (G3 Spec Ed) | Create student record |
| PUT | `/api/v1/group/{group_id}/acad/special-ed/students/{id}/` | JWT (G3 Spec Ed) | Update student record |
| PATCH | `/api/v1/group/{group_id}/acad/special-ed/students/{id}/deactivate/` | JWT (G3 Spec Ed) | Deactivate with reason |
| GET | `/api/v1/group/{group_id}/acad/special-ed/students/export/?format=xlsx` | JWT (G3+) | Export — access logged |
| GET | `/api/v1/group/{group_id}/acad/special-ed/students/charts/caseload/` | JWT (G3+) | Branch caseload bar |
| GET | `/api/v1/group/{group_id}/acad/special-ed/students/charts/disability-types/` | JWT (G3+) | Donut chart |
| POST | `/api/v1/group/{group_id}/acad/special-ed/students/bulk-remind/` | JWT (G3 Spec Ed) | IEP review reminders |

**Access log endpoint (immutable, write-only from application):**
| POST | `/api/v1/group/{group_id}/acad/special-ed/access-log/` | JWT | Log: user_id, student_id, timestamp, IP — server-side only |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../students/?q=` | `#students-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../students/?filters=` | `#students-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../students/?sort=&dir=` | `#students-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../students/?page=` | `#students-table-section` | `innerHTML` |
| View drawer (consent gate) | `click` | GET `.../students/{id}/consent-gate/` | `#drawer-body` | `innerHTML` |
| Consent confirmed → load profile | `click` | GET `.../students/{id}/` | `#drawer-body` | `innerHTML` |
| Student add drawer | `click` | GET `.../students/create-form/` | `#drawer-body` | `innerHTML` |
| Student create submit | `submit` | POST `.../students/` | `#drawer-body` | `innerHTML` |
| Deactivate confirm | `click` | PATCH `.../students/{id}/deactivate/` | `#student-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
