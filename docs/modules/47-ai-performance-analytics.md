# Module 47 — AI Performance Analytics

## 1. Purpose & Scope

AI Performance Analytics transforms raw activity data from every EduForge module into actionable intelligence for students, teachers, parents, and administrators. It does not merely display charts — it predicts outcomes, explains why, recommends what to do next, and nudges stakeholders to act.

The system ingests events from 10+ source modules, engineers 42 ML features per student, trains XGBoost models on SageMaker, serves predictions via a serverless endpoint, and delivers insights through role-specific dashboards in Flutter and HTMX.

**What it produces:**

| Consumer | Key Output |
|----------|-----------|
| Student | Predicted exam score ± CI, concept mastery grid, personalised daily study plan |
| Teacher | At-risk student list, class topic-gap heatmap, reteach suggestions |
| Parent | Plain-language weekly digest, drop alerts, predicted grade |
| Admin | Institution benchmark, cohort tracker, NIRF-ready performance report |

**Scope boundaries:**
- Source data collected by other modules; this module only reads and derives insights — no direct student-facing entry forms
- Doubt solving handled by Module 46; recommendations from this module deep-link to Module 46 for specific questions
- Adaptive difficulty of exam questions handled by Module 18/22; this module feeds the signal

---

## 2. Data Ingestion Architecture

All events are published to an EventBridge custom bus `eduforge.performance` by source modules. This module consumes them without any API coupling.

```
Source Module Events (EventBridge bus: eduforge.performance)
  │
  ├─ exam.result_published           (Module 20/21)
  ├─ attendance.daily_marked         (Modules 11/12/13)
  ├─ homework.graded                 (Module 14)
  ├─ video.progress_updated          (Module 44)
  ├─ doubt.resolved                  (Module 46)
  ├─ live_class.session_ended        (Module 45)
  ├─ mock_test.result_published      (Module 22)
  └─ leaderboard.rank_updated        (Module 23)
        │
        ▼
  Lambda `feature_extractor`
        ├─ Compute delta features from event payload
        ├─ Upsert to SageMaker Feature Store (online — DynamoDB, < 10ms)
        └─ Write raw event to Kinesis Firehose → S3 feature lake (Parquet GZIP)

  S3 Feature Lake  (partitioned by tenant_id/year/month/day/)
        └─ AWS Glue crawler (nightly 2 AM) → Glue Data Catalog
        └─ Amazon Athena external table `student_raw_events`
```

### Feature Groups (SageMaker Feature Store)

```python
# Feature Group definition
feature_group = FeatureGroup(
    name            = "student-academic-features",
    sagemaker_session = session,
)
feature_group.feature_definitions = [
    FeatureDefinition("student_id",                    FeatureTypeEnum.STRING),
    FeatureDefinition("tenant_id",                     FeatureTypeEnum.STRING),
    FeatureDefinition("event_time",                    FeatureTypeEnum.STRING),  # ISO8601
    # Rolling score features
    FeatureDefinition("avg_score_7d",                  FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition("avg_score_30d",                 FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition("avg_score_90d",                 FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition("score_slope_5exams",            FeatureTypeEnum.FRACTIONAL),  # linear regression slope
    FeatureDefinition("score_std_dev",                 FeatureTypeEnum.FRACTIONAL),  # consistency
    # Attendance
    FeatureDefinition("attendance_rate_30d",           FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition("attendance_streak_days",        FeatureTypeEnum.INTEGRAL),
    # Engagement
    FeatureDefinition("video_completion_rate_30d",     FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition("homework_submission_rate_30d",  FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition("live_class_attendance_rate",    FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition("doubt_count_7d",                FeatureTypeEnum.INTEGRAL),
    FeatureDefinition("engagement_composite",          FeatureTypeEnum.FRACTIONAL),
    # Peer comparison
    FeatureDefinition("peer_percentile_class",         FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition("peer_percentile_board",         FeatureTypeEnum.FRACTIONAL),
    # Time features
    FeatureDefinition("days_since_last_exam",          FeatureTypeEnum.INTEGRAL),
    FeatureDefinition("last_activity_hour",            FeatureTypeEnum.INTEGRAL),
    # Subject-specific (6 subjects × 3 features = 18)
    FeatureDefinition("math_avg_30d",                  FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition("math_slope",                    FeatureTypeEnum.FRACTIONAL),
    FeatureDefinition("math_irt_theta",                FeatureTypeEnum.FRACTIONAL),
    # ... physics, chemistry, biology, english, social
]
```

---

## 3. ML Model Architecture

### 3.1 Model Inventory

