# H-10 — Discipline & Conduct Register

> **URL:** `/school/hostel/conduct/`
> **File:** `h-10-discipline-conduct.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Warden (S3) — log incidents · Chief Warden (S4) — review and impose penalties · Principal (S6) — serious offences; removal from hostel

---

## 1. Purpose

Records conduct violations in the hostel and tracks disciplinary actions. Different from school disciplinary records (J-04) — hostel conduct is specific to residential life (after school hours behaviour).

---

## 2. Page Layout

### 2.1 Register
```
Conduct Register — 2026–27                           [Log Incident]

# | Student     | Class | Date       | Offence               | Action Taken        | Status
1 | Vijay S.    | X-B   | 20 Feb 26  | Lights out violation  | Verbal warning      | ✅ Closed
2 | Ravi K.     | IX-A  | 15 Mar 26  | Mobile phone found    | Phone confiscated   | ✅ Closed
3 | Arjun S.    | XI-A  | 10 Mar 26  | Ragging (minor teasing)| Counsellor referral | 🟡 Under review
```

---

## 3. Log Incident

```
[Log Incident]

Student: [Arjun Sharma — XI-A]
Date: 10 March 2026  ·  Time: 8:30 PM
Location: Common room
Warden reporting: Mr. Suresh Kumar

Offence category:
  ○ Lights out violation  ○ Noise after lights out
  ● Ragging (teasing, bullying)  ○ Contraband (phone, tobacco, etc.)
  ○ Unauthorised absence from hostel  ○ Damage to property
  ○ Fighting  ○ Theft  ○ Other

Description:
  "Arjun Sharma was observed pulling the chair from under a Class VI student
   (Rohit M.) in the common room, causing the student to fall. Rohit sustained
   no injury but was distressed. When confronted, Arjun said it was 'just a joke.'"

Anti-ragging compliance (if ragging/bullying):
  Per UGC Anti-Ragging Guidelines (applicable to school residential settings per MHW advisory):
  → Mandatory counsellor referral  ✅
  → Parent notification  ✅
  → Recorded in anti-ragging register (separate from conduct register)

Witnesses: [Rohit M. (VI-A), Dinesh P. (XI-B)]

Proposed action:
  ☑ Verbal warning  ☑ Parent notification  ☑ Counsellor referral
  ○ Written warning  ○ Hostel privileges suspended  ○ Removal from hostel

[Submit Incident Report]
```

---

## 4. Anti-Ragging Register

```
Anti-Ragging Register — Hostel — 2026–27

Per MHW/NCPCR guidelines, all bullying/ragging incidents must be separately registered.

# | Aggressor   | Victim      | Date       | Nature        | Action          | Resolved
1 | Arjun S.    | Rohit M.    | 10 Mar 26  | Minor teasing | Counsellor ref. | 🟡 Open
2 | Vijay group | New student | 5 Oct 2025 | Nickname mock | Written warning | ✅ Closed

All ragging incidents → school counsellor (J-05) within 24 hours.
Serious ragging → Principal + Parent + Police (if warranted by severity)

[Generate Anti-Ragging Report for CBSE]
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/hostel/conduct/?year={y}` | Conduct register |
| 2 | `POST` | `/api/v1/school/{id}/hostel/conduct/` | Log incident |
| 3 | `PATCH` | `/api/v1/school/{id}/hostel/conduct/{incident_id}/action/` | Update action taken |
| 4 | `GET` | `/api/v1/school/{id}/hostel/conduct/anti-ragging/?year={y}` | Anti-ragging register |

---

## 6. Business Rules

- Any ragging/bullying incident must be routed to the school counsellor (J-01) within 24 hours; NCPCR guidelines treat ragging as a serious welfare concern
- Removal from hostel (the most severe punishment) requires Principal approval and parent written consent; the student's school enrollment is not automatically affected by hostel removal
- Three written warnings in one term result in an automatic escalation to Chief Warden for possible suspension of hostel privileges
- Mobile phones: Many boarding schools prohibit or restrict mobile phones; found contraband is confiscated and returned only to parents on the next visiting day; this policy varies by school and is configurable
- Conduct records are visible to the school counsellor (J-01) and Principal; not visible to parents directly, but parents are notified of specific incidents per the action taken

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division H*
