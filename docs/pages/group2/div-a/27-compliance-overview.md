# 27 — Compliance Overview

> **URL:** `/group/gov/compliance/`
> **File:** `27-compliance-overview.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 · CEO G4 · President G4 (Academic) · VP G4 (Ops) · Trustee G1 · Advisor G1 (read)

---

## 1. Purpose

Cross-branch, cross-area compliance status dashboard. Shows the group's compliance health
across all regulatory and institutional obligations: board affiliations, POCSO training,
BGV completion, fire safety, data privacy (DPDP Act), RTE quota, and more.

For each compliance area, per-branch status is tracked. Action items with deadlines and
owners can be created for non-compliant branches, ensuring accountability.

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| Chairman | Full — view all, create actions, approve | |
| MD | Full | |
| CEO | Full | |
| President | Academic areas only (affiliation, POCSO, RTE) | |
| VP | Ops areas only (fire safety, transport safety) | |
| Trustee | Read-only — all areas | |
| Advisor | Read-only — all areas | |
| Exec Secretary | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Compliance Overview
```

### 3.2 Page Header
```
Compliance Overview                                    [+ Add Action]  [Export Report ↓]
Overall Score: 87/100 · [N] areas non-compliant · [N] actions overdue
```

### 3.3 Compliance Score Card (prominent)
- Large number: "87 / 100"
- Trend: ↑2 points vs last quarter
- Colour: Green ≥90 · Yellow 70–89 · Red <70
- Breakdown: "X areas compliant · Y areas partial · Z areas non-compliant"

---

## 4. Compliance Areas Matrix

> Main content — one row per compliance area, columns per branch (or aggregated).

### 4.1 View Toggle
- **Summary View** (default): One row per area, aggregated status across all branches
- **Detailed View**: One row per area per branch — shows exact per-branch status

### 4.2 Summary View Table

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Compliance Area | Text | ✅ | |
| Category | Badge | ✅ | Legal · Safety · Academic · HR · IT |
| Overall Status | Badge | ✅ | ✅ Compliant · ⚠ Partial · ❌ Non-Compliant |
| Compliant Branches | Progress `42/50` | ✅ | |
| % Compliant | Number + bar | ✅ | |
| Last Checked | Date | ✅ | |
| Renewal Due | Date | ✅ | Red if <60 days |
| Open Actions | Number | ✅ | Linked to action tracker |
| Responsible Division | Badge | ❌ | A, D, E, F, K, etc. |
| Actions | — | ❌ | View Details · Add Action |

**Default sort:** % Compliant ascending (worst first).

**Compliance areas tracked:**

| Area | Renewal? | Division |
|---|---|---|
| CBSE / BSEAP Affiliation | Annual | Group HQ / Branch |
| State Board Compliance | Annual | Group HQ |
| POCSO Mandatory Training | Annual | E — HR |
| BGV Completion — Teaching Staff | Annual | E — HR |
| BGV Completion — Non-Teaching | Annual | E — HR |
| Fire Safety NOC | Annual | Operations |
| Health & Sanitation Certificate | Annual | Health |
| RTE Quota Compliance | Academic Year | Academic |
| DPDP Act Compliance | Ongoing | F — IT |
| Transport Safety Certificate | Annual | Transport |
| Anti-Ragging Committee | Annual | K — Welfare |
| Child Protection Policy | Annual | K — Welfare |
| Insurance (Student Accident) | Annual | Health |

### 4.3 Detailed View Table (per branch per area)

Switched via view toggle. Shows one row per compliance area per branch.

**Columns:** Area · Branch · Status · Last Checked · Evidence · Renewal Due · Action Owner · Actions.

**Search + Filter available in detailed view.**

---

## 5. Action Tracker Section

> Actions created for non-compliant branches — tracked with deadline and owner.

**Display:** Table (below compliance matrix).

**Search:** Branch name, area. Debounce 300ms.

**Filters:** Area · Branch · Status · Owner · Overdue only.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ID | Text | ✅ | ACT-2026-0023 |
| Area | Badge | ✅ | |
| Branch | Text | ✅ | |
| Action Description | Text (truncated) | ❌ | |
| Status | Badge | ✅ | Open · In Progress · Completed · Overdue |
| Owner | Text | ✅ | User assigned |
| Deadline | Date | ✅ | Red if past due |
| Evidence Required | Yes/No | ✅ | |
| Created By | Text | ❌ | |
| Actions | — | ❌ | View · Edit · Mark Complete · Delete |

