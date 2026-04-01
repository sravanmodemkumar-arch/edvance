# 42 — Olympiad Exam Registry

> **URL:** `/group/acad/olympiad/exams/`
> **File:** `42-olympiad-exam-registry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Olympiad & Scholarship Coordinator G3 · CAO G4

---

## 1. Purpose

The Olympiad Exam Registry is the master list of all external competitive and olympiad examinations that the institution group participates in, across all branches and all eligible classes. It covers national-level olympiads — NTSE (National Talent Search Examination), NMMS (National Means-cum-Merit Scholarship), NSO (National Science Olympiad), IMO (International Mathematics Olympiad), KVPY (now INSPIRE, but commonly tracked as KVPY) — as well as state-level competitive exams and JEE/NEET screening tests that the group registers students for.

The registry is the source of truth from which all downstream olympiad workflows draw data: the Registration Manager (page 43) looks at this registry to know which exams exist; the Results & Awards page (page 44) looks at this registry to know which exams have results expected; and the scholarship pipeline references this registry for exam eligibility criteria.

The most operationally critical feature is the reminder automation system. Olympiad registration deadlines are notoriously easy to miss — especially in a group managing 50 branches with different teachers responsible for coordination. This page allows the Olympiad Coordinator to set automatic reminders N days before each registration deadline, which trigger notifications to branch coordinators and the Olympiad Coordinator themselves. A missed registration deadline cannot be undone — a student who is eligible for NTSE but not registered because the deadline was missed has lost a year's opportunity. The reminder automation is designed to prevent this.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All records | ✅ View · Export | Read with export |
| Group Academic Director | G3 | ✅ All records | ❌ | Read-only |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Group Stream Coord — MPC | G3 | ✅ JEE/Maths olympiads (IMO, KVPY) | ❌ | Read-only, filtered |
| Group Stream Coord — BiPC | G3 | ✅ Science/NEET olympiads (NSO, KVPY) | ❌ | Read-only, filtered |
| Group Stream Coord — MEC/CEC | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ✅ JEE/NEET-adjacent exams | ❌ | Read-only |
| Group IIT Foundation Director | G3 | ✅ Foundation-eligible exams (NTSE/NMMS/NSO/IMO) | ❌ | Read-only |
| Group Olympiad & Scholarship Coord | G3 | ✅ All records | ✅ Full — create · edit · delete · set reminders | Primary operator |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ All records | ✅ Export only | Read-only |
| Group Academic Calendar Manager | G3 | ✅ All records | ❌ | Read-only — for academic calendar coordination |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Olympiad & Scholarships  ›  Exam Registry
```

### 3.2 Page Header
```
Olympiad Exam Registry                              [+ Add Exam]  [Export XLSX ↓]
[Group Name] · Academic Year [YYYY–YY]              Olympiad Coordinator only — add button
```

### 3.3 Upcoming Deadline Alert Banner

Shown at top when any exam has a registration deadline within the next 30 days:

**Alert format (collapsible, amber):**
> "Registration deadlines approaching:"
> - NTSE State Level — Registration closes in **7 days** (DD MMM YYYY) — [View →]
> - NSO Level 1 — Registration closes in **14 days** (DD MMM YYYY) — [View →]

Dismiss per-alert (stored in session, reappears next login if still within 30 days). "View all upcoming deadlines →" link to the filtered table (Status = Active, deadline within 30 days).

### 3.4 Summary Stats Bar

| Stat | Value |
|---|---|
| Total Exams in Registry | 18 |
| Active (Registration Open or Not Yet Open) | 8 |
| Registration Closed | 4 |
| Exam Ongoing | 1 |
| Results Out | 3 |
| Exams with Reminder Set | 12 |
| Exams Without Reminder | 6 |

---

## 4. Main Content

### 4.1 Search / Filters / Table

**Search:** Exam name or body name — 300ms debounce, highlights match in Exam Name column.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Conducting Body | Multi-select | NCERT/CBSE · Ministry of Education · Science Olympiad Foundation (SOF) · HBCSE · State SCERT · Private Body |
| Eligible Classes | Multi-select | Class 6 · 7 · 8 · 9 · 10 · 11 · 12 |
| Eligible Streams | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · All |
| Exam Status | Multi-select | Upcoming (Registration Not Open) · Registration Open · Registration Closed · Exam Date Passed · Results Out · Closed |
| Academic Year | Select | Current year · Previous year |
| Reminder Set | Checkbox | Show only exams with reminders configured |
| No Reminder | Checkbox | Show only exams without reminders configured |

