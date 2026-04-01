# Group 2 — Division L: Sports & Extra-Curricular — Pages Reference

> **Division:** L — Sports & Extra-Curricular
> **Roles:** 5 roles (see Role Summary)
> **Base URL prefixes:** `/group/sports/` · `/group/cultural/` · `/group/nss/` · `/group/library/`
> **Theme:** Light (`portal_base.html`)
> **Status key:** ✅ Spec done · ⬜ Not started

---

## Scale Context

| Dimension | Value |
|---|---|
| Institution Groups on Platform | 150 |
| Branches per group | 5–50 |
| Students per large group | 20,000–1,00,000 |
| Sports teams per branch | 8–20 (Cricket, Football, Volleyball, Kabaddi, Athletics, Badminton, Chess, Table Tennis, etc.) |
| Cultural events per year | 15–40 group-wide |
| NSS students per large group | 2,000–8,000 |
| NCC cadets per large group | 500–3,000 |
| Library resources (e-library) | 500–10,000 digital items |
| Academic year | April 1 – March 31 |

---

## Division L — Role Summary

| # | Role | Level | Large | Small | Post-Login URL |
|---|---|---|---|---|---|
| 97 | Group Sports Director | G3 | ✅ Dedicated | ✅ Shared | `/group/sports/director/` |
| 98 | Group Sports Coordinator | G3 | ✅ Dedicated | ❌ | `/group/sports/coordinator/` |
| 99 | Group Cultural Activities Head | G3 | ✅ Dedicated | ✅ Shared | `/group/cultural/head/` |
| 100 | Group NSS / NCC Coordinator | G3 | ✅ Dedicated | ✅ Shared | `/group/nss/coordinator/` |
| 101 | Group Library & Learning Resources Head | G2 | ✅ Dedicated | ✅ Shared | `/group/library/head/` |

---

## Section 1 — Role Dashboards

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 01 | Sports Director Dashboard | `/group/sports/director/` | `01-sports-director-dashboard.md` | P0 | ✅ |
| 02 | Sports Coordinator Dashboard | `/group/sports/coordinator/` | `02-sports-coordinator-dashboard.md` | P0 | ✅ |
| 03 | Cultural Activities Head Dashboard | `/group/cultural/head/` | `03-cultural-activities-head-dashboard.md` | P0 | ✅ |
| 04 | NSS / NCC Coordinator Dashboard | `/group/nss/coordinator/` | `04-nss-ncc-coordinator-dashboard.md` | P0 | ✅ |
| 05 | Library & Learning Head Dashboard | `/group/library/head/` | `05-library-head-dashboard.md` | P0 | ✅ |

---

## Section 2 — Sports Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 06 | Sports Event Calendar | `/group/sports/calendar/` | `06-sports-event-calendar.md` | P1 | ✅ |
| 07 | Inter-Branch Tournament Manager | `/group/sports/tournaments/` | `07-inter-branch-tournament-manager.md` | P1 | ✅ |
| 08 | Sports Team Registry | `/group/sports/teams/` | `08-sports-team-registry.md` | P1 | ✅ |
| 09 | Coach & Sports Staff Registry | `/group/sports/coaches/` | `09-coach-staff-registry.md` | P1 | ✅ |
| 10 | Sports Equipment Inventory | `/group/sports/equipment/` | `10-sports-equipment-inventory.md` | P2 | ✅ |

---

## Section 3 — Cultural Activities Management

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 11 | Cultural Events Calendar | `/group/cultural/calendar/` | `11-cultural-events-calendar.md` | P1 | ✅ |
| 12 | Inter-Branch Competition Tracker | `/group/cultural/competitions/` | `12-inter-branch-competition-tracker.md` | P1 | ✅ |
| 13 | Cultural Event Register | `/group/cultural/events/` | `13-cultural-event-register.md` | P1 | ✅ |

---

