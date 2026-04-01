# 06 — Hostel Admission Coordinator Dashboard

> **URL:** `/group/hostel/admissions/`
> **File:** `06-hostel-admission-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Hostel Admission Coordinator (Role 72, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Hostel Admission Coordinator. Manages the full lifecycle of hostel admission across all branches — from initial application through hostel type selection (AC/Non-AC, Boys/Girls), seat allocation, room assignment, parent consent collection, and admission confirmation.

The Hostel Admission Coordinator operates in coordination with the Group Admissions Director (Division C): when a student is admitted academically, the hostel seat request flows to this coordinator for hostel-specific processing. Centralized hostel seat allocation is critical because large groups may have 500–3,000 hostel seats across 20–50 branches, and seat availability varies by room type, gender, and branch.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Hostel Admission Coordinator | G3 | Full — all branches, both genders | Exclusive dashboard |
| Group Boys Hostel Coordinator | G3 | View — boys applications only | Via own dashboard |
| Group Girls Hostel Coordinator | G3 | View — girls applications only | Via own dashboard |
| Group Hostel Director | G3 | View — admission summary | Via own dashboard |
| Group Hostel Fee Manager | G3 | View — admission-fee link | For fee plan creation after admission |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Hostel Admissions  ›  Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]         [+ New Application]  [Export Pipeline ↓]  [Settings ⚙]
Group Hostel Admission Coordinator · AY [current academic year]
Applications: [N]  ·  Pending Seat Allocation: [N]  ·  Confirmed: [N]  ·  Waitlisted: [N]
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Applications pending > 7 days without action | "[N] hostel applications have been pending for more than 7 days." | Amber |
| Branch hostel at > 95% capacity and applications pending | "[Branch] hostel is at [N]% capacity with [N] pending applications. Review allocation or waitlist." | Amber |
| Waitlist applications pending > 30 days | "[N] waitlisted students have been waiting > 30 days. Notify parents with status update." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Applications (AY) | All hostel applications this academic year | Blue always | → Page 15 |
| Pending Seat Allocation | Applications awaiting seat assignment | Green = 0 · Yellow 1–20 · Red > 20 | → Page 15 (pending filter) |
| Confirmed Hostelers | Admission complete + seat assigned | Blue always | → Page 16 |
| Waitlisted | On waitlist (seat not available) | Yellow > 0 | → Page 15 (waitlist filter) |
| Seats Available (Total) | Unfilled beds across all branches | Green > 50 · Yellow 1–50 · Red = 0 | → Page 16 |
| Seats Available — AC | AC beds available | Blue · Red = 0 | → Page 16 (filtered: AC) |

**HTMX:** `hx-trigger="every 10m"` → KPI auto-refresh.

---

## 5. Sections

### 5.1 Admission Pipeline — Summary Funnel

> Visual funnel of hostel admission stages.

**Stages (horizontal funnel):**
```
Received → Verified → Seat Allocated → Parent Consent → Confirmed
   [N]         [N]          [N]              [N]            [N]
