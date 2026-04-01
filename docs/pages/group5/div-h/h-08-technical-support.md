# H-08 — Technical Support & Issues

> **URL:** `/coaching/online/support/`
> **File:** `h-08-technical-support.md`
> **Priority:** P3
> **Roles:** Online Coordinator (K4) · Technical Support (K2) · Branch Manager (K6)

---

## 1. Support Ticket Queue

```
TECHNICAL SUPPORT — Open Tickets
As of 30 March 2026  |  Online Coordinator: Mr. Aditya Menon

  #     │ Student          │ Issue                          │ Raised      │ Priority │ Status
  ──────┼──────────────────┼────────────────────────────────┼─────────────┼──────────┼──────────────
  T-241 │ Kiran Naidu (2419)│ Video freezes after 15 min   │ 29 Mar 9 PM │ 🔴 High  │ ⏳ In Progress
  T-242 │ Sravya Rao (2418) │ Login OTP not received        │ 30 Mar 8 AM │ 🔴 High  │ ✅ Resolved
  T-243 │ Priya R. (2402)   │ PDF download not working      │ 29 Mar 4 PM │ 🟡 Med   │ ⏳ Pending
  T-244 │ Ravi S. (2403)    │ Test started but blank screen │ 28 Mar 6 PM │ 🔴 High  │ ✅ Resolved
  T-245 │ Akhil K. (2401)   │ Recording quality — 240p only │ 28 Mar 4 PM │ 🟡 Med   │ ⏳ Pending
  T-246 │ Anitha K. (2408)  │ Wrong batch shown in portal   │ 27 Mar 2 PM │ 🟡 Med   │ ✅ Resolved

  STATS (Last 7 Days):
    Tickets raised:    14
    Resolved:          10  (71.4%)
    Avg resolution:    4.2 hours
    SLA breaches (>8h for high, >24h for medium):  1 (T-241 — in progress 21 hrs)
```

---

## 2. Ticket Detail

```
TICKET T-241 — Kiran Naidu (TCC-2419)
Raised: 29 March 2026, 9:14 PM  |  Priority: 🔴 High  |  Status: ⏳ In Progress

  ISSUE DESCRIPTION:
    "Every time I watch a video for about 15 minutes, it freezes and I have to
     reload the page. This is happening with all videos, not just one. I'm
     using Chrome on Windows 11. My internet is Airtel 40 Mbps."

  SYSTEM DIAGNOSTICS (auto-run at ticket creation):
    Browser:           Chrome 124 ✅ (supported)
    OS:                Windows 11 ✅
    CDN node:          Hyderabad-2 ✅
    Student's video:   720p (1.2 GB file streaming)
    Bandwidth test:    Auto: 18.4 Mbps at time of issue (not 40 Mbps)
    CDN latency:       38 ms ✅
    Session error log: "HLS segment timeout — Hyd-2 node" (3 instances at 15 min)

  ROOT CAUSE HYPOTHESIS:
    CDN segment timeout at Hyd-2 node — likely peak traffic issue (9:14 PM)
    720p video streaming requires ~4 Mbps sustained; available was 18 Mbps but
    shared with household — likely drops during family usage hours

  RESOLUTION STEPS:
    [✓] Advised student to switch to 480p quality setting (lower bandwidth)
    [✓] Reported CDN Hyd-2 timeout issue to hosting team (ticket #HTS-8821)
    [ ] Follow-up with student to confirm 480p works — due 31 Mar

  ASSIGNED TO: Mr. Aditya Menon (Online Coordinator)
  Next update due: 31 March 2026, 10 AM
```

---

## 3. Common Issues & Self-Help

```
COMMON ISSUES — Self-Help Guide (Published on Student Portal)

  Issue                      │ Quick Fix                                │ If Unresolved
  ───────────────────────────┼──────────────────────────────────────────┼──────────────────
  OTP not received           │ Check spam folder; wait 2 min; retry    │ Call +91-40-XXXXXX
  Video buffering/freezing   │ Switch to 480p; clear cache; use Chrome │ Raise ticket
  Test not loading           │ Disable browser extensions; try incognito│ Raise ticket
  Can't see study material   │ Refresh; check if subscription expired   │ Raise ticket
  Wrong batch shown          │ Logout and login again                   │ Raise ticket
  Score not updated          │ Wait 5 min for auto-refresh              │ Raise ticket
  Can't download PDF         │ Downloads disabled — use view mode       │ Expected behavior
  Forgot password            │ Use "Forgot Password" link (OTP reset)   │ Contact support

  SUPPORT CHANNELS:
    WhatsApp: +91-9876543210 (9 AM – 9 PM, Mon–Sat)
    Email: support@tcc.in (response within 4 hours during working hours)
    In-app ticket: Available 24/7 (response by next morning for overnight)
    Phone: +91-40-XXXXXXXX (10 AM – 7 PM, Mon–Fri)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/online/support/tickets/` | All support tickets |
| 2 | `POST` | `/api/v1/coaching/{id}/online/support/tickets/` | Raise a new support ticket |
| 3 | `GET` | `/api/v1/coaching/{id}/online/support/tickets/{tid}/` | Ticket detail and log |
| 4 | `PATCH` | `/api/v1/coaching/{id}/online/support/tickets/{tid}/` | Update ticket status/notes |
| 5 | `GET` | `/api/v1/coaching/{id}/online/support/diagnostics/?student={sid}` | Auto-diagnostic for a student |
| 6 | `GET` | `/api/v1/coaching/{id}/online/support/stats/?days=7` | Support ticket stats |

---

## 5. Business Rules

- High-priority technical issues (video not playing, test blank screen, login failure) must be resolved within 8 hours; medium priority within 24 hours; an SLA breach (T-241 at 21 hours and counting) requires the Online Coordinator to escalate to the Branch Manager and update the student on progress; a student who cannot access the platform during their scheduled revision time loses preparation hours that cannot be recovered before their exam — the urgency is real, not bureaucratic
- Ticket auto-diagnostics (browser detection, CDN check, bandwidth test) reduce the information-gathering phase of support; when a student raises a ticket, the system captures their device profile and network data at that moment; this allows the coordinator to immediately triage whether the issue is device-specific, network-specific, or platform-wide; a platform-wide issue (CDN node down) affects many students simultaneously and triggers a status page update rather than individual ticket responses
- PDF downloads are intentionally disabled (students cannot download PDFs to their device); this is documented in the common issues guide as "expected behavior — use view mode"; a student who raises a ticket about PDF downloads "not working" receives this explanation and is shown how to use the PDF viewer within the platform; coordinators must be consistent — if one coordinator enables PDF downloads for one student as a "favour," it creates an unequal experience and a security gap
- Support tickets are linked to the student's enrollment record and are accessible by the Online Coordinator, the Batch Coordinator (read-only), and the Branch Manager; if a student has 5+ support tickets in a month, the Branch Manager is alerted — this may indicate a persistent technical issue on TCC's side (CDN, platform bug) or a student with equipment challenges who needs a device upgrade recommendation; TCC maintains a relationship with a local electronics retailer who offers EMI options to students in financial hardship
- DPDPA 2023 requires that system diagnostic data (student's IP address, browser fingerprint, device ID) collected during support is used only for resolving the support ticket; it cannot be retained beyond 90 days unless needed for a legal dispute; the Accounts team ensures the support ticket system's data retention policy is aligned with this requirement; EduForge's platform team performs an annual data retention audit across all modules

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division H*
