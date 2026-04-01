# Page 16 — Portal Templates

**URL:** `/portal/product/portal-templates/`
**Permission:** `product.manage_portal_templates`
**Priority:** P2
**Roles:** PM Institution Portal, UI/UX Designer, PM Platform

---

## Purpose

Central library for all UI templates, layout presets, and branded page configurations that institutions use to customise the appearance of their portal pages. Covers exam instruction templates, result page layouts, dashboard widget arrangements, email templates, PDF report templates, and landing page themes. The SRAV platform team maintains the master template library; institutions select and optionally customise from it.

Core responsibilities:
- Maintain the master template library for institution-facing portal components
- Provide preview and approval workflow for new templates before publishing
- Track which institutions use which templates and version
- Enable A/B testing of template variants before rolling them out as defaults
- Ensure template changes don't break any institution's live portal
- Version all templates with full rollback capability
- Enforce design system compliance on all published templates
- Support institution-level customisation within defined guardrails

**Scale:**
- 8 template categories · 60+ templates
- 1,950+ institutions using templates
- Any template change can affect hundreds of institutions simultaneously
- Template versions tracked with full history; all versions retained indefinitely
- A/B testing available at institution-type level for new template variants

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Portal Templates"          [New Template]  [Import Template]  │
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 5 cards                                            │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  All Templates · Exam Templates · Result Templates              │
│  Email Templates · PDF Templates · Dashboard Layouts            │
│  Landing Pages · Audit Log                                      │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 5 Cards

| # | Label | Value | Delta | Click Action |
|---|---|---|---|---|
| 1 | Total Templates | Count of active templates across all categories | — | Opens All Templates tab |
| 2 | Institutions Customised | Institutions using at least one non-default template | — | Filters to customised |
| 3 | Pending Review | Templates awaiting QA/design approval | — | Filters to pending |
| 4 | Published This Month | Templates published in last 30 days | — | Opens Audit Log |
| 5 | A/B Tests Active | Templates currently in A/B testing | — | Opens relevant template cards |

---

## Tab 1 — All Templates

### Toolbar
- Search by template name or description
- Category filter: All / Exam / Result / Email / PDF / Dashboard / Landing Page
- Status filter: All / Published / Draft / Under Review / Deprecated / Archived
- Sort: Newest / Most Used / Recently Updated / Alphabetical
- Design system compliance: All / Compliant / Non-Compliant

### Template Grid (3-column card layout)

Each template card shows:

| Field | Detail |
|---|---|
| Thumbnail | Static screenshot of template preview (160px tall, generated on publish) |
| Template Name | Bold, max 40 chars |
| Category | Badge |
| Version | "v1.3" |
| Status | Published (green) · Draft (amber) · Under Review (blue) · Deprecated (grey) |
| Institutions Using | Count (click to see list) |
| Last Updated | Relative date |
| Default | "Default" badge if this is the system-wide default for its category |
| A/B Test | "A/B Active" amber badge if in an active A/B test |
| Design System | ✓ Compliant / ⚠ badge if non-compliant |
| Actions | Preview · Edit · Duplicate · Archive |

Clicking a card thumbnail → opens Template Preview Drawer (800px).
Clicking "Edit" → opens Template Editor Drawer (720px).

### Bulk Actions (when rows selected in list view)

- Deprecate selected templates
- Export template configs as JSON
- Assign to A/B test

### List View Toggle

Toggle between Card Grid (default) and Table View. Table view columns: Name / Category / Version / Status / Institutions Using / Last Updated / Actions.

---

## Tab 2 — Exam Templates

Covers all templates used in the exam-taking interface: instruction screen, question layout, timer display, section navigation, and submission screen.

### Template Sub-categories and Defaults:

