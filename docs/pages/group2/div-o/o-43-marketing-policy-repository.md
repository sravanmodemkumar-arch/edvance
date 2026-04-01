# O-43 — Marketing Policy Repository

> **URL:** `/group/marketing/admin/policies/`
> **File:** `o-43-marketing-policy-repository.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary policy author & publisher

---

## 1. Purpose

The Marketing Policy Repository is the single source of truth for every formal policy governing marketing, admissions, and brand operations across all branches of the institution group. In the Indian education market — particularly among large chains operating 20-50 branches across multiple states — the absence of documented, centrally enforced marketing policies creates systemic chaos: one branch offers a 40% fee concession to fill seats while the corporate office caps discounts at 15%; a newly hired branch counsellor promises free transport to every parent because nobody told them the rule was discontinued last year; a franchisee branch puts up a "100% Results Guaranteed" flex banner that violates ASCI (Advertising Standards Council of India) guidelines and triggers a consumer court notice that costs the entire group its reputation.

This page solves six critical problems that every Indian education group faces:

1. **Discount & concession anarchy:** Without a written policy, branch principals and counsellors invent their own concession logic. RTE students, siblings, staff wards, single-parent families, toppers, sports quota, SC/ST/OBC candidates, NRI admissions — each category needs a documented maximum concession percentage, approval authority (branch principal up to 10%, regional head up to 20%, CEO above 20%), and audit trail. A 30-branch group with no discount policy can leak Rs. 50L-2Cr annually in unauthorised concessions.

2. **Brand usage violations:** Branches modify the group logo, use unapproved taglines, print prospectus with outdated information, or create social media posts with incorrect claims. The brand policy defines what is and isn't permitted — approved logo variants, colour codes, tagline versions, mandatory disclaimers, and the consequence of violations.

3. **Referral incentive mismanagement:** Parent referral programmes (Rs. 2,000-5,000 per successful referral) need documented rules: when the incentive becomes payable (after 3 months of enrolment, not at admission), who is eligible (existing parents only, not agents), tax implications (TDS above Rs. 5,000 per year under Section 194R), and the process for claiming the amount. Without documentation, some branches pay cash immediately while others delay 6 months, creating parent dissatisfaction.

4. **Advertising compliance gaps:** Indian education advertising is governed by ASCI guidelines (no misleading claims, no ranking claims without third-party verification, no guarantee of results), DPDPA 2023 (cannot use student photos in ads without verifiable consent), municipal bye-laws (hoarding sizes, permit requirements), and state-specific rules (some states restrict outdoor advertising near highways). A single policy document that every branch acknowledges prevents inadvertent violations.

5. **Social media risk:** A branch social media handler posts a student's photo with their JEE rank without the student's (or parent's, if minor) written consent. Under DPDPA 2023, this is a personal data breach — the Data Protection Board can impose penalties up to Rs. 250 Cr. The social media policy must specify: consent requirement (O-28 Topper Database consent flag), posting approval workflow (drafted by branch → approved by Content Coordinator before publishing), prohibited content (negative competitor mentions, unverified claims, political content), and crisis response protocol.

6. **Vendor and agency guidelines:** Groups working with 5-15 marketing vendors (newspaper agencies, hoarding contractors, digital agencies, WhatsApp API providers, event management companies) need a policy defining vendor empanelment criteria, payment terms, deliverable standards, escalation for delays, and conflict-of-interest declarations.

Every policy document in this repository is version-controlled (v1.0, v1.1, v2.0), has a mandatory acknowledgment workflow (every branch principal and relevant staff must acknowledge reading the policy within 7 days of publication), and links to the Brand Compliance Audit (O-05) for enforcement verification. Policies are categorised, searchable, and retain a full history — no version is ever deleted, only superseded.

**Scale:** 8-25 active policies per group . 5-50 branches requiring acknowledgment . Quarterly policy review cycle . 7-year retention for audit compliance

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — create, edit, publish, archive policies | Primary policy author |
| Group Campaign Content Coordinator | 131 | G2 | Read + Edit drafts — proofread, format, attach templates | Content support; cannot publish |
| Group Admission Data Analyst | 132 | G1 | Read only — view policies, acknowledgment reports | MIS reference |
| Group Admission Telecaller Executive | 130 | G3 | Read — view published policies relevant to telecalling | Must acknowledge discount and referral policies |
| Group Topper Relations Manager | 120 | G3 | Read — view published policies relevant to toppers/PR | Must acknowledge social media and data privacy policies |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve policies before publication; override acknowledgment deadlines | Mandatory approver for Discount and Compliance category policies |
| Branch Principal | — | G3 | Read (published) + Acknowledge — view and acknowledge policies | Filtered to published policies only; acknowledgment tracked |
| Branch Admin | — | G2 | Read (published) + Acknowledge | Support staff acknowledgment |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Policy creation: role 119 or G4+. Publication: role 119 with G4/G5 approval for Discount and Compliance categories; role 119 can self-publish Brand, Advertising, Social Media, Vendor categories. Branch users: read + acknowledge only, filtered to published policies.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Administration  >  Marketing Policy Repository
```

