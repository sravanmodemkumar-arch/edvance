# Group 3 — Division A: School Leadership & Administration — Pages Reference

> **Division:** A — Leadership & Administration
> **Roles:** 5 roles (see Role Summary below)
> **Base URL prefix:** `/school/admin/`
> **Theme:** Light (`portal_base.html`)
> **Group:** Group 3 — School Portal
> **Status key:** ✅ Spec done · ⬜ Not started

---

## Scale Context

| Dimension | Value |
|---|---|
| Schools on Platform | 1,000 |
| Students per school (avg) | 1,000 (range: 300 – 5,000) |
| Classes | LKG/UKG + I–XII (14 levels); or I–X/XII for secondary/senior secondary |
| Sections per class | 2–8 sections (A, B, C … H) |
| Teaching staff per school (avg) | 40–80 |
| Admin + support staff per school | 10–25 |
| Boards | CBSE · ICSE · 28 State Boards (AP, TS, MH, KA, TN, UP, WB, RJ, MP, …) |
| Streams (XI–XII) | Science PCM · Science PCB · Commerce · Humanities/Arts · Vocational |
| Integrated coaching schools | Up to 400 schools — dual curriculum (board + JEE/NEET prep) |
| Residential schools | 150+ schools with hostel facility |
| Academic year | April 1 – March 31 (CBSE/ICSE) · June–May (TN/Kerala/AP/TS boards) |
| Languages of instruction | English · Hindi · Telugu · Tamil · Kannada · Marathi · Bengali · Malayalam |
| Student types | Day Scholar (Regular · Scholarship · RTE 25% · Special Needs) · Hosteler (Boys/Girls) · NRI |

---

## Critical Indian School Context

**The Principal is the nerve centre of an Indian school.** In the CBSE/state board system, the Principal has legal and regulatory accountability that goes far beyond academic oversight:
- **CBSE Affiliation Officer** — must ensure CBSE norms are met year-round (infrastructure, teacher qualifications, student-teacher ratio); affiliation withdrawal means students cannot appear for board exams
- **Defaulting fee principal** — under RTE Act, 25% seats must be given free to EWS students; principal is liable if this isn't maintained
- **POCSO designated person** — every school must designate a staff member to receive POCSO complaints; in most schools this is the Principal or Vice-Principal
- **DPDPA data controller** — all student and staff PII is under the institution's control; Principal has data governance accountability
- **Exam administration officer** — for CBSE/ICSE board exams conducted at the school centre, the Principal is the Centre Superintendent

The **Promoter/Owner/Correspondent** is the financial and governance layer above the Principal — in India, most private schools are run by Societies, Trusts, or Section 8 Companies. The Correspondent (Trustee representative) controls fees, salaries, and capital expenditures. The Principal operates within the Correspondent's approved budget.

---

## Division A — Role Summary

| # | Role | Level | Description | Post-Login URL |
|---|---|---|---|---|
| 1 | School Promoter / Correspondent | S7 | Trustee/owner representative; controls fee structure, major expenditures, staff appointments above VP level; read-only operational data + financial approvals | `/school/admin/promoter/` |
| 2 | Principal | S6 | Full institutional access; CBSE Centre Superintendent; RBAC root for institution; TOTP-gated critical actions | `/school/admin/principal/` |
| 3 | Vice-Principal (Academic) | S5 | Academic calendar, exam coordination, syllabus oversight, result publication, teacher performance | `/school/admin/vp-academic/` |
| 4 | Vice-Principal (Administration) | S5 | Admissions, infrastructure, transport, hostel, non-teaching staff, procurement | `/school/admin/vp-admin/` |
| 5 | Administrative Officer / School Secretary | S3 | Communication dispatch, circular management, visitor records, staff registry, data entry coordination | `/school/admin/office/` |

**Level key:** S7 = Promoter (financial governance) · S6 = Principal (full ops) · S5 = Senior Management (VP) · S4 = HOD/Dept Head · S3 = Administrative Professional · S2 = Support Staff · S1 = Read-Only

> **Note:** Single VP schools use only the Principal and one combined VP role. The level system allows the Principal to create/modify roles below S6.

---

