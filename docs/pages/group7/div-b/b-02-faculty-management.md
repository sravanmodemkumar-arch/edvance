# B-02 — Faculty Management

> **URL:** `/tsp/admin/faculty/`
> **File:** `b-02-faculty-management.md`
> **Priority:** P1
> **Roles:** TSP Admin · TSP Manager · EduForge Support

---

## 1. Faculty List & Invite

```
FACULTY MANAGEMENT — TopRank Academy
12 active faculty | 2 pending invites | 1 deactivated

  SEARCH: [Search by name or email...        ]
  FILTER: Role: [All ▼]  Status: [Active ▼]  Exam: [All ▼]

  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │  # │ Name              │ Role           │ Exams          │ Questions│ Status     │
  ├────┼───────────────────┼────────────────┼────────────────┼──────────┼────────────┤
  │  1 │ Lakshmi Devi      │ Content Creator│ APPSC, TSPSC   │    2,840 │ Active     │
  │  2 │ Ravi Kumar        │ Content Creator│ SSC CGL/CHSL   │    1,960 │ Active     │
  │  3 │ Suresh Reddy      │ TSP Admin      │ All            │      420 │ Active     │
  │  4 │ Priya Sharma      │ Content Creator│ Banking IBPS   │    1,520 │ Active     │
  │  5 │ Venkat Rao        │ Test Manager   │ APPSC, SSC     │      — │ Active     │
  │  6 │ Anitha K.         │ Content Creator│ RRB NTPC       │      780 │ Active     │
  │  7 │ Ramesh Babu       │ Reviewer       │ All            │      — │ Active     │
  │  8 │ Kavitha M.        │ Content Creator│ APPSC          │    1,240 │ Active     │
  │  9 │ Srinivas P.       │ Test Manager   │ Banking, RRB   │      — │ Active     │
  │ 10 │ Deepika R.        │ Content Creator│ SSC, Banking   │      960 │ Active     │
  │ 11 │ Naresh G.         │ Content Creator│ APPSC, TSPSC   │      640 │ Active     │
  │ 12 │ Swathi B.         │ Content Creator│ SSC CGL        │      380 │ Active     │
  ├────┼───────────────────┼────────────────┼────────────────┼──────────┼────────────┤
  │ 13 │ Harish T.         │ Content Creator│ —              │      — │ Invited    │
  │ 14 │ Meena S.          │ Reviewer       │ —              │      — │ Invited    │
  └──────────────────────────────────────────────────────────────────────────────────┘

  [+ Invite Faculty]  [Bulk Invite via CSV]  [Export Faculty List]
```

---

## 2. Faculty Invite & Role Assignment

```
INVITE NEW FACULTY

  ── BASIC INFO ────────────────────────────────────────────────────────────
  Name:                 [ Harish Tiwari                          ]
  Email:                [ harish.t@gmail.com                     ]
  Phone:                [ +91-87654-XXXXX                        ]

  ── ROLE ASSIGNMENT ───────────────────────────────────────────────────────
  Role:                 [ Content Creator ▼ ]
                        Options:
                        ┌─────────────────────────────────────────────────┐
                        │ TSP Admin     — Full portal access, billing,   │
                        │                 settings, all management       │
                        │ TSP Manager   — Student + faculty management,  │
                        │                 reports, no billing/settings   │
                        │ Test Manager  — Create/schedule/publish tests, │
                        │                 view test analytics only       │
                        │ Content Creator— Upload questions, create      │
                        │                 study material, no management  │
                        │ Reviewer      — Review & approve questions,    │
                        │                 flag content, no creation      │
                        └─────────────────────────────────────────────────┘

  ── EXAM SCOPE ────────────────────────────────────────────────────────────
  Assigned exams:       [ ✅ APPSC  ○ SSC  ○ Banking  ○ RRB  ○ All ]
  (Faculty can only create content / manage tests for assigned exams)

  ── PERMISSIONS ───────────────────────────────────────────────────────────
  Can publish tests:    [ ○ Yes  ● No ] (requires Test Manager or Admin)
  Can view analytics:   [ ● Yes  ○ No ]
  Can manage students:  [ ○ Yes  ● No ] (requires Manager or Admin)
  Can access billing:   [ ○ Yes  ● No ] (TSP Admin only)

  [Send Invitation]  [Cancel]

  Invitation email sent to harish.t@gmail.com
  Faculty must accept invite within 7 days and set password.
```

