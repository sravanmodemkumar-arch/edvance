# I-08 — Incident & Accident Register

> **URL:** `/school/transport/incidents/`
> **File:** `i-08-incident-accident-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Transport In-Charge (S3) — log and manage · Administrative Officer (S3) — documentation · Principal (S6) — review and sign off · Academic Coordinator (S4) — follow-up

---

## 1. Purpose

Records all transport-related incidents: accidents (minor and major), breakdowns, medical emergencies on bus, near-misses, student misconduct, route deviations, and SOS events. This is a safety register with legal significance:
- **Insurance claim:** Requires contemporaneous incident record with GPS data
- **Parent dispute:** Parent claims injury on bus — incident log is legal evidence
- **RTO investigation:** Any road accident involving a school bus triggers RTO inquiry
- **POCSO:** Any incident with child safety implications (assault, inappropriate behaviour by driver/escort) is a mandatory reporting event
- **CBSE affiliation inspection:** Transport safety register is reviewed during inspection

The CBSE Transport Safety Code (2018 circular) requires every school to maintain a transport incident register.

---

## 2. Page Layout

### 2.1 Header

```
Incident & Accident Register — Transport                [+ Log Incident]
Academic Year: [2026–27 ▼]

Total incidents this year: 7
  Minor (breakdown/delay): 4
  Medical on bus: 2
  Road accident: 1 (minor — no injuries)
  POCSO/safety: 0

Pending action (unresolved): 1
```

### 2.2 Incident List

```
INC No.         Date         Route  Type              Status        Severity  Action
TRN/INC/2627/01  2 Apr 2026   R02   Breakdown         ✅ Resolved   Minor     —
TRN/INC/2627/02  15 Apr 2026  R01   Medical (student) ✅ Resolved   Minor     —
TRN/INC/2627/03  1 May 2026   R04   Road accident     ⏳ Pending    Moderate  Follow-up reqd
TRN/INC/2627/04  20 May 2026  R03   Delay (traffic)   ✅ Resolved   Info      —
TRN/INC/2627/05  3 Jun 2026   R01   Student fall       ✅ Resolved   Minor     —
TRN/INC/2627/06  27 Jun 2026  R05   Near-miss          ✅ Resolved   Minor     —
TRN/INC/2627/07  10 Jul 2026  R02   Medical (driver)  ⏳ Pending    Moderate  Route suspended

[Export register]  [View CBSE format report]
```

---

## 3. Log New Incident

```
[+ Log Incident]

Incident Reference: TRN/INC/2627/08  (auto-generated)
Date: [27 March 2026]  Time: [7:18 AM]
Reported by: [Transport In-Charge ▼]

Route involved: [R01 ▼]  Bus: [AP29AB1234]
Driver: Raju Kumar  ·  Escort: Ms. Kavitha

Incident type:
  ○ Road accident (collision/damage)
  ○ Breakdown (vehicle failure)
  ● Medical emergency (student on bus)
  ○ Medical emergency (driver/escort)
  ○ Student misconduct on bus
  ○ Unauthorised person on bus
  ○ Route deviation
  ○ SOS activation
  ○ Near-miss
  ○ Other: [___________]

Incident description:
  [Student Meena P. (VII-B) complained of chest pain and difficulty breathing
   at Stop 3 (Kothapet Bus Stop). Escort called parents immediately. Bus
   diverted to nearest hospital — Apollo Pharmacy, Kothapet. Parent arrived
   in 10 minutes. Student taken to hospital by parent. Route resumed at 7:35 AM.]

Students involved:
  [Meena P. — VII-B]  [+ Add student]

Injuries: ● None apparent  ○ Minor  ○ Major requiring hospitalisation  ○ Fatality

Emergency services called: ○ None  ● Ambulance (108)  ○ Police (100)  ○ Both
  If called: Ambulance called at 7:19 AM — arrived 7:28 AM — student already with parent

Parent notified: ✅ 7:19 AM (Escort called parent directly)
Transport In-Charge notified: ✅ 7:19 AM
Principal notified: ✅ 7:21 AM

