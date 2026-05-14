# GOVERN.AI — Complete Operational Manual

**Version**: MVP v3.0
**Date**: 14 May 2026
**Author**: ANTHERA Systems
**Audience**: Compliance Manager, DPO, CISO, AI Engineer, DevOps, Solution Architect

---

# Table of Contents

**PART 1 — USER GUIDE**
1. Platform introduction
2. Login, access and security
3. Main navigation
4. Overview Dashboard
5. AI Agent Registry
6. Policy Engine + Policy Guidance
7. SOX Section 404 Wizard
8. Compliance Monitor (8 standards)
9. Audit Trail
10. Intelligence Center (Score Center)
11. ARIA — AI Assistant
12. PDF/CSV Export
13. Internationalization IT/EN

**PART 2 — IMPLEMENTATION GUIDE**
14. Technical architecture
15. Data models (MongoDB)
16. REST API (complete endpoints)
17. Compliance Intelligence Engine
18. Policy and standard customization
19. LLM integration (litellm)
20. Frontend extension
21. RBAC and security

**PART 3 — DEPLOY GUIDE**
22. Local setup (Docker Compose)
23. Environment variables
24. Initial seed and demo data
25. Production deploy (Docker + Nginx)
26. CI/CD GitHub Actions
27. Monitoring, logging, backup
28. Common troubleshooting
29. Appendix — Credentials and useful links

---

# PART 1 — USER GUIDE

## 1. Platform introduction

**GOVERN.AI** is the sovereign control plane for governing AI agents in enterprises operating in regulated industries (banking, insurance, healthcare, public administration, critical infrastructure).

It allows you to:
- **Register** every AI agent with risk classification (EU AI Act)
- **Define** granular policies per regulation
- **Detect** policy conflicts with operational guidance
- **Quantify** compliance posture with a deterministic score (0-100)
- **Guide** Compliance Officers through SOX 404 wizards
- **Trace** every AI action in an explainable audit trail
- **Monitor** real-time 8 international standards
- **Export** PDF/CSV reports ready for regulators and audits

### Target personas

| Persona | Main need |
|---------|-----------|
| **Compliance Manager / DPO** | Unified visibility, quantitative score, gap management |
| **CISO** | Risk classification, audit trail, security headers |
| **Auditor (internal/external)** | Audit Readiness Score, PDF export, evidence |
| **AI Engineer** | Agent registry, lifecycle, policy enforcement |
| **Board / Investor** | Intelligence Center, posture score, trend |

---

## 2. Login, access and security

### Access

1. Open browser at `http://localhost:3000` (or your deploy URL)
2. You will be directed to the **Landing Page**
3. Click **"Get Started"** or **"Login"**
4. Enter credentials

### Demo credentials

- **Username**: `admin`
- **Password**: `AdminGovern2026!`

> In production change these credentials immediately. See section 21 — Security.

### Roles (RBAC)

| Role | Read | Write | Delete | Admin | Export |
|------|------|-------|--------|-------|--------|
| **Admin** | Yes | Yes | Yes | Yes | Yes |
| **DPO** | Yes | Yes | No | No | Yes |
| **Auditor** | Yes | No | No | No | Yes |
| **Viewer** | Yes | No | No | No | No |

### Session

- JWT signed HS256, expires after **8 hours**
- Token stored in browser localStorage
- Logout: button at top right of sidebar

---

## 3. Main navigation

### Sidebar (left)

After login the app shows the dashboard layout with collapsible sidebar and 8 main entries:

| Entry | Page | Content |
|-------|------|---------|
| Overview | `/dashboard/overview` | KPI + 3 main charts |
| Agents | `/dashboard/agents` | AI Agent registry |
| Policies | `/dashboard/policies` | Policies + Conflict Engine |
| SOX 404 | `/dashboard/sox` | SOX controls wizard |
| Audit | `/dashboard/audit` | Complete Audit Trail |
| Compliance | `/dashboard/compliance` | 8 regulatory standards |
| Intelligence | `/dashboard/intelligence` | Score Center (v3.0) |
| ARIA | `/dashboard/assistant` | AI Assistant |

### Language switch

Top right: **IT / EN** toggle.

---

## 4. Overview Dashboard

The Overview page displays:

- **4 KPI cards**: Total agents, Active policies, Total audit logs, Overall Compliance Score
- **3 Recharts**:
  - Risk distribution (pie chart)
  - Audit outcome trend (line chart)
  - Compliance progress per standard (bar chart)
