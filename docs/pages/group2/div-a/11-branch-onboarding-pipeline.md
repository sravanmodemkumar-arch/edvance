# 11 — Branch Onboarding Pipeline

> **URL:** `/group/gov/branches/onboarding/`
> **File:** `11-branch-onboarding-pipeline.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** MD G5 (full) · CEO G4 (full) · Chairman G5 (view) · VP G4 (view)

---

## 1. Purpose

Step-gated Kanban board for managing the onboarding of new branches from application through to
go-live. Each new branch must progress through 8 mandatory stages in sequence — a stage cannot
be marked complete unless all checklist items within it are done.

Prevents partial onboarding from resulting in a live branch with missing configuration, missing
staff accounts, or no principal assigned.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| MD | G5 | Full — advance stages, assign, edit | Primary owner of onboarding |
| CEO | G4 | Full — advance stages, assign, edit | Co-owner |
| Chairman | G5 | View — all stages, read-only | Oversight only |
| VP | G4 | View — operational stages only (Infra, Staff, Systems) | Ops oversight |
| Others | G3/G1 | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Branch Overview  ›  Onboarding Pipeline
```

### 3.2 Page Header
```
Branch Onboarding Pipeline                             [+ Start New Onboarding]  [Export Status ↓]
[N] branches in pipeline · [N] completed this year     (MD/CEO only)
```

### 3.3 Pipeline Stats Bar
| Stat | Value |
|---|---|
| In Pipeline | N branches currently onboarding |
| Completed (FY) | N branches went live this year |
| Avg Days to Go Live | N days (group average) |
| Blocked | N branches with blockers |

---

## 4. Kanban Board

**Layout:** Horizontal scroll. 8 stage columns. Branch cards within each column.

**Stages:**

| # | Stage | Description | Avg Days |
|---|---|---|---|
| 1 | Applied | Application received, initial review | 7 |
| 2 | Legal | Trust deed, land documents, NOC | 14 |
| 3 | Infrastructure | Building readiness, CCTV, fire safety | 21 |
| 4 | Staff Hiring | Principal assigned, core staff hired | 14 |
| 5 | System Setup | Portal configured, user accounts created | 7 |
| 6 | Training | Staff trained on EduForge platform | 5 |
| 7 | Soft Launch | Limited students, trial period | 14 |
| 8 | Live | Full go-live | — |

**Stage column header:**
- Stage name + number
- Count of branches in this stage
- Expected avg days indicator

### 4.1 Branch Card (within a stage column)

```
[Branch Name]                              [Blocker badge if blockers >0]
[City, State] · [Type: Day/Hostel]
Progress: [progress bar] X% complete
Expected Go-Live: [date]
Assigned: [Coordinator Name avatar]
Days in stage: [N] · [overdue badge if >avg]
[View Details] [Advance Stage ▶] (MD/CEO only)
```

**Advance Stage button:** Only enabled when all checklist items in current stage are complete.
Clicking opens advance-stage confirm modal.

**Blocker badge:** Red badge with count. Clicking opens the branch onboarding detail drawer
filtered to blocked items.

### 4.2 Branch Card — drag and drop
- MD/CEO can drag branch cards between stages (but only forward — cannot move backward via drag)
- Moving backward requires explicit "Revert Stage" action from detail drawer (with reason)

---

## 5. Branch Onboarding Detail Drawer

### Drawer: `branch-onboarding-detail`
- **Trigger:** Branch card → [View Details]
- **Width:** 760px
- **Tabs:** Overview · Stage Checklist · Documents · Timeline · Team

#### Tab: Overview
| Field | Value |
|---|---|
| Branch Name | [Name] |
| City / State | |
| Type | Day Scholar / Hostel / Both |
| Streams | [list] |
| Application Date | [date] |
| Expected Go-Live | [date] — editable (MD/CEO) |
| Assigned Coordinator | [name] — editable (MD/CEO) |
| Current Stage | [stage name] |
| Days in Current Stage | [N] |
| Overall Progress | [progress bar] X% |

