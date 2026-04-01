# A-28 — Parent Communication Log

> **URL:** `/school/admin/communications/parents/`
> **File:** `a-28-parent-communication-log.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · VP Academic (S5) — view · VP Admin (S5) — view · Admin Officer (S3) — view + add entries

---

## 1. Purpose

Records all significant individual communications between the school and specific parents/guardians — meetings, phone calls, escalated complaints, disciplinary discussions, counsellor referrals, TC conversations, fee dispute resolutions. This is distinct from bulk circular dispatch (A-26); this page tracks one-to-one parent interactions. Maintaining this log is important for POCSO compliance (documenting responses to parent complaints) and for Exam Cell/CBSE compliance (documenting communication about grievances).

---

## 2. Page Layout

### 2.1 Header
```
Parent Communication Log                    [+ Add Entry]  [Export]  [Filters ▼]
Total Entries This Year: 342 · Open Issues: 12 · Escalated: 3
```

---

## 3. Log Table

| Date | Student | Class | Parent/Guardian | Communication Type | Subject | Staff | Status | Action |
|---|---|---|---|---|---|---|---|---|
| 26 Mar 2026 | Aryan Sharma | XII MPC | Father — Mr. A. Sharma | Walk-in Meeting | Exam Result Grievance | VP Academic | Open | [View] |
| 25 Mar 2026 | Priya Roy | IX B | Mother — Ms. R. Roy | Phone Call | Fee Payment Query | Accountant | Closed | [View] |
| 22 Mar 2026 | Rahul Kumar | VII A | Father — Mr. S. Kumar | Complaint (written) | Teacher Behaviour | Principal | Escalated | [View] |

**Communication Types:** Walk-in Meeting · Phone Call · WhatsApp · Email · Written Complaint · Counsellor Meeting · PTM Follow-up · Fee Dispute · TC Request · Emergency Contact · POCSO Related

**Status:** Open · In Progress · Resolved · Escalated (POCSO or legal)

---

## 4. Communication Entry Drawer

**520px, tabs: Details · Follow-up Actions · History**

**Details tab:**
- Date + time of communication
- Student (search by name/roll no)
- Parent/guardian name + contact + relationship
- Communication type
- Staff who handled: select from staff list
- Subject/purpose
- Summary of discussion (notes — free text)
- Outcome: Resolved · Follow-up needed · Escalated to [Principal/POCSO/External]
- Next action: description + deadline + assigned to

**Follow-up Actions:**
- List of follow-up tasks created from this communication
- Each: task description · assigned to · due date · status

---

## 5. Parent Interaction Analytics

**Summary chart (monthly):**
- Bar chart: communication types per month
- Most common: Fee query · Academic query · Complaint · PTM follow-up

**Response time tracking:**
- Average time to first response: X hours
- Unresolved > 3 days: highlighted

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/parent-comms/` | Communication log list |
| 2 | `POST` | `/api/v1/school/{id}/parent-comms/` | Add log entry |
| 3 | `GET` | `/api/v1/school/{id}/parent-comms/{id}/` | Entry detail |
| 4 | `PATCH` | `/api/v1/school/{id}/parent-comms/{id}/` | Update status + follow-up |
| 5 | `GET` | `/api/v1/school/{id}/parent-comms/analytics/` | Communication analytics |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
