# Page: Self Registration
**Route:** `ssc.eduforge.in/register` / `student.eduforge.in/register` / `parent.eduforge.in/register`
**Auth Stage:** 1 of 3 (register → OTP → profile setup)
**Access:** Public — no auth required

---

## Overview

| Property | Value |
|---|---|
| Purpose | Allow new users to create their own account (no admin needed) |
| Who can self-register | Exam Domain users (Group 6), Students (Group 10), Parents (Group 8) |
| Who CANNOT | Platform staff (Group 1), Institution staff (Groups 2–5), B2B Partners (Group 9) |
| Post-registration | OTP verification → Profile setup → Free tier access |

---

## Page Sections

| # | Section | Purpose |
|---|---|---|
| 1 | Page Header | Domain branding + "Create your free account" |
| 2 | Registration Form | Core fields |
| 3 | Exam Selection | What exams are they preparing for |
| 4 | Terms & DPDP | Consent checkboxes |
| 5 | Submit | Create Account CTA |
| 6 | Login Redirect | Already have account? → Login |

---

## Section 1 — Page Header

| Element | Type | Spec |
|---|---|---|
| Domain logo | Image | e.g., SSC Exam Domain logo. 48px height. |
| Domain tagline | H3 | e.g., "SSC CGL · SSC CHSL · RRB NTPC · UPSC" |
| Page title | H1 | "Create your free account" |
| Benefits strip | 3-column | "✅ Free · ✅ 5 mock tests/month · ✅ Rank among lakhs" |

---

## Section 2 — Registration Form

| Field | Type | Required | Validation |
|---|---|---|---|
| Full Name | Text input | ✅ Yes | Min 2 chars, letters + spaces only |
| Mobile Number | Input[tel] | ✅ Yes | 10 digits, starts with 6–9 |
| Date of Birth | Date (DD/MM/YYYY) | ✅ Yes | Must be 18+ for exam domains. Under 18 → redirect to student portal. |
| State | Select dropdown | ✅ Yes | All Indian states + "Outside India" |
| City / District | Text input | Optional | Free text |
| Gender | Radio (M/F/Other/Prefer not to say) | Optional | |

### Age Gate — Under 18

```
┌──────────────────────────────────────────────────────┐
│  ℹ️  Looks like you're under 18                      │
│                                                      │
│  Exam domain registration requires age 18+.         │
│  For students under 18, please use:                  │
│                                                      │
│  [Student Portal — student.eduforge.in]              │
│  (Ask your school or coaching to enrol you)          │
└──────────────────────────────────────────────────────┘
```

---

## Section 3 — Exam Selection (Multi-select)

| Element | Type | Spec |
|---|---|---|
| Section heading | Label | "I am preparing for: (select all that apply)" |
| Exam checkboxes | Checkbox grid | 2 columns on mobile, 3 on desktop |
| Minimum selection | 0 | Optional — can be done later from profile |

### Exam Options (SSC Domain example)

| Checkbox | Exam |
|---|---|
| [  ] | SSC CGL |
| [  ] | SSC CHSL |
| [  ] | SSC MTS |
| [  ] | SSC CPO |
| [  ] | RRB NTPC |
| [  ] | RRB Group D |
| [  ] | UPSC CSE (Prelims) |
| [  ] | Banking (IBPS PO/Clerk) |
| [  ] | State PSC |
| [  ] | Other Government Exams |

> Selection used to: personalize dashboard, suggest relevant test series, filter content.

---

## Section 4 — Terms & DPDP Consent

```
[✅] I agree to EduForge's Terms of Service and Privacy Policy.

[  ] I consent to receiving exam tips, results, and offers via
     WhatsApp and SMS.
     (Optional — unchecking means critical alerts only)
```

| Checkbox | Required | Default |
|---|---|---|
| Terms of Service | ✅ Required | Unchecked — must explicitly check |
| Marketing consent | Optional | Unchecked |

> DPDP Act 2023: Separate checkbox per purpose. Cannot bundle marketing with terms.
> "Privacy Policy" and "Terms" links open in modal — not new tab.

---

## Section 5 — Submit CTA

| Element | Spec |
|---|---|
| Button text | "Create Account — Free" |
| Button style | Primary, full-width, pill shape |
| Sub-text below | "No credit card. No fees. Start immediately." |
| On click | Validate form → send OTP → navigate to [03-otp-verification.md](03-otp-verification.md) |
| Duplicate mobile | If mobile already registered: "Account exists. [Log in instead →]" |

---

## Section 6 — Login Redirect

| Element | Spec |
|---|---|
| Text | "Already have an account?" |
| Link | "[Log In →]" — goes to [02-login.md](02-login.md) |

---

## Post-Registration Flow

| Step | What Happens |
|---|---|
| 1 | Mobile OTP verification ([03-otp-verification.md](03-otp-verification.md)) |
| 2 | Account created in `identity.users` + `identity.roles` |
| 3 | Role assigned: `exam_domain_student_free` (access level S4, 5 tests/month) |
| 4 | Profile setup wizard ([05-profile-setup.md](05-profile-setup.md)) |
| 5 | Welcome WhatsApp message sent |
| 6 | Redirect to student dashboard with onboarding checklist |

---

## API Calls

| Action | Endpoint | Method | Payload |
|---|---|---|---|
| Check mobile availability | `/api/v1/auth/check-mobile` | POST | `{mobile}` |
| Register + send OTP | `/api/v1/auth/register` | POST | `{name, mobile, dob, state, exam_goals, consents}` |
