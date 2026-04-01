# L-06 — Competitor Analysis

> **URL:** `/coaching/marketing/competitors/`
> **File:** `l-06-competitor-analysis.md`
> **Priority:** P3
> **Roles:** Branch Manager (K6) · Director (K7) · Marketing Coordinator (K3)

---

## 1. Competitive Landscape

```
COMPETITOR ANALYSIS — SSC/Banking Coaching — Hyderabad
As of March 2026

  DIRECT COMPETITORS (Hyderabad-based, same segment):
    Name               │ Est. │ Students │ Branches │ Online? │ Key Strength     │ TCC Position
    ───────────────────┼──────┼──────────┼──────────┼─────────┼──────────────────┼──────────────
    Career Launcher    │ 1995 │  ~2,400  │    3     │   Yes   │ Brand, pan-India  │ Differentiate
    Vani Institute     │ 2002 │  ~2,100  │    2     │   No    │ GK specialisation │ Compete
    Hyderabad SSC Hub  │ 2016 │    ~800  │    1     │   No    │ Low price         │ Premium vs.
    EduFirst Hyd       │ 2019 │    ~600  │    1     │   Yes   │ Online-first      │ Hybrid advantage
    R.S. Brothers      │ 2008 │  ~1,200  │    2     │   No    │ Loyalty, local    │ Quality edge
    ───────────────────┴──────┴──────────┴──────────┴─────────┴──────────────────┴──────────────

  ONLINE-ONLY COMPETITORS (national, affect TCC's online enrolments):
    Unacademy:          ~100K students nationally | SSC/banking focus | price competitive
    TestBook:           Test-series-only | ₹499–₹2,499 for mock series (vs TCC ₹3,500)
    PW (Physics Wallah):Growing SSC presence | aggressive pricing | young faculty appeal

  TCC'S POSITION:
    Enrolments (main): 1,840 ↑ vs all local competitors ✅
    Premium segment:   ₹28,000–₹48,000 fee range (above Hyd SSC Hub's ₹18,000)
    Key differentiator: Hostel + test series + physical coaching bundled
```

---

## 2. Feature Comparison

```
FEATURE COMPARISON — TCC vs Top 3 Local Competitors

  Feature                     │ TCC        │ Career Launcher │ Vani Inst. │ Hyd SSC Hub
  ────────────────────────────┼────────────┼─────────────────┼────────────┼─────────────
  SSC CGL coaching            │ ✅         │ ✅              │ ✅         │ ✅
  IBPS PO/Clerk               │ ✅         │ ✅              │ ❌         │ ✅
  Online batch                │ ✅         │ ✅              │ ❌         │ ✅
  Hostel                      │ ✅ (108)   │ ❌              │ ❌         │ ❌
  Mock test series (own)      │ ✅ (28+)   │ ✅ (national)   │ ✅         │ ❌
  Doubt resolution (48h SLA)  │ ✅         │ 🟡 (no SLA)    │ 🟡         │ ❌
  Alumni network (active)     │ ✅ (4,840) │ ✅ (large)      │ 🟡         │ ❌
  Student counsellor (welfare)│ ✅         │ ❌              │ ❌         │ ❌
  Digital ID / certificates   │ ✅         │ ❌              │ ❌         │ ❌
  Avg faculty rating (public) │ 4.2/5.0   │ 4.0/5.0        │ 4.1/5.0   │ 3.7/5.0
  Google rating               │ 4.6/5.0   │ 4.2/5.0        │ 4.3/5.0   │ 3.9/5.0
  Fee range (full course)     │ ₹28K–48K  │ ₹32K–55K       │ ₹22K–38K  │ ₹15K–22K

  TCC ADVANTAGES: Hostel (unique), doubt SLA, counsellor, alumni depth, 4.6 Google rating
  TCC GAPS: Price above Vani/Hyd SSC Hub; no pan-India brand vs Career Launcher
```

---

## 3. Competitive Intelligence

