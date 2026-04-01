# 33 — Escalation & Incident Centre

> **URL:** `/group/gov/escalations/`
> **File:** `33-escalation-incident-centre.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 · CEO G4 · VP G4 (primary owner) · President G4 (Academic incidents) · Exec Secretary G3 (view + notify)

---

## 1. Purpose

Centralised hub for all cross-branch escalations and incidents at the group level. Covers
operational escalations (branch SLA breaches, procurement delays, transport incidents),
academic incidents (exam malpractice, grievance escalations), HR incidents (staff misconduct,
BGV failures), welfare incidents, and emergency events.

VP Operations is the primary owner — assigned, resolves, and escalates. Chairman/MD receive
escalations that the VP cannot resolve within SLA. CEO monitors all open escalations.

Each escalation has Severity 1–4, SLA clock, assignment, and full resolution trail.

---

## 2. Role Access

| Role | Create | Assign | Resolve | Escalate to CEO | Escalate to Chairman | View |
|---|---|---|---|---|---|---|
| Chairman | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| MD | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| CEO | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| VP | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| President | ✅ Academic | ✅ Academic | ✅ Academic | ❌ | ❌ | Academic |
| Exec Secretary | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (notify only) |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Escalation & Incident Centre
```

### 3.2 Page Header
```
Escalation & Incident Centre                           [+ New Escalation]  [Export ↓]
[N] open · [N] overdue SLA · [N] Sev 1 active         (role-based button visibility)
```

### 3.3 Alert Strip (conditional — live, auto-refreshing every 2 minutes)
**Shown when:** Any Severity 1 escalation is open.

```
🔴  SEVERITY 1 ACTIVE — [N] critical escalations require immediate attention
    [Escalation title] · [Branch] · Open for [Xh Ym]               [View Now →]
```
Strip colour: Red. Each active Sev 1 listed on separate line. Dismissible per session.

### 3.4 Summary Stats Bar

| Stat | Value | Colour |
|---|---|---|
| Open Escalations | N | — |
| Overdue SLA | N | Red if >0 |
| Avg Resolution Time | Xh Ym | Green/Yellow/Red vs SLA target |
| Resolved This Month | N | — |
| Sev 1 Active | N | Red if >0 |
| Sev 2 Active | N | Orange if >0 |

### 3.5 Tabs
```
Open Escalations  |  In Progress  |  Overdue  |  Resolved  |  All
```

---

## 4. Escalation Table (all tabs share same columns, filtered by status)

**Search:** Title, branch name, ID, assignee. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Severity | Multi-select | Sev 1 · Sev 2 · Sev 3 · Sev 4 |
| Category | Multi-select | Operational · Academic · HR · Welfare · Emergency · Finance · Transport · Infrastructure |
| Branch | Multi-select | All branches |
| Zone | Multi-select | |
| Assignee | Search + select | Any platform user |
| SLA Status | Multi-select | Within SLA · At Risk · Overdue |
| Date Range | Date picker | Created date range |

**Active filter chips:** Dismissible, "Clear All", count badge.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ID | Text | ✅ | ESC-2026-0247 format |
| Title | Text (truncated 60 chars) | ✅ | Full tooltip on hover |
| Severity | Badge | ✅ | 🔴 Sev 1 · 🟠 Sev 2 · 🟡 Sev 3 · 🟢 Sev 4 |
| Category | Badge | ✅ | |
| Branch | Text | ✅ | |
| Zone | Badge | ✅ | |
| Status | Badge | ✅ | Open · In Progress · Escalated · Resolved · Closed |
| Assignee | Text | ✅ | Name + role |
| SLA | Countdown | ✅ | Green: within SLA · Yellow: <2h remaining · Red: overdue |
| Created | Datetime | ✅ | DD MMM HH:MM |
| Last Updated | Datetime | ✅ | |
| Actions | — | ❌ | View · Assign · Resolve · Escalate |

**Default sort:** Severity ascending + SLA overdue first.

**Pagination:** Server-side · 25/page.

**Row click:** Opens `escalation-detail` drawer.

**Row colour:**
- Sev 1: `bg-red-50`
- Sev 2: `bg-orange-50`
- Overdue SLA: bold red SLA countdown

---

## 5. Severity & SLA Definitions

