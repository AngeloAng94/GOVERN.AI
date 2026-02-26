# AUDIT TECNICO — GOVERN.AI
**Data**: 26 Febbraio 2026 (aggiornato post Step 1)  
**Versione codebase**: MVP v1.1 (Step 1 completato)  
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
                                  │   db: test_db   │
                                  └────────────────┘
                                  
                                  ┌────────────────┐
                                  │  OpenAI GPT-5.2 │
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
| LLM integration | OpenAI GPT-5.2 via `emergentintegrations` | 0.1.0 |
| HTTP client (FE) | Axios | 1.8.4 |
| Routing (FE) | React Router DOM | 7.5.1 |
| Process manager | Supervisord | (sistema) |
| Validazione dati | Pydantic V2 | 2.12.5 |

### 1.3 Tipo di architettura

**Monolite a due tier** con separazione frontend/backend:
- Backend: singolo file `server.py` (491 righe) — monolite funzionale
- Frontend: SPA con routing lato client, 8 pagine
- Database: singola istanza MongoDB, nessun replica set
- Nessun layer di servizi, nessun message broker, nessuna cache

---

## 2. STRUTTURA DEL CODICE

### 2.1 Directory tree (file rilevanti)

```
/app/
├── backend/
│   ├── .env                          # Variabili ambiente (4 chiavi)
│   ├── requirements.txt              # 125 dipendenze (pip freeze completo)
│   └── server.py                     # UNICO file backend — 491 righe
├── frontend/
│   ├── .env                          # REACT_APP_BACKEND_URL
│   ├── package.json                  # 52 dependencies + 12 devDependencies
│   ├── tailwind.config.js            # Config Tailwind + shadcn theme
│   ├── postcss.config.js             # PostCSS standard
│   ├── craco.config.js               # Webpack overrides, alias @/
│   ├── jsconfig.json                 # Path alias
│   ├── components.json               # Shadcn config
│   ├── public/
│   │   └── index.html                # HTML template con font Google
│   └── src/
│       ├── index.js                  # Entry point React — 11 righe
│       ├── index.css                 # CSS globale + CSS vars + animazioni — 163 righe
│       ├── App.js                    # Router principale — 36 righe
│       ├── App.css                   # Vuoto (1 riga commento)
│       ├── contexts/
│       │   └── LanguageContext.js     # i18n EN/IT — 227 righe
│       ├── pages/
│       │   ├── LandingPage.js        # Landing page — 198 righe
│       │   ├── DashboardLayout.js    # Shell con sidebar — 83 righe
│       │   ├── OverviewPage.js       # KPI dashboard — 145 righe
│       │   ├── AgentsPage.js         # CRUD agenti — 235 righe
│       │   ├── PoliciesPage.js       # CRUD policy — 234 righe
│       │   ├── AuditPage.js          # Tabella audit — 148 righe
│       │   ├── CompliancePage.js     # Monitor compliance — 142 righe
│       │   └── AssistantPage.js      # Chat AI — 167 righe
│       ├── components/ui/            # 39 componenti Shadcn (pre-installati)
│       ├── hooks/
│       │   └── use-toast.js          # Hook toast (pre-installato)
│       └── lib/
│           └── utils.js              # cn() utility — 6 righe
├── backend_test.py                   # Test suite API (generato dal testing agent) — 339 righe
├── tests/
│   └── __init__.py                   # Vuoto
├── test_reports/
│   └── iteration_1.json             # Report test automatici
├── memory/
│   └── PRD.md                       # Product Requirements Document
└── design_guidelines.json           # Linee guida UX generate
```

### 2.2 Analisi file principali

| File | Righe | Responsabilita | Note |
|---|---|---|---|
| `backend/server.py` | 491 | Modelli, seed data, TUTTI gli endpoint, startup/shutdown | **Monolite**: modelli, logica, routing, seeding tutto in un file |
| `frontend/src/pages/AgentsPage.js` | 235 | CRUD agenti + form dialog + listing | Componente grande, potrebbe essere splittato |
| `frontend/src/pages/PoliciesPage.js` | 234 | CRUD policy + form dialog + listing | Pattern quasi identico ad AgentsPage (duplicazione logica) |
| `frontend/src/contexts/LanguageContext.js` | 227 | Tutte le traduzioni EN/IT inline | ~200 righe solo di stringhe hardcoded |
| `frontend/src/pages/LandingPage.js` | 198 | Landing completa: nav, hero, features, clients, CTA, footer | Un unico componente per l'intera landing |
| `frontend/src/pages/AssistantPage.js` | 167 | Chat UI + markdown renderer custom | Rendering markdown rudimentale (riga 50-61) |
| `frontend/src/index.css` | 163 | CSS vars, animazioni, scrollbar, glass-morphism | Ben strutturato con @layer |
| `frontend/src/pages/AuditPage.js` | 148 | Tabella audit filtri/ricerca | Buona separazione |
| `frontend/src/pages/CompliancePage.js` | 142 | Monitor compliance con progress bar | Buona separazione |
| `backend_test.py` | 339 | Suite test API completa | Generato dal testing agent, non integrato in CI |

