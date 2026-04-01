# 54 — Group Academic MIS Report

> **URL:** `/group/acad/mis/report/`
> **File:** `54-academic-mis-report.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Academic MIS Officer G1 · CAO G4 · Academic Director G3 · All G4+ roles (download)

---

## 1. Purpose

The Group Academic MIS Report is the primary structured reporting output of the Division B academic management system — the monthly, termly, and annual summary sent to the Chairman, MD, and Board of the institution group. This is not an analytics dashboard; it is a formal report builder that produces submission-ready PDF and XLSX outputs in a consistent, branded format.

In Indian institution groups, the Monthly MIS Report to the Chairman is a governance ritual: it summarises how many students attended, what the group exam results looked like, whether teachers are performing, and how many students are at risk of dropping out. Without a system like this, the MIS Officer spends two to three days manually compiling data from branch emails and spreadsheets — a process prone to errors, inconsistencies, and delays. This page compresses that process to minutes by pulling all data from the platform's unified database.

The report builder supports multiple scope levels: full group, zone, or individual branch. It allows the MIS Officer to select which sections to include (attendance, results, curriculum completion, teacher performance, dropout count, olympiad outcomes, special needs summary), preview the report inline in HTML, and then download in PDF (with branded group letterhead and page numbers) or XLSX. Recurring schedules can be set so the Monthly MIS report generates and emails automatically to the CAO and Chairman on the first of every month.

---

## 2. Role Access

| Role | Level | Can View | Can Create/Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ Full | ✅ Approve distribution list | Approves who receives scheduled reports |
| Group Academic Director | G3 | ✅ Full | ✅ Generate reports | Can generate any report |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Stream Coordinators (all) | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ❌ | ❌ | No access |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Full | ✅ Full — generate, schedule, download | Primary owner of this page |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |
| Chairman / MD / Board (G5) | Cross-div | ✅ Download only | ❌ | Receive scheduled reports via email |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Academic MIS & Analytics  ›  MIS Report
```

