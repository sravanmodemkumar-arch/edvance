# Division M — Finance & Billing: Pages Reference

> EduForge Group 1 Platform — internal Finance & Billing team only.
> 8 roles across invoice operations, receivables, GST compliance, refund processing, and pricing.

---

## Scale Context

| Dimension | Value |
|---|---|
| Total institutions billed | 2,050 |
| Monthly invoices generated | ~2,050 (Task M-2 auto-generates on 1st of month) |
| Annual invoice volume | ~24,600 |
| Invoice range | ₹500 (Starter micro-school) – ₹2,00,000+ (Enterprise coaching chain) |
| ARR range | ₹18Cr (early) – ₹90Cr (mature) |
| GST rate | 18% (SAC 9993 — Testing/Examination Services) |
| Payment gateway | Razorpay (orders, payments, settlements, refunds) |
| Overdue rate (steady state) | 3–5% → ~60–100 institutions at any time |
| Auto-pay retry policy | Day 1, Day 3, Day 7 after failure |
| Currency | INR only; amounts stored as paise (`INTEGER`) — never float |
| Decimal precision | `Decimal(28, 2)` in Python; `BIGINT` paise in PostgreSQL |
| Settlement payout frequency | T+2 to T+3 business days (Razorpay) |
| GSTR-1 due date | 11th of following month |
| GSTR-3B due date | 20th of following month |
| GSTR-9 (annual) due date | 31 December of following year |

---

## Division M Roles

| # | Role | Level | Primary Scope |
|---|---|---|---|
| 69 | Finance Manager | 1 | Revenue P&L, reconciliation sign-off, investor reporting, write-off decisions, refund approval > ₹10K |
| 70 | Billing Admin | 3 | Invoice generation/edit, plan assignment, account suspension/reactivation, refund request creation |
| 71 | Accounts Receivable Exec | 1 | 0–60 day overdue tracking, reminder dispatch, promise-to-pay logging (read-only on all finance records) |
| 72 | GST / Tax Consultant | 1 | GSTR-1/3B/9 filing, CGST/SGST/IGST computation, TDS 194J, Razorpay TCS |
| 73 | Refund Processing Exec | 3 | Refund validation, Razorpay API processing, refund status tracking |
| 74 | Pricing Admin | 3 | Subscription tier config, discount management, promo codes |
| 101 | Finance Analyst | 1 | ARR/MRR waterfall, NRR/GRR, P&L variance, investor deck prep, cohort revenue analysis (read-only, aggregated only) |
| 102 | Collections Executive | 3 | 60+ day overdue dunning calls, demand notices, payment plan negotiation, suspension coordination |

---

## Page Inventory

| ID | Route | Title | Primary Role(s) | Purpose |
|---|---|---|---|---|
| M-01 | `GET /finance/` | Finance Dashboard | #69, #101 | Central command: ARR/MRR KPIs, collection health, overdue overview, reconciliation status, refund queue, GST calendar |
| M-02 | `GET /finance/revenue/` | Revenue & P&L | #69, #101 | ARR waterfall, MRR trends, NRR/GRR, P&L by segment, investor-grade analytics |
| M-03 | `GET /finance/invoices/` | Billing & Invoices | #70 | Full invoice lifecycle: create, send, mark paid, void, write off |
| M-04 | `GET /finance/subscriptions/` | Subscription Manager | #70, #74 | All 2,050 institution subscriptions: plan assignment, upgrades, seat changes, suspension |
| M-05 | `GET /finance/ar/` | Accounts Receivable | #71, #102 | AR aging (4 buckets), follow-up log, dunning actions, payment plan tracker |
| M-06 | `GET /finance/settlements/` | Razorpay Settlements | #69 | Settlement reconciliation: match payouts to invoices, handle unmatched amounts |
| M-07 | `GET /finance/refunds/` | Refund Queue | #73 | Refund request queue: validate, approve-chain, process via Razorpay API |
| M-08 | `GET /finance/gst/` | GST & Tax | #72 | GSTR-1/3B/9 filing tracker, HSN/SAC summary, TDS, compliance calendar |
| M-09 | `GET /finance/pricing/` | Pricing & Discounts | #74 | Plan tier config, institution discounts, promo codes, pricing history |

---

## Role-to-Page Access Matrix

| Page | 69 FM | 70 Billing | 71 AR Exec | 72 GST | 73 Refund | 74 Pricing | 101 Analyst | 102 Collections |
|---|---|---|---|---|---|---|---|---|
| M-01 Finance Dashboard | Full | Billing strip | AR/overdue strip | GST strip | Refund strip | Pricing strip | Full read | Collections strip |
| M-02 Revenue & P&L | Full + export | No | No | No | No | Read (plan revenue only) | Full read + export | No |
| M-03 Billing & Invoices | Read + write-off | Full CRUD | Read overdue only | Read for GST | Read (payment records) | No | Read (aggregated) | Read overdue only |
| M-04 Subscription Manager | Read + approve | Full CRUD | No | No | No | Read + plan config | Read | No |
| M-05 AR | Full | Read | Full write | No | No | No | Read | Full write (60+ day only) |
| M-06 Settlements | Full | Read | No | Read (for TCS) | No | No | Read | No |
| M-07 Refund Queue | Full + approve > ₹10K | Create + read | No | No | Full process | No | Read | No |
| M-08 GST & Tax | Read | No | No | Full | No | No | Read | No |
| M-09 Pricing & Discounts | Read + approve > 20% discounts | No | No | No | No | Full | Read | No |

