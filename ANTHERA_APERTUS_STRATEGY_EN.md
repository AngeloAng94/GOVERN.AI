# ANTHERA Systems — Apertus Strategy

## Sovereign European AI as the Heart of the ANTHERA Ecosystem

**Version**: 1.0
**Date**: 14 May 2026
**Author**: ANTHERA Systems
**Audience**: Founder, Investor, Compliance Officer, Solution Architect, IT Procurement

---

## Executive Summary

ANTHERA Systems selects **Apertus** — the open-source Large Language Model developed by **ETH Zurich + EPFL + CSCS** (Swiss National Supercomputing Centre) — as the **default AI engine** for all products in its ecosystem, starting with **GOVERN.AI**.

This is not a technical choice; it is a **strategic and identity-defining** one: European data stays in Europe, the intelligence processing it is European, and the entire AI supply chain is transparent, inspectable and compliant.

**In one sentence**: *"European data deserves European AI."*

---

## 1. Why Apertus — The ANTHERA Rationale

### 1.1 The current problem

European enterprises adopting AI face a dilemma:

| Requirement | US LLM (GPT/Claude) | Consequence |
|-------------|---------------------|-------------|
| GDPR personal data | Extra-EU transfer | Complex Data Processing Addendum, Schrems III risk |
| DORA data sovereignty | Critical outsourcing | Authority notification, contingency plan |
| EU AI Act Art. 13/53 transparency | Secret training data | Impossible to attest provenance |
| NIS2 resilience | US supplier dependency | Geopolitical single point of failure |
| Public sector procurement | US Cloud Act | Exclusion from strategic tenders |

### 1.2 The ANTHERA answer

Apertus resolves all of these frictions **in one shot**:

- **100% transparent** (public weights + training data + recipe)
- **Sovereign EU/CH** (trained on Alps supercomputer in Lugano, EU hosting)
- **Natively multilingual** (Italian, German, French, Romansh on par with English)
- **Apache 2.0** (zero vendor lock-in, free for commercial use)
- **EU AI Act aligned by design** (not retrofit)

### 1.3 The ANTHERA commercial message

> *"Your data is European. Your governance is European. The AI processing it must be European too."*

This narrative becomes a **sales multiplier**:
- Italian banks (Bank of Italy + ECB requirements)
- Public Administration (AGID procurement, sovereignty)
- Healthcare (patient data, GDPR Art. 9)
- Defence / critical infrastructure (NIS2 supplier chain)
- Public sector CH/EU (Public AI Inference Utility by Swisscom)

---

## 2. What Apertus Is — Technical Datasheet

### 2.1 Identity

| Attribute | Value |
|-----------|-------|
| **Name** | Apertus (Latin for "open") |
| **Developers** | ETH Zurich, EPFL, CSCS (Swiss National Supercomputing Centre) |
| **Sponsor** | Swiss Confederation, Swiss AI Initiative |
| **Release** | September 2025 |
| **License** | Apache 2.0 (commercial-friendly) |
| **Site** | apertus.ai |
| **Available models** | Apertus-8B-Instruct, Apertus-70B-Instruct |
| **Supported languages** | 1,800+ (Italian, German, French, Romansh natively) |
| **Trained on** | Alps supercomputer (CSCS Lugano) — 10,000+ NVIDIA GH200 |
| **Transparency** | Weights + dataset + training recipe + code fully public |
| **Compliance** | EU AI Act Article 13/53 ready, GDPR-friendly |

### 2.2 Distinctive features

1. **Fully Open**: it is the first enterprise-scale LLM where **everything** is public (not only the weights)
2. **Balanced multilingual**: unlike GPT/Claude (90% English), Apertus treats Italian and German as first-class languages
3. **Auditability**: every model decision is traceable to training data
4. **Geopolitical independence**: outside the perimeter of US Cloud Act, CHIPS Act, extraterritorial sanctions

### 2.3 Positioning vs competition

| Feature | GPT-4o | Claude 3.5 | Gemini 2.0 | **Apertus 70B** |
|---------|--------|------------|------------|------------------|
| License | Proprietary | Proprietary | Proprietary | **Apache 2.0** |
| Public weights | No | No | No | **Yes** |
| Public training data | No | No | No | **Yes** |
| EU/CH sovereignty | No (US) | No (US) | No (US) | **Yes (CH)** |
| First-class IT multilingual | Partial | Partial | Partial | **Yes** |
| EU AI Act Art. 13 ready | Complex | Complex | Complex | **Native** |
| US Cloud Act | Yes | Yes | Yes | **No** |
| Self-hosting | No | No | No | **Yes** |
| Cost | High | High | Medium | **Free (infra cost only)** |

