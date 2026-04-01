# A-02 — Onboarding Wizard

> **URL:** `/partner/onboard/wizard/`
> **File:** `a-02-onboarding-wizard.md`
> **Priority:** P1
> **Roles:** TSP Owner (self-service steps) · EduForge Onboarding Specialist (support)

---

## 1. Wizard Steps

```
ONBOARDING WIZARD — TopRank Academy
Step 2 of 6 | Estimated: 45 min total

  PROGRESS:
  [✅ Account] → [🔵 Branding] → [○ Domain] → [○ Content] → [○ Payments] → [○ Go Live]

  STEP 1: ACCOUNT SETUP ✅ (completed)
    Admin account created: suresh@toprankacademy.in
    Password set, 2FA enabled
    Organisation record created in EduForge tenant system

  STEP 2: BRANDING (current — see A-03 for detail)
    Upload logo, set colours, configure portal name
    [Continue to Branding →]

  STEP 3: DOMAIN
    Subdomain: toprank.eduforge.in (auto-provisioned)
    Custom domain: www.toprankacademy.in (DNS setup guide provided)
    SSL certificate: auto-provisioned via Let's Encrypt

  STEP 4: CONTENT SETUP (see A-04 for detail)
    Import own questions (CSV/Excel upload)
    Select EduForge content licence tier (if applicable)
    Map exams and syllabus

  STEP 5: PAYMENT GATEWAY
    Connect TSP's own Razorpay/Paytm account
    Set student subscription pricing (TSP decides their own prices)
    Test payment flow

  STEP 6: GO LIVE (see A-05)
    Final review checklist
    Invite first batch of students
    [🚀 Launch Portal]
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/partner/onboard/status/` | Current onboarding step and progress |
| 2 | `PATCH` | `/api/v1/partner/onboard/step/{step}/complete/` | Mark step as complete |

---

## 5. Business Rules

- Each wizard step has a validation gate; the TSP cannot proceed to "Go Live" without completing branding (logo uploaded), domain (at least subdomain active), content (at least 1 mock test published or content licence activated), and payment (gateway connected or free-tier selected); a TSP that goes live with no content and no branding is a poor experience for their students and reflects badly on EduForge's platform quality
- The wizard is self-service but not unsupported; the assigned onboarding specialist monitors the TSP's progress and proactively reaches out if the TSP is stuck on a step for > 48 hours; common sticking points: DNS configuration (TSP doesn't know how to add a CNAME record), content import (CSV format errors), and payment gateway setup (KYC not complete on Razorpay); the specialist provides screen-share support for these steps
- The wizard creates the TSP's isolated tenant in EduForge's multi-tenant database; Step 1 provisions: a tenant ID, admin user, default role hierarchy (TSP Admin → TSP Faculty → TSP Student), and storage quota; all subsequent data (questions, students, mocks, analytics) is scoped to this tenant ID; a query from TSP-1's admin portal never returns TSP-2's data — the isolation is enforced at the database query layer, not just the UI
- The estimated 45-minute total is realistic for a tech-savvy TSP owner who has their logo, colour codes, content CSV, and Razorpay credentials ready; a non-technical TSP owner may take 2–3 days across multiple sessions; the wizard saves progress automatically — the TSP can close the browser and return later without losing completed steps

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division A*
