# C-01 — Admission Enquiry & Lead Manager

> **URL:** `/school/admissions/enquiries/`
> **File:** `c-01-admission-enquiry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Admission Officer (S3) — full · Administrative Officer (S3) — read · Academic Coordinator (S4) — read · Principal (S6) — full

---

## 1. Purpose

Manages the complete admission enquiry funnel from first contact to application form submission. Indian private schools receive hundreds of enquiries (November–March) through multiple channels — walk-ins, phone calls, WhatsApp, website forms, and education fairs. Without a structured lead management system, enquiries fall through cracks, follow-ups are missed, and schools lose prospective admissions. This page gives the Admission Officer a CRM-style pipeline view: new enquiries → contacted → application form issued → form returned → shortlisted. It tracks the source of every enquiry (for marketing ROI analysis), the class applying for, and the follow-up status. It also captures sibling information early, so families with siblings already enrolled are fast-tracked (a common policy in Indian schools).

Admission season in Indian private CBSE schools typically:
- Opens: November (for the next academic year starting June)
- Peaks: January–February (when parents visit after annual days and school fairs)
- Closes: March (final selections before April fee deadline)
- Off-season: July–August (mid-year transfers, urgent cases)

---

## 2. Page Layout

### 2.1 Header
```
Admission Enquiries                           [+ New Enquiry]  [Import from Website]  [Export]
Academic Year: 2026–27 (Admissions Open)
Total Enquiries: 284  ·  In Pipeline: 186  ·  Forms Issued: 124  ·  Converted: 58
Open Seats: Class Nursery: 32 · LKG: 30 · UKG: 28 · I: 15 · XI-Science: 8 · XI-Commerce: 6
```

### 2.2 Kanban Pipeline View (Default)
```
[New Enquiry]     [Contacted]     [Form Issued]     [Form Returned]     [Shortlisted]     [Admitted]
    48 leads         52 leads         38 leads            28 leads           14 leads          6 leads
  ┌────────────┐   ┌────────────┐   ┌────────────┐     ┌────────────┐    ┌────────────┐
  │ Rani P.    │   │ Suresh K.  │   │ Anika S.   │     │ Mahesh R.  │    │ Priya V.   │
  │ Class I    │   │ Class III  │   │ Class XI-S │     │ Class LKG  │    │ Class I    │
  │ 📞 3h ago  │   │ ✅ Called  │   │ Form: 234  │     │ Form: 221  │    │ Selected ✅│
  └────────────┘   └────────────┘   └────────────┘     └────────────┘    └────────────┘
  [+ More...]      [+ More...]      [+ More...]         [+ More...]       [+ More...]
```

### 2.3 List View (toggle from Kanban)
Full table with sortable columns: Name, Class, Contact, Source, Enquiry Date, Stage, Last Follow-up, Assigned Officer.

---

## 3. Enquiry Stages

| Stage | Description | Next Action |
|---|---|---|
| **New Enquiry** | Enquiry received, not yet contacted | Call/WhatsApp within 24h |
| **Contacted** | Initial call/meeting done; school explained | Send school brochure + fee structure |
| **Form Issued** | Application form given (physical or digital link) | Follow up in 3 days if not returned |
| **Form Returned** | Completed application form received with documents | Acknowledge; schedule test/interview |
| **Shortlisted** | Admitted to test/interview shortlist | Send interview call letter |
| **Admitted** | Admission confirmed, fee paid | Enrollment in C-05 |
| **Waitlisted** | No seat currently; on waitlist | Notify if seat opens |
| **Not Interested** | Explicitly withdrawn | Archive |
| **Rejected** | Did not qualify test/interview | Archive |

---

## 4. New Enquiry Form

[+ New Enquiry] → drawer (520px):

| Field | Value |
|---|---|
| Student Name | Full name |
| Date of Birth | (to verify class eligibility) |
| Class Applying For | Nursery / LKG / UKG / I / II / ... / XII (stream: Science/Commerce/Arts) |
| Academic Year | 2026–27 |
| Parent / Guardian Name | Father's name (primary) + Mother's name |
| Mobile (Primary) | WhatsApp number |
| Mobile (Secondary) | Optional |
| Email | Optional |
| Current School | (if applying for Class II+) |
| Current Class | |
| Enquiry Source | Walk-in · Phone Call · Website Form · WhatsApp · Education Fair · Sibling · Friend Referral · Social Media · Hoarding/Newspaper |
| Sibling at School? | Yes → link to sibling student ID · No |
| Special Requirements | Any disability/special need to note |
| Enquiry Date | Today (auto) |
| Assigned Officer | Admission Officer (auto from login; can reassign) |
| Notes | Free text |

**Auto-actions on save:**
- Stage set to "New Enquiry"
- WhatsApp template sent (if WhatsApp integration enabled): "Dear [Parent], Thank you for your interest in [School Name]. Our Admission Officer will contact you shortly. — Principal, [School Name]"
- Follow-up reminder created (24h from now)

---

## 5. Enquiry Detail View

Clicking any lead card opens a 640px side drawer:

```
Suresh Kumar  |  Class III (2026–27)  |  Phone: +91-98765-43210
Current School: St. Mary's English School  ·  Currently in: Class II

