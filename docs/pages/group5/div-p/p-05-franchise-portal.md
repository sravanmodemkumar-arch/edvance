# P-05 — Franchise Partner Portal

> **URL:** `/coaching/partners/franchise/`
> **File:** `p-05-franchise-portal.md`
> **Priority:** P2
> **Roles:** Director (K7) · Franchise Coordinator (K4) · Franchise Branch Manager (external)

---

## 1. Franchise Portal Dashboard

```
FRANCHISE PARTNER PORTAL — TCC Hyderabad (Head Office)
As of 31 March 2026

  ┌──────────────────────────────────────────────────────────────────────┐
  │  FRANCHISE NETWORK OVERVIEW                       [Export MIS PDF]  │
  ├──────────────────┬─────────────────┬───────────────┬────────────────┤
  │  TOTAL STUDENTS  │  MONTHLY ROYALTY │  ACTIVE BRANCHES│  ALERTS      │
  │     2,160        │    ₹3.24 L      │       6        │  1 (F2 ⚠️)  │
  │  (all branches)  │  (all branches) │   (+ 2 planned)│              │
  └──────────────────┴─────────────────┴───────────────┴────────────────┘

  FRANCHISE STATUS TABLE:
    Branch      │ Students │ Royalty Due │ Royalty Paid │ Rating │ MIS Report │ Status
    ────────────┼──────────┼─────────────┼──────────────┼────────┼────────────┼──────────
    F1 Secy     │    640   │   ₹96,000   │  ₹96,000 ✅  │  4.0   │ ✅ On time │ Green
    F2 Warangal │    480   │   ₹72,000   │  ₹72,000 ✅  │  3.8   │ 🟡 Late    │ Review ⚠️
    F3 Nizbd    │    360   │   ₹54,000   │  ₹54,000 ✅  │  4.1   │ ✅ On time │ Green
    F4 Karimnagar│   280   │   ₹42,000   │  ₹42,000 ✅  │  4.0   │ ✅ On time │ Green
    F5 Nalgonda │    220   │   ₹33,000   │  ₹33,000 ✅  │  4.1   │ ✅ On time │ Green
    F6 Khammam  │    180   │   ₹27,000   │  ₹27,000 ✅  │  4.0   │ ✅ On time │ Green
    ────────────┴──────────┴─────────────┴──────────────┴────────┴────────────┴──────────
    TOTAL       │  2,160   │  ₹3,24,000  │ ₹3,24,000 ✅ │  4.0 avg│             │
```

---

## 2. Franchise MIS Submission

```
FRANCHISE MIS SUBMISSION — F1 TCC Secunderabad
Submitted: 5 March 2026 (on time ✅) | Period: February 2026

  ENROLLMENT DATA:
    Active students (Feb):       640
    New admissions (Feb):         28
    Dropouts (Feb):                3
    Net change:                  +25

  ACADEMIC DATA:
    Mock tests conducted:          2
    Average score (full mock):   138/200
    Faculty attendance rate:     94.8%
    Doubt resolution SLA:        88.4%

  FINANCIAL DATA:
    Fees collected (Feb):        ₹8.4 L
    Royalty remitted:            ₹96,000 ✅
    Outstanding dues:            ₹1.2 L (24 students)

  OPERATIONAL DATA:
    Open grievances:              1 (resolved within SLA ✅)
    Maintenance issues:           2 open (< 7 days)
    Staff attendance:            96.2%

  FRANCHISE COORDINATOR REVIEW:
    Data verified: ✅ | Discrepancies: None | Flag to Director: None
```

---

## 3. Franchise Communication