```

Each stage count is clickable → filters the main pipeline table to that stage.

---

### 5.2 Application Pipeline Table

> All hostel applications with full lifecycle status.

**Search:** Student name, parent name, branch, application ID. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches with hostel |
| Gender | Radio | All / Boys / Girls |
| Hostel Type | Checkbox | AC / Non-AC |
| Stage | Checkbox | Received / Verified / Seat Allocated / Parent Consent / Confirmed / Waitlisted / Rejected |
| Age in Pipeline | Radio | Any / > 3 days / > 7 days / > 15 days |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / HEC / Foundation |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Application ID | ✅ | Auto ID — link → application detail drawer |
| Student Name | ✅ | |
| Gender | ✅ | M/F badge |
| Branch Requested | ✅ | |
| Stream | ✅ | |
| Hostel Type Pref | ✅ | AC / Non-AC |
| Applied On | ✅ | Date |
| Stage | ✅ | Badge |
| Seat Assigned | ✅ | Room # or "Pending" |
| Days in Stage | ✅ | Count (red if > 7) |
| Actions | ❌ | View · Allocate Seat · Waitlist · Reject |

**Default sort:** Days in stage descending (longest pending first).

**Pagination:** Server-side · 25/page.

---

### 5.3 Seat Availability Matrix

> Cross-branch seat availability snapshot — Coordinator's allocation tool.

| Branch | Boys AC Available | Boys Non-AC Available | Girls AC Available | Girls Non-AC Available | Total Available |
|---|---|---|---|---|---|
| [Branch 1] | [N] | [N] | [N] | [N] | [N] |
| [Branch 2] | [N] | [N] | [N] | [N] | [N] |

Cells turn red when available = 0. Cells turn amber when available ≤ 5.

[View Full Room Allocation →] → Page 14.

---

### 5.4 Waitlist Queue

> Students currently on hostel waitlist, in date order.

**Quick table:** Position # · Student Name · Gender · Branch · Hostel Type · Waiting Since · [Notify →] [Allocate →]

"View Full →" → Page 15 filtered: Waitlisted.

---

## 6. Drawers

### 6.1 Drawer: `admission-application`
- **Trigger:** Pipeline table → row or Application ID link
- **Width:** 640px
- **Tabs:** Applicant · Parent · Preferences · Documents · Status History
- **Applicant tab:** Student name, age, gender, stream, academic branch, special needs flag
- **Parent tab:** Father/mother name, contact, address, ID proof number
- **Preferences tab:** Hostel type preference, AC/Non-AC, room-sharing preference, dietary restrictions
- **Documents tab:** Upload checklist (birth certificate, medical fitness, parent ID proof, fee receipt) with ✅/❌ status
- **Status History:** Stage changes with actor and timestamp

### 6.2 Drawer: `admission-approve` — Allocate Seat & Confirm
- **Trigger:** Pipeline table → Allocate Seat
- **Width:** 480px
- **Fields:**
  - Branch (pre-filled, editable)
  - Hostel Type (AC / Non-AC radio)
  - Room # (dropdown from available rooms)
  - Bed # (dropdown: A/B/C based on room)
  - Fee Plan (dropdown from configured plans for this hostel type)
  - Notify Parent (checkbox + message preview)
  - Admission Date (date picker)
- **Validations:** Room must match gender; capacity check before confirming
- **On submit:** Seat locked; parent WhatsApp notification sent; hosteler record created in Page 12

### 6.3 Modal: Waitlist / Reject
- **Type:** Centred modal (480px)
- **Fields:** Reason (required textarea) + Notify Parent (checkbox)
- **On confirm:** Status updated; parent notified if checkbox checked

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Application created | "Hostel application #[ID] created for [Name]." | Success | 4s |
| Seat allocated | "Seat allocated: Room [#] Bed [#] at [Branch] for [Name]." | Success | 4s |
| Parent notified | "Parent notified via WhatsApp." | Info | 3s |
| Waitlisted | "[Name] added to waitlist at position [N]." | Info | 4s |
| Rejected | "Application #[ID] rejected. Parent notified." | Warning | 5s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No applications this AY | "No Hostel Applications Yet" | "No hostel applications have been submitted for this academic year." | [+ New Application] |
| No pending applications | "All Applications Processed" | "Every application has been actioned — seat allocated, waitlisted, or rejected." | — |
| No seats available | "All Hostel Seats Full" | "All configured hostel seats are allocated. Review waitlist or request branch to add capacity." | [View Waitlist] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: funnel + 6 KPI cards + application table (10 rows) + seat matrix |
| Table filter/search | Inline skeleton rows |
| KPI auto-refresh | Shimmer over card values |
| Seat allocation drawer submit | Spinner on Confirm; table row refreshes |

---

## 10. Role-Based UI Visibility

| Element | Admission Coordinator G3 | Boys Coordinator G3 | Girls Coordinator G3 | Hostel Director G3 |
|---|---|---|---|---|
| See all applications | ✅ All genders | ✅ Boys only | ✅ Girls only | ✅ All |
| Allocate seat | ✅ | ✅ Boys only | ✅ Girls only | ✅ |
| Reject application | ✅ | ❌ | ❌ | ✅ |
| View seat availability matrix | ✅ | ✅ (Boys columns) | ✅ (Girls columns) | ✅ All |
| Export pipeline | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/admissions/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/admissions/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/admissions/applications/` | JWT (G3+) | Application pipeline (paginated) |
| GET | `/api/v1/group/{group_id}/hostel/admissions/applications/{id}/` | JWT (G3+) | Application detail |
| POST | `/api/v1/group/{group_id}/hostel/admissions/applications/` | JWT (G3+) | Create application |
| POST | `/api/v1/group/{group_id}/hostel/admissions/applications/{id}/allocate/` | JWT (G3+) | Allocate seat |
| POST | `/api/v1/group/{group_id}/hostel/admissions/applications/{id}/waitlist/` | JWT (G3+) | Waitlist applicant |
| POST | `/api/v1/group/{group_id}/hostel/admissions/applications/{id}/reject/` | JWT (G3+) | Reject application |
| GET | `/api/v1/group/{group_id}/hostel/admissions/seat-availability/` | JWT (G3+) | Cross-branch seat matrix |
| GET | `/api/v1/group/{group_id}/hostel/admissions/waitlist/` | JWT (G3+) | Waitlist queue |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 10m` | GET `.../admissions/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Funnel stage click | `click` | GET `.../applications/?stage={stage}` | `#application-table-section` | `innerHTML` |
| Application search | `input delay:300ms` | GET `.../applications/?q={val}` | `#application-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../applications/?{filters}` | `#application-table-section` | `innerHTML` |
| Open application detail | `click` on ID | GET `.../applications/{id}/` | `#drawer-body` | `innerHTML` |
| Allocate seat submit | `click` on Confirm | POST `.../applications/{id}/allocate/` | `#application-table-section` | `innerHTML` |
| Seat matrix load | `load` | GET `.../seat-availability/` | `#seat-matrix` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
