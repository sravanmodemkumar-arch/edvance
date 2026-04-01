# A-27 — Circular & Notice Manager

> **URL:** `/school/admin/circulars/`
> **File:** `a-27-circular-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Admin Officer (S3) — full · VP Academic (S5) — compose · VP Admin (S5) — compose · Principal (S6) — approve + send

---

## 1. Purpose

Manages all official school circulars and notices — their drafting, approval (where required), dispatch to parents/staff, and archival. Circulars are the formal communication mode in Indian schools: exam schedules, fee notices, holiday announcements, PTM invitations, uniform guidelines, disciplinary notices, CBSE/board communications. The Admin Officer is the primary operator; important circulars require Principal approval before dispatch.

**Indian school circular culture:** Indian schools (CBSE in particular) maintain a "Circular Register" as a required record book. This page is the digital equivalent. CBSE/state board inspectors check this register during visits. Every circular must be numbered, dated, and retained for at least 3 academic years.

---

## 2. Page Layout

### 2.1 Header
```
Circular & Notice Manager                   [+ New Circular]  [Circular Register] [Export]
Total This Year: 48 circulars (No. CIR/2025-26/001 to CIR/2025-26/048)
Filter: Category [All ▼]  Status [All ▼]  Month [All ▼]
```

---

## 3. Circular Register Table

| Circular No | Date | Subject | Category | Audience | Channels | Approval | Status | Actions |
|---|---|---|---|---|---|---|---|---|
| CIR/2025-26/048 | 26 Mar 2026 | Annual Exam Schedule — Class I to IX | Academic | Parents + Staff | WhatsApp · SMS | Principal ✅ | Sent | [View] [Resend] |
| CIR/2025-26/047 | 24 Mar 2026 | Fee Payment Reminder — March 2026 | Finance | Parents | WhatsApp · SMS | Not required | Sent | [View] |
| CIR/2025-26/046 | 22 Mar 2026 | Sports Day — 5 April 2026 | Events | Parents + Students | All channels | Principal ✅ | Sent | [View] |
| DRAFT-003 | — | Upcoming Summer Vacation Notice | Academic | Parents | TBD | Pending draft | Draft | [Continue] [Delete] |

---

## 4. Circular Numbering

Auto-generated: `CIR/[YYYY-YY]/[NNN]`
- Example: CIR/2025-26/048
- Increments automatically; cannot be manually changed
- Draft circulars get number assigned only on final approval + dispatch

---

## 5. Compose Circular

**[+ New Circular] drawer (680px):**

**Fields:**
- Subject: short title for register
- Category: Academic · Finance/Fee · Events · Holiday · Uniform/Dress Code · Health/Safety · Disciplinary · CBSE/Board Notice · Administrative · Emergency
- Full text: rich text editor
  - School letterhead auto-added at top (from institution profile)
  - Auto-add circular number + date at top right
- Attachments: PDF/image (optional)
- Audience: All Parents · All Staff · Specific Classes · Custom
- Channels: WhatsApp · SMS · In-app · Email
- Approval required: Yes (auto-required for Academic, Finance, Disciplinary) / No (Admin Officer can send directly for minor notices)
- [Save as Draft] · [Submit for Approval] · [Preview as PDF]

---

## 6. Approval Workflow for Circulars

When approval required:
- Draft created by Admin Officer / VP
- Submitted to Principal for review
- Principal approves → auto-dispatched at scheduled time
- Principal returns → Admin Officer revises + resubmits
- All approvals tracked in A-23 Approval Hub

---

## 7. Physical Register Compliance

**[Print Circular Register]** — generates a formatted PDF listing all circulars for the academic year in prescribed register format (circular number, date, subject, audience, dispatch date) — ready for CBSE inspection.

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/circulars/` | Circular register |
| 2 | `POST` | `/api/v1/school/{id}/circulars/` | Create circular draft |
| 3 | `GET` | `/api/v1/school/{id}/circulars/{id}/` | Circular detail |
| 4 | `POST` | `/api/v1/school/{id}/circulars/{id}/submit-for-approval/` | Submit for approval |
| 5 | `POST` | `/api/v1/school/{id}/circulars/{id}/dispatch/` | Dispatch after approval |
| 6 | `GET` | `/api/v1/school/{id}/circulars/{id}/pdf/` | Circular as formatted PDF |
| 7 | `GET` | `/api/v1/school/{id}/circulars/register/pdf/` | Full circular register PDF |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