## Section 1 — Role Dashboards (post-login landing, one per role)

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| A-01 | Promoter / Correspondent Dashboard | `/school/admin/promoter/` | `a-01-promoter-dashboard.md` | P0 | ✅ |
| A-02 | Principal Dashboard | `/school/admin/principal/` | `a-02-principal-dashboard.md` | P0 | ✅ |
| A-03 | VP Academic Dashboard | `/school/admin/vp-academic/` | `a-03-vp-academic-dashboard.md` | P0 | ✅ |
| A-04 | VP Administration Dashboard | `/school/admin/vp-admin/` | `a-04-vp-admin-dashboard.md` | P0 | ✅ |
| A-05 | Administrative Officer Dashboard | `/school/admin/office/` | `a-05-office-dashboard.md` | P0 | ✅ |

---

## Section 2 — Institution Profile & Configuration

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| A-06 | Institution Profile & Settings | `/school/admin/profile/` | `a-06-institution-profile.md` | P0 | ✅ |
| A-07 | Board Affiliation Manager | `/school/admin/affiliation/` | `a-07-board-affiliation.md` | P1 | ✅ |
| A-08 | Class & Section Manager | `/school/admin/classes/` | `a-08-class-section-manager.md` | P0 | ✅ |
| A-09 | Stream & Subject Configuration | `/school/admin/streams/` | `a-09-stream-subject-config.md` | P1 | ✅ |

---

## Section 3 — Academic Calendar

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| A-10 | Annual Academic Calendar | `/school/admin/calendar/` | `a-10-academic-calendar.md` | P0 | ✅ |
| A-11 | Holiday & Leave Calendar | `/school/admin/calendar/holidays/` | `a-11-holiday-calendar.md` | P1 | ✅ |
| A-12 | Exam Calendar | `/school/admin/calendar/exams/` | `a-12-exam-calendar.md` | P0 | ✅ |

---

## Section 4 — Student Overview

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| A-13 | Student Strength Dashboard | `/school/admin/students/strength/` | `a-13-student-strength-dashboard.md` | P0 | ✅ |
| A-14 | Admission Pipeline | `/school/admin/admissions/pipeline/` | `a-14-admission-pipeline.md` | P0 | ✅ |
| A-15 | RTE Compliance Tracker | `/school/admin/rte/` | `a-15-rte-compliance-tracker.md` | P1 | ✅ |

---

## Section 5 — Staff Overview

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| A-16 | Staff Directory & Strength | `/school/admin/staff/` | `a-16-staff-directory.md` | P0 | ✅ |
| A-17 | Staff Attendance Overview | `/school/admin/staff/attendance/` | `a-17-staff-attendance-overview.md` | P1 | ✅ |
| A-18 | Staff Leave Management | `/school/admin/staff/leave/` | `a-18-staff-leave-management.md` | P1 | ✅ |
| A-19 | Recruitment & Vacancy Tracker | `/school/admin/staff/recruitment/` | `a-19-recruitment-tracker.md` | P2 | ✅ |

---

## Section 6 — Fee & Finance Overview

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| A-20 | Fee Collection Dashboard | `/school/admin/finance/fee-dashboard/` | `a-20-fee-collection-dashboard.md` | P0 | ✅ |
| A-21 | Monthly Financial Summary | `/school/admin/finance/monthly/` | `a-21-monthly-financial-summary.md` | P1 | ✅ |
| A-22 | Salary & Payroll Overview | `/school/admin/finance/payroll/` | `a-22-salary-payroll-overview.md` | P1 | ✅ |

---

## Section 7 — Approvals & Governance

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| A-23 | Approval Workflow Hub | `/school/admin/approvals/` | `a-23-approval-workflow-hub.md` | P0 | ✅ |
| A-24 | Policy Repository | `/school/admin/policies/` | `a-24-policy-repository.md` | P2 | ✅ |
| A-25 | Procurement & Purchase Requests | `/school/admin/procurement/` | `a-25-procurement-requests.md` | P2 | ✅ |

---

