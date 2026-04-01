# 19 — Mess Menu Manager

> **URL:** `/group/hostel/mess/menu/`
> **File:** `19-mess-menu-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Mess Manager (primary) · Hostel Director (view + approve) · Welfare Officer (view)

---

## 1. Purpose

Centralized weekly mess menu management across all hostel campuses. Branch-level mess supervisors submit weekly menus (breakfast/lunch/snacks/dinner for each day of the week) through their branch portal; the Group Mess Manager reviews and approves them here. Rejected menus are sent back with revision notes.

The Mess Manager also creates standardized menu templates that branches can use as a base, ensuring nutritional adequacy and variety standards are met group-wide.

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Mess Operations  ›  Menu Manager
```

### 2.2 Page Header
- **Title:** `Mess Menu Manager`
- **Week selector:** Current week (Mon–Sun) with Previous / Next navigation
- **Subtitle:** `Week of [date range] · [N] Branches · [N] Menus Approved · [N] Pending Review · [N] Not Submitted`
- **Right controls:** `+ Create Template` · `Bulk Approve` · `Export`

---

## 3. Weekly Menu Approval Table

**Columns:**
| Column | Sortable |
|---|---|
| Branch | ✅ |
| Submitted By | ✅ |
| Submitted At | ✅ |
| Days Complete | ✅ (7/7, 5/7, etc.) |
| Status | ✅ (Approved / Pending / Revision Requested / Not Submitted) |
| Last Audited Score | ✅ |
| Actions | ❌ (Review · Approve · Request Revision) |

**Bulk Approve:** Select all Pending menus that meet nutritional criteria → Approve All Selected.

---

## 4. Menu Review Drawer: `mess-menu-review`
- **Trigger:** Table → Review
- **Width:** 680px
- **Content:** 7-day grid
  - Rows: Day (Mon–Sun)
  - Columns: Breakfast · Mid-Morning Snack · Lunch · Evening Snack · Dinner
  - Each cell: Dish name(s) + any nutritional note
- **Nutrition Check Panel:** Protein days (≥ 4 days/week with protein source) · Fruits included (≥ 3 days) · Variety score (no dish repeated > 2× per week) — auto-calculated
- **Approve/Request Revision:** Revision note (textarea) if requesting changes
- **Nutrition Warnings:** Auto-flags if same item appears > 2× in a week or protein days < 4

---

## 5. Menu Template Manager

> Group-level standard menus that branches can import as a base.

**Columns:** Template Name · Created By · Season (Monsoon/Winter/Summer/All-year) · Approved · [Use in Branch / Edit / Archive]

**Create Template:** Same 7-day grid as review drawer.

---

## 6. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Menu approved | "Weekly menu for [Branch] — week of [date] approved." | Success | 4s |
| Revision requested | "Revision requested for [Branch] menu. Supervisor notified." | Info | 4s |
| Bulk approved | "[N] menus approved." | Success | 4s |
| Template created | "Menu template '[Name]' created." | Success | 4s |

---

## 7. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/mess/menus/?week_start={date}` | JWT (G3+) | Weekly menus across branches |
| GET | `/api/v1/group/{group_id}/hostel/mess/menus/{id}/` | JWT (G3+) | Menu detail (7-day grid) |
| POST | `/api/v1/group/{group_id}/hostel/mess/menus/{id}/approve/` | JWT (G3+) | Approve menu |
| POST | `/api/v1/group/{group_id}/hostel/mess/menus/{id}/request-revision/` | JWT (G3+) | Request revision |
| POST | `/api/v1/group/{group_id}/hostel/mess/menus/bulk-approve/` | JWT (G3+) | Bulk approve |
| GET | `/api/v1/group/{group_id}/hostel/mess/templates/` | JWT (G3+) | Menu templates |
| POST | `/api/v1/group/{group_id}/hostel/mess/templates/` | JWT (G3+) | Create template |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
