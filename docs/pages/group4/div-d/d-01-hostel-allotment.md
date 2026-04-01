# D-01 — Hostel Allotment & Room Allocation

> **URL:** `/college/hostel/allotment/`
> **File:** `d-01-hostel-allotment.md`
> **Priority:** P1
> **Roles:** Chief Warden (S4) · Warden (S3) · Hostel Admin (S3) · Principal/Director (S6)

---

## 1. Hostel Inventory

```
HOSTEL INVENTORY — GCEH 2026–27

BOYS' HOSTEL (Block A, B):
  Block A: 40 rooms × 3 beds = 120 beds (double/triple occupancy)
  Block B: 30 rooms × 2 beds = 60 beds (double occupancy)
  Total boys: 180 beds

GIRLS' HOSTEL (Block C):
  Block C: 50 rooms × 2 beds = 100 beds (double occupancy)
  Total girls: 100 beds

TOTAL CAPACITY: 280 beds

CURRENT OCCUPANCY (2026–27):
  Boys: 168 / 180 (93.3%)
  Girls: 94 / 100 (94.0%)
  Total: 262 / 280 (93.6%)

ROOM TYPES:
  Standard (3-bed): ₹42,000/yr (Boys Block A)
  Standard (2-bed): ₹48,000/yr (Boys Block B + Girls Block C)
  Reserved rooms (Ground floor, accessible): 4 rooms — PwD students (NBC 2016)

WARDEN QUARTERS:
  Boys' warden: Flat G-01 (ground floor Block A) — mandatory on-campus residence (AICTE)
  Girls' warden: Flat G-02 (ground floor Block C) — lady warden mandatory (UGC)
  Chief Warden: Flat G-03 (administrative block adjacent)
```

---

## 2. Allotment Process

```
HOSTEL ALLOTMENT — 2026–27
Application window: 15 June – 15 July 2026

ELIGIBILITY:
  Open to: All enrolled students (B.Tech, M.Tech, MBA, MCA)
  Priority order:
    1. Students from districts >100 km from Hyderabad (residence proof)
    2. Students from Telangana rural areas (Mandal HQ or below)
    3. Students with annual family income <₹3L (income proof)
    4. Girls (standalone girls' hostel — all applications given priority)
    5. SC/ST students (UGC hostel priority guidelines)
    6. PwD students (ground floor rooms reserved — mandatory)
    7. General (distance >50 km)

  Year-wise preference (within each category):
    First-year students given preference (adjustment to new environment)
    Continuing students: reallotment based on seniority

APPLICATIONS RECEIVED:
  Boys: 210 applications → 180 seats (30 overflow → waiting list)
  Girls: 98 applications → 100 seats (all accommodated)

ALLOTMENT ALGORITHM:
  Step 1: PwD students → 4 accessible rooms (auto-assign ground floor)
  Step 2: Sort remaining applications by priority category, then by merit rank
  Step 3: Assign rooms (same branch/year together where possible — preference)
  Step 4: Auto-generate allotment letter

ALLOTMENT LETTER — Student: Kiran S. (226J1A0312):
  Hostel: Boys' Block B
  Room: B-204
  Bed: B-204-02
  Room mates: Suresh V. (226J1A0318), Ramesh T. (226J1A0401)
  Reporting date: 20 July 2026 (before college orientation)
  Fee: ₹48,000/yr (payable as ₹24,000/semester)
  Conditions: Anti-ragging undertaking mandatory at check-in ✅

[Download Allotment Letter]  [View Room Details]
```

---

## 3. Check-In Process

```
CHECK-IN CHECKLIST — Kiran S. (226J1A0312)
Check-in date: 20 July 2026

DOCUMENTS COLLECTED AT CHECK-IN:
  ✅ Anti-ragging undertaking (UGC mandatory — student + parent signatures)
  ✅ Medical fitness certificate (doctor-certified, within 3 months)
  ✅ Parent/Guardian contact (primary + emergency contact updated)
  ✅ ID proof (Aadhaar masked copy on file)
  ✅ Hostel rules acknowledgement (signed)
  ✅ Valuables declaration (laptop serial, phone IMEI — for insurance/theft purposes)

ROOM CONDITION REPORT (at check-in):
  Furniture: ✅ (3 beds, 3 study tables, 3 chairs, 1 wardrobe each)
  Electrical: ✅ (tube light, fan, 2 power points, 1 network point)
  Defects noted: Right window hinge loose (Room B-204) → maintenance ticket #M-2240 created
  Occupant signs: ✅

BIOMETRIC ENROLLMENT:
  Fingerprint enrolled at hostel gate scanner → for entry/exit tracking
  Photo updated for hostel ID card

UNDERTAKINGS FILED: Physical copy → warden; digital copy → EduForge

[Complete Check-In]  [Print Room Card]  [Generate Gate Pass]
```

---

## 4. Waiting List Management

```
WAITING LIST — Boys' Hostel 2026–27
Position 1–30 on waiting list

Vacancies trigger automatic notification:
  1. Student vacates (or TC) → room released
  2. System notifies waiting list position 1 → 48-hour response window
  3. If no response → notifies position 2, and so on
  4. Waiting list student joins with standard check-in process

CURRENT VACANCIES: 0 (all 180 seats filled)
  Room B-117: Expected vacancy — student Vinod K. (226J1A0512) transferred
              to NIT Warangal; TC in progress → room to be released on TC completion

WAITING LIST #1: Prasad M. (226J1A0601) — notified via SMS/app → awaiting response
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hostel/inventory/` | Room inventory and occupancy |
| 2 | `POST` | `/api/v1/college/{id}/hostel/application/` | Submit hostel application |
| 3 | `GET` | `/api/v1/college/{id}/hostel/applications/` | All applications (prioritised list) |
| 4 | `POST` | `/api/v1/college/{id}/hostel/allot/` | Process allotment (bulk or individual) |
| 5 | `POST` | `/api/v1/college/{id}/hostel/checkin/{student_id}/` | Complete student check-in |
| 6 | `GET` | `/api/v1/college/{id}/hostel/waitinglist/` | Waiting list with positions |

---

## 6. Business Rules

- PwD students must be accommodated in ground-floor accessible rooms; NBC 2016 mandates accessible hostel facilities; refusal to accommodate PwD students in accessible rooms is a violation of the RPwD Act 2016 (enforceable by State Commissioner for Persons with Disabilities)
- UGC guidelines mandate a lady warden for girls' hostel who must reside on campus; a male warden for girls' hostel is impermissible; in emergencies (warden absence >2 days), a female faculty member must be designated as acting warden
- Anti-ragging undertaking at hostel check-in is mandatory under UGC Anti-Ragging Regulations 2009 (Regulation 6.1(c)); a student who does not sign cannot be allowed to move in; the undertaking is separate from the one signed at college admission
- Allotment letters must not reveal other residents' personal details to applicants on the waiting list; DPDPA 2023 data minimisation — a waiting list notification contains only the student's own position, not other students' details
- Room condition reports protect both the college and the student; without a documented check-in condition report, any pre-existing damage may be charged to the outgoing occupant on check-out — creating disputes; EduForge makes the check-in condition report mandatory before room keys are issued

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division D*
