# Division P — Audit & Quality (Institution Group Level)
## Page Index

> **Division:** P — Audit & Quality
> **Group:** Group 2 — Institution Groups (chains/trusts/societies owning 5–50 schools/colleges)
> **Scale:** 150 groups · 5–50 branches per group · ~1,900 total institutions
> **Base URL:** `/group/audit/`
> **Status:** ✅ All 26 page specs complete (P-01 through P-26)
> **Last updated:** 2026-03-26

---

## Overview

Division P covers the complete audit, quality assurance, compliance, and accreditation function for an Institution Group. It encompasses internal financial audits, academic quality inspections, branch-level operational audits, corrective action tracking, board affiliation compliance (CBSE/ICSE/State Board), quality certification management (ISO 9001/NAAC/QCI), regulatory filing schedules, grievance audit analysis, and compliance trend analytics.

In Indian education — particularly for multi-branch groups — audit and quality is not a luxury function; it's a survival function. A CBSE affiliation that lapses because one branch didn't renew its fire safety NOC means 2,000 students cannot appear for board exams. A RTE non-compliance penalty runs ₹1 lakh per day. A POCSO safety audit failure makes the Chairman criminally liable. A NAAC grade drop from 'A' to 'B+' costs a college ₹50L+ in lost government grants and forces fee reductions.

The problems Division P solves:

1. **Audit fragmentation:** Without a central system, audits happen in Excel sheets, WhatsApp messages, and physical registers. The Audit Head in a 30-branch group cannot track which branches were audited, what was found, and whether corrections were implemented. The platform centralises all audits — financial, academic, operational — with finding tracking and CAPA (Corrective Action / Preventive Action) workflows.

2. **Affiliation risk:** CBSE affiliation renewal happens every 5 years. The checklist has 40+ requirements: teacher-student ratio ≤ 1:30, playground ≥ 2000 sq.ft, fire safety NOC, building stability certificate, CCTV in corridors, functional science lab, library with ≥ 1500 books. Missing even one requirement risks affiliation denial. The platform tracks every requirement per branch with document uploads, expiry alerts, and gap analysis.

3. **Corrective action closure gap:** Indian education's biggest quality problem is the gap between "audit found it" and "branch fixed it." Findings pile up in reports no one reads. The CAPA module enforces: every finding → root cause → corrective action → deadline → verification → closure. Auto-escalation ensures non-closure reaches the CEO.

4. **Compliance score visibility:** CEOs need a single number per branch: "How compliant is this branch?" The Branch Compliance Scorecard computes a weighted score across financial, academic, safety, infrastructure, and regulatory dimensions — making it immediately clear which branches need attention.

5. **Regulatory filing deadlines:** Indian educational institutions must file UDISE+ (Oct), AISHE (Feb), RTE returns (quarterly), state education department reports (annual), fire safety renewal (annual), building safety certificate (5-year). Miss a deadline and the consequences range from fines to affiliation loss. The Regulatory Filing Calendar tracks every deadline per branch with advance alerts.

### Critical Context: Audit Independence

Audit roles are deliberately G1 (Read-Only) or G3 (Operations for field work only). Auditors must NOT have edit access to the data they audit — this preserves audit independence. The Internal Audit Head (121) can view all financial data across Division D but cannot modify it. The Academic Quality Officer (122) can view teaching records across Division B but cannot change them. Only the Inspection Officer (123) and Process Improvement Coordinator (128) have G3 access for creating audit records and CAPA items — they never edit the source data being audited.

### Two Deployment Profiles

| Profile | Branches | Students | Staffing Model |
|---|---|---|---|
| Large Group (Enterprise) | 20–50 | 20,000–1,00,000 | All 8 roles staffed; dedicated audit team of 6–10 people; 3–5 field inspectors; quarterly branch audits; annual affiliation tracking per branch; ISO/NAAC coordinator for colleges |
| Small Group (SME Trust) | 5–10 | 2,000–8,000 | 2–3 people covering audit + compliance; owner handles affiliation; annual audit by external CA; no dedicated quality or inspection roles |

### Scale Numbers