### 3.2 Page Header
```
Marketing Policy Repository                           [+ New Policy]  [Policy Categories]  [Send Reminder]  [Export]
Campaign Manager — Ramesh Venkataraman
Sunrise Education Group . 18 active policies . 4 pending acknowledgment . Last updated: 12 Mar 2026
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Policies | Integer | COUNT(policies) WHERE status = 'published' AND archived = false | Static blue | `#kpi-active` |
| 2 | Pending Acknowledgments | Integer | COUNT(ack_records) WHERE status = 'pending' across all active policies | Amber 1-10, Red > 10, Green = 0 | `#kpi-pending-ack` |
| 3 | Overdue Acknowledgments | Integer | COUNT(ack_records) WHERE status = 'pending' AND due_date < TODAY | Red > 0, Green = 0 | `#kpi-overdue-ack` |
| 4 | Last Policy Update | Date | MAX(published_at) across all policies | Amber > 90 days ago, Red > 180 days ago, Green <= 90 days | `#kpi-last-update` |
| 5 | Policy Compliance % | Percentage | (Total acknowledged / Total required acknowledgments) x 100 across all active policies | Green >= 95%, Amber 80-94%, Red < 80% | `#kpi-compliance` |
| 6 | Draft Policies | Integer | COUNT(policies) WHERE status IN ('draft', 'review') | Amber > 3, static grey otherwise | `#kpi-drafts` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/admin/policies/kpis/"` -> `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **All Policies** — Master list of all policy documents (active, draft, archived)
2. **Acknowledgment Tracker** — Branch-wise acknowledgment status per policy
3. **Version History** — All versions across all policies with diff view
4. **Policy Categories** — Category management and policy coverage overview

### 5.2 Tab 1: All Policies

**Filter bar:** Category (Brand/Discount-Concession/Referral/Advertising/Social Media/Data Privacy/Vendor/Compliance) . Status (Draft/In Review/Published/Archived) . Date range (last updated) . Created by . Search (keyword in title or content)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Policy Title | Text (link) | Yes | Click -> detail drawer; e.g., "Fee Concession & Discount Policy 2025-26" |
| Policy Code | Badge | Yes | Auto-generated: `POL-{CATEGORY_PREFIX}-{NNN}` e.g., `POL-DIS-003` |
| Category | Badge | Yes | Brand (indigo) / Discount (amber) / Referral (emerald) / Advertising (blue) / Social Media (violet) / Data Privacy (red) / Vendor (slate) / Compliance (rose) |
| Version | Text | Yes | v1.0, v1.1, v2.0 — major.minor; major = significant change, minor = clarification |
| Published Date | Date | Yes | Date when current version was published; blank for drafts |
| Effective From | Date | Yes | Date from which the policy is enforceable |
| Valid Until | Date | Yes | Expiry date; blank = no expiry (review-based) |
| Acknowledgment | Progress bar + fraction | Yes | "34/42 branches" with progress bar; green >= 95%, amber 80-94%, red < 80% |
| CEO Approval | Badge | Yes | Required (amber) / Approved (green) / Not Required (grey) — Discount + Compliance categories always require CEO approval |
| Status | Badge | Yes | Draft (grey) / In Review (amber) / Published (green) / Archived (slate) / Expired (red) |
| Actions | Buttons | No | [View] [Edit] [Publish] [Archive] — role-dependent |

