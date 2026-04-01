# 08 — Mobile App Config

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Mobile app platform | Flutter (iOS + Android) |
| Estimated app installs | ~3M+ (students + institution staff) |
| Active mobile users | ~1.8M+ monthly active |
| iOS version | App Store (Apple) |
| Android version | Google Play Store + direct APK (coaching centres often use APK) |
| Minimum supported Flutter SDK | 3.16 |
| FCM (Firebase Cloud Messaging) topics | ~15 topics (per exam domain, per institution type) |
| Hive local storage encryption | AES-256 key managed per-app instance |
| Force update SLA | Critical security fixes: force update within 24h |
| App version update frequency | ~monthly minor releases + emergency patches |

**Why this page matters at scale:** 3M+ students rely on the Flutter app to attend exams, access question banks, and receive notifications. A critical security vulnerability in a mobile app version cannot wait for the App Store review cycle — PM Platform must be able to force-block vulnerable versions within hours. At the same time, a forced update pushed carelessly during an active exam (74K concurrent) would cause mass disruption. This page gives PM Platform precise control over version enforcement, FCM routing, and mobile feature flags — separately from web feature flags.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Mobile App Config |
| Route | `/product/mobile-config/` |
| Django view class | `MobileAppConfigView` |
| Template | `product/mobile_config.html` |
| Permission — view | `portal.view_mobile_config` (all div-b roles) |
| Permission — manage | `portal.manage_mobile_config` (PM Platform only) |
| Permission — force update | `portal.force_update_mobile` (PM Platform + 2FA) |
| 2FA required | Yes — for force update, block version, Hive key rotation schedule |
| HTMX poll — version distribution | Every 300s (5 min) |
| Nav group | Product |
| Nav icon | `smartphone` |
| Priority | P2 |

---

## 3. Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Mobile App Config                       [Force Update] [Check App Store ↗] │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────────────────────────┤
│ Latest   │ iOS      │ Android  │ Users on │ Blocked  │ Active Exam Guard            │
│ Version  │ v3.4.2   │ v3.4.2   │ Latest   │ Versions │ ● ACTIVE (exam in progress) │
│ v3.4.2   │ On Store │ On Store │ 68.2%    │    0     │ Force update PAUSED          │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────────────────────────┤
│ TABS: [Version Control] [Feature Flags (Mobile)] [FCM Config] [Hive Config] [Logs] │
├────────────────────────────────────────────────────────────────────────────────────┤
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

| # | Card | Value | Alert |
|---|---|---|---|
| 1 | Latest Version | `v3.4.2` | — |
| 2 | iOS Store Version | `v3.4.2 · Live` | Mismatch with latest = amber |
| 3 | Android Play Version | `v3.4.2 · Live` | Mismatch with latest = amber |
| 4 | Users on Latest Version | `68.2%` | < 50% after 7 days = amber |
| 5 | Blocked Versions | `0` | Any blocked = `border-[#EF4444]` |
| 6 | Active Exam Guard | `ACTIVE` or `INACTIVE` | Active = `bg-[#064E3B] animate-pulse` |

**Active Exam Guard card:**
Critical safety feature — when an exam is live (any institution has an ongoing exam), force-update actions are automatically blocked to prevent disrupting active exam sessions.
- Active: `bg-[#064E3B] text-[#34D399] animate-pulse` "● ACTIVE — Force update paused"
- Inactive: `bg-[#1E2D4A] text-[#94A3B8]` "No active exams — Force update available"

---

### 4.2 Tab Bar

| Tab | Description |
|---|---|
| Version Control | Version matrix, force update rules, blocked versions |
| Feature Flags (Mobile) | Mobile-specific feature flags (separate from web flags) |
| FCM Config | Firebase Cloud Messaging topic management |
| Hive Config | Local database encryption key rotation schedule |
| Logs | Mobile config change audit log |

---

### 4.3 Tab: Version Control

#### 4.3.1 Version Distribution Chart

**Canvas id:** `version-dist-chart` · height 200px · Chart.js horizontal bar chart
**Poll:** `hx-get="?part=version_dist" hx-trigger="every 300s[!document.querySelector('.drawer-open,.modal-open')]"`

X-axis: % of users · Y-axis: version labels
Series: iOS `#6366F1` · Android `#10B981`

**Data (example):**
| Version | iOS Users % | Android Users % |
|---|---|---|
| v3.4.2 (latest) | 72.1% | 64.3% |
| v3.4.1 | 18.3% | 22.7% |
| v3.4.0 | 6.2% | 9.8% |
| v3.3.x | 2.8% | 2.4% |
| v3.2.x or older | 0.6% | 0.8% |

