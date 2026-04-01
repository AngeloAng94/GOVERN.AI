# GOVERN.AI — Technical Overview

## Sistema di Governance per Agenti AI Enterprise

**Versione**: MVP 2.4  
**Data**: Aprile 2026  
**Autore**: ANTHERA Systems

---

# 1. EXECUTIVE SUMMARY

## Cos'e GOVERN.AI?

GOVERN.AI e una piattaforma software (SaaS) progettata per governare, monitorare e garantire la compliance degli agenti AI nelle organizzazioni enterprise.

**In sintesi**: E il "control plane" che si posiziona tra i tuoi agenti AI e le normative europee e internazionali, garantendo che ogni azione sia tracciata, conforme e auditabile.

## Il Problema che Risolve

Le aziende stanno adottando agenti AI a ritmo accelerato, ma:
- **Mancanza di visibilita**: Non sanno cosa fanno gli agenti AI
- **Rischio normativo**: EU AI Act, GDPR, DORA, SOX richiedono tracciabilita
- **Assenza di controllo**: Nessun modo per definire policy di governance
- **Conflitti tra policy**: Policy contraddittorie creano rischi operativi
- **Audit impossibile**: Nessun log strutturato per i regolatori

## La Soluzione

GOVERN.AI fornisce:
- **Registro centralizzato** di tutti gli agenti AI
- **Motore di policy** con rilevamento automatico dei conflitti
- **SOX Section 404 Wizard** per la valutazione dei controlli interni
- **Audit trail completo** di ogni azione con export PDF/CSV
- **Dashboard di compliance** per **8 standard normativi**
- **Audit Readiness Score** per la prontezza alla revisione
- **Assistente AI** esperto di regolamentazione (ARIA)

---

# 2. ARCHITETTURA DEL SISTEMA

## 2.1 Overview Architetturale

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    React 19 + Tailwind                    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │   │
│  │  │ Landing  │ │Dashboard │ │  Agents  │ │ Policies │    │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │   │
│  │  │  Audit   │ │Compliance│ │   ARIA   │ │  Login   │    │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                  │   │
│  │  │SOX Wizard│ │ Policy   │ │          │                  │   │
│  │  │          │ │ Engine   │ │          │                  │   │
│  │  └──────────┘ └──────────┘ └──────────┘                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                    HTTPS / REST API                              │
└──────────────────────────────┼───────────────────────────────────┘
                               │
┌──────────────────────────────┼───────────────────────────────────┐
│                         BACKEND                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    FastAPI 0.110                          │    │
│  │  ┌─────────────────────────────────────────────────┐     │    │
│  │  │              MIDDLEWARE LAYER                    │     │    │
│  │  │  • CORS         • Security Headers              │     │    │
│  │  │  • Rate Limiting • JWT Authentication           │     │    │
│  │  └─────────────────────────────────────────────────┘     │    │
│  │                                                           │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │    │
│  │  │  Auth    │ │  Agents  │ │ Policies │ │  Audit   │    │    │
│  │  │ Router   │ │  Router  │ │  Router  │ │  Router  │    │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │    │
│  │  │Compliance│ │Dashboard │ │   Chat   │ │SOX Wizard│    │    │
│  │  │  Router  │ │  Router  │ │  Router  │ │  Router  │    │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘    │    │
│  │  ┌──────────┐                                             │    │
│  │  │ Policy   │                                             │    │
│  │  │ Engine   │                                             │    │
│  │  └──────────┘                                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
        ┌──────────────────────┴──────────────────────┐
        │                                              │
