# L-05 — Testimonials & Success Stories

> **URL:** `/coaching/marketing/testimonials/`
> **File:** `l-05-testimonials.md`
> **Priority:** P2
> **Roles:** Marketing Coordinator (K3) · Student Counsellor (K3) · Branch Manager (K6)

---

## 1. Testimonials Overview

```
TESTIMONIALS & SUCCESS STORIES — Toppers Coaching Centre
As of 31 March 2026

  TOTAL CONSENTED STORIES:   94 (all years)
  Active (published):         68
  Archived (withdrawn/expired): 26

  BY TYPE:
    Text testimonial (website/brochure): 48
    Video testimonial (YouTube/social):  28
    Photo + quote (social media):        18

  BY EXAM:
    SSC CGL selections:     38  (55.9%)
    IBPS PO/Clerk:          22  (32.4%)
    RRB PO/NTPC:             8  (11.8%)

  CURRENT YEAR (AY 2025–26):
    New stories collected (consented): 18
    Video stories (new):                6
    Pending consent (student agreed verbally, form not signed): 4
```

---

## 2. Success Story Profile

```
SUCCESS STORY — Published Profile
Student: Akhil Kumar (TCC-2401) | SSC CGL 2024

  CONSENT STATUS:
    Form signed:         ✅ 20 March 2026
    Consent type:        Full (name, photo, quote, video)
    Consent scope:       Website, social media, brochures, seminars
    Expiry:              No expiry stated (revocable any time)
    Marketing approved:  ✅ Branch Manager sign-off

  PUBLISHED ON:
    Website hero section:     ✅ Live (toppers-coaching.in/success-stories/)
    Instagram post:           ✅ 22 Mar 2026 (4,840 likes)
    YouTube reel:             ✅ 23 Mar 2026 (12,400 views)
    Physical brochure (2026): ✅ Printed — 2,000 copies
    Google Business post:     ✅ 24 Mar 2026

  STUDENT QUOTE (consented):
    "TCC's mock tests were harder than the real exam. When I sat for the
    actual SSC CGL, it felt like just another TCC mock. The Quant faculty's
    Caselet DI sessions were the deciding factor."
                                           — Akhil Kumar, Income Tax Inspector (2026)

  PERFORMANCE DATA SHOWN (with consent):
    Rank #1 in TCC batch | Score: 186/200 (mock) | SSC Tier-I: 164.25/200 (99.2%ile)

  REFERRALS GENERATED FROM THIS STORY:
    Enquiries mentioning "Akhil Kumar" or "that video":  28
    Enrolled from those enquiries:                         6
```

---

## 3. Testimonial Collection Process

```
TESTIMONIAL COLLECTION WORKFLOW

  TRIGGER:
    System flags students with:
      (a) Final exam result recorded in alumni tracker (J-06) AND
      (b) SSC/IBPS/RRB selection confirmed

  STEP 1 — Counsellor outreach (within 7 days of result):
    Congratulations call → mention testimonial request casually
    "Would you be open to sharing your experience for future students?"

  STEP 2 — Consent form (digital, DPDPA-compliant):
    Sent via WhatsApp / email
    Covers: name, photo, quote, video; scope of use; revocation right
    Verbal agreement ≠ legal consent — form must be signed

  STEP 3 — Story capture:
    Text quote: student writes or dictates; marketing edits for clarity only
    Video: 60–90 seconds; filmed at TCC or sent by student (mobile quality OK)
    Photo: professional headshot preferred; mobile photo acceptable

  STEP 4 — Review & publish:
    Marketing coordinator + Branch Manager review before publishing
    Student given a preview before publication (courtesy, not legal requirement)
    Published across approved channels

  PENDING CASES (verbal agreement, form not yet signed):
    Sravani P. (TCC-2408) — selected IBPS PO — form sent 28 Mar, awaiting
    Rajan K. (TCC-2415) — selected RRB PO — follow-up due 2 Apr
    Kavitha M. (TCC-2422) — SSC CHSL — prefers text only, form sent
    Vijay P. (TCC-2418) — SSC CGL — will sign after DV in Apr
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/marketing/testimonials/` | All published testimonials |
| 2 | `POST` | `/api/v1/coaching/{id}/marketing/testimonials/` | Add new testimonial with consent |
| 3 | `GET` | `/api/v1/coaching/{id}/marketing/testimonials/{tid}/` | Testimonial detail with consent status |
| 4 | `PATCH` | `/api/v1/coaching/{id}/marketing/testimonials/{tid}/withdraw/` | Process consent withdrawal |
| 5 | `GET` | `/api/v1/coaching/{id}/marketing/testimonials/pending-consent/` | Students with verbal but no signed consent |

---

## 5. Business Rules

- Every testimonial requires a signed consent form before publication; verbal or WhatsApp message agreement is not legally sufficient under DPDPA 2023 — the student must sign a consent form that clearly states what information will be used (name, photo, quote, video), where it will be published (website, social media, print), whether it can be used for advertising, and the student's right to withdraw consent; a testimonial published without this form exposes TCC to a data protection complaint; the four pending cases (verbal agreement) must not be published until forms are signed
- The student should be given a preview of the testimonial before it is published; while not a legal requirement, it is a courtesy that prevents misquotation disputes and builds trust; a student who feels their words were changed significantly ("I said the mock tests were hard, not that the real exam was easy") may withdraw consent or write a public counter-post; the marketing coordinator edits only for clarity and grammar, not for content; any substantive change to the student's message requires re-approval from the student
- Consent withdrawal must be processed within 30 days for digital content; when a student withdraws consent (e.g., Akhil Kumar's testimonial is to be removed), TCC must: (a) remove from the website; (b) remove from social media; (c) stop using in new ad campaigns; (d) update the consent record to "withdrawn"; printed materials already distributed do not need to be recalled, but the digital negative must be removed and no new print runs should include the testimonial; the withdrawal date and actions taken are documented for compliance
- Performance data published in testimonials (exam scores, ranks) must be accurate and verifiable from TCC's records; inflating a score ("she scored 186 but we'll say 190 to make it look better") or fabricating a rank is fraud under the Consumer Protection Act 2019; TCC publishes only data that matches the official result (for government exam scores) or TCC's mock test records (for mock scores); the alumni tracker (J-06) is the system of record; discrepancies between the testimonial and the records are flagged and corrected before publication
- Testimonials from students who are still enrolled (not yet selected) are treated differently from placed-alumni testimonials; an enrolled student saying "TCC is great, faculty is helpful" is a genuine current experience but lacks the ultimate outcome proof (exam selection); such testimonials are labelled "student experience" not "success story"; the distinction matters for consumers making enrollment decisions — a testimonial implying success when the student has not yet appeared for the exam could be misleading under Consumer Protection guidelines

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division L*
