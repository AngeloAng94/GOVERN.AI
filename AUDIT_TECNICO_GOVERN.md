# AUDIT TECNICO — GOVERN.AI
**Data**: 01 Aprile 2026 (aggiornato post MVP v2.4)  
**Versione codebase**: MVP v2.4  
**Autore**: Audit automatico  

---

## 1. PANORAMICA ARCHITETTURA ATTUALE

### 1.1 Schema a blocchi

```
┌─────────────────────┐     HTTPS      ┌──────────────────────────┐
│   Browser (Client)  │ ──────────────► │   Kubernetes Ingress     │
│                     │                 │   (path-based routing)    │
└─────────────────────┘                 └──────┬───────────┬───────┘
                                               │           │
                                       /api/*  │           │  /*
                                               ▼           ▼
                                  ┌────────────────┐  ┌────────────────┐
                                  │   FastAPI       │  │   React (CRA)  │
                                  │   Backend       │  │   Frontend     │
                                  │   :8001         │  │   :3000        │
                                  └───────┬────────┘  └────────────────┘
                                          │
                                          │ Motor (async)
                                          ▼
                                  ┌────────────────┐
                                  │   MongoDB       │
                                  │   :27017        │
                                  │   7 collections │
                                  └────────────────┘
                                  
                                  ┌────────────────┐
                                  │     litellm     │
                                  │  (via Emergent  │
                                  │   LLM Key)      │
                                  └────────────────┘
```

### 1.2 Stack tecnologico

| Componente | Tecnologia | Versione |
|---|---|---|
| Backend framework | FastAPI | 0.110.1 |
| Backend runtime | Python / Uvicorn | 3.x / 0.25.0 |
| Frontend framework | React | 19.0.0 |
| Frontend build tool | Create React App + CRACO | CRA 5.0.1, CRACO 7.1.0 |
| Component library | Shadcn/UI (Radix primitives) | New York style |
| CSS framework | Tailwind CSS | 3.4.17 |
| Database | MongoDB (Motor async driver) | pymongo 4.5.0 / motor 3.3.1 |
| LLM integration | litellm (OpenAI GPT-4o default, configurabile via `LLM_MODEL`) | 1.80.0 |
| HTTP client (FE) | Axios | 1.8.4 |
| Routing (FE) | React Router DOM | 7.5.1 |
| Process manager | Supervisord | (sistema) |
| Validazione dati | Pydantic V2 | 2.12.5 |
| Charts | Recharts | 3.6.0 |
| PDF Export | ReportLab | 4.1.0 |
| Rate Limiting | SlowAPI | — |

### 1.3 Tipo di architettura

**Architettura modulare a due tier** con separazione frontend/backend:
- Backend: `server.py` (orchestratore) + 9 file di route modulari in `routes/` + `models.py` + `database.py` + `seed.py` + `exporters.py`
- Frontend: SPA con routing lato client, 11 pagine, componente CRUD generico `CrudPage.js`
- Database: singola istanza MongoDB, 7 collections, 15+ indici
- Autenticazione: JWT con RBAC (4 ruoli)
- LLM: litellm (provider-agnostico)
- Nessun message broker, nessuna cache

---

## 2. STRUTTURA DEL CODICE

### 2.1 Directory tree (file rilevanti)