| Severity | Label | SLA Target | Description | Examples |
|---|---|---|---|---|
| Sev 1 | Critical | 4 hours | Life/safety risk, major system failure, legal/compliance emergency | Student injury, fire incident, data breach, exam paper leak |
| Sev 2 | High | 24 hours | Significant operational disruption affecting >1 branch or large group | Principal vacancy unresolved >7 days, fee collection failure, major transport incident |
| Sev 3 | Medium | 72 hours | Branch-level operational issue requiring group intervention | SLA breach by branch, staff misconduct complaint, parent grievance unresolved |
| Sev 4 | Low | 7 days | Non-urgent issue requiring tracking | Minor policy breach, minor infrastructure issue, suggestion/feedback escalation |

**SLA clock:** Starts on creation timestamp. Paused on "Awaiting Information" status. Stops on resolution.

---

## 6. Drawers & Modals

### 6.1 Drawer: `escalation-create`
- **Trigger:** [+ New Escalation]
- **Width:** 680px
- **Tabs:** Details · Impact · Assignment · Notify

#### Tab: Details
| Field | Type | Required | Validation |
|---|---|---|---|
| Title | Text | ✅ | Min 10, max 200 chars |
| Category | Select | ✅ | Operational · Academic · HR · Welfare · Emergency · Finance · Transport · Infrastructure |
| Severity | Select | ✅ | Sev 1–4 (with SLA shown inline per selection) |
| Branch | Multi-select | ✅ | At least 1 branch |
| Zone | Auto-fill | — | Auto from branch selection |
| Description | Textarea | ✅ | Min 50 chars |
| Root Cause (if known) | Textarea | ❌ | |
| First Occurrence Date | Date | ✅ | |
| First Occurrence Time | Time | ❌ | |
| Recurring Issue? | Toggle | ❌ | Default Off — if On: links to prior escalations |
| Evidence / Attachments | File upload | ❌ | PDF/IMG/DOC · Max 20MB · Multiple |

**Sev 1 special field:**
| Field | Type | Required |
|---|---|---|
| Immediate Safety Risk? | Toggle | ✅ |
| Authorities Notified? | Toggle | Conditional | Required if Safety Risk = Yes |

#### Tab: Impact
| Field | Type | Required |
|---|---|---|
| Students Affected | Number | ❌ |
| Staff Affected | Number | ❌ |
| Financial Impact (est.) | Currency | ❌ |
| Operational Impact | Textarea | ❌ | Describe disruption |
| Reputational Risk | Select | ❌ | None · Low · Medium · High |

#### Tab: Assignment
| Field | Type | Required |
|---|---|---|
| Assign To | Search + select | ✅ | Any group-level staff |
| Due By | Datetime | ✅ | Auto-calculated from SLA but editable |
| Escalate Automatically If Unresolved By SLA | Toggle | ✅ | Default On |
| Escalation Target | Select | Conditional | CEO · MD · Chairman |

#### Tab: Notify
| Field | Type | Required |
|---|---|---|
| Notify | Multi-select | ✅ | Chairman · MD · CEO · VP · Branch Principal · Others |
| Channel | Multi-select | ✅ | WhatsApp · Email · In-App |
| Notify on Each Update | Toggle | ❌ | Default Off |

**Submit:** [Create Escalation] — assignee and all notified users receive WhatsApp + email.

---

### 6.2 Drawer: `escalation-detail`
- **Trigger:** Row click or [View]
- **Width:** 760px
- **Tabs:** Overview · Timeline · Actions · Evidence · Related

#### Tab: Overview
- Full escalation metadata (all fields from create + current status)
- Status badge (large, prominent)
- SLA countdown (live — updates every 60s via HTMX polling)
- Assignee card with [Reassign] button (role-permissioned)
- Impact summary
- [Quick Actions panel]:
  - [Update Status] dropdown: Open → In Progress → Awaiting Info → Resolved
  - [Escalate to CEO/Chairman] button (role-permissioned)
  - [Close Escalation] button

#### Tab: Timeline
- Chronological log of all activity on this escalation
- Entry types: Created · Status Changed · Comment Added · Reassigned · Escalated · Evidence Added · Resolved
- Per entry: Timestamp · Actor · Action description · Content (comment/status change)
- [+ Add Comment] button at top: Rich text comment + mention @user + file attachment
- Comments visible to all assignees and watchers

