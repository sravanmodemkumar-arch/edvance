# EduForge — Page Specifications Index

> Ultra-professional UI spec for all portals.
> Each page described section-by-section: layout, components, states, business rules.
> Built for 25L+ students across 1,900+ institutions.

---

## Folder Structure

```
docs/pages/
  ├── README.md                    ← This file
  │
  ├── components/                  ← Shared UI component library (reusable, all groups)
  │   ├── README.md
  │   ├── 01-table-pagination.md
  │   ├── 02-modal-drawer.md
  │   ├── 03-alerts-toasts.md
  │   ├── 04-filters-search.md
  │   ├── 05-forms-inputs.md
  │   ├── 06-navigation.md
  │   ├── 07-data-display.md
  │   └── 08-design-tokens.md
  │
  ├── auth/                        ← Global auth (shared across ALL groups)
  │   └── 01-authentication.md    ← Landing, Login, OTP, Role Selector, Profile Setup
  │
  ├── group1/                      ← Platform Admin Portal (EduForge employees)
  │   ├── div-a-executive.md
  │   ├── div-b-product-design.md
  │   ├── div-c-engineering.md
  │   ├── div-d-content-academics.md
  │   ├── div-e-video-learning.md
  │   ├── div-f-exam-operations.md
  │   ├── div-g-bgv.md
  │   ├── div-h-data-analytics.md
  │   ├── div-i-customer-support.md
  │   ├── div-j-customer-success.md
  │   ├── div-k-sales-bd.md
  │   ├── div-l-marketing.md
  │   ├── div-m-finance-billing.md
  │   ├── div-n-legal-compliance.md
  │   └── div-o-hr-admin.md
  │
  ├── group2/                      ← Institution Group Portal
  ├── group3/                      ← School Portal
  ├── group4/                      ← College Portal
  ├── group5/                      ← Coaching Portal
  ├── group6/                      ← Exam Domain Portals
  ├── group7/                      ← TSP White-label Portal
  ├── group8/                      ← Parent Portal
  ├── group9/                      ← B2B Partner Portal
  └── group10/                     ← Student Portal
```

---

## Shared Component Library

> ALWAYS reference these — never re-document a component.

| Component File | What It Covers |
|---|---|
| [01-table-pagination.md](components/01-table-pagination.md) | Data tables, sorting, bulk actions, pagination, export |
| [02-modal-drawer.md](components/02-modal-drawer.md) | Modals, side drawers, bottom sheets, stacked drawers |
| [03-alerts-toasts.md](components/03-alerts-toasts.md) | Toast messages, alert banners, confirm dialogs, empty states |
| [04-filters-search.md](components/04-filters-search.md) | Search bar, quick filter chips, advanced filter panel, date picker |
| [05-forms-inputs.md](components/05-forms-inputs.md) | All input types, validation, date/time, file upload, form layout |
| [06-navigation.md](components/06-navigation.md) | Top nav, sidebar, tabs, breadcrumb, step progress, notifications |
| [07-data-display.md](components/07-data-display.md) | Stat cards, badges, avatars, progress bars, charts |
| [08-design-tokens.md](components/08-design-tokens.md) | Colors, typography, spacing, shadows, breakpoints, motion |

---

## Auth Pages (Global)

| Page | File | Covers |
|---|---|---|
| Authentication | [auth/01-authentication.md](auth/01-authentication.md) | Smart landing, login, OTP, role selector, profile setup, 2FA, session |

---

## Group 1 — Platform Admin Portal (`admin.eduforge.in`)

| Division | File | Roles Covered |
|---|---|---|
| A — Executive | [group1/div-a-executive.md](group1/div-a-executive.md) | CEO, CTO, COO, CFO |
| B — Product & Design | [group1/div-b-product-design.md](group1/div-b-product-design.md) | PMs, UX Designer, QA |
| C — Engineering | [group1/div-c-engineering.md](group1/div-c-engineering.md) | Backend, Frontend, DevOps, DBA, Security, AI/ML |
| D — Content & Academics | [group1/div-d-content-academics.md](group1/div-d-content-academics.md) | SMEs, Reviewer, Approver, Notes Editor |
| E — Video & Learning | [group1/div-e-video-learning.md](group1/div-e-video-learning.md) | Video Curator, Playlist Manager, YouTube Manager |
| F — Exam Operations | [group1/div-f-exam-operations.md](group1/div-f-exam-operations.md) | Exam Ops Manager, Results, Notification, Incident |
| G — BGV | [group1/div-g-bgv.md](group1/div-g-bgv.md) | BGV Manager, Executive, POCSO Officer |
| H — Data & Analytics | [group1/div-h-data-analytics.md](group1/div-h-data-analytics.md) | Analytics, Data Engineer, AI Gen Manager |
| I — Customer Support | [group1/div-i-customer-support.md](group1/div-i-customer-support.md) | L1/L2/L3 Support, Onboarding Specialist |
| J — Customer Success | [group1/div-j-customer-success.md](group1/div-j-customer-success.md) | CSM, Account Manager, Renewal |
| K — Sales & BD | [group1/div-k-sales-bd.md](group1/div-k-sales-bd.md) | Sales Manager, Executives, Partnership |
| L — Marketing | [group1/div-l-marketing.md](group1/div-l-marketing.md) | Marketing Manager, SEO, Social Media |
| M — Finance & Billing | [group1/div-m-finance-billing.md](group1/div-m-finance-billing.md) | Finance Manager, Billing Admin, GST |
| N — Legal & Compliance | [group1/div-n-legal-compliance.md](group1/div-n-legal-compliance.md) | Legal Officer, DPO, POCSO Reporting |
| O — HR & Administration | [group1/div-o-hr-admin.md](group1/div-o-hr-admin.md) | HR Manager, Recruiter, Admin |

---

## Page Spec Format Standard

Every page spec must include these sections:

```markdown
# Page: [Name]

## Overview
- Route, purpose, access level

## Page Sections
### Section: [Header / Sidebar / Main / Footer etc.]
- Purpose, layout, all components, states

## Component References
→ [Component name](../../components/XX.md) — context of use

## Business Rules
- Who can see this page
- What triggers state changes

## API Calls
- Endpoint, method, when triggered
```