- **Global governance score banner** (v3.0): tile with score, trend, quick link to Intelligence Center

### How to read the Compliance Score

- **0-49**: Critical (red) — immediate action
- **50-69**: Warning (yellow) — gaps to close
- **70-89**: Good (light green) — solid posture
- **90-100**: Excellent (dark green) — best-in-class

---

## 5. AI Agent Registry

### Content

List of all AI agents registered in the organization, with:

| Field | Description |
|-------|-------------|
| Name | Agent name |
| Type | Type (chatbot, classifier, advisor, monitor, etc.) |
| Risk Level | low / medium / high / unacceptable (EU AI Act) |
| Status | active / inactive / under_review |
| Owner | Responsible team or person |
| Description | Business function |

### Operations

- **Create** agent: button "+ Add Agent" -> form dialog
- **Edit**: "pencil" icon on row
- **Delete**: "trash" icon on row (Admin only)
- **Filter**: search bar + status and risk_level filters

### Best practices

- Register the agent **before** operational deploy
- Classify risk consistently with EU AI Act
- Associate the agent with one or more policies (see section 6)
- Use descriptive names (e.g., "Credit Scoring AI", "AML Monitor")

---

## 6. Policy Engine + Policy Guidance

### Policy

A **policy** defines a governance rule applied to one or more agents.

| Field | Description |
|-------|-------------|
| Name | Policy name |
| Regulation | Reference standard (GDPR, EU AI Act, SOX, ...) |
| Severity | low / medium / high / critical |
| Action | allow / log / require_review / block |
| Description | What the policy does |
| Status | active / draft / archived |

### Practical examples

- *GDPR Policy*: "Log all credit decisions with reasoning" — action=log
- *EU AI Act Policy*: "Block if biased input detected" — action=block
- *SOX Policy*: "Require human approval for financial decisions" — action=require_review

### Policy Conflict Engine (Step E4)

Clicking **"Run Conflict Scan"** the system automatically detects 4 anomaly types:

| Type | Description |
|------|-------------|
| **Action Conflict** | Two policies with conflicting actions on the same agent |
| **Gap** | Regulatory standard not covered by any policy |
| **Overlap** | Two policies overlapping on the same scope |
| **Redundancy** | Duplicate policies with the same action |

### Policy Guidance Engine (Step E5 — v2.5)

For each detected conflict, GOVERN.AI provides:

- **Contextual guidance**: what to do to resolve it
- **Impact analysis**: priority, urgency, business risk
- **Resolve dialog**: form to record the decision taken
- **Mandatory resolution notes** (auditable)
- **Automatic audit log** of the action

### Typical workflow

1. Create/import policies for each relevant standard
2. Run conflict scan
3. Open each conflict -> read guidance -> decide action
4. Fill resolution notes -> confirm
5. Verify recording in Audit Trail

---

## 7. SOX Section 404 Wizard

### What it does

Guided wizard for assessing the **20 SOX 404 controls** divided into **5 domains**:

1. **Access Control** (4 controls)
2. **Change Management** (4 controls)
3. **IT Operations** (4 controls)
4. **Data Integrity** (4 controls)
5. **Security** (4 controls)

### Workflow

1. Open the **SOX 404** page
2. Select a control: initial status **not_started**
3. Change status to:
   - **in_progress** (work ongoing)
   - **completed** (control satisfied)
   - **failed** (open gap)
4. Add evidence/notes in the edit dialog
5. Export the **SOX 404 Report PDF**

### Audit Readiness Score

At the bottom of the page, a **risk-weighted score** (0-100%) indicates how ready you are for a SOX audit. Computed considering:
- Number of completed vs. total controls
- Domain weight (Security/Access Control = higher weight)
- Number of failed controls (penalty)

---

## 8. Compliance Monitor (8 standards)

### Tracked standards

| Standard | Description | Demo progress |
|----------|-------------|---------------|
| EU AI Act | European AI Regulation | 45% |
| GDPR | Personal Data Protection | 78% |
| ISO 27001 | Information Security Mgmt | 92% |
| ISO 42001 | AI Management System | 34% |
| DORA | Digital Operational Resilience | 61% |
| NIS2 | Cybersecurity Directive | 83% |
| SOX | Sarbanes-Oxley (Section 404) | 56% |
| D.Lgs. 262/2005 | Italian Financial Controls | 48% |

### Available actions

