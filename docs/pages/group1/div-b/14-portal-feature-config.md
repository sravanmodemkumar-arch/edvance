# Page 14 — Portal Feature Config

**URL:** `/portal/product/feature-config/`
**Permission:** `product.manage_portal_features`
**Priority:** P1
**Roles:** PM Institution Portal, PM Platform

---

## Purpose

Master control panel for all features exposed in the institution-facing portal. Every capability that school admins, college admins, and coaching centre owners see in their dashboards is gated here before it reaches them. This page governs:

- Which features are available to which plan tiers (Starter / Standard / Professional / Enterprise)
- Which features are restricted to specific institution types (School / College / Coaching / Group)
- Per-institution exceptions (custom overrides beyond their plan)
- Add-on features purchasable separately from the plan
- The complete audit trail of every feature toggle made by any admin

**Scale context:**
- 80+ configurable portal features
- 1,000 schools + 800 colleges + 100 coaching centres + 150 groups = 1,950+ institutions
- 4 plan tiers
- 3 primary institution types + groups
- Changes to plan-level features affect hundreds to thousands of institutions simultaneously
- All changes staged before publish — never instant-apply

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────┐
│  "Portal Feature Config"                                       │
├────────────────────────────────────────────────────────────────┤
│  Staged Changes Banner (amber, shows when unpublished changes exist)│
│  "X feature changes staged — not yet live"    Publish  Discard │
├────────────────────────────────────────────────────────────────┤
│  KPI Strip — 5 cards                                           │
├────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                      │
│  Feature Matrix · Plan Overrides · Institution Overrides       │
│  Config History · Audit Log                                    │
├────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                          │
└────────────────────────────────────────────────────────────────┘
```

---

## Staged Changes Banner

Appears at the top of all tabs when there are unpublished feature changes. Shown in amber background.

**Banner content:**
- Icon: ⚠
- Message: "**X feature changes staged** — Not yet live. Review and publish to apply to all institutions."
- Count updates dynamically as edits are made
- **Publish button** → opens Publish Confirmation Modal (requires 2FA)
- **Discard button** → opens Discard Confirmation Modal

When no pending changes: banner is hidden. When changes are present: banner is sticky (stays visible even while scrolling the tab content).

---

## KPI Strip — 5 Cards

| # | Label | Value | Delta | Click Action |
|---|---|---|---|---|
| 1 | Total Features | Count of all configurable portal features | — | Opens Feature Matrix |
| 2 | Enabled for All | Features enabled across all plan tiers | — | Filters Feature Matrix to "All Tiers" |
| 3 | Plan-Gated | Features restricted to specific tiers | — | Filters Feature Matrix to "Plan-Gated" |
| 4 | Institution Overrides | Count of active per-institution custom settings | — | Opens Institution Overrides tab |
| 5 | Last Published | Timestamp of last config publish + admin name | — | Opens Config History tab |

---

## Tab 1 — Feature Matrix

Primary view. A searchable, filterable matrix of all 80+ portal features mapped against plan tiers and institution types.

### Toolbar

| Control | Options |
|---|---|
| Search | Free-text search on feature name and description |
| Category filter | All / Exam Management / Student Management / Analytics / Communication / Finance / Integrations / Mobile / Reports / AI Features / Settings |
| Status filter | All / Enabled / Plan-Gated / Disabled / Beta / Deprecated |
| Show mode | Show all features / Show differences only (features where plan tiers differ) |
| Edit Mode toggle | Switches matrix from read-only to editable. Shows amber "Edit Mode" badge in header when active. |

### Feature Matrix Table Structure

Rows = features. Columns = plan tiers + institution type gates.

| Column | Detail |
|---|---|
| Feature Name | Full name, with category tag pill and info icon (hover = description) |
| Starter | Toggle or restriction indicator |
| Standard | Toggle or restriction indicator |
| Professional | Toggle or restriction indicator |
| Enterprise | Toggle or restriction indicator |
| School | Institution-type gate toggle (if applicable) |
| College | Institution-type gate toggle (if applicable) |
| Coaching | Institution-type gate toggle (if applicable) |
| Group | Institution-type gate toggle (if applicable) |
| Status | Active / Beta / Deprecated |
| Overrides | Count of institution-level overrides for this feature (clickable — filters Institution Overrides tab) |

**Cell values in read-only mode:**
- ✓ Included — feature is enabled for this tier
- ✗ Not available — feature is disabled for this tier
- Add-on — available as a purchasable add-on for this tier
- — (dash) — not applicable (institution type gate)

**Cell values in edit mode:**
- Toggle switch (on/off)
- "Add-on" checkbox to mark as purchasable add-on
- Staged changes highlight row in amber background
- Dependency warning icon (⚠) if toggling this feature affects others

**Staged change indicator:** Changed rows show a small amber left border and "staged" badge in the row. Changed cells show amber background.

---

### Feature Categories and All Features (80+ total)

#### Exam Management (18 features)

| Feature Name | Description | Default |
|---|---|---|
| Create Practice Exams | Allow institution to create unproctored practice tests | All tiers |
| Create Mock Tests | Full-length mock tests with timer | Standard+ |
| Schedule Live Exams | Set specific date/time for exam delivery | Standard+ |
| Set Exam Password | Password-protect an exam | Standard+ |
| Section-wise Timer | Each section has its own countdown | Professional+ |
| Configure Negative Marking | Set per-question negative marks | All tiers |
| MCQ Questions | Multiple choice, single correct | All tiers |
| MSQ Questions | Multiple select, partial marks | Standard+ |
| Integer Questions | Numeric answer input | Standard+ |
| Custom Question Upload | CSV/manual question entry by institution | Standard+ |
| Show Solutions After Submit | Students see solutions once submitted | All tiers |
| Show Answer Key During Exam | Answer key shown mid-exam | Disabled all |
| Question Shuffle | Randomise question order per student | All tiers |
| Option Shuffle | Randomise option order within questions | Standard+ |
| Proctoring (AI-based) | AI behaviour analysis during exam | Professional+ |
| Webcam Proctoring | Mandatory webcam capture every X seconds | Enterprise / Add-on |
| Full-screen Lock | Force full-screen; detect exit | Professional+ |
| Tab-switch Detection | Alert admin on tab switching | Professional+ |
| Copy-paste Disable | Block clipboard during exam | Standard+ |
| Watermark on Questions | Student name watermark on question text | Professional+ |
| Exam Leaderboard | Live rank updates during exam | Standard+ |

#### Student Management (12 features)

| Feature Name | Description | Default |
|---|---|---|
| Bulk Student Import (CSV) | Import students from spreadsheet | Standard+ |
| Student Groups / Batches | Organise students into named groups | All tiers |
| Student Progress Tracking | Per-student performance over time | Standard+ |
| Individual Student Report | Detailed single-student PDF report | Standard+ |
| Attendance Tracking | Mark and track daily attendance | Standard+ |
| Student Notes | Admin can add notes on student profiles | Standard+ |
| Doubt Submission | Students submit doubts per question | Professional+ |
| Parent Portal Access | Parent login to view child's performance | Professional+ |
| Student Ranking | All-time and exam-wise rank for each student | Standard+ |
| Compare My Performance | Student compares self against batch/platform avg | Standard+ |
| Study Plan Builder | Institution-created structured study schedules | Professional+ |
| Target Exam Selector | Student selects target exam for personalised prep | All tiers |

#### Analytics (10 features)

| Feature Name | Description | Default |
|---|---|---|
| Institution Dashboard | KPI overview for institution admins | All tiers |
| Exam Performance Analytics | Per-exam results, topic breakdown | Standard+ |
| Student-wise Analytics | Filter analytics by individual student | Standard+ |
| Topic-wise Weakness Report | Shows which topics students struggle with | Professional+ |
| Comparative Analytics | Institution vs platform-wide averages | Professional+ |
| Cohort Analysis | Compare batches against each other | Enterprise |
| Predictive Score | ML-based score prediction for each student | Enterprise |
| Time Analytics | Time spent per question, per topic | Professional+ |
| Export Analytics as PDF | Bulk export analytics reports | Standard+ |
| API Access for Analytics | REST API endpoint for data export | Enterprise |

#### Communication (8 features)

| Feature Name | Description | Default |
|---|---|---|
| In-App Announcements | Banner or popup announcements to students | All tiers |
| Email Notifications | System emails (exam reminders, results) | Standard+ |
| SMS Notifications | SMS for exam reminders and results | Professional+ / Add-on |
| WhatsApp Notifications | WhatsApp messages via Meta Business API | Professional+ / Add-on |
| Push Notifications (Mobile) | FCM push to student mobile app | Standard+ |
| Bulletin Board | Pinned notice board visible to all students | Standard+ |
| Broadcast to All Students | Send message to all enrolled students | Standard+ |
| Targeted Announcement | Announce to specific batch or group only | Professional+ |

#### Finance (6 features)

| Feature Name | Description | Default |
|---|---|---|
| Payment Gateway Integration | Collect fees via Razorpay / Stripe | Professional+ |
| Coupon Codes | Create discount coupon codes | Professional+ |
| Course Pricing | Set prices for courses and test series | Professional+ |
| GST Invoice Generation | Automatic GST-compliant invoice generation | Professional+ |
| Refund Management | Process student refund requests | Professional+ |
| Revenue Dashboard | Revenue analytics for institution admin | Professional+ |

#### Integrations (8 features)

| Feature Name | Description | Default |
|---|---|---|
| Google SSO | Login with Google for students | Standard+ |
| Microsoft SSO | Login with Microsoft for students | Standard+ |
| Zoom Integration | Schedule Zoom classes from portal | Professional+ |
| Google Meet Integration | Schedule Google Meet sessions | Professional+ |
| Webhook Support | Send events to external URLs | Enterprise |
| REST API Access | Full institution data API | Enterprise |
| LMS Integration | Connect to Moodle, Canvas, etc. | Enterprise |
| Custom Domain (White-label) | Use institution's own domain | Professional+ |

#### AI Features (6 features)

| Feature Name | Description | Default |
|---|---|---|
| AI Question Generator | Generate questions from topic prompt | Enterprise / Add-on |
| AI Difficulty Predictor | Auto-tag question difficulty | Enterprise |
| AI Weakness Analyser | Identify student weak areas via ML | Enterprise |
| AI Study Plan Recommender | Personalised study schedule using ML | Enterprise |
| AI Doubt Solver | Auto-answer common student doubts | Enterprise / Add-on |
| AI Performance Prediction | Predict final exam score using history | Enterprise |

#### Reports (6 features)

| Feature Name | Description | Default |
|---|---|---|
| Exam Report PDF | Downloadable PDF per exam | Standard+ |
| Batch Performance Report | Aggregate batch results report | Standard+ |
| Monthly Progress Report | Auto-generated monthly summary per student | Professional+ |
| Topper Report | List of top performers per exam | Standard+ |
| Attendance Report | Attendance summary over date range | Standard+ |
| Custom Report Builder | Drag-and-drop report configurator | Enterprise |

#### Mobile (6 features)

| Feature Name | Description | Default |
|---|---|---|
| Mobile App Access | Students can use the SRAV mobile app | All tiers |
| Offline Exam Mode | Download and attempt exams offline | Professional+ |
| Mobile Push Notifications | FCM push via Flutter app | Standard+ |
| Live Exam on Mobile | Attempt scheduled live exams on mobile | Standard+ |
| Video Lectures on Mobile | Watch institution-uploaded videos | Professional+ |
| Biometric Login | Fingerprint / FaceID on mobile | Professional+ |

#### Settings (6 features)

| Feature Name | Description | Default |
|---|---|---|
| Custom Branding | Upload logo, set colours | Standard+ |
| Custom Email Footer | Institution-branded emails | Professional+ |
| Student Self-Registration | Students register without admin invite | Standard+ |
| Multi-language Support | Portal UI in regional languages | Professional+ |
| Custom Timezone | Set institution's local timezone | Standard+ |
| IP Restriction | Restrict portal access to specific IPs | Enterprise |

---

## Tab 2 — Plan Overrides

Manages the feature bundles for each plan tier. Separate from per-institution overrides.

### Plan Summary Cards — 4 cards (Starter / Standard / Professional / Enterprise)

Each card shows:
- Plan name (large text)
- Monthly price and annual price (Decimal — e.g. ₹2,499.00/month)
- Annual savings badge (e.g. "Save ₹5,988 annually")
- Feature count: Included / Add-on / Disabled
- "Edit Plan Features" button → opens Plan Feature Edit Drawer

### Plan Comparison Table

Shows only features where plan tiers differ. Useful for upsell gap analysis.

Columns: Feature Name · Starter · Standard · Professional · Enterprise · Institution Count Affected

Each intersection cell: ✓ Included · ✗ Not available · Add-on (orange badge)

Below table: "Upsell Opportunity" summary:
- "X Standard institutions can unlock Y features by upgrading to Professional"
- "Total ARR opportunity: ₹Z,ZZZ,ZZZ if all Standard institutions upgrade"

### Plan Feature Edit Drawer (560px)

Opens for a specific plan tier. Contains:

**Header:** Plan name + current feature count + "Staged changes: X" badge

**Feature list** grouped by category, each feature as a row:
- Feature name and description
- Toggle: Included / Add-on / Disabled (three-state)
- If changing from Included to Disabled: warning "This removes access for X institutions on this plan"
- If enabling a feature that has a dependency: "Requires: [feature name]" inline note

**Dependency chain warning box** (amber):
When a feature has dependents:
> "Disabling [Feature A] will also affect [Feature B] and [Feature C] which depend on it. Those features will continue to be toggled on but will not function."

**Preview impact panel** (below feature list):
- "If published now: X institutions gain access to Y new features, Z institutions lose access to W features"
- Breakdown by institution count per plan tier

**Buttons:**
- Save Changes (stages changes, does not publish)
- Cancel (discards changes in this drawer)

---

## Tab 3 — Institution Overrides

Per-institution exceptions to the plan defaults. Used for:
- Giving a Standard institution access to a Professional feature as part of a sales deal
- Disabling a feature for a specific institution due to compliance or contract
- Temporary trial overrides (expiry date set)

### Toolbar

| Control | Options |
|---|---|
| Search | Institution name |
| Override type | All / Feature Enabled (above plan) / Feature Disabled (below plan) |
| Institution type | All / School / College / Coaching / Group |
| Plan tier | All / Starter / Standard / Professional / Enterprise |
| Expiry status | All / Active / Expiring Soon (within 7 days) / Expired |

### Override Table — 9 columns

| Column | Detail |
|---|---|
| Institution | Name with type badge |
| Plan Tier | Current plan badge |
| Feature | Feature name with category tag |
| Override Type | Enabled (green badge) or Disabled (red badge) |
| vs Plan Default | Shows what the plan would give vs what the override provides |
| Reason | First 50 chars of reason (hover for full text) |
| Set By | Admin name |
| Set On | Date |
| Expires | Date or "Permanent" |
| Actions | Edit (pencil icon) · Remove (trash icon) |

Rows where expiry is within 7 days: amber row background with clock icon.
Expired rows: grey row background, removed from active computation but still shown in this table.

**Bulk actions:**
- Select multiple rows → "Remove Selected" bulk action

**Pagination:** Showing X–Y of Z overrides · page pills · per-page selector (10 / 25 / 50 / 100)

### "Add Override" Button (top-right of toolbar)

Opens **Add Institution Override Modal** (see Modals section).

---

## Tab 4 — Config History

Full timeline of all published configs. Enables rollback to any previous state.

### History Table

| Column | Detail |
|---|---|
| Published At | Timestamp (date and time) |
| Published By | Admin name with avatar |
| Changes Count | How many features changed in this publish |
| Change Summary | Auto-generated 1-line summary (e.g. "Enabled Proctoring for Professional tier; added 3 institution overrides") |
| Diff | "View Diff" button → opens Diff Drawer |
| Restore | "Restore This Config" button → stages a restore |

**Note on Restore:** Restoring a config does not instantly apply it. It stages all changes needed to return to that config state. The PM then reviews and publishes through the normal Publish flow (with 2FA).

### Diff Drawer (560px)

Opened via "View Diff" on any history row. Shows comparison between the selected historic config and the current live config.

**Three sections:**

**Features Added (green rows):**
- Feature name · Was: Disabled/Not available · Became: Included/Add-on · Affected plans

**Features Removed (red rows):**
- Feature name · Was: Included · Became: Disabled · Affected plans

**Features Changed (amber rows):**
- Feature name · Before → After (e.g. "Standard: Add-on → Included")

**Overrides Changed:**
- Added overrides (green)
- Removed overrides (red)

Footer: "Total institutions affected by this change: X"

---

## Tab 5 — Audit Log

Immutable record of every feature config action. Cannot be edited or deleted.

### Filters

| Filter | Options |
|---|---|
| Date range | Date picker (from – to) |
| Admin | Free-text search by admin name or email |
| Feature | Free-text search by feature name |
| Action type | All / Enable Feature / Disable Feature / Mark as Add-on / Add Override / Remove Override / Published Config / Discarded Changes |

### Audit Log Table — 8 columns

| Column | Detail |
|---|---|
| Timestamp | Full date and time |
| Admin | Name + role badge |
| Action | Coloured badge: Enable (green) · Disable (red) · Add-on (orange) · Override Added (blue) · Override Removed (grey) · Published (indigo) · Discarded (amber) |
| Feature | Feature name + category |
| Target | Plan tier name (e.g. "Professional") or institution name (for overrides) |
| Before | Previous value |
| After | New value |
| IP Address | Admin's IP at time of action |

**Row expand:** Click any row to see full change details including session ID and user agent.

**Pagination:** Showing X–Y of Z entries · page pills · per-page selector (25 / 50 / 100)

**Export:** "Export CSV" button exports the filtered audit log. Includes all 8 columns. Used for compliance audits.

---

## Modals

### Publish Confirmation Modal (requires 2FA)

**Title:** "Publish Feature Config Changes"

**Impact Summary Table:**

| Feature | Change Type | Before | After | Institutions Affected |
|---|---|---|---|---|
| Proctoring (AI) | Plan gate change | Professional ✗ | Professional ✓ | 312 institutions |
| Webcam Proctoring | New Add-on | Enterprise only | Standard Add-on | 847 institutions |
| AI Study Plan | Override added | Disabled | Enabled | 1 institution (Apex Academy) |

**Summary stats:**
- Total institutions gaining features: count
- Total institutions losing features: count
- Add-ons newly available: count

**Confirmation text:** "These changes will be applied immediately to all affected institutions upon publish."

**2FA Field:** "Enter your 6-digit authenticator code"

**Buttons:**
- "Confirm & Publish" (disabled until valid 2FA entered)
- "Cancel" (closes modal, changes remain staged)

---

### Discard Changes Confirmation Modal

**Title:** "Discard Staged Changes?"

**Content:**
- "You have X staged changes. This action permanently discards them and cannot be undone."
- List of changed feature names (max 10 shown, "and X more" if >10)

**Buttons:**
- "Discard All Changes" (red, destructive)
- "Cancel"

---

### Add Institution Override Modal

**Step 1 — Select Institution:**
- Search field with live autocomplete (searches by institution name)
- Selecting an institution shows: Plan tier badge · Institution type · Student count · Current feature status

**Step 2 — Configure Override:**
- Feature selector: searchable dropdown grouped by category
- Once feature selected, shows: Current plan entitlement (e.g. "Not available on Standard plan")
- Override value: Enable (radio) / Disable (radio)
- Reason field: required, max 200 characters
- Expiry: Permanent (radio) / Custom Date (date picker)

**Preview:** Shows before vs after summary once all fields filled.

**Buttons:**
- "Add Override" (stages the override)
- "Cancel"

---

### Edit Institution Override Modal

Same as Add Override Modal but fields pre-filled with existing values. Shows "Last modified by [name] on [date]" in footer.

**Extra field:** "Update Reason" — separate from original reason; logged in audit as amendment reason.

---

## Dependency Chain Rules

Features have declared dependencies. Examples:

| Feature | Depends On | Effect of Disabling Parent |
|---|---|---|
| Exam Reminders | Email Notifications | Exam Reminders break silently |
| Targeted Announcement | Broadcast to All Students | Targeted Announcement inherits broadcast capability |
| Webcam Proctoring | Proctoring (AI-based) | Webcam Proctoring requires AI Proctoring to be enabled first |
| Revenue Dashboard | Payment Gateway Integration | Dashboard shows no data if gateway disabled |
| Custom Report Builder | Export Analytics as PDF | Report builder cannot export without PDF export enabled |
| Google Meet Integration | Calendar Integration | Meeting scheduling requires calendar access |

When editing in Edit Mode:
- Toggling a parent feature OFF shows inline warning: "This will affect [N] dependent features"
- Dependent features remain toggled on in the matrix but render as "⚠ Requires [parent]" in their cell
- PM must consciously acknowledge the warning before saving

---

## Staged Changes System

All edits are staged — never applied live until Published.

**Staged change flow:**
1. PM enters Edit Mode on Feature Matrix or opens Plan Feature Edit Drawer
2. Makes one or more changes (toggles, add-ons, etc.)
3. Each change creates a `StagedFeatureChange` record with: feature, plan/institution target, old value, new value, staged by, staged at
4. Staged Changes Banner appears at top showing count
5. PM clicks "Publish" → review modal → 2FA → publish
6. On publish: all staged changes are atomically applied, a `FeatureConfigSnapshot` record is saved, audit log entries created
7. All staged changes cleared

**Concurrent editing protection:** If two PMs are editing simultaneously, the second PM to publish sees a conflict warning: "Another admin published changes while you were editing. Merge or discard your staged changes."

---

## Custom Domain & Subdomain Policy

**Purpose:** Each of 2,050 institutions gets a portal URL. By default: `{slug}.eduforge.in` (e.g., `narayana.eduforge.in`). Professional+ plan institutions can request a custom domain (e.g., `portal.narayana.com`). PM Institution Portal (Role 7) tracks custom domain requests, their DNS verification status, SSL certificate health, and enforces the plan-tier policy. DNS provisioning and SSL issuance are handled by Engineering (Division C DevOps, Role 14) — PM Portal has read/approve access.

**Why here (page 14) and not in Portal Templates (page 16):** Custom domains are a *plan-tier-gated feature entitlement*, not a template customisation. The feature "Custom Domain (White-label)" is already listed in the Feature Matrix. This section tracks the per-institution workflow for activating that entitlement.

---

### Custom Domain Request Table

| Institution | Plan | Requested Domain | Requested On | DNS Status | SSL Status | Go-Live Status | Actions |
|---|---|---|---|---|---|---|---|
| Narayana Jr College | Enterprise | `portal.narayana.in` | Mar 15 | ✅ Verified | ✅ Active | ✅ Live | [View] |
| Sri Chaitanya Group | Enterprise | `tests.srichaitanya.com` | Mar 18 | ⏳ Awaiting CNAME | 🔄 Pending | ⏳ Pending | [View] [Resend Instructions] |
| Resonance Coaching | Professional | `myportal.resonance.ac.in` | Mar 10 | ✅ Verified | ✅ Active | ✅ Live | [View] |
| DPS Hyderabad | Professional | `dps-hyd.portal.in` | Mar 19 | ❌ Verification failed | — | ❌ Blocked | [View] [Reset] |

**Status columns:**
- **DNS Status:** ✅ Verified (CNAME record pointing to EduForge load balancer confirmed) · ⏳ Awaiting (instructions sent, not yet configured) · ❌ Failed (CNAME incorrect or timeout after 72h)
- **SSL Status:** ✅ Active (Let's Encrypt cert issued) · 🔄 Pending (cert provisioning in progress, ~15 min) · ⚠ Expiring (cert expires < 30 days) · ❌ Error (renewal failed)
- **Go-Live Status:** ✅ Live (institution portal accessible via custom domain) · ⏳ Pending · ❌ Blocked

**SSL Auto-renewal:** Let's Encrypt certificates auto-renew 30 days before expiry via Certbot (managed by DevOps). If renewal fails, PM Portal sees ❌ Error and escalates to Engineering via [Create Engineering Ticket] button.

---

### Custom Domain Detail Drawer (560px)

**Trigger:** [View] in table row

**Section A — Domain Configuration:**
- Institution name (read-only)
- Requested domain (read-only after DNS verified)
- EduForge default URL: `narayana.eduforge.in` (always active as fallback)
- CNAME record to configure: `portal.narayana.in → ingress.eduforge.in`
- Instructions PDF: [Download Setup Guide] (sent to institution IT admin)
- [Resend Instructions Email] → sends DNS setup guide to institution's registered IT contact

**Section B — SSL Certificate:**
- Certificate provider: Let's Encrypt
- Issued: date
- Expires: date · days remaining
- Auto-renewal: Enabled (toggle — PM cannot disable)
- Last renewal attempt: date · status
- [Force Renewal] button (Engineering only — read-only for PM Portal)

**Section C — Traffic Split (migration period):**
During the first 7 days after a custom domain goes live, traffic is served from both `narayana.eduforge.in` and `portal.narayana.in`. After 7 days, EduForge default auto-redirects to custom domain.
- Traffic via default URL (last 7 days): 12% (declining)
- Traffic via custom domain (last 7 days): 88% (rising)
- [Force full cutover now] (PM Portal only · confirmation modal)

**Section C — Subdomain Policy:**

Standard subdomain format: `{institution-slug}.eduforge.in`
- Slug auto-generated from institution name (lowercase, hyphens, max 30 chars)
- PM Portal can override slug via [Edit Slug] (requires confirmation — affects all existing links)
- Slug change: old URL auto-redirects to new URL for 90 days

**Plan-tier subdomain entitlements:**
| Plan | URL format | Custom domain | Subdomain override |
|---|---|---|---|
| Starter | `{slug}.eduforge.in` | ❌ | ❌ |
| Standard | `{slug}.eduforge.in` | ❌ | ❌ |
| Professional | `{slug}.eduforge.in` | ✅ (1 domain) | ✅ |
| Enterprise | `{slug}.eduforge.in` | ✅ (3 domains) | ✅ |

---

### Parent Portal Feature Set

**Purpose:** In school and college portals, parents access a limited subset of features (exam results, attendance, fee status, upcoming exam schedule). This subset is separate from the student and teacher feature sets. PM Institution Portal (Role 7) configures which features are available to parent accounts.

**Parent Feature Matrix** (sub-section of Feature Matrix tab, toggle: [Student View] [Teacher View] [Parent View]):

| Feature | Starter | Standard | Professional | Enterprise | Notes |
|---|---|---|---|---|---|
| View child's exam results | ✅ | ✅ | ✅ | ✅ | Read-only |
| View child's rank in test | ❌ | ✅ | ✅ | ✅ | — |
| Upcoming exam schedule | ✅ | ✅ | ✅ | ✅ | Read-only |
| Attendance view | ❌ | ✅ | ✅ | ✅ | School/College only |
| Fee payment status | ❌ | ❌ | ✅ | ✅ | View only — payment via separate billing |
| WhatsApp result notification | ❌ | ✅ | ✅ | ✅ | DPDPA consent required |
| SMS result notification | ❌ | ✅ | ✅ | ✅ | TRAI DLT template |
| Download result PDF | ❌ | ❌ | ✅ | ✅ | — |
| Multiple child profiles | ❌ | ❌ | ✅ | ✅ | Family with 2+ children at same institution |
| Parent-teacher messaging | ❌ | ❌ | ❌ | ✅ | In-app messaging |

**Institution type scope:** Parent portal features apply to School and College institution types only. Coaching Centres and Institution Groups do not have parent accounts.

**DPDPA compliance note:** Parent accounts can access child data only with the student's (or guardian's) explicit consent. Consent is collected at parent account creation and stored in the institution's tenant schema.

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| Staged changes | Never publish immediately | A single publish affects up to 1,950 institutions; review step prevents accidents |
| 2FA on publish | Always required | Bulk feature change is among the highest-impact admin actions |
| Dependency warnings | Inline in edit mode | Prevents inadvertently breaking dependent features silently |
| Institution overrides | Separate tab from plan matrix | Overrides are exceptions — keeping them separate maintains matrix readability |
| Audit log | Immutable, separate tab | Compliance and accountability for any feature toggle |
| Plan feature edit | Drawer not inline | Full edit context in drawer; matrix remains clean reference view |
| Config history | Full restore capability | Enables rollback if a bad config publish disrupts institutions |
| Expiry dates on overrides | Optional date picker | Supports time-limited trial overrides without manual cleanup |
| Concurrent edit protection | Conflict detection on publish | Prevents one PM silently overwriting another's changes |
| Add-on column | Third state alongside enabled/disabled | Revenue vehicle: features that are not free but not plan-gated |

---

## Amendment G7 — Student Features Tab

**Gap:** No per-plan control over student-facing features. The Feature Matrix only covers institution-admin-facing capabilities (dashboards, reports, bulk tools). Student-facing features (live leaderboard, adaptive recommendations, offline mode, parent sharing) are either always-on or ungated.

### New Tab: "Student Features"

Added to the Tab Bar between `Institution Overrides` and `Config History`.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ STUDENT FEATURES                                [Stage All Changes] [Export CSV]│
│ Per-plan matrix for student-facing capabilities                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Filter: [All Categories ▼]                                                      │
├─────────────────────────────────────────────────┬──────┬───────┬─────┬──────────┤
│ Feature                                         │Start │Growth │ Pro │Enterprise│
├─────────────────────────────────────────────────┼──────┼───────┼─────┼──────────┤
│ EXAM EXPERIENCE                                 │      │       │     │          │
│  Live Leaderboard (during exam)                 │  ❌  │   ✅  │ ✅  │    ✅    │
│  Post-submit detailed solution PDF              │  ❌  │   ✅  │ ✅  │    ✅    │
│  Pause & Resume (non-live exams)                │  ✅  │   ✅  │ ✅  │    ✅    │
│  Night mode / Dark theme                        │  ✅  │   ✅  │ ✅  │    ✅    │
│  Offline mode (downloaded practice tests)       │  ❌  │   ❌  │ ✅  │    ✅    │
│  Text-to-speech for questions                   │  ❌  │   ❌  │ ✅  │    ✅    │
│ ANALYTICS                                       │      │       │     │          │
│  Personal score history dashboard               │  ✅  │   ✅  │ ✅  │    ✅    │
│  Chapter-wise strength/weakness report          │  ❌  │   ✅  │ ✅  │    ✅    │
│  Percentile tracking over time                  │  ❌  │   ✅  │ ✅  │    ✅    │
│  Adaptive study plan (AI-powered)               │  ❌  │   ❌  │ ✅  │    ✅    │
│  Peer comparison (anonymised batch rank)        │  ❌  │   ✅  │ ✅  │    ✅    │
│ SOCIAL & SHARING                                │      │       │     │          │
│  Share result card (image export)               │  ✅  │   ✅  │ ✅  │    ✅    │
│  Achievement badges                             │  ❌  │   ✅  │ ✅  │    ✅    │
│  Study streak tracker                           │  ❌  │   ✅  │ ✅  │    ✅    │
│  Group study rooms (invite peers)               │  ❌  │   ❌  │ ❌  │    ✅    │
│ COMMUNICATION                                   │      │       │     │          │
│  In-app chat with teacher                       │  ❌  │   ❌  │ ✅  │    ✅    │
│  Doubt submission (text/image)                  │  ❌  │   ✅  │ ✅  │    ✅    │
│  Push notification for new exams                │  ✅  │   ✅  │ ✅  │    ✅    │
│  WhatsApp result share                          │  ✅  │   ✅  │ ✅  │    ✅    │
└─────────────────────────────────────────────────┴──────┴───────┴─────┴──────────┘
```

