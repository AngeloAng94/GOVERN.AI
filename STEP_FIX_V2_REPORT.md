# STEP FIX V2 REPORT — GOVERN.AI

**Data**: 30 Marzo 2026  
**Versione**: MVP v1.9 -> v2.0  
**Fix implementati**: 2/2

---

## Bug #1 — Bar Chart "Audit Outcomes" (OverviewPage.js)

| | |
|---|---|
| **Problema** | Il grafico mostrava solo "Allowed" (Blocked e Escalated sempre 0) |
| **Root Cause** | `auditChartData` contava i log da `stats.recent_audit` (ultimi 5 log) invece di usare i totali gia disponibili in `stats.audit.blocked/escalated` |
| **Fix** | Sostituito il conteggio manuale con lettura diretta da `stats.audit.blocked`, `stats.audit.escalated`, e calcolo `allowed = total - blocked - escalated` |
| **File** | `frontend/src/pages/OverviewPage.js` (righe 93-103) |
| **Stato** | ✅ Verificato — Grafico mostra 3 barre coerenti con KPI card (389 events, 28 blocked) |

## Bug #2 — Delete senza conferma (CrudPage.js)

| | |
|---|---|
| **Problema** | Click su delete eliminava l'elemento immediatamente senza conferma |
| **Root Cause** | `onClick={onDelete}` chiamava `handleDelete` direttamente |
| **Fix** | Aggiunto stato `deleteConfirm`, redirect onClick a dialog, Dialog con "Cancel" e "Delete" |
| **File** | `frontend/src/components/CrudPage.js` |
| **Stato** | ✅ Verificato — Dialog appare con testo di conferma e bottoni Cancel/Delete |

## Test

| Test | Risultato |
|------|-----------|
| Backend pytest 22/22 | ✅ Passati |
| Bar chart 3 barre visibili | ✅ Allowed ~337, Blocked 28, Escalated visibile |
| Delete dialog visibile | ✅ "Confirm Delete" con Cancel e Delete |
| Cancel chiude dialog | ✅ |
| Delete effettua eliminazione | ✅ Solo dopo conferma |

---

**Stato finale**: MVP v2.0. Entrambi i bug risolti.
