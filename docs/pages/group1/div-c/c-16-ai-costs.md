# C-16 — AI Cost & Usage Monitor

> **Route:** `/engineering/ai-costs/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · AI/ML Engineer (Role 17)
> **Read Access:** DevOps/SRE (Role 14)
> **File:** `c-16-ai-costs.md`
> **Priority:** P2
> **Status:** ⬜ Amendment pending — G15 (Cost Forecast section) · G27 (API Rate Limits section)

---

## 1. Page Name & Route

**Page Name:** AI Cost & Usage Monitor
**Route:** `/engineering/ai-costs/`
**Part-load routes:**
- `/engineering/ai-costs/?part=kpi` — cost health KPI
- `/engineering/ai-costs/?part=daily-spend` — daily spend breakdown
- `/engineering/ai-costs/?part=by-model` — cost by LLM model
- `/engineering/ai-costs/?part=by-domain` — cost by exam domain
- `/engineering/ai-costs/?part=by-type` — cost by question type
- `/engineering/ai-costs/?part=wasted-spend` — rejected question cost analysis
- `/engineering/ai-costs/?part=optimization` — optimization flags panel
- `/engineering/ai-costs/?part=budget-config` — budget configuration

---

## 2. Purpose (Business Objective)

The AI Cost & Usage Monitor provides financial visibility into the platform's LLM API spend — the most variable and potentially unbounded cost item in the infrastructure budget at ₹8L–₹15L per month.

Unlike infrastructure costs (RDS, Lambda) which are relatively predictable, AI API costs scale directly with pipeline throughput. A misconfigured batch job, a runaway retry loop, or a set of prompts with very high output token counts can 2× the monthly bill without any business value added.

This page answers: "Where is our AI money going, is it being spent efficiently, and are we trending toward budget overrun?" It surfaces waste (cost of rejected questions), identifies expensive prompts, and enables hard budget stops before overspend occurs.

**Business goals:**
- Real-time LLM token consumption and cost tracking per model
- Cost attribution by exam domain and question type (which content areas are expensive to generate)
- Waste quantification: cost of rejected questions (money spent generating content that never reached users)
- Hard stop at 95% monthly budget to prevent overrun
- Model cost comparison to guide provider selection decisions

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full view + write: set budgets · configure alerts · enable/disable hard stop |
| AI/ML Engineer (17) | Level 4 | Full view; request budget changes (Admin must approve) |
| DevOps / SRE (14) | Level 4 — Read | View cost summary (for infrastructure cost planning); cannot set budgets |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Budget Status

**Purpose:** Instantly show whether AI spend is within budget or heading toward overrun.

**Budget Status Banner:**

| State | Colour | Text |
|---|---|---|
| ✅ Within budget | Green | "MTD spend: ₹6,84,200 of ₹12,00,000 budget (57%)" |
| ⚠ 80% alert | Amber | "MTD spend: ₹9,84,000 of ₹12,00,000 budget (82%). Projected overspend at current rate." |
| 🚨 Hard stop imminent | Red | "MTD spend: ₹11,41,000 of ₹12,00,000 budget (95%). Hard stop will trigger at 100%." |
| 🚫 Hard stop active | Red pulsing | "AI pipeline HALTED — monthly budget exceeded. No further LLM API calls until next billing cycle." |

**Header elements:**
- H1 "AI Cost & Usage Monitor"
- Budget status banner with percentage progress bar
- Monthly budget display: ₹12,00,000 (click to edit — Admin only)
- "View Pipeline" quick-link → C-15

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Spend Today (est.) | ₹ estimated from token usage today | > daily budget = amber |
| Spend MTD | ₹ month-to-date | > 80% monthly budget = amber |
| Questions Generated MTD | Total count | — |
| Cost per Approved Q (MTD) | ₹ / approved question | > ₹5 = amber (efficiency threshold) |
| Waste % | Cost of rejected Qs / total cost | > 40% = amber |
| Days Until Budget Hit | Projected at current run rate | < 7 days = amber |

**"Days Until Budget Hit" calculation:**
- `(Monthly budget − MTD spend) / (MTD spend / current day of month)`
- Example: MTD spend ₹9,84,000 on day 20 → daily rate ₹49,200 → days remaining in month = 11 → budget remaining = ₹2,16,000 → days until budget hit = 4.4 days → amber alert

---

### Section 3 — Daily Spend Trend Chart

**Purpose:** Visual overview of LLM API spend over time.

**Primary chart:** Bar chart — daily LLM API spend (₹) for last 30 days
- Stacked by model: Claude (blue) · GPT-4o (green) · Gemini (amber)
- Budget line: horizontal red dashed line at daily budget (monthly budget ÷ 30)
- Budget exceeded days: bar shown in red

**Secondary charts:**
- Token consumption chart: input tokens (blue) vs output tokens (red) per day
  - Note: output tokens are ~3–5× more expensive than input tokens on most models
- Questions generated per day (bar) overlaid with approval rate (line — right axis)

**Time range selector:** Last 7 days · Last 30 days · Last 90 days · Custom range

**Comparison toggle:** "Compare with previous period" — overlays same duration from last month

---

### Section 4 — Cost by LLM Model

**Purpose:** Understand relative cost and efficiency across three LLM providers.

**Model Cost Table (MTD):**

| Model | Provider | Input Tokens | Output Tokens | Total Tokens | Cost (₹) | Questions Generated | Approval Rate | Cost per Approved Q |
|---|---|---|---|---|---|---|---|---|
| Claude Sonnet 4.6 | Anthropic | 84.2M | 28.1M | 112.3M | ₹4,84,000 | 42,100 | 74.2% | ₹15.47 |
| GPT-4o | OpenAI | 12.4M | 4.1M | 16.5M | ₹72,000 | 6,200 | 71.8% | ₹16.16 |
| Gemini 1.5 Pro | Google | 8.2M | 2.7M | 10.9M | ₹32,000 | 4,100 | 68.4% | ₹11.40 |
| **Total** | | **104.8M** | **34.9M** | **139.7M** | **₹5,88,000** | **52,400** | **72.8%** | **₹15.39** |

**Model cost per 1M tokens (displayed as reference):**

| Model | Input $/1M | Output $/1M | INR equivalent |
|---|---|---|---|
| Claude Sonnet 4.6 | $3.00 | $15.00 | ₹250 / ₹1,250 per 1M |
| GPT-4o | $2.50 | $10.00 | ₹208 / ₹833 per 1M |
| Gemini 1.5 Pro | $1.25 | $5.00 | ₹104 / ₹417 per 1M |

**Note:** Gemini is cheapest per token but has lowest approval rate. Claude is most expensive but highest quality. GPT-4o is middle ground.

**Model efficiency chart:**
- Scatter plot: cost per approved question (Y) vs approval rate (X) per model
- "Efficient frontier" line: models on the line are optimally balancing cost and quality
- Models above the line are expensive for their quality level

**Actions (Admin):**
- "Adjust model traffic allocation" → link to C-15 LLM Model Tracking Panel
- "Set model spend cap" → per-model monthly budget ceiling (e.g., cap GPT-4o at ₹1,50,000/month)

---

### Section 5 — Cost by Exam Domain

**Purpose:** Understand which content areas are most expensive to generate.

**Domain Cost Table (MTD):**

| Domain | Questions Generated | Approval Rate | Cost (₹) | Cost per Approved Q | Avg Output Tokens/Q | Notes |
|---|---|---|---|---|---|---|
| JEE Advanced (Physics/Chem/Math) | 14,200 | 76.4% | ₹2,14,000 | ₹19.72 | 1,284 | High complexity = more tokens |
| NEET (Biology/Physics/Chem) | 12,800 | 74.1% | ₹1,72,000 | ₹18.09 | 1,120 | |
| UPSC Current Affairs | 4,100 | 62.3% | ₹84,000 | ₹32.84 | 1,840 | High cost — current affairs hard for LLMs |
| Class 10 (CBSE) | 8,400 | 79.2% | ₹84,000 | ₹12.60 | 820 | Simple questions = fewer tokens |
| Class 12 (CBSE) | 6,200 | 77.8% | ₹72,000 | ₹14.93 | 942 | |
| Banking (IBPS/SBI) | 3,200 | 71.2% | ₹42,000 | ₹18.49 | 1,020 | |
| **Total** | **52,400** | **72.8%** | **₹5,88,000** | | | |

**Chart:** Horizontal bar chart — cost per approved question by domain (sorted highest to lowest)
- Benchmark line at ₹15 (target efficiency)
- UPSC at ₹32.84 flagged as above benchmark

**Optimisation insight per domain:**
- High cost domains (> ₹20/question): "Consider: shorter prompt templates · remove few-shot examples · use cheaper model for first-pass with Claude for review-only"
- High rejection rate domains (< 65% approval): "Hallucination more common in this domain. Consider: stricter factual grounding in prompt · add domain-specific few-shot examples"

---

### Section 6 — Cost by Question Type

**Purpose:** Understand cost differences between question formats.

**Question Type Cost Table:**

| Type | Count MTD | Approval Rate | Avg Tokens/Q | Avg Cost/Q | Notes |
|---|---|---|---|---|---|
| MCQ Single (1 correct) | 32,400 | 75.2% | 920 | ₹12.40 | Most common, moderate cost |
| MCQ Multiple (1+ correct) | 8,200 | 71.8% | 1,120 | ₹15.10 | More complex options = more tokens |
| Integer Answer | 4,800 | 68.4% | 1,240 | ₹18.20 | Calculation problems = longer explanations |
| True/False | 3,200 | 81.2% | 480 | ₹6.40 | Simple — cheapest type |
| Assertion-Reason | 2,400 | 63.2% | 1,480 | ₹23.40 | Complex reasoning = most expensive |
| Match the Following | 1,400 | 61.8% | 1,680 | ₹27.60 | Highest token count + low approval |

**Insight:** "Assertion-Reason and Match-the-Following question types have the worst cost/quality profile (high cost + low approval). These two types account for 18% of spend but only 9% of approved questions. Consider reducing these types in pipeline config."

---

### Section 7 — Wasted Spend Analysis

**Purpose:** Quantify the cost of questions that were generated but never reached the question bank — the most actionable cost reduction opportunity.

**Waste Summary (MTD):**

| Category | Questions Rejected | Cost of Rejections | % of Total Spend |
|---|---|---|---|
| Hallucination failures | 6,482 | ₹1,12,000 | 19.1% |
| Duplicate questions | 7,840 | ₹84,000 | 14.3% |
| Format validation failures | 2,184 | ₹24,000 | 4.1% |
| Copyright match | 420 | ₹8,400 | 1.4% |
| Human reviewer rejected | 2,284 | ₹38,000 | 6.5% |
| **Total waste** | **19,210** | **₹2,66,400** | **45.4%** |

**Waste trend chart:** Line chart — waste % per day (last 30 days)
- Target: < 30% waste
- Current: 45.4% (above target)
- Trend: "Improving — was 52% 30 days ago"

**Waste root cause chart:** Donut chart — waste breakdown by rejection reason

**Waste reduction levers:**
- "Duplicate detection quality" — if duplicate rejection > 20%: "Consider increasing duplicate detection threshold or adding more examples to negative-example section of prompt"
- "Hallucination rate" — if > 15%: "Consider adding factual grounding instructions to prompt; use retrieval-augmented generation for factual domains"
- "Format failures" — if > 5%: "Consider adding output format validation example to prompt; check if model version change caused format regression"

---

### Section 8 — Optimization Flags

**Purpose:** Auto-generated actionable recommendations to improve cost efficiency.

**Optimization Recommendations:**

| Priority | Finding | Impact | Recommendation |
|---|---|---|---|
| 🔴 High | UPSC domain: ₹32.84/approved Q (2.1× platform avg) | -₹42,000/month if fixed | Switch UPSC to Gemini 1.5 Pro for first-pass generation; use Claude only for questions that pass hallucination check |
| 🔴 High | Assertion-Reason type: 38.2% waste rate + highest token count | -₹28,000/month if reduced | Reduce Assertion-Reason type from 15% to 5% of job mix |
| 🟡 Medium | 3 batch jobs with output token count > 2,000/question | -₹18,000/month | Review prompts: max_tokens parameter may be too high for these jobs; set to 1,400 |
| 🟡 Medium | GPT-4o error retry cost: 8% of GPT-4o spend is retries | -₹6,000/month | GPT-4o retry budget exhausted more often — investigate network timeout settings |
| 🟢 Low | Night-time batch jobs running at 02:00 IST — no cost benefit | — | No action needed (LLM APIs don't have off-peak pricing) |

**"Apply recommendation" actions:**
- Pre-fills the relevant config change in C-15 (AI Pipeline) or C-10 (if Lambda-related)
- Does not auto-apply — AI/ML Engineer must review and confirm

---

### Section 9 — Budget Configuration

**Purpose:** Set monthly budget, alert thresholds, and hard stop configuration.

**Budget Settings:**

| Setting | Current Value | Editable By |
|---|---|---|
| Monthly AI API Budget (₹) | ₹12,00,000 | Admin only |
| 80% Alert Threshold | ₹9,60,000 (auto-calculated) | Auto |
| 95% Hard Stop Threshold | ₹11,40,000 (auto-calculated) | Auto |
| Hard Stop Enabled | ✅ Yes | Admin only |
| Alert Recipients | Security + AI/ML Engineer | Admin |
| Budget Rollover | No rollover (monthly reset) | Admin |

**Hard stop behaviour:**
- At 95%: Celery AI pipeline workers stop accepting new jobs (existing jobs complete)
- API calls in-flight: allowed to complete (not mid-call stopped)
- New jobs triggered: return error "Monthly AI budget limit approaching. New jobs suspended until next billing cycle."
- Hard stop can be manually lifted by Admin with 2FA + reason (for genuine emergency generation needs)

**Per-model caps:**

| Model | Monthly Cap | Current MTD | Status |
|---|---|---|---|
| Claude (Anthropic) | ₹8,00,000 | ₹4,84,000 | ✅ |
| GPT-4o (OpenAI) | ₹2,00,000 | ₹72,000 | ✅ |
| Gemini (Google) | ₹1,50,000 | ₹32,000 | ✅ |

**Budget alert history:**
- Log of all times 80% threshold was crossed: date · spend at crossing · action taken

**Next month budget planning:**
- "Set next month budget" → date-picker: takes effect on 1st of selected month
- Budget change requires Admin 2FA

---

### Section 10 — Cost per Approved Question Trend

**Purpose:** The single most important efficiency metric — track improvement over time.

**Primary metric:** ₹ cost per approved question (lower = better)

**Chart:** Line chart — cost per approved question (₹) by week (last 12 weeks)

| Period | Cost/Approved Q | Change | Driver |
|---|---|---|---|
| Mar 2026 (MTD) | ₹15.39 | — | Baseline |
| Feb 2026 | ₹17.82 | -13.6% improvement | Prompt v4.2 deployed |
| Jan 2026 | ₹18.94 | -6.0% improvement | Switched NEET to GPT-4o |
| Dec 2025 | ₹22.10 | — | Baseline before optimizations |

**Target line:** ₹12.00 per approved question (platform efficiency goal for FY26-27)

**Decomposition:** Each week point expandable to show: approval rate · model mix · waste % — the three drivers of cost per approved question

---

## 5. User Flow

### Flow A — Month-End Budget Review

1. Platform Admin opens `/engineering/ai-costs/` on the 25th of the month
2. Budget status: 82% (₹9,84,000 of ₹12,00,000) — amber
3. KPI: "Days until budget hit: 4.2 days" (amber)
4. Reviews daily spend chart: spend accelerating in last 5 days (new UPSC domain jobs added)
5. Identifies UPSC domain: ₹32.84/approved Q (red flag)
6. Applies optimization: pauses UPSC generation until next month
7. Projected remaining spend: ₹72,000 over 6 days → total ₹10,56,000 (88% of budget) → safe
8. Sets next month budget to ₹14,00,000 (UPSC domain will be fully active)

### Flow B — Hard Stop Triggered Mid-Month

1. 5 large batch jobs triggered simultaneously by mistake (duplicate job trigger bug)
2. Spend spikes: ₹2,40,000 in 4 hours (normally ₹40,000/day)
3. Hard stop triggers at 95%: ₹11,40,000 reached on day 22
4. All new AI pipeline jobs blocked
5. Platform Admin reviews: sees 5 duplicate jobs from same engineer
6. Admin lifts hard stop with 2FA + reason: "Duplicate jobs — spend was anomalous; genuine remaining need"
7. Sets daily spend cap for remainder of month: ₹20,000/day
8. Celery job throttling applied via max_tokens per job configuration

---

## 6. Component Structure (Logical)

```
AICostMonitorPage
├── PageHeader
│   ├── BudgetStatusBanner (with % progress bar)
│   ├── PageTitle
│   └── BudgetEditButton (Admin)
├── KPIStrip × 6
├── DailySpendTrendChart
│   ├── StackedBarChart (by model)
│   ├── TokenConsumptionChart
│   └── TimeRangeSelector
├── CostByModelSection
│   ├── ModelCostTable
│   ├── ModelRatesReference
│   └── ModelEfficiencyScatterPlot
├── CostByDomainSection
│   ├── DomainCostTable
│   └── CostPerQBarChart
├── CostByQuestionTypeSection
│   └── QuestionTypeCostTable
├── WastedSpendAnalysis
│   ├── WasteSummaryTable
│   ├── WasteTrendChart
│   └── WasteRootCauseDonut
├── OptimizationFlagsPanel
│   └── RecommendationCard × N
├── BudgetConfigSection
│   ├── BudgetSettings
│   ├── PerModelCapsTable
│   └── HardStopControls
└── CostPerApprovedQTrend
    ├── TrendLineChart
    └── DecompositionTable
