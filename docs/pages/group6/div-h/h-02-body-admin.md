# H-02 — Conducting Body Management

> **URL:** `/admin/exam/bodies/`
> **File:** `h-02-body-admin.md`
> **Priority:** P1
> **Data:** `conducting_body` table + `notification_source` — CRUD for bodies + monitoring source setup

---

## 1. Body Admin

```
CONDUCTING BODY MANAGEMENT — Admin
84 active bodies | 4 inactive

  [+ Add New Body]

  ┌──────────────────────────────────────────────────────────────────────────────┐
  │  Name              │ Abbr  │ Level    │ State │ Exams│ Monitor │ Actions     │
  ├────────────────────┼───────┼──────────┼───────┼──────┼─────────┼─────────────┤
  │  APPSC              │ APPSC │ State    │ AP    │   8  │ ✅ Live │ [Edit][Del] │
  │  TSPSC              │ TSPSC │ State    │ TS    │   6  │ ✅ Live │ [Edit][Del] │
  │  SSC                │ SSC   │ National │ —     │  12  │ ✅ Live │ [Edit][Del] │
  │  SLPRB-AP           │ SLPRB │ State    │ AP    │   4  │ ✅ Live │ [Edit][Del] │
  │  HMRL               │ HMRL  │ Municipal│ TS    │   1  │ ❌ None │ [Edit][Add] │
  └──────────────────────────────────────────────────────────────────────────────┘

  CREATE / EDIT BODY:
    Name:          [ Andhra Pradesh Public Service Commission  ]
    Abbreviation:  [ APPSC ]
    Level:         [ State ▼ ]
    State:         [ AP ▼ ]  (null for national bodies)
    Website:       [ psc.ap.gov.in ]
    Logo:          [📁 Upload]

    MONITORING SOURCES (C-04):
    [+ Add Source]
    Source 1: URL: [ psc.ap.gov.in/Updates ]
              Method: [ dom_selector ▼ ]  Selector: [ table.news tr ]
              Frequency: [ Every 60 min ▼ ]  Status: ✅ Active
```

---

## 2. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/admin/exam/bodies/` | All conducting bodies |
| 2 | `POST` | `/api/v1/admin/exam/bodies/` | Create new body |
| 3 | `PUT` | `/api/v1/admin/exam/bodies/{id}/` | Update body |
| 4 | `POST` | `/api/v1/admin/exam/bodies/{id}/sources/` | Add monitoring source |

---

## 5. Business Rules

- Adding a new conducting body is the first step in onboarding a new exam domain; the body must be a legitimate exam-conducting organisation with an official website; adding "Coaching Centre XYZ" as a conducting body is not valid — only government departments, PSUs, statutory bodies, and officially recognised exam-conducting organisations are added; the content team verifies the body's authenticity before creation
- Every active conducting body must have at least one monitoring source (C-04); a body without monitoring relies entirely on manual notification detection, which is slower and less reliable; when HMRL is added without monitoring (status: ❌ None), the admin must add at least one source URL within 48 hours; the system shows a warning badge on the admin dashboard for bodies without active monitoring
- Body deactivation (used for dissolved bodies — e.g., if TSPSC were renamed to TGPSC, the old TSPSC record is deactivated and a new TGPSC record is created with exams migrated) preserves all historical data under the old body; exams already published under "TSPSC" retain their body linkage for historical accuracy; new exams use the new "TGPSC" body record
- Logo upload accepts PNG/SVG only; logos are displayed at 48×48px in catalogue cards and 96×96px on body detail pages; a blurry or stretched logo degrades the platform's visual quality; if an official high-resolution logo is not available, the content team uses the body's name in text (abbreviation) as a fallback instead of a low-quality image

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division H*
