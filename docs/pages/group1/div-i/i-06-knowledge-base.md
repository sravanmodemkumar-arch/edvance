# I-06 — Knowledge Base Manager

**Route:** `GET /support/knowledge-base/`
**Method:** Django CBV (`ListView`) + HTMX part-loads
**Primary roles:** Training Coordinator (#52) — author; Support Manager (#47) — approve/manage
**Also sees:** L1 (#48), L2 (#49), L3 (#50) — read only; Support Quality Lead (#108) — read + flag gap; Onboarding Specialist (#51) — read only

---

## Purpose

Internal knowledge base for the support team. Training Coordinator authors and maintains articles. Support Manager approves articles before publication. All support staff use published articles to resolve tickets faster. Support Quality Lead flags KB gaps when recurring ticket patterns reveal missing articles.

A secondary section manages **training sessions** (institution-facing sessions scheduled by Training Coordinator and Onboarding Specialist).

---

## Data Sources

| Section | Source |
|---|---|
| Article list | `kb_article` with filters; 10-min Memcached TTL for published; no cache for DRAFT |
| Gap flags | `kb_article_gap_flag` WHERE status='OPEN'; no cache |
| Training sessions | `onboarding_training_session` ordered by `scheduled_at` desc; 5-min TTL |
| Article stats | `kb_article.view_count`, `helpful_votes`, `not_helpful_votes` |

---

## URL Parameters

| Param | Values | Effect |
|---|---|---|
| `?tab` | `articles`, `gaps`, `sessions` | Active tab; default `articles` |
| `?status` | `DRAFT`, `PENDING_REVIEW`, `PUBLISHED`, `ARCHIVED` | Filter articles by status |
| `?category` | Any kb_article category | Filter articles |
| `?q` | text | Search article titles |
| `?article_id` | integer | Jump directly to article edit view |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| Article list | `?part=articles` | Page load, filter change |
| Article editor | `?part=editor&id={id}` | Edit button click |
| New article form | `?part=new_article` | [+ New Article] click |
| Gap flags list | `?part=gaps` | Tab switch |
| Training sessions | `?part=sessions` | Tab switch |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Knowledge Base        [Articles] [KB Gaps (3)] [Training]       │
├──────────────────────────────────────────────────────────────────┤
│  SEARCH + FILTERS           [+ New Article] (Training Coord only)│
├──────────────────────────────────────────────────────────────────┤
│  ARTICLE LIST / EDITOR / SESSIONS (tab content)                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Tab 1 — Articles

### Filter Row

| Filter | Options |
|---|---|
| Status | All / Draft / Pending Review / Published / Archived |
| Category | LOGIN / EXAM_FLOW / BILLING / ONBOARDING / TECHNICAL / ADMIN_PORTAL / RESULTS / GENERAL |
| Author | Dropdown of Training Coordinators and Support Managers |
| Sort | Newest / Most Viewed / Most Helpful / Recently Updated |

Search bar: full-text on `kb_article.title`.

---

### Article List

Each article as a table row (not card — better for scanning many articles):

| Column | Content |
|---|---|
| Title | Article title; links to inline editor (Training Coord) or preview (others) |
| Category | Badge |
| Status | DRAFT (grey), PENDING_REVIEW (steady blue), PUBLISHED (green), ARCHIVED (grey italic) |
| Author | Name |
| Published | Date or "—" |
| Views | `view_count` |
| Helpful | `helpful_votes` / `(helpful_votes + not_helpful_votes)` as percentage |
| Linked categories | Ticket category badges this article covers |
| Actions | Role-dependent (see below) |

**Training Coordinator (#52) row actions:**
- [Edit] — opens article editor
- [Submit for Review] — only for DRAFT articles; changes status to PENDING_REVIEW; clears `review_feedback` field (any prior rejection feedback is removed on re-submission)
- [Archive] — only for PUBLISHED articles; requires confirmation
- [Delete Draft] — only for DRAFT articles; hard-delete with confirmation "Delete this draft permanently? This cannot be undone."; article removed from list. Training Coordinator can clean up stale drafts they no longer intend to publish. Cannot delete PUBLISHED or ARCHIVED articles.
- [Duplicate] — creates DRAFT copy with "(Copy)" prefix

**Support Manager (#47) row actions:**
- [Approve] — only for PENDING_REVIEW articles; confirmation "Publish this article? It will be visible to all support staff immediately."
- [Reject] — returns to DRAFT with feedback note field
- [Edit] — can edit any article (inline or redirect to full editor)
- [Archive] — any non-archived article; changes status to ARCHIVED
- [Restore] — ARCHIVED articles only; returns status to DRAFT
- [Delete] — ARCHIVED articles only; hard-delete with confirmation modal: "Permanently delete '{title}'? This cannot be undone. The article will immediately stop appearing in KB suggestion panels." → POST `/support/knowledge-base/{id}/delete/`; row removed. Note: `support_ticket_message` records do NOT store FK references to KB articles — KB suggestions are computed at query time from live PUBLISHED articles, so there are no stored FK references to nullify. The article will no longer appear in I-03 KB suggestion panels on next page load. All `kb_article_vote` records for this article are cascaded-deleted. Deletion logged to audit trail.

**L1/L2/L3 / Onboarding Specialist / Quality Lead row actions:**
- [View] — opens read-only article preview

---

### Article Editor (Training Coordinator / Support Manager)

Opens as a right-side panel (900px) or full-page depending on screen width.

```
┌──────────────────────────────────────────────────────────────────┐
│  ← Back to Articles                     [Save Draft] [Preview]   │
├──────────────────────────────────────────────────────────────────┤
│  Title: [___________________________________________________]    │
│  Category: [▼ SELECT]   Status: DRAFT                            │
│  Linked ticket categories: [☐ Login Issue] [☐ Exam Access] ...  │
├──────────────────────────────────────────────────────────────────┤
│  MARKDOWN EDITOR (with toolbar)                                  │
│  [B] [I] [Code] [Link] [H1] [H2] [List] [Image] [Table]        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ ## Resolving Student Login Issues                        │   │
│  │                                                          │   │
│  │ If a student cannot log in, follow these steps:         │   │
│  │ 1. Check if account is active in the student portal.    │   │
│  │ ...                                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────────────┤
│  [Save Draft]   [Submit for Review]   (Training Coord)           │
│  [Approve]  [Reject with Feedback]   (Support Manager only)     │
└──────────────────────────────────────────────────────────────────┘
```

[Preview] toggle: switches editor to rendered markdown preview (same panel). Switch back with [Edit].

**Linked ticket categories** checkboxes: determines which ticket categories will show this article as a KB suggestion in I-03. Multiple selection allowed.

[Submit for Review] → status: PENDING_REVIEW; Support Manager gets F-06 notification.

**[Reject with Feedback] (Support Manager):**
```
Reject Article

Feedback for Training Coordinator:
[________________________________________________]
(required)

[Cancel]  [Reject & Return to Draft]
```

POST `/support/knowledge-base/{id}/reject/`; status → DRAFT; feedback note stored in `kb_article` (new `review_feedback` field); Training Coordinator gets notification with feedback text.

---

### Article Read View (L1/L2/L3/Others)

Clean rendered markdown. No editor controls.

```
Resolving Student Login Issues
Category: LOGIN  |  Published: 2 Nov 2024  |  Last updated: 5 Nov 2024

─────────────────────────────────────────────

If a student cannot log in, follow these steps:
1. Check if account is active in the student portal.
...

─────────────────────────────────────────────
Was this article helpful?   [👍 Yes (42)]   [👎 No (3)]
[Flag for Review]
```

[👍] / [👎] increments `helpful_votes` / `not_helpful_votes`. One vote per user per article (idempotent).

[Flag for Review] (Quality Lead only): creates `kb_article_gap_flag` with type "INACCURATE/OUTDATED" for this article's category; Support Manager notified.

`view_count` incremented on each page load (not HTMX part-load).

---

## Tab 2 — KB Gaps

List of open `kb_article_gap_flag` records.

Visible to: Support Manager, Support Quality Lead. Others see a "Not authorised" message in this tab.

Table: Flagged By | Category | Description | Status | Assigned To | Created | Actions

**Actions:**
- [Assign to Training Coordinator] (Support Manager) — assigns flag to Training Coordinator; status → ASSIGNED; Training Coordinator gets notification
- [Mark Resolved] (Support Manager; assigned Training Coordinator) — closes flag; status → RESOLVED
- [Create Article from Flag] — opens article editor pre-filled with category and gap description as article outline

```
OPEN Gap Flags (3)
─────────────────────────────────────────────────────────────────
❗ Category: EXAM_ACCESS | "No article for exam rejoin after session timeout"
   Flagged by: Ananya (Quality Lead) · 5 Nov 2024
   [Assign] [Create Article]

❗ Category: RESULTS | "No article explaining rank computation timeline"
   Flagged by: Rahul (L2) · 3 Nov 2024
   [Assign] [Create Article]
```

[+ Flag a Gap] button (Quality Lead; any agent):
```
Flag a KB Gap

Ticket category: [▼ SELECT]
Description: [_____________________________________]
(What topic is missing from the KB?)

[Cancel]  [Flag Gap]
```

---

## Tab 3 — Training Sessions

All training sessions across all onboarding instances + standalone sessions.

Filter: Institution | Session type | Status | Date range | Conducted by

Table: Institution | Session Type | Title | Scheduled | Duration | Status | Conducted By | Attendees | Actions

**Status badges:** SCHEDULED (blue), COMPLETED (green), CANCELLED (grey), NO_SHOW (red).

[Mark Completed] (Training Coordinator; Onboarding Specialist):
```
Mark Session as Completed

Attendees present:
  ☑ Meena Reddy  ☑ Rajesh Kumar  ☐ Priya Singh (marked absent)

Post-session notes:
[_____________________________________]

Recording URL (optional):
[_____________________________________]

[Cancel]  [Mark Completed]
```

POST `/support/onboarding/sessions/{id}/complete/`; updates `status`, `attendee_names` (present ones), `notes`, `recording_url`.

[+ New Session] button: opens the same modal as I-05 but without locking to a specific institution (institution is an optional autocomplete field — leave blank for a platform-wide standalone session).

Standalone sessions (`instance_id=null`): `title` and `scheduled_at` are required even without an institution. Stored in `onboarding_training_session` table; distinguished by "Standalone" badge. Visible in I-06 Training tab; also appears in I-05 Training Sessions tab under "Standalone sessions" section if the session has no `instance_id`.

**Training Coordinator permissions summary** (I-06 vs I-05):
- In I-06: can create and schedule sessions (both standalone and institution-linked), mark sessions as COMPLETED/CANCELLED/NO_SHOW, add attendee records — full write access
- In I-05: **no access** (cannot view the onboarding tracker page); Onboarding Specialist manages onboarding stages and checklists
- The separation is intentional: Training Coordinator owns session content delivery; Onboarding Specialist owns onboarding pipeline progression

---

## Edge Cases

1. **Training Coordinator tries to publish directly**: No [Publish] button shown. [Submit for Review] is the only forward action. Status field is read-only for Training Coordinator.
2. **Support Manager edits a PUBLISHED article**: Edit saves directly (no re-review required for minor edits); `updated_at` timestamp refreshes on the article; agents see "Updated X min ago" label.
3. **Article with 0 helpful/not_helpful votes**: Shows "No ratings yet" instead of percentage. Voting is tracked per user via `kb_article_vote` table (one row per user per article; re-voting updates the row from HELPFUL→NOT_HELPFUL or vice versa; `kb_article.helpful_votes` and `not_helpful_votes` are atomically incremented/decremented via DB trigger on `kb_article_vote`). Anonymous users (institution admins viewing published articles from institution portal) cannot vote — voting is support-team-only.
4. **Search returns 0 results**: "No articles found for '{query}'. [Clear search] or [Flag this as a KB gap →]" — second link opens [+ Flag a Gap] form pre-filled with the query text as description.
5. **Article linked to ticket category auto-suggestion in I-03**: Only PUBLISHED articles appear as suggestions. DRAFT/PENDING_REVIEW articles never surface in I-03.
6. **Duplicate article detection**: On article save, if another PUBLISHED article has >80% title similarity (checked server-side via trigram similarity in PostgreSQL `pg_trgm`), show warning: "Similar article found: 'How to resolve student login issues'. Review before saving."
6a. **Slug collision on title**: `kb_article.slug` is auto-generated from the title (`slugify(title)`). On collision with an existing slug, the server appends `-2`, `-3`, etc. (e.g., `student-login-issues-2`). The Training Coordinator does not see the slug during authoring; it is managed server-side. If the auto-generated slug exceeds 200 chars, it is truncated at a word boundary before appending the suffix.
7. **Archived article still linked in I-03**: If an article is archived while it's still in a ticket's KB suggestion list, the suggestion is removed on the next I-03 KB suggestion load (5-min TTL clears naturally).
8. **Training session with no-show**: Selecting NO_SHOW status prompts: "Reason for no-show: [text field]"; note saved to session. A follow-up session can be scheduled directly from this modal.

---

## Notifications (via F-06)

- Article submitted for review → push to Support Manager
- Article approved → push to authoring Training Coordinator: "Your article '{title}' is now published"
- Article rejected → push to Training Coordinator with feedback note
- KB gap flagged → push to Support Manager
- KB gap assigned → push to Training Coordinator
- Training session scheduled → email to attendees (AWS SES); F-06 push to Support Manager