## Section 4 — NSS / NCC Programs

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 14 | NSS Programme Tracker | `/group/nss/programmes/` | `14-nss-programme-tracker.md` | P1 | ✅ |
| 15 | NCC Camp Register | `/group/nss/ncc-camps/` | `15-ncc-camp-register.md` | P1 | ✅ |
| 16 | Civic Programme Register | `/group/nss/civic/` | `16-civic-programme-register.md` | P2 | ✅ |

---

## Section 5 — Library & Learning Resources

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 17 | E-Library Resource Catalogue | `/group/library/catalogue/` | `17-elibrary-resource-catalogue.md` | P1 | ✅ |
| 18 | Digital Content Distribution | `/group/library/distribution/` | `18-digital-content-distribution.md` | P1 | ✅ |

---

## Section 6 — Achievement & Analytics

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 19 | Student Achievement Register | `/group/sports/achievements/` | `19-student-achievement-register.md` | P1 | ✅ |
| 20 | Extra-Curricular Analytics | `/group/sports/analytics/` | `20-extracurricular-analytics.md` | P2 | ✅ |

---

## Section 7 — Sports Configuration

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 21 | Sport Master Configuration | `/group/sports/master/` | `21-sport-master-configuration.md` | P2 | ✅ |

---

## Section 8 — NSS Certificate & Officers

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 22 | NSS Certificate Management | `/group/nss/certificates/` | `22-nss-certificate-management.md` | P1 | ✅ |

---

## Section 9 — NCC Cadet Registry

| # | Page | URL | File | Priority | Status |
|---|---|---|---|---|---|
| 23 | NCC Cadet Registry | `/group/nss/ncc-cadets/` | `23-ncc-cadet-registry.md` | P1 | ✅ |

---

## Shared Drawers & Overlays (all div-l pages)

| Drawer | Trigger | Width | Tabs | Description |
|---|---|---|---|---|
| `tournament-create` | Tournament Manager → + New | 680px | Details · Teams · Schedule · Venue | Full tournament setup |
| `tournament-detail` | Tournament table → row | 680px | Overview · Teams · Fixtures · Results · Awards | Tournament detail + results |
| `team-create` | Team Registry → + New | 560px | Profile · Members · Coach | Team creation form |
| `team-detail` | Team table → row | 560px | Roster · Performance · History | Team detail view |
| `coach-create` | Coach Registry → + Add | 560px | Profile · Qualifications · Assignment | Coach profile form |
| `coach-detail` | Coach table → row | 560px | Profile · Branches · Achievements | Coach detail |
| `equipment-request` | Equipment → + Request | 480px | Item · Quantity · Branch · Justification | New equipment request |
| `cultural-event-create` | Cultural Events → + New | 680px | Details · Participants · Schedule · Venue | Cultural event setup |
| `cultural-event-detail` | Events table → row | 680px | Overview · Participants · Results · Report | Event full detail |
| `competition-result-entry` | Competition → Enter Results | 560px | Results · Positions · Certificates | Result entry form |
| `nss-activity-log` | NSS Tracker → + Activity | 480px | Activity · Date · Branch · Hours · Students | Activity log entry |
| `ncc-camp-create` | NCC → + Camp | 560px | Camp · Cadets · Dates · Officers | Camp creation |
| `resource-create` | Library → + Resource | 680px | Metadata · File · Classification · Access | Resource upload form |
| `resource-edit` | Catalogue → row | 680px | Metadata · File · Classification · Access | Resource edit form |
| `distribution-assign` | Distribution → Assign | 480px | Resource · Branches · Expiry | Assign resource to branches |
| `achievement-create` | Achievement Register → + Add | 480px | Student · Event · Award · Evidence | Achievement record |
| `sport-create` | Sport Master → + New Sport | 480px | Basic · Rules · Advanced | Sport catalog entry |
| `cadet-create` | NCC Cadet Registry → + Add Cadet | 560px | Profile · NCC Details · Records | Cadet record creation |
| `cadet-detail` | Cadet table → row | 560px | Profile · Certificates · Camp History · Nominations | Individual cadet profile |
| `nomination-create` | NCC Cadets → Nominate for Camp | 480px | Camp · Cadets | RDC/IDC nomination workflow |
| `certificate-generate-bulk` | NSS Certificates → Generate All | 560px | Selection · Preview | Bulk NSS cert generation |
| `nss-officer-edit` | Programme Officer → Edit | 480px | Officer Details | Programme Officer management |