| Model | Type | Algorithm | Prediction | Retrain |
|-------|------|-----------|-----------|---------|
| `score_predictor` | Regression | XGBoost | Next exam score (0–100) | Weekly |
| `at_risk_classifier` | Binary classification | XGBoost | P(score < 35%) | Weekly |
| `dropout_predictor` | Survival model | Cox PH → XGBoost | P(dropout in 30 days) | Weekly |
| `irt_calibrator` | IRT (3-PL) | `py-irt` | Per-concept mastery θ | After each exam |
| `content_recommender` | Collaborative filtering | ALS (implicit) | Video/notes per weak concept | Weekly |
| `vam_calculator` | Regression | Linear (OLS) | Teacher value-add vs baseline | Per exam cycle |

### 3.2 Training Pipeline (Step Functions — Sundays 1 AM)

```
Step Functions State Machine: weekly_model_retrain

State 1: GlueJobRun
  └─ Aggregate last-90-days S3 feature lake into SageMaker training data CSV

State 2: SageMakerTrainingJob (score_predictor)
  └─ XGBoost built-in algorithm
  └─ Objective: reg:squarederror
  └─ Hyperparameters: max_depth=6, n_estimators=300, learning_rate=0.05
  └─ Train/val split: 80/20 stratified by tenant_id

State 3: SageMakerModelEvaluation
  └─ Compute RMSE, MAE, R² on validation set
  └─ Compare to current production model RMSE
  └─ If improved by > 1% → promote; else keep current

State 4: RegisterModel
  └─ MLflow model registry: version tag, accuracy metrics, feature importance

State 5: UpdateEndpoint
  └─ SageMaker Serverless Endpoint update (zero-downtime blue/green)
```

### 3.3 Nightly Prediction Pipeline (Step Functions — 2 AM daily)

```
State 1: GlueAggregateFeatures
  └─ Pull latest features from Feature Store for all active students

State 2: SageMakerBatchTransform
  └─ Input:  s3://eduforge-ml/batch-input/YYYY-MM-DD/students.csv
  └─ Output: s3://eduforge-ml/batch-output/YYYY-MM-DD/predictions.csv
  └─ Transform instance: ml.m5.large (spot pricing = 70% savings)

State 3: Lambda store_predictions
  └─ Parse predictions.csv → upsert student_predictions table

State 4: Lambda generate_recommendations
  └─ For each student: fetch concept mastery gaps → match to content → upsert learning_recommendations

State 5: Lambda trigger_alerts
  └─ Students with dropout_prob > 0.70 → queue parent push notification
  └─ Students with at_risk_prob > 0.75 → add to teacher at-risk list
```

---

## 4. Feature Engineering

```python
# Lambda feature_extractor — processes each EventBridge event

def compute_features(student_id: str, event_type: str, payload: dict) -> dict:
    now = datetime.utcnow()

    features = {}

    if event_type == "exam.result_published":
        # Fetch last 10 exam scores from DB
        scores = get_recent_scores(student_id, n=10)
        features["avg_score_7d"]         = mean_in_window(scores, days=7)
        features["avg_score_30d"]        = mean_in_window(scores, days=30)
        features["score_slope_5exams"]   = linregress_slope([s.score for s in scores[-5:]])
        features["score_std_dev"]        = stdev([s.score for s in scores])

    if event_type == "attendance.daily_marked":
        att = get_attendance_history(student_id, days=30)
        features["attendance_rate_30d"]  = sum(att.present) / len(att)
        features["attendance_streak"]    = current_streak(att)

    # Engagement composite
    features["engagement_composite"] = (
        0.35 * features.get("attendance_rate_30d",   0.5) +
        0.25 * get_video_completion_rate(student_id, days=30) +
        0.25 * get_homework_submission_rate(student_id, days=30) +
        0.15 * get_live_class_attendance_rate(student_id, days=30)
    )

    # Peer percentile (cached, updated daily)
    features["peer_percentile_class"] = compute_percentile(
        student_id, scope="class", score=features.get("avg_score_30d", 50)
    )

    return features
```

### Forgetting Curve Feature

```python
# Based on Ebbinghaus forgetting model: R = e^(-t/S)
# t = days since last revision, S = stability (concept difficulty proxy)
# Feature: "forgetting_risk" per concept

def forgetting_risk(concept_mastery: ConceptMastery) -> float:
    days_since = (datetime.utcnow() - concept_mastery.last_assessed_at).days
    stability  = concept_mastery.questions_attempted / max(1, concept_mastery.questions_correct)
    return math.exp(-days_since / max(stability, 1.0))

# Concepts with forgetting_risk < 0.5 flagged for spaced repetition
```

---

## 5. IRT Concept Mastery Model

Item Response Theory (3-parameter logistic model) gives a continuous mastery score (θ) per student per concept, based on which questions they got right across all exams and mock tests.

```python
# py-irt library — 3PL model
# a = discrimination, b = difficulty, c = guessing
# P(correct | θ) = c + (1-c) / (1 + exp(-a(θ - b)))

from py_irt.training import train_irt

responses = fetch_all_responses(student_id, concept_id)
# responses: list of {item_id, correct (0/1), difficulty (b param from QB)}

model = train_irt(responses, model="3pl", epochs=200)
theta = model.get_theta(student_id)   # -3 to +3 scale
```

