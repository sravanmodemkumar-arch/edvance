# M-04 — IT Systems & Technology

> **URL:** `/coaching/operations/it/`
> **File:** `m-04-it-systems.md`
> **Priority:** P2
> **Roles:** IT Coordinator (K3) · Branch Manager (K6) · Director (K7)

---

## 1. IT Infrastructure Overview

```
IT SYSTEMS STATUS — Toppers Coaching Centre
As of 31 March 2026 | System Monitor: Suman G. (IT Coordinator)

  ┌──────────────────────────────────────────────────────────────────────┐
  │  ALL SYSTEMS OPERATIONAL ✅                                          │
  ├─────────────────────────┬────────────────────┬────────────────────────┤
  │  EduForge Portal         │  LMS (Online Batches)│  Network              │
  │  Uptime: 99.6% (30d)    │  Uptime: 99.2% (30d) │  Primary: 100 Mbps   │
  │  Response: 180ms avg    │  Active sessions: 4  │  Backup: 40 Mbps     │
  │  Last downtime: Mar 12  │  Concurrent users: 356│ Failover: < 30s     │
  ├─────────────────────────┼────────────────────┼────────────────────────┤
  │  CCTV / Security        │  Biometric System  │  Server Room           │
  │  24 cameras online ✅   │  6 devices ✅      │  Temp: 22°C ✅        │
  │  Storage: 30-day NVR    │  Sync: 7:58 AM     │  UPS: 4-hr backup     │
  │  Last test: Jan 2026    │  Attendance live   │  Generator: standby   │
  └─────────────────────────┴────────────────────┴────────────────────────┘

  RECENT INCIDENTS:
    12 Mar 2026: Portal downtime 14 mins (DB connection timeout) — RCA done ✅
    8 Mar 2026:  Internet outage 22 mins (ISP fault) — failover activated ✅
    1 Mar 2026:  Biometric device #3 sync failed — reset resolved ✅
```

---

## 2. Software & Licensing

```
SOFTWARE INVENTORY — March 2026

  Platform / Software        │ Version │ Licence Type │ Licences │ Expiry     │ Cost/yr
  ───────────────────────────┼─────────┼──────────────┼──────────┼────────────┼────────
  EduForge SaaS (all portals)│ v4.2    │ SaaS (cloud) │   1 org  │ Renew Dec  │ ₹3.6 L
  Microsoft 365 (staff)      │ Current │ Business Std  │   28     │ Sep 2026   │ ₹0.84 L
  Zoom (online classes)      │ Current │ Pro (10 hosts)│   10     │ Apr 2026   │ ₹0.48 L
  Tally Prime (accounts)     │ 4.1     │ Perpetual     │    1     │ N/A        │ ₹0.12 L
  Adobe Acrobat (PDF)        │ Current │ Standard      │    2     │ Jun 2026   │ ₹0.06 L
  Antivirus (ESET)           │ Current │ Business      │   28     │ Oct 2026   │ ₹0.14 L
  WhatsApp Business API      │ —       │ Pay-per-use   │   —      │ Ongoing    │ Variable
  ───────────────────────────┴─────────┴──────────────┴──────────┴────────────┴────────
  TOTAL ANNUAL SOFTWARE COST: ₹5.24 L  (3.4% of revenue — within 4% IT budget)

  UPCOMING RENEWALS (next 60 days):
    Zoom Pro: Renew by Apr 30 (₹48,000/yr) — ✅ Renewal initiated
    Microsoft 365: Sep 2026 — plan ahead
```

---

## 3. Data Backup & Security

