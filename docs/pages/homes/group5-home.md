# Home Page: Group 5 — Coaching Centre Portal
**Route:** `/home`
**Domain:** `www.coaching.com` (custom) or `[slug].eduforge.in/coaching`
**Access:** All roles — completely different view per role
**Portal type:** Coaching centre — batch management, mock tests, AIR rankings, dropper management

---

## Overview

| Property | Value |
|---|---|
| Purpose | Coaching-specific operations — batches, mock test AIR ranks, JEE/NEET/SSC prep analytics |
| Key difference from School | No classes/streams — BATCHES. Revenue-focused. Mock test national ranks (AIR). Dropper management. |
| Domain | Coaching's own domain (e.g., `www.abcjeecoaching.com`) |
| Roles | Director, Academic Head, Batch Manager, Faculty, Counsellor, Accountant, Student, Hostel Warden |

---

## Role-Based Home View Matrix

| Role | Home Shows |
|---|---|
| Director / Owner | Revenue dashboard — fee collection, batch enrollment, AIR toppers, retention rate |
| Academic Head | Academic performance — batch-wise scores, weak topics, exam calendar |
| Batch Manager | Their assigned batches — attendance, schedule, student progress |
| Faculty | Their subject — uploaded questions, student scores in their subject, upcoming tests |
| Counsellor | At-risk students — dropout signals, parent communication queue |
| Accountant | Fee collection — batch-wise, defaulters, Razorpay settlements |
| Student (Minor) | Personal batch dashboard — AIR rank, weak topics, schedule, parent messages |
| Student (Adult/Dropper) | Full self-access — AI study plan, unlimited tests, all analytics |

---

## Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Top Navigation | Coaching branding + exam-type badge |
| 2 | Sidebar | Coaching modules — batch-centric nav |
| 3 | Coaching KPI Bar | Revenue + academic metrics |
| 4 | Alert Banner | Batch issues, dropout risks, fee alerts |
| 5 | Batch Cards Grid | All batches — enrollment, attendance, performance |
| 6 | AIR Rank Leaderboard | Top 10 students by national rank |
| 7 | Upcoming Mock Tests | Test schedule next 7 days |
| 8 | Counsellor Queue | At-risk students needing intervention |
| 9 | Fee Snapshot | Collection by batch |
| 10 | Activity Feed | Coaching-wide events |

---

## Section 3 — Coaching KPI Bar

| Card | Metric | Sub-info |
|---|---|---|
| 1 | Total Students | By exam type: JEE (1,200) NEET (800) Foundation (400) |
| 2 | Revenue MTD | ₹ collected vs target. Trend. |
| 3 | Active Batches | "24 batches running. 3 starting next week." |
| 4 | Avg AIR (Top 100) | Average rank of top 100 students in mock tests |
| 5 | Dropout Risk | "12 students flagged — login gap + score drop" |
| 6 | BGV Status | "3 faculty pending BGV — POCSO risk" |

---

## Section 5 — Batch Cards Grid

