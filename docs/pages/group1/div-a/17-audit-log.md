# div-a-17 — Audit Log

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Audit events/day | ~50,000–200,000 |
| Audit events/month | ~1.5M–6M |
| Retention | 5 years (compliance requirement) |
| Event types | ~80 distinct event types |
| Users (platform staff) | ~20–50 |
| Institution admin users | ~4,000 (2 per institution avg) |
| Search latency target | < 500ms on last 90 days |

**Why this matters:** The Audit Log is the forensic trail. After a security incident or compliance audit, every action taken by every platform user must be traceable. DPDPA and ISO 27001 both require audit trails. This page must support "who did what to which institution's data, and when."

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Audit Log |
| Route | `/exec/audit/` |
| Django view | `AuditLogView` |
| Template | `exec/audit_log.html` |
| Priority | P1 |
| Nav group | Compliance |
| Required role | `exec`, `superadmin`, `compliance`, `ops` |
| 2FA required | Exporting audit logs |
| HTMX poll | None (on-demand search) |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Audit Log                                    [Export] [Live View ▾] │
├──────────┬──────────┬──────────┬──────────┬──────────────────────────────── ┤
│ Events   │ Events   │ Unique   │ High-Risk│  Event Types                    │
│ (Today)  │ (7d)     │ Users    │ Events   │  Tracked                        │
│  62,400  │ 421,000  │   184    │    12    │    80                           │
├──────────┴──────────┴──────────┴──────────┴──────────────────────────────── ┤
│ [🔍 Search events, user, entity ID, IP...]                                   │
│ [User ▾] [Event Type ▾] [Entity ▾] [Severity ▾] [Date Range ▾]             │
│ Active filters: User: admin@platform ×                          [Clear all] │
├──────────────────────────────────────────────────────────────────────────────┤
│ TABS: [All Events] [High Risk] [Auth Events] [Data Access] [Config Changes] │
├──────────────────────────────────────────────────────────────────────────────┤
│ Timestamp        │ User          │ Event Type     │ Entity  │ IP  │ Details │
│ 2025-03-15 14:32 │ admin@platform│ institution.suspend│ Inst#42│ ... │ [View] │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Detail | Alert |
|---|---|---|---|
| 1 | Events (Today) | Count today | — |
| 2 | Events (7d) | Count last 7 days | — |
| 3 | Unique Users (7d) | Distinct actors in last 7 days | — |
| 4 | High-Risk Events (7d) | Events flagged as high-risk | > 20 = amber |
| 5 | Event Types Tracked | Total distinct event types | — |

---

### 4.2 Search Bar

`id="audit-search"` · Full-width · debounced 500ms (slower debounce due to expensive query)
Placeholder: "Search by user, entity ID, IP address, event type, description..."
**Supports:** `user:email@example.com` · `ip:192.168.1.1` · `entity:institution` · `event:invoice.created` prefix syntax

---

### 4.3 Filter Bar

`id="audit-filters"` · `flex flex-wrap gap-3 p-4`

| Filter | Type | Options |
|---|---|---|
| User | Searchable dropdown | All users or search by email |
| Event Type | Searchable multi-select | 80 event types grouped by category |
| Entity | Dropdown | Institution / Student / Invoice / User / Plan / API Key / Webhook / Setting |
| Severity | Multi-select | Info / Warning / Critical |
| Date Range | Datetime range picker | Default: last 24h · max: 90 days |

**Date range limitation notice:** "Searches older than 90 days may take longer. Use Export for historical searches."

---

### 4.4 Tab Bar

Tabs: All Events · High Risk · Auth Events · Data Access · Config Changes
**Pre-defined filter sets per tab:**
- High Risk: severity = Critical + select high-risk event types
- Auth Events: event_type in [login, logout, 2fa, password_change, session]
- Data Access: event_type in [student.data.accessed, invoice.viewed, report.exported]
- Config Changes: event_type in [setting.changed, plan.changed, user.created, role.changed]

---

### 4.5 Audit Event Table

`id="audit-table"` · `hx-get="?part=audit_table"` `hx-trigger="load, filter-change"`

**No auto-poll** (audit log is query-on-demand)

**Container:** `bg-[#0D1526] rounded-xl border border-[#1E2D4A] overflow-x-auto`

#### Column Specifications

| Column | Width | Detail |
|---|---|---|
| Timestamp | 160px | `YYYY-MM-DD HH:MM:SS IST` · `font-mono text-xs text-[#64748B]` |
| User | 180px | Email + role badge · `text-sm` |
| Event Type | 180px | `event.category.action` monospace · colour-coded category |
| Entity Type | 100px | Institution / Student / Invoice / etc. |
| Entity ID / Name | 160px | Clickable → entity detail page |
| Severity | 80px | Info `text-[#60A5FA]` · Warning `text-[#FCD34D]` · Critical `text-[#F87171]` |
| IP Address | 110px | IPv4/IPv6 · `font-mono text-xs` |
| [Details] | 70px | Button → opens Event Detail Drawer |

**Event type colour coding:**
- `auth.*` → `text-[#A78BFA]`
- `institution.*` → `text-[#60A5FA]`
- `student.*` → `text-[#34D399]`
- `billing.*` → `text-[#FCD34D]`
- `security.*` → `text-[#F87171]`
- `config.*` → `text-[#22D3EE]`

**Critical severity rows:** `bg-[#1A0A0A]` background tint

**Pagination:** 50/page · `?page=N` · total count capped display at "10,000+" for large result sets (full count is expensive)
- "Showing 1–50 of 10,000+ events" for large queries

---

### 4.6 Live View Mode

Toggle [Live View ▾] → dropdown: Off / Last 100 / Last 500
When active: `hx-trigger="every 5s"` on table · prepends new events at top
`hx-swap="afterbegin" hx-target="#audit-event-rows"`
New events slide in with `animate-pulse` for 2 seconds then settle

