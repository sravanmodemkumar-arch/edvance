# 19 — Stream Configuration

> **URL:** `/group/acad/streams/`
> **File:** `19-stream-configuration.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Academic Director G3 · Curriculum Coordinator G2 · Stream Coords G3 · IIT Foundation Director G3 · JEE/NEET Integration Head G3

---

## 1. Purpose

Stream Configuration defines what a stream fundamentally is — its constituent subjects, minimum marks per subject, aggregate passing criteria, eligible class range, and which branches are permitted to offer it. This page is the authoritative source for stream identity across the group. Every other module that references "MPC" or "BiPC" or "Integrated JEE" derives its understanding of those streams from the configuration maintained here.

For a group offering 7–8 distinct streams across up to 50 branches, stream configuration is not trivial. An Integrated JEE stream combines regular MPC subjects with coaching-specific modules — Physics, Chemistry, Maths from CBSE syllabus plus JEE-specific problem-solving periods. The configuration for such a stream must specify subject weightages precisely, because those weightages determine how the result engine computes pass/fail, ranks students, and reports branch performance.

The CAO has full edit access; Academic Directors can view and propose changes. Stream Coordinators can view their own stream's configuration to understand the rules governing their domain. Changes to an active stream's pass criteria or subject list require the CAO to confirm, as they cascade to the result moderation engine, rank computation, and all branch exam schedules in progress.

---

## 2. Role Access

| Role | Level | Can View | Can Create | Can Edit | Can Delete | Notes |
|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All streams | ✅ | ✅ | ✅ (Deactivate only) | Full authority |
| Group Academic Director | G3 | ✅ All streams | ❌ | ✅ Propose (CAO approves) | ❌ | Can edit and submit for CAO review |
| Group Curriculum Coordinator | G2 | ✅ All streams | ❌ | ❌ | ❌ | View-only |
| Group Exam Controller | G3 | ✅ All streams | ❌ | ❌ | ❌ | View to understand exam scope |
| Group Results Coordinator | G3 | ✅ All streams | ❌ | ❌ | ❌ | View pass criteria for result engine |
| Stream Coord — MPC | G3 | ✅ MPC only | ❌ | ❌ | ❌ | Own stream only |
| Stream Coord — BiPC | G3 | ✅ BiPC only | ❌ | ❌ | ❌ | Own stream only |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC only | ❌ | ❌ | ❌ | Own stream only |
| JEE/NEET Integration Head | G3 | ✅ Integrated JEE/NEET | ❌ | ❌ | ❌ | View integrated stream config |
| IIT Foundation Director | G3 | ✅ Foundation only | ❌ | ❌ | ❌ | View Foundation Classes 6–10 |
| Olympiad & Scholarship Coord | G3 | ✅ All streams | ❌ | ❌ | ❌ | View for eligibility criteria |
| Special Education Coordinator | G3 | ✅ All streams | ❌ | ❌ | ❌ | View for IEP stream placement |
| Academic MIS Officer | G1 | ❌ | ❌ | ❌ | ❌ | No access |
| Academic Calendar Manager | G3 | ❌ | ❌ | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Stream Configuration
```

### 3.2 Page Header (with action buttons — role-gated)
```
Stream Configuration                      [+ New Stream]
[Group Name] · Defines streams, subjects, pass criteria         (CAO only)
```

Action button visibility:
- `[+ New Stream]` — CAO only

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Streams Configured | Count |
| Active Streams | Streams currently offered in at least 1 branch |
| Inactive Streams | Configured but not yet offered |
| Branches with MPC | Count |
| Branches with BiPC | Count |
| Branches with Foundation | Count |

Stats bar refreshes on page load.

---

## 4. Main Content — Stream Cards

The primary display is a responsive card grid. One card per stream. Cards are arranged in the following canonical order: MPC · BiPC · MEC · CEC · HEC · IIT Foundation · Integrated JEE · Integrated NEET.

### 4.1 Search
- Instant filter on stream name or subject name within cards
- 300ms debounce · Dims non-matching cards

### 4.2 Filters
Minimal — stream cards are few enough to not require a full filter drawer.

| Filter | Type | Options |
|---|---|---|
| Status | Toggle group | All · Active · Inactive |
| Class Range | Select | Classes 6–10 (Foundation) · Classes 11–12 (Senior Secondary) |

