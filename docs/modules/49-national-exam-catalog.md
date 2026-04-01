# Module 49 — National Exam Catalog (Group 6)

## 1. Purpose & Scope

The National Exam Catalog is EduForge's structured, maintained registry of every significant competitive examination in India — 300+ exams across central and state conducting bodies. It serves students preparing for government jobs, entrance tests, and professional certifications.

It is not merely a list. The catalog delivers:

- **Complete exam metadata**: pattern, eligibility, dates, marking scheme, salary, career trajectory
- **Previous Year Questions (PYQs)**: 75,000+ questions tagged to syllabus nodes, available for practice
- **Eligibility checker**: instant match of student profile to eligible exams
- **Application tracker**: personal pipeline management from "Interested" to "Appointed"
- **Cut-off history**: 7-year trends by category to benchmark mock test scores
- **Calendar integration**: all exam events synced to student calendar with smart alerts
- **Preparation roadmaps**: 6–18 month study plans per exam (feeds Module 47 learning paths)
- **Mock test series**: pre-configured test series per exam (feeds Module 22)

"Group 6" in module naming refers to the sixth role group in EduForge RBAC: Competitive Exam Aspirant — students enrolled in coaching institutes or self-study programs targeting government exams.

**What this module does NOT do:**
- Guarantee exam dates (official sources are authoritative — catalog is reference data)
- Generate external URLs (official website fields are static text, not LLM-generated links)
- Store PII for browsing (catalog is publicly accessible without login)

---

## 2. Exam Catalog — Coverage

### Central Government Exams

| Category | Key Exams |
|----------|-----------|
| **Civil Services** | UPSC CSE (IAS/IPS/IFS/IRS), CAPF AC, CMS, Engineering Services, SCRA, CISF AC, IB ACIO |
| **SSC** | CGL, CHSL, MTS, CPO, GD Constable, JHT, JE, Stenographer Grade C/D, Selection Posts (Phase I–XII) |
| **Banking** | IBPS PO/Clerk/RRB (PO+Clerk+Officer Scale II/III), SBI PO/Clerk, RBI Grade B/Office Attendant, NABARD Grade A/B, SEBI Grade A |
| **Railways** | RRB NTPC (Graduate + Undergraduate levels), RRB Group D, ALP, JE, SSE, Paramedical, Ministerial & Isolated Posts |
| **Defence** | NDA, CDS, AFCAT, Agniveer (Army/Navy/Air Force), Coast Guard |
| **Teaching** | CTET (Paper I + II), NVS TGT/PGT/PRT, KVS TGT/PGT/PRT, EMRS Teacher, DSSSB |
| **Insurance** | LIC AAO/ADO, NIACL AO/Assistant, UIIC AO, NICL AO, OIC AO |
| **Medical** | NEET UG, NEET PG, NEET MDS, AIIMS PG, FMGE (MCI), UPSC CMS |
| **Technical** | GATE (29 papers), BARC, ISRO Scientist, DRDO SET, AAI JE/ATC, ONGC GT |
| **Higher Education Entrance** | CUET (UG + PG), JEE Main, JEE Advanced |
| **Law** | CLAT, AILET, LSAT-India |
| **Management** | CAT, XAT, MAT, SNAP, CMAT, NMAT, GMAT, IIFT |

### State Government Exams (All 30 States + Major UTs)

| State Group | PSC Exams |
|-------------|-----------|
| Northern | UPPSC PCS, HPSC HCS, HPPSC HAS, JKPSC KAS, UKPSC PCS |
| Eastern | BPSC BPAS, WBPSC WBCS, JPSC JPAS, OPSC OAS, APSC ACS |
| Central | MPPSC MPAS, CGPSC CGAS, RPSC RAS |
| Western | GPSC GPCAS, MPSC MPAS (Maharashtra) |
| Southern | KPSC KAS, APPSC APAS, TNPSC TNAS, KPSCKE KPAS (Kerala), TSPSC TSAS |
| North-East | APSC, MIZORAM PSC, MEGHALAYA PSC, MANIPUR PSC, NAGALAND PSC |

State-specific exams also include: state teaching (TET/TGT/PGT), state police (SI/Constable), state banking (cooperative banks, RRBs), state electricity board JE/AE, state judicial services, and municipal service exams (MCGM, BMC, KDMC).

---

## 3. Data Model

### Catalog Hierarchy

