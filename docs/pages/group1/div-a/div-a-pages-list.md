# Group 1 — Division A: Executive Dashboard Pages Reference

> **Role access:** CEO · CFO · CTO · COO · Platform Owner
> **Base URL prefix:** `/exec/`
> **Theme:** Dark (`portal_base_dark.html`)
> **Status key:** ✅ Spec done · 🔨 In progress · ⬜ Not started

---

## Scale Context (always keep in mind when designing every page)

| Dimension | Value |
|---|---|
| Schools | 1,000 · 200–5,000 students each · avg 1,000 · total ~10L |
| Colleges (Intermediate) | 800 · 150–2,000 each · avg 500 · total ~4L |
| Institution Groups | 150 · 5–50 child institutions per group |
| Coaching Centres | 100 · 5,000–15,000 members each · avg 10,000 · total ~10L |
| **Total institutions** | **2,050** |
| **Total students** | **2.4M–7.6M** |
| Peak concurrent exam load | **74,000 simultaneous submissions** |
| Platform ARR | Rs.60 Cr+ |
| Mobile app installs | ~3M+ (Flutter — iOS + Android) |
| Questions in bank | 2M+ |
| Active test series | 800+ |
| New institutions/month | 30–50 onboardings |
| Staff needing BGV (POCSO) | ~100,000 across all institutions |

---

## Division A — Role Summary

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 1 | Platform Owner / CEO | 5 | Everything | — |
| 2 | Platform CTO | 5 | Tech architecture, infra, security, deployments | Commercial deals |
| 3 | Platform COO | 3 | Operations, SLAs, team mgmt, support escalations | Infra config, billing |
| 4 | Platform CFO | 1 | Revenue reports, GST, Razorpay settlements | Any data edit |

---

## Dashboard Core

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 01 | Executive Dashboard | `/exec/dashboard/` | `01-executive-dashboard.md` | P0 | ✅ | Main command center — KPI bar, Platform Health, Business Overview, Exam Ops, Revenue, Activity Feed |
| 02 | Platform Health Detail | `/exec/platform-health/` | `02-platform-health.md` | P0 | ⬜ | Full-page uptime/latency/error-rate charts, SLA tracker, incident timeline, service-by-service breakdown |
| 03 | Exam Operations | `/exec/exam-ops/` | `03-exam-operations.md` | P0 | ⬜ | Full exam table with advanced filters, bulk actions, live user heatmap, capacity alerts |

---

## War Room & Real-Time Ops

> Pages in this group are activated during high-load events (74K peak). They are architecturally separate from the standard dashboard — designed for speed, zero-distraction, command-and-control use.

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 32 | Exam Day War Room | `/exec/war-room/` | `32-war-room.md` | **P0** | ✅ | Full-screen command center for 74K peak exams — Lambda concurrency gauge, submission throughput, per-institution live status, one-click escalation, emergency scale controls |

---

## Institution & Growth

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 04 | Institution Growth | `/exec/institution-growth/` | `04-institution-growth.md` | P1 | ⬜ | MoM/YoY institution onboarding trend, geo choropleth map, cohort analysis, churn risk table |
| 05 | Institution Detail | `/exec/institutions/<id>/` | `05-institution-detail.md` | P1 | ⬜ | Single institution drill-down — usage stats, exam history, student count, billing status, health score |
| 06 | Institution List | `/exec/institutions/` | `06-institution-list.md` | P1 | ⬜ | Searchable/filterable institution table — tier, region, status, ARR, last active |
| 07 | Student Analytics | `/exec/student-analytics/` | `07-student-analytics.md` | P2 | ⬜ | Total enrollment trends, subject distribution, pass/fail rates, geographic spread |
| 35 | Customer Health & Churn Map | `/exec/customer-health/` | `35-customer-health.md` | P1 | ✅ | Composite health score per institution, churn probability, decay signals, CSM assignment, at-risk intervention workflow |
| 43 | Onboarding Pipeline Tracker | `/exec/onboarding-pipeline/` | `43-onboarding-pipeline.md` | P2 | ✅ | Kanban/timeline of 30–50 active institution onboardings, step completion, assigned specialist, go-live date, bottleneck analysis |

---