**Default sort:** Published Date DESC (most recent first)
**Pagination:** Server-side . 25/page

**Policy status flow:**
```
DRAFT -> IN_REVIEW -> APPROVED -> PUBLISHED -> ARCHIVED
                   \-> REVISION_NEEDED -> DRAFT (re-edit)
                                          EXPIRED (auto, when valid_until < TODAY)
```

### 5.3 Tab 2: Acknowledgment Tracker

**Filter bar:** Policy (dropdown — active published policies) . Branch . Status (Acknowledged/Pending/Overdue) . Role (Principal/Admin/Counsellor)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Branch | Text | Yes | Branch name + city |
| Acknowledger | Text | Yes | Name of person required to acknowledge |
| Role | Badge | Yes | Principal / Branch Admin / Counsellor / Telecaller |
| Policy | Text | Yes | Policy title (if viewing across policies) |
| Sent Date | Date | Yes | When acknowledgment request was sent |
| Due Date | Date | Yes | Acknowledgment deadline (default: 7 days after sent) |
| Acknowledged Date | Date | Yes | When acknowledged; blank if pending |
| Days Overdue | Integer | Yes | Red if > 0; calculated as MAX(0, TODAY - due_date) for pending items |
| Status | Badge | Yes | Acknowledged (green) / Pending (amber) / Overdue (red) |
| Actions | Buttons | No | [Send Reminder] [View Details] |

**Default sort:** Status (Overdue first), then Days Overdue DESC
**Pagination:** Server-side . 50/page

**Acknowledgment rules:**
- When a policy is published, the system auto-creates acknowledgment records for all branch principals and designated branch staff
- Default deadline: 7 days from publication (configurable per policy)
- Acknowledgment requires: checkbox "I have read and understood this policy" + digital signature (typed name)
- Overdue acknowledgments trigger auto-reminders at day 3, day 5, day 7 (escalate to regional head), day 14 (escalate to CEO)
- Re-acknowledgment required when a new version is published (major version change only)
- Branch principals cannot acknowledge on behalf of other branch staff

### 5.4 Tab 3: Version History

**Filter bar:** Policy (dropdown) . Version range . Author

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Policy Title | Text | Yes | Policy name |
| Version | Text | Yes | v1.0, v1.1, etc. |
| Change Type | Badge | Yes | Major (new version) / Minor (clarification) / Amendment (section-level change) |
| Change Summary | Text | No | Author's description of what changed |
| Author | Text | Yes | Who made the change |
| Date | Date | Yes | Version creation date |
| Approved By | Text | Yes | G4/G5 who approved (if applicable) |
| Status | Badge | Yes | Current (green) / Superseded (grey) / Draft (amber) |
| Actions | Buttons | No | [View] [Compare with Previous] [Compare with Current] |

**Default sort:** Date DESC
**Diff view:** Clicking "Compare" opens the version comparison drawer (Section 6.4)

### 5.5 Tab 4: Policy Categories

