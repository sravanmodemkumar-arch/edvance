# EduForge — Module 03: Roles & Permissions (RBAC)

**Platform:** EduForge — Multi-Tenant EdTech SaaS
**Target Scale:** 5 crore (50 million) students across India
**Module:** 03 — Roles & Permissions (RBAC)
**Scope:** All institution types — School, College, Coaching, Exam Domain, TSP, B2B

---

## Table of Contents

1. Overview
2. Role Groups (11 Groups)
3. Permission Model — 3 Dimensions
4. Pre-Built Role Templates
5. Custom Roles
6. Role Hierarchy
7. Who Assigns Roles
8. Multi-Role
9. Role Assignment Rules
10. Account Creation Flows
11. Authentication & Security
12. Permission Details
13. Data Access Rules
14. Special Role Scenarios
15. Student Auto-Promotion
16. Alumni Record
17. Parent Access Rules
18. Wallets
19. Communication Permissions
20. Academic Operations
21. Compliance & Safety
22. System Operations
23. Administrative Operations
24. Financial Operations
25. Student Grievance & Support
26. Staff Operations

---

## 1. Overview

EduForge implements a Role-Based Access Control (RBAC) system built on a 3-dimension permission model. Every permission decision in the platform is evaluated across three axes simultaneously: what action the user is performing, which module they are acting upon, and what scope of data they are permitted to affect.

The RBAC system is designed to serve all institution types operating on the platform — Schools, Colleges, Coaching Centres, Exam Domain providers, Test Series Providers (TSPs), and B2B API partners — under a single unified model, while allowing each institution type to configure their internal hierarchy independently.

Key design principles:

- 11 discrete role groups span the entire user base, from EduForge platform employees down to Alumni (who hold no login access at all)
- Pre-built role templates are provided for each institution type, enabling institutions to go live immediately without manual RBAC configuration
- Custom roles can be created by Institution Admins by composing EduForge-controlled building blocks — EduForge retains control over base permission primitives at all times
- Role hierarchy is strictly enforced: no user can assign or modify a role at or above their own level
- All role assignments, changes, deletions, and approvals generate immutable audit log entries

---

## 2. Role Groups (11 Groups)

| # | Group Name | Description |
|---|---|---|
| 1 | Platform Admin | EduForge employees — internal staff with cross-tenant access. Covers engineering, support, compliance, sales, and operations teams. Access to any tenant is time-limited and logged. |
| 2 | Institution Group Admin | Administrators managing a group of institutions under one ownership entity (e.g. a chain of schools or colleges). Oversees all branches under their group. |
| 3 | School | All roles operating within a school institution — Management, Principal, Vice-Principal, HOD, Exam Cell Head, Class Teacher, Subject Teacher, Librarian, Accountant, Counsellor, Nurse, Gate Staff, Hostel Warden, and all support staff. |
| 4 | College | All roles operating within a college or university — Management, Principal, Dean, HOD, Professor, Lab Incharge, Librarian, Accountant, Hostel Warden, and all support staff. |
| 5 | Coaching | All roles operating within a coaching centre — Owner, Center Director, Academic Head, Batch Coordinator, Faculty, Accountant, and support staff. |
| 6 | Exam Domain | Roles associated with national and state competitive exam preparation — content creators, exam administrators, and domain managers for SSC, RRB, UPSC, banking, and related exams. |
| 7 | TSP (Test Series Provider) | Roles within white-label test series providers who publish mock tests and practice series to students across institutions or directly to end users. |
| 8 | Parents | Parent and guardian accounts linked to one or more student accounts. Access is institution-specific and scoped strictly to the linked student's data. |
| 9 | B2B API Partners | External organisations consuming EduForge data or functionality via the partner API. Authentication via API keys only — no UI login. |
| 10 | Students | Student accounts across all institution types. Self-registered with institution-issued credentials. |
| 11 | Alumni | Database record only — no login, no portal access. Record created automatically when a student graduates. Alumni can request documents through the institution, not through self-service. |

---

## 3. Permission Model — 3 Dimensions

Every permission in EduForge is defined by three simultaneous dimensions. A user is granted access only when all three dimensions are satisfied for a given request.

### Dimension 1 — Action

The operation being performed on a resource.

| Action | Description |
|---|---|
| View | Read-only access to records |
| Create | Add new records |
| Edit | Modify existing records |
| Delete | Remove records (always subject to 3-step confirmation) |
| Approve | Formally authorise a pending action raised by someone below |
| Export | Extract data to external format (CSV, PDF, Excel) |
| Bulk | Perform an action on multiple records simultaneously |
| Publish | Make content or results visible to intended recipients |

### Dimension 2 — Module

The functional area of the platform being accessed — e.g. Attendance, Marks, Timetable, Fee, Library, Hostel, Communication, Reports, etc.

### Dimension 3 — Scope

The data boundary within which the action applies.

| Scope | Description |
|---|---|
| Own Only | Only data directly owned by or assigned to the logged-in user |
| Class | All students and data within the user's assigned class |
| Department | All students and staff within the user's assigned department |
| Institution | All data within the user's institution |
| Group | All data across all institutions within the user's institution group |
| Platform | All data across all tenants on the EduForge platform (EduForge staff only) |

### Example — Attendance Module Permission Matrix

| Role | Action | Module | Scope |
|---|---|---|---|
| Subject Teacher | View | Attendance | Own Class (subject periods only) |
| Subject Teacher | Create | Attendance | Own Class (subject periods only) |
| Class Teacher | View | Attendance | Own Class (all periods) |
| Class Teacher | Create | Attendance | Own Class (all periods) |
| Class Teacher | Edit | Attendance | Own Class (within 24-hour correction window) |
| HOD | View | Attendance | Own Department |
| HOD | Approve | Attendance | Own Department (leave approvals) |
| Principal | View | Attendance | Institution |
| Principal | Approve | Attendance | Institution |
| Principal | Export | Attendance | Institution |
| Group Admin | View | Attendance | Group |
| Group Admin | Export | Attendance | Group |
| Platform Admin | View | Attendance | Platform |

---

## 4. Pre-Built Role Templates

EduForge ships with pre-built role templates for each institution type. When an institution is onboarded, the appropriate template is automatically applied, and the institution can go live without any manual RBAC configuration. Templates can be customised post-onboarding subject to approval workflows.

### School Template

| Role | Pre-Configured Permissions Summary |
|---|---|
| Management | Financial approvals, budget setting, staff salary edits, compliance reports, affiliation, institution-wide view |
| Principal | Full institution access, role assignment, result publication, bulk notifications, TOTP-gated critical actions |
| Vice-Principal | Student welfare, sensitive data access (with Principal approval), disciplinary records, exam coordination |
| HOD | Department attendance, marks approval, leave approval, department notifications, budget tracking |
| Exam Cell Head | Exam scheduling, seating, hall tickets, result coordination, re-evaluation approvals |
| Class Teacher | Class attendance, marks entry, homework, parent communication, disciplinary entries |
| Subject Teacher | Subject attendance, marks entry for own subject, topic management, homework |
| Librarian | Book issue/return, fine management, catalogue management (new additions need Admin approval) |
| Accountant | Fee collection, receipts, salary view (no edit), financial reports |
| Counsellor | Student welfare records, parent communication, referral coordination |
| Nurse | Medical records (hostel only), first aid log, emergency escalation |
| Gate Staff | Visitor management, student exit verification, parent photo verification |
| Hostel Warden | Hostel attendance, room assignment, hostel fees, incident reporting |
| Support Staff | Limited to own function (e.g. transport, maintenance) — no student data |

### College Template

