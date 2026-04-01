# 33 — Hostel Audit Log

> **URL:** `/group/hostel/audit-log/`
> **File:** `33-hostel-audit-log.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Hostel Director (primary) · All hostel roles (view own actions)

---

## 1. Purpose

Immutable, comprehensive audit log of every action taken within the hostel management system across all branches. Every create, update, delete, status change, approval, escalation, decision, and notification event is recorded here with the actor's identity, timestamp, IP address, and before/after state.

The audit log cannot be edited or deleted by any user — not even the Group IT Admin. It is the compliance and accountability backbone for POCSO reporting, hostel governance audits, and regulatory inspections (CBSE boarding norms, state residential school rules).

The Hostel Director has full read access to all entries. Each hostel role can view only their own action history. The log is queryable with advanced filters and exportable for auditor use.

---

## 2. Role Access

| Role | Access |
|---|---|
| Group Hostel Director | Full read — all entries, all roles, all branches |
| All other hostel roles | Read — own actions only (same actor filter) |
| Group IT Admin | Read — all entries (for system-level compliance) |
| Group Internal Auditor | Read — all entries (for annual audits) |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Hostel Audit Log
```

### 3.2 Page Header
- **Title:** `Hostel Audit Log`
- **Subtitle:** `[N] Total Entries · Showing: [date range] · Last Updated: [time]`
- **Right controls:** `Advanced Filters` · `Export` · `Download for Audit`

---

## 4. KPI Summary

| Card | Value |
|---|---|
| Total Entries (All Time) | [N] |
| Entries Today | [N] |
| Actions by Discipline Committee | [N] (for POCSO/compliance value) |
| POCSO-linked Events | [N] (critical for compliance) |
| Entries This Month | [N] |

---

## 5. Main Audit Log Table

**Search:** Actor name, entity type, keyword. 300ms debounce.

**Advanced Filters:**
| Filter | Type |
|---|---|
| Date Range | Date-time range picker |
| Actor | Dropdown (all hostel staff) |
| Role | Multi-select (role types) |
| Event Category | Checkbox: Hosteler / Welfare / Discipline / Fee / Security / Medical / Mess / Admission / Policy / Room / Visitor / Parent Visit / Housekeeping / System |
| Action Type | Checkbox: Create / Update / Delete / Approve / Reject / Escalate / Close / Distribute / Login / Export |
| Branch | Multi-select |
| Entity | Text (e.g., "Welfare Incident", "Discipline Case", "Hosteler") |
| POCSO Event | Checkbox: POCSO-linked events only |

**Columns:**
| Column | Sortable |
|---|---|
| Timestamp | ✅ (default: most recent first) |
| Actor Name | ✅ |
| Role | ✅ |
| Branch | ✅ |
| Event Category | ✅ |
| Action | ✅ |
| Entity Type | ✅ |
| Entity ID / Name | ✅ |
| Summary | ❌ (e.g., "Welfare incident #145 status changed from Open to Resolved") |
| IP Address | ❌ |
| Actions | ❌ (View Detail) |

**Pagination:** Server-side · 50/page · Selector 25/50/100/All.

---

## 6. Event Categories and Action Examples

| Category | Example Events |
|---|---|
| Hosteler | "Hosteler admitted · Profile updated · Room transferred · Fee hold applied · Exited" |
| Welfare | "Incident created (Sev 2) · Status updated to In Progress · Escalated to Director · POCSO alert raised · Incident closed" |
| Discipline | "Case created · Evidence added · Hearing scheduled · Decision issued (Suspension 7 days) · Appeal filed · Appeal reviewed" |
| Fee | "Fee plan published · Payment recorded · Waiver approved · Defaulter reminded · Exit notice issued" |
| Security | "Security alert created (Sev 1) · CCTV offline reported · Alert escalated · Night roll call discrepancy logged · Alert closed" |
| Medical | "Medical visit logged · Emergency flagged · Doctor scheduled · Prescription marked collected · Medical watch added" |
| Mess | "Menu approved · Revision requested · Hygiene audit submitted (Score: 72%) · Vendor contract renewed" |
| Admission | "Application created · Seat allocated · Waitlisted · Rejected · Admission confirmed" |
| Policy | "Policy published · Policy archived · Acknowledgement reminder sent" |
| Room | "Bed allocated · Beds swapped · Room marked maintenance" |
| Visitor | "Visitor entry logged · Unauthorized entry flagged · Visitor exit logged" |
| Parent Visit | "Visit day scheduled · Visit day cancelled · Attendance marked · Calling violation logged" |