```
exam_families (e.g., "UPSC Civil Services")
    └─ exam_catalog (e.g., "CSE 2026")
          ├─ exam_stages (Prelims, Mains, Interview)
          │     └─ exam_papers (GS Paper 1, GS Paper 2, …)
          ├─ exam_dates (notification, app_open, app_close, admit_card, exam, result)
          ├─ exam_cutoffs (year × category × post)
          ├─ exam_salary_data (post × pay level)
          └─ exam_syllabus_nodes (links to Module 15 syllabus tree)
```

### Core Tables

```sql
-- exam_catalog
CREATE TABLE exams.exam_catalog (
    exam_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_family_id      UUID,
    conducting_body     VARCHAR(100) NOT NULL,     -- "UPSC", "IBPS", "SSC"
    official_name       TEXT NOT NULL,
    short_name          VARCHAR(100),
    acronym             VARCHAR(20),
    exam_type           VARCHAR(20),               -- 'central', 'state', 'ut'
    category            VARCHAR(30),               -- 'civil_services', 'banking', ...
    subcategory         VARCHAR(50),               -- 'IBPS PO', 'SSC CGL Tier 1', ...
    total_vacancies     INT,
    vacancy_year        INT,
    is_central          BOOLEAN DEFAULT TRUE,
    state_code          VARCHAR(2),                -- for state exams
    official_website    TEXT,                      -- static metadata only
    min_age             SMALLINT,
    max_age             SMALLINT,
    age_cutoff_date_rule TEXT,                     -- "1st August of exam year"
    min_qualification   TEXT,
    nationality_req     TEXT DEFAULT 'Indian Citizen',
    attempt_limit       SMALLINT,                  -- NULL = unlimited
    exam_mode           VARCHAR(20),               -- 'cbt', 'omr', 'both', 'remote'
    marking_scheme      JSONB,
    languages           TEXT[],
    is_active           BOOLEAN DEFAULT TRUE,
    last_updated        TIMESTAMPTZ DEFAULT NOW(),
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_ec_category    ON exams.exam_catalog (category, is_active);
CREATE INDEX idx_ec_state       ON exams.exam_catalog (state_code) WHERE state_code IS NOT NULL;

-- exam_stages
CREATE TABLE exams.exam_stages (
    stage_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_id         UUID NOT NULL REFERENCES exams.exam_catalog(exam_id),
    stage_name      VARCHAR(50) NOT NULL,      -- 'Prelims', 'Mains', 'Interview'
    stage_order     SMALLINT NOT NULL,
    is_qualifying   BOOLEAN DEFAULT FALSE,     -- qualifying-only stage (marks not counted)
    advance_ratio   NUMERIC(6,2)               -- ratio of applicants advancing to next stage
);

-- exam_papers
CREATE TABLE exams.exam_papers (
    paper_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stage_id            UUID NOT NULL REFERENCES exams.exam_stages(stage_id),
    paper_name          VARCHAR(100) NOT NULL,
    paper_order         SMALLINT,
    total_marks         INT,
    total_questions     INT,
    duration_min        INT,
    sections            JSONB,    -- [{name, questions, marks_each, negative}]
    negative_marking    NUMERIC(4,2) DEFAULT 0,
    language            VARCHAR(50),
    is_objective        BOOLEAN DEFAULT TRUE,
    is_qualifying_paper BOOLEAN DEFAULT FALSE
);

-- exam_dates
CREATE TABLE exams.exam_dates (
    date_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_id         UUID NOT NULL REFERENCES exams.exam_catalog(exam_id),
    year            INT NOT NULL,
    event_type      VARCHAR(30) NOT NULL
                    CHECK (event_type IN ('notification','app_start','app_end',
                                          'admit_card','exam_prelims','exam_mains',
                                          'exam_interview','result','final_merit')),
    date            DATE,
    date_range_end  DATE,                  -- for events spanning multiple days
    is_confirmed    BOOLEAN DEFAULT FALSE,
    source_url      TEXT,                  -- official notification URL (static)
    notes           TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (exam_id, year, event_type)
);

-- exam_cutoffs
CREATE TABLE exams.exam_cutoffs (
    cutoff_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_id         UUID NOT NULL REFERENCES exams.exam_catalog(exam_id),
    stage           VARCHAR(20),
    year            INT NOT NULL,
    post_name       VARCHAR(100),          -- for exams with multiple posts
    category        VARCHAR(20) NOT NULL,  -- 'UR', 'OBC', 'SC', 'ST', 'EWS', 'PWD', 'ExSM'
    cutoff_marks    NUMERIC(7,2),
    total_marks     INT,
    vacancies_filled INT,
    normalised      BOOLEAN DEFAULT FALSE,
    source_reference TEXT
);

CREATE INDEX idx_ec_exam_year ON exams.exam_cutoffs (exam_id, year DESC);

-- pyq_questions
CREATE TABLE exams.pyq_questions (
    pyq_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_id             UUID NOT NULL REFERENCES exams.exam_catalog(exam_id),
    year                INT NOT NULL,
    stage               VARCHAR(20),
    paper               VARCHAR(100),
    subject             VARCHAR(50),
    chapter             VARCHAR(100),
    topic               VARCHAR(200),
    syllabus_node_id    UUID REFERENCES syllabus_nodes(node_id),
    question_text       TEXT NOT NULL,
    options             JSONB,             -- null for descriptive
    correct_answer      VARCHAR(5),
    explanation         TEXT,
    difficulty          VARCHAR(10),       -- 'easy', 'medium', 'hard', 'very_hard'
    marks               NUMERIC(4,2),
    negative_marks      NUMERIC(4,2),
    frequency_score     NUMERIC(5,2) DEFAULT 1.0,  -- appears N times in 10 years
    is_memory_based     BOOLEAN DEFAULT FALSE,
    is_official         BOOLEAN DEFAULT TRUE,
    source_reference    TEXT NOT NULL,     -- "UPSC CSE Prelims 2023 — GS Paper I Q47"
    tags                TEXT[],
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_pyq_exam_year     ON exams.pyq_questions (exam_id, year DESC);
CREATE INDEX idx_pyq_subject       ON exams.pyq_questions (subject, chapter);
CREATE INDEX idx_pyq_node          ON exams.pyq_questions (syllabus_node_id)
                                   WHERE syllabus_node_id IS NOT NULL;

-- student_exam_follows
CREATE TABLE exams.student_exam_follows (
    student_id  UUID NOT NULL REFERENCES students(student_id),
    exam_id     UUID NOT NULL REFERENCES exams.exam_catalog(exam_id),
    followed_at TIMESTAMPTZ DEFAULT NOW(),
    alert_prefs JSONB DEFAULT '{"t60":true,"t30":true,"t7":true,"t1":true}',
    PRIMARY KEY (student_id, exam_id)
);

-- student_exam_applications
CREATE TABLE exams.student_exam_applications (
    app_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id           UUID NOT NULL REFERENCES students(student_id),
    exam_id              UUID NOT NULL REFERENCES exams.exam_catalog(exam_id),
    year                 INT NOT NULL,
    status               VARCHAR(30) DEFAULT 'interested'
                         CHECK (status IN ('interested','applied','exam_scheduled',
                                           'appeared','result_awaited','selected',
                                           'waitlisted','rejected','not_applied')),
    registration_number  VARCHAR(50),
    roll_number          VARCHAR(50),
    admit_card_url       TEXT,             -- stored by student, not generated by system
    exam_date            DATE,
    score_obtained       NUMERIC(7,2),
    rank_obtained        INT,
    stage_reached        VARCHAR(20),      -- 'prelims', 'mains', 'interview', 'final'
    notes                TEXT,
    applied_at           TIMESTAMPTZ,
    updated_at           TIMESTAMPTZ DEFAULT NOW()
);

-- exam_salary_data
CREATE TABLE exams.exam_salary_data (
    salary_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_id            UUID NOT NULL REFERENCES exams.exam_catalog(exam_id),
    post_name          VARCHAR(100) NOT NULL,
    pay_level          SMALLINT,          -- 7th CPC Pay Level 1–18
    basic_pay_entry    INT,               -- Rs.
    gross_salary_metro INT,               -- Rs. (X-city HRA)
    gross_salary_tier2 INT,               -- Rs. (Y-city HRA)
    take_home_approx   INT,               -- Rs. (after NPS+tax)
    posting_type       VARCHAR(30),       -- 'field', 'clerical', 'technical', 'gazetted'
    is_gazetted        BOOLEAN DEFAULT FALSE,
    is_all_india       BOOLEAN DEFAULT TRUE,
    pension_type       VARCHAR(20)        -- 'nps', 'ops', 'na'
);

-- exam_physical_standards (NDA, CDS, Police, Paramilitary)
CREATE TABLE exams.exam_physical_standards (
    std_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_id             UUID NOT NULL REFERENCES exams.exam_catalog(exam_id),
    gender              VARCHAR(10),
    category            VARCHAR(20),
    min_height_cm       NUMERIC(5,2),
    min_weight_kg       NUMERIC(5,2),
    chest_cm            NUMERIC(5,2),     -- if applicable
    vision_standard     TEXT,
    other_standards     JSONB
);
```