#### Tab: Stage Checklist
- Shows current stage's checklist items
- Stage selector at top (can view any stage's checklist — all past stages locked/complete)

**Checklist items per stage:**

**Legal Stage checklist:**
- [ ] Trust deed verified
- [ ] Land ownership/lease documents
- [ ] NOC from local authority
- [ ] CBSE/Board affiliation applied
- [ ] Bank account opened for branch

**Infrastructure Stage:**
- [ ] Building inspection completed
- [ ] Classroom count verified (min per Board norms)
- [ ] CCTV coverage installed
- [ ] Fire safety NOC
- [ ] Drinking water source certified

**Staff Hiring Stage:**
- [ ] Principal appointed and account provisioned
- [ ] Vice Principal appointed
- [ ] Min 80% teaching positions filled
- [ ] Hostel wardens appointed (if hostel)
- [ ] Administrative staff in place

**System Setup Stage:**
- [ ] EduForge branch portal configured
- [ ] WhatsApp notifications configured
- [ ] Fee structure entered
- [ ] Academic calendar imported
- [ ] Student admission system opened

**Training Stage:**
- [ ] All staff trained on EduForge basics
- [ ] Principal trained on admin features
- [ ] Mock test run completed
- [ ] Fee collection test completed

**Soft Launch Stage:**
- [ ] First batch of students admitted
- [ ] Attendance tracking running
- [ ] First fee collection cycle done
- [ ] Parent communication established
- [ ] No critical issues open >48h

Each item: Checkbox (MD/CEO can check) · Updated by · Updated at · Notes field.

**Progress bar** per stage: auto-calculated from checked items.

#### Tab: Documents
- Upload/view documents for each stage
- Table: Document Name · Stage · Uploaded By · Uploaded At · Type · [View] [Delete]
- [+ Upload Document] button (MD/CEO only)
- Max 20 files, 50MB each (PDFs, images)

#### Tab: Timeline
- Chronological log of all stage transitions, checklist updates, document uploads
- Fields: Timestamp · Actor · Action · Stage · Notes

#### Tab: Team
- Assigned coordinator (editable MD/CEO)
- Involved team members: add/remove (search by name)
- Branch principal (linked from user provisioning)

---

## 6. Modals

### 6.1 Modal: `advance-stage-confirm`
- **Width:** 420px
- **Content:** "Advance [Branch Name] from [Stage X] to [Stage Y]?" · All checklist items shown as complete (green checkmarks) · "This cannot be reversed without recording a reason."
- **Fields:** Optional note (for context in timeline)
- **Buttons:** [Advance Stage] (primary) + [Cancel]

### 6.2 Modal: `revert-stage-confirm`
- **Width:** 420px
- **Fields:** Reason (required, min 30 chars) — "Why are you reverting to the previous stage?"
- **Buttons:** [Revert Stage] (danger) + [Cancel]

### 6.3 Modal: `start-onboarding`
- **Width:** 560px
- **Fields:** Branch Name · City/State · Type · Expected Go-Live (date) · Assign Coordinator (select from group users) · Streams (multi-select)
- **Note:** "Full branch setup continues in Branch Overview → Create Branch after onboarding completes"
- **Buttons:** [Start Onboarding] + [Cancel]

### 6.4 Modal: `mark-blocker`
- **Width:** 420px
- **Fields:** Blocker description (required, min 20 chars) · Responsible party · Target resolve date
- **Buttons:** [Add Blocker] + [Cancel]

---

## 7. Charts

### 7.1 Pipeline Funnel (current snapshot)
- **Type:** Horizontal funnel or stacked bar
- **Data:** Branch count per stage
- **Colour:** Stage-specific colour
- **Export:** PNG

### 7.2 Days to Go-Live Distribution (historical)
- **Type:** Histogram
- **Data:** Number of branches per "days taken" bucket (30–60 days, 60–90 days, 90–120 days, 120+ days)
- **Shows** avg and median lines
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Stage advanced | "[Branch] advanced to [Stage Y]" | Success | 4s |
| Stage reverted | "[Branch] reverted to [Stage X]. Reason recorded." | Warning | 6s |
| Checklist item checked | "Checklist item marked complete" | Info | 3s |
| Document uploaded | "Document uploaded to [Branch] onboarding" | Success | 4s |
| Blocker added | "Blocker logged. Coordinator notified." | Warning | 6s |
| Onboarding started | "Onboarding pipeline started for [Branch]" | Success | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches in pipeline | "No active onboarding" | "Start onboarding a new branch to see it here" | [+ Start Onboarding] |
| Stage column empty | "No branches at this stage" | "Branches at [stage] will appear here" | — |
| No timeline entries | "No activity yet" | "Actions taken on this branch will appear here" | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + Kanban columns (3 cards per column skeleton) |
| Detail drawer open | Spinner in drawer |
| Checklist item save | Spinner on checkbox |
| Advance stage | Full-page overlay "Advancing to [Stage]…" |
| Document upload | Progress bar in document tab |

---

## 11. Role-Based UI Visibility

| Element | MD G5 | CEO G4 | Chairman G5 | VP G4 |
|---|---|---|---|---|
| [+ Start Onboarding] | ✅ | ✅ | ❌ | ❌ |
| [Advance Stage] button on card | ✅ | ✅ | ❌ | ❌ |
| Drag card between stages | ✅ | ✅ | ❌ | ❌ |
| Check checklist items | ✅ | ✅ | ❌ | ❌ |
| Upload documents | ✅ | ✅ | ❌ | ❌ |
| [Revert Stage] | ✅ | ✅ | ❌ | ❌ |
| [Mark Blocker] | ✅ | ✅ | ❌ | ❌ |
| [Export Status] | ✅ | ✅ | ✅ | ❌ |
| View entire pipeline (read) | ✅ | ✅ | ✅ | ✅ (Infra/Staff/Systems only) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/branches/onboarding/` | JWT | All branches in onboarding pipeline |
| POST | `/api/v1/group/{id}/branches/onboarding/` | JWT (G5/G4) | Start new onboarding |
| GET | `/api/v1/group/{id}/branches/onboarding/{oid}/` | JWT | Branch onboarding detail |
| PUT | `/api/v1/group/{id}/branches/onboarding/{oid}/` | JWT (G5/G4) | Update onboarding metadata |
| POST | `/api/v1/group/{id}/branches/onboarding/{oid}/advance/` | JWT (G5/G4) | Advance to next stage |
| POST | `/api/v1/group/{id}/branches/onboarding/{oid}/revert/` | JWT (G5/G4) | Revert to prev stage + reason |
| PATCH | `/api/v1/group/{id}/branches/onboarding/{oid}/checklist/{item_id}/` | JWT (G5/G4) | Check/uncheck item |
| POST | `/api/v1/group/{id}/branches/onboarding/{oid}/documents/` | JWT (G5/G4) | Upload document |
| DELETE | `/api/v1/group/{id}/branches/onboarding/{oid}/documents/{did}/` | JWT (G5/G4) | Delete document |
| POST | `/api/v1/group/{id}/branches/onboarding/{oid}/blockers/` | JWT (G5/G4) | Add blocker |
| GET | `/api/v1/group/{id}/branches/onboarding/stats/` | JWT | Pipeline summary stats |

---

## HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Filter by stage | `click` | GET `.../branches/onboarding/?stage=` | `#kanban-board` | `innerHTML` |
| Filter by assigned | `change` | GET `.../branches/onboarding/?assigned=` | `#kanban-board` | `innerHTML` |
| Open branch onboarding detail drawer | `click` | GET `.../branches/onboarding/{bid}/` | `#drawer-body` | `innerHTML` |
| Advance stage (checklist complete) | `click` | POST `.../branches/onboarding/{bid}/advance/` | `#kanban-card-{bid}` | `outerHTML` |
| Revert stage (with reason) | `click` | POST `.../branches/onboarding/{bid}/revert/` | `#kanban-card-{bid}` | `outerHTML` |
| Checklist item toggle | `change` | PUT `.../branches/onboarding/{bid}/checklist/{item}/` | `#checklist-item-{item}` | `outerHTML` |
| Document upload | `change` | POST `.../branches/onboarding/{bid}/documents/` | `#document-upload-status` | `innerHTML` |
| Stats bar refresh | `every 5m` | GET `.../branches/onboarding/stats/` | `#onboarding-stats` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