## Financial

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 08 | Financial Overview | `/exec/financial-overview/` | `08-financial-overview.md` | P0 | ⬜ | MTD/YTD revenue, ARR/MRR, subscription mix donut, forecast with confidence band, payment failure alerts |
| 09 | Revenue by Institution | `/exec/revenue/institutions/` | `09-revenue-by-institution.md` | P1 | ⬜ | Per-institution revenue table — plan tier, MRR, invoicing status, renewal date, churn risk |
| 10 | Billing & Invoices | `/exec/billing/` | `10-billing-invoices.md` | P1 | ⬜ | Invoice list with status (paid/overdue/draft), download PDF, resend, filter by period |
| 11 | Subscription Plans | `/exec/subscriptions/` | `11-subscription-plans.md` | P2 | ⬜ | Plan catalog — pricing tiers, feature matrix, upgrade/downgrade actions, active subscriber counts |
| 33 | Razorpay Settlement Tracker | `/exec/settlements/` | `33-razorpay-settlements.md` | P1 | ✅ | Settlement timeline, reconciliation (invoices vs received vs fees), failed payment root cause, refund pipeline, payment method split, gateway fee tracker |
| 34 | GST & Tax Compliance | `/exec/gst-compliance/` | `34-gst-compliance.md` | P1 | ✅ | GSTR-1/3B filing calendar, CGST/SGST/IGST breakdown by state, TDS tracking, SAC 9993 compliance, ITC reconciliation |
| 39 | P&L Overview | `/exec/pnl/` | `39-pnl-overview.md` | P2 | ✅ | Investor-grade P&L — Revenue, COGS, Gross Margin %, OpEx, EBITDA, burn rate, NRR, GRR by quarter; PDF export |
| 50 | Cost Center Breakdown | `/exec/cost-breakdown/` | `50-cost-breakdown.md` | P3 | ✅ | AWS Lambda/RDS/CDN costs, SMS/WhatsApp gateway spend, Razorpay fees, AI API spend — all OpEx line items by month |

---

## Operations

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 12 | Incident Manager | `/exec/incidents/` | `12-incident-manager.md` | P0 | ⬜ | Active + historical incidents, severity classification, MTTR tracker, post-mortem workflow (write-up, root cause, action items, owner, due date) |
| 13 | Incident Detail | `/exec/incidents/<id>/` | `13-incident-detail.md` | P1 | ⬜ | Timeline of events, impacted services, affected institutions, resolution steps, assignee, post-mortem link |
| 14 | Alerting Rules | `/exec/alerts/` | `14-alerting-rules.md` | P2 | ⬜ | View/edit threshold rules — metric, operator, threshold, channel (email/Slack/webhook) |
| 15 | Scheduled Maintenance | `/exec/maintenance/` | `15-scheduled-maintenance.md` | P2 | ⬜ | Upcoming + past maintenance windows, create/edit/cancel windows, notification log |
| 38 | Support Operations | `/exec/support-ops/` | `38-support-ops.md` | P1 | ✅ | L1/L2/L3 ticket volumes, open/resolved/SLA-breached, agent performance, top issue categories, escalation rate, institutions with most open tickets |
| 42 | Notification Operations | `/exec/notification-ops/` | `42-notification-ops.md` | P2 | ✅ | WhatsApp/SMS/Email delivery rates, OTP success rate (1h), queue depth, failed delivery reasons, TRAI DLT compliance, gateway health |

---

## Infrastructure & Engineering (CTO)

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 37 | Infrastructure & Capacity | `/exec/infrastructure/` | `37-infrastructure.md` | P1 | ✅ | Lambda concurrency/cold starts, RDS connection pool/replica lag, Redis memory/eviction/hit-ratio, CDN cache ratio, next 7-day exam load forecast vs headroom |
| 40 | Deployment & Release Tracker | `/exec/deployments/` | `40-deployments.md` | P2 | ✅ | Production version per service, deployment history (author/timestamp/SHA), migration log, CI/CD health, one-click rollback (CTO-gated) |
| 41 | Security Posture | `/exec/security-posture/` | `41-security-posture.md` | P2 | ✅ | SSL cert expiry countdown, KMS key rotation schedule, open CVEs with CVSS scores, last pen test findings, WAF coverage %, DPDP Act compliance checklist |
| 44 | Mobile App Analytics | `/exec/mobile-analytics/` | `44-mobile-analytics.md` | P2 | ✅ | Crash rate by version/platform, DAU/MAU, FCM delivery rate, app store rating (iOS + Android), version adoption curve, force-update compliance % |
| 47 | Capacity Planning & Forecasting | `/exec/capacity-planning/` | `47-capacity-planning.md` | P3 | ✅ | 30-day exam schedule vs predicted peak load vs infra ceiling; Lambda scale-out cost forecast; green/amber/red zone thresholds |
| 48 | AI/ML Operations | `/exec/ai-ops/` | `48-ai-ops.md` | P3 | ✅ | MCQ generation throughput, quality acceptance rate, cost per question, AI API spend, model version in production, pipeline queue depth |

