# AGENTS.md — Jumba (sistema próprio)

Política canônica para agentes de IA neste repositório.

## Papel e fronteiras

Sistema próprio de análise de opções da B3, inspirado nas telas do Jumba e construído **exclusivamente com fontes públicas**.

- **Pesquisa, catálogo e vetores:** este repositório (`~/Projects/Jumba`) concentra o catálogo de telas (`docs/catalogo-telas.md`), o backlog (`docs/backlog.md`), a base de conhecimento da B3 (`docs/conhecimento/`), o desenho de tempo real (`docs/desenho/`), as fontes e transcrições (`docs/fontes/`) e os vetores de teste reproduzíveis (`docs/vetores/`).
- **Código de produção no Farol:** o motor de opções (BSM, Black-76, Garman-Kohlhagen, SVI, GEX/DEX), o DataHub e as telas do Portal moram em `~/Projects/Farol` e integram exclusivamente pelo portão local do Farol (`integrar.sh`).
- **Agentes de apoio no MeusAgentes:** definições e execuções de agentes moram em `~/Projects/MeusAgentes`.
- **Restrição B3:** nenhuma coleta automatizada vedada pela B3 deve ser disparada. Qualquer decisão sobre a fonte da base diária ou sobre o acervo histórico aguarda deliberação explícita do dono.
