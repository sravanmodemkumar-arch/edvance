# A-29 — Compliance Dashboard

> **URL:** `/school/admin/compliance/`
> **File:** `a-29-compliance-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · Promoter (S7) — view · VP Admin (S5) — admin compliance items · VP Academic (S5) — academic compliance items

---

## 1. Purpose

Single-page view of all compliance obligations the school must meet — regulatory, statutory, safety, and academic. In Indian schools, there are compliance requirements from CBSE/board, Central government (RTE, POCSO, DPDPA), state government (labour laws, municipal, fire dept), and various statutory bodies (EPFO, ESIC, GST if applicable). Missing a deadline can mean inspection failure, penalty, or (in extreme cases) de-recognition.

---

## 2. Page Layout

### 2.1 Header
```
Compliance Dashboard — 2025–26              [Full Checklist] [Generate Compliance Report]
Overall Score: 91.4%    Critical: 0 · High: 2 · Medium: 4 · Low: 1
```

---

## 3. Compliance Categories

### 3.1 Regulatory / Affiliation

| Item | Authority | Frequency | Last Done | Next Due | Status | Action |
|---|---|---|---|---|---|---|
| CBSE Affiliation Renewal | CBSE | 1–5 years | 1 Apr 2022 | 31 Mar 2027 | ✅ 366 days left | — |
| CBSE Half-Yearly Report | CBSE | 2× per year | 30 Sep 2025 | 31 Mar 2026 | 🟡 Due in 5 days | [Submit] |
| UDISE+ Annual Data Entry | MHRD | Annual | 31 Dec 2025 | 31 Dec 2026 | ✅ Done | — |
| State Board Annual Return | State Board | Annual | 28 Feb 2026 | 28 Feb 2027 | ✅ Done | — |

### 3.2 Safety & Infrastructure

| Item | Authority | Last Done | Next Due | Status |
|---|---|---|---|---|
| Fire NOC | Municipal Corp | 15 Jan 2025 | 14 Jan 2026 | 🔴 OVERDUE (renewal needed) |
| Fire Drill | Internal | 15 Sep 2025 | 15 Mar 2026 | 🟠 Due in 11 days |
| CCTV System Check | Internal | 1 Mar 2026 | 1 Jun 2026 | ✅ |
| Drinking Water Quality Test | Municipal/State | 1 Jan 2026 | 1 Jul 2026 | ✅ |
| Electrical Safety Certificate | State Elect. Dept | 1 Aug 2024 | 1 Aug 2025 | 🔴 EXPIRED |
| Pest Control | Internal | 15 Feb 2026 | 15 May 2026 | ✅ |

### 3.3 Statutory / HR

| Item | Authority | Frequency | Last Filed | Next Due | Status |
|---|---|---|---|---|---|
| EPFO Monthly ECR | EPFO | Monthly | 15 Mar 2026 | 15 Apr 2026 | ✅ Up to date |
| ESIC Monthly Return | ESIC | Monthly | 15 Mar 2026 | 15 Apr 2026 | ✅ Up to date |
| Professional Tax (State) | State | Monthly | 10 Mar 2026 | 10 Apr 2026 | ✅ Up to date |
| TDS Return (Salary) | Income Tax Dept | Quarterly | 31 Jan 2026 | 31 Jul 2026 | ✅ |
| Staff BGV Compliance | Internal / CBSE | Ongoing | 26 Mar 2026 | Ongoing | 🟡 6 staff BGV pending |

### 3.4 Child Safety & POCSO

| Item | Requirement | Status |
|---|---|---|
| POCSO ICC Formation | Mandatory under POCSO Act 2012 | ✅ ICC formed (3 members + external) |
| POCSO Staff Training | Annual | ⚠️ 9 staff overdue (target: 100%) |
| Student Awareness Programme | Annual | ✅ Conducted 15 Jan 2026 |
| ICC Charter Published | Mandatory | ✅ v1.3 (2024) |
| Visitor Register Maintained | Daily | ✅ |
| Open Cases | — | 0 |

### 3.5 Data Protection (DPDPA 2023)

| Item | Status |
|---|---|
| Data Register Maintained | ✅ |
| Student Data Consent (parents) | ✅ Collected for all students |
| Staff Data Consent | ✅ 107/110 (3 pending) |
| Data Breach Response Protocol | ✅ Documented |
| Right to Erasure Requests | 0 open |

---

## 4. Overdue / Critical Items (highlighted section)

Red box at top:
```
🔴 CRITICAL — 2 items require immediate action:
  • Fire NOC expired (Municipal Corp) — arrange renewal inspection
  • Electrical Safety Certificate expired — contact state electricity board
```

---

## 5. Compliance Score Computation

Each item assigned a weight (critical/high/medium/low). Score = weighted sum of compliant items / total.
- 100% = full compliance
- < 90% = amber on all dashboards
- Any CRITICAL expired = red on all dashboards

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/compliance/summary/` | Dashboard summary + score |
| 2 | `GET` | `/api/v1/school/{id}/compliance/items/` | All compliance items |
| 3 | `PATCH` | `/api/v1/school/{id}/compliance/items/{id}/` | Update item (upload evidence, mark done) |
| 4 | `GET` | `/api/v1/school/{id}/compliance/overdue/` | Overdue items list |
| 5 | `GET` | `/api/v1/school/{id}/compliance/report/pdf/` | Compliance report PDF |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