| Sub-category | Description | System Default | Can Institutions Customise? |
|---|---|---|---|
| Exam Instructions | Full-screen instructions shown before exam starts | Yes | Yes — logo, colour, intro text |
| Question Layout — MCQ | How MCQ questions are displayed | Yes | No — structure fixed |
| Question Layout — MSQ | Multi-select question display | Yes | No |
| Question Layout — Integer | Integer answer input layout | Yes | No |
| Section Navigation | Left sidebar navigation panel design | Yes | Yes — colour scheme only |
| Timer Display | Countdown timer placement and style | Yes | Yes — position: top / top-right / none |
| Pause Screen | Full-screen shown when exam is paused | Yes | Yes — background colour |
| Submission Screen | Screen shown after "Submit Exam" clicked | Yes | Yes — confirmation message text |
| Result Screen | Immediate result shown post-submission | Yes | Yes — show/hide rank, percentile |
| Proctoring Warning Overlay | Warning shown on suspicious behaviour detection | Yes | No — safety-critical, no customisation |

### Exam Templates Table

| Column | Detail |
|---|---|
| Template Name | With sub-category badge |
| Version | Version number |
| Status | Published / Draft / Under Review |
| Institutions Using | Count |
| A/B Testing | "Active test" badge if in A/B |
| Customisable | Yes / No badge |
| Design System | Compliant / Non-Compliant |
| Last Updated | Date |
| Actions | Preview · Edit · Set as Default · Archive |

### Template Preview Drawer (800px)

Opens when clicking Preview on any exam template.

**Preview Area (top 60% of drawer):**
- Full-width preview frame rendered using the template's HTML/CSS with test data
- Device toggle: Desktop / Tablet / Mobile (iOS) / Mobile (Android)
- Dark / Light mode toggle for preview

**Metadata Panel (bottom 40%):**
- Template name, category, version, created by, last modified
- Description (full text)
- Customisation scope: what institutions can and cannot change
- "Institutions Using This Template" table:
  - Institution name · Type · Plan · Applied Date · Custom variant? (Yes = institution has modified it)

**Action buttons:**
- "Set as Default for All" button: replaces current default for this sub-category for all institutions that haven't customised. Requires confirmation modal showing impact count.
- "View Change History" button → opens version history panel (slide-in right panel within drawer)

---

## Tab 3 — Result Templates

Controls the appearance of result pages shown to students after exam submission, and the print/download result layouts.

### Template Sub-categories:

| Sub-category | Description |
|---|---|
| Immediate Result Page | Score, rank, accuracy shown right after submit |
| Detailed Analysis Page | Section-wise breakdown, topic-wise analysis |
| Leaderboard Page | Ranking view among batch/institution |
| Solution View | Question-by-solution display layout |
| Printable Result Card | A4 print layout for result card |
| Score Card PDF | Downloadable score certificate |
| Progress Report Page | Multi-exam trend view |
| Comparative Analysis | Side-by-side with platform average and batch average |

### Result Template Fields (per template):

Each result template configuration includes:

| Field | Options |
|---|---|
| Score display style | Large numeric / Gauge arc / Both |
| Percentile display | Show overall / Show batch only / Hide |
| Rank display | Show overall rank / Show batch rank / Hide entirely |
| Topic-wise table | Show / Hide |
| Time analytics | Show (time per question) / Hide |
| Comparison bar (vs platform avg) | Show / Hide |
| Motivational message | Custom text per score range: Excellent (≥ 85th percentile) / Good (65–84th) / Needs improvement (< 65th) |
| Share button | Show (WhatsApp / LinkedIn / Download screenshot) / Hide |
| Retake button | Show / Hide |
| Review solutions CTA | Show / Hide |
| Parent/guardian view | Show summary version (student choice) / Show full / Not applicable |
| Institution branding | Full header with logo / Minimal logo / No branding |

### Result Template Customisation Rules

Institutions can customise the following in result templates:
- Motivational message text (per score range)
- Whether to show/hide rank
- Whether to show/hide comparison bars
- Institution name and logo in header

