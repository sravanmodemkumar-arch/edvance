# Group 1 — Division B: Product & Design — Pages Reference

> **Division:** B — Product & Design
> **Roles:** Product Manager Platform · Product Manager Exam Domains · Product Manager Institution Portal · UI/UX Designer · QA Engineer
> **Base URL prefix:** `/product/`
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
| Exam domains | 6 (SSC · RRB · NEET · JEE · AP Board · TS Board) + IBPS/SBI/Banking |
| Active feature flags | ~120 flags in production |
| Subscription plan tiers | 4 (Starter · Standard · Professional · Enterprise) |
| New institutions/month | 30–50 onboardings |
| Test series active | ~800+ across all domains |
| Questions in bank | 2M+ |
| Mobile app installs | ~3M+ (Flutter — iOS + Android) |
| Platform ARR | Rs.60 Cr+ |
| GST compliance | CGST/SGST intra-state · IGST inter-state · SAC code 998315 |
| Indian financial year | April 1 – March 31 |

---

## Division B — Role Summary

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 5 | Product Manager — Platform | 3 | Feature flags · plan config · release notes · roadmap · A/B tests · announcements · mobile app config · revenue visibility | Infra config · billing transactions |
| 6 | Product Manager — Exam Domains | 3 | SSC/RRB/Board domain config · exam patterns · syllabus structure · test series · domain analytics · question bank | Content publish (Division D Approver only) |
| 7 | Product Manager — Institution Portal | 3 | School/college/coaching portal features · institution role config · portal templates · onboarding workflows · notification templates | Infra |
| 8 | UI/UX Designer | 1 | Read-only: design review · component audit · design issue logging | ALL writes blocked |
| 9 | QA Engineer | 3 | Test all modules · create test tenants · validate flows · defect tracking · performance testing · automation monitoring · student impersonation on test tenants | Production data edit |

---

## PM Platform — Pages (Role 5) · 11 pages

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 01 | Product Dashboard | `/product/dashboard/` | `01-product-dashboard.md` | P0 | ✅ | Central command — release velocity, flag health, roadmap burndown, QA blockers, feature adoption KPIs, activity feed, war room trigger |
| 02 | Feature Flags | `/product/feature-flags/` | `02-feature-flags.md` | P0 | ✅ | 120+ flag lifecycle: create · rollout % · per-institution overrides · kill switch · dependency graph · audit trail |
| 03 | Release Manager | `/product/releases/` | `03-release-manager.md` | P1 | ✅ | Release pipeline: planning → staging → UAT → pre-production → production · changelog editor · QA sign-off gate · rollback · environment promotion |
| 04 | Plan & Pricing Config | `/product/plan-config/` | `04-plan-config.md` | P1 | ✅ | 4-tier plan catalog · feature entitlement matrix · add-ons · upgrade/downgrade rules · proration preview · API rate limits per tier · 2FA-gated publish |
| 05 | Product Roadmap | `/product/roadmap/` | `05-product-roadmap.md` | P2 | ✅ | Epics · features · milestones · quarter capacity · Kanban board + timeline toggle · priority scoring · stakeholder view |
| 06 | A/B Test Manager | `/product/experiments/` | `06-ab-test-manager.md` | P2 | ✅ | Controlled experiments: variant config · rollout % · institution-type targeting · statistical significance tracker · winner declaration |
| 07 | Announcement Manager | `/product/announcements/` | `07-announcement-manager.md` | P2 | ✅ | Product comms to 2,050 institutions: in-app banners · email digests · targeting by type/plan · schedule · delivery reports |
| 08 | Mobile App Config | `/product/mobile-config/` | `08-mobile-app-config.md` | P2 | ✅ | Flutter app: minimum version enforcement · force update policy · iOS vs Android feature flags · FCM topic config · Hive key rotation schedule |
| 28 | Revenue & Billing Dashboard | `/product/revenue/` | `28-revenue-billing-dashboard.md` | P1 | ✅ | MRR/ARR · churn & expansion · plan distribution · collections · GST compliance · cohort analysis · NRR tracking · revenue forecast (P10/P50/P90) |
| 29 | Promo Code & Discount Manager | `/product/promos/` | `29-promo-code-manager.md` | P2 | ✅ | Promotional codes · partner discounts · seasonal offers · referral programs · per-institution overrides · usage analytics · expiry enforcement |
| 32 | Integration Hub | `/product/integrations/` | `32-integration-hub.md` | P2 | ✅ | Third-party integrations catalog: Google Classroom · Microsoft Teams · Zapier · partner content APIs · per-plan availability · credential management · sync health monitor |

