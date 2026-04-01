# 16 — Financial Audit Reports

- **URL:** `/group/finance/audit-reports/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Roles:** Finance Manager G1 (primary) · Internal Auditor G1 · CFO G1

---

## 1. Purpose

The Financial Audit Reports page is the repository for all internal and external audit reports submitted across branches. Reports include: quarterly internal audit reports (from Group Internal Auditor), statutory audit reports (from external CA firms), CBSE affiliation financial compliance reports, and special audit reports commissioned for irregularity investigations.

The Finance Manager reviews, annotates, and signs off on internal reports. External audit reports are uploaded and linked to the relevant branch and financial year. This page ensures audit evidence is centrally stored, searchable, and accessible during regulatory inspections.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Finance Manager | G1 | Full read + sign off internal reports |
| Group Internal Auditor | G1 | Full read + upload internal reports |
| Group CFO | G1 | Full read |
| Group Chairman | G5 | Read — summary only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Financial Audit Reports
```

### 3.2 Page Header
- **Title:** `Financial Audit Reports`
- **Subtitle:** `[N] Reports · FY [Year] · [X] Pending Sign-off`
- **Right-side controls:** `[FY ▾]` `[Branch ▾]` `[Type ▾]` `[+ Upload Report]` `[Export ↓]`

---

## 4. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Report Title | Text + link | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Type | Badge: Internal Quarterly · Statutory · CBSE · Special | ✅ | ✅ |
| Quarter / Period | Text | ✅ | ✅ |
| Uploaded By | Text | ✅ | — |
| Upload Date | Date | ✅ | — |
| Findings Count | Number | ✅ | — |
| Sign-off Status | Badge: Pending · Signed Off · Rejected | ✅ | ✅ |
| Actions | View · Download · Sign Off · Reject | — | — |

### 4.1 Filters

| Filter | Type |
|---|---|
| FY | Select |
| Branch | Multi-select |
| Report Type | Multi-select |
| Sign-off Status | Multi-select |

### 4.2 Search
- Report title · Branch name · 300ms debounce

### 4.3 Pagination
- Server-side · 20 rows/page

---

## 5. Drawers

### 5.1 Drawer: `report-upload` — Upload Audit Report
- **Trigger:** [+ Upload Report]
- **Width:** 600px

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | ✅ | |
| Report Type | Select | ✅ | |
| Period / Quarter | Select | ✅ | |
| Financial Year | Select | ✅ | |
| Report Title | Text | ✅ | Max 200 chars |
| File | File upload | ✅ | PDF/Excel max 50MB |
| Total Findings | Number | ❌ | |
| Summary | Textarea | ❌ | |

- [Cancel] [Upload Report]

### 5.2 Drawer: `report-view` — View Report
- **Trigger:** View action
- **Width:** 800px

**Sections:**
- Report metadata (Branch · Type · Period · Uploaded By · Date)
- Embedded PDF viewer (or download link)
- Findings summary table
- Management response section (editable by Finance Manager)
- Sign-off history

**Actions:**
- [Download PDF]
- [Sign Off] (Finance Manager only)
- [Reject — Request Revision] (Finance Manager only)

---

## 6. Charts

### 6.1 Reports by Type (Donut)
- **Segments:** Internal Quarterly · Statutory · CBSE · Special

### 6.2 Sign-off Status by Branch (Bar)
- **Data:** Pending vs Signed Off per branch

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Report uploaded | "Audit report uploaded for [Branch] — [Period]." | Success | 4s |
| Report signed off | "Report signed off for [Branch]." | Success | 3s |
| Report rejected | "Report rejected. Auditor notified to revise." | Warning | 4s |
| Download | "Report download started." | Info | 2s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No reports | "No audit reports" | "No audit reports uploaded for this period." | [+ Upload Report] |
| All signed off | "All reports signed off" | "All audit reports are reviewed and signed off." | — |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table |
| Upload drawer | Spinner + form skeleton |
| View drawer | Spinner + PDF loader |

---

## 10. Role-Based UI Visibility

| Element | Finance Mgr G1 | Internal Auditor G1 | CFO G1 |
|---|---|---|---|
| [+ Upload Report] | ❌ | ✅ | ❌ |
| [Sign Off] | ✅ | ❌ | ❌ |
| [Reject] | ✅ | ❌ | ❌ |
| View all reports | ✅ | ✅ | ✅ |
| Download | ✅ | ✅ | ✅ |
| Export list | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/audit-reports/` | JWT (G1+) | Report list |
| POST | `/api/v1/group/{id}/finance/audit-reports/` | JWT (G1, Auditor) | Upload report |
| GET | `/api/v1/group/{id}/finance/audit-reports/{rid}/` | JWT (G1+) | Report detail |
| POST | `/api/v1/group/{id}/finance/audit-reports/{rid}/sign-off/` | JWT (G1, Finance Mgr) | Sign off |
| POST | `/api/v1/group/{id}/finance/audit-reports/{rid}/reject/` | JWT (G1, Finance Mgr) | Reject |
| GET | `/api/v1/group/{id}/finance/audit-reports/{rid}/download/` | JWT (G1+) | Download |
| GET | `/api/v1/group/{id}/finance/audit-reports/export/` | JWT (G1+) | Export list |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../audit-reports/?q=` | `#reports-table-body` | `innerHTML` |
| Filter | `change` | GET `.../audit-reports/?type=&status=` | `#reports-section` | `innerHTML` |
| Upload drawer | `click` | GET `.../audit-reports/upload-form/` | `#drawer-body` | `innerHTML` |
| View drawer | `click` | GET `.../audit-reports/{id}/` | `#drawer-body` | `innerHTML` |
| Sign off | `click` | POST `.../audit-reports/{id}/sign-off/` | `#report-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
