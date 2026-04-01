# P-23 — Audit Template & Checklist Library

> **URL:** `/group/audit/templates/`
> **File:** `p-23-audit-template-library.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Inspection Officer (Role 123, G3) — primary operator

---

## 1. Purpose

The Audit Template & Checklist Library is the master repository of all audit instruments used by Division P — financial audit checklists, academic quality review forms, operational inspection checklists, affiliation compliance checklists, CAPA templates, and scoring rubrics. Without a standardised library, each auditor creates their own checklist, resulting in inconsistent coverage, unequal scrutiny across branches, and audit results that cannot be compared meaningfully.

In Indian education groups, audit quality degrades rapidly when audit instruments are not standardised. A new Inspection Officer who inherits a manual that says "check fire safety" will check different things than the officer who created it. When the Audit Head reviews findings from two inspectors who visited different branches in the same week using different checklists, the findings are not comparable. The library solves this — every auditor uses the same instrument, every branch is audited on the same criteria, and every result is directly comparable.

The problems this page solves:

1. **Checklist proliferation:** Over time, audit teams accumulate dozens of Excel checklists — V1, V2, final, final_v2, July-updated. There is no single authoritative version. The library enforces version control — one published version per checklist type at any time.

2. **CBSE/ICSE/State Board variation:** A CBSE school needs to be audited on CBSE affiliation norms; an ICSE school on CISCE norms; a State Board school on that state's education department requirements. The library maintains separate templates per board affiliation, with the applicable norms pre-loaded.

3. **Scoring inconsistency:** One inspector marks "fire extinguisher present but not serviced" as a pass; another marks it as a fail. The rubric in the template defines the scoring criteria precisely — with examples of what constitutes a pass, a partial pass, and a fail for each checklist item.

4. **Checklist maintenance lag:** CBSE updates its affiliation norms; POCSO guidelines are amended; new fire safety rules come into force. Without a centralised library, updated norms are not reflected in the checklists used in the field. The library has a version control and expiry system that flags when a checklist may be outdated.

5. **Field accessibility:** Inspectors on branch visits need checklists on their mobile device, not printed paper. The library provides mobile-optimised versions of all checklists accessible offline via the Flutter app.

**Scale:** 20–50 template types · 3–10 versions per template over time · Used by 3–5 field inspectors · Updated 1–2 times per year per template · Branch-type-specific variants

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Inspection Officer | 123 | G3 | Read + Use (apply to inspection visits) | Primary user |
| Group Internal Audit Head | 121 | G1 | Read + Approve new/updated templates before publishing | Approver |
| Group Process Improvement Coordinator | 128 | G3 | Read + Use (for CAPA verification checklists) | User |
| Group Affiliation Compliance Officer | 125 | G1 | Read + Maintain affiliation-specific templates | Domain editor |
| Group Academic Quality Officer | 122 | G1 | Read + Maintain academic quality templates | Domain editor |
| Group Compliance Data Analyst | 127 | G1 | Read | Reference |
| Branch Principal | — | G3 | Read (own institution-type templates) — self-assessment use | Self-audit |

> **Access enforcement:** `@require_role(min_level=G3, division='P')`. Template creation/edit: 123, 122, 125, 128 (domain-specific). Publishing (making live): 121 approval required. Principals access published templates for their institution type only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Template Library
```

### 3.2 Page Header
```
Audit Template & Checklist Library                  [+ New Template]  [Import Template]  [Export All]
Inspection Officer — S. Reddy
Sunrise Education Group · 34 published templates · 3 in draft · 2 under review · Last updated: 15-Mar-2026
```

### 3.3 Filter Bar
```
Type: [All / Inspection / Financial Audit / Academic Audit / Affiliation / CAPA / Safety / Grievance ▼]
Institution Type: [All / School / Coaching / Hostel / College / All Types ▼]
Board Affiliation: [All / CBSE / ICSE / State Board / General ▼]
Status: [All / Published / Draft / Under Review / Deprecated ▼]
                                                                        [Reset]
```

### 3.4 Template Library Grid

Cards in a 3-column grid (or table view — toggle available).

**Card layout:**

