# P-01 — Partner & Integration Overview

> **URL:** `/coaching/partners/`
> **File:** `p-01-partner-overview.md`
> **Priority:** P2
> **Roles:** Director (K7) · Branch Manager (K6) · IT Coordinator (K3)

---

## 1. Partner Ecosystem

```
PARTNER & INTEGRATION ECOSYSTEM — Toppers Coaching Centre
As of 31 March 2026

  TECHNOLOGY PARTNERS:
    Partner           │ Category         │ Integration Type  │ Status  │ Contract
    ──────────────────┼──────────────────┼───────────────────┼─────────┼──────────────
    EduForge Pvt Ltd  │ Core SaaS        │ Native platform   │ ✅ Live │ Annual (Dec)
    Razorpay          │ Payment gateway  │ API (REST)        │ ✅ Live │ Pay-per-use
    Google Workspace  │ Email + Docs     │ OAuth + API       │ ✅ Live │ Annual (Sep)
    Meta Business API │ WhatsApp + Ads   │ API (REST)        │ ✅ Live │ Pay-per-use
    Google Ads        │ Paid search      │ API (REST)        │ ✅ Live │ Pay-per-use
    Zoom              │ Online classes   │ API (SDK)         │ ✅ Live │ Annual (Apr)
    ESET              │ Antivirus        │ On-premise agent  │ ✅ Live │ Annual (Oct)

  EXAM BODY REFERENCES (no API — informational links):
    Staff Selection Commission (SSC):    ssc.nic.in
    IBPS (Banking):                      ibps.in
    Railway Recruitment Board (RRB):     indianrailways.gov.in/rrbcdg
    State PSC (Telangana):               tspsc.gov.in

  FINANCIAL INTEGRATIONS:
    HDFC Bank (salaries):    Net banking + NEFT batch
    Axis Bank (collections): Payment gateway settlement + account
    GST Portal:              GSTN integration (via CA/ERP)
    TDS Portal (TRACES):     Manual filing via CA with TAN login

  PARTNER HEALTH:
    All integrations: ✅ Operational (31 Mar 2026)
    Last integration check: Daily (automated by IT coordinator)
```

---

## 2. Integration Architecture

```
INTEGRATION ARCHITECTURE — TCC Technology Stack

  STUDENTS (mobile/web)
      │
      ▼
  ┌───────────────────────────────────────────────────────────┐
  │                   EduForge Portal (SaaS)                  │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │
  │  │ Admissions│ │Academic  │ │ Finance  │ │Student Afrs  │ │
  │  │ (Div F)   │ │(Div C,D) │ │(Div G)   │ │(Div J)       │ │
  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │
  └──────────────────────────┬────────────────────────────────┘
                             │ API calls
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────────┐   ┌───────────────┐
    │ Razorpay │      │  Zoom SDK    │   │  Meta API     │
    │ (payment)│      │(online class)│   │(WA + ads)     │
    └──────────┘      └──────────────┘   └───────────────┘
          │
          ▼
    Bank settlement
    (Axis Bank account)

  DATA FLOW:
    Student pays → Razorpay → EduForge fee module → receipt generated
    Student attends online → Zoom → EduForge LMS → attendance recorded
    Admin sends WA → EduForge notification → Meta API → student's phone
```

---

## 3. Partner SLA Summary

```
PARTNER SLA SUMMARY — Q3 AY 2025–26

  Partner      │ Our SLA with them  │ Their uptime (Q3)│ Issues Q3 │ Next review
  ─────────────┼────────────────────┼──────────────────┼───────────┼────────────
  EduForge     │ 99.5% uptime       │ 99.6% ✅         │ 1 (Mar12) │ Dec 2026
  Razorpay     │ 99.9% uptime       │ 99.98% ✅        │ 0         │ Ongoing
  Zoom         │ 99.9% uptime       │ 99.92% ✅        │ 1 (WA8)   │ Apr 2026
  Meta API     │ Best effort (Meta) │ 99.7% est. ✅    │ 0         │ Ongoing
  Google Ads   │ No SLA (service)   │ 99.9%+ ✅        │ 0         │ Ongoing
  Airtel ISP   │ 99.5% uptime       │ 99.1% 🟡         │ 2 outages │ Ongoing

  AIRTEL ISP NOTE:
    2 outages in Q3 (Mar 8: 22 min, Feb 12: 14 min) — both during off-peak
    SLA penalty clause: credit of 1 day per 30-min outage block
    Credit claimed for Mar 8 outage ✅ (received bill credit Apr invoice)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/partners/` | Partner and integration list |
| 2 | `GET` | `/api/v1/coaching/{id}/partners/{pid}/status/` | Partner integration health status |
| 3 | `GET` | `/api/v1/coaching/{id}/partners/sla-report/` | SLA compliance report |
| 4 | `POST` | `/api/v1/coaching/{id}/partners/incident/` | Report a partner integration issue |
| 5 | `GET` | `/api/v1/coaching/{id}/partners/architecture/` | Integration architecture diagram |

---

## 5. Business Rules

- EduForge is TCC's most critical technology dependency; all student records, financial transactions, academic data, and portal access depend on EduForge being operational; TCC's business continuity plan must account for extended EduForge downtime (beyond 4 hours); the plan includes: (a) manual attendance registers; (b) offline fee receipt books; (c) paper-based doubt collection; these fallbacks must be tested annually to ensure staff know how to operate without the system; a staff team that has never used the manual fallback will be confused during a real outage
- Partner contracts above ₹2 lakh annual value are reviewed by the Director before renewal; the review includes: performance (SLA adherence), pricing (benchmark against alternatives), dependency risk (can TCC switch if needed?), and data handling (DPDPA compliance); EduForge at ₹3.6 lakh annual value is reviewed annually; the switching cost for EduForge (data migration, staff retraining, integration rebuild) is high — TCC's dependency on EduForge is a concentration risk that the Director acknowledges and manages by ensuring contract terms protect TCC's data portability rights
- All API integrations use HTTPS and API key/OAuth authentication; API keys are stored in EduForge's secrets manager, not hardcoded in application files; the IT coordinator rotates API keys every 6 months or immediately if a key is compromised; API access is logged; a Razorpay API key used for an unauthorised transaction would appear in the access log; the IT coordinator reviews integration access logs monthly for anomalies; a payment gateway API call for an amount outside normal range (e.g., ₹10 lakh in a single transaction) triggers an alert
- Airtel ISP SLA credit claims require documentation: the outage start time, duration, and end time (from TCC's network monitoring log) are submitted to Airtel's support team; Airtel verifies and issues a credit in the following month's invoice; TCC's IT coordinator maintains a network uptime log (from the firewall or monitoring tool) to support any future claims; without this log, TCC has no evidence for the credit claim even if the outage clearly happened; the monitoring infrastructure (not just the ISP SLA) is the compliance asset
- Meta Business API's WhatsApp messaging for non-contacts requires pre-registered message templates (L-04); the template submission, approval (2–3 days), and management process must be planned in advance; a marketing campaign that depends on a new WhatsApp template (e.g., for the UPSC batch launch) must initiate the approval process 5 business days before the campaign launch; an unapproved template sent via API is automatically rejected by Meta, and repeated violations risk TCC's Business API access being suspended; suspension would prevent all WhatsApp broadcasts — a significant communication gap

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division P*