#### Tab: Actions
- **Resolution fields** (shown when [Update Status → Resolved] clicked):
  | Field | Type | Required |
  |---|---|---|
  | Resolution Summary | Textarea | ✅ | Min 100 chars |
  | Root Cause Identified | Select | ✅ | Yes · No · Partially |
  | Root Cause Description | Textarea | Conditional | Required if Yes/Partially |
  | Preventive Measures | Textarea | ❌ | Steps to prevent recurrence |
  | Resolved At | Datetime | ✅ | |
  | Resolution Verified By | Search + select | ❌ | A senior user who confirms |
- **[Mark Resolved]** button → status → Resolved · SLA clock stops · resolved-by recorded

**Escalation action:**
- [Escalate to CEO]: Confirmation modal → adds CEO as assignee, sends notification, logs escalation event
- [Escalate to Chairman/MD]: same pattern

#### Tab: Evidence
- Table: File Name · Uploaded By · Upload Date · Type · [View] [Download] [Delete]
- [+ Upload Evidence] button

#### Tab: Related
- **Linked Escalations:** Other escalations from the same branch or same category (last 6 months)
- **Related Compliance Actions:** If escalation type = Compliance, links to compliance action tracker
- **Related Audit Log Events:** Deep-links to audit log filtered by branch + date range of this escalation

---

### 6.3 Modal: `escalation-resolve`
- **Width:** 560px
- **Trigger:** [Resolve] from table row or [Mark Resolved] from drawer
- **Fields:**
  | Field | Type | Required |
  |---|---|---|
  | Resolution Summary | Textarea | ✅ | Min 100 chars |
  | Root Cause | Select | ✅ | |
  | Root Cause Description | Textarea | Conditional | |
  | Preventive Action | Textarea | ❌ | |
  | Notify Stakeholders | Toggle | ✅ | Default On |
- **Buttons:** [Mark Resolved] + [Cancel]

---

### 6.4 Modal: `escalation-escalate`
- **Width:** 440px
- **Trigger:** [Escalate] from table or drawer
- **Content:** Escalating to: [CEO/Chairman/MD] · Current SLA status · Time elapsed
- **Fields:** Escalation Reason (textarea, required, min 50 chars) · Notify (toggle)
- **Buttons:** [Escalate Now] + [Cancel]

---

## 7. Charts

### 7.1 Open Escalations by Severity (live)
- **Type:** Donut chart
- **Data:** Count per severity level
- **Auto-refresh:** Every 5 minutes
- **Export:** PNG

### 7.2 Escalation Volume Trend (last 12 months)
- **Type:** Stacked bar chart
- **Data:** Monthly escalation count stacked by category
- **Export:** PNG

### 7.3 Resolution Time Distribution
- **Type:** Histogram
- **Data:** Escalations grouped by resolution time (buckets: <4h · 4–24h · 1–3d · 3–7d · 7d+)
- **Colour:** Green → Yellow → Red (shorter = better)
- **Export:** PNG

### 7.4 SLA Compliance Rate (last 6 months)
- **Type:** Line chart
- **Data:** % escalations resolved within SLA per month
- **Threshold:** 90% target (dashed)
- **Export:** PNG

### 7.5 Top 10 Branches by Escalation Count
- **Type:** Horizontal bar chart
- **Data:** Branches sorted by total open escalations
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Escalation created | "Escalation [ESC-YYYY-NNN] created. Assignee notified." | Success | 4s |
| Escalation assigned | "Escalation reassigned to [Name]" | Success | 4s |
| Status updated | "Escalation status → [Status]" | Info | 4s |
| Comment added | "Comment added" | Success | 3s |
| Escalated to CEO/Chairman | "Escalation escalated to [Role]. [Name] notified." | Warning | 6s |
| Escalation resolved | "Escalation [ID] resolved. SLA met." / "Escalation resolved. SLA breached." | Success/Warning | 6s |
| Export started | "Escalation report generating…" | Info | Manual |
| Sev 1 created (special) | "⚠ Severity 1 escalation created. Immediate notifications sent." | Error | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No open escalations | "All Clear" | "No open escalations across branches" | — |
| No overdue | "No SLA Breaches" | "All escalations are within SLA" | — |
| No results (filter) | "No escalations match" | "Try different filters or search terms" | [Clear Filters] |
| No resolved (date range) | "No resolved escalations in this period" | "Try a wider date range" | [Change Range] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: alert strip + stats bar + table (10 rows) |
| Tab switch | Inline skeleton rows |
| Search / filter apply | Inline skeleton rows |
| Escalation detail drawer | Spinner in drawer |
| Timeline tab (within drawer) | Spinner in timeline section |
| SLA countdown (auto-refresh) | Silent background update — no visual loader |
| Chart initial load | Chart skeleton placeholder |
| Export | Spinner in export button |

