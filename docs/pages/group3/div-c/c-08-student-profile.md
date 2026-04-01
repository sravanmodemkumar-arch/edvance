# C-08 — Student Profile

> **URL:** `/school/students/{student_id}/`
> **File:** `c-08-student-profile.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** All roles — see section-level access below

---

## 1. Purpose

The student profile is the master record for every student — the single source of truth that all other EduForge modules reference. When an attendance module needs the student's class, it reads the profile. When a fee module computes dues, it reads the profile for scholarship and sibling discount. When the report card generator creates the report, it reads the profile for the student's name, class, roll number, and parent names. When CBSE board exam registration (B-33) submits the LOC, it reads the Aadhaar number, photo, and name from the profile.

This page is the comprehensive view of a student — combining enrollment information (C-05), academic performance summary (linked to B-18), attendance summary (linked to attendance module), fee status (linked to div-d), and documents (C-06) into one place.

**Access levels by role:**
- **Data Entry Operator (S2):** Can view and update basic demographics (no sensitive/financial data)
- **Class Teacher (S3):** Full view of their class students; can edit contact info, notes; cannot edit category/financial
- **Admission Officer / Admin Officer (S3):** Full view; can edit all fields except financial (handled in div-d)
- **Academic Coordinator (S4):** Full view; can edit class allocation, academic remarks
- **Principal (S6):** Full view and edit of all fields

---

## 2. Page Layout

### 2.1 Student Identity Card (Top Strip)
```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│  [Photo]   Arjun Sharma                                              Student ID: STU-0001187 │
│  35×45mm   Class: XI-A · Roll: 15 · House: Tagore                   Admission: GVS/2026/0187 │
│            DOB: 12 Apr 2008 (17 yrs)  ·  Blood Group: B+            Status: ✅ Active       │
│            Father: Rajesh Sharma · 9876543210                         Academic Year: 2026–27 │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Tab Navigation
```
[Personal]  [Family]  [Academic History]  [Documents]  [Performance]  [Attendance]  [Fees]  [Activity Log]
```

---

## 3. Tab: Personal Information

| Field | Value | Editable By |
|---|---|---|
| Full Name | Arjun Sharma | Admin Officer / Principal |
| Name on Certificate | Arjun Sharma | Admin Officer / Principal (if different) |
| Date of Birth | 12 April 2008 | Admin Officer / Principal |
| Gender | Male | Admin Officer / Principal |
| Nationality | Indian | Admin Officer |
| Religion | Hindu | Admin Officer |
| Mother Tongue | Telugu | Admin Officer |
| Category | OBC-NCL | Principal only (category is a sensitive field) |
| Sub-category | — | |
| Blood Group | B+ | Class Teacher, Admin Officer |
| Aadhaar Number | XXXX XXXX 4521 | Admin Officer (stored encrypted) |
| APAAR ID | AP2026XXXXXXXXXX | Admin Officer (once assigned) |
| Disability Status | None | Admin Officer; if CWSN → links to C-19 |
| Medical Conditions | Mild asthma | Class Teacher, Admin Officer |
| Emergency Medical Note | Carry inhaler | Class Teacher |
| RTE Student | No / Yes (Category, Year of RTE admission) | Read-only (set in C-07) |

---

## 4. Tab: Family Information

| Field | Value |
|---|---|
| Father's Name | Rajesh Sharma |
| Father's Occupation | Software Engineer |
| Father's Education | B.E. |
| Father's Aadhaar | XXXX XXXX 4521 |
| Father's Mobile | 9876543210 (Primary contact) |
| Father's Email | rajesh@email.com |
| Mother's Name | Meena Sharma |
| Mother's Occupation | Teacher |
| Mother's Education | M.A. |
| Mother's Mobile | 9876512345 |
| Mother's Email | meena@email.com |
| Guardian (if applicable) | Name, relation, contact |
| Annual Family Income | ₹8,50,000 |
| Residential Address | 14, Gandhi Nagar, Hyderabad — 500032 |
| Permanent Address | Same as residential |
| Communication Preference | WhatsApp + Email |
| Parent Portal Login (Father) | Active (last login: 20 Mar 2026) [Reset Password] |
| Parent Portal Login (Mother) | Active (last login: 18 Mar 2026) |
| Siblings at School | Rahul Sharma — Class IX-B — STU-0001050 [View] |