---

## 3. Faculty Performance & Activity

```
FACULTY DETAIL — Lakshmi Devi (Content Creator)
Joined: 15 Apr 2026 | Last active: 31 Mar 2026 10:18 AM

  ── CONTRIBUTION SUMMARY ─────────────────────────────────────────────────
  Total Questions Created:     2,840
  Questions This Month:          320
  Approved (by Reviewer):      2,680  (94.4%)
  Flagged / Rejected:            160  ( 5.6%)
  Avg Review Turnaround:       1.2 days

  ── EXAM-WISE BREAKDOWN ──────────────────────────────────────────────────
  ┌──────────────────────────────────────────────────────┐
  │ Exam              │ Created │ Approved │ Reject Rate │
  ├───────────────────┼─────────┼──────────┼─────────────┤
  │ APPSC Group 2     │  1,680  │  1,612   │  4.0%       │
  │ TSPSC Group 1     │    720  │    664   │  7.8%       │
  │ APPSC Group 1     │    440  │    404   │  8.2%       │
  └──────────────────────────────────────────────────────┘

  ── RECENT ACTIVITY ──────────────────────────────────────────────────────
  31 Mar 10:18  Uploaded 120 Banking Awareness questions (IBPS PO batch)
  30 Mar 16:40  Created mock: "APPSC Gr2 Prelims Mock #13" (150 Qs)
  29 Mar 14:10  Edited 8 questions flagged by Reviewer Ramesh Babu
  28 Mar 09:30  Uploaded 85 Indian Polity questions (APPSC + TSPSC tagged)

  [Edit Role]  [Change Exam Scope]  [Deactivate Faculty]  [Reset Password]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/tsp/admin/faculty/` | List all faculty for this TSP |
| 2 | `POST` | `/api/v1/tsp/admin/faculty/invite/` | Send faculty invitation |
| 3 | `GET` | `/api/v1/tsp/admin/faculty/{id}/` | Faculty detail with activity and stats |
| 4 | `PATCH` | `/api/v1/tsp/admin/faculty/{id}/` | Update role, permissions, exam scope |
| 5 | `POST` | `/api/v1/tsp/admin/faculty/bulk-invite/` | Bulk invite via CSV upload |
| 6 | `DELETE` | `/api/v1/tsp/admin/faculty/{id}/` | Deactivate faculty (soft delete) |

---

## 5. Business Rules

- Faculty accounts are scoped to the TSP tenant; Lakshmi Devi's login at toprank.eduforge.in gives her access only to TopRank Academy's question pool, mock tests, and student data; she cannot see or interact with any other TSP's content even though all TSPs share the same EduForge infrastructure; the scoping is enforced at the API middleware level using the faculty member's `tsp_id` claim in the JWT token; if a faculty member works for two different TSPs (e.g., teaches at TopRank and also at another coaching centre), they need separate accounts with separate email addresses for each TSP
- The exam scope restriction on faculty is a content quality measure; a faculty member assigned to "APPSC" can only create questions tagged to APPSC exams, not to SSC or Banking; this prevents a History faculty from accidentally creating Quantitative Aptitude questions for SSC CGL; the restriction applies to question creation, mock test assembly, and study material uploads; a TSP Admin can change the exam scope at any time, and the change takes effect immediately; existing content created by the faculty remains accessible even if the exam scope is narrowed
- Faculty invitation expires after 7 days for security; the invite email contains a one-time-use token that creates the faculty account upon first login; after 7 days the token is invalidated and the TSP Admin must re-invite; this prevents stale invitations from being used months later when the person may no longer be associated with the TSP; the TSP Admin dashboard shows pending invitations with their expiry dates and a "Resend" button; a maximum of 50 pending invitations is allowed at any time to prevent abuse
- Content attribution tracks every question and mock test back to its creating faculty member; this serves three purposes: (a) accountability — if a batch of questions has errors, the TSP Admin can identify the creator and provide feedback; (b) performance measurement — TopRank Academy can see that Lakshmi Devi creates 320 questions/month with a 94.4% approval rate while Swathi B. creates 80 questions/month with a 91% approval rate; (c) payment — many TSPs pay freelance content creators per approved question (Rs.15–25 per MCQ depending on difficulty), and the attribution data feeds into the payment calculation

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division B*