| Role | Pre-Configured Permissions Summary |
|---|---|
| Management | Financial approvals, budget, salary edits, compliance, affiliation, institution-wide view |
| Principal | Full institution access, role assignment, result publication, critical TOTP-gated actions |
| Dean | Faculty-wide oversight, department coordination, academic policy enforcement |
| HOD | Department attendance, marks approval, leave approval, department notifications |
| Professor | Subject attendance, marks entry, topic management, exam coordination |
| Lab Incharge | Lab booking approvals, equipment tracking, lab safety records |
| Librarian | Book issue/return, fine management, catalogue management |
| Accountant | Fee collection, receipts, salary view, financial reports |
| Hostel Warden | Hostel attendance, room assignment, hostel fees, incident reporting |

### Coaching Centre Template

| Role | Pre-Configured Permissions Summary |
|---|---|
| Owner | Full institution access, financial approvals, staff management, institution-wide view |
| Center Director | Operational oversight, batch management, staff coordination |
| Academic Head | Curriculum, question bank, test series management, faculty coordination |
| Batch Coordinator | Batch attendance, batch notifications, schedule management |
| Faculty | Batch attendance, marks entry, topic management, doubt sessions |
| Accountant | Fee collection, receipts, financial reports |

### Institution Group Template

| Role | Pre-Configured Permissions Summary |
|---|---|
| Group Admin | Cross-institution view, comparative reports, group-level bulk notifications, group compliance |
| Group Accountant | Cross-institution financial reports (view only) |
| Group Compliance Officer | Audit log access, compliance reports across group |

---

## 5. Custom Roles

Institution Admins can create custom roles to accommodate unique operational structures not covered by the default templates. The following rules govern custom role creation.

### Building Blocks

- EduForge defines and controls all base permission primitives (action + module + scope combinations)
- Institution Admins compose custom roles by selecting from the approved EduForge building block catalogue
- Institutions cannot define new primitives — only combine existing ones
- EduForge can add, modify, or deprecate building blocks platform-wide, with 30-day notice to institutions

### Role Duplication

- An existing role can be duplicated to create a starting point for a new custom role
- The duplicate is given a new name and then modified by the Institution Admin
- The original role remains unchanged

### Permission Testing

- Custom roles can be activated in test mode before going live
- Test mode uses a sandboxed dummy data environment — no real student, staff, or financial data is accessible
- Institution Admin and the designated test user verify all permissions function as intended
- Test mode does not generate any operational audit logs, but the test session itself is logged

### Approval

- All custom roles — new or modified — require Principal approval before activation
- Principal reviews the full permission set in plain-language summary before approving
- Approved custom roles are logged with the approving Principal's identity and timestamp
- Management is notified when any new custom role is approved

---

## 6. Role Hierarchy

Hierarchy determines who can assign roles to whom. No user can assign a role at or above their own level. Hierarchy also governs approval chains — requests escalate upward through the hierarchy.

### School Hierarchy

```
Management
    |
Principal
    |
Vice-Principal
    |
HOD / Exam Cell Head
    |
Class Teacher / Subject Teacher / Librarian / Accountant / Nurse / Hostel Warden / Counsellor
    |
Support Staff / Gate Staff
```

### College Hierarchy

```
Management
    |
Principal
    |
Dean
    |
HOD
    |
Professor / Lab Incharge / Librarian / Accountant / Hostel Warden
    |
Support Staff
```

### Coaching Centre Hierarchy

```
Owner
    |
Center Director
    |
Academic Head
    |
Batch Coordinator
    |
Faculty / Accountant
    |
Support Staff
```

### Hierarchy Enforcement Rule

A user can assign, modify, or remove roles only at a level strictly below their own position in the hierarchy. Peers cannot assign roles to peers. Attempts to assign a same-level or higher role are rejected by the system and flagged in the audit log.

---

## 7. Who Assigns Roles

| Role Being Assigned | Who Can Assign It |
|---|---|
| EduForge Platform Admin | EduForge HR / Internal Admin only |
| Group Admin | EduForge assigns |
| Institution Admin | EduForge assigns |
| TSP Admin | EduForge assigns |
| B2B Partner | EduForge assigns (API key provisioned) |
| Principal | Institution Admin (with EduForge confirmation for first Principal) |
| Vice-Principal | Principal |
| HOD | Principal |
| Exam Cell Head | Principal |
| Dean (College) | Principal |
| Class Teacher | Principal / HOD |
| Subject Teacher | HOD (own department only) |
| Librarian | Principal / Institution Admin |
| Accountant | Institution Admin / Management |
| Counsellor | Principal |
| Nurse | Principal |
| Gate Staff | Institution Admin |
| Hostel Warden | Institution Admin / Principal |
| Assistant Hostel Warden | Hostel Warden |
| Batch Coordinator (Coaching) | Academic Head |
| Faculty (Coaching) | Academic Head / Batch Coordinator |
| Invigilator (Temporary) | Exam Cell Head |
| Event Coordinator (Temporary) | Principal |
| Substitute Teacher (Temporary) | HOD / Principal |

### Key Assignment Rules

- EduForge assigns all Group 1 (Platform Admin) roles — no institution can assign these
- EduForge assigns Group Admin and Institution Admin roles at onboarding
- Institution Admin assigns all institution-level roles, subject to hierarchy constraints
- Principal assigns VP, HOD, Dean, and Exam Cell Head directly
- HOD assigns subject teachers within their own department only — cannot assign teachers to other departments
- Exam Cell Head assigns invigilators for exam sessions (temporary roles)
- Hostel Warden assigns assistant wardens within the hostel only

---

## 8. Multi-Role

EduForge allows one person to hold multiple roles simultaneously. This is common in smaller institutions where a single staff member covers more than one function.

### How Multi-Role Works

- A user account can have any number of active roles assigned to it simultaneously
- The system evaluates all active roles at the time of each request and applies the most permissive permission that is within the user's approved scope
- "Most permissive wins" applies only within the approved scope — a broader scope cannot be inherited from a secondary role if that scope is not approved for the user's institution context

### Example

A staff member who is both a Subject Teacher and a Batch Coordinator in a coaching centre will have the union of both roles' permissions applied. They can access both subject-level teaching tools and batch coordination tools from the same login.

### Delete Override

Regardless of how many roles a user holds, all Delete actions platform-wide require the 3-step confirmation workflow. No combination of roles bypasses this requirement. Delete is never "most permissive wins" — it is always strictly controlled.

---

## 9. Role Assignment Rules

### Temporary Roles

Temporary roles are time-bound role assignments with a defined start date and end date.

- The role is configured with an explicit start date and end date at the time of assignment
- The system auto-activates the role at 00:00 on the start date
- The system auto-expires and removes the role at 23:59 on the end date
- The assigned staff member receives a 2-day advance notification before the role activates and again before it expires
- The assigning authority also receives an expiry notification 2 days before
- Common uses: Invigilator (per exam session), Event Coordinator (annual day, sports day), Annual Day coordinator, Election Officer

### Contract Staff

- All role permissions for contract staff are tied to the contract end date stored in the system
- The system sends a 30-day advance warning to the Institution Admin and Principal before contract expiry
- On the contract end date, the role auto-expires and the staff member is forced out of any active session immediately
- Contract extension requires a new role assignment with updated dates — no automatic renewal

### Delegation

- A Principal or Management-level user can temporarily delegate their authority to a designated staff member
- Delegation is strictly time-bound — the authority automatically reverts to the original holder when the delegation period ends
- The delegated authority is limited to the specified actions and does not grant the full role
- All actions performed under delegation are logged with both the delegating authority's identity and the acting user's identity
- Delegation does not transfer login credentials — the delegated person uses their own account

### Substitute Teacher

- When a teacher is absent, a substitute teacher can be assigned to cover their classes for a defined period
- The substitute has access to the same class and subject data as the original teacher for the substitution period
- Both the original teacher (if on leave with view-only access) and the substitute have simultaneous access — no lockout of the original teacher
- The substitute role auto-expires when the substitution period ends
- Attendance entries made by the substitute are logged with the substitute's identity

### Role Change Audit

