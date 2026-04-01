# H-03 — Syllabus & Topic Tree Admin

> **URL:** `/admin/exam/{slug}/syllabus/`
> **File:** `h-03-syllabus-admin.md`
> **Priority:** P1
> **Data:** `syllabus_node` table — tree CRUD; changes affect mock tagging, study material mapping, progress tracking

---

## 1. Syllabus Tree Editor

```
SYLLABUS TREE EDITOR — APPSC Group 2 2025
Admin | Stage: [Prelims ▼]

  TREE (drag to reorder, click to edit):
  ┌──────────────────────────────────────────────────────────────────────┐
  │  ▼ Indian History  [Weight: 12%]  [Tags: indian-history]  [✏️][🗑️] │
  │    ├── Ancient India   [Weight: 4%] [✏️][🗑️]                       │
  │    ├── Medieval India  [Weight: 3%] [✏️][🗑️]                       │
  │    └── Modern India    [Weight: 5%] [✏️][🗑️]                       │
  │  ▼ AP & TS History [Weight: 8%] [Tags: ap-ts-history]    [✏️][🗑️] │
  │    ├── Satavahana, Kakatiya dynasties  [✏️][🗑️]                    │
  │    ├── Telangana Movement              [✏️][🗑️]                    │
  │    └── [+ Add child node]                                           │
  │  ▼ Indian Polity   [Weight: 10%] [Tags: indian-polity]   [✏️][🗑️] │
  │    ├── Constitution — FR, DPSP, Duties [✏️][🗑️]                    │
  │    ├── Parliament, State Legislature   [✏️][🗑️]                    │
  │    └── Panchayati Raj, Municipalities  [✏️][🗑️]                    │
  │  [+ Add root node]                                                   │
  └──────────────────────────────────────────────────────────────────────┘

  NODE EDIT FORM:
    Name (English):     [ Constitutional Amendments              ]
    Name (Telugu):      [ రాజ్యాంగ సవరణలు                         ]
    Parent:             [ Indian Polity ▼ ]
    Weightage (%):      [ 3 ]
    Avg questions:      [ 4 ] (from historical PYQ analysis)
    Difficulty:         [ Medium ▼ ]
    Tags (cross-exam):  [ indian-polity, constitutional-amendments ]
    [Save]  [Cancel]
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/admin/exam/{slug}/syllabus/?stage=prelims` | Full tree for admin |
| 2 | `POST` | `/api/v1/admin/exam/{slug}/syllabus/` | Add node |
| 3 | `PUT` | `/api/v1/admin/exam/{slug}/syllabus/{nid}/` | Update node |
| 4 | `DELETE` | `/api/v1/admin/exam/{slug}/syllabus/{nid}/` | Delete node (with child impact check) |
| 5 | `PATCH` | `/api/v1/admin/exam/{slug}/syllabus/reorder/` | Reorder nodes (drag-drop) |

---

## 5. Business Rules

- Deleting a syllabus node that has content mapped to it (questions tagged, study material linked, user progress tracked) requires confirmation and triggers a cascade: the admin is shown "This node has 184 questions, 4 study materials, and 2,840 user progress records. Deleting it will orphan these records."; the system offers: (a) reassign to another node (move questions to the parent node); (b) force delete (questions become un-tagged — usable but not discoverable by topic); soft-delete is preferred (node becomes inactive but data is preserved)
- Cross-exam tags on syllabus nodes (e.g., `indian-polity` appearing in both APPSC and SSC syllabi) are the mechanism that enables content sharing; the admin sets these tags deliberately — two nodes in different exams with the same tag are treated as "overlapping topics" by the question bank and study material system; a typo in the tag (`indian-polity` vs `indian_polity`) breaks the cross-exam linkage; the system suggests existing tags as the admin types (autocomplete) to prevent tag fragmentation
- Weightage percentages must sum to approximately 100% for a stage; the system validates: `SUM(weightage) for root nodes WHERE stage = 'prelims'` should be between 95% and 105% (allowing rounding); a syllabus where weightages sum to 60% means 40% of the exam content is unmapped — questions and material for those topics cannot be properly tagged; the admin is warned if the sum is below 90%
- Syllabus trees for exams with pattern changes across cycles (APPSC Group 2 2022 vs 2025 had different subject distributions) are versioned; the admin creates a new tree for the current cycle while preserving the previous cycle's tree (linked to historical mocks and PYQs); a student practicing PYQ 2022 should see it tagged against the 2022 syllabus; a student taking a 2025-pattern mock should see it tagged against the 2025 syllabus

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division H*
