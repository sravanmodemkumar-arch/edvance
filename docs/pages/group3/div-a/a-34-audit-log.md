# A-34 — Audit Log

> **URL:** `/school/admin/audit-log/`
> **File:** `a-34-audit-log.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · Promoter (S7) — view · Platform Admin (Group 1) — full

---

## 1. Purpose

Immutable audit trail of all significant actions performed in the school portal. Required for CBSE compliance, DPDPA compliance (digital record keeping), and internal governance. The audit log cannot be edited or deleted by any school staff — it is append-only at the database level. If there's ever a dispute ("I didn't change the result" / "Someone altered the fee record"), this is the authoritative record.

**DPDPA relevance:** India's DPDPA 2023 requires "processing of personal data" to be logged. EduForge logs all access to and modifications of student/staff PII.

---

## 2. Page Layout

### 2.1 Header
```
Audit Log                                   [Export] [Advanced Filters]
Total entries: 48,432 (this academic year)  Search: [___________]
```

### 2.2 Filter Bar
```
Category [All ▼]  Actor [All ▼]  Date Range [Last 30 days ▼]  Module [All ▼]
```

---

## 3. Log Table

| Timestamp | Actor | Role | Action | Module | Description | IP Address |
|---|---|---|---|---|---|---|
| 26 Mar 14:32:18 | Ms. Sudha Rani | VP Academic | PUBLISH | Exam Results | Published Class IX Unit Test 2 results to 108 students | 192.168.1.42 |
| 26 Mar 11:18:42 | Mr. Rajan T | Principal | APPROVE | Approvals | Approved EL leave for Mr. Kumar (5 days, 1–5 Apr) | 192.168.1.10 |
| 26 Mar 09:45:21 | Admin Officer | Office Staff | CREATE | Circular | Created CIR/2025-26/048 — Annual Exam Schedule | 192.168.1.25 |
| 25 Mar 16:22:09 | Principal | Principal | ACCESS | POCSO | Accessed POCSO case register | 192.168.1.10 |
| 25 Mar 14:11:33 | Ms. Kavitha | Class Teacher | EDIT | Attendance | Modified attendance: Class VII B, 24 Mar (correction) | 192.168.1.55 |

---

## 4. Audit Event Categories

| Category | Events Captured |
|---|---|
| Authentication | Login · Logout · Failed login · 2FA events · Session expiry |
| Student Records | Create · Edit · View PII · Admission · TC · Delete (blocked) |
| Staff Records | Create · Edit · Salary view · BGV update · Deactivate |
| Financial | Fee collection · Receipt generate · Waiver · Refund · Payroll process |
| Academic | Mark entry · Edit marks · Result publish · Result unpublish |
| Attendance | Bulk mark · Individual correction · Deletion (blocked) |
| Circulars | Create · Approve · Dispatch · Delete |
| POCSO | Page access · Case create · Case view · Report generate |
| Approvals | Approve · Reject · Return · Delegate |
| System | Settings change · Role change · User create/deactivate |

---

## 5. Log Entry Detail Drawer

Click any row → 520px drawer:
- **Event:** Action type + module + timestamp
- **Actor:** Name + role + Employee ID
- **Before/After:** If an edit, shows previous value → new value (diff)
- **Context:** Parent event (e.g., which approval request this was for)
- **IP/Session:** IP address, browser, device type, session ID

---

## 6. Export

[Export] → generates CSV with all filtered log entries. Large exports (> 10,000 rows) → background task → download link emailed to Principal.

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/audit-log/` | Log entries (paginated, filterable) |
| 2 | `GET` | `/api/v1/school/{id}/audit-log/{entry_id}/` | Entry detail |
| 3 | `GET` | `/api/v1/school/{id}/audit-log/export/` | Export (async for large sets) |

---

## 8. Business Rules

- Append-only at DB level: `school_audit_log` table has no UPDATE or DELETE permissions for application DB user
- Retained for 7 years (CBSE + DPDPA requirement)
- POCSO access events retained for 10 years (longer than other events per legal requirement)
- Platform Admin can view but not modify; Platform Admin's access is itself logged in a separate platform-level audit log

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
