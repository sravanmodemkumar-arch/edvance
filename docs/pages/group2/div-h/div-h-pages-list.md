# Division H — Hostel Management: Page Index

**Total Pages:** 33
**URL Base:** `/group/hostel/`
**Tech Stack:** Django 4.2 + HTMX 1.9 + Tailwind CDN · FastAPI · PostgreSQL 16

> **Division scope:** Full lifecycle management of hostel infrastructure across all branches —
> occupancy, admissions, fees (AC/Non-AC × Boys/Girls), mess operations, welfare incidents
> (Severity 1–4 daily tracking), security (biometric + CCTV + night patrol), parent visits,
> medical rooms, housekeeping, and discipline cases. Boys and Girls hostels are **always**
> managed separately. Small groups with 50–100 hostelers use 2–3 roles only.
> Laundry/Housekeeping Coordinator (G0) has NO EduForge access — work tracked by Hostel Director.

---

## Scale Context

| Dimension | Value |
|---|---|
| Institution Groups with hostels | ~100 of 150 (large groups: all; small groups: ~50%) |
| Hosteler students per large group | 5,000–30,000 |
| Hosteler students per small group | 50–100 |
| Hostel campuses per large group | 2–10 (separate Boys + Girls per branch) |
| AC rooms per large hostel | 30–60% of capacity |
| Non-AC rooms per large hostel | 40–70% of capacity |
| Mess capacity (large) | 500–3,000 meals per sitting |
| Welfare incidents per month (large) | 20–200 across all branches |
| Visitor entries per month (large) | 500–5,000 |
| Security guards on duty (large, all branches) | 50–200 |
| Medical room visits per month (large) | 100–800 |
| Discipline cases per month (large) | 5–30 |

---

## Division H — Role Summary

| # | Role | Level | Large | Small (if hostel) | Post-Login URL |
|---|---|---|---|---|---|
| 67 | Group Hostel Director | G3 | ✅ Dedicated | ✅ 1 person | `/group/hostel/director/` |
| 68 | Group Boys Hostel Coordinator | G3 | ✅ Dedicated | ❌ | `/group/hostel/boys/` |
| 69 | Group Girls Hostel Coordinator | G3 | ✅ Dedicated | ❌ | `/group/hostel/girls/` |
| 70 | Group Hostel Welfare Officer | G3 | ✅ Dedicated | ✅ Shared | `/group/hostel/welfare/` |
| 71 | Group Mess / Cafeteria Manager | G3 | ✅ Dedicated | ❌ | `/group/hostel/mess/` |
| 72 | Group Hostel Admission Coordinator | G3 | ✅ Dedicated | ✅ Shared | `/group/hostel/admissions/` |
| 73 | Group Hostel Fee Manager | G3 | ✅ Dedicated | ✅ Shared | `/group/hostel/fees/` |
| 74 | Group Hostel Security Coordinator | G3 | ✅ Dedicated | ❌ | `/group/hostel/security/` |
| 75 | Group Parent Visit Coordinator | G3 | ✅ Dedicated | ✅ Shared | `/group/hostel/parent-visits/` |
| 76 | Group Hostel Medical Coordinator | G3 | ✅ Dedicated | ✅ Shared | `/group/hostel/medical/` |
| 77 | Group Laundry / Housekeeping Coord | G0 | ✅ Large only | ❌ | NO PLATFORM ACCESS — external tools |
| 78 | Group Hostel Discipline Committee | G3 | ✅ Dedicated | ✅ Shared | `/group/hostel/discipline/` |

> G0 role (Laundry / Housekeeping Coord) does not log in to EduForge. Their work is tracked
> and visible through Hostel Director and Welfare Officer views in pages 29 and 31.

---

