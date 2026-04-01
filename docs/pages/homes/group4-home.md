# Home Page: Group 4 — College Portal (Intermediate)
**Route:** `/home`
**Domain:** `www.college.com` (custom) or `[slug].eduforge.in/college`
**Access:** All roles — content changes per role
**Portal type:** Intermediate college (Class 11–12) — MPC, BiPC, CEC, MEC streams

---

## Overview

| Property | Value |
|---|---|
| Purpose | Intermediate college management — stream-based academics, board exams, JEE/NEET integrated coaching |
| Domain | College's own domain (e.g., `www.narayana-junior.ac.in`) |
| Key difference from School | Stream-based (MPC/BiPC/CEC/MEC), board exam focus, JEE/NEET integrated batches, residential + day scholar mix |
| Roles | Principal, Vice Principal, Lecturer, HOD (per stream), Admin, Accountant, Hostel Warden, Student |

---

## Role-Based Home View Matrix

| Role | Home Shows |
|---|---|
| Principal | Full college dashboard — all streams, all KPIs, board exam preparation status |
| Vice Principal | Academic performance, lecturer workload, discipline records |
| HOD — MPC | MPC stream only — Maths/Physics/Chemistry performance, JEE rank trends |
| HOD — BiPC | BiPC stream only — Biology/Physics/Chemistry, NEET preparation |
| Lecturer | Their subject sections — upcoming tests, student marks, MCQ queue |
| Admin / Registrar | Admissions, certificates, TC, student records |
| Accountant | Fee collection — quarterly/annual structure |
| Hostel Warden | Hostel occupancy, welfare, mess |
| Student | Personal dashboard — stream-specific, board exam countdown |

---

## Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Top Navigation | College branding + stream context |
| 2 | Sidebar | Module nav — stream filtered for HODs/Lecturers |
| 3 | College KPI Bar | Real-time college-wide stats |
| 4 | Alert Banner | Critical academic + compliance alerts |
| 5 | Stream Performance Cards | MPC / BiPC / CEC / MEC comparison |
| 6 | Board Exam Countdown | Days to IPE / JEE / NEET |
| 7 | Upcoming Exam Schedule | Next 7 days tests |
| 8 | Top Performers | Rank holders, toppers list |
| 9 | Fee & Admission Snapshot | Collection + new admissions |
| 10 | Activity Feed | College-wide events |

---

## Section 3 — College KPI Bar

| Card | Metric | Sub-info |
|---|---|---|
| 1 | Total Students | By stream: MPC (420) BiPC (380) CEC (120) MEC (80) |
| 2 | Attendance Today | Stream-wise averages. ⚠️ if any stream < 75% |
| 3 | Fee Collection | Quarterly fee status. % collected. |
| 4 | Board Exam (IPE) | Days remaining. "67 days to IPE March 2024" |
| 5 | JEE/NEET Prep | % students above target score in mock tests |
| 6 | Hostel Occupancy | Rooms filled / total capacity |

---

## Section 5 — Stream Performance Cards

> 4 cards — one per stream. Visible to Principal, VP, Academic HODs.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Stream Performance Overview                                            │
│                                                                         │
│  ┌────────────────────┐  ┌────────────────────┐                        │
│  │  MPC  (420 students)│  │  BiPC (380 students)│                       │
│  │  Class 11: 210      │  │  Class 11: 195      │                       │
│  │  Class 12: 210      │  │  Class 12: 185      │                       │
│  │                    │  │                    │                        │
│  │  Avg Score:  74.2%  │  │  Avg Score:  71.8%  │                       │
│  │  Attendance: 91.4%  │  │  Attendance: 89.2%  │                       │
│  │  JEE Target: 68% ✅ │  │  NEET Tgt:  72% ✅  │                       │
│  │  [View MPC →]       │  │  [View BiPC →]      │                       │
│  └────────────────────┘  └────────────────────┘                        │
│                                                                         │
│  ┌────────────────────┐  ┌────────────────────┐                        │
│  │  CEC  (120 students)│  │  MEC  (80 students) │                       │
│  │  Avg Score:  78.1%  │  │  Avg Score:  76.4%  │                       │
│  │  Attendance: 93.2%  │  │  Attendance: 94.1%  │                       │
│  │  [View CEC →]       │  │  [View MEC →]       │                       │
│  └────────────────────┘  └────────────────────┘                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Section 6 — Board Exam Countdown

```
┌──────────────────────────────────────────────────────────────────┐
│  Board Exam Countdown                                            │
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  📅 IPE March   │  │  🎯 JEE Mains   │  │  🏥 NEET UG     │ │
│  │  Class 12       │  │  Session 2      │  │                 │ │
│  │                 │  │                 │  │                 │ │
│  │  67 days        │  │  45 days        │  │  89 days        │ │
│  │  Mar 25, 2024   │  │  Apr 4, 2024    │  │  May 5, 2024    │ │
│  │                 │  │                 │  │                 │ │
│  │  MPC + BiPC     │  │  MPC only       │  │  BiPC only      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## Student Home View — College Portal

```
┌──────────────────────────────────────────────────────────────────────┐
│  [College Logo]  Narayana Junior College           [👤 Akhil Kumar] │
│  Class 12 · MPC · Roll: 142 · JEE Aspirant                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────┐  ┌─────────────────────────────────────┐ │
│  │  📅 TODAY              │  │  🎯 BOARD EXAM PREP                 │ │
│  │  ✅ Present            │  │  IPE March 2024: 67 days            │ │
│  │  9AM: Maths            │  │  JEE Mains: 45 days                 │ │
│  │  11AM: Physics         │  │                                     │ │
│  │  2PM: Chemistry        │  │  Target: JEE Advanced Rank <5000    │ │
│  │                        │  │  Current mock rank: 4,231 ↑         │ │
│  └────────────────────────┘  └─────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────┐  ┌─────────────────────────────────────┐ │
│  │  📊 SUBJECT SCORES     │  │  ⚠️ WEAK AREAS                     │ │
│  │  Maths:  87 / 100      │  │  Organic Chemistry — 48%            │ │
│  │  Physics: 76 / 100     │  │  Integration — 52%                  │ │
│  │  Chem:   72 / 100      │  │  [Start Practice →]                 │ │
│  └────────────────────────┘  └─────────────────────────────────────┘ │
│                                                                      │
│  UPCOMING TESTS                          RECENT MARKS               │
│  ┌──────────────────────────────────┐   ┌────────────────────────┐  │
│  │  Tomorrow: Physics Half-Yearly   │   │  Maths SA-2: 87/100    │  │
│  │  22 Mar: Chemistry Practical     │   │  Physics Test: 76/100  │  │
│  │  [View full schedule →]          │   │  [View all marks →]    │  │
│  └──────────────────────────────────┘  └────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## API Calls

| Section | Endpoint |
|---|---|
| KPI Bar | `GET /api/v1/college/home/kpis?stream={stream}` |
| Stream cards | `GET /api/v1/college/streams/summary` |
| Board exam dates | `GET /api/v1/college/board-exams` |
| Upcoming exams | `GET /api/v1/college/exams/upcoming?days=7` |
| Student home data | `GET /api/v1/student/home?stream={stream}` |