```
/app/
├── backend/
│   ├── .env                          # Variabili ambiente
│   ├── requirements.txt              # Dipendenze Python
│   ├── server.py                     # FastAPI app + middleware + router include (~100 righe)
│   ├── models.py                     # 14 modelli Pydantic + 10 Enum (~240 righe)
│   ├── database.py                   # Connessione MongoDB + indici (~40 righe)
│   ├── seed.py                       # Dati seed enterprise (~986 righe)
│   ├── exporters.py                  # PDF/CSV generation con ReportLab
│   ├── rate_limiter.py               # Istanza condivisa slowapi
│   ├── generate_overview_pdf.py      # Generazione PDF technical overview
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py                   # Login, register, JWT, RBAC
│   │   ├── agents.py                 # CRUD agenti AI
│   │   ├── policies.py               # CRUD policy
│   │   ├── audit.py                  # Audit trail + export PDF/CSV
│   │   ├── compliance.py             # Standard compliance + export PDF
│   │   ├── dashboard.py              # Stats dashboard + KPI
│   │   ├── chat.py                   # ARIA AI assistant (SSE streaming)
│   │   ├── sox_wizard.py             # SOX Section 404 Wizard + Readiness Score
│   │   └── policy_engine.py          # Policy Conflict Detection Engine
│   └── tests/
│       ├── __init__.py
│       └── test_api.py               # Suite test API (34 test completi)
├── frontend/
│   ├── .env                          # REACT_APP_BACKEND_URL
│   ├── package.json                  # Dependencies
│   ├── tailwind.config.js            # Config Tailwind + shadcn theme
│   └── src/
│       ├── index.js                  # Entry point React
│       ├── index.css                 # CSS globale + animazioni
│       ├── App.js                    # Router principale + PageTitleUpdater
│       ├── contexts/
│       │   ├── AuthContext.js        # Gestione auth + token JWT
│       │   └── LanguageContext.js    # i18n con file JSON esterni
│       ├── pages/
│       │   ├── LandingPage.js        # Landing page con use case e social proof
│       │   ├── LoginPage.js          # Login form
│       │   ├── DashboardLayout.js    # Shell con sidebar responsive
│       │   ├── OverviewPage.js       # KPI dashboard + 3 grafici Recharts
│       │   ├── AgentsPage.js         # CRUD agenti (usa CrudPage)
│       │   ├── PoliciesPage.js       # CRUD policy (usa CrudPage)
│       │   ├── AuditPage.js          # Tabella audit + export
│       │   ├── CompliancePage.js     # Monitor compliance + export
│       │   ├── AssistantPage.js      # Chat AI ARIA (SSE streaming, react-markdown)
│       │   ├── SoxWizardPage.js      # SOX 404 Wizard con Readiness Score
│       │   └── PolicyEnginePage.js   # Policy Conflict Detection Engine
│       ├── components/
│       │   ├── CrudPage.js           # Componente CRUD generico
│       │   ├── Logo.js               # Logo ufficiale GOVERN.AI
│       │   ├── EmptyState.js         # Empty state generico
│       │   ├── SkeletonLoader.js     # Skeleton loading generico
│       │   └── ui/                   # ~39 componenti Shadcn
│       ├── locales/
│       │   ├── en.json               # Traduzioni inglese (~130+ chiavi)
│       │   └── it.json               # Traduzioni italiano (~130+ chiavi)
│       ├── hooks/
│       │   └── use-toast.js          # Hook toast
│       └── lib/
│           └── utils.js              # cn() utility
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI (4 job)
├── test_reports/
│   └── iteration_*.json              # Report test automatici (7 iterazioni)
├── memory/
│   └── PRD.md                        # Product Requirements Document
├── docker-compose.yml                # Orchestrazione 3 container
├── .env.example                      # Template variabili ambiente
├── .dockerignore                     # Docker ignore
├── README.md                         # Documentazione principale
├── AUDIT_TECNICO_GOVERN.md           # Questo documento
├── GOVERN_AI_TECHNICAL_OVERVIEW.md   # Overview tecnica dettagliata
├── GOVERN_AI_Investor_Intro_EN.md    # Deck investitori (EN)
├── GOVERN_AI_Investor_Intro_IT.md    # Deck investitori (IT)
└── GOVERN_AI_Investor_Intro_EN.pdf   # PDF investitori (EN)
```

### 2.2 Analisi file principali

