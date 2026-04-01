# 29 — Board Meeting Portal

> **URL:** `/group/gov/board-meetings/`
> **File:** `29-board-meeting-portal.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Chairman G5 · MD G5 · CEO G4 · Trustee G1 · Exec Secretary G3 (full) · Advisor G1 (read)

---

## 1. Purpose

Central hub for all board and governing body meetings of the institution group. Manages meeting
scheduling, agenda creation, pre-read document distribution, attendance tracking, resolution
recording, and minutes publication.

Exec Secretary has full operational control (schedule, agenda, minutes, document upload).
Chairman/MD approve resolutions. Trustees and Advisors access meeting materials and record attendance.

---

## 2. Role Access

| Role | Schedule Meetings | Create Agenda | Upload Docs | Record Minutes | Approve Resolutions | View Only |
|---|---|---|---|---|---|---|
| Chairman | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| MD | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| CEO | ✅ | ✅ | ✅ | ❌ | ❌ | — |
| Exec Secretary | ✅ | ✅ | ✅ | ✅ | ❌ | — |
| Trustee | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Advisor | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Board Meeting Portal
```

### 3.2 Page Header
```
Board Meeting Portal                                   [+ Schedule Meeting]  [Export ↓]
[N] meetings this year · Next: [Meeting Name] on [Date]  (role-based button visibility)
```

### 3.3 Tabs
```
Upcoming Meetings  |  Past Meetings  |  Resolutions Register  |  Document Library
```

---

## 4. Upcoming Meetings Tab

**Search:** Meeting title, type. Debounce 300ms.

**Filters:** Type · Status · Date range.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Meeting Title | Text + link | ✅ | Opens meeting-detail drawer |
| Type | Badge | ✅ | AGM · EGM · Board Review · Finance Committee · Academic Committee · Emergency |
| Scheduled Date | Date | ✅ | DD MMM YYYY |
| Time | Text | ❌ | HH:MM + timezone |
| Venue | Text | ❌ | Physical or [Virtual — Google Meet/Teams link] |
| Status | Badge | ✅ | Scheduled · Agenda Confirmed · In Progress · Completed · Cancelled |
| Agenda Items | Number | ✅ | Count of agenda items |
| Attendees | Number | ✅ | Invited count |
| Board Pack | Badge | ❌ | Ready · Pending · Not Created |
| Actions | — | ❌ | View · Edit · Cancel · Send Board Pack |

**Default sort:** Scheduled Date ascending (soonest first).

**Pagination:** 25/page.

---

## 5. Past Meetings Tab

**Search:** Meeting title. Debounce 300ms.

**Filters:** Type · Year · Quorum Met (Yes/No) · Has Minutes (Yes/No).

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Meeting Title | Text + link | ✅ | Opens meeting-detail drawer |
| Type | Badge | ✅ | |
| Date | Date | ✅ | |
| Quorum Met | Badge | ✅ | ✅ Yes · ❌ No |
| Attendees | Text | ✅ | e.g. "8 / 12 invited" |
| Resolutions Passed | Number | ✅ | |
| Minutes | Badge | ✅ | Published · Draft · Not Created |
| Actions | — | ❌ | View · Download Minutes · View Resolutions |

**Default sort:** Date descending (most recent first).

**Pagination:** 25/page.

---

## 6. Resolutions Register Tab

> Searchable register of all board resolutions ever passed.

**Search:** Resolution number, title, keyword. Debounce 300ms.

**Filters:** Status · Category · Date range · Meeting type.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Resolution No. | Text | ✅ | RES-2026-001 format |
| Title | Text (truncated 60 chars) | ✅ | |
| Category | Badge | ✅ | Financial · Academic · HR · Expansion · Compliance · Administrative |
| Meeting | Text | ✅ | Linked meeting name + date |
| Date Passed | Date | ✅ | |
| Status | Badge | ✅ | Active · Implemented · Superseded · Revoked |
| Passed By | Text | ❌ | Name of presiding authority |
| Actions | — | ❌ | View · Download · Mark Implemented |

**Default sort:** Date Passed descending.

**Pagination:** 25/page.

---

## 7. Document Library Tab

> All board documents — pre-reads, presentations, minutes, reports.

**Search:** Document name. Debounce 300ms.

