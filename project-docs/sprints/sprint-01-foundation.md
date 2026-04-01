# Sprint 01 — Foundation (Weeks 1–2)

**Goal:** OTP login → JWT → role detection → correct home page.

## Week 1 Tasks

| # | Task | Branch | Status |
|---|---|---|---|
| 1 | PostgreSQL 16 — create 7 schemas | `feature/layer-0-db-schemas` | pending |
| 2 | Docker Compose (PG + Django + FastAPI + pgAdmin) | `feature/layer-0-docker` | pending |
| 3 | Django project scaffold (core, auth apps) | `feature/layer-0-django-scaffold` | pending |
| 4 | FastAPI identity service scaffold | `feature/module-01-auth` | pending |
| 5 | Environment config (.env per environment) | `feature/layer-0-env-config` | pending |
| 6 | CI/CD pipeline (GitHub Actions) | done ✅ | completed |

## Week 2 Tasks

| # | Task | Branch | Status |
|---|---|---|---|
| 7 | Password login + JWT create/verify/refresh | `feature/module-01-auth` | pending |
| 8 | OTP send/verify (high-risk ops only) | `feature/module-01-auth` | pending |
| 9 | Multi-tenant middleware (domain → tenant_id) | `feature/module-02-multi-tenancy` | pending |
| 10 | Institution model + RBAC | `feature/module-03-roles-permissions` | pending |
| 11 | User-institution-role linking (N:N:N) | `feature/module-03-roles-permissions` | pending |
| 12 | Role-based home routing | `feature/layer-0-home-routing` | pending |

## Branch Flow

```
feature/* → develop → qa → staging → main
```

## Deliverable

`POST /auth/token` → JWT → role → correct portal home page.
