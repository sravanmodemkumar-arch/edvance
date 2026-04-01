# 74 — Group Timetable Standards

> **URL:** `/group/acad/timetable-standards/`
> **File:** `74-group-timetable-standards.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 (full) · Curriculum Coordinator G2 (edit standards) · Academic Director G3 (view + audit) · Stream Coordinators G3 (own stream)

---

## 1. Purpose

Defines and enforces group-wide minimum timetable standards: minimum number of periods per subject
per week per class and stream. Branches must build their timetables within these constraints.

The compliance audit feature allows branch timetables (uploaded as CSV or PDF) to be checked against
the group standards, generating a deviation report for non-compliant branches.

Without this page, each branch sets its own period allocation — leading to Mathematics getting only
3 periods/week in some branches while the group standard mandates 8, directly impacting results.

---

## 2. Role Access

| Role | Level | Can Define Standards | Can Run Audit | Can View | Notes |
|---|---|---|---|---|---|
| CAO | G4 | ✅ | ✅ | ✅ | Final approval on standards |
| Curriculum Coordinator | G2 | ✅ | ❌ | ✅ | Draft + edit standards |
| Academic Director | G3 | ❌ | ✅ | ✅ | Audit + monitor compliance |
| Stream Coord MPC | G3 | ❌ | ❌ | ✅ MPC only | |
| Stream Coord BiPC | G3 | ❌ | ❌ | ✅ BiPC only | |
| Stream Coord MEC/CEC | G3 | ❌ | ❌ | ✅ MEC/CEC only | |
| Stream Coord HEC | G3 | ❌ | ❌ | ✅ HEC only | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Group Timetable Standards
```

