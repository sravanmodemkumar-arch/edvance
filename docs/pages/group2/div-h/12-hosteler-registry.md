# 12 — Hosteler Registry

> **URL:** `/group/hostel/hostelers/`
> **File:** `12-hosteler-registry.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Hostel Director (primary owner) · Boys/Girls Coordinators · All hostel roles (view)

---

## 1. Purpose

The Hosteler Registry is the master searchable database of every current and past hosteler across all branches and all academic years. Each row represents a single hosteler's record — personal identity, gender, branch, room assignment, hostel type (AC/Non-AC), fee plan, medical conditions, welfare history, and current status (Active / On Leave / Exited).

This is the authoritative source of truth for hosteler data at the group level. Branch-level warden portals read from and write to this registry. Any action on a hosteler — room transfer, fee hold, welfare incident, discipline case, medical visit, or exit — is linked to their registry record. Scale: a 50-branch group may have 10,000–30,000 active hosteler records plus historical alumni.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Hostel Director | G3 | Full — all hostelers, all branches, both genders | Create, edit, exit |
| Group Boys Hostel Coordinator | G3 | Full — boys only | Edit boys records; no girls data |
| Group Girls Hostel Coordinator | G3 | Full — girls only | Edit girls records; no boys data |
| Group Hostel Welfare Officer | G3 | Read — all | Cannot edit profile; can add welfare note |
| Group Hostel Admission Coordinator | G3 | Read + Create (new admissions) | Create on seat allocation |
| Group Hostel Fee Manager | G3 | Read — for fee assignment | Cannot edit other fields |
| Group Hostel Medical Coordinator | G3 | Read + medical fields only | Can update medical condition |
| Group Hostel Discipline Committee | G3 | Read — for case context | Cannot edit |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Hosteler Registry
```

### 3.2 Page Header
- **Title:** `Group Hosteler Registry`
- **Subtitle:** `[N] Active Hostelers · [N] On Leave · [N] Exited (AY) · AY [current]`
- **Right controls:** `+ Add Hosteler` · `Bulk Actions ▾` · `Advanced Filters` · `Export`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Hostelers with no room assignment | "[N] hostelers are admitted but have no room assigned." | Amber |
| Hostelers with outstanding fee > 60 days | "[N] hostelers have outstanding fees for > 60 days." | Amber |
| Hostelers on medical watch with overdue check | "[N] hostelers on medical watch have missed their scheduled check." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Active Hostelers | Current enrolled | Blue |
| Boys Hostelers | Male active | Blue |
| Girls Hostelers | Female active | Blue |
| AC Hostelers | In AC rooms | Blue |
| Non-AC Hostelers | In Non-AC rooms | Blue |
| On Leave Today | Temporary leave approved | Yellow > 0 |

---

## 5. Main Table — Hosteler Registry

**Search:** Full-text — hosteler name, roll number, room number, parent name, phone. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Gender | Radio | All / Boys / Girls |
| Hostel Type | Checkbox | AC / Non-AC |
| Status | Checkbox | Active / On Leave / Exited / Suspended from Hostel |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / HEC / Foundation |
| Class | Multi-select | 6 through 12 |
| Special Needs | Checkbox | Show only special needs hostelers |
| Fee Status | Radio | Any / Current / Defaulter (30d+) / Fee Hold |
| Medical Watch | Checkbox | On medical watch |
| Admission Date Range | Date range picker | |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Photo | ❌ | Thumbnail or initials avatar |
| Name | ✅ | Link → view drawer |
| Roll No | ✅ | Branch-assigned roll number |
| Gender | ✅ | M/F badge |
| Class / Stream | ✅ | e.g., "Class 11 – MPC" |
| Branch | ✅ | |
| Room # | ✅ | Room + Bed (e.g., "B-204 / Bed A") |
| Hostel Type | ✅ | AC / Non-AC badge |
| Status | ✅ | Active / On Leave / Exited |
| Fee Status | ✅ | ✅ Current / ⚠ Defaulter / 🔴 Fee Hold |
| Medical | ✅ | ✅ Healthy / ⚠ Medical Watch |
| Admission Date | ✅ | |
| Actions | ❌ | View · Edit · Transfer · Exit |

**Bulk actions:** Export selected · Bulk send fee reminder · Bulk mark on leave.

**Pagination:** Server-side · 25/page · 10/25/50/All.

---

## 6. Drawers

### 6.1 Drawer: `hosteler-detail` — View Hosteler
- **Trigger:** Name link or Actions → View
- **Width:** 640px
- **Tabs:** Profile · Room · Fee · Welfare · Medical · Discipline · History
- **Profile:** Photo, name, roll no, gender, DOB, class, stream, branch, admission date, special needs flag, parent contacts
- **Room:** Current room, bed, hostel type, AC/Non-AC, room-mates (names)
- **Fee:** Plan, monthly amount, paid/outstanding, last payment date, waiver history
- **Welfare:** Open + last 5 closed welfare incidents, severity distribution
- **Medical:** Medical conditions, current medications, last medical visit, on medical watch flag
- **Discipline:** Open + closed discipline cases (summary)
- **History:** All status changes (room transfers, leave, re-admissions, exits) with timestamps