## Section 8 — Communication

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| A-26 | Principal's Communication Hub | `/school/admin/communications/` | `a-26-communications-hub.md` | P1 | ✅ |
| A-27 | Circular & Notice Manager | `/school/admin/circulars/` | `a-27-circular-manager.md` | P1 | ✅ |
| A-28 | Parent Communication Log | `/school/admin/communications/parents/` | `a-28-parent-communication-log.md` | P1 | ✅ |

---

## Section 9 — Compliance & Safety

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| A-29 | Compliance Dashboard | `/school/admin/compliance/` | `a-29-compliance-dashboard.md` | P1 | ✅ |
| A-30 | POCSO Compliance Centre | `/school/admin/compliance/pocso/` | `a-30-pocso-compliance.md` | P1 | ✅ |
| A-31 | Safety & Infrastructure Audit | `/school/admin/compliance/safety/` | `a-31-safety-audit.md` | P2 | ✅ |

---

## Section 10 — Analytics, Reports & Audit

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| A-32 | MIS Dashboard | `/school/admin/mis/` | `a-32-mis-dashboard.md` | P0 | ✅ |
| A-33 | Academic Performance Overview | `/school/admin/mis/academics/` | `a-33-academic-performance.md` | P1 | ✅ |
| A-34 | Audit Log | `/school/admin/audit-log/` | `a-34-audit-log.md` | P1 | ✅ |
| A-35 | User & Role Management | `/school/admin/users/` | `a-35-user-role-management.md` | P1 | ✅ |

---

## Shared Drawers & Overlays (all div-a pages)

| Drawer | Trigger | Width | Tabs | Description |
|---|---|---|---|---|
| `student-quick-view` | Student Strength → student row | 560px | Profile · Attendance · Marks · Fee | Read-only student summary |
| `staff-quick-view` | Staff Directory → staff row | 560px | Profile · Attendance · Leave · BGV | Staff summary with leave status |
| `staff-create` | Staff Directory → + Add Staff | 680px | Personal · Qualifications · Role · Salary | Full onboarding form |
| `staff-edit` | Staff table → Edit | 680px | same tabs | Edit staff details |
| `leave-approve` | Leave Management → pending row | 420px | Details · History · Action | Approve/reject with reason |
| `approval-action` | Approval Hub → pending row | 560px | Details · Context · History · Action | Multi-type approval handler |
| `circular-compose` | Circular Manager → + New | 680px | Content · Targeting · Channels · Schedule · Preview | Multi-channel circular composer |
| `class-create` | Class Manager → + Add Class | 420px | Class Details · Sections · Class Teacher | New class-section setup |
| `holiday-create` | Holiday Calendar → + Holiday | 400px | Date · Type · Description · Notify | Add holiday with notification |
| `exam-event-create` | Exam Calendar → + Add Event | 480px | Exam · Dates · Classes · Instructions | Exam calendar event |
| `admission-detail` | Admission Pipeline → applicant | 640px | Application · Documents · Interview · Fee · Offer | Full admission workflow |
| `rte-student-detail` | RTE Tracker → student row | 480px | Profile · Admission · Documents · Benefits | RTE student record |
| `purchase-request-create` | Procurement → + Request | 560px | Item · Quantity · Vendor · Budget · Justification | PR form with budget check |
| `purchase-request-approve` | Procurement → pending row | 520px | Request Details · Quotations · Budget · Action | Approve/reject with PO creation |
| `policy-create` | Policy Repository → + New | 680px | Content · Scope · Effective Date · Acknowledgement | Versioned policy with staff acks |
| `compliance-detail` | Compliance Dashboard → item | 480px | Status · Evidence · Action Plan · Deadline · Owner | Compliance item with evidence upload |
| `pocso-case-create` | POCSO Centre → + New Report | 640px | Incident · Parties · Details · Evidence · ICC Assignment | Confidential POCSO case record |
| `user-provision` | User & Role Mgmt → + Add User | 560px | Profile · Role · Login · Notify | User creation + invite |
| `user-edit` | User table → edit | 480px | Profile · Role · Status · History | Edit user role/status |
| `audit-detail` | Audit Log → row | 520px | Event · Before/After · Context · IP | Full audit event detail |
| `financial-summary-drill` | Monthly Summary → row | 560px | Fee · Payroll · Expenses · Surplus | Category drill-down |
| `mis-report-build` | MIS Dashboard → Build Report | 680px | Sections · Filters · Date Range · Recipients · Schedule | Custom report builder |

