# Home Page: Group 3 — School Portal
**Route:** `/home`
**Domain:** `www.school.com` (custom) or `[slug].eduforge.in`
**Access:** All roles inside the school — content changes completely per role
**Portal type:** School management + teaching + student + parent access

---

## Overview

| Property | Value |
|---|---|
| Purpose | Everything a school needs — one portal, role-aware views |
| Domain | School's own domain (e.g., `www.xyzschool.ac.in`) or EduForge subdomain |
| Branding | School logo, school colors, school name — set by School Admin |
| Who uses it | Principal, Vice Principal, HOD, Class Teacher, Subject Teacher, Librarian, Accountant, Front Desk, Transport, Hostel, Student, Parent |
| Key rule | SAME URL. Same portal. Different role = completely different home. |

---

## Role-Based Home View Matrix

| Role | Home Shows |
|---|---|
| Principal | Full school dashboard — all sections, all KPIs, all alerts |
| Vice Principal | Academic + discipline. No fee, no staff payroll. |
| HOD (Head of Dept) | Their department — teachers in dept, subject performance, exam schedule |
| Class Teacher | Their class ONLY — attendance, marks, parent messages, today's schedule |
| Subject Teacher | Their subjects — upcoming tests, student performance per subject, MCQ bank |
| Librarian | Library dashboard — books issued, due returns, fines |
| Accountant | Fee collection dashboard — defaults, receipts, Razorpay |
| Front Desk / Admin | Daily visitors, calls, new admissions, announcements |
| Transport Manager | Bus routes, today's attendance by bus, vehicle status |
| Hostel Warden | Occupancy, meal tracking, leave requests, welfare alerts |
| Student | Personal dashboard — attendance, marks, upcoming tests, fee status |
| Parent | Their child/children summary within this school |

---

## Page Sections — Principal View (Full View)

| # | Section | Purpose |
|---|---|---|
| 1 | Top Navigation | School branding + global search + notifications |
| 2 | Sidebar | Full school module navigation |
| 3 | Today's Pulse (KPI Bar) | Real-time school stats for today |
| 4 | Alert Banner | Critical issues needing action |
| 5 | Quick Actions | Principal's most-used shortcuts |
| 6 | Class-wise Attendance Grid | Today's attendance per class at a glance |
| 7 | Fee Collection Snapshot | Today's collections + defaulters |
| 8 | Upcoming Exams | Next 7 days exam schedule |
| 9 | Recent Activity | School-wide event feed |
| 10 | Staff On Duty | Who's present, who's absent today |

---

## Section 1 — Top Navigation

→ Component: [06-navigation.md](../components/06-navigation.md)

| Element | Spec |
|---|---|
| School logo | School's uploaded logo — 40px height. Fallback: school initials colored circle |
| School name | "[School Name]" — full name on desktop, short name on mobile |
| Academic year | "2024–25" badge next to school name |
| Quick search | Search students by name, roll no, mobile |
| Notifications bell | Unread count. School-specific: attendance alerts, fee reminders, exam results |
| Profile dropdown | Shows user's name, role, class (if teacher). Links: Profile, Settings, Logout |

---

## Section 2 — Sidebar Navigation

| Nav Item | Who Sees It | Notes |
|---|---|---|
| 🏠 Dashboard | All | |
| 🎓 Students | Admin / Teachers / Accountant | Teacher: their class only |
| 👨‍🏫 Staff | Principal / VP / Admin | |
| 📚 Classes | Principal / VP / Teachers | Teacher: assigned classes only |
| ✅ Attendance | Teachers / Principal | Class teachers mark their class |
| 📝 Examinations | Teachers / Principal / VP | Subject teacher sees their exams |
| 💰 Fees | Accountant / Principal / Admin | |
| 📋 Content | Teachers (L2+) | Notes, videos, MCQ |
| 📅 Timetable | All (view) / Admin (edit) | |
| 📢 Notifications | Principal / Admin / Teachers | |
| 📊 Reports | Principal / VP / Admin | |
| 🏨 Hostel | Warden / Principal | Feature flag: only if hostel enabled |
| 🚌 Transport | Transport Mgr / Principal | Feature flag: only if transport enabled |
| 📚 Library | Librarian / Principal | Feature flag: only if library enabled |
| ⚙️ Settings | Principal / School Admin | |

---

## Section 3 — Today's Pulse (KPI Bar)

→ Component: [07-data-display.md](../components/07-data-display.md) — Stat Card

> Real-time. Auto-refreshes every 5 minutes during school hours.

| Card | Metric | Sub-info |
|---|---|---|
| 1 | Attendance Today | "94.2% — 1,183 / 1,254 present" — progress bar, color-coded |
| 2 | Fee Collection MTD | "₹12.4L / ₹14.2L target" — progress bar |
| 3 | Exams Today | "3 exams — 8AM, 10AM, 2PM" — badge count |
| 4 | Absent Staff | "2 staff absent — substitutes assigned?" — ⚠️ if not covered |
| 5 | New Admissions | "4 today / 47 this month" |
| 6 | Fee Defaulters | "34 students — ₹3.2L outstanding" |

