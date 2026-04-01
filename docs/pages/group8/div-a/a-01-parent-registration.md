# A-01 — Parent Registration & Verification

> **URL:** `/parent/onboard/register`
> **File:** `a-01-parent-registration.md`
> **Priority:** P1
> **Roles:** Parent · Guardian

---

## 1. Registration Landing Page

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           EduForge — Parents Portal                          │
│                                                                              │
│          "One account. All your children. Every institution."                │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │   Register as a Parent / Guardian                                      │  │
│  │                                                                        │  │
│  │   Full Name *          [ Mrs. Lakshmi Devi                          ]  │  │
│  │                                                                        │  │
│  │   Mobile Number *      [ +91 ] [ 98765-43210                        ]  │  │
│  │                          This number will be your login ID             │  │
│  │                                                                        │  │
│  │   Relationship *       ( ) Mother  (o) Father  ( ) Guardian            │  │
│  │                        ( ) Grandparent  ( ) Other                      │  │
│  │                                                                        │  │
│  │   City / Town *        [ Vijayawada                                 ]  │  │
│  │   State *              [ Andhra Pradesh                        ▼    ]  │  │
│  │                                                                        │  │
│  │   Preferred Language   [ Telugu                                ▼    ]  │  │
│  │                        (English / Telugu / Hindi / Tamil / Kannada)     │  │
│  │                                                                        │  │
│  │   ── Optional Identity Verification ──────────────────────────────     │  │
│  │                                                                        │  │
│  │   Aadhaar Number       [ XXXX-XXXX-4832                            ]  │  │
│  │                        Aadhaar is optional but enables faster           │  │
│  │                        child linking via UIDAI family linkage.          │  │
│  │                                                                        │  │
│  │   ☐  I agree to the Terms of Service and Privacy Policy               │  │
│  │   ☐  I consent to receiving SMS/WhatsApp notifications about           │  │
│  │      my children's academic progress                                   │  │
│  │                                                                        │  │
│  │                  [ Send OTP & Register ]                               │  │
│  │                                                                        │  │
│  │   Already registered?  [ Login with Mobile OTP ]                      │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Trusted by 2,400+ institutions across Andhra Pradesh & Telangana            │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Mobile OTP Verification Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        Verify Your Mobile Number                             │
│                                                                              │
│  We sent a 6-digit OTP to +91-98765-43210 via SMS                           │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │   Enter OTP:    [ 7 ] [ 2 ] [ 4 ] [ 8 ] [ 1 ] [ 6 ]                 │  │
│  │                                                                        │  │
│  │   OTP expires in 04:28                                                │  │
│  │                                                                        │  │
│  │                    [ Verify & Continue ]                               │  │
│  │                                                                        │  │
│  │   Didn't receive?  [ Resend OTP ]  |  [ Try WhatsApp OTP ]           │  │
│  │                     (available after 30s)                              │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ── Verification Status ─────────────────────────────────────────────────    │
│                                                                              │
│  Step 1: Mobile Number     +91-98765-43210         [VERIFIED]               │
│  Step 2: Aadhaar (opt.)    XXXX-XXXX-4832          [PENDING — verify now]   │
│  Step 3: Link Children     0 children linked       [NEXT STEP ->]           │
│                                                                              │
│  ── What happens next? ──────────────────────────────────────────────────    │
│                                                                              │
│  1. You'll receive a Family Account ID (e.g., FAM-AP-2026-08421)           │
│  2. Ask your child's institution for a 6-digit Linking Code                 │
│  3. Enter the code to link each child to your account                       │
│  4. Start monitoring attendance, grades, and fees from one dashboard        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Family Account Confirmation

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     Welcome, Mrs. Lakshmi Devi!                              │
│                                                                              │
│  Your Family Account has been created successfully.                          │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                        │  │
│  │   Family Account ID:    FAM-AP-2026-08421                             │  │
│  │   Registered Mobile:    +91-98765-43210                               │  │
│  │   Aadhaar Status:       Linked (XXXX-XXXX-4832)                      │  │
│  │   Location:             Vijayawada, Andhra Pradesh                    │  │
│  │   Preferred Language:   Telugu                                        │  │
│  │   Account Created:      31-Mar-2026, 10:14 AM IST                    │  │
│  │                                                                        │  │
│  │   ── Children Linked ─────────────────────────────────────────────    │  │
│  │                                                                        │  │
│  │   No children linked yet.                                             │  │
│  │                                                                        │  │
│  │   To link your child:                                                 │  │
│  │   1. Contact the institution (school/college/coaching)                │  │
│  │   2. Request a Parent Linking Code for your child                     │  │
│  │   3. Enter it on the next screen                                      │  │
│  │                                                                        │  │
│  │            [ Link Your First Child -> ]                               │  │
│  │                                                                        │  │
│  │   ── Also sent to your phone ─────────────────────────────────────    │  │
│  │                                                                        │  │
│  │   SMS: "Namaste Mrs. Lakshmi Devi! Your EduForge Parents account     │  │
│  │   is active. Family ID: FAM-AP-2026-08421. Link your children at     │  │
│  │   eduforge.in/parent — EduForge"                                     │  │
│  │                                                                        │  │
│  │   WhatsApp: Same message + PDF welcome guide in Telugu               │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `POST` | `/api/v1/parent/register` | Create parent account with mobile, name, relationship, city, state, language |
| 2 | `POST` | `/api/v1/parent/otp/send` | Send 6-digit OTP to parent's mobile via SMS or WhatsApp |
| 3 | `POST` | `/api/v1/parent/otp/verify` | Verify OTP and activate account; returns JWT token + family_account_id |
| 4 | `POST` | `/api/v1/parent/aadhaar/initiate` | Initiate Aadhaar verification via UIDAI sandbox/DigiLocker |
| 5 | `POST` | `/api/v1/parent/aadhaar/callback` | Callback from Aadhaar verification service; updates aadhaar_verified flag |
| 6 | `GET` | `/api/v1/parent/profile` | Retrieve parent profile, family account details, verification status |
| 7 | `POST` | `/api/v1/parent/resend-otp` | Resend OTP; enforces rate limit (max 5 per 10 minutes) |
| 8 | `GET` | `/api/v1/parent/registration-status` | Check registration completion (mobile verified, aadhaar status, children linked) |

