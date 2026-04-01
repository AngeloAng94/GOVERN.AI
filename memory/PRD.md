# GOVERN.AI - PRD (Product Requirements Document)

## Company Context (dal Business Plan 2026-2029 v2.0)
- **Azienda**: ANTHERA Systems — Software house italiana, "Empowering Intelligent Systems"
- **Founder**: Angelo Anglani — Founder & Lead Engineer
- **Prodotto**: GOVERN.AI — "The Sovereign AI Control Plane for Regulated Enterprises"
- **Missione**: Trasformare la compliance normativa da freno burocratico ad abilitatore di innovazione
- **Secondo prodotto ANTHERA**: PowerLeave (gestione ferie/permessi, stesso stack)

## Market Context
- **TAM**: $5.78B entro 2029 (MarketsandMarkets, CAGR 45.3%)
- **SAM** (EU settori regolamentati): ~$1.7B entro 2029
- **SOM** (3 anni, IT/FR/DE): ~€17M ARR
- **Catalizzatore critico**: EU AI Act in vigore 2 agosto 2026 — sanzioni fino a €35M o 7% fatturato globale
- **Convergenza normativa**: AI Act + DORA + NIS2 creano matrice di requisiti unica

## Revenue Model (SaaS B2B Tiered)
| Piano | Target | Agenti | Prezzo/anno | Caratteristiche |
|---|---|---|---|---|
| Pro | Team/PMI | ≤10 | €12,000 | Registry, Policy base, Audit, 2 standard |
| Business | Medie imprese | ≤50 | €48,000 | + RBAC, Dashboard avanzate, 6 standard, AI Assistant, Export |
| Enterprise | Grandi aziende/PA | Illimitati | €100,000+ | + SLA, Connettori SIEM/IAM/ServiceNow, Multi-tenant |

- **ACV medio**: €48,000 | **LTV/CAC**: 12.8x | **Gross Margin**: 85% | **Churn**: 5%/anno
- **Target**: Break-even Q2 2027, ARR €3.6M fine 2028 (75 clienti)
- **Seed round**: €1.5M (40% sviluppo, 35% sales/marketing, 15% GRC, 10% riserva)

## Segmenti Target con ACV
| Segmento | Dimensione | Driver | ACV |
|---|---|---|---|
| Banche & Finanza | Fatturato >€1B | AI Act + DORA + NIS2 | €80-120K |
| Assicurazioni | Fatturato >€500M | AI Act + GDPR + DORA | €60-100K |
| Pubblica Amministrazione | Enti centrali/regionali | AI Act + GDPR + trasparenza | €40-80K |
| Sanita | Ospedali e ASL | AI Act + GDPR + ISO 27001 | €30-60K |
| Energia & Utility | Fatturato >€500M | NIS2 + AI Act | €50-80K |

## User Personas
- **CTO/CISO**: Panoramica landscape agenti AI e postura di rischio
- **DPO**: Conformita GDPR e governance dei dati
- **Compliance Officer**: Tracciamento standard regolatori (AI Act, ISO, DORA, NIS2)
- **IT Administrator**: Ciclo di vita agenti e enforcement policy

## Architecture (Current — MVP v2.3)
- **Frontend**: React 19 + Tailwind 3.4 + Shadcn/UI + Recharts (port 3000)
- **Backend**: FastAPI 0.110 + Pydantic V2 + modular routes + reportlab (port 8001)
- **Database**: MongoDB + Motor async (15 indici, 6 collections)
- **LLM**: OpenAI GPT-4o via litellm (ARIA assistant, dual-mode Emergent/OpenAI)
- **Auth**: JWT + RBAC (4 ruoli: admin, dpo, auditor, viewer)
- **Process Manager**: Supervisord (dev), Docker Compose (prod)
- **Tipo**: Architettura modulare a due tier

## 6 Moduli Funzionali
1. **Agent Registry**: Catalogazione agenti con profilo completo (risk level, status, azioni, domini ristretti)
2. **Policy Engine**: 5 tipi (restriction, approval, rate_limit, logging, retention) × 6 normative × 4 enforcement
3. **Audit Trail**: Tracciabilita immutabile con search sanitizzata e filtri
4. **Compliance Dashboard**: 8 standard (AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2, SOX, D.Lgs. 262)
5. **AI Compliance Assistant**: GPT-5.2 con memoria conversazionale
6. **Interfaccia bilingue**: IT/EN nativa

## What's Been Implemented

