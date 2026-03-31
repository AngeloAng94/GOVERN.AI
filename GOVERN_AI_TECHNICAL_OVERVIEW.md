# GOVERN.AI — Technical Overview

## Sistema di Governance per Agenti AI Enterprise

**Versione**: MVP 1.7  
**Data**: Marzo 2026  
**Autore**: ANTHERA Systems

---

# 1. EXECUTIVE SUMMARY

## Cos'è GOVERN.AI?

GOVERN.AI è una piattaforma software (SaaS) progettata per governare, monitorare e garantire la compliance degli agenti AI nelle organizzazioni enterprise.

**In sintesi**: È il "control plane" che si posiziona tra i tuoi agenti AI e le normative europee, garantendo che ogni azione sia tracciata, conforme e auditabile.

## Il Problema che Risolve

Le aziende stanno adottando agenti AI a ritmo accelerato, ma:
- **Mancanza di visibilità**: Non sanno cosa fanno gli agenti AI
- **Rischio normativo**: EU AI Act, GDPR, DORA richiedono tracciabilità
- **Assenza di controllo**: Nessun modo per definire policy di governance
- **Audit impossibile**: Nessun log strutturato per i regolatori

## La Soluzione

GOVERN.AI fornisce:
- **Registro centralizzato** di tutti gli agenti AI
- **Motore di policy** per definire cosa possono/non possono fare
- **Audit trail completo** di ogni azione
- **Dashboard di compliance** per 6 normative EU
- **Assistente AI** esperto di regolamentazione

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
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                  │    │
│  │  │Compliance│ │Dashboard │ │   Chat   │                  │    │
│  │  │  Router  │ │  Router  │ │  Router  │                  │    │
│  │  └──────────┘ └──────────┘ └──────────┘                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
        ┌──────────────────────┴──────────────────────┐
        │                                              │
┌───────┴───────┐                          ┌──────────┴──────────┐
│   MongoDB     │                          │      litellm        │
│   Database    │                          │   (configurable)    │
│               │                          │                     │
│ • users       │                          │  ARIA AI Assistant  │
│ • agents      │                          │  System Prompt      │
│ • policies    │                          │  verticale su       │
│ • audit_logs  │                          │  compliance EU      │
│ • compliance  │                          │                     │
│ • chat_msgs   │                          │                     │
└───────────────┘                          └─────────────────────┘
```

## 2.2 Stack Tecnologico

### Frontend
| Componente | Tecnologia | Scopo |
|------------|------------|-------|
| Framework | React 19 | UI reattiva e componentizzata |
| Styling | Tailwind CSS 3.4 | Design system utility-first |
| Components | Shadcn/UI + Radix | Componenti accessibili |
| Charts | Recharts | Visualizzazioni dati |
| Routing | React Router 6 | Navigazione SPA |
| HTTP | Axios | Chiamate API con interceptor JWT |
| i18n | Custom Context | Bilingue IT/EN |

### Backend
| Componente | Tecnologia | Scopo |
|------------|------------|-------|
| Framework | FastAPI 0.110 | API REST async ad alte prestazioni |
| Runtime | Uvicorn | Server ASGI async |
| Validation | Pydantic V2 | Type safety e validazione |
| Database | Motor (async MongoDB) | Operazioni DB non bloccanti |
| Auth | python-jose + bcrypt | JWT HS256 + password hashing |
| Rate Limiting | SlowAPI | Protezione endpoint |
| PDF Export | ReportLab 4.1 | Generazione report |
| LLM | litellm | Integrazione multi-provider LLM (OpenAI GPT-4o default, configurabile via `LLM_MODEL`) |

### Infrastructure
| Componente | Tecnologia | Scopo |
|------------|------------|-------|
| Database | MongoDB 7.0 | Document store flessibile |
| Container | Docker + Compose | Deployment containerizzato |
| Proxy | Nginx | Reverse proxy + SPA routing |

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
  "model_type": "GPT-4o|Claude-3.5|Custom-ML",
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
  "rule_type": "restriction|logging|rate_limit|approval|retention",
  "conditions": ["data_request_exceeds_scope"],
  "actions": ["block_request", "log_violation", "notify_dpo"],
  "severity": "low|medium|high|critical",
  "regulation": "GDPR|EU-AI-ACT|ISO-27001|ISO-42001|DORA|NIS2",
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
  "name": "GDPR",
  "code": "GDPR",
  "description": "General Data Protection Regulation...",
  "status": "compliant|in_progress|non_compliant",
  "progress": 78,
  "requirements_total": 36,
  "requirements_met": 28,
  "category": "regulation|standard|directive",
  "last_assessment": "ISO datetime",
  "next_review": "ISO datetime"
}
```