| File | Righe | Responsabilita | Note |
|---|---|---|---|
| `backend/server.py` | ~100 | App FastAPI, middleware sicurezza, include 9 router | Orchestratore pulito |
| `backend/models.py` | ~240 | 14 modelli Pydantic + 10 Enum | Separato e riutilizzabile |
| `backend/seed.py` | ~986 | Dati seed enterprise banking | 14 agenti, 20+ policy, 150+ log, 20 SOX controls |
| `backend/exporters.py` | ~300+ | PDF/CSV generation (ReportLab) | Audit + Compliance + SOX report |
| `backend/routes/*.py` | ~50-150 | Endpoint specifici per dominio | 9 file modulari |
| `frontend/src/components/CrudPage.js` | ~200 | Componente CRUD generico | Riusato da Agents/Policies |
| `frontend/src/pages/SoxWizardPage.js` | ~400+ | SOX 404 controls + Readiness Score | Accordion + domain cards |
| `frontend/src/pages/PolicyEnginePage.js` | ~350+ | Conflict detection UI | Summary + filtri + resolve dialog |

### 2.3 Problemi strutturali — TUTTI RISOLTI

| ID | Problema Originale | Stato | Soluzione Applicata |
|---|---|---|---|
| S1 | Backend monolite 491 righe | RISOLTO | Split in `models.py`, `database.py`, `seed.py`, `exporters.py`, 9 file route |
| S2 | Duplicazione CRUD AgentsPage/PoliciesPage | RISOLTO | Componente generico `CrudPage.js` |
| S3 | Traduzioni inline (227 righe) | RISOLTO | File JSON esterni `en.json`, `it.json` |
| S4 | `App.css` vuoto | RISOLTO | File ignorato |

---

## 3. DATABASE & MODELLO DATI

### 3.1 Elenco collections

| Collection | Documenti (attuale) | Campi principali |
|---|---|---|
| `agents` | 14 | `id`, `name`, `description`, `model_type`, `risk_level`, `status`, `allowed_actions[]`, `restricted_domains[]`, `data_classification`, `owner`, `created_at`, `updated_at` |
| `policies` | 20+ | `id`, `name`, `description`, `agent_id`, `rule_type`, `conditions[]`, `actions[]`, `severity`, `regulation`, `enforcement`, `status`, `violations_count` |
| `audit_logs` | 150+ | `id`, `timestamp`, `agent_name`, `action`, `resource`, `outcome`, `risk_level`, `details`, `policy_name`, `user`, `ip_address` |
| `compliance_standards` | 8 | `id`, `name`, `code`, `description`, `status`, `progress`, `requirements_total`, `requirements_met`, `category`, `last_assessment`, `next_review` |
| `chat_messages` | variabile | `id`, `session_id`, `role`, `content`, `timestamp` |
| `users` | 1+ | `id`, `username`, `email`, `password_hash`, `role`, `full_name`, `created_at` |
| `sox_controls` | 20 | `id`, `domain`, `control_id`, `title`, `description`, `section`, `status`, `evidence`, `assignee`, `due_date`, `completed_date`, `risk_level` |

### 3.2 Indici

| Collection | Indici presenti |
|---|---|
| `agents` | `id` (unique), `status`, `risk_level` |
| `policies` | `id` (unique), `regulation`, `severity` |
| `audit_logs` | `id` (unique), `timestamp` (desc), `outcome`, `risk_level`, `agent_name` |
| `compliance_standards` | `id` (unique), `code` (unique) |
| `chat_messages` | `session_id` + `timestamp` (compound) |
| `users` | `id` (unique), `username` (unique) |
| `sox_controls` | `id` (unique), `domain`, `status` |

**Stato**: Tutti gli indici necessari sono stati creati. Nessun COLLSCAN sulle query principali.

### 3.3 Modelli Pydantic (14 totali)