### 3.2 Page Header
```
Group Timetable Standards                      [+ Add Standard]  [Run Compliance Audit]  [Export ↓]
AY 2025–26 · [N] Standards Defined · [M] Branches Compliant · [P] Non-Compliant
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Standards Defined | 148 |
| Mandatory Standards | 92 |
| Branches Audited | 38 / 50 |
| Compliant Branches | 29 |
| Non-Compliant Branches | 9 |
| Most Violated Subject | Mathematics (12 branches) |

---

## 4. Standards Table

### 4.1 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Stream | Badge | ✅ | MPC / BiPC / MEC / CEC / HEC / Common |
| Class | Badge | ✅ | 6 / 7 / ... / 12 |
| Subject | Text | ✅ | |
| Min Periods/Week | Number | ✅ | Group-mandated minimum |
| Recommended | Number | ✅ | Suggested optimum |
| Mandatory | Badge | ✅ | Yes · No |
| Status | Badge | ✅ | Active · Draft · Archived |
| Effective From | Date | ✅ | |
| Actions | — | ❌ | Edit · Archive |

### 4.2 Filters

| Filter | Type | Options |
|---|---|---|
| Stream | Multi-select | MPC / BiPC / MEC / CEC / HEC / Common |
| Class | Multi-select | 6–12 |
| Subject | Multi-select | Subject names |
| Mandatory | Checkbox | Mandatory only |
| Status | Multi-select | Active · Draft · Archived |

### 4.3 Search
- Full-text: subject name
- 300ms debounce

---

## 5. Branch Compliance Table

Separate tab/section showing compliance status per branch:

| Column | Type | Notes |
|---|---|---|
| Branch | Text | |
| Last Audit | Date | Date of last timetable upload and audit |
| Standards Checked | Number | Total applicable standards |
| Compliant | Number | Passed |
| Non-Compliant | Number | Failed — red if > 0 |
| Compliance % | Progress bar | |
| Status | Badge | Fully Compliant · Partially Compliant · Non-Compliant · Not Audited |
| Actions | — | View Detail · Re-Audit |

---

## 6. Drawers

### 6.1 Drawer: `standard-edit` — Add / Edit Standard
- **Trigger:** [+ Add Standard] or Edit row
- **Width:** 480px

| Field | Type | Required | Validation |
|---|---|---|---|
| Stream | Select | ✅ | |
| Class | Select | ✅ | |
| Subject | Select/Text | ✅ | From Subject-Topic Master or custom |
| Min Periods/Week | Number | ✅ | 1–12 |
| Recommended Periods/Week | Number | ❌ | ≥ Min |
| Mandatory | Toggle | ✅ | |
| Effective From | Date | ✅ | |
| Notes | Text | ❌ | Rationale for this standard |

### 6.2 Drawer: `branch-compliance-detail` — Branch Audit Detail
- **Trigger:** View Detail row action in compliance table
- **Width:** 560px

**Content:**
- Branch name · Last audit date · Timetable file (download link)
- **Compliance table:** Subject · Min Required · Actual Periods · Status (✅ / ❌)
- **Deviations section:** Only non-compliant rows, with "Action Required" note
- **[Send Compliance Notice]** → sends formal notice to Branch Principal with deviation list

### 6.3 Modal: `audit-upload`
- **Trigger:** [Run Compliance Audit] header button
- **Width:** 480px
- **Content:** Select branches to audit · Upload timetable CSV/PDF per branch
- **Alternatively:** Request branch to upload via branch portal (sends notification)

---

## 7. Compliance Audit Process

1. CAO or Academic Director triggers audit for selected branches
2. Branch uploads timetable (CSV: Subject, Class, Day, Period slots)
3. System checks each subject-class combination against defined standards
4. Deviation report generated per branch:
   - ✅ Compliant: Actual periods ≥ Minimum standard
   - ❌ Non-Compliant: Actual periods < Minimum — deviation amount shown
5. Branch Principal notified of non-compliance with action-required notice
6. Follow-up: branch re-uploads corrected timetable → re-audit

---

## 8. Alert Logic

| Condition | Alert | Recipient |
|---|---|---|
| Branch has > 3 non-compliant subjects | In-app alert + notification | Academic Director |
| Branch not audited in 45 days | Reminder | Academic Director |
| Mandatory standard violated | Red flag on compliance row | Academic Director + CAO |

---

## 9. Charts

### 9.1 Compliance Rate by Branch (Bar)
- **Data:** Compliance % per branch (sorted ascending — worst first)
- **Color:** Green ≥ 90% · Amber 70–89% · Red < 70%
- **Export:** PNG

### 9.2 Most Violated Subjects (Bar)
- **Data:** Subjects with most non-compliance instances across all branches
- **Export:** PNG

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Standard added | "Standard added: [Subject] Class [N] — [M] periods/week." | Success | 4s |
| Standard updated | "Standard updated." | Success | 3s |
| Audit complete | "Audit complete for [N] branches. [M] non-compliant." | Info | 5s |
| Compliance notice sent | "Compliance notice sent to [Branch] Principal." | Success | 4s |
| Standard archived | "Standard archived." | Warning | 4s |

---

## 11. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No standards defined | "No timetable standards set" | "Define minimum periods per subject per week." | [+ Add Standard] |
| No audits run | "No branches audited" | "Run a compliance audit for any branch." | [Run Audit] |
| All compliant | "All branches compliant" | "All audited branches meet timetable standards." | — |

---

## 12. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: stats + standards table |
| Compliance table load | Skeleton rows |
| Audit run | Full-page overlay "Running timetable audit…" |
| Detail drawer | Spinner + skeleton |

---

## 13. Role-Based UI Visibility

| Element | CAO G4 | Curr Coord G2 | Academic Dir G3 | Stream Coords G3 |
|---|---|---|---|---|
| [+ Add Standard] | ✅ | ✅ | ❌ | ❌ |
| Edit standard | ✅ | ✅ | ❌ | ❌ |
| Archive standard | ✅ | ❌ | ❌ | ❌ |
| [Run Compliance Audit] | ✅ | ❌ | ✅ | ❌ |
| [Send Compliance Notice] | ✅ | ❌ | ✅ | ❌ |
| View standards | ✅ | ✅ | ✅ | ✅ (own stream) |
| Compliance table | ✅ | ❌ | ✅ | ✅ (own stream) |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/timetable-standards/` | JWT (G2+) | Standards list |
| POST | `/api/v1/group/{id}/acad/timetable-standards/` | JWT (G2+, G4 approve) | Add standard |
| PUT | `/api/v1/group/{id}/acad/timetable-standards/{sid}/` | JWT (G2+) | Edit standard |
| DELETE | `/api/v1/group/{id}/acad/timetable-standards/{sid}/` | JWT (G4) | Archive standard |
| GET | `/api/v1/group/{id}/acad/timetable-standards/compliance/` | JWT (G3+) | Branch compliance list |
| POST | `/api/v1/group/{id}/acad/timetable-standards/audit/` | JWT (G3+) | Run compliance audit |
| GET | `/api/v1/group/{id}/acad/timetable-standards/compliance/{bid}/` | JWT (G3+) | Branch audit detail |
| POST | `/api/v1/group/{id}/acad/timetable-standards/compliance/{bid}/notice/` | JWT (G3+) | Send compliance notice |
| GET | `/api/v1/group/{id}/acad/timetable-standards/stats/` | JWT (G2+) | Summary stats |
| GET | `/api/v1/group/{id}/acad/timetable-standards/export/?format=csv` | JWT (G2+) | Export standards |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Standards search | `input delay:300ms` | GET `.../timetable-standards/?q=` | `#standards-table-body` | `innerHTML` |
| Filter | `click` | GET `.../timetable-standards/?filters=` | `#standards-section` | `innerHTML` |
| Pagination | `click` | GET `.../timetable-standards/?page=` | `#standards-section` | `innerHTML` |
| Add/edit standard | `submit` | POST/PUT `.../timetable-standards/` | `#drawer-body` | `innerHTML` |
| Compliance tab load | `click` | GET `.../compliance/` | `#compliance-section` | `innerHTML` |
| Branch audit detail | `click` | GET `.../compliance/{bid}/` | `#drawer-body` | `innerHTML` |
| Run audit | `submit` | POST `.../audit/` | `#audit-modal-body` | `innerHTML` |
| Send notice | `click` | POST `.../notice/` | `#notice-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
