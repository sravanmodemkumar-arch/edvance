# J-06 — Playbook Hub

**Route:** `GET /csm/playbooks/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** CSM (#53), ISM (#94)
**Also sees:** Account Manager (#54) — start instances, read templates; CS Analyst (#93) — read-only; Escalation Manager (#55) — read-only; Renewal Executive (#56) — no access

---

## Purpose

Two-part hub: a template library where CSMs define and maintain standard playbooks for common CS scenarios (onboarding success, at-risk recovery, renewal prep), and an active instance tracker where the team monitors in-flight playbooks across all 2,050 institutions. Playbooks ensure consistency at scale — without them, different CSMs handle the same situation differently, producing unpredictable outcomes.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Template library | `csm_playbook_template` | 15 min |
| Active instances table | `csm_playbook_instance` JOIN `csm_playbook_template` JOIN `institution` WHERE status='ACTIVE' | 3 min |
| Instance KPI strip | `csm_playbook_instance` aggregated by status + trigger_type | 5 min |
| Overdue tasks | `csm_playbook_instance.task_states` parsed; tasks with due_days_offset passed and not completed | 3 min |
| Completed instances (recent) | `csm_playbook_instance` WHERE status='COMPLETED' AND completed_at ≥ now() - 30d | 10 min |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?section` | `templates`, `instances` | `instances` | Active section |
| `?trigger_type` | see enum | `all` | Filter templates or instances by trigger type |
| `?assigned_to` | user_id | `mine` (CSM/AM/ISM see own) | Filter instances by assignee |
| `?institution_type` | `school`, `college`, `coaching`, `group` | `all` | Filter instances by institution type |
| `?status` | `active`, `completed`, `abandoned` | `active` | Filter instances by status |
| `?template_id` | integer | — | Filter instances by template |
| `?overdue_only` | `1` | — | Show only instances with at least 1 overdue task |
| `?sort` | `next_task_due_asc`, `started_at_asc`, `progress_asc`, `institution_name` | `next_task_due_asc` | Instance sort |
| `?page` | integer | `1` | Instances pagination |
| `?template_active_only` | `1` | `1` | Filter templates to is_active=true only |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| Instance KPI strip | `?part=instance_kpis` | Page load + auto-refresh every 5 min |
| Template grid | `?part=template_grid` | Section = templates + filter change |
| Active instances table | `?part=instances_table` | Section = instances + filter change + sort + page |
| Overdue tasks panel | `?part=overdue_panel` | Page load + auto-refresh every 5 min |

---

## Page Layout

```
┌───────────────────────────────────────────────────────────────────┐
│  Playbook Hub                                                     │
│  [◼ Active Instances]  [☐ Template Library]                       │
├───────────────────────────────────────────────────────────────────┤
│  INSTANCE KPI STRIP (shown on Instances section)                  │
├───────────────────────────────────────────────────────────────────┤
│  INSTANCES: Filter row + table + pagination                       │
│  or                                                               │
│  TEMPLATES: Filter row + template grid                            │
├───────────────────────────────────────────────────────────────────┤
│  OVERDUE TASKS PANEL (instances section only)                     │
└───────────────────────────────────────────────────────────────────┘
```

---

## Section 1: Active Instances

### Instance KPI Strip (4 tiles)

```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ 38              │ │ 7               │ │ 12              │ │ 68%             │
│ Active          │ │ Overdue Tasks   │ │ Completed (30d) │ │ Avg Task        │
│ Playbooks       │ │                 │ │                 │ │ Completion Rate │
│                 │ │ [View →]        │ │                 │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
```

- **Active:** COUNT(status='ACTIVE')
- **Overdue Tasks:** Tasks where `started_at + due_days_offset days < today` and `task_states[].completed = false`; red if > 0
- **Completed (30d):** Instances completed in last 30 days
- **Avg Task Completion Rate:** (sum tasks_completed) / (sum tasks_total) × 100 across all ACTIVE instances

### Instances Filter Row

```
Trigger type: [All ▼]  Assigned: [Mine ▼]  Institution type: [All ▼]
Template: [All ▼]  Status: [Active ▼]  [Overdue only □]  [Clear]
Sort: [Next task due ▲]   Showing 38 active playbooks
```

### Instances Table

| Column | Description |
|---|---|
| Institution | Name (link → J-03 Playbooks tab) + type badge |
| Playbook | Template name + trigger type badge |
| Assigned To | Avatar + name |
| Progress | X/Y tasks · progress bar (green fill) |
| Status | ACTIVE (green) / COMPLETED (grey) / ABANDONED (red-struck) |
| Started | Date |
| Next Task | Title of next incomplete task + due date. Amber if due today, red if overdue |
| Health | Current health score + tier badge (from `csm_institution_health`) |
| Actions | [View Tasks] [Complete Task] [Abandon] |

**Pagination:** 25 rows per page. Page size fixed (no per-page selector). Pagination controls re-render with the `?part=instances_table` partial.