### 4.3 Stream Card Content

Each card displays:
- **Stream name** (large heading) + Status badge (Active / Inactive)
- **Class range** — e.g. "Class 11–12" or "Class 6–10"
- **Subjects list** — Bullet list of all subjects in this stream with subject code
- **Min marks per subject** — e.g. Physics: 35%, Chemistry: 35%, Maths: 35%
- **Aggregate pass %** — e.g. Overall aggregate ≥ 35% to pass
- **Active branches count** — "Offered in 38 branches"
- **Board affiliation** — CBSE / BSEAP / BSETS
- **[Edit] button** — Visible to CAO (direct edit) and Academic Dir (proposes change)
- **[View Branches] link** — Opens filtered branch list showing which branches offer this stream

### 4.4 Card Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| Edit | Pencil | CAO (direct), Academic Dir (propose) | `stream-edit` drawer 640px | CAO: saves immediately. Academic Dir: submits proposal for CAO approval |
| Deactivate | Toggle | CAO only | Confirm modal 420px | Cannot deactivate if branch has active students in stream |
| View Branches | Link | All | Opens Branch Overview filtered to this stream | External navigation |

---

## 5. Drawers & Modals

### 5.1 Drawer: `stream-create` — New Stream (CAO only)
- **Trigger:** [+ New Stream] header button
- **Width:** 640px
- **Tabs:** Identity · Subjects & Weights · Pass Criteria · Eligible Classes · Branch Toggle

#### Tab: Identity
| Field | Type | Required | Validation |
|---|---|---|---|
| Stream Name | Text | ✅ | Min 2 chars, max 100, unique in group |
| Stream Code | Text | ✅ | Alphanumeric, max 10, e.g. MPC, BIPC, ITF |
| Stream Type | Select | ✅ | Regular · Integrated Coaching · Foundation |
| Board | Multi-select | ✅ | CBSE · BSEAP · BSETS · ICSE |
| Description | Textarea | ❌ | Max 500 chars — shown on branch enrollment pages |
| Status | Select | ✅ | Active · Inactive |

#### Tab: Subjects & Weights
Dynamic subject rows. Add/remove subjects. Drag to reorder.

| Field | Type | Required | Validation |
|---|---|---|---|
| Subject | Select | ✅ per row | From Subject-Topic Master |
| Subject Code | Text (auto-filled) | ✅ | Auto-populated from Subject-Topic Master |
| Exam Weightage % | Number | ✅ per row | All subject weightages must sum to 100% |
| Is Core Subject | Toggle | ✅ | Core subjects must individually pass |
| Periods per Week | Number | ❌ | For timetable reference |

Validation: total weightage must equal 100% before tab is considered valid.

#### Tab: Pass Criteria
| Field | Type | Required | Validation |
|---|---|---|---|
| Min Marks per Core Subject | Number | ✅ | %, 1–100. Applied per subject marked as Core |
| Aggregate Pass % | Number | ✅ | Minimum aggregate to pass stream overall |
| Grace Marks Allowed | Toggle | ❌ | Enable grace mark system |
| Max Grace per Subject | Number | Conditional | Required if grace marks enabled |
| Compartment Allowed | Toggle | ❌ | Enable compartment exam for fail students |
| Attendance Requirement | Number | ❌ | Min attendance % to be eligible for exam |

#### Tab: Eligible Classes
| Field | Type | Required | Notes |
|---|---|---|---|
| Class Range | Multi-select | ✅ | Class 6 · 7 · 8 · 9 · 10 · 11 · 12 |
| Minimum Age for Enrollment | Number | ❌ | e.g. 14 years for Class 9 |
| Prerequisites | Multi-select | ❌ | Required previous streams or class completions |

#### Tab: Branch Toggle
| Field | Type | Required | Notes |
|---|---|---|---|
| Offer to All Branches | Toggle | ✅ | On = all branches may offer this stream |
| Select Branches | Multi-select | Conditional | Required if "All Branches" is off — select specific branches |

**Submit:** "Create Stream" — all tabs must be valid. CAO confirms, stream becomes active.