## Section 1 — Role Dashboards

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 01 | Hostel Director Dashboard | `/group/hostel/director/` | `01-hostel-director-dashboard.md` | P0 | ✅ |
| 02 | Boys Hostel Coordinator Dashboard | `/group/hostel/boys/` | `02-boys-hostel-coordinator-dashboard.md` | P0 | ✅ |
| 03 | Girls Hostel Coordinator Dashboard | `/group/hostel/girls/` | `03-girls-hostel-coordinator-dashboard.md` | P0 | ✅ |
| 04 | Hostel Welfare Officer Dashboard | `/group/hostel/welfare/` | `04-hostel-welfare-officer-dashboard.md` | P0 | ✅ |
| 05 | Mess Manager Dashboard | `/group/hostel/mess/` | `05-mess-manager-dashboard.md` | P0 | ✅ |
| 06 | Hostel Admission Coordinator Dashboard | `/group/hostel/admissions/` | `06-hostel-admission-coordinator-dashboard.md` | P0 | ✅ |
| 07 | Hostel Fee Manager Dashboard | `/group/hostel/fees/` | `07-hostel-fee-manager-dashboard.md` | P0 | ✅ |
| 08 | Hostel Security Coordinator Dashboard | `/group/hostel/security/` | `08-hostel-security-coordinator-dashboard.md` | P0 | ✅ |
| 09 | Parent Visit Coordinator Dashboard | `/group/hostel/parent-visits/` | `09-parent-visit-coordinator-dashboard.md` | P0 | ✅ |
| 10 | Hostel Medical Coordinator Dashboard | `/group/hostel/medical/` | `10-hostel-medical-coordinator-dashboard.md` | P0 | ✅ |
| 11 | Hostel Discipline Committee Dashboard | `/group/hostel/discipline/` | `11-hostel-discipline-committee-dashboard.md` | P0 | ✅ |

---

## Section 2 — Hosteler Registry & Occupancy

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 12 | Hosteler Registry | `/group/hostel/hostelers/` | `12-hosteler-registry.md` | P0 | ✅ |
| 13 | Hostel Occupancy Overview | `/group/hostel/occupancy/` | `13-hostel-occupancy-overview.md` | P0 | ✅ |
| 14 | Room Allocation Manager | `/group/hostel/rooms/` | `14-room-allocation-manager.md` | P1 | ✅ |

---

## Section 3 — Hostel Admissions

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 15 | Hostel Admission Pipeline | `/group/hostel/admissions/pipeline/` | `15-hostel-admission-pipeline.md` | P0 | ✅ |
| 16 | Hostel Seat Allocation | `/group/hostel/admissions/seats/` | `16-hostel-seat-allocation.md` | P1 | ✅ |

---

## Section 4 — Hostel Fee Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 17 | Hostel Fee Structure | `/group/hostel/fees/structure/` | `17-hostel-fee-structure.md` | P0 | ✅ |
| 18 | Hostel Fee Collection | `/group/hostel/fees/collection/` | `18-hostel-fee-collection.md` | P0 | ✅ |

---

## Section 5 — Mess & Cafeteria Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 19 | Mess Menu Manager | `/group/hostel/mess/menu/` | `19-mess-menu-manager.md` | P1 | ✅ |
| 20 | Mess Quality Audit | `/group/hostel/mess/quality/` | `20-mess-quality-audit.md` | P1 | ✅ |
| 21 | Mess Vendor Management | `/group/hostel/mess/vendors/` | `21-mess-vendor-management.md` | P1 | ✅ |

---

## Section 6 — Welfare Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 22 | Welfare Incident Tracker | `/group/hostel/welfare/incidents/` | `22-welfare-incident-tracker.md` | P0 | ✅ |
| 23 | Hostel Welfare Reports | `/group/hostel/welfare/reports/` | `23-hostel-welfare-reports.md` | P1 | ✅ |

---

## Section 7 — Security Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 24 | Hostel Security Dashboard | `/group/hostel/security/dashboard/` | `24-hostel-security-dashboard.md` | P0 | ✅ |
| 25 | Visitor Management | `/group/hostel/security/visitors/` | `25-visitor-management.md` | P1 | ✅ |

---

## Section 8 — Parent Visit Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 26 | Parent Visit Scheduler | `/group/hostel/parent-visits/scheduler/` | `26-parent-visit-scheduler.md` | P1 | ✅ |

---

## Section 9 — Medical Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 27 | Hostel Medical Tracker | `/group/hostel/medical/tracker/` | `27-hostel-medical-tracker.md` | P1 | ✅ |

---

## Section 10 — Discipline Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 28 | Hostel Discipline Cases | `/group/hostel/discipline/cases/` | `28-hostel-discipline-cases.md` | P1 | ✅ |

---

