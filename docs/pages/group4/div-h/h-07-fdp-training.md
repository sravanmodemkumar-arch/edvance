# H-07 — FDP & Faculty Development

> **URL:** `/college/hr/fdp/`
> **File:** `h-07-fdp-training.md`
> **Priority:** P2
> **Roles:** FDP Coordinator (S4) · HOD (S4) · Dean Academics (S5) · HR Officer (S3)

---

## 1. FDP Policy & Tracking

```
FACULTY DEVELOPMENT PROGRAMME (FDP) — GCEH

AICTE REQUIREMENT:
  AICTE mandates: Faculty must attend FDPs to remain current
  AICTE ATAL (Advancing Tectonic and Applied Learning): Online + offline FDP platform
  Minimum FDPs: Not a hard number per AICTE, but forms part of NAAC API scoring
  NAAC Criterion 2.4.2: FDP attended (% faculty, days per faculty per year) ← key metric

GCEH FDP POLICY:
  Target: Each faculty attends ≥2 FDPs per year (minimum 5 days total)
  Academic Leave: Granted for FDP attendance (up to 30 days/year)
  Budget: ₹4L/year allocated for FDP (registration fees + travel for outstation FDPs)
  Reimbursement: Outstation FDP (registration ≤₹5,000 + travel/accommodation ≤₹8,000)

FDP TRACKING 2026–27:

Faculty              | FDPs Attended | Days | AICTE ATAL | External  | On Target?
──────────────────────────────────────────────────────────────────────────────────────────
Dr. Suresh K.       | 3             | 12   | 1          | 2 (IEEE)  | ✅ Above target
Dr. Priya M.        | 2             | 8    | 1          | 1 (SERB)  | ✅
Dr. Ramesh D.       | 2             | 6    | 2          | 0         | ✅
Mr. Arun M.         | 1             | 3    | 1          | 0         | ⚠️ Below target
Ms. Deepa R.        | 2             | 7    | 1          | 1         | ✅
Mr. Kiran T.        | 0             | 0    | 0          | 0         | ❌ None attended
...

DEPT AVERAGES:
  CSE: 2.4 FDPs / faculty (avg 8.2 days) — ✅ above target
  ECE: 2.1 FDPs / faculty (avg 6.8 days) — ✅
  EEE: 1.8 FDPs / faculty (avg 5.4 days) — ✅ marginal
  Mech: 1.4 FDPs / faculty (avg 4.1 days) — ⚠️ below target (core engineering challenge)

NAAC DATA (Criterion 2.4.2):
  Faculty who attended FDP ≥1: 56/62 = 90.3% ✅
  Average FDP days per faculty: 7.2 days
  Score (est.): 4/5 (>80% faculty + adequate days)
```

---

## 2. FDP Register

```
FDP REGISTER — 2026–27

FDP ID  | Faculty          | Programme                           | Organiser          | Days | Type    | Cert
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────
FDP-001 | Dr. Suresh K.    | ATAL FDP: Cybersecurity Fundamentals| NITK (AICTE ATAL)  | 5    | Online  | ✅
FDP-002 | Dr. Suresh K.    | IEEE Workshop: Federated ML         | IEEE HYD Section   | 3    | Offline | ✅
FDP-003 | Dr. Priya M.     | ATAL FDP: 5G Networks & Applications| NIT Warangal       | 5    | Hybrid  | ✅
FDP-004 | Dr. Ramesh D.    | DSA and Competitive Programming     | ATAL Online         | 3    | Online  | ✅
FDP-005 | Dr. Priya M.     | SERB School: Signal Processing      | IISER Hyderabad    | 8    | Offline | ✅
FDP-006 | Ms. Deepa R.     | Python for Data Science (NPTEL)     | NPTEL+IIT Madras   | 12 wks| Online | ✅
FDP-007 | Dr. Anand R.     | Power Electronics (ATAL)            | IIT Bombay ATAL    | 5    | Online  | ✅
FDP-008 | Dr. Vikram S.    | Advanced Manufacturing Processes    | NIT Trichy (ATAL)  | 5    | Offline | ✅

INTERNAL FDPs CONDUCTED (GCEH-organized):
  Aug 2026: Research Paper Writing Workshop (2 days — for junior faculty; 28 attended)
  Nov 2026: OBE Implementation Workshop (1 day — all CSE/ECE faculty; NBA prep)
  Feb 2027: DPDPA Awareness Session (1 day — all faculty and admin; compliance)

FDP EVIDENCE (for NAAC):
  ✅ Participation certificates uploaded to EduForge (faculty service book linked)
  ✅ Leave records (academic leave for outstation FDPs)
  ✅ Expenditure reimbursement receipts
  ✅ Internal FDP: Attendance register + programme schedule
```