---

## UI Component Standard (applied to every page in div-a)

| Component | Specification |
|---|---|
| **Theme** | Light mode (`portal_base.html`) — white background, navy sidebar, accent colour per board (CBSE blue, ICSE maroon, State Board amber) |
| **Tables** | Sortable all columns · Checkbox row select + select-all · Responsive (card on mobile < 768px) · Column visibility toggle |
| **Search** | Full-text, 300ms debounce, highlights match |
| **Advanced Filters** | Slide-in filter drawer · Active filters as dismissible chips · "Clear All" · Filter count badge |
| **Pagination** | Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z results" |
| **Drawers** | Slide from right · Widths: 400/420/480/520/560/640/680px · Backdrop click closes (unsaved-changes guard) |
| **Modals** | Centred overlay · confirm/delete only · Max 480px width |
| **Forms** | Inline validation on blur · Required `*` · Character counter on textareas · Disabled submit until valid |
| **Toasts** | Bottom-right · Success 4s · Error manual dismiss · Warning 6s · Info 4s · Max 3 stacked |
| **Charts** | Chart.js 4.x · Responsive · Colorblind-safe · PNG export |
| **Role-based UI** | Every write control rendered server-side based on role level — S1 (Promoter read-only view) never sees edit buttons; S7 sees all |
| **Board branding** | School logo + board affiliation badge in top-left of header on all pages |
| **Academic year selector** | Persistent top-bar dropdown — selected year applies to all data on the page; default = current year |

---

## Role → Page Access Matrix

| Page | Promoter S7 | Principal S6 | VP Academic S5 | VP Admin S5 | Office S3 |
|---|---|---|---|---|---|
| A-01 Promoter Dashboard | ✅ Full | — | — | — | — |
| A-02 Principal Dashboard | ✅ Read | ✅ Full | — | — | — |
| A-03 VP Academic Dashboard | — | ✅ Read | ✅ Full | — | — |
| A-04 VP Admin Dashboard | — | ✅ Read | — | ✅ Full | — |
| A-05 Office Dashboard | — | ✅ Read | — | — | ✅ Full |
| A-06 Institution Profile | ✅ View | ✅ Full | ✅ View | ✅ View | ✅ View |
| A-07 Board Affiliation | ✅ Approve | ✅ Full | ✅ View | — | — |
| A-08 Class & Section Mgr | — | ✅ Full | ✅ Full | ✅ View | — |
| A-09 Stream & Subject Config | — | ✅ Full | ✅ Full | — | — |
| A-10 Academic Calendar | ✅ View | ✅ Full | ✅ Full | ✅ View | ✅ View |
| A-11 Holiday Calendar | ✅ View | ✅ Approve | ✅ Full | ✅ Full | ✅ View |
| A-12 Exam Calendar | ✅ View | ✅ Full | ✅ Full | — | — |
| A-13 Student Strength | ✅ View | ✅ Full | ✅ Full | ✅ Full | ✅ View |
| A-14 Admission Pipeline | ✅ View | ✅ Approve | — | ✅ Full | ✅ Manage |
| A-15 RTE Compliance | ✅ View | ✅ Full | — | ✅ Full | ✅ View |
| A-16 Staff Directory | ✅ View | ✅ Full | ✅ View | ✅ Full | ✅ View |
| A-17 Staff Attendance | — | ✅ View | ✅ View | ✅ Full | — |
| A-18 Staff Leave | ✅ View | ✅ Approve | ✅ Approve acad | ✅ Full | ✅ Manage |
| A-19 Recruitment Tracker | ✅ Approve | ✅ Full | ✅ View | ✅ Full | — |
| A-20 Fee Collection | ✅ Full | ✅ View | — | ✅ View | — |
| A-21 Monthly Financial | ✅ Full | ✅ View | — | ✅ View | — |
| A-22 Salary & Payroll | ✅ Full | ✅ View | — | ✅ View | — |
| A-23 Approval Workflow Hub | ✅ Promoter items | ✅ Full | ✅ Acad items | ✅ Admin items | — |
| A-24 Policy Repository | ✅ Approve | ✅ Full | ✅ View | ✅ View | ✅ View |
| A-25 Procurement Requests | ✅ Approve major | ✅ Approve | — | ✅ Full | ✅ Create |
| A-26 Communications Hub | ✅ View | ✅ Full | ✅ View | ✅ View | ✅ Manage |
| A-27 Circular Manager | ✅ View | ✅ Approve | ✅ Compose | ✅ Compose | ✅ Full |
| A-28 Parent Comms Log | — | ✅ Full | ✅ View | ✅ View | ✅ View |
| A-29 Compliance Dashboard | ✅ View | ✅ Full | ✅ Acad | ✅ Admin | — |
| A-30 POCSO Centre | — | ✅ Full | ✅ View | — | — |
| A-31 Safety & Infra Audit | ✅ View | ✅ Approve | — | ✅ Full | — |
| A-32 MIS Dashboard | ✅ Full | ✅ Full | ✅ Acad | ✅ Admin | ✅ View |
| A-33 Academic Performance | ✅ View | ✅ Full | ✅ Full | — | — |
| A-34 Audit Log | ✅ View | ✅ Full | ✅ View | ✅ View | — |
| A-35 User & Role Mgmt | — | ✅ Full | ✅ Create S4 and below | ✅ Create S3 and below | — |