---

## 4. PYQ Database & Practice

### PYQ Frequency Analysis

```python
# Topic frequency heatmap — which topics are asked most across years
SELECT
    eq.subject,
    eq.chapter,
    eq.topic,
    COUNT(*) AS total_appearances,
    COUNT(DISTINCT eq.year) AS years_appeared,
    AVG(eq.difficulty::numeric_score) AS avg_difficulty,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY eq.subject), 2) AS subject_share_pct
FROM exams.pyq_questions eq
WHERE eq.exam_id = $1
  AND eq.year   >= $2   -- last N years
GROUP BY eq.subject, eq.chapter, eq.topic
ORDER BY total_appearances DESC;
```

### Cross-Exam Overlap Analysis

```python
# Which topics are shared across multiple target exams?
# Student follows: IBPS PO, SSC CGL, UPSC Prelims

def compute_syllabus_overlap(exam_ids: list[str]) -> dict:
    # Get syllabus node sets for each exam
    node_sets = {}
    for exam_id in exam_ids:
        nodes = db.execute("""
            SELECT DISTINCT pq.syllabus_node_id, sn.chapter_title, sn.subject
            FROM   exams.pyq_questions pq
            JOIN   syllabus_nodes sn ON sn.node_id = pq.syllabus_node_id
            WHERE  pq.exam_id = $1
              AND  pq.syllabus_node_id IS NOT NULL
        """, exam_id).fetchall()
        node_sets[exam_id] = {n.syllabus_node_id: n for n in nodes}

    # Find intersection across all exams (common topics)
    common_node_ids = set.intersection(*[set(ns.keys()) for ns in node_sets.values()])

    return {
        "common_topics": [
            {"node_id": nid, "chapter": node_sets[exam_ids[0]][nid].chapter_title}
            for nid in common_node_ids
        ],
        "message": f"Studying these {len(common_node_ids)} topics prepares you for all {len(exam_ids)} exams."
    }
```

