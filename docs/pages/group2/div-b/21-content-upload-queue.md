# 21 — Content Upload Queue

> **URL:** `/group/acad/content-uploads/`
> **File:** `21-content-upload-queue.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Academic Director G3 · Curriculum Coordinator G2 · Stream Coords G3 · Academic MIS Officer G1

---

## 1. Purpose

The Content Upload Queue is the moderation gateway between branch-submitted or coordinator-uploaded content and the Shared Content Library. Every resource submitted for group-wide distribution — whether uploaded by a branch teacher through the branch portal, a Stream Coordinator, the Curriculum Coordinator, or the Division L Library Head — lands here before it goes live. Nothing reaches the Content Library without passing through this queue.

This page is the primary working view for reviewers. It shows every submission in its current state: Pending (awaiting assignment), In Review (a reviewer is actively working on it), Approved (live in library), or Rejected (returned to uploader). Reviewers can preview content directly in this page, check metadata accuracy, add feedback notes, and make approval decisions — all without leaving the queue.

For a group generating 50–200 new content submissions per month across 50 branches, the queue needs strong filtering so reviewers can focus on their assigned stream or the oldest pending items first. Bulk approval is available when a batch of items from the same source passes a quick spot-check, preventing bottlenecks from accumulating before examination periods.

---

## 2. Role Access

| Role | Level | Can View | Can Assign Reviewer | Can Approve | Can Reject | Notes |
|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | ✅ | Full authority — override any decision |
| Group Academic Director | G3 | ✅ All | ✅ | ✅ | ✅ | Approve/reject all content |
| Group Curriculum Coordinator | G2 | ✅ All | ✅ (assign to others) | ✅ (own stream scope) | ✅ (own stream) | Review + approve; cannot override CAO/Dir decisions |
| Group Exam Controller | G3 | ❌ | ❌ | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | ❌ | ❌ | No access |
| Stream Coord — MPC | G3 | ✅ MPC only | ❌ | ❌ | ❌ | View queue for own stream; cannot approve |
| Stream Coord — BiPC | G3 | ✅ BiPC only | ❌ | ❌ | ❌ | View queue for own stream; cannot approve |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC only | ❌ | ❌ | ❌ | View queue for own stream; cannot approve |
| JEE/NEET Integration Head | G3 | ✅ MPC+BiPC queue | ❌ | ❌ | ❌ | View relevant stream queue |
| IIT Foundation Director | G3 | ✅ Foundation only | ❌ | ❌ | ❌ | View Foundation queue |
| Olympiad & Scholarship Coord | G3 | ✅ Own uploads only | ❌ | ❌ | ❌ | Track own submissions |
| Special Education Coordinator | G3 | ✅ Own uploads only | ❌ | ❌ | ❌ | Track own submissions |
| Academic MIS Officer | G1 | ✅ All (read) | ❌ | ❌ | ❌ | Read-only — reporting |
| Academic Calendar Manager | G3 | ❌ | ❌ | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Content Upload Queue
```

### 3.2 Page Header (with action buttons — role-gated)
```
Content Upload Queue                      [Approve All Passing]  [Export XLSX ↓]
[Group Name] · Review and moderate uploaded content       (CAO / Academic Dir only for bulk approve)
```

Action button visibility:
- `[Approve All Passing]` — CAO, Academic Dir (bulk approve all items with no statistical issues)
- `[Export XLSX ↓]` — All roles with view access

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Pending | Count awaiting review |
| In Review | Count actively being reviewed |
| Approved Today | Count |
| Rejected Today | Count |
| Avg Review Time | Hours from submission to decision |
| Oldest Pending | Age of oldest unreviewed item (days) |

Stats bar refreshes on page load. "Oldest Pending" turns red if > 5 days.

---

## 4. Main Queue Table

### 4.1 Search
- Full-text across: Title, Subject, Branch Name, Submitted By name
- 300ms debounce · Highlights match in Title column
- Scope: All non-archived queue items by default

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Status | Multi-select | Pending · In Review · Approved · Rejected |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated JEE · Integrated NEET |
| Subject | Multi-select | Populated based on Stream selection |
| Branch | Multi-select | All branches in group |
| Content Type | Multi-select | PDF · Video · MCQ Set · Revision Sheet · Model Answer · Reference Doc |
| Date Submitted | Date range | From / To date picker |
| Assigned Reviewer | Search input | Filter by reviewer name |
| Unassigned Only | Checkbox | Show only items with no reviewer assigned |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| ☐ | Checkbox | — | CAO, Academic Dir, Curriculum Coord | Row select for bulk actions |
| Title | Text + link | ✅ | All | Opens content-review drawer |
| Type | Badge | ✅ | All | PDF · Video · MCQ Set etc. |
| Subject | Text | ✅ | All | Subject name |
| Branch | Text | ✅ | All | Submitting branch name |
| Submitted By | Text | ✅ | All | Name + role of uploader |
| Submitted At | Date+time | ✅ | All | Submission timestamp |
| Assigned Reviewer | Text | ✅ | CAO, Academic Dir, Curriculum Coord | Reviewer name or "Unassigned" |
| Status | Badge | ✅ | All | Pending (grey) · In Review (blue) · Approved (green) · Rejected (red) |
| Age | Duration | ✅ | All | Days since submission. Red if > 5 days |
| Actions | — | ❌ | Role-based | See Row Actions |

