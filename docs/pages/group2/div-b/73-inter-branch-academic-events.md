# 73 — Inter-Branch Academic Events Manager

> **URL:** `/group/acad/inter-branch-events/`
> **File:** `73-inter-branch-academic-events.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Academic Director G3 (full) · Olympiad Coordinator G3 (full) · CAO G4 (view + approve)

---

## 1. Purpose

Central management of group-owned inter-branch academic competitions: Quiz Bowls, Science Fairs,
Debate Competitions, Maths Olympiads (internal), Spelling Bees, GK Championships, and Essay contests.

These events build academic culture, motivate students beyond exams, and provide marketing material
for the group. Without this page, events are organised via WhatsApp groups — no registration tracking,
no structured results, and no group-level recognition of winners.

---

## 2. Role Access

| Role | Level | Can Create | Can Manage | Can View | Notes |
|---|---|---|---|---|---|
| Academic Director | G3 | ✅ | ✅ | ✅ | |
| Olympiad Coordinator | G3 | ✅ | ✅ | ✅ | Especially external olympiad parallels |
| CAO | G4 | ❌ | ❌ | ✅ + Approve | |
| Stream Coordinators | G3 | ❌ | ❌ | ✅ | Can see stream-relevant events |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Inter-Branch Academic Events
```

### 3.2 Page Header
```
Inter-Branch Academic Events Manager                  [+ New Event]  [Export Report ↓]
AY 2025–26 · [N] Events · [M] Upcoming
```

### 3.3 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Events (AY) | 12 |
| Upcoming | 4 |
| In Progress | 1 |
| Completed | 7 |
| Branches Participated | 45 / 50 |
| Students Participated | 3,280 |
| Certificates Issued | 2,940 |

---

## 4. Main Table

### 4.1 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Event Name | Text + link | ✅ | |
| Type | Badge | ✅ | Quiz · Science Fair · Debate · Maths · Spelling · GK · Essay · Other |
| Date | Date | ✅ | Event day |
| Venue / Format | Badge | ✅ | In-Person · Virtual · Hybrid |
| Branches Invited | Number | ✅ | |
| Branches Registered | Number | ✅ | |
| Students Registered | Number | ✅ | |
| Class Eligibility | Text | ✅ | e.g. "Class 9–12" |
| Status | Badge | ✅ | Draft · Open · Registration Closed · In Progress · Completed |
| Winner Branch | Text | ✅ | After completion |
| Actions | — | ❌ | View · Edit · Results |

### 4.2 Filters

| Filter | Type | Options |
|---|---|---|
| Event Type | Multi-select | Quiz · Debate · Science Fair · Maths · Spelling · GK · Essay · Other |
| Status | Multi-select | Draft · Open · Closed · In Progress · Completed |
| Format | Multi-select | In-Person · Virtual · Hybrid |
| Stream | Multi-select | MPC / BiPC / MEC / HEC / All streams |
| Date range | Date range | Event date range |

---

## 5. Drawers

### 5.1 Drawer: `event-create` — New Event
- **Trigger:** [+ New Event] header button
- **Width:** 640px

| Field | Type | Required | Validation |
|---|---|---|---|
| Event Name | Text | ✅ | Min 5 chars |
| Event Type | Select | ✅ | |
| Date & Time | DateTime | ✅ | Must be future |
| Venue | Text | ✅ | Address or "Virtual" |
| Format | Select | ✅ | In-Person · Virtual · Hybrid |
| Branch Scope | Multi-select | ✅ | All branches or select |
| Class Eligibility | Multi-select | ✅ | Class 6 – 12 |
| Stream Eligibility | Multi-select | ❌ | All or specific stream |
| Max Students per Branch | Number | ❌ | |
| Registration Deadline | Date | ✅ | Before event date |
| Judging Criteria | Rich text | ✅ | For judges and students |
| Prize | Text | ❌ | e.g. "Trophy + ₹5,000" |
| Contact Coordinator | Search select | ✅ | Event contact person |

### 5.2 Drawer: `event-detail` — Event Detail
- **Trigger:** View row action
- **Width:** 680px

**Tab: Overview**
- All event fields (read-only) · Registration deadline status · Branch participation rate

**Tab: Registrations**

| Column | Type |
|---|---|
| Branch | Text |
| Team / Students | Text (team name or student list) |
| Registered Date | Date |
| Status | Badge (Confirmed / Waitlisted / Withdrawn) |

- **[Approve Registration]** (if manual approval required)
- **[Send Reminder]** → notify non-registered branches

**Tab: Schedule**
- Round-wise schedule (for multi-round events like Quiz or Debate)
- Venue/link per round