## 3.2 Indici MongoDB

```javascript
// Performance indexes
db.agents.createIndex({ "id": 1 }, { unique: true })
db.agents.createIndex({ "status": 1 })
db.agents.createIndex({ "risk_level": 1 })

db.policies.createIndex({ "id": 1 }, { unique: true })
db.policies.createIndex({ "regulation": 1 })
db.policies.createIndex({ "severity": 1 })

db.audit_logs.createIndex({ "id": 1 }, { unique: true })
db.audit_logs.createIndex({ "timestamp": -1 })
db.audit_logs.createIndex({ "agent_name": 1 })
db.audit_logs.createIndex({ "outcome": 1 })
db.audit_logs.createIndex({ "risk_level": 1 })

db.users.createIndex({ "id": 1 }, { unique: true })
db.users.createIndex({ "username": 1 }, { unique: true })
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
     │
     │  Salva token in localStorage
     │  Axios interceptor aggiunge
     │  "Authorization: Bearer {token}"
     │  a tutte le richieste successive
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
                               │  4. Crea audit_log automatico:  │
                               │     {                           │
                               │       action: "agent_created",  │
                               │       agent_name: "...",        │
                               │       user: "admin",            │
                               │       outcome: "allowed"        │
                               │     }                           │
                               └────────────────┬────────────────┘
                                                │
┌──────────┐   { id, name, ... }           ┌────┴─────┐
│  Client  │ ◀──────────────────────────── │  Backend │
└──────────┘                               └──────────┘
```

## 4.3 Flusso ARIA AI Assistant

```
┌──────────┐   POST /api/chat              ┌──────────┐
│  Client  │ ────────────────────────────▶ │  Backend │
│          │   { message, session_id }     │          │
└──────────┘                               └────┬─────┘
                                                │
                          ┌─────────────────────┴─────────────────────┐
                          │  1. Valida lunghezza (5-2000 chars)       │
                          │  2. Rate limit check (10/min)             │
                          │  3. Carica history da chat_messages       │
                          │  4. Prepara system prompt ARIA:           │
                          │     "Sei ARIA, assistente compliance..."  │
                          │  5. Chiama LLM via litellm              │
                          │  6. Salva messaggio + risposta in DB      │
                          │  7. Log audit "chat_query"                │
                          └─────────────────────┬─────────────────────┘
                                                │
┌──────────┐   { response: "..." }         ┌────┴─────┐
│  Client  │ ◀──────────────────────────── │  Backend │
│  (react- │   Renderizzato con            │          │
│  markdown│   react-markdown              └──────────┘
└──────────┘
```

## 4.4 Flusso Export PDF

```
┌──────────┐   GET /api/audit/export/pdf   ┌──────────┐
│  Client  │ ────────────────────────────▶ │  Backend │
│          │   ?outcome=blocked&search=AML │          │
└──────────┘                               └────┬─────┘
                                                │
                          ┌─────────────────────┴─────────────────────┐
                          │  1. Verifica ruolo (auditor|dpo|admin)    │
                          │  2. Query MongoDB con filtri              │
                          │  3. Genera PDF con ReportLab:             │
                          │     • Header GOVERN.AI                    │
                          │     • Tabella audit colorata              │
                          │     • Executive Summary                   │
                          │  4. StreamingResponse con blob            │
                          └─────────────────────┬─────────────────────┘
                                                │
┌──────────┐   Content-Type: application/pdf    │
│  Client  │ ◀──────────────────────────────────┘
│          │   Content-Disposition: attachment
│ Download │   filename=audit_report_20260324.pdf
└──────────┘
```

---

# 5. SISTEMA DI SICUREZZA

## 5.1 Autenticazione JWT

```python
# Configurazione
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

# Struttura Token
{
  "sub": "admin",           # username
  "role": "admin",          # ruolo utente
  "exp": 1711324800         # scadenza (Unix timestamp)
}
```

## 5.2 RBAC (Role-Based Access Control)