- See progress, status, last update per standard
- Filter by status (Compliant / In Progress / Non Compliant)
- Open detail with specific KPIs
- Export **Compliance Report PDF**

---

## 9. Audit Trail

### Content

Complete log of every traceable platform action:

| Field | Description |
|-------|-------------|
| Timestamp | Date/time ISO 8601 (UTC) |
| Agent | AI agent involved |
| Action | Attempted action |
| Outcome | success / blocked / flagged |
| Risk Level | low / medium / high |
| Details | Explainability (JSON) |

### Filters

- By date (range picker)
- By agent
- By outcome
- By risk level

### Export

- **PDF**: report formatted for external audit
- **CSV**: for BI analysis

---

## 10. Intelligence Center (v3.0)

### Content

Investor-ready premium dashboard with:

- Central **Score Ring** (overall governance score)
- **KPI breakdown**: 4 evaluation dimensions (Agents, Policies, Audit, Compliance)
- **Top/Bottom agents** by score
- **Standard scores** (8 mini-tiles)
- **Positive and negative drivers**: what contributes in pluses/minuses
- **Methodology note**: how the score is computed
- **Insights, risks, remediation**: recommended actions
- **Score History**: snapshot with delta and trend

### How the score is computed

Deterministic algorithm (see section 17) considering:
- Agent risk distribution
- Policy status and open conflicts
- Audit outcome trend (success vs blocked)
- SOX 404 controls progress
- 8 standards coverage

### Investor use case

The Intelligence Center is designed to be shown in board meetings / due diligence:
- 1 synthetic score (main KPI)
- Historical trend (validation that posture improves)
- Driver list (transparency)
- Remediation (future visibility)

---

## 11. ARIA — AI Assistant

### What it does

ARIA is an AI advisor expert in the 8 regulations tracked by the platform. It answers in chat with **SSE streaming** with specific knowledge of:

- EU AI Act
- GDPR
- ISO 27001 / 42001
- DORA / NIS2
- SOX / D.Lgs. 262

### How to use it

1. Open **ARIA** page
2. Write a question (e.g., *"What SOX controls should I apply to credit scoring?"*)
3. ARIA replies in streaming
4. Conversations are **persisted per session**

### v3.0 contextualization

ARIA knows in real-time:
- The current governance score
- Open policy conflicts
- SOX control gaps

So it can provide **contextualized** advice on your compliance status.

---

## 12. PDF/CSV Export

| Report | Endpoint | Format |
|--------|----------|--------|
| Audit Trail | `/api/audit/export/pdf` or `/csv` | PDF / CSV |
| Compliance Report | `/api/compliance/export/pdf` | PDF |
| SOX 404 Report | `/api/sox/report/pdf` | PDF |
| Investor Score | from Intelligence Center | PDF (manual) |

All reports are generated with **ReportLab** in GOVERN.AI branded style.

---

## 13. Internationalization

- **IT/EN** fully translated (~140 i18n keys)
- Top-right toggle
- All pages, forms, tooltips and toasts are localized

---

# PART 2 — IMPLEMENTATION GUIDE

## 14. Technical architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  FRONTEND (React 19 + Vite)                   │
│  12 pages | Shadcn UI | Recharts | Tailwind | i18n IT/EN      │
└──────────────────────────────┬───────────────────────────────┘
                               │ HTTPS + JWT
┌──────────────────────────────▼───────────────────────────────┐
│                BACKEND (FastAPI + Python 3.11)                │
│  server.py + 10 routers + middleware + rate_limiter           │
│  ─────────────────────────────────────────────────────────── │
│  services/compliance_engine.py (Compliance Intelligence)      │
│  exporters.py (PDF/CSV ReportLab)                             │
└──────┬─────────────────────────────────────────────┬──────────┘
       │ Motor async                                  │ litellm