---

## 3. ANTHERA Integration Architecture

### 3.1 Principle: abstraction layer

ANTHERA already uses **litellm** across all products as an **LLM-agnostic abstraction layer**. This makes Apertus adoption **transparent** to the application code.

```
┌────────────────────────────────────────────────────────┐
│              APPLICATION (e.g. GOVERN.AI)               │
│            routes/chat.py -> ARIA Assistant             │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│                       litellm                           │
│         LLM-agnostic abstraction + streaming            │
└────────────┬────────────────────┬──────────────────────┘
             │                    │
             ▼                    ▼
   ┌──────────────────┐   ┌──────────────────┐
   │  Apertus-70B     │   │  GPT-4o          │
   │  (SOVEREIGN)     │   │  (FALLBACK)      │
   │  Public AI Swiss │   │  OpenAI US       │
   │  or vLLM EU      │   │  (optional)      │
   └──────────────────┘   └──────────────────┘
```

### 3.2 Switch via environment variable

Integration is limited to:

```bash
# backend/.env
LLM_PROVIDER=apertus
LLM_MODEL=apertus/apertus-70b-instruct
LLM_BASE_URL=https://api.publicai.swiss/v1
APERTUS_API_KEY=<key>
```

**Zero application code changes.** Routing happens at the litellm layer.

### 3.3 Suggested operating mode (Dual Mode)

To maximize commercial flexibility, ANTHERA suggests exposing a **"Sovereign Mode" toggle** in the UI:

| Mode | Model | Use case |
|------|-------|----------|
| **Sovereign Mode** (default) | Apertus 70B | Production, sensitive data, EU/CH clients |
| **Performance Mode** (opt-in) | GPT-4o / Claude | Very complex tasks, prototypes |
| **Offline Mode** | Apertus 8B via Ollama | On-prem demo, air-gapped environments |

This becomes a **killer sales argument**: *"Want total sovereignty? Sovereign Mode. Want max quality? Performance Mode. Your choice, in 1 click."*

---

## 4. Deployment Options — Step by Step

### 4.1 Option A — Public AI Inference Utility (Swisscom) **RECOMMENDED**

**Scenario**: SaaS production, zero ops, declared CH sovereignty.

**Steps**:
1. Register on `publicai.swiss` (Swiss Public AI Inference Utility, beta)
2. Obtain API key
3. Configure:
   ```bash
   LLM_MODEL=apertus/apertus-70b-instruct
   LLM_BASE_URL=https://api.publicai.swiss/v1
   APERTUS_API_KEY=<key>
   ```
4. Smoke-test endpoint with curl
5. Restart backend

**Time**: ~2 hours (incl. Swisscom onboarding)
**Cost**: per-token pricing, in line with OpenAI but CH-sovereign
**Pros**: zero infra, enterprise SLA, certified CH/EU compliance
**Cons**: single-provider dependency (mitigated by CH public entity)

---

### 4.2 Option B — Hugging Face Inference Endpoints

**Scenario**: rapid prototyping, customer pilot.

**Steps**:
1. Account on `huggingface.co`
2. Deploy "Apertus-70B-Instruct" on Inference Endpoints (EU region: Frankfurt or Helsinki)
3. Obtain endpoint URL + token
4. Configure:
   ```bash
   LLM_MODEL=huggingface/apertus-70b-instruct
   LLM_BASE_URL=https://<endpoint>.eu-west-1.aws.endpoints.huggingface.cloud
   HUGGINGFACE_API_KEY=<token>
   ```

**Time**: ~3 hours
**Cost**: ~2-4 USD/hour of active A100 GPU (auto-scaling)
**Pros**: deploy in 10 minutes, EU infra
**Cons**: HF is US-based corp (mitigated: EU hosting + Apache license on the model)

---

### 4.3 Option C — Self-Hosted vLLM on EU GPU **MAX SOVEREIGNTY**

**Scenario**: enterprise, banks, public administration, sensitive clients.

