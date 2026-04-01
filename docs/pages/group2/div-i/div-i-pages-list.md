# Division I — Transport Management: Page List

> **Division:** I — Transport Management
> **Total Pages:** 33
> **Roles covered:** 6 (Roles 79–84)
> **Spec version:** 1.0 · Last updated: 2026-03-21

---

## Role Coverage

| # | Role | Level | Large Group | Small Group | Dashboard |
|---|---|---|---|---|---|
| 79 | Group Transport Director | G3 | ✅ Dedicated | ✅ 1 person | Page 01 |
| 80 | Group Fleet Manager | G3 | ✅ Dedicated | ❌ | Page 02 |
| 81 | Group Route Planning Manager | G3 | ✅ Dedicated | ❌ | Page 03 |
| 82 | Group Transport Fee Manager | G3 | ✅ Dedicated | ✅ Shared | Page 04 |
| 83 | Group Driver/Conductor HR | G0 | ✅ Dedicated | ❌ | Page 05 (boundary) |
| 84 | Group Transport Safety Officer | G3 | ✅ Dedicated | ✅ Shared | Page 06 |

---

## Page Map

### Role Dashboards (P0)

| # | File | Title | Role | Priority |
|---|---|---|---|---|
| 01 | `01-transport-director-dashboard.md` | Transport Director Dashboard | Role 79 G3 | P0 |
| 02 | `02-fleet-manager-dashboard.md` | Fleet Manager Dashboard | Role 80 G3 | P0 |
| 03 | `03-route-planning-manager-dashboard.md` | Route Planning Manager Dashboard | Role 81 G3 | P0 |
| 04 | `04-transport-fee-manager-dashboard.md` | Transport Fee Manager Dashboard | Role 82 G3 | P0 |
| 05 | `05-driver-hr-dashboard.md` | Driver/Conductor HR Boundary Page | Role 83 G0 | P1 |
| 06 | `06-transport-safety-officer-dashboard.md` | Transport Safety Officer Dashboard | Role 84 G3 | P0 |

### Fleet Management

| # | File | Title | Primary Role | Priority |
|---|---|---|---|---|
| 07 | `07-vehicle-register.md` | Vehicle Register | Fleet Manager | P0 |
| 08 | `08-vehicle-maintenance-tracker.md` | Vehicle Maintenance Tracker | Fleet Manager | P0 |
| 09 | `09-fitness-permit-insurance-manager.md` | Fitness / Permit / Insurance Manager | Fleet Manager | P0 |
| 10 | `10-vehicle-assignment-manager.md` | Vehicle Assignment Manager | Fleet Manager | P1 |

### Route Management

| # | File | Title | Primary Role | Priority |
|---|---|---|---|---|
| 11 | `11-route-manager.md` | Route Manager | Route Planning Mgr | P0 |
| 12 | `12-pickup-drop-point-manager.md` | Pickup / Drop Point Manager | Route Planning Mgr | P1 |
| 13 | `13-route-optimization-tool.md` | Route Optimization Tool | Route Planning Mgr | P2 |
| 14 | `14-student-transport-allocation.md` | Student Transport Allocation | Route Planning Mgr | P0 |

### Driver & Conductor Management

| # | File | Title | Primary Role | Priority |
|---|---|---|---|---|
| 15 | `15-driver-conductor-registry.md` | Driver & Conductor Registry | Fleet Manager | P0 |
| 16 | `16-driver-license-tracker.md` | Driver Licence Tracker | Fleet Manager | P0 |
| 17 | `17-driver-bgv-training-records.md` | Driver BGV & Training Records | Fleet Manager | P1 |

### GPS Tracking

| # | File | Title | Primary Role | Priority |
|---|---|---|---|---|
| 18 | `18-gps-live-tracking.md` | GPS Live Tracking | Safety Officer | P0 |
| 19 | `19-gps-device-manager.md` | GPS Device Manager | Fleet Manager | P1 |

### Transport Fee Management

| # | File | Title | Primary Role | Priority |
|---|---|---|---|---|
| 20 | `20-transport-fee-structure.md` | Transport Fee Structure | Fee Manager | P0 |
| 21 | `21-transport-fee-collection.md` | Transport Fee Collection | Fee Manager | P0 |
| 22 | `22-transport-fee-defaulters.md` | Transport Fee Defaulters | Fee Manager | P0 |

### Safety & Incident Management