### Mastery Level Classification

| θ Range | Level | Colour | Action |
|---------|-------|--------|--------|
| θ < -1.0 | Not Started / Very Weak | 🔴 Red | Urgent study recommendation |
| -1.0 ≤ θ < 0.5 | Partial Understanding | 🟡 Yellow | Practice + revision |
| θ ≥ 0.5 | Mastered | 🟢 Green | Spaced repetition only |

---

## 6. Explainable AI (XAI)

### SHAP Value Computation

```python
import shap
import xgboost as xgb

def compute_shap_explanation(student_features: dict, exam_id: str) -> dict:
    model     = load_production_model("score_predictor")
    explainer = shap.TreeExplainer(model)
    features  = pd.DataFrame([student_features])
    shap_vals = explainer.shap_values(features)[0]   # array of shape (42,)

    feature_names = features.columns.tolist()
    top_positive  = sorted(zip(feature_names, shap_vals), key=lambda x: x[1], reverse=True)[:5]
    top_negative  = sorted(zip(feature_names, shap_vals), key=lambda x: x[1])[:5]

    return {
        "predicted_score":   float(model.predict(features)[0]),
        "base_value":        float(explainer.expected_value),
        "top_positive":      top_positive,   # what helps
        "top_negative":      top_negative,   # what hurts
        "all_shap_values":   dict(zip(feature_names, shap_vals.tolist())),
    }
```

### Natural Language Explanation (Claude Haiku)

```python
def generate_nl_explanation(shap_result: dict, language: str = "en") -> str:
    factors = []
    for feat, val in shap_result["top_positive"]:
        factors.append(f"{human_label(feat)} is helping (+{val:.1f} marks)")
    for feat, val in shap_result["top_negative"]:
        factors.append(f"{human_label(feat)} is hurting ({val:.1f} marks)")

    prompt = f"""
You are EduForge AI. Explain in 2 sentences (friendly, encouraging) why a student's
predicted score is {shap_result['predicted_score']:.0f}%.

Factors:
{chr(10).join(factors)}

Language: {language}
Tone: encouraging, practical. No jargon. Max 50 words.
"""
    response = bedrock.invoke_model(
        modelId="anthropic.claude-haiku-4-5-20251001",
        body=json.dumps({"messages": [{"role": "user", "content": prompt}], "max_tokens": 100})
    )
    return response["content"][0]["text"]
```

### "What If" Simulator

```python
# POST /api/v1/me/analytics/whatif/
# Body: {"attendance_rate": 0.90, "video_completion": 0.85}
# Returns: updated prediction

def simulate_prediction(student_id: str, overrides: dict) -> dict:
    base_features = get_current_features(student_id)
    sim_features  = {**base_features, **overrides}

    model         = load_production_model("score_predictor")
    base_pred     = model.predict(pd.DataFrame([base_features]))[0]
    sim_pred      = model.predict(pd.DataFrame([sim_features]))[0]

    return {
        "current_prediction":   float(base_pred),
        "simulated_prediction": float(sim_pred),
        "delta":                float(sim_pred - base_pred),
        "message": f"Improving attendance to {overrides.get('attendance_rate', 0)*100:.0f}% "
                   f"would improve your predicted score by {sim_pred - base_pred:+.1f} marks.",
    }
```

---

## 7. Personalised Learning Path Engine

### Gap → Content Matching

```python
def generate_recommendations(student_id: str, tenant_id: str) -> list[dict]:
    # Step 1: Find red/yellow concepts ordered by exam importance
    gaps = db.execute("""
        SELECT cm.concept_id, sn.chapter_title, sn.importance_weight,
               cm.irt_theta, cm.mastery_level
        FROM   concept_mastery cm
        JOIN   syllabus_nodes sn ON sn.node_id = cm.concept_id
        WHERE  cm.student_id  = $1
          AND  cm.mastery_level IN ('RED','YELLOW')
          AND  cm.tenant_id   = $2
        ORDER  BY sn.importance_weight DESC, cm.irt_theta ASC
        LIMIT  10
    """, student_id, tenant_id).fetchall()

    recommendations = []
    for gap in gaps:
        # Find best video chapter for this concept
        video = db.scalar("""
            SELECT vc.chapter_id, vc.title, vc.video_id, vc.start_seconds
            FROM   video_chapters vc
            JOIN   videos v ON v.video_id = vc.video_id
            WHERE  $1 = ANY(vc.concept_tags)
              AND  v.tenant_id = $2
              AND  v.is_published = true
            ORDER  BY vc.view_count DESC LIMIT 1
        """, gap.concept_id, tenant_id)

        # Find top MCQ set for this concept
        mcq_set = db.scalar("""
            SELECT qb_item_id FROM question_bank_items
            WHERE  $1 = ANY(concept_tags)
              AND  tenant_id = $2
              AND  difficulty = 'MEDIUM'
            ORDER BY usage_count DESC LIMIT 5
        """, gap.concept_id, tenant_id)

        recommendations.append({
            "concept_id":   gap.concept_id,
            "concept_title": gap.chapter_title,
            "irt_theta":    gap.irt_theta,
            "priority":     gap.importance_weight,
            "video":        video,
            "mcq_set":      mcq_set,
            "reason": f"You scored below threshold on {gap.chapter_title} questions "
                      f"(mastery score: {gap.irt_theta:.2f})"
        })

    return recommendations
```