Every role change — assignment, modification, removal, expiry — generates the following:

- An immutable audit log entry with: changed-by identity, changed-at timestamp, previous role state, new role state, reason if provided
- An email notification to the staff member whose role was changed
- The staff member must acknowledge the role change notification within 48 hours — unacknowledged changes are flagged to the HOD and Principal
- Role changes can take effect immediately or be scheduled for a future date (useful for promotions, transfers, academic year transitions)
- Scheduled future-date changes are visible to the assigned staff member in advance

---

## 10. Account Creation Flows

### All Account Types — Summary Table

| Account Type | Created By | First Credential | Verification Method |
|---|---|---|---|
| EduForge Staff | EduForge HR | HR-generated password | SMS OTP |
| Group Admin | EduForge | EduForge-generated credentials | SMS OTP |
| Institution Admin | EduForge | EduForge-generated credentials | SMS OTP |
| TSP Admin | EduForge | EduForge-generated credentials | SMS OTP |
| B2B Partner | EduForge | API key only | No UI login — API key authentication only |
| Staff (all institution types) | Institution Admin | Employee ID as first-time password | Email/SMS OTP + TOTP setup |
| Student | Self-register | Registration number as first-time password | Email OTP |
| Parent | Self-register | Student's registration number as first-time password | Email OTP + Photo mandatory |

### Registration Page Flow (All Staff and Student Accounts)

This flow applies universally to all accounts that involve a first-login registration step.

```
Step 1: User enters phone number / email + first-time password
        (Employee ID for staff / Registration Number for student/parent)
        |
        V
Step 2: System validates credentials against DB record
        User is redirected to Registration Page
        All personal details pre-filled from DB (read-only — cannot be edited here)
        |
        V
Step 3: User sets new password + confirms new password
        Password policy enforced immediately
        |
        V
Step 4: Email OTP / SMS OTP verification
        OTP sent to registered contact
        |
        V
Step 5: TOTP setup (Staff only)
        QR code displayed — user scans with Google / Microsoft Authenticator
        User enters TOTP code to confirm setup
        |
        V
Step 6: Account activated — user lands on role-specific home page
        If any pre-filled details are incorrect: user shown a contact card
        with the institution's admin contact — no self-correction permitted
```

### Parent Registration — Specific Rules

- Parent enters their phone number and the student's registration number as the first-time password
- Pre-filled fields: parent name, email address, phone number (all read-only — sourced from student admission record)
- Photo upload is mandatory during registration — this photo is used for gate verification when collecting the child
- Email OTP is compulsory — SMS OTP is not sufficient for parent accounts
- Maximum 3 OTP requests per day per parent account
- Forgot password: resolved via email OTP only (not SMS)
- If the pre-filled details are wrong, the parent must contact the institution admin — no self-service correction

### Student Registration — Specific Rules

- Student enters their email / phone and registration number as the first-time password
- Pre-filled fields: full name, date of birth, class, roll number (all read-only)
- Email OTP is compulsory
- No TOTP required for student accounts
- Maximum 3 OTP requests per day per student account

---

## 11. Authentication & Security

### Login Methods by Role

| Role Group | Login Method | 2FA Required |
|---|---|---|
| EduForge Platform Admin | Phone/Email + Password + TOTP | Yes — TOTP mandatory |
| Group Admin | Phone/Email + Password + TOTP | Yes — TOTP mandatory |
| Institution Admin | Phone/Email + Password + TOTP | Yes — TOTP mandatory |
| Principal | Phone/Email + Password + TOTP | Yes — TOTP mandatory |
| All Teaching Staff | Phone/Email + Password + TOTP | Yes — TOTP mandatory |
| All Non-Teaching Staff | Phone/Email + Password + TOTP | Yes — TOTP mandatory |
| Hostel Warden | Phone/Email + Password + TOTP | Yes — TOTP mandatory |
| Gate Staff | Phone/Email + Password + TOTP | Yes — TOTP mandatory |
| Students | Phone/Email + Password | No 2FA |
| Parents | Phone/Email + Password | No 2FA |

### TOTP Setup

- TOTP infrastructure is auto-provisioned by EduForge when an institution is created — no manual configuration required by the institution
- Staff scan a QR code displayed on first login using Google Authenticator or Microsoft Authenticator
- TOTP is required to complete first login — it cannot be skipped
- EduForge supports standard TOTP (RFC 6238) — any TOTP-compatible authenticator app works
- Cost to institution: Rs. 0 — TOTP is included in all EduForge plans

Lost Phone Recovery Process:

```
Staff reports lost phone to Admin
        |
        V
Admin raises a TOTP reset request in the platform
        |
        V
Principal approves the reset request
        |
        V
EduForge support team executes the reset
        |
        V
Staff sets up TOTP again on new device at next login
```

### Password Policy

| Rule | Requirement |
|---|---|
| Minimum length | 8 characters |
| Maximum length | 32 characters |
| Uppercase | At least 1 uppercase letter |
| Number | At least 1 numeric digit |
| Special character | At least 1 special character |
| Expiry | Every 90 days |
| Reuse | Cannot reuse any of the last 5 passwords |
| First login | Must change on first login — first-time password cannot be retained |

### Biometric Login (Mobile App Only)

- Available on iOS and Android mobile app — not available on the web portal
- Supported methods: Fingerprint (Touch ID) and Face ID
- First-time biometric setup requires Password + TOTP authentication — biometric cannot be enabled without completing standard login first
- If biometric fails 3 consecutive times, the app automatically falls back to Password + TOTP — biometric is temporarily disabled until the user re-authenticates with full credentials
- Biometric is a convenience layer — it does not bypass the underlying session security

### Session & Timeout

| Rule | Value |
|---|---|
| Session timeout (all roles) | 10 minutes of inactivity |
| Warning before timeout | Shown at 8 minutes of inactivity |
| Active exam exception | No timeout during an active ongoing exam session |
| Student devices | 1 device only (1 active session at a time) |
| Parent devices | 1 device only |
| Staff devices | 2 devices maximum (1 mobile + 1 PC/laptop) |
| Session reset trigger | Any user activity resets the inactivity timer |

### Account Lockout

| Rule | Detail |
|---|---|
| Failed attempt threshold | After every 3 failed login attempts, an EduForge verification challenge is presented (CAPTCHA-style or email OTP challenge) |
| Account unlock | Only EduForge Admin can unlock a locked account — institution admins and principals cannot self-unlock |
| OTP limit — Admin/Principal | Maximum 10 OTPs per day |
| OTP limit — All others | Maximum 3 OTPs per day |

### IP Restrictions (Staff)

- All staff accessing the platform from a PC or laptop must use a device with a pre-approved IP address
- IP whitelist approval process:

```
Staff requests new device/IP
        |
        V
Principal reviews and approves the request
        |
        V
Management gives final approval
        |
        V
IP added to whitelist — device can now log in
```

- Students and parents are not subject to IP restrictions — they can access the platform from any network
- Full audit log is maintained of all approved IP addresses, who approved them, and when

### Time-Based Login Restrictions

| Role | Default Login Hours |
|---|---|
| All staff (default) | School/institution operating hours only |
| Students | 24 hours / 7 days |
| Parents | 24 hours / 7 days |
| Hostel Warden | 24 hours / 7 days (by default) |
| Principal | 24 hours / 7 days (by default) |
| Institution Admin | 24 hours / 7 days (by default) |

- Principal and Institution Admin can grant 24/7 access to specific staff members on a case-by-case basis
- All time-restriction grants are logged

### Login History

- Each user can view their own login history for the last 30 days
- Suspicious logins (new location, unusual time, new device) are highlighted in red in the login history view
- Admin and Principal can view login history for all staff under their institution
- Students and parents can only view their own login history

### New Location Alert

When a login is detected from a city that has not previously been used for that account:

| Role | Alert Type |
|---|---|
| Admin / Principal | SMS alert |
| All Staff | Email alert |
| Students / Parents | In-app notification |

