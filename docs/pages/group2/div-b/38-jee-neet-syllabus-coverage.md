# 38 — JEE/NEET NTA Syllabus Coverage

> **URL:** `/group/acad/jee-neet/syllabus-coverage/`
> **File:** `38-jee-neet-syllabus-coverage.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** JEE/NEET Integration Head G3 · CAO G4 · Curriculum Coordinator G2

---

## 1. Purpose

The NTA Syllabus Coverage page maps the group's current JEE/NEET coaching curriculum against the official National Testing Agency (NTA) syllabus for JEE Main, JEE Advanced, and NEET-UG. The NTA publishes a fixed list of topics for each exam — and the gap between what a group's curriculum covers and what NTA requires is directly visible on this page.

For JEE Main, the NTA syllabus covers approximately 90 topics across Physics, Chemistry, and Mathematics. For NEET-UG, it covers approximately 97 topics across Physics, Chemistry, Botany, and Zoology. Each topic in the NTA list is mapped against the group's Subject-Topic Master and the Shared Content Library to determine whether the topic is: Fully Covered (study material exists + taught in coaching), Partially Covered (material exists but not fully taught, or taught but material lacking), or Not Covered (neither material nor teaching).

The primary audience — JEE/NEET Integration Head and Curriculum Coordinator — uses this page to identify gaps before the exam season and to plan content creation or procurement. A topic that appears on the NTA syllabus but is not in the group's coaching curriculum is a direct risk to student performance. This page makes that risk visible, prioritisable, and actionable through the "Bulk Assign" feature that links uncovered topics directly to the Content Library.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All subjects, all exams | ✅ View · Export gap report | Full visibility |
| Group Academic Director | G3 | ✅ All subjects | ❌ | Read-only |
| Group Curriculum Coordinator | G2 | ✅ All subjects | ✅ Edit coverage status · Bulk assign · Link resources | Primary content actor |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Group Stream Coord — MPC | G3 | ✅ JEE subjects (Physics/Chem/Maths) | ❌ | Read-only, filtered |
| Group Stream Coord — BiPC | G3 | ✅ NEET subjects (Physics/Chem/Bio) | ❌ | Read-only, filtered |
| Group Stream Coord — MEC/CEC | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ✅ All subjects | ✅ Edit coverage status · Bulk assign · Export | Primary operator |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ Summary stats only | ❌ | Read-only summary |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  JEE/NEET  ›  NTA Syllabus Coverage
```

### 3.2 Page Header
```
JEE/NEET NTA Syllabus Coverage                      [Export Gap Report PDF ↓]  [Export XLSX ↓]
[Group Name] · Exam: [JEE Main | JEE Advanced | NEET-UG] toggle
```

**Exam toggle:** Three options — JEE Main · JEE Advanced · NEET-UG. Switches the entire topic list and coverage data.

### 3.3 Summary Stats Bar (for selected exam)

| Stat | Value |
|---|---|
| NTA Topics — Total | 92 (JEE Main example) |
| Fully Covered | 68 (73.9%) |
| Partially Covered | 14 (15.2%) |
| Not Covered | 10 (10.9%) |
| Coverage Score | 73.9% |
| Last Updated | DD MMM YYYY |

**Coverage Score** is shown as a gauge chart (0–100%) in the stats bar area — colour-coded: Red < 60% · Amber 60–80% · Green > 80%.

---

## 4. Main Content

### 4.1 Coverage Matrix Table

**Search:** Topic name or keyword — 300ms debounce.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Subject | Multi-select | Physics · Chemistry · Maths (JEE) · Biology [Botany/Zoology] (NEET) |
| Coverage Status | Multi-select | Fully Covered · Partially Covered · Not Covered |
| NTA Weightage | Select | High (> 5 questions historically) · Medium (2–5) · Low (1–2) |
| Last Updated | Select | Updated this month · Updated this term · Never updated |