┌──────▼──────────┐                          ┌────────▼─────────┐
│   MongoDB 7.0   │                          │  LLM Provider    │
│  7 collections  │                          │  (OpenAI/Gemini) │
└─────────────────┘                          └──────────────────┘
```

### Layers

- **Frontend SPA**: React 19, Tailwind, Shadcn UI, Recharts, custom i18n
- **Modular backend**: server.py registers 10 routers (auth, agents, policies, audit, compliance, dashboard, chat, sox_wizard, policy_engine, score)
- **Service layer**: `services/compliance_engine.py` for scoring logic
- **Database**: MongoDB with Motor async, 15+ optimized indices
- **LLM**: portable via litellm (default `openai/gpt-4o`)
- **Security**: JWT HS256, bcrypt, SlowAPI rate limit, 5 security headers, restrictive CORS

---

## 15. Data models (MongoDB)

### Collections

| Collection | Typical docs | Key indices |
|------------|--------------|-------------|
| `users` | 1+ | id (unique), username (unique) |
| `agents` | 14 demo | id (unique), status, risk_level |
| `policies` | 20+ demo | id (unique), regulation, severity |
| `audit_logs` | 150+ demo | id (unique), timestamp, agent_name, outcome, risk_level |
| `compliance_standards` | 8 demo | id (unique), code (unique) |
| `chat_messages` | variable | session_id + timestamp (compound) |
| `sox_controls` | 20 | id (unique), domain, status |

### Example: Agent

```json
{
  "id": "uuid-1234",
  "name": "Credit Scoring AI",
  "type": "classifier",
  "risk_level": "high",
  "status": "active",
  "owner": "Risk Management",
  "description": "Automated credit decision support",
  "created_at": "2026-05-14T08:00:00Z"
}
```

### Example: Policy (with conflict resolution v2.5)

```json
{
  "id": "uuid-5678",
  "name": "GDPR — Log all decisions",
  "regulation": "GDPR",
  "severity": "high",
  "action": "log",
  "description": "...",
  "status": "active",
  "conflicts": [{
    "type": "overlap",
    "with_policy_id": "uuid-other",
    "guidance": "Merge policies into a single comprehensive rule",
    "impact": "medium",
    "resolution_notes": "Merged 2026-05-10 by user@example.com",
    "resolved_at": "2026-05-10T10:00:00Z"
  }]
}
```

---

## 16. REST API (complete endpoints)

> All endpoints are prefixed with `/api`. Auth via `Authorization: Bearer <JWT>` header.

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login (username + password) |
| POST | `/api/auth/register` | Registration (admin only) |
| GET | `/api/auth/me` | Current user profile |

### Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/agents` | List agents (with filters) |
| POST | `/api/agents` | Create agent |
| PATCH | `/api/agents/{id}` | Update agent |
| DELETE | `/api/agents/{id}` | Delete agent |

### Policies & Policy Engine

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/policies` | List policies |
| POST | `/api/policies` | Create policy |
| PATCH | `/api/policies/{id}` | Update |
| DELETE | `/api/policies/{id}` | Delete |
| GET | `/api/policy-engine/conflicts` | Scan conflicts |
| GET | `/api/policy-engine/conflicts/{id}/guidance` | Detailed guidance (v2.5) |
| POST | `/api/policy-engine/conflicts/{id}/resolve` | Resolve conflict with notes (v2.5) |
| GET | `/api/policy-engine/scan-history` | Scan history |

### Audit Trail

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/audit` | Filtered log list (paginated) |
| GET | `/api/audit/export/pdf` | PDF export |
| GET | `/api/audit/export/csv` | CSV export |

### Compliance

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/compliance` | List standards |
| GET | `/api/compliance/{code}` | Standard detail |
| GET | `/api/compliance/export/pdf` | PDF report |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/stats` | Overview KPI |

### SOX Wizard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sox/controls` | List 20 controls |
| PATCH | `/api/sox/controls/{id}` | Update control status |
| GET | `/api/sox/report` | JSON report |
| GET | `/api/sox/report/pdf` | PDF report |
| GET | `/api/sox/readiness-score` | Audit Readiness Score |

### Compliance Intelligence Engine (v3.0)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/score/overview` | Governance score + explainability |
| GET | `/api/score/agents` | Per-agent score |
| GET | `/api/score/agents/{id}` | Single agent score |
| GET | `/api/score/standards` | Per-standard score |
| GET | `/api/score/history` | Snapshot history |
| GET | `/api/score/insights` | Insights, risks, remediation |

### Chat (ARIA)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Single message |
| GET | `/api/chat/stream` | SSE streaming |
| GET | `/api/chat/sessions/{id}` | Session history |

### Interactive documentation