---

## PM Exam Domains — Pages (Role 6) · 9 pages

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 09 | Exam Domain Config | `/product/exam-domains/` | `09-exam-domain-config.md` | P1 | ✅ | SSC/RRB/NEET/JEE/AP Board/TS Board + IBPS/SBI domain cards · metadata · publish/unpublish · domain-level settings · i18n locale config per domain |
| 10 | Syllabus Builder | `/product/syllabus/` | `10-syllabus-builder.md` | P1 | ✅ | Drag-drop hierarchy: Subject → Chapter → Topic · coverage % against 2M+ question bank · per-domain mapping · version history |
| 11 | Test Series Manager | `/product/test-series/` | `11-test-series-manager.md` | P1 | ✅ | Series lifecycle: create · assign exams · schedule · enrollment caps · 100K+ enrollments · progress tracking · series analytics · exam schedule calendar view |
| 12 | Exam Pattern Builder | `/product/exam-patterns/` | `12-exam-pattern-builder.md` | P1 | ✅ | Section config · Q per section · marks/negative marking · time limits · normalization formulas (RRB multi-shift) · exam integrity controls · pattern versioning |
| 13 | Domain Analytics | `/product/domain-analytics/` | `13-domain-analytics.md` | P2 | ✅ | Per-domain: enrollment trends · question coverage · test series usage · institution adoption · dropout points · competitive benchmarks |
| 27 | Question Bank Manager | `/product/question-bank/` | `27-question-bank-manager.md` | P1 | ✅ | 2M+ questions: browse by domain tree · review queue · coverage gaps · duplicate detection · quality analytics · bulk import (CSV/PDF OCR/Partner API) · copyright management |
| 30 | Result Processing & Rank Config | `/product/result-config/` | `30-result-processing-config.md` | P1 | ✅ | RRB multi-shift normalization parameters · JEE/NEET percentile calc formulas · rank band definitions · cutoff config per exam type · result release schedule · tie-breaking rules |
| 34 | Board & Curriculum Manager | `/product/boards/` | `34-board-curriculum-manager.md` | P1 | ⬜ | CBSE · ICSE · 28 State Boards · IB · IGCSE · NIOS · NEET/JEE board config — grade structure · textbook chapter alignment · medium (English/Hindi/Regional) · board exam calendar · curriculum version history · affiliation type mapping |
| 35 | National Exam Catalog Manager | `/product/exam-catalog/` | `35-national-exam-catalog-manager.md` | P1 | ⬜ | 300+ exam catalog CRUD (Module 49 data management) — exam families · stages · eligibility · pattern summary · cutoff history (7 years × category) · salary/pay-level data · preparation roadmap config · application link management · exam date lifecycle · state PSC entries for 30 states |

---