---

## Compliance & Security

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 16 | Compliance Dashboard | `/exec/compliance/` | `16-compliance-dashboard.md` | P1 | ⬜ | SOC2/ISO27001/GDPR/DPDP Act 2023 status widgets, control pass rate, upcoming audit dates, evidence tracker |
| 17 | Audit Log | `/exec/audit-log/` | `17-audit-log.md` | P1 | ⬜ | Full audit trail — actor, action, resource, IP, timestamp; exportable; filterable by category |
| 18 | Security Events | `/exec/security/` | `18-security-events.md` | P2 | ⬜ | Failed logins, suspicious IPs, privilege escalations, anomaly alerts, SIEM-style feed |
| 19 | Data Residency | `/exec/data-residency/` | `19-data-residency.md` | P3 | ⬜ | Region-by-region data storage map, GDPR/DPDP DPA status per institution, retention policy viewer |
| 36 | BGV & POCSO Compliance | `/exec/bgv-compliance/` | `36-bgv-compliance.md` | P1 | ✅ | BGV coverage % per institution, pending/overdue verifications, BGV vendor SLA, POCSO incident log, NCPCR mandatory reporting dashboard |

---

## Content & Exam Management

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 20 | Exam Catalog | `/exec/exam-catalog/` | `20-exam-catalog.md` | P2 | ⬜ | All exam templates — subject, type (MCQ/Descriptive/Mixed), institution, status, usage count |
| 21 | Exam Detail | `/exec/exams/<id>/` | `21-exam-detail.md` | P1 | ⬜ | Exam metadata, live attempt count, student results table, issue log, time-series attempt chart |
| 22 | Question Bank | `/exec/question-bank/` | `22-question-bank.md` | P3 | ⬜ | Question inventory by subject/difficulty, usage frequency, flag/unflag, bulk import/export |
| 23 | Proctoring Overview | `/exec/proctoring/` | `23-proctoring-overview.md` | P2 | ⬜ | AI proctoring stats — flagged sessions, violation categories, escalation queue, false-positive rate |

---

## Reports & Analytics

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 24 | Executive Reports | `/exec/reports/` | `24-executive-reports.md` | P1 | ⬜ | Scheduled + on-demand reports — revenue, usage, compliance; export PDF/CSV/XLSX |
| 25 | Usage Analytics | `/exec/usage/` | `25-usage-analytics.md` | P2 | ⬜ | API call volume, feature adoption heatmap, peak usage times, slowest endpoints |
| 26 | SLA Dashboard | `/exec/sla/` | `26-sla-dashboard.md` | P1 | ⬜ | Per-tier SLA commitments vs actuals — uptime, response time, resolution time; breach history |
| 27 | Cohort Analysis | `/exec/cohorts/` | `27-cohort-analysis.md` | P3 | ⬜ | Institution retention cohorts, student enrollment cohorts, churn waterfall |
| 46 | Domain Performance Overview | `/exec/domain-performance/` | `46-domain-performance.md` | P3 | ✅ | Cross-domain enrollment, revenue per domain (SSC/RRB/NEET/JEE/AP/TS), question bank coverage, top institutions per domain |
| 49 | Student Outcomes Analytics | `/exec/student-outcomes/` | `49-student-outcomes.md` | P3 | ✅ | Pass/fail rates by domain/exam/institution type, rank distributions, result accuracy disputes, YoY improvement |

---

## Strategic & Board (CEO + CFO)

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 45 | Board / Investor Dashboard | `/exec/board-dashboard/` | `45-board-dashboard.md` | P3 | ✅ | Quarterly board KPIs — ARR, ARR YoY%, NRR, GRR, ARPU by segment, LTV, CAC, payback period; PDF/PPTX export for board decks |

