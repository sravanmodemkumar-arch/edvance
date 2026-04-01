# 67 — Academic Year Setup Wizard

> **URL:** `/group/acad/year-setup/`
> **File:** `67-academic-year-setup-wizard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** CAO G4 (initiate + submit) · Academic Director G3 (review each step) · MIS Officer G1 (read final confirmation)

---

## 1. Purpose

One-time wizard run at the end of each academic year to transition the group to the new academic year.
Covers student promotion, syllabus version activation, exam calendar reset, and branch notification.

Without this wizard, year-end rollover is done ad-hoc across branches — resulting in data inconsistency
(some branches still operating on old year data, promoted students showing in wrong class, etc.).

The wizard is **sequential** (steps must be completed in order), **draft-saveable** (can be paused and resumed),
and **guarded** (cannot initiate if prior year still has unresolved moderation).

---

## 2. Role Access

| Role | Level | Can Initiate | Can Review | Can Submit | Notes |
|---|---|---|---|---|---|
| CAO | G4 | ✅ | ✅ | ✅ | Primary owner of the wizard |
| Academic Director | G3 | ❌ | ✅ (each step) | ❌ | Can comment and flag issues |
| MIS Officer | G1 | ❌ | ❌ | ❌ | Read final confirmation summary only |
| Other Div-B roles | G3/G2 | ❌ | ❌ | ❌ | Notified on completion |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  Academic Year Setup
```

### 3.2 Page Header
```
Academic Year Setup Wizard                          [Save Draft]  [View Previous Year Setup]
AY 2024–25 → AY 2025–26 · CAO: [Name] · Status: In Progress (Step 3 of 6)
```

### 3.3 Wizard Progress Bar
```
[Step 1: Year Dates ✓] → [Step 2: Student Promotion ✓] → [Step 3: Syllabus →] → [Step 4: Calendar] → [Step 5: Fee Handoff] → [Step 6: Notify & Confirm]
```

Progress bar shows completed steps (green ✓), current step (blue →), and pending steps (grey).

---

## 4. Wizard Steps

### Step 1 — Confirm Year Dates

| Field | Type | Required | Validation |
|---|---|---|---|
| New Academic Year Label | Text | ✅ | e.g. "2025–26" — auto-suggested |
| Start Date | Date picker | ✅ | Must be future date |
| End Date | Date picker | ✅ | Must be after start date |
| Term 1 Start / End | Date range | ✅ | Within year range |
| Term 2 Start / End | Date range | ✅ | After Term 1 |
| Term 3 Start / End | Date range | ✅ | After Term 2 |
| Inherit holidays from previous year? | Toggle | ❌ | If Yes, holiday list cloned and editable |

**Guard:** If previous year has result moderation rows with status "Pending" → show blocking alert:
> "⚠ Previous year has [N] unresolved result moderation records. Resolve before initiating new year setup."
> [Go to Result Moderation →] (Page 27)

---

### Step 2 — Student Promotion

**Purpose:** Move students from current class to next class. Handle exceptions (detained, transferred, graduated).

| Element | Spec |
|---|---|
| **Promotion rules table** | Stream → Current Class → Next Class (editable mapping) e.g. Class 11 MPC → Class 12 MPC |
| **Pass criteria** | Minimum % to be auto-promoted (default from Academic Policy, page 65) — overridable here |
| **Auto-promotion preview** | Count of students auto-promoted per stream/class |
| **Exception list** | Students below pass criteria — shown in table for manual action |
| **Exception actions per student** | Promote (override) · Detain (repeat class) · Transfer Out · Mark Graduated |
| **Graduated students** | Class 12 students → marked graduated, moved to alumni pool |
| **Bulk action** | Select multiple exceptions → Apply same action |
| **Confirmation** | "Promote [N] students, Detain [M], Graduate [P]" → Confirm before proceeding |

---

### Step 3 — Activate New Syllabus Version

**Purpose:** Activate the syllabus prepared for the new year. Branches inherit the group syllabus.

| Element | Spec |
|---|---|
| **Syllabus list** | Table: Stream · Class · Current Version · Draft Version (if exists) · Status |
| **Action per row** | Activate Draft → makes draft the live syllabus for new year |
| **Clone option** | If no draft: "Clone from [Year] with edits?" — creates a copy in draft for quick activation |
| **Preview** | View syllabus topic list before activation |
| **Locked on activate** | Previous year syllabus becomes read-only archive |
| **Warning** | Branches with active lesson plans (Page 16) referencing old syllabus are flagged |

---

### Step 4 — Reset Exam Calendar

**Purpose:** Copy mandatory recurring exam events into the new year's calendar.

| Element | Spec |
|---|---|
| **Recurring events** | Events from previous year marked "Recurring" — listed for selection |
| **New year calendar preview** | Calendar grid for new AY showing imported events |
| **Editable on import** | Dates auto-adjusted; coordinator can shift dates before confirming |
| **New events** | Option to add new mandatory events directly in this step |
| **Link** | Full calendar editing remains in Group Academic Calendar (Page 59) post-setup |

---

### Step 5 — Fee Structure Handoff

