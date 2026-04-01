# A-05 — Administrative Officer Dashboard

> **URL:** `/school/admin/office/`
> **File:** `a-05-office-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Administrative Officer / School Secretary (S3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Administrative Officer (also called School Secretary, Office Superintendent, or Front Office Manager in different school systems). This role is the operational hub of the school's paperwork and communication: circulars go out through them, visitors are logged by them, staff records are maintained by them, and the daily morning report is compiled by them. They are the school's institutional memory for all documented processes.

**Indian school context:** The Administrative Officer in an Indian school manages:
- The school's official correspondence (CBSE/state board letters, legal notices)
- Visitor registers (mandatory under CBSE/state board norms, POCSO)
- Staff and student record registers (attendance registers must be maintained in prescribed formats)
- TCR (Transfer Certificate) issuance workflow
- CBSE OASIS / state board UDISE+ data entry
- Affiliation renewal documentation collection
- Daily attendance reporting to the Principal

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Administrative Officer | S3 | Full — all sections on this page |
| Principal | S6 | — (has own dashboard) |
| VP Administration | S5 | Read access to this page |

---

## 3. Page Header
```
Good morning, [Officer Name]                            [Quick Action ▼]  [⚙]
Administrative Officer · [School Name] · Year [2025–26 ▼]
```

**[Quick Action ▼]:**
- + New Circular
- Log Visitor
- TC Request (new)
- Search Student Record

---

## 4. KPI Strip (5 cards)

> HTMX refresh every 10m on `#office-kpi-strip`

| # | Card | Metric | Colour | Drill-down |
|---|---|---|---|---|
| 1 | Circulars Sent Today | `3 sent · 2 pending dispatch` | Blue | → Circular Manager A-27 |
| 2 | Visitors Today | `12 logged` (8 parent, 3 vendor, 1 official) | Blue | → Visitor Log |
| 3 | TC Requests Pending | `2 pending` (1 urgent) | Amber if >0 | → Student Records |
| 4 | Staff Leave Requests Pending | `6 awaiting approval` | Amber if >0 | → A-18 Leave |
| 5 | Correspondence Pending Reply | `3 items` (1 CBSE letter) | Red if any official letter > 7 days | → Correspondence Register |

---

## 5. Main Sections

### 5.1 Tab: Today's Tasks

**5.1.1 Morning Checklist**
Configurable checklist the office runs every school day. Checked off item by item:
- [ ] Take student attendance summary from class registers (or verify digital entry complete)
- [ ] Check staff attendance and compile morning absentee report
- [ ] Dispatch any queued circulars
- [ ] Log gate opening time
- [ ] Review visitor log completeness from yesterday

**5.1.2 Pending Circular Dispatch**
- Table: Title · Audience · Channel · Scheduled Time · Status
- Status: PENDING / SENDING / SENT / FAILED
- [Dispatch Now] for pending items
- [View Details] for in-progress

**5.1.3 Today's Visitor Log**
- Table: Time · Visitor Name · Purpose · Meeting With · ID Verified · Exit Time
- [+ Log Visitor] button (always visible, primary action on this page)
- POCSO requirement: all visitor IDs logged and photo captured (mandatory for all visitors to school premises)

---

### 5.2 Tab: Circular & Correspondence

**5.2.1 Circulars (last 30 days)**
- Table: Title · Date · Audience · Channel · Sent to (count) · Delivered % · Read %
- [+ New Circular] button
- [Resend Undelivered] for any circular with < 80% delivery

**5.2.2 Official Correspondence Register**
- Table: Date · From/To · Subject · Reference No · Due Date (if reply needed) · Status
- Incoming: CBSE letters, state board notices, municipal letters, legal notices
- Outgoing: NOC requests, affiliation renewal letters, fee hike applications
- [+ Add Entry] [Upload Scan]
- Flag any incoming item where reply is due within 7 days

**5.2.3 Circular Templates**
- Pre-saved templates: School Opening · Exam Date Notice · Holiday Announcement · Fee Reminder · PTM Invitation
- [Use Template] → opens circular-compose drawer pre-filled

---

### 5.3 Tab: Student Records

**5.3.1 Transfer Certificate (TC) Requests**
- Table: Student · Class · Request Date · Reason · Documents Received · Status
- Status: PENDING · IN PROCESS · READY TO ISSUE · ISSUED
- [Process TC] → opens TC workflow drawer
- TC issuance requires Principal approval (routed through A-23 Approval Hub)

