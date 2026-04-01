# 33 — Operations Audit Log

> **URL:** `/group/ops/audit-log/`
> **File:** `33-operations-audit-log.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full) · Operations Manager G3 (full — own actions + all ops actions) · Zone roles (own actions only)

---

## 1. Purpose

Immutable, append-only audit log of all operational actions performed in Division G pages.
Every state change, approval, assignment, and configuration change is recorded here with
full before/after context. Cannot be edited or deleted. Used for governance reviews,
dispute resolution, and compliance evidence.

---

## 2. Audited Events

| Category | Events Logged |
|---|---|
| Escalations | Created · Acknowledged · Assigned · Updated · Resolved · Escalated to CEO |
| Grievances | Created · Assigned · Priority changed · Responded · Resolved · Closed |
| SLA | Breach detected · Assigned · Remediation updated · Resolved · Config changed |
| Branch Coordinator | Assigned to branch · Removed from branch · Reassigned |
| Visits | Scheduled · Cancelled · Report submitted |
| Compliance | Item overridden · Checklist config changed · Score recalculated |
| Zones | Created · Edited · Branch assigned · Branch removed · Director changed |
| Procurement | Request created · Approved · Rejected · PO created · PO approved · Vendor added/edited/blacklisted · Delivery received · Payment recorded |
| Facilities | Maintenance ticket created · Assigned · Updated · Resolved · Building added/edited · CAPEX project created · Milestone updated · Certificate renewed |
| Reports | MIS generated · Scheduled · Resent |
| Configuration | SLA targets changed · Visit policy changed · Compliance checklist changed |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Audit Log
```

### 3.2 Page Header
```
Operations Audit Log                   [Export ↓]
Immutable · Append-only · [N] events today · [N] events this month
```

---

## 4. Search & Filters

**Search:** Event description, actor name, branch, entity ID. 300ms debounce.

**Advanced Filters:**
| Filter | Options |
|---|---|
| Event Category | Multi-select (all categories above) |
| Actor Role | COO · Ops Manager · Coordinator · Zone Director · Zone Ops · Zone Academic · System |
| Actor Name | Search |
| Branch | Multi-select |
| Zone | Multi-select |
| Date Range | Today · Last 7d · Last 30d · Last 90d · Custom |
| Severity | Info · Warning · Critical |

---

## 5. Audit Log Table

**Default sort:** Timestamp descending (newest first).

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Timestamp | ✅ | Date + time + timezone |
| Event | ✅ | Descriptive event name |
| Category | ✅ | Colour badge |
| Actor | ✅ | Name + role |
| Branch / Entity | ✅ | Affected branch or entity |
| Changes | ❌ | "Severity: P2 → P1" preview |
| IP Address | ✅ | Masked (last 2 octets visible) |
| Actions | — | View Details |

**Pagination:** Server-side · 50/page (higher than usual for audit logs) · 25/50/100/All.

**No edit/delete actions anywhere on this page.**

---

## 6. Audit Event Detail Drawer

- **Width:** 520px
- **Tabs:** Event · Before/After · Context · Session

**Event tab:**
- Full event description
- Actor: Name · Role · User ID
- Timestamp: exact with timezone
- Category and severity

**Before/After tab:**
- JSON diff view: what changed
- Highlighted: removed (red) · added (green) · unchanged (grey)

**Context tab:**
- Browser / device
- IP address (full, COO only — others see masked)
- Session ID
- Page URL where action was taken

**Session tab:**
- All actions by this actor in this session (session-scoped view)

---

## 7. Export

**Export formats:** CSV (flat) · PDF (formatted audit report) · JSON (machine-readable).

**Export includes:** All columns + full before/after JSON.

**Export requires COO authorization** for full data (including IP addresses).

---

## 8. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No events today | "No activity logged today" | — |
| No results | "No events match your search" | [Clear Filters] |

---

## 9. Loader States

Page load: Skeleton table (10 rows with varying column widths).
Filter apply: Inline skeleton rows.
Drawer open: Spinner in body.

---

## 10. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Zone roles |
|---|---|---|---|
| All events | ✅ | ✅ | Own actions only |
| IP address (full) | ✅ | ❌ Masked | ❌ |
| Before/After JSON | ✅ | ✅ | ✅ own |
| Export full | ✅ | ❌ limited | ❌ |
| Actor filter (any actor) | ✅ | ✅ | ❌ own only |

> **Immutability enforcement:** API returns 405 Method Not Allowed for any PUT/PATCH/DELETE
> on audit log endpoints. Only GET is permitted.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/ops/audit-log/` | JWT (G3+) | Audit log list |
| GET | `/api/v1/group/{id}/ops/audit-log/{event_id}/` | JWT (G3+) | Event detail |
| GET | `/api/v1/group/{id}/ops/audit-log/export/?format=csv&filters={}` | JWT (G4) | Export |

> No POST, PUT, PATCH, or DELETE endpoints exist for audit log. Write is append-only via
> internal Django signals, never via API request from frontend.

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | `/api/.../audit-log/?q={}` | `#audit-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../audit-log/?filters={}` | `#audit-table-section` | `innerHTML` |
| Sort | `click` | `/api/.../audit-log/?sort={}` | `#audit-table-section` | `innerHTML` |
| Pagination | `click` | `/api/.../audit-log/?page={n}` | `#audit-table-section` | `innerHTML` |
| Open event detail | `click` | `/api/.../audit-log/{id}/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
