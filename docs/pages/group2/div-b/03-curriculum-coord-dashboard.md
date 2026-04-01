# 03 — Curriculum Coordinator Dashboard

> **URL:** `/group/acad/curriculum-coord/`
> **File:** `03-curriculum-coord-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group Curriculum Coordinator (G2) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group Curriculum Coordinator (G2). This role manages the group's shared content library, handles content upload and review workflows, maintains lesson plan standards and templates, and tracks the curriculum library's health. The Curriculum Coordinator is the gatekeeper of educational content quality — they approve or reject content submitted by branches and teachers, and they ensure every subject and topic has adequate study materials available.

At G2, this is a contributor and coordinator role rather than a decision-making one. The Curriculum Coordinator does not approve academic policy or exam results — their authority is over content. The dashboard is organised around the content pipeline: what has been uploaded today, what is pending review, what has been approved or rejected, and where coverage gaps exist across subjects and topics.

For a large group with 10,000–50,000 curriculum resources spanning 7+ streams and 80–120 subject-topic pairs per stream, this dashboard's search, filter, and status views are essential daily tools. All data is group-scoped and read from FastAPI endpoints backed by the content management module.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Curriculum Coordinator | G2 | Full — all sections, all actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | View only — cannot edit | CAO may view but not act on this role's exclusive dashboard |
| Group Academic Director | G3 | View only | Can approve/reject in content upload queue — not on this dashboard page itself |
| Group Exam Controller | G3 | — | Has own dashboard `/group/acad/exam-controller/` |
| Group Results Coordinator | G3 | — | Has own dashboard `/group/acad/results-coord/` |
| Group Stream Coord — MPC | G3 | — | Has own dashboard `/group/acad/stream/mpc/` |
| Group Stream Coord — BiPC | G3 | — | Has own dashboard `/group/acad/stream/bipc/` |
| Group Stream Coord — MEC/CEC | G3 | — | Has own dashboard `/group/acad/stream/mec-cec/` |
| Group JEE/NEET Integration Head | G3 | — | Has own dashboard `/group/acad/jee-neet/` |
| Group IIT Foundation Director | G3 | — | Has own dashboard `/group/acad/iit-foundation/` |
| Group Olympiad & Scholarship Coord | G3 | — | Has own dashboard `/group/acad/olympiad/` |
| Group Special Education Coordinator | G3 | — | Has own dashboard `/group/acad/special-ed/` |
| Group Academic MIS Officer | G1 | — | Has own dashboard `/group/acad/mis/` |
| Group Academic Calendar Manager | G3 | — | Has own dashboard `/group/acad/cal-manager/` |

> **Access enforcement:** Django view decorator `@require_role('curriculum_coord')`. Any other role hitting this URL is redirected to their own dashboard. G4 roles landing here see a read-only banner: "Viewing as [Role] — write actions are disabled on this page."

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Division  ›  Curriculum Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                 [Upload New Content ↑]  [Settings ⚙]
[Group Name] — Group Curriculum Coordinator · Last login: [date time] · [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel at top of page, above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown

**Alert trigger examples:**
- Content upload queue has ≥10 items pending review for >3 days (red — Critical)
- Subject with zero lesson plans detected — gap in coverage (red — Critical)
- Rejected content with no replacement uploaded for >5 days (yellow — Warning)
- Content library has not had any new additions in >7 days (yellow — Warning)
- Lesson plan template overdue for review (yellow — Warning — CAO set deadline)

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Resources | `14,382` resources in library · `+47` added this month | Content library | Always neutral (informational) | → Shared Content Library `/group/acad/content-library/` |
| Pending Review | `23` items awaiting group-level approval | Upload queue | Green = 0 · Yellow 1–9 · Red ≥10 | → Section 5.3 (Pending Reviews) |
| Rejected Items | `5` rejected this month without replacement | Content tracker | Green = 0 · Yellow 1–4 · Red ≥5 | → Section 5.3 (filter: Rejected) |
| Lesson Plan Coverage | `78%` topics with at least one lesson plan across all streams | Lesson plan data | Green ≥90% · Yellow 70–89% · Red <70% | → Section 5.4 (Heatmap) |
| Topics with Zero Plans | `31` topics across all streams with no lesson plan | Coverage tracker | Green = 0 · Yellow 1–20 · Red >20 | → Section 5.5 (Gap Alerts) |
| Content Downloads | `1,247` downloads by branches this month | Analytics | Always neutral (trend arrow vs last month) | → Section 5.6 (Bar Chart) |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/curriculum-coord/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 Content Library Stats — Stat Cards

> Overview of the content library's current state — totals, monthly additions, and review pipeline.

**Display:** 4 stat cards in a 2×2 grid within a single card panel.

| Card | Value | Notes |
|---|---|---|
| Total Resources | `14,382` | All-time total active resources in library |
| Added This Month | `47` | Resources added in current calendar month |
| Pending Approval | `23` | Awaiting group-level review (links to Section 5.3) |
| Rejected This Month | `8` | Rejected by reviewer — needs replacement |

**Each card:** Count (large) · Trend vs last month (small arrow + %) · Link to detail.

**Click on "Pending Approval" card:** Scrolls to Section 5.3 (Pending Content Reviews).

**Click on "Rejected This Month" card:** Scrolls to Section 5.3 with filter pre-set to "Rejected".

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/curriculum-coord/library-stats/"` `hx-trigger="every 5m"` `hx-target="#library-stats-cards"` `hx-swap="innerHTML"`.

