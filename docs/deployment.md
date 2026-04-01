# EduForge — Deployment Guide

---

## Local Development

### Prerequisites
- Python 3.12
- Docker + Docker Compose
- Git

### Setup

```bash
# 1. Clone
git clone https://github.com/sravanmodemkumar-arch/mocktest.git
cd mocktest

# 2. Environment
cp .env.example .env
# Edit .env — set DATABASE_URL, JWT_SECRET_KEY

# 3. Start PostgreSQL
docker-compose up db -d

# 4. Identity service
cd identity
py -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

API docs available at: `http://localhost:8001/docs`

---

## Run All Services (Docker)

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Identity | http://localhost:8001 |
| Portal | http://localhost:8002 |
| Exam | http://localhost:8003 |

---

## Branch Strategy

| Branch | Purpose | Merges To |
|---|---|---|
| `main` | Production-ready code | — |
| `feature/project-setup-auth` | Auth service setup | main |
| `feature/docs` | Documentation | main |
| `feature/portal-pages` | Staff portal (next) | main |
| `feature/exam-engine` | Mock test engine (upcoming) | main |
| `feature/notes-videos` | Notes + YouTube (upcoming) | main |

### Workflow
```bash
# Start new feature
git checkout main
git pull origin main
git checkout -b feature/your-feature

# Push and open PR
git push -u origin feature/your-feature
# → Open PR on GitHub → Get review → Merge to main
```

---

## CI/CD Pipeline (GitHub Actions)

### On every push / PR → `ci.yml`
1. Checkout code
2. Setup Python 3.11 + 3.12 matrix
3. Install dependencies (`pip install -r requirements.txt`)
4. Lint — `flake8`
5. Format check — `black --check`
6. Tests — `pytest`

### On merge to `main` → `deploy.yml`
1. Setup Python 3.12
2. Install dependencies
3. Run pre-deploy tests
4. Deploy to AWS Lambda / ECS

---

## Production Infrastructure

| Component | Service | Notes |
|---|---|---|
| Identity, Exam, Billing, AI | AWS Lambda | Auto-scales, pay per call |
| Portal (Django HTMX) | AWS ECS Fargate | Always-on, 2× tasks minimum |
| Database | AWS RDS PostgreSQL 16 | db.t4g.medium to start |
| File Storage | Cloudflare R2 | Zero egress cost |
| CDN + WAF | Cloudflare | Serves 99% of all reads |
| Queue | AWS SQS | Async between services |
| Scheduler | AWS EventBridge | Nightly cleanup, rank jobs |
| Secrets | AWS KMS | Encryption keys |
| Monitoring | AWS CloudWatch + Sentry | Logs + error tracking |
| DNS | Cloudflare | All domains |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `JWT_SECRET_KEY` | Yes | JWT signing key — keep secret |
| `JWT_ALGORITHM` | No | Default: HS256 |
| `JWT_ACCESS_EXPIRE_MINUTES` | No | Default: 30 |
| `JWT_REFRESH_EXPIRE_DAYS` | No | Default: 7 |
| `OTP_EXPIRE_MINUTES` | No | Default: 5 |
| `WHATSAPP_TOKEN` | Yes (prod) | Meta Business API token |
| `WHATSAPP_PHONE_ID` | Yes (prod) | WhatsApp phone number ID |
| `MSG91_API_KEY` | Yes (prod) | SMS fallback |
| `APP_ENV` | No | development / production |
| `DEBUG` | No | true / false |

---

## Scaling Plan

| Phase | Students | Database | Fargate | Monthly Cost |
|---|---|---|---|---|
| Phase 1 | 0 – 50K | db.t4g.medium | 2× tasks | Rs. 25,000 – 42,000 |
| Phase 2 | 50K – 2L | db.t4g.large + 1 replica | 4× tasks | Rs. 55,000 – 85,000 |
| Phase 3 | 2L – 10L | db.r6g.large + 2 replicas | 8× tasks | Rs. 1,50,000 – 3,00,000 |
| Phase 4 | 10L+ | Aurora PostgreSQL Serverless v2 | Auto | Rs. 3,00,000+ |