### MVP v1.0 (18 Feb 2026)
- [x] Landing page completa (hero, features bento, clients, CTA, footer)
- [x] Dashboard con sidebar e navigazione 6 sezioni
- [x] KPI dashboard con dati real-time da MongoDB
- [x] CRUD Agents con risk/status management
- [x] CRUD Policies con mapping 6 normative
- [x] Audit Trail con ricerca/filtri
- [x] Compliance Monitor per 6 standard
- [x] AI Compliance Assistant GPT-5.2 (reale)
- [x] Toggle bilingue EN/IT
- [x] Auto audit log per ogni operazione CRUD
- [x] Seed data demo (4 agenti, 5 policy, 25 log, 6 standard)
- [x] Test suite 25/25 passati

### Step 1 Fixes (26 Feb 2026) — v1.1
- [x] 15 indici MongoDB (5 unique, 10 filtro)
- [x] Sanitizzazione regex (re.escape)
- [x] CORS restrittivo (ALLOWED_ORIGINS da env)
- [x] Chat history passata al LLM (initial_messages)
- [x] 7 Enum Pydantic tipizzati
- [x] Debounce search 300ms
- [x] Import inutilizzati rimossi
- [x] Migrazione lifespan (asynccontextmanager)
- [x] Errori LLM mascherati

### Step 2A (02 Mar 2026) — v1.2
- [x] Autenticazione JWT completa + RBAC (4 ruoli)
- [x] ARIA AI Assistant verticale con system prompt restrittivo
- [x] Rate limiting su tutti gli endpoint (slowapi)

### Step 2B (02 Mar 2026) — v1.3
- [x] Backend modulare: models.py, database.py, seed.py, 7 file route
- [x] Header di sicurezza (X-Frame-Options, CSP, etc.)
- [x] Componente CRUD generico (CrudPage.js)
- [x] Traduzioni JSON esterne (locales/)
- [x] react-markdown per chat ARIA
- [x] Test backend aggiornati (22/22)

### Step C1 (24 Mar 2026) — v1.4
- [x] Dashboard Charts con Recharts (3 grafici: PieChart risk, BarChart audit, BarChart compliance)
- [x] Enterprise Seed Data (12 agenti, 15 policy, 150+ audit log, 5 incident cluster)
- [x] Compliance progress realistici (GDPR 78%, EU AI Act 45%, ISO 27001 92%, etc.)

### Step C2 (24 Mar 2026) — v1.5
- [x] Export Audit Trail CSV (UTF-8 BOM, filtri supportati)
- [x] Export Audit Trail PDF (reportlab, header GOVERN.AI, Executive Summary)
- [x] Export Compliance Report PDF (progress bars, status badges)
- [x] Bottoni export UI con RBAC (solo admin/dpo/auditor)
- [x] Rate limiting su endpoint export

### Step C3A (24 Mar 2026) — v1.6
- [x] Logo ufficiale GOVERN.AI powered by ANTHERA integrato
- [x] Componente Logo.js riutilizzabile (size, variant, tagline)
- [x] Mobile sidebar con hamburger menu e drawer overlay
- [x] Desktop sidebar collapsabile (solo icone)
- [x] Favicon e meta tags aggiornati

### Step C3B (24 Mar 2026) — v1.7
- [x] Dockerfile backend (Python 3.11-slim + uvicorn)
- [x] Dockerfile frontend (multi-stage: node + nginx)
- [x] docker-compose.yml (mongodb, backend, frontend)
- [x] nginx.conf per SPA routing + API proxy
- [x] .env.example + .dockerignore
- [x] README.md professionale completo

### Documentazione (24 Mar 2026) — v1.7.1
- [x] GOVERN_AI_TECHNICAL_OVERVIEW.md (670 righe, architettura completa)
- [x] Presentazione HTML interattiva (12 slide navigabili con animazioni)
- [x] PDF Technical Overview professionale (ReportLab, 10+ pagine)
- [x] Endpoint API /api/docs/technical-overview-pdf per download PDF
- [x] Documenti per investitori (IT/EN, PDF)
- [x] Audit tecnico aggiornato (PDF)

### Step CICD (24 Mar 2026) — v1.8
- [x] `.github/workflows/ci.yml` — Pipeline GitHub Actions con 4 job paralleli
- [x] Job `backend-tests`: pytest 22/22 con MongoDB service container
- [x] Job `frontend-build`: yarn build check
- [x] Job `security-scan`: bandit + safety su dipendenze Python
- [x] Job `docker-build`: build immagini Docker backend + frontend
- [x] YAML validato (zero tab, sintassi corretta)
- [x] README.md aggiornato con badge CI, sezione CI/CD, istruzioni secrets
- [x] AUDIT_TECNICO_GOVERN.md aggiornato (TD18 risolto, v1.8)
- [x] STEP_CICD_REPORT.md generato

