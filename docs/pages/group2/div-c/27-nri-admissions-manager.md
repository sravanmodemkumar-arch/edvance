# Page 27: NRI Admissions Manager

**URL:** `/group/adm/nri-admissions/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions · Scholarship Section

---

## 1. Purpose

NRI (Non-Resident Indian) and foreign national admissions constitute a distinct category that requires separate management from the domestic admissions pipeline. NRI-quota students typically pay a significantly higher fee — commonly 3 to 5 times the general category fee — reflective of the commercial investment large private groups make in catering to the diaspora community. This revenue difference makes NRI admissions an important revenue stream for groups with the brand reputation and infrastructure to attract international families. However, the documentation, verification, and counselling complexity is proportionally higher.

The NRI Admissions Manager handles the complete NRI application pipeline: from initial inquiry through application, document verification (OCI cards, passports, foreign school marksheets, equivalency certificates), fee quotation, virtual counselling session scheduling, to final admission. A key complexity is transcript equivalency — a student who has been studying in the ICSE or CBSE equivalent in the UAE or the US will have foreign marks that need to be mapped to the Indian grading scale for class placement decisions. The page surfaces applications with pending document verification prominently so coordinators can follow up efficiently.

Virtual counselling is integral to this pipeline — parents based in Dubai, the US, or the UK will not travel to the school for an in-person session. The Group Demo Class Coordinator and Group Admission Counsellor manage these video sessions, which are tracked in Section 5.6. The NRI Fee Structure section (5.4) is managed exclusively by the Director — fee revisions for the NRI quota are a strategic decision and not left to coordinators. Country of origin data (Section 5.5) provides the Director with insight into which diaspora communities the group is reaching and where marketing investment is paying off.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (23) | G3 | Full — view, process, approve, edit NRI fees | Authority over NRI admissions overall |
| Group Admission Coordinator (24) | G3 | View all + process applications (accept/reject) | Cannot edit fee structure |
| Group Admission Counsellor (25) | G3 | Virtual counselling sessions management + view own assigned applications | Limited scope |
| Group Demo Class Coordinator (29) | G3 | Virtual sessions management + demo class scheduling for NRI candidates | Demo class scope |
| CEO | G1 | View only | Strategic oversight |
| Group Scholarship Manager (27) | G3 | No access | Different function scope |

**Enforcement:** `@role_required(['admissions_director', 'coordinator', 'counsellor', 'demo_coordinator', 'ceo'])`. NRI fee structure edit is enforced at API level: `if action == 'edit_fee' and role != 'admissions_director': return 403`. Counsellor is scoped to sessions they are assigned to via `assigned_counsellor == request.user`. Director has full scope.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → NRI Admissions → NRI Manager
```

### 3.2 Page Header
- **Title:** NRI & International Admissions Manager
- **Subtitle:** NRI quota applications — current admission cycle
- **Cycle Selector:** Dropdown for admission cycle
- **Action Buttons:** `[+ New NRI Application]` (Coordinator/Director) · `[Schedule Virtual Session]` · `[Export Applications]`

### 3.3 Alert Banner
Triggers:
- **Amber — Document Verification Pending:** "{n} NRI applications have documents awaiting verification. [Review →]"
- **Amber — Sessions Unconfirmed:** "{n} virtual counselling sessions are scheduled but not confirmed. [Confirm →]"
- **Red — NRI Seats Nearly Full:** "{n} branches have ≤ 2 NRI seats remaining. [View Seat Matrix →]"
- **Blue — Application Received:** "New NRI application received from {Country} for {Branch} — {Student Name}. [View →]"
- **Green — Admission Completed:** "{Student Name} (NRI) has completed admission to {Branch}."

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| NRI Applications This Cycle | COUNT of NRI applications in current cycle | `nri_application` | Blue always | → Section 5.1 full table |
| NRI Seats Available (Group) | SUM of (nri_seats_total – nri_enrolled) across all branches | `nri_seat_matrix` | Green > 0 · Amber ≤ 5 · Red = 0 | → Section 5.2 seat matrix |
| NRI Enrolled (Current Year) | COUNT of admitted NRI students with status = 'enrolled' | `nri_application` | Green always | → table filtered to enrolled |
| Pending Document Verification | COUNT where document_status != 'complete' and status != 'rejected' | `nri_application` | Amber > 0 · Green = 0 | → Section 5.3 doc verification |
| NRI Fee Collection Rate % | (Fees collected / Fees invoiced for NRI enrolled) × 100 | `nri_fee_collection` | Green ≥ 90% · Amber 70–89% · Red < 70% | → fee collection report |
| Countries of Origin | COUNT DISTINCT of country from active applications | `nri_application` | Blue always | → Section 5.5 |