| Metric | Large Group | Small Group |
|---|---|---|
| Branches to audit | 20–50 | 5–10 |
| Audits per year (all types) | 150–400 | 15–40 |
| Audit findings per year | 500–2,000 | 50–200 |
| Open CAPA items at any time | 50–200 | 10–30 |
| Affiliation renewals tracked | 20–50 (rolling) | 5–10 |
| Regulatory filings per year | 100–300 | 20–50 |
| Inspection visits per year | 60–200 | 10–30 |
| Quality certifications tracked | 5–20 | 1–3 |
| Grievance patterns analysed | 200–1,000 complaints/year | 30–100 |

---

## Roles in Division P

### Original Roles (from Group 2 Role Sheet)

| Role ID | Role Name | Level | Large Group | Small Group | Platform Function |
|---|---|---|---|---|---|
| 121 | Group Internal Audit Head | G1 | ✅ Dedicated | ✅ 1 person | Plan audits, review findings, generate audit MIS — read access across all divisions |
| 122 | Group Academic Quality Officer | G1 | ✅ Dedicated | ✅ Shared | Academic audit: lesson plan compliance, exam quality, syllabus coverage |
| 123 | Group Inspection Officer | G3 | ✅ Multiple (3–5) | ✅ Shared | Physical branch visits, checklist-based inspections, photo evidence, data verification |
| 124 | Group ISO / NAAC Coordinator | G1 | ✅ Dedicated | ❌ | Quality certification lifecycle: self-assessment, external audit prep, renewal |
| 125 | Group Affiliation Compliance Officer | G1 | ✅ Dedicated | ✅ Shared | CBSE/ICSE/State Board affiliation tracking, document readiness, renewal alerts |
| 126 | Group Grievance Audit Officer | G1 | ✅ Dedicated | ❌ | Complaint pattern analysis, resolution time audit, repeat offender detection |

### Additional Platform Roles (Division P Specific)

| Role ID | Role Name | Level | Large Group | Small Group | Platform Function |
|---|---|---|---|---|---|
| 127 | Group Compliance Data Analyst | G1 | ✅ Dedicated | ❌ (Audit Head covers) | Compliance scorecards, trend analytics, MIS reports, branch ranking calculations |
| 128 | Group Process Improvement Coordinator | G3 | ✅ Dedicated | ✅ Shared | Drives CAPA to closure, builds improvement plans, verifies implementation, escalates non-compliance |

**Access Level Summary:**
- G0 = No Platform Access (not applicable in Division P)
- G1 = Read-Only (view audit data, dashboards, reports — cannot edit source data being audited)
- G3 = Operations (create audit records, inspection reports, CAPA items — never edit audited source data)
- G4 = Admin (configure audit policies, scoring methodology, escalation rules)
- G5 = Super Admin (unrestricted — Chairman/Founder)

**Audit Independence Rule:** G1 roles can read data from other divisions (D for finance, B for academic, E for HR) but cannot modify it. This separation is enforced at the API level — Division P endpoints never write to Division B/D/E tables.

---

## Pages in Division P

### Section 1 — Dashboard

| # | File | Page Title | Priority | Primary Role | Key Function |
|---|---|---|---|---|---|
| 01 | `p-01-audit-quality-dashboard.md` | Audit & Quality Dashboard | P0 | Internal Audit Head (121, G1) | Central command — compliance scores, upcoming audits, open findings, branch health |

### Section 2 — Audit Planning & Execution

| # | File | Page Title | Priority | Primary Role | Key Function |
|---|---|---|---|---|---|
| 02 | `p-02-audit-calendar-planner.md` | Audit Calendar & Planner | P0 | Internal Audit Head (121, G1) | Annual audit schedule across all branches — financial, academic, operational |
| 03 | `p-03-financial-audit-manager.md` | Financial Audit Manager | P0 | Internal Audit Head (121, G1) | Branch-wise financial audit — fee reconciliation, vendor payments, petty cash |
| 04 | `p-04-academic-quality-audit.md` | Academic Quality Audit | P0 | Academic Quality Officer (122, G1) | Teaching quality — lesson plans, exam papers, syllabus coverage, result moderation |
| 05 | `p-05-operational-safety-audit.md` | Operational & Safety Audit | P1 | Inspection Officer (123, G3) | Infrastructure, fire safety, CCTV, hygiene, staffing compliance |
| 06 | `p-06-audit-finding-tracker.md` | Audit Finding Tracker | P0 | Internal Audit Head (121, G1) | All findings across all audit types — severity, status, ageing, closure tracking |

### Section 3 — Branch Inspection

