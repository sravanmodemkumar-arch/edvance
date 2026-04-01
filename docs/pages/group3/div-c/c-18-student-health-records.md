# C-18 — Student Health & Medical Records

> **URL:** `/school/students/health/`
> **File:** `c-18-student-health-records.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Class Teacher (S3) — own class (view + notes) · Administrative Officer (S3) — full · Principal (S6) — full

---

## 1. Purpose

Maintains student health and medical records that the school needs to know about to provide appropriate care and make adjustments. Indian schools are required under RTE Act and NEP 2020 to conduct annual health checkups for students and maintain health cards. CBSE affiliation norms also recommend schools maintain student health records.

This page covers:
- **Chronic conditions:** Asthma, epilepsy, diabetes, heart condition, food allergy — Class Teacher and office staff need to know these for emergencies
- **Disability status:** Feeds into C-19 (CWSN Register) and B-11 (Exam Configuration) for accommodation
- **Annual health checkup records:** Height, weight, BMI, vision, dental — government schools receive this from NRHM health teams; private schools do this voluntarily or via contracted doctor
- **Vaccination status:** Schools may track basic vaccinations for young students

This is NOT a medical records system — it is a school-appropriate summary of medically relevant information that teachers and school staff need for duty of care.

---

## 2. Page Layout

### 2.1 Header
```
Student Health Records                        [Annual Health Checkup Entry]  [Export Health Cards]
Academic Year: 2026–27  |  Class: [All ▼]
Health Records Entered: 312 / 380 (82%)  ·  Medical Conditions Flagged: 28  ·  Disabilities: 5
```

### 2.2 Student Health Summary (per class)
```
Class VIII-A — 42 students

Roll  Name             Conditions     Allergy  Disability  BMI     Vision   Status
01    Anjali Das       Asthma ⚠️      None     None        18.2    Normal   ✅
02    Arjun Sharma     None           Peanut⚠️ None        19.1    Normal   ✅
03    Priya Venkat     Epilepsy ⚠️    None     None        16.8    —        ⬜ Incomplete
04    Rohit Kumar      None           None     Visual(L)   17.2    Partial  Linked→C-19
```

---

## 3. Student Health Record

Clicking a student row → health record view/edit:

### 3.1 Emergency Medical Info (Critical — seen by Class Teacher)
| Field | Value |
|---|---|
| Blood Group | B+ |
| Chronic Conditions | Asthma (mild) — has inhaler |
| Food Allergies | Peanuts — anaphylaxis risk; EpiPen with school nurse |
| Medication (regular) | Salbutamol inhaler — before PE class |
| Medical Alert | Do not give milk products |
| Emergency Action | In case of wheezing: give inhaler; if no relief in 5min: call parent and 108 |
| Emergency Contact (Medical) | Dr. Rajesh (Father) — 9876543210 |

### 3.2 Annual Health Checkup (Latest — 2025–26)
| Parameter | Value | Normal Range | Status |
|---|---|---|---|
| Date of Checkup | 15 Jul 2025 | | |
| Checkup By | Dr. Meena Nair (School Doctor) | | |
| Height | 152 cm | | |
| Weight | 42 kg | | |
| BMI | 18.2 | 18.5–24.9 | ⚠️ Slightly under |
| Vision (Right Eye) | 6/6 | 6/6 | ✅ |
| Vision (Left Eye) | 6/6 | 6/6 | ✅ |
| Dental | No cavities | | ✅ |
| Haemoglobin | 11.8 g/dL | >12 g/dL | ⚠️ Mild anaemia |
| Referral | Nutritionist referral for low BMI | | |

### 3.3 Disability / Special Need
| Field | Value |
|---|---|
| Disability Type | None |
| Disability Certificate | N/A |
| CWSN Register | N/A (no disability) |
| Exam Accommodation | None required |

(If disability flagged: auto-links to C-19 CWSN Register.)

### 3.4 Vaccination Record (optional; mainly for Nursery–Class V)
| Vaccine | Required Age | Status | Date |
|---|---|---|---|
| MMR 2nd dose | 5 years | ✅ Done | Jan 2021 |
| DPT Booster | 10 years | ✅ Done | Apr 2026 |
| HPV (girls) | 9–14 years | ⬜ Pending | — |

---

## 4. Annual Health Checkup Entry

[Annual Health Checkup Entry] → batch entry mode:

School can enter health checkup data for entire classes at once (when a visiting doctor conducts checkup):
```
Annual Health Checkup — Class VI-A — 15 Jul 2025
Checkup Doctor: Dr. Meena Nair (School Doctor)

Roll  Name           Height  Weight  Vision R  Vision L  Referral
01    Anjali Das     148     40      6/6       6/6       —
02    Arjun Sharma   152     42      6/6       6/6       Nutrition
...
```

Bulk entry with Tab navigation between cells.

---

## 5. Medical Conditions Report

[Export] → class-teacher view (shared as PDF in staff meeting):

```
CONFIDENTIAL — Medical Conditions — Class VIII-A
For Class Teacher Use Only

Roll  Student         Condition         Action Required
01    Anjali Das      Asthma            Inhaler in school bag; no cold drinks
02    Arjun Sharma    Peanut Allergy    EpiPen with nurse; check snacks at events
03    Priya Venkat    Epilepsy          First aid: safe position; time seizure; call 108 if > 5min
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/{student_id}/health/` | Student health record |
| 2 | `PATCH` | `/api/v1/school/{id}/students/{student_id}/health/` | Update health record |
| 3 | `POST` | `/api/v1/school/{id}/students/health/checkup/bulk/` | Bulk annual checkup entry |
| 4 | `GET` | `/api/v1/school/{id}/students/health/conditions/?class_id={id}` | Class-wise medical conditions report |
| 5 | `GET` | `/api/v1/school/{id}/students/health/export/?class_id={id}` | Export health cards |

---

## 7. Business Rules

- Health records are DPDPA-sensitive (health data is a sensitive personal data category) — access limited to Class Teacher (own class only), Admin Officer, and Principal; no broader access
- Medical conditions and allergies are shared with Class Teacher on a need-to-know basis for duty of care — this is legally justified under DPDPA 2023 "reasonable purpose" clause
- Annual health checkup data is optional (not mandatory for private schools in most states) but recommended — if a school decides not to use it, this module can be disabled via feature flag
- If disability is recorded, the system auto-creates a placeholder in C-19 CWSN Register if one doesn't exist
- Health records of students are retained for 5 years after the student leaves the school; after 5 years, personal identifiers are removed but aggregate data (BMI trends, common conditions) may be kept for school health planning

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
