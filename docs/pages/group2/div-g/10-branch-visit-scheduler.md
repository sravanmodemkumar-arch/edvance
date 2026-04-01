# 10 — Branch Visit Scheduler

> **URL:** `/group/ops/visits/`
> **File:** `10-branch-visit-scheduler.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** COO G4 · Operations Manager G3 · Branch Coordinator G3 (own branches) · Zone Director G4 (zone) · Zone Ops Manager G3 (zone)

---

## 1. Purpose

Schedule, track, and record Branch Coordinator visits to all group branches. Enforces visit
frequency policy (minimum 1 per branch per month). After each visit, coordinators submit a
post-visit report with compliance checklist, issues found, and follow-up actions. COO and
Ops Manager monitor visit coverage and overdue branches.

---

## 2. Role Access

| Role | Access |
|---|---|
| COO G4 | All visits — schedule, view, export |
| Operations Manager G3 | All visits — schedule, view, export |
| Branch Coordinator G3 | Own assigned branches only |
| Zone Director G4 | Zone visits |
| Zone Ops Manager G3 | Zone visits |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Operations  ›  Branch Visit Scheduler
```

### 3.2 Page Header (with view toggle)
```
Branch Visit Scheduler                     [+ Schedule Visit]  [Export ↓]  [⚙ Policy]
[Calendar View]  [List View]  ← toggle
```

### 3.3 Summary Strip
| Card | Value |
|---|---|
| Scheduled This Month | `42 visits` |
| Completed | `28 / 42 (67%)` |
| Overdue | `4` (red if >0) |
| Reports Pending | `6 completed visits missing report` |

---

## 4. Calendar View (default)

**Display:** Full-month calendar grid. Each day cell shows visit markers.

**Visit marker:** Coloured dot with coordinator name + branch name on hover tooltip.
- Green: Completed + report submitted
- Blue: Scheduled (future)
- Yellow: Completed but report not submitted
- Red: Overdue (past date, not yet completed)

**Navigation:** Month prev/next arrows · "Today" button.

**Click on visit marker:** Opens `visit-detail` drawer.

**Click on empty date:** Opens `visit-schedule-create` drawer with date pre-filled.

**Zone/Coordinator filter:** Dropdown above calendar to filter by coordinator or zone.

---

## 5. List View (table)

**Search:** Branch name, coordinator name. 300ms debounce.

**Advanced Filters:**
| Filter | Options |
|---|---|
| Status | Scheduled · Completed · Overdue · Report Pending |
| Visit Type | Routine · Audit · Emergency · Follow-up |
| Coordinator | Select |
| Zone | Select |
| Date Range | This month · Last month · Custom |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | |
| Zone | ✅ | |
| Coordinator | ✅ | |
| Visit Type | ✅ | Routine / Audit / Emergency / Follow-up |
| Scheduled Date | ✅ | Red if overdue |
| Status | ✅ | Colour-coded badge |
| Report | ✅ | Submitted / Pending / N/A |
| Actions | — | View · Edit · Submit Report · Cancel |

**Pagination:** Server-side · 25/page.

---

## 6. Schedule Visit Drawer

- **Width:** 560px
- **Trigger:** [+ Schedule Visit] button or empty calendar date click

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Searchable select | Required · scoped to own branches (coordinator) |
| Coordinator | Select | Required · pre-filled if Branch Coordinator user |
| Visit Type | Select | Routine / Audit / Emergency / Follow-up |
| Date | Date picker | Must be future date |
| Estimated Duration | Select | 1h · 2h · Half day · Full day |
| Objectives / Checklist Template | Multi-select checkboxes | Academic Compliance · Fee Collection · Staff Conduct · Facilities · Safety · Hostel |
| Notes | Textarea | Optional · max 500 chars |
| Notify Principal | Toggle | ON = send WhatsApp + EduForge notification to branch Principal |

---

## 7. Post-Visit Report Drawer

> Submitted by coordinator after visit completion.

- **Width:** 640px
- **Trigger:** Visit row → [Submit Report]

**Sections:**

**Section 1 — Visit Summary**
- Date of visit (pre-filled) · Duration (actual) · People met

**Section 2 — Checklist Results**
| Checklist Item | Result | Notes |
|---|---|---|
| Academic compliance | ✅/⚠/❌ | |
| Fee collection status | ✅/⚠/❌ | |
| Staff conduct | ✅/⚠/❌ | |
| Facilities condition | ✅/⚠/❌ | |
| Safety checks | ✅/⚠/❌ | |
| Hostel welfare (if applicable) | ✅/⚠/❌ | |

