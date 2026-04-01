# A-01 — Partner Signup & Application

> **URL:** `/partner/signup/`
> **File:** `a-01-partner-signup.md`
> **Priority:** P1
> **Roles:** Prospective TSP owner (public form) · EduForge Partnership Team (review)

---

## 1. Partner Application Form

```
BECOME AN EDUFORGE WHITE-LABEL PARTNER
Launch your own branded exam prep platform in 7 days

  ── ABOUT YOUR ORGANISATION ───────────────────────────────────────────
  Organisation name:    [ TopRank Academy                        ]
  Type:                 [ Coaching Centre ▼ ]
                        Options: Coaching Centre | Ed-tech Startup | Content Creator |
                                 Training Company | Individual Educator | Other
  Website (if any):     [ www.toprankacademy.in                  ]
  Founded year:         [ 2018 ]
  State:                [ Andhra Pradesh ▼ ]
  City:                 [ Vijayawada ]

  ── CONTACT PERSON ────────────────────────────────────────────────────
  Name:                 [ Suresh Reddy ]
  Designation:          [ Director ]
  Phone:                [ +91-98765-XXXXX ]
  Email:                [ suresh@toprankacademy.in ]

  ── YOUR REQUIREMENTS ─────────────────────────────────────────────────
  Target exams:         [ ✅ APPSC  ✅ SSC  ✅ Banking  ○ UPSC  ○ Other ]
  Current students:     [ 2,000–5,000 ▼ ]
  Do you have own questions? (●) Yes, some  (○) Yes, full bank  (○) No
  Do you need EduForge content licence? (●) Yes  (○) No, own content only
  Preferred plan:       [ Standard ▼ ]  (pricing shown after review)
  Custom domain needed? (●) Yes (toprank.eduforge.in + custom domain)  (○) No

  [Submit Application]

  WHAT HAPPENS NEXT:
    1. EduForge Partnership Team reviews (1–2 business days)
    2. Demo call scheduled (30 min — your requirements + platform walkthrough)
    3. Agreement signed (digital — pricing, SLA, data terms)
    4. Onboarding wizard activated (A-02) — setup in 3–5 days
    5. Go live! 🚀
```

---

## 2. Application Review (EduForge Internal)

```
PARTNER APPLICATION REVIEW — EduForge Partnership Team

  APPLICATION: TopRank Academy (Vijayawada, AP)
  Applied: 28 March 2026 | Status: ⏳ Under Review

  REVIEW CHECKLIST:
    ✅ Legitimate organisation (website verified, Google Business exists)
    ✅ Contact verified (phone call completed)
    ✅ Student count plausible (2,000–5,000 for Vijayawada coaching centre)
    🟡 Content: Has ~4,000 own questions (SSC + APPSC) — needs EduForge licence for Banking
    ✅ No competing platform affiliation (not already on TestBook/Oliveboard white-label)
    ✅ Payment capacity confirmed (willing to pay Standard plan)

  DECISION: [✅ Approve]  [❌ Reject — reason: ___]  [🔄 Request more info]
  Approved by: Rajan M. (Partnership Lead) | 29 Mar 2026
  → Onboarding wizard link sent to suresh@toprankacademy.in
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/partner/signup/` | Submit partner application |
| 2 | `GET` | `/api/v1/admin/partner/applications/` | All applications (EduForge internal) |
| 3 | `PATCH` | `/api/v1/admin/partner/applications/{id}/review/` | Approve/reject application |

---

## 5. Business Rules

- TSP partner vetting ensures platform quality; EduForge white-labels its technology to legitimate education businesses, not to spam operations or content pirates; the review checklist verifies: organisation exists (website, Google Business, or physical presence), contact person is real (phone call), student count is plausible for the organisation size, and the TSP is not already white-labelling a competing platform; rejecting a dubious application protects EduForge's brand and existing TSP partners
- Content licensing intent (whether the TSP needs EduForge's question pool) is captured upfront because it affects pricing; a TSP with 50,000 own questions pays only for the platform; a TSP that needs to licence 18 lakh questions from EduForge's pool pays a content licence fee on top of the platform fee; the content licence is per-student-per-month, not a one-time fee, because the content pool is continuously updated (new questions, new CA entries)
- The "no competing platform affiliation" check is a business protection; if a TSP is simultaneously using TestBook's white-label and EduForge's white-label, they may be comparing platforms to eventually choose one — which is fine — but they must not use EduForge's licensed content on the other platform; the partnership agreement includes an exclusivity clause for EduForge-licensed content (the TSP's own content is their property and can be used anywhere)
- The 7-day signup-to-live timeline is a competitive advantage; competing white-label platforms take 30–60 days; EduForge achieves 7 days because the onboarding wizard (A-02) automates brand setup, domain configuration, and content import; the TSP owner does most of the setup themselves (self-service) with EduForge support on call; a dedicated onboarding specialist is assigned for the first 30 days to handle issues

---

*Last updated: 2026-03-31 · Group 7 — TSP White-Label Portal · Division A*