- **Swagger UI**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`

---

## 17. Compliance Intelligence Engine

### File

- `/app/backend/services/compliance_engine.py`

### Scoring logic

The governance score (0-100) is computed as a **weighted average** of:

| Dimension | Weight | Base KPI |
|-----------|--------|----------|
| Agents | 0.25 | Average risk, active status, policy coverage |
| Policies | 0.25 | Active vs draft, open conflicts, standard coverage |
| Audit | 0.20 | Success vs blocked outcomes, last-30-day trend |
| Compliance | 0.30 | Average progress of 8 standards, critical gaps |

### Structured output

```json
{
  "score": 87,
  "trend": "+4",
  "label": "Good",
  "breakdown": [
    {"dimension": "Agents", "score": 82, "weight": 0.25},
    {"dimension": "Policies", "score": 75, "weight": 0.25},
    {"dimension": "Audit", "score": 91, "weight": 0.20},
    {"dimension": "Compliance", "score": 94, "weight": 0.30}
  ],
  "positive_drivers": ["High ISO 27001 progress", "Low audit-blocked ratio"],
  "negative_drivers": ["EU AI Act gap", "3 open policy conflicts"],
  "methodology": "Weighted multi-dimensional deterministic score..."
}
```

### Snapshot history

Each scan creates a snapshot persisted in `score_snapshots`, with timestamp + score + breakdown. This enables **delta/trend** calculation.

---

## 18. Policy and standard customization

### Adding a standard

1. Edit `/app/backend/seed.py` -> `STANDARDS` array
2. Add entry with `code`, `name`, `description`, `progress`
3. Run `python backend/seed.py` to reload

### Adding a custom policy

- Via UI: Policies page -> "+ Add Policy"
- Via API: `POST /api/policies` with Pydantic payload

### Score weights

To modify weighting, open `/app/backend/services/compliance_engine.py` and change the `DIMENSION_WEIGHTS` dictionary. Weights must sum to 1.0.

---

## 19. LLM integration (litellm)

### Default

- Provider: OpenAI
- Model: `openai/gpt-4o`
- Variables: `OPENAI_API_KEY`, `LLM_MODEL`

### Provider switch

Litellm supports 100+ providers. Examples:
- **Anthropic**: `LLM_MODEL=anthropic/claude-3-5-sonnet-20241022` + `ANTHROPIC_API_KEY`
- **Gemini**: `LLM_MODEL=gemini/gemini-1.5-pro` + `GEMINI_API_KEY`
- **Local (Ollama)**: `LLM_MODEL=ollama/llama3.1` + `OLLAMA_API_BASE`

### Streaming

ARIA uses Server-Sent Events (SSE) via `/api/chat/stream`. Implemented in `routes/chat.py`.

---

## 20. Frontend extension

### Add a page

1. Create file in `/app/frontend/src/pages/MyPage.js`
2. Export `export default function MyPage() { ... }`
3. Add route in `App.js` inside `DashboardLayout`
4. Add sidebar link (`DashboardLayout.js`)

### Add i18n keys

- `/app/frontend/src/locales/it.json`
- `/app/frontend/src/locales/en.json`

Use `t("my.key")` in the component with the LanguageContext hook.

### Reusable components

- `CrudPage` for generic CRUD (see Agents/Policies pages)
- `EmptyState` for empty states
- `SkeletonLoader` for loading
- Shadcn components in `/components/ui/`

---

## 21. RBAC and security

### Route decorator

```python
@router.get("/agents")
@require_role("auditor")  # auditor or higher
async def list_agents(...):
    ...
```

### Security headers

The `server.py` middleware applies:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: same-origin`
- `Content-Security-Policy: ...`
- `Strict-Transport-Security: ...` (in production)

### Rate limiting

SlowAPI applies per-IP limits:
- `/api/auth/login`: 5/minute
- `/api/chat/*`: 30/minute
- Default: 100/minute

### Password hashing

bcrypt with cost factor 12. Configured in `routes/auth.py`.

---

# PART 3 — DEPLOY GUIDE

## 22. Local setup (Docker Compose)

### Prerequisites

- Docker >= 24.0
- Docker Compose >= 2.0
- Git

### Steps

```bash
git clone https://github.com/AngeloAng94/GOVERN.AI
cd GOVERN.AI
cp .env.example backend/.env
cp .env.example frontend/.env
docker-compose up --build
```

Open `http://localhost:3000`. Credentials: `admin / AdminGovern2026!`.

### Started services

| Service | Port | Description |
|---------|------|-------------|
| frontend | 3000 | React SPA |
| backend | 8001 | FastAPI |
| mongo | 27017 | MongoDB 7.0 |

---

## 23. Environment variables