---

## 11. Role-Based UI Visibility

| Element | Chairman/MD | CEO | VP | President | Exec Sec |
|---|---|---|---|---|---|
| [+ New Escalation] | ✅ | ✅ | ✅ | ✅ Academic | ❌ |
| [Escalate to CEO] | ✅ | — | ✅ | ❌ | ❌ |
| [Escalate to Chairman/MD] | — | ✅ | ❌ | ❌ | ❌ |
| [Assign / Reassign] | ✅ | ✅ | ✅ | ✅ own | ❌ |
| [Resolve Escalation] | ✅ | ✅ | ✅ | ✅ own | ❌ |
| [Add Comment] | ✅ | ✅ | ✅ | ✅ own | ❌ |
| [Upload Evidence] | ✅ | ✅ | ✅ | ✅ own | ❌ |
| View all categories | ✅ | ✅ | ✅ | Academic | ✅ read |
| Full resolution detail | ✅ | ✅ | ✅ | ✅ | ❌ |
| [Export] | ✅ | ✅ | ✅ | ❌ | ❌ |
| Alert Strip (Sev 1) | ✅ | ✅ | ✅ | ❌ | ✅ |
| All charts | ✅ | ✅ | ✅ | Partial | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/escalations/` | JWT (G3+) | Escalations list (paginated, filtered) |
| POST | `/api/v1/group/{id}/escalations/` | JWT (G3+) | Create escalation |
| GET | `/api/v1/group/{id}/escalations/{eid}/` | JWT (G3+) | Escalation detail |
| PUT | `/api/v1/group/{id}/escalations/{eid}/` | JWT (G3+) | Update escalation |
| POST | `/api/v1/group/{id}/escalations/{eid}/assign/` | JWT (G3+) | Assign/reassign |
| POST | `/api/v1/group/{id}/escalations/{eid}/escalate/` | JWT (G3+) | Escalate to higher authority |
| POST | `/api/v1/group/{id}/escalations/{eid}/resolve/` | JWT (G3+) | Resolve escalation |
| GET | `/api/v1/group/{id}/escalations/{eid}/timeline/` | JWT (G3+) | Activity timeline |
| POST | `/api/v1/group/{id}/escalations/{eid}/comments/` | JWT (G3+) | Add comment |
| POST | `/api/v1/group/{id}/escalations/{eid}/evidence/` | JWT (G3+) | Upload evidence |
| GET | `/api/v1/group/{id}/escalations/summary/` | JWT (G3+) | Stats bar summary |
| GET | `/api/v1/group/{id}/escalations/charts/by-severity/` | JWT (G4/G5) | Severity donut |
| GET | `/api/v1/group/{id}/escalations/charts/volume-trend/` | JWT (G4/G5) | Volume trend chart |
| GET | `/api/v1/group/{id}/escalations/charts/resolution-time/` | JWT (G4/G5) | Resolution histogram |
| GET | `/api/v1/group/{id}/escalations/charts/sla-compliance/` | JWT (G4/G5) | SLA compliance line |
| GET | `/api/v1/group/{id}/escalations/export/` | JWT (G4/G5) | Export report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../escalations/?q=` | `#escalation-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../escalations/?filters=` | `#escalation-table-section` | `innerHTML` |
| Tab switch | `click` | GET `.../escalations/?status=` | `#escalation-table-section` | `innerHTML` |
| Open detail drawer | `click` | GET `.../escalations/{id}/` | `#drawer-body` | `innerHTML` |
| Timeline tab (drawer) | `click` | GET `.../escalations/{id}/timeline/` | `#drawer-timeline` | `innerHTML` |
| SLA live countdown | `every 60s` | GET `.../escalations/summary/` | `#sla-stats` | `innerHTML` |
| Alert strip refresh | `every 120s` | GET `.../escalations/?severity=1&status=open` | `#alert-strip` | `innerHTML` |
| Add comment | `submit` | POST `.../escalations/{id}/comments/` | `#timeline-body` | `beforeend` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
