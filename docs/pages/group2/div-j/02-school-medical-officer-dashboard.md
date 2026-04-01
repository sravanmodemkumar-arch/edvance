# 02 — School Medical Officer Dashboard

> **URL:** `/group/health/medical-officer/`
> **File:** `02-school-medical-officer-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group School Medical Officer (Role 86, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group School Medical Officer. Operational hub for day-to-day clinical oversight across all branches — on-campus doctor coordination, prescription and consultation record management, patient visit logs, referral tracking, and follow-up monitoring.

The School Medical Officer is the clinical operations lead. Unlike the Medical Coordinator who owns infrastructure and policy, the Medical Officer is responsible for the quality and continuity of patient care. They ensure every branch has doctor coverage during school hours, that consultations are documented correctly, that prescriptions are handled safely, and that students referred to hospitals are tracked to resolution. Scale: 50–200 consultations/week across all branches · 2–10 active referrals at any time · 20–100 follow-ups outstanding.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group School Medical Officer | G3 | Full — all sections, consultation entry, referral management | Exclusive dashboard |
| Group Medical Coordinator | G3 | Full view — all sections | Cannot create/edit records directly |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('school_medical_officer')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  School Medical Officer Dashboard
```

### 3.2 Page Header
```
Welcome back, [Officer Name]                    [Export Consultation Report ↓]  [Settings ⚙]
[Group Name] — Group School Medical Officer · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  [N] Consultations Today  ·  [N] Referrals Active
```

### 3.3 Alert Banner (conditional — items requiring same-day clinical action)

| Condition | Banner Text | Severity |
|---|---|---|
| No doctor at branch today (school hours) | "No doctor assigned at [Branch] today during school hours. Immediate resolution required." | Red |
| Patient follow-up overdue > 3 days | "[N] patients have overdue follow-ups. Last overdue: [Patient] at [Branch] — [N] days." | Red |
| Student with chronic condition missed medication | "Student [Name] at [Branch] — chronic condition medication missed today. Nurse to verify." | Red |
| Referral pending hospital response > 2 days | "Referral for [Student] to [Hospital] has had no response for [N] days. Follow up required." | Amber |
| Prescription refill needed | "[N] students require prescription refills within 3 days." | Amber |
| Medical record completeness < 80% | "[Branch] medical records completeness is [N]%. Documentation drive needed." | Amber |
| Consultation backdated > 3 days | "Backdated consultation entry at [Branch]: record for [date] entered today. Audit flag auto-raised." | Amber |

Max 5 alerts visible. Alert links route to relevant sections. "View all health events → Health Audit Log" always shown below alerts.

---

## 4. KPI Summary Bar (7 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Consultations Today | Total across all branches (school hours only) | Blue (informational) | → Section 5.1 |
| Referrals Pending | Active referrals awaiting hospital response or outcome | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.4 |
| Active Prescriptions | Students with ongoing prescriptions group-wide | Blue always | → Consultation drawer |
| Branches with Doctor Today | Count of branches with a doctor on-site now | Green = all · Yellow 1–2 missing · Red > 2 missing | → Section 5.3 |
| Patients Requiring Follow-up | Outstanding follow-ups across all branches | Green = 0 · Yellow 1–10 · Red > 10 | → Section 5.2 |
| Medical Record Completeness % | Records with all required fields completed | Green ≥ 90% · Yellow 75–90% · Red < 75% | → Section 5.1 |
| Open Referrals | Total referrals not yet closed | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.4 |

**HTMX:** `hx-trigger="every 5m"` → Consultations today and branches with doctor auto-refresh.

---

## 5. Sections

### 5.1 Today's Consultations (Live Table)

> Live view of all consultations logged today across all branches. Updates every 5 minutes.

**Search:** Patient name, branch, complaint. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Complaint Category | Checkbox | Fever / Injury / Chronic / Allergy / Mental Health / Other |
| Severity | Checkbox | Routine / Moderate / Severe / Emergency |
| Outcome | Checkbox | Sent Back to Class / Rest at Sick Bay / Referred / Sent Home / Hospitalised |
| Doctor | Multi-select | All doctors active today |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Time | ✅ | HH:MM — consultation start time |
| Branch | ✅ | |
| Patient Type | ✅ | Student / Staff / Visitor |
| Complaint Category | ✅ | |
| Doctor | ✅ | Attending doctor name |
| Severity | ✅ | Colour-coded badge: Routine (Grey) / Moderate (Yellow) / Severe (Orange) / Emergency (Red) |
| Outcome | ✅ | |
| Prescription | ❌ | ✅ Issued / — None |
| Actions | ❌ | View · Edit · Flag Follow-up |

