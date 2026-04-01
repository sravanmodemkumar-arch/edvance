# Page 47: IT Knowledge Base

**URL:** `/group/it/support/knowledge-base/`
**Roles:** Group IT Support Executive (Role 57, G3) — create/edit articles; Group IT Admin (Role 54, G4) — full admin
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

Self-service IT knowledge base for branch staff and IT support. The knowledge base contains articles that help branch staff resolve common EduForge issues independently, without needing to raise a support ticket. This reduces ticket volume, speeds up resolution, and empowers branch staff to handle routine issues.

**Knowledge base objectives:**
- Enable branch staff to find answers to common questions via search
- Provide IT Support Executives with article links to include in ticket responses
- Reduce repeat tickets for the same issues
- Maintain up-to-date guidance as the platform evolves

**Article categories:**
- **Login Issues** — password reset, 2FA problems, account locked, wrong credentials
- **Portal Navigation** — finding features, menu structure, role-based visibility confusion
- **Feature Guides** — step-by-step guides for key workflows (fee collection, student registration, attendance, reports)
- **Troubleshooting** — error messages, slow performance, browser compatibility, mobile app issues
- **Integration Guides** — how to use EduForge integrations (WhatsApp notifications, payment gateways, SSO)

Branch staff can search the knowledge base from their branch portal (read-only view). This Group IT page is the management interface for creating and maintaining articles.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Admin (Role 54, G4) | Full admin | Create, edit, publish, archive, delete articles; view all stats |
| Group IT Support Executive (Role 57, G3) | Create/edit | Create and edit articles; can publish; cannot delete or archive others' articles |
| Group IT Director (Role 53, G4) | Read + export | View all articles and stats |
| Branch staff (via branch portal) | Public read | Can search and read published articles only — no management access |
| All other roles (Group portal) | No management access | Cannot access this management page |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > IT Support > Knowledge Base`

**Page Header:**
- Title: `IT Knowledge Base`
- Subtitle: `Self-service IT articles for branch staff and support executives`
- Right side: `+ Create Article` button (Role 54/57), `Export Article List (CSV)` (Role 54)

**Alert Banners:**

1. **Stale Articles** (amber, dismissible per session):
   - Condition: any published article with last_updated_date > 90 days ago
   - Text: `[X] articles haven't been updated in over 90 days. Review for accuracy as the platform evolves.`

2. **Draft Articles Pending Review** (blue, informational):
   - Condition: any articles with status = Draft for > 14 days
   - Text: `[X] article drafts have been waiting for review for more than 14 days. Review and publish or discard.`

---

## 4. KPI Summary Bar

Three KPI cards in a 3-column grid (or 3 of a 6-column grid to maintain visual consistency).

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Total Articles | Count of all articles (all statuses) | Plain number |
| 2 | Articles Published | Count where status = Published | Number, green |
| 3 | Avg Article Helpfulness Rating | Average of (helpful_votes / total_votes × 100) across all published articles with ≥ 5 ratings | % — with tooltip `Based on thumbs up/down feedback from branch staff` |

---

## 5. Main Table — Article List

**Table Title:** `Knowledge Base Articles`

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Article Title | Text link | Clickable — opens View Article drawer |
| Category | Badge | Login Issues / Portal Navigation / Feature Guides / Troubleshooting / Integration Guides |
| Sub-Category | Text | e.g., "Password Reset", "Fee Collection", "WhatsApp Integration" |
| Author | Text | Name of creator |
| Published Date | Date | Date first published; `—` if still Draft |
| Last Updated | Date | Last edit date; amber if > 90 days |
| Views (30d) | Number | Page views in last 30 days |
| Helpful % | % | (helpful_votes / (helpful_votes + not_helpful_votes)) × 100; `—` if < 5 ratings |
| Status | Badge | Published (green) / Draft (grey) / Archived (red outline) |
| Actions | Buttons | `View` / `Edit` (Role 54/57) / `Archive` (Role 54) / `Publish` (if Draft — Role 54/57) |

### Filters

- **Category:** All / Login Issues / Portal Navigation / Feature Guides / Troubleshooting / Integration Guides
- **Status:** All / Published / Draft / Archived
- **Author:** Dropdown of article authors

### Search

Full-text search on article title, sub-category, and tags. `hx-trigger="keyup changed delay:400ms"`, targets `#kb-table`.

### Pagination

Server-side, 20 rows per page. `hx-get="/group/it/support/knowledge-base/table/?page=N"`, targets `#kb-table`.

### Sorting

Sortable: Title, Category, Published Date, Last Updated, Views (30d), Helpful %. Default sort: Last Updated descending (most recently edited first).

---

## 6. Drawers

### A. Create / Edit Article Drawer (560px, right-side — Role 54/57)

Single drawer used for both Create (empty form) and Edit (pre-populated form).

**Drawer Header:** `Create Article` or `Edit Article: [Title]`

