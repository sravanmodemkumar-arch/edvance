# N-10 — Complaint & Grievance (Parent View)

> **URL:** `/parent/grievance/`
> **File:** `n-10-grievance.md`
> **Template:** `parent_portal.html`
> **Priority:** P1
> **Roles:** Parent/Guardian (S1-P)

---

## 1. Purpose

A parent who has a complaint or concern about their child's education, treatment, or safety can raise it formally through this module. The grievance system provides:
- A documented record of every complaint (protecting both parent and school)
- Clear SLAs and escalation paths
- Resolution tracking (parent can see status)
- NCPCR/consumer court evidence trail if needed

Parallel to J-05 (Student Grievance — school-side view), N-10 is the parent-facing submission and tracking interface.

---

## 2. Grievance Submission

```
RAISE A COMPLAINT — Parent Portal

Complainant: Mrs. Sunita Rao
Child: Rahul Rao (Class X-A)
Date: 27 March 2026

CATEGORY (select one):
  ○ Academic (marks, assessment, teaching quality)
  ● Teacher behaviour / classroom conduct
  ○ Bullying / harassment (peer) → [If involving bullying, special welfare path]
  ○ Fee / financial dispute
  ○ Infrastructure / safety
  ○ Transport issue
  ○ POCSO / child safety → [Immediately escalated to Principal; CHILDLINE 1098 info shown]
  ○ Other

Subject: "Concern about class atmosphere — teacher shouting"

Description (max 800 characters):
  "During Rahul's account, the Chemistry teacher Mr. [X] raises his voice very loudly
   at students who make mistakes. Rahul came home upset on 24 March saying the teacher
   shouted at him in front of the class for getting a question wrong. I understand firm
   teaching, but this affected Rahul's confidence. Please look into this.
   I am not looking to punish the teacher — I would like this to be addressed
   constructively."

Attached evidence (optional): None

SLA: Category "Teacher behaviour" — Resolution within 7 school days
Escalation if unresolved: VP → Principal → CBSE Grievance Cell

[Submit Grievance]  [Save as draft]
```

---

## 3. Grievance Status Tracking

```
GRIEVANCE STATUS — Rahul Rao (2025–26)

  GRV-2026-0041   Teacher behaviour concern    27 Mar 2026  ⏳ Under review
  GRV-2025-0018   Bus delay repeated            Oct 2025    ✅ Resolved (8 Nov 2025)

GRIEVANCE DETAIL — GRV-2026-0041:
  Filed: 27 Mar 2026  |  Category: Teacher behaviour
  Assigned to: VP (Ms. Meena Rao assumed it — Principal)
  SLA: 7 school days (due: 5 April 2026)
  Status: Under review — VP spoke with Class Teacher on 28 Mar

  TIMELINE:
    27 Mar — Grievance submitted (parent)
    27 Mar — Notification sent to HR Officer + VP (auto)
    28 Mar — VP acknowledged; assigned to herself for direct handling
    28 Mar — VP spoke with relevant teacher (classroom observation scheduled)
    [Resolution update pending]

EXPECTED RESOLUTION: By 5 April 2026
[If not resolved by 5 April, escalate to Principal] ← auto-trigger

PREVIOUS RESOLVED:
  GRV-2025-0018 (Bus delay):
    Filed: 2 Oct 2025  |  Resolved: 8 Nov 2025
    Resolution: "Route 3 schedule adjusted; driver briefed on time management.
                 3 consecutive on-time weeks confirmed. Issue closed."
    [Parent rating: ⭐⭐⭐⭐ (4/5) — "Took time but resolved properly"]
```

---

## 4. Anonymous Reporting

```
ANONYMOUS REPORT (for sensitive concerns)

For concerns where the parent wishes to remain anonymous:
  ● Child safety (suspected abuse or neglect — by anyone)
  ● POCSO concern (suspected inappropriate behaviour by staff or peer)
  ● Staff misconduct (serious)
  ● Ragging or bullying (if naming the aggressor)

[Submit anonymously →]

Note: Anonymous reports cannot be replied to; the school investigates and takes
  action without disclosure of the complainant's identity.
  For POCSO concerns, CHILDLINE 1098 is also available (national helpline).
  Anonymous reports are processed under POCSO/CBSE guidelines.
```

---

## 5. Grievance Rights Information

```
PARENT RIGHTS — Grievance Information

Your complaint rights as a parent:
  ● You have the right to raise a formal complaint with the school
  ● The school must respond within the specified SLA
  ● If unresolved at school level, you may escalate to:
      - CBSE Grievance Cell (cbse.gov.in/grievance)
      - National Commission for Protection of Child Rights (NCPCR.gov.in)
      - State Commission for Protection of Child Rights (TS-SCPCR)
      - Consumer Forum (for fee disputes — Consumer Protection Act 2019)
  ● For child safety concerns: CHILDLINE 1098 (24-hour helpline)

EduForge stores your grievance record for 5 years as per consumer protection
and DPDPA requirements.
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/grievance/` | Submit grievance |
| 2 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/grievance/` | List all grievances |
| 3 | `GET` | `/api/v1/parent/{parent_id}/child/{student_id}/grievance/{grv_id}/` | Grievance status and timeline |
| 4 | `POST` | `/api/v1/parent/{parent_id}/grievance/anonymous/` | Submit anonymous report |
| 5 | `POST` | `/api/v1/parent/{parent_id}/child/{student_id}/grievance/{grv_id}/rate/` | Rate resolution (after close) |

---

## 7. Business Rules

- Grievances submitted by parents are visible to the school side in J-05; the parent's name and contact are known to the school (unless anonymous submission was chosen); the school must not use the grievance submission against the parent or child — any retaliatory action is a serious governance failure and grounds for escalation to CBSE
- POCSO-related reports (anonymous or named) from parents trigger an immediate P0 alert to the Principal and POCSO Designated Officer (J-02); the school must follow up within 24 hours regardless of whether the concern turns out to be founded
- SLA timers start from submission, not from when the school first reads it; the school must check the grievance queue regularly (Compliance Officer / VP responsibility in J-05); an unread grievance that breaches SLA is still an SLA breach
- Anonymous reports are de-identified — EduForge stores the parent's identity server-side for audit purposes but displays it as "Anonymous" to school staff; the compliance team cannot see anonymous reporter identity unless there is a legal process (court order); this ensures genuine anonymity at the operational level
- Resolution confirmation is sent to the parent; the parent can rate the resolution (1–5 stars + comment); this rating feeds into the school's internal service quality metrics; the rating is not publicly visible (it is a management tool, not a public review)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division N*
