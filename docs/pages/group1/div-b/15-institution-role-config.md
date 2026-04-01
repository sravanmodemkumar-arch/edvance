# Page 15 — Institution Role Config

**URL:** `/portal/product/institution-role-config/`
**Permission:** `product.manage_institution_roles`
**Priority:** P1
**Roles:** PM Institution Portal, PM Platform

---

## Purpose

Defines and governs the complete permission system for all roles that exist inside institution-facing portals. Every school admin, college department head, coaching centre faculty member, batch manager, and group-level supervisor operates under a role whose permissions are defined here. This is the SRAV platform team's control over what institution-side users can do — a distinct concern from SRAV's own internal admin roles.

Core responsibilities:
- Define all institution role templates (system roles) that institutions choose from when creating users
- Control which permissions each role template carries per feature area
- Allow institutions to clone system role templates and create custom variants within defined bounds
- Manage role assignment rules (which roles can assign which other roles — anti-escalation)
- Track custom roles created by institutions and review for DPDPA compliance
- Audit all role configuration changes with immutable log
- Ensure data minimisation: roles carry only the permissions they legitimately need

**Scale context:**
- 1,950+ institutions (1,000 schools + 800 colleges + 100 coaching + 150 groups)
- Estimated 15,000–25,000 institution-side admin and faculty users across all institutions
- 40+ permission categories across 8 feature areas
- Each institution can create up to 20 custom role variants on top of the 12 system templates
- Changes to system roles propagate to all institutions using that role — high impact

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Institution Role Config"               [New System Role]      │
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 5 cards                                            │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  System Roles · Permission Matrix · Custom Roles                │
│  Assignment Rules · DPDPA Compliance · Audit Log                │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 5 Cards

| # | Label | Value | Colour | Click Action |
|---|---|---|---|---|
| 1 | System Roles | Count of platform-defined role templates | — | Opens System Roles tab |
| 2 | Total Permissions | Count of individual permission codenames in system | — | Opens Permission Matrix |
| 3 | Custom Roles Active | Count of institution-created role variants with at least 1 user | — | Opens Custom Roles tab |
| 4 | Unassigned Admins | Institution users with no role assigned (risk) | Red if > 0 | Opens Custom Roles tab filtered |
| 5 | Roles Changed (30d) | System role config changes in last 30 days | — | Opens Audit Log |

---

## Tab 1 — System Roles

Displays all platform-defined role templates. These are the base roles that every institution's user management interface presents when creating admin or faculty accounts.

### Role Grid (3-column cards)

Each card:

| Field | Detail |
|---|---|
| Role Name | Bold (e.g. "Institution Admin", "Faculty") |
| Category | Admin · Academic · Finance · Support |
| Description | 2-line summary |
| Permission Count | "X permissions across Y feature areas" |
| Institutions Using | Count of institutions with at least 1 user on this role |
| Users on Role | Total user count across all institutions |
| Restricted | Badge: if institutions cannot customise this role |
| Actions | Edit · View Permission Matrix · Clone · Archive |

### Complete 12 System Roles

**Admin Category:**

**1. Institution Admin**
- Full access to all institution features: exam management, student management, analytics, communication, finance, settings, integrations, mobile
- Can manage all users and assign all roles below Institution Admin
- Can delete institution account (irreversible — 2FA required)
- Can access billing and subscription management
- Typically 1–2 users per institution
- Restriction: Cannot be cloned by institutions; cannot be modified by institutions

**2. Co-Admin**
- Identical to Institution Admin except:
  - Cannot manage billing or subscriptions
  - Cannot delete institution account
  - Cannot manage the Institution Admin's account
  - Cannot change the institution's plan tier
- Designed for a second-in-command or department head who needs near-full access

**3. IT Admin**
- Institution settings, integrations, SSO configuration, webhook management, API key management
- Can manage user accounts (create, deactivate, reset passwords) but cannot change roles
- No access to exam data, student performance, or finance

**Academic Category:**

**4. Department Head**
- Full exam management for their assigned departments
- View analytics for all students in their departments (not restricted to batches)
- Can create, publish, and schedule exams
- Can view all student PII within their departments
- Can manage all faculty within their departments
- Cannot access finance or billing