### Study Schedule Generator

```python
def generate_study_schedule(student_id: str, exam_date: date) -> list[dict]:
    days_remaining = (exam_date - date.today()).days
    gaps           = get_concept_gaps(student_id, max_gaps=8)
    daily_hours    = get_available_study_hours(student_id)  # from historical activity

    # Topological sort: prerequisites first
    ordered_gaps = topological_sort_concepts(gaps)

    schedule = []
    day       = 0
    for concept in ordered_gaps:
        study_hours   = concept.estimated_hours_to_close_gap
        sessions_need = math.ceil(study_hours / daily_hours)
        for i in range(sessions_need):
            if day >= days_remaining:
                break
            schedule.append({
                "date":    (date.today() + timedelta(days=day)).isoformat(),
                "concept": concept.title,
                "activity": f"Watch video + do {concept.mcq_count} practice MCQs",
                "duration": f"{daily_hours:.1f} hours",
            })
            day += 1

    # Pad remaining days with spaced repetition of green concepts
    for remaining_day in range(day, days_remaining):
        schedule.append({
            "date":     (date.today() + timedelta(days=remaining_day)).isoformat(),
            "concept":  "Revision",
            "activity": "Full-length mock test + review errors",
        })

    return schedule
```

### Spaced Repetition Scheduler

```python
# Leitner box implementation
# Box 1 (Red): review every 1 day
# Box 2 (Yellow): review every 3 days
# Box 3 (Green): review every 7 days

def get_due_for_revision(student_id: str) -> list[str]:
    return db.execute("""
        SELECT concept_id, chapter_title
        FROM   concept_mastery
        WHERE  student_id = $1
          AND  (
              (mastery_level = 'RED'    AND last_assessed_at < NOW() - INTERVAL '1 day')  OR
              (mastery_level = 'YELLOW' AND last_assessed_at < NOW() - INTERVAL '3 days') OR
              (mastery_level = 'GREEN'  AND last_assessed_at < NOW() - INTERVAL '7 days')
          )
        ORDER  BY last_assessed_at ASC
    """, student_id).fetchall()
```

---

## 8. Teacher Value-Added Model (VAM)

```python
# VAM: compare actual class improvement to predicted improvement
# Controls for student baseline (prior exam score average)

def compute_vam(teacher_id: str, class_ids: list[str], term_id: str) -> float:
    students = get_students_for_classes(class_ids)

    # For each student: get baseline score (term start) and final score (term end)
    rows = []
    for s in students:
        baseline = get_baseline_score(s.student_id, term_id)
        final    = get_final_score(s.student_id, term_id)
        rows.append({"baseline": baseline, "final": final})

    df = pd.DataFrame(rows)

    # Expected improvement: linear model fitted on all students in tenant
    model            = load_production_model("baseline_improvement_predictor")
    df["expected"]   = model.predict(df[["baseline"]])
    df["residual"]   = df["final"] - df["expected"]

    vam_score        = df["residual"].mean()   # positive = above expected

    db.execute("""
        INSERT INTO teacher_vam_scores
            (teacher_id, term_id, expected_improvement, actual_improvement,
             vam_score, student_count, computed_at)
        VALUES ($1, $2, $3, $4, $5, $6, NOW())
        ON CONFLICT (teacher_id, term_id) DO UPDATE
            SET vam_score = EXCLUDED.vam_score
    """, teacher_id, term_id,
         float(df["expected"].mean()), float(df["final"].mean()),
         float(vam_score), len(rows))

    return vam_score
```

**VAM Access Rules:**
- Admin only — row-level security on `teacher_vam_scores`: `USING (current_setting('app.role') = 'admin')`
- Teachers see only class performance, not their own VAM rank
- VAM used only with explicit admin permission for HR decisions (Module 8 appraisal integration)

---

## 9. At-Risk & Dropout Detection

### At-Risk (Score < 35% in Next Exam)

```python
# XGBoost binary classifier
# Label: exam_score < 35 → 1 (at risk), else 0

# Threshold tuning: maximise F2-score (recall more important than precision)
# — better to flag a student who's actually fine than to miss a failing student

RISK_THRESHOLD = 0.65   # probability threshold for "at risk" label

def is_at_risk(prediction_proba: float) -> bool:
    return prediction_proba >= RISK_THRESHOLD
```

