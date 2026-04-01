# 26 — Group Audit Log

> **URL:** `/group/gov/audit-log/`
> **File:** `26-group-audit-log.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 · CEO G4 (full) · President G4 (Academic events) · VP G4 (Ops events) · Trustee G1 (read)

---

## 1. Purpose

Immutable, append-only audit log of all significant actions taken on the EduForge platform
for this institution group. Records who did what, when, where (IP), and what changed (before/after).

**Immutable rule:** No record can be edited or deleted — ever. Not even by Chairman. Records
are retained for 7 years per India's DPDP Act 2023.

Key audit events:
- User account changes (create, suspend, delete, role change)
- Branch activation/deactivation
- Approval decisions (approve/reject)
- Policy publish/archive
- Fee structure changes
- Exam schedule approvals/rejections
- Login events (all roles)
- Sensitive data views (student PII, financial data)
- Configuration changes (settings, feature toggles)

---

## 2. Role Access

| Role | Access | Scope |
|---|---|---|
| Chairman | Full — all events, all branches | All |
| MD | Full — all events | All |
| CEO | Full — all events | All |
| President | Academic events only | Exam, curriculum, scores |
| VP | Operational events only | Branch ops, escalations, procurement |
| Trustee | Read-only — key governance events | Approvals, policy, major changes |
| Advisor | ❌ | |
| Exec Secretary | ❌ | |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Group Audit Log
```

### 3.2 Page Header
```
Group Audit Log                                        [Export CSV ↓]  [?] Retention Policy
Immutable record · 7-year retention per DPDP Act · [N] events today
```

### 3.3 Summary Stats Bar (live)
| Stat | Value |
|---|---|
| Events Today | N |
| Events This Month | N |
| Unique Actors (Month) | N |
| Critical Events (Month) | N (login failures, suspensions, overrides) |

---

## 4. Audit Log Table

**Search:** Actor name, action description, target name. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Date Range | Date range picker | Last 7d · Last 30d · Last 90d · Custom |
| Actor | Search + select | Any user in the group |
| Action Type | Multi-select | Login · Create · Edit · Delete · Approve · Reject · View · Export · Config Change · Override · Suspend |
| Module | Multi-select | Branch · User · Academic · Finance · Approval · Policy · Communications · Settings |
| Branch | Multi-select | All branches + "Group-level" |
| Result | Multi-select | Success · Failed · Blocked |
| Severity | Multi-select | Info · Warning · Critical |

**Active filter chips:** Dismissible, "Clear All", count badge.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Timestamp | Datetime | ✅ | Format: DD MMM YYYY HH:MM:SS |
| Actor | Text | ✅ | Name + role in small text |
| Action | Badge + text | ✅ | Action type badge + description |
| Target | Text | ✅ | What was affected |
| Module | Badge | ✅ | Which area of the platform |
| Branch | Text | ✅ | Which branch or "Group-level" |
| Result | Badge | ✅ | Success (green) · Failed (red) · Blocked (orange) |
| Severity | Badge | ✅ | Info · Warning · Critical |
| IP Address | Text | ❌ | Partially masked: 192.168.*.* |
| Actions | — | ❌ | [View Details] |

**Default sort:** Timestamp descending (most recent first).

**Pagination:** Server-side · Default 50/page (audit logs have high volume) · Selector 25/50/100/All.

**Row click / [View Details]:** Opens `audit-detail` drawer.

**No row select** — no bulk actions allowed on audit log (immutable).

---

## 5. Drawers

### 5.1 Drawer: `audit-detail`
- **Trigger:** Row click or [View Details]
- **Width:** 520px
- **Tabs:** Event · Before/After · Context · IP/Session

#### Tab: Event
- **Fields displayed:**
  - Event ID (unique immutable ID)
  - Timestamp (full precision with timezone)
  - Actor: Name · Role · Level
  - Action Type: badge + full description
  - Target: Type + Name (e.g. "User: John Principal" or "Branch: HYD-04")
  - Module: Which system module
  - Branch: Which branch
  - Result: Success/Failed/Blocked
  - Severity: Info/Warning/Critical
  - System-generated note (if any)

#### Tab: Before/After
- Shows state of the changed object before and after the action
- Displayed as a diff table: Field · Before · After
- For non-edit actions (Create, Delete, Login): shows relevant state snapshot
- For financial changes: shows amount before/after + who authorized
- For role changes: old role → new role + who authorized
- "No change data available" message if action type doesn't produce a diff (e.g. pure view event)

#### Tab: Context
- Related events: Shows 5 events before and after this one in time (same actor or same target)
- Helps understand the chain of actions (e.g. an approval followed by a policy publish)