---

## 5. Tab: Academic History

### 5.1 Current Year
```
Class: XI-A  ·  Academic Year: 2026–27  ·  Stream: Science (PCM)
Class Teacher: Ms. Anita Reddy
Subjects: Physics · Chemistry · Mathematics · English Core · Physical Education
```

### 5.2 Year-wise Academic Record
| Year | Class | School | Board | Result | % | Promoted By |
|---|---|---|---|---|---|---|
| 2025–26 | X-A | [This School] | CBSE | ✅ Pass (Board) | 85.4% | Board |
| 2024–25 | IX-A | [This School] | CBSE | ✅ Pass | 79.2% | School |
| 2023–24 | VIII-A | [This School] | CBSE | ✅ Pass | 76.8% | School |
| 2022–23 | VII-B | [This School] | CBSE | ✅ Pass | 74.1% | School |
| 2021–22 | VI-A | St. Mary's | CBSE | ✅ Pass | 71.0% | School (TC) |

### 5.3 Class X Board Results (if applicable)
```
CBSE Class X — March 2026
Roll No.: 12342568  ·  Overall CGPA: 8.6

Subject              Theory  IA    Total  Grade
English Core           78     20     98    A1
Mathematics Standard   84     18    102    A2 (scaled)
Science                79     19     98    A1
Social Science         82     20    102    A1
Hindi                  71     18     89    B1
PE                     —      —      —    A+ (additional)
CGPA: 8.6  ·  Best 5 (excluding PE): 8.6
```

---

## 6. Tab: Documents

Summary view linking to C-06:
```
Documents for Arjun Sharma — STU-0001187

Document Type         Status     Date Filed     View
Birth Certificate     ✅ Verified  25 Mar 2026  [PDF]
Student Aadhaar       ✅ Verified  25 Mar 2026  [PDF]
Father Aadhaar        ✅ Verified  25 Mar 2026  [PDF]
TC from Previous      ✅ Verified  20 Mar 2026  [PDF]
Report Card (Class X) ✅ Filed     20 Mar 2026  [PDF]
Photos (4)            ✅ Filed     25 Mar 2026  [IMG]
Caste Certificate     ✅ Verified  25 Mar 2026  [PDF]  OBC-NCL — Tahsildar Balanagar
35×45 Photo (Board)   ✅ Filed     25 Mar 2026  [IMG]
Student Signature     ✅ Filed     25 Mar 2026  [IMG]
```

---

## 7. Tab: Performance Summary

Visual summary (links to detailed marks in B-18):
```
Academic Performance — Arjun Sharma

Current Year (2026–27):
  Class: XI-A  |  Term 1 Result: 78.4%  |  PT-1: 82% · PT-2: 79%

Last 3 Years Trend:
  2025–26: 85.4% (Class X Board)
  2024–25: 79.2% (Class IX Annual)
  2023–24: 76.8% (Class VIII Annual)
  Trend: ↑ Improving

Subject-wise (Current Year PT-2):
  Physics: 78/100  Chemistry: 82/100  Mathematics: 88/100  English: 76/100

Coaching Test Performance (if coaching_integration: true):
  JEE Weekly W-11: 234/270 (87.4%ile)  [View Full Trajectory]
```

---

## 8. Tab: Attendance Summary

```
Attendance — 2026–27  (Academic Year: Apr 2025 – Mar 2026)

Working Days So Far: 198  |  Present: 172  |  Absent: 26  |  Leave: 4
Attendance %: 86.9%  ·  Status: ✅ Eligible (≥ 75%)

Monthly Breakdown:
Apr: 22/22  May: 20/20  Jun: 18/20  Jul: 21/22  Aug: 19/22  Sep: 20/20
Oct: 20/22  Nov: 12/14  Dec: 18/22  Jan: 22/22  Feb: 20/22  Mar: 0 (ongoing)

Recent Absences:
  15 Mar 2026 — Absent (Unexcused)
  14 Mar 2026 — Leave (Medical — Parent note submitted)
  8 Feb 2026 — Absent (Unexcused)
```

