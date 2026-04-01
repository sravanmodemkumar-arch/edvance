# J-06 — Health & Wellness Records

> **URL:** `/school/welfare/health/`
> **File:** `j-06-health-wellness.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Counsellor (S3) — mental wellness flags · School Doctor/Nurse (S3) — medical records · Class Teacher (S3) — view wellness flags for own class · Principal (S6) — aggregate health reports · Parent (via N-portal) — own child's record only

---

## 1. Purpose

Maintains student health and wellness records at the school level — separate from the hostel medical room (H-07) but linked to it. Covers:
- Routine medical information (blood group, allergies, chronic conditions)
- Sick room visits and first-aid events during school hours
- Annual health check-up records (CBSE mandates health check-ups)
- Mental wellness flags (from J-01 counsellor and E-09 attendance triggers)
- Emergency medical information accessible quickly by any teacher in an emergency

CBSE Affiliation Bye-Laws require every school to maintain medical records for students and conduct annual health check-ups for all students.

Privacy: A student's health data is among the most sensitive personal data (DPDPA 2023 — special category). Class teachers can see only "wellness flags" not diagnosis; health records are accessible only to the medical staff, counsellor (mental wellness part), and Principal.

---

## 2. Student Health Profile

```
Student Health Profile — Priya Venkat (XI-A)

⚠️ MEDICAL — Accessible to School Nurse + Principal. Class teacher sees ONLY the flag.

Basic Health Information:
  Blood group: B+
  Height: 162 cm (last measured: Jun 2026)  ·  Weight: 52 kg
  BMI: 19.8 (normal range) ✅

Known Allergies:
  🚨 SEVERE ALLERGY: Peanuts — anaphylaxis risk
     Action: Epipen available in nurse's room (batch: 2026-12)
             Teacher briefed: ✅ (all class teachers of XI-A informed without naming other students)
             Canteen briefed: ✅ (peanut-free options marked for this student)
             Emergency contacts: Parent (Mother — +91 9876-XXXXX) [CALL IMMEDIATELY if reaction]

  Mild: Dust — seasonal rhinitis — no medication needed

Chronic Conditions:
  None currently active

Current Medications (school hours):
  None

Vision:
  Corrected vision: Uses spectacles (power: -2.5/-2.0)
  Teachers notified to seat near front: ✅ (all class teachers)

Last Annual Health Check: 15 June 2026 ✅
Next due: June 2027

Vaccination status:
  School-administered vaccinations this year: HPV (state govt programme — girls Class X–XI)
  Parent consent: ✅ signed 10 Jun 2026
  Administered: 18 Jun 2026 ✅
```

---

## 3. Sick Room Register (School Hours)

```
Sick Room Register — 27 March 2026

Visit No.  Time    Student      Class  Complaint           Action            Outcome
SRM/001    8:45 AM Rahul P.     IX-B   Headache            Rest 30 min       Returned to class
SRM/002    10:20 AM Meena S.    VII-A  Stomach ache        Rest; parent called Parent picked up 11:30 AM
SRM/003    1:30 PM Vikram G.    XI-B   Nose bleed (minor)  First aid applied Returned to class 1:45 PM

[+ Log New Visit]

Visit No.: SRM/004
Time: [3:00 PM]
Student: [____________]  Class: [___]
Complaint: [_________]
Initial assessment by: ● Teacher  ○ Nurse  ○ Self-referred
Action:
  ○ Sent home (parent called)  ● Rest in sick room (30–60 min)
  ○ First aid applied  ○ Referred to hospital
  ○ Medication administered: [Drug name]  [Dose]  [Parent pre-consent on file: ✅/⬜]

Note on medication: School staff may only administer pre-consented medications
  (parent has submitted a written consent with the specific drug, dose, and condition);
  No over-the-counter drugs are given without parental consent except basic first aid.

POCSO flag: If a student visits sick room with unexplained injuries, bruises,
  or injury patterns inconsistent with the stated cause → flag to POCSO DO (J-02)
  [This student has unexplained injury — flag for DO review]
```

---

## 4. Annual Health Check-Up

```
Annual Health Check-Up Programme — 2026–27

Date: 15 June 2026
Agency: Government School Health Programme (CBSE + State Health Dept)
Doctor: Dr. Anita Rao (MBBS) — visiting doctor

Coverage: 380 students (all students)
Completed: 362/380 (18 absent on that day — makeup scheduled 30 Jun 2026)

Parameters checked:
  ☑ Height and weight (BMI calculation)
  ☑ Vision (Snellen chart)
  ☑ Hearing (basic whisper test)
  ☑ Dental check
  ☑ Blood pressure (Class IX–XII)
  ☑ Haemoglobin / anaemia screening (girls — state programme)
  ☑ General physical examination

