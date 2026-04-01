# 19 — Policy Management

> **URL:** `/group/gov/policies/`
> **File:** `19-policy-management.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Chairman G5 · MD G5 · CEO G4 · President G4 (Academic) · VP G4 (Ops) · Trustee G1 · Advisor G1 (read)

---

## 1. Purpose

Versioned group-wide policy management — replaces emailing PDFs to 50 branch principals.
Every policy published here is tracked for acknowledgement per principal. A principal who hasn't
acknowledged a policy within the deadline triggers an automated reminder.

Policy types: Academic · HR · Finance · Safety · IT · Compliance.

Acknowledgement creates a legal record — important for POCSO, DPDP, and CBSE compliance audits.

---

## 2. Role Access

| Role | Can Create/Edit | Can Publish | Can View | Can Delete |
|---|---|---|---|---|
| Chairman | ✅ | ✅ | All | ✅ |
| MD | ✅ | ✅ | All | ✅ |
| CEO | ✅ | ✅ | All | ❌ |
| President | ✅ Academic only | ✅ | Academic | ❌ |
| VP | ✅ Ops/Safety only | ✅ | Ops/Safety | ❌ |
| Trustee | ❌ | ❌ | All | ❌ |
| Advisor | ❌ | ❌ | All | ❌ |
| Exec Secretary | ❌ | ❌ | ❌ | ❌ |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Policy Management
```

### 3.2 Page Header
```
Group Policy Management                                [+ New Policy]  [Export Acknowledgements ↓]
[N] policies published · [N] pending acknowledgements (MD/CEO/Chairman only)
```

### 3.3 Summary Stats Bar
| Stat | Value |
|---|---|
| Total Published Policies | N |
| Pending Acknowledgements | N (principals across N policies) |
| Fully Acknowledged Policies | N |
| Policies Due for Review | N (review date <30 days) |

---

## 4. Policy Table

**Search:** Policy name, category. Debounce 300ms.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Category | Multi-select | Academic · HR · Finance · Safety · IT · Compliance |
| Status | Multi-select | Draft · Published · Archived |
| Scope | Multi-select | All Branches · Specific Branches only |
| Acknowledgement | Select | All · Fully Acknowledged · Pending · Not Required |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Policy Name | Text + link | ✅ | Opens `policy-view` drawer |
| Category | Badge | ✅ | |
| Version | Text | ✅ | v1.0, v1.1, v2.0 etc. |
| Status | Badge | ✅ | Draft · Published · Archived |
| Published Date | Date | ✅ | |
| Effective From | Date | ✅ | |
| Review Due | Date | ✅ | Red if <30 days away |
| Scope | Badge | ✅ | All Branches · Partial |
| Ack Required | Yes/No | ✅ | |
| Ack Rate | Progress bar + fraction | ✅ | e.g. "42 / 50" — red if <100% and deadline passed |
| Ack Deadline | Date | ✅ | Red if past due |
| Actions | — | ❌ | View · Edit (draft only) · Publish · Archive · Delete |

**Default sort:** Published Date descending.

**Pagination:** 25/page.

**Row actions:**
| Action | Condition | Notes |
|---|---|---|
| View | Always | Opens `policy-view` drawer |
| Edit | Status = Draft | Opens `policy-create` drawer pre-filled |
| Publish | Status = Draft | Opens publish confirm modal |
| Archive | Status = Published | Opens archive confirm modal |
| Delete | Status = Draft + Chairman/MD | Opens delete confirm modal |
| Send Reminder | Published + Ack pending | Sends WhatsApp to non-acknowledging principals |

---

## 5. Drawers & Modals

### 5.1 Drawer: `policy-create` — Create / Edit Policy
- **Trigger:** [+ New Policy] or Edit row action
- **Width:** 680px
- **Tabs:** Content · Scope · Acknowledgement · Publish

