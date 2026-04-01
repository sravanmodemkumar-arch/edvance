# Division K — Sales & Business Development: Pages List & Architecture

> EduForge platform-level Sales & Business Development covering 2,050 education institutions across 4 segments.
> 10 roles total (IDs 57–63 + 95–97) handling lead pipeline, demo management, partnerships, channel partners, and quota tracking.
> Division K owns new revenue generation from first contact through signed contract handoff to Division I (Onboarding) and Division J (Customer Success).

---

## Scale Context

| Segment | Count | ARR Range / Institution | Total ARR Range | Avg Sales Cycle |
|---|---|---|---|---|
| Schools | 1,000 | ₹60K–₹2.4L | ₹6Cr–₹24Cr | 3–8 weeks |
| Colleges | 800 | ₹40K–₹1.5L | ₹3.2Cr–₹12Cr | 4–12 weeks |
| Coaching Centres | 100 | ₹1.5L–₹6L | ₹1.5Cr–₹6Cr | 2–6 weeks |
| Institution Groups | 150 | ₹2L–₹20L | ₹3Cr–₹30Cr | 8–24 weeks |
| **Total** | **2,050** | — | **~₹13.7Cr–₹72Cr ARR (pipeline + won)** | — |

Lead-to-close conversion target: 30–40% across all segments. Channel partner deals constitute ~20% of new logo volume. Govt/tender contracts (Partnership Manager) represent high-value but long-cycle wins.

---

## Division K Roles

| # | Role | Level | Can Do | Cannot Do |
|---|---|---|---|---|
| 57 | B2B Sales Manager | 3 | Full pipeline visibility all segments; pricing approvals; demo sign-off; bulk reassign; territory config; quota setting; approve channel commissions; manage partnerships; access all reports | Provision tenants directly; modify billing post-close; edit support tickets |
| 58 | Sales Executive — Schools | 3 | Create/edit/stage-move own school leads; log activities; schedule demos; propose ARR; export own leads | View college/coaching/group leads; set quotas; approve commissions; access channel partner financials |
| 59 | Sales Executive — Colleges | 3 | Create/edit/stage-move own college leads; log activities; schedule demos; propose ARR; export own leads | View school/coaching/group leads; set quotas; approve commissions; access channel partner financials |
| 60 | Sales Executive — Coaching | 3 | Create/edit/stage-move own coaching leads; log activities; schedule demos; propose ARR; export own leads | View school/college/group leads; set quotas; approve commissions; access channel partner financials |
| 61 | Partnership Manager | 3 | Full CRUD on `sales_partnership`; MoU upload; negotiate govt/coaching-chain contracts; view pipeline read-only | Stage-move sales leads directly; set exec quotas; access channel partner commissions |
| 62 | Demo Manager | 3 | Full CRUD on `sales_demo_tenant`; request tenant provisioning; load/reset demo data; manage demo seed templates; extend expiry; deactivate expired tenants | Stage-move sales leads; approve pricing; access channel commissions |
| 63 | Channel Partner Manager | 1 | Full CRUD on `sales_channel_partner`; manage `sales_channel_deal` records; view commission ledger; onboard new partners; mark commissions approved | Set exec quotas; approve pricing >₹5L; access partnership MoU docs |
| 95 | Sales Operations Analyst | 1 | Read-only access to entire pipeline, quota attainment, win/loss data, and channel commissions; export all reports; maintain data quality flags; manage `sales_quota` records | No writes to leads or activities; no pipeline stage moves; no approval actions |
| 96 | Pre-Sales / Solutions Engineer | 3 | Technical discovery notes on assigned leads (ARR >₹2L); RFP responses; PoC deployment requests; view product roadmap for pitching; access own assigned leads full detail | View unassigned leads; set pricing; approve commissions; access quota data |
| 97 | Inside Sales Executive | 3 | Create inbound leads (ORGANIC_INBOUND/MARKETING_CAMPAIGN sources); qualify leads; set initial stage; schedule first demo; own PROSPECT→CONTACTED→DEMO_SCHEDULED transitions | Approve pricing; access channel commissions; access partnership tracker; access quota reports |

---

## Page Inventory

