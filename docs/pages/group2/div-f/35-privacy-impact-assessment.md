# 35 — Privacy Impact Assessment Manager

- **URL:** `/group/it/privacy/pia/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Data Privacy Officer (Role 55, G1) — Read + Review/Approve; Group IT Admin (Role 54, G4) — Create + Edit

---

## 1. Purpose

Privacy Impact Assessments (PIAs) are structured risk assessments required before any new system, feature, integration, or business process that involves collecting or processing personal data is deployed. Under DPDP Act 2023 and international best practice (aligned with GDPR's DPIA framework), a PIA is mandatory for any processing that is "likely to result in a high risk to the rights and freedoms of data subjects." This includes: implementing new student monitoring systems, integrating third-party analytics, deploying AI-based features using student data, adding biometric attendance tracking, connecting to government data portals, and launching new mobile applications.

In the EduForge context, a PIA is initiated by the IT Admin or the Integration Manager whenever a new feature or integration is being planned. The requestor completes a structured questionnaire — what personal data will be collected, from whom, for what purpose, where it will be stored, how long it will be retained, who will have access, and what risks exist. The questionnaire auto-scores the risk level based on yes/no answers. High-risk PIAs are routed to the IT Director for co-sign, and all PIAs must be approved by the Data Privacy Officer before the feature goes live.

The DPO is not a rubber stamp — they have authority to reject a PIA, which effectively blocks the deployment of the feature until the privacy concerns are adequately addressed. Rejection reasons must be documented. The IT Admin can then revise the PIA and resubmit. This creates a governance gate: no new data processing activity can go live without DPO sign-off.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Data Privacy Officer | G1 | Read-only + review + approve/reject | Independent reviewer; cannot create or edit PIAs |
| Group IT Admin | G4 | Create + edit + submit | Operational PIA management |
| Group EduForge Integration Manager | G4 | Create + edit + submit | For integration-related PIAs |
| Group IT Director | G4 | Read + approve high-risk PIAs | Co-approver for high-risk PIAs only |
| All other Division F roles | — | Hidden | No access |
| Group Cybersecurity Officer (Role 56, G1) | Read-only | Can review high-risk PIAs for security assessment input |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Data Privacy → Privacy Impact Assessments
```

### 3.2 Page Header
- **Title:** `Privacy Impact Assessment Manager`
- **Subtitle:** `DPDP Act 2023 — PIA Register · [N] Total · [N] Pending Review`
- **Role Badge:** `Group Data Privacy Officer` or `Group IT Admin`
- **Right-side controls (IT Admin / Integration Manager):** `+ Create PIA` · `Export`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| PIA submitted for review >30 days with no DPO action | "PIA '[Name]' has been waiting for DPO review for [N] days. PIAs must be reviewed promptly to avoid blocking deployments." | Amber |
| High-risk PIA approved by DPO but missing IT Director sign-off | "High-risk PIA '[Name]' approved by DPO but requires IT Director sign-off before deployment is permitted." | Amber |
| Feature known to be deployed without approved PIA | "A new feature or integration has been flagged as deployed without a completed PIA. Compliance violation — create PIA retrospectively." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| PIAs Total | All PIA records in the system | Blue | No filter |
| Approved | PIAs with status = Approved | Green | Filter by Approved |
| Pending Review | PIAs with status = Submitted or Under Review | Amber if > 0 | Filter by Pending |
| High Risk | PIAs with risk_level = High | Red if any Pending, Amber if all resolved | Filter by High Risk |

---

## 5. Main Table — PIA Register

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| PIA Name | Text (descriptive name — e.g., "Biometric Attendance System - PIA") | Yes | Yes (text search) |
| Scope | Badge (Feature / Integration / Process / Vendor / Other) | Yes | Yes (multi-select) |
| Initiator | Staff name | Yes | No |
| Data Types Involved | Tag list (Student PII / Staff PII / Financial / Health / Academic / Location) | No | Yes (multi-select) |
| Risk Level | Badge (High / Medium / Low) — auto-scored | Yes | Yes (multi-select) |
| Status | Badge (Draft / Submitted / Under Review / Approved / Rejected) | Yes | Yes (multi-select) |
| Created Date | Date | Yes | Yes (date range) |
| Approved/Rejected Date | Date or "—" | Yes | No |
| Actions | View / Edit / Review / Approve / Reject | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Scope | Multi-select checkbox | Feature / Integration / Process / Vendor / Other |
| Risk Level | Multi-select checkbox | High / Medium / Low |
| Status | Multi-select checkbox | Draft / Submitted / Under Review / Approved / Rejected |
| Data Types | Multi-select | All data type categories |
| Created Date | Date range picker | Any range |

### 5.2 Search
- PIA Name, scope description
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer (Wizard): `pia-create` — Create PIA
- **Trigger:** `+ Create PIA` button
- **Width:** 720px (wider to accommodate questionnaire form)
- **Multi-step wizard (5 steps with progress indicator):**

**Step 1: Scope Description**
- PIA Name (required, text)
- Scope Type (required, dropdown: Feature / Integration / Process / Vendor)
- Description (required, textarea — describe what activity this PIA covers, what is being built or deployed, who initiated it and why)
- Target Go-Live Date (date picker — helps prioritise review urgency)
- Affected Branches (multi-select)