**Sections:**

**Article Metadata:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Title | Text input | Yes | Clear, descriptive title (max 100 chars) |
| Category | Dropdown | Yes | Login Issues / Portal Navigation / Feature Guides / Troubleshooting / Integration Guides |
| Sub-Category | Text input | Yes | More specific topic within category |
| Tags | Tag input | No | Comma-separated tags for better search; e.g., "password, login, 2FA" |
| Related Articles | Search/select | No | Link to other KB articles that are related (multi-select; searches by title) — optional, multi-select, search by title to link related KB articles. |

**Article Body:**
- Rich text editor (TipTap or similar Django-compatible)
- Toolbar: Bold, Italic, Heading 1/2/3, Bullet list, Ordered list, Blockquote, Code block, Link, Image upload
- Image upload → Cloudflare R2 (max 5MB per image, 10 images per article)
- Embedded images served via Cloudflare CDN (public read, signed write)
- Article Body: required when publishing (not required for draft); rich text; no raw script tags.

**SEO / Search Optimisation:**
- Meta description (optional, 160 chars max — used in branch portal search snippets)

**Publishing Options (footer of form):**
- `Publish` — saves and sets status = Published immediately
- `Save as Draft` — saves as Draft, not visible to branch staff yet
- `Cancel`

On Publish: Title, Category, Sub-Category, and Article Body are all required. If any missing, error shown: "Please complete title, category, and article body before publishing."

**Edit mode additional option:**
- `Archive Article` (Role 54 only) — sets status = Archived

On publish: `hx-post="/api/v1/it/knowledge-base/"` or `hx-put` for edit. Table refreshes. Toast: `Article "[Title]" published.` or `Article saved as draft.`

---

### B. View Article Drawer (560px, right-side — all roles)

Triggered by `View` button or clicking article title.

**Drawer Header:** `[Article Title]` + Status badge + Category badge

**Content:**
- Category / Sub-Category breadcrumb
- Author + Published Date + Last Updated
- Article body (rendered HTML from rich text editor)
- Related Articles (links to other KB articles)
- Tags (displayed as chips)

**Helpfulness Feedback Widget (read-only on management side):**
- Shows: `[X] staff found this helpful / [Y] total ratings` with visual progress bar
- Note: Rating is submitted by branch staff from their portal view

**Usage Stats (management view only):**
- Views (30d): [X]
- Views (all time): [X]
- Linked in tickets: [X] times (count of tickets where this article was referenced)

**Footer:** `Close` | `Edit Article` (Role 54/57) | `Archive` (Role 54 only, if Published)

---

### C. Archive Article Confirmation (440px — Role 54 only)

Triggered by `Archive` button.

**Fields:**
- Warning: `Archiving this article will hide it from branch staff. Ticket links to this article will show "Article Archived".`
- Confirm checkbox

**Footer:** `Confirm Archive` / `Cancel`

---

## 7. Charts

Two charts below the main table in a 2-column grid.

### Chart 1: Top 10 Most Viewed Articles (Last 30 Days)
- **Type:** Horizontal bar chart
- **Y-axis:** Article titles (truncated to 40 chars)
- **X-axis:** View count
- **Colour:** Category colour coding
- **Purpose:** Identify which articles are most used — verify they are up-to-date, and identify gaps (high-view articles may indicate persistent confusion)
- **Data endpoint:** `/api/v1/it/knowledge-base/charts/top-articles/`

### Chart 2: Articles by Category
- **Type:** Donut chart
- **Segments:** Each article category with count and %
- **Purpose:** Identify whether the knowledge base is balanced across categories or over-concentrated
- **Data endpoint:** `/api/v1/it/knowledge-base/charts/by-category/`

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Article published | Success: `Article "[Title]" published and visible to branch staff.` |
| Article saved as draft | Info: `Article saved as draft. Publish when ready.` |
| Article updated | Success: `Article "[Title]" updated.` |
| Article archived | Success: `Article "[Title]" archived. No longer visible to branch staff.` |
| Image uploaded | Info: `Image uploaded.` |
| Image upload failed | Error: `Image upload failed. File must be under 5MB.` |
| Export initiated | Info: `Exporting article list.` |
| Validation error | Error: `Please enter a title, category, and article body before publishing.` |
| Article too long | Warning: `Article body is very long (>5,000 words). Consider splitting into multiple articles.` |
| Article publish failed | Error: `Failed to publish article. Check for unsaved changes and try again.` | Error | 5s |
| Image upload failed (too large) | Error: `Image exceeds 5MB limit. Please compress and try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No articles created | Icon + `No articles yet. Create your first knowledge base article to help branch staff.` |
| No articles match filters | `No articles match the selected filters. Try a different category or status.` |
| No search results | `No articles found for "[search term]". Try different keywords.` |
| Charts — no data | `Not enough article view data to display. Check back after articles have been published.` |
| No related articles to link | In create/edit drawer: `No other articles available to link yet.` |
| No helpfulness ratings | In view drawer: `No staff feedback yet. Ratings appear after branch staff read and rate this article.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 3 skeleton shimmer cards |
| Article table | 5 skeleton rows |
| Create/Edit drawer (edit mode) | Spinner while loading article content into editor |
| View drawer | Spinner then article content fades in |
| Rich text editor | Loading indicator while editor JS initialises |
| Image upload | Progress bar in editor toolbar |
| Charts | Spinner in chart containers |
| Publish/Save buttons | `Publishing...` / `Saving...` + disabled |

