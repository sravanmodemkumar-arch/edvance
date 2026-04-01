# I-08 — Student Welfare MIS & Reports

> **URL:** `/college/welfare/reports/`
> **File:** `i-08-welfare-mis.md`
> **Priority:** P2
> **Roles:** Welfare Officer (S4) · NAAC Coordinator (S4) · Principal/Director (S6)

---

## 1. Welfare Dashboard

```
STUDENT WELFARE DASHBOARD — GCEH
As of 27 March 2027

WELFARE SNAPSHOT:
  ┌────────────────────────────────────────────────────────────────────────────┐
  │  142 sessions   28 grievances   312 scholarship  3 PwD            68 students│
  │  Counselling    (85.7% SLA)     beneficiaries    supported        counselled  │
  │  2026–27                        (56.1%)                           this year  │
  └────────────────────────────────────────────────────────────────────────────┘

ACTIVE WELFARE FLAGS (requiring action):
  🔴 2 students: Mental health referral (ongoing psychiatrist follow-up)
  🟡 1 grievance: GRV-005 (caste discrimination) — resolved ✅ (updated today)
  🟡 1 grievance: GRV-007 (JNTU result update) — awaiting JNTU response (8 days)
  🟡 TS ePASS receivable: ₹76L pending (govt delay — under follow-up)
  🟢 NSS certificates: 168/200 students achieved 240 hours ✅

NAAC CRITERION 5.1 INDICATORS (live):
  5.1.1 — Remedial coaching: 52 SC/ST + 22 OBC students in bridge programme ✅
  5.1.2 — Career counselling: 142 placement training sessions + counsellor ✅
  5.1.3 — Grievance redressal: 28 cases, 85.7% SLA compliance ✅
  5.1.4 — Student welfare schemes: 312 scholarship students supported ✅

STUDENT SATISFACTION (annual survey — Jan 2027):
  Overall campus experience: 82.4%
  Academic quality: 80.1%
  Infrastructure: 74.8% ← below target (labs need upgrade)
  Welfare services: 76.2%
  Hostel quality: 71.6% (Block A older facilities — improvement planned)
  Placement support: 88.4% ← highest rated
```

---

## 2. NAAC Criterion 5 Data Package

```
NAAC CRITERION 5 — STUDENT SUPPORT & PROGRESSION
(For SSR Cycle 3 — 2027)

5.1 — STUDENT SUPPORT:
  5.1.1 Scholarships/Freeships:
    Government scholarships: 306 students (55.0%)
    Institutional scholarships: 8 students (GCEH need-based — ₹5,000 – ₹15,000/year)
    Score: 4/5 (>50% students with financial support)

  5.1.2 Capability Enhancement:
    Soft skills training: Pre-placement training (all 332 final year students) ✅
    Language lab: 1 lab (60 seats); used for communication skills
    Bridge courses: 74 students in remedial programme ✅
    Career counselling: Placement cell + personal counsellor ✅
    Score: 4/5

  5.1.3 Grievance Redressal:
    Cases: 28 | Resolved within SLA: 24 (85.7%)
    Online mechanism: ✅ (EduForge)
    Anti-ragging: ✅ | POSH ICC: ✅
    Score: 3.5/5 (below 90% SLA target)

  5.1.4 Student Welfare Activities:
    Mediclaim: Group insurance for all students ✅
    Health facility: Campus dispensary (nurse + visiting doctor) ✅
    Canteen: FSSAI compliant, affordable (subsidised for economically weak) ✅
    Score: 4/5

5.2 — STUDENT PROGRESSION: (see Division E)
  Placement: 74.1% | Higher studies: 12.2% | Govt: 4.1%
  Score: 3.5/5

5.3 — STUDENT PARTICIPATION:
  NSS: 200 students (36%) | NCC: 60 (10.8%)
  Sports: 120 active + 28 inter-collegiate participants
  Cultural: 65 active (fest) + various club memberships (avg 3.4 clubs/student)
  Awards at inter-collegiate: 3 (Basketball runners-up, 2 technical awards)
  Score: 3.5/5

CRITERION 5 TOTAL: 3.7/5 (estimated)
```