### Dropout Predictor

```python
# Features: days_since_last_login, attendance_drop_7d,
#           fee_overdue_days, doubt_count_drop, consecutive_homework_missed

# Cox proportional hazard model → XGBoost approximation:
# event = "student stops appearing for 30 days"
# trained on 2 years of historical data

def compute_dropout_risk(student_id: str) -> float:
    features = get_features(student_id)
    model    = load_production_model("dropout_predictor")
    return float(model.predict_proba(pd.DataFrame([features]))[0][1])
```

### Alert Thresholds

| Dropout Risk | At-Risk Score | Action |
|-------------|---------------|--------|
| > 0.85 | Any | Immediate parent push + teacher alert |
| 0.70–0.85 | > 0.65 | Teacher alert in next morning digest |
| 0.50–0.70 | > 0.75 | Teacher nudge: "Consider checking in" |
| < 0.50 | > 0.65 | Appear in at-risk list; no push |

---

## 10. Student Dashboard — Flutter

### Radar Chart (Subject Performance)

```dart
RadarChart(
  RadarChartData(
    radarShape: RadarShape.polygon,
    dataSets: [
      RadarDataSet(
        fillColor: Colors.blue.withOpacity(0.2),
        borderColor: Colors.blue,
        dataEntries: [
          RadarEntry(value: student.mathScore),
          RadarEntry(value: student.physicsScore),
          RadarEntry(value: student.chemScore),
          RadarEntry(value: student.bioScore),
          RadarEntry(value: student.englishScore),
          RadarEntry(value: student.ssScore),
        ],
      ),
      // Class average overlay
      RadarDataSet(
        fillColor: Colors.grey.withOpacity(0.1),
        borderColor: Colors.grey,
        dataEntries: [/* class averages */],
      ),
    ],
    titleTextStyle: const TextStyle(fontSize: 12),
    tickCount: 5,
    ticksTextStyle: const TextStyle(fontSize: 8),
  ),
)
```

### Exam Readiness Gauge

```dart
AnimatedCircularGauge(
  value: readinessScore,          // 0–100
  minValue: 0,
  maxValue: 100,
  arcType: ArcType.HALF,
  arcBackgroundColor: Colors.grey[200]!,
  arcColor: _readinessColor(readinessScore),
  child: Text(
    '${readinessScore.toStringAsFixed(0)}%',
    style: Theme.of(context).textTheme.headlineLarge,
  ),
)
```

### Concept Mastery Grid

```dart
GridView.builder(
  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 4,
    mainAxisSpacing: 4,
    crossAxisSpacing: 4,
  ),
  itemCount: concepts.length,
  itemBuilder: (ctx, i) {
    final c = concepts[i];
    return GestureDetector(
      onTap: () => _showConceptDetail(c),  // open recommendation sheet
      child: Container(
        color: _masteryColor(c.masteryLevel),
        child: Center(
          child: Text(c.shortTitle, style: const TextStyle(fontSize: 9)),
        ),
      ),
    );
  },
)
```

### "Study Now" Recommendation Card

```dart
// Tapping deep-links to the exact video chapter
RecommendationCard(
  title: recommendation.conceptTitle,
  subtitle: 'Watch 12-min video + 5 practice questions',
  irtTheta: recommendation.irtTheta,
  onTap: () {
    if (recommendation.videoId != null) {
      context.push('/videos/${recommendation.videoId}?start=${recommendation.startSeconds}');
    }
  },
)
```

---

## 11. Teacher Dashboard — Web (HTMX)

### At-Risk List

```html
<!-- HTMX filter: updates list when class/subject changes -->
<div id="at-risk-list"
     hx-get="/teacher/analytics/at-risk/"
     hx-trigger="load, change from:#class-filter"
     hx-include="#class-filter"
     hx-swap="innerHTML">
  Loading…
</div>

<!-- One-click parent alert -->
{% for student in at_risk_students %}
<tr>
  <td>{{ student.name }}</td>
  <td>{{ (student.at_risk_prob * 100)|round }}%</td>
  <td>{{ student.main_risk_factor }}</td>
  <td>
    <button
      hx-post="/teacher/alert-parent/{{ student.id }}/"
      hx-confirm="Send alert to {{ student.parent_name }}?"
      hx-swap="outerHTML"
      class="btn btn-warning btn-sm">
      Alert Parent
    </button>
  </td>
</tr>
{% endfor %}
```

### Topic Gap Heatmap