Active filter chips: Dismissible, "Clear All" link, count badge.

### 4.2 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Row select for bulk actions |
| Exam Name | Text + link | ✅ | Opens exam detail drawer |
| Conducting Body | Text | ✅ | NCERT / SOF / HBCSE / State SCERT / etc. |
| Eligible Classes | Tags | ❌ | e.g. "Class 8, 9, 10" |
| Eligible Streams | Tags | ❌ | e.g. "All" or specific streams |
| Registration Opens | Date | ✅ | Date registration window opens |
| Registration Deadline | Date | ✅ | **Key column** — coloured: Red if within 7 days · Amber if 8–14 days · Blue if 15–30 days · Grey if closed |
| Exam Date | Date | ✅ | Scheduled exam date |
| Fee per Student | Currency | ✅ | e.g. ₹125 per student |
| Expected Result Date | Date | ✅ | Approximate result announcement date |
| Status | Badge | ✅ | Colour-coded by exam status |
| Reminder | Badge | ❌ | Set (N days) · Not Set (amber warning) |
| Official Site | Icon | ❌ | External link icon — opens official exam site |
| Actions | — | ❌ | See row actions |

**Registration Deadline column highlight rules:**
- Within 7 days: Red badge + red cell background `bg-red-50`
- 8–14 days: Amber badge + amber cell `bg-amber-50`
- 15–30 days: Blue badge — gentle reminder
- Past deadline: Strikethrough + grey text "Closed DD MMM YYYY"

**Default sort:** Registration Deadline ascending (soonest deadline first), Status Active first.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50.

### 4.3 Row Actions

| Action | Icon | Visible To | Opens | Notes |
|---|---|---|---|---|
| View Detail | Eye | All with access | `olympiad-detail` drawer 560px | Full exam information |
| Edit | Pencil | Olympiad Coord · CAO | `olympiad-edit` drawer 560px | Update dates, fee, details |
| Set Reminder | Bell | Olympiad Coord | `reminder-config` drawer 420px | Configure automated notifications |
| Edit Reminder | Bell-edit | Olympiad Coord | `reminder-config` drawer 420px | Shown if reminder already set |
| View Official Site | External | All | Opens official exam URL in new tab | |
| Archive | Archive | Olympiad Coord · CAO | Confirm modal 380px | Archives past exams — keeps history |
| Delete | Trash | Olympiad Coord · CAO | Confirm modal 380px | Hard delete — only for duplicates/errors |

### 4.4 Bulk Actions (shown when rows selected)

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | Olympiad Coord · CAO · MIS | |
| Set Reminder for Selected | Olympiad Coord | Opens bulk reminder config modal |
| Archive Selected | Olympiad Coord · CAO | Batch archive past exams |

---

## 5. Drawers & Modals

### 5.1 Drawer: `olympiad-add` / `olympiad-edit`
- **Trigger:** [+ Add Exam] header button / Pencil icon row action
- **Width:** 560px (create) · 560px (edit)
- **Title:** "Add Olympiad Exam" / "Edit — [Exam Name]"

| Field | Type | Required | Validation / Notes |
|---|---|---|---|
| Exam Name | Text | ✅ | Max 150 chars · Must be unique within academic year |
| Short Code | Text | ✅ | Max 10 chars · e.g. NTSE, NSO-L1, IMO — auto-suggested |
| Conducting Body | Text | ✅ | Free text — NCERT / SOF / HBCSE / State SCERT |
| Exam Type | Select | ✅ | National Olympiad · State Olympiad · Central Scholarship · Competitive |
| Eligible Classes | Multi-select | ✅ | Class 6 through Class 12 — at least one required |
| Eligible Streams | Multi-select | ✅ | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · All Streams |
| Academic Year | Select | ✅ | Current or upcoming academic year |
| Registration Opens | Date | ❌ | If blank, treated as "TBD" |
| Registration Deadline | Date | ✅ | Must be a future date at creation time |
| Exam Date | Date | ✅ | Must be after registration deadline |
| Exam Duration | Text | ❌ | e.g. "2 hours" |
| Expected Result Date | Date | ❌ | Approximate — shown as "Expected: [date]" |
| Fee per Student | Number | ❌ | In ₹ — 0 if free exam |
| Fee Payment Mode | Select | ❌ | Online · DD · Cheque · Free |
| Official Site URL | URL | ❌ | Must be valid URL if provided |
| Notes / Instructions | Textarea | ❌ | Internal notes for coordinators |
| Syllabus Reference | Textarea | ❌ | Key topics for exam preparation |

