# A-05 — Go-Live Checklist & Launch

> **URL:** `/partner/onboard/go-live/`
> **File:** `a-05-go-live-checklist.md`
> **Priority:** P1
> **Roles:** TSP Owner · EduForge Onboarding Specialist (final review)

---

## 1. Go-Live Checklist

```
GO-LIVE CHECKLIST — TopRank Academy
Step 6 of 6

  ALL ITEMS MUST BE ✅ TO LAUNCH

  ── BRANDING ──────────────────────────────────────────────────────────
  ✅ Logo uploaded (400×100 px, transparent PNG)
  ✅ Colour palette configured (contrast ratio validated)
  ✅ Portal tagline set: "Excel in Every Exam"
  ✅ Email branding configured

  ── DOMAIN ────────────────────────────────────────────────────────────
  ✅ Subdomain active: toprank.eduforge.in
  ✅ Custom domain verified: www.toprankacademy.in
  ✅ SSL certificate provisioned (Let's Encrypt, auto-renew)

  ── CONTENT ───────────────────────────────────────────────────────────
  ✅ Own questions: 4,312 uploaded (0 errors remaining)
  ✅ Content licence: Standard tier activated
  ✅ At least 1 mock test published (3 published)
  🟡 Study notes: 0 (optional — not blocking launch)

  ── PAYMENTS ──────────────────────────────────────────────────────────
  ✅ Razorpay connected (KYC verified, test payment successful)
  ✅ Student plans created:
       Monthly ₹299 | Quarterly ₹799 | Annual ₹2,499
  ✅ Test payment ₹1 processed and refunded

  ── TEAM ──────────────────────────────────────────────────────────────
  ✅ TSP Admin account: suresh@toprankacademy.in (2FA enabled)
  🟡 Faculty accounts: 0 invited (optional — TSP can add later)

  ── LEGAL ─────────────────────────────────────────────────────────────
  ✅ Partnership agreement signed (digital, 28 Mar 2026)
  ✅ Content licence terms accepted
  ✅ Data processing addendum signed (student data handling)

  READINESS: 14/16 ✅  |  2 optional items (🟡) — not blocking

  [🚀 Launch Portal]
```

---

## 2. Launch Confirmation

```
LAUNCH PORTAL — TopRank Academy

  ⚠️  PLEASE CONFIRM:

  You are about to make your white-label portal live.
  After launch:
    • Students can access www.toprankacademy.in
    • Student signups and payments will be real (not test mode)
    • Razorpay will be switched from test mode to live mode
    • EduForge content licence billing starts from today

  YOUR PORTAL:
  ┌──────────────────────────────────────────────────────────────────┐
  │  www.toprankacademy.in                                          │
  │  ┌────────────────────────────────────────────────────────────┐ │
  │  │  [TopRank Logo]   Home  Exams  Mock Tests  Login  Signup  │ │
  │  ├────────────────────────────────────────────────────────────┤ │
  │  │                                                            │ │
  │  │  🏆 Excel in Every Exam                                    │ │
  │  │  Practice with 8,00,000+ questions for APPSC, SSC,        │ │
  │  │  Banking & more                                            │ │
  │  │                                                            │ │
  │  │  [Get Started — ₹299/month]                                │ │
  │  │                                                            │ │
  │  └────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────┘

  [Cancel]  [🚀 Confirm Launch]
```

---

## 3. Post-Launch Actions

```
🎉 PORTAL LIVE — TopRank Academy
Launched: 31 March 2026, 14:30 IST

  WHAT HAPPENS NOW:
  ┌──────────────────────────────────────────────────────────────────────┐
  │ ✅ Portal is live at www.toprankacademy.in                          │
  │ ✅ Razorpay switched to live mode                                   │
  │ ✅ Content licence billing started                                   │
  │ ✅ Onboarding specialist assigned for 30 days: Priya K.             │
  │                                                                      │
  │ NEXT STEPS:                                                          │
  │  1. Invite students (share link or bulk SMS/WhatsApp)               │
  │     [📋 Copy Signup Link]  [📧 Email Invite Template]              │
  │  2. Add faculty accounts (Admin → Team → Invite Faculty)            │
  │  3. Create more mock tests (Admin → Content → New Mock Test)        │
  │  4. Upload study notes/videos (optional, when ready)                │
  │                                                                      │
  │ STUDENT INVITE LINK:                                                 │
  │  www.toprankacademy.in/signup?ref=launch                            │
  │                                                                      │
  │ WHATSAPP TEMPLATE:                                                   │
  │  "Join TopRank Academy's online test platform! Practice APPSC,      │
  │   SSC & Banking mocks. Sign up: www.toprankacademy.in               │
  │   Plans from ₹299/month."                                           │
  │  [📋 Copy]  [📤 Share via WhatsApp]                                 │
  └──────────────────────────────────────────────────────────────────────┘

  SUPPORT CONTACT:
    Onboarding specialist: Priya K. (priya@eduforge.in | +91-98765-XXXXX)
    Support hours: Mon–Sat 9 AM – 7 PM IST
    Escalation: partnership-support@eduforge.in
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/partner/onboard/checklist/` | Full checklist with status per item |
| 2 | `POST` | `/api/v1/partner/launch/` | Launch portal (switches to live mode) |
| 3 | `GET` | `/api/v1/partner/launch/status/` | Post-launch status and metrics |
| 4 | `POST` | `/api/v1/partner/invite/generate/` | Generate student invite link with tracking ref |

---

## 5. Business Rules

- The go-live checklist is a hard gate, not a suggestion; the system blocks the Launch button until all required items are ✅; optional items (study notes, faculty accounts) are marked 🟡 and do not block launch; this prevents a TSP from going live with a broken portal (no logo, no content, no payment gateway) which would give their students a terrible first impression and generate support tickets for EduForge
- Launch flips Razorpay from test mode to live mode atomically; there is no "half-live" state; before launch, any payment attempt shows a test-mode banner and no real money moves; after launch, all payments are real; this single-switch design avoids the dangerous state where some students pay real money on a portal the TSP thinks is still in test mode
- The 30-day onboarding specialist assignment is a retention strategy; TSP churn data shows that TSPs who struggle in the first 30 days are 4× more likely to cancel; the specialist proactively checks dashboard metrics (student signups, first mock test completion, support tickets) and reaches out if numbers are low; after 30 days, the TSP transitions to standard support (ticket-based, no dedicated specialist)
- Student invite links include a tracking ref parameter so the TSP's analytics dashboard can attribute signups to specific campaigns (WhatsApp blast, email, social media, offline flyer QR code); the TSP can create multiple invite links with different refs; this is not just analytics — TSPs who see which channel drives signups invest more in that channel, which grows their student base, which grows EduForge's per-student revenue

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division A*
