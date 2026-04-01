# A-03 — Conducting Body Directory

> **URL:** `/exam/bodies/`
> **File:** `a-03-conducting-bodies.md`
> **Priority:** P1
> **Data:** `conducting_body` table — fully dynamic; every body that has at least one active exam appears here

---

## 1. Conducting Body Directory

```
CONDUCTING BODY DIRECTORY — EduForge
All exam-conducting organisations | 84 bodies · 198 exams

  SEARCH: [🔍 Search organisation name...    ]

  BROWSE BY LEVEL:
  ┌────────────────────────────────────────────────────────────────────┐
  │  NATIONAL / CENTRAL (12 bodies)                                    │
  │  SSC · UPSC · IBPS · SBI · RBI · RRB · NTA · CBSE · DRDO ·      │
  │  ISRO · ONGC · LIC · NABARD · NIACL · HAL · NTPC · Coal India…   │
  ├────────────────────────────────────────────────────────────────────┤
  │  ANDHRA PRADESH (18 bodies)                                        │
  │  APPSC · SLPRB (AP Police) · DSE AP (DSC/TRT) · AP GENCO ·       │
  │  AP TRANSCO · Revenue Dept AP · AP Revenue (VRO/VRA) ·           │
  │  Andhra University (APSET) · JNTU Kakinada · VSKP Port Trust…    │
  ├────────────────────────────────────────────────────────────────────┤
  │  TELANGANA (16 bodies)                                             │
  │  TSPSC · TSLPRB (TS Police) · DSE Telangana (TSTET) ·            │
  │  OU (TSSET/PGECET) · HMRL · TSRTC · TSSPDCL · TSGENCO ·         │
  │  Revenue Dept TS · GHMC · TSNPDCL · TSTRANSCO…                  │
  ├────────────────────────────────────────────────────────────────────┤
  │  OTHER STATES (38 bodies)                                          │
  │  KPSC · TNPSC · MPSC · RPSC · UPPSC · BPSC · WBPSC ·            │
  │  UKPSC · HPSC · JPSC · Karnataka Police · Delhi Police…           │
  └────────────────────────────────────────────────────────────────────┘
```

---

## 2. Conducting Body Card (Dynamic)

```
CONDUCTING BODY DETAIL — APPSC
[Rendered from conducting_body record — same template for all bodies]

  ┌──────────────────────────────────────────────────────────────────────┐
  │  [APPSC Logo]  ANDHRA PRADESH PUBLIC SERVICE COMMISSION            │
  │  Short: APPSC | Level: State | State: Andhra Pradesh               │
  │  Website: psc.ap.gov.in | Notification URL: psc.ap.gov.in/updates  │
  │  EduForge monitoring: ✅ Live (last checked: 31 Mar 2026, 6:00 AM) │
  ├──────────────────────────────────────────────────────────────────────┤
  │  EXAMS BY THIS BODY (8 active):                                     │
  │    APPSC Group 1 2024  — Mains in progress                          │
  │    APPSC Group 2 2025  — CBT: Aug 2026 (tentative)                 │
  │    APPSC Group 3 2025  — Results expected Jun 2026                  │
  │    APPSC Group 4 2025  — Application closed                         │
  │    APPSC AEE 2025      — Notification released Mar 2026 🔴          │
  │    APPSC Lecturers 2025— Results declared ✅                        │
  │    APPSC DAO 2025      — CBT scheduled May 2026                     │
  │    APPSC APSRTC 2026   — Notification expected Q3 2026              │
  ├──────────────────────────────────────────────────────────────────────┤
  │  TOTAL ASPIRANTS (APPSC): 6,24,000                                  │
  │  🔔 [Subscribe to all APPSC notifications]                           │
  └──────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────────┐
  │  [TSLPRB Logo]  TELANGANA STATE LEVEL POLICE RECRUITMENT BOARD      │
  │  Short: TSLPRB | Level: State | State: Telangana                   │
  │  Website: tslprb.telangana.gov.in                                   │
  │  EduForge monitoring: ✅ Live                                        │
  ├──────────────────────────────────────────────────────────────────────┤
  │  EXAMS BY THIS BODY (4 active):                                     │
  │    TS Police SI (Civil) 2025 — Results declared ✅                  │
  │    TS Police Constable 2025  — Application open ⏰ (till Apr 15)   │
  │    TS Police SI (AR) 2026    — Notification expected May 2026       │
  │    TSSP Constable 2026       — Notification expected Jun 2026       │
  └──────────────────────────────────────────────────────────────────────┘
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/exam/bodies/?state=AP` | All conducting bodies, filterable by state |
| 2 | `GET` | `/api/v1/exam/bodies/{slug}/` | Conducting body detail + all its exams |
| 3 | `GET` | `/api/v1/exam/bodies/{slug}/exams/` | Paginated exams for this body |
| 4 | `POST` | `/api/v1/exam/bodies/{slug}/subscribe/` | Subscribe to all notifications from this body |

---

## 5. Business Rules

- A conducting body record is the master reference for all exams under that organisation; when APPSC is added as a conducting body once, all future APPSC exams simply reference `conducting_body_id = APPSC`; the body's official notification URL is the source that the notification engine (C-04) monitors; if APPSC changes its notification URL from `psc.ap.gov.in/news` to `recruitment.apsc.gov.in`, updating the body record's `notification_url` instantly re-points the monitoring for all 8+ APPSC exams without touching individual exam records
- The "Subscribe to all notifications from APPSC" feature is high-value for aspirants who prepare for multiple APPSC exams simultaneously; instead of subscribing exam-by-exam, one subscription covers every future notification from APPSC — new exam announcements, result declarations, schedule changes, admit card releases; this is implemented as `notification_subscription WHERE conducting_body_id = APPSC AND user_id = X`; individual exam subscriptions and body-level subscriptions are merged to avoid duplicate alerts
- Conducting body monitoring status (last checked timestamp) is surfaced to aspirants to communicate EduForge's data freshness commitment; an aspirant who sees "last checked 6:00 AM today" trusts that EduForge has checked the official source today; a status of "last checked 3 days ago" raises a concern — the monitoring may have failed; the content team must investigate and fix any monitoring failure within 24 hours; aspirants who discover a notification on the official website before EduForge alerts them lose trust in the platform's core value proposition
- New conducting bodies are added by the content team admin (H-02) as needed; there is no approval workflow for adding a body — the content team has full authority to add any legitimate exam-conducting organisation; adding a body requires: official name, abbreviation, state (or null for national), official website URL, notification source URL, and logo; a body with `active = false` still shows its historical exams but is excluded from monitoring and new exam creation; this handles dissolved or merged organisations without data loss

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division A*