---

## 5. Drawers

### 5.1 Event Detail Drawer (560 px)

`id="event-drawer"` · `body.drawer-open`

**Header:** Event type badge + timestamp · `[×]`

**Section A — Event Summary:**
| Field | Value |
|---|---|
| Event ID | EVT-XXXXXXXXXXXXXXXX (UUID) |
| Event type | `institution.suspended` |
| Timestamp | 2025-03-15 14:32:05.418 IST |
| User | admin@platform.com (Ops role) |
| Session ID | `sess_abc123...` (masked last 8) |
| IP Address | 192.168.1.100 |
| User Agent | Chrome 122 on Windows 11 |
| Severity | Critical |

**Section B — Entity:**
| Field | Value |
|---|---|
| Entity type | Institution |
| Entity ID | INST-00342 |
| Entity name | ABC Coaching Centre |

**Section C — Changes (if applicable):**
JSON diff view showing before → after:
```json
// Before
{"status": "active"}

// After
{"status": "suspended", "reason": "non_payment"}
```
`<pre class="bg-[#070C18] rounded-lg p-3 text-xs font-mono text-[#94A3B8] overflow-x-auto">`

**Section D — Context:**
- Request ID: for correlation with application logs
- Correlation events: other events in the same session around this timestamp

**Footer:** [View Entity] [Export Event] [Close]

---

## 6. Modals

### 6.1 Export Audit Log Modal (480 px)

**2FA required.**
| Field | Type | Detail |
|---|---|---|
| Date range | Datetime range | Required |
| Event types | Multi-select | Default: all |
| User filter | Search | Optional |
| Format | CSV / JSON / PDF | CSV default |
| Max rows | Number | Cap: 500,000 rows |
| Email delivery | Checkbox | Required if > 100K rows |

**Warning for large exports:** "Exports > 100K rows will be delivered by email (up to 30 min)."
**Footer:** [Cancel] [Export]

---

## 7. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/audit_kpi.html` | Page load |
| `?part=audit_table` | `exec/partials/audit_table.html` | Search · filter · tab · page |
| `?part=event_drawer&id={id}` | `exec/partials/event_drawer.html` | [Details] button |
| `?part=live_events` | `exec/partials/audit_live_rows.html` | Live view poll (every 5s) |

**Django view dispatch:**
```python
class AuditLogView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_audit_log"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/audit_kpi.html",
                "audit_table": "exec/partials/audit_table.html",
                "event_drawer": "exec/partials/event_drawer.html",
                "live_events": "exec/partials/audit_live_rows.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/audit_log.html", ctx)

    def post(self, request):
        if request.GET.get("part") == "export":
            return self._handle_export(request)
        return HttpResponseNotAllowed(["GET"])
```

**Query optimisation:**
```python
# Use read replica for audit queries
def _build_audit_qs(self, filters):
    return (
        AuditEvent.objects
        .using("readonly_replica")
        .filter(**filters)
        .select_related("user", "entity_institution")
        .order_by("-timestamp")
    )
```

---

## 8. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 300 ms | > 800 ms |
| Audit table (50 rows, last 24h) | < 500 ms | > 1.2 s |
| Audit table (50 rows, last 90d) | < 1 s | > 3 s |
| Event drawer | < 200 ms | > 500 ms |
| Export (100K rows CSV) | < 5 min | > 15 min |
| Full page initial load | < 1 s | > 2.5 s |

**Index requirements:** `(timestamp, user_id)` · `(event_type, timestamp)` · `(entity_type, entity_id, timestamp)` · `(severity, timestamp)` — all on `audit_events` table (partitioned by month for performance)

---

## 9. States & Edge Cases

| State | Behaviour |
|---|---|
| Search returns 0 results | Empty state: "No audit events match your search" + suggestion to broaden date range |
| Date range > 90 days | Warning banner "Searches > 90 days are slower. Consider exporting." |
| Export > 500K rows | Error: "Export exceeds 500K rows. Please narrow your filters." |
| Live view: very high event rate | Throttle live prepend to max 10 new events/refresh (avoid overwhelming DOM) |
| User searches for own activity | Shows their own events; no restriction |
| Critical event (security.breach) | Immediate email alert to compliance@platform.com on write |
| Audit DB partition not yet available | "Logs from {period} are being archived. Try again in 24h." |

---

## 10. Keyboard Shortcuts

| Key | Action |
|---|---|
| `F` | Focus search |
| `L` | Toggle live view |
| `E` | Export |
| `1`–`5` | Switch tabs |
| `↑` / `↓` | Navigate rows |
| `Enter` | Open event drawer |
| `Esc` | Close drawer / modal |
| `?` | Keyboard shortcuts help |

---

## 11. Template Files

| File | Purpose |
|---|---|
| `exec/audit_log.html` | Full page shell |
| `exec/partials/audit_kpi.html` | KPI strip |
| `exec/partials/audit_table.html` | Audit event table + pagination |
| `exec/partials/audit_live_rows.html` | Live mode prepend rows |
| `exec/partials/event_drawer.html` | Event detail drawer |
| `exec/partials/export_audit_modal.html` | Export modal |

---

## 12. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `SearchInput` | §4.2 (with prefix syntax) |
| `FilterBar` | §4.3 |
| `TabBar` | §4.4 |
| `AuditEventTable` | §4.5 |
| `SeverityBadge` | §4.5 |
| `EventTypeBadge` | §4.5 |
| `LiveViewToggle` | §4.6 |
| `DrawerPanel` | §5.1 |
| `JSONDiffViewer` | §5.1 Section C |
| `ModalDialog` | §6.1 |
| `PaginationStrip` | §4.5 |