**Default sort:** Deadline ascending (most urgent first).

**Pagination:** 25/page.

---

## 6. Drawers & Modals

### 6.1 Drawer: `compliance-detail` — Area Detail
- **Trigger:** Compliance area row → [View Details]
- **Width:** 640px
- **Tabs:** Status · Evidence · Actions · History

#### Tab: Status
- Per-branch status table: Branch · Status · Last Checked · Renewal Due · Notes
- Sortable — Status column (Non-Compliant first)
- [Mark Compliant] per row (Chairman/MD/CEO only) — requires evidence upload or reason

#### Tab: Evidence
- Table: Branch · Document Name · Uploaded By · Upload Date · Expiry Date · [View] [Delete]
- [+ Upload Evidence] button (role-permissioned)
- Expiry alerts: Red if expired, Yellow if <60 days

#### Tab: Actions
- Actions for this compliance area specifically (filtered view of main action tracker)
- [+ Add Action] button

#### Tab: History
- Compliance status history: Date · Status · Changed By · Notes
- Audit trail for each branch's compliance status changes

### 6.2 Drawer: `compliance-action` — Add/Edit Action
- **Trigger:** [+ Add Action] button or action table → [Edit]
- **Width:** 480px
- **Tabs:** Status · Evidence · Action Plan · Owner

#### Tab: Status
| Field | Type | Required | Validation |
|---|---|---|---|
| Compliance Area | Select | ✅ | From list |
| Branch | Multi-select | ✅ | At least 1 branch |
| Current Status | Select | ✅ | Non-Compliant · Partial |
| Non-Compliance Description | Textarea | ✅ | Min 30 chars |

#### Tab: Evidence
| Field | Type | Required | Validation |
|---|---|---|---|
| Evidence Required? | Toggle | ✅ | Default On |
| Evidence Type | Select | Conditional | Certificate · Report · Audit · Photograph · Other |
| Evidence Deadline | Date | Conditional | Required if evidence required |

#### Tab: Action Plan
| Field | Type | Required | Validation |
|---|---|---|---|
| Action Description | Textarea | ✅ | Min 50 chars |
| Steps to Complete | Textarea | ❌ | Numbered list |
| Deadline | Date | ✅ | Future date |
| Priority | Select | ✅ | High · Medium · Low |

#### Tab: Owner
| Field | Type | Required | Validation |
|---|---|---|---|
| Action Owner | Search + select | ✅ | Any platform user |
| Notify Owner | Toggle | ✅ | Default On — sends WhatsApp |
| Escalate To | Search + select | ❌ | If owner doesn't act by deadline |
| Reminder Days Before | Select | ❌ | 7 days · 3 days · 1 day |

**Submit:** "Create Action" — owner notified via WhatsApp.

### 6.3 Modal: `mark-compliant`
- **Width:** 480px
- **Fields:** Compliant as of (date) · Certificate/Evidence number (text) · Upload evidence (file, optional) · Notes
- **Buttons:** [Mark Compliant] + [Cancel]
- **On confirm:** Status updated · audit log entry · action (if any) marked complete

---

## 7. Charts

### 7.1 Compliance Score Trend (last 4 quarters)
- **Type:** Line chart
- **Data:** Composite compliance score (0–100) per quarter
- **Benchmark:** 90 target (dashed)
- **Export:** PNG

### 7.2 Compliance by Area (Bar)
- **Type:** Horizontal bar chart
- **Data:** % branches compliant per area
- **Sorted:** Ascending (worst area first)
- **Colour:** Green ≥90% · Yellow 70–90% · Red <70%
- **Export:** PNG

