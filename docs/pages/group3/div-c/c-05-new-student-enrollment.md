# C-05 — New Student Enrollment

> **URL:** `/school/admissions/enrollment/`
> **File:** `c-05-new-student-enrollment.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Admission Officer (S3) — full · Class Teacher (S3) — own class view · Administrative Officer (S3) — full · Academic Coordinator (S4) — full · Principal (S6) — full

---

## 1. Purpose

Creates the formal student record in EduForge — the moment a student is officially enrolled in the school. This is a P0 operation because every other module (attendance, fees, marks, report cards, hall tickets, transport, library) depends on the student master record created here. The enrollment process captures the complete student profile, assigns the student a system-generated Student ID, assigns them to a class-section, generates an admission number, and triggers downstream setup (parent portal account creation, fee ledger initialisation, etc.).

In Indian schools, enrollment happens at two distinct times:
1. **New Admissions (April–June):** After seat confirmation (C-04) for the upcoming year
2. **Mid-year admissions (July–March):** Transfer students joining mid-session from other schools

This page handles both cases. For new admissions, the application form data from C-02 pre-fills most fields.

---

## 2. Page Layout

### 2.1 Header
```
New Student Enrollment — 2026–27              [+ Enroll New Student]  [Bulk Enroll from Admissions]  [Export]
Enrolled This Year: 186  ·  Pending Enrollment (Confirmed in C-04): 12
Academic Year: 2026–27
```

### 2.2 Recent Enrollments
| Admission No. | Student ID | Name | Class | Enrollment Date | Status |
|---|---|---|---|---|---|
| GVS/2026/0186 | STU-0001186 | Arjun Sharma | XI-A (Science) | 25 Mar 2026 | ✅ Active |
| GVS/2026/0185 | STU-0001185 | Priya Venkat | XI-A (Science) | 25 Mar 2026 | ✅ Active |
| GVS/2026/0184 | STU-0001184 | Meera Raju | VII-B | 24 Mar 2026 | ✅ Active |

---

## 3. Enrollment Form — From Confirmed Admission

[Bulk Enroll from Admissions] → shows all candidates with Status = Confirmed in C-04:

```
Confirmed Candidates Pending Enrollment:

Form No.     Applicant      Class        Select
ADM/2026/045  Arjun Sharma  XI-Science    ☑
ADM/2026/046  Priya Venkat  XI-Science    ☑
ADM/2026/051  Rohit Kumar   Class IX      ☑

[Enroll Selected →]
```

Each selected candidate's application data pre-fills the enrollment form.

---

## 4. Enrollment Form — Individual

[+ Enroll New Student] or clicking from bulk → 5-tab enrollment form:

### Tab 1: Basic Information
| Field | Value | Notes |
|---|---|---|
| Admission Number | GVS/2026/0187 | Auto-generated: School code / Year / Sequential |
| Student ID | STU-0001187 | System UUID; used across all modules |
| Enrollment Date | 26 Mar 2026 | Today (default) |
| Academic Year | 2026–27 | Current year |
| Admission Type | New Admission · Transfer (Mid-year) · Re-admission |
| Class | XI-A | Select section |
| Roll Number | 15 | Auto-assigned or manual |
| House | Tagore House | Auto-assigned by rotation or manual |
| **Student Full Name** | Arjun Sharma | As per birth certificate |
| Name on Certificate | Arjun Sharma | Same unless parent specifies different |
| Date of Birth | 12 Apr 2008 | |
| Gender | Male / Female / Other | |
| Nationality | Indian | |
| Religion | Hindu | |
| Mother Tongue | Telugu | |
| Category | General · SC · ST · OBC-NCL · OBC (Creamy) |  |
| Sub-category | EWS · Minority · Ex-Serviceman |  |
| Blood Group | B+ | |

### Tab 2: Family & Guardian Information
| Field | Value |
|---|---|
| Father's Full Name | Rajesh Sharma |
| Father's Occupation | Software Engineer |
| Father's Qualification | B.E. |
| Father's Aadhaar | XXXX XXXX 4521 |
| Father's Mobile | 9876543210 (Primary) |
| Father's Email | rajesh.sharma@email.com |
| Mother's Full Name | Meena Sharma |
| Mother's Occupation | Teacher |
| Mother's Qualification | M.A. |
| Mother's Mobile | 9876512345 |
| Guardian (if different) | Name, relation, mobile |
| Emergency Contact | Name, relation, mobile |
| Annual Family Income | ₹8,50,000 |
| Residential Address | House No, Street, Area, City, PIN |
| Permanent Address | Same as above / different |
| Transport Opted | Yes — Bus Route 4 / No (self / walk) |
| Hostel Opted | Yes / No |

### Tab 3: Academic History
| Field | Value |
|---|---|
| Previous School Name | St. Mary's English Medium School |
| Previous School City | Hyderabad |
| Previous School Board | CBSE / ICSE / State Board / IB / IGCSE |
| Last Class Attended | Class X |
| Last Year's Result | Pass / Distinction / Compartment / Fail |
| Percentage | 85.4% |
| TC Number | SM/TC/2026/0089 |
| TC Date | 20 Mar 2026 |
| TC Received and Filed | ✅ |
| Reason for Transfer | New residence proximity |

### Tab 4: Documents Received
| Document | Required | Received | Filed Location | Notes |
|---|---|---|---|---|
| Birth Certificate | ✅ | ✅ | R2: doc/birth_cert.pdf | Original sighted |
| Aadhaar (Student) | ✅ | ✅ | R2: doc/aadhaar_student.pdf | |
| Aadhaar (Father) | ✅ | ✅ | R2: doc/aadhaar_father.pdf | |
| Transfer Certificate | ✅ (Class II+) | ✅ | R2: doc/tc.pdf | Original held by school |
| Report Card (Previous) | ✅ | ✅ | R2: doc/report_card.pdf | |
| Passport Photos (4) | ✅ | ✅ | R2: photo/student_photo.jpg | 35×45mm colour |
| Caste Certificate | If SC/ST/OBC | N/A | — | General category |
| Medical Certificate | Optional | ⬜ | — | Reminder scheduled |

### Tab 5: Additional Information
| Field | Value |
|---|---|
| Special Educational Needs | None / Learning Disability / Physical Disability / Hearing / Vision |
| Medical Conditions (to know) | Asthma, Epilepsy, Allergy (free text) |
| Sibling at School | Yes → [Link existing student] |
| Scholarship | None / Merit / Need-based / RTE |
| Student Photo | [Upload — 35×45mm JPG, 500KB max] |
| Signature (student, for Class IX+) | [Upload] |
| Parent/Guardian Signature | [Upload] |

---

## 5. Post-Enrollment Auto-Actions

On successful enrollment save:

1. **Student ID generated:** `STU-0001187` — alphanumeric, unique, immutable
2. **Admission number assigned:** `GVS/2026/0187` — school code + year + sequential
3. **Roll number assigned** (or confirmed if manually entered)
4. **Fee ledger initialised** (in div-d Fee module — current year fee structure applied)
5. **Parent portal account created:** Login credentials sent via SMS/WhatsApp to father's mobile and mother's mobile
6. **Class Teacher notified:** "New student Arjun Sharma (Roll 15) enrolled in your class XI-A."
7. **In C-01:** Enquiry stage updated to "Admitted"
8. **In C-04:** Seat allocation status updated to "Enrolled"

---

## 6. Class Assignment & Roll Numbers

After enrollment, class teacher sees the updated class roll:

```
Class XI-A — 2026–27 — Students: 38

