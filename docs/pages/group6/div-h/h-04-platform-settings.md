# H-04 — Platform Settings & Configuration

> **URL:** `/admin/exam/settings/`
> **File:** `h-04-platform-settings.md`
> **Priority:** P1
> **Data:** `platform_config` — global settings affecting exam portal behaviour

---

## 1. Platform Settings

```
PLATFORM SETTINGS — Exam Portal Configuration
Super Admin only

  ── CONTENT SETTINGS ──────────────────────────────────────────────────
  Free mocks per exam:           [ 2 ] (default for new exams)
  Free study materials per exam: [ 3 ] (default)
  CA capsule: free?              [●] Yes  [○] No
  Daily quiz: free?              [●] Yes  [○] No

  ── SUBSCRIPTION PLANS ────────────────────────────────────────────────
  Plan             │ Price/mo │ Price/yr │ Includes
  ─────────────────┼──────────┼──────────┼───────────────────────────
  Free             │    ₹0    │    ₹0    │ 2 mocks, 3 notes, CA, quiz
  Standard         │  ₹199    │ ₹1,499   │ All mocks + notes + videos
  Premium          │  ₹399    │ ₹2,999   │ Standard + rank predictor +
                   │          │          │ weak area blitz + AI planner
  Coaching Bundle  │ Custom   │ Custom   │ Institutional pricing
  [Edit plans]

  ── NOTIFICATION SETTINGS ─────────────────────────────────────────────
  Alert channels enabled:     [✅] Push  [✅] WhatsApp  [✅] Email  [✅] SMS
  Critical alert override DND:[●] Yes  [○] No
  Deadline reminders:         [ D-7, D-3, D-1 ]
  Weekly digest day:          [ Monday ▼ ] at [ 8:00 AM ▼ ]

  ── LANGUAGE SETTINGS ─────────────────────────────────────────────────
  Supported languages:  [✅] English  [✅] Telugu  [✅] Hindi  [  ] Tamil  [  ] Kannada
  Default language:     [ English ▼ ]
  Auto-detect from user state: [●] Yes (AP/TS → Telugu, others → English/Hindi)

  ── MONITORING SETTINGS ───────────────────────────────────────────────
  Default check frequency:    [ 60 ] minutes
  Max consecutive failures:   [ 10 ] (before marking unreachable)
  Verification SLA:           [ 2 ] hours

  ── PERFORMANCE ───────────────────────────────────────────────────────
  CDN cache (anonymous):      [ 5 ] minutes
  User data cache:            [ 60 ] minutes
  Eligibility cache refresh:  [ Daily at 6:00 AM ]
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/admin/exam/settings/` | All platform settings |
| 2 | `PATCH` | `/api/v1/admin/exam/settings/` | Update settings |

---

## 5. Business Rules

- Subscription pricing is the revenue model; the free tier is designed to demonstrate value (mock quality, analysis depth, CA freshness) so aspirants convert to Standard or Premium; the free-to-paid conversion rate target is 8–12% of monthly active users; pricing must be accessible to the target demographic (aspirants aged 18–28, many from middle-income families in AP/TS); ₹199/month is comparable to one autorickshaw ride's daily cost — affordable but not trivially cheap
- Language auto-detection from user's state is a critical UX decision; an AP domicile user who opens the platform should see Telugu as the default language, not English; a user from UP should see Hindi; auto-detection is based on the `user.domicile_state` field from their profile (D-03); unauthenticated users see the browser's `Accept-Language` header or the default (English); the user can always override the auto-detected language
- Adding new language support (e.g., Tamil for TNPSC aspirants, Kannada for KPSC) requires: (a) enabling the language in platform settings; (b) creating content (notes, questions, CA entries) in that language; (c) training content team members for that language; (d) updating notification templates; this is a significant operational investment; the platform setting only enables the language — content must follow; enabling Tamil without Tamil content creates empty pages, which is worse than not enabling it
- CDN cache duration (5 minutes for anonymous users) balances performance with freshness; during a notification release (SSC CGL notification comes out), the 5-minute cache means the notification appears in the feed within 5 minutes for anonymous users; for authenticated users, the feed is fetched fresh (no cache) because it is personalised; during result day traffic spikes, the CDN cache prevents the backend from being overwhelmed by millions of anonymous users refreshing the page

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division H*