**Steps**:
1. EU GPU provisioning: OVH (Strasbourg/Roubaix), Aruba (Italy), Open Telekom (DE), Scaleway (FR), or on-prem
2. Minimum hardware: 2x NVIDIA H100 80GB (for 70B), 1x A100 40GB (for 8B)
3. vLLM installation:
   ```bash
   pip install vllm
   python -m vllm.entrypoints.openai.api_server \
     --model swiss-ai/Apertus-70B-Instruct-2509 \
     --port 8000 \
     --tensor-parallel-size 2
   ```
4. Configure GOVERN.AI:
   ```bash
   LLM_MODEL=openai/apertus-70b-instruct
   LLM_BASE_URL=http://<vllm-host>:8000/v1
   OPENAI_API_KEY=dummy   # vLLM accepts any key
   ```

**Time**: 1-2 days (incl. GPU setup + benchmark)
**Cost**: ~3,000-8,000 EUR/month dedicated H100 (or CAPEX ~50k EUR on-prem)
**Pros**: total sovereignty, zero external dependency, optimal latency
**Cons**: ops overhead, GPU capex/opex

---

### 4.4 Option D — Ollama On-Prem (Apertus 8B)

**Scenario**: local demo, developers, air-gapped environments.

**Steps**:
1. Install Ollama (`brew install ollama` or Linux equivalent)
2. `ollama pull apertus:8b`
3. `ollama serve` (port 11434)
4. Configure:
   ```bash
   LLM_MODEL=ollama/apertus:8b
   LLM_BASE_URL=http://localhost:11434/v1
   ```

**Time**: 30 minutes
**Cost**: zero (runs on a MacBook M3 with 32 GB RAM)
**Pros**: offline demo, zero cost, maximum privacy
**Cons**: 8B only (lower quality), not scalable for production

---

## 5. ANTHERA Adoption Roadmap

### Phase 1 — GOVERN.AI (Q2 2026)

- Integrate Apertus as a configurable option in GOVERN.AI (~1 sprint)
- "Sovereign Mode" toggle in Settings UI
- Update documentation + Investor Intro: "Powered by Sovereign European AI"
- Pilot demo with an IT banking customer with Sovereign Mode active

### Phase 2 — Production validation (Q3 2026)

- Select 1 enterprise design partner for Apertus 70B pilot on Public AI Swiss
- Measure: latency, ARIA response quality, user satisfaction
- Blind A/B comparison vs GPT-4o
- Case study publication

### Phase 3 — Extension to the entire ANTHERA ecosystem (Q4 2026 — Q1 2027)

- Apertus as default on every new ANTHERA product
- Retrofit existing products where applicable
- Formal partnership with Swiss AI Initiative / CSCS
- ANTHERA as "Apertus Premier Partner" (proposed title)

### Phase 4 — Sovereignty go-to-market (2027)

- CH market opening (Swisscom, UBS, legacy Credit Suisse, federal PA)
- DE/AT market opening (BaFin, Bundesbank, Vienna Stock Exchange)
- FR market opening (CNIL, ACPR, defence sector)

---

## 6. Compliance — Apertus vs Regulations Mapping

| Regulation | Article | How Apertus helps |
|------------|---------|--------------------|
| **EU AI Act** | Art. 13 (Transparency) | Public training data -> immediate attestation |
| **EU AI Act** | Art. 53 (GPAI Models) | GPAI with complete technical documentation already available |
| **GDPR** | Art. 44 (Transfers) | EU/CH hosting -> no extra-EU transfer |
| **GDPR** | Art. 35 (DPIA) | Simplified DPIA thanks to model transparency |
| **DORA** | Art. 28 (ICT Third-party) | Critical EU/CH supplier approvable by the Board |
| **NIS2** | Art. 21 (Supply Chain) | Sovereign supply chain, not US-dependent |
| **D.Lgs. 262** | Internal Controls | Auditable model for Dirigente Preposto |
| **ISO 42001** | AI Management | Model transparency = easier lifecycle control |
| **US Cloud Act** | N/A | Apertus outside US jurisdiction |

---

## 7. Total Cost of Ownership (TCO) — Example

**Scenario**: GOVERN.AI in production with 50 concurrent users, 100,000 LLM queries/month.

