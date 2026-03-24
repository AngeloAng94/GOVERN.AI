# GOVERN.AI

### Sovereign Control Plane for Enterprise AI

#### powered by ANTHERA | antherasystems.com

---

GOVERN.AI is the governance and compliance platform for enterprise AI agents — built for the European regulatory landscape.

Designed for **DPO**, **CISO**, **Compliance Managers** and **AI Engineers** who need to demonstrate regulatory compliance without slowing down AI adoption.

---

## Key Features

- **Agent Registry**: register and classify AI agents by risk level
- **Policy Engine**: define and enforce governance policies per normativa
- **Audit Trail**: complete log of all agent actions, exportable PDF/CSV
- **Compliance Dashboard**: monitor 6 EU standards in real-time
- **ARIA Assistant**: AI expert on EU AI Act, GDPR, DORA, NIS2
- **JWT Auth + RBAC**: 4-role hierarchy (Admin, DPO, Auditor, Viewer)
- **Analytics**: risk distribution and audit outcome charts (Recharts)
- **Export**: PDF and CSV reports for auditors and regulators

---

## Compliance Coverage

| Standard | Status | Progress |
|----------|--------|----------|
| EU AI Act | In Progress | 45% |
| GDPR | In Progress | 78% |
| ISO 27001 | Compliant | 92% |
| ISO 42001 | In Progress | 34% |
| DORA | In Progress | 61% |
| NIS2 | In Progress | 83% |

---

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Backend | FastAPI + Python | 0.110.1 |
| Runtime | Uvicorn (async) | 0.25.0 |
| Frontend | React + TailwindCSS | 19.0.0 |
| UI | Shadcn/UI + Radix | — |
| Database | MongoDB (Motor async) | 7.0 |
| LLM | GPT-5.2 via Emergent | — |
| Auth | JWT HS256 + bcrypt | — |
| Export | ReportLab (PDF) | 4.1.0 |

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
- `EMERGENT_LLM_KEY` = your Emergent API key
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
npm install
npm start
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

---

## Project Structure

```
GOVERN.AI/
├── backend/
│   ├── server.py          # FastAPI app, middleware, routers
│   ├── models.py          # Pydantic models + Enums
│   ├── database.py        # MongoDB connection + indexes
│   ├── seed.py            # Enterprise demo data
│   ├── exporters.py       # PDF/CSV generation (ReportLab)
│   ├── rate_limiter.py    # SlowAPI shared instance
│   └── routes/            # 7 modular route files
│       ├── auth.py        # JWT login/register/RBAC
│       ├── agents.py      # AI Agent CRUD
│       ├── policies.py    # Policy Engine CRUD
│       ├── audit.py       # Audit Trail + Export
│       ├── compliance.py  # Compliance standards + Export
│       ├── dashboard.py   # Stats + KPIs
│       └── chat.py        # ARIA AI Assistant
├── frontend/
│   └── src/
│       ├── contexts/      # Auth + Language (IT/EN)
│       ├── pages/         # 8 pages (Landing to Assistant)
│       ├── components/    # CrudPage, Logo, Shadcn UI
│       └── locales/       # en.json, it.json
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Roles and Permissions

| Role | Read | Write | Delete | Admin |
|------|------|-------|--------|-------|
| Admin | ✅ | ✅ | ✅ | ✅ |
| DPO | ✅ | ✅ | ❌ | ❌ |
| Auditor | ✅ | ❌ | ❌ | ❌ |
| Viewer | ✅ | ❌ | ❌ | ❌ |

**Export (PDF/CSV)** available for: Auditor, DPO, Admin

---

## Running Tests

```bash
cd backend
pytest tests/test_api.py -v
```

Expected: **22/22 tests passed**

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGO_URL` | Yes | MongoDB connection string |
| `DB_NAME` | Yes | Database name |
| `EMERGENT_LLM_KEY` | Yes | Emergent API key for GPT-5.2 |
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

## Roadmap

### ✅ Completed (MVP v1.7)

- Core platform (agents, policies, audit, compliance)
- JWT authentication + RBAC
- ARIA AI compliance assistant
- Rate limiting + security headers
- Export PDF/CSV
- Recharts analytics dashboard
- Enterprise demo data (banking scenario)
- Responsive UI with collapsible sidebar
- Bilingual IT/EN
- Docker + docker-compose

### 🔄 In Progress

- CI/CD GitHub Actions

### 📋 Planned

- Streaming chat SSE
- Multi-tenancy
- ServiceNow / SIEM connectors
- WebSocket real-time monitoring
- Policy conflict detection engine

---

## License

**MIT License** — Copyright 2026 ANTHERA Systems

Built with precision in Italy.
Designed for European AI sovereignty.

**antherasystems.com**
