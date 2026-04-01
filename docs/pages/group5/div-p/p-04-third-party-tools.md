# P-04 — Third-Party Tools & APIs

> **URL:** `/coaching/partners/tools/`
> **File:** `p-04-third-party-tools.md`
> **Priority:** P3
> **Roles:** IT Coordinator (K3) · Branch Manager (K6)

---

## 1. Third-Party Tools Inventory

```
THIRD-PARTY TOOLS & APIs — TCC Technology Stack
As of 31 March 2026

  TOOL                  │ Category        │ Usage                        │ Data Shared      │ DPDPA OK?
  ──────────────────────┼─────────────────┼──────────────────────────────┼──────────────────┼──────────
  Razorpay              │ Payment         │ Fee collection               │ Student name, amt│ ✅ DPA signed
  Google Workspace      │ Productivity    │ Staff email + docs           │ Staff emails      │ ✅ DPA signed
  Meta Business API     │ Communication   │ WA broadcast + ad targeting  │ Phone numbers    │ ✅ DPA signed
  Google Ads            │ Advertising     │ Search + display ads         │ Demographics only│ ✅ No PII
  Google Analytics      │ Web analytics   │ Website traffic analysis     │ Anonymised IPs   │ ✅ Cookie notice
  Zoom                  │ Video conf.     │ Online classes               │ Student name+email│ ✅ DPA signed
  Microsoft 365         │ Productivity    │ Staff office tools           │ Staff data only  │ ✅ DPA signed
  ESET Antivirus        │ Security        │ Endpoint protection          │ Threat data only │ ✅ No PII
  pfSense (open source) │ Firewall        │ Network security             │ None (on-premise)│ ✅ N/A
  Tally Prime           │ Accounting      │ Bookkeeping + tax            │ Financial only   │ ✅ On-premise
  Google Search Console │ SEO             │ Organic search monitoring    │ Anonymised search│ ✅ No PII
  ──────────────────────┴─────────────────┴──────────────────────────────┴──────────────────┴──────────

  DATA PROCESSING AGREEMENTS (DPA):
    All tools that receive student personal data: DPA signed ✅
    DPA ensures: Indian data hosting (or adequacy), breach notification,
                 deletion on contract end, audit rights for TCC
    Tools with no student PII (Google Ads demographics, Analytics anonymised):
                 DPA not required — privacy notice on website sufficient
```

---

## 2. API Integration Details

```
API INTEGRATION DETAILS

  RAZORPAY:
    Authentication:   API Key (secret) + Webhook signature (HMAC-SHA256)
    Endpoints used:   POST /orders (create), GET /payments (verify),
                      POST /refunds (refund), Webhook endpoint
    Rate limit:       500 requests/min (well within TCC's usage)
    Key rotation:     Every 6 months (next: June 2026)
    Docs:             razorpay.com/docs

  META BUSINESS API (WhatsApp):
    Authentication:   System User Token (permanent, scoped to WABA)
    Endpoints used:   POST /messages (send), GET /templates (list)
    Rate limit:       1,000 msgs/day per phone number (sufficient for TCC)
    Template review:  2–3 business days per template
    Docs:             developers.facebook.com/docs/whatsapp

  ZOOM SDK:
    Authentication:   Server-to-Server OAuth (no user login needed)
    Usage:            Create/start meeting, join URL generation, attendance webhook
    Attendance:       Zoom join/leave timestamps → EduForge via webhook → LMS attendance
    Docs:             developers.zoom.us

  GOOGLE ANALYTICS 4 (website):
    Implementation:   gtag.js (cookied) + consent mode v2
    Consent mode:     Data collection delayed until user accepts cookies
    PII:              No PII sent to Google Analytics (User ID hashed) ✅
    Cookie notice:    Displayed on first visit ✅ (consent-first)
```

---

## 3. Tool Governance

