# ANTHERA Systems — Strategia Apertus

## Sovereign European AI come Cuore dell'Ecosistema ANTHERA

**Versione**: 1.0
**Data**: 14 Maggio 2026
**Autore**: ANTHERA Systems
**Destinatari**: Founder, Investor, Compliance Officer, Solution Architect, Procurement IT

---

## Executive Summary

ANTHERA Systems sceglie **Apertus** — il Large Language Model open-source sviluppato da **ETH Zurich + EPFL + CSCS** (Swiss National Supercomputing Centre) — come **motore AI di default** per tutti i prodotti del proprio ecosistema, a partire da **GOVERN.AI**.

Questa scelta non e tecnica, ma **strategica e identitaria**: i dati europei restano in Europa, l'intelligenza che li elabora e europea, e l'intera supply chain AI e trasparente, ispezionabile e conforme.

**In una frase**: *"European data deserves European AI."*

---

## 1. Perche Apertus — Il Razionale ANTHERA

### 1.1 Il problema attuale

Le imprese europee che adottano AI affrontano un dilemma:

| Esigenza | LLM US (GPT/Claude) | Conseguenza |
|----------|---------------------|-------------|
| Dati personali GDPR | Trasferimento extra-UE | Data Processing Addendum complesso, rischio Schrems III |
| Sovranita dati DORA | Outsourcing critico | Notifica all'autorita, contingency plan |
| Trasparenza EU AI Act Art. 13/53 | Training data segreto | Impossibile attestare provenienza |
| Resilienza NIS2 | Dipendenza supplier USA | Single point of failure geopolitico |
| Procurement PA | Cloud Act USA | Esclusione da gare strategiche |

### 1.2 La risposta ANTHERA

Apertus risolve tutti questi attriti **in un colpo solo**:

- **100% trasparente** (pesi + dati + ricetta di training pubblici)
- **Sovrano EU/CH** (training su supercomputer Alps a Lugano, hosting EU)
- **Multilingua nativo** (italiano, tedesco, francese, romancio al pari di inglese)
- **Apache 2.0** (zero vendor lock-in, free per uso commerciale)
- **Allineato a EU AI Act** by design (non retrofit)

### 1.3 Il messaggio commerciale ANTHERA

> *"I tuoi dati sono europei. La governance e europea. L'AI che li elabora deve esserlo anche essa."*