## Section 11 — Housekeeping Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 29 | Laundry & Housekeeping Tracker | `/group/hostel/housekeeping/` | `29-laundry-housekeeping-tracker.md` | P2 | ✅ |

---

## Section 12 — Policy, MIS, Analytics & Audit

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 30 | Hostel Policy Manager | `/group/hostel/policy/` | `30-hostel-policy-manager.md` | P1 | ✅ |
| 31 | Hostel MIS Report | `/group/hostel/reports/mis/` | `31-hostel-mis-report.md` | P1 | ✅ |
| 32 | Hostel Analytics | `/group/hostel/reports/analytics/` | `32-hostel-analytics.md` | P1 | ✅ |
| 33 | Hostel Audit Log | `/group/hostel/audit-log/` | `33-hostel-audit-log.md` | P1 | ✅ |

---

## Shared Drawers & Overlays (all div-h pages)

| Drawer / Modal | Trigger | Width | Tabs / Content |
|---|---|---|---|
| `hosteler-detail` | Registry → row | 640px | Profile · Room · Fee · Attendance · Medical · Welfare |
| `hosteler-create` | Registry → + Add Hosteler | 640px | Personal · Parent · Hostel Type · Room · Fee Plan |
| `hosteler-edit` | Registry → Edit | 640px | Same tabs |
| `hosteler-transfer` | Registry → Transfer | 520px | From Branch · To Branch · Room · Effective Date · Reason |
| `hosteler-exit` | Registry → Exit | 480px | Exit Date · Reason · Clearance checklist · Fee settlement |
| `room-allocate` | Room Manager → Allocate | 560px | Hosteler search · Room select · Bed number · AC/Non-AC · Effective date |
| `room-swap` | Room Manager → Swap | 480px | Hosteler A · Hosteler B · Reason · Effective date |
| `admission-application` | Admission Pipeline → row | 640px | Applicant · Parent · Stream · Hostel Pref · Documents · Status |
| `admission-approve` | Pipeline → Approve | 480px | Branch · Hostel Type · Room assign · Fee plan · Notify parent |
| `fee-plan-create` | Fee Structure → + New | 560px | Branch · Hostel Type · Academic Year · Tuition · Mess · Extras |
| `fee-plan-edit` | Fee Structure → Edit | 560px | Same fields |
| `defaulter-action` | Fee Collection → defaulter row | 480px | Balance · Last payment · Action: Remind / Waiver / Hold |
| `mess-menu-create` | Menu Manager → + Create | 560px | Branch · Week · Day-by-day meals · Nutritional notes |
| `quality-audit-create` | Mess Quality → + New Audit | 600px | Branch · Date · Hygiene checks · Food sample · Score · Photos |
| `vendor-create` | Mess Vendors → + New | 640px | Vendor · Category · Contract · Rate card · FSSAI · Payment |
| `welfare-incident-create` | Welfare → + New Incident | 600px | Hosteler · Branch · Severity · Description · Action taken · Follow-up |
| `welfare-incident-detail` | Welfare table → row | 640px | Overview · Timeline · Actions · Escalation · Resolution |
| `security-alert-create` | Security → + New Alert | 560px | Branch · Type · Location · Severity · Description · Action |
| `visitor-entry-create` | Visitors → + New Entry | 520px | Visitor name · Relation to hosteler · Hosteler name · ID proof · Purpose |
| `parent-visit-schedule` | Parent Visits → + Schedule | 560px | Branch · Date · Time slot · Allowed hosteler list · Biometric gate |
| `medical-visit-create` | Medical → + New Visit | 560px | Hosteler · Symptoms · Doctor · Prescription · Follow-up · Severity |
| `discipline-case-create` | Discipline → + New Case | 640px | Hosteler · Branch · Incident type · Description · Evidence · Initial action |
| `discipline-case-detail` | Discipline table → row | 680px | Case overview · Timeline · Hearings · Evidence · Decision · Appeal |
| `housekeeping-schedule-create` | Housekeeping → + New | 480px | Branch · Block · Type · Frequency · Contractor · Next due |
| `policy-create` | Policy Manager → + New | 600px | Title · Category · Applicability · Effective date · Document upload |
| `audit-detail` | Audit Log → row | 520px | Event · Before/After · Actor · IP · Session · Context |

---

## UI Component Standard (all div-h pages)

