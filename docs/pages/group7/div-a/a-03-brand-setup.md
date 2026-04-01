# A-03 — Brand Customisation (Logo, Colours, Domain)

> **URL:** `/partner/onboard/brand/`
> **File:** `a-03-brand-setup.md`
> **Priority:** P1
> **Roles:** TSP Owner (self-service) · EduForge Onboarding Specialist (support)

---

## 1. Brand Setup Interface

```
BRAND CUSTOMISATION — TopRank Academy
Step 2 of 6 · Estimated: 10 min

  ── LOGO & IDENTITY ───────────────────────────────────────────────────
  Primary logo:         [📁 Upload]  toprank-logo.png (400×100 px, transparent PNG)
                        Preview: [ TopRank Academy logo displayed ]
  Favicon:              [📁 Upload]  favicon-32.png (32×32 px)
  Tagline:              [ "Excel in Every Exam" ]

  ── COLOUR PALETTE ────────────────────────────────────────────────────
  Primary colour:       [ #1A5276 ] ████ (used: header, buttons, links)
  Secondary colour:     [ #F39C12 ] ████ (used: accents, badges, highlights)
  Background:           [ #FAFAFA ] ████ (portal background)
  Text colour:          [ #2C3E50 ] ████ (body text)
  Success / Error:      [ #27AE60 ] / [ #E74C3C ] (system — recommended defaults)

  LIVE PREVIEW:
  ┌──────────────────────────────────────────────────────────────────┐
  │ ████████████████████ HEADER (#1A5276) ████████████████████████  │
  │  [TopRank Logo]   Dashboard  Tests  Study Material   [👤 Suresh]│
  ├──────────────────────────────────────────────────────────────────┤
  │  Welcome, Student!                                              │
  │  ┌─────────────────┐  ┌─────────────────┐                      │
  │  │ Upcoming Test    │  │ Your Progress   │                      │
  │  │ APPSC Prelims #4 │  │ ████████░ 78%   │                      │
  │  │ [Start Test]█████│  │ 23/30 mocks done│                      │
  │  └─────────────────┘  └─────────────────┘                      │
  └──────────────────────────────────────────────────────────────────┘

  ── DOMAIN CONFIGURATION ──────────────────────────────────────────────
  EduForge subdomain:   toprank.eduforge.in   ✅ Active (auto-provisioned)
  Custom domain:        www.toprankacademy.in  🟡 Pending DNS setup

  DNS SETUP GUIDE:
  ┌──────────────────────────────────────────────────────────────────┐
  │ Add a CNAME record in your domain registrar's DNS settings:     │
  │                                                                  │
  │   Type:  CNAME                                                   │
  │   Name:  www                                                     │
  │   Value: toprank.eduforge.in                                     │
  │   TTL:   3600                                                    │
  │                                                                  │
  │ Then add a TXT record for domain verification:                   │
  │                                                                  │
  │   Type:  TXT                                                     │
  │   Name:  _eduforge-verify                                        │
  │   Value: ef-verify-a8b3c9d2e1f0                                  │
  │   TTL:   3600                                                    │
  │                                                                  │
  │ ⏱ DNS propagation takes 15 min – 48 hours                       │
  │ [🔍 Verify DNS Now]  [📋 Copy Instructions]  [📧 Email to IT]  │
  └──────────────────────────────────────────────────────────────────┘

  SSL: Auto-provisioned via Let's Encrypt once DNS is verified

  [← Back]  [Save & Continue →]
```

---

## 2. Email & Communication Branding

```
EMAIL BRANDING — TopRank Academy

  From name:            [ TopRank Academy ]
  Reply-to:             [ support@toprankacademy.in ]
  Email header:         [📁 Upload]  email-banner.png (600×120 px)
  Footer text:          [ TopRank Academy, Vijayawada, AP | Unsubscribe ]

  PREVIEW:
  ┌──────────────────────────────────────────────────────────────────┐
  │  [TopRank Academy Banner]                                       │
  │                                                                  │
  │  Hi Ravi,                                                       │
  │  Your APPSC Prelims Mock #4 is scheduled for tomorrow at 10 AM. │
  │  [Open Test Portal]                                              │
  │                                                                  │
  │  ── TopRank Academy, Vijayawada, AP | Unsubscribe ──            │
  └──────────────────────────────────────────────────────────────────┘

  [Save Email Branding]
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `PUT` | `/api/v1/partner/brand/` | Save brand settings (logo, colours, tagline) |
| 2 | `POST` | `/api/v1/partner/brand/logo/upload/` | Upload logo image |
| 3 | `PUT` | `/api/v1/partner/domain/` | Configure custom domain |
| 4 | `POST` | `/api/v1/partner/domain/verify/` | Trigger DNS verification check |
| 5 | `GET` | `/api/v1/partner/domain/ssl-status/` | SSL provisioning status |
| 6 | `PUT` | `/api/v1/partner/brand/email/` | Save email branding settings |

---

## 5. Business Rules

- Logo upload enforces dimension and format constraints (min 200×50 px, max 800×200 px, PNG or SVG with transparent background, max 500 KB) because the logo renders across multiple contexts — portal header, mobile app splash screen, email header, and PDF reports; a 2000×2000 px photo or a JPEG with a white background breaks the visual consistency; the system auto-generates a favicon from the logo if the TSP doesn't upload a separate one
- The colour palette is constrained to WCAG AA contrast ratios; the system validates that text colour against background meets 4.5:1 contrast ratio and that button text against primary colour meets 3:1; if the TSP picks a light yellow primary (#FFEB3B) with white text, the system warns "Insufficient contrast — your students may struggle to read buttons" and suggests alternatives; this protects TSP students from poor UI choices by non-designer TSP owners
- Custom domain setup is the #1 support ticket during onboarding because most TSP owners are not technical; the DNS guide is designed for copy-paste simplicity (the exact CNAME value is pre-filled); the "Email to IT" button generates a pre-written email the TSP owner can forward to their IT person or domain registrar support; despite this, ~35% of TSPs still need screen-share help from the onboarding specialist for DNS setup
- The EduForge subdomain (toprank.eduforge.in) is always available as a fallback even after custom domain setup; if the custom domain's DNS breaks or SSL expires, students are redirected to the subdomain automatically; the TSP cannot disable the subdomain — it is the safety net; this means every TSP has at least two working URLs from day one (subdomain + custom domain once verified)

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division A*