### 2.3 Problemi strutturali identificati

| ID | Problema | File | Impatto |
|---|---|---|---|
| S1 | Backend monolite: modelli, routing, seed, logica in un unico file da 491 righe | `server.py` | Manutenibilita scarsa su lungo termine |
| S2 | Duplicazione pattern CRUD tra AgentsPage e PoliciesPage (~80% struttura identica) | `AgentsPage.js`, `PoliciesPage.js` | Codice duplicato, bug da fixare in 2 posti |
| S3 | Traduzioni inline nel context (227 righe) — non scalabile per aggiunta lingue | `LanguageContext.js` | Difficile aggiungere DE/FR/ES senza esplodere il file |
| S4 | `App.css` praticamente vuoto (1 riga) | `App.css` | File morto, nessun impatto funzionale |

### 2.4 Import inutilizzati

| File | Riga | Import | Usato? |
|---|---|---|---|
| `server.py` | 2 | `StreamingResponse` | **No** — mai usato in nessun endpoint |
| `server.py` | 13 | `asyncio` | **No** — mai usato direttamente |
| `server.py` | 14 | `json` | **No** — mai usato direttamente |
| `OverviewPage.js` | 3 | `Ban` (da lucide-react) | **No** — importato ma mai renderizzato |
| `AuditPage.js` | 3 | `Filter` (da lucide-react) | **No** — importato ma mai renderizzato |
| `AgentsPage.js` | 3 | `X` (da lucide-react) | **No** — importato ma mai renderizzato |

---

## 3. DATABASE & MODELLO DATI

### 3.1 Elenco collections

| Collection | Documenti (attuale) | Campi principali |
|---|---|---|
| `agents` | 5 | `id`, `name`, `description`, `model_type`, `risk_level`, `status`, `allowed_actions[]`, `restricted_domains[]`, `data_classification`, `owner`, `created_at`, `updated_at`, `policy_count`, `last_audit` |
| `policies` | 7 | `id`, `name`, `description`, `agent_id`, `rule_type`, `conditions[]`, `actions[]`, `severity`, `regulation`, `enforcement`, `status`, `created_at`, `updated_at`, `violations_count` |
| `audit_logs` | 41 | `id`, `timestamp`, `agent_id`, `agent_name`, `action`, `resource`, `outcome`, `policy_id`, `policy_name`, `details`, `risk_level`, `ip_address`, `user` |
| `compliance_standards` | 6 | `id`, `name`, `code`, `description`, `status`, `progress`, `requirements_total`, `requirements_met`, `last_assessment`, `next_review`, `category` |
| `chat_messages` | 12 | `id`, `session_id`, `role`, `content`, `timestamp` |

### 3.2 Indici

| Collection | Indici presenti | Indici necessari mancanti |
|---|---|---|
| `agents` | Solo `_id_` (default) | `id` (unique), `status`, `risk_level` |
| `policies` | Solo `_id_` (default) | `id` (unique), `regulation`, `agent_id` |
| `audit_logs` | Solo `_id_` (default) | `id` (unique), `timestamp` (desc), `outcome`, `risk_level`, `agent_name` |
| `compliance_standards` | Solo `_id_` (default) | `id` (unique), `code` (unique) |
| `chat_messages` | Solo `_id_` (default) | `session_id` + `timestamp` (compound) |

**Impatto**: Senza indici su `id`, ogni query `find_one({"id": ...})` fa un COLLSCAN. Con volumi reali (>10K documenti) le performance degraderanno significativamente.

### 3.3 Note su schema e tipi

