# B-06 — Settings & Configuration

> **URL:** `/tsp/admin/settings/`
> **File:** `b-06-settings.md`
> **Priority:** P2
> **Roles:** TSP Admin · EduForge Support

---

## 1. Portal Settings & Branding

```
PORTAL SETTINGS — TopRank Academy
Domain: toprank.eduforge.in | Custom: www.toprankacademy.in

  ── BRANDING ──────────────────────────────────────────────────────────────
  Organisation Name:    [ TopRank Academy                        ]
  Tagline:              [ Your Path to Government Jobs            ]
  Logo (header):        [ toprank-logo.png ] 240x60px  [Change]
  Logo (favicon):       [ toprank-fav.ico  ] 32x32px   [Change]
  Primary Colour:       [ #1A5276 ] (Dark Blue)   [Pick]
  Secondary Colour:     [ #F39C12 ] (Orange)       [Pick]
  Login Page Banner:    [ login-banner.jpg ] 1920x600  [Change]
  Footer Text:          [ (c) 2026 TopRank Academy, Vijayawada. Powered by EduForge. ]

  ── DOMAIN CONFIGURATION ──────────────────────────────────────────────────
  EduForge Subdomain:   toprank.eduforge.in (cannot change)
  Custom Domain:        [ www.toprankacademy.in ]
  SSL Status:           Active (auto-renewed, Let's Encrypt)
  DNS CNAME:            www.toprankacademy.in → cname.eduforge.in  [Verified]

  ── PORTAL FEATURES ───────────────────────────────────────────────────────
  Mock Tests:           [ ✅ Enabled ]
  Study Material:       [ ✅ Enabled ]
  Video Lectures:       [ ○ Disabled ] (requires Premium plan)
  Discussion Forum:     [ ✅ Enabled ]
  Leaderboard:          [ ✅ Enabled ]
  Current Affairs:      [ ✅ Enabled ]
  Doubt Resolution:     [ ○ Disabled ] (enable to allow student queries to faculty)

  [Save Changes]  [Preview Portal]
```

---

## 2. Notification Preferences

```
NOTIFICATION SETTINGS — TopRank Academy

  ── STUDENT NOTIFICATIONS (what students receive) ─────────────────────────
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Event                      │ Email │ SMS  │ Push │ WhatsApp       │
  ├─────────────────────────────┼───────┼──────┼──────┼────────────────┤
  │  New mock test published    │  ✅   │  ✅  │  ✅  │  ✅            │
  │  Test result available      │  ✅   │  ○   │  ✅  │  ○             │
  │  Subscription expiry (7d)   │  ✅   │  ✅  │  ✅  │  ✅            │
  │  Subscription expired       │  ✅   │  ✅  │  ○   │  ✅            │
  │  New study material         │  ✅   │  ○   │  ✅  │  ○             │
  │  Weekly performance digest  │  ✅   │  ○   │  ○   │  ✅            │
  │  Exam date reminder         │  ✅   │  ✅  │  ✅  │  ✅            │
  │  Inactivity nudge (15d)     │  ○    │  ✅  │  ✅  │  ✅            │
  └──────────────────────────────────────────────────────────────────────┘

  ── ADMIN NOTIFICATIONS (what TSP Admin receives) ─────────────────────────
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Event                      │ Email │ SMS  │ Push                   │
  ├─────────────────────────────┼───────┼──────┼────────────────────────┤
  │  New student enrollment     │  ✅   │  ○   │  ✅                    │
  │  Payment received           │  ✅   │  ✅  │  ✅                    │
  │  Daily revenue summary      │  ✅   │  ○   │  ○                     │
  │  Student flagged question   │  ✅   │  ○   │  ✅                    │
  │  Faculty uploaded content   │  ✅   │  ○   │  ○                     │
  │  Scheduled test published   │  ✅   │  ○   │  ✅                    │
  │  Storage quota warning      │  ✅   │  ○   │  ✅                    │
  │  Monthly settlement ready   │  ✅   │  ✅  │  ✅                    │
  └──────────────────────────────────────────────────────────────────────┘

  ── SMS / WHATSAPP QUOTA ──────────────────────────────────────────────────
  SMS Credits:       4,200 / 10,000 remaining (Standard plan — 10K/month)
  WhatsApp Credits:  3,800 / 8,000 remaining (Standard plan — 8K/month)
  Next Reset:        01 Apr 2026
  [Buy Additional Credits]  [View Usage Log]

  [Save Notification Settings]
```

---

## 3. Integrations & Subscription Plans