| Component | Specification |
|---|---|
| **Tables** | Sortable all columns · Checkbox row select + select-all · Responsive (card on mobile < 768px) · Column visibility toggle · Row count badge |
| **Search** | Full-text, 300ms debounce, highlights match in results |
| **Advanced Filters** | Slide-in filter drawer · Active filters as dismissible chips · "Clear All" · Filter count badge |
| **Pagination** | Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z" · Page jump input |
| **Drawers** | Slide from right · Widths: 480/520/560/600/640/680px · Backdrop click closes (unsaved-changes guard) · ESC closes |
| **Modals** | Centred overlay · Confirm/delete only · Max 480px · Primary + cancel buttons |
| **Forms** | Inline validation on blur · Required `*` · Character counter on textareas · Disabled submit until valid · Server error summary at top |
| **Toasts** | Bottom-right · Success 4s · Error manual dismiss · Warning 6s · Info 4s · Max 3 stacked |
| **Loaders** | Skeleton screens matching layout · Spinner on action buttons · Full-page overlay for critical ops |
| **Empty States** | Illustration + heading + description + CTA · Separate "no data" vs "no search results" |
| **Charts** | Chart.js 4.x · Responsive · Colorblind-safe palette · Legend · Tooltip · PNG export |
| **Role-based UI** | Server-side rendering — G0 has no access · G3 write within scope · G4 full |

---

## Role → Page Access Matrix

| Page | Hostel Dir G3 | Boys Coord G3 | Girls Coord G3 | Welfare G3 | Mess Mgr G3 | Adm Coord G3 | Fee Mgr G3 | Security G3 | Parent Visit G3 | Medical G3 | Discipline G3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 Director Dashboard | ✅ Full | — | — | — | — | — | — | — | — | — | — |
| 02 Boys Dashboard | ✅ View | ✅ Full | — | — | — | — | — | — | — | — | — |
| 03 Girls Dashboard | ✅ View | — | ✅ Full | — | — | — | — | — | — | — | — |
| 04 Welfare Dashboard | ✅ View | ✅ View | ✅ View | ✅ Full | — | — | — | — | — | — | — |
| 05 Mess Dashboard | ✅ View | — | — | ✅ View | ✅ Full | — | — | — | — | — | — |
| 06 Admissions Dashboard | ✅ View | ✅ View | ✅ View | — | — | ✅ Full | — | — | — | — | — |
| 07 Fee Dashboard | ✅ View | — | — | — | — | — | ✅ Full | — | — | — | — |
| 08 Security Dashboard | ✅ View | ✅ View | ✅ View | ✅ View | — | — | — | ✅ Full | — | — | — |
| 09 Parent Visit Dashboard | ✅ View | ✅ View | ✅ View | ✅ View | — | — | — | ✅ View | ✅ Full | — | — |
| 10 Medical Dashboard | ✅ View | — | — | ✅ View | — | — | — | — | — | ✅ Full | — |
| 11 Discipline Dashboard | ✅ View | ✅ View | ✅ View | ✅ View | — | — | — | ✅ View | — | — | ✅ Full |
| 12 Hosteler Registry | ✅ Full | ✅ Boys only | ✅ Girls only | ✅ View | — | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View |
| 13 Occupancy Overview | ✅ Full | ✅ Boys | ✅ Girls | ✅ View | — | ✅ View | ✅ View | ✅ View | — | — | — |
| 14 Room Allocation | ✅ Full | ✅ Boys | ✅ Girls | ✅ View | — | ✅ Allocate | — | — | — | — | — |
| 15 Admission Pipeline | ✅ Full | ✅ Boys | ✅ Girls | — | — | ✅ Full | — | — | — | — | — |
| 16 Seat Allocation | ✅ Full | ✅ Boys | ✅ Girls | — | — | ✅ Full | — | — | — | — | — |
| 17 Fee Structure | ✅ View | — | — | — | — | ✅ View | ✅ Full | — | — | — | — |
| 18 Fee Collection | ✅ View | — | — | — | — | — | ✅ Full | — | — | — | — |
| 19 Mess Menu | ✅ View | — | — | ✅ View | ✅ Full | — | — | — | — | — | — |
| 20 Mess Quality Audit | ✅ Full | — | — | ✅ View | ✅ Full | — | — | — | — | — | — |
| 21 Mess Vendors | ✅ View | — | — | — | ✅ Full | — | — | — | — | — | — |
| 22 Welfare Incidents | ✅ Full | ✅ Boys | ✅ Girls | ✅ Full | — | — | — | ✅ View | — | ✅ View | ✅ View |
| 23 Welfare Reports | ✅ Full | ✅ Boys | ✅ Girls | ✅ Full | — | — | — | — | — | — | — |
| 24 Security Dashboard | ✅ View | ✅ View | ✅ View | ✅ View | — | — | — | ✅ Full | — | — | — |
| 25 Visitor Management | ✅ View | ✅ Boys | ✅ Girls | ✅ View | — | — | — | ✅ Full | ✅ View | — | — |
| 26 Parent Visit Scheduler | ✅ View | ✅ Boys | ✅ Girls | ✅ View | — | — | — | ✅ View | ✅ Full | — | — |
| 27 Medical Tracker | ✅ View | — | — | ✅ View | — | — | — | — | — | ✅ Full | — |
| 28 Discipline Cases | ✅ View | ✅ Boys | ✅ Girls | ✅ View | — | — | — | ✅ View | — | ✅ View | ✅ Full |
| 29 Housekeeping Tracker | ✅ Full | — | — | ✅ View | — | — | — | — | — | — | — |
| 30 Policy Manager | ✅ Full | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View |
| 31 Hostel MIS Report | ✅ Full | ✅ Boys | ✅ Girls | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View |
| 32 Hostel Analytics | ✅ Full | ✅ Boys | ✅ Girls | ✅ View | ✅ View | ✅ View | ✅ View | ✅ View | — | ✅ View | — |
| 33 Hostel Audit Log | ✅ Full | ✅ Own actions | ✅ Own actions | ✅ Own | ✅ Own | ✅ Own | ✅ Own | ✅ Own | ✅ Own | ✅ Own | ✅ Own |

