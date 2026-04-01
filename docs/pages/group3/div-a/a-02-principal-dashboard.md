# A-02 — Principal Dashboard

> **URL:** `/school/admin/principal/`
> **File:** `a-02-principal-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — exclusive landing page; Promoter (S7) — read access

---

## 1. Purpose

Primary post-login landing for the Principal. The Principal is the central operational authority — every critical school function either requires their approval or reports up to them. This dashboard is a live command centre, not a summary report. It is designed for the Principal who logs in at 7:45 AM before school starts and needs to know: Who is absent today (staff and students)? What's happening in exams? Are there any parent escalations? What needs my signature right now?

**Indian school reality:** The Indian school Principal is simultaneously:
- The academic head (signs report cards, approves syllabi)
- The HR head (approves all staff leave)
- The communications officer (sends CBSE/state board reports)
- The CBSE Centre Superintendent (during board exams)
- The POCSO designated person (receives and manages complaints)
- The financial co-signatory (countersigns cheques above a threshold)
- The public face of the school (parent communication, media)

No equivalent Western "headteacher" role has this breadth. The dashboard must serve all these contexts without becoming overwhelming.

---

## 2. Role Access

| Role | Level | Access |
|---|---|---|
| Principal | S6 | Full — all sections, all actions |
| Promoter / Correspondent | S7 | Read — KPI cards + alerts; no write actions on this page |
| VP Academic | S5 | — (has own dashboard) |
| VP Administration | S5 | — (has own dashboard) |

> **Access:** `@require_role_min('vp')` with special routing: Principal → this page; others → their own dashboard.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
[School Name]  ›  Principal Dashboard
```

### 3.2 Page Header
```
Good morning, [Principal Name]                          [Quick Action ▼]  [⚙]
[School Name] · Principal · Academic Year [2025–26 ▼]  Today: [Wed, 26 Mar 2026]
```

**[Quick Action ▼] dropdown:**
- + New Circular
- Approve Leave Requests (badge: count pending)
- Mark Today's Absent Staff
- View Today's Exam Schedule
- Emergency Announcement

### 3.3 Critical Alert Banner (conditional — shown only when alerts exist)

Priority 1 (red):
- Any open POCSO complaint (even 1 = red)
- Board exam running today + more than 5% absent invigilators
- CBSE affiliation document expired (not just expiring)
- Staff with BGV expired and direct student contact today

Priority 2 (amber):
- Staff attendance < 85% today
- Parent complaint open > 3 days without resolution
- Pending approval for > 5 days
- Any class without a teacher for a scheduled period (timetable gap)

---

## 4. KPI Summary Strip (8 cards, horizontal scroll on mobile)

> HTMX auto-refresh every 5 minutes: `hx-trigger="every 5m"` on `#principal-kpi-strip`

| # | Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|---|
| 1 | Student Attendance Today | `87.4% (924 / 1,057 present)` | Green ≥90% · Amber 80–89% · Red <80% | → div-e Attendance |
| 2 | Staff Attendance Today | `94% (75 / 80 present)` | Green ≥95% · Amber 85–94% · Red <85% | → A-17 Staff Attendance |
| 3 | Pending Approvals | `12 items` (leave: 8, purchase: 2, admission: 2) | Badge pulses if > 5 | → A-23 Approval Hub |
| 4 | Fee Collection (This Month) | `₹42.3L (78.3% of target)` | Green ≥90% · Amber 75–89% · Red <75% | → A-20 Fee Dashboard |
| 5 | Exams Today | `3 running` (Class X Pre-board, Class IX Mid-term, Class V Unit Test) | Blue = running · Grey = none | → div-f Exam Ops |
| 6 | Open Parent Complaints | `4 open` (1 > 3 days) | Green = 0 · Amber = 1–5 · Red = >5 or any >3 days | → A-28 Parent Comms Log |
| 7 | BGV Compliance | `94.3%` (76/80 verified) | Green ≥98% · Amber 90–97% · Red <90% (POCSO alert) | → A-16 Staff Directory |
| 8 | POCSO Status | `0 open cases` | Green = 0 · Red = any open | → A-30 POCSO Centre |

---

## 5. Main Sections

### 5.1 Today's View (default active tab)

