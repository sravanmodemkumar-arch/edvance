# P-22 — Branch Quality Ranking

> **URL:** `/group/audit/rankings/`
> **File:** `p-22-branch-quality-ranking.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Compliance Data Analyst (Role 127, G1) — primary operator

---

## 1. Purpose

The Branch Quality Ranking page produces the official quality league table for the Institution Group — a single, authoritative ranking of all branches from best to worst on overall compliance quality and across each of the six audit dimensions. This ranking is a governance tool, a motivational tool, and a resource allocation tool simultaneously.

As a governance tool, it answers the question CEOs and Chairmen ask at every management meeting: "Which are our best branches and which are our problem branches?" A ranked list with scores makes this answer unambiguous — no more subjective impressions, no more principals defending their branch with anecdotes. The data decides.

As a motivational tool, public ranking within the group drives healthy competition. Principals care about their ranking relative to peers. A branch that moves from rank 22 to rank 15 has something to celebrate. A branch that drops from rank 5 to rank 12 has something to explain at the next principals' meeting. Indian education institutions respond well to public recognition — the Best Compliance Branch award at the annual principals' conference, supported by this ranking, creates genuine improvement incentives.

As a resource allocation tool, the ranking directs audit intensity toward the bottom quartile — branches ranked 22–28 get more inspection visits, faster CAPA follow-up, and BIP consideration before they fall into crisis.

The problems this page solves:

1. **Relative standing invisibility:** A branch with a compliance score of 74% doesn't know if that's good or bad relative to its peers. The ranking provides immediate context — rank 4 of 28 is excellent; rank 24 of 28 demands attention.

2. **Dimension-specific ranking ignored:** A branch might rank 5th overall but rank 25th for safety. This masked weakness needs surfacing. The dimension-specific rankings let each branch understand exactly where they are weakest relative to peers.

3. **Ranking volatility and trend:** A branch that has moved from rank 18 to rank 8 over three quarters is a success story worth recognising. A branch that has dropped from rank 3 to rank 17 is a deterioration story worth investigating. Rank movement is as important as absolute rank.

4. **Institution-type unfairness in comparison:** Comparing a residential school (with 24/7 operations, hostel safety, food hygiene) to a day coaching centre on the same rubric is unfair. The ranking supports institution-type-specific league tables so branches are compared to true peers when needed.

**Scale:** 5–50 branches · 6 dimensions · Overall + dimension-specific rankings · Quarterly updates · Recognition system integration

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Compliance Data Analyst | 127 | G1 | Full — view all rankings, configure weights, export | Primary operator |
| Group Internal Audit Head | 121 | G1 | Read all — rankings inform audit resource allocation | Oversight |
| Group Process Improvement Coordinator | 128 | G3 | Read — use ranking to prioritise BIP initiation | Operational |
| Zone Director | — | G4 | Read — group ranking + own zone detail | Zone |
| Branch Principal | — | G3 | Read — own branch rank + peer comparison (institution type) | Competitive awareness |
| Group CEO / Chairman | — | G4/G5 | Read all + Recognition trigger | Executive |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Branch principals see their own rank and the institution-type peer table only — not all 28 branches in full. G1+ see all branches.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Branch Quality Ranking
```

### 3.2 Page Header
```
Branch Quality Ranking                          [Publish Rankings]  [Generate Certificates]  [Export]
Compliance Data Analyst — P. Sunitha
Sunrise Education Group · 28 branches · Last ranked: Q3 FY 2025-26 · Next ranking: Q4 FY 2025-26 (due 05-Apr-2026)
```

### 3.3 Filter Bar
```
Period: [Q3 FY 2025-26 ▼]    View: [Overall ▼]  [By Dimension]  [By Institution Type]
Institution Type: [All / School / Coaching / Hostel / College ▼]
Zone: [All / Zone 1 / Zone 2 / Zone 3 ▼]
                                                                    [Compare Periods]
```

---

## 4. Page Sections

### Section 1 — Overall Rankings

**Top 3 Podium (visual highlight at top):**

