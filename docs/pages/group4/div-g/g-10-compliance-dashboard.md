# G-10 — Compliance Dashboard & Alerts

> **URL:** `/college/compliance/dashboard/`
> **File:** `g-10-compliance-dashboard.md`
> **Priority:** P1
> **Roles:** Compliance Officer (S4) · IQAC Coordinator (S4) · Principal/Director (S6) · Trust/Management (S7)

---

## 1. Compliance Dashboard

```
COMPLIANCE DASHBOARD — GCEH
Principal / Compliance Officer View
As of 27 March 2027

OVERALL COMPLIANCE HEALTH: 86 / 100
  ████████████████████████████████░░░░  86%

DOMAIN SCORES:
  ┌────────────────────────────────────────────────────────────────────────────┐
  │ AICTE/UGC   │ 19/20 ████████████████████  ✅ Minor: Mandatory disclosure  │
  │ NAAC/NBA    │ 17/20 █████████████████░░░   ⚠️ SSR 6% pending             │
  │ Labour Law  │ 20/20 ████████████████████  ✅ All EPF/ESI/PT filed         │
  │ POSH        │ 18/20 ██████████████████░░   ⚠️ 1 case under inquiry       │
  │ Anti-Ragging│ 19/20 ████████████████████  ✅ 1 complaint under inquiry    │
  │ Fire/Build  │ 18/20 ██████████████████░░   ⚠️ Fire NOC renewal in process │
  │ DPDPA/IT    │ 16/20 ████████████████░░░░   ⚠️ DPDPA annual review pending │
  └────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Active Alerts

```
ACTIVE COMPLIANCE ALERTS — 27 March 2027

CRITICAL (P0 — Must resolve immediately):
  None ✅

HIGH (P1 — Resolve within 7 days):
  🔴 P1: SERB grant PRJ-001 annual report due 31 March 2027 (4 days)
          Owner: Dr. Suresh K. (PI) | Action: Report in preparation
  🔴 P1: Patent PAT-007 complete specification overdue (due 20 Feb 2027 — 35 days late)
          Owner: Dean Research | Action: Patent agent notified; expect filing in 7 days
          RISK: If not filed before 20 Feb 2027 + 30-day late grace = 22 March 2027
          STATUS: Patent Office allows late filing with surcharge (₹4,000/month)
                  Current surcharge liability: ₹4,000 × 1.5 months ≈ ₹6,000

MEDIUM (P2 — Resolve within 30 days):
  🟡 P2: Fire NOC renewal due 14 March 2027 — application submitted but NOC pending
          Owner: Estate Manager | Action: Follow up with Fire Department (3rd week)
  🟡 P2: NAAC SSR 2027 — 2 sections incomplete (Criterion 2.7, 5.3, 7.3)
          Owner: NAAC Coordinator | Target: 100% by 1 April 2027
  🟡 P2: Mandatory disclosure: Faculty PhD count mismatch (1 faculty — pending sync)
          Owner: Compliance Officer | Action: Update disclosure after HR sync

LOW (P3 — Monitor):
  🟢 P3: DPDPA annual data audit: Self-assessment review due (no hard deadline)
          Suggested: April 2027 (pre-NAAC visit best practice)
  🟢 P3: 3 PhD scholars with 0 publications (Year 2+)
          Owner: Dean Research | Action: Mentor meeting scheduled
  🟢 P3: MCA batch below 66% — intake reduction application filed; awaiting AICTE
```

---

## 3. Compliance Calendar

```
COMPLIANCE CALENDAR — 2026–27

COMPLETED:
  ✅ Oct 2025: AICTE EoA application filed
  ✅ Nov 2025: NBA SAR (B.Tech CSE, ECE) submitted
  ✅ Jan 2027: NIRF 2027 submission complete
  ✅ Jan 2027: POSH Annual Report filed to District Officer
  ✅ Feb 2027: Fire NOC renewal application submitted
  ✅ Feb 2027: EPF/ESI returns filed (April–January months)
  ✅ Feb 2027: EoA received for 2026–27