**Row click:** Expands inline accordion (same design as J-03 Playbooks tab) showing full task checklist.

**[Complete Task]:** Quick-complete the next overdue task. Opens inline confirmation: "Mark '[Task Title]' as completed?". POST to `/csm/playbooks/instances/{id}/tasks/{step}/complete/`. Returns HTMX swap of the row.

**[Abandon]:** Opens confirm dialog: "Abandon this playbook for [Institution]? This cannot be undone. The instance will be moved to Abandoned state and removed from the active list." POST to `/csm/playbooks/instances/{id}/abandon/`. Requires a short reason note.

### Task Detail Accordion (expanded inline)

```
  Step 1  ✓  Welcome call scheduled          Done 3 Mar · Ananya K.
  Step 2  ✓  Portal walkthrough session       Done 5 Mar · Ananya K.
  Step 3  ◻  Send exam setup guide            Due 25 Mar   [Mark Done]
  Step 4  ◻  First exam scheduled             Due 1 Apr    [Mark Done]
  Step 5  ◻  30-day check-in call             Due 10 Apr   [Mark Done]
  ...
```

For each incomplete task: [Mark Done] fires confirmation dialog → POST to complete endpoint → HTMX swap.

**Instance notes** shown below checklist (editable by assigned user and CSM). Save via [Save Note] → HTMX PATCH to `/csm/playbooks/instances/{id}/` with `{"notes": "..."}`. Returns updated row.

---

## Section 2: Template Library

Accessed by clicking [Template Library] tab.

### Template Filter Row

```
Trigger type: [All ▼]  Segment: [All ▼]  [Active only □ ✓]
[+ Create Template]  (CSM #53 only)
```

### Template Grid

Cards in a responsive 3-column grid (single column on mobile):

```
┌──────────────────────────────────────────┐
│  AT_RISK_RECOVERY                 ACTIVE │
│  "At-Risk Account Recovery"              │
│  Trigger: AT_RISK_RECOVERY               │
│  Segment: ALL                            │
│  10 tasks · ~30 days                     │
│  Active instances: 14                    │
│                                          │
│  [View Tasks ▼]   [Edit]   [Deactivate]  │
└──────────────────────────────────────────┘
```

Trigger type badges: ONBOARDING_SUCCESS=green, AT_RISK_RECOVERY=orange, RENEWAL_PREP=blue, EXPANSION=teal, EBR=violet, CHURN_SAVE=red, CUSTOM=grey.

[View Tasks ▼] expands an inline accordion listing all tasks:
```
  Step 1 (Day 1)   [CALL required]     Urgent check-in call with institution admin
  Step 2 (Day 2)   [INTERNAL_NOTE]     Root cause note in account profile
  Step 3 (Day 3)   [CALL required]     Health score review + action plan with AM
  Step 4 (Day 7)   [EMAIL required]    Send recovery plan PDF to institution
  ...
```

[Edit] opens Template Edit Drawer (CSM only).
[Deactivate] — shows confirm: "Deactivating this template prevents new instances. Existing instances continue." POST sets `is_active=false`. Shows "INACTIVE" badge on card; CSM can reactivate.

**Empty template grid:** "No templates found. Create your first playbook template." with [+ Create Template] button.

---

