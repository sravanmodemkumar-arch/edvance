# 07 — Executive Secretary Dashboard

> **URL:** `/group/gov/secretary/`
> **File:** `07-secretary-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Executive Secretary (G3) — exclusive landing page

---

## 1. Purpose

Communication and coordination centre for the Group Executive Secretary. The Exec Secretary is
the operational link between Group HQ and all 50 branch principals — responsible for:
- Sending group-level circulars and tracking delivery per principal
- Preparing and managing board meeting agendas and minutes
- Managing all group-wide announcements (WhatsApp/SMS/Email)
- Maintaining the communication calendar and scheduling

The Exec Secretary has G3 write access for communications but CANNOT approve, configure,
provision users, or access financial/compliance data.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Executive Secretary | G3 | Full — communications & calendar sections | Exclusive dashboard |
| Chairman / MD | G5 | — | Own dashboards |
| CEO / President / VP | G4 | — | Own dashboards |
| Trustee / Advisor | G1 | — | Own dashboards |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Executive Secretary Dashboard
```

### 3.2 Page Header
```
Group Secretary — [Secretary Name]                     [+ Compose Circular]  [+ New Announcement]
Executive Secretary · Last login: [date time]          [+ Schedule Communication]
```

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Circulars Sent (Month) | `23` circulars | Info | → Principal Comms Hub page 20 |
| Pending Deliveries | `3 principals haven't opened` | Red if >0 | → Principal Comms Hub page 20 |
| Board Meetings (Quarter) | `1 upcoming` · date | Info | → Board Meeting Portal page 29 |
| Announcements Published | `8` this month | Info | → Group Announcements page 21 |
| Scheduled Communications | `5 upcoming` | Info | → Comm Calendar page 22 |
| Acknowledgements Pending | `4 principals` on latest policy | Yellow if >0 | → Policy Management page 19 (read-only) |

---

## 5. Sections

### 5.1 Circular Status Tracker

> Main work surface — all circulars sent this month with delivery tracking per principal.

**Search:** Circular title, recipient name. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Month | Month picker | Current month default |
| Status | Multi-select | All Delivered · Partial · None Opened |
| Type | Multi-select | Circular · Notice · Reminder · Emergency Alert |
| Branch | Multi-select | All branches |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Circular Title | Text + link | ✅ | Opens `circular-detail` drawer |
| Type | Badge | ✅ | Circular · Notice · Reminder · Alert |
| Sent Date | Date | ✅ | |
| Total Recipients | Number | ❌ | Count of branch principals |
| Delivered | Number + bar | ✅ | Green when 100% |
| Opened / Read | Number + bar | ✅ | |
| Pending | Number | ✅ | Red if >0 |
| Replies Received | Number | ❌ | If circular requested reply |
| Actions | — | ❌ | View · Resend to Pending · Download Report |

**Default sort:** Sent Date descending (most recent first).

**Pagination:** Server-side · Default 25/page.

**Row actions:**
| Action | Notes |
|---|---|
| View | Opens `circular-detail` drawer with per-principal delivery breakdown |
| Resend to Pending | `hx-post` → sends WhatsApp to non-opened principals · Toast: "Reminder sent to [N] principals" |
| Download Report | Downloads PDF with per-principal delivery audit |

---

### 5.2 Compose Circular (prominent CTA)

**Display:** Highlighted card with [+ Compose Circular] button (primary blue).

When clicked: Opens `communications-compose` drawer.

---

### 5.3 Upcoming Board Meeting Prep

> Preparation status for the next upcoming board meeting.

**Display:** Card — next meeting details + checklist.

| Field | Value |
|---|---|
| Next Meeting | BM-2026-Q2 |
| Date & Time | [date time] |
| Venue | [venue] |
| Chairperson | [name] |

**Preparation Checklist (inline):**
- [ ] Agenda finalised — [Upload Agenda] button
- [ ] Attendees confirmed — [Manage Attendees] button
- [ ] Previous minutes uploaded — [Upload Minutes] button
- [ ] Resolutions from last meeting — [View Resolutions] button

**Checklist item click:** Opens Board Meeting Portal (page 29) at the relevant tab.

**"View Board Meeting Portal →"** link.

---

### 5.4 Announcement Queue

> Drafted and scheduled announcements pending publishing.

**Display:** Compact list — max 5 items.

| Field | Notes |
|---|---|
| Title | Truncated |
| Type | Badge (WhatsApp / SMS / Email / In-app) |
| Targeting | "All students" / "Branch X" / "MPC students" |
| Scheduled | Date + time OR "Draft" |
| Status | Draft · Scheduled · Published |
| Actions | Edit · Publish Now · Cancel |