**Column visibility toggle:** Gear icon top-right — saves preference per user.

**Default sort:** Status (Pending first), then Submitted At ascending (oldest first).

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z items" · Page jump input.

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| Preview | Eye | All | `content-review` drawer 560px | Opens preview + metadata + decision tabs |
| Assign Reviewer | Person + plus | CAO, Academic Dir, Curriculum Coord | Inline popover — select reviewer from list | Sets reviewer + changes status to In Review |
| Approve | Checkmark | CAO, Academic Dir, Curriculum Coord | Inline confirm toast | Publishes to Content Library |
| Reject | X | CAO, Academic Dir, Curriculum Coord | `reject-reason` drawer 480px | Reason required; notifies uploader |
| Request Changes | Refresh | CAO, Academic Dir, Curriculum Coord | Inline feedback input | Returns for revision without rejecting |

### 4.5 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Approve Selected | CAO, Academic Dir | Batch approve — all selected items published |
| Assign All Pending to Reviewer | CAO, Academic Dir, Curriculum Coord | Assign all unassigned pending items to a selected reviewer |
| Export Selected (XLSX) | All with view access | Queue metadata export |

---

## 5. Drawers & Modals

### 5.1 Drawer: `content-review` — Review Content
- **Trigger:** Preview row action or Title column link
- **Width:** 560px
- **Tabs:** Preview · Metadata · Reviewer Notes · Decision

#### Tab: Preview
Full embedded preview:
- PDF: Embedded PDF viewer (all pages scrollable)
- Video: YouTube embed player
- MCQ Set: Rendered question list
- Revision Sheet: Embedded PDF viewer

Download button at bottom for local review.

#### Tab: Metadata
Read-only display: Title, Content Type, Subject, Topic, Stream, Class, Board, Tags, Language, Uploaded By, Branch, Submission date, File size (or URL), Description. [Edit Metadata] button (CAO/Academic Dir/Curriculum Coord only) — opens inline edit panel within this tab.

#### Tab: Reviewer Notes
Threaded notes view. Each entry: reviewer avatar, name, timestamp, note text.
[Add Note] input at bottom — visible to any reviewer role. Notes persist across sessions and are visible to all reviewers (not uploader).

#### Tab: Decision
Visible to: CAO, Academic Director, Curriculum Coordinator.

| Action | Behaviour |
|---|---|
| [Approve & Publish] | Publishes to Content Library immediately. Status → Approved. Uploader notified. |
| [Request Changes] | Opens textarea for feedback message. Status remains In Review. Uploader notified with feedback. |
| [Reject] | Opens reject reason textarea (required, min 20 chars). Uploader notified with reason checkbox. Status → Rejected. |

**Note for Curriculum Coordinator:** Approve & Publish limited to content within their assigned stream scope. Cross-stream approvals require CAO or Academic Dir.

### 5.2 Drawer: `reject-reason` — Rejection Feedback
- **Trigger:** Reject row action or Reject button in Decision tab
- **Width:** 480px

| Field | Type | Required | Validation |
|---|---|---|---|
| Rejection Reason | Textarea | ✅ | Min 20 chars — must be specific enough for uploader to act on |
| Specific Issues | Multi-select | ❌ | Incorrect metadata · Low quality · Copyrighted content · Wrong subject · Duplicate content |
| Notify Branch Principal | Checkbox | — | Default off — on only if submission is from a branch teacher and principal oversight is needed |
| Notify Uploader via WhatsApp | Checkbox | — | Default on |

**Submit:** "Send Rejection" — status updated, uploader notified.

---

## 6. Charts

### 6.1 Queue Status Breakdown (Donut Chart)
- **Type:** Donut chart
- **Data:** Count of items in each status (Pending / In Review / Approved / Rejected)
- **Tooltip:** Status · Count · %
- **Export:** PNG