Questa narrativa diventa **moltiplicatore di vendita**:
- Banche italiane (vincoli Banca d'Italia + ECB)
- Pubblica Amministrazione (procurement AGID, sovranita)
- Sanita (dati paziente, art. 9 GDPR)
- Difesa / infrastrutture critiche (NIS2 supplier chain)
- Settore pubblico CH/EU (Public AI Inference Utility Swisscom)

---

## 2. Cos'e Apertus — Scheda Tecnica

### 2.1 Identita

| Attributo | Valore |
|-----------|--------|
| **Nome** | Apertus (dal latino "aperto") |
| **Sviluppatori** | ETH Zurich, EPFL, CSCS (Swiss National Supercomputing Centre) |
| **Sponsor** | Swiss Confederation, Swiss AI Initiative |
| **Rilascio** | Settembre 2025 |
| **Licenza** | Apache 2.0 (commercial-friendly) |
| **Sito** | apertus.ai |
| **Modelli disponibili** | Apertus-8B-Instruct, Apertus-70B-Instruct |
| **Lingue supportate** | 1.800+ (italiano, tedesco, francese, romancio nativi) |
| **Trained on** | Supercomputer Alps (CSCS Lugano) — 10.000+ NVIDIA GH200 |
| **Trasparenza** | Pesi + dataset + training recipe + code completamente pubblici |
| **Compliance** | EU AI Act Article 13/53 ready, GDPR-friendly |

### 2.2 Caratteristiche distintive

1. **Fully Open**: e il primo LLM di scala enterprise dove **tutto** e pubblico (non solo i pesi)
2. **Multilingua bilanciato**: a differenza di GPT/Claude (90% inglese), Apertus tratta italiano e tedesco come lingue di prima classe
3. **Auditabilita**: ogni decisione del modello e tracciabile fino al dato di training
4. **Indipendenza geopolitica**: fuori dal perimetro del Cloud Act USA, del CHIPS Act, di sanzioni extraterritoriali

### 2.3 Posizionamento vs concorrenza

| Caratteristica | GPT-4o | Claude 3.5 | Gemini 2.0 | **Apertus 70B** |
|----------------|--------|------------|------------|------------------|
| Licenza | Proprietaria | Proprietaria | Proprietaria | **Apache 2.0** |
| Pesi pubblici | No | No | No | **Si** |
| Training data pubblico | No | No | No | **Si** |
| Sovranita EU/CH | No (US) | No (US) | No (US) | **Si (CH)** |
| Multilingua IT first-class | Parziale | Parziale | Parziale | **Si** |
| EU AI Act Art. 13 ready | Complesso | Complesso | Complesso | **Nativo** |
| Cloud Act USA | Si | Si | Si | **No** |
| Self-hosting | No | No | No | **Si** |
| Costo | Alto | Alto | Medio | **Free (infra cost only)** |

---

## 3. Architettura di Integrazione ANTHERA

### 3.1 Principio: abstraction layer

ANTHERA gia utilizza **litellm** in tutti i prodotti come **layer di astrazione LLM-agnostic**. Questo rende l'adozione di Apertus **trasparente** dal punto di vista del codice applicativo.

```
┌────────────────────────────────────────────────────────┐
│              APPLICAZIONE (es. GOVERN.AI)               │
│           routes/chat.py -> ARIA Assistant              │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                       litellm                           │
│      Abstraction layer LLM-agnostic + streaming         │
└────────────┬────────────────────┬──────────────────────┘
             │                    │
             ▼                    ▼
   ┌──────────────────┐   ┌──────────────────┐
   │  Apertus-70B     │   │  GPT-4o          │
   │  (SOVEREIGN)     │   │  (FALLBACK)      │
   │  Public AI Swiss │   │  OpenAI US       │
   │  o vLLM EU       │   │  (opzionale)     │
   └──────────────────┘   └──────────────────┘
```

### 3.2 Switch via variabile d'ambiente

L'integrazione si limita a:

```bash
# backend/.env
LLM_PROVIDER=apertus
LLM_MODEL=apertus/apertus-70b-instruct
LLM_BASE_URL=https://api.publicai.swiss/v1
APERTUS_API_KEY=<chiave>
```

**Zero modifiche al codice applicativo.** Il routing avviene a livello di litellm.

### 3.3 Modalita operativa proposta (Dual Mode)

Per massimizzare flessibilita commerciale, ANTHERA suggerisce di esporre nella UI un **toggle "Sovereign Mode"**:

| Modalita | Modello | Use case |
|----------|---------|----------|
| **Sovereign Mode** (default) | Apertus 70B | Produzione, dati sensibili, clienti EU/CH |
| **Performance Mode** (opt-in) | GPT-4o / Claude | Task molto complessi, prototipi |
| **Offline Mode** | Apertus 8B via Ollama | Demo on-prem, ambienti air-gapped |

Questa scelta diventa **argomento di vendita killer**: *"Vuoi sovranita totale? Sovereign Mode. Vuoi qualita massima? Performance Mode. La scelta e tua, in 1 click."*

---

## 4. Opzioni di Deployment — Passo Passo

### 4.1 Opzione A — Public AI Inference Utility (Swisscom) **CONSIGLIATA**

**Scenario**: SaaS produzione, zero ops, sovranita CH dichiarata.

**Step**:
1. Registrarsi su `publicai.swiss` (Swiss Public AI Inference Utility, in beta)
2. Ottenere API key
3. Configurare:
   ```bash
   LLM_MODEL=apertus/apertus-70b-instruct
   LLM_BASE_URL=https://api.publicai.swiss/v1
   APERTUS_API_KEY=<key>
   ```
4. Verificare endpoint con curl di smoke test
5. Riavviare il backend

**Tempo**: ~2 ore (incluso onboarding Swisscom)
**Costo**: pricing per token, in linea con OpenAI ma sovrano CH
**Pro**: zero infra, SLA enterprise, conformita CH/EU certificata
**Contro**: dipendenza singolo provider (mitigato dal fatto che e ente pubblico CH)

---

### 4.2 Opzione B — Hugging Face Inference Endpoints

**Scenario**: prototipazione veloce, pilota cliente.

**Step**:
1. Account su `huggingface.co`
2. Deploy "Apertus-70B-Instruct" su Inference Endpoints (regione EU: Frankfurt o Helsinki)
3. Ottenere URL endpoint + token
4. Configurare:
   ```bash
   LLM_MODEL=huggingface/apertus-70b-instruct
   LLM_BASE_URL=https://<endpoint>.eu-west-1.aws.endpoints.huggingface.cloud
   HUGGINGFACE_API_KEY=<token>
   ```

**Tempo**: ~3 ore
**Costo**: ~2-4 USD/ora di GPU A100 attiva (auto-scaling)
**Pro**: deploy in 10 minuti, infra EU
**Contro**: HF e USA-based corporation (mitigato: hosting in EU + Apache license del modello)

---

### 4.3 Opzione C — Self-Hosted vLLM su GPU EU **MAX SOVRANITA**

**Scenario**: enterprise, banche, PA, clienti sensibili.

**Step**:
1. Provisioning GPU EU: OVH (Strasburgo/Roubaix), Aruba (Italia), Open Telekom (DE), Scaleway (FR), o on-prem
2. Hardware minimo: 2x NVIDIA H100 80GB (per 70B), 1x A100 40GB (per 8B)
3. Installazione vLLM:
   ```bash
   pip install vllm
   python -m vllm.entrypoints.openai.api_server \
     --model swiss-ai/Apertus-70B-Instruct-2509 \
     --port 8000 \
     --tensor-parallel-size 2
   ```
4. Configurare GOVERN.AI:
   ```bash
   LLM_MODEL=openai/apertus-70b-instruct
   LLM_BASE_URL=http://<vllm-host>:8000/v1
   OPENAI_API_KEY=dummy   # vLLM accetta qualsiasi key
   ```

**Tempo**: 1-2 giorni (incluso setup GPU + benchmark)
**Costo**: ~3.000-8.000 EUR/mese GPU H100 dedicata (oppure CAPEX ~50k EUR on-prem)
**Pro**: sovranita totale, zero dipendenza esterna, latenza ottima
**Contro**: ops overhead, capex/opex GPU

---

### 4.4 Opzione D — Ollama On-Prem (Apertus 8B)

**Scenario**: demo locale, sviluppatori, ambienti air-gapped.

**Step**:
1. Installare Ollama (`brew install ollama` o equivalente Linux)
2. `ollama pull apertus:8b`
3. `ollama serve` (porta 11434)
4. Configurare:
   ```bash
   LLM_MODEL=ollama/apertus:8b
   LLM_BASE_URL=http://localhost:11434/v1
   ```

**Tempo**: 30 minuti
**Costo**: zero (gira anche su MacBook M3 con 32 GB RAM)
**Pro**: demo offline, zero costi, privacy massima
**Contro**: solo 8B (qualita inferiore), non scalabile per produzione

---

## 5. Roadmap di Adozione ANTHERA

### Fase 1 — GOVERN.AI (Q2 2026)

- Integrare Apertus come opzione configurabile in GOVERN.AI (~1 sprint)
- UI toggle "Sovereign Mode" nelle Settings
- Aggiornare documentazione + Investor Intro: "Powered by Sovereign European AI"
- Demo a pilota cliente banking IT con Sovereign Mode attivo

### Fase 2 — Validazione produzione (Q3 2026)

- Selezionare 1 design partner enterprise per pilota Apertus 70B su Public AI Swiss
- Misurare: latenza, qualita risposte ARIA, soddisfazione utente
- Confronto blind A/B vs GPT-4o
- Pubblicazione case study

### Fase 3 — Estensione a tutto l'ecosistema ANTHERA (Q4 2026 — Q1 2027)

- Default Apertus su ogni nuovo prodotto ANTHERA
- Retrofit prodotti esistenti se applicabile
- Partnership formale con Swiss AI Initiative / CSCS
- ANTHERA come "Apertus Premier Partner" (titolo proposto)

### Fase 4 — Go-to-market sovranita (2027)

- Apertura mercato CH (Swisscom, UBS, Credit Suisse legacy, PA federale)
- Apertura mercato DE/AT (BaFin, Bundesbank, Vienna Stock Exchange)
- Apertura mercato FR (CNIL, ACPR, settore difesa)

---

## 6. Compliance — Mappatura Apertus vs Normative

| Normativa | Articolo | Come Apertus aiuta |
|-----------|----------|---------------------|
| **EU AI Act** | Art. 13 (Transparency) | Training data pubblico -> attestazione immediata |
| **EU AI Act** | Art. 53 (GPAI Models) | GPAI con technical documentation completa gia disponibile |
| **GDPR** | Art. 44 (Trasferimenti) | Hosting EU/CH -> nessun trasferimento extra-UE |
| **GDPR** | Art. 35 (DPIA) | DPIA semplificata grazie a trasparenza modello |
| **DORA** | Art. 28 (ICT Third-party) | Supplier EU/CH critico approvabile dal CdA |
| **NIS2** | Art. 21 (Supply Chain) | Supply chain sovrana, non US-dipendente |
| **D.Lgs. 262** | Internal Controls | Modello auditabile per Dirigente Preposto |
| **ISO 42001** | AI Management | Trasparenza modello = controllo lifecycle facilitato |
| **Cloud Act USA** | N/A | Apertus fuori giurisdizione USA |

---

## 7. Costo Totale di Ownership (TCO) — Esempio

**Scenario**: GOVERN.AI in produzione con 50 utenti concorrenti, 100.000 query LLM/mese.

| Voce | GPT-4o (OpenAI) | Apertus 70B (Public AI CH) | Apertus 70B (Self-host vLLM EU) |
|------|------------------|----------------------------|----------------------------------|
| Costo modello | ~3.000 EUR/mese | ~2.000 EUR/mese | 0 EUR/mese |
| Costo infra | 0 | 0 | ~5.000 EUR/mese (2x H100) |
| Costo compliance | Alto (DPA, valutazioni) | Basso | Minimo |
| Ops overhead | Basso | Basso | Medio |
| **TCO mensile** | **~3.000 EUR + compliance** | **~2.000 EUR** | **~5.000 EUR** |
| **TCO sovranita** | Bassa | Alta | Massima |
| **Vendor lock-in** | Alto | Medio | Zero |

---

## 8. FAQ

### 8.1 Apertus e davvero al livello di GPT-4o?

**Apertus-70B** e competitivo con **GPT-4-turbo / Claude 3.5 Sonnet** sui benchmark multilingua europei (Llama-3-Eval, EU-Truthful, ItaEval). E leggermente sotto GPT-4o su task molto complessi di reasoning, ma per i casi d'uso di ARIA (Q&A normativo, sintesi, guidance) la differenza e marginale e compensata dal multilingua nativo.

### 8.2 Quanto costa la migrazione tecnica?

**Zero o quasi**, grazie a litellm. Bastano 1-2 ore di un developer per testare l'endpoint Apertus e validare ARIA con qualche prompt rappresentativo.

### 8.3 E se Public AI Swiss avesse downtime?

Litellm supporta **fallback automatico**: configuriamo Apertus come primario e GPT-4o come fallback. Zero impatto sull'utente finale.

### 8.4 Posso usare Apertus per generare PDF/CSV?

Si, esattamente come oggi con GPT. La generazione e gestita lato ReportLab/Python, non dal LLM. Il LLM serve solo per il ragionamento normativo di ARIA.

### 8.5 Apertus risponde in italiano correttamente?

**Si, eccellentemente.** A differenza di GPT (che traduce dall'inglese internamente), Apertus tratta l'italiano come lingua di prima classe nel training. La qualita stilistica e legale italiana e superiore.

### 8.6 Possiamo addestrare un fine-tune su normative italiane?

Si, Apertus e Apache 2.0 e i pesi sono pubblici. Possiamo fare LoRA fine-tune su corpus normativo italiano (codice civile, codice penale, GDPR, leggi finanziarie) per creare un *"ARIA Legal Italian Edition"*. Costo: ~5-10k EUR di GPU + 1 settimana di lavoro.

### 8.7 E se OpenAI lancia un modello migliore?

Litellm permette di scegliere modello **per ogni richiesta**. Non perdiamo nulla: avremo sempre la possibilita di usare il meglio del mercato come opt-in, ma il default sovrano EU resta Apertus.

### 8.8 Apertus puo essere usato per i prodotti commerciali ANTHERA?

**Si, Apache 2.0** consente uso commerciale illimitato. Nessun obbligo di rilascio del codice ANTHERA che usa Apertus.

---

## 9. Prossimi Passi Operativi

1. **Valutazione Public AI Swiss**: registrazione, contatto Swisscom, ottenimento API key di test
2. **Smoke test su GOVERN.AI** (ambiente dev): cambio variabili env, validazione streaming ARIA
3. **Benchmark blind**: 20 prompt normativi -> confronto GPT-4o vs Apertus 70B -> scoring qualita
4. **Decisione GO/NO-GO** entro fine Q2 2026
5. **Roll-out production** Q3 2026 con UI toggle "Sovereign Mode"
6. **Comunicazione esterna**: aggiornamento sito ANTHERA, press release "ANTHERA adotta Apertus"
7. **Estensione a portfolio ANTHERA** Q4 2026

---

## 10. Conclusione

L'adozione di **Apertus** non e una scelta tecnica: e una **dichiarazione identitaria**.

ANTHERA Systems esiste per portare la sovranita digitale in Europa. Un prodotto di governance AI che gira su LLM US tradisce la propria missione. Con Apertus, ANTHERA diventa **end-to-end European**:

- **Dati europei** -> ospitati in EU/CH
- **Codice europeo** -> open source compliance-first
- **AI europea** -> Apertus, sviluppato e ospitato in Svizzera
- **Governance europea** -> conforme EU AI Act / GDPR / DORA / NIS2 per design

> *"Sovereign Control Plane for Enterprise AI, powered by Sovereign European AI."*

Questa e la promessa che ANTHERA puo mantenere — **a partire da oggi**.

---

## Contatti

**Angelo Anglani** — Founder, ANTHERA Systems
- angelo.anglani94@gmail.com
- +39 342 754 8655
- linkedin.com/in/angelo-anglani

**Riferimenti Apertus**:
- apertus.ai
- huggingface.co/swiss-ai
- publicai.swiss (Swiss Public AI Inference Utility)
- ethz.ch / epfl.ch / cscs.ch

---

*ANTHERA Systems — European data deserves European AI.*
*Documento strategico — 14 Maggio 2026 — v1.0*