Active filter chips: Dismissible, "Clear All" link.

### 4.2 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| ☐ | Checkbox | — | Row select for bulk assign |
| Subject | Badge | ✅ | Physics · Chemistry · Maths · Botany · Zoology |
| Chapter | Text | ✅ | Chapter grouping (e.g. "Mechanics" under Physics) |
| Topic (NTA) | Text | ✅ | Official NTA topic name |
| NTA Weightage | Badge | ✅ | High / Medium / Low (based on historical exam frequency) |
| Group Curriculum | Badge | ✅ | In Syllabus (✅) · Not in Syllabus (❌) · Partial (⚠) |
| Study Material | Badge | ✅ | Available (✅) · Partial (⚠) · Missing (❌) |
| Coverage Status | Badge | ✅ | Fully Covered (green) · Partially Covered (amber) · Not Covered (red) |
| Linked Resources | Number | ❌ | Count of content library items linked to this topic |
| Last Updated | Date | ✅ | When coverage status was last reviewed |
| Actions | — | ❌ | See row actions |

**Default sort:** Coverage Status (Not Covered first, then Partially Covered) — focuses attention on gaps.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50.

**Chapter grouping:** Topics grouped visually under chapter subheaders — expandable/collapsible. Collapsed by default when viewing the full list; expanded when filtering by subject.

### 4.3 Row Actions

| Action | Visible To | Opens | Notes |
|---|---|---|---|
| Edit Coverage Status | JEE/NEET Head · Curriculum Coord · CAO | Inline edit — row expands | Change coverage status + notes |
| Link Resources | JEE/NEET Head · Curriculum Coord | `link-resources` drawer 480px | Link content library items to this topic |
| View Resources | All with access | `view-resources` drawer 480px | Read-only view of linked resources |
| Mark as Covered | JEE/NEET Head · Curriculum Coord | Confirm modal 360px | Quick mark from Partial/Not Covered to Fully Covered |

### 4.4 Bulk Actions (shown when rows selected)

| Action | Visible To | Notes |
|---|---|---|
| Bulk Assign — Mark as Covered | JEE/NEET Head · Curriculum Coord · CAO | Sets all selected topics to "Fully Covered" with bulk note |
| Bulk Assign — Mark as Partially Covered | JEE/NEET Head · Curriculum Coord · CAO | Sets all selected to "Partially Covered" |
| Bulk Link Resource | JEE/NEET Head · Curriculum Coord | Links a single chosen resource to all selected topics |
| Export Selected Gaps (PDF) | All with export access | Gap report for selected topics only |

---

## 5. Drawers & Modals

### 5.1 Drawer: `link-resources`
- **Trigger:** "Link Resources" row action
- **Width:** 480px
- **Title:** "Link Resources — [Topic Name] — [Subject]"
- **Content:**

**Currently Linked Resources:**
Table: Resource Name · Type (PDF/Video/MCQ Set) · Uploaded By · Date Added · [Remove Link ×]

**Search and Add Resources:**
- Search bar: Full-text search from Content Library (page 17) — returns resources tagged to this subject
- Results list: Resource name · Type · Size/Duration · [Link →] button
- Filter: Type (PDF · Video · MCQ Set) · Stream (JEE/NEET) · Recency

- Instruction: "Resources must be approved in the Content Library before they can be linked here."
- [Create New Resource in Content Library →] — external link to page 17 with subject/topic pre-filled

**After linking:**
Coverage status auto-suggestion: "You've added study material for this topic. Do you want to update coverage to 'Partially Covered'?" — Yes/No prompt.

---

### 5.2 Drawer: `view-resources`
- **Trigger:** "View Resources" row action
- **Width:** 480px
- **Title:** "[Topic Name] — Linked Resources"
- **Content:** Read-only version of linked resources table + preview/download buttons
- All resources shown with type, uploader, and download/view link

---