┌───────┴───────┐                          ┌──────────┴──────────┐
│   MongoDB     │                          │      litellm        │
│   Database    │                          │   (configurable)    │
│   7 coll.     │                          │                     │
│ • users       │                          │  ARIA AI Assistant  │
│ • agents      │                          │  System Prompt      │
│ • policies    │                          │  verticale su       │
│ • audit_logs  │                          │  compliance EU +    │
│ • compliance  │                          │  SOX + D.Lgs. 262   │
│ • chat_msgs   │                          │                     │
│ • sox_controls│                          │                     │
└───────────────┘                          └─────────────────────┘
```

## 2.2 Stack Tecnologico

### Frontend
| Componente | Tecnologia | Scopo |
|------------|------------|-------|
| Framework | React 19 | UI reattiva e componentizzata |
| Styling | Tailwind CSS 3.4 | Design system utility-first |
| Components | Shadcn/UI + Radix | Componenti accessibili |
| Charts | Recharts 3.6 | Visualizzazioni dati (3 grafici) |
| Routing | React Router 7 | Navigazione SPA |
| HTTP | Axios | Chiamate API con interceptor JWT |
| i18n | Custom Context | Bilingue IT/EN (130+ chiavi) |
| Markdown | react-markdown | Rendering risposte ARIA |

### Backend
| Componente | Tecnologia | Scopo |
|------------|------------|-------|
| Framework | FastAPI 0.110 | API REST async ad alte prestazioni |
| Runtime | Uvicorn | Server ASGI async |
| Validation | Pydantic V2 | Type safety con 14 modelli + 10 Enum |
| Database | Motor (async MongoDB) | Operazioni DB non bloccanti |
| Auth | python-jose + bcrypt | JWT HS256 + password hashing |
| Rate Limiting | SlowAPI | Protezione endpoint |
| PDF Export | ReportLab 4.1 | Generazione report (Audit, Compliance, SOX) |
| LLM | litellm | Provider-agnostico (OpenAI, Anthropic, Azure, etc.) |
| Streaming | SSE (StreamingResponse) | Chat ARIA in streaming |

### Infrastructure
| Componente | Tecnologia | Scopo |
|------------|------------|-------|
| Database | MongoDB 7.0 | Document store, 7 collections, 15+ indici |
| Container | Docker + Compose | Deployment containerizzato (3 servizi) |
| Proxy | Nginx | Reverse proxy + SPA routing |
| CI/CD | GitHub Actions | 4 job: test, build, security, docker |

---

# 3. MODELLO DATI

## 3.1 Schema delle Collections

### Users
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "password_hash": "bcrypt hash",
  "role": "admin|dpo|auditor|viewer",
  "full_name": "string",
  "created_at": "ISO datetime"
}
```

### Agents (Agenti AI)
```json
{
  "id": "uuid",
  "name": "Customer Due Diligence Bot",
  "description": "Automated KYC document analysis...",
  "model_type": "GPT-5.2|Claude-3.5|Custom-ML",
  "risk_level": "low|medium|high|critical",
  "status": "active|suspended|inactive",
  "allowed_actions": ["analyze_documents", "verify_identity"],
  "restricted_domains": ["personal_data_export"],
  "data_classification": "public|internal|confidential|restricted",
  "owner": "Compliance Dept",
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime"
}
```

### Policies (Regole di Governance)
```json
{
  "id": "uuid",
  "name": "PII Data Minimization",
  "description": "Enforce data minimization principle...",
  "agent_id": "uuid (optional — for conflict detection)",
  "rule_type": "restriction|logging|rate_limit|approval|retention",
  "conditions": ["data_request_exceeds_scope"],
  "actions": ["block_request", "log_violation", "notify_dpo"],
  "severity": "low|medium|high|critical",
  "regulation": "GDPR|EU-AI-ACT|ISO-27001|ISO-42001|DORA|NIS2|SOX|DLgs262",
  "enforcement": "block|log|throttle|auto",
  "violations_count": 3,
  "created_at": "ISO datetime"
}
```

### Audit Logs
```json
{
  "id": "uuid",
  "timestamp": "ISO datetime",
  "agent_name": "AML Transaction Monitor",
  "action": "transaction_analysis",
  "resource": "/transactions/wire",
  "outcome": "allowed|blocked|escalated|logged",
  "risk_level": "low|medium|high|critical",
  "details": "Routine wire transfer analysis",
  "policy_applied": "PII Data Minimization",
  "user": "m.rossi@bancaenterprise.it",
  "ip_address": "10.0.2.45"
}
```

### Compliance Standards
```json
{
  "id": "uuid",
  "name": "SOX",
  "code": "SOX",
  "description": "Sarbanes-Oxley Act - Internal controls over financial reporting...",
  "status": "compliant|in_progress|non_compliant",
  "progress": 56,
  "requirements_total": 44,
  "requirements_met": 25,
  "category": "regulation|standard|directive",
  "last_assessment": "ISO datetime",
  "next_review": "ISO datetime"
}
```

### SOX Controls (NEW in v2.2)
```json
{
  "id": "uuid",
  "domain": "Access Control|Change Management|IT Operations|Data Integrity|Security",
  "control_id": "AC-01",
  "title": "Privileged Access Management",
  "description": "Verify that privileged access...",
  "section": "404",
  "status": "not_started|in_progress|completed|failed|not_applicable",
  "evidence": "PAM tool audit report Q1 2026",
  "assignee": "IT Security Team",
  "due_date": "ISO datetime",
  "completed_date": "ISO datetime",
  "risk_level": "low|medium|high|critical"
}
```