Hover tooltip: version · iOS count · Android count · "Last seen: X days ago"

---

#### 4.3.2 Version Policy Table

`id="version-policy-table"`

| Version | Released | iOS Status | Android Status | Policy | Affected Users | Actions ⋯ |
|---|---|---|---|---|---|---|
| v3.4.2 | Mar 15 | ✅ Latest | ✅ Latest | — | — | — |
| v3.4.1 | Feb 20 | ⚠ Outdated | ⚠ Outdated | Soft nudge | ~41% | [Block] [Enforce Update] |
| v3.4.0 | Jan 10 | ⚠ Outdated | ⚠ Outdated | Soft nudge | ~16% | [Block] [Enforce Update] |
| v3.3.x | Dec 2025 | ❌ Blocked | ❌ Blocked | Force update | ~2.4% | [Unblock] |

**Policy options per version:**

| Policy | Behaviour |
|---|---|
| None | Users can use this version freely |
| Soft nudge | Show "Update available" banner — dismissible |
| Recommended update | Modal on app open — can dismiss with "Remind me later" |
| Enforce update | Modal on app open — cannot dismiss · must update to continue |
| Blocked | App refuses to launch on this version · shows error with App Store link |

**Kebab menu (⋯):**
- Set Policy → inline dropdown select
- Block Version → 2FA confirmation modal
- Unblock Version → confirmation
- View Users on This Version → drawer with user list
- Export User List CSV

---

#### 4.3.3 Force Update Configuration Panel

`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4`

**Minimum required version:**
```
iOS minimum:     [v3.4.0 ▾]   (users below this are blocked)
Android minimum: [v3.4.0 ▾]   (users below this are blocked)
```

**Exam-day protection toggle:**
`flex items-center gap-3`
Toggle: `bg-[#6366F1]` when ON
"Pause forced updates during active exams"
`text-xs text-[#94A3B8]` "When enabled, force update messages will not show to students during live exam sessions."

**Scheduled force update:**
```
Schedule force update to v3.4.2:
After date: [Apr 1, 2026  ▾]
Grace period: [7] days (soft nudge first)
Affected users: ~1.8M (31.8% of active users)
```

[Save Configuration] — requires 2FA
[Preview Force Update Screen] — shows what the user sees

---

### 4.4 Tab: Feature Flags (Mobile)

**Purpose:** Mobile app feature flags are separate from web feature flags because:
1. Mobile releases have App Store review delay (up to 7 days) — flags allow enabling features post-approval
2. Some features only exist on mobile (camera, offline mode, biometric auth)
3. iOS vs Android may have different rollout timelines

**Layout:** Same table structure as page 02 (Feature Flags) but scoped to `domain=mobile`

**Additional mobile-specific columns:**
- Platform: iOS only · Android only · Both
- Requires app version: minimum version badge

**Mobile-specific flags (examples):**

| Flag Key | Name | Platform | Status | Rollout | Min Version |
|---|---|---|---|---|---|
| `offline_exam_mode` | Offline Exam Mode | Both | Partial | 5% | v3.4.0+ |
| `biometric_auth` | Biometric Authentication | Both | Enabled | 100% | v3.3.0+ |
| `camera_proctoring` | Camera-based Proctoring | Both | Partial | 20% coaching | v3.4.1+ |
| `ios_scribble` | iPad Scribble Support | iOS only | Disabled | 0% | v3.4.2+ |
| `android_widget` | Home Screen Widget | Android only | Draft | 0% | v3.5.0+ |
| `dark_mode_v2` | Dark Mode v2 | Both | Enabled | 100% | v3.3.0+ |

**Platform filter** (additional filter in toolbar): [All ▾] [iOS only] [Android only] [Both]

---

### 4.5 Tab: FCM Config

**Purpose:** Firebase Cloud Messaging topics determine which notifications each user receives. PM Platform configures topic structure; Engineering configures delivery.

#### 4.5.1 Topic Registry Table

| Topic Name | FCM Topic Key | Subscribers | Purpose | Auto-subscribe |
|---|---|---|---|---|
| All Students | `all_students` | ~1.8M | Broadcast to all | Yes — on registration |
| SSC Domain | `domain_ssc` | ~420K | SSC exam notifications | Yes — if enrolled in SSC |
| RRB Domain | `domain_rrb` | ~380K | RRB exam notifications | Yes — if enrolled |
| NEET Domain | `domain_neet` | ~280K | NEET prep notifications | Yes — if enrolled |
| JEE Domain | `domain_jee` | ~190K | JEE prep notifications | Yes — if enrolled |
| AP Board | `domain_ap_board` | ~240K | AP State Board | Yes — if enrolled |
| TS Board | `domain_ts_board` | ~210K | Telangana State Board | Yes — if enrolled |
| Exam Day Alert | `exam_day` | ~1.8M | Live exam notifications | Yes — always |
| Result Published | `results` | ~1.8M | Result notifications | Yes — always |
| Coaching Staff | `staff_coaching` | ~15K | Coaching centre admin topics | Yes — if staff |
| Institution Admin | `staff_admin` | ~6K | Admin announcements | Yes — if admin role |
| Beta Testers | `beta` | ~2K | Early feature testing | Manual opt-in |

