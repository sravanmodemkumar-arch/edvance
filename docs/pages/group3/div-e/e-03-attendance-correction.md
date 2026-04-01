# E-03 — Attendance Correction Register

> **URL:** `/school/attendance/corrections/`
> **File:** `e-03-attendance-correction.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Class Teacher (S3) — request corrections for own class · Administrative Officer (S3) — process corrections · Academic Coordinator (S4) — approve corrections > 48 hours old · Principal (S6) — approve bulk corrections / override

---

## 1. Purpose

All attendance corrections after submission go through this register — creating an immutable audit trail of what was changed, who changed it, why, and who approved it. CBSE inspection specifically checks: "Are attendance corrections documented? Is there a register showing original mark, corrected mark, and authorised by whom?"

Corrections are needed when:
- Class Teacher marked a student absent, but the student was actually present (confusion at roll call)
- Student arrived late but was marked absent — Class Teacher wants to correct to Late
- System error caused wrong marks for an entire class on a day
- Student submitted a medical certificate for a past absence — absence converted to medical leave
- A student was wrongly enrolled in a class — their attendance needs to be reversed

---

## 2. Page Layout

### 2.1 Header
```
Attendance Correction Register               [+ Request Correction]  [Export Register]
Pending Corrections: 3  ·  Approved This Month: 12  ·  Rejected: 1
```

### 2.2 Correction Log
| Req No. | Student | Class | Date | Original | Corrected | Reason | Requested By | Status |
|---|---|---|---|---|---|---|---|---|
| COR-2026-015 | Arjun Sharma | XI-A | 25 Mar | Absent | Present | Confusion at roll call | Ms. Anita (CT) | ✅ Approved |
| COR-2026-016 | Priya Venkat | XI-A | 26 Mar | Absent | Late (arrived 9:45) | Dental appointment | Ms. Anita (CT) | ⏳ Pending |
| COR-2026-017 | Rohit Kumar | IX-B | 20 Mar | Absent | Medical Leave | Doctor certificate submitted | Mr. Ravi (Admin) | ⏳ Pending |

---

## 3. Request Correction

[+ Request Correction] → form:

| Field | Value |
|---|---|
| Student | [Search] |
| Date to Correct | 25 Mar 2026 |
| Original Mark | Absent |
| Corrected Mark | Present · Late · Medical Leave · On-Duty |
| Reason | Student was present but I marked wrong during roll call. Cross-verified with period teacher. |
| Supporting Evidence | Period teacher confirmation / Medical certificate / Parent letter [Upload] |
| Urgency | Normal · Urgent (affects exam eligibility) |

**Approval routing:**
- Correction within 24 hours: Class Teacher self-approves (auto-approved)
- Correction 24–48 hours old: Administrative Officer approves
- Correction > 48 hours old: Academic Coordinator approves
- Bulk corrections (> 5 students, same day): Principal approves

---

## 4. Approval Workflow

### Administrative Officer view:
```
Pending Correction — COR-2026-016

Student: Priya Venkat (XI-A)
Date: 26 March 2026
Requested by: Ms. Anita Reddy (Class Teacher)
Change: Absent → Late (arrived 9:45 AM)
Reason: Dental appointment — parent note attached
Supporting doc: Parent note PDF ✅

[Approve]  [Reject — Reason: ___________]
```

After approval:
- Original mark retained in audit log (never deleted)
- New mark replaces the display mark for reports / notifications
- Parent is notified: "Attendance for Priya Venkat on 26 Mar corrected: Absent → Late (Approved by school)"

---

## 5. Special Correction Types

### Medical Leave Conversion
When a student submits a doctor's certificate for past absences:
```
Medical Leave Conversion — Rohit Kumar (IX-B)

Absent dates: 18 Mar, 19 Mar, 20 Mar 2026 (3 days)
Doctor Certificate: Dr. Suresh Clinic — Viral fever — [View PDF]
Conversion: Absent → Medical Leave (all 3 dates)

Effect on attendance %:
  Before: 188/210 = 89.5%
  After (medical leave not counted as absent in condonation): 188/207 = 90.8%
  Note: Medical leave reduces the denominator (days absent for medical reason excluded from % for condonation purposes)

Approval: Administrative Officer
```

### On-Duty Correction
Students absent because they represented school in sports/cultural events:
```
On-Duty — Arjun Sharma (XI-A) — 22 Mar 2026

Event: District-level Cricket Tournament (school team)
Absence is On-Duty — should not be counted against attendance
Certificate from: Sports Teacher / Academic Coordinator
Effect: Absent → On-Duty (not counted in absence denominator)
```

---

## 6. Export

[Export Register] → CBSE inspection format:
```
ATTENDANCE CORRECTION REGISTER — 2025–26
[School Name]

Req No.  Student  Class  Date  Original  Corrected  Reason  Approved By  Date
COR-001  Arjun S.  XI-A  05 Apr  Absent  Present   Error  Admin Meera  06 Apr
...
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/corrections/?year={year}` | Correction register |
| 2 | `POST` | `/api/v1/school/{id}/attendance/corrections/` | Request correction |
| 3 | `GET` | `/api/v1/school/{id}/attendance/corrections/{corr_id}/` | Correction detail |
| 4 | `PATCH` | `/api/v1/school/{id}/attendance/corrections/{corr_id}/approve/` | Approve/reject |
| 5 | `POST` | `/api/v1/school/{id}/attendance/corrections/bulk/` | Bulk correction (system error recovery) |
| 6 | `GET` | `/api/v1/school/{id}/attendance/corrections/export/?year={year}` | Export register |

---

## 8. Business Rules

- The original attendance mark is never deleted from the database — corrections create a new record (effective mark) while the original remains in the audit table; the audit log shows both
- A correction cannot change a Present to Absent retroactively (schools cannot retrospectively remove a student's attendance) — this would be a CBSE violation; system blocks it
- Medical leave conversion: medical leave is counted as "excused absence" for condonation purposes in E-11 but still counted as an absence day for the denominator in the official CBSE register
- Batch corrections for an entire class on a specific date (e.g., system was down and the teacher marked all as absent by default) require Principal approval and a formal note
- All correction approvals are logged with approver ID, timestamp, and IP address for security audit

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
