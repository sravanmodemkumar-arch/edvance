# Division J — Health & Medical: Page Index

> 24 pages · 5 roles (85–89) · Group Medical Coordinator · School Medical Officer · Mental Health Coordinator · Medical Insurance Coordinator (G0) · Emergency Response Officer

---

## Role Dashboards (4 pages)

| # | File | Title | Priority | Primary Role |
|---|---|---|---|---|
| 01 | `01-medical-coordinator-dashboard.md` | Medical Coordinator Dashboard | P0 | Role 85 — Group Medical Coordinator |
| 02 | `02-school-medical-officer-dashboard.md` | School Medical Officer Dashboard | P0 | Role 86 — Group School Medical Officer |
| 03 | `03-mental-health-coordinator-dashboard.md` | Mental Health Coordinator Dashboard | P0 | Role 87 — Group Mental Health Coordinator |
| 04 | `04-emergency-response-officer-dashboard.md` | Emergency Response Officer Dashboard | P0 | Role 89 — Group Emergency Response Officer |

---

## Medical Infrastructure (4 pages)

| # | File | Title | Priority | Primary Role |
|---|---|---|---|---|
| 05 | `05-medical-room-register.md` | Medical Room Register | P0 | Role 85 — Group Medical Coordinator |
| 06 | `06-doctor-medical-staff-registry.md` | Doctor & Medical Staff Registry | P1 | Role 85 — Group Medical Coordinator |
| 07 | `07-doctor-visit-schedule.md` | Doctor Visit Schedule | P1 | Role 85 — Group Medical Coordinator |
| 08 | `08-medicine-first-aid-inventory.md` | Medicine & First Aid Inventory | P0 | Role 85 — Group Medical Coordinator |

---

## Patient & Health Records (3 pages)

| # | File | Title | Priority | Primary Role |
|---|---|---|---|---|
| 09 | `09-patient-consultation-register.md` | Patient Consultation Register | P0 | Role 86 — Group School Medical Officer |
| 10 | `10-student-health-records.md` | Student Health Records | P0 | Role 85 — Group Medical Coordinator |
| 11 | `11-health-screening-manager.md` | Health Screening Manager | P1 | Role 85 — Group Medical Coordinator |

---

## Mental Health (4 pages)

| # | File | Title | Priority | Primary Role |
|---|---|---|---|---|
| 12 | `12-counsellor-registry.md` | Counsellor Registry | P1 | Role 87 — Group Mental Health Coordinator |
| 13 | `13-counselling-session-register.md` | Counselling Session Register | P0 | Role 87 — Group Mental Health Coordinator |
| 14 | `14-student-wellbeing-tracker.md` | Student Wellbeing Tracker | P0 | Role 87 — Group Mental Health Coordinator |
| 15 | `15-mental-health-programs.md` | Mental Health Programs | P1 | Role 87 — Group Mental Health Coordinator |

---

## Insurance (2 pages)

| # | File | Title | Priority | Primary Role |
|---|---|---|---|---|
| 16 | `16-insurance-policy-manager.md` | Insurance Policy Manager | P1 | Role 85 — Group Medical Coordinator |
| 17 | `17-insurance-claim-register.md` | Insurance Claim Register | P1 | Role 85 — Group Medical Coordinator |

---

## Emergency Response (5 pages)

| # | File | Title | Priority | Primary Role |
|---|---|---|---|---|
| 18 | `18-emergency-protocol-library.md` | Emergency Protocol Library | P0 | Role 89 — Group Emergency Response Officer |
| 19 | `19-emergency-drill-scheduler.md` | Emergency Drill Scheduler | P1 | Role 89 — Group Emergency Response Officer |
| 20 | `20-emergency-incident-register.md` | Emergency Incident Register | P0 | Role 89 — Group Emergency Response Officer |
| 21 | `21-hospital-ambulance-directory.md` | Hospital & Ambulance Directory | P0 | Role 89 — Group Emergency Response Officer |
| 22 | `22-first-responder-training.md` | First Responder Training Register | P1 | Role 89 — Group Emergency Response Officer |

---

## Analytics & Compliance (2 pages)

