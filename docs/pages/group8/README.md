# Group 8 — Parents Portal

> **Purpose:** Unified portal for parents and guardians to monitor their children's academic progress,
> attendance, fee payments, and communicate with institutions — across every institution type on EduForge
> (school, college, coaching centre, test-series platform). A parent with three children in three different
> institutions sees everything in one place.
>
> **URL prefix:** `{institution}.eduforge.in/parent/` or `eduforge.in/parent/` (unified cross-institution view)
> **Users:** Parent · Guardian · Institution Admin (configures parent visibility settings)

---

## Architecture Principle

```
PARENT PORTAL = CROSS-INSTITUTION + READ-MOSTLY + CHILD-CENTRIC VIEW

  Parent: Mrs. Lakshmi Devi (Vijayawada, AP)
      │
      ├── Child 1: Ravi Kumar (age 21, B.Tech CSE 3rd year)
      │     Institution: GCEH (Godavari College of Engineering)
      │     Parent sees: Attendance, semester results, fee dues, placement updates
      │
      ├── Child 2: Priya Kumar (age 16, Class 11 MPC)
      │     Institution: Sri Chaitanya Junior College, Vijayawada
      │     Parent sees: Daily attendance, marks, homework, PTM, bus tracking
      │
      └── Child 3: Ravi Kumar (same child — also enrolled in coaching)
            Institution: TopRank Academy (coaching — test series)
            Parent sees: Mock test scores, rank, practice stats, subscription status

  WHAT PARENTS GET:
    ✅ Single login for all children across all institutions
    ✅ Real-time attendance alerts (SMS + push notification)
    ✅ Fee payment (online — Razorpay/Paytm) + tax receipts (80C)
    ✅ Exam results and progress trends (semester-wise, subject-wise)
    ✅ Direct messaging with class teacher / course coordinator
    ✅ PTM scheduling (book slots online, video call option)
    ✅ Transport tracking (school bus GPS — live location)
    ✅ Announcements, circulars, event calendar from each institution

  WHAT PARENTS DO NOT GET:
    ❌ Edit any academic data (read-only — institution controls data)
    ❌ See other students' data (only their linked children)
    ❌ Admin or faculty functions
    ❌ Direct access to LMS or question bank

  DATA FLOW:
    Institution → EduForge Platform → Parent Portal (read-only mirror)
    Parent actions: Pay fees, send messages, book PTM, approve leave
    All writes go through institution's approval workflow

  CROSS-INSTITUTION IDENTITY:
    Parent registers once with Aadhaar-linked mobile number
    Child linking: Institution shares a 6-digit code → parent enters code → verified
    One parent account can link to children across unlimited institutions
    If both parents register, both see the same children (family account)
```

---

## Divisions

| Division | Area | Pages |
|---|---|---|
| div-a | Parent Onboarding & Child Linking | A-01 to A-04 |
| div-b | Academic Monitoring | B-01 to B-05 |
| div-c | Fee Management & Payments | C-01 to C-04 |
| div-d | Communication & Engagement | D-01 to D-05 |
| div-e | Student Welfare & Safety | E-01 to E-04 |

---

*Last updated: 2026-03-31 · Group 8 — Parents Portal*