**5. Senior Faculty**
- Can create, edit, and publish exams in their assigned batches
- Can upload questions to the question bank (institution-level)
- Can view all exam results and detailed analytics for their assigned batches
- Can send announcements to their batches
- Cannot delete exams or students

**6. Faculty**
- Can view exam results for their assigned students
- Can create practice exams (cannot schedule live exams)
- Can view batch-level analytics (not individual student PII beyond name and score)
- Can respond to student doubts
- Cannot create or modify student accounts

**7. Teaching Assistant (TA)**
- Can assist faculty in question review and result review
- Read-only access to exam results for their assigned batches
- Cannot create exams or upload questions
- No access to student PII beyond name and roll number

**8. Batch Manager**
- Manages student batches: enroll students, move between batches, create/rename batches
- Can send batch-level announcements
- Can view batch enrollment counts and basic performance metrics
- No access to individual exam results or detailed analytics

**9. Content Manager**
- Uploads and manages study materials, notes, videos, reference PDFs
- No access to exam creation, student data, or results
- Can categorise and tag content
- Can see content download/view statistics

**Finance Category:**

**10. Accounts Manager**
- Access to billing dashboard, fee collection, invoices, GST reports, payment gateway configuration
- Can process refunds
- No access to exam data, student performance, or academic settings

**Support Category:**

**11. Student Counsellor**
- Read-only access to individual student performance and progress reports
- Can view attendance records
- Can add private notes on student profiles
- Cannot modify any exam, student account, or settings
- DPDPA note: this role accesses student PII — purpose must be documented

**12. Observer**
- Read-only access to institution dashboard and high-level summary analytics only
- No access to individual student data, exams, or financial data
- Designed for board members, governing body members, or external auditors

### Role Detail Drawer (640px)

**Tab 1 — Overview:**
- Role name, description, category
- Created date · Last modified · Modified by
- Usage: X institutions using · Y total users · Z average users per institution
- "Restricted Role" explanation if flagged

**Tab 2 — Permission List:**
All permissions grouped by feature area. For each permission:
- Codename (e.g. `exam.create_exam`)
- Human-readable description
- Category badge
- Enabled (✓) or Disabled (✗)
- DPDPA sensitivity: PII access (🛡) or non-PII

**Tab 3 — Institutions Using:**
Table: Institution Name · Type · User Count on Role · Last Role Activity

**Tab 4 — Change History:**
All changes to this role template: Timestamp · Changed By · Permission Changed · Before · After

---

## Tab 2 — Permission Matrix

Full matrix of all permissions across all 12 system roles.

### Toolbar
- Search permissions (name or codename)
- Filter by Feature Area
- Filter by DPDPA sensitivity: All / PII-touching / Non-PII
- Edit Mode toggle (amber header when active)

### Permission Matrix Table

Rows = permissions. Columns = system roles (abbreviated headers). ✓ = granted · ✗ = not granted · 🛡 = granted but PII-sensitive.

**EXAM MANAGEMENT permissions:**

| Permission | Inst Admin | Co-Admin | IT Admin | Dept Head | Sr Faculty | Faculty | TA | Batch Mgr | Content Mgr | Accounts | Counsellor | Observer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Create exam | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Publish exam | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Edit exam | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Delete exam | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| View results (all batches) | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓🛡 | ✗ |
| View results (own batch) | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✓🛡 | ✗ |
| Enable proctoring | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Download answer scripts | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| View live exam feed | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Extend exam duration | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Cancel exam | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**STUDENT MANAGEMENT permissions:**

| Permission | Inst Admin | Co-Admin | IT Admin | Dept Head | Sr Faculty | Faculty | TA | Batch Mgr | Content Mgr | Accounts | Counsellor | Observer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Add student | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Edit student profile | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Delete student | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| View student PII | ✓🛡 | ✓🛡 | ✗ | ✓🛡 | ✓🛡 | ✗ | ✗ | ✓🛡 | ✗ | ✗ | ✓🛡 | ✗ |
| Export student data | ✓🛡 | ✓🛡 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Bulk import students | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Manage batches | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| View attendance | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✓ | ✗ |
| Mark attendance | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |

**ANALYTICS permissions:**

| Permission | Inst Admin | Co-Admin | IT Admin | Dept Head | Sr Faculty | Faculty | TA | Batch Mgr | Content Mgr | Accounts | Counsellor | Observer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| View institution dashboard | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| View student analytics | ✓🛡 | ✓🛡 | ✗ | ✓🛡 | ✓🛡 | ✗ | ✗ | ✗ | ✗ | ✗ | ✓🛡 | ✗ |
| View batch analytics | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| View comparative analytics | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Export analytics PDF | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| View financial analytics | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ |

**COMMUNICATION permissions:**

| Permission | Inst Admin | Co-Admin | IT Admin | Dept Head | Sr Faculty | Faculty | TA | Batch Mgr | Content Mgr | Accounts | Counsellor | Observer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Send announcement (all) | ✓ | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Send announcement (batch) | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Send bulk SMS | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Send bulk WhatsApp | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

**SETTINGS permissions:**

| Permission | Inst Admin | Co-Admin | IT Admin | Dept Head | Sr Faculty | Faculty | TA | Batch Mgr | Content Mgr | Accounts | Counsellor | Observer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Edit institution profile | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Manage integrations (SSO) | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Manage API keys | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Manage webhooks | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Manage users and roles | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Manage billing | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |

🛡 = PII-touching permission. DPDPA 2023 data minimisation principle applies.

**Edit Mode behaviour:**
- Toggle switches per cell
- Changing a PII-sensitive permission to enabled: inline DPDPA warning
- Changing a permission that has dependencies: inline dependency warning
- Changes are staged, not applied immediately

---

## Tab 3 — Custom Roles

Institution-created custom role variants. Institutions clone a system role and modify within allowed bounds.

### Toolbar
- Search by role name or institution name
- Filter by base role
- Filter by institution type and plan tier
- Filter by DPDPA risk: All / Contains PII permissions / Clean

### Custom Roles Table — 9 columns

| Column | Detail |
|---|---|
| Role Name | Institution's custom name |
| Institution | Name + type badge |
| Base Role | System template it was cloned from |
| Plan Tier | Institution's current plan |
| Users on Role | Count |
| Permission Delta | "+X / -Y" vs base role |
| DPDPA Risk | Low / Medium / High badge |
| Last Modified | Date |
| Actions | View Matrix · Flag for Review · Delete |

**DPDPA Risk calculation:**
- Low: same or fewer PII permissions than base role
- Medium: 1–2 additional PII permissions vs base
- High: 3+ additional PII permissions vs base, or export of student PII added

### Custom Role Detail Drawer (640px)

**Tab 1 — Permission Diff:**
- Added permissions (green rows): permission name + DPDPA sensitivity
- Removed permissions (red rows)
- Unchanged (grey, collapsed by default with "Show unchanged" toggle)

**Tab 2 — Users on Role:**
Table: Name · Email (masked) · Last login · Assigned on date

**Tab 3 — DPDPA Assessment:**
For each PII permission held by this role:
| Permission | Data Accessed | DPDPA Category | Purpose Documented | Risk |
|---|---|---|---|---|
| view student PII | Name, mobile, email, address | Personal data | "Student counselling" | Medium |
| export student data | All student fields | Personal data | Not documented | High |

"Flag for Review" button: marks this role for mandatory review in next compliance cycle.

---

## Tab 4 — Assignment Rules

Governs which roles can assign which other roles within an institution. Prevents privilege escalation.

### Assignment Rules Matrix

Rows = assigning role. Columns = assignable target roles.

| Assigner ↓ / Target → | Institution Admin | Co-Admin | IT Admin | Dept Head | Sr Faculty | Faculty | TA | Batch Mgr | Content Mgr | Accounts | Counsellor | Observer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Institution Admin | Cannot assign self | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Co-Admin | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| IT Admin | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Dept Head | ✗ | ✗ | ✗ | ✗ | ✓* | ✓* | ✓* | ✗ | ✗ | ✗ | ✗ | ✗ |
| All others | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