Overview of all policy categories with coverage and compliance status.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Category | Text | Yes | Category name |
| Active Policies | Integer | Yes | Count of published, non-archived policies in this category |
| Last Updated | Date | Yes | Most recent policy update in this category |
| Acknowledgment Rate | Percentage | Yes | Overall acknowledgment rate across all policies in category |
| CEO Approval Required | Badge | No | Yes (amber) / No (grey) |
| Review Cycle | Text | No | Quarterly / Biannual / Annual |
| Next Review Due | Date | Yes | When the next scheduled review is due |
| Status | Badge | Yes | Up to Date (green) / Review Pending (amber) / Overdue (red) |
| Actions | Buttons | No | [View Policies] [Schedule Review] |

**Policy category definitions:**

| Category | Prefix | Scope | CEO Approval | Review Cycle | Key Contents |
|---|---|---|---|---|---|
| Brand | BRD | Logo usage, colours, fonts, taglines, signage standards | No | Annual | Approved logo variants, colour palette (HEX/Pantone), font families, tagline versions, prohibited modifications |
| Discount & Concession | DIS | Fee concessions, discounts, waivers, scholarships | **Yes** | Biannual | Max concession by category (RTE, sibling, staff ward, topper, sports, SC/ST/OBC, NRI), approval authority matrix, documentation requirements |
| Referral | REF | Parent/alumni/staff referral incentives | **Yes** | Annual | Incentive amount, eligibility, payout timeline, TDS compliance (Section 194R above Rs. 5,000/year), exclusions (agents, brokers) |
| Advertising | ADV | Newspaper, outdoor, digital, print ads | No | Annual | ASCI guidelines compliance, municipal permit requirements, mandatory elements (registration no., contact, disclaimer), prohibited claims |
| Social Media | SOC | Facebook, Instagram, YouTube, WhatsApp posting | No | Biannual | Consent requirements (DPDPA), approval workflow, prohibited content, crisis response, brand voice guidelines |
| Data Privacy | DPR | Student data usage in marketing, DPDPA compliance | **Yes** | Annual | Consent capture, data minimisation, photo usage rules (minor consent via parent), data retention in marketing materials, breach notification |
| Vendor | VND | Marketing agency and vendor management | No | Annual | Empanelment criteria, payment terms (30/60/90 days), deliverable standards, conflict of interest, NDA requirements |
| Compliance | CMP | Regulatory compliance across marketing operations | **Yes** | Quarterly | ASCI, DPDPA, RTE advertising rules, municipal compliance, state-specific advertising restrictions, CERT-In data breach protocol |

---

## 6. Drawers & Modals

### 6.1 Modal: `create-policy` (720px)

- **Title:** "Create New Policy"
- **Fields:**
  - **Metadata:**
    - Policy title (text, required — e.g., "Fee Concession & Discount Policy 2025-26")
    - Category (dropdown, required): Brand / Discount & Concession / Referral / Advertising / Social Media / Data Privacy / Vendor / Compliance
    - Effective from (date, required — cannot be in the past)
    - Valid until (date, optional — blank = no expiry, review-based renewal)
    - Applicable to (multi-select): All Branches / Select specific branches / Select zones
    - Applicable roles (multi-select): Principal / Branch Admin / Counsellor / Telecaller / All Marketing Staff
    - Tags (multi-select free text): e.g., "ASCI", "DPDPA", "GST", "RTE"
    - Linked policies (multi-select from existing policies — for cross-references)
    - Linked audit page (dropdown): O-05 Brand Compliance Audit / None
  - **Content:**
    - Policy body (rich text editor — supports headings, bold, italic, bullet lists, numbered lists, tables, blockquotes)
    - Summary (textarea, max 500 chars — displayed in policy list and acknowledgment request)
    - Key changes from previous version (textarea — auto-displayed in version history; required if this is v1.1+)
  - **Attachments:**
    - Supporting documents (upload — PDF/DOCX, max 10 MB each, max 5 files)
    - Reference templates (e.g., discount approval form, referral claim form)
  - **Acknowledgment settings:**
    - Require acknowledgment (toggle, default ON)
    - Acknowledgment deadline (integer days, default 7, min 3, max 30)
    - Auto-reminder schedule (checkbox): Day 3 / Day 5 / Day 7 (escalate) / Day 14 (CEO escalate)