- All users see a "This wasn't me" button in the alert
- Pressing "This wasn't me" immediately locks the account and sends an automatic notification to EduForge security team
- EduForge initiates investigation and informs the Institution Admin and Principal

---

## 12. Permission Details

### Delete — 3-Step Confirmation (Platform-Wide)

All delete actions anywhere on the EduForge platform — regardless of the record type or the role performing the action — follow the mandatory 3-step confirmation workflow.

```
Step 1: Staff member raises a delete request with a mandatory written reason
        System stores reason + requester identity + timestamp
        |
        V
        HOD / Supervisor reviews within 3 working days
        Approves or rejects with reason
        |
        V
Step 2: HOD / Supervisor approval logged
        |
        V
        Principal / Institution Admin gives final approval within 3 working days
        |
        V
Step 3: Principal / Admin confirms via Email OTP
        Deletion executes only after OTP validation
        Original record retained in audit archive even after deletion
```

- Each step has a 3-working-day window. If any step is not completed within 3 working days, the request expires automatically and must be re-raised
- No delete request can be self-approved — the requester cannot be any of the approvers

### Bulk Export

Bulk export is restricted to specific authorised use cases only:

- Government compliance reporting
- Financial audit (internal or external)
- Institution exit from the EduForge platform

Bulk export workflow:

- 3-step approval (same structure as Delete)
- TOTP confirmation from the final approver
- Accessible from Laptop/PC only — mobile export is blocked
- All exported files are watermarked with the exporting user's name, role, timestamp, and institution name
- Every export is logged permanently in the audit trail

### Print Permissions

| Record Type | Who Can Print | Additional Requirement |
|---|---|---|
| Student report card | Principal / Class Teacher | TOTP confirmation |
| Fee receipt | Accountant | TOTP confirmation |
| Attendance report | HOD / Principal | TOTP confirmation |
| Mark sheet | Exam Cell Head / Principal | TOTP confirmation |
| Transfer Certificate | Institution Admin / Principal | TOTP + Principal approval |
| Character Certificate | Principal only | TOTP confirmation |
| Salary slip | Accountant (staff copy) / Staff (own copy) | TOTP confirmation |
| Compliance report | Principal / Management | TOTP confirmation |

- All print operations generate a watermarked output (user name, role, timestamp, institution)
- Print is available from Laptop/PC only — mobile printing is blocked for all sensitive documents

### Financial Approvals

All financial actions on the platform — without exception — require Management and Principal co-authorisation. This covers:

- Fee waivers and concessions
- Fee refunds
- Salary changes and increments
- Scholarship disbursements
- Budget reallocation

All financial approval workflows:

- Follow the same 3-step confirmation structure
- Require TOTP at the final approval step
- Can only be initiated or approved from Laptop/PC
- Generate a permanent audit log entry

### Marks Entry & Editing

| Action | Who Can Perform | Restriction |
|---|---|---|
| Marks entry | Subject Teacher | Own subject only — cannot enter marks for another teacher's subject |
| Marks edit request | Subject Teacher | Raises a formal edit request with reason |
| Edit approval — Level 1 | HOD | Approves or rejects within 3 working days |
| Edit approval — Level 2 | Exam Cell Head | Approves after HOD |
| Edit approval — Level 3 | Principal | Final approval — TOTP required |
| Maximum edits | — | Maximum 2 edits per student per exam across all subjects |
| TOTP | — | Required from all three approvers (HOD, Exam Cell Head, Principal) |

### Results Publication

- The Principal grants publication permission to a specific named person (e.g. Exam Cell Head) before each result cycle
- That designated person uses TOTP to confirm and execute publication
- Results are visible to students and parents only after publication — no early or partial visibility
- Results cannot be unpublished once published — any corrections require a Marks Correction workflow followed by a re-publication with fresh approval

### Bulk Notifications

| Scope | Who Can Send |
|---|---|
| School-wide / Institution-wide | Principal / Institution Admin only |
| Department-wide | HOD only |
| Class-wide | Class Teacher only |
| Bulk WhatsApp | Institution Admin only — TOTP + 3-step approval |

- A preview of the notification (including estimated WhatsApp cost if applicable) is shown to the sender before confirmation
- Once confirmed and sent, notifications cannot be unsent or recalled
- All bulk notifications are logged with sender identity, recipient count, content, and timestamp

### Search Permissions

| Role | Search Scope |
|---|---|
| Class Teacher | Own class students only |
| HOD | Own department students and staff only |
| Principal / Institution Admin | All students and staff in the institution |
| Accountant | Search by fee status only — no personal data beyond payment records |
| Counsellor | Own assigned students only |
| Students | Own data only |
| Parents | Own linked student's data only |

---

## 13. Data Access Rules

### Sensitive Data — Restricted Access

| Data Category | Who Can Access |
|---|---|
| Student photos, home address, personal contact details | Principal + Vice-Principal only by default |
| Student welfare and counselling records | Counsellor + Principal only |
| Other staff requesting sensitive data | Requires VP grant + Principal approval — logged permanently |
| Medical records (hostel residents) | Nurse + Principal + Special Education Teacher only |
| Salary data — own slip | Each staff member sees their own slip only |
| Salary data — all staff | Accountant can view — cannot edit |
| Salary data — edit | Management only — 3-step approval + TOTP |

### Data Minimization

Each role is served only the data fields required for their function. This is enforced at the database level using Row-Level Security (RLS) — roles do not see excess data even if they attempt to query it directly.

| Role | Data Accessible |
|---|---|
| Subject Teacher | Student name, roll number, attendance for own subject, marks for own subject |
| Class Teacher | Full class student list, all attendance, marks summary, parent contact |
| HOD | Department-wide student performance, staff attendance, department budget |
| Accountant | Fee records, payment history, salary records (view) |
| Librarian | Student library record, borrowed books, fines |
| Gate Staff | Student photo, registered parent photo, exit permissions |
| Nurse | Student medical record (hostel), emergency contact |
| Principal | All institutional data within scope |
| Platform Admin | Cross-tenant data (time-limited, reason required, fully logged) |

### Minor Data Protection

- Parent/guardian consent is required before any minor student's personal data is shared with any party outside the institution
- Every access to a minor's personal data by any staff member generates an automatic audit log entry — this logging cannot be disabled for minor records
- POCSO auto-flag: If an adult male staff member accesses personal data of a minor female student outside school operating hours, the system automatically generates an alert and flags the access for review by the Principal and EduForge compliance team

### Student Always Sees Own Data

| Data | When Visible to Student |
|---|---|
| Attendance record | Always visible |
| Timetable | Always visible |
| Certificates (earned) | Always visible |
| Exam results | Only after Principal-approved publication |
| Fee details | Visible to parents only — students do not see fee records |

### Device-Based Restrictions

| Action Type | Laptop/PC | Mobile / Tablet |
|---|---|---|
| View | Allowed | Allowed |
| Create | Allowed | Allowed (limited forms) |
| Edit | Allowed | Allowed (limited forms) |
| Delete | Allowed (with 3-step workflow) | Not allowed — request only |
| Bulk actions | Allowed | Not allowed |
| Export | Allowed | Not allowed |
| Admin operations | Allowed | Not allowed |
| Financial approvals | Allowed | Not allowed |
| TOTP-gated actions | Allowed | Not allowed (web) / Allowed (app with biometric) |

### Screenshot / Copy-Paste Prevention

| Control | Where Applied |
|---|---|
| Screenshot blocking | Mobile app — sensitive screens (student data, marks, financial records, medical) |
| Watermarking | Web portal — sensitive data pages are watermarked with user identity + timestamp |
| Copy-paste disabled | Sensitive fields on web and mobile: Aadhaar number, phone number, home address, medical records |
| Admin / Principal exemption | Admin and Principal can copy sensitive fields — every such action is logged automatically |

