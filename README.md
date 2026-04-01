# GOVERN.AI

![CI](https://github.com/AngeloAng94/GOVERN.AI/actions/workflows/ci.yml/badge.svg)
![Version](https://img.shields.io/badge/version-MVP%20v2.4-blue)
![Tests](https://img.shields.io/badge/tests-34%2F34%20passed-brightgreen)
![Standards](https://img.shields.io/badge/compliance-8%20standards-orange)
![License](https://img.shields.io/badge/license-MIT-green)

### Sovereign Control Plane for Enterprise AI

#### powered by ANTHERA | antherasystems.com

---

GOVERN.AI is the governance and compliance platform for enterprise AI agents — built for the European and international regulatory landscape.

Designed for **DPO**, **CISO**, **Compliance Managers** and **AI Engineers** who need to demonstrate regulatory compliance without slowing down AI adoption.

---

## Key Features

- **Agent Registry**: register and classify AI agents by risk level (14 enterprise agents demo)
- **Policy Engine**: define and enforce governance policies per normativa with **automated conflict detection**
- **Policy Conflict Detection**: identifies action conflicts, gaps, overlaps, and redundancies across policies
- **SOX Section 404 Wizard**: guided workflow for internal control assessment with **Audit Readiness Score**
- **Audit Trail**: complete log of all agent actions, exportable PDF/CSV
- **Compliance Dashboard**: monitor **8 regulatory standards** in real-time
- **ARIA Assistant**: AI expert on EU AI Act, GDPR, DORA, NIS2, SOX, D.Lgs. 262 — with **SSE streaming**
- **JWT Auth + RBAC**: 4-role hierarchy (Admin, DPO, Auditor, Viewer)
- **Analytics**: risk distribution, audit outcome, and compliance progress charts (Recharts)
- **Export**: PDF and CSV reports for auditors and regulators
- **Bilingual**: full IT/EN internationalization

---

## Compliance Coverage

| Standard | Description | Status | Progress |
|----------|-------------|--------|----------|
| EU AI Act | European AI Regulation | In Progress | 45% |
| GDPR | Data Protection Regulation | In Progress | 78% |
| ISO 27001 | Information Security Management | Compliant | 92% |
| ISO 42001 | AI Management System | In Progress | 34% |
| DORA | Digital Operational Resilience | In Progress | 61% |
| NIS2 | Cybersecurity Directive | In Progress | 83% |
| SOX | Sarbanes-Oxley Act (Section 404) | In Progress | 56% |
| D.Lgs. 262/2005 | Italian Financial Reporting Controls | In Progress | 48% |

---

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Backend | FastAPI + Python | 0.110.1 |
| Runtime | Uvicorn (async) | 0.25.0 |
| Frontend | React + TailwindCSS | 19.0.0 |
| UI | Shadcn/UI + Radix | — |
| Database | MongoDB (Motor async) | 7.0 |
| LLM | litellm (OpenAI GPT-4o default, configurable) | 1.80.0 |
| Auth | JWT HS256 + bcrypt | — |
| Export | ReportLab (PDF) | 4.1.0 |
| Charts | Recharts | 3.6.0 |

---

## Quick Start — Docker (Recommended)

**Prerequisites:** Docker >= 24.0, Docker Compose >= 2.0, Git

### Step 1 — Clone

```bash
git clone https://github.com/AngeloAng94/GOVERN.AI
cd GOVERN.AI
```

### Step 2 — Configure

```bash
cp .env.example backend/.env
```

Edit `backend/.env` and set:
- `OPENAI_API_KEY` = your OpenAI API key (or any litellm-compatible key)
- `LLM_MODEL` = model identifier (default: `openai/gpt-4o`)
- `JWT_SECRET_KEY` = random string, min 32 chars

```bash
cp .env.example frontend/.env
```

(default values work for local development)

### Step 3 — Start

```bash
docker-compose up --build
```

### Step 4 — Open

```
http://localhost:3000
```

**Default credentials** (CHANGE IN PRODUCTION):
- Username: `admin`
- Password: `AdminGovern2026!`

---

## Manual Setup — Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload --port 8001
```

### Frontend

```bash
cd frontend
yarn install
yarn start
```

### MongoDB (Docker only)

```bash
docker run -d -p 27017:27017 --name mongo mongo:7.0
```

---

## API Documentation

When backend is running:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Key API Endpoints

| Group | Endpoint | Method | Description |
|-------|----------|--------|-------------|
| Auth | `/api/auth/login` | POST | JWT authentication |
| Auth | `/api/auth/register` | POST | User registration |
| Agents | `/api/agents` | GET/POST | Agent CRUD |
| Policies | `/api/policies` | GET/POST | Policy CRUD |
| Audit | `/api/audit` | GET | Audit trail with filters |
| Audit | `/api/audit/export/pdf` | GET | Export audit report PDF |
| Audit | `/api/audit/export/csv` | GET | Export audit report CSV |
| Compliance | `/api/compliance` | GET | Compliance standards |
| Compliance | `/api/compliance/export/pdf` | GET | Export compliance report |
| Dashboard | `/api/dashboard/stats` | GET | Dashboard KPIs |
| Chat | `/api/chat` | POST | ARIA AI assistant |
| Chat | `/api/chat/stream` | GET | ARIA SSE streaming |
| SOX | `/api/sox/controls` | GET | SOX 404 controls |
| SOX | `/api/sox/controls/{id}` | PATCH | Update control status |
| SOX | `/api/sox/report` | GET | SOX report JSON |
| SOX | `/api/sox/report/pdf` | GET | SOX report PDF |
| SOX | `/api/sox/readiness-score` | GET | Audit Readiness Score |
| Policy Engine | `/api/policy-engine/conflicts` | GET | Detect policy conflicts |
| Policy Engine | `/api/policy-engine/conflicts/{id}/resolve` | POST | Resolve conflict |
| Policy Engine | `/api/policy-engine/scan-history` | GET | Scan history |

---

## Project Structure

```
GOVERN.AI/
├── backend/
│   ├── server.py          # FastAPI app, middleware, routers
│   ├── models.py          # Pydantic models + Enums (14 models)
│   ├── database.py        # MongoDB connection + indexes
│   ├── seed.py            # Enterprise demo data (banking scenario)
│   ├── exporters.py       # PDF/CSV generation (ReportLab)
│   ├── rate_limiter.py    # SlowAPI shared instance
│   └── routes/            # 9 modular route files
│       ├── auth.py        # JWT login/register/RBAC
│       ├── agents.py      # AI Agent CRUD
│       ├── policies.py    # Policy Engine CRUD
│       ├── audit.py       # Audit Trail + Export
│       ├── compliance.py  # Compliance standards + Export
│       ├── dashboard.py   # Stats + KPIs
│       ├── chat.py        # ARIA AI Assistant (SSE streaming)
│       ├── sox_wizard.py  # SOX Section 404 Wizard + Readiness Score
│       └── policy_engine.py # Policy Conflict Detection Engine
├── frontend/
│   └── src/
│       ├── contexts/      # Auth + Language (IT/EN)
│       ├── pages/         # 11 pages (Landing to PolicyEngine)
│       │   ├── LandingPage.js
│       │   ├── LoginPage.js
│       │   ├── DashboardLayout.js
│       │   ├── OverviewPage.js      # KPI + 3 charts
│       │   ├── AgentsPage.js
│       │   ├── PoliciesPage.js
│       │   ├── AuditPage.js
│       │   ├── CompliancePage.js
│       │   ├── AssistantPage.js     # ARIA with SSE streaming
│       │   ├── SoxWizardPage.js     # SOX 404 controls + Readiness Score
│       │   └── PolicyEnginePage.js  # Conflict detection UI
│       ├── components/    # CrudPage, Logo, EmptyState, SkeletonLoader, Shadcn UI
│       └── locales/       # en.json, it.json (~130+ keys each)
├── docker-compose.yml
├── .env.example
├── .github/workflows/ci.yml
└── README.md
```

---

## Roles and Permissions

| Role | Read | Write | Delete | Admin | Export |
|------|------|-------|--------|-------|--------|
| Admin | yes | yes | yes | yes | yes |
| DPO | yes | yes | no | no | yes |
| Auditor | yes | no | no | no | yes |
| Viewer | yes | no | no | no | no |

---

## Running Tests

```bash
cd backend
pytest tests/test_api.py -v
```

Expected: **34/34 tests passed**

Test coverage includes:
- Authentication (login, register, token validation)
- CRUD operations (agents, policies)
- Audit trail (query, export)
- Compliance standards (8 standards validation)
- SOX 404 Wizard (controls, report, readiness score)
- Policy Conflict Engine (detection, resolution, scan history)
- Dashboard statistics
- Chat API (ARIA assistant)

---

## CI/CD

Every push to `main` or `develop` triggers the GitHub Actions pipeline:

| Job | What it verifies |
|-----|------------------|
| `backend-tests` | 34 pytest against live API + MongoDB |
| `frontend-build` | `yarn build` completes without errors |
| `security-scan` | bandit + safety on Python dependencies |
| `docker-build` | `docker build` for backend + frontend images |

### GitHub Secrets Configuration

To enable the full pipeline, configure this secret in your GitHub repository:

**Settings > Secrets and variables > Actions > New repository secret**

| Secret | Value | Required |
|--------|-------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Optional* |

*If `OPENAI_API_KEY` is not configured, the backend-tests job will skip LLM-dependent tests. The pipeline will not fail.

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGO_URL` | Yes | MongoDB connection string |
| `DB_NAME` | Yes | Database name |
| `OPENAI_API_KEY` | Yes | OpenAI API key (or any litellm-compatible provider) |
| `LLM_MODEL` | No | LLM model identifier (default: `openai/gpt-4o`) |
| `JWT_SECRET_KEY` | Yes | JWT signing secret (32+ chars) |
| `ALLOWED_ORIGINS` | Yes | CORS allowed origins |
| `REACT_APP_BACKEND_URL` | Yes | Backend URL for frontend |

---

## Security

- JWT HS256 authentication with 8h token expiry
- bcrypt password hashing
- RBAC with 4 hierarchical roles
- Rate limiting on all endpoints (SlowAPI)
- CORS restricted to allowed origins
- Security headers: X-Frame-Options, CSP, X-Content-Type-Options, Referrer-Policy
- Input sanitization with Pydantic V2 + Enum validation
- Regex injection prevention (re.escape)
- LLM error masking (no stacktrace exposure)

---

## Demo Data

The platform ships with realistic enterprise banking demo data:

| Entity | Count | Details |
|--------|-------|---------|
| AI Agents | 14 | Including SOX Auditor, Dirigente Preposto, AML Monitor, Fraud Detection |
| Policies | 20+ | Across all 8 regulatory standards with intentional conflicts |
| Audit Logs | 150+ | 7 incident clusters + random distribution over 30 days |
| Compliance Standards | 8 | With realistic progress percentages |
| SOX Controls | 20 | 5 domains (Access Control, Change Mgmt, IT Ops, Data Integrity, Security) |

---

## Roadmap

### Completed (MVP v2.4)

- Core platform (agents, policies, audit, compliance)
- JWT authentication + RBAC (4 roles)
- ARIA AI compliance assistant with SSE streaming
- Rate limiting + security headers
- Export PDF/CSV
- Recharts analytics dashboard (3 charts)
- Enterprise demo data (banking scenario)
- Responsive UI with collapsible sidebar + mobile drawer
- Bilingual IT/EN
- Docker + docker-compose
- CI/CD GitHub Actions (4/4 jobs green)
- Portable LLM via litellm (any OpenAI-compatible provider)
- SOX Foundation (standard + agent + 3 policies + audit cluster)
- SOX Section 404 Wizard (20 controls, 5 domains, progress tracking)
- Audit Readiness Score (risk-weighted scoring algorithm)
- D.Lgs. 262/2005 (Italian financial reporting controls standard)
- Policy Conflict Detection Engine (action conflicts, gaps, overlaps, redundancies)
- Landing page with real use cases (Banking, Healthcare, Legal)
- Empty states + skeleton loaders
- Dynamic page titles

### Planned

- Multi-tenancy
- ServiceNow / SIEM / IAM connectors
- WebSocket real-time monitoring
- D.Lgs. 262 Wizard (dedicated workflow)
- Auto-Fix Engine (automated conflict resolution)
- Frontend unit tests (Jest + Testing Library)

---

## License

**MIT License** — Copyright 2026 ANTHERA Systems

Built with precision in Italy.
Designed for European AI sovereignty.

**antherasystems.com**
