# B-03 — Student Management

> **URL:** `/tsp/admin/students/`
> **File:** `b-03-student-management.md`
> **Priority:** P1
> **Roles:** TSP Admin · TSP Manager · EduForge Support

---

## 1. Student List & Search

```
STUDENT MANAGEMENT — TopRank Academy
3,042 total | 2,814 active | 186 expired | 42 suspended

  SEARCH: [Search name, email, phone, student ID...       ]
  FILTER: Exam: [All ▼]  Batch: [All ▼]  Status: [Active ▼]  Plan: [All ▼]

  ┌────────────────────────────────────────────────────────────────────────────────────┐
  │  # │ Student ID │ Name              │ Exam         │ Batch       │ Sub     │Status│
  ├────┼────────────┼───────────────────┼──────────────┼─────────────┼─────────┼──────┤
  │  1 │ TR-10042   │ Priya Mandal      │ APPSC Gr2    │ APPSC-Mar26 │ Premium │ Act  │
  │  2 │ TR-10041   │ Ravi Teja K.      │ SSC CGL      │ SSC-Feb26   │ Standard│ Act  │
  │  3 │ TR-10040   │ Sneha Reddy       │ APPSC Gr2    │ APPSC-Mar26 │ Premium │ Act  │
  │  4 │ TR-10039   │ Mahesh Babu P.    │ Banking IBPS │ BANK-Jan26  │ Standard│ Act  │
  │  5 │ TR-10038   │ Anjali Sharma     │ SSC CHSL     │ SSC-Feb26   │ Basic   │ Act  │
  │  6 │ TR-10037   │ Kiran Kumar D.    │ RRB NTPC     │ RRB-Mar26   │ Standard│ Act  │
  │  7 │ TR-10036   │ Divya Lakshmi     │ APPSC Gr2    │ APPSC-Jan26 │ Premium │ Exp  │
  │  8 │ TR-10035   │ Sunil Varma       │ SSC CGL      │ SSC-Dec25   │ Standard│ Exp  │
  │  … │ …          │ …                 │ …            │ …           │ …       │ …    │
  └────────────────────────────────────────────────────────────────────────────────────┘
  Showing 1–50 of 3,042  [< Prev]  [1] [2] [3] ... [61]  [Next >]

  [+ Add Student]  [Bulk Import CSV]  [Export All]  [Send Bulk Notification]
```

---

## 2. Bulk Import & Batch/Cohort Management

```
BULK STUDENT IMPORT

  Upload CSV:    [ Choose File ]  sample-students.csv (downloaded 340 times)
  ── CSV FORMAT ─────────────────────────────────────────────────────────────
  name, email, phone, exam, batch, plan
  "Rajesh Kumar", "rajesh.k@gmail.com", "+91-98765-10001", "APPSC Gr2", "APPSC-Mar26", "Premium"
  "Swathi N.", "swathi.n@gmail.com", "+91-98765-10002", "SSC CGL", "SSC-Feb26", "Standard"
  … (up to 500 rows per upload)

  IMPORT PREVIEW:
  ┌─────────────────────────────────────────────────────────────────────┐
  │  Total rows:         45                                            │
  │  Valid:              42  (will be created)                         │
  │  Duplicate email:     2  (rajesh.k@gmail.com, swathi.n@gmail.com) │
  │  Invalid phone:       1  (+91-0000-00000 — format error)          │
  └─────────────────────────────────────────────────────────────────────┘
  [Import 42 Students]  [Download Error Report]  [Cancel]

─────────────────────────────────────────────────────────────────────────────

BATCH / COHORT MANAGEMENT

  ┌──────────────────────────────────────────────────────────────────────┐
  │  Batch           │ Exam         │ Students │ Created    │ Status    │
  ├──────────────────┼──────────────┼──────────┼────────────┼───────────┤
  │  APPSC-Mar26     │ APPSC Gr2    │    420   │ 01 Mar 26  │ Active    │
  │  APPSC-Jan26     │ APPSC Gr2    │    380   │ 05 Jan 26  │ Active    │
  │  SSC-Feb26       │ SSC CGL/CHSL │    310   │ 10 Feb 26  │ Active    │
  │  BANK-Jan26      │ Banking IBPS │    280   │ 12 Jan 26  │ Active    │
  │  RRB-Mar26       │ RRB NTPC     │    180   │ 15 Mar 26  │ Active    │
  │  APPSC-Oct25     │ APPSC Gr2    │    360   │ 01 Oct 25  │ Completed │
  │  SSC-Dec25       │ SSC CGL      │    290   │ 05 Dec 25  │ Expired   │
  └──────────────────────────────────────────────────────────────────────┘

  [+ Create Batch]  [Merge Batches]  [Archive Completed]
```