```
              ┌──────────┐
         ┌────┤  🥇 #1   ├────┐
         │    │Sunrise   │    │
    ┌────┤    │HITEC City│    ├────┐
    │ #2 │    │  97%     │    │ #3 │
    │    │    │          │    │    │
    │    │    └──────────┘    │    │
    │    │                   │    │
  Sunrise│                 Sunrise│
Jubilee  │                 Banjara│
  Hills  │                  Hills │
  94%    │                   91%  │
    └────┘                   └────┘
```

**Full Rankings Table:**

| Rank | Movement | Branch | Zone | Type | Score | Band | Financial | Academic | Safety | Affiliation | CAPA | Grievance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | → | Sunrise HITEC City | Z1 | Coaching | 97% | A+ | 98% | 99% | 95% | 100% | 96% | 94% |
| 2 | ↑2 | Sunrise Jubilee Hills | Z1 | School | 94% | A+ | 92% | 97% | 91% | 98% | 93% | 91% |
| 3 | ↑1 | Sunrise Banjara Hills | Z2 | School | 91% | A | 89% | 94% | 88% | 95% | 91% | 88% |
| … | | … | | | | | | | | | | |
| 26 | ↓3 | Sunrise Ameerpet | Z3 | Coaching | 55% | C | 61% | 68% | 42% | 72% | 38% | 55% |
| 27 | ↓2 | Sunrise KPHB | Z2 | School | 57% | C | 58% | 71% | 45% | 75% | 44% | 51% |
| 28 | ↑1 | Sunrise Miyapur | Z1 | School | 55% | C | 55% | 69% | 48% | 74% | 51% | 62% |

**Column: Movement**
- ↑N = moved up N ranks vs prior period (green)
- ↓N = dropped N ranks (red)
- → = same rank (neutral)
- NEW = first ranking for this branch

**Row colour coding:**
- Rank 1–3: Gold/silver/bronze tint
- Band A+ (≥ 95%): Light green row
- Band C/D (< 70%): Light red row

**Cell colour per dimension score:**
- ≥ 85%: Green
- 70–84%: Amber
- < 70%: Red
- Lowest value in each column: Bold red — identifies the worst performer per dimension

**Row click:** Opens Branch Rank Detail Drawer.

---

### Section 2 — Dimension-Specific Rankings

**Tab selector:** [Financial] [Academic] [Safety] [Affiliation] [CAPA Closure] [Grievance]

Per-dimension ranking table — same structure as overall but sorted by that dimension's score.

**Why this matters:** The Safety dimension ranking shows which branches are most at risk from a safety perspective — the overall ranking might mask a branch that scores well on financial and academic but is dangerously low on safety.

**Safety ranking example:**
| Rank | Branch | Safety Score | Movement | Key Issues |
|---|---|---|---|---|
| 1 | Sunrise HITEC City | 95% | → | — |
| ... | | | | |
| 26 | Sunrise Ameerpet | 42% | ↓2 | Fire exit non-compliant, CCTV gaps, pending NOC |
| 27 | Sunrise KPHB | 45% | ↓1 | Playground safety, broken handrail |
| 28 | Sunrise Miyapur | 48% | ↑1 | Improving — 3 actions completed |

---

### Section 3 — Zone Rankings

One card per zone showing zone aggregate and internal ranking.

**Zone card:**
```
┌─────────────────────────────────────────────────┐
│  Zone 1  ·  9 branches  ·  Avg score: 82.4%    │
│  Zone rank: 2nd of 3 zones                      │
│                                                  │
│  Best branch: Sunrise HITEC City (97%)           │
│  Weakest branch: Sunrise Miyapur (55%)           │
│  Improving branches: 7 / 9                       │
│  On BIP: 2 branches                             │
│                                                  │
│  [View Zone Detail]                              │
└─────────────────────────────────────────────────┘
```

---

### Section 4 — Institution-Type Peer Ranking

Separate ranking tables for:
- Schools (Day) — N branches
- Coaching Institutes — N branches
- Residential Schools / Hostels — N branches
- Junior Colleges — N branches (if applicable)