```
TOOL GOVERNANCE — Approval & Review Process

  TOOL ONBOARDING (new tool request):
    Step 1: Department requests new tool (e.g., "we want to use Canva Pro")
    Step 2: IT Coordinator reviews: security, data handling, DPDPA compliance
    Step 3: If student data involved: Director approves + DPA executed
    Step 4: If no student data: Branch Manager approves (< ₹5,000/yr budget)
    Step 5: Tool added to inventory, staff trained on data handling policy

  TOOL OFFBOARDING (contract end or replacement):
    Step 1: Export all TCC data from the tool before deactivation
    Step 2: Request data deletion confirmation from vendor (DPA clause)
    Step 3: Update integration map and remove API credentials
    Step 4: Update DPDPA consent records if students were data subjects

  SHADOW IT POLICY:
    Staff cannot use personal tools (personal Dropbox, personal email)
    for TCC's business data; all tools must be approved and in the inventory;
    a staff member who stores student data on personal Google Drive violates
    DPDPA and TCC's data handling policy; the IT coordinator conducts
    quarterly checks on staff devices for unapproved tool usage

  UPCOMING TOOL DECISIONS:
    Canva for Teams (Apr 2026): Marketing requested — ₹4,800/yr, no PII → approved ✅
    AI doubt matching (Apr 2026): EduForge v4.3.0 built-in — no external tool ✅
    CRM upgrade (Q3 2026): Evaluate if EduForge CRM meets growing franchise needs
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/partners/tools/` | Third-party tools inventory |
| 2 | `POST` | `/api/v1/coaching/{id}/partners/tools/request/` | Request new tool onboarding |
| 3 | `GET` | `/api/v1/coaching/{id}/partners/tools/dpa-status/` | DPA signing status per tool |
| 4 | `PATCH` | `/api/v1/coaching/{id}/partners/tools/{tid}/` | Update tool details or status |

---

## 5. Business Rules

- Every tool that processes student personal data must have a signed Data Processing Agreement (DPA) with TCC before deployment; the DPA is not optional — it is a DPDPA 2023 requirement that TCC (as data fiduciary) must ensure its processors (tool vendors) are contractually bound to DPDPA-compliant data handling; a vendor who refuses to sign a DPA is not an eligible vendor for TCC if student data is involved; the IT coordinator maintains the DPA register and flags upcoming DPA renewals 60 days before expiry
- The shadow IT policy exists because unsanctioned tools create DPDPA blind spots; if a staff member stores student contact lists in their personal email drafts folder to send WhatsApp messages from their phone, TCC has no visibility or control over that data; if that personal email account is hacked, student contact data is breached; the breach obligation (72-hour DPDPB notification) falls on TCC even though the IT coordinator had no knowledge of the data being stored there; preventing shadow IT is a data protection imperative, not just an IT policy
- Google Analytics implementation uses consent mode v2 (required since January 2024 for Google's EEA compliance and adopted by TCC as best practice); cookies are only set for analytics after the user accepts the cookie notice; a user who rejects cookies still has their session counted but without persistent identifiers; this consent-first approach is aligned with DPDPA 2023's consent requirement for non-essential data collection; the cookie notice and Privacy Policy must be reviewed annually (or when Google updates its consent requirements) to maintain compliance
- API key management follows the principle of least privilege; Razorpay's API key used by EduForge is scoped to payment processing only — it cannot access Razorpay's reporting API or account management API; similarly, Meta's system user token is scoped to WhatsApp messaging only, not to Facebook page management or ad account access; over-privileged API keys (with broad access "just in case") create security risks if the key is compromised; the IT coordinator documents the exact scopes of each API key in the tool inventory
- When a tool contract ends (e.g., switching from Zoom to Google Meet), TCC must exercise the DPA clause requiring data deletion; Zoom holds historical class participant data (names, email addresses, join/leave timestamps) that was used for attendance tracking; TCC must request confirmed deletion of this data after migrating to the new platform; a transition that focuses only on the new tool setup and ignores data deletion from the old tool creates a DPDPA residual data risk; the IT coordinator must get written confirmation of deletion from Zoom's privacy team before the transition is considered complete

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division P*
