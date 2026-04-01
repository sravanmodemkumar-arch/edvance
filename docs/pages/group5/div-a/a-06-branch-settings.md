# A-06 — Branch Settings & Configuration

> **URL:** `/coaching/admin/settings/`
> **File:** `a-06-branch-settings.md`
> **Priority:** P2
> **Roles:** Director/Owner (K7) · Branch Manager (K6)

---

## 1. Settings Overview

```
BRANCH SETTINGS — TCC MAIN (HIMAYATNAGAR)
Managed by: Ms. Priya Sharma (Branch Manager)

SETTINGS CATEGORIES:
  ┌───────────────────────────────────┬──────────────────────────────────────────┐
  │ ⚙️  General                       │ Branch info, timings, contact details     │
  │ 📅  Batch Configuration           │ Batch types, capacities, schedules        │
  │ 💰  Fee Configuration             │ Course fees, installment rules, refund    │
  │ 🔔  Notifications                 │ SMS/WhatsApp/app alerts — what triggers   │
  │ 📋  Attendance Rules              │ Cutoff %, late-mark window, POCSO alerts  │
  │ 🔐  Access Control                │ Staff roles, permissions per role         │
  │ 🖨️  Branding                      │ Logo, colors, certificate template        │
  └───────────────────────────────────┴──────────────────────────────────────────┘
```

---

## 2. General & Batch Configuration

```
GENERAL SETTINGS:

  Branch Name:        Toppers Coaching Centre — Main
  Address:            Plot 42, Road 7, Himayatnagar, Hyderabad — 500029
  Contact Number:     040-2342-XXXX
  WhatsApp (admin):   +91-98490-XXXXX
  Working Days:       Mon – Sat  (Sunday: tests/special classes only)
  Morning batch:      6:00 AM – 9:00 AM
  Evening batch:      5:00 PM – 8:00 PM
  Office hours:       9:00 AM – 7:00 PM
  Holidays (2026):    [Manage Holidays →]  (14 holidays configured)

BATCH CONFIGURATION:

  Course         │ Capacity │ Min Enrol │ Fee (Full) │ Installments │ Duration
  ───────────────┼──────────┼───────────┼────────────┼──────────────┼──────────
  SSC CGL        │   250    │   20      │  ₹18,000   │ 2 (50/50)   │ 10 months
  SSC CHSL       │   200    │   20      │  ₹15,000   │ 2 (50/50)   │ 8 months
  RRB NTPC       │   200    │   20      │  ₹16,000   │ 2 (50/50)   │ 9 months
  Banking        │   220    │   20      │  ₹14,000   │ 2 (50/50)   │ 8 months
  Foundation 9-10│   150    │   15      │  ₹12,000   │ 3 (40/30/30)│ 12 months
  Dropper (JEE)  │    80    │   10      │  ₹65,000   │ 3 equal      │ 12 months
  Crash Course   │    60    │   10      │  ₹6,000    │ 1 (full)    │ 6 weeks
  Online Live    │  (unlim) │    5      │  ₹10,000   │ 2 (50/50)   │ varies

  [+ Add Course Type]   [Edit]  (Director approval required for fee changes)
```

---

## 3. Notification & Attendance Rules

```
NOTIFICATION RULES:

  Trigger                          │ Channel     │ To Whom          │ On/Off
  ─────────────────────────────────┼─────────────┼──────────────────┼────────
  Student absent (minor)           │ WhatsApp    │ Parent           │ ✅ ON
  Student absent (adult, 3rd time) │ SMS         │ Student          │ ✅ ON
  Fee due (7 days before)          │ WhatsApp+SMS│ Student + Parent │ ✅ ON
  Fee overdue (1 day)              │ WhatsApp    │ Student          │ ✅ ON
  Fee overdue (15 days)            │ SMS + Call  │ Student + Parent │ ✅ ON
  New test result published        │ App push    │ Student          │ ✅ ON
  Batch schedule change            │ WhatsApp    │ Student + Parent │ ✅ ON
  BGV overdue (staff)              │ Email       │ Branch Manager   │ ✅ ON
  Dropout risk flag                │ App         │ Counsellor       │ ✅ ON

ATTENDANCE RULES:

  Attendance cutoff (warning):     75%
  Attendance cutoff (action):      60%  → parent alert + counsellor flag
  Late-mark window:                15 minutes after class start
  Foundation batch (minor):        Absent = parent WhatsApp within 30 mins
  Monthly report card:             Auto-generated on 1st of each month
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/settings/` | All branch settings |
| 2 | `PATCH` | `/api/v1/coaching/{id}/settings/general/` | Update general settings |
| 3 | `PATCH` | `/api/v1/coaching/{id}/settings/batches/` | Update batch configuration |
| 4 | `PATCH` | `/api/v1/coaching/{id}/settings/notifications/` | Update notification rules |
| 5 | `PATCH` | `/api/v1/coaching/{id}/settings/attendance/` | Update attendance rules |
| 6 | `GET` | `/api/v1/coaching/{id}/settings/audit-log/` | Settings change history |

---

## 5. Business Rules

- Fee changes require Director (K7) approval even if initiated by a Branch Manager; this prevents branch-level fee discounting that erodes institute-wide pricing integrity; a Branch Manager who promises a student a lower fee to prevent dropout creates a precedent that other students will demand; all fee exceptions must go through the scholarship/waiver workflow in Division G, not through settings modification
- Notification rules for minor students (Foundation batch, hostel students under 18) must include parent WhatsApp alerts for every absence — this is both a POCSO duty-of-care requirement and a customer service standard; parents who pay ₹12,000/year for Foundation coaching expect to know when their child doesn't attend; disabling parent absence alerts for minor batches is not permitted even by the Director
- Batch capacity limits are enforced as hard caps; once a batch reaches capacity, the enrollment page shows "Batch Full — join waitlist"; the Branch Manager can manually override for up to 5% above capacity (e.g., 263 for a 250-capacity batch) with a documented reason; exceeding 110% capacity requires Director approval and must be accompanied by an infrastructure plan (additional room, split batch)
- Settings changes are audit-logged with actor, timestamp, old value, and new value; this is essential for dispute resolution — if a student claims they were charged more than the agreed fee, the settings audit log can show exactly when the fee was last changed and by whom; it also protects Branch Managers from being blamed for changes made by others
- The branding section controls the logo and color scheme visible on student-facing pages, certificates, and PDFs; franchise branches can only change branding within TCC's approved template (color palette, font, placement); they cannot use a different logo or remove TCC branding; this is enforced at the EduForge platform level — uploaded logos are validated against TCC's brand guidelines before being applied

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division A*