Roll  Admission No.   Name              Gender  Category  Status
01    GVS/2026/0001  Anjali Das         F       General   Active
02    GVS/2026/0002  Arjun Sharma       M       OBC-NCL   Active  ← newly enrolled
...
38    GVS/2026/0038  Zara Ahmed         F       General   Active
```

Roll numbers can be reassigned in bulk (alphabetical or custom order) by Class Teacher or Academic Coordinator.

---

## 7. Mid-Year Transfer Enrollment

For students joining mid-year:
- Same form as above
- Additional field: "Joining Date" (vs start of year)
- Attendance is tracked from joining date (not April 1)
- Fee is prorated from joining month (handled in div-d)
- TC from previous school must be received within 15 days of joining (system warning)

---

## 8. Enrollment Summary

```
Enrollment Summary — 2026–27
Class       Boys  Girls  Total  Target  Gap
Nursery       22    18     40     40     0
LKG           19    19     38     40     2
Class I       21    20     41     40    +1 (excess — Principal approved)
...
Class XI-A    18    20     38     40     2
XI-B          16    22     38     40     2
─────────────────────────────────────────
TOTAL        186   194    380    400    20
```

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/enrollment/?year={year}` | Enrollment list |
| 2 | `POST` | `/api/v1/school/{id}/students/enrollment/` | Enroll new student |
| 3 | `GET` | `/api/v1/school/{id}/students/enrollment/{student_id}/` | Enrollment detail |
| 4 | `PATCH` | `/api/v1/school/{id}/students/enrollment/{student_id}/` | Update enrollment record |
| 5 | `POST` | `/api/v1/school/{id}/students/enrollment/bulk/` | Bulk enroll from confirmed admissions |
| 6 | `GET` | `/api/v1/school/{id}/students/enrollment/{student_id}/documents/` | Document list |
| 7 | `POST` | `/api/v1/school/{id}/students/enrollment/{student_id}/documents/` | Upload document |
| 8 | `GET` | `/api/v1/school/{id}/students/enrollment/summary/?year={year}` | Class-wise enrollment summary |
| 9 | `POST` | `/api/v1/school/{id}/students/enrollment/{student_id}/reassign-roll/` | Reassign roll number |

---

## 10. Business Rules

- Student ID (`STU-XXXXXXX`) is immutable once assigned — never changes even on promotion, transfer, or re-admission; this is the anchor key across all modules
- Admission number format is school-configurable: default `{SCHOOL_CODE}/{YEAR}/{SEQ}` — EduForge generates the sequential number; schools can set their own prefix
- A student cannot be enrolled without a photo (required for hall ticket, ID card, CBSE registration)
- Enrollment in a class that has already reached capacity (A-08 class size limit) requires Principal override with justification
- Mid-year enrollments after October 31 for Classes IX and XI are flagged with a warning: "Student may not meet 75% attendance requirement for the current year — inform parent and Exam Cell"
- Parent portal credentials are single-use setup links (expire in 48h); if parent doesn't set up, a new link can be generated from A-35 User Management

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