## PM Institution Portal — Pages (Role 7) · 6 pages

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 14 | Portal Feature Config | `/product/portal-features/` | `14-portal-feature-config.md` | P1 | ✅ | 80+ features × 4 institution types × 4 plan tiers entitlement matrix · toggle overrides · dependency warnings · audit log |
| 15 | Institution Role Config | `/product/institution-roles/` | `15-institution-role-config.md` | P2 | ✅ | Institution-side roles (teacher/HOD/admin/principal/parent) · permission sets · role hierarchy · assignment rules per institution type · Redis pub/sub propagation |
| 16 | Portal Templates | `/product/portal-templates/` | `16-portal-templates.md` | P2 | ✅ | Layout templates per institution type · nav order · module visibility · white-label rules · branding config · A/B testing · live preview |
| 17 | Onboarding Workflow | `/product/onboarding/` | `17-onboarding-workflow.md` | P2 | ✅ | Step builder for 30–50 new institutions/month · mandatory vs skippable steps · per-institution-type flows · group onboarding · re-onboarding · completion tracking |
| 18 | Notification Template Manager | `/product/notification-templates/` | `18-notification-template-manager.md` | P2 | ✅ | Email/SMS/WhatsApp templates institutions use for student comms · variable substitution · per-plan availability · preview · A/B variant · DPDPA 2023 compliance |
| 31 | White-Label & Branding Manager | `/product/white-label/` | `31-white-label-branding.md` | P2 | ✅ | Enterprise institution custom subdomains · brand kit (logo/colors/fonts) · white-label rules per plan tier · subdomain provisioning workflow · brand asset CDN management |

---

## UI/UX Designer — Pages (Role 8) · 2 pages

> All pages: Level 1 read-only. Zero write operations permitted for this role.

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 19 | Design System | `/product/design-system/` | `19-design-system.md` | P2 | ✅ | Component library browser · colour tokens · typography scale · spacing system · animation specs · dark/light token audit · Figma links · deprecation policy · accessibility standards |
| 20 | UI Review Board | `/product/ui-review/` | `20-ui-review-board.md` | P3 | ✅ | Production design deviation log · severity triage · assign to dev · resolution tracking · screen comparison · WCAG audit results · annotation pin overlay |

---

## QA Engineer — Pages (Role 9) · 7 pages

| # | Page Name | URL | File | Priority | Status | Description |
|---|---|---|---|---|---|---|
| 21 | QA Dashboard | `/product/qa/` | `21-qa-dashboard.md` | P1 | ✅ | Coverage % · open defects by severity · test run history · module health scores · automation pass rate · release readiness gauge · QA quality score composite metric |
| 22 | Test Tenant Manager | `/product/test-tenants/` | `22-test-tenant-manager.md` | P1 | ✅ | Sandbox tenant CRUD · scenario presets · data reset · config snapshots · institution-type simulations · student impersonation · concurrent user simulation · resource usage monitor |
| 23 | Test Case Repository | `/product/test-cases/` | `23-test-case-repository.md` | P2 | ✅ | Test cases by module/feature/release · test plans · release checklists · execution history · traceability matrix · coverage gaps · test case templates library |
| 24 | Performance Test Dashboard | `/product/performance/` | `24-performance-test-dashboard.md` | P1 | ✅ | 74K concurrent exam load scenarios · latency profiles · throughput charts · Lambda scaling graphs · pre-release pass/fail gate · k6 integration · incident response panel |
| 25 | Defect Tracker | `/product/defects/` | `25-defect-tracker.md` | P1 | ✅ | Full defect lifecycle: Open→In Progress→In Review→Resolved→Closed · aging · severity triage · regression flags · module heatmap · institution-reported defects · SLA breach calculator |
| 26 | Automation Monitor | `/product/automation/` | `26-automation-monitor.md` | P2 | ✅ | CI/CD pipeline status · flaky test & flaky step detection · build time regression tracking · execution time trends · GitHub Actions integration · test suite health by module |
| 33 | API Testing Dashboard | `/product/api-testing/` | `33-api-testing-dashboard.md` | P2 | ✅ | Functional API test suites: endpoint validation · response schema · contract testing · Postman/Newman CI integration · API changelog diff · regression on every deploy |

---

## Cross-Division Shared Drawers (reused across all div-b pages)