---

## Full Functional Coverage — What Each Role Can Do

| # | Job to Be Done | Role | Page |
|---|---|---|---|
| 1 | See school-wide fee collection vs target at a glance | Promoter | A-01, A-20 |
| 2 | Approve large purchases and salary revisions | Promoter | A-23, A-22 |
| 3 | Monitor seat fill rate (admissions progress) | Promoter | A-01, A-14 |
| 4 | See P&L and monthly financial summary | Promoter | A-21 |
| 5 | Verify RTE 25% compliance | Promoter | A-15 |
| 6 | View real-time school health dashboard | Principal | A-02 |
| 7 | Approve exam schedules and results publication | Principal | A-12, A-23 |
| 8 | Manage class-section structure | Principal | A-08 |
| 9 | Control CBSE affiliation compliance | Principal | A-07 |
| 10 | Handle POCSO complaints | Principal | A-30 |
| 11 | Manage user accounts for all staff | Principal | A-35 |
| 12 | Approve all staff leaves | Principal | A-18 |
| 13 | Publish circulars to all parents and staff | Principal | A-27 |
| 14 | View and manage academic calendar | VP Academic | A-03, A-10 |
| 15 | Oversee syllabus and exam calendar | VP Academic | A-09, A-12 |
| 16 | Track teacher performance and attendance | VP Academic | A-17, A-33 |
| 17 | Manage admissions end-to-end | VP Admin | A-04, A-14 |
| 18 | Manage non-teaching staff leave and attendance | VP Admin | A-17, A-18 |
| 19 | Track procurement requests | VP Admin | A-25 |
| 20 | Monitor transport and hostel compliance | VP Admin | A-29 |
| 21 | Dispatch circulars and notices | Office | A-05, A-27 |
| 22 | Maintain visitor and meeting register | Office | A-05 |
| 23 | Manage staff registry and records | Office | A-16 |
| 24 | Coordinate parent communication responses | Office | A-28 |

---

## Implementation Priority

```
P0 — Before school portal goes live
  A-01 – A-05   All 5 role dashboards
  A-02           Principal Dashboard (P0 — most critical)
  A-06           Institution Profile
  A-08           Class & Section Manager
  A-10           Academic Calendar
  A-12           Exam Calendar
  A-13           Student Strength Dashboard
  A-14           Admission Pipeline
  A-20           Fee Collection Dashboard
  A-23           Approval Workflow Hub
  A-32           MIS Dashboard

P1 — Sprint 2
  A-07, A-11, A-15, A-16, A-17, A-18, A-21, A-22, A-26, A-27, A-28, A-29, A-30, A-33, A-34, A-35

P2 — Sprint 3
  A-09, A-19, A-24, A-25, A-31
```

---

*Last updated: 2026-03-26 · Total pages: 35 · Roles: 5 · Group: 3 — School Portal · Status: ✅ All 35 page specs complete*
