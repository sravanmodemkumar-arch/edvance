# 13 — Annual Strategic Plan

> **URL:** `/group/gov/strategic-plan/`
> **File:** `13-annual-strategic-plan.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 (approve) · MD G5 (full) · CEO G4 (full) · President G4 (Academic) · VP G4 (Ops) · Trustee G1 · Advisor G1 (read)

---

## 1. Purpose

Structured annual strategic plan management — from drafting branch-level targets through to
final Chairman approval. Replaces offline spreadsheets and email chains for annual planning.

Workflow: CEO/MD draft → review by President/VP for their functional sections → submit to
Chairman for final approval → approved plan locked (read-only thereafter).

Each branch has its own target set within the group annual plan.

---

## 2. Role Access

| Role | Access | Notes |
|---|---|---|
| Chairman | Approve/Reject plan · View all | Final approval authority |
| MD | Full — create, edit, submit for approval | Plan owner |
| CEO | Full — create, edit, submit | Co-owner |
| President | Edit academic targets section only | Owns academic KPIs |
| VP | Edit ops/infrastructure targets only | Owns operational KPIs |
| Trustee | Read-only | View approved plan |
| Advisor | Read-only + download | Strategic reference |
| Exec Secretary | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Annual Strategic Plan
```

### 3.2 Page Header
```
Annual Strategic Plan — FY 2026–27                     [+ New Plan]  [Export PDF ↓]
Status: [Draft / Under Review / Approved] badge        [Submit for Approval] (MD/CEO)
```

### 3.3 Plan Status Banner

**Draft:** Blue banner — "FY 2026–27 plan is in draft. Submit to Chairman for approval by March 31."

**Under Review:** Yellow banner — "Plan submitted to Chairman on [date]. Awaiting approval."

**Approved:** Green banner — "FY 2026–27 plan approved by Chairman [Name] on [date]. Plan is locked."

**Rejected:** Red banner — "Chairman rejected plan on [date]. Reason: [reason]. Revise and resubmit."

---

## 4. Plan Overview Section

**Display:** Summary card grid — group-level targets for the year.

| Target | FY 2025-26 Actual | FY 2026-27 Target | % Change |
|---|---|---|---|
| Total Enrollment | 82,340 | 95,000 | +15.4% |
| Annual Revenue | ₹84.2 Cr | ₹98 Cr | +16.4% |
| New Branches | 0 | 2 | — |
| Exam Pass Rate | 94.8% | 96% | +1.2pt |
| BGV Compliance | 87% | 100% | +13pt |
| POCSO Training | 92% | 100% | +8pt |

**Group-level KPI targets table** — editable by MD/CEO when plan is Draft or Rejected status.

---

## 5. Branch Targets Section

> Per-branch enrollment, revenue, and academic targets for the year.

**Search:** Branch name. Debounce 300ms.

**Filters:** State, Zone, Branch Type, Performance Tier.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | ✅ | |
| Zone | Text | ✅ | Large groups only |
| Enrollment Target | Number (editable) | ✅ | Editable inline or via drawer |
| Day Scholar Target | Number (editable) | ✅ | |
| Hosteler Target | Number | ✅ | If hostel branch |
| Revenue Target ₹ | Currency (editable) | ✅ | |
| Exam Pass Target % | Number | ✅ | |
| Infrastructure Capex ₹ | Currency | ✅ | Budget for building/equipment |
| Staff Hiring Plan | Number | ✅ | Additional staff to hire |
| Notes | Text | ❌ | Branch-specific note |
| Actions | — | ❌ | Edit (via drawer) · View History |

**Default sort:** Branch Name ascending.

**Pagination:** 25/page.

**Inline edit:** Click a cell to edit inline (for MD/CEO when plan is Draft). Changes auto-save
with 500ms debounce. Unsaved indicator if network error.

**Row action — Edit via Drawer:** `annual-plan-branch` drawer for full per-branch plan.

---

## 6. Budget Allocation Section

> Group-level budget distribution across functions.

**Display:** Table + donut chart.

**Table:**
| Function | Allocated Budget ₹ | % of Total | Change vs Last Year |
|---|---|---|---|
| Academic (Books, Labs) | ₹X Cr | X% | ↑X% |
| Infrastructure | ₹X Cr | X% | |
| Staff (Salary, Training) | ₹X Cr | X% | |
| Technology (EduForge) | ₹X Cr | X% | |
| Marketing / Admissions | ₹X Cr | X% | |
| Hostel Operations | ₹X Cr | X% | |
| Transport | ₹X Cr | X% | |
| Contingency | ₹X Cr | X% | |

