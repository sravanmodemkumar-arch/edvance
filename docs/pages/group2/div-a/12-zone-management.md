# 12 — Zone Management

> **URL:** `/group/gov/zones/`
> **File:** `12-zone-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 · CEO G4 (full) · President G4 · VP G4 (view) · Trustee G1 · Advisor G1 (read)

---

## 1. Purpose

Zone management for large institution groups. Large groups (20–50 branches) use an intermediate
zone layer between Group HQ and individual branches. Each zone contains 10–15 branches and is
managed by a Zone Director, Zone Academic Coordinator, and Zone Operations Manager.

Small groups (5–10 branches) do not have zones — they see a contextual empty state explaining this.

**Zone-level roles (Division G):**
- Zone Director (G4 — manages a zone of 10–15 branches)
- Zone Academic Coordinator (G3)
- Zone Operations Manager (G3)

This page manages zone creation, branch assignment, and zone staff assignment at the Group HQ level.

---

## 2. Role Access

| Role | Level | Can View | Can Create | Can Edit | Can Delete |
|---|---|---|---|---|---|
| Chairman | G5 | ✅ | ✅ | ✅ | ✅ |
| MD | G5 | ✅ | ✅ | ✅ | ✅ |
| CEO | G4 | ✅ | ✅ | ✅ | ❌ |
| President | G4 | ✅ View | ❌ | ❌ | ❌ |
| VP | G4 | ✅ View | ❌ | ❌ | ❌ |
| Trustee | G1 | ✅ Read | ❌ | ❌ | ❌ |
| Advisor | G1 | ✅ Read | ❌ | ❌ | ❌ |
| Exec Secretary | G3 | ❌ | ❌ | ❌ | ❌ |

**Small group guard:** If `group.type == 'small'` → render empty state:
"Zone management is available for large institution groups (20+ branches). Your group currently
operates without zones — Group HQ directly manages all branches."

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Zone Management
```