```
┌──────────────────────────────────────────────────────────┐
│  📋 Branch Physical Inspection Checklist                  │
│  Type: Inspection · Scope: All branches                   │
│  Board: All · Institution type: School + Coaching         │
│  Items: 87 checklist items · Sections: 8                  │
│  Version: v3.2 · Published: 15-Mar-2026                   │
│  Status: ✅ Published (Active)                             │
│                                                           │
│  Last used: 20-Mar-2026 · Used 34 times this FY           │
│  Maintained by: S. Reddy (123)                            │
│                                                           │
│  [View]  [Use in Inspection]  [Edit]  [Version History]   │
└──────────────────────────────────────────────────────────┘
```

**Status badges:**
- ✅ Published — active, used in field
- 🟡 Draft — being created, not yet submitted
- 🔵 Under Review — submitted to Audit Head for approval
- ⬛ Deprecated — superseded by newer version, archived

---

## 4. Template Types in Library

### Category: Physical Inspection

| Template Name | Scope | Items | Version | Last Updated |
|---|---|---|---|---|
| Branch Physical Inspection Checklist | School + Coaching | 87 items, 8 sections | v3.2 | 15-Mar-2026 |
| Hostel / Residential Inspection Checklist | Hostel + Residential School | 112 items, 10 sections | v2.1 | 20-Jan-2026 |
| Fire Safety Inspection Checklist | All branches | 34 items, 4 sections | v1.4 | 10-Feb-2026 |
| CCTV & Security Inspection Checklist | All branches | 22 items, 3 sections | v1.1 | 05-Jan-2026 |
| Laboratory Safety Checklist | Schools + Colleges | 28 items, 3 sections | v1.2 | 12-Feb-2026 |
| Canteen & Food Safety Checklist | All with canteen | 31 items, 4 sections | v1.3 | 01-Mar-2026 |

### Category: Financial Audit

| Template Name | Scope | Items | Version | Last Updated |
|---|---|---|---|---|
| Fee Collection Audit Checklist | All branches | 45 items, 5 sections | v2.3 | 10-Jan-2026 |
| Petty Cash Audit Checklist | All branches | 18 items, 2 sections | v1.2 | 15-Dec-2025 |
| Vendor Payment Audit Checklist | All branches | 32 items, 4 sections | v1.4 | 20-Feb-2026 |
| Annual Financial Audit Protocol | All branches | 78 items, 7 sections | v2.0 | 01-Apr-2025 |

### Category: Academic Quality

| Template Name | Scope | Items | Version | Last Updated |
|---|---|---|---|---|
| Lesson Plan Quality Review Checklist | Schools + Coaching | 24 items, 3 sections | v1.3 | 05-Feb-2026 |
| Exam Paper Quality Audit Template | All branches | 19 items, 2 sections | v1.1 | 10-Jan-2026 |
| Syllabus Coverage Audit Template | Schools + Coaching | 15 items, 2 sections | v1.0 | 15-Sep-2025 |
| Teaching Observation Rubric | Schools + Coaching | 20 criteria, 4 sections | v2.2 | 01-Mar-2026 |

### Category: Affiliation & Regulatory

| Template Name | Scope | Items | Version | Last Updated |
|---|---|---|---|---|
| CBSE Affiliation Readiness Checklist | CBSE branches | 48 items, 6 sections | v1.5 | 01-Feb-2026 |
| ICSE/ISC Affiliation Checklist | ICSE branches | 52 items, 6 sections | v1.2 | 15-Jan-2026 |
| Telangana State Board Affiliation | TS branches | 38 items, 5 sections | v1.1 | 10-Jan-2026 |
| AP State Board Affiliation | AP branches | 35 items, 5 sections | v1.0 | 10-Jan-2026 |
| Annual UDISE+ Readiness Checklist | All school branches | 22 items, 3 sections | v1.2 | 01-Sep-2025 |

### Category: CAPA Verification

| Template Name | Scope | Items | Version | Last Updated |
|---|---|---|---|---|
| CAPA Closure Verification Checklist (General) | All | 12 items | v1.1 | 01-Mar-2026 |
| Fire Safety CAPA Verification | All | 14 items | v1.0 | 15-Feb-2026 |
| Records & Documentation CAPA Verification | All | 10 items | v1.0 | 10-Feb-2026 |

