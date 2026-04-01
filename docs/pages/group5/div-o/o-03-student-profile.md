# O-03 — Student Profile & Settings

> **URL:** `/coaching/student-portal/profile/`
> **File:** `o-03-student-profile.md`
> **Priority:** P2
> **Roles:** Student (self) — authenticated view

---

## 1. Student Profile

```
STUDENT PROFILE — Akhil Kumar (TCC-2401)

  ┌──────────────────────────────────────────────────────────────────────┐
  │  [PHOTO]  AKHIL KUMAR                    [Edit Profile]             │
  │           Roll No: TCC-2401                                          │
  │           Batch: SSC CGL Morning 2025–26                            │
  │           Enrolled: 12 August 2025                                  │
  └──────────────────────────────────────────────────────────────────────┘

  PERSONAL DETAILS:
    Date of Birth:    15 June 2001 (Age: 24)
    Gender:           Male
    Category:         OBC
    Aadhar:           XXXX-XXXX-1234 (last 4 digits — not shown in full)
    Address:          H.No. 4-2-186, Dilsukhnagar, Hyderabad — 500060

  CONTACT DETAILS:
    Primary phone:    +91-98765-12345   [Edit ✍️]
    Email:            akhil.kumar01@gmail.com  [Edit ✍️]
    Emergency contact: Mr. Rajesh Kumar (Father) — +91-87654-12345

  ACADEMIC BACKGROUND:
    Graduation:       B.Com, Osmania University (2022) — 68.4%
    12th Standard:    TS State Board (2019) — 82.0%
    Target exam:      SSC CGL 2025–26 (Inspector / Auditor preference)

  PARENT/GUARDIAN:
    Name:    Mr. Rajesh Kumar (Father)
    Phone:   +91-87654-12345
    Email:   rajesh.k@email.com
    Portal:  Active (linked ✅)
```

---

## 2. Account Settings

```
ACCOUNT SETTINGS — Akhil Kumar

  LOGIN & SECURITY:
    Login method:         Mobile OTP (primary)
    Password:             [Change Password]
    Two-factor auth:      ✅ Enabled (SMS OTP)
    Active sessions:      1 (this device)  [View / Logout other sessions]
    Last login:           31 Mar 2026, 9:14 AM — Hyderabad, TS (mobile)

  NOTIFICATION PREFERENCES:
    WhatsApp:    ✅ On  (test results, attendance, schedule)
    Email:       ✅ On  (receipts, certificates, important announcements)
    Push notif.: ✅ On  (app — iOS/Android)
    Do Not Disturb: Off   [Set quiet hours]

  PRIVACY SETTINGS:
    Share progress with parent:  ✅ Yes (attendance, scores, schedule)
    Share counselling notes:     ❌ No (private)
    Share welfare information:   ❌ No (private)
    Show name on leaderboard:    ✅ Yes (top-10 public leaderboard)

  BIOMETRIC CONSENT:
    Status:   ✅ Consented (Aug 2025)
    Data:     Fingerprint stored in device only — not in cloud
    Withdraw: [Withdraw biometric consent] → manual attendance will be used

  DATA RIGHTS (DPDPA):
    [Request my data]  [Correct my data]  [Request data erasure]  [Raise concern]
```

---

## 3. Document Vault

```
MY DOCUMENTS — Akhil Kumar

  UPLOADED AT ENROLLMENT:
    ✅ Aadhar Card (front + back) — uploaded Aug 2025
    ✅ 10th Marksheet — uploaded Aug 2025
    ✅ 12th Marksheet — uploaded Aug 2025
    ✅ Graduation Degree — uploaded Aug 2025
    ✅ Category Certificate (OBC) — uploaded Aug 2025
    ✅ Passport-size photo — uploaded Aug 2025
    ✅ Signed admission form — uploaded Aug 2025

  DOCUMENTS ISSUED BY TCC:
    ✅ Enrollment Certificate — issued Aug 2025 [Download]
    ✅ Digital ID Card — issued Aug 2025 [View]
    ⏳ Rank Certificate (Mock #25) — processing (requested 30 Mar)
    📅 Course Completion Certificate — available Jun 2026

  STORAGE:
    Used: 4.2 MB of 50 MB limit ✅
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-portal/profile/` | Student profile |
| 2 | `PATCH` | `/api/v1/coaching/{id}/student-portal/profile/` | Update profile (contact, preferences) |
| 3 | `GET` | `/api/v1/coaching/{id}/student-portal/settings/` | Account settings |
| 4 | `PATCH` | `/api/v1/coaching/{id}/student-portal/settings/privacy/` | Update privacy settings |
| 5 | `GET` | `/api/v1/coaching/{id}/student-portal/documents/` | Document vault |
| 6 | `POST` | `/api/v1/coaching/{id}/student-portal/documents/` | Upload document |

---

## 5. Business Rules

- Aadhar number is collected at enrollment as an identity verification document but is stored in masked form (only last 4 digits visible in the UI); the full Aadhar number is stored encrypted in the database and is accessible only to the Branch Manager and Accounts team for identity verification purposes; UIDAI regulations prohibit the display or storage of full Aadhar numbers in plain text in any digital system; logging the full Aadhar in access logs or query logs is prohibited; TCC's IT coordinator must configure the database to mask Aadhar on read queries returning data to the portal
- Profile updates (phone number, email, address) require OTP verification to the existing contact before the change is accepted; a malicious actor who gains portal access cannot change the phone number and lock out the real student without the original phone receiving an OTP; the OTP is sent to the current registered number, not the new one being set; for critical changes (phone number — the login credential), an in-person verification at the front desk is additionally required; this two-step (OTP + in-person) prevents account takeover via portal
- The document vault stores student documents only for the duration of study + 3 years (per the data retention policy in N-03); after the retention period, documents are automatically deleted (with a 30-day advance notice to the student to download); the student owns these documents and can download them at any time; TCC holds them as copies for identity verification purposes only — the originals were not surrendered; a student requesting deletion of their documents before the retention period ends is told that minimum retention is required for certificate issuance (which requires identity verification even after course completion)
- The "Data Rights (DPDPA)" section gives students direct access to their rights without needing to contact staff; a student can request a copy of all their data (data portability), request correction of wrong information (e.g., wrong DOB), or request erasure of non-mandatory data; these requests flow into the rights request queue (N-03) and are processed within 7 days; making rights requests easily accessible (not buried in settings) is a DPDPA good-practice requirement and reduces the burden on the counsellor who would otherwise handle these verbally
- The privacy settings (share progress with parent / share counselling notes) give adult students control over what their parents can see; a student who does not want their parent to know their mock test scores (perhaps managing parental pressure about exam performance) can disable score sharing; the student's wellbeing takes priority over the parent's desire for information when the student is an adult; the counsellor may advise students to keep the parent channel open for their own wellbeing (informed parents are more supportive), but ultimately this is the student's choice; TCC does not override an adult student's privacy settings based on parental requests

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division O*
