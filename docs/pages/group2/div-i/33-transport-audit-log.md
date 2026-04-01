# 33 — Transport Audit Log

> **URL:** `/group/transport/audit/`
> **File:** `33-transport-audit-log.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Transport Director (primary) · Transport Safety Officer · Group IT Admin (Div F)

---

## 1. Purpose

Immutable, tamper-proof audit log of every action taken across the transport management system — vehicle additions/modifications, route approvals, driver assignments, fee plan changes, GPS alerts, incident reports, compliance renewals, bus pass issuances, policy publications, and user access events.

This page is critical for:
- Internal investigations following accidents or incidents
- Financial audits (fee plans, collections)
- Regulatory compliance (RTO, state transport authority)
- DPDP Act compliance (who accessed student transport data)

No actions can be performed from this page — it is read-only. All records are permanent and cannot be edited or deleted.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Transport Director | G3 | Full — all transport audit events | Primary consumer |
| Group Transport Safety Officer | G3 | Safety events — incidents, alerts, GPS | Scoped view |
| Group Fleet Manager | G3 | Fleet events — vehicles, maintenance, compliance | Scoped view |
| Group IT Admin (Div F) | G4 | Full — all events including access logs | IT oversight |
| Group Internal Auditor | G1 | Read-only — for audit review | View all |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Transport Audit Log
```

### 3.2 Page Header
- **Title:** `Transport Audit Log`
- **Subtitle:** `[N] Events Today · [N] Events This Month · Retention: 7 years`
- **Right controls:** `Advanced Filters` · `Export` · `Search`

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Events Today | Count | Blue |
| Events This Week | Count | Blue |
| High-Risk Events (Today) | Safety + compliance | Yellow > 0 |
| Failed Actions | Actions that returned error | Yellow > 0 |

---

## 5. Main Table — Audit Log

**Search:** User, action type, entity (bus number, student name, route name), IP address. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Event Category | Checkbox | Vehicle / Route / Driver / GPS / Fee / Safety / Bus Pass / Policy / Access |
| Action Type | Checkbox | Created / Updated / Deleted / Approved / Rejected / Published / Escalated / Exported / Login / Failed |
| User | Multi-select | All users with transport roles |
| Branch | Multi-select | All branches |
| Date Range | Date picker | |
| Severity | Radio | All / High-Risk / Normal |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Timestamp | ✅ | To the second |
| Event ID | ✅ | Unique immutable ID |
| User | ✅ | Name + role |
| Action | ✅ | e.g., "Vehicle Fitness Certificate Updated" |
| Category | ✅ | Badge (Vehicle / Route / Driver / etc.) |
| Entity | ✅ | Affected object (Bus No, Route Name, Student Name, etc.) |
| Branch | ✅ | |
| IP Address | ✅ | |
| Status | ✅ | Success / Failed / Warning |
| Details | ❌ | [View →] |

**Default sort:** Timestamp descending.
**Pagination:** Server-side · 50/page.

---

## 6. Event Detail Drawer

### 6.1 Drawer: `audit-event-detail`
- **Trigger:** Actions → View
- **Width:** 600px
- **Content:**
  - Event ID · Timestamp · User (name, role, IP)
  - Action · Category · Status
  - **Before state** (JSON or field-by-field table): What the record looked like before the action
  - **After state**: What it looks like after
  - **Diff highlight**: Changed fields highlighted in yellow
  - Session ID · User agent (browser/device)
  - Related events (same user, same session, same entity) — linked list

---

## 7. Export

**Export options:** CSV · XLSX · JSON (for compliance handoff)

**Fields exported:** All columns + before/after state + full diff

**Note:** Exports are logged themselves as audit events. Large exports (> 10,000 rows) are processed asynchronously and delivered via email/notification.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export initiated | "Audit log export is being prepared. You'll be notified when ready." | Info | 4s |
| Export ready | "Audit log export ready. Download below." | Success | 4s |
| Export failed | "Audit log export failed. Please try again or reduce the date range." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No events for filter | "No Audit Events Found" | "No events match the selected filters." |
| No events at all | "No Audit Events Yet" | "Audit events will appear here once transport operations begin." |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 4 KPI cards + table skeleton (20 rows) |
| Filter/search | Table body skeleton |
| Event detail drawer | 600px skeleton; before/after diff renders progressively |
| Large export | Async — spinner then notification when complete |

---

## 11. Role-Based UI Visibility

| Element | Transport Director G3 | Safety Officer G3 | Fleet Manager G3 | IT Admin G4 | Internal Auditor G1 |
|---|---|---|---|---|---|
| View All Events | ✅ | Safety events only | Fleet events only | ✅ | ✅ |
| View Event Detail | ✅ | ✅ (scoped) | ✅ (scoped) | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ | ✅ | ✅ |
| View Access Logs | ✅ | ❌ | ❌ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/audit/` | JWT (G3+) | Paginated, filtered audit log |
| GET | `/api/v1/group/{group_id}/transport/audit/{event_id}/` | JWT (G3+) | Event detail with diff |
| GET | `/api/v1/group/{group_id}/transport/audit/export/` | JWT (G3+) | Async export trigger |
| GET | `/api/v1/group/{group_id}/transport/audit/kpis/` | JWT (G3+) | KPI cards |

> **Note:** All write endpoints across the transport system automatically generate audit log entries via a Django signal (`post_save` + custom audit middleware). No separate API call is needed to log events.

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:400ms` | GET `.../audit/?q={val}` | `#audit-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../audit/?{filters}` | `#audit-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../audit/?sort={col}&dir={asc/desc}` | `#audit-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../audit/?page={n}` | `#audit-table-section` | `innerHTML` |
| Open event detail | `click` on View | GET `.../audit/{id}/` | `#drawer-body` | `innerHTML` |
| Export | `click` | GET `.../audit/export/?{filters}` | `#export-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
