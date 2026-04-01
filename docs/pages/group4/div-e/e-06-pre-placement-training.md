# E-06 — Pre-Placement Training & Aptitude

> **URL:** `/college/placement/training/`
> **File:** `e-06-pre-placement-training.md`
> **Priority:** P2
> **Roles:** Training & Placement Coordinator (S4) · Faculty Advisor — Placement (S3) · Placement Officer (S3)

---

## 1. Training Programme Structure

```
PRE-PLACEMENT TRAINING PROGRAMME — GCEH 2026–27
(For Final Year students — Batch 2022–26)

PROGRAMME OVERVIEW:
  Duration: June 2026 – October 2026 (pre-season; 4 months)
  Target: All final year students (332)
  Objective: Improve placement readiness, raise average CTC, increase placement %

MODULES:
  Module 1: Aptitude & Logical Reasoning (40 hours)
    Topics: Quantitative (number theory, time-speed-distance, probability),
            Verbal (RC, grammar, vocabulary, TOEFL-style),
            Logical (blood relations, data interpretation, syllogisms)
    Trainer: Internal faculty (Maths + English departments)
    Tests: Weekly mock tests (100Q, 60 min — TCS/Infosys pattern)

  Module 2: Technical Preparation (60 hours)
    Topics: Data Structures & Algorithms (arrays, trees, graphs, DP),
            C/C++/Java/Python (one language — student choice),
            DBMS (SQL queries — common drive test component),
            OS basics, Computer Networks fundamentals
    Trainer: CSE/IT faculty + external trainer (Hyderabad-based)
    Platform: LeetCode/HackerRank (EduForge tracks submission history)

  Module 3: Communication & Soft Skills (20 hours)
    Topics: Group discussion (GD) practice, Presentation, Email writing,
            Spoken English (accent, clarity), Body language for interviews
    Trainer: English department faculty + external communication coach

  Module 4: HR Interview Preparation (10 hours)
    Topics: Self-introduction, common HR questions (strength/weakness, STAR method),
            Salary negotiation basics, Offer evaluation (how to read CTC breakup)
    Trainer: Placement Officer + alumni volunteers

  Module 5: Domain-Specific Prep (20 hours)
    IT Track: System design basics, Cloud fundamentals (AWS/Azure entry level)
    Core Track: GATE-level domain refresh (useful for PSU + higher studies)
    Analytics Track: Excel advanced + SQL + basic Python data analysis
    Trainer: Senior faculty + industry guest (per track)

TOTAL TRAINING HOURS: 150 hours (over 4 months)
ATTENDANCE: ≥75% per module mandatory (else not permitted on eligible drive list — soft rule)
```

---

## 2. Training Progress Dashboard

```
TRAINING PROGRESS — 27 March 2027

OVERALL COMPLETION (all 332 students):
  Module 1 (Aptitude): 100% completed (June–July 2026) ✅
  Module 2 (Technical): 100% completed (July–September 2026) ✅
  Module 3 (Soft Skills): 100% completed (August 2026) ✅
  Module 4 (HR Prep): 100% completed (September 2026) ✅
  Module 5 (Domain): 95% (domain-specific; 17 students still completing Core Track) ⬜

APTITUDE TEST SCORES — Module 1 (Benchmark):
  Pre-training (June 2026 baseline):
    Mean score: 52.4 / 100  (TCS pattern mock test)
    Pass (≥60%): 148 / 332 = 44.6%

  Post-training (October 2026):
    Mean score: 69.8 / 100  (same pattern)
    Pass (≥60%): 274 / 332 = 82.5%
    Improvement: +17.4 points mean; +37.9% pass rate ✅

TECHNICAL ASSESSMENT — LeetCode Stats:
  Problems solved (median per student): 48 problems
  Students with >100 problems: 42 (12.7%)
  Students with 0 problems: 8 (non-compliant — flagged for counselling)
  Language distribution: Java 38%, Python 36%, C++ 18%, Others 8%

PLACEMENT CORRELATION:
  Students with aptitude ≥70%: Placed 88.4%
  Students with aptitude 50–70%: Placed 67.2%
  Students with aptitude <50%: Placed 41.8%
  → Strong correlation confirms training investment value
```

---

## 3. External Trainer & Platform Partnerships

