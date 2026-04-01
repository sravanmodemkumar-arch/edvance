# Home Page: Group 10 — Student Unified Portal
**Route:** `/home`
**Domain:** `student.eduforge.in` (unified) OR embedded within institution portals
**Access:** All student types — content adapts per enrollment profile
**Portal type:** Student-first — personal performance, study, tests, fees — across all institutions

---

## Overview

| Property | Value |
|---|---|
| Purpose | Student's single dashboard across all their institutions and exam domains |
| Two modes | 1) Within institution portal (`www.school.com/home` — student role) 2) Unified `student.eduforge.in/home` |
| Key difference | Institution portal = scoped to that institution. Unified portal = all institutions aggregated. |
| Who uses it | Students enrolled in school, coaching, exam domains — alone or in combination |

---

## Student Type → Home View Matrix

| Student Type | Home Shows |
|---|---|
| School-only student | School portal in student view — attendance, marks, schedule, fees |
| Coaching-only student | Coaching portal in student view — batches, mock test ranks, schedule |
| School + Coaching student | Unified dashboard — both institution cards + performance across both |
| Exam domain only (self-reg) | Exam domain home (Group 6 home) |
| School + Coaching + Exam domain | Full unified dashboard — 3 cards |
| Dropper (no institution) | Coaching + exam domain cards only |
| Working professional | Exam domain card only — evening/weekend mode |

---

## Page Sections — Unified Student Dashboard

| # | Section | Purpose |
|---|---|---|
| 1 | Top Navigation | Student portal branding + multi-institution switcher |
| 2 | Greeting + Today | Today's schedule, highlights |
| 3 | Alert Banner | Exam today, fee due, attendance warning |
| 4 | Institution Cards | One card per enrolled institution |
| 5 | Exam Domain Cards | SSC/RRB/etc. subscriptions |
| 6 | Overall Performance | Cross-institution performance trend |
| 7 | Weak Topics | AI-identified weak areas across all subjects |
| 8 | Upcoming Tests | Next 7 days — all institutions combined |
| 9 | Study Material | Notes + videos accessed recently |
| 10 | AI Study Plan | Personalized daily plan (if premium) |

---

## Section 1 — Top Navigation

| Element | Spec |
|---|---|
| Logo | EduForge Student logo (on unified portal) or Institution logo (within institution portal) |
| Name | "My Dashboard" or "[Student Name]'s Dashboard" |
| Institution switcher | Dropdown: "All Institutions ▼" or switch to view individual institution |
| Quick search | Search notes, tests, subjects across all content |
| Notifications | All alerts from all institutions merged — sorted by priority |
| Profile | Avatar, name, class/batch/exam, subscription badge |

---

## Section 2 — Greeting + Today's Highlights

```
┌──────────────────────────────────────────────────────────────────────┐
│  Good morning, Ravi! 👋                                              │
│  Tuesday, 19 March 2024 · 47 days to JEE Mains                     │
│                                                                      │
│  TODAY                                                               │
│  ● 09:00 AM  Maths class (XYZ School)                               │
│  ● 04:00 PM  Physics batch (ABC Coaching)                            │
│  ● ⚠️ Coaching fee due today — ₹8,500 → [Pay Now]                   │
│  ● 📝 JEE Mock #25 LIVE — Tomorrow 10AM  → [Set Reminder]           │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 3 — Alert Banner

| Priority | Alert |
|---|---|
| 🔴 High | "Attendance at ABC Coaching: 68% — minimum is 75%. At risk of de-enrolment." |
| 🔴 High | "Coaching fee overdue: ₹8,500 — [Pay Now]" |
| 🟡 Info | "Physics Half-Yearly exam: Tomorrow 9AM at XYZ School" |
| 🟢 Success | "JEE Mock #23 result published. Your AIR: 4,231 ↑ improved!" |

---

## Section 4 — Institution Cards

```
┌──────────────────────────────────────────────────────────────────────┐
│  MY INSTITUTIONS                                                     │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  🏫 XYZ School, Hyderabad                                      │ │
│  │  Class 12 MPC · Roll No: 42                                    │ │
│  │  ─────────────────────────────────────────────────────────── │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐│ │
│  │  │ 📅 TODAY     │  │ 📊 MARKS     │  │ 💰 FEES              ││ │
│  │  │ ✅ Present   │  │ Last: 87/100 │  │ ✅ Paid              ││ │
│  │  │ 3 classes    │  │ Rank: 12/48  │  │ Next: Apr 10         ││ │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘│ │
│  │  Next exam: Physics Half-Yearly — Tomorrow 9AM                 │ │
│  │  [Open School Portal →]                                        │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  🎓 ABC JEE Coaching, Hyderabad                                │ │
│  │  JEE Advanced Batch A · Morning                                │ │
│  │  ─────────────────────────────────────────────────────────── │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐│ │
│  │  │ 📅 TODAY     │  │ 🏆 RANK      │  │ 💰 FEES              ││ │
│  │  │ ✅ Present   │  │ AIR: 4,231   │  │ ⚠️ ₹8,500 DUE       ││ │
│  │  │ 3 sessions   │  │ ↑ from 6,890 │  │ Due: TODAY           ││ │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘│ │
│  │  Next test: JEE Mock #25 — Tomorrow 10AM                       │ │
│  │  [Pay ₹8,500]  [Open Coaching Portal →]                        │ │
│  └────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 5 — Exam Domain Cards

