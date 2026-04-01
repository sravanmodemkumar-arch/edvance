# 26 — Maintenance Request Tracker

> **URL:** `/group/ops/facilities/maintenance/`
> **File:** `26-maintenance-request-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 · Operations Manager G3 · Branch Coordinator G3 (own branches) · Zone roles (zone)

---

## 1. Purpose

Full lifecycle tracking of maintenance requests from all branch campuses. Covers everything
from a broken classroom fan to a structural safety issue. Priority triage ensures Critical
issues get immediate attention. Tracks assignment, progress, cost, and resolution.

---

## 2. Priority Levels & SLA

| Priority | Description | Response SLA | Resolution SLA |
|---|---|---|---|
| Critical | Safety hazard, structural damage, complete system failure | 1 hour | 4 hours |
| High | Major classroom/hostel disruption, plumbing failure | 4 hours | 24 hours |
| Medium | Minor disruption, non-urgent repairs | 24 hours | 72 hours |
| Low | Cosmetic repairs, non-urgent improvements | 48 hours | 14 days |

---

## 3. Categories

Electrical · Plumbing · Civil / Structural · HVAC / AC / Fans · IT Infrastructure / Internet · Security System / CCTV · Furniture · Flooring / Painting · Water Supply / Tank · Generator / Power Backup · Hostel Specific · Transport (Campus) · Other

---

## 4. Page Layout

### 4.1 Breadcrumb
```
Group HQ  ›  Facilities  ›  Maintenance Tracker
```

### 4.2 Page Header
```
Maintenance Request Tracker            [+ Raise Ticket]  [Export ↓]
[N] open · [N] Critical · [N] resolved this month
```

### 4.3 Status Tabs
```
[All]  [Open (N)]  [Acknowledged (N)]  [In Progress (N)]  [Overdue SLA (N)]  [Resolved (N)]  [Closed (N)]
```

### 4.4 Summary Strip
| Card | Value |
|---|---|
| Critical Open | Count (pulsing red if >0) |
| Overdue SLA | Count |
| Avg Resolution Time | Days |
| Cost This Month | ₹ total maintenance spend |

---

## 5. Search & Filters

**Search:** Ticket ID, branch name, category, description. 300ms debounce.

**Filters:** Category · Priority · Status · Branch · Zone · Assigned To · Date range · Has Photos

---

## 6. Maintenance Table

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| ☐ | Checkbox | |
| Ticket ID | ✅ | MNT-YYYY-NNNNN |
| Category | ✅ | Colour badge |
| Priority | ✅ | Critical red · High orange · Medium yellow · Low grey |
| Branch | ✅ | |
| Zone | ✅ | |
| Summary | ✅ | First 80 chars |
| Raised By | ✅ | |
| Raised Date | ✅ | |
| Response SLA | ✅ | Timer — red if breached |
| Assigned To | ✅ | Name or "Unassigned" (red) |
| Est. Cost | ✅ | ₹ |
| Status | ✅ | |
| Actions | — | View · Assign · Update · Resolve |

**Default sort:** Priority ascending (Critical first), then Age descending.

**Pagination:** 25/page.

---

## 7. Raise Ticket Drawer

- **Width:** 560px
- **Fields:**
  | Field | Type | Validation |
  |---|---|---|
  | Branch | Searchable select | Required |
  | Building | Select (from branch buildings) | Required |
  | Category | Select | Required |
  | Priority | Select | Required |
  | Summary | Text | Required · max 120 chars |
  | Description | Textarea | Required · min 30 chars |
  | Photos | File upload | Up to 10 · 10MB each |
  | Assign To | Select (optional) | Maintenance staff or vendor |
  | Estimated Cost | Number | Optional |

---

## 8. Maintenance Detail Drawer

- **Width:** 640px
- **Tabs:** Details · Progress · Photos · Cost · History

**Details tab:** Full info, SLA timers, assigned to.

**Progress tab:**
Timeline of updates: acknowledged → assigned → work in progress → completed.
[Add Progress Update] button: status + notes + photos.

**Photos tab:** Before photos (at creation) + after photos (at resolution). Lightbox view.

**Cost tab:**
- Estimated cost (at creation)
- Actual cost (at resolution)
- Invoice upload field
- Vendor/contractor details

**History tab:** Immutable event log.

**Actions (for assignee/Ops Mgr/COO):**
- [Acknowledge] → starts response SLA
- [Assign to Vendor/Staff]
- [Add Progress Update]
- [Mark Resolved] → requires actual cost + after photos + resolution description

---

## 9. Bulk Actions

| Action | Roles |
|---|---|
| Bulk Assign | COO/Ops Mgr |
| Export CSV | COO/Ops Mgr |
| Mark Multiple Resolved | COO/Ops Mgr |

---

## 10. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Ticket created | "Maintenance ticket MNT-[ID] created" | Success · 4s |
| Critical created | "Critical ticket created — COO and Facilities notified immediately" | Warning · manual |
| Assigned | "Ticket assigned to [Name]" | Success · 4s |
| Resolved | "Ticket MNT-[ID] resolved and closed" | Success · 4s |
| SLA breached | "SLA breach: MNT-[ID] Critical — [N]h overdue" | Error · manual |

---

## 11. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No open tickets | "No open maintenance tickets" | — |
| No critical | "No critical maintenance issues" | — |
| No results | "No tickets match search" | [Clear Filters] |

---

## 12. Loader States

Page load: Skeleton summary + tabs + table. Critical pulsing badge: always visible once loaded.

---

## 13. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Coordinator G3 | Zone Ops G3 |
|---|---|---|---|---|
| All branches | ✅ | ✅ | Own only | Zone only |
| [Raise Ticket] | ✅ | ✅ | ✅ | ✅ |
| [Assign] | ✅ | ✅ | ❌ | ✅ zone |
| [Mark Resolved] | ✅ | ✅ | ❌ | ✅ zone |
| Cost tab | ✅ | ✅ | ❌ | ❌ |
| Export | ✅ | ✅ | ❌ | ❌ |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/facilities/maintenance/` | JWT (G3+) | Ticket list |
| POST | `/api/v1/group/{id}/facilities/maintenance/` | JWT (G3+) | Create ticket |
| GET | `/api/v1/group/{id}/facilities/maintenance/{tid}/` | JWT (G3+) | Detail |
| POST | `/api/v1/group/{id}/facilities/maintenance/{tid}/acknowledge/` | JWT (G3+) | Acknowledge |
| POST | `/api/v1/group/{id}/facilities/maintenance/{tid}/assign/` | JWT (G3+) | Assign |
| POST | `/api/v1/group/{id}/facilities/maintenance/{tid}/update/` | JWT (G3+) | Progress update |
| POST | `/api/v1/group/{id}/facilities/maintenance/{tid}/resolve/` | JWT (G3+) | Resolve |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch | `click` | `/api/.../maintenance/?status={}` | `#mnt-table-section` | `innerHTML` |
| Search | `input delay:300ms` | `/api/.../maintenance/?q={}` | `#mnt-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../maintenance/?filters={}` | `#mnt-table-section` | `innerHTML` |
| Sort | `click` | `/api/.../maintenance/?sort={}` | `#mnt-table-section` | `innerHTML` |
| Open detail | `click` | `/api/.../maintenance/{id}/` | `#drawer-body` | `innerHTML` |
| Critical badge poll | `every 60s` | `/api/.../facilities/kpi-cards/` | `#critical-badge` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
