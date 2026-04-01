# Group 9 — B2B Content Partner Portal

> **Purpose:** Portal for content partners — publishers, subject matter experts (SMEs), content agencies,
> and regional language translators — who supply questions, study material, and videos to EduForge's
> shared content pool. Partners earn revenue when institutions or TSPs licence their content. This is the
> supply side of EduForge's content marketplace.
>
> **URL prefix:** `eduforge.in/content-partner/`
> **Users:** Content Partner (Publisher / SME / Agency) · EduForge Content Team (editorial review) · EduForge Finance (payouts)

---

## Architecture Principle

```
B2B CONTENT PARTNER = SUPPLY SIDE OF CONTENT MARKETPLACE

  EduForge Content Pool: 18,42,000+ questions
      │
      ├── SUPPLY (Content Partners — this portal)
      │     ├── Disha Publications (Delhi) — 2,40,000 questions
      │     │     Type: Publisher | Exams: UPSC, SSC, Banking, Railways
      │     │     Revenue: ₹4.8L/month (based on 2.4L students using their content)
      │     │
      │     ├── Dr. Venkat Rao (Visakhapatnam) — 18,500 questions
      │     │     Type: Individual SME | Exams: APPSC, SSC (Quant + Reasoning)
      │     │     Revenue: ₹38,000/month | Retired Maths Professor, Andhra University
      │     │
      │     ├── Telugu Vidya Content (Hyderabad) — 95,000 questions
      │     │     Type: Agency | Specialty: Telugu-medium translations
      │     │     Revenue: ₹1.2L/month
      │     │
      │     └── 340+ more content partners across India
      │
      ├── POOL (EduForge curates, tags, quality-scores)
      │     Every question: exam-mapped, difficulty-rated, language-tagged
      │     Quality score: 0–100 (based on accuracy, student feedback, discrimination index)
      │     Duplicate detection: normalised hash + semantic similarity
      │
      └── DEMAND (Institutions + TSPs licence content)
            TSPs (Group 7): licence content for white-label platforms
            Colleges (Group 4): use in internal assessments
            Coaching centres (Group 5): use in test series

  REVENUE MODEL:
    Content partner earns ₹0.02 per student per question per month
    Example: Dr. Venkat Rao's 18,500 questions × used by avg 1,200 students
             = ₹0.02 × 18,500 × 1,200 ÷ 18,500 (unique usage) ≈ ₹38,000/month
    EduForge takes 30% platform commission, partner gets 70%
    Monthly payouts via NEFT/IMPS to partner's bank account
    TDS deducted at source (10% for publishers, 10% for individuals under 194J)

  CONTENT LIFECYCLE:
    Partner Authors → Uploads → Editorial Review → Quality Score → Pool
    → Licensed by TSP/Institution → Students Attempt → Feedback Loop
    → Partner sees analytics (usage, accuracy, ratings)
```

---

## Divisions

| Division | Area | Pages |
|---|---|---|
| div-a | Partner Onboarding & Profile | A-01 to A-04 |
| div-b | Content Authoring & Upload | B-01 to B-05 |
| div-c | Content Review & Quality | C-01 to C-04 |
| div-d | Revenue & Payouts | D-01 to D-04 |
| div-e | Content Analytics & Performance | E-01 to E-04 |

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal*