```
┌──────────────────────────────────────────────────────────────────────┐
│  MY EXAM SUBSCRIPTIONS                                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  📝 EduForge SSC Domain            Premium ✅ · Renews May 1   │ │
│  │  Tests this month: 12 · Best AIR: 1,847 / 2,34,000            │ │
│  │  [Open SSC Portal →]                                           │ │
│  └────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 6 — Overall Performance

```
┌────────────────────────────────────────────────────────────────────┐
│  Overall Performance                            [Detailed View →]  │
│                                                                    │
│  ┌──────────────────────────────┐  ┌────────────────────────────┐ │
│  │  Score Trend (Last 3 Months) │  │  Subject Breakdown         │ │
│  │  100%┤            ●          │  │  Maths   ████████░░  78%   │ │
│  │   80%┤       ●────           │  │  Physics ███████░░░  72%   │ │
│  │   60%┤  ●────                │  │  Chem    ██████░░░░  65%   │ │
│  │      Jan   Feb   Mar         │  │  English █████████░  87%   │ │
│  └──────────────────────────────┘  └────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

---

## Section 7 — Weak Topics (AI-identified)

```
┌──────────────────────────────────────────────────────────────────────┐
│  ⚠️ Areas Needing Attention                     [Practice All →]   │
│                                                                      │
│  From School:                                                        │
│  1.  Organic Chemistry     42%  🔴  [Practice 20 MCQs]             │
│  2.  Integration           55%  🟡  [Practice]                      │
│                                                                      │
│  From Coaching (JEE):                                               │
│  3.  Rotational Motion     48%  🔴  [Practice]                      │
│  4.  Electrochemistry      52%  🟡  [Practice]                      │
│                                                                      │
│  From SSC Domain:                                                    │
│  5.  Reasoning (Non-Verbal) 61%  🟡  [Practice]                    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 8 — Upcoming Tests (All institutions)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Upcoming Tests & Exams                          [Full Calendar →]  │
│                                                                      │
│  TOMORROW                                                            │
│  ● 09:00 AM  Physics Half-Yearly [XYZ School] · Hall 1             │
│  ● 10:00 AM  JEE Mock #25 [ABC Coaching] · Online                  │
│                                                                      │
│  22 MAR                                                              │
│  ● 09:00 AM  Chemistry Practical [XYZ School]                       │
│  ● SSC CGL Mock #26 [SSC Domain] · Online · 2L+ aspirants          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 10 — AI Study Plan

```
┌──────────────────────────────────────────────────────────────────────┐
│  🤖 Your AI Study Plan                                              │
│  Personalized across School + Coaching + Exam domain                │
│  Goal: JEE Mains Rank < 2000  ·  47 days remaining                 │
│  ──────────────────────────────────────────────────────────────     │
│  TODAY — 3 hrs recommended                                          │
│  ● Organic Chemistry (Coaching weak) — 60 min  [Start]             │
│  ● Physics Mock Problems — 45 min             [Start]              │
│  ● JEE Mains 2022 Paper — 90 min              [Start]              │
│  ● Current Affairs — 15 min (SSC domain)      [Start]              │
│                                                                      │
│  [View Full Week Plan]                                               │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Single-Institution Student View (Scoped)

> When student logs into just `www.school.com`, they only see that school's data.
> No unified dashboard. Simple student view within the school portal.
> See [group3-home.md](group3-home.md) — Student Home View section.

---

## API Calls

| Section | Endpoint |
|---|---|
| Student profile + institutions | `GET /api/v1/student/me` |
| Institution cards data | `GET /api/v1/student/institutions/summary` |
| Domain subscriptions | `GET /api/v1/student/domains` |
| Performance data | `GET /api/v1/student/performance/overview` |
| Weak topics | `GET /api/v1/student/analytics/weak-topics` |
| Upcoming tests | `GET /api/v1/student/tests/upcoming?days=7` |
| AI study plan | `GET /api/v1/student/ai-plan/today` |