---

## 5. Business Rules

- **BR-01 — One Mobile, One Family Account:** Each Indian mobile number (+91) can be associated with exactly one parent/guardian family account in the EduForge system. If a parent attempts to register with a mobile number that already exists, the system must redirect them to the login flow rather than creating a duplicate account. This prevents fragmentation of child records across multiple parent accounts and ensures that institutions always send notifications to a single verified contact. In cases where both parents wish to have separate accounts (e.g., divorced parents with shared custody), the second parent must register with their own mobile number and request a separate linking code from the institution, which the institution admin can issue at their discretion based on the custody arrangement documented with the school.

- **BR-02 — OTP Delivery and Expiry Policy:** The 6-digit OTP sent to the parent's mobile number must expire after exactly 5 minutes from the time of generation. The system must first attempt delivery via SMS using the registered telecom gateway, and if the parent does not verify within 60 seconds, an automatic fallback to WhatsApp delivery is triggered (since WhatsApp penetration among Indian parents is significantly higher than email). A maximum of 5 OTP requests are permitted within a rolling 10-minute window to prevent abuse. After 3 consecutive failed verification attempts, the account is temporarily locked for 30 minutes, and the parent receives an SMS explaining the lockout with a support helpline number. OTPs must never be logged in plaintext in application logs; they are stored as bcrypt hashes in the otp_verification table with a TTL-based auto-purge.

- **BR-03 — Aadhaar Verification Is Optional but Incentivised:** Aadhaar-based identity verification is strictly optional for parent registration, in compliance with the Supreme Court of India's Puttaswamy judgment that restricts mandatory Aadhaar linkage to non-essential services. However, parents who complete Aadhaar verification receive a "Verified Parent" badge on their profile, gain access to expedited child linking (the system can auto-suggest children using UIDAI family linkage data if the child's Aadhaar is also on file at the institution), and receive priority support routing. The Aadhaar number is never stored in plaintext; only the last 4 digits are displayed in the UI, and the full number is stored as a one-way hash (SHA-256 with institution-specific salt) in the aadhaar_hash column. The Aadhaar verification flow uses the DigiLocker API or UIDAI e-KYC sandbox, and the consent screen clearly explains what data is being accessed and for what purpose.

- **BR-04 — Regional Language and Accessibility Defaults:** Upon registration, the parent's preferred language selection determines the default language for the entire Parents Portal interface, all SMS and WhatsApp notifications, PDF report cards, and push notification content. The system supports Telugu, Hindi, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Odia, and English, with the language list dynamically filtered based on the parent's state selection (e.g., a parent in Andhra Pradesh sees Telugu, English, and Hindi as the top choices). If the parent does not explicitly select a language, the system defaults to the official language of their registered state (Telugu for AP, Tamil for TN, etc.). Language preference can be changed at any time from the profile page, and the change takes effect immediately for the portal UI and within 24 hours for scheduled notification templates. All SMS messages must be under 160 characters in the selected language, using Unicode encoding for regional scripts, and WhatsApp messages use pre-approved template messages registered with the WhatsApp Business API.

---

*Last updated: 2026-03-31 · Group 8 — Parents Portal · Division A*