```
COMPETITIVE INTELLIGENCE — Q4 Updates

  RECENT COMPETITOR MOVES:
    Vani Institute (Mar 2026):
      Launched GK booster crash course at ₹4,999 (targeting TCC's non-hostel students)
      Action: Monitor enrollment impact; consider TCC's own GK intensive offering

    EduFirst Hyd (Feb 2026):
      Added live online classes for IBPS Clerk (₹8,999 — undercutting TCC online)
      Action: Review TCC's online IBPS Clerk value proposition; emphasise doubt SLA

    Unacademy (Jan 2026):
      Opened physical centre at Ameerpet (500m from TCC)
      Action: IMPORTANT — monitor closely; potential for student crossover ⚠️
      Response: Emphasise TCC's local reputation, hostel, personalised counselling

  KNOWN STUDENT DROPOUTS TO COMPETITORS (AY 2025–26):
    Switched to Vani:       1 student (GK specialisation preference)
    Switched to Career Launcher: 1 student (relocated to CL branch city)
    Total: 2 — minimal ✅

  SOURCES:
    Google Business Q&A monitoring (weekly)
    Alumni network intelligence (informal)
    New enquiry "where else are you considering?" CRM field
    Public fee lists and syllabi on competitor websites
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/marketing/competitors/` | Competitor database |
| 2 | `POST` | `/api/v1/coaching/{id}/marketing/competitors/` | Add/update competitor |
| 3 | `POST` | `/api/v1/coaching/{id}/marketing/competitors/{cid}/intelligence/` | Log competitive intelligence |
| 4 | `GET` | `/api/v1/coaching/{id}/marketing/competitors/comparison/` | Feature comparison matrix |
| 5 | `GET` | `/api/v1/coaching/{id}/marketing/competitors/alerts/` | Recent competitor moves |

---

## 5. Business Rules

- Competitor intelligence is gathered from public sources only — competitor websites, Google Business profiles, public social media posts, and informal feedback from new enquiries asking "where else are you considering?"; TCC does not engage in any form of corporate espionage (requesting confidential information from competitor employees, impersonating students to attend competitor seminars, etc.); intelligence gathering must be ethical and legal; the CRM field "other centres considered" is disclosed to enquiries as being used for our service improvement
- Competitive analysis informs TCC's positioning strategy but does not drive reactive price cuts; if Hyderabad SSC Hub drops its fee to ₹12,000, TCC does not respond by dropping to ₹25,000 — TCC's premium positioning is based on quality (hostel, doubt SLA, counselling, alumni network) that Hub cannot replicate; price matching would erode margin and signal to the market that TCC's quality is equivalent to the cheapest option; TCC responds to competitor price pressure by communicating its value differential more clearly
- Disparaging competitors by name in TCC's marketing ("Unlike Career Launcher, we answer doubts in 48 hours") is prohibited; the Marketing Guidelines (L-04) explicitly ban competitor disparagement; comparative advertising (implying competitor inferiority without naming them) is permitted only if the comparison is factually accurate and verifiable; "our test series quality is rated higher than the national average" is acceptable if the data supports it; "others don't care about students" is not acceptable — it is subjective and potentially defamatory
- The Unacademy physical centre opening at Ameerpet (500m from TCC) is the most significant competitive threat in 5 years; Unacademy's national brand recognition and digital content library give it an awareness advantage; TCC's response strategy is to double down on its local differentiators (hostel, personalised counselling, Hyderabad-specific exam patterns, alumni success stories from local students); a student choosing between TCC and Unacademy should hear from TCC's alumnus who cleared SSC CGL and is now posted in Hyderabad — that peer proof is what Unacademy cannot replicate locally
- Competitor intelligence reports are shared only with the Branch Manager and Director — not with faculty, students, or staff below K6 level; staff knowing that Unacademy has opened nearby could cause morale anxiety; management communicates competitive developments to staff as "market opportunities" ("the market is growing, more students are considering coaching — our job is to show them why TCC is the best choice") rather than threats; the Director reviews competitive strategy quarterly and adjusts growth targets based on competitive landscape changes

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division L*