### Step FINAL (30 Mar 2026) — v1.9
- [x] FIX 1: Landing Page Use Cases reali (3 card: Banking, Healthcare, Legal)
- [x] FIX 2: Landing Page Social Proof (4 stat)
- [x] FIX 3: SSE Streaming per ARIA (GET /api/chat/stream + EventSource frontend)
- [x] FIX 4: Titoli pagina dinamici (PageTitleUpdater in App.js)
- [x] FIX 5: Empty states professionali (EmptyState.js + integrazione 4 pagine)
- [x] FIX 6: Loading skeleton (SkeletonLoader.js + integrazione 5 pagine)
- [x] i18n: 38 nuove chiavi in en.json + it.json
- [x] AUDIT_TECNICO_GOVERN.md aggiornato (v1.9)
- [x] STEP_FINAL_REPORT.md generato

### Fix v2.0 (30 Mar 2026) — v2.0
- [x] Bar chart "Audit Outcomes" corretto — usa stats.audit reali
- [x] Delete confirmation dialog — CrudPage.js con dialog di conferma
- [x] AUDIT_TECNICO_GOVERN.md aggiornato (v2.0)
- [x] STEP_FIX_V2_REPORT.md generato

### Step E1 — SOX Foundation (01 Apr 2026) — v2.1
- [x] SOX compliance standard aggiunto al seed (code: SOX, progress: 56%, 25/44 requisiti)
- [x] Agente "SOX Internal Control Auditor" (high risk, 4 azioni, restricted domains)
- [x] 3 policy SOX: Financial Reporting Integrity, Internal Control Testing, CEO/CFO Certification Workflow
- [x] Cluster audit log SOX (5 eventi: control verification, effectiveness testing, deficiency flagging, sox report)
- [x] PoliciesPage: "SOX" aggiunto al dropdown regulation
- [x] OverviewPage: conteggio standard dinamico (da "6 standards" hardcoded a `${compliance.length} standards`)
- [x] LandingPage: "7" Regulations Covered (hero stats e social proof)
- [x] ARIA system prompt: SOX (Sarbanes-Oxley Act, 2002) aggiunto ai domini di competenza
- [x] AssistantPage: placeholder aggiornato con SOX
- [x] i18n: feat_compliance_desc e empty_assistant_subtitle aggiornati (en.json + it.json)
- [x] exporters.py: nota legale aggiornata con SOX Section 802
- [x] 2 nuovi test pytest (test_sox_standard_present, test_seven_compliance_standards)
- [x] 24/24 test backend passano
- [x] Testing agent: 100% pass rate frontend + backend

### Step E2 — SOX Section 404 Wizard (01 Apr 2026) — v2.2
- [x] Backend: ControlStatus enum + SoxControl model in models.py
- [x] Backend: routes/sox_wizard.py — 4 endpoint (GET /sox/controls, PATCH /sox/controls/{id}, GET /sox/report, GET /sox/report/pdf)
- [x] Backend: seed.py — 20 controlli SOX realistici in 5 domini (5 completed, 9 in_progress, 4 not_started, 2 failed)
- [x] Backend: exporters.py — SoxReportPDFBuilder per report PDF Section 404
- [x] Backend: server.py — sox_router registrato
- [x] Backend: ARIA prompt aggiornato con riferimento al SOX 404 Wizard
- [x] Frontend: SoxWizardPage.js — pagina completa con progress bar, domain cards, accordion controlli, edit dialog, auditor summary
- [x] Frontend: App.js — route /dashboard/sox-wizard
- [x] Frontend: DashboardLayout.js — voce SOX 404 in sidebar con icona ClipboardCheck
- [x] Frontend: locales en.json + it.json — 24 chiavi sox_* aggiunte
- [x] Backend: 4 nuovi test pytest (get_sox_controls, patch_sox_control, sox_report_json, sox_report_pdf)
- [x] 28/28 test backend passano
- [x] Testing agent: 100% pass rate frontend + backend