```python
# views.py — topic gap data for Chart.js heatmap
def topic_gap_heatmap(request):
    data = db.execute("""
        SELECT sn.chapter_title,
               AVG(CASE WHEN ea.score < 40 THEN 1.0 ELSE 0.0 END) AS fail_rate,
               COUNT(*) AS attempts
        FROM   exam_answers ea
        JOIN   question_bank_items qbi ON qbi.item_id = ea.question_id
        JOIN   syllabus_nodes sn       ON sn.node_id = ANY(qbi.concept_tags)
        WHERE  ea.class_id = ANY($1)
          AND  ea.exam_date >= NOW() - INTERVAL '30 days'
        GROUP  BY sn.chapter_title
        ORDER  BY fail_rate DESC
    """, teacher.class_ids).fetchall()
    return JsonResponse({"labels": [r.chapter_title for r in data],
                         "data":   [r.fail_rate for r in data]})
```

---

## 12. Parent Dashboard

```python
# GET /api/v1/parent/analytics/child/{student_id}/
# Requires: parental_access_verified = True (Module 09)

class ParentAnalyticsView(APIView):
    def get(self, request, student_id):
        student     = verify_parent_child(request.user, student_id)
        prediction  = get_latest_prediction(student_id)
        explanation = get_nl_explanation(student_id, language=student.parent_language)
        mastery     = get_top_weak_concepts(student_id, n=3)
        study_habit = get_optimal_study_window(student_id)

        return Response({
            "student_name":      student.name,
            "predicted_grade":   score_to_grade(prediction.predicted_score),
            "predicted_score":   f"{prediction.predicted_score:.0f}%",
            "confidence_range":  f"{prediction.confidence_lower:.0f}–{prediction.confidence_upper:.0f}%",
            "explanation":       explanation,
            "weak_subjects":     [c.chapter_title for c in mastery],
            "optimal_study_time": study_habit,
            "at_risk":           prediction.at_risk_prob > 0.65,
        })
```

### Weekly WhatsApp Digest (Module 36 Integration)

```python
# EventBridge cron: every Sunday 9 AM
def send_weekly_parent_digest(student_id: str):
    data    = get_parent_analytics(student_id)
    message = f"""
📊 *EduForge Weekly Report — {data['student_name']}*

✅ Strength: {data['top_subject']}
⚠️ Needs practice: {data['weak_subjects'][0]}
📈 Predicted grade next exam: *{data['predicted_grade']}*

Study tip: {data['student_name']} studies best between {data['optimal_study_time']}

View full report: {data['dashboard_url']}
"""
    send_whatsapp(parent_phone, message)
```

---

## 13. Data Model