### PYQ Practice Integration (Module 22)

```python
# Student selects exam + year → launch practice session

def create_pyq_practice_session(student_id: str, exam_id: str,
                                 year: int, stage: str) -> str:
    questions = db.execute("""
        SELECT pyq_id, question_text, options, correct_answer,
               marks, negative_marks, duration_min
        FROM   exams.pyq_questions
        WHERE  exam_id = $1 AND year = $2 AND stage = $3
        ORDER  BY pyq_id
    """, exam_id, year, stage).fetchall()

    # Create Module 22 mock test session with these questions
    session_id = mock_test_service.create_session(
        student_id  = student_id,
        title       = f"{exam_id} {year} {stage} — PYQ Practice",
        questions   = [q.pyq_id for q in questions],
        time_limit  = sum(q.duration_min for q in questions[:1]),  # paper duration
        source_type = "pyq"
    )
    return session_id
```

---

## 5. Eligibility Checker

```python
# POST /api/v1/exams/eligibility-check/
# No auth required (inputs not stored unless logged in)

class EligibilityCheckRequest(BaseModel):
    date_of_birth:    date
    qualification:    str    # 'class10', 'class12', 'diploma', 'graduate', 'postgraduate'
    category:         str    # 'UR', 'OBC', 'SC', 'ST', 'EWS'
    state_domicile:   str    # ISO state code
    gender:           str    # 'M', 'F', 'O'
    is_exserviceman:  bool = False
    is_pwd:           bool = False

def check_eligibility(req: EligibilityCheckRequest) -> list[dict]:
    today = date.today()

    eligible = db.execute("""
        SELECT ec.exam_id, ec.official_name, ec.acronym, ec.category,
               ec.min_age, ec.max_age, ec.age_cutoff_date_rule,
               ec.min_qualification, ec.attempt_limit
        FROM   exams.exam_catalog ec
        WHERE  ec.is_active = true
          AND  (
              -- Qualification check
              qualification_level($1) >= qualification_level(ec.min_qualification)
          )
          AND  (
              -- Age check (simplified — exact cutoff date logic per exam)
              $2 BETWEEN ec.min_age AND (ec.max_age +
                  CASE $3
                    WHEN 'SC' THEN 5 WHEN 'ST' THEN 5
                    WHEN 'OBC' THEN 3
                    ELSE 0
                  END +
                  CASE WHEN $4 THEN 10 ELSE 0 END  -- PWD
              )
          )
    """, req.qualification, age_today(req.date_of_birth),
         req.category, req.is_pwd).fetchall()

    return [
        {
            "exam_id":   row.exam_id,
            "name":      row.official_name,
            "acronym":   row.acronym,
            "category":  row.category,
            "basis":     "Qualification + age verified",
        }
        for row in eligible
    ]
```

---

## 6. Cut-Off Tracker

### Cut-Off History View

