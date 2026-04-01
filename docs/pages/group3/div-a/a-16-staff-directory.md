# A-16 — Staff Directory & Strength

> **URL:** `/school/admin/staff/`
> **File:** `a-16-staff-directory.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Principal (S6) — full · VP Admin (S5) — full · Admin Officer (S3) — view + edit basic · HOD (S4) — view own dept

---

## 1. Purpose

Complete registry of all school staff — teaching and non-teaching. This is the HR master database for the institution. Every EduForge function that requires staff lookup (timetable, attendance, leave, salary, BGV) reads from this registry. Staff who are not in this registry cannot log in to EduForge.

**Indian school staff categories:**
- **Teaching staff:** All teachers with direct instructional responsibility — need B.Ed/D.El.Ed qualification (mandatory for CBSE)
- **Non-teaching staff:** Administrative, support, maintenance, transport, hostel, security
- **Part-time/visiting faculty:** Guest lecturers, external coaches (Music/Dance/Sports)
- **Contract staff:** Housekeeping, security (often through agency — BGV compliance applies)

---

## 2. Page Layout

### 2.1 Header
```
Staff Directory — 2025–26                    [+ Add Staff]  [Export]  [BGV Status]  [Filters ▼]
Teaching: 78 · Non-Teaching: 24 · Contract: 8 · Total: 110 · Vacancies: 6
```

### 2.2 Filter Bar
- Category: All · Teaching · Non-Teaching · Contract · Visiting
- Department: All departments dropdown
- BGV Status: All · Verified · Pending · Expired
- Employment Type: Permanent · Probation · Contract · Part-time
- Status: Active · Inactive · On Leave

---

## 3. Staff Table

| Photo | Name | Designation | Department | Employee ID | Employment | Subjects | BGV | Status | Actions |
|---|---|---|---|---|---|---|---|---|---|
| [pic] | Ms. Sudha Rani | PGT Chemistry | Science Dept | EMP-241 | Permanent | Chem XI, XII | ✅ Verified | 🟢 Active | [View] [Edit] |
| [pic] | Mr. Rajan T | TGT Maths | Maths Dept | EMP-178 | Permanent | Math VIII, IX | ⚠️ Expiring 15 Apr | 🟢 Active | [View] [Edit] |
| [pic] | Ms. Priya K | PRT English | Language Dept | EMP-312 | Probation | English III | ✅ Verified | 🟢 Active | [View] [Edit] |
| [pic] | Mr. Suresh (Guard) | Security Guard | Admin | EMP-403 | Contract | — | ❌ Pending | 🟢 Active | [View] |

**BGV status colours:**
- ✅ Green = Verified
- ⚠️ Amber = Expiring soon (< 30 days) or pending (< 30 days since joining)
- ❌ Red = Not done or expired — **POCSO risk flag**

---

## 4. Staff Profile Drawer

**680px wide, tabs: Profile · Qualifications · Subjects & Timetable · Leave · Salary · BGV · Documents · History**

### Profile tab:
- Employee ID (auto-generated: EMP-NNN)
- Full name · Date of Birth · Gender · Blood Group
- Aadhaar No (masked) · PAN No (masked)
- Personal email + phone (for emergency contact)
- Home address
- Emergency contact: name + relation + phone
- Marital status · Children count (for maternity/paternity leave eligibility)
- Date of joining · Date of confirmation (if permanent)
- Current designation · Department · Reporting to (Principal / VP / HOD)
- Employment type: Permanent / Probation / Contract / Part-time / Visiting
- Salary grade / pay scale

### Qualifications tab:
- Highest degree + institution + year
- B.Ed/D.El.Ed/M.Ed details (mandatory for teachers)
- UGC-NET/CTET/State TET qualification (if any)
- Other certifications

### Subjects & Timetable tab:
- Subjects assigned (class-section-subject combinations)
- Current timetable slots
- Class teacher assignment (if any)

### Leave tab:
- Current year leave balance (per type)
- Leave history (all years)
- Upcoming approved leaves

### Salary tab:
- Current CTC breakdown
- Pay revision history
- Salary slip downloads (last 12 months)
- Read-only for S4 and below (only Principal + VP Admin + Accountant can see)

### BGV tab:
- BGV agency: [select or enter]
- Verification date
- Documents verified: ID proof · Address proof · Previous employer · Police verification · Education certificates
- BGV certificate upload
- Next renewal date

### Documents tab:
- Appointment letter · Joining form · Academic certificates · ID proof · Address proof · PAN · Aadhaar · Passport (if any)
- Upload / download each

### History tab:
- All changes to this staff record: who changed what, when, from-to values

---

## 5. Add Staff Form

**Triggered by [+ Add Staff]**
- Required at minimum: Name, designation, department, date of joining, phone, email
- Auto-generates Employee ID
- Sends login credentials to staff email + phone (WhatsApp)
- Creates BGV tracking record (sets due date = joining + 30 days)

---

## 6. Staff Strength by Department (chart)

Bar chart: Department on X-axis · Count on Y-axis · Split by Teaching/Non-Teaching
Shows vacancy positions in dashed outline bars.

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/staff/` | Staff list (paginated, filterable) |
| 2 | `POST` | `/api/v1/school/{id}/staff/` | Add new staff |
| 3 | `GET` | `/api/v1/school/{id}/staff/{staff_id}/` | Staff profile detail |
| 4 | `PATCH` | `/api/v1/school/{id}/staff/{staff_id}/` | Update staff profile |
| 5 | `POST` | `/api/v1/school/{id}/staff/{staff_id}/deactivate/` | Deactivate staff |
| 6 | `GET` | `/api/v1/school/{id}/staff/{staff_id}/bgv/` | BGV record |
| 7 | `PATCH` | `/api/v1/school/{id}/staff/{staff_id}/bgv/` | Update BGV status |
| 8 | `GET` | `/api/v1/school/{id}/staff/strength-by-dept/` | Department-wise strength |
| 9 | `GET` | `/api/v1/school/{id}/staff/bgv-status-summary/` | BGV compliance summary |
| 10 | `GET` | `/api/v1/school/{id}/staff/export/` | Export staff list CSV |

---

## 8. Business Rules

- Staff cannot be deleted — only deactivated (historical records must be preserved)
- BGV expired or not done → staff flagged in POCSO compliance; Principal notified daily
- Salary data is accessible only to Principal (S6), VP Admin (S5), and Accountant role (S4 Finance)
- Aadhaar/PAN data is masked in display (last 4 digits only); full access requires elevated permission log
- Part-time/visiting staff: limited EduForge access; can mark attendance and enter marks for their assigned periods only
- Contract staff from agencies: agency name + agency contact stored; BGV status tracked per individual, not just agency

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