GPS data at incident time: [Auto-attached from I-06]
  Location: 17.3789°N, 78.5678°E (Kothapet Bus Stop area)
  Speed at time: 0 km/h (bus had stopped)

CCTV footage: ☑ Preserve footage from this date (manually flagged — prevents loop overwrite)
  Footage window: 6:30 AM – 8:00 AM today  [Flag for preservation]

Follow-up required:
  ● Yes — Parent call-back tomorrow  ○ No

[Save Incident Report]
```

---

## 4. Road Accident — Full Report

```
Incident TRN/INC/2627/03 — Road Accident — 1 May 2026

Route: R04  ·  Bus: AP29IJ7890  ·  Driver: Kishore R.
Time: 7:12 AM  ·  Location: Vanasthalipuram Main Road (near Pillar 168)

Accident description:
  Bus was proceeding on route. An auto-rickshaw came from a side lane without
  stopping. Collision occurred at low speed. Bus has minor damage to front bumper
  (left corner). Auto-rickshaw has dent to right panel. No injuries.

Students on bus: 51 students (boarding in progress — 35 on board at time of accident)
Injuries: None — all students safe ✅
Driver condition: Uninjured ✅  ·  Escort condition: Uninjured ✅

Third party (auto-rickshaw):
  Driver: name/license not yet collected
  TP insurer: Not yet confirmed

Immediate actions taken:
  ✅ 7:12 AM — Driver called Transport In-Charge
  ✅ 7:13 AM — Transport In-Charge called Principal
  ✅ 7:15 AM — Substitute bus (AP29GH3456 — just returned from maintenance) dispatched
  ✅ 7:18 AM — All 51 students transferred to substitute bus; route resumed
  ✅ 7:45 AM — All students reached school (25 min late)
  ✅ 7:16 AM — Parents of all R04 students notified via WhatsApp (F-10 emergency template)
  ✅ 7:30 AM — Police FIR noted at Vanasthalipuram PS (Ref: Cr. No. 234/2026)
  ✅ 8:00 AM — Insurance company informed (Ref: Claim No. NIC/SCH/2627/041)

Insurance claim:
  Policy: National Insurance — School Bus Comprehensive
  Claim opened: 1 May 2026  ·  Claim No.: NIC/SCH/2627/041
  Estimated damage: ₹12,000 (bumper replacement)
  Surveyor visit: 3 May 2026 (scheduled)
  Documents required: [FIR copy] [GPS log] [CCTV footage] [Driver license copy]
  ✅ CCTV footage flagged for preservation on 1 May 2026

RTO inquiry:
  TS Motor Accident Claim Tribunal (MACT) notification: Not required (no injuries)
  RTO Vanasthalipuram: Notified ✅ (mandatory for school bus accident regardless of severity)

Vehicle: AP29IJ7890 — [Assess for roadworthiness]
  ✅ Roadworthy — bumper damage only; cleared to operate from 2 May 2026

Status: ⏳ Pending insurance settlement
[Update insurance status]  [Mark resolved when claim settled]
```

---

## 5. POCSO-Flagged Incident Handling

```
⚠️ POCSO Flag — Special Protocol

If incident type involves any complaint or allegation against driver, escort,
or any adult about inappropriate behaviour, touching, or safety violation
towards a student:

  → This section is RESTRICTED: accessible only by Principal (S6)
     Transport In-Charge is EXCLUDED from this report
     Administrative Officer is EXCLUDED from this report
     Only Designated POCSO Officer (Principal or nominated staff) can view

  Mandatory steps (auto-prompted):
  1. Student is immediately removed from route and alternative transport arranged
  2. Accused (driver/escort) is immediately suspended from duty pending inquiry
  3. School POCSO Committee (F-08) is convened within 24 hours
  4. Parent is notified (Principal calls personally — no WhatsApp for this)
  5. If student is a child (under 18): mandatory report to DCPU within 24 hours
     (Juvenile Justice Act + POCSO Act Section 19)
  6. Police FIR: School cannot delay — mandatory reporting within 24 hours

  This incident is NOT visible in the normal incident register listing.
  It appears only in the POCSO register (F-14 — restricted) and Principal's dashboard.
