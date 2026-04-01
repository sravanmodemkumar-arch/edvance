# K-10 — Data Privacy (DPDPA 2023) Compliance

> **URL:** `/school/compliance/dpdpa/`
> **File:** `k-10-data-privacy-dpdpa.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Data Protection Officer / DPO (S5 — Principal or nominated VP) — full access · Principal (S6) — oversight · Compliance Officer (S4) — implementation tracking · Administrative Officer (S3) — consent management

---

## 1. Purpose

India's Digital Personal Data Protection Act 2023 (DPDPA) imposes obligations on "Data Fiduciaries" — organisations that collect and process personal data. A school is a Data Fiduciary because it collects and processes personal data of students (minors), parents, and staff.

Key DPDPA obligations for schools:
- **Consent:** Lawful basis for processing personal data; verifiable parental consent for minors
- **Purpose limitation:** Data collected for school operations cannot be used for marketing or third-party purposes without separate consent
- **Data minimisation:** Collect only what is necessary
- **Data retention:** Personal data should not be held longer than necessary
- **Data breach notification:** Report to Data Protection Board within the prescribed timeframe (rules pending — likely 72 hours)
- **Data Principal rights:** Access, correction, erasure (with limitations for minors), grievance redressal
- **Data Protection Officer (DPO):** Required for significant data fiduciaries; schools handling data of all enrolled students should appoint one
- **Special category data:** Health, disability, POCSO-related data requires additional protection

---

## 2. DPDPA Compliance Dashboard

```
DPDPA 2023 Compliance Dashboard                      [Consent Status]  [Breach Log]
27 March 2026

Data Protection Officer: Ms. Meena Rao (Principal — acting DPO)
Registration with Data Protection Board: ⬜ Pending (rules not yet notified; school preparing)

Consent management:
  Student enrollment consent (parent): 374/380 obtained ✅ (6 new students — pending follow-up)
  Staff data processing consent: 87/87 ✅
  Communication consent (WhatsApp/SMS): 372/380 ✅ (8 opted out — respected)

Data breach log:
  Incidents this year: 0 ✅

Data access requests received: 2
  Request 1: Parent of Arjun S. — requested academic records → fulfilled in 7 days ✅
  Request 2: Former student (2024 pass-out) — TC and marks → fulfilled ✅

Data erasure requests: 1
  Request: Parent requested deletion of child's data after transfer to another school
  Status: ⏳ Under review (school must balance erasure request against statutory retention requirements)
```

---

## 3. Consent Management

```
Consent Framework — GREENFIELDS SCHOOL

At Enrollment:
  Parent signs a Data Collection and Processing Consent at admission (C-05):
  ✅ Collection of student and parent personal data for school operations
  ✅ Sharing with CBSE for examination and affiliation purposes
  ✅ Sharing with government portals (DISE/UDISE, NSP scholarships, state education dept)
  ✅ WhatsApp/SMS communication for attendance, fee, and safety notifications
  ✅ CCTV monitoring on school premises for safety
  ✅ Achievement photography for school publications (with opt-out option)
  ✅ GPS tracking on school bus (safety purpose — cannot be opted out)

Separate explicit consent required for:
  ⬜ Sharing student data with third-party vendors (e.g., external exam providers)
  ⬜ Use of student data for research, analytics beyond school operations
  ⬜ Publishing photographs/names in external media or third-party websites

Cannot be opted out of (legitimate interest / legal obligation):
  ● CBSE data submission (OASIS, LOC) — legal requirement
  ● Government portal reporting (DISE, RTE data) — legal requirement
  ● Police/court data disclosure on lawful order
  ● POCSO mandatory reporting — legal requirement overrides consent

Opt-out register (communication):
  8 parents have opted out of promotional/non-safety WhatsApp messages ✅
  Opt-outs respected in F-03 messaging module ✅
  Safety messages (bus late, SOS) — non-opt-outable ✅ (I-10 rules)
```

---

## 4. Data Inventory (What Data the School Holds)

```
Data Inventory — Personal Data Categories

Category              Data Types                            Sensitivity   Retention
Student basic info    Name, DOB, address, photo             Normal        Active enrollment + 10yr
Academic records      Marks, attendance, reports            Normal        Permanent (CBSE req.)
Health records        Blood group, allergies, conditions    High (special) Active + 3yr
Counselling records   Session notes, welfare flags          Very high     Active + 3yr
Financial records     Fee payments, bank details            High          7yr (Income Tax)
POCSO records         Disclosure, case records              Highest       Permanent
Discipline records    Incident log                          High          Active + 5yr
Parent contact data   Phone, email, address                 Normal        Active + 3yr
Staff personal data   Qualification, BGV, salary            High          Employment + 7yr
CCTV footage          Video of school premises              Medium        30 days overwrite
GPS tracking data     Bus location logs                     Medium        90 days (incidents: permanent)
Biometric (if any)    Fingerprint/face for attendance       Very high     Active enrollment only

Third-party sharing:
  CBSE: Student enrollment, exam data ✅ (consented; legal basis)
  Government portals (DISE, NSP): Aggregate + individual as required ✅
  WhatsApp (Meta): Template messages via approved BSP ✅ (DLT templates; no data stored by BSP)
  GPS vendor: Location data only (AIS-140 VLT) ✅
  No advertising/marketing platforms receive any school data ✅