| # | File | Page Title | Priority | Primary Role | Key Function |
|---|---|---|---|---|---|
| 07 | `p-07-branch-inspection-scheduler.md` | Branch Inspection Scheduler | P0 | Inspection Officer (123, G3) | Plan surprise + scheduled visits, assign inspectors, track visit completion |
| 08 | `p-08-inspection-checklist-builder.md` | Inspection Checklist Builder | P1 | Inspection Officer (123, G3) | Configurable checklists — CBSE norms, safety, infrastructure, academic, hygiene |
| 09 | `p-09-inspection-report-manager.md` | Inspection Report Manager | P0 | Inspection Officer (123, G3) | Individual visit reports — observations, photos, scores, action items |
| 10 | `p-10-branch-compliance-scorecard.md` | Branch Compliance Scorecard | P0 | Internal Audit Head (121, G1) | Per-branch weighted compliance score across all dimensions |

### Section 4 — Affiliation & Certification

| # | File | Page Title | Priority | Primary Role | Key Function |
|---|---|---|---|---|---|
| 11 | `p-11-board-affiliation-compliance.md` | Board Affiliation Compliance Tracker | P0 | Affiliation Compliance Officer (125, G1) | CBSE/ICSE/State Board requirements per branch — gap analysis, renewal tracking |
| 12 | `p-12-affiliation-document-manager.md` | Affiliation Document Manager | P1 | Affiliation Compliance Officer (125, G1) | Required documents — teacher qualifications, infrastructure proof, safety NOCs |
| 13 | `p-13-quality-certification-tracker.md` | Quality Certification (ISO/NAAC) Tracker | P1 | ISO/NAAC Coordinator (124, G1) | Certification lifecycle — application, self-assessment, external audit, renewal |
| 14 | `p-14-regulatory-filing-calendar.md` | Regulatory Filing Calendar | P1 | Affiliation Compliance Officer (125, G1) | UDISE+, AISHE, RTE returns, state filings — deadline tracking with alerts |

### Section 5 — Corrective Action & Follow-up

| # | File | Page Title | Priority | Primary Role | Key Function |
|---|---|---|---|---|---|
| 15 | `p-15-corrective-action-register.md` | Corrective Action Register (CAPA) | P0 | Process Improvement Coordinator (128, G3) | Finding → root cause → action → deadline → verification → closure |
| 16 | `p-16-non-compliance-escalation.md` | Non-Compliance Escalation Manager | P1 | Process Improvement Coordinator (128, G3) | Auto-escalation: Principal → Zone Director → CEO by severity and age |
| 17 | `p-17-branch-improvement-plan.md` | Branch Improvement Plan Builder | P1 | Process Improvement Coordinator (128, G3) | Per-branch improvement plans with milestones, deadlines, progress tracking |

### Section 6 — Grievance Audit

| # | File | Page Title | Priority | Primary Role | Key Function |
|---|---|---|---|---|---|
| 18 | `p-18-grievance-audit-dashboard.md` | Grievance Audit Dashboard | P1 | Grievance Audit Officer (126, G1) | Cross-branch complaint patterns, resolution time, repeat offender detection |
| 19 | `p-19-complaint-pattern-analyzer.md` | Complaint Pattern Analyzer | P2 | Grievance Audit Officer (126, G1) | Cluster analysis by type, branch, severity, time — systemic issue identification |

### Section 7 — Analytics & Reports

| # | File | Page Title | Priority | Primary Role | Key Function |
|---|---|---|---|---|---|
| 20 | `p-20-compliance-trend-analytics.md` | Compliance Trend Analytics | P1 | Compliance Data Analyst (127, G1) | Branch compliance scores over time, improvement/degradation trends |
| 21 | `p-21-audit-mis-report.md` | Audit MIS Report | P0 | Compliance Data Analyst (127, G1) | Monthly/quarterly report for Board — coverage, findings, closure rate, scores |
| 22 | `p-22-branch-quality-ranking.md` | Branch Quality Ranking | P1 | Compliance Data Analyst (127, G1) | Weighted quality ranking of all branches — overall and dimension-wise |

### Section 8 — Administration