Branches are ranked within their type. This is the "fair" comparison for principals — a residential school principal is compared to other residential school principals, not coaching institutes with lighter compliance requirements.

**Note displayed:** "Overall ranking (Section 1) uses the same scoring methodology across all institution types. Peer rankings (this section) compare branches to same-type peers only."

---

### Section 5 — Rank Movement Analysis

Who moved the most this quarter?

**Most Improved (Top 5):**
| Branch | Prior Rank | Current Rank | Change | Key Driver |
|---|---|---|---|---|
| Sunrise Begumpet | 22 | 14 | +8 ↑ | BIP successfully on track; 6 CAPAs closed |
| Sunrise Ameerpet was 20 → 24 | — | — | — | — |

**Most Declined (Bottom 5):**
| Branch | Prior Rank | Current Rank | Change | Key Driver |
|---|---|---|---|---|
| Sunrise Ameerpet | 23 | 26 | −3 ↓ | BIP off track; safety score fell further |

**`[Recognise Most Improved]`** → Triggers recognition notification to branch principal + CEO.

---

### Section 6 — Recognition Panel

Tracking of formal recognitions triggered from the ranking system.

**Types of recognition:**
- 🥇 Best Compliance Branch — Quarterly (Rank #1)
- 🏆 Most Improved Branch — Quarterly (largest rank improvement)
- ⭐ Zero-Defect Branch — Branch with 100% CAPA closure rate for the quarter
- 🎖️ Annual Compliance Excellence Award — Annual ranking

**Recognition history table:**

| Award | Branch | Period | Notified | Certificate |
|---|---|---|---|---|
| Best Compliance Branch Q3 | Sunrise HITEC City | Q3 FY 2025-26 | ✅ 10-Jan-2026 | 📄 Download |
| Most Improved Q3 | Sunrise Begumpet | Q3 FY 2025-26 | ✅ 10-Jan-2026 | 📄 Download |

**`[Generate Certificates]`** → Batch-generates PDF recognition certificates for all Q-period winners.

---

## 5. Drawers & Modals

### Drawer 1 — Branch Rank Detail Drawer (right, 780px)

**Trigger:** Click any branch row.

**Content:**
```
Sunrise Miyapur — Rank 28 of 28 (↑1 from rank 28 of 28 last quarter)
Score: 55%  ·  Band C — At Risk  ·  Zone 1  ·  School

Rank History:
Q1: 28 (55%) → Q2: 28 (48%) → Q3: 28 (55%)
Trend: Improving (+7 pts) but still in Band C

Dimension Scores:
  Financial:    55%  Rank 27/28  ↑2
  Academic:     69%  Rank 21/28  ↑3
  Safety:       48%  Rank 28/28  → (consistently last)
  Affiliation:  74%  Rank 18/28  ↑4
  CAPA Closure: 51%  Rank 26/28  ↑2
  Grievance:    62%  Rank 22/28  ↑1

Active Improvement Plan: BIP-2026-004 (Delayed)
Open CAPA Items: 9
Critical Open: 1 (POCSO — under investigation)
Last Inspection: 10-Mar-2026 (Score: 58%)
Next Inspection: Scheduled 25-Jun-2026

Peer Comparison (Same-type school peers — 14 branches):
  Overall rank: 14/14 (last in peer group)
  Strongest peer dimension: Affiliation (rank 9/14)
  Weakest vs peer: Safety (rank 14/14)
```

**Actions:**
```
[View Full CAPA Register]  [View BIP]  [Schedule Inspection]  [Raise Concern to CEO]
```

---

### Modal 1 — Publish Rankings

**Trigger:** `[Publish Rankings]` button.

Publishing makes rankings visible to Branch Principals (who can only see their own rank and peer table) and Zone Directors (who see their zone).

**Form:**
```
Publish Rankings — Q3 FY 2025-26

This will make rankings visible to:
  ✅ Branch Principals (own rank + peer table only)
  ✅ Zone Directors (own zone full detail)
  ✅ CEO / Chairman (full group ranking)

Notify via:
  ☑ Platform notification to each Branch Principal (auto: "Your branch ranked X of Y in Q3")
  ☑ Email to Zone Directors with zone summary
  ☑ Email to CEO with full ranking PDF attached

Publish Date: [Today ▼]

⚠️ Once published, rankings cannot be recalled without CEO approval.
```

**Actions:** `[Publish]` `[Cancel]`

---

### Modal 2 — Generate Recognition Certificates

**Form:**
```
Generate Certificates for Q3 FY 2025-26

Awards to generate:
  ☑ Best Compliance Branch — Sunrise HITEC City (Rank #1, Score 97%)
  ☑ Most Improved Branch — Sunrise Begumpet (+8 ranks)
  ☑ Zero-Defect CAPA Branch — Sunrise Jubilee Hills (100% CAPA closure)

Certificate template: [Group Letterhead + Chairman signature ▼]
Format: PDF (A4, landscape)

Send to:
  ☑ Branch Principal (email)
  ☑ CEO (cc)
  ☑ Group HR (for recognition records)
```

**Actions:** `[Generate & Send]` `[Generate Only]` `[Cancel]`

---

## 6. Weight Configuration

**Only G4/G5 can modify. Located under Settings → Audit → Scoring Weights.**

Current weights (visible on this page as reference):

| Dimension | Weight | Justification |
|---|---|---|
| Financial Compliance | 20% | Protects institutional financial health; audit accountability |
| Academic Quality | 25% | Core educational mission; highest weight |
| Safety & Infrastructure | 20% | Legal risk; student safety; CBSE affiliation risk |
| Affiliation Compliance | 15% | Regulatory must-have; loss = catastrophic |
| CAPA Closure Rate | 10% | Measures responsiveness to audit findings |
| Grievance Resolution | 10% | Student/parent satisfaction and legal risk |
| **Total** | **100%** | |

---

## 7. Charts

### Chart 1 — Score Distribution (box plot or violin)
- **Type:** Box plot per institution type (Chart.js 4.x or D3.js)
- **X-axis:** Institution types
- **Y-axis:** Score (0–100%)
- **Shows:** Median, quartiles, range, outliers
- **Purpose:** Reveals whether variance is within institution type or across types
- **API:** `GET /api/v1/group/{id}/audit/rankings/charts/distribution/`

### Chart 2 — Rank Movement Bubble (bubble chart)
- **Type:** Bubble chart (Chart.js 4.x)
- **X-axis:** Current rank
- **Y-axis:** Score
- **Bubble size:** Magnitude of rank change (larger = bigger movement)
- **Colour:** Green = improved rank · Red = declined rank · Grey = no change
- **API:** `GET /api/v1/group/{id}/audit/rankings/charts/movement/`

### Chart 3 — Dimension Radar — Group Average
- **Type:** Radar (Chart.js 4.x)
- **Axes:** 6 dimensions
- **Series:** Current quarter (blue) + prior quarter (dashed grey)
- **Purpose:** Shows where the whole group improved or declined per dimension
- **API:** `GET /api/v1/group/{id}/audit/rankings/charts/dimension-radar/`

### Chart 4 — Zone Comparison Bar
- **Type:** Grouped horizontal bar (Chart.js 4.x)
- **X-axis:** Score
- **Y-axis:** Zones
- **Groups:** 6 dimensions per zone
- **API:** `GET /api/v1/group/{id}/audit/rankings/charts/zone-comparison/`

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Rankings computed | "Q3 FY 2025-26 rankings computed — 28 branches · 6 dimensions" | Success (green) |
| Rankings published | "Q3 rankings published — Branch Principals and Zone Directors notified" | Success (green) |
| Certificates generated | "3 recognition certificates generated — Q3 FY 2025-26" | Success (green) |
| Recognition sent | "Most Improved Branch certificate sent to Sunrise Begumpet Principal + CEO" | Success (green) |
| Rank drop alert | "⚠️ Sunrise Ameerpet dropped 3 ranks this quarter — CEO has been notified" | Warning (amber) |
| Export complete | "Branch Quality Ranking report exported — Q3 FY 2025-26 · PDF" | Success (green) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No rankings computed | League table outline | "Rankings not yet computed for this period. Rankings are generated after compliance scores are updated." | `[Compute Rankings]` |
| No prior period data | Chart with single point | "Prior period data not available — ranking movement cannot be calculated for the first period." | — |
| Filter returns zero | Magnifying glass | "No branches match your filters." | `[Reset Filters]` |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Ranking computation | Progress bar: "Computing rankings for 28 branches…" | < 5s |
| Full rankings table | Skeleton rows → data | < 1s |
| Dimension-specific tab | Skeleton rows → sorted data | < 500ms |
| Branch rank detail drawer | Drawer skeleton → populated | < 500ms |
| Charts | Grey placeholders → Chart.js | < 500ms each |
| Certificate generation | "Generating certificates… 1/3" progress | 3–10s |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/rankings/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | Latest rankings for current period | G1+ |
| 2 | GET | `/?period={q}` | Rankings for specific period | G1+ |
| 3 | POST | `/compute/` | Trigger ranking computation for period | 127 |
| 4 | POST | `/publish/` | Publish rankings (make visible to principals/zones) | 127, G4+ |
| 5 | GET | `/{branch_id}/` | Branch rank detail + history | G1+ |
| 6 | GET | `/dimension/{dimension}/` | Dimension-specific rankings | G1+ |
| 7 | GET | `/zones/` | Zone-level aggregate rankings | G1+ |
| 8 | GET | `/peer-group/?institution_type={type}` | Institution-type peer ranking | G1+ |
| 9 | GET | `/movement/` | Rank movement analysis (most improved/declined) | G1+ |
| 10 | POST | `/recognitions/generate/` | Generate recognition certificates | 127, G4+ |
| 11 | POST | `/recognitions/send/` | Send certificates to recipients | 127 |
| 12 | GET | `/recognitions/` | Recognition history | G1+ |
| 13 | GET | `/kpis/` | Page-level KPI aggregates | G1+ |
| 14 | GET | `/charts/distribution/` | Chart 1 data | G1+ |
| 15 | GET | `/charts/movement/` | Chart 2 data | G1+ |
| 16 | GET | `/charts/dimension-radar/` | Chart 3 data | G1+ |
| 17 | GET | `/charts/zone-comparison/` | Chart 4 data | G1+ |
| 18 | GET | `/export/` | Export rankings report | G1+ |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Rankings table load | Page load | `hx-get=".../rankings/"` | `#rankings-table` | `innerHTML` | — |
| Dimension tab switch | Tab click | `hx-get=".../rankings/dimension/{dim}/"` | `#rankings-content` | `innerHTML` | — |
| Period change | Dropdown select | `hx-get=".../rankings/?period={q}"` | `#rankings-content` | `innerHTML` | — |
| Branch detail drawer | Row click | `hx-get=".../rankings/{branch_id}/"` | `#right-drawer` | `innerHTML` | 780px |
| Zone comparison | Section scroll | `hx-get=".../rankings/zones/"` | `#zone-section` | `innerHTML` | Lazy load |
| Institution type filter | Dropdown select | `hx-get=".../rankings/peer-group/?type={t}"` | `#peer-table` | `innerHTML` | — |
| Compute rankings | Button click | `hx-post=".../rankings/compute/"` | `#compute-result` | `innerHTML` | Progress + toast |
| Publish modal | Button click | — | `#modal-content` | `innerHTML` | Modal |
| Publish confirm | Form submit | `hx-post=".../rankings/publish/"` | `#publish-result` | `innerHTML` | Toast |
| Generate certs | Form submit | `hx-post=".../rankings/recognitions/generate/"` | `#cert-result` | `innerHTML` | Progress → download |
| Charts load | Section shown | `hx-get` chart endpoints | `#chart-{name}` | `innerHTML` | Chart.js |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
