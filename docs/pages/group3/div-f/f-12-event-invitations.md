# F-12 — Event Invitation Manager

> **URL:** `/school/event-invitations/`
> **File:** `f-12-event-invitations.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Communication Coordinator (S3) — create and manage invitations · Academic Coordinator (S4) — approve · Principal (S6) — formal invitations to VIPs and external guests · Administrative Officer (S3) — RSVP management

---

## 1. Purpose

Manages formal event invitations — both digital (WhatsApp, email, parent portal) and printed (for significant events like Annual Day, Republic Day function, Sports Day). Distinct from F-01 announcements (which are notices); invitations require RSVP, seating allocation, and guest management for formal school events.

Key events requiring formal invitations:
- **Annual Day / Cultural Function** — parents, alumni, district officials, CBSE RO representatives
- **Republic Day / Independence Day function** — parents, local government officials, flag hoisting ceremony
- **Sports Day** — parents, district sports officer, trophy sponsors
- **Graduation ceremony (Class XII farewell)** — parents, invited dignitaries
- **School inauguration / new wing opening** — VIP guests, press, government officials
- **PTM** (handled in F-05 — linked here for combined invitation management)

---

## 2. Page Layout

### 2.1 Header
```
Event Invitation Manager                             [+ New Event Invitation]
Academic Year: [2026–27 ▼]

Active Events: 1 (Annual Day — 22 Feb 2026)
Completed: 4  ·  Upcoming: 1 (Republic Day — 26 Jan 2027)
```

### 2.2 Events List
```
Event             Date         Invitations  Confirmed RSVPs  Status
Annual Day        22 Feb 2026  420          312 (74%)        ✅ Completed
Republic Day      26 Jan 2026  380          290 (76%)        ✅ Completed
Sports Day        15 Jan 2026  380          305 (80%)        ✅ Completed
Class XII Farewell 20 Mar 2026  145          138 (95%)        ✅ Completed
PTM (Mar 2026)    9 Mar 2026   380          312 (82%)        See F-05
```

---

## 3. Create Event Invitation

```
[+ New Event Invitation]

Event Name: [Annual Day 2026 — Greenfields School         ]
Date: [22 February 2026]  Time: [5:00 PM]  Duration: [3 hours]
Venue: [School Auditorium — Ground Floor, Block A          ]

Invitation Type:
  ● Parent invitation (all families)
  ○ Selected class parents only
  ○ VIP / External guest (dignitary, government, alumni)
  ○ Combined (parents + VIPs)

RSVP required: ☑ Yes  ·  RSVP deadline: [18 February 2026]
Seating: ☑ Yes (seat numbers to be allocated based on RSVP)
  Capacity: [500 seats]  ·  VIP section: [20 seats]  ·  General: [480 seats]

Digital Invitation Design:
  Template: [Annual Day — Gold Theme ▼]
  Customise:
    - School logo: ✅ (auto)
    - Event photo/banner: [Upload image] (event banner)
    - Programme highlights: [Cultural show / Prize distribution / Principal address]

Formal Printed Invitation:
  ☑ Generate PDF printed card (for VIP guests)
  Size: [A5 ▼]  Paper: [Art card — 300 gsm]
  Print quantity: [25] (for dignitaries + Chief Guest)

[Preview Digital Invitation]  [Preview Print Card]

Chief Guest:
  Name: [District Collector — Mr. Suresh Babu IAS     ]
  Formal address on invitation: "The District Collector, Guntur District"

[Save & Send Invitations]
```

---

## 4. RSVP Management

```
RSVP Dashboard — Annual Day (22 Feb 2026)

Parents: 312/380 confirmed (82%)
  ● Confirmed (will attend): 290
  ○ Declined: 22
  ○ No response: 68

VIP Guests: 8/10 confirmed
  ✅ District Collector — confirmed (coming)
  ✅ CBSE Regional Officer — confirmed
  ❌ MLA (declined — prior engagement)
  ⬜ DSP (no response) → [Follow-up by phone]

Seating allocation:
  Parents: Rows A–T (480 seats) — auto-assigned by RSVP order
  VIP: Front 2 rows (20 seats) — manually assigned

[Generate Seating Chart]  [Export Guest List for Security]
```

---

## 5. Seating Chart Generation

```
Seating Chart — Annual Day — Greenfields Auditorium

VIP Section (Front):
  Seat 1: District Collector Mr. Suresh Babu IAS
  Seat 2: CBSE RO Representative
  Seat 3: [School Management Chairman]
  ...

General Parent Seating:
  Row A: Parent of Anjali Das (XI-A) — Seat A1
  Row A: Parent of Arjun Sharma (XI-A) — Seat A2
  ...

[Print Seating Plan — A3]  [Export for Reception Desk]
[Print Name Badges — VIP Only]  [QR code entry passes for general parents]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/event-invitations/?year={y}` | Event invitation list |
| 2 | `POST` | `/api/v1/school/{id}/event-invitations/` | Create event invitation |
| 3 | `GET` | `/api/v1/school/{id}/event-invitations/{event_id}/rsvp/` | RSVP status |
| 4 | `POST` | `/api/v1/school/{id}/event-invitations/{event_id}/rsvp/{parent_id}/` | Record RSVP |
| 5 | `GET` | `/api/v1/school/{id}/event-invitations/{event_id}/seating/` | Seating chart |
| 6 | `GET` | `/api/v1/school/{id}/event-invitations/{event_id}/pdf/` | Invitation PDF generation |

---

## 7. Business Rules

- VIP invitations (government officials, CBSE representatives) must be approved by the Principal before sending; parent invitations can be sent by the Communication Coordinator
- Seating allocation is done after RSVP deadline — early birds don't get preferential seating unless specifically configured
- Chief Guest invitation includes a formal request letter (separate from the card) with school letterhead and Principal's signature
- RSVP data is used for catering/seating estimates only — it is not mandatory for entry (walk-ins are accommodated in available seats)
- Event security requires a guest list; the export for security shows name + photo (from parent portal, if available) for VIP verification at entry

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
