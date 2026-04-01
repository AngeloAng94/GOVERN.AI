# STEP E4 — Policy Conflict Engine Report

**Data:** 01 Aprile 2026
**Versione:** MVP v2.4
**Status:** COMPLETATO

---

## Obiettivo
Motore di detection automatica di conflitti, gap e sovrapposizioni tra policy attive.
Trasforma GOVERN.AI da sistema di registrazione statico a motore attivo di governance AI.

## Conflitti Rilevati (Dati Demo)

| Tipo | Severita | Esempio | Agente |
|---|---|---|---|
| action_conflict | Critical | Block vs Auto su stesse conditions | Fraud Detection Engine |
| gap | High | Nessuna policy assegnata | Customer Due Diligence Bot |
| gap | High | Nessuna policy assegnata | DORA Incident Responder |
| gap | High | Nessuna policy assegnata | KYC Verification Agent |
| gap | High | Nessuna policy assegnata | Dirigente Preposto Assistant |
| overlap | High | 2 policy GDPR con rule_type diverso | AML Transaction Monitor |
| overlap | High | 2 policy SOX con rule_type diverso | SOX Internal Control Auditor |
| overlap | High | 2 policy DORA con rule_type diverso | Fraud Detection Engine |
| redundancy | Low | Conditions identiche su 2 policy | Fraud Detection Engine |

## API Endpoints

| Metodo | Endpoint | Ruolo Min | Rate Limit | Descrizione |
|---|---|---|---|---|
| GET | /api/policy-engine/conflicts | auditor | - | Scan real-time conflitti |
| POST | /api/policy-engine/conflicts/{id}/resolve | dpo | - | Risolvi conflitto |
| GET | /api/policy-engine/scan-history | viewer | - | Ultimi 10 scan |

## Algoritmo Detection

1. **Action Conflict** — Due policy sullo stesso agente con conditions sovrapposte ed enforcement opposto (block vs auto)
2. **Gap** — Agenti critical/high risk senza alcuna policy assegnata
3. **Overlap** — Stessa normativa sullo stesso agente con rule_type diversi
4. **Redundancy** — Due policy con agent_id e conditions identiche

## Test Results
- **Backend pytest:** 34/34 passed
- **Testing agent:** 100% pass rate (frontend + backend)
- **Report:** `/app/test_reports/iteration_7.json`