#### Tab: IP/Session
- Full IP address (unmasked — Chairman/MD only, others see partial mask)
- User Agent: Browser + OS + Device type
- Session ID (truncated)
- Session duration at time of event
- Location (country/state if available from IP geolocation)

---

## 6. Export

**[Export CSV ↓] button:**
- Exports all currently filtered audit log records to CSV
- Maximum export: 100,000 records per export
- File name: `audit_log_{group_id}_{start_date}_{end_date}.csv`
- CSV includes all columns plus full IP and full before/after data

**Note for G1 Trustee:** Export button hidden — Trustees can view but not export audit data.

---

## 7. Critical Event Highlighting

**Critical events are visually highlighted in the table:**
- Row background: `bg-red-50` for Critical severity events
- Severity badge: Red "Critical"

**Critical event types:**
- Failed login attempts (3+ in 5 minutes → Critical)
- User account deletion
- Branch deactivation
- Chairman override of a rejection
- Bulk approve (unusual pattern)
- Sensitive data export (>100 records)
- Config change (feature toggle, permission change)
- BGV status overridden manually

---

## 7a. Charts

### 7a.1 Audit Event Volume (last 30 days)
- **Type:** Line chart
- **Data:** Daily event count for last 30 days — all severities stacked (Info / Warning / Critical)
- **X-axis:** Dates
- **Y-axis:** Event count
- **Colours:** Blue (Info) · Yellow (Warning) · Red (Critical)
- **Tooltip:** Date · Info: N · Warning: N · Critical: N · Total: N
- **Export:** PNG

### 7a.2 Event Type Distribution (this month)
- **Type:** Doughnut chart
- **Data:** Count per Action Type (Login · Create · Edit · Delete · Approve · Reject · Config Change · Override · Export)
- **Colours:** One per action type
- **Centre text:** Total events this month
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export started | "Audit log exporting… large exports may take a few minutes" | Info | Manual |
| Export ready | "Audit log CSV ready — click to download" | Success | Manual |
| Audit detail load error | "Failed to load event details. Try again." | Error | Manual |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No events for filter | "No events match your filters" | "Try a wider date range or clear some filters" | [Clear Filters] |
| No events today | "No events today" | "Platform activity will appear here as events occur" | — |
| Before/After not available | "No change data for this event type" | — | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (15 skeleton rows, as audit log is dense) |
| Filter/search apply | Inline skeleton rows |
| Table sort | Inline skeleton rows |
| Pagination | Inline skeleton rows |
| Audit detail drawer | Spinner in drawer |
| IP/Session tab | Brief spinner (geo lookup) |
| Export trigger | Spinner in export button |

---

## 11. Role-Based UI Visibility

| Element | Chairman/MD | CEO | President | VP | Trustee |
|---|---|---|---|---|---|
| All action types | ✅ | ✅ | Academic only | Ops only | Governance events |
| Full IP address | Chairman/MD | ❌ | ❌ | ❌ | ❌ |
| IP/Session tab | ✅ | ❌ | ❌ | ❌ | ❌ |
| Before/After tab | ✅ | ✅ | ✅ (Academic) | ✅ (Ops) | ❌ |
| [Export CSV] | ✅ | ✅ | ✅ | ✅ | ❌ |
| Delete any record | ❌ (nobody) | ❌ | ❌ | ❌ | ❌ |
| Edit any record | ❌ (nobody) | ❌ | ❌ | ❌ | ❌ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/audit-log/` | JWT | Audit log list (paginated, filtered) |
| GET | `/api/v1/group/{id}/audit-log/{eid}/` | JWT | Event detail |
| GET | `/api/v1/group/{id}/audit-log/export/?format=csv` | JWT (G4/G5) | Export CSV |
| GET | `/api/v1/group/{id}/audit-log/stats/` | JWT | Summary stats |
| GET | `/api/v1/group/{id}/audit-log/charts/volume/` | JWT | Daily event volume (last 30d) |
| GET | `/api/v1/group/{id}/audit-log/charts/type-distribution/` | JWT | Event type distribution |

**No POST/PUT/DELETE endpoints exist for audit log — append-only at database level (PostgreSQL row-level security).**

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../audit-log/?q=` | `#audit-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../audit-log/?filters=` | `#audit-table-section` | `innerHTML` |
| Sort | `click` | GET `.../audit-log/?sort=&dir=` | `#audit-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../audit-log/?page=` | `#audit-table-section` | `innerHTML` |
| Open detail | `click` | GET `.../audit-log/{id}/` | `#drawer-body` | `innerHTML` |
| Stats bar auto-refresh | `every 5m` | GET `.../audit-log/stats/` | `#audit-stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