**HTMX Refresh:** Every 5 minutes via `hx-trigger="every 5m"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 NRI Application Table

**Display:** Sortable, selectable, server-side paginated (20/page). Default sort: application_date DESC.

**Columns:**

| Column | Notes |
|---|---|
| Application ID | System ref, e.g., NRI-APP-2026-0043 |
| Student Name | Full name — linked to nri-application-detail drawer |
| Nationality | Flag emoji + country name |
| OCI/PIO/NRI Status | OCI (green chip) / PIO (blue chip) / NRI (amber chip) / Foreign National (grey chip) |
| Branch Preference | 1st preference (others shown in drawer) |
| Stream | MPC / BIPC / Commerce / Other |
| Class | Applying for class |
| Parent Location | City, Country |
| Documents Status | Complete (green ✓) / Partial (amber) / Pending (red ✗) |
| NRI Fee Quoted | ₹ formatted — annual |
| Application Date | DD-MMM-YYYY |
| Status | New (blue) / Under Review (amber) / Document Pending (orange) / Accepted (green) / Rejected (red) / Enrolled (teal) |
| Actions | `[View →]` · `[Accept]` · `[Reject]` |

**Filters:** Nationality, Branch, Status, Document status

**HTMX Pattern:** Filter changes → `GET /api/v1/group/{group_id}/adm/nri-admissions/applications/` targeting `#nri-table-body`.

**Empty State:** No NRI applications in this cycle. Heading: "No NRI Applications Yet." CTA: `[+ New NRI Application]`.

---

### 5.2 NRI Seat Matrix

**Display:** Table — one row per branch, columns by stream.

**Columns:**

| Column | Notes |
|---|---|
| Branch | Branch name + city |
| Stream | One column per stream offered (MPC / BIPC / Commerce / Arts) |
| NRI Seats Total | Per stream (typically 5% of intake) |
| NRI Enrolled | Count per stream |
| Available | Total – Enrolled — green if > 0 · red if = 0 |

**Note:** If no stream breakdown is configured, show single total/enrolled/available row per branch.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/nri-admissions/seat-matrix/` targeting `#nri-seat-matrix`.

**Empty State:** Seat matrix not configured. CTA: `[Configure NRI Seats]` (Director only).

---

### 5.3 Document Verification

**Display:** Alert list — NRI applications with pending document verification. Sorted by application_date ASC (oldest first).

**Required Documents (per application):**
- OCI Card / Passport copy (with visa if applicable)
- Foreign school marksheet(s)
- Transcript equivalency certificate (if required)
- Parent passport copy
- Proof of NRI status (employment proof / visa)

**Columns:** Application ID · Student Name · Country · Branch Preference · Missing Documents (comma list) · `[Request Documents →]` · `[View Application →]`

**`[Request Documents →]`:** Opens a modal to send a tailored document request via WhatsApp/email to the parent.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/nri-admissions/document-queue/` targeting `#nri-doc-queue`.

**Empty State:** All document verifications complete. Icon: file-check. Heading: "All Documents Verified."

---

### 5.4 NRI Fee Structure

**Display:** Card per branch — shows NRI-specific fee structure. Expandable accordion.

**Card per branch:**
- NRI Annual Tuition Fee (₹)
- NRI Hostel Fee (₹) — if applicable
- One-time Admission Charges (₹)
- NRI Caution Deposit (₹)
- `[Edit →]` button — **Director only**

**Accordion toggle:** Click branch name to expand/collapse.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/nri-admissions/fee-structure/` targeting `#nri-fee-structure`.

**Edit:** `[Edit →]` opens nri-fee-edit drawer (Director only).

