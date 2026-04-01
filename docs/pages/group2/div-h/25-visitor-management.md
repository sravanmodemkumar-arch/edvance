# 25 — Visitor Management

> **URL:** `/group/hostel/security/visitors/`
> **File:** `25-visitor-management.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Hostel Security Coordinator (primary) · Parent Visit Coordinator (view) · Boys/Girls Coordinators

---

## 1. Purpose

Digital visitor register for all hostel campuses. Replaces paper-based visitor books with a searchable, auditable digital register. Every visitor entry — pre-registered or walk-in — is logged with ID proof details, purpose, hosteler visited, entry time, and exit time.

Girls hostel visitor protocols are stricter: male visitors (including fathers) require additional verification and are permitted only during official parent visit days unless pre-approved. The system enforces this through the visitor entry form — attempting to log a male visitor to a girls hostel outside a scheduled parent visit day triggers a mandatory override justification.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Security  ›  Visitor Management
```

### 2.2 Page Header
- **Title:** `Visitor Management`
- **Subtitle:** `Today: [N] Entries · [N] Currently Inside · [N] Unauthorized`
- **Right controls:** `+ New Entry` · `Pre-register Visitor` · `Advanced Filters` · `Export`

---

## 3. KPI Cards (Today)

| Card | Metric | Colour Rule |
|---|---|---|
| Total Entries (Today) | | Blue |
| Currently Inside | Visitors who have not yet checked out | Yellow > 0 |
| Boys Hostel Entries | | Blue |
| Girls Hostel Entries | | Blue |
| Unauthorized Entries | Visitors without proper clearance | Red > 0 |
| Overstay (> 4 hours) | Visitors who have been inside > 4 hours | Amber > 0 |

---

## 4. Visitor Register Table

**Default view:** Today's entries. Date picker to change date.

**Search:** Visitor name, ID number, hosteler name. 300ms debounce.

**Filters:** Branch · Hostel Type (Boys/Girls) · Date range · Status (Inside/Exited/Denied) · Pre-registered vs Walk-in.

**Columns:**
| Column | Sortable |
|---|---|
| Entry # | ✅ |
| Branch | ✅ |
| Hostel | ✅ |
| Visitor Name | ✅ |
| Relation to Hosteler | ✅ |
| Hosteler Name | ✅ |
| ID Type + # | ✅ (partially masked) |
| Entry Time | ✅ |
| Exit Time | ✅ (blank if still inside) |
| Pre-registered? | ✅ |
| Authorized? | ✅ (✅ / ❌ Unauthorized) |
| Actions | ❌ |

---

## 5. Drawers

### 5.1 Drawer: `visitor-entry-create`
- **Trigger:** + New Entry
- **Width:** 520px
- **Fields:**
  - Branch
  - Hostel Type (Boys / Girls)
  - Visitor Name
  - Relation to Hosteler (Father / Mother / Guardian / Sibling / Other)
  - ID Proof Type (Aadhaar / PAN / Passport / DL)
  - ID Proof Number
  - Hosteler (search autocomplete)
  - Purpose of Visit
  - Entry Time (auto-filled with now; editable)
  - Pre-registered? (checkbox — if yes, system validates against pre-registration DB)
- **Girls hostel + male visitor guard:** If Hostel = Girls and Relation = Father/Male Guardian/Brother → mandatory field: "Is this a scheduled parent visit day?" (Yes/No). If No → "Override reason required" (textarea) + [Notify Girls Coordinator] (auto-checked).

### 5.2 Drawer: `visitor-detail`
- **Width:** 480px
- **Content:** All entry fields + entry/exit times + authorization status + log (who created this entry) + [Mark Exit] button

### 5.3 Drawer: `visitor-preregister`
- **Trigger:** Pre-register Visitor
- **Width:** 520px
- **Fields:** Parent/Guardian name · Relation · Mobile · ID proof · Hosteler name · Valid from/to dates · Biometric registration date · Notes

### 5.4 Modal: Deny Entry
- **Trigger:** Inline with new entry form if unauthorized trigger detected
- **Fields:** Reason for denial (required) · Notify security supervisor (checkbox)

---

## 6. Pre-registered Visitor List

> All parents/guardians cleared for hostel entry.

**Columns:** Name | Relation | Hosteler | Branch | Hostel | Valid From | Valid To | Biometric Status | Last Visit | Actions

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Entry logged | "Visitor entry logged for [Visitor Name] visiting [Hosteler]." | Success | 3s |
| Exit logged | "Exit recorded for [Visitor Name]. Duration: [N] minutes." | Info | 3s |
| Unauthorized entry flagged | "Unauthorized visitor entry flagged at [Branch] Girls Hostel. Girls Coordinator notified." | Warning | 6s |
| Pre-registration saved | "[Visitor Name] pre-registered for hostel visits." | Success | 4s |

---

## 8. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/visitors/` | JWT (G3+) | Visitor register (paginated, filtered) |
| POST | `/api/v1/group/{group_id}/hostel/visitors/` | JWT (G3+) | Log visitor entry |
| PATCH | `/api/v1/group/{group_id}/hostel/visitors/{id}/exit/` | JWT (G3+) | Log exit |
| GET | `/api/v1/group/{group_id}/hostel/visitors/preregistered/` | JWT (G3+) | Pre-registered visitor list |
| POST | `/api/v1/group/{group_id}/hostel/visitors/preregister/` | JWT (G3+) | Pre-register visitor |
| GET | `/api/v1/group/{group_id}/hostel/visitors/kpis/today/` | JWT (G3+) | Today's KPI cards |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