#### Tab: Content
| Field | Type | Required | Validation |
|---|---|---|---|
| Policy Name | Text | ✅ | Min 5, max 200 chars |
| Category | Select | ✅ | Academic · HR · Finance · Safety · IT · Compliance |
| Version | Text | ✅ | Format: v{major}.{minor} — e.g. v2.1 |
| Summary | Textarea | ✅ | Min 50, max 500 chars (shown to principals before full doc) |
| Policy Document | Rich text editor (TipTap) | Conditional | Min 200 chars (required if no PDF uploaded) |
| OR Upload PDF | File upload | Conditional | PDF only · Max 25MB · replaces rich text |
| Effective From | Date | ✅ | |
| Review Due Date | Date | ✅ | Must be after Effective From |
| Previous Version Reference | Text | ❌ | e.g. "Supersedes v1.2" |

#### Tab: Scope
| Field | Type | Required | Validation |
|---|---|---|---|
| Applies To | Radio | ✅ | All Branches · Select Specific Branches |
| Select Branches | Multi-select | Conditional | Required if "Select Specific Branches" |
| Applies To Roles | Multi-select | ✅ | All Staff · Teaching Only · Non-Teaching · Principals only · etc. |

#### Tab: Acknowledgement
| Field | Type | Required | Validation |
|---|---|---|---|
| Require Acknowledgement | Toggle | ✅ | Default: On |
| Acknowledgement From | Select | Conditional | Principals only · All staff · Both |
| Deadline | Date | Conditional | Required if Ack required · Must be after Effective From |
| Reminder Schedule | Select | ❌ | 3 days before · 1 day before · Day of deadline · 1 day after |
| Force Acknowledge | Toggle | ❌ | If on: principal must acknowledge before accessing their portal |

#### Tab: Publish
- Preview of policy details before publishing
- [Publish Now] or [Save as Draft] buttons
- **Publish warning:** "Once published, this policy will be sent to [N] principals via WhatsApp/Email.
  They will be notified immediately."

**Submit:** "Save as Draft" or "Publish Policy" — both available from any tab (tab validation checked).

### 5.2 Drawer: `policy-view` — View Policy + Acknowledgements
- **Trigger:** Policy table row click or View action
- **Width:** 640px
- **Tabs:** Content · Versions · Acknowledgements

#### Tab: Content
- Full policy document rendered (rich text or PDF viewer)
- Metadata: Category, Version, Published date, Effective from, Review due
- Scope: Branches, Roles

#### Tab: Versions
- Table: Version · Published Date · Published By · Change Summary
- [Download PDF] for each version
- [Compare with Previous] → opens diff view side-by-side (if both are rich text)

#### Tab: Acknowledgements
- Stats row: Acknowledged N · Pending N · Not Required N (for branches out of scope)
- Table: Principal Name · Branch · Acknowledged? · Acknowledged At · Reminder Count
- Sortable by Acknowledged status
- [Resend Reminder] per principal row (MD/CEO/Chairman only)
- [Resend All Pending] button at top (sends WhatsApp to all non-acknowledged principals)
- Export CSV of acknowledgement status

### 5.3 Modal: `policy-publish-confirm`
- **Width:** 420px
- **Content:** "Publish [Policy Name] v[X.X]?" · "Will notify [N] principals. Cannot be edited after publishing."
- **Fields:** Optional publishing note to accompany notification
- **Buttons:** [Publish] + [Cancel]

### 5.4 Modal: `policy-archive-confirm`
- **Width:** 380px
- **Content:** "Archive [Policy Name]? It will no longer be visible to principals."
- **Buttons:** [Archive] + [Cancel]

---

## 6. Charts

### 6.1 Acknowledgement Rate by Category
- **Type:** Horizontal bar chart
- **Data:** Avg acknowledgement % per category
- **Colour:** Green >90% · Yellow 70–90% · Red <70%
- **Export:** PNG