```
┌──────────────────────────────────────────────────────────────────────┐
│  All Batches  (24 active)     [Search batches...]    [+ New Batch]  │
│  Filter: [All ▼] [JEE ▼] [NEET ▼] [Foundation ▼]                   │
│                                                                      │
│  ┌────────────────────────┐  ┌────────────────────────┐             │
│  │  JEE Advanced 2024     │  │  NEET 2024 Batch A     │             │
│  │  Batch A · Morning     │  │  Evening · 5-8 PM      │             │
│  │                        │  │                        │             │
│  │  Students:    124      │  │  Students:    98        │             │
│  │  Attendance:  88% ████░│  │  Attendance:  91% ████░│             │
│  │  Avg AIR:     4,231    │  │  Avg NEET:    512/720  │             │
│  │  Topper AIR:  847      │  │  Top Score:   627/720  │             │
│  │                        │  │                        │             │
│  │  Batch Mgr: Ravi K.    │  │  Batch Mgr: Priya S.   │             │
│  │  Next test: Sun 10AM   │  │  Next test: Sat 9AM    │             │
│  │  [Open Batch →]        │  │  [Open Batch →]        │             │
│  └────────────────────────┘  └────────────────────────┘             │
│                                                                      │
│  ┌────────────────────────┐  ┌────────────────────────┐             │
│  │  Foundation 9-10       │  │  Dropper — JEE 2024    │             │
│  │  ⚠️ Attendance: 67%   │  │  Residential Batch     │             │
│  │  [Open Batch →]        │  │  [Open Batch →]        │             │
│  └────────────────────────┘  └────────────────────────┘             │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 6 — AIR Rank Leaderboard

> Visible to Director, Academic Head, all Faculty.

```
┌──────────────────────────────────────────────────────────────────┐
│  🏆 AIR Leaderboard — JEE Mock #14       [View Full →]          │
│  Last updated: Yesterday 6:42 PM                                 │
│  ─────────────────────────────────────────────────────────────  │
│  #1  [Photo] Akhil Kumar   JEE-A Batch   AIR: 247   ↑ 180       │
│  #2  [Photo] Priya Reddy   JEE-A Batch   AIR: 412   ↑ 93        │
│  #3  [Photo] Rahul Singh   Dropper-JEE   AIR: 589   ↓ 42        │
│  #4  [Photo] Divya Nair    JEE-A Batch   AIR: 847   ↑ 210       │
│  #5  [Photo] Karthik M.    JEE-B Batch   AIR: 1,023 ↑ 347       │
│  ...                                                             │
└──────────────────────────────────────────────────────────────────┘
```

---

## Section 7 — Counsellor Queue (Counsellors only)

```
┌──────────────────────────────────────────────────────────────────┐
│  ⚠️  At-Risk Students (12)              [View All Students →]   │
│                                                                  │
│  HIGH RISK (4 students)                                          │
│  ● Ravi Kumar — JEE-A — No login 14 days. Score dropped 30%.   │
│    Parent: Not contacted. [Call Parent] [Message]                │
│  ● Preethi S — NEET-A — Attendance 42%. Fee defaulter.          │
│    [Schedule Counselling] [Message]                              │
│                                                                  │
│  MEDIUM RISK (8 students)                                        │
│  ● [Show 8 students...]                                          │
└──────────────────────────────────────────────────────────────────┘
```

---

## Student Home View — Coaching Portal

```
┌──────────────────────────────────────────────────────────────────────┐
│  [Coaching Logo]  ABC JEE Coaching              [👤 Akhil Kumar]    │
│  JEE Advanced Batch A · Enrolled: June 2023                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────┐  ┌────────────────────────────────────┐ │
│  │  🎯 MY RANK             │  │  📅 TODAY                          │ │
│  │  Latest AIR: 4,231      │  │  ✅ Present (Batch A)              │ │
│  │  ↑ Improved from 6,890  │  │  9AM–11AM: Mathematics             │ │
│  │  Best ever: 3,847       │  │  11AM–1PM: Physics                 │ │
│  │  Target: < 2,000        │  │  2PM–4PM: Chemistry                │ │
│  └─────────────────────────┘  └────────────────────────────────────┘ │
│                                                                      │
│  ┌─────────────────────────┐  ┌────────────────────────────────────┐ │
│  │  📊 SUBJECT ANALYSIS    │  │  ⚠️ WEAK TOPICS                   │ │
│  │  Maths:   78% ████░     │  │  1. Organic Chemistry — 42%        │ │
│  │  Physics: 72% ███░░     │  │  2. Rotational Motion — 48%        │ │
│  │  Chem:    68% ███░░     │  │  3. Integration — 55%              │ │
│  │  Overall: 73% ████░     │  │  [Practice Now →]                  │ │
│  └─────────────────────────┘  └────────────────────────────────────┘ │
│                                                                      │
│  NEXT MOCK TEST                          AI STUDY PLAN              │
│  Sunday 10AM — JEE Mock #15             [View Your Plan →]          │
│  [View Syllabus]  [Remind Me]           2 hours recommended today   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## API Calls

| Section | Endpoint |
|---|---|
| KPI Bar | `GET /api/v1/coaching/home/kpis` |
| Batch cards | `GET /api/v1/coaching/batches?status=active` |
| AIR leaderboard | `GET /api/v1/coaching/rankings/top?exam_type=jee&limit=10` |
| At-risk students | `GET /api/v1/coaching/counselling/at-risk` |
| Student home | `GET /api/v1/student/coaching/home` |