*Department Head can only assign within their assigned departments.

**Editing assignment rules:**
"Edit Rules" button opens **Assignment Rules Editor Drawer (560px):**
- Rows and columns as above, each cell is a checkbox
- System enforces: a role cannot be allowed to assign a role with more permissions than itself
- Institution Admin assignment rule is locked (can only be set by SRAV platform admin, not by institutions)

---

## Tab 5 — DPDPA Compliance

Centralised view of data privacy compliance across all institution role configurations.

### Compliance Summary Cards (4 cards)

| Card | Value |
|---|---|
| Roles with High PII Risk | Count (red if > 0 unreviewed) |
| Custom Roles Pending Review | Count (amber if > 0) |
| Institutions with Export Permission Granted | Count |
| Last Compliance Audit | Date |

### PII Permission Registry

Table of every permission that accesses student personal data:

| Permission | Data Category | DPDPA Classification | Roles with This Permission | Principle |
|---|---|---|---|---|
| view_student_pii | Name, mobile, email, address | Personal Data | Institution Admin, Co-Admin, Dept Head, Sr Faculty, Batch Manager, Counsellor | Necessary for academic management |
| export_student_data | All fields including address | Personal Data | Institution Admin, Co-Admin | Data minimisation — restricted to top roles |
| view_payment_history | Fee amount, transaction ID | Financial Data | Institution Admin, Accounts Manager | Finance purpose |
| view_student_performance | Exam scores, rank | Performance Data | All academic roles | Core academic purpose |
| download_answer_scripts | Answer images with student ID | Sensitive Academic | Institution Admin, Co-Admin, Dept Head | Restricted — review/dispute only |

### Compliance Action Items

Automated checks generating action items:

| Item | Severity | Institution Count | Action |
|---|---|---|---|
| Custom roles with undocumented PII access purpose | High | 12 institutions | Flag for review |
| Roles granting "export student data" to Faculty | High | 3 institutions | Immediate review required |
| Student Counsellor roles with batch-level PII access beyond individual | Medium | 18 institutions | Review recommended |

---

## Tab 6 — Audit Log

Immutable log of every role configuration change.

### Filters
- Date range
- Admin name
- Role name
- Action type: Role Created / Permission Added / Permission Removed / Role Archived / Assignment Rule Changed / Custom Role Flagged

### Audit Table

| Timestamp | Admin | Action | Role | Institution | Permission | Before | After |
|---|---|---|---|---|---|---|---|
| 20 Mar 14:30 | Rahul Nair | Permission Removed | Senior Faculty | Platform | create_exam | ✓ | ✗ |
| 19 Mar 11:00 | Rahul Nair | Role Created | New system role | Platform | — | — | — |
| 18 Mar 09:15 | Deepa Menon | Custom Role Flagged | Custom: "Super Faculty" | Apex Academy | DPDPA high risk | — | Flagged |

Row expand: full change detail including session ID and browser context.

Pagination: 25 / 50 / 100 per page. CSV export for compliance reporting.

---

## Modals

