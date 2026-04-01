# H-02 — Hostel Admission

> **URL:** `/school/hostel/admission/`
> **File:** `h-02-hostel-admission.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Administrative Officer (S3) — intake and data entry · Chief Warden (S4) — approve admission · Principal (S6) — approve waitlist overrides · Hostel Accountant (S3) — fee setup

---

## 1. Purpose

Manages hostel admission applications — separate from school admission (C-02). A student may be admitted to the school but may apply for hostel separately (if hostel capacity is limited). Tracks the hostel admission waitlist, allocation, and move-in process.

---

## 2. Page Layout

### 2.1 Header
```
Hostel Admission                                     [+ New Hostel Application]
Academic Year: [2026–27 ▼]

Total hostel capacity: 300 (180 boys + 120 girls)
Current occupants: 280  ·  Vacant: 20
Applications pending: 12 (8 boys, 4 girls)
Waitlist: 5 (3 boys, 2 girls — capacity exceeded)
```

### 2.2 Applications
```
Application No.  Student         Class  Gender  Applied      Status
HAPP/2026/012    Chandana Rao   XI-A   Female  25 Mar 26    🟡 Under Review
HAPP/2026/011    Vijay P.       IX-B   Male    22 Mar 26    🟡 Under Review
HAPP/2026/010    Suresh M.      VIII-A Male    15 Mar 26    ✅ Approved → Room 102-B
HAPP/2026/009    Meena K.       VII-B  Female  10 Mar 26    ⏳ Waitlisted (Position 2)
```

---

## 3. Hostel Application Form

```
[+ New Hostel Application]

Student: [Chandana Rao — STU-0001190 — XI-A]
Academic Year: [2026–27 ▼]
Gender: Female → Girls' Hostel Block B

Admission type:
  ● Full boarding (Mon–Sun; home on school holidays only)
  ○ Day boarding (stays Mon–Fri; goes home weekends)

Room preference (optional):
  Roommate preference: [Priya Venkat — if available]
  No preference: ○

Parent/Guardian details (for hostel records — may differ from school records):
  Primary contact: Father — Mr. Raghav Das  +91 9876-XXXXX
  Emergency contact: Uncle — Mr. Suresh Das  +91 8765-XXXXX
  Local guardian (if different from parents): [Name, Address, Phone]

Medical information:
  Allergies: [None ▼]
  Chronic conditions: [Mild asthma — inhaler required]
  Dietary requirement: ● Vegetarian  ○ Non-vegetarian  ○ Jain  ○ Vegan  ○ Other
  Medication: [Salbutamol inhaler — to be kept with Matron]

Documents required:
  ☑ Medical fitness certificate (doctor's letter)
  ☑ Parent ID proof
  ☑ Address proof (for local guardian)
  ☑ 4 passport photos

Fee category (set by room allocated):
  Double room: ₹12,000/term (hostel + mess)
  [Wait for room allocation to confirm]

[Submit Application]
```

---

## 4. Approval & Move-In

```
Approval — HAPP/2026/012 — Chandana Rao

Chief Warden review:
  Capacity check: Girls' hostel 112/120 — 8 vacancies ✅
  Medical review: Asthma noted — Matron briefed ✅
  Room allocated: Block B, Room 201, Bed 2B

[Approve Admission]

Move-in checklist:
  Date: 28 March 2026
  ☑ Room key issued (Room 201)
  ☑ Bedding kit issued (H-11 inventory)
  ☑ Locker assigned: Locker 42-B
  ☑ Mess card issued
  ☑ Parent contact updated in hostel register
  ☑ Medical info handed to Matron
  ☑ Emergency contact form signed by parent
  ☑ Hostel rules booklet issued + parent receipt

[Complete Move-In]
```

---

## 5. Waitlist Management

```
Waitlist — Boys' Hostel (Capacity full: 180/180)

Position  Student          Class  Applied    Notes
1         Ravi P.          X-B    1 Feb 26   Waiting for vacancy in double room
2         Anand V.         IX-A   15 Feb 26
3         Kishore M.       VIII-B 10 Mar 26

When a vacancy opens (student withdraws or is removed from hostel):
  → Position 1 (Ravi P.) is notified via WhatsApp
  → 3-day window to confirm admission
  → If declined → Position 2 gets the offer
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/admission/?year={y}` | Application list |
| 2 | `POST` | `/api/v1/school/{id}/hostel/admission/` | New hostel application |
| 3 | `POST` | `/api/v1/school/{id}/hostel/admission/{app_id}/approve/` | Approve and allocate room |
| 4 | `GET` | `/api/v1/school/{id}/hostel/admission/waitlist/?gender={m|f}` | Waitlist |
| 5 | `POST` | `/api/v1/school/{id}/hostel/admission/{app_id}/move-in/` | Complete move-in checklist |

---

## 7. Business Rules

- Hostel admission is separate from school admission; a student can be enrolled in the school without being a boarder
- Girls' hostel applications are reviewed only by female wardens and the Principal; male administrative staff do not have access to girls' hostel applications (privacy + safety)
- Medical fitness certificate is mandatory before move-in; students with chronic conditions require specific medical clearance and their medical info is shared with the Matron
- Local guardian details are mandatory if parents live > 100 km from the school (emergency contact who can reach the hostel within 2 hours)
- Hostel admission fee (caution deposit) is separate from hostel term fee; it is tracked in D-14 Security Deposit and refunded on exit

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