---

### 5.2 Upload Queue Status — Progress List

> Files uploaded today — current processing/approval/rejection status shown as a live-updating list.

**Display:** Vertical progress list — each item is an upload card.

**Card fields:** File icon (PDF/Video/MCQ/Revision) · Title (truncated to 60 chars) · Subject · Class · Stream · Uploader (name + branch) · Upload time · Status badge · Progress bar (for processing).

**Status badges and colours:**
- `Processing` → Blue spinner badge — file is being virus-scanned and indexed
- `Awaiting Review` → Yellow — file queued for coordinator review
- `Approved` → Green — live in library
- `Rejected` → Red — with rejection reason shown inline
- `Duplicate Detected` → Orange — content fingerprint matches existing resource

**Today's uploads only:** Toggle to "All time" shows full upload queue (links to `/group/acad/content-uploads/`).

**[Review →]** button on "Awaiting Review" cards opens content review drawer.

**[Re-upload →]** button on "Rejected" cards opens upload drawer pre-filled with rejected item's metadata.

**Empty state:** "No uploads today. Click 'Upload New Content' in the header to add resources." — Upload icon illustration.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/curriculum-coord/upload-queue/?today=true"` `hx-trigger="every 2m"` `hx-target="#upload-queue-list"` `hx-swap="innerHTML"`.

---

### 5.3 Pending Content Reviews — Action Queue

> Content submitted by branches awaiting group-level approval — the Curriculum Coordinator's primary daily action list.

**Display:** Card list — each pending review item as an action card.

**Card fields:** Content type badge · Title · Subject · Stream · Class · Submitted by (Teacher name + Branch) · Submitted at · Days pending (red if >3) · [Preview →] [Approve ✓] [Reject ✗] buttons.

**Sort:** Days pending descending (oldest first).

**Filter chips (within section):**
- Type: All / PDF / Video / MCQ Set / Revision Sheet
- Stream: All / MPC / BiPC / MEC-CEC / Foundation
- Subject: Searchable dropdown

**[Preview →]:** Opens content review drawer (560px) — Preview tab shows file rendered or video thumbnail. Metadata tab shows subject/topic/class/stream tags. Reviewer Notes tab for comments.

**[Approve ✓]:** `hx-post="/api/v1/group/{group_id}/acad/content-uploads/{item_id}/approve/"` — toast + item removed from queue.

**[Reject ✗]:** Opens reject modal (400px) — required reason (min 20 chars) + select rejection category (Quality / Incorrect Subject-Topic / Copyright Concern / Duplicate / Other) + notify submitter checkbox.

