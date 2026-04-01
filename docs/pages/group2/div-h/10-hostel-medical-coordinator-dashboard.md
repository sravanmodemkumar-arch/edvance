# 10 — Hostel Medical Coordinator Dashboard

> **URL:** `/group/hostel/medical/`
> **File:** `10-hostel-medical-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Hostel Medical Coordinator (Role 76, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Hostel Medical Coordinator. Manages medical infrastructure across all hostel campuses — medical room operational status, doctor visit schedules, medical room visit logs, prescription tracking, hosteler health condition monitoring, and medical emergency response coordination.

In large hostel campuses, medical rooms serve 200–3,000 students. Boys and girls medical facilities may be on separate campuses. The Coordinator does not provide clinical diagnosis — they coordinate doctor availability, track medical visits, maintain basic health records for hostelers, and escalate emergencies to the Group Emergency Response Officer.

**Key requirements:**
- Every hostel campus with > 50 students must have a functional medical room (CBSE boarding norms)
- Doctor must visit at least twice per week for campuses with > 200 hostelers
- Medical emergencies must be escalated within 15 minutes to the Group Emergency Response Officer
- Female doctor / nurse must be available for girls hostel consultations

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Hostel Medical Coordinator | G3 | Full — all branches, both genders | Exclusive dashboard |
| Group Hostel Welfare Officer | G3 | View — medical incidents linked to welfare | Read-only |
| Group Hostel Director | G3 | View — medical summary | Via own dashboard |
| Group Emergency Response Officer | G3 | View — emergency flags (cross-system) | Via own portal |
| Branch Doctor / Nurse | Branch role | Report only | Via branch portal |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Medical Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]         [+ Log Medical Visit]  [Export Report ↓]  [Settings ⚙]
Group Hostel Medical Coordinator · Today: [date]
Medical Visits Today: [N]  ·  Emergencies (Active): [N]  ·  Medical Rooms Operational: [N/N]
```

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Active medical emergency | "MEDICAL EMERGENCY: [Hosteler Name] at [Branch] — [description]. Emergency Response Officer alerted." | Red |
| Medical room non-operational at any hostel | "Medical room at [Branch] [Boys/Girls] Hostel is non-operational. Compliance breach." | Red |
| Doctor visit overdue (> 7 days at ≥200-hosteler campus) | "Doctor visit overdue at [Branch] — last visit [N] days ago. Schedule immediately." | Amber |
| No nurse/female doctor at girls hostel | "Girls hostel at [Branch] has no female medical staff assigned." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Medical Rooms Operational | Functional / Total configured | Green = 100% · Yellow < 100% · Red any non-functional | → Page 27 |
| Medical Visits Today | Total medical room visits logged today | Blue always | → Page 27 |
| Active Emergencies | Hostelers with current medical emergency flag | Green = 0 · Red > 0 | → Page 27 |
| Doctor Visits This Month | Doctor visit sessions completed (all branches) | Blue always | → Page 27 |
| Hostelers on Medical Watch | Hostelers with ongoing medical conditions requiring monitoring | Yellow > 0 | → Page 27 |
| Prescriptions Pending Pickup | Logged prescriptions not yet marked collected | Yellow > 0 | → Page 27 |

**HTMX:** `hx-trigger="every 5m"` → KPI auto-refresh (medical emergencies require near-real-time monitoring).

---

## 5. Sections

### 5.1 Medical Room Status

> Operational status of every hostel medical room.

**Columns:** Branch | Hostel Type | Medical Room Status | Nurse on Duty | Doctor Name | Next Doctor Visit | Last Visit | [View →]

Status badges: ✅ Operational / ⚠ No nurse on duty / ❌ Non-operational.

**Red rows:** Girls hostel with no female medical staff, or any non-operational medical room.

---

### 5.2 Active Medical Cases

> Hostelers requiring medical attention or monitoring today.

**Display:** Card list.

**Card fields:**
- Hosteler Name + Gender badge
- Branch + Hostel type
- Condition/Complaint summary
- Severity: Emergency / Monitoring / Routine
- Doctor assigned
- Last update + actor
- [Update →] [Escalate to Emergency Response →] [Close →]

---

### 5.3 Doctor Visit Schedule

> Upcoming doctor visits across all branches.

**Columns:** Branch | Doctor Name | Specialty | Visit Date | Visit Time | Boys/Girls/Both | Status | [Edit] [Cancel]

**Today's visits highlighted.** Overdue visits (past scheduled date, not completed) shown in red.

---

### 5.4 Medical Visits Table (This Week)

> All medical room visits logged this week.

**Search:** Hosteler name, branch. 300ms debounce.

**Filters:** Branch · Gender · Date range · Severity (Emergency/Routine/Follow-up).

**Columns:**
| Column | Sortable |
|---|---|
| Visit # | ✅ |
| Date/Time | ✅ |
| Hosteler Name | ✅ |
| Gender | ✅ |
| Branch | ✅ |
| Complaint | ✅ |
| Doctor/Nurse | ✅ |
| Prescription | ✅ |
| Severity | ✅ |
| Follow-up Required | ✅ |
| Actions | ❌ |

**Pagination:** Server-side · 25/page.

---