```python
# GET /api/v1/exams/{exam_id}/cutoffs/?stage=prelims&category=UR

def get_cutoff_history(exam_id: str, stage: str, category: str) -> dict:
    rows = db.execute("""
        SELECT year, post_name, cutoff_marks, total_marks, vacancies_filled, normalised
        FROM   exams.exam_cutoffs
        WHERE  exam_id  = $1
          AND  stage    = $2
          AND  category = $3
        ORDER  BY year DESC
        LIMIT  7
    """, exam_id, stage, category).fetchall()

    # Trend analysis
    marks    = [r.cutoff_marks for r in rows]
    slope    = linregress_slope(marks)
    trend    = "increasing" if slope > 0.5 else "decreasing" if slope < -0.5 else "stable"

    return {
        "history": [row._asdict() for row in rows],
        "trend":   trend,
        "trend_slope": slope,
        "message": f"Cut-off is {trend} ({abs(slope):.1f} marks/year on average)."
    }
```

### Mock Score vs Cut-Off Widget

```python
def cutoff_comparison(student_mock_score: float, exam_id: str,
                      category: str, year_count: int = 3) -> dict:
    last_n = db.execute("""
        SELECT year, cutoff_marks
        FROM   exams.exam_cutoffs
        WHERE  exam_id  = $1
          AND  category = $2
          AND  stage    = 'prelims'
        ORDER  BY year DESC
        LIMIT  $3
    """, exam_id, category, year_count).fetchall()

    avg_cutoff = mean(r.cutoff_marks for r in last_n)
    margin     = student_mock_score - avg_cutoff

    return {
        "student_score":    student_mock_score,
        "avg_cutoff":       avg_cutoff,
        "margin":           margin,
        "status":           "ABOVE" if margin > 0 else "BELOW",
        "message":          f"You are {abs(margin):.0f} marks "
                            f"{'above' if margin > 0 else 'below'} the 3-year average cut-off."
    }
```

---

## 7. Exam Calendar & Alerts

### Calendar Events by Student

```python
# GET /api/v1/exams/calendar/?format=json (or ?format=ics)

def get_student_exam_calendar(student_id: str) -> list[dict]:
    return db.execute("""
        SELECT ed.exam_id, ec.acronym, ec.official_name,
               ed.event_type, ed.date, ed.date_range_end,
               ed.is_confirmed, ed.notes
        FROM   exams.exam_dates ed
        JOIN   exams.exam_catalog ec ON ec.exam_id = ed.exam_id
        JOIN   exams.student_exam_follows sef ON sef.exam_id = ed.exam_id
        WHERE  sef.student_id = $1
          AND  ed.year        = EXTRACT(YEAR FROM NOW())
          AND  ed.date        >= CURRENT_DATE
        ORDER  BY ed.date ASC
    """, student_id).fetchall()

def export_ics(events: list[dict]) -> str:
    cal = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//EduForge//Exam Calendar//EN"]
    for e in events:
        cal += [
            "BEGIN:VEVENT",
            f"UID:{e['exam_id']}-{e['event_type']}@eduforge.in",
            f"DTSTART;VALUE=DATE:{e['date'].strftime('%Y%m%d')}",
            f"SUMMARY:[{e['acronym']}] {e['event_type'].replace('_',' ').title()}",
            f"DESCRIPTION:{e['notes'] or ''}",
            "END:VEVENT",
        ]
    cal.append("END:VCALENDAR")
    return "\r\n".join(cal)
```

### Alert Lambda

```python
# EventBridge cron: daily at 7 AM
# Sends alerts for exams with events in T-60, T-30, T-7, T-1 days

def send_exam_date_alerts():
    for threshold in [60, 30, 7, 1]:
        target_date = date.today() + timedelta(days=threshold)

        events = db.execute("""
            SELECT sef.student_id, ec.acronym, ec.official_name, ed.event_type,
                   ed.date, st.fcm_token, st.whatsapp_phone
            FROM   exams.exam_dates ed
            JOIN   exams.exam_catalog ec ON ec.exam_id = ed.exam_id
            JOIN   exams.student_exam_follows sef ON sef.exam_id = ed.exam_id
                   AND (sef.alert_prefs->>('t' || $1))::bool = true
            JOIN   students st ON st.student_id = sef.student_id
            WHERE  ed.date = $2
        """, str(threshold), target_date).fetchall()

        for ev in events:
            event_label = ev.event_type.replace("_", " ").title()
            message = (
                f"[{ev.acronym}] {event_label} is in {threshold} day(s) "
                f"({ev.date.strftime('%d %b %Y')}). "
                f"Make sure you're prepared!"
            )
            send_fcm(ev.fcm_token, title=f"Exam Alert: {ev.acronym}", body=message)
            if threshold <= 7:
                send_whatsapp(ev.whatsapp_phone, message)
```