| Modello | Scopo |
|---|---|
| `UserCreate`, `UserLogin`, `UserOut` | Autenticazione utenti |
| `AgentCreate`, `Agent` | Registro agenti AI |
| `PolicyCreate`, `Policy` | Motore policy |
| `AuditLog` | Traccia audit |
| `ComplianceStandard` | Standard normativi |
| `SoxControl`, `ControlStatus` | SOX Section 404 controls |
| `PolicyConflict`, `ConflictType`, `ConflictSeverity` | Policy Conflict Engine |
| `ChatRequest` | Messaggi chat |

### 3.4 Enum Pydantic (10 totali)

`RiskLevel`, `AgentStatus`, `PolicySeverity`, `PolicyEnforcement`, `RuleType`, `AuditOutcome`, `DataClassification`, `UserRole`, `ControlStatus`, `ConflictType`, `ConflictSeverity`

---

## 4. SICUREZZA

### 4.1 Meccanismi implementati

| Meccanismo | Stato |
|---|---|
| Autenticazione JWT (HS256, 8h) | IMPLEMENTATO |
| Autorizzazione RBAC (4 ruoli) | IMPLEMENTATO |
| Rate limiting (SlowAPI) | IMPLEMENTATO |
| CORS restrittivo (da env) | IMPLEMENTATO |
| Security headers (5 header) | IMPLEMENTATO |
| Sanitizzazione regex | IMPLEMENTATO |
| Password hashing (bcrypt) | IMPLEMENTATO |
| Enum validation (Pydantic V2) | IMPLEMENTATO |
| LLM error masking | IMPLEMENTATO |

### 4.2 Rate Limiting

| Endpoint | Limite | Motivazione |
|----------|--------|-------------|
| `/api/auth/login` | 5/min | Previene brute force |
| `/api/chat`, `/api/chat/stream` | 10/min | Controlla costi LLM |
| `/api/*/export/pdf` | 5/min | Generazione pesante |
| `/api/*/export/csv` | 10/min | File piu leggeri |
| `/api/sox/report/pdf` | 5/min | Report SOX pesante |
| Altri endpoint | 30-60/min | Uso normale |

### 4.3 Vulnerabilita precedenti — STATO

| ID | Severita | Stato | Dettaglio |
|---|---|---|---|
| V1 | ALTA | RISOLTO | Autenticazione JWT implementata (Step 2A) |
| V2 | ALTA | RISOLTO | CORS restrittivo da env (Step 1) |
| V3 | ALTA | MITIGATO | Chiave LLM in `.env` — standard per SaaS |
| V4 | ALTA | RISOLTO | Regex injection sanitizzata con re.escape (Step 1) |
| V5 | MEDIA | RISOLTO | Rate limiting su tutti gli endpoint (Step 2A) |
| V6 | MEDIA | RISOLTO | Errori LLM mascherati (Step 1) |
| V7 | MEDIA | RISOLTO | Enum Pydantic per tutti i campi tipizzati (Step 1) |
| V9 | BASSA | RISOLTO | Security headers implementati (Step 2B) |

---

## 5. PERFORMANCE & SCALABILITA

### 5.1 Punti di forza

| Aspetto | Dettaglio |
|---|---|
| Backend completamente async | Motor + FastAPI: tutte le operazioni DB sono non-bloccanti |
| Indici MongoDB completi | 15+ indici su tutte le collection (no COLLSCAN) |
| Pydantic V2 | Usa `model_dump()` — performance migliori |
| SSE Streaming | Chat ARIA con risposta streaming (chunked) |
| Proiezione `_id: 0` | Correttamente escluso `_id` da tutte le query |
| Debounce search | 300ms debounce sulla ricerca audit trail |

### 5.2 Colli di bottiglia residui

| ID | Area | Problema | Impatto |
|---|---|---|---|
| P2 | Dashboard | Query multiple per stats (non aggregate) | Latenza con volumi alti |
| P5 | Audit | Nessuna paginazione reale nel frontend | Con 10K+ log: performance degradata |
| P8 | Bundle | 39 componenti Shadcn, ~12 usati | Bundle leggermente sovradimensionato |

---