| Drawer | Trigger | Width | Tabs | Description |
|---|---|---|---|---|
| flag-detail-drawer | Feature Flags → row click | 560px | Config · Overrides · History · Dependencies | Flag config · rollout slider · per-institution overrides · kill-switch · audit log |
| release-detail-drawer | Release Manager → row click | 640px | Summary · Changelog · Flags · QA Sign-off · Rollback | Full release record · QA checklist · flag inventory · environment promotion |
| plan-edit-drawer | Plan Config → Edit | 640px | Pricing · Features · Limits · Rate Limits · Preview | Editable plan card · API rate limits per tier · 2FA-gated save |
| domain-config-drawer | Exam Domain → card | 720px | Metadata · Patterns · Syllabus · Analytics · i18n | Domain details + pattern editor + locale config |
| test-tenant-drawer | Test Tenants → row | 560px | Config · Scenarios · Reset · Impersonate · Audit | Tenant settings · student impersonation · data reset flow |
| defect-detail-drawer | Defect Tracker → row | 560px | Details · Steps · History · Comments | Reproduce steps · status timeline · SLA breach indicator |
| design-token-drawer | Design System → token | 480px | Values · Usage · Components · Deprecation | Token values · usage locations · migration guide |
| announcement-preview-drawer | Announcement Manager | 600px | In-App · Email · SMS · WhatsApp | Rendered preview per channel + delivery report |
| question-detail-drawer | Question Bank → row | 720px | Content · Quality Signals · Usage Analytics · Versions · Review Activity | Question full view · discrimination index · reviewer ratings |
| revenue-invoice-drawer | Revenue Dashboard → invoice row | 640px | Invoice · Payment History · GST Breakdown · Communication Log | Invoice details · payment status · CGST/SGST/IGST breakdown |
| adoption-feature-drawer | Product Dashboard → Adoption tab row | 480px | By Institution Type · Timeline · Top Adopters · Not Yet Adopted | Feature adoption breakdown + re-engagement actions |

---

## Known Functional Gaps in Existing Specs — Amendment Required

> These are functional areas not adequately covered by any existing page. Each gap has been assigned to an existing page as an amendment — no new pages needed for G1–G5.