```

---

## 7. Data Model (High-Level)

### platform_ai_cost_daily (pre-aggregated)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| date | DATE | |
| model | ENUM | claude_sonnet/gpt4o/gemini_pro |
| domain | VARCHAR(100) | |
| question_type | ENUM | |
| input_tokens | BIGINT | |
| output_tokens | BIGINT | |
| questions_generated | INTEGER | |
| questions_approved | INTEGER | |
| questions_rejected | INTEGER | |
| cost_inr | DECIMAL(10,2) | |
| waste_cost_inr | DECIMAL(10,2) | cost of rejected questions |
| created_at | TIMESTAMPTZ | |

### platform_ai_budget_config

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| month | DATE | first day of month |
| total_budget_inr | DECIMAL(10,2) | |
| hard_stop_enabled | BOOLEAN | |
| claude_cap_inr | DECIMAL(10,2) | nullable |
| gpt4o_cap_inr | DECIMAL(10,2) | nullable |
| gemini_cap_inr | DECIMAL(10,2) | nullable |
| alert_80_sent_at | TIMESTAMPTZ | nullable |
| hard_stop_triggered_at | TIMESTAMPTZ | nullable |
| hard_stop_lifted_at | TIMESTAMPTZ | nullable |
| hard_stop_lifted_by | UUID FK → platform_staff | nullable |
| updated_by | UUID FK → platform_staff | |
| updated_at | TIMESTAMPTZ | |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| Monthly budget | Min ₹1,00,000 · Max ₹50,00,000 · Admin only · 2FA required for > 50% change |
| Per-model caps | Sum of all model caps must be ≤ total monthly budget |
| Hard stop | Cannot disable if MTD spend already > 90% of budget (would immediately exceed if disabled) |
| Hard stop lift | Admin only · 2FA · reason min 50 chars · creates audit entry |
| Cost calculation | Cost calculated from token counts × model pricing; pricing table updated quarterly in `platform_ai_model_pricing` table |
| Daily budget (derived) | Monthly ÷ 30; shown as reference; not a hard limit (only monthly budget enforced) |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| API cost data | Derived from token counts logged by Celery workers (not from LLM provider billing APIs) — avoids exposing billing credentials to this page |
| Budget config writes | Admin only · 2FA required for budget changes > 20% |
| Model API key cost | Token pricing table stored in DB (not from LLM provider APIs directly); monthly update by AI/ML Engineer |
| Hard stop | Implemented as Memcached key `platform:ai_hard_stop`; Celery workers check this key before each API call; fall back to DB flag if Memcached unavailable |
| Cost anomaly | If daily spend > 3× daily avg: immediate email to Admin + AI/ML Engineer; C-18 incident created |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| LLM provider changes pricing mid-month | AI/ML Engineer updates pricing table; historical costs already logged are not retroactively changed; forward costs use new pricing |
| Hard stop triggers mid-job | In-progress API calls complete; job marked as "partial — budget stop"; results saved up to stopping point |
| MTD spend jumps 50% in 1 hour (runaway job) | Cost anomaly detection fires; Admin alerted; individual large job can be cancelled from C-15 |
| Two models have very different approval rates (one month) | Dashboard reflects reality; no smoothing; AI/ML Engineer should investigate and adjust model mix |
| Budget config set to 0 (disables all AI generation) | System treats as "pause all generation"; informational banner: "AI generation paused — budget set to ₹0" |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| Cost aggregation | Pre-aggregated daily by Celery beat into `platform_ai_cost_daily`; all chart queries hit this pre-computed table (< 30ms) |
| Real-time MTD spend | Celery workers increment `platform_ai_cost_daily` ORM rows on each completed LLM API call; MTD total aggregated from DB; Memcached 30s TTL for page reads |
| 30-day daily chart | 30 rows × 3 models = 90 rows from `platform_ai_cost_daily`; trivial query |
| Optimization flags | Computed by Celery beat weekly; stored as JSONB in `platform_ai_optimization_flags` table; page reads from cache |
| Hard stop check | Memcached key check by Celery worker: < 1ms; falls back to `platform_ai_budget_config.hard_stop_enabled` DB flag if Memcached unavailable |
| Budget alert emails | Celery beat checks MTD spend against thresholds every 30 min; one-time email per threshold crossing per month |

---

## 12. Amendment — G15: Cost Forecast Section

**Assigned gap:** G15 — C-16 shows historical spend but has no month-end forecast, no "cost if we run N more batches" simulator, and no burn-rate visibility. AI/ML Engineer cannot predict whether the monthly cap will be breached.

**Where it lives:** New section added between Section 10 (Cost per Approved Question Trend) and Section 11 (not present — this becomes Section 11). The page gains this section after the cost trend chart.

---

### Cost Forecast Section

**Purpose:** Project end-of-month LLM API spend based on current burn rate, and allow the AI/ML Engineer to simulate the cost impact of planned batch jobs before triggering them — preventing budget surprises.

**Layout:** Two sub-sections — Month-End Projection · Spend Simulator

---

**Month-End Projection**

Displayed as a card at the top of the section, updated every 30 minutes by Celery beat.

**Projection method:** Simple linear extrapolation from current month-to-date spend and pace:
- Daily burn rate: MTD spend ÷ current day of month
- Projected spend at month end: daily burn rate × days in month
- Remaining budget: monthly budget − MTD spend
- Projected overrun: MAX(0, projected spend − monthly budget)
- Days until budget exhausted: remaining budget ÷ daily burn rate

**Display format:**

| Metric | Value |
|---|---|
| Today (Day 20 of 31) | ₹6,84,200 spent (57% of ₹12,00,000 budget) |
| Daily burn rate (7-day avg) | ₹36,200/day |
| Projected month-end spend | ₹11,22,200 (93.5% of budget) |
| Budget remaining | ₹3,15,800 |
| Days until budget exhausted | ~8.7 days at current rate |
| Projected hard stop | Day 29 (2 days before month end) |

**Visual:** Horizontal progress bar showing: MTD spend · projected remaining · headroom to hard stop · hard stop line.

**Forecast accuracy indicator:** "Projection based on last 7-day burn rate. Actual may vary with job scheduling."

**Trend alerts:**
- If projected month-end > 95%: amber — "Projected to hit hard stop before month end. Reduce job volume or request budget increase."
- If projected month-end > 100%: red — "Projected to exceed budget by ₹{overrun}. Immediate action required."

**Burn rate chart:**
- Line chart: daily burn rate (7-day rolling average) over last 30 days
- Horizontal line: required burn rate to stay within budget (monthly budget ÷ 31)
- Shows visually if spend is accelerating (rising line) or decelerating (falling line)

---

**Spend Simulator**

"What happens if I run more jobs this month?" tool.

**Simulator inputs:**

| Input | Description |
|---|---|
| Number of additional questions | Slider: 1,000 – 500,000 |
| Model mix | Slider: Claude % / GPT-4o % / Gemini % (must sum to 100%) |
| Expected approval rate | Slider: 50% – 90% |
| Prompt version | Select from active prompt versions (affects token count estimate) |
| Question type mix | MCQ Single / Multiple / Integer / etc. (affects token count) |

**Outputs (computed instantly from inputs):**

| Output | Estimated Value |
|---|---|
| Additional questions generated | 100,000 |
| Expected approved questions | 72,000 (72% approval rate) |
| Estimated additional tokens | 92M input + 30M output |
| Estimated additional cost | ₹1,24,000 |
| New projected month-end total | ₹8,08,200 (67.4% of budget) |
| Budget remaining after jobs | ₹3,91,800 |
| Within budget? | ✅ Yes — ₹3,91,800 remaining headroom |

**Output colour coding:**
- Green: within budget with > 20% headroom
- Amber: within budget but < 20% headroom
- Red: would exceed budget

**"Trigger these jobs" button:**
- If the simulation result is green, the button becomes active
- Takes AI/ML Engineer to C-15 "Trigger New Job" pre-filled with the simulated config
- Ensures the actual job config matches what was simulated

**Model-Switch Cost Forecast Scenario:**

A dedicated "Model Switch" tab within the Spend Simulator answers: "What would this month cost if I moved all remaining batches to a different model?"

| Input | Description |
|---|---|
| Switch to model | Select: Claude Sonnet 4.6 · GPT-4o · Gemini 1.5 Pro · Gemini 1.5 Flash |
| Switch from (day N) | Which day of the month to switch (default: today) |

Outputs (compared against current model mix):

| Output | Current Mix | If 100% Claude | If 100% GPT-4o | If 100% Gemini Flash |
|---|---|---|---|---|
| Remaining month spend | ₹3,15,800 | ₹3,28,000 | ₹2,86,000 | ₹1,72,000 |
| Month-end total | ₹9,99,800 | ₹10,12,200 | ₹9,70,200 | ₹8,56,200 |
| Budget impact vs current | baseline | +₹12,400 | −₹29,600 | −₹1,43,600 |
| Within ₹12L budget? | ✅ | ✅ | ✅ | ✅ |

The table recalculates instantly when the model selection changes. Pricing data sourced from `platform_ai_rate_limit_config` (manually maintained). Note: cheaper models may have different approval rates — a footnote shows "Model quality trade-off: Gemini Flash historically shows 8% lower approval rate for complex domains."

---

## 13. Amendment — G27: API Rate Limits Section

**Assigned gap:** G27 — AI/ML Engineer cannot see current RPM/TPM (requests/tokens per minute) consumption versus quota for Anthropic, OpenAI, or Google providers. Quota exhaustion silently stops the MCQ generation pipeline until discovered manually.

**Where it lives:** New section appended after the Cost Forecast section.

---

### API Rate Limits Section

**Purpose:** Surface real-time LLM API quota consumption for all three providers so the AI/ML Engineer knows how close the pipeline is to being throttled. Rate limit exhaustion causes API 429 errors that slow or stop question generation without any obvious dashboard signal.

**Layout:** One card per provider showing quota health + usage chart

---

**Provider Cards**

Three side-by-side cards (or stacked on mobile), one per LLM provider.

---

**Anthropic (Claude) Card:**

| Metric | Value | Status |
|---|---|---|
| Requests per minute (RPM) | 48 / 60 | 🟡 80% — amber |
| Input tokens per minute (ITPM) | 180,000 / 200,000 | 🟡 90% — amber |
| Output tokens per minute (OTPM) | 58,000 / 80,000 | ✅ 73% |
| Daily token limit (if applicable) | 2.4B / — | — |
| Current queue: Lambda workers waiting | 2 workers rate-limited | ⚠ |

**OpenAI (GPT-4o) Card:**

| Metric | Value | Status |
|---|---|---|
| Requests per minute (RPM) | 12 / 500 | ✅ 2% |
| Tokens per minute (TPM) | 84,000 / 800,000 | ✅ 10% |
| Current queue | 0 workers rate-limited | ✅ |

**Google (Gemini) Card:**

| Metric | Value | Status |
|---|---|---|
| Requests per minute (RPM) | 8 / 60 | ✅ 13% |
| Tokens per minute (TPM) | 42,000 / 300,000 | ✅ 14% |
| Current queue | 0 workers rate-limited | ✅ |

**Card colour coding:**
- Green: < 70% quota used
- Amber: 70–89% quota used
- Red: ≥ 90% quota used — "Rate limit pressure: pipeline may be throttled"

---

**Rate Limit Charts:**

For each provider: sparkline chart of RPM/TPM usage over the last 60 minutes (1-minute buckets). Shows spikes (batch job bursts) and throttling events (usage drops suddenly due to 429 responses from provider).

**429 error history (last 24h):**

| Time | Provider | Error Type | Duration of Throttling | Jobs Affected |
|---|---|---|---|---|
| 2h ago | Anthropic | RPM limit | 4 min | job-abc123 |
| 6h ago | Anthropic | ITPM limit | 8 min | job-def456 |

Throttling events are identified from Celery worker 429 error logs.

**Auto-pause configuration:**

When a provider's RPM or TPM usage exceeds 95% of quota, the pipeline can be configured to auto-pause new API calls to that provider rather than generate 429 errors:

| Provider | Auto-pause enabled | Auto-pause threshold | Fallback model on pause |
|---|---|---|---|
| Anthropic | ✅ Yes | 95% | GPT-4o |
| OpenAI | ✅ Yes | 95% | Gemini |
| Google | ✅ Yes | 95% | Anthropic (if recovered) |

"Edit auto-pause config" → allows AI/ML Engineer to toggle per-provider auto-pause and adjust threshold.

**Quota reset countdown:**

LLM provider quotas operate on rolling 1-minute windows. Each provider card shows:
- "Quota window resets in: **{N}s**" — countdown timer, updated every second via JavaScript
- Calculated as: 60 − (current_second % 60) seconds until next minute boundary
- Useful when rate-limited: shows exactly how long until the next burst of calls can be made
- During throttling (red state): countdown is displayed prominently so engineers know when to retry

**Provider API Status:**

Below the three provider cards, a "Provider API Health" row shows the current operational status of each provider's API, sourced from provider status pages polled by a Celery beat task every 5 minutes:

| Provider | Status | Last Checked |
|---|---|---|
| Anthropic (status.anthropic.com) | ✅ Operational | 3 min ago |
| OpenAI (status.openai.com) | ✅ Operational | 3 min ago |
| Google Cloud (status.cloud.google.com) | ⚠ Degraded — Vertex AI latency elevated | 3 min ago |

Status values: **Operational** (green) · **Degraded** (amber) · **Outage** (red) · **Unknown** (grey, if status page unreachable)

When a provider shows Degraded or Outage: amber/red banner appears above that provider's card — "Provider API degraded — pipeline may experience higher latency or failures."

Data model: `platform_ai_provider_status`

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| provider | ENUM | anthropic/openai/google |
| status | ENUM | operational/degraded/outage/unknown |
| status_description | TEXT | message from provider status page |
| checked_at | TIMESTAMPTZ | |

Celery beat task: `portal.tasks.ai_monitoring.refresh_provider_status` — runs every 5 minutes, fetches provider status page JSON APIs, upserts `platform_ai_provider_status`. Result shown via HTMX poll on `/engineering/ai-costs/?part=provider-status` every 60s.

**Quota limits configuration:**

Provider quotas are not fetched from provider APIs (no native quota API in all providers). They are configured manually:
- "Update quota limits" → simple form: RPM · TPM · OTPM per provider
- AI/ML Engineer updates these after receiving new quota from provider account team
- Stored in `platform_ai_rate_limit_config` table
- Last updated timestamp shown per provider

**Data source for current usage:**
- RPM/TPM metrics: aggregated from Celery worker API call logs (timestamp + token counts logged per API call)
- Aggregated every 60 seconds by Celery beat into `platform_ai_rate_limit_stats` (minute-level rolling window)
- Page polls every 30 seconds via HTMX for near-real-time view

**Data model:**

**platform_ai_rate_limit_config**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| provider | ENUM | anthropic/openai/google |
| rpm_limit | INTEGER | |
| itpm_limit | INTEGER | nullable (input tokens per minute) |
| otpm_limit | INTEGER | nullable (output tokens per minute) |
| auto_pause_enabled | BOOLEAN | |
| auto_pause_threshold_pct | SMALLINT | 50–99 |
| fallback_provider | ENUM | nullable |
| updated_by | UUID FK → platform_staff | |
| updated_at | TIMESTAMPTZ | |

**platform_ai_rate_limit_stats**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| provider | ENUM | |
| minute_bucket | TIMESTAMPTZ | truncated to minute |
| requests_count | INTEGER | |
| input_tokens | INTEGER | |
| output_tokens | INTEGER | |
| throttle_events | INTEGER | count of 429 errors in this minute |
