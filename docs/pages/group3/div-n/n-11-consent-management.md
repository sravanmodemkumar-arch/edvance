# N-11 — Consent & Permissions (Parent View)

> **URL:** `/parent/consent/`
> **File:** `n-11-consent-management.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P)

---

## 1. Purpose

Under DPDPA 2023, the school must obtain informed, specific consent from parents (as guardians of minor children) for processing the child's data and for certain activities. This module is the parent's central consent dashboard — they see what they have consented to, can grant or revoke consent, and give activity-specific permissions (e.g., school trips, photographs).

Two types of consent managed here:
1. **Data consent** (DPDPA 2023) — consent for how EduForge processes and shares the child's data
2. **Activity consent** — permission for specific school activities (field trips, photos for annual magazine, participation in inter-school events)

---

## 2. Data Consent Status

```
DATA CONSENT DASHBOARD — Mrs. Sunita Rao
For child: Rahul Rao (Class X-A)

DPDPA 2023 — CONSENT STATUS:

  Processing Purpose                         Status     Date Granted    Can Revoke?
  ─────────────────────────────────────────────────────────────────────────────────
  Student profile management (mandatory*)    ✅ Active   10 Apr 2025     No *
  Attendance recording (mandatory*)          ✅ Active   10 Apr 2025     No *
  Academic assessment and reports            ✅ Active   10 Apr 2025     Yes (no exams)
  Fee management and payment processing      ✅ Active   10 Apr 2025     Yes
  Transport tracking (parent-visible GPS)    ✅ Active   10 Apr 2025     Yes
  Parent communication (diary, WhatsApp)     ✅ Active   10 Apr 2025     Yes
  School annual magazine / photographs       ✅ Active   10 Apr 2025     Yes
  School website profile / achievements      ✅ Active   10 Apr 2025     Yes
  Alumni database (post-graduation)          ⬜ Not given —              —
  Research/analytics (anonymised)            ✅ Active   10 Apr 2025     Yes
  ─────────────────────────────────────────────────────────────────────────────────

* Mandatory consent: Cannot be revoked without withdrawal of admission (RTE / CBSE
  requirement for enrolled students). The school must maintain attendance records.

[Manage consent] → select item → toggle

NOTICE: Revoking "transport tracking" consent means the parent will no longer
  receive bus GPS updates or delay alerts. The school's internal GPS tracking
  for safety continues (CBSE Transport Safety Code requirement).
```

---

## 3. Activity Permissions

```
ACTIVITY PERMISSIONS — Rahul Rao (2025–26)

PENDING PERMISSIONS (require your response):
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  🎭 ANNUAL DAY SKIT — Class X Performance                                │
  │  Permission required by: 5 April 2026                                   │
  │  Details: Rahul has been selected for Class X skit "Future India"        │
  │  at the Annual Day (10 April 2026, 5:30 PM programme).                  │
  │  Requirements: School costume (provided), rehearsals on 5 Apr (2–4 PM)  │
  │  and 8 Apr (2–4 PM).                                                    │
  │  Photography/video will be taken; images may appear in school magazine. │
  │                                                                           │
  │  ✅ I permit Rahul to participate in the Annual Day skit                 │
  │  ☐ I do NOT permit participation                                         │
  │  [Submit] ← Required by 5 April                                          │
  └──────────────────────────────────────────────────────────────────────────┘

GIVEN PERMISSIONS (this year):
  Activity                           Date Given    Permission  Notes
  School trip — Golconda Fort        15 Sep 2025   ✅ Allowed  Medical emergency contacts given
  Inter-school quiz competition      10 Dec 2025   ✅ Allowed  Half-day out of school
  Annual magazine photograph         1 Nov 2025    ✅ Allowed  Photo for "Class X 2025–26" page
  Science exhibition display         5 Feb 2026    ✅ Allowed  Project on display in school lobby

WITHDRAWN PERMISSIONS:
  None this year ✅
```

---

## 4. School Trip Consent

```
SCHOOL TRIP CONSENT — EXAMPLE

UPCOMING: Science Trip to Birla Planetarium, Hyderabad
Date: 18 April 2026 (half-day)
Departure: 9:00 AM from school; Return: 1:00 PM
Cost: ₹450 (included in activity fee) — no additional payment needed
Supervision: 3 teachers + 1 parent volunteer (4:1 ratio) ✅
Transport: School bus (Route 3 — same driver, BGV verified ✅)

Emergency medical contact for trip:
  Rahul's medical conditions: Nil
  Allergies: None documented
  Emergency contact: +91 98XXXXXX (Mrs. Sunita Rao — mother)
  Blood group: O+ [Update if incorrect →]

PERMISSION:
  ● I permit Rahul to attend the Planetarium trip on 18 April 2026.
    I understand the school will take reasonable precautions for his safety.
  ○ I do NOT permit Rahul to attend this trip.

Medical note (if any specific instruction for trip day):
  [Text field — max 200 characters]

[Submit permission]
```

---

## 5. DPDPA Rights Centre

```
YOUR DATA RIGHTS (DPDPA 2023 — as Data Principal for your minor child)

Rights you have under DPDPA 2023:

1. Right to Access:
   What data we hold about Rahul: [View data inventory →]
   Includes: Profile, attendance, marks, health information on file, photos

2. Right to Correction:
   If any data is incorrect: [Request correction →]
   Example: Wrong date of birth, incorrect blood group, misspelled name

3. Right to Erasure (limited):
   Certain data can be erased after the student leaves the school.
   Data required by law (attendance, CBSE records, service book equivalent):
     Cannot be erased until statutory retention period expires.
   Data that can be erased on request: Additional photos, optional profiles
   [Request erasure →] ← submit request; school reviews within 30 days

4. Right to Grievance:
   If you believe your rights were violated:
   [Raise data privacy complaint →] → links to N-10 (privacy category)

Contact: Privacy Officer, Greenfields School — privacy@greenfieldsschool.edu
DPDPA Grievance Officer: VP (Ms. Meena Rao) — responds within 30 days
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/consent/` | All consent status |
| 2 | `PATCH` | `/api/v1/parent/{parent_id}/child/{student_id}/consent/{consent_id}/` | Update consent (grant/revoke) |
| 3 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/permissions/` | Activity permissions |
| 4 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/permissions/{perm_id}/respond/` | Grant/deny activity permission |
| 5 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/consent/data-inventory/` | DPDPA data inventory |
| 6 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/consent/erasure-request/` | Submit erasure request |

---

## 7. Business Rules

- Consent for mandatory data processing (attendance, academic records) cannot be revoked by the parent while the child is enrolled; withdrawal would constitute withdrawal from the school, which is the parent's right but the school's right to require minimal data for legitimate educational purposes (DPDPA Sec 4 — legitimate uses)
- Activity permissions are per-event; the school cannot use a blanket annual consent form for all trips and activities; each significant activity (field trips, inter-school events, media appearances) requires specific consent; this is in line with DPDPA's "specific and informed consent" requirement
- Consent changes are logged with timestamp and IP address (audit trail for DPDPA compliance); a revoked consent is not deleted — the revocation is recorded; the school can see the history of what was consented and when it was revoked
- For minors (students below 18), the parent/guardian is the data principal — they exercise DPDPA rights on behalf of the child; when the student turns 18 (rare in school context, but possible for Class XII repeaters), the student themselves becomes the data principal
- Medical emergency contact information provided in school trip consent is treated as special-category health data under DPDPA; it is accessible to the trip supervision team only during the trip and deleted from the trip manifest after return; it is retained in the student's general health record (J-06) long-term

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