| Aspetto | Stato | Dettaglio |
|---|---|---|
| Date come stringhe | **Si** | `created_at`, `updated_at`, `timestamp`, `last_assessment` sono tutte `str` ISO 8601 (non `datetime` nativo MongoDB) |
| `_id` duplicato | Presente | Ogni documento ha sia `_id` (ObjectId, auto-generato da MongoDB) che `id` (UUID string, generato dall'applicazione). Ridondanza. |
| Multi-tenancy | **Assente** | Nessun campo `tenant_id` o `organization_id`. Single-tenant. |
| Relazioni | **Deboli** | `policies.agent_id` e `audit_logs.agent_id` non sono enforced. Nessun indice, nessuna foreign key. |
| Denormalizzazioni | **Presente** | `audit_logs.agent_name` e `audit_logs.policy_name` sono denormalizzati (copiati invece di join). Rischio di disallineamento se l'entita originale viene rinominata. |
| DB name | `test_database` | Nome generico, evidentemente di default. Non rinominato per il progetto. |
| Schema validation | **Assente** | Nessun JSON Schema validator su MongoDB. I modelli Pydantic validano solo in entrata, non a livello DB. |

### 3.4 Campo `history` inutilizzato

In `server.py:434`, la variabile `history` viene letta dal database ma **mai passata al LLM**:
```python
history = await db.chat_messages.find(...)  # riga 434
# ... mai usata da chat.send_message()
```
Risultato: la chat LLM non ha contesto delle conversazioni precedenti, ogni messaggio e trattato come indipendente.

---

## 4. SICUREZZA

### 4.1 Meccanismi implementati

| Meccanismo | Stato |
|---|---|
| Autenticazione | **ASSENTE** — nessun sistema auth |
| Autorizzazione (RBAC) | **ASSENTE** — tutti gli endpoint sono pubblici |
| Rate limiting | **ASSENTE** — nessun throttling |
| CORS | Configurato ma `allow_origins="*"` (accetta tutto) |
| HTTPS | Gestito a livello Kubernetes Ingress (non applicativo) |
| Input sanitization | **Parziale** — Pydantic valida i tipi, ma nessuna sanitizzazione specifica |
| API key management | Chiave LLM in `.env`, non ruotata |

### 4.2 Tabella vulnerabilita

| ID | Severita | Priorita | Descrizione | File:Riga | Stato |
|---|---|---|---|---|---|
| V1 | **ALTA** | P0 | **Zero autenticazione**: tutti gli endpoint CRUD sono accessibili pubblicamente. Chiunque puo creare/eliminare agenti, policy, leggere audit trail. | `server.py:261-476` | Aperto |
| V2 | **ALTA** | P0 | **CORS wildcard**: `allow_origins="*"` consente richieste da qualsiasi dominio. In produzione permette attacchi CSRF. | `server.py:484` (`.env:3`) | Aperto |
| V3 | **ALTA** | P0 | **Chiave LLM esposta nel filesystem**: `EMERGENT_LLM_KEY` in `.env` senza crittografia. Se il server viene compromesso, la chiave e utilizzabile immediatamente. | `backend/.env:4` | Aperto |
| V4 | **ALTA** | P1 | **Regex injection**: il parametro `search` dell'audit trail viene passato direttamente a `$regex` MongoDB senza sanitizzazione. Un attaccante puo inviare pattern regex malevoli causando ReDoS. | `server.py:378-383` | Aperto |
| V5 | **MEDIA** | P1 | **Nessun rate limiting sugli endpoint**: possibile abuso dell'endpoint chat (costo LLM elevato per ogni richiesta) o flooding degli endpoint CRUD. | `server.py` (globale) | Aperto |
| V6 | **MEDIA** | P1 | **Errore LLM espone stacktrace**: `HTTPException(detail=f"AI service error: {str(e)}")` puo rivelare informazioni interne. | `server.py:444` | Aperto |
| V7 | **MEDIA** | P2 | **Nessuna validazione semantica**: i campi `risk_level`, `status`, `severity` accettano qualsiasi stringa (non sono enum Pydantic). Un client puo inviare `risk_level: "banana"`. | `server.py:36-127` | Aperto |
| V8 | **MEDIA** | P2 | **Nessun limite su lunghezza messaggi chat**: un utente puo inviare messaggi di dimensione arbitraria all'endpoint `/api/chat`, causando costi LLM eccessivi. | `server.py:126-128` | Aperto |
| V9 | **BASSA** | P2 | **Nessun header di sicurezza**: mancano Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security. | `server.py` (globale) | Aperto |
| V10 | **BASSA** | P3 | **DB name generico**: `test_database` puo essere indovinato facilmente. | `backend/.env:2` | Aperto |
| V11 | **BASSA** | P3 | **Nessun logging strutturato degli accessi**: le richieste HTTP non vengono loggate in formato strutturato (JSON). Difficile fare forensic analysis. | `server.py:30-32` | Aperto |

---

## 5. PERFORMANCE & SCALABILITA

### 5.1 Punti di forza

| Aspetto | Dettaglio |
|---|---|
| Backend completamente async | Motor + FastAPI: tutte le operazioni DB sono non-bloccanti |
| Frontend code splitting | React Router con import diretto (potenziale lazy loading) |
| Proiezione `_id: 0` | Correttamente escluso `_id` da tutte le query MongoDB |
| Pydantic V2 | Usa `model_dump()` (V2) non `dict()` (V1) — performance migliori |
| Glassmorphism via CSS | `backdrop-filter: blur()` offloaded alla GPU |

### 5.2 Colli di bottiglia

| ID | Area | Problema | Dove | Impatto |
|---|---|---|---|---|
| P1 | Database | **Nessun indice** su nessuna collection custom. Ogni query su `id` fa COLLSCAN. | Tutte le collections | Con >1K documenti: query lente (>100ms). Con >100K: inutilizzabile. |
| P2 | Dashboard | **7 query sequenziali** per la dashboard stats (count_documents x6 + find + aggregazione manuale). | `server.py:232-258` | Latenza proporzionale al numero di collection. Nessun caching. |
| P3 | Chat LLM | **Risposta sincrona** (no streaming). Il client attende ~8s per la risposta GPT-5.2 completa. | `server.py:440-441` | UX scadente: l'utente vede solo spinner per 8+ secondi. |
| P4 | Chat history | **History letta ma non usata**: si leggono fino a 20 messaggi (riga 434-436) che vengono scartati. Query inutile. | `server.py:434-436` | Spreco I/O su ogni chiamata chat. |
| P5 | Audit logs | **Nessuna paginazione reale** nel frontend. Il parametro `skip` esiste nel backend ma non e usato dal frontend. | `AuditPage.js` | Con 10K+ audit logs, la pagina carichera tutti i log (fino al limit di 50). |
| P6 | Seed data | **Seeding a ogni restart**: controlla `count_documents({}) == 0` ma se qualcuno cancella tutti i record, ri-semina dati demo. | `server.py:132-222` | Potenziale confusione in ambiente staging/produzione. |
| P7 | Frontend | **Nessun debounce** sulla ricerca audit trail. Ogni keystroke trigga una chiamata API. | `AuditPage.js:36-53` | Flood di richieste durante la digitazione. |
| P8 | Bundle size | **39 componenti Shadcn** importati nel progetto, ne vengono usati ~12. Tree-shaking CRA potrebbe non eliminarli tutti. | `components/ui/` | Bundle potenzialmente sovradimensionato. |

### 5.3 Raccomandazioni ordinate per priorita

| Priorita | Azione | Sforzo |
|---|---|---|
| 1 | Aggiungere indici MongoDB (`id` unique + campi filtro) | 30 min |
| 2 | Aggiungere debounce alla search (300ms) | 15 min |
| 3 | Aggregare dashboard stats in una singola pipeline MongoDB | 1h |
| 4 | Implementare streaming per chat LLM (SSE) | 2-3h |
| 5 | Rimuovere query `history` inutile o integrarla nel contesto LLM | 30 min |
| 6 | Aggiungere paginazione frontend per audit trail | 1-2h |

---

## 6. TESTING & QUALITA

### 6.1 Test automatici esistenti

| File | Tipo | Copertura | Risultato |
|---|---|---|---|
| `backend_test.py` | Test API end-to-end (requests) | 16 endpoint testati su 16 | **25/25 passati** (ultimo run) |
| `test_reports/iteration_1.json` | Report test automatizzati | Backend + Frontend integration | Tutti passati |
| `tests/__init__.py` | Placeholder | Vuoto | N/A |

**Nota**: `backend_test.py` e stato generato dal testing agent e NON e integrato in un framework (pytest). E uno script standalone che usa `requests`.

### 6.2 Cosa NON e coperto dai test

| Area | Dettaglio | Rischio |
|---|---|---|
| Unit test backend | Nessun test unitario per modelli Pydantic, logica di validazione, edge case | ALTO — regressioni non rilevate |
| Unit test frontend | Zero test React (jest/testing-library) | ALTO — nessun test su componenti, hook, context |
| Test di integrazione DB | Nessun test su query MongoDB, indici, concorrenza | MEDIO — query inefficienti non monitorate |
| Test negativi | Nessun test su input malformati, 404, 500, timeout LLM | ALTO — comportamento sconosciuto su errori |
| Test di sicurezza | Nessun test OWASP, injection, CORS abuse | CRITICO — vulnerabilita non monitorate |
| Test di performance | Nessun benchmark, load test, latency test | MEDIO — colli di bottiglia scoperti solo in produzione |
| Test i18n | Nessun test che le chiavi di traduzione IT/EN siano complete e sincronizzate | BASSO — stringhe mancanti = key mostrata raw |
| Accessibilita (a11y) | Nessun test WCAG | BASSO — ma richiesto da PA (cliente target) |

### 6.3 CI/CD

| Elemento | Stato |
|---|---|
| Dockerfile | **ASSENTE** — nessun Dockerfile nel progetto |
| docker-compose | **ASSENTE** |
| GitHub Actions | **ASSENTE** — nessuna directory `.github/workflows` |
| GitLab CI | **ASSENTE** |
| Jenkins | **ASSENTE** |
| Pre-commit hooks | **ASSENTE** |
| Linting automatico | **ASSENTE** — ESLint configurato in craco ma nessun script `lint` in package.json |
| Type checking | **ASSENTE** — frontend JS puro (non TypeScript), backend senza mypy in CI |

### 6.4 Qualita generale del codice

| Aspetto | Valutazione | Dettaglio |
|---|---|---|
| **Duplicazioni** | Medio-alta | AgentsPage/PoliciesPage condividono ~80% della struttura. Badge color maps ripetute in 4 file. |
| **Logging** | Minimale | Solo `logger.error` nella chat e `logger.info` nel seeding. Nessun logging strutturato per richieste HTTP. |
| **Error handling** | Insufficiente | Backend: un solo try/except (chat). Frontend: catch generico con `toast.error()` senza dettagli. |
| **Type safety** | Parziale | Backend: Pydantic valida i tipi ma non i valori (enum mancanti). Frontend: JS puro senza TypeScript. |
| **Commenti** | Minimi | Separatori di sezione (`# === AGENTS CRUD ===`) ma nessun docstring sulle funzioni. |
| **Naming** | Buono | Convenzioni consistenti: snake_case backend, camelCase frontend, kebab-case per data-testid. |
| **data-testid** | Eccellente | Presente su tutti gli elementi interattivi e strutturali. Naming chiaro. |
| **Responsive** | Buono | Grid responsive su landing e dashboard. Sidebar fissa (no hamburger mobile). |
| **Accessibilita** | Base | Shadcn usa Radix (aria nativo), ma nessun extra a11y custom. |

---

## 7. DEBITO TECNICO ATTUALE

| ID | Area | Problema | Impatto se non risolto | Sforzo stimato | Priorita |
|---|---|---|---|---|---|
| TD1 | Sicurezza | Zero autenticazione — tutti gli endpoint pubblici | Chiunque puo distruggere i dati in produzione | 4-8h (JWT base) | **P0** |
| TD2 | Sicurezza | CORS wildcard `*` | Attacchi CSRF possibili da qualsiasi dominio | 15 min | **P0** |
| TD3 | Sicurezza | Regex injection nella search audit | ReDoS attack, potenziale DoS | 30 min | **P0** |
| TD4 | Database | Zero indici custom — tutte COLLSCAN | Performance degradano a >1K documenti, inutilizzabile a >100K | 30 min | **P0** |
| TD5 | Backend | File monolite 491 righe (modelli + route + seed) | Ogni modifica tocca tutto, difficile lavorare in team | 2-3h (split in moduli) | **P1** |
| TD6 | Backend | Chat history letta ma non passata al LLM | L'assistente non ha memoria delle conversazioni — UX rotta | 30 min | **P1** |
| TD7 | Backend | Nessuna validazione enum sui campi (risk_level, status, severity) | Dati inconsistenti nel DB, filtri che non funzionano | 1h | **P1** |
| TD8 | Backend | API deprecate `@app.on_event("startup"/"shutdown")` | FastAPI raccomanda `lifespan` context manager; rimosso in versioni future | 30 min | **P1** |
| TD9 | Backend | Nessun rate limiting | Abuso API (flooding, costo LLM illimitato) | 1-2h (slowapi) | **P1** |
| TD10 | Frontend | Duplicazione AgentsPage/PoliciesPage (~80% identici) | Bug da fixare in 2 posti, inconsistenze | 2h (componente CRUD generico) | **P1** |
| TD11 | Frontend | Nessun debounce sulla ricerca audit | Flood di richieste API durante la digitazione | 15 min | **P1** |
| TD12 | Frontend | Traduzioni inline (227 righe in un file) | Non scalabile per nuove lingue, file enorme | 1h (file JSON separati) | **P2** |
| TD13 | Frontend | Markdown renderer custom rudimentale (chat) | Non gestisce bold inline, link, code block, tabelle | 1-2h (react-markdown) | **P2** |
| TD14 | Backend | Import inutilizzati (StreamingResponse, asyncio, json) | Nessun impatto runtime, ma sporcizia nel codice | 5 min | **P2** |
| TD15 | Frontend | Import lucide inutilizzati (Ban, Filter, X) | Bundle leggermente piu pesante | 5 min | **P2** |
| TD16 | Backend | Errore LLM espone stacktrace (`str(e)`) | Information disclosure | 10 min | **P2** |
| TD17 | Infra | Nessun Dockerfile/docker-compose | Non riproducibile localmente da altri dev | 1-2h | **P2** |
| TD18 | Infra | Nessun CI/CD pipeline | Test non automatizzati, deploy manuale | 2-4h | **P2** |
| TD19 | Database | Date come stringhe ISO anziché tipi nativi `datetime` | Query di range temporale inefficienti, sort lessicografico | 2h (migrazione) | **P2** |
| TD20 | Database | DB name `test_database` | Confusione ambiente, indovinabile | 5 min | **P3** |
| TD21 | Frontend | Sidebar non collassabile su mobile | UX mobile compromessa | 1-2h | **P3** |
| TD22 | Frontend | `App.css` vuoto (1 riga) | File morto | 1 min | **P3** |

---

## 8. ROADMAP SUGGERITA (3 STEP)

### Step 1: Fix critici e quick wins (P0/P1 a basso sforzo)
**Tempo stimato**: 1-2 giorni  
**Obiettivo**: Rendere il sistema sicuro e performante per demo/staging

| # | Azione | Sforzo | Riferimento |
|---|---|---|---|
| 1.1 | Aggiungere indici MongoDB su tutti i campi `id` (unique) + campi filtro | 30 min | TD4 |
| 1.2 | Sanitizzare input regex nella search audit (`re.escape()`) | 30 min | TD3 |
| 1.3 | Restringere CORS a domini specifici | 15 min | TD2 |
| 1.4 | Passare la chat history al contesto LLM | 30 min | TD6 |
| 1.5 | Aggiungere enum Pydantic per risk_level, status, severity, enforcement | 1h | TD7 |
| 1.6 | Aggiungere debounce alla search audit (300ms) | 15 min | TD11 |
| 1.7 | Rimuovere import inutilizzati (backend + frontend) | 10 min | TD14, TD15 |
| 1.8 | Migrare da `on_event` a `lifespan` context manager | 30 min | TD8 |
| 1.9 | Mascherare errori LLM (non esporre stacktrace) | 10 min | TD16 |

### Step 2: Refactoring strutturale e hardening
**Tempo stimato**: 3-5 giorni  
**Obiettivo**: Codebase manutenibile, sicura, pronta per team multi-persona

| # | Azione | Sforzo | Riferimento |
|---|---|---|---|
| 2.1 | Implementare autenticazione JWT (login/register + middleware protect) | 4-8h | TD1 |
| 2.2 | Splittare `server.py` in moduli: `models/`, `routes/`, `services/`, `seed.py` | 2-3h | TD5 |
| 2.3 | Estrarre componente CRUD generico per Agents/Policies | 2h | TD10 |
| 2.4 | Esternalizzare traduzioni in file JSON (`/locales/en.json`, `/locales/it.json`) | 1h | TD12 |
| 2.5 | Aggiungere rate limiting (slowapi) sugli endpoint critici (chat, CRUD) | 1-2h | TD9 |
| 2.6 | Aggiungere streaming SSE per risposte chat LLM | 2-3h | P3 |
| 2.7 | Scrivere test unitari: modelli Pydantic, edge case CRUD, input malformati | 4h | Copertura test |
| 2.8 | Convertire date in `datetime` nativo MongoDB (migrazione) | 2h | TD19 |
| 2.9 | Aggiungere react-markdown per rendering chat | 1h | TD13 |
| 2.10 | Aggiungere header di sicurezza (CSP, X-Frame-Options, HSTS) | 1h | V9 |

### Step 3: DevOps, integrazioni, feature avanzate
**Tempo stimato**: 1-2 settimane  
**Obiettivo**: Produzione-ready, integrazioni enterprise, feature differenzianti

| # | Azione | Sforzo | Riferimento |
|---|---|---|---|
| 3.1 | Creare Dockerfile + docker-compose per setup locale | 1-2h | TD17 |
| 3.2 | Configurare CI/CD (GitHub Actions: lint, test, build, deploy) | 2-4h | TD18 |
| 3.3 | RBAC: ruoli Admin, DPO, Auditor, Viewer con permessi granulari | 1-2 giorni | Backlog P0 |
| 3.4 | Dashboard con grafici temporali (recharts — gia installato) | 4-6h | Backlog P1 |
| 3.5 | Export PDF/CSV per audit trail e compliance report | 3-4h | Backlog P1 |
| 3.6 | Policy conflict detection engine | 1-2 giorni | Backlog P1 |
| 3.7 | Integrazione connettori enterprise (IAM, SIEM, ServiceNow) | 2-3 giorni/connettore | Backlog P2 |
| 3.8 | Multi-tenancy (organization-scoped data) | 2-3 giorni | Backlog P2 |
| 3.9 | Sidebar responsive con hamburger menu per mobile | 1-2h | TD21 |
| 3.10 | WebSocket per real-time agent monitoring | 1-2 giorni | Backlog P2 |

---

## 9. RIEPILOGO STATO PROGETTO

### Completato ✅

- Landing page completa con hero, features bento grid, settori target, CTA, footer
- Toggle lingua bilingue (EN/IT) funzionante su tutta l'applicazione
- Dashboard con sidebar e navigazione tra 6 sezioni
- Overview page con 4 KPI live (agenti, policy, audit, compliance score), attivita recente, distribuzione rischio
- CRUD completo per AI Agents (crea, leggi, modifica, elimina) con dialog form
- CRUD completo per Policy Engine con mapping a 6 normative (GDPR, AI Act, ISO 27001, ISO 42001, DORA, NIS2)
- Audit Trail con tabella densa, ricerca testuale, filtri per outcome e risk level
- Compliance Monitor con progress bar, stato per 6 standard normativi, date di revisione
- AI Compliance Assistant con GPT-5.2 reale (non mockato), chat bidirezionale, domande suggerite
- Ogni operazione CRUD genera automaticamente un audit log
- Dati seed realistici (4 agenti, 5 policy, 25 log audit, 6 standard compliance)
- Design system coerente: dark mode, Space Grotesk headings, JetBrains Mono code, glassmorphism
- Suite test API completa (25/25 passati)
- data-testid su tutti gli elementi interattivi

### Da completare 🔄

- **Autenticazione e RBAC** — sistema completamente aperto (P0)
- **Indici MongoDB** — nessun indice custom, performance a rischio (P0)
- **Sanitizzazione input regex** — vulnerabilita ReDoS (P0)
- **CORS restrittivo** — attualmente wildcard `*` (P0)
- **Contesto chat LLM** — history letta ma non passata (P1)
- **Rate limiting** — nessuna protezione contro abuso API (P1)
- **Enum validation** — campi accettano valori arbitrari (P1)
- **Refactoring backend** — monolite da splittare (P1)
- **Refactoring frontend** — duplicazione CRUD da eliminare (P1)
- **Streaming chat** — risposta LLM non in streaming (P2)
- **CI/CD pipeline** — assente (P2)
- **Dockerfile** — assente (P2)
- **Test unitari** — assenti (P2)
- **Dashboard charts** — recharts installato ma non usato (P2)
- **Export PDF/CSV** — non implementato (P2)
- **Connettori enterprise** (IAM, SIEM, ServiceNow) — non implementati (P2)
- **Multi-tenancy** — non implementato (P2)
- **Mobile sidebar** — non responsiva (P3)

---

*Fine audit tecnico. Documento generato analizzando il codice sorgente senza modifiche.*
