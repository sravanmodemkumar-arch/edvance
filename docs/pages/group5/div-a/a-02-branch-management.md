# A-02 — Branch Management

> **URL:** `/coaching/admin/branches/`
> **File:** `a-02-branch-management.md`
> **Priority:** P1
> **Roles:** Director/Owner (K7) · Operations Director (K6) · Branch Manager (K6)

---

## 1. Branch List Overview

```
BRANCH MANAGEMENT — TOPPERS COACHING CENTRE
As of 30 March 2026

  ┌────┬─────────────────────┬──────────┬─────────┬────────┬──────────────┬──────────┐
  │ #  │ Branch Name         │ Students │ Faculty │ Rooms  │ Monthly Rev  │ Status   │
  ├────┼─────────────────────┼──────────┼─────────┼────────┼──────────────┼──────────┤
  │ 1  │ Main (Himayatnagar) │    820   │   18    │   12   │  ₹22.4L      │ Active   │
  │ 2  │ Dilsukhnagar        │    480   │   11    │    8   │  ₹13.1L      │ Active   │
  │ 3  │ Kukatpally          │    360   │    8    │    6   │  ₹9.2L       │ Active   │
  │ 4  │ Online (TCC Live)   │    180   │    3    │   —    │  ₹3.5L       │ Active   │
  └────┴─────────────────────┴──────────┴─────────┴────────┴──────────────┴──────────┘

  [+ Add New Branch]                                      Total Students: 1,840
```

---

## 2. Branch Detail — Main (Himayatnagar)

```
BRANCH DETAIL: TCC MAIN — Himayatnagar, Hyderabad
Branch Manager: Ms. Priya Sharma  |  Est. 2018  |  Capacity: 900 students

BATCH BREAKDOWN:
  ┌──────────────────────────────┬──────────┬──────────┬────────────┬────────────┐
  │ Batch Name                   │ Students │ Capacity │ Attendance │ Avg Score  │
  ├──────────────────────────────┼──────────┼──────────┼────────────┼────────────┤
  │ SSC CGL Morning              │   240    │   250    │  85.2%     │ 162/200    │
  │ SSC CHSL Evening             │   180    │   200    │  80.1%     │ 141/200    │
  │ Banking Morning              │   200    │   220    │  83.4%     │ 158/200    │
  │ Foundation 9-10              │   120    │   150    │  88.9%     │  78%       │
  │ Dropper Batch                │    80    │    80    │  91.2%     │ 174/200    │
  └──────────────────────────────┴──────────┴──────────┴────────────┴────────────┘

FACULTY AT THIS BRANCH (18):
  Quantitative Aptitude: Mr. Suresh Kumar, Ms. Divya Nair, Mr. Arun Pillai (3)
  Reasoning:             Mr. Kiran Sharma, Ms. Ananya Roy (2)
  English:               Ms. Meena Iyer, Mr. Ravi Naidu (2)
  GK / Current Affairs:  Mr. Rajesh Varma, Ms. Sunita Bhat (2)
  Banking Specialist:    Mr. Praveen Rao, Ms. Latha Reddy (2)
  Computer / IT:         Mr. Deepak Sinha (1)
  Hindi:                 Ms. Vandana Sharma (1)
  Crash / Guest:         Mr. Harish Kumar, Mr. Naveen Joshi, Ms. Pooja Mehta (3)

INFRASTRUCTURE:
  Rooms: 12 (6 classrooms 60-seat, 4 classrooms 40-seat, 1 computer lab, 1 counselling)
  Library: 1,200 books + 3 newspaper subscriptions
  WiFi: 100 Mbps (4 access points)
```

---

## 3. Branch Performance Metrics

