# 28 — Mark Scheme & Answer Keys

> **URL:** `/group/acad/answer-keys/`
> **File:** `28-answer-keys.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** CAO G4 · Exam Controller G3 · Stream Coords G3

---

## 1. Purpose

The Mark Scheme & Answer Keys page is the authoritative register for official answer keys for every exam paper used by the group. Answer keys are never published before an exam ends — the system enforces this with a date-lock that prevents publication until the exam's scheduled end time has passed. Once an exam concludes, the Exam Controller uploads the key, the CAO or Exam Controller publishes it to branches, and an optional challenge window opens for a defined period during which students can formally dispute specific answers through the branch portal.

The challenge workflow is a significant feature for groups that run competitive internal exams (particularly for JEE/NEET integrated streams and olympiad exams) where answer disputes are common. Each challenge is reviewed centrally by the Exam Controller or CAO. If a challenge is accepted, the answer key is revised, marks are recomputed automatically, and the Results Coordinator is notified to re-run the rank computation. The finalization step closes the challenge window permanently, locks the answer key, and signals the Result Moderation queue that marks can now be finalised for this exam.

At group scale — with 10,000–50,000 questions in the bank and potentially 100+ exam papers per year — the answer key register is an important audit artefact. Every key upload, publication, challenge, and finalization is timestamped and attributed to a specific actor.

---

## 2. Role Access

| Role | Level | Can View | Can Upload Key | Can Publish Key | Can Open Challenge Window | Can Review Challenge | Can Finalize | Notes |
|---|---|---|---|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All | ✅ | ✅ | ✅ | ✅ | ✅ | Full authority |
| Group Academic Director | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | ❌ | View-only |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ✅ All | ✅ | ✅ | ✅ | ✅ | ❌ | Cannot finalize — CAO finalizes |
| Group Results Coordinator | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | ❌ | View to coordinate result release timing |
| Stream Coord — MPC | G3 | ✅ MPC | ❌ | ❌ | ❌ | ❌ | ❌ | View own stream keys |
| Stream Coord — BiPC | G3 | ✅ BiPC | ❌ | ❌ | ❌ | ❌ | ❌ | View own stream keys |
| Stream Coord — MEC/CEC | G3 | ✅ MEC/CEC | ❌ | ❌ | ❌ | ❌ | ❌ | View own stream keys |
| JEE/NEET Integration Head | G3 | ✅ JEE/NEET | ❌ | ❌ | ❌ | ❌ | ❌ | View coaching exam keys |
| IIT Foundation Director | G3 | ✅ Foundation | ❌ | ❌ | ❌ | ❌ | ❌ | View Foundation keys |
| Olympiad & Scholarship Coord | G3 | ✅ All | ❌ | ❌ | ❌ | ❌ | ❌ | View olympiad answer keys |
| Special Education Coordinator | G3 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | No access |
| Academic MIS Officer | G1 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | No access |
| Academic Calendar Manager | G3 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  Mark Scheme & Answer Keys
```

### 3.2 Page Header (with action buttons — role-gated)
```
Mark Scheme & Answer Keys                 [Export XLSX ↓]
[Group Name] · Official answer keys — published post-exam only    (All with view access)
```

Action button visibility:
- `[Export XLSX ↓]` — CAO, Exam Controller

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Exam Papers | Count with at least one key record |
| Key Not Uploaded | Papers with no key entry |
| Key Uploaded (Not Published) | Ready to publish |
| Published | Published to branches |
| Challenge Window Open | Count with active challenge window |
| Open Challenges | Count of unreviewed student challenges |
| Finalized | Keys fully closed |

Stats bar refreshes on page load. "Open Challenges" shown in amber if > 0.

---

## 4. Main Answer Keys Table

### 4.1 Search
- Full-text across: Exam Name, Paper ID, Subject
- 300ms debounce · Highlights match in Exam Name column

### 4.2 Advanced Filters (slide-in filter drawer)

| Filter | Type | Options |
|---|---|---|
| Exam Name | Search input | From Group Exam Calendar |
| Stream | Multi-select | MPC · BiPC · MEC · CEC · HEC · Foundation · Integrated JEE · NEET |
| Subject | Multi-select | From Subject-Topic Master |
| Key Status | Multi-select | Not Uploaded · Uploaded · Published · Challenge Open · Finalized |
| Challenge Window | Toggle | Show only keys with an open challenge window |
| Date Range | Date range | Exam date From / To |

Active filter chips: dismissible, "Clear All" link, count badge on filter button.

### 4.3 Columns