```
                    ┌─────────┐
                    │  ADMIN  │
                    │ ──────  │
                    │ • Read  │
                    │ • Write │
                    │ • Delete│
                    │ • Admin │
                    └────┬────┘
                         │
              ┌──────────┴──────────┐
              │                     │
         ┌────┴────┐          ┌─────┴────┐
         │   DPO   │          │ AUDITOR  │
         │ ──────  │          │ ──────── │
         │ • Read  │          │ • Read   │
         │ • Write │          │ • Export │
         │ • Export│          └─────┬────┘
         └────┬────┘                │
              │                     │
              └──────────┬──────────┘
                         │
                    ┌────┴────┐
                    │ VIEWER  │
                    │ ─────── │
                    │ • Read  │
                    └─────────┘
```

**Implementazione:**
```python
def require_role(*allowed_roles):
    async def role_checker(request: Request):
        token = extract_token(request)
        payload = verify_jwt(token)
        user_role = payload.get("role")
        
        role_hierarchy = {
            "admin": 4, "dpo": 3, 
            "auditor": 2, "viewer": 1
        }
        
        min_required = min(role_hierarchy[r] for r in allowed_roles)
        if role_hierarchy[user_role] < min_required:
            raise HTTPException(403, "Insufficient permissions")
        
        return user_data
    return role_checker
```

## 5.3 Rate Limiting

| Endpoint | Limite | Motivazione |
|----------|--------|-------------|
| `/api/auth/login` | 5/min | Previene brute force |
| `/api/chat` | 10/min | Controlla costi LLM |
| `/api/*/export/pdf` | 5/min | Generazione pesante |
| `/api/*/export/csv` | 10/min | File più leggeri |
| Altri endpoint | 30-60/min | Uso normale |

## 5.4 Security Headers

```python
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=()"
    return response
```

---

# 6. FUNZIONALITÀ PRINCIPALI

## 6.1 Agent Registry

**Scopo**: Censire tutti gli agenti AI dell'organizzazione

**Campi tracciati**:
- Nome e descrizione
- Tipo di modello (GPT-4o, Claude, Custom ML)
- Livello di rischio (low → critical)
- Stato operativo (active/suspended/inactive)
- Azioni consentite (whitelist)
- Domini ristretti (blacklist)
- Classificazione dati
- Owner/responsabile

**Use case**: 
> Il DPO deve sapere quanti agenti AI ad alto rischio sono in produzione e chi ne è responsabile per la reportistica EU AI Act.

## 6.2 Policy Engine

**Scopo**: Definire regole di governance per gli agenti

**Tipi di regole**:
- `restriction`: blocca azioni specifiche
- `logging`: forza logging dettagliato
- `rate_limit`: limita frequenza operazioni
- `approval`: richiede approvazione umana
- `retention`: gestisce conservazione dati

**Mapping normativo**:
Ogni policy è collegata a una normativa (GDPR, EU AI Act, DORA, etc.)

**Use case**:
> Creare una policy "High-Risk AI Oversight" che blocchi decisioni automatiche di credito senza approvazione umana, come richiesto dall'EU AI Act Art. 14.

## 6.3 Audit Trail

**Scopo**: Tracciabilità completa di ogni azione AI

**Dati registrati**:
- Timestamp preciso
- Agente coinvolto
- Azione eseguita
- Risorsa acceduta
- Esito (allowed/blocked/escalated)
- Livello di rischio
- Policy applicata
- Utente/sistema richiedente
- Indirizzo IP

**Export**:
- CSV: per analisi in Excel
- PDF: per auditor e regolatori (branded, con Executive Summary)

**Use case**:
> Durante un'ispezione Garante Privacy, esportare tutti gli eventi "blocked" dell'ultimo trimestre con dettagli delle policy GDPR violate.

## 6.4 Compliance Dashboard

**Scopo**: Monitoraggio real-time dello stato di conformità

**Standard monitorati**:
| Standard | Descrizione |
|----------|-------------|
| EU AI Act | Regolamento europeo sull'AI |
| GDPR | Protezione dati personali |
| ISO 27001 | Sicurezza informazioni |
| ISO 42001 | Gestione sistemi AI |
| DORA | Resilienza digitale finanza |
| NIS2 | Cybersecurity infrastrutture |

**Metriche per standard**:
- Percentuale di avanzamento
- Requisiti soddisfatti / totali
- Stato (compliant/in progress/at risk)
- Data ultimo assessment
- Data prossima revisione

