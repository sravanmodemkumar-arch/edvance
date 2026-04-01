# EduForge — Database Schema Design

## Pattern: Schema-per-Service

One PostgreSQL 16 cluster. Seven schemas. Each service owns its schema.

```sql
-- Connection per service
identity  service → SET search_path TO identity
portal    service → SET search_path TO portal
exam      service → SET search_path TO exam
...
```

**Benefits:**
- One cluster to manage, backup, and monitor
- Cross-schema JOINs possible via views
- PostgreSQL row-level security enforces isolation
- Rs. 4,500/month (db.t4g.medium) handles 5 lakh students

---

## Schema: identity

### institutions
```sql
CREATE TABLE identity.institutions (
    id               SERIAL PRIMARY KEY,
    name             VARCHAR(255) NOT NULL,
    domain           VARCHAR(100) UNIQUE NOT NULL,
    institution_type VARCHAR(50) NOT NULL,  -- school|college|coaching|ssc|rrb|state_board
    is_active        BOOLEAN DEFAULT TRUE,
    created_at       TIMESTAMPTZ DEFAULT NOW()
);
```

### users
```sql
CREATE TABLE identity.users (
    id               SERIAL PRIMARY KEY,
    institution_id   INT REFERENCES identity.institutions(id),
    mobile           VARCHAR(15) UNIQUE NOT NULL,
    role             VARCHAR(50) NOT NULL,  -- student|staff|admin
    is_active        BOOLEAN DEFAULT TRUE,
    created_at       TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_users_mobile ON identity.users(mobile);
```

### otps  ← Replaces Redis
```sql
CREATE TABLE identity.otps (
    id         SERIAL PRIMARY KEY,
    mobile     VARCHAR(15) NOT NULL,
    otp_hash   VARCHAR(255) NOT NULL,  -- bcrypt hash, plain OTP never stored
    expires_at TIMESTAMPTZ NOT NULL,
    used       BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_otps_mobile ON identity.otps(mobile);
```

### sessions
```sql
CREATE TABLE identity.sessions (
    id                  SERIAL PRIMARY KEY,
    user_id             INT REFERENCES identity.users(id),
    refresh_token_hash  VARCHAR(255) NOT NULL,
    expires_at          TIMESTAMPTZ NOT NULL,
    is_revoked          BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Schema: portal

### students
```sql
CREATE TABLE portal.students (
    id                SERIAL PRIMARY KEY,
    user_id           INT REFERENCES identity.users(id),
    institution_id    INT REFERENCES identity.institutions(id),
    roll_number       VARCHAR(50),
    academic_level    VARCHAR(50),    -- class_6|inter_1st_year|etc.
    residential_status VARCHAR(20),   -- day_scholar|hosteler
    special_status    VARCHAR(50)[],  -- scholarship|rte|special_needs
    admitted_on       DATE,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);
```

### attendance
```sql
CREATE TABLE portal.attendance (
    id           SERIAL PRIMARY KEY,
    student_id   INT REFERENCES portal.students(id),
    date         DATE NOT NULL,
    session_type VARCHAR(20) NOT NULL,  -- morning|afternoon
    status       VARCHAR(10) NOT NULL,  -- present|absent|late
    marked_by    INT REFERENCES identity.users(id),
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(student_id, date, session_type)
);
```

### fees
```sql
CREATE TABLE portal.fees (
    id             SERIAL PRIMARY KEY,
    student_id     INT REFERENCES portal.students(id),
    amount         NUMERIC(10,2) NOT NULL,
    fee_type       VARCHAR(50),   -- tuition|hostel|transport|exam
    due_date       DATE,
    paid_at        TIMESTAMPTZ,
    status         VARCHAR(20) DEFAULT 'pending',  -- pending|paid|overdue
    created_at     TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Schema: exam

### questions
```sql
CREATE TABLE exam.questions (
    id           SERIAL PRIMARY KEY,
    exam_type    VARCHAR(50),    -- ssc|rrb|ap_board|ts_board
    subject      VARCHAR(100),
    topic        VARCHAR(100),
    difficulty   VARCHAR(10),    -- easy|medium|hard
    question_en  TEXT NOT NULL,
    question_hi  TEXT,
    options      JSONB NOT NULL, -- {"A":"..","B":"..","C":"..","D":".."}
    answer       VARCHAR(1) NOT NULL,
    explanation  TEXT,
    approved_by  INT REFERENCES identity.users(id),
    created_at   TIMESTAMPTZ DEFAULT NOW()
);
```

### exam_sessions
```sql
CREATE TABLE exam.exam_sessions (
    id               SERIAL PRIMARY KEY,
    user_id          INT REFERENCES identity.users(id),
    test_id          INT NOT NULL,
    started_at       TIMESTAMPTZ DEFAULT NOW(),
    expires_at       TIMESTAMPTZ NOT NULL,
    answers_received BOOLEAN DEFAULT FALSE,  -- prevents double-submit
    submit_source    VARCHAR(20)             -- manual|timer|crash_recovery
);
```

### attempts
```sql
CREATE TABLE exam.attempts (
    id           SERIAL PRIMARY KEY,
    session_id   INT REFERENCES exam.exam_sessions(id),
    user_id      INT REFERENCES identity.users(id),
    answers      JSONB NOT NULL,  -- {"1":"A","2":"C",...}
    time_taken   INT,             -- seconds
    submitted_at TIMESTAMPTZ DEFAULT NOW()
);
```

### results
```sql
CREATE TABLE exam.results (
    id          SERIAL PRIMARY KEY,
    attempt_id  INT REFERENCES exam.attempts(id),
    score       NUMERIC(6,2),
    rank        INT,
    percentile  NUMERIC(5,2),
    computed_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Schema: billing

### payments
```sql
CREATE TABLE billing.payments (
    id                   SERIAL PRIMARY KEY,
    institution_id       INT REFERENCES identity.institutions(id),
    razorpay_payment_id  VARCHAR(100) UNIQUE,  -- prevents double-processing
    amount               NUMERIC(10,2),
    status               VARCHAR(20),   -- created|captured|failed|refunded
    created_at           TIMESTAMPTZ DEFAULT NOW()
);
```

### invoices
```sql
CREATE TABLE billing.invoices (
    id             SERIAL PRIMARY KEY,
    payment_id     INT REFERENCES billing.payments(id),
    invoice_number VARCHAR(50) UNIQUE,
    gstin          VARCHAR(20),
    sac_code       VARCHAR(10) DEFAULT '9993',  -- digital education services
    cgst           NUMERIC(10,2),
    sgst           NUMERIC(10,2),
    igst           NUMERIC(10,2),
    total          NUMERIC(10,2),
    pdf_r2_url     TEXT,
    created_at     TIMESTAMPTZ DEFAULT NOW()
);
```

---

## No Redis — What Replaces It

| Redis Use Case | Replacement | Performance |
|---|---|---|
| OTP storage (5 min TTL) | `identity.otps` + `expires_at` | ~2ms indexed query |
| Rate limiting | `identity.rate_limits` + COUNT | ~3ms acceptable |
| JWT validation | Stateless JWT verified locally | Faster — no network |
| Fragment cache | Cloudflare CDN Cache-Control | Better than Redis |
| Session store | Stateless JWT + refresh in DB | Same pattern |
| Nightly cleanup | EventBridge cron at 2 AM IST | Rs.0 |