### 3.2 Page Header
```
Zone Management                                        [+ Create Zone]  [Export ↓]
[N] zones · [N] branches assigned · [N] unassigned    (Chairman/MD/CEO only)
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Zones | N |
| Branches Assigned | N / 50 total |
| Unassigned Branches | N (highlighted yellow if >0) |
| Zone Directors Assigned | N / N zones |
| Avg Branches per Zone | N.N |

---

## 4. Zones Table

**Search:** Zone name, Zone Director name. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| State Coverage | Multi-select | States covered by zone |
| Performance | Select | High (>85) · Mid (70–85) · Low (<70) |
| Director Assigned | Checkbox | Show only zones without assigned director |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Zone Name | Text + link | ✅ | Opens zone detail drawer |
| Zone Code | Text | ✅ | e.g. ZONE-AP-01 |
| States | Tags | ❌ | States covered by this zone |
| Branches | Number + link | ✅ | Count — click opens list of branches |
| Students | Number | ✅ | Total students in zone |
| Zone Director | Text | ✅ | Name or "⚠ Not assigned" (red if empty) |
| Academic Coord. | Text | ✅ | Name or "Not assigned" |
| Ops Manager | Text | ✅ | Name or "Not assigned" |
| Avg Score % | Number + bar | ✅ | Academic average across zone branches |
| Avg Fee % | Number + bar | ✅ | Fee collection average |
| Performance Score | Number | ✅ | Composite 0–100 |
| Actions | — | ❌ | View · Edit · Delete |

**Default sort:** Zone Name ascending.

**Pagination:** Server-side · Default 10/page (zones are few — typically 3–5 per large group).

**Row select + bulk export.**

**Row actions:**

| Action | Visible To | Notes |
|---|---|---|
| View | All | Opens `zone-edit` drawer in view mode |
| Edit | Chairman/MD/CEO | Opens `zone-edit` drawer in edit mode |
| Delete | Chairman/MD | Confirm modal — requires unassigning all branches first |

---

## 5. Unassigned Branches Panel

**Display:** Shown below the zones table only if unassigned branches exist.
Collapsible panel — yellow background header, count badge.

**Content:** Mini table of unassigned branches: Name · City · Students · [Assign to Zone] dropdown.

**[Assign to Zone] dropdown:** Select from existing zones → inline assign (no drawer needed).

---

## 6. Drawers & Modals

### 6.1 Drawer: `zone-create` — Create Zone
- **Trigger:** [+ Create Zone] header button
- **Width:** 560px
- **Tabs:** Profile · Branches · Leadership

#### Tab: Profile
| Field | Type | Required | Validation |
|---|---|---|---|
| Zone Name | Text | ✅ | Min 3, max 100, unique in group |
| Zone Code | Text | ✅ | 4–10 alphanumeric, auto-suggested, unique |
| Description | Textarea | ❌ | Max 300 chars |
| States Covered | Multi-select | ✅ | At least 1 state |

#### Tab: Branches
| Field | Type | Required | Validation |
|---|---|---|---|
| Assign Branches | Multi-select with search | ✅ | Min 1, max 15 branches |
| Shows | Available branches (not yet in a zone) | — | |
| Preview count | Read-only | — | "X branches selected — X total students" |

> Branches already assigned to another zone appear greyed out with current zone shown.

#### Tab: Leadership
| Field | Type | Required | Validation |
|---|---|---|---|
| Zone Director | Search + select | ❌ | G4-level user assigned to group |
| Zone Academic Coordinator | Search + select | ❌ | G3 user |
| Zone Operations Manager | Search + select | ❌ | G3 user |

Note: Leadership can be assigned later. Zone can be created without it.

**Submit:** "Create Zone" — disabled until Profile + Branches tabs valid.

### 6.2 Drawer: `zone-edit` — Edit Zone
- **Width:** 560px — same tabs as create, pre-filled
- **Extra in Branches tab:** Can remove branches (confirmation: branch becomes unassigned)
- **Extra in Leadership tab:** Can change or remove leadership

### 6.3 Modal: `zone-delete-confirm`
- **Width:** 420px
- **Prerequisite check:** If zone has branches → "Cannot delete zone with assigned branches. Remove all branches from this zone first."
- **If empty:** "Delete [Zone Name]? This cannot be undone." + required reason
- **Buttons:** [Delete Zone] (danger) + [Cancel]

### 6.4 Modal: `reassign-branches`
- **Width:** 480px
- **Context:** Bulk reassign branches from one zone to another
- **Fields:** Select target zone (dropdown) · Optional note
- **Preview:** Shows branch list being moved
- **Buttons:** [Reassign] + [Cancel]

---

## 7. Zone Performance Chart

**Type:** Grouped bar chart — one group per zone.

**Metrics shown per zone:** Avg Score % · Avg Fee % · Performance Score.

**X-axis:** Zone names.

**Y-axis:** Percentage / Score (0–100).

**Tooltip:** Zone · Score: X · Fee: X% · Academic: X%.

**Export:** PNG.

---

## 8. Zone Branch Map (optional visual)

**Type:** Table-based matrix — branches as rows, zones as columns with checkmark.

Useful for large groups to see branch-zone allocation at a glance.

**Export:** CSV.

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Zone created | "Zone [Name] created with [N] branches" | Success | 4s |
| Zone updated | "Zone [Name] updated" | Success | 4s |
| Zone deleted | "Zone [Name] deleted" | Warning | 6s |
| Branch assigned to zone | "[Branch] assigned to [Zone]" | Success | 4s |
| Branch removed from zone | "[Branch] removed from [Zone]. Branch is now unassigned." | Warning | 6s |
| Leadership assigned | "[Name] assigned as Zone Director for [Zone]" | Info | 4s |
| Delete blocked (has branches) | "Remove all branches from [Zone] before deleting" | Error | Manual |

---

## 10. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| Small group (no zones) | "Zone management not applicable" | "Your group operates without zones. Group HQ directly manages all branches." | — |
| No zones created | "No zones set up" | "Create zones to organise branches for large-group management" | [+ Create Zone] |
| All branches assigned | "All branches assigned" | "Every branch is currently in a zone" | — |
| Unassigned branches > 0 | Shown inline in yellow panel | "N branches are not assigned to any zone" | [Assign] inline |

---

## 11. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (5 zone rows) |
| Table filter/search | Inline skeleton rows |
| Zone drawer open | Spinner in drawer |
| Zone create submit | Spinner in submit button |
| Unassigned branches panel | Shimmer on panel load |

---

## 12. Role-Based UI Visibility

| Element | Chairman/MD G5 | CEO G4 | President/VP G4 | Trustee/Advisor G1 |
|---|---|---|---|---|
| [+ Create Zone] | ✅ | ✅ | ❌ | ❌ |
| Edit row action | ✅ | ✅ | ❌ | ❌ |
| Delete row action | ✅ | ❌ | ❌ | ❌ |
| Assign Branch inline | ✅ | ✅ | ❌ | ❌ |
| Leadership fields in drawer | ✅ | ✅ | ❌ | ❌ |
| [Export] button | ✅ | ✅ | ❌ | ❌ |
| Performance chart | ✅ | ✅ | ✅ (read) | ✅ (read) |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/zones/` | JWT | All zones list |
| POST | `/api/v1/group/{id}/zones/` | JWT (G4+) | Create zone |
| GET | `/api/v1/group/{id}/zones/{zid}/` | JWT | Zone detail |
| PUT | `/api/v1/group/{id}/zones/{zid}/` | JWT (G4+) | Update zone |
| DELETE | `/api/v1/group/{id}/zones/{zid}/` | JWT (G5) | Delete zone |
| POST | `/api/v1/group/{id}/zones/{zid}/branches/` | JWT (G4+) | Assign branches to zone |
| DELETE | `/api/v1/group/{id}/zones/{zid}/branches/{bid}/` | JWT (G4+) | Remove branch from zone |
| GET | `/api/v1/group/{id}/branches/?zone=unassigned` | JWT | Unassigned branches |
| GET | `/api/v1/group/{id}/zones/performance-chart/` | JWT | Zone performance chart data |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Zone search | `input delay:300ms` | GET `.../zones/?q=` | `#zone-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../zones/?filters=` | `#zone-table-section` | `innerHTML` |
| Open zone drawer (view) | `click` | GET `.../zones/{id}/` | `#drawer-body` | `innerHTML` |
| Open zone drawer (edit) | `click` | GET `.../zones/{id}/edit-form/` | `#drawer-body` | `innerHTML` |
| Create zone submit | `submit` | POST `.../zones/` | `#drawer-body` | `innerHTML` |
| Inline branch assign | `change` | POST `.../zones/{zid}/branches/` | `#unassigned-row-{bid}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
