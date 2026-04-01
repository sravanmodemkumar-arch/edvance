# H-13 — Maintenance & Complaints

> **URL:** `/school/hostel/maintenance/`
> **File:** `h-13-maintenance-complaints.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Warden (S3) — raise complaints · Chief Warden (S4) — approve and track · Administrative Officer (S3) — coordinate repairs · Principal (S6) — high-value repairs

---

## 1. Purpose

Tracks infrastructure maintenance complaints and repairs for hostel facilities — plumbing, electrical, structural, cleaning, appliances. Important for:
- Student safety (broken steps, faulty wiring)
- Living comfort (AC/fan failures during summer)
- Hygiene compliance (FSSAI for mess kitchen, bathroom maintenance)
- Budget tracking (maintenance costs per block)

---

## 2. Page Layout

### 2.1 Header
```
Maintenance & Complaints                             [+ Raise Complaint]
Date: 27 March 2026

Open complaints: 8  ·  Resolved this month: 22  ·  Avg resolution time: 2.3 days
Critical/safety: 0 open  ·  Routine: 8 open
```

### 2.2 Complaint Register
```
Ticket   Location          Issue                       Priority  Status    Assigned To
MNT-084  Block A, Room 102 Leaking tap (bathroom)      Normal   🟡 Open   Plumber
MNT-083  Block A, Corridor  Tubelight not working      Low      ✅ Done   Electrician
MNT-082  Block B, Room 205  AC not cooling              High    🟠 In prog AC technician
MNT-081  Mess kitchen        Exhaust fan broken         High    ✅ Done   Vendor
MNT-080  Block A Gate        Lock jammed               Safety  ✅ Done   Carpenter (same day)
```

---

## 3. Raise Complaint

```
[+ Raise Complaint]

Location: [Block A ▼] / [Floor: Ground ▼] / [Area: Room 102]
Category: ● Plumbing  ○ Electrical  ○ Civil/Structural  ○ AC/Fan  ○ Furniture  ○ Cleaning  ○ Other
Description: [Bathroom tap has been leaking since yesterday morning. Wasting water.]
Priority: ● Normal  ○ High  ○ Critical/Safety (immediate action required)
Raised by: [Mr. Suresh Kumar — Warden]
Photo: [Attach photo] (optional)

For critical/safety complaints:
  → Chief Warden notified immediately
  → Admin Officer called
  → Resolution target: 4 hours

Normal complaints: Target 3 working days

[Submit]
```

---

## 4. Resolution Workflow

```
Ticket MNT-084 — Block A Room 102 — Leaking Tap

Status: In Progress
Assigned to: Local plumber (vendor contact)
Expected resolution: 28 Mar 2026

Warden follow-up: 28 Mar 10 AM — Plumber visited; parts needed (new tap washer)
                  Actual resolution: 28 Mar 3 PM ✅

Cost: ₹150 (material + labour)
[Raise D-20 Petty Cash voucher: ₹150]  OR  [Raise D-19 vendor payment]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/maintenance/?status={status}` | Complaint register |
| 2 | `POST` | `/api/v1/school/{id}/hostel/maintenance/` | Raise complaint |
| 3 | `PATCH` | `/api/v1/school/{id}/hostel/maintenance/{ticket_id}/resolve/` | Mark resolved |
| 4 | `GET` | `/api/v1/school/{id}/hostel/maintenance/analytics/?month={m}&year={y}` | Maintenance cost analytics |

---

## 6. Business Rules

- Critical/Safety complaints (fire hazard, structural damage, broken external door lock) have a mandatory 4-hour resolution target; if not resolved, escalation to Principal
- All maintenance costs are tracked against block/area for budgeting; high-maintenance blocks are reported to the Principal for capital improvement planning
- Student-reported complaints (via hostel suggestion box or Warden) are accepted; anonymous complaints are logged and investigated without requiring student identity

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
