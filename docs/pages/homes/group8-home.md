# Home Page: Group 8 — Parent Portal
**Route:** `/home`
**Domain:** `parent.eduforge.in` (or via school/coaching portal parent view)
**Access:** All parent/guardian types — view adapts per number of children and institutions
**Portal type:** Unified parent view — aggregates ALL children across ALL institutions

---

## Overview

| Property | Value |
|---|---|
| Purpose | One login for parent to see ALL children across ALL schools, coaching, exam domains |
| Key feature | Unified — a parent with 3 children in 3 different schools sees all in one dashboard |
| Domain | `parent.eduforge.in` — EduForge unified parent portal |
| Alternative access | Parent can also access via school/coaching portal — filtered to that institution only |
| Key rule | When student turns 18 → parent access auto-reduces (DPDP Act 2023) |

---

## Home View Variations

| Parent Scenario | Home Shows |
|---|---|
| 1 child, 1 school | Single child card with school data |
| 1 child in school + coaching | Two institution cards for same child |
| 2 children in different schools | Two child cards — each with their school |
| Multi-child, multi-institution | All children × all institutions — grid of cards |
| Child turns 18 during session | Notice banner. Some data auto-restricted. |
| Child has exam today | "Ravi has an exam at 9AM today" — highlighted alert |
| Fee overdue | ⚠️ badge on child's card. Pay Now CTA. |

---

## Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Top Navigation | Parent portal branding + notifications |
| 2 | Greeting + Date | Personalized welcome, today's highlights |
| 3 | Alert Banner | Fee due, exam today, absence, welfare alerts |
| 4 | Children Cards | One card per child — multi-institution per child |
| 5 | Fee Centre | All fees, all children, one payment screen |
| 6 | Messages | Teacher/counsellor messages across all institutions |
| 7 | Upcoming Events | Exams, PTMs, fee due dates — all children combined |
| 8 | Notifications | All alerts from all institutions |

---

## Section 1 — Top Navigation

| Element | Spec |
|---|---|
| Logo | EduForge parent portal logo — "EduForge · Parent" |
| Name | "Parent Portal" |
| Notifications bell | Shows alerts from ALL children across ALL institutions. Badge = total unread. |
| Profile | Parent's name, avatar, edit profile |
| Add child | "[+ Link Another Child]" — if parent has more children to add |

---

## Section 2 — Greeting + Today's Highlights

```
┌──────────────────────────────────────────────────────────────────────┐
│  Good morning, Suresh! 👋                                            │
│  Tuesday, 19 March 2024                                              │
│                                                                      │
│  TODAY AT A GLANCE                                                   │
│  ● 🎓 Ravi Kumar has Physics exam at 9AM (XYZ School)               │
│  ● ✅ Priya Kumari — attended today (ABC School) ✅                  │
│  ● 💰 Coaching fee due: ₹8,500 — due today for Ravi (ABC Coaching)  │
│  ● 📢 PTM: Saturday 10AM at ABC School — [Book Slot]                │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 3 — Alert Banner

| Priority | Alert |
|---|---|
| 🔴 Critical | "Priya absent for 3 consecutive days — [Contact School]" |
| 🔴 Critical | "Fee overdue by 15 days — Ravi Kumar, ABC Coaching — ₹8,500" |
| 🟠 Warning | "Ravi's attendance at ABC Coaching: 68% — below minimum 75%" |
| 🟡 Info | "New exam result published: Ravi — Maths Unit Test 87/100" |
| 🟢 Success | "PTM slot booked: Saturday 10AM — Mrs. Lakshmi (Class Teacher)" |

---

## Section 4 — Children Cards

> Core section. One card per CHILD. Each card shows ALL their institutions.

```
┌──────────────────────────────────────────────────────────────────────┐
│  MY CHILDREN                                   [+ Link Child]       │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  [Photo]  RAVI KUMAR                                         │   │
│  │           Class 12 MPC · Age 17 · DOB: 15 Jun 2006          │   │
│  │                                                              │   │
│  │  ┌────────────────────────┐  ┌─────────────────────────────┐│   │
│  │  │ 🏫 XYZ School         │  │ 🎓 ABC JEE Coaching          ││   │
│  │  │                       │  │                              ││   │
│  │  │ Attendance: 94% ████░ │  │ Attendance: 88% ████░        ││   │
│  │  │ Last marks: 87/100    │  │ Last AIR: 4,231              ││   │
│  │  │ Next exam: Tomorrow   │  │ Weak: Organic Chem ⚠️        ││   │
│  │  │ Fee: ✅ Paid          │  │ Fee: ⚠️ ₹8,500 due today     ││   │
│  │  │ [View Details →]      │  │ [Pay ₹8,500] [View →]        ││   │
│  │  └────────────────────────┘  └─────────────────────────────┘│   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  [Photo]  PRIYA KUMARI                                       │   │
│  │           Class 8 · Age 13 · DOB: 22 Sep 2010               │   │
│  │                                                              │   │
│  │  ┌────────────────────────────────────────────────────────┐ │   │
│  │  │ 🏫 ABC School                                          │ │   │
│  │  │                                                        │ │   │
│  │  │ ⚠️ Absent today                                       │ │   │
│  │  │ Attendance this month: 91%                            │ │   │
│  │  │ Recent marks: English 36/40                           │ │   │
│  │  │ Fee: ⚠️ ₹4,200 overdue (15 days)                     │ │   │
│  │  │ [Pay Fee]  [Message Teacher]  [View Details →]        │ │   │
│  │  └────────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

