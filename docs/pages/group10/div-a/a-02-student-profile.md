# A-02 — Student Profile & Identity

> **URL:** `/student/profile`
> **File:** `a-02-student-profile.md`
> **Priority:** P1
> **Roles:** All student types (S1–S6) · Parent (read-only view for minors) · Institution Admin (edits enrolment data)

---

## Overview

The student profile is the **single source of truth** for a student's identity across all institutions, exam domains, and subscription tiers on EduForge. A student like Ravi Kumar (Class 12, Hyderabad) enrolled in Sri Chaitanya Junior College AND TopRank JEE Coaching AND the JEE exam domain has ONE profile — not three. This page shows the unified profile, linked institutions, exam subscriptions, and account status. The profile adapts dynamically: a working professional (Suresh, 28, Vijayawada, SSC CGL prep) sees exam-focused fields; a school student sees class/section/roll number; a coaching student sees batch and schedule.

---

## 1. Profile Header

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ┌──────┐                                                                    │
│  │      │  Ravi Kumar                                                        │
│  │ PHOTO│  Student ID: EDU-STU-4827391                                       │
│  │      │  Class 12 MPC · JEE Aspirant · Premium ✅                          │
│  └──────┘  Hyderabad, Telangana · Joined 22 months ago                       │
│            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                      │
│            Profile completeness: ████████████░░ 85%  [Complete Profile →]    │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │ 🏫 2         │  │ 📝 3         │  │ ⭐ S5       │  │ 📅 22 months    │ │
│  │ Institutions │  │ Exam Domains │  │ Access Level │  │ Member Since    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Personal Information Section

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  PERSONAL INFORMATION                                         [Edit ✏️]      │
│                                                                              │
│  Full Name            Ravi Kumar                                             │
│  Date of Birth        15-Aug-2007 (18 years)    ← turned 18: Aug 2025       │
│  Gender               Male                                                   │
│  Mobile               +91 98765-43210 (verified ✅)                          │
│  Email                ravi.kumar2007@gmail.com (verified ✅)                 │
│  City                 Hyderabad                                              │
│  State                Telangana                                              │
│  Preferred Language   English (Telugu available)                              │
│                                                                              │
│  ── AGE TRANSITION NOTICE (shown once after 18th birthday) ──────────────   │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  🎂 You turned 18! Your data control has been upgraded.                │  │
│  │                                                                        │  │
│  │  ✅ You now control who sees your data (Settings → Privacy)           │  │
│  │  ✅ Parent view has been set to "Summary Only" (was "Full Access")    │  │
│  │  ✅ You can now pay fees directly without parent approval             │  │
│  │  ✅ Cross-platform data sharing requires YOUR consent only            │  │
│  │                                                                        │  │
│  │  Your parent (Mrs. Lakshmi Devi) can still see basic progress         │  │
│  │  unless you change this in Privacy Settings.                          │  │
│  │                                                                        │  │
│  │  [Review Privacy Settings →]  [Keep Current Settings]                 │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Linked Institutions

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MY INSTITUTIONS                                         [Link New → ]       │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  🏫 Sri Chaitanya Junior College, Kukatpally                  ACTIVE  │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │  Class 12 MPC · Section A · Roll No: 42                              │  │
│  │  Enrolled: June 2025 · Academic year: 2025–26                        │  │
│  │  Student ID (institution): SC-KPY-2025-1042                          │  │
│  │  Attendance: 94% · Last exam: Physics SA-2 (87/100, Rank 12)        │  │
│  │                                                                       │  │
│  │  Parent linked: Mrs. Lakshmi Devi (+91 87654-XXXXX) — Summary view   │  │
│  │  [View School Dashboard →]                                            │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  🎓 TopRank JEE Academy, Ameerpet                             ACTIVE  │  │
│  │  ─────────────────────────────────────────────────────────────────    │  │
│  │  JEE Advanced Batch A · Morning (6:30 AM – 10:30 AM)                │  │
│  │  Enrolled: April 2025 · Fee status: ₹8,500 due (this month)        │  │
│  │  Student ID (coaching): TR-JEE-A-0187                                │  │
│  │  Last mock: JEE Mock #23 — AIR 4,231 / 1,84,000 (↑ from 6,890)    │  │
│  │                                                                       │  │
│  │  [View Coaching Dashboard →]  [Pay ₹8,500 →]                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ── LINK A NEW INSTITUTION ──────────────────────────────────────────────   │
│  Enter the 8-digit code from your school/college/coaching:                  │
│  [ ________  ] [Link →]                                                     │
│                                                                              │
│  Can't find your code? Ask your class teacher or coaching admin.            │
│  Institution not on EduForge? [Tell them about us →]                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Exam Domain Subscriptions

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MY EXAM DOMAINS                                        [Add Domain → ]     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  📝 JEE Mains + Advanced                                    PREMIUM  │  │
│  │  Subscription: Premium (via TopRank coaching — institution-gifted)    │  │
│  │  Valid: Apr 2025 – Mar 2026 · Auto-renewed by coaching centre        │  │
│  │  Tests taken: 23 · Best AIR: 4,231 · Target: AIR < 2,000            │  │
│  │  [Open JEE Dashboard →]                                               │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  📝 SSC CGL 2026                                                FREE  │  │
│  │  Added: Jan 2026 · 5 tests/month limit · 3 tests remaining           │  │
│  │  Tests taken: 8 · Best rank: Not ranked (need Premium for AIR)       │  │
│  │  [Upgrade to Premium ₹299/month →]  [Open SSC Dashboard →]          │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │  📝 EAMCET (AP/TS)                                            PREMIUM │  │
│  │  Subscription: Premium (self-purchased ₹2,499/year)                  │  │
│  │  Valid: Oct 2025 – Sep 2026 · Renews: 14-Oct-2026                    │  │
│  │  Tests taken: 15 · Best rank: 1,847 / 94,000                        │  │
│  │  [Open EAMCET Dashboard →]                                            │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Profile — Working Professional View (Dynamic)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ┌──────┐                                                                    │
│  │      │  Suresh Babu                                                       │
│  │ PHOTO│  Student ID: EDU-STU-9183024                                       │
│  │      │  SSC CGL · IBPS Clerk · APPSC Group 2 — Working Professional      │
│  └──────┘  Vijayawada, AP · Free tier · Joined 3 months ago                  │
│                                                                              │
│  PERSONAL INFORMATION                                         [Edit ✏️]      │
│  Full Name            Suresh Babu                                            │
│  Age                  28 years (S4 — Full self-access)                       │
│  Qualification        B.Com, Acharya Nagarjuna University                   │
│  Occupation           Accounts Assistant, Private firm                       │
│  Study hours          Evening (6 PM – 10 PM) + Weekends                     │
│                                                                              │
│  ── NO INSTITUTIONS LINKED (exam domain only) ───────────────────────────   │
│  Working professionals typically prepare independently via exam domains.     │
│  Want to join a coaching centre? [Browse coaching near Vijayawada →]        │
│                                                                              │
│  MY EXAM DOMAINS                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐                │
│  │ SSC CGL     │  │ IBPS Clerk  │  │ APPSC Group 2        │                │
│  │ Free (2/5)  │  │ Free (4/5)  │  │ Free (1/5)           │                │
│  │ [Open →]    │  │ [Open →]    │  │ [Open →]             │                │
│  └─────────────┘  └─────────────┘  └──────────────────────┘                │
│                                                                              │
│  ⭐ Upgrade to Premium — ₹299/month for ALL domains combined               │
│     Unlimited tests + AI study plan + video library  [Upgrade →]            │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Profile — School Student View (Dynamic, Minor)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  ┌──────┐                                                                    │
│  │      │  Priya Kumar                                                       │
│  │ PHOTO│  Student ID: EDU-STU-7291835                                       │
│  │      │  Class 8 · Section B · Roll No: 18                                │
│  └──────┘  Vizag, AP · School: DAV Public School · S1 access (view only)    │
│                                                                              │
│  ⚠️ MINOR ACCOUNT — Parent/Guardian: Mrs. Lakshmi Devi (+91 87654-XXXXX)    │
│     Parent has full visibility of this dashboard.                            │
│                                                                              │
│  PERSONAL INFORMATION                                                        │
│  Full Name            Priya Kumar (set by school — cannot edit)              │
│  Date of Birth        22-Aug-2013 (12 years)                                │
│  Class / Section      8-B                                                    │
│  Roll Number          18                                                     │
│  Admission No.        DAV-VZG-2020-0842                                     │
│                                                                              │
│  ── S1 ACCESS: VIEW ONLY ────────────────────────────────────────────────   │
│  ✅ Can view: Marks, timetable, attendance, notes                           │
│  ❌ Cannot: Take online tests, pay fees, message teachers, download certs  │
│  ❌ Cannot: Edit profile (school admin manages)                             │
│  ❌ Cannot: Link other institutions or exam domains                        │
│                                                                              │
│  When Priya turns 14 → S2 access: can take tests, view notes, download     │
│  When Priya turns 16 → S3 access: full features, parent still sees data    │
│  When Priya turns 18 → S4 access: controls own data, parent access reduces │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/student/me` | Full profile with institutions, domains, access level |
| 2 | `PUT` | `/api/v1/student/me` | Update editable profile fields (name, city, language) |
| 3 | `POST` | `/api/v1/student/me/photo` | Upload/update profile photo (max 2 MB, face detection) |
| 4 | `GET` | `/api/v1/student/institutions` | List all linked institutions with status |
| 5 | `POST` | `/api/v1/student/institutions/link` | Link to institution via 8-digit code |
| 6 | `DELETE` | `/api/v1/student/institutions/{id}/unlink` | Unlink from institution (admin approval for minors) |
| 7 | `GET` | `/api/v1/student/domains` | List exam domain subscriptions |
| 8 | `POST` | `/api/v1/student/domains/add` | Add a new exam domain (free tier default) |
| 9 | `GET` | `/api/v1/student/access-level` | Current access level with feature matrix |
| 10 | `GET` | `/api/v1/student/profile-completeness` | Percentage + missing fields list |

---

## 8. Business Rules

- The student profile uses a **unified identity model** — one EduForge Student ID (format: `EDU-STU-{7-digit}`) persists across all institution changes, exam domain additions, and subscription upgrades; when Ravi transfers from Sri Chaitanya Kukatpally to Sri Chaitanya Dilsukhnagar, his student ID remains the same, his historical performance data stays intact, and only the institution linkage changes; the old institution's data becomes read-only archival, and the new institution sees a fresh enrolment with the option to import verified academic records from the previous institution (with student consent if 18+, or automatic for minors).

- Profile fields are sourced from different authorities depending on the student type: institution-created students have name, DOB, class, section, and roll number set by the institution admin — the student cannot edit these fields (greyed out with "Managed by [Institution Name]" label); self-registered students control all their own fields; when a self-registered student links to an institution, any conflicting data (e.g., DOB mismatch) is flagged to the institution admin for verification without blocking the student's access.

- The institution-linking flow via 8-digit code is the bridge between institution-managed and self-managed identities; the code is generated by the institution admin (Group 2/3/4/5 portals) and distributed to students via WhatsApp, printed on admission receipts, or displayed in the classroom; when a student enters the code, the system verifies: (a) code is valid and not expired (codes expire after 90 days), (b) code is not already used (one-time codes), (c) student's name approximately matches the institution's record (fuzzy match with 80% threshold to handle spelling variations like "Ravi" vs "Ravi Kumar"); on match, the institution is linked immediately and the student sees the institution card on their dashboard.

- Age-triggered access level transitions happen automatically at midnight IST on the student's birthday; the system runs a daily cron job checking all students whose DOB matches today's date and processes level upgrades: 13th birthday → S1→S2, 14th → (no change), 16th → S2→S3, 18th → S3→S4; on the 18th birthday transition, a one-time "You turned 18" banner (shown in Section 2 above) appears, parent access is automatically downgraded from "Full" to "Summary Only," and the student gains data control features (privacy settings, deletion request, cross-platform consent); the parent receives a WhatsApp notification: "Your child [Name] has turned 18. Your access level has been updated per DPDP Act 2023."

- Working professional profiles show additional fields: occupation, employer (optional), preferred study hours (morning/evening/weekend), and a "commute study" toggle that optimises the mobile experience for studying on buses/trains (larger fonts, offline-first content loading, shorter practice sessions of 10 questions instead of full mocks); 78% of working professionals access EduForge exclusively via mobile, and 42% report studying during their daily commute — the profile captures this to personalise the AI study plan (Division D).

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division A*