### Role-Based UI

- Menu items and features are not rendered at all for users who lack the corresponding permission — they are not greyed out or disabled, they are entirely absent from the interface
- If a user navigates to a URL for which they have no permission (e.g. via a saved link): they see a unified "You do not have permission to access this page" screen, with a "Request Access" button that routes a formal access request to their HOD and Principal
- If a user logs in and has no role assigned yet: they see a unified "No permissions assigned to your account" screen with their institution admin's contact information
- Each role is configured with a distinct home page that appears immediately after login — the system routes to the correct home page automatically

---

## 14. Special Role Scenarios

### BGV-Linked Permissions

All staff accounts have a BGV (Background Verification) status that directly governs their data access level.

| BGV Status | Access Level |
|---|---|
| BGV Pending (not yet initiated) | Restricted — can access own role's operational tools but cannot access any student personal data |
| BGV In Progress | Restricted — same as Pending |
| BGV Cleared | Full access per role |
| BGV Failed | Immediate access block + forced logout from all active sessions |

- BGV status decisions are made by VP or Principal — this is a human decision, not an automatic system decision
- BGV failure triggers an automatic alert to EduForge compliance team in addition to forcing logout

### Divorced Parent / Court Order

- Court-ordered custody or access restrictions affecting a parent's right to information about a student are managed manually by the Institution Admin
- The admin uploads the supporting document (court order) and marks the restricted parent's account
- The restricted parent's account is blocked from accessing the linked student's data — they can still log in but see no student information
- The institution does not communicate restriction status to the restricted parent through the platform
- Full audit log of all access attempts by the restricted parent is maintained

### Cross-Tenant Rules

- A student can be simultaneously enrolled in School A (one tenant) and Coaching Centre B (another tenant)
- Each institution's data is fully isolated — the student's School A data is not visible from Coaching Centre B and vice versa
- A parent linked to a student sees only the data of the institution through which they registered
- If two children of the same parent are enrolled in the same institution, one parent account shows both children's data — no separate accounts required

### Staff + Parent Same Account

- A staff member who is also a parent of a student in the same institution holds one account with two roles
- A "Switch View" button in the interface allows them to toggle between their staff view and their parent view
- Strict separation is enforced: when operating in the staff role, the user cannot access their own child's data through the staff interface
- All access to their child's data must occur through the parent view only
- Any attempt to access own child's records through the staff role is blocked and logged

### Transfer Student

- A student transferring from Institution A to Institution B gets a fresh account at Institution B
- The old account at Institution A becomes read-only — the student can log in to request documents (TC, marksheet, certificates) but cannot make any changes
- No student data is automatically transferred between institutions — tenants are isolated
- If the receiving institution needs historical records, the student provides physical or digitally certified documents

### CWSN Student (Children With Special Needs)

- CWSN flag is set by the Institution Admin at the time of admission or later by Principal
- Triggers automatic assignment of a Special Education Teacher to the student's record
- Additional exam time is automatically granted in the exam scheduling system when the flag is set
- Medical records for CWSN students: accessible only by Nurse + Principal + Special Education Teacher
- Accessibility settings (font size, high contrast, screen reader, animations off) are pre-configured on the student's account at the time of flag activation

### International Student

- International student flag is set by the Institution Admin at admission
- Passport number and visa expiry date are stored in the student's record
- System sends a 60-day advance alert to Institution Admin and Principal before visa expiry
- Passport and visa documents: accessible only by Admin and Principal
- No automated immigration action is taken — the alert is for manual follow-up by the institution

---

## 15. Student Auto-Promotion

At the end of each academic year, students are promoted to the next class through a 3-level approval workflow. No student is promoted without completing all three steps.

### Step 1 — Class Teacher Assessment

Class Teacher reviews each student in their class and marks one of three outcomes:

- Pass — student has met all criteria for promotion
- Fail — student has not met promotion criteria but is not formally detained
- Detained — student is formally detained and will repeat the same class

Class Teacher submits the assessment for all students in their class before moving to Step 2.

### Step 2 — HOD Review

HOD reviews the Class Teacher's assessments for all classes within their department. HOD can:

- Accept the assessment as submitted
- Flag specific students for re-review and return to the Class Teacher with comments

HOD approves the class-wise assessment once satisfied.

### Step 3 — Principal Final Approval

Principal reviews the full institution-wide promotion list. Once the Principal gives final approval:

- The system runs an overnight batch process that promotes all approved students to the next class
- Class Teacher role assignments are automatically updated to reflect the new class composition
- Detained students remain in the same class — their records are updated to reflect the repeated year

### Batch System Rules

- The batch will not run if any student in any class still has a Pending status — all students must have a final outcome before the batch executes
- The batch runs overnight to avoid daytime performance impact
- Class Teacher role assignments for the new academic year are updated automatically as part of the same batch
- Alumni records are automatically created for students in the final graduating class/year as part of the promotion batch

---

## 16. Alumni Record

Alumni hold no login credentials and have no access to the EduForge platform. They exist solely as database records for document issuance and institutional history.

### Alumni Record Fields

| Category | Fields |
|---|---|
| Personal | Full Name, Date of Birth, Gender, Phone Number, Email Address, Current Address, Photo, Aadhaar Number (AES-256 encrypted) |
| Academic Identity | Admission Number, Roll Number, Class / Course, Stream / Branch |
| Academic History | Year of Admission, Year of Passing, Board / University Name, Marks / Percentage, CGPA (if applicable), Division |
| Documents Issued | Transfer Certificate (TC) Issued — Yes/No, Marksheet Issued — Yes/No, Character Certificate Issued — Yes/No, Migration Certificate Issued — Yes/No |

### Alumni Document Request Flow

```
Former student contacts the institution through phone, email, or in-person
        |
        V
Institution Admin searches for the alumni record in the platform
        |
        V
Admin generates the requested document (TC, marksheet, character certificate, etc.)
        |
        V
Document sent via email or WhatsApp link
        |
        V
Link expires after 7 days — no permanent external hosting
        |
        V
Document issuance logged in the alumni record
```

Alumni records are permanent and are never deleted from the platform, even after the institution exits EduForge.

---

## 17. Parent Access Rules

### Parent Access by Institution Type

| Institution Type | Parent Access |
|---|---|
| School | Full parent access — attendance, marks, timetable, fees, communication |
| College | Full parent access — attendance, marks, timetable, fees, communication |
| Coaching Centre | Full parent access — attendance, marks, timetable, fees, communication |
| Institution Group | Per-institution access for each linked institution |
| National Exam (SSC, RRB, UPSC, banking, competitive) | Student only — no parent access for online exam platforms |

### When Parent Access Ends

Parent access to a student's data ends only under these specific conditions:

- Student graduates from the institution — Alumni record is created and parent access is removed automatically
- Student explicitly requests removal of parent access through the student's own account — Institution Admin reviews and implements
- Institution Admin removes parent access manually (requires written reason and is logged)

Parent access is never removed automatically for any other reason — including the student reaching the age of 18. If the student wishes to remove parental access upon turning 18, they must raise the request through the student account.

### Parent Gate Verification

When a parent arrives at the institution gate to collect their child:

```
Gate Staff enters the student's name in the Gate Management screen
        |
        V
System displays the photos of all registered parents/guardians for that student
        |
        V
Parent sends a live photo through the EduForge mobile app
        |
        V
Gate Staff compares the live photo with the registered photo
        |
        V
If matched: Gate Staff authorises student exit — logged in system
If not matched: Student not released — Gate Staff alerts the institution admin
```

### Court-Restricted Parent at Gate

If a parent with a court access restriction attempts to collect the student:

- System flags the access attempt when the gate staff searches for the student — shows restriction alert
- Gate Staff is instructed to not release the student
- Principal is automatically alerted via SMS
- Attempt is logged permanently

### Alternate Pickup Registration