| # | File | Title | Priority | Primary Role |
|---|---|---|---|---|
| 23 | `23-health-analytics.md` | Health Analytics Dashboard | P1 | Role 85 — Group Medical Coordinator |
| 24 | `24-medical-compliance-report.md` | Medical Compliance Report | P1 | Role 85 — Group Medical Coordinator |

---

## Page Count Summary

| Category | Pages |
|---|---|
| Role Dashboards | 4 |
| Medical Infrastructure | 4 |
| Patient & Health Records | 3 |
| Mental Health | 4 |
| Insurance | 2 |
| Emergency Response | 5 |
| Analytics & Compliance | 2 |
| **Total** | **24** |

---

## Role → Pages Mapping

| Role | Level | Pages Owned |
|---|---|---|
| Role 85 — Group Medical Coordinator | G3 | 01, 05, 06, 07, 08, 10, 11, 16, 17, 23, 24 (primary on 11 pages; co-access on all others) |
| Role 86 — Group School Medical Officer | G3 | 02, 09 (primary on 2 pages; branch-scoped create/view on consultation register, claim register, patient records, hospital directory) |
| Role 87 — Group Mental Health Coordinator | G3 | 03, 12, 13, 14, 15 (primary on 5 pages; view access on mental health section of analytics) |
| Role 88 — Group Medical Insurance Coordinator | G0 — No platform login | External actor only; no platform pages owned. Feeds policy and claim data externally to Role 85. |
| Role 89 — Group Emergency Response Officer | G3 | 04, 18, 19, 20, 21, 22 (primary on 6 pages; co-view on incident analytics, compliance emergency columns, and hospital directory) |

---

## URL Summary

| # | URL |
|---|---|
| 01 | `/group/health/` |
| 02 | `/group/health/smo-dashboard/` |
| 03 | `/group/health/mh-dashboard/` |
| 04 | `/group/health/ero-dashboard/` |
| 05 | `/group/health/medical-rooms/` |
| 06 | `/group/health/medical-staff/` |
| 07 | `/group/health/doctor-visits/` |
| 08 | `/group/health/medicine-inventory/` |
| 09 | `/group/health/consultations/` |
| 10 | `/group/health/student-health-records/` |
| 11 | `/group/health/screenings/` |
| 12 | `/group/health/counsellors/` |
| 13 | `/group/health/counselling-sessions/` |
| 14 | `/group/health/wellbeing-tracker/` |
| 15 | `/group/health/mh-programs/` |
| 16 | `/group/health/insurance-policies/` |
| 17 | `/group/health/insurance-claims/` |
| 18 | `/group/health/emergency-protocols/` |
| 19 | `/group/health/drills/` |
| 20 | `/group/health/incidents/` |
| 21 | `/group/health/hospital-directory/` |
| 22 | `/group/health/first-responder-training/` |
| 23 | `/group/health/analytics/` |
| 24 | `/group/health/compliance/` |

---

## API Base URL Structure

All Division J endpoints follow the pattern:

```
/api/v1/group/{group_id}/health/{resource}/
```

Examples:
- `/api/v1/group/{group_id}/health/insurance-claims/`
- `/api/v1/group/{group_id}/health/emergency-protocols/`
- `/api/v1/group/{group_id}/health/drills/`
- `/api/v1/group/{group_id}/health/incidents/`
- `/api/v1/group/{group_id}/health/hospital-directory/`
- `/api/v1/group/{group_id}/health/first-responder-training/`
- `/api/v1/group/{group_id}/health/analytics/`
- `/api/v1/group/{group_id}/health/compliance/`

---

## Technical Stack

| Layer | Technology |
|---|---|
| Backend framework | Django 4.2 + HTMX 1.9 |
| API layer | FastAPI (analytics and compliance endpoints); Django REST for CRUD modules |
| Database | PostgreSQL 16 |
| Authentication | JWT with `@require_role(...)` decorator |
| Base template | `portal_base.html` |
| File storage | Django FileField with server-side storage |
| Background jobs | Django management commands / Celery (export jobs) |
| Scale | 150 groups · 5–50 branches per group · up to 100,000 students per large group |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
