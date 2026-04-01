# 32 — Staff Transfer Request Manager

- **URL:** `/group/hr/transfers/requests/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Staff Transfer Coordinator (Role 47, G3)

---

## 1. Purpose

The Staff Transfer Request Manager is the primary operational page for all inter-branch staff transfers within the group. The key governance principle enforced here is that no branch can unilaterally initiate or execute a staff transfer — all transfers are routed exclusively through Group HR. A branch principal can request a transfer, but the Transfer Coordinator and HR Director hold approval authority. This centralisation prevents one branch from depleting another's critical teaching staff.

Four transfer types are handled on this page. Administrative Transfers are initiated by Group HQ — the group decides to redeploy a staff member for operational reasons. Mutual Transfer Requests cover two staff members who have agreed to swap branches — both parties must consent and both source branches must be assessed for vacancy impact before approval. Hardship Transfers are staff-initiated on medical or family grounds — these carry a compassionate priority and must be reviewed within 5 working days. Emergency Transfers are triggered when a receiving branch has an acute, immediate staffing need — these must be resolved within 24 hours and override normal priority queuing.

Every transfer request triggers an automated Vacancy Impact Assessment: the system checks whether the departure of this staff member from the source branch will create a critical vacancy — i.e., will a subject or department at the source branch be left without qualified coverage? The result is a three-tier risk rating: Green (no critical impact), Amber (partial impact — one other qualified staff member remains), or Red (critical — sole qualified teacher for a subject/grade departing). A Red impact rating prevents approval without an explicit HR Director override and a documented replacement plan.

The Transfer Coordinator manages the queue from creation through to execution. Execution means the system updates the staff member's branch assignment in the EduForge database, notifies the staff member, notifies both branch principals, and updates all module access to reflect the new branch. This page is the control centre for that workflow.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Staff Transfer Coordinator | G3 | Full CRUD + Execute | Primary operator of this page |
| Group HR Director | G3 | Read + Approve / Decline | Acts on escalated requests |
| Group HR Manager | G3 | Read + Impact Review | Reviews vacancy assessment |
| Group Performance Review Officer | G1 | No Access | Not applicable |
| Branch Principal | Branch G3 | Submit request (own branch) | Cannot view cross-branch transfer queue |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > Staff Transfers > Transfer Request Manager`

### 3.2 Page Header
- **Title:** Staff Transfer Request Manager
- **Subtitle:** Manage all inter-branch staff transfer requests
- **Actions (top-right):**
  - `+ Create Transfer Request` (primary button)
  - `Export Transfer Log` (secondary button)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Emergency transfer requests pending for > 24 hours | "URGENT: [N] emergency transfer request(s) have been open for more than 24 hours. Immediate action required." | Red — non-dismissible |
| Red vacancy risk requests awaiting action | "WARNING: [N] transfer request(s) have Critical Vacancy Risk (Red). Replacement plan required before approval." | Amber — dismissible |
| Standard requests pending > 7 days | "REMINDER: [N] standard transfer requests have been pending for more than 7 working days." | Amber — dismissible |
| All requests resolved | "No pending transfer requests. All requests are resolved." | Green — auto-dismiss 10s |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Requests | Total open requests (all stages) | Blue if < 10, Amber if 10–20, Red if > 20 | No drill-down |
| Impact Assessment Pending | Requests awaiting vacancy impact review | Amber if > 0 | Filters table to this stage |
| Awaiting Approval | Requests escalated to HR Director | Amber if > 0 | Filters table to this stage |
| Approved (Pending Execution) | Approved but not yet executed in system | Blue if > 0 | Filters to this stage |
| Executed This Month | Transfers completed in current calendar month | Green | Filters to Executed this month |
| Requests Declined | Declined in current month | Red if > 0, Grey if 0 | Filters to Declined |

---

## 5. Main Table — Transfer Requests

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Request ID | Text (auto-generated, e.g., TRF-2026-001) | No | No |
| Staff Name | Text + avatar | Yes | No |
| From Branch | Badge | Yes | Yes — dropdown |
| To Branch | Badge | Yes | Yes — dropdown |
| Transfer Type | Badge (Admin / Mutual / Hardship / Emergency) | No | Yes — multi-select |
| Vacancy Risk | Traffic light badge (Green / Amber / Red) | No | Yes — dropdown |
| Requested Date | Date | Yes | Yes — date range |
| Days Open | Integer (auto-calculated) | Yes | Yes — range |
| Status | Badge (Draft / Impact Pending / Awaiting Approval / Approved / Executed / Declined) | No | Yes — multi-select |
| Actions | Icon buttons (View / Approve / Execute) | No | No |

### 5.1 Filters
- **Transfer Type:** Admin / Mutual / Hardship / Emergency / All
- **From Branch / To Branch:** multi-select dropdowns
- **Vacancy Risk:** Green / Amber / Red
- **Status:** multi-select
- **Requested Date Range:** date-picker
- **Days Open Range:** input

### 5.2 Search
Free-text search on Staff Name and Request ID. Debounced `hx-get` on keyup (400 ms).

### 5.3 Pagination
Server-side, 25 rows per page. Displays `Showing X–Y of Z requests`.

---

## 6. Drawers

### 6.1 Create Transfer Request
**Trigger:** `+ Create Transfer Request` button
**Fields:**
- Staff Member (searchable dropdown — searches staff directory)
- From Branch (auto-populated from staff record, editable)
- To Branch (dropdown, required)
- Transfer Type (radio: Administrative / Mutual / Hardship / Emergency)
- If Mutual: Second Staff Member (searchable, required)
- Reason / Justification (textarea, required)
- Requested Effective Date (date picker)
- Supporting Document Upload (for Hardship: medical/family document; for Emergency: receiving branch request letter)
- Urgency Override (checkbox — Emergency only — flags for 24-hour SLA)
- Submit Request button → triggers vacancy impact assessment