### Policy Conflicts (computed, not stored)
```json
{
  "id": "uuid",
  "conflict_type": "action_conflict|overlap|gap|redundancy",
  "severity": "critical|high|medium|low",
  "title": "Conflicting enforcement on Fraud Detection",
  "description": "Policy A blocks while Policy B auto-approves...",
  "policy_ids": ["uuid1", "uuid2"],
  "policy_names": ["Block Suspicious", "Auto-Process Low-Risk"],
  "agent_ids": ["uuid"],
  "agent_names": ["Fraud Detection Engine"],
  "regulation": ["DORA"],
  "recommendation": "Review and resolve conflicting actions...",
  "resolved": false
}
```

## 3.2 Indici MongoDB

```javascript
// Users
db.users.createIndex({ "id": 1 }, { unique: true })
db.users.createIndex({ "username": 1 }, { unique: true })

// Agents
db.agents.createIndex({ "id": 1 }, { unique: true })
db.agents.createIndex({ "status": 1 })
db.agents.createIndex({ "risk_level": 1 })

// Policies
db.policies.createIndex({ "id": 1 }, { unique: true })
db.policies.createIndex({ "regulation": 1 })
db.policies.createIndex({ "severity": 1 })

// Audit Logs
db.audit_logs.createIndex({ "id": 1 }, { unique: true })
db.audit_logs.createIndex({ "timestamp": -1 })
db.audit_logs.createIndex({ "agent_name": 1 })
db.audit_logs.createIndex({ "outcome": 1 })
db.audit_logs.createIndex({ "risk_level": 1 })

// Compliance Standards
db.compliance_standards.createIndex({ "id": 1 }, { unique: true })
db.compliance_standards.createIndex({ "code": 1 }, { unique: true })

// Chat Messages
db.chat_messages.createIndex({ "session_id": 1, "timestamp": 1 })

// SOX Controls
db.sox_controls.createIndex({ "id": 1 }, { unique: true })
db.sox_controls.createIndex({ "domain": 1 })
db.sox_controls.createIndex({ "status": 1 })
```

---

# 4. FLUSSI APPLICATIVI

## 4.1 Flusso di Autenticazione

```
┌──────────┐     POST /api/auth/login      ┌──────────┐
│  Client  │ ─────────────────────────────▶│  Backend │
│          │   { username, password }       │          │
└──────────┘                                └────┬─────┘
                                                 │
                                    ┌────────────┴────────────┐
                                    │  1. Trova user in DB    │
                                    │  2. Verifica bcrypt     │
                                    │  3. Genera JWT (8h)     │
                                    │  4. Log audit "login"   │
                                    └────────────┬────────────┘
                                                 │
┌──────────┐     { token, user }            ┌────┴─────┐
│  Client  │ ◀─────────────────────────────│  Backend │
│          │                                │          │
└────┬─────┘                                └──────────┘
     │  Axios interceptor aggiunge
     │  "Authorization: Bearer {token}"
     ▼
```

## 4.2 Flusso CRUD con Audit

```
┌──────────┐   POST /api/agents            ┌──────────┐
│  Client  │ ────────────────────────────▶ │  Backend │
│          │   { name, risk_level, ... }   │          │
└──────────┘                               └────┬─────┘
                                                │
                               ┌────────────────┴────────────────┐
                               │  1. Valida JWT (ruolo admin/dpo)│
                               │  2. Valida Pydantic model       │
                               │  3. Inserisci in agents         │
                               │  4. Crea audit_log automatico   │
                               └────────────────┬────────────────┘
                                                │
┌──────────┐   { id, name, ... }           ┌────┴─────┐
│  Client  │ ◀──────────────────────────── │  Backend │
└──────────┘                               └──────────┘
```

## 4.3 Flusso ARIA AI Assistant (SSE Streaming)

```
┌──────────┐   GET /api/chat/stream         ┌──────────┐
│  Client  │ ────────────────────────────▶ │  Backend │
│ EventSrc │   ?message=...&session_id=... │          │
└──────────┘                               └────┬─────┘
                                                │
                          ┌─────────────────────┴─────────────────────┐
                          │  1. Valida lunghezza (5-2000 chars)       │
                          │  2. Rate limit check (10/min)             │
                          │  3. Carica history da chat_messages       │
                          │  4. System prompt ARIA (8 normative)      │
                          │  5. Chiama LLM via litellm               │
                          │  6. Streamma chunks via SSE               │
                          │  7. Salva messaggio + risposta in DB      │
                          └─────────────────────┬─────────────────────┘
                                                │
┌──────────┐   data: {"chunk": "..."}      ┌────┴─────┐
│  Client  │ ◀──────────────────────────── │  Backend │
│  (react- │   text/event-stream           │          │
│  markdown│                               └──────────┘
└──────────┘
```