### 5.3 Inline Row Edit — Coverage Status
- **Trigger:** "Edit Coverage Status" row action
- **Behaviour:** Row expands inline (not a separate drawer)
- **Fields:**
  - Coverage Status: Radio — Fully Covered · Partially Covered · Not Covered
  - Notes: Textarea — "What is covered? What is missing?" — optional
  - Group Curriculum: Toggle — In Syllabus · Not in Syllabus
  - Study Material: Toggle — Available · Partial · Missing
- **Buttons inline:** [Save] [Cancel]
- **On save:** Row collapses, status badge updates, Last Updated refreshes

---

### 5.4 Modal: `mark-covered-confirm`
- **Width:** 360px
- **Title:** "Mark as Fully Covered — [Topic Name]"
- **Fields:** Note (optional): "Confirm material and teaching complete for this topic"
- **Buttons:** [Mark as Covered] (primary green) + [Cancel]

---

### 5.5 Modal: `bulk-assign-confirm`
- **Width:** 400px
- **Title:** "Bulk Update — [N] Topics"
- **Content:** "Setting all [N] selected topics to [Coverage Status]."
- **Fields:** Bulk note (optional, max 200 chars) — applies to all selected topics
- **Buttons:** [Apply to [N] Topics] + [Cancel]

---

## 6. Charts

### 6.1 Coverage Gauge (inline in stats bar)
- **Type:** Semi-circle gauge
- **Value:** Coverage Score % (Fully Covered / Total)
- **Colour:** Red < 60% · Amber 60–80% · Green > 80%
- **Rendered:** As a small gauge widget within the stats bar area

### 6.2 Coverage by Subject (Horizontal Stacked Bar)
- **Type:** Horizontal stacked bar
- **Y-axis:** Subject names (Physics · Chemistry · Maths / Biology)
- **X-axis:** Topic count
- **Stacks:** Fully Covered (green) · Partially Covered (amber) · Not Covered (red)
- **Tooltip:** Subject · Covered: N · Partial: N · Not Covered: N · Coverage %
- **Colorblind-safe:** Green / Amber / Red with distinct patterns if needed
- **Export:** PNG

