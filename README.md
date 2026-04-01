# Edvance

> All-in-one Education Platform — Schools · Colleges · Coaching · Competitive Exams · AI Learning
> Scale: 5 crore students · Cost: ₹0.60/student/year

---

## Services

| Service | Port | Runtime | Responsibility |
|---|---|---|---|
| identity | 8001 | AWS Lambda / FastAPI | Auth, JWT, OTP, Users, Institutions |
| portal | 8002 | ECS Fargate / Django | School, College, Coaching portals |
| exam | 8003 | AWS Lambda / FastAPI | Mock tests, MCQ engine, submissions, ranks |
| notification | 8004 | AWS Lambda / FastAPI | WhatsApp, SMS, Email, Push |
| billing | 8005 | AWS Lambda / FastAPI | Subscriptions, Razorpay, GST |
| ai | 8006 | AWS Lambda / FastAPI | MCQ generation, doubt solving, study plans |
| analytics | 8007 | AWS Lambda / FastAPI | Reports, MIS, dashboards |

## Quick Start

```bash
# Clone
git clone https://github.com/sravanmodemkumar-arch/edvance.git
cd edvance

# Setup environment
cp .env.example .env

# Start all services
docker-compose up --build
```

| Service | URL |
|---|---|
| Identity API | http://localhost:8001/docs |
| Portal | http://localhost:8002 |
| Exam API | http://localhost:8003/docs |
| Notification API | http://localhost:8004/docs |
| Billing API | http://localhost:8005/docs |
| AI API | http://localhost:8006/docs |
| Analytics API | http://localhost:8007/docs |
| pgAdmin | http://localhost:5050 |

## Architecture

```
Cloudflare Edge (CDN + R2 + WAF)   ← serves 99% of reads at ₹0
        ↓ cache miss only
AWS API Gateway
        ↓
identity  portal  exam  notification  billing  ai  analytics
Lambda    Fargate  Lambda  Lambda     Lambda  Lambda  Lambda
        ↓
PostgreSQL 16 RDS (1 cluster, 7 schemas)
        ↓
AWS SQS (async scoring, notifications, ranks)
```

## Documentation

| Doc | Description |
|---|---|
| [DEVELOPMENT-PLAN.md](docs/DEVELOPMENT-PLAN.md) | 38-week plan, all 58 modules, 10 portal groups |
| [architecture.md](docs/architecture.md) | System architecture |
| [database.md](docs/database.md) | PostgreSQL schema design |
| [deployment.md](docs/deployment.md) | CI/CD, infrastructure, env vars |
| [api.md](docs/api.md) | API conventions |
| [modules/](docs/modules/) | 58 backend module specs |
| [pages/](docs/pages/) | Portal page specs (1,519 pages) |
| [roles/](docs/roles/) | RBAC role definitions |

## Branch Strategy

```
main        ← production (always deployable, protected)
develop     ← integration branch
feature/*   ← feature/module-01-auth, feature/group-3-school
hotfix/*    ← emergency production fixes
```

## Cost at Scale

| Phase | Students | Monthly Cost |
|---|---|---|
| Dev | 0–1K | ₹8,000 |
| Beta | 1K–50K | ₹25,000 |
| Launch | 50K–2L | ₹55,000 |
| Scale | 5 Crore | ₹3,00,000 → ₹0.60/student/year |
