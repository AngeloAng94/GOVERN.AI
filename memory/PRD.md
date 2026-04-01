# GOVERN.AI - PRD (Product Requirements Document)

## Versione: MVP v2.4
## Data ultimo aggiornamento: 01 Aprile 2026

---

## 1. Problema Originale

L'utente vuole creare GOVERN.AI, una piattaforma SaaS per la governance di agenti AI enterprise. La piattaforma deve coprire l'intero ciclo di vita della governance: registrazione agenti, definizione policy, audit trail, compliance monitoring, assistente AI, e funzionalita enterprise come SOX 404 Wizard e Policy Conflict Detection.

## 2. Target Users

- **DPO / Compliance Manager**: Visibilita e controllo sugli agenti AI
- **CISO**: Classificazione rischio e policy enforcement
- **CTO / Engineering**: API REST, architettura modulare, Docker ready
- **CEO / Board**: Dashboard executive, riduzione rischio sanzioni

## 3. Core Requirements — IMPLEMENTATI

### 3.1 Agent Registry
- CRUD completo per agenti AI
- Risk classification (low/medium/high/critical)
- Status management (active/suspended/inactive)
- 14 agenti demo enterprise banking

### 3.2 Policy Engine + Conflict Detection
- CRUD policy con 8 normative
- 5 rule types, 4 enforcement levels
- **Policy Conflict Detection Engine** con 4 tipi: action_conflict, gap, overlap, redundancy
- UI dedicata con summary cards, filtri, resolve dialog

### 3.3 SOX Section 404 Wizard
- 20 controlli in 5 domini
- Status tracking con progress bar per dominio
- Edit dialog per aggiornare status/evidence
- Export report PDF
- **Audit Readiness Score** pesato per rischio

### 3.4 Audit Trail
- 150+ log demo con 7 incident cluster
- Filtri multipli (outcome, risk, agent, search)
- Export PDF branded + CSV

### 3.5 Compliance Dashboard
- 8 standard: EU AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2, SOX, D.Lgs. 262/2005
- Progress tracking con percentuali
- Export report PDF

### 3.6 ARIA AI Assistant
- SSE streaming (risposta in tempo reale)
- Memoria conversazionale (session_id)
- System prompt verticale su 8 normative
- Rate limited

### 3.7 Auth + RBAC
- JWT HS256 con 8h expiry
- 4 ruoli: admin > dpo > auditor > viewer
- bcrypt password hashing

### 3.8 Analytics Dashboard
- 3 grafici Recharts (risk distribution, audit outcome, compliance progress)
- 5 KPI cards (agents, policies, audit events, compliance, conflicts)

### 3.9 Export & Reporting
- PDF branded con ReportLab (Audit, Compliance, SOX)
- CSV con UTF-8 BOM

### 3.10 i18n
- Bilingue IT/EN con 130+ chiavi per lingua
- Switch lingua in sidebar

### 3.11 DevOps
- Docker + Docker Compose (3 container)
- CI/CD GitHub Actions (4 job)
- 34/34 test backend (pytest)

### 3.12 Documentazione (Aprile 2026)
- README.md completo per v2.4
- AUDIT_TECNICO_GOVERN.md aggiornato
- Technical Overview (MD + PDF)
- Investor Intro EN/IT (MD + PDF)
- .env.example aggiornato

## 4. Architettura

```
Backend: FastAPI + Motor (MongoDB async) + litellm + ReportLab
Frontend: React 19 + Tailwind + Shadcn UI + Recharts + Axios
Database: MongoDB 7.0, 7 collections, 15+ indici
Auth: JWT HS256 + bcrypt + RBAC
DevOps: Docker Compose, GitHub Actions CI
```

## 5. Backlog — NON IMPLEMENTATO

### P2 Features
1. Multi-tenancy (supporto tenant isolati)
2. Connettori Enterprise (ServiceNow, SIEM, IAM)
3. Real-time Monitoring via WebSocket
4. D.Lgs. 262 Wizard (workflow dedicato)
5. Auto-Fix Engine (risoluzione automatica conflitti policy)
6. Test unitari frontend (Jest + Testing Library)

## 6. Credenziali Test
- Username: `admin`
- Password: `AdminGovern2026!`

## 7. File di Riferimento Principali
- `/app/backend/server.py` — Entry point FastAPI
- `/app/backend/models.py` — 14 modelli Pydantic
- `/app/backend/routes/` — 9 file route modulari
- `/app/frontend/src/pages/` — 11 pagine
- `/app/backend/tests/test_api.py` — 34 test
