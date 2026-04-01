# A-01 — Student Self-Registration

> **URL:** `/student/register`
> **File:** `a-01-student-registration.md`
> **Priority:** P1
> **Roles:** Unregistered user (self-service) · Institution Admin (bulk-creates students)

---

## Overview

Two registration paths exist: (1) **Self-registration** — a student discovers EduForge via an exam domain (SSC, Banking, Railways, State PSC) or a coaching centre's test-series link and signs up independently; (2) **Institution-created** — a school, college, or coaching centre bulk-uploads student records and the student receives a WhatsApp/SMS invite with a pre-provisioned account. This page covers the self-registration path. Institution-created students land directly on A-02 (Profile Setup) after first OTP login.

Self-registration handles 40,000+ new sign-ups per day during peak exam notification windows (e.g., SSC CGL notification week: 1,20,000 sign-ups in 3 days). The funnel must complete in under 2 minutes on a ₹8,000 Android phone over a 4G connection in a Tier-3 town.

---

## 1. Registration Landing — Exam Domain Entry Point

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     EduForge — Start Your Exam Prep                          │
│                                                                              │
│       "Join 5 crore students. Free mock tests. Instant rank."               │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │   Mobile Number *      [ +91 ] [ 98765-43210                        ]  │  │
│  │                         This will be your login ID                     │  │
│  │                                                                        │  │
│  │                  [ Send OTP & Start Free ]                             │  │
│  │                                                                        │  │
│  │   Already registered?  [ Login → ]                                    │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  POPULAR EXAM DOMAINS                                                        │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌─────────────┐  │
│  │  SSC CGL/CHSL │  │  Banking IBPS │  │  Railways RRB │  │  APPSC      │  │
│  │  28L students │  │  22L students │  │  18L students │  │  12L studs  │  │
│  │  [Start Free] │  │  [Start Free] │  │  [Start Free] │  │  [Start →]  │  │
│  └───────────────┘  └───────────────┘  └───────────────┘  └─────────────┘  │
│                                                                              │
│  + UPSC · TSPSC · CUET · JEE · NEET · Defence (CDS/NDA) · [View All 45+]   │
│                                                                              │
│  Trusted by: Disha Publications · TIME · Sri Chaitanya · Narayana · 1,900+  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. OTP Verification

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         Verify Your Mobile Number                            │
│                                                                              │
│   We sent a 6-digit OTP to +91 98765-43210                                  │
│                                                                              │
│   Enter OTP:   [ 4 ] [ 8 ] [ 2 ] [ 7 ] [ 1 ] [ 9 ]                        │
│                                                                              │
│   ⏱ Auto-read from SMS in 5 sec...                                          │
│                                                                              │
│   Didn't receive?  Resend via SMS (28s)  ·  Resend via WhatsApp             │
│                                                                              │
│                        [ Verify & Continue → ]                               │
│                                                                              │
│   ── EXISTING ACCOUNT DETECTED ──────────────────────────────────────────   │
│   (shown only if mobile already registered)                                  │
│                                                                              │
│   ⚠️ This mobile is already linked to:                                       │
│      Ravi Kumar · SSC Domain (Premium) · Joined 14 months ago               │
│      [Login to existing account →]  [Register new account with email →]     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Basic Profile Setup (Step 1 of 2)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  STEP 1 OF 2 — Tell Us About You                                            │
│  ━━━━━━━━━━━━━━━━━━━━ ○─────────────────────                                │
│                                                                              │
│  ┌── WHO ARE YOU? ────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │   Full Name *          [ Suresh Babu                                ]  │  │
│  │                                                                        │  │
│  │   Date of Birth *      [ 15 ] / [ 03 ] / [ 1998 ]                    │  │
│  │                         Age calculated: 28 years → Adult (S4 access)   │  │
│  │                                                                        │  │
│  │   Gender               (o) Male  ( ) Female  ( ) Other  ( ) Skip      │  │
│  │                                                                        │  │
│  │   City / Town *        [ Vijayawada                                 ]  │  │
│  │   State *              [ Andhra Pradesh                        ▼    ]  │  │
│  │                                                                        │  │
│  │   Preferred Language   [ Telugu                                ▼    ]  │  │
│  │                        English · Telugu · Hindi · Tamil · Kannada       │  │
│  │                        Marathi · Bengali · Gujarati · Odia · Malayalam  │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌── YOUR CURRENT STATUS ─────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │   I am currently:                                                      │  │
│  │   (o) Preparing for government exams (SSC/Banking/Railways/UPSC/PSC)  │  │
│  │   ( ) School student (Class 6–12)                                     │  │
│  │   ( ) College student (Intermediate / Degree / B.Tech)                │  │
│  │   ( ) Coaching student (JEE / NEET / Foundation)                      │  │
│  │   ( ) Working professional preparing for exams                        │  │
│  │   ( ) Dropper (gap year, preparing full-time)                         │  │
│  │                                                                        │  │
│  │   ── DYNAMIC: shown when "Preparing for government exams" ──          │  │
│  │                                                                        │  │
│  │   Which exams? (select all that apply)                                │  │
│  │   [x] SSC CGL      [x] SSC CHSL     [ ] SSC MTS                     │  │
│  │   [ ] IBPS PO      [x] IBPS Clerk   [ ] SBI PO                      │  │
│  │   [ ] RRB NTPC     [ ] RRB Group D  [ ] RPF                         │  │
│  │   [ ] UPSC CSE     [ ] UPSC CAPF    [ ] CDS / NDA                   │  │
│  │   [x] APPSC Group 1/2/3            [ ] TSPSC Group 1/2/3/4          │  │
│  │   [ ] CUET         [ ] CLAT         [ ] Other: [_____________]       │  │
│  │                                                                        │  │
│  │   Highest Education *  [ Graduation (B.A./B.Sc./B.Com)         ▼    ]  │  │
│  │   Attempt Number       [ 2nd attempt                           ▼    ]  │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│                                              [ Save & Continue → ]           │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Exam Domain Selection (Step 2 of 2)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  STEP 2 OF 2 — Choose Your Plan                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ━━━━━━━━━━━━━━━━━━━                       │
│                                                                              │
│  Based on your exams: SSC CGL · SSC CHSL · IBPS Clerk · APPSC Group 1/2/3  │
│                                                                              │
│  ┌─── FREE PLAN ──────────────────┐  ┌─── PREMIUM PLAN ──────────────────┐  │
│  │                                 │  │                                    │  │
│  │  ₹0 / forever                  │  │  ₹299/month  or  ₹2,499/year     │  │
│  │                                 │  │  (save ₹1,089 — 30% off)         │  │
│  │  ✅ 5 mock tests / month       │  │                                    │  │
│  │  ✅ Basic performance stats    │  │  ✅ Unlimited mock tests           │  │
│  │  ✅ Notes access (read-only)   │  │  ✅ Advanced analytics + AI plan  │  │
│  │  ✅ Previous year papers       │  │  ✅ Video library (4,200+ hrs)    │  │
│  │  ✅ Leaderboard view           │  │  ✅ Doubt resolution (priority)   │  │
│  │  ❌ AI study plan              │  │  ✅ Download notes + offline mode │  │
│  │  ❌ Video library              │  │  ✅ Current affairs daily digest  │  │
│  │  ❌ Doubt resolution           │  │  ✅ Sectional tests (unlimited)  │  │
│  │  ❌ Download / offline         │  │  ✅ All India Rank (detailed)     │  │
│  │                                 │  │  ✅ Topic-wise analysis           │  │
│  │  [ Start Free → ]              │  │                                    │  │
│  │                                 │  │  [ Start 7-Day Free Trial → ]    │  │
│  └─────────────────────────────────┘  └────────────────────────────────────┘  │
│                                                                              │
│  ── INSTITUTION-GIFTED ACCESS ───────────────────────────────────────────   │
│  Have an institution code?  [ Enter 8-digit code: ________ ] [Redeem]       │
│  Your school, college, or coaching may have already activated your account.  │
│                                                                              │
│  ── SCHOLARSHIP ─────────────────────────────────────────────────────────   │
│  EduForge Merit Scholarship: Score 80%+ in first 3 mock tests → 6 months   │
│  premium FREE. SC/ST/EWS: Upload income certificate for subsidised access.  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Dynamic Registration Paths (by Student Type)