---

## Settings & Administration

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 28 | Platform Settings | `/exec/settings/platform/` | `28-platform-settings.md` | P2 | ⬜ | Feature flags, global rate limits, maintenance mode toggle, SMTP config, OAuth providers |
| 29 | User Management | `/exec/settings/users/` | `29-user-management.md` | P1 | ⬜ | Admin + exec user list — roles, last login, 2FA status, suspend/activate, invite |
| 30 | Role & Permissions | `/exec/settings/roles/` | `30-role-permissions.md` | P2 | ⬜ | RBAC role editor — assign permissions per role, view effective permissions per user |
| 31 | API Keys & Webhooks | `/exec/settings/api/` | `31-api-keys-webhooks.md` | P2 | ⬜ | API key management (create/revoke/scope), webhook endpoint config, delivery log |

---

## Drawers & Overlays (used across pages)

| ID | Component | Trigger | Width | Description |
|----|-----------|---------|-------|-------------|
| drawer-A | Preferences | Toolbar avatar → Preferences | 360px | Theme, notification preferences, default date range |
| drawer-B | Service Detail | Platform Health → service row click | 480px | Service health tabs: Overview / Logs / Metrics / Config |
| drawer-C | Exam Detail | Exam Ops → eye icon | 640px | Exam info + Students tab (table + pagination) + Issues tab |
| drawer-D | Institution Detail | Institution rows | 480px | Summary, contact, billing status, quick actions |
| drawer-E | Incident Detail | Incident row | 600px | Timeline, impacted services, resolution steps, assignee |
| drawer-F | War Room Institution | War Room → institution row | 480px | Live exam status, submission %, error log, escalation controls |
| drawer-G | Settlement Detail | Settlement Tracker → row | 560px | Invoice reconciliation, Razorpay payout breakdown, dispute log |
| drawer-H | BGV Institution | BGV table → institution row | 520px | Staff verification list, pending BGVs, POCSO log, vendor contact |
| drawer-I | Health Score Detail | Customer Health → institution | 560px | Score breakdown by dimension, decay signals, CSM notes, intervention history |
| drawer-J | Deployment Detail | Deployments → row click | 600px | Commit log, services changed, migration steps, rollback confirmation |

---

## Known Functional Gaps in Existing Specs (pages 01–31)

> These pages have spec files. The gaps below must be addressed when those specs are deepened — they do not require new pages, just amendments to the existing file. Each gap has a severity rating: Critical = blocks a role from doing their job, High = significant missing value, Medium = noticeable but workaroundable.

| Page | Gap | Severity | Amendment Required |
|---|---|---|---|
| 01 — Executive Dashboard | Missing BGV/POCSO KPI card (6 existing cards, none surface compliance risk) | High | Add card 7: "BGV Coverage" — % institutions at 100% BGV. Red if any institution < 80%. Links to page 36. |
| 01 — Executive Dashboard | No War Room activation trigger during exam peaks | High | When concurrent users > 10,000: replace page header with pulsing red banner "74K PEAK ACTIVE — [Enter War Room]". Button navigates to `/exec/war-room/`. |
| 01 — Executive Dashboard | Missing mobile app health in Platform Health mini section | Medium | Add two service circles: Flutter Crash Rate + FCM Delivery Rate. Same green/amber/red dot logic as existing service circles. |
| 08 — Financial Overview | Describes itself as "CFO's real-time P&L proxy" but has zero COGS, gross margin, or OpEx — it is a revenue dashboard, not a P&L | Critical | Correct spec description. Add header link: "[View Full P&L →]" pointing to page 39. Add a "Settlement Status" row below MRR strip: "Last Razorpay settlement: 14h ago · Rs.4.2L pending → [View Settlements]". |
| 12 — Incident Manager | Post-mortem is a link field only — no in-platform workflow | Critical | Replace link field with structured post-mortem modal: Title, Root Cause (textarea), Contributing Factors (multi-select), Action Items (repeater: task + owner + due date), Status (Draft / In Review / Closed). COO writes, CTO marks Closed. Action items are tracked and show on the incident list row as "3/5 items done". |
| 12 — Incident Manager | No SLA credit calculator | Medium | When incident closes, auto-calculate: downtime duration x credit rate per SLA tier. Show inline: "Enterprise SLA breach: Rs.1.4L credit obligation". CTO acknowledges, triggers credit note via billing API. |
| 16 — Compliance Dashboard | DPDP Act 2023 missing (only SOC2/ISO27001/GDPR listed) | High | Add DPDP Act 2023 as 4th compliance framework widget. Add POCSO Coverage as 5th widget (% institutions with full BGV coverage). Both link to respective detail pages. |
| 26 — SLA Dashboard | Shows breaches but provides no action path for remediation | Medium | Add "Create Credit Note" action on each breach row. Opens a modal: institution pre-filled, amount auto-calculated, CFO approves. Creates record in billing system. |
| 29 — User Management | Shows 2FA status per user but no platform-wide enforcement policy | Medium | Add "Require 2FA for all Exec-level accounts" toggle at top of page (CEO/CTO only). Accounts without 2FA after toggle show warning badge and are locked from sensitive actions after 48h grace. |

