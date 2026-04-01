# 33 — Data Subject Request Manager

- **URL:** `/group/it/privacy/dsr/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Data Privacy Officer (Role 55, G1) — Read-only; Group IT Admin (Role 54, G4) — Full access

---

## 1. Purpose

The Data Subject Request (DSR) Manager handles all formal requests made by individuals (students, parents, staff) exercising their rights under the DPDP Act 2023. The Act grants every data subject four core rights with respect to their personal data held by EduForge:

**Right to Access** — the data subject may request a copy of all personal data EduForge holds about them, the purposes for which it is processed, and whom it has been shared with.

**Right to Correction** — the data subject may request correction of inaccurate or incomplete personal data.

**Right to Erasure ("Right to Be Forgotten")** — the data subject may request deletion of their personal data, subject to the group's legal obligation to retain certain records (academic results, payroll records, BGV records must be retained for statutory periods even after erasure request — these must be explained in the response).

**Right to Data Portability** — the data subject may request their data in a machine-readable format for portability to another service.

All DSRs must be logged here from the moment of receipt. The IT Admin assigns each request to a handler (typically a branch-level data admin or the IT Admin themselves), tracks progress, and must resolve or formally reject within 30 days. The Data Privacy Officer monitors the register to ensure no DSR is overdue and that rejections have valid legal grounds. DSRs overdue beyond 30 days constitute a legal violation under DPDP Act and are immediately escalated.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Data Privacy Officer | G1 | Read-only — all DSR records visible | Monitors compliance; cannot modify records |
| Group IT Admin | G4 | Full access — create, assign, process, resolve, reject | Operational management |
| Group IT Director | G4 | Read-only | Oversight for escalated or sensitive DSRs |
| All other Division F roles | — | Hidden | No access |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Data Privacy → Data Subject Requests
```

### 3.2 Page Header
- **Title:** `Data Subject Request Manager`
- **Subtitle:** `DPDP Act 2023 — Rights Requests Register · [N] Open · [N] Overdue`
- **Role Badge:** `Group Data Privacy Officer` or `Group IT Admin`
- **Right-side controls (IT Admin only):** `+ Log New DSR` · `Export`

### 3.3 Alert Banner (conditional — non-dismissible for legal obligations)

| Condition | Banner | Severity |
|---|---|---|
| DSRs overdue >30 days | "[N] Data Subject Request(s) are OVERDUE beyond the 30-day resolution deadline. This constitutes a breach of DPDP Act 2023. Immediate action required." | Red (non-dismissible) |
| New DSR pending assignment >24h | "[N] DSR(s) logged but not yet assigned to a handler for more than 24 hours. Assign immediately to avoid risk of deadline breach." | Amber |
| Erasure request involving minor student | "Erasure DSR #[N] involves a minor data subject. Review carefully — academic records must be retained per RTE Act. Ensure response addresses retention obligations." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open DSRs | Total count of DSRs with status Open or In Progress | Red if > 0, Amber if only low types open | Filter by Open/In Progress |
| Overdue (>30 Days) | DSRs where submitted_date + 30 days < today and status ≠ Resolved/Rejected | Red if > 0, Green if 0 | Filter by Overdue |
| Resolved This Month | DSRs with status = Resolved and resolution date in current calendar month | Green | Filter by Resolved + current month |
| Avg Resolution Time (Days) | Average number of days from submission to resolution (last 90 days) | Green ≤15d, Amber 15–25d, Red >25d | Informational |

---

## 5. Main Table — Data Subject Requests

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Request # | Auto-generated (e.g., DSR-00047) | No | No |
| Data Subject Type | Badge (Student / Parent / Staff) | Yes | Yes (multi-select) |
| Branch | Branch name | Yes | Yes (multi-select) |
| Request Type | Badge (Access / Correction / Erasure / Portability) | Yes | Yes (multi-select) |
| Submitted Date | Date | Yes | Yes (date range) |
| Due Date | Date (submitted + 30 days) — red if overdue | Yes | No |
| Status | Badge (Open / In Progress / Resolved / Rejected) | Yes | Yes (multi-select) |
| Assigned To | Staff name or "Unassigned" | Yes | No |
| Actions | View / Assign / Resolve / Reject | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All configured branches |
| Request Type | Multi-select checkbox | Access / Correction / Erasure / Portability |
| Status | Multi-select checkbox | Open / In Progress / Resolved / Rejected |
| Data Subject Type | Multi-select checkbox | Student / Parent / Staff |
| Submitted Date | Date range picker | Any range |
| Overdue Only | Toggle | Show only overdue DSRs |