```
DATA BACKUP & SECURITY STATUS

  BACKUP SCHEDULE:
    EduForge data:      Continuous (cloud — managed by EduForge SaaS)
    Tally database:     Daily at 11 PM → encrypted to external HDD + cloud
    CCTV footage:       30-day rolling (auto-overwrite)
    Staff documents:    Weekly → SharePoint (Microsoft 365)

  LAST BACKUP VERIFICATION:
    EduForge restore test:   Jan 2026 (quarterly — next Apr 2026)
    Tally backup test:       Mar 28 2026 ✅

  CYBERSECURITY:
    Firewall:            Active (pfSense — IT coordinator managed)
    Antivirus:           All 28 machines — last scan: 30 Mar 2026 ✅
    Patching:            Monthly (2nd Sunday) — last: Mar 9 2026 ✅
    Admin access:        MFA enabled for all admin accounts ✅
    Student data:        Encrypted at rest (EduForge AES-256)
    Password policy:     Min 12 chars, 90-day rotation enforced

  DPDPA 2023 DATA SECURITY:
    Data localisation:  EduForge servers hosted in India (Mumbai region) ✅
    Access log:         All data access logged (90-day retention)
    Breach notification: SOP exists — Director notified within 72 hrs of discovery
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/operations/it/status/` | IT systems status overview |
| 2 | `GET` | `/api/v1/coaching/{id}/operations/it/incidents/` | IT incident log |
| 3 | `POST` | `/api/v1/coaching/{id}/operations/it/incidents/` | Report new IT incident |
| 4 | `GET` | `/api/v1/coaching/{id}/operations/it/software/` | Software and licence inventory |
| 5 | `GET` | `/api/v1/coaching/{id}/operations/it/backup/status/` | Backup verification status |
| 6 | `GET` | `/api/v1/coaching/{id}/operations/it/security/alerts/` | Cybersecurity alerts |

---

## 5. Business Rules

- System uptime of 99.6% (approximately 26 hours downtime per year) is acceptable for a coaching centre but any downtime during a live mock test or online class is unacceptable; the IT SOP defines a "critical hours" window (6 AM–10 PM) during which planned maintenance is prohibited; all system updates and patches are deployed during the maintenance window (2nd Sunday, 11 PM–4 AM); an unplanned outage during a mock test triggers an immediate incident response: pause the test, contact all affected students, reschedule or extend the test window, and post a public acknowledgement on the portal
- Software licence compliance is the IT coordinator's direct responsibility; using unlicensed software (pirated Windows, cracked Adobe tools) exposes TCC to copyright infringement liability and civil suits under the Copyright Act 1957; a licence audit is conducted annually; any machine running unlicensed software must be remediated within 7 days of discovery; the cost of legitimate licences (₹5.24 lakh/year) is significantly less than the legal exposure from non-compliance; the Director approves the annual IT budget including software licences as a non-negotiable line item
- Data backup is tested quarterly — not just scheduled; a backup that has never been tested is a false sense of security; the January 2026 EduForge restore test confirmed that a complete data restoration from backup takes 4 hours; this means TCC's recovery time objective (RTO) for the EduForge platform is 4–6 hours; the Director accepted this RTO as part of the IT risk management review; if the RTO is unacceptable (live exam context where 4 hours is too long), TCC would need to upgrade to a higher-tier SaaS plan with faster failover
- DPDPA 2023 requires that personal data of students (name, contact, financial information, performance data) is stored and processed in India; EduForge's cloud hosting in Mumbai satisfies the data localisation requirement; if EduForge were to move servers outside India without TCC's knowledge, TCC would be in violation of DPDPA even though TCC did not make the decision; the TCC-EduForge contract must explicitly require Indian data hosting and require advance notice of any change; TCC's legal obligation cannot be delegated to a vendor without explicit contractual safeguards
- The MFA (Multi-Factor Authentication) requirement for admin accounts protects TCC's most sensitive data (payroll, student records, financial data) from credential theft; a staff member whose phone is lost or stolen must report it immediately to the IT coordinator so the MFA device can be deregistered; the 90-day password rotation policy reduces the risk window for a compromised credential; staff who write passwords on sticky notes or share credentials are creating a security violation; the IT coordinator conducts a 15-minute security awareness session with all new staff at joining

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division M*
