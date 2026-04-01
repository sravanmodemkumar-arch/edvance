# C-06 — CDN & Asset Manager

> **Route:** `/engineering/cdn/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · Frontend Engineer (Role 12) · DevOps/SRE (Role 14)
> **File:** `c-06-cdn-assets.md`
> **Priority:** P2
> **Status:** ⬜ Amendment pending — G3 (Performance Monitor tab)

---

## 1. Page Name & Route

**Page Name:** CDN & Asset Manager
**Route:** `/engineering/cdn/`
**Part-load routes:**
- `/engineering/cdn/?part=kpi` — CDN health KPI strip
- `/engineering/cdn/?part=distributions` — CloudFront distributions table
- `/engineering/cdn/?part=asset-browser&prefix={prefix}` — S3/R2 asset browser
- `/engineering/cdn/?part=invalidation-modal` — cache invalidation modal
- `/engineering/cdn/?part=invalidation-log` — recent invalidations log

---

## 2. Purpose (Business Objective)

The CDN & Asset Manager gives Frontend Engineers and DevOps control over the platform's content delivery infrastructure — primarily three CloudFront distributions serving the portal, static assets, and API edge, and the R2/S3 buckets holding CSS, JavaScript, fonts, images, and HTMX template fragments.

The most common use case is cache invalidation: after a CSS or JS deployment, the Frontend Engineer must bust the CDN cache so all 2,050 institution portals start serving the new version immediately rather than the cached version (which could persist for up to 24h). The second most common use is checking that Brotli compression is active and that cache hit rates are healthy — a drop in cache hit rate can dramatically increase API origin load.

**Business goals:**
- Enable instant cache invalidation without AWS console access
- Provide visibility into cache hit rates across all 3 distributions
- Manage static asset lifecycle: upload, version, and delete assets from a unified browser
- Track CDN cost per GB to inform caching and compression optimisation decisions
- Ensure Brotli/gzip compression is active on all text assets

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full: invalidation · asset upload/delete · distribution config |
| Frontend Engineer (12) | Level 4 | Full: invalidation · asset upload/delete · read distribution metrics |
| DevOps / SRE (14) | Level 4 | Full: invalidation · read asset browser · distribution config |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Global CDN Status

**Purpose:** Instant CDN health check and quick-access to most common action (cache invalidation).

**Header elements:**
- H1 "CDN & Asset Manager"
- "Invalidate Cache" primary CTA button (opens invalidation modal)
- Global CDN status indicator: ✅ All distributions healthy · ⚠ Degraded · 🚨 CloudFront incident
- Last data refresh timestamp

**Edge Cases:**
- CloudFront itself experiencing an incident (AWS Health Dashboard event): red banner with "CloudFront incident detected in ap-south-1. CDN performance degraded. Monitor AWS Health."

---

### Section 2 — KPI Strip — CDN Health

**KPI Cards:**

| Card | Metric | Source | Alert |
|---|---|---|---|
| Global Cache Hit Rate | Hits / (hits+misses) across all 3 distributions | CloudFront metrics | < 85% amber |
| Total Bandwidth (24h) | GB transferred | CloudFront | — |
| CDN Cost (MTD) | USD/INR estimated from CloudFront pricing | AWS Cost Explorer | > 80% monthly budget = amber |
| Error Rate (4xx+5xx) | Across all distributions | CloudFront | > 0.5% = amber |
| Active Invalidations | In-progress CloudFront invalidation batches | CloudFront API | — |
| Assets in S3/R2 | Total file count in static asset buckets | S3 ListObjectsV2 | — |

**Data Flow:**
- CloudFront metrics from CloudWatch `AWS/CloudFront` namespace (global — `us-east-1` region, CloudFront metrics are always us-east-1)
- Cost data from AWS Cost Explorer API (daily granularity, 1-day delay)
- Assets count from Memcached cache (S3 ListObjects expensive — cached 10 min)

---

### Section 3 — CloudFront Distributions Panel

**Purpose:** Per-distribution metrics and configuration overview.

**Distribution Cards (3 cards):**

| Distribution | Purpose | Behaviour Config |
|---|---|---|
| Portal Distribution | Institution portal HTML · HTMX fragment responses | Dynamic content · Low TTL (30s) · Compress enabled |
| Static Assets Distribution | CSS · JS · fonts · images · WOFF2 | Long TTL (1 year for content-hashed files) · Compress enabled |
| API Edge Distribution | API gateway (Lambda function URLs) | No cache (TTL = 0) for POST/PATCH · Short cache for GET |

**Per-distribution card shows:**

| Metric | Value |
|---|---|
| Distribution ID | Masked (first 8 chars visible) |
| Domain | `dxxxxxxxxx.cloudfront.net` |
| Custom Domain (CNAME) | `portal.platform.in` / `static.platform.in` / `api.platform.in` |
| Status | Deployed ✅ / InProgress 🔄 |
| Cache Hit Rate (24h) | % with sparkline (7 days) |
| Requests/min (now) | Live from CloudWatch |
| Bandwidth (24h) | GB |
| Error Rate | % 4xx + 5xx |
| Compression | Brotli ✅ / Gzip only ⚠ / None ❌ |
| HTTP/2 | Enabled ✅ |

**Actions per distribution:**
- "View origin config" — shows origin domain + SSL settings
- "View cache behaviours" — read-only list of path patterns + TTL + cache policy
- "View invalidations" — jumps to invalidation log filtered to this distribution

---

### Section 4 — Cache Invalidation Modal

**Purpose:** Guided interface for invalidating CloudFront cache paths.

**Trigger:** "Invalidate Cache" button in header; or "Invalidate" from distribution card

**Invalidation Types:**

| Type | Path | When to Use |
|---|---|---|
| Specific file | `/static/css/main.abc123.css` | Single asset update |
| Directory | `/static/js/*` | JS bundle update |
| Template fragment | `/templates/exam-header/*` | HTMX template deployment |
| Full static | `/static/*` | Major CSS/JS release |
| Emergency full purge | `/*` | Critical bug in all assets |

**Modal Fields:**
- Distribution: dropdown (Portal / Static Assets / API Edge)
- Invalidation paths: textarea (one path per line · supports `*` wildcard)
- Path preview: shows estimated number of objects that will be invalidated
- Reason: required text field (min 20 chars)
- Priority: Normal (queued) · High (jumps queue — use for incidents)

**Cost warning:**
- First 1,000 invalidation paths/month: free
- Beyond 1,000: $0.005 per path
- Inline counter: "You've used {n} of 1,000 free invalidation paths this month"
- Emergency full purge (`/*`): counts as 1 path (smart use of wildcard)

**Confirmation:**
- For `/*` (emergency full purge): confirmation modal: "Full cache purge will temporarily increase origin load as all assets are re-fetched from S3. CloudFront cold-cache period ~5 min. Confirm?"
- No 2FA required for normal invalidations
- 2FA required for emergency full purge (Admin only)

**On submit:**
- `POST /api/cdn/invalidations/` → calls CloudFront CreateInvalidation API
- Progress shown in invalidation log (status: InProgress → Completed, typically 30–120s)

**Edge Cases:**
- CloudFront invalidation limit: max 3,000 paths per distribution per invalidation batch; validation enforced client-side
- During active exam: amber warning "Exam in progress. Full cache purge may cause temporary asset unavailability for exam portal. Proceed only if critical."

---

### Section 5 — Recent Invalidations Log

**Purpose:** Track all cache invalidation requests and their completion status.

**Columns:**

| Column | Description |
|---|---|
| Timestamp | Created at |
| Distribution | Which distribution |
| Paths | Comma-separated (truncated to 3 paths + "and N more") |
| Status | InProgress (spinner) · Completed ✅ · Failed ❌ |
| Duration | Time from creation to completion |
| Requested By | Engineer name |
| Reason | Notes entered in modal |
| CF Invalidation ID | CloudFront InvalidationId (expandable) |

**Refresh:** 15s HTMX poll (InProgress items resolve in 30–120s)
**Retention:** Last 90 days visible; older entries archived

---

### Section 6 — S3/R2 Static Asset Browser

**Purpose:** Browse, upload, version, and delete static assets without AWS console access.

**Layout:** Two-panel: left = directory tree, right = file list

**Directory Tree (left panel):**

```
/ (root)
├── static/
│   ├── css/
│   ├── js/
│   ├── fonts/
│   ├── images/
│   └── icons/
├── templates/
│   ├── exam/
│   ├── dashboard/
│   └── components/
└── uploads/
    └── tenants/ (read-only in this view — managed via tenant media)
```

**File List (right panel):**

| Column | Description |
|---|---|
| File Name | Content-hash filename (e.g., `main.a1b2c3d4.css`) |
| Size | Human-readable (KB / MB) |
| Last Modified | Relative timestamp |
| Content Type | MIME type badge |
| Cache-Control | Header value (e.g., `max-age=31536000, immutable`) |
| Compression | Brotli ✅ · Gzip ⚠ · None ❌ |
| CDN URL | Shortened clickable URL (opens in new tab) |
| Actions | Download · Invalidate · Delete (Admin/Frontend only) |

**Search within browser:** filename search (client-side filter if < 500 files; server-side for larger directories)

**Upload:**
- "Upload File" button → file picker (max 50MB per file · multiple files allowed)
- On upload: S3 PutObject via presigned URL (browser → S3 directly; no server roundtrip for file bytes)
- After upload: metadata written to `platform_asset_registry` table
- Invalidation: optional "Invalidate CDN cache for this file" checkbox on upload modal

**Delete:**
- Confirmation modal: "Deleting {filename} will remove it from S3 and invalidate CDN cache. Any pages referencing this file will break."
- 2FA required for Admin only

**Compression status:**
- Files without Brotli encoding: amber warning chip
- "Compress with Brotli" action button → Celery job: fetches file, Brotli-compresses, re-uploads with `Content-Encoding: br`

**Asset Version History:**
- Click filename → shows version history (S3 versioning enabled)
- Last 10 versions: file size · uploaded at · uploaded by
- "Restore previous version" button (creates new version with old file content; no in-place overwrite)

---

### Section 7 — Asset Version Registry

**Purpose:** Track content-hashed file names across deployments — which hash corresponds to which release.

**Table:**

| File Base | Current Hash | Previous Hash | Deployed At | Deployed By | CI/CD Run |
|---|---|---|---|---|---|
| `main.css` | `a1b2c3d4` | `e5f6g7h8` | 2h ago | Priya Sharma | #4521 |
| `app.js` | `b2c3d4e5` | `f6g7h8i9` | 2h ago | Priya Sharma | #4521 |
| `fonts/inter.woff2` | `c3d4e5f6` | Same (unchanged) | 5 days ago | Rohan Dev | #4498 |

**Purpose:** During incident investigation, this table answers "what changed in the last deployment?" without needing to compare S3 files manually.

**Link to CI/CD:** Each row links to the specific C-09 pipeline run that produced this hash.

---

### Section 8 — CDN Cost & Bandwidth Analytics

**Purpose:** Visibility into CDN spend to guide caching and compression optimisation decisions.

**Charts:**
- Daily bandwidth chart: last 30 days (GB/day) — stacked by distribution
- Daily cost chart: last 30 days (USD/INR estimated)
- Cache hit rate trend: last 30 days — should be > 90% for static assets
- Top 10 most-requested files: by request count (last 7 days)
- Top 10 largest bandwidth files: by GB served (last 7 days)

**Cost breakdown table:**

| Distribution | Requests (MTD) | Bandwidth (GB, MTD) | Estimated Cost (MTD) |
|---|---|---|---|
| Portal | 84M | 1.2 TB | ₹4,200 |
| Static Assets | 210M | 8.4 TB | ₹18,600 |
| API Edge | 42M | 0.3 TB | ₹1,100 |
| **Total** | | **9.9 TB** | **₹23,900** |

**Optimisation flags:**
- Auto-detected opportunities shown as info cards:
  - "15 JS files > 1MB without Brotli compression — Enable compression to save ~3.2 GB/month"
  - "Cache hit rate for `/templates/*` is 62% — Consider increasing TTL from 30s to 300s"
  - "Top bandwidth file: `exam-video-intro.mp4` — Consider moving to lower-cost S3 storage class"

---

## 5. User Flow

### Flow A — Post-Deployment Cache Invalidation

1. CI/CD pipeline deploys new CSS/JS build
2. Frontend Engineer opens `/engineering/cdn/`
3. Sees cache hit rate still high (old assets being served from CDN)
4. Clicks "Invalidate Cache"
5. Selects "Static Assets" distribution
6. Paths: `/static/css/*` and `/static/js/*`
7. Reason: "Release #4521 — new CSS/JS bundle deployed"
8. Submits — CloudFront invalidation created
9. Invalidation log shows: InProgress → Completed (after 45s)
10. Refreshes asset browser — new content-hash filenames visible

### Flow B — Emergency Full Purge After Incident

1. Bug reported: wrong CSS being served platform-wide
2. Platform Admin opens CDN Manager
3. Clicks "Invalidate Cache" → selects all distributions
4. Path: `/*` (emergency full purge)
5. Warning modal shown — confirms
6. Enters TOTP (2FA required for `/*`)
7. Three invalidations created (one per distribution)
8. Cold-cache period: ~5 min while CloudFront re-fetches from S3
9. Bug-fixed assets now being served

### Flow C — Compression Audit

1. Frontend Engineer notices CDN cost higher than expected
2. Opens CDN Cost section → sees "15 JS files > 1MB without Brotli"
3. Navigates to asset browser → /static/js/ directory
4. Filters: "Compression: None" — finds 15 files
5. Selects all 15 → "Compress with Brotli" batch action
6. Celery jobs created for each file; progress shown in asset browser
7. After completion: re-checks file list — all show Brotli ✅
8. Next day: CDN bandwidth drops ~30%

---

## 6. Component Structure (Logical)

```
CDNAssetManagerPage
├── PageHeader
│   ├── PageTitle
│   ├── InvalidateCacheButton (primary CTA)
│   └── GlobalCDNStatus
├── KPIStrip
│   └── KPICard × 6
├── DistributionsPanel
│   ├── DistributionCard (Portal)
│   ├── DistributionCard (Static Assets)
│   └── DistributionCard (API Edge)
├── InvalidationModal
│   ├── DistributionSelect
│   ├── PathsTextarea
│   ├── PathPreview
│   ├── ReasonField
│   └── CostWarning
├── RecentInvalidationsLog
├── AssetBrowser
│   ├── DirectoryTree (left)
│   └── FileList (right)
│       ├── SearchBar
│       ├── FilterBar (compression · content-type)
│       ├── FileRow × N
│       └── UploadButton
├── AssetVersionRegistry
└── CostBandwidthAnalytics
    ├── BandwidthChart
    ├── CostChart
    ├── CacheHitRateTrend
    ├── CostBreakdownTable
    └── OptimisationFlags
```

---

## 7. Data Model (High-Level)

### platform_asset_registry

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| file_path | VARCHAR(512) | S3 key (full path) |
| file_name | VARCHAR(255) | |
| content_hash | VARCHAR(16) | first 8 chars of MD5/SHA256 |
| content_type | VARCHAR(100) | MIME type |
| size_bytes | BIGINT | |
| compression | ENUM | brotli/gzip/none |
| cache_control | VARCHAR(200) | |
| s3_bucket | VARCHAR(100) | |
| cdn_distribution | ENUM | portal/static/api |
| uploaded_at | TIMESTAMPTZ | |
| uploaded_by | UUID FK → platform_staff | |
| cicd_run_id | VARCHAR(100) | nullable |
| is_deleted | BOOLEAN | soft delete |

### platform_cdn_invalidations

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| distribution_id | VARCHAR(50) | CloudFront distribution ID |
| cf_invalidation_id | VARCHAR(50) | from CloudFront API response |
| paths | JSONB | array of path strings |
| status | ENUM | in_progress/completed/failed |
| reason | TEXT | |
| requested_by | UUID FK → platform_staff | |
| created_at | TIMESTAMPTZ | |
| completed_at | TIMESTAMPTZ | nullable |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| Invalidation path format | Must start with `/` · `*` only at end of path segment · max 3,000 paths per batch |
| Emergency full purge | `/*` path requires Admin role + 2FA |
| Upload file size | Max 50MB per file; files > 10MB: amber warning "Large files increase CDN costs" |
| Upload during active exam | Amber warning if any exam in progress; allow with acknowledgement |
| Delete asset | Blocked if file was accessed in last 24h (CloudFront access log check) unless Admin override |
| Brotli compression job | Only for text-based MIME types (CSS/JS/HTML/SVG); binary files (images/WOFF2) blocked from Brotli action |
| Cache-Control header | Immutable flag allowed only for content-hashed filenames (must contain 8+ hex chars in filename) |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| S3 access | Presigned URLs for upload (browser-to-S3 direct); admin Lambda role has `s3:PutObject` + `s3:DeleteObject` scoped to static asset prefix only; cannot access tenant data prefixes |
| CloudFront access | `cloudfront:CreateInvalidation` scoped to specific distribution ARNs; cannot invalidate non-platform distributions |
| Delete protection | S3 bucket has MFA delete enabled for permanent deletion; application layer soft-delete first; hard-delete requires Admin |
| Asset URL exposure | CDN URLs are public by design (static assets); no signed URLs needed for public assets |
| Upload malware scan | Uploaded files scanned by AWS Malware Protection for S3 on upload; quarantined if threat detected; admin notified |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| CloudFront invalidation quota (3,000/distribution/day) | Counter shown in invalidation modal; blocked at 2,900 with warning; emergency override available to Platform Admin |
| S3 bucket policy conflict during upload | Presigned URL generation fails → "Upload failed: bucket policy denied. Contact Platform Admin." |
| Brotli compression fails for a file | Celery job marks file as `compression_failed`; amber badge on file in browser; manual retry available |
| Asset deleted but still referenced in HTMX template | No automatic detection; engineer must verify before deletion; post-delete CDN errors in C-04 will surface broken references |
| S3 versioning rollback creates duplicate content-hash | Handled gracefully: `platform_asset_registry` creates new entry with same hash but new `uploaded_at`; both entries visible in version history |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| S3 ListObjects for asset browser | Paginated (max 1,000 per call); directory tree loaded lazily on expand; cached 10 min in Memcached |
| CloudFront metrics | Same CloudWatch batching pattern as C-04; metrics in `us-east-1` (CloudFront global namespace) |
| Asset browser search | Client-side filter for < 500 files per directory; server-side for larger directories |
| Upload throughput | Browser-direct presigned URL upload to S3; no server bandwidth used; S3 can handle 3,500 PUT/s per prefix |
| Invalidation status polling | 15s HTMX poll only while InProgress invalidations exist; stops polling when all completed |

---

## Amendment — G3: Performance Monitor Tab

**Gap addressed:** Frontend Engineer had no view of Core Web Vitals (LCP/FID/CLS), JS error rate, or real-user latency percentiles. Performance regressions went undetected until user complaints.

### New Tab on CDN & Asset Manager — Performance Monitor

**Access:** `/engineering/cdn/?tab=performance` — top-level tab alongside Invalidation and Asset Browser tabs.

**Data source:** AWS CloudWatch RUM (Real User Monitoring) — JavaScript agent embedded in portal pages collects real-user data and streams it to CloudWatch RUM.

**Layout:**

**Page Path Selector:**
- Dropdown of top-50 tracked page paths (e.g., `/dashboard/` · `/exam/take/` · `/results/` · `/login/`)
- "All pages" aggregate view as default
- Time range picker: Last 1h · 6h · 24h · 7 days · 30 days

**Core Web Vitals Panel (4 metrics, per selected page/time range):**

| Metric | Good | Needs Improvement | Poor | Description |
|---|---|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5–4s | > 4s | Time until main content visible |
| FID (First Input Delay) | < 100ms | 100–300ms | > 300ms | Time until page responds to first click |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1–0.25 | > 0.25 | Visual stability score |
| TTFB (Time to First Byte) | < 800ms | 800ms–1.8s | > 1.8s | Server response latency |

Each metric shown as: P75 value · P95 value · colour badge (green/amber/red) · 7-day trend sparkline

**Alert Threshold Config (per metric):**
- LCP amber threshold: configurable (default 2.5s) · red threshold (default 4s)
- Saved per-Frontend-Engineer; affects badge colour in this view only (not a platform-wide alert)

**JS Error Rate Panel:**
- Error rate %: JS errors / page views (last 24h)
- Top 5 error messages: error message · count · affected page paths · first seen · last seen
- Error trend: 7-day daily bar chart
- Each error row clickable → `cdn-perf-drawer` with full stack trace samples

**Page Load Time Trend:**
- Line chart: median page load time per day (7 days)
- Overlay: P95 line

**Device / OS Breakdown:**
- Pie chart: Desktop vs Mobile vs Tablet split
- Top OS + browser versions table (sorted by session count)

**cdn-perf-drawer (per page path row):**
- Web Vitals Trend: 30-day daily chart for all 4 metrics
- Error Log: top errors for this path with stack traces
- Device Breakdown: pie chart for this specific path
- Geographic breakdown: top 5 states (India) by session count + LCP P75 per state

**Data Flow:**
- CloudWatch RUM API: `GetAppMonitorData` called with metric filters per page path; results cached Memcached 5 min
- Error data: `GetAppMonitorData` with `event_type = "com.amazon.rum.js_error_event"`; cached 5 min
- No additional infrastructure required — CloudWatch RUM already deployed; only the portal UI to query it is new
| CDN cost data freshness | AWS Cost Explorer has 1-day delay; data shown with "(as of yesterday)" note; real-time estimate calculated from CloudFront bandwidth × pricing table |