---

## Data Models

### `finance_invoice`

```
finance_invoice (
  id                  SERIAL PRIMARY KEY,
  invoice_number      VARCHAR(20) UNIQUE NOT NULL,        -- e.g. INV-2026-00841
  institution_id      INTEGER NOT NULL REFERENCES institution(id),
  subscription_id     INTEGER REFERENCES finance_subscription(id),
  billing_period_month INTEGER NOT NULL CHECK (billing_period_month BETWEEN 1 AND 12),
  billing_period_year INTEGER NOT NULL,
  issue_date          DATE NOT NULL,
  due_date            DATE NOT NULL,
  subtotal_paise      BIGINT NOT NULL CHECK (subtotal_paise >= 0),
  cgst_paise          BIGINT NOT NULL DEFAULT 0,
  sgst_paise          BIGINT NOT NULL DEFAULT 0,
  igst_paise          BIGINT NOT NULL DEFAULT 0,
  total_paise         BIGINT GENERATED ALWAYS AS (subtotal_paise + cgst_paise + sgst_paise + igst_paise) STORED,
  paid_amount_paise   BIGINT NOT NULL DEFAULT 0,
  status              VARCHAR(20) NOT NULL DEFAULT 'DRAFT',  -- DRAFT/SENT/PAID/OVERDUE/PARTIALLY_PAID/WRITTEN_OFF/VOID
  payment_reference   VARCHAR(100),
  paid_date           DATE,
  payment_mode        VARCHAR(30),                          -- NEFT/IMPS/UPI/RAZORPAY/CHEQUE
  po_number           VARCHAR(100),
  line_items_json     JSONB NOT NULL DEFAULT '[]',
  auto_generated      BOOLEAN NOT NULL DEFAULT FALSE,
  send_count          INTEGER NOT NULL DEFAULT 0,           -- number of times emailed
  last_sent_at        TIMESTAMPTZ,
  voided_by_id        INTEGER REFERENCES auth_user(id),
  voided_at           TIMESTAMPTZ,
  void_reason         TEXT,
  created_by_id       INTEGER NOT NULL REFERENCES auth_user(id),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

Indexes:
```sql
-- finance_invoice
CREATE INDEX idx_invoice_institution    ON finance_invoice(institution_id);
CREATE INDEX idx_invoice_status         ON finance_invoice(status);
CREATE INDEX idx_invoice_due_date       ON finance_invoice(due_date) WHERE status NOT IN ('PAID','VOID','WRITTEN_OFF');
CREATE INDEX idx_invoice_period         ON finance_invoice(billing_period_year, billing_period_month);
CREATE UNIQUE INDEX idx_invoice_inst_period ON finance_invoice(institution_id, billing_period_year, billing_period_month)
  WHERE status NOT IN ('VOID');

-- finance_subscription
CREATE INDEX idx_subscription_status   ON finance_subscription(status);
CREATE INDEX idx_subscription_plan     ON finance_subscription(plan_id);
CREATE INDEX idx_subscription_end_date ON finance_subscription(end_date) WHERE status = 'ACTIVE';

-- finance_payment
CREATE INDEX idx_payment_institution   ON finance_payment(institution_id);
CREATE INDEX idx_payment_settlement    ON finance_payment(settlement_id, status);
CREATE INDEX idx_payment_unmatched     ON finance_payment(settlement_id) WHERE settlement_id IS NULL AND status = 'CAPTURED';

-- finance_refund
CREATE INDEX idx_refund_status         ON finance_refund(status);
CREATE INDEX idx_refund_payment        ON finance_refund(payment_id);
CREATE INDEX idx_refund_approval       ON finance_refund(approval_required) WHERE approval_required = TRUE;
CREATE INDEX idx_refund_created        ON finance_refund(created_at DESC);

-- finance_ar_aging
CREATE INDEX idx_ar_aging_institution  ON finance_ar_aging(institution_id);
CREATE INDEX idx_ar_aging_collections  ON finance_ar_aging(bucket_61_90_paise, bucket_91plus_paise)
  WHERE (bucket_61_90_paise > 0 OR bucket_91plus_paise > 0);

-- finance_ar_followup
CREATE INDEX idx_ar_followup_institution ON finance_ar_followup(institution_id);
CREATE INDEX idx_ar_followup_type      ON finance_ar_followup(followup_type);

-- finance_razorpay_settlement
CREATE INDEX idx_settlement_payout_date ON finance_razorpay_settlement(payout_date DESC);
CREATE INDEX idx_settlement_unmatched  ON finance_razorpay_settlement(reconciliation_status)
  WHERE reconciliation_status = 'UNMATCHED';