If a parent wants someone else (relative, driver, etc.) to collect the child on a specific day:

```
Parent registers the alternate pickup person through the mobile app
        (Photo of alternate person required)
        |
        V
Admin reviews the request
        |
        V
Principal approves
        |
        V
Alternate person added to gate list for the specified date/time window only
        |
        V
Gate Staff follows the same photo verification process
```

---

## 18. Wallets

### Wallet Summary

| Wallet | Managed By | Purpose |
|---|---|---|
| WhatsApp Wallet | Management | Funds all WhatsApp messages sent by the institution through EduForge |
| SMS Wallet | Management | Funds all SMS messages sent by the institution through EduForge |
| Student Canteen Wallet | Parent tops up | Student uses for canteen purchases |
| Student General Wallet | Parent tops up | Student uses for general school purchases (stationery, event fees, etc.) |
| EduForge Subscription Wallet | Management | Funds EduForge platform subscription and add-ons |
| Refund Wallet | Admin manages | Holds approved refunds pending disbursement to parent |

### Student Wallet Features

- Parent tops up the student's canteen and general wallets via Razorpay or PhonePe — no other payment methods accepted for student wallets
- Parent sets a daily spending limit per wallet — the system blocks transactions that exceed the daily limit
- Parent can freeze the student wallet instantly from the mobile app — no admin interaction required
- Every transaction (debit and credit) is visible to the parent in real-time
- Parent receives an instant push notification for every transaction on the student's wallet
- Monthly summary and daily summary are auto-generated and visible to the parent in the app

### WhatsApp Wallet

- The institution can only top up the WhatsApp wallet through EduForge — direct Whatsapp Business API top-ups are not allowed
- Low balance alert is sent to Admin, Principal, and Management when the wallet falls below a configurable threshold
- Before every bulk WhatsApp send, the platform shows the estimated cost and the balance remaining — the sender must explicitly confirm before messages are sent
- Per-message cost is shown transparently at the time of send

---

## 19. Communication Permissions

### Who Can Message Whom

| Sender | Can Message | Restriction |
|---|---|---|
| Teacher | Parent of own class students | During school hours only |
| Teacher | Own class students | During school hours only |
| Class Teacher | All parents in own class | During school hours only |
| HOD | All staff in own department | No restriction |
| HOD | Parents of own department students | During school hours only |
| Principal | All staff | No restriction |
| Principal | All parents | No restriction |
| Institution Admin | All staff | No restriction |
| Institution Admin | All parents | No restriction |
| Parent | Teacher of linked student | Reply only — cannot initiate a fresh conversation thread |
| Parent | Institution (general) | Via support ticket only |
| Student | Teacher | During school hours — query/question format only |

- The message button is hidden from the parent and student interface outside school hours — it is not greyed out, it is not visible
- Emergency messages sent by Principal or Admin bypass the school hours restriction — these are flagged as "Emergency" and are delivered immediately

### Read Receipts

- Read receipts are mandatory on the platform — they cannot be disabled by any user or admin
- Messages not read within 24 hours are flagged with an unread indicator visible to the sender
- For broadcast messages (one-to-many): the Admin / sender sees only the total read count — individual read status is not shown to preserve recipient privacy

### Message Security

| Control | Detail |
|---|---|
| Forwarding | Messages cannot be forwarded outside the EduForge platform |
| Copy-paste | Message text cannot be copy-pasted from the messaging interface |
| Screenshot | Blocked on mobile app for all message threads |
| Web watermark | All message screens on the web portal are watermarked with the viewing user's identity |

### Broadcast Groups

| Broadcast Sender | Audience |
|---|---|
| Principal / Institution Admin | All parents in the institution |
| Principal / Institution Admin | All staff in the institution |
| HOD | All staff in own department |
| Class Teacher | All parents of own class students |

- Broadcast is one-way — recipients cannot reply to the broadcast thread. They can reply only to the sender's direct message thread individually
- Institution-wide broadcast requires TOTP confirmation from the sender before dispatch
- Once sent, broadcasts cannot be recalled or deleted

---

## 20. Academic Operations

### Topic Access Control

- A subject teacher teaches a topic in class and marks it as "Completed" in the platform
- The system then enables the corresponding notes, resources, and assessments for that topic for the students in that class
- Students cannot access topic materials until the teacher has explicitly marked the topic as completed — no pre-access
- Platform generates per-student access reports showing which materials were accessed and corresponding test scores

### Question Paper Security

- Question papers are auto-generated from the EduForge question bank by Python based on the pattern configured by the Exam Cell Head
- Three sets are generated: Set A, Set B, Set C
- No faculty or non-authorised staff member can view the question paper at any stage before the exam
- Only the Principal or a specifically approved person can view the paper before distribution

Offline exam:

- Paper is stored encrypted on the platform
- Printed on the day of the exam — print is TOTP-gated
- Printed sets are distributed randomly to students (not sequentially)

Online exam:

- Paper remains encrypted on the platform until 5 minutes before the scheduled exam start time
- An approved person uses TOTP to unlock/decrypt the paper at the 5-minute mark
- Every view of the decrypted paper is logged with the viewer's identity and timestamp

### Hall Ticket & Seating Allocation

- Room and seating details (room numbers, capacity per room) are entered once and stored permanently — no need to re-enter each exam cycle
- Each exam cycle: the system presents the stored room list and prompts the Exam Cell Head with "Update or Proceed?" before generating allocations
- Python auto-allocates student seats based on room capacity and student count
- Principal reviews and approves the seating plan
- Students are notified with their own room and seat number only — they do not see the full seating plan

### Answer Script Access

