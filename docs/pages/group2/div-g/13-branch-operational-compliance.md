# 13 — Branch Operational Compliance Checklist

> **URL:** `/group/ops/compliance/`
> **File:** `13-branch-operational-compliance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 · Operations Manager G3 · Branch Coordinator G3 (own branches) · Zone roles (zone scope)

---

## 1. Purpose

Tracks operational compliance for every branch against a standard group-wide checklist.
Each checklist item is assigned a frequency (daily, weekly, monthly, termly, annual) and
weight. The compliance score drives the branch's overall operational health rating and
triggers escalations when critical items fail.

---

## 2. Compliance Checklist — Standard Items

| # | Item | Category | Frequency | Weight | Critical? |
|---|---|---|---|---|---|
| 1 | Daily attendance submitted by 9:30 AM | Academic | Daily | 10 | ✅ |
| 2 | Fee collection report submitted | Finance | Weekly | 8 | ✅ |
| 3 | All staff BGV completed | HR | Monthly | 15 | ✅ |
| 4 | POCSO training completion 100% | Safety | Monthly | 10 | ✅ |
| 5 | Fire extinguishers serviced | Facilities | Monthly | 8 | ✅ |
| 6 | CCTV operational (all cameras) | Safety | Weekly | 7 | ✅ |
| 7 | Fire drill conducted | Safety | Termly | 8 | ✅ |
| 8 | Coordinator visit completed | Operations | Monthly | 8 | ❌ |
| 9 | Parent-Teacher Meeting conducted | Academic | Termly | 6 | ❌ |
| 10 | Hostel roll call completed (hosteler branches) | Hostel | Daily | 10 | ✅ |
| 11 | Vehicle fitness certificate valid | Transport | Monthly | 8 | ✅ |
| 12 | First aid kit stocked | Safety | Monthly | 5 | ❌ |
| 13 | Grievances responded within SLA | Operations | Monthly | 8 | ✅ |
| 14 | Exam results published on time | Academic | Per-exam | 7 | ❌ |
| 15 | Building inspection certificate valid | Facilities | Annual | 7 | ✅ |

> Critical items: failure = immediate escalation to Group. Non-critical: tracked and reported.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Branch Compliance Checklist
```

### 3.2 Page Header
```
Branch Operational Compliance          [Configure Checklist]  [Export Report ↓]
Last evaluated: [timestamp] · Academic Year [current]
```

### 3.3 Summary Strip
| Card | Value |
|---|---|
| Group Avg Compliance | `83.2%` |
| Fully Compliant Branches | `22 / 50` |
| Critical Item Failures | `4` (red badge if >0) |
| Items Due This Week | `N` checklist items across all branches |

---

## 4. Search & Filters

**Search:** Branch name, checklist item. 300ms debounce.

**Advanced Filters:**
| Filter | Options |
|---|---|
| Zone | Multi-select |
| Category | Academic · Finance · HR · Safety · Facilities · Hostel · Transport · Operations |
| Compliance Score | Below 70% · 70–85% · Above 85% |
| Has Critical Failures | Checkbox |
| Branch Type | Day Scholar / Hostel / Both |
| Item Frequency | Daily · Weekly · Monthly · Termly · Annual |

---

## 5. Branch Compliance Table

**Default sort:** Compliance Score ascending (worst first).

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| ☐ | Checkbox | |
| Branch Name | ✅ | Link → `branch-compliance-detail` drawer |
| Zone | ✅ | |
| Overall Score | ✅ | Progress bar + %, colour-coded |
| Critical Failures | ✅ | Count, red if >0 |
| Items Passed | ✅ | X / 15 |
| Last Evaluated | ✅ | Date |
| Trend | ❌ | Sparkline (6 months) |
| Actions | — | View · Re-evaluate · Raise Escalation |

---

## 6. Checklist Heatmap View (toggle)

> Branch × checklist item grid.

- Rows: Branches
- Columns: Checklist items (abbreviated)
- Cell: ✅ Pass / ⚠ Due Soon / ❌ Fail / — Not Applicable

---

## 7. Branch Compliance Detail Drawer

- **Width:** 640px
- **Tabs:** Checklist · Score History · Actions

**Checklist tab:**
Table of all checklist items for this branch:
| Item | Category | Frequency | Due Date | Status | Last Checked | Evidence |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ✅/⚠/❌ | Date | View |

**Score History tab:**
- Bar chart: compliance score last 12 months
- Critical failures timeline

**Actions tab (COO/Ops Mgr):**
- [Override Item] (mark as compliant with documented exception)
- [Raise Escalation] (for critical failures)
- [Schedule Audit] (trigger coordinator visit for compliance check)

---

## 8. Checklist Configuration (COO only)

- Accessible via [Configure Checklist] button
- Add/edit/remove checklist items
- Set weight, frequency, critical flag
- Enable/disable items for specific branch types (e.g., hostel items only for hostel branches)
- Version history of checklist changes

---

## 9. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Item overridden | "Compliance override recorded with exception note" | Warning · 6s |
| Escalation raised | "Critical failure escalation raised" | Success · 4s |
| Audit scheduled | "Coordinator audit scheduled for [Branch]" | Success · 4s |
| Checklist updated | "Checklist configuration saved" | Success · 4s |

---

## 10. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No branches | "No branches found" | [Clear Filters] |
| All compliant | "All branches meeting compliance standards" | — |
| No checklist items | "No checklist configured" | [Configure Checklist] (COO) |

---

## 11. Loader States

Page load: Skeleton summary strip + table (5 rows).
Heat-map toggle: Skeleton grid.

---

## 12. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Coordinator G3 |
|---|---|---|---|
| All branches | ✅ | ✅ | Own only |
| [Configure Checklist] | ✅ | ❌ | ❌ |
| [Override Item] | ✅ | ✅ | ❌ |
| [Raise Escalation] | ✅ | ✅ | ✅ |
| Export | ✅ | ✅ | ❌ |

---

## 13. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/ops/compliance/` | JWT (G3+) | Branch compliance table |
| GET | `/api/v1/group/{id}/ops/compliance/heatmap/` | JWT (G3+) | Heatmap data |
| GET | `/api/v1/group/{id}/ops/compliance/branches/{branch_id}/` | JWT (G3+) | Branch detail |
| POST | `/api/v1/group/{id}/ops/compliance/branches/{branch_id}/override/` | JWT (G3+) | Override item |
| GET | `/api/v1/group/{id}/ops/compliance/config/` | JWT (G4) | Checklist config |
| PUT | `/api/v1/group/{id}/ops/compliance/config/` | JWT (G4) | Save config |
| GET | `/api/v1/group/{id}/ops/compliance/export/?format=pdf` | JWT (G3+) | Export |

---

## 14. HTMX Patterns

| Interaction | hx-trigger | hx-get | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | `/api/.../compliance/?q={}` | `#compliance-table-body` | `innerHTML` |
| Filter apply | `click` | `/api/.../compliance/?filters={}` | `#compliance-table-section` | `innerHTML` |
| Toggle heatmap | `click` | `/api/.../compliance/heatmap/` | `#compliance-view` | `innerHTML` |
| Branch detail | `click` | `/api/.../compliance/branches/{id}/` | `#drawer-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