---

## 7. Drawers

### 7.1 Drawer: `audit-detail`
- **Trigger:** Table → row or Actions → View Detail
- **Width:** 520px
- **Content:**
  - Event metadata: Timestamp, Actor, Role, Branch, IP address, Session ID
  - **Session ID:** Links this audit event to the actor's authenticated login session (matches the session token record in the auth system). Cross-referencing Session IDs across multiple log entries reveals all actions taken within a single login session — enables full session-replay forensics for security investigations (e.g., compromised account activity review).
  - Entity: Type + ID + Name + Link to entity (if still accessible)
  - Action: Full action type and summary
  - Before state: JSON-formatted previous state (if update/delete)
  - After state: JSON-formatted new state
  - Related events: Other audit entries for the same entity in last 24h

---

## 8. POCSO Compliance Export

> Special export for regulatory compliance (NCPCR, POCSO audits).

**Trigger:** Export → POCSO Events Only

**Exports:** All POCSO-linked audit events (welfare incidents with POCSO flag, POCSO alert raises, POCSO Coordinator notifications) in a formatted PDF with:
- Group name + group ID
- Reporting period
- Event list with timestamps, actors, and resolutions
- Director signature field (for official submission)

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export triggered | "Audit log export started. You'll be notified when ready." | Info | 4s |
| POCSO export triggered | "POCSO compliance export started. Ready for download shortly." | Info | 5s |

---

## 10. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No entries for filters | "No Audit Events Match Filters" | "Adjust date range or event category." | [Clear Filters] |
| No POCSO events | "No POCSO-linked Events Found" | "No welfare incidents have triggered POCSO alerts in the selected period." | — |

---

## 11. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 5 KPI cards + table (15 rows) |
| Filter apply | Inline table skeleton |
| Audit detail drawer open | Centred spinner in drawer |
| Export | Spinner on Export button |

---

## 12. Role-Based UI Visibility

| Element | Hostel Director G3 | Any Other Hostel Role |
|---|---|---|
| All actors' actions | ✅ | ❌ (own actions only) |
| Actor filter dropdown | ✅ All staff | ❌ Own name only |
| POCSO-only export | ✅ | ❌ |
| Full before/after state | ✅ | ✅ own actions |
| IP address column | ✅ | ❌ hidden |
| Download for Audit | ✅ | ❌ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/audit-log/` | JWT (G3+) | Audit log (paginated, filtered; scoped by role) |
| GET | `/api/v1/group/{group_id}/hostel/audit-log/{id}/` | JWT (G3+) | Audit event detail |
| GET | `/api/v1/group/{group_id}/hostel/audit-log/kpis/` | JWT (G3+) | KPI cards |
| GET | `/api/v1/group/{group_id}/hostel/audit-log/export/` | JWT (G3+) | Export filtered log as CSV/XLSX |
| GET | `/api/v1/group/{group_id}/hostel/audit-log/pocso-export/` | JWT (G3+, Director only) | POCSO compliance PDF export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../audit-log/?q={val}` | `#audit-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../audit-log/?{filters}` | `#audit-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../audit-log/?page={n}` | `#audit-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../audit-log/?sort={col}&dir={asc/desc}` | `#audit-table-section` | `innerHTML` |
| Open event detail | `click` on row | GET `.../audit-log/{id}/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