## Create / Edit Template Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  Create Playbook Template                                        │
├──────────────────────────────────────────────────────────────────┤
│  Template name*     [________________________________]           │
│  Description        [Free-text; markdown OK          ]          │
│  Trigger type*      [AT_RISK_RECOVERY              ▼]           │
│  Target segment*    [ALL                           ▼]           │
│  Est. duration (d)* [30]                                        │
│                                                                  │
│  TASKS                                    [+ Add Task]          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Step 1  ≡  Due day: [1  ]  Required: [✓]               │   │
│  │ Title*: [Urgent check-in call with institution admin    ] │   │
│  │ Desc:   [Call the primary contact to understand root... ] │   │
│  │ Owner:  [CSM                                          ▼] │   │
│  │ Type:   [CALL                                         ▼] │   │
│  │                                               [Remove]   │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ Step 2  ≡  Due day: [2  ]  Required: [✓]               │   │
│  │ Title*: [Root cause note in account profile            ]  │   │
│  │ ...                                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│  (Tasks reorderable via drag handle ≡)                          │
│                                                                  │
│  [Cancel]                        [Save Template]                │
└──────────────────────────────────────────────────────────────────┘
```

**Task fields per step:**
- Step number (auto-assigned, reorders on drag)
- Due day (days from instance start_at; integer ≥ 0)
- Required (boolean; required tasks block instance completion if not done)
- Title (required; max 200 chars)
- Description (optional; max 1,000 chars; markdown)
- Owner role (CSM, AM, ISM, Escalation Manager, Renewal Executive)
- Touchpoint type hint (CALL, EMAIL, EBR, INTERNAL_NOTE, etc.)

**Validation:**
- Name: required; min 5 chars; max 200 chars
- Trigger type: required
- At least 1 task required
- All tasks must have unique step numbers (auto-managed)
- Due day: non-negative integer
- Estimated duration: must be ≥ max(due_days_offset) across all tasks

POST/PATCH to `/csm/playbooks/templates/`. Returns 201/200 and HTMX swap of template grid.

**Editing active template:** Shows warning "This template has 14 active instances. Changes to task descriptions and due dates will apply only to new instances." Task deletions from active template require confirmation.

---

## Start Playbook (from Instances section)

[+ Start Playbook] button — top right of instances section.

```
┌──────────────────────────────────────────────────────────────────┐
│  Start Playbook                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Institution*   [Search institution...                    ]      │
│  Template*      [AT_RISK_RECOVERY — At-Risk Account Recovery ▼]  │
│  Assign to*     [Ananya K. (CSM)                          ▼]     │
│  Instance notes [Optional notes for this instance          ]     │
│                                                                  │
│  PREVIEW:  10 tasks  ·  ~30 days                                 │
│  Step 1 (Day 1):   Urgent check-in call                          │
│  Step 2 (Day 2):   Root cause note                               │
│  Step 3 (Day 3):   Health score review with AM                   │
│  [+ 7 more tasks]                                                │
│                                                                  │
│  ⚠  Delhi Public School already has 1 active instance of this    │
│     template. Start another?  ○ Yes  ● No (recommended)          │
│                                                                  │
│  [Cancel]                      [Start Playbook]                  │
└──────────────────────────────────────────────────────────────────┘
```

Guard: warns if institution already has active instance of same template. Does not block — CSM can override.

POST to `/csm/accounts/{institution_id}/playbooks/start/`. Returns 201 and re-renders instances table.

---

## Overdue Tasks Panel

Sticky panel at the bottom of the Instances section (collapsed by default; auto-expands if any overdue tasks exist).

```
┌──────────────────────────────────────────────────────────────────────┐
│  7 Overdue Tasks  [Expand ▼]                                         │
│                                                                      │
│  Delhi Public School   AT_RISK_RECOVERY  Step 3: H-score review      │
│  Due: 18 Mar (3 days overdue)    Assigned: Ananya K.   [Mark Done]  │
│                                                                      │
│  Sunrise College       RENEWAL_PREP      Step 2: Send quote          │
│  Due: 20 Mar (1 day overdue)     Assigned: Ravi S.     [Mark Done]  │
│  ...                                                                 │
└──────────────────────────────────────────────────────────────────────┘
```

[Mark Done] inline — same POST as task completion. HTMX swap removes the row from panel.

Auto-refresh every 5 min. If 0 overdue: "No overdue tasks." with green check icon. Panel remains collapsed.

---

## Empty States

| Condition | Message |
|---|---|
| No active playbook instances | "No active playbooks. Start a playbook from an account's profile or use the Start Playbook button." |
| Filter returns no instances | "No playbooks match the current filters." with [Clear Filters] |
| No templates | "No templates created yet. Create your first playbook template to standardise CS workflows." with [+ Create Template] |
| No overdue tasks | "No overdue tasks — team is on track." |

---

## Toast Messages

| Action | Toast |
|---|---|
| Template created | "Playbook template created." (green) |
| Template updated | "Template updated. Changes will apply to new instances only." (blue) |
| Template deactivated | "Template deactivated. Existing instances are unaffected." (amber) |
| Instance started | "Playbook started for [Institution]." (green) |
| Task marked complete | "Task marked as complete." (green) |
| All tasks done → auto-complete | "Playbook completed for [Institution]! " (green) |
| Instance abandoned | "Playbook abandoned." (grey) |

---

## Role-Based UI Visibility Summary

| Element | 53 CSM | 54 AM | 55 Escalation | 56 Renewal | 93 Analyst | 94 ISM |
|---|---|---|---|---|---|---|
| View instances | All | Own | Read | No access | Read | Own |
| Start playbook | Yes | No | No | No | No | Yes (own accounts, within 90-day tenure) |
| Complete task | Yes + team | No | No | No | No | Yes (assigned, within 90-day tenure) |
| Abandon instance | Yes | No | No | No | No | No |
| View templates | Yes | Yes | Yes | No | Yes | Yes |
| Create template | Yes | No | No | No | No | No |
| Edit template | Yes | No | No | No | No | No |
| Deactivate template | Yes | No | No | No | No | No |
| Overdue panel | Yes | Own | No | No | Read | Own |
| Instance KPI strip | Yes | Yes | Yes | No | Yes | Yes |

**ISM post-tenure note:** After `ism_tenure_end_date` passes (day 90), ISM (#94) access to playbook actions becomes read-only for the graduated account. Active playbook instances are transferred to the AM by Task J-6 (see div-j-pages-list Celery Tasks). The ISM's view of the instances page is filtered to `assigned_to_id = current_user`, so transferred instances (reassigned to AM) no longer appear in their Instances tab — only read-only via direct account profile navigation. ISM cannot start new playbooks or complete tasks on accounts outside their current active tenure.
