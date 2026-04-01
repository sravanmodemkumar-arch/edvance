# A-05 — Data Privacy & Consent

> **URL:** `/student/settings/privacy`
> **File:** `a-05-data-privacy-consent.md`
> **Priority:** P1
> **Roles:** Student (S4–S6, 18+ only) · Parent (read-only for minors) · EduForge DPO (compliance)

---

## Overview

Privacy and consent management for students aged 18+, compliant with India's Digital Personal Data Protection (DPDP) Act, 2023. This page controls who sees the student's data across institutions, exam domains, and the parent portal. For students under 18, privacy is managed by the parent/institution — this page is hidden for S0–S3 access levels. The page also handles cross-platform consent (allowing coaching to see school data and vice versa), marketing consent, and the right to data portability and erasure.

---

## 1. Privacy Dashboard

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  DATA PRIVACY & CONSENT                        DPDP Act 2023 Compliant 🔒  │
│                                                                              │
│  Your data, your control. As an adult student (18+), you decide              │
│  who sees what.                                                              │
│                                                                              │
│  ┌─── PARENT ACCESS ────────────────────────────────────────────────────┐   │
│  │                                                                       │   │
│  │  Parent: Mrs. Lakshmi Devi (+91 87654-XXXXX)                         │   │
│  │                                                                       │   │
│  │  Current level: SUMMARY ONLY  [Change ▼]                             │   │
│  │  ─────────────────────────────────────                               │   │
│  │  ( ) Full Access     — Parent sees everything (as when you were <18) │   │
│  │  (o) Summary Only    — Overall %, rank, fee status. No details.     │   │
│  │  ( ) Alerts Only     — Only critical: fee overdue, attendance <75%  │   │
│  │  ( ) No Access       — Parent sees nothing. You manage everything.  │   │
│  │                                                                       │   │
│  │  ⚠️ Your parent will be notified of access level changes.            │   │
│  │  Changes take effect immediately.                                     │   │
│  │                                                                       │   │
│  │  [Save Parent Access Level]                                           │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Cross-Platform Data Sharing

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  CROSS-PLATFORM DATA SHARING                                                 │
│                                                                              │
│  Allow institutions to see your performance from other platforms?            │
│  This helps institutions personalise your learning experience.              │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │  Sri Chaitanya (School) ←→ TopRank (Coaching)                         │  │
│  │  Can school see your JEE mock test ranks?         [ YES / NO ]        │  │
│  │  Can coaching see your school marks?               [ YES / NO ]        │  │
│  │                                                                        │  │
│  │  Currently: Both OFF (institutions see only their own data)           │  │
│  │                                                                        │  │
│  │  Why enable? Your coaching can adjust your JEE prep based on          │  │
│  │  school exam performance. Your school can recognise JEE progress.     │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │  Exam Domains ←→ Institutions                                         │  │
│  │  Can SSC domain share your performance with institutions?  [ NO ]     │  │
│  │  Can institutions share your data with exam domains?       [ NO ]     │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │  EduForge Analytics (anonymised)                                      │  │
│  │  Allow your data (anonymised) to improve AI recommendations           │  │
│  │  for all 5 crore students?                          [ YES / NO ]      │  │
│  │  Currently: YES                                                       │  │
│  │  Note: This is ANONYMOUS — no one can identify you from this data.   │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Visibility Matrix

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  WHAT EACH PARTY CAN SEE                                                     │
│                                                                              │
│  ┌──────────────────────┬──────────┬──────────┬──────────┬───────────────┐  │
│  │ Data Type            │ You      │ Parent   │ School   │ Coaching      │  │
│  ├──────────────────────┼──────────┼──────────┼──────────┼───────────────┤  │
│  │ Name, DOB, photo     │ ✅       │ ✅       │ ✅       │ ✅            │  │
│  │ Mobile number        │ ✅       │ ✅       │ ❌       │ ❌            │  │
│  │ School marks         │ ✅       │ Summary  │ ✅       │ ❌ (unless →)│  │
│  │ Coaching mock ranks  │ ✅       │ Summary  │ ❌       │ ✅            │  │
│  │ JEE domain AIR       │ ✅       │ Summary  │ ❌       │ ❌            │  │
│  │ SSC domain scores    │ ✅       │ ❌       │ ❌       │ ❌            │  │
│  │ AI study plan        │ ✅       │ ❌       │ ❌       │ ❌            │  │
│  │ Fee payment history  │ ✅       │ ✅       │ Own fees │ Own fees      │  │
│  │ Chat with teachers   │ ✅       │ ❌       │ ✅       │ ✅            │  │
│  │ Attendance           │ ✅       │ Summary  │ Own inst │ Own inst      │  │
│  │ Study hours/activity │ ✅       │ ❌       │ ❌       │ ❌            │  │
│  │ Bookmarks & notes    │ ✅       │ ❌       │ ❌       │ ❌            │  │
│  └──────────────────────┴──────────┴──────────┴──────────┴───────────────┘  │
│                                                                              │
│  → = Can be enabled via cross-platform sharing (Section 2 above)            │
│  Parent column reflects "Summary Only" level. Changes with access level.    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Marketing & Communication Consent

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MARKETING & COMMUNICATION CONSENT                                           │
│                                                                              │
│  [x] Essential communications (test results, fee reminders, security)       │
│      ⚠️ Cannot be disabled — required for platform operation                │
│                                                                              │
│  [x] Educational updates (new test series, syllabus changes, exam dates)    │
│                                                                              │
│  [ ] Promotional offers (discounts, partner offers, upgrade campaigns)      │
│                                                                              │
│  [ ] Third-party partner communications (coaching ads, book publishers)     │
│                                                                              │
│  [x] EduForge newsletter (weekly tips, toppers' strategies, current affairs)│
│                                                                              │
│  Unsubscribe from all non-essential: [One-click unsubscribe →]              │
│                                                                              │
│  [Save Consent Preferences]                                                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Data Portability & Erasure

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  YOUR DATA RIGHTS (DPDP Act 2023)                                            │
│                                                                              │
│  ── RIGHT TO ACCESS ─────────────────────────────────────────────────────   │
│  View all data EduForge holds about you.                                    │
│  [View My Data →]  (opens detailed data inventory)                          │
│                                                                              │
│  ── RIGHT TO CORRECTION ─────────────────────────────────────────────────   │
│  Request correction of inaccurate personal data.                            │
│  [Request Correction →]  (opens support ticket)                             │
│                                                                              │
│  ── RIGHT TO DATA PORTABILITY ───────────────────────────────────────────   │
│  Export ALL your data in machine-readable format (JSON).                    │
│  Includes: profile, test results, analytics, notes, certificates.          │
│  Delivered to your email within 24 hours.                                   │
│  [Request Data Export →]                                                     │
│  Last export: 15-Mar-2026 (42 MB)  [Download again →]                      │
│                                                                              │
│  ── RIGHT TO ERASURE (Right to be Forgotten) ────────────────────────────   │
│  Permanently delete all personal data from EduForge.                        │
│  Processing time: 30 days. Cannot be undone.                                │
│  ⚠️ Academic records held by institutions may be retained                   │
│     per education regulations — only your EduForge profile is deleted.     │
│  [Request Account Deletion →]                                                │
│                                                                              │
│  ── GRIEVANCE OFFICER ───────────────────────────────────────────────────   │
│  Name: Mr. Anil Kumar, Data Protection Officer                              │
│  Email: dpo@eduforge.in                                                     │
│  Response time: Within 48 hours (weekdays)                                  │
│  [File a Grievance →]                                                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Consent Log

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  CONSENT HISTORY                                                [Export ↓]  │
│                                                                              │
│  ┌──────────┬───────────────────────────────────────┬────────┬────────────┐ │
│  │ Date     │ Action                                │ By     │ Channel    │ │
│  ├──────────┼───────────────────────────────────────┼────────┼────────────┤ │
│  │ 31-Mar-26│ Parent access: Full → Summary Only    │ Self   │ Web        │ │
│  │ 15-Aug-25│ Auto: Turned 18 → parent downgraded  │ System │ Auto       │ │
│  │ 15-Aug-25│ Auto: Access level S3 → S4            │ System │ Auto       │ │
│  │ 10-Apr-25│ Cross-platform sharing: Enabled        │ Self   │ Mobile app │ │
│  │ 01-Jun-24│ Registration consent + ToS accepted    │ Parent │ Web        │ │
│  └──────────┴───────────────────────────────────────┴────────┴────────────┘ │
│                                                                              │
│  Full audit trail: 12 entries · [View All →]                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/student/privacy` | Current privacy settings + consent state |
| 2 | `PUT` | `/api/v1/student/privacy/parent-access` | Update parent access level |
| 3 | `PUT` | `/api/v1/student/privacy/cross-platform` | Update cross-platform sharing toggles |
| 4 | `PUT` | `/api/v1/student/privacy/marketing-consent` | Update marketing consent preferences |
| 5 | `GET` | `/api/v1/student/privacy/data-inventory` | Full data inventory (what EduForge holds) |
| 6 | `POST` | `/api/v1/student/privacy/export` | Request data export (async, emailed as JSON) |
| 7 | `POST` | `/api/v1/student/privacy/delete` | Request account deletion (30-day process) |
| 8 | `POST` | `/api/v1/student/privacy/correction` | Submit data correction request |
| 9 | `GET` | `/api/v1/student/privacy/consent-log` | Full consent audit trail |
| 10 | `POST` | `/api/v1/student/privacy/grievance` | File grievance with DPO |

---

## 8. Business Rules

- Parent access level changes take effect **immediately** — when Ravi (18, Hyderabad) changes his parent's access from "Summary Only" to "No Access," Mrs. Lakshmi Devi's Parent Portal (Group 8) immediately stops showing Ravi's data, and she receives a WhatsApp notification: "Ravi Kumar has updated your access level. You will no longer receive academic updates. If you believe this is an error, contact the institution."; the parent cannot override this — the DPDP Act 2023 grants the 18+ student sovereign control over their personal data; however, if the student is linked to an institution where the parent is also registered, the institution can independently share summary reports with parents as part of their academic reporting workflow (separate from student-controlled privacy).

- Cross-platform data sharing is **opt-in** and **granular** — each pair of institutions requires separate consent; enabling "School → Coaching" does not automatically enable "Coaching → School" — the student controls each direction independently; when consent is granted, the receiving institution sees a real-time summary (not raw data) — for example, TopRank coaching sees "Ravi scored 87/100 in Physics at school (Rank 12/48)" but not individual question-level answers or teacher remarks; consent can be revoked at any time, and revocation removes the shared data from the receiving institution's view within 15 minutes (cache invalidation).

- The consent log is an immutable audit trail stored in a separate database table — it cannot be modified or deleted, even by the EduForge DPO; every consent action records: timestamp (UTC), action type, old value, new value, actor (self/system/parent), device, IP address, and channel (web/mobile/auto); this log is essential for DPDP Act compliance during regulatory audits by the Data Protection Board of India; the log is available for download by the student in JSON format and is included in any data export request.

- For students under 18, this entire page is hidden — privacy is managed by the parent through the Parent Portal (Group 8, Division E); when a minor student's account page is accessed, the URL `/student/settings/privacy` redirects to a simplified page that says "Your privacy settings are managed by your parent/guardian. When you turn 18, you'll gain full control over your data."; the minor can see what data is shared (read-only data visibility matrix) but cannot change any settings.

- EduForge's anonymised analytics consent (the "EduForge Analytics" toggle) is pre-set to YES during registration but can be toggled OFF at any time; anonymised data is genuinely anonymous — it goes through k-anonymity processing (k=50 minimum) before being used for aggregate statistics like question difficulty calibration, exam trend analysis, and AI recommendation model training; even with consent OFF, the student's data still contributes to their own personalised recommendations (AI study plan, weak topic identification) — the toggle only affects whether anonymised data feeds into platform-wide models.

---

*Last updated: 2026-03-31 · Group 10 — Student Unified Portal · Division A*