---

## Implementation Priority Order

```
P0 — Must have before first exam goes live
  01  Executive Dashboard            SPEC DONE
  02  Platform Health Detail
  03  Exam Operations
  08  Financial Overview
  12  Incident Manager
  26  SLA Dashboard
  32  Exam Day War Room              NEW — most critical safety gap

P1 — Sprint 2
  04  Institution Growth
  05  Institution Detail
  06  Institution List
  09  Revenue by Institution
  10  Billing & Invoices
  13  Incident Detail
  16  Compliance Dashboard
  17  Audit Log
  21  Exam Detail
  24  Executive Reports
  29  User Management
  33  Razorpay Settlement Tracker    NEW — CFO gap
  34  GST & Tax Compliance           NEW — CFO legal risk
  35  Customer Health & Churn Map    NEW — COO/CEO retention
  36  BGV & POCSO Compliance         NEW — COO legal risk
  37  Infrastructure & Capacity      NEW — CTO gap
  38  Support Operations             NEW — COO gap

P2 — Sprint 3
  07, 11, 14, 15, 18, 20, 23, 25, 28, 30, 31
  39  P&L Overview                   NEW
  40  Deployment & Release Tracker   NEW
  41  Security Posture               NEW
  42  Notification Operations        NEW
  43  Onboarding Pipeline Tracker    NEW
  44  Mobile App Analytics           NEW

P3 — Backlog
  19, 22, 27
  45  Board / Investor Dashboard     NEW
  46  Domain Performance Overview    NEW
  47  Capacity Planning & Forecasting NEW
  48  AI/ML Operations               NEW
  49  Student Outcomes Analytics     NEW
  50  Cost Center Breakdown          NEW
```

---

## Page Spec Format (v2 — applies to all new pages 32–50)

Each spec at `docs/pages/group1/div-a/XX-page-name.md` must include all 13 sections:

1. **Page Metadata** — route, view, template, roles, priority, polling rules
2. **Purpose & Business Logic** — why this page exists, what decisions it enables, what role gap it fills
3. **User Roles & Access** — who can see what, who can act, what is hidden per role
4. **Section-wise UI Breakdown** — for EACH section on the page:
   - Section name & purpose
   - User interaction (what the user does here)
   - UI elements (table, chart, gauge, input, etc.)
   - Data flow (API → cache → UI → state)
   - Role-based visibility differences
   - Edge cases (empty, error, loading, permission-denied)
   - Performance considerations
   - Mobile behavior
   - Accessibility notes
5. **Full Page Wireframe** — ASCII art showing complete layout
6. **Component Architecture** — reusable components list + props structure
7. **HTMX Architecture** — partials map, poll intervals, swap targets, poll-pause logic
8. **Backend View & API** — Django view class, endpoint map, request/response shapes
9. **Database & Caching** — queries, Redis keys, TTLs, Celery beat tasks
10. **Validation Rules** — per form field and per action
11. **Security Considerations** — permission checks, 2FA gates, audit log events triggered
12. **Edge Cases (system-level)** — P0 active, network failure, session expiry, mobile breakpoints
13. **Performance & Scaling** — response time targets, cache strategy, query plan notes

---

*Last updated: 2026-03-20*
*Total pages: 50 (31 original + 19 new)*
*Existing spec amendments: 9 functional gaps identified across 6 pages*