### Child Card Features

| Element | Spec |
|---|---|
| Child photo | 56×56px circle. Initials fallback. |
| Age + DOB | Shown as age. "Age 17". Full DOB below. |
| "Turns 18 soon" | If DOB within 60 days: yellow banner "Ravi turns 18 in 47 days — data access will change" |
| Institution cards | Horizontal scroll on mobile if more than 2 institutions |
| Fee badge | ✅ Paid (green) or ⚠️ Due (orange) or 🔴 Overdue (red) |
| [Pay Now] | In-card payment — Razorpay opens in modal. No page navigation. |
| Absence alert | 🔴 Red banner on institution card if absent today |

---

## Section 5 — Fee Centre

> Unified fee payment for ALL children across ALL institutions.

```
┌──────────────────────────────────────────────────────────────────────┐
│  Fee Centre                                    [Payment History →]  │
│                                                                      │
│  OUTSTANDING FEES                                                    │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Child             Institution          Amount     Due Date   │  │
│  │  ─────────────────────────────────────────────────────────── │  │
│  │  Ravi Kumar       ABC Coaching          ₹8,500    Today ⚠️   │  │
│  │  Priya Kumari     ABC School            ₹4,200    5 Mar 🔴   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  Total outstanding:  ₹12,700                                        │
│  [Pay ₹12,700 — All at once]   or pay individually above           │
│                                                                      │
│  ─────────────────────────────────────────────────────────────────  │
│  RECENT PAYMENTS (Last 30 days)                                      │
│  ✅ ₹15,000 — Ravi, XYZ School — 15 Feb  [View Receipt]            │
│  ✅ ₹12,500 — Priya, ABC School — 10 Feb  [View Receipt]           │
└──────────────────────────────────────────────────────────────────────┘
```

### Pay All Feature
- Single Razorpay checkout for multiple fee items
- One transaction, multiple receipts generated
- All institutions receive payment notification automatically

---

## Section 6 — Messages

```
┌──────────────────────────────────────────────────────────────────────┐
│  Messages from Teachers                              [View All →]   │
│                                                                      │
│  ● Mrs. Lakshmi (Class Teacher, XYZ School)          2 hrs ago      │
│    "Ravi has been distracted in class. Please discuss at PTM."       │
│    Child: Ravi Kumar    [Reply]                                      │
│                                                                      │
│  ● Mr. Rajesh (Counsellor, ABC Coaching)              Yesterday      │
│    "Priya's Maths score needs attention. Weak in algebra."           │
│    Child: Priya Kumari  [Reply]                                      │
│                                                                      │
│  [Send Message to Ravi's Teachers]  [Send to Priya's Teachers]     │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Section 7 — Upcoming Events (All Children Combined)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Upcoming Events                                                     │
│                                                                      │
│  TODAY                                                               │
│  ● Ravi — Physics exam 9AM (XYZ School)                             │
│  ● ⚠️ Coaching fee due: ₹8,500 (Ravi — ABC Coaching)               │
│                                                                      │
│  SAT, 22 MAR                                                         │
│  ● PTM: XYZ School 10AM (Ravi) — [Book Slot]                        │
│                                                                      │
│  MON, 25 MAR                                                         │
│  ● Priya — Annual Day (ABC School) 11AM                              │
│  ● Fee due: ₹4,200 (Priya — ABC School — already overdue)           │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Child Turns 18 — Transition Notice

> Auto-triggered on child's 18th birthday.

```
┌──────────────────────────────────────────────────────────────────────┐
│  ℹ️  Ravi Kumar turned 18 on 15 June 2024                           │
│                                                                      │
│  As per DPDP Act 2023, Ravi now controls his own data.              │
│  Your access has been updated:                                       │
│                                                                      │
│  ✅ Still visible: Attendance, timetable                             │
│  🔒 Now private (Ravi's choice): Mock test ranks, AI study plan      │
│                                                                      │
│  Ravi can grant you access to specific data from his profile.       │
│                                                                      │
│  [Understood]                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

---

## API Calls

| Section | Endpoint |
|---|---|
| Children list | `GET /api/v1/parent/children` |
| Each child's institutions | `GET /api/v1/parent/children/:id/institutions` |
| Fee outstanding | `GET /api/v1/parent/fees/outstanding` |
| Messages | `GET /api/v1/parent/messages` |
| Upcoming events | `GET /api/v1/parent/events?days=14` |
| Pay fees | `POST /api/v1/parent/fees/pay` |
