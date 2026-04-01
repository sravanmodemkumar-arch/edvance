# H-07 — Medical Room

> **URL:** `/school/hostel/medical/`
> **File:** `h-07-medical-room.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Matron (S3) — primary medical room management · Chief Warden (S4) — oversight · Principal (S6) — hospital referral approval · Warden (S3) — initial report of sick student

---

## 1. Purpose

Manages the in-hostel medical room (sick room/infirmary) — the first line of healthcare for boarding students. Indian residential school requirements:
- **Compulsory sick room:** CBSE Affiliation Bye-Laws require a sick room with basic medical facilities in residential schools
- **Matron/Nurse:** A resident matron or trained nurse is required; many schools have a visiting doctor (2-3 times/week)
- **Medical register:** Mandatory log of all student illnesses, medications dispensed, and hospital referrals; produced during CBSE inspection
- **Pharmacy stock:** Basic medicines (paracetamol, antacids, ORS, antiseptic) maintained; prescription medicines require doctor's order
- **Hospital referral:** If student needs more than basic care → referral to empanelled hospital; parent notified before referral (unless emergency)
- **POCSO sensitivity:** If a student presents with injuries inconsistent with the reported cause (fall, accident), the Matron must report to POCSO Designated Person — potential abuse indicator

---

## 2. Page Layout

### 2.1 Header
```
Medical Room                                         [+ Admit to Sick Room]  [Log Medication]
Date: 27 March 2026

Currently in sick room: 2 students
Outpatients treated today: 5
Awaiting hospital referral: 0
Visiting doctor: Dr. Suresh Reddy — Tomorrow (Wednesday 9 AM)
```

### 2.2 Sick Room Register
```
Patient         Class  Admitted    Complaint          Status           Discharge
Arjun Sharma   XI-A   27 Mar 8 AM Fever (102°F)      🟡 Monitoring    —
Meena D.      XII-A   26 Mar 7 PM Stomach pain        ✅ Recovered    Discharge today
```

---

## 3. Admit to Sick Room

```
[+ Admit to Sick Room]

Student: [Arjun Sharma — XI-A — Room 101]
Date & Time: 27 March 2026, 8:00 AM
Reported by: Mr. Suresh Kumar (Warden — Room 101 area)

Presenting complaint: [Fever — measured 102°F]

Vital signs:
  Temperature: [102°F]
  Pulse: [88 bpm]
  BP: [Not taken (standard for age)]
  SpO2: [98%]

Assessment: ● Fever — monitoring  ○ Injury  ○ Gastroenteritis  ○ Allergic reaction  ○ Other

Medication dispensed:
  [Paracetamol 500mg — 1 tablet at 8:15 AM]  [+ Add medication]

School attendance impact:
  → School session today: [Absent — in sick room] (auto-links to E-01 for today)
  → Class Teacher Ms. Anita notified: ✅ WhatsApp sent

Parent notification: ✅ WhatsApp sent at 8:30 AM:
  "Arjun Sharma is in the school medical room with a fever (102°F).
   Matron is monitoring. Will update you. If needed, we will arrange
   a hospital visit. — Greenfields Hostel"

POCSO flag check: No unexplained injuries. No flag required.

[Save Admission]
```

---

## 4. Medication Log

```
Medication Log — 2026–27

All medications dispensed from sick room must be logged:

Date       Student       Medication             Dose      Time    Authorized By
27 Mar     Arjun S.      Paracetamol 500mg      1 tablet  8:15 AM Matron
27 Mar     Meena D.      ORS sachet             1 sachet  8:00 AM Matron
26 Mar     Chandana R.   Salbutamol inhaler      2 puffs   10 PM   Self (prescribed)
                         (student's own — logged as administered)
15 Mar     Vijay S.      Antacid syrup           10 ml     9 PM    Matron

Prescription medications (student's own):
  Chandana Rao — Salbutamol inhaler (kept with Matron; administered when needed)
  Ravi K. — Vitamin D capsule (daily; self-administered with Matron supervision)

Stock check — this week:
  Paracetamol 500mg: 80 tablets (reorder threshold: 50)
  ORS sachets: 12 (reorder threshold: 10) ⚠️ Reorder soon
  Antiseptic (Dettol): 1 bottle (adequate)
  [Generate Pharmacy Stock Report]  [Raise Reorder (D-20 Petty Cash)]
```

---

## 5. Hospital Referral

```
Hospital Referral — Arjun Sharma

Condition: Fever not subsiding after 24 hours (Day 2, still 101°F)

Decision: ● Refer to hospital  ○ Continue monitoring
Hospital: [Apollo Hospital, Vijayawada] (empanelled hospital)
Referral type: ● OPD visit (today afternoon)  ○ Emergency  ○ Admission

Parent notification:
  WhatsApp + Call to Father: "Arjun's fever has persisted for 24 hours. We are taking him
  to Apollo Hospital for a doctor's examination. Please meet us there at 3 PM if possible.
  Accompanied by: Matron (Ms. Kavitha). Emergency contact: +91 9999-XXXXX."

Parent consent: ● Yes (verbal — logged)  ○ Written required for admission

Accompanied by: [Matron Ms. Kavitha + Female staff]
  Note: Student is NEVER sent to hospital alone.

Transport: School vehicle — Van (AV1)
Departure: 2:30 PM

[Generate Referral Letter]  [Log Referral in Register]
```

---

## 6. Visiting Doctor Register

```
Visiting Doctor Sessions — 2026–27

Doctor: Dr. Suresh Reddy MBBS (Gen Practice)
Schedule: Wednesdays and Saturdays, 9 AM – 11 AM

Session log:
Date        Patients seen  Cases referred  Medicines prescribed
22 Mar 2026   8             1 (Apollo OPD)   Antibiotics (2 students)
15 Mar 2026   5             0                Vitamins/supplements
8 Mar 2026    12            2               —

Doctor's prescription register: Maintained separately (legal requirement)
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/medical/sick-room/?date={date}` | Sick room current patients |
| 2 | `POST` | `/api/v1/school/{id}/hostel/medical/admit/` | Admit student to sick room |
| 3 | `POST` | `/api/v1/school/{id}/hostel/medical/discharge/{patient_id}/` | Discharge patient |
| 4 | `POST` | `/api/v1/school/{id}/hostel/medical/medication/` | Log medication dispensed |
| 5 | `POST` | `/api/v1/school/{id}/hostel/medical/referral/` | Hospital referral |
| 6 | `GET` | `/api/v1/school/{id}/hostel/medical/register/?month={m}&year={y}` | Medical register for month |
| 7 | `GET` | `/api/v1/school/{id}/hostel/medical/stock/` | Pharmacy stock check |

---

## 8. Business Rules

- Any student in the sick room for school hours has their school attendance (E-01) updated to "Medical — Sick Room" by the Matron; the Class Teacher is notified
- Unexplained injuries (bruises, burns inconsistent with the student's account) must be flagged to the POCSO Designated Person within 1 hour — the Matron is a mandatory reporter under POCSO 2012
- Medications are dispensed only from the approved stock list (basic first aid); any other medication requires a doctor's prescription from the visiting doctor or a hospital
- If a student requires hospitalization: parent must be reached before admission (except life-threatening emergency where treatment proceeds and parent is notified simultaneously); if parent is unreachable, the Principal authorises treatment
- Medical records from H-07 are added to the student's C-18 health record for chronic conditions; episodic illness (fever, cold) is not added to C-18 unless it becomes recurring

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
