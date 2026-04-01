# O-08 — Learning & Development

**Route:** `GET /hr/learning/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** L&D Coordinator (#107)
**Also sees:** HR Manager (#79) — full access + budget approval authority; HR Business Partner (#106) — read-only analytics + skills matrix + training needs; all employees — self-serve enrollment view via `/hr/my-learning/` (not covered in this spec)

---

## Purpose

Structured learning and development programme for all 100–150 EduForge employees. The L&D Coordinator uses this page to run the annual training calendar, manage the course library (internal + external + LMS), track mandatory compliance training completion (POSH, Data Privacy, POCSO awareness for roles with child data access), maintain the skills matrix, and track professional certifications. At EduForge's scale, L&D is not just a perk — POSH awareness training and data privacy training are legal compliance obligations, and the skills gap between current team capabilities and product roadmap requirements needs continuous tracking.

Key obligations:
- **POSH Act 2013:** POSH awareness training mandatory for all employees annually (Section 4 requires ICC formation; awareness is a standard obligation)
- **DPDP Act 2023:** Data privacy awareness for all roles handling personal data of students/institutions
- **POCSO awareness:** Mandatory for roles in Divisions D, G, I that interact with minor data (student data for schools/coaching)
- **Induction:** Every new joiner completes a structured 5-day induction programme within their first 2 weeks

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `hr_training_enrollment` aggregated + `hr_training_course WHERE mandatory=true` completion counts | 5 min |
| Course library | `hr_training_course` ORDER BY category, created_at | 10 min |
| Enrollment table | `hr_training_enrollment` JOIN `hr_employee` JOIN `hr_training_course` | 5 min |
| Skills matrix | `hr_skills` JOIN `hr_employee` | 15 min |
| Certifications | `hr_certification` JOIN `hr_employee` | 10 min |
| Analytics | `hr_training_enrollment` aggregated + `hr_skills` for reports | 30 min |
| Training calendar | `hr_training_course` WHERE scheduled_date IS NOT NULL AND scheduled_date >= today ORDER BY scheduled_date | 10 min |
| TNA feed | `hr_performance_review.self_assessment` + `hr_pip` learning goals → parsed training needs | 30 min |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?tab` | `calendar`, `courses`, `enrollments`, `skills`, `certifications`, `analytics` | `calendar` | Active section |
| `?category` | `technical`, `domain`, `compliance`, `leadership`, `soft_skills`, `all` | `all` | Filter courses by category |
| `?mandatory` | `1` | — | Show only mandatory courses |
| `?division` | A–O | `all` | Filter enrollments/skills by division |
| `?employee_id` | UUID | — | Jump to specific employee's learning profile |
| `?completion_status` | `enrolled`, `in_progress`, `completed`, `failed`, `overdue`, `all` | `all` | Filter enrollments |
| `?cert_expiry_before` | `YYYY-MM-DD` | — | Certifications expiring before date |
| `?export` | `completion_report_csv`, `skills_matrix_csv` | — | Export (L&D Coordinator + HR Manager) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| Training calendar | `?part=calendar` | Page load + tab click | `#o8-calendar` |
| Course library | `?part=courses` | Tab click + filter | `#o8-courses` |
| Enrollment table | `?part=enrollments` | Tab click + filter | `#o8-enrollments` |
| Skills matrix | `?part=skills_matrix` | Tab click + filter | `#o8-skills-matrix` |
| Certifications table | `?part=certifications` | Tab click + filter | `#o8-certifications` |
| Analytics | `?part=analytics` | Tab click | `#o8-analytics` |
| Course drawer | `?part=course_drawer&id={id}` | Row click | `#o8-course-drawer` |
| Enrollment drawer | `?part=enrollment_drawer&id={id}` | Row click | `#o8-enrollment-drawer` |
| Create course modal | `?part=create_course_modal` | [+ Add Course] click | `#modal-container` |
| Enroll employees modal | `?part=enroll_modal&course_id={id}` | [Enroll Employees] click | `#modal-container` |
| Send reminder action | `POST /hr/learning/enrollments/{id}/remind/` | [Send Reminder] click | Inline toast |
| Mark complete action | `POST /hr/learning/enrollments/{id}/complete/` | [Mark Complete] click | Inline swap |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Learning & Development                           [+ Add Course]     │
├──────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 tiles)                                                 │
├──────────────────────────────────────────────────────────────────────┤
│  [Calendar] [Courses] [Enrollments] [Skills] [Certifications] [Analytics] │
└──────────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip (5 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 84%          │ │ 3            │ │ 42           │ │ 18           │ │ 7            │
│ Mandatory    │ │ Sessions     │ │ Enrollments  │ │ Certif.      │ │ Expiring     │
│ Completion   │ │ This Month   │ │ In Progress  │ │ Tracked      │ │ in 30d       │
│ 94/112 emp.  │ │              │ │              │ │              │ │ ⚠ renew      │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Mandatory Completion Rate:** `COUNT(hr_training_enrollment WHERE mandatory=true AND completion_status='COMPLETED') / COUNT(hr_employee WHERE status='ACTIVE') × 100`. Green if ≥ 90%, amber if 75–89%, red if < 75%.

**Tile 2 — Sessions This Month:** Upcoming/completed training sessions scheduled this calendar month.

**Tile 3 — Enrollments In Progress:** Active enrollments (ENROLLED + IN_PROGRESS combined). Clicking opens Enrollments tab filtered to in-progress.

**Tile 4 — Certifications Tracked:** Total certifications on record across all employees.

**Tile 5 — Expiring in 30d:** Certifications expiring within 30 days. Amber warning. Clicking opens Certifications tab filtered by expiry.

---

## Calendar Tab (default)

### Training Calendar

A monthly calendar view of all scheduled training sessions.

```
  April 2026
  ─────────────────────────────────────────────────────────
  Mon 1 Apr    — no sessions
  Tue 2 Apr    AWS Advanced (Vendor: CloudPath)   10:00–17:00   Room A + Zoom   8 enrolled
  Thu 4 Apr    POSH Awareness FY26 (Batch 3)      14:00–16:00   Zoom            6 enrolled
  Mon 7 Apr    Django Masterclass (In-house)       10:00–13:00   Room B          12 enrolled
  ...
  ─────────────────────────────────────────────────────────
  [Previous Month]                                [Next Month]
```

Click on session → opens Course Drawer with enrollment list for that session.

**Session types:**
- **IN_HOUSE:** Internal facilitator (SME, HRBP, L&D Coordinator). No vendor cost.
- **EXTERNAL_VENDOR:** Third-party trainer. Cost per seat tracked.
- **ONLINE_LMS:** Self-paced on internal/external LMS. No fixed date — enrollment-based completion.

**[+ Schedule Session]:** L&D Coordinator adds a new training date to an existing course. Sends enrollment invite to enrolled employees.

---

## Courses Tab

### Course Library Table

| Column | Description |
|---|---|
| Title | Course name (link → opens Course Drawer) |
| Category | TECHNICAL / DOMAIN / COMPLIANCE / LEADERSHIP / SOFT_SKILLS |
| Delivery Mode | IN_HOUSE / EXTERNAL_VENDOR / ONLINE_LMS |
| Mandatory | ✓ (green) / — |
| Applicable Roles | Count of role types this course is designed for |
| Duration | Hours |
| Enrolled (active) | Count of current active enrollments |
| Completed (all time) | Total completions |
| Cost/Seat | ₹ (blank if in-house) |
| Actions | [View] [Enroll Employees] [Edit] [Archive] |

### Course Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  AWS Certified Developer — Associate Prep            [Edit] [×]  │
│  Category: TECHNICAL · External Vendor: CloudPath               │
│  Duration: 16 hours (2 days) · Cost: ₹8,500/seat               │
│  Mandatory: No · Target roles: Backend Eng., DevOps, AI/ML Eng. │
├──────────────────────────────────────────────────────────────────┤
│  Description:                                                    │
│  "Preparation for the AWS Developer Associate certification.     │
│   Covers Lambda, API Gateway, DynamoDB, S3, CloudFormation,     │
│   and CI/CD pipelines. Recommended for Division C engineers."   │
├──────────────────────────────────────────────────────────────────┤
│  Scheduled Sessions:                                             │
│  2 Apr 2026   10:00–17:00   Room A + Zoom   8 enrolled   [View] │
│  (next: 5 Jun 2026)                                             │
├──────────────────────────────────────────────────────────────────┤
│  Enrolled Employees (8):                                        │
│  Rohan V. (Div C)   IN_PROGRESS                                 │
│  Priya S. (Div C)   ENROLLED                                    │
│  Arjun M. (Div C)   ENROLLED                                    │
│  ...                                                            │
│  [Enroll More Employees]  [Export Attendance List]              │
├──────────────────────────────────────────────────────────────────┤
│  Completion History: 24 employees completed (all time)          │
└──────────────────────────────────────────────────────────────────┘
```

### Create Course Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Add Course to Library                                           │
├──────────────────────────────────────────────────────────────────┤
│  Course Title*           [                              ]        │
│  Category*               [TECHNICAL                   ▼]        │
│  Delivery Mode*          [EXTERNAL_VENDOR             ▼]        │
│  Duration (hours)*       [16     ]                              │
│  Mandatory?              [☐]  Applicable Roles: [+ Select]       │
│  Vendor Name             [CloudPath                    ]        │
│  Cost per Seat (₹)       [8500   ]                              │
│  Description             [                              ]        │
│  Learning Objectives     [                              ] [+ Add] │
│                                                                  │
│  ⚠ Cost per seat > ₹50,000 requires HR Manager budget approval.  │
│                                                                  │
│  [Cancel]                                  [Add to Library]      │
└──────────────────────────────────────────────────────────────────┘
```

**Budget approval gate:** Courses with `cost_per_seat > ₹50,000` OR total enrollment cost (cost_per_seat × enrolled count) > ₹2,00,000 require HR Manager approval before vendor confirmation.

### Enroll Employees Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Enroll Employees — AWS Developer Associate Prep                 │
├──────────────────────────────────────────────────────────────────┤
│  Select employees:   [Search by name or division...]             │
│  ☑ Rohan Verma      Backend Engineer (Div C)                    │
│  ☑ Priya Sharma     Backend Engineer (Div C)                    │
│  ☐ Kavya Rao        Frontend Engineer (Div C)                   │
│  ...                                                             │
│  Selected: 8 employees   Estimated cost: ₹68,000                │
│  ⚠ Total cost exceeds ₹50K threshold — HR Manager approval req.  │
│                                                                  │
│  Session: [2 Apr 2026 — 10:00 AM ▼]                             │
│  [Cancel]                              [Enroll & Notify]         │
└──────────────────────────────────────────────────────────────────┘
```

On enroll: creates `hr_training_enrollment` rows, sends email notifications to enrolled employees with calendar invite.

---

## Enrollments Tab

### Enrollment Table

| Column | Description |
|---|---|
| Employee | Name + division |
| Course | Course title |
| Category | |
| Mode | Delivery mode badge |
| Enrolled Date | |
| Session Date | Scheduled date (if applicable) |
| Status | ENROLLED / IN_PROGRESS / COMPLETED / FAILED / DROPPED |
| Score | % score (if assessed) or — |
| Certificate | ✓ (link) / — |
| Actions | [View] [Mark Complete] [Send Reminder] [Drop] |

Colour coding: OVERDUE rows (mandatory course, session date passed, not completed) in red-50 background.

**[Mark Complete]:** L&D Coordinator marks completion for offline/vendor-led courses. Prompts for:
- Completion date
- Score % (optional, if assessed)
- Certificate upload (PDF to R2, stored in `hr_training_enrollment.certificate_r2_key`)

**[Send Reminder]:** Throttled (max once per 3 days per enrollment). Sends email to employee: "Your [course name] session is on [date]. Please confirm attendance / complete the module."

**[Drop]:** Removes enrollment. If mandatory course: creates a warning in the employee's learning profile — "Dropped mandatory course [name]. Re-enrollment required by [deadline]."

---

## Mandatory Compliance Training Tracking

Special section within Enrollments tab, filtered view of mandatory compliance courses:

```
  Mandatory Compliance Training — FY 2025-26

  POSH Awareness FY26
  ─────────────────────────────────────────────────────────
  Required: All 112 active employees
  Completed: 94   Pending: 12   Overdue: 6
  Progress bar: [████████████████████░░░░░]  84%
  ─────────────────────────────────────────────────────────
  [View Pending List]  [Send Bulk Reminder to Overdue]

  Data Privacy Awareness FY26
  ─────────────────────────────────────────────────────────
  Required: All 112 active employees
  Completed: 107  Pending: 5   Overdue: 0
  Progress bar: [████████████████████████░]  95.5%
  ─────────────────────────────────────────────────────────
  [View Pending List]  [Send Bulk Reminder to Pending]

  POCSO Awareness FY26 (Divisions D, G, I only — 31 employees required)
  ─────────────────────────────────────────────────────────
  Completed: 29   Pending: 2   Overdue: 0
  Progress bar: [████████████████████████░]  93.5%
  ─────────────────────────────────────────────────────────
```

[Send Bulk Reminder to Overdue]: one-click sends reminder emails to all employees with overdue mandatory training. L&D Coordinator and HR Manager only. Toast: "Reminder sent to [N] employees."

**POSH Annual Report data:** This section also feeds the POSH annual report. At year-end, L&D Coordinator exports the POSH training completion list for inclusion in the Division N Legal Officer's POSH annual report to the District Officer.

---

## Skills Tab

### Skills Matrix

Heatmap table — employees (rows) × skills (columns). Cell = proficiency level.

```
              Django  PostgreSQL  AWS  HTMX  Flutter  Python  React
  Rohan V.    EXPERT  ADVANCED    INT  INTER  —        ADV    —
  Priya S.    ADV     INTER       ADV  BEG    —        INTER  —
  Kavya R.    INTER   BEG         —    ADV    —        BEG    ADV
  ...
```

Colour coding:
- BEGINNER: grey-100
- INTERMEDIATE: blue-100
- ADVANCED: blue-400
- EXPERT: blue-700
- — (not assessed): white

Filter by:
- Division (show only Division C skills, for example)
- Skill category (Technical / Domain / Soft Skills)
- Proficiency level (show gaps: filter to BEGINNER or —)

**Skills Gap Analysis:** [View Gap Report] button — compares current team skills against a predefined "skills required" list (editable by L&D Coordinator and HR Manager) for each division. Shows which skills are understaffed.

```
  Skills Gap Report — Division C (Engineering)
  ─────────────────────────────────────────────────────────
  Skill           Required   ADVANCED+   Gap
  Django          8          6           2 employees need upskilling
  AWS Lambda      8          4           4 employees need upskilling  ⚠
  HTMX            8          3           5 employees need upskilling  ⚠
  PostgreSQL      8          7           1 employee needs upskilling
  ...
  [Export as CSV]
```

### Add / Edit Skill

L&D Coordinator, HRBP, or HR Manager can add/edit skills for an employee (or employees can self-update via `/hr/my-learning/skills/`). Proficiency levels updated after training completion (can be auto-updated if `hr_training_course` maps to a skill: `course.skill_impact` JSONB field).

---

## Certifications Tab

### Certifications Table

| Column | Description |
|---|---|
| Employee | Name + division |
| Certification | Cert name |
| Issuing Body | AWS, Google, SHRM, etc. |
| Issued Date | |
| Expiry Date | Colour-coded: red if < 30 days, amber if < 90 days |
| Status | ACTIVE / EXPIRING_SOON / EXPIRED |
| Certificate | [View PDF] |
| Actions | [Edit] [Renew] [Delete] |

[Renew]: opens modal to upload renewed certificate with new issued/expiry dates. Old certificate archived.

**Task O-12 feed:** Daily certification expiry scanner flags certs expiring within 30 days → shown here with amber/red badges + L&D Coordinator and employee notified.

### Add Certification Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Add Certification                                               │
├──────────────────────────────────────────────────────────────────┤
│  Employee*            [Search employee...           ▼]           │
│  Certification Name*  [AWS Certified Developer       ]           │
│  Issuing Body*        [Amazon Web Services           ]           │
│  Issued Date*         [2026-03-15                    ]           │
│  Expiry Date          [2029-03-15                    ]           │
│  Upload Certificate*  [Choose PDF...                 ]           │
│                                                                  │
│  [Cancel]                             [Save Certification]       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Analytics Tab

### Training Completion Trend (12 months)

Line chart — monthly training completion count vs enrollments.

- **Line 1 (blue):** total enrollments created per month
- **Line 2 (green):** completions per month
- **Reference line:** 70% completion target (amber dashed)
- **Hover tooltip:** month · enrollments · completions · completion rate %

### Training by Category (donut chart)

Distribution of training hours consumed across categories: TECHNICAL / DOMAIN / COMPLIANCE / LEADERSHIP / SOFT_SKILLS.

### L&D Spend Trend

Bar chart — monthly training spend (₹) from `hr_training_enrollment` × `hr_training_course.cost_per_seat`.

- Bar per month (last 12 months)
- Reference line: monthly L&D budget threshold (configurable by HR Manager)
- Hover: month · spend · sessions · employees trained

**Visible to:** HR Manager (#79) only (budget data).

### Skills Coverage Heatmap

Division-level view of skill coverage:

```
  Division C — Engineering   ████████░░  82% skill coverage vs required
  Division D — Content       ████████████ 94% skill coverage
  Division I — Support       ██████░░░░░  61% skill coverage  ⚠
  ...
```

Red/amber for divisions below 70% coverage threshold. Drives TNA (Training Needs Assessment) planning.

### Training Needs Analysis (TNA) Feed

Auto-generated suggestions based on:
1. Performance reviews: `hr_performance_review.self_assessment` mentions training needs → extracted and grouped by skill/category
2. PIP goals: training components from active PIPs
3. Skills gap report: high-gap skills across divisions

```
  Suggested Training Needs (auto-extracted from performance reviews + PIPs):

  AWS Lambda (advanced)    Mentioned by 6 employees in self-assessment   [Add Course]
  System Design            Mentioned by 4 employees in self-assessment   [Add Course]
  Communication Skills     Mentioned by 3 managers in reviews            [Add Course]
```

[Add Course] → pre-fills the Create Course modal with the suggested skill.

---

## Induction Programme

New joiner induction is a special course (`mandatory=true`, `applicable_to='ALL'`) auto-enrolled for every new joiner on their join date. Structure:

```
  5-Day EduForge Induction Programme

  Day 1 (L&D Coord):    Company overview, culture, values, tools walkthrough
  Day 2 (HR Mgr):       HR policies, leave, payroll, POSH, Code of Conduct
  Day 3 (Platform Admin): Internal systems access, security policies, data privacy
  Day 4 (Division head): Role-specific onboarding + team introductions
  Day 5 (HRBP):          OKR framework, performance review process, probation expectations
```

Completion tracked per day. Induction completion shown on O-01 HR Dashboard L&D strip.

---

## Empty States

| Condition | Message |
|---|---|
| No courses in library | "No courses in the library yet. [+ Add Course]" |
| No scheduled sessions this month | "No training sessions scheduled for [month]. [+ Schedule Session]" |
| No active enrollments | "No active enrollments." |
| No skills data for employee | "No skills recorded. Update after completing training or assessment." |
| No certifications | "No certifications tracked. [+ Add Certification]" |
| All mandatory training complete | "All mandatory compliance training completed for the period." with green shield |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Course added | "Course '[title]' added to library." | Green |
| Employees enrolled | "[N] employees enrolled in '[course]'. Invites sent." | Green |
| Completion marked | "[Name] marked as completed for '[course]'." | Green |
| Reminder sent | "Reminder sent to [Name] for '[course]'." | Blue |
| Bulk reminder sent | "Reminder sent to [N] employees for mandatory training." | Blue |
| Certification added | "Certification '[name]' added for [employee]." | Green |
| Budget approval required | "Course cost exceeds ₹50K. HR Manager approval required." | Amber |
| Skills updated | "Skills updated for [Name]." | Green |

---

## Authorization

**Route guard:** `@division_o_required(allowed_roles=[79, 107])` applied to `LearningView`. HR Business Partner (#106) read-only access to analytics and skills matrix at `/hr/learning/?readonly=1`.

| Scenario | Behaviour |
|---|---|
| [+ Add Course] | L&D Coordinator (#107) and HR Manager (#79) |
| Budget approval | HR Manager (#79) only — approval modal and gate |
| [Mark Complete] | L&D Coordinator (#107) and HR Manager (#79) |
| Export skills matrix / completion report | L&D Coordinator (#107) and HR Manager (#79) |
| POSH bulk reminder | L&D Coordinator (#107) and HR Manager (#79) |
| L&D Spend chart | HR Manager (#79) only |
| Skills Gap Report | L&D Coordinator (#107) full; HRBP (#106) read-only; HR Manager (#79) full |

---

## Skills Gap Auto-Remediation Rules

When the Skills Gap Report identifies an employee with a gap (required proficiency not met), the system takes one of two actions depending on configuration:

### Policy: Alert-Only vs Auto-Enrol

Configured globally by HR Manager in `hr_policy_config.skills_gap_remediation` (default: ALERT_ONLY):

| Mode | Behaviour |
|---|---|
| `ALERT_ONLY` | Skills gap appears in L&D Coordinator's dashboard strip on O-01 and in the Skills Gap Report. No automatic enrollment. L&D Coordinator decides manually whether to enroll. Toast on gap detection: "5 employees have a gap in AWS Lambda. [View Gap Report]" |
| `AUTO_ENROL` | If a course in the library directly maps to the gap skill (`hr_training_course.skill_impact` JSONB contains the skill), the system auto-enrolls the employee in the next scheduled session of that course. L&D Coordinator receives notification: "[Name] auto-enrolled in [course] to address AWS Lambda gap." Employee receives enrollment notification. HR Manager approval gate still applies if cost exceeds ₹50K. |

### Gap Detection Trigger

Gap detection runs:
1. **Daily** — Task O-12 extension: after certification/skill update, re-runs gap check for affected employee
2. **After performance review cycle close** — HRBP's skills recommendations from review → `hr_required_skill` update → gap re-check
3. **Manual** — L&D Coordinator or HR Manager clicks [Run Gap Analysis] in Skills tab

### Auto-Enrol Edge Cases

| Case | Handling |
|---|---|
| No matching course in library | Falls back to ALERT_ONLY. Gap flagged for L&D Coordinator to source a course. |
| Employee already enrolled | No duplicate enrollment created. Existing enrollment noted in gap report. |
| Course has no upcoming session | Gap alert raised + L&D Coordinator prompted to schedule a session. |
| Employee on leave during session | Enrollment created but L&D Coordinator notified: "[Name] is on leave on session date." |
| Cost threshold exceeded | Auto-enrol paused; HR Manager approval required before enrollment confirmed. |

---

## TNA Feed — Extraction Methodology

Training Needs Analysis (TNA) is auto-populated from three sources:

### Source 1: Performance Review Self-Assessments

After each review cycle closes, a Celery task parses `hr_performance_review.self_assessment` (free-text field) for training signals:

```python
# Pattern matching via keyword extraction (no LLM — keyword list maintained by L&D Coord)
TRAINING_KEYWORDS = [
    "training", "learn", "upskill", "certification", "course",
    "improve", "develop", "skill", "gap", "need to", "wish I knew"
]
# Extracts sentences containing keywords + associated skill/technology mentions
# Groups by most-mentioned skills across all employees in the cycle
# Stores as hr_tna_suggestion rows: {source='REVIEW', skill, mention_count, cycle_id}
```

### Source 2: Manager Review Recommendations

`hr_performance_review.manager_review` free-text parsed for the same keyword list. Manager-suggested training needs weighted ×1.5 vs self-identified (manager visibility tends to be more objective).

### Source 3: Active PIP Goals

All open PIPs with `goal_text` containing training milestones (e.g., "Complete AWS certification by...") are extracted directly — these are the highest-priority TNA items as they are linked to active performance remediation.

### TNA Display in Analytics Tab

```
  Training Needs Analysis (auto-extracted — FY 2025-26 Annual Review Cycle)
  Last refreshed: 21 Mar 2026

  Source: Performance Reviews + Manager Reviews + Active PIPs

  Skill / Area             Mentions   Sources              Priority   Actions
  ──────────────────────────────────────────────────────────────────────────
  AWS Lambda (advanced)       6       4 self + 2 mgr        MEDIUM    [Add Course]
  System Design               5       2 self + 3 mgr        HIGH      [Add Course]
  Communication Skills        4       0 self + 4 mgr        HIGH      [Add Course]
  HTMX Internals              3       3 self + 0 mgr        MEDIUM    [Add Course]
  Python Performance          2       1 self + 1 mgr + PIP  CRITICAL  [Add Course]
  ──────────────────────────────────────────────────────────────────────────
  [Export TNA Report CSV]
```

Priority logic:
- `CRITICAL`: mentioned in at least 1 active PIP goal
- `HIGH`: mentioned ≥3 times across reviews AND ≥1 manager mention
- `MEDIUM`: mentioned 2–4 times, no manager mention or PIP link

[Add Course] pre-fills Create Course modal with skill name in the description field.

---

## `/hr/my-learning/` — Employee Self-Serve Spec

All employees access their own learning profile. `@login_required` only — no Division O membership.

| Feature | Description |
|---|---|
| My Courses | Grid/list of enrolled courses with status (ENROLLED / IN_PROGRESS / COMPLETED / OVERDUE). Click → course detail with session date, materials link (if LMS), and certificate download (if completed) |
| Mandatory Training Status | Prominent card: mandatory compliance courses for the employee's role. Shows completion status and due date. Overdue courses shown with red badge |
| Request Enrollment | Employee can browse the course library and request enrollment in any course. L&D Coordinator receives notification to approve/enroll. Creates a `hr_training_enrollment` row with `status='PENDING_APPROVAL'` |
| My Skills | View own skills profile with proficiency levels. Employee can self-update proficiency (pending L&D Coordinator confirmation for ADVANCED+ levels) |
| My Certifications | View own certifications with expiry dates. Upload new certificate (pending L&D Coordinator review) |
| My Learning History | Paginated history of all past enrollments, completion dates, and scores |

**Enrollment request flow:**
```
  Employee → [Request Enrollment] on course
  → POST /hr/my-learning/enroll-request/{course_id}/
  → hr_training_enrollment created: status='PENDING_APPROVAL'
  → L&D Coordinator notified: "[Name] requested enrollment in [course]."
  → L&D Coordinator approves/rejects in O-08 Enrollments tab
  → Employee notified of outcome via email
```

**Skill self-update:**
```
  Employee → [Update Skill] → select proficiency [BEG/INT/ADV/EXPERT]
  → If INTERMEDIATE or below: auto-confirmed, updates hr_skills directly
  → If ADVANCED or EXPERT: status='PENDING_CONFIRMATION'
    → L&D Coordinator reviews in Skills tab [Confirm Skill] queue
    → Confirmation requires evidence: training completion or certification link
```

Route guard: `@login_required`. No minimum role — every active employee sees own learning profile.

---

## Role-Based UI Visibility Summary

| UI Element | HR Manager (#79) | L&D Coord (#107) | HRBP (#106) |
|---|---|---|---|
| Calendar tab — full access | ✓ | ✓ | Read-only |
| Courses tab — [+ Add Course] | ✓ | ✓ | — |
| Budget approval gate | ✓ (approver) | — (requestor) | — |
| Enrollments tab — [Mark Complete] | ✓ | ✓ | — |
| Enrollments tab — [Send Reminder] | ✓ | ✓ | — |
| Mandatory compliance tracker | ✓ | ✓ | Read-only |
| [Send Bulk Reminder — Overdue] | ✓ | ✓ | — |
| Skills tab — full matrix | ✓ | ✓ | Read-only |
| Skills gap report | ✓ (full) | ✓ (full) | Read-only |
| [Confirm Skill] queue | ✓ | ✓ | — |
| Certifications tab — [Add/Renew] | ✓ | ✓ | — |
| Analytics — L&D Spend chart | ✓ | — | — |
| Analytics — TNA feed | ✓ | ✓ | Read-only |
| [Export skills matrix / completion report] | ✓ | ✓ | — |
| `/hr/my-learning/` (self-serve) | ✓ (own) | ✓ (own) | ✓ (own) |

---

## Performance Requirements

| Operation | Target | Notes |
|---|---|---|
| Calendar tab load | < 800ms P95 | Upcoming sessions + KPI strip; Memcached 10 min |
| Course library load | < 600ms P95 | Paginated 50/page; Memcached 10 min |
| Enrollment table load | < 800ms P95 | JOIN across 3 tables, paginated; Memcached 5 min |
| Skills matrix render | < 1.5s P95 | 150 employees × 20+ skills heatmap; Memcached 15 min |
| Skills gap report generation | < 3s | Compares skills vs `hr_required_skill`; triggered on demand |
| TNA feed parse (post-cycle) | < 30s | Celery task; keyword extraction across all review texts |
| Mandatory compliance tracker | < 1s P95 | Aggregated completion counts; Memcached 5 min |
| Certificate PDF upload to R2 | < 5s | Up to 10MB; KMS-encrypted at rest |
| Export completion report CSV | < 10s | All enrollments for FY; async if > 500 rows |
| `/hr/my-learning/` self-serve | < 500ms P95 | Own records; no matrix computation |

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `g l` | Go to Learning & Development page (`/hr/learning/`) |
| `t c` | Switch to Calendar tab |
| `t o` | Switch to Courses tab |
| `t e` | Switch to Enrollments tab |
| `t s` | Switch to Skills tab |
| `t x` | Switch to Certifications tab |
| `t a` | Switch to Analytics tab |
| `n` | New Course (opens Create Course modal) |
| `/` | Focus search / filter input |
| `Esc` | Close drawer / modal |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Calendar tab load | < 1.5s P95 | Simple calendar render |
| Skills matrix load (all employees) | < 3s P95 | Heavy join: `hr_skills` × 100+ employees × 50+ skills — consider chunked HTMX loads by division |
| Enrollment table (100+ rows) | < 1s P95 (cache hit: 5 min) | Server-side paginated |
| TNA feed generation | < 5s | Text extraction from JSONB fields; runs on tab click, not page load |