**Reminder configuration prompt (shown in drawer after mandatory fields filled):**
> "Would you like to set deadline reminders for this exam?"
> [Set Reminders →] — expands inline reminder config section (same as reminder-config drawer fields)

**Submit:** [Add Exam] / [Save Changes] — disabled until required fields valid.

**On success:** Exam appears in registry · Reminder (if set) is scheduled · Toast shown.

---

### 5.2 Drawer: `olympiad-detail`
- **Trigger:** Eye icon or exam name click
- **Width:** 560px
- **Tabs:** Overview · Eligibility · Reminders · Registration Status · History

#### Tab: Overview
Full exam details: Name · Body · Type · Academic Year · Dates (Registration open · Deadline · Exam · Results) · Fee · Official site link · Notes.

Status timeline (visual):
```
[Exam Added] → [Registration Opens] → [Registration Closes] → [Exam Date] → [Results] → [Awards]
      ✅                ✅                    🔴 IN 7 DAYS            ○               ○          ○
```

#### Tab: Eligibility
- Eligible Classes: List with checkmarks
- Eligible Streams: List
- Approximate eligible students: Auto-calculated from enrollment data — "Approx. [N] students across [M] branches are eligible"

#### Tab: Reminders
Shows all configured reminders for this exam:

| Reminder | Days Before Deadline | Recipients | Channel | Status |
|---|---|---|---|---|
| Primary Reminder | 30 days | Olympiad Coord + All branch principals | WhatsApp + Email | Scheduled |
| Final Reminder | 7 days | Olympiad Coord + All branch principals | WhatsApp + Email | Scheduled |
| Last Chance | 2 days | Olympiad Coord only | Email | Scheduled |

[Edit Reminders] button — opens `reminder-config` drawer.
[Test Reminder] button (Olympiad Coord only) — sends a test notification to self immediately.

#### Tab: Registration Status
- Quick link: "[View in Registration Manager →]" → page 43 filtered to this exam
- Summary: Branches registered: N / Total eligible · Students registered: N · Registration rate: X%
- Status: Registration not started / In progress / Submitted

#### Tab: History
Audit table: Action · Timestamp · Actor — for all edits, reminder changes, archive/restore events.

---

### 5.3 Drawer: `reminder-config`
- **Trigger:** "Set Reminder" / "Edit Reminder" row action
- **Width:** 420px
- **Title:** "Reminder Configuration — [Exam Name]"

**Reminder slots:** Up to 4 reminder triggers per exam.

For each reminder slot:
| Field | Type | Required | Notes |
|---|---|---|---|
| Reminder Label | Text | ✅ | e.g. "Primary Reminder" / "Final Notice" / "Last Chance" |
| Days Before Registration Deadline | Number | ✅ | e.g. 30 · 14 · 7 · 2 |
| Recipients — Group Level | Multi-checkbox | ✅ | Olympiad Coordinator · CAO · Academic Director |
| Recipients — Branch Level | Multi-checkbox | ✅ | All Branch Principals · Branch Olympiad Coordinators · All Branch Teachers |
| Channels | Multi-checkbox | ✅ | WhatsApp · Email · Portal Notification |
| Message Preview | Read-only text | Auto | Auto-generated from template: "Registration for [Exam Name] closes in [N] days ([Date]). [Total eligible students] students across [N] branches are eligible. Register before the deadline." |
| Custom Message Override | Textarea | ❌ | Replaces auto-generated message if filled |

**[+ Add Another Reminder]** — adds another slot (max 4).

**[Remove]** link per slot.

**Active status:** Each configured reminder shows its trigger date when saved — e.g. "Will send on: DD MMM YYYY (30 days before deadline)."

**Submit:** [Save Reminder Configuration] — saves all slots.

**On save:** Reminder jobs scheduled in background task queue · Confirmation shows all scheduled dates.

---

### 5.4 Modal: `archive-confirm`
- **Width:** 380px
- **Title:** "Archive [Exam Name]"
- **Content:** "Archiving moves this exam to the historical record. It will no longer appear in the active registry but remains accessible in the archive. Scheduled reminders will be cancelled."
- **Buttons:** [Archive Exam] (primary) + [Cancel]

---

### 5.5 Modal: `delete-confirm`
- **Width:** 380px
- **Title:** "Delete [Exam Name]"
- **Warning:** "This permanently removes the exam from the registry. Use Archive instead if this exam has historical value. If students have been registered for this exam, their registration data will be preserved separately."
- **Buttons:** [Delete Exam] (danger red) + [Cancel]
- Only shown to Olympiad Coord and CAO.

