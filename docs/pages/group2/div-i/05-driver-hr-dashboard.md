# 05 — Driver / Conductor HR (External Tool Boundary)

> **URL:** `/group/transport/driver-hr/` → redirect to external ATS
> **File:** `05-driver-hr-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Driver/Conductor HR (Role 83, G0) — No EduForge platform access

---

## 1. Purpose

The Group Driver/Conductor HR (Role 83) operates at access level **G0 — No Platform Access**. This role does not log into EduForge directly. All driver and conductor recruitment, onboarding, licence verification, and ATS activity occurs in the group's external HR / ATS tool (e.g., Zoho Recruit, Keka, or custom HR software).

This page serves as:
1. A **boundary documentation page** for other transport roles who need to understand why Driver/Conductor HR is not on EduForge.
2. An **integration reference** page explaining how driver and conductor data flows from the external ATS into EduForge's Driver Registry (Page 15) via API sync.
3. A **handoff interface** shown to other G3 transport roles who click "Driver HR" from the Driver Registry, so they understand where to escalate driver hiring requests.

EduForge receives a sync of confirmed, onboarded drivers/conductors from the external system. Transport roles manage the EduForge-side data (licence tracking, BGV status, route assignment) — hiring decisions live outside EduForge.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Driver/Conductor HR | G0 | **No EduForge Login** | Uses external ATS only |
| Group Fleet Manager | G3 | View this boundary page only | Cannot act on hiring |
| Group Transport Director | G3 | View this boundary page only | Cannot act on hiring |
| Group Transport Safety Officer | G3 | View this boundary page only | Cannot act on hiring |

> **Access enforcement:** `@require_role('fleet_manager', 'transport_director', 'transport_safety_officer')` — transport roles can read this page for context; Driver/Conductor HR role has no EduForge session.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Transport Management  ›  Driver / Conductor HR
```

### 3.2 Page Header
```
Driver & Conductor HR — External Process
Group Driver/Conductor HR (Role 83) operates outside EduForge.
Onboarded drivers sync automatically into the Driver Registry.
```

---

## 4. Integration Overview Panel

### 4.1 How Driver Data Flows Into EduForge

| Step | What Happens | System |
|---|---|---|
| 1. Job Posting | Driver/Conductor vacancy created | External ATS |
| 2. Screening | Resume shortlist, phone screen | External ATS |
| 3. Licence Verification | DL type, validity checked against RTO | External ATS + manual |
| 4. BGV | Background verification — criminal record, previous employer | External BGV vendor |
| 5. Offer & Onboarding | Offer letter, joining formalities | External HRMS |
| 6. Sync to EduForge | `POST /api/v1/group/{group_id}/transport/drivers/sync/` triggered | EduForge API |
| 7. Driver Record Created | Driver appears in Driver Registry (Page 15) | EduForge |
| 8. Route Assignment | Fleet Manager assigns driver to route | EduForge |

### 4.2 Data Synced into EduForge (Read-only from HR system)

| Field | Source |
|---|---|
| Full Name | External HRMS |
| Employee ID | External HRMS |
| Driving Licence Number | External HRMS / manual entry |
| Licence Type (LMV / HMV / PSV) | External HRMS |
| Licence Expiry Date | External HRMS |
| Joining Date | External HRMS |
| Branch Assignment | External HRMS |
| BGV Status (Passed / Pending / Failed) | External BGV vendor → HRMS |
| Photo | External HRMS |
| Emergency Contact | External HRMS |

### 4.3 What EduForge Manages After Sync

| Field | Managed By |
|---|---|
| Route Assignment | Fleet Manager / Transport Director |
| Licence Renewal Reminders | EduForge (auto) — Page 16 |
| Daily Duty Status (On Duty / On Leave / Absent) | Branch-level transport portal |
| Training Records (Road Safety, First Aid) | EduForge — Page 17 |
| Accident / Incident Association | Safety Officer — Page 23 |
| Bus Pass (for driver's dependents, if applicable) | Fee Manager — Page 28 |

---

## 5. Pending Hiring Requests Panel

> Transport roles can raise a hiring request that routes to the Driver/Conductor HR via external system.

### 5.1 Raise Hiring Request (Button → External Form)

**"Raise Driver Hiring Request"** → Opens external HRMS/ATS URL in new tab.

Fields pre-populated via URL params:
- Branch
- Vehicle type (HMV / PSV required)
- Urgency (Immediate / Planned)
- Raised by (current user)

### 5.2 Open Hiring Requests (Read-Only Table)

> Pulled from external system via API if integration is configured.

**Columns:** Request ID · Branch · Position · Urgency · Raised By · Raised Date · Status (Open / In Progress / Closed) · [View in ATS →]

**Fallback (no integration):** "Connect external ATS in Integration Registry (Page 24, Division F) to see live hiring status here."

---

## 6. API Sync Configuration Panel

> Shown to Group IT Admin context — configuration reference only for transport roles.

| Config Item | Value | Status |
|---|---|---|
| External HRMS Sync Endpoint | Configured in Integration Registry | ✅ / ❌ |
| Sync Frequency | Daily at 02:00 IST | — |
| Last Successful Sync | [Timestamp] | — |
| Sync Errors (last 7 days) | [Count] | — |
| [View Integration Config →] | → Div F Page 24 — Integration Registry | — |

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Hiring request raised | "Driver hiring request raised for [Branch]. ATS notified." | Info | 4s |
| Sync triggered manually | "Driver data sync triggered. Check Driver Registry in 5 minutes." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No hiring requests visible | "No Open Hiring Requests" | "Raise a request or connect external ATS to see live data." | [Raise Driver Hiring Request] |
| ATS not connected | "External ATS Not Connected" | "Connect your ATS in the Integration Registry to view live hiring data." | [→ Integration Registry] |

---

## 9. Role-Based UI Visibility

| Element | Transport Director G3 | Fleet Manager G3 | Safety Officer G3 |
|---|---|---|---|
| Raise Hiring Request | ✅ | ✅ | ❌ |
| View Open Requests | ✅ | ✅ | ✅ |
| Trigger Manual Sync | ✅ | ❌ | ❌ |
| View Integration Config | ✅ (read) | ❌ | ❌ |

---

## 10. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/transport/driver-hr/hiring-requests/` | JWT (G3+) | Open hiring requests from ATS |
| POST | `/api/v1/group/{group_id}/transport/driver-hr/hiring-requests/` | JWT (G3+) | Raise new hiring request |
| POST | `/api/v1/group/{group_id}/transport/drivers/sync/` | JWT (G4+) | Trigger manual sync from HRMS |
| GET | `/api/v1/group/{group_id}/transport/driver-hr/sync-status/` | JWT (G3+) | Last sync timestamp + error count |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