## 6. TESTING & QUALITA

### 6.1 Test automatici

| File | Tipo | Copertura | Risultato |
|---|---|---|---|
| `backend/tests/test_api.py` | Test API end-to-end (pytest) | 34 endpoint/scenario testati | **34/34 passati** |
| `test_reports/iteration_1-7.json` | Report test automatizzati (testing agent) | Backend + Frontend | 7 iterazioni, tutte passate |

### 6.2 Copertura test backend (34/34)

| Area | Test | Stato |
|---|---|---|
| Auth | login, register, token | 3/3 |
| Agents | CRUD completo | 4/4 |
| Policies | CRUD completo | 4/4 |
| Audit Trail | query, filtri, export PDF/CSV | 4/4 |
| Compliance | list, export PDF, 8 standards | 3/3 |
| Dashboard | stats | 1/1 |
| Chat | ARIA query | 1/1 |
| SOX Wizard | controls, patch, report JSON, report PDF | 4/4 |
| Readiness Score | score calculation | 1/1 |
| Policy Engine | conflicts, resolution, gaps, scan history | 4/4 |
| Standards validation | 7 standards, 8 standards | 2/2 |
| Misc | root, RBAC | 3/3 |

### 6.3 Cosa NON e coperto

| Area | Dettaglio | Rischio |
|---|---|---|
| Unit test frontend | Zero test React (jest/testing-library) | MEDIO |
| Test di performance | Nessun load test | BASSO (MVP) |
| Test a11y | Nessun test WCAG | BASSO |

### 6.4 CI/CD

| Elemento | Stato |
|---|---|
| Dockerfile | PRESENTE — backend (Python 3.11-slim) + frontend (multi-stage node+nginx) |
| docker-compose | PRESENTE — 3 container (MongoDB, Backend, Frontend) |
| GitHub Actions | PRESENTE — `.github/workflows/ci.yml` con 4 job |
| Jobs CI | backend-tests (34 pytest), frontend-build, security-scan, docker-build |

### 6.5 Qualita generale del codice

| Aspetto | Valutazione | Dettaglio |
|---|---|---|
| **Modularita** | Eccellente | 9 route file, modelli separati, seed separato |
| **Type safety** | Buono | 14 modelli Pydantic + 10 Enum tipizzati |
| **data-testid** | Eccellente | Presente su tutti gli elementi interattivi |
| **Naming** | Buono | snake_case backend, camelCase frontend, kebab-case testid |
| **Responsive** | Buono | Sidebar collapsabile + drawer mobile |
| **i18n** | Completo | 130+ chiavi EN/IT in file JSON separati |
| **Error handling** | Buono | try/except con masking errori LLM, toast frontend |
| **Logging** | Adeguato | logger su seed, chat, startup/shutdown |

---

## 7. DEBITO TECNICO RESIDUO

| ID | Area | Problema | Priorita |
|---|---|---|---|
| TD19 | Database | Date come stringhe ISO anziche `datetime` nativo | P2 |
| TD20 | Database | DB name `test_database` in dev | P3 |
| TD-FE1 | Frontend | Nessun test unitario frontend (Jest) | P2 |
| TD-FE2 | Frontend | Bundle size ottimizzabile (tree-shaking) | P3 |
| TD-BE1 | Backend | Query dashboard non aggregate in pipeline | P2 |
| TD-BE2 | Backend | Paginazione audit solo backend (frontend non usa skip) | P2 |

---

## 8. FUNZIONALITA IMPLEMENTATE — DETTAGLIO v2.4

### 8.1 SOX Foundation (Step E1 — v2.1)
- Standard SOX aggiunto come 7o framework di compliance
- Agente "SOX Internal Control Auditor" (high risk, 4 azioni)
- 3 policy SOX: Financial Reporting Integrity, Internal Control Testing, CEO/CFO Certification Workflow
- Cluster audit log SOX con 5 eventi realistici