```
EXTERNAL TRAINING PARTNERSHIPS

TRAINING VENDORS (contracted 2026–27):
  Vendor 1: FACE Academy (Aptitude specialists)
    Contract: ₹3.2L (for 150 hours of aptitude training)
    Track record: GCEH using since 2022 — placement improvement documented
    Rating: 4.1/5 (student feedback)

  Vendor 2: CodeTantra (Technical — DSA/Programming)
    Contract: ₹4.8L (platform license for 332 students + 60 hrs instruction)
    LMS integration: EduForge → CodeTantra API (progress sync)
    Rating: 3.9/5

  Vendor 3: British Council Spoken English Module
    Contract: ₹1.6L (online course access for all students)
    Outcome: 22% improvement in spoken English assessment score
    Rating: 4.3/5

TOTAL EXTERNAL TRAINING SPEND: ₹9.6L (2026–27)
Cost per placed student: ₹9.6L / 224 = ₹4,286/placed student
ROI: Median CTC ₹4.5L → ₹4,286 training cost = ~1.05% of Year 1 salary ← very high ROI

ONLINE PLATFORMS (student access — college-provisioned):
  LeetCode Premium: 332 licenses (₹1.8L)
  InfyTQ certification: Free (Infosys-provided) → 180 students certified
  TCS iON Ready: Free (TCS-provided) → 220 students attempted
  AMCAT subscription: ₹1.1L (helps in Tier 2 company tests)
```

---

## 4. Company-Specific Mock Tests

```
COMPANY-SPECIFIC MOCK DRIVES (Internal)

PRE-DRIVE MOCK: Held before each major company visit
  TCS Mock Drive (5 days before actual TCS visit):
    Students: All eligible 224 (TCS CGPA requirement: 60%)
    Format: TCS NQT pattern (3 sections + coding)
    Duration: 120 minutes
    Result: 182/224 (81.3%) cleared mock →
            Actual TCS drive: 148/189 (78.3%) cleared → shows mock is calibrated

MOCK GD + INTERVIEW:
  Groups of 8 students + faculty panel
  Topics: Current affairs, tech topics ("Is AI a threat to jobs?"), abstract ("Blue")
  Evaluation: Faculty rates participation, logic, communication
  Feedback: Individual written feedback given to each student

RESUME REVIEW (Placement Officer + Senior Faculty):
  All 332 resumes reviewed before season start
  Common issues found: Objective statement too generic, projects poorly described,
                       CGPA displayed inconsistently, contact info wrong
  Mass feedback session + individual corrections
  Resume v2 uploaded: All 332 students ✅ (by 15 September 2026)
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/placement/training/modules/` | Training modules and schedule |
| 2 | `GET` | `/api/v1/college/{id}/placement/training/progress/` | Student-wise progress |
| 3 | `POST` | `/api/v1/college/{id}/placement/training/test/` | Record mock test result |
| 4 | `GET` | `/api/v1/college/{id}/placement/training/analytics/` | Training effectiveness analytics |
| 5 | `GET` | `/api/v1/college/{id}/placement/training/correlations/` | Training score vs placement correlation |

---

## 6. Business Rules

- Pre-placement training expenditure is a legitimate college expense under "student development / placement support"; it is not a capital expense but an operational one; NAAC expects to see evidence of systematic training (Criterion 5.1 — Student Support); training programme documentation (modules, attendance, pre/post assessments) is key NAAC evidence
- Training attendance below 75% should have consequences for drive eligibility; however, these consequences must be clearly communicated in advance and not applied retroactively; students who missed training due to medical reasons or family emergency must be given a grace path; blanket exclusion without process violates natural justice
- Company-specific mock tests use publicly available information about test patterns (TCS NQT pattern, Infosys InfyTQ, etc.) — this is not confidential and is widely used in coaching; the college is not violating any agreement by preparing students for these tests
- The placement-training correlation data (students who trained more got placed at higher rates) is powerful evidence for continued investment; sharing this data with the Governing Body during budget discussions helps justify training expenditure; EduForge generates this correlation analysis automatically
- Training vendor contracts must include a performance clause — if training outcomes (post-test scores, placement rates) do not improve by a minimum benchmark, the vendor fee is partially withheld; this incentivises quality delivery and protects the college from paying for ineffective training

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division E*