### Step E3 — D.Lgs. 262 + Audit Readiness Score (01 Apr 2026) — v2.3
- [x] D.Lgs. 262/2005 come 8o standard di compliance (code: DLgs262, progress: 48%, 13/28)
- [x] 2 policy DLgs262: Attestazione Dirigente Preposto (critical), Procedure Amministrativo-Contabili (high)
- [x] Agente "Dirigente Preposto Assistant" (high risk, CFO Office)
- [x] 8 audit log DLgs262 nel cluster 7 (evidence_collection, attestation_draft, procedure_verification, 262_report)
- [x] GET /api/sox/readiness-score: score pesato per rischio, top 5 priority controls, domain_scores
- [x] Frontend: Audit Readiness Score card con score circolare, badge, gap, priority controls con +pts
- [x] PoliciesPage: DLgs262 nel dropdown, LandingPage: "8 regulations", locales aggiornati
- [x] ARIA prompt aggiornato con D.Lgs. 262/2005 e art. 154-bis
- [x] 2 nuovi test pytest (readiness_score, eight_compliance_standards)
- [x] 30/30 test backend passano
- [x] Testing agent: 100% pass rate frontend + backend

## Roadmap Tecnica (dal Business Plan)

### Phase 1 — Foundation (Q2 2026, 3 mesi)
- [x] JWT + RBAC (Admin, DPO, Auditor, Viewer) ✅ Step 2A
- [x] Split backend monolite → moduli (models/, routes/, services/) ✅ Step 2B
- [x] Rate limiting (slowapi) su endpoint critici ✅ Step 2A
- [x] Header di sicurezza (CSP, X-Frame-Options, HSTS) ✅ Step 2B
- [ ] WebSocket monitoraggio real-time

### Phase 2 — Intelligence (Q3-Q4 2026, 6 mesi)
- [x] Dashboard visualizzazioni avanzate (Recharts) ✅ Step C1
- [x] Export report PDF/CSV ✅ Step C2
- [ ] Motore rilevamento conflitti policy
- [ ] Algoritmo scoring automatico compliance
- [ ] Timeline attivita agenti
- [ ] Streaming SSE per chat LLM

### Phase 3 — Integration (Q1-Q2 2027, 6 mesi)
- [ ] Connettori SIEM (Splunk, ELK)
- [ ] Connettori IAM (Okta, Azure AD)
- [ ] Connettore ServiceNow/CMDB
- [ ] Multi-tenant
- [ ] API key management per registrazione agenti esterna
- [ ] Sistema notifiche (email alerts su violazioni policy)
- [ ] Custom compliance framework builder

### Evoluzione Architetturale Target (Enterprise)
| Componente | MVP v1.1 | Target Enterprise |
|---|---|---|
| Policy Engine | CRUD MongoDB | OPA/Rego |
| Intercettazione | API manuale | Envoy Proxy / Istio |
| Identita Agenti | UUID stringhe | SPIFFE/SPIRE |
| Audit Trail | MongoDB standard | Immutable Ledger (QLDB/Hyperledger) |
| Scalabilita | Monolite Supervisord | Microservizi Kubernetes |
| Autenticazione | Assente | JWT + RBAC + SSO (Okta/Azure AD) |

### Certificazioni Pianificate
| Certificazione | Target | Costo stimato |
|---|---|---|
| ISO 27001 | Q3 2026 | €30-50K |
| ISO 42001 | Q4 2026 | €20-40K |
| SOC2 Type II | Q1 2027 | €40-60K |
| EU AI Act Compliance Seal | Q2 2027 | TBD |

## Competitive Landscape
| Competitor | Sede | Funding | Focus | Agent Governance |
|---|---|---|---|---|
| Credo AI | US | $39.3M | Risk mgmt, model cards | Parziale |
| Holistic AI | UK/US | $5M | Bias auditing, etica | No |
| IBM Watsonx.gov | US | Corporate | Model lifecycle | No |
| OneTrust | US | $920M+ | Privacy, consent | No |
| Airia | US | N/D | Agent constraints | Si |
| Enkrypt AI | US | N/D | AI security, policy LLM | Si |
| **GOVERN.AI** | **Italia** | **Pre-seed** | **Agent governance + compliance EU** | **Si (8 standard)** |

## Dipendenze Strategiche gia presenti
- PyJWT 2.11.0 + bcrypt 4.1.3 → pronti per autenticazione
- Stripe 14.3.0 → pronto per billing
- websockets 15.0.1 → pronto per real-time monitoring
- Recharts 3.6.0 → pronto per dashboard avanzate

## Next Tasks
1. P2: Policy Conflict Detection
2. P2: Algoritmo scoring automatico compliance
3. P2: Multi-tenancy
4. P2: Connettori Enterprise (SIEM, IAM, ServiceNow)
5. P2: WebSocket real-time monitoring
6. P2: Sistema notifiche (email alerts)
7. P2: Test unitari frontend (Jest + Testing Library)