---

## 5. Template Detail View

**URL:** `/group/audit/templates/{template_id}/`

Full-page view for a single template.

### Header
```
Branch Physical Inspection Checklist                    [Edit]  [Use in Inspection]  [Deprecate]
Type: Inspection · Scope: School + Coaching · Version: v3.2 · Published: 15-Mar-2026
Maintained by: S. Reddy (123) · Approved by: T. Subramaniam (121)
```

### Section 1 — Template Metadata

| Field | Value |
|---|---|
| Template ID | TPL-INSP-001 |
| Name | Branch Physical Inspection Checklist |
| Type | Inspection |
| Institution Type | School + Coaching Centre |
| Board Affiliation | All boards |
| Language | English (Telugu version available — TPL-INSP-001-TE) |
| Version | v3.2 |
| Status | Published |
| Total Items | 87 |
| Sections | 8 (see below) |
| Estimated Completion Time | 45–90 minutes per branch visit |
| Last Changed | Section 5 (Infrastructure) — 2 items updated per CBSE 2025 circular |
| Revision Notes | v3.2: Added CCTV coverage angle requirement per CBSE Safety Circular 2025. Updated fire exit clearance requirement from 1.2m to 1.5m. |
| Next Review Due | Sep-2026 (semi-annual review cycle) |
| Related Policy | Group Inspection Policy P-016 |

### Section 2 — Checklist Items (structured view)

**Section 1 — Building & Infrastructure (12 items):**

| # | Item | Type | Scoring | Notes Prompt |
|---|---|---|---|---|
| 1.1 | Building stability certificate valid (< 5 years old) | Document check | Pass / Fail | Upload photo of certificate |
| 1.2 | Building visibly structurally sound — no cracks, seepage | Visual | Pass / Partial / Fail | Describe any visible damage |
| 1.3 | All staircases have handrails on both sides | Visual | Pass / Partial / Fail | Note which staircases lack handrails |
| 1.4 | Roof condition — no visible damage or leakage | Visual | Pass / Partial / Fail | Check all floors |
| 1.5 | Drinking water supply functional and clean | Visual + Test | Pass / Partial / Fail | Check RO/purification system |
| 1.6 | Toilet blocks — separate for boys, girls, staff | Visual | Pass / Fail | Count functional units |
| 1.7 | Classroom sizes meet CBSE minimum (≥ 40 sq.ft/student) | Measurement | Pass / Fail | Use formula: room area ÷ student count |
| 1.8 | Library room with minimum 1,500 books (CBSE requirement) | Physical count | Pass / Fail | Record actual book count |
| 1.9 | Science lab equipped with basic apparatus and safety equipment | Visual | Pass / Partial / Fail | List major missing items |
| 1.10 | Computer lab with functional computers (student:computer ≤ 2:1) | Count | Pass / Fail | Record computer count + students |
| 1.11 | Playground / open area ≥ 2,000 sq.ft | Measurement | Pass / Fail | Record actual area |
| 1.12 | Adequate lighting in all classrooms and corridors | Visual | Pass / Fail | Note dark areas |

**Section 2 — Fire Safety (10 items):**

| # | Item | Scoring |
|---|---|---|
| 2.1 | Fire NOC from State Fire Dept — valid and displayed | Pass / Fail |
| 2.2 | Fire extinguishers — present in all required locations | Pass / Partial / Fail |
| 2.3 | Fire extinguishers — serviced within last 12 months (check label) | Pass / Fail |
| 2.4 | Fire exit doors — all exit doors openable from inside, not locked | Pass / Fail |
| 2.5 | Fire exit corridors — clear of obstructions ≥ 1.5m width | Pass / Fail |
| 2.6 | Fire exit signage — illuminated "EXIT" signs present at all exits | Pass / Fail |
| 2.7 | Fire alarm system — functional (test during visit) | Pass / Fail |
| 2.8 | Emergency evacuation map — posted in each classroom | Pass / Partial / Fail |
| 2.9 | Fire drill conducted in last 3 months — register available | Document | Pass / Fail |
| 2.10 | Assembly point clearly marked in campus | Visual | Pass / Fail |