### New System Role Modal
- Role Name (unique, max 60 chars)
- Category: Admin / Academic / Finance / Support
- Description (required, max 300 chars)
- Restricted Role toggle (if on: institutions cannot modify this role's permissions)
- Start from: Blank / Clone existing system role
- After creation: opens Role Detail Drawer on Permission tab to configure immediately

### Edit Role Modal
- Name, Category, Description (editable)
- Impact warning: "Changing this role affects X institutions and Y users"
- Changes staged with 2FA required for permission changes (not for metadata)

### Delete Role Confirmation Modal
- Shows count of institutions and users affected
- Fallback role assignment: all affected users revert to "Faculty" by default (configurable)
- Typed confirmation: "DELETE [ROLE NAME]"

---

## Staged Changes Workflow

Permission changes to system roles do not take effect immediately — they are staged and require PM Platform 2FA confirmation before propagating to all 1,950+ institutions.

### Staged Changes Banner

When any permission has been modified in Edit Mode but not yet published:

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠ STAGED CHANGES: 3 permission changes pending publication     │
│  Affects: 2 roles · 8 institutions · ~1,200 users               │
│  [Review Changes]  [Discard All]                                │
└─────────────────────────────────────────────────────────────────┘
```

Amber banner, always visible at top of page when staged changes exist.

### Review Changes Drawer (640px)

Shows all staged changes before publication:

| Role | Permission | Change | Impact |
|---|---|---|---|
| Senior Faculty | create_exam | ✓ → ✗ (removing) | 340 Senior Faculty users lose exam creation |
| Faculty | view_results (all batches) | ✗ → ✓ (adding) | 890 Faculty users gain cross-batch result view |
| Department Head | export_student_data | ✓ → ✗ (removing) | 🛡 120 Dept Heads lose PII export permission |

Impact summary:
- Users gaining permissions: 890
- Users losing permissions: 460
- PII permission changes: 1

"Publish Changes" button → 2FA confirmation modal. After 2FA: changes applied synchronously (cached role permissions invalidated platform-wide via Redis pub/sub).

---

## Propagation and Caching

When a system role's permissions change:

1. **Staged changes published:** 2FA verified, change committed to DB
2. **Cache invalidation:** Redis pub/sub message sent to all application servers: `INVALIDATE_ROLE:{role_id}`
3. **Application server response:** All servers clear role permission cache for affected role
4. **Next request:** Each user's session refreshes permissions from DB on next API request
5. **Propagation latency:** < 30 seconds for all active sessions to reflect new permissions
6. **Audit entry:** Full change record with publisher name, timestamp, session ID

For custom institution roles: propagation is immediate on save (no staging) because they affect only one institution.

---

## Permission Dependency Rules

Some permissions have dependencies — granting one requires another to function correctly.

| Permission | Requires | Rule |
|---|---|---|
| publish_exam | create_exam | Cannot publish an exam you cannot create |
| view_results (all batches) | view_results (own batch) | Cannot have wider view without narrower |
| export_student_data | view_student_pii | Cannot export what you cannot view |
| send_bulk_sms | send_announcement (batch) | SMS is a bulk communication tool |
| enable_proctoring | create_exam | Only exam creators can enable proctoring |

When a dependency is violated in the permission matrix (enabling a permission without its prerequisite), an inline warning is shown:
"⚠ Enabling [Permission X] requires [Permission Y] to also be enabled. Both will be added."

---

## Integration Points

| Page | Integration |
|---|---|
| Page 14 — Portal Feature Config | Feature availability per plan tier constrains which permissions are accessible. E.g. if Proctoring feature is disabled for Starter plan, the `enable_proctoring` permission is hidden from Starter plan institutions regardless of role config. |
| Page 28 — Revenue & Billing | Accounts Manager role permissions determine who can access billing and payment dashboards on the institution side. |
| Page 18 — Notification Templates | Institution-side admins with `send_announcement` permission see communication features. Their notification delivery is governed by notification rules. |

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| 12 base system roles | Platform-defined templates | Institutions cannot build from scratch — ensures security baseline |
| Staging on permission changes | Same as feature config | Bulk permission change affects 25,000+ users; review step prevents accidents |
| DPDPA compliance tab | Separate from permission matrix | Compliance is a distinct concern from operational permission management |
| Anti-escalation rule | Cannot assign higher-permission role | Classic privilege escalation prevention; prevents Faculty from self-promoting |
| Observer role | Read-only, no student PII | Board members need visibility without operational or PII access |
| Custom role delta view | Show only diffs from base | Easier to audit what an institution changed vs reviewing 40+ permissions per role |
| PII permissions shield icon | Visual marker in matrix | Compliance visibility without cluttering the interface |
| Redis pub/sub propagation | < 30s permission update | Stale cached permissions create security gaps; fast propagation prevents windows of incorrect access |
| Dependency rules | Auto-add prerequisites | Without dependency enforcement, granting "publish exam" without "create exam" creates a broken UI state |
| Staged changes impact count | Shows users affected | Before publishing, PM must see the blast radius — how many users are affected in each direction |

| DPDPA risk score | Automated, not manual | 1,950+ institutions' custom roles cannot be manually reviewed; automation flags the risky ones |