**Purpose:** Signal to the finance module that academic year has changed. Fee configuration is handled by branch finance teams, but must be triggered from here.

| Element | Spec |
|---|---|
| **Action** | One-click: "Mark AY 2025–26 fee structure as pending setup" |
| **Effect** | Each branch Principal receives a task in their branch portal: "Set up AY 2025–26 fee structure" |
| **Status** | Shows how many branches have completed fee setup (updates live after step is submitted) |
| **Note** | This step does not configure fees — it only notifies branch administrators |

---

### Step 6 — Notify Branches & Confirm

**Purpose:** Send official AY setup completion notice to all branch Principals. Require acknowledgement.

| Element | Spec |
|---|---|
| **Notification preview** | Shows the message that will be sent to all Principals |
| **Notification content** | AY dates · Promotion summary · New syllabus version · Calendar reset confirmation · Fee setup task |
| **Channels** | Portal notification + WhatsApp (if configured) |
| **Acknowledgement tracking** | Table: Branch · Principal · Notified At · Acknowledged At · Status |
| **Submit wizard** | [Complete AY Setup] button — sends notifications, locks wizard, creates AY record |
| **Post-submit** | Wizard becomes read-only "Completed" view · New wizard can be initiated next year only |

---

## 5. Draft & Resumption

| Behaviour | Detail |
|---|---|
| Auto-save | Every step saved on "Next" click — state persisted in DB |
| Resume | Page shows "Resume from Step N" when draft exists |
| Multi-session | CAO and Academic Director can view same draft — only CAO can advance steps |
| Abandon draft | [Discard Draft] option — requires typed confirmation "DISCARD" |

---

## 6. Wizard History

- **Trigger:** [View Previous Year Setup] header button
- **Content:** Table of all previous AY setups — Year · Initiated By · Completed Date · Download Summary
- **Download Summary:** PDF of all choices made in wizard for that year (audit trail)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Step completed | "Step [N] saved. Proceed to Step [N+1]." | Success | 3s |
| Draft saved | "Draft saved. Resume anytime." | Info | 3s |
| Guard triggered | "Unresolved moderation records — resolve before initiating." | Error | Manual |
| Wizard completed | "AY 2025–26 setup complete. All branches notified." | Success | 6s |
| Syllabus activated | "Syllabus for [Stream] Class [N] activated for AY 2025–26." | Success | 4s |

---

## 8. Empty States

| Condition | Heading | Description |
|---|---|---|
| No draft, no history | "Start New Academic Year Setup" | First time — initiate wizard |
| Draft in progress | "AY Setup In Progress" | Resume wizard from Step N |
| Completed | "AY 2025–26 Setup Complete" | View summary / download PDF |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Wizard page load | Skeleton: progress bar + step content area |
| Step 2 promotion preview | Spinner in promotion table (calculating from results data) |
| Step 3 syllabus list load | Skeleton table rows |
| Submit wizard | Full-page overlay "Setting up AY 2025–26… Notifying branches…" |

---

## 10. Role-Based UI Visibility

| Element | CAO G4 | Academic Director G3 | MIS Officer G1 |
|---|---|---|---|
| [Initiate Wizard] | ✅ | ❌ | ❌ |
| [Next Step] button | ✅ | ❌ | ❌ |
| [Comment on step] | ✅ | ✅ | ❌ |
| [Complete AY Setup] | ✅ | ❌ | ❌ |
| View wizard summary | ✅ | ✅ | ✅ (final only) |
| [Discard Draft] | ✅ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/acad/year-setup/` | JWT (G3+) | Get current draft or completed setup |
| POST | `/api/v1/group/{id}/acad/year-setup/` | JWT (G4) | Initiate new wizard draft |
| PUT | `/api/v1/group/{id}/acad/year-setup/{wid}/steps/{n}/` | JWT (G4) | Save step N data |
| POST | `/api/v1/group/{id}/acad/year-setup/{wid}/complete/` | JWT (G4) | Submit wizard and notify branches |
| DELETE | `/api/v1/group/{id}/acad/year-setup/{wid}/` | JWT (G4) | Discard draft |
| GET | `/api/v1/group/{id}/acad/year-setup/history/` | JWT (G3+) | Previous year setups |
| GET | `/api/v1/group/{id}/acad/year-setup/{wid}/summary.pdf` | JWT (G4) | PDF summary of completed setup |
| GET | `/api/v1/group/{id}/acad/year-setup/{wid}/promotion-preview/` | JWT (G4) | Step 2 auto-promotion preview |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load wizard state | `load` | GET `.../year-setup/` | `#wizard-container` | `innerHTML` |
| Save and advance step | `click` | PUT `.../steps/{n}/` | `#wizard-step-body` | `innerHTML` |
| Promotion preview | `load` (step 2) | GET `.../promotion-preview/` | `#promotion-table` | `innerHTML` |
| Syllabus list load | `load` (step 3) | GET `.../syllabus-versions/` | `#syllabus-table` | `innerHTML` |
| Complete wizard | `click` | POST `.../complete/` | `#wizard-container` | `innerHTML` |
| Discard draft confirm | `click` | DELETE `.../year-setup/{wid}/` | `#wizard-container` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