**5.3.2 Student Record Search**
- Search by: Name · Roll No · Admission No · Parent Name
- Returns: student profile summary (read-only) + links to marks/attendance for Principal/VP access

**5.3.3 New Student Documents Pending**
- Students admitted this session whose document folder is incomplete
- Table: Student · Class · Missing Documents · Deadline
- [Send Reminder to Parent] per row

---

### 5.4 Tab: Staff Records

**5.4.1 Joining / Relieving Register** (current month)
- New joiners this month: name, date, designation
- Departures this month: name, last date, reason
- [+ Record Joiner] [+ Record Departure]

**5.4.2 Leave Register Summary**
- Total leaves taken per type this month: CL/EL/SL/ML/Paternity/LWP
- Department-wise leave balance summary
- [View Full Leave Register →] A-18

**5.4.3 Service Register Pending Updates**
- Staff whose service records need updating (address change, qualification update, salary revision)
- [Send Reminder] per staff

---

## 6. Drawers

### `log-visitor` (primary)
- 480px wide
- Fields: Name · Organization/Relation · Purpose · Meeting With (staff selector) · ID Type · ID Number · Photo capture (webcam or upload) · Vehicle No (optional)
- [Log In] → creates record; auto-sets Entry Time = now
- Later: [Log Out] → sets Exit Time

### `tc-workflow` (TC processing)
- 560px wide
- Tabs: Request Details · Documents Check · TC Preview · Issue
- Documents check: checkbox list (Original TC from previous school / Birth certificate / Transfer reason letter)
- TC Preview: rendered TC in CBSE/state board prescribed format
- Issue: [Generate TC PDF] → goes to Principal for digital signature approval
- After Principal approval: [Download TC] + status changes to ISSUED

### `circular-compose` (same as defined in A-02)
- 680px wide — reused component

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/office/dashboard/` | Dashboard data |
| 2 | `GET` | `/api/v1/school/{id}/office/kpi-strip/` | KPI strip refresh |
| 3 | `GET` | `/api/v1/school/{id}/visitors/today/` | Today's visitor log |
| 4 | `POST` | `/api/v1/school/{id}/visitors/` | Log new visitor |
| 5 | `PATCH` | `/api/v1/school/{id}/visitors/{id}/exit/` | Record visitor exit |
| 6 | `GET` | `/api/v1/school/{id}/circulars/?days=30` | Recent circulars |
| 7 | `POST` | `/api/v1/school/{id}/circulars/` | Create + dispatch circular |
| 8 | `GET` | `/api/v1/school/{id}/correspondence/` | Official correspondence register |
| 9 | `POST` | `/api/v1/school/{id}/correspondence/` | Add correspondence entry |
| 10 | `GET` | `/api/v1/school/{id}/students/tc-requests/` | TC request list |
| 11 | `POST` | `/api/v1/school/{id}/students/{id}/tc/initiate/` | Initiate TC process |
| 12 | `GET` | `/api/v1/school/{id}/students/{id}/tc/preview/` | TC PDF preview |
| 13 | `GET` | `/api/v1/school/{id}/staff/joining-relieving/?month=current` | Joining/relieving register |

---

## 8. HTMX Patterns

```html
<!-- Visitor log new entry inline append -->
<form hx-post="/api/v1/school/{{ school_id }}/visitors/"
      hx-target="#visitor-table-body"
      hx-swap="afterbegin"
      hx-on::after-request="this.reset()">
  <!-- Visitor form fields -->
  <button type="submit">Log In</button>
</form>

<!-- KPI refresh -->
<div id="office-kpi-strip"
     hx-get="/api/v1/school/{{ school_id }}/office/kpi-strip/"
     hx-trigger="every 10m"
     hx-target="#office-kpi-strip"
     hx-swap="outerHTML">
</div>
```

---

## 9. Security & Compliance

- **Visitor log is legally required** under CBSE/POCSO norms; all entries are immutable once saved (can add notes but not delete)
- **TC issuance** requires Principal digital approval before PDF is generated; prevents duplicate/fraudulent TCs
- **Circular dispatch** for non-teaching events (holidays, fee notices) can be done by Admin Officer without Principal approval; circulars about academic/disciplinary matters require VP or Principal pre-approval
- Admin Officer cannot access financial data (fee collection, salary) — those tabs are hidden server-side for S3 role

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
