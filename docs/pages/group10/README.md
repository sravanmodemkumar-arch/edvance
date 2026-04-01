# Group 10 — Student Unified Portal

> **Purpose:** The student-facing portal — the single most important surface in EduForge. Serves 5,00,00,000+
> (5 crore) students across every institution type: schools (Class 1–12), junior colleges, degree colleges,
> coaching centres, exam domains, and TSP platforms. A student can simultaneously be enrolled in a school,
> a coaching centre, and an exam domain — this portal unifies everything into one profile, one dashboard,
> one login. The portal dynamically adapts layout, features, and content based on student type, age,
> access level, institution(s), subscription tier, exam domain, and preferred language.
>
> **URL prefix:** `student.eduforge.in/` (unified) OR `{institution}.eduforge.in/student/` (within institution)
> **Users:** All 20 student types (Primary School → Working Professional) · 6 access levels (S0–S6)

---

## Architecture Principle

```
STUDENT PORTAL = UNIFIED IDENTITY + DYNAMIC ADAPTATION + SCALE

  5,00,00,000 students (5 crore / 50 million)
      │
      ├── BY INSTITUTION TYPE
      │     ├── 12,00,000 school students (Class 1–12)
      │     ├── 8,40,000 college students (intermediate + degree)
      │     ├── 6,20,000 coaching students (JEE/NEET/Foundation)
      │     ├── 2,80,00,000 exam domain students (SSC/Banking/Railways/State PSC)
      │     ├── 1,50,00,000 working professionals (evening/weekend)
      │     └── 45,00,000 multi-platform students (school + coaching + domain)
      │
      ├── BY ACCESS LEVEL
      │     S0: No direct access (Class 1–5, parent/teacher managed)     — 8,00,000
      │     S1: View only (Class 6–8, see own marks/timetable)           — 6,00,000
      │     S2: Basic self-access (Class 9–10, take tests, view notes)   — 10,00,000
      │     S3: Full self-access, minor (Class 11–12, parent still sees) — 12,00,000
      │     S4: Full self-access, adult (18+, no mandatory parent view)  — 3,20,00,000
      │     S5: Premium subscriber (paid, advanced analytics, unlimited) — 1,40,00,000
      │     S6: Topper / Rank holder (special badge, mentorship)         — 25,000
      │
      ├── BY AGE & PRIVACY
      │     Under 13: COPPA-equivalent — no direct login, teacher/parent only
      │     13–17: Self-access with mandatory parent visibility
      │     18+: Full data control — parent access reduced per DPDP Act 2023
      │     18+ with deletion request: Must comply within 30 days
      │
      ├── DYNAMIC PAGE ADAPTATION
      │     Every page checks: student_type + access_level + institutions[]
      │     + subscription_tier + exam_domains[] + language + age
      │     and renders ONLY what that student should see.
      │     Example: Ravi (Class 12 MPC, Hyderabad, school + JEE coaching)
      │       → sees school card + coaching card + JEE domain card
      │       → performance dashboard merges school marks + mock test ranks
      │       → AI study plan weighs JEE Mains (47 days away) highest
      │     Example: Suresh (28, working professional, SSC CGL prep, Vijayawada)
      │       → sees ONLY SSC domain card, no school/coaching sections
      │       → evening/weekend study plan, current affairs emphasis
      │       → mobile-first layout (studies on phone during commute)
      │     Example: Priya (Class 6, Vizag, school only, parent-managed)
      │       → S1 access: view marks, timetable — cannot take online tests
      │       → parent sees same dashboard with parental controls
      │
      └── SCALE ARCHITECTURE
            Peak: 18,00,000 concurrent during SSC CGL mock test window
            CDN: Static assets via CloudFront — 22 edge locations across India
            Real-time: WebSocket for live test sync, rank updates, notifications
            Caching: Redis cluster — student dashboard cached 5 min, invalidated on event
            DB: Read replicas per region (South, North, East, West, Central)
            Mobile: 78% of students access via mobile — responsive-first design

  STUDENT IDENTITY MODEL:
    One EduForge Student ID → links to N institutions + N exam domains
    Profile persists across institution changes (school transfer, coaching switch)
    Historical data always accessible (alumni read-only access)
    Cross-platform analytics only with student consent (18+)
    Under-18: institution + parent see all data by default

  REVENUE CONTEXT:
    Free tier: 5 mock tests/month per domain, basic analytics, notes access
    Premium: ₹299/month or ₹2,499/year — unlimited tests, AI study plan,
             advanced analytics, video library, doubt resolution priority
    Institution-gifted: College/coaching pays bulk — students get premium free
    Scholarship: Merit/need-based — fee waived, premium access granted
```

---

## Divisions

| Division | Area | Pages |
|---|---|---|
| div-a | Student Registration, Profile & Settings | A-01 to A-05 |
| div-b | Academic Performance & Analytics | B-01 to B-05 |
| div-c | Mock Tests & Practice Engine | C-01 to C-05 |
| div-d | Study Material & Learning | D-01 to D-05 |
| div-e | Fees, Payments & Documents | E-01 to E-04 |

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal*