**"View All Announcements →"** link to page 21.

---

### 5.5 Communication Calendar (week view)

> Current week's communication schedule — compact view.

**Display:** 7-column week grid (Mon–Sun). Events displayed as coloured tags within date cells.

**Event types:** Circular (blue) · Announcement (green) · Exam Notification (orange) · Fee Reminder (yellow) · Board Meeting (purple) · Emergency Alert (red).

**Click event:** Opens event detail (edit for Secretary, read for others).

**"View Full Calendar →"** link to page 22.

**[+ Schedule Communication] button:** Opens `calendar-event-create` drawer.

---

## 6. Drawers & Modals

### 6.1 Drawer: `communications-compose`
- **Trigger:** [+ Compose Circular] button or header button
- **Width:** 680px
- **Tabs:** Compose · Template · Recipients · Schedule

#### Tab: Compose
| Field | Type | Required | Validation |
|---|---|---|---|
| Subject / Title | Text | ✅ | Min 5 chars, max 200 |
| Type | Select | ✅ | Circular · Notice · Reminder · Emergency Alert |
| Body | Rich text editor (TipTap) | ✅ | Min 20 chars · Char counter shown |
| Attachments | File upload | ❌ | PDF/DOCX/JPG · Max 5 files · 10MB each |
| Request Reply? | Checkbox | ❌ | If checked — reply deadline field appears |
| Reply Deadline | Date | Conditional | Required if Reply requested |

#### Tab: Template
- List of pre-built templates (Term Start, Exam Notice, Holiday Notice, Fee Reminder, Emergency)
- Click template → pre-fills Compose tab fields
- [Save as Template] button (saves current compose content as new template)

#### Tab: Recipients
| Field | Type | Required | Validation |
|---|---|---|---|
| Recipient Type | Radio | ✅ | All Principals · Select Branches · Select Individuals |
| Branches (if select) | Multi-select | Conditional | Shows list of all branches |
| Individuals (if select) | Multi-select | Conditional | Search by name |
| Preview count | Read-only | — | "Will send to N principals" |

#### Tab: Schedule
| Field | Type | Required | Validation |
|---|---|---|---|
| Send Now | Radio | ✅ | |
| Schedule for later | Radio | ✅ | |
| Scheduled Date & Time | Datetime picker | Conditional | Future datetime required |
| Delivery Channel | Checkbox group | ✅ | WhatsApp (default on) · Email · In-app |

**Submit:** "Send Circular" or "Schedule Circular" — disabled until all required fields valid.
**On success:** Drawer closes · toast · circular appears in Circular Status Tracker.

### 6.2 Drawer: `circular-detail`
- **Trigger:** Circular table → Title click or View action
- **Width:** 680px
- **Tabs:** Overview · Per-Principal Status · Replies

#### Tab: Overview
- Circular metadata (title, body, sent date, type, attachments)

#### Tab: Per-Principal Status
- Table: Principal Name · Branch · Status (Delivered/Opened/Not Opened) · Delivered At · Opened At
- Sortable by Status
- [Resend to Pending] button at top — sends WhatsApp to all "Not Opened" principals

#### Tab: Replies
- List of replies received with principal name, branch, reply text, timestamp
- Only shown if circular had "Request Reply" enabled

### 6.3 Drawer: `announcement-compose`
- **Width:** 680px
- **Tabs:** Compose · Targeting · Channel · Schedule · Preview
- **Channel tab:** WhatsApp Broadcast · SMS · Email · In-app — toggle each on/off
- **Preview tab:** Shows how announcement looks on each selected channel (character limit indicator for SMS: 160 chars)

### 6.4 Drawer: `calendar-event-create`
- **Width:** 520px
- **Tabs:** Details · Branches · Recurrence · Notify

#### Tab: Details
| Field | Type | Required | Validation |
|---|---|---|---|
| Title | Text | ✅ | Max 100 chars |
| Type | Select | ✅ | Circular · Announcement · Exam · Fee · Board Meeting · Emergency |
| Date | Date | ✅ | |
| Time | Time | ❌ | |
| Description | Textarea | ❌ | Max 300 chars |

#### Tab: Branches
- Applies to: All branches · Select branches

#### Tab: Recurrence
- One-time / Weekly / Monthly / Custom interval

#### Tab: Notify
- Notify who: Principals · All staff · Students and Parents
- Advance notice: 1 day · 3 days · 7 days before event

---

## 7. Charts