| Page | Route | Primary Role | Purpose |
|---|---|---|---|
| K-01 | `/group1/k/dashboard/` | B2B Sales Manager (#57) | Central command view — funnel health, quota attainment, leaderboard, stale leads, upcoming demos |
| K-02 | `/group1/k/pipeline/` | Sales Execs #58–60 + Manager #57 + Inside Sales #97 | Master lead management — create, filter, stage-move, bulk reassign, export |
| K-03 | `/group1/k/account/<lead_id>/` | All sales roles | Full lead/account profile — activities, demo status, proposal history, contact timeline |
| K-04 | `/group1/k/demos/` | Demo Manager (#62) | Demo tenant lifecycle — create, seed data, reset, monitor usage, expire |
| K-05 | `/group1/k/partnerships/` | Partnership Manager (#61) | Partnership tracker — MoU status, contract values, coverage, renewal dates |
| K-06 | `/group1/k/channel-partners/` | Channel Partner Manager (#63) | Channel partner portal — onboarding, deal registration, commission ledger |
| K-07 | `/group1/k/territory/` | B2B Sales Manager (#57) | Territory mapping, quota setting, exec assignment by territory |
| K-08 | `/group1/k/reports/` | Sales Manager #57 + Sales Ops #95 | Full sales analytics — funnel, win/loss, quota attainment, cohort, forecast |

---

## Role-to-Page Access Matrix

| Page | 57 Manager | 58 Schools | 59 Colleges | 60 Coaching | 61 Partnership | 62 Demo | 63 Channel | 95 Ops Analyst | 96 Pre-Sales | 97 Inside Sales |
|---|---|---|---|---|---|---|---|---|---|---|
| K-01 Dashboard | Full all | Own segment | Own segment | Own segment | Read pipeline only | Demo strip only | Channel metrics only | Read-only full | Denied (→K-03) | Own inbound queue |
| K-02 Pipeline | Full all + bulk | Own school leads | Own college leads | Own coaching leads | Read-only | Read-only (demo status) | Channel deals only | Read-only all | Assigned leads only | Own inbound leads |
| K-03 Account Profile | Full all | Own leads full | Own leads full | Own leads full | Read + partnership tab | Demo tab full | Channel tab read | Read all tabs | Assigned leads — tech tabs | Own leads full |
| K-04 Demos | Read + approve | Read own demos | Read own demos | Read own demos | No access | Full CRUD | No access | Read-only | Read PoC demos | Schedule only |
| K-05 Partnerships | Full | No access | No access | No access | Full CRUD | No access | No access | Read-only | No access | No access |
| K-06 Channel Partners | Full + approve commissions | No access | No access | No access | No access | No access | Full CRUD | Read-only | No access | No access |
| K-07 Territory & Quota | Full CRUD | View own quota | View own quota | View own quota | No access | No access | No access | Read-only all | No access | View own quota |
| K-08 Reports | Full all sections | Own performance only | Own performance only | Own performance only | Partnership metrics only | Demo metrics only | Channel metrics only | Full all + export | No access | Own conversion metrics |

---

## Data Model

### `sales_lead`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| institution_name | varchar(300) | NOT NULL; min 3 chars enforced in application |
| institution_type | varchar(20) | NOT NULL; enum `SCHOOL` · `COLLEGE` · `COACHING` · `GROUP` |
| segment_size | varchar(20) | NOT NULL; enum `MICRO` (<100 students) · `SMALL` (100–500) · `MEDIUM` (500–2000) · `LARGE` (2000–10000) · `ENTERPRISE` (>10000) |
| stage | varchar(20) | NOT NULL DEFAULT `PROSPECT`; enum `PROSPECT` · `CONTACTED` · `DEMO_SCHEDULED` · `DEMO_DONE` · `PROPOSAL_SENT` · `NEGOTIATION` · `CLOSED_WON` · `CLOSED_LOST` |
| owner_id | int | FK → auth_user NOT NULL; the exec responsible for this lead |
| manager_id | int | FK → auth_user NOT NULL; Sales Manager overseeing this lead |
| presales_id | int | FK → auth_user NULLABLE; Pre-Sales Engineer (#96) assigned for ARR > ₹2L leads |
| lead_source | varchar(30) | NOT NULL; enum `ORGANIC_INBOUND` · `REFERRAL` · `CHANNEL_PARTNER` · `OUTBOUND_COLD` · `GOVT_TENDER` · `MARKETING_CAMPAIGN` · `CONFERENCE` · `DEMO_TRIAL` |
| territory | varchar(30) | NOT NULL; enum `ANDHRA_PRADESH` · `TELANGANA` · `KARNATAKA` · `MAHARASHTRA` · `RAJASTHAN` · `UP_EAST` · `UP_WEST` · `BIHAR` · `ODISHA` · `MP` · `OTHER_STATE` · `PAN_INDIA` |
| state | varchar(100) | NOT NULL; Indian state name (free text, validated against states list) |
| city | varchar(100) | NOT NULL |
| contact_name | varchar(200) | NOT NULL |
| contact_phone | varchar(15) | NOT NULL; validated ^[6-9]\d{9}$ |
| contact_email | varchar(254) | NULLABLE |
| student_count_estimate | int | NULLABLE; used for ARR auto-calculation |
| arr_estimate_paise | bigint | NOT NULL DEFAULT 0; in paise (₹1 = 100 paise). Application-level constraint: arr_estimate_paise must be > 0 when stage transitions to CLOSED_WON (enforced in Django model clean() method). Allowed to be 0 during early pipeline stages (PROSPECT through NEGOTIATION) — prompts amber warning in UI but does not block form submission. |
| expected_close_date | date | NULLABLE; must be future at creation |
| won_at | timestamptz | Set when stage → CLOSED_WON |
| lost_at | timestamptz | Set when stage → CLOSED_LOST |
| lost_reason | varchar(30) | NULLABLE; enum `PRICE_TOO_HIGH` · `BUDGET_CUT` · `COMPETITOR_WON` · `TIMING_NOT_RIGHT` · `FEATURE_GAP` · `NO_RESPONSE` · `WENT_INHOUSE` · `TENDER_LOST` |
| notes | text | NULLABLE; free-form |
| is_channel_deal | boolean | NOT NULL DEFAULT false |
| channel_partner_id | int | FK → sales_channel_partner NULLABLE; set when is_channel_deal=true |
| created_at | timestamptz | DEFAULT now() |
| updated_at | timestamptz | DEFAULT now() |

**Indexes:**
```sql
CREATE INDEX sales_lead_owner_stage_idx ON sales_lead (owner_id, stage);
CREATE INDEX sales_lead_stage_idx ON sales_lead (stage);
CREATE INDEX sales_lead_territory_idx ON sales_lead (territory);
CREATE INDEX sales_lead_won_at_idx ON sales_lead (won_at) WHERE won_at IS NOT NULL;
CREATE INDEX sales_lead_institution_type_idx ON sales_lead (institution_type);
```

---

### `sales_activity`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| lead_id | int | FK → sales_lead NOT NULL |
| logged_by | int | FK → auth_user NOT NULL |
| activity_type | varchar(20) | NOT NULL; enum `CALL` · `EMAIL` · `MEETING` · `DEMO` · `WHATSAPP` · `SITE_VISIT` · `PROPOSAL` · `RFP_RESPONSE` |
| occurred_at | timestamptz | NOT NULL |
| duration_minutes | smallint | NULLABLE |
| outcome | varchar(20) | NOT NULL; enum `POSITIVE` · `NEUTRAL` · `NEGATIVE` · `NO_SHOW` · `RESCHEDULED` |
| notes | text | NOT NULL; min 10 chars enforced in application |
| next_action | varchar(500) | NULLABLE; free text describing next step |
| next_action_due | date | NULLABLE; surfaced as reminder in K-03 and stale-lead check |
| created_at | timestamptz | DEFAULT now() |

**Indexes:**
```sql
CREATE INDEX sales_activity_lead_idx ON sales_activity (lead_id, occurred_at DESC);
CREATE INDEX sales_activity_logged_by_idx ON sales_activity (logged_by, occurred_at DESC);
```

---

### `sales_demo_tenant`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| lead_id | int | FK → sales_lead NOT NULL |
| tenant_id | int | FK → tenant UNIQUE NOT NULL; provisioned by Platform Admin (#10) via Div-C |
| demo_type | varchar(20) | NOT NULL; enum `STANDARD` · `CUSTOM` · `ENTERPRISE_POC` |
| created_by | int | FK → auth_user NOT NULL; Demo Manager (#62) |
| data_template | varchar(30) | NOT NULL; enum `SCHOOL_DEMO` · `COLLEGE_DEMO` · `COACHING_DEMO` · `BLANK` |
| student_seed_count | smallint | NOT NULL DEFAULT 50; max 500 for ENTERPRISE_POC |
| exam_seed_count | smallint | NOT NULL DEFAULT 5; max 50 for ENTERPRISE_POC |
| created_at | timestamptz | DEFAULT now() |
| expires_at | timestamptz | NOT NULL; default created_at + 14 days; max 60 days for ENTERPRISE_POC |
| last_reset_at | timestamptz | NULLABLE; set each time Demo Manager resets the tenant |
| reset_count | smallint | NOT NULL DEFAULT 0; max resets enforced at application level |
| is_active | boolean | NOT NULL DEFAULT true; set false by Celery Task K-4 on expiry |
| last_login_at | timestamptz | NULLABLE; updated on each tenant login event |
| total_logins | int | NOT NULL DEFAULT 0; incremented on each login event |

---

### `sales_partnership`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| partner_name | varchar(300) | NOT NULL |
| partner_type | varchar(30) | NOT NULL; enum `STATE_BOARD` · `COACHING_CHAIN` · `GOVT_CONTRACT` · `NGO` · `UNIVERSITY_AFFILIATE` · `DISTRICT_AUTHORITY` |
| owner_id | int | FK → auth_user NOT NULL; Partnership Manager (#61) |
| state | varchar(100) | NOT NULL |
| territory | varchar(30) | NOT NULL; same enum as sales_lead.territory |
| status | varchar(20) | NOT NULL DEFAULT `PROSPECTING`; enum `PROSPECTING` · `NEGOTIATION` · `MOU_SIGNED` · `ACTIVE` · `EXPIRED` · `TERMINATED` |
| contract_value_paise | bigint | NULLABLE; total contract value in paise |
| institutions_covered | int | NULLABLE; number of institutions under this partnership |
| mou_s3_path | varchar(500) | NULLABLE; S3 key for signed MoU PDF |
| mou_signed_at | date | NULLABLE |
| mou_expires_at | date | NULLABLE |
| annual_review_date | date | NULLABLE; surfaced as reminder in K-05 |
| notes | text | NULLABLE |
| created_at | timestamptz | DEFAULT now() |
| updated_at | timestamptz | DEFAULT now() |

---

### `sales_channel_partner`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| partner_name | varchar(300) | UNIQUE NOT NULL |
| partner_type | varchar(20) | NOT NULL; enum `RESELLER` · `DISTRIBUTOR` · `AFFILIATE` · `REFERRAL` |
| owner_id | int | FK → auth_user NOT NULL; Channel Partner Manager (#63) |
| state | varchar(100) | NOT NULL |
| territory | varchar(30) | NOT NULL; same enum as sales_lead.territory |
| status | varchar(20) | NOT NULL DEFAULT `ONBOARDING`; enum `ACTIVE` · `INACTIVE` · `SUSPENDED` · `ONBOARDING` |
| commission_rate_pct | numeric(5,2) | NOT NULL DEFAULT 10.00; 0.00–30.00 range |
| total_deals_closed | int | NOT NULL DEFAULT 0; denormalised count updated by Celery Task K-5 |
| total_arr_paise | bigint | NOT NULL DEFAULT 0; Denormalised — updated by Celery Task K-5 via UPDATE ... SET total_arr_paise = total_arr_paise + new_arr, total_deals_closed = total_deals_closed + 1 WHERE id = channel_partner_id. Uses SELECT FOR UPDATE on sales_channel_partner row to prevent race conditions during concurrent CLOSED_WON events. |
| commission_earned_paise | bigint | NOT NULL DEFAULT 0; total commissions earned (lifetime) |
| commission_paid_paise | bigint | NOT NULL DEFAULT 0; total commissions paid out (lifetime) |
| bank_account_verified | boolean | DEFAULT FALSE. Read-only via Sales module API (DRF serializer marks field as read_only=True). Can only be set to TRUE via Django admin by Platform Admin (#10) after offline bank account verification. No API endpoint in the Sales app allows writing this field — prevents programmatic bypass. |
| contact_name | varchar(200) | NOT NULL |
| contact_phone | varchar(15) | NOT NULL |
| contact_email | varchar(254) | NOT NULL |
| onboarded_at | date | NULLABLE; set when status → ACTIVE |
| last_deal_at | date | NULLABLE; set by Task K-5 on each new CLOSED_WON deal |

> Note: commission_rate_pct stores percentage as a whole number (e.g., 10.00 = 10%). Division by 100 applied at payout calculation: commission_paise = arr_estimate_paise × commission_rate_pct / 100.

---

### `sales_channel_deal`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| channel_partner_id | int | FK → sales_channel_partner NOT NULL |
| lead_id | int | FK → sales_lead UNIQUE NOT NULL; one commission record per lead |
| commission_paise | bigint | NOT NULL; computed as arr_estimate_paise × commission_rate_pct / 100 |
| commission_status | varchar(20) | NOT NULL DEFAULT `PENDING`; enum `PENDING` · `APPROVED` · `PAID` · `DISPUTED` |
| approved_by | int | FK → auth_user NULLABLE; Sales Manager (#57) who approved |
| approved_at | timestamptz | NULLABLE |
| paid_at | timestamptz | NULLABLE; set when Billing Admin (#70) marks payment processed |
| deal_closed_at | TIMESTAMPTZ | Copied from sales_lead.won_at at commission compute time — audit trail |

---

### `sales_quota`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| owner_id | int | FK → auth_user NOT NULL |
| period_type | varchar(10) | NOT NULL; enum `MONTHLY` · `QUARTERLY` |
| period_year | smallint | NOT NULL; e.g., 2026 |
| period_num | smallint | NOT NULL; month (1–12) or quarter (1–4) |
| segment | varchar(20) | NOT NULL; enum `SCHOOL` · `COLLEGE` · `COACHING` · `ALL` |
| target_deals | smallint | NOT NULL CHECK (target_deals > 0) |
| target_arr_paise | bigint | NOT NULL CHECK (target_arr_paise > 0) |

**Unique constraint:**
```sql
UNIQUE (owner_id, period_type, period_year, period_num)
```

---

**Table: `analytics_sales_funnel`** *(pre-aggregated by Celery Task K-1 — do not write directly)*

| Column | Type | Notes |
|---|---|---|
| id | BIGSERIAL PK | |
| computed_at | TIMESTAMPTZ | Timestamp of aggregation run |
| period_date | DATE | First day of the period (month) |
| stage | VARCHAR(30) | Pipeline stage enum |
| segment | VARCHAR(20) | SCHOOL / COLLEGE / COACHING / ALL |
| owner_id | BIGINT NULLABLE | NULL = aggregate across all execs |
| count_leads | INTEGER | Leads in this stage at computation time |
| total_arr_paise | BIGINT | Sum ARR of leads in stage |
| entered_from_prev | INTEGER | Leads that moved INTO this stage since last period |
| exited_to_next | INTEGER | Leads that moved OUT to next stage since last period |
| exited_to_lost | INTEGER | Leads moved to CLOSED_LOST from this stage since last period |
| conversion_pct | NUMERIC(5,2) | exited_to_next / (entered_from_prev) × 100 |
| median_days_in_stage | NUMERIC(6,1) | Median days leads spent in this stage before moving |

UNIQUE: (computed_at, period_date, stage, segment, owner_id)

---

### Database Indexes

| Table | Index | Type | Reason |
|---|---|---|---|
| `sales_lead` | `(owner_id, stage)` | B-tree composite | Pipeline table filtered by owner+stage on every exec login |
| `sales_lead` | `(stage, updated_at DESC)` | B-tree composite | Manager pipeline view sorted by recency |
| `sales_lead` | `(channel_partner_id)` WHERE is_channel_deal=TRUE | Partial B-tree | Channel deal attribution lookup |
| `sales_lead` | `(expected_close_date)` WHERE stage NOT IN ('CLOSED_WON','CLOSED_LOST') | Partial B-tree | Stale lead and close-date filter queries |
| `sales_activity` | `(lead_id, occurred_at DESC)` | B-tree composite | Timeline queries in K-03 (most common read) |
| `sales_activity` | `(logged_by, occurred_at DESC)` | B-tree composite | Recent activity feed in K-01 per exec |
| `sales_demo_tenant` | `(lead_id)` | B-tree | Demo status join in K-02 and K-04 |
| `sales_demo_tenant` | `(expires_at) WHERE is_active=TRUE` | Partial B-tree | Celery Task K-4 expiry scan |
| `sales_quota` | `(owner_id, period_type, period_year, period_num)` | B-tree (UNIQUE) | Quota attainment join |
| `sales_channel_deal` | `(channel_partner_id, commission_status)` | B-tree composite | Commission ledger in K-06 |
| `sales_partnership` | `(status, mou_expires_at)` | B-tree composite | Renewal calendar expiry queries |

---

## Celery Tasks

| Task ID | Name | Schedule | Description |
|---|---|---|---|
| K-1 | `compute_pipeline_summary` | Every 6 hours | Aggregates deals per stage + ARR totals per territory, segment, and exec. Writes results to `analytics_sales_funnel` (Div-H read). Also recomputes `avg_deal_size`, `demo_to_close_rate`, and `pipeline_velocity` metrics used in K-01 KPI strip. Duration ~3–5 min on 2,000+ lead dataset. Runs every 6 hours (NOT nightly). K-08 Reports references "nightly" incorrectly — the source is refreshed every 6 hours. |
| K-2 | `compute_quota_attainment` | Daily 07:00 IST | For each active quota record in `sales_quota`, queries `sales_lead` WHERE stage=CLOSED_WON AND won_at within period. Computes actual_deals, actual_arr_paise, attainment_pct. Results stored in `analytics_quota_attainment` for K-07 and K-08. Sends in-app notification to execs at <50% attainment with 7 days left in period. |
| K-3 | `flag_stale_leads` | Daily 09:00 IST | For each lead not in CLOSED_WON/CLOSED_LOST, checks MAX(occurred_at) in `sales_activity` for that lead_id. If last activity > 14 days ago (or no activity at all since creation > 7 days ago), marks lead as stale in a `sales_lead_flag` shadow store (not a column). Sends in-app alert to lead owner. Sends escalation alert to manager_id if lead is stale AND expected_close_date < today + 7 days. |
| K-4 | `expire_demo_tenants` | Daily 02:00 IST | Sets `is_active=False` on `sales_demo_tenant` rows where `expires_at < now()` and `is_active=True`. Sends in-app + email notification to Demo Manager (#62) listing all expired tenants. Also sends a deactivation request to Platform Admin (#10) via Div-C integration to revoke tenant access. Does not delete tenant data — preserved for 30 days post-expiry before Platform Admin hard-deletes. |
| K-5 | `compute_channel_commissions` | Daily 06:00 IST | On new CLOSED_WON leads with is_channel_deal=True: (1) SELECT FOR UPDATE sales_channel_partner row, (2) INSERT into sales_channel_deal with commission_paise computed, (3) UPDATE denormalised totals on sales_channel_partner. Runs within a single DB transaction to prevent race conditions. |

---

## Integration Points

| Direction | Division | Event | Action |
|---|---|---|---|
| K → Div-I | Customer Support (#51 Onboarding Specialist) | `sales_lead.stage` → CLOSED_WON | Creates onboarding task in Div-I queue; passes institution_name, contact details, ARR, segment, assigned exec. Notification sent to Onboarding Specialist. |
| K → Div-J | Customer Success (#94 ISM) | `sales_lead.stage` → CLOSED_WON | Creates `csm_account_assignment` with `csm_id` and `account_manager_id` pre-populated by Sales Manager. ISM receives handoff notification. |
| K → Div-C | Platform Admin (#10) | Demo tenant creation request from Demo Manager (#62) | `sales_demo_tenant` creation triggers tenant provisioning request in Div-C queue. Div-C Platform Admin provisions tenant and sets `tenant_id`. |
| K → Div-M | Billing Admin (#70) | `sales_lead.stage` → CLOSED_WON | Billing Admin receives subscription activation task with ARR, plan, institution details. Billing subscription record created from `arr_estimate_paise`. |
| K reads Div-F | Exam Engine | Sales Exec views public exam schedule | Read-only access to Div-F exam schedule for demo pitch context. No writes. |
| K → Div-H | Analytics | `compute_pipeline_summary` (Task K-1) | Sales funnel data written to `analytics_sales_funnel` every 6 hours for Ops Analyst reporting. |
| Div-L → K | Marketing (#97 Inside Sales queue) | Campaign lead events from Div-L | Marketing campaigns feed inbound leads directly to Inside Sales (#97) queue in K-02 with source=MARKETING_CAMPAIGN. |
| K reads Div-J | Customer Success | Churned institution win-back | Sales Manager (#57) has a read-only view of CHURNED renewals from `csm_renewal` for win-back campaign targeting. |

---

## URL Namespace

All Division K routes under `/group1/k/` prefix. Django app name: `sales`.

**Shell pages (GET):**

| URL Pattern | View Function | Name |
|---|---|---|
| `GET /group1/k/dashboard/` | `sales_dashboard` | `sales:dashboard` |
| `GET /group1/k/pipeline/` | `lead_pipeline` | `sales:pipeline` |
| `GET /group1/k/pipeline/export/` | `pipeline_export` | `sales:pipeline_export` |
| `GET /group1/k/account/<int:lead_id>/` | `account_profile` | `sales:account` |
| `GET /group1/k/demos/` | `demo_manager` | `sales:demos` |
| `GET /group1/k/partnerships/` | `partnership_tracker` | `sales:partnerships` |
| `GET /group1/k/channel-partners/` | `channel_partner_portal` | `sales:channel_partners` |
| `GET /group1/k/territory/` | `territory_quota` | `sales:territory` |
| `GET /group1/k/reports/` | `sales_reports` | `sales:reports` |
| `GET /group1/k/reports/export/` | `reports_export` | `sales:reports_export` |

**Write endpoints (POST / PATCH / DELETE):**

| URL Pattern | Method | View Function | Name |
|---|---|---|---|
| `/group1/k/pipeline/create/` | POST | `lead_create` | `sales:lead_create` |
| `/group1/k/account/<int:lead_id>/` | PATCH | `lead_update` | `sales:lead_update` |
| `/group1/k/account/<int:lead_id>/stage/` | POST | `lead_stage_move` | `sales:lead_stage` |
| `/group1/k/account/<int:lead_id>/activities/` | POST | `activity_create` | `sales:activity_create` |
| `/group1/k/account/<int:lead_id>/activities/<int:act_id>/` | PATCH | `activity_update` | `sales:activity_update` |
| `/group1/k/account/<int:lead_id>/activities/<int:act_id>/` | DELETE | `activity_delete` | `sales:activity_delete` |
| `/group1/k/pipeline/bulk-assign/` | POST | `lead_bulk_assign` | `sales:bulk_assign` |
| `/group1/k/pipeline/bulk-stage/` | POST | `lead_bulk_stage` | `sales:bulk_stage` |
| `/group1/k/pipeline/bulk-delete/` | POST | `lead_bulk_delete` | `sales:bulk_delete` |
| `/group1/k/demos/` | POST | `demo_tenant_create` | `sales:demo_create` |
| `/group1/k/demos/<int:demo_id>/reset/` | POST | `demo_tenant_reset` | `sales:demo_reset` |
| `/group1/k/demos/<int:demo_id>/extend/` | POST | `demo_tenant_extend` | `sales:demo_extend` |
| `/group1/k/demos/<int:demo_id>/deactivate/` | POST | `demo_tenant_deactivate` | `sales:demo_deactivate` |
| `/group1/k/partnerships/` | POST | `partnership_create` | `sales:partnership_create` |
| `/group1/k/partnerships/<int:pk>/` | PATCH | `partnership_update` | `sales:partnership_update` |
| `/group1/k/partnerships/<int:pk>/mou/` | POST | `partnership_mou_upload` | `sales:partnership_mou` |
| `/group1/k/channel-partners/` | POST | `channel_partner_create` | `sales:cp_create` |
| `/group1/k/channel-partners/<int:pk>/` | PATCH | `channel_partner_update` | `sales:cp_update` |
| `/group1/k/channel-partners/<int:pk>/deals/<int:deal_id>/approve/` | POST | `channel_deal_approve` | `sales:deal_approve` |
| `/group1/k/channel-partners/<int:pk>/deals/<int:deal_id>/pay/` | POST | `channel_deal_pay` | `sales:deal_pay` |
| `/group1/k/territory/quota/` | POST | `quota_create` | `sales:quota_create` |
| `/group1/k/territory/quota/<int:pk>/` | PATCH | `quota_update` | `sales:quota_update` |
| `/group1/k/territory/assign/` | POST | `territory_assign` | `sales:territory_assign` |

---

## Authorization & Security

### Role Enforcement
All Division K views enforce role-based access via a `@division_k_required` decorator applied to every Django view class. The decorator:
1. Verifies the user is authenticated (`request.user.is_authenticated`).
2. Checks the user's role ID is in the allowed set for that view.
3. Returns `403 Forbidden` (JSON `{"error": "Access denied"}`) for API endpoints; redirects to `/403/` for template views.

| Access Scenario | Response |
|---|---|
| Unauthenticated request to any K route | 302 redirect to `/login/?next=<url>` |
| Authenticated user with wrong role | 403 Forbidden |
| Exec accessing another exec's lead | 403 Forbidden (filtered at queryset level — exec sees 404 not 403, to avoid information leakage) |
| Manager accessing any lead | 200 OK |
| Read-only role (#95, #63) attempting POST | 403 Forbidden |

### Multi-Tenant Data Isolation
All `sales_lead` queries are scoped to `owner_id = request.user.id` for Sales Executives (#58–60, #97). Sales Manager (#57) and Sales Ops (#95) queries are unscoped (platform-wide). Pre-Sales Engineer (#96) queries filter by `presales_id = request.user.id`.

No sales data is tenant-scoped in the institution sense — Division K is a platform-internal module. All `sales_lead` records are EduForge-internal data, not visible to institution users.

### Sensitive Field Protection
- `bank_account_verified` on `sales_channel_partner`: read-only in all Sales API serializers; writable only via Django admin.
- `commission_paise` on `sales_channel_deal`: computed server-side on CLOSED_WON event; not settable via API.
- `arr_estimate_paise` on CLOSED_WON leads: server validates > 0 in model `clean()` before save.
- All soft-deleted leads (`deleted_at IS NOT NULL`): excluded from all queryset filters via a default manager that adds `.filter(deleted_at__isnull=True)`.

---

## Notification Events

| Event | Trigger | Recipient | Channel |
|---|---|---|---|
| Lead stage moved to CLOSED_WON | Post-save signal on `sales_lead.stage` | Sales Manager (#57) + Onboarding Specialist (#51) + Billing Admin (#70) + ISM (#94) | In-app + Email |
| Lead stage moved to CLOSED_LOST | Post-save signal on `sales_lead.stage` | Sales Manager (#57) | In-app |
| Lead stale (no activity 14+ days) | Task K-3 daily 09:00 | Lead owner (exec) | In-app |
| Stale lead with close date < 7 days | Task K-3 daily 09:00 | Lead owner + Sales Manager (#57) | In-app + Email |
| Quota attainment <50% with ≤7 days left in period | Task K-2 daily 07:00 | Individual exec | In-app |
| Demo tenant expiring in 48h | Task K-4 daily 02:00 (pre-expiry check) | Demo Manager (#62) + Lead owner | In-app |
| Demo tenant expired | Task K-4 daily 02:00 | Demo Manager (#62) | In-app + Email |
| Channel deal commission computed (new CLOSED_WON channel deal) | Task K-5 daily 06:00 | Channel Partner Manager (#63) | In-app |
| Channel commission approved | Post-save on `sales_channel_deal.commission_status` | Channel Partner Manager (#63) | In-app |
| New inbound lead assigned (MARKETING_CAMPAIGN source) | Div-L marketing event | Inside Sales Exec (#97) | In-app |
| Partnership MoU expiring in 30 days | Task K-1 (pipeline summary includes MoU expiry check) | Partnership Manager (#61) | In-app + Email |
| Demo tenant reset performed | Post-save on `sales_demo_tenant.last_reset_at` | Sales Manager (#57) (if >3 resets) | In-app |
| Pre-Sales Engineer assigned to lead (ARR > ₹2L) | Post-save on `sales_lead.presales_id` | Pre-Sales Engineer (#96) | In-app + Email |
| Lead created (by Inside Sales #97) | sales_lead INSERT with source=ORGANIC_INBOUND or MARKETING_CAMPAIGN | Assigned exec + Sales Manager (#57) | In-app |
| Commission rate changed >15% | sales_channel_partner.commission_rate_pct updated to >15 | Sales Manager (#57) | In-app + email |
| Demo tenant provisioning failed | Provisioning webhook returns error status | Demo Manager (#62) + Lead owner | In-app + email |
| Demo template refresh completed | Template refresh async task completes | Demo Manager (#62) | In-app |
| ENTERPRISE_POC trial requested >30 days | demo_type=ENTERPRISE_POC AND trial_duration > 30 | Sales Manager (#57) | In-app |
| Backward stage move escalated to COO | No Sales Manager action in 24h after backward-move request | Platform COO (#3) | In-app + email |