**Step 2: Data Inventory**
- What personal data will be collected or processed? (multi-select checkboxes + free text additions):
  - Name, Contact details, Date of birth, Photo/Video, Location data, Academic records, Financial data, Health/Medical data, Biometric data, Special categories
- Whose data? (checkboxes: Students / Parents / Staff / Visitors / Other)
- How is the data collected? (checkboxes: Online Form / Mobile App / Physical Form / Automated System / Third Party / CCTV / Biometric)
- Where is data stored? (dropdown: AWS Mumbai / Cloudflare R2 India / EduForge PostgreSQL / Third-Party system (name required))
- How long will data be retained? (dropdown: Session only / 1 month / 1 year / Academic year / Indefinite / Per retention policy)
- Who has access? (checkboxes + text: Internal staff / Branch admin / Group IT / Third-party processor / Government)

**Step 3: Risk Questionnaire (20 yes/no questions — auto-scoring)**

Each question answered "Yes" that indicates risk adds to the risk score. Sample questions:
1. Does this process large volumes of personal data (>1,000 records)?
2. Does this process special category data (health, biometric, financial, location)?
3. Does data leave India's borders for processing or storage?
4. Does a third party have access to the personal data?
5. Is the data processing automated with potential for significant decisions affecting individuals?
6. Does this involve tracking or monitoring individuals (e.g., CCTV, location, attendance)?
7. Is there a new or untested technology involved?
8. Could a breach of this data cause significant harm to data subjects?
9. Is the personal data of minors (students under 18) involved?
10. Does this involve profiling of individuals?
11. Is there a legitimate legal basis clearly documented for this processing?
12. Can individuals opt out of this processing without impact on core services?
13. Is there a defined retention and deletion schedule for this data?
14. Has a security assessment of the system/vendor been completed?
15. Are data subjects adequately informed about this processing in the privacy notice?
16. Is access to this data restricted by role-based access control?
17. Are processing logs maintained for this activity?
18. Does this processing share data with other systems or databases?
19. Has the vendor's (if any) data processing agreement been reviewed and signed?
20. Could this processing lead to discrimination, exclusion, or adverse treatment of individuals?

Auto-score: Count of risk-positive answers → 0–5 = Low, 6–12 = Medium, 13–20 = High

**Step 4: Mitigation Measures**
- For each risk identified (mapped from questionnaire answers), describe the mitigation:
  - Pre-populated risk items based on Yes answers from Step 3
  - Each risk item: description (read-only) + Mitigation text field (required)
  - Residual Risk after mitigation (dropdown per risk: Accepted / Mitigated / Transferred / Avoided)
- Overall mitigation summary (required, textarea)
- Are all high risks mitigated to acceptable level? (radio: Yes / No)
- If No: explain why residual risk is accepted and who has authorised acceptance

**Step 5: Submit for Review**
- Review summary: PIA name, risk level (auto-scored), data types, scope, mitigation completeness
- Additional notes for reviewer (optional, textarea)
- Declaration: "I confirm that the information in this PIA is accurate and complete to the best of my knowledge." (required checkbox)
- Submit for DPO Review button

On Submit: PIA status → Submitted; DPO notified via in-app notification; email sent to DPO

### 6.2 Drawer: `pia-review` — Review PIA (DPO)
- **Trigger:** Actions → Review (visible to DPO when status = Submitted or Under Review)
- **Width:** 720px
- **All 5 PIA sections displayed read-only for DPO to review:**
  - Each section is expandable/collapsible
  - Full data inventory with display
  - Questionnaire answers shown with scoring breakdown
  - Mitigation measures listed per risk
- **DPO Review section (below PIA content):**
  - Review Comments (required, textarea — DPO must document their assessment)
  - Section-level comments: DPO can add comment to any individual section
  - DPO Assessment (radio: Adequate — approve / Requires Changes — request revision / Inadequate — reject)
  - If High Risk: additional field — IT Director Sign-off Required checkbox (pre-ticked for High Risk; can override)

### 6.3 Modal: Approve PIA
- Confirmation: "You are approving PIA '[Name]'. This approval confirms the processing activity is compliant with DPDP Act 2023 and may proceed. This action is logged against your DPO credentials."
- Buttons: Confirm Approve · Cancel

### 6.4 Modal: Reject PIA
- Required: Rejection Reason (required, dropdown: Insufficient data inventory / Inadequate mitigation for identified risks / Missing legal basis / Data residency non-compliant / Consent mechanism absent / Other)
- Detailed rejection comments (required, textarea — min 100 characters; specific guidance for revision)
- Buttons: Confirm Reject · Cancel

**Audit Trail:** All PIA lifecycle events (creation, submission, DPO review, approval, rejection, IT Director sign-off) are automatically logged to the IT Audit Log with actor, timestamp, and reason.

---

## 7. Charts