### 7.3 Renewal Calendar (next 6 months)
- **Type:** Gantt-style timeline
- **Data:** Compliance renewals due in next 6 months
- **Rows:** Areas, Columns: Months
- **Shows:** Renewal deadlines as markers
- **Colour:** Red = overdue · Orange = <30 days · Green = >30 days

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Branch marked compliant | "[Branch] marked compliant for [Area]" | Success | 4s |
| Action created | "Compliance action created. [Owner] notified." | Success | 4s |
| Action completed | "Action [ID] marked complete" | Success | 4s |
| Evidence uploaded | "Evidence uploaded for [Branch] — [Area]" | Success | 4s |
| Export started | "Compliance report generating…" | Info | 4s |
| Renewal reminder set | "Renewal reminder set for [N] days before [date]" | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| All compliant | "Excellent — full compliance" | "All branches are compliant across all areas" | — |
| No actions | "No open actions" | "All compliance issues have been resolved" | — |
| No actions (filtered) | "No actions match" | "Try different filters" | [Clear Filters] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: score card + compliance matrix (10 rows) |
| View toggle (Summary ↔ Detailed) | Matrix skeleton |
| Compliance detail drawer | Spinner in drawer |
| Action table filter | Inline skeleton rows |
| Mark Compliant | Spinner in button |

---

## 11. Role-Based UI Visibility

| Element | Chairman/MD/CEO | President | VP | Trustee/Advisor |
|---|---|---|---|---|
| All compliance areas | ✅ | Academic areas | Ops/Safety areas | ✅ read |
| [Mark Compliant] action | ✅ | ✅ (Academic) | ✅ (Ops) | ❌ |
| [+ Add Action] | ✅ | ✅ (Academic) | ✅ (Ops) | ❌ |
| [Upload Evidence] | ✅ | ✅ (Academic) | ✅ (Ops) | ❌ |
| [Export Report] | ✅ | ✅ | ✅ | ❌ |
| Action owner assignment | ✅ | ✅ | ✅ | ❌ |
| View evidence documents | ✅ | ✅ | ✅ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/compliance/` | JWT | Compliance overview summary |
| GET | `/api/v1/group/{id}/compliance/{area}/` | JWT | Area detail (per-branch) |
| POST | `/api/v1/group/{id}/compliance/{area}/{bid}/mark-compliant/` | JWT (G3+) | Mark branch compliant |
| POST | `/api/v1/group/{id}/compliance/{area}/{bid}/evidence/` | JWT (G3+) | Upload evidence |
| GET | `/api/v1/group/{id}/compliance/actions/` | JWT | Action tracker list |
| POST | `/api/v1/group/{id}/compliance/actions/` | JWT (G3+) | Create action |
| PUT | `/api/v1/group/{id}/compliance/actions/{aid}/` | JWT (G3+) | Update action |
| POST | `/api/v1/group/{id}/compliance/actions/{aid}/complete/` | JWT (G3+) | Mark complete |
| DELETE | `/api/v1/group/{id}/compliance/actions/{aid}/` | JWT (G5) | Delete action |
| GET | `/api/v1/group/{id}/compliance/charts/score-trend/` | JWT | Score trend chart |
| GET | `/api/v1/group/{id}/compliance/charts/by-area/` | JWT | By-area bar chart |
| GET | `/api/v1/group/{id}/compliance/export/` | JWT (G4/G5) | Export compliance report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| View toggle (Summary ↔ Detailed) | `click` | GET `.../compliance/?view=summary\|detailed` | `#compliance-matrix` | `innerHTML` |
| Sort column | `click` | GET `.../compliance/?sort=&dir=` | `#compliance-matrix` | `innerHTML` |
| Open compliance detail drawer | `click` | GET `.../compliance/{area}/` | `#drawer-body` | `innerHTML` |
| Open add-action drawer | `click` | GET `.../compliance/actions/new/` | `#drawer-body` | `innerHTML` |
| Action table search | `input delay:300ms` | GET `.../compliance/actions/?q=` | `#action-table-body` | `innerHTML` |
| Action table filter | `click` | GET `.../compliance/actions/?filters=` | `#action-table-section` | `innerHTML` |
| Action pagination | `click` | GET `.../compliance/actions/?page=` | `#action-table-section` | `innerHTML` |
| Mark compliant (modal confirm) | `click` | POST `.../compliance/{area}/{bid}/mark-compliant/` | `#compliance-row-{area}` | `outerHTML` |
| Upload evidence | `change` | POST `.../compliance/{area}/{bid}/evidence/` | `#evidence-upload-status` | `innerHTML` |
| Mark action complete | `click` | POST `.../compliance/actions/{aid}/complete/` | `#action-row-{aid}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