Institutions cannot customise:
- Score calculation display (must show accurate, unadjusted score)
- Percentile methodology (always platform-wide percentile)
- Solutions display structure (locked for academic integrity)

---

## Tab 4 — Email Templates

All transactional and notification email templates used across the platform. Institutions can set their own header/footer branding but cannot change the core email structure.

### Template List

| Template Name | Trigger | Key Variables |
|---|---|---|
| Exam Reminder | 24h before scheduled exam | student_name, exam_name, exam_time, institution_name, portal_link |
| Exam Reminder (1h before) | 1h before exam | student_name, exam_name, minutes_remaining, portal_link |
| Exam Extended | Admin extends duration | student_name, exam_name, new_end_time |
| Exam Cancelled | Admin cancels exam | student_name, exam_name, reason, rescheduled_date |
| Result Published | When results are released | student_name, exam_name, score, rank, result_link |
| New Exam Assigned | When student is assigned to exam | student_name, exam_name, start_date, end_date, portal_link |
| Registration Welcome | After student account creation | student_name, institution_name, login_link, support_email |
| Password Reset | Triggered by forgot password | student_name, reset_link, expiry_time |
| Batch Enrolled | Student added to a batch | student_name, batch_name, faculty_name |
| Fee Receipt | After fee payment | student_name, amount, transaction_id, invoice_link, gst_number |
| Exam Cancelled | Admin cancels a scheduled exam | student_name, exam_name, reason, rescheduled_date |
| Score Certificate | When certificate is generated | student_name, exam_name, score, percentile, download_link |
| Account Suspension | Student account suspended | student_name, reason, appeal_link, support_email |
| Monthly Progress | Monthly digest | student_name, exams_attempted, avg_score, rank_change, dashboard_link |
| Doubt Response | When faculty responds to a doubt | student_name, question_reference, faculty_name, response_preview |
| Subscription Expiring | 30d, 14d, 7d before expiry | admin_name, plan_name, expiry_date, renew_link |
| New Device Login Alert | On login from unknown device | user_name, device, location, timestamp, secure_link |

### Email Template Editor Drawer (640px)

Each email template is edited in a drawer with the following structure:

