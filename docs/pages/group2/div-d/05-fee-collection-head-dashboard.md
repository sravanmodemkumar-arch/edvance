# 05 — Group Fee Collection Head Dashboard

- **URL:** `/group/finance/collection/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Fee Collection Head (Role 34, G3)

---

## 1. Purpose

The Fee Collection Head Dashboard is the primary control panel for tracking fee collection performance across all branches. The Group Fee Collection Head (G3) is responsible for cross-branch defaulter management, waiver approvals, and collection drives. This is a high-stakes role: uncollected fees directly impact group cash flow and branch operations.

The dashboard surfaces real-time collection rates by branch, the total outstanding dues pipeline, all pending waiver requests submitted by branches, and active collection drives. The Fee Collection Head has authority to approve or reject waiver requests and can initiate group-wide collection drives targeted at specific student segments (e.g., Term 2 defaulters across all branches).

Unlike the CFO who views financial health strategically, this role acts on it — reaching out to branch fee managers, approving concessions, and escalating chronic defaulters.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Fee Collection Head | G3 | Full read + approve waivers + initiate drives | Primary owner |
| Group CFO | G1 | Read — all sections | Cannot approve waivers |
| Group Finance Manager | G1 | Read — all sections | Cannot approve waivers |
| Group Fee Structure Manager | G3 | Read — collection stats only | No waiver access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Collection Head Dashboard
```

### 3.2 Page Header
- **Title:** `Fee Collection Head Dashboard`
- **Subtitle:** `Cross-Branch Collection · AY [Year] · Term [N]`
- **Role Badge:** `Group Fee Collection Head`
- **Right-side controls:** `[AY ▾]` `[Term ▾]` `[+ New Collection Drive]` `[Export ↓]`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Total outstanding > 10% of annual demand | "Outstanding dues at [X]% of annual demand. Immediate collection action required." | Red |
| Waiver requests pending > 48 hours | "[N] fee waiver requests pending approval for more than 48 hours." | Amber |
| Branch collection rate < 70% | "[N] branches have collection rate below 70%." | Red |
| Term fee deadline within 7 days | "Term [N] fee deadline on [Date]. [X] students yet to pay." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Collected (Term) | ₹ | Informational | → Page 28 |
| Collection Rate % | Collected/Demand | Green ≥ 90% · Amber 75–89% · Red < 75% | → Page 28 |
| Total Defaulters | Count cross-branch | Red if > 0 | → Page 29 |
| Waiver Requests Pending | Count | Amber if > 0 · Red if > 10 | → Page 30 |
| Outstanding Dues | ₹ | Red if > 5% demand | → Page 31 |
| Active Collection Drives | Count | Informational | → Page 33 |

---

## 5. Section 5.1 — Branch Collection Status Table

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Fee Demand (Term) | ₹ | ✅ |
| Collected | ₹ | ✅ |
| Outstanding | ₹ | ✅ |
| Collection % | % badge | ✅ |
| Defaulters | Count | ✅ |
| Waiver Requests | Count | ✅ |
| Actions | View · Send Reminder | — |

**Filters:** Branch · Term · Collection % range
**Search:** Branch name · 300ms debounce
**Pagination:** 20 rows/page

---

## 5.2 Section 5.2 — Pending Waiver Requests

| Column | Type | Sortable |
|---|---|---|
| Student Name | Text | ✅ |
| Branch | Text | ✅ |
| Class | Text | ✅ |
| Waiver Type | Badge: Full · Partial · Scholarship | ✅ |
| Fee Amount | ₹ | ✅ |
| Waiver Requested | ₹ | ✅ |
| Reason | Text | — |
| Submitted By | Text | ✅ |
| Submitted Date | Date | ✅ |
| Actions | Review · Approve · Reject | — |

**[View All Waivers →]** links to Page 30.

---

## 5.3 Section 5.3 — Active Collection Drives

| Column | Type | Notes |
|---|---|---|
| Drive Name | Text | |
| Target | Badge: All · Day Scholar · Hosteler · Stream | |
| Branches | Count | |
| Target Amount | ₹ | |
| Collected So Far | ₹ | |
| Deadline | Date | |
| Status | Badge: Active · Completed · Overdue | |

**[Manage Drives →]** links to Page 33.

---

## 6. Charts

### 6.1 Collection Rate by Branch (Bar)
- **Y-axis:** Collection %
- **Colour:** Green ≥ 90% · Amber 75–89% · Red < 75%
- **Export:** PNG