### 7.1 Circular Open Rate Trend (last 6 months)
- **Type:** Line chart
- **Data:** % of principals who opened circulars each month
- **X-axis:** Months
- **Y-axis:** Open rate %
- **Benchmark:** 90% target (dashed horizontal)
- **Tooltip:** Month · Open rate: X% · Circulars sent: N
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Circular sent | "Circular sent to [N] principals" | Success | 4s |
| Circular scheduled | "Circular scheduled for [date time]" | Info | 4s |
| Resend triggered | "Reminder sent to [N] principals who haven't opened" | Success | 4s |
| Announcement published | "Announcement published to [N] recipients" | Success | 4s |
| Calendar event created | "Communication scheduled on [date]" | Success | 4s |
| Send error | "Failed to send circular. Check your connection and try again." | Error | Manual |
| Attachment too large | "Attachment exceeds 10MB. Please compress and re-upload." | Warning | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No circulars this month | "No circulars sent this month" | "Compose your first circular to branch principals" | [+ Compose Circular] |
| No pending deliveries | "All circulars delivered and opened" | "Every principal has opened this month's circulars" | — |
| No board meeting upcoming | "No upcoming board meeting" | "Board meetings will appear here once scheduled" | [Schedule Meeting] |
| No announcements in queue | "No announcements scheduled" | "Schedule your next announcement to students or staff" | [+ New Announcement] |
| Empty comm calendar | "No communications scheduled" | "Add communications to your calendar to track them" | [+ Schedule] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 6 KPI cards + circular table (8 rows) + board prep card + calendar grid |
| Circular table filter | Inline skeleton rows |
| Compose drawer open | Spinner in drawer body |
| Send circular submit | Full-page overlay "Sending to [N] principals…" |
| Resend to pending | Spinner in Resend button |
| Calendar load | Grid skeleton |

---

## 11. Role-Based UI Visibility

| Element | Exec Secretary G3 | G1 Trustee/Advisor | G4/G5 |
|---|---|---|---|
| Page | ✅ | ❌ redirect | ❌ redirect |
| [+ Compose Circular] | ✅ | ❌ | ❌ |
| [+ New Announcement] | ✅ | ❌ | ❌ |
| [Resend to Pending] in table | ✅ | ❌ | ❌ |
| Board meeting prep [Upload] buttons | ✅ | ❌ | ❌ |
| [Edit] on announcement queue | ✅ | ❌ | ❌ |
| [+ Schedule Communication] | ✅ | ❌ | ❌ |
| Circular body content (view) | ✅ | ❌ | ✅ (via page 20) |

> Note: Communications hub page 20 is where G4/G5 can VIEW circulars. The Secretary's
> dashboard is the only place where G3 can COMPOSE and SEND.

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/secretary/dashboard/` | JWT (G3 Sec) | Full secretary dashboard |
| GET | `/api/v1/group/{id}/communications/circulars/` | JWT (G3) | Circulars list |
| POST | `/api/v1/group/{id}/communications/circulars/` | JWT (G3) | Create and send circular |
| GET | `/api/v1/group/{id}/communications/circulars/{cid}/delivery/` | JWT (G3) | Per-principal delivery status |
| POST | `/api/v1/group/{id}/communications/circulars/{cid}/resend/` | JWT (G3) | Resend to non-opened |
| GET | `/api/v1/group/{id}/announcements/?status=draft,scheduled` | JWT (G3) | Announcement queue |
| POST | `/api/v1/group/{id}/announcements/` | JWT (G3) | Create announcement |
| GET | `/api/v1/group/{id}/board-meetings/?upcoming=true` | JWT (G3) | Next board meeting |
| GET | `/api/v1/group/{id}/calendar/events/?week=current` | JWT (G3) | Current week events |
| POST | `/api/v1/group/{id}/calendar/events/` | JWT (G3) | Create calendar event |
| GET | `/api/v1/group/{id}/communications/open-rate-trend/` | JWT (G3) | 6-month open rate chart |

---

## HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Circular status table search | `input delay:300ms` | GET `.../communications/?q=` | `#circular-table-body` | `innerHTML` |
| Circular filter apply | `click` | GET `.../communications/?status=&date=` | `#circular-table-section` | `innerHTML` |
| Open compose drawer | `click` | GET `.../communications/new/` | `#drawer-body` | `innerHTML` |
| Open circular detail drawer | `click` | GET `.../communications/{cid}/` | `#drawer-body` | `innerHTML` |
| Announcement queue filter | `click` | GET `.../announcements/?status=pending` | `#announcement-queue` | `innerHTML` |
| Calendar week navigation | `click` | GET `.../comm-calendar/?week=` | `#calendar-week-view` | `innerHTML` |
| Board meeting checklist update | `change` | PUT `.../board-meetings/{mid}/checklist/` | `#meeting-checklist` | `innerHTML` |
| Stats bar auto-refresh | `every 5m` | GET `.../secretary/dashboard/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