## 4.4 Flusso Policy Conflict Detection (NEW in v2.4)

```
┌──────────┐   GET /api/policy-engine/conflicts   ┌──────────┐
│  Client  │ ──────────────────────────────────▶  │  Backend │
└──────────┘                                      └────┬─────┘
                                                       │
                          ┌────────────────────────────┴────────────────────────────┐
                          │  1. Fetch all policies with agent_id assigned            │
                          │  2. Group policies by agent                              │
                          │  3. For each agent, detect conflicts:                    │
                          │     a) action_conflict: block vs auto on same conditions │
                          │     b) overlap: same rule_type on same conditions        │
                          │     c) redundancy: same enforcement + actions            │
                          │  4. Detect gaps: agents without assigned policies        │
                          │  5. Return sorted conflicts (critical first)             │
                          └────────────────────────────┬────────────────────────────┘
                                                       │
┌──────────┐   [{ conflict_type, severity, ... }]  ┌───┴─────┐
│  Client  │ ◀──────────────────────────────────── │  Backend │
│  UI:     │                                       └──────────┘
│  Summary │
│  Cards   │
│  Resolve │
│  Dialog  │
└──────────┘
```

## 4.5 Flusso SOX 404 Wizard + Readiness Score (NEW in v2.2-2.3)

```
┌──────────┐   GET /api/sox/controls        ┌──────────┐
│  Client  │ ────────────────────────────▶ │  Backend │
│  SOX     │                               │          │
│  Wizard  │   GET /api/sox/readiness-score │          │
│  Page    │ ────────────────────────────▶ │          │
└──────────┘                               └────┬─────┘
                                                │
                          ┌─────────────────────┴─────────────────────┐
                          │  Controls: 20 SOX controls, 5 domains     │
                          │  Readiness Score:                          │
                          │    • Weight per risk: critical=4, high=3,  │
                          │      medium=2, low=1                       │
                          │    • Score = sum(completed weights) /      │
                          │            sum(all weights) * 100          │
                          │    • Top 5 priority controls (by pts gap)  │
                          │    • Domain-level scores                   │
                          └─────────────────────┬─────────────────────┘
                                                │
┌──────────┐   { score: 62, badge: "...",   ┌───┴──────┐
│  Client  │     priority_controls: [...],  │  Backend │
│  Score   │     domain_scores: [...] }     │          │
│  Card    │ ◀──────────────────────────── │          │
└──────────┘                               └──────────┘
```

---

# 5. SISTEMA DI SICUREZZA

## 5.1 Autenticazione JWT

```python
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

# Token structure
{
  "sub": "admin",
  "role": "admin",
  "exp": 1711324800
}
```

## 5.2 RBAC (Role-Based Access Control)

```
                    ┌─────────┐
                    │  ADMIN  │
                    │ • CRUD  │
                    │ • Delete│
                    │ • Export│
                    │ • Admin │
                    └────┬────┘
                         │
              ┌──────────┴──────────┐
         ┌────┴────┐          ┌─────┴────┐
         │   DPO   │          │ AUDITOR  │
         │ • Read  │          │ • Read   │
         │ • Write │          │ • Export │
         │ • Export│          └─────┬────┘
         └────┬────┘                │
              └──────────┬──────────┘
                    ┌────┴────┐
                    │ VIEWER  │
                    │ • Read  │
                    └─────────┘
```

## 5.3 Rate Limiting

| Endpoint | Limite | Motivazione |
|----------|--------|-------------|
| `/api/auth/login` | 5/min | Previene brute force |
| `/api/chat/*` | 10/min | Controlla costi LLM |
| `/api/*/export/pdf` | 5/min | Generazione pesante |
| `/api/*/export/csv` | 10/min | File piu leggeri |
| Altri endpoint | 30-60/min | Uso normale |

---

# 6. FUNZIONALITA PRINCIPALI

## 6.1 Agent Registry
Censimento di tutti gli agenti AI (14 nel demo). Traccia risk level, status, azioni consentite/ristrette, classificazione dati, owner.

## 6.2 Policy Engine + Conflict Detection
Definizione di regole di governance (20+ policy) mappate a 8 normative. Il **Policy Conflict Engine** (v2.4) rileva automaticamente:
- **Action Conflict**: policy con enforcement contraddittorio sullo stesso agente
- **Overlap**: policy con stesse condizioni e rule_type sullo stesso agente
- **Gap**: agenti senza policy assegnate
- **Redundancy**: policy duplicate sullo stesso agente