*(Sections 3–8 similarly detailed: CCTV & Security · Staff & Records · Academic · Hygiene & Sanitation · Student Welfare · Compliance Documentation)*

**Scoring methodology (shown at top of checklist):**
```
Scoring:
  Pass (2 pts): Requirement fully met
  Partial (1 pt): Requirement partially met — specify gap in notes
  Fail (0 pts): Requirement not met — CAPA required
  N/A: Not applicable to this branch type

Section score = (actual points / maximum points) × 100%
Overall inspection score = weighted average across sections

Minimum pass threshold per item: Some items are marked "Critical" —
  a Fail on any Critical item automatically flags the visit as requiring
  immediate CAPA regardless of overall score.
Critical items (marked ⚠️): 2.1, 2.4, 2.5, 2.7 (fire safety), and any
  POCSO-related compliance items in Section 7.
```

### Section 3 — Version History

| Version | Released | Changed By | Changes Summary |
|---|---|---|---|
| v3.2 | 15-Mar-2026 | S. Reddy (123) | CCTV coverage angle added; fire exit width updated to 1.5m |
| v3.1 | 10-Jan-2026 | S. Reddy (123) | Added 3 new items per CBSE 2025 safety circular |
| v3.0 | 01-Apr-2025 | T. Subramaniam (121) | Major revision — restructured sections; added hostel section |
| v2.5 | 15-Oct-2024 | S. Reddy (123) | Minor updates to lab safety items |

### Section 4 — Usage Statistics

| Metric | Value |
|---|---|
| Total uses (all FYs) | 124 |
| Uses this FY | 34 |
| Branches covered | 26 of 28 |
| Avg completion time | 67 minutes |
| Avg score on this checklist | 74% |
| Most common fail item | 2.3 (Fire extinguisher not serviced) — 18 fails |
| Most common partial | 1.8 (Library book count) — 12 partials |

---

## 6. Template Editor

**URL:** `/group/audit/templates/{id}/edit/`

Full-page editor for creating and modifying templates.

**Left panel — Section Manager:**
- List of sections with drag-to-reorder
- `[+ Add Section]` `[Delete Section]`
- Each section: name, weight (% of total score), description

**Centre panel — Item Editor:**
For the selected section, shows all items. Each item has:
- Item text (required)
- Type: Visual / Document Check / Measurement / Interview / Count
- Critical item flag (⚠️) — fail triggers mandatory CAPA
- Scoring type: Pass/Fail | Pass/Partial/Fail | Numeric (0–10) | Percentage
- Score weight within section
- Evidence required: None / Photo / Document / Both
- Notes prompt (guidance for inspector)
- Help text (e.g., "CBSE Circular 2025 reference: Section 4.3")

**Right panel — Preview:**
Live preview of how the checklist item appears in the field (mobile view simulation).

**Toolbar:**
```
[Save Draft]  [Preview Full Checklist]  [Submit for Review]
```

---

## 7. Modals

### Modal 1 — New Template

**Trigger:** `[+ New Template]`

**Form:**
```
Template Name: [_______________________]
Type: [Inspection / Financial Audit / Academic / Affiliation / CAPA Verification / Safety ▼]
Institution Type: [All / School / Coaching / Hostel / College / Multi-select ▼]
Board Affiliation: [All / CBSE / ICSE / State Board / Not Applicable ▼]
Language: [English ▼]
Start from: ◉ Blank template   ○ Copy from existing: [Select template ▼]
```

**Actions:** `[Create & Open Editor]` `[Cancel]`

---

### Modal 2 — Submit for Review

**Form:**
```
Submitting: Branch Physical Inspection Checklist v3.2 (draft)
To: T. Subramaniam (Audit Head, 121)

Change Summary (required): [What changed and why]
Regulation reference (if applicable): [CBSE Circular / RTE amendment / etc.]
Effective Date: [When this version should go live]
```

**Actions:** `[Submit for Review]` `[Cancel]`

---

### Modal 3 — Approve / Return (Audit Head view)

**Available to Role 121 only.**

```
Review: Branch Physical Inspection Checklist v3.2
Submitted by: S. Reddy · 14-Mar-2026
Change summary: [shows submitter's notes]

Review checklist items: [scrollable preview]

Decision:
  ◉ Approve & Publish (replaces v3.1 immediately)
  ○ Return with comments

Comments: [___________________________]
```