---

## UI Component Standard (applied to every page in div-l)

| Component | Specification |
|---|---|
| **Tables** | Sortable all columns · Checkbox row select + select-all · Responsive (card on mobile < 768px) · Column visibility toggle · Row count badge |
| **Search** | Full-text, 300ms debounce, highlights match |
| **Advanced Filters** | Slide-in filter drawer · Active filters as dismissible chips · "Clear All" · Filter count badge |
| **Pagination** | Server-side · Default 25/page · Selector 10/25/50/All · "Showing X–Y of Z results" · Page jump input |
| **Drawers** | Slide from right · Widths: 400/480/520/560/640/680px · Backdrop click closes (unsaved-changes guard) · ESC closes |
| **Modals** | Centred overlay · Confirm/delete only · Max 480px |
| **Forms** | Inline validation on blur · Required `*` · Character counter on textareas · Disabled submit until valid · Server error summary at top |
| **Toasts** | Bottom-right · Success 4s · Error manual · Warning 6s · Info 4s · Max 3 stacked |
| **Loaders** | Skeleton screens · Spinner on action buttons · Overlay for critical ops |
| **Empty States** | Illustration + heading + description + CTA · Separate "no data" vs "no search results" states |
| **Charts** | Chart.js 4.x · Responsive · Colorblind-safe palette · Legend · Tooltip · PNG export |
| **Role-based UI** | All write controls rendered server-side based on role level · G2 sees content controls only |

---

## Role → Page Access Matrix

| Page | Sports Dir G3 | Sports Coord G3 | Cultural Head G3 | NSS/NCC Coord G3 | Library Head G2 |
|---|---|---|---|---|---|
| 01 Sports Director Dashboard | ✅ Full | — | — | — | — |
| 02 Sports Coordinator Dashboard | — | ✅ Full | — | — | — |
| 03 Cultural Head Dashboard | — | — | ✅ Full | — | — |
| 04 NSS/NCC Dashboard | — | — | — | ✅ Full | — |
| 05 Library Head Dashboard | — | — | — | — | ✅ Full |
| 06 Sports Event Calendar | ✅ Full | ✅ Full | ✅ View | — | — |
| 07 Tournament Manager | ✅ Full | ✅ Coord | — | — | — |
| 08 Sports Team Registry | ✅ Full | ✅ Full | — | — | — |
| 09 Coach Registry | ✅ Full | ✅ Full | — | — | — |
| 10 Equipment Inventory | ✅ View | ✅ Full | — | — | — |
| 11 Cultural Events Calendar | ✅ View | ✅ View | ✅ Full | ✅ View | — |
| 12 Competition Tracker | ✅ View | ✅ View | ✅ Full | — | — |
| 13 Cultural Event Register | ✅ View | ✅ View | ✅ Full | — | — |
| 14 NSS Programme Tracker | — | — | ✅ View | ✅ Full | — |
| 15 NCC Camp Register | — | — | — | ✅ Full | — |
| 16 Civic Programme Register | — | — | ✅ View | ✅ Full | — |
| 17 E-Library Catalogue | — | — | — | — | ✅ Full |
| 18 Content Distribution | — | — | — | — | ✅ Full |
| 19 Student Achievement Register | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ View |
| 20 Extra-Curricular Analytics | ✅ Full | ✅ View | ✅ Full | ✅ Full | ✅ View |
| 21 Sport Master Configuration | ✅ Full | ✅ View | — | — | — |
| 22 NSS Certificate Management | — | — | ✅ View | ✅ Full | — |
| 23 NCC Cadet Registry | — | — | — | ✅ Full | — |

---

## Functional Coverage Audit — Zero Gaps