**Toggle behaviour:** Same staged-publish workflow as the main Feature Matrix. Student feature changes do NOT take effect until published. Active exam sessions unaffected until session ends.

**Per-institution override:** Student features can be individually overridden in the `Institution Overrides` tab — same mechanism as portal features.

**Models added:**

```python
class StudentFeature(models.Model):
    """Registry of student-facing features."""
    key = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)  # exam_experience, analytics, social, communication
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)


class StudentFeaturePlanConfig(models.Model):
    PLANS = [('starter','Starter'),('growth','Growth'),('pro','Pro'),('enterprise','Enterprise')]
    STATE = [('enabled','Enabled'),('disabled','Disabled'),('addon','Add-on')]

    feature = models.ForeignKey(StudentFeature, on_delete=models.CASCADE, related_name='plan_configs')
    plan = models.CharField(max_length=20, choices=PLANS)
    state = models.CharField(max_length=10, choices=STATE, default='disabled')
    staged_state = models.CharField(max_length=10, choices=STATE, null=True, blank=True)

    class Meta:
        unique_together = ('feature', 'plan')
```

---

## Amendment G8 — Parent Access Section

**Gap:** No configuration for parent-portal capabilities. Institutions on Pro/Enterprise plans have a parent-facing portal where parents track their child's exam scores, attendance, and receive reports. There is no PM control over what parents can see or whether the parent portal is enabled.