```

---

## 5. Data Breach Protocol

```
Data Breach Response Protocol

DPDPA Section 8: Data Fiduciary must notify the Data Protection Board within
  the prescribed period (72 hours in draft rules) of becoming aware of a personal
  data breach that is likely to cause harm to Data Principals.

Breach categories:
  Level 1: Internal access control breach (staff member accessed data outside their role)
    Action: Log internally; investigate; fix access control; no external notification needed unless harm risk
  Level 2: Data theft or unauthorised external access (hacking, lost device with data)
    Action: Immediate containment; DPO notification within 1 hour; Board notification per DPDPA timeline
  Level 3: Large-scale exposure (multiple students' sensitive data exposed)
    Action: Board notification; affected parent notification; Principal crisis management

Current breach: 0 ✅

Breach log format:
  Date/time discovered: [___]
  Nature of breach: [___]
  Data affected: [number of individuals, data types]
  Likely harm: [___]
  Containment steps taken: [___]
  Notification sent to Data Protection Board: [Yes/No] — [Date/time]
  Notification sent to affected Data Principals: [Yes/No] — [Date/time]
  Root cause analysis: [___]
  Preventive measures implemented: [___]

[Log new breach]  [Generate DPB notification draft]
```

---

## 6. Data Principal Rights Management

```
Data Principal Rights Requests

DPDPA Section 11–13: Rights of Data Principals:
  ● Right to access personal data held
  ● Right to correction of inaccurate data
  ● Right to erasure (with limitations)
  ● Right to nominate (minor's parent acts on their behalf)
  ● Right to grievance redressal

Active requests:

Request 1: Parent of Kiran S. — Erasure request
  Status: ⏳ Under review
  Concern: School cannot erase data that it is legally required to retain
    (CBSE admission records, TC, academic history — permanent retention required)
  Response draft: "Under DPDPA Section 8(7), we are required to retain personal
    data as long as necessary for legal or regulatory compliance. CBSE requires us
    to retain student academic records permanently. We will delete marketing/non-essential
    data (preference settings, communication logs beyond 180 days) upon your request.
    Academic and enrollment records cannot be deleted."
  [Send response]  [Close request]

Response SLA: 30 days (DPDPA specifies — school adopts this)
Grievance escalation: To DPO (Principal) within 7 days of unresolved request
  Second escalation: To Data Protection Board (DPB) if school fails to resolve
```

---

## 7. Staff Training on DPDPA

```
DPDPA Staff Training — 2026–27

All staff handling student data must understand their obligations.

Training content:
  ☑ What is personal data (with school-specific examples)
  ☑ Why we need consent before sharing data
  ☑ What data they can access in their role (need-to-know)
  ☑ What to do if they accidentally see data they shouldn't
  ☑ What to do if a parent asks about their data
  ☑ What is a data breach and how to report it
  ☑ Never share student data on personal WhatsApp/email for convenience

Training conducted: 22 June 2026 (combined with POCSO training)
Attendance: 85/87 ✅ (2 pending makeup)

Key rules reinforced:
  ● Do not screenshot student data and share on personal devices
  ● Do not discuss student welfare/health information in public spaces
  ● Always log out of EduForge after use on shared computers
  ● Never share your EduForge login credentials with colleagues
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/compliance/dpdpa/dashboard/` | DPDPA compliance overview |
| 2 | `GET` | `/api/v1/school/{id}/compliance/dpdpa/consent-status/` | Consent collection status |
| 3 | `POST` | `/api/v1/school/{id}/compliance/dpdpa/consent/{student_id}/update/` | Update consent record |
| 4 | `GET` | `/api/v1/school/{id}/compliance/dpdpa/breach-log/` | Data breach log |
| 5 | `POST` | `/api/v1/school/{id}/compliance/dpdpa/breach-log/` | Log new breach |
| 6 | `GET` | `/api/v1/school/{id}/compliance/dpdpa/rights-requests/` | Data principal rights requests |
| 7 | `POST` | `/api/v1/school/{id}/compliance/dpdpa/rights-requests/` | Log new rights request |
| 8 | `PATCH` | `/api/v1/school/{id}/compliance/dpdpa/rights-requests/{req_id}/respond/` | Log response to request |

---

## 9. Business Rules

- DPDPA Rules 2025 (draft): pending final notification; school should operate as if the rules are in effect (proactive compliance is the safest position; retroactive compliance after enforcement is harder)
- Consent must be free, specific, informed, and unambiguous; bundling "by enrolling your child you agree to all data uses" into a general enrollment form is not DPDPA-compliant; specific uses must be listed and separately consented
- Children's data (under 18) requires verifiable parental consent; for students 18+, the student themselves is the Data Principal; handover of data rights occurs at 18
- School data must not be used for any purpose beyond education administration; using student contact data for advertising school events to external parties (e.g., coaching institutes) without consent is a violation
- EduForge as a data processor: EduForge (the platform) processes school data under a Data Processing Agreement (DPA); the school is the Data Fiduciary; EduForge does not use school student data for training models, analytics, or any purpose beyond providing the software service
- Security measures mandated: role-based access control (RBAC) — enforced throughout EduForge; encryption at rest (Cloudflare R2 encryption); encryption in transit (TLS 1.3); audit logs for all data access; session timeouts after inactivity

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division K*