### 5.2 Search
- Request # search
- 300ms debounce

### 5.3 Pagination
- Server-side · 25 rows/page

### 5.4 Default Sort
- Overdue DSRs first (due_date < today, status ≠ Resolved/Rejected), then Open by submitted date ascending (oldest first)

---

## 6. Drawers

### 6.1 Drawer: `dsr-view` — View DSR Detail
- **Trigger:** Actions → View
- **Width:** 720px
- **Content (read-only for DPO; read + process for IT Admin):**
  - Request number, submitted date, due date, days remaining (or overdue by N days — red)
  - Data subject type (masked — no full name or contact)
  - Branch
  - Request type with description label
  - Request description (the actual text of the request from the data subject)
  - Documents submitted by data subject (if any — identity verification etc.): file list with download links
  - Current status and assigned handler
  - Action history timeline (each status change: who changed, when, what action, notes)

### 6.2 Drawer: `dsr-process` — Assign / Process DSR (IT Admin only)
- **Trigger:** Actions → Assign or Resolve
- **Width:** 560px
- **Sections:**
  - **Assign Handler:**
    - Handler (dropdown — staff members who can handle DSRs)
    - Assignment notes (optional)
    - Status → changes to In Progress on assignment
  - **Record Action Taken:**
    - Action Taken (dropdown: Data Provided / Data Corrected / Data Partially Deleted / Data Deleted / Portability Export Sent / No Action — Retention Exemption)
    - Response sent to data subject (checkbox + date)
    - Resolution notes (required, textarea — explain what was done and why; this is the legal record)
    - Attachments (optional — upload response letter or data export receipt to Cloudflare R2)
  - **Mark Resolved:** Button — sets status to Resolved and records resolution timestamp
  - All fields required to resolve

### 6.3 Drawer: `dsr-reject` — Reject DSR (IT Admin only)
- **Trigger:** Actions → Reject
- **Width:** 480px
- **Important:** Rejection must have valid legal grounds. Valid reasons enumerated:
  - Identity of data subject could not be verified
  - Request is manifestly unfounded or excessive (repeated identical requests)
  - Erasure not possible due to legal obligation to retain (must specify statute)
  - Request relates to data processed for national security or law enforcement purposes
  - Other (requires written explanation — must be detailed)
- **Fields:**
  - Rejection Reason (required, dropdown: select from valid reasons above)
  - Detailed Explanation (required, textarea — min 100 characters)
  - Response sent to data subject (checkbox + date — required)
  - Confirm: "I confirm this rejection is based on valid legal grounds and a response has been sent to the data subject."
- On confirm: Status → Rejected; DPO notified; rejection reason logged

### 6.4 Drawer: `dsr-create` — Log New DSR (IT Admin only)
- **Trigger:** `+ Log New DSR` button
- **Width:** 560px
- **Fields:**
  - Data Subject Type (required, dropdown: Student / Parent / Staff)
  - Branch (required, dropdown)
  - Subject Reference (internal ID — for linking to subject record; masked from DPO)
  - Request Type (required, dropdown: Access / Correction / Erasure / Portability)
  - Submitted Date (required, date picker — date request was received)
  - Request Description (required, textarea — verbatim or summarised description of what the data subject is requesting)
  - Received Via (dropdown: Portal Form / Email / Post / In Person)
  - Identity Verification Status (dropdown: Verified / Pending Verification)
  - Document Upload (optional — copy of original request or identity documents)
- On submit: DSR-[N] ID generated; IT Director and DPO notified; 30-day clock starts from submitted date

---

## 7. Charts

No standalone charts on this page. Trend data is visible on the Compliance Dashboard (page 31).

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| DSR logged | "DSR #[N] logged. 30-day resolution clock starts from [submitted date]." | Success | 5s |
| DSR assigned | "DSR #[N] assigned to [Handler Name]." | Success | 3s |
| DSR resolved | "DSR #[N] marked Resolved. Data Privacy Officer notified." | Success | 4s |
| DSR rejected | "DSR #[N] rejected. Reason logged. Data Privacy Officer notified." | Warning | 5s |
| Overdue alert | "DSR #[N] is now overdue. Immediate action required." | Error | 8s |
| Export triggered | "DSR register export is being prepared." | Info | 3s |
| DSR assignment failed | Error: `Failed to assign DSR #[N]. Verify handler role permissions.` | Error | 5s |
| DSR resolution failed | Error: `Failed to resolve DSR #[N]. Ensure all required fields are completed.` | Error | 5s |

