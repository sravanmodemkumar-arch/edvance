# G-07 — Fire Safety & Building Compliance

> **URL:** `/college/compliance/fire-safety/`
> **File:** `g-07-fire-safety.md`
> **Priority:** P2
> **Roles:** Compliance Officer (S4) · Estate Manager (S3) · Principal/Director (S6)

---

## 1. Fire Safety Compliance

```
FIRE SAFETY — GCEH
(Telangana Fire Services Act + NBC 2016 + AICTE Building Norms)

FIRE NOC STATUS:
  Authority: Telangana State Disaster Response & Fire Services Department
  Current NOC: ✅ Valid (issued 15 March 2026; validity 1 year)
  Renewal due: 14 March 2027 ← In process (application submitted Feb 2027)
  Covering: Main academic block (G+4), Hostel Block A (G+3), Block B (G+2),
            Block C Girls (G+2), Administrative block, Library block

FIRE SAFETY EQUIPMENT INVENTORY:
  Equipment              | Required (NBC) | Installed | Last Check | Status
  ───────────────────────────────────────────────────────────────────────────
  Fire extinguishers     | 40             | 48        | 15 Mar 2027| ✅ (ABC type)
  Smoke detectors        | 80 (all rooms) | 112       | Jan 2027   | ✅ (ionisation)
  Sprinklers             | Required (G+4) | 36 heads  | Jan 2027   | ✅ (overhead)
  Fire hydrants          | 4 (area basis) | 6         | Mar 2027   | ✅ (mains connected)
  Fire alarm panel       | 1 per block    | 6         | Feb 2027   | ✅ (addressable)
  Emergency lighting     | All stairways  | ✅         | Mar 2027   | ✅ (LED, battery bkp)
  Fire exits (signage)   | All floors     | ✅         | Mar 2027   | ✅ (illuminated)
  Hose reel cabinets     | Every 30m      | 12        | Mar 2027   | ✅
  Terrace water tank     | Min 10,000L    | 2×10,000L | —          | ✅

FIRE EXIT COMPLIANCE:
  All fire exits: Clear (no obstruction check — monthly)
  Emergency exit doors: Open outward (NBC 2016 — inward-opening exits prohibited)
  Corridor width: Min 1.8m (NBC) — all corridors ≥2.1m ✅
  Staircase lighting: Emergency battery backup ✅
  Evacuation plan: Displayed on each floor, hostel corridors ✅
```

---

## 2. Evacuation Drills

```
EVACUATION DRILL RECORD

DRILL HISTORY:
  Date              | Block            | Time to evacuate | Issues noted
  ──────────────────────────────────────────────────────────────────────────
  15 October 2026   | Hostel (all)     | 4 min 20 sec     | 2 students slow (instructed)
  20 October 2026   | Academic Block   | 3 min 45 sec     | None ✅
  22 October 2026   | Library + Admin  | 2 min 10 sec     | None ✅
  Next drill due:   | All blocks       | Sep 2027 (start of next academic year)

NBC 2016 REQUIREMENT: Minimum 1 drill per year (GCEH exceeds: 2 drills)
AICTE / NAAC: Evidence of evacuation drills required for Criterion 4

DRILL PROCEDURE:
  Alarm activated (fire panel simulation)
  All occupants: Evacuate to designated muster points (4 points on campus map)
  Roll call at muster points (faculty/warden responsible for headcount)
  "All clear" declared after headcount complete
  Time recorded from alarm to all-clear
  Post-drill debrief: Issues discussed; corrective actions documented

IMPROVEMENTS FROM OCTOBER DRILL:
  Lab 3 (CAD lab): Students were slow to stop saving files and evacuate
    Action: Lab rules updated — "EVACUATE IMMEDIATELY, no saving"
  Block A hostel: Students in deep-sleep during morning drill hesitant
    Action: Drill announced 24 hours in advance (practical consideration);
            UNannounced drill for hostels will be separate

FIRE SAFETY TRAINING:
  All faculty: 1-hour fire safety induction (annually — at year start)
  Security staff: 2-hour drill (extinguisher operation; when to fight vs evacuate)
  New students: Evacuation map orientation in induction week
```

