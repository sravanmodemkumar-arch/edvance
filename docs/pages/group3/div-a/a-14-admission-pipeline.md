# A-14 — Admission Pipeline

> **URL:** `/school/admin/admissions/pipeline/`
> **File:** `a-14-admission-pipeline.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** VP Admin (S5) — full · Admin Officer (S3) — manage · Principal (S6) — approve/view · Promoter (S7) — view

---

## 1. Purpose

End-to-end admission management from first enquiry to student enrollment. In Indian schools, the admission season runs November–April for the next academic year. Large schools with good reputation have enquiries starting in October; under-enrolled schools run admission drives into June. This page manages the full funnel and gives leadership real-time seat-fill visibility.

**Indian admissions context:**
- CBSE/ICSE schools do not have government-mandated common admission processes (unlike IITs/NITs)
- Schools set their own admission criteria: written test (often for Class IX–XI), interview, entrance test
- RTE Act: 25% seats in Class 1 (or entry-level class) must be reserved for EWS students — free of charge
- Many large school groups: admission enquiries come via WhatsApp, phone, school website, social media, and walk-in
- Common cycle: Enquiry → Application Form → Test/Interview → Offer → Fee Payment → Enrollment

---

## 2. Page Layout

### 2.1 Header
```
Admission Pipeline — 2026–27 Season         [+ New Enquiry]  [View Seats]  [Export]  [Filters ▼]
Current Season: 2026–27 ▼      Cutoff Date: 31 May 2026
```

### 2.2 Funnel Summary Strip

```
Enquiries: 1,240  →  Applications: 680  →  Tests/Interview: 420  →  Offers: 380  →  Confirmed: 312  →  Reported: 287
  (100%)               (54.8%)                (33.9%)                (30.6%)           (25.2%)             (23.1%)
```

Percentage shows conversion from total enquiries. Green if on track vs last year; red if lagging.

---

## 3. Main Sections

### 3.1 Pipeline Kanban Board

Swimlane Kanban — one column per stage:

**Columns:**
1. **Enquiry** — Initial contact received (call/walk-in/WhatsApp/website/app)
2. **Application Received** — Application form submitted + application fee paid
3. **Test/Interview Scheduled** — Entrance test or interview date assigned
4. **Test/Interview Done** — Result pending
5. **Offer Given** — Admission offer letter generated + sent to parents
6. **Fee Paid** — First instalment / full fee paid; student admitted
7. **Reported** — Student physically reported on first day; enrollment complete

Each card: Student name · Class applying for · Parent name · Contact · Source · Date · [Move Forward ▶] [View] [Call]

Drag-and-drop to move cards between stages. Server-side HTMX swap on drop.

Filter Kanban by: Class / Stream / Source / Date range

### 3.2 Table View (toggle from Kanban)

| Student | Class | Stage | Applied Date | Last Activity | Days in Current Stage | Source | Counsellor | Action |
|---|---|---|---|---|---|---|---|---|
| Aryan Sharma | IX | Offer Given | 15 Mar 2026 | 22 Mar 2026 | 8 days | Walk-in | Ms. Priya | [Follow Up] |
| … | … | … | … | … | … | … | … | … |

Colour alert: Orange if > 7 days in same stage; Red if > 14 days (at risk of dropping off).

---

## 4. Class-wise Seat Availability

| Class | Capacity | Enrolled (current year) | Promotions to fill | Available Next Year | Applications | Offers | Confirmed |
|---|---|---|---|---|---|---|---|
| LKG | 90 | 78 | 0 (new entry class) | 90 | 142 | 80 | 64 |
| Class I | 120 | 142 (over-cap) | ~138 promote from LKG | ~18 + LKG graduates | 98 | 60 | 48 |
| Class VI | 90 | 80 | ~78 promote from V | ~12 lateral seats | 44 | 28 | 22 |
| Class IX | 120 | 112 | ~105 promote from VIII | ~15 lateral seats | 68 | 42 | 38 |
| Class XI | 120 | 76 | ~100 promote from X (estimated) | ~20 remaining | 118 | 88 | 72 |
| **Total** | **1,200** | | | **~152** | **1,240** | **680** | **312** |

---

## 5. RTE Admission Tracker

**Section within Admission Pipeline for RTE-25% management:**
- Classes with RTE seats: entry-level class (LKG or Class I per school)
- Mandated seats: 25% of total intake capacity
- Applications from EWS/DG category: count received
- Lottery date (if applications > seats): [Schedule Lottery]
- Results of lottery: list of selected students + wait-list
- Documentation status per selected student: Income certificate · Caste certificate · Age proof · Residence proof
- [Generate RTE List for RTE Portal] — submits to state RTE portal

---

## 6. Admission Form Configuration

**[Configure Admission Form]** button (Principal only):
- Sections in form: Personal info · Academic info · Previous school (if applicable) · Parent/Guardian details · Documents
- Required vs optional fields
- Application fee amount: ₹[amount] (refundable if not selected: Yes/No)
- Online payment toggle: enable/disable
- Form available from: [date] to [date]
- [Preview Form] → how it looks to parents on the portal

---

## 7. Key Drawers

### `admission-process` (from enquiry card / row)
640px wide, tabs:
- **Enquiry:** Source, date, notes, contact history
- **Application:** Form filled status, documents, application fee status
- **Assessment:** Test score (if applicable), interview notes
- **Offer:** Offer letter details, fee amount, acceptance deadline
- **Enrollment:** Fee payment confirmation, admission number assignment, section allocation
- **Timeline:** Full activity log from first contact to enrollment

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/admissions/pipeline/` | Pipeline data (all stages) |
| 2 | `POST` | `/api/v1/school/{id}/admissions/enquiries/` | Create new enquiry |
| 3 | `GET` | `/api/v1/school/{id}/admissions/{app_id}/` | Application detail |
| 4 | `PATCH` | `/api/v1/school/{id}/admissions/{app_id}/stage/` | Move to next stage |
| 5 | `GET` | `/api/v1/school/{id}/admissions/seat-availability/` | Class-wise seat table |
| 6 | `GET` | `/api/v1/school/{id}/admissions/rte/` | RTE applicants + status |
| 7 | `POST` | `/api/v1/school/{id}/admissions/rte/lottery/` | Run RTE lottery |
| 8 | `POST` | `/api/v1/school/{id}/admissions/{app_id}/offer/` | Generate offer letter |
| 9 | `GET` | `/api/v1/school/{id}/admissions/{app_id}/offer/pdf/` | Offer letter PDF |
| 10 | `POST` | `/api/v1/school/{id}/admissions/{app_id}/enroll/` | Confirm enrollment + assign admission no |
| 11 | `GET` | `/api/v1/school/{id}/admissions/funnel/` | Funnel conversion data |

---

## 9. Business Rules

- Enrollment is only complete after fee payment confirmation is received (online) or manually marked (offline cash)
- RTE students: zero fees charged; admission fee waived; no deposit
- Admission number auto-generated: School prefix + Year + 4-digit serial (e.g., SVHS-2026-0001)
- Applications from previous years: archived automatically at academic year start; new season = fresh pipeline
- Offers expire after 14 days (configurable); expired offers → applicant moved back to "Applied" stage

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
