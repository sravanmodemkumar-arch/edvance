# EduForge — Group 13: Students (Unified Student Group)

> Students are the PRIMARY users of EduForge — everything is built for them.
> A student can simultaneously be in School + Coaching + Exam Domain + TSP.
> They need ONE unified student profile across all platforms.

---

## Why Students Need Their Own Unified Group

| Problem Without Unified Group | Solution With Group 13 |
|---|---|
| Student in school + coaching has 2 logins | One student ID across all platforms |
| Mock test rank in coaching not visible in school | Unified performance dashboard |
| Student switches coaching — performance history lost | Profile persists — institution changes, student stays |
| School can't see student's SSC prep performance | With consent, cross-platform analytics possible |
| Student turns 18 — parent access auto-reduces | Student controls their own data |
| Dropper student — no institution but needs exam domain | Self-registered student profile works standalone |

---

## Student Types — Complete Matrix

| # | Student Type | Age | Institution | Platform Access |
|---|---|---|---|---|
| 1 | Primary Student (Class 1–5) | 6–11 | School | Limited — teacher/parent managed |
| 2 | Upper Primary Student (Class 6–8) | 11–14 | School | Basic self-access + parent managed |
| 3 | High School Student (Class 9–10) | 14–16 | School | Self-access + parent view |
| 4 | Intermediate Student (Class 11–12) | 16–18 | College | Self-access — parent view until 18 |
| 5 | Coaching Student — Minor | 13–17 | Coaching | Self-access + parent view |
| 6 | Coaching Student — Adult | 18–30 | Coaching | Full self-access — no parent |
| 7 | Dropper — JEE | 18–20 | Coaching / None | Full self-access |
| 8 | Dropper — NEET | 18–20 | Coaching / None | Full self-access |
| 9 | Foundation Student (Class 6–10) | 11–15 | Coaching / School | Self-access + parent managed |
| 10 | Exam Domain Subscriber — Free | 18+ | None (self-reg) | Free tier — 5 tests/month |
| 11 | Exam Domain Subscriber — Premium | 18+ | None (self-reg) | Unlimited access |
| 12 | Working Professional | 22–35 | None | Evening/weekend — SSC, Banking |
| 13 | Correspondence / Distance | Any | None | Study material + tests only |
| 14 | TSP User (Coaching's test series) | Any | Via coaching | Access coaching's TSP portal |
| 15 | B2B Student (via institution) | Any | Institution pays | Access gifted by institution |
| 16 | Scholarship Student | Any | Any | Fee waived — merit or need |
| 17 | Government Scheme Student | 18–35 | Govt batch | PMKVY / Skill India funded |
| 18 | NRI / International Student | Any | Any | Overseas — time zone aware |
| 19 | Special Needs Student | Any | Any | Accessibility features, extra time |
| 20 | Trial User | Any | None | 7-day free trial |

---

## System Access Levels — Students

| Level | Label | Who | Age |
|---|---|---|---|
| S0 | No Direct Access | Primary (Class 1–5) — teacher/parent manages | 6–11 |
| S1 | View Only | Upper primary — see own marks, timetable | 11–14 |
| S2 | Basic Self-Access | High school — take tests, view notes | 14–16 |
| S3 | Full Self-Access (Minor) | Intermediate — all features, parent still views | 16–18 |
| S4 | Full Self-Access (Adult) | 18+ — all features, no mandatory parent view | 18+ |
| S5 | Premium Student | Paid subscriber — advanced analytics, unlimited | 18+ |
| S6 | Topper / Rank Holder | Special badge, leaderboard, mentorship access | Any |

---

## Division A — What Every Student Can Do (by access level)

| Feature | S0 | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|---|
| View attendance | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| View marks / results | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Take mock tests | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| View test analytics | ❌ | ❌ | Basic | ✅ | ✅ | Advanced |
| Access notes | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Access videos | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| View fee statement | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pay fees online | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Download rank card | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Download certificate | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Message teacher | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Cross-platform dashboard | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| AI study plan | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Unlimited tests | ❌ | ❌ | ❌ | School only | Domain: 5/mo | ✅ |
| Competitive rank (AIR) | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Doubt submission | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Manage own data / consent | ❌ | ❌ | ❌ | Partial | ✅ | ✅ |

---

## Division B — Student Unified Dashboard

```
Student Login — Single EduForge ID
          │
          ▼
┌─────────────────────────────────────────────────┐
│           MY DASHBOARD                          │
│                                                 │
│  ┌──────────────────┐  ┌─────────────────────┐ │
│  │  XYZ School      │  │  ABC Coaching       │ │
│  │  Class 12 MPC    │  │  JEE Batch          │ │
│  │  Attendance: 94% │  │  Last AIR: 4,231    │ │
│  │  Next exam: Mon  │  │  Weak: Org Chem     │ │
│  │  Fee: ✅ Paid    │  │  Next test: Sun 10AM│ │
│  └──────────────────┘  └─────────────────────┘ │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  SSC Domain (ssc.eduforge.in)           │  │
│  │  Subscription: Premium                  │  │
│  │  Tests this month: 12                   │  │
│  │  Best rank: 1,847 / 2,34,000           │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  Performance Trend    Weak Topics    AI Plan   │
└─────────────────────────────────────────────────┘
```

---

## Division C — Student Lifecycle (All Stages)

| Stage | What Happens | Platform Action |
|---|---|---|
| Enrolment | Institution creates student profile | Student gets login credentials via WhatsApp |
| First Login | OTP verification | Profile setup — photo, mobile, email |
| Active — Minor | Takes tests, views marks | Parent also sees data |
| Turns 18 | Birthday trigger | Parent notified → access reduces. Student controls data |
| Institution change | TC from old, join new | Old data archived, new institution linked |
| Multiple institutions | School + coaching simultaneously | Unified dashboard shows all |
| Subscription | Exam domain purchase | Razorpay → instant access |
| Dropper year | Leaves college, joins coaching | Marks profile as "dropper" — coaching linked |
| Exam selection | Cracks JEE/NEET/SSC | Topper badge, certificate, alumni status |
| Alumni | No active institution | Read-only access to own records — always |
| Data deletion request | DPDP Act 2023 right | Student can request deletion — platform must comply |

---

## Division D — Student Roles in System (12 platform roles)

| # | Role | Level | Linked To | Special Notes |
|---|---|---|---|---|
| 1 | Primary School Student | S2 | School only | Parent view mandatory |
| 2 | Intermediate College Student | S3 | College | Board exam tracking |
| 3 | Coaching Student — Minor | S3 | Coaching | Parent view until 18 |
| 4 | Coaching Student — Adult | S4 | Coaching | No mandatory parent view |
| 5 | Exam Domain Student — Free | S4 | Domain | 5 tests/month limit |
| 6 | Exam Domain Student — Premium | S5 | Domain | Unlimited + advanced analytics |
| 7 | Multi-Platform Student | S4 | School + coaching + domain | Unified dashboard |
| 8 | Dropper Student | S4 | Coaching only | Hostel-linked if residential |
| 9 | Self-Registered Student | S4 | None (independent) | Exam domain or TSP only |
| 10 | Working Professional | S4 | Exam domain | Evening/weekend usage pattern |
| 11 | Special Needs Student | S3/S4 | Any | Accessibility mode, extra time in tests |
| 12 | Topper / Rank Holder | S6 | Any | Special badge, leaderboard, mentorship |

---

## Division E — Student Data & Privacy

| Data Type | Who Can See It | Student Controls? |
|---|---|---|
| Name, photo, DOB | Institution + parent | ❌ (set at enrolment) |
| Mobile number | Platform only | ✅ (after 18) |
| Attendance records | Institution + parent | ❌ |
| Exam marks | Institution + parent + student | ❌ |
| Mock test ranks | Student + coaching + parent (minor) | Partial |
| AI study plan | Student only | ✅ |
| Cross-platform data | Student only (with consent) | ✅ |
| Historical records | Student always | ✅ (alumni access) |
| Deletion request | Student (18+) right | ✅ DPDP Act 2023 |

---

## Full Role Count — Group 13

| Division | Total |
|---|---|
| A — Access Level Permissions (matrix) | — |
| B — Dashboard (design, not roles) | — |
| C — Lifecycle stages | — |
| D — Student Platform Roles | 12 |
| E — Privacy (policy, not roles) | — |
| Student Types | 20 |
| **Total** | **32** |
