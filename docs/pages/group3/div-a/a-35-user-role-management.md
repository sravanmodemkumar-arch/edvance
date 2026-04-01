# A-35 — User & Role Management

> **URL:** `/school/admin/users/`
> **File:** `a-35-user-role-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · VP Academic (S5) — create staff accounts S4 and below (teaching) · VP Admin (S5) — create staff accounts S4 and below (admin/support)

---

## 1. Purpose

Creates and manages EduForge login accounts for all school staff. Every staff member who needs to use EduForge must have an account created here. The Principal is the RBAC root for the institution — they can create/modify/deactivate accounts for all staff below S6. VP Academic manages teaching staff accounts; VP Admin manages non-teaching staff accounts.

---

## 2. Page Layout

### 2.1 Header
```
User & Role Management                      [+ Add User]  [Export]  [Inactive Users]
Total Users: 112 · Active: 110 · Inactive: 2 · Never Logged In: 8
```

---

## 3. User Table

| Name | Role | Level | Department | Last Login | Status | 2FA | Actions |
|---|---|---|---|---|---|---|---|
| Mr. [Principal Name] | Principal | S6 | — | Today | 🟢 Active | ✅ On | [Edit] [Reset PW] |
| Ms. Sudha Rani | PGT Chemistry | S3 Teacher | Science | 25 Mar | 🟢 Active | ❌ Off | [Edit] [Reset PW] |
| Mr. Rajan (Guard) | Security Staff | S2 Support | Admin | 20 Mar | 🟢 Active | ❌ Off | [Edit] [Deactivate] |
| Ms. Absent Teacher | Class Teacher | S3 Teacher | Language | 4 days ago | 🟡 Not accessed | ❌ Off | [Send Reminder] |

---

## 4. Add User Form

**Triggered by [+ Add User] drawer (560px):**

| Field | Description |
|---|---|
| Staff | Search and select from Staff Directory (staff must be in A-16 first) |
| Role | Dropdown of all defined roles for the school |
| Level | Auto-set based on role; Principal can override for custom roles |
| Login Method | EduForge account (email + password) |
| Email (login ID) | Pre-filled from staff profile; editable |
| Phone (for OTP) | Pre-filled from staff profile |
| 2FA Required | Yes / No (mandatory for Principal, VP; optional for others) |
| Welcome Notification | Send login credentials via: [Email ✅] [WhatsApp ✅] |

---

## 5. Role Configuration (School-level)

**[Manage Roles]** section (Principal only):

Pre-built roles (from EduForge default School template):
| Role | Level | Scope | Modules Access |
|---|---|---|---|
| Principal | S6 | Full institution | All modules |
| VP Academic | S5 | Full academic scope | Academic, Attendance, Exams, Results |
| VP Administration | S5 | Full admin scope | Admissions, Finance overview, HR, Transport |
| HOD | S4 | Own department | Attendance, Marks, Syllabus (dept-scope) |
| Exam Cell Head | S4 | Exams scope | Exam Config, Hall Tickets, Results |
| Class Teacher | S3 | Own class | Attendance, Marks, Homework, Parent comms |
| Subject Teacher | S3 | Own subject/classes | Attendance (periods), Marks (subject), Notes |
| School Accountant | S4 Finance | Finance | Fee collection, Receipts, Reports |
| Librarian | S3 | Library | Book catalogue, Issue/Return |
| Counsellor | S3 Welfare | Student welfare | Student profiles, Parent comms, Health records |
| Nurse/Medical | S3 Medical | Health records | Medical records (hostel/school) |
| Transport In-charge | S3 Admin | Transport | Route config, Driver records, GPS |
| Hostel Warden | S3 Admin | Hostel | Room allotment, Hostel attendance, Health |
| Gate Staff | S2 | Gate only | Visitor log, Student exit verification |
| POCSO Coordinator | S4 Welfare | POCSO | POCSO Centre (A-30) only |
| Administrative Officer | S3 Admin | Office | Circulars, Visitor log, Staff records, TC |

**Custom Roles:** Principal can create custom roles by duplicating an existing role and modifying permissions. Requires Principal 2FA confirmation.

---

## 6. Password & Security Management

- **Reset Password:** [Reset PW] button → sends OTP to staff phone → staff sets new password
- **Force Logout:** [Force Logout] → invalidates all active sessions for the user
- **Account Lock:** After 5 failed login attempts, account auto-locks for 30 minutes; VP Admin/Principal can manually unlock
- **2FA Enforcement:** Configure which roles require 2FA (Principal mandatory by default; customisable)

---

## 7. Never-Logged-In Users

Users with accounts but who have never logged in (common for new staff who haven't started using the platform):
- Highlighted in the table
- [Send Reminder] → WhatsApp message with login link and credentials

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/users/` | User list |
| 2 | `POST` | `/api/v1/school/{id}/users/` | Create user account |
| 3 | `PATCH` | `/api/v1/school/{id}/users/{user_id}/` | Update role/status |
| 4 | `POST` | `/api/v1/school/{id}/users/{user_id}/reset-password/` | Trigger password reset |
| 5 | `POST` | `/api/v1/school/{id}/users/{user_id}/deactivate/` | Deactivate account |
| 6 | `POST` | `/api/v1/school/{id}/users/{user_id}/force-logout/` | Invalidate sessions |
| 7 | `GET` | `/api/v1/school/{id}/roles/` | Defined roles list |
| 8 | `POST` | `/api/v1/school/{id}/roles/` | Create custom role |
| 9 | `PATCH` | `/api/v1/school/{id}/roles/{role_id}/` | Update custom role |

---

## 9. Business Rules

- Cannot create a user account at S6 (Principal level) or above without Platform Admin countersign
- Deactivated user accounts are retained for audit purposes; they are not deleted
- Role changes are logged in A-34 Audit Log with before/after values
- 2FA must be enabled for all Principal-level accounts (platform enforced; cannot be disabled by school)
- Staff deactivated in A-16 (Staff Directory) does not auto-deactivate their EduForge login — must be done separately here (intentional separation to prevent accidental access removal)

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
