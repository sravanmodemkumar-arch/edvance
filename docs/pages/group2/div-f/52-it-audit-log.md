# Page 52: IT Audit Log

**URL:** `/group/it/audit/`
**Roles:** Group IT Director (Role 53, G4) — read; Group IT Admin (Role 54, G4) — read; Group Cybersecurity Officer (Role 56, G1) — read-only
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

Immutable audit trail of all IT operations performed across the EduForge platform by IT Admin, Integration Manager, and IT Director. Every configuration change, user account action, feature toggle, permission modification, integration config update, and security policy change is automatically logged here with a full before/after record.

**What is logged:**
- Portal configuration changes (branding, domain, feature toggles, notification settings)
- User account operations (creation, deactivation, role changes, password resets forced)
- Integration configurations (API key changes, SSO setup, webhook edits)
- Security policy changes (device policy, phishing campaign settings, training requirements)
- Feature toggle changes (enabling/disabling features per branch)
- Permission changes (role assignments, access level changes)
- Notification configuration changes
- Audit-significant data operations (bulk imports, data exports)

**Key properties:**
- Immutable: No one can edit or delete entries — not even Super Admin (G5)
- Append-only: New entries are only ever added; existing records cannot be modified
- Forensically reliable: Used for incident investigation, compliance audits, and accountability
- Full context: Each entry stores actor, timestamp, IP address, session ID, affected entity, and before/after values

The IT Audit Log is used by:
- IT Director and IT Admin: forensic investigation of configuration incidents
- Cybersecurity Officer: review of sensitive actions during security audits
- External auditors: evidence of controlled change management

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Director (Role 53, G4) | Read-only | View all entries; export |
| Group IT Admin (Role 54, G4) | Read-only | View all entries; export |
| Group Cybersecurity Officer (Role 56, G1) | Read-only | View all entries; cannot export |
| Super Admin (G5) | Read-only | Cannot delete or modify entries |
| All other roles | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| No one | Mutation | The audit log table is write-protected at the database level — INSERT only, no UPDATE/DELETE |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > Audit Log`

**Page Header:**
- Title: `IT Audit Log`
- Subtitle: `Immutable audit trail of all IT operations — read-only`
- Right side: `Export Audit Log (CSV)` button (Role 53/54 only)
- Security notice chip: `This log is immutable. Entries cannot be edited or deleted.`

**Alert Banners:**

1. **High-Risk Actions Today** (amber, dismissible):
   - Condition: any high-risk actions logged today (role changes, account suspensions, feature disables)
   - Text: `[X] high-risk actions were taken today. Review the log for any unauthorised changes.`

2. **Unusual Actor Activity** (amber, dismissible):
   - Condition: single actor performed > 50 actions in < 1 hour
   - Text: `Unusual activity detected: [Actor Name] performed [X] actions in the last hour. Verify this was authorised.`

---

## 4. KPI Summary Bar

Four KPI cards in a 4-column grid.

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Events Today | Count of audit entries with timestamp = today | Plain number |
| 2 | Events This Month | Count of audit entries in current calendar month | Plain number |
| 3 | High Risk Actions | Count of entries with risk_level = high-risk in last 30 days (role changes, account suspensions, feature disables, permission grants) | Number — amber if > 0 |
| 4 | Unique Actors (Last 30d) | Count of distinct user IDs who have taken audited actions in last 30 days | Number |

---

## 5. Main Table — Audit Log

**Table Title:** `IT Audit Log`
**Note displayed under title:** `All entries are read-only. Audit log integrity is enforced at database level.`

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Timestamp | DateTime | Full datetime with timezone; sortable |
| Actor | Text | `[Full Name] ([Role])` |
| Action Category | Badge | Portal Config / User Management / Integration / Security Policy / Feature Toggle / Permission Change / Notification Config / Data Operation |
| Action Description | Text | Human-readable description, e.g., `Changed fee module to Enabled for Bangalore Branch` |
| Affected Entity | Text | Branch name, user email, integration name, or feature name |
| Before Value | Text (truncated) | Previous value; truncated at 40 chars; full detail in drawer |
| After Value | Text (truncated) | New value; truncated at 40 chars; full detail in drawer |
| IP Address | Text | IP address of the actor's session |
| Risk Level | Badge | Routine (grey) / Sensitive (amber) / High-Risk (red) |
| Actions | Button | `View Full Detail` |

### Filters

- **Actor:** Dropdown of all users who have audit log entries
- **Action Category:** Multi-select (all categories listed)
- **Branch:** Multi-select (branch affected by the action)
- **Date Range:** From/to datetime picker
- **Risk Level:** All / Routine / Sensitive / High-Risk

### Search

Full-text search on Action Description and Affected Entity. `hx-trigger="keyup changed delay:400ms"`, targets `#audit-table`.