**Actions:** `[Submit Decision]` `[Cancel]`

---

### Modal 4 — Deprecate Template

```
Deprecate: Fee Collection Audit Checklist v1.0

This template will be marked as deprecated and no longer available for new audits.
Existing audit records that used this template are unaffected.

Reason: [Superseded by v2.3 / No longer applicable / Other ▼]
Replacement Template: [Fee Collection Audit Checklist v2.3 ▼]
```

**Actions:** `[Deprecate]` `[Cancel]`

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Template created | "Branch Physical Inspection Checklist v3.2 created — 87 items" | Success (green) |
| Draft saved | "Template draft saved — Branch Physical Inspection v3.2" | Success (green) |
| Submitted for review | "Checklist submitted to T. Subramaniam for review" | Info (blue) |
| Template approved | "Branch Physical Inspection Checklist v3.2 approved — now live" | Success (green) |
| Template returned | "Checklist returned with 2 comments — review and resubmit" | Warning (amber) |
| Template deprecated | "Fee Collection Audit Checklist v1.0 deprecated — replaced by v2.3" | Info (blue) |
| Checklist outdated | "⚠️ CBSE Affiliation Checklist v1.4 is 6+ months old — review recommended" | Warning (amber) |
| Import successful | "12 templates imported from external file" | Success (green) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No templates | Library bookshelf empty | "No audit templates in the library. Create your first checklist to standardise inspections." | `[+ New Template]` |
| Filter returns zero | Magnifying glass | "No templates match your filters." | `[Reset Filters]` |
| No templates for institution type | Building icon | "No templates found for {institution type}. You may need to create institution-type-specific templates." | `[+ New Template]` |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Template grid | Skeleton cards → populated | < 1s |
| Template detail page | Skeleton sections → populated | < 1s |
| Template editor | Section list + item list skeletons | < 1s |
| Preview render | "Rendering preview…" | < 500ms |
| Version history | Skeleton table → data | < 500ms |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/templates/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | List templates (filterable) | G1+ |
| 2 | GET | `/{template_id}/` | Template detail with all items | G1+ |
| 3 | POST | `/` | Create new template (draft) | 123, 122, 125, 128 |
| 4 | PATCH | `/{template_id}/` | Update template metadata or items | 123, 122, 125, 128 (own domain) |
| 5 | POST | `/{template_id}/submit-review/` | Submit for Audit Head review | 123, 122, 125, 128 |
| 6 | POST | `/{template_id}/approve/` | Approve and publish | 121 |
| 7 | POST | `/{template_id}/return/` | Return with comments | 121 |
| 8 | POST | `/{template_id}/deprecate/` | Deprecate template | 121, G4+ |
| 9 | GET | `/{template_id}/versions/` | Version history | G1+ |
| 10 | POST | `/{template_id}/duplicate/` | Duplicate as new draft | G1+ |
| 11 | GET | `/{template_id}/usage-stats/` | How often used + avg score | G1+ |
| 12 | GET | `/export/` | Export all templates as Excel/ZIP | G1+ |
| 13 | POST | `/import/` | Import templates from file | 121, G4+ |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Template grid load | Page load | `hx-get=".../templates/"` | `#template-grid` | `innerHTML` | — |
| Filter change | Select change | `hx-get` with filters | `#template-grid` | `innerHTML` | Debounced |
| View template | `[View]` click | — | Full page navigate | — | Sub-page |
| Create template | `[+ New Template]` | — | `#modal-content` | `innerHTML` | Modal → redirect to editor |
| Submit for review | Button click | `hx-post=".../templates/{id}/submit-review/"` | `#template-status` | `innerHTML` | Toast + status badge |
| Approve | Button click (121) | `hx-post=".../templates/{id}/approve/"` | `#template-status` | `innerHTML` | Toast + badge → Published |
| Deprecate | Modal confirm | `hx-post=".../templates/{id}/deprecate/"` | `#template-status` | `innerHTML` | Toast + badge → Deprecated |
| Version history | `[Version History]` click | `hx-get=".../templates/{id}/versions/"` | `#version-panel` | `innerHTML` | Side panel |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