**"View Full Upload Queue →"** links to `/group/acad/content-uploads/`.

**Pagination (within section):** Load more (12 cards visible, "Load 12 more →" button).

**Empty state:** "No content pending review. All submissions have been processed." — Green checkmark illustration.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/curriculum-coord/pending-reviews/"` `hx-trigger="every 2m"` `hx-target="#pending-reviews-section"` `hx-swap="innerHTML"`.

---

### 5.4 Lesson Plan Coverage — Branch × Subject Heatmap

> Colour-coded heatmap showing lesson plan coverage per branch per subject — the Curriculum Coordinator sees exactly where the gaps are.

**Display:** Heatmap grid. Rows = Branches. Columns = Subjects (scoped to selected stream). Cells = coverage status.

**Cell colour logic:**
- Green (`bg-green-500`): Lesson plan complete (all topics for this subject have a plan)
- Amber (`bg-yellow-400`): Partial — some topics have plans, some do not
- Red (`bg-red-500`): No lesson plan — zero plans for any topic in this subject
- Grey (`bg-gray-200`): Subject not offered at this branch

**Cell tooltip:** Branch · Subject · Topics covered: X/Y · Last plan uploaded: [date] · Uploader name.

**Click on cell:** Opens lesson plan detail drawer (560px) — topic-level plan status, upload history, missing topics list.

**Stream filter (above heatmap):** Single-select — MPC / BiPC / MEC-CEC / Foundation. Required (no "All" option — too many columns). Defaults to MPC.

**Branch filter:** Multi-select — defaults to All.

**"View Lesson Plan Standards →"** links to `/group/acad/lesson-plans/`.

**Export:** "Export as CSV" — downloads heatmap data as a flat table.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/curriculum-coord/lesson-plan-heatmap/?stream={stream_id}"` `hx-trigger="change"` on stream filter `hx-target="#heatmap-grid"` `hx-swap="innerHTML"`.

---

### 5.5 Subject-Topic Gaps — Alert List

> Topics with zero lesson plans across any branch — the Curriculum Coordinator must ensure these gaps are filled.

**Display:** Alert list — each item: Red indicator dot · Subject · Topic name · Class · Stream · Branches affected count · [Assign Task →] button.

**Sort:** By number of branches affected (descending — worst gaps first).

**Filter (within section):** Stream selector (single-select) · Class selector.

**[Assign Task →]:** Opens task assignment modal (420px) — pre-filled with gap details. Fields: Assign to (branch coordinator or group teacher — search dropdown) · Due date · Priority (Low/Medium/High) · Notes. POST to create task in academic task tracker.

**Count badge:** Total gaps shown above list — e.g. "31 topics with no lesson plan."

**"View All Topics in Subject-Topic Master →"** links to `/group/acad/subject-topic/`.

**Empty state:** "No topic gaps found. All topics have at least one lesson plan." — Green shield illustration.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/curriculum-coord/topic-gaps/?stream={}&class={}"` `hx-trigger="change"` on filters `hx-target="#topic-gaps-list"` `hx-swap="innerHTML"`.

---

### 5.6 Content Downloads by Branch — Bar Chart

> Which branches are accessing the most content from the shared library — indicates engagement and usage patterns.

**Display:** Horizontal bar chart (Chart.js 4.x). Y-axis = branch names. X-axis = download count. Sorted descending (highest first).

**Tooltip:** Branch name · Total downloads · Most downloaded subject · Most downloaded content type.

**Filters (within card):**
- Date range: This Month / Last Month / This Term / Custom
- Content type: All / PDF / Video / MCQ Set / Revision

**Click on bar:** Opens branch content usage drawer (480px) — top 10 downloaded resources for that branch with subject, type, count.

**Export:** "Export PNG" button.

**Empty state:** "No download data for the selected period. Content access tracking requires branches to use the portal."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/curriculum-coord/content-downloads/"` on filter change `hx-target="#downloads-chart"` `hx-swap="innerHTML"`.