---

## 3. Building Compliance

```
BUILDING COMPLIANCE — NBC 2016 / Local Regulations

BUILDING COMPLETION CERTIFICATES:
  Main block (G+4): BCC issued 2014 ✅ (HMDA)
  Hostel Blocks A, B, C: BCC issued 2010, 2018, 2022 ✅
  Library block: BCC issued 2020 ✅
  Admin block: BCC issued 2015 ✅
  Under construction (Block D Girls hostel): BCC pending (Phase 1 structure complete)

STRUCTURAL SAFETY:
  Last structural audit: March 2025 (by empanelled structural engineer)
  Finding: "All load-bearing structures in good condition"
  Recommended: Minor cracks in Block A (2010 construction) → repair done ✅
  Next audit due: March 2027 (scheduled)

ELECTRICAL SAFETY:
  Last electrical audit: January 2027
  Finding: 2 panels in Mech lab outdated (pre-2005 components) → replacement ordered
  LT panel certification: ✅ All panels (except 2 Mech lab — replacement in progress)
  Earthing: ✅ All buildings tested (annual requirement — IS 3043)
  Emergency power: DG set (125 kVA) — covers critical loads (servers, lights, security)

LIFT SAFETY:
  Lifts installed: 2 (Main block — faculty/differently-abled; Admin block)
  Lift inspection: Annual (Telangana Lift Inspector)
  Last inspection: December 2026 ✅
  Licence: ✅ Valid until December 2027

ACCESSIBILITY (RPwD Act 2016 / NBC 2016):
  Ramps: ✅ All buildings have accessible ramps (1:12 gradient)
  Toilets (accessible): ✅ 2 per building (ground floor)
  Signage (Braille): ✅ Lift buttons, key locations
  Tactile paths: ⬜ Campus-wide tactile flooring for visually impaired — Phase 2 (2027)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/college/{id}/compliance/fire/status/` | Fire safety compliance status |
| 2 | `GET` | `/api/v1/college/{id}/compliance/fire/equipment/` | Equipment inventory |
| 3 | `POST` | `/api/v1/college/{id}/compliance/fire/drill/` | Record evacuation drill |
| 4 | `GET` | `/api/v1/college/{id}/compliance/building/certificates/` | Building compliance docs |

---

## 5. Business Rules

- Fire NOC renewal must be applied at least 30 days before expiry; an expired Fire NOC means the college is operating without a mandatory safety certification; if a fire incident occurs with an expired NOC, the institution and its management face criminal negligence charges; AICTE also checks Fire NOC during inspection and can impose a condition or defer EoA if NOC is expired; EduForge sets reminders at 60 and 30 days before expiry
- Fire extinguisher monthly checks are not optional; they must be physically checked (pressure indicator in green zone) and the check recorded; an extinguisher that has leaked pressure, has a missing pin, or is obstructed is a compliance failure; NAAC Criterion 4 and insurance audits both examine extinguisher maintenance records; the monthly check log (with checker's signature) is sufficient evidence
- Evacuation drill records must include time-to-evacuate; a drill with no time measurement is incomplete; NAAC peer teams ask "how long does it take to evacuate your building?" and expect a data-driven answer; the NBC 2016 guidance (for educational buildings) is that full evacuation should be achievable within 5 minutes
- Accessibility compliance under RPwD Act 2016 is not merely about physical ramps; it includes sensory accessibility (Braille signage, visual alarms for hearing-impaired), cognitive accessibility (clear simple signage), and digital accessibility (accessible website, accessible EduForge app); institutions that focus only on ramps miss the broader requirements; NAAC Criterion 7 (Institutional Values) specifically assesses differently-abled accessibility
- The building completion certificate (BCC) and the occupancy certificate must match the actual usage; a building constructed with residential BCC but used for academic purposes (or vice versa) is technically illegal and voids both the fire NOC and the insurance; this situation arises when colleges rapidly expand without obtaining fresh BCCs for new constructions

---

*Last updated: 2026-03-27 · Group 4 — College Portal · Division G*