### Backend (`backend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGO_URL` | Yes | MongoDB connection |
| `DB_NAME` | Yes | Database name |
| `OPENAI_API_KEY` | Yes | LLM API key (or litellm equivalent) |
| `LLM_MODEL` | No | Default `openai/gpt-4o` |
| `JWT_SECRET_KEY` | Yes | String >=32 chars |
| `ALLOWED_ORIGINS` | Yes | CSV of authorized origins |

### Frontend (`frontend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `REACT_APP_BACKEND_URL` | Yes | Backend public URL |

> Never commit `.env` with real values. Use `.env.example` as template.

---

## 24. Initial seed and demo data

The `/app/backend/seed.py` script loads:
- 1 admin user
- 14 enterprise AI agents
- 20+ policies with realistic conflicts
- 150+ audit logs with 7 incident clusters
- 8 regulatory standards
- 20 SOX 404 controls

### Manual execution

```bash
cd backend
python seed.py
```

The script is idempotent: if data exists, it recreates only if the collection is empty.

---

## 25. Production deploy (Docker + Nginx)

### Suggested architecture

```
[Cloudflare / WAF]
       │ TLS
       ▼
[Nginx Reverse Proxy]
   /         /api
   │           │
[Frontend]  [Backend FastAPI]
                │
            [MongoDB Atlas / Replicaset]
```

### Minimal Nginx config

```nginx
server {
    listen 443 ssl http2;
    server_name app.govern.ai;
    ssl_certificate /etc/letsencrypt/live/app.govern.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.govern.ai/privkey.pem;

    location /api/ {
        proxy_pass http://backend:8001;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_buffering off;          # for SSE
        proxy_read_timeout 3600s;
    }

    location / {
        proxy_pass http://frontend:3000;
    }
}
```

### Best practices

- TLS via Let's Encrypt
- WAF (Cloudflare, AWS WAF)
- Managed MongoDB (Atlas)
- Periodic secret rotation for `JWT_SECRET_KEY`
- Daily backups (see section 27)

---

## 26. CI/CD GitHub Actions

The `.github/workflows/ci.yml` workflow runs 4 parallel jobs on every push to `main` or `develop`:

| Job | What it does |
|-----|--------------|
| `backend-tests` | 50 pytest against live API + MongoDB |
| `frontend-build` | `yarn build` |
| `security-scan` | bandit + safety |
| `docker-build` | build backend and frontend images |

### Required secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `OPENAI_API_KEY` | No (skip LLM tests) | For end-to-end LLM tests |

---

## 27. Monitoring, logging, backup

### Logging

- Backend: structured Python log on stdout (captured by Docker)
- Frontend: errors sent to Sentry (optional)

### Recommended metrics (Prometheus + Grafana)

- Endpoint latency
- 5xx error rate
- LLM tokens consumed
- Open conflicts count

### MongoDB backup

- Atlas: native continuous snapshot
- Self-hosted: daily `mongodump` cron on S3
- Retention: minimum 30 days

### Health check

- `GET /api/health` -> `200 OK` (implement if not already present)
- Docker `healthcheck` configured in `docker-compose.yml`

---

## 28. Common troubleshooting

| Symptom | Probable cause | Solution |
|---------|---------------|----------|
| Login doesn't work | JWT_SECRET_KEY missing | Set variable and restart |
| ARIA doesn't respond | Invalid OPENAI_API_KEY | Check key, verify balance |
| Conflicts not detected | Policy without `regulation` | Fill regulation field |
| PDF not generated | Missing font in ReportLab | Verify installed fonts |
| 504 backend | Slow MongoDB | Increase `pool_size`, check indices |
| CORS error | Missing `ALLOWED_ORIGINS` | Add frontend URL |
| Blank frontend | Wrong `REACT_APP_BACKEND_URL` | Check `.env` |

### Useful logs

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongo
sudo supervisorctl status      # if installed via supervisor
tail -n 100 /var/log/supervisor/backend.*.log
```

---

## 29. Appendix — Credentials and useful links

### Demo credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `AdminGovern2026!` |

> Change immediately in production.

### Links

- **GitHub Repository**: https://github.com/AngeloAng94/GOVERN.AI
- **Swagger**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`

### Support contacts

**Angelo Anglani** — Founder
- angelo.anglani94@gmail.com
- +39 342 754 8655
- linkedin.com/in/angelo-anglani

---

*GOVERN.AI — Sovereign Control Plane for Enterprise AI.*
*A product by ANTHERA Systems.*
*Manual updated on 14 May 2026 — MVP v3.0*
