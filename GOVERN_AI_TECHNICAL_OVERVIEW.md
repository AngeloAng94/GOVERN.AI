# GOVERN.AI — Technical Overview

## Sovereign Control Plane for Enterprise AI

**Versione**: MVP 3.0  
**Data**: 14 Maggio 2026  
**Autore**: ANTHERA Systems

---

# 1. EXECUTIVE SUMMARY

## Cos'e GOVERN.AI?

GOVERN.AI e una piattaforma software (SaaS) progettata per governare, monitorare e garantire la compliance degli agenti AI nelle organizzazioni enterprise.

**In sintesi**: E il "control plane" che si posiziona tra i tuoi agenti AI e le normative europee e internazionali, garantendo che ogni azione sia tracciata, conforme e auditabile — con un **motore di scoring proprietario** che valuta in tempo reale la postura di governance.

## Il Problema che Risolve

Le aziende stanno adottando agenti AI a ritmo accelerato, ma:
- **Mancanza di visibilita**: Non sanno cosa fanno gli agenti AI
- **Rischio normativo**: EU AI Act, GDPR, DORA, SOX richiedono tracciabilita
- **Assenza di controllo**: Nessun modo per definire policy di governance
- **Conflitti tra policy**: Policy contraddittorie creano rischi operativi
- **Nessuna misura**: Nessuno score oggettivo della postura di compliance
- **Audit impossibile**: Nessun log strutturato per i regolatori

## La Soluzione

GOVERN.AI fornisce:
- **Registro centralizzato** di tutti gli agenti AI
- **Motore di policy** con rilevamento automatico dei conflitti e guidance operativa
- **Compliance Intelligence Engine** — scoring deterministico e spiegabile
- **Intelligence Center** — dashboard premium con score, ranking, rischi e remediation
- **SOX Section 404 Wizard** con Audit Readiness Score
- **Audit trail completo** con export PDF/CSV
- **Dashboard di compliance** per **8 standard normativi**
- **Assistente AI (ARIA)** esperto di regolamentazione con streaming

---

# 2. ARCHITETTURA DEL SISTEMA

## 2.1 Overview Architetturale

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (12 pagine)                     │
│  React 19 + Tailwind + Shadcn UI + Recharts                     │
│  Landing | Dashboard | Agents | Policies | Audit | Compliance   │
│  ARIA | SOX Wizard | Policy Engine | Intelligence Center        │
└──────────────────────────────┼───────────────────────────────────┘
                               │ HTTPS / REST API
┌──────────────────────────────┼───────────────────────────────────┐
│                         BACKEND (10 route)                        │
│  FastAPI 0.110 + Pydantic V2 + Motor (async MongoDB)             │
│  ┌──────────────────────────────────────────────────────┐        │
│  │ services/compliance_engine.py                        │        │
│  │   score_agent() | score_standard() | overview()      │        │
│  │   explainability | history & momentum                │        │
│  └──────────────────────────────────────────────────────┘        │
│  Auth | Agents | Policies | Audit | Compliance | Dashboard       │
│  Chat (SSE) | SOX Wizard | Policy Engine | Score API             │
└──────────────────────────────┼───────────────────────────────────┘
                               │
         ┌─────────────────────┴─────────────────────┐
    ┌────┴─────┐                              ┌──────┴────┐
    │ MongoDB  │                              │  litellm  │
    │ 8 coll.  │                              │ (ARIA AI) │
    └──────────┘                              └───────────┘