### Clash Detection

```python
def detect_exam_clashes(student_id: str) -> list[dict]:
    exam_days = db.execute("""
        SELECT ed.date, array_agg(ec.acronym) AS exams_on_day
        FROM   exams.exam_dates ed
        JOIN   exams.exam_catalog ec ON ec.exam_id = ed.exam_id
        JOIN   exams.student_exam_follows sef ON sef.exam_id = ed.exam_id
        WHERE  sef.student_id = $1
          AND  ed.event_type  IN ('exam_prelims', 'exam_mains')
          AND  ed.date        >= CURRENT_DATE
        GROUP  BY ed.date
        HAVING COUNT(*) > 1
    """, student_id).fetchall()

    return [
        {"date": row.date, "clashing_exams": row.exams_on_day,
         "message": f"Clash on {row.date}: {' and '.join(row.exams_on_day)}"}
        for row in exam_days
    ]
```

---

## 8. Preparation Roadmaps

### Roadmap Structure (Stored as Content)

```json
{
  "exam_id": "uuid-ibps-po",
  "duration_months": 6,
  "phases": [
    {
      "phase": 1,
      "title": "Foundation (Month 1–2)",
      "focus": ["Quantitative Aptitude basics", "Verbal Ability grammar"],
      "target_syllabus_nodes": ["uuid-qant-basics", "uuid-verbal-grammar"],
      "mock_tests_per_week": 1,
      "suggested_daily_hours": 3
    },
    {
      "phase": 2,
      "title": "Core Preparation (Month 3–4)",
      "focus": ["Data Interpretation", "Reasoning puzzles", "Banking Awareness"],
      "target_syllabus_nodes": ["uuid-di", "uuid-reasoning-puzzles"],
      "mock_tests_per_week": 2,
      "suggested_daily_hours": 4
    },
    {
      "phase": 3,
      "title": "Revision + Mock Marathon (Month 5–6)",
      "focus": ["Full-length mocks", "PYQ practice", "Current Affairs"],
      "target_syllabus_nodes": [],
      "mock_tests_per_week": 5,
      "suggested_daily_hours": 6
    }
  ]
}
```

### Module 47 Integration (Learning Path Generation)

```python
# When student follows an exam and sets exam date:
# Module 47 generates a personalised study plan merging:
# 1. Exam roadmap phases
# 2. Student's current concept mastery (IRT θ per topic)
# 3. Days remaining to exam

def generate_personalised_prep_plan(student_id: str, exam_id: str,
                                     target_exam_date: date) -> dict:
    roadmap      = get_exam_roadmap(exam_id)
    mastery_gaps = get_concept_gaps(student_id, exam_id)   # from Module 47
    days_left    = (target_exam_date - date.today()).days

    # Prioritise topics by: (roadmap phase weight) × (1 - mastery_score) × (pyq_frequency)
    prioritised  = prioritise_topics(roadmap, mastery_gaps, days_left)

    return {
        "days_to_exam":    days_left,
        "plan":            generate_schedule(prioritised, days_left),
        "mock_test_dates": suggest_mock_test_dates(days_left),
    }
```

---

## 9. Salary & Career Data

### In-Hand Salary Calculator

```python
# GET /api/v1/exams/{exam_id}/salary/?post=IBPS_PO_Scale_I&city_tier=X

def compute_take_home(exam_id: str, post_name: str, city_tier: str) -> dict:
    sd = db.scalar("""
        SELECT basic_pay_entry, pay_level FROM exams.exam_salary_data
        WHERE exam_id = $1 AND post_name = $2
    """, exam_id, post_name)

    basic        = sd.basic_pay_entry
    da_rate      = 0.50          # 50% DA (current as of 2026, updated quarterly)
    hra_rates    = {"X": 0.27, "Y": 0.18, "Z": 0.09}
    ta_flat      = 3600          # Rs. (approx)

    da           = basic * da_rate
    hra          = basic * hra_rates[city_tier]
    gross        = basic + da + hra + ta_flat

    nps_employee = basic * 0.10
    nps_employer = basic * 0.14  # not deducted from employee
    # Income tax: simplified (30% slab on taxable income above Rs. 7L)
    taxable      = max(0, gross * 12 - 700000)
    tax_monthly  = (taxable * 0.30) / 12 if taxable > 0 else 0

    take_home    = gross - nps_employee - tax_monthly

    return {
        "basic":       basic,
        "da":          round(da),
        "hra":         round(hra),
        "ta":          ta_flat,
        "gross":       round(gross),
        "nps_deduction": round(nps_employee),
        "income_tax":  round(tax_monthly),
        "take_home":   round(take_home),
        "city_tier":   city_tier,
        "disclaimer":  "Approximate as per 2026 pay matrix + 50% DA. Actual may vary."
    }
```