**Header section:**
- Institution logo placeholder (shown as grey box with "INSTITUTION LOGO" label; auto-replaced at send time)
- Header background colour picker (institution's brand colour)
- Header text colour picker

**Body section:**
- Subject line (editable, supports template variables; max 90 chars)
- Subject preview: shows how subject looks in Gmail / Outlook (with preheader)
- Preheader text (shown in email client preview; max 130 chars)
- Body HTML editor: dual-mode (WYSIWYG / Raw HTML toggle)
- Available components (drag-in): Header block / Body text / Button CTA / Divider / Image / Table / Footer
- Variable insertion button: opens panel listing all `{{ variable }}` names for this template with description and example values
- Character/word count shown in corner

**Footer section:**
- Institution name + address (auto-populated from institution profile; can be overridden)
- Unsubscribe link (mandatory, auto-appended at bottom; cannot be removed — TRAI/CAN-SPAM compliance)
- Social links (optional: Facebook / Instagram / YouTube / LinkedIn — icons shown)

**Test send:**
- "Send Test Email" button → modal asking for email address (default: logged-in admin's email)
- Test email substitutes variables with realistic sample data (student_name → "Arjun Sharma", etc.)
- Preview panel (right half of drawer): rendered HTML email preview updates live as fields are edited; toggle mobile/desktop preview width

---

## Tab 5 — PDF Templates

Controls layout and branding for all downloadable PDF documents generated by the platform.

### PDF Template Types

| Template | Description | Generated By | Frequency |
|---|---|---|---|
| Exam Result PDF | Individual student result with score, analysis, rank | Student or admin | Per exam, per student |
| Score Certificate | Official-looking certificate with institution branding and stamp | Admin | On demand |
| Batch Report PDF | Aggregate batch performance report | Admin | Per exam, per batch |
| Monthly Progress Report | Student's monthly exam summary | Automated (monthly) | Monthly per student |
| Attendance Report | Student/batch attendance summary | Admin | On demand |
| Fee Receipt / Invoice | GST-compliant tax invoice (GSTIN shown) | Automated (post-payment) | Per payment |
| Exam Paper PDF | Question paper download (if allowed by institution) | Admin | On demand |
| Topper List | Institution's top performers for an exam | Admin | Per exam |
| Seat Allotment | Hall ticket / admit card style PDF | Admin | Pre-exam |
| Custom Report | Admin-configured fields and layout | Admin (requires Custom Report Builder feature flag enabled) | On demand |

### PDF Template Configuration (per template)

| Setting | Options |
|---|---|
| Page size | A4 (default) / Letter |
| Orientation | Portrait / Landscape |
| Institution logo position | Top-left / Top-right / Top-center |
| Institution name | Show (large, below logo) / Show (small) / Hide |
| Institution address | Show / Hide |
| Header colour | Colour picker (brand colour) |
| Header text colour | Colour picker |
| Font family | System Default (Noto Sans for Unicode/Hindi support) / Serif / Sans-serif |
| Font size | Normal / Large (for accessibility) |
| Watermark | None / Institution logo (faint, angled) / "CONFIDENTIAL" text / "COPY" text |
| Page footer | Custom text with variables (e.g. "Generated on {{ date }} by SRAV") |
| Page numbers | Show (bottom-center) / Show (top-right) / Hide |
| Digital signature field | Show blank signature line / Hide |
| QR code | None / Verification QR (links to online verification portal) |
| Colour mode | Full colour / Grayscale (for cheaper printing) |
| Margins | Narrow / Normal / Wide |

### PDF Preview Drawer (720px)

- Embedded PDF viewer showing a sample PDF generated with this template
- Sample data used: default student name, sample exam, sample scores
- "Download Sample" button: downloads sample PDF for offline review
- Page navigation: prev/next page if multi-page template
- "Update Template" button → saves settings and regenerates preview

### PDF Generation Infrastructure

PDFs are generated asynchronously using Celery + WeasyPrint / pdfkit. For bulk generation (e.g. 10,000 result PDFs for a large coaching centre's exam result release):
- Batch processing: 100 PDFs per Celery task
- Estimated completion time shown (e.g. "~8 minutes for 10,000 PDFs")
- Email + in-app notification when batch complete with download link
- Batch PDFs zipped per institution; download link valid for 72 hours
- Generated PDFs stored in S3 for 90 days then auto-deleted (DPDPA data minimisation)

---

## Tab 6 — Dashboard Layouts

Defines the widget arrangement options for institution admin dashboards. Institutions pick a layout from the available presets and can reorder widgets within the chosen layout.

### Layout Presets

| Layout Name | Description | Best For | Default For |
|---|---|---|---|
| Analytics-First | Large analytics section at top, quick actions below | Coaching centres with large student base | Coaching Centre |
| Exam-First | Upcoming exams panel dominant, analytics secondary | Schools focused on scheduled exam calendar | School |
| Compact Overview | Dense KPI grid, minimal charts, action-oriented | Small institutions needing quick access | Starter plan |
| Detailed Analytics | Full-width charts, multiple analytics panels | Institutions with analytics-heavy workflow | Enterprise plan |
| Mobile-Optimised | Stacked single-column layout | Institutions primarily using mobile admin access | Mobile users |
| Minimal Clean | Only essential widgets; minimal data | New institutions still in onboarding | First 30 days |

### Widget Library (all configurable widgets)

| Widget | Description | Default Position | Customisable? |
|---|---|---|---|
| KPI Summary Strip | Quick stats: students, exams, avg score, active today | Top | No — always present |
| Upcoming Exams | List of next 5 scheduled exams with time countdown | Top-right | Yes — count: 3/5/10 |
| Recent Results | Latest exam results across all batches | Centre | Yes — filter by batch |
| Active Students (24h) | Students active in last 24 hours as a count + bar | Sidebar | Yes |
| Batch Performance | Top 5 batches by avg score this month | Centre | Yes — sort column |
| Weak Topics | Top 5 most-failed topics platform-wide for this institution | Bottom | Yes |
| Fee Collection Summary | Monthly fee stats (if Finance feature enabled) | Sidebar | Yes — show/hide |
| Announcements Widget | Recent announcements sent to students | Bottom | Yes — count: 3/5 |
| Exam Calendar | Monthly calendar view with exam markers | Centre | Yes |
| Quick Actions | Shortcut buttons for common actions | Top-right | Yes — select 4–6 actions |
| Attendance Summary | Week's attendance percentages by batch | Sidebar | Yes |
| Doubt Queue | Open doubt submissions count with oldest unanswered | Sidebar | Yes |
| Domain Coverage | Domain coverage % heatmap (mini version) | Bottom | Yes |
| Leaderboard Preview | Top 5 students across all exams this month | Sidebar | Yes |

### Widget Configuration

Each widget has a gear icon (PM only) that opens a mini-configuration panel:
- Widget title (rename)
- Data source filter (e.g. "Upcoming Exams" → filter to specific batch or domain)
- Display options (specific to each widget, e.g. chart type: bar / line)
- Refresh interval: inherit global / 30s / 60s / 120s / 5min / manual only

### Layout Editor Drawer (720px)

Opens when editing a layout preset.

- **Grid canvas:** drag-and-drop grid area (12 columns × variable rows). Widgets placed as grid items.
- **Widget sidebar (left):** all available widgets listed with drag-handle. Categorised: Analytics / Exam / Student / Finance / Communication / Quick Access.
- **Widget resize:** each placed widget shows resize handle at bottom-right corner. Minimum 3×1 grid units; maximum 12×4.
- **Preview mode:** "Preview as Institution" button shows the layout as an institution admin would see it with live data from a test tenant (page 22).
- **Responsive preview:** toggle Desktop / Tablet / Mobile to see responsive layout.
- **"Set as Default" panel:**
  - Set as default for institution types: multi-select checkboxes (School / College / Coaching / Group)
  - Set as default for plan tiers: multi-select checkboxes
  - Warning: "This will change the default layout for X institutions. Existing customisations will be preserved."
- **Revert button:** resets canvas to last published state (discards unsaved changes).
- **"Save Draft"** and **"Publish Layout"** buttons. Publish requires confirmation.

---

## Tab 7 — Landing Pages

Manages the pre-login landing page templates that institutions can configure for their portal URL.

### Landing Page Templates

| Template | Description | Use Case |
|---|---|---|
| Clean Minimal | White background, logo, login form centred | Schools and colleges |
| Bold Header | Full-width hero banner with institution photo | Coaching centres with strong brand |
| Stats Showcase | Shows institution's student count, exam count, topper stats | Marketing-oriented landing page |
| Exam Today Banner | Prominently highlights today's upcoming exams | During active exam periods |
| Announcement-First | Latest announcements shown before login form | Institutions that broadcast frequently |
| Dark Premium | Dark background, premium look | High-end coaching brands |

### Landing Page Configuration (per template)

| Setting | Detail |
|---|---|
| Hero banner | Image upload (JPG/PNG, min 1200×400px) or solid colour |
| Institution tagline | Max 100 chars; supports Hindi/regional languages |
| Feature highlights | Up to 4 feature bullet points (optional; with emoji/icon selector) |
| Login box position | Left / Center / Right |
| Login box style | Floating card / Inline / Fullscreen overlay |
| Student count display | Show live count / Show rounded (e.g. "2,000+ students") / Hide |
| Social proof | Show topper names and scores / Show count only / Hide |
| Announcement banner | Show latest announcement above fold / Hide |
| Background image | Full-width / Left panel only / Pattern |
| Footer links | Privacy Policy / Terms / Contact Us / Support (toggle each) |
| Custom CSS | Advanced: institution can add up to 200 chars of CSS overrides (sanitised) |

### Landing Page Preview

Each landing page template has a full-screen preview accessible from the template card. Preview shows:
- Mobile view (375px width)
- Tablet view (768px width)
- Desktop view (1280px width)
- With sample data: institution name, logo, student count, sample announcement

---

## Tab 8 — Audit Log

### Filters
- Date range (default: last 30 days)
- Admin name
- Template name or category
- Action: Created / Published / Deprecated / Set as Default / Archived / Restored / A/B Test Started / A/B Test Winner Declared

### Audit Table

| Column | Detail |
|---|---|
| Timestamp | Full date and time (IST) |
| Admin | Avatar + name + role |
| Action | Colour-coded badge |
| Template | Name + category + version |
| Change Summary | 1-line auto-generated (e.g. "Published v1.3 — adds Hindi question layout") |
| Institutions Affected | Count of institutions whose default changed (shown for Set as Default / Deprecated actions) |
| Rollback | "Rollback to this version" button (creates a new version identical to this one) |

**Pagination:** 25 / 50 / 100. CSV export.

---

## New Template Modal

**Step 1 — Basic Info:**
- Template Name (required, max 60 chars)
- Category (dropdown: Exam / Result / Email / PDF / Dashboard / Landing Page)
- Sub-category (contextual dropdown based on category)
- Description (required, max 300 chars)
- Start from: Blank / Clone existing template (searchable dropdown)

**Step 2 — Assignment:**
- Assigned designer (team member dropdown)
- Target review date (date picker)
- Platform surface: Institution Portal / Student Portal / Admin Portal / All

**Step 3 — Review workflow:**
- Required approvers: auto-populated based on category (UI/UX for visual templates; QA for functional templates; PM for defaults)
- Additional approvers: optional multi-select

After creation: opens Template Editor Drawer for the new template in Draft status.

---

## Template Approval Workflow

All new templates and significant edits go through a review process before publishing:

| Stage | Description | Responsible | Gate Criteria |
|---|---|---|---|
| Draft | PM or designer creates/edits template | PM Institution Portal or UI/UX Designer | None |
| Internal Review | Design review against SRAV design system guidelines | UI/UX Designer | Design system compliance check passed |
| QA Testing | Functional testing on test tenant (page 22) | QA Engineer | No rendering issues across device sizes; no broken variables |
| Approval | PM Platform or PM Institution Portal approves | PM Platform | No blocking issues; content approved |
| Published | Template available to institutions | — | All criteria met |

**Status transitions:**
- Draft → Internal Review: "Submit for Review" button (available to creator)
- Internal Review → QA Testing: "Approve Design" button (UI/UX Designer only). Can also move to "Changes Required" (back to Draft).
- QA Testing → Approval: "QA Passed" button (QA Engineer only). Can also "Fail QA" (back to Draft with failure notes).
- Approval → Published: "Publish Template" button (PM Platform or PM Institution Portal). 2FA required for templates that will be set as a new default.
- Published → Deprecated: "Deprecate" button with mandatory migration path: must specify which replacement template institutions should migrate to.

**Skipping workflow for minor edits:**
If a change is classified as "Minor edit" (e.g. fixing a typo in email template text, updating a URL), PM can publish directly after Draft with abbreviated QA check. Classification is a checkbox on the Edit modal: "This is a minor edit (no structural change)."

---

## Template Versioning

Every published edit creates a new version. Previous versions are retained indefinitely and can be restored.

**Version history panel (within Template Preview Drawer):**
- List of all versions: version number · published date · published by · change summary
- "Compare" button: select two versions → opens side-by-side diff view
  - For email/HTML templates: side-by-side rendered preview (not raw HTML diff)
  - For config-based templates (PDF, Dashboard): table diff showing changed field values
- "Restore" button: creates a new Draft version identical to the selected old version (does not overwrite history; old versions always retained)
- "Mark as Canonical" button: PM can mark a version as the reference/canonical version for documentation purposes

---

## A/B Testing for Templates

For high-impact template changes, A/B testing is available to validate before full rollout.

### How A/B Tests Work

1. PM creates two template variants (Variant A = control, Variant B = challenger)
2. Selects target population: by institution type, plan tier, or specific institution list
3. Sets split: 50/50 (default) or custom (e.g. 10% on Variant B for safer rollout)
4. Sets winning metric: exam completion rate / result page engagement / email open rate / time on page
5. Sets minimum duration: 7 days (default) / 14 days / 30 days
6. A/B test starts: institutions in Variant B group receive the new template

### A/B Test Results

During the test, Analytics tab shows:
- Institutions in Variant A: count + performance metrics
- Institutions in Variant B: count + performance metrics
- Statistical significance: p-value shown. Test marked as significant at p < 0.05.
- Winning condition reached? Yes/No + "Declare Winner" button

When PM clicks "Declare Winner":
- Winner variant becomes the new default for all institutions in the test group
- Loser variant archived
- Results logged with significance data in Audit Log

### A/B Test Guardrails

- Maximum 3 A/B tests active simultaneously across the platform
- Any template in an active A/B test is marked with "A/B Active" badge — edits to these templates are blocked until test concludes or is cancelled
- Cancelling a test reverts all institutions to the previous default (Variant A)

---

## Institution Override Management

Track and manage institutions that use non-default templates.

### Institution Overrides View (within each template's detail)

Accessible from template preview drawer or from the "Institutions Using" count badge:

| Column | Detail |
|---|---|
| Institution Name | Name + type badge + plan badge |
| Template Applied | This template name + version |
| Applied Date | When institution selected this template |
| Customised? | Yes (has institution-level overrides) / No (using template as-is) |
| Customisation Details | If Yes: shows which settings they changed |
| Last Preview | Date institution admin last previewed the template |
| Revert Action | "Revert to Default" button (PM only — force institution back to platform default) |

### Bulk Management

Select multiple institutions → "Apply New Default" → replaces their template with a specified version while preserving their institution-specific customisations if compatible with new version.

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| 4-stage approval workflow | Gate at Design · QA · Approval stages | Templates affect visual UX for thousands of students — quality control critical |
| Version history | All versions retained indefinitely | Enables rollback; documents evolution; compliance audit trail |
| Template preview | Mobile/desktop/tablet toggles + device frames | Institutions use portal across all device types; template must work on all |
| Email test send | Send to logged-in admin | Safe way to verify email rendering without spamming students |
| PDF watermark | Optional "CONFIDENTIAL" | Required by some coaching institutions for exam papers to prevent leaks |
| Widget drag-and-drop | Grid-based layout editor with resize handles | Familiar paradigm; no coding required for PM to configure |
| Landing page templates | 6 presets + config | Covers institution diversity without exposing raw HTML editing (security risk) |
| A/B testing flag | Visible badge on template card; edits blocked | Prevents accidental edits to templates under active A/B test, which would invalidate results |
| Minor edit workflow skip | PM classification override | Full 4-stage workflow for a typo fix is disproportionate; classification-based shortcut balances speed vs quality |
| Custom CSS limit | 200 chars max, sanitised | Allows institutions micro-adjustments (font size, colour) without risking layout breakage or XSS |
| Deprecation requires migration path | Mandatory replacement specification | Prevents institutions from being left with a deprecated template and no upgrade path |
| PDF async generation | Celery batches for bulk | 10,000 PDFs cannot be generated synchronously; Celery queue with progress notification is correct architecture |
| QR verification code on PDFs | Optional per template | Competitive exam coaching centres want verifiable certificates to prevent forgery |
| Template categories locked for functional templates | Proctoring Warning Overlay: no customisation | Safety-critical UI elements (exam integrity) must not vary by institution branding |