```sql
-- student_performance_features: one row per student per day (written by feature_extractor)
CREATE TABLE analytics.student_performance_features (
    feature_id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id                UUID NOT NULL REFERENCES students(student_id),
    tenant_id                 UUID NOT NULL REFERENCES tenants(tenant_id),
    as_of_date                DATE NOT NULL,
    avg_score_7d              NUMERIC(5,2),
    avg_score_30d             NUMERIC(5,2),
    avg_score_90d             NUMERIC(5,2),
    score_slope_5exams        NUMERIC(6,4),
    score_std_dev             NUMERIC(5,2),
    attendance_rate_30d       NUMERIC(5,4),
    attendance_streak_days    INT,
    video_completion_rate_30d NUMERIC(5,4),
    homework_submission_rate  NUMERIC(5,4),
    live_class_rate           NUMERIC(5,4),
    doubt_count_7d            INT,
    engagement_composite      NUMERIC(5,4),
    peer_percentile_class     NUMERIC(5,2),
    peer_percentile_board     NUMERIC(5,2),
    days_since_last_exam      INT,
    created_at                TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (student_id, as_of_date)
);

CREATE INDEX idx_spf_tenant_date ON analytics.student_performance_features (tenant_id, as_of_date);

-- student_predictions: results of nightly batch inference
CREATE TABLE analytics.student_predictions (
    prediction_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id        UUID NOT NULL REFERENCES students(student_id),
    tenant_id         UUID NOT NULL REFERENCES tenants(tenant_id),
    exam_id           UUID REFERENCES exam_sessions(session_id),
    predicted_score   NUMERIC(5,2),
    confidence_lower  NUMERIC(5,2),
    confidence_upper  NUMERIC(5,2),
    at_risk_prob      NUMERIC(5,4),    -- P(score < 35%)
    dropout_prob      NUMERIC(5,4),    -- P(dropout in 30 days)
    readiness_score   NUMERIC(5,2),    -- 0–100 for specific exam
    model_version     VARCHAR(30),
    predicted_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sp_student_latest ON analytics.student_predictions (student_id, predicted_at DESC);

-- concept_mastery: IRT θ per student per concept
CREATE TABLE analytics.concept_mastery (
    mastery_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id          UUID NOT NULL REFERENCES students(student_id),
    tenant_id           UUID NOT NULL REFERENCES tenants(tenant_id),
    concept_id          UUID NOT NULL REFERENCES syllabus_nodes(node_id),
    irt_theta           NUMERIC(6,4) DEFAULT 0.0,
    mastery_level       VARCHAR(6) DEFAULT 'RED'
                        CHECK (mastery_level IN ('RED','YELLOW','GREEN')),
    questions_attempted INT DEFAULT 0,
    questions_correct   INT DEFAULT 0,
    last_assessed_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (student_id, concept_id)
);

-- learning_recommendations: personalised content links
CREATE TABLE analytics.learning_recommendations (
    rec_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id         UUID NOT NULL REFERENCES students(student_id),
    tenant_id          UUID NOT NULL REFERENCES tenants(tenant_id),
    concept_id         UUID REFERENCES syllabus_nodes(node_id),
    priority_rank      SMALLINT NOT NULL,    -- 1 = highest priority
    rec_type           VARCHAR(10) NOT NULL
                       CHECK (rec_type IN ('video','notes','mcq_set','mock_test')),
    content_id         UUID NOT NULL,        -- FK to respective module table
    content_start_sec  INT,                  -- for videos: start timestamp
    reason_text        TEXT,
    shap_contribution  NUMERIC(6,4),
    generated_at       TIMESTAMPTZ DEFAULT NOW(),
    acted_on           BOOLEAN DEFAULT FALSE,
    acted_on_at        TIMESTAMPTZ
);

CREATE INDEX idx_lr_student_priority
ON analytics.learning_recommendations (student_id, priority_rank)
WHERE acted_on = FALSE;

-- teacher_vam_scores: admin-only
CREATE TABLE analytics.teacher_vam_scores (
    vam_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    teacher_id           UUID NOT NULL REFERENCES staff(staff_id),
    subject              VARCHAR(50),
    class_level          SMALLINT,
    term_id              UUID REFERENCES academic_terms(term_id),
    expected_improvement NUMERIC(5,2),
    actual_improvement   NUMERIC(5,2),
    vam_score            NUMERIC(6,4),   -- positive = above expected
    student_count        INT,
    computed_at          TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (teacher_id, term_id, subject)
);

-- Row-level security: only admin role can read
ALTER TABLE analytics.teacher_vam_scores ENABLE ROW LEVEL SECURITY;
CREATE POLICY vam_admin_only ON analytics.teacher_vam_scores
    USING (current_setting('app.role', true) = 'admin');

-- prediction_explanations: SHAP + natural language
CREATE TABLE analytics.prediction_explanations (
    exp_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prediction_id  UUID NOT NULL REFERENCES analytics.student_predictions(prediction_id),
    shap_values    JSONB NOT NULL,
    nl_explanation TEXT,
    language       VARCHAR(10) DEFAULT 'en',
    generated_at   TIMESTAMPTZ DEFAULT NOW()
);

-- analytics_opt_out: DPDPA right to opt-out
CREATE TABLE analytics.analytics_opt_out (
    student_id    UUID PRIMARY KEY REFERENCES students(student_id),
    opted_out_at  TIMESTAMPTZ DEFAULT NOW(),
    opt_out_reason TEXT
);

-- concept_prerequisites: DAG for learning sequence
CREATE TABLE analytics.concept_prerequisites (
    parent_concept_id UUID NOT NULL REFERENCES syllabus_nodes(node_id),
    child_concept_id  UUID NOT NULL REFERENCES syllabus_nodes(node_id),
    PRIMARY KEY (parent_concept_id, child_concept_id)
);
```

---

## 14. API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/v1/me/analytics/dashboard/` | Student | Radar, predictions, mastery grid, recommendations |
| `GET` | `/api/v1/me/analytics/recommendations/` | Student | Today's personalised study plan with content deep-links |
| `GET` | `/api/v1/me/analytics/readiness/{exam_id}/` | Student | Exam readiness score + SHAP explanation |
| `POST` | `/api/v1/me/analytics/whatif/` | Student | Simulate feature change → updated prediction |
| `GET` | `/api/v1/me/analytics/mastery/` | Student | Concept mastery grid (all subjects) |
| `GET` | `/api/v1/me/analytics/schedule/` | Student | AI-generated study schedule to next exam |
| `POST` | `/api/v1/me/analytics/opt-out/` | Student | DPDPA opt-out from AI predictions |
| `GET` | `/api/v1/teacher/analytics/at-risk/` | Teacher | At-risk list for teacher's classes |
| `GET` | `/api/v1/teacher/analytics/topic-gaps/` | Teacher | Class-level weak topic heatmap |
| `GET` | `/api/v1/teacher/analytics/student/{id}/` | Teacher | Individual student full analytics |
| `POST` | `/api/v1/teacher/alert-parent/{student_id}/` | Teacher | Send parent alert for at-risk student |
| `GET` | `/api/v1/admin/analytics/institution/` | Admin | Institution benchmark + NIRF performance |
| `GET` | `/api/v1/admin/analytics/cohort/` | Admin | Cohort tracker (admission year → current) |
| `GET` | `/api/v1/admin/analytics/vam/` | Admin | Teacher VAM scores |
| `GET` | `/api/v1/parent/analytics/child/{student_id}/` | Parent | Parent dashboard (verified guardian only) |