## 6.5 ARIA AI Assistant

**Scopo**: Consulente AI esperto di compliance

**System Prompt** (estratto):
```
Sei ARIA, l'assistente AI di GOVERN.AI specializzato in:
- EU AI Act e classificazione del rischio
- GDPR e protezione dei dati
- ISO 27001/42001
- DORA e NIS2

Rispondi SOLO a domande su compliance, governance AI, 
normative europee. Rifiuta educatamente domande off-topic.
```

**Caratteristiche**:
- Mantiene contesto della conversazione (session_id)
- Risponde in italiano o inglese
- Formatta risposte in Markdown (tabelle, liste, codice)
- Rate limited a 10 query/minuto

---

# 7. PERCHÉ USARE GOVERN.AI

## 7.1 Per il DPO / Compliance Manager

✅ **Visibilità totale** sugli agenti AI in produzione  
✅ **Tracciabilità** di ogni azione per audit e ispezioni  
✅ **Mapping normativo** automatico (GDPR, AI Act, DORA)  
✅ **Report pronti** per regolatori in formato PDF  
✅ **Assistente AI** sempre disponibile per dubbi normativi  

## 7.2 Per il CISO

✅ **Classificazione rischio** allineata a EU AI Act  
✅ **Policy enforcement** automatico  
✅ **Security headers** e rate limiting integrati  
✅ **RBAC granulare** (4 livelli di permessi)  
✅ **Audit immutabile** di tutte le operazioni  

## 7.3 Per il CTO / Engineering

✅ **API REST** documentata (Swagger/ReDoc)  
✅ **Architettura modulare** e manutenibile  
✅ **Stack moderno** (FastAPI, React, MongoDB)  
✅ **Docker ready** per deployment rapido  
✅ **Test suite** con 22 test automatizzati  

## 7.4 Per il CEO / Board

✅ **Riduzione rischio sanzioni** (EU AI Act: fino a €35M)  
✅ **Due diligence** documentabile per investitori  
✅ **Competitive advantage** sulla compliance  
✅ **Dashboard executive** con KPI real-time  
✅ **ROI** su costi di compliance manuale  

---

# 8. DEPLOYMENT

## 8.1 Docker Compose (Raccomandato)

```bash
# Clone
git clone https://github.com/AngeloAng94/GOVERN.AI
cd GOVERN.AI

# Configure
cp .env.example backend/.env
# Edit backend/.env con le tue chiavi

# Start
docker-compose up --build

# Access
http://localhost:3000
```

## 8.2 Architettura Container

```
┌─────────────────────────────────────────────────┐
│              Docker Compose Network              │
│                                                  │
│  ┌──────────────┐   ┌──────────────┐           │
│  │   MongoDB    │   │   Backend    │           │
│  │   :27017     │◀──│   :8001      │           │
│  │              │   │   (FastAPI)  │           │
│  └──────────────┘   └──────┬───────┘           │
│                            │                    │
│                     ┌──────┴───────┐           │
│                     │   Frontend   │           │
│                     │   :3000      │           │
│                     │ (Nginx+React)│           │
│                     └──────────────┘           │
│                                                 │
└─────────────────────────────────────────────────┘
                      │
                      ▼
               Browser Client
```

---

# 9. ROADMAP

## Completato (v1.7)

- ✅ Core platform completa
- ✅ Autenticazione JWT + RBAC
- ✅ ARIA AI Assistant
- ✅ Export PDF/CSV
- ✅ Dashboard con grafici
- ✅ Mobile responsive
- ✅ Docker deployment
- ✅ Documentazione completa

## Prossimi sviluppi

- 🔄 CI/CD con GitHub Actions
- 🔄 Streaming chat (SSE)
- 📋 Multi-tenancy
- 📋 Connettori enterprise (ServiceNow, SIEM)
- 📋 Motore rilevamento conflitti policy
- 📋 WebSocket real-time monitoring

---

# 10. CONTATTI

**Angelo Anglani**  
Founder, GOVERN.AI  

📧 angelo.anglani94@gmail.com  
📱 +39 342 754 8655  
🔗 linkedin.com/in/angelo-anglani

---

*GOVERN.AI — Sovereign Control Plane for Enterprise AI*  
*powered by ANTHERA Systems*

---

**Documento generato**: Marzo 2026  
**Versione**: 1.0