| # | File | Title | Primary Role | Priority |
|---|---|---|---|---|
| 23 | `23-accident-incident-register.md` | Accident & Incident Register | Safety Officer | P0 |
| 24 | `24-safety-inspection-tracker.md` | Safety Inspection Tracker | Safety Officer | P1 |
| 25 | `25-emergency-protocol-manager.md` | Emergency Protocol Manager | Safety Officer | P1 |
| 26 | `26-student-safety-alerts.md` | Student Safety Alerts | Safety Officer | P0 |

### Operations

| # | File | Title | Primary Role | Priority |
|---|---|---|---|---|
| 27 | `27-fuel-expense-tracker.md` | Fuel & Expense Tracker | Fleet Manager | P1 |
| 28 | `28-bus-pass-manager.md` | Bus Pass Manager | Fee Manager | P1 |

### Analytics, Reports & Compliance

| # | File | Title | Primary Role | Priority |
|---|---|---|---|---|
| 29 | `29-transport-analytics-dashboard.md` | Transport Analytics Dashboard | Transport Director | P1 |
| 30 | `30-transport-mis-report.md` | Transport MIS Report | Transport Director | P1 |
| 31 | `31-transport-compliance-dashboard.md` | Transport Compliance Dashboard | Transport Director | P0 |
| 32 | `32-transport-policy-manager.md` | Transport Policy Manager | Transport Director | P2 |
| 33 | `33-transport-audit-log.md` | Transport Audit Log | Transport Director | P1 |

---

## Functional Coverage Matrix

| Function | Pages |
|---|---|
| Fleet inventory | 07, 10 |
| Vehicle compliance (fitness/permit/insurance) | 09, 31 |
| Vehicle maintenance | 08 |
| Route management + approval | 11, 03 |
| Pickup/drop points | 12 |
| Route optimization | 13 |
| Student transport allocation | 14 |
| Driver/conductor registry | 15 |
| Driver licence compliance | 16 |
| Driver BGV + training | 17 |
| GPS live tracking | 18 |
| GPS device management | 19 |
| Transport fee structure | 20 |
| Transport fee collection | 21 |
| Fee defaulters + bus pass suspension | 22 |
| Bus pass issuance/renewal | 28 |
| Accident/incident management | 23 |
| Safety inspections | 24 |
| Emergency protocols | 25 |
| Student safety alerts | 26 |
| Fuel & expense tracking | 27 |
| Analytics | 29 |
| Monthly MIS report | 30 |
| Compliance dashboard | 31 |
| Policy management | 32 |
| Audit trail | 33 |
| Driver HR boundary (G0) | 05 |

---

## URL Structure

All Division I pages live under `/group/transport/`:

```
/group/transport/director/                    01
/group/transport/fleet/                       02
/group/transport/routes/                      03
/group/transport/fees/                        04
/group/transport/driver-hr/                   05
/group/transport/safety/                      06
/group/transport/vehicles/                    07
/group/transport/vehicles/maintenance/        08
/group/transport/compliance/documents/        09
/group/transport/vehicles/assignments/        10
/group/transport/routes/list/                 11
/group/transport/routes/stops/                12
/group/transport/routes/optimize/             13
/group/transport/students/                    14
/group/transport/staff/                       15
/group/transport/staff/licences/              16
/group/transport/staff/bgv-training/          17
/group/transport/gps/live/                    18
/group/transport/gps/devices/                 19
/group/transport/fees/structure/              20
/group/transport/fees/collection/             21
/group/transport/fees/defaulters/             22
/group/transport/safety/incidents/            23
/group/transport/safety/inspections/          24
/group/transport/safety/emergency-protocols/  25
/group/transport/safety/alerts/               26
/group/transport/operations/fuel/             27
/group/transport/fees/bus-passes/             28
/group/transport/analytics/                   29
/group/transport/reports/mis/                 30
/group/transport/compliance/                  31
/group/transport/policies/                    32
/group/transport/audit/                       33
```

---

## Cross-Division Links

| This page | Links to | Division |
|---|---|---|
| Page 05 (Driver HR) | Integration Registry | Div F Page 24 |
| Page 06, 23 (Safety) | Escalate to COO | Div G |
| Page 17 (BGV) | Group BGV Manager | Div E Page 08 |
| Page 30 (MIS) | Distribution to Chairman | Div A |
| Page 31 (Compliance) | Insurance cost view | Div D CFO |
| All pages | Transport Audit Log | Page 33 |

---

*Division I spec version: 1.0 · Total pages: 33 · Last updated: 2026-03-21*