### Pagination

Server-side, 50 rows per page (audit logs are high-volume; larger page size appropriate). `hx-get="/group/it/audit/table/?page=N"`, targets `#audit-table`.

### Sorting

Default sort: Timestamp descending (most recent first). Cannot be changed (audit logs should always show newest first). No alternative sort provided.

---

## 6. Drawers

### A. View Event Detail Drawer (640px, right-side — all permitted roles)

Triggered by `View Full Detail` button.

**Drawer Header:** `Audit Event Detail — [Timestamp]`

**Sections:**

**Actor & Session:**
- Actor Name + Role
- Session ID (UUID)
- IP Address
- User Agent (browser/device info)
- Timestamp (full with timezone)

**Action Details:**
- Action Category badge
- Risk Level badge
- Action Description (full, untruncated)
- Affected Entity (full)

**Change Record (Before / After):**
- Displayed as a structured diff:
  - If simple value: `Before: [value]` → `After: [value]`
  - If complex object (JSON): formatted JSON diff showing added/changed/removed fields in colour (green additions, red removals, amber changes)
  - For sensitive fields (passwords, API keys): shown as `[REDACTED]` — audit records existence of change but not the actual value

**Related Entities:**
- If linked to a ticket: link to ticket
- If linked to a security incident: link to incident
- If linked to an access review: link to review

**Footer:** `Close` only. No action buttons — this is strictly read-only.

---

## 7. Charts

Two charts below the main table in a 2-column grid.

### Chart 1: Audit Event Volume Over 30 Days
- **Type:** Line chart
- **Series:** Total events (blue), High-Risk events (red)
- **X-axis:** Last 30 days (daily data points)
- **Y-axis:** Event count
- **Purpose:** Identify unusual spikes in activity that may indicate unauthorised bulk changes
- **Data endpoint:** `/api/v1/it/audit/charts/volume-trend/`

### Chart 2: Events by Action Category
- **Type:** Donut chart
- **Segments:** Each action category with count and %
- **Period:** Last 30 days
- **Purpose:** Understand the composition of IT operations — what types of changes are most common
- **Data endpoint:** `/api/v1/it/audit/charts/by-category/`

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Export initiated | Info: `Exporting audit log. Large exports may take a few moments.` |
| Export ready | Success: `Audit log CSV downloaded.` |
| Page filtered | Info: `Audit log filtered. Showing [X] matching entries.` |
| Alert dismissed | Info: `Alert hidden for this session.` |

> No create/update/delete operations exist. No success/error toasts for data mutations.

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No audit entries yet | Icon + `No audit events recorded yet. Events will appear as IT operations are performed.` |
| No entries match filters | `No audit entries match the selected filters. Try adjusting the date range or category.` |
| No high-risk actions today | KPI card: `0` (green) |
| Drawer — no before/after data | `No before/after values recorded for this event type.` |
| Drawer — no related entities | Related Entities section: `No linked records.` |
| Filter returns no entries | `No audit entries match the selected filters. Try adjusting the date range or category.` | — |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 4 skeleton shimmer cards |
| Audit table | 8 skeleton rows (audit table is denser) |
| Event detail drawer | Spinner then sections render progressively |
| JSON diff display | Spinner then diff renders (may involve formatting large JSON) |
| Charts | Spinner in chart containers |
| Export button | `Exporting...` text + disabled (exports can be large) |