## 6.3 Audit Trail
Tracciabilita completa con 150+ log demo, 7 incident cluster, export PDF/CSV.

## 6.4 Compliance Dashboard
Monitoraggio real-time di **8 standard**: EU AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2, SOX, D.Lgs. 262/2005.

## 6.5 SOX Section 404 Wizard
Workflow guidato per la valutazione dei controlli interni con:
- 20 controlli in 5 domini
- Progress bar per dominio
- Edit dialog per aggiornare status/evidence
- Export report PDF
- **Audit Readiness Score** pesato per rischio

## 6.6 ARIA AI Assistant
Consulente AI esperto di compliance con:
- SSE streaming (risposta in tempo reale)
- Memoria conversazionale (session_id)
- System prompt verticale su 8 normative
- Rate limited a 10 query/minuto
- Rendering Markdown (tabelle, liste, codice)

---

# 7. PERCHE USARE GOVERN.AI

## 7.1 Per il DPO / Compliance Manager
- Visibilita totale sugli agenti AI
- Tracciabilita per audit e ispezioni
- Mapping normativo automatico (8 standard)
- Report pronti per regolatori in PDF
- SOX 404 Wizard per controlli interni
- Rilevamento conflitti tra policy

## 7.2 Per il CISO
- Classificazione rischio allineata a EU AI Act
- Policy enforcement automatico
- Security headers e rate limiting
- RBAC granulare (4 livelli)
- Audit Readiness Score per preparazione audit

## 7.3 Per il CTO / Engineering
- API REST documentata (Swagger/ReDoc)
- Architettura modulare (9 route, 14 modelli)
- Stack moderno (FastAPI, React, MongoDB)
- Docker ready + CI/CD GitHub Actions
- 34 test automatizzati con pytest

## 7.4 Per il CEO / Board
- Riduzione rischio sanzioni (EU AI Act: fino a 35M EUR)
- Due diligence documentabile
- Dashboard executive con KPI real-time
- Audit Readiness Score per board reporting
- 8 framework normativi coperti

---

# 8. DEPLOYMENT

## 8.1 Docker Compose (Raccomandato)

```bash
git clone https://github.com/AngeloAng94/GOVERN.AI
cd GOVERN.AI
cp .env.example backend/.env
docker-compose up --build
# Access: http://localhost:3000
```

## 8.2 Architettura Container

```
┌─────────────────────────────────────────────────┐
│              Docker Compose Network              │
│                                                  │
│  ┌──────────────┐   ┌──────────────┐           │
│  │   MongoDB    │   │   Backend    │           │
│  │   :27017     │◀──│   :8001      │           │
│  │   7 coll.    │   │   FastAPI    │           │
│  └──────────────┘   └──────┬───────┘           │
│                            │                    │
│                     ┌──────┴───────┐           │
│                     │   Frontend   │           │
│                     │   :3000      │           │
│                     │ Nginx+React  │           │
│                     └──────────────┘           │
└─────────────────────────────────────────────────┘
```

---

# 9. ROADMAP

## Completato (MVP v2.4)

- Core platform (agents, policies, audit, compliance)
- JWT + RBAC (4 ruoli)
- ARIA AI Assistant con SSE streaming
- Export PDF/CSV (Audit, Compliance, SOX)
- Dashboard con 3 grafici Recharts
- 8 standard normativi
- SOX Section 404 Wizard + Audit Readiness Score
- D.Lgs. 262/2005 (Italian financial reporting controls)
- Policy Conflict Detection Engine
- Mobile responsive + sidebar collassabile
- Bilingue IT/EN (130+ chiavi)
- Docker + CI/CD GitHub Actions (4 job)
- 34/34 test backend

## Prossimi sviluppi

- Multi-tenancy
- Connettori enterprise (ServiceNow, SIEM, IAM)
- D.Lgs. 262 Wizard dedicato
- Auto-Fix Engine per conflitti policy
- WebSocket real-time monitoring
- Test unitari frontend

---

# 10. CONTATTI

**Angelo Anglani**  
Founder, GOVERN.AI  

angelo.anglani94@gmail.com  
+39 342 754 8655  
linkedin.com/in/angelo-anglani

---

*GOVERN.AI — Sovereign Control Plane for Enterprise AI*  
*powered by ANTHERA Systems*

---

**Documento generato**: Aprile 2026  
**Versione**: 2.4
