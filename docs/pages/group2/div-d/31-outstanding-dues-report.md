# 31 — Outstanding Dues Report

- **URL:** `/group/finance/collection/outstanding/`
- **Template:** `portal_base.html`
- **Priority:** P2
- **Role:** Fee Collection Head G3 · Finance Manager G1 · CFO G1

---

## 1. Purpose

The Outstanding Dues Report provides a comprehensive, exportable report of all unpaid student fees across branches, used for management review, board presentations, and statutory audit support. Unlike the Defaulter Tracker (Page 29) which is an action-oriented operational tool, this page is the formal reporting layer — formatted for external presentation.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Group Fee Collection Head | G3 | Full read + export |
| Group Finance Manager | G1 | Full read + export |
| Group CFO | G1 | Full read + export |
| Group Internal Auditor | G1 | Read |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Finance → Fee Collection → Outstanding Dues Report
```

### 3.2 Page Header
- **Title:** `Outstanding Dues Report`
- **Subtitle:** `As of [Date] · Total Outstanding: ₹[X]`
- **Right-side controls:** `[AY ▾]` `[As-of Date ▾]` `[Branch ▾]` `[Student Type ▾]` `[Export PDF ↓]` `[Export Excel ↓]`

---

## 4. Ageing Summary Table (Group Level)

| Age Bucket | Students | Amount | % of Total Outstanding |
|---|---|---|---|
| Current (not yet due) | [N] | ₹ | % |
| 0–30 Days | [N] | ₹ | % |
| 31–60 Days | [N] | ₹ | % |
| 61–90 Days | [N] | ₹ | % |
| > 90 Days | [N] | ₹ | % |
| **Total** | **[N]** | **₹** | **100%** |

---

## 5. Branch-Level Outstanding Table

| Column | Type | Sortable |
|---|---|---|
| Branch | Text | ✅ |
| Total Students with Dues | Count | ✅ |
| Total Outstanding | ₹ | ✅ |
| 0–30 Days | ₹ | ✅ |
| 31–60 Days | ₹ | ✅ |
| >60 Days | ₹ | ✅ |
| % of Branch Demand | % | ✅ |

**Filters:** Branch · Student Type · Age Bucket
**Pagination:** 25 rows/page

---

## 6. Fee Component Outstanding Breakdown

| Fee Component | Outstanding | % of Component Demand |
|---|---|---|
| Tuition Fee | ₹ | % |
| Hostel Fee | ₹ | % |
| Mess Fee | ₹ | % |
| Transport Fee | ₹ | % |
| Coaching Fee | ₹ | % |
| **Total** | **₹** | **%** |

---

## 7. Charts

### 7.1 Outstanding by Branch (Bar)
### 7.2 Ageing Distribution (Donut)

---

## 8. Export Formats

| Format | Content |
|---|---|
| PDF | Formatted ageing report — suitable for board presentation |
| Excel | Raw data with all students, branches, and amounts |
| CSV | Machine-readable for accounting software import |

---

## 9. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Export | "Outstanding dues report exported." | Info | 3s |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton tables |
| Date change | Tables skeleton |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/finance/collection/outstanding/` | JWT (G1+) | Ageing summary |
| GET | `/api/v1/group/{id}/finance/collection/outstanding/branch/` | JWT (G1+) | Branch breakdown |
| GET | `/api/v1/group/{id}/finance/collection/outstanding/components/` | JWT (G1+) | Component breakdown |
| GET | `/api/v1/group/{id}/finance/collection/outstanding/export/?format=pdf` | JWT (G1+) | Export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Date change | `change` | GET `.../outstanding/?as_of=` | `#outstanding-body` | `innerHTML` |
| Branch filter | `change` | GET `.../outstanding/?branch=` | `#branch-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