### 3.2 Page Header
```
Group Academic MIS Report                        [Generate New Report]  [Manage Schedules]
Formal MIS reporting — monthly / term / annual                  (MIS Officer, Academic Dir)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Reports Generated This Month | Count |
| Last Report Generated | Datetime |
| Next Scheduled Report | Datetime |
| Active Schedules | Count |

---

## 4. Main Content

### 4.1 Report Builder (primary area — above history table)

**Step 1 — Report Type**

| Type | Description |
|---|---|
| Monthly MIS | Standard monthly report — all core sections — for Chairman/Board |
| Term Report | End-of-term comprehensive summary with exam results |
| Annual Report | Full academic year summary — all metrics |
| Custom | User-selected sections and date range |

**Step 2 — Scope**

| Field | Type | Required |
|---|---|---|
| Report scope | Select | ✅ — Group-wide / Zone (multi-select) / Branch (multi-select) |
| Date range | Date range picker | ✅ — For Monthly: auto-populated as last calendar month |
| Academic year | Select | ✅ |

**Step 3 — Sections to Include**
Checkboxes — all checked by default for Monthly and Term; deselectable for Custom:

- ☑ Attendance Summary (group avg, branch breakdown)
- ☑ Exam Results Summary (last exam cycle — avg marks, pass %, topper)
- ☑ Curriculum Completion (% syllabus covered by branch and stream)
- ☑ Teacher Performance (avg composite score, PIP count, CPD status)
- ☑ Dropout & At-Risk Count (dropout signals, counsellor assignments)
- ☑ Olympiad & Scholarship Outcomes (medals, registrations, awards)
- ☑ Special Needs Summary (IEP count, overdue reviews — anonymised)
- ☑ Academic Calendar Compliance (PTMs held, events scheduled vs conducted)
- ☐ Financial Snapshot (fee collection % — requires Div-D access; off by default)

**Step 4 — Preview & Export**
- [Preview Report] button → renders inline HTML below builder
- [Download PDF] button → PDF with group letterhead, report title, date, MIS Officer name, page numbers
- [Download XLSX] button → raw data per section in separate tabs

### 4.2 Report History Table

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Report ID | Text | ✅ | |
| Type | Badge | ✅ | Monthly / Term / Annual / Custom |
| Scope | Text | ✅ | Group / Zone / [Branch names] |
| Date Range | Text | ✅ | |
| Generated By | Text | ✅ | |
| Generated At | Datetime | ✅ | |
| Sections | Number | ❌ | Count of sections included |
| Download | Icons | ❌ | PDF and XLSX buttons |

**Default sort:** Generated At descending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All.

### 4.3 Search and Filters

- **Search:** Report ID, Generated By
- **Filters:** Report Type · Scope · Generated By · Date range

### 4.4 Row Actions

| Action | Visible To | Notes |
|---|---|---|
| Download PDF | All roles with access | Re-download |
| Download XLSX | All roles with access | |
| Delete | MIS Officer, CAO | Soft delete from history |

---

## 5. Drawers & Modals

### 5.1 Drawer: `report-schedule`
- **Trigger:** [Manage Schedules] header button
- **Width:** 480px

**Existing schedules table:** Report type · Frequency · Next run · Recipients · Actions (Edit / Delete)

**Create new schedule form:**
| Field | Type | Required | Notes |
|---|---|---|---|
| Report type | Select | ✅ | Monthly / Term / Annual |
| Frequency | Select | ✅ | Monthly / Termly / Annual |
| Day of month (for monthly) | Number | Conditional | 1–28 |
| Scope | Multi-select | ✅ | |
| Sections | Checkboxes | ✅ | Pre-filled based on report type |
| Format | Select | ✅ | PDF / XLSX / Both |
| Recipients | Multi-select of roles + email | ✅ | CAO + Chairman pre-selected |
| Active | Toggle | ✅ | Pause/resume schedule |

- **Submit:** "Save Schedule"

### 5.2 Modal: `delete-report-confirm`
- **Width:** 420px
- **Content:** "Remove this report from history? Underlying data is retained."
- **Buttons:** [Confirm] · [Cancel]

---

## 6. Charts

Charts are embedded inside the generated report preview, not on the page itself. Each section of the preview renders its own chart:

| Section | Chart Type |
|---|---|
| Attendance Summary | Horizontal bar (branch attendance %) |
| Exam Results | Grouped bar (avg marks by stream) |
| Teacher Performance | Box plot (composite score distribution) |
| Dropout Signals | Stacked bar (risk level by branch) |
| Curriculum Completion | Heatmap (branch × stream) |

All charts are Chart.js 4.x, colorblind-safe, PNG-exportable in the downloaded PDF.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Report generated | "Report generated. Preview ready." | Success | 4s |
| PDF downloaded | "PDF downloaded." | Info | 4s |
| XLSX downloaded | "XLSX downloaded." | Info | 4s |
| Schedule created | "Auto-report scheduled. Next run: [Date]." | Success | 4s |
| Schedule deleted | "Schedule removed." | Info | 4s |
| Report deleted | "Report removed from history." | Info | 4s |
| Scheduled report sent | "Monthly MIS Report sent to [N] recipients." | Success | — (email notification) |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No reports generated | "No reports yet" | "Generate your first MIS report using the builder above" | [Generate New Report] |
| No schedules set | "No scheduled reports" | "Set up monthly auto-delivery to the Chairman" | [Manage Schedules] |
| No history matches filters | "No reports match" | "Clear filters" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + report builder + history table |
| Report preview generate | Full-width spinner → inline HTML preview renders |
| PDF / XLSX download | Spinner in download button |
| Schedule drawer open | Spinner |
| History filter/page | Skeleton rows |

---

## 10. Role-Based UI Visibility

| Element | MIS G1 | CAO G4 | Academic Dir G3 | G5 Chairman/MD |
|---|---|---|---|---|
| Report builder | ✅ | ✅ | ✅ | ❌ |
| [Manage Schedules] | ✅ | ✅ (approve recipients) | ❌ | ❌ |
| Download PDF/XLSX (history) | ✅ | ✅ | ✅ | ✅ (via email link) |
| Delete from history | ✅ | ✅ | ❌ | ❌ |
| Financial Snapshot section | ❌ (Div-D required) | ✅ (if Div-D access) | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/mis/report/` | JWT | Report history |
| GET | `/api/v1/group/{group_id}/acad/mis/report/stats/` | JWT | Stats bar |
| POST | `/api/v1/group/{group_id}/acad/mis/report/generate/` | JWT (G1 MIS, G3 Dir, G4) | Generate report — returns preview HTML + download token |
| GET | `/api/v1/group/{group_id}/acad/mis/report/{id}/download-pdf/` | JWT | PDF download |
| GET | `/api/v1/group/{group_id}/acad/mis/report/{id}/download-xlsx/` | JWT | XLSX download |
| DELETE | `/api/v1/group/{group_id}/acad/mis/report/{id}/` | JWT (G1 MIS, G4) | Remove from history |
| GET | `/api/v1/group/{group_id}/acad/mis/report/schedules/` | JWT | Scheduled reports list |
| POST | `/api/v1/group/{group_id}/acad/mis/report/schedules/` | JWT (G1 MIS, G4) | Create schedule |
| PUT | `/api/v1/group/{group_id}/acad/mis/report/schedules/{id}/` | JWT (G1 MIS, G4) | Update schedule |
| DELETE | `/api/v1/group/{group_id}/acad/mis/report/schedules/{id}/` | JWT (G1 MIS, G4) | Delete schedule |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Report preview | `click` | POST `.../mis/report/generate/` | `#report-preview-container` | `innerHTML` |
| History search | `input delay:300ms` | GET `.../mis/report/?q=` | `#report-history-body` | `innerHTML` |
| History filter | `click` | GET `.../mis/report/?filters=` | `#report-history-section` | `innerHTML` |
| Pagination | `click` | GET `.../mis/report/?page=` | `#report-history-section` | `innerHTML` |
| Schedule drawer | `click` | GET `.../mis/report/schedules/form/` | `#drawer-body` | `innerHTML` |
| Schedule create | `submit` | POST `.../mis/report/schedules/` | `#drawer-body` | `innerHTML` |
| Delete confirm | `click` | DELETE `.../mis/report/{id}/` | `#report-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