──── Stage ────────────────────────────────────────────
[New] → [Contacted ✅] → [Form Issued] → [Form Returned] → [Shortlisted] → [Admitted]
                  Move to next stage: [Issue Form ▸]

──── Follow-up Log ────────────────────────────────────
26 Mar 2026, 10:30 AM  Admission Officer Meera
  "Called on 9876543210. Parent interested. Wants to know about scholarship.
   Explained school policy. Sending brochure via WhatsApp."

24 Mar 2026, 3:00 PM  Admission Officer Meera
  "Initial enquiry via walk-in. Father present. Tour of school given."

──── Add Follow-up ────────────────────────────────────
Channel: [Phone ▼]  Outcome: [Positive ▼]
Notes: [                                    ]
Reminder in: [3 days ▼]           [Save Follow-up]

──── Actions ───────────────────────────────────────────
[Issue Application Form]  [Mark Not Interested]  [Reject]  [Move to Waitlist]
```

---

## 6. Follow-up Reminders

The system auto-creates follow-up reminders:
- New enquiry not contacted within 24h → reminder to Admission Officer
- Form issued but not returned within 5 days → follow-up reminder
- Shortlisted but not yet confirmed after 3 days → reminder

Reminders appear in the Admission Officer's notification bell (A-26 Communications Hub).

---

## 7. Seat Availability Display

The header shows real-time seat availability computed from:
- Total seats in class (from A-08 Class Manager)
- RTE seats (C-07 RTE Admission Manager — reserved 25%)
- Already enrolled (from C-05 New Student Enrollment count)
- Already admitted but not yet enrolled (Admitted stage in pipeline)

| Class | Total Seats | RTE Reserved | General Seats | Admitted So Far | Available |
|---|---|---|---|---|---|
| Nursery | 40 | 10 | 30 | 8 | 22 |
| LKG | 40 | 10 | 30 | 12 | 18 |
| Class I | 40 | 10 | 30 | 28 | 2 |
| Class XI Science | 60 | 0 | 60 | 52 | 8 |

When seats = 0, the [Issue Application Form] button is replaced with [Add to Waitlist].

---

## 8. Import from Website

Schools using EduForge website module can import online enquiry form submissions:
- [Import from Website] → shows pending online enquiries not yet in CRM
- Each row: Name, Class, Mobile, Date — checkbox → [Import Selected]
- Duplicate detection: same mobile + class → merge confirmation

---

## 9. Enquiry Source Analytics (Quick Chart)

At bottom of page, a compact bar chart (Chart.js):
```
Enquiry Sources — 2026–27
Walk-in        ████████████  84 (29.6%)
Phone          ████████     56 (19.7%)
Sibling Ref    ███████      48 (16.9%)
Website Form   █████        38 (13.4%)
WhatsApp       ████         28 ( 9.9%)
Education Fair ██           16 ( 5.6%)
Social Media   █            12 ( 4.2%)
Other          ▌             2 ( 0.7%)
```

---

## 10. Export

[Export] → options:
- **Enquiry Register PDF** — CBSE inspection format (all enquiries with contact details, status)
- **Pipeline Summary Excel** — stage-wise count, source-wise count
- **Pending Follow-ups** — all leads where last follow-up > 3 days ago

---

## 11. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/admissions/enquiries/?year={year}&stage={stage}` | Enquiry list with filters |
| 2 | `POST` | `/api/v1/school/{id}/admissions/enquiries/` | Create new enquiry |
| 3 | `GET` | `/api/v1/school/{id}/admissions/enquiries/{enquiry_id}/` | Enquiry detail + follow-up log |
| 4 | `PATCH` | `/api/v1/school/{id}/admissions/enquiries/{enquiry_id}/stage/` | Move to next stage |
| 5 | `POST` | `/api/v1/school/{id}/admissions/enquiries/{enquiry_id}/followup/` | Add follow-up entry |
| 6 | `GET` | `/api/v1/school/{id}/admissions/seat-availability/?year={year}` | Real-time seat counts |
| 7 | `GET` | `/api/v1/school/{id}/admissions/enquiries/analytics/?year={year}` | Source analytics, funnel stats |
| 8 | `POST` | `/api/v1/school/{id}/admissions/enquiries/import-website/` | Import from website form |
| 9 | `GET` | `/api/v1/school/{id}/admissions/enquiries/export/?year={year}&format={pdf|excel}` | Export |

---

## 12. Business Rules

- An enquiry can only move forward through stages (no skipping to Admitted without passing Form Returned and Shortlisted) unless Principal overrides
- Sibling linkage at enquiry stage grants priority flag — many schools have a published sibling priority admission policy
- RTE applicants are NOT tracked here — they go through C-07 RTE Admission Manager (separate process with lottery and income verification)
- Enquiry data is retained for 3 years for reference (school inspection audit trail); after 3 years, personal data is anonymised per DPDPA 2023
- WhatsApp auto-messages are sent only if the school has WhatsApp integration configured in A-26

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division C*