---

### 5.6 Modal: `bulk-reminder-config`
- **Width:** 480px
- **Title:** "Set Reminders — [N] Exams"
- **Content:** Applies one standard reminder template to all selected exams.
- **Template:** 30-day + 7-day + 2-day reminders · All branch principals + Olympiad Coord · WhatsApp + Email
- **Customisation:** Option to change days before deadline only (channels and recipients fixed in bulk mode)
- **Overwrite warning:** "This will overwrite existing reminders for [N] of the selected exams."
- **Buttons:** [Apply Reminder Template to [N] Exams] + [Cancel]

---

## 6. Charts

### 6.1 Exam Calendar Timeline (Gantt-style)
- **Type:** Horizontal Gantt bar chart (Timeline)
- **Y-axis:** Exam names (one row per exam)
- **X-axis:** Academic year months (Apr–Mar)
- **Bars:** Registration window (blue bar) + Gap (grey) + Exam date (star/point marker) + Result date (diamond marker)
- **Colour-coding by status:** Active (blue) · Closed (grey) · Ongoing (orange) · Results Out (green)
- **Tooltip:** Exam name · Registration: from–to · Exam date · Result expected
- **Export:** PNG
- **Shown:** In "Exam Calendar" collapsible card above the main table — gives a full-year visual calendar of all olympiad events

### 6.2 Fee per Student by Exam (Bar)
- **Type:** Horizontal bar chart
- **X-axis:** Fee in ₹
- **Y-axis:** Exam names
- **Colour:** Green for free exams · Blue for paid
- **Tooltip:** Exam name · Fee per student · Total eligible students · Estimated total fee (Fee × Eligible students)
- **Export:** PNG
- **Shown:** In "Fee Overview" collapsible card — helps the group plan and budget for olympiad participation

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exam added | "[Exam Name] added to the registry." | Success | 4s |
| Exam edited | "[Exam Name] updated." | Success | 4s |
| Reminder saved | "Reminders configured for [Exam Name]. Scheduled: [dates list]." | Success | 5s |
| Reminder test sent | "Test reminder sent to your registered contact." | Info | 4s |
| Bulk reminder applied | "Reminder template applied to [N] exams." | Success | 5s |
| Exam archived | "[Exam Name] archived. Scheduled reminders cancelled." | Info | 4s |
| Exam deleted | "[Exam Name] permanently deleted." | Warning | 5s |
| Export started | "XLSX export preparing — download will begin shortly." | Info | 4s |
| URL invalid | "The official site URL is not valid. Please check and re-enter." | Error | Manual |
| Duplicate exam detected | "An exam with the name [Exam Name] already exists for this academic year." | Error | Manual |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No exams in registry | "No Olympiad Exams Added" | "Add the olympiad and competitive exams your group participates in to start tracking registrations and results" | [+ Add Exam] |
| No exams match filters | "No Exams Match" | "Try different filters or clear them to see all registry entries" | [Clear Filters] |
| No upcoming deadlines | "No Upcoming Deadlines" | "No registration deadlines are within the next 30 days" | — |
| No exams with reminders | "No Reminders Set" | "Set deadline reminders to ensure branches register students on time" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: alert banner placeholder + stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| Add/edit exam drawer open | Spinner in drawer body |
| Exam detail drawer open | Spinner + skeleton tabs |
| Reminder config drawer open | Spinner in drawer body |
| Timeline Gantt chart load | Spinner centred in chart card + "Loading calendar…" |
| Archive / delete confirm actions | Spinner in confirm button + button disabled |
| Export trigger | Spinner in export button (momentary) |
| Bulk reminder apply | Spinner inside [Apply Reminder Template] + button disabled |

---

## 10. Role-Based UI Visibility

