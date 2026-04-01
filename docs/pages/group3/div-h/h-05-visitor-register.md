# H-05 — Visitor Register

> **URL:** `/school/hostel/visitors/`
> **File:** `h-05-visitor-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Warden (S3) — log visitors · Administrative Officer (S3) — main gate · Chief Warden (S4) — review and restrict · Principal (S6) — VIP visitor protocol

---

## 1. Purpose

Records all visitors entering the hostel premises — parents, relatives, friends, vendors. Indian boarding school security requirements:
- **MHA Guidelines for Girls' Hostels:** Mandatory visitor register; visitors only allowed in designated reception area (not in rooms); male visitors restricted for girls' hostel
- **POCSO compliance:** Unregistered visitors to hostel premises where children reside is a safeguarding risk; every visitor must be logged with ID
- **Parent visits:** Typically allowed only on designated visiting days (Sunday, or specific hours); surprise visits must be announced
- **Security:** Some residential schools have experienced incidents involving unregistered visitors; the register is both preventive and forensic evidence

---

## 2. Page Layout

### 2.1 Header
```
Visitor Register — Hostel                            [Log New Visitor]
Date: 27 March 2026

Today's visitors: 8
Currently on premises: 3 (not yet signed out)
Restricted visitors (blocked): 0
```

### 2.2 Visitor Log
```
Time In  Name              Relation     Student Visited  ID Verified  Location       Time Out
09:15    Mr. Rajesh Sharma Father       Arjun Sharma     ✅ Aadhaar   Visitor Room    10:30
10:00    Mrs. Vimala Rao   Mother       Chandana Rao     ✅ Aadhaar   Visitor Room    11:45
11:30    Mr. Suresh Das    Uncle        Priya V.         ✅ PAN Card  Visitor Room    🟡 Still inside
14:00    NBD vendor        Book vendor  (school)         ✅ Vehicle   Admin Office    15:30
```

---

## 3. Log Visitor

```
[Log New Visitor]

Visitor name: [Mr. Rajesh Sharma                    ]
Visitor type:
  ● Parent  ○ Relative  ○ Family friend  ○ Teacher (visiting)  ○ Vendor  ○ Official  ○ Other

Student being visited: [Arjun Sharma — XI-A — Room 101]
Relationship to student: [Father]

ID verification:
  ID Type: [Aadhaar Card ▼]  ID Number: [XXXX XXXX 1234] (masked)
  ID verified physically: ☑ Yes (Warden/Gate staff signed)

Contact number: [+91 9876-XXXXX] (auto-filled from C-20 family record if parent)
Vehicle number: [AP29 AB 1234] (if applicable)

Visit area:
  ● Visitor Reception Room (standard)
  ○ Hostel room (special permission required from Chief Warden)
  ○ School grounds
  ○ Admin office (vendor/official)

Girls' hostel protocol:
  Male visitors to Girls' Hostel → allowed only in Visitor Reception Room
  No male visitor beyond reception area (MHA guidelines)
  Female warden must be present during the visit

Time in: [9:15 AM]  ·  Escorted by: [Gate Security → Warden]

[Save Visitor Entry]  [Generate Visitor Slip]
```

---

## 4. Visitor Slip

```
VISITOR PASS — GREENFIELDS SCHOOL HOSTEL
Visitor: Mr. Rajesh Sharma (Father of Arjun Sharma, XI-A)
Date: 27 March 2026  ·  Time In: 9:15 AM
Visit Area: Visitor Reception Room
ID: Aadhaar Card verified ✅
[School Seal]  [Warden signature]

Visitor is requested to:
  • Remain within the designated visitor area
  • Return this slip when leaving
  • Obtain exit stamp from warden on departure

[Print Visitor Slip]
```

---

## 5. Restricted Visitor Management

```
Restricted Visitors:

Restriction can be placed by: Chief Warden or Principal (for safety/welfare reasons)

Example:
  Visitor: Mr. X (uncle of Priya V.) — Restricted since: 15 Feb 2026
  Reason: [Confidential — welfare concern flagged by H-12 student welfare]
  Action if visitor arrives: Alert Chief Warden immediately; do not grant entry

[Add to Restricted List]  [Review Restrictions]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/visitors/?date={date}` | Visitor log for date |
| 2 | `POST` | `/api/v1/school/{id}/hostel/visitors/` | Log visitor entry |
| 3 | `PATCH` | `/api/v1/school/{id}/hostel/visitors/{visit_id}/exit/` | Record exit time |
| 4 | `GET` | `/api/v1/school/{id}/hostel/visitors/restricted/` | Restricted visitors list |
| 5 | `POST` | `/api/v1/school/{id}/hostel/visitors/restricted/` | Add visitor restriction |
| 6 | `GET` | `/api/v1/school/{id}/hostel/visitors/export/?from={date}&to={date}` | Export visitor log |

---

## 7. Business Rules

- Every visitor must show valid government-issued photo ID; the ID number is recorded but masked in the register (only last 4 digits visible to staff other than Chief Warden)
- Male visitors are not allowed in girls' hostel rooms under any circumstances; violation of this rule is grounds for a conduct inquiry and report to the school management
- If a visitor is visiting a student who is on H-04 leave (not in hostel), the visitor is informed and the visit is logged as "student absent" — useful for tracking if an undisclosed meeting occurs
- Restricted visitor flag is handled with confidentiality — the gate/warden is told not to admit the person but not told the reason; the reason is accessible only to Chief Warden and Principal
- Vendor/maintenance visitor log is maintained for hostel premises (not school premises which are handled separately)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