No standalone charts. PIA statistics are reflected in KPI cards.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| PIA created (draft) | "PIA '[Name]' saved as draft." | Info | 3s |
| PIA submitted | "PIA '[Name]' submitted for DPO review. Data Privacy Officer has been notified." | Success | 4s |
| PIA approved | "PIA '[Name]' approved. Processing activity may proceed." | Success | 4s |
| PIA rejected | "PIA '[Name]' rejected. Rejection reason documented. Initiator notified." | Warning | 5s |
| High-risk sign-off required | "High-risk PIA '[Name]' approved by DPO. IT Director sign-off required before deployment." | Info | 5s |
| Export triggered | "PIA register export prepared." | Info | 3s |
| PIA submission failed | Error: `Failed to submit PIA. Ensure all required sections are complete.` | Error | 5s |
| PIA approval failed | Error: `Failed to approve PIA. Please try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No PIAs | "No PIAs Recorded" | "No Privacy Impact Assessments have been created. Create a PIA for any new feature or integration that processes personal data." | + Create PIA |
| All approved | "All PIAs Approved" | "All submitted PIAs have been reviewed and approved." | — |
| No filter results | "No Matching PIAs" | "No PIAs match the selected filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 4 KPI shimmer cards + table skeleton (10 rows) |
| Filter / search | Table skeleton shimmer |
| Create PIA wizard — open | Drawer spinner; Step 1 form loads immediately |
| Review PIA drawer | Drawer spinner; each section loads progressively (large drawer) |
| Submit / Approve / Reject | Button spinner |
| Questionnaire auto-score | Inline score updates in real time as answers change (no API call — client-side score calculation) |

---

## 11. Role-Based UI Visibility

| Element | DPO (G1) | IT Admin (G4) | IT Director (G4) | Integration Manager (G4) |
|---|---|---|---|---|
| + Create PIA | Hidden | Visible | Hidden | Visible |
| Edit PIA (Draft/Submitted) | Hidden | Visible | Hidden | Visible |
| Review Action | Visible | Hidden | Hidden | Hidden |
| Approve Action | Visible | Hidden | Hidden | Hidden |
| Reject Action | Visible | Hidden | Hidden | Hidden |
| IT Director sign-off action | Hidden | Hidden | Visible (for High Risk) | Hidden |
| View PIA (all sections) | Visible | Visible | Visible | Visible |
| DPO review comments | Visible + editable | Read-only | Read-only | Read-only |
| Risk score breakdown | Visible | Visible | Visible | Visible |
| Export | Hidden | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/privacy/pia/` | JWT (G1+) | Paginated PIA list |
| POST | `/api/v1/it/privacy/pia/` | JWT (G4 — IT Admin / Integration Manager) | Create PIA (draft) |
| GET | `/api/v1/it/privacy/pia/{id}/` | JWT (G1+) | Full PIA detail |
| PATCH | `/api/v1/it/privacy/pia/{id}/` | JWT (G4) | Update PIA (draft/submitted only) |
| POST | `/api/v1/it/privacy/pia/{id}/submit/` | JWT (G4) | Submit PIA for DPO review |
| POST | `/api/v1/it/privacy/pia/{id}/approve/` | JWT (G1 DPO / G4 IT Director for high-risk) | Approve PIA |
| POST | `/api/v1/it/privacy/pia/{id}/reject/` | JWT (G1 DPO) | Reject PIA with reasons |
| POST | `/api/v1/it/privacy/pia/{id}/director-sign-off/` | JWT (G4 — IT Director) | IT Director sign-off for high-risk PIA |
| GET | `/api/v1/it/privacy/pia/kpis/` | JWT (G1+) | KPI card values |
| GET | `/api/v1/it/privacy/pia/export/` | JWT (G4) | Export PIA register |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/privacy/pia/kpis/` | `#kpi-bar` | `innerHTML` |
| Load PIA table | `load` | GET `/api/v1/it/privacy/pia/` | `#pia-table` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/privacy/pia/?risk=...&status=...` | `#pia-table` | `innerHTML` |
| Search PIAs | `input` (300ms debounce) | GET `/api/v1/it/privacy/pia/?q=...` | `#pia-table` | `innerHTML` |
| Open view / review drawer | `click` on View or Review | GET `/api/v1/it/privacy/pia/{id}/` | `#pia-drawer` | `innerHTML` |
| Wizard step navigation | `click` on Next | PATCH `/api/v1/it/privacy/pia/{id}/` (auto-save) | `#wizard-step-content` | `innerHTML` |
| Submit PIA | `click` on Submit | POST `/api/v1/it/privacy/pia/{id}/submit/` | `#pia-table` | `innerHTML` |
| Confirm approve | `click` on Confirm Approve | POST `/api/v1/it/privacy/pia/{id}/approve/` | `#pia-table` | `innerHTML` |
| Confirm reject | `click` on Confirm Reject | POST `/api/v1/it/privacy/pia/{id}/reject/` | `#pia-table` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/privacy/pia/?page=N` | `#pia-table` | `innerHTML` |
| IT Director sign-off | `click` on Sign Off button | POST `/api/v1/it/privacy/pia/{id}/director-sign-off/` | `#pia-table` | `innerHTML` |
| Export PIA register | `click` on Export | GET `/api/v1/it/privacy/pia/export/` | `#export-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