### 6.2 View Impact Assessment
**Trigger:** Eye icon or row click when Status = Impact Pending or later
**Displays:** Request details, Vacancy Impact Assessment result (Green/Amber/Red with explanation), subject/department coverage analysis at source branch, replacement plan field (required if Red — Transfer Coordinator must enter before escalating for approval), staff transfer history, current transfer SLA timer.

### 6.3 Approve / Decline (Transfer Coordinator view)
**Trigger:** Available when Coordinator has reviewed impact and replacement plan is documented
**Approve (for standard/hardship):** Escalates to HR Director queue (Transfer Coordinator cannot self-approve; Coordinator creates the request and HR Director approves).
**Decline (Transfer Coordinator):** Can decline at intake stage if request is clearly invalid; requires reason.

### 6.4 Execute Transfer
**Trigger:** Execute button — available only once HR Director has approved
**Confirmation Modal:** "This will update [Staff Name]'s branch from [From] to [To] effective [Date]. Staff will be notified. Both branch principals will be notified. Confirm?" Requires typed "CONFIRM" to proceed.

---

## 7. Charts

**Transfer Volume by Type (Donut Chart)**
- Segments: Administrative, Mutual, Hardship, Emergency
- Tooltip: count and % of total requests
- Date range selector to change reporting period

**Transfer Status Pipeline (Horizontal Funnel)**
- Stages: Created → Impact Assessed → Awaiting Approval → Approved → Executed
- Bar width = count at each stage
- Highlights Emergency requests in a separate red overlay bar

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Transfer request created | "Transfer request [ID] created. Vacancy impact assessment initiated." | Success | 4s |
| Impact assessment completed | "Vacancy impact assessment complete for [Staff Name]. Risk: [Green/Amber/Red]." | Info | 5s |
| Request escalated to HR Director | "Request [ID] submitted for HR Director approval." | Info | 4s |
| Transfer executed | "[Staff Name] has been transferred to [Branch]. All parties notified." | Success | 5s |
| Request declined | "Transfer request [ID] declined. Reason recorded." | Info | 4s |
| Error on execution | "Transfer execution failed. Please check system permissions and try again." | Error | 6s |

---

## 9. Empty States

- **No active requests:** "No transfer requests found. Click '+ Create Transfer Request' to begin."
- **No requests match filters:** "No requests match your filter criteria. Adjust filters to see results."
- **All requests resolved:** "All transfer requests have been resolved. No pending actions."

---

## 10. Loader States

- Table skeleton: 6 rows with animated shimmer.
- KPI cards: shimmer rectangles.
- Impact assessment drawer: spinner while vacancy analysis computes.
- Chart area: placeholder with "Loading chart…" text.

---

## 11. Role-Based UI Visibility

| Element | Transfer Coordinator (G3) | HR Director (G3) | HR Manager (G3) |
|---|---|---|---|
| Create Transfer Request button | Visible + enabled | Hidden | Hidden |
| View Impact Assessment | Visible | Visible | Visible |
| Approve / Decline (final) | Hidden | Visible + enabled | Hidden |
| Execute Transfer button | Visible + enabled (post-approval) | Hidden | Hidden |
| Export Transfer Log | Visible | Visible | Visible |
| Vacancy Risk column | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/transfers/requests/` | JWT G3 | List transfer requests (paginated) |
| POST | `/api/v1/hr/transfers/requests/` | JWT G3 Coordinator | Create transfer request |
| GET | `/api/v1/hr/transfers/requests/{id}/` | JWT G3 | View request details and impact assessment |
| PATCH | `/api/v1/hr/transfers/requests/{id}/` | JWT G3 Coordinator | Update request (pre-approval) |
| POST | `/api/v1/hr/transfers/requests/{id}/escalate/` | JWT G3 Coordinator | Escalate to HR Director for approval |
| POST | `/api/v1/hr/transfers/requests/{id}/decline/` | JWT G3 | Decline request with reason |
| POST | `/api/v1/hr/transfers/requests/{id}/execute/` | JWT G3 Coordinator | Execute approved transfer |
| GET | `/api/v1/hr/transfers/requests/kpis/` | JWT G3 | KPI summary bar data |
| GET | `/api/v1/hr/transfers/requests/charts/type/` | JWT G3 | Transfer type donut chart data |
| GET | `/api/v1/hr/transfers/requests/export/` | JWT G3 | Export transfer log |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search staff or request ID | keyup changed delay:400ms | GET `/api/v1/hr/transfers/requests/?q={val}` | `#transfers-table-body` | innerHTML |
| Filter change | change | GET `/api/v1/hr/transfers/requests/?{params}` | `#transfers-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/transfers/requests/?page={n}` | `#transfers-table-body` | innerHTML |
| Open create drawer | click | GET `/api/v1/hr/transfers/requests/new/` | `#drawer-container` | innerHTML |
| Open view drawer | click | GET `/api/v1/hr/transfers/requests/{id}/` | `#drawer-container` | innerHTML |
| Submit create form | submit | POST `/api/v1/hr/transfers/requests/` | `#transfers-table-body` | innerHTML |
| Refresh KPI bar after action | htmx:afterRequest | GET `/api/v1/hr/transfers/requests/kpis/` | `#kpi-bar` | innerHTML |
| Execute transfer confirm | click | POST `/api/v1/hr/transfers/requests/{id}/execute/` | `#transfers-table-body` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