**Tab: Results**

| Column | Type |
|---|---|
| Rank | Number |
| Branch | Text |
| Team / Student | Text |
| Score / Points | Number |
| Notes | Text |

- **[Enter Results]** → opens results entry form
- **[Generate Certificates]** → bulk PDF

**Tab: Gallery**
- Photo/video upload links
- Public sharing toggle (visible on group website if enabled)

---

## 6. Certificate Generation

- **Trigger:** [Generate Certificates] in Results tab
- **Types:** Winner · Runner-Up · Participation
- **Content:** Student/Team name · Event · Date · Rank · Group signature block · Group logo
- **Format:** Bulk PDF · One ZIP download
- **Watermark:** Group name + date

---

## 7. Charts

### 7.1 Events per Term (Bar)
- **Data:** Number of events per academic term
- **Color by type:** Quiz (blue) · Science Fair (green) · Debate (orange) · Other (grey)
- **Export:** PNG

### 7.2 Branch Participation Rate (Heatmap)
- **Rows:** Branches
- **Columns:** Events
- **Cell:** Participated (green) / Not Participated (red)
- **Export:** PNG

### 7.3 Winning Branch History (Bar)
- **Data:** Number of times each branch has won events this AY
- **Export:** PNG

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "Event '[Name]' created. Invitations sent to [N] branches." | Success | 4s |
| Registration confirmed | "Branch [Name] registration confirmed." | Success | 3s |
| Results entered | "Results recorded. [Branch] wins '[Event]'." | Success | 4s |
| Certificates generated | "Certificates generated. Download link ready." | Success | 4s |
| Reminder sent | "Registration reminder sent to [N] branches." | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No events | "No inter-branch events yet" | "Create the first group-level academic event." | [+ New Event] |
| No registrations | "No registrations yet" | "Registration link was sent. Waiting for branches." | [Resend Invitation] |
| No results | "Results not entered" | "Enter results after the event is complete." | [Enter Results] |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Page load | Skeleton: stats bar + 5 event cards |
| Filter/search | Inline skeleton |
| Detail drawer | Spinner + skeleton tabs |
| Certificate generation | Full-page overlay "Generating certificates…" |

---

## 11. Role-Based UI Visibility

| Element | Academic Dir G3 | Olympiad Coord G3 | CAO G4 |
|---|---|---|---|
| [+ New Event] | ✅ | ✅ | ❌ |
| [Approve Registration] | ✅ | ✅ | ❌ |
| [Enter Results] | ✅ | ✅ | ❌ |
| [Generate Certificates] | ✅ | ✅ | ❌ |
| [CAO Approve Event] | ❌ | ❌ | ✅ |
| View all events | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/inter-branch-events/` | JWT (G3+) | Event list |
| POST | `/api/v1/group/{id}/acad/inter-branch-events/` | JWT (G3) | Create event |
| GET | `/api/v1/group/{id}/acad/inter-branch-events/{eid}/` | JWT (G3+) | Event detail |
| PUT | `/api/v1/group/{id}/acad/inter-branch-events/{eid}/` | JWT (G3) | Update event |
| GET | `/api/v1/group/{id}/acad/inter-branch-events/{eid}/registrations/` | JWT (G3+) | Registrations list |
| POST | `/api/v1/group/{id}/acad/inter-branch-events/{eid}/results/` | JWT (G3) | Enter results |
| POST | `/api/v1/group/{id}/acad/inter-branch-events/{eid}/certificates/` | JWT (G3) | Generate certificates |
| POST | `/api/v1/group/{id}/acad/inter-branch-events/{eid}/send-reminder/` | JWT (G3) | Send branch reminder |
| GET | `/api/v1/group/{id}/acad/inter-branch-events/stats/` | JWT (G3+) | Summary stats |
| GET | `/api/v1/group/{id}/acad/inter-branch-events/export/?format=csv` | JWT (G3+) | Export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search | `input delay:300ms` | GET `.../inter-branch-events/?q=` | `#events-table-body` | `innerHTML` |
| Filter | `click` | GET `.../inter-branch-events/?filters=` | `#events-section` | `innerHTML` |
| Open detail | `click` | GET `.../inter-branch-events/{id}/` | `#drawer-body` | `innerHTML` |
| Create submit | `submit` | POST `.../inter-branch-events/` | `#drawer-body` | `innerHTML` |
| Enter results | `submit` | POST `.../results/` | `#results-tab-body` | `innerHTML` |
| Generate certificates | `click` | POST `.../certificates/` | `#cert-btn` | `outerHTML` |
| Send reminder | `click` | POST `.../send-reminder/` | `#reminder-btn` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
