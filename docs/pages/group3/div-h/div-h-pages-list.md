# Division H — Hostel Management — Pages List

> **Group:** 3 — School Portal
> **Division:** H — Hostel Management
> **Total Pages:** 14
> **Directory:** `docs/pages/group3/div-h/`

---

## Purpose

Manages residential hostel operations for boarding schools. Indian boarding school context:
- **Residential schools** (Sainik Schools, Navodaya Vidyalayas, private boarding schools) house hundreds to thousands of students
- **CBSE and state regulations** require hostels to maintain registers, duty rosters, health records, and visitor logs
- **JNV (Jawahar Navodaya Vidyalaya):** Government scheme residential schools; specific accommodation and dietary standards mandated by NVS guidelines
- **Girls' hostel regulations:** MHA guidelines and state rules mandate specific security measures for girls' hostels (CCTV, visitor restrictions, female wardens)
- **24/7 warden duty:** Duty register, night rounds log, emergency contact protocols
- **Hostel committee:** Many hostels have a resident student welfare committee; complaints go here first
- **Mess / Canteen:** Managed as part of hostel operations; dietary requirements, allergies, religious food preferences
- **Leave and absence:** Hostel students have a different leave protocol than day scholars — weekend leave, home leave, exeat
- **Medical room:** In-hostel medical facility with basic first aid and sick room

---

## Roles (new to this division)

| Role | Code | Level | Description |
|---|---|---|---|
| Chief Warden | S4 | S4 | Manages all hostel wardens; hostel policy; reports to Principal |
| Warden (Male) | S3 | S3 | Manages a specific boys' hostel block; duty register; room inspections |
| Warden (Female) | S3 | S3 | Manages girls' hostel; specific security protocols |
| House Parent / Residential Tutor | S3 | S3 | Lives in hostel; responsible for a group of students |
| Hostel Accountant | S3 | S3 | Hostel fee, mess charges, and expenses |
| Matron | S3 | S3 | Girls' hostel welfare; hygiene; medical room |

---

## Pages

| Page ID | Title | URL Slug | Priority | Key Function |
|---|---|---|---|---|
| H-01 | Student Room Allocation | `hostel/rooms/` | P1 | Room assignment, bed allocation, batch moves |
| H-02 | Hostel Admission | `hostel/admission/` | P1 | Hostel admission application, waitlist, allocation |
| H-03 | Hostel Attendance | `hostel/attendance/` | P0 | Daily hostel headcount; night roll call |
| H-04 | Hostel Leave & Exeat | `hostel/leave/` | P0 | Weekend leave, home leave, gate pass |
| H-05 | Visitor Register | `hostel/visitors/` | P1 | Parent visits; visitor log; VIP visitor protocol |
| H-06 | Mess / Canteen Management | `hostel/mess/` | P1 | Menu planning, mess fee, dietary requirements |
| H-07 | Medical Room | `hostel/medical/` | P1 | Sick room register, medication log, hospital referrals |
| H-08 | Warden Duty Register | `hostel/duty/` | P1 | Warden duty roster, night rounds log |
| H-09 | Hostel Fees & Billing | `hostel/fees/` | P1 | Hostel fee, mess charges, laundry, medical extras |
| H-10 | Discipline & Conduct Register | `hostel/conduct/` | P2 | Rules, violations, penalties, counsellor referral |
| H-11 | Hostel Inventory | `hostel/inventory/` | P2 | Bedding, furniture, amenities stock |
| H-12 | Student Welfare (Hostel) | `hostel/welfare/` | P1 | Student welfare concerns, homesickness, mental health |
| H-13 | Maintenance & Complaints | `hostel/maintenance/` | P2 | Infrastructure complaints, repair requests |
| H-14 | Hostel Reports & Analytics | `hostel/reports/` | P2 | Occupancy, incident reports, health trend |

---

## Key Integrations

- **C-05 Student Enrollment:** Hostel admission linked to student record; hostel status flag
- **E-01 Daily Attendance:** Hostel students marked absent in school if not present in school section; cross-check with H-03 hostel attendance
- **D-04 / D-07 Fee Collection:** Hostel fee billed via D-04 and tracked in D-07 fee ledger
- **C-13 TC Generator:** Hostel clearance required for TC (all dues paid, room vacated, equipment returned)
- **C-18 Student Health Records:** Medical room (H-07) updates C-18 for chronic conditions
- **J-01 Student Welfare:** Hostel welfare concerns escalate to school counsellor (J-01)
- **F-10 Emergency Alert System:** Emergency at hostel triggers F-10 mass notification

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
