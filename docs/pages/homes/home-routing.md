# Home Page — Dynamic Routing by Profile & Institution

> After login + OTP verified, the user lands on THEIR home page.
> The home page content, branding, and modules shown are 100% based on:
>   1. Which institution they belong to
>   2. What their role is within that institution
>   3. Their access level (L0–L5 or S0–S6)
>
> ONE home page engine — infinite personalized views.

---

## Core Routing Logic (After Login)

```
User verified OTP
       │
       ▼
What is their primary role?
       │
       ├── Platform Staff (Group 1)
       │         → admin.eduforge.in/home
       │
       ├── Institution Group Staff (Group 2)
       │         → [group-slug].eduforge.in/home
       │
       ├── School Staff / Teacher (Group 3)
       │         → [school-slug].eduforge.in/home
       │         Brand: School logo + name + colors
       │
       ├── College Staff / Teacher (Group 4)
       │         → [college-slug].eduforge.in/home
       │         Brand: College logo + name + colors
       │
       ├── Coaching Staff / Faculty (Group 5)
       │         → [coaching-slug].eduforge.in/home
       │         Brand: Coaching logo + name + colors
       │
       ├── Student (Group 10) — enrolled in School
       │         → [school-slug].eduforge.in/home
       │         Brand: SAME school portal — student view
       │
       ├── Student (Group 10) — enrolled in Coaching
       │         → [coaching-slug].eduforge.in/home
       │         Brand: SAME coaching portal — student view
       │
       ├── Student — Multi-institution (School + Coaching)
       │         → Role Selector → choose which to open
       │         OR → unified student dashboard showing both
       │
       ├── Exam Domain User (Group 6/10)
       │         → ssc.eduforge.in/home (or rrb, upsc etc.)
       │
       ├── Parent (Group 8)
       │         → parent.eduforge.in/home
       │         Aggregates: ALL children's institutions in ONE view
       │
       ├── TSP Operator (Group 7)
       │         → [brand].testpro.in/home
       │
       └── B2B Partner (Group 9)
                 → partners.eduforge.in/home
```

---

## Home Page Personalization Matrix

Same URL ([slug].eduforge.in/home) — different content per role:

### School Portal: `[slug].eduforge.in/home`

| Who logs in | What they see |
|---|---|
| Principal | Full school management dashboard — attendance, finances, staff, exams, alerts |
| Vice Principal | Academic performance, exam schedule, teacher workload |
| Class Teacher | Their class attendance, student marks, parent messages |
| Subject Teacher | Their subject's test schedule, student performance in subject, MCQ bank |
| Student (S2–S4) | Personal attendance %, upcoming tests, marks, notes, fee status |
| Hostel Warden | Hostel occupancy, meal tracking, welfare alerts |
| Accountant | Fee collection, defaults, Razorpay settlements |
| Front Desk | Today's arrivals, calls, visitor log |
| Transport Manager | Route-wise bus attendance, vehicle tracking |

---

### Coaching Portal: `[slug].eduforge.in/coaching/home`

| Who logs in | What they see |
|---|---|
| Director | Revenue, total students, batch performance, AIR toppers |
| Batch Manager | Their batch — attendance, test schedule, student progress |
| Faculty | Their subject tests, student ranks in subject, MCQ upload queue |
| Counsellor | At-risk students, dropout signals, parent messages |
| Student (Minor) | Batch attendance, mock test AIR rank, weak topics, schedule |
| Student (Adult/Dropper) | Same + AI study plan, unlimited test access |
| Accountant | Batch-wise fee collection, defaulters |

---

### Exam Domain: `ssc.eduforge.in/home`

| Who logs in | What they see |
|---|---|
| Free user (5 tests/month) | Tests taken this month (X/5), best rank, upcoming free tests, upgrade CTA |
| Premium subscriber | Full dashboard — all test series, performance trends, AIR rank, AI plan |
| Working professional | Weekend test schedule highlighted, evening content blocks |

---

### Parent Portal: `parent.eduforge.in/home`

> Always aggregated across ALL children, ALL institutions.

| Children context | What they see |
|---|---|
| 1 child in 1 school | School attendance, marks, fee, timetable |
| 1 child in school + coaching | Combined view — school card + coaching card |
| 2 children in different schools | Both children's cards side by side |
| Child turns 18 | Notice: "Ravi has turned 18. Some data now private." Reduced view. |

---

## Institution Branding (Dynamic per Login)

When a user logs into ANY institution portal, the ENTIRE home page reflects that institution's identity:

| Element | How it changes |
|---|---|
| Page title | "[Institution Name] Portal" |
| Logo | Institution's logo (uploaded by admin) |
| Primary color | Institution-set color (default to portal type color if not set) |
| Portal name | "XYZ School" or "SR Nagar Coaching" |
| Background | Subtle pattern using institution color |
| Favicon | Institution logo |
| WhatsApp messages | Sent as "[Institution Name]: ..." |

> **Rule:** If institution has not uploaded a logo → EduForge logo shown.
> **Rule:** If institution has not set a color → portal type default color used.
> **TSP portals:** 100% operator-defined branding. No EduForge branding visible.

---

## Multi-Institution Student — Unified Dashboard

> When student is enrolled in School + Coaching simultaneously.

```
┌────────────────────────────────────────────────────────────────────┐
│  [EduForge Student Logo]  Welcome, Ravi Kumar             [👤 ▼]  │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  MY INSTITUTIONS                                                   │
│                                                                    │
│  ┌────────────────────────────┐  ┌──────────────────────────────┐ │
│  │ [XYZ School Logo]          │  │ [ABC Coaching Logo]           │ │
│  │ XYZ School, Hyderabad      │  │ ABC JEE Coaching             │ │
│  │ Class 12 MPC               │  │ JEE Advanced Batch           │ │
│  │                            │  │                              │ │
│  │ Attendance: 94% ████░      │  │ Last AIR: 4,231              │ │
│  │ Next exam: Mon 10AM        │  │ Weak: Organic Chemistry      │ │
│  │ Fee: ✅ Paid               │  │ Next test: Sun 10AM          │ │
│  │                            │  │ Fee: ⚠️ Due ₹8,500          │ │
│  │ [Open School Portal →]     │  │ [Open Coaching Portal →]     │ │
│  └────────────────────────────┘  └──────────────────────────────┘ │
│                                                                    │
│  MY EXAM DOMAINS                                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  [SSC Domain]  Premium ✅  · Tests this month: 12            │ │
│  │  Best rank: 1,847 / 2,34,000  · [Open SSC Domain →]         │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  PERFORMANCE SNAPSHOT                [View detailed analytics →]  │
│  [Chart: Overall score trend — 3 months]                          │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

This is `student.eduforge.in/home` — student's unified dashboard (Group 10).
Each institution card links into that institution's portal with student-level access.

---

## API — Home Page Data

| Data | Endpoint | Scope |
|---|---|---|
| User profile + role | `/api/v1/user/me` | Always |
| Institution branding | `/api/v1/institution/{slug}/branding` | Per institution |
| Role-specific home data | `/api/v1/home?role={role}&institution={slug}` | Role-filtered |
| Multi-institution list | `/api/v1/user/institutions` | Students with multiple |
| KPIs for home | `/api/v1/home/kpis` | Returns only what role can see |