**Section 3 — Issues Found**
- Issues list (add multiple): Type · Severity · Description · Photo upload
- Each issue auto-creates a maintenance ticket or escalation based on type

**Section 4 — Recommendations**
- Free text · min 30 chars

**Section 5 — Overall Rating**
- Branch overall rating: 1–5 stars with mandatory comment

**Section 6 — Photos**
- Up to 10 photos · captions · stored in Cloudflare R2

**[Submit Report] button:** Creates immutable visit record. Cannot be edited after submission.

---

## 8. Visit Detail Drawer

- **Width:** 560px
- **Tabs:** Summary · Checklist · Issues · Photos

---

## 9. Visit Policy Configuration (COO only)

- **Access:** [⚙ Policy] button in page header
- **Settings:** Minimum visits per branch per month · Visit types (enable/disable) · Checklist templates · Overdue threshold (days)
- **Stored as group configuration, not per-page settings**

---

## 10. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Visit scheduled | "Visit scheduled for [Branch] on [Date]. Principal notified." | Success · 4s |
| Report submitted | "Visit report submitted. [N] issues auto-created as tickets." | Success · 4s |
| Visit cancelled | "Visit cancelled. [Coordinator] notified." | Warning · 6s |
| Policy saved | "Visit policy updated" | Success · 4s |

---

## 11. Empty States

| Condition | Heading | CTA |
|---|---|---|
| No visits this month | "No visits scheduled this month" | [+ Schedule Visit] |
| No branches assigned (Coordinator) | "No branches assigned" | Contact Ops Manager |
| No overdue | "All visits on track" | — |

---

## 12. Loader States

Page load: Skeleton calendar grid + summary strip.
List view switch: Table skeleton rows.
Drawer open: Spinner in drawer body.

---

## 13. Role-Based UI Visibility

| Element | COO G4 | Ops Mgr G3 | Coordinator G3 | Zone Dir G4 |
|---|---|---|---|---|
| All branches | ✅ | ✅ | Own only | Zone only |
| [+ Schedule Visit] | ✅ | ✅ | ✅ own | ✅ zone |
| [Submit Report] | ✅ (any) | ✅ (any) | ✅ own visits | ✅ zone |
| [Cancel Visit] | ✅ | ✅ | ✅ own upcoming | ❌ |
| [⚙ Policy] | ✅ | ❌ | ❌ | ❌ |
| Export | ✅ | ✅ | ❌ | ✅ |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/visits/` | JWT (G3+) | Visit list with filters/sort/page |
| GET | `/api/v1/group/{id}/visits/calendar/?month={yyyy-mm}` | JWT (G3+) | Calendar view data |
| POST | `/api/v1/group/{id}/visits/` | JWT (G3+) | Create visit schedule |
| PUT | `/api/v1/group/{id}/visits/{visit_id}/` | JWT (G3+) | Edit scheduled visit |
| DELETE | `/api/v1/group/{id}/visits/{visit_id}/` | JWT (G3+) | Cancel visit |
| POST | `/api/v1/group/{id}/visits/{visit_id}/report/` | JWT (G3+) | Submit post-visit report |
| GET | `/api/v1/group/{id}/visits/{visit_id}/` | JWT (G3+) | Visit detail |
| GET | `/api/v1/group/{id}/visits/summary/` | JWT (G3+) | Summary strip counts |
| PUT | `/api/v1/group/{id}/ops/visit-policy/` | JWT (G4) | Update visit policy |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| Month navigation | `click` | `/api/.../visits/calendar/?month={}` | `#visit-calendar` | `innerHTML` |
| Calendar coordinator filter | `change` | `/api/.../visits/calendar/?coordinator_id={}&month={}` | `#visit-calendar` | `innerHTML` |
| List search | `input delay:300ms` | `/api/.../visits/?q={}` | `#visit-table-body` | `innerHTML` |
| List filter apply | `click` | `/api/.../visits/?filters={}` | `#visit-table-section` | `innerHTML` |
| Visit marker click | `click` | `/api/.../visits/{id}/` | `#drawer-body` | `innerHTML` |
| [Submit Report] click | `click` | GET `/api/.../visits/{id}/report-form/` | `#drawer-body` | `innerHTML` |
| Report submit | `click` | POST `/api/.../visits/{id}/report/` | `#visit-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