| Column | Type | Sortable | Visible By | Notes |
|---|---|---|---|---|
| Exam Name | Text + link | ✅ | All | Links to Group Exam Calendar entry |
| Paper ID | Text | ✅ | All | PAP-2025-XXXX |
| Stream | Badge | ✅ | All | Stream |
| Subject | Text | ✅ | All | Subject(s) |
| Key Status | Badge | ✅ | All | Not Uploaded (grey) · Uploaded (blue) · Published (green) · Challenge Open (amber) · Finalized (dark green) |
| Published At | Date+time | ✅ | All | Timestamp of publication. "—" if not yet published |
| Challenge Window | Text | ✅ | All | "Open until [Date]" · "Closed" · "Not opened" |
| Challenges | Number | ✅ | CAO, Exam Controller | Count of student challenges received. Red if > 0 |
| Actions | — | ❌ | Role-based | See Row Actions |

**Default sort:** Key Status (Not Uploaded first, then Uploaded, then Challenge Open), then Exam date ascending.

**Pagination:** Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z papers" · Page jump input.

**Exam date lock enforcement:** Rows where the exam has not yet ended display a lock icon. Upload Key and Publish actions are disabled with tooltip "Key cannot be published until the exam ends ([Exam End Time])."

### 4.4 Row Actions

| Action | Icon | Visible To | Drawer/Modal | Notes |
|---|---|---|---|---|
| Upload Key | Upload | CAO, Exam Controller | `key-upload` drawer 480px | Available only after exam end time. Locked before. |
| Preview | Eye | All | `key-preview` modal 560px | View uploaded key — all questions + answers |
| Publish | Broadcast | CAO, Exam Controller | `publish-confirm` modal 420px | Publishes key to branches. Available only after exam end. |
| Open Challenge Window | Clock | CAO, Exam Controller | `challenge-window` modal 420px | Sets start and end date for challenge period |
| View Challenges | Flag | CAO, Exam Controller | `challenge-list` drawer 560px | Lists all challenges with status |
| Finalize | Lock | CAO only | `finalize-confirm` modal 420px | Closes challenge window permanently and locks key |

---

## 5. Drawers & Modals

### 5.1 Drawer: `key-upload` — Upload Answer Key
- **Trigger:** Upload Key row action
- **Width:** 480px
- **Enforcement:** Page checks current server time against exam end time. If exam not yet ended — drawer shows a countdown: "This exam ends in [Xh Ym]. Key upload will be enabled at [HH:MM]." Upload fields disabled.

| Field | Type | Required | Validation |
|---|---|---|---|
| Upload PDF Answer Key | File input | ❌ (optional, alongside Q-by-Q entry) | PDF only, max 10 MB |
| Question-by-Question Entry | Dynamic table | ✅ (at least one Q entry required) | |

**Q-by-Q Entry Table:**

| Column | Type | Required | Notes |
|---|---|---|---|
| Q# | Auto-filled | — | From paper structure |
| Question Type | Auto-filled | — | MCQ / Short / Long / Numerical |
| Correct Answer | Input | ✅ | MCQ: Radio A/B/C/D. Numerical: value + tolerance range (e.g. 9.8 ± 0.1). Short/Long: mark scheme text |
| Marks for Correct | Number | ✅ | Auto-filled from paper — editable |
| Negative Marks | Number | ❌ | Auto-filled from paper |
| Partial Credit Allowed | Toggle | ❌ | For Short/Long answers |
| Notes to Moderator | Text | ❌ | Explanation for non-obvious correct answer |

**Submit:** "Save Answer Key" — status → Uploaded. Key not published to branches until Publish action.

### 5.2 Drawer: `challenge-list` — Student Challenges
- **Trigger:** View Challenges row action
- **Width:** 560px
- **Tabs:** Open Challenges · Reviewed Challenges · All Challenges

#### Tab: Open Challenges
Table: Challenge ID · Q# · Student's Claim · Branch · Student Name (masked to roll no for junior roles) · Submitted At · Status.

Each row has [Review] button → opens `challenge-review` drawer 480px.

Filter within drawer: Branch filter · Q# filter.

#### Tab: Reviewed Challenges
Table: Challenge ID · Q# · Decision (Accepted / Rejected) · Reviewed By · Reviewed At · Original Answer · Final Answer.

#### Tab: All Challenges
Combined view with all statuses. Export to XLSX available from this tab.

### 5.3 Drawer: `challenge-review` — Review Single Challenge
- **Trigger:** Review button in challenge-list drawer
- **Width:** 480px

**Content:**
- Q# and full question text (KaTeX rendered if applicable)
- Official answer (current)
- Student's claimed correct answer
- Student's justification (if provided through branch portal)
- Branch name