---

## 9. Tab: Fee Status

Summary view linking to div-d:
```
Fee Status — 2026–27

Annual Fee: ₹72,000  |  Paid: ₹54,000  |  Outstanding: ₹18,000
Next Due: Q4 Instalment — ₹18,000 — Due: 1 Apr 2026

Payment History:
  Apr 2025: ₹18,000  ✅  Receipt: R/2025/1872
  Jul 2025: ₹18,000  ✅  Receipt: R/2025/4218
  Oct 2025: ₹18,000  ✅  Receipt: R/2025/7834
  Jan 2026: ₹18,000  ⏳  Pending
```

---

## 10. Tab: Activity Log

Audit trail of changes to this student's record:
```
26 Mar 2026 10:30  Meera (Admin Officer)  — Photo uploaded (35×45mm board exam photo)
25 Mar 2026 15:00  Meera (Admin Officer)  — Enrolled in Class XI-A; student ID assigned
20 Mar 2026 12:00  Meera (Admin Officer)  — TC from St. Mary's received and verified
15 Mar 2026 09:00  Kavitha (Principal)    — Seat confirmed; offer letter sent
```

---

## 11. Actions (Role-gated)

| Action | Allowed Roles | Notes |
|---|---|---|
| [Edit Profile] | Admin Officer, Academic Coord, Principal | Opens edit form |
| [Change Class/Section] | Academic Coordinator, Principal | Internal transfer (links to C-11) |
| [Generate TC] | Admin Officer, Principal | Links to C-13 |
| [Generate Bonafide] | Class Teacher, Admin Officer | Links to C-14 |
| [Generate ID Card] | Admin Officer | Links to C-15 |
| [Mark Inactive] | Principal | Withdrawal, expulsion, or long absence; triggers C-12 |
| [Reset Parent Password] | Admin Officer | Resets parent portal login |
| [Export Student Data] | All roles | PDF/Excel of full profile (DPDPA data export) |

---

## 12. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/students/{student_id}/` | Full student profile |
| 2 | `PATCH` | `/api/v1/school/{id}/students/{student_id}/` | Update student profile |
| 3 | `GET` | `/api/v1/school/{id}/students/?class_id={id}&year={year}` | Class student list |
| 4 | `GET` | `/api/v1/school/{id}/students/{student_id}/performance/` | Performance summary (multi-year) |
| 5 | `GET` | `/api/v1/school/{id}/students/{student_id}/attendance/summary/?year={year}` | Attendance summary |
| 6 | `GET` | `/api/v1/school/{id}/students/{student_id}/fees/summary/?year={year}` | Fee status summary |
| 7 | `GET` | `/api/v1/school/{id}/students/{student_id}/activity-log/` | Audit trail |
| 8 | `POST` | `/api/v1/school/{id}/students/{student_id}/mark-inactive/` | Mark student inactive |
| 9 | `GET` | `/api/v1/school/{id}/students/{student_id}/export/` | Full data export (DPDPA) |

---

## 13. Business Rules

- Student ID is immutable — never changes through promotions, transfers, or re-admissions
- Aadhaar number stored encrypted; displayed masked; only decrypted for PDF generation processes (e.g., board exam LOC)
- Category field (SC/ST/OBC) edit requires Principal-level access; changes are logged with a mandatory reason note (to prevent category fraud)
- Student photo must be maximum 30 days old for board exam purposes; system warns if photo upload date > 1 year ago when B-33 LOC preparation begins
- A student marked "Inactive" (withdrawn) is moved from active rolls; their historical data (marks, attendance, fees) remains accessible but they are excluded from current-year counts
- The Performance tab shows data only for years this student was enrolled in this school; data from previous schools is shown only if manually entered in Academic History

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