### 6.2 Outstanding Dues Trend (Line)
- **X-axis:** Months of AY
- **Y-axis:** ₹ outstanding
- **Series:** Current AY vs Previous AY

### 6.3 Waiver Volume by Branch (Bar)
- **Data:** Waiver count and ₹ value per branch

---

## 7. Drawers

### 7.1 Drawer: `waiver-review` — Review Waiver Request
- **Trigger:** Review action in waiver table
- **Width:** 640px

| Field | Value |
|---|---|
| Student Name | [Name] |
| Class / Stream | [Class] — [Stream] |
| Branch | [Branch] |
| Fee Demand | ₹[X] |
| Already Paid | ₹[Y] |
| Outstanding | ₹[Z] |
| Waiver Requested | ₹[W] (Full / Partial) |
| Reason | [Text] |
| Supporting Documents | [File links] |
| Recommended By | [Branch Fee Manager Name] |

**Actions:**
- [Approve] — opens amount confirmation (for partial: enter approved amount)
- [Reject] — requires rejection reason text field
- [Request More Info] — message sent back to branch

**Approval form fields:**
| Field | Type | Required | Validation |
|---|---|---|---|
| Approved Waiver Amount | Number | ✅ | ≤ Outstanding amount |
| Approval Note | Textarea | ✅ | Min 20 chars |
| Internal Reference | Text | ❌ | |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Waiver approved | "Waiver of ₹[X] approved for [Student]. Branch notified." | Success | 4s |
| Waiver rejected | "Waiver rejected for [Student]. Branch notified with reason." | Warning | 4s |
| Reminder sent | "Fee reminder sent to [N] students in [Branch]." | Info | 3s |
| Drive created | "Collection drive '[Name]' launched for [N] branches." | Success | 4s |
| Export | "Collection report exported." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No waiver requests | "No pending waivers" | "No fee waiver requests from any branch." | — |
| All branches ≥ 90% | "Collection on track" | "All branches have collection rate ≥ 90%." | — |
| No active drives | "No active drives" | "Create a collection drive to push outstanding dues." | [+ New Collection Drive] |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton KPIs + 3 section skeletons |
| Term switch | Table skeleton |
| Waiver drawer | Spinner + skeleton fields |
| Approve action | Spinner on approve button |

---

## 11. Role-Based UI Visibility

| Element | Collection Head G3 | CFO G1 | Finance Mgr G1 |
|---|---|---|---|
| [+ New Collection Drive] | ✅ | ❌ | ❌ |
| [Approve] waiver | ✅ | ❌ | ❌ |
| [Reject] waiver | ✅ | ❌ | ❌ |
| [Send Reminder] | ✅ | ❌ | ❌ |
| View all sections | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/collection/kpis/` | JWT (G1+) | KPI cards |
| GET | `/api/v1/group/{id}/finance/collection/branch-status/` | JWT (G1+) | Branch collection table |
| GET | `/api/v1/group/{id}/finance/collection/waivers/?status=pending` | JWT (G1+) | Pending waiver requests |
| GET | `/api/v1/group/{id}/finance/collection/waivers/{wid}/` | JWT (G1+) | Waiver detail |
| PUT | `/api/v1/group/{id}/finance/collection/waivers/{wid}/approve/` | JWT (G3) | Approve waiver |
| PUT | `/api/v1/group/{id}/finance/collection/waivers/{wid}/reject/` | JWT (G3) | Reject waiver |
| GET | `/api/v1/group/{id}/finance/collection/drives/` | JWT (G1+) | Active drives list |
| POST | `/api/v1/group/{id}/finance/collection/drives/` | JWT (G3) | Create drive |
| POST | `/api/v1/group/{id}/finance/collection/send-reminder/` | JWT (G3) | Bulk reminder |
| GET | `/api/v1/group/{id}/finance/collection/export/` | JWT (G1+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Term switch | `change` | GET `.../branch-status/?term=` | `#collection-table` | `innerHTML` |
| Search | `input delay:300ms` | GET `.../branch-status/?q=` | `#collection-table-body` | `innerHTML` |
| Waiver review drawer | `click` | GET `.../waivers/{id}/` | `#drawer-body` | `innerHTML` |
| Approve | `click` | PUT `.../waivers/{id}/approve/` | `#waiver-row-{id}` | `outerHTML` |
| Reject | `click` | PUT `.../waivers/{id}/reject/` | `#waiver-row-{id}` | `outerHTML` |
| Pagination | `click` | GET `.../branch-status/?page=` | `#collection-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
