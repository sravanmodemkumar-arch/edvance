# A-24 — Policy Repository

> **URL:** `/school/admin/policies/`
> **File:** `a-24-policy-repository.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Principal (S6) — full · Promoter (S7) — approve · All staff (S3+) — view own applicable policies

---

## 1. Purpose

Versioned repository of all institutional policies — fee policy, leave policy, disciplinary policy, examination policy, POCSO policy (mandatory), academic integrity policy, transport safety policy, etc. Staff must acknowledge reading key policies. Regulators (CBSE, state board) expect schools to have documented policies during inspection visits.

---

## 2. Policy Table

| Policy | Version | Effective From | Last Updated | Acknowledgement | Staff Acknowledged |
|---|---|---|---|---|---|
| Fee Refund & Waiver Policy | v2.1 | 1 Apr 2025 | 20 Mar 2025 | Required | 98/110 (89.1%) |
| POCSO Policy & ICC Charter | v1.3 | 1 Aug 2024 | 28 Jul 2024 | Required (mandatory) | 110/110 (100%) |
| Leave Policy | v3.0 | 1 Apr 2025 | 15 Mar 2025 | Optional | — |
| Examination Integrity Policy | v1.2 | 1 Jun 2024 | 28 May 2024 | Required | 92/110 (83.6%) |
| Transport Safety Policy | v1.0 | 1 Aug 2023 | 1 Aug 2023 | Required (bus staff only) | 12/12 (100%) |
| Academic Integrity Policy | v1.1 | 1 Jun 2023 | 28 May 2023 | Optional | — |
| Data Privacy Policy (DPDPA) | v1.0 | 15 Aug 2023 | 10 Aug 2023 | Required | 107/110 (97.3%) |

---

## 3. Policy Detail / Edit

**680px drawer, tabs: Content · Scope · Acknowledgement · Versions**

- Content: Rich text editor (Principal/Promoter only can edit)
- Scope: Apply to all staff / specific department / specific role / students + parents (some policies shared with parents)
- Acknowledgement: Required / Optional · Deadline to acknowledge
- Versions: Full version history with diff between versions

**[Publish New Version]** → notifies all applicable staff with in-app notification + WhatsApp. Acknowledgement resets to 0.

---

## 4. Pending Acknowledgements

Staff who haven't acknowledged a required policy:
- Name · Role · Policy · Deadline · Days remaining
- [Send Reminder] per row · [Bulk Remind] button

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/policies/` | Policy list |
| 2 | `POST` | `/api/v1/school/{id}/policies/` | Create new policy |
| 3 | `PATCH` | `/api/v1/school/{id}/policies/{id}/publish/` | Publish new version |
| 4 | `POST` | `/api/v1/school/{id}/policies/{id}/acknowledge/` | Staff acknowledges policy |
| 5 | `GET` | `/api/v1/school/{id}/policies/{id}/acknowledgements/` | Acknowledgement status |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
