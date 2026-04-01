# Home Page: Group 1 — Platform Admin Portal
**Route:** `admin.eduforge.in/home`
**Access:** All Group 1 staff. Dashboard sections visible vary by access_level (0–5).
**Portal:** `admin.eduforge.in`

---

## Overview

| Property | Value |
|---|---|
| Purpose | EduForge's internal command center. Real-time view of the entire platform. |
| Primary users | Platform Admin (L5), Engineers, Support, Content, Sales, Finance |
| Key difference from others | This portal sees ALL institutions, ALL data — not scoped to one institution |
| Critical: Exam Day | War room mode — live exam monitoring takes over this page during exams |

---

## Page Sections

| # | Section | Visibility | Purpose |
|---|---|---|---|
| 1 | Top Navigation | All levels | Portal nav, global search, notifications, profile |
| 2 | Sidebar | All levels | Division-based navigation — filtered by access level |
| 3 | Platform KPI Bar | L3–L5 | Real-time platform-wide numbers |
| 4 | Alert Banner | L3–L5 | Active incidents, BGV warnings, subscription expirations |
| 5 | Quick Actions | By role | Role-specific shortcuts |
| 6 | Activity Feed | L3–L5 | Live platform events |
| 7 | My Work Queue | By role | Pending tasks for this user |
| 8 | Charts & Analytics | L1–L5 | Performance charts (level-filtered) |
| 9 | Team Activity | L3–L5 | What their team is working on |

---

## Section 1 — Top Navigation (admin.eduforge.in)

→ Component: [06-navigation.md](../components/06-navigation.md) — Top Nav
Special additions for Platform Admin:

| Element | Spec |
|---|---|
| Portal name | "EduForge Admin" — not an institution name |
| Global search | Searches across ALL institutions, users, exams, content |
| Notifications bell | Shows platform-level alerts (e.g., Lambda error, exam failure, BGV breach) |
| "War Room" button | Red button visible ONLY during active exams. Opens war room overlay. |
| Environment badge | "PROD" badge in red (vs "STAGING" in yellow) — always visible |

---

## Section 2 — Sidebar Navigation

→ Component: [06-navigation.md](../components/06-navigation.md) — Sidebar

### Nav Items by Access Level

| Nav Item | Min Level | Division |
|---|---|---|
| 🏠 Dashboard | L0 | All |
| 🏫 Institutions | L3 | C, I, J, K |
| 👥 Users (All Tenants) | L3 | C, I |
| 📝 MCQ Bank | L2 | D |
| 📋 Notes Library | L2 | D |
| 🎬 Video Library | L2 | D, E |
| 📅 Exam Management | L3 | F |
| 📊 Analytics & MIS | L1 | H |
| 🔍 BGV Management | L3 | G |
| 💬 Customer Support | L3 | I |
| 🤝 Customer Success | L3 | J |
| 💼 Sales & BD | L3 | K |
| 💰 Finance & Billing | L1 | M |
| ⚖️ Legal & Compliance | L1 | N |
| ⚙️ System Settings | L4 | C |
| 🔐 Security & Audit | L4 | C |
| 🤖 AI / ML Pipeline | L4 | H |

---

## Section 3 — Platform KPI Bar (Level 3+)

> 6 stat cards in a horizontal scrollable row. Real-time, auto-refreshes every 60 seconds.

→ Component: [07-data-display.md](../components/07-data-display.md) — Stat Card

| Card | Metric | Sub-info |
|---|---|---|
| 1 | Total Active Institutions | 1,247 / 1,900 registered. +3 this week |
| 2 | Total Students | 24,78,342. Trend vs last month. |
| 3 | Tests Running Now | 3 live. 47,320 students online. |
| 4 | Revenue MTD | ₹2.47 Cr. vs ₹2.1 Cr target |
| 5 | Support Tickets Open | 34 open. 12 overdue SLA |
| 6 | BGV Pending | 47 staff across 23 institutions |

> Level 0–2 users: KPI bar hidden or shows only relevant division metrics.
> Level 1 (e.g., CFO): only Revenue MTD visible.

---

## Section 4 — Alert Banner

→ Component: [03-alerts-toasts.md](../components/03-alerts-toasts.md) — Alert Banner

| Priority | Alert Type | Example |
|---|---|---|
| 🔴 Critical | Active incident | "Lambda function error — 3,200 exam submissions failing" [War Room] |
| 🟠 Warning | BGV | "47 staff have pending BGV. POCSO compliance risk." [Review] |
| 🟡 Info | Subscription | "12 institutions expire in 7 days. Renewal pipeline open." [View] |
| 🟢 Success | Resolved | "Yesterday's exam results published. 74,000 ranks computed." [View] |

> Multiple alerts: Stack vertically. Most critical at top. User can dismiss resolved ones.
> Critical alerts: Cannot be dismissed until incident resolved.

---

## Section 5 — Quick Actions (Role-specific)

> Cards of 4–6 most-used actions for this user's division. Different per role.