### 5.2 Drawer: `stream-edit` — Edit Stream
- **Width:** 640px — same tabs as `stream-create`, pre-filled
- **CAO:** Saves directly on submit
- **Academic Director:** Submit shows "Propose Change" button — creates a change proposal in CAO's approval queue with diff summary. CAO receives notification. Original stream unchanged until CAO approves.
- **Warning on subject change:** "Changing subjects in an active stream will affect the exam paper builder and result engine. Existing exam papers referencing removed subjects will need manual review."

### 5.3 Modal: Deactivate Stream Confirm
- **Width:** 420px
- **Content:** "Deactivate [Stream Name]? Branches currently offering this stream will be unable to enroll new students."
- **Check:** System verifies no active students are currently enrolled. If yes: blocks deactivation with message "Cannot deactivate — [N] students actively enrolled in this stream across [M] branches."
- **Fields:** Reason (required, min 20 chars) · Effective date (date picker — cannot be past)
- **Buttons:** [Confirm Deactivate] (danger) + [Cancel]

---

## 6. Charts

No dedicated charts section. Stats bar provides the key summary. The Branch Overview page (09) provides the detailed branch × stream matrix.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Stream created | "[Stream Name] stream created." | Success | 4s |
| Stream updated (CAO) | "[Stream Name] configuration updated." | Success | 4s |
| Change proposed (Academic Dir) | "Change proposal submitted. CAO will review." | Info | 4s |
| Change approved by CAO | "[Stream Name] update approved and applied." | Success | 4s |
| Stream deactivated | "[Stream Name] deactivated. Branch principals notified." | Warning | 6s |
| Deactivation blocked | "Cannot deactivate — [N] students currently enrolled." | Error | Manual |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No streams configured | "No streams configured" | "Add the first stream to define your academic offerings." | [+ New Stream] (CAO only) |
| Search returns no cards | "No streams match" | "Try a different stream or subject name." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + 4 skeleton cards (2×2 grid) |
| Search/filter | Cards fade and reload — skeleton overlay |
| stream-create/edit drawer open | Spinner in drawer body |
| Tab change inside drawer | Spinner in tab content area |
| Stream create submit | Spinner in submit button · success toast on resolve |
| Deactivation confirm | Spinner in confirm button |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Dir G3 | Curriculum Coord G2 | Stream Coords G3 | JEE/NEET Head G3 | Foundation Dir G3 |
|---|---|---|---|---|---|---|
| [+ New Stream] button | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit button (card) | ✅ (direct save) | ✅ (propose only) | ❌ | ❌ | ❌ | ❌ |
| Deactivate button | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| View Branches link | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ (own) | ✅ (own) |
| All stream cards visible | ✅ | ✅ | ✅ | ❌ (own only) | ✅ (Integrated) | ✅ (Foundation) |
| Pass Criteria tab | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ (own) | ✅ (own) |
| Branch Toggle tab | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Change proposal notification | ✅ (receives) | ✅ (sends) | ❌ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/streams/` | JWT | List all streams (card data) |
| POST | `/api/v1/group/{group_id}/acad/streams/` | JWT (CAO) | Create new stream |
| GET | `/api/v1/group/{group_id}/acad/streams/{stream_id}/` | JWT | Stream detail |
| PUT | `/api/v1/group/{group_id}/acad/streams/{stream_id}/` | JWT (CAO/Dir) | Update stream (CAO: direct, Dir: proposal) |
| POST | `/api/v1/group/{group_id}/acad/streams/{stream_id}/deactivate/` | JWT (CAO) | Deactivate stream |
| POST | `/api/v1/group/{group_id}/acad/streams/{stream_id}/approve-change/` | JWT (CAO) | Approve Academic Dir's change proposal |
| GET | `/api/v1/group/{group_id}/acad/streams/stats/` | JWT | Summary stats bar data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Stream search | `input delay:300ms` | GET `.../streams/?q=` | `#stream-cards-grid` | `innerHTML` |
| Status filter | `change` | GET `.../streams/?status=` | `#stream-cards-grid` | `innerHTML` |
| Edit drawer open | `click` | GET `.../streams/{id}/edit-form/` | `#drawer-body` | `innerHTML` |
| Create drawer open | `click` | GET `.../streams/create-form/` | `#drawer-body` | `innerHTML` |
| Stream save (CAO) | `submit` | PUT `.../streams/{id}/` | `#stream-card-{id}` | `outerHTML` |
| Deactivate confirm | `click` | POST `.../streams/{id}/deactivate/` | `#stream-card-{id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../streams/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
