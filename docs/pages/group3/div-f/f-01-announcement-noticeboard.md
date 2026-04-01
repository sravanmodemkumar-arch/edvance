# F-01 — Announcement & Notice Board

> **URL:** `/school/announcements/`
> **File:** `f-01-announcement-noticeboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Communication Coordinator (S3) — create/edit · Class Teacher (S3) — class-specific announcements · Academic Coordinator (S4) — school-wide approve · Principal (S6) — publish official notices · All Staff — view · Parents — view own class/school-level notices via parent portal

---

## 1. Purpose

The central notice board for the school — the digital equivalent of the school's physical noticeboard. Every stakeholder (staff, parents, students) has a view of notices relevant to them. This is P0 because:
- **Daily operations** depend on announcements being visible to the right people at the right time (schedule changes, exam postponements, holiday declarations, PTM notifications)
- **Legal notices** (fee circulars with due dates, exam results, promotion/detention decisions) must be officially "published" here for timestamp record
- **Parent portal integration** — parents see school-level and class-level announcements via the parent app/portal; this is the primary way modern Indian schools communicate post-COVID

The notice board is the authoritative single source of truth for current school notices; F-02 manages the printed circular variants of the same notices.

---

## 2. Page Layout

### 2.1 Admin View (Communication Coordinator / Principal)
```
Announcement & Notice Board                          [+ New Announcement]  [View as Parent]
Academic Year: [2026–27 ▼]   Filter: [All ▼]  Status: [All ▼]

📌 PINNED — IMPORTANT
─────────────────────────────────────────────────────────────────────────────
  🔴 URGENT: Annual Exam Schedule — Class X                    Published 22 Mar 2026
      Audience: Parents of Class X  |  Expires: 15 Apr 2026  |  Views: 89/120 (74%)
      [Edit]  [Unpin]  [Resend to unread]

  🔴 Term 2 Fee Due Date: 31 March 2026                        Published 1 Mar 2026
      Audience: All Parents  |  Expires: 31 Mar 2026  |  Views: 342/380 (90%)
      [Edit]  [Unpin]

─────────────────────────────────────────────────────────────────────────────
📋 RECENT NOTICES
─────────────────────────────────────────────────────────────────────────────
  📅 PTM Schedule — Secondary Section (9 Mar 2026)             Published 25 Feb 2026
      Audience: Parents of Classes VI–XII  |  Views: 198/230
      [View]  [Edit]  [Resend]

  📚 Syllabus for Annual Exam — All Classes                     Published 20 Feb 2026
      Audience: All Parents  |  Views: 290/380
      [View]  [Edit]

  🏆 Sports Day Invitation (15 Feb 2026)                       Published 5 Feb 2026
      Audience: All  |  Expired  |  Archive
```

---

## 3. Create Announcement

```
[+ New Announcement] → drawer:

Title: [Annual Exam Schedule — Class X                           ]

Content (rich text):
  [Formatting toolbar: Bold / Italic / Bullet list / Numbered list / Table]
  ┌──────────────────────────────────────────────────────────────────────┐
  │ Dear Parents,                                                         │
  │                                                                       │
  │ The Annual Examination for Class X will be held as per the schedule  │
  │ below. Please ensure your ward is prepared.                           │
  │                                                                       │
  │ [Table: Subject | Date | Timing | Venue]                             │
  │ Mathematics    | 1 Apr 2026 | 9 AM – 12 PM | Exam Hall              │
  │ ...                                                                   │
  └──────────────────────────────────────────────────────────────────────┘

Attachments: [+ Add File] (PDF/image, max 5 MB per file, up to 3 files)
  Attached: exam_schedule_x.pdf (120 KB)

Category:
  ○ Academic  ● Examination  ○ Fee  ○ Holiday  ○ Event  ○ Emergency  ○ General

Audience:
  ○ All parents and staff
  ○ Selected classes: [✅ Class X-A  ✅ Class X-B  ✅ Class X-C]
  ○ Staff only
  ○ Specific role groups

Language: ● English  ○ Telugu  ○ Hindi  ○ Tamil  (multiple if school is bilingual)

Expiry date: [15 Apr 2026]  (notice auto-archives after this date)
Pin to top: ☑ Yes (urgent notice)
Priority: ● Normal  ○ Important  ○ Urgent (red banner)

Notification:
  ☑ Push notification via parent app (if installed)
  ☑ WhatsApp broadcast (via F-03)
  ☑ In-app notice board (visible on parent portal)
  ☐ SMS (reserve for truly urgent)

Schedule publish: ● Now  ○ Schedule for: [Date] [Time]

Approval required: ☑ Academic Coordinator (school-wide notices)

[Save Draft]  [Preview]  [Submit for Approval]  [Publish Now (if no approval)]
```

---

## 4. Parent Portal View

Parents see a curated view:

```
School Notices — Arjun Sharma (Class XI-A) — Parent View

📌 IMPORTANT
─────────────
  🔴 Annual Exam Schedule                          22 Mar 2026
  🔴 Term 2 Fee Due — 31 March                     1 Mar 2026

FOR CLASS XI-A
───────────────
  📅 PTM on 9 Mar — Time slot confirmed: 10:30 AM  25 Feb 2026  [View]
  📚 Chemistry syllabus for Annual Exam            20 Feb 2026  [View]  [Download]

SCHOOL-WIDE
────────────
  🎉 Annual Day — 22 Feb 2026 (Tomorrow!)          21 Feb 2026  [View]
  📋 Summer vacation dates announced               15 Feb 2026  [View]

[View all notices]
```

---

## 5. Read Tracking & Resend

```
Read Status — Annual Exam Schedule (Class X, 120 parents)

Read: 89 (74%)   Unread: 31 (26%)   Delivered: 115   Failed: 5

Unread Parents:
  Parent of: Ravi Kumar (X-A), Sita D. (X-B), Meena D. (X-B)...

[Resend to Unread — WhatsApp]   [SMS unread parents]
[Export unread list for follow-up]
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/announcements/?year={y}&class={class_id}` | Announcements list (filtered) |
| 2 | `POST` | `/api/v1/school/{id}/announcements/` | Create announcement |
| 3 | `GET` | `/api/v1/school/{id}/announcements/{ann_id}/` | Announcement detail |
| 4 | `PATCH` | `/api/v1/school/{id}/announcements/{ann_id}/` | Edit announcement |
| 5 | `POST` | `/api/v1/school/{id}/announcements/{ann_id}/publish/` | Publish (after approval) |
| 6 | `GET` | `/api/v1/school/{id}/announcements/{ann_id}/read-status/` | Read tracking report |
| 7 | `POST` | `/api/v1/school/{id}/announcements/{ann_id}/resend/` | Resend to unread |
| 8 | `GET` | `/api/v1/school/{id}/announcements/parent-view/?student_id={id}` | Parent-filtered view |

---

## 7. Business Rules

- School-wide announcements (audience = all parents) require Academic Coordinator or Principal approval before publishing; class-level announcements can be published by the Class Teacher directly
- Fee-related announcements must state the exact due date and fee amount — vague notices are rejected by the approval workflow
- Emergency announcements (category = Emergency) bypass approval and publish immediately — but are flagged in the audit log for post-event review
- Notices expire automatically on the set expiry date and move to archive — they are not deleted, for audit trail
- Parents can acknowledge a notice (tap "✅ Seen") via the parent portal; acknowledgement is tracked for PTM confirmations, signed circulars, etc.
- DPDPA: Notices containing student-specific data (exam marks, attendance) are sent individually, not as broadcast group messages

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
