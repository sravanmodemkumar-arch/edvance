# 11 — Grievance Resolution Centre

> **URL:** `/group/ops/grievances/`
> **File:** `11-grievance-resolution-centre.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full) · Operations Manager G3 (full) · Branch Coordinator G3 (own branches) · Zone roles (zone scope)

---

## 1. Purpose

Central management of all grievances escalated from branch level to Group HQ. Branches can
raise student, parent, and staff grievances internally — only unresolved or high-priority
grievances escalate to Group level. The Operations Manager owns resolution and SLA compliance.

> **Escalation policy:** Branch resolves within 7 days. If unresolved or P1/P2, auto-escalates
> to Group. P1 (child safety/abuse) auto-escalates immediately.

---

## 2. Grievance Categories & SLA

| Category | Sub-types | SLA (Resolution) | P-Level |
|---|---|---|---|
| Child Safety / POCSO | Abuse, harassment, bullying | P1 — 4h | P1 |
| Academic | Grade dispute, exam irregularity, teacher misconduct | P2 — 24h | P2 |
| Hostel Welfare | Food, hygiene, discipline, safety | P2 — 24h | P2 |
| Fee / Financial | Wrong billing, refund delayed, scholarship issue | P2 — 24h | P2 |
| Staff Conduct | Teacher/staff behaviour | P2 — 48h | P2 |
| Infrastructure | Facilities, transport, safety hazard | P3 — 72h | P3 |
| Administrative | Admission, TC, documentation | P3 — 72h | P3 |
| General | Other / unclassified | P4 — 7 days | P4 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Grievance Resolution Centre
```

### 3.2 Page Header
```
Grievance Resolution Centre             [+ Log Grievance]  [Export ↓]
[N] open · [N] overdue · [N] resolved this month
```

### 3.3 Status Tabs
```
[All]  [Open (N)]  [In Progress (N)]  [Overdue (N)]  [Resolved (N)]  [Closed (N)]
```
Each tab pre-filters the table below.

### 3.4 Summary Strip
| Card | Value |
|---|---|
| Total Open | Count |
| P1 Active | Count (red badge, pulsing if >0) |
| Overdue SLA | Count (orange if >0) |
| Avg Resolution Time | Days |
| Resolution Rate This Month | `88%` |

---

## 4. Search & Filters

**Search:** Grievance ID, complainant name, branch, subject. 300ms debounce.

**Advanced Filters:**
| Filter | Options |
|---|---|
| Category | Multi-select (all categories above) |
| Priority | P1 · P2 · P3 · P4 |
| Status | Open · In Progress · Overdue · Resolved · Closed · Withdrawn |
| Branch | Multi-select |
| Zone | Multi-select |
| Raised By | Student · Parent · Staff · Anonymous |
| Assigned To | Select coordinator/ops staff |
| Date Range | Custom date picker |
| SLA Status | Within SLA · At Risk (>75%) · Breached |

---

## 5. Grievances Table

**Default sort:** Priority ascending, then Age descending.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| ☐ | Checkbox | Row select |
| ID | ✅ | GRV-YYYY-NNNNN |
| Category | ✅ | Colour-coded badge |
| Priority | ✅ | P1 red · P2 orange · P3 yellow · P4 grey |
| Branch | ✅ | |
| Raised By | ✅ | Student / Parent / Staff / Anonymous |
| Subject | ✅ | First 60 chars |
| Raised Date | ✅ | |
| SLA Deadline | ✅ | Red if past · Yellow if <2h remaining |
| Days Open | ✅ | Red if >SLA |
| Assigned To | ✅ | Name or "Unassigned" (red) |
| Status | ✅ | Colour badge |
| Actions | — | View · Assign · Resolve · Escalate |

**Pagination:** Server-side · 25/page · 10/25/50/All.

**Bulk actions (Ops Mgr+):**
| Action | Notes |
|---|---|
| Bulk Assign | Assign selected to same owner |
| Export CSV | Selected or all filtered rows |
| Mark Reviewed | Acknowledge multiple at once |

---

## 6. Grievance Detail Drawer

- **Width:** 640px
- **Tabs:** Overview · Timeline · Actions · Escalation History · Related

**Overview tab:**
- Full description · Category · Priority · Branch · Complainant (name masked if anonymous) · Submitted date · SLA status
- Attached files/evidence
- Branch's last response/action

**Timeline tab:**
- Chronological event log: raised → acknowledged → assigned → in progress → resolved
- Each event: actor · timestamp · notes
- Cannot be edited (immutable)

