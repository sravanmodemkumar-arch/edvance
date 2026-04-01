# 05 — VP Dashboard (Operations)

> **URL:** `/group/gov/vp/`
> **File:** `05-vp-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Vice President (Operations) (G4) — exclusive landing page

---

## 1. Purpose

Operations control centre for the Group VP. The VP manages day-to-day operational health
across all branches — escalation resolution, branch SLA compliance, procurement pipeline,
transport incidents, and infrastructure issues. The VP is the first responder for operational
escalations before they reach the CEO or Chairman.

Core VP responsibilities surfaced here:
- Manage operational escalations (Severity 2–4; Severity 1 escalated to CEO/Chairman)
- Monitor branch SLA compliance (response times, grievance closure rates)
- Approve/review procurement requests from branches
- Track transport and infrastructure status

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group VP (Operations) | G4 | Full — all sections, all actions | Exclusive dashboard |
| Chairman / MD | G5 | — | Own dashboards |
| CEO / President | G4 | — | Own dashboards |
| Trustee / Advisor | G1 | — | Own dashboards |
| Exec Secretary | G3 | — | Own dashboard |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  VP Dashboard (Operations)
```

### 3.2 Page Header
```
Operations — [VP Name]                                 [+ Log Escalation]  [Export Daily Report ↓]
Group Vice President (Operations) · Last login: [date time]
```

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Open Escalations | `7 open (2 critical)` | Red if any Sev-1/2 · Yellow if Sev-3 only | → Escalation Centre page 33 |
| Branch SLA Compliance | `91.2% compliant` | Green ≥95% · Yellow 85–95% · Red <85% | → Escalation Centre page 33 |
| Procurement Pending | `14 items` awaiting VP | Badge — red if >10 | → inline section |
| Transport Incidents (30d) | `2 incidents` | Green = 0 · Yellow = 1–2 · Red = 3+ | → inline section |
| Grievances Overdue | `3 overdue` | Red if >0 | → Compliance Overview page 27 |
| Infrastructure Tickets | `8 open` | Yellow if >5 · Red if >15 | → inline section |

---

## 5. Sections

### 5.1 Escalation Queue (VP-owned)

> Operational escalations assigned to VP or awaiting VP action.

**Search:** Escalation ID, branch name, title. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Type | Multi-select | Welfare · Financial · Academic Misconduct · Infrastructure · Safety · IT · Grievance |
| Severity | Multi-select | Sev 1 (Critical) · Sev 2 (High) · Sev 3 (Medium) · Sev 4 (Low) |
| Status | Multi-select | Open · Assigned · In Progress · Pending Info |
| SLA | Select | All · On Track · SLA Breached |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ID | Text | ✅ | e.g. ESC-2026-0042 |
| Branch | Text | ✅ | |
| Type | Badge | ✅ | |
| Severity | Badge | ✅ | 1=red · 2=orange · 3=yellow · 4=grey |
| Title | Text (truncated 60 chars) | ✅ | |
| Reported By | Text | ❌ | |
| Assigned To | Text | ✅ | Blank if unassigned |
| Age (hrs) | Number | ✅ | Red if SLA exceeded |
| SLA Status | Badge | ✅ | On Track · Warning · Breached |
| Status | Badge | ✅ | Open · In Progress · Pending Info |
| Actions | — | ❌ | View · Assign · Resolve · Escalate to CEO |

**Default sort:** Severity ascending (Sev 1 first), then Age descending.

**Pagination:** Server-side · Default 25/page.

**Row actions:**
| Action | Trigger | Notes |
|---|---|---|
| View | `escalation-detail` drawer | Full details + timeline |
| Assign | Inline select dropdown | Assign to self or another role |
| Resolve | `escalation-resolve` modal | Requires resolution notes (min 50 chars) |
| Escalate to CEO | Confirm modal | Only for Sev 1–2 — CEO notified |

---

### 5.2 Branch SLA Status Table

> Per-branch operational SLA compliance.

**Search:** Branch name. Debounce 300ms.

**Filters:** State, Type (Day/Hostel), SLA Status.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text + link | ✅ | → Branch Detail page 10 |
| City | Text | ✅ | |
| SLA Score | Number + bar | ✅ | 0–100, colour-coded |
| Open Issues | Number | ✅ | |
| Overdue | Number | ✅ | Red if >0 |
| Avg Resolution Time | Text | ✅ | "2.4 days" |
| Trend | Arrow | ✅ | ↑ improving · ↓ worsening |
| Last Incident | Date | ✅ | |
| Actions | — | ❌ | View Issues · Flag for Review |