| Phase | Who Can View |
|---|---|
| During evaluation | Evaluator (for their own subject only) |
| After results published | Student (own script only) |
| After results published | Parent (linked student's script only) |

- Script view is view-only — download is not available, screenshot is blocked
- The viewing window is open for 30 days after result publication — after 30 days, scripts are archived and no longer accessible via the platform
- Re-evaluation requests can be raised directly from the script view screen

### Re-evaluation

- Student or parent raises a re-evaluation request from within the platform (from the answer script view screen or from the results screen)
- Request goes to: Exam Cell Head → Principal (for approval)
- Once approved, a second evaluator is assigned — this evaluator sees only the specific question(s) under re-evaluation, not the full script
- Maximum 1 re-evaluation request per subject per exam per student
- The re-evaluation result is final — no further appeal within the platform

### Grace Marks

| Grace Marks Range | Approval Level |
|---|---|
| Up to 2% | HOD approves |
| Up to 5% | Principal approves |
| Above 5% | Management gives final approval |

- TOTP is required at each approval level
- Grace marks decisions are permanently logged with the approving authority's identity

### Marks Correction

Refer to Section 12 — Permission Details (Marks Entry & Editing) for the full workflow.

---

## 21. Compliance & Safety

### POCSO Compliance

- Auto-alert: if an adult male staff member accesses personal data of a minor female student outside the institution's operating hours, the system generates an automatic flag and sends an alert to the Principal and EduForge compliance team
- Flagged access is automatically locked pending human review — the Principal decides whether to unlock or escalate
- Unverified visitor cannot be permitted to meet a minor student without explicit Principal approval — gate staff cannot override this
- Any staff member who fails BGV is immediately blocked and forced out of all active sessions
- Each institution must have a POCSO officer assigned — this is tracked in the platform
- EduForge maintains a dedicated POCSO compliance team that is automatically notified for all POCSO flags
- All POCSO-related audit logs are retained permanently — they are never deleted or archived out of reach

### Data Breach Response

```
System detects unusual data access pattern (volume, timing, geographic anomaly)
        |
        V
Affected accounts are locked automatically
        |
        V
EduForge security team is notified instantly (automated alert)
        |
        V
Institution Admin + Principal are notified
        |
        V
Full access logs for the affected period are pulled for investigation
        |
        V
Principal decides what to communicate to students and parents and when
        EduForge does not contact students or parents directly
        |
        V
Post-investigation report filed and retained permanently
```

### Right to Erasure (DPDPA Compliance)

```
Student or parent raises a right-to-erasure request through the app
        |
        V
Institution Admin reviews the request
        |
        V
EduForge legal team approves the erasure
        |
        V
Data deleted from active operational database
        |
        V
Cold archive purged within 30 days of approval
```

Exceptions — the following records cannot be erased regardless of erasure requests:

- Financial records (fee receipts, payment history): retained for 7 years per tax law requirements
- Government-mandated exam records: retained permanently

### Consent Management

| Data Sharing Type | Consent Required From |
|---|---|
| Student data shared with parent | Parent consent (given at registration) |
| Student data shared with government body | Principal + Management approval — no individual consent required (legal compliance) |
| Student data shared with third-party vendor | Parent consent + Principal approval + EduForge legal team approval |
| Staff data shared with third party | Staff written consent + Management approval |
| Anonymous aggregated data (no PII) | No consent required |

- Consent can be withdrawn within 24 hours of being granted — after 24 hours, withdrawal requires a formal request through the Institution Admin
- Full audit trail of all consent grants and withdrawals is maintained permanently

### Whistleblower Protection

- Any staff member can submit an anonymous report of misconduct, safety concern, bullying, harassment, or POCSO-related issue directly to the EduForge compliance team
- The reporter's identity is protected within the platform — it cannot be revealed to the institution or any other party without a formal court order
- A case number is issued to the reporter at the time of submission — they can use this to track the status of their report
- Every report is investigated by the EduForge compliance team
- Reporter is protected from institutional retaliation — any retaliation reported to EduForge triggers a formal compliance response against the institution

### Annual Permission Review

- At the start of each academic year, the system automatically sends a reminder to the Principal and Institution Admin to review all staff role assignments
- Principal reviews and confirms each staff member's role is current and correct
- Management approves the final reviewed role list
- If the review is not completed within 30 days of the reminder, EduForge is automatically notified and the Platform Admin team follows up with the institution

---

## 22. System Operations

### Maintenance Mode

| Who Can Activate | Scope |
|---|---|
| Institution Admin + Principal jointly | Their institution only — both must approve |
| EduForge Super Admin | Any individual institution or the entire platform |

- Scheduled maintenance: 24-hour advance notice sent to all affected users
- Emergency maintenance: Immediate activation — notification sent simultaneously with activation
- During maintenance mode, all active sessions are terminated gracefully (users see a maintenance notice)
- Maintenance mode cannot be activated by either Institution Admin or Principal alone — joint approval required for institution-level maintenance

### EduForge Super Admin Access to Tenant

EduForge Super Admin access to any tenant (institution) is strictly governed:

| Rule | Detail |
|---|---|
| Pre-access approval | EduForge Manager must approve the access request before it is granted |
| Reason required | Super Admin must enter a written reason for every access request |
| Session duration | Maximum 2-hour sessions — access automatically expires after 2 hours |
| Institution notification | The institution is never notified that a Super Admin is accessing their data |
| Logging | Every session is logged permanently: Super Admin identity, reason, start time, end time, actions performed |
| Review | EduForge Management reviews the monthly Super Admin access report |

### Audit Log Retention — 3-Tier Storage

| Tier | Period | Storage |
|---|---|---|
| Hot (immediately queryable) | Last 90 days | PostgreSQL operational read replica |
| Warm (queryable with slight delay) | 90 days to 1 year | Compressed PostgreSQL archive |
| Cold (archive — queryable on demand) | 1 year to 7 years | Cloudflare R2 object storage |

- Audit logs are stored in a separate, isolated database — they are never stored in or mixed with the operational database
- Only meaningful actions are logged — routine reads are not logged to prevent log bloat. Logged events include: role changes, deletions, approvals, logins (new device/location), financial actions, data exports, TOTP-gated actions, access to sensitive data
- Python runs a monthly auto-archiving job that moves logs from Hot to Warm and from Warm to Cold on schedule

### Auto-Generated Reports

| Report | Frequency | Generated By |
|---|---|---|
| Attendance report (student) | Weekly + Monthly | Python batch |
| Attendance report (staff) | Monthly | Python batch |
| Fee collection report | Monthly | Python batch |
| Student academic performance | Monthly + Yearly | Python batch |
| Subject / Chapter / Topic-wise results | Per exam cycle | Python batch |
| Online test participation | Per test | Python batch |
| Result comparison (year-on-year) | Yearly | Python batch |
| Rank report | Per exam | Python batch |

Report Visibility by Role:

| Report | Who Sees It |
|---|---|
| Attendance (student) | Class Teacher, HOD, Principal, Parent (own child), Student (own) |
| Attendance (staff) | HOD (own dept), Principal, Institution Admin |
| Fee collection | Accountant, Principal, Management |
| Student performance | Class Teacher, HOD, Principal, Parent (own child), Student (own) |
| Subject / Topic results | Subject Teacher (own), HOD, Exam Cell Head, Principal |
| Online test participation | Faculty (own batch), Academic Head, Principal |
| Year-on-year comparison | Principal, Management, Group Admin |
| Rank report | Principal, HOD, Exam Cell Head, Student (own rank), Parent (own child) |

### Dashboard Customisation

- Each role has a default dashboard configured and deployed by EduForge at the time of institution setup
- Users can rearrange dashboard widgets using drag-and-drop within their permitted widget set
- Mandatory widgets (defined by EduForge for each role) cannot be removed from the dashboard — they can be repositioned but not hidden
- Users cannot add widgets that correspond to permissions they do not hold
- Principal can set an institution-wide default dashboard layout for any role in their institution — overrides individual user customisation for that role

### Language & Accessibility

Supported Languages:

- English (default)
- Hindi, Tamil, Telugu, Kannada, Malayalam, Marathi, Bengali, Gujarati

Accessibility Options:

| Feature | Detail |
|---|---|
| Font size | Adjustable by user |
| High contrast mode | Available — toggle in accessibility settings |
| Screen reader compatibility | WCAG 2.1 AA compliant |
| Colour blind mode | Available — toggle in accessibility settings |
| Animations off | Available — for users with motion sensitivity |

CWSN students: all accessibility settings are pre-configured at the time the CWSN flag is set during admission — the student does not need to configure these manually.

---

## 23. Administrative Operations

### Visitor Management

| Field Captured | Detail |
|---|---|
| Visitor name | Mandatory |
| Visitor phone number | Mandatory |
| Purpose of visit | Mandatory |
| Whom they are meeting | Mandatory |
| Photo | Mandatory — captured at gate |
| ID proof | Mandatory — type and number recorded |
| Entry time | Auto-stamped |
| Exit time | Recorded by gate staff at exit |

- Gate Staff role is scoped exclusively to visitor management and student exit verification — they have no access to student academic data, staff data, or any other institutional records
- POCSO rule: an unverified visitor cannot meet any minor student without explicit Principal approval — gate staff cannot override this restriction regardless of the visitor's claimed identity
- Student exit: parent sends a live photo via the EduForge app → gate staff verifies against registered parent photo → child released only on successful verification

### Library Management

| Rule | Detail |
|---|---|
| Student book limit | Maximum 2 books at a time |
| Staff book limit | Maximum 5 books at a time |
| Reservation validity | 3 days — reserved books not collected within 3 days are released back |
| Fine calculation | Auto-calculated by Python based on overdue days and fine rate per day |
| Fine payment | Deducted from the student's General Wallet |
| New book additions | Librarian raises → Institution Admin approves |

### Lab / Sports Facility Booking

- Minimum 24-hour advance booking required
- Teacher submits a booking request → Lab Incharge or Sports Incharge approves
- Principal can override any booking for special events, institutional priorities, or visiting dignitaries
- Students cannot directly book labs or sports facilities — bookings must be made through a teacher

### ID Card

| Feature | Detail |
|---|---|
| Template | Institution-branded, unique design per institution type — configured by EduForge during onboarding |
| Fields | Name, Photo, Class / Year, Roll Number, Academic Year, Emergency Contact Number, Blood Group (optional) |
| Generation | Auto-generated by Python at the time of admission |
| Format | Digital (available in-app) + printable PDF |

### Bus Pass

```
Parent applies for bus pass through the app
        Route selected → fee calculated automatically by system
        |
        V
Fee shown upfront — parent pays via app (Razorpay / PhonePe)
        |
        V
Transport Incharge reviews the application
        |
        V
Institution Admin approves
        |
        V
Python generates the digital bus pass
        |
        V
Driver verifies digitally at boarding — scans student ID or QR code
        |
        V
Bus pass auto-expires at end of academic year — renewal required
```

- Route-based fee is auto-calculated by the system based on the student's pick-up/drop-off location and the defined route rates
- No manual fee calculation required

### Lost & Found

- Photo is mandatory when a found item is registered in the system
- Claims are made through the mobile app
- Gate Staff or Admin verifies the claimant's identity before releasing the item
- If no claim is made within 30 days, the item is marked for disposal — a platform-wide notification is sent before disposal
- All claim and release events are logged

### Disciplinary Records

| Step | Detail |
|---|---|
| Record creation | Class Teacher or HOD enters the incident and details |
| Approval | Principal approves the disciplinary record |
| Parent notification | Automated notification sent to parent immediately upon Principal approval |
| Student visibility | Student can view own disciplinary record only after Principal approves visibility |
| Permanence | Disciplinary records are never deleted — they are permanent institutional records |
| Appeal | Student or parent can raise an appeal through the platform — appeal goes to Principal |

### Accident / Incident Report

- Must be filed within 1 hour of the incident
- If a student is involved: parent is notified automatically within the same hour
- Photo and/or video evidence can be attached to the report
- Reports are permanent records — never deleted
- Any incident that falls under POCSO is automatically flagged to EduForge compliance team in addition to the institution's Principal

---

## 24. Financial Operations

### Budget Allocation

- Management sets the institution's overall budget for the academic year
- Principal allocates department-level budgets from the overall allocation
- HOD tracks their department's budget in real-time from the HOD dashboard
- The system automatically blocks any expenditure request that would cause the department budget to be exceeded
- Budgets reset at the start of each new academic year

### Purchase Order Workflow

```
HOD / Lab Incharge / Librarian raises a purchase request with item details + cost
        |
        V
Principal reviews and approves
        |
        V
Management gives final approval (TOTP required)
        |
        V
Institution Admin places the order with the supplier
        |
        V
Receiving staff confirms delivery in the system
        |
        V
Accountant processes payment — logged against the department budget
```

### Scholarship Disbursement

```
Scholarship Coordinator identifies eligible student and raises disbursement
        |
        V
HOD reviews and approves
        |
        V
Principal approves
        |
        V
Management gives final approval (TOTP required)
        |
        V
Accountant processes the disbursement — credited to student's fee balance
        |
        V
Python auto-generates the scholarship certificate
```

### Fee Receipt Correction

- The original fee receipt is preserved in the system — it cannot be modified or deleted
- The original is marked as "Corrected" and a new corrected receipt is issued with a reference back to the original
- Maximum 1 correction per receipt — a corrected receipt cannot be corrected again
- Parent is automatically notified when a corrected receipt is issued

### Compliance Reports

- Python auto-generates the annual compliance report in the board-specific format (CBSE / ICSE / State board format configured at institution setup)
- Principal reviews the report within the platform
- Management approves the report
- Principal submits the report using TOTP confirmation
- System sends a 60-day advance reminder before the compliance report submission deadline

### Affiliation Renewal

- System sends a 90-day advance reminder to Principal and Admin before affiliation expiry
- A document checklist for the renewal is shown — status of each required document is tracked in the system
- All supporting documents are stored on CDN (Cloudflare R2)
- Principal submits the renewal application with TOTP confirmation

---

## 25. Student Grievance & Support

### Grievance Escalation

| Level | Responsible Party | Time Limit |
|---|---|---|
| Level 1 | Class Teacher | 3 working days |
| Level 2 | HOD | 3 working days from Level 1 escalation |
| Level 3 | Principal | 3 working days from Level 2 escalation |
| Level 4 | EduForge Platform | 3 working days from Level 3 escalation |

- A case number is generated at the time of grievance submission — student and parent can use this to track status
- Parent is notified automatically at each escalation step
- If a level does not respond within 3 working days, the case is automatically escalated to the next level

### Anonymous Student Reporting

- Students can submit reports of bullying, harassment, misconduct, or safety concerns anonymously
- The student's identity is hidden from everyone at the institution — including Principal and Admin
- EduForge holds the identity for legal purposes only — it is not shared with the institution without a court order
- A case number is issued to the student for tracking
- EduForge compliance team investigates all anonymous reports

### Data Correction Request

- Parent identifies an error in the student's record (e.g. name spelling, date of birth)
- Parent raises a correction request through the app with a supporting document (birth certificate, Aadhaar, etc.)
- Institution Admin reviews the supporting document
- Principal approves the correction
- The old value is preserved in the audit log — the correction does not erase the history

### Parent Feedback on Teachers

- Parents can submit one anonymous feedback per teacher per term
- Identity is never shown to the teacher
- Principal and HOD can see individual feedback responses for each teacher
- Teacher sees only their aggregated score for the term — not individual responses
- Feedback scores are included as one input in the annual staff performance review

---

## 26. Staff Operations

### Leave Management

- Leave types (casual, medical, maternity, compensatory, etc.) and their approval levels are customisable per institution
- EduForge provides a default leave management template at onboarding — institutions can modify it
- Staff on approved leave have view-only access to the platform — they cannot create, edit, or approve anything while on leave
- When leave is approved, the system prompts the HOD to assign a substitute teacher if applicable
- Full access is automatically restored on the day of return, as configured in the leave record

### Staff Performance Review

- Annual review cycle — one review per academic year
- Each staff member sees only their own review scores and feedback
- HOD and Principal can view individual staff reviews within their scope
- Management sees all staff reviews across the institution
- Promotion and increment decisions based on performance review require joint approval from Management and Principal

### Staff Training (Mandatory Compliance Training)

| Training | Who Must Complete | Access Impact |
|---|---|---|
| POCSO Awareness Training | All staff before first accessing any student data | Access to student data blocked until training is completed and certificate uploaded |
| Data Protection / DPDPA | All staff | Tracked — alert if overdue |

- Completion of mandatory training is tracked automatically by the system
- If a staff member's training certificate expires or is overdue, the system sends an alert to the staff member, HOD, and Principal
- Staff must upload the training certificate — Admin verifies the certificate

### Probation

- Probation duration is set individually by the Principal for each staff member — there is no fixed platform-wide probation period
- Principal can extend probation any number of times — each extension is logged
- BGV must be cleared before a staff member can be confirmed (moved out of probation) — probation cannot end while BGV is still pending or in progress
- If the Principal does not take action (confirm or extend probation) within 7 working days of the probation end date, the system automatically suspends the staff account — the account remains suspended until the Principal acts

### Salary Slips

| Access Level | Detail |
|---|---|
| Auto-generation | Python generates salary slips monthly, on a fixed date configured per institution |
| Template | Institution-branded, unique design — configured at onboarding |
| Staff (own slip) | Each staff member sees and downloads only their own current and past slips |
| Accountant | Can view all staff salary slips — cannot edit any |
| Management | Can edit salary records — requires 3-step approval + TOTP before any change takes effect |
| Slip notification | Staff notified via in-app notification when monthly slip is generated |

---

*End of Module 03 — Roles & Permissions (RBAC)*

*EduForge Platform Documentation | Confidential — Internal Use*