| Element | Olympiad Coord G3 | CAO G4 | Academic Dir G3 | Stream Coords G3 | MIS G1 |
|---|---|---|---|---|---|
| [+ Add Exam] button | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit Exam action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Set / Edit Reminder | ✅ | ❌ | ❌ | ❌ | ❌ |
| Test Reminder button (in drawer) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Archive action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Delete action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Bulk Set Reminder | ✅ | ❌ | ❌ | ❌ | ❌ |
| Bulk Archive | ✅ | ✅ | ❌ | ❌ | ❌ |
| Fee column | ✅ | ✅ | ✅ | ❌ | ✅ |
| Official Site link | ✅ | ✅ | ✅ | ✅ | ✅ |
| Reminders tab in detail drawer | ✅ | ✅ | ❌ | ❌ | ❌ |
| Registration Status tab in detail drawer | ✅ | ✅ | ✅ | ✅ | ✅ |
| Export XLSX | ✅ | ✅ | ❌ | ❌ | ✅ |
| Timeline Gantt chart | ✅ | ✅ | ✅ | ✅ (own stream exams) | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/olympiad/exams/` | JWT | Exam registry list (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/olympiad/exams/stats/` | JWT | Summary stats bar |
| GET | `/api/v1/group/{group_id}/acad/olympiad/exams/upcoming-deadlines/` | JWT | Alert banner data — exams with deadline ≤ 30 days |
| POST | `/api/v1/group/{group_id}/acad/olympiad/exams/` | JWT (Olympiad Coord) | Create exam |
| GET | `/api/v1/group/{group_id}/acad/olympiad/exams/{exam_id}/` | JWT | Exam detail drawer data |
| PUT | `/api/v1/group/{group_id}/acad/olympiad/exams/{exam_id}/` | JWT (Olympiad Coord / CAO) | Update exam |
| DELETE | `/api/v1/group/{group_id}/acad/olympiad/exams/{exam_id}/` | JWT (Olympiad Coord / CAO) | Hard delete exam |
| POST | `/api/v1/group/{group_id}/acad/olympiad/exams/{exam_id}/archive/` | JWT (Olympiad Coord / CAO) | Archive exam |
| GET | `/api/v1/group/{group_id}/acad/olympiad/exams/{exam_id}/reminders/` | JWT (Olympiad Coord / CAO) | Get reminder config for exam |
| POST | `/api/v1/group/{group_id}/acad/olympiad/exams/{exam_id}/reminders/` | JWT (Olympiad Coord) | Save reminder configuration |
| POST | `/api/v1/group/{group_id}/acad/olympiad/exams/{exam_id}/reminders/test/` | JWT (Olympiad Coord) | Send test reminder to self |
| POST | `/api/v1/group/{group_id}/acad/olympiad/exams/bulk-reminders/` | JWT (Olympiad Coord) | Bulk apply reminder template |
| POST | `/api/v1/group/{group_id}/acad/olympiad/exams/bulk-archive/` | JWT (Olympiad Coord / CAO) | Bulk archive |
| GET | `/api/v1/group/{group_id}/acad/olympiad/exams/export/?format=xlsx` | JWT | Export registry XLSX |
| GET | `/api/v1/group/{group_id}/acad/olympiad/exams/charts/timeline/` | JWT | Gantt timeline chart data |
| GET | `/api/v1/group/{group_id}/acad/olympiad/exams/charts/fee/` | JWT | Fee per exam bar chart data |
| GET | `/api/v1/group/{group_id}/acad/olympiad/exams/{exam_id}/eligibility-count/` | JWT | Eligible student count for exam |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Exam search | `input delay:300ms` | GET `.../olympiad/exams/?q=` | `#olympiad-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../olympiad/exams/?filters=` | `#olympiad-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../olympiad/exams/?sort=&dir=` | `#olympiad-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../olympiad/exams/?page=` | `#olympiad-table-section` | `innerHTML` |
| Add/edit drawer open | `click` | GET `.../olympiad/exams/create-form/` or `.../exams/{id}/edit-form/` | `#drawer-body` | `innerHTML` |
| Exam detail drawer open | `click` | GET `.../olympiad/exams/{id}/` | `#drawer-body` | `innerHTML` |
| Detail drawer tab switch | `click` | GET `.../olympiad/exams/{id}/?tab=reminders` etc. | `#olympiad-detail-tab-content` | `innerHTML` |
| Reminder config drawer open | `click` | GET `.../olympiad/exams/{id}/reminders/` | `#drawer-body` | `innerHTML` |
| Save reminder | `click` | POST `.../olympiad/exams/{id}/reminders/` | `#drawer-body` | `innerHTML` |
| Test reminder | `click` | POST `.../olympiad/exams/{id}/reminders/test/` | `#reminder-test-result` | `innerHTML` |
| Archive confirm | `click` | POST `.../olympiad/exams/{id}/archive/` | `#olympiad-row-{id}` | `outerHTML` |
| Alert banner dismiss | `click` | POST `.../upcoming-deadlines/{id}/dismiss/` | `#deadline-alert-{id}` | `outerHTML` |
| Timeline chart load | `load` | GET `.../olympiad/exams/charts/timeline/` | `#timeline-chart-container` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