**Default sort:** SLA Score ascending (worst first).

**Pagination:** 25/page.

---

### 5.3 Procurement Pipeline

> Branch procurement requests awaiting VP approval.

**Display:** Table — max 10 rows + "View All" link.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Request ID | Text | ✅ | |
| Branch | Text | ✅ | |
| Category | Badge | ✅ | Books · Uniforms · Lab Equipment · Furniture · IT |
| Item Description | Text (truncated) | ❌ | |
| Quantity | Number | ✅ | |
| Estimated Cost | Currency ₹ | ✅ | |
| Requested By | Text | ❌ | |
| Days Pending | Number | ✅ | Red if >7 |
| Actions | — | ❌ | [Approve] [Reject] [View Quote] |

**Approve:** Opens approval confirm modal — amount displayed prominently.

**Reject:** 400px modal — required reason (sent back to branch).

---

### 5.4 Transport Status Summary

> Fleet health and incident overview — large groups only.

**Display:** 3 stat cards + incident list.

| Card | Metric |
|---|---|
| Total Buses | Group-wide fleet count |
| Operational | Count + % operational |
| Incidents (30d) | Recent transport incidents |

**Incident list (last 5):**
Fields: Branch · Bus No · Type (Breakdown / Accident / Route Deviation) · Date · Status (Resolved/Open).

---

### 5.5 Infrastructure Tickets

> Open infrastructure issues across branches.

**Display:** Compact list — branch, issue type, reported date, status. Max 5, "View All" link.

**Issue types:** Electrical · Plumbing · Security Camera · Gate · Hostel Facility · Classroom.

---

## 6. Drawers & Modals

### 6.1 Drawer: `escalation-detail`
- **Width:** 680px
- **Tabs:** Overview · Timeline · Actions · Resolution
- **Overview tab:** All escalation details (branch, type, severity, description, evidence files)
- **Timeline tab:** Chronological log — who did what and when
- **Actions tab:** [Assign to self] [Assign to role] [Request info from branch] [Escalate to CEO] [Add note]
- **Resolution tab (shown when status = In Progress):** Resolution description (textarea, 500 chars, required) · Root cause category · Preventive action · [Mark Resolved]

### 6.2 Modal: `escalation-resolve`
- **Width:** 480px
- **Fields:** Resolution Notes (required, min 50 chars, 500 limit) · Root Cause (select: Process / Human Error / Equipment / External / Unknown) · Preventive Action (textarea, optional)
- **Buttons:** [Mark Resolved] + [Cancel]
- **On resolve:** Status changes to Resolved · Branch Principal notified · Audit log entry

### 6.3 Modal: `escalate-to-ceo`
- **Width:** 400px
- **Content:** "Escalate ESC-[ID] to CEO?" + reason field (required) + urgency toggle
- **Buttons:** [Confirm Escalation] + [Cancel]

### 6.4 Modal: `procurement-approve`
- **Width:** 420px
- **Content:** "Approve procurement of [description] from [Branch]?" · Cost: ₹[amount] · Vendor: [if specified]
- **Optional comment:** Textarea
- **Buttons:** [Approve] (primary) + [Cancel]

### 6.5 Modal: `procurement-reject`
- **Width:** 420px
- **Fields:** Reason (required, min 20 chars) · Alternative suggestion (optional)
- **Buttons:** [Reject] (danger) + [Cancel]

---

## 7. Charts

### 7.1 Escalation Trend (last 30 days)
- **Type:** Stacked bar chart
- **Data:** Daily escalation count by severity (Sev 1–4)
- **X-axis:** Last 30 days
- **Y-axis:** Count
- **Colours:** Red (Sev 1) · Orange (Sev 2) · Yellow (Sev 3) · Grey (Sev 4)
- **Tooltip:** Date · Sev breakdown · Total open
- **Export:** PNG