```
FRANCHISE COMMUNICATION HUB — March 2026

  ANNOUNCEMENTS FROM HEAD OFFICE:
    28 Mar — Q4 Mock Test Schedule (Mocks #26–30 dates) [Sent to all] ✅
    20 Mar — Study Material Update: GK Supplement Apr 2026 [Distributed] ✅
    15 Mar — Franchise Meeting Agenda — Apr 10 (annual conference) [Sent] ✅
    1 Mar  — New EduForge features (v4.2): Training video shared [Sent] ✅

  FRANCHISE ANNUAL CONFERENCE (Apr 10, 2026):
    Venue:    TCC Hyderabad Main — Hall A
    Agenda:
      10:00  Director's address: AY 2025–26 performance review
      11:00  Academic Director: Q3 results analysis + Q4 curriculum
      12:00  Branch best practice sharing (F3 Nizamabad — attendance initiative)
      13:00  Lunch
      14:00  Marketing: new campaign templates + summer batch
      15:00  Compliance update: DPDPA + GST changes
      16:00  Q&A + individual franchise reviews (30 min per branch)
    Attendance: All 6 franchise branch managers (confirmed) ✅

  FRANCHISE HELPDESK (head office → franchise support):
    EduForge issues:    IT Coordinator — suman@tcc.in
    Academic queries:   Academic Director — academic@tcc.in
    Compliance:         Branch Manager — km@tcc.in
    Urgent (Director):  director@tcc.in | +91-98765-YYYYY (WhatsApp)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/partners/franchise/dashboard/` | Franchise network dashboard (HQ view) |
| 2 | `GET` | `/api/v1/coaching/{id}/partners/franchise/{fid}/` | Individual franchise detail |
| 3 | `POST` | `/api/v1/coaching/{id}/partners/franchise/{fid}/mis/` | Submit monthly MIS (franchise) |
| 4 | `GET` | `/api/v1/coaching/{id}/partners/franchise/communication/` | Franchise announcements |
| 5 | `POST` | `/api/v1/coaching/{id}/partners/franchise/announcement/` | Send announcement to all franchises |
| 6 | `GET` | `/api/v1/coaching/{id}/partners/franchise/royalty/?month=2026-03` | Royalty collection status |

---

## 5. Business Rules

- The franchise portal is TCC's operational interface with its partner network; it must provide real-time visibility into each franchise's performance without requiring phone calls or email requests; a Franchise Coordinator who must call each branch to get their enrollment numbers is working inefficiently; the portal's MIS submission feature (Step 2 above) standardises the data that each franchise reports and the timeline (5th of each month); a franchise that consistently submits MIS late (F2 Warangal — 8th instead of 5th) is undermining the Head Office's ability to prepare consolidated reports; MIS delay is documented as a franchise agreement compliance issue
- Royalty calculation and collection are governed by the franchise agreement; the royalty rate (₹1,500 per enrolled student per month) must be applied to the franchise's reported enrollment; if a franchise under-reports enrollment (claiming 480 students when they have 520 to reduce royalty), this is a franchise agreement breach; TCC's annual audit visit includes a physical headcount of enrolled students against the franchise's reported data; discrepancies above 5% trigger a royalty adjustment invoice and a formal warning; three instances of material under-reporting are grounds for franchise termination
- The annual franchise conference (Apr 10) is TCC's most valuable tool for maintaining brand cohesion and knowledge sharing across branches; franchise branch managers who are isolated from the head office develop different practices (some better, some worse) over time; the conference resets alignment — the academic curriculum, marketing templates, compliance requirements, and system updates are all standardised at the conference; the "best practice sharing" segment (F3 Nizamabad presenting their attendance improvement initiative) creates a peer-learning culture where franchise managers learn from each other, not just from Head Office
- Study material distribution to franchises follows a master-copy model; TCC creates the master PDF/print-ready files and distributes them to franchises; each franchise prints locally (using their own printing vendor or TCC's approved vendor at negotiated rates); this avoids TCC having to ship physical materials across Telangana and allows franchises to print on-demand; however, the master copies are TCC's intellectual property; a franchise cannot share the master files with competitors, modify the content, or sell study material separately; the franchise agreement explicitly grants the right to print-for-students only
- The franchise helpdesk (IT Coordinator, Academic Director, Branch Manager, Director) ensures that franchise staff have clear escalation paths for different types of issues; a franchise branch manager who calls the Director for an EduForge login issue is bypassing the correct channel; having clear, named contacts for different categories of issues (IT vs academic vs compliance) reduces the Director's operational interruptions and ensures issues reach the right expert quickly; the helpdesk contacts are communicated at the annual conference and updated whenever staff changes at TCC Head Office

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division P*