### 8.2 SOX Section 404 Wizard (Step E2 — v2.2)
- 20 controlli SOX in 5 domini: Access Control, Change Management, IT Operations, Data Integrity, Security
- Pagina UI dedicata con domain cards, accordion controlli, edit dialog
- Export report PDF con ReportLab (SoxReportPDFBuilder)
- 4 endpoint: GET controls, PATCH control, GET report JSON, GET report PDF

### 8.3 D.Lgs. 262/2005 + Audit Readiness Score (Step E3 — v2.3)
- 8o standard: D.Lgs. 262/2005 (Italian financial reporting controls)
- 2 policy DLgs262: Attestazione Dirigente Preposto, Procedure Amministrativo-Contabili
- Agente "Dirigente Preposto Assistant" (CFO Office)
- **Audit Readiness Score**: score pesato per rischio con top 5 priority controls e domain scores
- Endpoint: GET `/api/sox/readiness-score`

### 8.4 Policy Conflict Engine (Step E4 — v2.4)
- Algoritmo di detection con 4 regole: action_conflict, gap, overlap, redundancy
- 3 endpoint: GET conflicts, POST resolve, GET scan-history
- Pagina UI con summary cards, filtri per tipo/severita, conflict cards, resolve dialog
- 5o KPI card in OverviewPage con conteggio conflitti critici
- Demo data: policy con conflitto intenzionale (block vs auto) su Fraud Detection Engine

---

## 9. RIEPILOGO STATO PROGETTO

### Completato

- **[MVP v1.0]** Landing page, Dashboard 6 sezioni, CRUD Agents/Policies, Audit Trail, Compliance 6 standard, AI Assistant, i18n EN/IT
- **[Step 1 — v1.1]** 15 indici MongoDB, sanitizzazione regex, CORS restrittivo, chat history, Enum Pydantic, debounce, lifespan, LLM error masking
- **[Step 2A — v1.2]** JWT + RBAC (4 ruoli), ARIA verticale, rate limiting
- **[Step 2B — v1.3]** Backend modulare (9 route), security headers, CrudPage generico, traduzioni JSON, react-markdown
- **[Step C1 — v1.4]** Dashboard Recharts (3 grafici), enterprise seed data (banking)
- **[Step C2 — v1.5]** Export PDF/CSV (Audit Trail + Compliance Report)
- **[Step C3A — v1.6]** Logo ufficiale, mobile sidebar responsive
- **[Step C3B — v1.7]** Docker + docker-compose, README professionale
- **[Step CICD — v1.8]** GitHub Actions CI (4 job paralleli)
- **[Step FINAL — v1.9]** Landing use cases, social proof, SSE streaming ARIA, titoli dinamici, empty states, skeleton loaders
- **[Fix v2.0]** Bar chart audit corretto, delete confirmation dialog, portabilita LLM (litellm)
- **[Step E1 — v2.1]** SOX Foundation (standard + agente + 3 policy + audit cluster)
- **[Step E2 — v2.2]** SOX Section 404 Wizard (20 controlli, 5 domini, report PDF)
- **[Step E3 — v2.3]** D.Lgs. 262/2005 (8o standard) + Audit Readiness Score
- **[Step E4 — v2.4]** Policy Conflict Detection Engine (4 regole, 3 endpoint, UI completa)

### Da completare

- **Test unitari frontend** — assenti (P2)
- **Connettori enterprise** (IAM, SIEM, ServiceNow) — non implementati (P2)
- **Multi-tenancy** — non implementato (P2)
- **D.Lgs. 262 Wizard** — workflow dedicato simile al SOX Wizard (P2)
- **Auto-Fix Engine** — risoluzione automatica conflitti policy (P2)
- **WebSocket real-time monitoring** — aggiornamenti dashboard live (P2)

---

*Fine audit tecnico. Documento generato analizzando il codice sorgente. Ultimo aggiornamento: 01 Aprile 2026 (MVP v2.4).*
