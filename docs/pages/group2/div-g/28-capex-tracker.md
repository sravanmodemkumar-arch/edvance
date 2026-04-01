# 28 — Capital Expenditure Tracker

> **URL:** `/group/ops/facilities/capex/`
> **File:** `28-capex-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 (full) · Operations Manager G3 (view + update milestones)

---

## 1. Purpose

Tracks all capital expenditure projects across group campuses — new construction, major
renovations, equipment installations, and infrastructure upgrades. CAPEX projects have
significant budgets and multi-month timelines requiring milestone tracking and oversight.

---

## 2. Project Status Flow

```
Planning → Approved → Contractor Assigned → In Progress → Milestone Reviews → Complete
```

**Approval thresholds:**
- ≤₹5L: COO approves
- ₹5L–₹50L: CEO + COO
- >₹50L: Chairman approval (via Div-A approval workflow)

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Facilities  ›  CAPEX Tracker
```

### 3.2 Summary Strip
| Card | Value |
|---|---|
| Active Projects | Count |
| Total Budget | ₹ Cr |
| Total Spent | ₹ Cr |
| Overdue Milestones | Count (orange if >0) |
| Budget Overruns | Count (red if >0) |

---

## 4. Filters

**Filters:** Status · Branch · Zone · Budget range · Contractor · Year.

---

## 5. CAPEX Projects Table

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Project Name | ✅ | Link → project detail drawer |
| Branch | ✅ | |
| Type | ✅ | New Construction / Renovation / Equipment / Infrastructure |
| Budget | ✅ | ₹ |
| Spent | ✅ | ₹ + % of budget |
| Expected Completion | ✅ | Red if overdue |
| Status | ✅ | |
| Progress | ❌ | Progress bar (milestone completion %) |
| Contractor | ✅ | |
| Actions | — | View · Update · Raise Issue |

---

## 6. Project Create Drawer

- **Width:** 640px
- **Tabs:** Project Info · Budget · Milestones · Contractor · Documents

**Project Info:** Name · Branch · Type · Description · Expected Start · Expected End.

**Budget:** Total budget · Funding source (group fund / bank loan / government grant) · Contingency %.

**Milestones:** Add multiple milestones: Name · Target Date · % of project · Completion criteria.

**Contractor:** Contractor company · Contact · Contract value · Payment schedule.

**Documents:** Plans/drawings · Approval letters · Contracts.

---

## 7. Project Detail Drawer

- **Width:** 680px
- **Tabs:** Overview · Milestones · Budget & Payments · Photos · Documents · Issues

**Milestones tab:**
| Milestone | Target Date | Status | Completion Date | Notes |
|---|---|---|---|---|
| Foundation Work | Date | ✅ Completed | Date | |
| Structure | Date | 🔵 In Progress | — | |
| Finishing | Date | ⬜ Pending | — | |

[Update Milestone] → opens milestone update modal.

**Budget & Payments tab:**
- Budget breakdown per phase
- Payments made: amount · date · payment mode · invoice reference

**Photos tab:** Progress photos per milestone. Timeline view.

**Issues tab:** Any issues raised against this CAPEX project.

---

## 8. Milestone Update Modal

- **Width:** 480px
- **Fields:** Status (Pending / In Progress / Completed / Delayed) · Actual Completion Date (if complete) · Completion % · Notes · Photo uploads

---

## 9. Budget Overrun Alert

If Spent > Budget × 105% → automatic escalation to COO → COO must acknowledge.
If Spent > Budget × 115% → escalation to CEO.

---

## 10. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Project created | "CAPEX project created — pending approval" | Success · 4s |
| Milestone updated | "Milestone updated" | Success · 4s |
| Budget overrun alert | "Budget overrun detected: [Project] — [%] over budget" | Warning · manual |

---

## 11. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 |
|---|---|---|
| [+ Create Project] | ✅ | ❌ |
| [Approve Project] | ✅ | ❌ |
| [Update Milestone] | ✅ | ✅ |
| [Record Payment] | ✅ | ❌ |
| Budget details | ✅ | ✅ view |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/facilities/capex/` | JWT (G3+) | Project list |
| POST | `/api/v1/group/{id}/facilities/capex/` | JWT (G4) | Create project |
| GET | `/api/v1/group/{id}/facilities/capex/{pid}/` | JWT (G3+) | Project detail |
| PUT | `/api/v1/group/{id}/facilities/capex/{pid}/` | JWT (G4) | Edit project |
| POST | `/api/v1/group/{id}/facilities/capex/{pid}/milestones/{mid}/update/` | JWT (G3+) | Update milestone |
| POST | `/api/v1/group/{id}/facilities/capex/{pid}/payment/` | JWT (G4) | Record payment |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