---

### 5.7 Recent Uploads — Table

> Last 20 uploads to the content library — regardless of status — for quick review and audit.

**Display:** Sortable table.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Title | Text + icon | ✅ | File type icon (PDF/Video/MCQ/Revision) |
| Subject | Text | ✅ | |
| Topic | Text | ✅ | |
| Stream | Badge | ✅ | |
| Class | Text | ✅ | e.g. Class XI |
| Uploader | Text | ✅ | Name + Branch |
| Upload Date | Date | ✅ | |
| Status | Badge | ✅ | Processing / Awaiting Review / Approved / Rejected |
| Actions | — | ❌ | Preview · Edit Metadata · Re-review (if Approved) |

**Default sort:** Upload Date descending.

**No search or filter on this section** — it is a fixed last-20 snapshot. "View All in Content Library →" links to full searchable library.

**[Edit Metadata]:** Opens metadata edit drawer (480px) — Fields: Title, Subject (searchable dropdown), Topic, Class, Stream, Description. Can re-tag content without re-uploading file.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/curriculum-coord/recent-uploads/?limit=20"` `hx-trigger="every 2m"` `hx-target="#recent-uploads-table"` `hx-swap="innerHTML"`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `content-upload` (triggered by [Upload New Content ↑] header button)
- **Width:** 680px
- **Tabs:** File / Link · Metadata · Access Scope · Preview · Submit
- **File / Link tab:** Upload file (PDF max 50MB, XLSX max 10MB) OR paste YouTube/Google Drive URL · File type auto-detected · Virus scan status shown
- **Metadata tab:** Title (required) · Subject (searchable dropdown, required) · Topic (dependent on subject, required) · Class (multi-select, required) · Stream (multi-select, required) · Description (textarea) · Tags (multi-value input)
- **Access Scope tab:** Available to (All branches / Specific branches — multi-select) · Restrict download (All can download / Only specific branches)
- **Preview tab:** File rendered in browser (PDF iframe / video embed / MCQ question list preview)
- **Submit tab:** Summary of all fields — [Submit for Review] button
- **On submit:** `hx-post="/api/v1/group/{group_id}/acad/content-uploads/"` — toast + item appears in upload queue

### 6.2 Drawer: `content-review` (from Pending Reviews [Preview →] or Upload Queue [Review →])
- **Width:** 560px
- **Tabs:** Preview · Metadata · Reviewer Notes
- **Preview tab:** Renders content in browser — PDF iframe (with fallback "Download to preview"), video embed, MCQ list
- **Metadata tab:** All tags — subject, topic, class, stream, uploader, upload date, file size
- **Reviewer Notes tab:** Text area for notes (saved as draft, not submitted) · Previous review history for this uploader
- **Footer actions:** [Approve ✓] (primary green) · [Reject with Reason ✗] (danger red) · [Request Revision] (secondary)
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/content-uploads/{item_id}/review/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.3 Drawer: `lesson-plan-cell-detail` (from heatmap cell click)
- **Width:** 560px
- **Tabs:** Topics · Upload History · Missing Topics
- **Topics tab:** Table — Topic name, Subtopics covered, Plan uploaded Y/N, Last upload date, Uploaded by
- **Upload History tab:** All plan uploads for this subject-branch — date, uploader, status, file link
- **Missing Topics tab:** List of topics with no lesson plan — Topic, Chapter, Sequence no., [Assign Task →]
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/curriculum-coord/lesson-plan-cell/?branch={}&subject={}&stream={}"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.4 Drawer: `content-metadata-edit`
- **Width:** 480px
- **Fields:** Title · Subject (searchable dropdown) · Topic (dependent dropdown) · Class (multi-select) · Stream (multi-select) · Description · Tags
- **Buttons:** [Save Changes] + [Cancel]
- **HTMX:** `hx-put="/api/v1/group/{group_id}/acad/content-library/{resource_id}/"` on save