**Default sort:** Time descending (most recent first).
**Pagination:** Server-side · 25/page.

**Auto-refresh:** `hx-trigger="every 5m"` — new consultations appear at top without full page reload.

---

### 5.2 Follow-up Required Table

> Patients across all branches flagged as needing a follow-up visit.

**Search:** Patient name, branch, condition. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Overdue | Checkbox | Show overdue only (due date passed) |
| Condition Category | Checkbox | Injury / Chronic / Post-Referral / Mental Health / Other |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Patient Name | ✅ | Student/Staff name; masked to initials for non-clinical viewers |
| Branch | ✅ | |
| Class / Role | ✅ | Grade + Section (students) or Department (staff) |
| Last Visit | ✅ | Date of most recent consultation |
| Condition | ✅ | Brief diagnosis/condition |
| Follow-up Due | ✅ | Date — Red if overdue |
| Doctor | ✅ | Assigned follow-up doctor |
| Status | ✅ | Pending / Overdue / Completed |
| Actions | ❌ | Log Follow-up · Reschedule · View History |

**Default sort:** Follow-up Due ascending (most overdue first).
**Pagination:** Server-side · 25/page.

---

### 5.3 Branch Doctor Coverage Today

> Real-time view of doctor assignments across all branches for today.

**Display:** Summary grid (table format) — one row per branch.

**Columns:**
| Column | Notes |
|---|---|
| Branch | Branch name |
| Doctor Assigned | Doctor name or ❌ None (Red badge) |
| Specialty | General Physician / Paediatrician / Other |
| On-Site Hours | e.g., 09:00–13:00 |
| Contact | Mobile number |
| Coverage Status | ✅ Present · ⚠ Late · ❌ Absent · — Not Scheduled |
| Actions | Assign Doctor · Contact Doctor |

**Refresh:** `hx-trigger="every 10m"` on coverage status column.

---

### 5.4 Referral Tracker

> All active hospital referrals from any branch, requiring Medical Officer follow-through.

**Search:** Student name, hospital, branch. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Status | Checkbox | Referred / Admitted / Discharged / Lost to Follow-up / Closed |
| Days Open | Radio | All / < 3 days / 3–7 days / > 7 days |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Student Name | ✅ | Masked for non-clinical roles |
| Branch | ✅ | |
| Condition | ✅ | Referral diagnosis/complaint |
| Referred Hospital | ✅ | |
| Referral Date | ✅ | Date of referral |
| Days Open | ✅ | Red if > 7 days |
| Referring Doctor | ✅ | |
| Status | ✅ | Colour-coded badge |
| Follow-up Due | ✅ | Next contact date |
| Actions | ❌ | Update Status · View · Close Referral |

**Default sort:** Days Open descending (longest open first).
**Pagination:** Server-side · 25/page.

---

### 5.5 Quick Actions

| Action | Target |
|---|---|
| Log Consultation | Opens `consultation-log` drawer |
| Schedule Doctor Visit | → Page 07 (visit create drawer) |
| View Patient Records | → Patient record search modal |
| Flag Follow-up | Opens follow-up flag modal |
| Export Consultation Report | Download CSV — current day or date range |

---

## 6. Drawers

### 6.1 Drawer: `consultation-log` — Log / View Consultation
- **Trigger:** "Log Consultation" quick action, or Actions → View/Edit on consultation row
- **Width:** 620px
- **Mode:** Create (new) or View/Edit (existing record)