### 6.2 Drawer: `hosteler-create` — Add Hosteler
- **Trigger:** + Add Hosteler
- **Width:** 640px
- **Tabs:** Personal · Parent / Guardian · Academic · Hostel Preferences · Medical
- **Personal:** Full name, gender (locked after save), DOB, Aadhaar, photo upload
- **Parent/Guardian:** Father name, mother name, emergency contact, address, relation
- **Academic:** Branch, class, stream, roll number, admission date
- **Hostel Preferences:** AC/Non-AC preference, gender-appropriate hostel auto-assigned, dietary restrictions, room-sharing notes
- **Medical:** Known medical conditions, allergies, medications, special needs (checkbox)
- **Validation:** Gender cannot be changed after first save; room must match gender; AC/Non-AC must match available capacity

### 6.3 Drawer: `hosteler-edit` — Edit Hosteler
- **Trigger:** Actions → Edit
- **Width:** 640px (same tabs as create, pre-populated)
- **Read-only fields:** Name, gender, DOB, branch (after admission) — change via transfer flow
- **Editable:** Room, fee plan, medical flags, stream, class, parent contacts

### 6.4 Drawer: `hosteler-transfer` — Room / Branch Transfer
- **Trigger:** Actions → Transfer
- **Width:** 520px
- **Fields:** Transfer Type (Room within branch / Branch transfer) · From Branch/Room · To Branch · To Room (dropdown of available rooms matching gender) · Effective Date · Reason · Notify Parent (checkbox)
- **Validation:** Target room must match gender; capacity check required

### 6.5 Modal: `hosteler-exit` — Exit Hosteler
- **Trigger:** Actions → Exit
- **Width:** 480px
- **Fields:** Exit Date · Exit Type (Academic completion / Transfer out / Voluntary exit / Disciplinary expulsion / Medical reason) · Clearance Checklist (Room cleared ✓ / Fees settled ✓ / ID returned ✓ / Equipment returned ✓) · Notify Parent (checkbox)
- **Warning:** "This action is irreversible. Hosteler record will be archived with exit date."

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Hosteler added | "[Name] added to hosteler registry." | Success | 4s |
| Profile updated | "[Name]'s profile updated." | Success | 4s |
| Transfer completed | "[Name] transferred to [Room/Branch]." | Success | 4s |
| Exited | "[Name] exited hostel on [date]. Record archived." | Info | 5s |
| Bulk export | "Hosteler export is being prepared. You'll be notified when ready." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No hostelers at all | "No Hostelers Found" | "No hosteler records exist yet." | [+ Add Hosteler] |
| No results for filter | "No Hostelers Match Filters" | "Adjust branch, gender, or status filters." | [Clear Filters] |
| No results for search | "No Hostelers Found for '[term]'" | "Check the name, roll number, or room number." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + table skeleton (15 rows × 12 columns) |
| Filter/search | Table body skeleton |
| Hosteler detail drawer | 640px drawer skeleton; tabs load lazily |
| Transfer confirm | Spinner on Confirm; table row updates in-place |

---

## 10. Role-Based UI Visibility

| Element | Hostel Director G3 | Boys Coord G3 | Girls Coord G3 | Welfare G3 | Admission Coord G3 | Fee Manager G3 | Medical Coord G3 |
|---|---|---|---|---|---|---|---|
| See all genders | ✅ | Boys only | Girls only | ✅ | ✅ | ✅ | ✅ |
| Add Hosteler | ✅ | ✅ Boys | ✅ Girls | ❌ | ✅ | ❌ | ❌ |
| Edit Profile | ✅ | ✅ Boys | ✅ Girls | ❌ | ❌ | Fee fields only | Medical fields only |
| Transfer | ✅ | ✅ Boys | ✅ Girls | ❌ | ✅ | ❌ | ❌ |
| Exit | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Export | ✅ | ✅ Boys | ✅ Girls | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/hostelers/` | JWT (G3+) | Paginated, filtered hosteler list |
| GET | `/api/v1/group/{group_id}/hostel/hostelers/{id}/` | JWT (G3+) | Hosteler full profile |
| POST | `/api/v1/group/{group_id}/hostel/hostelers/` | JWT (G3+) | Create hosteler |
| PATCH | `/api/v1/group/{group_id}/hostel/hostelers/{id}/` | JWT (G3+) | Update hosteler (scoped by role) |
| POST | `/api/v1/group/{group_id}/hostel/hostelers/{id}/transfer/` | JWT (G3+) | Transfer room/branch |
| POST | `/api/v1/group/{group_id}/hostel/hostelers/{id}/exit/` | JWT (G3+) | Exit hosteler |
| GET | `/api/v1/group/{group_id}/hostel/hostelers/kpis/` | JWT (G3+) | KPI card values |
| GET | `/api/v1/group/{group_id}/hostel/hostelers/export/` | JWT (G3+) | Async CSV/XLSX export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../hostelers/?q={val}` | `#hosteler-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../hostelers/?{filters}` | `#hosteler-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../hostelers/?page={n}` | `#hosteler-table-section` | `innerHTML` |
| Sort | `click` on header | GET `.../hostelers/?sort={col}&dir={asc/desc}` | `#hosteler-table-section` | `innerHTML` |
| Open view drawer | `click` on name | GET `.../hostelers/{id}/` | `#drawer-body` | `innerHTML` |
| Submit create | `click` | POST `.../hostelers/` | `#hosteler-table-section` | `innerHTML` |
| Transfer confirm | `click` | POST `.../hostelers/{id}/transfer/` | `#hosteler-row-{id}` | `outerHTML` |
| Exit confirm | `click` | POST `.../hostelers/{id}/exit/` | `#hosteler-table-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