### 6.2 Policy Acknowledgement Over Time (selected policy)
- **Trigger:** View in `policy-view` drawer Acknowledgements tab
- **Type:** Area line chart — cumulative acknowledgement % vs days since published
- **Benchmark line:** Deadline (vertical dashed line)
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Policy saved as draft | "Policy saved as draft" | Info | 4s |
| Policy published | "Policy published and [N] principals notified" | Success | 4s |
| Policy archived | "Policy archived" | Info | 4s |
| Reminder sent | "Acknowledgement reminder sent to [N] principals" | Success | 4s |
| Policy deleted | "Draft policy deleted" | Warning | 6s |
| PDF upload error | "PDF upload failed. Check file size and format." | Error | Manual |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No policies | "No policies published" | "Create your first group-wide policy" | [+ New Policy] |
| No drafts | "No draft policies" | "All policies are published" | — |
| All acknowledged | "Fully acknowledged" | "All principals have acknowledged this policy" | — |
| No search results | "No policies match" | "Try different search terms or clear filters" | [Clear Filters] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + table (10 rows) |
| Policy view drawer | Spinner in drawer + tab skeleton |
| PDF viewer in drawer | PDF loading indicator |
| Acknowledgement tab in drawer | Table skeleton rows |
| Reminder send | Spinner in Send Reminder button |
| Policy publish | Full-page overlay "Publishing policy…" |

---

## 10. Role-Based UI Visibility

| Element | Chairman/MD | CEO | President | VP | Trustee/Advisor |
|---|---|---|---|---|---|
| [+ New Policy] | ✅ | ✅ | ✅ (Academic) | ✅ (Ops/Safety) | ❌ |
| Edit row action | ✅ | ✅ (own) | ✅ (Academic draft) | ✅ (Ops draft) | ❌ |
| Publish row action | ✅ | ✅ | ✅ (Academic) | ✅ (Ops/Safety) | ❌ |
| Archive / Delete | ✅ | ❌ | ❌ | ❌ | ❌ |
| Acknowledgements tab | ✅ | ✅ | ✅ | ✅ | ❌ |
| [Send Reminder] | ✅ | ✅ | ✅ | ✅ | ❌ |
| [Export Acknowledgements] | ✅ | ✅ | ✅ | ✅ | ❌ |
| View policy content | ✅ | ✅ | ✅ (Academic) | ✅ (Ops) | ✅ |
| Force Acknowledge toggle | Chairman/MD | ❌ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/policies/` | JWT | Policy list |
| POST | `/api/v1/group/{id}/policies/` | JWT (G4+) | Create policy draft |
| GET | `/api/v1/group/{id}/policies/{pid}/` | JWT | Policy detail |
| PUT | `/api/v1/group/{id}/policies/{pid}/` | JWT (G3+) | Update draft |
| POST | `/api/v1/group/{id}/policies/{pid}/publish/` | JWT (G3+) | Publish policy |
| POST | `/api/v1/group/{id}/policies/{pid}/archive/` | JWT (G5/G4) | Archive |
| DELETE | `/api/v1/group/{id}/policies/{pid}/` | JWT (G5) | Delete draft |
| GET | `/api/v1/group/{id}/policies/{pid}/acknowledgements/` | JWT | Ack status list |
| POST | `/api/v1/group/{id}/policies/{pid}/remind/` | JWT (G3+) | Send reminder to pending |
| GET | `/api/v1/group/{id}/policies/{pid}/versions/` | JWT | Version history |
| GET | `/api/v1/group/{id}/policies/export-acks/?pid={pid}` | JWT | Export ack CSV |

---

## HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Tab switch (Active · Draft · Archived) | `click` | GET `.../policies/?tab=active\|draft\|archived` | `#policies-tab-content` | `innerHTML` |
| Search policies | `input delay:300ms` | GET `.../policies/?q=` | `#policies-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../policies/?category=&scope=&date=` | `#policies-table-section` | `innerHTML` |
| Sort column | `click` | GET `.../policies/?sort=&dir=` | `#policies-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../policies/?page=` | `#policies-table-section` | `innerHTML` |
| Open policy create drawer | `click` | GET `.../policies/new/` | `#drawer-body` | `innerHTML` |
| Open policy view drawer | `click` | GET `.../policies/{pid}/` | `#drawer-body` | `innerHTML` |
| Policy drawer tab switch | `click` | GET `.../policies/{pid}/?tab=content\|versions\|acknowledgements` | `#policy-drawer-tab` | `innerHTML` |
| Send acknowledgement reminder | `click` | POST `.../policies/{pid}/reminders/` | `#reminder-result-{pid}` | `innerHTML` |
| Publish policy | `click` | POST `.../policies/{pid}/publish/` | `#policy-row-{pid}` | `outerHTML` |
| Archive policy | `click` | POST `.../policies/{pid}/archive/` | `#policy-row-{pid}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