### 6.3 Coverage Progress Over Time (Line)
- **Type:** Line chart
- **X-axis:** Months (academic year)
- **Y-axis:** Coverage % (fully covered / total)
- **Lines:** JEE Main (blue) · JEE Advanced (teal) · NEET (green) — if user has access to all three
- **Tooltip:** Month · Coverage % per exam type
- **Purpose:** Shows how quickly coverage gaps are being closed across the year
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Coverage status updated | "[Topic Name] coverage updated to [Fully Covered / Partially Covered / Not Covered]." | Success | 4s |
| Resource linked | "[Resource Name] linked to [Topic Name]." | Success | 4s |
| Resource link removed | "Resource unlinked from [Topic Name]." | Info | 4s |
| Bulk update applied | "[N] topics updated to [Status]." | Success | 4s |
| Bulk resource linked | "[Resource Name] linked to [N] topics." | Success | 4s |
| Gap report export started | "Gap report PDF preparing — download will begin shortly." | Info | 4s |
| XLSX export started | "Coverage data XLSX preparing." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| NTA syllabus not loaded | "NTA Syllabus Not Configured" | "The official NTA syllabus has not been loaded for this exam. Contact the platform administrator." | — |
| No topics match filters | "No Topics Match" | "Try removing some filters to see more topics" | [Clear Filters] |
| Subject has full coverage | "All Topics Covered" | "All [Subject] topics are fully covered for this exam" | — |
| No resources linked to topic | "No Resources Linked" | "No study material has been linked to this topic yet" | [Link Resources] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar (gauge placeholder) + table (15 skeleton rows) |
| Exam toggle switch | Full page body skeleton reload |
| Filter/search apply | Inline skeleton rows (10) |
| Link-resources drawer open | Spinner in drawer body + skeleton resource list |
| Inline row edit | Row expands with form — minimal load, fields appear immediately |
| Charts load | Spinner centred in each chart card |
| Export triggers | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | JEE/NEET Head G3 | CAO G4 | Curriculum Coord G2 | Stream Coords G3 | MIS G1 |
|---|---|---|---|---|---|
| Exam toggle (all 3) | ✅ | ✅ | ✅ | ✅ (own stream only) | ✅ (summary only) |
| Edit Coverage Status (inline) | ✅ | ✅ | ✅ | ❌ | ❌ |
| Link Resources action | ✅ | ❌ | ✅ | ❌ | ❌ |
| Mark as Covered action | ✅ | ✅ | ✅ | ❌ | ❌ |
| Bulk Assign actions | ✅ | ✅ | ✅ | ❌ | ❌ |
| Remove resource link | ✅ | ❌ | ✅ | ❌ | ❌ |
| Export Gap Report PDF | ✅ | ✅ | ✅ | ❌ | ❌ |
| Export XLSX | ✅ | ✅ | ✅ | ❌ | ❌ |
| Coverage Progress chart | ✅ | ✅ | ✅ | ❌ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/` | JWT | Topic coverage list (filtered/paginated) |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/stats/` | JWT | Summary stats bar + coverage score |
| PATCH | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/{topic_id}/` | JWT (JEE/NEET Head / Curriculum Coord / CAO) | Update coverage status for one topic |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/bulk-update/` | JWT (JEE/NEET Head / Curriculum Coord / CAO) | Bulk coverage status update |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/{topic_id}/resources/` | JWT | List resources linked to topic |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/{topic_id}/resources/` | JWT (JEE/NEET Head / Curriculum Coord) | Link a resource to topic |
| DELETE | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/{topic_id}/resources/{resource_id}/` | JWT (JEE/NEET Head / Curriculum Coord) | Unlink resource |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/bulk-link-resource/` | JWT (JEE/NEET Head / Curriculum Coord) | Link resource to multiple topics |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/search-resources/` | JWT | Search content library for linkable resources |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/export/gap-report/?format=pdf` | JWT | Gap report PDF |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/export/?format=xlsx` | JWT | Full coverage data XLSX |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/charts/by-subject/` | JWT | Coverage by subject stacked bar chart |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/syllabus-coverage/charts/progress/` | JWT | Coverage progress over time chart |

Query params: `exam_type` (jee_main / jee_advanced / neet), `subject`, `coverage_status`, `nta_weightage`, `q` (search), `sort`, `page`.

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Exam toggle | `click` | GET `.../syllabus-coverage/?exam_type=` | `#coverage-page-body` | `innerHTML` |
| Topic search | `input delay:300ms` | GET `.../syllabus-coverage/?q=&exam_type=` | `#coverage-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../syllabus-coverage/?filters=&exam_type=` | `#coverage-table-section` | `innerHTML` |
| Sort / paginate | `click` | GET `.../syllabus-coverage/?sort=&page=&exam_type=` | `#coverage-table-section` | `innerHTML` |
| Edit inline expand | `click` | GET `.../syllabus-coverage/{id}/edit-form/` | `#topic-row-{id}-edit` | `innerHTML` |
| Save inline edit | `click` | PATCH `.../syllabus-coverage/{id}/` | `#topic-row-{id}` | `outerHTML` |
| Link resources drawer open | `click` | GET `.../syllabus-coverage/{id}/resources/` | `#drawer-body` | `innerHTML` |
| Link a resource | `click` | POST `.../syllabus-coverage/{id}/resources/` | `#linked-resources-list` | `innerHTML` |
| Unlink resource | `click` | DELETE `.../syllabus-coverage/{id}/resources/{rid}/` | `#linked-resources-list` | `innerHTML` |
| Resource search in drawer | `input delay:300ms` | GET `.../search-resources/?q=&subject=` | `#resource-search-results` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