---

## Full Functional Coverage Audit — Zero Gaps

| # | Job to Be Done | Role | Page(s) |
|---|---|---|---|
| 1 | Command view of entire hostel system across all branches | Hostel Director | 01, 13 |
| 2 | Monitor all boys hostels — warden supervision, discipline | Boys Coordinator | 02, 12, 22 |
| 3 | Monitor all girls hostels — warden supervision, safety | Girls Coordinator | 03, 12, 22 |
| 4 | Track daily welfare incidents (Severity 1–4) | Welfare Officer | 04, 22, 23 |
| 5 | Manage food quality, daily menus, hygiene audits | Mess Manager | 05, 19, 20 |
| 6 | Process hostel admission applications, allocate seats | Admission Coordinator | 06, 15, 16 |
| 7 | Configure AC/Non-AC fee structures per branch | Fee Manager | 07, 17 |
| 8 | Track hostel fee collection, chase defaulters | Fee Manager | 07, 18 |
| 9 | Manage night security, CCTV policy, visitor register | Security Coordinator | 08, 24, 25 |
| 10 | Schedule and manage parent visits with biometric gate | Parent Visit Coordinator | 09, 26 |
| 11 | Track medical room visits, doctor schedules | Medical Coordinator | 10, 27 |
| 12 | Handle discipline cases, suspension from hostel | Discipline Committee | 11, 28 |
| 13 | Master registry of all hostelers across all branches | Hostel Director | 12 |
| 14 | View real-time occupancy — AC/Non-AC, Boys/Girls per branch | All hostel roles | 13 |
| 15 | Allocate and swap rooms for hostelers | Admission Coord / Boys/Girls Coord | 14 |
| 16 | End-to-end hostel admission pipeline (application → allocation) | Admission Coordinator | 15 |
| 17 | Cross-branch hostel seat planning and allocation | Admission Coordinator | 16 |
| 18 | Create and update fee plans (tuition + mess + extras) | Fee Manager | 17 |
| 19 | Daily fee collection monitoring and defaulter management | Fee Manager | 18 |
| 20 | Manage weekly/daily mess menus per branch | Mess Manager | 19 |
| 21 | Conduct and record mess quality/hygiene audits | Mess Manager | 20 |
| 22 | Manage caterer/vendor contracts and payments | Mess Manager | 21 |
| 23 | Real-time welfare incident tracking with severity escalation | Welfare Officer | 22 |
| 24 | Trend analysis of welfare events across branches | Welfare Officer / Director | 23 |
| 25 | Monitor CCTV coverage and security guard deployment | Security Coordinator | 24 |
| 26 | Record and manage visitor entries to hostel campus | Security Coordinator | 25 |
| 27 | Schedule parent visit slots and manage biometric entry | Parent Visit Coordinator | 26 |
| 28 | Log medical visits, prescriptions, doctor schedules | Medical Coordinator | 27 |
| 29 | Open, investigate, and close discipline cases | Discipline Committee | 28 |
| 30 | Track housekeeping schedules and quality standards | Hostel Director | 29 |
| 31 | Manage hostel-wide policies and SOPs | Hostel Director | 30 |
| 32 | Generate monthly hostel MIS for Chairman/Board | Hostel Director | 31 |
| 33 | Hostel occupancy and welfare trend analytics | Hostel Director | 32 |
| 34 | Immutable audit log of all hostel-level actions | Hostel Director | 33 |