| # | File | Page Title | Priority | Primary Role | Key Function |
|---|---|---|---|---|---|
| 23 | `p-23-audit-template-library.md` | Audit Template & Checklist Library | P1 | Inspection Officer (123, G3) | Master library of audit templates, checklists, scoring rubrics |
| 24 | `p-24-auditor-assignment-manager.md` | Auditor Assignment & Workload Manager | P2 | Internal Audit Head (121, G1) | Auditor workload, assignment tracking, conflict-of-interest rules |
| 25 | `p-25-audit-policy-repository.md` | Audit Policy Repository | P2 | Internal Audit Head (121, G1) | Audit frequency, scoring methodology, escalation rules, CAPA standards |
| 26 | `p-26-audit-activity-log.md` | Audit Activity Log | P2 | G4/G5 | Immutable log of all Division P actions — meta-audit for the auditors |

---

## Audit Cycle — Indian Education Annual Calendar

| Phase | Months | Key Activities | Platform Pages Used |
|---|---|---|---|
| Phase 1 — Pre-Session Readiness Audit | Apr–May | New academic year readiness: infrastructure, staff in place, syllabus mapped, safety compliance, affiliation documents current | P-05, P-07, P-11, P-12 |
| Phase 2 — Q1 Financial Audit | Jul–Aug | First quarter fee collection reconciliation, vendor payments, petty cash verification | P-03, P-06, P-15 |
| Phase 3 — Mid-Year Academic Quality Check | Sep–Oct | Syllabus coverage audit, lesson plan adherence, exam paper quality review, UDISE+ filing verification | P-04, P-14, P-09 |
| Phase 4 — Affiliation Renewal Window | Oct–Dec | CBSE/State Board renewal applications, document submission, gap closure for branches due for renewal | P-11, P-12, P-16 |
| Phase 5 — Q2 Financial + Operational Audit | Nov–Dec | Half-year financial review, operational compliance, safety re-audit | P-03, P-05, P-06 |
| Phase 6 — Board Exam Readiness Audit | Jan–Feb | Exam centre compliance (CBSE/ICSE norms), practical lab readiness, question paper security | P-04, P-07, P-08 |
| Phase 7 — Annual Audit & MIS | Feb–Mar | Comprehensive annual audit across all dimensions, Board presentation, compliance MIS, branch ranking | P-21, P-22, P-10, P-20 |

---

## Compliance Score Model

```
Branch Compliance Score = Weighted average across 6 dimensions:

┌─────────────────────────────┬────────┬────────────────────────────────┐
│ Dimension                   │ Weight │ Source                         │
├─────────────────────────────┼────────┼────────────────────────────────┤
│ Financial Compliance        │ 20%    │ P-03 audit scores              │
│ Academic Quality            │ 25%    │ P-04 audit scores              │
│ Safety & Infrastructure     │ 20%    │ P-05 audit scores              │
│ Affiliation Compliance      │ 15%    │ P-11 requirement fulfilment    │
│ CAPA Closure Rate           │ 10%    │ P-15 closure % within deadline │
│ Grievance Resolution        │ 10%    │ P-18 resolution metrics        │
├─────────────────────────────┼────────┼────────────────────────────────┤
│ Total                       │ 100%   │                                │
└─────────────────────────────┴────────┴────────────────────────────────┘

Score Bands:
  A+ (≥ 95%) — Exemplary
  A  (85–94%) — Compliant
  B  (70–84%) — Needs Improvement
  C  (50–69%) — At Risk
  D  (< 50%)  — Critical — CEO escalation mandatory
```

---

## Cross-Division Data Access

Division P reads data from other divisions but never writes to them:

| Source Division | Data Accessed | Purpose | Access Level |
|---|---|---|---|
| Division B (Academic) | Syllabus coverage, lesson plans, exam papers, results | Academic quality audit | G1 read-only |
| Division C (Admissions) | Admission records, seat allocation | RTE compliance, enrollment audit | G1 read-only |
| Division D (Finance) | Fee collection, vendor payments, budgets, scholarships | Financial audit | G1 read-only |
| Division E (HR) | Staff records, BGV status, qualifications | Teacher qualification audit, POCSO compliance | G1 read-only |
| Division H (Hostel) | Hostel occupancy, welfare events, mess hygiene | Hostel safety audit | G1 read-only |
| Division I (Transport) | Fleet records, GPS data, driver licenses | Transport safety audit | G1 read-only |
| Division K (Welfare) | Child protection records, CCTV coverage, safety incidents | POCSO / safety compliance | G1 read-only |
| Division N (Legal) | Regulatory filings, compliance records | Compliance verification | G1 read-only |

---

*Division index version: 1.0 · Last updated: 2026-03-26*