```

### `finance_subscription`

```
finance_subscription (
  id                  SERIAL PRIMARY KEY,
  institution_id      INTEGER NOT NULL UNIQUE REFERENCES institution(id),
  plan_id             INTEGER NOT NULL REFERENCES finance_plan(id),
  start_date          DATE NOT NULL,
  end_date            DATE NOT NULL,
  billing_cycle       VARCHAR(10) NOT NULL DEFAULT 'ANNUAL',   -- MONTHLY/ANNUAL
  arr_paise           BIGINT NOT NULL CHECK (arr_paise > 0),
  mrr_paise           BIGINT GENERATED ALWAYS AS (arr_paise / 12) STORED,
  seats               INTEGER NOT NULL DEFAULT 0,
  auto_renew          BOOLEAN NOT NULL DEFAULT TRUE,
  status              VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',   -- ACTIVE/SUSPENDED/CANCELLED/EXPIRED/PENDING_APPROVAL
  discount_id         INTEGER REFERENCES finance_discount(id),
  activated_at        TIMESTAMPTZ,
  suspended_at        TIMESTAMPTZ,
  suspended_reason    TEXT,
  reactivated_at      TIMESTAMPTZ,
  reactivated_by_id   INTEGER REFERENCES auth_user(id),
  reactivation_reason TEXT,
  cancelled_at        TIMESTAMPTZ,
  created_by_id       INTEGER NOT NULL REFERENCES auth_user(id),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

### `finance_plan`

```
finance_plan (
  id                  SERIAL PRIMARY KEY,
  name                VARCHAR(100) NOT NULL,
  slug                VARCHAR(50) UNIQUE NOT NULL,             -- starter/standard/professional/enterprise
  tier                VARCHAR(20) NOT NULL,                    -- STARTER/STANDARD/PROFESSIONAL/ENTERPRISE
  billing_cycle       VARCHAR(10) NOT NULL,                    -- MONTHLY/ANNUAL
  base_price_paise    BIGINT NOT NULL CHECK (base_price_paise >= 0),
  price_per_seat_paise BIGINT NOT NULL DEFAULT 0,
  min_seats           INTEGER NOT NULL DEFAULT 0,
  max_seats           INTEGER,                                 -- NULL = unlimited (Enterprise)
  features_json       JSONB NOT NULL DEFAULT '{}',
  is_active           BOOLEAN NOT NULL DEFAULT TRUE,
  effective_from      DATE NOT NULL,
  effective_until     DATE,                                    -- NULL = currently active
  version             INTEGER NOT NULL DEFAULT 1,
  created_by_id       INTEGER NOT NULL REFERENCES auth_user(id),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

### `finance_payment`

```
finance_payment (
  id                      SERIAL PRIMARY KEY,
  institution_id          INTEGER NOT NULL REFERENCES institution(id),
  invoice_id              INTEGER REFERENCES finance_invoice(id),
  razorpay_payment_id     VARCHAR(50) UNIQUE NOT NULL,
  razorpay_order_id       VARCHAR(50),
  amount_paise            BIGINT NOT NULL CHECK (amount_paise > 0),
  payment_date            DATE NOT NULL,
  payment_method          VARCHAR(30),                         -- card/netbanking/upi/bank_transfer
  status                  VARCHAR(20) NOT NULL,                -- CAPTURED/FAILED/REFUNDED/PARTIALLY_REFUNDED
  refunded_amount_paise   BIGINT NOT NULL DEFAULT 0,           -- accumulated refund total; updated on each PROCESSED refund
  settlement_id           INTEGER REFERENCES finance_razorpay_settlement(id),
  reconciled_at           TIMESTAMPTZ,
  reconciled_by_id        INTEGER REFERENCES auth_user(id),
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

### `finance_razorpay_settlement`

```
finance_razorpay_settlement (
  id                      SERIAL PRIMARY KEY,
  razorpay_settlement_id  VARCHAR(50) UNIQUE NOT NULL,
  payout_date             DATE NOT NULL,
  amount_paise            BIGINT NOT NULL,                     -- gross settlement amount
  fees_paise              BIGINT NOT NULL DEFAULT 0,
  tax_paise               BIGINT NOT NULL DEFAULT 0,           -- GST on Razorpay fees
  net_paise               BIGINT GENERATED ALWAYS AS (amount_paise - fees_paise - tax_paise) STORED,
  tcs_paise               BIGINT NOT NULL DEFAULT 0,           -- TCS deducted by Razorpay
  status                  VARCHAR(20) NOT NULL DEFAULT 'SETTLED',
  reconciliation_status   VARCHAR(20) NOT NULL DEFAULT 'UNMATCHED',  -- AUTO_MATCHED/MANUALLY_MATCHED/UNMATCHED/EXCESS
  reconciled_by_id        INTEGER REFERENCES auth_user(id),
  reconciled_at           TIMESTAMPTZ,
  notes                   TEXT,
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

### `finance_refund`

```
finance_refund (
  id                      SERIAL PRIMARY KEY,
  institution_id          INTEGER NOT NULL REFERENCES institution(id),
  payment_id              INTEGER NOT NULL REFERENCES finance_payment(id),
  invoice_id              INTEGER REFERENCES finance_invoice(id),
  amount_paise            BIGINT NOT NULL CHECK (amount_paise > 0),
  reason                  VARCHAR(30) NOT NULL,    -- DUPLICATE_PAYMENT/PLAN_CANCELLED/BILLING_ERROR/GOODWILL/OVERPAYMENT/OTHER
  reason_notes            TEXT,
  status                  VARCHAR(25) NOT NULL DEFAULT 'PENDING_REVIEW',  -- PENDING_REVIEW/APPROVED/REJECTED/PROCESSING/PROCESSED/FAILED
  requested_by_id         INTEGER NOT NULL REFERENCES auth_user(id),
  reviewed_by_id          INTEGER REFERENCES auth_user(id),
  reviewed_at             TIMESTAMPTZ,
  review_notes            TEXT,
  approval_required       BOOLEAN GENERATED ALWAYS AS (amount_paise > 1000000) STORED,  -- > ₹10K needs FM approval
  razorpay_refund_id      VARCHAR(50) UNIQUE,
  processed_at            TIMESTAMPTZ,
  failed_reason           TEXT,
  retry_count             INTEGER NOT NULL DEFAULT 0,          -- max 3 retries before FM manual investigation
  receipt_pdf_path        VARCHAR(500),                        -- S3 key for generated refund receipt PDF
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

### `finance_ar_followup`

```
finance_ar_followup (
  id                  SERIAL PRIMARY KEY,
  institution_id      INTEGER NOT NULL REFERENCES institution(id),
  invoice_id          INTEGER REFERENCES finance_invoice(id),   -- NULL = portfolio-level follow-up
  followup_type       VARCHAR(30) NOT NULL,    -- REMINDER_EMAIL/PHONE_CALL/WHATSAPP/DEMAND_NOTICE/PAYMENT_PLAN_AGREED/ESCALATED/SUSPENDED/PROMISE_TO_PAY
  notes               TEXT,
  next_followup_date  DATE,
  promise_to_pay_date DATE,
  promise_amount_paise BIGINT,
  notice_pdf_path     VARCHAR(500),                            -- S3 key for generated demand notice PDF (DEMAND_NOTICE type only)
  created_by_id       INTEGER NOT NULL REFERENCES auth_user(id),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

### `finance_ar_aging`  *(pre-aggregated by Task M-1)*

```
finance_ar_aging (
  id                      SERIAL PRIMARY KEY,
  computed_at             TIMESTAMPTZ NOT NULL,
  institution_id          INTEGER NOT NULL REFERENCES institution(id),
  bucket_0_30_paise       BIGINT NOT NULL DEFAULT 0,
  bucket_31_60_paise      BIGINT NOT NULL DEFAULT 0,
  bucket_61_90_paise      BIGINT NOT NULL DEFAULT 0,
  bucket_91plus_paise     BIGINT NOT NULL DEFAULT 0,
  total_outstanding_paise BIGINT GENERATED ALWAYS AS
    (bucket_0_30_paise + bucket_31_60_paise + bucket_61_90_paise + bucket_91plus_paise) STORED,
  oldest_invoice_days     INTEGER NOT NULL DEFAULT 0,
  last_payment_date       DATE,
  last_followup_date      DATE,
  promise_to_pay_date     DATE,                               -- latest active promise date (synced from finance_ar_followup)
  promise_amount_paise    BIGINT,                             -- latest promise amount
  entered_0_30_date       DATE,                               -- when institution first entered 0–30d bucket this cycle
  entered_31_60_date      DATE,                               -- when institution first entered 31–60d bucket
  entered_61_90_date      DATE,                               -- when institution first entered 61–90d bucket (SLA clock start)
  entered_91plus_date     DATE,                               -- when institution first entered 90+ bucket (escalation clock start)
  assigned_collector_id   INTEGER REFERENCES auth_user(id)    -- NULL = AR Exec; #102 if escalated to Collections
)
```

### `finance_discount`

```
finance_discount (
  id                  SERIAL PRIMARY KEY,
  institution_id      INTEGER REFERENCES institution(id),       -- NULL = global / promo-linked
  discount_type       VARCHAR(20) NOT NULL,                    -- PERCENTAGE/FIXED_PAISE
  discount_value      BIGINT NOT NULL CHECK (discount_value > 0),  -- % × 100 or fixed paise
  valid_from          DATE NOT NULL,
  valid_to            DATE,                                    -- NULL = permanent
  reason              VARCHAR(100) NOT NULL,
  min_plan_tier       VARCHAR(20),                             -- minimum plan tier to qualify
  applies_to_plan_id  INTEGER REFERENCES finance_plan(id),    -- NULL = all plans
  fm_approval_required BOOLEAN GENERATED ALWAYS AS (discount_type='PERCENTAGE' AND discount_value > 2000) STORED,  -- > 20%
  approved_by_id      INTEGER REFERENCES auth_user(id),
  is_active           BOOLEAN NOT NULL DEFAULT TRUE,
  created_by_id       INTEGER NOT NULL REFERENCES auth_user(id),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

### `finance_promo_code`

```
finance_promo_code (
  id                      SERIAL PRIMARY KEY,
  code                    VARCHAR(30) UNIQUE NOT NULL,         -- e.g. SCHOOL2026, LAUNCH20
  discount_type           VARCHAR(20) NOT NULL,                -- PERCENTAGE/FIXED_PAISE
  discount_value          BIGINT NOT NULL CHECK (discount_value > 0),
  max_uses                INTEGER,                             -- NULL = unlimited
  current_uses            INTEGER NOT NULL DEFAULT 0,
  valid_from              DATE NOT NULL,
  valid_to                DATE,
  is_active               BOOLEAN NOT NULL DEFAULT TRUE,
  plan_restriction        VARCHAR(20),                         -- NULL = all plans
  institution_type_restriction VARCHAR(20),                   -- NULL = all types
  created_by_id           INTEGER NOT NULL REFERENCES auth_user(id),
  created_at              TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

### `finance_config`  *(key-value configuration store for Finance domain settings)*

```
finance_config (
  id                  SERIAL PRIMARY KEY,
  key                 VARCHAR(100) UNIQUE NOT NULL,
  value               TEXT NOT NULL,
  value_type          VARCHAR(20) NOT NULL DEFAULT 'STRING',  -- STRING/BIGINT/BOOLEAN/JSON
  description         TEXT,
  updated_by_id       INTEGER REFERENCES auth_user(id),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

Seed rows (managed via Django migration or admin):

| Key | Type | Default | Description |
|---|---|---|---|
| `arr_target_paise` | BIGINT | `1800000000` | Target ARR in paise for dashboard ARR trend target line (M-01) |
| `settlement_sync_manual_count_today` | BIGINT | `0` | Counter reset daily at midnight; max 3 manual Razorpay syncs per day (M-06) |
| `fm_signature_path` | STRING | `s3://eduforge-assets/signatures/fm_default.png` | S3 path to FM signature image for demand notices (M-05) |
| `refund_approval_threshold_paise` | BIGINT | `1000000` | Refund amount (paise) above which FM approval is required (M-07; default = ₹10,000) |
| `ar_sla_0_30_hours` | BIGINT | `24` | SLA: first reminder within N hours of invoice becoming overdue |
| `ar_sla_31_60_hours` | BIGINT | `48` | SLA: follow-up within N hours of entering 31–60d bucket |

---

### `finance_gst_return`

```
finance_gst_return (
  id                  SERIAL PRIMARY KEY,
  return_type         VARCHAR(10) NOT NULL,                    -- GSTR1/GSTR3B/GSTR9
  period              VARCHAR(7) NOT NULL,                     -- YYYY-MM (annual: YYYY)
  due_date            DATE NOT NULL,
  filing_date         DATE,                                    -- NULL = not filed yet
  status              VARCHAR(25) NOT NULL DEFAULT 'UPCOMING', -- UPCOMING/FILED/OVERDUE/FILED_WITH_PENALTY
  cgst_paise          BIGINT NOT NULL DEFAULT 0,
  sgst_paise          BIGINT NOT NULL DEFAULT 0,
  igst_paise          BIGINT NOT NULL DEFAULT 0,
  total_tax_paise     BIGINT GENERATED ALWAYS AS (cgst_paise + sgst_paise + igst_paise) STORED,
  taxable_paise       BIGINT NOT NULL DEFAULT 0,               -- subtotal before GST
  b2b_count           INTEGER NOT NULL DEFAULT 0,              -- number of B2B invoices in this period
  filed_by_id         INTEGER REFERENCES auth_user(id),
  arn                 VARCHAR(50),                             -- Acknowledgement Reference Number from GSTN
  notes               TEXT,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (return_type, period)
)
```

### `finance_tds_log`  *(manual TDS deduction entries — Section 194J)*

```
finance_tds_log (
  id                  SERIAL PRIMARY KEY,
  institution_id      INTEGER NOT NULL REFERENCES institution(id),
  invoice_id          INTEGER REFERENCES finance_invoice(id),   -- NULL = not invoice-specific
  amount_paise        BIGINT NOT NULL CHECK (amount_paise > 0),
  tds_rate            NUMERIC(5,2) NOT NULL,                    -- e.g. 10.00 for 10%
  form_16b_ref        VARCHAR(50),
  quarter             VARCHAR(10) NOT NULL,                     -- Q1/Q2/Q3/Q4 + year e.g. 'Q4-2026'
  deduction_date      DATE NOT NULL,
  notes               TEXT,
  created_by_id       INTEGER NOT NULL REFERENCES auth_user(id),
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

---

### `finance_plan_feature`  *(master feature registry — drives checkbox list in M-09 Create/Edit Plan)*

```
finance_plan_feature (
  id                  SERIAL PRIMARY KEY,
  name                VARCHAR(120) NOT NULL UNIQUE,               -- e.g. "Unlimited live exams"
  description         TEXT,                                       -- tooltip text in UI
  category            VARCHAR(50),                                -- e.g. "Exams", "Support", "Integrations"
  display_order       SMALLINT NOT NULL DEFAULT 0,                -- sort order within category
  is_active           BOOLEAN NOT NULL DEFAULT TRUE,              -- FALSE = archived; hidden in create modal
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

Features are stored as a JSONB array of IDs in `finance_plan.features_json` (e.g., `[1, 3, 7, 12]`). When rendering the plan detail drawer the app JOINs IDs against this table for display names. When a feature is archived (`is_active=FALSE`), it no longer appears in the create/edit checkbox list but remains readable in existing plan records.

---

### `finance_audit_log`  *(immutable audit trail for all state-changing Finance operations)*

```
finance_audit_log (
  id                  BIGSERIAL PRIMARY KEY,
  table_name          VARCHAR(60) NOT NULL,                       -- e.g. 'finance_invoice', 'finance_refund'
  record_id           INTEGER NOT NULL,
  action              VARCHAR(40) NOT NULL,                       -- e.g. 'CREATED','PAID','WRITTEN_OFF','PROCESSED','SUSPENDED','REACTIVATED'
  old_value_json      JSONB,                                      -- state before change; NULL on CREATE
  new_value_json      JSONB NOT NULL,                             -- state after change
  actor_id            INTEGER REFERENCES auth_user(id),           -- NULL if system/Celery task
  actor_ip            INET,                                       -- NULL if background task
  task_name           VARCHAR(80),                                -- Celery task name if triggered by background task
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
)
```

**Indexes:**
```sql
CREATE INDEX idx_audit_log_table_record ON finance_audit_log (table_name, record_id);
CREATE INDEX idx_audit_log_actor ON finance_audit_log (actor_id) WHERE actor_id IS NOT NULL;
CREATE INDEX idx_audit_log_created ON finance_audit_log (created_at DESC);
```

**Immutability:** No `UPDATE` or `DELETE` permissions granted on `finance_audit_log` to any application user. The write path is a dedicated `AuditLogWriter` service class that inserts only.

**Retention:** All audit records retained indefinitely (no purge). Table partitioned by `created_at` (monthly) to keep query performance stable at scale. Partition creation handled by `pg_partman`.

---

### `analytics_revenue`  *(pre-aggregated nightly by Task M-5)*

```
analytics_revenue (
  id                  SERIAL PRIMARY KEY,
  period_month        INTEGER NOT NULL CHECK (period_month BETWEEN 1 AND 12),
  period_year         INTEGER NOT NULL,
  segment             VARCHAR(20) NOT NULL DEFAULT 'all',      -- all/school/college/coaching/group
  plan_tier           VARCHAR(20) NOT NULL DEFAULT 'all',      -- all/STARTER/STANDARD/PROFESSIONAL/ENTERPRISE
  arr_paise           BIGINT NOT NULL DEFAULT 0,
  mrr_paise           BIGINT NOT NULL DEFAULT 0,
  new_arr_paise       BIGINT NOT NULL DEFAULT 0,               -- first subscriptions this month
  expansion_arr_paise BIGINT NOT NULL DEFAULT 0,               -- upgrades/seat additions
  contraction_arr_paise BIGINT NOT NULL DEFAULT 0,             -- downgrades/seat reductions
  churned_arr_paise   BIGINT NOT NULL DEFAULT 0,               -- cancellations/non-renewals
  invoiced_paise      BIGINT NOT NULL DEFAULT 0,
  collected_paise     BIGINT NOT NULL DEFAULT 0,
  overdue_paise       BIGINT NOT NULL DEFAULT 0,
  invoice_count       INTEGER NOT NULL DEFAULT 0,
  paid_count          INTEGER NOT NULL DEFAULT 0,
  overdue_count       INTEGER NOT NULL DEFAULT 0,
  active_subscription_count INTEGER NOT NULL DEFAULT 0,
  computed_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (period_year, period_month, segment, plan_tier)
)
```

---

## Celery Tasks

| Task | Schedule | Description | Approx Duration |
|---|---|---|---|
| **M-1** AR aging recompute | Daily 2:00 AM IST | Scans all `finance_invoice` WHERE status IN ('SENT','OVERDUE','PARTIALLY_PAID'), computes days overdue, populates `finance_ar_aging` with 4 buckets per institution. Triggers: auto-status upgrade SENT → OVERDUE when due_date < today. Sends amber alert to AR Exec (#71) if any institution crosses into 90+ bucket. | ~3–8 min |
| **M-2** Monthly invoice auto-generation | 1st of month, 9:00 AM IST | For all `finance_subscription` WHERE status='ACTIVE' AND billing_cycle='MONTHLY': generates one `finance_invoice` per subscription. Annual subscriptions generate on their `start_date` anniversary. Skips if a non-VOID invoice already exists for that institution + period. Sends notification to Billing Admin (#70) with batch summary (N generated, N skipped). | ~5–12 min |
| **M-3** Razorpay settlement sync | Daily 6:00 AM IST | Calls Razorpay Settlements API, fetches settlements from last 7 days. Upserts `finance_razorpay_settlement`. For each settlement, auto-matches to `finance_payment` rows using razorpay_payment_id; marks reconciliation_status=AUTO_MATCHED if fully resolved, UNMATCHED if no match found. Sends alert to Finance Manager (#69) if UNMATCHED count > 0. | ~2–5 min |
| **M-4** GST deadline alerts | Daily 8:00 AM IST | Checks `finance_gst_return` WHERE due_date IN (today+7, today+1) AND status IN ('UPCOMING','OVERDUE'). Sends email alert to GST Consultant (#72) and Finance Manager (#69). Also alerts on return_type=GSTR9 when due_date is 30 days out. | ~30 sec |
| **M-5** Revenue analytics aggregation | Daily 3:00 AM IST | Aggregates invoice + subscription data into `analytics_revenue`. Computes new/expansion/contraction/churn ARR movements by comparing current month subscriptions against prior month state. Runs for all segment × plan_tier combinations (5 segments × 5 tiers + totals = ~30 rows per month). | ~8–15 min |

---

## Integration Points

| Event | Source Division | Action in Division M |
|---|---|---|
| `CLOSED_WON` deal finalised | Division K (#57 Sales Manager) | Billing Admin (#70) receives notification: institution name, ARR, plan tier, deal ID. Billing Admin creates `finance_subscription` and first `finance_invoice`. |
| Onboarding handoff complete | Division I (#51 Onboarding Specialist) | Billing Admin prompted to activate subscription; trigger Task M-2 early for new institution. |
| Institution renewal confirmed | Division J (#54 Account Manager) | Billing Admin generates renewal invoice; updates `finance_subscription.end_date`. |
| Institution health = CHURNED_RISK | Division J (#53 CSM) | Finance Manager (#69) receives alert: institution at churn risk, outstanding invoices if any. |
| Exam Day incident (P1/P2) | Division F (#38 Incident Manager) | Finance Manager may issue goodwill discount or credit note to affected institutions — creates `finance_discount` record. |
| DPDP consent withdrawal | Division N (#76 DPO) | Billing Admin must not generate new invoices; Finance Manager informed for write-off of outstanding balance. |
| Platform subscription activated | Division C (#10 Platform Admin) | Billing Admin notified to ensure `finance_subscription` record is active and correctly mapped. |
| NPS DETRACTOR from coaching chain | Division J (#93 CS Analyst) | Finance Manager may approve goodwill discount; Pricing Admin creates institution-specific `finance_discount`. |
| WhatsApp/SMS payment reminders | Division F (#37 Notification Manager) | AR Exec (#71) or Collections Exec (#102) triggers via notification service; tracked in `finance_ar_followup`. |
| Channel partner commission | Division K (#63 Channel Partner Manager) | Finance Manager approves commission payout; Billing Admin adjusts ARR to reflect net revenue. |

---

## URL Namespace

All Division M routes live under `/finance/`. Shell pages (GET) are Django `TemplateView`; write endpoints (POST/PATCH/DELETE) are Django `View` subclasses.

```
GET   /finance/                          → FinanceDashboardView
GET   /finance/revenue/                  → RevenuePLView
GET   /finance/invoices/                 → BillingInvoicesView
POST  /finance/invoices/create/          → InvoiceCreateView
PATCH /finance/invoices/{id}/status/     → InvoiceStatusView        (mark paid, void, write-off)
POST  /finance/invoices/{id}/send/       → InvoiceSendView
POST  /finance/invoices/bulk-remind/     → BulkReminderView
GET   /finance/subscriptions/            → SubscriptionManagerView
POST  /finance/subscriptions/create/     → SubscriptionCreateView
PATCH /finance/subscriptions/{id}/       → SubscriptionUpdateView
POST  /finance/subscriptions/{id}/suspend/         → SubscriptionSuspendView
POST  /finance/subscriptions/{id}/reactivate/      → SubscriptionReactivateView
POST  /finance/subscriptions/{id}/cancel/          → SubscriptionCancelView       (FM #69 only, 2FA required)
PATCH /finance/subscriptions/{id}/approve-arr/     → SubscriptionARRApproveView   (FM #69 only; approves >20% ARR change)
GET   /finance/ar/                                 → AccountsReceivableView
POST  /finance/ar/followup/                        → ARFollowupCreateView
GET   /finance/settlements/                        → SettlementsView
POST  /finance/settlements/sync/                   → SettlementSyncView           (FM #69 only; rate-limited 3/day)
POST  /finance/settlements/{id}/match/             → SettlementMatchView
GET   /finance/refunds/                            → RefundQueueView
POST  /finance/refunds/create/                     → RefundCreateView
POST  /finance/refunds/lookup-payment/             → RefundLookupPaymentView      (validates payment_id; returns amount + institution)
PATCH /finance/refunds/{id}/review/                → RefundReviewView
POST  /finance/refunds/{id}/process/               → RefundProcessView            (2FA required)
POST  /finance/refunds/{id}/retry/                 → RefundRetryView              (2FA required; FAILED status only)
GET   /finance/gst/                                → GSTTaxView
POST  /finance/gst/returns/{id}/file/              → GSTReturnFileView
PATCH /finance/gst/returns/{id}/confirm/           → GSTReturnConfirmView         (FM #69 only; confirms GST Consultant's filing)
POST  /finance/gst/tds/                            → TDSLogCreateView             (GST Consultant #72 only)
GET   /finance/pricing/                            → PricingDiscountsView
POST  /finance/pricing/plans/                      → PlanCreateView
PATCH /finance/pricing/plans/{id}/                 → PlanUpdateView
POST  /finance/pricing/plans/{id}/archive/         → PlanArchiveView              (Pricing Admin #74 only)
POST  /finance/pricing/discounts/                  → DiscountCreateView
PATCH /finance/pricing/discounts/{id}/             → DiscountUpdateView
POST  /finance/pricing/discounts/{id}/approve/     → DiscountApproveView          (FM #69 only)
POST  /finance/pricing/discounts/{id}/reject/      → DiscountRejectView           (FM #69 only)
POST  /finance/pricing/promos/                     → PromoCodeCreateView
POST  /finance/pricing/promos/{id}/deactivate/     → PromoCodeDeactivateView      (Pricing Admin #74 only)
POST  /finance/revenue/forecast/                   → RevenueForecastUpdateView    (FM #69 only)
```

HTMX partial loads: all routes accept `?part=<partial_name>` and return HTML fragments.

---

## Authorization & Security

**Role enforcement decorator:** `@division_m_required(allowed_roles=[69, 70, 71, 72, 73, 74, 101, 102])` applied to all finance views.

**Sensitive operations requiring 2FA (TOTP):**
- Mark Invoice as Paid
- Write Off Invoice
- Approve Refund > ₹10K
- Trigger Razorpay Refund API call (Process + Retry)
- Issue Demand Notice
- Suspend Institution Account
- Reactivate Institution Account
- Cancel Subscription

**Financial data isolation:**
- All paise values stored as `BIGINT` — no float arithmetic anywhere in the stack.
- All monetary computations use Python's `decimal.Decimal` with `ROUND_HALF_UP`.
- Invoice PDFs generated server-side (WeasyPrint); never computed client-side.
- Razorpay API keys (Key ID + Key Secret) stored in AWS KMS; never in environment variables or code.
- Razorpay webhook signatures verified using HMAC-SHA256 before processing any payment event.

**CSRF Protection:** All POST/PATCH/DELETE endpoints validate Django CSRF tokens. HTMX includes `X-CSRFToken` header automatically via base template meta tag (`{% csrf_token %}`). Webhook endpoints (`/finance/settlements/webhook/`) are exempt from CSRF; they use Razorpay HMAC-SHA256 signature verification instead.

**Audit log:** Every state-changing operation on `finance_invoice`, `finance_subscription`, `finance_refund` writes to `finance_audit_log` (id, table_name, record_id, action, old_value_json, new_value_json, actor_id, actor_ip, created_at). Immutable — no UPDATE or DELETE on audit records.

**Data access segmentation:**
- #71 AR Exec and #101 Finance Analyst: read-only Django permissions (`has_perm('finance.view_*')` only).
- #102 Collections Exec: write access only to `finance_ar_followup` and `finance_subscription` suspend action.
- #72 GST Consultant: read access to invoices/payments; write access only to `finance_gst_return`.

---

## Notification Events

| Event | Recipient(s) | Channel | When |
|---|---|---|---|
| Invoice auto-generated (Task M-2) | #70 Billing Admin | In-app + email | Batch summary at 9:05 AM on 1st of month |
| Invoice overdue (≥ 1 day past due_date) | #71 AR Exec | In-app | Task M-1 run |
| Institution enters 90+ day bucket | #102 Collections Exec + #69 Finance Manager | Email + in-app | Task M-1 run |
| Refund request created | #73 Refund Exec + #69 Finance Manager (if > ₹10K) | In-app | Immediate on creation |
| Refund processed successfully | #70 Billing Admin + institution billing contact | In-app + email | On Razorpay API success response |
| Refund failed (Razorpay error) | #73 Refund Exec + #69 Finance Manager | In-app + email | Immediate on failure |
| Razorpay settlement unmatched | #69 Finance Manager | In-app + email | Task M-3 completion if UNMATCHED > 0 |
| GST filing due in 7 days | #72 GST Consultant + #69 Finance Manager | Email | Task M-4 |
| GST filing due tomorrow | #72 GST Consultant + #69 Finance Manager | Email + SMS | Task M-4 |
| GST return OVERDUE (missed due date) | #72 GST Consultant + #69 Finance Manager | Email + Slack | Task M-4 |
| Account suspended for non-payment | #54 Account Manager (Div J) + #70 Billing Admin | In-app + email | On suspension action |
| Payment plan agreed with institution | #71 AR Exec + #69 Finance Manager | In-app | On `finance_ar_followup` PAYMENT_PLAN_AGREED creation |
| Discount > 20% created (pending approval) | #69 Finance Manager | In-app | Immediate |
| Discount > 20% approved/rejected | #74 Pricing Admin | In-app | Immediate |
| Account reactivated | #54 Account Manager (Div J), #53 CSM (Div J), institution billing contact | In-app + email | On reactivation action |
| Subscription cancelled | #54 Account Manager (Div J), #53 CSM (Div J), institution billing contact | In-app + email | On cancel action |
| AR SLA breach (0–30d: >24h without followup) | #71 AR Exec + #69 Finance Manager | In-app | Task M-1 daily digest |
| AR SLA breach (61–90d: no demand notice within 5 biz days) | #69 Finance Manager | Email + in-app | Task M-1 daily digest |
| ARR change > 20% pending approval | #69 Finance Manager | In-app | Immediate on PENDING_APPROVAL subscription creation |
| ARR change approved by FM | #70 Billing Admin | In-app | On approval action |
| GST return filing confirmed by FM | #72 GST Consultant | In-app | On FM confirm action |
| Promise-to-Pay broken (due date passed, not paid) | #71 AR Exec + #102 Collections Exec | In-app | Task M-1 run |