**Layout: 3-column grid (left 40% · centre 35% · right 25%)**

#### 5.1.1 Left Column — Attendance Summary

**Student Attendance by Class (table)**
| Class | Section | Total | Present | % | Status |
|---|---|---|---|---|---|
| XII | A | 45 | 43 | 95.6% | ✅ |
| XII | B | 44 | 38 | 86.4% | ⚠️ |
| … | … | … | … | … | … |
| I | A | 35 | 31 | 88.6% | ⚠️ |

- Filterable by class, section, status
- Click any row → opens student absentee list for that class
- [Send Absentee SMS to Parents] bulk action (WhatsApp/SMS broadcast)
- Late arrivals shown with "L" badge

**Staff Absent Today** (compact list, max 5 visible, "View All" link)
- Name · Subject/Class · Substituted by (if arranged) · [Arrange Substitute]
- If substitute not arranged → row highlights in red with [Urgent: Arrange Now]

#### 5.1.2 Centre Column — Exams & Schedule

**Running Exams (if any)**
- For each running exam:
  - Exam name · Class · Room · Invigilator(s) · Status: RUNNING / NOT STARTED / COMPLETED
  - Time remaining (live countdown)
  - [Monitor] link → div-f Exam Support

**Today's Timetable Gaps** (if any)
- Periods with no assigned teacher (absent teacher + no substitute)
- "Period 3, Class VIII B — Math — No substitute arranged" [Assign Now]

#### 5.1.3 Right Column — Quick Decisions