**Actions tab (Ops Mgr/COO only):**
| Action | Notes |
|---|---|
| Assign to | Select coordinator or ops staff · required comment |
| Change Priority | Ops Mgr can escalate priority · logged |
| Add Response | Internal note or external response to complainant |
| Escalate to COO | For Ops Mgr — sends to COO queue |
| Escalate to Division | Route to HR / Finance / Academic team |
| Request More Info | Send request for additional information from branch |
| Mark Resolved | Resolution type + description (min 50 chars) |
| Close (No Action) | Only if duplicate, withdrawn, or out of scope |

**Escalation History tab:**
- All previous escalations for this grievance (if re-raised or transferred)

**Related tab:**
- Other grievances from same complainant / same branch in same period

---

## 7. Log Grievance Drawer (COO/Ops Mgr only)

> For manually logging grievances received offline (phone, in-person).

- **Width:** 560px
- **Fields:** Branch · Category · Priority · Raised By (type) · Complainant Name (optional for anonymous) · Subject · Full Description · Evidence files · SLA Start Date (default: today)
- **Note:** Auto-assigns SLA based on category priority

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Grievance assigned | "Grievance assigned to [Name]" | Success · 4s |
| Priority escalated | "Priority escalated to P[N] — notifications sent" | Warning · 6s |
| Grievance resolved | "Grievance marked resolved — complainant notified" | Success · 4s |
| Grievance escalated | "Escalated to COO — [COO Name] notified" | Warning · 6s |
| P1 grievance logged | "P1 grievance created — COO and POCSO Coordinator notified immediately" | Warning · manual dismiss |

---

## 9. P1 Auto-Alert

> When a P1 grievance is created or escalated from branch:
> - Immediate WhatsApp alert to COO, Operations Manager, and Group POCSO Coordinator
> - Pulsing red badge on all dashboards (COO, Ops Mgr)
> - Cannot be dismissed from dashboard until acknowledged by COO

---

## 10. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No open grievances | "No open grievances — all resolved" | — |
| No P1 grievances | "No child safety incidents" | — |
| No search results | "No grievances match your search" | [Clear Filters] |

---

## 11. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton summary strip + status tabs + table (5 rows) |
| Tab switch | Inline skeleton rows |
| Filter apply | Inline skeleton rows |
| Drawer open | Spinner in drawer |
| Resolve action | Full-page overlay "Processing resolution…" |

---

## 12. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Coordinator G3 | Zone Dir G4 |
|---|---|---|---|---|
| All branches | ✅ | ✅ | Own branches | Zone |
| Complainant Name (masked) | ✅ Unmasked | ✅ Unmasked | ❌ Masked | ✅ |
| [Assign] button | ✅ | ✅ | ❌ | ✅ zone |
| [Escalate to COO] | N/A | ✅ | ❌ | ✅ |
| [Close No Action] | ✅ | ✅ | ❌ | ❌ |
| [Log Grievance] | ✅ | ✅ | ❌ | ❌ |
| Export | ✅ | ✅ | ❌ | ✅ |
| P1 auto-alert view | ✅ | ✅ | ❌ | ✅ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/grievances/` | JWT (G3+) | Grievance list with all filters |
| GET | `/api/v1/group/{id}/grievances/summary/` | JWT (G3+) | Summary strip counts |
| GET | `/api/v1/group/{id}/grievances/{grv_id}/` | JWT (G3+) | Grievance detail |
| POST | `/api/v1/group/{id}/grievances/` | JWT (G3+) | Create grievance |
| POST | `/api/v1/group/{id}/grievances/{grv_id}/assign/` | JWT (G3+) | Assign |
| POST | `/api/v1/group/{id}/grievances/{grv_id}/resolve/` | JWT (G3+) | Resolve |
| POST | `/api/v1/group/{id}/grievances/{grv_id}/escalate/` | JWT (G3+) | Escalate |
| POST | `/api/v1/group/{id}/grievances/{grv_id}/respond/` | JWT (G3+) | Add response |
| GET | `/api/v1/group/{id}/grievances/export/?format=csv&filters={}` | JWT (G3+) | Export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | `/api/.../grievances/?status={}` | `#grievance-table-section` | `innerHTML` |
| Search | `input delay:300ms` | `/api/.../grievances/?q={}` | `#grievance-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../grievances/?filters={}` | `#grievance-table-section` | `innerHTML` |
| Sort | `click` | `/api/.../grievances/?sort={}` | `#grievance-table-section` | `innerHTML` |
| Open detail | `click` | `/api/.../grievances/{id}/` | `#drawer-body` | `innerHTML` |
| Resolve submit | `click` | POST `/api/.../grievances/{id}/resolve/` | `#grievance-row-{id}` | `outerHTML` |
| P1 badge poll | `every 60s` | `/api/.../grievances/summary/` | `#p1-badge` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
