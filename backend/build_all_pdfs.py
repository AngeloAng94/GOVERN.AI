"""
Master script: regenerate ALL GOVERN.AI / ANTHERA PDFs with the new
institutional design (pdf_theme.py).

Outputs (in /app):
- GOVERN_AI_Investor_Intro_IT.pdf
- GOVERN_AI_Investor_Intro_EN.pdf
- AUDIT_TECNICO_GOVERN.pdf
- GOVERN_AI_Technical_Overview.pdf
- GOVERN_AI_USER_MANUAL_IT.pdf
- GOVERN_AI_USER_MANUAL_EN.pdf
- ANTHERA_APERTUS_STRATEGY_IT.pdf
- ANTHERA_APERTUS_STRATEGY_EN.pdf
"""
import os
import sys

# Make local modules importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_investor_pdf_v2 import build_investor_pdf
from pdf_md_renderer import render_md_to_pdf


APP = "/app"


def write(path: str, data: bytes) -> str:
    with open(path, "wb") as f:
        f.write(data)
    return f"{path}  ({len(data):,} bytes)"


def main():
    print("\n== INVESTOR INTRO ==")
    print(" ", write(f"{APP}/GOVERN_AI_Investor_Intro_IT.pdf", build_investor_pdf("it")))
    print(" ", write(f"{APP}/GOVERN_AI_Investor_Intro_EN.pdf", build_investor_pdf("en")))

    print("\n== AUDIT TECNICO ==")
    n = render_md_to_pdf(
        md_path=f"{APP}/AUDIT_TECNICO_GOVERN.md",
        output_path=f"{APP}/AUDIT_TECNICO_GOVERN.pdf",
        brand_top="GOVERN.AI",
        doc_type="Audit Tecnico",
        version="v3.1 - Sovereign Mode",
        date_str="21 Maggio 2026",
        tagline="European data deserves European AI.",
        intro_callout=("Audit tecnico interno della piattaforma GOVERN.AI. "
                       "Aggiornato a valle del rilascio Sovereign Mode (v3.1)."),
    )
    print(f"  {APP}/AUDIT_TECNICO_GOVERN.pdf  ({n:,} bytes)")

    print("\n== TECHNICAL OVERVIEW ==")
    n = render_md_to_pdf(
        md_path=f"{APP}/GOVERN_AI_TECHNICAL_OVERVIEW.md",
        output_path=f"{APP}/GOVERN_AI_Technical_Overview.pdf",
        brand_top="GOVERN.AI",
        doc_type="Technical Overview",
        version="MVP v3.1",
        date_str="21 Maggio 2026",
        tagline="Sovereign Control Plane for Enterprise AI.",
        intro_callout=("Documento tecnico-funzionale destinato a CTO, Solution Architect "
                       "e Compliance Officer. Allineato alla release v3.1."),
    )
    print(f"  {APP}/GOVERN_AI_Technical_Overview.pdf  ({n:,} bytes)")

    print("\n== USER MANUAL ==")
    n = render_md_to_pdf(
        md_path=f"{APP}/GOVERN_AI_USER_MANUAL_IT.md",
        output_path=f"{APP}/GOVERN_AI_USER_MANUAL_IT.pdf",
        brand_top="GOVERN.AI",
        doc_type="Manuale Operativo",
        version="MVP v3.1",
        date_str="21 Maggio 2026",
        tagline="Manuale completo - utente, implementazione, deploy.",
        intro_callout=("Guida operativa completa: utilizzo della piattaforma, "
                       "estensione tecnica, deploy in produzione."),
    )
    print(f"  {APP}/GOVERN_AI_USER_MANUAL_IT.pdf  ({n:,} bytes)")
    n = render_md_to_pdf(
        md_path=f"{APP}/GOVERN_AI_USER_MANUAL_EN.md",
        output_path=f"{APP}/GOVERN_AI_USER_MANUAL_EN.pdf",
        brand_top="GOVERN.AI",
        doc_type="Operational Manual",
        version="MVP v3.1",
        date_str="21 May 2026",
        tagline="Complete manual - user, implementation, deploy.",
        intro_callout=("Complete operational guide: platform usage, "
                       "technical extension, production deployment."),
    )
    print(f"  {APP}/GOVERN_AI_USER_MANUAL_EN.pdf  ({n:,} bytes)")

    print("\n== APERTUS STRATEGY ==")
    n = render_md_to_pdf(
        md_path=f"{APP}/ANTHERA_APERTUS_STRATEGY_IT.md",
        output_path=f"{APP}/ANTHERA_APERTUS_STRATEGY_IT.pdf",
        brand_top="ANTHERA",
        brand_bottom="x  APERTUS",
        doc_type="Strategia Sovereign European AI",
        version="v1.0",
        date_str="14 Maggio 2026",
        tagline="European data deserves European AI.",
        classification="Strategic / Confidential",
        intro_callout=("Documento strategico di adozione di Apertus come motore AI sovrano "
                       "dell'ecosistema ANTHERA Systems."),
    )
    print(f"  {APP}/ANTHERA_APERTUS_STRATEGY_IT.pdf  ({n:,} bytes)")
    n = render_md_to_pdf(
        md_path=f"{APP}/ANTHERA_APERTUS_STRATEGY_EN.md",
        output_path=f"{APP}/ANTHERA_APERTUS_STRATEGY_EN.pdf",
        brand_top="ANTHERA",
        brand_bottom="x  APERTUS",
        doc_type="Sovereign European AI Strategy",
        version="v1.0",
        date_str="14 May 2026",
        tagline="European data deserves European AI.",
        classification="Strategic / Confidential",
        intro_callout=("Strategic adoption document for Apertus as the sovereign AI engine "
                       "of the ANTHERA Systems ecosystem."),
    )
    print(f"  {APP}/ANTHERA_APERTUS_STRATEGY_EN.pdf  ({n:,} bytes)")

    print("\n== DONE ==")


if __name__ == "__main__":
    main()
