# A-04 — VP Administration Dashboard

> **URL:** `/school/admin/vp-admin/`
> **File:** `a-04-vp-admin-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Vice-Principal (Administration) (S5) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the VP Administration. This role owns everything operational that is not directly academic: admissions pipeline, fee collection status, non-teaching staff, transport, hostel, infrastructure, vendor management, procurement, and safety compliance. In schools without a dedicated VP Admin, the Principal absorbs this role.

**Indian school context:** The VP Admin in a large Indian school is the person who:
- Signs the transport log every morning before buses depart
- Manages the Hostel Warden and reviews hostel attendance
- Approves vendor invoices and petty cash
- Ensures fire safety NOC is renewed
- Manages the gate staff, sweepers, and peons (Class IV employees)
- Coordinates with the municipality for water/electricity/waste
- Receives and processes student admission enquiries
- Ensures the CCTV system is functional (CBSE/state board requirement)

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| VP Administration | S5 | Full — all sections |
| Principal | S6 | Read access |
| VP Academic | S5 | — |
| Administrative Officer | S3 | Read — limited tabs visible |

---

## 3. Page Header
```
Good morning, [VP Admin Name]                           [Quick Action ▼]  [⚙]
VP Administration · [School Name] · Year [2025–26 ▼]
```

**[Quick Action ▼]:**
- View Transport Status (buses departed?)
- Review Admission Enquiries (today)
- Pending Purchase Requests
- Check Hostel Attendance

### Alert Banner (conditional)
- Red: Any bus not back within 60 min of scheduled return time
- Red: Hostel fire drill overdue by > 30 days
- Amber: Admission pipeline conversion < 60% vs target
- Amber: Non-teaching staff leave > 20% today

---

## 4. KPI Strip (6 cards)

> HTMX refresh every 5m on `#vpadmin-kpi-strip`

| # | Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|---|
| 1 | Non-Teaching Staff | `31/35 present today (88.6%)` | Green ≥95% · Amber 80–94% · Red <80% | → A-17 Staff Attendance |
| 2 | Today's Admissions Enquiries | `14 new enquiries` | Blue | → A-14 Admission Pipeline |
| 3 | Fee Collection (This Month) | `₹42.3L / ₹54L (78.3%)` | Green ≥90% · Amber 75–89% · Red <75% | → A-20 Fee Dashboard |
| 4 | Pending Purchase Requests | `5 pending` approval | Badge if >0 | → A-25 Procurement |
| 5 | Transport Status | `12 / 14 buses returned` | Green = all returned · Red = any overdue | → div-j Transport |
| 6 | Hostel Occupancy | `248 / 300 beds (82.7%)` | Blue | → div-i Hostel |

---

## 5. Main Sections

### 5.1 Tab: Operations Today

**5.1.1 Transport Morning Log**
- Table: Route No · Bus No · Driver · Departure Time · Expected Return · Actual Return · Status
- Status badge: ON TIME · DELAYED · NOT RETURNED
- Overdue buses (not returned within 60 min of expected) → red row + alert
- [Mark Returned] per route
- [Emergency Alert] button (sends bulk WhatsApp to all parents on that route)

**5.1.2 Today's Admission Enquiries**
- Table: Enquiry time · Student name · Class for · Parent name · Contact · Source (walk-in/call/WhatsApp/website) · [Process]
- [Process] → opens admission detail drawer

**5.1.3 Non-Teaching Staff Absent Today**
- List: Name · Role · Area managed · Leave type
- [Arrange Cover] per absent staff

---

### 5.2 Tab: Admissions

**5.2.1 Admission Funnel (current season)**
- Funnel: Enquiry → Application → Test/Interview → Offer → Confirmed → Reported
- Current vs same period last year comparison
- By class: which classes are filling faster/slower

**5.2.2 Pending Application Actions**
- Table: Student · Class · Stage · Waiting Since · Action
- Stages: DOCUMENTS PENDING · TEST SCHEDULED · OFFER PENDING · FEE PENDING
- [Act] per row

**5.2.3 RTE Admission Status**
- RTE 25% slots: Filled / Total per class
- Lottery draw scheduled date (if applicable)
- [Submit RTE Report] button (for state board/RTE portal)

---

### 5.3 Tab: Infrastructure & Safety