**Filters:** Document Type · Meeting · Year · Uploaded By.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Document Name | Text + icon | ✅ | File type icon (PDF/PPT/DOCX) |
| Type | Badge | ✅ | Board Pack · Agenda · Minutes · Pre-Read · Resolution · Financial Report · Other |
| Meeting | Text | ✅ | Associated meeting |
| Uploaded By | Text | ✅ | |
| Upload Date | Date | ✅ | |
| File Size | Text | ❌ | KB/MB |
| Access | Badge | ❌ | All Trustees · Chairman/MD Only |
| Actions | — | ❌ | View · Download · Delete (uploader or Chairman/MD) |

**Pagination:** 25/page.

---

## 8. Drawers & Modals

### 8.1 Drawer: `meeting-create` / `meeting-edit`
- **Trigger:** [+ Schedule Meeting] or [Edit] on meeting row
- **Width:** 760px
- **Tabs:** Details · Agenda · Attendees · Documents · Notifications

#### Tab: Details
| Field | Type | Required | Validation |
|---|---|---|---|
| Meeting Title | Text | ✅ | Min 5, max 150 chars |
| Meeting Type | Select | ✅ | AGM · EGM · Board Review · Finance Committee · Academic Committee · Emergency |
| Date | Date | ✅ | Future date |
| Start Time | Time | ✅ | |
| End Time | Time | ✅ | After start time |
| Venue Type | Radio | ✅ | Physical · Virtual · Hybrid |
| Venue / Link | Text | Conditional | Physical address or meeting URL |
| Meeting Number | Text | ❌ | Auto-generated or manual override |
| Quorum Required | Number | ✅ | Min attendees for valid meeting |
| Description / Agenda Summary | Textarea | ❌ | Max 500 chars |

#### Tab: Agenda
- **Display:** Ordered list of agenda items (drag to reorder)
- **Add Item:** [+ Add Agenda Item] button — opens inline form

**Per agenda item fields:**
| Field | Type | Required |
|---|---|---|
| Item Number | Auto-increment | — |
| Title | Text | ✅ |
| Presenter | Search + select | ❌ |
| Duration (minutes) | Number | ❌ |
| Item Type | Select | ✅ | Discussion · Decision · Information · Resolution · AOB |
| Description / Notes | Textarea | ❌ |
| Pre-Read Document | File upload | ❌ |

- Total estimated duration shown (sum of item durations).
- [Remove] per item. Drag handle to reorder.

#### Tab: Attendees
| Field | Type | Required |
|---|---|---|
| Invite from Platform Users | Multi-select | ✅ (at least 1) |
| Add External Attendees | Repeater: Name + Email + Role | ❌ |
| Mark as Mandatory | Toggle per attendee | ❌ |

- **Quorum warning:** If mandatory attendees < quorum required → yellow warning.
- Auto-populates with board members (Chairman, MD, Trustees, Advisors).

#### Tab: Documents
- **Pre-Meeting Documents:**
  - Upload: multiple files (PDF/PPT/DOCX/XLSX) · Max 50MB per file
  - Doc type tag per upload: Board Pack · Agenda · Pre-Read · Financial Report · Other
  - Access level: All Invitees · Chairman/MD Only
- **Board Pack auto-generate:** [Generate Board Pack] — compiles agenda + attached docs into single PDF

#### Tab: Notifications
| Field | Type | Required |
|---|---|---|
| Send Meeting Invite | Toggle | ✅ | Default On |
| Invite Channel | Multi-select | ✅ | WhatsApp · Email |
| Send Reminder | Toggle | ❌ | Default On |
| Reminder Before | Select | ❌ | 7 days · 3 days · 1 day · Day of |
| Send Board Pack When | Select | ❌ | On generation · 3 days before · 1 day before |

**Submit:** [Schedule Meeting] / [Save Changes].

---

### 8.2 Drawer: `meeting-detail`
- **Trigger:** Meeting title click or [View]
- **Width:** 800px
- **Tabs:** Overview · Agenda · Attendees · Documents · Minutes · Resolutions

#### Tab: Overview
- Meeting metadata: Type · Date/Time · Venue · Status · Quorum
- Status badge + [Mark In Progress] [Mark Completed] (Exec Sec / Chairman / MD)
- Pre-meeting checklist: Agenda confirmed · Board Pack sent · Quorum confirmed · AV ready

#### Tab: Agenda
- Read-only ordered list of agenda items
- Each item: number · title · presenter · duration · type
- During meeting: [Mark Done] per item (changes item to strikethrough)
- [Add AOB Item] (during/after meeting only)

