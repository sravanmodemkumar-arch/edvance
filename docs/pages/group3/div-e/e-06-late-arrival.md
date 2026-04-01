# E-06 — Late Arrival Register

> **URL:** `/school/attendance/late-arrivals/`
> **File:** `e-06-late-arrival.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Class Teacher (S3) — own class · Administrative Officer (S3) — full (gate management) · Academic Coordinator (S4) — alerts view · Principal (S6) — full

---

## 1. Purpose

Tracks students who arrive at school after the official start time (gate closes / roll call time). Late arrivals are a discipline and safety concern in Indian schools:
- **Gate security:** Students arriving after 8:30 AM (or whatever the school's cut-off is) must sign the late register at the gate before going to class
- **Chronic late arrival:** Students with 3+ late arrivals per month get a note sent home; 5+ = parent meeting; some schools convert late arrivals into half-absence for attendance purposes
- **Class Teacher notification:** When a student is at the gate, the class teacher is notified so they know the student is coming
- **Safety record:** If a student is reported missing, the late arrival register shows the last recorded arrival time

---

## 2. Page Layout

### 2.1 Header
```
Late Arrival Register — 2026–27              [+ Record Late Arrival]  [Export]
Today (27 Mar): 8 late arrivals  ·  This Month (Mar): 42 total
Threshold alerts sent: 3 parents (> 5 late arrivals this month)
```

### 2.2 Today's Late Arrivals
| # | Student | Class | Arrival Time | Reason | Parent Notified | Teacher Notified |
|---|---|---|---|---|---|---|
| 1 | Arjun Sharma | XI-A | 9:05 AM | Traffic jam | ✅ | ✅ |
| 2 | Priya Venkat | VIII-B | 9:22 AM | Doctor visit | ✅ | ✅ |
| 3 | Meera S. | VI-A | 9:45 AM | No reason given | ✅ | ✅ |

---

## 3. Record Late Arrival

[+ Record Late Arrival] → at gate / by class teacher:

| Field | Value |
|---|---|
| Student | [Search by name/roll] |
| Arrival Time | 9:05 AM |
| Reason | Traffic / Doctor / Bus delay / No reason / Other |
| Parent Note | Yes (submitted written note) / No |
| Entry Authorised By | Gate Security / Admin Officer |

On save:
- Class Teacher notified via in-app notification: "Arjun Sharma arrived late at 9:05 AM — going to class"
- Parent notified (if late arrival alert is enabled): "Your ward Arjun Sharma arrived late today at 9:05 AM. — [School Name]"

---

## 4. Monthly Late Arrival Analysis

```
Late Arrival Summary — Class XI-A — March 2026

Roll  Name            Late Arrivals  Threshold Alert
02    Arjun Sharma         6         ✅ Alert sent (5+)
15    Suresh M.            3         —
22    Kavya P.             2         —
```

**Threshold actions:**
- 3 late arrivals/month: WhatsApp alert to parent
- 5 late arrivals/month: Parent called by Class Teacher
- 7+ late arrivals/month: Parent meeting with Academic Coordinator
- Schools that convert late arrivals to half-absences: each late arrival > 30 min counts as 0.5 absence day (configurable)

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/late-arrivals/?date={date}` | Today's late arrivals |
| 2 | `POST` | `/api/v1/school/{id}/attendance/late-arrivals/` | Record late arrival |
| 3 | `GET` | `/api/v1/school/{id}/attendance/late-arrivals/summary/?class_id={id}&month={m}&year={y}` | Monthly summary |
| 4 | `GET` | `/api/v1/school/{id}/attendance/late-arrivals/chronic/?threshold={n}&month={m}` | Chronic late arrivals |

---

## 6. Business Rules

- Late arrival time is captured to the minute — for security purposes; if a student is reported missing later in the day, this is the last recorded entry point
- Schools that convert late arrivals to half-absence (configurable policy) must publish this in their school rules; the E-11 exam eligibility calculation reflects this if the school has enabled it
- Late arrival records older than 3 years are archived (DPDPA data minimisation)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
