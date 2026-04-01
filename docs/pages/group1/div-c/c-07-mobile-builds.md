# C-07 — Mobile Build Pipeline

> **Route:** `/engineering/mobile-builds/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · Mobile Engineer — Flutter (Role 13)
> **Read Access:** DevOps/SRE (Role 14)
> **File:** `c-07-mobile-builds.md`
> **Priority:** P2
> **Status:** ⬜ Amendment pending — G28 (FCM Delivery Monitor tab)

---

## 1. Page Name & Route

**Page Name:** Mobile Build Pipeline
**Route:** `/engineering/mobile-builds/`
**Part-load routes:**
- `/engineering/mobile-builds/?part=kpi` — build health KPI strip
- `/engineering/mobile-builds/?part=builds` — build list table (iOS + Android)
- `/engineering/mobile-builds/?part=drawer&build_id={id}` — build detail drawer
- `/engineering/mobile-builds/?part=signing` — code signing management panel
- `/engineering/mobile-builds/?part=store-tracker` — App Store / Play Store submission tracker
- `/engineering/mobile-builds/?part=crashlytics` — Crashlytics crash analysis panel

---

## 2. Purpose (Business Objective)

The Mobile Build Pipeline page gives Mobile Engineers and DevOps complete visibility and control over the Flutter mobile app's CI/CD cycle — from code push through build, sign, test, beta distribution, and App Store/Play Store release. With 3M+ app installs on iOS and Android, every release must be managed with precision: incorrect provisioning profiles or keystore issues cause silent failures in production that can take days to diagnose.

Crashlytics integration on this page closes the feedback loop — engineers can see crash-free rate and ANR trends immediately after a release and decide within hours whether to push a hotfix or roll forward.

**Business goals:**
- Track all Flutter build jobs (iOS + Android) across GitHub Actions
- Manage iOS provisioning profiles and Android keystore securely
- Track App Store Connect and Google Play submission lifecycle
- Distribute beta builds to institutions via Firebase App Distribution
- Monitor crash-free rate post-release and act within hours on critical crashes

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full access all sections |
| Mobile Engineer (13) | Level 4 | Full: builds · signing · store submission · crashlytics · beta distribution |
| DevOps / SRE (14) | Level 4 — Read | View build status and logs; cannot trigger builds or manage signing |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Build Status

**Purpose:** Current build health for both platforms at a glance.

**Header elements:**
- H1 "Mobile Build Pipeline"
- Platform tabs: iOS | Android | Both (default: Both)
- Current version badges:
  - iOS: "v3.8.1 (Build 421) — Live on App Store · 3 days ago"
  - Android: "v3.8.1 (Build 421) — Live on Play Store · 3 days ago"
- "Trigger Build" button (Mobile Engineer · DevOps) — opens trigger modal
- Global crash-free rate badge: "Crash-free: 99.2% iOS · 99.4% Android" — colour: green > 99% · amber 98–99% · red < 98%

**Edge Cases:**
- Crash-free rate drops below 95%: red pulsing badge + "CRITICAL: Crash rate exceeds threshold. Immediate hotfix review required."

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Latest Build Status | Last build outcome: ✅ Success / ❌ Failed / 🔄 Running | Failed = red |
| Crash-Free Rate (iOS) | % from Crashlytics (last 7 days) | < 99% amber · < 95% red |
| Crash-Free Rate (Android) | % from Crashlytics (last 7 days) | < 99% amber · < 95% red |
| App Store Version | Live version on App Store | Mismatch with latest build = amber |
| Play Store Version | Live version on Play Store | Mismatch = amber |
| Beta Testers Active | Firebase App Distribution active testers | — |

---

### Section 3 — Build List Table

**Purpose:** Full history of all Flutter build jobs for iOS and Android.

**Table Columns:**

| Column | Description | Sortable |
|---|---|---|
| Platform | iOS 🍎 / Android 🤖 badge | ✅ |
| Build Number | Auto-incremented (e.g., Build 422) | ✅ |
| Version | Semantic version (e.g., v3.8.2) | ✅ |
| Git Branch | Branch that triggered the build | — |
| Git Commit | Short SHA (link to GitHub) | — |
| Status | ✅ Success · ❌ Failed · 🔄 Running · ⏸ Queued · 🚫 Cancelled | ✅ |
| Stage | Checkout · Test · Build · Sign · Upload · Submitted | — |
| Duration | Total build time (hh:mm:ss) | ✅ |
| Triggered By | Engineer name or "Auto (push)" | — |
| Distribution | Beta (Firebase) · TestFlight · Play Internal · Production | — |
| Signed | ✅ Signed · ❌ Not signed · — N/A | — |
| Started At | Timestamp | ✅ |

**Row Colour Rules:**
- Failed: red left border
- Running: blue pulsing left border
- Latest successful production build: green highlight

**Filter Bar:**
- Platform: All / iOS / Android
- Status: All / Success / Failed / Running
- Distribution: All / Beta / Production
- Branch: All / main / release/* / hotfix/*
- Date range picker

**Data Flow:**
- Build data from `platform_mobile_builds` table (populated by GitHub Actions webhook on job completion)
- Running builds: polled from GitHub Actions API every 30s
- Table refresh: 30s HTMX poll (guard: no drawer open)

---

### Section 4 — Build Detail Drawer

**Purpose:** Full detail for a single build job.

**Drawer Width:** 640px
**Tabs:**

---

#### Tab 1 — Build Stages

**Purpose:** Step-by-step build pipeline status with timing per stage.

**Stages (iOS example):**

| Stage | Status | Duration | Notes |
|---|---|---|---|
| Checkout | ✅ | 0:12 | Commit abc123 |
| Dart/Flutter Analysis | ✅ | 1:24 | 0 errors · 3 warnings |
| Unit Tests | ✅ | 2:11 | 847 tests passed |
| Widget Tests | ✅ | 0:58 | 142 tests passed |
| Integration Tests | ✅ | 8:30 | On Firebase Test Lab |
| Build IPA | ✅ | 12:45 | Release mode · arm64 |
| Code Signing | ✅ | 0:23 | Provisioning profile: MockTest_Production_2026 |
| Upload to TestFlight | ✅ | 2:10 | Build 421 visible in TestFlight |
| dSYM Upload | ✅ | 0:31 | Symbol file uploaded to Crashlytics |

**Stages (Android example):**

| Stage | Status | Duration | Notes |
|---|---|---|---|
| Checkout | ✅ | 0:10 | |
| Analysis | ✅ | 1:18 | |
| Unit Tests | ✅ | 1:54 | |
| Widget Tests | ✅ | 0:52 | |
| Build APK/AAB | ✅ | 9:20 | Release AAB for Play Store |
| Keystore Signing | ✅ | 0:08 | Keystore: mocktest-release.jks |
| ProGuard/R8 | ✅ | 3:12 | Obfuscation applied |
| Upload to Play Console | ✅ | 1:45 | Internal testing track |
| ProGuard Mapping Upload | ✅ | 0:22 | Uploaded to Crashlytics |

**Failed stage behaviour:** Failed stage shown in red; subsequent stages shown as "Skipped" in grey; failed stage expands to show error message

---

#### Tab 2 — Build Logs

**Purpose:** Full GitHub Actions log for this build.

**Display:**
- ANSI-colour log output (green for success lines, red for errors, yellow for warnings)
- Stage filter: dropdown to jump to log section for specific stage
- Search within logs: Ctrl+F style search (client-side)
- "Download full log" button (plain text download)
- Log auto-scrolls to first error if build failed

**Data Flow:**
- Logs fetched from GitHub Actions API `GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs/{job_id}/logs`
- Stored in `platform_mobile_build_logs` S3 prefix after build completion (GitHub Actions log retention = 90 days)
- Logs for builds > 90 days old: served from S3

---

#### Tab 3 — Artifacts

**Purpose:** Build output files and their distribution status.

**Artifact Table:**

| Artifact | Size | Type | Status | Distributed To | Download |
|---|---|---|---|---|---|
| MockTest_3.8.1_421.ipa | 84 MB | iOS App | ✅ Uploaded | TestFlight | — (App Store only) |
| MockTest_3.8.1_421.aab | 62 MB | Android Bundle | ✅ Uploaded | Play Internal | — |
| MockTest_3.8.1_421.apk | 91 MB | Android APK | ✅ Built | Firebase Beta | ⬇ Download |
| MockTest_3.8.1_421.dSYM | 12 MB | Debug Symbols (iOS) | ✅ Uploaded | Crashlytics | ⬇ Download |
| ProGuard_3.8.1_421.zip | 2 MB | Mapping (Android) | ✅ Uploaded | Crashlytics | ⬇ Download |

**Notes:**
- IPA download not available (Apple DRM; only via TestFlight)
- AAB download not available (Play Store only)
- APK download available for direct beta installation
- dSYM and ProGuard mapping files downloadable for local symbolication

---

#### Tab 4 — Store Submission

**Purpose:** Track this build's submission status on App Store Connect and Google Play Console.

**iOS — TestFlight / App Store:**

| Step | Status | Timestamp |
|---|---|---|
| Uploaded to TestFlight | ✅ | 3 days ago |
| Processing (Apple) | ✅ | 3 days ago (~25 min) |
| TestFlight internal testing | ✅ Active | 3 days ago |
| TestFlight external testing | ✅ Active | 2 days ago |
| Submitted for App Review | ✅ | 1 day ago |
| App Review | ✅ Approved | 6 hours ago |
| Released to App Store | ✅ | 3 hours ago |

**Android — Play Console:**

| Step | Status | Timestamp |
|---|---|---|
| Uploaded to Internal Testing | ✅ | 3 days ago |
| Internal Testing | ✅ Active | 3 days ago |
| Promoted to Alpha | ✅ | 2 days ago |
| Promoted to Beta | ✅ | 1 day ago |
| Promoted to Production (100%) | ✅ | 3 hours ago |

**Actions (Mobile Engineer):**
- "Promote to next track" (Android — moves build up the track ladder)
- "Submit for App Review" (iOS)
- "Halt rollout" (Android — pauses production rollout at current percentage)
- "Increase rollout percentage" (Android — staged rollout: 10% → 25% → 50% → 100%)

---

### Section 5 — Code Signing Management

**Purpose:** Manage iOS provisioning profiles, certificates, and Android keystores — the most security-sensitive assets in the mobile pipeline.

**Access:** Mobile Engineer · Platform Admin · (DevOps: read-only)

**Layout: Two sub-sections**

---

#### iOS Signing Sub-section

**Active Certificates:**

| Certificate | Type | Expiry | Status | Fingerprint |
|---|---|---|---|---|
| MockTest Distribution | Apple Distribution | Aug 2027 | ✅ Valid | `XX:XX:XX:XX` |
| MockTest Development | Apple Development | Aug 2026 | ✅ Valid | `YY:YY:YY:YY` |
| Apple WWDR Intermediate | CA Cert | Feb 2030 | ✅ Valid | System |

**Expiry alerts:** 90-day warning (amber) · 30-day warning (red) · Daily email to Mobile Engineer after 30-day mark

**Provisioning Profiles:**

| Profile Name | Type | Expiry | Bundle IDs | Status |
|---|---|---|---|---|
| MockTest_Production_2026 | App Store Distribution | Dec 2026 | `in.platform.mocktest` | ✅ Active |
| MockTest_Development_2026 | Development | Dec 2026 | `in.platform.mocktest` | ✅ Active |
| MockTest_Beta_2026 | Ad Hoc | Dec 2026 | `in.platform.mocktest` | ✅ Active |

**Actions:**
- "Upload new provisioning profile" (.mobileprovision file)
- "Renew certificate" — instructions link to Apple Developer Portal (cannot be done in-platform; external action required)
- "Download profile" — .mobileprovision file download (Mobile Engineer only)
- "Delete expired profile" (confirmation required)

**Storage:** Provisioning profiles and certificates stored encrypted (AES-256) in AWS Secrets Manager; referenced by GitHub Actions workflow via secrets injection at build time.

---

#### Android Signing Sub-section

**Active Keystores:**

| Keystore | Alias | Key Algorithm | Key Size | Expiry | Status |
|---|---|---|---|---|---|
| mocktest-release.jks | mocktest-release | RSA | 4096 | 2050 | ✅ Active |

**Note:** Android keystores for Play Store have very long validity (25+ years recommended by Google). The expiry shown is Google's "keys never expire" convention; most keystores are valid indefinitely.

**Actions:**
- "View keystore metadata" (MD5/SHA-1/SHA-256 fingerprints — for Google Play app signing setup)
- "Rotate keystore" — generates new keystore, uploads to Secrets Manager (requires dual Mobile Engineer approval — losing keystore = losing ability to update the app on Play Store)

**Keystore security:**
- Keystore file NEVER displayed or downloadable from this UI
- Only fingerprints and metadata shown
- Keystore reference (Secrets Manager ARN) injected into GitHub Actions at build time
- Rotation requires: Mobile Engineer + Platform Admin 2FA + written justification

**App Signing by Google (Play App Signing):**
- Status: ✅ Enrolled (Google holds the upload key)
- Upload key fingerprint shown (for verification)
- Note: App Signing by Google means actual signing key is with Google; keystore managed here is the upload key only

---

### Section 6 — Firebase App Distribution (Beta)

**Purpose:** Track and manage beta builds distributed to institution testers via Firebase App Distribution.

**Layout:**

**Active Beta Release:**
- Current beta version: v3.9.0-beta.2 (Build 425)
- Testers: 142 active
- Download rate: 89% (126/142 have downloaded)
- Crash-free rate (beta): 98.1%

**Beta Tester Groups:**

| Group | Count | Type | Last Release Sent |
|---|---|---|---|
| Platform Internal | 12 | Staff | 1 day ago |
| Partner Institutions | 85 | External testers | 1 day ago |
| Coaching Centers Beta | 30 | External testers | 1 day ago |
| QA Automation | 15 | Automated test devices | 1 day ago |

**Actions:**
- "Distribute new build to beta" — selects build from list + tester groups + release notes
- "Add testers" — email input (individual or CSV upload)
- "Remove tester" — removes from all groups; stops future distributions
- "View feedback" — Firebase console deep-link (in-app feedback from beta users)

**Release Notes editor:**
- Rich text editor for beta release notes (shown in Firebase notification to testers)
- Multi-language: EN (required) · HI (optional)
- Character limit: 500 per language

---

### Section 7 — Crashlytics Crash Analysis Panel

**Purpose:** Post-release crash monitoring — the first place Mobile Engineers check after a production release.

**Platform selector:** iOS | Android | Both

**Overview Stats (last 7 days):**

| Metric | iOS | Android |
|---|---|---|
| Crash-free sessions | 99.2% | 99.4% |
| Total crashes | 4,821 | 3,204 |
| Affected users | 1,840 | 1,210 |
| ANR rate (Android) | — | 0.08% |
| Crash-free (last release only) | 99.1% (v3.8.1) | 99.5% (v3.8.1) |

**Critical Threshold Alerts:**
- Crash-free < 99%: amber banner "Crash rate exceeds threshold. Review top crashes immediately."
- Crash-free < 95%: red banner + auto-notification to Mobile Engineer + Platform Admin + C-18 incident created

**Top Crashes Table:**

| # | Issue Title | Crash Count (7d) | Affected Users | First Seen | Last Seen | Version | Status |
|---|---|---|---|---|---|---|---|
| 1 | NullPointerException in ExamTimerWidget | 1,842 | 720 | v3.8.0 | v3.8.1 | 🔴 Not fixed | |
| 2 | SocketException on result fetch | 923 | 412 | v3.8.1 | v3.8.1 | 🟡 In review | |
| 3 | Hive encryption key missing on cold start | 412 | 198 | v3.7.2 | v3.8.1 | 🟢 Fixed in v3.9.0 | |

**Per-crash row:**
- Click → opens crash detail drawer (stack trace · affected device models · OS versions · breadcrumbs leading to crash)
- "Mark as fixed in version" — sets expected fix version (Crashlytics will auto-close if crash disappears in that version)
- "Link to GitHub issue" — URL input (cross-reference with GitHub issue tracker)

**Device & OS Breakdown:**
- Pie chart: affected device manufacturers (Samsung · OnePlus · Xiaomi · Apple · Others)
- Bar chart: affected OS versions (Android 12/13/14/15 · iOS 16/17/18)
- Heatmap: crash rate by device model × OS version combination

**Version Comparison Chart:**
- Line chart: crash-free rate by app version (last 8 releases)
- Helps identify if a regression was introduced in a specific release

**Data Flow:**
- Crashlytics data via Firebase REST API (Management API + Crashlytics Data API)
- Data cached in Memcached 10 min (Crashlytics API has rate limits)
- Crash-free rate alerts evaluated by Celery beat every 30 min

---

### Section 8 — dSYM / ProGuard Symbol Registry

**Purpose:** Track upload status of debug symbol files — required for human-readable crash reports in Crashlytics.

**Table:**

| Version | Platform | File Type | Size | Uploaded At | Crashlytics Status |
|---|---|---|---|---|---|
| v3.8.1 | iOS | dSYM | 12 MB | 3 days ago | ✅ Processed |
| v3.8.1 | Android | ProGuard mapping | 2 MB | 3 days ago | ✅ Processed |
| v3.8.0 | iOS | dSYM | 11.8 MB | 12 days ago | ✅ Processed |
| v3.7.9 | iOS | dSYM | 11.5 MB | 25 days ago | ✅ Processed |

**Critical:** If dSYM/ProGuard not uploaded, Crashlytics shows obfuscated crash reports — useless for debugging.

**Missing symbol alert:** If a production build has `Crashlytics Status = ❌ Missing`: red banner "dSYM not uploaded for v{n} iOS — crash reports are not symbolicated. Upload now."

**Manual upload:** "Upload dSYM" / "Upload ProGuard mapping" file picker buttons (for emergency manual uploads if CI/CD symbol upload step failed)

---

## 5. User Flow

### Flow A — Release New Version to Production

1. Mobile Engineer triggers build from GitHub (or from "Trigger Build" button on page)
2. Build pipeline starts: Checkout → Tests → Build → Sign → Upload
3. Build List shows new row: iOS Build 425 · Running · Stage: "Build IPA"
4. After ~25 min: ✅ Success · Uploaded to TestFlight
5. Mobile Engineer opens drawer → Store Submission tab → "Submit for App Review"
6. Apple processes (1–3 days): status updates show in drawer
7. App approved: "Released to App Store" status
8. KPI strip: App Store Version updates to v3.9.0
9. Crashlytics panel shows v3.9.0 crash data after first users update

### Flow B — Hotfix After Crash Spike

1. Crashlytics panel: crash-free rate drops to 97.1% (amber banner)
2. Top crash: NullPointerException in ExamTimerWidget — 1,842 crashes in 1 hour
3. Mobile Engineer reviews crash detail in drawer: stack trace points to v3.8.1 change
4. Pushes hotfix commit → triggers build automatically via GitHub Actions
5. Build list: iOS Build 426 + Android Build 426 · Running
6. After build: distributed to beta (Firebase) first
7. Beta crash-free: 99.8% — hotfix working
8. Submits iOS for expedited review; Android promoted to production immediately
9. Platform Admin notified via C-18 incident auto-created at crash spike

### Flow C — Provisioning Profile Expiry

1. Code Signing panel: "MockTest_Production_2026" provisioning profile expiring in 30 days (red badge)
2. Mobile Engineer receives email notification
3. Navigates to Code Signing → iOS section
4. Clicks "Renew certificate" → follows instructions to Apple Developer Portal
5. Downloads renewed profile → "Upload new provisioning profile"
6. Old profile deleted
7. Next build automatically uses new profile (GitHub Actions reads from Secrets Manager)

---

## 6. Component Structure (Logical)

```
MobileBuildPipelinePage
├── PageHeader
│   ├── PageTitle
│   ├── PlatformTabs (iOS / Android / Both)
│   ├── CurrentVersionBadges (iOS + Android)
│   ├── TriggerBuildButton
│   └── CrashFreeRateBadge
├── KPIStrip
│   └── KPICard × 6
├── BuildListTable
│   ├── FilterBar
│   └── BuildRow × N
│       └── (all columns)
├── BuildDetailDrawer (640px)
│   └── DrawerTabs
│       ├── BuildStagesTab
│       ├── BuildLogsTab
│       ├── ArtifactsTab
│       └── StoreSubmissionTab
├── CodeSigningPanel
│   ├── iOSSigningSection
│   │   ├── CertificatesTable
│   │   └── ProvisioningProfilesTable
│   └── AndroidSigningSection
│       └── KeystoresTable
├── FirebaseBetaDistribution
│   ├── ActiveBetaCard
│   ├── TesterGroupsTable
│   └── DistributeModal
├── CrashlyticsPanel
│   ├── PlatformSelector
│   ├── OverviewStats
│   ├── CriticalAlertBanner (conditional)
│   ├── TopCrashesTable
│   ├── DeviceOSBreakdown
│   └── VersionComparisonChart
└── SymbolRegistryTable
```

---

## 7. Data Model (High-Level)

### platform_mobile_builds

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| platform | ENUM | ios/android |
| build_number | INTEGER | auto-increment per platform |
| version | VARCHAR(20) | semver |
| git_branch | VARCHAR(100) | |
| git_sha | CHAR(40) | |
| status | ENUM | queued/running/success/failed/cancelled |
| current_stage | VARCHAR(50) | |
| duration_seconds | INTEGER | nullable |
| triggered_by | UUID FK → platform_staff | nullable (null = auto) |
| distribution_target | ENUM | beta/testflight/play_internal/production |
| is_signed | BOOLEAN | |
| github_run_id | BIGINT | |
| github_job_id | BIGINT | |
| started_at | TIMESTAMPTZ | |
| completed_at | TIMESTAMPTZ | nullable |
| artifacts | JSONB | `[{name, size, type, url}]` |

### platform_mobile_signing_assets

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| platform | ENUM | ios/android |
| asset_type | ENUM | certificate/provisioning_profile/keystore |
| name | VARCHAR(100) | |
| expiry_date | DATE | nullable |
| fingerprint | VARCHAR(200) | |
| secrets_manager_arn | VARCHAR(512) | actual file stored here |
| is_active | BOOLEAN | |
| uploaded_by | UUID FK → platform_staff | |
| uploaded_at | TIMESTAMPTZ | |

---

## 8. Validation Rules

| Field | Rule |
|---|---|
| Provisioning profile upload | Must be .mobileprovision format · must not be expired · bundle ID must match `in.platform.mocktest` |
| Keystore rotation | Requires Mobile Engineer + Platform Admin both provide 2FA · justification min 100 chars (high-risk: losing keystore = losing app update ability) |
| Beta release notes | Required in English · max 500 chars · HTML not allowed |
| Beta tester email | Valid email format · cannot add more than 10,000 testers (Firebase limit) |
| Build trigger | Only from branches matching `main`, `release/*`, `hotfix/*` via normal flow; other branches blocked unless Mobile Engineer confirms |
| Manual dSYM upload | Must be a .zip containing .dSYM folder · max 1GB |
| Crashlytics threshold | Crash-free threshold cannot be set below 90% (would be too permissive) |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| Keystore never exposed | Keystore file stored in Secrets Manager; never downloadable or viewable via UI; only metadata and fingerprints shown |
| Provisioning profile download | Only Mobile Engineer role can download .mobileprovision files; downloaded via presigned S3 URL (1-hour expiry) |
| Crashlytics API key | Stored in Secrets Manager; injected into Celery worker at runtime; never exposed in UI |
| GitHub Actions secrets | Signing credentials injected as GitHub Actions secrets by Secrets Manager sync; never in source code |
| Build logs | May contain environment variable names (not values — values are masked by GitHub Actions); log access restricted to Mobile Engineer + DevOps + Admin |
| dSYM files | Contain compiled app symbols — useful for reverse engineering; download restricted to Mobile Engineer + Admin; S3 presigned URL with 1-hour expiry |
| Beta APK download | APK downloads for direct installation: Mobile Engineer + Admin only; each download logged |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| iOS certificate expired mid-build | Build fails at code signing stage with "Certificate expired" error; immediate email to Mobile Engineer; Signing panel shows red badge |
| Play Store upload rejected (policy violation) | Play Console API returns rejection reason; Store Submission tab shows rejection with reason text and Play Console review appeal link |
| Firebase App Distribution quota exceeded | Firebase free tier: 10,000 testers; amber warning at 9,000; upgrade path shown |
| Build timed out (> 45 min) | GitHub Actions job cancelled; build status = failed with "Build timeout"; retry available from build drawer |
| Duplicate build number (race condition) | Build number is auto-incremented per platform with DB-level unique constraint; race condition returns error to second triggering party |
| Crashlytics API rate limit | Cached 10 min; if cache miss and rate limited: stale data shown with "Crashlytics data delayed" banner |
| Missing dSYM for production crash | Red banner on Crashlytics panel: "Crash reports for v{n} are obfuscated — dSYM not found. Upload now." with direct upload button |
| App Store review rejection | Store Submission tab shows rejection reason from Apple; "Respond to reviewer" link opens App Store Connect (external) |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| Build log size | Logs can be 5–20 MB; streamed from S3 via chunked response; only last 5,000 lines shown in UI; "load more" button for older lines |
| Crashlytics data polling | 10-min Memcached cache; Celery beat refreshes proactively every 9 min; crash threshold alerts run independently every 30 min |
| GitHub Actions API rate limit | 5,000 requests/hour for authenticated requests; build status polling (30s × 68 functions max) = 120 req/min; well within limit |
| Build list table | Max ~50 builds shown by default (last 14 days); older builds accessible via date range filter; no virtual scroll needed at this volume |
| Store submission status | Polled from App Store Connect API (fastlane spaceship) and Play Developer API every 15 min; not real-time (Apple processing has inherent delay) |
| Firebase distribution | Firebase Admin SDK batches tester notification sending; no UI blocking during distribution; result shown asynchronously |

---

## Amendment — G28: FCM Delivery Monitor Tab

**Gap addressed:** Mobile Engineer could not see push notification delivery rates, iOS vs Android split, device token health (expired/unregistered = uninstalled apps), or active FCM topic subscriber counts. Delivery failures went undetected.

### New Tab on Mobile Build Pipeline — FCM Delivery Monitor

**Access:** `/engineering/mobile-builds/?tab=fcm-delivery`

**Data source:** Firebase Cloud Messaging (FCM) Admin SDK + Firebase Management API for delivery statistics.

**Layout:**

**Overall Delivery Summary (KPI strip — last 24h):**

| Card | Metric |
|---|---|
| Total Sent | Push notifications sent in last 24h |
| Delivered | Successfully delivered count + % |
| Failed | Failed delivery count + % |
| iOS Delivery Rate | % delivered on iOS (APNs gateway) |
| Android Delivery Rate | % delivered on Android (FCM direct) |
| Unregistered Tokens | Count of device tokens returned as unregistered (= app uninstalled) |

**Colour rules:** Delivery rate < 90% → amber · < 80% → red · Unregistered tokens > 5% of total → amber (high uninstall rate indicator)

**iOS vs Android Delivery Split:**
- Side-by-side bar: iOS delivered/failed · Android delivered/failed (last 7 days, daily bars)
- Tooltip per bar: sent count + delivery rate

**Device Token Health Panel:**

| Status | Count | Description |
|---|---|---|
| Valid | Count | Active tokens that have received at least 1 notification in last 30 days |
| Expired | Count | Tokens returned as expired by APNs/FCM but device still exists |
| Unregistered | Count | App uninstalled — these tokens should be purged from the platform DB |

- "Purge Unregistered Tokens" button (Admin + Mobile Engineer · no 2FA — data hygiene operation): triggers Celery task to remove all unregistered tokens from `platform_fcm_tokens` table across all 2,050 tenant schemas → progress shown via HTMX poll

**Active FCM Topics Table:**

| Column | Description |
|---|---|
| Topic Name | e.g., `question_returned` · `exam_starting` · `key_rotation_reminder` · `app_update` |
| Subscriber Count | Current subscribed device count |
| Last Notification | Timestamp of most recent notification sent to this topic |
| 24h Sent | Notifications sent to topic in last 24h |
| 24h Delivery Rate | % of sent that were delivered |

**Recent Notification Log (last 50):**

| Column | Description |
|---|---|
| Timestamp | Sent at |
| Topic | FCM topic name |
| Title | Notification title |
| Sent | Count of devices targeted |
| Delivered | Count confirmed delivered |
| Failed | Count failed |
| Failure Reason | Most common failure: `UNREGISTERED` / `INVALID_ARGUMENT` / `QUOTA_EXCEEDED` / `INTERNAL` |

**Notification Template Manager:**
- Predefined payloads for platform notifications: `question_returned` · `exam_starting` · `key_rotation_reminder` · `app_update`
- Each template: Title (English + Hindi) · Body · Data payload (JSONB) · Icon · Sound
- Edit template: inline edit + "Save" (Admin + Mobile Engineer · no 2FA for template edits)
- "Send Test" button per template: opens mini-modal → select target topic → sends test notification immediately → shows "Test sent to {n} devices" toast

**fcm-delivery-drawer (per notification log row):**
- Delivery Stats: sent / delivered / failed / pending breakdown
- Device Breakdown: iOS vs Android pie
- Failed Tokens: sample of 5 failed token IDs (masked) + failure reason
- Retry Status: whether auto-retry was attempted (FCM retries UNAVAILABLE errors automatically)

**Data Flow:**
- Delivery stats: FCM Data API (Firebase Management API v1) — `projects/{project_id}/androidApps/{app_id}/deliveryData` + equivalent iOS endpoint; cached Memcached 10 min
- Topic subscriber counts: FCM Admin SDK topic management endpoint
- Recent notification log: stored in `platform_fcm_notification_log` table (platform sends all notifications via backend; log captured at send time)

**Data Model Addition — platform_fcm_notification_log:**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| topic | VARCHAR(100) | |
| title | VARCHAR(255) | |
| body | TEXT | |
| sent_count | INTEGER | |
| delivered_count | INTEGER | nullable — updated async |
| failed_count | INTEGER | nullable — updated async |
| failure_reason | VARCHAR(100) | nullable — most common failure type |
| sent_at | TIMESTAMPTZ | |
| sent_by | UUID FK → platform_staff | nullable (null = system-automated) |
