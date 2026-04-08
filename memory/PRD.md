# GOVERN.AI - PRD (Product Requirements Document)

## Versione: MVP v2.5
## Data ultimo aggiornamento: 08 Aprile 2026

---

## 1. Problema Originale

Piattaforma SaaS per la governance di agenti AI enterprise. Copre il ciclo di vita completo della governance: registrazione agenti, definizione policy, rilevamento conflitti con guidance operativa, audit trail, compliance monitoring, SOX 404 Wizard, e assistente AI.

## 2. Target Users

- **DPO / Compliance Manager**: Visibilita e controllo sugli agenti AI
- **CISO**: Classificazione rischio e policy enforcement
- **CTO / Engineering**: API REST, architettura modulare, Docker ready
- **CEO / Board**: Dashboard executive, riduzione rischio sanzioni

## 3. Core Requirements — IMPLEMENTATI

### 3.1 Agent Registry
- CRUD completo per agenti AI, risk classification, status management
- 14 agenti demo enterprise banking

### 3.2 Policy Engine + Conflict Detection + Guidance (v2.4-2.5)
- CRUD policy con 8 normative, 5 rule types, 4 enforcement levels
- Policy Conflict Detection Engine con 4 tipi: action_conflict, gap, overlap, redundancy
- **Policy Guidance Engine** (v2.5): guidance operativa, impact analysis, risoluzione documentata con audit trail
- IDs conflitto deterministici (SHA-256)
- ConflictResolution model con notes obbligatorie (min 10 char)
- Endpoint guidance dedicato per singolo conflitto

### 3.3 SOX Section 404 Wizard
- 20 controlli in 5 domini, Audit Readiness Score pesato per rischio

### 3.4 Audit Trail
- 150+ log demo, filtri multipli, export PDF/CSV

### 3.5 Compliance Dashboard
- 8 standard: EU AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2, SOX, D.Lgs. 262/2005

### 3.6 ARIA AI Assistant
- SSE streaming, memoria conversazionale, system prompt verticale

### 3.7 Auth + RBAC
- JWT HS256, 4 ruoli: admin > dpo > auditor > viewer

### 3.8 DevOps
- Docker + Docker Compose, CI/CD GitHub Actions (4 job), 39/39 test backend

## 4. Backlog — NON IMPLEMENTATO

### P2 Features
1. Multi-tenancy
2. Connettori Enterprise (ServiceNow, SIEM, IAM)
3. Real-time Monitoring via WebSocket
4. D.Lgs. 262 Wizard dedicato
5. Test unitari frontend (Jest + Testing Library)

## 5. Credenziali Test
- Username: `admin`
- Password: `AdminGovern2026!`

## 6. Changelog Recente
- **v2.5 (08/04/2026)**: Policy Guidance Engine — guidance, impact, risoluzione documentata, 5 nuovi test (39/39)
- **v2.4 (01/04/2026)**: Policy Conflict Detection Engine
- **v2.3**: D.Lgs. 262/2005 + Audit Readiness Score
- **v2.2**: SOX Section 404 Wizard
- **v2.1**: SOX Foundation
