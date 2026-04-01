# 10 — Syllabus Builder

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total questions in bank | 2M+ |
| Exam domains | 8 (SSC · RRB · NEET · JEE · AP Board · TS Board · IBPS · SBI) |
| Subjects per domain | 4–12 subjects |
| Chapters per subject | 5–40 chapters |
| Topics per chapter | 3–20 topics |
| Total syllabus nodes (approx) | ~12,000–18,000 topic nodes across all domains |
| Coverage % target | 95%+ of all topics must have ≥ 10 questions |
| Topics with 0 questions (gap) | Must be flagged and surfaced |

**Why this page matters at scale:** The syllabus hierarchy is the backbone of the entire question bank. Every question in the 2M+ bank is tagged to a topic. If a topic doesn't exist in the syllabus, questions can't be tagged, test series can't cover it, and students miss critical content areas. PM Exam Domains builds and maintains this tree. A subject renamed here flows through to question bank tagging, test series coverage reports, and student analytics — making correctness critical.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Syllabus Builder |
| Route | `/product/syllabus/` |
| Django view class | `SyllabusBuilderView` |
| Template | `product/syllabus_builder.html` |
| Permission — view | `portal.view_syllabus` (all div-b roles) |
| Permission — manage | `portal.manage_syllabus` (PM Exam Domains only) |
| 2FA required | No (syllabus changes do not affect live exam scoring) |
| HTMX poll | None |
| Nav group | Product |
| Nav icon | `tree` |
| Priority | P1 |

---

