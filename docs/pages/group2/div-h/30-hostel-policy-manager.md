# 30 — Hostel Policy Manager

> **URL:** `/group/hostel/policy/`
> **File:** `30-hostel-policy-manager.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Hostel Director (primary — create/publish) · All hostel roles (view)

---

## 1. Purpose

Central repository for all hostel policies and standard operating procedures (SOPs) across the group. The Hostel Director creates, versions, and publishes policies that apply to all branches. Branch wardens and hostel staff access their branch portal's policy section — but the authoritative source is always the group-level Policy Manager.

**Policy categories:**
- Hostel Admission Policy (eligibility, seat allocation, preferences)
- Fee Policy (payment schedule, late fee, waiver criteria)
- Welfare Policy (Severity classification, escalation protocol, POCSO SOP)
- Security Policy (visitor protocols, CCTV, night security, biometric)
- Mess Policy (menu standards, hygiene standards, FSSAI compliance)
- Medical Policy (medical room standards, emergency protocol)
- Discipline Policy (prohibited conduct, case procedure, appeals)
- Housekeeping Policy (cleanliness standards, laundry frequency)
- Calling Hours Policy (daily phone call slots, restrictions)
- Leave Policy (hosteler leave types, approval process)
- Parent Visit Policy (visiting hours, pre-registration, gender-specific rules)

---

## 2. Page Layout

### 2.1 Breadcrumb
```
Group HQ  ›  Hostel Management  ›  Policy Manager
```

### 2.2 Page Header
- **Title:** `Hostel Policy Manager`
- **Subtitle:** `[N] Active Policies · [N] Draft Policies · [N] Archived`
- **Right controls:** `+ New Policy` · `Advanced Filters` · `Export All Policies`

---

## 3. Policy Table

**Search:** Policy title, category, keyword. 300ms debounce.

**Filters:** Category · Status (Draft/Active/Archived) · Applicability (All branches/Specific branches/Boys only/Girls only/Large groups only).

**Columns:**
| Column | Sortable |
|---|---|
| Policy Title | ✅ |
| Category | ✅ |
| Version | ✅ |
| Applicability | ✅ |
| Status | ✅ |
| Published Date | ✅ |
| Published By | ✅ |
| Next Review Date | ✅ (amber if overdue) |
| Actions | ❌ |

---

## 4. Drawers

### 4.1 Drawer: `policy-create`
- **Trigger:** + New Policy
- **Width:** 600px
- **Fields:**
  - Policy Title
  - Category (dropdown from list above)
  - Applicability (All Branches / Specific branches multi-select / Boys hostels only / Girls hostels only / Large groups only)
  - Effective Date
  - Review Date (mandatory — policies must be reviewed periodically)
  - Policy Content (rich text editor — headings, bullets, tables supported)
  - Document Upload (optional PDF attachment)
  - Status: Draft / Active
  - Notify all branch principals when published (checkbox)
- **On publish (Active status):** All branch principals receive WhatsApp notification with policy title + summary

### 4.2 Drawer: `policy-detail`
- **Trigger:** Table → row or title
- **Width:** 640px
- **Tabs:** Content · Version History · Applicability · Acknowledgements
- **Content tab:** Full policy text (rendered) + PDF download
- **Version History:** All past versions with dates and changed-by
- **Applicability tab:** Which branches this policy applies to + branch acknowledgement status
- **Acknowledgements tab:** Which branch principals have acknowledged receiving this policy

### 4.3 Modal: Archive Policy
- **Fields:** Reason for archiving · Replacement policy (optional link to new policy)

---

## 5. Policy Acknowledgement Tracker

> Track which branches have acknowledged each active policy.

**Display:** Toggle on any policy row → shows: Branch | Principal Name | Acknowledged? | Acknowledged At

Amber rows for branches that have not acknowledged a policy within 7 days of publication.

---

## 6. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Policy saved as draft | "Policy '[Title]' saved as Draft." | Info | 3s |
| Policy published | "Policy '[Title]' published. [N] branch principals notified." | Success | 4s |
| Policy archived | "Policy '[Title]' archived." | Info | 4s |
| Acknowledgement reminder sent | "Acknowledgement reminder sent to [N] branches." | Info | 4s |

---

## 7. Role-Based UI Visibility

| Element | Hostel Director G3 | All Other Hostel Roles |
|---|---|---|
| Create Policy | ✅ | ❌ |
| Publish / Archive | ✅ | ❌ |
| View all policies | ✅ | ✅ (read-only) |
| Send acknowledgement reminder | ✅ | ❌ |
| Download PDF | ✅ | ✅ |

---

## 8. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/hostel/policies/` | JWT (G3+) | All policies |
| POST | `/api/v1/group/{group_id}/hostel/policies/` | JWT (G3+) | Create policy |
| GET | `/api/v1/group/{group_id}/hostel/policies/{id}/` | JWT (G3+) | Policy detail + versions |
| PATCH | `/api/v1/group/{group_id}/hostel/policies/{id}/` | JWT (G3+) | Edit draft |
| POST | `/api/v1/group/{group_id}/hostel/policies/{id}/publish/` | JWT (G3+) | Publish |
| POST | `/api/v1/group/{group_id}/hostel/policies/{id}/archive/` | JWT (G3+) | Archive |
| GET | `/api/v1/group/{group_id}/hostel/policies/{id}/acknowledgements/` | JWT (G3+) | Branch acks |
| POST | `/api/v1/group/{group_id}/hostel/policies/{id}/remind-acknowledgement/` | JWT (G3+) | Send reminder |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
