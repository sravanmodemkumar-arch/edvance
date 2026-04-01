# Division N — Legal & Compliance: Pages List

> 7 pages · 6 roles (4 original + 2 new: #103, #104)
> Covers: contract lifecycle, DPDP Act 2023 compliance, regulatory filings (TRAI/CERT-In/MeitY), POCSO incident management, policy versioning, and compliance calendar.

---

## Roles

| # | Role | Level | Owns |
|---|---|---|---|
| 75 | Legal Officer | 1 | Institution contracts, ToS, privacy policy updates |
| 76 | Data Privacy Officer (DPO) | 1 | DPDP Act 2023, consent records, 72-hour breach notification |
| 77 | Regulatory Affairs Exec | 1 | TRAI (SMS sender ID EDUFGE), CERT-In, MeitY filings |
| 78 | POCSO Reporting Officer | 1 | Mandatory incident reporting to NCPCR, child welfare coordination |
| 103 | Contract Coordinator | 2 | Contract workflow management, e-signature dispatch, template library, expiry follow-up |
| 104 | Data Compliance Analyst | 1 | DSR triage and intake, data flow documentation, consent coverage reporting, DPDP compliance KPIs |

> **Why #103?** At 2,050 institutions and 6,150+ contract records, a Legal Officer cannot manage the mechanical workflow of sending, following up, and tracking contracts while also handling substantive legal work. The Contract Coordinator owns the operational pipeline; the Legal Officer owns legal judgement.
>
> **Why #104?** The DPO needs analytical bandwidth to respond to DPDP authority enquiries. The Data Compliance Analyst handles DSR intake triage, maintains the data flow register, and produces the weekly compliance data pack — freeing the DPO for decisions requiring legal expertise.

---

## Pages

| Page | Route | Title | Primary Role(s) |
|---|---|---|---|
| N-01 | `GET /legal/` | Legal & Compliance Dashboard | Legal Officer (#75), DPO (#76) |
| N-02 | `GET /legal/contracts/` | Contract Management | Legal Officer (#75), Contract Coordinator (#103) |
| N-03 | `GET /legal/privacy/` | Data Privacy & DPDP Compliance | DPO (#76), Legal Officer (#75) |
| N-04 | `GET /legal/filings/` | Regulatory Filings | Reg. Affairs Exec (#77), Legal Officer (#75) |
| N-05 | `GET /legal/pocso/` | POCSO Incident Registry | POCSO Reporting Officer (#78), Legal Officer (#75) |
| N-06 | `GET /legal/documents/` | Policy & Document Repository | Legal Officer (#75), DPO (#76) |
| N-07 | `GET /legal/calendar/` | Compliance Calendar | All Division N roles (scoped by category) |

---

## Data Model Summary

| Table | Purpose |
|---|---|
| `legal_contract` | Institution contracts lifecycle (MSA/DPA/SLA/ToS/NDA/MoU) |
| `legal_contract_template` | Template library — versioned contract templates |
| `legal_contract_reminder` | Audit log of unsigned-contract reminder emails |
| `legal_policy_document` | Versioned public policies (ToS, Privacy Policy, Cookie Policy) |
| `legal_document_review_log` | Review actions on policy documents |
| `legal_compliance_deadline` | Unified deadline registry — all categories |
| `dpdp_dsr` | Data Subject Requests under DPDP Act §11–14 |
| `dpdp_breach_incident` | Data breach incidents — CERT-In/DPDP notification tracking |
| `dpdp_breach_notification_log` | Audit log of all breach notification submissions |
| `dpdp_consent_record` | Per-institution consent coverage tracking |
| `dpdp_consent_snapshot` | Nightly consent coverage aggregation for trend charts |
| `dpdp_data_flow` | Data flow register (ROPA — Records of Processing Activities) |
| `dpdp_sub_processor` | Sub-processor register per DPDP Act §8(6) |
| `regulatory_filing` | Filing tracker: TRAI, CERT-In, MeitY, State Boards |
| `regulatory_filing_document` | Documents attached to regulatory filings |
| `dpdp_dlt_template` | TRAI DLT SMS template registry (sender ID EDUFGE) |
| `pocso_incident` | POCSO incident records — KMS encrypted |
| `pocso_case_note` | Case notes on POCSO incidents — immutable |
| `pocso_access_log` | Immutable audit log of every POCSO data access |
| `institution_tos_acceptance` | Per-institution ToS acceptance state + re-acceptance flags |
| `legal_contract_reminder` | Audit log of unsigned-contract reminder emails (Task N-2) |
| `legal_document_notification_log` | Audit log of ToS/policy publication notification emails (Task N-8) |
| `pocso_backup_officer` | Designated backup POCSO reporting officer + activation conditions. Fields: id, user_id (FK), designated_by_id (FK Legal Officer), designated_at, deactivated_at (nullable), is_active (bool), notes |
| `pocso_incident_accused` | Multiple accused per POCSO incident. Fields: id, incident_id (FK), accused_type, bgv_id (FK nullable), accused_order, external_name (nullable), external_contact (nullable) |
| `dpdp_dsr_audit_log` | Append-only audit log for all DSR state changes (separate from policy document review log). Fields: id, dsr_id (FK), action_type (CREATED/ASSIGNED/STATUS_CHANGE/NOTE_ADDED/RESOLVED/REJECTED/ESCALATED), actor_id (FK), timestamp, details (JSON) |
| `meity_grievance_officer` | Current and historical MeitY Grievance Officer designations |
| `meity_grievance_complaint` | Complaints received at grievance officer email (IT Rules 2021 §4(1)(c)) |
| `pocso_annual_report` | Generated annual NCPCR compliance reports (linked to N-06 document repository) |
| `dpdp_dsr_supporting_doc` | Supporting documents for NOMINATION/GRIEVANCE DSR types |

---

## Background Tasks

| Task | Schedule | Owned By |
|---|---|---|
| N-1 — Contract Expiry Scanner | Daily 08:00 IST | N-02 |
| N-2 — Unsigned Contract Reminder | Every 3 days | N-02 |
| N-3 — DSR SLA Monitor | Every 4 hours | N-03 |
| N-4 — Consent Coverage Snapshot | Daily 02:00 IST | N-03 |
| N-5 — Breach Deadline Monitor | Every 15 minutes | N-03 |
| N-6 — Filing Deadline Monitor | Daily 07:00 IST | N-04 |
| N-7 — TRAI DLT Status Sync | Weekly Sunday 06:00 IST | N-04 |
| N-8 — ToS Publication Notifier | Triggered on publish | N-06 |
| N-9 — Document Review Reminder | Weekly Monday 09:00 IST | N-06 |
| N-10 — Annual Document Audit | Annually 1 April | N-06 |
| N-11 — Sub-Processor DPA Expiration Monitor | Daily 07:00 IST | N-06 |
| N-5 (Ext.) — POCSO Backup Activation Monitor | Every 30 min (active-deadline window only) | N-05 |

---

## External Integration Webhooks

| Webhook | Endpoint | Source | Description |
|---|---|---|---|
| DigiSign contract signed | `POST /legal/contracts/webhooks/digisign/` | DigiSign e-signature platform | Contract signature completion → auto-activates contract in N-02 |

**DigiSign webhook security:** HMAC-SHA256 signature in `X-DigiSign-Signature` header. Verified against `settings.DIGISIGN_WEBHOOK_SECRET`. Invalid signatures rejected with 403. See N-02 for full webhook payload spec and error handling.

---

## Critical Regulatory Obligations (EduForge context)

| Regulation | Obligation | Deadline | Consequence of failure |
|---|---|---|---|
| CERT-In Directions 2022 | Report cyber incident | 6 hours from discovery | ₹5L penalty + criminal liability for designated officer |
| DPDP Act 2023 | Notify DPDP authority of breach | 72 hours from discovery | Penalty up to ₹250 crore |
| DPDP Act 2023 | Resolve data subject requests | 30 days from receipt | Complaint to Data Protection Board; civil penalty |
| POCSO Act 2012 §19 | Report incident to SJPU/Police | Immediately (in practice: < 24h for NCPCR) | Criminal offence under §21 for Reporting Officer |
| TRAI DLT | Maintain entity registration | Renewal before expiry | SMS/OTP failure for entire platform (7.6M students) |
| IT Rules 2021 (MeitY) | Publish Grievance Officer contact | Continuously maintained | Loss of intermediary liability safe harbour under §79 |
| GST Law | MSA as tax-valid agreement | Before first invoice | Potential dispute on SAC 9993 classification |

---

## Role Cross-Reference with Other Divisions

| Division N Role | Interacts With |
|---|---|
| Legal Officer (#75) | Finance Manager (#69) — contract terms; CEO (#1) — legal escalations; BGV Manager (#39) — POCSO-BGV coordination |
| DPO (#76) | Security Engineer (#16) — breach incidents; Platform Admin (#10) — consent coverage; Analytics Manager (#42) — data minimisation |
| Regulatory Affairs Exec (#77) | DevOps/SRE Engineer (#14) — CERT-In technical details; Notification Manager (#37) — TRAI DLT/WhatsApp compliance |
| POCSO Reporting Officer (#78) | BGV Operations Supervisor (#92) — flagging accused staff; BGV Manager (#39) — BGV policy for flagged cases |
| Contract Coordinator (#103) | Billing Admin (#70) — contract → subscription activation workflow; Onboarding Specialist (#51) — contract required before onboarding |
| Data Compliance Analyst (#104) | Data Analyst (#44) — overlap on data quality; Report Designer (#46) — DPDP compliance report templates |