## 3. Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Syllabus Builder          [+ Add Node]  [Import]  [Export]  [Coverage ▾]  │
├────────────────────────────────────────────────────────────────────────────────────┤
│ Domain selector: [SSC ▾]   Exam type: [SSC CGL Tier 1 ▾]   [Version: v4 ▾]       │
├──────────────────────────────────┬─────────────────────────────────────────────────┤
│ TREE PANEL (left 380px)          │ NODE DETAIL PANEL (right — remainder)          │
│                                  │                                                 │
│ 🔍 [Search topics...]            │ [Node selected: Quantitative Aptitude]          │
│                                  │                                                 │
│ ▼ Quantitative Aptitude      87% │ Questions: 85,420                              │
│   ▼ Number System            94% │ Sub-nodes: 8 chapters                          │
│     ● LCM and HCF            92% │ Coverage: 87%                                  │
│     ● Simplification         98% │ Mapped exam types: CGL T1, CHSL, CPO, MTS     │
│     ● Square Roots           88% │                                                 │
│     ● Indices & Surds        67% │ [Edit] [Add Chapter] [Move] [Delete]           │
│   ▼ Percentage              100% │                                                 │
│     ● Basic Percentage       100% │ ──────────────────────────────────────────── │
│     ● Profit & Loss          99% │ COVERAGE CHART (bar chart)                     │
│   ▶ Ratio & Proportion       82% │ Shows Q count vs target per chapter            │
│   ▶ Average                  91% │                                                 │
│   ▶ Time & Work              88% │                                                 │
│ ▶ General Intelligence       79% │                                                 │
│ ▶ English Language           91% │                                                 │
│ ▶ General Awareness          84% │                                                 │
└──────────────────────────────────┴─────────────────────────────────────────────────┘
```

---

## 4. Layout: Two-Panel Design

### 4.1 Left Panel — Syllabus Tree

**Width:** 380px · `bg-[#0D1526] border-r border-[#1E2D4A] h-full overflow-y-auto`

#### Domain + Exam Type Selectors (sticky header)

```
[SSC ▾]  ›  [SSC CGL Tier 1 ▾]  ›  [Version: v4 ▾]
```

**Domain dropdown:** `select.bg-[#131F38] border border-[#1E2D4A] text-[#F1F5F9] text-sm rounded`
**Exam type dropdown:** updates when domain changes · `hx-get="?part=exam_types&domain={id}" hx-swap="innerHTML" hx-target="#exam-type-select"`
**Version dropdown:** shows syllabus versions with dates · "v4 (current)" · "v3 (Feb 2026)"

#### Search

`input.bg-[#131F38] border border-[#1E2D4A] rounded px-3 py-2 text-sm w-full placeholder:text-[#475569]`
`placeholder="Search topics, chapters, subjects..."`
debounce 300ms · `hx-get="?part=tree_search&q={value}" hx-target="#tree-container" hx-swap="innerHTML"`
Clears to full tree on empty

#### Tree Container

`id="tree-container"` · `space-y-0`

**Level 1 — Subject node:**
```
▼ Subject Name          [coverage %]   [Q count]
```
`flex items-center gap-2 px-3 py-2 cursor-pointer hover:bg-[#131F38] group`
Chevron: `▼` expanded · `▶` collapsed · click toggles
Coverage %: `text-xs` colour:
- 90–100%: `text-[#34D399]`
- 75–89%: `text-[#FCD34D]`
- 50–74%: `text-[#F59E0B]`
- < 50%: `text-[#F87171]`

**Level 2 — Chapter node (indent 16px):**
```
  ▼ Chapter Name        [coverage %]   [Q count]
```
Same colour coding.

**Level 3 — Topic node (indent 32px):**
```
    ● Topic Name        [coverage %]   [Q count]
```
Bullet dot (`●`) instead of chevron — no children.
Topic dot colour = same coverage colour scale.

**Selected node:** `bg-[#131F38] border-l-2 border-[#6366F1]`

**Node context menu (right-click or hover → 3-dot icon):**
- Add Child
- Edit
- Move (drag handle appears)
- Duplicate Subtree
- Delete (only if Q count = 0)
- View Questions → opens question bank filtered to this topic

---

### 4.2 Right Panel — Node Detail

`flex-1 bg-[#070C18] p-6 overflow-y-auto`

#### Node Header

```
[Node level badge: Subject / Chapter / Topic]  [Node name]  [Edit button ✎]
[Exam domain badge]  [Last updated: X days ago by Name]
```

#### Node Summary Cards

`grid grid-cols-4 gap-3 mb-6`

| Card | Value |
|---|---|
| Questions | `85,420` |
| Sub-nodes (if subject/chapter) | `8 chapters` or `24 topics` |
| Coverage | `87%` with mini gauge |
| Mapped Exam Types | Count badge → expandable list |

#### Coverage Chart (for Subject/Chapter level)

**Canvas id:** `coverage-chart` · height 200px · Chart.js horizontal bar
X-axis: Question count
Y-axis: Chapter or Topic names

**Series:**
- Actual questions: `#6366F1`
- Target questions (minimum recommended): `#1E2D4A` (grey background)

**Target line:** dashed vertical line at recommended minimum per topic (typically 10 questions)

Hover tooltip: topic name · actual Q · target Q · gap if under-covered

#### Chapter/Topic List (for Subject node selected)

Table of immediate children:

| # | Name | Level | Q Count | Coverage | Target | Gap | Actions |
|---|---|---|---|---|---|---|---|
| 1 | Number System | Chapter | 8,420 | 94% | 8,000 | — | Edit · Expand |
| 2 | Percentage | Chapter | 12,300 | 100% | 10,000 | — | Edit · Expand |
| 3 | Time & Work | Chapter | 4,200 | 62% | 6,000 | -1,800 | Edit · Expand |

Gap column: red when actual < target · `text-[#F87171]` "-1,800 Q needed"

**[View All Questions]** link: `text-[#6366F1] text-sm` → question bank (page 22 in div-a) filtered to this node

#### Mapped Exam Types Panel

`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4`
"This topic/chapter is included in:"

| Exam Type | Section | Weight |
|---|---|---|
| SSC CGL Tier 1 | Quantitative Aptitude | ~25% of section |
| SSC CHSL Tier 1 | Quantitative Aptitude | ~25% of section |
| SSC CPO | Quantitative Aptitude | ~25% of section |

[+ Map to Exam Type] button → modal to select exam types

#### Action Buttons

`flex gap-3 mt-6`
- [Edit Node] `bg-[#131F38] border border-[#1E2D4A]`
- [Add Child Chapter] / [Add Child Topic] `bg-[#6366F1]`
- [Move Node] `bg-[#131F38]` → drag-and-drop mode activates
- [Duplicate Subtree] `bg-[#131F38]`
- [Delete Node] `text-[#F87171]` (only if Q count = 0)

---

## 5. Coverage Dashboard Modal

**Trigger:** [Coverage ▾] header button → [View Coverage Dashboard]
**Width:** 80vw · `max-w-[1000px]`

### 5.1 Domain-Level Coverage Summary

`grid grid-cols-4 gap-4 mb-6`

| Domain | Subjects | Topics | Coverage | Gaps (< target) |
|---|---|---|---|---|
| SSC | 5 | 248 | 87% | 28 topics |
| RRB | 6 | 192 | 83% | 34 topics |
| NEET | 3 | 180 | 91% | 16 topics |
| JEE | 4 | 220 | 78% | 48 topics |

### 5.2 Gap Report Table

"Topics with fewer than target questions:"

| Domain | Subject | Chapter | Topic | Q Count | Target | Gap | Assigned SME |
|---|---|---|---|---|---|---|---|
| JEE | Chemistry | Organic | Grignard Reactions | 3 | 15 | -12 | Unassigned |
| SSC | QA | Time & Work | Pipes & Cisterns | 6 | 10 | -4 | SME Ravi |

**[Assign SME]** per row → links to Content Director (Division D) workflow
**[Export Gap Report CSV]**

---

## 6. Inline Node Edit

**Trigger:** [Edit Node] button in right panel or double-click node in tree

Inline edit form appears in right panel (replaces detail view):

| Field | Type |
|---|---|
| Node Name | Text · required · max 120 chars |
| Display Name (institution-facing) | Text · if different from internal name |
| Code / Slug | Text · font-mono · auto-generated · editable |
| Description | Textarea |
| Target Q count (minimum) | Number |
| Tags | Multi-select (e.g., "high-weightage", "frequently-asked", "PYQS") |
| Status | Active / Disabled / Draft |

**[Save]** · **[Cancel]**

Name change propagates to question bank tags — confirmation required if > 1,000 questions tagged.

---

## 7. Add Node Modal

**Trigger:** [+ Add Node] header button or context menu → Add Child
**Width:** 480px

| Field | Type |
|---|---|
| Node Type | Select: Subject / Chapter / Topic |
| Parent | Auto-selected if triggered from context menu, else dropdown |
| Name | Text · required |
| Code | Text · auto-generated from name |
| Target Q count | Number |
| Copy structure from | Select existing node (optional — copies children without Q mappings) |

---

## 8. Move Node (Drag-and-Drop)

**Trigger:** [Move Node] button or drag handle (6-dot icon on hover)
**Mode:** Drag-and-drop within same tree · target node highlighted on hover

Rules:
- Subject can only be moved within same domain (cannot move to different domain)
- Chapter can be moved between subjects within same domain
- Topic can be moved between chapters within same subject

**Cross-domain move:** not supported via drag. Use Duplicate → then Delete original.

Moved node: `hx-post="?action=move_node"` `hx-vals='{"node_id": X, "new_parent_id": Y, "new_order": N}'`

---

## 9. Import / Export

### 9.1 Import

**Trigger:** [Import] header button
**Width:** 560px

**Drop zone:**
`border-2 border-dashed border-[#1E2D4A] rounded-xl p-8 text-center hover:border-[#6366F1]`
"Drag and drop a CSV or JSON syllabus file here"

**Supported format (CSV):**
```
level,parent_code,code,name,target_q
subject,,QA,Quantitative Aptitude,5000
chapter,QA,QA_NS,Number System,800
topic,QA_NS,QA_NS_LCM,LCM and HCF,50
```

**Preview table** after upload:
| Action | Code | Name | Level | Parent |
- New nodes: `text-[#34D399]` "Will create"
- Existing (no change): `text-[#94A3B8]` "No change"
- Conflicts: `text-[#F87171]` "Code conflict — will skip"

**Import options:**
- `[○] Merge with existing` (default)
- `[○] Replace entire syllabus` (destructive — requires 2FA)

**Footer:** [Import] · [Cancel]

### 9.2 Export

Export to: JSON (full tree) · CSV (flat list) · PDF (formatted for review)

---

## 10. Version History

**Trigger:** [Version ▾] selector → [View Version History]

Each version: version number · date · created by · node count · changes summary

**Version comparison:** Select 2 versions → side-by-side diff
- Added nodes: `text-[#34D399]` with `+` prefix
- Removed nodes: `text-[#F87171]` with `−` prefix
- Renamed nodes: `text-[#FCD34D]` with `~` prefix

**[Restore Version]** button — reverts entire syllabus to selected version (confirmation required)

---

## 11. Django View

```python
class SyllabusBuilderView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_syllabus"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "tree":           "product/partials/syllabus_tree.html",
                "node_detail":    "product/partials/syllabus_node_detail.html",
                "tree_search":    "product/partials/syllabus_search.html",
                "exam_types":     "product/partials/syllabus_exam_types.html",
                "coverage_chart": "product/partials/syllabus_coverage.html",
                "gap_report":     "product/partials/syllabus_gaps.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/syllabus_builder.html", ctx)

    def post(self, request):
        if not request.user.has_perm("portal.manage_syllabus"):
            return JsonResponse({"error": "Permission denied"}, status=403)
        action = request.POST.get("action")
        dispatch = {
            "create_node":    self._create_node,
            "update_node":    self._update_node,
            "move_node":      self._move_node,
            "delete_node":    self._delete_node,
            "duplicate_tree": self._duplicate_tree,
            "import_syllabus":self._import_syllabus,
            "restore_version":self._restore_version,
        }
        handler = dispatch.get(action)
        if handler:
            return handler(request)
        return JsonResponse({"error": "Unknown action"}, status=400)
```

---

## 12. Data Model Reference

```python
class SyllabusNode(models.Model):
    NODE_TYPES = [
        ("subject", "Subject"),
        ("chapter", "Chapter"),
        ("topic",   "Topic"),
    ]
    domain       = models.ForeignKey("ExamDomain", on_delete=models.CASCADE)
    parent       = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="children")
    node_type    = models.CharField(max_length=10, choices=NODE_TYPES)
    code         = models.SlugField(max_length=60, unique=True, db_index=True)
    name         = models.CharField(max_length=120, db_index=True)
    display_name = models.CharField(max_length=120, blank=True)
    description  = models.TextField(blank=True)
    target_q     = models.PositiveIntegerField(default=10)
    order        = models.PositiveSmallIntegerField(default=0)
    status       = models.CharField(max_length=20, default="active")
    version      = models.PositiveSmallIntegerField(default=1)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    updated_by   = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["order", "name"]
        indexes = [
            models.Index(fields=["domain", "node_type"]),
            models.Index(fields=["parent", "order"]),
        ]

    @property
    def question_count(self):
        # Cached via Redis — expensive if live-computed for 2M Q bank
        from django.core.cache import cache
        return cache.get_or_set(
            f"syllabus:node:{self.id}:q_count",
            lambda: Question.objects.filter(topic_code=self.code).count(),
            300  # 5 min cache
        )

    @property
    def coverage_pct(self):
        q = self.question_count
        return min(100, round(q / self.target_q * 100)) if self.target_q > 0 else 0
```

---

## 13. Empty States

| Context | Copy |
|---|---|
| No syllabus for domain | "No syllabus configured for this domain. Import a syllabus or add subjects manually." |
| Search returns no results | "No topics found matching '{query}'. Try a different term." |
| Node has 0 questions | Topic dot shown in red `text-[#F87171]` with "0 questions — content gap" tooltip |
| No version history | "This is the first version of this syllabus." |

---

## 14. Bulk Operations

**Trigger:** Select multiple nodes in the tree (Ctrl+click or Shift+click) → bulk action toolbar appears at top of right panel.

**Supported bulk operations:**

| Action | Conditions | Behaviour |
|---|---|---|
| Bulk Retag | Select multiple topics | Opens modal: choose new tags to add/remove across all selected topics |
| Bulk Set Target Q | Select multiple nodes | Set a new target question count for all selected nodes at once |
| Bulk Move | Select multiple topics/chapters | Opens parent picker modal — moves all selected to chosen parent (same domain only) |
| Bulk Status Change | Select multiple nodes | Set Active / Disabled / Draft for all selected |
| Bulk Export | Any selection | Exports selected subtrees to CSV/JSON |
| Bulk Map to Exam Type | Select multiple topics | Maps all selected topics to a chosen exam type in one action |

**Selection indicator:** `"3 nodes selected"` badge in right panel header · [Clear Selection ×]

**Bulk move validation:** System checks all selected nodes are compatible with destination parent (e.g., cannot move a Subject into another Subject). Incompatible nodes shown in a validation summary before confirming.

---

## 15. Syllabus Review Workflow

**Purpose:** Syllabus changes (new topics, renames, restructuring) have downstream impact on question bank tagging, test series coverage, and student-facing content. Major changes must be reviewed before being marked active.

**Who triggers review:** PM Exam Domains (manages) submits syllabus version for review.
**Who reviews:** Senior PM Exam Domains or Head of Content (defined in Division A).

**Review flow:**
1. PM Exam Domains makes changes → syllabus is in "Draft (changes pending)" state
2. PM clicks [Submit for Review] → status changes to "Under Review"
3. Reviewer is notified (email + in-app alert)
4. Reviewer opens Syllabus Builder → sees a diff view (current vs previous version) showing all additions, removals, renames
5. Reviewer can [Approve] → syllabus becomes Active version, question bank re-tagging job queued in Celery
6. Reviewer can [Request Changes] → comment required, status returns to "Draft"

**Impact assessment shown to reviewer:**
- New nodes: "3 new topics — these will appear in coverage gap report but have 0 questions"
- Renamed nodes: "2 topics renamed — 8,420 question tags will be migrated automatically"
- Deleted nodes: "1 topic deleted — 340 questions will become untagged (action required)"

**2FA not required for syllabus changes** (low blast radius — question bank re-tagging is reversible via version restore).

---

## 16. Notification Rules

| Event | Recipients | Channel | Trigger |
|---|---|---|---|
| Coverage drops below 75% for a topic | PM Exam Domains owner of that domain | Email + in-app | Nightly coverage recompute |
| New content gap (topic with 0 questions) appears | PM Exam Domains | In-app badge on Coverage Dashboard | Question deleted/moved |
| Syllabus review submitted | Reviewer (Senior PM / Head of Content) | Email | Submit for review action |
| Syllabus review approved | PM Exam Domains (submitter) | Email | Approval action |
| Syllabus review changes requested | PM Exam Domains (submitter) | Email | Request changes action |
| Question re-tagging Celery job completes | PM Exam Domains | In-app toast | Celery task `syllabus_retag_complete` |
| Bulk move affects > 1,000 questions | PM Exam Domains | Email confirmation required before proceeding | Move confirmation |

---

## 17. Integration Points

| Page | Direction | What flows |
|---|---|---|
| 27 — Question Bank Manager | Both | Questions are tagged to syllabus nodes; coverage % shown in this page is derived from question count per node in page 27 |
| 12 — Exam Pattern Builder | Inbound | Exam sections reference syllabus subjects; pattern builder uses the subject list from this page |
| 13 — Domain Analytics | Outbound | Syllabus coverage metrics (% topics covered, gap count) appear in domain analytics dashboard |
| 09 — Exam Domain Config | Inbound | Domain config controls which syllabus versions are active per domain |
| 10 (self) | Self | Version history and comparison is internal to this page; restore version creates a new version entry |

---

## 18. Key Design Decisions

| Decision | Chosen approach | Why |
|---|---|---|
| 3-level hierarchy (Subject → Chapter → Topic) | Fixed 3 levels, not arbitrary depth | Arbitrary depth trees become unmanageable at 12,000–18,000 nodes; 3 levels maps naturally to how exams are structured (section → unit → concept) |
| Coverage % cached 5 minutes (Redis) | Not real-time | Computing coverage for 2M+ questions across 18,000 nodes in real-time would require sequential DB scans; 5-minute staleness is acceptable for PM planning |
| Delete only allowed when Q count = 0 | Hard rule — no override | Deleting a topic with tagged questions orphans them in the question bank; orphaned questions disappear from coverage and test series — undetectable until exam content fails |
| Name change triggers re-tagging confirmation if > 1,000 questions | Threshold-based confirmation | Below 1,000: quick operation. Above 1,000: takes 15–30 min in Celery; PM needs to be aware before clicking Save |
| Cross-domain move not supported via drag | Duplicate → Delete only | A chapter in SSC Quantitative Aptitude and a chapter in RRB Quantitative Aptitude are different entities even if same name; moving implies the same content applies to both domains which requires explicit review |
| Version restore creates a new version (not rollback-in-place) | Append-only version history | Rollback-in-place would destroy the history of the rolled-back version; creating a new "restored from v3" version preserves the full audit trail |

---

## 19. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `↑ ↓` | Navigate tree nodes |
| `→` | Expand selected node |
| `←` | Collapse selected node |
| `N` | Add child node to selected |
| `E` | Edit selected node |
| `Del` | Delete selected node (if Q count = 0) |
| `/` | Focus search |
| `Esc` | Clear search / close modal |
| `Ctrl+Z` | Undo last node move/create/rename |
