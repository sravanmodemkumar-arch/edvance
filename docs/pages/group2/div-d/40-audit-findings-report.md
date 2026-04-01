# 40 — Audit Findings Report

- **URL:** `/group/finance/audit/findings/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Internal Auditor G1 (primary) · Finance Manager G1

---

## 1. Purpose

The Audit Findings Report page is where the Internal Auditor records, tracks, and manages all findings raised during branch audits. A finding is a documented observation of a financial control gap, compliance failure, or irregularity — each with a severity rating, root cause, management response, and closure status.

The workflow: Auditor raises finding → Branch management reviews and provides response → Finance Manager signs off on response adequacy → Finding closed. Findings without management response after 30 days are automatically escalated.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Internal Auditor | G1 | Full CRUD on findings |
| Group Finance Manager | G1 | Read + sign off on management responses |
| Group CFO | G1 | Read — summary of open findings |
| Group Chairman | G5 | Read — critical findings only |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Internal Audit → Audit Findings
```

### 3.2 Page Header
- **Title:** `Audit Findings Report`
- **Subtitle:** `[N] Open Findings · [X] Critical · [Y] Closed (FY [Year])`
- **Right-side controls:** `[FY ▾]` `[Branch ▾]` `[Severity ▾]` `[Status ▾]` `[+ Raise Finding]` `[Export ↓]`

---

## 4. Main Table

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Finding ID | Text | ✅ | — |
| Branch | Text | ✅ | ✅ |
| Audit Period | Text | ✅ | — |
| Category | Badge: Fee · Procurement · Payroll · Assets · Compliance · IT | ✅ | ✅ |
| Severity | Badge: Critical · High · Medium · Low | ✅ | ✅ |
| Finding Summary | Text | — | — |
| Raised Date | Date | ✅ | — |
| Days Open | Number (red if >30) | ✅ | — |
| Management Response | Badge: Not Received · Received · Accepted | ✅ | ✅ |
| Status | Badge: Open · Under Review · Resolved · Closed | ✅ | ✅ |
| Actions | View · Close · Escalate | — | — |

### 4.1 Filters

| Filter | Type |
|---|---|
| Branch | Multi-select |
| Severity | Multi-select |
| Category | Multi-select |
| Status | Multi-select |
| Date Range | Date picker |
| Days Open | Range |

### 4.2 Search
- Finding ID · Summary text

### 4.3 Pagination
- 25 rows/page · Sort: Severity + Days Open (most critical, oldest first)

---

## 5. Drawers

### 5.1 Drawer: `finding-raise` — Raise New Finding
- **Trigger:** [+ Raise Finding]
- **Width:** 720px

| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | ✅ | |
| Linked Audit | Select | ✅ | From audit planner |
| Category | Select | ✅ | |
| Severity | Select | ✅ | Critical · High · Medium · Low |
| Finding Title | Text | ✅ | Max 200 chars |
| Detailed Description | Textarea | ✅ | Min 100 chars |
| Root Cause | Textarea | ✅ | |
| Evidence | File upload (multi) | ❌ | PDF/image |
| Recommended Action | Textarea | ✅ | |
| Response Deadline | Date | ✅ | Default: 14 days |
| Notify Branch Principal | Toggle | — | Default: ON |

- [Cancel] [Raise Finding]

### 5.2 Drawer: `finding-detail` — Finding Detail & Response
- **Trigger:** View action
- **Width:** 800px

**Tab: Finding Details**
- All fields from raise form

**Tab: Management Response**
- Response from Branch Management:
  - Response Date · Responded By
  - Acceptance: Accept · Partially Accept · Dispute
  - Response Note
  - Action Plan: What will be done + by when
  - [Accept Response] / [Reject Response] (Auditor)

**Tab: Audit Trail**
- Chronological log of all actions

**Tab: Evidence**
- Uploaded documents + auditor photos

**Actions:**
- [Send Reminder] — to branch management
- [Close Finding] — requires: closure date + closure note + Finance Manager sign-off
- [Escalate] — to CFO / Chairman

### 5.3 Drawer: `close-finding` — Close Finding
| Field | Type | Required |
|---|---|---|
| Closure Date | Date | ✅ |
| Closure Note | Textarea | ✅ |
| Closure Evidence | File | ❌ |
| Finance Manager Sign-off | Toggle (confirm) | ✅ |

---

## 6. Charts

### 6.1 Findings by Severity (Donut)
- **Segments:** Critical · High · Medium · Low

### 6.2 Findings Raised vs Closed (Bar — Monthly)
- **Series:** Raised (red) · Closed (green)

### 6.3 Open Findings by Branch (Bar)
- **Sort:** Desc

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Finding raised | "Finding [ID] raised for [Branch]. Branch notified." | Success | 4s |
| Finding closed | "Finding [ID] closed for [Branch]." | Success | 3s |
| Response accepted | "Management response accepted for Finding [ID]." | Info | 3s |
| Escalated | "Finding [ID] escalated to CFO." | Warning | 4s |
| Reminder sent | "Response reminder sent to [Branch] Principal." | Info | 3s |
| Export | "Findings report exported." | Info | 3s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No findings | "No audit findings" | "No findings raised for this period." | [+ Raise Finding] |
| All closed | "All findings resolved" | "All audit findings are closed." | — |

---

## 9. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton table + chart skeletons |
| Finding drawer | Spinner + skeleton tabs |
| Close action | Spinner |

---

## 10. Role-Based UI Visibility

| Element | Internal Auditor G1 | Finance Mgr G1 | CFO G1 |
|---|---|---|---|
| [+ Raise Finding] | ✅ | ❌ | ❌ |
| [Close Finding] | ✅ | ✅ (sign-off) | ❌ |
| [Escalate] | ✅ | ✅ | ❌ |
| [Accept Response] | ✅ | ❌ | ❌ |
| View all findings | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/audit/findings/` | JWT (G1+) | Findings list |
| POST | `/api/v1/group/{id}/finance/audit/findings/` | JWT (G1) | Raise finding |
| GET | `/api/v1/group/{id}/finance/audit/findings/{fid}/` | JWT (G1+) | Finding detail |
| PUT | `/api/v1/group/{id}/finance/audit/findings/{fid}/response/accept/` | JWT (G1) | Accept response |
| POST | `/api/v1/group/{id}/finance/audit/findings/{fid}/close/` | JWT (G1) | Close finding |
| POST | `/api/v1/group/{id}/finance/audit/findings/{fid}/escalate/` | JWT (G1) | Escalate |
| POST | `/api/v1/group/{id}/finance/audit/findings/{fid}/remind/` | JWT (G1) | Send reminder |
| GET | `/api/v1/group/{id}/finance/audit/findings/export/` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../findings/?q=` | `#findings-table-body` | `innerHTML` |
| Filter | `change` | GET `.../findings/?severity=&status=` | `#findings-section` | `innerHTML` |
| Raise drawer | `click` | GET `.../findings/raise-form/` | `#drawer-body` | `innerHTML` |
| Detail drawer | `click` | GET `.../findings/{id}/` | `#drawer-body` | `innerHTML` |
| Submit finding | `submit` | POST `.../findings/` | `#drawer-body` | `innerHTML` |
| Close | `click` | GET `.../findings/{id}/close-form/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
