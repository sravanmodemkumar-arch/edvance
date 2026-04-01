# C-11 — Internal Transfer Manager

> **URL:** `/school/students/transfers/internal/`
> **File:** `c-11-internal-transfer.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Class Teacher (S3) — view own class · Academic Coordinator (S4) — full · Principal (S6) — full

---

## 1. Purpose

Manages mid-year changes to a student's class-section assignment within the school. This is different from year-end promotion (C-10) — these are transfers that happen during the academic year due to:
- **Section balancing:** One section is overloaded (42 students) while a parallel section is thin (28 students)
- **Subject/stream change:** A Class XI student decides to switch from Science to Commerce within the first month (permitted up to a deadline)
- **Personality/behavioural:** Student placed in wrong section (sibling in same class was accidentally enrolled in same section — school policy prohibits)
- **Correction of year-end promotion error:** A student was mistakenly put in the wrong section during C-10 rollover

All internal transfers require Academic Coordinator approval, and some (stream changes, correction of errors) require Principal approval. Each transfer is logged with reason and approver.

---

## 2. Page Layout

### 2.1 Header
```
Internal Transfer Register — 2026–27         [+ Request Transfer]
Total Transfers This Year: 12
Section Rebalancing: 3  ·  Stream Change: 2  ·  Correction: 4  ·  Other: 3
```

### 2.2 Transfer List
| # | Student | From | To | Reason | Requested | Approved By | Effective Date | Status |
|---|---|---|---|---|---|---|---|---|
| T-2026-012 | Arjun Sharma | XI-A | XI-B | Section rebalancing | 15 Mar 2026 | Academic Coord | 18 Mar 2026 | ✅ Done |
| T-2026-011 | Priya Venkat | XI-A Sci | XI-C Commerce | Stream change | 12 Mar 2026 | Principal | 14 Mar 2026 | ✅ Done |
| T-2026-010 | Rohit Kumar | VII-A | VII-B | Sibling separation | 10 Feb 2026 | Academic Coord | 12 Feb 2026 | ✅ Done |

---

## 3. Request Transfer

[+ Request Transfer] → form:

| Field | Value |
|---|---|
| Student | [Search by name/roll/ID] |
| Current Class-Section | XI-A (auto-populated) |
| Transfer To (Class-Section) | XI-B |
| Transfer Type | Section Change · Stream Change · Error Correction · Other |
| Reason | Section rebalancing — XI-A has 42 students, XI-B has 28 |
| Effective Date | 18 Mar 2026 |
| Approval Required From | Academic Coordinator (for section change) / Principal (for stream change) |

**Validation checks on submit:**
- Target section exists and has capacity
- For stream changes: student meets eligibility for target stream
- For stream changes: within the allowed stream-change window (configurable; e.g., within 30 days of joining XI)

---

## 4. Impact of Transfer

When a transfer is processed, the following are updated automatically:

| Module | Update |
|---|---|
| **Student Profile (C-08)** | Class-section updated; class teacher updated |
| **Attendance** | Attendance records continue; class register changes from effective date |
| **Timetable (B-06)** | Student appears in new class's timetable |
| **Fee (div-d)** | If stream change → fee structure may change (Science fee ≠ Commerce fee) |
| **Marks** | Previous marks stay in old class records; future marks in new class |
| **Roll Number** | Re-assigned in new section (last roll or specific number) |

---

## 5. Section Strength Display

When selecting target section, real-time strength shown:
```
XI-A (Science PCM): 42 students  ← Overloaded (>40 limit)
XI-B (Science PCM): 28 students  ← Underloaded
XI-C (Commerce):    36 students  ← Normal
```

---

## 6. Stream Change — Special Handling

Class XI stream change within the first 30 days of academic year:

```
Stream Change Request — Priya Venkat (XI-A Science → XI-C Commerce)

Reason: Student reports difficulty with Physics; father requests Commerce stream
Current Stream: Science (PCM) — joined 5 Apr 2026
Requested Stream: Commerce (Mathematics group)
Days since joining: 12 (within 30-day window ✅)

Class X Class X subjects/marks:
  Mathematics: 68%  ✅ (Commerce eligible: ≥ 50%)
  Science: 84%

Impact:
  Fee difference: Science (₹8,500/m) → Commerce (₹7,800/m) — ₹700/month less
  Fee adjustment: Will be processed in fee module

Approval: PRINCIPAL REQUIRED for stream change
[Send for Principal Approval]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/transfers/internal/?year={year}` | Transfer list |
| 2 | `POST` | `/api/v1/school/{id}/students/transfers/internal/` | Request transfer |
| 3 | `GET` | `/api/v1/school/{id}/students/transfers/internal/{transfer_id}/` | Transfer detail |
| 4 | `PATCH` | `/api/v1/school/{id}/students/transfers/internal/{transfer_id}/approve/` | Approve transfer |
| 5 | `PATCH` | `/api/v1/school/{id}/students/transfers/internal/{transfer_id}/process/` | Execute transfer (post-approval) |

---

## 8. Business Rules

- A transfer takes effect only after approval; before approval, the student remains in their current class
- Stream changes (Science ↔ Commerce ↔ Arts) can only be done within the first 30 days of the academic year (configurable); after this window, stream changes require Board/CBSE NOC (rare) and are blocked in the system
- Transfer affects roll number assignment: student gets a new roll number in the target section (system assigns next available roll by default; can be overridden)
- All historical marks, attendance, and fee records remain linked to the student (via Student ID — immutable); only future records attach to the new class
- Transfer log is permanent — cannot be deleted; provides audit trail for CBSE inspection

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
