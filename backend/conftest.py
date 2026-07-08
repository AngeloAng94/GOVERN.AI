"""
Pytest hooks per la trasparenza della copertura LLM.

Obiettivo: la CI NON deve poter mostrare un badge "verde" nascondendo il fatto
che i path LLM (Performance / Sovereign Apertus) non sono stati esercitati.
Quando un test marcato `llm` o `sovereign` viene SKIPPED (tipicamente per
assenza delle API key), stampiamo un WARNING esplicito nel riepilogo finale.
"""

_LLM_MARKERS = ("llm", "sovereign")


def _skip_reason(report) -> str:
    lr = getattr(report, "longrepr", None)
    # Per gli skip, longrepr e' una tupla (path, lineno, "Skipped: <msg>")
    if isinstance(lr, tuple) and len(lr) == 3:
        return str(lr[2]).replace("Skipped: ", "").strip()
    return str(lr) if lr else "no reason provided"


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    skipped = terminalreporter.stats.get("skipped", [])
    llm_skipped = [
        r for r in skipped
        if any(m in getattr(r, "keywords", {}) for m in _LLM_MARKERS)
    ]
    if not llm_skipped:
        return

    tw = terminalreporter
    tw.write_sep("=", "LLM COVERAGE WARNING", red=True, bold=True)
    tw.write_line(
        "I seguenti test LLM NON sono stati eseguiti (SKIPPED). Le chiamate reali "
        "verso i provider AI non sono state verificate:",
        red=True,
    )
    for r in llm_skipped:
        tw.write_line(f"  \u26a0 SKIPPED: {r.nodeid} \u2014 {_skip_reason(r)}", yellow=True)
    tw.write_line(
        "La CI NON deve considerare questa run pienamente verde: valorizzare le API "
        "key (OPENAI_API_KEY / PUBLICAI_API_KEY) per esercitare i path LLM.",
        red=True,
    )