| Gap ID | Gap Description | Severity | Assigned Amendment |
|---|---|---|---|
| G1 | **Exam Schedule Calendar** — PM Exam Domains has no calendar view of all scheduled exams across 2,050 institutions for capacity planning | High | Add "Calendar View" toggle to Test Series Manager (page 11) — weekly/monthly calendar showing all scheduled exam sessions across domains, colour-coded by institution type |
| G2 | **Localization / i18n Config** — No page manages Telugu/Hindi/Tamil/English content language toggles per exam domain | High | Add "Localization" tab to Exam Domain Config drawer (page 09) — language codes, default locale, content availability per language, translation status % |
| G3 | **Student Impersonation on Test Tenants** — QA needs to log in as a specific student on a test tenant to validate full student-facing flows end-to-end | High | Add "Impersonate" tab to Test Tenant drawer (page 22) — search student account on that tenant, click "Impersonate" with 2FA, opens student portal in a new tab with impersonation banner; all actions are audit-logged; session auto-expires in 30 minutes |
| G4 | **API Rate Limits per Plan Tier** — API throttle values per tier (Starter: 100 req/min, Enterprise: 2,000 req/min) not configurable anywhere in Division B | Medium | Add "Rate Limits" tab to Plan Config edit drawer (page 04) — per-tier rate limit config for API calls, bulk exports, report generation, and exam submission endpoints |
| G5 | **Cross-Page Critical Alert Bus** — When a P0 defect opens, production flag kill-switch fires, or peak concurrent users spike, no page describes how alert banners cascade across all div-b pages | Medium | Add "Critical Alert Banner" as a shared component to pages 01, 02, 03, 21, 24, 25: server-side SSE or 60s poll checks a `platform_alerts` Redis key; if any P0-level alert exists, a red dismissible banner appears at the top of all div-b pages until the alert is cleared |
| G6 | **Pages 27 & 28 missing from master index** — Question Bank Manager and Revenue & Billing Dashboard existed as spec files but were not registered in this index | Critical | ✅ Fixed in this update — both pages added to their respective role groups above |
| G7 | **Student Portal Feature Entitlements missing** — Page 14 (Portal Feature Config) covers institution admin features only. Student-facing features per plan (Download results PDF: Standard+; Compare with toppers: Professional+; Offline exam: Enterprise) have no configuration page | High | Add "Student Features" tab to Portal Feature Config (page 14) — per-plan student-facing feature matrix, distinct from institution-staff feature matrix |
| G8 | **Parent Portal Config missing** — Parent access module (view child's performance, receive exam notifications, fee status, attendance) is plan-gated and institution-type-specific but not configurable anywhere in Division B | High | Add "Parent Access" section to Portal Feature Config (page 14) — per-institution-type parent portal toggle, per-plan feature set, notification preferences |
| G9 | **Content Flag & Error Report Manager missing** — Students and institutions report question errors (wrong answer, ambiguous wording, copyright violation). No workflow exists in Division B for PM Exam Domains to receive, review, and action these flags | High | Add "Content Flags" tab to Question Bank Manager (page 27) — flagged question queue, severity classification, review → confirm error → pull from bank → update workflow, reporter notification |
| G10 | **Advanced Test Data Management missing** — Test Tenant Manager (page 22) has basic data reset and scenario presets. Structured test data management (anonymized production snapshots, repeatable data fixtures per scenario, institution-type data generators) is not covered | Medium | Add "Test Data" tab to Test Tenant Manager (page 22) — named data fixtures, anonymized prod snapshot import, data generator config per institution type, fixture version history |
| G11 | **Competitive Benchmarking missing from Domain Analytics** — Page 13 (Domain Analytics) shows platform-internal metrics only. PM Exam Domains needs competitive context: how does EduForge's SSC question coverage compare to industry benchmarks? What % of actual exam questions appear in the bank? | Medium | Add "Benchmarking" section to Domain Analytics (page 13) — question bank coverage vs official syllabus %, difficulty distribution vs past paper analysis, topic gap identification |

---

## Implementation Priority Order

```
P0 — Must have before div-b goes live
  01-product-dashboard
  02-feature-flags

P1 — Sprint 2
  03-release-manager
  04-plan-config              (+ G4 amendment: rate limits tab)
  09-exam-domain-config       (+ G2 amendment: i18n tab in domain drawer)
  10-syllabus-builder
  11-test-series-manager      (+ G1 amendment: exam schedule calendar)
  12-exam-pattern-builder
  14-portal-feature-config
  21-qa-dashboard
  22-test-tenant-manager      (+ G3 amendment: student impersonation)
  24-performance-test-dashboard
  25-defect-tracker
  27-question-bank-manager    (NEW — PM Exam Domains)
  28-revenue-billing-dashboard (NEW — PM Platform)

P2 — Sprint 3
  05-product-roadmap
  06-ab-test-manager
  07-announcement-manager
  08-mobile-app-config
  13-domain-analytics
  15-institution-role-config
  16-portal-templates
  17-onboarding-workflow
  18-notification-template-manager
  19-design-system
  23-test-case-repository
  26-automation-monitor
  → G5 amendment (critical alert bus): implemented as shared component
    across pages 01, 02, 03, 21, 24, 25 in Sprint 3

P3 — Backlog
  20-ui-review-board
```

---

## Functional Coverage Matrix — All 5 Roles

> Confirms every role's core job can be fully done within Division B pages.

| # | Job to Be Done | Role | Pages Covering It |
|---|---|---|---|
| 1 | Monitor platform product health at a glance | PM Platform | 01 |
| 2 | Create, rollout, and kill-switch feature flags | PM Platform | 02 |
| 3 | Manage release pipeline from planning to production | PM Platform | 03 |
| 4 | Configure subscription plan tiers and entitlements | PM Platform | 04 |
| 5 | Manage product roadmap and track quarter capacity | PM Platform | 05 |
| 6 | Run controlled A/B experiments on institutions | PM Platform | 06 |
| 7 | Send product announcements to 2,050 institutions | PM Platform | 07 |
| 8 | Configure Flutter mobile app versions and policies | PM Platform | 08 |
| 9 | Monitor revenue, MRR/ARR, churn, GST compliance | PM Platform | 28 |
| 10 | Configure exam domains and publish/unpublish them | PM Exam Domains | 09 |
| 11 | Build and version exam syllabus hierarchies | PM Exam Domains | 10 |
| 12 | Create and manage test series with 100K+ enrollments | PM Exam Domains | 11 |
| 13 | Build exam patterns with normalization formulas | PM Exam Domains | 12 |
| 14 | View domain-level analytics and adoption | PM Exam Domains | 13 |
| 15 | Manage 2M+ question bank quality and coverage | PM Exam Domains | 27 |
| 16 | Configure 80+ portal features per institution type | PM Institution Portal | 14 |
| 17 | Define institution-side roles and permissions | PM Institution Portal | 15 |
| 18 | Manage portal layout templates and white-labelling | PM Institution Portal | 16 |
| 19 | Build and monitor institution onboarding flows | PM Institution Portal | 17 |
| 20 | Manage notification templates (email/SMS/WhatsApp) | PM Institution Portal | 18 |
| 21 | Browse component library and audit design tokens | UI/UX Designer | 19 |
| 22 | Log and track production design deviations | UI/UX Designer | 20 |
| 23 | Monitor QA coverage, defects, and release readiness | QA Engineer | 21 |
| 24 | Create and manage test tenant sandboxes | QA Engineer | 22 |
| 25 | Manage test cases, plans, and traceability | QA Engineer | 23 |
| 26 | Run 74K concurrent load tests and gate releases | QA Engineer | 24 |
| 27 | Track full defect lifecycle and triage severity | QA Engineer | 25 |
| 28 | Monitor CI/CD pipeline health and flaky tests | QA Engineer | 26 |
| 29 | Create and manage promotional codes / partner discounts | PM Platform | 29 |
| 30 | Configure result processing, rank formulas, normalization params | PM Exam Domains | 30 |
| 31 | Manage white-label brand kits and subdomain provisioning | PM Institution Portal | 31 |
| 32 | Manage third-party integrations and sync health | PM Platform | 32 |
| 33 | Run functional API test suites and CI contract tests | QA Engineer | 33 |
| 34 | Configure student-facing per-plan features | PM Institution Portal | 14 (G7) |
| 35 | Configure parent portal access and capabilities | PM Institution Portal | 14 (G8) |
| 36 | Review and action user-reported question content flags | PM Exam Domains | 27 (G9) |
| 37 | Manage structured test data fixtures and prod snapshots | QA Engineer | 22 (G10) |
| 38 | Benchmark question bank vs official syllabus and past papers | PM Exam Domains | 13 (G11) |
| 39 | Manage all school/college board configurations (CBSE/ICSE/state/IB) | PM Exam Domains | 34 (new) |
| 40 | Manage 300+ national exam catalog entries with cutoff/salary data | PM Exam Domains | 35 (new) |

---

*Last updated: 2026-03-26*
*Total pages: 35 (26 original + 9 new: pages 27–35)*
*Indian education additions: Board & Curriculum Manager (34) · National Exam Catalog Manager (35)*
*Functional gaps identified: 11 · All 11 resolved: G6 fixed in index · G1–G5 assigned as amendments to existing pages · G7–G11 fully implemented as amendments to pages 14, 14, 27, 22, 13*
