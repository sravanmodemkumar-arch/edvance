# 12 — Operational Escalation Tracker

> **URL:** `/group/ops/escalations/`
> **File:** `12-operational-escalation-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full) · Operations Manager G3 (full) · Branch Coordinator G3 (raise/view own) · Zone Director G4 (zone) · Zone Ops Manager G3 (zone)

---

## 1. Purpose

Tracks all operational escalations raised from branches or by coordinators that require
Group HQ intervention. Separate from grievances (which are complainant-raised) — escalations
are internally raised by ops staff when branch cannot resolve an issue independently.

**Escalation types:** Staffing crisis · Infrastructure failure · Safety incident · Financial
irregularity · Academic misconduct · Student welfare · Transport emergency · Hostel incident.

---

## 2. Severity & SLA Framework

| Severity | Label | Description | SLA (First Response) | SLA (Resolution) |
|---|---|---|---|---|
| P1 | Critical | Child safety, physical harm, POCSO | 1 hour | 24 hours |
| P2 | High | Academic misconduct, financial fraud, major infrastructure | 4 hours | 72 hours |
| P3 | Medium | Staff dispute, minor infrastructure, transport delay | 24 hours | 7 days |
| P4 | Low | Administrative, process gap, minor complaints | 48 hours | 14 days |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Operational Escalation Tracker
```

### 3.2 Page Header
```
Operational Escalation Tracker          [+ New Escalation]  [Export ↓]
[N] open · [N] P1 active · [N] overdue SLA
```

### 3.3 Status Tabs
```
[All]  [Open (N)]  [Acknowledged (N)]  [In Progress (N)]  [Overdue (N)]  [Resolved (N)]
```

### 3.4 Summary Strip
| Card | Value |
|---|---|
| P1 Active | Count (pulsing red if >0) |
| P2 Active | Count |
| Overdue SLA | Count |
| Avg Resolution Days | Number |
| Escalations This Month | Count vs last month trend |

---

## 4. Search & Filters

**Search:** Escalation ID, branch name, type, description keywords. 300ms debounce.

**Advanced Filters:**
| Filter | Options |
|---|---|
| Type | Staffing Crisis · Infrastructure · Safety · Financial · Academic · Welfare · Transport · Hostel · Other |
| Severity | P1 · P2 · P3 · P4 |
| Status | Open · Acknowledged · In Progress · Overdue · Resolved · Closed |
| Branch | Multi-select |
| Zone | Multi-select |
| Raised By | Coordinator · Ops Manager · Branch Principal · System |
| Assigned To | Select |
| Date Range | Custom picker |

---

## 5. Escalations Table

**Default sort:** Severity ascending, then Age descending (P1 first, oldest first).

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| ☐ | Checkbox | Row select |
| ESC ID | ✅ | ESC-YYYY-NNNNN |
| Type | ✅ | Colour badge |
| Severity | ✅ | P1–P4 badge |
| Branch | ✅ | |
| Zone | ✅ | |
| Summary | ✅ | First 80 chars |
| Raised By | ✅ | |
| Raised Date | ✅ | |
| Response SLA | ✅ | Timer — red if breached |
| Resolution SLA | ✅ | Days remaining |
| Owner | ✅ | |
| Status | ✅ | |
| Actions | — | View · Reassign · Resolve · Escalate to CEO |

**Pagination:** Server-side · 25/page · 10/25/50/All.

---

## 6. Escalation Detail Drawer

- **Width:** 680px
- **Tabs:** Overview · Timeline · Actions · Evidence · Linked Records

**Overview tab:**
- Full description · Type · Severity · Branch · Zone · Raised by · Date
- SLA countdown timers (response + resolution)
- Current owner and status

**Timeline tab:**
- Immutable event log: created → acknowledged → assigned → progress updates → resolved
- Each entry: actor · timestamp · note

**Actions tab (COO/Ops Mgr):**
| Action | Notes |
|---|---|
| Acknowledge | Starts response SLA timer |
| Assign to Owner | Select from COO/Ops Mgr/Zone staff |
| Change Severity | With mandatory reason (audited) |
| Add Progress Update | Free text note, visibility: internal / visible to branch |
| Request Branch Action | Assign action to branch principal with deadline |
| Escalate to CEO | For COO — routes to CEO's approval queue |
| Link to Grievance | Link this escalation to a related grievance |
| Resolve | Resolution type + notes + outcome |
| Close (Not Actionable) | If out of scope or duplicate |

**Evidence tab:**
- Uploaded files, photos, documents
- [Add Evidence] button (any status)

**Linked Records tab:**
- Related grievances, maintenance tickets, visit reports linked to this escalation

---

## 7. Create Escalation Drawer