---

## 10. API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/v1/exams/catalog/` | Public | Browse all exams (`?category=&state=&mode=`) |
| `GET` | `/api/v1/exams/{exam_id}/` | Public | Full exam detail |
| `GET` | `/api/v1/exams/{exam_id}/pattern/` | Public | Stages, papers, marking scheme |
| `GET` | `/api/v1/exams/{exam_id}/syllabus/` | Public | Linked syllabus tree |
| `GET` | `/api/v1/exams/{exam_id}/dates/` | Public | Upcoming dates this cycle |
| `GET` | `/api/v1/exams/{exam_id}/cutoffs/` | Public | Historical cut-offs by category |
| `GET` | `/api/v1/exams/{exam_id}/pyqs/` | Public | PYQ list (`?year=&subject=&difficulty=`) |
| `POST` | `/api/v1/exams/{exam_id}/pyqs/practice/` | Student | Launch PYQ practice in Module 22 |
| `GET` | `/api/v1/exams/{exam_id}/salary/` | Public | Salary breakdown calculator |
| `GET` | `/api/v1/exams/calendar/` | Student | Student's exam calendar (`?format=ics`) |
| `POST` | `/api/v1/exams/eligibility-check/` | Public | Eligibility checker |
| `GET` | `/api/v1/exams/compare/` | Public | Side-by-side comparison (`?ids=uuid1,uuid2`) |
| `GET` | `/api/v1/exams/overlaps/` | Student | Syllabus overlap across followed exams |
| `POST` | `/api/v1/me/exams/follow/{exam_id}` | Student | Follow exam + alert preferences |
| `DELETE` | `/api/v1/me/exams/follow/{exam_id}` | Student | Unfollow exam |
| `GET` | `/api/v1/me/exams/applications/` | Student | Application tracker |
| `POST` | `/api/v1/me/exams/applications/` | Student | Track new application |
| `PATCH` | `/api/v1/me/exams/applications/{app_id}/` | Student | Update application status/score |
| `GET` | `/api/v1/me/exams/clashes/` | Student | Detect date clashes across followed exams |
| `GET` | `/api/v1/admin/exams/catalog/` | Admin | Full catalog management list |
| `POST` | `/api/v1/admin/exams/catalog/` | Admin | Add new exam |
| `PUT` | `/api/v1/admin/exams/{exam_id}/dates/{date_id}` | Admin | Update exam date (triggers notifications) |
| `POST` | `/api/v1/admin/exams/{exam_id}/pyqs/import` | Admin | Bulk import PYQ CSV |

---

## 11. Flutter App

### Exam Browser

```dart
// Tab bar: All | Banking | Railways | SSC | UPSC | Defence | Teaching | State
DefaultTabController(
  length: 8,
  child: Column(
    children: [
      TabBar(tabs: examCategories.map((c) => Tab(text: c.label)).toList()),
      Expanded(
        child: TabBarView(
          children: examCategories.map((c) =>
            ExamGridView(category: c.id)
          ).toList(),
        ),
      ),
    ],
  ),
)
```

### Application Tracker (Kanban)

```dart
// Drag-and-drop Kanban board for application status
KanbanBoard(
  columns: [
    KanbanColumn(title: 'Interested',      color: Colors.blue,   status: 'interested'),
    KanbanColumn(title: 'Applied',         color: Colors.orange, status: 'applied'),
    KanbanColumn(title: 'Exam Scheduled',  color: Colors.purple, status: 'exam_scheduled'),
    KanbanColumn(title: 'Result Awaited',  color: Colors.amber,  status: 'result_awaited'),
    KanbanColumn(title: 'Selected',        color: Colors.green,  status: 'selected'),
  ],
  items: studentApplications,
  onStatusChange: (appId, newStatus) => AppApi.updateStatus(appId, newStatus),
)
```

---

## 12. Web Interface (HTMX)

### Public Exam Catalog (No Login)

```python
# views.py — publicly accessible, Django cached view (1-hour cache)
@cache_page(3600)
def exam_catalog_public(request):
    category = request.GET.get("category", "all")
    exams    = ExamCatalog.objects.filter(is_active=True)
    if category != "all":
        exams = exams.filter(category=category)
    return render(request, "exams/catalog_public.html", {"exams": exams})
```