---

### 5.5 Country of Origin

**Display:** Stat list — ranked by count of applications. No chart — clean text with count.

**Format:**
| Rank | Country | NRI Category | Applications | Enrolled |
|---|---|---|---|---|
| 1 | UAE | NRI | 18 | 12 |
| 2 | USA | NRI/OCI | 9 | 6 |
| 3 | UK | OCI/PIO | 7 | 5 |
| 4 | Qatar | NRI | 6 | 3 |
| 5 | India (Returning) | Returning NRI | 4 | 4 |
| Other | Various | — | 5 | 2 |

**Interaction:** Click a country row → filters Section 5.1 table to that country.

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/nri-admissions/country-stats/` targeting `#country-origin-list`.

---

### 5.6 Virtual Counselling Sessions

**Display:** Table — online counselling sessions for NRI/international applicants.

**Columns:**

| Column | Notes |
|---|---|
| Session ID | System ref |
| Student Name | Applicant name |
| Country | Country of residence |
| Scheduled Date & Time | IST datetime with timezone note |
| Counsellor | Assigned staff name |
| Mode | Video Call platform (Zoom / Google Meet / Teams) |
| Meeting Link | Masked (show on hover for privacy) |
| Status | Scheduled (blue) / Confirmed (green) / Completed (teal) / No-show (red) / Rescheduled (amber) |
| Actions | `[Confirm →]` · `[Reschedule →]` · `[Mark Complete]` · `[View Notes →]` |

**HTMX Load:** `hx-trigger="load"` → `GET /api/v1/group/{group_id}/adm/nri-admissions/virtual-sessions/` targeting `#virtual-sessions-table`.

**Empty State:** No virtual sessions scheduled. CTA: `[Schedule Virtual Session]`.

---

## 6. Drawers & Modals