**Donut chart:** Budget by function. Tooltip: Function · ₹X Cr · X%.

---

## 7. Approval Workflow

**Submit for Approval button** (MD/CEO, visible only when Status = Draft or Rejected):
- Click: Opens confirm modal — "Submit FY 2026–27 Strategic Plan to Chairman for approval?"
- On confirm: Status → Under Review · Chairman receives WhatsApp notification
- Chairman's approval card appears at top: "FY 2026–27 plan awaiting your approval"

**Chairman approval options (shown only to Chairman when Status = Under Review):**
- [Approve Plan] green button → confirm modal with optional note
- [Reject with Reason] red button → required reason (min 50 chars) → Status = Rejected · plan unlocked for revision

**After Approval:** All fields locked. "Approved by [Chairman Name] on [date]" shown throughout.

---

## 8. Drawers & Modals

### 8.1 Drawer: `annual-plan-branch`
- **Trigger:** Branch table row → Edit drawer
- **Width:** 640px
- **Tabs:** Budget · Academic · Enrollment · Hostel

#### Tab: Budget
| Field | Type | Required | Validation |
|---|---|---|---|
| Total Revenue Target | Currency | ✅ | > 0 |
| Fee Revenue Target | Currency | ✅ | ≤ Total Revenue |
| Infrastructure Capex | Currency | ✅ | ≥ 0 |
| Staff Cost Budget | Currency | ✅ | ≥ 0 |
| Other Costs | Currency | ❌ | ≥ 0 |
| Notes | Textarea | ❌ | Max 500 chars |

#### Tab: Academic
| Field | Type | Required | Validation |
|---|---|---|---|
| Exam Pass Rate Target | Number % | ✅ | 0–100 |
| Avg Score Target | Number % | ✅ | 0–100 |
| Toppers Target (90%+) | Number | ✅ | ≥ 0 |
| NTSE/Olympiad Target | Number | ❌ | |
| Curriculum Completion by July | % | ✅ | 0–100 |

#### Tab: Enrollment
| Field | Type | Required | Validation |
|---|---|---|---|
| Total Enrollment Target | Number | ✅ | > 0 |
| Day Scholar Target | Number | ✅ | |
| Hosteler Target | Number | Conditional | Required if hostel branch |
| New Admissions Target | Number | ✅ | |
| Retention Target % | Number | ✅ | 0–100 |

#### Tab: Hostel (shown only for hostel branches)
| Field | Type | Required | Validation |
|---|---|---|---|
| Hostel Occupancy Target % | Number | ✅ | 0–100 |
| Mess Cost per Student | Currency | ✅ | |
| Hostel Revenue Target | Currency | ✅ | |

**Submit:** "Save Branch Plan" — disabled until all required fields valid.

### 8.2 Modal: `submit-for-approval`
- **Width:** 420px
- **Content:** Plan summary (total enrollment target, revenue target, branches count)
- **Note field:** Optional message to Chairman
- **Buttons:** [Submit for Chairman Approval] + [Cancel]

### 8.3 Modal: `approve-plan`
- **Width:** 420px
- **Content:** "Approve FY 2026–27 Annual Strategic Plan?" + summary
- **Optional note:** For the record
- **Buttons:** [Approve Plan] (primary green) + [Cancel]

### 8.4 Modal: `reject-plan`
- **Width:** 420px
- **Fields:** Reason (required, min 50 chars, 500 char limit with counter) — sent to MD/CEO
- **Buttons:** [Reject Plan] (danger) + [Cancel]

---

## 9. Charts

### 9.1 Enrollment Target vs Actuals (Branch-wise)
- **Type:** Grouped bar — Target vs Last Year Actual per branch
- **Export:** PNG

### 9.2 Budget Allocation Donut
- **Type:** Doughnut
- **Data:** Budget by function
- **Export:** PNG

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Branch plan saved | "Branch plan for [Name] saved" | Success | 4s |
| Plan submitted | "FY plan submitted to Chairman for approval. Chairman notified." | Info | 4s |
| Plan approved | "FY plan approved. Plan is now locked." | Success | 4s |
| Plan rejected | "FY plan rejected. Reason sent to CEO/MD. Plan unlocked for revision." | Warning | 6s |
| Inline cell save | Auto-save (no toast — subtle save indicator in cell) | — | — |
| Auto-save failed | "Changes not saved — check connection" | Error | Manual |
| Export started | "PDF generating…" | Info | 4s |