---

## 11. Role-Based UI Visibility

| UI Element | Role 57 (G3) | Role 54 (G4) | Role 53 (G4) |
|------------|-------------|-------------|-------------|
| Create Article button | Visible | Visible | Hidden |
| Edit button | Visible (own articles + unowned) | Visible (all) | Hidden |
| Publish button (from draft) | Visible | Visible | Hidden |
| Archive button | Hidden | Visible | Hidden |
| Delete (not implemented — articles are archived not deleted for audit) | N/A | N/A | N/A |
| View button | Visible | Visible | Visible |
| Usage stats in view drawer | Visible | Visible | Visible |
| Export CSV | Hidden | Visible | Visible |
| Author filter | Visible (self only) | Visible (all authors) | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/knowledge-base/` | Fetch article list (paginated) |
| POST | `/api/v1/it/knowledge-base/` | Create article (Role 54/57) |
| GET | `/api/v1/it/knowledge-base/{id}/` | Fetch article detail |
| PUT | `/api/v1/it/knowledge-base/{id}/` | Update article (Role 54/57) |
| POST | `/api/v1/it/knowledge-base/{id}/publish/` | Publish draft article |
| POST | `/api/v1/it/knowledge-base/{id}/archive/` | Archive article (Role 54) |
| POST | `/api/v1/it/knowledge-base/{id}/image/` | Upload image to Cloudflare R2 |
| GET | `/api/v1/it/knowledge-base/{id}/stats/` | Fetch article view and helpfulness stats |
| GET | `/api/v1/it/knowledge-base/kpis/` | Fetch KPI values |
| GET | `/api/v1/it/knowledge-base/charts/top-articles/` | Top 10 most viewed |
| GET | `/api/v1/it/knowledge-base/charts/by-category/` | Category distribution |
| GET | `/api/v1/it/knowledge-base/export/csv/` | Export article list |
| GET | `/api/v1/it/knowledge-base/search/` | Full-text search (used by branch portal) |
| GET | `/api/v1/it/knowledge-base/search/?q={query}` | JWT (G3+) | Full-text search on title, category, and tags |
| POST | `/api/v1/it/knowledge-base/{id}/rate/` | Submit helpfulness rating (branch portal only) |

---

## 13. HTMX Patterns

```html
<!-- Article table -->
<div id="kb-table"
     hx-get="/group/it/support/knowledge-base/table/"
     hx-trigger="load"
     hx-target="#kb-table"
     hx-include="#kb-filter-form">
</div>

<!-- Search with debounce -->
<input type="text" name="search" placeholder="Search articles..."
       hx-get="/group/it/support/knowledge-base/table/"
       hx-trigger="keyup changed delay:400ms"
       hx-target="#kb-table"
       hx-include="#kb-filter-form" />

<!-- Create article drawer -->
<button hx-get="/group/it/support/knowledge-base/create-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer(); initRichTextEditor()">
  + Create Article
</button>

<!-- Publish article -->
<form hx-post="/api/v1/it/knowledge-base/"
      hx-target="#kb-table"
      hx-swap="outerHTML"
      hx-on::after-request="closeDrawer(); refreshKPIs()">
  <!-- form fields including rich text content as hidden input -->
  <button type="submit" name="action" value="publish">Publish</button>
  <button type="submit" name="action" value="draft">Save as Draft</button>
</form>

<!-- Edit existing article -->
<button hx-get="/group/it/support/knowledge-base/{{ article.id }}/edit-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer(); initRichTextEditor()">
  Edit
</button>

<!-- View article drawer -->
<button hx-get="/group/it/support/knowledge-base/{{ article.id }}/view/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  View
</button>

<!-- Image upload (in rich text editor) -->
<form hx-post="/api/v1/it/knowledge-base/{{ article.id }}/image/"
      hx-encoding="multipart/form-data"
      hx-target="#image-upload-result"
      hx-swap="innerHTML">
  <input type="file" name="image" accept="image/*" />
</form>

<!-- Publish draft -->
<button hx-post="/api/v1/it/knowledge-base/{{ article.id }}/publish/"
        hx-target="#kb-table"
        hx-swap="outerHTML"
        hx-on::after-request="refreshKPIs()">
  Publish
</button>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