#### Tab: Attendees
- Table: Name · Role · Type (Invitee/External) · Mandatory? · Attended (Yes/No/Virtual)
- **[Record Attendance]** button (Exec Sec / Chairman / MD) — bulk attendance marking
- Attendance summary: X / Y attended · Quorum: Met / Not Met

#### Tab: Documents
- All uploaded documents listed with view/download
- [+ Upload Document] (role-permissioned)
- [Download Board Pack] if generated

#### Tab: Minutes
- **If not created:** Empty state with [+ Create Minutes] button (Exec Sec / Chairman / MD)
- **If draft:** Rich text editor showing draft minutes · [Save Draft] · [Submit for Review] · [Publish Minutes]
- **If published:** Read-only view + [Download PDF] button
- Minutes structure auto-populated from agenda items (each item = one minutes section)

#### Tab: Resolutions
- Table of resolutions from this meeting
- [+ Add Resolution] (Chairman / MD only)
- Per resolution: Number · Title · Moved By · Seconded By · Vote (For/Against/Abstain) · Status
- [Approve Resolution] button (Chairman / MD) → changes status from Draft to Passed

---

### 8.3 Modal: `meeting-cancel`
- **Width:** 440px
- **Fields:** Cancellation Reason (textarea, required) · Notify Attendees (toggle, default On)
- **Buttons:** [Cancel Meeting] (danger) + [Keep Meeting]
- **On confirm:** Status → Cancelled · Attendees notified via WhatsApp + email

### 8.4 Modal: `resolution-add`
- **Width:** 480px
- **Fields:**
  | Field | Type | Required |
  |---|---|---|
  | Resolution Number | Text | ✅ | Auto-generated (RES-YYYY-NNN) — editable |
  | Title | Text | ✅ | Max 200 chars |
  | Category | Select | ✅ | Financial · Academic · HR · Expansion · Compliance · Administrative |
  | Full Text | Textarea | ✅ | Min 50 chars |
  | Moved By | Search + select | ✅ | From attendees |
  | Seconded By | Search + select | ✅ | From attendees |
  | Vote For | Number | ✅ | |
  | Vote Against | Number | ✅ | |
  | Vote Abstain | Number | ✅ | |
- **On submit:** Resolution created with status Draft → Chairman/MD clicks [Approve Resolution] to mark Passed.

### 8.5 Modal: `send-board-pack`
- **Width:** 480px
- **Shows:** List of invited attendees with email addresses
- **Fields:** Additional Recipients (comma-separated emails) · Message (textarea, optional) · Attach PDF (toggle, default On)
- **Buttons:** [Send Board Pack] + [Cancel]
- **On send:** Board pack PDF emailed + WhatsApp message to all attendees.

---

## 9. Charts

### 9.1 Meeting Frequency (last 12 months)
- **Type:** Bar chart — meetings per month
- **Stacked by type:** AGM/EGM/Board Review/Committee
- **Export:** PNG

### 9.2 Resolution Status Breakdown
- **Type:** Donut chart
- **Data:** Active · Implemented · Superseded · Revoked
- **Export:** PNG

### 9.3 Attendance Rate Trend
- **Type:** Line chart — average attendance % per meeting over last 8 meetings
- **Threshold line:** Quorum % (dashed)
- **Export:** PNG

---

## 10. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Meeting scheduled | \"Meeting [Name] scheduled for [Date]\" | Success | 4s |
| Meeting updated | \"Meeting updated\" | Success | 4s |
| Meeting cancelled | \"Meeting cancelled. Attendees notified.\" | Warning | 6s |
| Board pack sent | \"Board pack sent to [N] attendees\" | Success | 4s |
| Board pack generated | \"Board pack PDF generated — ready to send\" | Info | 4s |
| Minutes published | \"Minutes for [Meeting] published\" | Success | 4s |
| Resolution passed | \"Resolution [RES-XXXX-NNN] recorded as passed\" | Success | 4s |
| Attendance recorded | \"Attendance recorded — quorum [Met/Not Met]\" | Info | 4s |
| Document uploaded | \"[Filename] uploaded\" | Success | 4s |

---

## 11. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No upcoming meetings | "No meetings scheduled" | "Schedule the next board meeting" | [+ Schedule Meeting] |
| No past meetings | "No past meetings" | "Completed meetings will appear here" | — |
| No resolutions | "No resolutions recorded" | "Resolutions from board meetings will appear here" | — |
| No documents | "No documents" | "Upload board documents or generate a board pack" | [+ Upload] |
| No minutes | "No minutes created" | "Record the minutes after the meeting concludes" | [+ Create Minutes] |