| Field | Type | Required | Notes |
|---|---|---|---|
| Decision | Radio | ✅ | Accept · Reject · Accept with Modification |
| Reviewer Notes | Textarea | ✅ | Min 20 chars — explanation of decision |
| Revised Answer (if Accept/Modification) | Input | Conditional | New correct answer if accepted |

**Submit:** "Submit Decision" — challenge marked Reviewed. If Accepted: answer key for this Q# updated. Notification sent to branch. If all marks affected: Results Coordinator notified to re-run moderation for impacted branches.

**Note on mark recomputation:** Accepting a challenge that changes the correct answer does not auto-recompute all branch marks. Instead, it sets a flag on the moderation record for affected branches: "Answer key revised for Q#[N] — marks may need recomputation". Results Coordinator handles recomputation.

### 5.4 Drawer: key-preview — Preview Key
- **Trigger:** Preview row action
- **Width:** 560px (read-only)
- Rendered list: Q# · Question text (truncated, 50 chars + "..." hover) · Correct Answer · Marks · Notes. KaTeX rendered for mathematical answers.
- Download PDF button (if PDF was uploaded)

### 5.5 Modal: `challenge-window` — Set Challenge Window
- **Width:** 420px
- **Content:** "Open a challenge window for '[Exam Name]'? Students will be able to submit challenges through the branch portal."
- **Fields:** Challenge window start (date + time, default = now) · Challenge window end (date + time, default = now + 48 hours) · Maximum challenges per student (number, default 3) · Challenge fee (₹) (number, default ₹0 — set to ₹50–100 for JEE/NEET stream to prevent frivolous challenges)
- **Buttons:** [Open Challenge Window] (primary) + [Cancel]
- **On confirm:** Challenge window opens · Branch principals notified · Challenge submission form enabled in branch portal

### 5.6 Modal: `publish-confirm` — Publish Key
- **Width:** 420px
- **Content:** "Publish answer key for '[Exam Name]' to all branches? Branches and students will see this key immediately."
- **Enforcement:** Checks that current time is after exam end time. Shows warning if exam is still in progress.
- **Checklist:** All questions have answers entered · PDF uploaded (advisory) · Exam has ended
- **Buttons:** [Publish Answer Key] (primary green) + [Cancel]
- **On confirm:** Key status → Published · Branch principals and exam coordinators notified · Branch portal shows key for enrolled students

### 5.7 Modal: `finalize-confirm` — Finalize Key
- **Trigger:** Finalize row action (CAO only)
- **Width:** 420px
- **Content:** "Finalize answer key for '[Exam Name]'? The challenge window will close permanently and this key will be locked."
- **Warning:** "Finalization is irreversible. Ensure all challenges have been reviewed."
- **Stats shown:** Open challenges: [N] · Accepted challenges: [M] · Rejected: [P]
- **Block:** If Open Challenges > 0: shows "Cannot finalize — [N] challenges still open. Review all challenges before finalizing." Finalize button disabled.
- **Fields:** Confirmation (type exam name to confirm — text match required)
- **Buttons:** [Finalize Key] (danger, enabled only if no open challenges + name typed correctly) + [Cancel]
- **On confirm:** Key status → Finalized · Challenge window closed permanently · Result Moderation notified that this paper's key is locked · Audit entry created

---

## 6. Charts