---

## 3. Student Detail & Status Management

```
STUDENT DETAIL — Priya Mandal (TR-10042)
Enrolled: 08 Mar 2026 | Batch: APPSC-Mar26 | Plan: Premium (expires 07 Sep 2026)

  ── PROFILE ──────────────────────────────────────────────────────────────
  Email:     priya.mandal@gmail.com        Phone: +91-90123-XXXXX
  Exam:      APPSC Group 2 (Prelims)       Language: Telugu + English
  City:      Guntur, AP                    Qualification: B.Com

  ── ACTIVITY SUMMARY ─────────────────────────────────────────────────────
  Tests Attempted:     28 / 84 available (33.3%)
  Avg Score:           112.6 / 150 (75.1%)
  Best Score:          142 / 150 (Mock #11 — top 1% in batch)
  Study Hours (MTD):   48.2 hrs
  Last Login:          31 Mar 2026 09:14 AM
  Login Streak:        12 days

  ── SUBSCRIPTION ─────────────────────────────────────────────────────────
  Plan: Premium (Rs.999 / 6 months)
  Start: 08 Mar 2026    Expiry: 07 Sep 2026    Status: Active
  Payment: Razorpay TXN-RP-4028376  |  Rs.999 received 08 Mar 2026
  Auto-renew: ON (card ending 4521)

  ── ACTIONS ──────────────────────────────────────────────────────────────
  [Edit Profile]  [Change Batch]  [Extend Subscription]
  [Suspend Student]  [Send Notification]  [View Full Analytics]
  [Reset Password]  [Download Progress Report]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/tsp/admin/students/` | List students (paginated, filterable) |
| 2 | `POST` | `/api/v1/tsp/admin/students/` | Add single student |
| 3 | `POST` | `/api/v1/tsp/admin/students/bulk-import/` | Bulk import students via CSV |
| 4 | `GET` | `/api/v1/tsp/admin/students/{id}/` | Student detail with activity summary |
| 5 | `PATCH` | `/api/v1/tsp/admin/students/{id}/` | Update student profile, batch, status |
| 6 | `GET` | `/api/v1/tsp/admin/batches/` | List all batches/cohorts |
| 7 | `POST` | `/api/v1/tsp/admin/batches/` | Create new batch |
| 8 | `PATCH` | `/api/v1/tsp/admin/batches/{id}/` | Update batch details or merge batches |

---

## 5. Business Rules

- Student IDs are auto-generated with the TSP prefix (TR- for TopRank) followed by a sequential number; this prefix is configurable during onboarding (A-02) and cannot be changed after the first student is enrolled because it appears on progress reports, certificates, and payment receipts; the ID is unique within the TSP but not globally — another TSP could have their own TR-10042; global uniqueness is ensured by the internal UUID, while the display ID (TR-10042) is a human-friendly identifier that coaching centres use in their offline records, attendance sheets, and parent communications
- Bulk import is capped at 500 rows per upload to prevent timeout and memory issues; a typical Vijayawada coaching centre like TopRank Academy enrolls students in batches of 30–100 at the start of a new coaching cycle (e.g., March batch for APPSC aspirants); the 500-row limit accommodates even the largest single-batch enrollment; for TSPs with 10,000+ students migrating from another platform, EduForge provides a dedicated migration API with async processing and progress tracking, handled by the EduForge onboarding team rather than self-service CSV upload
- Batch/cohort assignment determines which mock test schedule, study plan, and leaderboard a student sees; a student in the APPSC-Mar26 batch sees APPSC-specific mocks released on the March schedule, competes on the APPSC-Mar26 leaderboard (not the entire TopRank leaderboard), and follows the APPSC Prelims study plan; changing a student's batch mid-cycle (e.g., moving from SSC to APPSC because they changed their exam target) resets their leaderboard position but preserves all historical test attempts and analytics; the TSP Admin can move students between batches freely
- Student suspension is a reversible action used when a student violates platform rules (sharing credentials, screenshot distribution of premium content) or when payment disputes arise; a suspended student cannot log in but their data and test history are fully preserved; suspension is preferred over deletion because Indian consumer protection regulations require retaining transaction records for the subscription period; the TSP Admin must provide a suspension reason (logged in audit trail); the student receives an email notification with the reason and a support contact; reactivation restores full access with all historical data intact

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division B*
