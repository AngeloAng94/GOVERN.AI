# GOVERN.AI - PRD (Product Requirements Document)

## Versione: MVP v3.0
## Data ultimo aggiornamento: 14 Maggio 2026

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
- **v3.0 (14/05/2026)**: Documentazione completa aggiornata - Investor Intro IT/EN, Audit Tecnico, Technical Overview, INVESTOR_INTRO + **nuovo Manuale Operativo Completo IT/EN** (Guida Utente + Implementazione + Deploy). Tutti i 6 PDF rigenerati con metadata v3.0 / 14 Maggio 2026.
- **v3.0 (08/04/2026)**: Compliance Intelligence Engine, Explainability, Intelligence Center, ARIA upgrade, Overview KPI, 11 nuovi test (50/50)
- **v2.5**: Policy Guidance Engine
- **v2.4**: Policy Conflict Detection Engine
- **v2.3**: D.Lgs. 262/2005 + Audit Readiness Score
- **v2.2**: SOX Section 404 Wizard

## 8. Documentazione Disponibile

| Documento | Markdown | PDF | Lingua |
|-----------|----------|-----|--------|
| Investor Intro | GOVERN_AI_Investor_Intro_IT.md | GOVERN_AI_Investor_Intro_IT.pdf | IT |
| Investor Intro | GOVERN_AI_Investor_Intro_EN.md | GOVERN_AI_Investor_Intro_EN.pdf | EN |
| Investor Intro (one-pager) | INVESTOR_INTRO.md | - | EN |
| Audit Tecnico | AUDIT_TECNICO_GOVERN.md | AUDIT_TECNICO_GOVERN.pdf | IT |
| Technical Overview | GOVERN_AI_TECHNICAL_OVERVIEW.md | GOVERN_AI_Technical_Overview.pdf | IT |
| **Manuale Operativo (NEW v3.0)** | GOVERN_AI_USER_MANUAL_IT.md | GOVERN_AI_USER_MANUAL_IT.pdf | IT |
| **Manuale Operativo (NEW v3.0)** | GOVERN_AI_USER_MANUAL_EN.md | GOVERN_AI_USER_MANUAL_EN.pdf | EN |
| README | README.md | - | EN |

---

## Hardening Sprint (2026-07-08) — Prompt 1.1 / 1.2 / 1.3

**1.1 Docker/Mongo hardening**
- backend/Dockerfile: utente non-root (appuser), USER prima del CMD, HEALTHCHECK (/health), curl installato
- backend/.dockerignore creato
- frontend/Dockerfile: HEALTHCHECK nginx (wget)
- docker-compose.yml: auth MongoDB, connection string autenticata, no source volume mount, resource limits, rimossa chiave version
- backend/database.py: MONGO_URL via os.environ.get + RuntimeError

**1.2 Pydantic + indici**
- models.py: ComplianceUpdate, SoxControlUpdate (pattern SOX allineato all'enum reale: not_started|in_progress|completed|failed|not_applicable)
- routes/compliance.py, routes/sox_wizard.py: data: <Model> + model_dump(exclude_none=True)
- database.py: 7 indici aggiunti (sox_controls, conflict_scans, resolved_conflicts, score_history)

**Trasparenza test LLM**
- pytest.ini (-ra --strict-markers, marker llm/sovereign), conftest.py (banner LLM COVERAGE WARNING su skip)
- test_api.py: TestChat marcato llm; nuova TestSovereignMode (skip visibile se manca PUBLICAI_API_KEY); TestSoxWizard reso robusto (token cache)

**1.3 Igiene repo**
- Rimossa password admin hardcoded da README, manuali IT/EN, STEP2A_REPORT, generate_overview_pdf.py, backend_test.py
- seed_admin: ADMIN_PASSWORD da env, altrimenti password random (secrets) stampata una sola volta al primo boot
- backend/.env: aggiunti ADMIN_PASSWORD, APP_VERSION
- Endpoint GET /api/health e /health (status DB, llm_provider, version — nessun dato sensibile)
- Frontend: banner persistente "DEMO DATA" in DashboardLayout (i18n it/en), data-testid demo-data-banner

Test: 50 passed, 1 skipped (Sovereign, no key), 0 failed.
