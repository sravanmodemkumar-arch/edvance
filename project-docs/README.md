# Project Docs

Non-spec, non-code project documents. Living records of decisions, meetings, sprints, and diagrams.

## Structure

| Folder | Contents |
|---|---|
| [decisions/](decisions/) | Architecture Decision Records (ADRs) — why we made key choices |
| [sprints/](sprints/) | Sprint plans, task tracking, week-by-week progress |
| [meetings/](meetings/) | Meeting notes, standup summaries |
| [diagrams/](diagrams/) | System diagrams, flow charts, ERDs |

## ADRs

| ADR | Decision |
|---|---|
| [ADR-001](decisions/ADR-001-framework-split.md) | Django + FastAPI split architecture |
| [ADR-002](decisions/ADR-002-no-redis.md) | No Redis — PostgreSQL + Cloudflare instead |

## Sprint Plans

| Sprint | Weeks | Goal |
|---|---|---|
| [Sprint 01](sprints/sprint-01-foundation.md) | 1–2 | Foundation — Auth, Docker, DB schemas |

> For feature specs, see [docs/modules/](../docs/modules/) and [docs/pages/](../docs/pages/).