### 5.5 Hostelers on Medical Watch

> Hostelers with flagged medical conditions requiring ongoing monitoring.

**Columns:** Hosteler · Branch · Condition · Doctor · Last Check · Next Scheduled Check · [View →]

---

## 6. Drawers

### 6.1 Drawer: `medical-visit-create`
- **Trigger:** + Log Medical Visit
- **Width:** 560px
- **Fields:**
  - Branch (dropdown)
  - Hostel Type (Boys / Girls radio)
  - Hosteler (search autocomplete — mandatory)
  - Visit Date + Time
  - Doctor / Nurse name
  - Chief Complaint (text, required)
  - Diagnosis / Assessment (text)
  - Prescription (textarea — drug name, dose, frequency, duration)
  - Severity: Routine / Follow-up Required / Medical Watch / Emergency
  - If Emergency: escalate to Group Emergency Response Officer (auto-checked)
  - Next Visit Date (if follow-up)
  - Notify Parent (checkbox — mandatory for Emergency)
- **On submit:** Visit logged; if Emergency → POST to emergency response endpoint; parent WhatsApp sent

### 6.2 Drawer: `doctor-visit-schedule-create`
- **Trigger:** + Schedule Doctor Visit
- **Width:** 520px
- **Fields:** Branch · Doctor Name · Specialty · Date · Time · Hostel type (Boys/Girls/Both) · Recurring (checkbox: weekly/bi-weekly)

### 6.3 Modal: Medical Emergency Escalation
- **Trigger:** Active Cases → Escalate to Emergency Response
- **Type:** Centred modal (480px)
- **Content:** Hosteler details, condition summary
- **Required:** Emergency description + current action taken + ambulance required (Yes/No)
- **On confirm:** Emergency Response Officer alerted; Branch Principal notified; parent notified; audit log

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Medical visit logged | "Medical visit logged for [Hosteler Name]." | Success | 4s |
| Emergency escalated | "Medical emergency escalated. Emergency Response Officer and parent notified." | Error | Manual dismiss |
| Doctor schedule created | "Doctor visit scheduled at [Branch] for [date]." | Success | 4s |
| Prescription marked collected | "Prescription marked as collected by [Hosteler Name]." | Success | 3s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No medical visits today | "No Medical Visits Logged Today" | "No hostelers have visited the medical room today." | [+ Log Medical Visit] |
| No active emergencies | "No Active Medical Emergencies" | — | — |
| No doctor visits scheduled | "No Doctor Visits Scheduled" | "Schedule regular doctor visits for all hostel campuses." | [+ Schedule Doctor Visit] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 6 KPI cards + medical room status table + active cases + doctor schedule |
| KPI auto-refresh (5m) | Shimmer on card values |
| Medical visit log submit | Spinner on Submit; active cases section refreshes |
| Emergency escalation confirm | Spinner on Confirm + full-page overlay "Alerting Emergency Response…" |

---

## 10. Role-Based UI Visibility

| Element | Medical Coordinator G3 | Welfare Officer G3 | Hostel Director G3 |
|---|---|---|---|
| Log Medical Visit | ✅ | ❌ | ❌ |
| Schedule Doctor Visit | ✅ | ❌ | ✅ |
| View girls hostel medical data | ✅ | ✅ (welfare link only) | ✅ |
| Escalate Emergency | ✅ | ✅ (via welfare) | ✅ |
| Export medical report | ✅ | ❌ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/medical/dashboard/` | JWT (G3+) | Dashboard data |
| GET | `/api/v1/group/{group_id}/hostel/medical/kpi-cards/` | JWT (G3+) | KPI auto-refresh |
| GET | `/api/v1/group/{group_id}/hostel/medical/rooms/` | JWT (G3+) | Medical room status |
| GET | `/api/v1/group/{group_id}/hostel/medical/cases/active/` | JWT (G3+) | Active medical cases |
| GET | `/api/v1/group/{group_id}/hostel/medical/visits/` | JWT (G3+) | Medical visits (paginated, filtered) |
| POST | `/api/v1/group/{group_id}/hostel/medical/visits/` | JWT (G3+) | Log new medical visit |
| GET | `/api/v1/group/{group_id}/hostel/medical/doctor-schedule/` | JWT (G3+) | Doctor visit schedule |
| POST | `/api/v1/group/{group_id}/hostel/medical/doctor-schedule/` | JWT (G3+) | Schedule doctor visit |
| POST | `/api/v1/group/{group_id}/hostel/medical/cases/{id}/emergency/` | JWT (G3+) | Escalate emergency |
| GET | `/api/v1/group/{group_id}/hostel/medical/watch-list/` | JWT (G3+) | Hostelers on medical watch |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../medical/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Active cases refresh | `every 5m` | GET `.../medical/cases/active/` | `#active-cases` | `innerHTML` |
| Visit search | `input delay:300ms` | GET `.../medical/visits/?q={val}` | `#visits-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../medical/visits/?{filters}` | `#visits-table-section` | `innerHTML` |
| Log visit submit | `click` | POST `.../medical/visits/` | `#visits-table-section` | `innerHTML` |
| Emergency escalate confirm | `click` | POST `.../cases/{id}/emergency/` | `#active-cases` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