**Fields:**
| Field | Type | Notes |
|---|---|---|
| Branch | Select | Branch where consultation occurred |
| Patient Type | Radio | Student / Staff / Visitor |
| Patient Name / ID | Lookup | Type-ahead from student/staff roster |
| Date & Time | DateTime | Default: now |
| Doctor | Select | From doctor registry, filtered by branch |
| Chief Complaint | Text | Free text |
| Complaint Category | Select | Fever / Injury / Chronic / Allergy / Headache / Stomach / Mental Health / Other |
| Severity | Radio | Routine / Moderate / Severe / Emergency |
| Examination Notes | Textarea | Clinical notes |
| Diagnosis | Text | |
| Prescription Issued | Toggle | Show/hide prescription section |
| Prescription Details | Textarea | Medicine name, dose, frequency, duration |
| Outcome | Select | Sent Back to Class / Rest at Sick Bay / Sent Home / Referred / Hospitalised |
| Referral Details | Conditional | Hospital name, doctor, reason — shows if Outcome = Referred or Hospitalised |
| Follow-up Required | Toggle | If Yes: follow-up date, follow-up doctor |
| Notes | Textarea | Internal notes |

**Validation:** Patient must be on roster · Doctor must be assigned to branch · Referral fields mandatory if outcome is Referred.

### 6.2 Drawer: `referral-update` — Update Referral Status
- **Trigger:** Actions → Update Status on referral row
- **Width:** 520px
- **Fields:** Status (select) · Hospital update notes · Discharge date (if discharged) · Follow-up action required (toggle) · Next review date

---

### 6.3 Drawer: `quick-assign-doctor` — Assign Doctor to Branch
- **Trigger:** Actions → Assign Doctor in Section 5.3 Branch Doctor Coverage table; empty-state [Assign Doctor] CTA
- **Width:** 480px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Select | Pre-selected from row context; read-only |
| Doctor | Lookup | Type-ahead from medical staff registry — filters to doctors available today |
| Specialty | Read-only | Auto-populated from selected doctor's profile |
| On-Site Date | Date | Default: today |
| On-Site From | Time | Required |
| On-Site To | Time | Required; must be after From |
| Coverage Type | Radio | Scheduled Replacement / Emergency Cover / Temporary |
| Contact Number | Text | Pre-populated from doctor profile; editable |
| Notes | Textarea | Optional — reason for assignment |
| Notify Medical Coordinator | Checkbox | Default ✅ — sends alert to Role 85 |

**Validation:** Doctor must have an active registration (non-expired MCI). Cannot assign same doctor to two branches with overlapping hours on the same day. Minimum 1-hour slot required.

**On success:** Drawer closes; coverage grid row updates via `hx-swap-oob="true"` to show new doctor; KPI card "Branches with Doctor Today" refreshes.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Consultation logged | "Consultation logged for [Patient] at [Branch]." | Success | 4s |
| Consultation updated | "Consultation record updated." | Success | 4s |
| Referral updated | "Referral status updated for [Student] — [Status]." | Success | 4s |
| Follow-up flagged | "Follow-up flagged for [Patient]. Due: [date]." | Info | 4s |
| Follow-up completed | "Follow-up marked complete for [Patient]." | Success | 4s |
| Doctor absence alert sent | "Doctor absence alert sent to Medical Coordinator for [Branch]." | Warning | 5s |
| Doctor assigned to branch | "Dr [Name] assigned to [Branch] for [date] [from]–[to]." | Success | 4s |
| Consultation report exported | "Report export prepared. Download ready." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No consultations today | "No Consultations Yet Today" | "No consultations have been logged today across any branch." | [Log Consultation] |
| No follow-ups outstanding | "All Follow-ups Complete" | "No patients have pending follow-up visits." | — |
| No active referrals | "No Active Referrals" | "There are no hospital referrals currently open." | — |
| Search returns no results | "No Results Found" | "No patients or consultations match your search." | [Clear Search] |
| Branch has no doctor today | "No Doctor Coverage" | "No doctor is assigned to this branch today." | [Assign Doctor] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 7 KPI cards + consultations table + follow-up table + coverage grid + alerts |
| Consultations table auto-refresh | Shimmer overlay on table body only; headers preserved |
| Filter/search on any table | Inline skeleton rows (8 rows) |
| Consultation log drawer open | 620px drawer form skeleton |
| Referral update drawer | 520px drawer skeleton |
| Doctor coverage refresh | Row shimmer on status column only |

---

## 10. Role-Based UI Visibility