---

## 12. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: tab headers + table (8 rows) |
| Tab switch | Inline skeleton |
| Meeting detail drawer | Spinner in drawer |
| Board pack generation | Progress bar in drawer Documents tab |
| Minutes load (rich text) | Spinner in tab area |
| Attendance save | Spinner in button |
| Document upload | Progress bar in upload area |

---

## 13. Role-Based UI Visibility

| Element | Chairman/MD | CEO | Exec Secretary | Trustee/Advisor |
|---|---|---|---|---|
| [+ Schedule Meeting] | ✅ | ✅ | ✅ | ❌ |
| [Edit] meeting | ✅ | ✅ | ✅ | ❌ |
| [Cancel] meeting | ✅ | ✅ | ✅ | ❌ |
| [Create Minutes] | ✅ | ❌ | ✅ | ❌ |
| [Publish Minutes] | ✅ | ❌ | ✅ | ❌ |
| [Approve Resolution] | ✅ | ❌ | ❌ | ❌ |
| [+ Add Resolution] | ✅ | ❌ | ❌ | ❌ |
| [Mark Implemented] | ✅ | ✅ | ✅ | ❌ |
| [Send Board Pack] | ✅ | ✅ | ✅ | ❌ |
| [Record Attendance] | ✅ | ❌ | ✅ | ❌ |
| [Upload Document] | ✅ | ✅ | ✅ | ❌ |
| [Download Documents] | ✅ | ✅ | ✅ | ✅ |
| [Export] button | ✅ | ✅ | ✅ | ❌ |
| View all tabs | ✅ | ✅ | ✅ | ✅ read |

---

## 14. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/board-meetings/` | JWT | Meetings list (paginated) |
| POST | `/api/v1/group/{id}/board-meetings/` | JWT (G3+) | Create meeting |
| GET | `/api/v1/group/{id}/board-meetings/{mid}/` | JWT | Meeting detail |
| PUT | `/api/v1/group/{id}/board-meetings/{mid}/` | JWT (G3+) | Update meeting |
| DELETE | `/api/v1/group/{id}/board-meetings/{mid}/` | JWT (G4/G5) | Cancel meeting |
| POST | `/api/v1/group/{id}/board-meetings/{mid}/send-board-pack/` | JWT (G3+) | Send board pack |
| POST | `/api/v1/group/{id}/board-meetings/{mid}/generate-board-pack/` | JWT (G3+) | Generate PDF |
| GET | `/api/v1/group/{id}/board-meetings/{mid}/attendance/` | JWT | Attendance list |
| PUT | `/api/v1/group/{id}/board-meetings/{mid}/attendance/` | JWT (G3+) | Record attendance |
| GET | `/api/v1/group/{id}/board-meetings/{mid}/minutes/` | JWT | Minutes content |
| PUT | `/api/v1/group/{id}/board-meetings/{mid}/minutes/` | JWT (G3+) | Save/publish minutes |
| GET | `/api/v1/group/{id}/board-meetings/{mid}/resolutions/` | JWT | Meeting resolutions |
| POST | `/api/v1/group/{id}/board-meetings/{mid}/resolutions/` | JWT (G5) | Add resolution |
| PUT | `/api/v1/group/{id}/board-meetings/{mid}/resolutions/{rid}/` | JWT (G5) | Approve/update resolution |
| GET | `/api/v1/group/{id}/board-meetings/resolutions/` | JWT | All resolutions register |
| GET | `/api/v1/group/{id}/board-meetings/documents/` | JWT | Document library |
| POST | `/api/v1/group/{id}/board-meetings/{mid}/documents/` | JWT (G3+) | Upload document |
| DELETE | `/api/v1/group/{id}/board-meetings/{mid}/documents/{did}/` | JWT (G3+) | Delete document |

---

## 15. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../board-meetings/?q=` | `#meetings-table-body` | `innerHTML` |
| Tab switch | `click` | GET `.../board-meetings/?tab=` | `#tab-content` | `innerHTML` |
| Filter apply | `click` | GET `.../board-meetings/?filters=` | `#meetings-table-section` | `innerHTML` |
| Open meeting detail | `click` | GET `.../board-meetings/{id}/` | `#drawer-body` | `innerHTML` |
| Record attendance | `click` | PUT `.../attendance/` | `#attendance-section` | `innerHTML` |
| Mark minutes published | `click` | PUT `.../minutes/` | `#minutes-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