---

## 11. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No plan for current FY | "No plan for FY 2026–27" | "Create the annual strategic plan for this financial year" | [+ New Plan] |
| No branches in plan | "No branch targets set" | "Add branch-level targets to complete the plan" | [Add Targets] |
| Plan approved — no edits needed | Green banner only — no empty state | — | — |

---

## 12. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: status banner + overview cards + branch table (10 rows) |
| Branch targets table filter | Inline skeleton rows |
| Annual-plan-branch drawer open | Spinner in drawer |
| Branch plan save (inline) | Subtle cell shimmer |
| Plan submit | Full-page overlay "Submitting plan to Chairman…" |

---

## 13. Role-Based UI Visibility

| Element | Chairman | MD/CEO | President | VP | Trustee/Advisor |
|---|---|---|---|---|---|
| [+ New Plan] | ❌ | ✅ | ❌ | ❌ | ❌ |
| [Submit for Approval] | ❌ | ✅ | ❌ | ❌ | ❌ |
| [Approve Plan] | ✅ | ❌ | ❌ | ❌ | ❌ |
| [Reject Plan] | ✅ | ❌ | ❌ | ❌ | ❌ |
| Branch target inline edit | ❌ | ✅ | Academic cols | Ops cols | ❌ |
| Budget section edit | ❌ | ✅ | ❌ | ❌ | ❌ |
| [Export PDF] | ✅ | ✅ | ✅ | ✅ | ✅ |
| View entire plan | ✅ | ✅ | Academic sections | Ops sections | ✅ read |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/strategic-plan/?fy=2026-27` | JWT | Current FY plan |
| POST | `/api/v1/group/{id}/strategic-plan/` | JWT (G5/G4) | Create new plan |
| PUT | `/api/v1/group/{id}/strategic-plan/{pid}/` | JWT (G5/G4) | Update plan overview |
| GET | `/api/v1/group/{id}/strategic-plan/{pid}/branches/` | JWT | Branch targets list |
| PUT | `/api/v1/group/{id}/strategic-plan/{pid}/branches/{bid}/` | JWT (G4+) | Update branch targets |
| POST | `/api/v1/group/{id}/strategic-plan/{pid}/submit/` | JWT (G5/G4) | Submit for approval |
| POST | `/api/v1/group/{id}/strategic-plan/{pid}/approve/` | JWT (G5 Chairman) | Approve plan |
| POST | `/api/v1/group/{id}/strategic-plan/{pid}/reject/` | JWT (G5 Chairman) | Reject with reason |
| GET | `/api/v1/group/{id}/strategic-plan/{pid}/export/` | JWT | Export PDF |

---

## HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Branch targets table search | `input delay:300ms` | GET `.../strategic-plan/?q=` | `#targets-table-body` | `innerHTML` |
| Branch targets filter | `click` | GET `.../strategic-plan/?zone=&status=` | `#targets-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../strategic-plan/?sort=&dir=` | `#targets-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../strategic-plan/?page=` | `#targets-table-section` | `innerHTML` |
| Open branch plan drawer | `click` | GET `.../strategic-plan/branch/{bid}/` | `#drawer-body` | `innerHTML` |
| Inline cell edit (target value) | `dblclick` | GET `.../strategic-plan/branch/{bid}/edit-cell/?field=` | `#cell-{bid}-{field}` | `outerHTML` |
| Save inline cell | `blur` | PUT `.../strategic-plan/branch/{bid}/` | `#cell-{bid}-{field}` | `outerHTML` |
| Submit plan for approval | `click` | POST `.../strategic-plan/submit/` | `#plan-status-banner` | `innerHTML` |
| Approve plan (Chairman) | `click` | POST `.../strategic-plan/approve/` | `#plan-status-banner` | `innerHTML` |
| Reject plan (Chairman) | `click` | POST `.../strategic-plan/reject/` | `#plan-status-banner` | `innerHTML` |
| Budget tab section switch | `click` | GET `.../strategic-plan/?section=targets\|budget` | `#plan-content-area` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