UPCOMING:
  31 Mar 2027: SERB PRJ-001 annual report (Dr. Suresh K.) — P1
  1 Apr 2027:  NAAC SSR completion target (internal)
  10 Apr 2027: PT monthly remittance (March 2027 collection)
  15 Apr 2027: EPF ECR (March 2027 payroll)
  May 2027:    AQAR 2025–26 submission to NAAC
  Jun 2027:    Form 16 issuance (employees — TDS 2026–27)
  Sep 2027:    Evacuation drill (start of next academic year)
  Oct 2027:    NAAC Cycle 3 peer team visit (expected)
  Oct 2027:    AICTE EoA application for 2027–28
  Nov 2027:    NBA renewal visit (B.Tech CSE, ECE)

ANNUAL RECURRING:
  Monthly: EPF ECR (15th), PT (10th), GSTR-1 + 3B (11th/20th)
  Quarterly: ESI return, Advance tax (IT)
  Annually: EPF annual returns (April), Form 16 (June), POSH report (January)
```

---

## 4. Compliance Score Trend

```
COMPLIANCE SCORE TREND — Annual

Year     | Score  | Grade  | Key improvement / issue
──────────────────────────────────────────────────────────────────────────────
2022–23  | 78/100 | B      | EPF delay (1 month) penalised
2023–24  | 81/100 | B+     | POSH ICC reconstituted properly
2024–25  | 84/100 | B+     | Fire NOC 2-month gap (renovation delay)
2025–26  | 86/100 | A-     | All regularised; minor pending items only
2026–27  | 86/100 | A-     | Patent overdue; Fire NOC pending renewal (minor)
Target   | 90/100 | A      | NAAC Grade A + DPDPA full compliance

SCORING METHODOLOGY:
  Each domain: 20 points
  Deductions: P0 issue = -5; P1 = -3; P2 = -1; P3 = -0.5
  Audit findings: External auditor (NAAC/AICTE inspection findings deduct per severity)

COMPLIANCE INVESTMENT VALUE:
  Cost of non-compliance (if EPF delayed 1 month): ₹10L × 12%/yr × 1/12 = ₹10,000 penalty
  Cost of non-compliance (POSH violation, Section 26): ₹50,000 per offence
  Cost of non-compliance (expired Fire NOC + incident): Criminal liability + civil suit
  EduForge compliance monitoring cost: Included in platform fee
  → Cost avoidance is the primary ROI of proactive compliance management
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/compliance/dashboard/` | Real-time compliance dashboard |
| 2 | `GET` | `/api/v1/college/{id}/compliance/alerts/` | Active alerts by priority |
| 3 | `GET` | `/api/v1/college/{id}/compliance/calendar/` | Upcoming compliance deadlines |
| 4 | `GET` | `/api/v1/college/{id}/compliance/score/trend/` | Annual compliance score trend |
| 5 | `POST` | `/api/v1/college/{id}/compliance/alerts/{id}/resolve/` | Mark alert resolved |

---

## 6. Business Rules

- Compliance is not a binary state (compliant / non-compliant); it is a continuous spectrum; the compliance score model helps the Principal and Trust understand not just whether the college is compliant today, but how far it is from a serious problem — a score of 86/100 with only P2 and P3 issues is fundamentally different from a score of 72/100 with a P0 (critical) issue even if both are "passing"
- Proactive compliance (addressing issues before deadlines) costs far less than reactive compliance (addressing after penalties); the patent overdue penalty (₹6,000 surcharge) is minor; a lapsed Fire NOC followed by an incident is existential; the compliance dashboard converts all compliance activities into a unified risk view that allows rational prioritisation
- The compliance calendar must be maintained and monitored weekly; a compliance function that only reacts to reminders on the day of deadline is chronically underprepared; the Principal and Compliance Officer should review the 30-day and 90-day compliance calendar weekly; EduForge's calendar sends SMS and app notifications to the responsible owner 30, 14, 7, and 1 day before each deadline
- Audit findings from external bodies (AICTE inspection, NAAC peer team, EPF/ESI audit) must be logged and tracked to closure; an audit finding that is not addressed in the stipulated time compounds into a bigger violation in the next audit cycle; EduForge's audit finding tracker maintains open, in-progress, and closed status with owner assignment and deadline
- The Trust (Governing Body) must receive a quarterly compliance report; compliance failures at institutional level are ultimately the Governing Body's responsibility under the Companies Act (for trust companies) and the UGC/AICTE terms of approval; a Governing Body that cannot demonstrate it was monitoring compliance cannot claim it was unaware of violations — ignorance is not a defence in regulatory proceedings

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division G*