| Student Type | Entry Point | Registration Flow | Post-Registration Landing |
|---|---|---|---|
| Exam domain (self-reg, 18+) | `ssc.eduforge.in` or ad link | Mobile OTP → Profile → Exam select → Plan | SSC domain dashboard |
| Working professional (25+) | Google search "SSC CGL mock test" | Mobile OTP → Profile → Exam select → Plan | Domain dashboard (evening mode) |
| School student (institution-created) | WhatsApp invite from school | OTP verify → Profile confirm (pre-filled) | School student dashboard |
| Coaching student (institution-created) | Coaching centre bulk upload | OTP verify → Profile confirm (pre-filled) | Coaching student dashboard |
| College student (institution-created) | College ERP import | OTP verify → Profile confirm (pre-filled) | College student dashboard |
| Dropper (self-reg) | Coaching website link | Mobile OTP → Profile → Exam + coaching link | Coaching + domain dashboard |
| Minor (13–17, self-reg via coaching) | Coaching registration desk | Parent mobile for OTP → Profile → Parent linked | Coaching dashboard + parent view |
| Trial user | "Try free" CTA on landing page | Mobile OTP → Skip profile → 3 free tests | Instant test start (profile later) |

---

## 6. Minor Student Registration (Under 18)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  STUDENT REGISTRATION — Minor (Under 18)                                     │
│                                                                              │
│  ⚠️ Students under 18 require a parent/guardian mobile number.               │
│  Your parent will receive an SMS to approve your account.                    │
│                                                                              │
│  Student Name *       [ Priya Kumar                                      ]  │
│  Date of Birth *      [ 22 / 08 / 2010 ]   Age: 15 → Minor (S2 access)     │
│                                                                              │
│  Parent/Guardian Mobile * [ +91 ] [ 87654-32100                          ]  │
│  Relationship *       ( ) Mother  (o) Father  ( ) Guardian                   │
│                                                                              │
│  ── PARENT CONSENT FLOW ─────────────────────────────────────────────────   │
│                                                                              │
│  1. OTP sent to PARENT's mobile (not student's)                             │
│  2. Parent enters OTP on this page (or student reads it from parent)        │
│  3. Parent receives WhatsApp: "Your child Priya has registered on           │
│     EduForge. You will receive academic updates. [View Dashboard →]"        │
│  4. Parent's mobile auto-linked to Parent Portal (Group 8)                  │
│                                                                              │
│  Parent OTP:   [ _ ] [ _ ] [ _ ] [ _ ] [ _ ] [ _ ]                         │
│                                                                              │
│                        [ Verify & Create Account → ]                         │
│                                                                              │
│  ── WHAT PARENTS SEE ────────────────────────────────────────────────────   │
│  ✅ All test scores, marks, attendance                                      │
│  ✅ Fee dues and payment history                                            │
│  ✅ Study time and activity (hours/day)                                     │
│  ❌ Private notes or bookmarks (student's personal space)                   │
│  ❌ Chat messages with teachers (visible only to student + teacher)         │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `POST` | `/api/v1/student/register/send-otp` | Send OTP to mobile (new or existing check) |
| 2 | `POST` | `/api/v1/student/register/verify-otp` | Verify OTP, return session token |
| 3 | `GET` | `/api/v1/student/register/check-mobile/{mobile}` | Check if mobile already registered |
| 4 | `POST` | `/api/v1/student/register/profile` | Submit basic profile (name, DOB, city, exams) |
| 5 | `POST` | `/api/v1/student/register/select-plan` | Choose free/premium/trial plan |
| 6 | `POST` | `/api/v1/student/register/redeem-code` | Redeem institution-gifted 8-digit code |
| 7 | `POST` | `/api/v1/student/register/minor/parent-otp` | Send OTP to parent's mobile for minor consent |
| 8 | `POST` | `/api/v1/student/register/minor/verify-parent` | Verify parent OTP + auto-link parent account |
| 9 | `GET` | `/api/v1/exam-domains/popular` | List popular exam domains with student counts |
| 10 | `GET` | `/api/v1/plans/compare` | Compare free vs premium feature matrix |

---

## 8. Business Rules

- The self-registration funnel is optimised for mobile-first, single-thumb operation on Android devices costing ₹8,000–₹15,000 with 4G connections in Tier-2/3 towns like Vijayawada, Warangal, Guntur, Patna, Lucknow, and Indore — these students represent 72% of new sign-ups; the entire flow from landing to first mock test must complete in under 2 minutes with no more than 3 screen transitions; the OTP auto-read uses the SMS Retriever API on Android to eliminate manual entry for 68% of users; WhatsApp OTP fallback is offered after 30 seconds because 22% of students report SMS delays on BSNL and Jio networks in rural AP and Telangana.

- Duplicate detection uses mobile number as the primary key — one mobile = one student account; however, siblings sharing a parent's phone are handled via the "institution-created" path where the institution assigns individual student IDs and the shared mobile is linked as a parent contact, not a student login; if a student tries to self-register with a mobile that already has an account, they see the existing account name (first name + last initial only, for privacy) and are offered login instead; the system never creates a second student account for the same mobile.

- Age calculation from DOB drives the entire access-level assignment: under 13 → S0/S1 (parent/teacher managed, no self-registration allowed — must be institution-created); 13–15 → S2 (basic self-access, parent OTP required during registration, parent auto-linked); 16–17 → S3 (full features, parent still sees all data); 18+ → S4 (adult, no parent linkage required, full data control); the DOB entered during registration is validated against the institution's records when the student later links to a school or coaching centre — a mismatch flags for admin review but does not block the student.

- Exam domain selection during registration personalises the entire student experience — selecting "SSC CGL" sets the default dashboard to SSC, loads SSC-specific mock tests, calibrates the AI study plan to CGL syllabus and exam pattern (200 questions, 60 minutes, negative marking -0.50), and ranks the student against the 28,00,000+ SSC CGL aspirants on EduForge; students can add or remove exam domains at any time from Settings without affecting their historical performance data; a student preparing for both SSC CGL and APPSC Group 2 sees a domain switcher in the top nav.

- The 7-day free trial for Premium requires only mobile OTP verification — no credit card, no UPI pre-auth; after 7 days, the account auto-downgrades to Free tier with a "Your trial ended — upgrade for ₹299/month" banner; trial-to-paid conversion is 18% nationally and 24% in AP/TS where EduForge has strongest brand recognition; the trial includes full analytics, AI study plan, and video library access to demonstrate premium value during the critical first week when study habits are forming.

- Institution-gifted access via 8-digit code works as follows: the institution (school, coaching, or college) purchases bulk Premium licences at ₹199/student/year (33% discount on retail); each licence generates a unique 8-digit alphanumeric code (e.g., `GCEH-4A7B`); the student enters this code during registration or from Settings; the code links the student to the institution and activates Premium for the licence period; if the student already has a free account, entering the code upgrades to Premium without losing any existing data or test history.

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division A*