---

## 3. Annual Welfare Report

```
ANNUAL STUDENT WELFARE REPORT — 2025–26
(Placed before Governing Body — September 2026)

EXECUTIVE SUMMARY:
  Student welfare services expanded significantly in 2025–26
  Key achievement: Professional counsellor appointed (first dedicated counsellor at GCEH)
  TS ePASS coverage: 56.1% of students with scholarship — record high
  Grievance resolution: 28 cases, 85.7% SLA (target: 90%)

WELFARE EXPENDITURE 2025–26:
  Counsellor salary + room: ₹5.4L
  NSS activities + camp: ₹2.8L
  Student club activities + fest: ₹4.2L
  FDP for welfare staff: ₹0.8L
  Sports activities: ₹1.2L
  Scholarship support cell: ₹1.4L
  PwD accommodation (modified workstations): ₹0.8L
  Medical (dispensary supplies, nurse): ₹2.4L
  Total welfare expenditure: ₹19.0L (3.4% of total revenue — NAAC recommends >3%)

IMPROVEMENTS RECOMMENDED:
  1. Hire additional counsellor or peer counsellors (current load: 142 sessions/1 counsellor)
  2. Sign language interpreter for Ravi K. (PwD student — hearing impaired)
  3. Improve Block A hostel ventilation (satisfaction 71.6%)
  4. Launch alumni mentorship formally (38% of alumni willing — survey data)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/welfare/reports/dashboard/` | Real-time welfare dashboard |
| 2 | `GET` | `/api/v1/college/{id}/welfare/reports/naac/criterion5/` | NAAC Criterion 5 data |
| 3 | `GET` | `/api/v1/college/{id}/welfare/reports/annual/` | Annual welfare report |
| 4 | `GET` | `/api/v1/college/{id}/welfare/reports/satisfaction/` | Student satisfaction survey data |

---

## 5. Business Rules

- Welfare expenditure as a percentage of revenue is a NAAC indicator; institutions that spend <2% on student welfare typically score poorly on Criterion 5; the ₹19L on welfare (3.4% of revenue) is within an acceptable range; the Governing Body should see this not as "cost" but as investment — better welfare services improve retention, reduce mental health crises, and improve NAAC scores
- The student satisfaction survey is a mandatory evidence item for NAAC Criterion 7; NAAC requires a documented student satisfaction survey with results and action taken; conducting a survey and not acting on results is worse than not conducting one (it shows the institution collects data only for compliance, not improvement); EduForge's satisfaction survey includes an action-tracking module that links each low-scoring area to an improvement plan
- Welfare MIS data aggregation must maintain individual privacy while enabling institutional decision-making; the Welfare Officer can see aggregate patterns (80 students with financial stress, 20 with relationship issues) but individual records must remain confidential; EduForge generates aggregate reports with a minimum cell size of 5 (any category with <5 responses is suppressed) to prevent individual identification from aggregate data
- The welfare function connects to almost every other module in EduForge; a student who has 3 absences flagged in the attendance module (A-05), a fee overdue in the fee module (C-02), and a low CIE score (B-03) is a high-welfare-risk student; EduForge's welfare module aggregates these signals into a "student at risk" score that triggers proactive welfare officer contact — this is the most powerful preventive welfare function
- Welfare services must be culturally sensitive; a counsellor who is not familiar with Telangana social contexts (caste, family structure, economic conditions, seasonal agricultural employment effects on fees) will miss important context; the counsellor should receive regional context orientation; EduForge's welfare notes module allows counsellors to tag sessions by presenting concern category (which feeds the aggregate analytics) without capturing sensitive narrative content

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division I*