### 6.1 NRI Application Detail Drawer
- **Width:** 640px
- **Trigger:** `[View →]` on table row or application ID
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/nri-admissions/applications/{application_id}/detail/`
- **Tabs:**
  1. **Student Profile** — Name, DOB, gender, class applying for, stream, branch preference(s)
  2. **Nationality Documents** — OCI/PIO/NRI status, document upload previews, verification status per document, expiry dates
  3. **Transcripts** — Foreign school name, country, marksheets (previews), equivalency certificate, proposed class placement
  4. **Fee Details** — NRI fee quoted, any special concessions, payment terms, fee collection status
  5. **Counselling Notes** — Notes from virtual sessions, counsellor observations, parent queries recorded
  6. **Decision** — Accept (with seat assignment — branch + stream + class) / Reject (with reason) / Request Documents

### 6.2 NRI Fee Edit Drawer
- **Width:** 480px
- **Access:** Director only
- **Trigger:** `[Edit →]` in Section 5.4
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/nri-admissions/fee-structure/{branch_id}/edit/`
- **Content:** Fee fields: NRI Tuition (₹ per year), Hostel fee (₹), One-time admission charges, Caution deposit. Effective from date. Notes field.
- **Submit:** `hx-put` → `/api/v1/group/{group_id}/adm/nri-admissions/fee-structure/{branch_id}/`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Application created | "NRI application NRI-APP-{id} created for {Student Name}." | Success | 4 s |
| Application accepted | "{Student Name}'s NRI application accepted. Seat assigned at {Branch}." | Success | 4 s |
| Application rejected | "{Student Name}'s NRI application rejected." | Info | 4 s |
| Document request sent | "Document request sent to {Student Name}'s parent ({Country})." | Info | 4 s |
| NRI fee updated | "NRI fee structure updated for {Branch}." | Success | 3 s |
| Virtual session scheduled | "Virtual session scheduled for {Student Name} — {Date} IST." | Success | 4 s |
| Session confirmed | "Session with {Student Name} confirmed." | Success | 3 s |
| Session marked complete | "Session with {Student Name} marked as completed." | Success | 3 s |
| No-show marked | "{Student Name} marked as no-show. Session can be rescheduled." | Warning | 5 s |
| Export queued | "NRI applications export is being prepared." | Info | 3 s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No NRI applications | Globe icon | "No NRI Applications Yet" | "No NRI applications have been received for this admission cycle." | `[+ New NRI Application]` |
| No document issues | File-check icon | "All Documents Verified" | "All NRI applicants have complete documents." | None |
| NRI seat matrix not configured | Table-x icon | "Seat Matrix Not Configured" | "Configure NRI seat allocations for each branch." | `[Configure NRI Seats]` (Director) |
| No virtual sessions | Video-x icon | "No Virtual Sessions" | "No virtual counselling sessions are scheduled." | `[Schedule Virtual Session]` |
| Filter returns no results | Search-x icon | "No Applications Match Filters" | "Try adjusting filter criteria." | `[Clear Filters]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | KPI shimmer (6 cards) + table skeleton (8 rows) |
| KPI auto-refresh | In-place spinner per card |
| Application table filter | Table skeleton (8 row shimmer) |
| NRI seat matrix load | Table skeleton (matrix layout shimmer) |
| Document queue load | Alert list skeleton (5 items) |
| NRI fee structure load | Accordion skeleton (branch cards) |
| Country origin list load | List skeleton (6 row shimmer) |
| Virtual sessions table load | Table skeleton (6 row shimmer) |
| Application detail drawer open | 640px drawer with 6 tab shimmers |
| NRI fee edit drawer open | 480px drawer with form field shimmers |
| Accept / reject action | Row-level inline spinner |

---

## 10. Role-Based UI Visibility

| Element | Director (23) | Coordinator (24) | Counsellor (25) | Demo Coord (29) | CEO |
|---|---|---|---|---|---|
| `[+ New NRI Application]` | Visible | Visible | Hidden | Hidden | Hidden |
| `[Accept]` / `[Reject]` actions | Visible | Visible | Hidden | Hidden | Hidden |
| `[Request Documents →]` | Visible | Visible | Hidden | Hidden | Hidden |
| Section 5.4 NRI Fee Structure | Visible (edit) | Visible (read) | Hidden | Hidden | Visible (read) |
| `[Edit →]` fee structure | Visible | Hidden | Hidden | Hidden | Hidden |
| Section 5.5 Country Origin | Visible | Visible | Visible | Hidden | Visible |
| Section 5.6 Virtual Sessions | Visible (full) | Visible (full) | Visible (own sessions) | Visible (own sessions) | Visible (read) |
| `[Schedule Virtual Session]` | Visible | Visible | Visible | Visible | Hidden |
| `[Mark Complete]` session | Visible | Visible | Visible (own) | Visible (own) | Hidden |
| `[Export Applications]` | Visible | Visible | Hidden | Hidden | Hidden |
| Decision tab in application drawer | Visible | Visible | Hidden | Hidden | Hidden |
| Counselling Notes tab | Visible | Visible | Visible (own) | Visible (own) | Visible |

*All UI visibility decisions made server-side in Django template. No client-side JS role checks.*

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/nri-admissions/kpis/` | JWT G3 | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/nri-admissions/applications/` | JWT G3 | Paginated, filtered NRI application list |
| POST | `/api/v1/group/{group_id}/adm/nri-admissions/applications/` | JWT G3 write | Create NRI application |
| GET | `/api/v1/group/{group_id}/adm/nri-admissions/applications/{application_id}/detail/` | JWT G3 | Application detail drawer fragment |
| POST | `/api/v1/group/{group_id}/adm/nri-admissions/applications/{application_id}/accept/` | JWT G3 write | Accept application |
| POST | `/api/v1/group/{group_id}/adm/nri-admissions/applications/{application_id}/reject/` | JWT G3 write | Reject application |
| POST | `/api/v1/group/{group_id}/adm/nri-admissions/applications/{application_id}/request-docs/` | JWT G3 write | Request missing documents |
| GET | `/api/v1/group/{group_id}/adm/nri-admissions/seat-matrix/` | JWT G3 | NRI seat matrix data |
| PUT | `/api/v1/group/{group_id}/adm/nri-admissions/seat-matrix/{branch_id}/` | JWT Director | Update NRI seat allocation |
| GET | `/api/v1/group/{group_id}/adm/nri-admissions/document-queue/` | JWT G3 | Document verification queue |
| GET | `/api/v1/group/{group_id}/adm/nri-admissions/fee-structure/` | JWT G3 | NRI fee structure (all branches) |
| GET | `/api/v1/group/{group_id}/adm/nri-admissions/fee-structure/{branch_id}/edit/` | JWT Director | Fee edit drawer fragment |
| PUT | `/api/v1/group/{group_id}/adm/nri-admissions/fee-structure/{branch_id}/` | JWT Director | Update NRI fee structure |
| GET | `/api/v1/group/{group_id}/adm/nri-admissions/country-stats/` | JWT G3 | Country of origin stats |
| GET | `/api/v1/group/{group_id}/adm/nri-admissions/virtual-sessions/` | JWT G3 | Virtual sessions table |
| POST | `/api/v1/group/{group_id}/adm/nri-admissions/virtual-sessions/` | JWT G3 write | Schedule virtual session |
| PUT | `/api/v1/group/{group_id}/adm/nri-admissions/virtual-sessions/{session_id}/` | JWT G3 write | Update session (confirm, reschedule) |
| POST | `/api/v1/group/{group_id}/adm/nri-admissions/virtual-sessions/{session_id}/complete/` | JWT G3 write | Mark session complete |
| GET | `/api/v1/group/{group_id}/adm/nri-admissions/export/applications/` | JWT G3 | Export applications CSV/PDF |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `.../nri-admissions/kpis/` | `#kpi-bar` | `innerHTML` |
| Filter application table | `change` on filter inputs | GET `.../nri-admissions/applications/?{filters}` | `#nri-table-body` | `innerHTML` |
| Paginate application table | `click` on page link | GET `.../nri-admissions/applications/?page={n}` | `#nri-table-container` | `innerHTML` |
| Sort application table | `click` on column header | GET `.../nri-admissions/applications/?sort={col}&dir={asc\|desc}` | `#nri-table-body` | `innerHTML` |
| Open application detail drawer | `click` on `[View →]` or student name | GET `.../nri-admissions/applications/{id}/detail/` | `#drawer-container` | `innerHTML` |
| Accept application (inline) | `click` on `[Accept]` | POST `.../nri-admissions/applications/{id}/accept/` | `#nri-row-{id}` | `outerHTML` |
| Reject application (inline) | `click` on `[Reject]` | POST `.../nri-admissions/applications/{id}/reject/` | `#nri-row-{id}` | `outerHTML` |
| Load seat matrix | `load` on section | GET `.../nri-admissions/seat-matrix/` | `#nri-seat-matrix` | `innerHTML` |
| Load document queue | `load` on section | GET `.../nri-admissions/document-queue/` | `#nri-doc-queue` | `innerHTML` |
| Request documents (modal) | `click` on `[Request Documents →]` | GET `.../nri-admissions/applications/{id}/doc-request-modal/` | `#modal-container` | `innerHTML` |
| Load fee structure | `load` on section | GET `.../nri-admissions/fee-structure/` | `#nri-fee-structure` | `innerHTML` |
| Open fee edit drawer | `click` on `[Edit →]` (Director) | GET `.../nri-admissions/fee-structure/{branch_id}/edit/` | `#drawer-container` | `innerHTML` |
| Submit fee edit | `submit` on fee form | PUT `.../nri-admissions/fee-structure/{branch_id}/` | `#fee-card-{branch_id}` | `outerHTML` |
| Load country origin stats | `load` on section | GET `.../nri-admissions/country-stats/` | `#country-origin-list` | `innerHTML` |
| Click country to filter table | `click` on country row | GET `.../nri-admissions/applications/?country={code}` | `#nri-table-body` | `innerHTML` |
| Load virtual sessions | `load` on section | GET `.../nri-admissions/virtual-sessions/` | `#virtual-sessions-table` | `innerHTML` |
| Mark session complete | `click` on `[Mark Complete]` | POST `.../nri-admissions/virtual-sessions/{id}/complete/` | `#session-row-{id}` | `outerHTML` |
| Refresh KPIs after accept/reject | `htmx:afterRequest` from accept/reject calls | GET `.../nri-admissions/kpis/` | `#kpi-bar` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