- **Width:** 640px
- **Trigger:** [+ New Escalation] or branch row → [Raise Escalation]

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Escalation Type | Select | Required |
| Severity | Select | Required |
| Branch | Searchable select | Required |
| Summary | Text | Required · max 120 chars |
| Full Description | Textarea | Required · min 50 chars |
| Evidence | File upload | Up to 10 files · 10MB each |
| Suggested Owner | Select | Optional |
| Immediate Action Taken | Textarea | Optional |
| P1 Notification | Auto-shown if P1 | "P1 will notify COO, POCSO Coord, CEO immediately" |

---

## 8. P1 Auto-Notifications

> Triggered immediately when P1 escalation is created/received.

- WhatsApp: COO, Operations Manager, Group POCSO Coordinator
- EduForge notification: CEO, COO, Operations Manager
- Pulsing badge on all dashboards until P1 is acknowledged
- If not acknowledged within 30 minutes: escalation auto-promoted to CEO

---

## 9. Resolution Workflow

**States:** Open → Acknowledged → In Progress → Resolved → Closed

**Resolution form:**
- Outcome type: Issue Resolved · Partial Resolution · No Action Required · Transferred to External Authority
- Resolution description: min 100 chars
- Follow-up required: Yes/No
- If Yes: follow-up action + owner + due date
- Notify branch: toggle (sends resolution summary to branch Principal)

---

## 10. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Escalation created | "Escalation ESC-[ID] created — owner notified" | Success · 4s |
| P1 created | "P1 Critical escalation created — emergency notifications sent" | Warning · manual dismiss |
| Acknowledged | "Escalation acknowledged — response SLA started" | Success · 4s |
| Assigned | "Escalation assigned to [Name]" | Success · 4s |
| Resolved | "Escalation resolved — branch notified" | Success · 4s |
| SLA breach alert | "SLA breach: [ESC-ID] — [N]h overdue" | Error · manual dismiss |

---

## 11. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No open escalations | "No open escalations" | — |
| No P1 | "No critical incidents" | — |
| No results | "No escalations match search" | [Clear Filters] |

---

## 12. Loader States

Page load: Skeleton summary strip + status tabs + table.
Drawer: Spinner in body while fetching detail.
Resolve action: Full-page overlay "Processing resolution…"

---

## 13. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Coordinator G3 | Zone Dir G4 |
|---|---|---|---|---|
| All branches | ✅ | ✅ | ❌ own only | Zone only |
| [Escalate to CEO] | ✅ | ✅ | ❌ | ❌ |
| [Acknowledge] | ✅ | ✅ | ❌ | ✅ zone |
| [Change Severity] | ✅ | ✅ | ❌ | ❌ |
| [Close Not Actionable] | ✅ | ✅ | ❌ | ❌ |
| [+ New Escalation] | ✅ | ✅ | ✅ (own branches) | ✅ |
| Export | ✅ | ✅ | ❌ | ✅ |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/escalations/` | JWT (G3+) | List with all filters |
| GET | `/api/v1/group/{id}/escalations/summary/` | JWT (G3+) | Summary strip |
| POST | `/api/v1/group/{id}/escalations/` | JWT (G3+) | Create escalation |
| GET | `/api/v1/group/{id}/escalations/{esc_id}/` | JWT (G3+) | Detail |
| POST | `/api/v1/group/{id}/escalations/{esc_id}/acknowledge/` | JWT (G3+) | Acknowledge |
| POST | `/api/v1/group/{id}/escalations/{esc_id}/assign/` | JWT (G3+) | Assign owner |
| POST | `/api/v1/group/{id}/escalations/{esc_id}/update/` | JWT (G3+) | Progress update |
| POST | `/api/v1/group/{id}/escalations/{esc_id}/resolve/` | JWT (G3+) | Resolve |
| POST | `/api/v1/group/{id}/escalations/{esc_id}/escalate-ceo/` | JWT (G4) | Escalate to CEO |
| GET | `/api/v1/group/{id}/escalations/export/?format=csv` | JWT (G3+) | Export |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | `/api/.../escalations/?status={}` | `#esc-table-section` | `innerHTML` |
| Search | `input delay:300ms` | `/api/.../escalations/?q={}` | `#esc-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../escalations/?filters={}` | `#esc-table-section` | `innerHTML` |
| Open detail | `click` | `/api/.../escalations/{id}/` | `#drawer-body` | `innerHTML` |
| Acknowledge | `click` | POST `/api/.../escalations/{id}/acknowledge/` | `#esc-row-{id}` | `outerHTML` |
| P1 badge poll | `every 60s` | `/api/.../escalations/summary/` | `#p1-badge` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