---

## Functional Gaps — Fully Resolved

| Gap | Resolution |
|---|---|
| No post-login dashboards per hostel role | Pages 01–11 — dedicated dashboard per role |
| No master hosteler registry across branches | Page 12 — Hosteler Registry with type/branch/room/status |
| No real-time occupancy view (AC/Non-AC × Boys/Girls) | Page 13 — Occupancy Overview with heat-map by branch |
| Room allocation managed only on paper | Page 14 — Room Allocation Manager with drag-assign + swap |
| Hostel admission pipeline not tracked in EduForge | Page 15 — Admission Pipeline with application → approval flow |
| No cross-branch seat planning tool | Page 16 — Seat Allocation with waitlist and conflict detection |
| Fee structure (AC/Non-AC/Mess/Extras) not in platform | Page 17 — Fee Structure builder per branch × hostel type |
| Hostel fee defaulters tracked only in spreadsheets | Page 18 — Fee Collection with defaulter list and reminder actions |
| Mess menus not visible cross-branch | Page 19 — Mess Menu Manager with weekly planning grid |
| No structured hygiene audit workflow | Page 20 — Mess Quality Audit with checklist + photo evidence |
| Caterer contracts not tracked in EduForge | Page 21 — Mess Vendor Management with contract + payments |
| Welfare Severity 1–4 tracking not in platform | Page 22 — Welfare Incident Tracker with severity SLA timers |
| No cross-branch welfare trend analysis | Page 23 — Welfare Reports with incident heatmap |
| CCTV and night security untracked in EduForge | Page 24 — Security Dashboard with guard rosters + CCTV status |
| Visitor register maintained only on paper | Page 25 — Visitor Management digital register |
| Parent visit scheduling not centrally managed | Page 26 — Parent Visit Scheduler with biometric gate list |
| Medical room visits not logged in EduForge | Page 27 — Medical Tracker with visit log + prescription records |
| Discipline cases tracked in physical files only | Page 28 — Discipline Cases with full case lifecycle |
| Housekeeping standards not monitored in EduForge | Page 29 — Laundry & Housekeeping Tracker |
| No central hostel policy repository | Page 30 — Hostel Policy Manager with version history |
| No hostel MIS report for Chairman/Board | Page 31 — Auto-generated monthly Hostel MIS |
| No cross-hostel analytics | Page 32 — Hostel Analytics with occupancy + welfare + fee charts |
| No hostel-level audit log | Page 33 — Hostel Audit Log |

---

## Implementation Priority

```
P0 — Before hostel portal goes live
  01–11   All 11 role dashboards
  12      Hosteler Registry
  13      Hostel Occupancy Overview
  15      Hostel Admission Pipeline
  17      Hostel Fee Structure
  18      Hostel Fee Collection
  22      Welfare Incident Tracker
  24      Hostel Security Dashboard

P1 — Sprint 2
  14, 16, 19, 20, 21, 23, 25, 26, 27, 28, 30, 31, 32, 33

P2 — Sprint 3
  29
```

---

*Last updated: 2026-03-21 · Total pages: 33 · Roles: 12 (11 with platform access) · Gaps resolved: 23 · Audit: zero gaps remaining*