```
BRANCH PERFORMANCE COMPARISON — FEB 2026 MOCK RESULTS

                     MAIN     DILSUKHNAGAR   KUKATPALLY   ONLINE
  ─────────────────────────────────────────────────────────────────
  SSC CGL avg score   162/200    158/200         154/200    149/200
  SSC CHSL avg score  141/200    138/200         135/200      —
  Banking avg score   158/200    154/200         150/200    148/200
  Attendance rate     82.6%       79.4%           77.1%      68.3%
  Dropout rate (MTD)   0.4%        0.6%            0.8%       1.2%
  NPS score (student)   72          68              64         61
  ─────────────────────────────────────────────────────────────────
  Overall rank          #1          #2              #3         #4

ATTRITION DEEP-DIVE (Kukatpally ⚠️):
  Reasons logged: 3× transport issues, 2× shifted to competitor, 2× family reasons
  Recommended action: Add Saturday morning batch; coordinate with auto-stand nearby
```

---

## 4. Add / Edit Branch Form

```
ADD NEW BRANCH — TOPPERS COACHING CENTRE

  Branch Name:        [__________________________________]
  Location / City:    [__________________________________]
  Full Address:       [__________________________________]
  Branch Manager:     [Select from staff list ▼          ]
  Capacity (students):[______]  Rooms: [______]
  Contact Number:     [__________________________________]
  Email:              [__________________________________]
  Established Date:   [DD/MM/YYYY]
  Branch Type:        ( ) Owned   ( ) Franchise   ( ) Online-only
  GST Number:         [__________________________________]
  Status:             ( ) Active  ( ) Inactive  ( ) Upcoming

  BATCHES TO ENABLE AT THIS BRANCH:
    [ ] SSC CGL        [ ] SSC CHSL       [ ] RRB NTPC
    [ ] Banking        [ ] Foundation 9-10 [ ] Dropper
    [ ] Custom batch   [+ Add custom]

  [Save Branch]  [Cancel]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/branches/` | List all branches with summary stats |
| 2 | `GET` | `/api/v1/coaching/{id}/branches/{branch_id}/` | Full detail for one branch |
| 3 | `POST` | `/api/v1/coaching/{id}/branches/` | Create a new branch |
| 4 | `PATCH` | `/api/v1/coaching/{id}/branches/{branch_id}/` | Update branch details |
| 5 | `DELETE` | `/api/v1/coaching/{id}/branches/{branch_id}/` | Deactivate a branch (soft delete) |
| 6 | `GET` | `/api/v1/coaching/{id}/branches/{branch_id}/performance/` | Branch KPIs & mock score averages |
| 7 | `GET` | `/api/v1/coaching/{id}/branches/{branch_id}/faculty/` | Faculty list for a branch |
| 8 | `GET` | `/api/v1/coaching/{id}/branches/compare/` | Side-by-side branch comparison |

---

## 6. Business Rules

- Branch capacity is a hard operational limit enforced by the system; when student enrolments at a branch reach 95% of configured capacity, the system automatically stops accepting new online enrolments for that branch and notifies the Director and Branch Manager; a coaching centre that consistently operates above 90% capacity will see declining student satisfaction scores due to overcrowding, reduced faculty attention, and classroom noise — all factors that drive students to competitors.
- Each branch must have a designated Branch Manager assigned in the system before any student or faculty can be added to it; the Branch Manager role grants access to that specific branch's data only — they cannot view other branches' fee collection figures or faculty salary data; this role isolation is essential in multi-branch operations where managers may be in competition for performance bonuses.
- Branch performance comparison metrics are computed at 23:59 daily and cached for 24 hours; real-time KPIs (today's attendance, today's admissions) are computed on demand; directors must understand that the daily performance comparison reflects the previous day's close, not the current moment; this design prevents excessive database load from 40 faculty and 1,840 students simultaneously triggering aggregation queries.
- Deactivating a branch is a soft-delete operation — the branch's historical data (student records, fee transactions, test scores) is retained for 7 years per income tax and GST compliance requirements; only the branch's active status is changed, preventing new enrolments; any active students at the time of deactivation must be manually transferred to another branch before deactivation is allowed; the system will block the deactivation if unresolved active enrolments exist.
- Branch performance NPS (Net Promoter Score) is collected via an automated SMS survey sent to students 45 days after joining and again at the 6-month mark; the Branch Manager cannot view individual student NPS responses — only aggregate scores — to prevent any targeted pressure on students who gave low scores; the Director can view the distribution (how many Promoters, Passives, Detractors) per branch and use it for branch manager performance reviews.

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division A*
