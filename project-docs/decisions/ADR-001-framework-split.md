# ADR-001 — Framework Split: Django + FastAPI

**Date:** 2026-04-01  
**Status:** Accepted

## Decision

Use **Django + HTMX** for the portal service and **FastAPI** for all 6 API services.

## Context

Edvance has two fundamentally different workloads:
1. **Portal UI** — 1,519 pages, complex forms, attendance sheets, fee tables, timetables, CBVs
2. **API services** — stateless, Lambda, high throughput, auto-docs required

## Options Considered

| Option | Portal | APIs | Verdict |
|---|---|---|---|
| Django everywhere | ✅ Natural fit | ⚠️ DRF is heavier, slow Lambda cold starts | Rejected |
| FastAPI everywhere | ⚠️ Manual forms, no admin | ✅ Perfect | Rejected |
| **Django + FastAPI split** | ✅ CBV + HTMX | ✅ Lambda + Pydantic | **Accepted** |

## Consequences

- One team must know both Django and FastAPI
- Shared JWT validation across all services via `JWT_SECRET_KEY`
- Portal runs on ECS Fargate (always-on); APIs run on Lambda (pay-per-call)
- Django admin provides free CRUD for internal tools