Findings summary (anonymised aggregate):
  Underweight (BMI <18.5): 12 students (3.2%) → parent letters sent with nutrition guidance
  Overweight (BMI >25): 8 students (2.1%) → parent letters sent
  Vision defect (new glasses needed): 14 students → referral letters to ophthalmologist
  Dental issues requiring attention: 22 students → dental referral letters
  Anaemia (Hb < 12 g/dL — girls): 8 girls → prescribed iron supplements (state programme)

Individual reports: [Sent to parents via F-03 WhatsApp secure link — encrypted PDF]

CBSE Affiliation compliance: ✅ Annual health check conducted as required
[Export health check summary for CBSE inspection]
```

---

## 5. Mental Wellness Dashboard (Counsellor View)

```
Mental Wellness Dashboard — 27 March 2026

Active wellness flags:
  Referral source          Count   Categories
  J-01 Counsellor          14      Academic stress (7), social isolation (4), family (3)
  E-09 Attendance trigger   8      >15% absence — possible avoidance behaviour
  H-12 Hostel welfare       3      Homesickness, adjustment
  J-04 Discipline pattern   2      3+ incidents — behaviour concern
  J-03 Anti-ragging         1      Victim support

Students with multiple flags (high priority):
  Student A (IX-B) — E-09 flag + J-04 pattern + counsellor active case
  Student B (XI-A) — J-01 active + hostel welfare flag

Class-level wellness index (anonymised):
  Class   Students  Active flags  % flagged   Index
  VII-A   40         2              5%         🟢 Low concern
  VIII-B  42         5             12%         🟡 Monitor
  IX-B    38         7             18%         ⚠️ High concern — review with CT and VP
  X-A     41         3              7%         🟢 Low concern
  XI-A    38         4             11%         🟡 Monitor
  XII-A   36         2              6%         🟢 Low concern

IX-B pattern: High welfare flags — counsellor to meet class teacher for briefing
[Schedule CT-Counsellor meeting for IX-B]
```

---

## 6. Emergency Medical Card (Quick Access)

```
Emergency Medical Card — [Accessible to any teacher in 1 tap for emergency]

Student: Priya Venkat (XI-A)
Emergency contacts:
  Mother: +91 9876-XXXXX (primary)
  Father: +91 9765-XXXXX

⚠️ CRITICAL ALLERGY: PEANUTS — ANAPHYLAXIS
  Symptoms: Hives, throat swelling, breathing difficulty
  Action: Administer Epipen (nurse's room, top drawer, marked "Priya V.")
          Call 108 IMMEDIATELY
          Call parent (mother) simultaneously
          DO NOT delay — anaphylaxis can be fatal within minutes

Blood group: B+
Known medications: None currently

[This card is visible to all teachers on the emergency panel — no login required
 during school emergency; accessible by scanning student ID card QR code]
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/welfare/health/student/{student_id}/` | Student health profile |
| 2 | `PATCH` | `/api/v1/school/{id}/welfare/health/student/{student_id}/` | Update health info |
| 3 | `POST` | `/api/v1/school/{id}/welfare/health/sickroom/` | Log sick room visit |
| 4 | `GET` | `/api/v1/school/{id}/welfare/health/sickroom/?date={date}` | Sick room register for day |
| 5 | `GET` | `/api/v1/school/{id}/welfare/health/annual-checkup/` | Annual health check summary |
| 6 | `GET` | `/api/v1/school/{id}/welfare/health/wellness-dashboard/` | Counsellor wellness overview |
| 7 | `GET` | `/api/v1/school/{id}/welfare/health/emergency-card/{student_id}/` | Emergency medical card |
| 8 | `POST` | `/api/v1/school/{id}/welfare/health/student/{student_id}/vaccination/` | Log vaccination |

---

## 8. Business Rules

- Medical records are accessible only to medical staff (school nurse/doctor) and the Principal; class teachers see only the wellness flag ("this student has a medical note — see nurse for emergency protocol") not the diagnosis
- Critical allergy information is an exception to the restricted access rule: class teachers and canteen staff must know about life-threatening allergies; this is disclosed only to the extent necessary (allergy trigger, symptoms, first-response) without full medical history
- POCSO link: unexplained injuries observed during sick room visit must be flagged to the POCSO DO (J-02); the nurse or first aid person logs this flag; the DO follows up
- Annual health check-up is mandatory under CBSE Affiliation Bye-Laws; schools that cannot produce health check records during inspection risk affiliation issues; the record includes a doctor's certificate
- Medication at school: a school may administer only medications for which parent consent exists in writing with the drug name, dose, and condition; teachers should NEVER administer medication on their own judgement
- Health data under DPDPA: as a special category of sensitive personal data (health/medical), it may only be shared with parents (for their child), medical professionals, and the Principal; it cannot be included in any bulk data export or analytics report
- Parent can access their child's health record via the Parent Portal (N-14); they can update basic information (blood group, allergies) which the school nurse reviews and confirms before it becomes the active record

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division J*
