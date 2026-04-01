# J-06 — Alumni & Success Tracker

> **URL:** `/coaching/student-affairs/alumni/`
> **File:** `j-06-alumni-tracker.md`
> **Priority:** P2
> **Roles:** Student Counsellor (K3) · Branch Manager (K6) · Marketing (K3)

---

## 1. Alumni Overview

```
ALUMNI TRACKER — Toppers Coaching Centre
All batches | As of 30 March 2026

  TOTAL ALUMNI (all years):        4,840
  Government jobs secured (known): 1,284  (26.5% of alumni)
  Success rate tracking:
    Alumni who shared results:     2,640  (54.5%)
    Confirmed selections:          1,284  (48.6% of those who shared)
    Result not reported:           2,200  (45.5%) — DPDPA-compliant (consent required)

  CURRENT YEAR (SSC CGL 2024 results — declared Feb 2026):
    TCC batch students appeared:   184
    Tier-I cleared:                 96   (52.2%)
    Final selections (known):       28   (15.2%)

  POST SELECTIONS (known jobs — cumulative):
    SSC CGL (Tax Inspector, Auditor etc):   526
    IBPS PO / Clerk:                        284
    RRB PO / NTPC:                          186
    State PSC:                              142
    Others:                                 146
```

---

## 2. Success Story Profile

```
SUCCESS PROFILE — Akhil Kumar (TCC-2401)
Batch: SSC CGL 2025–26 Morning

  JOURNEY:
    Enrolled: Aug 2025 | Batch: SSC CGL Morning (May 2025)
    Rank in batch: #1 (consistently Mock #21–25)
    Avg full mock score: 172/200 (mock series)

  EXAM RESULT (SSC CGL 2024, results Feb 2026):
    Tier-I Score: 164.25/200 (percentile 99.2%)
    Tier-II:     Cleared ✅
    Final posting: Income Tax Inspector (awaited — DV in Apr 2026)

  TCC RECORD:
    Attendance: 95.4% (full year)
    Tests taken: 28 full mocks + 36 sectionals
    Rank improvement: Mock #1: 124/200 → Mock #25: 186/200 (+62 pts)
    Doubt sessions: 24 submitted, avg response 4.3/5

  MARKETING CONSENT:
    (●) Consent given for testimonial  ✅
    Name visible: Akhil Kumar (full name)
    Photo: Provided (professional headshot)
    Quote: "TCC's mock tests were harder than the real exam. When I sat
            for the actual SSC CGL, it felt like just another TCC mock.
            The Quant faculty's Caselet DI sessions were the deciding factor."

  REFERRALS MADE: 4 students enrolled due to Akhil's recommendation ✅
```

---

## 3. Alumni Engagement

```
ALUMNI COMMUNICATION — March 2026

  ACTIVE ALUMNI IN TCC NETWORK:
    WhatsApp group (TCC Alumni): 842 members (self-joined) ✅
    LinkedIn TCC page followers: 1,240
    Newsletter subscribers:       680

  ALUMNI ACTIVITIES (AY 2026–27):
    Batch guest sessions:          3  (2 SSC, 1 Banking alumni spoke to current batches)
    Referrals from alumni:         12 new students enrolled via alumni referrals
    Testimonials collected:        18  (video: 6, text: 12)
    Alumni mentoring (pairs):       8  (alumni mentor + current at-risk student)

  UPCOMING:
    Apr 15: Alumni meet (Hyderabad Main) — 45 RSVPs received
    May 1: Alumni testimonial video compilation for new batch orientation
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-affairs/alumni/` | Alumni database |
| 2 | `GET` | `/api/v1/coaching/{id}/student-affairs/alumni/{aid}/` | Alumni profile |
| 3 | `POST` | `/api/v1/coaching/{id}/student-affairs/alumni/result/` | Record alumni exam result |
| 4 | `GET` | `/api/v1/coaching/{id}/student-affairs/alumni/success-stories/` | Consented success stories for marketing |
| 5 | `GET` | `/api/v1/coaching/{id}/student-affairs/alumni/stats/?year=2026` | Annual alumni stats |

---

## 5. Business Rules

- Alumni result tracking is opt-in; TCC cannot compel former students to report their exam results; the 54.5% reporting rate means 45.5% of alumni either didn't share, didn't appear, or don't maintain contact; the reported success rate (48.6% of those who shared = 26.5% of total alumni) is published in TCC's marketing with the caveat "% of alumni who reported results"; publishing it without the caveat would misrepresent the true effectiveness rate (which could be lower if non-reporters had lower success); DPDPA 2023 and Consumer Protection Act 2019 require truthful marketing
- Marketing consent for success stories (name, photo, quote) must be explicit and documented; a student who shared their result in casual conversation did not give marketing consent; the consent form explicitly asks: "Can we use your name and photo in our marketing materials?"; consent can be withdrawn at any time; when consent is withdrawn, TCC must remove the testimonial from all active channels within 30 days; archived materials (printed brochures already distributed) do not need to be recalled, but digital content must be removed
- The alumni mentoring programme (alumni mentor + at-risk student) is one of TCC's most effective welfare tools; a recently-placed alumnus who cleared SSC CGL can provide authentic motivation and practical advice ("here's exactly how I improved my Caselet DI in 3 weeks") that a counsellor cannot; the mentoring programme requires volunteer alumni commitment; alumni are screened for suitability (no ongoing legal issues with TCC, positive attitude) and given a brief orientation; the counsellor coordinates and monitors the pairs
- Alumni referrals (12 students enrolled via alumni recommendation) are tracked for revenue attribution; these referrals are slightly different from student-referrals (F-08) because alumni are former students, not current ones; TCC's referral reward applies to current students; alumni referrals are rewarded differently (a "TCC Ambassador" recognition, not a cash reward) to maintain tax clarity; if TCC pays cash rewards to alumni, they are taxable commission income under Section 194H, just like student referral rewards
- The Alumni WhatsApp group (842 members) is TCC's most scalable community asset; it generates organic word-of-mouth and provides TCC with a channel to share new batch openings, exam notifications, and success stories; the group is moderated by TCC (admin-only posts for official communication, but members can share their own job news); an active, well-moderated alumni group is a competitive moat that competitors cannot easily replicate — it takes years to build

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division J*
