# D-02 — Usage Analytics

> **URL:** `/content-partner/revenue/usage-analytics/`
> **File:** `d-02-usage-analytics.md`
> **Priority:** P2
> **Roles:** Content Partner (own content) · EduForge Content Strategy Team

---

## 1. TSP & Institution Usage Overview

```
USAGE ANALYTICS — Dr. Venkat Rao (Partner ID: CP-0472)
March 2026 | 18,500 questions in pool

  CONTENT LICENSED BY TSPs / INSTITUTIONS
  ┌─────┬──────────────────────────────────┬──────────┬─────────┬──────────┐
  │  #  │ TSP / Institution                │ Students │ Qs Used │ Attempts │
  ├─────┼──────────────────────────────────┼──────────┼─────────┼──────────┤
  │  1  │ Disha Publications (TSP-0108)    │   28,400 │  6,200  │ 4,82,000 │
  │  2  │ Unacademy AP (TSP-0054)          │   22,100 │  5,100  │ 3,64,200 │
  │  3  │ AV College, Hyderabad (INST-312) │    8,200 │  3,400  │ 1,18,600 │
  │  4  │ Narayana IAS Academy (TSP-0221)  │    6,800 │  2,200  │   94,200 │
  │  5  │ Sri Chaitanya Competitive (INST) │    4,100 │  1,600  │   62,400 │
  ├─────┴──────────────────────────────────┼──────────┼─────────┼──────────┤
  │  TOTAL (5 licensees)                   │   69,600 │ 18,500  │11,21,400 │
  └────────────────────────────────────────┴──────────┴─────────┴──────────┘

  [i] New licensee this month: Sri Chaitanya Competitive (started 12-Mar-2026)
  [i] Highest per-student usage: AV College (14.5 attempts/student/month)
```

---

## 2. Student Count & Attempt Trends

```
STUDENT & ATTEMPT TREND — Last 6 Months

  Students                                         Attempts (in lakhs)
  80,000 ┤                                          12.0 ┤
  70,000 ┤                          ██ 69,600       10.0 ┤                    ██ 11.21
  60,000 ┤                    ██    ██                8.0 ┤              ██    ██
  50,000 ┤              ██    ██    ██                6.0 ┤        ██    ██    ██
  40,000 ┤        ██    ██    ██    ██                4.0 ┤  ██    ██    ██    ██
  30,000 ┤  ██    ██    ██    ██    ██                2.0 ┤  ██    ██    ██    ██
  20,000 ┤  ██    ██    ██    ██    ██                0.0 ┼──Oct──Dec──Feb──Mar──
  10,000 ┤  ██    ██    ██    ██    ██
       0 ┼──Oct───Dec───Feb───Mar───

   Oct    Nov    Dec    Jan    Feb    Mar
  32,400 38,100 44,200 52,800 61,500 69,600  ← Unique students
  3.84L  4.62L  5.88L  7.14L  9.02L 11.21L  ← Total attempts

  Avg. Attempts per Student: 16.1 (Mar) vs 11.8 (Oct) — engagement deepening
```

---

## 3. Geographic Distribution

```
GEOGRAPHIC DISTRIBUTION OF CONTENT USAGE — March 2026

  ┌──────────────────────────────────────────────────────────────────────┐
  │  STATE / REGION              │ Students │ % Share │ Top Exam         │
  ├──────────────────────────────┼──────────┼─────────┼──────────────────┤
  │  Andhra Pradesh              │   24,200 │  34.8%  │ APPSC Group 2    │
  │  Telangana                   │   21,600 │  31.0%  │ TSPSC Group 1    │
  │  Delhi NCR                   │    8,400 │  12.1%  │ SSC CGL          │
  │  Karnataka                   │    5,200 │   7.5%  │ KAS Prelims      │
  │  Uttar Pradesh               │    4,800 │   6.9%  │ SSC CGL          │
  │  Maharashtra                 │    3,100 │   4.5%  │ IBPS PO          │
  │  Other (12 states)           │    2,300 │   3.3%  │ Various          │
  ├──────────────────────────────┼──────────┼─────────┼──────────────────┤
  │  TOTAL                       │   69,600 │ 100.0%  │                  │
  └──────────────────────────────┴──────────┴─────────┴──────────────────┘

  Insight: AP + Telangana = 65.8% of usage — content is strongest for
  state PSC exams. SSC/IBPS content gaining traction in North India.
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/content-partner/revenue/usage/licensees/?month=2026-03` | List TSPs/institutions using partner's content with student and attempt counts |
| 2 | `GET` | `/api/v1/content-partner/revenue/usage/trends/?months=6` | Student count and attempt trends over specified period |
| 3 | `GET` | `/api/v1/content-partner/revenue/usage/geography/?month=2026-03` | Geographic distribution of content usage by state |
| 4 | `GET` | `/api/v1/content-partner/revenue/usage/questions/?month=2026-03&sort=-attempts&limit=50` | Per-question usage statistics sorted by attempts |
| 5 | `GET` | `/api/v1/content-partner/revenue/usage/licensees/{tsp_id}/detail/?month=2026-03` | Detailed usage breakdown for a specific TSP or institution |

---

## 5. Business Rules

- Usage analytics are computed from the content-usage pipeline that ingests attempt events from the mock test engine and practice modules; each event records the student ID, question ID, TSP/institution ID, timestamp, and geographic region (derived from the student's registered address, not IP geolocation, because VPN usage among aspirants is common and IP-based location would be unreliable); the pipeline aggregates these events nightly into a per-partner usage summary table, and the analytics page reads from this aggregated table rather than querying raw events, ensuring that Dr. Venkat Rao's dashboard for 11.21 lakh attempts loads in under 3 seconds rather than scanning millions of raw event rows.

- The TSP/institution breakdown is critical because it lets the partner understand which licensees drive the most revenue and whether their content is reaching new markets; when a new licensee starts using the partner's content (such as Sri Chaitanya Competitive starting on 12-Mar-2026), the system generates a notification to the partner; however, the system never reveals the licensing terms between EduForge and the TSP (such as the per-student fee the TSP pays to EduForge) because those are confidential B2B agreements; the partner only sees their own revenue share calculated at the agreed rate of Rs. 0.02 per student per question per month, never the upstream pricing.

- Geographic distribution data helps partners make informed decisions about content strategy; if Dr. Venkat Rao sees that 65.8% of his usage comes from AP and Telangana for state PSC exams, he may choose to double down on APPSC/TSPSC content, or conversely invest in SSC/IBPS content where his 12.1% Delhi NCR share suggests growth potential; the geographic data is aggregated at the state level and never reveals individual student identities or institutional enrolment numbers below the aggregate level; EduForge's privacy policy prohibits sharing student-level data with content partners, and the analytics pipeline enforces this by only exposing counts above a minimum threshold of 50 students per dimension to prevent re-identification in small institutions.

- The per-question usage statistics (accessible via the questions endpoint) allow partners to identify which specific questions are high-performers and which are unused; a question that has zero attempts in 3 consecutive months is flagged with a "low traction" label, suggesting the partner review it for quality, relevance, or tagging issues; conversely, questions with extremely high attempt counts (such as Q-28471 with 1,24,000 attempts) indicate foundational topics that aspirants practise repeatedly, and the partner can use this insight to create variant questions on the same topic to increase their question pool's depth without reducing quality.

---

*Last updated: 2026-03-31 · Group 9 — B2B Content Partner Portal · Division D*
