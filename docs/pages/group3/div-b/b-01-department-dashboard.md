# B-01 — Department Dashboard

> **URL:** `/school/academic/dept/<dept>/`
> **File:** `b-01-department-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** HOD (S4) — full own dept · VP Academic (S5) — read all depts · Principal (S6) — full all depts

---

## 1. Purpose

The HOD's command centre for their academic department. Provides a single-screen view of department health: how many teachers are present today, how much of the syllabus has been covered, which lesson plans are pending review, which students are at risk in the department's subjects, and whether the department is on track for the upcoming exam. In an Indian school, the HOD is accountable to the Principal for their department's CBSE/board results — this dashboard is where that accountability is made visible every day.

**Department scope:** Science, Mathematics, Social Studies, Languages (English/Hindi/Telugu/etc.), Computer Science, Commerce, Vocational. Each HOD sees only their own department unless they have VP-level access.

---

## 2. Page Layout

### 2.1 Header
```
[Dept Icon] Science Department                    [Switch Dept ▼]  [Export Report]
HOD: Dr. Priya Venkataraman  |  Academic Year: 2025–26  |  Term: Term 2
Staff: 8 teachers  ·  Subjects: 6  ·  Classes: LKG–XII (science sections)
```

**[Switch Dept ▼]** — visible to Principal and VP Academic only; HOD cannot switch.

---

## 3. KPI Strip

Auto-refreshes every 5 minutes via HTMX polling.

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Staff Present   │ Syllabus Cover  │ Lesson Plans    │ Pending QP      │ Avg Score       │ At-Risk Students│
│ Today           │ (This Term)     │ Pending Review  │ Approvals       │ (Last Exam)     │ (< 35%)         │
│                 │                 │                 │                 │                 │                 │
│   6 / 8         │   67.4%         │      4          │      2          │   72.3%         │      14         │
│  🟡 2 Absent    │  ▓▓▓▓▓▓░░░░     │  ⚠️ 2 Overdue   │  🔴 Urgent      │  ↑ 1.8%         │  ↓ 2 from last  │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

| Card | Value | Colour Logic |
|---|---|---|
| Staff Present | X / Total today | Green ≥90%; Yellow 75–89%; Red <75% |
| Syllabus Cover | % of planned topics done for term | Green ≥80%; Yellow 60–79%; Red <60% |
| Lesson Plans Pending | Count awaiting HOD review | Green 0; Yellow 1–3; Red ≥4 |
| Pending QP Approvals | Question papers awaiting HOD sign-off | Green 0; Red any pending (exam approaching) |
| Avg Score | Dept avg in last completed exam | Trend arrow vs previous exam |
| At-Risk Students | Students < 35% in any dept subject | Red if any; Green 0 |

Click any KPI card → deep-links to relevant management page (e.g., Syllabus → B-03, Lesson Plans → B-02).

---

## 4. Main Sections

### 4.1 Today's Teaching Schedule

```
Period | Subject        | Class  | Teacher           | Room   | Status
-------|----------------|--------|-------------------|--------|--------
P1     | Physics        | XII-A  | Ms. Lakshmi       | Lab 1  | ✅ In session
P2     | Chemistry      | XI-B   | Mr. Ravi          | 203    | ✅ In session
P3     | Biology        | X-A    | Ms. Anjali        | 301    | ⚠️ Teacher absent
P4     | Physics        | XI-A   | Ms. Lakshmi       | 204    | ⏳ Upcoming
P5     | Chemistry Lab  | XII-B  | Mr. Ravi          | Lab 2  | ⏳ Upcoming
```

- Absent teacher periods shown in amber — substitute required alert
- [Arrange Substitute] button appears on absent teacher rows → links to B-08 (Substitution Manager)
- Live status from timetable + attendance integration

---

### 4.2 Syllabus Completion — Subject-wise

Progress bars for each subject in the department for the current term:

| Subject | Class Level | Topics Done | Total Topics | % | Target | Gap |
|---|---|---|---|---|---|---|
| Physics | XI | 18 | 28 | 64.3% | 70% | ⚠️ –5.7% |
| Chemistry | XI | 22 | 28 | 78.6% | 70% | ✅ +8.6% |
| Physics | XII | 14 | 26 | 53.8% | 65% | 🔴 –11.2% |
| Biology | XI | 20 | 30 | 66.7% | 70% | ⚠️ –3.3% |
| Chemistry | XII | 19 | 28 | 67.9% | 65% | ✅ +2.9% |
| Biology | XII | 16 | 30 | 53.3% | 65% | 🔴 –11.7% |

Click any row → opens B-03 (Syllabus Tracker) pre-filtered to that subject+class.

---

### 4.3 Lesson Plan Queue

Last 5 submitted lesson plans awaiting HOD review:

| Teacher | Subject | Class | Week | Submitted | Status | Action |
|---|---|---|---|---|---|---|
| Ms. Anjali | Biology | XI-A | Week 12 | 2 days ago | 🟡 Pending | [Review] |
| Mr. Ravi | Chemistry | XII-B | Week 12 | 3 days ago | 🟡 Pending | [Review] |
| Ms. Lakshmi | Physics | XII-A | Week 12 | 4 days ago | 🔴 Overdue | [Review] |
| Ms. Anjali | Biology | X-A | Week 11 | 5 days ago | 🟡 Pending | [Review] |

[View All (4 Pending)] → B-02 (Lesson Plan Review)

**Review** button opens `lesson-plan-review` drawer (680px) inline.

---

### 4.4 Teacher Performance Summary

| Teacher | Periods Taken | Syllabus % | Avg LP Score | Absent Days (Month) | Last Observation |
|---|---|---|---|---|---|
| Ms. Lakshmi Devi | 48/52 | 68.4% | 4.2/5 | 1 | 15 Mar |
| Mr. Ravi Kumar | 50/52 | 74.1% | 4.5/5 | 0 | 20 Mar |
| Ms. Anjali Singh | 44/52 | 62.3% | 3.8/5 | 3 | 8 Mar |
| Dr. Suresh P | 51/52 | 77.2% | 4.7/5 | 0 | 22 Mar |

- Click teacher name → staff profile (A-16) pre-filtered
- [Add Observation Note] per teacher → logs to teacher performance history
- Lesson plan score = HOD-rated score on submitted lesson plans

---

### 4.5 Department Result Snapshot (Last Exam)

| Class | Subject | Appeared | Pass | Pass % | Avg | A+ | Below 35 |
|---|---|---|---|---|---|---|---|
| XII-A | Physics | 38 | 38 | 100% | 81.4% | 11 | 0 |
| XII-B | Chemistry | 22 | 21 | 95.5% | 74.8% | 5 | 1 |
| XI-A | Physics | 40 | 37 | 92.5% | 68.2% | 3 | 2 |
| XI-A | Biology | 40 | 38 | 95.0% | 71.3% | 4 | 1 |

[Full Analytics →] → B-05 (Department Performance Analytics)

---

### 4.6 Upcoming Events (Dept)

| Date | Event | Type | Notes |
|---|---|---|---|
| 28 Mar | Chemistry Unit Test 2 | Exam | QP submission pending |
| 2 Apr | Physics Practical XII | Practical | Lab booked (confirm needed) |
| 5 Apr | Science Exhibition | Competition | 6 student entries registered |
| 10 Apr | Half-Yearly Exam Begins | Board Exam | Seating plan in review |

---

### 4.7 Quick Actions Panel

```
[📋 Review Lesson Plans (4)]   [📝 Approve Question Paper (2)]
[📊 View Dept Analytics]        [📅 Syllabus Tracker]
[👥 Teacher Performance]        [🏆 Competitions Register]
```

---

## 5. HOD Observation Log (Section)

**Record classroom observation** (HOD visits a teacher's class and observes):

| Date | Teacher Observed | Class | Subject | Observer | Score (1–5) | Follow-up |
|---|---|---|---|---|---|---|
| 22 Mar | Dr. Suresh P | XI-B | Physics | HOD | 4.7/5 | None |
| 15 Mar | Ms. Lakshmi | XII-A | Physics | HOD | 4.2/5 | LP quality feedback shared |
| 8 Mar | Ms. Anjali | XI-A | Biology | HOD | 3.8/5 | Improvement plan issued |

[+ Add Observation] → drawer (400px):
- Date, Teacher (dept filtered), Class, Subject, Observation Type (Routine/Formal/Surprise)
- Rating (1–5 on 4 parameters: Content delivery, Classroom management, Student engagement, Time management)
- Summary notes
- Follow-up action (None/Feedback shared/Improvement plan/Escalate to VP)

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/dashboard/` | Full dashboard data |
| 2 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/kpi/` | KPI strip (auto-refresh) |
| 3 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/schedule/today/` | Today's teaching schedule |
| 4 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/syllabus-summary/` | Subject-wise syllabus % |
| 5 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/lesson-plans/pending/` | Pending LP queue |
| 6 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/teacher-performance/` | Teacher performance table |
| 7 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/results/last-exam/` | Last exam result snapshot |
| 8 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/upcoming-events/` | Upcoming events |
| 9 | `POST` | `/api/v1/school/{id}/dept/{dept_id}/observations/` | Add observation note |
| 10 | `GET` | `/api/v1/school/{id}/dept/{dept_id}/observations/` | Observation log |

---

## 7. Business Rules

- HOD can only view their own department; dept param in URL is validated against HOD's assignment
- VP Academic and Principal can view all departments and switch between them
- KPI strip data is cached for 5 minutes; manual [Refresh] forces a cache bust
- Lesson plans submitted > 5 days ago without HOD review are flagged as "Overdue" (amber → red after 7 days)
- Syllabus target % is computed from the academic calendar: (days elapsed ÷ total working days) × 100 with a 10-day lead
- Teacher performance data (absent days, syllabus %, lesson plan scores) is read-only on this page; managed in dedicated pages
- Observation records are editable within 24 hours of creation; after that they are locked
- At-risk students (< 35%) trigger an automatic notification to class teacher and counsellor when result is first published

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