```

---

## 6. Breakdown Management

```
Incident TRN/INC/2627/01 — Breakdown — 2 April 2026

Route R02  ·  Bus AP29CD5678  ·  7:32 AM

Breakdown type: Tyre puncture (rear left)
Location: LB Nagar bypass (GPS: 17.3123°N, 78.5012°E)
Students on board: 38 students

Actions:
  7:32 AM — Driver called Transport In-Charge
  7:35 AM — Spare bus dispatched (took 22 min to arrive)
  7:57 AM — Students transferred; route resumed
  8:18 AM — Students reached school (48 min late)
  8:05 AM — All R02 parents notified: "Bus R02 had a flat tyre. Students
             transferred to backup bus. ETA school: 8:15 AM. All safe."

Vehicle: Tyre replaced by roadside mechanic — ₹1,200
  [Log in I-01 maintenance log]  [Deduct from I-11 if hired vehicle]

Late arrival logged: 38 students — auto-pushed to E-01 (teachers informed;
  no marks deducted for duty-related late arrival per CBSE policy)

⚠️ Note: Route R02 has had 3 breakdowns in 6 months — escalate to Principal
  for vehicle inspection review [Flag for I-01 comprehensive service review]
```

---

## 7. CBSE Transport Safety Register Export

```
CBSE Transport Safety Register — 2026–27

Format: CBSE Affiliation Bye-Laws Appendix (Transport Safety section)

School: GREENFIELDS SCHOOL  ·  CBSE Affiliation: 1200XXX
Academic Year: 2026–27

S.No.  Date         Route  Incident Type          Persons Affected    Action Taken              Resolved
1      2 Apr 2026   R02    Vehicle breakdown       None               Backup bus deployed        ✅
2      15 Apr 2026  R01    Student medical         Meena P. (VII-B)   Parent notified/hospital   ✅
3      1 May 2026   R04    Road accident (minor)   None — no injuries FIR/insurance filed         ⏳
...

Signed by: Principal — _______________ (signature required)
Date: ________________

[Export as PDF]  [Print for CBSE inspection file]
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/transport/incidents/` | Incident list |
| 2 | `POST` | `/api/v1/school/{id}/transport/incidents/` | Log new incident |
| 3 | `GET` | `/api/v1/school/{id}/transport/incidents/{inc_id}/` | Incident detail |
| 4 | `PATCH` | `/api/v1/school/{id}/transport/incidents/{inc_id}/` | Update incident |
| 5 | `POST` | `/api/v1/school/{id}/transport/incidents/{inc_id}/resolve/` | Mark resolved |
| 6 | `POST` | `/api/v1/school/{id}/transport/incidents/{inc_id}/cctv-flag/` | Flag CCTV footage for preservation |
| 7 | `GET` | `/api/v1/school/{id}/transport/incidents/export/cbse/` | CBSE safety register export |
| 8 | `GET` | `/api/v1/school/{id}/transport/incidents/summary/?year={y}` | Annual summary stats |

---

## 9. Business Rules

- Every incident, regardless of severity, must be logged before the end of the school day; the Transport In-Charge cannot close the day's GPS dashboard without acknowledging unresolved incidents
- A road accident involving a school bus is reported to the RTO and the school's insurance company within 24 hours; the school need not wait for police to initiate this
- CCTV footage (30-day loop on SD card) must be manually flagged for preservation on the day of the incident; after flagging, the system sends a reminder to physically extract the SD card backup within 48 hours
- If a student reports any form of physical or sexual misconduct by transport staff: this is immediately classified as a POCSO incident; the driver/escort is suspended from duty that same day pending inquiry; Transport In-Charge does not handle the investigation — it goes to the POCSO Designated Officer (typically the Principal)
- Insurance documentation: GPS log, CCTV footage, and incident report together constitute the contemporaneous evidence required by insurance surveyors; schools that cannot produce these may have claims rejected
- Incident register (CBSE format) must be available for inspection at any time; the Principal's signature on the register is required termly
- Medical emergency on bus: if a student requires hospital care and the parent is unreachable, the escort accompanies the student to hospital; the school bears the initial emergency medical cost and recovers from parent (documented via D-20 voucher)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division I*