| Role | Quick Actions Shown |
|---|---|
| Platform Admin (L5) | [Add Institution] [Suspend User] [Run Migration] [Clear CDN Cache] [View Audit Log] |
| Content Director | [Create MCQ] [Review Queue (14)] [Pending Approvals (7)] [AI Generation Jobs] |
| Exam Ops Manager | [Schedule Exam] [Live Monitor] [Publish Results] [Send Notification] |
| Support Manager | [Open Tickets (34)] [Overdue SLA (12)] [Escalate to L3] [Call Log] |
| Finance Manager | [Outstanding (₹4.2L)] [Generate Invoice] [Razorpay Settlement] [GST Report] |
| BGV Manager | [Pending BGV (47)] [Send Reminders] [Flag Expired] [Institution Report] |

---

## Section 6 — Activity Feed (Level 3+)

> Live log of significant platform events. Real-time via WebSocket.

```
┌────────────────────────────────────────────────────────────────────┐
│  Platform Activity                              [Filter ▼] [Pause] │
│  ─────────────────────────────────────────────────────────────────│
│  🟢  2 min ago   · JEE Mock Test #47 started · 12,400 students    │
│  🔵  5 min ago   · New institution enrolled: Keshava College, Hyd │
│  🟡  12 min ago  · BGV approved: Ravi Kumar — XYZ School          │
│  🔴  18 min ago  · L2 ticket escalated: SSC domain login error    │
│  🟢  23 min ago  · Razorpay settlement: ₹1.24L received           │
│  🔵  31 min ago  · MCQ batch approved: 200 Maths Qs by Approver   │
│  ─────────────────────────────────────────────────────────────────│
│  [Load more]                                    Showing 6 of 247  │
└────────────────────────────────────────────────────────────────────┘
```

| Filter | Options |
|---|---|
| Event type | All / Exams / Institutions / Content / Finance / Support / Security |
| Time range | Last hour / Today / Yesterday / Last 7 days |
| Institution | Filter by specific institution |

---

## Section 7 — My Work Queue

> Pending tasks assigned to or owned by this user.

| Column | Content |
|---|---|
| Priority | 🔴 High / 🟡 Med / 🟢 Low |
| Task | Description of what's needed |
| Created | Relative time |
| Due | Deadline if set |
| Action | [View] [Complete] |

**Examples by role:**
- Question Reviewer: "14 MCQs waiting review — Maths (4), Chemistry (10)"
- BGV Executive: "3 verification requests — reply from employer awaited"
- Support L2: "Ticket #2847 — DB query needed for user data recovery"
- Billing Admin: "Invoice #INV-2024-1042 awaiting approval — ₹47,000"

---

## Section 8 — Charts & Analytics (Level 1+)

> 2-column grid of charts. Different charts per role.

| Role | Charts Shown |
|---|---|
| Platform Admin | MAU trend, Revenue trend, Exam volume, Error rate |
| Content Director | MCQ bank growth, Subject coverage %, Approval throughput |
| Exam Ops | Tests/month, Peak concurrent users, Results publish time |
| Analytics Manager | Student retention, Dropout signals, Cohort performance |
| Finance Manager | Revenue by segment, Churn, Outstanding dues aging |
| Sales Manager | Pipeline stages, Win rate, Institution segment breakdown |

→ Component: [07-data-display.md](../components/07-data-display.md) — Chart Components

---

## Section 9 — Team Activity (Managers only — L3+)

> For managers who have a team. Shows what their direct reports are working on.

```
┌────────────────────────────────────────────────────┐
│  Team Activity                                     │
│  ─────────────────────────────────────────────────│
│  [Priya]  Reviewing 12 MCQs — Chemistry           │
│  [Arun]   BGV call: Ramesh Kumar (ABC School)     │
│  [Divya]  Ticket #2845 — investigating DB issue   │
│  [Ravi]   Off today                               │
└────────────────────────────────────────────────────┘
```

---

## War Room Mode (Exam Day Override)

> Activated when: any exam has ≥ 1,000 concurrent students.
> Transforms the entire dashboard into exam monitoring.

```
┌────────────────────────────────────────────────────────────────────┐
│  🔴  WAR ROOM — EXAM LIVE                     [Exit War Room]      │
│  JEE Mock Test #47 · Started 10:00 AM · 74,320 online             │
│                                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Online   │  │ Errors   │  │ Submitted│  │ Lambda   │          │
│  │ 74,320   │  │ 3        │  │ 12,400   │  │ 847 warm │          │
│  │ ↑ normal │  │ ↑ LOW    │  │ 16.7%    │  │ ✅ ok    │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
│                                                                    │
│  Live error log (auto-refresh 5s)                                  │
│  [Pause Exam]  [Extend Time +15min]  [Emergency Broadcast]        │
└────────────────────────────────────────────────────────────────────┘
```

---

## API Calls (Home Page)

| Section | Endpoint | Method | Refresh |
|---|---|---|---|
| KPI Bar | `/api/v1/platform/kpis` | GET | Every 60s |
| Alert banners | `/api/v1/platform/alerts` | GET | Every 30s |
| Activity feed | `/ws/platform/activity` | WebSocket | Real-time |
| Work queue | `/api/v1/user/work-queue` | GET | On load + every 5 min |
| Charts | `/api/v1/platform/analytics?period=7d` | GET | On load |
| War room | `/ws/exam/war-room` | WebSocket | Real-time (exam day only) |