**Actions per topic:**
- [Edit] — rename topic, change auto-subscribe rules
- [Send Test Notification] — sends FCM test to PM's own device
- [View Subscriber Count History] — line chart

**[+ New Topic]** button — creates new FCM topic
**[Send Broadcast]** button — opens broadcast modal (separate from Announcement Manager — raw FCM push)

---

#### 4.5.2 Topic Subscription Rules

Defines which FCM topics a user is automatically subscribed to on app install/login:

```python
# Rules defined here, applied by mobile backend on auth:
if user.role == "student":
    subscribe(f"domain_{user.enrolled_domain}")
    subscribe("exam_day")
    subscribe("results")
    subscribe("all_students")
if user.role in ("admin", "principal"):
    subscribe("institution_admin")
    subscribe("exam_day")
if institution.type == "coaching":
    subscribe("staff_coaching")
```

Rules are editable via form on this page (JSON-like rule builder UI).

---

### 4.6 Tab: Hive Config

**Purpose:** Flutter Hive is a local NoSQL database used for offline caching of question bank content, user progress, and exam drafts. Encryption keys rotate periodically.

**Why it matters:** If a compromised device has a student's locally-cached exam questions, those questions could leak. Key rotation ensures old cached data becomes unreadable after rotation.

#### 4.6.1 Encryption Key Status

| Platform | Current Key Version | Created | Next Rotation | Status |
|---|---|---|---|---|
| iOS | key_v4 | Jan 15, 2026 | Apr 15, 2026 | ✅ Active |
| Android | key_v4 | Jan 15, 2026 | Apr 15, 2026 | ✅ Active |

**Key rotation schedule:**
```
Rotation frequency: Every [90] days
Rotation strategy:  [○ Rotate on next app launch] [○ Force update + rotate]
Overlap period:     [7] days (old key valid during overlap for graceful migration)
User impact:        App re-encrypts local data on first launch after rotation
```

**[Schedule Next Rotation]** — requires 2FA

**Rotation history table:**
| Version | Platform | Rotated On | Rotated By | Users migrated | Duration |
|---|---|---|---|---|---|
| key_v4 → key_v5 | Both | Apr 15, 2026 (scheduled) | — | — | — |
| key_v3 → key_v4 | Both | Jan 15, 2026 | Priya S. | 1.8M (98.2%) | 7 days |

---

#### 4.6.2 Cached Data Types

`bg-[#0D1526] rounded-xl border border-[#1E2D4A] p-4`

| Data Type | Encrypted? | TTL | Max Size | Notes |
|---|---|---|---|---|
| Question Bank (offline) | ✅ Yes | 7 days | 200 MB | AES-256 with Hive key |
| User progress sync | ✅ Yes | 24 hours | 5 MB | — |
| Exam draft (offline exam) | ✅ Yes | 4 hours | 2 MB | Deleted on submit |
| App settings | ✅ Yes | Persistent | 500 KB | — |
| Auth token | ✅ Yes | 8 hours | 4 KB | Rotated per session |

[Edit TTL/Size] per row — opens inline edit form

---

### 4.7 Tab: Logs

**Same structure as feature flags audit tab.**

All mobile config changes logged:
- Version policy changes
- Force update triggers
- Feature flag changes (mobile)
- FCM topic changes
- Hive key rotation events

**Columns:** Timestamp · Actor · Action · Details · IP Address

---

## 5. Modals

### 5.1 Force Update Modal

**Trigger:** [Force Update] header button or version row action
**Width:** 560px
**Warning:** `bg-[#1A0A0A] border border-[#EF4444]`

**Exam guard check (automatic):**
If any exam is currently live:
`bg-[#1A0A0A] border border-[#EF4444] rounded p-3`
"⚠ BLOCKED: {N} exams currently in progress. Force update cannot be initiated during active exam sessions. The exam guard will automatically lift when all exams complete."
[Force Update] button is disabled.

If no active exams:

**Configuration:**
- Versions to block: multi-select from version list
- Policy: Enforce update (modal, no dismiss) / Blocked (app won't launch)
- Affected users estimate: auto-computed
- Schedule: [Now] or [Date + Time picker]
- Message to users: textarea (max 200 chars)
- 2FA code: required

**Footer:** [Confirm Force Update] `bg-[#EF4444]` · [Cancel]

---

### 5.2 Block Version Modal

**Width:** 440px
"Block v3.3.2? Users on this version will see an error and be unable to use the app until they update."
- 2FA required
- Reason: textarea (required)
- Impact: "~28,000 users currently on this version"

**Footer:** [Block Version] `bg-[#EF4444]` · [Cancel]

---

### 5.3 Test Notification Modal

**Trigger:** [Send Test Notification] in FCM Config
**Width:** 400px

- Topic: pre-selected or dropdown
- Title: text input
- Body: textarea
- Click action: URL or deep link
- Target: [My device only] (sends to PM's registered test device)

**Footer:** [Send Test] · [Cancel]

---

## 6. Django View

```python
class MobileAppConfigView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_mobile_config"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi":           "product/partials/mobile_kpi.html",
                "version_dist":  "product/partials/mobile_version_dist.html",
                "version_policy":"product/partials/mobile_version_policy.html",
                "mobile_flags":  "product/partials/mobile_flags.html",
                "fcm_topics":    "product/partials/mobile_fcm.html",
                "hive_config":   "product/partials/mobile_hive.html",
                "mobile_logs":   "product/partials/mobile_logs.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "product/mobile_config.html", ctx)

    def post(self, request):
        action = request.POST.get("action")
        gated = {"force_update", "block_version", "schedule_hive_rotation", "update_min_version"}
        if action in gated:
            if not request.session.get("2fa_verified"):
                return JsonResponse({"error": "2FA required"}, status=403)
            # Extra guard: block force updates during active exams
            if action == "force_update":
                from portal.apps.exams.models import ExamSession
                active_exams = ExamSession.objects.filter(status="live").count()
                if active_exams > 0:
                    return JsonResponse({
                        "error": f"Force update blocked: {active_exams} exams currently live."
                    }, status=409)

        if not request.user.has_perm("portal.manage_mobile_config"):
            return JsonResponse({"error": "Permission denied"}, status=403)

        dispatch = {
            "set_version_policy":      self._set_version_policy,
            "force_update":            self._force_update,
            "block_version":           self._block_version,
            "unblock_version":         self._unblock_version,
            "update_min_version":      self._update_min_version,
            "create_fcm_topic":        self._create_fcm_topic,
            "update_fcm_topic":        self._update_fcm_topic,
            "send_test_notification":  self._send_test_notification,
            "schedule_hive_rotation":  self._schedule_hive_rotation,
            "update_hive_ttl":         self._update_hive_ttl,
        }
        handler = dispatch.get(action)
        if handler:
            return handler(request)
        return JsonResponse({"error": "Unknown action"}, status=400)
```

---

## 7. Empty States

| Section | Copy |
|---|---|
| No blocked versions | "No versions blocked. All app versions are permitted." |
| No FCM topics | "No FCM topics configured yet." |
| No Hive rotation history | "No key rotations recorded." |
| No mobile-specific flags | "No mobile-only feature flags. Create one to get started." |

---

## 8. Error States

| Error | Display |
|---|---|
| Force update during active exam | `bg-[#1A0A0A] border-[#EF4444]` "Blocked: N exams currently live" |
| FCM topic key collision | "Topic key already exists. Choose a unique key." |
| Hive rotation < 30 days after last | "Key rotation was less than 30 days ago. Are you sure?" amber warning |
| Version below current minimum | "Cannot set minimum version higher than current latest release." |

---

## 9. App Store Release Notes Management

**Purpose:** When a new mobile version is shipped, the App Store (iOS) and Google Play (Android) listing must include "What's New" text. PM Platform drafts this text here, synced to the engineering release checklist via Release Manager (page 03).

**Release Notes Panel** (sub-section of Version Control tab, below Version Policy Table):

| Field | iOS | Android |
|---|---|---|
| Version | v3.5.0 (upcoming) | v3.5.0 (upcoming) |
| What's New | Textarea · max 4,000 chars (App Store limit) | Textarea · max 500 chars (Play Store short limit) |
| Keywords | Text · max 100 chars (App Store only) | N/A |
| Status | Draft · Submitted · Approved · Live | Draft · Submitted · Approved · Live |

**[Auto-generate from Release Changelog]:** Pulls bullet points from the linked Release Manager entry and formats them for each store's length constraint. PM edits before submitting.

**[Link to Release]:** Connects this version's release notes to a Release Manager record (page 03). When QA signs off on that release, the release notes status moves to "Submitted."

---

## 10. Crash Reporting Integration

**Purpose:** Firebase Crashlytics crash data is surfaced here so PM Platform can correlate crashes with specific app versions and make informed force-update decisions. High crash rate on v3.4.1 = strong justification to block it.

**Crash Rate Summary Panel** (visible at top of Version Control tab):

| Version | iOS Crash-Free Rate | Android Crash-Free Rate | 7-day Trend | Action |
|---|---|---|---|---|
| v3.4.2 (latest) | 99.7% | 99.5% | → Stable | — |
| v3.4.1 | 97.2% | 96.8% | ↓ Worsening | ⚠ Consider blocking |
| v3.4.0 | 95.1% | 94.3% | → Stable | ❌ Block recommended |

**Crash threshold alerts:**
- Crash-free rate < 99%: amber warning badge on version row
- Crash-free rate < 95%: red badge + auto-suggestion: "Block recommended — click to review"
- Crash-free rate < 90%: critical alert bus notification (G5) to all div-b pages

**[View Crash Details →]**: links to Firebase Crashlytics dashboard (external tab)

---

## 11. Deep Link Configuration

**Purpose:** Notifications (FCM) and marketing links use deep links to open specific screens inside the app. PM Platform defines the mapping between link slugs and in-app destinations.

**Deep Link Registry Table:**

| Link Slug | In-App Destination | Used By | Active |
|---|---|---|---|
| `/exam/{exam_id}` | Exam detail screen | Result notifications | ✅ |
| `/result/{attempt_id}` | Result screen | Result-published FCM | ✅ |
| `/series/{series_id}` | Test series screen | Enrollment notifications | ✅ |
| `/payment` | Payment screen | Payment due FCM | ✅ |
| `/announcement/{id}` | Announcement detail | Feature update banners | ✅ |
| `/profile` | Student profile | Account notifications | ✅ |
| `/question-bank` | Question bank home | Study reminder FCM | ✅ |
| `/offline-sync` | Offline sync screen | Connectivity warnings | ⬜ Draft |

**[+ Add Deep Link]** modal: Link slug (text, must start with `/`) · Destination screen (select from app screen list) · Description

**Minimum app version per deep link:** Ensures old app versions that don't support the destination screen silently fall back to home screen rather than crashing.

---

## 12. Integration Points

| Page | Direction | What flows |
|---|---|---|
| 02 — Feature Flags | Inbound | Mobile-specific flags (this tab) are a scoped subset of the full flag registry in page 02; kill-switch on page 02 overrides mobile flag |
| 03 — Release Manager | Both | Release notes drafted here link to Release Manager release records; QA sign-off on release triggers "Submitted" status on release notes |
| 07 — Announcement Manager | Outbound | FCM topics configured here are the delivery mechanism for announcements sent via page 07 |
| 18 — Notification Template Manager | Outbound | FCM delivery channels configured here are used by notification templates on page 18 |
| 25 — Defect Tracker | Inbound | Mobile crashes (Crashlytics) that cross the 95% crash-free threshold auto-create a P1 defect in page 25 |

---

## 13. Key Design Decisions

| Decision | Chosen approach | Why |
|---|---|---|
| Active Exam Guard on force update | Hard block in both UI and backend | 74K concurrent students in exam sessions cannot be force-restarted; a forced update would close the exam app and lose answers — unrecoverable data loss |
| Separate mobile feature flags from web flags | Distinct flag namespace `domain=mobile` | Mobile flags require a minimum app version constraint that web flags don't have; merging them would require all 120+ web flags to carry unused mobile fields |
| Hive key rotation overlap period (7 days) | Configurable overlap, default 7 | Rotation must not lock out users mid-exam; 7-day overlap allows all active users to upgrade and migrate before old key is revoked |
| FCM topic auto-subscribe rules defined here (not in Django admin) | PM-managed rule builder | Engineering-managed Django admin subscriptions are slow to change and require a code deploy; PM needs to respond to domain launches (e.g., new IBPS domain) within hours |
| Crash rate sourced from Crashlytics, not custom | Firebase integration (read-only display) | Crashlytics is already the engineering source of truth; duplicating crash tracking would create divergence; PM reads from the same source Engineering uses |
| App Store release notes linked to Release Manager | Cross-page linkage | Prevents PM writing release notes that contradict the actual release changelog; single source of truth for what shipped |

---

## 14. Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `1–5` | Switch tabs |
| `Esc` | Close drawer/modal |
| `R` | Refresh version distribution |
