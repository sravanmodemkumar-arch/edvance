# H-05 — Audit Log & Data Integrity

> **URL:** `/admin/exam/audit/`
> **File:** `h-05-audit-log.md`
> **Priority:** P1
> **Data:** `audit_log` — every admin action recorded; immutable log for compliance and debugging

---

## 1. Audit Log

```
AUDIT LOG — Exam Portal
All admin actions | Immutable | Retained: 24 months

  FILTER: User: [All ▼]  Action: [All ▼]  Entity: [All ▼]  Date: [Last 7 days ▼]

  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │  Timestamp          │ User        │ Action      │ Entity            │ Detail     │
  ├─────────────────────┼─────────────┼─────────────┼───────────────────┼────────────┤
  │  2 Apr 26, 10:14 AM │ Rajan K.    │ UPDATE      │ exam/ssc-cgl-2026│ notif_date │
  │                     │             │             │                   │ set Apr 2  │
  │  2 Apr 26, 9:58 AM  │ Priya M.    │ VERIFY      │ notification/4821│ SSC CGL    │
  │                     │             │             │                   │ notif verify│
  │  31 Mar 26, 6:00 PM │ System      │ CACHE_REFRESH│ eligibility      │ All users  │
  │  31 Mar 26, 2:14 PM │ Rajan K.    │ CREATE      │ exam/ongc-aee-26 │ New exam   │
  │  31 Mar 26, 11:42 AM│ Priya M.    │ UPDATE      │ question/Q-482840│ Answer key │
  │                     │             │             │                   │ corrected  │
  │  31 Mar 26, 10:08 AM│ System      │ ALERT_SENT  │ notification/4818│ 4,28,000   │
  │                     │             │             │                   │ alerts sent│
  └──────────────────────────────────────────────────────────────────────────────────┘
  [Export CSV]  Page 1 of 2,480
```

---

## 2. Data Integrity Checks

```
DATA INTEGRITY — Automated Daily Checks (run 3:00 AM)

  CHECK                                │ Result    │ Action
  ─────────────────────────────────────┼───────────┼──────────────────
  Exams without syllabus nodes         │ 3 found   │ [Fix] — add nodes
  Syllabus weightages not summing 100% │ 2 exams   │ [Fix] — adjust
  Questions with no exam_tag           │ 420       │ [Assign] — tag
  Active mocks with unreviewed Qs      │ 0         │ ✅ Clean
  Monitoring sources with 0 checks/24h │ 2 sources │ [Investigate]
  Cut-offs without source_url          │ 4 entries │ [Add source]
  Users with stale eligibility cache   │ 0         │ ✅ Clean
  Orphaned study material (no node)    │ 8 items   │ [Map to nodes]

  LAST RUN: 31 Mar 2026, 3:00 AM | Duration: 4 min 22 sec | Issues: 7 (non-critical)
```

---

## 3. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/admin/exam/audit/?user=rajan&action=UPDATE&days=7` | Filtered audit log |
| 2 | `GET` | `/api/v1/admin/exam/integrity/` | Latest data integrity check results |
| 3 | `POST` | `/api/v1/admin/exam/integrity/run/` | Trigger manual integrity check |

---

## 5. Business Rules

- The audit log is append-only and immutable; no admin can edit or delete audit entries; this ensures that if a question's answer key is changed (and 50,000 aspirants' scores are re-computed), there is a permanent record of who changed it, when, and from what to what; in a dispute ("my score was higher yesterday"), the audit log provides the definitive history; the log is retained for 24 months (beyond this, it is archived to cold storage, not deleted)
- Every mutation to the `exam`, `question`, `study_material`, `conducting_body`, `syllabus_node`, `cut_off`, and `notification` tables generates an audit entry; read operations are not logged (too voluminous); the audit entry captures: user_id, timestamp, action (CREATE/UPDATE/DELETE/VERIFY), entity_type, entity_id, and a JSON diff of the changed fields (old_value → new_value); this field-level diff enables precise investigation ("who changed APPSC Group 2 application_end from Jun 30 to Jul 15?")
- Data integrity checks run daily at 3:00 AM and catch data quality issues before aspirants encounter them; an exam without syllabus nodes means the study material hub shows no topics — an aspirant clicking "Study Material" for that exam sees an empty page; a question without an exam_tag cannot appear in any exam-specific mock test; these checks are the quality safety net — they catch issues that the content team's manual workflow missed
- The integrity check for "active mocks with unreviewed questions" is the most critical quality check; it ensures that no full-length mock test (the highest-stakes content type) contains questions that haven't been reviewed by a second person; a mock with a wrong answer key question reaches thousands of aspirants and triggers hundreds of error reports; the integrity check blocks this by verifying that every question in an active mock has `reviewed = true`; new mocks with unreviewed questions are flagged and cannot be published until all questions are reviewed
- System-generated audit entries (CACHE_REFRESH, ALERT_SENT, MONITORING_RUN) provide operational visibility; if the eligibility cache refresh fails at 6:00 AM, the audit log shows no CACHE_REFRESH entry — the admin can investigate; if an alert delivery sent 4,28,000 notifications, the ALERT_SENT entry confirms the scale; these system entries, combined with admin action entries, provide a complete timeline of everything that happened on the platform

---

*Last updated: 2026-03-31 · Group 6 — Exam Domain Portal · Division H*