### 6.5 Drawer: `branch-content-usage` (from Downloads chart bar click)
- **Width:** 480px
- **Content:** Top 10 downloads for this branch — rank, title, subject, type, download count, last downloaded date
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/curriculum-coord/branch-downloads/{branch_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.6 Modal: `content-reject`
- **Width:** 400px
- **Fields:** Rejection reason (textarea, required, min 20 chars) · Category (select: Quality / Incorrect Subject-Topic / Copyright / Duplicate / Other) · Notify submitter (checkbox, default on)
- **Buttons:** [Confirm Rejection] (danger red) + [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/content-uploads/{item_id}/reject/"` — toast + item updated in queue

### 6.7 Modal: `topic-gap-assign-task`
- **Width:** 420px
- **Pre-filled:** Gap subject, topic, stream, class
- **Fields:** Assign to (search dropdown — group teachers or branch coordinators, required) · Due date (date picker, required) · Priority (Low/Medium/High, required) · Notes (textarea, optional)
- **Buttons:** [Create Task] + [Cancel]

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Content approved | "[Title] approved and added to the content library." | Success (green) | 4s auto-dismiss |
| Content rejected | "[Title] rejected. Submitter notified." | Success | 4s |
| Upload submitted | "[Title] submitted for review. It will appear in the pending queue shortly." | Info | 4s |
| Metadata saved | "Metadata for [Title] updated successfully." | Success | 4s |
| Task assigned (gap) | "Task assigned to [Name] for [Topic] gap in [Subject]." | Success | 4s |
| KPI load error | "Failed to load library data. Retrying…" | Error (red) | Manual dismiss |
| Upload queue refresh | "Upload queue refreshed." | Info | 3s |
| Export triggered | "Export started — download will begin shortly." | Info | 4s |
| Revision requested | "Revision request sent to [Uploader Name] for [Title]." | Info | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No pending reviews | Checkmark circle | "Review queue is clear" | "All submitted content has been reviewed. No items awaiting approval." | — |
| No uploads today | Upload cloud | "No uploads today" | "No content has been uploaded today. Click 'Upload New Content' to add resources." | [Upload New Content] |
| No topic gaps | Shield check | "No topic gaps found" | "Every topic in the curriculum has at least one lesson plan." | — |
| No download data | Chart outline | "No download data" | "No download activity recorded for the selected period." | — |
| Heatmap no data | Grid outline | "No lesson plan data" | "No lesson plans have been uploaded for the selected stream. Start by uploading templates." | [Go to Lesson Plan Standards] |
| Content library empty | Book outline | "Content library is empty" | "No resources have been uploaded yet. Start building the library." | [Upload New Content] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + library stats (4 cards) + upload queue (4 skeleton cards) + heatmap grid skeleton |
| KPI auto-refresh | Subtle shimmer over existing card values |
| Upload queue auto-refresh (every 2m) | Subtle shimmer over list items (no layout shift) |
| Pending reviews auto-refresh | Shimmer over card list |
| Heatmap stream filter change | Full heatmap grid shimmer + spinner |
| Content review drawer open | Spinner in drawer body + tab skeletons |
| Approve/Reject button click | Spinner inside button + button disabled |
| Downloads chart filter change | Chart area shimmer + spinner |
| Upload submit | Full drawer overlay: "Uploading and scanning… please wait" |
| Recent uploads table auto-refresh | Subtle shimmer over table rows |

---

## 10. Role-Based UI Visibility

| Element | Curriculum Coord G2 | CAO G4 (view-only) | Academic Director G3 (view-only) | All other roles |
|---|---|---|---|---|
| Page itself | ✅ Rendered | ✅ Read-only banner | ✅ Read-only banner | ❌ Redirected |
| Alert Banner | ✅ Shown | ✅ Shown | ✅ Shown | N/A |
| [Approve ✓] / [Reject ✗] in Pending Reviews | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Upload New Content] header button | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Edit Metadata] in Recent Uploads | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Assign Task →] in Topic Gaps | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Request Revision] in content-review drawer | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| Download chart and export buttons | ✅ Shown | ✅ Shown | ✅ Shown | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/dashboard/` | JWT (G2) | Full page data |
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/kpi-cards/` | JWT (G2) | KPI card values (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/library-stats/` | JWT (G2) | 4 library stat cards |
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/upload-queue/` | JWT (G2) | Upload queue list (today filter, status) |
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/pending-reviews/` | JWT (G2) | Pending content review cards |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/{item_id}/approve/` | JWT (G2) | Approve content item |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/{item_id}/reject/` | JWT (G2) | Reject with reason + category |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/{item_id}/request-revision/` | JWT (G2) | Request revision from uploader |
| GET | `/api/v1/group/{group_id}/acad/content-uploads/{item_id}/review/` | JWT (G2) | Content review drawer data |
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/lesson-plan-heatmap/` | JWT (G2) | Heatmap data (stream filter) |
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/lesson-plan-cell/` | JWT (G2) | Cell detail (branch, subject, stream) |
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/topic-gaps/` | JWT (G2) | Topics with zero plans (stream, class filters) |
| POST | `/api/v1/group/{group_id}/acad/curriculum-coord/topic-gaps/assign-task/` | JWT (G2) | Assign gap fill task |
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/content-downloads/` | JWT (G2) | Download chart data (date range, type) |
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/branch-downloads/{branch_id}/` | JWT (G2) | Branch download usage drawer |
| GET | `/api/v1/group/{group_id}/acad/curriculum-coord/recent-uploads/` | JWT (G2) | Last 20 uploads table |
| POST | `/api/v1/group/{group_id}/acad/content-uploads/` | JWT (G2) | Submit new content upload |
| PUT | `/api/v1/group/{group_id}/acad/content-library/{resource_id}/` | JWT (G2) | Update content metadata |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../curriculum-coord/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Library stats auto-refresh | `every 5m` | GET `.../curriculum-coord/library-stats/` | `#library-stats-cards` | `innerHTML` |
| Upload queue auto-refresh | `every 2m` | GET `.../curriculum-coord/upload-queue/?today=true` | `#upload-queue-list` | `innerHTML` |
| Pending reviews auto-refresh | `every 2m` | GET `.../curriculum-coord/pending-reviews/` | `#pending-reviews-section` | `innerHTML` |
| Pending reviews type filter | `click` | GET `.../curriculum-coord/pending-reviews/?type={}` | `#pending-reviews-section` | `innerHTML` |
| Approve button | `click` | POST `.../content-uploads/{id}/approve/` | `#pending-reviews-section` | `innerHTML` |
| Reject confirm (modal) | `click` on Confirm | POST `.../content-uploads/{id}/reject/` | `#pending-reviews-section` | `innerHTML` |
| Preview drawer open | `click` | GET `.../content-uploads/{id}/review/` | `#drawer-body` | `innerHTML` |
| Heatmap stream filter | `change` | GET `.../curriculum-coord/lesson-plan-heatmap/?stream={}` | `#heatmap-grid` | `innerHTML` |
| Heatmap cell click | `click` | GET `.../curriculum-coord/lesson-plan-cell/?branch={}&subject={}&stream={}` | `#drawer-body` | `innerHTML` |
| Topic gaps stream filter | `change` | GET `.../curriculum-coord/topic-gaps/?stream={}&class={}` | `#topic-gaps-list` | `innerHTML` |
| Downloads chart filter | `change` | GET `.../curriculum-coord/content-downloads/?range={}&type={}` | `#downloads-chart` | `innerHTML` |
| Downloads bar click | `click` | GET `.../curriculum-coord/branch-downloads/{branch_id}/` | `#drawer-body` | `innerHTML` |
| Recent uploads auto-refresh | `every 2m` | GET `.../curriculum-coord/recent-uploads/?limit=20` | `#recent-uploads-table` | `innerHTML` |
| Upload submit (drawer) | `submit` | POST `.../acad/content-uploads/` | `#drawer-body` | `innerHTML` |
| Metadata edit save | `click` | PUT `.../content-library/{id}/` | `#recent-uploads-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