```html
<!-- Category filter (HTMX) -->
<div class="category-pills">
  {% for cat in categories %}
  <button hx-get="/exams/catalog/?category={{ cat.id }}"
          hx-target="#exam-grid"
          hx-swap="innerHTML"
          class="pill {% if selected == cat.id %}active{% endif %}">
    {{ cat.icon }} {{ cat.label }}
  </button>
  {% endfor %}
</div>
<div id="exam-grid">
  {% include "exams/_exam_cards.html" %}
</div>
```

### Eligibility Checker (HTMX)

```html
<form hx-post="/exams/eligibility-check/"
      hx-target="#eligibility-results"
      hx-swap="innerHTML"
      hx-indicator="#loading-spinner">
  <input type="date" name="date_of_birth" required>
  <select name="qualification">
    <option value="class10">Class 10 Pass</option>
    <option value="class12">Class 12 Pass</option>
    <option value="graduate">Graduate</option>
    <option value="postgraduate">Post-Graduate</option>
  </select>
  <select name="category">
    <option value="UR">General (UR)</option>
    <option value="OBC">OBC</option>
    <option value="SC">SC</option>
    <option value="ST">ST</option>
    <option value="EWS">EWS</option>
  </select>
  <button type="submit">Check Eligibility</button>
</form>
<div id="eligibility-results"><!-- HTMX injects results here --></div>
```

---

## 13. Background Jobs

| Job | Trigger | Function |
|-----|---------|----------|
| `exam_date_alerts` | EventBridge daily 7 AM | Send FCM/WhatsApp for T-60/30/7/1 day exam events |
| `exam_date_propagation` | `exam.date_updated` event | Notify all followers of updated date |
| `eligibility_window_check` | EventBridge monthly | Alert students who just became eligible for a followed exam |
| `pyq_frequency_compute` | Nightly (after PYQ imports) | Recalculate frequency scores across all PYQs |
| `cutoff_trend_compute` | On new cutoff added | Recompute trend slope per exam × category |
| `clash_detection_notify` | After `exam_dates` update | Run clash check for all students following affected exam |

---

## 14. Content Administration

### Bulk PYQ Import

```python
# POST /api/v1/admin/exams/{exam_id}/pyqs/import
# CSV format: year, stage, paper, subject, chapter, topic, question_text,
#             option_a, option_b, option_c, option_d, correct_answer,
#             explanation, marks, negative_marks, is_memory_based

def import_pyq_csv(exam_id: str, csv_file: IO) -> dict:
    reader = csv.DictReader(csv_file)
    rows   = list(reader)
    imported, failed = 0, 0

    for row in rows:
        try:
            # Validate + clean
            question = PyqQuestion(
                exam_id         = exam_id,
                year            = int(row["year"]),
                stage           = row["stage"],
                question_text   = row["question_text"].strip(),
                options         = {
                    "A": row["option_a"], "B": row["option_b"],
                    "C": row["option_c"], "D": row["option_d"]
                },
                correct_answer  = row["correct_answer"].upper(),
                explanation     = row["explanation"],
                marks           = float(row["marks"]),
                negative_marks  = float(row["negative_marks"] or 0),
                is_memory_based = row["is_memory_based"].lower() == "true",
                source_reference = f"{get_exam_name(exam_id)} {row['year']} — {row['paper']}",
            )
            # Auto-map to syllabus node via chapter name
            question.syllabus_node_id = lookup_syllabus_node(
                row["subject"], row["chapter"]
            )
            db.add(question)
            imported += 1
        except Exception as e:
            failed += 1
            log_import_error(row, str(e))

    db.commit()
    return {"imported": imported, "failed": failed}
```

---

## 15. DPDPA & Compliance

| Aspect | Implementation |
|--------|---------------|
| **Public data** | Exam catalog (dates, pattern, cut-offs, salary) is public information — no personal data. Browsable without login. |
| **Eligibility checker** | DOB/category inputs used for one-time computation. Not stored unless student is logged in. If logged in → stored in `student_exam_applications` under student's own profile. |
| **Application tracker** | Entirely student-controlled personal data. Stored under student profile. Standard Module 42 retention (2 years after account closure). |
| **PYQ copyright** | Every question attributed with `source_reference` ("UPSC CSE Prelims 2023 — GS Paper I"). EduForge does not claim authorship of official questions. Memory-based questions labelled clearly as unofficial. |
| **No generated links** | Official website URLs stored as static text fields entered by admin. System never LLM-generates external URLs. |
| **Audit log** | Admin date/cutoff/vacancy updates logged to Module 42 audit events. |