### New Section: "Parent Access" (within Student Features tab)

Positioned as a separate sub-section below the student feature matrix, accessible via anchor `#parent-access`.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PARENT ACCESS CONFIGURATION                       Available: Pro / Enterprise   │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Parent Portal Enabled: [Toggle — ON for Pro, Enterprise / OFF for Starter, Growth]│
│                                                                                 │
│ PARENT PORTAL CAPABILITIES (per plan)                                          │
├─────────────────────────────────────────────────────┬──────┬───────┬─────┬─────┤
│ Capability                                          │Start │Growth │ Pro │Ent. │
├─────────────────────────────────────────────────────┼──────┼───────┼─────┼─────┤
│ View child's exam scores & rank                     │  ❌  │  ❌   │ ✅  │  ✅ │
│ View chapter-wise performance report                │  ❌  │  ❌   │ ✅  │  ✅ │
│ Receive automated SMS/WhatsApp result alerts        │  ❌  │  ❌   │ ✅  │  ✅ │
│ View attendance record                              │  ❌  │  ❌   │ ✅  │  ✅ │
│ Download consolidated progress report (PDF)         │  ❌  │  ❌   │ ❌  │  ✅ │
│ View AI-generated study recommendations for child   │  ❌  │  ❌   │ ❌  │  ✅ │
│ In-app messaging with teacher (parent-initiated)    │  ❌  │  ❌   │ ❌  │  ✅ │
│ View fee payment history & receipts                 │  ❌  │  ❌   │ ✅  │  ✅ │
├─────────────────────────────────────────────────────┴──────┴───────┴─────┴─────┤
│ Parent Account Creation:                                                        │
│  • Auto-invite: Institution admin links parent email to student account        │
│  • Auth: OTP login only (no password) — parent email or mobile                │
│  • Multi-child: One parent account can link up to 5 children                  │
│  • Data scope: Parent sees ONLY their linked child's data — no cross-student   │
│                                                                                 │
│ Parent Notification Settings (institution-configurable):                        │
│  • After every exam: [✅ SMS] [✅ WhatsApp] [❌ Email]                         │
│  • Weekly summary: [✅ SMS] [✅ WhatsApp] [✅ Email]                           │
│  • Low performance alert (score < institution threshold): [✅ All channels]    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Models added:**

```python
class ParentPortalPlanConfig(models.Model):
    PLANS = [('starter','Starter'),('growth','Growth'),('pro','Pro'),('enterprise','Enterprise')]

    plan = models.CharField(max_length=20, choices=PLANS, unique=True)
    portal_enabled = models.BooleanField(default=False)
    capabilities = models.JSONField(
        default=dict,
        help_text='Map of capability_key → enabled boolean'
    )
    staged_capabilities = models.JSONField(null=True, blank=True)


class ParentAccount(models.Model):
    """Parent portal user."""
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20, blank=True)
    institution = models.ForeignKey('institutions.Institution', on_delete=models.CASCADE)
    linked_students = models.ManyToManyField(
        'students.Student',
        through='ParentStudentLink',
        related_name='parents'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)


class ParentStudentLink(models.Model):
    parent = models.ForeignKey(ParentAccount, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    linked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    linked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('parent', 'student')
```

**Security:** Parent auth is OTP-only. Parent session scoped to institution — cannot access another institution's data even if linked student transfers. Parent data is excluded from all PM-level reports; PMs see only aggregate "parent portal active sessions" count.
