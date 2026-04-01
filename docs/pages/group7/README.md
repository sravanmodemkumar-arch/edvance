# Group 7 — TSP White-Label Portal

> **Purpose:** White-label SaaS for Third-party Service Providers (TSPs) — coaching centres, ed-tech startups,
> content creators, and training companies who want to run their own branded exam prep platform powered by EduForge.
> The TSP gets their own domain, branding, student management, and content — all running on EduForge infrastructure.
>
> **URL prefix:** `{tsp-slug}.eduforge.in` or TSP's own custom domain
> **Users:** TSP Admin · TSP Faculty · TSP Students · EduForge Partnership Team

---

## Architecture Principle

```
WHITE-LABEL = MULTI-TENANT + CUSTOM BRANDING + CONTENT ISOLATION

  EduForge Platform (shared infrastructure)
      │
      ├── TSP-1: "TopRank Academy" (toprank.eduforge.in)
      │     Brand: own logo, colours, domain
      │     Content: own questions + EduForge shared pool (licensed)
      │     Students: 12,000 (isolated — TSP-2 cannot see them)
      │     Billing: TSP pays EduForge monthly per active student
      │
      ├── TSP-2: "Vizag Coaching Hub" (vizagcoach.com → custom domain)
      │     Brand: fully custom
      │     Content: 100% own content (no shared pool)
      │     Students: 4,200
      │
      └── TSP-N: ...

  WHAT TSP GETS:
    ✅ Branded student portal (their logo, colours, domain)
    ✅ Mock test engine (E-02 player) under their brand
    ✅ Question bank (own + optionally licensed from EduForge pool)
    ✅ Student management (enrollment, progress, analytics)
    ✅ Content CMS (notes, videos, CA — their own)
    ✅ Payment gateway (their Razorpay/Paytm account)
    ✅ Mobile app (white-labelled — their name on Play Store)

  WHAT TSP DOES NOT GET:
    ❌ Access to other TSPs' data
    ❌ EduForge's internal analytics
    ❌ Direct DB access (API only)
    ❌ Source code
```

---

## Divisions

| Division | Area | Pages |
|---|---|---|
| div-a | TSP Onboarding & Setup | A-01 to A-05 |
| div-b | TSP Admin Portal | B-01 to B-06 |
| div-c | White-Label Student Portal | C-01 to C-04 |
| div-d | Content Licensing & Marketplace | D-01 to D-04 |
| div-e | TSP Billing & Revenue | E-01 to E-04 |

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal*
