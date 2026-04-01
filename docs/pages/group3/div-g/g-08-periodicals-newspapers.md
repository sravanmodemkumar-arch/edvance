# G-08 — Periodicals & Newspapers

> **URL:** `/school/library/periodicals/`
> **File:** `g-08-periodicals-newspapers.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Librarian (S3) — manage subscriptions and receipt · Library Assistant (S2) — mark received · Academic Coordinator (S4) — approve new subscriptions

---

## 1. Purpose

Tracks magazine, journal, and newspaper subscriptions. Periodicals are handled differently from books:
- They are not issued outside the library (in most schools)
- They arrive on a recurring schedule (daily/weekly/monthly)
- Missing issues need to be tracked and claimed from the vendor
- Old issues need systematic archival/disposal (back volumes)
- Subscription renewal is annual and must be budgeted

Common Indian school library periodicals:
- **Newspapers:** The Hindu, Times of India, Deccan Chronicle (English) + regional language daily
- **Magazines:** Science Reporter, Frontline, Digit, Competitive Success Review, Pratiyogita Darpan, National Geographic, Reader's Digest India
- **Academic journals:** Physical Review (for senior secondary physics); rarely, but some progressive schools subscribe
- **NCERT Journals:** School Science, Indian Educational Review (free distribution from NCERT)

---

## 2. Page Layout

### 2.1 Header
```
Periodicals & Newspapers                             [+ Add Subscription]
Academic Year: [2026–27 ▼]

Active Subscriptions: 24  ·  Annual cost: ₹28,400
Renewal due this month: 3  ·  Issues received today: 4
Missing issues (last 30 days): 2
```

### 2.2 Subscription List
```
Title                Frequency  Language  Copies  Annual Cost  Renewal     Issues Rec'd  Status
The Hindu            Daily       English   2       ₹4,380       Apr 2027    Automated     ✅ Current
Science Reporter     Monthly     English   2       ₹840         Oct 2026    ⚠️ Due soon   ✅ Current
Deccan Chronicle     Daily       English   1       ₹2,190       Apr 2027    Automated     ✅ Current
Eenadu              Daily       Telugu    2       ₹2,920       Apr 2027    Automated     ✅ Current
National Geographic  Monthly     English   1       ₹1,800       Dec 2026    Upcoming      ✅ Current
Frontline           Fortnightly  English   1       ₹1,200       Jun 2026    ⚠️ Due soon   ✅ Current
Digit               Monthly      English   1       ₹720         Mar 2027    Upcoming      ✅ Current
```

---

## 3. Add Subscription

```
[+ Add Subscription]

Title: [Science Reporter          ]
Publisher: [National Institute of Science Communication (CSIR)]
ISSN: [0036-8512]
Frequency: [Monthly ▼]  (Daily / Weekly / Fortnightly / Monthly / Quarterly / Annual)
Language: [English ▼]
Category: [Science ▼]  (Science / Current Affairs / Literature / Sports / Arts / Technology)

Copies: [2]
Start Date: [April 2026]
Annual subscription cost: ₹420 × 2 copies = ₹840
Vendor/Agent: [Sai Magazines, Vijayawada]
Payment mode: ● Annual prepaid  ○ Quarterly  ○ Monthly

Budget check: ₹840 from Library Annual Budget ✅ (₹37,500 balance)

[Save Subscription]  [Raise Purchase Order (D-19)]
```

---

## 4. Issue Receipt Tracking

```
Mark Issues Received — 27 March 2026

Expected today:
  The Hindu (2 copies) — ✅ Received (8:10 AM)
  Eenadu (2 copies) — ✅ Received (8:12 AM)
  Deccan Chronicle (1 copy) — ❌ NOT received (missing)
  Science Reporter (monthly — not due today) — N/A

[Mark Received]  [Report Missing Issue]

Missing Issue — Deccan Chronicle (27 Mar 2026):
  Action: ☑ Alert vendor (auto-WhatsApp to vendor contact)
  Vendor complaint: DC/2026/047
  [Request replacement copy]
```

---

## 5. Back Volume Management

```
Back Volumes — Archival & Disposal

The Hindu — 2024-25 back volumes:
  Volumes: Jan 2024 – Mar 2025 (15 months)
  Condition: Good
  Action: ● Retain in back-issue rack  ○ Bind (annual binding)  ○ Dispose

Annual binding (recommended for reference magazines):
  Science Reporter 2024-25: 12 issues → bind as one volume
  Cost: ₹80/volume (local binder) → [Raise petty cash voucher D-20]

Newspapers: Retain for 1 month, then dispose (recycling)
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/library/periodicals/?year={y}` | Subscription list |
| 2 | `POST` | `/api/v1/school/{id}/library/periodicals/` | Add subscription |
| 3 | `POST` | `/api/v1/school/{id}/library/periodicals/{sub_id}/receive/` | Mark issue received |
| 4 | `POST` | `/api/v1/school/{id}/library/periodicals/{sub_id}/missing/` | Report missing issue |
| 5 | `GET` | `/api/v1/school/{id}/library/periodicals/renewal-due/?days={30}` | Upcoming renewals |

---

## 7. Business Rules

- Newspaper subscriptions are managed as auto-renewed (vendor delivers daily without individual PO); annual cost is budgeted under Library in D-17
- Magazines with academic value (Science Reporter, Frontline, National Geographic) are bound annually and retained as permanent collection; newspapers are disposed after 1 month
- Missing issues must be reported to the vendor within 48 hours; after 7 days, replacement is typically not possible — the loss is noted in the subscription record
- CBSE affiliation inspection checks: minimum 5 newspaper subscriptions (English + regional language) and 10 magazine subscriptions for senior secondary; this module's count is exported for the inspection report

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division G*