| Item | GPT-4o (OpenAI) | Apertus 70B (Public AI CH) | Apertus 70B (Self-host vLLM EU) |
|------|------------------|----------------------------|----------------------------------|
| Model cost | ~3,000 EUR/month | ~2,000 EUR/month | 0 EUR/month |
| Infra cost | 0 | 0 | ~5,000 EUR/month (2x H100) |
| Compliance cost | High (DPA, assessments) | Low | Minimal |
| Ops overhead | Low | Low | Medium |
| **Monthly TCO** | **~3,000 EUR + compliance** | **~2,000 EUR** | **~5,000 EUR** |
| **Sovereignty TCO** | Low | High | Maximum |
| **Vendor lock-in** | High | Medium | Zero |

---

## 8. FAQ

### 8.1 Is Apertus really at GPT-4o level?

**Apertus-70B** is competitive with **GPT-4-turbo / Claude 3.5 Sonnet** on European multilingual benchmarks (Llama-3-Eval, EU-Truthful, ItaEval). It is slightly below GPT-4o on very complex reasoning tasks, but for ARIA use cases (regulatory Q&A, summary, guidance) the difference is marginal and offset by native multilingual quality.

### 8.2 How much does the technical migration cost?

**Zero or near-zero**, thanks to litellm. 1-2 hours of a developer are enough to test the Apertus endpoint and validate ARIA with representative prompts.

### 8.3 What if Public AI Swiss has downtime?

Litellm supports **automatic fallback**: configure Apertus as primary and GPT-4o as fallback. Zero impact on the end user.

### 8.4 Can I use Apertus to generate PDF/CSV?

Yes, exactly as today with GPT. Generation is handled on the ReportLab/Python side, not by the LLM. The LLM is only used for ARIA's regulatory reasoning.

### 8.5 Does Apertus respond correctly in Italian?

**Yes, excellently.** Unlike GPT (which internally translates from English), Apertus treats Italian as a first-class language in training. Italian stylistic and legal quality is superior.

### 8.6 Can we fine-tune on Italian regulations?

Yes, Apertus is Apache 2.0 and weights are public. We can LoRA fine-tune on Italian regulatory corpus (civil code, criminal code, GDPR, financial laws) to create *"ARIA Legal Italian Edition"*. Cost: ~5-10k EUR GPU + 1 week of work.

### 8.7 What if OpenAI launches a better model?

Litellm allows model choice **per request**. We lose nothing: we will always have the option to use the best of the market as opt-in, but the sovereign EU default remains Apertus.

### 8.8 Can Apertus be used in ANTHERA commercial products?

**Yes, Apache 2.0** allows unlimited commercial use. No obligation to release ANTHERA code using Apertus.

---

## 9. Operational Next Steps

1. **Public AI Swiss evaluation**: registration, Swisscom contact, test API key
2. **Smoke test on GOVERN.AI** (dev env): env vars switch, ARIA streaming validation
3. **Blind benchmark**: 20 regulatory prompts -> GPT-4o vs Apertus 70B -> quality scoring
4. **GO/NO-GO decision** by end of Q2 2026
5. **Production roll-out** Q3 2026 with "Sovereign Mode" UI toggle
6. **External communication**: ANTHERA website update, press release "ANTHERA adopts Apertus"
7. **ANTHERA portfolio extension** Q4 2026

---

## 10. Conclusion

The adoption of **Apertus** is not a technical choice: it is an **identity-defining statement**.

ANTHERA Systems exists to bring digital sovereignty to Europe. An AI governance product running on US LLMs betrays its own mission. With Apertus, ANTHERA becomes **end-to-end European**:

- **European data** -> hosted in EU/CH
- **European code** -> compliance-first open source
- **European AI** -> Apertus, developed and hosted in Switzerland
- **European governance** -> EU AI Act / GDPR / DORA / NIS2 compliant by design

> *"Sovereign Control Plane for Enterprise AI, powered by Sovereign European AI."*

This is the promise ANTHERA can keep — **starting today**.

---

## Contacts

**Angelo Anglani** — Founder, ANTHERA Systems
- angelo.anglani94@gmail.com
- +39 342 754 8655
- linkedin.com/in/angelo-anglani

**Apertus references**:
- apertus.ai
- huggingface.co/swiss-ai
- publicai.swiss (Swiss Public AI Inference Utility)
- ethz.ch / epfl.ch / cscs.ch

---

*ANTHERA Systems — European data deserves European AI.*
*Strategy document — 14 May 2026 — v1.0*