### 7.2 Branch SLA Score Distribution
- **Type:** Horizontal bar chart (sorted ascending)
- **Data:** SLA score per branch
- **Benchmark line:** 90 (target)
- **Colour:** Green >90 · Yellow 75–90 · Red <75
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Escalation assigned | "Escalation [ID] assigned to [Name]" | Success | 4s |
| Escalation resolved | "Escalation [ID] marked resolved" | Success | 4s |
| Escalated to CEO | "Escalation [ID] escalated to CEO. CEO notified." | Warning | 6s |
| Procurement approved | "Procurement [ID] approved. Branch notified." | Success | 4s |
| Procurement rejected | "Procurement [ID] rejected. Branch notified with reason." | Success | 4s |
| Note added | "Note added to escalation [ID]" | Info | 4s |
| Error | "Action failed. Try again." | Error | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open escalations | "All escalations resolved" | "No operational escalations are open right now" | — |
| No SLA breaches | "SLA compliance looks good" | "All branches are meeting their operational SLAs" | — |
| No procurement pending | "No procurement requests" | "No procurement requests are awaiting your approval" | — |
| No transport incidents | "No transport incidents" | "No transport incidents in the last 30 days" | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 6 KPI cards + escalation table (8 rows) + SLA table (5 rows) |
| Table filter/search | Inline skeleton rows |
| Escalation drawer open | Spinner + tabs skeleton |
| Approve / Reject action | Spinner in button + disabled |
| Mark resolved | Full-page overlay "Processing resolution…" |

---

## 11. Role-Based UI Visibility

| Element | VP G4 | CEO G4 | President G4 | Others |
|---|---|---|---|---|
| Page | ✅ | ❌ redirect | ❌ redirect | ❌ redirect |
| [Assign] [Resolve] on escalations | ✅ | ❌ | ❌ | ❌ |
| [Escalate to CEO] | ✅ | N/A | ❌ | ❌ |
| [Approve] [Reject] procurement | ✅ | ❌ | ❌ | ❌ |
| [+ Log Escalation] header | ✅ | ✅ (via own dashboard) | ❌ | ❌ |
| Export Daily Report | ✅ | ❌ | ❌ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/vp/dashboard/` | JWT (G4 VP) | Full VP dashboard |
| GET | `/api/v1/group/{id}/escalations/?assigned_to=vp` | JWT (G4) | VP escalation queue |
| GET | `/api/v1/group/{id}/escalations/{eid}/` | JWT (G4) | Escalation detail |
| POST | `/api/v1/group/{id}/escalations/{eid}/assign/` | JWT (G4 VP) | Assign escalation |
| POST | `/api/v1/group/{id}/escalations/{eid}/resolve/` | JWT (G4 VP) | Resolve escalation |
| POST | `/api/v1/group/{id}/escalations/{eid}/escalate/` | JWT (G4 VP) | Escalate to CEO |
| GET | `/api/v1/group/{id}/branches/sla/` | JWT (G4) | Branch SLA status |
| GET | `/api/v1/group/{id}/procurement/requests/?status=pending` | JWT (G4) | Procurement queue |
| POST | `/api/v1/group/{id}/procurement/requests/{rid}/approve/` | JWT (G4 VP) | Approve procurement |
| POST | `/api/v1/group/{id}/procurement/requests/{rid}/reject/` | JWT (G4 VP) | Reject with reason |
| GET | `/api/v1/group/{id}/transport/incidents/?days=30` | JWT (G4) | Transport incidents |
| GET | `/api/v1/group/{id}/escalations/trend/?days=30` | JWT (G4) | Escalation trend data |
| GET | `/api/v1/group/{id}/branches/sla/chart/` | JWT (G4) | SLA distribution chart |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Escalation search | `input delay:300ms` | GET `.../escalations/?q=` | `#escalation-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../escalations/?filters=` | `#escalation-section` | `innerHTML` |
| Pagination | `click` | GET `.../escalations/?page=` | `#escalation-section` | `innerHTML` |
| Open escalation drawer | `click` | GET `.../escalations/{id}/` | `#drawer-body` | `innerHTML` |
| Resolve modal submit | `submit` | POST `.../resolve/` | `#escalation-row-{id}` | `outerHTML` |
| Procurement approve | `click` | POST `.../approve/` | `#procurement-row-{id}` | `outerHTML` |
| SLA table sort | `click` | GET `.../branches/sla/?sort=` | `#sla-table-body` | `innerHTML` |
| KPI stats auto-refresh | `every 5m` | GET `.../vp/dashboard/stats/` | `#vp-stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
