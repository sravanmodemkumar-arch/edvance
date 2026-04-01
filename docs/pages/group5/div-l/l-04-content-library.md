# L-04 — Content Library & Branding

> **URL:** `/coaching/marketing/content/`
> **File:** `l-04-content-library.md`
> **Priority:** P3
> **Roles:** Marketing Coordinator (K3) · Branch Manager (K6)

---

## 1. Content Library

```
CONTENT LIBRARY — Toppers Coaching Centre
Brand Assets & Published Content

  BRAND ASSETS:
    Category          │ Files │ Last Updated │ Notes
    ──────────────────┼───────┼─────────────┼──────────────────────────────────
    Logo (primary)    │   4   │ Jan 2025     │ PNG + SVG, dark/light variants
    Logo (icon only)  │   2   │ Jan 2025     │ Favicon + app icon
    Colour palette    │   1   │ Jan 2025     │ TCC Blue #1A3C6E, Gold #D4A017
    Typography guide  │   1   │ Jan 2025     │ Montserrat (headings), Open Sans
    Brand guidelines  │   1   │ Jan 2025     │ v2.1 — approved by Director
    Certificate template│  4  │ Mar 2026     │ Rank, Completion, Merit, Enroll
    ID card template  │   2   │ Aug 2025     │ Physical + digital formats
    ──────────────────┴───────┴─────────────┴──────────────────────────────────

  MARKETING MATERIALS:
    Category          │ Files │ Last Updated │ Channel
    ──────────────────┼───────┼─────────────┼──────────────────────────────────
    Brochure (general)│   3   │ Mar 2026     │ Print + digital PDF
    Batch-specific ads│  24   │ Mar 2026     │ Social (1080px, story, reel)
    Seminar banners   │   8   │ Mar 2026     │ Print (6×4 ft) + digital
    YouTube thumbnails│  16   │ Feb 2026     │ YouTube (1280×720)
    WhatsApp templates│  12   │ Mar 2026     │ Meta Business API approved
    Email templates   │   6   │ Feb 2026     │ HTML (mobile responsive)
    ──────────────────┴───────┴─────────────┴──────────────────────────────────

  PUBLISHED CONTENT (Blog / YouTube):
    Blog posts (total): 48  │  YTD 2026: 6  │  Avg organic sessions: 380
    YouTube videos:     84  │  YTD 2026: 12 │  Total views: 284,000
    Playlists:          12  │  (SSC, Banking, GK, CA, English, Quant...)
```

---

## 2. Content Calendar

```
CONTENT CALENDAR — April 2026

  Date    │ Content                                    │ Type    │ Channel    │ Owner     │ Status
  ────────┼────────────────────────────────────────────┼─────────┼────────────┼───────────┼────────
  Apr 1   │ "SSC CGL 2026 Notification — What changed" │ Blog    │ Website    │ Rajan K.  │ ✍️ Draft
  Apr 2   │ Akhil Kumar success reel                   │ Video   │ YT+Insta  │ Mktg team │ ✅ Ready
  Apr 3   │ Seminar promo — last day to register       │ Post    │ All social │ Deepa M.  │ ✅ Ready
  Apr 5   │ "Mock test vs real exam — what to expect"  │ Video   │ YouTube    │ Suresh K. │ ✍️ Draft
  Apr 7   │ Weekly GK digest (Apr W1)                  │ Story   │ Instagram  │ Mktg team │ 🔄 Template
  Apr 10  │ Demo class announcement                    │ Post    │ All social │ Mktg team │ ✅ Ready
  Apr 12  │ "Top 5 mistakes in Quant" carousel         │ Post    │ Insta      │ Suresh K. │ ✍️ Draft
  Apr 14  │ Alumni meet announcement                   │ Post    │ All social │ Mktg team │ 📅 Scheduled
  Apr 20  │ Parent orientation invite                  │ WA msg  │ WhatsApp   │ Counsellr │ 📅 Scheduled
  ────────┴────────────────────────────────────────────┴─────────┴────────────┴───────────┴────────
```

---

