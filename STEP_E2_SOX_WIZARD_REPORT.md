# STEP E2 — SOX Section 404 Wizard Report

**Data:** 01 Aprile 2026
**Versione:** MVP v2.2
**Status:** COMPLETATO

---

## Obiettivo
Implementare una pagina dedicata `/dashboard/sox-wizard` che guidi l'utente attraverso una checklist strutturata
dei controlli SOX Section 404, tracci lo stato di ogni controllo, generi report per gli auditor, e si integri
con l'audit trail esistente.

## File Modificati / Creati

### Backend
| File | Azione | Descrizione |
|---|---|---|
| `models.py` | Modificato | Aggiunto `ControlStatus` enum e `SoxControl` model |
| `routes/sox_wizard.py` | Creato | 4 endpoint: GET controls, PATCH control, GET report JSON, GET report PDF |
| `seed.py` | Modificato | `seed_sox_controls()` con 20 controlli in 5 domini |
| `exporters.py` | Modificato | `SoxReportPDFBuilder` per report PDF Section 404 |
| `server.py` | Modificato | Registrato `sox_router` |
| `routes/chat.py` | Modificato | ARIA prompt aggiornato con SOX 404 Wizard |
| `tests/test_api.py` | Modificato | 4 nuovi test SOX (28 totali) |

### Frontend
| File | Azione | Descrizione |
|---|---|---|
| `pages/SoxWizardPage.js` | Creato | Pagina completa wizard SOX 404 |
| `App.js` | Modificato | Route `/dashboard/sox-wizard` + import + page title |
| `pages/DashboardLayout.js` | Modificato | Voce sidebar "SOX 404" con ClipboardCheck |
| `locales/en.json` | Modificato | 24 chiavi `sox_*` aggiunte |
| `locales/it.json` | Modificato | 24 chiavi `sox_*` aggiunte (tradotte) |

## Seed Data (20 Controlli, 5 Domini)

| Dominio | Controlli | Completati | In Corso | Non Iniziati | Falliti |
|---|---|---|---|---|---|
| Access Control | AC-01..04 | 2 | 2 | 0 | 0 |
| Change Management | CM-01..04 | 1 | 2 | 1 | 0 |
| IT Operations | OP-01..04 | 1 | 1 | 1 | 1 |
| Data Integrity | DI-01..04 | 1 | 3 | 0 | 0 |
| Security | SE-01..04 | 0 | 1 | 2 | 1 |
| **Totale** | **20** | **5** | **9** | **4** | **2** |

## Test Results
- **Backend pytest:** 28/28 passed
- **Testing agent:** 100% pass rate (frontend + backend)
- **Report:** `/app/test_reports/iteration_5.json`

## API Endpoints

| Metodo | Endpoint | Ruolo Minimo | Descrizione |
|---|---|---|---|
| GET | `/api/sox/controls` | viewer | Lista controlli raggruppati per dominio |
| PATCH | `/api/sox/controls/{id}` | auditor | Aggiorna controllo + audit log |
| GET | `/api/sox/report` | viewer | Report JSON strutturato |
| GET | `/api/sox/report/pdf` | dpo | Report PDF (rate limit: 5/min) |