---

## 3. FDP Budget Tracking

```
FDP BUDGET 2026–27

BUDGET: ₹4,00,000

EXPENDITURE TO DATE (March 2027):
  Registration fees: ₹68,400 (19 paid registrations)
  Travel (outstation): ₹1,24,000 (Dr. Suresh — Singapore; Dr. Vikram — NIT Trichy; others)
  Accommodation: ₹86,000 (outstation stays)
  Internal FDP organization (printing, refreshments, speaker honorarium): ₹42,000
  Total spent: ₹3,20,400

REMAINING: ₹79,600 (for Q4 FDPs — April–June 2027)
  Planned: 2 faculty for annual conference in Chennai (April) — ₹40,000 estimated
  Remaining after planned: ₹39,600 (carry forward to next year not typical)
  Recommendation: Use remaining for internal NAAC preparation workshop (₹25,000)

TDS ON FDP SPEAKER FEES:
  External speaker honorarium: ₹5,000–₹15,000 per session
  TDS: Section 194J (10%) if >₹30,000/year to same person
  March 2027: ₹22,000 total speaker fees — below TDS threshold ← no TDS
  Best practice: Track cumulative payment per speaker across academic year
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/hr/fdp/` | All FDP records |
| 2 | `POST` | `/api/v1/college/{id}/hr/fdp/register/` | Register FDP attendance |
| 3 | `GET` | `/api/v1/college/{id}/hr/fdp/analytics/` | Department-wise FDP analytics |
| 4 | `GET` | `/api/v1/college/{id}/hr/fdp/budget/` | FDP budget utilisation |
| 5 | `GET` | `/api/v1/college/{id}/hr/fdp/naac/` | NAAC Criterion 2.4 data |

---

## 5. Business Rules

- FDP certificates must be uploaded to the system (not just verbally claimed) to count for API scoring and NAAC evidence; a faculty member who attended a conference but has no certificate and no leave record provides no verifiable evidence of the FDP; EduForge's FDP module makes certificate upload mandatory before the FDP is counted in any metric
- Internal FDPs organized by the institution can be counted for faculty (non-organizers) but not for the organizing faculty in the same proportion; a faculty member who organizes an FDP gets credit for organizing (Category III API) but cannot claim the FDP attendance credit simultaneously for the same event
- NPTEL online courses and certifications count as FDP for API scoring purposes only if the faculty completes the proctored exam; completing the course without the proctored exam gives a completion certificate but NAAC and UGC treat it as learning, not FDP; EduForge distinguishes between "NPTEL with proctored exam" and "NPTEL course only" in the FDP register
- FDP budget allocation should be prioritised towards junior faculty and faculty in departments with publication deficiency; senior faculty with strong publication records benefit less marginally from another FDP than junior faculty who have no publications; the Dean Academics should guide the FDP budget allocation strategically, not on first-come-first-served basis
- Organizing FDPs for neighboring colleges adds to NAAC Criterion 3.6 (extension activities) and Criterion 6.3 (professional development support); GCEH organizing research writing workshops and inviting faculty from affiliated colleges is a cost-effective way to improve both NAAC metrics and institutional goodwill in the academic ecosystem

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division H*