---

## 15. Background Jobs

| Job | Trigger | Function |
|-----|---------|----------|
| `feature_extractor` | EventBridge (all performance events) | Delta feature computation → Feature Store update |
| `nightly_prediction_pipeline` | EventBridge cron `0 2 * * ?` | Batch inference → store predictions → generate recommendations |
| `weekly_model_retrain` | EventBridge cron `0 1 ? * SUN *` | Retrain all models → evaluate → promote if improved |
| `irt_calibrator` | On `exam.result_published` | Re-compute IRT θ for all students who took exam |
| `sla_dropout_alert` | EventBridge cron `0 8 * * ?` | Identify dropout_prob > 0.70 → queue parent push |
| `parent_weekly_digest` | EventBridge cron `0 9 ? * SUN *` | Generate + send WhatsApp digests to all parents |
| `drift_monitor` | EventBridge cron `0 9 * * ?` | Compare model accuracy vs prior week → alert if drift > 5% |
| `bias_audit` | EventBridge cron `0 0 1 * ?` | Monthly fairness metrics across demographic groups |
| `analytics_retention_cleanup` | EventBridge cron `0 2 1 * ?` | Purge predictions > 1 year; features > 2 years |

---

## 16. Competitive Exam Readiness

```python
# Readiness = weighted percentile across subject areas vs cutoff benchmark

JEE_MAIN_BENCHMARKS = {
    "mathematics": {"general_cutoff_percentile": 90},
    "physics":     {"general_cutoff_percentile": 85},
    "chemistry":   {"general_cutoff_percentile": 82},
}

def compute_jee_readiness(student_id: str) -> dict:
    features = get_features(student_id)
    scores   = {}
    for subject, bench in JEE_MAIN_BENCHMARKS.items():
        student_pct  = features[f"{subject}_percentile_board"]
        target_pct   = bench["general_cutoff_percentile"]
        scores[subject] = min(100, (student_pct / target_pct) * 100)

    overall = mean(scores.values())
    return {
        "readiness_score":    overall,
        "subject_breakdown":  scores,
        "days_to_target":     estimate_days_to_80pct_readiness(student_id, overall),
        "est_air":            estimate_air(features),  # All India Rank estimate
    }
```

---

## 17. DPDPA & Ethics Compliance

| Obligation | Implementation |
|------------|---------------|
| **Profiling children** | Students < 18: predictions not shared externally without parental consent (Module 09 parental access gate). |
| **No discriminatory features** | Caste, religion, gender excluded from all feature groups. Monthly bias audit with fairness metrics (equalized odds, demographic parity). |
| **Right to explanation** | Every prediction has SHAP + NL explanation accessible via `GET /me/analytics/readiness/`. Response within 30 days of request. |
| **Right to opt-out** | `analytics_opt_out` table. On opt-out: predictions hidden on all dashboards; opt-out event written to Module 42 audit. |
| **Accuracy disclosure** | Model RMSE, MAE, R² published on EduForge platform status page annually. |
| **Data minimisation** | Only academic activity features. No social graph, family income, or demographic data as direct features. |
| **Retention** | Predictions: 1 year. Raw features: 2 years. Training datasets anonymised after 3 years (replace student_id with hash). |
| **Audit log** | Every prediction access, dashboard view, parent alert, opt-out logged to Module 42 `audit.events` with `resource_type='analytics'`. |
| **VAM sensitivity** | Teacher VAM stored in row-security-protected table. Admin access only. Not used in HR decisions without explicit admin override. |

---

## 18. Operational Excellence

### Model Accuracy SLA

| Model | Target RMSE | Target AUC | Alert If |
|-------|------------|-----------|---------|
| `score_predictor` | ≤ 9 marks | — | RMSE > 12 |
| `at_risk_classifier` | — | ≥ 0.82 | AUC < 0.75 |
| `dropout_predictor` | — | ≥ 0.80 | AUC < 0.72 |

### Cost Summary

| Component | Frequency | Est. Monthly Cost |
|-----------|----------|-----------------|
| SageMaker Batch Transform (ml.m5.large spot) | Daily | Rs. 3,000 |
| SageMaker Serverless Inference (real-time) | On demand | Rs. 1,500 |
| SageMaker Training Jobs (weekly) | Weekly | Rs. 5,000 |
| S3 Feature Lake (100 GB at 50M students) | Storage | Rs. 200 |
| Athena queries (admin dashboards) | 50 queries/day | Rs. 500 |
| Glue crawlers + jobs | Nightly | Rs. 800 |
| **Total** | | **~Rs. 11,000/month** |

At 50M students — Rs. 11,000/month for the entire ML analytics stack is possible due to serverless/spot pricing and the CDN-first architecture reducing API load.