---

## 11. Role-Based UI Visibility

| UI Element | Role 56 (G1) | Role 54 (G4) | Role 53 (G4) |
|------------|-------------|-------------|-------------|
| Audit table | Visible | Visible | Visible |
| View Full Detail button | Visible | Visible | Visible |
| Actor filter | Visible | Visible | Visible |
| Risk Level filter | Visible | Visible | Visible |
| Export CSV | Hidden | Visible | Visible |
| All KPI cards | Visible | Visible | Visible |
| Alert banners | Visible | Visible | Visible |
| Charts | Visible | Visible | Visible |
| Any edit/delete | Not available | Not available | Not available |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/audit/` | Fetch audit log entries (paginated, filtered) |
| GET | `/api/v1/it/audit/{id}/` | Fetch single event detail |
| GET | `/api/v1/it/audit/kpis/` | Fetch KPI values |
| GET | `/api/v1/it/audit/charts/volume-trend/` | Event volume over 30 days |
| GET | `/api/v1/it/audit/charts/by-category/` | Events by category |
| GET | `/api/v1/it/audit/export/csv/` | Export audit log CSV |

**No POST/PUT/DELETE endpoints exist for the audit log. All audit entries are written by internal system services (Django signals/middleware), not by frontend API calls.**

**Query Parameters (audit list):**
- `page`, `page_size` (default 50)
- `actor_id` (UUID)
- `action_category` (multi — comma-separated)
- `branch_id` (UUID)
- `date_from`, `date_to` (ISO datetime)
- `risk_level` (routine/sensitive/high-risk)
- `search` (text)

---

## 13. HTMX Patterns

```html
<!-- Audit table with filters -->
<div id="audit-table"
     hx-get="/group/it/audit/table/"
     hx-trigger="load"
     hx-target="#audit-table"
     hx-include="#audit-filter-form">
</div>

<!-- Search -->
<input type="text" name="search" placeholder="Search actions or entities..."
       hx-get="/group/it/audit/table/"
       hx-trigger="keyup changed delay:400ms"
       hx-target="#audit-table"
       hx-include="#audit-filter-form" />

<!-- Date range filter apply -->
<button hx-get="/group/it/audit/table/"
        hx-target="#audit-table"
        hx-swap="outerHTML"
        hx-include="#audit-filter-form">
  Apply Filters
</button>

<!-- View event detail drawer -->
<button hx-get="/group/it/audit/{{ event.id }}/detail/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  View Full Detail
</button>

<!-- Pagination -->
<button hx-get="/group/it/audit/table/?page={{ next_page }}"
        hx-target="#audit-table"
        hx-include="#audit-filter-form">
  Next →
</button>

<!-- KPI bar -->
<div id="audit-kpis"
     hx-get="/group/it/audit/kpis/"
     hx-trigger="load"
     hx-target="#audit-kpis">
</div>

<!-- Charts -->
<div id="chart-volume"
     hx-get="/group/it/audit/charts/volume-trend/"
     hx-trigger="load"
     hx-target="#chart-volume">
</div>

<div id="chart-categories"
     hx-get="/group/it/audit/charts/by-category/"
     hx-trigger="load"
     hx-target="#chart-categories">
</div>
```

**Audit Log Writing Pattern (Django middleware — not frontend):**

```python
# Example Django signal / middleware pattern for writing audit entries
# This writes to audit_log table with INSERT only (no UPDATE/DELETE ever)
def log_audit_event(actor, category, description, entity, before, after, request):
    AuditLog.objects.create(
        actor=actor,
        action_category=category,
        action_description=description,
        affected_entity=entity,
        before_value=json.dumps(before),
        after_value=json.dumps(after),
        ip_address=get_client_ip(request),
        session_id=request.session.session_key,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        risk_level=derive_risk_level(category, description),
    )
    # Never call .save(), .update(), or .delete() on AuditLog from application code
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