**5.3.1 CCTV & Safety Systems**
- CCTV: Total cameras · Online · Offline (< 24h) · Offline (> 24h = red alert)
- Fire extinguishers last checked date
- Fire alarm last tested
- Emergency exits status (blocked/clear — manual check record)

**5.3.2 Maintenance Requests**
- Table: Area · Issue · Reported By · Date · Priority · Status
- [+ New Request] [Assign Contractor]

**5.3.3 Compliance Calendar**
- List of infrastructure compliance items due in next 60 days:
  - Fire NOC renewal · Electrical safety certificate · Water quality test · Pest control · CCTV license renewal

---

### 5.4 Tab: Procurement & Vendors

**5.4.1 Purchase Requests Pending Approval**
- Table: Item · Requested By · Amount · Budget Code · Days Pending · [Approve/Reject]

**5.4.2 Vendor Register**
- List of approved vendors: Name · Category · Contact · Contract expiry · Rating
- [+ Add Vendor]

**5.4.3 Petty Cash Status (current month)**
- Opening balance · Spent · Balance remaining
- Recent transactions list

---

### 5.5 Tab: Hostel Overview

- Total capacity vs occupied (boys / girls separately)
- Today's hostel attendance (present / absent / on leave)
- Hostel fee status: paid / pending per hosteler
- Recent incidents or complaints
- [View Hostel Dashboard →] link to div-i

---

## 6. Key Drawers

### `admission-process` (from Today's Enquiries)
- 640px wide
- Tabs: Enquiry Details · Student Info · Documents · Schedule Test · Offer
- Records enquiry stage, moves through pipeline
- Fee payment link can be generated from Offer stage

### `purchase-approve` (from Procurement tab)
- 520px wide
- Item details, budget remaining, 3 quotations upload field (if >₹25,000)
- [Approve] [Request More Quotations] [Reject]

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/vp-admin/dashboard/` | Full dashboard |
| 2 | `GET` | `/api/v1/school/{id}/vp-admin/kpi-strip/` | KPI cards |
| 3 | `GET` | `/api/v1/school/{id}/transport/today-log/` | Transport morning log |
| 4 | `POST` | `/api/v1/school/{id}/transport/{bus_id}/mark-returned/` | Mark bus returned |
| 5 | `GET` | `/api/v1/school/{id}/admissions/today-enquiries/` | Today's enquiries |
| 6 | `GET` | `/api/v1/school/{id}/admissions/funnel/` | Admission funnel |
| 7 | `GET` | `/api/v1/school/{id}/admissions/rte-status/` | RTE compliance status |
| 8 | `GET` | `/api/v1/school/{id}/procurement/pending/` | Pending purchase requests |
| 9 | `POST` | `/api/v1/school/{id}/procurement/{id}/decide/` | Approve/reject purchase |
| 10 | `GET` | `/api/v1/school/{id}/hostel/summary/` | Hostel occupancy + attendance |
| 11 | `GET` | `/api/v1/school/{id}/maintenance/requests/?status=open` | Open maintenance requests |
| 12 | `GET` | `/api/v1/school/{id}/safety/compliance-calendar/?days=60` | Safety compliance upcoming items |

---

## 8. HTMX Patterns

```html
<!-- KPI strip refresh -->
<div id="vpadmin-kpi-strip"
     hx-get="/api/v1/school/{{ school_id }}/vp-admin/kpi-strip/"
     hx-trigger="every 5m"
     hx-target="#vpadmin-kpi-strip"
     hx-swap="outerHTML">
</div>

<!-- Transport log auto-refresh (every 10 min during school hours 6-9am and 2-6pm) -->
<div id="transport-log"
     hx-get="/school/admin/vp-admin/transport-log/"
     hx-trigger="every 10m[isSchoolTransportTime()]"
     hx-target="#transport-log"
     hx-swap="outerHTML">
</div>
```

---

## 9. Security & Performance

- VP Admin cannot view or modify academic content (syllabus, marks, results)
- All purchase approvals > ₹25,000 require 3-quotation upload (enforced in form validation)
- Transport emergency alert dispatch goes through WhatsApp SQS queue; VP sees real-time status
- CCTV status pulled from IoT integration (or manual check record if no integration)
- Dashboard tabs lazy-loaded; Transport and Admissions tabs pre-loaded on default Today view

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