**Pending Leave Approvals (today's urgent)**
- List of leaves that start today or tomorrow (needs approval now)
- Each item: Staff name · Type · Dates · [✅ Approve] [❌ Reject]
- HTMX inline approve/reject — no page reload

**Today's Events** (from Academic Calendar)
- List: PTM session at 2pm · Class XI Annual Day rehearsal · Sports day meeting
- [View Full Calendar →]

---

### 5.2 Tab: Academic Overview

**5.2.1 This Week's Homework Completion Rate (per class)**
- Bar chart: Class on X-axis, completion % on Y-axis
- Colour: ≥80% green · 60–79% amber · <60% red
- Drill-down: click any bar → class-wise subject breakdown

**5.2.2 Last Exam Performance Summary**
- Table: Class · Exam Name · Avg Score · Pass % · Topper Score · Below 40% Count
- [View Full Results →] link to div-f Results page

**5.2.3 Syllabus Completion Status** (by dept/class)
- Table: Dept · Class · Subjects · % Covered · Expected by Now · Delta
- [View Full Syllabus Tracker →] link to div-b pages

---

### 5.3 Tab: Parent & Communication

**5.3.1 Open Parent Complaints / Queries**
- Table: Student name · Class · Complaint date · Category · Assigned to · Days open · Status
- Categories: Academic · Fee · Transport · Safety/POCSO · Behaviour · Other
- [Open →] any row → opens parent communication detail drawer

**5.3.2 Recent Circulars / Notices Sent**
- List: Title · Date · Channel (WhatsApp/SMS/In-app) · Delivered count · Read count
- [+ New Circular] button → opens circular-compose drawer

**5.3.3 Upcoming PTM Schedule**
- Next PTM date, registered parent count, confirmed vs total
- [View PTM Manager →] link

---

### 5.4 Tab: Finance Snapshot

**5.4.1 Month-to-date Fee Collection**
- Donut chart: Collected vs Pending vs Overdue (> 30 days)
- Numbers: ₹42.3L collected, ₹8.7L pending, ₹3.1L overdue
- [View Fee Dashboard →] A-20

**5.4.2 Fee Defaulters Alert**
- Top 10 students by outstanding amount (> 60 days)
- Name · Class · Outstanding · Last Payment · [Send Notice]

**5.4.3 Salary Disbursement Status** (current month)
- Status: PENDING / PROCESSED / PAID
- If pending → date expected; if overdue → red alert
- [View Payroll →] A-22

---

### 5.5 Tab: Compliance & Safety

**5.5.1 Compliance Items Due Soon**
- Table: Item · Regulation · Due Date · Status · [Act]
- Pre-sorted by urgency (expired first, then soonest due)

**5.5.2 POCSO Dashboard Summary**
- Training coverage: XX% trained, YY staff overdue
- Open cases: 0 (or count with red badge)
- Last drill/training date
- [View POCSO Centre →] A-30

**5.5.3 BGV Status Summary**
- Total staff: XX · Verified: XX · Pending: XX · Expired: XX
- [View Staff Directory →] A-16

---

## 6. Drawers

### `leave-approve` (inline from Section 5.1.3)
- 420px wide
- Shows: Staff name, leave type (CL/EL/SL/ML/Paternity/LWP), dates, reason, total balance, history last 6 months
- [Approve] [Reject with reason] [Ask for document]

### `parent-complaint-detail` (from Section 5.3.1)
- 640px wide
- Tabs: Complaint details · Child record · History · Action
- Action: [Assign to VP/HOD] [Mark Resolved] [Escalate to POCSO]
- If category = Safety/POCSO: [Escalate to POCSO Centre] appears prominently

### `circular-compose` (from + New Circular)
- 680px wide
- Tabs: Compose · Audience · Channels · Schedule · Preview
- Compose: Rich text editor, subject line, attachment upload
- Audience: All parents · All staff · Specific classes · Specific sections · Custom list
- Channels: WhatsApp (if subscribed) · SMS · In-app notification · Email
- Schedule: Send now · Schedule for [date/time]
- Preview: Per-channel preview with character count

### `substitute-arrange` (from Today's View staff absent list)
- 480px wide
- Absent teacher name + period(s) affected
- Suggested substitutes (staff with free periods in those slots — from timetable)
- [Assign] button per period
- Email/WhatsApp notification to substitute teacher sent on confirmation

---

## 7. Charts

### 7.1 Student Attendance Trend (last 30 days)
- Section: Academic Overview tab
- Line chart, daily values
- Secondary line: industry benchmark (typically 90%)
- API: `GET /api/v1/school/{id}/attendance/student-trend/?days=30`

### 7.2 Homework Completion Rate by Class (last week)
- Bar chart, per class
- API: `GET /api/v1/school/{id}/homework/completion-rate/`

### 7.3 Fee Collection Donut (Finance Tab)
- Donut: Collected/Pending/Overdue
- API: `GET /api/v1/school/{id}/finance/collection-status/?month=current`

---

## 8. Toast Notifications

| Trigger | Type | Message |
|---|---|---|
| Leave approved (inline) | Success | "Leave approved. [Staff Name] notified via WhatsApp." |
| Leave rejected | Info | "Leave rejected. Reason sent to [Staff Name]." |
| Circular sent | Success | "Circular sent to [X parents, Y staff] via [channels]." |
| Substitute arranged | Success | "Substitute arranged: [Name] for Period [X], [Class]." |
| Complaint resolved | Success | "Parent complaint marked resolved. Parent notified." |
| POCSO escalation | Info | "Escalated to POCSO Centre. Case ID: [#]. Response within 24h required." |

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/principal/dashboard/` | Full dashboard data |
| 2 | `GET` | `/api/v1/school/{id}/principal/kpi-strip/` | KPI strip refresh (HTMX) |
| 3 | `GET` | `/api/v1/school/{id}/attendance/today/summary/` | Today's student + staff attendance |
| 4 | `GET` | `/api/v1/school/{id}/attendance/today/class-table/` | Per-class attendance table |
| 5 | `GET` | `/api/v1/school/{id}/staff/absent-today/` | Absent staff with substitute status |
| 6 | `GET` | `/api/v1/school/{id}/exams/today/` | Running/scheduled exams today |
| 7 | `GET` | `/api/v1/school/{id}/timetable/gaps/today/` | Timetable gaps (no teacher) |
| 8 | `GET` | `/api/v1/school/{id}/approvals/?status=pending&urgent=true` | Urgent pending approvals |
| 9 | `POST` | `/api/v1/school/{id}/approvals/{approval_id}/decide/` | Approve/reject leave etc. |
| 10 | `GET` | `/api/v1/school/{id}/parent-complaints/?status=open` | Open parent complaints |
| 11 | `POST` | `/api/v1/school/{id}/parent-complaints/{id}/action/` | Assign/resolve/escalate |
| 12 | `GET` | `/api/v1/school/{id}/circulars/?limit=5&order=-date` | Recent circulars |
| 13 | `POST` | `/api/v1/school/{id}/circulars/` | Create + send circular |
| 14 | `GET` | `/api/v1/school/{id}/finance/collection-status/?month=current` | Fee collection summary |
| 15 | `GET` | `/api/v1/school/{id}/finance/top-defaulters/?days=60` | Defaulter list |
| 16 | `GET` | `/api/v1/school/{id}/principal/alerts/` | Critical alert banner |
| 17 | `GET` | `/api/v1/school/{id}/compliance/snapshot/` | Compliance items due soon |
| 18 | `POST` | `/api/v1/school/{id}/timetable/substitutes/assign/` | Assign substitute teacher |

---

## 10. HTMX Patterns

### 10.1 KPI Strip Auto-Refresh
```html
<div id="principal-kpi-strip"
     hx-get="/api/v1/school/{{ school_id }}/principal/kpi-strip/"
     hx-trigger="every 5m"
     hx-target="#principal-kpi-strip"
     hx-swap="outerHTML">
  <!-- 8 KPI cards -->
</div>
```

### 10.2 Tab Navigation
```html
<div class="tab-nav">
  <button hx-get="/school/admin/principal/tab/today/"
          hx-target="#principal-tab-content"
          hx-push-url="?tab=today"
          class="tab-btn active">Today's View</button>
  <button hx-get="/school/admin/principal/tab/academic/"
          hx-target="#principal-tab-content"
          hx-push-url="?tab=academic">Academic</button>
  <button hx-get="/school/admin/principal/tab/parents/"
          hx-target="#principal-tab-content"
          hx-push-url="?tab=parents">Parent & Comms</button>
  <button hx-get="/school/admin/principal/tab/finance/"
          hx-target="#principal-tab-content"
          hx-push-url="?tab=finance">Finance</button>
  <button hx-get="/school/admin/principal/tab/compliance/"
          hx-target="#principal-tab-content"
          hx-push-url="?tab=compliance">Compliance</button>
</div>
<div id="principal-tab-content"><!-- Tab content --></div>
```

### 10.3 Inline Leave Approval
```html
<form hx-post="/api/v1/school/{{ school_id }}/approvals/{{ leave_id }}/decide/"
      hx-target="#leave-row-{{ leave_id }}"
      hx-swap="outerHTML">
  <input type="hidden" name="decision" value="APPROVED">
  <button type="submit" class="btn-sm-primary">✅ Approve</button>
</form>
```

### 10.4 Student Attendance Table Refresh (for class drill-down)
```html
<div id="attendance-class-table"
     hx-get="/school/admin/principal/attendance/class-table/"
     hx-trigger="change from:#class-filter"
     hx-target="#attendance-class-table"
     hx-include="#class-filter">
  <!-- Per-class attendance table -->
</div>
```

---

## 11. Security

- **POCSO section:** All POCSO data rendered in a separate, permission-gated section; only Principal (S6+) can view case details; all accesses logged
- **Leave approval audit:** Every approval/rejection logged with actor, timestamp, IP, and decision
- **Circular dispatch:** Bulk WhatsApp/SMS dispatch requires 2-step confirmation (compose → review → confirm send); WhatsApp gateway rate limits enforced
- **Session:** Principal session = 4 hours idle timeout (school hours context); after timeout, redirected to re-login
- **Substitute assignment:** Only logged-in Principal or VP Admin can assign; creates `timetable_substitute` record with actor audit trail

---

## 12. Performance

| Concern | Approach |
|---|---|
| Dashboard load time | Attendance data is the heaviest query; pre-computed at 7:00 AM daily by Celery task per school; updated on each attendance marking event |
| KPI strip | Cached per school with 5-min TTL; invalidated on attendance/fee/approval events |
| Today's exam schedule | Direct DB query (must be real-time) — indexed on `exam_date` and `school_id` |
| Tab content | Loaded lazily via HTMX on tab click; not all tabs loaded on initial page load |
| Circular send | Dispatched via SQS → Lambda → WhatsApp/SMS gateway; principal sees "Sending…" toast until SQS acknowledges, then "Sent" |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