No standalone charts section. The stats bar provides the operational summary. Challenge analytics (accepted vs rejected counts per subject) can be exported via the challenge-list drawer's XLSX export.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Key uploaded | "Answer key uploaded for '[Exam Name]'. Review before publishing." | Success | 4s |
| Key published | "Answer key published for '[Exam Name]'. Branches notified." | Success | 4s |
| Challenge window opened | "Challenge window open for '[Exam Name]' until [Date] [Time]." | Info | 4s |
| Challenge reviewed (accepted) | "Challenge for Q#[N] accepted. Answer key updated." | Warning | 6s |
| Challenge reviewed (rejected) | "Challenge for Q#[N] rejected." | Info | 4s |
| Key finalized | "Answer key for '[Exam Name]' finalized and locked." | Success | 4s |
| Finalize blocked | "Cannot finalize — [N] open challenges must be reviewed first." | Error | Manual |
| Upload blocked (exam not ended) | "Exam has not ended. Key can be uploaded after [End Time]." | Warning | Manual |
| Export started | "Export preparing… download will start shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No exam papers yet | "No exam papers found" | "Create exam papers in the Exam Paper Builder to generate answer key entries here." | [Go to Paper Builder] |
| All keys uploaded | "All keys uploaded" | "Answer keys have been uploaded for all completed exams." | — |
| No challenges submitted | "No challenges" | "No students have submitted challenges for this exam." | — |
| Filter returns empty | "No keys match your filters" | "Try removing some filters." | [Clear All Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 skeleton rows) |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| key-upload drawer open | Spinner + Q-by-Q table skeleton |
| Q-by-Q table populate (from paper) | Spinner while paper structure loads |
| challenge-list drawer open | Spinner + skeleton tabs |
| challenge-review drawer open | Spinner in drawer body |
| Key upload submit | Spinner in submit button |
| Key publish confirm | Spinner in publish button |
| Finalize confirm | Spinner in finalize button |
| Challenge decision submit | Spinner in submit button |
| Export trigger | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Exam Controller G3 | Stream Coords G3 | Academic Dir G3 | Results Coord G3 |
|---|---|---|---|---|---|
| Upload Key action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Preview action | ✅ | ✅ | ✅ (own stream) | ✅ | ✅ |
| Publish action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Open Challenge Window | ✅ | ✅ | ❌ | ❌ | ❌ |
| View Challenges action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Finalize action | ✅ | ❌ | ❌ | ❌ | ❌ |
| Challenge review drawer | ✅ | ✅ | ❌ | ❌ | ❌ |
| Challenges column | ✅ | ✅ | ❌ | ❌ | ❌ |
| Published At column | ✅ | ✅ | ✅ | ✅ | ✅ |
| Challenge Window column | ✅ | ✅ | ✅ (own stream) | ✅ | ✅ |
| Stream filter (all streams) | ✅ | ✅ | ❌ (own only) | ✅ | ✅ |
| [Export XLSX] button | ✅ | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/answer-keys/` | JWT | List answer key entries (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/answer-keys/{key_id}/` | JWT | Key detail + Q-by-Q answers |
| POST | `/api/v1/group/{group_id}/acad/answer-keys/{key_id}/upload/` | JWT (CAO/Exam Ctrl) | Upload answer key (PDF + Q-by-Q) |
| PUT | `/api/v1/group/{group_id}/acad/answer-keys/{key_id}/` | JWT (CAO/Exam Ctrl) | Update key (before publish) |
| POST | `/api/v1/group/{group_id}/acad/answer-keys/{key_id}/publish/` | JWT (CAO/Exam Ctrl) | Publish key to branches |
| POST | `/api/v1/group/{group_id}/acad/answer-keys/{key_id}/challenge-window/` | JWT (CAO/Exam Ctrl) | Open challenge window |
| GET | `/api/v1/group/{group_id}/acad/answer-keys/{key_id}/challenges/` | JWT (CAO/Exam Ctrl) | List all challenges for this key |
| GET | `/api/v1/group/{group_id}/acad/answer-keys/{key_id}/challenges/{ch_id}/` | JWT (CAO/Exam Ctrl) | Challenge detail |
| POST | `/api/v1/group/{group_id}/acad/answer-keys/{key_id}/challenges/{ch_id}/review/` | JWT (CAO/Exam Ctrl) | Submit challenge review decision |
| POST | `/api/v1/group/{group_id}/acad/answer-keys/{key_id}/finalize/` | JWT (CAO) | Finalize and lock key |
| GET | `/api/v1/group/{group_id}/acad/answer-keys/stats/` | JWT | Summary stats bar data |
| GET | `/api/v1/group/{group_id}/acad/answer-keys/export/` | JWT (CAO/Exam Ctrl) | XLSX export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Answer key search | `input delay:300ms` | GET `.../answer-keys/?q=` | `#keys-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../answer-keys/?filters=` | `#keys-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../answer-keys/?sort=&dir=` | `#keys-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../answer-keys/?page=` | `#keys-table-section` | `innerHTML` |
| Upload drawer open | `click` | GET `.../answer-keys/{id}/upload-form/` | `#drawer-body` | `innerHTML` |
| Challenge list drawer | `click` | GET `.../answer-keys/{id}/challenges/` | `#drawer-body` | `innerHTML` |
| Challenge review drawer | `click` | GET `.../answer-keys/{id}/challenges/{ch_id}/` | `#drawer-body` | `innerHTML` |
| Key upload submit | `submit` | POST `.../answer-keys/{id}/upload/` | `#drawer-body` | `innerHTML` |
| Publish confirm | `click` | POST `.../answer-keys/{id}/publish/` | `#key-row-{id}` | `outerHTML` |
| Finalize confirm | `click` | POST `.../answer-keys/{id}/finalize/` | `#key-row-{id}` | `outerHTML` |
| Challenge review submit | `submit` | POST `.../answer-keys/{id}/challenges/{ch_id}/review/` | `#challenge-row-{ch_id}` | `outerHTML` |
| Stats bar refresh | `load` | GET `.../answer-keys/stats/` | `#stats-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
