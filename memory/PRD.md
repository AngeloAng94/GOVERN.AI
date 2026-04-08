# GOVERN.AI - PRD (Product Requirements Document)

## Versione: MVP v3.0
## Data ultimo aggiornamento: 08 Aprile 2026

---

## 1. Problema Originale

Piattaforma SaaS per la governance di agenti AI enterprise con motore di compliance intelligence proprietario.

## 2. Target Users

- DPO / Compliance Manager, CISO, CTO / Engineering, CEO / Board

## 3. Core Requirements — IMPLEMENTATI

### 3.1 Compliance Intelligence Engine (v3.0)
- Motore deterministico di scoring: agent scores, standard scores, overall governance score
- Score breakdown con positive/negative drivers
- Explainability layer con spiegazioni strutturate e methodology notes
- Integration con Policy Conflict Engine: conflitti impattano lo score
- Score History & Momentum: snapshot, delta, trend direction
- Priority remediations con impact scoring
- Top risks, missing controls, insights strutturati
- 6 API endpoints: /api/score/overview, /agents, /agents/{id}, /standards, /history, /insights

### 3.2 Intelligence Center (frontend v3.0)
- Score ring (RadialBarChart) con badge banda
- Score Composition con mini KPI cards
- Agent Distribution pie chart
- Agent Ranking (dal piu basso) con progress bar
- Standard Scores con cards per ogni normativa
- Active Insights con severity badges
- Priority Remediations con impact bar
- Top Risks grid
- Missing Controls list
- Delta/Trend indicators

### 3.3 Previous Features (v1.0-v2.5)
- Agent Registry (14 agenti), Policy Engine (20+ policy), Audit Trail (150+ log)
- 8 compliance standards, SOX 404 Wizard + Readiness Score
- Policy Conflict Engine + Guidance Engine
- D.Lgs. 262/2005, ARIA AI Assistant (SSE streaming)
- JWT + RBAC (4 ruoli), Export PDF/CSV, i18n IT/EN
- Docker + CI/CD, 50/50 test backend

## 4. Scoring Formula

**Agent Score (0-100):**
- Base: risk_level (critical=25, high=45, medium=65, low=82)
- Policy coverage: +15 max (con policy) / -20 (senza policy)
- Audit outcome: +/-15 (ratio allowed/total)
- Conflict penalty: critical=-18, high=-10, medium=-5, low=-2
- Status: active=0, suspended=-10, inactive=-20

**Standard Score (0-100):**
- Base: progress %
- Requirements bonus: delta req_ratio vs progress
- Policy coverage: +12 max / -8
- Conflict penalty per regulation

**Overall: standards 55% + agents 45% - global critical penalty**

## 5. Backlog

- P2: Multi-tenancy, Connettori Enterprise, WebSocket monitoring
- P2: D.Lgs. 262 Wizard, Test unitari frontend

## 6. Credenziali Test
- Username: `admin` / Password: `AdminGovern2026!`

## 7. Changelog
- **v3.0 (08/04/2026)**: Compliance Intelligence Engine, Explainability, Intelligence Center, ARIA upgrade, Overview KPI, 11 nuovi test (50/50)
- **v2.5**: Policy Guidance Engine
- **v2.4**: Policy Conflict Detection Engine
- **v2.3**: D.Lgs. 262/2005 + Audit Readiness Score
- **v2.2**: SOX Section 404 Wizard