- **Buttons:** Cancel . Save as Draft . Submit for Review
- **Access:** Role 119 or G4+
- **Validation:** Title must be unique across active policies in the same category; effective date must be >= today

### 6.2 Drawer: `policy-detail` (720px, right-slide)

- **Tabs:** Content . Versions . Acknowledgments . Audit Trail
- **Content tab:**
  - Policy metadata bar: code, category badge, version, effective date, valid until, status
  - Full rendered policy content (rich text)
  - Attachments list with download links
  - Linked policies (clickable)
  - Summary box (highlighted)
  - Tags displayed as badges
- **Versions tab:**
  - List of all versions with date, author, change summary
  - [Compare] button between any two versions
  - Current version highlighted in green
- **Acknowledgments tab:**
  - Branch-wise acknowledgment grid: branch name | acknowledger | status | date
  - Progress bar at top: "34/42 acknowledged (81%)"
  - [Send Reminder to All Pending] button (role 119 or G4+)
  - [Download Acknowledgment Report] button (PDF with signatures)
- **Audit Trail tab:**
  - Every action on this policy: created, edited, submitted, approved, published, acknowledged by [X], reminder sent, archived
  - Timestamp + actor + action + details
- **Footer:** [Edit] [New Version] [Publish] [Send Reminder] [Archive] [Duplicate] — role-dependent

### 6.3 Modal: `acknowledgment-reminder` (480px)

- **Title:** "Send Acknowledgment Reminder"
- **Fields:**
  - Policy (auto-filled — the selected policy)
  - Recipients (multi-select): All Pending / Specific branches / Overdue Only
  - Reminder message (textarea — pre-filled with default: "Please acknowledge the [Policy Title] policy by [Due Date]. Non-acknowledgment will be escalated.")
  - Channel (checkbox): In-App Notification / WhatsApp / Email / All
  - Escalation note (toggle + textarea): Include escalation warning
- **Buttons:** Cancel . Send Reminder
- **Access:** Role 119 or G4+
- **Behaviour:** Sends notification via selected channels; logs reminder in audit trail

### 6.4 Drawer: `version-comparison` (800px, right-slide)

- **Title:** "Policy Version Comparison — [Policy Title]"
- **Layout:** Side-by-side diff view
  - Left panel: Older version (version number + date in header)
  - Right panel: Newer version (version number + date in header)
  - Additions highlighted in green background
  - Deletions highlighted in red background
  - Unchanged sections in normal text
- **Navigation:** Previous/Next change buttons to jump between diff sections
- **Footer:** [Close] [Restore This Version] (G4/G5 only — creates a new version with old content)

### 6.5 Modal: `approval-review` (640px, G4/G5 only)

- **Title:** "Review Policy — [Policy Title] v[X.Y]"
- **Content preview:** Full rendered policy with highlighted changes from previous version
- **Checklist (mandatory for Discount and Compliance categories):**
  - [ ] All concession limits verified against board-approved fee structure
  - [ ] Legal compliance checked (ASCI / DPDPA / RTE / state-specific)
  - [ ] No conflict with existing published policies
  - [ ] Applicable branches and roles correctly scoped
  - [ ] Acknowledgment deadline appropriate
- **Actions:** Approve . Request Revision (with comments) . Reject (with reason)
- **Note:** Approval triggers auto-publish if category does not require CEO approval; for CEO-required categories, approval triggers acknowledgment workflow
- **Access:** G4/G5 only

---

## 7. Charts

### 7.1 Acknowledgment Progress by Policy (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Policy Acknowledgment Progress — Active Policies" |
| Data | Acknowledgment % per active policy |
| X-axis | Percentage (0-100%) |
| Y-axis | Policy name (truncated to 40 chars) |
| Colour | Green >= 95%, Amber 80-94%, Red < 80% (per bar) |
| Reference line | Dashed vertical at 100% target |
| Tooltip | "[Policy]: [X]/[Y] acknowledged ([Z]%)" |
| API | `GET /api/v1/group/{id}/marketing/admin/policies/analytics/acknowledgment-progress/` |