| # | Job to Be Done | Role | Page |
|---|---|---|---|
| 1 | View all branches' sports program status at a glance | Sports Director | 01, 06 |
| 2 | Create and manage inter-branch tournaments | Sports Director | 07 |
| 3 | Nominate students for state/national sports teams | Sports Director | 01, 19 |
| 4 | Set and publish group-wide sports policy | Sports Director | 01 |
| 5 | Manage coach assignments across branches | Sports Coordinator | 02, 09 |
| 6 | Track equipment requests and inventory levels | Sports Coordinator | 10 |
| 7 | Maintain sports calendar with events and fixtures | Sports Coordinator | 06 |
| 8 | Manage team rosters per sport per branch | Sports Coordinator | 08 |
| 9 | Plan and manage annual day and cultural events | Cultural Head | 03, 13 |
| 10 | Track inter-branch competition registrations and results | Cultural Head | 12 |
| 11 | Manage group-wide cultural calendar | Cultural Head | 11 |
| 12 | Register students for external competitions (NTSE quiz, debate) | Cultural Head | 12 |
| 13 | Track NSS enrolments and 240-hour activity targets | NSS/NCC Coord | 04, 14 |
| 14 | Register and manage NCC camp attendance and certificates | NSS/NCC Coord | 15 |
| 15 | Log civic programme activities and community service | NSS/NCC Coord | 16 |
| 16 | Manage central e-library resource catalogue | Library Head | 05, 17 |
| 17 | Distribute digital resources to specific branches | Library Head | 18 |
| 18 | Track resource usage and access per branch | Library Head | 18, 20 |
| 19 | Record all co-curricular student achievements (sports + cultural + NSS) | All | 19 |
| 20 | Analyse cross-division extra-curricular participation trends | All | 20 |
| 21 | Award and certificate management for competitions | Cultural Head / Sports Director | 12, 07 |
| 22 | Manage NCC officer appointments per branch | NSS/NCC Coord | 04, 15 |
| 23 | Monitor branches with no sports program active | Sports Director | 01 |
| 24 | Track student participation count per sport per branch | Sports Coordinator | 08 |
| 25 | Monitor branches without cultural activity this term | Cultural Head | 03 |
| 26 | Configure and maintain group sport catalog (names, min players, rules) | Sports Director | 21 |
| 27 | Generate and distribute NSS certificates to 240h achievers | NSS/NCC Coord | 22 |
| 28 | Manage NSS Programme Officer roster across all branches | NSS/NCC Coord | 22 |
| 29 | Export volunteer completion list in state NSS Directorate format | NSS/NCC Coord | 22 |
| 30 | Maintain individual NCC cadet records for camp nominations | NSS/NCC Coord | 23 |
| 31 | Nominate top cadets for RDC / IDC / TSC / VSC national camps | NSS/NCC Coord | 23 |
| 32 | Track NCC certificate level (A/B/C) progression per cadet | NSS/NCC Coord | 23 |
| 33 | Auto-create achievement records when tournament awards are published | Sports Director | 07→19 |
| 34 | Auto-create achievement records when competition results are published | Cultural Head | 12→19 |
| 35 | Track medical fitness certificates for state/national sports nominations | Sports Director | 19 |
| 36 | Flag high-achieving students for Group Marketing brand ambassador use | Sports Dir / Cultural Head | 07, 12, 19 |
| 37 | View Division L analytics — cross-division intelligence (Division M consumers) | Analytics Director / MIS Officer | 20 |

---

## Implementation Priority

```
P0 — Before division portal goes live
  01–05   All 5 role dashboards

P1 — Sprint 2
  06, 07, 08, 09, 11, 12, 13, 14, 15, 17, 18, 19, 22, 23

P2 — Sprint 3
  10, 16, 20, 21
```

---

## Division Count Summary

| Division | Total | Large Uses | Small Uses |
|---|---|---|---|
| L — Sports & Extra-Curricular | 23 | 23 | 6–8 |

---

*Last updated: 2026-03-21 · Total pages: 23 · Roles: 5 · Audit pass: 2 — zero gaps · Deep audit: 15-pass*