```

## 2.2 Stack Tecnologico

| Layer | Tecnologia | Scopo |
|-------|------------|-------|
| Frontend | React 19 + Tailwind 3.4 + Shadcn/UI | UI reattiva |
| Charts | Recharts 3.6 (RadialBar, Pie, Bar, Area) | Visualizzazioni |
| Backend | FastAPI 0.110 + Uvicorn | API REST async |
| Validation | Pydantic V2 (15 modelli + 10 Enum) | Type safety |
| Database | MongoDB 7.0 + Motor (async) | 8 collections |
| Auth | JWT HS256 + bcrypt | Autenticazione |
| LLM | litellm (provider-agnostico) | ARIA assistant |
| Export | ReportLab 4.1 | Report PDF |
| DevOps | Docker Compose + GitHub Actions CI | Deployment |

### AI Provider — Dual Mode (v3.1)

- **Primary (Sovereign):** Apertus-70B-Instruct (Swiss AI Initiative)
  via Public AI Swiss (`platform.publicai.co`).
  Licenza Apache 2.0 — EU/CH sovereign — EU AI Act compliant.
- **Fallback (Performance):** GPT-4o (OpenAI).
  Attivo automaticamente se Apertus non configurato o in errore.
- **Abstraction layer:** litellm (zero code change per switch provider).
- **Toggle:** UI Settings (admin) o variabili ambiente (ops).

---

# 3. COMPLIANCE INTELLIGENCE ENGINE

Il cuore proprietario della piattaforma. Un motore deterministico, spiegabile e modulare.

## 3.1 Cosa Calcola

| Output | Descrizione |
|--------|-------------|
| **Agent Score** (0-100) | Valutazione per ciascun agente AI |
| **Standard Score** (0-100) | Valutazione per ciascuno degli 8 standard normativi |
| **Overall Governance Score** | Punteggio complessivo pesato |
| **Score Band** | excellent / strong / warning / critical |
| **Top Risks** | Rischi principali ordinati per impatto |
| **Missing Controls** | Controlli mancanti per agenti scoperti |
| **Priority Remediations** | Azioni correttive ordinate per impatto |
| **Explainability** | Spiegazione completa di ogni punteggio |

## 3.2 Formula di Scoring

**Agent Score:**
```
base = risk_level_map(critical=25, high=45, medium=65, low=82)
+ policy_coverage (+15 max con policy, -20 senza = gap)
+ audit_outcome_factor (+/-15 da ratio allowed/total)
- conflict_penalty (critical=-18, high=-10, medium=-5)
+ status_factor (active=0, suspended=-10, inactive=-20)
```

**Standard Score:**
```
base = progress_percentage
+ requirements_bonus (delta ratio vs progress)
+ policy_coverage (+12 max, -8 senza)
- conflict_penalty per regulation
```

**Overall:** `standards * 55% + agents * 45% - global_critical_penalty (max -15)`

## 3.3 Explainability Layer

Ogni score include un payload strutturato:
- `explanation_summary` — descrizione leggibile
- `why_this_score` — formula con dati reali
- `strongest_positive_factor` / `strongest_negative_factor`
- `methodology_note` — "deterministico, nessun LLM nel calcolo"
- `score_breakdown` — decomposizione numerica

## 3.4 Score History & Momentum

- Snapshot salvati automaticamente a ogni calcolo
- `previous_score`, `delta_score`, `trend_direction` per ogni entita
- Trend visibili nell'Intelligence Center

## 3.5 Integrazione Policy Conflict Engine

- Conflitti non risolti impattano direttamente lo score (-18 pts per critical)
- Gap → missing controls nell'output
- Overlap/redundancy → remediation suggestions
- Il Policy Conflict Engine e una sorgente strutturata del motore di scoring

---

# 4. FUNZIONALITA PRINCIPALI

## 4.1 Agent Registry
14 agenti enterprise demo con risk classification e status tracking.

## 4.2 Policy Engine + Conflict Detection + Guidance
20+ policy su 8 normative. Rilevamento automatico di 4 tipi di conflitto (action_conflict, gap, overlap, redundancy). Guidance operativa con impact analysis. Risoluzione documentata con audit trail.

## 4.3 SOX Section 404 Wizard
20 controlli in 5 domini. Audit Readiness Score pesato per rischio. Export report PDF.

## 4.4 Audit Trail
150+ log demo. Filtri multipli. Export PDF branded e CSV.

## 4.5 Compliance Dashboard
8 standard: EU AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2, SOX, D.Lgs. 262/2005.

## 4.6 Intelligence Center (v3.0)
Dashboard premium con: score ring, score composition, agent distribution, agent ranking, standard scores, active insights, priority remediations, top risks, missing controls.

## 4.7 ARIA AI Assistant
SSE streaming, memoria conversazionale, system prompt verticale su 8 normative + Compliance Intelligence Engine. Puo spiegare perche un agente ha un certo score e suggerire remediation.

---

# 5. API ENDPOINTS (26 totali)

| Gruppo | Endpoint | Metodo | Descrizione |
|--------|----------|--------|-------------|
| Auth | `/api/auth/login` | POST | JWT login |
| Auth | `/api/auth/register` | POST | Registrazione |
| Agents | `/api/agents` | GET/POST | CRUD agenti |
| Policies | `/api/policies` | GET/POST | CRUD policy |
| Audit | `/api/audit` | GET | Audit trail |
| Audit | `/api/audit/export/pdf` | GET | Export PDF |
| Audit | `/api/audit/export/csv` | GET | Export CSV |
| Compliance | `/api/compliance` | GET | Standard |
| Compliance | `/api/compliance/export/pdf` | GET | Export PDF |
| Dashboard | `/api/dashboard/stats` | GET | KPI |
| Chat | `/api/chat` | POST | ARIA |
| Chat | `/api/chat/stream` | GET | SSE streaming |
| SOX | `/api/sox/controls` | GET | Controlli SOX |
| SOX | `/api/sox/controls/{id}` | PATCH | Aggiorna controllo |
| SOX | `/api/sox/report` | GET | Report JSON |
| SOX | `/api/sox/report/pdf` | GET | Report PDF |
| SOX | `/api/sox/readiness-score` | GET | Readiness Score |
| Score | `/api/score/overview` | GET | Governance score + explainability |
| Score | `/api/score/agents` | GET | Score tutti gli agenti |
| Score | `/api/score/agents/{id}` | GET | Score singolo agente |
| Score | `/api/score/standards` | GET | Score standard |
| Score | `/api/score/history` | GET | Storico snapshot |
| Score | `/api/score/insights` | GET | Insight strutturati |
| Policy Engine | `/api/policy-engine/conflicts` | GET | Detect conflitti |
| Policy Engine | `/api/policy-engine/conflicts/{id}/resolve` | POST | Risolvi |
| Policy Engine | `/api/policy-engine/conflicts/{id}/guidance` | GET | Guidance |

---

# 6. PERCHE USARE GOVERN.AI

| Stakeholder | Valore |
|-------------|--------|
| **DPO** | Visibilita totale, mapping normativo, report PDF, score oggettivo |
| **CISO** | Risk classification, policy enforcement, Audit Readiness Score |
| **CTO** | API REST documentata, 15 modelli Pydantic, Docker, 50 test |
| **CEO/Board** | Dashboard executive, Governance Score, Intelligence Center |

---

# 7. DEPLOYMENT

```bash
git clone https://github.com/AngeloAng94/GOVERN.AI
cd GOVERN.AI
cp .env.example backend/.env
docker-compose up --build
# Access: http://localhost:3000
```

---

# 8. ROADMAP

**Completato (MVP v3.0):** Core platform, JWT/RBAC, ARIA SSE, Export PDF/CSV, 8 standard, SOX 404 Wizard + Readiness Score, D.Lgs. 262/2005, Policy Conflict Engine + Guidance, Compliance Intelligence Engine + Explainability + Intelligence Center + Score History, Docker + CI/CD, 50 test.

**Prossimi sviluppi:** Multi-tenancy, connettori enterprise, D.Lgs. 262 Wizard, WebSocket monitoring, test frontend.

---

## Contatti

**Angelo Anglani** — Founder, GOVERN.AI  
angelo.anglani94@gmail.com | +39 342 754 8655  
linkedin.com/in/angelo-anglani

---

*GOVERN.AI — Sovereign Control Plane for Enterprise AI*  
*powered by ANTHERA Systems*

**Documento generato**: 14 Maggio 2026 — Versione 3.0