### 7.2 Policy Coverage by Category (Doughnut)

| Property | Value |
|---|---|
| Chart type | Doughnut (Chart.js 4.x) |
| Title | "Active Policies by Category" |
| Data | COUNT active policies per category |
| Colour | Category-specific palette: Brand `#6366F1`, Discount `#F59E0B`, Referral `#10B981`, Advertising `#3B82F6`, Social Media `#8B5CF6`, Data Privacy `#EF4444`, Vendor `#64748B`, Compliance `#F43F5E` |
| Centre text | Total active policy count |
| Tooltip | "[Category]: [N] policies" |
| API | `GET /api/v1/group/{id}/marketing/admin/policies/analytics/by-category/` |

### 7.3 Acknowledgment Trend (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Monthly Acknowledgment Completion Rate — Last 12 Months" |
| Data | Average acknowledgment completion % per month |
| X-axis | Month (Mar 2025 - Mar 2026) |
| Y-axis | Percentage (0-100%) |
| Colour | `#10B981` green line; dashed reference at 95% target |
| Tooltip | "[Month]: [X]% average acknowledgment rate" |
| API | `GET /api/v1/group/{id}/marketing/admin/policies/analytics/acknowledgment-trend/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Policy created | "Policy '[Title]' saved as draft — submit for review when ready" | Success | 3s |
| Submitted for review | "Policy '[Title]' submitted for G4 review" | Success | 3s |
| Approved | "Policy '[Title]' approved — ready for publication" | Success | 4s |
| Published | "Policy '[Title]' v[X.Y] published — acknowledgment requests sent to [N] people across [M] branches" | Success | 5s |
| Revision requested | "Policy '[Title]' needs revision — see reviewer comments" | Warning | 5s |
| Rejected | "Policy '[Title]' rejected by [Approver] — [Reason]" | Error | 5s |
| Acknowledged | "You have acknowledged '[Title]' — thank you" | Success | 3s |
| Reminder sent | "Acknowledgment reminder sent to [N] pending recipients" | Success | 3s |
| New version created | "New version v[X.Y] created for '[Title]' — previous version archived" | Info | 4s |
| Policy archived | "Policy '[Title]' archived — no longer active" | Info | 3s |
| Export generated | "Policy report ready for download" | Success | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No policies created | 📄 | "No Policies Yet" | "Create your first marketing policy to establish brand, discount, and compliance standards across all branches." | New Policy |
| No policies in category | 📂 | "No Policies in [Category]" | "This category has no policies yet. Create one to define rules for [category context]." | New Policy |
| No pending acknowledgments | ✅ | "All Acknowledged" | "Every branch has acknowledged all active policies. Full compliance achieved." | — |
| No versions for comparison | 📋 | "Single Version" | "This policy has only one version. Create a new version to enable comparison." | New Version |
| No results for search/filter | 🔍 | "No Matching Policies" | "Adjust your search terms or filters to find policies." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + filter bar + table skeleton (12 rows) |
| Tab switch | Content skeleton matching target tab structure |
| Policy detail drawer | 720px right-slide skeleton: metadata bar + content block + tabs |
| Create policy modal | Form skeleton with rich text editor placeholder |
| Acknowledgment tracker load | Table skeleton (25 rows) with progress bar placeholders |
| Version comparison drawer | 800px side-by-side skeleton with diff block placeholders |
| Chart load | Grey canvas placeholder with axis labels |
| Send reminder | Spinner: "Sending reminders to [N] recipients..." |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/admin/policies/` | G1+ | List all policies (paginated, filterable by category, status, date) |
| GET | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/` | G1+ | Single policy detail with content and metadata |
| POST | `/api/v1/group/{id}/marketing/admin/policies/` | G3+ | Create new policy (draft) |
| PUT | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/` | G3+ | Update policy (draft only; published policies require new version) |
| DELETE | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/` | G4+ | Delete draft policy (published policies cannot be deleted, only archived) |
| PATCH | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/submit/` | G3+ | Submit policy for G4 review |
| PATCH | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/approve/` | G4+ | Approve policy |
| PATCH | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/reject/` | G4+ | Reject policy (with reason) |
| PATCH | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/revise/` | G4+ | Request revision (with comments) |
| PATCH | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/publish/` | G3+ | Publish approved policy (triggers acknowledgment workflow) |
| PATCH | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/archive/` | G3+ | Archive policy (soft delete — remains in history) |
| POST | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/versions/` | G3+ | Create new version of published policy |
| GET | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/versions/` | G1+ | List all versions of a policy |
| GET | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/versions/{version_id}/` | G1+ | Single version content |
| GET | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/versions/compare/?v1={a}&v2={b}` | G1+ | Diff between two versions |
| GET | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/acknowledgments/` | G1+ | List acknowledgment records for a policy |
| POST | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/acknowledge/` | G2+ | Record acknowledgment (branch staff) |
| POST | `/api/v1/group/{id}/marketing/admin/policies/{policy_id}/remind/` | G3+ | Send acknowledgment reminders |
| GET | `/api/v1/group/{id}/marketing/admin/policies/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/admin/policies/categories/` | G1+ | List policy categories with stats |
| GET | `/api/v1/group/{id}/marketing/admin/policies/analytics/acknowledgment-progress/` | G1+ | Acknowledgment bar chart data |
| GET | `/api/v1/group/{id}/marketing/admin/policies/analytics/by-category/` | G1+ | Category doughnut data |
| GET | `/api/v1/group/{id}/marketing/admin/policies/analytics/acknowledgment-trend/` | G1+ | Monthly acknowledgment trend |
| POST | `/api/v1/group/{id}/marketing/admin/policies/export/` | G1+ | Export policy report (PDF/Excel) |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../admin/policies/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#policies-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdowns/search | `hx-get` with query params | `#policies-table-body` | `innerHTML` | `hx-trigger="change"` for dropdowns; `hx-trigger="keyup changed delay:300ms"` for search |
| Policy detail drawer | Row click | `hx-get=".../admin/policies/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create policy | Form submit | `hx-post=".../admin/policies/"` | `#create-result` | `innerHTML` | Rich text content serialised as HTML |
| Submit for review | Button click | `hx-patch=".../admin/policies/{id}/submit/"` | `#status-badge-{id}` | `innerHTML` | Inline badge update |
| Approve policy | Approval form | `hx-patch=".../admin/policies/{id}/approve/"` | `#approval-result` | `innerHTML` | Toast + status update |
| Publish policy | Publish button | `hx-patch=".../admin/policies/{id}/publish/"` | `#policy-row-{id}` | `outerHTML` | Full row refresh (status + acknowledgment count update) |
| Acknowledge | Acknowledge form | `hx-post=".../admin/policies/{id}/acknowledge/"` | `#ack-result` | `innerHTML` | Checkbox + typed name; toast on success |
| Send reminder | Reminder form | `hx-post=".../admin/policies/{id}/remind/"` | `#reminder-result` | `innerHTML` | Spinner during send |
| Version compare | Compare button | `hx-get=".../admin/policies/{id}/versions/compare/?v1={a}&v2={b}"` | `#comparison-drawer` | `innerHTML` | Opens 800px drawer |
| Acknowledgment tracker | Tab 2 load | `hx-get=".../admin/policies/{id}/acknowledgments/"` | `#ack-tracker-body` | `innerHTML` | `hx-trigger="click"` on tab |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#policies-table-body` | `innerHTML` | 25/page for policies; 50/page for acknowledgments |

---

*Page spec version: 1.0 . Last updated: 2026-03-26*