| Element | School Medical Officer G3 | Medical Coordinator G3 |
|---|---|---|
| Log Consultation | ✅ | ❌ (view only) |
| Edit Consultation | ✅ (own branch records same day) | ❌ |
| Update Referral Status | ✅ | ❌ |
| Flag Follow-up | ✅ | ❌ |
| Assign Doctor to Branch | ✅ | ✅ |
| View All Branches Data | ✅ | ✅ |
| Export Report | ✅ | ✅ |
| View Prescription Details | ✅ | ✅ |
| Delete Consultation Record | ❌ (log only — no deletion) | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/medical-officer/dashboard/` | JWT (G3+) | Full dashboard data payload |
| GET | `/api/v1/group/{group_id}/health/medical-officer/kpi-cards/` | JWT (G3+) | KPI auto-refresh values |
| GET | `/api/v1/group/{group_id}/health/consultations/today/` | JWT (G3+) | Today's consultation list, filterable |
| POST | `/api/v1/group/{group_id}/health/consultations/` | JWT (G3+) | Create new consultation record |
| PATCH | `/api/v1/group/{group_id}/health/consultations/{id}/` | JWT (G3+) | Update consultation |
| GET | `/api/v1/group/{group_id}/health/consultations/{id}/` | JWT (G3+) | Single consultation detail |
| GET | `/api/v1/group/{group_id}/health/follow-ups/` | JWT (G3+) | Follow-up required list |
| POST | `/api/v1/group/{group_id}/health/follow-ups/{id}/complete/` | JWT (G3+) | Mark follow-up complete |
| GET | `/api/v1/group/{group_id}/health/referrals/` | JWT (G3+) | Active referrals list |
| PATCH | `/api/v1/group/{group_id}/health/referrals/{id}/` | JWT (G3+) | Update referral status |
| GET | `/api/v1/group/{group_id}/health/doctor-coverage/today/` | JWT (G3+) | Today's branch doctor coverage |
| POST | `/api/v1/group/{group_id}/health/doctor-coverage/assign/` | JWT (G3+) | Assign doctor to branch for a date/slot |
| POST | `/api/v1/group/{group_id}/health/medical-officer/export/` | JWT (G3+) | Initiate async consultation report export; returns `{job_id}` |
| GET | `/api/v1/group/{group_id}/health/medical-officer/export/status/{job_id}/` | JWT (G3+) | Poll export job status (`pending` / `ready` / `failed`) |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../medical-officer/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Consultations table refresh | `every 5m` | GET `.../consultations/today/` | `#consultations-table-body` | `innerHTML` |
| Doctor coverage refresh | `every 10m` | GET `.../doctor-coverage/today/` | `#coverage-grid` | `innerHTML` |
| Consultation search | `input delay:300ms` | GET `.../consultations/today/?q={val}` | `#consultations-table-body` | `innerHTML` |
| Follow-up search | `input delay:300ms` | GET `.../follow-ups/?q={val}` | `#followup-table-body` | `innerHTML` |
| Referral search | `input delay:300ms` | GET `.../referrals/?q={val}` | `#referral-table-body` | `innerHTML` |
| Filter apply (any table) | `click` | GET `.../?{filters}` | `#{table}-section` | `innerHTML` |
| Open consultation drawer | `click` | GET `.../consultations/{id}/` | `#drawer-body` | `innerHTML` |
| Submit consultation log | `click` | POST `.../consultations/` | `#consultations-table-section` | `innerHTML` |
| Mark follow-up complete | `click` | POST `.../follow-ups/{id}/complete/` | `#followup-row-{id}` | `outerHTML` |
| Open quick-assign-doctor drawer | `click` Assign Doctor | GET `.../health/medical-staff/?available=today&type=doctor` | `#drawer-body` | `innerHTML` |
| Submit doctor assignment | `click` Save | POST `.../health/doctor-coverage/assign/` | `#coverage-row-{branch_id}` | `outerHTML` |
| OOB KPI refresh on doctor assign | (triggered by assign POST response) | — | `#kpi-bar` | `hx-swap-oob="true"` |
| Initiate export | `click` | POST `.../medical-officer/export/` | `#export-status` | `innerHTML` |
| Poll export status | `every 5s [!#export-done]` | GET `.../medical-officer/export/status/{job_id}/` | `#export-status` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