> Class Teacher sees only: Attendance for their class, today's exams for their class, fee status for their class.
> Student sees only: Own attendance %, own upcoming exams, own fee status.

---

## Section 4 — Alert Banner

→ Component: [03-alerts-toasts.md](../components/03-alerts-toasts.md)

| Priority | Alert (Principal) | Alert (Class Teacher) |
|---|---|---|
| 🔴 Critical | "5 staff have no BGV — POCSO compliance risk" | "3 students absent for 5+ consecutive days" |
| 🟠 Warning | "Class 11 fee collection at 42% — 34 defaulters" | "Parent meeting request from Ravi Kumar's father" |
| 🟡 Info | "Annual Day event added to calendar: March 28" | "Exam schedule updated for next week" |

---

## Section 5 — Quick Actions (Role-Based)

| Role | Quick Actions |
|---|---|
| Principal | [📊 Today's Report] [📢 Send Circular] [✅ Approve TC] [💰 Fee Overview] |
| Class Teacher | [✅ Mark Attendance] [📝 Enter Marks] [💬 Message Parent] [📅 My Schedule] |
| Subject Teacher | [📝 Create Exam] [✏️ Upload MCQs] [📊 Class Performance] |
| Accountant | [💰 Collect Fee] [📄 Generate Receipt] [⚠️ Defaulters (34)] |
| Hostel Warden | [🏨 Room Status] [🍽 Meal Count] [📋 Leave Requests] |
| Transport Mgr | [🚌 Route Status] [✅ Bus Attendance] [⚠️ Vehicle Issues] |
| Student | [📅 Today's Schedule] [📊 My Performance] [💰 Pay Fees] |

---

## Section 6 — Class-wise Attendance Grid

> Principal / VP / Admin view only.
> All classes shown in a grid. Color shows attendance health.

```
┌──────────────────────────────────────────────────────────────────────┐
│  Today's Attendance by Class             [Date: Tue, 19 Mar 2024]   │
│                                                                      │
│  ┌──────────┬─────────┬────────────┬────────────┬────────────┐      │
│  │ Class    │ Teacher │ Total      │ Present    │ Status     │      │
│  ├──────────┼─────────┼────────────┼────────────┼────────────┤      │
│  │ Class 6A │ Ravi K  │ 42         │ 40 (95%)   │ 🟢 Good   │      │
│  │ Class 6B │ Priya S │ 40         │ 38 (95%)   │ 🟢 Good   │      │
│  │ Class 9A │ Ramesh  │ 45         │ 32 (71%)   │ 🔴 Low    │      │
│  │ Class 9B │ Sunita  │ 43         │ —          │ ⏳ Pending │      │
│  │ Class 12A│ Kumar   │ 48         │ 46 (96%)   │ 🟢 Good   │      │
│  │ Class 12B│ Meena   │ 47         │ 44 (94%)   │ 🟢 Good   │      │
│  └──────────┴─────────┴────────────┴────────────┴────────────┘      │
│                                                                      │
│  ⏳ 3 classes pending attendance entry    [Send Reminder to Teachers]│
└──────────────────────────────────────────────────────────────────────┘
```

| Status | Color | Condition |
|---|---|---|
| 🟢 Good | Green | ≥ 85% present |
| 🟡 Average | Yellow | 70–84% |
| 🔴 Low | Red | < 70% |
| ⏳ Pending | Gray | Teacher hasn't marked yet |

> Click any row → opens that class's attendance details
> [Send Reminder] → WhatsApp message to teachers with pending attendance

---

## Section 7 — Fee Collection Snapshot

> Accountant / Principal view.

```
┌──────────────────────────────────────────────────────────────────┐
│  Fee Collection — March 2024                [View Full Report →] │
│                                                                  │
│  Collected:  ₹12,47,500                                          │
│  Target:     ₹15,60,000   ████████████████░░░░  79.9%           │
│                                                                  │
│  Today's collections:  ₹34,500 (12 students)                    │
│  Defaulters:           34 students — ₹3,12,000 outstanding      │
│                                                                  │
│  By Class:                                                       │
│  Class 12  ████████████░░  88%    Class 9  ████████░░░░  67%    │
│  Class 11  █████████████░  91%    Class 8  ████████░░░░  71%    │
│                                                                  │
│  [Collect Fee]    [View Defaulters]    [Send Reminders]         │
└──────────────────────────────────────────────────────────────────┘
```

---

## Section 8 — Upcoming Exams

```
┌──────────────────────────────────────────────────────────────────┐
│  Upcoming Exams — Next 7 Days                [View Calendar →]  │
│                                                                  │
│  Today, 19 Mar                                                   │
│  ●  10:00 AM  Mathematics Unit Test    Class 11 MPC   Hall 1    │
│  ●  02:00 PM  English FA-3             Class 9 A & B  Hall 2    │
│                                                                  │
│  Tomorrow, 20 Mar                                                │
│  ●  09:00 AM  Physics Half-Yearly      Class 12 MPC   Hall 1    │
│  ●  09:00 AM  Social Studies FA-3      Class 8 A-D    Hall 3    │
│                                                                  │
│  22 Mar                                                          │
│  ●  09:00 AM  Chemistry Practical      Class 12 BiPC  Lab       │
│                                                                  │
│  [+ Schedule Exam]                                               │
└──────────────────────────────────────────────────────────────────┘
```

> Class Teacher sees: Only exams for their class
> Subject Teacher sees: Only their subject exams
> Student sees: Only exams they're supposed to take

---

## Section 9 — Recent Activity

```
┌──────────────────────────────────────────────────────────────────┐
│  School Activity                                       [All ▼]  │
│  ────────────────────────────────────────────────────────────── │
│  ✅  5 min ago   · Attendance marked: Class 9A — Ramesh Kumar   │
│  💰  12 min ago  · Fee received: Ravi Teja (Class 12A) ₹12,500 │
│  📝  1 hr ago    · Test results published: Maths Class 11       │
│  👤  2 hrs ago   · New student enrolled: Priya Kumari, 7th      │
│  📢  Yesterday   · Circular sent: Annual Day — 28 March         │
└──────────────────────────────────────────────────────────────────┘
```

---

## Section 10 — Staff On Duty

> Principal / VP view. Today's date.

```
┌───────────────────────────────────────────────────┐
│  Staff Today (47 present / 52 total)    [Manage] │
│                                                   │
│  ✅ Present (47)   ❌ Absent (3)  🏥 Leave (2)  │
│                                                   │
│  Absent:                                          │
│  ● Ravi Kumar (Class 11 Physics) — no substitute  │
│  ● Meena Devi (Class 8 English)  — substitute: OK │
│  ● Suresh M   (Library)          — leave approved │
└───────────────────────────────────────────────────┘
```

---

## Student Home View (Same Portal, Student Role)

> When a student logs into `www.xyzschool.com`, they see a PERSONAL dashboard — not the admin view.

```
┌──────────────────────────────────────────────────────────────────────┐
│  [School Logo]  XYZ School                          [👤 Ravi Kumar] │
├──────────────────────────────────────────────────────────────────────┤
│  Good morning, Ravi! 👋                                              │
│  Class 12 MPC · Roll No: 42 · Today: Tuesday, 19 March 2024         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────┐  ┌────────────────────┐  ┌───────────────┐  │
│  │  📅 TODAY           │  │  📊 PERFORMANCE     │  │  💰 FEES      │  │
│  │                    │  │                    │  │               │  │
│  │  ✅ Present         │  │  Overall: 78.4%    │  │  ✅ Paid      │  │
│  │  9:00 Maths        │  │  Rank: 12 / 48     │  │  Next due:    │  │
│  │  11:00 Physics     │  │  ↑ from last month │  │  April 10     │  │
│  │  2:00 Chemistry    │  │  Weak: Org Chem ⚠️ │  │  ₹12,500      │  │
│  └────────────────────┘  └────────────────────┘  └───────────────┘  │
│                                                                      │
│  UPCOMING TESTS                          RECENT MARKS               │
│  ┌──────────────────────────────────┐   ┌────────────────────────┐  │
│  │ Tomorrow 9AM: Physics Half-Yearly│   │ Maths Unit Test: 87/100│  │
│  │ 22 Mar: Chemistry Practical      │   │ English FA-3: 36/40    │  │
│  │ 25 Mar: English FA-4             │   │ Physics Test: 72/100   │  │
│  └──────────────────────────────────┘   └────────────────────────┘  │
│                                                                      │
│  NOTES & STUDY MATERIAL                                              │
│  📋 Organic Chemistry Notes — added by Chem teacher (3 days ago)   │
│  🎬 Integration — YouTube video added by Maths teacher              │
└──────────────────────────────────────────────────────────────────────┘
```

---

## API Calls

| Section | Endpoint | Scope |
|---|---|---|
| KPI Bar | `GET /api/v1/school/home/kpis` | Role-filtered response |
| Attendance grid | `GET /api/v1/school/attendance/today` | Principal: all. Teacher: their class. |
| Fee snapshot | `GET /api/v1/school/fees/snapshot` | Accountant + Principal only |
| Upcoming exams | `GET /api/v1/school/exams/upcoming?days=7` | Role-filtered |
| Activity feed | `WS /ws/school/activity` | Real-time |
| Student home data | `GET /api/v1/student/home` | Own data only |
