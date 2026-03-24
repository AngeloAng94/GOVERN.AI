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

## Architecture (Current — MVP v1.4)
- **Frontend**: React 19 + Tailwind 3.4 + Shadcn/UI + Recharts (port 3000)
- **Backend**: FastAPI 0.110 + Pydantic V2 + modular routes (port 8001)
- **Database**: MongoDB + Motor async (15 indici, 6 collections)
- **LLM**: OpenAI GPT-5.2 via Emergent LLM key (ARIA assistant)
- **Auth**: JWT + RBAC (4 ruoli: admin, dpo, auditor, viewer)
- **Process Manager**: Supervisord
- **Tipo**: Architettura modulare a due tier

## 6 Moduli Funzionali
1. **Agent Registry**: Catalogazione agenti con profilo completo (risk level, status, azioni, domini ristretti)
2. **Policy Engine**: 5 tipi (restriction, approval, rate_limit, logging, retention) × 6 normative × 4 enforcement
3. **Audit Trail**: Tracciabilita immutabile con search sanitizzata e filtri
4. **Compliance Dashboard**: 6 standard EU (AI Act, GDPR, ISO 27001, ISO 42001, DORA, NIS2)
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

## Roadmap Tecnica (dal Business Plan)

### Phase 1 — Foundation (Q2 2026, 3 mesi)
- [x] JWT + RBAC (Admin, DPO, Auditor, Viewer) ✅ Step 2A
- [x] Split backend monolite → moduli (models/, routes/, services/) ✅ Step 2B
- [x] Rate limiting (slowapi) su endpoint critici ✅ Step 2A
- [x] Header di sicurezza (CSP, X-Frame-Options, HSTS) ✅ Step 2B
- [ ] WebSocket monitoraggio real-time

### Phase 2 — Intelligence (Q3-Q4 2026, 6 mesi)
- [x] Dashboard visualizzazioni avanzate (Recharts) ✅ Step C1
- [ ] Motore rilevamento conflitti policy
- [ ] Algoritmo scoring automatico compliance
- [ ] Export report PDF/CSV
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
| **GOVERN.AI** | **Italia** | **Pre-seed** | **Agent governance + compliance EU** | **Si (6 standard)** |

## Dipendenze Strategiche gia presenti
- PyJWT 2.11.0 + bcrypt 4.1.3 → pronti per autenticazione
- Stripe 14.3.0 → pronto per billing
- websockets 15.0.1 → pronto per real-time monitoring
- Recharts 3.6.0 → pronto per dashboard avanzate

## Next Tasks
1. Phase 1 Foundation: JWT + RBAC (P0)
2. Phase 1 Foundation: Split monolite backend
3. Phase 1 Foundation: Rate limiting + security headers
4. Loghi ANTHERA + GOVERN.AI (richiesta utente — in sospeso)