### 6.2 Submissions per Week (Bar Chart)
- **Type:** Vertical bar chart — last 8 weeks
- **Data:** Submissions received vs decisions made per week
- **X-axis:** Week
- **Y-axis:** Count
- **Bars:** Received (blue) · Approved (green) · Rejected (red)
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Content approved | "'[Title]' approved and live in Content Library." | Success | 4s |
| Changes requested | "Feedback sent to uploader for '[Title]'." | Info | 4s |
| Content rejected | "'[Title]' rejected. Uploader notified." | Warning | 6s |
| Reviewer assigned | "[Reviewer Name] assigned to '[Title]'." | Success | 4s |
| Bulk approved | "[N] items approved and added to Content Library." | Success | 4s |
| Bulk assigned | "All pending items assigned to [Reviewer Name]." | Success | 4s |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No items in queue | "No content pending review" | "All submissions have been reviewed. The queue is clear." | — |
| No pending items | "No pending items" | "All submissions are either In Review, Approved, or Rejected." | [View All Statuses] |
| Filter returns empty | "No items match your filters" | "Try removing some filters." | [Clear All Filters] |
| No results for search | "No items match" | "Try a different title or branch name." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| content-review drawer open | Spinner + skeleton tabs |
| Preview tab load (PDF/Video) | Spinner in preview area while content loads |
| Approve/Reject action | Spinner in action button |
| Bulk approve | Full-page overlay "Approving [N] items…" |
| Charts load | Skeleton chart placeholders |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Curriculum Coord G2 | Stream Coords G3 | MIS Officer G1 |
|---|---|---|---|---|---|
| [Approve All Passing] button | ✅ | ✅ | ❌ | ❌ | ❌ |
| [Export XLSX] button | ✅ | ✅ | ✅ | ✅ | ✅ |
| Assign Reviewer action | ✅ | ✅ | ✅ | ❌ | ❌ |
| Approve row action | ✅ | ✅ | ✅ (own stream) | ❌ | ❌ |
| Reject row action | ✅ | ✅ | ✅ (own stream) | ❌ | ❌ |
| Request Changes action | ✅ | ✅ | ✅ (own stream) | ❌ | ❌ |
| Decision tab in drawer | ✅ | ✅ | ✅ (own stream) | ❌ | ❌ |
| Reviewer Notes tab | ✅ | ✅ | ✅ | ❌ | ❌ |
| Bulk approve | ✅ | ✅ | ❌ | ❌ | ❌ |
| Assigned Reviewer column | ✅ | ✅ | ✅ | ❌ | ✅ |
| Stream filter (all streams) | ✅ | ✅ | ✅ | ❌ (own only) | ✅ |
| Age column | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/content-uploads/` | JWT | Queue list (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/content-uploads/{item_id}/` | JWT | Item detail + preview metadata |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/{item_id}/assign/` | JWT (CAO/Dir/Coord) | Assign reviewer |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/{item_id}/approve/` | JWT (CAO/Dir/Coord) | Approve item |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/{item_id}/reject/` | JWT (CAO/Dir/Coord) | Reject item with reason |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/{item_id}/request-changes/` | JWT (CAO/Dir/Coord) | Request changes with feedback |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/{item_id}/notes/` | JWT (reviewer roles) | Add reviewer note |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/bulk-approve/` | JWT (CAO/Dir) | Bulk approve selected items |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/bulk-assign/` | JWT (CAO/Dir/Coord) | Bulk assign reviewer |
| GET | `/api/v1/group/{group_id}/acad/content-uploads/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/content-uploads/export/` | JWT | XLSX export |
| GET | `/api/v1/group/{group_id}/acad/content-uploads/charts/status-breakdown/` | JWT | Donut chart data |
| GET | `/api/v1/group/{group_id}/acad/content-uploads/charts/submissions-trend/` | JWT | Bar chart data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Queue search | `input delay:300ms` | GET `.../content-uploads/?q=` | `#queue-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../content-uploads/?filters=` | `#queue-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../content-uploads/?sort=&dir=` | `#queue-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../content-uploads/?page=` | `#queue-table-section` | `innerHTML` |
| Preview drawer open | `click` | GET `.../content-uploads/{id}/` | `#drawer-body` | `innerHTML` |
| Approve action (row) | `click` | POST `.../content-uploads/{id}/approve/` | `#queue-row-{id}` | `outerHTML` |
| Assign reviewer (popover) | `click` | GET `.../content-uploads/{id}/assign-form/` | `#assign-popover-{id}` | `innerHTML` |
| Assign submit | `submit` | POST `.../content-uploads/{id}/assign/` | `#queue-row-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../content-uploads/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