## 3. Brand Guidelines Summary

```
BRAND GUIDELINES — TCC v2.1 (Summary)

  VISUAL IDENTITY:
    Primary colour:   TCC Blue (#1A3C6E) — trust, knowledge
    Accent colour:    Gold (#D4A017) — excellence, achievement
    Background:       White (#FFFFFF) with light grey (#F5F5F5) for panels

  TYPOGRAPHY:
    Headings:   Montserrat Bold (digital) | Arial Bold (print fallback)
    Body text:  Open Sans Regular
    Certificates: Times New Roman (formal document context only)

  LOGO USAGE:
    ✅ Use on white or TCC Blue backgrounds
    ✅ Maintain minimum clear space (= logo height × 0.5 on all sides)
    ❌ Do not stretch, recolour, or add effects
    ❌ Do not place on busy photographic backgrounds without a white box

  TONE OF VOICE:
    Aspirational but honest: "Your success, our mission" — not "100% selection guaranteed"
    Indian cultural context: reference to family pride, government stability, career security
    Direct and informative: exam dates, eligibility, syllabus — accurate always
    Warm and supportive: never dismissive, never fear-based marketing

  PROHIBITED CONTENT:
    ❌ Unverified claims ("Best in Hyderabad" without a verifiable source)
    ❌ Success rate claims without the caveat "% of students who reported results"
    ❌ Student testimonials without written DPDPA consent
    ❌ Competitor disparagement (by name)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/marketing/content/library/` | Content library assets |
| 2 | `POST` | `/api/v1/coaching/{id}/marketing/content/library/` | Upload new asset |
| 3 | `GET` | `/api/v1/coaching/{id}/marketing/content/calendar/?month=2026-04` | Content calendar |
| 4 | `POST` | `/api/v1/coaching/{id}/marketing/content/calendar/` | Add content calendar item |
| 5 | `GET` | `/api/v1/coaching/{id}/marketing/content/brand-guidelines/` | Brand guidelines document |

---

## 5. Business Rules

- Brand consistency is maintained by requiring all marketing materials to be created using approved templates from the content library; a marketing coordinator who creates an ad with the wrong blue colour or a stretched logo erodes the brand's professionalism; the TCC Brand Guidelines v2.1 is the authoritative reference; any proposed change to the visual identity (new logo, colour change, typography update) requires Director approval; franchises may add their branch name to materials but must not alter the TCC core brand elements
- The content calendar is owned by the Marketing Coordinator but content is created with faculty input (subject-specific posts require faculty accuracy review); a Quant carousel ("Top 5 mistakes") drafted by marketing without Suresh K.'s review risks publishing incorrect exam strategies to thousands of followers; all exam-strategy content must be reviewed by the relevant faculty before publishing; the review turn-around time is 48 hours; content that misses its publishing date because of a late review is the faculty's accountability, not marketing's
- Tone of voice rules prevent fear-based and misleading marketing; "Don't fail your family — join TCC now" is fear-based marketing that exploits the social pressure many government exam aspirants already face; it may drive short-term conversions but damages brand trust and attracts students who are not genuinely motivated; TCC's philosophy is aspirational motivation ("you can do this, here's how TCC helps") over fear-based urgency; the Branch Manager reviews all ad copy before a campaign goes live
- Copyright of all content created by TCC's marketing team belongs to TCC; student success stories published with consent (testimonials, reels featuring student photos) are explicitly licensed by the student through the consent form (J-06 alumni consent process); if a student withdraws consent, the content must be removed from all active digital channels within 30 days; content featuring faculty must similarly have the faculty member's consent; a faculty who leaves TCC can request removal of their image from active marketing materials
- WhatsApp message templates must be pre-approved by Meta via the Business API before they can be sent to non-contacts; approval takes 2–3 business days; TCC maintains a library of 12 approved templates for common scenarios (batch open, seminar announcement, result celebration, payment reminder); a message that deviates from an approved template (even slightly) will be rejected by the API; the marketing coordinator must plan new message types at least 5 business days before the intended send date to allow time for Meta approval

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division L*