```
INTEGRATIONS — TopRank Academy

  ── PAYMENT GATEWAY ───────────────────────────────────────────────────────
  Gateway:              Razorpay    [Connected]
  Razorpay Key ID:      rzp_live_****XXXX
  Webhook URL:          https://toprank.eduforge.in/api/v1/payments/webhook/
  Webhook Secret:       ••••••••••  [Reveal]  [Regenerate]
  Test Mode:            [ ○ Enabled  ● Disabled ]
  Auto-settlement:      [ ✅ Enabled — 10th of every month ]

  ── WHATSAPP BUSINESS ─────────────────────────────────────────────────────
  Provider:             Interakt (WhatsApp Business API)
  Status:               [Connected]
  API Key:              ••••••••••  [Reveal]
  Sender Number:        +91-80XX-XXXXXX (TopRank Academy)
  Templates Approved:   8 / 8 (all templates active)

  ── GOOGLE ANALYTICS ──────────────────────────────────────────────────────
  Tracking ID:          [ G-XXXXXXXXXX ]
  Status:               [Connected]
  Enhanced E-commerce:  [ ✅ Enabled ]

  ── CUSTOM WEBHOOK ────────────────────────────────────────────────────────
  Endpoint:             [ https://api.toprankacademy.in/eduforge-events ]
  Events:               [ ✅ New enrollment  ✅ Payment  ○ Test completed ]
  Secret:               ••••••••••  [Regenerate]
  Status:               [Active — last event 31 Mar 10:22 AM]

  ── SUBSCRIPTION PLANS (configured by TSP) ────────────────────────────────
  ┌──────────────────────────────────────────────────────────────────────┐
  │  Plan     │ Price    │ Duration │ Mock Access │ Study Mat │ Students │
  ├───────────┼──────────┼──────────┼─────────────┼───────────┼──────────┤
  │  Basic    │ Rs.299   │ 3 months │ 20 mocks    │ Limited   │    840   │
  │  Standard │ Rs.499   │ 6 months │ 50 mocks    │ Full      │  1,420   │
  │  Premium  │ Rs.999   │ 6 months │ Unlimited   │ Full+Video│    782   │
  └──────────────────────────────────────────────────────────────────────┘
  [Edit Plans]  [Create New Plan]  [View Plan Analytics]

  [Save Integration Settings]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/tsp/admin/settings/` | Get all portal settings |
| 2 | `PATCH` | `/api/v1/tsp/admin/settings/branding/` | Update branding (logo, colours, text) |
| 3 | `PATCH` | `/api/v1/tsp/admin/settings/domain/` | Update custom domain configuration |
| 4 | `GET` | `/api/v1/tsp/admin/settings/notifications/` | Get notification preferences |
| 5 | `PATCH` | `/api/v1/tsp/admin/settings/notifications/` | Update notification preferences |
| 6 | `GET` | `/api/v1/tsp/admin/settings/integrations/` | Get integration configurations |
| 7 | `PATCH` | `/api/v1/tsp/admin/settings/integrations/{provider}/` | Update specific integration |
| 8 | `GET` | `/api/v1/tsp/admin/settings/plans/` | List subscription plans |
| 9 | `POST` | `/api/v1/tsp/admin/settings/plans/` | Create new subscription plan |
| 10 | `PATCH` | `/api/v1/tsp/admin/settings/plans/{id}/` | Update subscription plan |

---

## 5. Business Rules

- Branding changes (logo, colours, tagline) are applied to the live portal within 60 seconds via CDN cache invalidation; the TSP Admin's "Preview Portal" button shows the changes in a sandboxed iframe before saving; however, changing the organisation name requires EduForge Support approval because the name appears on payment receipts, GST invoices, and student certificates — a name change without proper verification could be used for impersonation or fraud; the EduForge subdomain (toprank.eduforge.in) is permanently assigned and cannot be changed after onboarding because it serves as the canonical identifier in EduForge's internal systems and partner API integrations
- SMS and WhatsApp credits are metered because they have real per-message costs; EduForge pays Interakt approximately Rs.0.35 per WhatsApp message and Rs.0.25 per SMS via the DLT-registered route; the Standard plan includes 10,000 SMS and 8,000 WhatsApp credits per month, which is sufficient for a 3,000-student TSP sending 2–3 notifications per student per month; exceeding the quota blocks further messages until the next month or the TSP purchases additional credits at Rs.0.30/SMS and Rs.0.40/WhatsApp; the TSP Admin can view the usage log to see exactly which notifications consumed credits and optimise their notification strategy
- The Razorpay integration is the only payment flow; students pay through TopRank Academy's Razorpay account (not EduForge's), which means the money lands directly in TopRank's bank account; EduForge's platform fee is invoiced separately and debited from the TSP's settlement on the 10th of each month; this model is preferred by Indian coaching centres because they see the full payment in their bank account immediately (better cash flow) and the platform fee feels like a service charge rather than a revenue share; the webhook URL must be HTTPS and is auto-configured during onboarding; changing the Razorpay key requires re-verification to prevent accidental payment routing errors
- Subscription plan configuration is fully controlled by the TSP; TopRank Academy sets its own prices (Rs.299/499/999), durations, and access tiers; EduForge does not mandate pricing because each TSP's market is different — a Vijayawada coaching centre competes with Rs.200–500 local alternatives, while a pan-India ed-tech startup may charge Rs.1,999; the TSP can create up to 10 subscription plans; modifying a plan's price affects only new subscriptions — existing subscribers continue at their original price until renewal; deleting a plan is not allowed if active subscribers exist on that plan; the TSP must first migrate those subscribers to another plan or wait for all subscriptions to expire

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division B*