---

**Audit Trail:** All DSR state transitions (create, assign, process, complete, reject) are logged to the IT Audit Log with actor user ID, timestamp, DSR ID, and previous/new status.

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No DSRs | "No Data Subject Requests" | "No DSRs have been logged. When data subjects exercise their DPDP Act rights, requests are logged here." | + Log New DSR |
| No open DSRs | "All DSRs Resolved" | "All logged Data Subject Requests have been resolved or rejected." | — |
| No results for filter | "No Matching DSRs" | "No DSRs match the selected filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 4 KPI shimmer cards + table skeleton (15 rows) |
| Filter / search | Table skeleton shimmer |
| View DSR drawer | Drawer spinner; action history timeline lazy-loads |
| Process / assign submit | Button spinner |
| Reject submit | Button spinner: "Recording rejection…" |
| Create DSR submit | Button spinner |
| Export | Button spinner: "Preparing export…" |

---

## 11. Role-Based UI Visibility

| Element | Data Privacy Officer (G1) | IT Admin (G4) | IT Director (G4) |
|---|---|---|---|
| + Log New DSR | Hidden | Visible | Hidden |
| Assign Action | Hidden | Visible | Hidden |
| Resolve Action | Hidden | Visible | Hidden |
| Reject Action | Hidden | Visible | Hidden |
| View Action | Visible | Visible | Visible |
| Subject reference in view drawer | Hidden (type only) | Visible | Hidden |
| Resolution notes | Visible (read-only) | Visible (editable) | Visible (read-only) |
| Rejection reason + explanation | Visible (read-only) | Visible (editable) | Visible (read-only) |
| Export | Hidden | Visible | Visible |
| Action history timeline | Visible | Visible | Visible |
| Document uploads/downloads | Visible (download) | Visible (upload + download) | Visible (download) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/privacy/dsr/` | JWT (G1+) | Paginated DSR list |
| POST | `/api/v1/it/privacy/dsr/` | JWT (G4 — IT Admin) | Log new DSR |
| GET | `/api/v1/it/privacy/dsr/{id}/` | JWT (G1+) | Full DSR detail + action history |
| POST | `/api/v1/it/privacy/dsr/{id}/assign/` | JWT (G4 — IT Admin) | Assign DSR to handler |
| POST | `/api/v1/it/privacy/dsr/{id}/resolve/` | JWT (G4 — IT Admin) | Resolve DSR with action details |
| POST | `/api/v1/it/privacy/dsr/{id}/reject/` | JWT (G4 — IT Admin) | Reject DSR with legal grounds |
| GET | `/api/v1/it/privacy/dsr/kpis/` | JWT (G1+) | KPI card values |
| GET | `/api/v1/it/privacy/dsr/export/` | JWT (G4 — IT Admin / IT Director) | Export DSR register |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/privacy/dsr/kpis/` | `#kpi-bar` | `innerHTML` |
| Load DSR table | `load` | GET `/api/v1/it/privacy/dsr/` | `#dsr-table` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/privacy/dsr/?type=...&status=...` | `#dsr-table` | `innerHTML` |
| Overdue toggle | `change` on overdue toggle | GET `/api/v1/it/privacy/dsr/?overdue=true` | `#dsr-table` | `innerHTML` |
| Search DSR # | `input` (300ms debounce) | GET `/api/v1/it/privacy/dsr/?q=...` | `#dsr-table` | `innerHTML` |
| Open view drawer | `click` on View | GET `/api/v1/it/privacy/dsr/{id}/` | `#dsr-drawer` | `innerHTML` |
| Submit assign | `click` on Assign | POST `/api/v1/it/privacy/dsr/{id}/assign/` | `#dsr-drawer` | `innerHTML` |
| Submit resolve | `click` on Mark Resolved | POST `/api/v1/it/privacy/dsr/{id}/resolve/` | `#dsr-table` | `innerHTML` |
| Submit reject | `click` on Confirm Reject | POST `/api/v1/it/privacy/dsr/{id}/reject/` | `#dsr-table` | `innerHTML` |
| Submit new DSR | `click` on Submit | POST `/api/v1/it/privacy/dsr/` | `#dsr-table` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/privacy/dsr/?page=N` | `#dsr-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
